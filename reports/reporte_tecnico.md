# CebadaVision: predicción del rendimiento de cebada de temporal en el Altiplano central

Reto AgroCebada 2026 (FIRA). Equipo CebadaVision.

Cada sección respeta el límite de palabras de las bases (se indica entre corchetes). El texto se
copia campo por campo en la plataforma; Bibliografía y Anexos se suben como PDF.

---

## 1. Introducción [400–550 palabras]

La cebada (*Hordeum vulgare* L.) es el cuarto cereal en superficie en México y el insumo central
de la industria maltera. Alrededor de tres cuartas partes de la superficie nacional se siembra en el
Altiplano central, en condiciones de temporal de verano, y los estados de Hidalgo, Puebla y Tlaxcala
concentran la mayor parte de esa producción (SIAP, 2023). En esta región el cultivo lo practican
predominantemente pequeños y medianos productores que venden su cosecha a comercializadoras y
parafinancieras, de modo que el rendimiento por hectárea determina a la vez el ingreso del
productor y la capacidad de pago de los créditos de avío que financian el ciclo.

Estimar ese rendimiento con cobertura total de parcelas y sin visitas de campo es un problema
abierto con valor público directo. La percepción remota ofrece hoy series densas de índices de
vegetación a escala de parcela: Sentinel-2 cada cinco días a 10 m y constelaciones comerciales
como Planet casi a diario a 3 m. La literatura muestra que modelos de aprendizaje automático
alimentados con estas series, clima y relieve explican una parte sustancial de la variación del
rendimiento en cereales de temporal (van Klompenburg et al., 2020), aunque su desempeño depende del
tamaño de la muestra, de la calidad del dato de rendimiento y de la estructura espacial.

El Reto AgroCebada 2026 plantea exactamente este problema sobre un conjunto real: 197 parcelas
georreferenciadas de cebada de temporal del ciclo abril–octubre de 2025 en Hidalgo, Tlaxcala y
Puebla, con índices de vegetación de Sentinel-2, Landsat y Planet, precipitación y temperatura
mensuales, elevación y pendiente. El rendimiento (grano, t/ha) se conoce para 138 parcelas; el de
las 59 restantes lo resguarda el comité y sirve para evaluar las predicciones. El dato de
rendimiento proviene en su mayoría del registro de compra de la comercializadora, no de una
medición instrumental, lo que introduce ruido y, en algunas zonas, redondeo a múltiplos de 0.5 t/ha.

Este trabajo desarrolla CebadaVision, una solución compuesta por (i) una tabla de variables por
parcela que resume la fenología de cada índice (valores mensuales, emergencia, máximo, duración de
la temporada verde, velocidad de secado), el clima del ciclo, el relieve y la ubicación; (ii) un
modelo de ensamble de árboles (LightGBM y Random Forest) validado con validación cruzada repetida
y estratificada por estado, que alcanza un RMSE de 0.49 t/ha frente a 0.85 t/ha de predecir la
media regional; y (iii) una aplicación web que ejecuta el modelo, muestra las 197 parcelas en un
mapa, entrega la estimación con intervalo y explica en lenguaje llano cómo se llegó a cada número.

El análisis exploratorio reveló un hecho que organiza todo el trabajo: la ubicación de la parcela
explica cerca de dos tercios de la varianza del rendimiento, porque las tres zonas tienen
regímenes distintos (≈4.5 t/ha en el este de Puebla, ≈3.0 en el suroeste de Tlaxcala y ≈3.3 en el
norte de Hidalgo) y porque parcelas vecinas comparten suelo, clima y manejo. Por ello el modelo
incorpora la información espacial y evalúa el aporte de índices, clima y relieve *dentro* de esa
estructura, que es también el marco con el que respondemos las tres preguntas guía.

## 2. Justificación [100–200 palabras]

FIRA y los intermediarios financieros rurales otorgan crédito de avío a productores de cebada
sin una medida objetiva, oportuna y de bajo costo del rendimiento esperado por parcela. Esa
ausencia encarece el crédito, excluye a quienes no tienen historial documentado y dificulta
diseñar seguros ligados a la producción. Un modelo que, a partir de datos satelitales y
climáticos públicos, estime el rendimiento de cualquier parcela georreferenciada con un error
conocido convierte información ya disponible en un insumo de decisión financiera.

El reto aporta además un caso de estudio inusual: datos reales de 197 parcelas con rendimiento
comercial, no sintéticos ni de estación experimental. Resolverlo con rigor —validación
reproducible, cuantificación honesta de la incertidumbre y explicación de cada predicción— es
necesario para que la herramienta sea creíble tanto para el analista de crédito como para el
productor, que fue el público prioritario señalado por FIRA en las sesiones de dudas.

## 3. Objetivos [200 palabras]

**Objetivo general.** Predecir el rendimiento de grano (t/ha) de parcelas de cebada de temporal
del ciclo abril–octubre de 2025 en Hidalgo, Tlaxcala y Puebla, a partir de índices de vegetación
satelitales, clima, relieve y ubicación, y entregar las predicciones de las 59 parcelas sin dato
con un error cuantificado.

**Objetivos específicos.**

1. Construir una tabla reproducible de variables por parcela que resuma la fenología de los
   índices de Planet y Sentinel-2 (ventanas mensuales, emergencia, máximo, duración, velocidad de
   secado), el clima del ciclo, el relieve y la ubicación.
2. Comparar modelos (Ridge, Random Forest, LightGBM, proceso gaussiano y ensambles) con un mismo
   esquema de validación cruzada repetida y estratificada por estado, complementado con validación
   agrupada por municipio, usando como referencia la media regional (RMSE 0.851) y un kNN espacial.
3. Responder con evidencia las tres preguntas guía: qué índice de vegetación pesa más, qué variable
   climática tiene mayor peso y qué combinación de variables funciona mejor.
4. Poner el modelo al alcance de analistas y productores mediante una aplicación web que lo ejecute,
   muestre mapa, intervalo de predicción y una explicación en lenguaje llano por parcela, y discutir
   su uso en inclusión financiera.

## 4. Metodología [600–700 palabras]

**Datos.** Se usó exclusivamente el dataset oficial: 197 polígonos (138 de entrenamiento con
rendimiento, 59 de predicción), 47 804 observaciones de Planet (NDVI, EVI, LAI, MSAVI) de 2025,
107 666 observaciones de Sentinel-2 y Landsat 2022–2025 (22 índices), rásteres mensuales de
precipitación (CHIRPS) y temperatura mínima y máxima a ~5 km, y elevación y pendiente del Continuo
de Elevaciones Mexicano. Una auditoría confirmó 197 identificadores únicos en todas las fuentes,
la unión sin pérdidas entre shapefile y tablas y el reparto 138/59. Se usó el ciclo abril–octubre
de 2025 (más noviembre para capturar la senescencia); las observaciones con nubosidad del 100 % se
descartaron por traer índices vacíos y no se imputó ninguna. Landsat no aporta índices en 2025.

**Variables.** Para cada parcela e índice se calculó, sobre la serie de promedios del polígono
suavizada con mediana móvil de tres observaciones: mediana mensual de abril a noviembre, medianas
por ventana (mayo–junio, julio–septiembre, octubre–noviembre), valor y fecha del máximo, amplitud,
integral abril–octubre, inicio y fin de la temporada verde (cruce del 50 % de la amplitud), duración
y pendientes de crecimiento y secado: 80 variables de Planet y 160 de Sentinel-2 (NDVI, EVI, SAVI,
LAI, fAPAR, NDWI, MSI, NDTI). El clima se resumió en precipitación acumulada abril–octubre,
temperaturas mínima y máxima medias y anomalía de precipitación respecto a 2022–2024 (solo 25
valores distintos para las 197 parcelas, por la resolución del ráster). El relieve aporta elevación
media, su desviación y pendiente media. La ubicación se representó con las coordenadas del centroide
(EPSG:6372, km), la zona (k-means de tres grupos sobre centroides, sin usar el rendimiento), el
promedio del rendimiento de la zona y el promedio ponderado por distancia del rendimiento de las
ocho parcelas de entrenamiento más cercanas.

**Validación.** La métrica principal es el RMSE (criterio de FIRA), con MAE y R². Se usó validación
cruzada de 5 particiones estratificadas por estado —réplica del reparto oficial 70/30, proporcional
por zona y espacialmente intercalado— repetida 10 veces con semillas distintas; se reporta la media
y la desviación entre repeticiones, y se considera ruido toda diferencia de RMSE menor a 0.03 t/ha. Como prueba de robustez espacial se añadió una validación agrupada por municipio
(10 grupos), más pesimista que el caso real. Las variables de vecinos y de zona se recalculan dentro
de cada partición únicamente con las parcelas de entrenamiento de esa partición (y por *leave-one-out*
para las propias parcelas de entrenamiento), de modo que el rendimiento de una parcela nunca
participa en sus propias variables ni en las de las parcelas con las que se evalúa.

**Modelos.** Se compararon regresión ridge con selección interna de penalización, Random Forest
(400 árboles, hoja mínima 3, 33 % de variables por partición), LightGBM pequeño (300 árboles,
tasa 0.03, 7 hojas, submuestreo, regularización L2) y un proceso gaussiano con núcleo RBF más
ruido; los faltantes se imputan con la mediana de entrenamiento dentro de cada ajuste. El banco de
experimentos (`reports/experimentos.md`) evaluó cada grupo de variables por separado, la ubicación
más cada grupo, combinaciones completas y ensambles por promedio. Para las preguntas guía se evaluó
cada índice con sus variables fenológicas y cada variable climática, solos y con la ubicación fija,
y se calculó la importancia por permutación del modelo final y una ablación por grupos con la misma
receta de ensamble.

**Modelo final.** Promedio de dos modelos: LightGBM con ubicación, relieve y clima (11 variables) y
Random Forest con ubicación, fenología de Planet, clima y relieve (91 variables); la predicción se
recorta al rango plausible 1.5–6.5 t/ha. El intervalo de predicción al 80 % se construye como
±1.28·RMSE de validación. La explicación por parcela usa valores SHAP (Lundberg y Lee, 2017)
promediados entre ambos modelos, agregados por tipo de variable y traducidos a una nota en lenguaje
llano. Para que la aplicación ejecute el modelo en el navegador se ajustó una regresión ridge
sustituta sobre 11 variables interpretables, cuya diferencia con el ensamble se reporta.

**Implementación.** Python 3.13 (pandas, geopandas, rasterio, scikit-learn, LightGBM, SHAP);
aplicación en React, TypeScript, Leaflet y Recharts; pipeline de cinco scripts documentado en el
README del repositorio.

## 5. Resultados y discusión [800 palabras]

**Referencias.** Predecir la media de entrenamiento da RMSE 0.851 t/ha (R² −0.02). Un kNN
espacial con las ocho parcelas vecinas baja a 0.501 (R² 0.65): la ubicación sola explica cerca de
dos tercios de la varianza y es la vara real que cualquier modelo debía superar.

**Grupos de variables por separado** (CV 5×10, LightGBM). Solo coordenadas: 0.507; solo vecinos:
0.502; solo clima: 0.545; solo fenología de Planet: 0.625; solo Sentinel-2: 0.636; solo
estadísticos simples de Planet (media, desviación, máximo, mínimo): 0.784; solo relieve: 0.762.
La fenología completa vale mucho más que los estadísticos simples, porque la señal agronómica está
en el inicio del ciclo y en el secado, no en el máximo, que satura en agosto–septiembre; y el clima
"predice" bien pese a tener solo 25 valores distintos: actúa como proxy de la zona.

**Ubicación más cada grupo.** Añadir a la ubicación los índices de Planet, Sentinel-2 o el clima
deja el RMSE entre 0.500 y 0.515; añadir relieve lo lleva a 0.492. Ningún grupo aporta más de
0.01–0.02 t/ha una vez conocida la ubicación: la correlación de cualquier variable satelital con el
residuo del kNN espacial no supera |ρ| = 0.17. Con 138 parcelas y un rendimiento comercial,
redondeado a 0.5 t/ha en toda la zona de Tlaxcala, el piso de ruido es alto. Los modelos lineales se
degradan al aumentar variables (ridge con 251 variables: 0.567); los de árboles se mantienen.

**Modelo final.** El ensamble LightGBM (ubicación, relieve, clima) + Random Forest (ubicación,
fenología Planet, clima, relieve) obtiene RMSE 0.491 ± 0.007, MAE 0.336 y R² 0.664; en la validación
agrupada por municipio, RMSE 0.574 frente a 0.708 del kNN puro: las variables satelitales,
climáticas y de relieve sí mejoran la extrapolación a municipios no vistos. Por estado, el RMSE es
0.357 en Hidalgo, 0.375 en Tlaxcala y 0.578 en Puebla, donde el rendimiento es más alto y variable
(≈4.5 ± 0.5 t/ha): el modelo acierta el nivel de cada zona, pero explica poco de la variación
dentro de Puebla. Las 59 predicciones tienen media 3.95 t/ha y rango 2.88–4.65, consistentes con el
entrenamiento (media 3.96): 4.47 en Puebla, 3.79 en Hidalgo y 3.00 en Tlaxcala. Frente al Ridge
provisional de nueve variables (0.551) la mejora es de 0.06 t/ha; frente a la media, de 0.36.

**Pregunta 1: ¿qué índice es más importante?** EVI de Planet. Con los mismos folds, cada índice
solo con sus variables fenológicas da RMSE 0.639 (EVI), 0.655 (MSAVI), 0.678 (NDVI) y 0.685 (LAI);
en Sentinel-2 el mejor es LAI/SAVI (0.660) y el peor NDTI (0.733). La importancia por permutación
del modelo final mantiene el orden EVI > MSAVI > NDVI > LAI; las variables de EVI que más pesan son
la mediana de mayo–junio (emergencia) y la velocidad de secado. EVI es menos sensible a la
saturación del dosel y al fondo de suelo que NDVI (Huete et al., 2002).

**Pregunta 2: ¿qué variable climática pesa más?** La precipitación del ciclo. Sola, la anomalía de
precipitación respecto a 2022–2024 es la que más explica (RMSE 0.584), seguida de la temperatura
mínima (0.603), la precipitación acumulada (0.604) y la temperatura máxima (0.658). 2025 fue más
lluvioso que 2022–2024 en todas las parcelas (anomalía de +202 a +574 mm) y las de mayor anomalía
rinden menos, coherente con exceso de humedad. Con la ubicación fija ninguna variable climática
agrega más de 0.01 t/ha, y dentro del modelo final la temperatura mínima es la que más mueve la
predicción; ambas lecturas están limitadas por la resolución de 5 km del clima.

**Pregunta 3: ¿qué combinación funciona mejor?** Ubicación + relieve + clima + fenología de Planet
(RMSE 0.494 en la ablación), seguida de ubicación + relieve (0.496); la mejor sin ubicación es
índices + clima + relieve (0.538) y la peor, solo relieve (0.754). Sumar Sentinel-2 a Planet no
mejora (0.507–0.520): ambos capturan la misma fenología y Planet, casi diario, la describe mejor.
La combinación óptima es información poca pero complementaria: ubicación para el nivel, relieve y
clima para la zona fina, fenología para la variación interna.

**Discusión.** En esta muestra la predicción espacial domina y los índices afinan en el margen; es
una limitación del dato (138 parcelas, rendimiento comercial con redondeo, 25 píxeles de clima),
no del método. Las predicciones son robustas (desviación entre repeticiones de 0.007 t/ha) pero su
intervalo al 80 % es de ±0.63 t/ha, que la aplicación muestra junto a cada estimación.

## 6. Uso de la ciencia de datos en la inclusión financiera del sector agro [300 palabras]

El crédito de avío a pequeños productores de cebada se decide hoy con información asimétrica: el
intermediario financiero conoce el historial del productor, si existe, pero no el potencial
productivo de la parcela concreta que respaldará el pago. CebadaVision convierte datos públicos
—imágenes satelitales, clima, relieve y la ubicación de la parcela— en una estimación de rendimiento
por parcela con error conocido, disponible sin visita de campo y actualizable cada ciclo. Eso cambia
tres decisiones financieras.

Primero, el dimensionamiento del crédito. Con rendimiento esperado, superficie y precio de referencia
se obtiene el valor esperado de la cosecha y, con el intervalo del modelo, un escenario conservador;
el monto de avío puede ajustarse a lo que la parcela puede pagar, no a un promedio regional. La
aplicación muestra producción estimada en toneladas y un semáforo bajo/medio/alto por terciles,
pensado como primer filtro de riesgo.

Segundo, la inclusión de productores sin historial. Un productor sin expediente crediticio puede
ser evaluado por la evidencia objetiva de su parcela y de sus vecinas; la ubicación, que domina el
modelo, es precisamente información que el productor no puede manipular y que la financiera no
necesita verificar en campo.

Tercero, el diseño de seguros y garantías. El error por zona (0.36 t/ha en Hidalgo y Tlaxcala, 0.58
en Puebla) y la trayectoria del vigor del cultivo durante el ciclo permiten detectar desviaciones
tempranas respecto a lo esperado y activar seguros paramétricos o reestructuras antes de la cosecha.

La condición para que esto sea inclusión y no exclusión es la transparencia: cada estimación se
entrega con su intervalo y con una explicación en lenguaje llano de qué la subió o la bajó, para que
el productor pueda entenderla, cuestionarla y usarla en su propia negociación con la comercializadora
o la financiera.

## 7. Conclusiones [400 palabras]

Se construyó un modelo reproducible que predice el rendimiento de grano de parcelas de cebada de
temporal en Hidalgo, Tlaxcala y Puebla con RMSE de 0.491 ± 0.007 t/ha, MAE de 0.336 y R² de 0.664
en validación cruzada estratificada por estado repetida diez veces, frente a 0.851 de la media y
0.501 de un kNN espacial. El modelo final es un ensamble de LightGBM y Random Forest sobre
ubicación, relieve, clima y fenología de Planet, y entrega las 59 predicciones solicitadas con media
3.95 t/ha y un intervalo al 80 % de ±0.63 t/ha.

El hallazgo principal es estructural: la ubicación de la parcela explica cerca de dos tercios de la
varianza del rendimiento, porque las tres zonas operan en regímenes distintos y porque parcelas
vecinas comparten suelo, clima y manejo. Un modelo que ignore esto subestima su error o atribuye a
los índices satelitales un mérito que pertenece a la geografía. Evaluar las variables dentro de esa
estructura permitió responder las preguntas guía con evidencia comparable: el índice más importante
es EVI de Planet, por su señal en la emergencia y en el secado; la variable climática con mayor
peso es la precipitación del ciclo, en particular su anomalía respecto a 2022–2024; y la mejor
combinación es ubicación + relieve + clima + fenología de Planet; sumar Sentinel-2 no mejora.

Las limitaciones se declaran en la aplicación: rendimiento de origen comercial, con redondeo en una
zona; clima a 5 km con solo 25 valores distintos; 138 parcelas de un solo ciclo; variedad, fecha
de siembra, dosis y siniestros desconocidos. Por ello el aporte de los índices sobre la ubicación
es pequeño, aunque sí mejora la extrapolación a municipios no vistos.

La aplicación CebadaVision ejecuta el modelo en el navegador, muestra las 197 parcelas en un mapa,
permite consultar cada una por identificador, presenta la estimación con intervalo y semáforo,
explica en lenguaje llano cómo se llegó al número y ofrece simulador y descarga del CSV, con
prioridad en el productor.

Como trabajo futuro, el mismo pipeline se extendería a varios ciclos y a rendimientos medidos en
campo, para modelar el residuo dentro de zona con la fenología, estimar antes de la cosecha con
ventanas parciales y calibrar el intervalo por zona. En colaboración con FIRA, el modelo
podría integrarse a la originación de crédito de avío como variable objetiva de capacidad productiva.

## Bibliografía

- Breiman, L. (2001). Random forests. *Machine Learning*, 45(1), 5–32.
- FIRA (2026). *Bases del Reto AgroCebada 2026*. Fideicomisos Instituidos en Relación con la
  Agricultura. https://www.fira.gob.mx/Nd/Convocatoria-2026.html
- Funk, C., Peterson, P., Landsfeld, M., et al. (2015). The climate hazards infrared precipitation
  with stations—a new environmental record for monitoring extremes. *Scientific Data*, 2, 150066.
- Huete, A., Didan, K., Miura, T., Rodriguez, E. P., Gao, X. y Ferreira, L. G. (2002). Overview of the
  radiometric and biophysical performance of the MODIS vegetation indices. *Remote Sensing of
  Environment*, 83(1–2), 195–213.
- Ke, G., Meng, Q., Finley, T., et al. (2017). LightGBM: A highly efficient gradient boosting decision
  tree. *Advances in Neural Information Processing Systems*, 30, 3146–3154.
- Lundberg, S. M. y Lee, S.-I. (2017). A unified approach to interpreting model predictions.
  *Advances in Neural Information Processing Systems*, 30, 4765–4774.
- Pedregosa, F., Varoquaux, G., Gramfort, A., et al. (2011). Scikit-learn: Machine learning in Python.
  *Journal of Machine Learning Research*, 12, 2825–2830.
- Qi, J., Chehbouni, A., Huete, A. R., Kerr, Y. H. y Sorooshian, S. (1994). A modified soil adjusted
  vegetation index. *Remote Sensing of Environment*, 48(2), 119–126.
- Roberts, D. R., Bahn, V., Ciuti, S., et al. (2017). Cross-validation strategies for data with
  temporal, spatial, hierarchical, or phylogenetic structure. *Ecography*, 40(8), 913–929.
- SIAP (2023). *Panorama Agroalimentario 2023*. Servicio de Información Agroalimentaria y Pesquera,
  Secretaría de Agricultura y Desarrollo Rural. https://www.gob.mx/siap
- van Klompenburg, T., Kassahun, A. y Catal, C. (2020). Crop yield prediction using machine learning:
  A systematic literature review. *Computers and Electronics in Agriculture*, 177, 105709.

## Anexos (máx. 4 cuartillas; ver `reports/anexos.md`)

1. Tabla de predicciones de las 59 parcelas (ID_POLIGONO, rendimiento predicho t/ha).
2. Actividades y aportaciones de cada integrante.
3. Registro de uso de inteligencia artificial y prompts (`prompts_ia.md`).
4. Enlace al repositorio y a la aplicación.
