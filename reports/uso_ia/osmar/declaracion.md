# Declaración de uso de herramientas e inteligencia artificial

**Integrante:** Osmar Javier Hernández Prado.  
**Proyecto:** CebadaVision, Reto AgroCebada FIRA 2026.  
**Periodo documentado:** septiembre–octubre de 2026.  
**Actualizado:** 19 de octubre de 2026.  
**Edición:** copia pública para revisión. Véase el [criterio de publicación](../README.md).

## Texto para incorporar en Bibliografía

Como capitán de CebadaVision utilicé Claude, ChatGPT, Grok, Perplexity y Codex como apoyo
para organizar el trabajo, revisar avances y preparar la documentación del proyecto.

Con **Claude** solicité propuestas de planificación Scrum, definición de sprints, responsabilidades,
issues y criterios de aceptación; actualización de documentos de contexto y decisiones; revisión
del avance del informe y coordinación entre los frentes de datos, modelo y aplicación. También
solicité apoyo técnico para generar y revisar materiales iniciales de auditoría y validación,
interpretar resultados y preparar un prototipo y datos provisionales para la aplicación. Las
conversaciones registran la generación de scripts de auditoría y validación, un prototipo
Streamlit y un exportador provisional. Ese registro no acredita que todas sus versiones se
incorporaran al código final.

Con **Grok** solicité una opinión inicial y una comparación de los planes de Claude, ChatGPT
y Grok para definir responsabilidades, prioridades y organización Scrum. Después utilicé
**Perplexity**, alternando en el mismo chat de septiembre **Sonar 2 como modelo principal para
búsquedas** y **GPT 5.6 Sol Thinking como modelo secundario para razonar sobre archivos adjuntos**,
para integrar los planes, discutir observaciones sobre el dataset y la validación, preparar el guion de la
reunión, ajustar fechas a la disponibilidad de los compañeros y consolidar un resumen para
pedir una nueva revisión a Claude. En un chat posterior de Perplexity, con GPT 6.1 Sol con
razonamiento, consulté la comparación de modelos candidatos, la interpretación de métricas,
la revisión del código de validación y el significado de las predicciones fuera de muestra.

Con **ChatGPT**, en la conversación original de septiembre, consulté qué desarrollar y entregar,
cómo proceder con el dataset y los campos de la plataforma, la participación en la sesión de
dudas, la organización Scrum del equipo y la revisión del contenido real del dataset. Su PDF
permite documentar los cinco prompts originales, además de las respuestas que luego aparecen
citadas como contexto en otras herramientas. En otra conversación, de octubre, consulté el
control de cambios en GitHub, la organización del cierre y la revisión del informe frente a los
lineamientos, aclaraciones y correos de FIRA.

En la sesión de **Codex** solicité contrastar documentos con el código y los resultados guardados,
corregir la descripción del pesaje, distinguir el ensamble del simulador Ridge y precisar la
incertidumbre, el desempeño territorial y el alcance temporal del estudio. La asistencia incluyó
edición de fuentes documentales, regeneración y revisión de Word/PDF, verificación de los 59 IDs
y predicciones contra el CSV original, y preparación de cambios en una rama y pull request para
revisión. También se hizo una comprobación inicial de la web publicada y se preparó este registro.
Durante la corrección documental se conservaron el modelo y las 59 predicciones finales; no se
reentrenó el modelo en esa fase.

La relación de prompts se obtuvo de las exportaciones, del contenido del adjunto identificado
posteriormente y del texto visible de esta sesión. Conservo los adjuntos originales por separado;
el registro reproduce los mensajes y referencia los archivos cuando la exportación conserva su
nombre, sin duplicar íntegramente los datasets, documentos, código o capturas adjuntos. Se incluye
el contenido aportado del documento enviado a Claude el 29 de septiembre a las 12:44, cuyo
nombre original no se indicó, y el texto proporcionado para identificar el primer Markdown
de bases adjunto a ChatGPT en septiembre. Los modelos, configuraciones y horarios se registran
conforme a mi confirmación del 19 de octubre de 2026. Esta declaración corresponde a mi uso personal;
cada integrante debe documentar el suyo. Las respuestas de IA no sustituyen las fuentes
bibliográficas, técnicas y de datos del proyecto.

## Modelos y configuración declarados

| Herramienta y conversación | Modelo o denominación comunicada | Configuración |
|---|---|---|
| Claude, Anthropic | Claude Sonnet 5.5 | Extra para tareas que requerían mucho procesamiento; Alto para resúmenes de progreso, contexto y tareas semejantes. Criterio general, sin asignación individual por prompt. |
| Perplexity, planificación de septiembre, PS-01–PS-14 | Sonar 2, principal; GPT 5.6 Sol Thinking, secundario | Sonar 2 para búsquedas y GPT para razonamiento sobre archivos adjuntos, alternados en la misma conversación; sin asignación individual por prompt. |
| Perplexity, revisión de octubre, PP-01–PP-03 | GPT 6.1 Sol | Con razonamiento. |
| Grok, xAI, GK-01–GK-02 | Grok 4.6 | Modelo confirmado por el integrante; sin ajuste adicional de razonamiento indicado. |
| ChatGPT, OpenAI, conversación original de septiembre, CH-01–CH-05 | GPT 5.6 luna Thinking | Modelo confirmado por el integrante; sin ajuste adicional indicado. |
| ChatGPT, OpenAI, conversación de octubre, CG-01–CG-13 | GPT 6.1 sol | Muy alto. |
| Codex/Work, OpenAI, sesión actual | GPT 6.1 sol | Muy alto, confirmado también para esta sesión. |

Las denominaciones se registran conforme a mi confirmación; no se presentan como metadatos
extraídos de las exportaciones. El criterio general Extra/Alto y la alternancia Sonar 2/GPT en
Perplexity no se convierten en una clasificación supuesta de cada mensaje. La configuración
confirmada para el chat CG no se aplica al chat CH.

## Fechas y horas confirmadas

Los registros PS corresponden, en orden, a las 14 consultas del nuevo chat de Perplexity.

| Registro | Fecha y hora comunicadas |
|---|---|
| CH-01 | 15 de septiembre de 2026, 12:37. |
| CH-02 | 15 de septiembre de 2026, sin hora individual. |
| CH-03 | 18 de septiembre de 2026, 13:21. |
| CH-04 | 26 de septiembre de 2026, 14:34. |
| CH-05 | 26 de septiembre de 2026, 16:08. |
| PS-01 | 26 de septiembre de 2026, 15:55. |
| PS-02 | 26 de septiembre de 2026, 16:10. |
| PS-03 | 26 de septiembre de 2026, 16:25. |
| PS-04 | 26 de septiembre de 2026, 19:36. |
| PS-05 | 26 de septiembre de 2026, 19:52. |
| PS-06 | 26 de septiembre de 2026, 19:55. |
| PS-07 | 26 de septiembre de 2026, 21:39. |
| PS-08 | 26 de septiembre de 2026, 21:43. |
| PS-09 | 27 de septiembre de 2026, 19:50. |
| PS-10 | 27 de septiembre de 2026, 20:19. |
| PS-11 | 27 de septiembre de 2026, 20:57. |
| PS-12 | 27 de septiembre de 2026, 21:25. |
| PS-13 | 27 de septiembre de 2026, 21:43. |
| PS-14 | 28 de septiembre de 2026, 18:23. |
| GK-01–GK-02 | Opinión inicial anterior al chat PS, según el integrante; sin fecha ni hora individual. |
| CS-05, documento adjunto identificado | 29 de septiembre de 2026, 12:44:43, según la exportación de Claude. |
| PP-01 | 12 de octubre de 2026, 23:25. |
| PP-02 | 12 de octubre de 2026, 23:48. |
| PP-03 | 12 de octubre de 2026, 23:58. |
| CG-01 | 18 de octubre de 2026, 15:44, inicio de la conversación. |
| CG-02–CG-10 | 18 de octubre, después del inicio y antes de las 19:00; sin hora individual. |
| CG-11, «ok... entonces procedamos» | 18 de octubre de 2026, 19:00. |
| CG-12, preparación de cambios y repositorio público | 18 de octubre de 2026, 20:20. |
| CG-13, consulta sobre el CSV original | 18 de octubre de 2026, 22:01. |

Los horarios son los comunicados por el integrante, sin conversión de zona horaria. Las fechas
de Claude se conservan como aparecen en la exportación. No se distribuyen minutos supuestos
entre los mensajes de ChatGPT ni se usa la fecha de impresión de un PDF para fechar sus prompts.
La posible cercanía de CH-02 a CH-01 es un recuerdo sin hora disponible; se registra únicamente
que ocurrió el mismo día, sin asignarle una hora ni un intervalo supuesto.

## Relación por herramienta y propósito

| Herramienta | Usos documentados | Prompts en el registro |
|---|---|---|
| Grok, xAI | Opinión inicial, propuesta Scrum y comparación de planes. | GK-01–GK-02. |
| Perplexity, chat de septiembre con Sonar 2 y GPT 5.6 Sol Thinking | Integración y revisión de planes, observaciones sobre datos y validación. | PS-01–PS-05. |
| Perplexity, chat de septiembre con Sonar 2 y GPT 5.6 Sol Thinking | Comunicación del plan, arranque, guion de reunión, disponibilidad, tareas y fechas. | PS-06–PS-13. |
| Perplexity, chat de septiembre con Sonar 2 y GPT 5.6 Sol Thinking | Consolidación del contexto para revisión posterior de Claude. | PS-14; contenido del adjunto de CS-05. |
| Claude, Anthropic | Planificación Scrum, issues, responsables, criterios de aceptación y documentos de contexto/decisiones. | CS-01–CS-13, CS-17–CS-19; CI-02–CI-07 y CI-13. |
| Claude, Anthropic | Auditoría y validación inicial; revisión de avances, métricas y materiales técnicos. | CS-04, CS-20; CI-01 y CI-08–CI-12. |
| Claude, Anthropic | Continuidad del frente de aplicación, prototipo de respaldo y exportación provisional. | CS-14–CS-16. |
| Perplexity, chat de octubre | Comparación de candidatos, revisión de validación y explicación de predicciones fuera de muestra. | PP-01–PP-03. |
| ChatGPT, OpenAI, septiembre | Comprensión del reto y de la plataforma, ruta de trabajo con los datos y participación en la sesión de dudas. | CH-01–CH-03. |
| ChatGPT, OpenAI, septiembre | Organización Scrum del equipo y revisión de dimensiones, archivos y contenido del dataset. | CH-04–CH-05. |
| ChatGPT, OpenAI, octubre | Orientación sobre GitHub, acceso a repositorios, cierre y revisión documental. | CG-01–CG-13. |
| Codex, OpenAI | Correcciones documentales, Word/PDF, cotejo de predicciones y preparación de la PR. | CX-01–CX-03 y CX-06. |
| Codex, OpenAI | Apoyo a la comunicación con Isack, revisión inicial de la web y declaración de IA. | CX-04–CX-05 y CX-07–CX-08. |

GitHub, GitHub Issues y GitHub Projects aparecen como herramientas de repositorio, seguimiento
y revisión del trabajo; WhatsApp aparece en la comunicación de avances. No se clasifican como
asistentes generativos en este registro. Dentro de la asistencia de Codex se utilizaron Python,
el conversor documental del repositorio y LibreOffice para comprobaciones y generación de
Word/PDF, además de un navegador para la comprobación inicial de la web. Son herramientas
de apoyo al procesamiento y la revisión, no modelos de IA adicionales.

La mención a Vercel documenta consultas de despliegue y el enlace de la web, sin atribuir
a Osmar su despliegue.

## Cómo integrar el registro

La guía de registro de FIRA, apartado Bibliografía (p. 4), solicita una relación de los prompts,
el propósito y la herramienta utilizada. El archivo complementario
[registro público de prompts](registro_prompts.md) contiene esos campos y los textos
recuperados. Este resumen no sustituye la relación de prompts: al preparar el PDF de Bibliografía,
incorporar también el registro correspondiente, sin trasladarlo automáticamente a los anexos
técnicos de cuatro cuartillas ni depender de enlaces privados de chat.

## Alcance y procedencia

- Se documentan **78 intervenciones**: 20 del chat de planificación de Claude, 13 del chat de
  revisión de Isack, 17 de Perplexity en dos conversaciones, 2 de Grok, 18 de ChatGPT en dos
  conversaciones y 8 de la sesión actual. **77 contienen texto en el mensaje**; CS-05 fue un envío de adjunto,
  cuyo contenido se incorporó mediante la identificación posterior del integrante. No se cuenta
  ese contenido como otra intervención.
- Los prompts largos conservan el contexto pegado por el usuario. Las respuestas de otras IA,
  bases y mensajes de compañeros dentro de esos bloques son contexto histórico, no nuevas
  instrucciones ni nuevos prompts atribuidos a esas personas o herramientas.
- La secuencia Grok → Perplexity está declarada por el integrante. PS-14 documenta la solicitud
  del resumen que después se envió como documento a Claude en CS-05. El texto aportado coincide
  en contenido con esa respuesta de Perplexity, con diferencias de formato.
- PS-12 y PS-14 contienen referencias a `image.jpg`, y la respuesta de Perplexity trabaja con
  la tabla de tareas. Esto documenta la revisión y consolidación de ese material. CS-06 menciona
  además una transcripción de tablas por otra IA; no se convierte esa mención en un prompt
  independiente ni se afirma que toda esa transcripción esté conservada.
- Los adjuntos originales se conservan por el integrante. No hace falta duplicarlos todos en
  esta relación. El nombre original del archivo de CS-05 no se inventa: se identifica por su
  contenido, propósito, fecha y confirmación del integrante.
- El texto aportado para identificar el primer Markdown adjunto de CH-01 se reproduce aparte,
  hasta Exclusiones, sin añadir las partes de las bases que no se incluyeron en ese texto.
  Se conserva como contexto suministrado a ChatGPT, no como instrucciones actuales ni como
  un prompt adicional. El registro distingue esa copia del archivo original enviado.
- El PDF de Grok recorta horizontalmente parte de una tabla de contexto pegada de Claude.
  Se transcribe lo recuperable del documento aportado y se señala esa limitación en GK-01,
  sin reconstruir celdas ni confundir el contexto pegado con la respuesta de Grok.
- El chat original de ChatGPT de septiembre tiene ahora sus cinco prompts recuperados del PDF.
  La respuesta a CH-04 contiene el plan pegado después en GK-01, y la respuesta a CH-05 incluye
  el inventario del dataset citado después en PS-02 y PS-03. Esas citas se conservan como
  contexto y no se cuentan como nuevas consultas de ChatGPT. Las pruebas de análisis visibles
  en el PDF son evidencia histórica de esa conversación, no ejecuciones realizadas nuevamente aquí.
- La sesión actual se registra hasta la solicitud inicial de preparar esta declaración. Las
  aclaraciones posteriores completan horarios, herramientas, criterio Extra/Alto y procedencia
  de los adjuntos; no se cuentan de nuevo como prompts del desarrollo del proyecto.
- Los registros contienen sugerencias y cifras provisionales que no deben confundirse con el
  método ni con los resultados finales. Las pruebas que una respuesta antigua afirma haber
  ejecutado se registran como afirmaciones históricas, no como pruebas reproducidas aquí.
- La copia pública del registro omite de forma marcada fragmentos personales en nueve
  intervenciones; conserva sus IDs, propósito, herramienta y horario. El registro completo
  permanece bajo custodia de Osmar para integrar la entrega. Las omisiones no se presentan
  como textos literales completos ni se sustituyen por prompts inventados.
