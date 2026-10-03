# SVMF001 — Respuesta del autor a la ronda 2 de revisión interna (informe del 03/10/2026)

Respuesta redactada el 03/10/2026 en una sesión de Claude Code (session_01MTmjU2K8b4sgpjjL3JTtDz), en el papel de autor. Informe atendido: `REFEREE_SVMF001_ronda2_20261003.md` (veredicto: cambios mayores, solo de texto; 0 bloqueantes, 7 mayores, 10 menores; reproducción bit a bit; ningún hallazgo cambia el veredicto del criterio).

*Documento escrito de forma incremental; las secciones se completan a medida que se aplican los cambios.*

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

### M7. Extensión — **ACEPTADO CON MATIZ** (véase la sección "Extensión")

(en curso)

## Hallazgos menores

(en curso)

## Verificación de la ronda 1 (puntos a medias o con error nuevo)

(en curso)

## Bibliografía

(en curso)

## Extensión

(en curso)

## Cómputo usado

(en curso)

## Qué queda abierto

(en curso)
