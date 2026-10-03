# Informe de árbitro interno — HQF001, ronda 1 (30/09/2026)

Objeto: borrador v0.1 "Local Resolution and Abstention: A Controlled Comparison of Anisotropic Resolution Fields with Local-Metric and Prototype Baselines under a Predefined Criterion" (manuscript/main.tex, 11 páginas), código en experiments/, resultados en results/, README, nota de continuidad y ficha propuesta. Archivos de trabajo del árbitro en el scratchpad (`referee_HQF001/`: `verif_math_stats.txt`, `verif_best_vs_direct.txt`, `verif_resummarise_shift.txt`, `repro/repro_log.txt`, `build/manuscript/main.log`). No se modificó ningún archivo del autor.

## Veredicto

**Cambios mayores.** El resultado principal (criterio predefinido no cumplido: 0 de 8 datasets mejor que la mejor referencia) es correcto, reproducible bit a bit y sobrevive a cualquier lectura conservadora; pero las afirmaciones *positivas* que lo acompañan en resumen, Tabla 9 y ficha ("la anisotropía añade información en 3 datasets", "peor en 6", recuentos de la Tabla 5) descansan en intervalos bootstrap percentil sobre 15 pliegues dependientes con B = 2000 y no sobreviven a un intervalo t ni, menos aún, a la corrección de Nadeau–Bengio; además persiste exactamente el defecto que la nota de continuidad declara corregido (dos IC distintos para el mismo par), y el resumen y la ficha enuncian la identidad para K ≥ 3 sin la hipótesis de priors iguales.

Recuento: 2 bloqueantes, 6 mayores, 12 menores.

---

## Hallazgos bloqueantes

### B1. Las afirmaciones positivas no sobreviven a una lectura conservadora de los intervalos; el texto afirma lo contrario

**Ubicación.** main.tex:50 (resumen: "Anisotropy adds information relative to the field's own isotropic ablation on 3 datasets and removes it on 2"; "significantly worse on 6"); main.tex:161 ("this works *against* a negative conclusion, not for it"); main.tex:220, 236, 254, 328, 330 ("both caveats make the negative result conservative"); Tabla 9 filas 7–8; FICHA_HQF001_propuesta.md:13 y :24; README.md ("La anisotropía sí añade información…").

**Problema.** Los IC son percentiles bootstrap (selective_benchmark.py:494–499) de la media de 15 diferencias pareadas procedentes de 3×5 pliegues repetidos (cada punto de prueba aparece 3 veces; los conjuntos de entrenamiento se solapan en ~80 %). El manuscrito reconoce el optimismo (líneas 161 y 330) pero sostiene que solo perjudica a la conclusión negativa. Eso es cierto para el recuento "mejor" del criterio (0 de 8 no puede bajar), y **falso para todo lo demás que se afirma**: "peor con IC que excluye 0 en 6", "la anisotropía mejora a la ablación isótropa en 3 datasets", y los recuentos "NCM 8/0, LDA 4/3, …" de la Tabla 5 son afirmaciones positivas inflados por el mismo optimismo.

**Evidencia** (recalculado desde `results.json → per_fold`, script en `verif_math_stats.txt`, sección D3; columnas: bootstrap almacenado | intervalo t (14 g.l.) | t corregido Nadeau–Bengio con ρ = n_test/n_train = 1/4):

| comparación | boot. B=2000 (publicado) | IC t | IC t Nadeau–Bengio | victorias/empates/derrotas |
|---|---|---|---|---|
| iris: campo − mejor ref. (LDA) | +0.20 [+0.04, +0.43] **peor** | [−0.03, +0.43] no concl. | [−0.30, +0.70] no concl. | 1/6/8 |
| breast-cancer: campo − LogReg | +0.58 [+0.35, +0.90] peor | [+0.26, +0.90] peor | [−0.11, +1.27] no concl. | 0/0/15 |
| synth-informative: campo − RForest | +1.30 [+0.76, +1.87] peor | [+0.69, +1.92] peor | [−0.03, +2.64] no concl. | 2/0/13 |
| iris: aniso − iso | −0.28 [−0.54, −0.05] **mejor** | [−0.58, +0.01] no concl. | [−0.92, +0.35] no concl. | 8/4/3 |
| wine: aniso − iso | −0.20 [−0.37, −0.05] mejor | [−0.39, −0.01] mejor | [−0.61, +0.21] no concl. | 8/5/2 |
| digits: aniso − iso | −0.78 [−1.19, −0.43] mejor | [−1.25, −0.32] mejor | [−1.79, +0.23] no concl. | 15/0/0 |
| breast-cancer: aniso − iso | +0.37 [+0.19, +0.59] peor | [+0.14, +0.61] peor | [−0.14, +0.89] no concl. | 1/0/14 |

Resumen de veredictos que cambian: con IC t cambian 9 de 72 (todos de "significativo" a "no concluyente"); con Nadeau–Bengio, 22 de 72. En concreto:
- Criterio (campo vs mejor referencia): publicado 0 mejor / 6 peor / 2 no concl. → con IC t: 0 / **5** / 3 (iris pasa a no concluyente) → con NB: 0 / **3** / 5. "No cumplido" en los tres casos.
- Ablación aniso − iso: publicado 3 mejor / 2 peor → con IC t: **2** (wine, digits) / 2 → con NB: **0** / 1. La frase del resumen y de la ficha "añade información en 3 datasets" depende del método de intervalo.
- Tabla 5 (campo vs cada referencia), recuentos mejor/peor con IC t: k-NN 1/1, NCM 7/0, LDA 4/2, QDA 3/2, LogReg 4/2, RForest 3/2, DANN 1/2 (publicado: 2/2, 8/0, 4/3, 3/3, 4/2, 3/2, 2/3).
- En iris y wine los pliegues de prueba tienen 30 y 35 puntos; la mejor referencia tiene AURC exactamente 0 en 8/15 (iris) y 10/15 (wine) pliegues; hay 6 y 4 empates exactos. "Significativamente peor en iris" descansa en 8 derrotas, 1 victoria y 6 empates con diferencias de 0–2 errores.

**Corrección propuesta.**
1. En main.tex:161 y :330 sustituir la frase "this works against a negative conclusion, not for it" por: "This optimism cannot create a 'better' verdict where there is none, so the criterion count is conservative; it does inflate every 'significantly worse' and every positive ablation count below, which we therefore also report with a Student-t interval over folds and, as an extreme, with the Nadeau–Bengio corrected variance."
2. Añadir a la Tabla 4 y a la Tabla 6 una columna con el IC t (o sustituir el bootstrap por el IC t; con n = 15 y empates, el percentil bootstrap no es más fiable que el t), y reportar victorias/empates/derrotas (hoy los empates se pierden en "wins").
3. Reescribir la afirmación positiva del resumen (main.tex:50), de la Tabla 9 (fila 8), de la Sección 6 (main.tex:328) y de la ficha (FICHA:13, :24) así: "Anisotropy improves on the field's own isotropic ablation on 2–3 datasets depending on the interval used (15/15 fold wins on digits, 8/15 on wine and iris) and hurts on 1–2; the evidence that the representation is non-empty is therefore suggestive, not established."
4. Cambiar "significantly worse on 6" por "worse with a 95 % bootstrap interval excluding zero on 6 (5 with a t-interval)".

### B2. El mismo par se sigue reportando con dos IC distintos, y la nota describe mal el efecto del `--resummarise`

**Ubicación.** selective_benchmark.py:537–548 (bucle `for r in refs + ["__best__"]`: la comparación `__best__` y la comparación directa con esa misma referencia se remuestrean por separado, con distinto ruido Monte Carlo); CONTINUIDAD, sección "Decisiones tomadas", viñeta "Estadísticas recalculadas sin recorrer el benchmark"; main.tex:236 (recuentos "k-NN 2/2, NCM 8/0, …"); make_numbers.py:122–127 (Tabla 4 toma `__best__`) y :221–230 (Tabla 5 y macros `\Vs*` toman la directa).

**Problema y evidencia.**
- `verif_best_vs_direct.txt`: en 43 de 48 pares (dataset, variante) los extremos del IC de `__best__` y los de la comparación directa con la misma referencia difieren a dos decimales. Ejemplos de la variante principal: breast-cancer vs LogReg, Tabla 4 [+0.35, +0.90] frente a macro `\VsBcLogreg` [+0.33, +0.88]; synth-informative vs RForest [+0.76, +1.87] frente a [+0.76, +1.84]; synth-lda vs LDA [+1.04, +1.50] frente a [+1.03, +1.51]. En el PDF no se ve porque la Tabla 5 imprime solo medias, pero `results.json`, `tables.md` y las macros llevan dos IC para un mismo par; es exactamente el defecto que la nota declara corregido.
- Emulando el orden original de consumo del RNG (antes del `--resummarise`; script en `verif_math_stats.txt`, D2): los extremos de IC cambian con mediana 0.014, percentil 90 = 0.079 y **máximo 0.25** (AURC×100); 84 de 464 extremos cambian más de 0.05 (la nota dice "0.01–0.05"). Cambian **4 veredictos** de comparaciones individuales: breast-cancer campo vs k-NN (no concl. → peor), breast-cancer campo vs NCM (no concl. → mejor), breast-cancer iso vs k-NN (mejor → no concl.), synth-informative anisotropía vs LogReg (no concl. → mejor). Con B = 200 000, breast-cancer campo vs NCM vuelve a "no concluyente": el recuento "NCM 8/0" de main.tex:236 depende del sorteo; debería ser "7/0 más un caso límite".
- Los veredictos del **criterio** no cambian en ninguna de las variantes (eso sí es cierto).

**Corrección propuesta.**
1. En `summarise`, después del bucle sobre `refs`, hacer `comp["__best__"] = dict(comp[best_ref])` en vez de remuestrear de nuevo (una línea), y subir `B` a 20 000 o más (coste < 10 s). Alternativamente, sembrar el RNG por par (`default_rng(hash((ds, m, r)))`) para que el IC de un par no dependa del orden de evaluación.
2. Re-ejecutar `--resummarise`, regenerar macros y tablas, y en main.tex:236 sustituir "NCM 8/0" por lo que resulte, señalando como límite todo intervalo cuyo extremo esté a < 0.02 de cero (hoy lo son también wine vs mejor referencia [−0.005, +0.10], breast-cancer vs NCM [−0.65, −0.00] y moons aniso − iso [−0.10, +0.00]; el manuscrito solo marca breast-cancer vs k-NN).
3. En la nota, reescribir la viñeta: "los extremos se movieron hasta 0.25 (mediana 0.014) y cambiaron 4 veredictos de comparaciones individuales (ninguno del criterio)".

---

## Hallazgos mayores

### M1. El resumen, la ficha y el README enuncian la identidad para K ≥ 3 sin la hipótesis de priors iguales

**Ubicación.** main.tex:50 ("is equal to twice the log-ratio of the two largest posteriors for any number of classes"); FICHA:13 ("para cualquier número de clases") y :24 ("for any number of classes"); README.md:33 ("Con K ≥ 3, s = 2 log(p₍₁₎/p₍₂₎)"). La Proposición 3.1(iii) (main.tex:113) sí dice "and the priors are equal".
**Evidencia.** `verif_math_stats.txt` (iii'): con priors (0.6, 0.3, 0.1) la desviación máxima |s − 2 log(p₍₁₎/p₍₂₎)| sobre 500 casos aleatorios es 3.58 (no 10⁻¹⁵). La identidad exige priors iguales (o el margen corregido por priors, como en (ii)).
**Corrección.** En los tres textos: "equals twice the log-ratio of the two largest posteriors for any number of **equiprobable** classes". Opcional: añadir a 3.1(iii) la versión general s = 2 log(p₍₁₎/p₍₂₎) − 2 log(π₍₁₎/π₍₂₎) cuando las dos clases más próximas coinciden con las de mayor posterior, que es inmediata de la misma prueba.

### M2. No hay registro fechado del criterio previo a la corrida, y `results.json` fue producido por una versión anterior del script

**Ubicación.** selective_benchmark.py:566–576 (criterio codificado como `len(better) >= n//2 + 1`); results.json → `meta.resummarised`, `datasets.*.shift = null`, `datasets.synth_classcov.note = "mean shift calibrated so Bayes error = 10%"`; make_numbers.py:91–100 (parche que vuelve a ejecutar `make_datasets` porque el JSON no trae `shift`); CONTINUIDAD, "Decisiones tomadas" (corrección de la clave K_m "detectada en la prueba rápida y corregida antes de la corrida de referencia").
**Problema.** El manuscrito dice "fixed before the run" (main.tex:50, :163). La única evidencia es la afirmación de la nota. El código actual difiere del que produjo `results.json` en al menos tres puntos (exporta `shift`, cambia la nota del dataset, añade `--resummarise`), y el resumen estadístico fue recalculado a posteriori. **No encontré indicio de que el umbral del criterio haya cambiado**: el criterio está en la misma función desde la que se escribe el JSON, el JSON almacena `majority_needed = 5`, los datos por pliegue son idénticos a una corrida fresca (B.3 abajo: 585 valores bit a bit) y el generador no cambió (errores de Bayes replicados bit a bit). Pero la metadata del JSON afirma algo falso ("calibrated so Bayes error = 10 %"; el real es 7.7 %).
**Corrección.** (1) Regenerar `results.json` con el script actual (449 s) para que metadata y código coincidan, o declarar en el Apéndice A que el resumen fue recalculado y que la metadata de datasets es de la versión anterior. (2) Añadir un archivo `CRITERIO_HQF001.md` fechado (o la línea exacta del commit/sesión) con el criterio y su hash, y citarlo en main.tex:163. (3) Decir en main.tex:163 que la clave de hiperparámetros se corrigió entre la prueba rápida y la corrida de referencia (hoy solo está en la nota y en el Apéndice sin fecha).

### M3. Lenguaje inferencial excesivo y comparaciones múltiples sin corrección

**Ubicación.** main.tex:220 ("significantly better/worse"), :236, :254, :328 ("The field is statistically indistinguishable from the best reference only on wine and digits"); Tablas 5 y 6 (56 + 48 intervalos; además 48 en Tabla 4 y 6 variantes).
**Problema.** "Statistically indistinguishable" es una lectura incorrecta de "no concluyente": en wine el IC es [−0.005, +0.10] con 7 derrotas y 4 victorias (apunta a ligeramente peor). Los recuentos de las Tablas 5–6 son 104 intervalos al 95 % sin corrección; el texto los usa como "significativo". Con n = 15 y empates, un IC percentil bootstrap no tiene cobertura nominal.
**Corrección.** Sustituir "significantly" por "with a 95 % interval excluding zero" en todo el texto; en main.tex:328 escribir "inconclusive (wine: 4 wins, 4 ties, 7 losses; digits: 7/0/8)"; añadir una frase en la Sección 4 ("no multiplicity correction is applied; the per-reference counts are descriptive"); y mover el p de Wilcoxon de "secondary check" a la tabla si se mantiene.

### M4. synth-classcov: la calibración falló y vuelve vacías tres de las "victorias" del campo

**Ubicación.** selective_benchmark.py:119–129 (`_calibrate_shift`, intervalo [0.05, 20]) y :161–178; main.tex:152 ("This was not intended but is kept"), :236 ("The field does beat the global-prototype methods … where their linear boundaries are wrong (synth-classcov, …)"), Tabla 9 fila 9; Tabla 1 ("rotated class-specific covariances", sin mencionar medias coincidentes); results.json nota del dataset ("calibrated so Bayes error = 10 %").
**Problema.** Con desplazamiento 0.05 y covarianzas rotadas con autovalores 2…0.05, el error de Bayes es 7.7 % y las medias coinciden a efectos prácticos. NCM, LDA y LogReg tienen por construcción error ≈ 48 % (AURC 48.4): "el campo vence a NCM/LDA/LogReg en synth-classcov" (Δ ≈ −47) no es un hallazgo sino una consecuencia del diseño, y así debe decirse o eliminarse. La bisección está mal planteada para este caso: si e(lo) < target la respuesta correcta es "no hay solución en el intervalo", no devolver el extremo. El manuscrito lo documenta honestamente (main.tex:152), pero la Tabla 1, la nota del JSON y la frase de main.tex:236 no.
**Corrección.** (1) Correr la variante con desplazamiento no nulo (p. ej. fijar el target en 10 % partiendo de covarianzas con autovalores menos dispares, o simplemente desplazamiento 1.0): coste ≈ 56 s de CPU; es la única pieza que falta para que el "régimen QDA" esté representado como se diseñó. (2) Mientras tanto: en Tabla 1 escribir "two Gaussians, d = 6, rotated class-specific covariances, **coinciding means** (Bayes 7.7 %)"; en main.tex:236 y Tabla 9 quitar NCM/LDA/LogReg de la lista de referencias vencidas en synth-classcov o añadir "trivially, since their boundaries are linear and the means coincide"; en `_calibrate_shift` devolver también un indicador de "límite alcanzado" y guardarlo en el JSON.

### M5. Alcance: README y ficha "cierran" la línea más de lo que el cuerpo autoriza

**Ubicación.** README.md:5 ("la línea queda cerrada con números"); FICHA:10 y :21 ("Estado: Cerrada"), :14 y :25 ("La única vía abierta es una versión supervisada del campo o una regla bidimensional margen + volumen"); main.tex:332 ("Absent these, the line is closed").
**Problema.** La nota de continuidad admite que la definición del campo es una reconstrucción no confirmada por el autor (supuestos 1–3) y lista alternativas no corridas (información de Fisher, campo aprendido, covarianza intra-clase); el propio manuscrito (main.tex:332) da **tres** vías (a)–(c), no dos; y el resultado es "esta formulación, en estos ocho datasets". "La única vía abierta" y "Cerrada" sin calificativo son sobreafirmaciones. También el resumen dice "the question the line left open is answered in the negative" cuando lo contestado es la versión reconstruida de la pregunta.
**Corrección.** README:5 → "la formulación reconstruida queda descartada con números; la línea se propone cerrar salvo las tres vías del §6". FICHA estado → "Cerrada para la formulación no supervisada evaluada — resultado negativo con criterio predefinido (borrador v0.1)". FICHA alcance → "Vías no exploradas: campo supervisado (intra-clase/Fisher), regla bidimensional margen + volumen, alta dimensión". Resumen (main.tex:50) → "the question, in the precise form reconstructed here, is answered in the negative".

### M6. Remark 3.3 convierte las Proposiciones en una afirmación sobre el método que no se sigue de ellas

**Ubicación.** main.tex:133–135 ("the field cannot improve on LDA by construction"; "where the field *could* help, it must do so through the component of A(x) − Σ̂⁻¹ along the local discriminant direction"); FICHA:14 (usa la Prop. 3.2 para justificar "la única vía").
**Problema.** Las dos proposiciones están enunciadas con las medias verdaderas μ_c como prototipos (main.tex:101 y :122). El método usa prototipos **locales** (Definición 2.1), de modo que s_A − s tiene además un término por el cambio de prototipos que la Prop. 3.2 no cubre; el control synth-lda muestra precisamente una diferencia de +1.25 que el texto atribuye a "estimation error or the effect of local prototypes" sin separar ambos. La frase "it must do so through…" es por tanto heurística bajo la hipótesis de prototipos fijos, y así debe etiquetarse (hoy lleva "[proved here / design]").
**Corrección.** Reetiquetar Remark 3.3 como "[proved here for fixed prototypes / design]" y añadir: "with local prototypes μ_c(x) a second term, 2(x − m̄)ᵀΣ⁻¹(δ(x) − δ) plus the change of midpoint, appears; the ablation 'aniso, global prototypes' of Table 3 isolates it empirically". Opcional y barato: una Proposición 3.2' con prototipos arbitrarios (misma álgebra, tres líneas).

---

## Hallazgos menores

- **m1. Nota de continuidad desactualizada.** CONTINUIDAD, "Resultados de referencia": "máx |s − 2 log(p₍₁₎/p₍₂₎)| = 3.6×10⁻¹⁵" pero `results_identity.json` y el PDF (p. 4) dicen 7.1×10⁻¹⁵; "0.01–0.05" (véase B2). Numeración: la nota, el README, `lda_identity.py` (docstring) y `tables_identity.md` hablan de "Proposición 1/2"; el manuscrito las numera 3.1/3.2. Unificar.
- **m2. Cita de Demšar (main.tex:161).** Demšar (2006) trata comparaciones *entre datasets*; aquí el Wilcoxon es sobre pliegues de un mismo dataset, uso que Demšar desaconseja. Citar Wilcoxon (1945) o decir "as a descriptive secondary check".
- **m3. Fuente de LVQ (main.tex:55, :97; refs.bib `kohonen1990`).** El artículo de 1990 describe LVQ en una sección, pero la referencia canónica es T. Kohonen, *Self-Organizing Maps*, Springer Series in Information Sciences 30, Springer, Berlin, 1995 (3.ª ed. 2001), o Kohonen, "Learning vector quantization", *Neural Networks* 1 (Suppl. 1), 303, 1988. Añadir una de las dos.
- **m4. refs.bib `franc2023`.** Falta el número de artículo: JMLR 24(11):1–49, 2023. Añadir `number = {11}`. Restaurar diacríticos (Průša, Voráček) con `{\v{s}}`, `{\'a}`, `{\v{c}}`.
- **m5. Estandarización y PCA dentro de la CV interna** (selective_benchmark.py:691–695 frente a :445–456). El escalador y la PCA se ajustan con todo el pliegue de entrenamiento externo y luego la CV interna divide ese mismo conjunto: la validación interna ve estadísticas de sus propios puntos. No afecta a los números de prueba (el pliegue de prueba externo no interviene), solo a la selección de hiperparámetros; decirlo en el Apéndice A.
- **m6. QDA con configuraciones omitidas** (selective_benchmark.py:253–256). Si `reg_param` falla en algunos pliegues internos y no en otros, su media interna se calcula sobre menos pliegues y la selección queda sesgada. Registrar el número de pliegues válidos y descartar la configuración si no completa los 3.
- **m7. Figura 3 (forest plot) con eje symlog, `linthresh = 1`** (make_figures.py:52). Casi todas las diferencias del campo anisótropo están en |Δ| < 1, exactamente la zona que el symlog comprime. Usar eje lineal recortado a [−2, +2] para "aniso/iso" y relegar la serie euclidiana (o anotar sus valores), o eliminar la figura (duplica la Tabla 4).
- **m8. Flotantes a la deriva.** Tabla 7, Figura 4 y Tabla 8 (Secciones 5.2–5.3) aparecen en las páginas 9–10, bajo el encabezado del Apéndice A y junto a las referencias. Añadir `\FloatBarrier` antes de la Sección 6 o mover esas tablas al apéndice (véase recortes). Las etiquetas "[computationally verified]" dentro de párrafos del cuerpo (main.tex:141, :272) sobran: el estado ya está en la Tabla 9.
- **m9. Intervalo de wine en la Tabla 4** se imprime como "[−0.00, +0.10]": imprimir con tres decimales o marcar como caso límite (es un extremo a 0.005 de cero y entra en el criterio).
- **m10. Macros y residuos.** `AblAnisoKnn*`, `AblAnisoLda*`, `AblAnisoDann*` se generan y no se usan; `results_fast.json` no se conserva (la nota cita su tiempo); `.gitignore` excluye `main.bbl`, que sin embargo está en la carpeta; `make_numbers.py:91–100` es un parche para un JSON desactualizado (desaparece con M2).
- **m11. Prop. 3.2, hipótesis "same pair in the same order".** Correcta y necesaria; conviene decir en una línea que si el orden se invierte la identidad vale con signo cambiado, y que si cambia el par no vale.
- **m12. Sección 2.1, "the error rate of h is the AURC of a random ordering".** Cierto en esperanza (ya se dice "in expectation" una frase antes); añadir "in expectation" también aquí, pues la Tabla 7 compara un AURC medio con una tasa de error media sin IC.

---

## Verificación matemática (detalle)

| Enunciado | Etiqueta en el texto | Verificación | Resultado |
|---|---|---|---|
| Prop. 3.1(i): m = tanh(s/4), K = 2 equiprobable; misma ordenación y AURC | proved here | Derivación a mano (p₍₁₎/p₍₂₎ = e^{s/2}, p₍₁₎+p₍₂₎ = 1) y 200 casos aleatorios (Σ, μ, x, d ∈ 2..7): desv. máx. 2.2×10⁻¹⁶ | Correcta |
| Prop. 3.1(ii): m = tanh(\|σ + 2 log(π₁/π₂)\|/4); banda de desacuerdo | proved here | 2000 casos aleatorios: desv. 2.2×10⁻¹⁶; banda exactamente como se enuncia | Correcta |
| Prop. 3.1(iii): s = 2 log(p₍₁₎/p₍₂₎), priors iguales; contraejemplo | proved here | 2000 casos K ∈ 3..6: desv. 8.9×10⁻¹⁶; contraejemplo recomputado: d² = (0.5625, 1.5625, 4.0625) y (0.8125, 1.8125, 2.3125), s = 1, m = 0.221/0.189, MSP = 0.562/0.481 | Correcta; **falla con priors desiguales** (desv. 3.58) — véase M1 |
| Prop. 3.2: s_A − s = 2(x − m̄)ᵀ(A − Σ⁻¹)δ; (b) s_A = λs | proved here | Álgebra verificada (requiere M simétrica, que se cumple); 1397 casos aleatorios bajo la hipótesis: desv. 6.8×10⁻¹³ | Correcta con prototipos fijos; su uso en Remark 3.3 excede la hipótesis (M6) |
| Remark 3.4 (sesgo de la covarianza de mezcla) | heuristic | Es la descomposición mezcla = intra + π(1−π)δδᵀ; etiqueta adecuada | OK |
| "LDA posterior and Bayes optimality for shared-covariance Gaussians" | classical | Correcto; citas Fisher 1936 / Hastie et al. 2009 adecuadas | OK |
| Esperanza exacta de la curva riesgo–cobertura bajo desempate aleatorio (Apéndice A) | — | Fuerza bruta: 20 000 desempates aleatorios sobre 40 puntos con 4 niveles de puntuación: exacto 0.182496, MC 0.182343 ± 0.000085 | Correcta |

## Afirmaciones frente a evidencia

- 448 macros muestreadas (AURC, exactitud, error, IC y victorias de las 8×13 celdas y de las 8 comparaciones con la mejor referencia) coinciden con `results.json` sin excepción; los recuentos de la Tabla 5 y de las ablaciones recomputados desde el JSON coinciden con las macros. Ningún número tipeado a mano.
- Las cifras del README, de la nota y de la ficha coinciden con el JSON, salvo m1.
- Sobreafirmaciones detectadas: B1 (positivas no robustas), M1 (priors), M3 ("indistinguishable"), M4 (victorias vacías en synth-classcov), M5 (cierre de la línea).

## Código

Leído completo `selective_benchmark.py`, `lda_identity.py`, `make_numbers.py`, `make_figures.py`. Sin fuga de información hacia los pliegues de prueba (escalador y PCA ajustados en entrenamiento; prototipos de reserva, medias globales y vecinos tomados solo de entrenamiento). Semillas fijas y deterministas (reproducción bit a bit confirmada). Empates tratados correctamente. Puntos a corregir: B2 (doble remuestreo del mismo par), M4 (bisección sin detección de límite), m5, m6. Observación: con K_m = 80 en iris la "covarianza local" interna usa 79 de 80 puntos (es la covarianza global); la clave nominal evita el desajuste de claves pero no el cambio de régimen entre CV interna (N = 80) y externa (N = 120); inherente al tamaño, basta mencionarlo.

## Estadística

Véase B1 (dependencia de pliegues, B pequeño, empates) y M3 (multiplicidad, lenguaje). Añadido: la "mejor referencia" se elige por media en los mismos pliegues (sesgo a favor de las referencias, ya reconocido); como el criterio no se cumple ni siquiera contra cada referencia por separado en ≥ 5 datasets, esto no cambia la conclusión. Con lectura conservadora (IC t) la conclusión principal se mantiene; las secundarias se debilitan como se detalla en B1.

## Bibliografía

Red: `api.crossref.org`, `api.openalex.org`, `dblp.org` y `jmlr.org` están bloqueados por el proxy de salida; la búsqueda web sí funcionó. Verifiqué por búsqueda web las entradas señaladas "de memoria" en la nota y las de selección/abstención; el resto no pude cotejarlo en red en esta sesión (son entradas canónicas y no detecté discrepancias con los datos editoriales conocidos, pero quedan como no verificadas).

| Entrada | Estado | Corrección / nota |
|---|---|---|
| franc2023 | **corregida** | JMLR 24(11):1–49, 2023: añadir `number = {11}`; restaurar diacríticos Průša, Voráček |
| street1993 | verificada | Proc. SPIE 1905 (Biomedical Image Processing and Biomedical Visualization), pp. 861–870, 1993 (ADS 1993SPIE.1905..861S). Opcional: editores R. S. Acharya y D. B. Goldgof |
| kohonen1990 | verificada | Proc. IEEE 78(9):1464–1480, 1990. Como fuente de LVQ, añadir Kohonen (1995) o (1988) (m3) |
| geifman2019 | verificada | ICLR 2019 (poster); es la fuente correcta del AURC |
| elyaniv2010 | verificada | JMLR 11:1605–1641, 2010 |
| chow1970 | verificada | IEEE Trans. Inf. Theory 16(1):41–46, 1970 |
| geifman2017, hendrycks2017, hastie1996, fisher1936, cover1967, tibshirani2002, ledoit2004, breiman2001, weinberger2009, hastie2009, efron1993, dietterich1998, nadeau2003, demsar2006, pedregosa2011, harris2020, virtanen2020, hunter2007 | no verificables en red en esta sesión | Datos coherentes con los canónicos; sin discrepancias detectadas. demsar2006: respalda otra cosa de lo que se cita (m2) |

Recuento: 5 verificadas, 1 corregida, 18 no verificadas en red. Cada cita respalda la afirmación para la que se usa, salvo demsar2006 (m2) y kohonen1990 como fuente de LVQ (débil, m3).

## Verificación computacional

Todo desde copias en el scratchpad; nada se escribió en la carpeta del autor. Entorno: Python 3.11.15, NumPy 2.4.6, SciPy 1.17.1, scikit-learn 1.9.1 (idéntico al declarado).

| Qué | CPU | Resultado |
|---|---|---|
| Protocolo **completo** (3×5 pliegues, CV interna, 13 métodos) en iris, wine y synth-classcov, comparado con `per_fold` de `results.json` | 109.3 s (iris 26.2, wine 28.3, synth-classcov 52.1, generación 2.7) | **585 de 585 AURC por pliegue idénticos (diferencia máxima 0.0)**; hiperparámetros seleccionados idénticos en los 585 casos; medias de la tabla coinciden |
| Replay del generador de datasets | incluido | Errores de Bayes bit a bit iguales a los almacenados (synth-classcov 0.0774318129…, synth-lda 0.0983565973…); desplazamientos 0.05 y 1.20 |
| `summarise()` desde `per_fold` con la misma semilla | ≈ 3 s | Reproduce exactamente todos los IC almacenados (estado "resummarised" confirmado) |
| Re-análisis estadístico (B = 200 000, IC t, Nadeau–Bengio, emulación del orden original del RNG) | ≈ 8 s | Véanse B1 y B2 |
| Verificación independiente de Props. 3.1/3.2 y del manejo de empates | < 1 s | Véase tabla de matemáticas |
| Compilación de `main.tex` (latexmk, pdflatex + bibtex) | 3 s | 11 páginas, 0 cajas desbordadas (hbox/vbox), 0 referencias indefinidas, 0 avisos de BibTeX |
| **Total** | **≈ 125 s** | Dentro del presupuesto de 5 min. No corrí `--fast` (habría consumido 148 s para una comparación aproximada); la reproducción exacta en 3 de 8 datasets es un control más fuerte. digits, breast-cancer, synth-informative, moons-aniso y synth-lda no se reprodujeron (≈ 370 s). |

## Recortes propuestos para llegar a ≤ 10 páginas (hoy 11)

1. Resumen: de ~430 a ~220 palabras (quitar la lista de referencias y la frase de la fórmula de desviación; queda en §3). (≈ 0.3 p.)
2. Fusionar Tablas 2 y 3 en una sola tabla "AURC×100" de 8 filas × 13 columnas + "err." (la Tabla 3 repite la mejor referencia). (≈ 0.3 p.)
3. Eliminar la Figura 3 (forest plot) o la Tabla 4: duplican información; si se conserva la figura, corregir el eje (m7). (≈ 0.4 p.)
4. Tabla 7 (geometría) y Tabla 8 (exactitud a cobertura fija) al apéndice o a `results/tables.md`, dejando en §5.2–5.3 las dos frases con macros que ya las resumen. Figura 4 (curvas riesgo–cobertura) al apéndice. (≈ 0.8 p.)
5. Fusionar Remarks 3.3 y 3.4 en un párrafo de texto corriente tras la Prop. 3.2 (con la reetiqueta de M6). (≈ 0.15 p.)
6. Párrafos "Tie handling" y "Grids" del Apéndice A a `results/tables.md` (ya está todo en el JSON), dejando tres líneas con la ruta. (≈ 0.3 p.)
7. Tabla 9: conservarla (es la pieza más útil del §6) y recortar el texto de §6 a un párrafo, pues repite el resumen.
Total estimado: ≈ 2.2 páginas → 8.5–9 páginas sin perder contenido verificable.

## Lista de acciones (por prioridad, en imperativo)

1. Añade a las Tablas 4 y 6 una columna de IC t sobre pliegues (o sustituye el bootstrap percentil por él), reporta victorias/empates/derrotas y reescribe main.tex:161 y :330 reconociendo que el optimismo infla todas las afirmaciones positivas (B1).
2. Reescribe en resumen, §6, Tabla 9 y ficha la afirmación sobre la ablación isótropa como "2–3 datasets según el intervalo; sugerente, no establecida", y "peor en 6" como "6 con bootstrap, 5 con IC t" (B1).
3. En `summarise`, copia la comparación directa en `__best__` en lugar de remuestrearla, sube B a ≥ 20 000 o siembra el RNG por par; recalcula con `--resummarise`; corrige "NCM 8/0" y marca como límite todo IC con extremo a < 0.02 de cero (B2).
4. Corrige la viñeta "Estadísticas recalculadas" de la nota: desplazamientos hasta 0.25, 4 veredictos individuales cambiados, ninguno del criterio (B2).
5. Añade "equiprobable" al enunciado para K ≥ 3 en main.tex:50, FICHA:13, FICHA:24 y README:33 (M1).
6. Regenera `results.json` con el script actual o declara en el Apéndice A que el resumen fue recalculado y que la metadata de datasets es anterior; crea un archivo fechado con el criterio y cítalo en main.tex:163 (M2).
7. Sustituye "significantly" por "with a 95 % interval excluding zero", "statistically indistinguishable" por "inconclusive", y declara que no hay corrección por multiplicidad (M3).
8. Corre synth-classcov con desplazamiento de medias no nulo (≈ 56 s) o, mientras tanto, declara las medias coincidentes en la Tabla 1 y quita o califica de triviales las victorias sobre NCM/LDA/LogReg en ese dataset; haz que `_calibrate_shift` señale cuándo toca el límite (M4).
9. Reformula README:5, FICHA:10/21 y FICHA:14/25: "cerrada para la formulación no supervisada evaluada"; lista las tres vías de §6 y no "la única vía" (M5).
10. Reetiqueta Remark 3.3 como heurística bajo prototipos fijos o añade la Prop. 3.2' con prototipos locales (M6).
11. Corrige refs.bib: `franc2023` número 11 y diacríticos; añade Kohonen (1995) para LVQ; cambia la justificación de la cita a Demšar (m2–m4).
12. Actualiza la nota (7.1×10⁻¹⁵, numeración 3.1/3.2) y los docstrings de `lda_identity.py` y `tables_identity.md` (m1).
13. Aplica los recortes 1–6 y `\FloatBarrier` antes de §6; corrige el eje de la Figura 3; elimina las etiquetas "[computationally verified]" del cuerpo (m7, m8).
14. Documenta en el Apéndice A que el escalador/PCA se ajustan al pliegue externo antes de la CV interna, y registra configuraciones de QDA omitidas (m5, m6).
