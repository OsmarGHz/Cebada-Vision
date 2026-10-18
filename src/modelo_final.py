"""Modelo final CebadaVision: ensamble de LightGBM + Random Forest con variables de ubicacion,
relieve, clima y fenologia de Planet. Entrena con las 138 parcelas, predice las 197 y deja todo
lo que necesitan la app, el CSV para FIRA y el reporte.

Modelo (ver reports/experimentos.md, bloque D):
  M1  LightGBM  ubicacion (vecinos kNN, media de zona, x, y) + relieve + clima           (11 vars)
  M2  RandomForest  ubicacion + fenologia Planet (ndvi/evi/lai/msavi) + clima + relieve   (91 vars)
  prediccion = promedio(M1, M2), recortada al rango plausible [1.5, 6.5] t/ha

Validacion: 5 folds estratificados por estado x 10 repeticiones; la media de vecinos se calcula
dentro de cada fold. Reporta tambien la CV agrupada por municipio.

Salidas (data/processed/):
  predicciones_197.csv   ID, conjunto, estado, rendimiento real, prediccion, intervalo 80 %,
                         prediccion fuera de muestra (promedio de las 10 repeticiones)
  modelo_final.json      metricas, importancias por permutacion, ablacion por grupos
                         (pregunta guia 3), respuestas a las preguntas guia, simulador lineal
                         sustituto, umbrales del semaforo, contribuciones SHAP por parcela
  submissions/predicciones_59_CebadaVision.csv   lo que se manda a FIRA (4 decimales)
Uso:  .venv/Scripts/python.exe src/modelo_final.py
"""
import json
import sys
import warnings
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd
import shap
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler

sys.path.insert(0, str(Path(__file__).resolve().parent))
from modelar import MODELOS, R, evaluar, folds, grupos_de, vecinos_fold  # noqa: E402

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "data" / "processed"
SUB = ROOT / "submissions"
EQUIPO = "CebadaVision"
REPS = 10
Z80 = 1.2816
RANGO = (1.5, 6.5)  # t/ha plausibles para cebada de temporal en el Altiplano
VERSION = "1.0.0"

# variables que ve el productor en la app (con etiqueta y texto llano); el simulador lineal se
# ajusta sobre ellas. Deben existir para las 197 parcelas.
VARIABLES_APP = [
    ("vecinos_knn", "Cosecha de parcelas vecinas", "t/ha", "otra",
     "Promedio del rendimiento reportado en las 8 parcelas más cercanas. Es la referencia más "
     "fuerte: parcelas vecinas comparten suelo, clima y manejo."),
    ("elev_mean", "Elevación", "m", "geofisica", "Altura de la parcela sobre el nivel del mar."),
    ("pend_mean", "Pendiente", "°", "geofisica", "Qué tan inclinado es el terreno."),
    ("prec_abr_oct", "Lluvia abril-octubre", "mm", "clima",
     "Lluvia total durante el ciclo (todas las parcelas son de temporal)."),
    ("prec_anomalia", "Lluvia vs. años anteriores", "mm", "clima",
     "Cuánta lluvia más (o menos) cayó en 2025 que el promedio de 2022 a 2024."),
    ("tmin_media_abr_oct", "Temperatura mínima media", "°C", "clima",
     "Promedio de las temperaturas más bajas del día durante el ciclo."),
    ("tmax_media_abr_oct", "Temperatura máxima media", "°C", "clima",
     "Promedio de las temperaturas más altas del día durante el ciclo."),
    ("planet_evi_may_jun", "Vigor en mayo-junio (EVI)", "", "indice",
     "Qué tan verde se veía la parcela desde el satélite al inicio del ciclo (emergencia)."),
    ("planet_evi_pico", "Vigor máximo (EVI)", "", "indice",
     "El verdor más alto del ciclo, normalmente en agosto-septiembre."),
    ("planet_lai_auc_abr_oct", "Hoja acumulada en el ciclo (LAI)", "", "indice",
     "Cuánta hoja mantuvo el cultivo a lo largo de todo el ciclo (área bajo la curva)."),
    ("planet_evi_duracion", "Duración de la temporada verde", "días", "indice",
     "Días entre que el cultivo emergió y que empezó a secarse."),
]
COLS_APP = [v[0] for v in VARIABLES_APP]


def preparar():
    df = pd.read_csv(PROC / "features_parcela.csv")
    tr = df[df["CONJUNTO"] == "ENTRENAMIENTO"].reset_index(drop=True)
    te = df[df["CONJUNTO"] == "PREDICCION"].reset_index(drop=True)
    (tr["vecinos_knn"], tr["media_zona"]), (te["vecinos_knn"], te["media_zona"]) = vecinos_fold(tr, te)
    G = grupos_de(df.columns)
    loc = G["vecinos"] + G["xy"]
    m1 = loc + G["relieve"] + G["clima"]
    m2 = loc + G["planet_feno"] + G["clima"] + G["relieve"]
    return tr, te, G, {"lgbm": m1, "rf": m2}


def metricas(y, p):
    e = y - p
    return {"rmse": float(np.sqrt(np.mean(e ** 2))), "mae": float(np.mean(np.abs(e))),
            "r2": float(1 - np.sum(e ** 2) / np.sum((y - y.mean()) ** 2))}


def cv_ensamble(tr, cols):
    """Predicciones fuera de fold del ensamble (n_rep x n) con los mismos folds para los dos
    modelos."""
    reps = folds(tr, "estratificada", REPS)
    muni = folds(tr, "municipio", 1)
    oof = {k: evaluar(tr, c, MODELOS[k], reps, True)[1] for k, c in cols.items()}
    oof_m = {k: evaluar(tr, c, MODELOS[k], muni, True)[1] for k, c in cols.items()}
    ens = np.clip(np.mean(list(oof.values()), axis=0), *RANGO)
    ens_m = np.clip(np.mean(list(oof_m.values()), axis=0), *RANGO)[0]
    return oof, ens, ens_m


def ablacion(tr, G, loc):
    """Pregunta guia 3: RMSE del ensamble (misma receta) quitando/poniendo grupos. 3 reps."""
    reps = folds(tr, "estratificada", 3)
    y = tr[R].to_numpy()
    casos = {
        "Solo ubicación": (loc, loc),
        "Solo índices (Planet)": (G["planet_feno"], G["planet_feno"]),
        "Solo clima": (G["clima"], G["clima"]),
        "Solo relieve": (G["relieve"], G["relieve"]),
        "Índices + clima + relieve (sin ubicación)": (G["clima"] + G["relieve"],
                                                     G["planet_feno"] + G["clima"] + G["relieve"]),
        "Ubicación + índices": (loc, loc + G["planet_feno"]),
        "Ubicación + clima": (loc + G["clima"], loc + G["clima"]),
        "Ubicación + relieve": (loc + G["relieve"], loc + G["relieve"]),
        "Ubicación + clima + relieve": (loc + G["clima"] + G["relieve"], loc + G["clima"] + G["relieve"]),
        "Ubicación + índices + clima + relieve (final)": (loc + G["relieve"] + G["clima"],
                                                         loc + G["planet_feno"] + G["clima"] + G["relieve"]),
    }
    out = []
    for nombre, (c1, c2) in casos.items():
        usa_v = "vecinos_knn" in c1 or "vecinos_knn" in c2
        o1 = evaluar(tr, c1, MODELOS["lgbm"], reps, usa_v)[1]
        o2 = evaluar(tr, c2, MODELOS["rf"], reps, usa_v)[1]
        p = np.clip((o1 + o2) / 2, *RANGO)
        e = y[None, :] - p
        rm = np.sqrt((e ** 2).mean(1)).mean()
        r2 = (1 - (e ** 2).sum(1) / ((y - y.mean()) ** 2).sum()).mean()
        vars_ = sorted(set(c1) | set(c2))
        out.append({"nombre": nombre, "variables": vars_, "rmse": round(float(rm), 4),
                    "r2": round(float(r2), 4)})
        print(f"  {nombre:48s} RMSE {rm:.3f}  R2 {r2:.3f}")
    return out


def importancia_permutacion(modelos, cols, tr, reps=5):
    """Importancia por permutacion del ensamble sobre las 138 (aumento de RMSE al barajar cada
    variable), agrupada por variable y por grupo."""
    rng = np.random.default_rng(0)
    y = tr[R].to_numpy()
    base = np.sqrt(np.mean((y - predecir(modelos, cols, tr)) ** 2))
    todas = sorted(set(cols["lgbm"]) | set(cols["rf"]))
    imp = {}
    for v in todas:
        d = []
        for _ in range(reps):
            x = tr.copy()
            x[v] = rng.permutation(x[v].to_numpy())
            d.append(np.sqrt(np.mean((y - predecir(modelos, cols, x)) ** 2)) - base)
        imp[v] = max(0.0, float(np.mean(d)))
    return imp


def predecir(modelos, cols, X):
    p = np.mean([modelos[k].predict(X[c]) for k, c in cols.items()], axis=0)
    return np.clip(p, *RANGO)


def shap_por_parcela(modelos, cols, df):
    """Contribucion SHAP (t/ha) de cada variable al ensamble, promedio de los dos modelos."""
    contrib = pd.DataFrame(0.0, index=df.index, columns=sorted(set(cols["lgbm"]) | set(cols["rf"])))
    base = 0.0
    for k, c in cols.items():
        pipe = modelos[k]
        X = pipe[:-1].transform(df[c])
        ex = shap.TreeExplainer(pipe[-1])
        sv = ex.shap_values(X)
        contrib[c] += pd.DataFrame(sv, index=df.index, columns=c) / len(cols)
        base += float(np.ravel(ex.expected_value)[0]) / len(cols)
    return base, contrib


ETIQUETA = {v[0]: v[1] for v in VARIABLES_APP}
ETIQUETA.update({"media_zona": "Promedio de su zona", "x_km": "Posición este-oeste",
                 "y_km": "Posición norte-sur", "elev_std": "Variación de elevación"})


def etiqueta(v):
    if v in ETIQUETA:
        return ETIQUETA[v]
    if v.startswith("planet_"):
        idx = v.split("_")[1].upper()
        resto = "_".join(v.split("_")[2:])
        nombres = {"may_jun": "mayo-junio", "jul_sep": "julio-septiembre", "oct_nov": "octubre-noviembre",
                   "pico": "máximo", "doy_pico": "fecha del máximo", "amplitud": "amplitud",
                   "auc_abr_oct": "acumulado del ciclo", "doy_inicio": "fecha de emergencia",
                   "doy_fin": "fecha de secado", "duracion": "duración verde",
                   "pend_subida": "velocidad de crecimiento", "pend_bajada": "velocidad de secado"}
        if resto.startswith("m") and resto[1:].isdigit():
            return f"{idx} en {['', 'ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic'][int(resto[1:])]}"
        return f"{idx}: {nombres.get(resto, resto)}"
    return v


def nota_llana(fila, contrib, base, pred):
    """Explicacion en lenguaje sencillo de como se llego al numero de una parcela."""
    c = contrib.loc[fila.name].sort_values()
    # agrupar por bloque para que la nota hable de 4 cosas, no de 90
    grupo = {}
    for v, val in c.items():
        g = ("vecinos" if v in ("vecinos_knn", "media_zona", "x_km", "y_km") else
             "clima" if v in ("prec_abr_oct", "prec_anomalia", "tmin_media_abr_oct", "tmax_media_abr_oct") else
             "relieve" if v.startswith(("elev", "pend")) else "satelite")
        grupo[g] = grupo.get(g, 0.0) + val
    frases = {
        "vecinos": ("las parcelas vecinas cosecharon más que el promedio regional",
                    "las parcelas vecinas cosecharon menos que el promedio regional"),
        "clima": ("el clima del ciclo (lluvia y temperatura) fue favorable",
                  "el clima del ciclo (lluvia y temperatura) fue poco favorable"),
        "relieve": ("la altura y la pendiente del terreno ayudan", "la altura y la pendiente del terreno restan"),
        "satelite": ("el satélite vio un cultivo vigoroso y de ciclo largo",
                     "el satélite vio un cultivo con menos vigor o ciclo más corto"),
    }
    partes = []
    for g, val in sorted(grupo.items(), key=lambda t: -abs(t[1])):
        if abs(val) < 0.05:
            continue
        signo = f"+{val:.2f}" if val > 0 else f"{val:.2f}"
        partes.append(f"{frases[g][0 if val > 0 else 1]} ({signo} t/ha)")
    txt = (f"Estimación: {pred:.2f} t/ha. Se parte del promedio regional ({base:.2f} t/ha). "
           + ("Luego: " + "; ".join(partes) + "." if partes else "Esta parcela se comporta como el promedio."))
    return txt


def main():
    tr, te, G, cols = preparar()
    loc = G["vecinos"] + G["xy"]
    y = tr[R].to_numpy()

    print("1. Validación cruzada del ensamble (5 folds x 10 rep + agrupada por municipio)")
    oof, ens, ens_m = cv_ensamble(tr, cols)
    por_rep = [metricas(y, ens[r]) for r in range(REPS)]
    m_cv = {k: float(np.mean([m[k] for m in por_rep])) for k in ("rmse", "mae", "r2")}
    m_cv["rmse_sd"] = float(np.std([m["rmse"] for m in por_rep]))
    m_muni = metricas(y, ens_m)
    oof_prom = ens.mean(0)
    print(f"   ensamble  RMSE {m_cv['rmse']:.3f}±{m_cv['rmse_sd']:.3f}  MAE {m_cv['mae']:.3f}  "
          f"R2 {m_cv['r2']:.3f}   | municipio: RMSE {m_muni['rmse']:.3f} R2 {m_muni['r2']:.3f}")
    for k in oof:
        mk = [metricas(y, np.clip(oof[k][r], *RANGO)) for r in range(REPS)]
        print(f"   {k:5s}     RMSE {np.mean([m['rmse'] for m in mk]):.3f}  R2 {np.mean([m['r2'] for m in mk]):.3f}")
    por_estado = []
    for est, g in tr.assign(oof=oof_prom).groupby("Estado"):
        por_estado.append({"estado": est, "n": int(len(g)), **{k: round(v, 4) for k, v in metricas(g[R], g["oof"]).items()}})
        print(f"   {est:9s} n={len(g):3d} RMSE {por_estado[-1]['rmse']:.3f} R2 {por_estado[-1]['r2']:.3f}")

    print("\n2. Ajuste final con las 138 y predicción de las 197")
    modelos = {k: MODELOS[k]().fit(tr[c], tr[R]) for k, c in cols.items()}
    todo = pd.concat([tr, te], ignore_index=True)
    pred = predecir(modelos, cols, todo)
    margen = Z80 * m_cv["rmse"]
    todo["rendimiento_pred"] = pred.round(4)
    todo["pred_lo"] = np.clip(pred - margen, RANGO[0], None).round(4)
    todo["pred_hi"] = (pred + margen).round(4)
    todo["prediccion_cv"] = np.concatenate([oof_prom.round(4), np.full(len(te), np.nan)])
    print(f"   predicción 59: media {pred[len(tr):].mean():.3f}, rango {pred[len(tr):].min():.2f}-{pred[len(tr):].max():.2f}")
    print(f"   entrenamiento 138: media real {y.mean():.3f}, media predicha {pred[:len(tr)].mean():.3f}")

    print("\n3. Importancia por permutación del ensamble")
    imp = importancia_permutacion(modelos, cols, tr)
    top = sorted(imp.items(), key=lambda t: -t[1])[:15]
    for v, val in top:
        print(f"   {etiqueta(v):40s} +{val:.3f} RMSE")
    imp_grupo = {}
    for v, val in imp.items():
        g = ("ubicacion" if v in loc else "clima" if v in G["clima"] else
             "relieve" if v in G["relieve"] else "indice_" + v.split("_")[1])
        imp_grupo[g] = imp_grupo.get(g, 0.0) + val
    print("   por grupo:", {k: round(v, 3) for k, v in sorted(imp_grupo.items(), key=lambda t: -t[1])})

    print("\n4. Ablación por grupos (pregunta guía 3)")
    combinaciones = ablacion(tr, G, loc)

    print("\n5. SHAP por parcela y notas en lenguaje llano")
    base, contrib = shap_por_parcela(modelos, cols, todo)
    todo["nota"] = [nota_llana(todo.loc[i], contrib, base, todo.loc[i, "rendimiento_pred"]) for i in todo.index]
    print("   ejemplo:", todo.loc[len(tr), "ID_POLIGONO"], "->", todo.loc[len(tr), "nota"])
    # top-4 factores por parcela (etiqueta + aporte) para la ficha de la app
    factores = []
    for i in todo.index:
        c = contrib.loc[i]
        c = c[c.abs() > 0.02].sort_values(key=np.abs, ascending=False).head(5)
        factores.append([{"variable": v, "etiqueta": etiqueta(v), "aporte": round(float(a), 3)} for v, a in c.items()])

    print("\n6. Simulador lineal sustituto (para que la app ejecute el modelo en el navegador)")
    # la fenologia puede no detectar fin de temporada en algunas parcelas: para la ficha y el
    # simulador se rellena con la mediana (el ensamble ya imputa internamente)
    todo[COLS_APP] = todo[COLS_APP].fillna(todo[COLS_APP].median())
    sc = StandardScaler().fit(todo[COLS_APP])
    sur = Ridge(alpha=1.0).fit(sc.transform(todo[COLS_APP]), pred)
    rmse_sur = float(np.sqrt(np.mean((sur.predict(sc.transform(todo[COLS_APP])) - pred) ** 2)))
    print(f"   RMSE sustituto vs ensamble: {rmse_sur:.3f} t/ha")

    terciles = tr[R].quantile([1 / 3, 2 / 3]).round(1)
    resumen = {
        "nombre": "CebadaVision · ensamble LightGBM + Random Forest",
        "version": VERSION,
        "generado": date.today().isoformat(),
        "es_mock": False,
        "descripcion": ("Promedio de dos modelos de árboles: LightGBM con ubicación (rendimiento de "
                        "parcelas vecinas, zona, coordenadas), relieve y clima; y Random Forest que "
                        "además usa la fenología de los índices de Planet (NDVI, EVI, LAI, MSAVI). "
                        "Validado con 5 folds estratificados por estado, repetidos 10 veces."),
        "intervalo": "Intervalo de predicción al 80 % (± 1.28 · RMSE de validación cruzada)",
        "variables": [{"nombre": n, "etiqueta": e, "unidad": u, "grupo": g, "descripcion": d}
                      for n, e, u, g, d in VARIABLES_APP],
        "metricas": {"rmse": round(m_cv["rmse"], 4), "mae": round(m_cv["mae"], 4), "r2": round(m_cv["r2"], 4),
                     "rmse_sd": round(m_cv["rmse_sd"], 4),
                     "validacion": "CV de 5 folds estratificada por estado, 10 repeticiones (media de vecinos calculada dentro de cada fold)",
                     "por_estado": por_estado,
                     "municipio": {k: round(v, 4) for k, v in m_muni.items()},
                     "referencias": {"media_global": {"rmse": 0.851, "mae": 0.751, "r2": -0.018},
                                     "knn_espacial": {"rmse": 0.506, "r2": 0.644},
                                     "ridge_provisional": {"rmse": 0.551, "r2": 0.578}}},
        # la app muestra importancias solo de sus variables; el reporte usa la lista completa
        "importancias": [{"variable": v, "importancia": round(imp.get(v, 0.0), 4)} for v in COLS_APP],
        "importancias_todas": [{"variable": v, "etiqueta": etiqueta(v), "importancia": round(val, 4)}
                               for v, val in sorted(imp.items(), key=lambda t: -t[1])],
        "importancias_grupo": {k: round(v, 4) for k, v in sorted(imp_grupo.items(), key=lambda t: -t[1])},
        "combinaciones": combinaciones,
        "simulador": {
            "tipo": "lineal",
            "descripcion": (f"Regresión ridge sustituta ajustada a las predicciones del ensamble sobre "
                            f"{len(COLS_APP)} variables interpretables; el mapa y la ficha usan el "
                            "ensamble exacto."),
            "rmse": round(rmse_sur, 4),
            "intercepto": round(float(sur.intercept_), 6),
            "variables": [{"nombre": c, "coef": round(float(b), 6), "media": round(float(mu), 6),
                           "std": round(float(s), 6), "min": round(float(todo[c].min()), 4),
                           "max": round(float(todo[c].max()), 4)}
                          for c, b, mu, s in zip(COLS_APP, sur.coef_, sc.mean_, sc.scale_)],
        },
        "umbrales": {"bajo": float(terciles.iloc[0]), "alto": float(terciles.iloc[1])},
        "shap_base": round(base, 4),
        "preguntas_guia": preguntas_guia(imp_grupo, combinaciones),
    }
    (PROC / "modelo_final.json").write_text(json.dumps(resumen, ensure_ascii=False, indent=2), encoding="utf-8")

    cols_out = ["ID_POLIGONO", "CONJUNTO", "Estado", "Municipio", "AREA_HA", R, "rendimiento_pred",
                "pred_lo", "pred_hi", "prediccion_cv", "nota"] + COLS_APP
    salida = todo[cols_out].copy()
    salida["factores"] = [json.dumps(f, ensure_ascii=False) for f in factores]
    salida.to_csv(PROC / "predicciones_197.csv", index=False)

    SUB.mkdir(exist_ok=True)
    fira = (todo.loc[todo["CONJUNTO"] == "PREDICCION", ["ID_POLIGONO", "rendimiento_pred"]]
            .sort_values("ID_POLIGONO").rename(columns={"rendimiento_pred": "RENDIMIENTO_T_HA"}))
    fira.insert(0, "EQUIPO", EQUIPO)
    assert len(fira) == 59 and fira["ID_POLIGONO"].is_unique
    fira.to_csv(SUB / f"predicciones_59_{EQUIPO}.csv", index=False, float_format="%.4f")
    print(f"\nGuardado: data/processed/predicciones_197.csv, modelo_final.json, "
          f"submissions/predicciones_59_{EQUIPO}.csv")


def preguntas_guia(imp_grupo, combinaciones):
    idx = {k: v for k, v in imp_grupo.items() if k.startswith("indice_")}
    mejor_idx = max(idx, key=idx.get).replace("indice_", "").upper() if idx else "EVI"
    rm = {c["nombre"]: c["rmse"] for c in combinaciones}
    orden_idx = ", ".join(f"{k.replace('indice_', '').upper()} {v:.3f}"
                          for k, v in sorted(idx.items(), key=lambda t: -t[1]))
    # cifras del banco de experimentos (10 repeticiones), si ya se corrio src/modelar.py
    solo_idx, solo_clima = "", ""
    try:
        ex = pd.read_csv(ROOT / "reports" / "experimentos.csv")
        e = ex[(ex.bloque == "E_indice") & ex.experimento.str.contains("planet") & ex.experimento.str.endswith("solo")]
        solo_idx = ", ".join(f"{r.experimento.split(':')[1].split()[0].upper()} {r.rmse:.3f}"
                             for r in e.sort_values("rmse").itertuples())
        f = ex[(ex.bloque == "F_clima") & ex.experimento.str.endswith("solo")]
        nombres = {"prec_anomalia": "anomalía de lluvia", "prec_abr_oct": "lluvia acumulada",
                   "tmin_media_abr_oct": "temperatura mínima", "tmax_media_abr_oct": "temperatura máxima"}
        solo_clima = ", ".join(f"{nombres[r.experimento.split()[1]]} {r.rmse:.3f}"
                               for r in f.sort_values("rmse").itertuples())
    except Exception:  # noqa: BLE001
        pass
    return {
        "indice": {
            "respuesta": f"{mejor_idx} (Planet)",
            "detalle": (f"Importancia por permutación del ensamble agregada por índice (aumento de RMSE en "
                        f"t/ha): {orden_idx}. Con los mismos folds, cada índice solo (RMSE): {solo_idx}. La señal "
                        "útil está en mayo-junio (emergencia) y en la velocidad de secado, no en el máximo del "
                        "ciclo, que satura en agosto-septiembre.")},
        "clima": {
            "respuesta": "Precipitación del ciclo (acumulada abril-octubre y su anomalía respecto a 2022-2024)",
            "detalle": (f"Cada variable climática sola, con los mismos folds (RMSE): {solo_clima}. Una vez "
                        "controlada la ubicación ninguna agrega más de 0.01 t/ha, porque el clima viene en 25 "
                        "píxeles de 5 km y actúa en gran parte como proxy de la zona; dentro del modelo final la "
                        "temperatura mínima es la que más mueve la predicción (permutación).")},
        "combinacion": {
            "respuesta": "Ubicación (vecinos, zona, coordenadas) + relieve + clima + fenología de Planet",
            "detalle": "RMSE por combinación con la misma receta de ensamble: " + "; ".join(
                f"{k} {v:.3f}" for k, v in sorted(rm.items(), key=lambda t: t[1])) + "."},
    }


if __name__ == "__main__":
    main()
