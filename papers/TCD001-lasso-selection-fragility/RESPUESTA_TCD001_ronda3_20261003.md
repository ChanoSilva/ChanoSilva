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

(pendiente)

## Hallazgos menores

(pendiente)

## Bibliografía

(pendiente)

## Cómputo y compilación

(pendiente)

## Lo que queda abierto

(pendiente)
