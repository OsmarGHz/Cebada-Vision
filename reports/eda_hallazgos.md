# EDA — Hallazgos (18-sep-2026)

Scripts: `src/eda_01_estructura.py`, `src/eda_02_relaciones.py`, `src/eda_03_zonas.py`,
`src/extraer_raster.py`. Figuras en `reports/figuras/`.

## Datos

| Insumo | Contenido | Notas |
|---|---|---|
| `ID_area_rendimiento_70_30…csv` | 197 parcelas: 138 ENTRENAMIENTO, 59 PREDICCION | Rendimiento = ciclo abr–oct 2025 |
| Shapefile | Polígonos, `Municipio`, `Estado`, `Cultivo`, `CONJUNTO` | Campo ID truncado a `ID_POLIGON`; EPSG:4326 |
| BASICO | 107,666 filas, 2022–2025. Sentinel-2 (22 índices) y Landsat (solo VI6T) en filas separadas | ~66 obs S2 por parcela mar–nov 2025 |
| PRO (Planet) | 47,804 filas, 2025. NDVI, EVI, LAI, MSAVI | ~177 obs por parcela mar–nov 2025 |
| Clima | Prec, Tmin, Tmax mensuales 2022–2025, píxel ~5 km | Solo **25 píxeles distintos** cubren las 197 parcelas |
| Topografía | Elevación y pendiente 120 m | 2,497–2,905 m s.n.m.; pendiente media 0.3–8.9° |

- Nubosidad es casi binaria: 0 % (mayoría) o 100 % (índices vacíos). Filtro natural: nubosidad < 100 (o ≤ 20).
- Sin duplicados parcela-fecha-sensor.

## Objetivo (rendimiento t/ha, n = 138)

- Media 3.96, DE 0.85, rango 2.00–5.59. Distribución bimodal (~3.0 y ~4.5).
- Solo 67 valores únicos; 3.0, 3.5 y 2.5 concentran 43 parcelas.
- Área de parcela: 0.35–64 ha; correlación débil negativa con rendimiento (ρ = −0.25).

## Hallazgo 1 — Tres zonas con regímenes distintos

| Zona | Municipios principales | Train / Pred | Media | DE | % valores múltiplos de 0.5 |
|---|---|---|---|---|---|
| 0 (este, Puebla) | Chignahuapan, Almoloya, Cuautepec | 85 / 37 | **4.49** | 0.54 | 1 % |
| 1 (suroeste, Tlaxcala) | Calpulalpan, Apan, Emiliano Zapata | 35 / 15 | **3.03** | 0.38 | **100 %** |
| 2 (norte, Hidalgo) | Singuilucan, Cuautepec | 18 / 7 | **3.25** | 0.63 | 50 % |

- La zona 1 reporta rendimientos redondeados (2.5 / 3.0 / 3.5): probablemente estimación del
  productor, no medición. Su variación interna es mayormente ruido de redondeo.
- El campo `Cultivo` difiere por zona ("CEBADA" vs "Cebada"): distinta fuente de captura.
- El reparto 70/30 está estratificado: PREDICCION replica la proporción de zonas.

## Hallazgo 2 — Fuerte dependencia espacial

- Correlación del rendimiento con el de su vecino más cercano: **0.80**.
- Parcelas de PREDICCION están a una mediana de **0.35 km** de una de entrenamiento (máx 1.9 km).
- Baselines (CV 5-fold × 10):

| Modelo | RMSE | R² |
|---|---|---|
| Media global | 0.855 | −0.02 |
| Media por zona | 0.525 | 0.62 |
| Media por municipio | 0.514 | 0.63 |
| kNN espacial (k = 8) | **0.507** | **0.64** |

**Implicación:** la ubicación explica ~63 % de la varianza. El valor del modelo está en explicar
la variación *dentro* de zona (DE 0.4–0.6) con índices satelitales. Todo modelo debe superar
RMSE 0.507.

## Hallazgo 3 — Fenología y señal satelital

- Temporada visible en índices: suelo desnudo hasta mayo, emergencia **finales de mayo–junio**,
  pico **agosto–septiembre**, senescencia **octubre–noviembre**.
- Tercil bajo: emerge más tarde y senesce antes (menor duración de ciclo verde).
- Correlación (Spearman) rendimiento vs mediana mensual:
  - EVI / SAVI / LAI (S2) en mayo–junio: **0.5–0.6**; en jul–sep: **~0** (saturación del dosel).
  - Oct–nov: 0.35–0.45 (senescencia tardía = más rendimiento).
  - MSAVI / EVI Planet en mayo: ~0.6.
  - Índices de agua (NDWI, MSI) débiles salvo oct–nov.
  - Correlaciones de ene–mar (antes de siembra) también positivas → capturan la zona, no el
    cultivo. Hay que evaluar señal dentro de zona para evitar confusión.

## Hallazgo 4 — Clima y topografía

- Clima 2025: Tmin (ρ = +0.54), precipitación (ρ = −0.38), Tmax (ρ = −0.40). Con solo 25 píxeles,
  el clima actúa principalmente como proxy de ubicación; difícil separar efecto causal.
- Elevación (ρ = +0.25) y pendiente (ρ = +0.24): efecto débil, también ligado a zona.

## Implicaciones para el modelado

1. **Validación:** CV aleatoria estratificada por zona (réplica del split oficial) como métrica
   principal; CV agrupada por zona como prueba de robustez.
2. **Features espaciales:** zona / municipio, coordenadas, media de vecinos de entrenamiento
   (fuera de fold, para evitar fuga).
3. **Features fenológicas:** fecha de emergencia, pico, fin de ciclo, duración, AUC de EVI/SAVI/LAI,
   valores en ventanas (mayo–jun, jul–sep, oct–nov). Suavizar series (S2 + Planet por separado).
4. **Modelo por residuo:** predecir desviación respecto a la media de zona/vecinos.
5. **Preguntas guía:** medir importancia *dentro de zona* para no confundir índice con ubicación.
6. **Duda para el comité:** origen del redondeo en Tlaxcala (¿estimación del productor?).
