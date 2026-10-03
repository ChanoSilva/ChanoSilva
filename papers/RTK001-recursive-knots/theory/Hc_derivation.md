# Derivación de (H_c) para la familia RTK001 — caso p = 2

Estado: documento de trabajo (2026-10-02, completado 2026-10-03). Cada paso está o bien justificado o bien
marcado **[BRECHA]**. Las desigualdades intermedias se verifican numéricamente en
`check_Hc.py` (salida en `check_Hc_output.txt`).

## 0. Notación y hipótesis

- `K = K_{d-1}`: curva cerrada regular `C^2` (en la familia, `C^∞`), parametrizada con
  periodo `2π`, velocidad `v(t)=|K'(t)| ∈ [v_min, v_max]`, tangente unitaria `T`,
  curvatura `κ ≤ κ_max ≤ 1/τ`, grosor `τ = thick(K) > 0`.
- Marco paralelo (Bishop, **sin** cerrar) `(T, N_0, B_0)`: `N_0' = -κ_1 v T`,
  `B_0' = -κ_2 v T`, `κ_1²+κ_2² = κ²`. Marco cerrado `N = cos ω N_0 + sin ω B_0`,
  `ω = -α t/2π`, `|α| ≤ π`.
- `K_d(t) = K(t) + r U(t)`, `U = cos θ N + sin θ B = cos ψ N_0 + sin ψ B_0`, con
  `θ = (q/p)t + φ` y por tanto `ψ = θ + ω = m t + φ`, **tasa angular efectiva**
  `m := q/p - α/2π ∈ [q/p - 1/2, q/p + 1/2]` (constante). Esto absorbe el término
  `ω'` de (frame) exactamente: en el marco paralelo la hebra gira a tasa constante `m`.
- `f := r/τ ≤ 1/2`. **Parámetro de paso** `h := v/m` (avance en longitud de arco de la
  base por radián de giro de la hebra; coincide con `|K'|p/q` del manuscrito cuando
  `α = 0`). `h_min = v_min/m`, `h_max = v_max/m`; `η_min = h_min/r`, `η_max = h_max/r`.
- Dos puntos `X_i = K(t_i) + r U_i`, `U_i = U(t_i)`. Diferencia de parámetro en `K_d`:
  `Δ = t_2 - t_1 ∈ (-πp, πp]`; diferencia de base `s = Δ mod 2π ∈ (-π, π]`, índice de
  hebra `k = (Δ-s)/2π ∈ {0,…,p-1}`. Entonces el ángulo relativo de `U_2` respecto de `U_1`,
  medido en el marco paralelo transportado desde `t_1` a lo largo del arco corto, es
  `Δψ = m s + 2π q k/p (mod 2π)`. (Comprobación: `N_0(t+2π) = R_α N_0(t)`, así que el ángulo de
  `U_2` en el marco `N_0(t_1+s)` es `ψ_2 + kα = ψ_1 + m s + 2πk(q/p - α/2π) + kα`; los términos en `α`
  se cancelan. En el marco cerrado en `t_1` el ángulo de `U_2` es `θ_2 - α s/2π`, que es lo que usa `check_Hc.py`.)
  Para `p = 2`: `k = 0` (misma hebra) o `k = 1` (hebra antipodal, desfase `π`).
- `σ := ∫_{t_1}^{t_2} v dt` longitud de arco de base entre los puntos base (por el arco
  corto), `δ := σ/τ`. `u := m|s|` giro angular de la hebra entre los dos puntos.
  Relación: `σ ∈ [v_min|s|, v_max|s|]`, luego `u ∈ [δ τ/h_max, δ τ/h_min] = [δ/(f η_max), δ/(f η_min)]`.

Fórmula LSDR/Gonzalez–Maddocks usada: `thick(K_d) = min(minRad(K_d), dcsd(K_d)/2)`.
Objetivo: `dcsd(K_d) ≥ 2ρ` y `minRad(K_d) ≥ ρ` con `ρ = min(τ-r, c r sin(π/p))`.

## 1. Lema A (cuerda vs. arco en curvas gruesas) — demostrado

**Lema A.** Sea `K` cerrada `C^{1,1}` con `thick(K) ≥ τ`, parametrizada por arco. Sean
`x = K(0)`, `g(σ) = |K(σ) - x|`. Entonces (i) todo mínimo local de `g` en `(0, L)`
vale `≥ 2τ`; (ii) `{σ : g(σ) < 2τ}` es la unión de un intervalo inicial `[0,a)` y uno
final `(L-b, L)`, en los que `g` es monótona, con `a, b ≤ πτ`; (iii) en `[0,a)`:
`g(σ) ≥ 2τ sin(σ/2τ)`.

*Prueba.* (i) Si `y = K(σ_0)` es mínimo local de `g` con `σ_0 ∈ (0,L)`, entonces
`(y-x) ⊥ T(y)` y el radio punto-tangente de Gonzalez–Maddocks es
`ρ_pt(y,x) = |x-y|/(2 sin ∠(T_y, x-y)) = |x-y|/2`; como `thick(K) = inf ρ_pt ≥ τ`,
`|x-y| ≥ 2τ`. (ii) Si una componente de `{g < 2τ}` fuera un intervalo interior
`(c,e)` con `0<c<e<L`, `g(c)=g(e)=2τ` y `g<2τ` dentro, habría un mínimo interior `<2τ`,
contradiciendo (i); lo mismo excluye un mínimo local dentro de `[0,a)`, de modo que
`g` es monótona creciente ahí. (iii) En `[0,a)`, `g` es Lipschitz, `g' = cos β ≥ 0`
c.t.p., con `β = ∠(T(σ), K(σ)-x)`; la condición `ρ_pt(K(σ), x) ≥ τ` da
`sin β ≤ g/(2τ)`, luego `g' ≥ √(1 - g²/4τ²)`. Con `Φ = arcsin(g/2τ)` (bien definida
porque `g < 2τ`), `Φ' ≥ 1/(2τ)`, `Φ(0)=0`, así `g(σ) ≥ 2τ sin(σ/2τ)`; en particular
`g` alcanza `2τ` antes de `σ = πτ`, por lo que `a ≤ πτ`. ∎

(Resultado clásico: cf. Gonzalez–Maddocks–Schuricht–von der Mosel 2002, Lema 2, y
Schuricht–von der Mosel 2003; se incluye la prueba para que el lema sea autocontenido.
La referencia exacta debe comprobarla quien integre.)

**Consecuencia (clasificación de pares).** Para dos puntos base `x ≠ y` de `K`:
o bien `|x-y| ≥ 2τ`, o bien están unidos por un arco de longitud `σ = τδ < πτ` con
`|x-y| ≥ 2τ sin(δ/2)`. En el segundo caso, si `δ ≥ δ_0(c) := 2 arcsin(f(1+c))`
(con `f(1+c) ≤ 1`), entonces `|x-y| ≥ 2r(1+c)` y
`|X_2-X_1| ≥ |x-y| - 2r ≥ 2cr`. Esto extiende el caso (b) de la Proposición: **el
único caso abierto es `0 < δ < δ_0(c)`** ("caso local").

## 2. Estimaciones elementales en el caso local (todas demostradas)

Sea `x = K(a)`, `y = K(a+s)`, `s>0`, `ℓ = |y-x|`, `e = (y-x)/ℓ`, `T̄ = (1/σ)∫ v T dt`
(tangente media), de modo que `e = T̄/|T̄|`, `|T̄| = ℓ/σ`. Usamos
`|T(t)-T(t')| ≤ |σ(t)-σ(t')|/τ` (porque `|dT/dσ| = κ ≤ 1/τ`).

- (E1) `ℓ ≥ ℓ_0(δ) := 2τ sin(δ/2)` (Lema A), `ℓ ≤ σ = τδ`.
- (E2) `|T̄ - T(a)| ≤ (1/σ)∫_0^σ u/τ du = δ/2`; igualmente `|T̄ - T(a+s)| ≤ δ/2`.
- (E3) Para `w ⊥ T(a)`: `|w·e| ≤ |w| β(δ)`, `β(δ) := δ²/(4 sin(δ/2))`.
  *Prueba:* `w·e = w·Π_a e`, `Π_a e = Π_a(T̄ - T(a))/|T̄|`, `|Π_a e| ≤ (δ/2)(σ/ℓ) ≤ (δ/2)·δ/(2 sin(δ/2))`.
- (E4) Para `w ⊥ T(a)` unitario: `|w·(y-x)| ≤ E(δ)`, con
  `E(δ) := τ(1-cos δ)` si `δ ≤ π/2`, `E(δ) := τ(1 + δ - π/2)` si `π/2 < δ ≤ π`.
  *Prueba:* `w·(y-x) = ∫ v w·Π_a T(t) dt`, `|Π_a T(t)| = sin ∠(T(t),T(a)) ≤ sin(min(σ(t)/τ, π/2))`.
  Lo mismo con `w ⊥ T(a+s)` (integrando desde el otro extremo).
- (E5) Defecto de transporte paralelo. Sea `Ũ_2 := cos ψ_2 N_0(a) + sin ψ_2 B_0(a)`
  (mismo ángulo que `U_2`, marco en `a`). Entonces
  `U_2 - Ũ_2 = -∫_a^{a+s} κ_⊥(t) v T(t) dt`, `κ_⊥ = κ_1 cos ψ_2 + κ_2 sin ψ_2`, `|κ_⊥| ≤ κ ≤ 1/τ`.
  Por tanto: (E5a) `|U_2 - Ũ_2| ≤ δ`; (E5b) `|(U_2-Ũ_2)·T(a)| ≤ δ`;
  (E5c) **componente ortogonal a la cuerda**: `|(U_2-Ũ_2)_{⊥e}| ≤ δ²/3`.
  *Prueba de (E5c):* la distancia de `T(t)` a la recta `ℝe` es `≤ |T(t)-T̄|
  ≤ (1/σ)∫_0^σ |u-u_t|/τ du = (u_t²+(σ-u_t)²)/(2στ)`; integrando contra `κ v ≤ v/τ`:
  `≤ (1/τ)∫_0^σ (u²+(σ-u)²)/(2στ) du = σ²/(3τ²)`.
- (E6) `Ũ_2 - U_1` está en el plano normal en `a` y `|Ũ_2 - U_1| = 2|sin((ψ_2-ψ_1)/2)|`.

## 3. Descomposición a lo largo de la cuerda de base

`X_2 - X_1 = (y-x) + r(U_2 - U_1)`. Descomponemos en la dirección `e` y su ortogonal:
`|X_2-X_1|² = A² + |Q|²`, `A = (X_2-X_1)·e`, `Q = (X_2-X_1) - A e = r (U_2-U_1)_{⊥e}`.

**(3.1) Componente a lo largo de la cuerda.**
`A = ℓ + r(U_2·e - U_1·e) = ℓ + (r/ℓ)[U_2·(y-x) - U_1·(y-x)] ≥ ℓ - 2rE(δ)/ℓ` por (E4)
(aplicado a `U_1 ⊥ T(a)` y a `U_2 ⊥ T(a+s)`). La función `ℓ ↦ ℓ - 2rE/ℓ` es creciente,
y `ℓ ≥ ℓ_0(δ)`, luego

    A ≥ Λ(δ) := ℓ_0(δ) - 2 r E(δ)/ℓ_0(δ).

Para la circunferencia de radio `τ` y los puntos en el ecuador interior esto es
exacto: `Λ = 2τ sin(δ/2) - 2r sin(δ/2) = 2(τ-r) sin(δ/2)` (para `δ ≤ π/2`).

**(3.2) Componente ortogonal a la cuerda.**
`(U_2-U_1)_{⊥e} = (Ũ_2-U_1)_{⊥e} + (U_2-Ũ_2)_{⊥e}`. Con `w = Ũ_2-U_1 ⊥ T(a)`,
`|w_{⊥e}|² = |w|² - (w·e)² ≥ |w|²(1-β(δ)²)` por (E3). Con (E5c):

    |Q| ≥ r · P(δ, Δψ) ,  P := [ 2|sin(Δψ/2)| √(max(0, 1-β(δ)²)) - δ²/3 ]_+ ,

donde `Δψ = ψ_2 - ψ_1 = m s + π k` (p = 2).

**(3.3) Cota local.** Para todo par con separación de base `δ ∈ (0, π)`:

    |X_2 - X_1| ≥ D_k(δ, u) := √( Λ(δ)_+² + r² P(δ, u + πk)² ),   u = m s ∈ [δ/(fη_max), δ/(fη_min)].

Y simultáneamente la cota de cuerda `|X_2-X_1| ≥ ℓ_0(δ) - 2r`.

## 4. Caso antipodal (k = 1), p = 2 — demostrado (incondicional)

Para `k = 1`, `|sin(Δψ/2)| = |cos(u/2)|` con `u = m|s|`. Escribimos `Θ := h/τ = v/(mτ) = fη`
("paso sobre grosor de la base"), `Θ_min = h_min/τ`, `Θ_max = h_max/τ`; la relación `σ ∈ [v_min|s|, v_max|s|]`
da `u ∈ [δ/Θ_max, δ/Θ_min]`.

**4.0 Constante bidimensional.**

    c_1(f, Θ_min, Θ_max) := (1/2r) · inf_{δ∈(0,π), u∈[δ/Θ_max, δ/Θ_min]} max{ D_1(δ,u), ℓ_0(δ) - 2r },

con `D_1` de (3.3) (`k = 1`). Todas las cantidades son homogéneas de grado 1 en longitud, así que
`c_1` depende solo de `(f, Θ_min, Θ_max)`. Por §1–§3, **todo par de puntos de `K_d` en hebras
distintas está a distancia `≥ min(2(τ-r), 2 c_1 r)`** (los pares con `δ ≥ π` o cuerda de base `≥ 2τ`
dan `≥ 2(τ-r)` por la Proposición (b) y la clasificación de §1; los demás tienen `δ < π`,
`ℓ ≥ ℓ_0(δ)` y satisfacen (3.3)). El ínfimo es de una función elemental explícita sobre un compacto
(cerrando en `δ = π`); `check_Hc.py` lo evalúa en malla (`[c1]`).

**4.1 Reducción a una variable (η_max no interviene).** En la cota (3.3) con `k = 1` la única
dependencia en `u` es a través de `|cos(u/2)|`, que es decreciente en `u ∈ [0, π]`. Como `u ≤ δ/Θ_min`,

    |cos(u/2)| ≥ cos(δ/(2Θ_min))  si  δ ≤ πΘ_min,     y  ≥ 0 en otro caso.

Definimos `P_1(δ) := [2 cos(δ/2Θ_min) √(1-β(δ)²) - δ²/3]_+` (`:= 0` si `δ > πΘ_min`) y

    c_1^{1D}(f, Θ_min) := (1/2r) · inf_{δ∈(0,π)} max{ √(Λ(δ)_+² + r² P_1(δ)²),  ℓ_0(δ) - 2r }.

Entonces `c_1 ≥ c_1^{1D}` y **todo par antipodal está a distancia `≥ min(2(τ-r), 2 c_1^{1D} r)`**.
Numéricamente `c_1^{1D} = c_1` en todos los niveles de la familia (el mínimo 2-D se alcanza en
`u = δ/Θ_min`): no se pierde nada. `c_1^{1D}` es un ínfimo de una función explícita de **una**
variable en `(0, π]`; `check_Hc.py` lo evalúa en una malla de 20 000 puntos y resta `2·Lip·paso`
(Lipschitz estimada por diferencias finitas) — valor "certificado" en `[c1-1D]` y en la tabla
`c_1^(1D)(f, Θ)`.

**Monotonía.** `ℓ_0/r - 2 = (2/f) sin(δ/2) - 2` y `Λ/r` (para `δ ≤ π/2`: `2(1/f - 1) sin(δ/2)`;
para `δ > π/2`: `(2/f) sin(δ/2) - (1 + δ - π/2)/sin(δ/2)`) son decrecientes en `f`; `P_1` no depende de `f`
y es no decreciente en `Θ_min`. Por tanto `c_1^{1D}(f, Θ_min)` es **no creciente en `f` y no decreciente
en `Θ_min`**, y para `f ≤ 1/2`, `Θ_min ≥ 2/3`:

    c_1^{1D}(f, Θ_min) ≥ c_1^{1D}(1/2, 2/3) = 0.6117  (certificado; valor en malla 0.6119).

**4.2 Régimen cerrado para `c = 1/2`, `f ≤ 1/2`.** (i) `δ ∈ [π/3, π]`: `Λ(δ) ≥ r`. Para
`δ ∈ [π/3, π/2]`, `Λ = 2(τ-r) sin(δ/2) ≥ τ - r ≥ r`. Para `δ ∈ [π/2, π]`, `Λ/r ≥ 4 sin(δ/2) - (1+δ-π/2)/sin(δ/2) =: φ(δ)`
(peor caso `f = 1/2`), con `φ(π/2) = √2`, `φ(π) = 4 - (1+π/2) = 1.43` y `φ ≥ 1.41` en todo `[π/2, π]`
(comprobado en malla). En total, `min_{[π/3,π]} Λ/r = 1.0000` para `f = 1/2`, alcanzado en `δ = π/3`
(`Λ(π/3) = τ - r = r`); `1.857` para `f = 0.35`, `3.000` para `f = 0.25` (`check_Hc.py`). (ii) `δ < π/3`: `β(δ) ≤ 0.5236 δ` (máximo de
`β/δ = (δ/2)/sin(δ/2)·(1/2)` en `δ = π/3`), `√(1-β²) ≥ 1 - 0.15 δ²`, `Λ ≥ 0.954 (τ-r) δ`, y la cota es
`max{(2/f) sin(δ/2) - 2, √((0.954(1/f-1)δ)² + [2cos(δ/2Θ_min)(1-0.15δ²) - δ²/3]_+²)} ≥ 1` — una
desigualdad explícita en una variable con parámetros `(f, Θ_min)`; para `f = 1/2`, `Θ_min = 2/3`
se cumple con margen (el ínfimo real de la función completa es `2·0.6117 = 1.22`).

**4.3 Cota a priori de `Θ_min` en la familia por defecto `(2,3)`, `f ≤ 1/2`.** (a) `thick(K_d) ≤ r_d`:
el par antipodal del mismo disco normal (`t`, `t+2π`) es doblemente crítico (`X_2 - X_1 = -2rU_1 ⊥ K_d'`
en ambos extremos por (deriv)) a distancia `2r`, luego `dcsd ≤ 2r`. Por tanto
`τ_{d-1} ≤ r_{d-1} = f τ_{d-2} ≤ 2^{-(d-1)}`. (b) Velocidad: tras reparametrizar a periodo `2π`
(`t ↦ t/p`), `v_d ≥ p (1-f) v_{d-1,min} ≥ v_{d-1,min}` para `p = 2`, `f ≤ 1/2`; `v_0 = 1`, así que
`v_min ≥ 1` a toda profundidad. (c) `m = q/p - α/2π ≤ 3/2 + 1/2 = 2`. Luego para `d ≥ 2`:
`Θ_min = v_min/(m τ_{d-1}) ≥ 2^{d-1}/2 ≥ 1`; para `d = 1`: `α = 0`, `m = 3/2`, `v = 1`, `τ_0 = 1`,
`Θ = 2/3`. **En la familia `(2,3)` con `f ≤ 1/2`, `Θ_min ≥ 2/3` a toda profundidad**, y por 4.1:

    todo par de puntos de K_d en hebras distintas dista ≥ min(2(τ-r), 1.223 r)   (c_1 = 0.6117 > 1/2).

Para `(2,5)`, `f = 1/2`, `d = 1`: `Θ = 2/5`, `c_1^{1D} = 0.4882 < 1/2` (medido `dcsd/2r = 0.5646`): la
cota **no** alcanza `c = 1/2` ahí (sí `c = 0.488`); para `d ≥ 2` de `(2,5)`, `c_1 ≥ 0.70`.

**4.4 Por qué `c_1 < 1` y su límite.** En el tubo recto la cota se reduce a `min_u √(h²u² + 4r²cos²(u/2)) = 2r`
si `h ≥ r`. En el tubo curvado el paso efectivo interior es `h(1-f)` (contenido en `Λ`, exacto para la
circunferencia) y los términos `β(δ)`, `δ²/3` de (E3), (E5c) son los que bajan `c_1` a `≈ 0.61–0.71`
para `f = 1/2` (el mínimo se alcanza en `δ ≈ 1.2–1.5`, donde `δ²/3 ≈ 0.5–0.75` anula `P`). Con `Θ_min → ∞`,
`c_1^{1D}(1/2, ·) → 0.7070` (función solo de `f`). Afinar (E5c) con control de `κ'` (nula para la
circunferencia) permitiría acercarse a `c = 0.83` (valor medido en `d = 1`), pero no se hace aquí.

## 5. Curvatura de K_d — identidad exacta y cota cerrada (demostradas); dependencia en K''' (hallazgo)

**5.1 Identidad.** Con `x := rκ_⊥ ∈ [-f, f]`, `c_T := v(1-x)`, `c_W := rm`, `A := v²(1-x)²`, `Bm := r²m²`
(`|K_d'|² = A + Bm`), y `κ_1 N_0 + κ_2 B_0 = κ_⊥ U + κ_W W`, la fórmula de §5 (versión anterior) se reescribe

    K_d'  = c_T T + c_W W,
    K_d'' = a T + b_U U + b_W W,   a = v'(1-x) - r v (κ_1' cos ψ + κ_2' sin ψ) - 2 r v m κ_W,
                                  b_U = v²(1-x) κ_⊥ - r m²,   b_W = v²(1-x) κ_W,

y como `T × U = W`, `W × T = U`, `U × W = T`:

    |K_d' × K_d''|² = b_U² |K_d'|² + (c_W a - c_T b_W)².                              (5.1)

(Verificada en `check_Hc.py` `[K2]` frente al producto vectorial directo: error relativo `10^{-15}`.)

**5.2 Cota cerrada.** Sea `a_0 := v'(1-x) - r v(κ_1' cos ψ + κ_2' sin ψ)` (la parte de `a` que depende de
`K'''`), de modo que `c_W a - c_T b_W = r m a_0 - κ_W v (A + 2Bm)`. Por Minkowski,

    κ_d = √(5.1)/|K_d'|³ ≤ √(β_1²|K_d'|² + κ_W² v² (A+2Bm)²)/|K_d'|³ + √(r²m⁴|K_d'|² + r²m²a_0²)/|K_d'|³,

con `β_1 := v²(1-x)κ_⊥`. Primer sumando: `β_1²(A+Bm) + κ_W² v²(A+2Bm)² = v²[κ_⊥² A(A+Bm) + κ_W²(A+2Bm)²]
≤ v² κ² (A+2Bm)²` (porque `A(A+Bm) ≤ (A+2Bm)²`), luego `≤ v κ (A+2Bm)/(A+Bm)^{3/2}`; la función
`A ↦ (A+2B)/(A+B)^{3/2}` es decreciente, y `A ≥ v²(1-f)²`, así que con `ζ := v(1-f)/(rm)` (paso efectivo
interior en unidades de `r`; `ζ = (1-f)η`):

    primer sumando ≤ (κ/(1-f)) · g(ζ),   g(ζ) := ζ(ζ²+2)/(ζ²+1)^{3/2},   sup g = g(√2) = 1.0887,  g → 1 (ζ→∞).

Segundo sumando `≤ r m²/|K_d'|² + r m |a_0|/|K_d'|³ ≤ 1/(r(1+ζ²)) + r m |a_0|/(v²(1-f)² + r²m²)^{3/2}`.
Con `κ ≤ κ_max ≤ 1/τ`, `τ(1-f) = τ - r`, y `G(ζ_min) := sup_{ζ ≥ ζ_min} g = 1.0887` si `ζ_min ≤ √2`,
`= g(ζ_min)` si no:

    κ_d ≤ κ̄_d := G(ζ_min)/(τ - r) + 1/(r(1+ζ_min²)) + Γ_3,
    Γ_3 := r m [ V_1 (1+f) + r v_max K_1 ] / ( v_min²(1-f)² + r²m² )^{3/2},                 (5.2)
    V_1 := sup|v'|,  K_1 := sup √(κ_1'² + κ_2'²) (marco paralelo; ≤ sup √(κ_1^c'²+κ_2^c'²) + |ω'| κ_max en el cerrado).

Interpretación: `1/(τ-r)` es la curvatura de la hebra interior sobre el tubo curvado (exacta en el
límite de paso grande), `1/(r(1+ζ²))` la curvatura de la hélice de paso `h(1-f)`, y `Γ_3` el único
término que ve `K'''`, suprimido por el factor `rm/|K_d'| ≈ 1/η`. **Consecuencia:**
`minRad(K_d) ≥ 1/κ̄_d`, y `1/κ̄_d ≥ ρ_d = min(τ-r, r/2)` (es decir `c_κ := 1/(rκ̄_d) ≥ 1/2`) si y solo si
`f·G/(1-f) + 1/(1+ζ_min²) + r Γ_3 ≤ 2` (para `f ≤ 1/2`, donde `ρ_d = r/2`). Sin el término `Γ_3`
(p.ej. base circular) basta `ζ_min ≥ 0.32` para `f = 1/2`; para `f ≤ 0.35`, cualquier `ζ_min ≥ 0`.

**5.3 Hallazgo: (H_c) necesita una hipótesis sobre K'''.** `Γ_3` no está controlado por `thick(K)`
ni por `κ_max`. Si `K` es `C^{1,1}` con `κ` saltando de `0` a `1/τ` (segmento seguido de arco de radio
`τ`; `thick(K) = τ`), por (deriv) la dirección de `K_d'` salta de `vT + rmW` a `v(1-f)T + rmW` en la hebra
interior: `K_d` tiene una esquina y `thick(K_d) = 0`. Suavizando el salto en una longitud `ε`,
`thick(K) → τ` y `κ_d ~ r v κ'/|K_d'|² ~ r/(τ ε |K_d'|) → ∞`. Luego **no existe `c > 0` dependiente solo de
`(p, q, f)` tal que (H_c) valga para toda base `K` con `thick(K) = τ`, ni siquiera suave**. La hipótesis
(H_c) del manuscrito (c dependiente solo de `(p,q,f)`) debe leerse para la familia concreta, y la
uniformidad en `d` de la constante requiere controlar `r_d Γ_3^{(d)}` en `d`, lo cual no se hace aquí
(véase §7). Hipótesis explícita usada: **(H_3)**: `sup|v'| ≤ V_1`, `sup|κ'| ≤ K_1` para `K = K_{d-1}`.

## 6. Misma hebra (k = 0) — demostrado condicionalmente a (5.2), constante débil

Un par doblemente crítico `X_1, X_2` de `K_d` cumple `(X_2-X_1)·T_d(X_1) = ∫_0^{σ_d} T_d·T_d(X_1) dσ = 0`,
y con `κ_d ≤ κ̄_d`, `T_d(σ)·T_d(0) ≥ cos(κ̄_d σ)`, así que `∫ ≥ sin(κ̄_d σ_d)/κ̄_d > 0` si `σ_d < π/κ̄_d`.
Luego `σ_d ≥ π/κ̄_d`, y como `|K_d'| ≤ V_d := v_max(1+f) + rm`, la separación de parámetro de base es
`|s| ≥ s_0 := π/(κ̄_d V_d)`, `u ≥ m s_0`. Para `k = 0`, `Δψ = u`, y

    c_0 := (1/2r) inf { max(D_0(δ,u), ℓ_0(δ) - 2r) : δ ∈ (0,π), u ∈ [δ/Θ_max, δ/Θ_min], u ≥ m s_0 }.

**Todo par doblemente crítico en la misma hebra dista `≥ min(2(τ-r), 2 c_0 r)`.** Aquí sí interviene
`Θ_max` (para `δ` dado, `u` pequeño es lo peor). Valores (`[c0]`): `c_0 ≥ 0.65` para `f ≤ 0.35`
(todas las profundidades), `c_0 ≥ 1.33` para `f = 0.25`, pero `c_0 = 0.32, 0.13, 0.16` para `f = 1/2`,
`d = 1, 2, 3`. **Limitación estructural:** `c_0 ≈ (π/2)(1-f)/f · (v_min/V_d)/(τκ̄_d)`, y como el primer término
de (5.2) ya da `τκ̄_d ≥ τ/(τ-r) = 2` para `f = 1/2`, esta vía **no puede** dar `c_0 ≥ 1/2` en `f = 1/2`
(con el `κ_d,max` medido en vez de `κ̄_d` sí saldría `c_0 ≈ 0.7`, pero eso no es una demostración).
Los términos de orden `s²` del par (que deciden si es doblemente crítico) involucran `K_d''`, de modo que
un argumento sin curvatura no es posible aquí.

## 7. Enunciado demostrado, constantes y brechas

**Teorema (p = 2).** Sea `K` cerrada `C^∞` regular con `thick(K) = τ`, `κ ≤ 1/τ`, parametrizada con
periodo `2π` y velocidad `v ∈ [v_min, v_max]`; `K_d` dado por (Kd) con `p = 2`, `q` impar, `r = fτ`,
`f ≤ 1/2`, `m = q/2 - α/2π`, `h_min = v_min/m`, `Θ_min = h_min/τ`, `ζ_min = (1-f)h_min/r`.

(A) [incondicional] Todo par de puntos de `K_d` en hebras distintas dista
`≥ min(2(τ-r), 2 c_1^{1D}(f, Θ_min) r)`, con `c_1^{1D}` definido en 4.1. Si `Θ_min ≥ 2/3`,
`c_1^{1D} ≥ 0.6117 > 1/2`. En la familia `(2,3)` con `f ≤ 1/2` se tiene `Θ_min ≥ 2/3` a toda profundidad (4.3).

(B) [bajo (H_3)] `minRad(K_d) ≥ 1/κ̄_d` con `κ̄_d` de (5.2).

(C) [bajo (H_3)] Todo par doblemente crítico en la misma hebra dista `≥ min(2(τ-r), 2 c_0 r)`, `c_0` de §6.

(D) Por LSDR/GM, `thick(K_d) = min(minRad, dcsd/2) ≥ min(τ - r, c r)` con
`c = min(c_1^{1D}, c_0, 1/(rκ̄_d))`.

**Valores en la familia (polígonos de `recursive_knots.py`, datos (H_3) medidos en el polígono):**
`(2,3)`: `f = 0.25`: `c = 1.00, 1.00, 1.00` (`d = 1,2,3`); `f = 0.35`: `c = 0.65, 0.66, 0.67`; `f = 0.5`:
`c = 0.32, 0.13, 0.16` (limitado por `c_0`; `c_1 = 0.61, 0.70, 0.71`; `c_κ = 0.56, 0.48, 0.85`).
`(2,5)`, `f = 0.5`: `c = 0.37, 0.26, 0.23` (`c_1 = 0.49, 0.70, 0.71`).

**Lo que queda abierto (exacto):**
1. `c = 1/2` para `f = 1/2` en el caso misma hebra (k = 0): la exclusión `σ_d ≥ π/κ̄_d` con la cota a priori
   (5.2) es demasiado débil (§6). Hace falta o una cota de `κ_d` más fina que `1/(τ-r)` lejos del lado
   interior (p.ej. evaluar el supremo sobre el ángulo `ψ` de la expresión exacta (5.1) en vez de usar
   `κ_⊥² + κ_W² = κ²`), o un argumento de criticidad doble que use la curvatura local y no la global.
2. El término `Γ_3` de (5.2) requiere (H_3) (`sup|v'|`, `sup|κ'|` de `K_{d-1}`), que no se deduce de
   `thick(K_{d-1})`; la uniformidad en `d` de `r_d Γ_3^{(d)}` (y por tanto de `c`) está **abierta**. En los
   polígonos, `r Γ_3 = 0, 0.006, 0.0002` (`f = 0.25`), `0, 0.065, 0.003` (`f = 0.35`), `0, 0.82, 0.155` (`f = 0.5`).
3. `c_1 = 1/2` falla en `(2,5)`, `f = 1/2`, `d = 1` (`c_1 = 0.488`, medido `0.565`): afinar (E3)/(E5c).
4. `p ≥ 3`: no tratado (la reducción 4.1 usa `|sin(Δψ/2)| = |cos(u/2)|`, específica de `p = 2`).
5. Nada de lo anterior es una cota certificada para los **polígonos** (los ínfimos 1-D/2-D se evalúan en
   malla con control Lipschitz estimado numéricamente, no con aritmética de intervalos).

## 8. Comprobaciones numéricas (check_Hc.py → check_Hc_output.txt)

Por nivel (`d = 1..3`, cadenas `(2,3)` con `f = 0.25, 0.35, 0.5` a `N_0 = 256`, `(2,3)` `f = 0.5` a
`N_0 = 512`, `(2,5)` `f = 0.5`): `[A]` Lema A en la base (ninguna pareja con cuerda `< 2τ` tiene arco
`≥ πτ`; `cuerda/(2τ sin(σ/2τ)) ≥ 1`); `[E]` holguras de (E3), (E4), (E5c), (E6+E3) `≥ 0` salvo (E4) a
`-4·10^{-5}` (`-10^{-5}` al duplicar `M`: discretización); `[C]` `A ≥ Λ`, `|Q| ≥ rP` en todos los pares
locales; `[D]` `dist/cota ≥ 1.0001` para `k = 1` y `≥ 1.0012` para `k = 0` en todos los pares locales;
`[c1]`, `[c1-1D]` constantes antipodales (coinciden); `[K]` fórmula de `K_d''` vs diferencias finitas
(`10^{-3}`–`10^{-4}`); `[K2]` identidad (5.1) (`10^{-15}`); `[K3]` cota (5.2) `≥ κ_d,max` medido en todos los
niveles (holgura factor 1.9–18); `[c0]` constante misma hebra; `[RESULT]` `c` del nivel y
`min(τ-r, c r)` frente a `τ_d` medido (cociente `1.00`–`7.4`, siempre `≥ 1`). Tiempo total `≈ 40 s`.
