# Segundo orden en la ley del realizador (MRT001, Obs. 5.11)

Correspondencia con `second_order.tex`: Teorema 1 y Corolario 1 + §2 = `thm:secondN`; Teorema 2 =
`thm:bestpois`; Lema 1 = `lem:signs`; Lema 3 = `lem:intref`; Proposición 3 = `prop:sharpC`;
§5 = `rem:secondopen`. Salida de referencia: `theory/check_second_order_output.txt` (51 s de CPU),
números en `theory/second_order_results.json`.

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

## 4. Constante explícita en el Teorema 5.9

Notación: `(m)_j = m(m−1)⋯(m−j+1)`, `E I_k(m) = (m−k+1)²/C(m,k)` (Paso 2 del Apéndice B),
`s_m`, `h_m` como en la prueba del Lema B.2(b), `E` el evento malo del Lema B.2.

**Lema 3 (intervalos, versión afinada del Lema B.2(a)).** Sea
`F̄(m) = 42/(m)_2 + 936/(m)_3 + 600/(m)_4 + 4320/(m)_5`. Para `m ≥ 12`:

(a) `Σ_{k=4}^{m−2} E I_k(m) ≤ F̄(m)`;
(b) `P(E) ≤ P̄_E(n) := 90/(n)_2 + 944/(n)_3 + 600/(n)_4 + 4320/(n)_5` (con `n = m`);
(c) `s_m ≤ 10/m + F̄(m)` y `h_m ≤ 8/m + 18/(m)_2 + F̄(m)`.

*Prueba.* (a) Valores exactos: `E I_4 = 24(m−3)/(m)_3 ≤ 24/(m)_2`, `E I_{m−2} = 18/(m)_2`,
`E I_{m−3} = 96/(m)_3`, `E I_{m−4} = 600/(m)_4`, `E I_5 = 120(m−4)/(m)_4 ≤ 120/(m)_3`,
`E I_{m−5} = 4320/(m)_5`; los seis índices son distintos si `m ≥ 12`. Para `6 ≤ k ≤ m−6`
(`m − 11` términos), `C(m,k) ≥ C(m,6)` y `(m−k+1)² ≤ (m−5)²`, así que su suma es
`≤ 720(m−11)(m−5)/(m)_5 ≤ 720/(m)_3` (porque `(m−11)(m−5) ≤ (m−3)(m−4)`). Total:
`(24+18)/(m)_2 + (96+120+720)/(m)_3 + 600/(m)_4 + 4320/(m)_5`.
(b) La prueba del Lema B.2(a) da `P(E) ≤ Σ_{k=4}^{n−2} E I_k + E C(I_3,2) + E[I_3 I_{n−1}] +
E C(I_{n−1},2)` con los momentos de pares exactos
`E C(I_3,2) = 18(n−4)(n−5)/(n)_4 + 4(n−3)/(n)_3 + 8(n−4)/(n)_4 ≤ 18/(n)_2 + 4/(n)_2 + 8/(n)_3`,
`E[I_3 I_{n−1}] = 4(6n−16)/(n)_3 ≤ 24/(n)_2`, `E C(I_{n−1},2) = 2/(n)_2`. Sumando con (a):
`(42+18+4+24+2)/(n)_2 + (936+8)/(n)_3 + …`.
(c) `s_m = E I_3(m) + Σ_{k=4}^{m−2} E I_k(m) + E I_{m−1}(m)` con `E I_3 = 6(m−2)/(m)_2 ≤ 6/m` y
`E I_{m−1} = 4/m`. Para `h_m`, la prueba del Lema B.2(b) da
`h_m ≤ 4/m + 18/(m)_2 + Σ_{l=4}^{m−1} E I_l(m)`. ∎

(Asintóticamente `n² P̄_E(n) → 90` frente a `223` del Lema B.2(a): el término `120/n²` de
`5 ≤ k ≤ n−5` es en realidad `O(n^{−3})`.)

**Proposición 3 (constante explícita).** Sea, para `n ≥ 22`,

    B(n) = ρ̄_1(n) + P̄_E(n) + Ē(n) + Ō(n) + 3/(n)_2,
    ρ̄_1(n) = 2^{n+1}/(n (n+1)!) + 1/n!,
    Ē(n) = (3(n−2)/(n)_2)(s̄_{n−2} + 3 h̄_{n−2}) + 12/(n)_2 + (2/n)(s̄_{n−1} + h̄_{n−1}),
    Ō(n) = (3(n−2)/(n)_2)(4/(n−2) + 2 d̄_{n−2}) + (2/n)(2/(n−1) + 2 d̄_{n−1}),

con `s̄_m`, `h̄_m` las cotas del Lema 3(c) y `d̄_m = e^{−1}/m + 2/(m·m!)`. Entonces, para todo
conjunto `A` y todo `n ≥ 22`,

    |P(R_n ∈ A) − P(2^Z ∈ A) − μ(A)/n| ≤ B(n),

`n² B(n)` es no creciente, y por tanto `|d_TV(R_n, 2^Z) − c_2/n| ≤ C(n_0)/n²` para `n ≥ n_0` con
`C(22) = 421.5`, `C(30) = 363.2`, `C(50) = 314.4`, `C(100) = 285.8`, `C(1000) = 264.8`
(valores de `n_0² B(n_0)` redondeados hacia arriba) y `lim n² B(n) = 259 + 10/e = 262.68`.
En particular: **para todo `n ≥ 22`, `|d_TV(R_n, 2^Z) − c_2/n| ≤ 422/n²`.**

*Prueba.* Se siguen los pasos de la prueba del Teorema 5.9 y se acota cada error:

1. Primer corchete: `|ρ_1| ≤ ρ̄_1(n)` (Teorema 5.8(i), como en la prueba del Teorema 5.9).
2. Fuera de `E` la diferencia `1{R∈A} − 1{2^N∈A}` es `Σ_ω 1_ω g_ω(N)`; el error por usar esta
   suma en todo el espacio es `≤ P(E) + E[#ω; E] ≤ P̄_E(n) + Ē(n)`: la cota de `E[#ω; E]` es la
   de la prueba del Lema B.2(b) con `s_m`, `h_m` acotados por el Lema 3(c) (`m = n−2 ≥ 20`).
3. Para una ocurrencia de tres elementos, `|E[g_ω(N) | ω] − E g_ω(N(p) + Z)| ≤ 2P(δ ≠ 0 | ω) +
   2 d_TV(N_{n−2}, Z) ≤ 4/(n−2) + 2 d̄_{n−2}` (`g_ω` toma valores en `{−1, 0, 1}`, `δ ≠ 0` exige una
   sucesión descendente de `σ` en una de las dos posiciones vecinas de `j*`, cada una con
   probabilidad `1/(n−2)`, y el Teorema 5.8(ii) con `n − 2 ≥ 4`); para las dos ocurrencias de
   borde, `2/(n−1) + 2 d̄_{n−1}`. Multiplicando por los pesos `3(n−2)/(n)_2` y `2/n` se obtiene
   `Ō(n)`.
4. Sustituir los pesos exactos `(n−2)/(n(n−1))` por `1/n` cuesta `1/(n(n−1))` por patrón, es decir
   `3/(n)_2` en total (`|E g| ≤ 1`).

Como `d_TV(R_n, 2^Z) = sup_A |P(R_n∈A) − P(2^Z∈A)|` y `c_2/n = sup_A |μ(A)|/n`, la diferencia de
los supremos está acotada por el supremo de las diferencias. Monotonía: tras las sustituciones,
cada sumando de `n² B(n)` es de la forma `c · n² / (n^a (n−1)^b (n−2)^c ⋯)` con `c > 0` y grado
del denominador `≥ 2`, o `n² ρ̄_1(n)`; todos son no crecientes en `n ≥ 22` (se comprobó además
numéricamente para `22 ≤ n ≤ 5000`; los términos con factorial, `n²·2^{n+1}/(n(n+1)!)`, `n²/n!` y los
que vienen de `2/(m·m!)` en `d̄_m`, también decrecen). El límite:
`90 + (3·(10+24) + 12 + 2·18) + (12 + 6/e + 4 + 4/e) + 3 = 90 + 150 + 16 + 10/e + 3 = 259 + 10/e
= 262.68`. ∎

Comparación numérica (sección D de la salida): con la ley exacta de `R_n` para `n ≤ 600`,
`n² |d_TV(R_n, 2^Z) − c_2/n| ≤ 5.72` para `22 ≤ n ≤ 600` (máximo `8.00` en `n = 12` sobre
`4 ≤ n ≤ 600`); la cota es unas 70 veces holgada, sobre todo por `P(E)` y `E[#ω; E]`, que cuentan
todos los intervalos largos aunque casi nunca cambien `R_n`.

## 5. La ley exacta de `R_n` y el término `n^{−2}` (numérico)

**Método (exacto).** Por la Observación B.1 (fórmula de Gallai), `t(G_π)` es el producto sobre los
nodos del árbol de descomposición por sustitución de `1` (suma directa), `k!` (suma sesgada con `k`
hijos) y `2` (nodo simple), y `R = t/2` salvo para la identidad. Un producto es de la forma
`2^a 3^b` con `b ≤ 1` sii los nodos sesgados tienen `k ∈ {2,3,4}` (`2! = 2`, `3! = 2·3`,
`4! = 2³·3`) y a lo sumo uno con `k ∈ {3,4}`. Con `z` = tamaño, `y` = exponente de 2, `w` = factor
3 (truncando `w² = 0`, `y^{20} = 0`), la serie `A` de las permutaciones no vacías con
`t = 2^a 3^b`, `b ≤ 1`, satisface

    A = z + D + K + S,   D = Σ_{k≥2} I_⊕^k,   I_⊕ = z + K + S,
    K = y I_⊖² + y w I_⊖³ + y³ w I_⊖⁴,   I_⊖ = z + D + S,   S = y Σ_{m≥4} s_m A^m,

con `s_m` el número de permutaciones simples de longitud `m` (unicidad de la descomposición:
Albert–Atkinson 2005). Los `s_m` salen de `Σ_{m≥4} s_m u^m = u − g(u) − 2u²/(1+u)`, `g` la inversa
composicional de `Σ n! z^n`, que cumple `(1+u) g g' − u g' + g² = 0` (porque
`f = Σ n! z^n` cumple `z² f' + (z−1) f + z = 0`), lo que da una recurrencia `O(M²)` exacta. Así
`P(R_n = 2^k) = [z^n y^{k+1} w^0] A / n!` (más `1/n!` si `k = 0`, la identidad) y
`P(R_n = 3·2^k) = [z^n y^{k+1} w] A / n!`. La masa restante (otros valores de `R_n`) se obtiene
por diferencia, y `d_TV(R_n, 2^Z)` es exacta salvo `P(Z ≥ 19) < 10^{−17}` y el redondeo.

**Comprobaciones.** Ley GF = fórmula de Gallai en todas las permutaciones `n ≤ 8`; = fuerza bruta
sobre pares de extensiones lineales `n ≤ 6`; aritmética entera exacta (`n ≤ 30`) = coma flotante
escalada (error relativo `1.1·10^{−15}`); `s_4..s_10` = valores conocidos y fuerza bruta `m ≤ 8`.

**Resultados (numéricos; no demostrados).** Con la ley exacta para `n ≤ 600`:

* átomo a átomo, `n(P(R_n = x) − P(2^Z = x)) → μ(x)` (Teorema 5.9 confirmado sin Monte Carlo;
  `n² |P − P_Z − μ/n| ≤ 3.15` para `100 ≤ n ≤ 600` en todos los átomos seguidos);
* `n · d_TV(R_n, 2^Z)` decrece hacia `c_2 = 1.18394` (`1.19262` en `n = 500`);
* `κ := lim n² (d_TV(R_n, 2^Z) − c_2/n) ≈ 4.29707` (ajustes polinómicos en `1/n` de grado 2, 3 y
  4 sobre `200 ≤ n ≤ 600` coinciden en 6 cifras);
* coeficientes de segundo orden `μ_2(x) = lim n²(P(R_n = x) − P(2^Z = x) − μ(x)/n)` en la salida
  (sección D3), con `n² P(R_n ∉ {2^k, 3·2^k}) → 1/2`.

**Formas cerradas observadas (conjetura).** Los límites extrapolados (ajuste de grado 3,
`200 ≤ n ≤ 600`) multiplicados por `e` son: en `2^k`, `−5, −8, 1/2, 5/3, 19/24, 1/3, 0.134722,
0.044841, …` para `k = 0, 1, 2, …`; en `3·2^k`, `0, 2, 3, 2, 5/6, 1/4, 0.058333, 0.011111, …`. Los
valores `e·k!·μ_2(2^k)` son `−5, −8, 1, 10, 19, 40, 97, 226, 475, 904`, cuyas cuartas diferencias
son constantes (`12`), es decir

    μ_2(2^k) ≈ π_k [12 C(k,4) − 12 C(k,3) + 12 C(k,2) − 3k − 5],
    μ_2(3·2^k) ≈ (k+1) π_{k−1}   (k ≥ 1),   μ_2(3) = 0,

y la masa `1/2` va a los demás valores de `R_n`. Comprobación de masa total:
`E[12C(Z,4) − 12C(Z,3) + 12C(Z,2) − 3Z − 5] = 1/2 − 2 + 6 − 3 − 5 = −7/2`,
`Σ_{k≥1}(k+1)π_{k−1} = 3`, `−7/2 + 3 + 1/2 = 0`. Como `μ > 0` solo en `4` y en `3·2^k` (`k ≥ 1`),
y `μ = 0` en `2`, `3` y `8` (con `μ_2(2) = −8/e < 0`, `μ_2(3) = 0`, `μ_2(8) = 5/(3e) > 0`), el
segundo orden de la distancia sería

    κ = μ_2(4) + μ_2(8) + Σ_{k≥1} μ_2(3·2^k) + 1/2 = 1/(2e) + 5/(3e) + 3 + 1/2 = 7/2 + 13/(6e)
      = 4.2970716…,

frente a `4.2970713` y `4.2970722` (ajustes de grado 3 y 4) y `4.297071` (suma átomo a átomo). La
coincidencia es de 6 cifras, pero las formas cerradas se han leído de los números: son una
conjetura, no un resultado.

Lo que **no** se afirma: ni la existencia de un desarrollo `c_2/n + κ/n² + O(n^{−3})` ni el valor
de `κ` están demostrados; son extrapolaciones de valores exactos. Un camino plausible para
demostrarlos es el mismo análisis que el Teorema 5.9 llevado un orden más (pares de ocurrencias,
intervalos de 4 y `n−2` elementos, correcciones `O(1/n)` de los pesos y de `N_{n−2}` frente a `Z`),
o bien un teorema de tipo Bender para la ecuación funcional de la sección 5.

## 6. Resumen de estados

| afirmación | estado |
|---|---|
| `n² d_TV(N_n, Po(1−1/n)) → 3/(4e)`; forma cerrada `Φ(1/n)` salvo `(2^{n+1}−n−2)/(n(n+1)!)`; siguiente término `1/(4en)` | demostrado aquí (Teorema 1, Corolario 1) |
| momentos factoriales: `E(N_n)_r − (1−1/n)^r = −C(r,2)/n² + θC(r,3)/n³`; corrección `−π_k(k²−3k+1)/(2n²)` | demostrado aquí |
| mejor Poisson: `n² inf_λ d_TV → 1/(2e)`, `λ = 1 − 1/n + 1/(2n²)` | demostrado aquí (Teorema 2) |
| `|d_TV(R_n,2^Z) − c_2/n| ≤ 422/n²` (`n ≥ 22`), `≤ 286/n²` (`n ≥ 100`) | demostrado aquí, usa Gallai (Proposición 3) |
| `n²|d_TV(R_n,2^Z) − c_2/n| ≤ 5.72` para `22 ≤ n ≤ 600` | verificado numéricamente (ley exacta) |
| `κ = 4.29707…` | verificado numéricamente (extrapolación de valores exactos) |
| `κ = 7/2 + 13/(6e)`, formas cerradas de `μ_2` | conjetural |

Nada de lo anterior ha pasado por un árbitro independiente.
