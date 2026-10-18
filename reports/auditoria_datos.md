# Auditoría de datos — frente Datos (30-sep-2026)

Script: `src/auditoria_datos.py`. Salida: `data/processed/auditoria_union_4fuentes.csv`.

## Objetivo

Confirmar que shapefile, CSV de rendimiento, BASICO y PRO se pueden unir sin perder ni duplicar
parcelas, antes de construir la tabla de variables.

## Confirmación pedida

- **197 IDs únicos en las 4 fuentes**: shapefile, CSV rendimiento, BASICO, PRO → confirmado, 0
  faltantes / 0 sobrantes en cada una respecto al CSV de rendimiento.
- **138 ENTRENAMIENTO con rendimiento, 59 PREDICCION sin rendimiento** → confirmado exacto
  (crosstab `CONJUNTO` × `rendimiento_nulo`: ENTRENAMIENTO 138/0, PREDICCION 0/59).
- **Unión de las 4 fuentes**: 197 filas, 0 duplicados de `ID_POLIGONO`, 0 `left_only`/`right_only`
  en el join CSV rendimiento ↔ shapefile, y las 197 parcelas del CSV están presentes en BASICO y
  en PRO.

**No hay bloqueos.** Nada que reportar como ID faltante, duplicado o fecha rota.

## Salida completa de `auditoria_datos.py`

```
== Fechas: rango y formato ==
BASICO: 2022-01-01 -> 2025-12-31, nulos tras parseo: 0
PRO: 2025-01-01 -> 2025-12-30, nulos tras parseo: 0

== Auditoria de IDs por fuente ==
                        fuente  n_ids_unicos id_duplicado_indebido
ID_area_rendimiento (objetivo)           197                 False
            Shapefile parcelas           197                 False
     BASICO (Sentinel/Landsat)           197                  None
                  PRO (Planet)           197                  None
             Clima (procesado)           197                  None
        Topografia (procesada)           197                 False
(id_duplicado_indebido = None para tablas largas por diseno: BASICO/PRO por fecha, clima por mes)

== Confirmacion split CONJUNTO / rendimiento ==
CONJUNTO
ENTRENAMIENTO    138
PREDICCION        59
rendimiento_nulo  False  True
CONJUNTO
ENTRENAMIENTO       138      0
PREDICCION            0     59
split 138 ENTRENAMIENTO con rendimiento / 59 PREDICCION sin rendimiento: True

== Prueba de union: shapefile + CSV rendimiento + BASICO + PRO (ID_POLIGON -> ID_POLIGONO) ==
resultado_union_shp   n
               both 197
          left_only   0
         right_only   0
filas con CONJUNTO distinto entre CSV rendimiento y shapefile: 0

   fuente  presentes  faltantes_de_197
shapefile        197                 0
   BASICO        197                 0
      PRO        197                 0
total parcelas tras union (base = CSV rendimiento): 197 (esperado: 197)
duplicados de ID_POLIGONO tras union: 0 (esperado: 0)

Tabla de union guardada en D:\AgroCebada\data\processed\auditoria_union_4fuentes.csv

== Tabla PRO: una fila por parcela, agregada abr-oct 2025 ==
parcelas: 197 (esperado: 197)
nulos por columna: 0 en todas las columnas
Tabla PRO guardada en D:\AgroCebada\data\processed\variables_pro_abr_oct_2025.csv
```

## Unión `ID_POLIGON` (shapefile) ↔ `ID_POLIGONO` (resto de tablas)

- El shapefile trunca el nombre del campo a 10 caracteres (`ID_POLIGON`) por límite del formato
  `.dbf`. El valor del ID en sí **no** está truncado (sigue siendo `AGC_0XX`), solo el nombre de
  columna.
- CSV rendimiento, BASICO y PRO ya usan `ID_POLIGONO` completo.
- Corrección: `shp.rename(columns={"ID_POLIGON": "ID_POLIGONO"})` antes de cualquier unión.

## Otros hallazgos de limpieza (no bloqueos)

- Columna `Unnamed: 4` (vacía) en `ID_area_rendimiento_70_30…csv` — se descarta con
  `dropna(axis=1, how="all")`.
- Campo de área en el shapefile viene mal codificado (`�rea_ha`) si se lee sin `encoding="latin1"`;
  con ese encoding se lee correctamente como `área_ha`.
- `Cultivo` tiene dos grafías (`CEBADA` / `Cebada`) según zona — no afecta el join, solo hay que
  normalizar si se usa como feature categórica (ver `reports/eda_hallazgos.md`).

## Tabla PRO agregada (bonus del issue)

`data/processed/variables_pro_abr_oct_2025.csv` — una fila por parcela (197/197, 0 nulos), con
`ndvi/evi/lai/msavi_promedio` (mean/std/max/min) y `n_obs_validas`, agregados sobre observaciones
Planet de abr–oct 2025 con `porcentaje_nubosidad < 100` (nubosidad 100 → índices vacíos, se
excluyen antes de agregar). Rango de `n_obs_validas` por parcela: 125–139 antes del filtro de
nubes.

## Conclusión

Unión de las 4 fuentes (shapefile, CSV rendimiento, BASICO, PRO) validada: sin parcelas perdidas,
sin duplicados, split 138/59 exacto. Listo para construir la tabla de variables.
