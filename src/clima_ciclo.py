"""Clima del ciclo abril-octubre 2025: una fila por parcela.

Entrada: data/processed/clima_mensual_parcela.csv (ID_POLIGONO, anio, mes, prec, tmin, tmax),
         generado por src/extraer_raster.py.
Salida:  data/processed/clima_ciclo_2025.csv (197 filas, una por ID_POLIGONO).

Columnas:
  prec_abr_oct          suma de precipitacion mensual (mm) abril-octubre 2025
  tmax_media_abr_oct    promedio de tmax mensual (C) abril-octubre 2025
  tmin_media_abr_oct    promedio de tmin mensual (C) abril-octubre 2025
  prec_anomalia         prec_abr_oct 2025 menos el promedio de prec_abr_oct de 2022, 2023 y 2024

Limitacion: los rasters de clima son de ~5 km, asi que muchas parcelas caen en el mismo pixel y
comparten valores. Al final se imprime cuantos valores unicos tiene cada columna.

Uso:  .venv/Scripts/python.exe src/clima_ciclo.py
"""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
ENT = ROOT / "data" / "processed" / "clima_mensual_parcela.csv"
OUT = ROOT / "data" / "processed" / "clima_ciclo_2025.csv"

MESES = range(4, 11)  # abril a octubre
ANIO = 2025
ANIOS_HIST = [2022, 2023, 2024]


def agregar_ciclo(clima, anio):
    """prec suma, tmax/tmin promedio de abril-octubre del anio dado, una fila por parcela."""
    ciclo = clima[(clima["anio"] == anio) & clima["mes"].isin(MESES)]
    assert not ciclo[["prec", "tmin", "tmax"]].isna().any().any(), f"NaN en clima {anio}"
    n_meses = ciclo.groupby("ID_POLIGONO")["mes"].nunique()
    assert (n_meses == len(MESES)).all(), f"faltan meses abr-oct {anio}"
    return ciclo.groupby("ID_POLIGONO").agg(
        prec_abr_oct=("prec", "sum"),
        tmax_media_abr_oct=("tmax", "mean"),
        tmin_media_abr_oct=("tmin", "mean"),
    )


def construir_tabla(clima):
    tabla = agregar_ciclo(clima, ANIO)
    hist = pd.concat([agregar_ciclo(clima, a)["prec_abr_oct"] for a in ANIOS_HIST], axis=1)
    tabla["prec_anomalia"] = tabla["prec_abr_oct"] - hist.mean(axis=1)
    return tabla.reset_index()


def main():
    tabla = construir_tabla(pd.read_csv(ENT))

    assert len(tabla) == 197 and tabla["ID_POLIGONO"].is_unique
    assert not tabla.isna().any().any()

    tabla.to_csv(OUT, index=False)
    print(f"Filas: {len(tabla)}  Columnas: {tabla.columns.tolist()}")
    print(tabla.describe().round(2).T.to_string())
    print("\nValores unicos por columna (esperado ~25, uno por pixel de ~5 km):")
    print(tabla.drop(columns="ID_POLIGONO").nunique().to_string())
    print(f"\nGuardada en {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
