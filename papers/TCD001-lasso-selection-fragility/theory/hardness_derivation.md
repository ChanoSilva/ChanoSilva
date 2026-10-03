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

Estado: DEMOSTRADO; verificación exhaustiva exacta en §3 (312/312). Texto final: hardness_p2.tex (Lema lem:entry, Teorema thm:enter2).

Nota sobre las condiciones: u^2 > N es SUFICIENTE (el término −(1−ρ)μ' da holgura extra); κ−ρ ≤ 1/B es lo
que impide la entrada con signo negativo cuando Σb ≫ t (c_2 sigue bajando tras activarse la variable 1);
ρ < 1 solo sirve para que también los D∖R sin gadget tengan minimizador único (con ρ = 1 son no únicos y,
por la Def. 2.2, no son testigos; el teorema seguiría valiendo pero sería menos robusto).

Lo que NO funciona (registrado para no repetirlo): (i) columnas con soporte disjunto ⇒ el Lasso se
desacopla y "entra" vuelve a ser p = 1 (fácil); (ii) un solo gadget con s0 no entero bajo la regla P sin
desplazar los y_i: Δ ∈ s0 + ℤ y la condición de absorción Δ_min·u²/(u²+N) > s0 falla; el desplazamiento
y_i = b_i + λ con λ = μ/n hace que μ' = λ|K| se cancele exactamente con λN y deja Δ = β − t ∈ ℤ.

## 2. Algoritmo pseudo-polinómico para p fijo (todas las metas, ambas reglas)

Observación: el objetivo en D∖R es ½β^T G_K β − g_K^T β + const + μ'||β||_1 con G_K = X_K^T X_K,
g_K = X_K^T y_K. El conjunto de minimizadores (y por tanto unicidad, soporte con signo y cualquier meta
Π ∈ {any (con/sin signo), leave(j), enter(j)}) depende solo de (G_K, g_K, μ'), y μ' depende solo de |K|.
Unicidad decidible desde (G, g, μ'): β̂ cualquiera (enumeración de 3^p soportes con signo para p fijo);
minimizadores = {β : G(β − β̂) = 0, ||β||_1 ≤ ||β̂||_1} (Gv = 0 ⇔ X_K v = 0); 2p PL.
Datos enteros |x_ij|, |y_i| ≤ M: las entradas de (G_K, g_K) son enteros en [−nM², nM²].
DP: recorrer las filas manteniendo el conjunto de estados alcanzables (|K|, triu(G_K), g_K);
#estados ≤ (n+1)(2nM²+1)^{d}, d = p(p+3)/2; cada paso O(d·#estados); al final evaluar Π en cada estado con
1 ≤ |K| ≤ n−1; f_Π = n − max{|K| : Π se cumple con minimizador único}.
Tiempo: O(c_p · n² (2nM²+1)^{p(p+3)/2}) operaciones sobre números de O(p log(nM) + bits(μ)) bits, c_p
dependiente solo de p. ⇒ Para p fijo, existencia de testigo y f_Π son pseudo-polinómicos ⇒ ninguna de
estas variantes con p fijo es NP-dura en sentido fuerte salvo P = NP. Esto delimita (a) del Thm 5.1 y el
nuevo teorema: dureza fuerte requiere p no acotado. Para p = 1 se recupera la Obs. 5.2(i) (allí basta Σ a_i).
Estado: DEMOSTRADO (argumento elemental; verificado por implementación en el script, §3).

## 3. Verificación (theory/check_hardness.py → check_hardness_output.txt, 39 s)

- 156 instancias fuente (78 SÍ, 78 NO; todas las t de 3 vectores b pequeños + 100 aleatorias, m ≤ 11,
  n ≤ 12), reglas C y P: 312 pares; 137 328 subconjuntos D∖R resueltos en aritmética racional exacta.
- Equivalencia (existe testigo de entrada ⇔ Subset Sum SÍ): 312/312.
- Caracterización conjunto a conjunto (entra ⇔ gadget presente, ≥1 ítem, Σ b = t): 0 fallos.
- Unicidad certificada (X_E de rango completo) en TODOS los subconjuntos; 0 empates KKT; D correcto 312/312.
- Biblioteca: test cerrado de la Prop. 3.1 vs exacto: 0 discrepancias; lasso_lars (guarda KKT) vs exacto:
  0 discrepancias de soporte en 33 172 ajustes.
- DP de §2: f_enter igual al exhaustivo en 312/312; DP vs exhaustivo en datos enteros aleatorios
  (p = 2, 3; metas enter/leave/any): 145/145.
- Controles negativos (deben fallar): u = 1, κ = 2 y ρ = 1 producen fallos de caracterización, una
  equivalencia rota (u = 1, κ = 2) o subconjuntos sin unicidad certificada (ρ = 1). El chequeo discrimina.

## 4. Parte 3 (dureza fuerte con p creciente): NO demostrada

Delimitación demostrada: por §2, con p fijo no hay dureza fuerte (salvo P = NP), para ninguna meta.
Ruta candidata (NO verificada, no se afirma): generalizar el gadget a d absorbedores l = 1..d, cada uno con
su Δ_l lineal en las filas quitadas; la entrada de la variable objetivo exigiría Δ_l ≤ 0 para todo l
(absorbedores inactivos) y Σ_l Δ_l ≥ 0 (correlación suficiente), es decir Δ_l = 0 para todo l: una suma
vectorial exacta con entradas pequeñas (p. ej. Exact Cover by 3-Sets: filas = tripletas, coordenadas =
elementos), que es fuertemente NP-completa. Lo que falta: controlar la interacción de varios absorbedores
activos a través de la matriz de Gram (con d > 1 la variable objetivo no queda absorbida automáticamente
cuando solo algunos Δ_l > 0, y hay que excluir entradas con signo negativo), y la unicidad. Queda como
conjetura.

## 5. Entregable y compilación
hardness_p2.tex: Lema lem:entry, Teorema thm:enter2, Proposición prop:pseudo, Corolario cor:weak,
Observación rem:verify2, Conjetura conj:strong (+ ediciones sugeridas a main.tex en comentarios, NO aplicadas).
Compilado insertado en una copia de main.tex (scratchpad) antes de conj:enter: sin errores ni referencias
indefinidas (13 páginas). main.tex no se tocó.
