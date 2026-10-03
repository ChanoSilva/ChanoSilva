# Respuesta del autor al informe de árbitro interno — HQF001, ronda 1 (30/09/2026)

Respuesta escrita el 03/10/2026 sobre el informe `REFEREE_HQF001_ronda1_20260930.md` (2 bloqueantes, 6 mayores, 12 menores, 14 acciones). Documento de trabajo escrito de forma incremental mientras se aplicaban los cambios; estado final al cierre de la sesión.

Convención: **aceptar** = se aplica tal cual; **aceptar con matiz** = se aplica una versión y se explica; **rebatir** = solo con demostración o cálculo.

## Resumen de decisiones

| id | decisión | estado |
|---|---|---|
| B1 | aceptar | aplicado |
| B2 | aceptar | aplicado |
| M1 | aceptar | aplicado |
| M2 | aceptar con matiz | aplicado |
| M3 | aceptar | aplicado |
| M4 | aceptar | aplicado (opción 1: dataset recalibrado y corrida completa) |
| M5 | aceptar | aplicado |
| M6 | aceptar | aplicado (Prop. 3.2(c) añadida) |
| m1–m12 | aceptar (12/12); m5 y m7 con matiz | aplicados |

Recuento: 20 hallazgos; **19 aceptados**, **1 aceptado con matiz** (M2: el registro fechado del criterio solo puede crearse ahora, y así se declara), **0 rebatidos**. Las 14 acciones de la lista final están aplicadas; la 8 en su opción fuerte (correr la variante), la 13 con la figura eliminada en vez de corregida.

## Plan de trabajo (orden de ejecución)

1. Código (`selective_benchmark.py`): B2 (IC por par con semilla propia, `__best__` copia la comparación directa, B = 20 000), B1 (IC t de Student e IC t corregido Nadeau–Bengio por par; victorias/empates/derrotas), M4 (calibración con indicador de límite y espectro de covarianzas que admite solución), m6 (configuraciones de QDA que no completan los pliegues internos se descartan).
2. Corrida de referencia completa con el script actual (M2.1) → `results/results.json` nuevo; la v0.1 se conserva en `results/results_v01.json`.
3. `make_numbers.py`: macros para IC t / NB, W/T/L, recuentos bajo cada intervalo, casos límite (< 0.02 de cero), tabla única AURC, tabla de diferencias rediseñada.
4. Manuscrito: reescrituras B1/M3/M5/M6, M1, m2–m4, m8–m12, recortes a ≤ 10 páginas, Apéndice A (m5, M2).
5. Archivo fechado con el criterio (M2.2), README, FICHA, CONTINUIDAD.

## Detalle por hallazgo

### B1 — IC bootstrap optimistas que inflan todas las afirmaciones positivas. **Aceptar.**
El árbitro tiene razón en el punto central: el optimismo de los IC sobre pliegues repetidos solo es conservador para el recuento "mejor" del criterio (que no puede bajar de 0), y favorece a todo lo demás que el texto afirmaba en positivo. Verifiqué sus cifras desde `per_fold` antes de tocar nada: mi implementación del IC t (14 g.l.) y del IC con corrección de Nadeau–Bengio (ρ = n_test/n_train = 1/4) reproduce exactamente las suyas (iris campo − LDA: t [−0.03, +0.43], NB [−0.30, +0.70], V/E/D 1/6/8; digits aniso − iso: t [−1.25, −0.32], NB [−1.79, +0.23], 15/0/0; etc.).
Cambios: (a) `selective_benchmark.py`, nueva función `pair_stats`: para cada par se almacenan media, IC bootstrap percentil (el predefinido), IC t de Student, IC t Nadeau–Bengio, victorias/empates/derrotas, p de Wilcoxon (descriptivo), veredicto bajo cada intervalo y un indicador de caso límite (extremo del IC bootstrap o t a < 0.02 de cero en AURC×100); el criterio se evalúa con el bootstrap (predefinido) y se reporta también el mismo recuento bajo t y NB. (b) `make_numbers.py` y `main.tex`: la Tabla de diferencias frente a la mejor referencia pasa a dar las tres columnas de IC, V/E/D y p; la tabla de ablaciones da IC bootstrap, IC t y V/E/D para aniso − iso y marca las demás celdas con negrita/cursiva solo cuando **ambos** intervalos excluyen cero (superíndice b: solo el bootstrap); lo mismo en la tabla campo vs cada referencia. (c) Reescritas las frases de main.tex:161 y :330 con la formulación del árbitro; resumen, §6, Tabla de afirmaciones y ficha con "2–3 datasets según el intervalo; sugerente, no establecida" y "6 con bootstrap, 5 con IC t" (los números concretos salen de macros, no se tipean). Véanse las cifras finales en la sección "Números que cambiaron" al final de este documento.

### B2 — Dos IC distintos para el mismo par; viñeta de la nota incorrecta. **Aceptar.**
Confirmado: `__best__` se remuestreaba aparte. Cambios: (a) cada par tiene su propio generador sembrado con la semilla maestra y un CRC32 del nombre del par (`pair_rng`; no se usa `hash()` porque Python lo sala por proceso), así que el IC de un par no depende del orden de evaluación; (b) `__best__` es ahora `dict(comp[best_ref])`, una copia; (c) B = 20 000 (coste ≈ 3 s al re-resumir). Resultado sobre los pliegues v0.1 (antes de la nueva corrida): breast-cancer campo vs NCM pasa a [−0.65, +0.0006] → **no concluyente y límite**, como anticipó el árbitro con B = 200 000; breast-cancer vs k-NN [+0.0017, +0.54] sigue "peor" pero límite; moons aniso − iso [−0.10, +0.005] límite; wine vs mejor referencia [−0.005, +0.10] límite. Todos los pares límite se marcan en las tablas (superíndice ∘) y se listan en el texto mediante macros. "NCM 8/0" se sustituye por lo que resulte de la corrida v0.2. (d) Viñeta de la nota reescrita con las cifras del árbitro (desplazamientos hasta 0.25, mediana 0.014, 4 veredictos individuales cambiados, ninguno del criterio); no las recalculé yo: cito su verificación (`verif_math_stats.txt`, D2) como fuente.

### M4 — synth-classcov con medias coincidentes. **Aceptar** (opción 1 del árbitro: correr la variante con desplazamiento no nulo).
`_calibrate_shift` devuelve ahora `(shift, at_bound)` y el indicador se guarda en el JSON (`shift_at_bound`). Con el espectro v0.1 (2, 1, 0.5, 0.25, 0.1, 0.05) no hay solución en [0.05, 20] (error de Bayes con medias coincidentes 7.7 %); probé cuatro espectros menos dispares (coste 4 s de CPU) y elegí `geomspace(2, 0.25, 6)`: error de Bayes 20.6 % con medias coincidentes, desplazamiento calibrado 1.54, error de Bayes 9.9 %. Las rotaciones y todos los demás sorteos son idénticos a v0.1 (mismo consumo del RNG; synth-lda reproduce su desplazamiento 1.20 y su error 9.8 %). Como el dataset cambia, se repite la **corrida de referencia completa** con el script v0.2 (resuelve a la vez M2.1, B2 y m6); la v0.1 se conserva en `results/results_v01.json` y `results/tables_v01.md`, y el manuscrito y la nota reportan explícitamente los números v0.1 de synth-classcov (medias coincidentes) junto a los v0.2, con la advertencia de que el conjunto de datasets del criterio se modificó tras ver los resultados v0.1 (el veredicto del criterio es el mismo en ambas versiones).

### m6 — QDA con configuraciones omitidas. **Aceptar.** En `evaluate_fold`, una configuración que no completa los 3 pliegues internos se descarta y se cuenta (`inner_configs_dropped`, agregado por método y dataset en el resumen); el Apéndice A reporta el total. En la prueba de humo (iris, pliegue 1) no se descartó ninguna y los 13 AURC coinciden bit a bit con v0.1.

### M1 — Identidad para K ≥ 3 sin "equiprobable". **Aceptar.**
Añadido "equiprobable" en el resumen (main.tex), en la ficha (ES/EN) y en el README. Además, siguiendo la sugerencia opcional, la Prop. 3.1(iii) enuncia la forma general $s = 2\log(p_{(1)}/p_{(2)}) - 2\log(\pi_{(1)}/\pi_{(2)})$ cuando los dos prototipos más próximos son las dos clases de mayor posterior (en el mismo orden), con la línea de prueba correspondiente ($\log(p_i/p_j) = \log(\pi_i/\pi_j) + (d_j^2 - d_i^2)/2$). `lda_identity.py` la verifica con priors (0.6, 0.3, 0.1): desviación de la identidad sin término de priors 3.58 (la misma cifra que obtuvo el árbitro), 7.1×10⁻¹⁵ con el término, sobre el 85.3 % de puntos en que coinciden los pares.

### M2 — Sin registro fechado del criterio; `results.json` de una versión anterior del script. **Aceptar con matiz.**
(1) Se regeneró `results.json` con el script actual mediante la corrida completa (284.5 s de CPU), así que metadata y código coinciden; la metadata falsa ("calibrated so Bayes error = 10%") desaparece y el JSON exporta `shift` y `shift_at_bound`; el parche de `make_numbers.py` que reproducía el generador se eliminó. (2) Se creó `CRITERIO_HQF001.md` con el texto exacto del criterio (también en la constante `CRITERION_TEXT` del script y en `meta.criterion` del JSON), la línea que lo evalúa, el sha256 del script v0.2 y la historia. **Matiz:** el archivo está fechado el 03/10/2026; no existe un registro fechado independiente anterior a la corrida y el archivo y el manuscrito (§4) lo dicen explícitamente, citando como evidencia indirecta `results_v01.json` (`majority_needed = 5`, mismo veredicto) y la reproducción bit a bit del árbitro. (3) §4 declara la corrección de la clave de hiperparámetros entre la prueba rápida y la corrida de referencia, antes de ver resultado alguno.

### M3 — Lenguaje inferencial y comparaciones múltiples. **Aceptar.**
"Significantly" eliminado de todo el texto (resumen, §4, §5, Tabla de afirmaciones); se usa "with a 95 % interval excluding zero" y se indica con qué intervalo. "Statistically indistinguishable" → "inconclusive", con victorias/empates/derrotas por macro (wine 4/4/7, digits 7/0/8; iris 1/6/8 con IC t). Frase explícita en §4: no se aplica corrección por multiplicidad a los 56 + 48 intervalos de las Tablas 4 y 5, que son descriptivos; no se hacen los tests entre datasets de Demšar. El p de Wilcoxon pasa a la Tabla 3 como chequeo descriptivo, citando Wilcoxon (1945) (véase m2).

### M5 — README y ficha cierran la línea más de lo que el cuerpo autoriza. **Aceptar.**
README: "la formulación reconstruida queda descartada con números; se propone cerrar la línea salvo las tres vías concretas del §6". Ficha (ES/EN): estado "Cerrada para la formulación no supervisada evaluada — resultado negativo con criterio predefinido"; alcance con las tres vías no exploradas (campo supervisado, regla margen + volumen, alta dimensión) en lugar de "la única vía", y la advertencia de que la definición es una reconstrucción. Resumen: "the question, in the precise form reconstructed here, is answered in the negative". §6: "the line is proposed to close for the unsupervised formulation evaluated here".

### M6 — Remark 3.3 excede las hipótesis de las proposiciones. **Aceptar.**
Añadida la Prop. 3.2(c) (prototipos arbitrarios $\nu_c(x)$): $s_{A,\nu} - s = 2(x-\bar m)^{\top}(A-\Sigma^{-1})\delta + 2(x-\bar m)^{\top}A(\delta_\nu-\delta) + 2(\bar m-\bar m_\nu)^{\top}A\delta_\nu$, con prueba de tres líneas (la identidad $d^2_M(x,\nu_2)-d^2_M(x,\nu_1) = 2(x-\bar\nu)^{\top}M(\nu_1-\nu_2)$ vale para cualquier $M$ simétrica y cualquier par) y verificación numérica (residuo relativo 4×10⁻¹⁴ en 500 casos aleatorios). Las Remarks 3.3 y 3.4 se fusionaron en un párrafo de texto corriente etiquetado "proved here for fixed prototypes / heuristic for local prototypes / design", que dice que la variante de prototipos globales aísla empíricamente los términos de prototipos y que synth-lda mide error de estimación y efecto de prototipos sin separarlos. La Tabla de afirmaciones separa la fila demostrada (Prop. 3.2) de la fila heurística ("where the field could help it must do so along δ" para el método tal como se corre).

### Menores
- **m1. Aceptar.** Nota: 7.1×10⁻¹⁵; numeración 3.1/3.2 en nota, README, docstring de `lda_identity.py` y título de `tables_identity.md`.
- **m2. Aceptar.** El test por pliegues cita Wilcoxon (1945) (añadido a `refs.bib`: *Biometrics Bulletin* 1(6):80–83); Demšar (2006) se cita solo para los tests entre datasets que no se realizan.
- **m3. Aceptar.** Añadido Kohonen (1995), *Self-Organizing Maps*, Springer Series in Information Sciences 30, Springer, Berlín; se cita junto a Kohonen (1990) como fuente de LVQ.
- **m4. Aceptar.** `franc2023`: `number = {11}`; autores con diacríticos (Vojt\v{e}ch Franc, Daniel Pr\r{u}\v{s}a, V\'aclav Vor\'a\v{c}ek).
- **m5. Aceptar con matiz (documentar, no corregir).** Apéndice A, párrafo "Preprocessing and inner selection": el escalador y la PCA se ajustan al pliegue externo de entrenamiento antes de la CV interna; afecta solo a la selección de hiperparámetros, nunca a los números de prueba. No se corrigió en el código porque cambiaría la selección y exigiría otra corrida completa fuera del presupuesto.
- **m6. Aceptar.** Véase arriba (configuraciones descartadas y contadas; 0 en la corrida v0.2, reportado en el Apéndice A por macro).
- **m7. Aceptar (eliminar).** La figura forest se eliminó de `make_figures.py` y de `figures/` (duplicaba la Tabla 3 y el eje symlog comprimía justo |Δ| < 1).
- **m8. Aceptar.** `\FloatBarrier` antes de §6 y del apéndice; las tablas de geometría y exactitud y la figura de curvas riesgo–cobertura salieron del PDF a `results/tables.md` (nueva sección "Geometry-only scores") y `figures/fig_rc_curves.pdf`, con un párrafo del apéndice que remite a ellas; etiquetas "[computationally verified]" quitadas de los párrafos del cuerpo.
- **m9. Aceptar.** `spct` imprime con tres decimales los extremos que redondean a ±0.00 (wine: [−0.005, +0.10]) y el par lleva marca de caso límite (∘) en la tabla y en el texto.
- **m10. Aceptar.** Macros `AblAnisoKnn/Lda/Dann` eliminadas (y los pares de ablación duplicados que las generaban); `.gitignore` deja de excluir `main.bbl`; el parche de `make_numbers.py` desapareció con M2; `results_fast.json` sigue sin conservarse (no se repitió `--fast`: 148 s de CPU; la nota lo dice).
- **m11. Aceptar.** Frase añadida a la Prop. 3.2: las identidades valen para los márgenes con signo; con el par igual y el orden invertido valen con $s_A + s$ y cambio de signo; si cambia el par no hay identidad de esa forma.
- **m12. Aceptar.** "in expectation" añadido en §2.1.

### Recortes y compilación
Aplicados los recortes 1–7 del árbitro (resumen a ≈ 240 palabras; Tablas 2 y 3 fusionadas; figura forest eliminada; Tablas 7–8 y Figura 4 fuera del PDF; Remarks 3.3–3.4 fusionados; "Tie handling" y "Grids" reducidos; §6 en un párrafo + limitaciones + vías). Como v0.2 añade contenido (tres IC por par, Prop. 3.2(c), M2, m5, registro v0.1 de synth-classcov), el PDF pasó de 11 a 13 páginas antes de los recortes y quedó en 10 páginas tras ellos. Compilación: 0 errores, 0 referencias/citas indefinidas, `pdftotext main.pdf - | grep -c "??"` = 0.

## Números que cambiaron (v0.1 → v0.2)

Fuente: `results/results.json` (v0.2) frente a `results/results_v01.json`. Los 7 datasets no modificados reproducen v0.1 bit a bit en los 15 × 13 AURC por pliegue; sus IC bootstrap cambian solo por el nuevo sembrado por par y B = 20 000 (segundo decimal).

| magnitud | v0.1 (publicado) | v0.2 |
|---|---|---|
| Criterio (campo vs mejor ref.): mejor / peor / no concl. | 0 / 6 / 2 (bootstrap B = 2000) | 0 / 6 / 2 bootstrap; **0 / 5 / 3 IC t**; 0 / 3 / 5 Nadeau–Bengio; no cumplido en las tres |
| Ablación aniso − iso: mejor / peor | 3 / 2 | 3 / 2 bootstrap; **2 / 2 IC t**; 0 / 1 NB; V/E/D digits 15/0/0, wine 8/5/2, iris 8/4/3 |
| Campo vs NCM (mejor/peor) | 8 / 0 | **7 / 0** + breast-cancer límite ([−0.65, +0.0006]) |
| Campo vs k-NN | 2 / 2 | 1 / 3 bootstrap (0 / 1 t); wine mejor solo con bootstrap; synth-classcov peor solo con bootstrap y límite |
| Campo vs LDA / QDA / LogReg / RForest / DANN | 4/3, 3/3, 4/2, 3/2, 2/3 | 4/3, 3/3, 4/2, 3/2, 1/3 (bootstrap); 4/2, 3/2, 4/2, 3/2, 0/2 (t) |
| synth-classcov: desplazamiento / error de Bayes | 0.05 (límite) / 7.7 % | 1.54 / 9.9 % |
| synth-classcov AURC×100: QDA / campo / iso / euclid / k-NN / DANN / RF / LDA | 0.97 / 1.40 / 1.24 / 1.23 / 1.69 / 1.77 / 2.48 / 48.44 | 1.69 / 2.77 / 2.30 / 2.31 / 2.55 / 2.83 / 3.42 / 6.30 |
| synth-classcov: campo − QDA | +0.43 [+0.32, +0.56] | +1.08 [+0.86, +1.33] bootstrap, [+0.81, +1.35] t, 0/0/15 |
| synth-classcov: campo vs k-NN / DANN / RF | −0.29 / −0.37 / −1.08 (mejor en los tres) | +0.22 (peor bootstrap, límite; t no concl.) / −0.06 (no concl.) / −0.65 (mejor) |
| synth-classcov: aniso − iso | +0.16 [+0.10, +0.21] | +0.47 [+0.35, +0.58] |
| Pares límite marcados | 1 (breast-cancer vs k-NN) | 5 vs referencias + wine vs mejor ref. + 5 ablaciones |
| CPU corrida de referencia | 449 s | 284.5 s |

## Tiempo de cómputo de la ronda
Corrida completa v0.2 284.5 s; pruebas de humo y `--resummarise` ≈ 15 s; exploración de espectros 4 s; `lda_identity.py` < 1 s; figuras 3 s; compilaciones ≈ 30 s. Total ≈ 5.6 min de CPU (≤ 10 min).
