# TCD001 — Derivación: dureza fuerte con p creciente (Conjetura 5.8), notas de trabajo 03/10/2026

Notación de `main.tex`: Lasso en forma suma, regla C (μ' = μ), testigo = R propio no vacío con minimizador
único en D∖R y objetivo cumplido; K := [n]∖R. Todo lo que sigue es para la **regla C** y el objetivo
**ENTER** (Selection-Witness). Archivo de verificación: `check_strong.py` → `check_strong_output.txt`.

## 0. Diagnóstico de la ruta anterior (hardness_derivation.md §4)

La ruta "d absorbedores + suma vectorial exacta" no se cerró por dos motivos: (1) con varios absorbedores
activos acoplados por la matriz de Gram no se controlaba ni el signo ni el tamaño de sus coeficientes
(podía haber absorbedores con signo negativo que *suben* la correlación de la variable objetivo);
(2) si la fila "gadget" de un absorbedor se quita, ese absorbedor deja de estar dominado y su
comportamiento es arbitrario. Aquí se resuelven ambos con tres ingredientes:

* **anclas dominantes**: cada absorbedor e tiene una fila propia a_e con entrada u, u² ≥ 9m² ≫ el acoplamiento
  (≤ 2·cov_e por fila de Gram). Con todas las entradas de X y de y no negativas, el Lasso restringido a los
  absorbedores coincide con un Lasso *no negativo* (todos los coeficientes ≥ 0) y su soporte se lee de
  enteros: e activo ⇔ cov_e ≥ 2;
* **desplazamiento grande S = m**: el ancla aporta S a q_e, y μ = S + 1. Si se quita el ancla de e,
  q_e = cov_e ≤ m < μ: el absorbedor queda inactivo y no perturba a los demás;
* **margen estrecho θ**: la variable objetivo es ρ·(promedio de absorbedores) + una desviación η sobre las
  anclas; el margen de entrada θ = ηS − (1−ρ)μ se fija en 1/(24q), menor que todo lo que se pierde en los
  casos malos (quitar un ancla, un absorbedor activo, un elemento sin cubrir). Ya no hace falta que la
  absorción "gane" a toda la desviación, solo al margen θ.

Lo que mata la entrada no es que la correlación de los absorbedores caiga, sino que la parte de desviación
η w Σ_e (S − u²β_e) baja en ≥ η w/2 en cuanto hay un absorbedor activo, y que ρ w Σ_e c_e ≤ ρμ siempre
(combinación convexa de correlaciones acotadas por μ).

## 1. Construcción (X3C → Selection-Witness, regla C)

Fuente: **Exact Cover by 3-Sets** (X3C; Garey–Johnson [SP2], NP-completo en sentido fuerte porque no tiene
números): universo U = {1..3q}, familia C_1..C_m de subconjuntos de 3 elementos; ¿hay q de ellos disjuntos
dos a dos (equivalentemente, una partición de U)? Casos triviales: si la propia familia es una cubierta
exacta (m = q y disjuntos) se devuelve una instancia SÍ fija. Si no, se usa:

Parámetros: d = 3q, w = 1/d, u = 3m, S = m, μ = S + 1, η = 1/2, θ = 1/(24q),
ε = (ηS − θ)/μ = (12qm − 1)/(24q(m+1)) ∈ (0, 1/2), ρ = 1 − ε ∈ (1/2, 1), κ = ρ + η.

Columnas: 0 (objetivo), e ∈ U (absorbedores); p = 3q + 1. Filas (n = m + 3q):

| fila | x_0 | x_e (e ∈ U) | y |
|---|---|---|---|
| tripleta i ∈ [m] | ρ/q | 1 si e ∈ C_i, 0 si no | 1 |
| ancla a_e, e ∈ U | κ w u | u en la columna e, 0 en las demás | S/u |

Identidad clave: X_0 = ρ w Σ_e X_e + η w u Σ_e δ_{a_e} (filas tripleta: ρ w·3 = ρ/q; anclas: ρwu + ηwu = κwu).

Entero: con α = 24q²(m+1), α' = 3, (αX, α'y, αα'μ) es entero; y ∈ {1, 3}, |x| ≤ 72q²m(m+1),
μ = 72q²(m+1)². El reescalado (αX, α'y, αα'μ), β = (α'/α)β', multiplica el objetivo por α'² (apéndice de
main.tex): soportes, unicidad y testigos no cambian. **Números polinómicamente acotados ⇒ dureza fuerte.**

## 2. Lema A (criterio de entrada para p arbitrario) — DEMOSTRADO

Sea r₋ⱼ el residuo del Lasso en (X_{K,−j}, y_K, μ') (único: todos los minimizadores comparten el ajuste,
Tibshirani 2013). (a) Si |X_{K,j}ᵀ r₋ⱼ| ≤ μ', (b̂, β_j = 0) cumple KKT para cualquier minimizador b̂ del
restringido ⇒ existe minimizador con β_j = 0 ⇒ R no es testigo de ENTER(j) (o no es único, o j ∉ S).
(b) Si > μ', un minimizador con β_j = 0 minimizaría el restringido (F(b,0) = min F ≤ min F₋ⱼ), tendría
residuo r₋ⱼ y violaría KKT en j. Es el Lema 5.3 sin la fórmula explícita de β₁*.

## 3. Lema B (absorbedores) — DEMOSTRADO

Fijo K. P := {e : a_e ∈ K} (anclados), B := U∖P, cov_e := #tripletas conservadas que contienen e,
N := #tripletas conservadas. Gram de absorbedores en K: G_ee = u²[e∈P] + cov_e,
G_ee' = #tripletas conservadas que contienen e y e' (≥ 0), Σ_{e'≠e} G_ee' = 2 cov_e;
q_e = S[e∈P] + cov_e ≥ 0. Afirmación: el Lasso restringido a los absorbedores tiene un minimizador β con
β_B = 0, β_P ≥ 0, soporte exactamente P₂ := {e ∈ P : cov_e ≥ 2}, u²β_e ≥ 1/2 en P₂, u²β_e ≤ cov_e − 1,
y correlaciones c_e = q_e − (Gβ)_e ∈ [0, μ] para todo e.

Prueba. b* := minimizador (único, G_PP ⪰ u²I) de ½bᵀG_PP b − (q_P − μ1)ᵀb sobre b ≥ 0; β := (b*, 0).
KKT no negativo: c_e ≤ μ en P, = μ si β_e > 0. Si β_e > 0: G_ee β_e = cov_e − 1 − Σ_{e'≠e}G_ee'β_e'
≤ cov_e − 1 ⇒ β_e ≤ (m−1)/u² y u²β_e ≤ cov_e − 1 (y β_e > 0 ⇒ cov_e ≥ 2). Acoplamiento:
Σ_{e'≠e} G_ee'β_e' ≤ 2cov_e(m−1)/u² ≤ 2cov_e/(9m). Entonces: e ∈ B ⇒ c_e ∈ [0, cov_e] ⊂ [0, m] ⊂ [−μ, μ);
e ∈ P inactivo ⇒ c_e ≥ m − 2/9 > 0; e activo ⇒ c_e = μ. Así β cumple el KKT del Lasso (con signo): es
minimizador, y su residuo es EL residuo. Soporte: si e ∈ P, cov_e ≥ 2 y β_e = 0, c_e ≥ S + cov_e − 2cov_e/(9m)
> S + 1 = μ, absurdo. Cota inferior en P₂: G_eeβ_e ≥ cov_e(1/2 − 2/9) = (5/18)cov_e y G_ee ≤ u² + m ⇒
u²β_e ≥ (5/9)·9m²/(9m²+m) ≥ 1/2. ∎

## 4. Teorema (dureza fuerte de ENTER, regla C) — DEMOSTRADO

c₀ := X_0ᵀ r con r el residuo del Lema B. Por la identidad de §1 y u·r_{a_e} = S − u²β_e:

    c₀ = ρ w Σ_e c_e + η w Σ_{e∈P} (S − u²β_e).

Cota superior general (c_e ≤ μ, Σ_e w = 1): c₀ ≤ ρμ + η w Σ_{e∈P}(S − u²β_e), y ρμ + ηS = μ + θ.
* (i) B ≠ ∅: c₀ ≤ μ + θ − ηwS ≤ μ + 1/(24q) − m/(6q) < μ.
* (ii) B = ∅, P₂ ≠ ∅: c₀ ≤ μ + θ − ηw/2 = μ + 1/(24q) − 1/(12q) < μ.
* (iii) B = ∅, P₂ = ∅ (todo cov_e ≤ 1): β = 0, r = y_K, c_e = S + cov_e, Σcov_e = 3N ≤ 3q y
  c₀ = κS + ρN/q = μ + θ − ρ(q − N)/q: si N = q (todo cov_e = 1: cubierta exacta) c₀ = μ + θ > μ;
  si N ≤ q − 1, c₀ ≤ μ + θ − ρ/q < μ (θ = 1/(24q) < ρ/q).
Cota inferior: c_e ≥ 0, S − u²β_e ≥ S − m + 1 = 1 > 0 ⇒ c₀ ≥ 0 > −μ.
Por el Lema A: |c₀| > μ ⇔ todas las anclas conservadas y las tripletas conservadas son una cubierta exacta;
en otro caso existe un minimizador con β₀ = 0 y R no es testigo.
Unicidad en el testigo: las anclas dan u·I en los absorbedores; si X_0 = Σθ_eX_e en K, las anclas fuerzan
θ_e = κw y una tripleta conservada daría 3κw = κ/q ≠ ρ/q: X_K tiene rango completo p ⇒ único, y 0 ∈ S(D∖R).
D: si la familia no es una cubierta exacta, D cae en (ii) o en (iii) con N < q ⇒ |c₀| < μ, X de rango
completo ⇒ minimizador único con 0 ∉ S(D). Testigo para SÍ (no trivial): R = tripletas fuera de la cubierta,
no vacío porque m > q, propio porque conserva las anclas. Recíprocamente todo testigo da una cubierta exacta.
f_ENTER(0) = m − q en las instancias SÍ.

**Enunciado demostrado**: con p parte de la entrada y la regla C, Selection-Witness (existencia de testigo
para ENTER(j)) es NP-duro en sentido fuerte: ya lo es con datos enteros acotados por 72q²(m+1)² (≤ 72n⁴,
y ∈ {1,3}), en instancias con minimizador único en D. Por tanto calcular f_ENTER(j) es NP-duro en sentido
fuerte, y no hay algoritmo polinómico en (n, p, M) salvo P = NP (la dependencia exponencial en p de la
Prop. 5.5 es esencial).

**Pertenencia a NP** (p en la entrada, cualquier regla): certificado R, el soporte con signo (S, s) del
minimizador en D∖R y 2p soluciones duales. El verificador resuelve el sistema KKT en S exactamente
(eliminación gaussiana, tamaño polinómico) y comprueba KKT; la unicidad equivale a que max/min β_k sobre el
politopo M = {β : G_K β = G_K β̂, ‖β‖₁ ≤ ‖β̂‖₁} valgan β̂_k (2p PL acotados y factibles); por dualidad fuerte
cada óptimo tiene un certificado dual óptimo básico, cuya codificación es polinómica (regla de Cramer sobre un
subsistema cuadrado no singular); el verificador solo comprueba factibilidad dual e igualdad de valores. No
se necesita resolver PL en tiempo polinómico (no se cita Khachiyan). ⇒ fuertemente NP-completo.

## 5. Verificación (check_strong.py → check_strong_output.txt, 107 s de CPU)

* 40 instancias X3C (20 SÍ, 20 NO): 38 con q = 2 (n ≤ 12, p = 7; 36 aleatorias con m ∈ {3,4,5,6} y dos a
  mano) y 2 con q = 3 (n = 13, p = 10); datos **enteros** escalados (máximo 12 960).
* En cada D∖R (81 840 subconjuntos) el Lasso se resuelve exactamente (propuesta flotante + KKT racional,
  respaldo por enumeración de los 3^p soportes con signo: 0 usos). Unicidad certificada por rango de X_E en
  todos los subconjuntos.
* Equivalencia (existe testigo ⇔ X3C SÍ): 40/40. Caracterización conjunto a conjunto (entra ⇔ anclas
  conservadas y cubierta exacta): 0 fallos. D: objetivo inactivo y único 40/40.
* Afirmaciones intermedias (problema sin la columna objetivo): soporte = {anclados con cov ≥ 2},
  coeficientes ≥ 0, |X_0ᵀ r₋₀| > μ ⇔ predicho: 0 fallos.
* Empates KKT (|c_e| = μ con β_e = 0) en 35 890 subconjuntos: son los absorbedores anclados cubiertos una vez,
  que están exactamente en el umbral por diseño; la unicidad está certificada igualmente.
* lasso_lars con guarda KKT (flotante) vs exacto: 0 discrepancias de soporte en 1 560 ajustes.
* Controles negativos: θ = 1/q (margen demasiado grande), θ < 0, S = 0 y u = 1 producen fallos (u = 1 solo en
  las afirmaciones intermedias del Lema B, no en la equivalencia: en estas instancias pequeñas la conclusión
  sobrevive sin dominancia, pero la prueba no la cubre).

## 6. Lo que NO se demuestra (sigue abierto)

* **Deselection-Witness (LEAVE) y ANY sin signo con p creciente**: sin dureza fuerte demostrada. La
  construcción de §1 no sirve tal cual (quitar tripletas cambia el soporte de muchas maneras, así que ANY es
  fácil de disparar en ella; para LEAVE haría falta un gadget que convierta "entra 0" en "sale v" con
  unicidad controlada, no construido).
* **Regla P**: μ' = μ(n−k)/n depende de |K| y rompe la igualdad exacta q_e = μ' en la cubierta (cada fila
  toca solo 3 absorbedores, así que el desplazamiento y_i = b_i + λ del caso p = 2 no se generaliza).
* **Datos en {−1, 0, 1} salvo escala común** (versión fuerte de la Conjetura 5.8): aquí los enteros llegan a
  72q²(m+1)²; las anclas de tamaño u = 3m son esenciales para la prueba.
* **W[1]-dureza en p** (ruta (c)): no estudiada; la reducción tiene p = 3q + 1 lineal en el tamaño, así que no
  dice nada paramétrico.

## 7. Entregable
`strong_hardness.tex`: Lema lem:entry-any, Teorema thm:strong, Corolario cor:strong-f, Observación
rem:verify-strong, conjetura revisada conj:strong-rest (texto propuesto para sustituir la Conjetura 5.8;
main.tex NO se tocó).
