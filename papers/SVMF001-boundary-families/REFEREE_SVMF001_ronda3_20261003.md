# Informe de arbitraje interno independiente — SVMF001, ronda 3 (v0.4, commit 7e03402)

Árbitro: agente independiente (no participó en las rondas 1–2 ni en la teoría v0.4). Fecha: 03/10/2026.
Trabajo auxiliar (fuera del repositorio): `scratchpad/referee3_SVMF001/` (`exact_ref.py`, `mc_select.py`, `mc_select_svm.py`, `mc_rinf.py`, `majority_search.py`, `majority_sklearn.py`, copia `copy/` para compilar y regenerar macros). No se ha tocado nada de la carpeta salvo este informe.

## Veredicto

**Cambios menores (solo de texto).** Las piezas nuevas de v0.4 (Prop. 3.6, Cor. 3.7, Lemas 3.8–3.10, Teorema 3.11, Cor. 3.12) son correctas tal como están enunciadas y como las prueba el Apéndice C; ni la lectura paso a paso ni la verificación numérica propia encuentran errores ni contraejemplos. Antes de circular hay que corregir dos afirmaciones de estado (resumen y tabla frente a la Tabla 5; "verified numerically" de la Obs. 3.13) y recortar unas 2 páginas.

Recuento: 0 bloqueantes, 3 mayores (todos de texto), 10 menores. Ronda 2: 16 de 17 puntos bien aplicados, 1 a medias (extensión), 0 sin aplicar.

## 0. Teoremas nuevos v0.4 (prioridad máxima)

### 0.1 Lectura paso a paso

| resultado | dictamen | comentario |
|---|---|---|
| Prop. 3.6 `prop:select` (main.tex:158–167) | **correcta** | El bloque B=((X_i,Y_i)_{i≤n},(X,Y)) es independiente de G=σ(W_1..W_n,W,U) por la estructura producto (triples independientes, W_i⊥(X_i,Y_i) dentro de cada uno, U independiente). {I=J}∈G para cada J⊆{1..n} (ι medible con valores en un conjunto finito). La suma finita Σ_J 1{I=J}·P(A(S_J)(X)≠Y │ G) es legítima y cada término vale R_A(│J│) por B⊥G. Contiene la Prop. 3.2 (W_i=Z_i, W=Z, I={i:Z_i=Z}, K│Z=j ~ Bin(n,p_j)); la condición de estrictez "P(R_A(K)>R_A(n))>0" cubre la de la Prop. 3.2. Hipótesis implícitas no escritas: véase m1. |
| Cor. 3.7 `cor:knnfree` (171–173) | **correcta** | Consecuencia directa con K=k y la monotonía estricta de R_nc en n≥1 (Prop. 3.4). Cocientes reproducidos (tabla 0.3). |
| Lema 3.8 `lem:radius` (177–179; prueba 365–367) | **correcto** | Argumento clásico de estadísticos de orden. La hipótesis exacta usada es la que dice el paréntesis: que la ley de ‖X−x‖ (en ese x) no tenga átomos; con ella las distancias son distintas c.s., 1−F(s)=P(‖X−x‖>s) y el evento {(I,J)=(I,j)} está bien definido. La ley condicional dada R=r es una versión regular (c.t.p. en r), como se dice. Falta cita (m3). |
| Lema 3.9 `lem:popsign` (181–186) | **correcto** | g impar y estrictamente creciente (g' = varianza de la normal truncada); x−t_r(x)=½[g(μ+x)−g(μ−x)] tiene el signo de x. |
| Lema 3.10 `lem:majority` (190–192; prueba 369–371) | **correcto** | Cada desigualdad comprobada: F(ŵ,b̂')≤F(0,0)=Ck ⇒ ‖ŵ‖≤√(2Ck); F≤F(0,1)=2Cn₋; cota inferior por 1-Lipschitz de la bisagra; Σh(y_jb')≥k para b'≤0 (=k+b'(n₋−n₊) en [−1,0], ≥2n₊>k debajo); de ahí 1≤n₊−n₋≤kr√(2Ck), absurdo si r<r₀. Vale para *todo* minimizador (el intercepto no es único en general). **Convención:** el objetivo con intercepto sin penalizar es el de libsvm, que es lo que usa el experimento (`families.py:45–46`, `SVC(kernel="linear", C=C)`, y `families.py:117–118`), no `LinearSVC` (liblinear penaliza el intercepto): coincide. Matices de implementación y holgura de r₀: m2. |
| Teorema 3.11 `thm:kfixed` (194–208; prueba 373–379) | **correcto** | (i) El paso al límite es por **convergencia dominada con convergencia puntual** de π_n(x) para todo x; no hace falta uniformidad en x (integrando acotado por 1). Para cada x: R_n→0 en probabilidad porque f>0; τ(r)→0 por continuidad y positividad de f en x, y E min{1,τ(R_n)}→0. El acoplamiento de etiquetas (VT ≤ Σ│η(x+D_j)−η(x)│ ≤ kμR_n/2, con │∂η/∂x₁│=2μη(1−η)≤μ/2) es correcto porque la vecindad es función solo de las entradas. P(S=0)=0 porque una vecindad mixta tiene k≥2 y al menos un punto interior con primera coordenada continua (para m=1 el punto frontera es ±1, discreto, y no se necesita). **Frontera η=½**: es {x₁=0}, de medida nula, y allí el integrando vale 0. Álgebra de (a−½)(1−a^k+b^k), igualdad k=1,2 y monotonía estricta en k≥2 verificadas a mano. (ii) Usa solo R_n<r₀ ⇒ voto mayoritario (Lema 3.10, r₀ no depende de la geometría) y el acoplamiento; no necesita el Lema 3.8. **Entradas estandarizadas:** correcto; el radio estandarizado está acotado por R_n/min_l σ̂_l y los desplazamientos originales por max_l σ̂_l·R_n^std, ambos →0 en probabilidad; el Lema 3.10 se aplica en coordenadas estandarizadas con el mismo r₀. El enunciado del cuerpo coincide con lo que prueba el apéndice. Observación de presentación sobre R_∞(k)→½: m10. |
| Cor. 3.12 `cor:kfixed` (210–212) | **correcto** | R_nc(n)→R* (convergencia dominada en la Prop. 3.4(ii)) y límites >R* ⇒ existe n₀(k); sin n₀ explícito, como se declara. Compara la kNN-SVM con el umbral de centroides global, no con la SVM lineal global (declarado; véase m9). |
| Obs. 3.13 `rem:rho` (214–216) | **heurística, declarada como tal** | La cuenta de primer orden es correcta (rehecha: exceso ≈ μφ(μ)σ²/(2v²) con σ²=v/(ρn) y ∫₀^∞uΦ(−u)du=¼ dan μφ(μ)/(2ρvn)). No se presenta como demostrada. Pero la etiqueta "verified numerically" exagera lo que muestran los datos (M2). |

### 0.2 Verificación numérica independiente (código propio, sin funciones del autor)

1. **Prop. 3.6 con selecciones raras** (`mc_select.py`, 40 000 réplicas, μ=0.8, n=30, W discreto en {0,1,2,3} para forzar empates; riesgo exacto dado el umbral; comparación pareada con R_nc(K) exacto):

| selección | E R(loc) − E R_A(K) | z |
|---|---|---|
| kNN en W con empates masivos rotos por U | +0.00013 ± 0.00021 | +0.63 |
| misma celda de W ∪ moneda auxiliar (K aleatorio) | −0.00012 ± 0.00012 | −0.97 |
| "récords por la izquierda" si W > mediana, si no los primeros 3·#valores distintos | −0.00012 ± 0.00033 | −0.35 |
| 2-medias en W con inicialización aleatoria (U), 3 pasos de Lloyd | +0.00004 ± 0.00008 | +0.52 |
| **control**: kNN en la coordenada de señal | +0.0604 ± 0.0023 | **+26.5** |
| **control**: selección que usa etiquetas (4 positivos + 3 negativos) | −0.0068 ± 0.0001 | **−67.3** |

Con A = SVM lineal (`SVC`, C=1) sobre X₁ y selección "celda ∪ moneda" (3 000 réplicas, pareada contra una muestra i.i.d. nueva de tamaño K; `mc_select_svm.py`): +0.0011 ± 0.0022 (z=0.49). La identidad se cumple con selecciones dependientes de W con empates y aleatorizadas, y los controles muestran que el test tiene potencia: falla en cuanto la selección mira X₁ o las etiquetas.

2. **Límites del Teorema 3.11** (`exact_ref.py` por cuadratura; `mc_rinf.py`, n=50 000, 30 muestras × 4 000 consultas en m=1, 10 × 4 000 en m=2; exceso estimado como E[│2η−1│·1{pred≠Bayes}]):

| k | R_∞(k) (cuadratura propia) | MC m=1 | MC m=2 | límite del voto (propio) | voto MC m=1 |
|---|---|---|---|---|---|
| 1 | 0.07434 | 0.07451 ± 0.00036 | 0.07552 ± 0.00063 | 0.07434 | 0.07451 ± 0.00036 |
| 2 | 0.07434 | 0.07435 ± 0.00037 | 0.07476 ± 0.00059 | — | — |
| 3 | 0.08154 | 0.08148 ± 0.00045 | 0.08182 ± 0.00074 | 0.05995 | 0.05984 ± 0.00022 |
| 5 | 0.09530 | 0.09529 ± 0.00053 | 0.09422 ± 0.00086 | 0.05613 | 0.05605 ± 0.00013 |

Todo dentro de 1.9 errores estándar (μ=1.645), incluida la igualdad no trivial R_∞(1)=R_∞(2) y el caso m=2 (vecindades en ambas coordenadas). `SVC(kernel="linear", C=1, tol=1e-6)` predijo la mayoría en 900/900 vecindades mixtas con k=3 a n=50 000 y también en 900/900 a n=320.

3. **Contraejemplos al Lema 3.10** (`majority_search.py`: solver exacto propio en d=1 —mínimo exacto en b' sobre los puntos de quiebre y sección áurea en w—, búsqueda adversarial de Nelder–Mead sobre las posiciones con mayoría mínima n₊=n₋+1; se mide el hueco G₋−G entre el mínimo con b'≤0 y el global, positivo ⇔ todo minimizador predice la mayoría):
   - Para r/r₀ ∈ {0.5, 0.99, 1.5} y k ∈ {3,5,9}, C ∈ {1,10}: hueco mínimo ≥ 0.95·C. **Ningún contraejemplo.**
   - Primer hueco nulo (predicción de la minoría posible): entre 3 y 6·r₀ (k=3), entre 6 y 12·r₀ (k=5), entre 12 y 25·r₀ (k=9).
   - `majority_sklearn.py` con libsvm por defecto (tol=1e−3), d ∈ {1,2,5}, k ∈ {3,5,9}, C ∈ {1,10,100}, r/r₀ ∈ {0.5,0.9,0.999}: 0/3 240 predicciones de la minoría o decisión nula. Búsqueda aleatoria de la primera predicción minoritaria con C=1: r/r₀ ≈ 7.3 (k=3), 14.2 (k=5), 25.8 (k=9). El lema es correcto y **r₀ es holgado en un factor que crece con k** (≈ k^{1}·2–3); véase m2.

### 0.3 Números de v0.4 contra resultados

Cifras de forma cerrada recalculadas con código propio, todas coinciden con las macros (`manuscript/knn_numbers.tex`): cocientes del Cor. 3.7 4.036/16.84/176.5 (macros 4.04/16.8/176); R_∞(k) para μ=1.645: 0.07434, 0.08154, 0.09530, 0.12020, 0.15071 (macros 0.0743…0.1507) y para μ=0.5: 0.3980, 0.4129, 0.4403, 0.4739, 0.4919; límites del voto 0.05995 y 0.05344 (0.0599, 0.0534); Q(½)=5.612, Q(¼)=20.29 (μ=1.645) y 11.45, 94.37 (μ=0.5). Las cotas dirigidas comprobadas contra `theory/check_knn_localisation_output.txt`: z máx. 1.33 a n=20 000, k≤5 (macro "1.4", hacia arriba); diferencia máx. 0.00235 (μ=0.5, k=20; macro 0.0024, hacia arriba); hueco mínimo 0.02396 (μ=1.645, n=320, k=2; macro 0.023, hacia abajo); d=2,5 a n=2000 entre 0.07625 y 0.10947 (0.076 y 0.110). `KLSelMaxZ`=1.4 frente a 1.36 real, correcto aunque viene del redondeo al más cercano. 36 = 2 μ × 3 n × 6 k y 14 = 18 filas P1 menos las 4 con k=1: correcto.

### 0.4 Etiquetas de estado

La tabla de afirmaciones (main.tex:330–345) separa bien "proved here (v0.4); not yet checked by an independent referee" (filas 1 y 3) de "verified, not proved" (fila 4), y la Obs. 3.13 no se presenta como demostrada (status "heuristic, not proved", main.tex:214; Limitations main.tex:347; FICHA:14,25 "es una heurística"). Dos defectos: la palabra "verified" aplicada a la inflación 1/(ρv) (M2) y la ausencia del Cor. 3.7 y del Lema 3.8 en la tabla (m5). README:31 dice "comprobada numéricamente" (M2).

## 1. Verificación de la ronda anterior (ronda 2)

| id | estado | evidencia (archivo:línea, versión actual) |
|---|---|---|
| M1 empate VB/RBF limitado por la rejilla | aplicado bien | main.tex:272 ("This tie is grid-limited too", recuentos por macro); fila de la tabla main.tex:338 "measured, grid-limited"; resumen main.tex:53; PREREGISTRO_SVMF001.md:44–46 (anotación correctora). |
| M2 "no alcanzan la RBF"; mecanismo de varianza; rejillas de C | aplicado bien | main.tex:270 ("what the three families do not do under the grids…", "an omission of our preregistration"); main.tex:305 ("consistent with, though not covered by"); main.tex:347 ("not attributed to that mechanism"); PREREGISTRO:47. |
| M3 paréntesis de la Prop. 3.2 | aplicado bien | main.tex:116 "(in particular, if n≥2 and R_A is strictly decreasing on {1,…,n})": ahora implica R_A(n−1)>R_A(n). |
| M4 recuentos esperados por azar unilaterales y cobertura real | aplicado bien | main.tex:237; numbers.tex:531–539 (`\CovTen`=89.9, `\CovFive`=83.5, `\ExpectedPosMain`=1.2, `\ExpectedPosRobust`=4.0); `experiments/bootstrap_coverage.py`. |
| M5 preregistro verificable | aplicado bien (con el matiz aceptable del autor) | main.tex:239; `head -n 40 PREREGISTRO_SVMF001.md │ sha256sum` = c89b2c76…132be, igual al anotado (PREREGISTRO:45). |
| M6 celda gaussiana | aplicado bien | main.tex:272 (`\GaussCellPts` … `\GaussSelLinLossFolds`). Véase la propuesta de recorte 7. |
| M7 extensión | **a medias** | v0.3 bajó a 12 pp.; v0.4 sube a **16 pp.** (compilación propia), por encima del ≤ 14 del coordinador. Véase M3. |
| m1 sub-rejillas de C del miembro global | aplicado bien | main.tex:101; pie de la tabla anidada main.tex:299. |
| m2 "in population risk" | aplicado bien | main.tex:101. |
| m3 wine/cell-SVM −0.008 pp | aplicado bien | main.tex:259; numbers.tex:1739. |
| m4 tres positivos persisten | aplicado bien | main.tex:305; fila main.tex:339. |
| m5 riesgo frente a exceso en D1 | aplicado bien | main.tex:357 ("in excess risk … more than a hundred times larger"). |
| m6 condicionar en S̃ | aplicado bien | main.tex:119. |
| m7 "data-set/edge cells" | aplicado bien | main.tex:270. |
| m8 leyenda de la Fig. 2 | aplicado bien (código) | `experiments/run_comparison.py:478–479`; `figures/fig_paired.pdf` regenerada a las 10:06. No inspeccioné la figura visualmente. |
| m9 kNN-SVM en el resumen | aplicado bien | main.tex:53. |
| m10 anotación de la tolerancia | aplicado bien | PREREGISTRO:48. |
| Bibliografía (zhang2004, stone1977, cheng2007) | aplicado bien | refs.bib:75 y :102 (DOI); refs.bib:37–42 sin páginas. |

Total: 16 bien, 1 a medias (M7), 0 sin aplicar, 0 con error nuevo.

## 2. Hallazgos nuevos

### Bloqueantes

Ninguno.

### Mayores

**M1. El resumen y la tabla de afirmaciones dicen que ninguna familia cumple el criterio; la Tabla 5 y §5.3 dicen que una lo cumple "por la letra".** (Viene de v0.2/v0.3; las rondas 1–2 no lo vieron.)
- Ubicación: main.tex:53 ("No family met it"), main.tex:336 ("No family meets the criterion"), frente a `manuscript/table_criterion.tex` (VB-RBF-SVM: "named regime (B): linear; added value: **yes (by the letter; see text)**") y main.tex:309 ("The regime clause (B) is met, by the letter, by \NFamiliesAddedValue{} family", `\NFamiliesAddedValue`=1).
- Problema: el titular negativo contradice la tabla del propio criterio. El texto de §5.3 explica bien por qué no se lee como valor añadido, pero el resumen no puede decir lo contrario de la Tabla 5. README:33 y FICHA:13 dicen "criterio de **mayoría**", que es correcto.
- Corrección (resumen): "No family met its majority clause; the regime clause is met, by the letter, only by VB-RBF-SVM in the one-data-set linear regime, where Section 3 shows that no gain is possible, and we read this as a flaw of the criterion, not as added value: of …". Fila de main.tex:336: "No family meets the majority clause; the regime clause is met by the letter by VB-RBF-SVM in a one-data-set regime (a flaw of the criterion); the single interval above zero is …".

**M2. La Obs. 3.13 y la fila 4 de la tabla llaman "verified numerically" a la inflación 1/(ρv), y los datos no lo sostienen para ρ=¼.**
- Ubicación: main.tex:214 (status "heuristic, not proved; verified numerically"), main.tex:335 ("inflation 1/(ρv) for k=ρn … verified, not proved; 1/(ρv) heuristic"), README:31 ("comprobada numéricamente"), README:42 (solo cita ρ=½).
- Evidencia (`theory/check_knn_localisation_output.txt`, bloque P4): μ=0.5, ρ=¼: cociente 88.4±4.0, 88.4±4.5, **83.9±4.5** a n=2 000, 8 000, 32 000 frente a Q=94.4 (z=−2.3 a n=32 000 y sin acercarse); μ=1.645, ρ=¼: 210±19 → 65±16 → 19.1±1.1 frente a 20.3 (coincide solo en el último n). Solo ρ=½ es compatible (z=+1.5 y +1.0). El texto de la observación da estas cifras con honestidad; la etiqueta no.
- Corrección: status "heuristic, not proved; supported numerically at ρ=½, within about 10 % at ρ=¼ and n=32 000"; fila 4: "… inflation ≈1/(ρv) for k=ρn (heuristic; at n=32 000 the simulated ratios are within 10 % of it, 2.3 SE below for ρ=¼, μ=0.5)"; README:31 "apoyada numéricamente para ρ=½ y aproximada (≈10 %) para ρ=¼"; README:42 añadir "84 ± 5 frente a 94.4 (ρ=¼, μ=0.5)".

**M3. Extensión: 16 páginas frente a ≤ 14.** La teoría v0.4 añade ~4 páginas (pp. 5–7 del cuerpo y el Apéndice C, pp. 14–15). Recortes concretos (estimación ≈ 2 pp.):
1. Enunciar la Prop. 3.6 antes y dejar la Prop. 3.2 como corolario con prueba de 3 líneas (K│Z=j ~ Bin(n,p_j) y la estrictez): se elimina el argumento de condicionamiento duplicado (main.tex:115–124 frente a 158–167). ≈ 0.3 p.
2. Mover el enunciado del Lema 3.8 al Apéndice C (solo se usa en la prueba del Teorema 3.11(i) y en la Obs. 3.13); dejar una frase en §3. ≈ 0.2 p.
3. Mover la prueba del Lema 3.9 y el párrafo "So the kNN-localised…" (main.tex:185–188) al Apéndice C. ≈ 0.15 p.
4. Cor. 3.7: dejar la identidad y los tres cocientes; la frase de Monte Carlo (`\KLSel…`) al Apéndice B. ≈ 0.1 p.
5. Cor. 3.12: dejar enunciado y límites; la frase de simulaciones (D5–D6, comprobación de mayoría, riesgo a n=2000) al Apéndice B. ≈ 0.25 p.
6. Obs. 3.13: dejar la heurística y Q(ρ) en 4–5 líneas; los cocientes simulados al Apéndice B (D7). ≈ 0.2 p.
7. §5.1, celda gaussiana (main.tex:272, la cadena `\GaussVbOwnFolds` … `\GaussSelLinLossFolds`): dejar "3 test points out of 800; the fold-by-fold account is in results/tables.md". ≈ 0.25 p.
8. Intro, "Scope" (main.tex:62) y fecha del título (main.tex:46): quitar la historia v0.2/v0.3/v0.4 (está en el README). ≈ 0.15 p.
9. Resumen: quitar el detalle de saturación multiescala (≈ 50 palabras). ≈ 0.1 p.
10. Limitations: quitar la repetición del alcance v0.4 (ya está en Scope y en la tabla). ≈ 0.1 p.
11. Solo si aún pasa de 14: Tabla 3 (saturación) a `results/tables.md`, manteniendo en el texto los recuentos que sostienen "grid-limited". ≈ 0.4 p.

### Menores

**m1.** Prop. 3.6 (main.tex:158–163), hipótesis implícitas: (a) medibilidad conjunta de (S,x)↦A(S)(x); (b) si A es aleatorizado, su aleatoriedad debe ser independiente de todo y estar dentro de R_A, no en U; (c) "in any metric" sobre un espacio medible arbitrario no garantiza que la selección kNN sea medible: escribir "in any measurable metric (e.g. a norm on R^p)"; (d) aquí P es la ley de (X,Y) sin W, no la del vector completo de entrada de §2: decirlo ("R_A is the learning curve under the law P of (X,Y)").

**m2.** Lema 3.10 y Teorema 3.11(ii) tratan minimizadores exactos; libsvm devuelve uno aproximado (tol=1e−3) y el código predice −1 con valor de decisión exactamente 0 (`families.py:118`). Añadir: "the simulations use libsvm with its default tolerance; Lemma 3.10 concerns exact minimisers". Además r₀ es holgado (primer contraejemplo a ≈ 3–7·r₀ para k=3, 6–14·r₀ para k=5, 12–26·r₀ para k=9; §0.2.3), así que la comprobación "6 646 mixed queries with radius below r₀" (main.tex:211) solo explora la zona con holgura; decirlo o quitarla.

**m3.** Lema 3.8 "classical argument" sin cita (main.tex:177). Citar una fuente del argumento de estadísticos de orden condicionados al k-ésimo radio (p. ej. G. Biau y L. Devroye, *Lectures on the Nearest Neighbor Method*, Springer, 2015; comprobar capítulo y lema antes de citar).

**m4.** Obs. 3.13 (main.tex:215): "because v<1 at the values used": v<1 siempre (truncar una normal a un intervalo reduce su varianza). Escribir "because v<1 (truncating a Gaussian to an interval reduces its variance)".

**m5.** Tabla de afirmaciones: ni el Cor. 3.7 ni el Lema 3.8 aparecen por número; añadir "(Cor. 3.7; Lemma 3.8)" en las filas 1 y 3 (main.tex:332, 334). Tras esta ronda, sustituir "not yet checked by an independent referee" por "checked by an internal referee (round 3)" en main.tex:46, 62, 156, 332, 334, 347, 360, README:5,31,42 y FICHA:3,11,13,22,24.

**m6.** Título del Apéndice B (main.tex:355), "Simulations for rules not covered by Proposition 3.2": D4 (celdas independientes de la etiqueta) sí está cubierto por la Prop. 3.2 (lo no demostrado es la monotonía de la curva de la SVM), y D1, D5–D7 lo están en parte por el Teorema 3.11. Retitular "Simulations".

**m7.** `manuscript/knn_numbers.tex` define macros no usadas en main.tex (comprobado): `\KLPtwoMaxZ`, `\KLPtwoMaxDiff` (0.0023, menor que el 0.00235 real: falsa como cota), `\KLPtwoMinGap` (0.024, mayor que el 0.02396 real: falsa como cota), `\KLPtwoDallMin`, `\KLPtwoDallMax`, `\KLLimNc…Hard`. Hoy son inocuas; dejar de emitir las tres primeras o renombrarlas `…Nearest` para que nadie las use como cota.

**m8.** README:42 "Verificación independiente del integrador": quien integró no es independiente; escribir "verificación del integrador".

**m9.** Título del Cor. 3.12 "Fixed k cannot match the global rule": para la kNN-SVM la comparación es con el umbral de centroides global, no con la SVM lineal global (cuya consistencia no se prueba, main.tex:211). Título sugerido: "Fixed k is eventually worse than the global nearest-centroid rule".

**m10.** Teorema 3.11(i): "R_∞(k)→½ as k→∞" sorprenderá al lector (el voto k-NN tiende a R*). Añadir media frase: "with n→∞ first, a mixed neighbourhood shrinks to a point and its threshold falls on either side of the query with probability ½, so the rule degenerates to a coin flip on mixed neighbourhoods; this is an artefact of fixed k, not of k=ρn (Remark 3.13)".

## 3. Lectura fresca (resto del manuscrito)

Aparte de M1, la lectura del resto (§§1–2, 4–6, Apéndices A–B) no encuentra afirmaciones nuevas sin respaldo: los cambios de la ronda 2 están bien integrados y el texto de §5 es coherente con las tablas. El alcance (main.tex:62, 347; FICHA:14, 25) refleja con exactitud lo que cubren la Prop. 3.6 y el Teorema 3.11 (localización a lo largo de coordenadas sin información; límite con k fijo en un modelo gaussiano; k-means o pesos suaves en la coordenada de señal y C elegido por validación no cubiertos).

## 4. Bibliografía

| entrada | estado | corrección |
|---|---|---|
| (entradas nuevas en v0.4) | ninguna: `git diff 2a9ce22 7e03402 -- …/refs.bib` vacío | — |
| cover1967 (uso nuevo: límite del 1-NN E[2η(1−η)]) | metadatos correctos (IEEE Trans. Inf. Theory 13(1):21–27, 1967) y atribución correcta | añadir `doi = {10.1109/TIT.1967.1053964}` |
| devroye1996 (uso nuevo: riesgo asintótico del voto k-NN) | atribución correcta (cap. 5) | opcional: citar el capítulo |
| stone1977 (App. B: consistencia del voto con k→∞, k/n→0) | correcta | — |
| cheng2007 | páginas retiradas; existencia confirmada en ronda 2 | sin cambios |
| (sugerida) Biau–Devroye 2015 | no está en refs.bib | véase m3 |

No hice búsquedas web: no hay entradas nuevas y el presupuesto se dedicó a la verificación matemática.

## 5. Verificación computacional

| qué | tiempo de CPU | resultado |
|---|---|---|
| `exact_ref.py` (cuadratura propia de R_∞, límite del voto, Q(ρ), R_nc exacto) | < 2 s | coincide con todas las macros de forma cerrada (§0.3) |
| `mc_select.py` (Prop. 3.6, 4 selecciones raras + 2 controles, 40 000 réplicas) | 39 s | │z│<1 en las 4; controles z=+26.5 y −67.3 |
| `mc_select_svm.py` (Prop. 3.6 con SVM lineal) | 7 s | z=+0.49 |
| `mc_rinf.py` (Teorema 3.11, n=50 000, m=1,2; k=1,2,3,5; voto; SVC frente a mayoría) | 5 s | todo dentro de 1.9 errores estándar; 1 800/1 800 SVC = mayoría |
| `majority_search.py` (solver exacto, búsqueda adversarial) | ≈ 150 s (detenido al terminar k=9, C=1) | ningún contraejemplo con r<r₀; hueco ≥ 0.95·C |
| `majority_sklearn.py` (libsvm por defecto, d=1,2,5) | 21 s | 0/3 240 violaciones bajo r₀ |
| `make_knn_numbers.py` en una copia | < 1 s | SHA-256 f035b43d… coincide con `results/knn_localisation_results.sha256`; `knn_numbers.tex` regenerado **idéntico** |
| `latexmk -pdf` en una copia | ≈ 5 s | código de salida 0; 0 advertencias en `main.log`; 0 referencias o citas indefinidas; 0 "??" en el texto extraído; **16 páginas** |

**No reproduje `theory/check_knn_localisation.py`** (≈ 128 s): con las comprobaciones propias (≈ 240 s) habría pasado de los 5 min de CPU. En su lugar: el JSON congelado tiene el SHA-256 declarado, las 51+5 macros se rederivan idénticas, todas las cifras de forma cerrada coinciden con mi código y las magnitudes de Monte Carlo (límites a n grande, voto, SVM = mayoría) coinciden con mi simulación independiente. La reproducción bit a bit del Monte Carlo del autor queda pendiente. El README (línea 59) ya avisa de que el script sobrescribe `theory/`.

## 6. Lista final de acciones (por prioridad)

1. Corregir el resumen (main.tex:53) y la fila de main.tex:336 para que digan que ninguna familia cumple la cláusula de mayoría y que la cláusula de régimen la cumple por la letra VB-RBF-SVM en un régimen de un solo conjunto (M1).
2. Cambiar la etiqueta "verified numerically" de la Obs. 3.13 y de la fila 4 de la tabla, y "comprobada numéricamente" en README:31; añadir a README:42 la cifra ρ=¼, μ=0.5 (M2).
3. Recortar a ≤ 14 páginas con los recortes 1–10 de M3 (y el 11 si hace falta), sin quitar ninguna prueba del PDF.
4. Escribir en la Prop. 3.6 las hipótesis implícitas (medibilidad de A, aleatoriedad de A, métrica medible, P = ley de (X,Y)) (m1).
5. Añadir al Lema 3.10 / Cor. 3.12 la frase sobre minimizadores exactos frente a libsvm y sobre la holgura de r₀ (m2).
6. Citar una fuente del Lema 3.8 (m3) y añadir el DOI de cover1967.
7. Corregir "v<1 at the values used" (m4), retitular el Apéndice B (m6), el título del Cor. 3.12 (m9) y añadir la frase sobre R_∞(k)→½ (m10).
8. Completar la tabla de afirmaciones con el Cor. 3.7 y el Lema 3.8 y actualizar en todos los archivos "not yet checked by an independent referee" (m5).
9. Dejar de emitir las macros redondeadas al más cercano que serían falsas como cotas (m7); cambiar "independiente" en README:42 (m8).
10. Cuando haya presupuesto, ejecutar `theory/check_knn_localisation.py` en una copia y comparar el JSON byte a byte con el congelado.
