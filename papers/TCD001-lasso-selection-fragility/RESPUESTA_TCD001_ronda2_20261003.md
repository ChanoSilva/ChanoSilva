# Respuesta del autor — TCD001, ronda 2 de revisión interna (03/10/2026)

Objeto: informe `REFEREE_TCD001_ronda2_20261003.md` (cambios menores; 0 bloqueantes, 3 mayores, 13 menores; verificación de la ronda 1: 22 bien, 2 a medias, 1 con error nuevo). Versión resultante: borrador v0.3 (3 October 2026), `manuscript/main.pdf`, 10 páginas.

## Resumen

- **Recuento:** 16 hallazgos nuevos → 15 aceptados, 1 aceptado con matiz (M2), 0 rebatidos. Las tres correcciones pendientes de la ronda 1 (m10 con error nuevo; m11 y m12 a medias) quedan aplicadas a través de M2, m7, m2 y m3. Bibliografía: Rubinstein–Hopkins añadida; Konrad–Kuschnig añadida tras verificar su resumen.
- **Números:** corrida de referencia v0.3 completa en una sola sesión, necesaria para que el contador de M1 salga de una corrida real de todos los scripts (≈ 108 s de CPU). Todos los recuentos, fracciones, medias, veredictos, ejemplos exactos y certificados son idénticos a v0.2 (409 de 494 macros previas idénticas). Cambian 79 macros de tiempo o coste (corrida nueva y dos cifras significativas) y 6 por correcciones de formato pedidas (m5, m10). Ningún veredicto cambia: 0 de 18 combinaciones cumplen el criterio (cociente mínimo bruto 0.44, ajustado 0.25).
- **Compilación:** v0.2 tenía 10 páginas; tras los añadidos el PDF llegó a 11 y, tras los recortes, v0.3 tiene 10. `build.sh` da 0 errores, 0 referencias o citas indefinidas, 0 "??" y 0 Overfull.
- **No tocado:** `theory/` (otro agente). La Conjetura 5.3 queda como estaba; solo se corrigió en la introducción el alcance de "lo abierto" (m1).

## Hallazgos mayores

**M1. "Never triggered in the reference runs" es falso.** → **Aceptado.**
- Código: `lasso_fragility.py` cuenta las llamadas a `lasso_lars` y los retrocesos en `KKT_STATS`, junto con su clasificación (empate exacto del máximo de |x_jᵀy|, rango completo de X) y los errores KKT máximos relativos a max(1, μ) de las salidas aceptadas, de las rechazadas y de las de descenso por coordenadas. Cada script reinicia el contador y lo vuelca en `meta.kkt_guard` de su JSON. `exact_examples.py --no-guard` repite E0 sin guarda y escribe `results/examples_noguard.json`. `make_numbers.py` convierte los contadores en macros (`\EzeroFits`, `\EzeroFallbacks`, `\EoneToFiveFits`, `\EoneToFiveFallbacks`, `\EzeroGuardIdentical`, …). Además comprueba con aserciones que E1–E5 tienen 0 retrocesos, que todos los de E0 son empates con X de rango completo y que los ejemplos son idénticos con y sin guarda: si una corrida futura contradice el texto, el build falla.
- Resultado (idéntico a la tabla del árbitro): E0 tiene 950 ajustes y 91 retrocesos (91 con empate exacto en la entrada y 91 con X de rango completo; error activo de la salida rechazada de hasta 6.2·max(1, μ)). E1: 0 de 16 191; E2/E3/E5: 0 de 117 708; E4: 0 de 10 365. `examples.json` es idéntico con y sin guarda, e idéntico al de v0.2.
- Texto: Limitations (`main.tex`, párrafo "Limitations") con la redacción propuesta por el árbitro, por macro; Apéndice A, "Solver" (91 de 950 en E0, ninguno en E1–E5, contadores en `meta.kkt_guard`). También el docstring de `lasso_lars`, CONTINUIDAD (línea del solver) y una fe de erratas añadida a la respuesta a B1 en `RESPUESTA_TCD001_ronda1_20260930.md`, que limita "nunca se activa" a E1–E5.

**M2. E4: "resolución del cronómetro", familia B omitida y coste del greedy sobreafirmado.** → **Aceptado con matiz.**
- Aceptado: se borra "dominated by timer resolution". El párrafo de E4 dice que en la familia B el greedy es más lento que la búsqueda exhaustiva en todo n ≤ 34, y que en A lo es a n ≤ 18. Lo explica con datos de la corrida: con f pequeño, un lote de n tests cerrados (mediana ≤ 0.13 ms en B) gana a los al menos dos ajustes del greedy (1.2–1.5 ms). "Cheap" queda limitado a la familia A con n = 34; la exactitud se da como 17 de 19 instancias con f finito (89 %, error típico 7 puntos), diciendo que 20 instancias no deciden la parte de exactitud y que la exactitud no es monótona en n (77, 93, 82 y 89 %). Los cocientes se imprimen con dos cifras significativas (`sig2` en `make_numbers.py`, también en la Tabla 2 y en las macros de E3). La fila de la tabla de afirmaciones, el README y la ficha (ES/EN, "familia A"; "familia B 8–11 veces más cara") quedan corregidos.
- Matiz 1 (variabilidad, punto (v)): la redacción propuesta ("for n ≤ 26 in family A … the greedy is slower") **no se sostiene en la corrida v0.3**: con A y n = 26 el cociente mediano es 0.92, y con n = 22 la repetición del árbitro dio 0.595. Por eso los cocientes se dan como rangos sobre tres corridas completas del mismo código con las mismas semillas: la v0.2, la repetición del árbitro (archivada en `results/cost_ratios_run_referee.json` desde su carpeta de trabajo) y la v0.3. Rangos: B 8.1–11; A 4.3–11 con n ≤ 18, 0.60–1.4 con n = 22–26, 0.58–0.68 con n = 30 y 0.055–0.070 con n = 34. El factor máximo entre corridas es ×2.3 (A, n = 22), calculado por `make_numbers.py` y no tecleado. Cada frase cualitativa ("más lento en B y en A con n ≤ 18", "más rápido en las tres corridas solo con n ≥ 30", "bajo el 10 % solo con n = 34") tiene su aserción. La fila de la tabla de afirmaciones dice ahora "cheaper than the exhaustive search in all three runs only in family A at n ≥ 30, and below the cost threshold only at n = 34, with 17/19 exact".
- Matiz 2 (aritmética, punto (iv)): con 17/19 el déficit frente al umbral del 90 % es (0.90 − 0.895)/0.070 ≈ 0.07 errores típicos, no 0.15 (`\EfourAThirtyfourShortfallSE` = 0.1). La conclusión del árbitro (20 instancias no deciden nada) se refuerza.
- Matiz 3 (ficha): el árbitro propuso "en torno al 6–7 %"; el rango medido es 5.5–7 %, y es lo que se escribe.

**M3. Obs. 3.5 sin la hipótesis de unicidad.** → **Aceptado.** La Obs. 3.5 dice ahora: "if the Lasso minimiser on every subsample of size ⌊n/2⌋ is unique (with probability one for designs with a continuous distribution), f_leave(j)(D) > ⌈n/2⌉ under the rule used implies Π_j = 1; without uniqueness a subsample on which the solver drops j need not be a witness". También dice sin rodeos que "In the original paper the Lasso is ‖Y − Xβ‖²₂ + λ‖β‖₁ with λ fixed across subsamples, i.e. rule C (with μ = λ/2)". La tabla de afirmaciones recoge la hipótesis. Verificación de la forma de Meinshausen–Bühlmann: solo por fragmentos de búsqueda (los del árbitro); stat.ethz.ch, people.math.ethz.ch y wiley siguen bloqueados por el proxy en esta sesión, y así consta en CONTINUIDAD.

## Hallazgos menores

| Id | Decisión | Qué se cambió y dónde |
|---|---|---|
| m1 | Aceptado | Introducción: "deselection for p ≥ 2 inherits the hardness, and the complexity of selection witnesses for p ≥ 2 is open (Conjecture 5.3)". También en el README. |
| m2 | Aceptado | Teo. 5.1(a): "some nonempty proper R"; prueba: "For a nonempty proper R…", "nonempty because t < Σb_i forces K' ≠ [m], and proper because m+1 ∉ R". |
| m3 | Aceptado (primera opción) | Ej. 4.3: "all 26 removal sets with \|R\| ≤ n − 2 (including R = ∅)"; se corrigieron el comentario de `exact_examples.py` y el texto de `examples.md`. Comprobación aparte (fuera de `results/`, no citada en el PDF): los 5 conjuntos con \|R\| = 4 también se verifican en exacto (una sola fila; soporte {1}, {2} o ∅), y con ellos los pares no monótonos para LEAVE(1) pasarían de 3 a 9 (los superconjuntos que dejan solo la observación 1 devuelven la variable 1). No se amplió el bucle en esta versión porque cambiaría la definición de `\ExTwoPairs` y el texto; queda como opción para v0.4. |
| m4 | Aceptado | "to $10^{-14}$" pasa a la macro `\KKTMaxActiveRel` (3.6·10⁻¹⁴ relativo a max(1, μ), máximo en E1–E5, del contador de M1). |
| m5 | Aceptado | `half()` en `make_numbers.py` para medianas y cuartiles (macros y `table_e4b.tex`). La mediana a n = 400 es 10.5. También corrige 6 → 6.5 (A, 100), 10 → 9.5 (A, 200) y 2 → 1.5 (B, 200), que `:.0f` redondeaba al par. README corregido. |
| m6 | Aceptado | E3: "E3 uses the unsigned ANY target, which coincided with the signed one in every instance". |
| m7 | Aceptado | Cor. 3.2: "if S = ∅, m = +∞ and the first term below is 0". |
| m8 | Aceptado | Tabla de afirmaciones: "(Lemma 2.4); uniqueness under full rank of X_E (Tibshirani 2013)". |
| m9 | Aceptado | "Timing": "subtracting from every heuristic its mean time per refit step (which includes one scoring step and so favours the heuristic)". Leyenda de la Tabla 2: "adj. subtracts the heuristic's mean time per refit step (at least one refit)". |
| m10 | Aceptado | `pct`/`pctcell` imprimen un decimal en [99.5, 100) y en (0, 0.5): "99.6% ± 0.4" en la fila (B, any, sorted scores); también `\EthreeBLeaveKpredUnder` 0 → 0.4. |
| m11 | Aceptado | Segunda verificación KKT tras el retroceso, con `RuntimeError` si falla (máximo medido en E0: 5·10⁻¹² relativo); docstring de `kkt_residuals` corregido (devuelve dos valores). |
| m12 | Aceptado | CONTINUIDAD: "0.067" sustituido (0.062 en v0.3; 0.055–0.070 en tres corridas) y línea del solver corregida (M1). |
| m13 | Aceptado | Columna "IQR cost ratio" en el veredicto de `results/fragility.md` (y en `results/scaling.md`, con medianas de tiempos); la leyenda de la Tabla 2 remite a ella. |

## Verificación de la ronda 1: puntos pendientes

| Id (ronda 1) | Estado en v0.2 | Acción en v0.3 |
|---|---|---|
| m10 | Error nuevo ("timer resolution") | Frase borrada; ver M2. |
| m11 | A medias (falta S = ∅) | Ver m7. |
| m12 | A medias ("nonempty" no propagado) | Ver m2 y m3. |
| M1 (salvedad de unicidad no trasladada a la Obs. 3.5) | Señalado | Ver M3. |
| M2 (ficha: n = 34 sin "familia A") | Señalado | Ver M2. |
| M3 (afirmación sobre la guarda KKT) | Señalado | Ver M1. |
| M7 (puede escribirse "regla C") | Mejorable | Ver M3. |
| m13 (fila del Lema 2.4) | Señalado | Ver m8. |
| m7 (redondeo en la misma frase) | Señalado | Ver m5. |

## Bibliografía

- Rubinstein y Hopkins (ICLR 2025, arXiv:2410.07916): **añadida** (`rubinstein2025`). Autores, título, sede y contenido verificados por búsqueda (resumen de arXiv, OpenReview, actas de ICLR y mlanthology); arxiv.org está bloqueado para lectura directa. Se cita tras la Prop. 3.4 ("certified lower bounds on the number of removals that can overturn a least-squares conclusion, for far larger problems"), en la Obs. 5.2(iii) y en la introducción.
- Konrad y Kuschnig (ICML 2026, arXiv:2606.05919): **añadida** (`konrad2026`). Autores (Lucas D. Konrad, Nikolas Kuschnig), título, sede, fecha de envío (04/06/2026) y contenido (para estimandos con efectos de eliminación lineal-fraccionales, el conjunto más influyente se reduce a una sucesión de problemas top-k por Dinkelbach) verificados en varios resultados de búsqueda concordantes. Se cita una sola vez en la introducción y solo por lo que dice el resumen.
- meinshausen2010: ver M3.
- Las 16 entradas clásicas siguen sin verificación en red (CONTINUIDAD).
- Cambios de formato para la extensión: autores de pedregosa2011 abreviados con "and others"; dirección duplicada de woodbury1950 suprimida; nota de moitra2022 abreviada ("ICLR 2023").

## Extensión

Tras los añadidos el PDF llegó a 11 páginas. Recortes sin pérdida de contenido verificable:
- guía de secciones de la introducción condensada;
- lista de cocientes del greedy en E3 sustituida por la remisión a la Tabla 2, que los contiene;
- frase redundante de E1;
- frase introductoria del Ej. 4.3 y frase sobre la granularidad en la Obs. 5.2(i);
- Tabla 2 con `arraystretch` 0.85 y Figura 1 al 72 % del ancho;
- "Pre-specification" y próximos pasos condensados;
- tres ajustes de formato en `refs.bib`.

Resultado: 10 páginas.

## Cómputo

Corrida de referencia v0.3 en una sola sesión (03/10/2026 10:00:07–10:02:00 UTC, `results/run_session_v03.txt`). E0 1.6 s, E0 sin guarda 1.5 s, E1 9.8 s, E2/E3/E5 50.9 s, E4 45.5 s y figuras; ≈ 108 s de CPU en total, más ≈ 3 s de comprobaciones (`check_b1_counterexample.py`, pruebas del contador) y las compilaciones.

## Registro de trabajo (incremental)

- [inicio] Leídos los briefs, el informe y `main.tex` v0.2.
- [código] `lasso_fragility.py`: contador `KKT_STATS` (llamadas, retrocesos, clasificación de retrocesos —empate exacto en la entrada, rango completo—, errores KKT relativos máximos de las salidas aceptadas, rechazadas y de descenso por coordenadas), segunda verificación KKT tras el retroceso con `RuntimeError` si falla (m11), docstring de `kkt_residuals` corregido (m11). Los cuatro scripts reinician el contador y lo vuelcan en `meta.kkt_guard` de su JSON. `exact_examples.py --no-guard` escribe `results/examples_noguard.json` para la comparación con y sin guarda. Nuevo `snapshot_cost_ratios.py`: archivó los cocientes de coste de la corrida v0.2 antes de volver a correr (M2(v)); el archivo quedó finalmente como `results/cost_ratios_run_v02.json`. IQR de los cocientes de coste en `fragility.md` y `scaling.md` (m13).
- [corrida] Corrida de referencia v0.3 completa en una sola sesión (03/10/2026 10:00:07–10:02:00 UTC, `results/run_session_v03.txt`): E0 1.6 s, E0 sin guarda 1.5 s, E1 9.8 s, E2/E3/E5 50.9 s, E4 45.5 s de pared. Contadores: E0 950 ajustes, 91 retrocesos (91 con empate exacto de |x_jᵀy| en la entrada, 91 con X de rango completo), error activo máximo de una salida rechazada 6.2·max(1, μ); E1 0/16 191; E2/E3/E5 0/117 708; E4 0/10 365; error activo máximo aceptado en E1–E5: 3.6·10⁻¹⁴ relativo a max(1, μ). `examples.json` idéntico con y sin guarda e idéntico al de v0.2. Coinciden exactamente con la tabla de M1 del árbitro.
- [variabilidad] `snapshot_cost_ratios.py` archivó los cocientes de coste de dos corridas completas anteriores del mismo código con las mismas semillas: la v0.2 (`results/cost_ratios_run_v02.json`) y la repetición completa del árbitro de la ronda 2 (`results/cost_ratios_run_referee.json`, tomada de su carpeta de trabajo, 09:46–09:48 UTC; mismo código más un contador). `make_numbers.py` calcula los rangos de los cocientes por celda sobre las tres corridas y comprueba con aserciones las frases cualitativas del texto (el build falla si una nueva corrida las contradice).
- [números] `make_numbers.py` regenerado (528 macros). Respecto de v0.2, 409 macros idénticas; cambian 79 de tiempo o coste (corrida nueva, ahora a 2 cifras significativas) y 6 por las correcciones de formato pedidas: `\EthreeBAnyAmipExact` 100 → 99.6 y `\EthreeBLeaveKpredUnder` 0 → 0.4 (m10); medianas greedy `\EfourAHundredMedian` 6 → 6.5, `\EfourATwohundredMedian` 10 → 9.5, `\EfourAFourhundredMedian` 10 → 10.5, `\EfourBTwohundredMedian` 2 → 1.5 (m5: `:.0f` redondeaba al par). Ningún recuento, fracción ni veredicto cambió. E3: cociente mínimo bruto 0.44 (v0.2: 0.46), ajustado 0.25 (0.26): 0/18 se mantiene.
- [bibliografía] Verificadas por búsqueda web (arxiv.org, stat.ethz.ch y wiley bloqueados por el proxy; los resultados reproducen el resumen de arXiv, la página de ICLR/OpenReview y mlanthology): Rubinstein y Hopkins; Konrad y Kuschnig. Añadidas a `refs.bib`. Meinshausen–Bühlmann (2010): el PDF sigue inaccesible; la forma suma con λ fijo se apoya en los fragmentos de búsqueda que citó el árbitro.
- [manuscrito] `main.tex` v0.3 editado en pasos compilables (M1, M2, M3, m1–m10, citas nuevas). 11 → 10 páginas con los recortes descritos en "Extensión". `build.sh`: 0 errores, 0 citas o referencias indefinidas, 0 "??", 0 Overfull, 2 Underfull (los mismos de v0.2, tabla de afirmaciones).
- [notas] README (estado v0.3, cifras de E1/E3/E4, guarda KKT, reproducción), ficha (ES/EN), CONTINUIDAD (correcciones y sección "Ronda 2 de revisión interna (03/10/2026)") y fe de erratas en la respuesta de la ronda 1.

## Queda abierto

1. Cotejar la forma del Lasso de Meinshausen–Bühlmann (2010) con el PDF.
2. Leer el texto completo de rubinstein2025 y konrad2026 (solo se verificaron los resúmenes).
3. Verificación en red de las 16 entradas clásicas.
4. Los cocientes de coste dependen de la carga de la máquina (hasta ×2.3 entre corridas); a n = 34 la parte de exactitud del criterio no está decidida (17/19).
5. Integración de `theory/` (otro agente), por separado.
