# RTK001 — Caso d = 2 de (H_c) con c = 1/2: demostración asistida por computador (aritmética de intervalos), y barrido conjunto de normalizaciones para la Conjetura 3.23

Bloque de teoría/cómputo certificado, 03/10/2026. No modifica `manuscript/main.tex` ni ningún archivo existente.
Archivos: `theory/certify_d2.py` (+ `certify_d2_output.txt`, `certify_d2.json`), `theory/joint_phase_sweep.py`
(+ `joint_phase_sweep_output.txt`, `joint_phase_sweep.json`), `theory/d2_certified.tex` (bloque para pegar).
Numeración de v0.4: Def. 2.1 (`def:family`), Prop. 3.5 (`prop:upper`), Lema 3.7 (`lem:Hc1`), Prop. 3.8
(`prop:Hccurv`), Teorema 3.12 (`thm:Hc`), Lema 3.14 (`lem:speedrec`), Prop. 3.15 (`prop:curvrec`, ec. (kaprec)),
Cor. 3.16 (`cor:tolerance`), Prop. 3.17 (`prop:noclose`), Obs. 3.18 (`rem:H3status`), Hip. 3.19 (`hyp`),
Cor. 3.20 (`cor:rec`), Conj. 3.23 (`conj`).

## 0. Qué hay que demostrar

Por el Teorema 3.12(c), para la familia por defecto (2,3) con f_j ≤ 1/2 en cada nivel, (H_c) con c = 1/2 en la
profundidad d ≥ 2 equivale a

    minRad(K_d) ≥ r_d / 2,   es decir   r_d · κ_max(K_d) ≤ 2.

(La parte de pares doblemente críticos, ½ dcsd(K_d) ≥ r_d/2, ya está demostrada a priori en toda profundidad.)
En d = 2 la base es K_1, un polinomio trigonométrico explícito. La Obs. 3.18 constata que con las constantes a
priori (ζ' ≥ √13/2, ε ≤ 1/2, λ ≤ 2/√13, ...) no se llega: haría falta (6/√13)ν(K_1) + (1/√13)μ(K_1) ≤ 0.685 y
los polígonos dan 1.95 (con los datos certificados de abajo, ≤ 2.006; sigue fallando). Aquí se usa la
Prop. 3.15 con los datos **verdaderos** de K_1, encerrados rigurosamente.

## 1. La reducción: solo hacen falta cuatro números de K_1 y la cota a priori m ≤ 2

**Prop. 3.15 (ya demostrada en el manuscrito).** Para una base K (C^∞, regular, cerrada, parámetro de periodo 2π
heredado de la Def. 2.1) y K_d construida con su marco de Bishop cerrado,

    κ_max(K_d) ≤ κ_max(K) G(ζ')/(1−ε) + 1/(r(1+ζ'²)) + λ(ν(K)(1+ε) + r μ(K))/(1−ε)³,

con ε = r κ_max(K), λ = r m / v_min, ζ' = v_min(1−ε)/(r m), G(ζ) = sup_{z ≥ ζ} g(z),
g(z) = z(z²+2)/(z²+1)^{3/2}, ν = sup|v'|/v², μ = sup|Π_⊥ dκ/dσ| (κ = vector curvatura) y m = q/p − α/2π.
Revisé la demostración paso a paso (descomposición K_d' = c_T T + c_W W, identidad
|K_d'×K_d''|² = b_U²(A+B) + (r m a_0 − κ_W v(A+2B))², separación de Minkowski en tres términos; cada término se
acota como en el texto). Solo usa ε < 1 (para 1 − x > 0) y m > 0.

**Monotonía (paso clave).** Multiplicando por r = r_2:

    Φ := r κ_max(K) G(ζ')/(1−ε) + 1/(1+ζ'²) + r λ (ν(1+ε) + r μ)/(1−ε)³.

* Φ es no decreciente en κ_max, ν, μ, r y m, y no creciente en v_min: ε crece con r y κ_max; ζ' decrece con
  r, κ_max, m y crece con v_min; G es no creciente (g crece en [0,√2] y decrece en [√2,∞), por lo que
  G(ζ) = g(√2) para ζ ≤ √2 y G(ζ) = g(ζ) para ζ ≥ √2); λ crece con r, m y decrece con v_min.
* Por tanto basta evaluar Φ en (κ_max ↑, ν ↑, μ ↑, r ↑, m ↑, v_min ↓): cotas superiores de κ_max, ν, μ, inferior
  de v_min, el mayor r_2 admisible y m = 2.

**m ≤ 2 a priori, sin calcular el marco.** α ∈ (−π, π] da m = 3/2 − α/2π ∈ [1, 2). Como Φ es creciente en m,
m = 2 da una cota válida **para cualquier holonomía**. Consecuencia: el marco de Bishop de K_1 (definido por una
EDO) **no interviene** en la cota; no hace falta integrarlo ni validarlo.

**Independencia de la normalización y de las fases.** (i) Cambiar φ_1 o la normal inicial del marco de K_0
mueve K_1 por una congruencia y una traslación del parámetro: (e^{2is}(1 + r sin(3s+φ)), r cos(3s+φ)) es K_1
con s ↦ s + φ/3 rotada −2φ/3 alrededor de e_z. v_min, κ_max, ν, μ son invariantes por movimientos rígidos y
traslaciones del parámetro. (ii) La normal inicial del marco de K_1 y φ_2 solo cambian la dirección U(t) de la
hebra, que en la Prop. 3.15 se acota por su norma. Así que el resultado vale para **toda** normalización y fase
en las profundidades 1 y 2 (la Def. 2.1 es un caso particular).

**Qué r_2 hay que cubrir.** (H_c) en d = 2 se exige para todo r_2 ≤ f thick(K_1), f ≤ 1/2. Por la Prop. 3.5
(r_1 < 1 = thick(K_0)), thick(K_1) ≤ r_1, así que r_2 ≤ f r_1 ≤ r_1/2. Como Φ crece con r, basta r_2 = f r_1
(familia concreta r_1 = f) o r_2 = r_1/2 (todo f ≤ 1/2 y todo r_1 ≤ f). No se usa ningún valor medido de
thick(K_1).

## 2. K_1 explícita y las cantidades a encerrar

Con K_0(t) = (cos t, sin t, 0), T = (−sin t, cos t, 0), N_0(0) = e_z (proyección de e_z; el marco de Bishop de
un círculo plano es N = e_z, B = T × N = (cos t, sin t, 0), holonomía 0), φ_1 = 0 y t = 2s (periodo 2π):

    K_1(s) = ( e^{2is}(1 + r_1 sin 3s),  r_1 cos 3s ),   es decir   x + i y = e^{2is} + (r_1/2i)(e^{5is} − e^{−is}),

usando sin 3s · e^{2is} = (e^{5is} − e^{−is})/(2i). Las derivadas son exactas:
D_j := d^jK_1/ds^j, (x+iy)^{(j)} = (2i)^j e^{2is} + (r_1/2i)((5i)^j e^{5is} − (−i)^j e^{−is}),
z^{(j)} = r_1 3^j cos^{(j)}(3s). Con v = |D_1|, v v' = D_1·D_2, Π_⊥ = proyección normal:

* κ = |D_1 × D_2| / v³;
* ν_pt = |v'|/v² = |D_1·D_2| / v³ (invariante por reparametrizaciones lineales, como dice el texto);
* vector curvatura κ = Π_⊥D_2 / v²; de K'' = v'T + v²κ y T' = vκ sale K''' = v''T + 3 v v' κ + v² κ', así que
  Π_⊥K''' = 3 v v' κ + v² Π_⊥ κ', luego Π_⊥ dκ/dt = (Π_⊥D_3 − 3 (D_1·D_2) Π_⊥D_2 / v²)/v² y
  μ_pt = |Π_⊥ dκ/dt| / v = |Π_⊥D_3 − 3(D_1·D_2)Π_⊥D_2/v²| / v³
  (en la notación del texto, κ_par' = Π_⊥ dκ/dt, porque d/dt(κ_1N_0 + κ_2B_0) = κ_1'N_0 + κ_2'B_0 − v|κ|² T).

v_min se mide en el parámetro s de periodo 2π, que es el que usa la Def. 2.1 para K_1 (velocidad
v = 2|dK_1/dt|); m también está referido a s (θ_2 = 3s/2 + φ_2). Comprobación en coma flotante (no rigurosa)
contra el cálculo independiente del integrador (`verify_H3.py`, DOP853): v_min = 1.80278, κ_max = 1.39832,
ν = 0.41819, μ = 4.54438 en r_1 = 1/2 — idénticos a 5 cifras.

**Simetría usada en (B).** K_1(s + 2π/3) = R_z(4π/3) K_1(s) exactamente (e^{2i(s+2π/3)} = e^{4πi/3}e^{2is}, y
sin 3s, cos 3s tienen periodo 2π/3). Las cuatro cantidades son invariantes, de modo que el supremo/ínfimo sobre
[0, 2π] coincide con el de [0, 2π/3]. (El script lo comprueba numéricamente: residuo 2·10⁻¹⁵; y el caso (A) se
hace sobre el periodo completo, sin usar la simetría.)

## 3. Método de certificación (qué es riguroso y por qué)

1. **Cajas.** El dominio se cubre por cajas s ∈ [s_j, s_{j+1}] (s_j = 2πj/N, o 2πj/(3N)) × r_1 ∈ [a_i, b_i]
   (extremos binarios exactos, b_i − a_i = 1/1024 en (B); en (A) r_1 es un intervalo de un ulp que contiene
   el decimal 0.5, 0.35 o 0.25). Los extremos s_j se encierran en mpmath.iv, de modo que la unión de las cajas
   contiene [0, 2π] (o [0, 2π/3]) aunque 2π/N no sea representable.
2. **Trigonometría.** cos(ks), sin(ks) (k = 1, 2, 3, 5) sobre cada caja con `mpmath.iv` (aritmética de
   intervalos rigurosa, 80 bits); los extremos se redondean hacia fuera a binary64 (`nextafter`).
3. **Aritmética.** +, −, ×, ÷, √ en numpy binary64 (IEEE 754, redondeo correcto al más cercano) y después un ulp
   hacia fuera en cada extremo (`np.nextafter`): el error de un redondeo al más cercano es < 1 ulp, así que el
   intervalo resultante contiene el valor exacto. Multiplicación por los cuatro productos; división solo por
   intervalos que no contienen 0 (si no, error); cuadrados con cota inferior 0; normas como raíz de suma de
   cuadrados. Es la extensión natural por intervalos (no forma de Taylor): sobreestima en O(ancho de caja), lo
   cual basta porque el margen es grande.
4. **Supremos.** Cota superior de sup κ, sup ν_pt, sup μ_pt = máximo de los extremos superiores sobre todas las
   cajas; cota inferior de v_min = mínimo de los extremos inferiores.
5. **Desigualdad final.** Φ se evalúa en la misma aritmética, en los extremos dados por la monotonía del §1
   (κ, ν, μ, r_2, m = 2 por arriba; v_min por abajo; ζ' por abajo; G(ζ') ≤ g(√2) = 4√2/(3√3) si ζ' ≤ √2 y ≤ g(ζ'_lo)
   si no).

**Base de confianza** (lo que hay que creer además de las demostraciones del manuscrito): que numpy en esta
máquina cumple IEEE 754 para +, −, ×, ÷, √ en binary64 (sin FMA implícita: cada ufunc redondea por separado), que
`mpmath.iv` es correcto, y que el script implementa las fórmulas de arriba (≈ 100 líneas, legibles). Es el
estándar habitual de una "computer-assisted proof" por intervalos; no es una verificación formal.

## 4. Resultados certificados (salida de `certify_d2.py`, 8 s de CPU)

(A) Familia concreta r_1 = f, todo r_2 ∈ (0, f r_1], periodo completo, 4096 cajas en s:

| r_1 = f | v_min ≥ | κ_max ≤ | ν ≤ | μ ≤ | r_2 máx | ε ≤ | ζ' ≥ | r_2 κ_max(K_2) ≤ |
|---|---|---|---|---|---|---|---|---|
| 0.5  | 1.79890 | 1.42634 | 0.43263 | 4.63787 | 0.25   | 0.3566 | 2.3148 | **1.2017** |
| 0.35 | 1.66665 | 1.27523 | 0.41735 | 3.49489 | 0.1225 | 0.1563 | 5.7399 | **0.2446** |
| 0.25 | 1.67273 | 1.17759 | 0.34395 | 2.03430 | 0.0625 | 0.0736 | 12.396 | **0.0891** |

(valores redondeados hacia el lado seguro; los exactos están en `certify_d2.json`). Valores en coma flotante en
una malla de 2·10⁵ puntos (no rigurosos, para ver la holgura del encierro): v_min = 1.80278, κ_max = 1.39832,
ν = 0.41819, μ = 4.54438 (r_1 = 1/2). Repetido sobre [0, 2π/3] con 1366 cajas: 1.1916.

(B) Todo r_1 ∈ (0, 1/2] (512 cajas de ancho 1/1024) × s ∈ [0, 2π/3] (2048 cajas), r_2 = b_i/2 en cada caja:
**max r_2 κ_max(K_2) ≤ 1.1862 < 2**, alcanzado en la última caja r_1 ∈ [0.49902, 0.5]
(v_min ≥ 1.8002, κ_max ≤ 1.4188, ν ≤ 0.4297, μ ≤ 4.5775); la cota crece con r_1 (0.0805 en r_1 ≈ 1/8, 0.224
en 1/4, 0.533 en 3/8).

**Enunciado certificado.** Para el patrón (2,3), todo r_1 ∈ (0, 1/2], todo r_2 ∈ (0, r_1/2], toda fase
φ_1, φ_2 y toda normal inicial de los marcos de K_0 y K_1:

    r_2 κ_max(K_2) ≤ 1.187,  luego  minRad(K_2) ≥ 0.842 r_2 > r_2/2

(el valor exacto de la cota es 1.18616…, de modo que también minRad(K_2) ≥ 0.843 r_2; en el texto se usa 0.842 =
floor(1/1.187) para que el redondeo sea transparente).

Con el Teorema 3.12(c): **thick(K_2) ≥ r_2/2 para todo f ≤ 1/2, toda r_1 ≤ f y toda r_2 ≤ f thick(K_1)**;
es decir, la Hipótesis 3.19 con c = 1/2 vale en d = 1 (demostrado a mano) y en d = 2 (demostración asistida por
computador), sin (H_3) medido en polígonos. Para f = 1/2 y la familia concreta (r_1 = 1/2) también se tiene la
cota ≤ 1.2017 calculada sobre el periodo completo sin simetría.

**Consecuencia para el Corolario 3.20.** En su cadena r_1 = f, ρ_1 = f/2, r_2 = fρ_1 = f²/2 ≤ f thick(K_1)
(porque thick(K_1) ≥ ρ_1 está demostrado). Por lo tanto thick(K_d) ≥ ρ_d y Rop(K_d) ≤ 2πΛ_Rop^d son
**incondicionales para d ≤ 2** (siguen condicionales a (H_c) para d ≥ 3).

**Bono para la Conjetura 3.23 (parte de curvatura) en d = 2.** Con r_2 ≤ f² (familia r_1 = f), r_2 κ_max(K_2) < 1,
es decir minRad(K_2) > r_2, queda certificado para todo f ≤ 0.484375 (cajas de (B) con r_2 = b_i²); con r_2 ≤ r_1/2
cualquiera, para r_1 ≤ 0.47168. En f = 1/2 la cota (1.19) no basta para minRad > r_2 (el cálculo suave NO certificado del integrador,
`verify_H3.py`, da r_2κ_max(K_2) ≈ 0.40 en r_2 = 1/4: la Prop. 3.15 separa los cuatro supremos y usa m ≤ 2, y
pierde un factor ≈ 3; este número no está en `certify_d2.json` y no debe pasar al texto). La
parte de pares doblemente críticos de la conjetura **no** se certifica aquí.

**Holonomía vía torsión (no usada en la cota).** Como κ(K_1) > 0, el marco de Frenet es periódico y el de
Bishop es el de Frenet girado θ(s) = θ(0) − ∫_0^s τ v ds' (de N_0' ∥ T sale θ' = −vτ). Así
α_2 ≡ −∫_0^{2π} τ v ds (mod 2π). En coma flotante: ∫τ dσ = 15.59336 (r_1 = 1/2) → α_2 = −3.02700, igual a la
holonomía de la EDO integrada con DOP853 (−3.0270), y 17.23654 → α_2 = 1.6130 (r_1 = 0.35), −0.79708 → α_2 =
0.7971 (r_1 = 0.25), también iguales. El encierro riguroso por sumas de Riemann con 4096 cajas es demasiado ancho
(∫τ dσ ∈ [14.95, 16.26] en r_1 = 1/2) para mejorar m ≤ 2; se reporta como comprobación, no como certificado útil.
Esta es la "forma cerrada" del marco de Bishop de K_1 (Frenet + ángulo integral de la torsión) que serviría para
certificar d = 3 (véase §6).

## 5. Qué sigue siendo evaluación en malla (sin cambios)

* d ≥ 3: minRad(K_d) ≥ r_d/2 sigue reducido a (H_3)/crecimiento (Cor. 3.16) con ν(K_{d−1}), μ(K_{d−1}) solo
  medidos en polígonos; la Tabla 2 (1/(r κ̂_d) en d = 3) sigue siendo evaluación en malla.
* Los valores refinados c_1 ≈ 0.6117, c_0', δ_turn de la Tabla 2 (los umbrales ≥ 1/2 ya eran analíticos).
* Todo lo poligonal: τ, L/τ, márgenes de la Conjetura 3.23, writhe.

## 6. Ruta concreta para d = 3 (no hecha aquí)

Cor. 3.16 en d = 3 necesita (96/√13)4⁻³ν(K_2) + (64/√13)8⁻³μ(K_2) ≤ 0.896, es decir aprox.
0.416 ν(K_2) + 0.0347 μ(K_2) ≤ 0.896 (polígonos: 0.48). La cota recursiva del Lema 3.14 con los datos
certificados de K_1 da ν(K_2) ≤ 4.2 (no basta). Pero ν(K_2), μ(K_2) en el punto t dependen solo de los datos
locales de K_1 en s (hasta la 4.ª derivada, explícitas), de r_2, de m y del ángulo de U en el plano normal; con
U recorriendo **toda** la circunferencia normal (cajas en el ángulo), m en el intervalo certificado (o [1,2]) y
r_2 en (0, r_1/2], una cuenta de intervalos en cajas (s, ángulo, r_2) daría cotas de ν(K_2), μ(K_2) válidas para
toda normalización sin integrar ninguna EDO; con ellas, el Cor. 3.16 daría (H_c) en d = 3. Coste estimado:
10⁶ cajas, segundos de CPU en numpy; requiere escribir K_2''' en el marco (T, U, W) (ya verificado
simbólicamente en `verify_H3.py` del integrador).

## 7. Barrido conjunto de normalizaciones (Conjetura 3.23)

**Planteamiento.** Girar la normal inicial del marco de Bishop de K_{d−1} un ángulo β equivale a φ_d ↦ φ_d + β
(Def. 2.1), y φ_d + π da la misma curva (p = 2, q impar: se intercambian las hebras). La normalización del marco de
K_0 solo mueve K_1 por una congruencia (§1). Por tanto el margen de d = 3 es una función de (β_1, β_2) ∈ [0, π)²,
β_1 = φ_2 (marco de K_1), β_2 = φ_3 (marco de K_2). `experiments/phase_margin.py` solo barrió β_2 con β_1 = 0.
Margen = (mínima distancia entre pares de vértices doblemente críticos de K_3 que **no** son antipodales de un mismo
disco normal de K_2)/(2 r_3) − 1, en %, con exactamente el censo de `classify_pairs.py` (mismas funciones
importadas). Un margen negativo significaría τ(K_3) < r_3 para esa normalización.

**Protocolo (fijado antes de correr).** Cadena (2,3), f = 1/2, r_d = f τ(K_{d−1}) poligonal (como en el paper).
(1) rejilla gruesa N_0 = 256: β_1 = kπ/18 (18 valores), β_2 = kπ/24 (24 valores); (2) dos refinamientos locales
9 × 9 alrededor del mejor punto, con pasos h/4 y h/16; (3) N_0 = 512 en el minimizador conjunto, en el
minimizador 1-D de `phase_margin.py` (0, 0.4654) y en (0, 0); (4) consistencia: los valores (0, 0) y (0, 0.4654)
de N_0 = 256 se recalculan y se comparan con `results/phase_margin.json`.

**Resultados** (`joint_phase_sweep.py`, 145 s de CPU, salida en `joint_phase_sweep_output.txt` y `.json`):

* Consistencia: (0, 0) → 2.128287 % y (0, 0.4654) → 0.238843 %, idénticos a `phase_margin.json`.
* Rejilla gruesa (432 pares): margen entre 0.2340 % y 13.165 %; mínimo en (β_1, β_2) = (π/3, 0.6545).
  El mínimo sobre β_2 en función de β_1 tiene periodo π/3 (filas k, k+6, k+12 iguales a ≤ 0.049 puntos
  porcentuales, diferencia debida a la rejilla gruesa en β_2): 0.243, 0.332, 0.654, 1.382, 0.673, 0.333 (k = 0..5).
  Es decir, el valle está en β_1 ≡ 0 (mod π/3) — la normalización por defecto de K_1 ya está cerca del peor caso.
* Refinamientos: minimizador conjunto (β_1, β_2) = (1.05811, 0.67086) (≡ β_1 = 0.0109 mod π/3), margen
  **0.2333 %** a N_0 = 256 y **0.2317 %** a N_0 = 512 (convergencia: −0.0016 puntos). Para comparar, el
  minimizador 1-D (0, 0.4654) da 0.2388 % / 0.2329 % (256 / 512) y la normalización por defecto 2.128 % / 2.027 %.
* En las 594 evaluaciones a N_0 = 256 y las 3 a N_0 = 512: τ_3/r_3 = 1 (a 2·10⁻¹⁴), la clase del siguiente par
  es siempre "far" (bases a arco ≥ πτ: el par a través de la curva, no un par local), **ningún margen negativo**.

**Conclusión.** El barrido conjunto **no refuta** la Conjetura 3.23 ni la afirmación numérica f_*(3) ≥ 1/2 para las
normalizaciones probadas: el mínimo conjunto (0.232 % a N_0 = 512) es apenas menor que el mínimo 1-D (0.233 %).
El margen es estrecho pero positivo y estable en N_0. Advertencias: (i) es una rejilla con refinamiento local alrededor
del mejor punto de la rejilla gruesa, no una minimización global certificada; por la periodicidad π/3 en β_1 los otros
valles (β_1 ≈ 0, 2π/3) son copias del refinado (rejilla gruesa 0.243 % y 0.238 %); (ii) el margen es una cantidad
poligonal (pares de vértices) y no está certificado; (iii) solo f = 1/2 (para f = 0.35 los márgenes 1-D son mayores,
véase el texto). La Conjetura 3.23 se refiere a la normalización por defecto; el barrido refuerza la afirmación
"para toda normalización probada" pasando de 20 normalizaciones a 594 pares.

## 8. Cambios propuestos en el manuscrito (detalle en el Bloque B de `d2_certified.tex`)

* Resumen e introducción: d = 2 deja de estar abierto (demostración asistida por computador); thick(K_d) ≥ r_d/2
  demostrado para d ≤ 2.
* Nueva Prop. `prop:d2cert` + Obs. `rem:d2method` tras la Obs. 3.18 (Bloque A, compilado en una copia de main.tex
  en el scratchpad: 14 páginas, sin errores, sin referencias indefinidas ni cajas desbordadas).
* Hip. 3.19: estado "demostrado en d = 1 y (asistido por computador) en d = 2"; párrafo de estado reescrito.
* Cor. 3.20: incondicional para d ≤ 2.
* Tabla de constantes: la columna 1/(rκ̂_d) en d = 2 queda superada por la cota certificada.
* Tabla de afirmaciones: fila nueva (asistido por computador) para d = 2; la fila "abierto" pasa a d ≥ 3; la fila
  del Cor. 3.20 y la de la conjetura se actualizan.
* Limitaciones (1) y (4); Next steps (1) (se elimina la tarea d = 2, se añade la ruta d = 3 del §6) y (2).
* Conj. 3.23 y párrafo de normalizaciones de la Sección 4: margen mínimo conjunto 0.232 % (N_0 = 512) en lugar de
  0.23 % de un barrido 1-D; nada se refuta; parte de curvatura (minRad(K_2) > r_2) demostrada para f ≤ 0.484375.

## 9. Cómputo

`certify_d2.py`: 8 s de CPU. `joint_phase_sweep.py`: 145 s de CPU (+ pruebas de tiempo ≈ 2 s). Total ≈ 2.6 min de
CPU. Sin aleatoriedad. Python 3.11.15, numpy 2.4.6, mpmath 1.3.0.
