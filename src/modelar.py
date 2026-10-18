"""Banco de experimentos: compara grupos de variables y modelos con los mismos folds.

Validacion principal: 5 folds estratificados por Estado, repetidos 10 veces (50 ajustes por
configuracion). Prueba de robustez espacial: folds agrupados por municipio (una parcela nunca
se evalua con vecinas de su mismo municipio en entrenamiento).

Las variables de ubicacion que usan el rendimiento (media de vecinos kNN, media de zona) se
calculan DENTRO de cada fold solo con las parcelas de entrenamiento del fold, para no filtrar
el objetivo.

Entrada: data/processed/features_parcela.csv (src/features.py)
Salida:  reports/experimentos.md, reports/experimentos.csv
Uso:     .venv/Scripts/python.exe src/modelar.py [--rapido]
"""
import argparse
import re
import warnings
from pathlib import Path

import lightgbm as lgb
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel, WhiteKernel
from sklearn.impute import SimpleImputer
from sklearn.linear_model import RidgeCV
from sklearn.model_selection import GroupKFold, RepeatedStratifiedKFold
from sklearn.neighbors import KNeighborsRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[1]
FEAT = ROOT / "data" / "processed" / "features_parcela.csv"
R = "RENDIMIENTO_T_HA"
ALPHAS = np.logspace(-1, 3, 25)
K_VECINOS = 8


# ----------------------------------------------------------------------------- grupos
def grupos_de(cols):
    pl_stats = [c for c in cols if re.fullmatch(r"(ndvi|evi|lai|msavi)_(mean|std|max|min)", c)]
    return {
        "xy": ["x_km", "y_km"],
        "vecinos": ["vecinos_knn", "media_zona"],  # se calculan en el fold
        "planet_stats": pl_stats,
        "planet_feno": [c for c in cols if c.startswith("planet_") and not c.endswith("n_obs")],
        # fenologia compacta: ventanas y forma de la curva de los indices con mas senal (EDA)
        "feno_core": [c for c in cols if re.fullmatch(
            r"(planet_(evi|lai)|s2_(savi|lai|msi))_(may_jun|jul_sep|oct_nov|auc_abr_oct|doy_inicio|"
            r"duracion|pico|pend_bajada)", c)],
        "s2": [c for c in cols if c.startswith("s2_") and not c.endswith("n_obs")],
        "clima": ["prec_abr_oct", "tmax_media_abr_oct", "tmin_media_abr_oct", "prec_anomalia"],
        "relieve": ["elev_mean", "pend_mean", "elev_std"],
    }


# ----------------------------------------------------------------------------- modelos
def ridge():
    return make_pipeline(SimpleImputer(strategy="median"), StandardScaler(), RidgeCV(alphas=ALPHAS))


def bosque():
    return make_pipeline(SimpleImputer(strategy="median"),
                         RandomForestRegressor(400, min_samples_leaf=3, max_features=0.33,
                                               random_state=0, n_jobs=-1))


def lgbm():
    return make_pipeline(SimpleImputer(strategy="median"),
                         lgb.LGBMRegressor(n_estimators=300, learning_rate=0.03, num_leaves=7,
                                           min_child_samples=8, subsample=0.8, subsample_freq=1,
                                           colsample_bytree=0.5, reg_lambda=5.0, verbose=-1,
                                           random_state=0))


def gpr():
    """Proceso gaussiano: RBF sobre las variables estandarizadas + ruido blanco. Con pocas
    variables (ubicacion + relieve) se comporta como un kriging con tendencia."""
    k = ConstantKernel(0.5) * RBF(length_scale=1.0) + WhiteKernel(0.2)
    return make_pipeline(SimpleImputer(strategy="median"), StandardScaler(),
                         GaussianProcessRegressor(k, normalize_y=True, n_restarts_optimizer=2,
                                                  random_state=0))


MODELOS = {"ridge": ridge, "rf": bosque, "lgbm": lgbm, "gpr": gpr}


# ----------------------------------------------------------------------------- CV
def vecinos_fold(tr, te):
    """Media ponderada por distancia del rendimiento de los k vecinos de entrenamiento + media de
    zona. Para las parcelas de entrenamiento se usa leave-one-out (no se cuenta a si misma)."""
    knn = KNeighborsRegressor(K_VECINOS, weights="distance").fit(tr[["x_km", "y_km"]], tr[R])
    loo = KNeighborsRegressor(K_VECINOS + 1).fit(tr[["x_km", "y_km"]], tr[R])
    d, i = loo.kneighbors(tr[["x_km", "y_km"]])
    d, i = d[:, 1:], i[:, 1:]  # quitar el propio punto (distancia 0)
    w = 1.0 / np.maximum(d, 1e-3)
    tr_v = (w * tr[R].to_numpy()[i]).sum(1) / w.sum(1)
    te_v = knn.predict(te[["x_km", "y_km"]])
    mz = tr.groupby("zona")[R].mean()
    nz, sz = tr.groupby("zona")[R].transform("size"), tr.groupby("zona")[R].transform("sum")
    tr_z = ((sz - tr[R]) / (nz - 1)).to_numpy()
    te_z = te["zona"].map(mz).fillna(tr[R].mean()).to_numpy()
    return (tr_v, tr_z), (te_v, te_z)


def folds(df, modo, reps):
    """Lista de repeticiones; cada repeticion es una lista de (idx_train, idx_test)."""
    if modo == "municipio":
        gkf = GroupKFold(n_splits=min(10, df["Municipio"].nunique()))
        return [list(gkf.split(df, groups=df["Municipio"]))]
    rskf = RepeatedStratifiedKFold(n_splits=5, n_repeats=reps, random_state=42)
    sp = list(rskf.split(df, df["Estado"]))
    return [sp[r * 5:(r + 1) * 5] for r in range(reps)]


def evaluar(df, cols, modelo, reps, usa_vecinos):
    """Devuelve (rmse, sd_rmse, mae, r2) promediados entre repeticiones y la matriz de
    predicciones fuera de fold (n_rep x n)."""
    y = df[R].to_numpy()
    rmses, maes, r2s, oofs = [], [], [], []
    for splits in reps:
        oof = np.full(len(df), np.nan)
        for tr_i, te_i in splits:
            tr, te = df.iloc[tr_i].copy(), df.iloc[te_i].copy()
            if usa_vecinos:
                (tr["vecinos_knn"], tr["media_zona"]), (te["vecinos_knn"], te["media_zona"]) = \
                    vecinos_fold(tr, te)
            m = modelo().fit(tr[cols], tr[R])
            oof[te_i] = m.predict(te[cols])
        e = y - oof
        rmses.append(np.sqrt(np.mean(e ** 2)))
        maes.append(np.mean(np.abs(e)))
        r2s.append(1 - np.sum(e ** 2) / np.sum((y - y.mean()) ** 2))
        oofs.append(oof)
    return (np.mean(rmses), np.std(rmses), np.mean(maes), np.mean(r2s)), np.array(oofs)


# ----------------------------------------------------------------------------- experimentos
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rapido", action="store_true", help="3 repeticiones en vez de 10")
    a = ap.parse_args()
    reps = 3 if a.rapido else 10

    df = pd.read_csv(FEAT)
    df = df[df["CONJUNTO"] == "ENTRENAMIENTO"].reset_index(drop=True)
    G = grupos_de(df.columns)
    sp_main = folds(df, "estratificada", reps)
    sp_muni = folds(df, "municipio", 1)
    y = df[R].to_numpy()
    resultados = []

    def correr(nombre, grupos, modelo_nom, bloque, muni=True):
        cols = sum((G[g] for g in grupos), [])
        usa_v = "vecinos" in grupos
        (rm, sd, ma, r2), oof = evaluar(df, cols, MODELOS[modelo_nom], sp_main, usa_v)
        fila = {"bloque": bloque, "experimento": nombre, "modelo": modelo_nom,
                "grupos": "+".join(grupos), "n_vars": len(cols),
                "rmse": rm, "rmse_sd": sd, "mae": ma, "r2": r2}
        if muni:
            (rm2, _, _, r22), _ = evaluar(df, cols, MODELOS[modelo_nom], sp_muni, usa_v)
            fila["rmse_municipio"], fila["r2_municipio"] = rm2, r22
        resultados.append(fila)
        print(f"  {bloque:11s} {nombre:46s} {modelo_nom:5s} n={len(cols):3d}  RMSE {rm:.3f}±{sd:.3f}"
              f"  MAE {ma:.3f}  R2 {r2:.3f}" + (f"  | muni {fila['rmse_municipio']:.3f}" if muni else ""))
        return oof

    # --- referencias
    print("Referencias")
    resultados.append({"bloque": "referencia", "experimento": "media global (V0)", "modelo": "-",
                       "grupos": "-", "n_vars": 0, "rmse": 0.851, "rmse_sd": 0, "mae": 0.751,
                       "r2": -0.018, "rmse_municipio": np.nan, "r2_municipio": np.nan})
    ident = lambda: make_pipeline(StandardScaler(), RidgeCV(alphas=[1e-6]))  # noqa: E731
    (rm, sd, ma, r2), _ = evaluar(df, ["vecinos_knn"], ident, sp_main, True)
    (rm2, _, _, r22), _ = evaluar(df, ["vecinos_knn"], ident, sp_muni, True)
    resultados.append({"bloque": "referencia", "experimento": "kNN espacial (k=8)", "modelo": "knn",
                       "grupos": "vecinos", "n_vars": 1, "rmse": rm, "rmse_sd": sd, "mae": ma, "r2": r2,
                       "rmse_municipio": rm2, "r2_municipio": r22})
    print(f"  media global (V0): RMSE 0.851\n  kNN espacial k=8: RMSE {rm:.3f}±{sd:.3f} MAE {ma:.3f} "
          f"R2 {r2:.3f} | muni {rm2:.3f}")

    print("\nA. Cada grupo de variables por separado")
    for g in ["xy", "vecinos", "planet_stats", "planet_feno", "feno_core", "s2", "clima", "relieve"]:
        for mn in ["ridge", "lgbm"]:
            correr(f"solo {g}", [g], mn, "A_grupo")
    correr("solo xy", ["xy"], "gpr", "A_grupo")

    print("\nB. Ubicacion (vecinos + xy) + cada grupo")
    loc = ["vecinos", "xy"]
    for g in ["planet_stats", "planet_feno", "feno_core", "s2", "clima", "relieve"]:
        for mn in ["ridge", "lgbm"]:
            correr(f"ubicacion + {g}", loc + [g], mn, "B_loc+grupo")
    for g in ["feno_core", "clima", "relieve"]:
        correr(f"ubicacion + {g}", loc + [g], "gpr", "B_loc+grupo")

    print("\nC. Combinaciones")
    U, UR, UF = "ubicacion", "ubicacion + relieve + clima", "ubicacion + feno_core + relieve + clima"
    UP = "ubicacion + planet_feno + clima + relieve"
    combos = {
        U: (loc, ["ridge", "rf", "lgbm", "gpr"]),
        UR: (loc + ["relieve", "clima"], ["ridge", "rf", "lgbm", "gpr"]),
        UF: (loc + ["feno_core", "relieve", "clima"], ["ridge", "rf", "lgbm", "gpr"]),
        UP: (loc + ["planet_feno", "clima", "relieve"], ["ridge", "rf", "lgbm"]),
        "ubicacion + satelite + clima + relieve": (loc + ["planet_feno", "s2", "clima", "relieve"],
                                                  ["ridge", "rf", "lgbm"]),
        "todo sin ubicacion": (["planet_stats", "planet_feno", "s2", "clima", "relieve"],
                               ["ridge", "rf", "lgbm"]),
        "todo": (loc + ["planet_stats", "planet_feno", "s2", "clima", "relieve"], ["ridge", "rf", "lgbm"]),
    }
    oofs = {}
    for nombre, (grupos, modelos) in combos.items():
        for mn in modelos:
            oofs[(nombre, mn)] = correr(nombre, grupos, mn, "C_combo")

    def ens(nombre, partes):
        p = np.mean([oofs[k] for k in partes], axis=0)  # n_rep x n
        e = y[None, :] - p
        rm = np.sqrt((e ** 2).mean(1))
        resultados.append({"bloque": "D_ensamble", "experimento": nombre, "modelo": "ens",
                           "grupos": " | ".join(f"{a}/{b}" for a, b in partes), "n_vars": np.nan,
                           "rmse": rm.mean(), "rmse_sd": rm.std(), "mae": np.abs(e).mean(),
                           "r2": (1 - (e ** 2).sum(1) / ((y - y.mean()) ** 2).sum()).mean()})
        print(f"  {nombre:62s} RMSE {rm.mean():.3f}±{rm.std():.3f}")

    print("\nD. Ensambles (promedio de predicciones fuera de fold, todas las repeticiones)")
    ens("gpr(ubic) + lgbm(ubic+relieve+clima)", [(U, "gpr"), (UR, "lgbm")])
    ens("gpr(ubic) + lgbm(ubic+feno+relieve+clima)", [(U, "gpr"), (UF, "lgbm")])
    ens("gpr + lgbm (ubic+relieve+clima)", [(UR, "gpr"), (UR, "lgbm")])
    ens("gpr + lgbm + rf (ubic+relieve+clima)", [(UR, "gpr"), (UR, "lgbm"), (UR, "rf")])
    ens("gpr + lgbm (ubic+feno+relieve+clima)", [(UF, "gpr"), (UF, "lgbm")])
    ens("gpr + lgbm + rf (ubic+feno+relieve+clima)", [(UF, "gpr"), (UF, "lgbm"), (UF, "rf")])
    ens("gpr + lgbm + rf + ridge (ubic+feno+relieve+clima)",
        [(UF, "gpr"), (UF, "lgbm"), (UF, "rf"), (UF, "ridge")])
    ens("lgbm(ubic+relieve+clima) + rf(ubic+planet_feno+clima+relieve)", [(UR, "lgbm"), (UP, "rf")])
    ens("gpr(ubic) + lgbm(ubic+relieve+clima) + rf(ubic+planet_feno+clima+relieve)",
        [(U, "gpr"), (UR, "lgbm"), (UP, "rf")])

    print("\nE. Pregunta guia 1: cada indice por separado (sus variables fenologicas)")
    for sensor, idxs in [("planet", ["ndvi", "evi", "lai", "msavi"]),
                         ("s2", ["ndvi", "evi", "savi", "lai", "fapar", "ndwi", "msi", "ndti"])]:
        for idx in idxs:
            G[f"idx_{sensor}_{idx}"] = [c for c in df.columns if c.startswith(f"{sensor}_{idx}_")
                                       and not c.endswith("n_obs")]
            correr(f"indice {sensor}:{idx} solo", [f"idx_{sensor}_{idx}"], "lgbm", "E_indice", muni=False)
            correr(f"ubicacion + indice {sensor}:{idx}", loc + [f"idx_{sensor}_{idx}"], "lgbm", "E_indice",
                   muni=False)

    print("\nF. Pregunta guia 2: cada variable climatica")
    for v in G["clima"]:
        G[f"clima_{v}"] = [v]
        correr(f"clima {v} solo", [f"clima_{v}"], "lgbm", "F_clima", muni=False)
        correr(f"ubicacion + {v}", loc + [f"clima_{v}"], "lgbm", "F_clima", muni=False)

    res = pd.DataFrame(resultados)
    res.to_csv(ROOT / "reports" / "experimentos.csv", index=False)
    escribir_md(res, reps)
    print("\nGuardado en reports/experimentos.md y .csv")


def escribir_md(res, reps):
    def tabla(sub, cols):
        s = sub[cols].copy()
        for c in s.columns:
            if s[c].dtype.kind == "f":
                s[c] = s[c].round(3)
        return s.to_markdown(index=False)

    cols_full = ["experimento", "modelo", "n_vars", "rmse", "rmse_sd", "mae", "r2", "rmse_municipio"]
    cols_corto = ["experimento", "modelo", "n_vars", "rmse", "rmse_sd", "mae", "r2"]
    partes = [
        "# Banco de experimentos",
        f"Validación principal: 5 folds estratificados por estado × {reps} repeticiones (RMSE promedio "
        "entre repeticiones; `rmse_sd` = desviación entre repeticiones). `rmse_municipio`: CV agrupada "
        "por municipio (prueba espacial más exigente: ninguna parcela se evalúa con vecinas de su "
        "municipio en entrenamiento). Las variables de vecinos (kNN k=8 ponderado por distancia, "
        "media de zona) se calculan dentro de cada fold. Diferencias de RMSE menores a ~0.03 están "
        "dentro del ruido.\n",
        "## Referencias", tabla(res[res.bloque == "referencia"], cols_full),
        "\n## A. Cada grupo de variables por separado", tabla(res[res.bloque == "A_grupo"], cols_full),
        "\n## B. Ubicación + cada grupo", tabla(res[res.bloque == "B_loc+grupo"], cols_full),
        "\n## C. Combinaciones", tabla(res[res.bloque == "C_combo"], cols_full),
        "\n## D. Ensambles", tabla(res[res.bloque == "D_ensamble"], ["experimento", "rmse", "rmse_sd", "mae", "r2"]),
        "\n## E. Pregunta guía 1: índice más importante", tabla(res[res.bloque == "E_indice"], cols_corto),
        "\n## F. Pregunta guía 2: variable climática", tabla(res[res.bloque == "F_clima"], cols_corto),
    ]
    (ROOT / "reports" / "experimentos.md").write_text("\n".join(partes), encoding="utf-8")


if __name__ == "__main__":
    main()
