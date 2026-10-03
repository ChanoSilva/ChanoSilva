# SVMF001 — Preregistro de la corrida ampliada (ronda 1 de revisión interna)

**Fecha y hora de escritura:** 03/10/2026, antes de ejecutar ningún pliegue de la corrida ampliada. Este archivo responde al hallazgo M5 del informe de arbitraje (ausencia de un registro fechado del criterio y las rejillas) y al B1 (saturación de rejillas). Se escribe **antes** de modificar `experiments/run_comparison.py` y antes de correr; después de la corrida no se modifica (cualquier corrección posterior se anota al final, fechada, sin borrar lo anterior).

## Cronología declarada de la corrida original (30/09/2026)

- El criterio de valor añadido, los regímenes, las familias, la semilla (20260930) y las rejillas se fijaron en el código antes de la primera corrida completa; la rejilla de C de la RBF se redujo de {0.1, 1, 10, 100} a {0.1, 1, 10} por presupuesto de cómputo **antes** de ejecutar ningún pliegue externo completo, según la nota de la sesión original. Para esa corrida **no existe** un registro fechado independiente del código: la afirmación "fijado antes de correr" descansa en la palabra del redactor, y así se declara ahora en el manuscrito y en la nota de continuidad.
- La única adición posterior a ver resultados fue el chequeo oráculo (`posthoc_oracle.py`), etiquetado como post hoc en código, nota y manuscrito.

## Qué NO cambia respecto a la corrida original

- Criterio predefinido de valor añadido: (A) mejora pareada media > 0 con IC bootstrap percentil 95 % (B = 2000, sobre los pliegues externos) que excluya 0 en la mayoría de los 6 conjuntos de la condición principal; o (B) un régimen nombrado en cuyos conjuntos se cumpla (A) sin que ningún conjunto fuera del régimen tenga IC enteramente por debajo de 0. Convención: un IC con extremo exactamente 0 cuenta como que incluye 0 (regla `lo > 0` / `hi < 0` estrictas).
- Regímenes: real (wine, breast cancer, digits par/impar), lineal (gaussiano d = 10), multiescala (lunas y tablero a dos escalas). Se reconoce (ya desde v0.1) que la cláusula (B) con un régimen de un solo conjunto es un defecto de diseño; **no se repara** a posteriori: se aplica la misma letra y se discute.
- Conjuntos, submuestreos (300 / 400 / 400), PCA(16) en digits, semilla maestra 20260930, condiciones (principal 2×5 pliegues; noise20 y sub25 con 5 pliegues; cada etiqueta de entrenamiento invertida independientemente con probabilidad 0.2; 25 % del pliegue de entrenamiento con mínimo 40 puntos), CV interna estratificada de 3 pliegues con exactitud, desempates hacia el miembro global (y referencia: RBF solo si su puntuación interna es estrictamente mayor que la de la lineal), C = 1 fijo en la kNN-SVM, validación interna de la kNN-SVM submuestreada a 40 puntos, β ∈ {0, 0.5, 1}, κ = 10, C de cell-SVM ∈ {0.1, 1, 10}, C de LLSVM ∈ {0.01, 0.1, 1, 10}.

## Qué cambia: rejillas ampliadas por los extremos donde el árbitro documentó saturación

| hiperparámetro | rejilla v0.1 | rejilla ampliada | motivo (recuento del árbitro, condición principal) |
|---|---|---|---|
| γ_mult (RBF y VB-RBF) | {0.1, 0.3, 1, 3, 10} | {0.1, 0.3, 1, 3, 10, 30, 100} | 10 (borde superior) en 20/20 pliegues multiescala |
| C (RBF y VB-RBF) | {0.1, 1, 10} | {0.1, 1, 10, 100, 1000} | 10 (borde superior) en 20/20 pliegues multiescala |
| C (SVM lineal) | {0.01, 0.1, 1, 10} | {0.001, 0.01, 0.1, 1, 10} | 0.01 (borde inferior) en 8/10 pliegues del gaussiano |
| M (cell-SVM y LLSVM) | {1, 2, 4, 8} | {1, 2, 4, 8, 16, 32} | 8 (borde superior) en 14–16/20 multiescala y 10/10 digits |
| k (kNN-SVM) | {20, 50, 100, todos} | {5, 10, 20, 50, 100, todos} | 20 (borde inferior) en 15/20 multiescala |

Guardia técnica (no cambia ningún resultado donde no se activa): un valor de M mayor que el número de puntos del pliegue de entrenamiento interno se omite de la rejilla en ese pliegue (k-means no puede formar más celdas que puntos); solo puede ocurrir en sub25 con 40 puntos de entrenamiento (≈ 27 por pliegue interno), para M = 32.

## Qué se añade al resumen de resultados

- Para cada método e hiperparámetro, la fracción de pliegues externos en que la CV interna seleccionó el extremo inferior o superior de su rejilla ("saturación"). Se reporta en una tabla del apéndice y se declara en el texto si persiste la saturación en algún borde tras la ampliación.
- La comparación anidada de cada familia frente a su propio miembro global fijo (ya calculada en `posthoc_oracle.json`) pasa a reportarse.

## Qué se hará con los resultados, decidido ahora

- Si las magnitudes o los signos de las conclusiones de v0.1 cambian (p. ej. la celda positiva del gaussiano, el empate VB/RBF en multiescala, las pérdidas de −10 a −18 pp de las familias lineales locales), el texto, el resumen, la tabla de afirmaciones, el README y la ficha cambian para describir lo observado; no se vuelve a la corrida de v0.1 ni se eligen rejillas a posteriori.
- Si persiste saturación en algún extremo, se declara y la afirmación afectada se marca como "medida, limitada por la rejilla".
- Los cambios de código (rejillas, estadístico de saturación, nombres de figuras, guardia de M) se hacen en un solo paso antes de correr; la corrida es una sola, completa, con la semilla 20260930.

## Anotaciones posteriores a la corrida (fechadas; no se borra nada de lo anterior)

- **03/10/2026 04:04–04:08 UTC.** Corrida única completa ejecutada tal como se preregistró (230.7 s de pared, salida 0). Resultados en `results/results.json`; los de v0.1 en `results/v01/`.
- **03/10/2026 04:16 UTC — tolerancia numérica en la clasificación de intervalos.** Al revisar los resultados se vio que una celda (cell-SVM, tablero, noise20) tenía IC [−0.075, −2.2·10⁻¹⁷] y quedaba clasificada "neg" por residuo de coma flotante, en contra de la convención declarada arriba (extremo exactamente 0 cuenta como que incluye 0). Se añadió a `run_comparison.py` la función `sig_of` con tolerancia 10⁻⁹ (y la misma regla en `posthoc_oracle.py`) y un modo `--resummarise` que rehace los resúmenes desde los pliegues guardados con las mismas semillas: ningún modelo se reajusta, ningún IC ni exactitud cambia; el único cambio de etiqueta es esa celda (y sus dos homólogas del post hoc), que pasan a "none". Esto es una corrección de implementación de la convención ya fijada, no un cambio de criterio; se anota aquí porque se decidió después de ver los resultados.
- **03/10/2026.** Saturación residual en la condición principal: kNN-SVM k = 5 en 8–10/10 pliegues de digits, lunas y tablero; LLSVM M = 32 en 7–10/10 de los mismos; cell-SVM M = 32 en 4–7/10; C = 10 de cell-SVM/LLSVM en 9–10/10 de lunas, tablero (y digits para LLSVM); RBF C = 1000 en 5/10 del tablero; γ ya no satura por arriba en ningún conjunto. Conforme a lo decidido arriba, las afirmaciones afectadas (déficit de las familias lineales locales en multiescala) se marcan "medidas, limitadas por la rejilla" y **no** se vuelve a ampliar la rejilla en esta ronda (una sola corrida comprometida; presupuesto; por debajo de k = 5 o por encima de M = 32 las SVM lineales locales degeneran en reglas de vecinos/centroides).
