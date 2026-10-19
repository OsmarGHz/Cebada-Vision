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
| 5 | `src/features.py` | pasos 1, 3, 4 + PRO y BASICO crudos | `features_parcela.csv` (285 variables: fenología Planet y Sentinel-2, clima, relieve, ubicación) |
| 6 | `src/modelar.py` | paso 5 | `reports/experimentos.md` y `.csv` (banco de experimentos, CV 5×10 + municipio) |
| 7 | `src/modelo_final.py` | paso 5 (+ 6 para textos) | `predicciones_197.csv`, `modelo_final.json`, `submissions/predicciones_59_CebadaVision.csv` |
| 8 | `src/exportar_app.py` | paso 7 + shapefile + PRO | `data/app/` (archivos que lee la app) |
| 9 | `src/generar_anexos.py` | paso 7 | `reports/anexos_final.md` |

```bash
.venv/Scripts/python.exe src/extraer_raster.py
.venv/Scripts/python.exe src/auditoria_datos.py
.venv/Scripts/python.exe src/tabla_pro.py
.venv/Scripts/python.exe src/clima_ciclo.py
.venv/Scripts/python.exe src/features.py
.venv/Scripts/python.exe src/modelar.py          # ~10 min; --rapido para 3 repeticiones
.venv/Scripts/python.exe src/modelo_final.py     # ~4 min
.venv/Scripts/python.exe src/exportar_app.py
.venv/Scripts/python.exe src/generar_anexos.py "URL de la app" "URL del video"
```

## 3b. Modelo final

Ensamble (promedio) de LightGBM —ubicación, relieve, clima— y Random Forest —ubicación, fenología
de Planet, clima, relieve—. Ubicación = rendimiento promedio de las 8 parcelas vecinas (ponderado
por distancia), promedio de la zona y coordenadas; se calcula dentro de cada fold de validación.
Validación: 5 folds estratificados por estado × 10 repeticiones. **RMSE 0.491 ± 0.007, MAE 0.336,
R² 0.664** (media regional 0.851; kNN espacial 0.501). Detalle en `reports/experimentos.md`,
`reports/reporte_tecnico.md` y `DECISIONES.md` (17 oct). La reducción de 0.010 t/ha frente al
kNN es pequeña y no demuestra superioridad estadística. El margen ±0.63 t/ha es orientativo,
sin cobertura del 80 % calibrada. El R² por estado es 0.784 en Hidalgo, 0.007 en Puebla y
−0.026 en Tlaxcala. El análisis retrospectivo usa observaciones hasta noviembre de 2025;
la predicción precosecha y la actualización por ciclo requieren validación adicional.

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

El exportador lee las salidas de `src/modelo_final.py` (no reentrena). Además del contrato base,
escribe por parcela una `nota` en lenguaje llano y los `factores` SHAP, y en `modelo.json` las
`preguntas_guia`. `data/app/` no se versiona aquí: los archivos viven en el repo de la app
(`public/data/`). El mapa y las fichas consultan predicciones precalculadas del ensamble;
el navegador ejecuta el simulador Ridge sustituto (RMSE de ajuste frente al ensamble: 0.3161
t/ha sobre las mismas 197 parcelas), sin interpretación causal. Esta cifra no es su error
validado contra rendimientos reales.

Revisión documental, fuentes y pendientes: `reports/REVISION_DOCUMENTAL_2026-10-18.md`.
Copia con nombre para entrega: `reports/entrega/CebadaVision_prediccion.csv`; conserva
exactamente los bytes del CSV original y requiere cotejo con la plantilla oficial.

## 6. Estructura

```
src/             scripts de datos, features y modelo
data/processed/  tablas limpias y features (versionadas)
notebooks/       EDA y experimentos
app/             dashboard
reports/         reporte técnico y figuras
submissions/     predicciones de las 59 parcelas
DECISIONES.md    bitácora de acuerdos del equipo
```
