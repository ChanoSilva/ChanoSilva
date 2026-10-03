# SVMF001 — Respuesta del autor a la ronda 3 de revisión interna (informe del 03/10/2026)

Respuesta redactada el 03/10/2026 en una sesión de Claude Code (session_01MTmjU2K8b4sgpjjL3JTtDz), en el papel de autor. Informe atendido: `REFEREE_SVMF001_ronda3_20261003.md` (veredicto: cambios menores, solo de texto; 0 bloqueantes, 3 mayores, 10 menores; Prop. 3.6, Cor. 3.7, Lemas 3.8–3.10, Teorema 3.11 y Cor. 3.12 de v0.4 confirmados correctos; Obs. 3.13 heurística).

Entregable: manuscrito **v0.5** (fecha fija 3 October 2026; `manuscript/main.pdf`, **15 páginas** frente a 16 de v0.4; 0 errores, 0 advertencias, 0 cajas desbordadas, 0 referencias o citas indefinidas, 0 "??" en el texto extraído), `experiments/make_knn_numbers.py` modificado (m7 y macros de M2), `manuscript/refs.bib` (+1 entrada, +1 DOI), README, ficha propuesta y nota de continuidad (sección "Ronda 3 de revisión interna (03/10/2026)").

**Recuento:** 13 hallazgos (0 B + 3 M + 10 m): **10 aceptados, 3 aceptados con matiz (M2, M3, m3), 0 rebatidos.** Ningún número de la corrida de referencia ni de los resultados congelados de `theory/` cambia; cambian el estado de dos afirmaciones (M1, M2), la numeración de §3 (recorte 1 de M3) y el conjunto de macros emitidas (m7, M2).

## Decisión general

No se vuelve a correr la comparación ni `theory/check_knn_localisation.py` (no se ejecutó en su sitio; `theory/` no se tocó: listado con fechas idéntico antes y después). Todos los cambios son de texto, salvo `experiments/make_knn_numbers.py`, que sigue leyendo el JSON congelado, comprobando su SHA-256 (`f035b43d…`, verificado) y rederivando las 51 macros guardadas.

**Renumeración de §3** (consecuencia del recorte 1 de M3, que pone primero el resultado general): Prop. 3.6 → **Prop. 3.2**; Prop. 3.2 → **Cor. 3.3**; Obs. 3.3 → 3.4; Prop. 3.4 → 3.5; Cor. 3.5 → 3.6; Cor. 3.7 = 3.7; Lema 3.8 → **Lema C.1**; Lemas 3.9–3.10 → 3.8–3.9; Teorema 3.11 → **3.10**; Cor. 3.12 → **3.11**; Obs. 3.13 → **3.12**. Simulaciones: D5 nueva (la comprobación Monte Carlo del Cor. 3.7), D5–D7 → D6–D8. Tablas: saturación (antes Tabla 3) fuera del PDF; criterio = Tabla 4; afirmaciones = Tabla 5. Abajo se usan los números de v0.4 del informe con el nuevo entre paréntesis cuando importa.

## Hallazgos mayores

### M1. Resumen y tabla de afirmaciones frente a la Tabla 5 — **ACEPTADO**

Verificado contra los resultados del preregistro: `results/results.json`, clave `criterion.vb_rbf`: `n_ci_positive = 1`, `majority_criterion = false`, `named_regimes = ["linear"]`, `added_value = true`; las otras tres familias, `added_value = false`. La regla del preregistro (cláusula (B) "un régimen nombrado en cuyos conjuntos se cumpla (A) sin que ningún conjunto fuera del régimen tenga IC enteramente por debajo de 0") la cumple por la letra VB-RBF-SVM en el régimen lineal (un solo conjunto). El resumen y la fila de la tabla decían lo contrario; el árbitro tiene razón.
- Resumen: "No family met its majority clause: of 24 … intervals, 9 lie below zero and 1 above (about 1.2 expected by chance). That interval makes the variable-bandwidth family meet the regime clause by the letter, in the one-data-set linear regime, where the linear reference already contains the Bayes rule: a flaw of the criterion, not added value." (No se escribe "donde la teoría descarta toda ganancia": el Lema 3.1 solo dice que la referencia lineal ya contiene la regla de Bayes y que solo queda el término de estimación.)
- Tabla de afirmaciones (Tabla 5): "No family meets the majority clause; VB-RBF-SVM meets the regime clause by the letter, in the one-data-set linear regime (a flaw of the criterion), through the only interval above zero, which is against the selected reference, compatible with chance and absent against its own global member" → *measured*.
- §5.3 ya era correcto; se precisa "in that regime the reference class contains the Bayes rule, so that only the estimation term is available (Lemma 3.1)" (antes: "no reduction of excess risk is available", algo más fuerte de lo que prueba §3). Lo mismo en §5.1 ("where the linear reference contains the Bayes rule" en lugar de "where Section 3 says that local adaptation cannot reduce the excess risk").
- README (punto 3), ficha ES/EN (estado: "ninguna familia cumple la cláusula de mayoría … la de régimen se cumple solo por la letra"; hallazgos). El estado de la ficha decía "resultado negativo bajo criterio predefinido" sin matiz; ahora dice cuál cláusula.

### M2. "Verified numerically" de la Obs. 3.13 (ahora 3.12) — **ACEPTADO CON MATIZ**

Verificado en el JSON congelado (bloque P4): ρ = ¼, μ = 0.5: 88.4 ± 4.0, 88.4 ± 4.5, 83.9 ± 4.5 en n = 2 000, 8 000, 32 000 frente a Q = 94.37 (z = −2.31 en n = 32 000, sin acercarse); ρ = ¼, μ = 1.645: 210 ± 19, 65 ± 16, 19.1 ± 1.1 frente a 20.29 (z = −1.09 solo en el último n); ρ = ½: |z| ≤ 1.54 en los 6 casos. El matiz: la redacción propuesta por el árbitro ("within about 10 % at ρ = ¼ and n = 32 000") es falsa por la letra para μ = 0.5 (1 − 83.91/94.37 = 11.1 %); se usa la cifra exacta, por macro.
- Obs. 3.12, estado: **"heuristic, not proved; simulations agree only in part"**; texto: "The simulated ratios (Appendix B, D8) agree with Q(½) at every n tested, approach Q(¼) only at the largest n for μ = 1.645, and stay 11 % below it (z = −2.3) at n = 32 000 for μ = 0.5: at ρ = ¼ the heuristic is not confirmed."
- Apéndice B (D8): todas las cifras, incluidas 88 ± 4, 88 ± 4, 84 ± 5 frente a 94.4 y "within 1.6 standard errors of Q(½) at every n and μ".
- Tabla de afirmaciones: la inflación 1/(ρv) sale de la fila "verified, not proved" y tiene fila propia, estado "heuristic; simulations agree only in part", con 11 % y z = −2.3.
- README: "apoyada por la simulación solo en parte … 84 ± 5 frente a 94.4, z = −2.3"; ficha: "heurística que la simulación apoya solo en parte". Siguiente paso (a): "Make Remark 3.12 rigorous **or correct it**".
- Macros nuevas (de `make_knn_numbers.py`, desde el JSON congelado): `\KLRatioQuarterHardA` = `\KLRatioQuarterHardB` = 88 ± 4, `\KLZQuarterHardC` = −2.3, `\KLGapQuarterHardPct` = 11, `\KLHalfMaxZUp` = 1.6 (techo de 1.54, es una cota), y `\KLZQuarterMainC` = −1.1, `\KLGapQuarterMainPct` = 6 (emitidas, no usadas).

### M3. Extensión: 16 páginas frente a ≤ 14 — **ACEPTADO CON MATIZ (15 páginas)**

Aplicados los 11 recortes:
1. **Prop. 3.6 primero** (ahora Prop. 3.2) y la de particiones como **Cor. 3.3** con prueba de 4 líneas (W_i = Z_i, I = {i : Z_i = Z}, K | Z = j ~ Bin(n, p_j); estrictez por P(N_j = n − 1) > 0). Se elimina el argumento de condicionamiento duplicado y el párrafo "Proposition 3.2 is the case …".
2. Lema 3.8 → **Lema C.1** (enunciado y prueba en el apéndice C), con una frase en §3 ("Neighbourhoods in the signal coordinate").
3. Prueba del Lema 3.9 (ahora 3.8) y el párrafo "So the kNN-localised …" → apéndice C.
4. Cor. 3.7: identidad y tres cocientes; Monte Carlo → apéndice B (D5).
5. Cor. 3.12 (3.11): enunciado y límites; simulaciones → apéndice B (D6–D7).
6. Obs. 3.13 (3.12): heurística, Q(ρ) y una frase con el resultado de la simulación; cocientes → D8.
7. Celda gaussiana: dos líneas (3 de 800; 2 pliegues de VB sobre su RBF; 1 de selección). Matiz: el árbitro proponía remitir a `results/tables.md`, pero esa cuenta pliegue a pliegue no está allí; se deja la frase corta autocontenida y se quita la explicación de por qué la referencia seleccionada queda bajo ambas medias (el pie de la Tabla 2 ya lo dice en general).
8. Título y Scope sin historia de versiones (va al README).
9. Resumen sin el detalle de saturación (y algo más compacto en general).
10. Limitations sin repetir el alcance v0.4.
11. Tabla de saturación → `results/tables.md` (ya contenía las mismas cuentas, "lower/upper of N", con "-" para el miembro global); los recuentos que sostienen "grid-limited" siguen en el texto por macro.

Además: Fig. 2 (intervalos pareados) fuera del PDF (sus intervalos están en la Tabla 2 y en `results/tables.md`; la figura sigue en `figures/fig_paired.pdf` y el texto remite a ella), y condensados el párrafo de comparación pareada, el del preregistro (se conserva todo: hora, commit posterior, registro de sesión, SHA-256 de las 40 líneas), los de VB-RBF, robustez y veredicto, la tabla de afirmaciones, el apéndice A (la lista de scripts con sus salidas está en el README) y D1–D4.

Resultado: **16 → 15 páginas** (14 de texto y apéndices + 1 de bibliografía). **No se llegó a 14**: trasladar texto a los apéndices no acorta el documento, y el ahorro real de los recortes 1–11 fue ≈ 0.7 páginas; la Fig. 2 y las condensaciones dieron el resto. Para 14 haría falta sacar ≈ 0.6 páginas más, es decir, la Fig. 1 y la Tabla 3 (anidada, cuyos números solo están en `results/posthoc_oracle.json`, no en un `.md`) o la Tabla 1; se juzga peor que una página de exceso. Ninguna prueba salió del PDF; márgenes, letra y espaciados sin cambios.

## Hallazgos menores

- **m1 (ACEPTADO).** §2: "(S, x) ↦ A(S)(x) jointly measurable; a randomised rule draws its internal randomness independently of everything else". Prop. 3.2: "with learning curve R_A under the law P of (X, Y) (any internal randomness of A is part of R_A, not of U)"; "in a measurable metric (e.g. a norm on R^p)".
- **m2 (ACEPTADO).** Tras el Lema 3.9: "The lemma and Theorem 3.10(ii) concern exact minimisers; the experiment and the simulations use libsvm with its default tolerance (10⁻³), which returns approximate ones. The radius r_0 comes from crude bounds and is far from sharp." D7: la verificación de las 6 646 consultas mixtas con radio < r_0 "checks the implementation only, since r_0 is far from sharp (an adversarial search during the internal review found the first minority predictions only at several multiples of r_0, more for larger k)". Las cifras del árbitro (≈ 3–7·r_0 con k = 3, 6–14·r_0 con k = 5, 12–26·r_0 con k = 9) no se pasan al PDF porque salen de scripts fuera del repositorio; constan en la nota de continuidad. (El código predice −1 con valor de decisión exactamente 0, `families.py:118`; con el minimizador exacto el lema da b' > 0 estricto, así que ese empate no aparece en la teoría.)
- **m3 (ACEPTADO CON MATIZ).** Lema C.1: "[proved here; classical argument, see Biau and Devroye]" y en §3 "a classical order-statistics argument; see Biau and Devroye (2015)". Entrada `biau2015` (G. Biau, L. Devroye, *Lectures on the Nearest Neighbor Method*, Springer Series in the Data Sciences, Springer, Cham, 2015) **sin capítulo ni DOI**: la red a Crossref y doi.org está bloqueada en esta sesión (403 del proxy), y el árbitro pedía comprobar capítulo y lema antes de citarlos; queda pendiente.
- **m4 (ACEPTADO).** "because v < 1 (truncating a Gaussian to an interval reduces its variance)".
- **m5 (ACEPTADO).** Tabla de afirmaciones: fila de vecinos con Prop. 3.2, Cor. 3.7, Teorema 3.10, Cor. 3.11 y Lemas 3.8, 3.9 y C.1 → **"proved here; checked by an independent internal referee (round 3)"**; párrafo de entrada de §3 y apéndice C con la misma etiqueta; README y ficha actualizados. `grep "not yet\|aún no"` en manuscrito, README y ficha: 0. La Obs. 3.12 sigue como heurística.
- **m6 (ACEPTADO).** Apéndice B: "Simulations".
- **m7 (ACEPTADO).** `make_knn_numbers.py` sigue verificando las 51 macros guardadas, pero ya **no emite** las 6 que redondean una cota al más cercano: `KLSelMaxZ`, `KLPtwoMaxZ`, `KLPtwoMaxDiff`, `KLPtwoMinGap`, `KLPtwoDallMin`, `KLPtwoDallMax`. `\KLSelMaxZ` (1.4) se usaba ("within … standard errors") y se sustituye por `\KLSelMaxZUp` = techo(1.36) = 1.4: mismo valor, ahora dirigido.
- **m8 (ACEPTADO).** README: "Verificación del integrador".
- **m9 (ACEPTADO).** Cor. 3.11: "Fixed k is eventually worse than the global nearest-centroid rule"; se añade que la comparación de la kNN-SVM con la SVM lineal global (cuya consistencia no se prueba) es solo numérica (D7).
- **m10 (ACEPTADO).** Teorema 3.10(i): "with n → ∞ first, a mixed neighbourhood shrinks to a point and its threshold falls on either side of the query with probability ½, an artefact of fixed k, not of k = ρn (Remark 3.12)".

## Bibliografía

- cover1967: `doi = {10.1109/TIT.1967.1053964}` añadido (dado por el árbitro; coincide con el DOI habitual; no se pudo consultar Crossref).
- biau2015: nueva (m3). 26 entradas, todas citadas.
- devroye1996 (capítulo opcional): no se añade capítulo (no verificable aquí).

## Lista final de acciones del árbitro

| # | acción | estado |
|---|---|---|
| 1 | Resumen y fila de la tabla (M1) | hecho |
| 2 | Etiqueta de la Obs. 3.13, fila 4, README:31 y README:42 (M2) | hecho (cifra 11 %, no "≈ 10 %") |
| 3 | ≤ 14 páginas con los recortes 1–11 (M3) | 11 recortes hechos + Fig. 2 fuera; 15 páginas |
| 4 | Hipótesis de la Prop. 3.6 (m1) | hecho |
| 5 | Minimizadores exactos y holgura de r_0 (m2) | hecho |
| 6 | Cita del Lema 3.8 y DOI de cover1967 (m3) | hecho, sin capítulo ni DOI de Biau–Devroye |
| 7 | m4, m6, m9, m10 | hecho |
| 8 | Tabla de afirmaciones y "not yet checked" (m5) | hecho |
| 9 | Macros redondeadas al más cercano (m7); "independiente" (m8) | hecho |
| 10 | Ejecutar `check_knn_localisation.py` en una copia y comparar | no en esta ronda (presupuesto ≤ 5 min de CPU; el integrador ya lo hizo en v0.4: salida idéntica salvo el tiempo); queda abierto para un árbitro |

## Qué cambió en los números

Ningún número de la corrida de referencia, del ejemplo exacto ni del JSON congelado de `theory/` cambia; `numbers.tex` es idéntico al de v0.4 y ninguna macro usada de `knn_numbers.tex` cambia de valor. Cambios:
- Macros que dejan de emitirse (m7): `\KLSelMaxZ` (1.4), `\KLPtwoMaxZ` (1.3), `\KLPtwoMaxDiff` (0.0023), `\KLPtwoMinGap` (0.024), `\KLPtwoDallMin` (0.076), `\KLPtwoDallMax` (0.109).
- Macros nuevas: `\KLSelMaxZUp` = 1.4 (sustituye a `\KLSelMaxZ`, mismo valor), `\KLRatioQuarterHardA` = 88 ± 4, `\KLRatioQuarterHardB` = 88 ± 4, `\KLZQuarterHardC` = −2.3, `\KLGapQuarterHardPct` = 11, `\KLHalfMaxZUp` = 1.6, `\KLZQuarterMainC` = −1.1, `\KLGapQuarterMainPct` = 6.
- Cifras que el PDF ya no muestra (siguen en `results/`): la explicación de la referencia seleccionada en el gaussiano (`\GaussPickRbf…`, `\AccMainGauss…`), los recuentos v0.1 de C máximo de la RBF y la Monte Carlo del Cor. 3.6 (en `results/exact_example.md`).

## Compilación

`manuscript/build.sh` (make_numbers + make_knn_numbers + latexmk + `latexmk -c`): código 0; 0 errores, 0 advertencias, 0 cajas desbordadas (una aparecida con el nuevo título del Cor. 3.3 se corrigió acortándolo), 0 referencias o citas indefinidas, `pdftotext main.pdf - | grep -c '??'` = 0; **15 páginas**; quedan `main.pdf` y `main.bbl`. Páginas renderizadas y revisadas: §3 (pp. 4–6), tabla de afirmaciones y apéndices (pp. 11–13).

## Cómputo

Sin corridas nuevas. `make_knn_numbers.py` y `make_numbers.py` (< 2 s cada uno, varias veces), ≈ 12 compilaciones de 2–4 s, renderizados. Total < 1 min de CPU.

## Qué queda abierto

1. Extensión: 15 páginas frente a ≤ 14 (véase M3).
2. Obs. 3.12 (k = ρn): versión rigurosa o corrección; la simulación la contradice en (ρ, μ) = (¼, 0.5).
3. n_0(k) explícito; SVM local con coordenadas fuera de la métrica; k-means/LLSVM en la coordenada de señal; consistencia de la SVM lineal global; C por validación interna.
4. Reproducción de `theory/check_knn_localisation.py` por un árbitro en una copia (acción 10).
5. Capítulo y DOI de Biau y Devroye (2015).
6. Sin cambios desde la ronda 2: comparaciones limitadas por la rejilla, positivos de robustez como hipótesis, inferencia entre pliegues, predefinición de v0.1.
