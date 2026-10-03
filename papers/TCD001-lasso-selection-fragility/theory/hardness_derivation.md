# TCD001 — Derivación: estatus computacional para p ≥ 2 (notas de trabajo, 03/10/2026)

Notación de `main.tex`: Lasso en forma suma, reglas C (μ' = μ) y P (μ' = μ(n−k)/n), testigo = R propio
no vacío con minimizador único en D∖R y objetivo cumplido. K := [n]∖R (filas que se quedan).

## 0. Lema clave para p = 2 (criterio de entrada)

Para p = 2 y un subconjunto K con P := Σ_K x_{i1}^2 > 0, sean
A := Σ_K x_{i1} y_i, Bc := Σ_K x_{i2} y_i, Q := Σ_K x_{i1} x_{i2}.
El problema restringido (β_2 = 0) es estrictamente convexo, con solución β_1* = soft(A, μ')/P.
Por convexidad, existe un minimizador con β_2 = 0 sii (β_1*, 0) cumple KKT en la coordenada 2,
es decir sii |Bc − Q β_1*| ≤ μ'. Por tanto, si el minimizador en D∖R es único:

    la variable 2 está en S(D∖R)  ⇔  |Bc − Q·soft(A, μ')/P| > μ'.            (E)

(Si |·| ≤ μ', (β_1*,0) es minimizador y por unicidad es EL minimizador; si |·| > μ', ningún minimizador
tiene β_2 = 0, porque sería minimizador del problema restringido, i.e. (β_1*,0).)

Para p = 1 la selección es "salir de un intervalo" (fácil, Thm 5.1(b)). Para p = 2, (E) es una función
de las sumas con un QUIEBRE: mientras la variable 1 está inactiva (|A| ≤ μ'), c_2 = Bc es lineal y
creciente en la suma de pesos; en cuanto la variable 1 se activa, absorbe la correlación (Q/P grande
relativo a la pendiente) y c_2 cae por debajo de μ'. Con datos enteros, el quiebre crea una VENTANA de
ancho < 1: la variable 2 entra sii una suma de subconjunto cae exactamente en t. Esto es la idea del
encargo ("competencia"), verificada abajo con las cuentas exactas.

## 1. Construcción (Subset Sum → Selection-Witness, p = 2)

Fuente: enteros positivos b_1..b_m, objetivo t, con 1 ≤ t ≤ B−1, B := Σ b_i (los casos t ≤ 0 o t ≥ B
se deciden trivialmente y se mapean a instancias fijas SÍ/NO).

Parámetros (todos racionales de tamaño polinómico):
  s0 = 1/2,  η = 1/(2B),  κ = 1 + η,  u = m + 1 (así u^2 > m),
  regla C: μ = t + 1/2,                 y_i = b_i              (ítems)
  regla P: λ = t + 1/2, μ = λ(m+1),     y_i = b_i + λ          (ítems; desplazamiento que cancela |K|)
  ε = η/(4μ),  ρ = 1 − ε.
Filas (n = m + 1, p = 2):
  ítem i ∈ [m]:  (x_{i1}, x_{i2}; y_i) = (1, ρ; y_i)
  gadget g:      (u, κu; s0/u)
Variable objetivo: j = 2 (inactiva en D).

Sumas sobre K ∋ g con conjunto de ítems I, N = |I|, β := Σ_{i∈I} b_i, W := Σ_{i∈I} y_i:
  P = u^2 + N,  Q = κu^2 + ρN,  A = s0 + W,  Bc = κ s0 + ρW.
Definimos Δ := A − μ'.
  Regla C: Δ = 1/2 + β − t − 1/2 = β − t.
  Regla P: μ' = μ(N+1)/(m+1) = λ(N+1), W = β + λN ⇒ Δ = 1/2 + β − λ = β − t.
En ambos casos Δ = β − t ∈ ℤ (aquí está el papel del desplazamiento λ en la regla P).

Identidades:
  Bc − μ' = (κ−ρ)s0 + ρΔ − (1−ρ)μ'.
  Q/P − ρ = (κ−ρ) u^2/(u^2+N).
A > 0 siempre (y_i > 0), luego β_1* = (A − μ')_+/P = Δ_+/P.

Caso Δ ≤ 0 (variable 1 inactiva en el restringido): c_2 = Bc > 0.
  Δ = 0:  Bc − μ' = (η+ε)/2 − εμ' ≥ (η+ε)/2 − η/4 > 0  ⇒ ENTRA.
  Δ ≤ −1: Bc − μ' ≤ (κ−ρ)/2 − ρ < 0 (κ−ρ = η+ε ≤ 2η ≤ 1, ρ > 1/2) ⇒ no entra; además Bc > 0 > −μ'.
Caso Δ ≥ 1 (variable 1 activa, signo +): c_2 = Bc − QΔ/P,
  c_2 − μ' = (κ−ρ)[1/2 − Δ u^2/(u^2+N)] − (1−ρ)μ' < 0   pues Δu^2/(u^2+N) ≥ u^2/(u^2+N) > 1/2 (u^2 > N);
  c_2 + μ' > (1+ρ)μ' − (κ−ρ)Δ ≥ (1+ρ)μ' − (B−t)/B > 0   pues κ−ρ ≤ 1/B, Δ ≤ B − t, μ' ≥ 3/2.
  ⇒ no entra.
Conclusión para K ∋ g, N ≥ 1: la variable 2 entra ⇔ Δ = 0 ⇔ Σ_{i∈I} b_i = t. El minimizador es único
porque las filas (1,ρ) y (u,κu) son independientes (κ ≠ ρ) ⇒ X_K de rango 2 ⇒ objetivo estrictamente convexo.

K ∌ g (solo ítems, N ≥ 1): x_2 = ρ x_1 en K. Para un ajuste fijo f = β_1 + ρβ_2,
|β_1| + |β_2| = |f − ρβ_2| + |β_2| ≥ |f| + (1−ρ)|β_2|, mínimo único en β_2 = 0; el ajuste óptimo f es
único (convexidad estricta en f). ⇒ minimizador único con β_2 = 0: no entra.
K = {g} (N = 0): una fila (u, κu), κ > 1 ⇒ la representación ℓ1 más barata usa solo x_2; la correlación
es κ s0 = κ/2 < 3/2 ≤ μ' ⇒ minimizador único β = 0: no entra.
D completo (N = m, β = B ≥ t+1): Δ ≥ 1, S(D) = {1} con signo +, variable 2 inactiva estrictamente
(usa u^2 > m), único (rango 2).

⇒ Existe testigo de entrada para j = 2  ⇔  la instancia de Subset Sum es SÍ.
   (Si I con Σ b = t: R = [m]∖I es propio y no vacío porque 1 ≤ t ≤ B−1 ⇒ ∅ ≠ I ≠ [m].)
Además: TODO subconjunto D∖R (R propio) tiene minimizador único. Tamaños: u, 1/η, 1/ε, μ polinómicos en
el tamaño binario de la entrada (ε^{-1} = 8Bμ).

p fijo ≥ 3: añadir p−2 columnas nulas (β_j = 0 forzado, c_j = 0 < μ'), unicidad preservada.

Pertenencia a NP (p arbitrario): certificado (R, β̂ en D∖R). β̂ racional de tamaño polinómico
(β̂_S = (X_S^T X_S)^{-1}(X_S^T y − μ' s), Lema 2.4). Verificación: KKT exacto en D∖R; unicidad: el conjunto
de minimizadores es M = {β : X_K β = X_K β̂, ||β||_1 ≤ ||β̂||_1} (todos los minimizadores comparten ajuste y
norma ℓ1), y β̂ es único sii max/min β_k sobre M valen β̂_k para todo k: 2p programas lineales. Para p fijo
basta enumerar los 3^p soportes con signo.

Estado: DEMOSTRADO (pendiente verificación exhaustiva exacta, §3).
