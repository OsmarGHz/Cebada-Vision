# Qué se entrega y cómo — Reto AgroCebada FIRA 2026

Alcance de esta revisión y cotejo de los nueve adjuntos originales: `REVISION_DOCUMENTAL_2026-10-18.md`.

Fuentes cotejadas: bases, guía de registro (pp. 2–4), acuerdos por correo del 21 de septiembre,
sesión del 9 de octubre, recordatorio del 14 de octubre y correo del **16 de octubre**
("Importante: envío de propuestas"). La guía y el recordatorio confirman cuatro cuartillas
para anexos; el último correo precisa el envío obligatorio de la documentación completa.

**Fecha límite: lunes 19 de octubre de 2026, 23:59 h.** Después no reciben nada.

## 1. Lo que cambió con el correo del 16 de octubre

La plataforma ha fallado al guardar textos largos. Por eso FIRA pide **dos cosas a la vez**:

1. Intentar subir todo a la plataforma (completar todos los apartados).
2. **Obligatorio para todos**, hayan subido o no a la plataforma: mandar un correo a
   **innovacion@fira.gob.mx** con cinco cosas. Si la plataforma falla, **el correo cuenta como
   entrega válida** siempre que llegue antes del 19 oct 23:59 con todo completo.

## 2. Los cinco elementos del correo (y dónde están)

| # | Qué pide FIRA | Archivo nuestro | Estado |
|---|---|---|---|
| 1 | **Informe en PDF**, con la estructura y límites de palabras de la plataforma (Introducción, Justificación, Objetivos, Metodología, Resultados y discusión, Inclusión financiera, Conclusiones) | `reports/entrega/01_Informe_CebadaVision.docx` → exportar a PDF | Revisado en esta rama; pendiente de aprobación |
| 2 | **Bibliografía en PDF aparte** | `reports/entrega/02_Bibliografia_CebadaVision.docx` → PDF | Falta integrar prompts reales, propósito y herramienta; aprobar el PDF |
| 3 | **Anexos en PDF aparte** (máx. 4 cuartillas: tabla de 59 predicciones, aportaciones por integrante, enlaces) | `reports/entrega/03_Anexos_CebadaVision.docx` → PDF | Faltan URLs verificadas y aprobación de aportaciones |
| 4 | **Enlace a la aplicación**, verificado que abre sin permisos | URL pública de `agrocebada-pagina` (ver `DESPLIEGUE_APP.md`) | **Falta desplegar** |
| 5 | **CSV con las 59 estimaciones**, en el formato que indicaron | `reports/entrega/CebadaVision_prediccion.csv` | Copia idéntica del original; cotejar encabezados e IDs con la plantilla oficial antes de entregar |

También conviene adjuntar (correos del 21 de septiembre y 14 de octubre: enlaces al código y
repositorios son complementarios): liga al repo `https://github.com/OsmarGHz/Cebada-Vision` y al de la app, o un
zip del código. Y la liga del **video de máximo 5 minutos**, que las bases piden como parte de la
entrega de la aplicación (puede ir en el mismo correo y en los anexos).

## 3. ¿Cómo se entrega "la página"?

Además del código fuente y las instrucciones de ejecución, se entrega **un enlace público** que el jurado
abra desde cualquier navegador, sin usuario ni contraseña. Eso implica:

1. Desplegar `agrocebada-pagina` en un hosting (Netlify, Vercel, GitHub Pages o un VPS propio).
   Instrucciones en `DESPLIEGUE_APP.md`.
2. Probar el enlace en una ventana de incógnito y desde un celular.
3. Pegar la URL en: el campo "Enlaces" de la plataforma, el correo a FIRA y el anexo A3
   (`python src/generar_anexos.py "URL_APP" "URL_VIDEO"` regenera `reports/anexos_final.md`;
   luego volver a generar el docx de anexos).
4. Como recomendación del equipo, mantenerla accesible al menos hasta el 20 de noviembre
   (premiación). Los originales exigen acceso para el jurado, sin fijar ese plazo de alojamiento.

El video: subirlo a YouTube (no listado) o Google Drive con acceso "cualquiera con el enlace", y
probar también en incógnito.

## 4. Plataforma (si deja)

- Un campo por sección; cada campo tiene **contador de palabras con tope duro**. Pegar desde
  `reports/reporte_tecnico.md` (sin los encabezados ni la nota entre corchetes).
- Bibliografía y Anexos se suben como PDF. Verificar que el nombre del archivo quede en azul
  (significa que sí se cargó).
- El campo Enlace admite app, interfaz, dashboard o video de hasta cinco minutos (guía, p. 4).
  El correo del 16 de octubre exige además acceso a la aplicación, herramienta o dashboard;
  usar allí la URL de la app y añadir el video como complemento.
- Dar clic en **Guardar** en cada apartado; la plataforma **no deja publicar si falta algún campo**.
- Revisar antes de **Publicar**: después la plataforma ya no permite cambios (guía, p. 2).
- Solo el capitán tiene acceso.

## 5. Checklist final (orden sugerido)

- [ ] Cervantes despliega la app y comparte la URL.
- [ ] Grabar y subir el video con `reports/guion_video.md`.
- [ ] Cada integrante aprueba su fila en `reports/anexos.md` e integra en `reports/entrega/bibliografia.md` sus prompts reales, propósito y herramienta. Sincronizar Bibliografía en `reports/reporte_tecnico.md` y regenerar su Word/PDF. No reconstruir ni inventar registros.
- [ ] `python src/generar_anexos.py "URL_APP" "URL_VIDEO"` → regenerar `03_Anexos_CebadaVision.docx` (`node src/md2docx.js reports/anexos_final.md reports/entrega/03_Anexos_CebadaVision.docx`) → PDF. Sincronizar también `reports/entrega/anexos.md` y comprobar el límite de cuatro cuartillas tras incorporar enlaces y aprobar aportaciones.
- [ ] Abrir los tres .docx en Word, revisar, **Guardar como PDF**.
- [ ] Verificar en la copia `CebadaVision_prediccion.csv` las 59 filas, cuatro decimales, encabezados e IDs contra la plantilla oficial. Conservar intactos ambos CSV originales.
- [ ] Subir todo a la plataforma (intentar; si falla, no pasa nada).
- [ ] **Correo a innovacion@fira.gob.mx** con: Informe.pdf, Bibliografia.pdf, Anexos.pdf, CSV, URL de la app, URL del video, liga o zip del código. Asunto sugerido: "Entrega final – Equipo CebadaVision – Reto AgroCebada 2026".
- [ ] Guardar copia del correo enviado (captura) como respaldo.

## 6. Qué se evalúa (para no olvidar nada que dé puntos)

- 70 % desempeño predictivo y justificación técnica (RMSE, MAE y R²; el documento de preguntas adicionales no establece una jerarquía entre ellas) → informe + CSV.
- 30 % aplicación o interfaz web funcional → enlace + video.
- Bonus: las tres preguntas guía respondidas y justificadas → están en Resultados y en la app.
- Descalifica: información falsa o no propia, no entregar documentación, no presentarse ante el
  jurado, incumplir las bases.
