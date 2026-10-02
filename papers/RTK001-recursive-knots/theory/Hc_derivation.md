# Derivación de (H_c) para la familia RTK001 — caso p = 2

Estado: documento de trabajo (2026-10-02). Cada paso está o bien justificado o bien
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
  hebra `k = (Δ-s)/2π ∈ {0,…,p-1}`. Entonces `ψ_2 - ψ_1 = m s + 2π q k/p (mod 2π)`.
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

## 4. Caso antipodal (k = 1), p = 2 — demostrado

Para `k = 1`, `|sin(Δψ/2)| = |cos(u/2)|`. Definimos

    c_1(f, η_min, η_max) := (1/2r) · inf_{δ∈(0,π), u∈[δ/(fη_max), δ/(fη_min)]} max{ D_1(δ,u), ℓ_0(δ) - 2r }.

Todas las cantidades están en unidades de `r` (dividir por `r`: `τ = 1/f`), así que
`c_1` depende solo de `(f, η_min, η_max)`. Para `δ → 0`, `D_1 → 2r` (par antipodal en el
mismo disco: `c_1 ≤ 1`). La función es continua en el compacto (cerrando en `δ = π`),
el ínfimo se alcanza y se calcula numéricamente sobre una malla fina (ver §7 para los
valores en la familia). **Toda pareja de puntos de `K_d` en hebras distintas (p = 2) está
a distancia `≥ min(2(τ-r), 2 c_1 r)`.** Combinado con la Proposición (a) y la
clasificación del §1, esto cubre completamente el caso `k = 1`.

Comentario sobre la forma cerrada: en el tubo recto (`δ²`-términos nulos, `Λ` sustituida
por `h u`) la cota se reduce a `min_u √(h²u² + 4r² cos²(u/2))`, que es `2r` si `h ≥ r`
(el par antipodal es mínimo local exactamente cuando `h ≥ r`, como dice el manuscrito).
La curvatura de la base entra por dos vías: el paso efectivo `h(1-f)` en el lado interior
(contenido en `Λ`, que para la circunferencia es exacto) y el defecto de transporte
paralelo `δ²/3` (nulo para la circunferencia plana, pero no en general sin control de `κ'`).

## 5. Curvatura de K_d — derivada; cota condicional **[BRECHA parcial]**

Con `W := -sin ψ N_0 + cos ψ B_0` (unitario, `U' = m W - κ_⊥ v T`), `κ_W := -κ_1 sin ψ + κ_2 cos ψ`
(`κ_⊥² + κ_W² = κ²`), `T' = v(κ_1 N_0 + κ_2 B_0)`:

    K_d'  = v(1 - rκ_⊥) T + r m W                                   (deriv)
    K_d'' = [v(1-rκ_⊥)]' T + v²(1-rκ_⊥)(κ_1 N_0 + κ_2 B_0) - r m² U - r m κ_W v T

con `[v(1-rκ_⊥)]' = v'(1-rκ_⊥) - r v (κ_1' cos ψ + κ_2' sin ψ) - r v m κ_W`.
Curvatura: `κ_d = |K_d' × K_d''| / |K_d'|³`. Como `|K_d'|² = v²(1-rκ_⊥)² + r²m² ≥ v_min²(1-f)² + r²m²`,
y `|K_d' × K_d''| ≤ |K_d'| · |K_d''_{⊥K_d'}| ≤ |K_d'| |K_d''|`:

    κ_d ≤ |K_d''| / |K_d'|²  ≤  [ |v'|(1+f) + r v_max(|κ_1'|+|κ_2'|)_max + 2 r v_max m κ_max + v_max² (1+f) κ_max + r m² ] / ( v_min²(1-f)² + r²m² ).

(Para una cota ligeramente mejor se descarta la componente de `K_d''` paralela a `K_d'`;
no se hace aquí.) **Hallazgo:** `κ_d` depende de `v'` y de `(κ_1', κ_2')`, es decir de
`K'''`, que **no** está controlado por `thick(K)` ni por `κ_max`. Contraejemplo: si `K`
es `C^{1,1}` con un salto de `κ` de `0` a `1/τ` (segmento recto seguido de un arco de
radio `τ`, grosor `τ`), la hebra interior de `K_d` tiene velocidad `v T + r m W` antes
del salto y `v(1-f) T + r m W` después: la dirección de `K_d'` salta, `K_d` tiene una
esquina y `thick(K_d) = 0`. Por tanto **(H_c) es falsa para una base `K` general con
las solas hipótesis `thick(K) = τ`, `r ≤ τ/2`**; necesita una hipótesis sobre `K'''`.
Para la familia, `v'` y `κ'` de `K_{d-1}` están determinados por `K_{d-2}` hasta orden 4,
etc.: la recursión no se cierra con un número fijo de derivadas, y la uniformidad en `d`
de la constante queda **abierta**. Lo que sí se tiene: con la hipótesis explícita
`(H_3)`: `|v'| ≤ V_1`, `|κ_i'| ≤ Κ_1`, la cota anterior es explícita y se verifica
numéricamente (§7).

## 6. Misma hebra (k = 0) **[BRECHA parcial, condicional a §5]**

Pares doblemente críticos en la misma hebra. Si `κ_d ≤ κ̄_d` (§5), un par doblemente
crítico `X_1, X_2` satisface `(X_2-X_1)·T_d(X_1) = 0`; pero
`(X_2-X_1)·T_d(X_1) = ∫_0^{σ_d} T_d·T_d(X_1) dσ ≥ sin(κ̄_d σ_d)/κ̄_d > 0` si
`σ_d < π/κ̄_d` (`σ_d` = longitud de arco de `K_d` entre ellos). Luego
`σ_d ≥ π/κ̄_d`, y como `|K_d'| ≤ V_d := v_max(1+f) + r m`, la separación de base es
`|s| ≥ s_0 := π/(κ̄_d V_d)`, `u ≥ m s_0`, `δ ≥ v_min s_0/τ`. Entonces
`|X_2-X_1| ≥ max{ D_0(δ,u), ℓ_0(δ)-2r }` sobre la región `δ ≥ v_min s_0/τ`,
`u ∈ [δ/(fη_max), δ/(fη_min)]`, `u ≥ m s_0`. Se define `c_0` como el ínfimo
correspondiente dividido por `2r`. Esto es una demostración **condicional a una cota
de curvatura `κ̄_d`**, que a su vez requiere `(H_3)`. Sin `(H_3)` no hay cota.

## 7. Resultado y valores numéricos

Ver `check_Hc_output.txt` (generado por `check_Hc.py`). Resumen al final de este archivo.
