"""EDA 2: rendimiento vs. ubicación, topografía, clima y trayectorias de índices (ciclo 2025)."""
from pathlib import Path

import geopandas as gpd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "DATASET_RETO_AGRO_2026"
P = ROOT / "data" / "processed"
FIG = ROOT / "reports" / "figuras"
FIG.mkdir(parents=True, exist_ok=True)
pd.set_option("display.width", 200, "display.max_columns", 40, "display.max_rows", 200)

y = pd.read_csv(D / "ID_area_rendimiento_70_30_Reto_AgroCebada.csv").dropna(axis=1, how="all")
g = gpd.read_file(D / "Parcelas_Reto_AGC_CONJUNTO_70_30" / "Parcelas_Reto_AGC_CONJUNTO.shp")
g = g.rename(columns={"ID_POLIGON": "ID_POLIGONO"})
cen = g.to_crs(6372).geometry.centroid
g["x"], g["y"] = cen.x, cen.y
base = g[["ID_POLIGONO", "Municipio", "Estado", "x", "y"]].merge(y, on="ID_POLIGONO")
tr = base[base["CONJUNTO"] == "ENTRENAMIENTO"].copy()
R = "RENDIMIENTO_T_HA"

# --- Objetivo -------------------------------------------------------------
print("valores únicos de rendimiento:", tr[R].nunique(), "de", len(tr))
print("valores más repetidos:\n", tr[R].value_counts().head(10))
print("\nPor estado:\n", base.groupby(["Estado", "CONJUNTO"]).size().unstack())
print("\nPor municipio:\n", base.groupby(["Municipio", "CONJUNTO"]).size().unstack().fillna(0).astype(int))
print("\nRendimiento por municipio:\n", tr.groupby("Municipio")[R].agg(["count", "mean", "std", "min", "max"]).round(2))

# Autocorrelación espacial: correlación del rendimiento con el de su vecino más cercano
from scipy.spatial import cKDTree

xy = tr[["x", "y"]].to_numpy()
d, j = cKDTree(xy).query(xy, k=2)
tr["dist_vecino_km"] = d[:, 1] / 1000
tr["rend_vecino"] = tr[R].to_numpy()[j[:, 1]]
print("\ndistancia al vecino (train) km:", tr["dist_vecino_km"].describe().round(2).to_dict())
print("corr rendimiento vs vecino más cercano:", tr[[R, "rend_vecino"]].corr().iloc[0, 1].round(3))
pr = base[base["CONJUNTO"] == "PREDICCION"]
dp, _ = cKDTree(xy).query(pr[["x", "y"]].to_numpy(), k=1)
print("distancia de parcelas PREDICCION a la de entrenamiento más cercana km:",
      pd.Series(dp / 1000).describe().round(2).to_dict())

# --- Topografía -----------------------------------------------------------
topo = pd.read_csv(P / "topografia_parcela.csv")
tr = tr.merge(topo, on="ID_POLIGONO")
print("\nSpearman rendimiento vs topografía/área:\n",
      tr[[R, "AREA_HA", "elev_mean", "pend_mean", "x", "y"]].corr(method="spearman")[R].round(3))

# --- Clima ciclo 2025 -------------------------------------------------------
cl = pd.read_csv(P / "clima_mensual_parcela.csv")
c25 = cl[(cl["anio"] == 2025) & cl["mes"].between(4, 10)]
print("\npíxeles climáticos distintos (prec abr-oct 2025):",
      c25.groupby("ID_POLIGONO")["prec"].sum().round(3).nunique())
agg = c25.groupby("ID_POLIGONO").agg(prec_tot=("prec", "sum"), tmin_med=("tmin", "mean"), tmax_med=("tmax", "mean"))
tr = tr.merge(agg, on="ID_POLIGONO")
print("Spearman rendimiento vs clima abr-oct 2025:\n",
      tr[[R, "prec_tot", "tmin_med", "tmax_med"]].corr(method="spearman")[R].round(3))
mensual = c25.merge(tr[["ID_POLIGONO", R]], on="ID_POLIGONO")
print("Spearman mensual prec/tmax vs rendimiento:\n",
      mensual.groupby("mes").apply(lambda t: pd.Series({
          "prec": t[["prec", R]].corr(method="spearman").iloc[0, 1],
          "tmax": t[["tmax", R]].corr(method="spearman").iloc[0, 1],
          "tmin": t[["tmin", R]].corr(method="spearman").iloc[0, 1]}), include_groups=False).round(2))

# --- Trayectorias de índices 2025 -----------------------------------------
s2 = pd.read_csv(D / "Conjunto_datos_BASICO_AgroCebada2026.csv")
s2["fecha"] = pd.to_datetime(s2["fecha_captura"], dayfirst=True)
s2 = s2[(s2["sensor"] == "Sentinel-2") & (s2["fecha"].dt.year == 2025)]
print("\nSentinel-2 2025 nubosidad (valores):", s2["porcentaje_nubosidad"].round(0).value_counts().head(8).to_dict())
print("NDVI no nulo según nubosidad:\n",
      s2.assign(nub=pd.cut(s2["porcentaje_nubosidad"], [-1, 0, 20, 50, 99, 100]))
        .groupby("nub", observed=True)["ndvi_promedio"].agg(["size", lambda v: v.notna().mean()]))

pl = pd.read_csv(D / "Conjunto_datos_PRO_AgroCebada.csv")
pl["fecha"] = pd.to_datetime(pl["fecha_captura"], dayfirst=True)

tr["terc"] = pd.qcut(tr[R], 3, labels=["bajo", "medio", "alto"])
fig, axes = plt.subplots(2, 2, figsize=(14, 9))
for ax, (df, col, titulo) in zip(axes.ravel(), [
        (s2, "ndvi_promedio", "Sentinel-2 NDVI"), (s2, "lai_promedio", "Sentinel-2 LAI"),
        (pl, "ndvi_promedio", "Planet NDVI"), (s2, "ndwi_promedio", "Sentinel-2 NDWI")]):
    t = df[df["porcentaje_nubosidad"] <= 20].merge(tr[["ID_POLIGONO", "terc"]], on="ID_POLIGONO")
    t["sem"] = t["fecha"].dt.to_period("W").dt.start_time
    m = t.groupby(["terc", "sem"], observed=True)[col].median().unstack(0)
    m.plot(ax=ax, marker=".")
    ax.set_title(f"{titulo} (mediana por tercil de rendimiento, nubosidad ≤20%)")
    ax.axvspan(pd.Timestamp("2025-04-01"), pd.Timestamp("2025-10-31"), alpha=.08)
fig.tight_layout()
fig.savefig(FIG / "trayectorias_indices_2025.png", dpi=110)

# Correlación rendimiento vs mediana mensual de cada índice (Sentinel-2, nubosidad ≤20%)
idx = [c for c in s2.columns if c.endswith("_promedio")]
t = s2[s2["porcentaje_nubosidad"] <= 20].copy()
t["mes"] = t["fecha"].dt.month
mm = t.groupby(["ID_POLIGONO", "mes"])[idx].median().reset_index().merge(tr[["ID_POLIGONO", R]], on="ID_POLIGONO")
corr = mm.groupby("mes").apply(lambda q: q[idx].corrwith(q[R], method="spearman"), include_groups=False).T
corr.index = [i.replace("_promedio", "") for i in corr.index]
print("\nSpearman rendimiento vs mediana mensual del índice (Sentinel-2, 2025):\n", corr.round(2))
tp = pl[pl["porcentaje_nubosidad"] <= 20].copy()
tp["mes"] = tp["fecha"].dt.month
pidx = [c for c in pl.columns if c.endswith("_promedio")]
mp = tp.groupby(["ID_POLIGONO", "mes"])[pidx].median().reset_index().merge(tr[["ID_POLIGONO", R]], on="ID_POLIGONO")
cp = mp.groupby("mes").apply(lambda q: q[pidx].corrwith(q[R], method="spearman"), include_groups=False).T
print("\nSpearman rendimiento vs mediana mensual (Planet, 2025):\n", cp.round(2))

# --- Mapa -----------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 8))
ax.scatter(pr["x"], pr["y"], c="lightgray", edgecolor="k", s=30, label="PREDICCION")
sc = ax.scatter(tr["x"], tr["y"], c=tr[R], cmap="viridis", s=40, edgecolor="k", label="ENTRENAMIENTO")
plt.colorbar(sc, label="t/ha")
ax.legend(); ax.set_title("Parcelas y rendimiento 2025"); ax.set_aspect("equal")
fig.savefig(FIG / "mapa_rendimiento.png", dpi=110)

fig, ax = plt.subplots(figsize=(7, 4))
tr[R].hist(bins=30, ax=ax); ax.set_title("Distribución del rendimiento (t/ha), n=138")
fig.savefig(FIG / "hist_rendimiento.png", dpi=110)
