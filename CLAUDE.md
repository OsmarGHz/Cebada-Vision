# Reto AgroCebada 2026 (FIRA) — Contexto del proyecto

Datathon organizado por FIRA (Fideicomisos Instituidos en Relación con la Agricultura).
Fuente oficial: `Reto Agrocebada Bases.pdf` (en esta carpeta) y
https://www.fira.gob.mx/Nd/Convocatoria-2026.html#bases
Contacto: innovacion@fira.gob.mx

## Objetivo

Desarrollar un modelo que prediga el **rendimiento de parcelas de cebada** en Hidalgo, Tlaxcala y
Puebla, y convertirlo en una **solución funcional** (app web, dashboard interactivo u otra
herramienta) para visualizar y consultar resultados.

## Dataset

- Se descarga de la plataforma oficial del reto (credenciales llegan al correo del capitán).
- **197 parcelas georreferenciadas** con índices de vegetación, precipitación, temperatura y
  rendimiento al final de cosecha.
- Rendimiento disponible solo para el **70 %** (~138 parcelas); hay que **estimar el 30 %**
  restante (~59). El valor real lo resguarda el comité y solo se usa para calificar.
- Se permite usar **cualquier información pública adicional**.

## Evaluación

### Etapa 1 (define los 3 finalistas)

| Criterio | Peso |
|---|---|
| Desempeño predictivo y justificación técnica (RMSE, MAE, R² u otras que defina el comité) | 70 % |
| Aplicación o interfaz web (implementación práctica, utilidad para consulta/visualización) | 30 % |

**Bonus:** desarrollar y justificar las preguntas guía:
1. ¿Qué índice es más importante en la predicción?
2. ¿Qué variable climática tiene mayor peso?
3. ¿Qué combinación de variables funciona mejor?

### Etapa 2 (solo finalistas)

Presentación de máx. 15 minutos ante jurado. Se evalúa:
- Dominio de temas y herramientas.
- Justificación e interpretación de resultados; capacidad de transmitir conocimiento.
- Relación de la herramienta con un problema de política pública (**inclusión financiera** en el
  sector agropecuario y rural).
- Viabilidad de propuestas y conclusiones.

En empate técnico del modelo, la presentación decide 1.º, 2.º y 3.er lugar.

## Entregables (se suben a la plataforma)

### a) Reporte técnico

| Sección | Extensión |
|---|---|
| Introducción | 400–550 palabras |
| Justificación | 100–200 palabras |
| Objetivos | 200 palabras |
| Metodología | 600–700 palabras |
| Resultados y discusión | 800 palabras |
| Uso de la ciencia de datos en la inclusión financiera del sector agro | 300 palabras |
| Conclusiones | 400 palabras |
| Bibliografía | — |
| Anexos | máx. 4 cuartillas (el PDF de bases dice 2, pero FIRA confirmó en la sesión de dudas del 27-sep que el límite real es 4 — para dejar espacio a la tabla de predicciones) |

Los anexos deben incluir las **actividades y aportaciones de cada integrante**, los **prompts de
IA** utilizados, y (si se usa) la liga a repositorio/notebook (opcional, no obligatorio).

**Entrega adicional por correo (no está en el PDF de bases):** antes del cierre (19 oct) hay que
mandar a innovacion@fira.gob.mx un **CSV con el rendimiento predicho de las 59 parcelas**, aparte
de subir la solución a la plataforma. FIRA manda plantilla/recordatorio por correo. El código
fuente también puede mandarse como adjunto en ese mismo correo (GitHub no es obligatorio).

### b) Aplicación o interfaz

- App / interfaz web / dashboard **funcional** que ejecute el modelo y permita consultar
  resultados de forma interactiva.
- **Código fuente** de la app y del modelo, con documentación para ejecutarlo.
- **Video demostrativo** (máx. 5 min) explicando el modelo y la solución.
- **Enlace** a la app si está desplegada, para consulta del jurado.

## Calendario 2026

| Fecha | Evento |
|---|---|
| 19 ago | Publicación de la convocatoria |
| 19 ago – 07 sep | Inscripción |
| 14 sep | Entrega del dataset (inicio del reto) |
| 18 sep | Sesión de dudas en línea |
| **19 oct, 23:59** | **Fecha límite de entrega** |
| 03 nov | Notificación de los 3 finalistas |
| 10 nov | Presentación ante el jurado (en línea) |
| 20 nov | III Congreso Nacional de Ciencia de Datos y premiación (viáticos por cuenta del equipo) |

Nota: la página web indica 10 nov como "anuncio de finalistas"; el PDF de bases indica 03 nov
(notificación) y 10 nov (presentación). Se toma el PDF como referencia.

## Reglas importantes

- **Uso de IA permitido** siempre que se indique dónde se usó y se **anexen los prompts** en el
  escrito. Mantener el registro en `prompts_ia.md` conforme avance el proyecto.
- Equipos de 3 a 5 estudiantes de licenciatura con inscripción vigente en universidades de
  Hidalgo, Tlaxcala o Puebla.
- Causas de descalificación: información falsa o que no sea de autoría propia, no entregar
  documentación, no presentarse ante el jurado, tema distinto al del reto, incumplir las bases.
- Exclusiones: familiares de personal de FIRA, prestadores de servicio social en FIRA, o personas
  en SUSTRAE/BUROTEC.

## Premios (por integrante)

| Lugar | UDIS | Aprox. MXN (UDI = $8.6662) |
|---|---|---|
| 1.º | 2,884.77 | ~$25,000 |
| 2.º | 1,730.86 | ~$15,000 |
| 3.º | 1,153.91 | ~$10,000 |

## Estrategia técnica

- **Muestra pequeña** (~138 de entrenamiento): priorizar validación robusta (CV repetida; CV
  espacial/agrupada si las parcelas están agrupadas geográficamente) sobre complejidad del modelo.
- **Modelos candidatos:** Ridge / ElasticNet, Random Forest, gradient boosting pequeño, GPR,
  ensamble por promedio. Evitar deep learning.
- **Features:** fenología a partir de series de índices de vegetación (máximo, integral/AUC,
  fecha del pico, pendientes de crecimiento y senescencia); clima agregado por etapa fenológica
  (precipitación acumulada, grados-día, estrés térmico, heladas).
- **Datos externos posibles:** elevación (SRTM), suelo (SoilGrids), NASA POWER, CHIRPS,
  Sentinel-2 / Landsat vía Google Earth Engine, estadísticas SIAP por municipio.
- **Preguntas bonus:** SHAP / importancia por permutación + ablación por grupos de variables.
- **App:** prioridad productor (FIRA, sesión 2): nota en lenguaje llano de cómo se llegó al número. Mapa de parcelas, predicción con intervalo de incertidumbre, explicación por parcela
  y enfoque de riesgo crediticio / inclusión financiera.

## Dudas por resolver con el comité

- Métrica exacta del ranking y cómo se combinan RMSE, MAE y R² (RMSE confirmado como primer
  filtro; ponderación exacta con metodología y app aún no detallada).
- Formato del archivo de predicciones: ya se sabe (sesión 2) — un número por parcela, máx. 4 decimales, 59 filas (equipo + ID + t/ha), sin intervalos; plantilla llega por correo. Sin ponderar por superficie.
- Fechas exactas de siembra/cosecha (ciclo: todo temporal; siembra típica 1 may–15 jun; FIRA podría dar fecha de algunas parcelas). Desconocidos: rotación, siniestros, dosis, variedad.
- Coordenadas: ¿centroide o polígono?
- ¿La app debe estar desplegada en línea o basta ejecución local?
- Fórmulas exactas de cálculo de cada índice espectral y cómo se excluyen píxeles con nubes/
  sombras (pendiente que FIRA mande por correo; hay valores negativos de índices con nubosidad
  0% sin explicar aún).

## Hechos clave del dataset

- Rendimiento = ciclo **abr–oct 2025** únicamente; datos 2022–2024 solo como historial.
- Rendimiento = **grano** (no forraje), t/ha. Fuente: mayormente la **comercializadora/parafinanciera** que le compra al productor (pocos casos directos del productor); sin medición instrumental. Una medición por parcela.
- Todas las parcelas son de **temporal** (sin riego) — confirmado por FIRA (27-sep).
- Partición 70/30 entrenamiento/predicción es **estratificada por zona geográfica**, no aleatoria
  pura — cada una de las 3 zonas está representada en ambos conjuntos.
- Shapefile: campo ID truncado a `ID_POLIGON` → renombrar a `ID_POLIGONO`. Los `.shp` vienen
  siempre acompañados de `.dbf`/`.prj`/`.shx`/`.cpg` en la misma carpeta (abrir solo el `.shp` en
  QGIS, arrastra el resto automático).
- Los TIF no son solo clima: incluyen también **elevación (DEM)** y **pendiente del terreno**
  como capas/variables geofísicas adicionales — agregarlas como features, no solo hipótesis.
- Tres zonas: este/Puebla (~4.5 t/ha), suroeste/Tlaxcala (~3.0, valores redondeados a 0.5),
  norte/Hidalgo (~3.25). Ubicación explica ~63 % de la varianza.
- Sentinel-2 y Landsat en filas separadas; Planet (PRO) no se fusiona con S2 como equivalente.
  Planet = mejor resolución espacial pero menos índices; Sentinel/Landsat = más índices, menor
  resolución. Ninguno es "mejor" — comparar combinaciones es parte del reto (pregunta bonus 3).
- Nubosidad casi binaria (0 o 100); con 100 los índices vienen vacíos. Cada observación trae su
  % de nubosidad explícito; vacío = 0% (satélite no detectó nubes).
- Clima ~5 km: solo 25 píxeles distintos → casi proxy de ubicación.
- Ejecutar con `D:\AgroCebada\.venv\Scripts\python.exe`.

## Estructura

```
data/raw/        dataset oficial (no versionar)
data/external/   datos públicos descargados (clima, suelo, elevación, satélite)
data/processed/  tablas limpias y features
notebooks/       EDA y experimentos
src/             código reutilizable (features, modelos, validación)
app/             dashboard (Streamlit)
reports/         reporte técnico y figuras
submissions/     predicciones del 30 %
prompts_ia.md    registro obligatorio de prompts de IA
```

Entorno: Python 3.13, dependencias en `requirements.txt`.

## Estado

- [x] Bases estudiadas
- [x] Dataset descargado en `DATASET_RETO_AGRO_2026/`
- [x] EDA → ver `reports/eda_hallazgos.md` (baseline a vencer: kNN espacial RMSE 0.507, R² 0.64)
- [x] Modelo base + esquema de validación (`src/modelar.py`, CV 5×10 estratificada + municipio)
- [x] Ingeniería de variables (`src/features.py`; sin datos externos adicionales)
- [x] Predicciones del 30 % (`submissions/predicciones_59_CebadaVision.csv`; modelo final RMSE 0.491)
- [x] App / dashboard (`agrocebada-pagina/`, datos del modelo final en `public/data/`) — falta **desplegar** y pegar URL
- [x] Reporte técnico (`reports/reporte_tecnico.md`; anexos en `reports/anexos_final.md`)
- [ ] Video demo (guion en `reports/guion_video.md`; falta grabar)
- [ ] Correo a innovacion@fira.gob.mx con CSV + código antes del 19 oct 23:59
