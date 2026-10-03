# Propuesta de actualización de la ficha MRT001 en el CV web

Texto propuesto para reemplazar la ficha actual (estado "En pausa — Desarrollo conceptual suspendido") en `investigacion.html` y `research-en.html`. Mantiene el formato de la página: título, descripción breve, estado, objetivo, principales hallazgos y alcance actual. Cifras tomadas de la corrida de referencia (semilla 20260930).

## Español

- **Código:** MRT001
- **Área:** Matemáticas y estructuras
- **Título:** Invariantes y fundamentos geométricos
- **Descripción breve:** Lenguaje mínimo de formalismos, traducciones e invariantes para precisar en qué sentido una estructura "precede" a una descripción geométrica, aplicado a la cadena euclidiana finita y a la cadena de orden causal en 1+1.
- **Estado:** En desarrollo — Borrador v0.6 (manuscrito en LaTeX con experimentos reproducibles y tres rondas de revisión interna; Conjetura 5.3 demostrada)
- **Objetivo:** Precisar qué afirmaciones sobre estructuras previas a la geometría pueden formularse y contrastarse dentro de marcos matemáticos definidos, separando lo demostrado, lo medido y lo conjetural.
- **Principales hallazgos:** Las primitivas de Tarski (intermediación y congruencia) son vacías en muestras finitas genéricas (demostrado; 0 instancias en 4000 configuraciones con aritmética exacta). El orden de las distancias no determina la forma para ningún tamaño finito, pero la recupera asintóticamente salvo semejanza (disparidad de Procrustes mediana 2×10⁻¹⁰ con 256 puntos, con la salvedad de que el solver solo aproxima la clase ordinal). Las cantidades geométricas usuales se ordenan por "profundidad de formalismo": árbol generador mínimo, grafo k-NN y grafo de vecindad relativa son ordinales; diámetro, dimensión afín y grafo de Gabriel son métricos. En la cadena lorentziana 1+1, el núcleo de la traducción al orden causal contiene al grupo conforme y coincide con él para cerca de un tercio de las muestras finitas uniformes (realizador único del orden); el número de realizadores sigue asintóticamente la ley 2^{Poisson(1)}, demostrado: es 2^N, con N el número de pares de puntos adyacentes en ambos órdenes de coordenadas con sentidos opuestos, salvo con probabilidad 5/n + O(n⁻²), y la prueba usa un único resultado citado (teorema de Gallai sobre grafos de comparabilidad primos); el orden solo estima la dimensión y, con el conteo, recupera tiempos propios y coordenadas.
- **Alcance actual:** Modelo matemático sobre fondos fijos (cubo euclidiano, diamante de Minkowski 1+1). No se presenta como teoría unificada ni como evidencia experimental; las tasas finitas observadas no están demostradas.

## English

- **Code:** MRT001
- **Area:** Mathematics and structures
- **Title:** Invariants and geometric foundations
- **Short description:** A minimal language of formalisms, translations and invariants that makes precise in what sense a structure "precedes" a geometric description, worked out on the finite Euclidean chain and on the causal-order chain in 1+1 dimensions.
- **Status:** In development — Working draft v0.6 (LaTeX manuscript with reproducible experiments and three internal review rounds; Conjecture 5.3 proved)
- **Objective:** Specify which claims about structures preceding geometry can be formulated and tested within defined mathematical frameworks, separating what is proved, what is measured and what is conjectural.
- **Main findings:** Tarski's primitives (betweenness and congruence) are empty on generic finite samples (proved; no instance in 4000 exact-arithmetic configurations). The ranking of distances does not determine shape at any finite size but recovers it asymptotically up to similarity (median Procrustes disparity 2×10⁻¹⁰ with 256 points, with the caveat that the solver only approximates the ordinal class). Standard geometric quantities sort by "formalism depth": minimum spanning tree, k-NN graph and relative neighbourhood graph are ordinal; diameter, affine dimension and Gabriel graph are metric. In the 1+1 Lorentzian chain the kernel of the causal-order translation contains the conformal group and coincides with it for about a third of finite uniform samples (unique realizer of the order); the number of realizers asymptotically follows the law 2^{Poisson(1)}, proved: it equals 2^N, with N the number of pairs of points adjacent in both coordinate orders with opposite directions, except with probability 5/n + O(n⁻²), and the proof uses a single cited result (Gallai's theorem on prime comparability graphs); the order alone estimates dimension and, with counting, recovers proper times and coordinates.
- **Current scope:** A mathematical model on fixed backgrounds (Euclidean cube, 1+1 Minkowski diamond). Not presented as a unified theory or as experimental evidence; the observed finite-sample rates are not proved.
