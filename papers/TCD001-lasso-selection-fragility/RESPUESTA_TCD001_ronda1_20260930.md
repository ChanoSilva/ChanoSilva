# Respuesta del autor al informe de árbitro interno — TCD001, ronda 1 (30/09/2026)

Respuesta redactada el 03/10/2026 sobre el borrador v0.1; el resultado es el borrador **v0.2** (`manuscript/main.pdf`, 10 páginas; `results/` regenerado en una sola sesión). Documento construido de forma incremental durante la sesión.

Convenciones: **Aceptado** = se aplicó el cambio tal como se pidió; **Aceptado con matiz** = se aplicó una versión y se explica la diferencia; **Rebatido** = no se aplica, con la demostración o el cálculo. Numeración de resultados según el PDF (Lema 2.4; Prop. 3.1; Cor. 3.2; Obs. 3.3; Prop. 3.4; Obs. 3.5; Prop. 4.1; Ej. 4.2 y 4.3; Teo. 5.1; Obs. 5.2; Conj. 5.3); en v0.2 se conserva idéntica (por eso no se fusionó la Obs. 3.3 en el Cor. 3.2, ver recorte 6).

## Recuento

| | Aceptados | Aceptados con matiz | Rebatidos |
|---|---|---|---|
| Bloqueante (1) | B1 | — | — |
| Mayores (7) | M1, M2, M3, M4, M5, M7 | M6 | — |
| Menores (17) | m1–m9, m11–m17 | m10 | — |
| Recortes propuestos (8) | 1, 2, 3, 4, 7, 8 | 5, 6 | — |
| **Total hallazgos (25)** | **23** | **2** | **0** |

Ningún número no temporal del manuscrito cambió. Todos los conteos, porcentajes, medias y veredictos de v0.1 se reprodujeron en la corrida v0.2; solo cambiaron tiempos y cocientes de coste (ver "Números que cambiaron").

## Hallazgo bloqueante

### B1 — Cor. 3.2 enuncia `h_i < 1` como incondicional. **Aceptado.**

El árbitro tiene razón: el enunciado era incondicional y la prueba condicional. Su contraejemplo (n = p = 2, X = I₂, y = (3,3)ᵀ, μ = 1) es correcto: β̂ = (2,2)ᵀ, S = {1,2}, A = I, h₁ = h₂ = 1; quitar una observación deja X_{S,−i} con una columna nula.

- **Enunciado** reescrito con la hipótesis `h_i < 1` (equivalente a rango completo de X_{S,−i}); `h_i = 1` se remite al caso (a) de la Prop. 3.1 (rango deficiente, (S, s) no se conserva); convención ι_i := +∞ cuando h_i = 1, de modo que `max_i ι_i < 1 ⇒ f ≥ 2` vale sin excepción. Se añaden las convenciones de m11 (Sᶜ = ∅ ⇒ γ = +∞ y segundo término 0; γ = 0 es frontera KKT y queda excluido) y una precisión sobre qué residuo es r (m15). La prueba incorpora el contraejemplo como muestra de que la hipótesis no es vacua.
- **Código**: `single_removal_indices` (`lasso_fragility.py`) trata explícitamente `h_i ≥ 1 − 10⁻¹²` con `e_i = ι_i = +∞` y devuelve una máscara `rank_deficient` (antes dependía de la división por cero de NumPy, que da `inf` pero daría `nan` si además r_i = 0). El contraejemplo es ahora una comprobación ejecutable, `experiments/check_b1_counterexample.py`: `removal_test` devuelve "no conservado" por rango (det(I − H_R) = 0) para R = {1} y R = {2}, ι = +∞ en ambas observaciones, y una instancia genérica no cambia.
- **Hallazgo colateral** (gracias al contraejemplo): `sklearn.linear_model.lars_path` devuelve un camino erróneo cuando dos variables entran exactamente a la misma penalización (en esta instancia da β = (5, 2), que viola KKT con error 3.0; descenso por coordenadas o un empate roto por 10⁻⁹ dan (2, 2)). Es un caso de probabilidad cero en diseños continuos y, en los ejemplos enteros, el certificado exacto lo habría detectado (los 26 subconjuntos del Ej. 4.3 pasan la verificación KKT exacta). Aun así, `lasso_lars` verifica ahora KKT en cada ajuste (tolerancia relativa 10⁻⁸) y retrocede a descenso por coordenadas si falla; en las corridas de referencia el retroceso nunca se activa (todos los números coinciden con v0.1). Documentado en el Apéndice A ("Solver"), en Limitations y en la nota de continuidad.

## Hallazgos mayores

### M1 — El test decide "(S, s) se conserva", no "R es testigo"; falta la unicidad en D∖R. **Aceptado.**
Párrafo nuevo tras la Prop. 3.1 con el texto propuesto (unicidad c.s. por posición general en diseños continuos, cita a Tibshirani 2013; para datos enteros la unicidad se certifica en exacto; para los otros objetivos se reajusta). Frase añadida en Limitations, en la fila correspondiente de la tabla de afirmaciones y en el docstring de `fragility_exact`.

### M2 — Sobreafirmación de cierre en introducción y ficha. **Aceptado.**
`main.tex` (intro): sustituido por el texto propuesto ("gives the line a precise core: it proves what can be proved, reports which certificates are loose, and shows that on small synthetic instances the predefined advantage criterion is not met because exhaustive search with the closed-form test is already cheap; novelty is not claimed"). Resumen: "at n ≤ 14" junto a la afirmación sobre un décimo del coste exhaustivo. Ficha (`FICHA_TCD001_propuesta.md`, español e inglés): párrafo "Principales hallazgos" con el texto propuesto (familias elegidas tras un barrido piloto; 52 % y 92 %; a n = 34 el greedy cuesta el 7 % con 89 % de exactitud; "en parte porque..."). README: la frase "cierra en negativo lo que la ficha dejaba abierto" se reemplazó por la misma formulación. Coincido además con el cálculo del árbitro: con un reajuste de ≈ 0.44–0.57 ms y una búsqueda exhaustiva de ANY de ≈ 2 ms en la familia A, el criterio de coste ≤ 10 % es inalcanzable por construcción a n ≤ 14; el manuscrito lo dice ahora (párrafo "Pre-specification and changes" y E3).

### M3 — Decisiones tomadas tras ver resultados sin declarar; `results/` con dos versiones de la biblioteca. **Aceptado.**
(a) Párrafo "Pre-specification and changes" en la Sec. 6: criterio fijado en el código antes de toda corrida y registrado en `fragility.json`; familias elegidas tras un barrido piloto no incluido (rango de c, n ≤ 14, casi todas f = 1 con c ≤ 1; A la más estable sin soporte siempre verdadero); greedy de un paso corregido tras una primera corrida completa (puntuación por el margen del objetivo en vez de cualquier ruptura) con repetición de E2/E3/E5; nota sobre la contabilidad de tiempos (M5). (b) Los cuatro scripts se corrieron en una sola sesión con la biblioteca final (03/10/2026 04:08:11–04:09:40 UTC, `results/run_session_v02_start.txt`; 84 s de CPU), y se regeneraron `results/*.json`, `*.md`, logs, tiempos, `numbers.tex`, `table_*.tex`, figuras y PDF. El `fallback` inalcanzable del greedy se eliminó (no afecta a ningún resultado, como anticipó el árbitro).

### M4 — `examples.json` sin el Ejemplo 1b. **Aceptado.**
Regenerado; `examples.json` tiene ahora `example1b` y el log imprime "Example 1b (enter) verified exactly under both rules". Macro nueva `\ExOneChecks` = 12/12 (conjuntos de datos × reglas verificados en exacto para los Ej. 4.2 "sale" y "entra"), citada en el Ej. 4.2.

### M5 — Errores típicos en E3 y cronómetros asimétricos. **Aceptado.**
Texto de E3: estimaciones puntuales sobre 206–240 instancias con errores típicos de 0.4–3.1 puntos; el déficit del greedy en ENTER (86 %/88 % frente a 90 %) está a 1.7 y 1.1 errores típicos del umbral y "no debe leerse como un fracaso establecido". Tabla E3: columna "exact ± s.e." (error típico binomial) y columna "adj. cost ratio". Contabilidad de tiempos: a cada heurística se le descuenta el tiempo de un reajuste (estimado por instancia como su tiempo total dividido por su número de reajustes, lo que también descuenta un paso de puntuación y favorece a la heurística); el mínimo cociente de coste mediano ajustado sobre las 18 combinaciones es 0.26 (bruto 0.46), así que ningún veredicto cambia; dicho en "Pre-specification and changes" y en E3. Todas estas cantidades son macros generadas por `make_numbers.py`.

### M6 — Tabla 8 `[H]` desbordada. **Aceptado con matiz.**
El `Overfull \vbox` desapareció (0 cajas desbordadas en la compilación final). No suprimí la tabla de afirmaciones porque el brief original de la línea exige una "tabla de afirmaciones y estado" en el manuscrito; la compacté (11 filas fusionadas, `footnotesize`, `[!htb]`, columnas `p{}` para que el estado se parta) y conservé "Limitations" y "Next steps". Si en una versión para envío se prefiere suprimirla, las etiquetas `\status{}` en línea ya cubren cada afirmación.

### M7 — Obs. 3.5 atribuye la regla P a Meinshausen–Bühlmann. **Aceptado.**
Reformulada con el texto propuesto: penalización fija cuya regla (C o P) depende de la parametrización (forma suma en el artículo original, forma por observación en el software habitual); bajo la regla que se use, f_leave(j) > ⌈n/2⌉ ⇒ Π_j = 1. Mi recuerdo coincide con el del árbitro (forma suma con λ fijo en el artículo de 2010, es decir, regla C en nuestra notación), pero no pude cotejarlo con el PDF en esta sesión; queda anotado como pendiente en la nota de continuidad.

## Hallazgos menores

| Id | Decisión | Qué se cambió y dónde |
|---|---|---|
| m1 | Aceptado | Numeración unificada con el PDF en README, CONTINUIDAD y docstrings de `lasso_fragility.py`, `run_validation.py`, `run_scaling.py` (Prop. 3.1 / Cor. 3.2 / Prop. 3.4 / Obs. 3.5). La numeración del PDF no cambió entre v0.1 y v0.2. |
| m2 | Aceptado | Coste de la Prop. 3.4: O(nps₀ + pn log n) (ordenar p+1 vectores; O(np) con selección). También en CONTINUIDAD. |
| m3 | Aceptado | Teo. 5.1(a): "equivalently the unsigned f_ANY, since for p = 1 every unsigned change is a deselection". |
| m4 | Aceptado | Entrada `woodbury1950` (Memorandum Report 42, SRG Princeton) añadida y citada: "Sherman–Morrison–Woodbury identity \citep{sherman1950,woodbury1950,hager1989}". |
| m5 | Aceptado | `kuschnig2021` pasa a `@techreport` CESifo Working Paper 8981, Múnich, 2021, y se cita en la frase de heurísticas ("adaptive heuristics for influential sets"), no en la de algoritmos exactos. `broderick2020` con "v4 (2023)". |
| m6 | Aceptado | E1: "15 instances per cell for the comparison with refits and 30 fresh instances per cell for the certificates" (macro `\EoneCorInstancesPerCell`). `make_numbers.py`: helper `pctcell` imprime "--" sin "%" (visible en `table_e1b.tex` y `results/`). |
| m7 | Aceptado | E4: "mean g/n ≈ 0.028" y "over the 113 family-A instances with n ≥ 22 and finite f the median cost ratio is 0.774 (0.68 over all 120 instances with n ≥ 22)"; README dice g/n. Macros nuevas `\EfourACostOnestepMedianBigAll`, `\EfourANBigAll`. |
| m8 | Aceptado | E4: "censored mean fragility number (instances above the cap excluded, which biases the mean downwards as n grows; medians are in results/scaling.md)". README: "media censurada". |
| m9 | Aceptado | Resumen reducido de ≈ 450 a ≈ 190 palabras. |
| m10 | Aceptado con matiz | La tabla E4 ya no está en el PDF (recorte 3); en el texto de E4 se indica que los cocientes a n ≤ 18 (búsqueda exhaustiva < 10 ms) están dominados por la resolución del cronómetro y no se citan. La columna sigue en `results/scaling.md` sin alterar. |
| m11 | Aceptado | Cor. 3.2: convenciones Sᶜ = ∅ (γ = +∞, término 0) y γ = 0 (frontera KKT, excluida). |
| m12 | Aceptado | Def. 2.2: "nonempty proper subset ∅ ≠ R ⊊ [n]" y f_Π ≥ 1. |
| m13 | Aceptado | `\status{classical}` en el Lema 2.4; fila de la tabla de afirmaciones "classical / literature". |
| m14 | Aceptado | "20 of the (up to 50) collected minimal witnesses" en E2 y E5 (la leyenda de la antigua Tabla 3 también se corrigió antes de trasladarla a `results/fragility.md`). |
| m15 | Aceptado | Obs. 3.3: r es el residuo del ajuste Lasso en D (difiere del de mínimos cuadrados sobre X_S en μ X_S A⁻¹ s), e_i el residuo leave-one-out del ajuste con soporte fijo; la identificación con DFBETA se dice "under the constant rule" (en Obs. 3.3, resumen y ficha). |
| m16 | Aceptado | 0 `Overfull` y 0 avisos de fuente en la compilación final: Tabla 1 en `footnotesize` con encabezado más corto; display de la prueba de la Prop. 3.4 partido en dos líneas (`gather*`); `\textsc` sustituido por `\tsc` (= `\textnormal{\textsc{…}}`, versalitas rectas también dentro de teoremas en cursiva) y `\status` con `\textnormal`. |
| m17 | Aceptado | Obs. 5.2(i): "strong NP-hardness (hardness for numbers polynomially bounded in n) is excluded for p = 1 by this pseudo-polynomial algorithm unless P = NP". |

## Verificación matemática del árbitro
Sin objeciones; agradezco la verificación paso a paso de la Prop. 3.1, la Prop. 3.4, los Ej. 4.2–4.3 y el Teo. 5.1. La única corrección matemática necesaria era la de B1.

## Bibliografía
Aplicadas las correcciones verificadas (kuschnig2021, woodbury1950, broderick2020 v4). Las 16 entradas "no verificables en red" quedan marcadas como tales en la nota de continuidad; no se borró ninguna porque todas se citan con razón. La continuación de Freund–Hopkins (arXiv 2410.07916) no se cita: no pude comprobar sus autores.

## Lista de acciones del árbitro (13)

| # | Acción | Estado |
|---|---|---|
| 1 | Cor. 3.2 con h_i < 1 e ι_i = ∞ si h_i = 1 (B1) | hecho (+ script de comprobación, + guarda KKT en el solver) |
| 2 | Salvedad de unicidad tras la Prop. 3.1 y en Limitations (M1) | hecho |
| 3 | Cuatro scripts en una sesión; regenerar `results/`, `numbers.tex`, tablas, figuras, PDF (M3b, M4) | hecho (84 s de CPU) |
| 4 | Párrafo "Pre-specification and changes" (M3a) | hecho |
| 5 | Textos de M2 en `main.tex:62`, ficha; "at n ≤ 14" en el resumen | hecho |
| 6 | Errores típicos y nota de tiempos en E3 (M5) | hecho (texto, columna ± s.e., cociente ajustado) |
| 7 | Eliminar Tabla 8 o quitarle `[H]` (M6) | hecho con matiz: tabla conservada, compacta, sin `[H]`, 0 overfull |
| 8 | Obs. 3.5 sin atribuir la regla P (M7) | hecho; fórmula del artículo no cotejada con el PDF (pendiente) |
| 9 | kuschnig2021 corregido y movido; Woodbury 1950 (m4, m5) | hecho |
| 10 | "unsigned f_ANY"; coste Prop. 3.4; g/n y "with finite f"; "30 fresh instances"; "nonempty R" | hecho |
| 11 | Numeración unificada en README, CONTINUIDAD, docstrings (m1) | hecho |
| 12 | Recortes 1–8 a ≤ 10 páginas; resumen ≤ 200 palabras (m9) | hecho: 15 → 10 páginas (ver nota de extensión) |
| 13 | "--%", columna de cocientes n ≤ 18, cajas desbordadas, `\textsc` en cursiva (m6, m10, m16) | hecho |

### Nota de extensión (recortes)
Aplicados: resumen a ≈ 190 palabras (1); lista numerada de la introducción sustituida por un párrafo con referencias a secciones (2); las cinco tablas por celda (E1b, E2, E4, E4b, E5) salen del PDF y quedan en `results/validation.md`, `results/fragility.md`, `results/scaling.md`, con frases de remisión en el texto (3; el árbitro ofrecía esta alternativa); Figuras 1 y 2 fusionadas en una figura de cuatro paneles (`fig_combined.pdf`) (4); Apéndice A reducido a "Solver" y "Exact test and search" (7); E2/E3 sin repetir en el texto los números de las tablas conservadas (8). Con matiz: la tabla de afirmaciones se conserva compacta (5); la Obs. 3.3 no se fusionó en el Cor. 3.2 para no desplazar la numeración que el informe utiliza, pero se acortó junto con la Obs. 5.2(iii) (6). Esos recortes de contenido llevaron de 15 a 12 páginas; las dos últimas se ganaron con el cuerpo a 10pt y márgenes de 0.9in (`geometry`), cambios de formato que declaro como tales. Nada demostrado se eliminó; la única pérdida es que los lectores del PDF deben ir a `results/*.md` para las cifras por celda.

## Números que cambiaron (v0.1 → v0.2)
Solo cantidades dependientes del tiempo de ejecución (misma máquina compartida, otra carga), ninguna de las cuales altera un veredicto:
- Rendimiento E1-D: 1.4 → 1.1 μs por subconjunto; 569 → 442 μs por reajuste; ×395 → ×399.
- Cocientes de coste medianos del greedy de un paso (E3; A/B): ANY 1.44/0.77 → 1.34/0.73; LEAVE 0.52/0.59 → 0.48/0.58; ENTER 0.78/0.51 → 0.76/0.52. Mínimo sobre las 18 combinaciones: 0.46 (nuevo macro), ajustado 0.26 (nuevo).
- E4: coste del greedy a n = 34: 0.067 → 0.070; mediana sobre A con n ≥ 22 y f finita: 0.690 → 0.774 (y 0.68 sobre las 120, nuevo).
- Tiempos de los scripts: 13/58/60 s → 8/40/35 s (total de Python 127 → 84 s; el resumen de reproducibilidad lo refleja).
- Nuevos: errores típicos de E3 (0.4–3.1 puntos; déficit ENTER 1.7/1.1 e.t.), `\ExOneChecks` = 12/12.
Sin cambio: 2760/2760, 7200/7200, 1216/2114 (58 %), 52 %/92 %, máximos 4/3, media 1.73, tipos 51/43/6 y 54/25/20, k* ≥ 1 en 30 % (brecha 1.2), 0/18, 97/100, 95/98, 86/88, k_pred 70/99, E4 1.43 → 4.00 (1 n.f.), 75 %, 10, g/n 0.028, k* = 5, 0.57, 89 %, E5 7.1/10.5 %, 6960/8092, 51/72 %, 14.9/9.3 %. La réplica instancia a instancia del árbitro (120 instancias de E4, 0 discrepancias) es coherente con esto.

## Estado de compilación
`manuscript/build.sh` (make_numbers + latexmk): 0 errores, 0 referencias/citas indefinidas, `pdftotext main.pdf - | grep -c "??"` = 0, 0 `Overfull`, 0 avisos de fuente. Páginas: 15 (v0.1) → 10 (v0.2). Las páginas con la Tabla 1, la Tabla E3, la figura combinada y la tabla de afirmaciones se renderizaron y revisaron.

## Lo que queda abierto
1. Cotejar con el PDF de Meinshausen–Bühlmann (2010) la forma del Lasso (suma con λ fijo, según memoria) para cerrar M7 del todo.
2. Las 16 entradas bibliográficas clásicas siguen sin verificación en red (marcadas en CONTINUIDAD).
3. Decidir si la tabla de afirmaciones se mantiene en una versión para envío (M6, recorte 5).
4. Los cocientes de coste dependen de la implementación y de la carga de la máquina (cambiaron hasta un 12 % entre v0.1 y v0.2 sin alterar veredictos); una versión para envío debería repetir E3 varias veces o reportar intervalos.
5. La guarda KKT del solver se añadió a posteriori; convendría un test unitario con más instancias con empates (datos enteros) antes de confiar en el solver fuera de diseños continuos.
6. Pendientes de investigación ya listados en "Next steps" (Conj. 5.3, dureza fuerte para p ≥ 2, apretar la Prop. 3.4, μ por validación cruzada, elastic net).

## Tiempo de cómputo de esta ronda
Corrida de referencia v0.2: 84 s de CPU (1.6 + 8.1 + 40.3 + 34.6 s; 89 s de pared). Pruebas rápidas, comprobación de B1 y una decena de compilaciones con latexmk: ≈ 1 min más. Total ≈ 2.5 min de CPU, muy por debajo del presupuesto de 10 min.
