# Registro de IA

| Fecha | Herramienta | Integrante | Uso (sección / archivo) | Prompt |
|---|---|---|---|---|
| 2026-09-17 | Claude Code | David | `CLAUDE.md` | "lee las bases del reto y con lo leido, arma el contexto del proyecto en un archivo `CLAUDE.md`, y asi el asistente conserve el objetivo, las reglas y la estrategia en cada sesión de trabajo." |
| 2026-09-17 | Claude Code | David | Documento de contexto | "Genera un .md independiente con el contexto del reto, con el fin de que cualquier integrante del equipo pueda consultarlo sin leer las bases completas." |
| 2026-09-17 | Claude Code | David | Checklist de estado | "agrega un checklist de lo que ya está hecho y lo que falta y darme seguimiento al avance hacia la fecha límite." |
| 2026-09-18 | Claude Code | David | planeacion | "dime qué sigue y en qué orden (dataset, EDA, baseline, variables, validación, app, reporte), para que me pueda planear el trabajo de las semanas restantes." |
| 2026-09-18 | Claude Code | David | Estructura de carpetas | "define la estructura de carpetas del proyecto (`data`, `src`, `notebooks`, `app`, `reports`, `submissions`), para mantener el código y los datos ordenados y reproducibles." |
| 2026-09-18 | Claude Code | David | Revisión del dataset | "Ya está el dataset: inspecciona qué contiene cada archivo (rendimiento, Sentinel, Landsat, Planet, shapefile, TIF), y explicame detalladamente como si fuera un burro para entender que variables hay y cmo se relacionan." |
| 2026-09-18 | Claude Code | David | `reports/eda_hallazgos.md` | "Deja por escrito los hallazgos del EDA para que mi equipo y el reporte técnico puedan usarlos como respaldo." |
| 2026-10-02 | Claude Code | David | `src/tabla_pro.py`, `variables_pro_abr_oct_2025.csv` | "Deja una fila por parcela con las variables de PRO para entregar una tabla lista para el baseline del compañero de modelado." |
| 2026-10-02 | Claude Code | David | Verificación | "verifica que no se perdieron parcelas ni IDs en la tabla t asegurar que la unión de fuentes es correcta." |
| 2026-10-11 | Claude Code | David | README, `requirements.txt` | "Haz el repositorio reproducible con un README del orden de ejecución y versiones fijas de las librerías, con el fin de que cualquier persona pueda regenerar los resultados." |
| 2026-10-17 | Claude Code | David | `src/features.py` | "crea variables fenológicas (pico, fecha del pico, área bajo la curva, duración) de Planet y Sentinel-2 junto con la ubicación" |
| 2026-10-17 | Claude Code | David | `src/modelar.py`, `reports/experimentos.md` | "Arma la validación cruzada repetida y por municipio, con vecinos calculados dentro de cada fold, y un banco de experimentos, para asi comparar modelos sin fuga de información." |
| 2026-10-17 | Claude Code | David | `src/exportar_app.py` | "pasa los resultados del modelo final a la app" |
| 2026-09-30 a 2026-10-06 | Claude (claude.ai) | Osmar | Seguimiento de issues del equipo, revisión del borrador de Isaac, verificación de scripts de Boni, baseline de Hugo, actualización de `contexto_proyecto.md` y `DECISIONES.md` | Chat compartido: "Por ahora te vas a encargar de checar el progreso de la parte de Isaac…", "qué me tocaría actualizar? Toca crear nuevas issues…", "como estaria eso de los prompts?", "Isaac ya hizo su parte…", "cuando alguien termine lo de una issue suya, qué tendría que reportar…", "Olvidé pasarte los archivos de boni", "Me puso Lucy…", "te paso el md de decisiones y el md de contexto… actualízalos" |
