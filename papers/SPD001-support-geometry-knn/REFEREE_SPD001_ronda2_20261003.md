# Informe de árbitro interno — SPD001, ronda 2 (03/10/2026)

Objeto: `papers/SPD001-support-geometry-knn/` v0.2 (commit a9b26f1): `manuscript/main.tex` (306 líneas, 10 pp.), `numbers.tex`, tablas, `experiments/*.py`, `results/*.json`, README, FICHA, CONTINUIDAD y la respuesta `RESPUESTA_SPD001_ronda1_20260930.md`. Árbitro nuevo, independiente del de la ronda 1. Scripts y salidas auxiliares en el scratchpad `referee2_SPD001/` (`check_nb.py`, `check_ties.py`, `copy/experiments/moons_check.py`, `moons_check2.py`, recompilación en `copy/manuscript/`). No se modificó ningún archivo de la carpeta salvo este informe; git solo en lectura.

## Veredicto

**Cambios mayores.** El veredicto primario C1 (0 de 8) es sólido, reproducible y está bien comunicado, y las macros de Nadeau–Bengio son correctas; pero la decisión de no ampliar las rejillas se apoya en una estimación de coste que no corresponde (los dos conjuntos afectados cuestan 16 s de CPU) y la ampliación, que corrí en 51 s, elimina uno de los tres efectos con que se sostiene la atribución C2 (TOD − TD en moons+ruido pasa de +2.7 a +0.5 / −0.3 puntos); además la nueva Observación 3.2 está mal contada (omite iris) y oculta que, con el k elegido, HKNN no tiene término de casco en 5 de 8 conjuntos, y la "mejor referencia" de moons es un empate exacto a tres resuelto por redondeo de coma flotante.

Recuento: 0 bloqueantes, 3 mayores, 11 menores. Ronda 1: 18 bien aplicados, 2 a medias, 1 aplicado con error nuevo, 0 no aplicados.

---

## Verificación de la ronda 1

| Id | Estado | Evidencia |
|---|---|---|
| B1 (cota +1.33 solo bootstrap) | aplicado bien | Pareja +1.3 / +3.5 en resumen (`main.tex:59`), C1 (`:220`), tabla de afirmaciones (`:266`, `:271`), Limitaciones (`:280`), columna "NB CI" en Tabla 2 (`:211`); README:39 (+1.33/+3.54), FICHA:14/25, CONTINUIDAD:26/35. Macros `CiHiBestMaxNb`=+3.5, `CiHiBestMaxNbTwo`=+3.54, arg = wine: recalculadas por mí desde las 25 diferencias por pliegue con media ± t₀.₉₇₅,₂₄·√((1/25+1/4)·s²): coinciden en los 8 conjuntos a 2 decimales. `make_numbers.py:63-71` usa 1/J + 1/(K−1) con K = 5, es decir 1/25 + 1/4, y `student_t.ppf(0.975, J−1)`: fórmula correcta. Los `nb_p` del JSON son coherentes con los IC NB en las 9 comparaciones × 8 conjuntos (p < 0.05 ⇔ IC excluye 0). |
| M1 (recuentos solo bootstrap) | aplicado bien | Pareja boot/NB en `:59`, `:216`, `:242-244`, `:246`, `:255`, `:265-269`, README:41-43, CONTINUIDAD:26-30. Recuentos NB recalculados: TD 2/8 (digits, esferas), SD 2/8, kNN 0, LPH 0, HKNN 0, pérdidas C1 0, C3 0/0, E2 0/0 y p = 0.282 en p = 2: todos coinciden. Defecto residual en el "1 of 13" (ver m1). |
| M2 (rejillas en el borde) | **aplicado a medias** | Fracciones declaradas en `:179`, `:280`, Tabla 5 (`:293`) y README:44, con valores correctos para TOD/HKNN/kNN/λ. Pero (i) omiten los métodos más afectados (ablación TD, SD) y todo E2; (ii) la justificación de no ampliar (≈ 9 min de CPU, k = 50 inviable en iris/wine) se refiere a recorrer los 8 conjuntos, cuando el problema está en dos que cuestan 4.3 s y 11.7 s; (iii) la frase "the comparison is symmetric" es falsa para las ablaciones: al ampliar, el efecto C2 en moons+ruido desaparece. Detalle en M1 nuevo. |
| M3 (lectura V–B; h₀ ≡ 0) | **aplicado con error nuevo** | (i) Lectura única declarada en Def. 2.3 (`:93`) con la fórmula alternativa; los pesos λ²/(s_j²+λ)² son correctos (residuo t_jλ/(s_j²+λ)). La coletilla "nothing else in the paper changes" es excesiva (m5). Cotejo con el original: sigue sin poder hacerse (ver Bibliografía). (ii) La Observación 3.2 (`:130-131`) dice "the 3 datasets with d ≤ 3"; iris (d = 4 < k_min = 5) también cumple ρ = d para todo k de la rejilla; `make_numbers.py:323` usa `d <= 3` en lugar de `d < min(K_GRID)`. Y con el k realmente elegido el fenómeno abarca 5 de 8 conjuntos más el 60 % de los pliegues de wine (M2 nuevo). |
| M4 (prerregistro) | aplicado bien | `:177` ("no time-stamped preregistration…"), `:59` y `:68` ("before the first complete run"), README:5, FICHA:12/23, CONTINUIDAD:12. |
| M5 (extensión) | aplicado bien | Recompilado en copia con `latexmk`: **10 páginas**, 0 errores, 0 `Overfull`, 0 citas/referencias indefinidas, `pdftotext | grep -c "??"` = 0; `.bbl` y texto del PDF idénticos a los del repositorio. Sin `\resizebox`. Fig. 3 al 0.40 del ancho queda con leyenda de ~5 pt (m9). |
| m1 (ejemplo 2-D Prop. 3.6) | aplicado bien | `:163-164`. Recalculado: μ = (2/3, 0), producto cruzado centrado = 0 (escala diagonal), s = (2.9439, 0.5099), T₁ = 2, O₁ = 0.5 para ambos; D(q₁) = 0.4216, D(q₂) = 0.0251. Direcciones de S(xᵢ − q) correctas. Converso 1-D: D(1) = D(5/3) = 2/3, T₁ = 1/3 y 1. |
| m2 (D = 1 en la mediana) | aplicado bien | `:104`; Milasevic–Ducharme verificado (Bibliografía). |
| m3 ("hull method") | aplicado bien | `:220` "local-support method (HKNN, LPH or NFL)"; README:40. (El "8 of 8" es frágil por el empate de moons: M3 nuevo.) |
| m4 (C3 vs mejor por exactitud selectiva) | aplicado bien | `:246`; `SelBySel*` coinciden con `sel_vs_best_by_sel` del JSON (digits LCD +0.07 [−0.12, +0.27]; moons −3.21 [−3.79, −2.62]). |
| m5 (multiplicidad p = 2) | **aplicado a medias** | `:255` "one of 13 depth intervals … (the p = 0 row repeats the moons)". También la fila p = 10 es idéntica pliegue a pliegue a moons+ruido (comprobado en los 11 métodos): son 11 intervalos distintos, no 13 (m1 nuevo). |
| m6 (resolución por pliegue) | aplicado bien | `:280`; `FoldResIris` = 3.33, `FoldResWine` = 2.78 (= 100/⌈n/5⌉). |
| m7 (`params_mode` determinista) | aplicado bien | `support_geometry.py:466-473` y `make_numbers.py:88-93`; al regenerar, `make_numbers.py` avisa de 4 modas distintas de las almacenadas (wine/LPH, breast cancer/OD, moons/HKNN, esferas/kNN); las tres que aparecen en la Tabla 5 son las que lista la respuesta. |
| m8 (desempate de vecinos) | aplicado bien (con matiz aceptable) | `:77` "ties broken deterministically". |
| m9 (resustitución en logit) | aplicado bien | `:173`; `OptimTod*` 0.4–2.0, `OptimHknn*` 0.4–2.1 regenerados idénticos. |
| m10 (bibliografía) | aplicado bien | 29 entradas, todas citadas (comparé claves de `refs.bib` con `\cite*` de `main.tex`); cevikalp2008, fixhodges1989 corregidas; tres entradas nuevas verificadas por web (Bibliografía). |
| m11 ("four" → "five") | aplicado bien | `:280`, `NNearCeiling` = 5 con umbral 96 % explícito. |
| m12 (FICHA "no superó…") | aplicado bien | FICHA:13/24. (Otra frase de la FICHA introduce un error distinto: m4 nuevo.) |
| m13 (tabla de afirmaciones) | aplicado bien | `:259-276`, 7 filas. |
| m14 (`k_NN`) | aplicado bien | macro `\kNN` (`:45`) en `:107`, `:173`, `:179`, `:293`. |
| m15 (fecha fija, README) | aplicado bien | `:52` "3 October 2026"; README:15 "10 páginas". |

---

## Hallazgos nuevos

### Bloqueantes

Ninguno. El veredicto C1 no depende de ninguno de los problemas siguientes (lo comprobé en la corrida de sensibilidad de M1).

### Mayores

#### M1. La ampliación de rejillas que se descartó es barata y cambia la evidencia de C2; las fracciones en el borde declaradas omiten las ablaciones y E2

- **Ubicación.** `main.tex:179` (Note on the grids: "On the two moons datasets the comparison is symmetric… A further widening… was measured at about twice the cost of the reference run"); `:244` (C2: "the attribution therefore rests on the size of the effects (+5.1 points on digits, +3.5 on spheres, +2.7 on the moons with noise)"); `:255` (E2, contribución ortogonal +1.1 a +2.7); `:59` (resumen, 7/8), `:267` (C2 "verified"), `:280`; README:41/44; FICHA:13/24; CONTINUIDAD:19/45/65; RESPUESTA (M2).
- **Problema 1 (coste).** La respuesta estima ≈ 9 min de CPU para recorrer *todo* con rejillas ampliadas, dominado por digits (186 s de los 294 s, `results.json` → `seconds_cpu`). El problema de borde está en moons (4.3 s) y moons+ruido (11.7 s), con 240 puntos por clase en el pliegue de entrenamiento: allí k = 50 o 75 es viable y no hace falta tocar iris ni wine. Medido por mí (copia del script, mismas semillas, solo esos dos conjuntos, `K_GRID = {5,10,20,30,50,75}`, kNN hasta 81, λ_rel hasta 1000): **19 s + 32 s de CPU**.
- **Problema 2 (no es simétrico para las ablaciones).** Fracción de pliegues con k = 30 en `results.json` (no reportada en el texto): **TD 100 %** en moons+ruido, 76 % en moons, 52 % en digits; SD 84 % / 100 % en moons / moons+ruido; en E2, p = 5: TD 80 %, SD 68 %, HKNN 56 %; p = 20: TD 100 %, SD 100 %, HKNN 92 %, LCD 88 %, k_NN = 41 en 80 %. La "Note on the grids" solo da TOD/HKNN (y kNN/λ en moons+ruido).
- **Evidencia (sensibilidad, moons+ruido, 5×5 completo):**

  | | rejilla de referencia (k ≤ 30) | k ≤ 50 | k ≤ 75 |
  |---|---|---|---|
  | exactitud TD | 79.80 | 82.60 | 83.37 |
  | exactitud TOD | 82.47 | 83.10 | 83.10 |
  | **TOD − TD** (bootstrap) | **+2.67 [+1.5, +3.8]** | **+0.50 [−0.43, +1.40]** | **−0.27 [−1.17, +0.60]** |
  | pliegues de TD en el k máximo | 100 % | 96 % | 76 % |
  | mejor referencia | HKNN 82.83 (empate con LCD) | LPH 83.47 | LPH 83.43 |
  | TOD − mejor referencia | −0.37 [−1.30, +0.57] | −0.37 | −0.33 [−1.17, +0.47] |

  En moons (k ≤ 75): TOD 89.10, mejor referencia kNN 89.87, TOD − mejor = −0.77 [−1.63, +0.17] (deja de ser "pérdida significativa"); TOD − TD = +1.03 (antes +1.07); TOD solo elige k = 50 en 4 % de los pliegues (su borde no era limitante), HKNN en 44 %.
- **Consecuencia.** C1 no cambia (0 victorias en todas las variantes). Pero de los tres efectos con que el texto sostiene "the orthogonal component carries the information", el de moons+ruido es un artefacto de truncar la rejilla del *modelo reducido*: TD necesita vecindades mayores y la rejilla se las niega. El de digits (+5.1, el mayor) tiene TD en el borde en el 52 % de los pliegues y no pude comprobarlo dentro del presupuesto. Solo el de esferas (TD en el borde en 0 %) queda limpio. Lo mismo afecta a la contribución ortogonal en E2 (`:255`, +1.1 a +2.7), con TD en el borde en 64–100 % de los pliegues para p ≥ 2.
- **Corrección.** (1) Corre como *análisis de sensibilidad declarado* (sin sustituir la corrida de referencia ni el criterio) moons, moons+ruido y E2 con `K_GRID` hasta 75, `KNN_GRID` hasta 81 y λ_rel hasta 1000 (≈ 2 min de CPU), y digits con `K_GRID` hasta 75 (80 puntos por clase en el pliegue; coste estimado ≈ 2× 186 s); guarda `results/results_sensitivity.json` y genera macros. (2) Sustituye en `:179` desde "On the two moons datasets…" por: "The edge is not symmetric across models: the reduced model TD sits at $k=30$ in all folds on the moons with noise (\FracKMaxMoonsNTd\%), and a sensitivity run with $k\le75$ (Appendix~B) changes TOD$-$TD there from \AblMoonsNTd{} to \SensAblMoonsNTd{} points, while C1 is unchanged (\SensDeltaBestMoonsN{} against the best reference)." (3) En `:244` deja como efectos de apoyo solo los que sobreviven a la sensibilidad y añade "(the moons-with-noise effect is a grid artefact; see Appendix B)"; ajusta el resumen y la fila C2 de la tabla de afirmaciones (p. ej. "verified on spheres and digits; grid-dependent on the moons with noise"). (4) Genera las fracciones en el borde para *todos* los métodos (incluidas TO, TD, OD, SD, LCD, NFL) y para E2, y publícalas en `results/tables_appendix.md`; en `:179` cita el máximo fuera de los moons sobre todos los métodos, no solo TOD/HKNN. (5) Corrige README:44, FICHA, CONTINUIDAD:19/45/65 y la respuesta a M2 (el coste real de la opción (a) acotada a los conjuntos afectados).

#### M2. La Observación 3.2 omite iris y subestima el alcance: con el k elegido, HKNN no tiene término de casco en 5 de 8 conjuntos

- **Ubicación.** `main.tex:131` ("This is the case for every $k$ in our grids on the \NLowDim{} datasets with $d\le3$"); `make_numbers.py:323-324` (`D[n]["d"] <= 3`); `:150` (Obs. 3.4: "HKNN already combines the two distances"); `:220` ("best reference was a local-support method … on 8 of 8"); `:278` ("does not add predictive information beyond the local hull"); resumen `:59` ("describes local-hull classifiers well"); README:34; FICHA:13/24; CONTINUIDAD:13/37.
- **Problema.** La condición de la Observación es k > d con k ∈ {5, 10, 20, 30}; iris tiene d = 4 < 5, así que son **4** conjuntos (iris, swiss roll, moons, esferas), no 3. Más importante: con los k *elegidos* (`results.json`, `params`), HKNN trabaja con k > d (ρ = d, O_ρ ≡ 0) en el **100 %** de los pliegues en iris, swiss roll, moons, moons+ruido (d = 12, k ∈ {20, 30}) y esferas, y en el **60 %** en wine (d = 13); solo en breast cancer y digits (0 %) hay término de casco. En esos cinco conjuntos HKNN es h_λ² = Σ_j λt_j²/(s_j²+λ) = rᵀ(I + VᵀV/λ)⁻¹r, una distancia de Mahalanobis local regularizada al centroide, no una distancia a un casco; y como HKNN es la mejor referencia en 5 de 8 conjuntos (4 de ellos de ese grupo), la conclusión "beyond the local hull" describe mal lo que se comparó.
- **Corrección.** (1) `make_numbers.py:323-324`: `mac("NLowDim", sum(D[n]["d"] < min(m["k_grid"]) for n in D))` y la lista correspondiente; añade la macro `HknnRhoEqDList` con la fracción de pliegues en que el k elegido de HKNN supera d. (2) Sustituye la segunda frase de la Obs. 3.2 por: "This happens for every $k$ in our grids on the \NLowDim{} datasets with $d<5$ (\LowDimList), and, at the neighbourhood size actually selected, for \meth{HKNN} in all folds on the moons with noise and in \FracHknnRhoWine\% of the folds on wine: on five of the eight datasets \meth{HKNN} is therefore the penalised tangential term $r^\top(I+V^\top V/\lambda)^{-1}r$, a regularised local Mahalanobis distance to the neighbourhood centroid, and not a distance to a hull." (3) En `:278` y en el resumen, cambia "beyond the local hull" / "local-hull classifiers" por "beyond HKNN-type local distances (a regularised hull distance where $d\ge k$, a regularised local Mahalanobis distance where $k>d$)". (4) README:34, FICHA:13/24, CONTINUIDAD:13: "en los conjuntos con d < k (4 por la rejilla; 5 por el k elegido)".

#### M3. La "mejor referencia" de moons es un empate exacto a tres, resuelto por redondeo de coma flotante; la "pérdida significativa" en moons depende de ello

- **Ubicación.** `support_geometry.py:452` (`best_ref = max(REFERENCES, key=lambda m: means[m])`, sin regla de empate declarada); `main.tex:177` (definición de la mejor referencia); Tabla 1 (`:200`, moons: kNN 89.9, **HKNN 89.9**, LCD 89.9); Tabla 2 y su pie (`:216`, "significant losses: 2 … (digits, moons)"); `:220` ("on 8 of the 8 datasets"; pérdida en moons); README:39/40; CONTINUIDAD:19/26/36.
- **Evidencia.** En moons kNN, HKNN y LCD aciertan exactamente 2697 de 3000 predicciones de prueba; sus medias almacenadas son 0.8989999999999999, 0.899 y 0.8989999999999999, así que `max` elige HKNN por el último bit. Contra cada una de las tres empatadas, TOD − referencia = −0.77 con IC bootstrap [−1.27, −0.27] (HKNN), [−1.40, −0.13] (LCD) y **[−1.60, +0.17] (kNN)**. En moons+ruido HKNN y LCD empatan (2485/3000). Las filas p = 0 y p = 10 de E2 heredan ambos empates.
- **Corrección.** Declara una regla de empate en `:177` y en el código (comparar el número entero de aciertos, no la media en coma flotante; ante empate, informar de todas las referencias empatadas y usar para cada afirmación la menos favorable a ella: para una pérdida, la de límite superior más alto). Texto en `:220`: "The best reference was a local-support method on 7 of the 8 datasets; on the moons kNN, HKNN and LCD tie exactly (2697 of 3000 correct)…"; pie de la Tabla 2: "significant losses with the bootstrap: digits, and moons against two of the three tied references; 0 with NB". Señala el empate en la Tabla 1 (negrita en las tres o nota al pie).

### Menores

- **m1. "One of 13 depth intervals" (`main.tex:255`, `make_numbers.py:369`, README:43, CONTINUIDAD:30).** Las filas p = 0 y p = 10 de E2 son idénticas pliegue a pliegue a moons y moons+ruido (comprobado en los 11 métodos; `make_datasets` usa las mismas `noise_dims[:, :10]`). Son 11 intervalos distintos. Texto: "one of 11 distinct depth intervals in E1 and E2 (the rows $p=0$ and $p=10$ repeat the moons and the moons with noise)"; macro `len(D) + len(rn) - 2` o, mejor, deduplicar comparando las listas por pliegue.
- **m2. Tabla 2: la misma comparación aparece con dos IC bootstrap distintos.** En los 5 conjuntos cuya mejor referencia es HKNN, "TOD − best" y "TOD − HKNN" son la misma diferencia, pero los IC difieren: moons [−1.27, −0.27] frente a [−1.27, −0.23]; breast cancer [−0.70, +0.21] / [−0.67, +0.21]; swiss roll [−0.60, +0.17] / [−0.60, +0.20]; moons+ruido [−1.30, +0.57] / [−1.30, +0.53]; esferas [−0.53, +0.97] / [−0.50, +1.00]. Causa: `compare()` llama a `paired_stats` dos veces con el mismo `rng` (`support_geometry.py:454-456`). Corrección: en `compare`, generar una sola matriz de índices de remuestreo por conjunto (`idx = rng.integers(0, J, (N_BOOT, J))`) y aplicarla a todas las diferencias (bootstrap pareado común), o reutilizar `vs_each[best_ref]` como `vs_best`. Sin recorrer, `make_numbers.py` puede imprimir en la Tabla 2 `vs_each["HKNN"]` para ambas columnas cuando coinciden.
- **m3. Esferas: "where the depth is the component that helps" (`main.tex:242`; README:41; CONTINUIDAD:28).** El intervalo citado es TOD − TO = +0.5 [−0.0, +1.0] (exacto: +0.47 [−0.03, +0.97]): no excluye 0, y el texto dice dos frases después que quitar la profundidad nunca cuesta de forma significativa. Sustituir por "where the depth adds +0.5 points (bootstrap interval [−0.03, +0.97], not significant)".
- **m4. FICHA:13 y :24.** "quitar la profundidad o la tangencial no cambia la exactitud de forma significativa en ninguna de las dos lecturas" / "does not change accuracy significantly in either reading": con el bootstrap, quitar la profundidad *mejora* la exactitud en breast cancer (TOD − TO = −0.35 [−0.70, −0.00]). Escribir "no la reduce de forma significativa en ninguna de las dos lecturas" / "never reduces accuracy significantly in either reading" (como el resumen).
- **m5. Def. 2.3, `main.tex:93`: "and nothing else in the paper changes".** Bajo la lectura alternativa HKNN sería otro clasificador: cambiaría su columna en la Tabla 1 y la mejor referencia en los 5 conjuntos donde lo es. Sustituir por "Proposition 3.3 and Remark 3.4 hold with weights … in place of …; the empirical results are for the reading adopted here."
- **m6. Prop. 3.3 es la identidad de la regresión ridge.** min_α ‖r − Vᵀα‖² + λ‖α‖² = λ rᵀ(VᵀV + λI)⁻¹ r = rᵀ(I + VᵀV/λ)⁻¹ r; la descomposición espectral de (I + VᵀV/λ)⁻¹ da directamente la fórmula. Añadir esta línea tras la proposición: acorta la demostración, deja claro que HKNN es una distancia de Mahalanobis local regularizada (lo que usa M2) y evita que se lea como resultado nuevo.
- **m7. Signos y ceros en las cifras.** `make_numbers.py:50-51` (`signed`) produce un guion ASCII que en texto se compone como guion, no como signo menos ("-0.4 to +0.5" en las pp. 6–7 del PDF), y los límites que deciden la significación salen como "−0.0"/"+0.0" (Tabla 3: breast cancer [−0.7, −0.0] cuenta como < 0, esferas [−0.0, +1.0] no cuenta como > 0, NB esferas [+0.0, +7.1] cuenta como > 0; texto: "upper limit -0.0"). Corrección: `signed` debe devolver `$-0.4$`/`$+0.5$` (o usar `\textminus`), y la Tabla 3 debe ir a dos decimales como la Tabla 2.
- **m8. Cita de apoyo en `main.tex:242`.** "these are the known advantages of local hulls over points and over depth [vincentbengio2002]": Vincent–Bengio comparan con kNN y SVM, no con clasificadores por profundidad. Limitar la cita a "over points" o citar ghoshchaudhuri2005/licuestaliu2012 para la comparación con profundidad.
- **m9. Figura 3 al 0.40 del ancho (`main.tex:250`).** Leyenda y ejes de ~5 pt en el PDF (p. 7); las curvas HKNN y LCD se superponen. Subir a 0.5 del ancho o eliminar la figura y dejar dos frases (la tabla ya está en `tables_appendix.md`).
- **m10. Incoherencias en archivos auxiliares.** README:45 y CONTINUIDAD:74 dicen "ronda 1 ≈ 45 s de CPU"; la RESPUESTA (M2) dice "≈ 1.5 min". CONTINUIDAD:60 dice "bibliografía en `\small`"; `main.tex:302` usa `\footnotesize`. CONTINUIDAD:47 sigue listando como "a cotejar" tres entradas que ya están verificadas (Bibliografía).
- **m11. Prueba entre conjuntos (opcional, `main.tex:175`).** Se cita Demšar (2006) para no agregar conjuntos, pero Demšar recomienda el test de rangos con signo de Wilcoxon sobre las diferencias medias por conjunto. Añadirlo como lectura complementaria cuesta una línea y refuerza el negativo: sobre las 8 diferencias TOD − mejor referencia, W = 4, p bilateral = 0.055, p unilateral (TOD mejor) = 0.98; test de signos: 2 de 8 positivas, p unilateral = 0.96.

---

## Bibliografía

Red: `WebFetch` bloqueado para proceedings.neurips.cc, frontiersin.org y lacuna.tiptreesystems.com; `curl` rechazado por el proxy para researchgate.net, arxiv.org, export.arxiv.org, citeseerx.ist.psu.edu, www.iro.umontreal.ca, web.archive.org, scholar.archive.org, api.crossref.org, dblp.org, openreview.net, pdfs.semanticscholar.org y core.ac.uk. Solo hubo búsqueda web (resúmenes de resultados).

| Entrada | Estado | Corrección |
|---|---|---|
| bouckaertfrank2004 (nueva) | verificada (web, Springer): PAKDD 2004, LNCS 3056, pp. 3–12, Springer; respalda el uso de 1/J + n_test/n_train para k-fold repetida | añadir `doi = {10.1007/978-3-540-24775-3_3}` |
| milasevicducharme1987 (nueva) | verificada (web, Project Euclid): Ann. Statist. 15(3), 1332–1333, 1987; el resultado (unicidad si la medida no está concentrada en una recta) respalda `main.tex:104` | añadir `doi = {10.1214/aos/1176350511}` |
| uci (cambiada) | verificada (web): Kelly, Longjohn & Nottingham, 2023, https://archive.ics.uci.edu | opcional: citar además el conjunto wine (Aeberhard & Forina, con el DOI que da su página en UCI) |
| kambhatlaleen1997 (ahora citada) | verificada (web): Neural Computation 9(7), 1493–1516, 1997 | añadir `doi = {10.1162/neco.1997.9.7.1493}` |
| demsar2006 (ahora citada) | verificada (web, JMLR): 7, 1–30, 2006 | ver m11 |
| vincentbengio2002 | metadatos verificados (web): NIPS 14, pp. 985–992. **Lectura de la puntuación HKNN: no verificable por búsqueda web.** Los resúmenes accesibles solo dicen que se añade una penalización de "weight decay" que mantiene el punto "fantaseado" cerca del centro de los vecinos y que α se obtiene de un sistema con VᵀV y λ; eso fija el minimizador, no si la puntuación es el valor del objetivo o la distancia sin penalizar en el minimizador. El PDF no fue accesible por ninguna ruta | mantener la lectura declarada con la redacción de m5; cotejar con una copia local del PDF |
| cevikalp2008, fixhodges1989, serfling2002, lilu1999, vardizhang2000, paindaveinevanbever2013 | verificadas en la ronda 1; los campos corregidos están en `refs.bib` | — |
| resto (coverhart1967, hastietibshirani1996, tukey1975, liu1990, zuoserfling2000, chaudhuri1996, ghoshchaudhuri2005, licuestaliu2012, chow1970, dietterich1998, nadeaubengio2003, efrontibshirani1993, pedregosa2011, harris2020, virtanen2020, fisher1936, street1993) | sin cambios desde la ronda 1; no las volví a verificar | — |

Uso de las citas: todas respaldan lo que se afirma, salvo vincentbengio2002 en `:242` para "over depth" (m8).

---

## Verificación computacional

CPU total gastada por este árbitro: ≈ 2.5 min (4 núcleos, BLAS de un hilo).

| Qué | Coste | Resultado |
|---|---|---|
| `make_numbers.py` sobre una copia de la carpeta | 1.5 s CPU | `numbers.tex` (1313 macros), las 9 `table_*.tex` y `results/tables_appendix.md` **idénticos byte a byte** a los del repositorio |
| IC NB independientes (`check_nb.py`) desde las listas por pliegue de `results.json` y `results_regime.json` | < 2 s | macros `NbLo/NbHi*`, `CiHiBestMaxNb(Two)`, recuentos `N*NbAboveZero/BelowZero`, `NSelNb*`, `NRegSigWinsNb`, p = 0.282 en E2: todos coinciden; `nb_p` del JSON coherentes con los IC NB |
| Reproducción del protocolo completo (5×5) de moons, moons+ruido, iris y esferas con el script v0.2 y la semilla maestra | ≈ 35 s CPU | exactitudes por pliegue **idénticas** a `results.json` en los 11 métodos de los 4 conjuntos. No repetí la corrida completa (294 s CPU, dominada por digits) para respetar el presupuesto |
| Sensibilidad de rejillas en moons y moons+ruido (k ≤ 75, k_NN ≤ 81, λ_rel ≤ 1000; y k ≤ 50 en moons+ruido) | 19 + 32 + 19 s CPU | ver M1: C1 sin cambios; TOD − TD en moons+ruido +2.67 → +0.50 → −0.27 |
| Empates de la mejor referencia (`check_ties.py`) | < 1 s | M3 |
| Fracciones en el borde para todos los métodos y E2; fracción de pliegues con k elegido > d | < 1 s | M1, M2 |
| Prop. 3.6 (ejemplo 2-D y 1-D) | < 1 s | coincide (m1 de la ronda 1) |
| Duplicados en E2 | < 1 s | p = 0 ≡ moons, p = 10 ≡ moons+ruido (m1) |
| `latexmk -pdf` en copia, desde cero | 2.5 s | 10 páginas, 0 errores, 0 `Overfull`, 0 indefinidas, 0 "??", `.bbl` y texto del PDF idénticos a los del repositorio |

---

## Extensión

El PDF tiene exactamente 10 páginas con bibliografía. No hace falta recortar. Si se añade la sensibilidad de M1, conviene ponerla en el Apéndice B en una tabla de cuatro filas (moons, moons+ruido, E2 p = 5, p = 20) y compensar quitando la Figura 3 (m9), cuya información ya está en dos frases y en `tables_appendix.md`.

---

## Lista de acciones (por prioridad)

1. Corre la sensibilidad de rejillas en moons, moons+ruido y E2 con k hasta 75 (≈ 2 min de CPU) y, si el presupuesto lo permite, digits con k hasta 75; guárdala aparte sin tocar la corrida de referencia (M1).
2. Reescribe la atribución C2 (`main.tex:244`, resumen `:59`, fila C2 de `:267`, README:41, FICHA:13/24) apoyándola solo en los efectos que sobreviven a la sensibilidad; declara el de moons+ruido como artefacto de rejilla (M1).
3. Sustituye la "Note on the grids" (`:179`) y Limitaciones (`:280`) con las fracciones en el borde de *todos* los métodos, incluidas las ablaciones y E2, y quita "the comparison is symmetric"; corrige la estimación de coste en README:44, CONTINUIDAD:19/45/65 y RESPUESTA (M1).
4. Corrige `NLowDim` (`make_numbers.py:323`: `d < min(k_grid)`, 4 conjuntos) y reescribe la Obs. 3.2 con la fracción de pliegues en que HKNN elige k > d (5 de 8 conjuntos, 60 % en wine) (M2).
5. Cambia "beyond the local hull" / "local-hull classifiers" en `:59` y `:278` por una formulación que cubra el régimen k > d (distancia de Mahalanobis local regularizada) (M2, m6).
6. Declara y aplica una regla de empate para la mejor referencia (aciertos enteros; informar de todas las empatadas); corrige "8 of 8", el pie de la Tabla 2 y la pérdida de moons (`:177`, `:216`, `:220`, README:39/40, CONTINUIDAD) (M3).
7. Corrige "one of 13 depth intervals" a 11 distintos (`:255`, `make_numbers.py:369`, README:43, CONTINUIDAD:30) (m1).
8. Usa los mismos índices de remuestreo bootstrap para todas las comparaciones de un conjunto, o imprime una sola vez TOD − HKNN en la Tabla 2 (m2).
9. Corrige "the depth is the component that helps" en esferas (`:242`, README:41, CONTINUIDAD:28) (m3) y la frase de la FICHA sobre quitar la profundidad (m4).
10. Sustituye "and nothing else in the paper changes" en `:93` (m5); añade la forma rᵀ(I + VᵀV/λ)⁻¹r tras la Prop. 3.3 (m6).
11. Haz que `signed()` devuelva signos menos en modo matemático y pon la Tabla 3 a dos decimales (m7).
12. Limita la cita de Vincent–Bengio en `:242` a "over points" (m8); añade los DOI de bouckaertfrank2004, milasevicducharme1987 y kambhatlaleen1997 y pásalas a "verificadas" en CONTINUIDAD:47 (Bibliografía, m10).
13. Agranda o elimina la Figura 3 (m9); unifica el CPU de la ronda 1 y la nota sobre `\small`/`\footnotesize` (m10).
14. Opcional: añade el test de Wilcoxon entre conjuntos como lectura complementaria (m11).
15. Mantén abierto el cotejo de la §3 de Vincent–Bengio con una copia local del PDF; ninguna ruta de red disponible lo permite.
