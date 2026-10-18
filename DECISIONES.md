# Decisiones del proyecto — Reto AgroCebada 2026 (Cebada Vision)

Bitácora corta: fecha + qué se acordó, en una línea cuando se pueda. Se llena
conforme pasa, no se reconstruye después de memoria.

## 27 sep — Reunión de arranque
- Ciclo relevante para el rendimiento: abril–octubre 2025 (aclarado por FIRA en Q&A).
- El shapefile trae `ID_POLIGON` (truncado a 10 caracteres), los CSV traen
  `ID_POLIGONO` — se normaliza a `ID_POLIGONO` antes de cualquier unión.
- Unidad de modelado = una parcela (una fila), nunca una observación satelital suelta.
- Particiones de validación fijas en `particiones_cv.csv` (5 folds, semilla 42,
  estratificadas por Estado). Nadie las regenera; todos comparan contra las mismas.
- Referencia V0 (predecir la media de entrenamiento): RMSE=0.851, MAE=0.751 — piso
  mínimo que cualquier variable o modelo debe superar para justificarse.
- Roles: Datos – Bonifacio · Modelo – Hugo (posible apoyo de Osmar) · App – Cervantes
  · Reporte – Isaac (a confirmar) · Capitán – Osmar.
- Meta del domingo 4 de oct: tabla por parcela → baseline evaluado → CSV provisional
  para las 59 → consulta por ID. No es la entrega final, es prueba de flujo completo.

## 29 sep
- Isaac confirma: reporte es su tarea principal; apoyo secundario en App si
  Cervantes lo necesita.
- Corrección: PRO sí cubre hasta diciembre 2025 (incluye sep–oct). La afirmación
  anterior de que terminaba en agosto fue un error de comparar fechas como texto,
  no una limitación real del dataset. Se sigue empezando con PRO por tener menos
  huecos (~25% nulos vs. 58-71% en BASICO); BASICO se suma después por variedad
  de índices (25 vs. 4), no por cobertura de fechas.
- La pantalla provisional (Sprint 1, hace *lookup* de un CSV) y la app final
  (Sprint 2-3, ejecuta el modelo real) son dos entregables distintos, no una
  evolución del mismo código.

## Pendiente de confirmar con FIRA (sesión del 9 de octubre)
- Anexos: bases generales dicen máx. 2 cuartillas; lineamientos posteriores dicen
  máx. 4. Se diseña para que quepa en 2 mientras se confirma.
- Encabezados exactos esperados en el CSV de predicción.


## 17 oct — Modelo final, app y reporte (cierre técnico)
- **Modelo final = ensamble LightGBM + Random Forest** (promedio). M1: ubicación (vecinos kNN k=8,
  media de zona, x, y) + relieve + clima (11 variables). M2: ubicación + fenología Planet
  (80 variables: medianas mensuales, ventanas, emergencia, pico, duración, pendientes) + clima +
  relieve. Predicción recortada a 1.5–6.5 t/ha. Scripts: `src/features.py` → `src/modelar.py` →
  `src/modelo_final.py` → `src/exportar_app.py`.
- **Métricas (CV 5 folds estratificada por estado × 10 repeticiones, vecinos calculados dentro del
  fold):** RMSE 0.491 ± 0.007, MAE 0.336, R² 0.664. CV agrupada por municipio: RMSE 0.574.
  Referencias con los mismos folds: media 0.851; kNN espacial 0.501; Ridge provisional (9 vars) 0.551.
- **Hallazgo central:** la ubicación explica ~2/3 de la varianza; índices, clima y relieve agregan
  0.01–0.02 t/ha una vez conocida la ubicación. Se declara como limitación del dato (138 parcelas,
  rendimiento comercial redondeado en Tlaxcala, clima a 5 km), no se oculta.
- **Preguntas guía:** (1) EVI de Planet (señal en mayo–junio y velocidad de secado); (2) precipitación
  del ciclo (anomalía respecto a 2022–2024); (3) ubicación + relieve + clima + fenología Planet;
  Sentinel-2 no mejora sobre Planet. Evidencia en `reports/experimentos.md` y `modelo_final.json`.
- **Folds:** `particiones_cv.csv` original no está en ningún branch del repo; se usa
  `RepeatedStratifiedKFold(5, 10, random_state=42)` sobre Estado, documentado en `src/modelar.py`.
  El V0 reproduce 0.851 igual.
- **CSV para FIRA:** `submissions/predicciones_59_CebadaVision.csv` (EQUIPO, ID_POLIGONO,
  RENDIMIENTO_T_HA, 4 decimales, 59 filas). Ajustar encabezados a la plantilla de FIRA si difiere.
- **App:** nombre **CebadaVision**; ficha con nota en lenguaje llano y factores SHAP por parcela;
  página Modelo muestra las respuestas a las preguntas guía del equipo; Acerca corregido
  ("proporcional entre estados", Planet en el modelo final, descripción del modelo); simulador =
  ridge sustituta (diferencia típica con el ensamble reportada en `modelo.json`). Contrato de datos
  actualizado (`nota`, `factores`, `preguntas_guia` opcionales).
- **Reporte técnico:** `reports/reporte_tecnico.md`, secciones dentro de los límites de palabras.
  Bibliografía solo con referencias verificables; se descartó Arizo-García (no localizada).
- **Pendientes del equipo (no automatizables):** desplegar la app y pegar la URL (issue #14);
  grabar el video con `reports/guion_video.md` (issue #15); cada integrante aprueba su fila en
  `reports/anexos.md` (issue #10); pegar el reporte en la plataforma y verificar contador de
  palabras; enviar correo a innovacion@fira.gob.mx con CSV + código antes del 19 oct 23:59.

- **Borrador de Isaac (`Documento Cebada-Vision.docx`)** integrado al informe: su Introducción,
  Justificación y Objetivos son la base de esas secciones (con las afirmaciones ajustadas a lo que
  los datos sostienen); su referencia de la Fuente et al. (2023) verificada y citada. La de
  Arizo-García et al. no se localizó con ningún título/DOI, por lo que no se incluye.
- **Experimento de Hugo:** `OneHotRandomForest_0` (clima + municipio/estado one-hot, particiones
  propias): RMSE 0.513 ± 0.087, MAE 0.363, R² 0.621. Se cita en Resultados como evidencia del
  equipo del predominio de la ubicación.
