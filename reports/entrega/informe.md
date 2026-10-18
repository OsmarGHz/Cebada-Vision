# CebadaVision: predicción del rendimiento de cebada de temporal en Hidalgo, Tlaxcala y Puebla

Reto AgroCebada 2026 (FIRA) · Equipo CebadaVision · Octubre de 2026

## 1. Introducción [400–550 palabras]

La cebada es uno de los cultivos más importantes del sector agroindustrial: es fundamental para la
industria maltera y cervecera y un insumo clave para alimentos y ganado. Todo ese sistema depende
de la predictibilidad: el rendimiento por hectárea y la calidad del grano determinan la logística,
los precios y la operación de la industria. En México, cerca de tres cuartas partes de la superficie se siembra en el
Altiplano central, casi toda de temporal, y Hidalgo, Puebla y Tlaxcala concentran la mayor parte de
la producción (SIAP, 2023), en manos de pequeños y medianos productores que venden su cosecha a
comercializadoras y parafinancieras.

El cultivo enfrenta desafíos crecientes: el cambio climático altera los patrones de lluvia y
temperatura, las plagas son menos predecibles y los insumos se encarecen. El entorno
es especialmente difícil para los pequeños productores, que carecen de herramientas para
monitorear sus cultivos de forma continua y toman decisiones reactivas. Ante ello, la combinación de imágenes satelitales, datos climáticos y
aprendizaje automático permite convertir información compleja en decisiones claras: Sentinel-2
observa cada cinco días a 10 m, Planet casi a diario a 3 m, y los modelos que combinan estas series
con clima y relieve explican buena parte de la variación del rendimiento en cultivos de temporal
(van Klompenburg et al., 2020; de la Fuente et al., 2023).

El Reto AgroCebada 2026 plantea ese problema con datos reales: 197 parcelas de cebada de temporal
del ciclo abril–octubre de 2025 en Hidalgo, Tlaxcala y Puebla, con índices de vegetación de
Sentinel-2, Landsat y Planet, precipitación y temperatura mensuales, elevación y pendiente. El rendimiento de grano (toneladas por hectárea) se conoce para 138 parcelas; el de las
otras 59 lo resguarda el comité para calificar las predicciones. Ese rendimiento proviene, en la
mayoría de los casos, del registro de compra de la comercializadora y no de una medición en campo,
por lo que contiene ruido y, en algunas zonas, está redondeado a medias toneladas.

Este trabajo presenta CebadaVision, una solución con tres partes. Primero, una tabla de variables
por parcela que resume cómo se comportó cada índice durante el ciclo (cuándo emergió el cultivo,
cuánto verdor alcanzó, cuánto duró verde y qué tan rápido se secó), más clima, relieve y ubicación. Segundo, un modelo que promedia dos algoritmos de árboles
(LightGBM y Random Forest), validado con un esquema repetido y estratificado por estado, que
alcanza un error (RMSE) de 0.49 t/ha frente a 0.85 t/ha de predecir el promedio regional. Tercero,
una aplicación web que ejecuta el modelo, muestra las 197 parcelas en un mapa, entrega la
estimación con su rango y explica con palabras sencillas cómo se llegó a cada número.

El análisis exploratorio reveló un hecho que ordena todo el trabajo: la ubicación de la parcela
explica cerca de dos tercios de la variación del rendimiento. Las tres zonas del estudio rinden
distinto (alrededor de 4.5 t/ha en el este de Puebla, 3.0 en el suroeste de Tlaxcala y 3.3 en el
norte de Hidalgo) y las parcelas vecinas comparten suelo, clima y manejo. Por eso el modelo usa de
forma explícita la información espacial y mide lo que aportan los índices satelitales, el clima y
el relieve *dentro* de esa estructura. Ese mismo marco se utiliza para responder las tres
preguntas guía del reto.

## 2. Justificación [100–200 palabras]

Los modelos tradicionales de evaluación y financiamiento agrícola dependen de estimaciones basadas
en datos históricos y empíricos que no reflejan la realidad actual de cada parcela. Esa falta de
información precisa genera incertidumbre y eleva el riesgo percibido; como resultado, los
productores tienen dificultades para acceder a créditos justos y seguros adecuados, y quedan
expuestos al clima y a otros imprevistos.

Este proyecto busca transformar esa vulnerabilidad en estabilidad: reducir la incertidumbre sobre el
rendimiento con proyecciones basadas en evidencia satelital y climática, no en suposiciones, y con
un error cuantificado. Los datos que genera son transparentes y trazables, lo que reduce la
desigualdad de información en la cadena de valor y facilita el acceso a servicios financieros y la
inversión pública y privada en el sector. El reto aporta además un caso poco común: datos reales de
197 parcelas con rendimiento comercial, no sintéticos. Resolverlo con rigor —validación reproducible
y explicación de cada predicción— es lo que hace creíble la herramienta para el analista de crédito
y para el productor, público prioritario según FIRA.

## 3. Objetivos [200 palabras]

**Objetivo general.** Predecir el rendimiento de grano (t/ha) de parcelas de cebada de temporal del
ciclo abril–octubre de 2025 en Hidalgo, Tlaxcala y Puebla a partir de índices de vegetación
satelitales, clima, relieve y ubicación, y entregar las predicciones de las 59 parcelas sin dato.

**Objetivos específicos.**

1. Recopilar, auditar y limpiar datos de varias fuentes —índices de vegetación de Planet y
   Sentinel-2, clima, relieve y registros espaciales— para construir un conjunto reproducible de
   variables por parcela con la fenología de cada índice.
2. Crear y probar modelos de aprendizaje automático (Ridge, Random Forest, LightGBM, proceso
   gaussiano y ensambles) que predigan la cosecha de cada terreno, comparados con un mismo esquema
   de validación cruzada repetida y estratificada por estado, con RMSE, MAE y R² frente al promedio
   regional (RMSE 0.851) y a un kNN espacial.
3. Responder con evidencia las tres preguntas guía: qué índice de vegetación pesa más, qué variable
   climática tiene mayor peso y qué combinación de variables funciona mejor.
4. Diseñar y poner en funcionamiento una aplicación interactiva que incluya el modelo y muestre las
   predicciones en un mapa con su rango y una explicación sencilla por parcela; discutir su uso en
   inclusión financiera.

## 4. Metodología [600–700 palabras]

**Datos.** Se utilizó únicamente el dataset oficial: 197 polígonos (138 de entrenamiento y 59 por
predecir), 47 804 observaciones de Planet (NDVI, EVI, LAI, MSAVI) de 2025, 107 666 de Sentinel-2 y
Landsat de 2022 a 2025 (22 índices), rásteres mensuales de precipitación (CHIRPS) y de temperatura
mínima y máxima a unos 5 km, y elevación y pendiente del Continuo de Elevaciones Mexicano. Una
auditoría confirmó 197 identificadores únicos en todas las fuentes, la unión sin pérdidas y el
reparto 138/59. Se trabajó con el ciclo abril–octubre de 2025 (más
noviembre, para capturar la senescencia). Las observaciones con nubosidad del 100 % se descartaron
porque traen los índices vacíos; no se imputó ninguna. Landsat no aporta índices en 2025.

**Variables.** Para cada parcela e índice se tomó la serie del promedio del polígono, se suavizó
con una mediana móvil de tres observaciones y se calcularon: mediana de cada mes de abril
a noviembre, medianas por ventana (mayo–junio, julio–septiembre, octubre–noviembre), valor y fecha
del máximo, amplitud, área bajo la curva de abril a octubre, inicio y fin de la temporada verde
(cuando la curva cruza la mitad de su amplitud al subir y al bajar), duración y velocidades de
crecimiento y de secado. Resultaron 80 variables de Planet y 160 de Sentinel-2 (NDVI, EVI, SAVI,
LAI, fAPAR, NDWI, MSI, NDTI). El clima se resumió en lluvia acumulada abril–octubre, temperaturas
mínima y máxima medias del ciclo y anomalía de lluvia respecto al promedio 2022–2024; por la
resolución del ráster, estas variables solo toman 25 valores distintos en las 197 parcelas. El
relieve aporta elevación media, su variación y pendiente media. La ubicación se representó con las
coordenadas del centroide (km), la zona (k-means de tres grupos sobre los centroides, sin usar el
rendimiento), el rendimiento promedio de la zona y el promedio ponderado por distancia del
rendimiento de las ocho parcelas de entrenamiento más cercanas.

**Validación.** La métrica principal es el RMSE (criterio de FIRA), con MAE y R². Se usó
validación cruzada de 5 particiones estratificadas por estado —imita el reparto oficial 70/30,
proporcional por zona y espacialmente mezclado— repetida 10 veces con semillas distintas; se
reporta promedio y desviación entre repeticiones, y se considera ruido cualquier diferencia de
RMSE menor a 0.03 t/ha. Como prueba más exigente se añadió una validación agrupada por municipio.
Las variables de vecinos y de zona se
recalculan dentro de cada partición solo con las parcelas de entrenamiento de esa partición (y sin
contar a la propia parcela), de modo que el rendimiento de una parcela nunca entra en sus propias
variables ni en las de las parcelas con las que se evalúa.

**Modelos.** Se compararon regresión ridge, Random Forest (400 árboles, hoja mínima de 3, 33 % de
variables por partición), un LightGBM pequeño (300 árboles, tasa 0.03, 7 hojas, submuestreo,
regularización L2) y un proceso gaussiano con núcleo RBF más ruido; los faltantes se rellenan con
la mediana de entrenamiento dentro de cada ajuste. El banco de experimentos evaluó cada grupo de
variables por separado, la ubicación más cada grupo, combinaciones completas y ensambles. Para las preguntas guía se evaluó cada índice con sus variables fenológicas y cada
variable climática, solos y con la ubicación fija, y se calcularon la importancia por permutación
del modelo final (aumento del RMSE al barajar cada variable) y una ablación por grupos.

**Modelo final.** Promedio de dos modelos: LightGBM con ubicación, relieve y clima (11 variables)
y Random Forest con ubicación, fenología de Planet, clima y relieve (91 variables). La predicción
se recorta al rango plausible de 1.5 a 6.5 t/ha; el rango de predicción al 80 % es ±1.28 veces el
RMSE de validación. Para explicar cada predicción en la aplicación se calculan
valores SHAP (Lundberg y Lee, 2017) promediados entre ambos modelos y agrupados por tipo de
variable; con ellos la ficha de cada parcela indica qué factores subieron o bajaron su estimación. Para que la aplicación ejecute el modelo en el navegador se ajustó
una regresión ridge sustituta sobre 11 variables y se reporta cuánto difiere del ensamble.

**Implementación.** Python 3.13 (pandas, geopandas, rasterio, scikit-learn, LightGBM, SHAP);
aplicación en React, TypeScript, Leaflet y Recharts.

## 5. Resultados y discusión [800 palabras]

**Puntos de referencia.** Predecir el promedio de entrenamiento da RMSE 0.851 t/ha (R² −0.02).
Un kNN espacial que solo usa las ocho parcelas vecinas baja a 0.501 (R² 0.65): la ubicación por
sí sola explica cerca de dos tercios de la variación y es la referencia que cualquier modelo debe superar.

**Cada grupo de variables por separado** (CV 5×10, LightGBM). Solo coordenadas: 0.507; solo
vecinos: 0.502; solo clima: 0.545; solo fenología de Planet: 0.625; solo Sentinel-2: 0.636; solo
estadísticos simples de Planet (media, desviación, máximo, mínimo): 0.784; solo relieve: 0.762.
La fenología completa vale mucho más que los estadísticos simples, porque la señal agronómica está
al inicio del ciclo y en el secado, no en el máximo, que se satura en agosto–septiembre. El clima
predice bien pese a tomar solo 25 valores distintos: opera, en la práctica, como indicador de zona.

**Ubicación más cada grupo.** Sumar a la ubicación los índices de Planet, Sentinel-2 o el clima deja
el RMSE entre 0.500 y 0.515; sumar relieve lo lleva a 0.492. Ningún grupo aporta más de 0.01–0.02
t/ha una vez conocida la ubicación: la correlación de cualquier variable satelital con lo que el kNN
no explica no pasa de |ρ| = 0.17. Con 138 parcelas y un rendimiento comercial, redondeado a medias
toneladas en toda la zona de Tlaxcala, el piso de ruido es alto. Los modelos lineales empeoran al
agregar variables (ridge con 251 variables: 0.567); los de árboles se mantienen.

**Modelo final.** El ensamble LightGBM (ubicación, relieve, clima) + Random Forest (ubicación,
fenología Planet, clima, relieve) obtiene RMSE 0.491 ± 0.007, MAE 0.336 y R² 0.664. En la
validación agrupada por municipio da RMSE 0.574 frente a 0.708 del kNN puro: las variables
satelitales, climáticas y de relieve sí mejoran la extrapolación a municipios no vistos.
Por estado, el RMSE es 0.357 en Hidalgo, 0.375 en Tlaxcala y 0.578 en Puebla, donde el rendimiento
es más alto y más variable (≈4.5 ± 0.5 t/ha): el modelo acierta el nivel de cada zona, pero explica
poco de la variación dentro de Puebla. Las 59 predicciones tienen promedio 3.95 t/ha y van de 2.88 a
4.65, en línea con el entrenamiento: 4.47 en Puebla, 3.79 en Hidalgo y 3.00 en Tlaxcala. Frente
al Ridge provisional de nueve variables (0.551) la mejora es de 0.06 t/ha; frente al promedio, 0.36.
Un Random Forest del equipo con clima y municipio/estado codificados (one-hot), con particiones
propias, obtuvo 0.513 ± 0.087 (MAE 0.363, R² 0.621), coherente con el predominio de la zona.

**Pregunta 1: ¿qué índice es más importante?** El EVI de Planet. Con los mismos folds, cada índice
solo con sus variables fenológicas da RMSE 0.639 (EVI), 0.655 (MSAVI), 0.678 (NDVI) y 0.685 (LAI);
en Sentinel-2 los mejores son LAI y SAVI (0.660) y el peor NDTI (0.733). La importancia por
permutación del modelo final mantiene el orden EVI > MSAVI > NDVI > LAI; las variables de EVI que
más pesan son la mediana de mayo–junio (emergencia) y la velocidad de secado. EVI se satura menos
que NDVI cuando el cultivo cubre todo el suelo y es menos sensible al fondo (Huete et al., 2002).

**Pregunta 2: ¿qué variable climática pesa más?** La precipitación del ciclo. Sola, la anomalía de
lluvia respecto a 2022–2024 es la que más explica (RMSE 0.584), seguida de la temperatura mínima
(0.603), la lluvia acumulada (0.604) y la temperatura máxima (0.658). 2025 fue más lluvioso que el
promedio 2022–2024 en todas las parcelas (de +202 a +574 mm) y las parcelas con mayor exceso de
lluvia rindieron menos. Con la ubicación fija, ninguna variable climática agrega más de 0.01 t/ha,
y dentro del modelo final la temperatura mínima es la que más mueve la predicción; ambas lecturas
están limitadas por los 5 km de resolución del clima.

**Pregunta 3: ¿qué combinación funciona mejor?** Ubicación + relieve + clima + fenología de Planet
(RMSE 0.494 en la ablación), seguida de ubicación + relieve (0.496); la mejor sin ubicación es
índices + clima + relieve (0.538) y la peor, solo relieve (0.754). Sumar Sentinel-2 a Planet no
mejora (0.507–0.520): ambos sensores capturan la misma fenología y Planet, casi diario, la describe
mejor. La combinación óptima reúne información complementaria: la ubicación fija el nivel, relieve
y clima afinan la zona y la fenología explica diferencias dentro de ella.

**Discusión.** En esta muestra la predicción espacial domina y los índices afinan en el margen; es
una limitación del dato (138 parcelas, rendimiento comercial con redondeo, 25 píxeles de clima), no
del método. Las predicciones son estables (desviación entre repeticiones de 0.007 t/ha), pero su
rango al 80 % es de ±0.63 t/ha, y la aplicación lo muestra junto a cada estimación.

## 6. Uso de la ciencia de datos en la inclusión financiera del sector agro [300 palabras]

Actualmente el crédito de avío a pequeños productores de cebada se decide con información asimétrica: el
intermediario financiero conoce el historial del productor, si lo hay, pero no el potencial
productivo de la parcela concreta que respaldará el pago. CebadaVision convierte datos públicos
—imágenes satelitales, clima, relieve y la ubicación de la parcela— en una estimación de
rendimiento por parcela con error conocido, sin visita de campo y actualizable cada ciclo. Eso
cambia tres decisiones.

Primera, el dimensionamiento del crédito. Con rendimiento esperado, superficie y precio de referencia se
obtiene el valor esperado de la cosecha y, con el rango del modelo, un escenario conservador; el
monto de avío puede ajustarse a lo que esa parcela puede pagar, no a un promedio regional. La
aplicación muestra la producción estimada en toneladas y un semáforo bajo/medio/alto por terciles,
pensado como primer filtro de riesgo.

Segunda, la inclusión de productores sin historial. Alguien sin expediente crediticio puede ser
evaluado por la evidencia objetiva de su parcela y de sus vecinas; la ubicación, que es lo que más
pesa en el modelo, es justamente información que el productor no puede alterar y que la financiera
no necesita verificar en campo.

Tercera, el diseño de seguros y garantías. El error por zona (0.36 t/ha en Hidalgo y Tlaxcala, 0.58
en Puebla) y la trayectoria del vigor del cultivo durante el ciclo permiten detectar a tiempo
desviaciones respecto a lo esperado y activar seguros paramétricos o reestructuras antes de la
cosecha.

Para que esto sea inclusión y no exclusión hace falta transparencia: cada estimación se entrega con
su rango y con una explicación sencilla de qué la subió o la bajó, para que el productor pueda
entenderla, cuestionarla y usarla en su propia negociación con la comercializadora o la financiera.

## 7. Conclusiones [400 palabras]

Se construyó un modelo reproducible que predice el rendimiento de grano de parcelas de cebada de
temporal en Hidalgo, Tlaxcala y Puebla con RMSE de 0.491 ± 0.007 t/ha, MAE de 0.336 y R² de 0.664
en validación cruzada estratificada por estado y repetida diez veces, frente a 0.851 del promedio
regional y 0.501 de un kNN espacial. El modelo final es un ensamble de LightGBM y Random Forest
sobre ubicación, relieve, clima y fenología de Planet, y entrega las 59 predicciones solicitadas con
promedio de 3.95 t/ha y un rango al 80 % de ±0.63 t/ha.

El hallazgo principal es estructural: la ubicación de la parcela explica cerca de dos tercios de la
variación del rendimiento, porque las tres zonas rinden distinto y porque parcelas vecinas comparten
suelo, clima y manejo. Un modelo que ignore esto subestima su error o atribuye a los índices
satelitales un mérito que pertenece a la geografía. Evaluar las variables dentro de esa estructura
permitió responder las preguntas guía con evidencia comparable: el índice más importante es el EVI
de Planet, por su señal en la emergencia y en el secado; la variable climática con mayor peso es la
precipitación del ciclo, en particular su anomalía respecto a 2022–2024; y la mejor combinación es
ubicación + relieve + clima + fenología de Planet; sumar Sentinel-2 no mejora.

Las limitaciones se declaran en la aplicación: rendimiento de origen comercial, redondeado en una
zona; clima a 5 km con solo 25 valores distintos; 138 parcelas de un solo ciclo; variedad, fecha de
siembra, dosis y siniestros desconocidos. Por eso el aporte de los índices sobre la ubicación es
pequeño, aunque mejora la extrapolación a municipios no vistos.

La aplicación CebadaVision ejecuta el modelo en el navegador, muestra las 197 parcelas en un mapa,
permite buscar cada una por su identificador, presenta la estimación con rango y semáforo, explica
con palabras sencillas cómo se llegó al número y ofrece un simulador y la descarga del CSV, con
prioridad en el productor.

Como siguiente paso, el mismo pipeline se extendería a varios ciclos y a rendimientos medidos en
campo, para modelar con la fenología lo que la ubicación no explica, estimar antes de la cosecha y
calibrar el rango por zona. Con FIRA, el modelo podría integrarse a la originación de crédito de
avío como variable objetiva de capacidad productiva por parcela.
