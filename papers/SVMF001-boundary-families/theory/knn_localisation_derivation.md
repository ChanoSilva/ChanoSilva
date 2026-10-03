# SVMF001 — Localización por vecinos en el modelo gaussiano: derivación completa

Pendiente 2 de `CONTINUIDAD_SVMF001_20260930.md`: "cota inferior para la localización por vecinos
(kNN-SVM lineal en el modelo gaussiano) en función del tamaño local; extendería la Prop. 3.2
(`prop:thin`) a la familia que realmente se usa". La Obs. 3.3(iii) (`rem:covers`) dice que la
localización por vecinos y las particiones dependientes de los datos no están cubiertas porque sus
submuestras locales no son i.i.d. de P. Aquí se separan dos casos y se demuestra lo que se puede.

Resumen de estados:

| resultado | estado |
|---|---|
| Prop. A: selección que depende solo de coordenadas independientes de (X_1, Y) ⇒ E R = E R_A(K); kNN en esas coordenadas ⇒ E R = R_A(k) | demostrado aquí |
| Lema B: dado el radio del k-ésimo vecino, los k−1 vecinos interiores son i.i.d. de P restringida a la bola | demostrado aquí (argumento clásico de estadísticos de orden) |
| Lema C: el umbral local *poblacional* sobre una ventana simétrica tiene el signo de Bayes | demostrado aquí |
| Teorema D: k fijo, n → ∞, vecindario que incluye la coordenada de señal, umbral de centroides local ⇒ límite R_∞(k) = R* + E[(a−½)(1−a^k+b^k)] > R*, creciente en k ≥ 2, → ½ | demostrado aquí |
| Lema E + Teorema F: SVM lineal local con C fijo y radio < 1/(k√(2Ck)) predice la mayoría; k impar fijo ⇒ límite = riesgo asintótico del voto k-NN > R* | demostrado aquí |
| Observación G: k = ρn, cociente de exceso ≈ 1/(ρ v(μ, r_ρ)) > 1/ρ | heurística de primer orden; verificada numéricamente |

## 0. Modelo y notación

- Y uniforme en {−1, +1}; X_1 | Y ~ N(Yμ, 1); opcionalmente W ∈ R^{d−1} (o cualquier espacio medible),
  independiente de (X_1, Y). η(x) = P(Y = 1 | X = x) = 1/(1 + e^{−2μ x_1}) depende solo de x_1.
  Densidad de X_1: f(x_1) = ½[φ(x_1 − μ) + φ(x_1 + μ)], continua y positiva en todo R.
- Bayes: sgn(x_1), R* = Φ(−μ). Exceso de riesgo de un clasificador g: R(g) − R* = E[|2η(X) − 1| 1{g(X) ≠ sgn(X_1)}].
- a(x) = max(η(x), 1 − η(x)) ∈ [½, 1), b(x) = 1 − a(x); E[b(X)] = R*, E[a(X) − ½] = ½ − R*.
- η es Lipschitz en x_1: η' = 2μ η(1 − η) ≤ μ/2.
- A_nc: umbral t̂ = ½(X̄_+ + X̄_−) sobre X_1, predice +1 si x_1 > t̂; con una sola clase presente predice esa clase.
  Curva exacta R_nc(n) (Prop. 3.4 del manuscrito), estrictamente decreciente para n ≥ 1, R_nc(n) → R*.
- Regla localizada por vecinos: en el punto de prueba x se ajusta A a los k puntos de entrenamiento más
  cercanos (en la métrica que se especifique) y se predice en x. Para la "kNN-SVM" del manuscrito:
  si los k vecinos tienen la misma etiqueta se predice esa etiqueta; si no, SVM lineal (C fijo) sobre ellos.

## 1. Caso no informativo (Prop. A)

**Enunciado.** Sean (X_i, W_i, Y_i), i ≤ n, y (X, W, Y) i.i.d., con W independiente de (X, Y); sea U un
elemento aleatorio auxiliar (desempates, inicializaciones) independiente de todo lo anterior. Sea
I = ι(W_1, …, W_n, W, U) ⊆ {1, …, n} cualquier regla de selección medible y K = |I|. Sea A cualquier regla
de aprendizaje que use solo pares (X, Y). La regla localizada predice A(S_I)(X), S_I = ((X_i, Y_i))_{i∈I}
(en orden de índice). Entonces

  E R(localizada) = E[R_A(K)].

Si R_A es no creciente en {0, …, n}, esto es ≥ R_A(n); es > R_A(n) si P(R_A(K) > R_A(n)) > 0.

**Demostración.** Sea G = σ(W_1, …, W_n, W, U). El bloque B = ((X_i, Y_i)_{i≤n}, (X, Y)) es independiente
de G: dentro de cada par (X_i, W_i, Y_i) la W es independiente de (X_i, Y_i), los pares son independientes
entre sí y U es independiente de todo. Luego, condicionado a G, B tiene su ley incondicional P^{n+1}
(P = ley de (X, Y)). I es G-medible; dado G, S_I son K coordenadas distintas fijas de una muestra i.i.d.
de P, es decir una muestra i.i.d. de tamaño K, independiente de la coordenada (X, Y). Por tanto
P(A(S_I)(X) ≠ Y | G) = E[R(A(S_m))]|_{m=K} = R_A(K) (por el lema de congelamiento / Fubini, porque
(S_I, X, Y) es función medible de B y de I). Tomando esperanza: E R = E[R_A(K)]. Las desigualdades
siguen de K ≤ n. ∎

**Casos particulares.**
1. kNN en W (cualquier métrica, desempates por U): K = k fijo ⇒ E R = R_A(k). Con A = A_nc y 1 ≤ k < n:
   E R = R_nc(k) > R_nc(n), estricto porque R_nc es estrictamente decreciente en n ≥ 1.
2. Celdas de k-means calculadas sobre (W_1, …, W_n) con inicialización U, y el punto de prueba asignado
   a la celda de su centro más cercano en W: K = tamaño (aleatorio) de esa celda; E R = E R_A(K).
3. Prop. 3.2 (`prop:thin`): Z_i función de (W_i, U) con celdas independientes; recupera la identidad
   binomial. Así la Prop. A contiene a la Prop. 3.2 (cuando Z es función de una coordenada W independiente,
   que es la lectura de la Obs. 3.3(i)).

**Lo que no cubre.** Si A usa también W (p. ej. una SVM lineal sobre todas las coordenadas), las W_i
locales están concentradas cerca de W y no se distribuyen como W: la identidad falla y no hay una
comparación general. Tampoco cubre pesos suaves (la mezcla tipo LLSVM).

## 2. Estructura del vecindario kNN (Lema B) y regla local poblacional (Lema C)

**Lema B.** Sea X ∈ R^m con densidad f; (X_i, Y_i) i.i.d.; x fijo; D_i = ‖X_i − x‖ (distintos c.s.);
R = D_(k) (k-ésimo menor), J el índice que lo alcanza, I = {i : D_i < R} (|I| = k − 1 c.s.).
Condicionado a (I, J, R) = (I, j, r), los pares (X_i, Y_i)_{i∈I} son i.i.d. de P_r = P(· | ‖X − x‖ < r)
e independientes de (X_j, Y_j), cuya X_j tiene la ley condicional de X dado ‖X − x‖ = r (densidad
∝ f respecto de la medida de superficie de la esfera) e Y_j | X_j ~ η(X_j).

*Demostración.* Fijados I, j y conjuntos medibles B_i (i ∈ I), condicionando a (X_j, Y_j) = (z, y) con
‖z − x‖ = s, los demás pares son independientes de (X_j, Y_j) y entre sí, así que
P((X_i, Y_i) ∈ B_i ∀i ∈ I, D_i < s ∀ i ∈ I, D_l > s ∀ l ∉ I ∪ {j} | (X_j, Y_j) = (z, y))
= Π_{i∈I} P((X, Y) ∈ B_i, ‖X − x‖ < s) · (1 − F(s))^{n−k}
= Π_{i∈I} P_s(B_i) · F(s)^{k−1} (1 − F(s))^{n−k},
con F(s) = P(‖X − x‖ < s). La dependencia en (z, y) es solo a través de s y factoriza como un producto de
P_s(B_i) por una función de s; integrando contra la ley de (X_j, Y_j) se obtiene la afirmación. ∎

**Consecuencia (k fijo).** Si f es continua y f(x) > 0, en coordenadas reescaladas u = (X − x)/r los
puntos interiores tienen densidad h_r(u) = f(x + r u)/∫_B f(x + r v) dv sobre la bola unidad B, que
converge uniformemente a la uniforme de B cuando r → 0; el punto frontera tiene densidad ∝ f(x + r u)
sobre la esfera unidad, que converge a la uniforme de la esfera (en m = 1: ±1 con probabilidad ½). Por
tanto la distancia en variación total entre la ley de la configuración reescalada U = (D_j/r)_j dado
R = r y la ley límite U^∞ (k − 1 uniformes en B y una uniforme en la esfera, independientes) es
τ(r) ≤ (k − 1) TV(h_r, Unif_B) + TV(frontera_r, Unif_S) → 0. La ley límite es invariante por u ↦ −u.
Además R_n → 0 en probabilidad: P(R_n ≥ ε) = P(Bin(n, F(ε)) < k) → 0 porque F(ε) > 0.

**Lema C (m = 1, umbral poblacional).** Para una ventana simétrica [x − r, x + r] sean
m_±(x) = E[X_1 | Y = ±1, |X_1 − x| ≤ r] y t_r(x) = ½(m_+ + m_−). Entonces sgn(x − t_r(x)) = sgn(x) para
todo x ≠ 0 y todo r > 0, y t_r(0) = 0.

*Demostración.* Sea g(u) la media de N(u, 1) truncada a [−r, r]. g es impar y estrictamente creciente
(familia exponencial: g'(u) = varianza de la truncada > 0). En coordenadas de desplazamiento,
m_+ − x = g(μ − x) y m_− − x = g(−μ − x) = −g(μ + x). Luego
x − t_r(x) = ½[g(μ + x) − g(μ − x)], que tiene el signo de x. ∎

Lectura: la regla local *poblacional* (medias de clase locales exactas) es exactamente la regla de Bayes,
para cualquier tamaño de ventana. La localización informativa no introduce sesgo de aproximación en el
signo de la decisión; todo lo que gane o pierda es estimación (coherente con el Lema 3.1, `lem:approx`).

## 3. Caso informativo, k fijo y n → ∞

### 3.1 Umbral de centroides local (Teorema D)

**Enunciado.** X = (X_1, W) ∈ R^m (m = d ≥ 1, W ~ N(0, I) independiente; m = 1 es "vecindario solo en la
coordenada de señal"); vecindario de los k más cercanos en distancia euclídea en R^m; A_nc sobre X_1.
Para k ≥ 1 fijo, cuando n → ∞,

  E R_n → R_∞(k) := E[ η^k(1 − η) + (1 − η)^k η + ½(1 − η^k − (1 − η)^k) ](X)
        = R* + E[(a(X) − ½)(1 − a(X)^k + b(X)^k)].

Además R_∞(1) = R_∞(2) = E[2η(1 − η)] > R* (límite de Cover–Hart del 1-NN), R_∞ es estrictamente
creciente en k ≥ 2 y R_∞(k) → ½ cuando k → ∞.

**Demostración.**
1. *Forma de la regla.* Con desplazamientos D_j = X_{(j)} − x, t̂ = x_1 + S con
   S = ½(media de D_{j,1} sobre los positivos + media sobre los negativos). En vecindario mixto se predice
   +1 sii x_1 > t̂ sii S < 0. S es homogénea de grado 1: S(D) = r S(U). Así la predicción es una función
   ψ(L, U) de las etiquetas L y la configuración reescalada U, invariante por permutaciones de los pares
   (L_j, U_j).
2. *Etiquetas.* Dadas todas las X, las Y son independientes con P(Y_i = 1) = η(X_i). Las etiquetas de los
   vecinos tienen ley producto de Bernoulli(η(x + D_j)), a distancia en variación total
   ≤ Σ_j |η(x + D_j) − η(x)| ≤ k(μ/2) R de la ley producto L' de Bernoulli(η(x)) independiente de todo.
3. *Posiciones.* Por el Lema B, dado R = r, |E[ψ(L', U) | R = r] − E[ψ(L', U^∞)]| ≤ τ(r).
4. Sea π_n(x) = P(predicción = +1 en x). Entonces
   |π_n(x) − E ψ(L', U^∞)| ≤ E[min(1, kμR_n/2)] + E[min(1, τ(R_n))] → 0 porque R_n → 0 en probabilidad.
5. *Límite.* Si L' es pura, ψ es su etiqueta: probabilidades η^k y (1 − η)^k. Si L' es mixta (k ≥ 2),
   S(L', −U) = −S(L', U), U^∞ y −U^∞ tienen la misma ley e independiente de L', y P(S(L', U^∞) = 0) = 0
   (hay al menos un punto interior, cuya primera coordenada es continua, con coeficiente no nulo);
   luego P(S < 0) = ½. Así π_∞(x) = η^k + ½(1 − η^k − (1 − η)^k).
6. *Riesgo.* La etiqueta de prueba es independiente del entrenamiento dado X, así que
   E R_n = E[π_n(X)(1 − η(X)) + (1 − π_n(X)) η(X)] → E[π_∞(1 − η) + (1 − π_∞)η] por convergencia dominada.
   Desarrollando, el error condicional límite es η^k(1−η) + (1−η)^k η + ½ q, q = 1 − η^k − (1−η)^k.
7. *Identidad.* Con a ≥ ½ (el caso a = 1 − η es simétrico): error − b = a^k b + b^k a + ½ − ½a^k − ½b^k − b
   = (½ − b)(1 − a^k) + b^k(a − ½) = (a − ½)(1 − a^k + b^k), usando ½ − b = a − ½.
8. *Propiedades.* k = 1: (a − ½)·2b ⇒ error = 2ab. k = 2: a² − b² = a − b ⇒ igual que k = 1.
   a^{k+1} − b^{k+1} − (a^k − b^k) = ab(b^{k−1} − a^{k−1}) < 0 para k ≥ 2 y a ∈ (½, 1), así que
   1 − a^k + b^k es estrictamente creciente en k ≥ 2; a < 1 para todo x, luego a^k, b^k → 0 y por
   convergencia dominada R_∞(k) → R* + E[a − ½] = ½. R_∞(1) − R* = E[(a − ½)2b] > 0 porque a > ½ y b > 0
   salvo en x_1 = 0. ∎

**Corolario D'.** Para cada k fijo existe n_0(k) tal que E R_n(localizada) > R_nc(n) para todo n ≥ n_0(k)
(porque R_nc(n) → R* < R_∞(k); R_nc(n) → R* por convergencia dominada en la fórmula de la Prop. 3.4, ya
que N_± → ∞ c.s.). No se da n_0 explícito; numéricamente la desigualdad ya se cumple en n = 320 (§5).

Lectura del mecanismo: con k fijo el vecindario se encoge a un punto; las dos medias de clase locales
tienden ambas a x y el umbral local deja de contener información: en vecindarios mixtos la decisión es
una moneda. Los vecindarios puros (más frecuentes lejos de 0) predicen la etiqueta presente, que coincide
con Bayes con probabilidad a^k.

### 3.2 SVM lineal local (Lema E, Teorema F)

**Lema E (determinista).** Sean z_j = x + D_j ∈ R^m, j ≤ k, con ‖D_j‖ ≤ r, etiquetas y_j con mayoría
estricta (n_+ ≠ n_−) y (ŵ, b̂) cualquier minimizador de F(w, b) = ½‖w‖² + C Σ_j max(0, 1 − y_j(⟨w, z_j⟩ + b)).
Si r < r_0(k, C) := 1/(k √(2Ck)), entonces sgn(⟨ŵ, x⟩ + b̂) es la etiqueta mayoritaria.

*Demostración.* Reparametrizar b' = b + ⟨w, x⟩: F = ½‖w‖² + C Σ hinge(y_j(⟨w, D_j⟩ + b')), y la predicción
en x es sgn(b'). Supongamos mayoría positiva (el otro caso es simétrico). (i) F(ŵ, b̂') ≤ F(0, 0) = Ck,
luego ‖ŵ‖ ≤ √(2Ck). (ii) min F ≤ F(0, 1) = 2C n_−. (iii) Como la bisagra es 1-Lipschitz,
F(w, b') ≥ G(b') − C k r ‖w‖ con G(b') = C Σ hinge(y_j b'). (iv) Para b' ≤ 0, G(b') ≥ C k:
en [−1, 0], G = C[n_+ + n_− + b'(n_− − n_+)] ≥ Ck; para b' < −1, G = C n_+(1 − b') ≥ 2C n_+ > Ck.
(v) Si b̂' ≤ 0: Ck − Ckr√(2Ck) ≤ F(ŵ, b̂') ≤ 2Cn_−, es decir n_+ − n_− ≤ k r √(2Ck) < 1, contradicción con
n_+ − n_− ≥ 1. Luego b̂' > 0 y se predice +1. ∎

**Teorema F.** Mismo modelo, vecindario euclídeo en todas las coordenadas que usa la SVM (m = 1: solo
la señal), k impar fijo, regla kNN-SVM del manuscrito (vecindario puro ⇒ su etiqueta; si no, SVM lineal
con C fijo). Cuando n → ∞,

  E R_n → R_∞^{voto}(k) := R* + E[(2a(X) − 1) P(Bin(k, a(X)) < k/2)] > R*,

el riesgo asintótico de la regla de la mayoría de k vecinos; R_∞^{voto}(k) → R* cuando k → ∞ (ley de
los grandes números y convergencia dominada).

*Demostración.* En el evento R_n < r_0 la predicción es la mayoría local (Lema E; si el vecindario es puro
también). P(R_n ≥ r_0) → 0. Por el paso 2 de la demostración del Teorema D, la ley de las etiquetas locales
está a distancia ≤ E min(1, kμR_n/2) → 0 de Bin(k, η(x)) independiente. Luego
P(pred = +1 | X = x) → P(Bin(k, η(x)) > k/2) y, como en el paso 6, el exceso condicional tiende a
(2a − 1) P(Bin(k, a) < k/2), positivo para a ∈ (½, 1). ∎

Comentario: el Teorema F explica por qué la kNN-SVM con C fijo y k pequeño "degenera a un voto de
vecinos" (lo que el manuscrito decía como observación en D1): es exacto en cuanto el radio del vecindario
baja de r_0. Comparación con la SVM lineal global: el teorema da el límite local; que la SVM global
converja a R* en este modelo no se demuestra aquí, así que la comparación con ella es numérica (§5).
Con la regla global de centroides (de la misma clase lineal) la comparación es la del Corolario D'.

## 4. k = ρn (Observación G; heurística de primer orden, m = 1, A_nc)

Con k = ρn, la ventana kNN en x ≈ 0 converge a [−r_ρ, r_ρ], con P(|X_1| ≤ r_ρ) = ρ, es decir
Φ(r_ρ − μ) + Φ(r_ρ + μ) − 1 = ρ. Por el Lema C el umbral poblacional tiene el signo correcto, así que la
regla es consistente; la pregunta es la constante. Desarrollo:
- pendiente: x − t(x) ≈ c x con c = g'(μ) = v(μ, r_ρ) := Var(N(μ, 1) truncada a [−r_ρ, r_ρ]);
- ruido: dado el radio, los k − 1 interiores son i.i.d. de la ventana (Lema B); cerca de 0 hay ≈ ρn/2
  de cada clase, así que Var(t̂) ≈ ¼(2 v/(ρn/2)) = v/(ρn);
- exceso ≈ ∫ |2η − 1| f P(error) dx ≈ μ f(0) ∫ |x| Φ(−c|x|√(ρn/v)) dx = μ φ(μ) v/(2 ρ n v²)
  (usando |2η(x) − 1| ≈ μ|x|, f(0) = φ(μ) y ∫_R |x| Φ(−|x|/s) dx = s²/2).
- La regla global (ρ = 1, v = 1) da μφ(μ)/(2n), que coincide con el desarrollo del Cor. 3.5.

Cociente de primer orden: Q(ρ) = 1/(ρ v(μ, r_ρ)). Como el truncamiento de una normal a un intervalo
reduce la varianza (v < 1; lo compruebo numéricamente en los valores usados), Q(ρ) > 1/ρ, que es el
factor de una partición sin información de tamaño local ρn (Prop. 3.2 con M = 1/ρ). Para ρ pequeño,
r_ρ ≈ ρ/(2φ(μ)), v ≈ r_ρ²/3 y Q ≈ 12 φ(μ)²/ρ³; trasladado a k = ρn, el exceso es ≈ 6 μ φ(μ)³ n²/k³, que
solo es pequeño si k ≫ n^{2/3}. Estado: heurística (no se controlan los términos de segundo orden: radio
aleatorio, proporciones de clase desiguales en x ≠ 0, punto frontera); se contrasta con Monte Carlo en §5.

## 5. Verificación numérica

Script: `theory/check_knn_localisation.py` (semilla 20261003, un hilo BLAS, 129 s de CPU), salida en
`theory/check_knn_localisation_output.txt`, números en `theory/knn_localisation_results.json`
(clave `macros`: las macros `\KL...` que usa `knn_localisation.tex`; se regeneran con
`python check_knn_localisation.py --macros > ../manuscript/knn_numbers.tex`). Todas las cifras de
esta sección se copian de esa salida. μ = 1.645 (el del manuscrito, R* = 0.0500) y μ = 0.5 (R* = 0.3085).

- **[C] Constantes exactas** (cuadratura). Límite k fijo del centroide local R_∞(k), μ = 1.645:
  0.0743 (k = 1 = k = 2), 0.0815 (3), 0.0953 (5), 0.1202 (10), 0.1507 (20), 0.2356 (100), 0.3601 (1000):
  creciente hacia ½ como dice el Teorema D. Límite de la SVM local (= voto k-NN): 0.0743 (1), 0.0599 (3),
  0.0561 (5), 0.0534 (9), 0.0515 (21), 0.0506 (51), decreciente hacia R*. Global exacto R_nc(n):
  0.05025 (n = 320), 0.05003 (2000), 0.04999 (20000).
- **[L] Lema C**: signo correcto del umbral poblacional en 1920 pares (x, r) (x ∈ [−4, 4], r de 0.01 a 5,
  ambos μ).
- **[P1] Prop. A** (vecindario kNN en W ∈ R², 1000 muestras de entrenamiento × 100 puntos de prueba; riesgo
  exacto dado el umbral): en los 14 casos con 1 < k ≤ n el Monte Carlo coincide con R_nc(k) exacto con
  |z| ≤ 1.4 (p. ej. μ = 1.645, n = 320, k = 20: 0.054474 ± 0.000041 frente a 0.054460). Cocientes exactos de
  exceso frente a k = n = 320: 4.04 (k = 80), 16.8 (k = 20), 176 (k = 5). SVM lineal sobre X_1 (C = 1),
  n = 320: localizada 0.07485 ± 0.00062 frente a la curva 0.07421 ± 0.00051 (k = 10) y 0.05557 ± 0.00013
  frente a 0.05562 ± 0.00009 (k = 40). Nota de honestidad: en una primera corrida con 60 muestras de
  entrenamiento la comparación SVM en k = 40 dio z = −4.0; un diagnóstico con 600/6000 repeticiones
  (0.05552 ± 0.00013 frente a 0.05551 ± 0.00010) mostró que el riesgo por ajuste tiene cola pesada
  (percentil 99.9 ≈ 0.112, máximo 0.135) y que 60 repeticiones subestiman el error estándar; se
  aumentaron las repeticiones (600 y 8000) antes de fijar los números.
- **[P2] Teorema D**, d = 1, 200 muestras por caso, exceso por cuadratura en x: en n = 20000 el riesgo está a
  ≤ 1.3 errores estándar de R_∞(k) para k ≤ 5 (ambos μ), y a ≤ 0.0023 en valor absoluto para k ≤ 20 (el
  mayor desvío, μ = 0.5 y k = 20, 0.4896 frente a 0.4919, se acerca monótonamente al límite al crecer n:
  0.4203, 0.4739, 0.4896 para n = 320, 2000, 20000). En los 36 casos (n ∈ {320, 2000, 20000}, k ≤ 20) el
  riesgo localizado supera a R_nc(n) en al menos 0.024. Vecindarios en todas las coordenadas (d = 2 y 5,
  n = 2000, k ∈ {3, 10}): riesgos entre 0.076 y 0.109, por debajo del límite (en d > 1 los vecindarios se
  encogen como n^{−1/d}) y muy por encima del global 0.0500.
- **[P3] Teorema F**, d = 1, SVM local C = 1, 25 × 400 consultas: la predicción coincidió con la mayoría
  local en el 100 % de las consultas en todos los casos, y en las 6646 consultas mixtas con radio < r_0 (el
  caso del Lema E). Riesgos en n = 2000: 0.0725 ± 0.0013 (k = 1; límite 0.0743), 0.0606 ± 0.0010 (k = 3;
  0.0599), 0.0561 ± 0.0008 (k = 5; 0.0561), 0.0531 ± 0.0004 (k = 9; 0.0534); SVM lineal global:
  0.05072 ± 0.00006 (n = 320) y 0.05010 ± 0.00001 (n = 2000). Peor que la global en todos los casos.
- **[P4] Observación G**, k = ρn, 600 muestras, exceso por cuadratura fina cerca de 0. Cociente de exceso
  frente al global exacto (Q heurístico entre paréntesis): μ = 1.645, ρ = ½: 5.53 ± 0.31, 5.68 ± 0.33,
  6.12 ± 0.33 para n = 2000, 8000, 32000 (Q = 5.61); ρ = ¼: 210 ± 19, 65 ± 16, 19.1 ± 1.1 (Q = 20.3);
  μ = 0.5, ρ = ½: 11.5 ± 0.6, 11.1 ± 0.6, 12.2 ± 0.7 (Q = 11.4); ρ = ¼: 88 ± 4, 88 ± 4, 84 ± 5 (Q = 94.4).
  Control ρ = 1 (que es exactamente la regla global, cociente 1): entre 0.89 ± 0.06 y 1.04 ± 0.07, lo que
  da la escala del error de Monte Carlo de este estimador (~10 %). Lectura: la heurística acierta el orden y,
  en n = 32000, el valor dentro de ~2 errores estándar (o ~11 % en μ = 0.5, ρ = ¼); en μ = 1.645, ρ = ¼, el
  régimen de primer orden solo se alcanza en n = 32000 (en n = 2000 el cociente es 10 veces Q). No analicé
  dónde se concentran esos errores adicionales; los términos de segundo orden no se controlan.

## 6. ¿Puede ayudar la localización informativa?

En este modelo y con estas dos reglas base, no en ningún régimen examinado:
- k fijo: inconsistente (límite > R*, Teoremas D y F), peor que la regla global para n grande (Corolario
  D'), y numéricamente ya en n = 320.
- k = ρn: consistente (Lema C), pero el exceso se multiplica, a primer orden, por 1/(ρv) > 1/ρ: peor
  que una partición sin información del mismo tamaño local.
- Lo que sí aparece es que la SVM local con C fijo se comporta mucho mejor que el centroide local para k
  pequeño (voto de mayoría frente a moneda), lo cual es un efecto de la regla base, no de la localización.
Esto es coherente con el Lema 3.1: el modelo tiene frontera de Bayes lineal, la clase global ya contiene a
Bayes y además la regla local poblacional es Bayes (Lema C), así que solo queda el término de estimación,
y localizar reduce el tamaño efectivo. No se afirma nada fuera de este modelo: con fronteras curvas (los
conjuntos multiescala del manuscrito) el término de aproximación de la referencia lineal es positivo y la
localización sí puede reducirlo (la Tabla 7 del manuscrito lo mide frente a la SVM lineal).

Qué queda abierto:
1. Versión rigurosa de la Observación G (k = ρn, y en general k → ∞ con k/n → 0; la heurística sugiere que
   el centroide local solo es consistente si k ≫ n^{2/3}) y una cota inferior no asintótica explícita en n
   (no se da n_0(k) en el Corolario D').
2. La SVM lineal local que usa coordenadas fuera de la métrica del vecindario (p. ej. vecinos en W pero SVM
   en todas las coordenadas): ni la Prop. A ni el Teorema F la cubren.
3. Celdas de k-means formadas en la coordenada de señal y la mezcla de pesos suaves (LLSVM).
4. Comparación con la SVM lineal global: requiere su consistencia en el modelo (no demostrada aquí; la
   monotonía de su curva ya era una hipótesis comprobada numéricamente en el manuscrito).
5. El Teorema F supone C fijo; con C elegido por validación interna (como en el experimento real para
   otras familias) no se ha analizado.

## 7. Cambios propuestos al manuscrito

Detallados en la cabecera de `theory/knn_localisation.tex` (con los números de línea de main.tex v0.3):
1. Sustituir el párrafo "Rules not covered by the proposition." (main.tex:158) por el bloque nuevo:
   Prop. `prop:select`, Cor. `cor:knnfree`, Lemas `lem:radius`, `lem:popsign`, `lem:majority`, Teorema
   `thm:kfixed`, Cor. `cor:kfixed`, Obs. `rem:rho`.
2. Obs. 3.3(iii) (`rem:covers`): la localización por vecinos y las particiones dependientes de los datos
   quedan cubiertas cuando se forman en coordenadas sin información (Prop. `prop:select`); con la
   coordenada de señal, límite k fijo (Teorema) y heurística para k = ρn.
3. Tabla de afirmaciones: fila 1 con la extensión a `prop:select`; nueva fila "proved here" para
   `thm:kfixed`/`lem:popsign`; la fila "verified, not proved" incluye los límites alcanzados en n = 20000 y
   la heurística 1/(ρv).
4. Introducción (Scope), Limitaciones, Próximos pasos (a) y Apéndice B (D1 y nuevo D5–D7).
5. Opcional: una frase en el resumen.
6. Esta nota (`CONTINUIDAD_SVMF001_20260930.md`), pendiente 2: "hecho en parte (theory/knn_localisation.tex):
   cubierto el caso no informativo (identidad exacta) y el límite k fijo en la coordenada de señal para
   el centroide local y la kNN-SVM con C fijo; abierto: k = ρn riguroso, n_0 explícito, SVM con
   coordenadas fuera del vecindario, k-means en la coordenada de señal".
7. `make_numbers.py`/build: añadir `\input{knn_numbers.tex}` generado por
   `python theory/check_knn_localisation.py --macros`.

Compilación de prueba: copia de main.tex en el scratchpad con los siete cambios aplicados; pdflatex +
bibtex + 2 × pdflatex sin errores, sin referencias ni citas indefinidas; 16 páginas (v0.3: 14). El
bloque añade unas dos páginas; si se quiere recortar, las demostraciones de los Lemas `lem:radius`,
`lem:majority` y del Teorema pueden ir a un apéndice.
