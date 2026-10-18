"""EDA 3: estructura por zonas, redondeo del rendimiento y varianza explicada por ubicación."""
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.model_selection import KFold, cross_val_predict
from sklearn.neighbors import KNeighborsRegressor

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "DATASET_RETO_AGRO_2026"
P = ROOT / "data" / "processed"
pd.set_option("display.width", 200, "display.max_columns", 40)
R = "RENDIMIENTO_T_HA"

y = pd.read_csv(D / "ID_area_rendimiento_70_30_Reto_AgroCebada.csv").dropna(axis=1, how="all")
g = gpd.read_file(D / "Parcelas_Reto_AGC_CONJUNTO_70_30" / "Parcelas_Reto_AGC_CONJUNTO.shp")
g = g.rename(columns={"ID_POLIGON": "ID_POLIGONO"})
cen = g.to_crs(6372).geometry.centroid
g["x"], g["y"] = cen.x, cen.y
df = g[["ID_POLIGONO", "Cultivo", "Municipio", "Estado", "x", "y"]].merge(y, on="ID_POLIGONO")
df["zona"] = KMeans(3, n_init=10, random_state=0).fit_predict(df[["x", "y"]])
tr = df[df["CONJUNTO"] == "ENTRENAMIENTO"].copy()
tr["redondeado"] = (tr[R] * 2).round(6) % 1 == 0  # múltiplo de 0.5

print("Zonas (k-means sobre centroides):")
print(df.groupby(["zona", "CONJUNTO"]).size().unstack())
print(tr.groupby("zona").agg(n=(R, "size"), media=(R, "mean"), std=(R, "std"),
                             pct_redondeado=("redondeado", "mean"),
                             municipios=("Municipio", lambda s: ", ".join(sorted(s.unique())))).round(2))
print("\nCultivo (capitalización) vs zona:\n", pd.crosstab(df["zona"], df["Cultivo"]))
print("\n% redondeado por municipio:\n", tr.groupby("Municipio")["redondeado"].agg(["mean", "size"]).round(2))

# Varianza explicada solo por ubicación (CV aleatoria, 10 repeticiones)
def cv_rmse(pred_fn, reps=10):
    out = []
    for r in range(reps):
        pred = np.zeros(len(tr))
        for a, b in KFold(5, shuffle=True, random_state=r).split(tr):
            pred[b] = pred_fn(tr.iloc[a], tr.iloc[b])
        out.append([np.sqrt(np.mean((tr[R] - pred) ** 2)), 1 - np.sum((tr[R] - pred) ** 2) / np.sum((tr[R] - tr[R].mean()) ** 2)])
    return np.round(np.mean(out, axis=0), 3)

print("\nBaselines CV 5-fold x10  [RMSE, R2]:")
print("media global     ", cv_rmse(lambda a, b: np.full(len(b), a[R].mean())))
print("media por zona   ", cv_rmse(lambda a, b: b["zona"].map(a.groupby("zona")[R].mean()).fillna(a[R].mean()).to_numpy()))
print("media municipio  ", cv_rmse(lambda a, b: b["Municipio"].map(a.groupby("Municipio")[R].mean()).fillna(a[R].mean()).to_numpy()))
for k in [3, 5, 8]:
    print(f"kNN espacial k={k}", cv_rmse(lambda a, b, k=k: KNeighborsRegressor(k, weights="distance")
                                         .fit(a[["x", "y"]], a[R]).predict(b[["x", "y"]])))
