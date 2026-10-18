# Qué se entrega y cómo — Reto AgroCebada FIRA 2026

Fuentes: `Reto Agrocebada Bases.pdf` (sección de entregables), sesiones de dudas (27 sep y 9 oct)
y el correo de FIRA del **16 de octubre** ("Importante: envío de propuestas"). El correo manda
sobre lo demás porque es lo más reciente.

**Fecha límite: domingo 19 de octubre de 2026, 23:59 h.** Después no reciben nada.

## 1. Lo que cambió con el correo del 16 de octubre

La plataforma ha fallado al guardar textos largos. Por eso FIRA pide **dos cosas a la vez**:

1. Intentar subir todo a la plataforma (completar todos los apartados).
2. **Obligatorio para todos**, hayan subido o no a la plataforma: mandar un correo a
   **innovacion@fira.gob.mx** con cinco cosas. Si la plataforma falla, **el correo cuenta como
   entrega válida** siempre que llegue antes del 19 oct 23:59 con todo completo.

## 2. Los cinco archivos del correo (y dónde están)

| # | Qué pide FIRA | Archivo nuestro | Estado |
|---|---|---|---|
| 1 | **Informe en PDF**, con la estructura y límites de palabras de la plataforma (Introducción, Justificación, Objetivos, Metodología, Resultados y discusión, Inclusión financiera, Conclusiones) | `reports/entrega/01_Informe_CebadaVision.docx` → exportar a PDF | Listo; revisar y exportar |
| 2 | **Bibliografía en PDF aparte** | `reports/entrega/02_Bibliografia_CebadaVision.docx` → PDF | Listo |
| 3 | **Anexos en PDF aparte** (máx. 4 cuartillas: tabla de 59 predicciones, aportaciones por integrante, enlaces) | `reports/entrega/03_Anexos_CebadaVision.docx` → PDF | Falta: URL de la app y del video, y que cada quien apruebe su fila |
| 4 | **Enlace a la aplicación**, verificado que abre sin permisos | URL pública de `agrocebada-pagina` (ver `DESPLIEGUE_APP.md`) | **Falta desplegar** |
| 5 | **CSV con las 59 estimaciones**, en el formato que indicaron | `reports/entrega/04_predicciones_59_CebadaVision.csv` | Listo; si la plantilla de FIRA usa otros encabezados, renombrar columnas |

También conviene adjuntar (lo dijeron en la sesión del 27 sep: el código puede ir por correo, GitHub
no es obligatorio): liga al repo `https://github.com/OsmarGHz/Cebada-Vision` y al de la app, o un
zip del código. Y la liga del **video de máximo 5 minutos**, que las bases piden como parte de la
entrega de la aplicación (puede ir en el mismo correo y en los anexos).

## 3. ¿Cómo se entrega "la página"?

No se entrega el código ni un zip de la página: se entrega **un enlace público** que el jurado
abra desde cualquier navegador, sin usuario ni contraseña. Eso implica:

1. Desplegar `agrocebada-pagina` en un hosting (Netlify, Vercel, GitHub Pages o un VPS propio).
   Instrucciones en `DESPLIEGUE_APP.md`.
2. Probar el enlace en una ventana de incógnito y desde un celular.
3. Pegar la URL en: el campo "Enlaces" de la plataforma, el correo a FIRA y el anexo A4
   (`python src/generar_anexos.py "URL_APP" "URL_VIDEO"` regenera `reports/anexos_final.md`;
   luego volver a generar el docx de anexos).
4. Dejar la página en línea **al menos hasta el 20 de noviembre** (premiación). Si somos
   finalistas, la usan en la presentación del 10 nov.

El video: subirlo a YouTube (no listado) o Google Drive con acceso "cualquiera con el enlace", y
probar también en incógnito.

## 4. Plataforma (si deja)

- Un campo por sección; cada campo tiene **contador de palabras con tope duro**. Pegar desde
  `reports/reporte_tecnico.md` (sin los encabezados ni la nota entre corchetes).
- Bibliografía y Anexos se suben como PDF. Verificar que el nombre del archivo quede en azul
  (significa que sí se cargó).
- Un solo campo de enlace: poner la URL de la app. El video va en anexos y en el correo.
- Dar clic en **Guardar** en cada apartado; la plataforma **no deja publicar si falta algún campo**.
- Solo el capitán tiene acceso.

## 5. Checklist final (orden sugerido)

- [ ] Cervantes despliega la app y comparte la URL (sábado 18).
- [ ] Grabar y subir el video con `reports/guion_video.md` (sábado 18).
- [ ] Cada integrante aprueba su fila en `reports/anexos.md`.
- [ ] `python src/generar_anexos.py "URL_APP" "URL_VIDEO"` → regenerar `03_Anexos_CebadaVision.docx` (`node src/md2docx.js reports/anexos_final.md reports/entrega/03_Anexos_CebadaVision.docx`) → PDF.
- [ ] Abrir los tres .docx en Word, revisar, **Guardar como PDF**.
- [ ] Verificar que el CSV tenga 59 filas, 4 decimales y los encabezados de la plantilla de FIRA.
- [ ] Subir todo a la plataforma (intentar; si falla, no pasa nada).
- [ ] **Correo a innovacion@fira.gob.mx** con: Informe.pdf, Bibliografia.pdf, Anexos.pdf, CSV, URL de la app, URL del video, liga o zip del código. Asunto sugerido: "Entrega final – Equipo CebadaVision – Reto AgroCebada 2026".
- [ ] Guardar copia del correo enviado (captura) como respaldo.

## 6. Qué se evalúa (para no olvidar nada que dé puntos)

- 70 % desempeño predictivo y justificación técnica (RMSE primero; MAE y R² después) → informe + CSV.
- 30 % aplicación o interfaz web funcional → enlace + video.
- Bonus: las tres preguntas guía respondidas y justificadas → están en Resultados y en la app.
- Descalifica: información falsa o no propia, no entregar documentación, no presentarse ante el
  jurado, incumplir las bases.
