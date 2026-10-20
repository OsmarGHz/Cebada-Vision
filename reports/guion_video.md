# Guion del video demostrativo (máx. 5 min) — CebadaVision

Formato: grabación de pantalla de la app con voz en off + 3 diapositivas simples (problema, método,
resultados). Asignar las voces y la captura de pantalla según disponibilidad confirmada; puede narrar
un integrante o repartirse por bloques. Cifras tomadas
de `data/processed/modelo_final.json` (modelo congelado, v1.0.0) y del banco
`reports/experimentos.csv` para el kNN (0.501; el JSON de modelación conserva 0.506, pendiente de conciliación).

| Tiempo | Pantalla | Texto (voz) |
|---|---|---|
| 0:00–0:25 | Diapositiva 1: mapa de las 197 parcelas con los tres estados | "FIRA nos dio 197 parcelas de cebada de temporal en Hidalgo, Tlaxcala y Puebla, del ciclo 2025. De 138 conocemos cuánto cosecharon; de 59 no. Nuestro reto: estimar esas 59 y convertir el modelo en una herramienta que sirva al productor y al analista de crédito." |
| 0:25–1:10 | Diapositiva 2: pipeline (datos → variables → validación → ensamble) | "El modelo final usa índices de Planet; Sentinel-2 se evaluó en experimentos. Por parcela resumimos la curva completa de los índices: cuándo emergió, cuánto verdor alcanzó, cuánto duró verde y qué tan rápido se secó. Sumamos lluvia, temperaturas, elevación, pendiente y, lo más importante, la ubicación: qué cosecharon las ocho parcelas vecinas. Validamos todo con cinco particiones estratificadas por estado, repetidas diez veces, y nunca dejamos que el rendimiento de una parcela entre en sus propias variables." |
| 1:10–2:10 | Diapositiva 3: tabla de resultados (media 0.851 → kNN 0.501 → final 0.491; por estado) | "Predecir la media regional se equivoca 0.85 toneladas por hectárea. Nuestro ensamble de LightGBM y Random Forest baja el error a 0.49, con R² de 0.66. La ventaja frente al kNN de 0.501 es pequeña, sin superioridad estadística demostrada. El R² es 0.784 en Hidalgo, pero cercano a cero en Puebla y Tlaxcala. Las tres preguntas guía: el índice más importante es el EVI de Planet, por su señal en mayo–junio; en clima, destacó la anomalía de lluvia al evaluar cada variable por separado, y la temperatura mínima por permutación dentro del ensamble; y la mejor combinación es ubicación, relieve, clima y fenología de Planet." |
| 2:10–2:40 | App · Resumen (modo Productor) | "Esta es CebadaVision. Arriba se consulta cualquier parcela por su ID. El mapa colorea las 197 por rendimiento estimado y los indicadores resumen por estado." |
| 2:40–3:25 | App · Ficha de una parcela de predicción (ej. AGC_003) | "La ficha muestra la estimación precalculada del ensamble, un margen orientativo de ±0.63 toneladas por hectárea sin cobertura del 80 % calibrada, categorías de rendimiento con umbrales fijos y una explicación sencilla. Abajo, la curva de verdor del ciclo y las condiciones de la parcela comparadas con su estado." |
| 3:25–3:55 | App · Simulador | "El simulador ejecuta una regresión Ridge sustituta. Su discrepancia de ajuste frente al ensamble es 0.3161 toneladas por hectárea; explorar sus variables no demuestra efectos causales ni reproduce las predicciones oficiales." |
| 3:55–4:20 | App · Modelo (modo Analista) | "Para el analista: métricas, observado contra predicho, error por estado, importancia de variables y las respuestas a las preguntas guía con su evidencia. Desde aquí se descarga el CSV de las 59 predicciones preparado para FIRA." |
| 4:20–4:45 | App · Acerca de | "¿Por qué importa? La estimación podría complementar la evaluación financiera tras validación operativa. Usamos pesaje en báscula sin ajustes por humedad, impurezas o mermas, clima a 5 km y un solo ciclo, con observaciones hasta noviembre de 2025. El análisis es retrospectivo; las alertas precosecha y la actualización por ciclo requieren validación adicional." |
| 4:45–4:50 | Cierre | "CebadaVision: evidencia para comprender el rendimiento. Gracias." |

## Checklist de grabación

- [ ] Confirmar quién narra y quién captura pantalla; los audios pueden grabarse por separado.
- [ ] App con datos del modelo final (`npm run validate` en verde, sin `es_mock`).
- [ ] Probar el enlace público en incógnito antes de grabar.
- [ ] Cifras del guion = `modelo_final.json` (RMSE 0.491, MAE 0.336, R² 0.664).
- [ ] Revisar que las etiquetas de incertidumbre y las cifras de la app coincidan con el informe; ver pendientes de la revisión documental.
- [ ] Ensayar con las voces reales: objetivo 4:50; duración final < 5:00. Exportar a 1080p. Subir a YouTube (no listado) o Drive con acceso por enlace.
- [ ] Probar que el enlace del video abre sin iniciar sesión.
