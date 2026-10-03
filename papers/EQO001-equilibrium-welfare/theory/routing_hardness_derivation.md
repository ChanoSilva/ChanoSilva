# Pregunta 7.1 (EQO001 v0.3): dureza de λ ∈ Λ(f*) en ruteo multimercancía con costos afines

Derivación incremental. Notación de main.tex: C_k(f)=Σ_{p∈P_k} f_p c_p(f) = Σ_e c_e(f_e) f_e^k,
Φ_λ = Σ_k λ_k C_k (minimizar; W_λ = −Φ_λ), Λ(f*) = {λ ≥ 0 : f* ∈ argmin_K Φ_λ}.
Modelo: el de la Definición def:wardrop (conjuntos de rutas P_k dados explícitamente; cada ruta es un conjunto de aristas).

## Paso 0. Forma de Φ_λ y de dónde sale la no convexidad

Con c_e(x)=a_e x+b_e: Φ_λ(f) = Σ_e (a_e f_e + b_e) g_e, con g_e = Σ_k λ_k f_e^k (flujo ponderado en e).
* Si en cada arista todos los usuarios tienen el mismo peso μ_e, g_e = μ_e f_e y Φ_λ = Σ_e μ_e(a_e f_e² + b_e f_e) es convexa: λ ∈ Λ ⇔ λ ∈ Λ₁ (test lineal). Ejemplo: λ = 1 (óptimo del sistema).
* Para dos mercancías con pesos λ_i ≠ λ_j en una arista compartida, el término a_e(y_i+y_j)(λ_i y_i+λ_j y_j) tiene hessiano de determinante −a_e²(λ_i−λ_j)² < 0. La no convexidad requiere pesos distintos.
* Observación clave: si λ_h = 0, f^h sólo entra en f_e (no en g_e). Luego **Φ_λ es afín en los flujos de las mercancías con λ_h = 0**, conjuntamente, para flujos fijos de las ponderadas. No hay productos entre dos mercancías de peso cero.

## Paso 1. Lema de concavidad (general)

Sea Q = supp(λ) y R = el resto. Para flujos f^Q fijos, Φ_λ es afín en f^R. Por tanto
h(f^R) = min_{f^Q} Φ_λ(f^Q, f^R) es un ínfimo de funciones afines: **cóncava** en f^R, y su mínimo sobre el producto de símplices de R se alcanza en un vértice (cada mercancía de R en una sola ruta).
Si además λ = μ·1_Q (pesos iguales en Q), Φ_λ es convexa en f^Q para f^R fijo (Σ_e (a_e(g_e+r_e)+b_e) g_e con g = μ·flujo de Q). Entonces
  min_K Φ_λ = min sobre perfiles puros de R (sólo cuentan las mercancías de R que comparten arista con Q) de un QP convexo.
Consecuencia (algoritmo): para λ = e_W y un número acotado de mercancías que comparten aristas con W (rutas explícitas), decidir λ ∈ Λ es polinomial (Π|P_k| QPs convexos, cada uno polinomial: Kozlov–Tarasov–Khachiyan). La dureza tiene que venir de muchas mercancías de peso cero.

## Paso 2. Gadget mediador (una mercancía ponderada ve un corte)

Una sola mercancía ponderada W (λ = e_W) con una ruta "O" de costo constante y una ruta T_m por cada arista orientada m=(i→j) del grafo.
T_m pasa por e1_m (compartida con la ruta S_i del nodo i), e2_m (compartida con la ruta P_j del nodo j) y ez_m (compartida con la ruta Z1 del interruptor z).
Variables reducidas: x_i = flujo del nodo i en S_i (1−x_i en P_i), z = flujo del interruptor en Z1, t_m = flujo de W en T_m.
Costos: e1_m, e2_m: α_m x; ez_m: 2α_m x; p_m (privada de T_m): constante β_m = b_o − α_m; o: constante b_o = max_m α_m; dz (primera arista de toda ruta de W, y de Z0): a_D x.
Entonces (demanda de W = D, de nodos y z = 1)
  C_W = a_D D (D+1−z) + b_o D + Σ_m α_m [ 4 t_m² + t_m (x_i − x_j + 2z) ].
(Comprobación: t_m[β_m − b_o + α_m(t+x_i) + α_m(t+1−x_j) + 2α_m(t+z)] = α_m[4t² + t(x_i−x_j+2z)].)
Mínimo en t_m ≥ 0: t_m = (x_j−x_i−2z)_+/8 ≤ 1/8, valor −(α_m/16)((x_j−x_i−2z)_+)². Con D ≥ M/8 la restricción Σt ≤ D no está activa.
  h(x,z) = a_D D(D+1−z) + b_o D − Σ_{m=(i→j)} (α_m/16) ((x_j − x_i − 2z)_+)².
Con α_m = 16 w_ij y vértices: z=1 ⇒ h = C* := a_D D² + b_o D (para todo x, incluso no entero: x_j−x_i−2 ≤ −1).
z=0 ⇒ h = C* + a_D D − Σ_{m=(i→j)} w_ij [x_i=0, x_j=1] = C* + a_D D − cut_w(x).
Por el Paso 1, h es cóncava en (x,z) (de hecho C_W es afín en (x,z) para t fijo, explícito arriba), así que
  min_K C_W = min( C*, C* + a_D D − maxcut_w ).
Con a_D D = k − 1/2: f* = (x=0, z=1, t=0) minimiza C_W ⇔ maxcut_w ≤ k − 1/2 ⇔ maxcut_w < k.

## Paso 3. Que f* sea el (único) equilibrio de Wardrop, y Λ₁ = ortante

Rutas privadas de nodos y z (no afectan a C_W porque W no las usa): s_i: x + B (en S_i), r_i: x (en P_i), q1: x (en Z1), q0: x + B_z (en Z0 = {q0, dz}).
B = B_z = 2 + 2(D+1) Σ_m α_m.
* Dominancia estricta: costo(P_i) ≤ 1 + (D+1) Σ α < B ≤ costo(S_i); costo(Z1) ≤ 1 + 2(D+1)Σα < B_z ≤ costo(Z0). En todo equilibrio x=0, z=1.
* Dado x=0, z=1: costo(T_m) − costo(O) = α_m(t+0) + α_m(t+1) + 2α_m(t+1) + β_m − b_o = 4α_m t_m + 2α_m > 0. En todo equilibrio t = 0. **f* es el único equilibrio de Wardrop** (en flujos de ruta).
* Todas las pendientes son > 0 salvo o y p_m (constantes). Cada ruta distinta de O tiene una arista de pendiente positiva que la identifica (s_i, r_i, q1, q0; T_m vía e1_m una vez fijado h_{S_i}=0), y h_O = −Σ h_{T_m}: el jacobiano Δᵀdiag(a)Δ es definido positivo en el espacio tangente, **F es fuertemente monótono en K**.
* e_W ∈ Λ₁(f*): derivadas de C_W en flujos de ruta en f*: O: 2a_D D + b_o; T_m: 2a_D D + b_o + 2α_m (≥, no usada); S_i, P_i: 0 y 0 (iguales); Z1: 0 (usada), Z0: a_D D (≥, no usada). KKT de minimización ✓.
* e_i ∈ Λ(f*): C_i ≥ σ_i(1−x_i)² + B x_i con σ_i = 1 + Σ_{m∈in(i)} α_m = C_i(f*); y σ(1−x)²+Bx−σ = x(σx − 2σ + B) ≥ 0 si B ≥ 2σ_i ✓.
* e_z ∈ Λ(f*): C_z ≥ σ_z z² + B_z(1−z), σ_z = 1 + 2Σα = C_z(f*); diferencia (1−z)(B_z − σ_z(1+z)) ≥ 0 si B_z ≥ 2σ_z ✓ (D ≥ 1).
* Λ ⊆ Λ₁, Λ₁ cono convexo que contiene a todos los e_k ⇒ Λ₁ = ortante. Y Λ = Λ₁ ⇔ e_W ∈ Λ ⇔ maxcut_w < k.

## Paso 4. Tamaño y pertenencia a co-NP

D = M = 2|E|, α_m = 16 w_ij, b_o = 16 w_max, β_m = 16(w_max − w_ij), a_D = (2k−1)/(2D), B = B_z = 2 + 2(D+1)·16·2W_tot: todo racional de tamaño polinomial; n+2 mercancías, 5M + 2n + 4 aristas (contando o, dz, q0, q1).
Pertenencia: el argumento de la Prop. prop:hard (cara de K, politopo de puntos estacionarios, vértice de tamaño polinomial; Vavasis 1990) vale para un poliedro K cualquiera dado por desigualdades, y aquí K es producto de símplices con descripción explícita. Para Λ ≠ Λ₁: rayo extremo de Λ₁ (poliédrico, datos racionales) + testigo.

**Resultado:** decidir λ ∈ Λ(f*) en ruteo de Wardrop multimercancía con costos afines (rutas explícitas) es co-NP-completo; también decidir Λ(f*) = Λ₁(f*). La dureza persiste con λ vector unitario, f* único equilibrio, F fuertemente monótono, Λ₁(f*) = ortante, cada arista compartida por a lo sumo dos mercancías, todas las mercancías salvo una con exactamente dos rutas, demandas enteras.

## Paso 5. Realización como red (P_k = todas las rutas s_k–t_k de un DAG)

DAG por niveles: nivel 0 = dz, o, p_m; nivel 1 = e1 (cadenas S_i); nivel 2 = e2 (cadenas P_j); nivel 3 = ez (cadena Z1).
Conectores: W sube de nivel (dz→p_m→e1_m→e2_m→ez_m→t_W; dz→o→t_W); las cadenas de nodos y de z se quedan en su nivel; conectores internos de cadena con costo constante H_c > b_o.
* Nodo i: desde S_i (nivel 1) sólo puede saltar a W hacia e2_m en la cadena P_j (j ≠ i) y no puede volver; desde P_i sólo a nivel 3. ⇒ exactamente dos rutas s_i–t_i.
* W: toda ruta s_W–t_W distinta de O y T_m usa un conector interno ajeno (costo H_c). Mover su flujo a O baja C_W en ≥ δ(H_c − b_o) > 0 (c(f)g − c(f−δ)(g−δ) ≥ δ c(f−δ)).
* z: rutas extra = q0 → dz → (rama de W) → ... → cadena Z1 → t_z. Contienen q0 (costo ≥ B_z, no se usan en equilibrio) y cargan dz más aristas de W: dominadas por Z0 para C_W (los costos son no decrecientes).
* Los conectores internos suman (deg(i)−1)H_c a ambas rutas del nodo i (igual), y (M−1)H_c a Z1: B_z se aumenta en 2(M−1)H_c.
⇒ mismo min_K C_W, mismo C_W(f*), f* único equilibrio. (Sin fuerte monotonía: las rutas mixtas de z no se distinguen por aristas de pendiente positiva.)

## Paso 6. Verificación numérica

Ver theory/check_routing_hardness.py y su salida (se registra abajo al terminar).
