# Propuesta de actualización de la ficha SVMF001 en el CV web

Texto propuesto para reemplazar la ficha actual (estado "En pausa"). Mantiene el formato de la página. Cifras tomadas de la corrida de referencia (semilla 20260930) descrita en `papers/SVMF001-boundary-families/`. Redactada por la sesión coordinadora a partir del README, la nota de continuidad y el resumen del manuscrito.

## Español

- **Código:** SVMF001
- **Área:** Inteligencia artificial y aprendizaje
- **Título:** Familias de fronteras de clasificación
- **Descripción breve:** Variantes de máquinas de vectores de soporte con frontera localmente adaptativa (SVM lineal por vecinos, SVM por celdas, RBF con ancho de banda variable definido positivo, mezcla suave de SVM lineales locales) frente a referencias globales emparejadas, con un enunciado exacto de cuándo la adaptación local no puede ayudar.
- **Estado:** Borrador v0.1 (reconstrucción autocontenida; manuscrito en LaTeX con demostraciones y comparación reproducible); resultado negativo bajo criterio predefinido
- **Objetivo:** Examinar estabilidad y valor adicional frente a referencias comparables, con un criterio de éxito fijado antes de correr.
- **Principales hallazgos:** Si la clase de la referencia ya contiene la regla de Bayes, la localización solo puede actuar sobre el error de estimación; para modelos locales ajustados en celdas independientes de la etiqueta, el riesgo esperado es una mezcla de la curva de aprendizaje de la referencia en tamaños binomialmente reducidos, así que nunca es menor si la curva es no creciente y es estrictamente mayor si es estrictamente decreciente (demostrado). En el modelo gaussiano con umbral de centroides todo es cerrado: con n = 320 y cuatro celdas el exceso de riesgo se multiplica por 4.08. En la comparación controlada (6 conjuntos, validación cruzada repetida, referencias ajustadas por CV interna, cada familia contiene a su referencia como caso particular), ninguna familia cumplió el criterio de mayoría: de 24 celdas, 8 intervalos quedan por debajo de cero y uno por encima, y ese último desaparece frente a la mejor de las dos referencias. En el régimen multiescala diseñado para favorecer la adaptación local, la familia de ancho de banda variable empata con la RBF-SVM. Ninguna familia es más robusta con 20 % de ruido en etiquetas ni con 25 % de submuestreo.
- **Alcance actual:** Las variantes originales de la línea no están disponibles; todo es una reconstrucción declarada. Conjuntos de hasta 400 puntos. No se afirma superioridad general en robustez ni en clasificación, y el enunciado exacto no cubre la localización por vecinos ni particiones dependientes de los datos.

## English

- **Code:** SVMF001
- **Area:** Artificial intelligence and learning
- **Title:** Families of classification boundaries
- **Short description:** Support vector machine variants with locally adaptive boundaries (kNN linear SVM, cell-partitioned SVM, positive-definite variable-bandwidth RBF, soft mixture of local linear SVMs) against matched global references, with an exact statement of when local adaptation cannot help.
- **Status:** Working draft v0.1 (self-contained reconstruction; LaTeX manuscript with proofs and a reproducible comparison); negative result under a predefined criterion
- **Objective:** Examine stability and added value against comparable references, with a success criterion fixed before running.
- **Main findings:** If the reference's class already contains the Bayes rule, localisation can only act on the estimation error; for local models fitted on label-independent cells the expected risk is a mixture of the reference's learning curve at binomially thinned sample sizes, hence never smaller when that curve is non-increasing and strictly larger when it is strictly decreasing (proved). In the Gaussian location model with the centroid threshold everything is closed-form: with n = 320 and four cells the excess risk is multiplied by 4.08. In the controlled comparison (6 data sets, repeated cross-validation, references tuned by inner CV, each family containing its reference as a special case), no family met the majority criterion: of 24 cells, 8 intervals lie below zero and one above, and that one disappears against the better of the two references. In the multi-scale regime designed to favour local adaptation, the variable-bandwidth family matched but did not beat the RBF-SVM. No family is more robust under 20 % label noise or 25 % subsampling.
- **Current scope:** The line's original variants are not available; everything is a declared reconstruction. Data sets of up to 400 points. No general superiority in robustness or classification is claimed, and the exact statement does not cover neighbour-based localisation or data-dependent partitions.
