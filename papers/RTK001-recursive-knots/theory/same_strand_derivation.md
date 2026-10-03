# Same-strand pairs for p = 2 (RTK001 v0.2) — derivation

Status: working document (2026-10-03). Notation as in `Hc_derivation.md` §0 and main.tex §3:
`K = K_{d-1}`, period `2π`, speed `v ∈ [v_min, v_max]`, `κ ≤ κ_max ≤ 1/τ`, `τ = thick(K)`,
`r = fτ`, `f ≤ 1/2`, parallel-frame angle `ψ = mt + φ`, `m = q/2 − α/2π > 0`,
`h_min = v_min/m`, `Θ_min = h_min/τ`, `ζ_min = (1−f)h_min/r = (1−f)Θ_min/f`.
Same strand = strand index `k = 0` relative to the shorter base arc (length `σ = τδ`).
Numerical checks: `check_same_strand.py` → `check_same_strand_output.txt`.

## 0. Why the old route fails, and what replaces it

Prop. 3.9 excludes short same-strand doubly critical (DC) pairs through `σ_d ≥ π/κ̄_d`
(K_d-arclength) and converts to base parameter with the crude `V_d = v_max(1+f)+rm`.
Two losses: (i) `κ̄_d` is a sup over the whole curve (and contains `G/(τ−r)` and the
`Γ_3` term), (ii) `κ̄_d·V_d` multiplies a sup taken at `v_min` by a sup taken at `v_max`.
Replacement: measure the turning of `T_d` **per unit base arclength**, and for `d ≥ 2`
avoid derivatives altogether by splitting `T_d` into a bounded "cone angle" `χ` and a
frame that moves at a rate controlled by `κ ≤ 1/τ` and `m` only.

## 1. Lemma T (turning exclusion) — proved

**Lemma T.** Let `γ:[0,ℓ] → ℝ³` be a `C¹` arc parametrised by arclength, unit tangent
`T_γ`, endpoints `X_1 = γ(0)`, `X_2 = γ(ℓ)`, `T_1 = T_γ(0)`, `T_2 = T_γ(ℓ)`. If
`a(σ) + b(σ) < π` for all `σ`, with `a = ∠(T_γ(σ), T_1)`, `b = ∠(T_γ(σ), T_2)`, then
`(X_2 − X_1)·(T_1 + T_2) > 0`; in particular `(X_1, X_2)` is not doubly critical.

*Proof.* `a, b ∈ [0, π]`, so `cos a + cos b = 2 cos((a+b)/2) cos((a−b)/2) > 0` because
`(a+b)/2 ∈ [0, π/2)` and `|a−b|/2 < π/2`. Hence `T_γ·(T_1+T_2) > 0` pointwise and
`(X_2−X_1)·(T_1+T_2) = ∫_0^ℓ T_γ·(T_1+T_2) dσ > 0`. A DC pair has `(X_2−X_1)·T_i = 0`. ∎

*Corollary T′.* If the total turning `Φ = ∫_0^ℓ |T_γ'|` satisfies `Φ < π`, the pair is not DC
(since `a(σ) ≤ ∫_0^σ|T_γ'|`, `b(σ) ≤ ∫_σ^ℓ|T_γ'|`). This is the sharp form of the old
argument (semicircle: `Φ = π`, DC), with the *integrated* rather than the sup curvature.

## 2. Route R1: turning rate per base arclength (exact identity, ψ kept pointwise)

From (5.1) of `Hc_derivation.md`, with `A = v²(1−x)²`, `B = r²m²`, `x = rκ_⊥ ∈ [−f, f]`,
`a_0 = v'(1−x) − rv(κ_1'cos ψ + κ_2' sin ψ)`, the turning rate of `T_d` per unit `t` is
`ω := κ_d |K_d'| = |K_d'×K_d''|/|K_d'|²`, and by Minkowski (same split as Prop. 3.8)

    ω ≤ vκ (A+2B)/(A+B) + rm²/√(A+B) + rm|a_0|/(A+B).

Write `tan χ := c_W/c_T = rm/(v(1−x))` (`χ` = angle between `T_d` and `T`). Then
`B/(A+B) = sin²χ`, `rm/√(A+B) = sin χ`, so per unit **base** arclength (`dσ = v dt`):

    ω/v ≤ κ (1 + sin²χ) + (m/v) sin χ + rm|a_0|/(v(A+B)).                      (R1)

`χ` is largest on the inner side (`x = f`) at `v = v_min`: `tan χ_hi = 1/ζ_min`,
`sin χ_hi = (1+ζ_min²)^{-1/2}`. With `κ ≤ 1/τ`, `m/v ≤ 1/h_min`:

    τ Ω̄ := 1 + 1/(1+ζ_min²) + 1/(Θ_min √(1+ζ_min²)) + τ Γ_3',
    Γ_3' := rm [V_1(1+f)/v_min + r K_1] / (v_min²(1−f)² + r²m²)          ((H_3) data),

and `ω/v ≤ Ω̄` everywhere. The turning of the K_d-arc over a base arc of length `σ = τδ`
is `≤ Ω̄σ = (τΩ̄)δ`, so by Cor. T′ a same-strand DC pair has `δ ≥ δ_R1 := π/(τΩ̄)`.

**d = 1 (base = unit circle, unconditional).** `v ≡ 1`, `κ ≡ 1 = 1/τ`, `α = 0`, `m = 3/2`,
`a_0 ≡ 0` (`v' = 0`, `κ_i' = 0`), `Θ = 2/3`, `ζ = (1−f)/(1.5 f)`. At `f = 1/2`:
`ζ = 2/3`, `τΩ̄ = 1 + 9/13 + (3/2)(3/√13) = 2.94038 < 3`, so `δ_R1 = π/2.94038 = 1.06843 > π/3`.
For `f < 1/2`, `ζ` is larger and `τΩ̄` smaller (e.g. `f = 0.35`: `τΩ̄ = 2.3373`, `δ_R1 = 1.3441`).

## 3. Route R2: no derivatives of the base (no (H_3))

`T_d = cos χ T + sin χ W` with `χ(t) ∈ [χ_lo, χ_hi]`,
`tan χ_lo = rm/(v_max(1+f))`, `tan χ_hi = rm/(v_min(1−f)) = 1/ζ_min` (only `v`, `x` enter;
no derivative). Fix `χ_1 = χ(t_1)` and put `Y_1(t) = cos χ_1 T(t) + sin χ_1 W(t)`. Using
`T' = v(κ_⊥U + κ_W W)`, `W' = −mU − vκ_W T`:

    Y_1' = (vκ_⊥ cos χ_1 − m sin χ_1) U + vκ_W cos χ_1 W − vκ_W sin χ_1 T,
    |Y_1'|² = (vκ_⊥ cos χ_1 − m sin χ_1)² + v²κ_W² ≤ (vκ + m sin χ_1)²

(expand; use `κ_⊥²cos²χ_1 + κ_W² ≤ κ²` and `−κ_⊥ cos χ_1 ≤ κ`). Since `T_d(t)` and `Y_1(t)`
lie in `span(T(t), W(t))` at angles `χ(t)`, `χ_1` from `T(t)`,

    a(t) = ∠(T_d(t), T_d(t_1)) ≤ |χ(t) − χ_1| + ∫_{t_1}^{t} (vκ + m sin χ_1) dt,

and symmetrically for `b(t)` from `t_2`. Summing, for every `t` in the arc,

    a(t) + b(t) ≤ 2Δχ + δ + u sin χ_hi ≤ 2Δχ + δ (1 + sin χ_hi/Θ_min),   Δχ = χ_hi − χ_lo,

(`∫κ v dt ≤ σ/τ = δ`, `u = m|s| ≤ δ/Θ_min`). By Lemma T a same-strand DC pair has

    δ ≥ δ_R2 := (π − 2Δχ) / (1 + sin χ_hi/Θ_min).                                 (R2)

Only `κ ≤ 1/τ`, `v_min`, `v_max`, `m` enter: **no (H_3)**. A-priori form (drop `χ_lo ≥ 0`):
`δ_R2 ≥ δ_R2^ap(f, Θ_min) := (π − 2 arctan(1/ζ_min))/(1 + 1/(Θ_min√(1+ζ_min²)))`,
increasing in `Θ_min` and decreasing in `f`.

## 4. From `δ ≥ δ_turn` to the distance (proved)

For a pair with `δ < π` (Lemma A), Step 3 of Lemma 3.7 gives `|X_2−X_1| ≥ A ≥ Λ(δ)`, for every strand
index. **Claim:** `Λ(δ) ≥ r` on `[π/3, π)` for `f ≤ 1/2`. On `[π/3, π/2]`, `Λ = 2(τ−r) sin(δ/2) ≥ τ−r ≥ r`;
on `[π/2, π)` this is Step 4 of Lemma 3.7 at `f = 1/2` (`φ(ς) ≥ 0`), and `Λ/r` is decreasing in `f`.
Hence: **if `δ_turn ≥ π/3`, every same-strand DC pair satisfies `|X_2−X_1| ≥ min(2(τ−r), r)`, i.e. `c_0 ≥ 1/2`.**
Pairs with `δ ≥ π` or base chord `≥ 2τ` give `≥ 2(τ−r)` (Prop. 3.6(b) + Lemma A), as before.
Sharper: `c_0 ≥ (1/2r) inf_{δ ∈ [δ_turn, π)} max(Λ, ℓ_0 − 2r)` (`c0_Lam`), and with the `P_0` term of
Prop. 3.9 restricted to `δ ≥ δ_turn` (`c0_2D`, grid value).
At `d = 1`, `f = 1/2`: `c_0 ≥ sin(δ_R1/2) = 0.5092` (on `[δ_R1, π/2]`, `Λ/r = 2 sin(δ/2)`; on `[π/2, π)` the
argument of Step 4 with `1` replaced by `1.0183`: `φ_c(ς) = 4ς² − 1.0183ς − 1 + π/2 − 2 arcsin ς` has the same
`φ_c''`, `φ_c'(1/√2) = 1.81 > 0`, `φ_c(1/√2) = 0.280`, `φ_c(1) = 0.411`). With `P_0` (`u = 1.5δ` exactly at `d = 1`):
`0.650` (grid).

## 5. A-priori bounds in the (2,3) family, `f_j ≤ 1/2` at every depth (proved)

(a) `v_min(K_1) ≥ 2√((1−f_1)² + (3f_1/2)²)` (`|K_1'|² = (1−x)² + r_1²m_1²`, `r_1 = f_1`, `m_1 = 3/2`, period change ×2).
(b) `v_min(K_j) ≥ 2(1−f_j) v_min(K_{j−1})` (tangential coefficient, ×2) and `τ_j ≤ r_j = f_jτ_{j−1}` (Prop. 3.5), so
`v_min(K_j)/τ_j ≥ (2(1−f_j)/f_j) v_min(K_{j−1})/τ_{j−1} ≥ 2 v_min(K_{j−1})/τ_{j−1}`.
(c) `v_min(K_1)/τ_1 ≥ 2√((1−f)²/f² + 9/4) ≥ 2√(13/4) = 3.6056` for `f ≤ 1/2`; `m_d ≤ 3/2 + 1/2 = 2`.
Hence for `d ≥ 2`: **`Θ_min ≥ 1.8028·2^{d−2}`** and `ζ_min = (1−f_d)Θ_min/f_d ≥ Θ_min`. Since `δ_R2^ap` increases in
`Θ_min` and `ζ_min`, **`δ_R2 ≥ δ_R2^ap(1.8028, 1.8028) = 1.6774 > π/3` for every `d ≥ 2`**, and
`c_0 ≥ (1/2r) inf_{δ≥1.6774} Λ ≥ 0.7436` at `f = 1/2` (grid, Lipschitz-corrected; `≥ 1/2` is analytic by §4).
At `f = 1/2` the threshold for `δ_R2^ap ≥ π/3` is `Θ_min ≥ 1.1121`; the cruder bound `Θ_min ≥ 2^{d−2}` of Step 5 of
Lemma 3.7 would not suffice at `d = 2` — (a) is needed.
`d = 1`: exact circle data, route R1, `δ_R1 = 1.0684 > π/3` (`f = 1/2`), `1.3441` (`f = 0.35`).

**Conclusion (same strand, (2,3), `f ≤ 1/2`, all `d ≥ 1`, no (H_3)):** every DC pair of `K_d` with distinct base
points and strand index `0` relative to the shorter base arc satisfies `|X_2−X_1| ≥ min(2(τ−r), 2c_0r)` with
`c_0 ≥ 1/2`; more precisely `c_0 ≥ sin(δ_R1/2) = 0.509` at `d = 1, f = 1/2` and `c_0 ≥ 0.74` for `d ≥ 2`.

## 6. Curvature: ψ kept pointwise (route 1 of the task) — under (H_3)

From (5.1) without Minkowski: with `x = rκ_⊥ ∈ [−f, f]`, `|κ_W| ≤ √(1/τ² − x²/r²)`, `|a_0| ≤ V_1(1−x) + rvK_1`,

    κ_d ≤ κ̂_d := sup_{|x| ≤ f, v ∈ [v_min, v_max]} √( b_U²(A+B) + (rm(V_1(1−x)+rvK_1) + |κ_W| v (A+2B))² ) / (A+B)^{3/2},

`b_U = v²(1−x)x/r − rm²` (for fixed `x` the expression increases with `|κ_W|`, so `κ = 1/τ` is the worst case).
Grid sup with neighbour-increment correction: `r κ̂_d = 0.704, 0.967, 1.001` (`f = 1/2`, `d = 1,2,3`) vs. old
`r κ̄_d = 1.781, 2.062, 1.171` and measured `0.699, 0.325, 0.191`. So `c_κ = 1/(rκ̂_d) = 1.420, 1.034, 0.999`
(`f = 1/2`), `2.215, 1.879, 1.855` (`f = 0.35`): `c_κ ≥ 1/2` at every measured level, including `(f = 1/2, d = 2)`
(old `0.485`). At `d = 1` the bound is essentially exact (`0.7043` vs `0.6990`) and unconditional.

## 7. Resulting constants (`c = min(c_1, c_0, c_κ)`, polygons `N_0 = 256`)

| f | d | c_1 (Lemma 3.7) | c_0 new (route, H_3?) | c_0 a priori | c_κ new (H_3 for d≥2) | c |
|---|---|---|---|---|---|---|
| 0.50 | 1 | 0.6117 | 0.5091 (R1; 0.650 with P_0) | same | 1.420 | 0.509 (0.612 with P_0) |
| 0.50 | 2 | 0.6991 | 0.8454 (R2, no H_3) | 0.7436 | 1.034 | 0.699 |
| 0.50 | 3 | 0.7067 | 0.9886 (R2, no H_3) | 0.8828 | 0.999 | 0.707 |
| 0.35 | 1 | 0.9659 | 1.1561 (R1; 1.190 with P_0) | same | 2.215 | 0.966 |
| 0.35 | 2 | 0.9998 | 1.8243 (R2) | 1.6977 | 1.879 | 0.9998 |
| 0.35 | 3 | 0.9998 | 1.8567 (R2) | 1.8268 | 1.855 | 0.9998 |

Old values (Thm. 3.10): `c_0 = 0.32, 0.13, 0.16` (`f = 1/2`), `0.65, 0.66, 0.67` (`f = 0.35`).
Resolution: `f = 1/2`, `N_0 = 512`, `d = 1, 2`: identical to 4 digits.

## 8. Numerical checks (`check_same_strand.py`, ~21 s)

All on the real polygons, `(2,3)`, `f ∈ {0.25, 0.35, 0.5}`, `d = 1..3`, plus `N_0 = 512`:
`[X]` measured `χ(t) ∈ [χ_lo, χ_hi]` (slack `≥ −3·10^{-10}`; `|T_d·U| ≤ 2·10^{-4}`); `[R1]` measured turning per base
arclength `≤ Ω̄` (ratio `0.08–0.74`); `[Y]` `|dY/dσ| ≤ 1/τ + sin χ_1/h_min` (the bound used in R2; ratio `≤ 0.97`); the
pointwise form `κ + (m/v) sin χ_1` is exceeded by forward differences by up to `12%` at `d = 3` (`1.0103 → 1.0036` from
`N_0 = 256` to `512` at `d = 2`: discretisation of a fast-varying `κ`, not a failure of the identity);
`[T]` on every same-strand arc with `δ < 1.25 δ_turn`: discrete `max_t(a+b) ≤ 2Δχ + δ + u sin χ_hi` (slack `≤ −0.15`),
total turning `≤ τΩ̄δ` (slack `≤ −0.012`), and for `δ < δ_turn`: `max(a+b) ≤ 2.28 < π` and
`(X_2−X_1)·(T_1+T_2)/|X_2−X_1| ≥ 0.83 > 0`;
`[DC]` census (vertex local minima and sign-change cells of both criticality functions): same-strand DC pairs
with `δ < π` occur only at `d = 1`, all with `δ ≥ 1.96` (`f = 1/2`) and distance `≥ 3.70 r`; none at `d = 2, 3`.
`[Kap]` `κ̂_d ≥` measured `κ_d` at every level. `Λ/r ≥ 1` on `[π/3, π)` at `f = 1/2` (min `1.000000`).

## 9. What remains open

1. The curvature bound (`minRad(K_d) ≥ 1/κ̂_d`) still needs (H_3) for `d ≥ 2` (unavoidable: Remark 3.11(i)), and
   the uniformity in `d` of `r_dκ̂_d` is not proved (measured `V_1`, `K_1`).
2. `κ̂_d` and the refined `c_0` values are grid infima/suprema with an estimated Lipschitz/increment correction
   (as all constants of Thm. 3.10 except the analytic thresholds); the statements `c_0 ≥ 1/2` are analytic.
3. Nothing here is certified for the polygons themselves.
4. `p ≥ 3` and patterns with `q/p` other than `3/2` are not treated (R2 itself is general; the a-priori
   bound §5(c) uses `m ≤ 2` and `m_1 = 3/2`).
