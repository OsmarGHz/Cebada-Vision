# Anexos (máx. 4 cuartillas) — CebadaVision

## A1. Predicciones de las 59 parcelas (t/ha, 4 decimales)

Rendimiento de grano estimado por el modelo final (ensamble LightGBM + Random Forest) para las 59
parcelas del conjunto de predicción. Mismos identificadores y valores que el CSV preparado para FIRA, aún pendiente de envío.

<!-- TABLA_PREDICCIONES -->

## A2. Actividades y aportaciones de cada integrante

Relación pendiente de revisión y aprobación por cada integrante.

| Integrante | Rol | Actividades y aportaciones |
|---|---|---|
| Osmar Javier (capitán) | Coordinación | Organización en sprints e issues de GitHub; registro de decisiones (`DECISIONES.md`); seguimiento de las sesiones de dudas con FIRA; integración de entregables y carga en la plataforma. |
| David Bonifacio | Datos | Auditoría independiente de IDs, fechas y unión de fuentes (`src/auditoria_datos.py`); extracción de clima y topografía por polígono (`src/extraer_raster.py`); tabla PRO por parcela con filtro de nubosidad sin imputación (`src/tabla_pro.py`); clima por ciclo y README reproducible (`src/clima_ciclo.py`). |
| Hugo Palencia | Modelo | Baseline V0 (media) y V1 (regresión lineal) con los folds fijos; comparación por bloques de variables; Random Forest con clima y municipio/estado codificados (RMSE 0.513 ± 0.087, R² 0.621), que confirmó el peso de la ubicación. |
| David Cervantes | App | Diseño y desarrollo de la aplicación web (React/TypeScript/Leaflet), contrato de datos modelo→app, validador, modo productor/analista, simulador; despliegue público pendiente de verificación. |
| Isaac | Reporte | Documento compartido con las secciones y límites; redacción de Introducción, Justificación y Objetivos (base del informe final); referencias bibliográficas; guion del video con Cervantes. |
| Equipo | Modelo final | Ingeniería de variables fenológicas (`src/features.py`), banco de experimentos con CV repetida y agrupada (`src/modelar.py`), ensamble final y explicación por parcela (`src/modelo_final.py`), exportador (`src/exportar_app.py`). |

## A3. Enlaces

- Aplicación: <!-- URL_APP -->
- Video demostrativo: <!-- URL_VIDEO -->
- Repositorio de modelación: https://github.com/OsmarGHz/Cebada-Vision
- Repositorio de la aplicación: https://github.com/David54s/agrocebada-pagina
- Banco de experimentos completo: `reports/experimentos.md`

## A4. Uso de inteligencia artificial

El registro de prompts reales, su propósito y la herramienta utilizada debe incorporarse en
Bibliografía, conforme a la guía de FIRA (p. 4). Sigue pendiente de integración y aprobación
por el equipo en `reports/entrega/bibliografia.md`. No se han inventado registros de uso.
