# Informe de arbitraje interno — SVMF001 "Families of Classification Boundaries" — ronda 1 (30/09/2026)

Árbitro independiente (no autor). Material leído completo: `README.md`, `CONTINUIDAD_SVMF001_20260930.md`, `FICHA_SVMF001_propuesta.md`, `manuscript/main.tex` (433 líneas), `refs.bib`, `numbers.tex` y `table_*.tex`, los seis `experiments/*.py`, `results/*.json|*.md|*.txt` y las 14 páginas del PDF (renderizadas a 70 dpi). Archivos de trabajo del árbitro en el scratchpad (`referee_SVMF001/`: notas, páginas, reproducción). Nada de la carpeta ha sido modificado.

## Veredicto

**Cambios mayores.** Las matemáticas son correctas salvo un desajuste de hipótesis reparable (M1), todos los números del texto salen de los JSON y el ejemplo exacto se reproduce cifra por cifra; pero (i) en el régimen multiescala y en digits la CV interna eligió el borde de la rejilla en casi todos los pliegues, para las referencias y para las familias, de modo que las magnitudes que sostienen el resultado negativo (−10 a −18 pp; "VB empata con RBF") son comparaciones entre métodos truncados por la rejilla y el manuscrito no lo reporta (B1); (ii) la ficha propuesta y el README afirman "ninguna familia es más robusta", que el cuerpo no mide (B2); (iii) no se discute la multiplicidad de 24 intervalos al 95 % (M2); (iv) 14 páginas frente a un objetivo de ≤ 10.

## Hallazgos bloqueantes

**B1. Saturación sistemática de las rejillas en los conjuntos que deciden el resultado.** Ubicación: `main.tex:247` (rejillas), `main.tex:295` ("piecewise-linear boundaries built from local linear SVMs do not reach the RBF-SVM"), `main.tex:376-378` (veredicto), `main.tex:421` (limitaciones, no lo menciona). Evidencia (recuento sobre `results/results.json`, condición principal, campos `folds[*][m]["cfg"]`): en los 20 pliegues de los dos conjuntos multiescala la RBF-SVM de referencia seleccionó `gamma_mult = 10` (borde superior) en 20/20 y `C = 10` (borde superior) en 20/20; VB-RBF-SVM `gamma_mult = 10` en 20/20; cell-SVM `M = 8` (borde superior) en 14/20; LLSVM `M = 8` en 16/20; kNN-SVM `k = 20` (borde inferior) en 15/20 (10/10 en el tablero). En digits: cell-SVM y LLSVM `M = 8` en 10/10, RBF `gamma_mult = 3` en 10/10. En el gaussiano lineal la SVM lineal de referencia eligió `C = 0.01` (borde inferior) en 8/10. Consecuencia: (a) la referencia RBF en multiescala está probablemente infra-ajustada (la frontera a escala 0.25/0.5 pide γ mayor), así que "la RBF-SVM" del texto es "la RBF-SVM con γ ≤ 10·γ_med, C ≤ 10"; (b) las familias lineales locales están limitadas a ≤ 8 celdas / ≥ 20 vecinos en un problema cuya estructura (4×4 celdas de lado ½ más 2×2 de lado 1) necesita del orden de 20 regiones, luego la frase de `main.tex:295` describe un efecto de la rejilla tanto como de la familia; (c) el "empate" VB/RBF se produce con ambas en el mismo borde de γ. Corrección propuesta (una de dos): **(1)** ampliar las rejillas y volver a correr: `gamma_mults` → `[0.1, 0.3, 1, 3, 10, 30, 100]`, `C_rbf` → `[0.1, 1, 10, 100, 1000]`, `cell_Ms`/`llsvm_Ms` → `[1, 2, 4, 8, 16, 32]`, `knn_ks` → `[5, 10, 20, 50, 100]`; coste estimado 2–3× los 206 s actuales (cabe en el presupuesto); añadir a `run_comparison.summarise` la fracción de pliegues con selección en el borde y una tabla de una fila por familia en el apéndice; **(2)** si no se vuelve a correr, reescribir `main.tex:295` como "with the grids of Section 4 (M ≤ 8, k ≥ 20, γ ≤ 10γ_med, C ≤ 10), which the inner cross-validation saturated in 14–20 of 20 multiscale folds, …", añadir la frase equivalente al párrafo de limitaciones (`main.tex:421`) y al README/ficha ("bajo las rejillas usadas"), y degradar en la Tabla 11 la fila "Local linear families are significantly worse … on the curved multiscale sets" a "measured, grid-limited".

**B2. Sobreafirmación de robustez en los textos públicos.** Ubicación: `FICHA_SVMF001_propuesta.md:13` ("Ninguna familia es más robusta con 20 % de ruido en etiquetas ni con 25 % de submuestreo") y `:24` ("No family is more robust under 20 % label noise or 25 % subsampling"); `README.md:27` ("Nadie es más robusto que la referencia; kNN-SVM es menos robusto"). El cuerpo (`main.tex:339`) dice, correctamente, "we find no evidence of superior robustness"; con 5 pliegues e IC de ±5 pp (p. ej. VB en lunas sub25: +4.25 [−1.75, +9.00]) la ausencia de evidencia no es evidencia de ausencia, y el propio manuscrito registra esas dos celdas como hipótesis. Además, "más robusto" no está definido: la caída absoluta (Tabla 8) se declara no comparable. Corrección: ficha ES "No se encontró evidencia de mayor robustez de ninguna familia bajo 20 % de ruido en etiquetas ni con el 25 % del entrenamiento; kNN-SVM queda significativamente por debajo de la referencia en 4/6 y 3/6 conjuntos"; ficha EN "No evidence of superior robustness was found for any family under 20 % label noise or 25 % subsampling; kNN-SVM is significantly below the reference on 4/6 and 3/6 data sets"; README igual. Añadir "post hoc" donde la ficha dice "desaparece frente a la mejor de las dos referencias".

## Hallazgos mayores

**M1. Prop. 3.2 (caso estricto) y Cor. 3.5: la hipótesis no la cumple R_nc.** Ubicación: `main.tex:125` ("if R_A is strictly decreasing and M ≥ 2, it is strictly larger"), `main.tex:135-147` Prop. 3.4(ii) ("non-increasing in n ≥ 0 and strictly decreasing for n ≥ 1"), `main.tex:150` Cor. 3.5 (sin restricción sobre n). Problema: R_nc(0) = R_nc(1) = 1/2, luego R_nc no es estrictamente decreciente en n ≥ 0 y el Cor. 3.5 no puede invocar la Prop. 3.2 tal como está enunciada; de hecho la conclusión es falsa en n = 1: para n = 1 y M = 2, E R = ½ = R_nc(1) (comprobado numéricamente). La prueba de la Prop. 3.2 funciona si existe m < n alcanzable con R_A(m) > R_A(n). Corrección: en `main.tex:125` sustituir por "if R_A is non-increasing and R_A(n−1) > R_A(n) (in particular if R_A is strictly decreasing on {1,…,n}) and M ≥ 2, then it is strictly larger, because P(N_j = n−1) > 0"; en el Cor. 3.5 añadir "n ≥ 2". Ningún número cambia (n = 320).

**M2. Multiplicidad no discutida.** Ubicación: `main.tex:249-251` y `main.tex:304`. Con 24 intervalos al 95 % en la condición principal (72 en total) se esperan ≈ 1.2 (≈ 3.6) intervalos que excluyan 0 por azar bajo la hipótesis nula de ninguna diferencia; la única celda positiva es compatible con eso incluso antes de la explicación por selección. La cláusula (A) (mayoría) protege; la cláusula (B) con un régimen de un solo conjunto no protege en absoluto, y es exactamente la que se "cumplió". Corrección: añadir una frase en `main.tex:249` ("With 24 intervals at the 95 % level, about one is expected to exclude zero by chance alone; the majority clause is meant to absorb this, the single-data-set regime clause does not") y una en `main.tex:304`.

**M3. Nesting y referencia: enunciado demasiado fuerte y comparación anidada no reportada.** Ubicación: `main.tex:106` ("can rise above the best global reference only through genuine adaptation") — falso tal como está: puede subir por ruido en la *selección de la referencia*, que es lo que el propio manuscrito demuestra en el gaussiano (la CV interna eligió RBF en 8/10 pliegues con exactitud de prueba inferior a la lineal; en el pliegue 1: lineal 0.950, RBF 0.875, VB 0.9125). Además (i) el "miembro global" de kNN-SVM es la SVM lineal con C = 1 fijo, no la referencia lineal ajustada (que eligió C ≠ 1 en 36/60 pliegues), así que la cadena "familia ⊇ referencia" no es exacta para esa familia; (ii) la comparación realmente anidada (familia frente a su propio miembro global fijo: VB vs RBF, cell/LLSVM/kNN vs lineal) ya está calculada en `results/posthoc_oracle.json` (`*_vs_rbf`, `*_vs_linear`) y no se reporta: VB vs RBF fija en el gaussiano es +0.50 [−0.25, +1.37], en todos los conjuntos ninguna celda significativa. Corrección: reescribir `main.tex:106` como "and can rise above its own global member only through genuine adaptation; it can rise above the *selected* best global reference also through selection noise in that choice (Section 5.1)"; añadir a la Tabla 6 (o al apéndice) la columna "vs. own global member"; decir explícitamente que el miembro global de kNN-SVM es la lineal con C = 1.

**M4. Extensión y legibilidad.** 14 páginas (objetivo 5–10). Tablas 5, 6 y 9 van en `\resizebox{\linewidth}` (`main.tex:275, 309, 359`) y salen a ~6 pt, ilegibles en papel; la página 10 queda medio vacía por la colocación de flotantes; la Sección 6 (Tabla 11) repite el resumen y las limitaciones. Véase "Recortes propuestos".

**M5. "Predefinido" sin registro verificable.** Ubicación: `main.tex:251` ("the criterion, the regimes, the grids and the seed were fixed before the run"); `CONTINUIDAD:36-37` ("Para caber en el presupuesto: rejilla de C de la RBF reducida a {0.1, 1, 10}; 2×5 pliegues …"; "la primera ejecución del ejemplo exacto tardó 422 s … se redujeron D2 y el Monte Carlo"). No hay archivo fechado/hash del criterio y las rejillas antes de la primera corrida completa; la nota no dice si la reducción de la rejilla de C ocurrió antes o después de ver algún resultado externo. No encuentro indicios de ajuste a posteriori del criterio (el código `evaluate_criterion` coincide con el texto; el chequeo oráculo está etiquetado post hoc en código, nota y manuscrito; la reducción de D2/MC afecta solo a ilustraciones y la nota afirma coherencia con la primera ejecución), pero la afirmación descansa en la palabra del redactor. Corrección: añadir `PREREGISTRO_SVMF001.md` con criterio, regímenes, rejillas y semilla, y declarar en la nota la cronología exacta de la reducción de rejillas ("antes de cualquier pliegue externo" si es cierto); en la próxima corrida (B1) fijar y fechar las rejillas ampliadas antes de ejecutar.

## Hallazgos menores

**m1.** Numeración incoherente: `README.md:25` y `CONTINUIDAD:15,22,29,30,46,50` citan "Lema 2.3" (núcleo) y "Prop. 3.3" (adelgazamiento); el manuscrito/PDF tiene Lemma 2.2 y Proposition 3.2 (Remark 3.3 es la observación de cobertura). `experiments/exact_example.py:15,19` dice "Proposition 2 of the paper". Corregir los tres.

**m2.** Regla de desempate de la referencia no declarada: `run_comparison.py:172` elige RBF solo si su puntuación interna es estrictamente mayor; hubo 10 empates (p. ej. breast cancer principal ×2, gaussiano principal ×1) resueltos a favor de la lineal. Declararlo en `main.tex:249`.

**m3.** `main.tex:247` dice "20 % of the training labels … are flipped"; el código (`run_comparison.py:157`) invierte cada etiqueta con probabilidad 0.2 (Bernoulli), no exactamente el 20 %. Decir "each training label is flipped independently with probability 0.2".

**m4.** Las "caídas" de la Tabla 8 restan medias calculadas sobre particiones distintas (2×5 pliegues con una semilla, 1×5 con otra: `run_comparison.py:271`), así que mezclan el efecto de la condición con la variabilidad de la partición. Decirlo en el pie de la Tabla 8 o calcular las condiciones de robustez sobre los mismos 5 pliegues de la primera repetición.

**m5.** Ancho de banda discontinuo en los puntos de entrenamiento (`families.py:225-236`): r_κ excluye el propio punto en entrenamiento y no hay exclusión para consultas, luego a(·) no es una función única de x y K_a(z, x_i) no tiende a 1 cuando z → x_i. No afecta a la PSD de la Gram de entrenamiento ni a los resultados, pero contradice la letra del Lema 2.2 ("any function a"). Una frase en el apéndice basta.

**m6.** `main.tex:118` cita `steinwart2007` (tasas rápidas con núcleos gaussianos) para "universal kernel"; la referencia natural es Steinwart (2001, JMLR 2:67–93) o `steinwart2008` §4.6, ya citado.

**m7.** `main.tex:339` "(its variable bandwidth was selected more often there)": cierto para lunas (0.1 → 0.6) pero no para breast cancer (0.2 → 0.2). Reformular.

**m8.** `main.tex:49` "(three real, three synthetic regimes)" es ambiguo: son tres conjuntos reales y tres sintéticos en dos regímenes nombrados (lineal, multiescala). Escribir "three real data sets and three synthetic ones in two regimes".

**m9.** LLSVM (`main.tex:87`): los pesos softmax de distancia a anclas son una simplificación de la codificación local de Ladický–Torr; el código ya dice "LLSVM-style". Usar la misma expresión en el texto.

**m10.** Tabla 2, D2: el valor "global" usa el riesgo exacto del hiperplano y los valores kNN el riesgo condicional promediado en 125 puntos de prueba; son estimadores distintos. Añadirlo al pie.

**m11.** Lema 2.2: "positive-definite" se usa en sentido Aronszajn (Gram semidefinida positiva). Decir "positive semidefinite Gram matrices (a kernel in the sense of Aronszajn)" para evitar la lectura "estrictamente".

**m12.** Figuras: Fig. 2 usa nombres de código (`knn_svm`, `moons_2scale`) en ejes y leyenda; Fig. 3 títulos a ~6 pt; Fig. 1 (panel central) la leyenda tapa parte de la curva. Usar los nombres de las tablas y mover leyendas.

**m13.** Las dos celdas con límite inferior exactamente 0 y media positiva (noise20: LLSVM en breast cancer +1.00 [0.00, +3.00]; VB en digits +1.50 [0.00, +4.00]) se clasifican como "none" porque la regla es `lo > 0` estricta. Correcto y conservador; declarar la convención ("an interval whose endpoint is exactly zero counts as including zero").

**m14.** `.gitignore` excluye `main.bbl`, pero `manuscript/main.bbl` está en la carpeta; decidir (para reproducibilidad del PDF conviene conservarlo y quitarlo del `.gitignore`).

## Bibliografía

Red: `api.crossref.org`, `jmlr.org` y `arxiv.org` bloqueados por el proxy de salida (CONNECT 403); solo funcionó la búsqueda web. Cada cita respalda la afirmación para la que se usa salvo `steinwart2007` (m6).

| Entrada | Estado | Corrección / comentario |
|---|---|---|
| ladicky2011 | **corregida** (verificada en línea) | añadir `pages = {985--992}` (ICML 2011, Bellevue); opcional `publisher = {Omnipress}` |
| viering2023 | verificada | IEEE TPAMI 45(6):7799–7819, 2023; añadir `doi = {10.1109/TPAMI.2022.3220744}` |
| segata2010 | verificada | JMLR 11:1883–1926, 2010 |
| zhang2006 | verificada; completar | CVPR 2006, **vol. 2**, pp. 2126–2136; añadir `volume = {2}`, `doi = {10.1109/CVPR.2006.301}` |
| cheng2007 | existencia verificada; **páginas no verificables** en línea | 461–466 coincide con el conocimiento del árbitro (SDM 2007, Minneapolis); confirmar en epubs.siam.org |
| bottou1992 | verificada | Neural Computation 4(6):888–900 |
| abramson1982 | verificada | Ann. Statist. 10(4):1217–1223 |
| zhang2004 | no verificable en línea | el artículo ocupa 56–85; 86–134 es la discusión. Usar `pages = {56--85}` o indicar "with discussion" |
| stone1977 | no verificable en línea | el artículo ocupa 595–620; hasta 645 con discusión. Mismo tratamiento |
| steinwart2007 | no verificable en línea; campos coinciden con el conocimiento del árbitro | ver m6 (cita poco pertinente para "universal kernel") |
| cortes1995, steinwart2008, bartlett2006, devroye1996, cover1967, hastie2009, vapnik1998, scholkopf2002, micchelli2006, terrell1992, pedregosa2011, chang2011, dietterich1998, demsar2006, nadeau2003, efron1993 | no verificables en línea (red); todos los campos coinciden con el conocimiento del árbitro | sin cambios propuestos |

Resumen: 7 verificadas en línea (1 de ellas corregida, 1 completada), 19 no verificables por la red (2 con sugerencia de páginas), 0 erróneas detectadas.

## Verificación computacional

- **Macros ↔ JSON.** Script del árbitro: 45 macros muestreadas de `numbers.tex` (diferencias, IC, exactitudes, fracciones de selección, recuentos de celdas, caídas de robustez, segundos, ratios exactos, k peor de D1) coinciden con `results.json`, `exact_example.json`, `posthoc_oracle.json`; `diff_mean` = media(familia) − media(referencia) en las 24 celdas; `best_global.acc` = exactitud del método elegido en los 120 pliegues; `evaluate_criterion` recalculado da el mismo veredicto (VB: 1/6 positivas, régimen "linear").
- **Lema 2.2.** Producto interno de gaussianas y norma comprobados por cuadratura en d = 1 (coinciden a 1e−15); 1000 matrices de Gram aleatorias (n = 40, d ∈ {1,2,5,16,30}, anchos entre e^−5 y e^5): autovalor mínimo ≥ 0; testigo de 5 puntos reproducido (−0.962 sin prefactor, +0.043 con él). El código `vb_kernel` implementa exactamente el exponente d/2.
- **Prop. 3.4 / Cor. 3.5.** E[R(t̂)] = Φ(−μ/√(1+s²)) comprobado por cuadratura; R''(0) = μφ(μ) comprobado; R_nc(320) = 0.0502507, exceso 2.658e−4, ratios 2.01 / 4.08 / 8.38 / 17.99 / 61.68 recalculados con código independiente; contraejemplo n = 1 (M1).
- **Reproducción rápida** (copia de `experiments/` en el scratchpad, sin tocar `results/`): `run_comparison.py --fast` (1×3 pliegues, rejillas reducidas, 6 conjuntos): 25.1 s de pared, 25.4 s de CPU, salida 0. Cualitativamente coherente (familias lineales locales pierden en lunas, VB empata con RBF) pero no comparable número a número por el protocolo reducido (p. ej. en el gaussiano VB −2.24 [−4.48, 0.00]). `exact_example.py` completo: 29.6 s de pared, 32.3 s de CPU; el JSON resultante es **idéntico** al publicado en todos los campos salvo `meta.seconds` (27.84 → 29.63). Total de CPU consumido por el árbitro: ≈ 65 s.
- Entorno: Python 3.11, NumPy 2.4.6, SciPy 1.17.1, scikit-learn 1.9.1 (iguales a los declarados).

## Recortes propuestos (de 14 a ≤ 10 páginas, sin perder contenido verificable)

1. Tabla 2 (D1–D4) y el párrafo "Illustration for rules not covered…" → apéndice B; en el cuerpo dejar dos frases y la Figura 1 (≈ −0.8 p).
2. Mitad derecha de la Tabla 1 (curva R_nc(n)) → eliminar; ya está en el panel derecho de la Figura 1 (≈ −0.3 p).
3. Tablas 6 (post hoc), 7 (fracciones locales) y 9 (robustez por conjunto) → apéndice o `results/tables.md`, con una frase cada una en el cuerpo (≈ −1.5 p).
4. Figura 3 (regiones de decisión) → apéndice (≈ −0.5 p).
5. Sección 6 / Tabla 11: eliminar o reducir a las seis filas que no repiten el resumen ni las limitaciones (≈ −0.8 p).
6. Fusionar "Did the inner cross-validation want to be local?" con "The one positive cell" (≈ −0.3 p).
7. Fusionar Tablas 4 y 5 en una sola (exactitud de la referencia + diferencias) y quitar los `\resizebox` usando `\footnotesize` y `tabcolsep` 3 pt (≈ −0.4 p y legibilidad).
8. Párrafo "Details" del Apéndice A → README (≈ −0.3 p).
Estimación: ≈ 9–9.5 páginas.

## Alcance (ficha pública)

La ficha propuesta es coherente con un estudio metodológico reconstruido y no afirma aplicaciones; con B2 corregida y la precisión de B1 ("bajo las rejillas usadas" o con rejillas ampliadas) puede publicarse. Mantener "reconstrucción autocontenida" y "n ≤ 400" tal como están.

## Lista de acciones (por prioridad)

1. Amplía las rejillas (γ hasta 100·γ_med, C hasta 1000, M hasta 32, k desde 5), vuelve a correr `run_comparison.py` y reporta la fracción de selecciones en el borde; si no, reescribe `main.tex:295`, `:421`, Tabla 11, README y ficha como resultados "bajo las rejillas usadas" (B1).
2. Sustituye en `FICHA_SVMF001_propuesta.md:13,24` y `README.md:27` "ninguna familia es más robusta / nadie es más robusto" por "no se encontró evidencia de mayor robustez" y añade "post hoc" al chequeo oráculo (B2).
3. Corrige el caso estricto de la Prop. 3.2 (`main.tex:125`) a "R_A no creciente y R_A(n−1) > R_A(n)" y añade "n ≥ 2" al Cor. 3.5 (M1).
4. Añade la frase de multiplicidad (≈ 1.2 intervalos espurios esperados entre 24) en `main.tex:249` y `:304` (M2).
5. Reescribe `main.tex:106` (ruido de selección de la referencia), declara que el miembro global de kNN-SVM es la lineal con C = 1 y añade la columna "vs. own global member" tomada de `posthoc_oracle.json` (M3).
6. Crea `PREREGISTRO_SVMF001.md` fechado con criterio, regímenes, rejillas y semilla, y aclara en la nota la cronología de la reducción de rejillas (M5).
7. Aplica los recortes 1–8 y elimina los `\resizebox` (M4).
8. Unifica la numeración (Lemma 2.2 / Prop. 3.2) en README, CONTINUIDAD y `exact_example.py` (m1).
9. Declara el desempate de la referencia hacia la lineal y la convención de IC con extremo 0 (m2, m13).
10. Corrige "20 % flipped" → "each label flipped with probability 0.2" y añade la nota sobre particiones distintas en la Tabla 8 (m3, m4).
11. Añade `pages = {985--992}` a ladicky2011, `volume = {2}` y DOI a zhang2006, DOI a viering2023; revisa páginas de zhang2004 y stone1977; cambia la cita de "universal kernel" (bibliografía, m6).
12. Anota la discontinuidad de a(·) en puntos de entrenamiento, el estimador distinto de D2 "global" y "LLSVM-style" (m5, m9, m10).
13. Renombra ejes y leyendas de las Figuras 1–3 con los nombres de las tablas (m12).
