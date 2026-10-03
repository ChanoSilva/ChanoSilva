# Respuesta del autor al informe de árbitro interno — HQF001, ronda 1 (30/09/2026)

Respuesta escrita el 03/10/2026 sobre el informe `REFEREE_HQF001_ronda1_20260930.md` (2 bloqueantes, 6 mayores, 12 menores, 14 acciones). Documento de trabajo; se actualiza de forma incremental mientras se aplican los cambios (si una sección dice "EN CURSO", el cambio aún no se ha cerrado).

Convención: **aceptar** = se aplica tal cual; **aceptar con matiz** = se aplica una versión y se explica; **rebatir** = solo con demostración o cálculo.

## Resumen de decisiones

| id | decisión | estado |
|---|---|---|
| B1 | aceptar | EN CURSO |
| B2 | aceptar | EN CURSO |
| M1 | aceptar | EN CURSO |
| M2 | aceptar con matiz | EN CURSO |
| M3 | aceptar | EN CURSO |
| M4 | aceptar | EN CURSO |
| M5 | aceptar | EN CURSO |
| M6 | aceptar | EN CURSO |
| m1–m12 | ver detalle | EN CURSO |

## Plan de trabajo (orden de ejecución)

1. Código (`selective_benchmark.py`): B2 (IC por par con semilla propia, `__best__` copia la comparación directa, B = 20 000), B1 (IC t de Student e IC t corregido Nadeau–Bengio por par; victorias/empates/derrotas), M4 (calibración con indicador de límite y espectro de covarianzas que admite solución), m6 (configuraciones de QDA que no completan los pliegues internos se descartan).
2. Corrida de referencia completa con el script actual (M2.1) → `results/results.json` nuevo; la v0.1 se conserva en `results/results_v01.json`.
3. `make_numbers.py`: macros para IC t / NB, W/T/L, recuentos bajo cada intervalo, casos límite (< 0.02 de cero), tabla única AURC, tabla de diferencias rediseñada.
4. Manuscrito: reescrituras B1/M3/M5/M6, M1, m2–m4, m8–m12, recortes a ≤ 10 páginas, Apéndice A (m5, M2).
5. Archivo fechado con el criterio (M2.2), README, FICHA, CONTINUIDAD.

## Detalle por hallazgo

### B1 — IC bootstrap optimistas que inflan todas las afirmaciones positivas. **Aceptar.**
El árbitro tiene razón en el punto central: el optimismo de los IC sobre pliegues repetidos solo es conservador para el recuento "mejor" del criterio (que no puede bajar de 0), y favorece a todo lo demás que el texto afirmaba en positivo. Verifiqué sus cifras desde `per_fold` antes de tocar nada: mi implementación del IC t (14 g.l.) y del IC con corrección de Nadeau–Bengio (ρ = n_test/n_train = 1/4) reproduce exactamente las suyas (iris campo − LDA: t [−0.03, +0.43], NB [−0.30, +0.70], V/E/D 1/6/8; digits aniso − iso: t [−1.25, −0.32], NB [−1.79, +0.23], 15/0/0; etc.).
Cambios: (a) `selective_benchmark.py`, nueva función `pair_stats`: para cada par se almacenan media, IC bootstrap percentil (el predefinido), IC t de Student, IC t Nadeau–Bengio, victorias/empates/derrotas, p de Wilcoxon (descriptivo), veredicto bajo cada intervalo y un indicador de caso límite (extremo del IC bootstrap o t a < 0.02 de cero en AURC×100); el criterio se evalúa con el bootstrap (predefinido) y se reporta también el mismo recuento bajo t y NB. (b) `make_numbers.py` y `main.tex`: la Tabla de diferencias frente a la mejor referencia pasa a dar las tres columnas de IC, V/E/D y p; la tabla de ablaciones da IC bootstrap, IC t y V/E/D para aniso − iso y marca las demás celdas con negrita/cursiva solo cuando **ambos** intervalos excluyen cero (superíndice b: solo el bootstrap); lo mismo en la tabla campo vs cada referencia. (c) Reescritas las frases de main.tex:161 y :330 con la formulación del árbitro; resumen, §6, Tabla de afirmaciones y ficha con "2–3 datasets según el intervalo; sugerente, no establecida" y "6 con bootstrap, 5 con IC t" (los números concretos salen de macros, no se tipean). Véanse las cifras finales en la sección "Números que cambiaron" al final de este documento.

### B2 — Dos IC distintos para el mismo par; viñeta de la nota incorrecta. **Aceptar.**
Confirmado: `__best__` se remuestreaba aparte. Cambios: (a) cada par tiene su propio generador sembrado con la semilla maestra y un CRC32 del nombre del par (`pair_rng`; no se usa `hash()` porque Python lo sala por proceso), así que el IC de un par no depende del orden de evaluación; (b) `__best__` es ahora `dict(comp[best_ref])`, una copia; (c) B = 20 000 (coste ≈ 3 s al re-resumir). Resultado sobre los pliegues v0.1 (antes de la nueva corrida): breast-cancer campo vs NCM pasa a [−0.65, +0.0006] → **no concluyente y límite**, como anticipó el árbitro con B = 200 000; breast-cancer vs k-NN [+0.0017, +0.54] sigue "peor" pero límite; moons aniso − iso [−0.10, +0.005] límite; wine vs mejor referencia [−0.005, +0.10] límite. Todos los pares límite se marcan en las tablas (superíndice ∘) y se listan en el texto mediante macros. "NCM 8/0" se sustituye por lo que resulte de la corrida v0.2. (d) Viñeta de la nota reescrita con las cifras del árbitro (desplazamientos hasta 0.25, mediana 0.014, 4 veredictos individuales cambiados, ninguno del criterio); no las recalculé yo: cito su verificación (`verif_math_stats.txt`, D2) como fuente.

### M4 — synth-classcov con medias coincidentes. **Aceptar** (opción 1 del árbitro: correr la variante con desplazamiento no nulo).
`_calibrate_shift` devuelve ahora `(shift, at_bound)` y el indicador se guarda en el JSON (`shift_at_bound`). Con el espectro v0.1 (2, 1, 0.5, 0.25, 0.1, 0.05) no hay solución en [0.05, 20] (error de Bayes con medias coincidentes 7.7 %); probé cuatro espectros menos dispares (coste 4 s de CPU) y elegí `geomspace(2, 0.25, 6)`: error de Bayes 20.6 % con medias coincidentes, desplazamiento calibrado 1.54, error de Bayes 9.9 %. Las rotaciones y todos los demás sorteos son idénticos a v0.1 (mismo consumo del RNG; synth-lda reproduce su desplazamiento 1.20 y su error 9.8 %). Como el dataset cambia, se repite la **corrida de referencia completa** con el script v0.2 (resuelve a la vez M2.1, B2 y m6); la v0.1 se conserva en `results/results_v01.json` y `results/tables_v01.md`, y el manuscrito y la nota reportan explícitamente los números v0.1 de synth-classcov (medias coincidentes) junto a los v0.2, con la advertencia de que el conjunto de datasets del criterio se modificó tras ver los resultados v0.1 (el veredicto del criterio es el mismo en ambas versiones).

### m6 — QDA con configuraciones omitidas. **Aceptar.** En `evaluate_fold`, una configuración que no completa los 3 pliegues internos se descarta y se cuenta (`inner_configs_dropped`, agregado por método y dataset en el resumen); el Apéndice A reporta el total. En la prueba de humo (iris, pliegue 1) no se descartó ninguna y los 13 AURC coinciden bit a bit con v0.1.
