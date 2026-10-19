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
- Se cotejaron directamente los **nueve PDF originales** proporcionados por el capitán.
  Se conservaron fuera del repositorio público; no se publicaron los correos ni sus adjuntos.
  Las referencias siguientes corresponden a la paginación de esos PDF.

| Original | Evidencia utilizada |
|---|---|
| *Reto Agrocebada Bases (2).pdf* | pp. 5–7: informe, aplicación, documentación e IA. Es idéntico en bytes al PDF de bases ya versionado. |
| *Lineamientos y Guía de Registro de Proyectos_.pdf* | p. 2: guardado, publicación y cierre; pp. 3–4: máximos por sección; p. 4: prompts, propósito y herramienta en **Bibliografía**, anexos de hasta cuatro cuartillas y tabla obligatoria. |
| *Preguntas y respuestas adicionales .pdf* | p. 1, preguntas 1–4: rendimiento de grano en t/ha, evaluación por parcela sin ponderación por área y pesaje en báscula sin ajustes; p. 2, preguntas 5–7: partición 138/59, fecha de corte y alcance del error. |
| *Segunda_Sesion_Preguntas_Reto.pdf* | Sesión del 9-oct; p. 1, preguntas 1–10: temporal, procedencia, cuatro decimales, muestreo aleatorio estratificado y datos faltantes; p. 2: polígonos, explicación en la app y variedades sin identificación por parcela. |
| *Ecuaciones_indices_AgroCebada_FIRA_2026.pdf* | pp. 1–2: ecuaciones por sensor, incluidos EVI, NDVI, MSAVI y LAI2 de Planet. El código usa índices suministrados; no se recalcularon desde bandas crudas. |
| *Gmail_Acuerdos_de_la_1ra_sesión_de_preguntas_–_Reto_AgroCebada_FIRA.pdf* | Correo del 21-sep, p. 1: temporal, ecuaciones adjuntas y formato `nombre_del_equipo_prediccion.csv`; enlaces al código como complemento. |
| *Gmail_Recordatorio_de_fecha_límite_de_entrega_–_Reto_AgroCebada.pdf* | Correo del 14-oct, p. 1: cuatro cuartillas, exactamente 59 parcelas, IDs originales, nombre del CSV y cierre el 19-oct a las 23:59. |
| *Gmail_Importante_envío_de_propuestas_–_Reto_AgroCebada_FIRA_2026.pdf* | Correo del 16-oct, p. 1: intentar plataforma y enviar documentación completa por correo en todos los casos, incluidos tres PDF separados, CSV y enlace accesible a la aplicación, herramienta o dashboard. |
| *BETA1-Documento Cebada-Vision.pdf* | pp. 1–4: borrador inicial y esquema de trabajo. Sus algoritmos y validación temporal tentativos no sustituyen la implementación final comprobada. |

La guía y el recordatorio precisan el límite de cuatro cuartillas, frente a las dos de las bases.
La aclaración de báscula se comprobó directamente en preguntas adicionales (p. 1, pregunta 3);
la procedencia por comercializadora o productor no implica ausencia de medición. Los resúmenes
históricos se conservan con una nota que identifica las precisiones vigentes.

FIRA no impone una fecha de corte al conjunto de datos (preguntas adicionales, p. 2, pregunta 6).
Usar el ciclo completo está permitido; afirmar anticipación precosecha requiere indicar cuándo
se emitiría la predicción y qué información estaría disponible entonces.

Posteriormente se recibieron y cotejaron dos archivos adicionales:

- `Revision_CebadaVision_Propuestas_2026-10-18.md`: se contrastaron los puntos C1–C8 y las
  propuestas de anexos contra esta rama. SHA-256:
  `c80d949a1360741a57b12de8086e35b2930d59c676874cff9f431df0cce455f9`.
- `ID_area_rendimiento_70_30_Reto_AgroCebada.csv`, del dataset original: fuente para comprobar
  la pertenencia de las 59 parcelas a evaluación. SHA-256:
  `ec07b7ede0ae692109d91b3e941b1a353fe7f89410507db9bfbe6d7c112590ef`.
  Contiene 197 IDs únicos, 138 filas `ENTRENAMIENTO` con rendimiento y 59 `PREDICCION`
  con rendimiento vacío. Sus cuatro campos son `ID_POLIGONO`, `AREA_HA`, `RENDIMIENTO_T_HA`
  y `CONJUNTO`; una coma final añade una columna vacía en todas las filas.

Este CSV es la tabla de entrada del modelo, no una plantilla de salida de 59 estimaciones.
Permite cerrar el cotejo de los IDs originales, sin trasladar las 197 filas, la columna vacía ni
los rendimientos conocidos al archivo de entrega. Se conservan los encabezados actuales de la
salida: `EQUIPO,ID_POLIGONO,RENDIMIENTO_T_HA`. No se recibió una plantilla de salida distinta.
Ambos originales se consultaron sin modificarlos y no se incorporaron al repositorio público.

Se revisó también el código y los datos de la aplicación en
[`David54s/agrocebada-pagina`, commit `d77d4852`](https://github.com/David54s/agrocebada-pagina/tree/d77d4852f1b0ed7256428cbb22e188be68dcbbfd).
No se verificó un despliegue público ni se repitieron pruebas funcionales de la aplicación.

## Correcciones y evidencia técnica

| Tema | Redacción e interpretación propuestas | Evidencia |
|---|---|---|
| Rendimiento observado | Pesaje en báscula de la cosecha de cada parcela; sin ajustes por humedad, impurezas o mermas. El redondeo no demuestra ausencia de medición. | Preguntas y respuestas adicionales, p. 1, pregunta 3; segunda sesión, p. 1, preguntas 5–8. |
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

- 25 archivos de código, datos, experimentos y predicciones originales conservan
  exactamente los bytes de la base revisada.
- Los dos CSV originales y la nueva copia `entrega/CebadaVision_prediccion.csv` son idénticos:
  59 filas, 59 IDs únicos, cuatro decimales, mismos encabezados, orden y valores.
- SHA-256 de los tres CSV:
  `16f532445d5c1e0930bf0e323908e08445b8a15c12ff261b771718ed83d28ae9`.
- Los 59 pares ID/rendimiento coinciden con las tablas Markdown, Word y PDF de anexos, con
  `predicciones_197.csv` y con los IDs del subconjunto de predicción de `features_parcela.csv`.
  Los 59 pares también coinciden con `public/data/predicciones.csv` de la app en el commit
  revisado. Además, las 59 filas `PREDICCION` del CSV original del dataset coinciden exactamente
  con los IDs y el orden de los tres CSV de entrega: cero duplicados, faltantes o sobrantes.
- Los 197 IDs, áreas y etiquetas de conjunto de `features_parcela.csv` coinciden con el CSV
  original; también coinciden los 138 rendimientos observados y los 59 rendimientos vacíos.
  Este cotejo no revela los rendimientos reservados ni evalúa la precisión sobre esas 59 parcelas.
- La plantilla de anexos reproduce el Markdown final usando las predicciones originales y
  los marcadores de enlaces pendientes.
- El texto del Word y del PDF del informe coincide con su fuente Markdown, excluyendo las
  marcas de formato y las notas de extensión. Informe: 6 páginas; bibliografía: 2; anexos: 2.
  La bibliografía incorpora documentos técnicos de FIRA y el registro de IA pendiente.
  Se revisaron visualmente todas las páginas de los tres PDF regenerados.
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
| Metodología | 661 | 674 | 700 |
| Resultados y discusión | 758 | 771 | 800 |
| Inclusión financiera | 270 | 272 | 300 |
| Conclusiones | 344 | 348 | 400 |

Introducción y Metodología también conservan los mínimos de 400 y 600 palabras.

## Cotejo del archivo de propuestas recuperado

La redacción conserva el contenido de las correcciones C1–C8 sin exigir una sustitución literal:

| Propuesta | Aplicación en esta rama |
|---|---|
| C1: origen del rendimiento | Introducción, Justificación y Conclusiones corrigen a pesaje en báscula sin ajustes; las fuentes identifican comercializadoras y productores. |
| C2: aplicación | Introducción distingue las salidas precalculadas del ensamble y el simulador aproximado. |
| C3: margen | Metodología aclara la falta de calibración de la cobertura del 80 %. |
| C4: Ridge | Metodología precisa 11 variables y discrepancia 0.3161 t/ha frente al ensamble, sin validación independiente. |
| C5: incertidumbre | Resultados distingue desviación del RMSE entre repeticiones de la incertidumbre individual. |
| C6: kNN y estados | Resultados matiza 0.491 frente a 0.501 e incorpora R² y RMSE por estado; la discrepancia 0.506 de la app queda identificada. |
| C7: alcance financiero y temporal | Inclusión financiera condiciona anticipación, nuevos ciclos y uso operativo a validación adicional. |
| C8: cierre | Conclusiones mantiene las mismas reservas y distingue ensamble y Ridge. |

Se conserva la tabla de 59 predicciones y se marca la aprobación de aportaciones como pendiente;
la fila de Cervantes no acredita un despliegue verificado. No se inventan enlaces ni prompts.
La guía original resuelve la ubicación de la relación de IA en Bibliografía, con referencia en A4.
Los Word/PDF ya regenerados y sus conteos no cambian en este cotejo.

La propuesta recuperada dice que el repositorio es privado: esa nota quedó superada por el
cambio autorizado por el capitán y la consulta actual a GitHub, que confirma visibilidad pública.
Su nombre sugerido `cebadavision_prediccion.csv` se interpreta dentro del patrón oficial
`nombre_del_equipo_prediccion.csv`; la copia actual usa el nombre de equipo CebadaVision.
Las instrucciones de envío del archivo se registran como requisitos para el equipo y no se ejecutan.

## Discrepancias de la app que requieren una revisión separada

Referencias al commit revisado; este PR no modifica el segundo repositorio ni los JSON de datos:

- [Acerca, líneas 49–50](https://github.com/David54s/agrocebada-pagina/blob/d77d4852f1b0ed7256428cbb22e188be68dcbbfd/src/pages/Acerca.tsx#L49-L50):
  conserva «sin medición instrumental», contradicho por el original de FIRA.
- [Modelo JSON, línea 7](https://github.com/David54s/agrocebada-pagina/blob/d77d4852f1b0ed7256428cbb22e188be68dcbbfd/public/data/modelo.json#L7)
  y [PanelParcela, línea 40](https://github.com/David54s/agrocebada-pagina/blob/d77d4852f1b0ed7256428cbb22e188be68dcbbfd/src/components/PanelParcela.tsx#L40):
  la ficha muestra la etiqueta de intervalo al 80 %, cuya cobertura no está calibrada.
- [Simulador, línea 74](https://github.com/David54s/agrocebada-pagina/blob/d77d4852f1b0ed7256428cbb22e188be68dcbbfd/src/pages/Simulador.tsx#L74)
  y [líneas 159–160](https://github.com/David54s/agrocebada-pagina/blob/d77d4852f1b0ed7256428cbb22e188be68dcbbfd/src/pages/Simulador.tsx#L159-L160):
  aclarar que ejecuta Ridge sustituta y que 0.3161 es discrepancia de ajuste frente al ensamble;
  los valores ±RMSE no son intervalos calibrados. El cálculo lineal está en
  [`surrogate.ts`, líneas 25–27](https://github.com/David54s/agrocebada-pagina/blob/d77d4852f1b0ed7256428cbb22e188be68dcbbfd/src/model/surrogate.ts#L25-L27).
- [Acerca, línea 42](https://github.com/David54s/agrocebada-pagina/blob/d77d4852f1b0ed7256428cbb22e188be68dcbbfd/src/pages/Acerca.tsx#L42)
  y [Modelo JSON, línea 128](https://github.com/David54s/agrocebada-pagina/blob/d77d4852f1b0ed7256428cbb22e188be68dcbbfd/public/data/modelo.json#L128):
  kNN figura como 0.506; el banco revisado da 0.501. El generador del repositorio de modelación
  también conserva esa referencia y necesitaría sincronizarse en una corrección técnica posterior.
- [Modelo, línea 51](https://github.com/David54s/agrocebada-pagina/blob/d77d4852f1b0ed7256428cbb22e188be68dcbbfd/src/pages/Modelo.tsx#L51):
  el RMSE no equivale al error absoluto medio ni garantiza un rango ± por parcela.
- [Acerca, líneas 69–71](https://github.com/David54s/agrocebada-pagina/blob/d77d4852f1b0ed7256428cbb22e188be68dcbbfd/src/pages/Acerca.tsx#L69-L71):
  presentar la anticipación y la utilidad financiera como posibilidades sujetas a validación.
- [README, líneas 34–35](https://github.com/David54s/agrocebada-pagina/blob/d77d4852f1b0ed7256428cbb22e188be68dcbbfd/README.md#L34-L35):
  aún describe los datos como salida de Ridge provisional, aunque corresponden al ensamble final.

## Pendientes antes de entregar

1. Confirmar que el nombre inscrito del equipo es CebadaVision. La copia propuesta
   `CebadaVision_prediccion.csv` cumple el patrón confirmado por los correos originales;
   no se cambiaron encabezados ni se sustituyó el archivo fuente.
2. Incorporar en **Bibliografía** los prompts reales, su propósito y la herramienta empleada
   por cada integrante. A4 remite a ese registro; revisar y aprobar también las aportaciones.
3. Incorporar únicamente URLs verificadas de aplicación y video; aún no se proporcionaron.
4. Resolver las discrepancias de la app descritas arriba y comprobar su funcionamiento.
5. Revalidar los contadores de la plataforma, regenerar Word/PDF tras completar los pendientes
   y verificar las cuatro cuartillas de anexos. La guía advierte que **Publicar** impide cambios
   posteriores. El equipo debe aprobar el contenido y realizar la entrega completa.

La revisión queda propuesta en una rama independiente. La fusión, el despliegue y el correo
quedan fuera de esta intervención.
