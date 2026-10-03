# (H_3) uniforme en d — derivación (RTK001, ronda 3, trabajo teórico)

Estado: documento de trabajo, 03/10/2026. Notación de main.tex §3 y `Hc_derivation.md` §0.
`K = K_{d-1}`, parámetro `t` de periodo `2π`, velocidad `v`, marco de Bishop `(T, N_0, B_0)`,
`(κ_1, κ_2)` curvaturas del marco paralelo, `k = κ_1 N_0 + κ_2 B_0 = dT/dσ` (vector curvatura),
`U = cos ψ N_0 + sin ψ B_0`, `W = T × U`, `ψ = m t + φ`, `m = q/p − α/2π`,
`κ_⊥ = k·U`, `κ_W = k·W`, `x = rκ_⊥`, `c_T = v(1−x)`, `c_W = rm`, `w = |K_d'| = (c_T² + c_W²)^{1/2}`.
Derivadas en `t` con prima. `κ_par' := κ_1' N_0 + κ_2' B_0 = Π_⊥(dk/dt)` (parte normal de `dk/dt`).
Comprobaciones numéricas: `check_H3.py` → `check_H3_output.txt`.

## 0. Cantidades adimensionales/geométricas adecuadas

La hipótesis (H_3) del manuscrito usa `M_v = sup|v'|`, `M_κ = sup|κ_par'|` en el parámetro `t`.
Ambas dependen de la parametrización y crecen con `d` sólo por la compresión `t ↦ t/p` (factor
`p² = 4` para `v'`, `p = 2` para `κ_par'` por nivel). Las cantidades naturales son las de longitud de arco:

    ν(K) := sup |v'|/v²   ( = sup |d log v / dσ| ),        μ(K) := sup |κ_par'|/v  ( = sup |Π_⊥ dk/dσ| ).

`ν` es invariante por reparametrización lineal (`ṽ(s) = p v(ps)` da `ṽ'/ṽ² = v'/v²`) y `μ` es geométrica
(independiente de la parametrización y de la rotación constante del marco). Además
`M_v ≤ ν v_max²`, `M_κ ≤ μ v_max`.

## 1. Fórmulas exactas hasta tercer orden — y la pérdida de una derivada

Con `T' = v(κ_⊥U + κ_W W)`, `U' = mW − vκ_⊥T`, `W' = −mU − vκ_W T` y
`κ_⊥' = κ̇_⊥ + mκ_W`, `κ_W' = κ̇_W − mκ_⊥`, donde `κ̇_⊥ := κ_par'·U`, `κ̇_W := κ_par'·W`:

(1.1) `K_d' = c_T T + c_W W`.

(1.2) `w' = c_T c_T'/w`, `c_T' = a_0 − rvmκ_W`, `a_0 = v'(1−x) − rvκ̇_⊥` (la `a_0` de la Prop. 3.8).
      **Sólo intervienen `v, v', κ, κ_par'` de la base: la velocidad de `K_d` cierra a nivel (H_3).**

(1.3) `K_d''' = K''' + rU'''`, con
      `U''' = mW'' − (vκ_⊥)''T − 2(vκ_⊥)'T' − vκ_⊥T''`,  `W'' = −mU' − (vκ_W)'T − vκ_W T'`,
      `T'' = v'k + v(κ_par' − vκ²T)`·v ... (todo de orden ≤ 3 en `K`) **salvo** el término
      `−r(vκ_⊥)''T`, que contiene `v κ_par''·U` y `v''κ_⊥` (orden 4 y orden 3 no incluido en (H_3)).
      La parte normal a `K_d` de `T` es `sin χ` (`T_d = cos χ T + sin χ W`, `tan χ = c_W/c_T`), así que

          Π_{⊥,d} K_d''' = −r sin χ · (v κ_par''·U + v''κ_⊥ + 2v'κ_⊥') · n_χ + R_3,
          n_χ := sin χ T − cos χ W (unitario, normal a K_d),

      con `R_3` acotado por `(v, v', κ, κ_par', m, r)` y `K'''` (que a su vez está acotado por (H_3) más `v''`).

**Consecuencia (no-clausura).** `μ(K_d) = sup|Π_{⊥,d} K_d'''|/w³ + …` depende de `κ_par''` y de `v''` de la base.
Por tanto **no existe** una recursión `K_1(d) ≤ C K_1(d−1) + D` con `C, D` funciones de los datos (H_3) de
`K_{d−1}`: para una base arbitraria se puede hacer `sup|κ_par''| → ∞` manteniendo acotados `v, v', κ, κ_par'`
(perturbación normal local `ε^{7/2}Φ(σ/ε)`: cambia `K''` en `O(ε^{3/2})`, `K'''` en `O(ε^{1/2})`, `K''''` en
`O(ε^{−1/2})`), y entonces `μ(K_d) → ∞` porque `r sin χ > 0`. Es el análogo, un orden más arriba, de la
Obs. 3.14(i). La ruta sugerida (recursiones cerradas para `V_1` y `K_1`) **no cierra**: cierra la de `V_1`
(o `ν`), no la de `K_1` (o `μ`). Controlar `μ` uniformemente exige una jerarquía infinita (cada nivel pierde una
derivada: `K_{d-1} ∈ C^k` da en general `K_d ∈ C^{k−1}`), con el término perdido multiplicado por `r_d sin χ_d`,
que en la familia decae como `8^{−d}` (§4). Esto se registra como estructura, no como prueba.

## 2. Lo que sí cierra (demostrado; enunciados en `H3_uniform_lemma.tex`)

`ε := rκ_max(K) ≤ f`, `λ := rm/v_min`, `ζ' := v_min(1−ε)/(rm) ≥ ζ_min`.

**Lema 2.1 (velocidad).** De (1.2), `|w'|/w² ≤ |a_0 − rvmκ_W|/c_T²`, luego
`ν(K_d) ≤ ν(K)/(1−ε) + (rμ(K) + λκ_max(K))/(1−ε)²`. Cierra a nivel (H_3); `ν` es invariante por `t ↦ t/p`.

**Prop. 2.2 (curvatura con κ_max de la base en vez de 1/τ).** El reparto de Minkowski de la Prop. 3.8 con
`|x| ≤ ε` y `κ ≤ κ_max(K)` da
`κ_max(K_d) ≤ κ_max(K)G(ζ')/(1−ε) + 1/(r(1+ζ'²)) + λ(ν(1+ε) + rμ)/(1−ε)³`.
Mejora clave: el primer término es `ε G/(1−ε)` tras multiplicar por `r`, con `ε = r_dκ_max(K_{d−1}) → 0`
(medido 0.29, 0.16, 0.096 en `d = 2, 3, 4`, f = 1/2), en vez de `f/(1−f) = 1`.

**Cor. 2.3 (tolerancia, (2,3), f ≤ 1/2, d ≥ 3).** Con `ζ' ≥ Θ_min ≥ √13·2^{d−3}`, `r_d ≤ 2^{−d}`,
`λ ≤ 2^{3−d}/√13`, `ε ≤ 1/2`: si `(96/√13)4^{−d}ν(K_{d−1}) + (64/√13)8^{−d}μ(K_{d−1}) ≤ 2 − g(√13) − 1/14 = 0.8961`,
entonces `minRad(K_d) ≥ r_d/2` y `thick(K_d) ≥ r_d/2`. Crecimiento tolerado: `ν ≤ 0.0336·4^d`, `μ ≤ 0.0505·8^d`.
En `d = 2` las constantes a priori no bastan (`1.664ν_1 + 0.277μ_1 ≤ 0.684` haría falta; `ν_1 ≈ 0.42`, `μ_1 ≈ 4.5`).

## 3. Lo que no cierra

`μ(K_{d−1})` (orden 3) necesita `κ_par''` y `v''` de `K_{d−2}` (§1), éstos el orden 5 de `K_{d−3}`, etc. Una cota
a priori uniforme exige controlar todas las derivadas; la ruta natural (no hecha) es una inducción en una banda
compleja `|Im t| < η_d` (el marco de Bishop resuelve `Y' = −(Y·K'')K'/(K'·K')`, analítico sin raíces cuadradas;
la banda se reduce por `p` por nivel, a la par que las frecuencias crecen; las pérdidas de Cauchy van multiplicadas
por `r_d/(δ_d v_min)`, sumable). Sin esa inducción, **(H_c) con c = 1/2 sigue demostrado sólo en d = 1**; para d ≥ 3
queda reducido a la condición explícita de crecimiento del Cor. 2.3, y en d = 2 a una evaluación (malla/polígono).

## 4. Numérica (`check_H3.py`, 8 s de pared)

f = 1/2 (N_0 = 256 y 512, idénticos a 3 cifras; d = 4 con N_0 = 128):
`ν = 0.42, 0.72, 1.12, 1.35`, `μ = 4.5, 5.0, 6.2, 6.9`, `κ_max = 1.40, 1.57, 1.84, 2.03` (d = 1..4): crecimiento
acotado con cocientes decrecientes (ν: 1.71, 1.56, 1.21; κ_max: 1.12, 1.17, 1.10 ≈ 1/(1−ε_d)).
Normalización sugerida por el encargo: `r_{d}M_v(K_{d−1})/v_min = 0.28, 0.46, 0.62` (crece despacio, por
`v_max/v_min` = 1.86, 2.66, 3.32), `r_d²M_κ(K_{d−1}) = 0.35, 0.17, 0.093` (decrece ≈ 2^{−d}).
[W] identidad (1.2): error relativo ≤ 5·10⁻³ (N_0 = 128), ≤ 3·10⁻⁴ (N_0 = 512). [NU] Lema 2.1: cociente
medido/cota ≤ 0.90 en todos los niveles. [KA] Prop. 2.2: ≤ 0.989 (f = 0.25, d = 3), 0.979 (f = 1/2, d = 4).
[TOL] lado izquierdo del Cor. 2.3: 0.47 (d = 3), 0.14 (d = 4) ≤ 0.896; forma afinada con datos medidos
`r_d·cota = 0.72, 0.21, 0.11` (d = 2, 3, 4) ≤ 2. Todo con f ∈ {0.25, 0.35, 0.5}: ningún fallo.
