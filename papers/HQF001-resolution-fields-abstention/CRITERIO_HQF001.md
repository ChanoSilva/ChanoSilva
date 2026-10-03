# Criterio predefinido de HQF001 — registro fechado

**Fecha de este archivo:** 03/10/2026 (v0.2 del borrador), creado a petición del árbitro interno (hallazgo M2 de la ronda 1).

## Criterio (texto exacto)

> *Residual gain* = the AURC of the anisotropic resolution field is lower than that of the best reference (the reference with the lowest mean AURC on that dataset, among the 7 references: k-NN, NCM, LDA, QDA, logistic regression, random forest, DANN) on a majority (≥ n//2 + 1 = 5 of n = 8 datasets) of datasets, with the paired 95 % percentile-bootstrap interval over the 15 folds excluding zero.

El mismo texto está en la constante `CRITERION_TEXT` de `experiments/selective_benchmark.py` y se almacena en `results/results.json → meta.criterion`. La evaluación está en la función `summarise` del mismo archivo: `criterion_met = len(c0["better"]) >= maj` con `maj = n_ds // 2 + 1`, donde `c0["better"]` son los datasets con veredicto `"field better"` según el intervalo bootstrap de la comparación con la mejor referencia (`__best__`).

## Historia y honestidad del registro

- El criterio se fijó en la sesión del 30/09/2026 **antes** de la corrida de referencia v0.1, según consta en `CONTINUIDAD_HQF001_20260930.md` (supuesto 5). **No existe un registro fechado independiente anterior a esa corrida**: este archivo se escribe el 03/10/2026 y así se declara en el manuscrito (§4, "Predefined criterion").
- Evidencia indirecta de que el umbral no cambió: `results/results_v01.json` (escrito el 30/09/2026 por el script v0.1) almacena `criterion.Field-aniso.majority_needed = 5` y el mismo veredicto (`criterion_met = false`, 0 mejor / 6 peor / 2 no concluyente); el árbitro reprodujo bit a bit 585 de 585 AURC por pliegue y confirmó que la función que evalúa el criterio es la misma que escribe el JSON.
- Lo que sí cambió entre la prueba rápida y la corrida de referencia v0.1 (declarado en la nota y ahora en §4): la clave de hiperparámetros del campo pasó a llevar el K_m nominal en vez del recortado, para que la configuración seleccionada en la CV interna coincida con la externa en datasets pequeños. No se había visto ningún resultado de referencia.
- Entre v0.1 y v0.2 (03/10/2026) **no cambió el criterio** (umbral, intervalo, mayoría, referencias). Cambió el dataset synth-classcov (recalibración de la separación de medias, hallazgo M4 del árbitro); el veredicto del criterio es el mismo con ambas versiones del dataset. En v0.2 se reporta además el mismo recuento con un IC t sobre pliegues y con la corrección de Nadeau–Bengio; el criterio sigue siendo el bootstrap.

## Hash del script que evalúa el criterio (v0.2, 03/10/2026)

`sha256(experiments/selective_benchmark.py) = ad532282ca90cb1773f876e4e1c7ff52451c044dae1d5707d402d8ddd8fbc0e8`

Comprobación: `sha256sum experiments/selective_benchmark.py`.
