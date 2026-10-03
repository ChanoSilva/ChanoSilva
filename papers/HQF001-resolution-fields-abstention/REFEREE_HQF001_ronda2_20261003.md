# Informe de árbitro interno — HQF001, ronda 2 (03/10/2026)

Objeto: borrador v0.2 (manuscript/main.tex, commit 9233b58 y anteriores del 03/10/2026), respuesta del autor `RESPUESTA_HQF001_ronda1_20260930.md`, `CRITERIO_HQF001.md`, código, `results/results.json` (v0.2), `results/results_v01.json`, tablas, README y ficha. Árbitro nuevo, independiente del de la ronda 1. Versión v0.1 de referencia: `git show b632e86:papers/HQF001-resolution-fields-abstention/...`. Trabajo auxiliar en el scratchpad (`referee2_HQF001/`). No se modificó ningún archivo del autor salvo este informe.

## Veredicto

**Cambios mayores, acotados.** El veredicto negativo es correcto, se reproduce bit a bit (585/585 AURC por pliegue en tres datasets, incluido el regenerado) y resiste una rejilla de hiperparámetros ampliada. Pero la afirmación positiva del resumen sobre la anisotropía contradice la regla de casos límite del propio texto y omite la lectura Nadeau–Bengio; el registro de la predefinición omite cambios de protocolo que git documenta (y no cita el commit que sí fecha el criterio antes de la corrida); y la saturación de la rejilla del campo, que mueve el AURC hasta un 25 %, no se declara.

Recuento de hallazgos nuevos: 0 bloqueantes, 5 mayores (R2-M1–M5), 11 menores (R2-m1–m11), más 2 correcciones bibliográficas. Ronda 1: 17 de 20 hallazgos aplicados bien, 2 a medias (M2, m1), 0 no aplicados, 1 aplicado con error nuevo (B1).

## Verificación de la ronda 1

Líneas de `manuscript/main.tex` según la versión actual (291 líneas). "R2-Mx/mx" remite a los hallazgos nuevos de este informe.

| id | estado | evidencia |
|---|---|---|
| B1 | **aplicado con error nuevo** | Columnas de IC t y NB, V/E/D y p de Wilcoxon en la Tabla 3 (`table_diff.tex`) y en la de ablaciones (`table_ablation.tex`); frase de optimismo reescrita (main.tex:160, :273); "significantly" eliminado (grep: 0 apariciones en main.tex, README, FICHA). Recalculé desde `per_fold` los 336 pares campo–referencia y los 56 de ablación: coincidencia exacta (desviación máxima 0) de media, IC bootstrap, t, NB, V/E/D y veredictos. **Pero** la cifra positiva que B1 pedía matizar ("mejora a la ablación isótropa en 2–3 datasets según el intervalo", main.tex:51, :235, :260, :271; FICHA:13, :24) cuenta como "mejor" dos pares que el propio manuscrito marca como límite y manda "leer como no concluyentes" (main.tex:160), y el rango omite la tercera lectura (NB: 0 mejor / 1 peor). Véase R2-M1. |
| B2 | aplicado bien | `selective_benchmark.py:531–535` (generador por par con CRC32), `:624` (`__best__ = dict(comp[best_ref])`), `:527` (B = 20 000). Comprobado: en los 48 pares (dataset, variante) `__best__` es idéntico a la comparación directa; IC reproducidos bit a bit con mi propia implementación. "NCM 8/0" → `\VsRefNcmBetter`/`\VsRefNcmWorse` = 7/0 (main.tex:214). Viñeta de la nota corregida (CONTINUIDAD:33). |
| M1 | aplicado bien | "equiprobable" en main.tex:51, FICHA:13 y :24, README:35; forma general con término de priors en Prop. 3.1(iii) (main.tex:114) y su prueba (:119); verificación en `lda_identity.py:180–197` (desviación ingenua 3.58, corregida 7.1×10⁻¹⁵). Álgebra comprobada a mano. Menor de notación: R2-m4. |
| M2 | **aplicado a medias** | (1) `results.json` regenerado (log `results/run_log_v02.txt`, 03/10 04:08–04:13 UTC); metadata coherente (`shift`, `shift_at_bound`, nota correcta). Pero el hash de `CRITERIO_HQF001.md:20` es el del script *posterior* a la corrida: `git diff e776acc 2040e2b` muestra +11 líneas en `write_markdown` después de que se escribiera `results.json` (inocuo para los números, pero el registro dice otra cosa). (2) `CRITERIO_HQF001.md` creado; afirma que "no existe un registro fechado independiente anterior a esa corrida" (:13) y que lo único que cambió entre la prueba rápida y la corrida fue la clave de K_m (:15). El historial de git contradice ambas cosas: véase R2-M2. (3) main.tex:162 declara la corrección de la clave de K_m. |
| M3 | aplicado bien | "inconclusive" con V/E/D por macro (main.tex:271); frase de multiplicidad (main.tex:160); p de Wilcoxon en la Tabla 3. Matiz de redacción sobre el optimismo: R2-m2. |
| M4 | aplicado bien (con un defecto de declaración) | `_calibrate_shift` devuelve `(shift, at_bound)` (`selective_benchmark.py:134–150`); espectro `geomspace(2, 0.25, 6)` (:189); JSON `shift = 1.5436`, `shift_at_bound = false`, error de Bayes 9.92 %; reproducido por mí bit a bit (véase Verificación computacional). Tabla 1 y main.tex:151 declaran el cambio y que se hizo tras ver v0.1. No se declara en el manuscrito que se probaron cuatro espectros antes de elegir uno (RESPUESTA:41): R2-M3. |
| M5 | aplicado bien | README:5; FICHA:11, :14, :22, :25 ("Cerrada para la formulación no supervisada evaluada", tres vías); main.tex:51 ("in the precise form reconstructed here"), :275. |
| M6 | aplicado bien | Prop. 3.2(c) (main.tex:127–131) y prueba (:135): verifiqué el álgebra paso a paso (véase R2-m3 para dos imprecisiones de enunciado que no afectan a la identidad). Párrafo reetiquetado "proved here for fixed prototypes / heuristic for local prototypes / design" (:138); Tabla 6 separa la fila demostrada de la heurística (:256–257). |
| m1 | aplicado a medias | 7.1×10⁻¹⁵ y numeración 3.1/3.2 corregidos (CONTINUIDAD:56, `lda_identity.py:2`, `tables_identity.md`). Pero la nota conserva secciones v0.1 sin etiquetar que contradicen el manuscrito v0.2: R2-m8. |
| m2 | aplicado bien | `wilcoxon1945` (refs.bib:90–98) citado en main.tex:160; Demšar solo para los tests entre datasets no realizados. |
| m3 | aplicado bien | `kohonen1995` (refs.bib:81–89), citado en main.tex:56 y :98. |
| m4 | aplicado bien | refs.bib:36–44 (`number = {11}`, diacríticos). |
| m5 | aplicado bien (documentado, no corregido) | main.tex:284. |
| m6 | aplicado bien | `selective_benchmark.py:489–499`; `\DroppedConfigs` = 0 (main.tex:284). |
| m7 | aplicado bien (figura eliminada) | `figures/` ya no contiene `fig_diff_forest.*`. |
| m8 | aplicado bien | `\FloatBarrier` en main.tex:243 y :277; tablas de geometría/exactitud y Figura 4 fuera del PDF; "[computationally verified]" solo en la Tabla 6. |
| m9 | aplicado bien | `table_diff.tex`: wine "[-0.005, +0.10]" con marca ∘. |
| m10 | aplicado bien | 0 macros `AblAnisoKnn/Lda/Dann` en numbers.tex; `.gitignore` ya no excluye `main.bbl`; parche de `make_numbers.py` eliminado. |
| m11 | aplicado bien | main.tex:131; comprobado: con el orden invertido, s_A + s = −2(x−m̄)ᵀ(A−Σ⁻¹)δ. |
| m12 | aplicado bien | main.tex:70. |

Recuento sobre los 20 hallazgos de la ronda 1 (B1, B2, M1–M6, m1–m12): **17 aplicados bien** (M4 con el defecto de declaración remitido a R2-M3; m5 cuenta como bien porque se aceptó solo documentarlo), **2 a medias** (M2, m1), **0 no aplicados**, **1 aplicado con error nuevo** (B1).

## Hallazgos nuevos

Numeración de tablas según el PDF compilado: Tabla 1 datasets, 2 AURC, 3 campo vs mejor referencia, 4 campo vs cada referencia, 5 ablaciones, 6 afirmaciones.

### Bloqueantes

Ninguno. El resultado principal (criterio no cumplido; 0 "mejor" en las tres lecturas) es correcto, se reproduce bit a bit y resiste también una rejilla de hiperparámetros ampliada (R2-M4).

### Mayores

#### R2-M1. La afirmación positiva sobre la anisotropía contradice la regla de "caso límite" del propio manuscrito y omite la tercera lectura

**Ubicación.** main.tex:51 (resumen: "improves on the field's own isotropic ablation on \AblAnisoIsoFirstRange{} [= 2–3] datasets, depending on the interval used, and hurts on \AblAnisoIsoSecondRange{} [= 2]"); :235 ("with a $t$ interval on \AblAnisoIsoFirstT{} [= 2] (wine, digits)"); :260 (Tabla 6); :271 (§6); FICHA:13 y :24; README:32 ("2 con IC t (wine, digits)"); `make_numbers.py:286` (`rng_str(len(fb), len(ft))`: el rango solo usa bootstrap y t).

**Problema.** main.tex:160 fija la regla: "An interval whose end lies within 0.02 (AURC×100) of zero is marked borderline (°) and read as inconclusive". Los pares aniso − iso de iris y wine están marcados ° (Tabla 5; `\AblBorderList`), pero se cuentan como "mejor" en el resumen, en §5.2, en la Tabla 6 y en la ficha. Valores exactos (recalculados de `per_fold`, AURC×100):

| dataset | bootstrap | t | NB | V/E/D | ° |
|---|---|---|---|---|---|
| iris | [−0.558, −0.046] | [−0.575, **+0.009**] | [−0.92, +0.35] | 8/4/3 | sí (por el extremo t) |
| wine | [−0.375, −0.048] | [−0.389, **−0.013**] | [−0.61, +0.21] | 8/5/2 | sí (por el extremo t) |
| digits | [−1.216, −0.407] | [−1.246, −0.320] | [−1.79, +0.23] | 15/0/0 | no |

El IC t de wine termina a 0.013 de cero: por la regla, ese intervalo se lee como no concluyente, de modo que el recuento "con IC t: 2 (wine, digits)" es **1 (digits)** bajo cualquier lectura de la regla (por intervalo o por par). Si la marca ° se aplica al par, como hace el texto para la Tabla 4 ("all of them should be read as inconclusive", main.tex:214), también el recuento bootstrap baja de 3 a 1. Además, "depending on the interval used" omite la tercera lectura que el propio texto da en :235: con Nadeau–Bengio, 0 mejor y 1 peor (`\AblAnisoIsoFirstNB` = 0, `\AblAnisoIsoSecondNB` = 1). El rango coherente con las tres lecturas es "0–3 mejor, 1–2 peor", y el único caso que sobrevive a t y a la regla de límite es digits.

**Corrección.** (1) `make_numbers.py`: calcular `rng_str` sobre las tres lecturas y excluir del recuento los pares con `borderline = True`, o bien imprimir los dos recuentos ("3 / 2 / 0; 1 / 1 / 0 sin los casos límite"). (2) Resumen, sustituir la frase por: "Anisotropy improves on the field's own isotropic ablation on digits (15 of 15 folds) under the bootstrap and $t$ intervals, and on iris and wine only under the bootstrap interval with borderline $t$ intervals; with the Nadeau--Bengio correction it improves on none. It hurts on breast-cancer and synth-classcov (synth-classcov alone under Nadeau--Bengio). Whether the representation is non-empty is therefore suggestive at most." (3) Mismo cambio en :235, :260, :271, FICHA:13/:24 y README:32. (4) Tabla 6, fila 8: "on 1 dataset robustly (digits), up to 3 with the bootstrap interval; 0 with Nadeau–Bengio".

#### R2-M2. El registro de la predefinición es incompleto y en parte inexacto; el historial de git ofrece un registro mejor que el que se declara

**Ubicación.** `CRITERIO_HQF001.md:13` ("No existe un registro fechado independiente anterior a esa corrida"), :15 (lo único que cambió entre la prueba rápida y la corrida fue la clave de K_m), :16 ("no cambió el criterio (umbral, intervalo, …)"), :20 (hash); main.tex:51 ("fixed before the run"), :162.

**Evidencia** (solo comandos de lectura de git):
- El commit `31398e3` (2026-09-30 08:29:24 UTC) ya contiene `experiments/selective_benchmark.py` con el criterio (`majority_needed=len(summary)//2+1`, veredicto de `__best__` por IC bootstrap al 95 %) y **no** contiene `results/results.json`; este aparece por primera vez en `0c3bde3` (08:44:39 UTC). Es un registro fechado independiente, anterior a la corrida de referencia v0.1, que el autor no cita.
- `git diff 31398e3 0c3bde3 -- experiments/selective_benchmark.py`: entre ese registro y la corrida cambiaron `n_repeats` 4 → 3, la rejilla de LogReg {0.01, 0.1, 1, 10, 100} → {0.1, 1, 10} y la de QDA (se quitó `reg_param = 0`, con captura de `LinAlgError`). La clave nominal de K_m ya estaba en `31398e3`. La nota lo atribuye al presupuesto (CONTINUIDAD:29–30), pero `CRITERIO_HQF001.md:15` y main.tex:162 mencionan solo la clave de K_m, y la nota (CONTINUIDAD:32) dice que esa corrección vino de la prueba rápida, cuya salida (script de `31398e3`, `main()`) imprime el veredicto del criterio también en modo `--fast`. Es decir: se vio un veredicto del criterio sobre datos reducidos antes de fijar repeticiones y rejillas. No veo indicio de que esto sesgue la conclusión negativa (rejilla de LogReg más estrecha favorece al campo; menos repeticiones ensancha los IC en ambos sentidos), pero el registro debe decirlo.
- `CRITERIO_HQF001.md:20` da el sha256 del script actual (`ad5322…`), que no es el que produjo `results.json`: `git diff e776acc 2040e2b` añade 11 líneas a `write_markdown` después de la corrida (el script de `e776acc` tiene sha256 `40280a3e…`). Inocuo para los números, inexacto como registro.
- :16 dice que entre v0.1 y v0.2 no cambió "el intervalo"; cambiaron B (2 000 → 20 000) y el sembrado (por par). Es la misma clase de intervalo, no la misma implementación.
- El resumen dice "fixed before the run", pero la corrida reportada es la v0.2, hecha tras ver v0.1 y con un dataset regenerado (R2-M3). El criterio se fijó antes de la **primera** corrida.

**Corrección.** (1) `CRITERIO_HQF001.md`: sustituir :13 por "El registro fechado más antiguo es el commit `31398e3` (30/09/2026 08:29:24 UTC), que contiene el código del criterio y no contiene resultados de la corrida de referencia (que aparecen en `0c3bde3`, 08:44:39 UTC). Antes de ese commit se había ejecutado al menos una prueba rápida (`--fast`, 2×5 pliegues sobre submuestras de 600 puntos), cuya salida incluye el veredicto del criterio sobre esos datos reducidos."; ampliar :15 con "Entre `31398e3` y la corrida de referencia se redujeron las repeticiones de 4 a 3 y las rejillas de LogReg (C ∈ {0.1, 1, 10}) y QDA (sin `reg_param = 0`), por presupuesto de cómputo"; en :16 añadir "B pasó de 2 000 a 20 000 y el generador pasó a sembrarse por par"; en :20 dar el hash del script que corrió (`40280a3e…`, commit `e776acc`) y aparte el del actual. (2) main.tex:162: añadir una frase con lo mismo ("The criterion is recorded in commit 31398e3 … before the reference run; between that record and the run the number of repeats (4→3) and the LogReg and QDA grids were reduced for compute budget."). (3) main.tex:51: "fixed before the first run".

#### R2-M3. El cambio post hoc de synth-classcov está declarado, pero no la búsqueda que lo precedió

**Ubicación.** main.tex:151 ("The dataset was regenerated for version 0.2 … after the v0.1 results had been seen"); RESPUESTA:41 ("probé cuatro espectros menos dispares (coste 4 s de CPU) y elegí `geomspace(2, 0.25, 6)`"); `selective_benchmark.py:182–189`; `CRITERIO_HQF001.md:16`.

**Problema.** El manuscrito declara bien que el dataset cambió después de ver v0.1 y que el veredicto del criterio no depende de ello (comprobado: 0/6/2 en ambas versiones; los otros 7 datasets son idénticos bit a bit). Lo que no declara en ninguna parte del manuscrito ni del registro del criterio es que se probaron cuatro espectros candidatos y con qué regla se eligió uno. Según la respuesta, sobre los candidatos solo se corrió la calibración (4 s de CPU, sin benchmark), lo que haría la elección independiente del resultado; pero eso solo consta en la respuesta, y los candidatos no se listan. Como el dataset regenerado sostiene una afirmación propia (Tabla 6, fila 9: "on synth-classcov … its isotropic and Euclidean ablations beat the full method"), la regla de elección tiene que estar en el manuscrito. Comprobé que el espectro v0.1 da un error de Bayes de 7.8 % con medias coincidentes y toca el límite (`at_bound = True`), y que `geomspace(2, 0.25, 6)` da 20.6 % con medias coincidentes y un desplazamiento calibrado de 1.5436 (idéntico al del JSON).

**Corrección.** main.tex:151, tras "(same rotations and draws)": "The spectrum was chosen among four less disparate candidates [listarlos] by the rule [p. ej. 'the most disparate one for which the calibration has an interior solution'], using only the Bayes-error calibration (no benchmark was run on the candidates)." Añadir lo mismo a `CRITERIO_HQF001.md:16`. Si la regla no fue esa, decir cuál fue.

#### R2-M4. Los hiperparámetros del campo se seleccionan en el borde de la rejilla; las magnitudes y la conclusión sobre synth-classcov dependen de ello

**Ubicación.** main.tex:241 ("the tuning prefers the strongest shrinkage on offer, i.e. a mildly anisotropic field"); rejilla `fgrid = dict(K_m=[20, 40, 80], alpha=[0.05, 0.2, 0.5])` (`selective_benchmark.py:454`); §5.1 (:215, "on synth-classcov anisotropy is a handicap rather than a help"); §6 Limitations (:273, no lo menciona).

**Evidencia.** Selección de (α, K_m) de Field-aniso por pliegue (`results.json → per_fold`): synth-informative, synth-classcov y synth-lda eligen la esquina (0.5, 80) en 15/15 pliegues; breast-cancer α = 0.5 en 15/15; moons-aniso α = 0.5 en 14/15; wine K_m = 80 en 12/15. En 6 de 8 datasets, ≥ 14 de 15 pliegues tocan un borde superior. Para un resultado negativo *sobre el método evaluado* es la objeción obvia: el método no tuvo su mejor oportunidad. Corrí (como análisis de sensibilidad, ajeno al criterio predefinido) Field-aniso con la rejilla K_m ∈ {20, 40, 80, 160, 320}, α ∈ {0.05, 0.2, 0.5, 0.7, 0.9}, mismo protocolo, pliegues y semillas (72 s de CPU en total; `grid_sens.py`):

| dataset | AURC×100 rejilla v0.2 | rejilla ampliada | mejor ref. | Δ ampliada − mejor ref., IC t | V/E/D | selección dominante |
|---|---|---|---|---|---|---|
| synth-classcov | 2.77 | **2.07** | QDA 1.69 | +0.38 [+0.21, +0.55] | 1/0/14 | (0.9, 160) 15/15 |
| synth-lda | 2.83 | **2.24** | LDA 1.58 | +0.66 [+0.46, +0.86] | 0/0/15 | (0.05, 320) 12/15 |
| synth-informative | 4.81 | 4.94 | RF 3.51 | +1.43 [+0.89, +1.97] | 1/0/14 | (0.5, 80) 11/15 |
| breast-cancer | 0.83 | 0.79 | LogReg 0.25 | +0.54 [+0.13, +0.95] | 3/0/12 | (0.5, 160) 7/15 |
| moons-aniso | 1.19 | 1.19 | RF 0.62 | +0.56 [+0.33, +0.80] | 2/0/13 | (0.5, 20) 9/15 |
| wine | 0.08 | 0.13 | QDA 0.03 | +0.10 [+0.01, +0.18] | 3/3/9 | (0.05, 160) 6/15 |

Lectura: (a) el veredicto del criterio **no cambia** (el campo sigue peor que la mejor referencia en los seis datasets); (b) en synth-classcov y synth-lda el AURC del campo baja 25 % y 21 %, y la brecha con QDA/LDA se reduce a menos de la mitad, de modo que las magnitudes de las Tablas 2–3 y la frase "the largest loss" dependen de la rejilla; (c) en synth-classcov el campo casi isótropo con K_m = 160 (2.07) supera a la ablación isótropa limitada a K_m ≤ 80 (2.30), así que "anisotropy is a handicap" en ese dataset compara α ≤ 0.5 con α = 1 bajo un tope de K_m que también limita a la ablación; (d) la selección sigue en el borde nuevo (α = 0.9 en synth-classcov, K_m = 320 en synth-lda); (e) en wine el veredicto "no concluyente" frente a la mejor referencia es frágil: con la rejilla ampliada pasa a "peor" con IC t. Las referencias también saturan su rejilla (k-NN k = 31 en 14/15 en synth-classcov; DANN (100, 21) en 12–14/15 en varios; LogReg en un extremo en 15/15 en iris y moons-aniso), lo que favorece al campo y no amenaza la conclusión negativa.

**Corrección.** (1) Reportar en §5.3 la saturación (fracción de pliegues en el borde por dataset, para el campo y las referencias). (2) Añadir un párrafo de sensibilidad, explícitamente no predefinido, con la rejilla ampliada al menos para el campo y sus ablaciones (iso y Euclid. también con K_m ∈ {160, 320}) y, si el presupuesto lo permite, k-NN y DANN; coste estimado < 3 min de CPU para los ocho datasets. (3) Reescribir main.tex:215 ("on synth-classcov anisotropy is a handicap") y la fila 9 de la Tabla 6 condicionándolas a la rejilla ("with $K_m\le80$"). (4) Añadir a Limitations: "The field's selected hyper-parameters lie on the edge of the grid in most folds of six datasets; a wider grid lowers its AURC by about a fifth on synth-classcov and synth-lda without changing any verdict against the best reference".

#### R2-M5. Las puntuaciones geométricas no son "casi no informativas": la ficha y la Tabla 6 contradicen los números

**Ubicación.** main.tex:262 (Tabla 6: "Geometry-only scores (volume, anisotropy) are close to uninformative"); FICHA:13 ("están al nivel del azar o por debajo") y :24 ("are at or below chance level"); README:34 ("Las puntuaciones puramente geométricas no informan").

**Evidencia** (`results.json → summary`; cociente AURC / tasa de error del propio clasificador, que es el AURC esperado de un orden aleatorio): log-volumen 0.37 (iris), 0.25 (wine), 0.30 (digits), 0.51 (moons-aniso), 0.71 (breast-cancer); anisotropía 0.28 (wine), 0.66 (breast-cancer), 0.67 (digits). En digits el log-volumen da AURC×100 0.66, mejor que LDA (1.54), QDA (1.80), NCM (2.97) y similar a LogReg (0.64). Solo en synth-informative, synth-classcov y synth-lda (volumen) y en cinco datasets (anisotropía) el cociente supera 1. El cuerpo (main.tex:239) lo dice bien ("far from the margin"); las frases resumidas no. Además, "worse than a random ordering" se afirma sobre medias sin intervalo (moons-aniso 0.51 frente al umbral 0.5 cuenta como "above half").

**Corrección.** Tabla 6: "Geometry-only scores are far weaker than the margin; the log-volume is informative on iris, wine and digits (AURC at 25–37 % of the random level) and worse than random on the three Gaussian/`make_classification` problems". FICHA ES: "Las puntuaciones puramente geométricas (volumen, anisotropía) son muy inferiores al margen: el log-volumen informa en iris, wine y digits y es peor que el azar en los tres sintéticos gaussianos; la anisotropía es peor que el azar en cinco de ocho". Ídem EN y README:34. En main.tex:239, añadir "(point estimates, no interval)".

### Menores

- **R2-m1. Prop. 3.2(b), afirmación falsa (ya estaba en v0.1, el primer árbitro no la vio).** main.tex:127: "the ordering changes as soon as $\lambda$ is non-constant". Falso: si λ(x) = f(s(x)) con f > 0 creciente (p. ej. λ = s), λs es creciente en s y el orden no cambia. Sustituir por: "the ordering can change when $\lambda$ is non-constant: two points with $s(x)<s(x')$ swap order if and only if $\lambda(x)/\lambda(x')>s(x')/s(x)$." (El ejemplo de `lda_identity.py:215–227` construye un λ concreto; no prueba el "as soon as").
- **R2-m2. Lógica del optimismo de los IC.** main.tex:160 ("This optimism cannot create a 'better' verdict where there is none") y :273 ("neither can produce a 'better' verdict for the field"). Un intervalo demasiado estrecho sí puede producir veredictos "mejor" espurios; lo que es cierto es que aquí no produjo ninguno, de modo que la conclusión no depende de él. Sustituir por: "Since even these optimistic intervals give no 'better' verdict, the conclusion that the criterion is unmet does not depend on their optimism; the optimism does inflate every 'worse' verdict and every positive ablation count, which we therefore also report with the $t$ interval and the Nadeau–Bengio correction." En :273, "neither produced a 'better' verdict here".
- **R2-m3. Precisión del enunciado de la Prop. 3.2.** (i) En (c) basta que el mismo par, en el mismo orden, sea el más próximo en las configuraciones (Σ⁻¹, μ) y (A, ν); la tercera, (A, μ), solo hace falta para leer el primer término como s_A − s. Escribir: "…is nearest under $(\Sig^{-1},\mu)$ and under $(A(x),\nu)$ (and, for the first term to equal $s_A-s$, under $(A(x),\mu)$)". (ii) En (a), "components of the metric orthogonal to δ cannot change the score" es impreciso: la condición es $(A-\Sig^{-1})\delta=0$; un término cruzado $vw^{\top}+wv^{\top}$ con $v\perp\delta$, $w\parallel\delta$ sí cambia la puntuación. Escribir "metric perturbations with $\delta$ in their kernel cannot change the score". (iii) main.tex:138 usa $\hat\Sig^{-1}$ al resumir la Prop. 3.2(a), enunciada con $\Sig^{-1}$ verdadera; unificar.
- **R2-m4. Notación $\pi_{(1)}$ en Prop. 3.1(iii)** (main.tex:114). Se lee como estadístico de orden de los priors; es el prior de la clase con mayor posterior. Escribir $\pi_{c_1}$, $\pi_{c_2}$ con $c_1,c_2$ las clases de $p_{(1)},p_{(2)}$.
- **R2-m5. synth-lda no es un control "donde no hay ganancia posible" por la Prop. 3.1.** main.tex:138 ("one shared-covariance control where no gain is possible"); CONTINUIDAD:27 ("control donde por la Proposición 3.1 no puede haber ganancia"). synth-lda tiene K = 3, y la Prop. 3.1(iii) muestra justamente que s no ordena como el máximo posterior. Lo que impide la ganancia es la optimalidad del orden por máximo posterior verdadero (Chow 1970), no la Prop. 3.1(i), que es K = 2. Añadir: "(for $K=3$ by the optimality of the true maximum-posterior ordering~\citep{chow1970}, not by Proposition 3.1(i))".
- **R2-m6. Número tecleado y erróneo en el Apéndice.** main.tex:284: "On iris, $K_m=80$ of 96 inner training points". La CV interna es de 3 pliegues (`selective_benchmark.py:471`) sobre 120 puntos: los conjuntos internos de entrenamiento tienen **80** puntos y K_m = 80 se recorta a 79 (`:381`), es decir, la covarianza "local" interna es la global. Además el mismo cambio de régimen afecta a wine (≈ 95 puntos internos), que es donde K_m = 80 se elige en 12/15 pliegues; iris elige K_m = 40 en 13/15. Corregir: "On iris and wine, $K_m=80$ is capped at 79 of the 80 (iris) or about 95 (wine) inner training points…". Relacionado: main.tex:60 dice "Every number in the text is … injected as a generated macro; none is typed", pero hay parámetros de diseño tecleados (este, 0.30/0.06, 30°, [0.05, 20], 40 pasos, 40 000 puntos, K_m y α de la Figura 1, 0.02). Escribir "Every result in the text…".
- **R2-m7. Contraejemplo con precisión inconsistente.** `\CexDtwoA` = "0.5625, 1.562, 4.062" y `\CexDtwoB` = "0.8125, 1.812, 2.312" (main.tex:119): los valores exactos son 0.5625, 1.5625, 4.0625 y 0.8125, 1.8125, 2.3125; "1.562" sugiere un número distinto. Imprimir con cuatro decimales.
- **R2-m8. "Inconclusive only on …" omite la lectura NB.** main.tex:271: "inconclusive only on wine, digits with the bootstrap interval … plus iris with the $t$ interval". Con Nadeau–Bengio también breast-cancer y synth-informative (`\CritFanisoInconListNB`). Añadir "and also on breast-cancer and synth-informative with the Nadeau–Bengio correction".
- **R2-m9. Nota de continuidad con secciones v0.1 sin etiquetar que contradicen v0.2.** CONTINUIDAD:36–56 ("Resultados de referencia", 449 s, IC con B = 2 000, synth-classcov +0.43), :61–67 ("Limitaciones (explícitas en el manuscrito)": "ambos sesgos favorecen encontrar una ganancia, así que refuerzan la conclusión negativa", justo lo que B1 refutó; "synth-classcov con medias coincidentes"), :20–24 (11 páginas, 24 entradas, 4 figuras), :28 (synth-classcov "no se corrigió ni se recorrió"). Titular esas secciones "(v0.1, 30/09/2026; superado por v0.2)" o actualizarlas. Tiempo de la ronda: CONTINUIDAD:125 dice 5.1 min y RESPUESTA:97 5.6 min; unificar.
- **R2-m10. Resumen más largo de lo declarado.** RESPUESTA:75 dice ≈ 240 palabras; el resumen compilado tiene ≈ 300. Sobra la frase de la fórmula de desviación (ya en la Prop. 3.2) y la frase "The formulation is computational…" (ya en §1).
- **R2-m11. Orden no determinista en macros de texto.** Regenerando con `make_numbers.py` sobre el mismo JSON, `\AblAnisoEuclidWinsText` y `\AblAnisoGprotoWinsText` salen con los empates (15/0/0) en otro orden que el de `numbers.tex` versionado. No se usan en el PDF; ordenar con clave secundaria (nombre del dataset) para que la regeneración sea idéntica byte a byte.

### Extensión y presentación

El PDF recompilado tiene 10 páginas con apéndice y referencias (p. 1–8 cuerpo, p. 9 Tabla 6, apéndice y comienzo de referencias, p. 10 referencias), dentro del límite: no hacen falta recortes. Dos ajustes de presentación: la Tabla 6 flota a la p. 9, después del texto que la comenta (p. 8); con `[t]` o `\FloatBarrier` antes de "Table 6 lists…" quedaría junto a su discusión. El resumen (≈ 300 palabras) puede bajar a ≈ 230 (R2-m10) y ganaría espacio para el párrafo de sensibilidad de R2-M4 sin pasar de 10 páginas.

## Bibliografía

Red: la búsqueda web funcionó; no intenté Crossref ni arXiv directamente (el árbitro de la ronda 1 los encontró bloqueados por el proxy). 26 entradas en `refs.bib`, 26 citadas, ninguna huérfana; BibTeX sin avisos.

| entrada | estado | corrección / nota |
|---|---|---|
| kohonen1995 (nueva) | verificada | Springer Series in Information Sciences 30, 1995 (Springer, Berlin/Heidelberg); contiene el capítulo de LVQ, así que respalda el uso. Sin cambios. |
| wilcoxon1945 (nueva) | verificada | *Biometrics Bulletin* 1(6):80–83, 1945. Sin cambios. |
| franc2023 (corregida en ronda 1) | correcta | JMLR 24(11):1–49 (verificada por el árbitro 1; la corrección está aplicada). |
| nadeau2003 | verificada | *Machine Learning* 52(3):239–281, 2003, doi:10.1023/A:1024068626366. **Respaldo parcial:** la corrección (1/J + n_test/n_train) se dedujo para J particiones aleatorias independientes; su uso con validación cruzada repetida (J = r·k = 15) es el "corrected repeated k-fold cv test" de Bouckaert y Frank. Añadir `bouckaert2004` y citarlo en main.tex:160 junto a nadeau2003. |
| bouckaert2004 (propuesta) | verificada | R. R. Bouckaert y E. Frank, "Evaluating the replicability of significance tests for comparing learning algorithms", en *Advances in Knowledge Discovery and Data Mining (PAKDD 2004)*, LNCS 3056, Springer, pp. 3–12, doi:10.1007/978-3-540-24775-3_3. |
| geifman2017 | verificada; incompleta | NeurIPS 2017 (NIPS 30), pp. 4878–4887. Añadir `volume = {30}`, `pages = {4878--4887}`. |
| ledoit2004 | verificada | *J. Multivariate Analysis* 88(2):365–411, 2004. Sin cambios. |
| street1993, kohonen1990, geifman2019, elyaniv2010, chow1970 | verificadas en la ronda 1 | Sin cambios. |
| hendrycks2017, hastie1996, fisher1936, cover1967, tibshirani2002, breiman2001, weinberger2009, hastie2009, efron1993, dietterich1998, demsar2006, pedregosa2011, harris2020, virtanen2020, hunter2007 | no verificadas en red en esta sesión | Los datos coinciden con los canónicos que conozco (volumen, número y páginas plausibles para cada una); sin discrepancias detectadas. Siguen pendientes de cotejo en red. |

Uso de las citas: correcto en general. chow1970 respalda además el argumento que propongo en R2-m5 (optimalidad del rechazo por máximo posterior). demsar2006 se cita ahora para lo que no se hace, que es un uso correcto.

## Verificación computacional

Todo desde una copia en el scratchpad (`referee2_HQF001/copy/`); nada se escribió en la carpeta del autor salvo este informe. Entorno: Python 3.11.15, NumPy 2.4.6, SciPy 1.17.1, scikit-learn 1.9.1 (el declarado).

| qué | CPU | resultado |
|---|---|---|
| Recalcular desde `per_fold` todas las estadísticas por par con una implementación propia (media, bootstrap con el mismo generador por par, t, NB, V/E/D, veredictos) para los 336 pares campo–referencia y los 56 de ablación; comprobar que `__best__` = comparación directa y que la mejor referencia es la de menor media | ≈ 1 s | **Desviación máxima 0** en todos los valores; 0 discrepancias de veredicto; `__best__` idéntico a la directa en 48/48 |
| `results_v01.json` frente a `results.json`, 7 datasets no modificados | < 1 s | 1365/1365 AURC por pliegue y parámetros seleccionados idénticos; `results_v01.json` es byte a byte el `results.json` versionado en `b632e86` |
| Macros `\VOne…` de synth-classcov (v0.1) | < 1 s | Coinciden (AURC, errores, Δ, IC t, V/E/D) |
| Reproducción del protocolo **completo** (3×5 pliegues, CV interna, 13 métodos) en synth-classcov (dataset regenerado), synth-lda (comprueba "mismo consumo del RNG") e iris | 98.8 s (generación 3.9; classcov 36.5; lda 39.1; iris 19.3) | **585/585 AURC por pliegue idénticos (diferencia 0.0) y 585/585 configuraciones seleccionadas idénticas**; desplazamientos 1.5436 / 1.2021 y errores de Bayes 9.92 % / 9.84 % idénticos al JSON |
| Calibración con el espectro v0.1 y con el v0.2 | 3.9 s | v0.1: error 7.8 % con medias coincidentes, `at_bound = True`; v0.2: 20.6 % con medias coincidentes, desplazamiento 1.5436, `at_bound = False` |
| Sensibilidad a la rejilla del campo (K_m hasta 320, α hasta 0.9) en 6 datasets | 72.3 s | Véase R2-M4: el veredicto no cambia; el AURC baja 25 % (synth-classcov) y 21 % (synth-lda) |
| `make_numbers.py` sobre el JSON | ≈ 2 s | Las 8 tablas generadas son idénticas byte a byte a las versionadas; `numbers.tex` difiere solo en el orden de los empates de dos macros sin uso (R2-m11) |
| Compilación (`latexmk -pdf`) de una copia | 2.5 s | 10 páginas; 0 referencias o citas indefinidas; 0 "??" en `pdftotext`; 0 cajas desbordadas; BibTeX sin avisos; el texto del PDF compilado coincide con el `main.pdf` versionado (diff vacío) |
| Prop. 3.1(iii) (contraejemplo), Prop. 3.2 y 3.2(c), regla del orden invertido | a mano | Álgebra correcta; d² del contraejemplo (0.5625, 1.5625, 4.0625) y (0.8125, 1.8125, 2.3125), m = 0.221/0.189, MSP = 0.562/0.481 recalculados. Error en el enunciado de 3.2(b): R2-m1 |
| Historial de git (solo lectura: `log`, `show`, `diff`, `ls-tree`) | — | Véase R2-M2 |
| **Total** | **≈ 185 s** | Dentro del presupuesto de 5 min. No repetí la corrida completa (284.5 s declarados): la reproducción exacta de 3 datasets, incluido el regenerado, más la identidad bit a bit de los otros 7 con v0.1 (ya reproducida por el árbitro 1) es un control más fuerte por segundo de CPU. |

## Lista de acciones (por prioridad)

1. Rehaz la afirmación sobre aniso − iso en resumen, §5.2, §6, Tabla 6, FICHA y README con las tres lecturas y aplicando la regla de casos límite: digits es el único caso robusto; iris y wine solo con bootstrap y con IC t límite; ninguno con NB. Cambia `rng_str` en `make_numbers.py` para que use las tres lecturas y excluya o separe los pares límite (R2-M1).
2. Corrige `CRITERIO_HQF001.md` y main.tex:162: cita el commit `31398e3` como registro fechado anterior a la corrida, declara la prueba rápida previa y los cambios de repeticiones (4→3) y de rejillas de LogReg y QDA, el cambio de B y de sembrado, y da el hash del script que corrió; en el resumen escribe "fixed before the first run" (R2-M2).
3. Declara en main.tex:151 y en `CRITERIO_HQF001.md` los cuatro espectros candidatos de synth-classcov y la regla con que se eligió uno, y que solo se calibraron (R2-M3).
4. Reporta la saturación de la rejilla del campo y de las referencias y añade un análisis de sensibilidad, explícitamente no predefinido, con K_m ∈ {…, 160, 320} y α ∈ {…, 0.7, 0.9} para el campo y sus ablaciones; condiciona a la rejilla la frase "on synth-classcov anisotropy is a handicap" y la fila 9 de la Tabla 6; añádelo a Limitations (R2-M4).
5. Corrige "close to uninformative" (Tabla 6), "al nivel del azar o por debajo" / "at or below chance level" (FICHA) y "no informan" (README): el log-volumen informa en iris, wine y digits (R2-M5).
6. Corrige el enunciado de la Prop. 3.2(b) ("can change", con la condición si y solo si) (R2-m1).
7. Reescribe la frase sobre el optimismo de los IC en main.tex:160 y :273 (R2-m2).
8. Precisa la Prop. 3.2: configuraciones necesarias en (c), condición de núcleo en (a), Σ frente a Σ̂ en :138; usa π_{c_1}, π_{c_2} en la Prop. 3.1(iii) (R2-m3, R2-m4).
9. Justifica synth-lda como control "sin ganancia posible" por la optimalidad del máximo posterior verdadero, no por la Prop. 3.1(i) (R2-m5).
10. Corrige "K_m = 80 of 96 inner training points" (son 80, recortado a 79) y extiende la observación a wine; cambia "Every number" por "Every result" en main.tex:60 (R2-m6).
11. Imprime el contraejemplo con cuatro decimales; añade la lectura NB a la frase "inconclusive only on…" de main.tex:271 (R2-m7, R2-m8).
12. Etiqueta como v0.1 o actualiza las secciones obsoletas de la nota de continuidad; unifica el tiempo de la ronda (R2-m9).
13. Recorta el resumen a ≈ 230 palabras; ordena los empates en `make_numbers.py` con clave secundaria (R2-m10, R2-m11).
14. Añade `bouckaert2004` y cítalo junto a nadeau2003; completa volumen y páginas de geifman2017.
