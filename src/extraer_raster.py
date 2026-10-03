"""Extrae clima mensual (CHIRPS / CHIRTS-ERA5) y topografía (INEGI CEM) por parcela.

Salidas:
  data/processed/clima_mensual_parcela.csv  (ID_POLIGONO, anio, mes, prec, tmin, tmax)
  data/processed/topografia_parcela.csv     (ID_POLIGONO, elev_*, pend_*)
"""
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
from rasterstats import zonal_stats

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "DATASET_RETO_AGRO_2026"
OUT = ROOT / "data" / "processed"
OUT.mkdir(parents=True, exist_ok=True)

PREC_DIR = next(D.glob("Reto_AgroCebada_CHIRPS*/**/Precipitacion_mensual"))
TEMP_DIR = next(D.glob("Reto_AgroCebada_Temperatura*/Reto_AgroCebada_Temperatura_2022_2025"))
TOPO_DIR = next(D.glob("Reto_AgroCebada_Topografia*/**/Elevacion_INEGI_CEM4_120m.tif")).parent

parcelas = gpd.read_file(D / "Parcelas_Reto_AGC_CONJUNTO_70_30" / "Parcelas_Reto_AGC_CONJUNTO.shp")
parcelas = parcelas.rename(columns={"ID_POLIGON": "ID_POLIGONO"})  # dbf trunca a 10 caracteres
ids = parcelas["ID_POLIGONO"].to_numpy()


def muestreo_puntual(tif: Path, pts: gpd.GeoSeries) -> np.ndarray:
    """Valor del píxel en el centroide (rásters de ~5 km: una parcela cae en 1-2 píxeles)."""
    with rasterio.open(tif) as src:
        p = pts.to_crs(src.crs)
        vals = np.array([v[0] for v in src.sample(zip(p.x, p.y))], dtype=float)
        vals[vals == src.nodata] = np.nan
    return vals


def clima() -> pd.DataFrame:
    centroides = parcelas.to_crs(6372).geometry.centroid
    filas = []
    for anio in range(2022, 2026):
        for mes in range(1, 13):
            rec = {"prec": PREC_DIR / f"{anio}" / f"PREC_{anio}_{mes:02d}.tif",
                   "tmin": TEMP_DIR / "Tmin" / f"{anio}" / f"Tmin_{anio}_{mes:02d}.tif",
                   "tmax": TEMP_DIR / "Tmax" / f"{anio}" / f"Tmax_{anio}_{mes:02d}.tif"}
            df = pd.DataFrame({"ID_POLIGONO": ids, "anio": anio, "mes": mes})
            for var, tif in rec.items():
                df[var] = muestreo_puntual(tif, centroides)
            filas.append(df)
    return pd.concat(filas, ignore_index=True)


def topografia() -> pd.DataFrame:
    res = pd.DataFrame({"ID_POLIGONO": ids})
    for var, fname in [("elev", "Elevacion_INEGI_CEM4_120m.tif"),
                       ("pend", "Pendiente_INEGI_CEM4_120m_grados.tif")]:
        tif = TOPO_DIR / fname
        with rasterio.open(tif) as src:
            geoms = parcelas.to_crs(src.crs).geometry
            nodata = src.nodata
        zs = zonal_stats(geoms, str(tif), stats=["mean", "min", "max", "std"],
                         nodata=nodata, all_touched=True)
        for st in ["mean", "min", "max", "std"]:
            res[f"{var}_{st}"] = [z[st] for z in zs]
    return res


if __name__ == "__main__":
    c = clima()
    c.to_csv(OUT / "clima_mensual_parcela.csv", index=False)
    print("clima:", c.shape, "| NaN:", c[["prec", "tmin", "tmax"]].isna().sum().to_dict())
    t = topografia()
    t.to_csv(OUT / "topografia_parcela.csv", index=False)
    print("topografia:", t.shape, "| NaN:", t.isna().sum().sum())
    print(t.describe().round(1).T)
