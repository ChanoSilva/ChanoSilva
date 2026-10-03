# TCD001 — Complejidad del objetivo ANY con signo para p ≥ 2 (derivación)

Archivos: `theory/signed_any.tex` (bloque para `main.tex`), `theory/check_signed_any.py` →
`theory/check_signed_any_output.txt`, `theory/signed_any_results.json`. `main.tex` no se tocó. El bloque se
compiló en una copia de `main.tex` en el scratchpad (pdflatex + bibtex: 0 errores, 0 referencias indefinidas,
0 cajas sobrellenas; 15 páginas frente a 13).

## 0. Resultado en una línea

**La pregunta de la Obs. 5.2(iv) NO queda resuelta.** No se demuestra ni NP-dureza ni un algoritmo polinomial
para el número de fragilidad con signo con p ≥ 2 (fijo o en la entrada). Se demuestra: (1) un caso polinomial
(soporte vacío en D, cualquier p, bajo unicidad); (2) una identidad exacta (forma de Cauchy–Binet) de la única
condición bilateral para p = 2, |S| = 1, que explica por qué el gadget de Subset Sum del Teorema 5.4 no se
adapta dentro de familias de ítems polinomiales; (3) una identidad exacta para gadgets tipo X3C con filas de
tripleta uniformes y anclas conservadas: todo el KKT es afín en un único escalar f(K), así que las coberturas
exactas no quedan aisladas. (2) y (3) son afirmaciones sobre familias de gadgets, no cotas de complejidad.

## 1. El problema

Objetivo ANY con signo (Def. 2.2): R ≠ ∅ propio es testigo si el Lasso en D∖R tiene minimizador único y
(S(D∖R), s(D∖R)) ≠ (S, s). Versión de decisión natural de "calcular f^signed": dado (X, y, μ, k), ¿f^signed ≤ k?
Está en NP (certificado R más el certificado de unicidad de la prueba del Teorema 5.4 para p fijo, o de la del
Teorema 5.8 con p en la entrada). La versión "¿existe algún testigo?" es casi siempre trivial cuando S ≠ ∅ (con
K = {i}, el minimizador tiene soporte de tamaño ≤ 1), por eso la pregunta interesante es la de umbral k.

## 2. Caso polinomial: soporte vacío en D (Proposición prop:signed-empty) — demostrado

Hipótesis: ‖Xᵀy‖_∞ ≤ μ (S(D) = ∅). Sea K = [n]∖R, μ' = μ_{|R|}, q = X_Kᵀy_K.

1. β = 0 minimiza en D∖R ⟺ ‖q‖_∞ ≤ μ' (KKT: 0 ∈ −q + μ'∂‖0‖₁).
2. Todos los minimizadores comparten ajuste y norma ℓ₁ (Tibshirani 2013). Si 0 es minimizador, la norma común
   es 0, así que 0 es el único: soporte con signo (∅,·) = el de D ⇒ R no es testigo.
3. Si ‖q‖_∞ > μ', ningún minimizador es 0, el soporte con signo cambia; R es testigo ⟺ el minimizador es único.
4. ‖q‖_∞ > μ' ⟺ ∃j: |X_{K,j}ᵀy_K| > μ'. Para cada j es el problema p = 1 con a_i = x_ij y_i y |T_j| ≤ μ (por
   hipótesis): el menor |R| que lo logra es f⁰_j, que el Teorema 5.1(b) da tras ordenar (a_i): con σ⁺_k, σ⁻_k las
   sumas de los k mayores/menores, hay R de tamaño k sii T_j − σ⁻_k > μ_k o T_j − σ⁺_k < −μ_k.
5. Luego f^signed ≥ f⁰ := min_j f⁰_j, con igualdad si en todo subconjunto el minimizador es único (p. ej. columnas
   de cada X_K en posición general, c.s. en diseños continuos). Coste O(p n log n).

Alcance: es un caso particular (nada seleccionado en D); no dice nada del caso S(D) ≠ ∅, que es el de los
experimentos con señal.

## 3. Forma de Cauchy–Binet (Lema lem:cb) — demostrado

p = 2, S = {1}, s = +, G₁₁ > 0. El candidato es β̃₁ = (q₁ − μ')/G₁₁ y c₂ = q₂ − G₁₂ β̃₁. Fallos posibles:
q₁ ≤ μ' (unilateral, lineal: se resuelve ordenando como en el Teorema 5.1(c)), c₂ ≥ μ' o c₂ ≤ −μ'.

G₁₁ c₂ = G₁₁ q₂ − G₁₂ q₁ + μ' G₁₂, y G₁₁q₂ − G₁₂q₁ = det(X_{K,{1,2}}ᵀ [X_{K,1}, y_K]) = Σ_{i<l} m_il m'_il por
Cauchy–Binet, con m_il = x_i1 x_l2 − x_l1 x_i2 y m'_il = x_i1 y_l − x_l1 y_i. Por tanto

  G₁₁(c₂ − μ') = Σ_{i<l∈K} m_il m'_il − μ' Σ_{i∈K} x_i1(x_i1 − x_i2),
  G₁₁(c₂ + μ') = Σ_{i<l∈K} m_il m'_il + μ' Σ_{i∈K} x_i1(x_i1 + x_i2).

Ítems x_i = (1, 1 + e b_i), y_i = y₀ + y₁ b_i: m_il = e(b_l − b_i), m'_il = y₁(b_l − b_i), y la parte ítem–ítem es
e y₁ Σ_{i<l}(b_l − b_i)² = e y₁ (N Σb_i² − σ²). Con un ancla (α_g, β_g), y_g: m_ig = β_g − α_g(1 + e b_i),
m'_ig = y_g − α_g(y₀ + y₁ b_i), cuyo término en b_i² es e y₁ α_g² ≥ 0. El coeficiente total de Σ b_i² es
e y₁ (N + Σ_g α_g²) ≥ e y₁ N y el de σ² es −e y₁: la parte cóncava en σ viene siempre acompañada de un término
en Σb_i² que la domina (σ² ≤ N Σ b_i²) y que no es función de (N, σ). Con ítems polinomiales en b_i en general,
la parte ítem–ítem es Σ Ψ(b_i, b_l) con Ψ simétrica y Ψ(b, b) = 0 (los menores se anulan en filas iguales), lo que
excluye Ψ(b, b') = −2bb' + κ₁(b + b') + κ₀, la forma que exigiría −(σ − t)² (en la diagonal daría −2b² + 2κ₁b + κ₀,
que no es idénticamente 0).

## 4. Por qué no se adapta el Teorema 5.4 (Obs. rem:gadgets (i))

En el Teorema 5.4 la ventana Δ = 0 nace del quiebre en que la variable 1 se activa (β₁* = Δ₊/G₁₁): toda familia
conservada con Δ ≤ 0 ya cambia el soporte con signo (la variable 1 sale), así que hay testigos con signo
"unilaterales" (quitar los ítems mayores hasta que σ ≤ t) que se encuentran ordenando. Dentro de un soporte con
signo fijo todo es racional y suave en las sumas; una ventana tendría que venir de la curvatura de §3, y en las
familias de ítems afines/polinomiales esa curvatura está dominada por Σb_i².

**Ruta explorada y no cerrada (no se afirma).** Con respuestas racionales (no polinomiales), p. ej. ítems
x_i = (1, r_i), y_i = −1/r_i, la parte cuadrática se vuelve (Σr)(Σ1/r) = C² − S² (C = Σcosh s_i, S = Σsinh s_i,
r_i = e^{s_i}) y el término molesto pasa a ser de cuarto orden. Pero al hacer el cálculo con anclas resulta que
en la ventana G₁₂ ≈ 0 y q₁ − μ ≈ 0 a la vez: la variable 1 queda en su umbral y reaparece el fallo unilateral
"la variable 1 sale". Parece que se podría compensar con un desplazamiento común grande de los números (todas
las familias con N₀ ítems tendrían σ por encima del umbral de salida) y con el presupuesto k = m − N₀, pero
faltan: las cotas explícitas, el caso N > N₀, la eliminación de anclas y la unicidad. Es la ruta más prometedora
para la dureza débil con p = 2 fijo; no está demostrada.

## 5. Por qué no se adapta el Teorema 5.8 (Obs. rem:gadgets (ii)) — identidad demostrada

Gadget: columnas 0 (objetivo) y e ∈ U (|U| = 3q). Filas de tripleta i ∈ K: x_i0 = θ, x_iU = c_i (incidencia),
y_i = 3b₀ + γ. Para cada e, L filas ancla x_0 = φ, x_e = 1, y = b₀ + μ/L. Todas las anclas conservadas, regla C.
Candidato en el soporte con signo fijo (U, +): G_UU = L I + C_KᵀC_K, q_U − μ1 = L b₀ 1 + (3b₀ + γ) C_Kᵀ1.
Como C_K 1 = 3·1 (cada tripleta tiene 3 elementos), (L I + C_KᵀC_K) b₀1 = L b₀ 1 + 3b₀ C_Kᵀ1, luego

  β̃_U = b₀1 + γ (L I + C_KᵀC_K)⁻¹ C_Kᵀ1 = b₀1 + γ C_Kᵀ (L I + M_K)⁻¹ 1   (M_K = C_K C_Kᵀ, "push-through").

Residuos de tripleta: r = (3b₀ + γ)1 − C_K β̃_U = γ[1 − M_K (L I + M_K)⁻¹1] = γ L (L I + M_K)⁻¹ 1.
Residuo de ancla de e: b₀ + μ/L − β̃_e. Correlación del objetivo:
c₀ = θ 1ᵀr + φ L Σ_e (b₀ + μ/L − β̃_e) = θγL f + 3qφμ − φL γ·1ᵀC_Kᵀ(LI + M_K)⁻¹1 = 3qφμ + γL(θ − 3φ) f,
con f(K) = 1ᵀ(L I + M_K)⁻¹ 1 (usando otra vez C_K 1 = 3·1). Cualquier umbral sobre c₀ (y sobre cualquier
funcional uniforme de los residuos de tripleta) es un umbral sobre el escalar f. Para L grande,
f ≈ N/L − Σ_e cov_e²/L² + O(N m²/L³): crece con N y decrece con los solapamientos; para que las coberturas
exactas fueran el máximo entre las familias con N ≥ q haría falta restar casi exactamente N/L, y una columna
"contador" sólo cambia f por f/(1 + f/a_z) (Sherman–Morrison), monótona. En la comprobación (30 gadgets con
q = 2, 9 con cobertura exacta) ninguna cobertura exacta es el máximo o el mínimo estricto de f. El mecanismo
del Teorema 5.8 aísla las coberturas precisamente porque los absorbentes cambian de estado, y eso ya es un
cambio de soporte con signo.

**Ruta explorada y no cerrada (no se afirma).** En la parametrización por eliminación (Prop. 3.1), con
residuos y X̃ uniformes en las tripletas, todo es afín en h(R) = 1ᵀ(I − H_R)⁻¹1 ≈ |R| + Σ_e(cov^R_e)²/a', creciente
en |R| y en los solapamientos; lo que haría falta es −α|R| + β'Σ_e(cov^R_e)² con α > 3β' (entonces las coberturas
exactas serían los mínimos estrictos con |R| ≤ q). Bajo la regla P el umbral μ' = μ(n − |R|)/n aporta un término
lineal en |R| de signo opuesto: candidato para la dureza fuerte con p en la entrada bajo la regla P, sin
completar (faltan anclas removibles, signos de los absorbentes, unicidad).

## 6. Verificación (`theory/check_signed_any.py`, semilla 20261003, aritmética exacta, 3.8 s de CPU)

- (A) 400 instancias con S(D) = ∅ (p ∈ {2, 3}, n ∈ {5,…,8}, ambas reglas; una de cada cuatro con entradas en
  {−2,…,2}, adversarial por empates), búsqueda exhaustiva sobre todos los R ≠ ∅ propios con resolución KKT
  exacta (3^p soportes con signo, unicidad certificada por rango completo y desigualdades estrictas):
  f^signed ≥ f⁰ en 400/400; el menor |R| con ‖X_Kᵀy_K‖_∞ > μ' coincide con f⁰ en 400/400; f^signed = f⁰ en
  397/397 instancias sin subconjuntos empatados (3 instancias tienen algún subconjunto no certificado).
- (B) Identidad del Lema lem:cb: 295/295 submuestras aleatorias; forma de ítems e y₁(NΣb² − σ²): 200/200.
- (C) Identidades del gadget X3C (c₀ y residuos de tripleta): 344/344 familias conservadas en 30 gadgets;
  coberturas exactas como máximo/mínimo estricto de f: 0 de 9.

No hay reducción que verificar (no se obtuvo); la parte (ii) del encargo (algoritmo vs. exhaustiva) se cumple
para el único algoritmo nuevo, el de la Proposición prop:signed-empty.

## 7. Qué queda abierto

1. Complejidad de f^signed ≤ k para p = 2 fijo con S(D) ≠ ∅ (la ruta de §4 con respuestas racionales es la
   candidata a dureza débil; tampoco se descarta un algoritmo polinomial).
2. Con p en la entrada: dureza (fuerte) de f^signed; la ruta de §5 con la regla P es candidata.
3. Si hubiera dureza para p fijo, sería débil con datos enteros (Prop. 5.5), como las demás.

## 8. Cambios propuestos (no aplicados)

- Pegar el bloque de `signed_any.tex` al final de la Sección 5 (Prop. 5.12, Lema 5.13, Obs. 5.14, Obs. 5.15).
- Obs. 5.2(iv): añadir "; it is polynomial when nothing is selected on D (Proposition prop:signed-empty), and
  Remark rem:gadgets explains why the gadgets of Theorems thm:enter2 and thm:strong do not adapt".
- Tabla de afirmaciones: nueva fila "Signed f_ANY for p ≥ 2 polynomial when S(D) = ∅ under uniqueness;
  Cauchy–Binet form and gadget identities — proved here; verified (exact)". La fila "complexity of the signed
  f_ANY for p ≥ 2 — open" se mantiene.
- Next steps (a): "… for p ≥ 2 when S(D) ≠ ∅; Remark rem:gadgets rules out the natural adaptations of the
  existing gadgets and points to rational item families (p fixed) and to rule P (p in the input)".
- CONTINUIDAD, "Queda abierto" (ii): igual en sustancia; añadir el caso polinomial y las dos identidades como
  avance parcial.
- Macros opcionales: \SignedEmptyTotal = 400, \SignedEmptyClean = 397, \SignedEmptyAgree = 397,
  \SignedEmptyTies = 3, \SignedCBOk = 295, \SignedVarOk = 200, \SignedGadgetOk = 344, \SignedGadgetCovers = 9.
