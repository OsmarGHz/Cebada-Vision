# Cebada Vision — Reto AgroCebada 2026 (FIRA)

Predicción del rendimiento (t/ha) de 197 parcelas de cebada de temporal en Hidalgo, Tlaxcala y
Puebla, ciclo abril–octubre 2025.

## 1. Entorno

Python 3.13.

```bash
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt   # Windows
# .venv/bin/python -m pip install -r requirements.txt         # Linux / macOS
```

## 2. Datos crudos (no están en el repo)

El dataset oficial se descarga de la plataforma del reto (credenciales al correo del capitán) como
`DataSet.zip`. Descomprimir en la raíz del repo de modo que quede:

```
DATASET_RETO_AGRO_2026/
├── ID_area_rendimiento_70_30_Reto_AgroCebada.csv      rendimiento (138) + 59 a predecir
├── Conjunto_datos_BASICO_AgroCebada2026.csv           Sentinel-2 / Landsat, por fecha
├── Conjunto_datos_PRO_AgroCebada.csv                  Planet, por fecha
├── Parcelas_Reto_AGC_CONJUNTO_70_30/                  shapefile de polígonos (.shp + .dbf/.prj/.shx/.cpg)
├── Reto_AgroCebada_CHIRPS_Precipitacion_2022_2025/    precipitación mensual (TIF)
├── Reto_AgroCebada_Temperatura_2022_2025_RECORTADA_CHIRPS/   Tmin / Tmax mensual (TIF)
└── Reto_AgroCebada_Topografia_INEGI_CEM4/             elevación y pendiente (TIF)
```

`DATASET_RETO_AGRO_2026/` y `DataSet.zip` están en `.gitignore`.

## 3. Orden de ejecución

Desde la raíz del repo:

| # | Script | Lee | Escribe en `data/processed/` |
|---|---|---|---|
| 1 | `src/extraer_raster.py` | shapefile + TIF de clima y topografía | `clima_mensual_parcela.csv`, `topografia_parcela.csv` |
| 2 | `src/auditoria_datos.py` | CSV de rendimiento, shapefile, BASICO, PRO | `auditoria_union_4fuentes.csv` |
| 3 | `src/tabla_pro.py` | PRO | `variables_pro_abr_oct_2025.csv` |
| 4 | `src/clima_ciclo.py` | `clima_mensual_parcela.csv` (paso 1) | `clima_ciclo_2025.csv` |
| 5 | `src/exportar_app.py` | pasos 1–4 + dataset | `data/app/` (archivos que lee la app) |

```bash
.venv/Scripts/python.exe src/extraer_raster.py
.venv/Scripts/python.exe src/auditoria_datos.py
.venv/Scripts/python.exe src/tabla_pro.py
.venv/Scripts/python.exe src/clima_ciclo.py
.venv/Scripts/python.exe src/exportar_app.py
```

`tabla_pro.py` acepta opcionalmente la ruta a `particiones_cv.csv` para imprimir el RMSE del
modelo de media por fold.

## 4. Tablas por parcela (197 filas, llave `ID_POLIGONO`)

- `variables_pro_abr_oct_2025.csv`: ndvi, evi, lai, msavi (mean/std/max/min) + `n_obs`.
- `clima_ciclo_2025.csv`: `prec_abr_oct` (suma, mm), `tmax_media_abr_oct`, `tmin_media_abr_oct`
  (promedio, °C) y `prec_anomalia` (2025 menos promedio abr–oct 2022–2024).
  **Limitación:** los rásters de clima son de ~5 km; cada columna tiene solo 25 valores únicos
  (uno por píxel), así que el clima funciona casi como proxy de ubicación.
- `topografia_parcela.csv`: elevación y pendiente (mean/min/max/std) por polígono.

Unir con `ID_area_rendimiento_70_30_Reto_AgroCebada.csv` por `ID_POLIGONO` (el shapefile trae el
campo truncado como `ID_POLIGON`; los scripts lo renombran).

## 5. App

La app web está en otro repositorio:
[agrocebada-pagina](https://github.com/David54s/agrocebada-pagina). `src/exportar_app.py` genera
lo que la app lee (`parcelas.geojson`, `modelo.json`, `series.json`, `predicciones.csv`) con el
formato de su `docs/CONTRATO_DATOS.md`; se copian a `public/data/` de la app.

El modelo del exportador es un **Ridge provisional** (índices de Planet + clima + relieve, RMSE
de CV 0.551). Al tener el modelo final se cambia `VARIABLES` y `ajustar()` en el script; la app no
cambia. `data/app/` no se versiona aquí: los archivos viven en el repo de la app.

## 6. Estructura

```
src/             scripts de datos, features y modelo
data/processed/  tablas limpias y features (versionadas)
notebooks/       EDA y experimentos
app/             dashboard
reports/         reporte técnico y figuras
submissions/     predicciones de las 59 parcelas
DECISIONES.md    bitácora de acuerdos del equipo
prompts_ia.md    registro obligatorio de prompts de IA
```
