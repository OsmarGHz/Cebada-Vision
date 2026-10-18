# CebadaVision — ideas para subir puntos de la app (30 % de la Etapa 1)

## Decisión: NO hacer app nueva ni usar Power BI

- La web ya existe en `agrocebada-pagina/` (React + Vite + Leaflet + Recharts). Ya tiene mapa,
  modo Productor / Analista, simulador, carga CSV por lote, páginas Resumen / Parcela / Modelo /
  Acerca. **Se complementa, no se reemplaza.**
- No es app móvil nativa. Es web responsive; si se quiere "sentir app", agregar PWA (instalable).
- Power BI: no ejecuta el modelo y no se despliega fácil. Las bases piden una app que *ejecute* el
  modelo. Descartado.

## Nombre

- **CebadaVision** (el repo de modelación ya se llama `Cebada-Vision`).
- Slogan: *"Ver la cosecha antes de que llegue"*.
- Alternativas: AgroVista, SurcoVisión, Cebada Sentinel.
- Aplicarlo: título del `<title>`, encabezado, favicon, README, reporte, video.

## Ideas ordenadas por retorno / esfuerzo

### Alto retorno, poco esfuerzo
1. Mapa con parcelas coloreadas por rendimiento predicho + ficha al hacer clic. *(ya existe; pulir)*
2. Predicción con **intervalo** (ej. 3.8 t/ha, rango 3.3–4.3) en barra visual.
3. **Nota en lenguaje llano** por parcela (FIRA lo pidió): "Rinde más que el promedio por buena
   vegetación en julio, pero la lluvia fue baja".
4. **Semáforo de riesgo crediticio** según rendimiento esperado vs. punto de equilibrio. Conecta
   con inclusión financiera (Etapa 2).
5. **Explicación SHAP por parcela** (cascada). Responde preguntas bonus.

### Diferenciadores
6. Línea de tiempo NDVI de la parcela con el pico fenológico marcado.
7. Simulador "¿y si?": sliders de lluvia / temperatura. *(ya hay simulador; ligarlo al modelo final)*
8. Comparador de zonas (Puebla, Tlaxcala, Hidalgo) con boxplots.
9. Página **Preguntas guía** (bonus): índice más importante, variable climática de mayor peso,
   mejor combinación; con importancia por permutación y ablación por grupos.
10. **Calculadora de crédito**: costo/ha + precio/t → probabilidad de cubrir el crédito usando el
    intervalo del modelo.

### Presentación
11. Tema verde-dorado, logo simple, tarjetas KPI arriba (RMSE, R², nº parcelas).
12. Pestaña "Metodología" con diagrama del pipeline.
13. Botón **descargar CSV** de predicciones.
14. Despliegue público (Vercel / Netlify / GitHub Pages; es sitio estático) → enlace para el jurado.
15. PWA instalable (opcional).

## Plan mínimo (2 días)

Hacer: 1, 2, 3, 4, 5, 9, 13, 14 + renombrar a CebadaVision. El resto es opcional.

**Prioridad real:** el modelo pesa 70 %. No sacrificarlo por adornos. Los datos de la web siguen
con Ridge provisional; reexportar con `src/exportar_app.py` cuando el modelo final esté listo.
