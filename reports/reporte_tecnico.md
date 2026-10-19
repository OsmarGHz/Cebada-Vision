# CebadaVision: predicción del rendimiento de cebada de temporal en Hidalgo, Tlaxcala y Puebla

Reto AgroCebada 2026 (FIRA) · Equipo CebadaVision · Octubre de 2026

## 1. Introducción [400–550 palabras]

La cebada es uno de los cultivos más importantes del sector agroindustrial: es fundamental para la
industria maltera y cervecera y un insumo clave para alimentos y ganado. El rendimiento por hectárea y la calidad del grano determinan la logística, los precios
y la operación de la industria. En México, cerca de tres cuartas partes de la superficie se siembra en el
Altiplano central, casi toda de temporal, y Hidalgo, Puebla y Tlaxcala concentran la mayor parte de
la producción (SIAP, 2023), en manos de pequeños y medianos productores que venden su cosecha a
comercializadoras y parafinancieras.

El cultivo enfrenta desafíos crecientes: el cambio climático altera los patrones de lluvia y
temperatura, las plagas son menos predecibles y los insumos se encarecen. Para los pequeños productores, el monitoreo continuo es difícil. Las imágenes satelitales,
los datos climáticos y el aprendizaje automático permiten estudiar el rendimiento: Sentinel-2
observa cada cinco días a 10 m, Planet casi a diario a 3 m, y los modelos que combinan estas series
con clima y relieve explican buena parte de la variación del rendimiento en cultivos de temporal
(van Klompenburg et al., 2020; de la Fuente et al., 2023).

El Reto AgroCebada 2026 plantea ese problema con datos reales: 197 parcelas de cebada de temporal
del ciclo abril–octubre de 2025 en Hidalgo, Tlaxcala y Puebla, con índices de vegetación de
Sentinel-2, Landsat y Planet, precipitación y temperatura mensuales, elevación y pendiente. El rendimiento de grano (toneladas por hectárea) se conoce para 138 parcelas; el de las
otras 59 lo resguarda el comité para calificar las predicciones. Según la aclaración de FIRA, el rendimiento procede del pesaje en báscula de la cosecha
de cada parcela, sin ajustes por humedad, impurezas o mermas. En Tlaxcala se observa redondeo
a medias toneladas; esto no implica ausencia de medición.

Este trabajo presenta CebadaVision, una solución con tres partes. Primero, una tabla de variables
por parcela que resume cómo se comportó cada índice durante el ciclo (cuándo emergió el cultivo,
cuánto verdor alcanzó, cuánto duró verde y qué tan rápido se secó), más clima, relieve y ubicación. Segundo, un modelo que promedia dos algoritmos de árboles
(LightGBM y Random Forest), validado con un esquema repetido y estratificado por estado, que
alcanza un error (RMSE) de 0.49 t/ha frente a 0.85 t/ha de predecir el promedio regional. Tercero,
una aplicación web que muestra las predicciones precalculadas del ensamble para las 197 parcelas,
su margen orientativo y explicaciones sencillas; su simulador utiliza una regresión Ridge sustituta.

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

Este proyecto estima retrospectivamente el rendimiento mediante evidencia satelital y climática,
con un error medido en validación. La trazabilidad de los datos podría reducir la desigualdad de
información en la cadena de valor y apoyar la evaluación financiera, aunque ese beneficio requiere
validación operativa. El reto aporta además un caso poco común: datos reales de
197 parcelas y 138 rendimientos conocidos obtenidos por pesaje en báscula. Resolverlo con rigor —validación reproducible
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
4. Implementar una aplicación que muestre las predicciones precalculadas del ensamble con margen
   orientativo y explicación por parcela, distinga el simulador Ridge sustituto y discuta su posible
   uso en inclusión financiera.

## 4. Metodología [600–700 palabras]

**Datos.** Se utilizó únicamente el dataset oficial: 197 polígonos (138 de entrenamiento y 59 por
predecir), 47 804 observaciones de Planet (NDVI, EVI, LAI, MSAVI) de 2025, 107 666 de Sentinel-2 y
Landsat de 2022 a 2025 (22 índices), rásteres mensuales de precipitación (CHIRPS) y de temperatura
mínima y máxima a unos 5 km, y elevación y pendiente del Continuo de Elevaciones Mexicano. La auditoría confirmó identificadores únicos, unión sin pérdidas y reparto 138/59. Se trabajó con el ciclo abril–octubre de 2025 (más
noviembre, para capturar la senescencia). Las observaciones con nubosidad del 100 % se descartaron
porque traen los índices vacíos; no se imputó ninguna. Landsat no aporta índices en 2025.

**Variables.** Para cada parcela e índice se tomó la serie del promedio del polígono, se suavizó
con una mediana móvil de tres observaciones y se calcularon: mediana de cada mes de abril
a noviembre, medianas por ventana (mayo–junio, julio–septiembre, octubre–noviembre), valor y fecha
del máximo, amplitud, área bajo la curva de abril a octubre, inicio y fin de la temporada verde
(cruce de media amplitud), duración y velocidades de
crecimiento y de secado. Resultaron 80 variables de Planet y 160 de Sentinel-2 (NDVI, EVI, SAVI,
LAI, fAPAR, NDWI, MSI, NDTI). El clima se resumió en lluvia acumulada abril–octubre, temperaturas
mínima y máxima medias del ciclo y anomalía de lluvia respecto al promedio 2022–2024; por la
resolución del ráster, estas variables solo toman 25 valores distintos en las 197 parcelas. El
relieve aporta elevación media, su variación y pendiente media. La ubicación se representó con las
coordenadas del centroide (km), la zona (k-means de tres grupos sobre los centroides, sin usar el
rendimiento), el rendimiento promedio de la zona y el promedio ponderado por distancia del
rendimiento de las ocho parcelas de entrenamiento más cercanas.

**Validación.** El equipo prioriza RMSE, junto con MAE y R², considerados por FIRA. Se usó
validación cruzada de 5 particiones estratificadas por estado —mantiene representación estatal, con proporción 80/20 por partición— repetida 10 veces; se
reporta promedio y desviación entre repeticiones, y diferencias de RMSE menores a 0.03 t/ha se interpretan con cautela, sin prueba de significancia. Como prueba más exigente se añadió una validación agrupada por municipio.
Las variables de vecinos y zona se recalculan dentro de cada partición usando únicamente
sus rendimientos de entrenamiento; al construir las variables de una parcela de entrenamiento
se excluye su propio rendimiento. Los rendimientos de validación no intervienen.

**Modelos.** Se compararon regresión ridge, Random Forest (400 árboles, hoja mínima de 3, 33 % de
variables por partición), un LightGBM pequeño (300 árboles, tasa 0.03, 7 hojas, submuestreo,
regularización L2) y un proceso gaussiano con núcleo RBF más ruido; los faltantes se rellenan con
la mediana de entrenamiento dentro de cada ajuste. El banco de experimentos evaluó cada grupo de
variables por separado, la ubicación más cada grupo, combinaciones completas y ensambles. Para las preguntas guía se evaluó cada índice con sus variables fenológicas y cada
variable climática, solos y con la ubicación fija, y se calcularon importancia por permutación sobre entrenamiento (aumento del RMSE al barajar
cada variable) y ablación por grupos con tres repeticiones.

**Modelo final.** Promedio de LightGBM con ubicación, relieve y clima (11 variables) y Random
Forest con ubicación, fenología de Planet, clima y relieve (91 variables). La predicción se
recorta a 1.5–6.5 t/ha. El margen orientativo es ±1.2816 × RMSE, aproximadamente ±0.63 t/ha;
su cobertura del 80 % no está calibrada ni verificada empíricamente. Se calculan valores SHAP
(Lundberg y Lee, 2017), promediados entre modelos y agrupados por tipo de variable, para explicar
las estimaciones precalculadas que muestran el mapa y las fichas. El navegador ejecuta únicamente
el simulador Ridge sustituto de 11 variables, ajustado a las predicciones del ensamble sobre
las 197 parcelas. Su discrepancia RMSE de 0.3161 t/ha se mide en esos mismos datos; no es una
validación independiente contra rendimientos reales ni evidencia causal.

**Implementación.** Python 3.13 (pandas, geopandas, rasterio, scikit-learn, LightGBM, SHAP);
aplicación en React, TypeScript, Leaflet y Recharts.

## 5. Resultados y discusión [800 palabras]

**Puntos de referencia.** Predecir el promedio de entrenamiento da RMSE 0.851 t/ha (R² −0.02).
Un kNN espacial que solo usa las ocho parcelas vecinas baja a 0.501 (R² 0.65): la ubicación por
sí sola explica cerca de dos tercios de la variación y constituye la referencia espacial.

**Cada grupo de variables por separado** (CV 5×10, LightGBM). Solo coordenadas: 0.507; solo
vecinos: 0.502; solo clima: 0.545; solo fenología de Planet: 0.625; solo Sentinel-2: 0.636; solo
estadísticos simples de Planet (media, desviación, máximo, mínimo): 0.784; solo relieve: 0.762.
La fenología completa vale mucho más que los estadísticos simples, porque la señal agronómica está
al inicio del ciclo y en el secado, no en el máximo, que se satura en agosto–septiembre. El clima
predice bien pese a tomar solo 25 valores distintos: opera, en la práctica, como indicador de zona.

**Ubicación más cada grupo.** Sumar a la ubicación los índices de Planet, Sentinel-2 o el clima deja
el RMSE entre 0.500 y 0.515; sumar relieve lo lleva a 0.492. Ningún grupo aporta más de 0.01–0.02
t/ha una vez conocida la ubicación: la correlación de cualquier variable satelital con lo que el kNN
no explica no pasa de |ρ| = 0.17. Las 138 parcelas, el redondeo observado en Tlaxcala y el clima de baja resolución
limitan la interpretación de mejoras pequeñas. Los modelos lineales empeoran al
agregar variables (ridge con 251 variables: 0.567); los de árboles se mantienen.

**Modelo final.** El ensamble LightGBM (ubicación, relieve, clima) + Random Forest (ubicación,
fenología Planet, clima, relieve) obtiene RMSE 0.491 ± 0.007, MAE 0.336 y R² 0.664. La diferencia frente al kNN es 0.010 t/ha, menor que el umbral orientativo de 0.03:
no demuestra superioridad estadística. En validación por municipio obtiene RMSE 0.574 frente a
0.708 del kNN; es evidencia favorable dentro de esta muestra, sin garantizar generalización
a otras regiones o ciclos. Por estado (predicciones fuera de fold promediadas), RMSE/R² son
0.357/0.784 en Hidalgo (n=36), 0.578/0.007 en Puebla (n=71) y 0.375/−0.026 en Tlaxcala (n=31).
El desempeño global no se reproduce dentro de Puebla y Tlaxcala: se explica muy poca variación
interna y, en Tlaxcala, no se supera su media estatal según R². Las 59 predicciones tienen promedio 3.95 t/ha y van de 2.88 a
4.65, en línea con el entrenamiento: 4.47 en Puebla, 3.79 en Hidalgo y 3.00 en Tlaxcala. Frente al Ridge provisional de nueve variables (0.551), la reducción observada es 0.06 t/ha;
frente al promedio, 0.36. Aquel Ridge es distinto del sustituto usado por el simulador.

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
mejor. La combinación con menor error observado reúne información complementaria; su ventaja
requiere confirmación en muestras independientes.

**Discusión.** La predicción espacial domina; no puede atribuirse esta limitación exclusivamente
al dato o al método. La desviación de 0.007 t/ha describe el RMSE entre repeticiones, no la
incertidumbre de cada parcela. El margen ±0.63 t/ha es orientativo: no tiene cobertura del 80 %
calibrada. El uso de información hasta noviembre hace retrospectivo este análisis.

## 6. Uso de la ciencia de datos en la inclusión financiera del sector agro [300 palabras]

El crédito de avío requiere información sobre la capacidad productiva de la parcela y la situación
del productor. CebadaVision aporta una estimación retrospectiva del ciclo 2025 con error medido
en validación. Puede servir como evidencia complementaria para estudiar aplicaciones financieras;
no se ha validado como sistema de decisión crediticia, de seguros ni de alerta temprana.

Una primera aplicación potencial es explorar escenarios de valor de cosecha combinando rendimiento,
superficie y precio de referencia. El margen orientativo del modelo permite ilustrar sensibilidad,
pero no constituye una pérdida máxima ni una garantía de pago. Los terciles bajo/medio/alto de la
aplicación clasifican rendimiento, no probabilidad de incumplimiento.

Una segunda posibilidad es complementar la evaluación de productores sin historial crediticio con
información trazable de sus parcelas. Debe comprobarse que el uso de la ubicación no reproduzca
desventajas territoriales: el R² global oculta diferencias importantes de desempeño entre estados.
La estimación no sustituye la verificación de identidad, manejo, costos u otras condiciones del
productor, ni justifica por sí sola otorgar o rechazar crédito.

El estudio utiliza observaciones hasta noviembre de 2025. Por tanto, detectar desviaciones y activar
seguros o reestructuras antes de la cosecha son aplicaciones futuras: requieren fijar una fecha de
corte, reconstruir únicamente las variables disponibles entonces y validar con ciclos independientes.
Actualizar el sistema cada ciclo también exige datos nuevos, evaluación de cambios y recalibración;
esa capacidad no está demostrada aquí.

La transparencia implica distinguir las predicciones del ensamble de las simulaciones Ridge,
explicar las limitaciones del margen y permitir que productores y analistas cuestionen los resultados.
Una prueba operativa con FIRA podría evaluar utilidad, equidad y desempeño antes de su adopción.

## 7. Conclusiones [400 palabras]

Se construyó un modelo reproducible de rendimiento de grano de cebada de temporal en Hidalgo,
Tlaxcala y Puebla. En validación cruzada estratificada por estado y repetida diez veces obtuvo
RMSE 0.491 ± 0.007 t/ha, MAE 0.336 y R² 0.664. El ensamble de LightGBM y Random Forest
entrega las 59 predicciones solicitadas, con promedio 3.95 t/ha. Frente al kNN espacial (0.501),
la reducción observada de 0.010 t/ha es pequeña y no demuestra superioridad estadística;
sí es amplia frente al promedio regional (0.851). El margen ±0.63 t/ha es orientativo,
sin cobertura del 80 % calibrada.

La ubicación concentra gran parte de la señal predictiva. Evaluar los demás grupos dentro de esa
estructura permitió responder las preguntas guía: EVI de Planet destaca entre los índices;
la precipitación y su anomalía respecto a 2022–2024 destacan al evaluar clima por separado;
y ubicación, relieve, clima y fenología de Planet ofrecen la combinación con menor error observado
en la ablación. Estas asociaciones no prueban efectos causales del manejo o del clima.

El desempeño varía por estado. Los R² de 0.784 en Hidalgo, 0.007 en Puebla y −0.026 en Tlaxcala
impiden extender la interpretación del R² global a todas las parcelas. La validación por municipio
es favorable en esta muestra, pero no demuestra desempeño en regiones o ciclos nuevos.

Las limitaciones incluyen 138 rendimientos conocidos de un solo ciclo, pesaje en báscula sin
ajustes por humedad, impurezas o mermas, redondeo en Tlaxcala, clima a unos 5 km y ausencia de
información de manejo. Se requieren más ciclos y documentación de la calidad del pesaje.

La aplicación muestra predicciones y explicaciones precalculadas del ensamble. Su simulador ejecuta
una regresión Ridge sustituta cuya discrepancia de ajuste frente al ensamble es 0.3161 t/ha;
no tiene el mismo desempeño validado ni representa intervenciones causales.

Como siguiente paso se propone calibrar la incertidumbre y evaluar predicción anticipada con
fechas de corte explícitas y datos disponibles en cada fecha. El análisis actual usa observaciones
hasta noviembre de 2025: las alertas precosecha, la actualización por ciclo y la incorporación
a decisiones financieras requieren validación temporal y operativa adicional.

## Bibliografía

- Breiman, L. (2001). Random forests. *Machine Learning*, 45(1), 5–32.
- de la Fuente, D., Rivilla, E., Tena, A., Vitorino, J., Navascués, E. y Tabasco, A. (2023). Yield
  estimation using machine learning from satellite imagery.
  *BIO Web of Conferences*, 68, 01013 (44th World Congress of Vine and Wine).
  https://doi.org/10.1051/bioconf/20236801013
- FIRA (2026). *Bases del Reto AgroCebada 2026*. Fideicomisos Instituidos en Relación con la
  Agricultura. https://www.fira.gob.mx/Nd/Convocatoria-2026.html
- FIRA (2026). *Ecuaciones de los índices de vegetación, Reto AgroCebada 2026*.
  Documento técnico proporcionado por el Comité Organizador, pp. 1–2.
- FIRA (2026). *Lineamientos y Guía de Registro de Proyectos, Reto AgroCebada FIRA 2026*.
  Guía proporcionada a los equipos, pp. 2–4.
- FIRA (2026). *Preguntas y respuestas adicionales*. Documento de apoyo para integrantes
  del jurado, pp. 1–3; preguntas 1–8.
- FIRA (2026, 9 de octubre). *Segunda sesión de preguntas y respuestas*.
  Documento de apoyo para integrantes del jurado, pp. 1–2.
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

### Uso de inteligencia artificial generativa — pendiente de completar

La guía de registro de FIRA (p. 4, apartado Bibliografía) solicita los prompts utilizados,
el propósito de cada uno y la herramienta empleada. Esta relación no sustituye las referencias
bibliográficas, técnicas o de datos.

Falta incorporar los registros reales de cada integrante, con el texto de cada prompt,
su propósito y la herramienta utilizada; indicar también el integrante y la actividad o archivo
correspondiente para facilitar su revisión. No se han reconstruido ni inventado registros.
Este apartado debe completarse y aprobarse antes de entregar el PDF de Bibliografía.

## Anexos (máx. 4 cuartillas; ver `reports/anexos_final.md`)

1. Tabla de predicciones de las 59 parcelas (ID_POLIGONO, rendimiento predicho t/ha).
2. Actividades y aportaciones de cada integrante.
3. Enlaces al repositorio y a la aplicación.
4. Referencia al registro de uso de IA en Bibliografía (pendiente de integrar).
