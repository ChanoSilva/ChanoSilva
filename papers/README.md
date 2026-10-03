# papers/

Avances de líneas de investigación de Luciano Silva Alarco (PUCP) producidos en sesiones de Claude Code a partir de las fichas públicas del CV web. Cada carpeta es autocontenida: manuscrito LaTeX + PDF, experimentos con semilla fija, resultados, README y nota de continuidad en español.

| Carpeta | Código | Línea | Estado del avance |
|---|---|---|---|
| `MRT001-foundational-geometry/` | MRT001 | Invariantes y fundamentos geométricos | **v0.5** (20 pp.), tres rondas de revisión interna aplicadas; prueba de la Prop. 5.2 completada, conjetura E5f sobre la ley de realizadores |
| `SPD001-support-geometry-knn/` | SPD001 | Geometría del soporte y vecinos cercanos | **v0.2** (10 pp.), ronda 1 aplicada: comparación aislante con criterio predefinido, **resultado negativo** (0/8 en lecturas bootstrap y Nadeau–Bengio); cota de potencia +1.3/+3.5 puntos; propuesta de cierre |
| `LMI001-mechanical-clustering/` | LMI001 | Analogías mecánicas para agrupamiento | **v0.2** (13 pp.), ronda 1 aplicada: teorema "agrupamiento mecánico = agrupamiento por kernels" para la familia de pares reconstruida de la ficha (supuesto por confirmar); certificados exactos de lo que sale de la familia |
| `TCD001-lasso-selection-fragility/` | TCD001 | Fragilidad de la selección con Lasso | **v0.2** (10 pp.), ronda 1 aplicada: test exacto de eliminación, no monotonía, NP-completitud con p=1, números de fragilidad exactos hasta n=34; guarda KKT en el solver |
| `SGE001-frontier-aggregation/` | SGE001 | Agregación dinámica de fronteras productivas | **v0.2** (12 pp.), ronda 1 aplicada: certificado observable 2B₂<|Q₂|, fallo demostrado del segundo orden en umbrales de capacidad, nueva corrida de referencia con semillas por experimento |
| `RTK001-recursive-knots/` | RTK001 | Geometría de nudos recursivos | **v0.2** (11 pp.), ronda 1 aplicada: (H_c) reenunciada para la familia (falsa para bases arbitrarias, demostrado); caso de hebras distintas demostrado para p=2; cota inferior Rop ≥ L/r_d; abierto el caso misma hebra en f=1/2 |
| `HQF001-resolution-fields-abstention/` | HQF001 | Resolución local e incertidumbre | **v0.2** (10 pp.), ronda 1 aplicada: clasificación selectiva con tres tipos de intervalo, **resultado negativo** en las tres lecturas; propuesta de cierre para la formulación no supervisada evaluada |
| `EQO001-equilibrium-welfare/` | EQO001 | Operadores de equilibrio y bienestar | **v0.2** (14 pp.), ronda 1 aplicada: la pregunta abierta 1 queda cerrada por un cono no poliédrico explícito; contraejemplo nuevo para la pregunta 2; literatura de ineficiencia genérica incorporada |
| `SVMF001-boundary-families/` | SVMF001 | Familias de fronteras de clasificación | **v0.2** (14 pp.), ronda 1 aplicada: rejillas ampliadas bajo preregistro fechado y corrida nueva; enunciado exacto de cuándo la adaptación local no puede ayudar; **resultado negativo** se mantiene |
| `OMR001-transferable-corrections/` | OMR001 | Correcciones transferibles | **v0.2** (10 pp.), ronda 1 aplicada: imposibilidad para correcciones aprendidas en fuentes, cota explícita de no-daño (garantía de selección), corolario nuevo uniforme en θ; afirmación de cierre retirada |

Documentos transversales:
- `TRIAJE_lineas_en_pausa_20260930.md`: triaje de las 23 líneas en pausa y 4 archivadas, con bloqueos y pasos mínimos.

Revisión interna (02–03/10/2026): cada carpeta contiene el informe de un árbitro independiente (`REFEREE_*.md`) y la respuesta punto por punto del autor (`RESPUESTA_*.md`); MRT001 lleva tres rondas, el resto una. Todos los manuscritos compilan sin referencias indefinidas ni cajas desbordadas.

Convenciones: ningún número de los manuscritos está tipeado a mano (se generan desde `results/`); toda afirmación lleva estado explícito (demostrada aquí / clásica / literatura / verificada computacionalmente / conjetural); los resultados negativos se reportan como tales.
