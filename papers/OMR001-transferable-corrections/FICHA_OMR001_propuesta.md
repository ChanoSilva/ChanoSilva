# Propuesta de actualización de la ficha OMR001 en el CV web

Texto propuesto para reemplazar la ficha actual (estado "En pausa"). Mantiene el formato de la página. Cifras tomadas de la corrida de referencia (semilla 20260930).

## Español

- **Código:** OMR001
- **Área:** Estadística y medición
- **Título:** Correcciones transferibles entre tareas de estimación
- **Descripción breve:** Formalización de "corrección post-estimación con reversión a una referencia segura" y demostración de qué garantía admite: una cota explícita de no-daño que es una garantía de selección por muestra retenida, no del operador.
- **Estado:** Cerrada con nota técnica — Borrador v0.1 (manuscrito en LaTeX con demostraciones y simulación reproducible)
- **Objetivo:** Establecer qué puede y qué no puede garantizarse para correcciones aprendidas en tareas fuente y aplicadas a una tarea objetivo con reversión validada.
- **Principales hallazgos:** Ninguna corrección fijada de antemano o aprendida en fuentes no informativas mejora el riesgo minimax de la referencia (demostrado); en una o dos dimensiones toda regla que use alguna vez la corrección es peor que la referencia en algún punto. Con un test unilateral de nivel α sobre una muestra retenida de tamaño m, el riesgo del estimador con reversión excede al de la referencia en a lo sumo min{α·E[Δ⁺], φ(z₁₋α)·2σ·E‖C−R‖/√m}, la probabilidad de transferencia dañina es ≤ α y la constante es óptima salvo un factor explícito (demostrado; verificado en 345 configuraciones). El estimador con reversión es selección por muestra retenida entre dos candidatos, lo que hace precisa la conclusión previa de la línea. En la simulación, la construcción con garantía solo es útil (≥5 % de ganancia sobre la media con todos los datos) cuando las tareas son casi idénticas, porque la partición cuesta más que la transferencia; las variantes útiles en un rango amplio (reajuste tras el chequeo, reversión por SURE) son construcciones clásicas sin garantía demostrada aquí.
- **Alcance actual:** Modelo gaussiano de localización con varianza conocida y una familia estructural jerárquica. No se afirma mejora general de exactitud, garantía de transferencia ni nada sobre poblaciones reales.

## English

- **Code:** OMR001
- **Area:** Statistics and measurement
- **Title:** Transferable corrections across estimation tasks
- **Short description:** A formalisation of "post-estimation correction with reversion to a safe reference" and a proof of the guarantee it admits: an explicit do-no-harm bound that is a hold-out selection guarantee, not a property of the operator.
- **Status:** Closed with a technical note — Working draft v0.1 (LaTeX manuscript with proofs and a reproducible simulation)
- **Objective:** Establish what can and cannot be guaranteed for corrections learned on source tasks and applied to a target task with validated reversion.
- **Main findings:** No correction fixed in advance or learned from non-informative sources improves the minimax risk of the reference (proved); in one or two dimensions any rule that ever uses the correction is worse than the reference somewhere. With a one-sided level-α test on a held-out sample of size m, the risk of the reverting estimator exceeds that of the reference by at most min{α·E[Δ⁺], φ(z₁₋α)·2σ·E‖C−R‖/√m}, the probability of harmful transfer is ≤ α, and the constant is sharp up to an explicit factor (proved; verified in 345 configurations). The reverting estimator is hold-out selection between two candidates, which makes the line's earlier conclusion precise. In the simulation the guaranteed construction is useful (≥5 % gain over the full-data mean) only when tasks are nearly identical, because the split costs more than the transfer gains; the variants useful over a wide range (refit after the check, SURE-based reversion) are classical constructs with no guarantee proved here.
- **Current scope:** Gaussian location model with known variance and one hierarchical structural family. No general accuracy improvement, no transfer guarantee and nothing about real populations is claimed.
