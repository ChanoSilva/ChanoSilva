# Propuesta de actualización de la ficha HQF001 en el CV web

Texto propuesto para reemplazar la ficha actual (estado "En pausa"). Cifras tomadas de la corrida de referencia (semilla 20260930, `results/results.json`).

## Español

- **Código:** HQF001
- **Área:** Inteligencia artificial y aprendizaje
- **Título:** Resolución local e incertidumbre en aprendizaje
- **Descripción breve:** Campos de resolución anisótropos (una métrica local definida positiva por punto, estimada de la geometría de los datos) como representación de la incertidumbre para decisiones de abstención, evaluados como clasificación selectiva.
- **Estado:** Cerrada — resultado negativo con criterio predefinido (borrador v0.1 con experimentos reproducibles)
- **Objetivo:** Comprobar si la representación añade información más allá de las métricas locales y los métodos de prototipos, con un criterio de éxito fijado antes de correr.
- **Principales hallazgos:** En 8 datasets (4 reales, 4 sintéticos con anisotropía controlada) y 15 folds pareados, el margen de resolución no supera a la mejor referencia ajustada (k-NN, centroides, LDA, QDA, regresión logística, random forest, DANN) en ningún dataset; es peor con IC 95 % en 6 y no concluyente en 2. La anisotropía sí añade información respecto a la versión isótropa del propio campo en 3 datasets (y la quita en 2), pero es redundante dadas las referencias; las puntuaciones puramente geométricas (volumen, anisotropía) están al nivel del azar o por debajo. Enunciado exacto: con la métrica igual a la inversa de la covarianza compartida, el margen de resolución es función monótona del margen posterior de LDA para dos clases equiprobables, iguala el doble del log-cociente de las dos mayores posteriores para cualquier número de clases, y su desviación bajo un campo arbitrario es $2(x-\bar m)^{\top}(A(x)-\Sigma^{-1})\delta$.
- **Alcance actual:** Formulación computacional sobre datasets públicos y sintéticos; no se afirma nada sobre fenómenos físicos ni cuánticos. La única vía abierta es una versión supervisada del campo o una regla bidimensional margen + volumen, bajo el mismo criterio.

## English

- **Code:** HQF001
- **Area:** Artificial intelligence and learning
- **Title:** Local resolution and uncertainty in learning
- **Short description:** Anisotropic resolution fields (a positive definite local metric per point, estimated from the data geometry) as a representation of uncertainty for abstention decisions, evaluated as selective classification.
- **Status:** Closed — negative result under a predefined criterion (working draft v0.1 with reproducible experiments)
- **Objective:** Test whether the representation adds information beyond local metrics and prototype-based methods, with a success criterion fixed before the run.
- **Main findings:** On 8 datasets (4 real, 4 synthetic with controlled anisotropy) and 15 paired folds, the resolution margin never beats the best tuned reference (k-NN, class centroids, LDA, QDA, logistic regression, random forest, DANN); it is worse with a 95% interval on 6 datasets and inconclusive on 2. Anisotropy does add information relative to the field's own isotropic version on 3 datasets (and removes it on 2), but is redundant given the references; purely geometric scores (volume, anisotropy) are at or below chance level. Exact statement: with the metric equal to the shared inverse covariance, the resolution margin is a monotone function of the LDA posterior margin for two equiprobable classes, equals twice the log-ratio of the two largest posteriors for any number of classes, and its departure under an arbitrary field is $2(x-\bar m)^{\top}(A(x)-\Sigma^{-1})\delta$.
- **Current scope:** Computational formulation on public and synthetic datasets; no claim about physical or quantum phenomena. The only open avenue is a supervised version of the field or a two-dimensional margin + volume rule, under the same criterion.
