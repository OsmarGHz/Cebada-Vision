# Revisión documental de CebadaVision — 18 de octubre de 2026

Propuesta para revisión del equipo, preparada desde `main` en
`bdc4ca2cd64b21972397517dafcbe9b90c5c4c6b`. Corrige la interpretación del modelo y el alcance
de la aplicación. No modifica código de modelación, datos procesados ni las 59 predicciones;
no acredita que la entrega a FIRA esté completa.

## Fuentes y alcance del cotejo

- Se revisaron `src/features.py`, `src/modelar.py`, `src/modelo_final.py`,
  `src/exportar_app.py`, `reports/experimentos.csv` y `data/processed/modelo_final.json`,
  junto con las salidas de predicción guardadas. No se reentrenó el modelo ni se reprodujo
  el banco completo de experimentos.
- Se consultaron las [bases oficiales de FIRA](https://www.fira.gob.mx/Nd/Reto%20Agrocebada%20Bases.pdf),
  también presentes en el repositorio. Las páginas 5–6 establecen las secciones y extensiones;
  la página 7 pide declarar el uso de IA y anexar los prompts.
- Se revisaron las notas de sesiones y las guías de entrega del repositorio. El límite posterior
  de cuatro cuartillas para anexos consta en esas notas y en la conversación de revisión;
  el PDF de bases aún dice dos. Los anexos actuales ocupan dos páginas.
- La descripción de pesaje en báscula, sin ajustes por humedad, impurezas o mermas, se incorpora
  conforme a la aclaración de FIRA transmitida en la revisión y confirmada en la solicitud del
  capitán. Los resúmenes históricos que decían «sin medición instrumental» se señalan como
  superados; no se borró la historia de las sesiones.
- **Pendiente de cotejo directo:** `Revision_CebadaVision_Propuestas_2026-10-18.md`, los
  lineamientos y aclaraciones adjuntos a la conversación anterior, los correos del 14 y 16 de
  octubre y la plantilla original de predicciones. La conversación pudo consultarse, pero sus
  archivos adjuntos no estaban disponibles en este entorno. No se presenta esta revisión como
  una comparación literal de esos originales ni se atribuyen a ellos citas o páginas nuevas.
- Se consultó `public/data/modelo.json` del repositorio público de la aplicación
  [David54s/agrocebada-pagina](https://github.com/David54s/agrocebada-pagina), sin modificarlo.
  No se verificó un despliegue público ni se repitieron las pruebas de la aplicación.

## Correcciones y evidencia técnica

| Tema | Redacción e interpretación propuestas | Evidencia |
|---|---|---|
| Rendimiento observado | Pesaje en báscula de la cosecha de cada parcela; sin ajustes por humedad, impurezas o mermas. El redondeo no demuestra ausencia de medición. | Aclaración transmitida por el capitán; original pendiente de cotejo. |
| Ensamble y simulador | Mapa y fichas consultan predicciones precalculadas del ensamble. El simulador ejecuta Ridge sobre 11 variables. | `preparar`, `predecir` y ajuste de `sur` en `src/modelo_final.py`; exportador. |
| Discrepancia de Ridge | 0.3161 t/ha es RMSE de ajuste frente al ensamble sobre las mismas 197 parcelas; no es error independiente contra rendimientos reales ni efecto causal. | Ajuste y evaluación de `sur` sobre `todo`; `simulador.rmse` del JSON. |
| Incertidumbre | ±1.2816 × RMSE ≈ ±0.63 t/ha es un margen orientativo; cobertura del 80 % sin calibración ni verificación empírica. | `Z80`, cálculo de `margen`, `pred_lo` y `pred_hi` en el código. |
| Ventaja frente a kNN | 0.491 frente a 0.501: diferencia redondeada de 0.010 t/ha, sin superioridad estadística demostrada. | Banco: kNN 0.5006065357; JSON: ensamble 0.4913. |
| Desempeño territorial | RMSE/R²: Hidalgo 0.357/0.784 (n=36), Puebla 0.578/0.007 (n=71), Tlaxcala 0.375/−0.026 (n=31). | Métricas recalculadas desde `prediccion_cv`, promedio de predicciones fuera de fold; coinciden con el JSON al redondear. |
| Anticipación y ciclos | Análisis retrospectivo con observaciones hasta noviembre de 2025. Alertas precosecha y actualización por ciclo requieren fecha de corte y validación temporal y operativa. | Ventanas en `features.py` y un solo ciclo con rendimiento conocido. |

Además, se aclara que los cinco folds usan aproximadamente 80/20 por partición, que el umbral
de 0.03 t/ha es orientativo, que la importancia por permutación se calcula sobre entrenamiento y
que la ablación del ensamble usa tres repeticiones. El informe y su copia de entrega contienen
las mismas siete secciones; el guion, README, guías y anexos reflejan las mismas reservas.

## Verificaciones realizadas

- 28 archivos de código, datos, experimentos, predicciones originales y bibliografía conservan
  exactamente los bytes de la base revisada.
- Los dos CSV originales y la nueva copia `entrega/CebadaVision_prediccion.csv` son idénticos:
  59 filas, 59 IDs únicos, cuatro decimales, mismos encabezados, orden y valores.
- SHA-256 de los tres CSV:
  `16f532445d5c1e0930bf0e323908e08445b8a15c12ff261b771718ed83d28ae9`.
- Los 59 pares ID/rendimiento coinciden con las tablas Markdown, Word y PDF de anexos, con
  `predicciones_197.csv` y con los IDs del subconjunto de predicción de `features_parcela.csv`.
  Esto verifica consistencia interna; el cotejo con la plantilla original de FIRA sigue pendiente.
- La plantilla de anexos reproduce el Markdown final usando las predicciones originales y
  los marcadores de enlaces pendientes.
- El texto del Word y del PDF del informe coincide con su fuente Markdown, excluyendo las
  marcas de formato y las notas de extensión. Informe: 6 páginas; anexos: 2 páginas.
  Se revisaron visualmente todas las páginas. La bibliografía no se modificó.
- Se regeneraron Word y PDF mediante el conversor documental existente y LibreOffice.
  En el Word de anexos se ajustó la tabla de aportaciones y se inició A2 en una página nueva
  para evitar filas partidas. Estos ajustes de formato deben revisarse al regenerarlo.
- `git diff --check` sin errores. No se ejecutaron entrenamientos, despliegues ni envíos.

### Conteos por sección

Se excluyen encabezados de sección, notas de extensión, marcas Markdown y numeración de listas;
se incluyen los rótulos internos. El segundo conteo separa también guiones, barras y símbolos,
manteniendo los decimales. Ninguno sustituye el contador de Word o de la plataforma FIRA.

| Sección | Por espacios | Léxico | Máximo |
|---|---:|---:|---:|
| Introducción | 519 | 525 | 550 |
| Justificación | 157 | 157 | 200 |
| Objetivos | 189 | 192 | 200 |
| Metodología | 662 | 675 | 700 |
| Resultados y discusión | 758 | 771 | 800 |
| Inclusión financiera | 270 | 272 | 300 |
| Conclusiones | 344 | 348 | 400 |

Introducción y Metodología también conservan los mínimos de 400 y 600 palabras.

## Pendientes antes de entregar

1. Cotejar los documentos originales de FIRA y el archivo de propuestas mencionado arriba.
2. Confirmar el nombre de equipo inscrito y el formato `nombre_del_equipo_prediccion.csv`
   frente al recordatorio original; la copia propuesta usa `CebadaVision_prediccion.csv`.
   No se cambiaron encabezados ni se sustituyó el archivo fuente.
3. Incorporar herramientas, usos y prompts reales de cada integrante; revisar y aprobar las
   aportaciones. A4 conserva el pendiente explícito y no inventa registros de uso.
4. Incorporar únicamente URLs verificadas de aplicación y video; aún no se proporcionaron.
5. Revisar por separado las etiquetas y referencias de la app: el JSON y el generador conservan
   «intervalo al 80 %» y kNN 0.506, mientras el banco documenta 0.501. Este PR corrige la
   documentación y deja identificada esa discrepancia; no cambia datos ni funcionamiento.
6. Revalidar conteos en la plataforma y extensión de anexos después de incorporar prompts y
   enlaces. Aprobar el contenido, regenerar los formatos afectados y realizar la entrega.

La revisión queda propuesta en una rama independiente. La fusión, el despliegue y el correo
quedan fuera de esta intervención.
