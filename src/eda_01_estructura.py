"""EDA 1: estructura de tablas, faltantes, cobertura temporal y objetivo."""
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "DATASET_RETO_AGRO_2026"
pd.set_option("display.width", 200, "display.max_columns", 40, "display.max_rows", 200)

# --- Objetivo -------------------------------------------------------------
y = pd.read_csv(D / "ID_area_rendimiento_70_30_Reto_AgroCebada.csv").dropna(axis=1, how="all")
print("== ID/area/rendimiento", y.shape)
print(y["CONJUNTO"].value_counts())
print(y.groupby("CONJUNTO")["AREA_HA"].describe())
print(y["RENDIMIENTO_T_HA"].describe())
print("cuantiles:", y["RENDIMIENTO_T_HA"].quantile([0, .05, .25, .5, .75, .95, 1]).round(2).tolist())
print("corr area-rend:", y[["AREA_HA", "RENDIMIENTO_T_HA"]].corr(method="spearman").iloc[0, 1].round(3))

# --- Parcelas -------------------------------------------------------------
g = gpd.read_file(D / "Parcelas_Reto_AGC_CONJUNTO_70_30" / "Parcelas_Reto_AGC_CONJUNTO.shp")
print("\n== Shapefile", g.shape, g.crs)
print(g.head())
print(g.geom_type.value_counts())
c = g.to_crs(4326).geometry.centroid
print("lon", c.x.min().round(3), c.x.max().round(3), "lat", c.y.min().round(3), c.y.max().round(3))

# --- Satélite -------------------------------------------------------------
for name in ["Conjunto_datos_BASICO_AgroCebada2026.csv", "Conjunto_datos_PRO_AgroCebada.csv"]:
    s = pd.read_csv(D / name)
    s["fecha"] = pd.to_datetime(s["fecha_captura"], dayfirst=True)
    print(f"\n== {name}", s.shape)
    print("parcelas:", s["ID_POLIGONO"].nunique(), "| fechas:", s["fecha"].min().date(), "->", s["fecha"].max().date())
    print(s.groupby("sensor").agg(n=("fecha", "size"), fechas=("fecha", "nunique"),
                                  parcelas=("ID_POLIGONO", "nunique")))
    print("nubosidad:", s["porcentaje_nubosidad"].describe().round(2).to_dict())
    dup = s.duplicated(["ID_POLIGONO", "fecha", "sensor"]).sum()
    print("duplicados parcela-fecha-sensor:", dup)
    idx = [col for col in s.columns if col.endswith("_promedio")]
    cov = s.groupby("sensor")[idx].apply(lambda t: t.notna().mean().round(2)).T
    print("fracción no nula por índice y sensor:\n", cov)
    s25 = s[(s["fecha"] >= "2025-03-01") & (s["fecha"] <= "2025-11-30")]
    per = s25.groupby(["sensor", "ID_POLIGONO"])["fecha"].nunique().groupby("sensor").describe()
    print("obs por parcela mar-nov 2025:\n", per)
    print("obs por mes 2025:\n", s[s["fecha"].dt.year == 2025].groupby([s["fecha"].dt.month, "sensor"]).size().unstack())
