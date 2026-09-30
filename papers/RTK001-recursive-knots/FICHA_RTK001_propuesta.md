# Propuesta de actualización de la ficha RTK001 en el CV web

Texto propuesto para reemplazar la ficha actual (estado "En pausa"). Mantiene el formato de la página: título, descripción breve, estado, objetivo, principales hallazgos y alcance actual. Cifras tomadas de la corrida de referencia (`results/results.json`, determinista, N_0 = 1024).

## Español

- **Código:** RTK001
- **Área:** Matemáticas y estructuras
- **Título:** Geometría de nudos recursivos
- **Descripción breve:** Familia explícita de nudos anidados (cables iterados por desplazamiento en un marco de Bishop cerrado) y estudio de la longitud de cuerda necesaria para representarlos como tubos sin autointersección.
- **Estado:** En desarrollo — Borrador v0.1 (manuscrito en LaTeX con experimentos reproducibles; pendiente de revisión interna)
- **Objetivo:** Construir configuraciones factibles de nudos recursivos y precisar qué puede afirmarse sobre sus cotas de longitud y grosor, separando lo demostrado, lo medido y lo conjetural.
- **Principales hallazgos:** Para la familia fijada se demuestra que cada nivel es una curva embebida si el radio de desplazamiento no supera la mitad del grosor del nivel anterior, que el marco usado tiene número de enlace igual al entero más próximo al writhe (lo que identifica el tipo de nudo de cada nivel como un cable explícito), y una cota de longitud recursiva. Bajo una hipótesis local sobre el grosor, verificada numéricamente pero no demostrada, la cota de ropelength crece geométricamente con la profundidad con constante explícita. Polígonos explícitos dan ropelength poligonal 38.4, 155.6 y 622.7 en profundidades 1, 2 y 3 (patrón (2,3)), estables al 0.03 % al duplicar la resolución; el tipo de nudo del segundo nivel cambia dentro de la malla de parámetros porque el writhe del trébol cruza 3.5.
- **Alcance actual:** Cotas superiores verificadas numéricamente para polígonos explícitos, no grosores suaves certificados. No se certifica estacionariedad ni optimalidad; no se establece una ley de flujo recursiva; no se derivan cotas inferiores nuevas (el número de cruces de los cables iterados no se conoce en general).

## English

- **Code:** RTK001
- **Area:** Mathematics and structures
- **Title:** Geometry of recursive knots
- **Short description:** An explicit family of nested knots (iterated cables by offsets in a closed Bishop frame) and a study of the rope length needed to represent them as tubes without self-intersection.
- **Status:** In development — Working draft v0.1 (LaTeX manuscript with reproducible experiments; internal review pending)
- **Objective:** Construct feasible configurations of recursive knots and make precise what can be claimed about their length and thickness bounds, separating what is proved, what is measured and what is conjectural.
- **Main findings:** For the fixed family, each level is proved to be an embedded curve when the offset radius is at most half the previous thickness; the frame used has linking number equal to the nearest integer to the writhe, which identifies the knot type of each level as an explicit cable; and a recursive length bound holds. Under a local thickness hypothesis, verified numerically but not proved, the ropelength bound grows geometrically with depth with an explicit constant. Explicit polygons give polygonal ropelength 38.4, 155.6 and 622.7 at depths 1, 2 and 3 (pattern (2,3)), stable to 0.03% under doubling of the resolution; the depth-two knot type changes inside the parameter grid because the writhe of the trefoil crosses 3.5.
- **Current scope:** Numerically verified upper bounds for explicit polygons, not certified smooth thicknesses. Neither stationarity nor optimality is certified; no recursive flow law is established; no new lower bounds are derived (the crossing number of iterated cables is not known in general).
