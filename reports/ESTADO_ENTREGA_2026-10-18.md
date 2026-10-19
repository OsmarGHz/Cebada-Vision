# Estado de la entrega — CebadaVision (18 oct 2026)

Resumen de lo que quedó hecho el 17–18 de octubre y de lo que falta antes del cierre del
**19 de octubre, 23:59**. Para correr todo, ver `INSTRUCCIONES_EJECUCION.md`. Las pruebas y el estado de la app
indicados abajo corresponden al registro previo del equipo; esta revisión documental no los
reproduce. Ver `REVISION_DOCUMENTAL_2026-10-18.md` para evidencia, reservas y pendientes.

## 1. Modelo (70 % de la calificación) — listo

| Modelo | RMSE | MAE | R² |
|---|---|---|---|
| Media regional (V0 del equipo) | 0.851 | 0.751 | −0.02 |
| Ridge provisional (9 variables, lo que tenía la app) | 0.551 | 0.418 | 0.58 |
| kNN espacial puro (k = 8) | 0.501 | 0.362 | 0.65 |
| **Final: ensamble LightGBM + Random Forest** | **0.491 ± 0.007** | **0.336** | **0.664** |

- **Qué es:** promedio de dos modelos. LightGBM con ubicación (rendimiento de las 8 parcelas
  vecinas, promedio de zona, coordenadas) + relieve + clima (11 variables). Random Forest con
  ubicación + fenología de Planet (80 variables: medianas mensuales, emergencia, máximo, duración,
  velocidad de secado) + clima + relieve. Predicción recortada a 1.5–6.5 t/ha.
- **Validación:** 5 folds estratificados por estado × 10 repeticiones. La media de vecinos y de
  zona se calcula **dentro** de cada fold, solo con parcelas de entrenamiento (sin fuga del
  objetivo). Prueba extra: CV agrupada por municipio → RMSE 0.574 (kNN puro: 0.708), evidencia favorable en esta muestra, sin garantía para otras regiones o ciclos.
- **Hallazgo central (va en el reporte, sin esconderlo):** la ubicación explica ~2/3 de la
  varianza. Índices, clima y relieve agregan 0.01–0.02 t/ha una vez conocida la ubicación. No se demuestra superioridad estadística frente al kNN. Hay 138 rendimientos de pesaje
  en báscula sin ajustes por humedad, impurezas o mermas, redondeo a 0.5 en Tlaxcala y
  clima en 25 píxeles de 5 km; no puede atribuirse el límite solo al dato.
- **Por estado (RMSE/R²):** Hidalgo 0.357/0.784, Tlaxcala 0.375/−0.026, Puebla 0.578/0.007.
- **Incertidumbre:** margen orientativo ±0.63 t/ha, sin cobertura del 80 % calibrada.
- **Alcance temporal:** análisis retrospectivo con datos hasta noviembre de 2025; alertas
  precosecha y actualización por ciclo requieren validación adicional.
- **Preguntas guía (bonus), con evidencia en `reports/experimentos.md`:**
  1. Índice más importante: **EVI de Planet** (señal en mayo–junio y en la velocidad de secado).
  2. Variable climática: **precipitación del ciclo** (anomalía respecto a 2022–2024).
  3. Mejor combinación: **ubicación + relieve + clima + fenología Planet**. Sumar Sentinel-2 no mejora.
- **59 predicciones:** `submissions/predicciones_59_CebadaVision.csv` (EQUIPO, ID_POLIGONO,
  RENDIMIENTO_T_HA; 4 decimales). Media 3.95 t/ha, rango 2.88–4.65. Si la plantilla de FIRA trae
  otros encabezados, cotejar antes de adaptar una copia; los originales y valores se conservan.
  Copia con nombre de entrega: `reports/entrega/CebadaVision_prediccion.csv`.

Scripts: `src/features.py` → `src/modelar.py` → `src/modelo_final.py` → `src/exportar_app.py`.
Nota: `particiones_cv.csv` y `validacion_cv.py` originales no están en ningún branch; los folds
se generan con `RepeatedStratifiedKFold(5, 10, random_state=42)` sobre Estado (V0 da 0.851 igual).

## 2. App (30 %) — estado previo y discrepancias pendientes

- Datos del modelo final en `agrocebada-pagina/public/data/` (`parcelas.geojson`, `modelo.json`,
  `series.json`, `predicciones.csv`). `npm run validate` ✓, 24/24 pruebas ✓, `npm run build` ✓.
- Nuevo: en la ficha de parcela, tarjeta **"¿Cómo se llegó a este número?"** con nota en
  lenguaje llano y factores SHAP (lo que FIRA pidió con prioridad productor). Página Modelo muestra
  las respuestas a las preguntas guía del equipo. Acerca corregido (issue #13: "proporcional entre
  estados", Planet en el modelo final, descripción del modelo). Nombre **CebadaVision**.
- Simulador: Ridge sustituta (RMSE de ajuste frente al ensamble 0.3161 t/ha sobre las mismas
  197 parcelas). Mapa y ficha muestran predicciones precalculadas del ensamble. La sustituta
  no tiene validación independiente contra rendimientos reales ni interpretación causal.
- Cotejo del código actual (`d77d4852f1b0ed7256428cbb22e188be68dcbbfd`): persisten
  «sin medición instrumental», etiquetas de intervalo al 80 % y kNN 0.506; el simulador
  necesita distinguir Ridge del ensamble. Ver el detalle en la revisión documental.
- **No verificado visualmente** (Chrome no abrió localhost desde la automatización). Revisar con
  `npm run preview` antes de desplegar.

## 3. Documentos — correcciones propuestas, pendientes de aprobación

| Archivo | Qué es |
|---|---|
| `reports/reporte_tecnico.md` | Las 7 secciones + bibliografía. Conteos de esta revisión y método: `REVISION_DOCUMENTAL_2026-10-18.md`. La plataforma puede contar distinto: pegar con "Guardar avances" y verificar; recortar si marca exceso. |
| `reports/anexos_final.md` | Tabla de 59 predicciones en 3 columnas, aportaciones por integrante, enlaces. Convertir a PDF (máx. 4 cuartillas). |
| `reports/guion_video.md` | Guion de 5 minutos por bloques, con cifras del modelo final. |
| `reports/experimentos.md` | Banco completo de experimentos (10 repeticiones). |
| `DECISIONES.md` | Entrada del 17 oct con todas las decisiones de cierre. |

Bibliografía: referencias y documentos técnicos de FIRA cotejados; pendiente integrar los prompts reales, su propósito y herramienta conforme a la guía (p. 4). Se descartó Arizo-García et al. (no localizada).

## 4. Pendiente del equipo (no automatizable)

| # | Qué | Quién | Issue |
|---|---|---|---|
| 1 | Desplegar la app (Netlify/Vercel/GitHub Pages con `dist/`), probar en incógnito y celular | Cervantes | #14 |
| 2 | Poner la URL en la plataforma y en `src/generar_anexos.py "URL_APP" "URL_VIDEO"` → regenera `anexos_final.md` | Osmar | #14 |
| 3 | Grabar el video con `reports/guion_video.md`, subir con acceso por enlace | Isaac + Cervantes | #15 |
| 4 | Cada integrante revisa y aprueba su fila en `reports/anexos.md` (sección A2) | Todos | #10 |
| 5 | Integrar prompts reales, propósito y herramienta en Bibliografía; A4 remite a ese registro | Todos | — |
| 6 | Pegar el reporte sección por sección en la plataforma; subir Bibliografía y Anexos en PDF; verificar enlaces en azul | Osmar | — |
| 7 | **Correo a innovacion@fira.gob.mx** con el CSV de 59 predicciones + código (zip del repo o liga) antes del 19 oct 23:59 | Osmar | — |
| 8 | Borrar el comentario "sex" en la issue #11 y cerrar #11, #12 (poner respuesta a preguntas guía), #5, #8 | Osmar / Boni | — |
| 9 | `gh auth logout` en la PC compartida | Boni | — |
