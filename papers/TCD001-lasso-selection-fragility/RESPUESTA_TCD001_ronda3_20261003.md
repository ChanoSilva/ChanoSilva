# Respuesta del autor — TCD001, ronda 3 de revisión interna (03/10/2026)

Objeto: informe `REFEREE_TCD001_ronda3_20261003.md` (cambios menores; 0 bloqueantes, 2 mayores, 12 menores; teoremas de v0.4 correctos; 16/16 puntos de la ronda 2 bien aplicados) e integración del trabajo de `theory/` sobre dureza fuerte (`strong_hardness.tex`, `strong_hardness_derivation.md`, `check_strong.py`). Versión resultante: borrador v0.5 (3 October 2026).

*Documento escrito de forma incremental; las secciones marcadas "pendiente" se completan a medida que se aplican los cambios.*

## Resumen

(pendiente)

## Verificación propia del teorema de dureza fuerte (theory/)

Leí `theory/strong_hardness.tex` y `strong_hardness_derivation.md` línea a línea y rehíce cada paso a mano antes de integrarlos. Resultado: **el teorema es correcto**; encontré cuatro imprecisiones, ninguna afecta al enunciado, y las corregí al integrarlo.

| Pieza | Qué comprobé | Resultado |
|---|---|---|
| Parámetros | ε = (ηS − θ)/μ = (m/2 − 1/(24q))/(m+1) ∈ (0, ½) para m, q ≥ 1, luego ρ ∈ (½, 1); κ = ρ + ½. Identidades (eq:theta): θ = ηS − (1−ρ)μ es la definición de ρ; ρμ + ηS = μ − (1−ρ)μ + ηS = μ + θ; κS + ρ = ρ(S+1) + ηS = ρμ + ηS. | Correcto. |
| Gram y correlaciones de los absorbedores | Un ancla a_e sólo toca la columna e entre los absorbedores ⇒ G_ee = u²·1[e∈P] + cov_e, G_ee′ = nº de tripletas conservadas con e y e′ (≥ 0), Σ_{e′≠e} G_ee′ = Σ_{i∋e}(\|C_i\|−1) = 2cov_e; q_e = u·(S/u)·1[e∈P] + cov_e. | Correcto. |
| Lema lem:absorb | (1) G_PP = u²I + (Gram de las tripletas) ⪰ u²I ⇒ el problema no negativo tiene minimizador único b*. (2) KKT no negativo ⇒ c_e ≤ μ en P, = μ donde β_e > 0. (3) β_e > 0 ⇒ G_eeβ_e ≤ q_e − μ = cov_e − 1 (G_ee′ ≥ 0, β ≥ 0) ⇒ cov_e ≥ 2, u²β_e ≤ cov_e − 1, β_e ≤ (m−1)/u². (4) Acoplamiento ≤ 2cov_e(m−1)/(9m²) ≤ 2cov_e/(9m) ≤ cov_e. (5) e ∈ B: c_e ∈ [0, cov_e] ⊆ [0, m], \|c_e\| < μ = m+1; e ∈ P inactivo: c_e ≥ S > 0 (el texto da la cota más débil S − 2/9, válida); activo: c_e = μ. Así β cumple el KKT del Lasso con signo y es minimizador; c_e ∈ [0, μ]. (6) Soporte = P₂: si cov_e ≥ 2, e ∈ P y β_e = 0, c_e ≥ S + cov_e(1 − 2/(9m)) ≥ S + 14/9 > μ. (7) Cota inferior: G_eeβ_e ≥ cov_e − 1 − 2cov_e/(9m) ≥ cov_e(½ − 2/9) = (5/18)cov_e ≥ 5/9 y G_ee ≤ u² + m ⇒ u²β_e ≥ (5/9)·9m/(9m+1) ≥ (5/9)(9/10) = ½. El lema afirma sólo la existencia de *un* minimizador con estas propiedades (sin anclas las columnas de absorbedores pueden ser dependientes); el teorema sólo usa su residuo, que es común a todos los minimizadores. | Correcto. |
| Identidad de la columna objetivo | Tripleta: ρw·3 = ρ/q; ancla: (ρ + η)wu = κu/(3q). ⇒ X_{K,0} = ρwΣ_eX_{K,e} + ηwuΣ_{e∈P}δ_{a_e}; u·r_{a_e} = S − u²β_e. | Correcto. |
| Caracterización (i)–(iii) | Cota general c₀ ≤ μ + θ − ηwS\|B\| − ηwΣ_P u²β_e (porque c_e ≤ μ, w\|U\| = 1). (i) B ≠ ∅: pérdida ηwS = m/(6q) > 1/(24q). (ii) B = ∅, P₂ ≠ ∅: pérdida ≥ ηw/2 = 1/(12q) > θ. (iii) B = ∅, P₂ = ∅: β = 0, c_e = S + cov_e, c₀ = μ + θ − ρ(q−N)/q; N = q ⇔ cubierta exacta (3q incidencias, cada cov_e ≤ 1); N ≤ q−1 ⇒ pérdida ρ/q > 1/(2q) > θ. Cota inferior c₀ > 0 (si P = ∅ hay N ≥ 1 tripletas y Σc_e = 3N > 0). | Correcto. |
| Unicidad en el testigo y en D | Anclas ⇒ bloque uI en los absorbedores; X_{K,0} = Σϑ_eX_{K,e} fuerza ϑ_e = κw y una tripleta daría κ/q ≠ ρ/q (η = ½ > 0). Rango completo ⇒ objetivo estrictamente convexo. En D: 3m incidencias > 3q si m > q ⇒ algún cov_e ≥ 2 ⇒ caso (ii). | Correcto. |
| Reescalado entero | ρ = (12qm + 24q + 1)/(24q(m+1)); con α = 24q²(m+1), α′ = 3: αρ/q = 12qm + 24q + 1; ακu/(3q) = m(12qm + 24q + 1) + 12qm(m+1); αu = 72q²m(m+1); y ∈ {3, 1}; μ = 72q²(m+1)² ≤ 72n⁴ (q ≤ n, m + 1 ≤ n). | Correcto. |
| Pertenencia a NP (p en la entrada) | Certificado R, soporte con signo, 2p duales. M = {β : G(β − β̂) = 0, ‖β‖₁ ≤ ‖β̂‖₁} es el conjunto de minimizadores; único ⇔ max = min = β̂_k en cada coordenada; LP factibles y acotados. | Correcto con un matiz (abajo, punto 2). |
| Corolario cor:strong-f | f_ENTER(0) = m − q en las instancias SÍ (los testigos son exactamente los complementos de cubiertas). | Correcto, con un matiz de redacción (abajo, punto 3). |

Imprecisiones encontradas y corregidas en la integración:
1. **Casos triviales.** La prueba sólo excluye "la familia ya es una partición"; con m = 0 la construcción degenera (u = 0). Se sustituye por: "si m ≤ q la respuesta se decide directamente (SÍ sii m = q y los conjuntos son disjuntos) y se devuelve una instancia SÍ o NO fija; en adelante m > q", que además hace inmediato que en D algún cov_e ≥ 2.
2. **Duales básicos.** "Por dualidad fuerte cada LP tiene una solución dual básica óptima" exige que el poliedro dual sea puntiagudo; con G singular las filas de la igualdad G β = G β̂ son dependientes y el dual tiene un espacio de linealidad. Se añade: "tras descartar las filas linealmente dependientes de la igualdad (lo que no cambia el conjunto factible) el poliedro dual es puntiagudo", y entonces existe un vértice óptimo dado por Cramer.
3. **"La dependencia exponencial en p no puede eliminarse".** La dureza fuerte excluye un algoritmo polinomial en (n, p, M), no uno de la forma g(p)·poly(n, M) (eso sería una pregunta de complejidad parametrizada, W[1], que no se estudia). Se escribe "cannot be made polynomial in p".
4. **Frase "the route sketched after Conjecture 5.8 lacked"**: la conjetura desaparece; se reformula sin la referencia cruzada.

Además (no es un error de la prueba, pero sí de alcance, en línea con M2 del árbitro): el teorema es sobre ENTER; en su construcción los testigos ANY (con o sin signo) son triviales (quitar una tripleta que cubre un elemento dos veces cambia el soporte de los absorbedores), así que no dice nada del objetivo ANY con signo de los experimentos. Así se dice en la Obs. 5.2(iv) y en la conjetura revisada.

Verificación computacional: ver "Cómputo y compilación" (corrida de `check_strong.py` y comprobación independiente propia).

## Hallazgos mayores

**M1. "Dureza débil" sin la restricción a datos enteros.** → **Aceptado.** El árbitro tiene razón: los Teoremas 5.1 y 5.4 son para datos racionales y la Prop. 5.5 sólo da un algoritmo pseudo-polinomial para datos enteros (un factor común que lleve datos racionales a enteros puede tener tamaño exponencial). Cambios: resumen ("in both cases weak for integer data (a pseudo-polynomial algorithm exists for integer data and every fixed p)"); introducción ("makes all this hardness weak for integer data"); Obs. 5.2(i) ("weak for integer data … excluded for p = 1 and integer data") y (ii) ("to integer data and every fixed p"); tabla de afirmaciones ("for integer data a pseudo-polynomial algorithm …, so for integer data these problems are only weakly NP-complete for fixed p"); Limitations ("weak for integer data and every fixed p; for rational data with many distinct denominators the pseudo-polynomial algorithm does not apply"); README y FICHA ("con datos enteros"). El Corolario 5.6 ya estaba bien restringido y no cambia.

**M2. El objetivo ANY con signo (el de los experimentos) no estaba tratado; "fragility number NP-hard in general".** → **Aceptado.** Lo demostré y lo incorporé como **Teorema 5.1(c)** [proved here]: para p = 1 el minimizador es único en todo D∖R (estrictamente convexo si x_K ≠ 0; μ′\|β\| más una constante si x_K = 0); si \|T\| ≤ μ un testigo ANY con signo es un testigo de selección (parte (b)); si \|T\| > μ y s = sgn T, el soporte con signo se conserva sii s·Σ_{i∉R}a_i > μ_{\|R\|}, y sobre \|R\| = k el mínimo de s·Σ_{i∉R}a_i es sT − σ_k^{(s)} (σ_k^{(s)} = suma de los k mayores valores s·a_i), así que hay testigo de tamaño k sii sT − σ_k^{(s)} ≤ μ_k; una ordenación da todos los σ_k^{(s)}: O(n log n). Comprobado además en aritmética exacta contra búsqueda exhaustiva en 2 400/2 400 instancias aleatorias con empates y ceros, ambas reglas (`experiments/check_signed_any_p1.py` → `results/signed_any_p1.json`, macros `\SignedPOneAgree`/`\SignedPOneTotal`; 0.8 s). Texto: nueva Obs. 5.2(iv) ("the reductions say nothing about the signed ANY target …: padding (c) with zero columns gives O(n log n), and in the constructions of Theorems 5.4 and 5.8 signed ANY witnesses always exist … Its complexity for p ≥ 2 is open (it is in NP, and pseudo-polynomial for integer data and fixed p)"); tabla de afirmaciones: la fila dice ahora "f_LEAVE and the unsigned f_ANY are NP-hard; for p = 1, selection witnesses and the signed f_ANY in O(n log n)", y una fila "complexity of the signed f_ANY for p ≥ 2 — open"; introducción ("… and the complexity of the signed fragility number for p ≥ 2 remain open"); resumen; Next steps (a); Limitations ("none of the hardness results covers the signed ANY target of the experiments"); CONTINUIDAD. Contraste con Moitra–Rohatgi (verificado por búsqueda, ver Bibliografía) en la Obs. 5.2(iii): algoritmo n^{O(d³)} para decidir si k eliminaciones cambian el signo de un coeficiente de mínimos cuadrados y exclusión de algoritmos n^{o(d)} bajo ETH; el cambio de signo es unilateral y la deselección es una ventana bilateral \|c_j\| ≤ μ, que es lo que codifica Subset Sum. Junto a la conjetura revisada: la cota ETH no se traslada (otro objetivo) y no se demuestra ninguna cota parametrizada en p.

Nota sobre el teorema nuevo de dureza fuerte (integración de `theory/`): con él, "only strong hardness with unbounded p remains open" deja de ser cierto también por otra razón; la introducción dice ahora que con p en la entrada los testigos de selección son fuertemente NP-completos bajo la regla C (Teorema 5.8), y que quedan abiertas la dureza fuerte para deselección/ANY sin signo/regla P (Conjetura 5.11) y la complejidad del ANY con signo para p ≥ 2.

## Hallazgos menores

| Id | Decisión | Qué se cambió y dónde |
|---|---|---|
| m1 | Aceptado | Obs. 5.2(i): "(with the cardinality as a second state, which rule P needs also for the existence question)". |
| m2 | Aceptado | `experiments/check_hardness.py` ya no escribe la línea `elapsed` en el log congelado (sólo la imprime y la guarda en `hardness.json`, `meta.seconds`); `meta.log_has_timing = false`. Nueva corrida (38 s): log idéntico al anterior salvo esa línea (diff vacío); SHA-256 nuevo `8652338a0a6d7921…`. `make_numbers.py` comprueba además que el log no tiene línea de tiempo. Lo mismo para `check_strong.py` (ver integración). Apéndice A: "the logs carry no timing lines (times go to the JSON files) and are frozen by SHA-256 prefixes that a rerun reproduces". |
| m3 | Aceptado | `check_hardness.py` reinicia `lf.KKT_STATS` y lo vuelca en `hardness.json` (`meta.kkt_guard`): 33 484 llamadas, 0 retrocesos, error activo máximo 1.6·10⁻¹⁴ (coincide con la repetición del árbitro). Macros `\HardKKTFits`, `\HardKKTFallbacks` con aserción "0 retrocesos". Limitations: "never in E1–E5 (144,264 fits) or in the hardness check for fixed p (33,484 fits)". La verificación de dureza fuerte sí activa la guarda (340 de 1 560 ajustes, empates exactos por construcción) y así se dice. |
| m4 | Aceptado | Apéndice B (la construcción pasó allí por m10(b)): "a shift that makes q₁ − μ′ = σ − t independent of \|K\| whenever the gadget is kept". |
| m5 | Aceptado | Prueba de pertenencia a NP: "an initial piece of it from β̂ lies in one closed orthant, whose intersection with M is then a polytope of dimension ≥ 1 and has a vertex other than β̂"; y "(for p in the input see the proof of Theorem 5.8)", que da certificados duales. |
| m6 | Aceptado | "Let … t ≥ 1 the target. If t ≥ B the answer is immediate (for t = B the construction below would have Δ = 0 on D, so variable 2 would be active on D) …"; se eliminó el caso t ≤ 0 (convención t ≥ 1). |
| m7 | Aceptado | Tras el Teorema 5.4: "The conditions on D are checked in polynomial time for fixed p (proof of membership in NP), so instances violating them can be rejected"; en la prueba: "The same procedure checks the conditions on D". |
| m8 | Aceptado | CONTINUIDAD: la línea desfasada dice ahora "La dureza es débil para datos enteros y todo p fijo, usa datos con estructura especial; con p en la entrada, ENTER es fuertemente NP-completo (regla C)". |
| m9 | Aceptado | "In the construction (Appendix B) the slack Δ = σ − t between a kept subset sum and the target is an integer and the kink leaves a window of width less than one around Δ = 0, so …". |
| m10 | Aceptado con matiz | (a) La Obs. 5.7 queda en una frase con remisión al Apéndice A; (b) el párrafo "Construction" del Teo. 5.4 pasó al Apéndice B (en el cuerpo queda una frase); (c) E4: se quitaron el factor por celda, los tiempos en ms de B y la lista de exactitud por n (todo está en `results/scaling.md`, al que se remite); (d) las filas de los Teo. 5.1 y 5.4 de la tabla de afirmaciones se unieron. Además: lemas 5.3 y "entry-any" de theory/ fusionados en un único Lema 5.3; Apéndice A comprimido; introducción, Obs. 3.3, 3.5, E3 y Limitations abreviadas; estilo `abbrvnat`. **Matiz:** con el teorema de dureza fuerte (enunciado, esquema y prueba completa, ≈ 1.5 páginas) el objetivo de ≤ 12 páginas no se alcanza sin quitar tablas o pruebas; ver "Cómputo y compilación". |
| m11 | Aceptado | `\texorpdfstring{$n\le14$}{n <= 14}` y `\texorpdfstring{$n$}{n}` en los títulos de E2 y E4: 0 avisos "Token not allowed". |
| m12 | Aceptado | Obs. 5.2(iii): Moitra–Rohatgi (algoritmo n^{O(d³)}, exclusión de n^{o(d)} bajo ETH) y el contraste unilateral/bilateral; junto a la Conjetura 5.11: "the ETH bound of Moitra and Rohatgi concerns least-squares signs and does not transfer". Opcionales: Hu et al. (NeurIPS 2024) añadido en E3 (verificado por búsqueda: autores, sede, arXiv:2409.18153; su resumen dice que las heurísticas voraces basadas en influencia pueden fallar incluso en regresión lineal y que la versión adaptativa captura parte de las interacciones, lo que coincide con E3); Konrad–Kuschnig (ICLR 2026) no se añade: no hay en el texto una afirmación que lo necesite. |

## Bibliografía

(pendiente)

## Cómputo y compilación

(pendiente)

## Lo que queda abierto

(pendiente)
