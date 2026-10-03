# Informe de árbitro independiente — TCD001, ronda 3 (verificación de los teoremas nuevos de v0.4) — 03/10/2026

Árbitro: independiente y nuevo (no participó en las rondas 1–2).
Objeto: `manuscript/main.tex` v0.4 (commit `2a18de3`): Lema 5.3, Teorema 5.4, Proposición 5.5, Corolario 5.6, Observación 5.7, Conjetura 5.8, Apéndice B; respuesta a la ronda 2 (`RESPUESTA_TCD001_ronda2_20261003.md`).
Trabajo auxiliar (scripts propios y salidas): `/tmp/claude-0/-home-user-ChanoSilva/6d28bda3-759e-5faa-92d7-8739680d15c2/scratchpad/referee3_TCD001/`.

## Veredicto

**Cambios menores.** Las cinco piezas nuevas son correctas: revisé cada paso a mano y una verificación exhaustiva independiente en aritmética racional (1 192 pares instancia × regla, 49 040 submuestras, con un test de unicidad necesario y suficiente) no encuentra ningún fallo. Quedan dos problemas de alcance en cómo se resumen los resultados (M1: "dureza débil" sin la restricción "datos enteros" de la que depende; M2: la complejidad del objetivo ANY con signo, el que usan los experimentos, no está tratada, y para p = 1 es polinomial) y varios menores, entre ellos que el PDF tiene 12 páginas.

---

## 1. Verificación de los teoremas nuevos (prioridad 0)

### 1.1 Lectura paso a paso

| Pieza (main.tex) | Qué comprobé | Resultado |
|---|---|---|
| Lema 5.3 (`:252–254`, prueba `:375–377`) | Problema restringido a β₂ = 0 estrictamente convexo si G₁₁ > 0; β₁* es el umbral blando; KKT en (β₁*, 0) ⇔ \|γ\| ≤ μ′; (a) usa la suficiencia de KKT y la Def. 2.2 (sin unicidad no hay testigo); (b) usa que un minimizador con β₂ = 0 minimiza el problema restringido. En la reducción siempre G₁₁ > 0 (o el gadget está en K, o N ≥ 1). | Correcto. |
| Teo. 5.4, pertenencia a NP (`:380`) | (i) Un minimizador único tiene X_{K,S} de rango completo (Lema 2.4), así que aparece entre los 3^p sistemas KKT con signo; (ii) M = {β : G(β − β̂) = 0, ‖β‖₁ ≤ ‖β̂‖₁} es exactamente el conjunto de minimizadores (ajuste y norma ℓ₁ comunes; recíprocamente, igual ajuste y norma no mayor da objetivo no mayor); (iii) si M contiene un segmento, un trozo inicial del segmento desde β̂ cae en un ortante cerrado, de modo que M ∩ ortante es un politopo de dimensión ≥ 1 con un vértice distinto de β̂; (iv) cada intersección tiene a lo sumo 2p + 1 restricciones en dimensión p: enumeración de vértices polinomial para p fijo, tamaño de bits polinomial por Cramer. | Correcto. Falta la media frase de (iii) (ver m5). La restricción "p fijo" no es necesaria (la unicidad se decide por programación lineal), pero es inocua. |
| Construcción (`:259`, `:382`) | n = m + 1; η = 1/(2B), ε = η/(4μ) = 1/(8Bμ), ρ = 1 − ε coincide con ρ = 1 − 1/(8Bμ) del cuerpo; κ − ρ = η + ε ∈ (0, 1/B] porque ε ≤ 1/(12B); ρ > 1/2; u² = (m+1)² > m; μ′ ≥ 3/2 (regla C: t + ½; regla P: λ\|K\| ≥ λ). | Correcto. |
| Caso g ∉ K (`:384`) | G₁₁ = N, G₁₂ = ρN, q₂ = ρq₁; \|γ\| = ρ·min(\|W\|, μ′) < μ′ (W > 0 en ambas reglas). | Correcto. |
| Caso g ∈ K: cancelación de la regla P (`:386`) | μ′ = λ(N+1), W = σ + λN, q₁ = ½ + W ⇒ Δ = q₁ − μ′ = σ + ½ − λ = σ − t. Regla C: Δ = ½ + σ − t − ½. | Correcto; Δ ∈ ℤ en ambas reglas. |
| Identidades (eq:entry-id, `:388–389`) | q₂ − μ′ = ½(κ−ρ) + ρΔ − (1−ρ)μ′ (sustituyendo W = Δ + μ′ − ½) y G₁₂/G₁₁ − ρ = (κ−ρ)u²/(u²+N). También comprobadas con aserciones exactas en mis 49 040 submuestras. | Correcto. |
| (i) Δ ≤ −1 | β₁* = 0, γ = q₂ > 0 y q₂ − μ′ ≤ ½(κ−ρ) − ρ < 0 porque ½(κ−ρ) ≤ 1/(2B) < ½ < ρ. | Correcto. |
| (ii) Δ = 0 | q₂ − μ′ = ½(η+ε) − εμ′ ≥ ½(η+ε) − η/4 > 0; σ = t ≥ 1 ⇒ N ≥ 1 ⇒ rango 2 ⇒ unicidad ⇒ 2 ∈ S(D∖R) por el Lema 5.3(b). | Correcto. |
| (iii) Δ ≥ 1 ("absorción") | γ − μ′ = (κ−ρ)(½ − Δu²/(u²+N)) − (1−ρ)μ′ < 0 porque u² > N; γ + μ′ = ½(κ−ρ) + (1+ρ)μ′ − (κ−ρ)Δu²/(u²+N) > (1+ρ)μ′ − (κ−ρ)Δ ≥ 3/2 − (B−t)/B > 0. | Correcto. (Basta u² ≥ N: con u² = N el primer término es ≤ 0 y el segundo estrictamente negativo; u = m + 1 tiene holgura.) |
| Ventana de ancho < 1 (`:250`) | Como función de Δ real, la variable 2 entra exactamente en (Δ_lo, Δ_hi) con Δ_lo = ((1−ρ)μ′ − ½(κ−ρ))/ρ ∈ (−1, 0) y Δ_hi = (u²+N)/u² · (½ − (1−ρ)μ′/(κ−ρ)) ∈ (0, 1); como Δ ∈ ℤ, sólo Δ = 0. | Correcto (la palabra "integer data" de `:250` se refiere a que Δ es entero; ver m9). |
| Datos completos y testigos (`:395`) | K = [n] ⇒ Δ = B − t ≥ 1 ⇒ caso (iii): S(D) = {1}, β₁ > 0, único. Una subfamilia de suma t ∈ [1, B−1] es no vacía y distinta de [m], así que R = [m] ∖ I es no vacío y propio; el recíproco exige g ∉ R por el caso g ∉ K. Rama trivial t ≥ B: necesaria (con t = B la variable 2 ya está activa en D; lo detecté por error propio al incluir t = B en mi lista). | Correcto. |
| Unicidad en todo D∖R (`:397`) | g ∈ K y N ≥ 1: rango 2. K = {g}: filas ∝ (1, κ), minimizadores con β₁ + κβ₂ fijo, ℓ₁ mínima sólo en β₁ = 0 porque κ > 1. g ∉ K: filas ∝ (1, ρ), mínima sólo en β₂ = 0 porque 0 < ρ < 1. | Correcto. |
| Reescalado a enteros (`:397`) | (αX, α′y, αα′μ) con β = (α′/α)β′ multiplica el objetivo por α′² en ambas reglas (μ_k escala igual). Denominadores de X: 4B(2t+1) (C) o 4B(2t+1)(m+1) (P); de y: 2u. Las entradas enteras quedan acotadas por un polinomio en (m, B, t) (medido: M ≤ 1.25·B²(2t+1)(m+1)³), es decir, tamaño de bits polinomial. | Correcto. |
| p ≥ 3 (`:397`) | Columnas nulas: todo minimizador las anula (mismo ajuste, mayor ℓ₁) y la unicidad se reduce a las dos primeras columnas. | Correcto. |
| Prop. 5.5 (`:261–262`, prueba `:401`) | El objetivo en D∖R es ½yᵀ_Ky_K − q_Kᵀβ + ½βᵀG_Kβ + μ′‖β‖₁: minimizadores, unicidad (M depende de G_K) y objetivo dependen sólo de (\|K\|, G_K, q_K). Entradas enteras en [−nM², nM²]; p(p+1)/2 + p = p(p+3)/2 coordenadas ⇒ ≤ (n+1)(2nM²+1)^{p(p+3)/2} estados; n filas × O(p²) por estado ⇒ O(n²(2nM²+1)^{p(p+3)/2}) sumas de O(log(nM)) bits; f = n − max\|K\| con 1 ≤ \|K\| ≤ n − 1. | Correcto. |
| Cor. 5.6 (`:266–271`) | Dureza por los Teo. 5.1(a) (datos enteros, μ = ½) y 5.4 (reescalado); algoritmo polinomial en n, M y bits de μ ⇒ no fuertemente NP-duro salvo P = NP (Garey–Johnson, §4.2: un problema fuertemente NP-completo no admite algoritmo pseudo-polinomial salvo P = NP). Restringido correctamente a datos enteros. | Correcto. El resumen, la tabla de afirmaciones, README y FICHA pierden la restricción (M1). |
| Conj. 5.8 (`:277–280`) | Etiquetada [conjectural]; afirma sólo NP-dureza (no pertenencia a NP con p en la entrada). | Estado correcto. |
| Obs. 5.7 y Apéndice A (`:273–275`, `:369`) | Cifras contra `results/hardness.json` y el log congelado: 156 fuentes (78/78), 312/312, 137 328 submuestras, 33 172 ajustes, 312/312 DP, 145/145 aleatorios, 38 s. Reproducido (§5). | Correcto; ver m2 (SHA) y m3 (contador KKT). |

Etiquetas de estado: Lema 5.3, Teo. 5.4, Prop. 5.5 y Cor. 5.6 llevan [proved here], la Obs. 5.7 [computationally verified (exact arithmetic)] y la Conj. 5.8 [conjectural]; la fila correspondiente de la tabla de afirmaciones (`:349`) dice "proved here; verified (exact arithmetic)" y la Conj. 5.8 tiene su fila "conjectural" (`:350`). Las etiquetas son correctas; lo que falla es el alcance de las frases-resumen (M1, M2).

### 1.2 Verificación exhaustiva independiente (código propio, sin importar `lasso_fragility.py` ni `check_hardness.py`)

- `indep_lasso.py`: Lasso exacto en `fractions` por enumeración de los 3^p soportes con signo y KKT en función de (G, q). La unicidad se decide con un criterio **necesario y suficiente** distinto del del autor (él usa rango completo de X_E, que es sólo suficiente): el minimizador es único sii la derivada direccional de ‖·‖₁ en β̂ es > 0 en toda dirección no nula de null(G); se decide exactamente probando un conjunto finito de rayos (dim null ≤ 2, columnas nulas eliminadas antes). Validado contra casos conocidos (X = I₂, y = (3,3), μ = 1; filas (1,1) con solución no única) y contra `sklearn.linear_model.Lasso` en 298 instancias aleatorias con p = 3 (0 discrepancias > 10⁻⁶).
- `check_reduction.py` (17.7 s): **todas** las instancias con m ≤ 4, b_i ∈ {1,…,4} (multiconjuntos) y todo t ∈ [1, B−1], más bordes: m = 1 (b₁ = 2…6, siempre NO), b_i repetidos ([1]^m, [3]^m con m ≤ 7), t = 1 y t = B − 1, [5,5,5,7], potencias de 2, [100,1], [100,100,1], y 40 instancias aleatorias con m = 5…8. Ambas reglas: **1 192 pares (742 SÍ), 49 040 submuestras; equivalencia testigo ⇔ SÍ en 1 192/1 192; caracterización conjunto a conjunto ("g ∉ R y suma conservada = t") 0 fallos; submuestras no únicas 0; empates KKT 0; S(D) = {1}, β₁ > 0, único en 1 192/1 192; f_ENTER = m − max\|I\| (I de suma t) en 1 192/1 192.** Márgenes mínimos: \|γ\| − μ′ ≥ 1.2·10⁻³ en los testigos y μ′ − \|γ\| ≥ 1.6·10⁻⁴ fuera (del orden de 1/(8Bn): inocuo en aritmética exacta, pero conviene saberlo si alguien usa la construcción en coma flotante).
- `check_scaling_pad.py` (12.3 s): relleno con 1 y 2 columnas nulas (p = 3, 4): conjuntos de testigos idénticos y unicidad en todo, 120/120; datos reescalados a enteros: idénticos, 132/132. Controles negativos propios: u = 1 rompe la caracterización en 21 y la equivalencia en 8 de 132 instancias; κ = 2 en 10 y 4; ρ = 1 deja submuestras con minimizador **realmente** no único (criterio NyS) en 132/132.
- `check_dp.py` (42.0 s): programa dinámico propio sobre (\|K\|, G_K, q_K) contra búsqueda exhaustiva, 400 instancias enteras aleatorias (p ∈ {2,3}, \|x\|,\|y\| ≤ M ∈ {1,2}, n ≤ 8, ambas reglas, objetivos ANY con y sin signo, LEAVE(j), ENTER(j)): **1 795/1 795** pares (instancia, objetivo) coinciden; en instancias de la reducción, 12/12. Estados alcanzados / cota de la Prop. 5.5 ≤ 5.4·10⁻⁵ (la cota es holgada, como debe).
- `check_signed_any_p1.py`: ver M2 (2 243/2 243).

---

## 2. Verificación de la ronda anterior

| Id (ronda 2) | Estado | Evidencia |
|---|---|---|
| M1 guarda KKT | aplicado bien | Limitations `main.tex:360` y Apéndice A `:370` con macros; `results/*.json` `meta.kkt_guard`: E0 950 llamadas/91 retrocesos (91 empates, 91 rango completo), E1 0/16 191, E2–E5 0/117 708, E4 0/10 365 (suma 144 264 = `\EoneToFiveFits`). Código: segunda verificación con `RuntimeError` (`lasso_fragility.py:95`); aserciones en `make_numbers.py:127–134`. Pendiente menor: la verificación de dureza no registra su contador (m3). |
| M2 coste del greedy | aplicado bien | E4 `main.tex:317` con rangos; recalculé los rangos desde `cost_ratios_run_v02.json`, `cost_ratios_run_referee.json` y `scaling.json`: A n ≤ 18 4.31–10.7, n = 22–26 0.595–1.36, n = 30 0.576–0.678, n = 34 0.0550–0.0702, B 8.10–11.3, factor máximo 2.29 (A, 22): coinciden con `\EfourACostSmallLo`…`\EfourBCostHi` y `\EfourRunFactor` (dos cifras). Tabla de afirmaciones `:352` y FICHA corregidas; aserciones `make_numbers.py:445–449`. |
| M3 Obs. 3.5 (unicidad) | aplicado bien | `main.tex:188` (hipótesis de unicidad, "rule C (with μ = λ/2)"); tabla `:347`. |
| m1 introducción | aplicado bien (superado) | `:63` reescrita en v0.4 para el Teo. 5.4; coherente con la Obs. 5.2(ii). |
| m2 Teo. 5.1(a) "nonempty proper" | aplicado bien | `:236`, `:241`. |
| m3 Ej. 4.3 recuento | aplicado bien | `:208` "with \|R\| ≤ n−2 (including R = ∅)". |
| m4 10⁻¹⁴ tecleado | aplicado bien | `\KKTMaxActiveRel` = 3.6·10⁻¹⁴ = máx. de `max_active_rel` (E4, 3.56·10⁻¹⁴). |
| m5 medianas | aplicado bien | `\EfourAFourhundredMedian` = 10.5, `\EfourAHundredMedian` = 6.5, `\EfourATwohundredMedian` = 9.5, `\EfourBTwohundredMedian` = 1.5. |
| m6 ANY sin signo en E3 | aplicado bien | `:300`. |
| m7 S = ∅ en Cor. 3.2 | aplicado bien | `:154`. |
| m8 fila del Lema 2.4 | aplicado bien | `:342`. |
| m9 cociente ajustado | aplicado bien | `:288`, leyenda Tabla 2 `:312`. |
| m10 "100% ± 0.4" | aplicado bien | `table_e3.tex`: "99.6\% $\pm$ 0.4". |
| m11 segunda verificación KKT y docstring | aplicado bien | `lasso_fragility.py:95` y docstring de `kkt_residuals` (dos valores). |
| m12 CONTINUIDAD 0.067 | aplicado bien | `CONTINUIDAD:29`. Pero la línea `:43` quedó desfasada en v0.4 (m8 de esta ronda). |
| m13 IQR de cocientes | aplicado bien | `results/fragility.md:112` (columna "IQR cost ratio"). |

Recuento: 16 bien aplicados, 0 a medias, 0 no aplicados, 0 con error nuevo.

---

## 3. Hallazgos nuevos

### Bloqueantes

Ninguno.

### Mayores

**M1. "Dureza débil" se afirma sin la restricción a datos enteros de la que depende.**
Ubicación: resumen `main.tex:56` ("weak NP-completeness … of selection-witness existence for every fixed p ≥ 2, with a pseudo-polynomial algorithm for every fixed p"); introducción `:63` ("makes all this hardness weak"); tabla de afirmaciones `:349` ("so these problems are only weakly NP-complete for fixed p"); Limitations `:360` ("The hardness statements are weak for every fixed p"); README `:34` ("toda esta dureza es débil"); FICHA `:13`/`:24` ("un algoritmo pseudo-polinómico resuelve todos estos problemas" / "a pseudo-polynomial algorithm solves all these problems").
Problema: los Teoremas 5.1 y 5.4 están enunciados para datos **racionales**, y la Prop. 5.5 sólo da un algoritmo pseudo-polinomial para datos **enteros**. Llevar datos racionales a enteros exige un factor común α para todo X (un reescalado por columnas cambia el Lasso), y el mínimo común múltiplo de n·p denominadores pequeños pero distintos puede ser exponencial en n (p. ej. 1/p_i con primos distintos). Con numeradores y denominadores polinomiales, la versión racional podría ser fuertemente NP-dura incluso con p = 1. El Corolario 5.6 está bien restringido ("For integer data …"; CONTINUIDAD `:119` documenta que la restricción fue deliberada), pero la restricción no llegó a los resúmenes.
Corrección: en el resumen, "…for every fixed $p\ge2$, with a pseudo-polynomial algorithm for integer data and every fixed $p$"; en la introducción, "makes all this hardness weak for integer data"; en la tabla, "so for integer data these problems are only weakly NP-complete for fixed $p$"; en Limitations, "The hardness statements are weak for integer data and every fixed $p$ (Corollary~\ref{cor:weak}); for rational data with many distinct denominators the pseudo-polynomial algorithm does not apply"; README y FICHA análogos ("con datos enteros").

**M2. La "situación computacional" no trata el objetivo que usan los experimentos (ANY con signo), y la tabla de afirmaciones dice "fragility number NP-hard in general".**
Ubicación: tabla de afirmaciones `main.tex:348` ("fragility number NP-hard in general"); Obs. 5.2(ii) `:247`; Sección 5 en general; E2/E4 (`:296`, `:317`) calculan f^signed_ANY.
Problema: las reducciones cubren LEAVE, ENTER y ANY **sin** signo (Teo. 5.1(a) con columnas nulas). El número de fragilidad que el resumen, E2, E4 y la Figura 1 llaman "exact fragility number" es el ANY **con signo**, y su complejidad no se dice. Para p = 1 es fácil: si la variable está seleccionada con signo s, un testigo de tamaño k existe sii s·(T − σ_k^{(s)}) ≤ μ_k, donde σ_k^{(s)} es la suma de los k valores a_i con mayor s·a_i (el mínimo de s·Σ_{i∈K} a_i sobre \|R\| = k se alcanza quitando esos k), así que f^signed_ANY se calcula en O(n log n) igual que en el Teo. 5.1(b); si no está seleccionada, coincide con la selección del Teo. 5.1(b). Lo comprobé contra fuerza bruta exacta en 2 243/2 243 instancias aleatorias con p = 1 (`check_signed_any_p1.py`). Por tanto el relleno con columnas nulas no da dureza para el ANY con signo, y la construcción del Teo. 5.4 tampoco (en ella hay testigos ANY triviales, p. ej. R = [m], porque la variable 1 sale). La complejidad del objetivo principal de los experimentos queda abierta para p ≥ 2, y la introducción (`:63`: "only strong hardness with unbounded $p$ remains open") y CONTINUIDAD `:125` ("solo queda abierta la dureza fuerte con p no acotado") dicen lo contrario. La frase de la tabla es literalmente cierta para f_LEAVE, pero en el contexto del artículo induce a leer que el número calculado en E2/E4 es NP-duro.
Contexto que el texto debería usar: la diferencia es la de un umbral **unilateral** (cambio de signo: s·Σ ≤ μ) frente a una **ventana bilateral** (deselección: \|Σ\| ≤ μ, que es lo que codifica Subset Sum). Para el análogo de mínimos cuadrados (cambio de signo de un coeficiente), Moitra y Rohatgi (`moitra2022`, ya citado en la Obs. 5.2(iii)) dan, según su resumen, un algoritmo en tiempo n^{O(d³)} para decidir Stability(X, y) ≤ k (polinomial para d fijo, sin depender de las magnitudes) y, bajo la Exponential Time Hypothesis, ninguno en n^{o(d)}. Es plausible que el objetivo ANY con signo del Lasso, unión de eventos unilaterales salvo la salida de variables, se comporte como el problema de signo y no como la deselección; en todo caso es la comparación natural y hoy no aparece.
Corrección: (a) tabla `:348`: "…; $f_{\tsc{leave}}$ and the unsigned $f_{\tsc{any}}$ NP-hard; …"; (b) añadir a la Obs. 5.2 un punto (iv): "For the signed \tsc{any} target used in Section~\ref{sec:experiments} the reductions give nothing: for $p=1$ a variable selected with sign $s$ has a witness of size $k$ iff $s\,(T-\sigma^{(s)}_k)\le\mu_k$ with $\sigma^{(s)}_k$ the sum of the $k$ entries with largest $s\,a_i$, so $f^{\mathrm{signed}}_{\tsc{any}}$ is computable in $O(n\log n)$, as is the sign of a least-squares coefficient in fixed dimension~\citep{moitra2022}; its complexity for $p\ge2$ is open."; (c) introducción `:63`: "…and only strong hardness with unbounded $p$, and the complexity of the signed \tsc{any} target for $p\ge2$, remain open"; (d) añadirlo a "Next steps" (a) y a CONTINUIDAD `:51`.

### Menores

**m1.** Obs. 5.2(i) `main.tex:247`: "(with the cardinality as a second state under rule P)". Para **calcular** f_LEAVE (el mínimo \|R\|) hace falta la cardinalidad con ambas reglas; sólo la pregunta de existencia bajo la regla C se resuelve con las sumas parciales solas. Escribir: "(with the cardinality as a second state, which rule P needs also for the existence question)".

**m2.** El SHA-256 "congelado" no sirve como prueba de reproducción. `results/check_hardness_output.txt` incluye la línea `elapsed 37.7 s`; cualquier nueva corrida cambia el hash (mi corrida en una copia: `6eed294c9a4be6e7…` frente a `2049f31ebeec189b…`, con el log idéntico salvo esa línea), y el script reescribe a la vez el log, `check_hardness_output.sha256` y `hardness.json`, de modo que la aserción de `make_numbers.py:460` sólo detecta ediciones manuales del log. Corrección: calcular el hash sobre el log sin la línea de tiempo (o escribir el tiempo sólo en `hardness.json`) y decir en el Apéndice A: "frozen with SHA-256 prefix … of the log without its timing line, which a rerun reproduces".

**m3.** La verificación de dureza llama 33 484 veces a `lasso_lars` con guarda KKT (medido en mi repetición: 0 retrocesos, error activo máximo 1.6·10⁻¹⁴), pero no vuelca `meta.kkt_guard` en `hardness.json`, y el Apéndice A/Limitations sólo dan contadores de E0–E5. Corrección: volcar `lf.KKT_STATS` en `hardness.json` y añadir en Limitations "and in none of the 33\,484 fits of the hardness check" (por macro).

**m4.** Construcción `main.tex:259`: "a shift that makes $q_1-\mu'=\sigma-t$ … independent of $|K|$" sólo vale con el gadget conservado; sin él, q₁ − μ′ = σ en ambas reglas. Escribir "…makes $q_1-\mu'=\sigma-t$ whenever the gadget is kept…".

**m5.** Prueba de pertenencia a NP `main.tex:380`: "If $\mathcal M$ contains a segment, its intersection with some closed orthant has a vertex other than $\hat\beta$" omite el porqué. Añadir: "(an initial piece of the segment from $\hat\beta$ lies in one closed orthant, so that intersection is a polytope of dimension $\ge1$)". Opcionalmente, observar que para p en la entrada la unicidad se decide por programación lineal (no es necesario para la tesis).

**m6.** Teo. 5.4, `main.tex:382`: "If $t\le0$ or $t\ge B$ the answer is immediate". Con la convención t ≥ 1 del Teo. 5.1 el caso t ≤ 0 no aparece; y conviene decir por qué la rama es necesaria: con t = B el dato completo tiene Δ = 0 y la variable 2 ya es activa en D (lo comprobé), lo que violaría la hipótesis j ∉ S(D). Escribir: "If $t\ge B$ (then $\Delta=0$ on $D$ when $t=B$, so the construction would violate $j\notin S(D)$) the answer is immediate …".

**m7.** Teo. 5.4, enunciado `main.tex:257`: "decide whether some nonempty proper $R$ … is a witness" es una pregunta de decisión con promesa (minimizador único en D y j ∉ S(D)). La promesa se verifica en tiempo polinomial para p fijo con el mismo procedimiento de la prueba; decirlo en una frase evita la objeción de que el problema esté mal definido fuera de la promesa.

**m8.** `CONTINUIDAD_TCD001_20260930.md:43`: "La dureza es débil y solo para p = 1" contradice v0.4 (dureza para todo p fijo ≥ 2). Actualizar a "La dureza es débil (datos enteros, todo p fijo) y usa datos con estructura especial".

**m9.** `main.tex:250`: "With integer data the kink leaves a window of width less than one": los datos de la construcción no son enteros; lo entero es Δ = σ − t. Escribir: "Since the slack $\Delta=\sigma-t$ is an integer and the kink leaves a window of width less than one around $\Delta=0$, the inactive variable enters exactly when a subset sum hits a target".

**m10.** Extensión: el PDF tiene **12 páginas** (v0.3: 10; el cuerpo termina en la p. 11, Apéndices A–B y referencias en pp. 11–12; `README.md:12` y CONTINUIDAD lo dicen). El añadido de la Sección 5 y del Apéndice B está justificado por su contenido, pero hay redundancias que permiten volver a 11 sin perder nada verificable: (a) la Obs. 5.7 y el párrafo "Exhaustive check" del Apéndice A dicen casi lo mismo: dejar en el cuerpo una frase ("checked exhaustively in exact arithmetic, \HardEquivOk/\HardPairs{} pairs; Appendix~\ref{app:repro}") y los detalles en el apéndice (≈ 6 líneas); (b) mover el párrafo "Construction" (`:259`) al Apéndice B, dejando en el cuerpo la frase de la ventana (`:250`), que ya explica el mecanismo (≈ 5 líneas); (c) E4 (`:317`): pasar las cifras por tamaño (exactitud a n = 22…34, tiempos de B en ms) a `results/scaling.md` y dejar sólo los rangos y la conclusión (≈ 6 líneas); (d) unir en la tabla de afirmaciones las filas de los Teo. 5.1 y 5.4 (≈ 2 líneas).

**m11.** Cosmético: la compilación da 5 avisos de hyperref "Token not allowed in a PDF string", por las fórmulas de los títulos de las subsecciones E2 (`main.tex:295`, `$n\le14$`) y E4 (`:316`, `$n$`); usar `\texorpdfstring{$n\le14$}{n <= 14}` y análogo.

**m12.** Conjetura 5.8 y su comentario (`main.tex:277–280`), Obs. 5.2(iii) (`:247`): la literatura citada ya contiene resultados de complejidad que sitúan la conjetura y no se mencionan. Moitra y Rohatgi (`moitra2022`) prueban, para el cambio de signo de un coeficiente de mínimos cuadrados, un algoritmo n^{O(d³)} (polinomial para d fijo) y una cota inferior n^{o(d)} bajo ETH; es decir, para el problema de signo con d en la entrada ya hay dureza (condicional) con d creciente y no hay dureza alguna con d fijo, mientras que aquí la deselección es NP-completa ya con p = 1. Añadir a la Obs. 5.2(iii): "for the sign of a least-squares coefficient, \citet{moitra2022} give an $n^{O(d^3)}$ algorithm and an ETH lower bound $n^{\Omega(d)}$; the two-sided window $|c_j|\le\mu$ of a Lasso deselection is what makes the problem hard already for $p=1$", y decir junto a la conjetura si esa cota inferior se traslada o no al Lasso (no se traslada directamente: el objetivo es otro). Opcional: Hu et al., "Most Influential Subset Selection: Challenges, Promises, and Beyond" (NeurIPS 2024), sobre el fallo de las heurísticas aditivas de influencia, pertinente para E3, y Konrad y Kuschnig, "Testing Most Influential Sets" (ICLR 2026, arXiv:2510.20372), de los mismos autores que `konrad2026`.

---

## 4. Bibliografía

| Entrada | Estado | Corrección |
|---|---|---|
| `rubinstein2025` (Rubinstein, Hopkins, ICLR 2025, arXiv:2410.07916) | Verificada por búsqueda: autores, título, sede (mlanthology, actas ICLR 2025, NSF PAR); el resumen (certificados de robustez de OLS a la eliminación de muestras, algoritmos para dimensión ≥ 4) respalda el uso tras la Prop. 3.4. | Ninguna. |
| `konrad2026` (Konrad, Kuschnig, ICML 2026, arXiv:2606.05919) | Verificada por búsqueda: autores, título, sede; resumen: para estimandos con efectos de eliminación lineal-fraccionales el conjunto más influyente se reduce a una sucesión de problemas top-k (Dinkelbach). El uso en la introducción (`:61`) coincide. | Ninguna. |
| `moitra2022` | Verificada (arXiv:2205.14284, ICLR 2023). Su resumen contiene el algoritmo n^{O(d³)} y la cota bajo ETH que el texto no usa. | Ver M2 y m12. |
| `amaldi1995` | Verificada: TCS 147 (1995) 181–210. | Ninguna. |
| Resto de entradas clásicas (14) | Coinciden con lo que conozco (revistas, volúmenes y páginas de tibshirani1996, efron2004, osborne2000, tibshirani2013, zhao2006, wainwright2009, meinshausen2010, cook1977, hampel1974, karp1972, amaldi1998, sherman1950, hager1989, pedregosa2011); no las verifiqué una a una en red en esta ronda. | Mantener la marca "no verificadas en red" en CONTINUIDAD hasta hacerlo. |
| Faltantes posibles | Hu et al. (NeurIPS 2024); Konrad y Kuschnig (ICLR 2026). | Opcional (m12). |

arxiv.org y proceedings no se leyeron directamente; las verificaciones se apoyan en varios resultados de búsqueda concordantes (títulos de páginas de arXiv, mlanthology, actas, NSF PAR).

---

## 5. Verificación computacional

| Qué | Tiempo (CPU) | Resultado |
|---|---|---|
| `indep_lasso.py` (solver exacto propio) contra casos conocidos y contra `sklearn.linear_model.Lasso` (298 instancias, p = 3) | ~3 s | 0 discrepancias. |
| `check_reduction.py`: reducción del Teo. 5.4, ambas reglas, todas las instancias con m ≤ 4 y b_i ≤ 4 más bordes (m = 1, b_i repetidos, t = 1, t = B − 1, valores grandes, 40 aleatorias con m ≤ 8) | 17.7 s | 1 192/1 192 equivalencias; 0 fallos de caracterización en 49 040 submuestras; 0 no unicidades (criterio NyS); 0 empates; identidades (eq:entry-id) exactas en todas las submuestras con gadget. |
| `check_scaling_pad.py`: relleno p = 3, 4; reescalado a enteros; controles negativos | 12.3 s | 120/120; 132/132; los controles rompen la reducción como predice la prueba. |
| `check_dp.py`: DP propio de la Prop. 5.5 contra búsqueda exhaustiva | 42.0 s | 1 795/1 795 y 12/12. |
| `check_signed_any_p1.py`: ANY con signo para p = 1 por ordenación contra fuerza bruta exacta | 4.0 s | 2 243/2 243 (M2). |
| Repetición de `experiments/check_hardness.py` del autor en una copia (con `KKT_STATS` leído al final) | 39.7 s | Log idéntico al congelado salvo la línea `elapsed`; por eso el SHA-256 cambia (m2). Guarda KKT: 33 484 llamadas, 0 retrocesos (m3). |
| `make_numbers.py` sobre la copia con la salida repetida | <2 s | 545 macros; sólo cambian `\HardSeconds` (38 → 39) y `\HardSha`. |
| Rangos de coste de E4 recalculados desde los tres JSON | <1 s | Coinciden con todas las macros de rango y con el factor 2.3 (ronda 2, M2). |
| `latexmk` sobre una copia | 4 s | 0 errores, 0 referencias o citas indefinidas, 0 "??", 0 Overfull, 2 Underfull (tabla de afirmaciones, ya conocidos), 5 avisos de hyperref (m11); **12 páginas**. |

CPU total ≈ 2.5 min. La reproducción del autor coincidió (salvo el tiempo) y mi verificación independiente confirma todas las afirmaciones de la Sección 5 y del Apéndice B.

---

## 6. Lista final de acciones (por prioridad)

1. Añadir "for integer data" a toda afirmación de dureza débil o de algoritmo pseudo-polinomial: resumen, introducción, tabla de afirmaciones, Limitations, README y FICHA (M1).
2. Precisar en la tabla de afirmaciones que la dureza es de f_LEAVE y del ANY sin signo; añadir a la Obs. 5.2 el punto (iv) sobre el ANY con signo (O(n log n) para p = 1, abierto para p ≥ 2), corregir "only strong hardness … remains open" en la introducción y añadirlo a Next steps y CONTINUIDAD (M2).
3. Citar en la Obs. 5.2(iii) y junto a la Conjetura 5.8 el algoritmo n^{O(d³)} y la cota bajo ETH de Moitra–Rohatgi para el problema de signo (m12).
4. Calcular el SHA-256 del log de dureza sin la línea de tiempo, para que una nueva corrida lo reproduzca (m2), y volcar el contador de la guarda KKT de la verificación de dureza en `hardness.json` y en Limitations (m3).
5. Corregir las frases de la construcción y de la ventana: "whenever the gadget is kept" (m4); "Since the slack Δ = σ − t is an integer…" (m9).
6. Completar la prueba de pertenencia a NP con el argumento del trozo inicial del segmento (m5), justificar la rama t ≥ B (m6) y declarar la promesa del problema (m7).
7. Corregir la Obs. 5.2(i) sobre la cardinalidad como estado (m1) y la línea desfasada de CONTINUIDAD `:43` (m8).
8. Volver a 11 páginas con los recortes (a)–(d) de m10, o justificar las 12 en el README.
9. Usar `\texorpdfstring` en los títulos de E2 y E4 (m11).
