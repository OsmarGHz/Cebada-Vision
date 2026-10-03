"""Tabla PRO (Planet): una fila por parcela, abril-octubre 2025.

Entrada: DATASET_RETO_AGRO_2026/Conjunto_datos_PRO_AgroCebada.csv (una fila por parcela y fecha).
Salida:  data/processed/variables_pro_abr_oct_2025.csv (197 filas, una por ID_POLIGONO).

Por cada indice (ndvi, evi, lai, msavi) se toma la columna `<indice>_promedio` de cada captura
(promedio del indice dentro del poligono) y se agrega en el tiempo por parcela con
mean, std (ddof=1), max y min. Ademas `<indice>_n_obs` = capturas con valor no nulo.

Nulos: se OMITEN, no se rellenan. En PRO los indices vienen vacios exactamente cuando
porcentaje_nubosidad == 100 (se verifica abajo); esas capturas se descartan con dropna y no hay
imputacion de ningun tipo. No incluye RENDIMIENTO_T_HA ni fold: se une desde particiones_cv.csv.

Uso:  .venv/Scripts/python.exe src/tabla_pro.py [ruta/particiones_cv.csv]
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "DATASET_RETO_AGRO_2026"
OUT = ROOT / "data" / "processed" / "variables_pro_abr_oct_2025.csv"

FECHA_INI, FECHA_FIN = "2025-04-01", "2025-10-31"
INDICES = ["ndvi", "evi", "lai", "msavi"]
ESTADISTICOS = ["mean", "std", "max", "min"]


def cargar_pro():
    pro = pd.read_csv(D / "Conjunto_datos_PRO_AgroCebada.csv")
    pro["fecha"] = pd.to_datetime(pro["fecha_captura"], format="%d/%m/%Y")
    return pro


def construir_tabla_pro(pro):
    ventana = pro[(pro["fecha"] >= FECHA_INI) & (pro["fecha"] <= FECHA_FIN)]
    cols = [f"{i}_promedio" for i in INDICES]

    # los nulos coinciden con nubosidad 100; si FIRA cambia el archivo, que truene aqui
    nulo = ventana[cols].isna()
    assert (nulo.all(axis=1) == nulo.any(axis=1)).all(), "nulos parciales entre indices"
    assert (nulo.all(axis=1) == (ventana["porcentaje_nubosidad"] >= 100)).all(), \
        "nulos no coinciden con nubosidad 100"
    assert not ventana.duplicated(["ID_POLIGONO", "fecha"]).any(), "fecha repetida por parcela"

    g = ventana.groupby("ID_POLIGONO")  # mean/std/max/min/count de pandas omiten NaN
    tabla = g[cols].agg(ESTADISTICOS)
    tabla.columns = [f"{c.removesuffix('_promedio')}_{s}" for c, s in tabla.columns]
    for c in cols:
        tabla[f"{c.removesuffix('_promedio')}_n_obs"] = g[c].count()
    tabla = tabla.reset_index()

    resumen = {
        "capturas_en_ventana": len(ventana),
        "capturas_descartadas_nulas": int(nulo.all(axis=1).sum()),
        "fecha_min_valida": ventana.loc[~nulo.all(axis=1), "fecha"].min().date(),
        "fecha_max_valida": ventana.loc[~nulo.all(axis=1), "fecha"].max().date(),
    }
    return tabla, resumen


def rmse_modelo_media(particiones, tabla):
    """Modelo de media por fold: predice el promedio de entrenamiento del fold."""
    df = particiones.merge(tabla[["ID_POLIGONO"]], on="ID_POLIGONO", how="inner")
    assert len(df) == len(particiones), "IDs de particiones no estan en la tabla PRO"
    err = []
    for f in sorted(df["fold"].unique()):
        tr, te = df[df["fold"] != f], df[df["fold"] == f]
        err.append(te["RENDIMIENTO_T_HA"] - tr["RENDIMIENTO_T_HA"].mean())
    return float(np.sqrt((pd.concat(err) ** 2).mean()))


def main():
    tabla, resumen = construir_tabla_pro(cargar_pro())

    assert len(tabla) == 197 and tabla["ID_POLIGONO"].is_unique
    assert not tabla.isna().any().any()
    assert not {"RENDIMIENTO_T_HA", "fold"} & set(tabla.columns)

    print(f"Ventana: {FECHA_INI} -> {FECHA_FIN}")
    for k, v in resumen.items():
        print(f"  {k}: {v}")
    print(f"Filas: {len(tabla)}  Columnas: {tabla.shape[1]}")
    print(tabla.columns.tolist())
    print(tabla[[f"{i}_n_obs" for i in INDICES]].describe().loc[["min", "50%", "max"]].to_string())

    tabla.to_csv(OUT, index=False)
    print(f"Guardada en {OUT.relative_to(ROOT)}")

    if len(sys.argv) > 1:
        part = pd.read_csv(sys.argv[1])
        print(f"RMSE modelo de media (folds de {sys.argv[1]}): {rmse_modelo_media(part, tabla):.3f}")


if __name__ == "__main__":
    main()
