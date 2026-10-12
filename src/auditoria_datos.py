"""Auditoria de datos: IDs, fechas, y prueba de union sin parcelas perdidas.

Frente Datos - primera tarea (ver reports/auditoria_datos.md para el resumen).
"""
from pathlib import Path

import geopandas as gpd
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "DATASET_RETO_AGRO_2026"
OUT = ROOT / "data" / "processed"
pd.set_option("display.width", 200, "display.max_columns", 40)


def cargar():
    y = pd.read_csv(D / "ID_area_rendimiento_70_30_Reto_AgroCebada.csv").dropna(axis=1, how="all")
    shp = gpd.read_file(
        D / "Parcelas_Reto_AGC_CONJUNTO_70_30" / "Parcelas_Reto_AGC_CONJUNTO.shp",
        encoding="latin1",
    ).rename(columns={"ID_POLIGON": "ID_POLIGONO"})  # dbf trunca nombre de campo a 10 caracteres
    basico = pd.read_csv(D / "Conjunto_datos_BASICO_AgroCebada2026.csv")
    pro = pd.read_csv(D / "Conjunto_datos_PRO_AgroCebada.csv")
    for df, col in [(basico, "fecha_captura"), (pro, "fecha_captura")]:
        df["fecha"] = pd.to_datetime(df[col], format="%d/%m/%Y", dayfirst=True)
    return y, shp, basico, pro


def auditar_ids(y, shp, basico, pro):
    # clima y topografia no se auditan aqui: extraer_raster.py toma sus IDs del mismo
    # shapefile, asi que coincidirian por construccion y la revision no probaria nada
    fuentes = {
        "ID_area_rendimiento (objetivo)": set(y["ID_POLIGONO"]),
        "Shapefile parcelas": set(shp["ID_POLIGONO"]),
        "BASICO (Sentinel/Landsat)": set(basico["ID_POLIGONO"]),
        "PRO (Planet)": set(pro["ID_POLIGONO"]),
    }
    base = fuentes["ID_area_rendimiento (objetivo)"]
    # una fila por ID (no por observacion); series largas (satelite por fecha) se
    # comparan aparte porque repiten ID por diseno (una fila por fecha)
    filas_por_id = {
        "ID_area_rendimiento (objetivo)": y,
        "Shapefile parcelas": shp,
    }
    filas = []
    for nombre, ids in fuentes.items():
        df_id = filas_por_id.get(nombre)
        dup = df_id["ID_POLIGONO"].duplicated().any() if df_id is not None else None
        filas.append({
            "fuente": nombre,
            "n_ids_unicos": len(ids),
            "id_duplicado_indebido": dup,
            "faltan_vs_objetivo": sorted(base - ids),
            "sobran_vs_objetivo": sorted(ids - base),
        })
    tabla = pd.DataFrame(filas)
    return tabla


def prueba_union(y, shp, basico, pro):
    """Union shapefile + CSV rendimiento + BASICO + PRO por ID_POLIGONO.

    No debe perder ni duplicar parcelas de ninguna de las 4 fuentes.
    """
    m = y.merge(shp[["ID_POLIGONO", "Municipio", "Estado", "CONJUNTO"]], on="ID_POLIGONO",
                how="outer", suffixes=("_y", "_shp"), indicator="_merge_shp")
    conjunto_inconsistente = (m["CONJUNTO_y"] != m["CONJUNTO_shp"]).sum()

    ids_basico = set(basico["ID_POLIGONO"])
    ids_pro = set(pro["ID_POLIGONO"])
    m["en_basico"] = m["ID_POLIGONO"].isin(ids_basico)
    m["en_pro"] = m["ID_POLIGONO"].isin(ids_pro)

    resumen_shp = m["_merge_shp"].value_counts().rename_axis("resultado_union_shp").reset_index(name="n")
    resumen_4 = pd.DataFrame([{
        "fuente": "shapefile",
        "presentes": (m["_merge_shp"] != "left_only").sum(),
    }, {
        "fuente": "BASICO",
        "presentes": m["en_basico"].sum(),
    }, {
        "fuente": "PRO",
        "presentes": m["en_pro"].sum(),
    }])
    resumen_4["faltantes_de_197"] = 197 - resumen_4["presentes"]

    return m, resumen_shp, resumen_4, conjunto_inconsistente


def main():
    y, shp, basico, pro = cargar()

    print("== Fechas: rango y formato ==")
    for nombre, df in [("BASICO", basico), ("PRO", pro)]:
        print(f"{nombre}: {df['fecha'].min().date()} -> {df['fecha'].max().date()}, "
              f"nulos tras parseo: {df['fecha'].isna().sum()}")

    print("\n== Auditoria de IDs por fuente ==")
    tabla_ids = auditar_ids(y, shp, basico, pro)
    print(tabla_ids.drop(columns=["faltan_vs_objetivo", "sobran_vs_objetivo"]).to_string(index=False))
    print("(id_duplicado_indebido = None para tablas largas por diseno: BASICO/PRO por fecha)")
    for _, r in tabla_ids.iterrows():
        if r["faltan_vs_objetivo"] or r["sobran_vs_objetivo"]:
            print(f"  {r['fuente']}: faltan={r['faltan_vs_objetivo']} sobran={r['sobran_vs_objetivo']}")

    print("\n== Confirmacion split CONJUNTO / rendimiento ==")
    print(y["CONJUNTO"].value_counts().to_string())
    cross = pd.crosstab(y["CONJUNTO"], y["RENDIMIENTO_T_HA"].isna(), rownames=["CONJUNTO"],
                         colnames=["rendimiento_nulo"])
    print(cross.to_string())
    ok_split = (y.query("CONJUNTO == 'ENTRENAMIENTO'")["RENDIMIENTO_T_HA"].notna().all()
                and y.query("CONJUNTO == 'PREDICCION'")["RENDIMIENTO_T_HA"].isna().all()
                and (y["CONJUNTO"] == "ENTRENAMIENTO").sum() == 138
                and (y["CONJUNTO"] == "PREDICCION").sum() == 59)
    print("split 138 ENTRENAMIENTO con rendimiento / 59 PREDICCION sin rendimiento:", ok_split)

    print("\n== Prueba de union: shapefile + CSV rendimiento + BASICO + PRO (ID_POLIGON -> ID_POLIGONO) ==")
    m, resumen_shp, resumen_4, conjunto_inconsistente = prueba_union(y, shp, basico, pro)
    print(resumen_shp.to_string(index=False))
    print("filas con CONJUNTO distinto entre CSV rendimiento y shapefile:", conjunto_inconsistente)
    print()
    print(resumen_4.to_string(index=False))
    print("total parcelas tras union (base = CSV rendimiento):", len(m), "(esperado: 197)")
    print("duplicados de ID_POLIGONO tras union:", m["ID_POLIGONO"].duplicated().sum(), "(esperado: 0)")

    out_path = OUT / "auditoria_union_4fuentes.csv"
    m.to_csv(out_path, index=False)
    print(f"\nTabla de union guardada en {out_path}")
    # la tabla PRO por parcela se genera en src/tabla_pro.py


if __name__ == "__main__":
    main()
