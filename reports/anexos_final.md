# Anexos (máx. 4 cuartillas) — CebadaVision

## A1. Predicciones de las 59 parcelas (t/ha, 4 decimales)

Archivo: `submissions/predicciones_59_CebadaVision.csv` (mismo contenido que se envía por correo a
innovacion@fira.gob.mx). La tabla se genera con el script de abajo y se pega aquí en tres columnas
para que quepa en una cuartilla.

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

> Cada integrante revisa y aprueba su fila (issue #10). Completar con 3–5 líneas de hechos.

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


| Fecha | Herramienta | Integrante | Uso (sección / archivo) | Prompt |
|---|---|---|---|---|
| 2026-09-17 | Claude Code | | Lectura y resumen de las bases del reto; creación de `CLAUDE.md` | "vamos a trabajar en un proyecto para el datathon AgroCebada, estudia el pdf y la info de esta pagina: https://www.fira.gob.mx/Nd/Convocatoria-2026.html#bases" |
| 2026-09-17 | Claude Code | | Documento de contexto del proyecto | "ok, igual genera un .md para el contexto" |
| 2026-09-18 | Claude Code | | Planeación de siguientes pasos y estructura del proyecto | "que sigue?" |
| 2026-09-18 | Claude Code | | EDA, extracción de clima/topografía por parcela, baselines espaciales (`src/eda_*.py`, `src/extraer_raster.py`, `reports/eda_hallazgos.md`) | "ya está el dataset, continua con lo del punto 1" |
| 2026-10-02 | Claude Code | | Tabla PRO una fila por parcela abr–oct 2025, nulos omitidos y verificados (`src/tabla_pro.py`, `data/processed/variables_pro_abr_oct_2025.csv`) | "Objetivo: Dejar en el repo la tabla de una fila por parcela con variables de PRO (abril–octubre 2025), lista para el baseline de Hugo" (issue + revisión del issue anterior) |
| 2026-10-11 | Claude Code | | Tabla de clima abr–oct 2025 por parcela (`src/clima_ciclo.py`, `data/processed/clima_ciclo_2025.csv`), README con orden de ejecución, versiones fijadas en `requirements.txt`, `n_obs` única en tabla PRO, auditoría sin revisión redundante de IDs de clima/topografía | "este es un nuevo issue, hazlo y dime como entregarlo" (captura del issue: tabla de clima por parcela + repo reproducible) |
| 2026-10-11 | Claude Code | | Revisión de la app (`agrocebada-pagina`) contra las bases; exportador de datos reales con Ridge provisional (`src/exportar_app.py`) y ajustes de textos en la app | "como vez agrocebada-pagina cumple?" / "puedes hacerlo y hacer las modificaciones en el repo original?" |
| 2026-09-30 a 2026-10-06 | Claude (claude.ai) | Osmar | Seguimiento de issues del equipo, revisión del borrador de Isaac, verificación de scripts de Boni, baseline de Hugo, actualización de `contexto_proyecto.md` y `DECISIONES.md` | Chat compartido: "Por ahora te vas a encargar de checar el progreso de la parte de Isaac…", "qué me tocaría actualizar? Toca crear nuevas issues…", "como estaria eso de los prompts?", "Isaac ya hizo su parte…", "cuando alguien termine lo de una issue suya, qué tendría que reportar…", "Olvidé pasarte los archivos de boni", "Me puso Lucy…", "te paso el md de decisiones y el md de contexto… actualízalos" |
| 2026-10-17 | Claude Code | | Lectura del chat compartido y de las issues del repo `OsmarGHz/Cebada-Vision` (vía `gh`), resumen de estado y riesgos | "como te puedo pasar info de un chat de claude que me compartieron?" / "checa las issues del repositorio https://github.com/OsmarGHz/Cebada-Vision.git" |
| 2026-10-17 | Claude Code | | Ingeniería de variables fenológicas Planet/Sentinel-2 + ubicación (`src/features.py`); banco de experimentos con CV 5×10 estratificada y CV por municipio, vecinos fuera de fold (`src/modelar.py`, `reports/experimentos.md`); modelo final ensamble LightGBM+RF, importancia por permutación, ablación, SHAP y notas en lenguaje llano, CSV de 59 predicciones (`src/modelo_final.py`, `submissions/`); exportador para la app (`src/exportar_app.py`); ajustes de la app (nota llana, factores SHAP, preguntas guía, textos de Acerca, nombre CebadaVision); reporte técnico (`reports/reporte_tecnico.md`), guion del video, anexos | "en base a los avances reportados en los issues del repositorio, sus tres ramas, y la pagina ya hecha, necesito que termines y complementes el proyecto del reto… termina lo que empezaste" |


## A4. Enlaces

- Aplicación: (pendiente de despliegue)
- Video demostrativo: (pendiente)
- Repositorio de modelación: https://github.com/OsmarGHz/Cebada-Vision
- Repositorio de la aplicación: https://github.com/David54s/agrocebada-pagina
- Banco de experimentos completo: `reports/experimentos.md`
