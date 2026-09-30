# Propuesta de actualización de la ficha SGE001 en el CV web

Texto propuesto para reemplazar la ficha actual (estado "En pausa"). Mantiene el formato de la página. Cifras tomadas de la corrida de referencia (semilla 20260930) descrita en `papers/SGE001-frontier-aggregation/`. Redactada por la sesión coordinadora a partir del README, la nota de continuidad y el resumen del manuscrito.

## Español

- **Código:** SGE001
- **Área:** Estadística y medición
- **Título:** Agregación dinámica de fronteras productivas
- **Descripción breve:** Error de agregar unidades con una frontera cóncava común mediante la unidad representativa y su corrección de segundo orden por covarianza de insumos, en régimen suave y en cruces de umbral de capacidad.
- **Estado:** Borrador v0.1 (manuscrito en LaTeX con demostraciones y simulación reproducible); resultado principal negativo para la mejora general
- **Objetivo:** Hacer preciso el error de las aproximaciones de primer y segundo orden, establecer cuándo la corrección de segundo orden mejora y qué puede certificarse para comparaciones entre agregados.
- **Principales hallazgos:** En régimen suave se demuestra una identidad exacta del resto y una cota del error de segundo orden por el tercer momento absoluto de los insumos, con constante calculable para fronteras Cobb–Douglas; el factor de mejora crece como el inverso de la dispersión y las cotas se cumplen en todas las poblaciones simuladas. En un umbral de capacidad se demuestra que el error de segundo orden es igual a −N·T_u salvo términos de segundo orden, donde T_u es la distancia media unilateral de los productos individuales a la capacidad; T_u es lineal en la dispersión cuando hay unidades a ambos lados, así que el segundo orden no aporta nada (razón de errores → 1). Una condición de margen certifica que la aproximación conserva el orden de dos agregados; entre las comparaciones certificadas no hubo reversiones, pero el certificado cubre una fracción decreciente de los pares y nunca existe en un cruce, donde dos poblaciones con iguales media y covarianza pueden tener agregados distintos a primer orden. El criterio predefinido de mejora uniforme de 5× se cumple con insumos simétricos, falla con log-normales por encima de σ ≈ 0.42 y falla en 15 de 23 celdas con capacidad; una recalibración escalar del término de segundo orden no lo restaura.
- **Alcance actual:** Simulación controlada con fronteras Cobb–Douglas y CES y poblaciones sintéticas. No se afirma nada sobre sectores reales, fronteras estimadas ni decisiones de política. Las nociones de "dinámica", "jerarquía" y "calibración posterior" fueron reconstruidas de la ficha (no existe manuscrito previo) y deben confirmarse con el autor.

## English

- **Code:** SGE001
- **Area:** Statistics and measurement
- **Title:** Dynamic aggregation of production frontiers
- **Short description:** Error of aggregating units that share a concave frontier through the representative unit and its second-order input-covariance correction, in the smooth regime and at capacity-threshold crossings.
- **Status:** Working draft v0.1 (LaTeX manuscript with proofs and a reproducible simulation); main finding negative for a general improvement
- **Objective:** Make the error of the first- and second-order approximations precise, establish when the second-order correction helps, and state what can be certified for comparisons between aggregates.
- **Main findings:** In the smooth regime an exact remainder identity and a bound of the second-order error by the third absolute moment of the inputs are proved, with a computable constant for Cobb–Douglas frontiers; the improvement factor grows like the inverse dispersion and the bounds hold in every simulated population. At a capacity threshold the second-order error is proved to equal −N·T_u up to second-order terms, where T_u is the one-sided mean distance of the individual outputs to the capacity; T_u is linear in the dispersion when units straddle the threshold, so the second order adds nothing (error ratio → 1). A margin condition certifies that the approximation preserves the ordering of two aggregates; no reversal occurred among certified comparisons, but the certificate covers a shrinking share of pairs and is never available at a crossing, where two populations with identical mean and covariance can have aggregates that differ at first order. The predefined criterion of a uniform fivefold improvement holds for symmetric inputs, fails for log-normal inputs above σ ≈ 0.42 and fails in 15 of 23 capacity cells; a scalar recalibration of the second-order term does not restore it.
- **Current scope:** Controlled simulation with Cobb–Douglas and CES frontiers and synthetic populations. Nothing is claimed about real sectors, estimated frontiers or policy decisions. The notions of "dynamic", "hierarchical" and "later calibration" were reconstructed from the public record (no earlier manuscript exists) and should be confirmed by the author.
