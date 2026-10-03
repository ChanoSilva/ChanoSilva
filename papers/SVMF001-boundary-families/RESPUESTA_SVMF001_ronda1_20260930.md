# SVMF001 — Respuesta del autor a la ronda 1 de revisión interna (informe del 30/09/2026)

Respuesta redactada el 03/10/2026 en una sesión de Claude Code (session_01MTmjU2K8b4sgpjjL3JTtDz), en el papel de autor. Informe atendido: `REFEREE_SVMF001_ronda1_20260930.md` (veredicto: cambios mayores; 2 bloqueantes, 5 mayores, 14 menores, bibliografía, recortes). Entregable: manuscrito v0.2 (`manuscript/main.pdf`, 14 páginas, 0 errores, 0 referencias indefinidas), `PREREGISTRO_SVMF001.md`, README, nota de continuidad y ficha actualizados.

**Recuento:** 21 hallazgos (2 B + 5 M + 14 m): **17 aceptados, 4 aceptados con matiz (B2, M4, M5, m4), 0 rebatidos.** Bibliografía: todas las correcciones del árbitro aplicadas. Al árbitro: gracias; el hallazgo B1 cambió el resultado numérico más citado del borrador y la reescritura es en su dirección.

---

## Hallazgos bloqueantes

### B1. Saturación sistemática de las rejillas — **ACEPTADO** (opción 1: rejillas ampliadas y corrida completa repetida)

Decisión. El recuento del árbitro sobre `results/results.json` v0.1 es exacto (lo reproducen los macros `\VOneEdge*` generados ahora desde `results/v01/`: γ_mult = 10 y C = 10 en 20/20 pliegues multiescala de la RBF; M = 8 en 14/20 cell-SVM y 16/20 LLSVM; k = 20 en 15/20). Las magnitudes del resultado negativo eran comparaciones entre métodos truncados por la rejilla y el manuscrito no lo decía.

Qué se hizo.
- `PREREGISTRO_SVMF001.md` (nuevo, fechado 03/10/2026, escrito antes de modificar el código y de correr): criterio, regímenes, semilla, rejillas ampliadas y qué se haría con los resultados. Rejillas v0.2: γ_mult ∈ {0.1, 0.3, 1, 3, 10, 30, 100}; C_RBF ∈ {0.1, 1, 10, 100, 1000}; M ∈ {1, 2, 4, 8, 16, 32} (cell-SVM y LLSVM); k ∈ {5, 10, 20, 50, 100, todos}; C_lineal ∈ {0.001, 0.01, 0.1, 1, 10} (extremo inferior, por el 8/10 del gaussiano). Lo demás no cambia.
- `experiments/run_comparison.py`: rejillas; `edge_counts` (fracción de pliegues con selección en el extremo inferior/superior de cada rejilla, por método e hiperparámetro; los extremos que son el miembro global —k = todos, M = 1, β = 0— no cuentan como saturación); guardia M ≤ puntos del pliegue interno (solo actúa en sub25 con 40 puntos, para M = 32); nombres legibles en la figura (m12). `make_numbers.py`: tabla de saturación (Tabla 4) y macros de recuento, incluidos los valores v0.1 leídos de `results/v01/` para que el texto "antes/después" no tenga números tipeados.
- Corrida completa única (semilla 20260930, BLAS a un hilo): 03/10/2026 04:04–04:08 UTC, 230.7 s de pared, 229 s de CPU (v0.1: 206 s), salida 0 (`results/run_log.txt`). Los resultados v0.1 se conservan en `results/v01/`. `exact_example.py` no se volvió a correr (ningún hallazgo toca sus números; el árbitro lo reprodujo cifra por cifra); solo se redibujó su figura con `--figure-only`.
- Tolerancia numérica (anotación fechada en el PREREGISTRO): una celda (cell-SVM, tablero, noise20) tenía IC [−0.075, −2.2·10⁻¹⁷] y quedaba "neg" por residuo de coma flotante, contra la convención declarada (m13). Se añadió `sig_of` con tolerancia 10⁻⁹ y un modo `--resummarise` que rehace resúmenes, criterio y bloque de robustez desde los pliegues guardados con las mismas semillas (IC idénticos, ninguna exactitud cambia). Único cambio de etiqueta: esa celda pasa a "none" (y sus dos homólogas del post hoc). Registrado en `results.json` (`meta.resummarised`).

Qué cambió en los números (v0.1 → v0.2, condición principal). El árbitro tenía razón en el fondo: buena parte de las magnitudes era efecto de la rejilla.
- Familias lineales locales en multiescala: lunas kNN-SVM −10.63 → **−0.37 [−1.63, +1.00]** (deja de ser significativa), cell-SVM −11.38 → −3.75 [−5.88, −1.25], LLSVM −12.00 → −7.38 [−9.13, −5.75]; tablero kNN-SVM −13.12 → −3.50 [−6.38, −0.50], cell-SVM −18.25 → −7.63 [−11.38, −3.25], LLSVM −17.75 → −4.88 [−7.63, −1.87]. La exactitud de kNN-SVM sube de 86.9 a 96.6 % (lunas) y de 73.9 a 85.9 % (tablero); la RBF pasa de 97.5 a 97.0 y de 87.0 a 89.4. En digits: kNN −0.87 → +0.75 (n.s.), cell −3.37 → −2.00, LLSVM −4.12 → −1.13.
- Recuento: 8 negativas / 1 positiva / 15 nulas → **9 / 1 / 14** (nuevas negativas: cell-SVM en wine −1.42 [−2.83, −0.01] y kNN-SVM en el gaussiano −2.62 [−3.88, −1.62]; deja de serlo kNN-SVM en lunas).
- Empate VB-RBF/RBF en multiescala: se mantiene (+0.12 [−1.25, +1.37]; +0.50 [−0.50, +2.12]). La celda positiva del gaussiano se mantiene pero se encoge: +0.75 [+0.12, +1.50] → **+0.37 [+0.12, +0.75]**; frente a su miembro global fijo (RBF) +0.12 [−0.25, +0.50]; frente al oráculo −0.62 [−2.00, +0.25]. Veredicto del criterio: sin cambio (nadie cumple (A); VB-RBF cumple (B) por la letra en el régimen "lineal" de un solo conjunto).
- Robustez: **4 de 48 intervalos por encima de 0** (v0.1: 0; ≈ 2.4 esperados por azar): VB-RBF-SVM en lunas con ruido +2.25 [+0.50, +4.00] y con submuestreo +5.50 [+2.25, +9.00] (también frente al oráculo y a la RBF fija), cell-SVM en lunas submuestreadas +5.00 [+2.25, +8.00], LLSVM en digits con ruido +2.00 [+0.75, +3.50] (frente al oráculo +0.75 [−2.50, +3.26], n.s.). kNN-SVM por debajo en 3/6 y 3/6 (v0.1: 4/6 y 3/6); VB-RBF por debajo en 1/6 con ruido (v0.1: 2/6) y 0/6 con submuestreo. Caídas medias de la referencia 7.1 / 6.4 pp (v0.1: 6.0 / 6.2).
- Saturación residual (condición principal, de 10 pliegues por conjunto): kNN-SVM k = 5 en 8/10 digits, 10/10 lunas, 10/10 tablero; LLSVM M = 32 en 7, 9, 10; cell-SVM M = 32 en 6, 4, 7; C = 10 de cell-SVM en 10/10 lunas y tablero y de LLSVM en 10/10 digits, 9/10 lunas, 10/10 tablero; RBF C = 1000 en 5/10 tablero; γ = 0.1·γ_med de la RBF en 8/10 del gaussiano (esperable: regla de Bayes lineal); lineal C = 0.001 en 7/10 tablero (irrelevante, 50 %). **Ya no hay saturación de γ por arriba** (0/10 en los seis conjuntos), que era la que infra-ajustaba a la referencia RBF.

Qué conclusiones cambian. (1) "Las familias lineales locales pierden 10–18 pp en multiescala" → "quedan por debajo en 5 de 6 celdas multiescala, entre 3.5 y 7.6 pp (kNN-SVM empata en las lunas), con la CV interna todavía en el extremo local de las rejillas": estado **medido, limitado por la rejilla** en texto, tabla de afirmaciones, README y ficha; la frase "piecewise-linear boundaries … do not reach the RBF-SVM" se reescribe diciendo que con las rejillas v0.1 el déficit era en gran parte de la rejilla, y que frente a su propio miembro global (la lineal) estas familias sí adaptan (+5 a +35 pp donde la frontera es curva). (2) "Ninguna familia queda significativamente por encima en robustez" → retirado; se reportan los 4/48 positivos, la expectativa por azar, la ausencia de criterio predefinido para robustez y su estatus de hipótesis. (3) El empate VB/RBF y la explicación de la celda positiva se mantienen y se refuerzan con la comparación anidada. (4) Resumen, afirmaciones, limitaciones, README, nota y ficha reescritos en consecuencia.

Por qué no se amplía otra vez la rejilla en esta ronda: el preregistro comprometía una sola corrida; el presupuesto de CPU de la ronda; y por debajo de k = 5 o por encima de M = 32 con 320 puntos las SVM lineales locales degeneran en votos de vecinos o reglas de centroide (otra familia). Se declara como limitación, se marca "grid-limited" y queda como siguiente paso con n mayor.

### B2. Sobreafirmación de robustez en los textos públicos — **ACEPTADO CON MATIZ**

Decisión. Se acepta el fondo: "ninguna familia es más robusta" afirmaba lo que el cuerpo no mide. El matiz es que el texto propuesto por el árbitro ("no se encontró evidencia de mayor robustez…; kNN-SVM por debajo en 4/6 y 3/6") quedó desactualizado por la nueva corrida: ahora hay 4/48 intervalos por encima de la referencia (3 en las lunas a dos escalas) y kNN-SVM está por debajo en 3/6 y 3/6. Texto final en ficha (ES/EN) y README: "No se encontró evidencia de mayor robustez de ninguna familia … que pueda afirmarse: 4 de 48 intervalos quedan por encima de la referencia (≈ 2.4 esperados por azar), tres de ellos en un mismo conjunto sintético, y se registran como hipótesis; kNN-SVM queda significativamente por debajo de la referencia en 3/6 y 3/6 conjuntos". "Post hoc" añadido donde la ficha habla de la mejor de las dos referencias. En el manuscrito (§5.2): "we claim no superior robustness for any family".

---

## Hallazgos mayores

### M1. Prop. 3.2 (caso estricto) y Cor. 3.5 — **ACEPTADO**

El árbitro tiene razón: R_nc(0) = R_nc(1) = 1/2, luego R_nc no es estrictamente decreciente en n ≥ 0 y el Cor. 3.5 no podía invocar la Prop. 3.2; el contraejemplo n = 1, M = 2 es correcto. Cambios: Prop. 3.2 enuncia ahora "si R_A es no creciente, ≥ R_A(n); si además R_A(n−1) > R_A(n) (en particular, si es estrictamente decreciente en {1,…,n}) y M ≥ 2, estrictamente mayor", con la prueba cerrada por P(N_j = n−1) = n p_j^{n−1}(1−p_j) > 0 cuando p_j < 1, R_A(N_j) = R_A(n−1) > R_A(n) en ese evento y ≥ R_A(n) en el resto. Prop. 3.4(ii) declara explícitamente R_nc(0) = R_nc(1) = 1/2 y R_nc(n+1) < R_nc(n) para n ≥ 1 (la prueba de acoplamiento ya daba eso). Cor. 3.5 añade "n ≥ 2" y una frase que verifica las hipótesis ("R_nc no creciente y R_nc(n−1) > R_nc(n) para n ≥ 2; para n = 1 ambas reglas tienen riesgo 1/2"). Resumen y tabla de afirmaciones: "strictly larger when the curve still decreases at the last step". Ningún número cambia (n = 320).

### M2. Multiplicidad — **ACEPTADO**

Añadido en el protocolo ("With 24 intervals at the 95 % level … about 1.2 (3.6 over the three conditions) are expected to exclude zero by chance alone; the majority clause is meant to absorb this, the single-data-set regime clause is not"), en el resumen, en el veredicto ("a single interval excluding zero among 24 is what chance alone would produce"), en la robustez (4 de 48 frente a ≈ 2.4) y en las limitaciones. Los conteos salen de macros (`\ExpectedFalseMain`, `\ExpectedFalseRobust`).

### M3. Anidamiento y referencia — **ACEPTADO**

Observación 2.3 reescrita: una familia solo puede superar a su propio miembro global por adaptación genuina, pero puede superar a la referencia *seleccionada* también por ruido en la selección de esa referencia; se declara que el miembro global de la kNN-SVM es la SVM lineal con C = 1 fijo, no la referencia lineal ajustada. Se reporta la comparación anidada frente al miembro global fijo (`*_vs_rbf`, `*_vs_linear` de `posthoc_oracle.json`) en la Tabla 7 del apéndice (con la salvedad de la kNN-SVM en el pie) y en el texto: VB-RBF-SVM frente a la RBF fija nunca es significativamente mejor (0/6; gaussiano +0.12 [−0.25, +0.50]); las familias lineales locales frente a la lineal son muy superiores donde la frontera es curva (reducen el término de aproximación), lo que matiza la lectura de B1. `posthoc_oracle.py` ya calculaba todo; solo faltaba reportarlo.

### M4. Extensión y legibilidad — **ACEPTADO CON MATIZ**

Aplicado: recortes 1–8 del árbitro (D1–D4 fuera del cuerpo y, por espacio, fuera del PDF: párrafo en el apéndice B y tabla completa en `results/exact_example.md`; mitad derecha de la Tabla 1 eliminada; tablas post hoc, de fracciones locales y de robustez por conjunto fuera del PDF, remitidas a `results/tables.md` y `results/posthoc_oracle.md`; figura de regiones al apéndice; Sección 6 reducida a nueve filas no redundantes; párrafos fusionados; Tablas 4 y 5 fusionadas en una tabla de dos líneas por conjunto a 8 pt sin `\resizebox`; párrafo "Details" al README; tabla de caídas medias eliminada y sus números en el texto; bibliografía a `\footnotesize`; sin páginas de flotantes vacías). Matiz: el PDF queda en **14 páginas (como v0.1), con cuerpo ≈ 11, apéndice ≈ 1.5 y bibliografía ≈ 1.5**, porque la ronda añadió lo que B1, M2, M3 y M5 exigen (tabla de saturación, tabla anidada, discusión de multiplicidad y preregistro, antes/después de las rejillas). Bajar de 10 obligaría a quitar demostraciones, la tabla de saturación o la bibliografía; se opta por el mínimo razonable y se declara.

### M5. "Predefinido" sin registro verificable — **ACEPTADO CON MATIZ**

Creado `PREREGISTRO_SVMF001.md` (fechado, antes de la corrida v0.2) con criterio, regímenes, semilla, rejillas y lo que se haría con los resultados; anotaciones post-corrida fechadas (incluida la tolerancia numérica). Cronología de v0.1 declarada en la nota de continuidad y en el manuscrito. Matiz honesto: para v0.1 **no existe** un registro fechado independiente del código; el manuscrito dice ahora "fixed in the code before the first run, but not in a dated record independent of the code, so that statement rests on the authors' word". La reducción de C_RBF a {0.1, 1, 10} se hizo por presupuesto antes de ejecutar ningún pliegue externo completo según la nota de la sesión original, y esa afirmación también descansa en la palabra del redactor.

---

## Hallazgos menores

| id | decisión | acción |
|---|---|---|
| m1 | aceptado | README, CONTINUIDAD y docstring de `exact_example.py`: Lema 2.2, Prop. 3.2, Observación 3.3 (la numeración del PDF) |
| m2 | aceptado | §4: "the RBF-SVM only if its score is strictly higher (ties go to the linear SVM)"; también en README y nota |
| m3 | aceptado | §4 y docstring: "each training label … is flipped independently with probability 0.2" |
| m4 | aceptado con matiz | la tabla de caídas se eliminó por espacio; la advertencia (otra partición; niveles distintos) va en el texto de §5.2 |
| m5 | aceptado | apéndice A: discontinuidad de a(·) en los puntos de entrenamiento; la Gram de entrenamiento y los números no se ven afectados |
| m6 | aceptado | "universal kernel" cita micchelli2006 y steinwart2008 §4.6; steinwart2007 retirada del texto y de `refs.bib` |
| m7 | aceptado | la frase "(its variable bandwidth was selected more often there)" se retiró; el nuevo texto da las fracciones de selección solo donde son pertinentes (lunas: 80 % y 80 %) |
| m8 | aceptado | "three real data sets and three synthetic ones in two regimes" |
| m9 | aceptado | "LLSVM-style mixture … a simplification of the locally linear SVM of Ladický and Torr" |
| m10 | aceptado | apéndice B: "global" (riesgo exacto del hiperplano) y kNN (riesgo condicional promediado) son estimadores distintos |
| m11 | aceptado | Lema 2.2: "positive-definite kernel … in the sense of Aronszajn (all Gram matrices are positive semidefinite)" |
| m12 | aceptado | Fig. 2 con nombres de las tablas en ejes y leyenda; Fig. 3 rehecha (2×4 a 7.5×4 in, títulos 8 pt, filas rotuladas); Fig. 1 leyenda central movida a la esquina inferior izquierda (redibujada desde el JSON, `--figure-only`) |
| m13 | aceptado | §4: "an interval whose endpoint is exactly zero counts as including zero"; implementado con tolerancia 10⁻⁹ (véase B1) |
| m14 | aceptado | `manuscript/*.bbl` quitado de `.gitignore`; `main.bbl` se conserva |

## Bibliografía

| entrada | acción |
|---|---|
| ladicky2011 | `pages = {985--992}`, `publisher = {Omnipress}`, `address = {Bellevue, WA}` |
| zhang2006 | `volume = {2}`, `doi = {10.1109/CVPR.2006.301}` |
| viering2023 | `doi = {10.1109/TPAMI.2022.3220744}` |
| zhang2004 | `pages = {56--85}` + nota "followed by a discussion, pp. 86–134" (no verificado en línea) |
| stone1977 | `pages = {595--620}` + nota "followed by a discussion, pp. 621–645" (no verificado en línea) |
| steinwart2007 | retirada (m6) |
| cheng2007 y las 16 no verificables por la red | sin cambios; marcadas como tales en la nota de continuidad (sección "Bibliografía: estado de verificación") |

## Recortes propuestos (1–8)

Todos aplicados, con dos diferencias respecto a la propuesta: la tabla D1–D4 y las tablas post hoc/fracciones/robustez por conjunto salen del PDF (a `results/*.md`) en lugar de ir al apéndice, por espacio; y la tabla de caídas medias también se elimina. Véase M4 para el recuento de páginas.

## Cómputo usado en esta ronda

Comparación completa 229 s de CPU (231 s de pared); `--resummarise` 4 s; `posthoc_oracle.py` 2 × 5 s; `make_region_figure.py` 28 s; `exact_example.py --figure-only` 2 s; prueba de humo 1.5 s; `make_numbers.py` ≈ 8 × 1 s. Total de experimentos ≈ 4.7 min; compilaciones LaTeX ≈ 1.5 min adicionales. Sin git; ninguna otra carpeta de `papers/` tocada.

## Qué queda abierto

1. Saturación residual en el extremo local (k = 5, M = 32, C máximo de cell/LLSVM; C = 1000 de la RBF en 5/10 del tablero): declarada; ampliar más cambia la naturaleza de las familias y se difiere a una corrida con n mayor.
2. Los 4 intervalos positivos de robustez son hipótesis (5 pliegues, sin criterio predefinido para robustez, 48 intervalos simultáneos).
3. El criterio de régimen de un solo conjunto no se repara a posteriori; se reparará (≥ 2 conjuntos) en la próxima corrida.
4. Predefinición de v0.1 no verificable independientemente.
5. 14 páginas frente al objetivo de ≤ 10.
6. Páginas de cheng2007, zhang2004 y stone1977 por confirmar en las fuentes.
