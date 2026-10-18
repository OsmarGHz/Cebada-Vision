# Anexos (máx. 4 cuartillas) — CebadaVision

## A1. Predicciones de las 59 parcelas (t/ha, 4 decimales)

Rendimiento de grano estimado por el modelo final (ensamble LightGBM + Random Forest) para las 59
parcelas del conjunto de predicción. Mismo contenido que el archivo CSV enviado a FIRA.

<!-- TABLA_PREDICCIONES -->

## A2. Actividades y aportaciones de cada integrante

| Integrante | Rol | Actividades y aportaciones |
|---|---|---|
| Osmar Javier (capitán) | Coordinación | Organización en sprints e issues de GitHub; registro de decisiones (`DECISIONES.md`); seguimiento de las sesiones de dudas con FIRA; integración de entregables y carga en la plataforma. |
| David Bonifacio | Datos | Auditoría independiente de IDs, fechas y unión de fuentes (`src/auditoria_datos.py`); extracción de clima y topografía por polígono (`src/extraer_raster.py`); tabla PRO por parcela con filtro de nubosidad sin imputación (`src/tabla_pro.py`); clima por ciclo y README reproducible (`src/clima_ciclo.py`). |
| Hugo Palencia | Modelo | Baseline V0/V1 con los folds fijos; comparación Ridge por bloques de variables (`docs/experimentos.md`); validación de referencias del modelo. |
| David Cervantes | App | Diseño y desarrollo de la aplicación web (React/TypeScript/Leaflet), contrato de datos modelo→app, validador, modo productor/analista, simulador y despliegue público. |
| Isaac | Reporte | Documento compartido con las secciones y límites; borrador de Introducción, Justificación y Objetivos; referencias; guion del video con Cervantes. |
| Equipo (con asistencia de IA) | Modelo final | Ingeniería de variables fenológicas (`src/features.py`), banco de experimentos con CV repetida y agrupada (`src/modelar.py`), ensamble final, SHAP y notas en lenguaje llano (`src/modelo_final.py`), exportador (`src/exportar_app.py`). Ver A3. |

## A3. Uso de inteligencia artificial y prompts

Se usó Claude (Anthropic) como asistente de programación y redacción, siempre con revisión del
equipo. El registro completo, con fecha, integrante, uso y prompt textual, está en `prompts_ia.md`
del repositorio; se reproduce íntegro aquí.

<!-- PROMPTS_IA -->

## A4. Enlaces

- Aplicación: <!-- URL_APP -->
- Video demostrativo: <!-- URL_VIDEO -->
- Repositorio de modelación: https://github.com/OsmarGHz/Cebada-Vision
- Repositorio de la aplicación: https://github.com/David54s/agrocebada-pagina
- Banco de experimentos completo: `reports/experimentos.md`
