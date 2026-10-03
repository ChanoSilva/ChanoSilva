# Informe de árbitro interno — SPD001 (ronda 1, 30/09/2026; emitido 02/10/2026)

Objeto: `papers/SPD001-support-geometry-knn/` (manuscrito v0.1 *Support Geometry and Nearest Neighbours*, README, nota de continuidad, ficha propuesta, código y resultados). Archivos de trabajo del árbitro en el scratchpad `referee_SPD001/` (scripts `check_hknn.py`, `nb_ci.py`, corrida rápida en `repro/`, recompilación en `texcopy/`). No se modificó ningún archivo de la carpeta salvo la creación de este informe.

## Veredicto

**Cambios mayores.** Las matemáticas son correctas, el código no filtra información del pliegue de prueba, todos los números del texto salen del JSON y el veredicto negativo C1 (0 de 8) es sólido; pero la afirmación sobre la *potencia* del resultado negativo ("se excluyen ganancias mayores de ~1 punto") y varios recuentos de significación descansan solo en el bootstrap sobre pliegues dependientes, que el propio manuscrito reconoce anticonservador: con la corrección de Nadeau–Bengio que el texto usa como "lectura cautelosa", la cota pasa de +1.33 a +3.54 puntos y el recuento 7/8 de la ablación ortogonal pasa a 2/8. Esto afecta al resumen, a la tabla de afirmaciones ("verified"), al README, a la nota de continuidad y a la ficha propuesta, y debe corregirse antes de cerrar la línea con ese texto. Además el manuscrito tiene 12 páginas (objetivo ≤ 10).

Recuento: 1 bloqueante, 5 mayores, 15 menores.

---

## Hallazgos bloqueantes

### B1. La cota "ganancias mayores de +1.33 puntos quedan excluidas al 95 %" se presenta como verificada, pero solo vale para el bootstrap anticonservador; con la corrección NB del propio artículo la cota es +3.54

- **Ubicación.** `manuscript/main.tex:58` (resumen: "the largest gain compatible with the data at the 95% level is +1.33 points"); `main.tex:215` ("gains larger than that are excluded at the 95% level everywhere"); `main.tex:320` (Tabla 8, fila "Upper 95% limit … at most +1.33 points on every dataset — verified"); `main.tex:335` (Limitations: "power to exclude gains of about one point"); `README.md:37` ("ganancias mayores quedan excluidas"); `CONTINUIDAD_SPD001_20260930.md:35` ("El estudio excluye ganancias mayores de ~1 punto"); `FICHA_SPD001_propuesta.md:14` y `:25` ("excluye ganancias mayores de ~1 punto, no menores").
- **Problema.** El límite superior +1.33 es el máximo de los límites superiores del IC bootstrap percentil sobre 25 pliegues de CV repetida 5×5. Esos pliegues comparten datos (cada punto está en 5 pliegues de prueba y en 20 de entrenamiento); el manuscrito lo reconoce (`main.tex:170`, `:335`) y por eso añade el test t corregido de Nadeau–Bengio. Pero la afirmación de potencia, que es la que da valor al resultado negativo, se formula únicamente con el bootstrap y se etiqueta "verified".
- **Evidencia (calculada a partir de `results/results.json`, mismas 25 diferencias por pliegue, IC = media ± t₀.₉₇₅,₂₄·√((1/25+1/4)·s²), es decir, el mismo factor de inflación que el test NB del artículo):**

  | conjunto | TOD − mejor ref., bootstrap | IC con varianza NB |
  |---|---|---|
  | iris | −0.27 [−1.20, +0.67] | [−2.87, +2.34] |
  | wine | +0.10 [−1.03, +1.33] | [−3.33, +3.54] |
  | breast cancer | −0.25 [−0.70, +0.21] | [−1.56, +1.06] |
  | digits | −0.34 [−0.64, −0.06] | [−1.18, +0.50] |
  | swiss roll | −0.20 [−0.60, +0.17] | [−1.34, +0.94] |
  | moons | −0.77 [−1.27, −0.27] | [−2.23, +0.70] |
  | moons+10 ruido | −0.37 [−1.30, +0.57] | [−3.03, +2.29] |
  | spheres | +0.23 [−0.53, +0.97] | [−1.91, +2.38] |

  Máximo límite superior: **+1.33 (bootstrap) frente a +3.54 (NB)**. La corrección NB es conocida por ser conservadora, así que la verdad está entre ambas; pero el texto solo cita el extremo favorable.
- **Corrección propuesta.**
  1. `main.tex:58`: sustituir "and the largest gain compatible with the data at the 95% level is \CiHiBestMax{} points" por "the largest bootstrap upper limit over datasets is \CiHiBestMax{} points (\CiHiBestMaxNb{} points with the Nadeau–Bengio variance), so the study excludes gains of a few points, not of one".
  2. `main.tex:215`: tras "The largest upper interval limit … is \CiHiBestMax{} points" añadir "with the bootstrap, and \CiHiBestMaxNb{} points with the Nadeau–Bengio variance; gains larger than the latter are excluded under the cautious reading, gains between the two are not".
  3. `main.tex:320`: "Upper 95% limit of the gain over the best reference is at most \CiHiBestMax{} (bootstrap) / \CiHiBestMaxNb{} (NB) points — verified".
  4. `make_numbers.py`: añadir macros `CiHiBestMaxNb` y, por conjunto, `NbLoBest<tag>`, `NbHiBest<tag>` (fórmula arriba; `paired_stats` ya calcula `var` y `J`; basta añadir `nb_lo`, `nb_hi` en `support_geometry.py:403`). Incluir una columna "NB 95% CI" en la Tabla 2 en lugar de solo "NB p".
  5. README:37, CONTINUIDAD:35, FICHA:14 y :25: "excluye ganancias de más de ~1 punto con el bootstrap sobre pliegues y de más de ~3.5 puntos con la corrección de Nadeau–Bengio; no excluye ganancias menores".

---

## Hallazgos mayores

### M1. Todos los recuentos de significación (C2, pérdidas de C1, C3, E2) son solo bootstrap; bajo la lectura NB cambian de forma sustancial y el texto no lo dice donde los usa

- **Ubicación.** `main.tex:58` (resumen: "interval above zero on 7 of 8 datasets"); `main.tex:211` (pie Tabla 2: "significant losses: 2"); `main.tex:254` (C2); `main.tex:282` (C3: "above zero on 1 dataset (digits)"); `main.tex:304` y `:323` (E2, p = 2); `main.tex:321` (Tabla 8, C2 "verified"); `README.md:39`; `CONTINUIDAD:28`.
- **Evidencia (mismo cálculo que B1).** TOD − TD (ortogonal): bootstrap 7/8 por encima de 0; NB **2/8** (digits [+3.01, +7.19], spheres [+0.01, +7.05]). TOD − SD: 6/8 → 2/8. TOD − kNN: 2/8 → 0/8. TOD − LPH: 1/8 → 0/8. Pérdidas C1 (digits, moons): 2 → 0 (ya dicho en el texto vía p). E2 p = 2, TOD − TO = +0.90 [+0.33, +1.50] bootstrap; NB [−0.79, +2.59], p = 0.28; es 1 de 13 intervalos de la contribución de la profundidad en todo el estudio (8 + 5), compatible con el azar incluso sin la dependencia entre pliegues. C3 digits +0.20 [+0.05, +0.35]: NB [−0.24, +0.64].
- **Problema.** La atribución de C2 ("la información está en la componente ortogonal") sigue siendo defendible por el tamaño de los efectos (+5.1 puntos en digits, +3.5 en spheres, +2.7 en moons+ruido) y por los pesos ajustados, pero no por "7 de 8 intervalos sobre cero". El resumen, la Tabla 8 y la nota de continuidad presentan los recuentos bootstrap sin calificativo.
- **Corrección.** En cada recuento, dar la pareja "(bootstrap n/8; NB m/8)" o, si se prefiere una sola cifra, usar la NB y comentar la bootstrap. Reescribir el resumen: "removing the orthogonal component costs between +0.7 and +5.1 points (bootstrap interval above zero on 7 of 8 datasets, Nadeau–Bengio interval on 2)". En la Tabla 8 cambiar la fila C2 a "the orthogonal component carries the information: effect +0.7 to +5.1 points (7/8 bootstrap, 2/8 NB)". En E2 (`main.tex:304`) añadir "(NB p = 0.28; one of 13 depth intervals in the study)".

### M2. Los hiperparámetros siguen en el borde superior de las rejillas en moons y moons+ruido después de la ampliación; la "Note on the grids" da a entender que el problema quedó resuelto

- **Ubicación.** `main.tex:174`; `support_geometry.py:66-69` (rejillas); Tabla 5.
- **Evidencia (fracción de los 25 pliegues en que el valor elegido es el máximo de la rejilla, `results.json`):** moons: TOD k = 30 en 56 %, HKNN k = 30 en 68 %, kNN k = 41 en 36 %, λ_rel = 100 en 20 %; moons+10 ruido: TOD k = 30 en **84 %**, HKNN k = 30 en **96 %**, λ_rel = 100 en 56 %, kNN k = 41 en 60 %. En los otros seis conjuntos la fracción es ≤ 52 % (HKNN en iris y wine) y en general baja.
- **Problema.** Moons es precisamente el conjunto con la mayor pérdida de TOD (−0.77) y uno de los dos con IC bootstrap < 0. Como TOD y HKNN están ambos en el borde, la comparación no está claramente sesgada, pero la afirmación implícita de que las rejillas ya son suficientes no se sostiene y el lector no puede saberlo desde el texto.
- **Corrección.** O bien (a) ampliar una vez más para esos dos conjuntos (K_GRID → {5,10,20,30,50}, KNN_GRID hasta 61, LAMBDA_GRID hasta 1000; moons tiene 480 puntos de entrenamiento por pliegue, 240 por clase, así que k = 50 es viable) y volver a correr todo (≈ 6 min de CPU), o bien (b) dejar las rejillas y escribir en `main.tex:174`: "after widening, the chosen k still sits at the top of the grid in most folds on moons (56–68 %) and moons with noise (84–96 %) for both TOD and HKNN; the comparison is symmetric but the absolute accuracies there may be slightly below their optimum". Añadir a `make_numbers.py` la macro con esas fracciones (ya existe `NLocalKMax` pero sobre la moda, no sobre la fracción).

### M3. Atribución de la forma penalizada a Vincent–Bengio no verificada; y en 3 de 8 conjuntos la "distancia al casco" es idénticamente cero

- **Ubicación.** `main.tex:88-91` (Def. 2.3), `main.tex:129-134` (Prop. 3.2), resumen (`:58`), FICHA:13/24 ("La distancia HKNN regularizada es exactamente…").
- **Verificación hecha.** La identidad h_λ² = O_ρ² + Σ λ t_j²/(s_j²+λ), *para el objetivo tal como lo define la Def. 2.3*, es correcta: comprobada paso a paso (descomposición α = Wβ + γ, mínimo por coordenada, valor λ t_j²/(s_j²+λ), términos j > ρ con s_j = 0 que suman O_ρ²) y numéricamente frente a mínimos cuadrados aumentados en 200 vecindades aleatorias × 5 valores de λ (error relativo máximo 7·10⁻¹⁴). Ejemplo explícito: N = {(0,0),(2,0),(0,1),(3,3)}, q = (4,−1), λ = 0.5: μ = (1.25, 1), s = (3.2237, 1.5354), t = (0.6867, −3.3303), O² = 0 (ρ = d = 2); fuerza bruta 1.962349 = fórmula 1.962349. Monotonía en λ comprobada (0 → 0.456 → 3.345 → 9.206 → 11.263 → |r|² = 11.5625).
- **Problema 1 (atribución).** Si el clasificador de Vincent–Bengio usa como puntuación la *distancia pura* ‖r − Vᵀα*‖ en el minimizador penalizado y no el valor del objetivo, la fórmula para *su* clasificador es O_ρ² + Σ λ² t_j²/(s_j²+λ)² (también verificada numéricamente: 0.340579 en el ejemplo). Sigue siendo una combinación ponderada tangencial–ortogonal, así que la Observación 3.3 y las conclusiones no cambian, pero la frase "the regularised local-hyperplane distance of Vincent and Bengio is exactly…" dependería de la definición. La nota de continuidad dice que "se asume que el valor incluye la penalización, como en el artículo". No pude comprobarlo: el proxy de red bloquea proceedings.neurips.cc, papers.nips.cc, semanticscholar, mlanthology y PMC. Mi recuerdo del artículo coincide con el supuesto del autor, pero es un recuerdo.
- **Problema 2 (bajo d).** Con d = 2 (moons, moons_p0) y d = 3 (swiss roll, spheres) y k ≥ d+1 se tiene ρ = d, luego aff N = ℝ^d y h_0 ≡ 0: en esos conjuntos HKNN *es* el término tangencial penalizado (una distancia al centroide anisótropa), y LPH solo existe porque m se restringe a ≤ d−1. Esto refuerza la Observación 3.3 pero no se dice; un lector podría creer que "casco" significa algo en d = 2.
- **Corrección.** (i) En Def. 2.3 escribir "we take as HKNN score the value of the penalised objective (this is how we read Vincent and Bengio, §3; if one takes instead the plain distance at the penalised minimiser, Proposition 3.2 holds with weights λ²/(s_j²+λ)², which does not affect Remark 3.3)". El autor debe cotejar la ecuación de la sección 3 del artículo original y dejar una sola lectura. (ii) Añadir una frase tras la Prop. 3.1 o en la sección 4: "on the three datasets with d ≤ 3 and k > d, ρ = d, the hull distance vanishes identically and HKNN reduces to the penalised tangential term".

### M4. "Criterio fijado antes de las corridas": no hay evidencia independiente, y las rejillas sí se cambiaron tras ver resultados

- **Ubicación.** `main.tex:172` ("Criterion (fixed before the runs)"), `:174`; `README.md:5`; `FICHA:12` ("con un criterio fijado de antemano"); `CONTINUIDAD` §Decisiones.
- **Evidencia.** No existe prerregistro con marca temporal ni hash. Las marcas de tiempo del sistema de archivos son coherentes con el relato: `tables_run1_narrow_grids.md` 08:33:26 → `support_geometry.py` modificado 08:35:05 → `results.json` 08:40:17 (311 s después, igual a los 310 s de pared registrados). Pero el script se editó entre las dos corridas, así que no se puede separar "cambio de rejillas" de cualquier otro cambio; el criterio (`support_geometry.py:465`, `needed = n_ds // 2 + 1`, IC bootstrap > 0) solo está atestiguado por la palabra del autor. La corrida 1 produjo el mismo veredicto, lo que da verosimilitud, pero también muestra que el protocolo se tocó después de ver resultados (ampliación de rejillas, decisión razonable y divulgada).
- **Corrección.** En `main.tex:172` sustituir "(fixed before the runs)" por "(fixed before the runs; no time-stamped preregistration exists, the only record is the code constant and the two complete runs kept in `results/`)". Para futuras líneas: guardar un archivo `PREREGISTRO_<CODIGO>.md` con hash y fecha antes de la primera corrida completa.

### M5. Extensión: 12 páginas frente al objetivo ≤ 10, con dos tablas ilegibles por `\resizebox`

- **Ubicación.** `main.tex:217-229` (Tabla 3) y `:233-245` (Tabla 4), ambas `\footnotesize` + `\resizebox{\linewidth}`; Tablas 5, 6, 7 y 8.
- **Evidencia.** `pdfinfo`: 12 páginas; recompilación en scratch: 0 cajas desbordadas, sin avisos. Las Tablas 3 y 4 quedan a ~6 pt tras el escalado (ver `p-07.png`).
- **Corrección.** Ver la sección "Recortes" al final; con esos recortes se llega a 9–10 páginas sin perder ningún número verificable (todo queda en `results/tables.md` o en apéndice).

---

## Hallazgos menores

- **m1. Prop. 3.5 (`main.tex:155-160`): el contraejemplo es degenerado.** En d = 1 se tiene O₁ ≡ 0, así que solo muestra que D no es función de T. Es lógicamente suficiente, pero conviene un ejemplo con O > 0. Uno verificado: N = {(−1, 0.3), (0, −0.4), (3, 0.1)} en ℝ² (k = 3, μ = (2/3, 0), covarianza diagonal, u₁ = e_x, u₂ = e_y, s = (2.944, 0.510)), m = 1; q₁ = (8/3, 1/2) y q₂ = (−4/3, 1/2) tienen T₁ = 2, O₁ = 0.5 y D(q₁) = 0.4216, D(q₂) = 0.0251. Sustituir o añadir.
- **m2. `main.tex:103`: "The spatial depth equals 1 exactly at the spatial median".** Con la convención S(0) = 0, si la mediana espacial es uno de los vecinos x_i, D(x_i) = 1 − ‖(1/k)Σ_{j≠i} S(x_j − x_i)‖ puede ser < 1 (la condición de mediana en un dato es ‖Σ_{j≠i} S‖ ≤ 1, no = 0). Escribir "equals 1 at the spatial median when the median is not a neighbour". La unicidad "when the neighbours are not collinear" es correcta (Milasevic–Ducharme 1987); citar si se quiere fuente primaria.
- **m3. `main.tex:215`: "The best reference was a hull method (HKNN, LPH or NFL)".** NFL no es un método de casco; decir "a local-support method (hull or feature line)". Lo mismo en README:37 si se reproduce.
- **m4. C3 (`main.tex:282`, Tabla 6): el único IC > 0 (digits, +0.20) depende de comparar con la mejor referencia *por exactitud*.** Con la mejor referencia por exactitud selectiva (ya calculada en `results.json`, campo `sel_vs_best_by_sel`: LCD en digits) la diferencia es +0.07 [−0.12, +0.27]; en moons pasa a −3.21 [−3.79, −2.62]. Reportar `sel_vs_best_by_sel` (es la comparación natural para C3) o decir que el "1 por encima de 0" desaparece con ella. La conclusión negativa de C3 se refuerza.
- **m5. Multiplicidad del hallazgo p = 2 (`main.tex:304`, `:323`, `:333`).** Ya tratado con cautela, pero añadir que es 1 de 13 intervalos de la profundidad y que su p NB es 0.28 (ver M1).
- **m6. Resolución de la exactitud por pliegue (`main.tex:215`, "within one point on 8 of 8").** Un error de prueba vale 3.33 puntos en iris (n_test = 30) y 2.78 en wine (36); allí "dentro de un punto" está por debajo de la resolución de un pliegue y 16 de 25 pliegues son empates exactos (Tabla 2, W/L/T 4/5/16). Mencionarlo en Limitations.
- **m7. `support_geometry.py:457-458`, `params_mode`: `max(set(ps), key=ps.count)` no es determinista en empates** (el orden de un `set` de cadenas depende de `PYTHONHASHSEED`; comprobado: 4 resultados distintos en 30 semillas de hash con un empate a cuatro). Afecta solo a la Tabla 5. Cambiar a `max(sorted(set(ps)), key=ps.count)` o a `collections.Counter(ps).most_common(1)` tras ordenar.
- **m8. Def. 2.1 (`main.tex:76`): "ties broken by index" no está garantizado por el código** (`support_geometry.py:160-163`: `argpartition` seguido de `argsort` estable sobre el bloque parcial, cuyo orden interno no es el de índice). Iris tiene exactamente 1 fila duplicada; efecto nulo en la práctica. Reescribir "ties broken deterministically" o usar `np.lexsort((idx, D))`.
- **m9. `main.tex:168`: "Every hyper-parameter is chosen on the training fold by leave-one-out accuracy".** Para los modelos logit, (k, m) se elige por la exactitud de *resustitución* de un logit ajustado sobre rasgos leave-one-out (`support_geometry.py:369-377`: el mismo `Fz` se usa para ajustar w y para medir `acc`); los pesos ven el punto. Está reconocido en Limitations (`:335`) pero debe decirse en el párrafo de Evaluación. El optimismo medido (LOO − test) es similar para TOD y HKNN (p. ej. wine 2.0 vs 2.1 puntos), así que no sesga la comparación.
- **m10. Bibliografía.** (a) `refs.bib:39-44` cevikalp2008: añadir `pages = {120--127}`, `address = {Helsinki}`, `publisher = {Omnipress}` (editores Cohen, McCallum, Roweis). (b) Cinco entradas no citadas (breunig2000, demsar2006, kambhatlaleen1997, roweissaul2000, zhangzha2004): eliminarlas o citarlas; Demšar 2006 encaja en el párrafo de Statistics (comparación sobre varios conjuntos). (c) Añadir Bouckaert & Frank (2004, PAKDD, LNAI 3056, 3–12), que es la referencia estándar para aplicar la corrección NB a k-fold repetida (NB la derivaron para submuestreo aleatorio). (d) `uci`: la forma actual recomendada por el repositorio es Kelly, Longjohn & Nottingham (2023); o citar directamente el conjunto wine (Aeberhard & Forina). (e) Añadir `doi = {10.2307/1403797}` a fixhodges1989. Tabla completa más abajo.
- **m11. `main.tex:335`: "for four of them, close to the accuracy ceiling".** Son cinco con exactitud ≥ 96 % (iris, wine, breast cancer, digits, swiss roll).
- **m12. FICHA:13/24: "no superó a la mejor referencia en ningún conjunto".** La media de TOD es superior en wine (+0.10) y spheres (+0.23); escribir "no la superó de forma significativa en ninguno (diferencias entre −0.8 y +0.2 puntos)". Y la frase de alcance (FICHA:14/25) según B1.
- **m13. Tabla 8 (`main.tex:308-331`)** repite el texto; tras los recortes, reducirla a las seis filas no triviales (C1, cota, C2, C3, E2, "not established") o moverla al apéndice.
- **m14. Notación.** `k` denota a la vez el tamaño de la vecindad de clase y el `k` de kNN (Tabla 5 los distingue por columna, el texto no siempre). Sugerencia: `k_{\rm NN}` para kNN. El símbolo `W` se usa para la matriz de vectores singulares izquierdos (Def. 2.1) y `W/L/T` en la Tabla 2; inocuo.
- **m15. README:14 "12 páginas" y `main.tex:51` `\today`.** Tras los recortes, actualizar el README; fijar la fecha en lugar de `\today` para que el PDF sea reproducible byte a byte.

Lo que está bien (una línea cada uno): Prop. 3.1, 3.2, 3.4 y 3.5 correctas tal como están enunciadas; `numbers.tex` y las 7 tablas se regeneran idénticos desde `results/*.json`; no hay fuga de información del pliegue de prueba en `run_fold` (estandarización, selección LOO, escala de HKNN, estandarización de rasgos del logit y pesos: todo del pliegue de entrenamiento); gradiente del logit correcto por inspección; fórmula NFL correcta (a² − (a·b)²/|b|²); fórmula del t corregido correcta; el código corre en modo rápido y en completo con semilla fija.

---

## Bibliografía

Red: `api.crossref.org` (403 del proxy), `proceedings.neurips.cc`, `papers.nips.cc`, `icml.cc`, `api.semanticscholar.org`, `mlanthology.org` y `pmc.ncbi.nlm.nih.gov` bloqueados. Solo fue posible usar búsqueda web (resúmenes con enlace a JSTOR, Springer, T&F, PNAS). "Verificada (web)" = campos coincidentes con la página de la editorial o JSTOR según el resultado de búsqueda; "no verificable" = sin acceso; "coincide" = coincide con mi conocimiento sin discrepancias detectadas.

| Entrada | Estado | Corrección / nota |
|---|---|---|
| vincentbengio2002 | verificada parcialmente (web): autores, título, NIPS 14, 2002; páginas 985–992 solo por resumen de búsqueda | mantener; cotejar páginas y la definición de la distancia penalizada (M3) en el PDF original |
| fixhodges1989 | verificada (web, JSTOR): ISR 57(3), dic. 1989, 238–247 | añadir `doi = {10.2307/1403797}` |
| cevikalp2008 | **corregida** (web): ICML 2008, Helsinki, pp. 120–127 | añadir `pages = {120--127}`, `address = {Helsinki}`, `publisher = {Omnipress}` |
| serfling2002 | verificada (web, Springer cap. DOI 10.1007/978-3-0348-8201-9_3): Dodge (ed.), Birkhäuser, Basel, 25–38 | opcional: añadir `series = {Statistics for Industry and Technology}` |
| lilu1999 | verificada (web): IEEE TNN 10(2), 439–443, 1999 | — |
| vardizhang2000 | verificada (web, PNAS): 97(4), 1423–1426 | opcional DOI 10.1073/pnas.97.4.1423 |
| paindaveinevanbever2013 | verificada (web, T&F): JASA 108(503), 1105–1119 | opcional DOI 10.1080/01621459.2013.813390 |
| coverhart1967, hastietibshirani1996, tukey1975, liu1990, zuoserfling2000, chaudhuri1996, ghoshchaudhuri2005, licuestaliu2012, chow1970, dietterich1998, nadeaubengio2003, efrontibshirani1993, pedregosa2011, harris2020, virtanen2020, fisher1936, street1993 | no verificables en red; coinciden | — |
| uci | no verificable; forma habitual pero desactualizada | sustituir por Kelly, Longjohn & Nottingham (2023), *The UCI Machine Learning Repository*, https://archive.ics.uci.edu, o citar Aeberhard & Forina (1991) |
| breunig2000, demsar2006, kambhatlaleen1997, roweissaul2000, zhangzha2004 | en `refs.bib`, **no citadas** | eliminar, o citar demsar2006 en Statistics |
| (falta) Bouckaert & Frank 2004 | — | añadir y citar junto a nadeaubengio2003 en `main.tex:170` |

Resumen: 7 verificadas (1 parcial), 1 corregida, 17 no verificables (coinciden), 1 desactualizada, 5 no citadas, 1 ausente recomendada. Soporte de cada cita a su afirmación: correcto en todos los casos revisados; la única atribución sustantiva en duda es la de M3.

---

## Verificación computacional

| Qué | Resultado |
|---|---|
| Regenerar `numbers.tex` y `table_*.tex` desde `results/*.json` con `make_numbers.py` en scratch | **idénticos** a los del manuscrito (750 macros, 7 tablas); muestreo manual de ~40 cifras del texto, README y FICHA frente al JSON: sin discrepancias |
| Prop. 3.2 (forma cerrada HKNN) frente a mínimos cuadrados aumentados | 200 vecindades × 5 λ: error relativo máx. 7.4·10⁻¹⁴; ejemplo explícito en M3; hull `lstsq` = O_ρ² |
| Prop. 3.5 (ejemplo d = 1) | reproducido: D(8/3) = 2/3, D(−4/3) = 0; D(1) = D(5/3) = 2/3 con T = 1/3 y 1 |
| Corrida rápida `--fast` (3×1 pliegues, digits 50/clase, 1000 remuestreos), copia del script en scratch | **31 s de pared / 26 s de CPU** (4 núcleos, BLAS de 1 hilo). Veredicto 0/8 victorias, 0 pérdidas significativas. TOD − mejor ref.: iris −1.33, wine −1.69, bc −0.35, digits 0.00, swiss +0.17, moons −0.83, moons+ruido −0.67, spheres +0.50 (corrida completa: −0.27, +0.10, −0.25, −0.34, −0.20, −0.77, −0.37, +0.23). Mismo orden de magnitud; signo coincidente en 5/8; la mejor referencia cambia en 4/8 (3 pliegues es poco). Coincide en lo esencial |
| Recompilación `pdflatex` ×2 con el `.bbl` existente | 12 páginas, 0 `Overfull`, sin avisos de referencias |
| IC con varianza NB a partir de las 25 diferencias por pliegue | tabla en B1; recuentos en M1 |
| Fracción de pliegues con hiperparámetro en el borde de la rejilla | M2 |
| No determinismo de `params_mode` | 30 semillas de hash, empate a cuatro: 4 resultados distintos |
| Marcas de tiempo de archivos | coherentes con dos corridas y edición intermedia del script (M4) |
| Duplicados en datos | iris: 1 fila duplicada; digits (1797): 0 |

CPU total gastada por el árbitro: ≈ 45 s.

---

## Recortes propuestos para llegar a ≤ 10 páginas

1. **Resumen (`main.tex:58`)**: de ~330 a ~180 palabras; quitar la enumeración de referencias y la lista de rangos de las ablaciones (dejar C1, la cota con ambas lecturas y una frase de C2). Ahorro: ⅓ página.
2. **Tabla 3 (vs cada referencia)**: eliminar; mover la columna "vs HKNN" a la Tabla 2 (nueva columna "TOD − HKNN [CI]") y dejar el resto en `results/tables.md` / apéndice. La Figura 2 y la Tabla 4 (que ya contiene vs LPH y vs SD) cubren lo demás. Ahorro: ½ página.
3. **Tabla 5 (hiperparámetros y pesos)**: al apéndice; en el texto de C2 basta el rango de los pesos (ya está). Ahorro: ⅓ página.
4. **Tabla 6 (selectiva)**: al apéndice, dejando el párrafo C3 con una frase y la columna `sel_vs_best_by_sel`. Ahorro: ⅓ página.
5. **Tabla 7 (régimen)**: al apéndice; la Figura 3 más dos frases bastan (añadir a la figura una banda o marcador del mejor método por p). Ahorro: ¼ página.
6. **Tabla 8 (afirmaciones)**: reducir a 6 filas (C1, cota, C2, C3, E2, no establecido); las filas "proved here" ya están etiquetadas junto a cada proposición (`main.tex:162`). Ahorro: ⅓ página.
7. **Fusionar** los párrafos "Against each reference" y "C2" (`main.tex:231` y `:254`): el primero termina con la familia de cascos y el segundo con los pesos; una sola sección "Where the information is" de ~15 líneas. Ahorro: ¼ página.
8. **Apéndice A, párrafo "Computation"**: reducir a tres líneas (lo demás está en el docstring del script). Ahorro: ⅙ página.
9. **Figura 1**: `width=0.7\linewidth`. Ahorro: ⅙ página.

Total estimado: 2.5–3 páginas → 9–9.5 páginas con bibliografía.

---

## Lista de acciones (por prioridad, imperativo)

1. Añade a `paired_stats` (`support_geometry.py:403`) los límites `nb_lo`, `nb_hi` = media ± t₀.₉₇₅,J−1·√((1/J+1/4)·var) y regenera `results.json` (o calcúlalos en `make_numbers.py` desde las listas `acc` por pliegue, sin recorrer); crea las macros `CiHiBestMaxNb`, `NbLoBest<tag>`, `NbHiBest<tag>` y la columna "NB 95% CI" en la Tabla 2.
2. Reescribe la cota de potencia en `main.tex:58`, `:215`, `:320`, `:335`, `README.md:37`, `CONTINUIDAD:35`, `FICHA:14` y `:25` como "+1.33 puntos con bootstrap, +3.54 con la varianza de Nadeau–Bengio" (B1).
3. Da cada recuento de significación como pareja bootstrap/NB en `main.tex:58`, `:211`, `:254`, `:282`, `:304`, `:321-323`, `README.md:39`, `CONTINUIDAD:28` (M1); en E2 añade "NB p = 0.28, 1 de 13 intervalos".
4. Decide sobre las rejillas en moons y moons+ruido: amplía (K_GRID hasta 50, KNN_GRID hasta 61, λ_rel hasta 1000) y vuelve a correr, o declara en `main.tex:174` las fracciones de pliegues en el borde (M2).
5. Coteja en Vincent–Bengio (§3) si la puntuación penalizada es el valor del objetivo o la distancia pura; escribe la lectura adoptada en la Def. 2.3 con la fórmula alternativa en una frase (M3); añade la observación de que h₀ ≡ 0 cuando ρ = d (3 de 8 conjuntos).
6. Sustituye "(fixed before the runs)" en `main.tex:172` por la formulación con la ausencia de prerregistro (M4) y refleja lo mismo en `FICHA:12` ("criterio fijado de antemano y documentado en el código").
7. Aplica los recortes 1–9 y comprueba `pdfinfo main.pdf | grep Pages` ≤ 10; actualiza `README.md:14`.
8. Sustituye el ejemplo de la Prop. 3.5 por el bidimensional de m1 (o añádelo).
9. Corrige `main.tex:103` ("equals 1 at the spatial median when the median is not a neighbour").
10. Reporta en C3 la comparación con la mejor referencia por exactitud selectiva (`sel_vs_best_by_sel`) y ajusta el texto de `main.tex:282`.
11. Cambia "hull method (HKNN, LPH or NFL)" por "local-support method" en `main.tex:215`.
12. Escribe en `main.tex:168` que para los modelos logit la selección de (k, m) usa la exactitud de resustitución del logit ajustado sobre rasgos leave-one-out.
13. Añade a Limitations la resolución por pliegue (3.33 puntos en iris, 2.78 en wine) y corrige "four" por "five" en `main.tex:335`.
14. Corrige `params_mode` (`support_geometry.py:458`) con un orden determinista; corrige o reformula "ties broken by index" (`main.tex:76`).
15. Bibliografía: añade páginas a cevikalp2008, DOI a fixhodges1989, Bouckaert & Frank 2004 en `main.tex:170`, actualiza `uci`; elimina o cita las 5 entradas huérfanas.
16. En la FICHA cambia "no superó a la mejor referencia en ningún conjunto" por "no la superó de forma significativa en ninguno" y la frase de alcance según el punto 2.
17. Fija la fecha en `main.tex:51` en lugar de `\today`.
