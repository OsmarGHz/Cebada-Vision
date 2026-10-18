"""Exporta los datos que lee la app (agrocebada-pagina) a partir del modelo final.

Lee las salidas de src/modelo_final.py (data/processed/predicciones_197.csv y modelo_final.json)
y escribe, con el formato de docs/CONTRATO_DATOS.md de la app:
  parcelas.geojson   197 parcelas: geometria, estado, prediccion, intervalo, variables, nota en
                     lenguaje llano y factores SHAP
  modelo.json        metricas, importancias, combinaciones, simulador, umbrales, preguntas guia
  series.json        NDVI / EVI / MSAVI de Planet por fecha, abril-octubre 2025
  predicciones.csv   59 parcelas de PREDICCION (ID_POLIGONO, rendimiento_pred, 4 decimales)

Uso:  .venv/Scripts/python.exe src/exportar_app.py [carpeta_salida]
Por defecto escribe en data/app/. Luego copiar los 4 archivos a agrocebada-pagina/public/data/ y
correr `npm run validate`.
"""
import argparse
import json
from pathlib import Path

import geopandas as gpd
import pandas as pd
import shapely

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "DATASET_RETO_AGRO_2026"
PROC = ROOT / "data" / "processed"
FECHA_INI, FECHA_FIN = "2025-04-01", "2025-10-31"


def construir_parcelas(modelo):
    pred = pd.read_csv(PROC / "predicciones_197.csv")
    shp = gpd.read_file(D / "Parcelas_Reto_AGC_CONJUNTO_70_30" / "Parcelas_Reto_AGC_CONJUNTO.shp",
                        encoding="latin1").rename(columns={"ID_POLIGON": "ID_POLIGONO"})
    df = shp[["ID_POLIGONO", "geometry"]].merge(pred, on="ID_POLIGONO", validate="1:1")
    assert len(df) == 197
    cols_var = [v["nombre"] for v in modelo["variables"]]
    props = pd.DataFrame({
        "ID_POLIGONO": df["ID_POLIGONO"],
        "estado": df["Estado"],
        "municipio": df["Municipio"],
        "superficie_ha": df["AREA_HA"],
        "conjunto": df["CONJUNTO"].str.lower(),
        "rendimiento_real": df["RENDIMIENTO_T_HA"],
        "rendimiento_pred": df["rendimiento_pred"],
        "pred_lo": df["pred_lo"],
        "pred_hi": df["pred_hi"],
        "prediccion_cv": df["prediccion_cv"],
        "nota": df["nota"],
        "factores": df["factores"].map(json.loads),
        **{c: df[c].round(4) for c in cols_var},
    })
    geo = gpd.GeoDataFrame(props, geometry=shapely.force_2d(df.geometry.values), crs=shp.crs)
    return geo.to_crs(4326)


def construir_series():
    pro = pd.read_csv(D / "Conjunto_datos_PRO_AgroCebada.csv")
    pro["fecha"] = pd.to_datetime(pro["fecha_captura"], format="%d/%m/%Y")
    pro = pro[(pro["fecha"] >= FECHA_INI) & (pro["fecha"] <= FECHA_FIN)]
    largo = pro.melt(id_vars=["ID_POLIGONO", "fecha", "porcentaje_nubosidad"],
                     value_vars=["ndvi_promedio", "evi_promedio", "msavi_promedio"],
                     var_name="indice", value_name="valor").dropna(subset=["valor"])
    largo["indice"] = largo["indice"].str.removesuffix("_promedio").str.upper()
    largo["indice"] = pd.Categorical(largo["indice"], ["NDVI", "EVI", "MSAVI"], ordered=True)
    largo = largo.sort_values(["ID_POLIGONO", "fecha", "indice"])
    series = {}
    for pid, g in largo.groupby("ID_POLIGONO"):
        # nubosidad vacia o 0 se omite: la app la toma como 0 (criterio de FIRA)
        series[pid] = [{"fecha": f.strftime("%Y-%m-%d"), "indice": i, "valor": round(float(v), 3),
                        "fuente": "Planet", **({"nubosidad": float(n)} if n > 0 else {})}
                       for f, i, v, n in zip(g["fecha"], g["indice"], g["valor"],
                                             g["porcentaje_nubosidad"].fillna(0))]
    return series


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("salida", nargs="?", default=str(ROOT / "data" / "app"))
    a = ap.parse_args()
    out = Path(a.salida)
    out.mkdir(parents=True, exist_ok=True)

    modelo = json.loads((PROC / "modelo_final.json").read_text(encoding="utf-8"))
    geo = construir_parcelas(modelo)
    # GeoJSON no admite listas de objetos como propiedad via fiona: se escribe a mano
    fc = json.loads(geo.to_json(na="null", drop_id=True))
    for f, fac in zip(fc["features"], geo["factores"]):
        f["properties"]["factores"] = fac
    (out / "parcelas.geojson").write_text(json.dumps(fc, ensure_ascii=False, separators=(",", ":")),
                                          encoding="utf-8")
    (out / "modelo.json").write_text(json.dumps(modelo, ensure_ascii=False, indent=2), encoding="utf-8")
    (out / "series.json").write_text(json.dumps(construir_series(), separators=(",", ":")),
                                     encoding="utf-8")
    pred = (geo.loc[geo["conjunto"] == "prediccion", ["ID_POLIGONO", "rendimiento_pred"]]
            .sort_values("ID_POLIGONO"))
    assert len(pred) == 59
    pred.to_csv(out / "predicciones.csv", index=False, float_format="%.4f")

    mt = modelo["metricas"]
    print(f"{modelo['nombre']} v{modelo['version']}: RMSE {mt['rmse']}  MAE {mt['mae']}  R2 {mt['r2']}")
    for f in sorted(out.iterdir()):
        print(f"  {f.name:18s} {f.stat().st_size / 1024:8.0f} KB")


if __name__ == "__main__":
    main()
