# Instrucciones de ejecución — CebadaVision

Reproduce el modelo, las 59 predicciones y los datos de la app desde cero. Probado en Windows 11
con Python 3.13 y Node 22. Todo se corre desde la raíz del repo `Cebada-Vision`.

## 1. Entorno Python

```bash
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt      # Windows
# .venv/bin/python -m pip install -r requirements.txt            # Linux / macOS
```

Dependencias clave: pandas, geopandas, rasterio, rasterstats, scikit-learn, lightgbm, shap, tabulate.

## 2. Datos crudos

Descargar `DataSet.zip` de la plataforma del reto y descomprimirlo en la raíz, de modo que exista
`DATASET_RETO_AGRO_2026/` con el CSV de rendimiento, BASICO, PRO, el shapefile y los TIF de clima y
topografía (ver README, sección 2). Esa carpeta está en `.gitignore`.

## 3. Pipeline completo (orden obligatorio)

| Paso | Comando | Tiempo | Salida |
|---|---|---|---|
| 1 | `.venv/Scripts/python.exe src/extraer_raster.py` | ~1 min | `data/processed/clima_mensual_parcela.csv`, `topografia_parcela.csv` |
| 2 | `.venv/Scripts/python.exe src/auditoria_datos.py` | seg | `data/processed/auditoria_union_4fuentes.csv` (verifica 197 IDs y 138/59) |
| 3 | `.venv/Scripts/python.exe src/tabla_pro.py` | seg | `data/processed/variables_pro_abr_oct_2025.csv` |
| 4 | `.venv/Scripts/python.exe src/clima_ciclo.py` | seg | `data/processed/clima_ciclo_2025.csv` |
| 5 | `.venv/Scripts/python.exe src/features.py` | ~1 min | `data/processed/features_parcela.csv` (285 variables) |
| 6 | `.venv/Scripts/python.exe src/modelar.py` | ~10 min (`--rapido`: ~3) | `reports/experimentos.md`, `reports/experimentos.csv` |
| 7 | `.venv/Scripts/python.exe src/modelo_final.py` | ~4 min | `data/processed/predicciones_197.csv`, `modelo_final.json`, **`submissions/predicciones_59_CebadaVision.csv`** |
| 8 | `.venv/Scripts/python.exe src/exportar_app.py` | ~1 min | `data/app/parcelas.geojson`, `modelo.json`, `series.json`, `predicciones.csv` |
| 9 | `.venv/Scripts/python.exe src/generar_anexos.py "URL_APP" "URL_VIDEO"` | seg | `reports/anexos_final.md` |

Los pasos 1–5 y 7–8 son deterministas (semillas fijas). El paso 6 solo produce las tablas del
reporte; el 7 lee `reports/experimentos.csv` para los textos de las preguntas guía (si no existe,
los deja genéricos).

Verificación rápida tras el paso 7: la consola debe imprimir
`ensamble RMSE 0.491±0.007 MAE 0.336 R2 0.664` y `predicción 59: media 3.947`.

## 4. Aplicación web (`agrocebada-pagina`, repo aparte)

```bash
cd agrocebada-pagina
npm install
# copiar los 4 archivos de Cebada-Vision/data/app/ a public/data/
npm run validate     # debe terminar sin ✗
npm test             # 24 pruebas
npm run dev          # http://localhost:5173
npm run build        # genera dist/ (sitio estático)
```

Despliegue: Netlify/Vercel con comando `npm run build` y carpeta `dist`, o subir `dist/` a GitHub
Pages. No necesita backend ni variables de entorno.

## 5. Qué entregar a FIRA

1. Plataforma: las 7 secciones de `reports/reporte_tecnico.md`, Bibliografía y Anexos
   (`reports/anexos_final.md`) en PDF, enlace a la app y video.
2. Correo a innovacion@fira.gob.mx antes del 19 oct 23:59: `submissions/predicciones_59_CebadaVision.csv`
   (ajustar encabezados a la plantilla de FIRA si difiere) + código fuente (zip o liga al repo).
