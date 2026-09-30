# Propuesta de actualización de la ficha LMI001 en el CV web

Texto propuesto para reemplazar la ficha actual (estado "En pausa"). Mantiene el formato de la página: título, descripción breve, estado, objetivo, principales hallazgos y alcance actual. Cifras tomadas de la corrida de referencia (semillas 20260930 y 20260931).

## Español

- **Código:** LMI001
- **Área:** Inteligencia artificial y aprendizaje
- **Título:** Analogías mecánicas para agrupamiento de datos
- **Descripción breve:** Estudio de formulaciones de agrupamiento inspiradas en tensión, levantamiento y sistemas mecánicos, y del teorema que las reduce a agrupamiento por kernels.
- **Estado:** Cerrada con resultado — Borrador v0.1 (manuscrito en LaTeX con demostraciones y experimentos reproducibles)
- **Objetivo:** Determinar si el componente mecánico produce un efecto distinguible frente a controles de kernel emparejados, y explicar el resultado.
- **Principales hallazgos:** Toda energía elástica de pares (resortes con cualquier potencial φ(d), con o sin levantamiento, normalizada por partícula) es, salvo una constante, el objetivo de kernel k-means de la matriz −φ(D) (demostrado); los resortes de Hooke dan k-means exactamente; si φ(d) = ψ(d²) con ψ de Bernstein, el teorema de Schoenberg da un kernel definido positivo universal y el resorte es un resorte de Hooke sobre una configuración levantada; la energía total y su dual de tensión son min-sum k-clustering / max-k-cut; la relajación a temperatura cero del sistema de resortes es el método de Hartigan y sus puntos fijos son puntos fijos de Lloyd. Confirmación computacional: identidad de valores en 19 285/19 285 comprobaciones (error máximo 1×10⁻¹¹), trayectorias idénticas de la implementación física y la kernel en 90/90 corridas, 600/600 puntos fijos de la relajación estables de Voronoi. Con aritmética exacta se certifica que términos de muchos cuerpos, longitudes de reposo adaptativas y normalización por resorte salen de la familia.
- **Alcance actual:** El cribado nulo es consecuencia de la equivalencia, no de un experimento fallido. No se afirma nada sobre calidad de agrupamiento en datos reales. Queda abierta, formulada como problema y conjetura, la vía dinámica (relajación de posiciones, tipo gravitacional o mean shift).

## English

- **Code:** LMI001
- **Area:** Artificial intelligence and learning
- **Title:** Mechanical analogies for data clustering
- **Short description:** A study of clustering formulations inspired by tension, lifting and mechanical systems, and of the theorem that reduces them to kernel clustering.
- **Status:** Closed with a result — Working draft v0.1 (LaTeX manuscript with proofs and reproducible experiments)
- **Objective:** Determine whether the mechanical component produces an effect distinguishable from matched kernel controls, and explain the outcome.
- **Main findings:** Every pairwise elastic energy (springs with any potential φ(d), with or without a lift, normalised per particle) is, up to a constant, the kernel k-means objective of the matrix −φ(D) (proved); Hooke springs give k-means exactly; if φ(d) = ψ(d²) with ψ a Bernstein function, Schoenberg's theorem yields a universal positive definite kernel and the spring is a Hooke spring on a lifted configuration; the total energy and its tension dual are min-sum k-clustering / max-k-cut; the zero-temperature relaxation of the spring system is Hartigan's method and its fixed points are Lloyd fixed points. Computational confirmation: identical values in 19,285/19,285 checks (max error 1×10⁻¹¹), identical trajectories of the physical and the kernel implementation in 90/90 runs, 600/600 relaxation fixed points Voronoi-stable. Exact arithmetic certifies that many-body terms, adaptive rest lengths and per-spring normalisation leave the family.
- **Current scope:** The null screening is a consequence of the equivalence, not a failed experiment. Nothing is claimed about clustering quality on real data. The dynamic route (relaxation of positions, gravitational or mean-shift type) remains open, stated as a problem and a conjecture.
