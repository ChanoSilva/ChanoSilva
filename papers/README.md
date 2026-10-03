# papers/

Avances de líneas de investigación de Luciano Silva Alarco (PUCP) producidos en sesiones de Claude Code a partir de las fichas públicas del CV web. Cada carpeta es autocontenida: manuscrito LaTeX + PDF, experimentos con semilla fija, resultados, README y nota de continuidad en español.

| Carpeta | Código | Línea | Estado del avance |
|---|---|---|---|
| `MRT001-foundational-geometry/` | MRT001 | Invariantes y fundamentos geométricos | **v0.6** (26 pp.), tres rondas de revisión interna; la ley de realizadores queda **demostrada** (Teorema 5.6: R_n = 2^{N_n} con probabilidad 1 − O(1/n), N_n → Poisson(1), tasas explícitas; Prop. 5.7 clasifica las excepciones) |
| `SPD001-support-geometry-knn/` | SPD001 | Geometría del soporte y vecinos cercanos | **v0.3** (10 pp.), dos rondas aplicadas: rejillas ampliadas bajo preregistro y corrida nueva; **resultado negativo** C1 = 0/8 en lecturas bootstrap y Nadeau–Bengio; atribución a la componente ortogonal en 5/8; propuesta de cierre |
| `LMI001-mechanical-clustering/` | LMI001 | Analogías mecánicas para agrupamiento | **v0.3** (12 pp.), dos rondas aplicadas: las equivalencias centrales se atribuyen a la literatura (Hofmann–Buhmann, Roth et al., Sejdinovic et al., França et al.); aporte propio declarado pequeño; familia reconstruida por confirmar |
| `TCD001-lasso-selection-fragility/` | TCD001 | Fragilidad de la selección con Lasso | **v0.4** (12 pp.), dos rondas aplicadas + teoría nueva: la selección es **NP-completa para p fijo ≥ 2** (ambas reglas), algoritmo pseudo-polinomial ⇒ dureza solo débil para p fijo; abierta la dureza fuerte con p creciente |
| `SGE001-frontier-aggregation/` | SGE001 | Agregación dinámica de fronteras productivas | **v0.3** (11 pp.), dos rondas aplicadas: certificados con microdatos y con momentos+rango separados; fallo demostrado del segundo orden en umbrales; criterio predefinido de mejora 5× no se cumple en general |
| `RTK001-recursive-knots/` | RTK001 | Geometría de nudos recursivos | **v0.3** (12 pp.), dos rondas aplicadas + teoría nueva: caso misma hebra **demostrado** sin hipótesis extra para (2,3); (H_c) con c = 1/2 demostrada en d = 1 para todo f ≤ 1/2; abierto (H_3) uniforme en d |
| `HQF001-resolution-fields-abstention/` | HQF001 | Resolución local e incertidumbre | **v0.3** (10 pp.), dos rondas aplicadas: rejilla ampliada bajo preregistro y corrida nueva; **resultado negativo** en las tres lecturas y con ambas rejillas; propuesta de cierre para la formulación no supervisada |
| `EQO001-equilibrium-welfare/` | EQO001 | Operadores de equilibrio y bienestar | **v0.3** (13 pp.), dos rondas aplicadas: cono de pesos no poliédrico (dos y tres mercancías, demostrado), pertenencia **co-NP-completa** (reducción desde MAX-CUT); las dos preguntas abiertas originales quedan resueltas |
| `SVMF001-boundary-families/` | SVMF001 | Familias de fronteras de clasificación | **v0.3** (12 pp.), dos rondas aplicadas: conclusiones afectadas marcadas como limitadas por la rejilla según el preregistro; enunciado exacto de cuándo la adaptación local no puede ayudar; **resultado negativo** |
| `OMR001-transferable-corrections/` | OMR001 | Correcciones transferibles | **v0.3** (10 pp.), dos rondas aplicadas: constantes κ(α) exactamente óptimas, tasa m^{-1/2} exacta con n_e fijo, cota uniforme 13× más fina; línea en pausa |

Documentos transversales:
- `TRIAJE_lineas_en_pausa_20260930.md`: triaje de las 23 líneas en pausa y 4 archivadas, con bloqueos y pasos mínimos.

Revisión interna (02–03/10/2026): cada carpeta contiene los informes de árbitros independientes (`REFEREE_*.md`) y las respuestas punto por punto del autor (`RESPUESTA_*.md`): dos rondas en nueve líneas y tres en MRT001. Las demostraciones nuevas obtenidas por agentes teóricos se verificaron de forma independiente antes de integrarse; sus salidas de verificación están congeladas con SHA-256. Todos los manuscritos compilan sin referencias indefinidas ni cajas desbordadas.

Convenciones: ningún número de los manuscritos está tipeado a mano (se generan desde `results/`); toda afirmación lleva estado explícito (demostrada aquí / clásica / literatura / verificada computacionalmente / conjetural); los resultados negativos se reportan como tales.
