# Informe de árbitro interno — TCD001, ronda 2 (03/10/2026)

Objeto: borrador v0.2 (`manuscript/main.tex`, `main.pdf`, 10 pp.), `experiments/*.py`, `results/*`, `README.md`, `FICHA_TCD001_propuesta.md`, `CONTINUIDAD_TCD001_20260930.md`, frente a `REFEREE_TCD001_ronda1_20260930.md` y `RESPUESTA_TCD001_ronda1_20260930.md`. Versión anterior: commit `b632e86` (v0.1); v0.2 corresponde al commit `2215056`; después solo cambiaron este informe y `theory/`. La subcarpeta `theory/` (trabajo paralelo sobre p ≥ 2) no se evalúa. Trabajo auxiliar (copias, scripts, logs, notas): `scratchpad/referee2_TCD001/`. Numeración según el PDF v0.2 (Lema 2.4; Prop. 3.1; Cor. 3.2; Obs. 3.3; Prop. 3.4; Obs. 3.5; Prop. 4.1; Ej. 4.2, 4.3; Teo. 5.1; Obs. 5.2; Conj. 5.3).

## Veredicto

**Cambios menores.** Las demostraciones (Prop. 3.1, Cor. 3.2 corregido, Prop. 3.4, Teo. 5.1 en ambas reglas) son correctas en una lectura nueva y la corrida de referencia se reproduce exactamente en las 422 macros no temporales. Quedan tres correcciones de cierto peso, todas de redacción y ninguna exige nuevas demostraciones: (M1) el texto afirma que la guarda KKT "nunca se activa en las corridas de referencia", pero se activa 91 veces en E0; (M2) la conclusión de E4 sobre el coste del greedy se apoya en un argumento falso ("resolución del cronómetro"), omite que en la familia B el greedy es entre 8 y 11 veces más caro y aplica a n = 34 una lectura estadística más laxa que en E3; (M3) a la Obs. 3.5 le falta la hipótesis de unicidad que la Def. 2.2 exige.

Recuento: 0 bloqueantes, 3 mayores, 13 menores.

## Verificación de la ronda 1

Comprobado contra `main.tex` v0.2 (líneas citadas), el código y los resultados regenerados. "Bien" = aplicado y correcto.

| Id | Estado | Evidencia |
|---|---|---|
| B1 | aplicado bien | `main.tex:150` (hipótesis h_i < 1 y su equivalencia de rango), `:156` (ι_i = +∞ si h_i = 1), `:161` (prueba y contraejemplo). Código: `lasso_fragility.py:225–245` (`h_tol`, máscara `rank_deficient`). `check_b1_counterexample.py` pasa (1.2 s). El fallo de `lars_path` que se menciona como hallazgo colateral se reproduce exactamente (ver "Verificación computacional"). |
| M1 | aplicado bien | Párrafo `main.tex:147`; Limitations `:330`; tabla de afirmaciones `:315`; docstring de `fragility_exact` (`lasso_fragility.py:315–327`). Falta trasladar la misma salvedad a la Obs. 3.5 (nuevo M3). |
| M2 | aplicado bien | Intro `main.tex:63` con el texto propuesto; resumen `:56` con "at n ≤ 14"; ficha (ES/EN) con "familias elegidas tras un barrido piloto". La frase nueva de la ficha sobre n = 34 hereda el problema de M2 de esta ronda (no dice que es la familia A). |
| M3 | aplicado bien | (a) Párrafo "Pre-specification and changes", `main.tex:260`. (b) Sesión única 04:08:11–04:09:40 UTC (`results/run_session_v02_start.txt`); `lasso_fragility.py` (mtime 04:02:30) es anterior a la sesión; reproduje la sesión completa con 0 diferencias en las macros no temporales. La afirmación nueva de ese párrafo y de Limitations sobre la guarda KKT es falsa (nuevo M1). |
| M4 | aplicado bien | `examples.json` contiene `example1b`; `\ExOneChecks` = 12/12 citado en `main.tex:198`. |
| M5 | aplicado bien | Texto E3 `main.tex:272` (e.t. 0.4–3.1 puntos; déficit de ENTER a 1.7/1.1 e.t.); Tabla 2 con "exact ± s.e." y "adj. cost ratio". Discrepancia menor entre la descripción del ajuste y el código (m9). |
| M6 | aplicado bien (con matiz aceptable) | Tabla de afirmaciones conservada, `[!htb]`, `footnotesize`; compilación: 0 `Overfull`, 2 `Underfull \hbox` (badness 4217, `main.tex:321–323`), cosméticos. |
| M7 | aplicado bien (mejorable) | `main.tex:188`: ya no atribuye la regla P. La búsqueda web confirma la forma suma ‖Y−Xβ‖²₂ + λΣ|β_k| sin 1/n en el artículo (ver Bibliografía), de modo que puede escribirse "regla C" sin rodeos. |
| m1 | aplicado bien | README `:14,:30`, CONTINUIDAD `:23–25`, docstrings (`lasso_fragility.py:97,168,227,249`; `run_validation.py:3–4`; `run_scaling.py:6`) usan Prop. 3.1 / Cor. 3.2 / Prop. 3.4. |
| m2 | aplicado bien | `main.tex:174`. |
| m3 | aplicado bien | `main.tex:236`. |
| m4 | aplicado bien | `refs.bib` (`woodbury1950`), `main.tex:132`; entrada verificada. |
| m5 | aplicado bien | `main.tex:61` (Kuschnig et al. en la frase de heurísticas); `refs.bib` como `@techreport` CESifo WP 8981; verificada. |
| m6 | aplicado bien | `main.tex:263` (`\EoneCorInstancesPerCell` = 30); `results/validation.md` sin "--%". |
| m7 | aplicado bien | `main.tex:289` ("mean g/n", "with finite f", y la mediana sobre las 120). Error nuevo de redondeo en la misma frase (m5 de esta ronda). |
| m8 | aplicado bien | `main.tex:289` ("censored mean …"). |
| m9 | aplicado bien | Resumen ≈ 200 palabras (203 tokens con fórmulas, `pdftotext`). |
| m10 | aplicado con error nuevo | `main.tex:289`: "ratios at n ≤ 18 … are dominated by timer resolution". Es falso: `time.perf_counter` resuelve 1 ns (`get_clock_info`), y los tiempos exhaustivos medianos son 0.12–0.66 ms. Los cocientes de 4 a 10 son reales: con f = 1 la búsqueda exhaustiva hace un solo lote de n tests (≈ 0.13 ms), mientras que el greedy necesita ≥ 2 reajustes. Ver M2. (El árbitro de la ronda 1 propuso esa explicación; el autor la adoptó sin comprobarla.) |
| m11 | aplicado a medias | `main.tex:154` trata Sᶜ = ∅ y γ = 0; falta la convención para S = ∅ (m = +∞, primer término 0), que el código sí aplica (`lasso_fragility.py:134–136, 241`) y que ocurre en 8 instancias de la familia B. Ver m7. |
| m12 | aplicado a medias | Def. 2.2 (`main.tex:84`) dice "nonempty proper"; el cambio no se propagó: el Teo. 5.1(a) (`:236`) dice "some proper R", la prueba (`:241`) atribuye a "proper" lo que es no vacío, y el Ej. 4.3 (`:208`) cuenta R = ∅ entre los "26 proper removal sets" (m2, m3). |
| m13 | aplicado bien | `main.tex:93`, `:314`. La fila `:314` atribuye además al Lema 2.4 un resultado que no demuestra (m8). |
| m14 | aplicado bien | `main.tex:268`, `:302`. |
| m15 | aplicado bien | Obs. 3.3, `main.tex:165`; resumen `:56` ("under a constant penalty"); ficha ("penalización constante"). |
| m16 | aplicado bien | 0 `Overfull`, 0 avisos de sustitución de fuente (solo `Font Info`). |
| m17 | aplicado bien | `main.tex:247`. |
| Recortes 1–8 | aplicados (5 y 6 con matiz) | 10 páginas exactas; 0 "??" ni referencias indefinidas. El límite de 10 pp. se cumple sin exceso; no propongo recortes adicionales. |

Balance: 22 bien aplicados (incluidos M6 y M7 con matiz aceptable), 2 a medias (m11, m12), 1 aplicado con error nuevo (m10), 0 no aplicados (25 hallazgos; los recortes se cuentan aparte).

## Hallazgos nuevos

### Bloqueantes

Ninguno.

### Mayores

**M1. "Never triggered in the reference runs" es falso: la guarda KKT se activa 91 veces en E0, y el código no registra activaciones.**
Ubicación: `main.tex:330` (Limitations: "every fit is therefore KKT-checked with a coordinate-descent fallback, never triggered in the reference runs"); `main.tex:338` (Solver: "which happens only on exact ties of correlations … and never in the reference runs"); `lasso_fragility.py:44` (docstring: "In the reference runs (Gaussian designs) the fallback is never needed"); `CONTINUIDAD_TCD001_20260930.md:32`; respuesta a B1.
Evidencia: instrumenté `lasso_lars` en una copia (contador de llamadas y de retrocesos) y repetí la corrida completa con las semillas publicadas:

| Script | Ajustes | Retrocesos | Máx. error KKT activo / max(1, μ) |
|---|---|---|---|
| `exact_examples.py` (E0) | 950 | **91** | 6.2 (antes del retroceso) |
| `run_validation.py` (E1) | 16 191 | 0 | 5.0·10⁻¹⁵ |
| `run_fragility.py` (E2/E3/E5) | 117 708 | 0 | 7.6·10⁻¹⁵ |
| `run_scaling.py` (E4) | 10 365 | 0 | 3.6·10⁻¹⁴ |

Los 91 casos de E0 son reajustes de la búsqueda sobre datos enteros con 2–4 filas, todos con X de rango completo y un empate exacto |x₁ᵀy| = |x₂ᵀy| en la entrada (clasificación automática en `scratchpad/referee2_TCD001/e0test/`). Con la guarda desactivada, `examples.json` sale idéntico al publicado. La guarda no cambia ningún número, pero E0 forma parte de la corrida de referencia (Apéndice A: "`exact_examples.py` (E0)"), así que la afirmación es falsa. Además, nada en el código permitía comprobarla: no hay contador ni registro.
Corrección: (i) Código: añadir en `lasso_fragility.py` un contador `KKT_FALLBACKS = {"calls": 0, "fallbacks": 0}` que `lasso_lars` incremente; cada script lo vuelca en `meta` de su JSON y `make_numbers.py` lo convierte en macros. (ii) `main.tex:330`: "…every fit is therefore KKT-checked with a coordinate-descent fallback. The fallback was triggered only in the integer-data search of E0 (\EzeroFallbacks{} of \EzeroFits{} fits, all exact ties of $|x_j^{\top}y|$ at entry; the examples are identical with and without it) and never in E1–E5 (0 of \EoneToFiveFits{} fits)." (iii) Hacer el mismo cambio en `:338`, en el docstring y en CONTINUIDAD. (iv) En la respuesta a B1, "en las corridas de referencia el retroceso nunca se activa" debe limitarse a E1–E5.

**M2. E4 y la tabla de afirmaciones: el argumento de la "resolución del cronómetro" es falso, la familia B queda fuera y la conclusión sobre el coste del greedy está sobreafirmada.**
Ubicación: `main.tex:289` ("the heuristic becomes cheap at the sizes where its accuracy drops below the criterion … ratios at n ≤ 18, where the exhaustive search takes under 10 ms, are dominated by timer resolution"); tabla de afirmaciones `:322` ("the one-step greedy is the most accurate and cheap only for n ≥ 22 (E3, E4)"); ficha (ES/EN, "a n = 34 el greedy cuesta el 7 % con 89 % de exactitud"); README `:41`.
Evidencia (de `results/scaling.json`; la resolución de `perf_counter` es 1 ns):

| fam. | n | t exhaustivo mediano | t greedy mediano | cociente mediano | greedy exacto |
|---|---|---|---|---|---|
| A | 10 / 14 / 18 | 0.14 / 0.66 / 0.36 ms | 1.5 / 2.5 / 2.0 ms | 9.4 / 4.4 / 5.5 | — |
| A | 22 / 26 / 30 / 34 | 2.4 / 2.5 / 3.8 / 52 ms | 3.2 / 2.8 / 2.8 / 3.9 ms | 1.37 / 1.63 / 0.69 / 0.073 | 30/39, 25/27, 23/28, 17/19 |
| B | 10 … 34 | 0.12–0.15 ms | 1.2–1.4 ms | 8.1–10.4 en todos los n | ≥ 95 % |

(i) Los cocientes a n ≤ 18 no son artefactos: son el coste real de los reajustes frente a un lote vectorizado de tests. El umbral "10 ms" tampoco separa nada, porque a n = 22–30 en A el tiempo exhaustivo también está por debajo de 10 ms y esos cocientes sí se citan. (ii) En la familia B el greedy es entre 8 y 11 veces más caro que la búsqueda exhaustiva en todos los n ≤ 34, y E4 no lo menciona. (iii) "Cheap only for n ≥ 22" no se sostiene: en A el cociente mediano es mayor que 1 a n = 22 y 26, menor que 1 solo a n ≥ 30 y menor que 0.10 solo a n = 34, con 20 instancias. (iv) "Where its accuracy drops below the criterion": a n = 34 son 17 de 19 instancias (89 %, e.t. 7 puntos, a 0.15 e.t. del umbral) y la exactitud no decrece de forma monótona con n (77, 93, 82 y 89 % para n = 22, 26, 30 y 34). El texto de E3 rehúsa leer como fracaso un déficit de 1.7 e.t. y E4 lee como caída uno de 0.15 e.t. (v) Los cocientes temporales varían mucho de una corrida a otra. En mi repetición, con el mismo código y las mismas semillas, salieron 0.595 en lugar de 1.361 (A, n = 22), 0.055 en lugar de 0.070 (A, n = 34), 0.683 en lugar de 0.774 y 0.50 en lugar de 0.68 (medianas agrupadas con n ≥ 22). Tres decimales son precisión espuria. Ningún veredicto de E3 cambia (mínimo bruto 0.45 frente a 0.46 publicado; ajustado 0.26).
Corrección: sustituir en `main.tex:289`, desde "At $n=34$", por: "At $n=34$ its median cost was \EfourAThirtyfourCostOnestep{} of the exhaustive search, the only size at which it falls below the 10\% threshold, while it was exact in 17 of the 19 instances with finite $f$ (89\%, standard error 7 points), so 20 instances do not decide the accuracy part at that size. For $n\le26$ in family A, and at every $n\le34$ in family B, the greedy is slower than the exhaustive search (median ratios 1.3–9 in A and 8–11 in B): when $f$ is small, one batch of $n$ closed-form tests (about 0.1~ms) beats a single refit. Cost ratios vary by up to a factor of two between repeated runs on the shared machine and are given to two significant digits." Borrar "dominated by timer resolution". En `:322`: "…the one-step greedy is the most accurate; it is cheaper than the exhaustive search only in family A for $n\ge30$ and below the cost threshold only at $n=34$ (E3, E4)". En la ficha (ES): "(en la familia A, a n = 34 el greedy cuesta en torno al 6–7 % de la búsqueda exhaustiva con 17 de 19 instancias exactas; en la familia B es 8–11 veces más caro a todos los tamaños)"; lo mismo en EN y en README `:41`. Imprimir los cocientes con dos cifras significativas (`make_numbers.py`, macros `Efour*Cost*`).

**M3. Obs. 3.5: la implicación "f_LEAVE(j) > ⌈n/2⌉ ⇒ Π_j = 1", etiquetada "proved here", necesita unicidad en cada submuestra.**
Ubicación: `main.tex:188`; tabla de afirmaciones `:319`.
Problema: por la Def. 2.2 (`:84`), R es testigo solo si el minimizador en D∖R es único. Si alguna submuestra de tamaño ⌊n/2⌋ tiene minimizadores no únicos, ese R no es testigo aunque el solver devuelva una solución sin j, de modo que f_LEAVE(j) > ⌈n/2⌉ no impide Π_j < 1. Es la misma salvedad que la ronda 1 (M1) impuso a la Prop. 3.1 y que se añadió allí pero no aquí. Con datos enteros (Ej. 4.3, submuestras de 2 filas) la no unicidad es real; en E0 hubo empates exactos en reajustes de 2 filas.
Corrección: "If the Lasso minimiser on every subsample of size $\lfloor n/2\rfloor$ is unique (with probability one for designs with a continuous distribution), then $f_{\tsc{leave}(j)}(D)>\lceil n/2\rceil$ under that rule implies $\Pi_j=1$." Aprovechar para precisar la regla: "in the original paper the Lasso is $\lVert Y-X\beta\rVert_2^2+\lambda\lVert\beta\rVert_1$ with $\lambda$ fixed across subsamples, i.e. rule C" (ver Bibliografía).

### Menores

**m1.** `main.tex:63`: "selection witnesses for $p=1$ are easy, and the case $p\ge2$ is open" contradice la Obs. 5.2(ii) (`:247`): la deselección para p ≥ 2 hereda la dureza; lo abierto es la selección (Conj. 5.3) y la dureza fuerte. Escribir: "…selection witnesses for $p=1$ are easy; deselection for $p\ge2$ inherits the hardness, and the complexity of selection witnesses for $p\ge2$ is open (Conjecture~\ref{conj:enter})."

**m2.** Teo. 5.1(a). El enunciado (`main.tex:236`) dice "some proper $R\subsetneq[n]$" y debe decir "some nonempty proper $R$", como la Def. 2.2. En la prueba (`:241`), "proper because $t<\sum_ib_i$ forces $K'\neq[m]$" invierte los papeles: $R=[n]\setminus(K'\cup\{m+1\})$ es propio porque $m+1\notin R$, y no vacío porque $K'\neq[m]$. Escribir: "nonempty because $t<\sum_ib_i$ forces $K'\neq[m]$, and proper because $m+1\notin R$." La reducción, la pertenencia a NP, el tratamiento de ambas reglas ($\mu_k\in(0,\tfrac12]$, suma entera ⇒ $|\Sigma|\le\mu_k\iff\Sigma=0$), la unicidad trivial con p = 1 y la parte (b) son correctos (verificados paso a paso).

**m3.** Ej. 4.3 (`main.tex:208`): "all \ExTwoSubsets{} proper removal sets of this instance are exactly verifiable". Los 26 son los R con |R| ≤ 3 = n − 2 incluido R = ∅ (`exact_examples.py:197`, `range(0, n - 1)`), es decir, D y 25 conjuntos no vacíos. Quedan fuera los 5 conjuntos propios con |R| = 4. Escribir "all 26 removal sets with $|R|\le n-2$ (including $R=\emptyset$)", o extender el bucle a `range(0, n)` y regenerar.

**m4.** `main.tex:256`: "whose output satisfies the KKT equalities to $10^{-14}$" es un número tecleado que ningún script produce, contra lo que dice el Apéndice A ("no number in the text is typed"). Medido por mí: el error activo relativo a max(1, μ) llega a 3.6·10⁻¹⁴ en E4, lo que en valor absoluto es ≈ 10⁻¹² con μ ≈ 50. Registrar el máximo en el contador de M1 y citarlo con una macro, o escribir "to about $10^{-13}$ relative to $\mu$".

**m5.** `main.tex:289`: "the median greedy witness has \EfourAFourhundredMedian{} observations" imprime 10, pero la mediana es 10.5 (`scaling.json`, `g_onestep_C_median` = 10.5; `make_numbers.py:303` usa `:.0f`, que redondea 10.5 a 10). Usar `:.1f` o `:g` en `:303` y `:289`; README `:41` repite "10 observaciones".

**m6.** E3 usa el objetivo ANY sin signos (`run_fragility.py`, `TARGETS = ["any", …]`, exacto `f_any_C`) y E2 el ANY con signos; el texto (`main.tex:272`) no lo dice. Como coinciden en las 480 instancias (`\EtwoASignedNeUnsignedCount` = `\EtwoBSignedNeUnsignedCount` = 0), basta una frase: "E3 uses the unsigned \tsc{any} target, which coincided with the signed one in every instance."

**m7.** Cor. 3.2 (`main.tex:154`): añadir la convención para S = ∅ ("if $S=\emptyset$, $m=+\infty$ and the first term is $0$"), que el código aplica (`lasso_fragility.py:241`) y que se da en 8 instancias de B.

**m8.** Tabla de afirmaciones, `main.tex:314`: "uniqueness under full rank of $X_E$ (Lemma~\ref{lem:rank})". El Lema 2.4 demuestra solo la dirección "único ⇒ X_S de rango completo"; la unicidad bajo rango completo de X_E es de \citet{tibshirani2013}. Escribir "(Lemma~\ref{lem:rank}; \citealp{tibshirani2013})".

**m9.** Cociente ajustado: el texto (`main.tex:260`, "removing one refit's worth of time") y la leyenda de la Tabla 2 (`:284`, "removes one refit (the heuristic's initial fit)") no describen el cálculo. El código resta el tiempo medio por paso, t·(1 − 1/n_refit) (`make_numbers.py:204–218`), que incluye la puntuación y favorece a la heurística. Escribir en la leyenda: "adj. subtracts the heuristic's mean time per refit step (at least one refit)".

**m10.** Tabla 2: la fila (B, any, sorted scores) imprime "100% ± 0.4" (237/238 redondeado). Imprimir una cifra decimal cuando el valor esté en [99.5, 100) o el recuento entero.

**m11.** Código: el resultado del retroceso a descenso por coordenadas no se vuelve a verificar (`lasso_fragility.py:54–56`). Añadir una segunda comprobación KKT y lanzar un error si falla. El docstring de `kkt_residuals` (`:77`) anuncia tres valores y devuelve dos.

**m12.** `CONTINUIDAD_TCD001_20260930.md:29` conserva el valor de v0.1 ("a n = 34 el costo baja a 0.067"); en v0.2 es 0.070. Actualizarlo, junto con la línea `:32` (M1).

**m13.** `main.tex:258/272`: el criterio compara medianas de cocientes por instancia, pero la Tabla 2 no da su dispersión, y M2(v) muestra que esta es grande. Añadir en `results/fragility.md` el rango intercuartílico de los cocientes. No es imprescindible en el PDF.

## Bibliografía

Red: `rss.onlinelibrary.wiley.com`, `stat.ethz.ch`, `people.math.ethz.ch` y `semanticscholar.org` bloqueados por el proxy (EGRESS_BLOCKED); WebSearch operativo. No intenté Crossref ni arXiv directamente; las comprobaciones son por resultados de búsqueda.

| Entrada | Estado | Corrección / nota |
|---|---|---|
| woodbury1950 (nueva) | verificada | Woodbury, M. A., *Inverting modified matrices*, Statistical Research Group, Memorandum Report 42, Princeton, 1950, 4 pp. (MR0038136). Correcta. |
| kuschnig2021 (corregida) | verificada | CESifo Working Paper No. 8981, 2021 (ifo.de, RePEc `ces/ceswps/_8981`, EconStor 10419/235351, SSRN 3819102). Correcta. |
| broderick2020 ("v4 (2023)") | no reverificada | Aceptada en la ronda 1. |
| meinshausen2010 | verificada (datos) | JRSS-B 72(4), 417–473 (EconPapers). Según los fragmentos indexados del texto, el Lasso se escribe ‖Y − Xβ‖²₂ + λΣ|β_k|, sin 1/n, con λ fijo en las submuestras, lo que es la regla C en la notación del manuscrito. No pude abrir el PDF (dominios bloqueados). Permite cerrar el pendiente 1 de la respuesta (M3). |
| (falta) Rubinstein, I. y Hopkins, S. B. (2025), *Robustness auditing for linear regression: to singularity and beyond*, ICLR 2025, arXiv:2410.07916 | añadir | La ronda 1 la llamó "continuación de Freund–Hopkins" y la respuesta no la citó por no poder comprobar los autores: son Ittai Rubinstein y Samuel B. Hopkins. Es pertinente para la Prop. 3.4 (cotas inferiores certificadas del número de eliminaciones en MCO) y para la Obs. 5.2(iii). |
| (opcional) Konrad, L. D. y Kuschnig, N. (2026), *Finding most influential sets*, ICML 2026, arXiv:2606.05919 | considerar | Reduce la búsqueda de conjuntos más influyentes con efectos lineal-fraccionales a problemas top-k, la misma estructura que el Teo. 5.1(b) y la Prop. 3.4. Una frase en la introducción evitaría que un lector externo lo eche en falta. |
| moitra2022, freund2023, tibshirani2013 | verificadas en la ronda 1 | Sin cambios. |
| tibshirani1996, efron2004, osborne2000, zhao2006, wainwright2009, cook1977, hampel1974, pedregosa2011, amaldi1995, amaldi1998, sherman1950, hager1989, buhlmann2011, belsley1980, garey1979, karp1972 | no reverificadas; estándar | Datos coincidentes con los de uso común. |

Uso de las citas: todas respaldan lo que se afirma. La de meinshausen2010 en la Obs. 3.5 puede precisarse (M3).

## Verificación computacional

Todo en copias dentro de `scratchpad/referee2_TCD001/` (`repro/`, `e0test/`, `compile/`); no se tocó la carpeta del artículo salvo este informe. CPU total ≈ 2.3 min.

| Qué | Tiempo (CPU) | Resultado |
|---|---|---|
| `lars_path` en X = I₂, y = (3,3), μ = 1 (`lars_tie.py`) | < 1 s | Afirmación del autor reproducida: `lars_path(X, y, method="lasso", alpha_min=0.5)` (también `"lar"`) devuelve (5, 2), con nodos α = [1.5, 1.5, 0.5] y sin aviso; gradiente Xᵀ(y − Xβ) = (−2, 1), error KKT activo 3.0. Descenso por coordenadas: (2, 2); empate roto con 10⁻⁹: (2, 2). Otros empates: y = (5,5) → (9, 4); y = (3,−3) → (5, −2). sklearn 1.9.1, la misma versión de la corrida de referencia. |
| `check_b1_counterexample.py` | 1.2 s | Pasa (ι = +∞, `rank_ok` = False, instancia genérica intacta). |
| Corrida de referencia completa (E0, E1, E2/E3/E5, E4), copia con contador KKT | 2.0 + 9.7 + 50.9 + 42.4 s | Contadores en M1. `make_numbers.py` sobre los JSON reproducidos: 494 macros, **422 no temporales idénticas** a `numbers.tex` publicado (todos los recuentos, fracciones, medias, veredictos, ejemplos exactos y certificados); las 72 que difieren son tiempos o cocientes de coste. Variación: rendimiento 1.1 → 1.3 μs y 442 → 558 μs (×399 → ×435); cocientes de E3 dentro de ±0.04, con mínimo bruto 0.45 y ajustado 0.26, de modo que 0/18 se mantiene; E4 con variaciones de hasta ×2.3 (M2). |
| E0 con la guarda activada y desactivada | 2 × 2 s | `examples.json` idéntico en ambos casos al publicado. Los 91 retrocesos son empates exactos en la entrada con X de rango completo. |
| Coherencia interna de `results/*.json` | — | k* < f en todas las instancias de E2 y E4 (validez de la Prop. 3.4); ningún greedy por debajo del mínimo exacto; los 2 "not found" de B están entre las 8 instancias de soporte vacío, como dice el texto; ANY con y sin signos coinciden en las 480 instancias de E2. |
| Prueba de la Prop. 3.1 y del Teo. 5.1 | — | Releídas paso a paso: Woodbury, la identidad y_R + (I−H)⁻¹H y_R = (I−H)⁻¹y_R, el bloque R del residuo igual a e_R, el término δz en β̃ y c̃, la unicidad con desigualdades estrictas; la reducción desde Subset Sum (T ≥ 1 > ½ ≥ μ_k; Σ entero ⇒ Σ = 0; m+1 ∈ K obligatorio), NP en ambas reglas y la parte (b). Ej. 4.3 recalculado a mano en D∖{3,4}: β̂₂ = −5/12, c₁ = 11/4 < 7/2 < |x₁ᵀy| = 4. |
| Compilación (`latexmk` en copia) | — | 10 pp., 0 errores, 0 referencias o citas indefinidas, 0 "??" (`pdftotext`), 0 `Overfull`, 2 `Underfull \hbox` (badness 4217) en la tabla de afirmaciones. |

Extensión: 10 páginas exactas con cuerpo de 10 pt y márgenes de 0.9 in. Se cumple el objetivo; no hacen falta recortes. Las correcciones M2 y M3 añaden 3–4 líneas netas, que se compensan borrando la frase sobre la resolución del cronómetro.

## Lista final de acciones (por prioridad)

1. Añade un contador de retrocesos KKT a `lasso_lars`, vuélcalo en el `meta` de cada JSON y sustituye "never triggered in the reference runs" (`main.tex:330`, `:338`, docstring `lasso_fragility.py:44`, CONTINUIDAD `:32`) por la redacción de M1 (91 de 950 en E0, solo empates exactos; 0 en E1–E5).
2. Reescribe la frase de E4 sobre el coste del greedy (`main.tex:289`) y la fila `:322` de la tabla de afirmaciones según M2: borra "dominated by timer resolution", menciona la familia B (cocientes 8–11), limita "cheap" a A con n = 34 y trata 17/19 con su error típico. Corrige la ficha (ES/EN) y README `:41` para decir "familia A". Imprime los cocientes con dos cifras significativas.
3. Añade a la Obs. 3.5 la hipótesis de unicidad en cada submuestra y escribe "rule C" para el artículo original (M3).
4. Propaga "nonempty" al Teo. 5.1(a) y corrige "proper because…" en la prueba (m2); corrige "26 proper removal sets" en el Ej. 4.3 o extiende la comprobación a |R| = 4 (m3).
5. Corrige "the case $p\ge2$ is open" en la introducción (m1).
6. Sustituye el "10⁻¹⁴" tecleado por una macro medida (m4) y corrige la mediana 10 → 10.5 a n = 400 (m5, `make_numbers.py:303`, README).
7. Declara que E3 usa ANY sin signos (m6); añade la convención S = ∅ al Cor. 3.2 (m7); corrige la atribución de la fila `:314` (m8); describe el ajuste del cociente tal como se calcula (m9); arregla "100% ± 0.4" (m10).
8. Verifica la salida del retroceso a descenso por coordenadas y corrige el docstring de `kkt_residuals` (m11); actualiza "0.067" en CONTINUIDAD (m12); añade el rango intercuartílico de los cocientes a `results/fragility.md` (m13).
9. Cita Rubinstein y Hopkins (ICLR 2025) junto a la Prop. 3.4 y la Obs. 5.2(iii); considera citar Konrad y Kuschnig (ICML 2026).
10. Regenera `numbers.tex` y el PDF con `build.sh`, y comprueba de nuevo 0 "??" y 10 páginas.
