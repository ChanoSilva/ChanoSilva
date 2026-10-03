[EN CURSO]

# Segundo orden en la ley del realizador (MRT001, Obs. 5.11)

Notas de trabajo (español). Notación de `manuscript/main.tex`, Sección 5 y Apéndice B:
`π` uniforme en `S_n`, `N = N_n` = número de sucesiones descendentes, `R = R_n` = realizadores
módulo el intercambio, `Z ~ Po(1)`, `p_k = P(N_n = k)`, `π_k = e^{-1}/k!` (`π_k = 0` si `k < 0`),
`r_{n,k}` el resto del Teorema 5.8(i): `p_k = π_k(1 − (k−1)/n) + r_{n,k}`,
`|r_{n,k}| ≤ 1/(n k! (n−k+1)!)` para `0 ≤ k ≤ n−1`, y `p_k = 0` para `k ≥ n`.
Comprobación numérica: `theory/check_second_order.py`, salida en
`theory/check_second_order_output.txt`.

## 1. La ley de `N_n` frente a `Po(1 − 1/n)`

Sea `x = 1/n`, `λ = 1 − x`, `q_k = P(Po(λ) = k) = π_k e^{x} (1−x)^k`. Definimos

    h_k(x) = e^{x}(1−x)^k − 1 − (1−k)x ,

de modo que `π_k(1 − (k−1)/n) − q_k = −π_k h_k(x)` y, para `0 ≤ k ≤ n−1`,

    p_k − q_k = −π_k h_k(x) + r_{n,k}.                                         (1.1)

**Lema 1 (signos).** Para `0 < x < 1/2`: `h_0 > 0`, `h_1 < 0`, `h_2 < 0` y `h_k > 0` para todo
entero `k ≥ 3`.

*Prueba.* `h_0 = e^x − 1 − x > 0`. `h_1 = e^x(1−x) − 1 < 0` porque `1 − x < e^{−x}`.
`h_2 = e^x(1−x)^2 − (1−x) = (1−x) h_1 < 0`. Para `k = 3`: `h_3 > 0` equivale a
`φ(x) = x + 3 log(1−x) − log(1−2x) > 0`; `φ(0) = 0` y
`φ'(x) = 1 − 3/(1−x) + 2/(1−2x) = x(2x+1)/((1−x)(1−2x)) > 0`. Finalmente `k ↦ h_k(x)` (con `k`
real) es convexa (exponencial en `k` menos una función afín), y `h_2 < 0 < h_3`, así que para
`k ≥ 3`, `h_k ≥ h_3 + (k−3)(h_3 − h_2) ≥ h_3 > 0`. ∎

**Teorema 1 (forma cerrada).** Para `n ≥ 3`,

    d_TV(N_n, Po(1 − 1/n)) = D(1/n) + ε_n,
    D(x) = (e^{−1}/2) (3 − x) (1 − (1−x) e^{x}),
    |ε_n| ≤ (2^{n+1} − n − 2) / (n (n+1)!).

*Prueba.* `d_TV = Σ_k (p_k − q_k)^+`. Para `k ≥ n`, `p_k = 0` y el término es `0`. Para
`0 ≤ k ≤ n−1` sea `y_k = −π_k h_k(1/n)`; como `t ↦ t^+` es 1-Lipschitz,
`|(p_k − q_k)^+ − y_k^+| ≤ |r_{n,k}|`. Por el Lema 1 (`x = 1/n ≤ 1/3`), `y_k^+ = π_k |h_k|` para
`k ∈ {1, 2}` (ambos `≤ n−1` porque `n ≥ 3`) y `y_k^+ = 0` en los demás casos. Así
`d_TV = π_1|h_1| + π_2|h_2| + ε_n` con `|ε_n| ≤ Σ_{k=0}^{n−1} |r_{n,k}|
≤ (1/(n (n+1)!)) Σ_{k=0}^{n−1} C(n+1, k) = (2^{n+1} − n − 2)/(n (n+1)!)`. Por último
`π_1|h_1| + π_2|h_2| = e^{−1}(1 − e^x(1−x)) + (e^{−1}/2)(1−x)(1 − e^x(1−x)) = D(x)`. ∎

**Desarrollo.** `1 − (1−x)e^x = Σ_{j≥2} (j−1) x^j / j!` (coeficientes positivos), luego

    D(x) = e^{−1} Σ_{j≥2} d_j x^j,   d_j = (−j² + 5j − 3) / (2 · j!),

`d_2 = 3/4`, `d_3 = 1/4`, `d_4 = 1/48` y `d_j < 0` para `j ≥ 5`. Para `0 < x ≤ 1/3`,
`Σ_{j≥5} |d_j| x^{j−4} ≤ x Σ_{j≥5}|d_j| < 1/48`, de modo que

    0 < n² D(1/n) − 3/(4e) − 1/(4e n) ≤ 1/(48 e n²)      (n ≥ 3).

**Corolario 1.** `n² d_TV(N_n, Po(1 − 1/n)) = 3/(4e) + 1/(4e n) + θ_n/(48 e n²) + n² ε_n` con
`θ_n ∈ (0, 1]`; en particular `n² d_TV(N_n, Po(1 − 1/n)) → 3/(4e) = 0.27591…`.
La Observación 5.11 era correcta; ahora está demostrada, con el término siguiente `1/(4e n)`.
(En `n = 1000`: `3/(4e) + 1/(4000e) = 0.276002…`, frente a `0.2760` observado.)

## 2. Momentos factoriales y la corrección de segundo orden

Por el Paso 3 del Apéndice B, `E[(N_n)_r] = 1 − r/n` para `0 ≤ r ≤ n−1`. La medida con signo
`π + ν/n`, `ν(k) = π_k − π_{k−1}`, tiene exactamente esos momentos factoriales *para todo* `r`:
`Σ_k π_k (k)_r = 1` y `Σ_k ν(k) (k)_r = 1 − E[(Z+1)_r] = 1 − (1 + r) = −r` (porque
`(Z+1)_r = (Z)_r + r (Z)_{r−1}`). Esto explica que `p_k − π_k − ν(k)/n` sea superexponencialmente
pequeño (Teorema 5.8(i)).

Para `Po(λ)`, `E[(X)_r] = λ^r`, y con `λ = 1 − 1/n`:

    E[(N_n)_r] − (1 − 1/n)^r = −Σ_{i=2}^{r} C(r,i) (−1/n)^i = −C(r,2)/n² + θ C(r,3)/n³,

`θ ∈ [0,1]`, para `r ≤ n−1` (serie alternada con términos decrecientes, pues
`C(r,i+1)/(C(r,i) n) = (r−i)/((i+1)n) < 1`). En la escala de las probabilidades puntuales:

    q_k = π_k e^{x}(1−x)^k = π_k Σ_{j≥0} c_j(k) x^j,   c_j(k) = Σ_{i=0}^{j} (−1)^i C(k,i)/(j−i)!,

(`c_j(k)` es el coeficiente de `x^j` en `e^x(1−x)^k`; son, salvo el factor `j!`, los polinomios de
Charlier de parámetro 1 — observación no usada en las pruebas), con `c_0 = 1`, `c_1(k) = 1 − k`,
`c_2(k) = (k² − 3k + 1)/2`. Por tanto, exactamente,

    p_k = q_k − π_k Σ_{j≥2} c_j(k) n^{−j} + r_{n,k}      (0 ≤ k ≤ n−1),

y el término de corrección de segundo orden es `−π_k (k² − 3k + 1)/(2n²)`.
`Σ_k π_k c_2(k) = 0` y `Σ_k π_k |c_2(k)| = 3/(2e)` (solo `k = 1, 2` son negativos), de donde
de nuevo `3/(4e)`.

## 3. La mejor Poisson

Con `λ = 1 − 1/n + a/n²`, el primer orden sigue anulándose y el segundo depende de `a`:

    g_a(k) = c_2(k) + a(k − 1) = [(k−1)(k−2+2a) − 1]/2,   L(a) = Σ_k π_k |g_a(k)|.

**Teorema 2.** (i) Para cada `a` real fijo, `n² d_TV(N_n, Po(1 − 1/n + a/n²)) → L(a)/2`.
(ii) `L(a) ≥ e^{−1}` con igualdad si y solo si `a = 1/2`; para `a ≥ −1/4`,
`L(a) = e^{−1}[1 + (2a−1)^+ + (1/2 − a)^+]` (`L(0) = 3/(2e)`).
(iii) `n² inf_{λ>0} d_TV(N_n, Po(λ)) → 1/(2e)`, y `λ_n = 1 − 1/n + 1/(2n²)` alcanza el límite.

*Prueba.* (i) Sea `δ = 1 − λ = x − a x²`, `0 < δ ≤ 1` para `n` grande. Como
`|c_j(k)| ≤ [x^j] e^x (1+x)^k` y `Σ_j [x^j] e^x(1+x)^k = e 2^k`,
`|q_k − π_k(1 + c_1(k) δ + c_2(k) δ²)| ≤ π_k e 2^k δ³`, y `Σ_k π_k e 2^k = e²`. Para
`k ≤ n−1`, por (1.1) y `p_k = π_k(1 + c_1(k) x) + r_{n,k}`:

    p_k − q_k = −π_k g_a(k) x² + π_k c_2(k)(x² − δ²) + r_{n,k} + O(π_k e 2^k δ³),

ya que `c_1(k)(x − δ) = (1−k) a x²`. Para `k ≥ n`, `|p_k − q_k + π_k g_a(k) x²| ≤ q_k +
π_k|g_a(k)| x²`, cuya suma es superexponencialmente pequeña. Sumando,
`|2 d_TV − x² L(a)| ≤ (3/(2e))|x² − δ²| + e² δ³ + Σ_k|r_{n,k}| + (cola) = O(x³)`, uniformemente
para `a` en compactos.
(ii) `Σ_k π_k g_a(k) = 0` (porque `E c_2(Z) = 0` y `E(Z − 1) = 0`). Con `f(1) = −1` y `f(k) = 1`
si `k ≠ 1`: `L(a) ≥ Σ_k π_k g_a(k) f(k) = −2 π_1 g_a(1) = e^{−1}`, pues `g_a(1) = −1/2`. La
igualdad exige `g_a(k) ≥ 0` para `k ≠ 1`; `g_a(0) = (1−2a)/2` y `g_a(2) = (2a−1)/2` fuerzan
`a = 1/2`, y `g_{1/2}(k) = k(k−2)/2` la cumple. Para `a ≥ −1/4` los únicos `k` con `g_a(k) < 0`
son `k = 1` y, según el signo de `a − 1/2`, `k = 0` o `k = 2` (`g_a(3) = (1+4a)/2 ≥ 0`, y
`(k−1)(k−2+2a) − 1 ≥ 5 + 6a > 0` para `k ≥ 4`), lo que da la fórmula.
(iii) Cota superior: (i) con `a = 1/2`. Cota inferior: si `a ∈ [−1/2, 3/2]`, (i) uniforme y (ii)
dan `n² d_TV ≥ 1/(2e) − O(1/n)`. Si `λ > 1 − 1/n + 3/(2n²)`, como `q_0 = e^{−λ}` decrece,
`d_TV ≥ p_0 − q_0(λ) ≥ p_0 − q_0(1 − x + 3x²/2) = e^{−1}[1 + x − e^{x − 3x²/2}] + r_{n,0}
= e^{−1}x² + O(x³)`; si `λ < 1 − 1/n − 1/(2n²)`, igualmente
`d_TV ≥ q_0(λ) − p_0 ≥ e^{−1}[e^{x + x²/2} − 1 − x] − |r_{n,0}| = e^{−1}x² + O(x³)`. En ambos
casos `n² d_TV ≥ e^{−1} − o(1) > 1/(2e)`. ∎

Lectura: `Po(1 − 1/n)` (la Poisson con la media exacta) no es la mejor Poisson a segundo orden; la
óptima tiene `λ = 1 − 1/n + 1/(2n²) + o(n^{−2})` (que coincide a ese orden con `e^{−1/n}`) y
constante `1/(2e) = 0.18394…` en lugar de `3/(4e) = 0.27591…`.
