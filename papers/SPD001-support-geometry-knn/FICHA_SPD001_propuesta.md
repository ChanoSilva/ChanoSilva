# Propuesta de actualización de la ficha SPD001 en el CV web

Texto propuesto para reemplazar la ficha actual (estado "En pausa"). Mantiene el formato de la página: título, descripción breve, estado, objetivo, principales hallazgos y alcance actual. Cifras tomadas de la corrida de referencia (semilla 20260930) descrita en `papers/SPD001-support-geometry-knn/`.

## Español

- **Código:** SPD001
- **Área:** Inteligencia artificial y aprendizaje
- **Título:** Geometría del soporte y vecinos cercanos
- **Descripción breve:** Descomposición de una consulta respecto de sus vecinos de clase en componentes tangencial, ortogonal y de profundidad, y comparación aislante frente a líneas de rasgos, cascos locales y clasificadores por profundidad.
- **Estado:** Cerrada con resultado negativo — Borrador v0.1 (manuscrito en LaTeX con experimentos reproducibles)
- **Objetivo:** Determinar, con un criterio fijado de antemano, si la descomposición añade información predictiva más allá de las líneas de rasgos, los cascos locales (HKNN) y las medidas de profundidad.
- **Principales hallazgos:** La distancia HKNN regularizada es exactamente una combinación ponderada de la componente ortogonal y de las coordenadas tangenciales (demostrado), de modo que la única componente nueva frente a los cascos es la profundidad. En 8 conjuntos (4 estándar, 4 variedades sintéticas) con validación cruzada 5×5 y referencias afinadas por leave-one-out, la combinación de las tres componentes no superó a la mejor referencia en ningún conjunto (se exigían 5 de 8 con IC bootstrap por encima de 0); las diferencias quedaron entre −0.8 y +0.2 puntos de exactitud. Las ablaciones sitúan la información en la componente ortogonal (quitarla cuesta hasta 5 puntos); quitar la profundidad o la tangencial no cambia la exactitud de forma significativa. Tampoco hay ganancia en exactitud selectiva ni en un barrido con hasta 20 coordenadas de ruido fuera de la variedad.
- **Alcance actual:** Estudio metodológico en conjuntos pequeños; excluye ganancias mayores de ~1 punto, no menores. Se probó una profundidad (espacial local) y una regla de combinación (logit condicional). No se afirma nada sobre dominios de aplicación.

## English

- **Code:** SPD001
- **Area:** Artificial intelligence and learning
- **Title:** Support geometry and nearest neighbors
- **Short description:** Decomposition of a query with respect to its class neighbours into tangential, orthogonal and depth components, and an isolating comparison against feature lines, local hulls and depth classifiers.
- **Status:** Closed with a negative finding — Working draft v0.1 (LaTeX manuscript with reproducible experiments)
- **Objective:** Determine, under a criterion fixed in advance, whether the decomposition adds predictive information beyond feature lines, local hulls (HKNN) and depth measures.
- **Main findings:** The regularised HKNN distance is exactly a weighted combination of the orthogonal component and the tangential coordinates (proved), so the only component new relative to hulls is the depth. On 8 datasets (4 standard, 4 synthetic manifolds) with 5×5 cross-validation and references tuned by leave-one-out, the three-component combination did not beat the best reference on any dataset (5 of 8 with a bootstrap interval above zero were required); differences lay between −0.8 and +0.2 accuracy points. Ablations locate the information in the orthogonal component (removing it costs up to 5 points); removing the depth or the tangential component does not change accuracy significantly. No gain in selective accuracy either, nor in a scan with up to 20 off-manifold noise coordinates.
- **Current scope:** Methodological study on small datasets; excludes gains larger than about 1 point, not smaller ones. One depth (local spatial depth) and one combination rule (conditional logit) were tested. No claim about application domains.
