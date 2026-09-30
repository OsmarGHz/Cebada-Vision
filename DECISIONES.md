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

## Registro de uso de IA (obligatorio en la entrega — llenar según se use)
| Fecha | Herramienta | Para qué se usó |
|---|---|---|
| | | |
