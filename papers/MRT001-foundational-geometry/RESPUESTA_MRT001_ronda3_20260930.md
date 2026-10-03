# Respuesta del autor al informe de arbitraje interno — MRT001, ronda 3

Manuscrito revisado: v0.4 (la portada decía v0.3) → **v0.5** (portada "Working draft v0.5 — 3 October 2026", fecha fija). Fecha de la respuesta: 03/10/2026 (nombre de archivo con la fecha de la carpeta, 30/09/2026). Informe atendido: `REFEREE_MRT001_ronda3_20260930.md` (veredicto "cambios menores": 0 bloqueantes, 4 mayores, 9 menores, 13 acciones).

Agradezco la verificación línea a línea de las seis proposiciones, la comprobación de que las rondas 1 y 2 estaban aplicadas de verdad, el cotejo de las 37 referencias y, en particular, la comprobación numérica del caso de punto compartido de la Prop. 3.8 y la sugerencia de la ley 2^Poisson(1), que resultó defendible y se incorporó como conjetura con un experimento propio.

## Recuento

- Mayores: 4 → **3 aceptados** (M1, M2, M3), **1 aceptado con matiz** (M4: aplicado en su totalidad, pero el cotejo con el PDF original sigue pendiente porque las fuentes primarias están bloqueadas desde el contenedor).
- Menores: 9 → **8 aceptados** (m1, m2, m3, m4, m5, m6, m7, m9), **1 aceptado con matiz** (m8: año 1989 tomado del informe, registro del MIT no consultable).
- Rebatidos: **0**. Las 13 acciones de la lista final están aplicadas, incluida la 13 (opcional).
- Números del texto que cambiaron: **ninguno de los previos**. Cambió solo la forma de un macro (`\EfiveDablation`: de "less than one percent" a "+0.4\%", misma ablación) y se añadieron los números del nuevo experimento E5f. No se relanzaron E1–E5.
- Compilación: 0 errores, 0 referencias/citas indefinidas (`grep -c "??"` = 0), 0 cajas desbordadas. Páginas: 18 (v0.4) → 20 (v0.5); el aumento son la prueba completa de la Prop. 5.2, el párrafo del caso compartido, el párrafo de la conjetura con la Tabla E5f, y una página de flotantes (Figura 3 + tabla de afirmaciones) que antes se repartía entre otras páginas.
- Cómputo de la ronda: ≈ 4 min de CPU (E5f 128 s; verificaciones del autor ≈ 1 min; `--replot`, `make_numbers.py` y cinco compilaciones ≈ 1.5 min). No se relanzaron E1–E5.

## Hallazgos mayores

### M1 — Prop. 5.2, enunciado: la fórmula de conteo falla para la cadena. **Aceptado.**
Tiene razón: el grafo de incomparabilidad vacío tiene exactamente una orientación transitiva y "la mitad" sería 1/2. Enunciado reescrito (main.tex, Prop. 5.2): *"The number of realizers modulo the swap is 1 for a chain and otherwise equals half the number of transitive orientations of the incomparability graph of the order (the unique realizer (≺,≺) of a chain is fixed by the swap, whereas for any other order the reversal of an orientation is a different orientation); it is n!/2 for an antichain, and 1 whenever the incomparability graph has a unique transitive orientation up to reversal …"*. El código (`lorentzian_chain.py`, `count_realizers_mod_swap`, k = 0 → 1) no necesitaba cambio.

### M2 — Prop. 5.2, prueba: no se demostraba que T = <_u ∩ inc(≺) es una orientación transitiva. **Aceptado.**
Prueba completada en los dos sentidos, siguiendo la línea del informe:
1. T orienta toda arista del grafo de incomparabilidad y es transitiva: si a ∥ b, b ∥ c y a <_u b <_u c, entonces v_a > v_b > v_c, luego a ∥ c y (a,c) ∈ T.
2. Recíprocamente, para toda orientación transitiva T, ≺ ∪ T es un orden lineal: total y antisimétrico por construcción; transitivo porque en el caso mixto a ≺ b, (b,c) ∈ T las alternativas a (a,c) ∈ ≺ ∪ T son c ≺ a (daría c ≺ b, contra b ∥ c) y (c,a) ∈ T (daría (b,a) ∈ T por transitividad de T, contra a ≺ b); el caso espejo (a,b) ∈ T, b ≺ c es análogo. Con <_u = ≺ ∪ T y <_v = ≺ ∪ T⁻¹ se obtiene un realizador (<_u ∩ <_v = ≺ porque T es antisimétrica).
3. Así los realizadores corresponden biyectivamente a las orientaciones transitivas y la reversión de T es el swap; la cláusula "for which ≺ ∪ T is transitive" se **eliminó** por automática. El párrafo antiguo entre paréntesis (que probaba compatibilidad con ≺, no transitividad de T) se sustituyó.
Dónde: main.tex, prueba de la Prop. 5.2 (p. 11–12).

### M3 — Golumbic usado sin cita. **Aceptado.**
Añadidas `golumbic1977` (J. Combin. Theory Ser. B 22(1), 68–90, 1977) y, como complemento, `golumbic1980` (*Algorithmic Graph Theory and Perfect Graphs*, Academic Press, 1980). Citadas en E5e ("Golumbic's Γ-relation [9, 10]") y en el apéndice E5 ("implication classes [9]"). Aprovecho para decir en E5e por qué la enumeración 2^k es exhaustiva (toda orientación transitiva contiene cada clase de implicación o su reversa), y la fórmula producto de Golumbic se usa también en el nuevo párrafo de m4.

### M4 — Teorema 3.7, enunciado informal más débil que el original. **Aceptado con matiz.**
Aplicado todo lo pedido:
- (a) "bounded, connected and open **and satisfy the mild regularity condition imposed in [K–vL] (for instance, Ω a finite union of open balls)**";
- (b) "the **complete** ordinal pattern …, that is, the outcome of **all** comparisons D_ab < D_cd over quadruples of labels" y "y^{(n)} ∈ (R^d)^n, **in the same dimension d**";
- (c) identificación con la Def. 2.6: C_n = {(x_1,…,x_n)}, segmentos iniciales de **una sucesión densa fija**, δ = disparidad de Procrustes, y el teorema "read with the alignment **uniform over the labels i ≤ n**, which is what a vanishing disparity requires";
- Terada–von Luxburg: "a conclusion of the same kind … for points drawn from a density on a suitable domain and k → ∞ with k/n → 0, **at a rate specified there**";
- se mantiene la etiqueta "informal statement", se añade "We state the theorem informally and refer to the source for the exact regularity condition and for the mode of convergence", y la tabla de afirmaciones pasa de "literature" a "literature (informal statement)".

Matiz: no cito número de teorema porque no lo conozco con certeza. Intenté leer el PDF (tml.cs.uni-tuebingen.de, proceedings.mlr.press, dl.acm.org) y el proxy los bloquea, como le ocurrió al árbitro; el cotejo se hizo con los resúmenes secundarios que devuelve la búsqueda web (ficha del artículo y reformulación de Arias-Castro), que coinciden punto por punto con las hipótesis añadidas (U acotado, conexo, abierto con condiciones adicionales, p. ej. unión finita de bolas; C = [n]⁴; misma dimensión; recuperación salvo semejanza en el límite denso). El cotejo con el original (número de teorema, condición exacta, uniformidad en i) queda registrado como pendiente nº 1 en la nota de continuidad.

## Hallazgos menores

### m1 — Prop. 3.8, paréntesis del caso compartido. **Aceptado.**
La frase "generally lies strictly inside the interval" era falsa: en el caso colineal con a en medio el desplazamiento de cierre es exactamente g/4. Lo comprobé por mi cuenta (`scratchpad/author_MRT001/shared_point.py`: bisección en e con maximización interna del cierre por Nelder–Mead): e/g = 0.25000 (180°), 0.25433 (150°), 0.26795 (120°), 0.29289 (90°), 0.33333 (60°), idéntico a 1/(2(1+sin(θ/2))) a cinco cifras. Texto nuevo en la prueba: la dirección óptima de x_a es e_ac − e_ab, que cambia D_ab − D_ac a primer orden en ‖e_ab − e_ac‖ = 2 sin(θ/2) por unidad de desplazamiento; cierre en g/(2(1+sin(θ/2))) + O(g²); igual a g/4 exactamente en el caso colineal (configuración admitida) y → g/2 cuando θ → 0; y la observación de que el radio inscrito es el mínimo de los desplazamientos de cierre sobre los pares consecutivos (una configuración fuera de la clase se alcanza a lo largo del segmento desde X solo después de un empate entre distancias consecutivas en X), con lo que la pertenencia a [g/4, g/2] queda argumentada dentro de la prueba.

### m2 — "a disparity of at most 3g²/8". **Aceptado.**
Ahora: "a disparity **of order** 3g²/8 (the squared displacement n(g/4)² divided by the expected squared centred norm n/6 of a uniform sample of the unit square; an order-of-magnitude estimate, not a bound valid for every X)". El macro `\EtwocBoundNsixtyfour` se renombró `\EtwocDispEstNsixtyfour` (mismo valor, 1.4×10⁻¹⁴).

### m3 — "(Schoenberg)" sin referencia precisa. **Aceptado.**
Añadida `schoenberg1937` (Ann. of Math. 38(4), 787–793) y citada en la frase sobre D^p con p < 1; `schoenberg1935` sigue para el criterio de la matriz doblemente centrada.

### m4 — "The extra realizers come from …" y conjetura 2^Poisson(1). **Aceptado, conjetura incluida.**
- "typically come from". El mecanismo se formula con cuidado: un par adyacente en ambos órdenes con direcciones opuestas es un par de gemelos incomparables y por tanto un **módulo** del grafo de incomparabilidad; cuando esos pares son los únicos módulos no triviales y el cociente es primo (lo típico para n grande), la fórmula producto de Golumbic da 2·2^N orientaciones transitivas, es decir 2^N realizadores módulo el swap. Evité escribir "ambas orientaciones del par son transitivas" porque no es cierto en general: si un tercer punto es incomparable a ambos, {a,b} puede no ser módulo fuerte y el factor es 3!, no 2·2 (eso es exactamente lo que producen las excepciones observadas).
- N = número de sucesiones descendentes de la permutación rango-u → rango-v; media (n−1)/n; asintóticamente Poisson(1) (cita `kaplansky1945`, Ann. Math. Statist. 16(2), 200–203; datos bibliográficos verificados por búsqueda, enunciado cotejado solo en fuentes secundarias, que atribuyen a Wolfowitz y Kaplansky la ley de Poisson de media 1 para sucesiones en una dirección y media 2 en cualquier orden).
- Verificación propia antes de incluir la conjetura: nuevo script `experiments/realizer_law.py` (E5f, semilla 20260933, 128 s, resultados en `results/results_realizer_law.json` y `results/tables_realizer_law.md`): el conteo exacto de E5e coincide con 2^N en 151/200, 179/200, 192/200, 98/100, 98/100 y 49/50 muestras para n = 20, 50, 100, 200, 300, 500 (767/850 en total; 437/450 con n ≥ 100); las excepciones difieren de 2^N por factores 3/2, 2 o 3 (módulos mayores, p. ej. rachas de tres puntos mutuamente incomparables). Con eso la conjetura me parece defendible.
- Texto: **Conjetura 5.3** ("stated, not proved"): realizadores = 2^N con probabilidad → 1, ley límite 2^Poisson(1), fracciones límite e⁻¹, e⁻¹, (8/3)e⁻¹; predicciones 0.368/0.368/0.981 frente a 0.34/0.37/0.98 observadas en n = 300 (Tabla E5e); nueva Tabla E5f; párrafo E5f en el apéndice; fila "conjectural" en la tabla de afirmaciones; README y ficha mencionan la conjetura como tal. Ningún número está tipeado: los macros `\Rlaw*` (incluidos e⁻¹ y (8/3)e⁻¹) los genera `make_numbers.py`.

### m5 — Versionado, README, tiempos y recuentos. **Aceptado.**
Portada "Working draft v0.5 — research line MRT001 — 3 October 2026" (fecha fija, sin `\today`). README: estado v0.5, tres rondas, tiempos reales (E1–E4 ≈ 20 min / 1201 s; E2c ≈ 3 min / 168 s; E5 ≈ 5 min / 315 s; E5f ≈ 2 min / 128 s), cuatro scripts y semillas. Nota de continuidad: "92/92" → "91/91" (con mención del error de transcripción) y "E5 en 149 s" → "315 s". Ficha propuesta: v0.5, tres rondas.

### m6 — Restos de "walk radius". **Aceptado.**
`ordinal_class.py`: docstring (ahora "walk range … lower bound on the extent of the class … not a radius"), mensajes, leyenda de la figura, cabecera de `tables_class.md` y claves del JSON (`walk_range_median/q1/q3`, `slope_walk_range`, `raw.ranges`); `make_numbers.py` adaptado. Para no relanzar los 168 s por un cambio de nombre, añadí el modo `--replot`, que regenera figura y tablas desde el JSON existente y migra las claves antiguas dejando constancia en `meta.keys_renamed` (valores intactos). Figura regenerada: leyenda "walk range (slope −7.9)".

### m7 — `\EfiveDablation` imprimía "less than one percent". **Aceptado.**
Imprime siempre el porcentaje con signo y un decimal ("+0.4\%"), y el texto añade los dos valores: "changes the median error at n = 2000 by +0.4 %, from 0.0312 to 0.0313" (macros `\EfiveDrmseLastFour`, `\EfiveDrmseAblLastFour`).

### m8 — `meyer1988`. **Aceptado con matiz.**
Entrada con `year = {1989}` y `note = {MIT handle 1721.1/14328; often cited as 1988}`; clave renombrada `meyer1989` y cita actualizada. Matiz: no pude ver el registro del MIT (dspace bloqueado); el año se toma del informe, que sí lo consultó, y queda anotado como pendiente de confirmación.

### m9 — Inyectividad en Prop. 3.8(ii). **Aceptado.**
En el enunciado: "there is an **injective** configuration Y … (the moved points stay distinct because g(X) ≤ min_{a≠b} D_ab)"; la justificación sigue al final de la prueba.

### Acción 13 (opcional). **Aplicada.**
`sorkin2005` con `doi = {10.1007/0-387-24992-3_7}`; `myrheim1978` con `number = {CERN-TH-2538}` y URL del registro CDS 293594.

## Otros puntos del informe

- Los dos puntos "parciales" de la verificación de rondas 1 y 2 (leyenda "walk radius"; portada v0.3 y "less than one percent") quedan cerrados (m6, m5, m7).
- Macros frente a JSON: no se tocó ningún valor existente; se añadieron `\EfiveEtwoNmax`, `\EfiveEmaxCountNten`, `\EfiveDrmseLastFour`, `\EfiveDrmseAblLastFour` y los `\Rlaw*`. `python3 experiments/make_numbers.py` regenera todo.
- Maquetación: al crecer la Sección 5, la tabla de afirmaciones caía tras las referencias; se corrigió el orden de las tablas E5e/E5f en el fuente y la Figura 3 y la tabla de afirmaciones se colocan ahora en una página de flotantes (p. 16) inmediatamente después del texto de la Sección 6. Se revisaron las páginas renderizadas (Teorema 3.7, Prop. 3.8, E2c, Prop. 5.2, E5e–E5f, página de flotantes, apéndice, referencias).

## Lo que queda abierto (también en la nota de continuidad)

1. Cotejo del Teorema 3.7 y de la frase sobre Terada–von Luxburg con los PDF originales (número de teorema, condición exacta de regularidad, modo de convergencia, condición exacta sobre k).
2. Confirmación del año de la tesis de Meyer en el registro del MIT y del parámetro de Poisson en Kaplansky 1945.
3. Demostración de la Conjetura 5.3.
