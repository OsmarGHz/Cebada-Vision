# Notas — Sesión de preguntas y respuestas con FIRA (2026-09-27)

> Nota de revisión del 18 oct 2026: se conserva abajo el resumen histórico de las sesiones.
> Las frases «sin medición instrumental» quedaron superadas por la aclaración de pesaje en
> báscula de la cosecha de cada parcela, sin ajustes por humedad, impurezas o mermas.
> No utilizarlas como descripción vigente. El cotejo directo de los nueve adjuntos consta en
> `REVISION_DOCUMENTAL_2026-10-18.md`: acuerdos por correo del 21-sep y segunda sesión del 9-oct.
> Los originales especifican cuatro decimales, muestreo aleatorio estratificado sin detallar
> estratos, variedades Josefa/Voyager sin asignación por parcela y ecuaciones ya proporcionadas.
> Las fechas y pendientes de las notas históricas siguientes no son la referencia vigente.


Resumen de puntos **nuevos o que aclaran/contradicen** lo que ya sabíamos, extraídos de la
transcripción de la sesión de dudas con Pablo Iván Argueta, Maye Rodríguez y Angi Fermoso (FIRA).
No repite lo que ya está en `CLAUDE.md`.

## 🚨 Cambia lo que sabíamos / posible conflicto con las bases

- **Riego: TODAS las parcelas son de temporal** (no de riego). Angi lo confirma explícitamente
  tras la pregunta de Eduardo Flores. Esto responde la duda abierta en `CLAUDE.md` ("Ciclo
  agrícola y fechas de siembra/cosecha... ¿riego?"). Se puede eliminar como pregunta pendiente.
- **Extensión de anexos: hay contradicción en las bases (2 vs 4 cuartillas).** Pablo admite el
  error y dice que el número correcto/válido es **4 cuartillas**, no 2 como dice `CLAUDE.md`
  (tomado del PDF). Motivo: quiere dejar espacio para incluir ahí mismo la tabla con las
  predicciones de las 59 parcelas. **Actualizar el entregable a 4 cuartillas de anexos.**
- **Entrega adicional NO mencionada en las bases originales:** antes de que cierre el periodo de
  entrega (19 oct), cada equipo debe enviar por correo a innovacion@fira.gob.mx un **CSV con el
  rendimiento predicho de las 59 parcelas** (aparte de subirlo a la plataforma). FIRA mandará un
  correo recordatorio con el formato. Esto es para que el comité evalúe más rápido. **Hay que
  agregar este paso a nuestro checklist de entrega.**
- **Rendimiento = dato autorreportado por el productor, sin validación oficial.** Son toneladas
  por hectárea (t/ha, confirmado). No hay medición instrumental de por medio — es lo que el
  productor declaró que cosechó. Relevante para justificar ruido/incertidumbre en el reporte
  técnico y en la sección de metodología.

## Aclaraciones útiles (no estaban documentadas)

- **Herramientas para abrir los archivos espaciales:** QGIS (gratuito) es la opción recomendada
  por FIRA para abrir `.shp`/`.tif`. Alternativas válidas y explícitamente permitidas: Python, R,
  C++, Google Earth Engine — "no hay ninguna limitación", usar lo que sea más cómodo para el
  equipo.
- **Los `.shp` vienen en conjunto de archivos que deben estar juntos en la misma carpeta:**
  `.shp` (geometría), `.dbf` (atributos/tabla), `.prj` (proyección), `.shx` (índice), `.cpg`
  (encoding). Solo se arrastra el `.shp` a QGIS y automáticamente toma los demás.
- **Los TIF no son solo clima:** también incluyen capas de **elevación (DEM)** y **pendiente/
  inclinación del terreno**, tratadas como variables geofísicas/ambientales adicionales para el
  modelo. No estaban mencionadas como features candidatas en nuestra estrategia técnica —
  conviene agregarlas al pipeline de features junto con SRTM (que ya contemplábamos).
- **Diferencia Planet (PRO) vs Sentinel/Landsat (básico):** Planet = mejor resolución espacial
  pero menos índices. Sentinel/Landsat = más índices disponibles, resolución menor. No hay una
  "mejor", es parte del reto decidir qué combinación de variables funciona mejor (conecta
  directo con la pregunta bonus 3).
- **Nubosidad:** cada observación trae un % de nubosidad explícito; si el campo viene vacío se
  interpreta como 0% (satélite no detectó nubes). Una integrante (Dafne) reportó valores
  **negativos en NDVI/algún índice incluso con nubosidad 0%** — FIRA no dio explicación en vivo,
  quedó pendiente de mandar por correo las **fórmulas exactas de cálculo de cada índice** y
  cómo se excluyen píxeles con nubes/sombras. **Seguir de cerca ese correo, puede afectar cómo
  limpiamos los índices.**
- **Partición 70/30 es estratificada geográficamente**, no puramente aleatoria — buscaron que
  cada una de las tres zonas (Puebla/Tlaxcala/Hidalgo) esté representada proporcionalmente tanto
  en entrenamiento como en predicción. Confirma que el enfoque de CV espacial/agrupada que ya
  teníamos planeado tiene sentido.
- **Métrica de evaluación:** primer filtro = **error cuadrático medio (RMSE)** entre predicción y
  valor real resguardado. Después se evalúa metodología y la app/interfaz. No dieron fórmula de
  cómo se combinan RMSE/MAE/R² más allá de esto — sigue sin haber más detalle.
- **Variables externas públicas: permitidas explícitamente**, con la única condición de citarlas.
-
- **Código fuente / repos:** un repositorio de GitHub **no es obligatorio** para el reto. Basta
  con mandar el código como adjunto en el correo final (junto con el CSV de predicciones). Subir
  a GitHub/Colab/Posit es opcional y solo aporta si el equipo quiere dar acceso abierto — puede
  mandarse la liga en ese mismo correo si se desea.
- **Público objetivo de la app/dashboard: ambos** — analistas/especialistas de FIRA y
  productores agropecuarios directamente. Sugerencia explícita de FIRA: pensar en una interfaz
  "ilustrativa" (ej. HTML) entendible por alguien fuera del área técnica, sin que la propuesta
  pierda rigor. El **reporte técnico**, en cambio, debe mantener lenguaje académico porque el
  jurado son profesores universitarios.
- **Nombre del proyecto no se puede cambiar** una vez inscrito en el sistema (tal vez sí en la
  presentación final si el equipo llega a finalista, pero no está garantizado).
- **Asesores externos:** se permite apoyarse en un profesor u otra persona como asesor, pero
  **no se pueden inscribir nuevos integrantes** al equipo (el registro ya cerró). El asesor debe
  quedar reportado como tal (no como integrante) en los anexos, y cada integrante del equipo
  debe poder defender el conocimiento completo del proyecto ante el jurado.
- **Constancias de inscripción:** deben incluir una **fecha explícita del periodo vigente**
  (ej. "otoño 2026"), no basta con que diga "vigente" sin fecha. Equipos con constancias
  observadas tienen ~1 semana extra para reenviarlas.
- Habrá una **segunda sesión de dudas en ~2 semanas** (alrededor de la 1:00 pm), para revisar
  avances.

## Ambigüedad detectada en la transcripción (no aclarada)

- En un momento la sesión se refiere al cultivo como "trigo" en vez de "cebada" al hablar de
  destino (malta vs. forraje). Puede ser un lapsus del ponente; FIRA respondió que el
  rendimiento se deja **estandarizado, sin distinguir destino/uso final** del grano — aplica
  igual independientemente del nombre usado.

## Acciones sugeridas para el equipo

1. Actualizar `CLAUDE.md`: quitar la duda de riego (todo es temporal), corregir anexos a 4
   cuartillas, agregar el paso de enviar CSV de predicciones por correo antes del 19 oct.
2. Agregar elevación y pendiente como features confirmadas (no solo hipótesis) en el pipeline.
3. Esperar el correo de FIRA con: fórmulas de índices espectrales, y la plantilla/formato del
   CSV de predicciones a enviar por correo.
4. Diseñar el dashboard pensando en doble audiencia (especialista + productor) — posible reflejo
   en dos vistas o modos dentro de la misma app.

---

# Sesión de Q&A #2 con FIRA (~1 semana antes del cierre, fecha exacta por confirmar)

Segunda transcripción (moderador Luis; ponentes Pablo, Angi, Maye, Fer). Solo puntos **nuevos o que
corrigen** lo anterior y `CLAUDE.md`. Se mantiene todo lo de la sesión 1.

## 🚨 Corrige / matiza lo que sabíamos

- **Origen del rendimiento: NO es solo autorreportado.** En la mayoría de los casos el dato lo
  reportó la **empresa comercializadora/parafinanciera a la que el pequeño productor vende** su
  cosecha; solo una parte muy pequeña viene directo del productor. Es dato por parcela, y **una
  misma medición no se asigna a varias parcelas**. Actualizar `CLAUDE.md` ("autorreportado por el
  productor"): es registro de compra/acopio, probablemente menos ruidoso que una declaración
  libre, aunque sigue sin ser medición instrumental ni estandarizada. Compatible con que
  Tlaxcala venga redondeado a 0.5.
- **Rendimiento = GRANO únicamente, no forraje** (Angi lo confirmó por chat tras la duda de
  Felipe). Unidad: t/ha de cosecha. Resuelve la ambigüedad "trigo/forraje" de la nota anterior.
- **Formato de predicción:** un **número cerrado** por parcela (sin intervalos), **máx. 4
  decimales**. Tabla con nombre del equipo + ID de polígono + rendimiento predicho (t/ha), las
  **59 filas**. Pablo enseñó la plantilla al final; llegará por correo. → El intervalo de
  incertidumbre va solo en la app/reporte, **no** en el CSV.
- **Evaluación:** sobre las 59 parcelas, **sin ponderar por superficie** (cada parcela pesa
  igual). El comité define la métrica; el equipo define cómo mide su propio error interno.
- **La restricción temporal no aplica:** el ciclo abr–oct 2025 ya pasó; preguntaron si solo usar
  info publicada "a la fecha de estimación" y la respuesta es que es retrospectivo → se puede
  usar cualquier dato público, incluso posterior a la cosecha (clima observado del ciclo, etc.).

## Datos y su calidad

- **Nulos = dos causas distintas:** (1) nubosidad 100% → índice no medible; (2) Sentinel y
  Landsat pasan en **fechas distintas**, así que una fila de un sensor no tiene valor de otro ese
  día. No hay que calcular/imputar índices por nuestra cuenta; nubosidad es **solo filtro de
  calidad**. → Filtrar por nubosidad y agregar por sensor/ventana, no imputar fila a fila.
- **Polígonos:** trazados por la empresa **NXT** (monitoreo satelital). Origen del trazo mixto
  (GPS de campo, imagen satelital o registro del productor/aseguradora), validado en campo e
  imagen. El rendimiento corresponde al polígono completo → estadísticas por polígono con todos
  los píxeles son coherentes con el rendimiento.
- **IDs aleatorios**, sin vínculo a productor; lo único identificable es la ubicación.
- **Selección train/pred:** estratificada por zona, **espacialmente bien repartida, sin
  manchones/clusters**. → los 59 test están intercalados con los train: CV espacial agrupada
  puede ser *más pesimista* que la prueba real; kNN espacial/vecinos cercanos tiene ventaja.
  Considerar reportar ambas (CV aleatoria repetida y CV por bloques).
- **Tipo de grano:** FIRA cree que es el mismo en todas las parcelas; **pendiente confirmar** por
  correo (oficina regional). La **variedad** quedó pendiente también.
- **Fecha de siembra:** típica **1 mayo – 15 junio**. Puede que manden fecha/semana real de
  *algunas* parcelas; sin garantía. Sirve para acotar ventana fenológica.
- **Desconocido para todos (no buscar, declararlo como limitación):** rotación de cultivos
  2022–2024, siniestros 2025 (granizo, helada, plaga, seguro), dosis de siembra. Para dosis:
  **Agrocostos** en fira.gob.mx tiene paquetes tecnológicos por estado/zona (usable como
  referencia externa citada).

## Qué esperan del modelo y la app

- **Generalizar a toda la región** (no sobreajustar a las 138): los rendimientos son parecidos
  entre zonas; el modelo debe representar a los tres estados. Escala de insumos externos
  cercana a la de las parcelas. Insumos externos: sin límite, siempre que sean públicos, bien
  citados y **justificados**.
- **Si somos finalistas:** el modelo podría usarse en parcelas futuras y habría colaboración con
  FIRA para extender el estudio → mencionarlo como visión en conclusiones/presentación.
- **App:** objetivo real = **utilidad para el productor** (matemática ya resuelta; hacerla fácil
  de entender). Debe incluir **nota en lenguaje sencillo de cómo se llegó al número** (explicación
  por parcela), además de consulta de predicciones. Respuesta de FIRA: "ambas cosas, prioridad
  productor". Confirma doble audiencia de la sesión 1 pero **con prioridad productor**.

## Plataforma de entrega (operativo)

- Cada campo del reporte tiene **contador de palabras con tope duro** (no deja pasarse).
- **Hay que dar clic en guardar** y verificar que el enlace del documento quede en azul con el
  nombre del archivo; igual para anexos y bibliografía (PDF).
- **No deja publicar si falta algún campo** → llenar todo.
- Un solo campo de enlace para dashboard/video; cualquier otra cosa extra, por correo, **antes
  del 19 oct** (aún reciben complementos).
- Baja de equipo: mensaje en la plataforma o correo, sin trámite.
- Dudas extra: todavía hay ~1 semana por correo.

## Acciones nuevas

1. Corregir en `CLAUDE.md`: fuente del rendimiento (comercializadora, no autorreportado), grano
   no forraje, CSV con ≤4 decimales y sin ponderar por superficie.
2. Pipeline: filtrar por nubosidad (no imputar), separar S2/Landsat, clip de predicciones a rango
   plausible y `round(4)` al exportar.
3. Reporte (limitaciones): rotación, siniestros, dosis, variedad desconocidos; dato de origen
   comercial.
4. App: agregar bloque "¿cómo se obtuvo este número?" en lenguaje llano por parcela.
5. Considerar Agrocostos como fuente citada para contexto agronómico (paquete tecnológico).
6. Esperar correo FIRA: plantilla CSV, tipo de grano/variedad, fórmulas de índices.
