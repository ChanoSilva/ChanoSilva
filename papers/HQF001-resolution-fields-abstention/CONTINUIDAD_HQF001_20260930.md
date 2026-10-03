# HQF001 — Continuidad interna, 30/09/2026

Documento de trabajo interno. No incorporar al manuscrito ni a entregas institucionales.

## Proyecto y alcance
Línea HQF001, "Resolución local e incertidumbre en aprendizaje" / "Local resolution and uncertainty in learning", área Inteligencia artificial y aprendizaje, estado en el CV web: "En pausa". Ficha pública: "An exploration of anisotropic resolution fields for representing uncertainty and abstention decisions. Objective: test whether the representation adds information beyond local metrics and prototype-based methods. Findings: available comparisons do not establish a residual gain over those references. Scope: the formulation is computational and makes no claim about quantum physical phenomena."

Pedido en la sesión de Claude Code (session_01MTmjU2K8b4sgpjjL3JTtDz, repositorio ChanoSilva, carpeta `papers/`): correr la comparación controlada que faltaba, con criterio predefinido, y escribirla honestamente; incluir un enunciado exacto que aísle lo que la anisotropía podría aportar.

## Supuestos: qué hubo que reconstruir de la ficha (verificar con el autor)
No existe manuscrito, código ni notas previas de la línea; solo la ficha. Todo lo siguiente es una **reconstrucción** y debe confirmarse o corregirse:

1. **Definición del campo.** Se tomó $A(x) = S(x)^{-1}$ con $S(x) = (1-\alpha)\,C(x) + \alpha\,(\operatorname{tr} C(x)/d)\,I$, donde $C(x)$ es la covarianza muestral de los $K_m$ vecinos euclidianos de $x$ (características estandarizadas). Es la versión **no supervisada** del campo (geometría de los datos, sin etiquetas). Alternativas no corridas: información de Fisher de un modelo local de probabilidad de clase; covarianza intra-clase local (descomposición DANN); campo aprendido.
2. **Puntuaciones.** Margen de Mahalanobis $d^2_{(2)} - d^2_{(1)}$ bajo $A(x)$ a **prototipos locales** (media de los vecinos de cada clase; si la clase no aparece en el vecindario, su punto de entrenamiento más cercano); log-volumen $-\log\det S(x)$; anisotropía $-\log(\lambda_{\max}/\lambda_{\min})$. La ficha habla de "abstention decisions": se formalizó como clasificación selectiva (rechazar si la puntuación está por debajo de un umbral) evaluada por curvas riesgo–cobertura, AURC y exactitud a cobertura 90 % y 80 %.
3. **Ablaciones.** Isótropa ($\alpha = 1$: solo escala local), euclidiana ($A = I$: centroide local), prototipos globales con métrica local.
4. **Referencias.** k-NN (fracción de votos, pesos uniformes o por distancia), NCM (margen euclidiano a medias de clase), LDA, QDA, regresión logística, random forest (máxima probabilidad), DANN (Hastie–Tibshirani 1996, una iteración, ε = 1). LVQ no se implementó (no está en scikit-learn y un LVQ en bucle Python excedía el presupuesto); NCM representa a la familia de prototipos.
5. **Criterio de "ganancia residual"** (fijado antes de correr): AURC menor que la mejor referencia (mejor media por dataset entre las 7) en ≥ 5 de 8 datasets con IC bootstrap pareado al 95 % que excluya 0. Se reporta además la comparación contra cada referencia por separado para eliminar el sesgo de selección de la mejor.
6. **"Cuántico".** Solo se reproduce la salvedad de la ficha; el término "resolución" nombra un campo matricial y nada más.

## Qué se produjo en v0.1 (30/09/2026; superado por v0.2 y v0.3 — estado actual en el README y en las secciones de las rondas 1 y 2)
1. `manuscript/main.tex` (inglés, 11 páginas con referencias) + `refs.bib` (24 entradas) + `main.pdf`; macros y tablas generadas por `experiments/make_numbers.py`.
2. `experiments/selective_benchmark.py` (benchmark completo), `experiments/lda_identity.py` (verificación de las Proposiciones 3.1 y 3.2), `experiments/make_figures.py`.
3. `results/results.json`, `results/tables.md`, `results/results_identity.json`, `results/tables_identity.md`; `figures/` (4 figuras).
4. README, esta nota y una propuesta de ficha.

## Decisiones tomadas (v0.1, 30/09/2026; las que cambiaron se indican en las secciones de las rondas 1 y 2)
- **Datasets:** iris, wine, breast-cancer, digits (PCA a 20 componentes ajustado en cada fold de entrenamiento, para que las covarianzas de vecindario sean estimables para todos los métodos locales por igual), y cuatro sintéticos diseñados según la Proposición 3.2: synth-informative (`make_classification`), moons-aniso (dos lunas + ruido gaussiano anisótropo 0.30×0.06 rotado 30° + 3 dimensiones de ruido), synth-classcov (covarianzas rotadas distintas), synth-lda (covarianza compartida, 3 clases; control donde ninguna puntuación puede superar a un LDA bien estimado salvo por error de estimación: para K = 3 lo garantiza la optimalidad del rechazo por máximo posterior verdadero (Chow 1970), no la Proposición 3.1(i), que es para K = 2 — corregido en la ronda 2, R2-m5).
- **[v0.1; superado: dataset regenerado en v0.2] synth-classcov terminó con medias coincidentes.** La separación de medias se buscaba por bisección hacia un error de Bayes del 10 % en [0.05, 20], pero las dos covarianzas rotadas ya separan las clases con 7.7 % de error, así que la bisección tocó el límite inferior (desplazamiento 0.05). No se corrigió ni se recorrió: es el caso más nítido del régimen donde una métrica local podría importar, explica que NCM/LDA/LogReg estén al nivel de azar (≈48 % de error) y se documenta explícitamente en el manuscrito. Una variante con desplazamiento de medias y covarianzas distintas queda pendiente.
- **Presupuesto de cómputo:** 3 repeticiones × 5 folds (no 4×5) y rejilla de regresión logística C ∈ {0.1, 1, 10} para caber en ~10 min de CPU. Un hilo BLAS (`OMP_NUM_THREADS=1`) para que CPU ≈ reloj.
- **QDA con `reg_param = 0` excluido** (falla por covarianza singular en folds internos pequeños); rejilla {0.01, 0.1, 0.5}.
- **Empates en la puntuación:** la curva riesgo–cobertura se calcula como esperanza exacta bajo desempate aleatorio uniforme (por bloques), porque las fracciones de voto de k-NN y las probabilidades de random forest tienen muchos empates y el AURC depende de cómo se traten.
- **Ajuste de hiperparámetros:** todos los métodos por CV interna de 3 folds minimizando AURC (el criterio de evaluación), refit en el fold completo. La clave de configuración lleva el $K_m$ nominal (no el recortado) para que la selección interna coincida con la configuración externa en datasets pequeños; este fue un error detectado en la prueba rápida y corregido antes de la corrida de referencia.
- **Estadísticas recalculadas sin recorrer el benchmark (v0.1).** Tras la primera versión se detectó que un mismo par (campo vs. k-NN en breast-cancer) aparecía con dos IC distintos porque se remuestreaba dos veces (comparaciones y ablaciones) con distinto ruido Monte Carlo y su extremo inferior está en +0.01. Se añadió `--resummarise` y las ablaciones cuyo segundo miembro es una referencia copiaron la comparación; pero la comparación con la "mejor referencia" (`__best__`) siguió remuestreándose aparte de la directa, así que el defecto persistió en 43 de 48 pares (hallazgo B2 del árbitro). Efecto real del `--resummarise` sobre v0.1 (verificado por el árbitro emulando el orden original del RNG, `verif_math_stats.txt` D2): los extremos de IC se movieron hasta 0.25 en AURC×100 (mediana 0.014, percentil 90 0.079; 84 de 464 extremos más de 0.05) y cambiaron 4 veredictos de comparaciones individuales (breast-cancer campo vs k-NN y vs NCM, breast-cancer iso vs k-NN, synth-informative anisotropía vs LogReg); **ninguno del criterio**. Corregido en v0.2: generador por par y `__best__` copia la directa (véase la sección de la ronda 1).
- **Idioma:** manuscrito en inglés; README y nota en español.

## Resultados de referencia v0.1 (30/09/2026; superados por v0.2 y v0.3: synth-classcov regenerado, IC con B = 2 000, rejilla del campo v0.2 — no usar estas cifras)

Corrida completa v0.1, semilla 20260930, 449 s CPU / 477 s reloj.
AURC×100 (media sobre 15 folds); mejor referencia en negrita; err = tasa de error de la mejor referencia:

| dataset | k-NN | NCM | LDA | QDA | LogReg | RForest | DANN | err | Field-aniso | Field-iso | Field-euclid | Field-vol | Field-anis | Field-gproto |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| iris | 0.68 | 2.73 | **0.17** | 0.23 | 0.25 | 0.54 | 0.19 | 2.0 | 0.37 | 0.65 | 0.76 | 1.54 | 6.79 | 1.77 |
| wine | 0.69 | 0.57 | 0.10 | **0.03** | 0.11 | 0.15 | 0.70 | 0.9 | 0.08 | 0.28 | 0.34 | 0.65 | 0.64 | 1.10 |
| breast-cancer | 0.57 | 1.15 | 0.61 | 0.54 | **0.25** | 0.64 | 0.86 | 2.3 | 0.83 | 0.45 | 0.57 | 4.73 | 4.35 | 1.66 |
| digits | 0.28 | 2.97 | 1.54 | 1.80 | 0.64 | 0.41 | **0.25** | 2.5 | 0.26 | 1.04 | 4.11 | 0.66 | 1.42 | 2.16 |
| synth-informative | 4.81 | 21.04 | 18.00 | 6.41 | 17.54 | **3.51** | 3.96 | 10.5 | 4.81 | 4.95 | 4.95 | 17.10 | 15.60 | 21.31 |
| moons-aniso | 0.82 | 2.36 | 2.18 | 2.23 | 2.17 | **0.62** | 1.23 | 4.0 | 1.19 | 1.23 | 1.64 | 4.67 | 10.18 | 2.00 |
| synth-classcov | 1.69 | 48.46 | 48.44 | **0.97** | 48.45 | 2.48 | 1.77 | 7.3 | 1.40 | 1.24 | 1.23 | 18.02 | 16.69 | 46.62 |
| synth-lda | 2.90 | 5.05 | **1.58** | 1.64 | 1.63 | 3.67 | 2.26 | 8.9 | 2.83 | 2.94 | 3.10 | 15.02 | 14.42 | 4.48 |

Diferencias pareadas Field-aniso − mejor referencia (AURC×100, IC 95 % bootstrap, victorias/15 folds): iris +0.20 [+0.04, +0.43] 1/15; wine +0.05 [−0.00, +0.10] 4/15; breast-cancer +0.58 [+0.35, +0.90] 0/15; digits +0.01 [−0.11, +0.14] 7/15; synth-informative +1.30 [+0.76, +1.87] 2/15; moons-aniso +0.56 [+0.35, +0.76] 2/15; synth-classcov +0.43 [+0.32, +0.56] 0/15; synth-lda +1.25 [+1.04, +1.50] 0/15. **Criterio: 0 mejor, 6 peor, 2 no concluyente → no cumplido.** Las otras cinco variantes: peores en 8/8.

Ablación aniso − iso: iris −0.28 [−0.54, −0.05]; wine −0.20 [−0.37, −0.05]; breast-cancer +0.37 [+0.19, +0.59]; digits −0.78 [−1.19, −0.43]; synth-informative −0.14 [−0.52, +0.19]; moons-aniso −0.05 [−0.10, +0.00]; synth-classcov +0.16 [+0.10, +0.21]; synth-lda −0.11 [−0.36, +0.10].

Hiperparámetros elegidos para Field-aniso (120 pares dataset–fold): α = 0.05 en 9 %, 0.2 en 18 %, 0.5 en 72 %; $K_m$ = 20 en 31 %, 40 en 16 %, 80 en 53 %.

Verificación de la Proposición 3.1 del manuscrito (parámetros verdaderos, d = 5, n = 4000): K = 2 equiprobable: Spearman(s, m) = 1.000000, máx |m − tanh(s/4)| = 2.8×10⁻¹⁶, diferencia de AURC = 0. Priors (0.8, 0.2): Spearman 0.9725, no monótono, predicciones distintas en 0.57 % de los puntos; puntuación corregida monótona (desviación 4.4×10⁻¹⁶). K = 3 (error 11.2 %): máx |s − 2 log(p₍₁₎/p₍₂₎)| = 7.1×10⁻¹⁵; monótono en el log-cociente, no en p₍₁₎−p₍₂₎ ni en MSP; AURC×100 2.415 (s), 2.392 (p₍₁₎−p₍₂₎), 2.380 (MSP). Contraejemplo explícito: μ₁=(0,0), μ₂=(2,0), μ₃=(1,2), Σ=I, x_A=(0.75,0), x_B=(0.75,0.5): s = 1 en ambos; margen posterior 0.221 vs 0.189; MSP 0.562 vs 0.481.

## Tiempo total de cómputo de la sesión v0.1 (30/09/2026)
Corrida de referencia 449 s CPU; verificación ≈ 1 s; figuras ≈ 5 s; prueba rápida completa (`--fast`) 148 s; dos intentos abortados de la prueba rápida ≈ 35 s; depuración de la calibración ≈ 10 s. Total ≈ 650 s ≈ 10.8 min de CPU.

## Limitaciones (v0.1, 30/09/2026; superadas — las vigentes están en el §6 del manuscrito v0.3)
- El campo es **una** reconstrucción; formulaciones supervisadas o aprendidas, o la combinación margen + volumen como regla bidimensional, no se corrieron y podrían cambiar el resultado.
- Datasets pequeños/medianos y de baja dimensión tras el preprocesado (n ≤ 1797, d ≤ 30); en alta dimensión la comparación puede moverse en cualquier sentido.
- CV interna de 3 folds sobre AURC es ruidosa en iris y wine.
- [Incorrecto, corregido en la ronda 1 (B1)] Los IC bootstrap sobre folds repetidos son optimistas y la mejor referencia se elige en los mismos folds: ambos sesgos favorecen encontrar una ganancia, así que refuerzan la conclusión negativa. (El optimismo de los IC infla también los veredictos "peor" y los recuentos positivos de ablación; véase el manuscrito.)
- DANN no se ajustó más allá de la rejilla indicada (una iteración, ε = 1).
- [v0.1; superado] synth-classcov con medias coincidentes (véase decisiones).

## Lo que NO se afirma
- No se afirma que ningún campo de resolución sea inútil para abstención: se afirma que **esta** formulación, en **estos** datasets, no supera a las referencias bajo el criterio predefinido.
- No se afirma nada sobre poblaciones reales, ni sobre redes neuronales, ni sobre alta dimensión.
- No se afirma nada físico ni cuántico; la ficha ya lo excluía.
- La "ganancia" en synth-classcov sobre k-NN/DANN/RForest no se atribuye a la anisotropía (la ablación euclidiana la obtiene igual o mejor).
- La observación heurística sobre el sesgo de la covarianza de mezcla a lo largo de δ es una explicación plausible, no un resultado demostrado.

## Bibliografía: notas de verificación
Todas las entradas de `refs.bib` corresponden a trabajos reales que conozco. Datos a cotejar antes de enviar: (i) Franc, Průša y Voráček, "Optimal strategies for reject option classifiers", JMLR 24 (2023): el número de artículo y las páginas (se puso 1–49) deben verificarse; (ii) Street, Wolberg y Mangasarian (1993): el nombre exacto del volumen de SPIE (se puso "Biomedical Image Processing and Biomedical Visualization", vol. 1905, pp. 861–870); (iii) Kohonen (1990) se cita como fuente de LVQ porque el artículo lo describe, aunque la referencia canónica de LVQ es el libro *Self-Organizing Maps* (1995), no incluido por no tener a mano los datos editoriales exactos; (iv) los nombres de autores acentuados (Průša, Voráček) se escribieron sin diacríticos en el `.bib`.

## Pendientes y próximos pasos concretos
1. Confirmar con el autor la reconstrucción de la definición (supuestos 1–3). Si su noción original era supervisada (información de Fisher / intra-clase), correr esa variante con el mismo protocolo y criterio: es la vía por la que la Proposición 3.2 deja abierta una ganancia con prototipos fijos (con prototipos locales entran dos términos más, Prop. 3.2(c)).
2. Regla bidimensional margen + log-volumen (rechazar si el margen es pequeño **o** el volumen es grande), con el mismo criterio predefinido.
3. synth-classcov con desplazamiento de medias no nulo, y un benchmark de mayor dimensión con regularización explícita de covarianza.
4. Si nada de lo anterior se retoma: actualizar la ficha del CV web con `FICHA_HQF001_propuesta.md` (de "En pausa" a "Cerrada — resultado negativo con criterio predefinido").


## Ronda 1 de revisión interna (30/09/2026; respuesta aplicada el 03/10/2026)

Informe: `REFEREE_HQF001_ronda1_20260930.md` (2 bloqueantes, 6 mayores, 12 menores). Respuesta punto por punto: `RESPUESTA_HQF001_ronda1_20260930.md`. Resultado: borrador **v0.2**; la corrida de referencia se repitió completa con el script v0.2 (284.5 s de CPU, 287 s de reloj; los 7 datasets no modificados reproducen v0.1 bit a bit en los 15 × 13 AURC por pliegue). La v0.1 se conserva en `results/results_v01.json` y `results/tables_v01.md`.

| hallazgo | decisión | acción |
|---|---|---|
| B1 IC bootstrap optimistas inflan las afirmaciones positivas | aceptar | `pair_stats`: IC bootstrap (predefinido) + IC t + IC t Nadeau–Bengio (ρ = 1/4), V/E/D, p de Wilcoxon, indicador de caso límite (< 0.02 de cero); Tabla de diferencias con los tres IC; tablas de ablación y vs-referencias marcan solo cuando ambos IC excluyen cero; resumen, §4, §5, §6, tabla de afirmaciones y ficha reescritos ("6 con bootstrap, 5 con IC t"; ablación "2–3 según el intervalo; sugerente, no establecida") |
| B2 dos IC para el mismo par; viñeta de la nota incorrecta | aceptar | generador por par (semilla + CRC32 del nombre), `__best__` = copia de la directa, B = 20 000; viñeta corregida arriba; "NCM 8/0" → 7/0 con breast-cancer vs NCM límite ([−0.65, +0.0006]) |
| M1 identidad K ≥ 3 sin "equiprobable" | aceptar | "equiprobable" en resumen, ficha y README; Prop. 3.1(iii) añade la forma general con término de priors (verificada: desviación ingenua 3.58 con priors (0.6, 0.3, 0.1), corregida 7.1×10⁻¹⁵) |
| M2 sin registro fechado del criterio; JSON de versión anterior | aceptar con matiz | `CRITERIO_HQF001.md` (fechado 03/10/2026, declara que no hay registro anterior a la corrida, hash sha256 del script); corrida completa regenerada con el script actual (metadata = código); §4 declara la corrección de la clave K_m entre prueba rápida y corrida |
| M3 lenguaje inferencial y multiplicidad | aceptar | "significantly" eliminado; "with a 95 % interval excluding zero"; "indistinguishable" → "inconclusive" con V/E/D; frase explícita de no corrección por multiplicidad (56 + 48 intervalos descriptivos); Wilcoxon en la tabla como chequeo descriptivo citando Wilcoxon (1945) |
| M4 synth-classcov con medias coincidentes | aceptar | `_calibrate_shift` devuelve indicador de límite (guardado en el JSON); espectro geomspace(2, 0.25, 6) → desplazamiento 1.54, error de Bayes 9.9 %; dataset regenerado; v0.1 reportada en §5.1 y aquí |
| M5 cierre de la línea sobreafirmado | aceptar | README, ficha y §6: "cerrada para la formulación no supervisada evaluada"; tres vías de §6 listadas, no "la única vía"; resumen: "in the precise form reconstructed here" |
| M6 Remark 3.3 excede las hipótesis | aceptar | Prop. 3.2(c) con prototipos arbitrarios (demostrada, residuo 4×10⁻¹⁴ en 500 casos); Remark 3.3 y 3.4 fusionados en un párrafo etiquetado "proved here for fixed prototypes / heuristic for local prototypes / design" |
| m1 nota desactualizada | aceptar | 7.1×10⁻¹⁵; numeración 3.1/3.2 en nota, README, docstring y tabla de identidad |
| m2 Demšar | aceptar | Wilcoxon (1945) para el test por pliegues; Demšar citado solo para los tests entre datasets que no se hacen |
| m3 LVQ | aceptar | añadido Kohonen (1995), *Self-Organizing Maps*, Springer Series in Information Sciences 30 |
| m4 franc2023 | aceptar | `number = {11}`; diacríticos Vojtěch Franc, Daniel Průša, Václav Voráček |
| m5 escalador/PCA antes de la CV interna | aceptar (documentar) | Apéndice A, párrafo "Preprocessing and inner selection" |
| m6 QDA con configuraciones omitidas | aceptar | configuraciones que no completan los 3 pliegues internos se descartan y se cuentan (`inner_configs_dropped`); en la corrida v0.2: 0 |
| m7 forest plot symlog | aceptar (eliminar) | figura eliminada (duplicaba la tabla de diferencias) |
| m8 flotantes a la deriva; etiquetas en el cuerpo | aceptar | `\FloatBarrier` antes de §6 y del apéndice; tablas de geometría y exactitud y curvas R-C fuera del cuerpo; etiquetas "[computationally verified]" quitadas de los párrafos |
| m9 IC de wine "[−0.00, +0.10]" | aceptar | extremos que redondean a 0.00 se imprimen con tres decimales y el par se marca como límite |
| m10 macros sin uso, `results_fast.json`, `.gitignore`, parche de `make_numbers` | aceptar | macros `AblAnisoKnn/Lda/Dann` eliminadas; parche eliminado (el JSON v0.2 exporta `shift`); `main.bbl` deja de estar ignorado; `results_fast.json` no se conserva (no se volvió a correr `--fast`: 148 s de CPU que no cabían en el presupuesto) |
| m11 hipótesis de orden en Prop. 3.2 | aceptar | frase añadida: orden invertido → identidad con s_A + s y cambio de signo; par distinto → no vale |
| m12 "in expectation" | aceptar | añadido |

**Números que cambiaron entre v0.1 y v0.2** (todos los demás AURC medios son idénticos):
- synth-classcov (dataset nuevo, desplazamiento 1.54, error de Bayes 9.9 %): AURC×100 k-NN 2.55, NCM 8.51, LDA 6.30, **QDA 1.69**, LogReg 5.96, RForest 3.42, DANN 2.83; campo aniso 2.77, iso 2.30, euclid 2.31, vol 16.70, anis 15.10, prot. globales 10.23. Campo − QDA: +1.08 [+0.86, +1.33] bootstrap, [+0.81, +1.35] t, 0/0/15. Campo vs k-NN +0.22 (peor con bootstrap [+0.03, +0.43], límite; t [−0.00, +0.45] no concluyente); vs DANN −0.06 no concluyente; vs RForest −0.65 mejor; vs NCM/LDA/LogReg −5.73/−3.53/−3.18 mejor. Aniso − iso +0.47 [+0.35, +0.58] (la anisotropía perjudica). v0.1 era: QDA 0.97, campo 1.40, iso 1.24, euclid 1.23, k-NN 1.69, DANN 1.77, RForest 2.48, NCM/LDA/LogReg ≈ 48.4 (azar).
- Criterio: 0 mejor / 6 peor / 2 no concluyente con bootstrap (igual que v0.1); **0 / 5 / 3 con IC t** (iris pasa a no concluyente); 0 / 3 / 5 con Nadeau–Bengio. No cumplido en las tres lecturas.
- Ablación aniso − iso: mejor en 3 (iris, wine, digits) con bootstrap, **2 (wine, digits) con IC t**, 0 con NB; peor en 2 (breast-cancer, synth-classcov) con ambos IC, 1 con NB. V/E/D: digits 15/0/0, wine 8/5/2, iris 8/4/3.
- Campo vs cada referencia (mejor/peor con bootstrap → con t): k-NN 1/3 → 0/1; NCM 7/0 → 7/0; LDA 4/3 → 4/2; QDA 3/3 → 3/2; LogReg 4/2 → 4/2; RForest 3/2 → 3/2; DANN 1/3 → 0/2. Pares límite: iris vs QDA, wine vs QDA, breast-cancer vs k-NN, breast-cancer vs NCM, synth-classcov vs k-NN.
- Los IC bootstrap de los otros 7 datasets se movieron en el segundo decimal por el nuevo sembrado y B = 20 000 (p. ej. iris campo − LDA [+0.04, +0.43] → [+0.05, +0.43]); ningún veredicto de esos datasets cambió respecto a v0.1 salvo breast-cancer vs NCM (mejor → no concluyente, límite).

**Queda abierto tras la ronda 1:**
1. Confirmar con el autor la reconstrucción de la definición (supuestos 1–3) y la decisión de regenerar synth-classcov (cambio del conjunto de datasets tras ver v0.1; el veredicto no depende de ello).
2. Las bibliografías marcadas "no verificables en red" por el árbitro (18 entradas canónicas) siguen sin cotejo en red; no se detectaron discrepancias.
3. m5 solo se documenta: ajustar el escalador/PCA dentro de cada pliegue interno cambiaría la selección de hiperparámetros y requeriría otra corrida completa.
4. Las vías (a)–(c) del §6 (campo supervisado, regla margen + volumen, alta dimensión) no se corrieron.
5. Tiempo de cómputo de la ronda: corrida completa 284.5 s + pruebas de humo y re-resumen ≈ 15 s + exploración de espectros 4 s + verificación de la proposición < 1 s + figuras 3 s + compilaciones ≈ 30 s ≈ 5.6 min de CPU (cifra unificada con la respuesta de la ronda 1; la versión anterior de esta línea omitía espectros y compilaciones).
