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

## Qué se produjo (todo en `papers/HQF001-resolution-fields-abstention/`)
1. `manuscript/main.tex` (inglés, 11 páginas con referencias) + `refs.bib` (24 entradas) + `main.pdf`; macros y tablas generadas por `experiments/make_numbers.py`.
2. `experiments/selective_benchmark.py` (benchmark completo), `experiments/lda_identity.py` (verificación de la Proposición 1), `experiments/make_figures.py`.
3. `results/results.json`, `results/tables.md`, `results/results_identity.json`, `results/tables_identity.md`; `figures/` (4 figuras).
4. README, esta nota y una propuesta de ficha.

## Decisiones tomadas
- **Datasets:** iris, wine, breast-cancer, digits (PCA a 20 componentes ajustado en cada fold de entrenamiento, para que las covarianzas de vecindario sean estimables para todos los métodos locales por igual), y cuatro sintéticos diseñados según la Proposición 2: synth-informative (`make_classification`), moons-aniso (dos lunas + ruido gaussiano anisótropo 0.30×0.06 rotado 30° + 3 dimensiones de ruido), synth-classcov (covarianzas rotadas distintas), synth-lda (covarianza compartida, 3 clases; control donde por la Proposición 1 no puede haber ganancia).
- **synth-classcov terminó con medias coincidentes.** La separación de medias se buscaba por bisección hacia un error de Bayes del 10 % en [0.05, 20], pero las dos covarianzas rotadas ya separan las clases con 7.7 % de error, así que la bisección tocó el límite inferior (desplazamiento 0.05). No se corrigió ni se recorrió: es el caso más nítido del régimen donde una métrica local podría importar, explica que NCM/LDA/LogReg estén al nivel de azar (≈48 % de error) y se documenta explícitamente en el manuscrito. Una variante con desplazamiento de medias y covarianzas distintas queda pendiente.
- **Presupuesto de cómputo:** 3 repeticiones × 5 folds (no 4×5) y rejilla de regresión logística C ∈ {0.1, 1, 10} para caber en ~10 min de CPU. Un hilo BLAS (`OMP_NUM_THREADS=1`) para que CPU ≈ reloj.
- **QDA con `reg_param = 0` excluido** (falla por covarianza singular en folds internos pequeños); rejilla {0.01, 0.1, 0.5}.
- **Empates en la puntuación:** la curva riesgo–cobertura se calcula como esperanza exacta bajo desempate aleatorio uniforme (por bloques), porque las fracciones de voto de k-NN y las probabilidades de random forest tienen muchos empates y el AURC depende de cómo se traten.
- **Ajuste de hiperparámetros:** todos los métodos por CV interna de 3 folds minimizando AURC (el criterio de evaluación), refit en el fold completo. La clave de configuración lleva el $K_m$ nominal (no el recortado) para que la selección interna coincida con la configuración externa en datasets pequeños; este fue un error detectado en la prueba rápida y corregido antes de la corrida de referencia.
- **Estadísticas recalculadas sin recorrer el benchmark.** Tras la primera versión se detectó que un mismo par (campo vs. k-NN en breast-cancer) aparecía con dos IC distintos porque se remuestreaba dos veces (comparaciones y ablaciones) con distinto ruido Monte Carlo y su extremo inferior está en +0.01. Se añadió `--resummarise` (recalcula resumen y criterio desde los resultados por fold guardados, misma semilla) y las ablaciones cuyo segundo miembro es una referencia copian la comparación. Los veredictos del criterio no cambiaron; algunos extremos de IC se movieron en 0.01–0.05. Ese par se señala en el manuscrito como efectivamente no concluyente.
- **Idioma:** manuscrito en inglés; README y nota en español.

## Resultados de referencia (corrida completa, semilla 20260930, 449 s CPU / 477 s reloj)
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

Verificación de la Proposición 1 (parámetros verdaderos, d = 5, n = 4000): K = 2 equiprobable: Spearman(s, m) = 1.000000, máx |m − tanh(s/4)| = 2.8×10⁻¹⁶, diferencia de AURC = 0. Priors (0.8, 0.2): Spearman 0.9725, no monótono, predicciones distintas en 0.57 % de los puntos; puntuación corregida monótona (desviación 4.4×10⁻¹⁶). K = 3 (error 11.2 %): máx |s − 2 log(p₍₁₎/p₍₂₎)| = 3.6×10⁻¹⁵; monótono en el log-cociente, no en p₍₁₎−p₍₂₎ ni en MSP; AURC×100 2.415 (s), 2.392 (p₍₁₎−p₍₂₎), 2.380 (MSP). Contraejemplo explícito: μ₁=(0,0), μ₂=(2,0), μ₃=(1,2), Σ=I, x_A=(0.75,0), x_B=(0.75,0.5): s = 1 en ambos; margen posterior 0.221 vs 0.189; MSP 0.562 vs 0.481.

## Tiempo total de cómputo de la sesión
Corrida de referencia 449 s CPU; verificación ≈ 1 s; figuras ≈ 5 s; prueba rápida completa (`--fast`) 148 s; dos intentos abortados de la prueba rápida ≈ 35 s; depuración de la calibración ≈ 10 s. Total ≈ 650 s ≈ 10.8 min de CPU.

## Limitaciones (explícitas en el manuscrito)
- El campo es **una** reconstrucción; formulaciones supervisadas o aprendidas, o la combinación margen + volumen como regla bidimensional, no se corrieron y podrían cambiar el resultado.
- Datasets pequeños/medianos y de baja dimensión tras el preprocesado (n ≤ 1797, d ≤ 30); en alta dimensión la comparación puede moverse en cualquier sentido.
- CV interna de 3 folds sobre AURC es ruidosa en iris y wine.
- Los IC bootstrap sobre folds repetidos son optimistas y la mejor referencia se elige en los mismos folds: ambos sesgos favorecen encontrar una ganancia, así que refuerzan la conclusión negativa.
- DANN no se ajustó más allá de la rejilla indicada (una iteración, ε = 1).
- synth-classcov con medias coincidentes (véase decisiones).

## Lo que NO se afirma
- No se afirma que ningún campo de resolución sea inútil para abstención: se afirma que **esta** formulación, en **estos** datasets, no supera a las referencias bajo el criterio predefinido.
- No se afirma nada sobre poblaciones reales, ni sobre redes neuronales, ni sobre alta dimensión.
- No se afirma nada físico ni cuántico; la ficha ya lo excluía.
- La "ganancia" en synth-classcov sobre k-NN/DANN/RForest no se atribuye a la anisotropía (la ablación euclidiana la obtiene igual o mejor).
- La observación heurística sobre el sesgo de la covarianza de mezcla a lo largo de δ es una explicación plausible, no un resultado demostrado.

## Bibliografía: notas de verificación
Todas las entradas de `refs.bib` corresponden a trabajos reales que conozco. Datos a cotejar antes de enviar: (i) Franc, Průša y Voráček, "Optimal strategies for reject option classifiers", JMLR 24 (2023): el número de artículo y las páginas (se puso 1–49) deben verificarse; (ii) Street, Wolberg y Mangasarian (1993): el nombre exacto del volumen de SPIE (se puso "Biomedical Image Processing and Biomedical Visualization", vol. 1905, pp. 861–870); (iii) Kohonen (1990) se cita como fuente de LVQ porque el artículo lo describe, aunque la referencia canónica de LVQ es el libro *Self-Organizing Maps* (1995), no incluido por no tener a mano los datos editoriales exactos; (iv) los nombres de autores acentuados (Průša, Voráček) se escribieron sin diacríticos en el `.bib`.

## Pendientes y próximos pasos concretos
1. Confirmar con el autor la reconstrucción de la definición (supuestos 1–3). Si su noción original era supervisada (información de Fisher / intra-clase), correr esa variante con el mismo protocolo y criterio: es la única vía por la que la Proposición 2 deja abierta una ganancia.
2. Regla bidimensional margen + log-volumen (rechazar si el margen es pequeño **o** el volumen es grande), con el mismo criterio predefinido.
3. synth-classcov con desplazamiento de medias no nulo, y un benchmark de mayor dimensión con regularización explícita de covarianza.
4. Si nada de lo anterior se retoma: actualizar la ficha del CV web con `FICHA_HQF001_propuesta.md` (de "En pausa" a "Cerrada — resultado negativo con criterio predefinido").
