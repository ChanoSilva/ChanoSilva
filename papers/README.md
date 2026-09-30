# papers/

Avances de líneas de investigación de Luciano Silva Alarco (PUCP) producidos en sesiones de Claude Code a partir de las fichas públicas del CV web. Cada carpeta es autocontenida: manuscrito LaTeX + PDF, experimentos con semilla fija, resultados, README y nota de continuidad en español.

| Carpeta | Código | Línea | Estado del avance |
|---|---|---|---|
| `MRT001-foundational-geometry/` | MRT001 | Invariantes y fundamentos geométricos | Borrador v0.4 (18 pp.), dos rondas de revisión interna aplicadas |
| `SPD001-support-geometry-knn/` | SPD001 | Geometría del soporte y vecinos cercanos | Borrador v0.1 (12 pp.): comparación aislante con criterio predefinido, **resultado negativo** (0/8 victorias); propuesta de cierre |
| `LMI001-mechanical-clustering/` | LMI001 | Analogías mecánicas para agrupamiento | Borrador v0.1 (15 pp.): teorema "agrupamiento mecánico = agrupamiento por kernels" (energías de pares, levantamiento, tensión, relajación = Hartigan); el cribado nulo de la ficha es consecuencia del teorema; queda abierta la vía dinámica |
| `TCD001-lasso-selection-fragility/` | TCD001 | Fragilidad de la selección con Lasso | Borrador v0.1 (15 pp.): test exacto de eliminación en forma cerrada, no monotonía de los testigos, NP-completitud de la deselección con p=1 (Subset Sum), números de fragilidad exactos hasta n=34; ninguna heurística cumple el criterio predefinido |
| `SGE001-frontier-aggregation/` | SGE001 | Agregación dinámica de fronteras productivas | Borrador v0.1 (15 pp.): identidades y cotas de resto en régimen suave, fallo demostrado del segundo orden en cruces de capacidad (E₂ = −N·T_u), condición de margen para comparaciones; criterio predefinido de mejora 5× no se cumple en general |
| `RTK001-recursive-knots/` | RTK001 | Geometría de nudos recursivos | Cotas de longitud de cuerda (ver su README) |
| `HQF001-resolution-fields-abstention/` | HQF001 | Resolución local e incertidumbre | Borrador v0.1 (11 pp.): comparación controlada de clasificación selectiva con criterio predefinido, **resultado negativo** (0/8 mejor, 6/8 peor); proposición exacta que aísla qué podría aportar la anisotropía; propuesta de cierre |
| `EQO001-equilibrium-welfare/` | EQO001 | Operadores de equilibrio y bienestar | Nota v0.1 (13 pp.): qué es y qué no es teorema; problemas abiertos |
| `SVMF001-boundary-families/` | SVMF001 | Familias de fronteras de clasificación | Borrador v0.1 (14 pp.): enunciado exacto de cuándo la adaptación local no puede ayudar (adelgazamiento binomial de la curva de aprendizaje), comparación controlada de cuatro familias con criterio predefinido, **resultado negativo** (0 familias cumplen) |
| `OMR001-transferable-corrections/` | OMR001 | Correcciones transferibles | Nota v0.1 (14 pp.): qué puede y qué no puede garantizarse; cota explícita de no-daño para la reversión validada (es una garantía de selección, no del operador); simulación con 345 configuraciones |

Documentos transversales:
- `TRIAJE_lineas_en_pausa_20260930.md`: triaje de las 23 líneas en pausa y 4 archivadas, con bloqueos y pasos mínimos.

Convenciones: ningún número de los manuscritos está tipeado a mano (se generan desde `results/`); toda afirmación lleva estado explícito (demostrada aquí / clásica / literatura / verificada computacionalmente / conjetural); los resultados negativos se reportan como tales.
