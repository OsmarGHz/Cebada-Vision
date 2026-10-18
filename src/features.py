"""Tabla de variables por parcela para el modelo (197 filas, llave ID_POLIGONO).

Junta en una sola tabla:
  ubicacion   centroide (km, EPSG:6372), zona (k-means de 3 sobre centroides), estado, municipio, area
  planet_*    fenologia de Planet (PRO) abril-noviembre 2025: medianas mensuales, ventanas, pico,
              inicio/fin de temporada verde, integral (AUC) y pendientes de crecimiento/senescencia
  s2_*        lo mismo con Sentinel-2 (BASICO), para los indices con mas cobertura
  clima       prec_abr_oct, tmax/tmin medias, prec_anomalia (data/processed/clima_ciclo_2025.csv)
  relieve     elev_mean, pend_mean (data/processed/topografia_parcela.csv)

Reglas: capturas con nubosidad 100 se descartan (sus indices vienen vacios); no se imputa fila a
fila. Lo que no se puede calcular queda NaN y lo imputa el modelo (mediana de entrenamiento).

Salida: data/processed/features_parcela.csv
Uso:    .venv/Scripts/python.exe src/features.py
"""
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "DATASET_RETO_AGRO_2026"
PROC = ROOT / "data" / "processed"
OUT = PROC / "features_parcela.csv"

ANIO = 2025
MESES = list(range(4, 12))  # abril-noviembre: el ciclo es abr-oct, noviembre captura senescencia
VENTANAS = {"may_jun": (5, 6), "jul_sep": (7, 9), "oct_nov": (10, 11)}
IDX_PLANET = ["ndvi", "evi", "lai", "msavi"]
IDX_S2 = ["ndvi", "evi", "savi", "lai", "fapar", "ndwi", "msi", "ndti"]


def leer_serie(archivo, sensor, indices):
    """Serie larga (ID, fecha, doy, indice, valor) de un sensor, sin nubes ni vacios."""
    df = pd.read_csv(D / archivo)
    df = df[df["sensor"] == sensor]
    df["fecha"] = pd.to_datetime(df["fecha_captura"], format="%d/%m/%Y")
    df = df[(df["fecha"].dt.year == ANIO) & (df["porcentaje_nubosidad"].fillna(0) < 100)]
    cols = {f"{i}_promedio": i for i in indices}
    df = df[["ID_POLIGONO", "fecha"] + list(cols)].rename(columns=cols)
    largo = df.melt(id_vars=["ID_POLIGONO", "fecha"], var_name="indice", value_name="valor")
    largo = largo.dropna(subset=["valor"])
    largo["mes"] = largo["fecha"].dt.month
    largo["doy"] = largo["fecha"].dt.dayofyear
    return largo


def fenologia(g):
    """Metricas de una serie (un indice, una parcela) ordenada por fecha."""
    g = g.sort_values("doy")
    # mediana movil de 3 para quitar picos aislados (nubes no detectadas, sombras)
    v = g["valor"].rolling(3, center=True, min_periods=1).median().to_numpy()
    d = g["doy"].to_numpy(dtype=float)
    out = {}
    temporada = (d >= 91) & (d <= 334)  # 1 abr - 30 nov
    if temporada.sum() < 5:
        return out
    v, d = v[temporada], d[temporada]
    i_max = int(np.argmax(v))
    base = np.nanmin(v[: max(i_max, 1)]) if i_max > 0 else v[0]
    amp = v[i_max] - base
    out["pico"] = v[i_max]
    out["doy_pico"] = d[i_max]
    out["amplitud"] = amp
    out["auc_abr_oct"] = np.trapezoid(v[d <= 304], d[d <= 304]) if (d <= 304).sum() >= 2 else np.nan
    if amp > 0.05:
        umbral = base + 0.5 * amp
        sube = np.where(v[: i_max + 1] >= umbral)[0]
        baja = np.where(v[i_max:] <= umbral)[0]
        sos = d[sube[0]] if len(sube) else np.nan
        eos = d[i_max + baja[0]] if len(baja) else np.nan
        out["doy_inicio"] = sos
        out["doy_fin"] = eos
        out["duracion"] = eos - sos if np.isfinite(sos) and np.isfinite(eos) else np.nan
        # pendientes: t/dia de subida (inicio->pico) y de bajada (pico->fin)
        out["pend_subida"] = amp / (d[i_max] - sos) if np.isfinite(sos) and d[i_max] > sos else np.nan
        out["pend_bajada"] = amp / (eos - d[i_max]) if np.isfinite(eos) and eos > d[i_max] else np.nan
    return out


def features_sensor(largo, prefijo, indices):
    filas = {}
    for (pid, idx), g in largo.groupby(["ID_POLIGONO", "indice"]):
        f = filas.setdefault(pid, {})
        mens = g.groupby("mes")["valor"].median()
        for m in MESES:
            f[f"{prefijo}_{idx}_m{m:02d}"] = mens.get(m, np.nan)
        for nom, (a, b) in VENTANAS.items():
            sel = g[(g["mes"] >= a) & (g["mes"] <= b)]["valor"]
            f[f"{prefijo}_{idx}_{nom}"] = sel.median() if len(sel) else np.nan
        for k, val in fenologia(g).items():
            f[f"{prefijo}_{idx}_{k}"] = val
        f[f"{prefijo}_{idx}_n_obs"] = len(g)
    tabla = pd.DataFrame.from_dict(filas, orient="index")
    tabla.index.name = "ID_POLIGONO"
    return tabla.reset_index()


def ubicacion():
    y = pd.read_csv(D / "ID_area_rendimiento_70_30_Reto_AgroCebada.csv").dropna(axis=1, how="all")
    shp = gpd.read_file(D / "Parcelas_Reto_AGC_CONJUNTO_70_30" / "Parcelas_Reto_AGC_CONJUNTO.shp",
                        encoding="latin1").rename(columns={"ID_POLIGON": "ID_POLIGONO"})
    cen = shp.to_crs(6372).geometry.centroid
    u = pd.DataFrame({"ID_POLIGONO": shp["ID_POLIGONO"], "Estado": shp["Estado"],
                      "Municipio": shp["Municipio"], "x_km": cen.x / 1000, "y_km": cen.y / 1000})
    # zonas geograficas: k-means sobre centroides de las 197 (no usa el rendimiento)
    u["zona"] = KMeans(3, n_init=10, random_state=0).fit_predict(u[["x_km", "y_km"]])
    return u.merge(y, on="ID_POLIGONO", validate="1:1")


def main():
    u = ubicacion()
    planet = features_sensor(leer_serie("Conjunto_datos_PRO_AgroCebada.csv", "Planet", IDX_PLANET),
                             "planet", IDX_PLANET)
    s2 = features_sensor(leer_serie("Conjunto_datos_BASICO_AgroCebada2026.csv", "Sentinel-2", IDX_S2),
                         "s2", IDX_S2)
    clima = pd.read_csv(PROC / "clima_ciclo_2025.csv")
    topo = pd.read_csv(PROC / "topografia_parcela.csv")[["ID_POLIGONO", "elev_mean", "pend_mean",
                                                          "elev_std"]]
    pro = pd.read_csv(PROC / "variables_pro_abr_oct_2025.csv")  # estadisticos ya validados por Boni

    df = u
    for t in (pro, planet, s2, clima, topo):
        df = df.merge(t, on="ID_POLIGONO", how="left", validate="1:1")
    assert len(df) == 197 and df["ID_POLIGONO"].is_unique
    df.to_csv(OUT, index=False)

    nulos = df.isna().mean()
    print(f"{len(df)} filas x {df.shape[1]} columnas -> {OUT.relative_to(ROOT)}")
    print("Columnas con >20 % de NaN:")
    print(nulos[nulos > 0.2].round(2).to_string() if (nulos > 0.2).any() else "  ninguna")
    print("\nSentinel-2: sensores presentes en BASICO 2025 y obs validas por parcela")
    print(s2.filter(like="_n_obs").describe().loc[["min", "50%", "max"]].round(0).to_string())
    print("\nZonas:", df.groupby(["zona", "Estado"]).size().to_dict())


if __name__ == "__main__":
    main()
