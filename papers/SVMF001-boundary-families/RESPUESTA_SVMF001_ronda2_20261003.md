# SVMF001 — Respuesta del autor a la ronda 2 de revisión interna (informe del 03/10/2026)

Respuesta redactada el 03/10/2026 en una sesión de Claude Code (session_01MTmjU2K8b4sgpjjL3JTtDz), en el papel de autor. Informe atendido: `REFEREE_SVMF001_ronda2_20261003.md` (veredicto: cambios mayores, solo de texto; 0 bloqueantes, 7 mayores, 10 menores; reproducción bit a bit; ningún hallazgo cambia el veredicto del criterio).

Entregable: manuscrito **v0.3** (`manuscript/main.pdf`, **12 páginas** frente a 14 de v0.2; 0 errores, 0 advertencias, 0 referencias o citas indefinidas, 0 "??" en el texto extraído), `PREREGISTRO_SVMF001.md` con anotación fechada nueva (líneas 1–40 intactas, SHA-256 verificable), `experiments/bootstrap_coverage.py` y `results/bootstrap_coverage.json` nuevos, `make_numbers.py` ampliado, Fig. 2 redibujada, README, ficha y nota de continuidad actualizados.

**Recuento:** 17 hallazgos (0 B + 7 M + 10 m): **14 aceptados, 3 aceptados con matiz (M5, M7, m5), 0 rebatidos.** Ningún hallazgo cambia el veredicto del criterio ni ningún número de la corrida de referencia; cambian las cifras de comparación "esperadas por azar" (M4) y el estado de dos afirmaciones, que pasan a "measured, grid-limited" (M1, M2).

## Decisión general sobre una nueva corrida

**No se vuelve a correr la comparación en esta ronda.** El preregistro de v0.2 comprometía una sola corrida, el árbitro pide expresamente que la ampliación de rejillas (γ de VB-RBF-SVM por arriba; C de cell-SVM y LLSVM hasta 1000) se haga "en la próxima corrida (no en esta ronda)" bajo un preregistro con commit propio, y ampliar ahora, tras haber visto qué bordes saturan, sería exactamente el tipo de elección de rejilla a posteriori que el preregistro excluye. En su lugar, todo lo afectado por la saturación se marca "measured, grid-limited" en el manuscrito, la tabla de afirmaciones, el README, la ficha, la nota de continuidad y una anotación fechada del preregistro. Ningún número de la corrida de referencia cambia; se añaden macros nuevas (recuentos de saturación por conjunto, esperanzas unilaterales, cobertura simulada del bootstrap, desglose de la celda gaussiana) generadas por `make_numbers.py` desde los mismos JSON.

## Hallazgos mayores

### M1. Empate VB-RBF-SVM/RBF en multiescala limitado por la rejilla — **ACEPTADO**

Verificado sobre `results/results.json` (condición principal): VB-RBF-SVM elige γ = 100·γ_med en 6/10 pliegues de las lunas (configuraciones por pliegue idénticas a las que cita el árbitro), C = 1000 en 4/10 del tablero, y la RBF de referencia C = 1000 en 5/10 del tablero (6/20 en multiescala). La regla del propio preregistro ("si persiste saturación en algún extremo … la afirmación afectada se marca como 'medida, limitada por la rejilla'", línea 36) obligaba a marcar también este empate, y no se hizo. La anotación post-corrida del preregistro (línea 43) y la respuesta de la ronda 1 (B1) decían "γ ya no satura por arriba en ningún conjunto": era cierto solo para la RBF de referencia, falso para VB-RBF-SVM. Cambios:
- `main.tex` §5.1 (párrafo "The variable-bandwidth family"): "This tie is grid-limited too", con los recuentos por macro (`\EdgeMainMoonsVbGammaHi` = 6, `\EdgeMainCheckVbCHi` = 4, `\EdgeMainCheckRbfCHi` = 5, `\EdgeMainMultiRbfGammaHi` = 0 frente a 20/20 en v0.1, `\EdgeMainMultiRbfCHi` = 6) y "with larger grids the comparison could move in either direction".
- Tabla de afirmaciones: fila "VB-RBF-SVM ties the RBF-SVM on the multiscale sets, with its own γ at the top of the grid in 6 of 10 moons folds and C at the top for both in 4–5 of 10 checkerboard folds" → **measured, grid-limited**.
- Resumen: "both outcomes are grid-limited, as the inner cross-validation still selects grid edges there"; veredicto §5.3: "a tie with the RBF-SVM under grids that still bind on both"; limitaciones y siguiente paso (b) con γ por encima de 100·γ_med.
- `PREREGISTRO_SVMF001.md`: anotación fechada nueva que corrige la de la línea 43 sin borrarla. README, ficha (ES/EN) y nota de continuidad: "empate limitado por la rejilla".
- La respuesta de la ronda 1 no se reescribe (es un registro histórico); la corrección consta aquí y en el preregistro.

### M2. "No alcanzan a la RBF" y lectura por el mecanismo de varianza — **ACEPTADO**

Verificado: LLSVM elige (M, C) = (32, 10) a la vez en 18/20 pliegues multiescala (8/10 lunas, 10/10 tablero); cell-SVM C = 10 en 20/20 y (32, 10) a la vez en 11/20; kNN-SVM k = 5 en 20/20. En v0.1 las rejillas de C ya saturaban (cell-SVM C = 10 en 17/20 multiescala; LLSVM en 17/20 multiescala y 10/10 digits) y el preregistro no las amplió: omisión nuestra. El argumento de la ronda 1 ("por debajo de k = 5 o por encima de M = 32 las SVM lineales locales degeneran") no vale para C, como dice el árbitro. Cambios:
- §5.1 (párrafo "Local linear families"): la frase incondicional se sustituye por "what the three families do not do under the grids of Section 4, which bind on both of their hyper-parameters on these sets, is reach the RBF reference (kNN-SVM ties it on the moons)", precedida de los recuentos de saturación conjunta (macros `\EdgeMainMultiLlsvmBothHi` = 18, `\EdgeMainMultiCellBothHi` = 11) y de la declaración de que las rejillas de C no se ampliaron aunque v0.1 ya las saturaba (`\VOneEdgeCellCHi` = 17, `\VOneEdgeLlsvmCHi` = 17), "an omission of our preregistration". También "data-set/edge cells" (m7).
- §5.2: "in line with the variance mechanism" → "consistent with, though not covered by, the variance mechanism of Section 3" (solo para el patrón de kNN-SVM), y se reporta que cell-SVM supera a la RBF y al oráculo en las lunas con 80 puntos de entrenamiento (m4).
- Limitaciones: "where Section 3 shows a variance cost for label-independent partitions; on the multiscale sets the inner cross-validation nonetheless asked for the most local configurations available, so the deficit there is not attributed to that mechanism", más la declaración de las rejillas de C no ampliadas.
- Preregistro (anotación fechada), README, ficha y nota: las rejillas de C de cell-SVM/LLSVM saturaban ya en v0.1 y no se ampliaron.

**Sobre ampliar las rejillas ahora.** No se hace (véase "Decisión general"): sería una ampliación decidida después de ver qué bordes saturan en v0.2, y el preregistro comprometía una sola corrida. Queda como siguiente paso (b) del manuscrito: γ por encima de 100·γ_med, C hasta 1000 para cell-SVM y LLSVM y criterio de robustez, en un preregistro con commit propio antes de tocar el código.

### M3. Prop. 3.2: paréntesis falso en n = 1 — **ACEPTADO**

El contraejemplo es correcto (A = A_nc, n = 1, M = 2: la condición "estrictamente decreciente en {1}" es vacua y E R = ½ = R_nc(1)). Paréntesis corregido a "(in particular, if $n\ge2$ and $\Risk_A$ is strictly decreasing on $\{1,\dots,n\}$)". Junto con m6 (condicionar en $\tilde S=(X_i,Y_i,Z_i)_{i\le n}$). Ningún número cambia.

### M4. Recuentos "esperados por azar" — **ACEPTADO**

Los 1.2 y 2.4 eran 0.05·N (bilaterales) comparados con recuentos de intervalos *por encima* de 0 (unilaterales), y suponían cobertura nominal. Verificación: corrí el `coverage.py` del árbitro (85.0 % con 5 pliegues, 89.9 % con 10, B = 1000) y escribí `experiments/bootstrap_coverage.py`, que reproduce exactamente `bootstrap_ci` (percentil, B = 2000) sobre diferencias normales i.i.d. de media 0 con 20 000 réplicas (11 s): cobertura **89.9 %** con 10 pliegues y **83.5 %** con 5; probabilidad por lado (promedio de ambas colas) 5.1 % y 8.2 %. Resultado en `results/bootstrap_coverage.json`; macros `\CovTen`, `\CovFive`, `\OneSidedTen`, `\OneSidedFive`, `\ExpectedPosMain`, `\ExpectedPosRobust`, etc. Cifras nuevas: esperados por encima de 0 con cobertura nominal 0.6 (principal, 24) y 1.2 (robustez, 48); con la cobertura simulada **1.2 y 4.0**. Con la nominal, P(X ≥ 4 | Bin(48, 0.025)) = 0.03 (los 4 positivos de robustez no parecerían azar); con la simulada, P(X ≥ 4 | Bin(48, 0.082)) = 0.57. Cambios: §4 reescrito (nominal 0.025·N "y otros tantos por debajo", cobertura simulada, "indicative figures, since fold dependence raises them and cells with a true difference do not contribute"); resumen, §5.2, veredicto y tabla de afirmaciones usan los esperados unilaterales con cobertura simulada ("up to about 4.0" en robustez, porque con 12/48 intervalos por debajo de 0 no todas las celdas son nulas). Nota: el "≈ 1.2" de la condición principal coincide numéricamente con la cifra anterior (0.05·24), pero ahora es la esperanza unilateral con cobertura ≈ 90 %; el "≈ 2.4" de robustez pasa a ≈ 4.0. La conclusión cualitativa (hipótesis, no resultado) se mantiene y queda mejor apoyada.

### M5. Preregistro no verificable desde el repositorio — **ACEPTADO CON MATIZ**

Verificado en el registro de la sesión del agente autor (`…/subagents/agent-a3bfa343c2e12f272.jsonl`): `Write PREREGISTRO_SVMF001.md` a las 04:00:02.138Z, primera edición de `GRID` en `run_comparison.py` a las 04:01:46Z, corrida 04:04:40–04:08:33Z, anotaciones 04:17:58Z. `head -n 40 PREREGISTRO_SVMF001.md | sha256sum` da `c89b2c76fa744f1c8c1864818ee2dd43a2e7f43a78aee6960000aed842d132be`, igual al del árbitro. Matiz: el árbitro propone escribir la hora y el hash *en la cabecera*; eso cambiaría las líneas 1–40 y con ellas el propio hash. Se añaden por tanto al final, como anotación fechada (la regla del archivo dice que toda corrección posterior se anota al final), con la orden para verificarlo; las líneas 1–40 quedan byte a byte como se escribieron a las 04:00:02. En `main.tex` §4: "written down in PREREGISTRO_SVMF001.md at 04:00 UTC on 3 October 2026, before the code change (04:01) and the re-run (04:04–04:08 UTC). That file was first committed together with the results and its file date is later than the run …, so its timing rests on the session log of the drafting agent; the file records the SHA-256 digest of its pre-run part". Limitaciones: idem. En adelante: commit propio del preregistro antes de tocar el código (anotado como regla para la próxima corrida; en esta sesión no se usa git por instrucción del coordinador).

### M6. Explicación de la celda positiva del gaussiano — **ACEPTADO**

Recontado desde `results.json` (aciertos sobre 80 por pliegue): la celda +0.37 pp son **3 aciertos de 800**: pliegues 3 y 4 (VB con β = ½ acierta uno más que su miembro RBF) y pliegue 5 (la CV eligió la lineal, 75, frente a 76 de RBF y VB). De los 8 pliegues en que se eligió la RBF, la lineal fue mejor en 2, igual en 5 y peor en 1; la referencia seleccionada queda por debajo de la media de la lineal por el pliegue 0 (RBF elegida, 5 aciertos menos; los demás se compensan, +1 y −1) y por debajo de la RBF por los pliegues 5 y 6 (lineal elegida, un acierto menos en cada uno). La frase de v0.1 ("picked the RBF-SVM … although the linear SVM was better on the test folds") se arrastró sin recomprobar. Reescrita en §5.1 con macros generadas por `make_numbers.py` (`\GaussCellPts`, `\GaussCellN`, `\GaussVbOwnFolds`, `\GaussSelLinVbGainFolds`, `\GaussPickRbfN`, `\GaussPickRbfLinBetter`, `\GaussPickRbfTie`, `\GaussPickRbfLinWorse`, `\GaussPickRbfLossMax`, `\GaussSelLinLossFolds`), con `assert` que comprueban las palabras "by one point", "one point each" y "the other differences cancel". README corregido. La conclusión (sin valor añadido) no cambia.

### M7. Extensión — **ACEPTADO CON MATIZ**

De 14 a **12 páginas** (cuerpo pp. 1–11, apéndices A–B pp. 11–12, bibliografía p. 12) sin quitar ninguna demostración ni ningún número verificable del texto. Detalle y razón de no bajar a 11 en la sección "Extensión".

## Hallazgos menores

| id | decisión | acción |
|---|---|---|
| m1 | aceptado | Obs. 2.3: "for VB-RBF-SVM the member is the RBF-SVM over the same grid as the reference; for cell-SVM and LLSVM it is a linear SVM tuned over a sub-grid of the reference's C values (C ≥ 0.1 and C ≥ 0.01 against C ≥ 0.001; LLSVM with a regularised constant feature); for kNN-SVM … C = 1 fixed" (valores por macro). Pie de la tabla anidada (ahora Tabla 4): "Only the VB-RBF-SVM column is exactly nested … those three columns approximate the nested comparison". |
| m2 | aceptado | Obs. 2.3: "In population risk a local family can … rise above it only through genuine adaptation; observed test-fold differences also carry test-sample noise in both directions." |
| m3 | aceptado | Comprobado: el extremo superior en coma flotante es −7.94·10⁻⁵ (−0.008 pp), igual al −1/12600 exacto del árbitro, residuo de pliegues de prueba de 36 y 35 puntos. Pie de la Tabla 2: "The upper end of the wine/cell-SVM interval is −0.008 points, a residue of unequal test-fold sizes: by the letter it excludes zero" (macro `\DiffHiExactMainWineCell`). Se sigue contando como negativa (es la letra del criterio y la tolerancia 10⁻⁹ no la toca); no afecta al veredicto. |
| m4 | aceptado | §5.2: "Of the positives, 3 persist against both the fixed RBF-SVM and the post-hoc oracle reference …, all on the two-scale moons: VB-RBF-SVM under noise and under subsampling, and cell-SVM under subsampling, with 80 training points (+5.00 [+2.25, +8.00]; +4.75 [+2.00, +7.25] against the oracle); the cell of LLSVM on digits (parity) under noise does not" (macros `\NPosRobustPersist`, `\PosRobustNotPersist`). Tabla de afirmaciones y CONTINUIDAD corregidas ("2 de VB-RBF-SVM que sobreviven al oráculo" → 3). |
| m5 | aceptado con matiz | Apéndice B (D1): "about twice the 0.0503 of k = n; in excess risk, which the middle panel of Figure 1 plots, 0.0570 against 0.0003, more than a hundred times larger" (macros `\ExKnnCWorstExc`, `\ExKnnCGlobalExc`). Matiz: no escribo "≈ 190 veces" porque el exceso global estimado en D1 (0.00029) es del orden de su propio error Monte Carlo (0.00026); el cociente puntual (196) no es fiable, el orden de magnitud sí. El párrafo de §3 que repetía la cifra se redujo a una frase que remite al apéndice. |
| m6 | aceptado | Prueba de la Prop. 3.2 condicionada en $\tilde S=(X_i,Y_i,Z_i)_{i\le n}$. |
| m7 | aceptado | "data-set/edge cells" en §5.1. |
| m8 | aceptado | Leyenda de la Fig. 2 fuera de los ejes (`fig.legend(..., loc="upper center", ncol=4)`, `tight_layout(rect=(0, 0, 1, 0.92))`); figura redibujada con la opción nueva `run_comparison.py --figure-only`, que solo lee `results.json` (sin reajustar ni reescribir resultados). Comprobado visualmente: ya no tapa ningún intervalo. |
| m9 | aceptado | Resumen: "kNN-SVM is below the reference on 3 and 3 of 6 data sets". |
| m10 | aceptado | Anotación del preregistro (punto 4): la tolerancia favorece a la familia (quita una celda negativa y sus dos homólogas post hoc), no toca la condición principal ni ninguna positiva; recálculo exacto del árbitro 288/288. |

## Verificación de la ronda 1 (puntos a medias o con error nuevo)

| id ronda 1 | estado según el árbitro | corrección en v0.3 |
|---|---|---|
| B1 saturación | a medias | Regla preregistrada aplicada también al empate VB/RBF (M1) y a las rejillas de C no ampliadas (M2); anotación correctora en el preregistro. |
| B2 robustez (arrastre de "≈ 2.4") | bien, con imprecisión | Cifra sustituida por la esperanza unilateral con cobertura simulada (≈ 4.0) en README, ficha y nota (M4). |
| M1 Prop. 3.2 | error nuevo | Paréntesis con n ≥ 2 (M3) y condicionamiento en $\tilde S$ (m6). |
| M2 multiplicidad | a medias | Recuentos unilaterales y cobertura del bootstrap (M4). |
| M3 anidamiento | bien, con imprecisión | Sub-rejillas de C de cell-SVM y LLSVM declaradas; pie de la tabla anidada (m1, m2). |
| M4 extensión | no aplicado | 14 → 12 páginas (M7). |
| M5 preregistro | a medias | Hora, SHA-256 y forma de verificarlo en el preregistro; manuscrito dice en qué descansa la fecha (M5). |
| m12 figuras | a medias | Leyenda de la Fig. 2 fuera de los ejes (m8); Fig. 3 fuera del PDF (M7). |

## Lista final de acciones del árbitro

| acción | estado |
|---|---|
| 1 (empate VB/RBF grid-limited) | hecho: M1 |
| 2 (frase condicionada; mecanismo de varianza; rejillas de C) | hecho: M2 |
| 3 (paréntesis n ≥ 2; condicionar en (X_i, Y_i, Z_i)) | hecho: M3, m6 |
| 4 (esperanzas unilaterales y cobertura real) | hecho: M4 |
| 5 (hora, SHA-256 y nota en el preregistro; texto del manuscrito) | hecho con matiz (al final del archivo, no en la cabecera): M5 |
| 6 (celda gaussiana) | hecho: M6 |
| 7 (≤ 11 páginas) | parcialmente: 12 páginas (M7, sección "Extensión") |
| 8 (Obs. 2.3 y pie de la tabla anidada; "in population risk") | hecho: m1, m2 |
| 9 (3 de 4 positivos persisten; CONTINUIDAD:68) | hecho: m4 |
| 10 (wine −0.008 pp; riesgo/exceso; data-set/edge; leyenda; kNN-SVM en el resumen; tolerancia) | hecho: m3, m5, m7, m8, m9, m10 |
| 11 (DOI de zhang2004 y stone1977; páginas de cheng2007) | hecho: DOI añadidos; páginas de cheng2007 retiradas por no confirmadas |
| 12 (próxima corrida con rejillas ampliadas y criterio de robustez, preregistro con commit propio) | diferido, como pide el árbitro: siguiente paso (b) del manuscrito, anotación 3 del preregistro y nota de continuidad |

## Bibliografía

| entrada | acción |
|---|---|
| zhang2004 | `doi = {10.1214/aos/1079120130}` añadido; la nota "pp. 86–134" de la discusión (no verificada por ningún árbitro) se sustituye por "Followed by a discussion". |
| stone1977 | `doi = {10.1214/aos/1176343886}` añadido; nota "Discussion: pp. 621–645" (el árbitro confirma que la discusión llega a 645). |
| cheng2007 | Una búsqueda web propia (03/10/2026) solo confirma de nuevo la existencia (SDM 2007; PDF del autor en cse.msu.edu, Semantic Scholar), no las páginas. Se **quita** `pages = {461--466}` (opción ofrecida por el árbitro) para no imprimir un dato no verificado; queda anotado en la nota de continuidad. La entrada se mantiene porque se cita con razón (SVM localizada por vecinos y por perfiles/clusters). |
| resto | Sin cambios; ladicky2011, zhang2006, viering2023, micchelli2006 verificadas por el árbitro; las demás siguen marcadas como no verificables por la red del entorno en la nota de continuidad. |

## Extensión

14 páginas (v0.2) → **12 páginas** (v0.3). Recortes aplicados (numeración del árbitro en M7):
1. Resumen de ≈ 330 a ≈ 210 palabras, sin las cifras de v0.1 ni el detalle de robustez.
2. Tabla 1 (sumas exactas) eliminada: los cocientes siguen en el Cor. 3.5 y la tabla completa en `results/exact_example.md`.
3. Tabla de afirmaciones de 9 a 8 filas, más compactas (no se redujo a 5 porque el brief exige la tabla de afirmaciones con estado, y las filas de teoría y simulación son las que fijan los estados "proved"/"verified").
4. Fig. 3 (regiones de decisión) fuera del PDF (sigue en `figures/fig_regions.pdf`, citada en el apéndice A); apéndice C suprimido y la tabla anidada movida a §5.1, donde se usa; apéndice A reducido a un párrafo.
5. Obs. 3.6 (lectura de primer orden) integrada en una frase del Cor. 3.5; Obs. 3.3(i) en una frase; el párrafo de §3 sobre simulaciones reducido a una frase (las cifras quedan en el apéndice B).
6. §5.2 (robustez) reducido a la mitad.
7. Limitaciones y siguientes pasos condensados (no fusionados con el veredicto, que conserva la discusión del defecto del criterio).
8. Bibliografía a dos columnas con `\bibsep` compacto; espaciado de flotantes algo más ajustado (`\textfloatsep`, `\floatsep`, `skip` de los pies).

Por qué no 11: con el cuerpo en pp. 1–11, bajar otra página obligaría a sacar del PDF el apéndice B (cifras D1–D4 en que se apoya la fila "verified, not proved" de la tabla de afirmaciones), la tabla de conjuntos de datos o la tabla de saturación (base de los "grid-limited"). Ninguna demostración se ha quitado. Se declara: 12 páginas, por encima del objetivo de ≤ 10 del brief y dentro del ≤ 12 pedido por el coordinador.

## Cómputo usado

Sin corrida nueva de la comparación. `coverage.py` del árbitro (verificación) ≈ 7 s; `experiments/bootstrap_coverage.py` 3 s (4000 réplicas, prueba) + 11 s (20 000 réplicas, definitiva); scripts de verificación de recuentos en el scratchpad ≈ 2 s; `run_comparison.py --figure-only` 2.4 s; `make_numbers.py` ≈ 10 × 1 s. Total de cómputo de experimentos ≈ 0.6 min de CPU; compilaciones LaTeX ≈ 1 min adicional. Sin git; ninguna otra carpeta de `papers/` tocada; no existe subcarpeta `theory/` en esta línea.

## Qué cambió en los números

Ningún número de la corrida de referencia (exactitudes, diferencias, intervalos, recuentos de significación, veredicto del criterio, saturación) cambia. Cambian solo cifras de comparación o de lectura:
- "Esperados por azar": principal 1.2 (bilateral, 0.05·24) → 1.2 (unilateral con cobertura simulada; 0.6 nominal); robustez 2.4 (bilateral) → **4.0** (unilateral con cobertura simulada; 1.2 nominal). Nuevas: cobertura 89.9 % (10 pliegues) y 83.5 % (5 pliegues).
- Celda gaussiana: explicación nueva en aciertos (3 de 800; 2 + 1; 8 elecciones de RBF con la lineal mejor en 2, igual en 5, peor en 1).
- Positivos de robustez que persisten frente al oráculo y a la RBF fija: 3 (antes el texto decía 2, solo VB).
- Recuentos nuevos de saturación usados en el texto (6/10, 4/10, 5/10, 18/20, 11/20, 17/20).
- Exceso de riesgo en D1: 0.0570 frente a 0.0003 (antes solo el riesgo, 0.1070 frente a 0.0503).

## Qué queda abierto

1. **Comparaciones limitadas por la rejilla** (empate VB/RBF en multiescala; déficit de las familias lineales locales): requieren una corrida nueva con γ por encima de 100·γ_med (RBF y VB-RBF), C ∈ {…, 100, 1000} para cell-SVM y LLSVM, n mayor, criterio reparado (≥ 2 conjuntos por régimen) y criterio predefinido de robustez, todo en un preregistro con commit propio antes de tocar el código.
2. Los 4 positivos de robustez son hipótesis (compatibles con azar con la cobertura real del bootstrap).
3. La inferencia entre pliegues sigue siendo descriptiva: el bootstrap percentil infracubre (≈ 90 % / 83 % con pliegues independientes, menos con dependencia); una versión futura podría usar la corrección de Nadeau–Bengio o más pliegues.
4. Extensión: 12 páginas frente al objetivo de ≤ 10.
5. Predefinición de v0.1 no verificable; la de v0.2 descansa en el registro de sesión (documentada, con hash de la parte pre-corrida).
6. Páginas de cheng2007 por confirmar (retiradas de `refs.bib` mientras tanto).
