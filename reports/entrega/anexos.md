# Anexos (máx. 4 cuartillas) — CebadaVision

## A1. Predicciones de las 59 parcelas (t/ha, 4 decimales)

Rendimiento de grano estimado por el modelo final (ensamble LightGBM + Random Forest) para las 59
parcelas del conjunto de predicción. Mismos identificadores y valores que el CSV preparado para FIRA, aún pendiente de envío.

| ID | t/ha | ID | t/ha | ID | t/ha |
|---|---:|---|---:|---|---:|
| AGC_003 | 3.4582 | AGC_076 | 4.6049 | AGC_142 | 4.6490 |
| AGC_011 | 4.5491 | AGC_082 | 4.5076 | AGC_143 | 4.5267 |
| AGC_016 | 4.4001 | AGC_085 | 4.2365 | AGC_147 | 2.9875 |
| AGC_025 | 3.0380 | AGC_086 | 3.0426 | AGC_149 | 4.4601 |
| AGC_027 | 2.9742 | AGC_087 | 2.8776 | AGC_153 | 4.2589 |
| AGC_028 | 4.5693 | AGC_088 | 4.4664 | AGC_154 | 4.5223 |
| AGC_029 | 2.9709 | AGC_091 | 4.5210 | AGC_156 | 3.2345 |
| AGC_030 | 3.1045 | AGC_093 | 2.9494 | AGC_158 | 4.2025 |
| AGC_031 | 4.2783 | AGC_094 | 4.4543 | AGC_173 | 3.1163 |
| AGC_036 | 4.4455 | AGC_095 | 4.5666 | AGC_174 | 4.3857 |
| AGC_039 | 2.9821 | AGC_107 | 4.4860 | AGC_175 | 4.4178 |
| AGC_042 | 3.0120 | AGC_113 | 3.1797 | AGC_177 | 4.4497 |
| AGC_043 | 4.4842 | AGC_116 | 4.4596 | AGC_182 | 4.4916 |
| AGC_050 | 3.0147 | AGC_118 | 3.0863 | AGC_183 | 2.9948 |
| AGC_052 | 4.4507 | AGC_120 | 3.0751 | AGC_186 | 4.5575 |
| AGC_061 | 3.0559 | AGC_126 | 4.4792 | AGC_188 | 4.5433 |
| AGC_063 | 4.5332 | AGC_128 | 4.5121 | AGC_190 | 4.4076 |
| AGC_065 | 4.4761 | AGC_129 | 3.3870 | AGC_191 | 4.6349 |
| AGC_071 | 2.9163 | AGC_130 | 4.4504 | AGC_192 | 4.5541 |
| AGC_075 | 2.9131 | AGC_136 | 4.4922 |  |  |

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

- Aplicación: (pendiente de despliegue)
- Video demostrativo: (pendiente)
- Repositorio de modelación: https://github.com/OsmarGHz/Cebada-Vision
- Repositorio de la aplicación: https://github.com/David54s/agrocebada-pagina
- Banco de experimentos completo: `reports/experimentos.md`

## A4. Uso de inteligencia artificial

El registro de prompts reales, su propósito y la herramienta utilizada debe incorporarse en
Bibliografía, conforme a la guía de FIRA (p. 4). Sigue pendiente de integración y aprobación
por el equipo en `reports/entrega/bibliografia.md`. No se han inventado registros de uso.
