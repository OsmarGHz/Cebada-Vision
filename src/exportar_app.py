"""Exporta los datos que lee la app (agrocebada-pagina) con un modelo Ridge PROVISIONAL.

Formato: docs/CONTRATO_DATOS.md del repo de la app. Salidas en la carpeta indicada (por
defecto data/app/):
  parcelas.geojson   197 parcelas: geometria, estado, prediccion, intervalo, variables
  modelo.json        metricas de CV, importancias, combinaciones de grupos, simulador, umbrales
  series.json        NDVI / EVI / MSAVI de PRO (Planet) por fecha, abril-octubre 2025
  predicciones.csv   59 parcelas de PREDICCION (ID_POLIGONO, rendimiento_pred, 4 decimales)

El modelo es Ridge sobre variables estandarizadas, asi que el simulador de la app es el modelo
exacto (no un sustituto). Cuando exista el modelo final, cambiar VARIABLES y ajustar() aqui;
la app no necesita cambios.

Validacion: 5 folds estratificados por Estado, semilla 42 (DECISIONES.md). Si se pasa
particiones_cv.csv (ID_POLIGONO, fold) se usan esos folds.

Entradas: dataset oficial + data/processed/{variables_pro_abr_oct_2025, clima_ciclo_2025,
topografia_parcela}.csv (correr antes los scripts del README).

Uso:  .venv/Scripts/python.exe src/exportar_app.py [carpeta_salida] [--particiones ruta.csv]
Luego copiar los 4 archivos a agrocebada-pagina/public/data/ y correr `npm run validate`.
"""
import argparse
import json
from datetime import date
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import shapely
from sklearn.linear_model import RidgeCV
from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "DATASET_RETO_AGRO_2026"
PROC = ROOT / "data" / "processed"

ALPHAS = np.logspace(-2, 3, 30)
Z80 = 1.2816  # intervalo de prediccion al 80 %: pred +- z * RMSE_cv
FECHA_INI, FECHA_FIN = "2025-04-01", "2025-10-31"

# nombre, etiqueta, unidad, grupo, descripcion para productores
VARIABLES = [
    ("ndvi_max", "NDVI máximo", "", "indice",
     "Qué tan verde y vigoroso estuvo el cultivo en su mejor momento."),
    ("evi_max", "EVI máximo", "", "indice",
     "Vigor del cultivo, menos sensible al suelo desnudo y a la atmósfera."),
    ("lai_max", "LAI máximo", "m²/m²", "indice",
     "Cuánta hoja cubrió el suelo en el mejor momento del ciclo."),
    ("prec_abr_oct", "Lluvia abril-octubre", "mm", "clima",
     "Lluvia total durante el ciclo (todas las parcelas son de temporal)."),
    ("prec_anomalia", "Lluvia vs. años anteriores", "mm",
     "clima", "Cuánta lluvia más (o menos) cayó en 2025 que el promedio de 2022 a 2024."),
    ("tmin_media_abr_oct", "Temperatura mínima media", "°C", "clima",
     "Promedio de las temperaturas más bajas del día durante el ciclo."),
    ("tmax_media_abr_oct", "Temperatura máxima media", "°C", "clima",
     "Promedio de las temperaturas más altas del día durante el ciclo."),
    ("elev_mean", "Elevación", "m", "geofisica", "Altura de la parcela sobre el nivel del mar."),
    ("pend_mean", "Pendiente", "°", "geofisica", "Qué tan inclinado es el terreno."),
]
COLS = [v[0] for v in VARIABLES]
GRUPO = {v[0]: v[3] for v in VARIABLES}
COMBINACIONES = [
    ("Solo índices", ["indice"]),
    ("Solo clima", ["clima"]),
    ("Solo relieve", ["geofisica"]),
    ("Índices + clima", ["indice", "clima"]),
    ("Índices + relieve", ["indice", "geofisica"]),
    ("Clima + relieve", ["clima", "geofisica"]),
    ("Índices + clima + relieve", ["indice", "clima", "geofisica"]),
]


def cargar():
    y = pd.read_csv(D / "ID_area_rendimiento_70_30_Reto_AgroCebada.csv").dropna(axis=1, how="all")
    shp = gpd.read_file(D / "Parcelas_Reto_AGC_CONJUNTO_70_30" / "Parcelas_Reto_AGC_CONJUNTO.shp",
                        encoding="latin1").rename(columns={"ID_POLIGON": "ID_POLIGONO"})
    df = shp[["ID_POLIGONO", "Estado", "Municipio", "geometry"]].merge(y, on="ID_POLIGONO",
                                                                       validate="1:1")
    for f in ["variables_pro_abr_oct_2025", "clima_ciclo_2025", "topografia_parcela"]:
        df = df.merge(pd.read_csv(PROC / f"{f}.csv"), on="ID_POLIGONO", validate="1:1")
    assert len(df) == 197 and not df[COLS].isna().any().any()
    return gpd.GeoDataFrame(df, geometry="geometry", crs=shp.crs)


def folds_cv(tr, ruta_particiones):
    if ruta_particiones:
        part = pd.read_csv(ruta_particiones)[["ID_POLIGONO", "fold"]]
        f = tr[["ID_POLIGONO"]].merge(part, on="ID_POLIGONO", how="left", validate="1:1")["fold"]
        assert f.notna().all(), "hay parcelas de entrenamiento sin fold"
        return f.to_numpy(), "particiones_cv.csv (5 folds, estratificada por estado)"
    f = np.empty(len(tr), dtype=int)
    for k, (_, te) in enumerate(StratifiedKFold(5, shuffle=True, random_state=42)
                                .split(tr, tr["Estado"])):
        f[te] = k
    return f, "CV de 5 folds estratificada por estado (semilla 42)"


def ajustar(X, y):
    return make_pipeline(StandardScaler(), RidgeCV(alphas=ALPHAS)).fit(X, y)


def predicciones_oof(tr, cols, folds):
    oof = np.empty(len(tr))
    for k in np.unique(folds):
        te = folds == k
        oof[te] = ajustar(tr.loc[~te, cols], tr.loc[~te, "RENDIMIENTO_T_HA"]).predict(tr.loc[te, cols])
    return oof


def metricas(y, p):
    e = y - p
    return {"rmse": float(np.sqrt((e ** 2).mean())), "mae": float(e.abs().mean()),
            "r2": float(1 - (e ** 2).sum() / ((y - y.mean()) ** 2).sum())}


def r(x, n=4):
    return None if x is None or pd.isna(x) else round(float(x), n)


def construir(df, ruta_particiones):
    tr = df[df["CONJUNTO"] == "ENTRENAMIENTO"].reset_index(drop=True)
    folds, txt_val = folds_cv(tr, ruta_particiones)

    oof = predicciones_oof(tr, COLS, folds)
    m = metricas(tr["RENDIMIENTO_T_HA"], oof)
    por_estado = []
    for est, g in tr.assign(oof=oof).groupby("Estado"):
        por_estado.append({"estado": est, "n": len(g), **metricas(g["RENDIMIENTO_T_HA"], g["oof"])})

    combinaciones = []
    for nombre, grupos in COMBINACIONES:
        cols = [c for c in COLS if GRUPO[c] in grupos]
        mc = metricas(tr["RENDIMIENTO_T_HA"], predicciones_oof(tr, cols, folds))
        combinaciones.append({"nombre": nombre, "variables": cols,
                              "rmse": r(mc["rmse"]), "r2": r(mc["r2"])})

    final = ajustar(tr[COLS], tr["RENDIMIENTO_T_HA"])
    sc, ridge = final[0], final[-1]
    pred = final.predict(df[COLS])
    media = tr["RENDIMIENTO_T_HA"].mean()
    terciles = tr["RENDIMIENTO_T_HA"].quantile([1 / 3, 2 / 3]).round(1)

    modelo = {
        "nombre": "Ridge (provisional)",
        "version": "0.2.0",
        "generado": date.today().isoformat(),
        "es_mock": False,
        "descripcion": ("Modelo provisional: regresión ridge con índices de Planet, clima y "
                        "relieve. Se reemplazará por el modelo final del equipo."),
        "intervalo": "Intervalo de predicción al 80 % (± 1.28 · RMSE de validación cruzada)",
        "variables": [{"nombre": n, "etiqueta": e, "unidad": u, "grupo": g, "descripcion": d}
                      for n, e, u, g, d in VARIABLES],
        "metricas": {**{k: r(v) for k, v in m.items()}, "validacion": txt_val,
                     "por_estado": [{**e, **{k: r(e[k]) for k in ("rmse", "mae", "r2")}}
                                    for e in por_estado]},
        # coeficientes sobre variables estandarizadas: t/ha por desviacion estandar
        "importancias": [{"variable": c, "importancia": r(abs(b))}
                         for c, b in sorted(zip(COLS, ridge.coef_), key=lambda t: -abs(t[1]))],
        "combinaciones": combinaciones,
        "simulador": {
            "tipo": "lineal",
            "descripcion": (f"Es el modelo ridge completo (alpha = {ridge.alpha_:.2f}), no un "
                            "sustituto: da las mismas predicciones que el mapa."),
            "rmse": 0.0,
            "intercepto": r(ridge.intercept_, 6),
            "variables": [{"nombre": c, "coef": r(b, 6), "media": r(mu, 6), "std": r(s, 6),
                           "min": r(df[c].min()), "max": r(df[c].max())}
                          for c, b, mu, s in zip(COLS, ridge.coef_, sc.mean_, sc.scale_)],
        },
        "umbrales": {"bajo": float(terciles.iloc[0]), "alto": float(terciles.iloc[1])},
    }

    oof_por_id = dict(zip(tr["ID_POLIGONO"], oof))
    margen = Z80 * m["rmse"]
    props = pd.DataFrame({
        "ID_POLIGONO": df["ID_POLIGONO"],
        "estado": df["Estado"],
        "municipio": df["Municipio"],
        "superficie_ha": df["AREA_HA"],
        "conjunto": df["CONJUNTO"].str.lower(),
        "rendimiento_real": df["RENDIMIENTO_T_HA"],
        "rendimiento_pred": pred.round(4),
        "pred_lo": np.clip(pred - margen, 0, None).round(4),
        "pred_hi": (pred + margen).round(4),
        "prediccion_cv": df["ID_POLIGONO"].map(oof_por_id).round(4),
        **{c: df[c].round(4) for c in COLS},
    })
    geo = gpd.GeoDataFrame(props, geometry=shapely.force_2d(df.geometry.values), crs=df.crs)
    print(f"Media de entrenamiento {media:.3f} t/ha; alpha {ridge.alpha_:.3f}")
    return modelo, geo.to_crs(4326)


def construir_series():
    pro = pd.read_csv(D / "Conjunto_datos_PRO_AgroCebada.csv")
    pro["fecha"] = pd.to_datetime(pro["fecha_captura"], format="%d/%m/%Y")
    pro = pro[(pro["fecha"] >= FECHA_INI) & (pro["fecha"] <= FECHA_FIN)]
    largo = pro.melt(id_vars=["ID_POLIGONO", "fecha", "porcentaje_nubosidad"],
                     value_vars=["ndvi_promedio", "evi_promedio", "msavi_promedio"],
                     var_name="indice", value_name="valor").dropna(subset=["valor"])
    largo["indice"] = largo["indice"].str.removesuffix("_promedio").str.upper()
    # la app grafica los indices en el orden en que aparecen: NDVI primero
    largo["indice"] = pd.Categorical(largo["indice"], ["NDVI", "EVI", "MSAVI"], ordered=True)
    largo = largo.sort_values(["ID_POLIGONO", "fecha", "indice"])
    series = {}
    for pid, g in largo.groupby("ID_POLIGONO"):
        # nubosidad vacia o 0 se omite: la app la toma como 0 (criterio de FIRA) y el archivo pesa menos
        series[pid] = [{"fecha": f.strftime("%Y-%m-%d"), "indice": i, "valor": round(float(v), 3),
                        "fuente": "Planet", **({"nubosidad": float(n)} if n > 0 else {})}
                       for f, i, v, n in zip(g["fecha"], g["indice"], g["valor"],
                                             g["porcentaje_nubosidad"].fillna(0))]
    return series


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("salida", nargs="?", default=str(ROOT / "data" / "app"))
    ap.add_argument("--particiones", default=None)
    a = ap.parse_args()
    out = Path(a.salida)
    out.mkdir(parents=True, exist_ok=True)

    modelo, geo = construir(cargar(), a.particiones)
    geo.to_file(out / "parcelas.geojson", driver="GeoJSON", COORDINATE_PRECISION=6)
    (out / "modelo.json").write_text(json.dumps(modelo, ensure_ascii=False, indent=2),
                                     encoding="utf-8")
    (out / "series.json").write_text(json.dumps(construir_series(), separators=(",", ":")),
                                     encoding="utf-8")
    pred = (geo.loc[geo["conjunto"] == "prediccion", ["ID_POLIGONO", "rendimiento_pred"]]
            .sort_values("ID_POLIGONO"))
    assert len(pred) == 59
    pred.to_csv(out / "predicciones.csv", index=False, float_format="%.4f")

    mt = modelo["metricas"]
    print(f"CV: RMSE {mt['rmse']}  MAE {mt['mae']}  R2 {mt['r2']}  ({mt['validacion']})")
    for e in mt["por_estado"]:
        print(f"  {e['estado']:9s} n={e['n']:3d}  RMSE {e['rmse']}  R2 {e['r2']}")
    for c in modelo["combinaciones"]:
        print(f"  {c['nombre']:28s} RMSE {c['rmse']}  R2 {c['r2']}")
    print("Umbrales semaforo:", modelo["umbrales"])
    for f in sorted(out.iterdir()):
        print(f"  {f.name:18s} {f.stat().st_size / 1024:8.0f} KB")


if __name__ == "__main__":
    main()
