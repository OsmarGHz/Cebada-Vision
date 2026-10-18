# Banco de experimentos
Validación principal: 5 folds estratificados por estado × 10 repeticiones (RMSE promedio entre repeticiones; `rmse_sd` = desviación entre repeticiones). `rmse_municipio`: CV agrupada por municipio (prueba espacial más exigente: ninguna parcela se evalúa con vecinas de su municipio en entrenamiento). Las variables de vecinos (kNN k=8 ponderado por distancia, media de zona) se calculan dentro de cada fold. Diferencias de RMSE menores a ~0.03 están dentro del ruido.

## Referencias
| experimento        | modelo   |   n_vars |   rmse |   rmse_sd |   mae |     r2 |   rmse_municipio |
|:-------------------|:---------|---------:|-------:|----------:|------:|-------:|-----------------:|
| media global (V0)  | -        |        0 |  0.851 |     0     | 0.751 | -0.018 |          nan     |
| kNN espacial (k=8) | knn      |        1 |  0.501 |     0.009 | 0.362 |  0.651 |            0.708 |

## A. Cada grupo de variables por separado
| experimento       | modelo   |   n_vars |   rmse |   rmse_sd |   mae |    r2 |   rmse_municipio |
|:------------------|:---------|---------:|-------:|----------:|------:|------:|-----------------:|
| solo xy           | ridge    |        2 |  0.532 |     0.003 | 0.383 | 0.607 |            0.7   |
| solo xy           | lgbm     |        2 |  0.507 |     0.011 | 0.37  | 0.643 |            0.625 |
| solo vecinos      | ridge    |        2 |  0.504 |     0.013 | 0.354 | 0.646 |            0.71  |
| solo vecinos      | lgbm     |        2 |  0.502 |     0.012 | 0.346 | 0.649 |            0.552 |
| solo planet_stats | ridge    |       16 |  0.773 |     0.014 | 0.618 | 0.169 |            1.155 |
| solo planet_stats | lgbm     |       16 |  0.784 |     0.026 | 0.617 | 0.145 |            1.177 |
| solo planet_feno  | ridge    |       80 |  0.66  |     0.064 | 0.496 | 0.389 |            0.955 |
| solo planet_feno  | lgbm     |       80 |  0.625 |     0.014 | 0.472 | 0.457 |            0.913 |
| solo feno_core    | ridge    |       40 |  0.643 |     0.021 | 0.491 | 0.424 |            0.926 |
| solo feno_core    | lgbm     |       40 |  0.62  |     0.012 | 0.46  | 0.465 |            0.928 |
| solo s2           | ridge    |      160 |  0.657 |     0.018 | 0.506 | 0.4   |            0.92  |
| solo s2           | lgbm     |      160 |  0.636 |     0.014 | 0.472 | 0.437 |            0.968 |
| solo clima        | ridge    |        4 |  0.545 |     0.003 | 0.407 | 0.587 |            0.924 |
| solo clima        | lgbm     |        4 |  0.545 |     0.007 | 0.38  | 0.588 |            0.671 |
| solo relieve      | ridge    |        3 |  0.787 |     0.005 | 0.667 | 0.138 |            1.131 |
| solo relieve      | lgbm     |        3 |  0.762 |     0.024 | 0.596 | 0.192 |            1.061 |
| solo xy           | gpr      |        2 |  0.51  |     0.005 | 0.353 | 0.638 |            0.723 |

## B. Ubicación + cada grupo
| experimento              | modelo   |   n_vars |   rmse |   rmse_sd |   mae |    r2 |   rmse_municipio |
|:-------------------------|:---------|---------:|-------:|----------:|------:|------:|-----------------:|
| ubicacion + planet_stats | ridge    |       20 |  0.517 |     0.011 | 0.362 | 0.628 |            0.684 |
| ubicacion + planet_stats | lgbm     |       20 |  0.51  |     0.007 | 0.347 | 0.638 |            0.549 |
| ubicacion + planet_feno  | ridge    |       84 |  0.536 |     0.016 | 0.387 | 0.6   |            0.669 |
| ubicacion + planet_feno  | lgbm     |       84 |  0.506 |     0.009 | 0.344 | 0.644 |            0.633 |
| ubicacion + feno_core    | ridge    |       44 |  0.515 |     0.009 | 0.368 | 0.631 |            0.661 |
| ubicacion + feno_core    | lgbm     |       44 |  0.506 |     0.012 | 0.345 | 0.644 |            0.546 |
| ubicacion + s2           | ridge    |      164 |  0.578 |     0.016 | 0.427 | 0.535 |            0.746 |
| ubicacion + s2           | lgbm     |      164 |  0.515 |     0.008 | 0.355 | 0.632 |            0.554 |
| ubicacion + clima        | ridge    |        8 |  0.511 |     0.007 | 0.368 | 0.636 |            0.692 |
| ubicacion + clima        | lgbm     |        8 |  0.5   |     0.009 | 0.342 | 0.652 |            0.578 |
| ubicacion + relieve      | ridge    |        7 |  0.515 |     0.031 | 0.369 | 0.629 |            0.694 |
| ubicacion + relieve      | lgbm     |        7 |  0.492 |     0.011 | 0.343 | 0.663 |            0.543 |
| ubicacion + feno_core    | gpr      |       44 |  0.516 |     0.012 | 0.367 | 0.63  |            0.711 |
| ubicacion + clima        | gpr      |        8 |  0.513 |     0.007 | 0.362 | 0.634 |            0.92  |
| ubicacion + relieve      | gpr      |        7 |  0.51  |     0.011 | 0.371 | 0.638 |            0.705 |

## C. Combinaciones
| experimento                               | modelo   |   n_vars |   rmse |   rmse_sd |   mae |    r2 |   rmse_municipio |
|:------------------------------------------|:---------|---------:|-------:|----------:|------:|------:|-----------------:|
| ubicacion                                 | ridge    |        4 |  0.504 |     0.008 | 0.353 | 0.646 |            0.684 |
| ubicacion                                 | rf       |        4 |  0.506 |     0.006 | 0.338 | 0.644 |            0.627 |
| ubicacion                                 | lgbm     |        4 |  0.493 |     0.007 | 0.335 | 0.661 |            0.565 |
| ubicacion                                 | gpr      |        4 |  0.538 |     0.034 | 0.356 | 0.596 |            0.741 |
| ubicacion + relieve + clima               | ridge    |       11 |  0.517 |     0.018 | 0.378 | 0.627 |            0.673 |
| ubicacion + relieve + clima               | rf       |       11 |  0.503 |     0.005 | 0.344 | 0.649 |            0.601 |
| ubicacion + relieve + clima               | lgbm     |       11 |  0.493 |     0.01  | 0.343 | 0.662 |            0.542 |
| ubicacion + relieve + clima               | gpr      |       11 |  0.516 |     0.008 | 0.376 | 0.63  |            0.66  |
| ubicacion + feno_core + relieve + clima   | ridge    |       51 |  0.521 |     0.007 | 0.374 | 0.623 |            0.667 |
| ubicacion + feno_core + relieve + clima   | rf       |       51 |  0.498 |     0.006 | 0.339 | 0.655 |            0.613 |
| ubicacion + feno_core + relieve + clima   | lgbm     |       51 |  0.508 |     0.012 | 0.347 | 0.641 |            0.559 |
| ubicacion + feno_core + relieve + clima   | gpr      |       51 |  0.519 |     0.011 | 0.37  | 0.626 |            0.759 |
| ubicacion + planet_feno + clima + relieve | ridge    |       91 |  0.533 |     0.012 | 0.388 | 0.605 |            0.648 |
| ubicacion + planet_feno + clima + relieve | rf       |       91 |  0.5   |     0.006 | 0.341 | 0.652 |            0.654 |
| ubicacion + planet_feno + clima + relieve | lgbm     |       91 |  0.509 |     0.009 | 0.348 | 0.639 |            0.621 |
| ubicacion + satelite + clima + relieve    | ridge    |      251 |  0.567 |     0.014 | 0.413 | 0.552 |            0.752 |
| ubicacion + satelite + clima + relieve    | rf       |      251 |  0.507 |     0.006 | 0.348 | 0.643 |            0.646 |
| ubicacion + satelite + clima + relieve    | lgbm     |      251 |  0.52  |     0.009 | 0.358 | 0.623 |            0.626 |
| todo sin ubicacion                        | ridge    |      263 |  0.596 |     0.018 | 0.443 | 0.505 |            0.779 |
| todo sin ubicacion                        | rf       |      263 |  0.602 |     0.008 | 0.436 | 0.495 |            0.968 |
| todo sin ubicacion                        | lgbm     |      263 |  0.592 |     0.019 | 0.425 | 0.513 |            0.946 |
| todo                                      | ridge    |      267 |  0.564 |     0.014 | 0.413 | 0.557 |            0.718 |
| todo                                      | rf       |      267 |  0.506 |     0.007 | 0.347 | 0.643 |            0.662 |
| todo                                      | lgbm     |      267 |  0.517 |     0.011 | 0.354 | 0.628 |            0.627 |

## D. Ensambles
| experimento                                                               |   rmse |   rmse_sd |   mae |    r2 |
|:--------------------------------------------------------------------------|-------:|----------:|------:|------:|
| gpr(ubic) + lgbm(ubic+relieve+clima)                                      |  0.501 |     0.006 | 0.343 | 0.651 |
| gpr(ubic) + lgbm(ubic+feno+relieve+clima)                                 |  0.507 |     0.006 | 0.343 | 0.643 |
| gpr + lgbm (ubic+relieve+clima)                                           |  0.497 |     0.008 | 0.352 | 0.657 |
| gpr + lgbm + rf (ubic+relieve+clima)                                      |  0.497 |     0.006 | 0.348 | 0.657 |
| gpr + lgbm (ubic+feno+relieve+clima)                                      |  0.5   |     0.009 | 0.347 | 0.652 |
| gpr + lgbm + rf (ubic+feno+relieve+clima)                                 |  0.496 |     0.008 | 0.341 | 0.658 |
| gpr + lgbm + rf + ridge (ubic+feno+relieve+clima)                         |  0.496 |     0.007 | 0.345 | 0.658 |
| lgbm(ubic+relieve+clima) + rf(ubic+planet_feno+clima+relieve)             |  0.491 |     0.007 | 0.336 | 0.664 |
| gpr(ubic) + lgbm(ubic+relieve+clima) + rf(ubic+planet_feno+clima+relieve) |  0.495 |     0.005 | 0.336 | 0.66  |

## E. Pregunta guía 1: índice más importante
| experimento                     | modelo   |   n_vars |   rmse |   rmse_sd |   mae |    r2 |
|:--------------------------------|:---------|---------:|-------:|----------:|------:|------:|
| indice planet:ndvi solo         | lgbm     |       20 |  0.678 |     0.016 | 0.514 | 0.36  |
| ubicacion + indice planet:ndvi  | lgbm     |       24 |  0.507 |     0.01  | 0.347 | 0.643 |
| indice planet:evi solo          | lgbm     |       20 |  0.639 |     0.011 | 0.482 | 0.432 |
| ubicacion + indice planet:evi   | lgbm     |       24 |  0.498 |     0.008 | 0.336 | 0.655 |
| indice planet:lai solo          | lgbm     |       20 |  0.685 |     0.019 | 0.521 | 0.347 |
| ubicacion + indice planet:lai   | lgbm     |       24 |  0.501 |     0.008 | 0.344 | 0.651 |
| indice planet:msavi solo        | lgbm     |       20 |  0.655 |     0.013 | 0.484 | 0.404 |
| ubicacion + indice planet:msavi | lgbm     |       24 |  0.5   |     0.009 | 0.339 | 0.653 |
| indice s2:ndvi solo             | lgbm     |       20 |  0.67  |     0.017 | 0.52  | 0.375 |
| ubicacion + indice s2:ndvi      | lgbm     |       24 |  0.502 |     0.009 | 0.35  | 0.65  |
| indice s2:evi solo              | lgbm     |       20 |  0.679 |     0.014 | 0.496 | 0.359 |
| ubicacion + indice s2:evi       | lgbm     |       24 |  0.501 |     0.009 | 0.342 | 0.651 |
| indice s2:savi solo             | lgbm     |       20 |  0.66  |     0.017 | 0.488 | 0.394 |
| ubicacion + indice s2:savi      | lgbm     |       24 |  0.503 |     0.011 | 0.344 | 0.648 |
| indice s2:lai solo              | lgbm     |       20 |  0.659 |     0.022 | 0.492 | 0.395 |
| ubicacion + indice s2:lai       | lgbm     |       24 |  0.507 |     0.012 | 0.349 | 0.643 |
| indice s2:fapar solo            | lgbm     |       20 |  0.706 |     0.009 | 0.532 | 0.307 |
| ubicacion + indice s2:fapar     | lgbm     |       24 |  0.506 |     0.008 | 0.346 | 0.643 |
| indice s2:ndwi solo             | lgbm     |       20 |  0.68  |     0.022 | 0.513 | 0.356 |
| ubicacion + indice s2:ndwi      | lgbm     |       24 |  0.507 |     0.011 | 0.347 | 0.643 |
| indice s2:msi solo              | lgbm     |       20 |  0.704 |     0.017 | 0.532 | 0.311 |
| ubicacion + indice s2:msi       | lgbm     |       24 |  0.503 |     0.011 | 0.345 | 0.648 |
| indice s2:ndti solo             | lgbm     |       20 |  0.733 |     0.014 | 0.551 | 0.253 |
| ubicacion + indice s2:ndti      | lgbm     |       24 |  0.502 |     0.007 | 0.343 | 0.65  |

## F. Pregunta guía 2: variable climática
| experimento                    | modelo   |   n_vars |   rmse |   rmse_sd |   mae |    r2 |
|:-------------------------------|:---------|---------:|-------:|----------:|------:|------:|
| clima prec_abr_oct solo        | lgbm     |        1 |  0.604 |     0.012 | 0.419 | 0.492 |
| ubicacion + prec_abr_oct       | lgbm     |        5 |  0.494 |     0.008 | 0.337 | 0.661 |
| clima tmax_media_abr_oct solo  | lgbm     |        1 |  0.658 |     0.008 | 0.48  | 0.399 |
| ubicacion + tmax_media_abr_oct | lgbm     |        5 |  0.495 |     0.008 | 0.34  | 0.659 |
| clima tmin_media_abr_oct solo  | lgbm     |        1 |  0.603 |     0.017 | 0.432 | 0.494 |
| ubicacion + tmin_media_abr_oct | lgbm     |        5 |  0.494 |     0.008 | 0.337 | 0.661 |
| clima prec_anomalia solo       | lgbm     |        1 |  0.584 |     0.014 | 0.411 | 0.526 |
| ubicacion + prec_anomalia      | lgbm     |        5 |  0.494 |     0.009 | 0.337 | 0.661 |