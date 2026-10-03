# SVMF001 — Respuesta del autor a la ronda 1 de revisión interna (informe del 30/09/2026)

Respuesta redactada el 03/10/2026 en una sesión de Claude Code (session_01MTmjU2K8b4sgpjjL3JTtDz), en el papel de autor. Informe atendido: `REFEREE_SVMF001_ronda1_20260930.md` (veredicto: cambios mayores; 2 bloqueantes, 5 mayores, 14 menores, bibliografía, recortes). Este archivo se escribe de forma incremental: cada hallazgo lleva su estado (**hecho** / **en curso** / **pendiente**) y el estado es exacto en el momento de la última escritura.

Resumen de decisiones (se actualiza al final): véase la sección "Recuento".

---

## Hallazgos bloqueantes

### B1. Saturación sistemática de las rejillas — **ACEPTADO (opción 1: ampliar rejillas y volver a correr)** — estado: en curso

Decisión. Se acepta el hallazgo íntegramente: el recuento del árbitro sobre `results/results.json` es correcto (RBF γ_mult = 10 y C = 10 en 20/20 pliegues multiescala; cell/LLSVM M = 8 en 14–16/20; kNN k = 20 en 15/20; digits M = 8 en 10/10; gaussiano lineal C = 0.01 en 8/10). Las magnitudes del resultado negativo eran comparaciones entre métodos truncados por la rejilla y el manuscrito no lo decía. Se elige la opción (1) del árbitro: ampliar las rejillas por los extremos donde se documenta saturación y volver a correr la comparación completa.

Qué se cambió.
- `PREREGISTRO_SVMF001.md` (nuevo, fechado 03/10/2026, escrito **antes** de la corrida): criterio, regímenes, semilla y rejillas ampliadas: γ_mult ∈ {0.1, 0.3, 1, 3, 10, 30, 100}; C_RBF ∈ {0.1, 1, 10, 100, 1000}; M ∈ {1, 2, 4, 8, 16, 32} para cell-SVM y LLSVM; k ∈ {5, 10, 20, 50, 100, todos}; C_lineal ∈ {0.001, 0.01, 0.1, 1, 10} (extremo inferior, por el 8/10 en el gaussiano). Las demás rejillas (β, κ, C de cell/LLSVM, pliegues internos) no cambian.
- `experiments/run_comparison.py`: rejillas ampliadas; `summarise` calcula además, por método e hiperparámetro, la fracción de pliegues externos con selección en el extremo inferior/superior de la rejilla (`edge`); guardia para M > número de puntos del pliegue interno (solo puede ocurrir en sub25 con 40 puntos); nombres legibles en la figura (m12).
- `experiments/make_numbers.py`: tabla de saturación (apéndice) y macros de recuento de bordes.
- Corrida completa (semilla 20260930, BLAS a un hilo): 03/10/2026 04:04–04:08 UTC, 230.7 s de pared (229 s de CPU; v0.1: 206 s), salida 0 (`results/run_log.txt`). Los resultados v0.1 se conservan en `results/v01/` para cotejo. No se volvió a correr `exact_example.py` (ningún hallazgo toca sus números; el árbitro lo reprodujo cifra por cifra); solo se redibujó su figura desde el JSON (`--figure-only`).
- Tolerancia numérica (anotación fechada en `PREREGISTRO_SVMF001.md`): una celda (cell-SVM, tablero, noise20) tenía IC [−0.075, −2.2·10⁻¹⁷] y quedaba clasificada "neg" por residuo de coma flotante, contra la convención declarada (m13: extremo exactamente 0 cuenta como que incluye 0). Se añadió `sig_of` con tolerancia 10⁻⁹ y un modo `--resummarise` que rehace resúmenes, criterio y bloque de robustez desde los pliegues guardados con las mismas semillas (IC idénticos, ninguna exactitud cambia). Único cambio de clasificación: esa celda pasa a "none" (y las dos homólogas del post hoc). Queda registrado en `results.json` (`meta.resummarised`).

**Qué cambió en los números (v0.1 → v0.2, condición principal).** El árbitro tenía razón en el fondo: buena parte de las magnitudes era efecto de la rejilla.
- Familias lineales locales en multiescala: lunas kNN-SVM −10.63 → **−0.37 [−1.63, +1.00]** (deja de ser significativa), cell-SVM −11.38 → −3.75 [−5.88, −1.25], LLSVM −12.00 → −7.38 [−9.13, −5.75]; tablero kNN-SVM −13.12 → −3.50 [−6.38, −0.50], cell-SVM −18.25 → −7.63 [−11.38, −3.25], LLSVM −17.75 → −4.88 [−7.63, −1.87]. La exactitud de kNN-SVM sube de 86.9 a 96.6 % (lunas) y de 73.9 a 85.9 % (tablero); la RBF pasa de 97.5 a 97.0 y de 87.0 a 89.4. En digits: kNN −0.87 → +0.75 (n.s.), cell −3.37 → −2.00, LLSVM −4.12 → −1.13 (ambas aún significativas).
- Recuento: 8 negativas / 1 positiva / 15 nulas → **9 negativas / 1 positiva / 14 nulas** (nuevas negativas: cell-SVM en wine −1.42 [−2.83, −0.01] y kNN-SVM en el gaussiano −2.62 [−3.88, −1.62]; deja de serlo kNN-SVM en lunas).
- Empate VB-RBF/RBF en multiescala: se mantiene (lunas +0.12 [−1.25, +1.37]; tablero +0.50 [−0.50, +2.12]). La celda positiva del gaussiano se mantiene pero se encoge: +0.75 [+0.12, +1.50] → **+0.37 [+0.12, +0.75]**; frente a su propio miembro global fijo (RBF) es +0.12 [−0.25, +0.50] y frente al oráculo −0.62 (IC incluye 0): la explicación por ruido de selección se confirma. El veredicto del criterio no cambia (nadie cumple (A); VB-RBF cumple (B) por la letra en el régimen "lineal" de un solo conjunto).
- Robustez: **4 de 48 intervalos quedan por encima de 0** (v0.1: 0; ≈ 2.4 esperados por azar al 95 %): VB-RBF-SVM en lunas con ruido +2.25 [+0.50, +4.00] y con submuestreo +5.50 [+2.25, +9.00] (también frente al oráculo y frente a la RBF fija), cell-SVM en lunas submuestreadas +5.00 [+2.25, +8.00], LLSVM en digits con ruido +2.00 [+0.75, +3.50] (frente al oráculo +0.75 [−2.50, +3.26], n.s.). kNN-SVM por debajo en 3/6 (ruido) y 3/6 (submuestreo) (v0.1: 4/6 y 3/6); VB-RBF por debajo en 1/6 con ruido (v0.1: 2/6) y 0/6 con submuestreo. Caídas medias de la referencia: 7.1 / 6.4 pp (v0.1: 6.0 / 6.2).
- Saturación residual (condición principal, pliegues de 10): kNN-SVM k = 5 (extremo inferior) en 8/10 digits, 10/10 lunas, 10/10 tablero; LLSVM M = 32 en 7/10, 9/10, 10/10; cell-SVM M = 32 en 6/10, 4/10, 7/10; C = 10 (superior) de cell-SVM en 10/10 lunas y tablero y de LLSVM en 10/10 digits, 9/10 lunas, 10/10 tablero; RBF C = 1000 en 5/10 tablero; γ = 0.1·γ_med (inferior) de la RBF en 8/10 del gaussiano (esperable: la regla de Bayes es lineal); SVM lineal C = 0.001 en 7/10 tablero (irrelevante: 50 % de exactitud). **Ya no hay saturación de γ en el extremo superior** (0/10 en los seis conjuntos), que era la que infra-ajustaba a la referencia RBF.

**Qué conclusiones cambian y cómo se redactan ahora.** (1) "Las familias lineales locales pierden entre 10 y 18 pp en multiescala" → "quedan por debajo de la referencia en 5 de 6 celdas multiescala, entre 3.5 y 7.6 pp (kNN-SVM empata en las lunas), con la CV interna todavía en el extremo local de las rejillas (k = 5, M = 32, C = 10)": estado **medido, limitado por la rejilla**, así en texto, tabla de afirmaciones, README y ficha. (2) "Ninguna familia queda significativamente por encima de la referencia bajo ruido o submuestreo" → se retira; ahora se reportan los 4 intervalos positivos de 48 (3 en las lunas a dos escalas), se dice que ≈ 2.4 se esperan por azar, que la robustez no tenía criterio predefinido y que son hipótesis para una corrida mayor, no resultado. (3) El empate VB/RBF en multiescala y la explicación de la celda positiva se mantienen y se refuerzan con la comparación anidada. (4) La frase de v0.1 "piecewise-linear boundaries built from local linear SVMs do not reach the RBF-SVM" se reescribe: con las rejillas de v0.1 el déficit era en gran parte de la rejilla.

**Por qué no se amplía otra vez la rejilla en esta ronda.** El preregistro comprometía una sola corrida; el presupuesto de CPU de la ronda (≤ 10 min) está en ≈ 4.5 min usados; y por debajo de k = 5 o por encima de M = 32 con 320 puntos de entrenamiento las SVM lineales locales degeneran en votos de vecinos o reglas de centroide (otra familia). Se declara como limitación y como siguiente paso.

### B2. Sobreafirmación de robustez en los textos públicos — **ACEPTADO** — estado: pendiente

Decisión. Se acepta. "Ninguna familia es más robusta" afirma lo que el cuerpo no mide; con 5 pliegues e IC de ±5 pp, la ausencia de evidencia no es evidencia de ausencia. Se sustituye por el texto propuesto por el árbitro (ES y EN) en `FICHA_SVMF001_propuesta.md` y en `README.md`, con los recuentos 4/6 y 3/6 tomados de la nueva corrida (si cambian, cambia el texto), y se añade "post hoc" donde la ficha dice "desaparece frente a la mejor de las dos referencias".

---

## Hallazgos mayores

### M1. Prop. 3.2 (caso estricto) y Cor. 3.5 — **ACEPTADO** — estado: pendiente

Decisión. El árbitro tiene razón: R_nc(0) = R_nc(1) = 1/2, luego R_nc no es estrictamente decreciente en n ≥ 0 y el Cor. 3.5 no podía invocar la Prop. 3.2 tal como estaba; el contraejemplo n = 1, M = 2 (E R = 1/2 = R_nc(1)) es correcto. Se reenuncia el caso estricto como "R_A no creciente y R_A(n−1) > R_A(n) (en particular, estrictamente decreciente en {1,…,n}) y M ≥ 2", con la prueba cerrada vía P(N_j = n−1) = n p_j^{n−1}(1−p_j) > 0, y se añade "n ≥ 2" al Cor. 3.5. Ningún número cambia (n = 320).

### M2. Multiplicidad no discutida — **ACEPTADO** — estado: pendiente

Se añaden las frases propuestas (≈ 1.2 intervalos espurios esperados entre 24 al 95 %; la cláusula de mayoría absorbe esto, la cláusula de régimen de un solo conjunto no) en el protocolo y en la discusión de la celda positiva (si tras la nueva corrida sigue existiendo; si no, la frase se adapta a lo observado).

### M3. Nesting y referencia — **ACEPTADO** — estado: pendiente

Se reescribe la observación de anidamiento (puede superar a la referencia *seleccionada* también por ruido de selección), se declara que el miembro global de la kNN-SVM es la SVM lineal con C = 1 fijo (no la referencia lineal ajustada), y se añade la comparación anidada "frente a su propio miembro global fijo" tomada de `posthoc_oracle.json` (VB vs RBF; cell/LLSVM vs lineal; kNN vs lineal ajustada, con la salvedad del C fijo) en la tabla post hoc del apéndice.

### M4. Extensión y legibilidad — **ACEPTADO** — estado: pendiente

Se aplican los recortes 1–8 del árbitro (tablas D1–D4, post hoc, fracciones locales y robustez por conjunto al apéndice; se elimina la mitad derecha de la Tabla 1; figura de regiones al apéndice; Sección 6 reducida a las filas no redundantes; fusión de párrafos; fusión de las tablas de exactitud y diferencias; `\resizebox` eliminados). Objetivo ≤ 10 páginas. [pendiente: páginas antes/después]

### M5. "Predefinido" sin registro verificable — **ACEPTADO CON MATIZ** — estado: en curso

Se acepta la acción (archivo `PREREGISTRO_SVMF001.md` fechado antes de la corrida ampliada; cronología declarada en la nota de continuidad). Matiz honesto: para la corrida original (30/09) no existe un registro fechado independiente, y así se dice ahora en el manuscrito ("fixed before the run, but not in a dated, independently verifiable record") y en la nota; la reducción de la rejilla de C de la RBF a {0.1, 1, 10} se hizo por presupuesto de cómputo antes de ejecutar ningún pliegue externo completo, según la nota de la sesión original, pero esa afirmación sigue descansando en la palabra del redactor y se declara como tal. Para la corrida ampliada de hoy sí hay registro previo.

---

## Hallazgos menores

| id | decisión | acción | estado |
|---|---|---|---|
| m1 | aceptado | README/CONTINUIDAD/docstring de `exact_example.py`: Lema 2.2 y Prop. 3.2 (la numeración del PDF) | pendiente |
| m2 | aceptado | declarar el desempate de la referencia hacia la lineal (RBF solo si su puntuación interna es estrictamente mayor) | pendiente |
| m3 | aceptado | "each training label is flipped independently with probability 0.2" | pendiente |
| m4 | aceptado | pie de la tabla de caídas: las condiciones usan particiones distintas de la principal | pendiente |
| m5 | aceptado | frase en el apéndice sobre la discontinuidad de a(·) en los puntos de entrenamiento | pendiente |
| m6 | aceptado | cita de "universal kernel": `micchelli2006` y `steinwart2008` (§4.6); `steinwart2007` se retira del texto y de refs.bib (ya no se cita) | pendiente |
| m7 | aceptado | reformular la frase sobre la selección del ancho variable bajo ruido según los nuevos números | pendiente |
| m8 | aceptado | "three real data sets and three synthetic ones in two regimes" | pendiente |
| m9 | aceptado | "LLSVM-style" en el texto | pendiente |
| m10 | aceptado | pie de la tabla D1–D4: estimadores distintos para "global" y kNN en D2 | pendiente |
| m11 | aceptado | "positive semidefinite Gram matrices (a kernel in the sense of Aronszajn)" | pendiente |
| m12 | aceptado | nombres legibles en ejes/leyendas de las tres figuras; leyenda de la Fig. 1 movida | pendiente |
| m13 | aceptado | declarar la convención "an interval whose endpoint is exactly zero counts as including zero" | pendiente |
| m14 | aceptado | se conserva `main.bbl` y se quita de `.gitignore` | pendiente |

## Bibliografía

| entrada | acción | estado |
|---|---|---|
| ladicky2011 | `pages = {985--992}`, `publisher = {Omnipress}` | pendiente |
| zhang2006 | `volume = {2}`, `doi = {10.1109/CVPR.2006.301}` | pendiente |
| viering2023 | `doi = {10.1109/TPAMI.2022.3220744}` | pendiente |
| zhang2004 | `pages = {56--85}` (artículo sin la discusión) | pendiente |
| stone1977 | `pages = {595--620}` (artículo sin la discusión) | pendiente |
| steinwart2007 | retirada (m6) | pendiente |
| cheng2007 y las 16 "no verificables" | sin cambio; se marcan como no verificadas en línea en la nota de continuidad | pendiente |

## Recuento

[pendiente]

## Cómputo usado en esta ronda

[pendiente]
