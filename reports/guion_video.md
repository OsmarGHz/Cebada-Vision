# Guion del video demostrativo (máx. 5 min) — CebadaVision

Formato: grabación de pantalla de la app con voz en off + 3 diapositivas simples (problema, método,
resultados). Quien habla: un integrante por bloque; Cervantes maneja la app en vivo. Cifras tomadas
de `data/processed/modelo_final.json` (modelo congelado, v1.0.0).

| Tiempo | Pantalla | Texto (voz) |
|---|---|---|
| 0:00–0:25 | Diapositiva 1: mapa de las 197 parcelas con los tres estados | "FIRA nos dio 197 parcelas de cebada de temporal en Hidalgo, Tlaxcala y Puebla, del ciclo abril–octubre 2025. De 138 conocemos cuánto cosecharon; de 59 no. Nuestro reto: estimar esas 59 y convertir el modelo en una herramienta que sirva al productor y al analista de crédito." |
| 0:25–1:15 | Diapositiva 2: pipeline (datos → variables → validación → ensamble) | "Para cada parcela resumimos la curva completa de los índices de Planet y Sentinel-2: cuándo emergió, cuánto verdor alcanzó, cuánto duró verde y qué tan rápido se secó. Sumamos lluvia, temperaturas, elevación, pendiente y, lo más importante, la ubicación: qué cosecharon las ocho parcelas vecinas. Validamos todo con cinco particiones estratificadas por estado, repetidas diez veces, y nunca dejamos que el rendimiento de una parcela entre en sus propias variables." |
| 1:15–2:15 | Diapositiva 3: tabla de resultados (media 0.851 → kNN 0.501 → final 0.491; por estado) | "Predecir la media regional se equivoca 0.85 toneladas por hectárea. Nuestro ensamble de LightGBM y Random Forest baja el error a 0.49, con R² de 0.66. El hallazgo clave: la ubicación explica dos tercios de la variación; los índices, el clima y el relieve afinan. Las tres preguntas guía: el índice más importante es el EVI de Planet, por su señal en mayo–junio; la variable climática con mayor peso es la precipitación del ciclo; y la mejor combinación es ubicación, relieve, clima y fenología de Planet." |
| 2:15–2:45 | App · Resumen (modo Productor) | "Esta es CebadaVision. Arriba se consulta cualquier parcela por su ID. El mapa colorea las 197 por rendimiento estimado y los indicadores resumen por estado." |
| 2:45–3:30 | App · Ficha de una parcela de predicción (ej. AGC_003) | "La ficha da la estimación con su rango más probable, el semáforo bajo/medio/alto, y la nota en lenguaje sencillo: de dónde sale el número, qué lo subió y qué lo bajó. Abajo, la curva de verdor del ciclo y las condiciones de la parcela comparadas con su estado." |
| 3:30–4:00 | App · Simulador | "El simulador ejecuta el modelo en el navegador: mueve lluvia, temperatura o vigor y ve cómo cambia la estimación. También acepta un CSV con muchas parcelas y devuelve sus predicciones." |
| 4:00–4:25 | App · Modelo (modo Analista) | "Para el analista: métricas, observado contra predicho, error por estado, importancia de variables y las respuestas a las preguntas guía con su evidencia. Desde aquí se descarga el CSV de las 59 predicciones que enviamos a FIRA." |
| 4:25–4:55 | App · Acerca de | "¿Por qué importa? Una estimación objetiva por parcela, con error conocido, permite dimensionar el crédito de avío a lo que la parcela puede pagar, evaluar a productores sin historial y detectar desviaciones a tiempo para seguros. Limitaciones: dato de rendimiento comercial, clima a 5 km y un solo ciclo; lo declaramos en la app." |
| 4:55–5:00 | Cierre | "CebadaVision: ver la cosecha antes de que llegue. Gracias." |

## Checklist de grabación

- [ ] App con datos del modelo final (`npm run validate` en verde, sin `es_mock`).
- [ ] Probar el enlace público en incógnito antes de grabar.
- [ ] Cifras del guion = `modelo_final.json` (RMSE 0.491, MAE 0.336, R² 0.664).
- [ ] Duración < 5:00. Exportar a 1080p. Subir a YouTube (no listado) o Drive con acceso por enlace.
- [ ] Probar que el enlace del video abre sin iniciar sesión.
