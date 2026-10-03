# Informe de árbitro interno independiente — MRT001, ronda 5 (03/10/2026)

**Veredicto: cambios menores** — las pruebas de los Teoremas 5.8–5.9, la Proposición 5.10 y el Lema B.2 son correctas (verificadas paso a paso y con enumeración exhaustiva hasta n = 11 y Monte Carlo propio hasta n = 200); quedan una sobreafirmación numérica en n = 50, una hipótesis n ≥ 6 omitida, redondeos de cotas hacia abajo, un choque de notación y la extensión.

Recuento: 0 bloqueantes, 0 mayores, 11 menores (m6–m9 opcionales). Ronda 4: 11/11 puntos bien aplicados.

Versión arbitrada: v0.7 (commit a4c05eb), `manuscript/main.tex` (676 líneas), PDF de 31 páginas.
Prioridad: Teoremas 5.8 (`thm:sharpN`), 5.9 (`thm:sharpR`), Proposición 5.10 (`prop:sharpexplicit`), Observación 5.11 (`rem:sharpopen`), Lema B.2 (`lem:sharpbad`), Tabla 11 (`tab:sharp`).
Trabajo auxiliar (no en la carpeta): `/tmp/claude-0/-home-user-ChanoSilva/6d28bda3-759e-5faa-92d7-8739680d15c2/scratchpad/referee5_MRT001/` (`perm.c`, `find_small.py`, `bij.py`, `analyze_exact.py`, `analyze_mc.py`, salidas `exact.jsonl`, `mc50/100/200.jsonl`).

## 0. Verificación de los teoremas nuevos (prioridad máxima)

He leído cada paso de las pruebas de main.tex:415–466 (enunciados) y main.tex:619–654 (pruebas; Tabla 11 en :657–672), contra theory/sharp_rate.tex y theory/sharp_rate_derivation.md solo como apoyo. Resumen: **no encuentro ningún error matemático**. Todas las constantes, signos e identidades que comprobé a mano coinciden, y mi verificación computacional independiente (C + Python, escrita desde cero) las confirma. Los hallazgos son de precisión de enunciado y de redacción (sección 2).

### 0.1 Teorema 5.8 (ley de N_n)

- (i) Inversión de momentos: con E[(N_n)_r] = 1 − r/n, la inclusión–exclusión da p_k = (1/k!) Σ_{s=0}^{n−1−k} (−1)^s/s! (1 − (k+s)/n) (main.tex:597, :621). Serie completa = e^{-1}(1 − (k−1)/n) (usa Σ(−1)^s s/s! = −e^{-1}). Cola T_k: el término s = n−k se anula; con s = n−k+m, T_k = −(1/n)Σ_{m≥1}(−1)^{n−k+m} m/(n−k+m)!, cociente de módulos (m+1)/(m(n−k+m+1)) ≤ 2/(n−k+2) ≤ 2/3 < 1 porque k ≤ n−1; serie alternante ⇒ |T_k| ≤ 1/(n(n−k+1)!). Correcto, y la cota es asintóticamente ajustada (ver 0.6: el cociente |r|·n·k!(n−k+1)! sube a 0,86 en n = 11 y a 0,97 en n = 60 según la salida congelada).
- (ii) Signos: para 2 ≤ k ≤ n−2, |nT_k| ≤ 1/3! = 1/6 < e^{-1} ≤ e^{-1}(k−1); para k = n−1, |nT_k| ≤ 1/2 < 2e^{-1} ≤ e^{-1}(n−2) exige n ≥ 4. Correcto. **La hipótesis n ≥ 4 es un artefacto de la prueba, no del resultado**: calculé la ley exacta para n = 1,…,11 y la identidad d_TV = (p_0−π_0) + (p_1−π_1)^+ y la desigualdad |d_TV − e^{-1}/n| < 2/(n·n!) valen también para n = 1, 2, 3 (en n = 3: p = (1/2, 1/3, 1/6), p_2 = 0,1667 < π_2 = 0,1839). No hay contraejemplo en n = 4, 5, 6: el patrón de signos de p_k − π_k es `++--`, `+----`, `++----` (el de k = 1 alterna con la paridad de n: positivo para n par), siempre p_k < π_k para k ≥ 2.
- Límite: Σ_k |k−1|/k! = 2 (único término negativo k = 0), n·d_TV → e^{-1}. Correcto.

### 0.2 Teorema 5.9 (ley de primer orden de R_n) y medida μ

- μ(2^k) = (π_k − π_{k−1}) [ν] − π_{k−2} [321: masa que sale de 4·2^Z] + 4(π_{k−1} − π_k) [cuatro configuraciones ×2] = −3π_k + 3π_{k−1} − π_{k−2} = −(e^{-1}/k!)(k−1)(k−3); μ(3·2^k) = π_{k−1} [321: masa que llega a 6·2^{Z}]. Verificado a mano y simbólicamente.
- Masa total: −3 + 3 − 1 + 1 = 0. ‖μ‖ = e^{-1}Σ|(k−1)(k−3)|/k! + 1 = e^{-1}(e+1) + 1 = 2 + e^{-1} (Σ(k−1)(k−3)/k! = 2e − 4e + 3e = e; único término negativo k = 2, −1/2). c_2 = 1 + 1/(2e) = 1,18394. Parte positiva = átomos 3·2^k (masa 1) y átomo 4 (e^{-1}/2): suma c_2, coherente.
- Valores particulares (main.tex:448): P(R=1) = e^{-1}(1−3/n), P(R=2) = e^{-1}, P(R=4) = ½e^{-1}(1+1/n), P(R=6) = P(R=12) = e^{-1}/n, P(R≤8) = (8/3)e^{-1} − (3/2)e^{-1}/n (μ(8) = 0), P(no potencia de 2) = 1/n. Todos correctos.
- Cancelación de las excepciones de razón 2: las cuatro configuraciones ×2 (peso 4/n) aportan 4(π_{k−1}−π_k) a átomos que 2^Z ya carga; por eso la constante baja de 5 + e^{-1} (acoplamiento) a 1 + 1/(2e). El razonamiento de main.tex:460 es correcto.
- Descomposición de la prueba (main.tex:642–650): (1) corchete de N_n vía Teorema 5.8(i) con ρ_1 ≤ 2^{n+1}/(n(n+1)!) + 1/n! (comprobado: para k ≥ n, |−π_k − ν(k)/n| = π_k|k−1−n|/n ≤ π_k k/n); (2) fuera de 𝓔, 1{R∈A} − 1{2^N∈A} = Σ_ω 1_ω g_ω(N_n) y |ρ_2| ≤ P(𝓔) + E[#ω; 𝓔] (correcto: se descompone en 1_{𝓔^c} y 1_𝓔); (3) condicionado a ω, N_n = N(p) + N(σ) + δ con δ ≠ 0 solo si σ tiene una sucesión descendente en j* (prob. ≤ 2/(n−2)), y |E g(X) − E g(Y)| ≤ 2 d_TV porque g ∈ {−1,0,1}; (4) pesos (n−2)/(n(n−1)) = 1/n + O(n^{-2}) y 1/n. Todos los errores son uniformes en A, luego d_TV = sup_A|μ(A)|/n + O(n^{-2}) = ‖μ‖/(2n) + O(n^{-2}). Correcto.

### 0.3 Corrección de la definición de "ocurrencia" y biyección de contracción

La definición nueva (main.tex:626: ventana de posiciones + patrón, probabilidad (n−2)!/n! = 1/(n(n−1))) es la correcta: la contracción de J a j* = i con el valor del punto más bajo y los valores superiores rebajados en 2 es una biyección sobre S_{n−2} (inversa: inflar σ en j* con el patrón p); fijar también la ventana de valores fijaría σ(j*) y rompería la uniformidad, como dice el paréntesis. **Comprobado por enumeración exhaustiva para n = 6, 7, 8** (`bij.py`): para cada ventana i y cada patrón 321/231/312 las permutaciones contraídas son exactamente S_{n−2} (0 fallos); en las 288/1800/12960 ocurrencias, δ ≠ 0 en 36/192/1200 casos y **siempre** con una sucesión descendente de σ en j* (0 excepciones); para π(1) = n y π(n) = 1, N_n = N(π') + 1{π(2) = n−1} (resp. 1{π(n−1) = 2}) sin fallos.

### 0.4 Lema B.2 (evento malo) y la constante 223/n²

- (a) Σ_{k=4}^{n−2} E I_k ≤ (24+19+6+3+120)/n² = 172/n² (cada desigualdad para n ≥ 20 comprobada: n ≥ 19 para E I_{n−2}, n² − 19n + 2 ≥ 0 para E I_{n−3}, 200n ≤ (n−1)(n−2)(n−3) para E I_{n−4}, 7n² − 25n − 6 ≥ 0 para el bloque central).
- Momentos de pares: dos 3-intervalos distintos son disjuntos (18(n−4)(n−5)/(n)_4), solapan en dos puntos (la unión es un 4-intervalo con patrón en {1234, 1324, 4231, 4321}: exactamente 4, verificado a mano), o en uno (unión 5-intervalo, valor común = 3, 2·2·2 = 8 patrones). E[I_3 I_{n−1}] = 4(6n−16)/(n(n−1)(n−2)) (I_{n−1} = 1{π(1)∈{1,n}} + 1{π(n)∈{1,n}}; dado π(1) = 1, 6(n−3)/((n−1)(n−2)) + 2/((n−1)(n−2))). E C(I_{n−1},2) = 2/(n(n−1)). Cotas 23, 25 (diferencia (n² − 11n + 50)/(n²(n−1)(n−2)) > 0, discriminante negativo) y 3. Total 172 + 23 + 25 + 3 = 223. **Las tres fórmulas de pares coinciden en aritmética racional exacta con la enumeración completa de S_n para n = 6,…,11** (el autor solo lo comprobó en n = 8, 9).
- (b) Los tres casos (K disjunto de J; K ⊋ J; solape parcial con U = J ∪ K intervalo y a lo sumo dos K por U) y el caso de frontera (π(1) = n: intervalos de π' o [1,k] con [2,k] intervalo inicial de π') son exhaustivos; h_m ≤ 4/m + 18/(m(m−1)) + Σ_{l≥4} E I_l(m) = 8/m + O(m^{-2}). Correcto. Ensamblando las constantes la cota es ≈ (102 + 12 + 36)/n² ≈ 150/n²; la enumeración exacta da n²·E[#ω; 𝓔] = 23,0; 26,2; …; 37,4 para n = 6,…,11.
- Afirmación estructural clave ("fuera de 𝓔 ocurre a lo sumo una ocurrencia y R_n = c_ω 2^{N_n}, o 2^{N_n} si no ocurre ninguna", main.tex:626): **verificada sin excepción para todas las permutaciones de S_n, 6 ≤ n ≤ 11** (4,4·10^7 permutaciones), con R calculado por la fórmula de Gallai validada contra un conteo por fuerza bruta de orientaciones transitivas (vía extensiones lineales, Dushnik–Miller) en todo S_n, n ≤ 7 (0 discrepancias). **Falla en n = 4 (17 permutaciones) y n = 5 (8)**: p. ej. 21453 (un solo 3-intervalo 453 de patrón 231, R = 2 = 2^N, no 2·2^N: la contracción tiene longitud 3 y no es simple) y 32541 (R = 4, N = 2, ocurrencia π(n) = 1 pero R ≠ 2·2^N). No contradice nada enunciado (el lema es para n ≥ 20 y el teorema es asintótico), pero la frase de main.tex:626 no lleva hipótesis sobre n (ver m3).

### 0.5 Proposición 5.10

Fuera de 𝓔, R_n ≠ 2^{N_n} exige una ocurrencia; E[#ω] = 3(n−2)/(n(n−1)) + 2/n ≤ 5/n − 3/n² (verificado exactamente por enumeración en 6 ≤ n ≤ 11); con 223/n² da 5/n + 220/n²; con Teorema 5.8(ii) y 2/(n·n!) ≤ 1/n², (5 + e^{-1})/n + 221/n². Correcto.

### 0.6 Observación 5.11 (lo abierto)

Declara abierto exactamente lo no demostrado: (1) la constante explícita C de |d_TV(R_n,2^Z) − c_2/n| ≤ C/n²; (2) n²·d_TV(N_n, Po(1−1/n)) → 3/(4e), solo numérico. Comprobé la heurística: e^{1/n}(1−1/n)^k = 1 + (1−k)/n + (k²−3k+1)/(2n²) + O(k³/n³), así que p_k − Po_{1−1/n}(k) = −π_k(k²−3k+1)/(2n²) + …, con Σ(k²−3k+1)/k! = 0 y términos negativos solo en k = 1, 2 (−1 y −1/2), luego Σ|·| = 3 y el límite es 3/(4e) = 0,27591. Observación: (2) es demostrable en pocas líneas (Teorema 5.8(i) + resto de Taylor alternante de (1−x)^k, |R_3| ≤ C(k,3)x³, sumable contra π_k); ver m6. Una precisión de redacción: "gives every error term in closed form" exagera (h_m y s_m se acotan como 8/m + O(m^{-2}) y 10/m + O(m^{-2}), no en forma cerrada); ver m5.

### 0.7 Tabla 11, números y salida congelada

- `sha256sum results/check_sharp_rate_output.txt` = `72d23ffe8f50726c66bd8d38b5f9e8a078c6f4f0063c5f13d7258448ec911282` = `results/check_sharp_rate_output.sha256` = `meta.json`, y prefijo de `\SharpSha` ✓. La copia de `theory/` difiere solo en 10 líneas de tiempo (`diff`) ✓.
- Macros `\Sharp*` de numbers.tex:166–225 contrastadas con la salida congelada: 0,97 / 0,95 / 0,016 / 2,1·10⁻⁷ / 3,6·10⁻¹⁹ / 0,2760 / 106,4 / 0,156–0,046–0,008 / 2592 de 4921 / 720 de 2460 / 134 de 984 / tabla_sharp.tex (cuatro filas) ✓, con la salvedad de redondeo de m4.
- Los 173 macros de v0.6 (commit 2a9ce22) tienen exactamente el mismo valor en v0.7; se añadieron 80 (comprobado por programa) ✓, como dice la respuesta.
- Mi Monte Carlo independiente (exacto por muestra: todos los intervalos, sin ventana; control con la ley exacta de N_n) reproduce la Tabla 11 dentro de los errores: n·P(R≠2^N) = 4,963 ± 0,021 (n = 50; autor 5,01 ± 0,05), 4,993 ± 0,039 (n = 100; autor 5,04 ± 0,08), 4,887 ± 0,110 (n = 200; autor 4,92 ± 0,12); n·d_TV (estimador plug-in con variable de control) 1,271 / 1,235 / 1,241 frente a 1,261 / 1,231 / 1,165 del autor. Detalle en la sección "Verificación computacional".

## 1. Verificación de la ronda anterior (ronda 4)

| id | estado | evidencia |
|---|---|---|
| M1 (atribución Lemas 5.4–5.5, estadística de intervalos) | aplicado bien | main.tex:394 `[known, e.g. Brignall 2010; proof included…]`; :398 `[classical, the prime-node case of Gallai's decomposition…]`; frase del primer momento en :467 y :595; "claim as new" en :467; tabla :540–541 "uses Gallai and classical interval statistics"; refs.bib:385–415 (`corteel2006`, `albert2003`, `brignall2010`); README:5 y FICHA:13 "autocontenida salvo el teorema de Gallai…" |
| m1 (Obs. B.1, fuentes de razones) | aplicado bien | main.tex:611: "Ratios R/2^N other than 1, 3/2 and 2 require an interval with at least four elements … or two of the configurations…"; ejemplos 563412 y 4231; "only sketched" eliminado; "The formula is not used in the proofs…". Comprobé las razones 3 (π(1)=n, π(2)=n−1) y 6 (π(1)=n, π(n)=1) |
| m2 (alcance doble fuerza bruta) | aplicado bien | main.tex:616 con macros numbers.tex:157–160 (873 perms n ≤ 6 con dos; 5040 de n = 7 con una) |
| m3 (n pequeño, IC) | aplicado bien | main.tex:470 "partly fortuitous…" con 2592 de 4921 (salida (F)); IC [4.87, 5.11] → [3.0, 7.0] (numbers.tex:161–164); tabla :542 sin la comparación en n = 20 |
| m4 ("n ≥ 20" en la tabla) | aplicado bien | main.tex:540 |
| m5 (última frase de "Sharpness and data") | aplicado bien | main.tex:470 "with probability 1−O(1/n)…"; "kernel class is also open (Proposition 3.5) but is never a finite union of similarity orbits, since these … have empty interior" (argumento correcto: órbitas de dimensión d(d+1)/2+1 < nd) |
| m6 (d_TV(N_n,Po(1)) = e⁻¹/n + O(n⁻²)) | aplicado bien (superado) | Teorema 5.8(ii) (main.tex:425–431), verificado en 0.1 |
| m7 (cota 24/n² + … derivada) | aplicado bien | main.tex:607: derivación condicionando a π(1) = n; cota 24/n² + 8/(n(n−1)(n−2)), recomprobada |
| m8 (docstring E5f) | aplicado bien | experiments/realizer_law.py:2–27 |
| m9 (CONTINUIDAD, README, FICHA, copias de salida) | aplicado bien | CONTINUIDAD:105 "[Cerrado en v0.6…]", :62 "cota inferior de la extensión"; README:19–20 y main.tex:566 (copias de `results/` = referencia); FICHA:13–14 |
| m10 (DOI Gallai) | aplicado bien | refs.bib:362 |
| Opcional (regla de forzado, dos sentidos) | aplicado bien | main.tex:391 "since a→x→b, like b→x→a, would force the edge ab" |
| Acción 12 (cotejos con fuentes primarias) | abierto, declarado | CONTINUIDAD:167 y RESPUESTA §"Qué queda abierto" 3 |

Recuento: 11/11 bien aplicados (+1 opcional), 0 a medias, 0 no aplicados, ninguno con error nuevo.

## 2. Hallazgos nuevos

### Bloqueantes
Ninguno.

### Mayores
Ninguno. Las pruebas de los Teoremas 5.8–5.9, la Proposición 5.10 y el Lema B.2 son correctas tal como están escritas (sección 0).

### Menores

**m1. Choque de notación π / π_k / p / p_k / p_i en las pruebas nuevas** (main.tex:416 "Write p_k = Pr(N_n = k) and π_k = e^{-1}/k!"; :626 patrón "p ∈ {321, 231, 312}"; :642–650, donde conviven "π(1) = n", "π(2) = n−1" y "π_{k−1}", "π_{k−2}"; y p_i para puntos en :385).
*Problema:* π es la permutación, π_k el peso de Poisson, p el patrón, p_k la ley de N_n y p_i un punto; en la prueba del Teorema 5.9 aparecen π(·) y π_k en la misma frase. No hay error, pero es la parte que más cuesta verificar.
*Corrección:* llamar q_k = e^{-1}/k! a los pesos de Poisson (main.tex:415–466 y :619–654) y τ al patrón de tres elementos (ω = (J, τ), N(τ), G_τ); por ejemplo, "Write $p_k=\Pr(N_n=k)$ and $q_k=e^{-1}/k!$ for $k\ge0$, $q_k=0$ for $k<0$".

**m2. "Agree" en n = 50 es una sobreafirmación** (main.tex:658 "The estimates of $n\,d_{\mathrm{TV}}(R_n,2^Z)$ agree with $c_2$ … and with the first-order law"; tabla de afirmaciones main.tex:546 "agrees with the first-order law, atom by atom and in $d_{\mathrm{TV}}$" para 50 ≤ n ≤ 400).
*Evidencia:* Tabla 11, n = 50: 1,261 ± 0,041 excluye el valor del modelo (1,201) y c_2 (1,184); max|z| = 4,4. Mi Monte Carlo independiente en n = 50 (2·10⁶ permutaciones, variable de control) da 1,271, con un sesgo plug-in estimado ≤ 0,01: el exceso de ≈ +0,07 es real, un término de segundo orden ≈ +4/n en n·d_TV (también visible en n = 100: 1,235 frente a 1,192).
*Corrección:* "For $n\ge100$ the estimates … agree with $c_2$ and with the first-order law; at $n=50$ they exceed the first-order value by about $0.06$ (three standard errors), and the atom-wise deviation reaches $|z|=4.4$: the $O(n^{-2})$ remainder is visible there." En la tabla de afirmaciones: "… agrees with the first-order law for $100\le n\le400$; at $n=50$ the $O(n^{-2})$ term is visible (Table 11)".

**m3. Afirmación estructural sin hipótesis sobre n** (main.tex:626 "The proof of Proposition 5.7 shows that outside $\mathcal E$ at most one occurrence happens, $R_n=c_\omega2^{N_n}$ if $\omega$ does…").
*Evidencia:* es falsa en n = 4 (17 permutaciones) y n = 5 (8), p. ej. 21453 (R = 2 = 2^N con una ocurrencia 231) y 32541 (R = 4, N = 2, ocurrencia π(n) = 1); verdadera para todo S_n, 6 ≤ n ≤ 11 (enumeración exhaustiva) y, por la prueba, para n ≥ 6 (el Paso 1 se aplica a π' de longitud n−1 ≥ 5).
*Corrección:* "For $n\ge6$, the proof of Proposition~\ref{prop:exceptions} shows that …".

**m4. Redondeo de cotas superiores hacia abajo** (main.tex:658 "each of the four pieces of that proof is at most \SharpPieceMax{} times its bound" = 0,97, pero la salida congelada da 0,9731; "lies between \SharpDevMin{} and \SharpDevMax" = 0,95, pero el máximo es 0,9521).
*Causa:* experiments/make_numbers.py:367 y :389 usan `:.2f`.
*Corrección:* para cantidades que se presentan como cota superior, redondear hacia arriba: `f"{math.ceil(100*x)/100:.2f}"` (0,98 y 0,96), o dar tres decimales (0,974 y 0,953).

**m5. Observación 5.11: "gives every error term in closed form" exagera** (main.tex:463).
*Problema:* en el Lema B.2(b) los términos se acotan como s_m = 10/m + O(m^{-2}) y h_m ≤ 8/m + O(m^{-2}); no están en forma cerrada (aunque ensamblarlos es rutinario: ≈ (102 + 12 + 36)/n² ≈ 150/n² con los primeros órdenes).
*Corrección:* "Every error term in the proof of Theorem~\ref{thm:sharpR} is bounded by explicit first moments of interval counts, but the constants were not assembled, so the constant $C$ … is not explicit."

**m6. El límite 3/(4e) de la Observación 5.11 es demostrable en pocas líneas** (main.tex:463; opcional).
Con el Teorema 5.8(i) (Σ_k|r_{n,k}| ≤ 2^{n+1}/(n(n+1)!)), e^{1/n} = 1 + 1/n + 1/(2n²) + O(n^{-3}) y (1−x)^k = 1 − kx + C(k,2)x² − θC(k,3)x³ con 0 ≤ θ ≤ 1 para 0 ≤ x ≤ 1, se tiene Po_{1−1/n}(k) = q_k[1 + (1−k)/n + (k²−3k+1)/(2n²)] + O(q_k(1+k³)/n³), sumable en k; luego d_TV(N_n, Po(1−1/n)) = (e^{-1}/(4n²))Σ_k|k²−3k+1|/k! + O(n^{-3}) = 3/(4en²) + O(n^{-3}) (Σ(k²−3k+1)/k! = 0; negativos solo k = 1, 2, con suma −3/2). O se escribe y se etiqueta "proved here", o se deja como está; pero no debería presentarse como problema abierto del mismo rango que la constante C.

**m7. La hipótesis n ≥ 4 del Teorema 5.8(ii) es un artefacto de la prueba** (main.tex:425; opcional). La identidad y la cota valen para todo n ≥ 1 (cálculo exacto n = 1,…,11; en n = 3, p_2 = 1/6 < q_2 = 0,184). Añadir "(the identity and the bound also hold for $n\le3$, by direct computation)" o dejarlo; el enunciado actual es correcto.

**m8. Antecedentes del Teorema 5.8** (main.tex:431 "proved here").
La ley exacta de N_n es clásica (la propia App. B cita la forma cerrada C(n−1,k)(D_{n−k} + D_{n−k−1})/n! de Kaplansky 1945), y (i)–(ii) son consecuencias elementales de ella. No encontré (una búsqueda) un enunciado explícito de d_TV ~ e^{-1}/n para sucesiones, pero la literatura de aproximación de Poisson (Barbour–Holst–Janson 1992, capítulo de permutaciones aleatorias) es el lugar natural. *Corrección:* etiqueta "proved here (an elementary consequence of the classical exact law~\citep{kaplansky1945})" y una búsqueda dirigida antes de presentarlo como nuevo.

**m9. c_2 sin c_1** (main.tex:446). El manuscrito define c_2 pero no c_1 (solo aparece en la salida de la comprobación). Definir c_1 = e^{-1} en el Teorema 5.8(ii) ("$n\,d_{\mathrm{TV}}(N_n,\mathrm{Po}(1))\to c_1=e^{-1}$") o renombrar c_2 → c_R.

**m10. Etiquetas de estado tras esta ronda.** Si el coordinador acepta este informe, actualizar "not yet independently refereed / aún sin arbitraje independiente" en main.tex:70 (resumen), :416, :431, :448, :457, :629 (Lema B.2), :543–545 (tabla), :559 (Limitations), README:5 y :34, FICHA:11, :13, :22, :24, por ejemplo "proved here; checked by an internal referee (round 5)", conservando "internal" (no es arbitraje externo) y manteniendo "open" para la constante C.

**m11. Figura 3 fuera de su sección y página casi vacía** (main.tex:500 `\begin{figure}[p]`). En el PDF la Figura 3 (E5d, Sección 5) ocupa sola la p. 21 (104 palabras), después de la Sección 6 y de la tabla de afirmaciones, y la p. 19 queda a media página. *Corrección:* `[tb]` (o `[t]` con `width=0.9\linewidth`) colocada junto a la Tabla 7 de E5d; ahorra ≈ 1 página.

## 3. Lectura fresca de las secciones nuevas y encaje con el resto

- El párrafo "Sharp rates" (main.tex:415–416), los enunciados 5.8–5.10, el párrafo sobre la composición de μ (:460) y la Observación 5.11 encajan con la Sección 5 sin contradicciones: el Teorema 5.6(b)–(c) queda como cota cruda revisada en la ronda 4 y la Proposición 5.10 la mejora; "Sharpness and data" (:470) remite correctamente al Teorema 5.8 para explicar n·d_TV = 0,368.
- El resumen (:70), la tabla de afirmaciones (:543–547), Limitations (:559), README:5/:34 y FICHA:11/:13/:22/:24 etiquetan de forma coherente los resultados nuevos ("proved here; not yet independently refereed"; "open (second: numerical only)"). No encontré ninguna afirmación que vaya más allá de lo demostrado, salvo m2 (n = 50) y m5 ("closed form").
- La definición corregida de ocurrencia (:626) es la que usa la prueba del Lema B.2(b) y del Teorema 5.9; la nota de cabecera de theory/sharp_rate.tex y theory/sharp_rate_derivation.md describe bien la corrección (no modifiqué theory/).
- Con el Teorema 5.8 y la Proposición 5.10 demostrados, la parte de d_TV del Teorema 5.6(b) y el apartado (c) (con 10 + e² y 167/n²) y el final del Paso 3 y el Paso 4 de su prueba (:597–599) quedan dominados; se pueden retirar (ver Extensión).

## 4. Bibliografía (entradas nuevas de v0.7)

| entrada | estado | corrección |
|---|---|---|
| `corteel2006` Corteel, Louchard, Pemantle, "Common intervals in permutations", DMTCS 8 (2006) 189–214 | verificada por WebSearch (ficha de dmtcs.episciences.org/362 y dblp: título "Common Intervals in Permutations", vol. 8, pp. 189–214; el resumen enuncia la convergencia del número de intervalos a Poisson(2)) | ninguna obligatoria. Cuidado con la versión de congreso homónima "Common Intervals of Permutations" (Birkhäuser, Mathematics and Computer Science III, 2004), que es otra publicación. Opcional: DOI de DMTCS (formato 10.46298/dmtcs.362, a confirmar). Nota de contenido: el Poisson(2) lo producen sobre todo los intervalos de tamaño 2 (sucesiones ascendentes + descendentes); la frase de main.tex:467/:595 es correcta pero la parte relevante para el paper es que los intervalos de tamaño 3..n−1 tienen probabilidad O(1/n) |
| `albert2003` Albert, Atkinson, Klazar, "The enumeration of simple permutations", J. Integer Seq. 6 (2003), art. 03.4.4 | verificada (cs.uwaterloo.ca/journals/JIS/VOL6/Albert/; resumen: "asymptotic expansion for these coefficients") | ninguna; opcional `url`. La asintótica e^{-2}(1 − 4/n + O(n^{-2})) solo cotejada vía resumen/OEIS A111111, como dice la respuesta |
| `brignall2010` Brignall, "A survey of simple permutations", Permutation Patterns, LMS LNS 376, CUP 2010, pp. 41–65 | verificada (cambridge.org/core, arXiv:0801.0963) | añadir `eprint = {0801.0963}` para que la correspondencia intervalo–módulo pueda cotejarse en la versión abierta; la página exacta sigue sin cotejar (pendiente declarado) |
| `gallai1967` (DOI añadido) | DOI 10.1007/BF02020961 ya verificado en la ronda 4 | ninguna |

Los PDF de los editores no se descargaron (la verificación es por fichas y resúmenes de búsqueda, como en la ronda 4).

## 5. Verificación computacional (independiente; ningún código del autor reutilizado)

Todo en `/tmp/claude-0/-home-user-ChanoSilva/6d28bda3-759e-5faa-92d7-8739680d15c2/scratchpad/referee5_MRT001/`. CPU total ≈ 1,5 min (bajo el presupuesto de 5 min).

1. **`perm.c`** (C, escrito desde cero): t(G_π) por descomposición modular escrita directamente sobre la permutación (suma directa → producto; suma sesgada con k hijos → k!·producto; nodo primo → 2·producto, comprobando que los intervalos maximales propios forman partición y que el cociente tiene ≥ 4 elementos); N, todos los intervalos, ocurrencias y evento 𝓔 por definición.
   - Validación de R: fuerza bruta independiente de orientaciones transitivas vía extensiones lineales (Dushnik–Miller: T transitiva ⇔ P ∪ T orden lineal), todo S_n con n ≤ 7: **0 discrepancias** (0,5 s). Además `find_small.py` (Python, fuerza bruta pura) para n ≤ 6.
   - **Enumeración exacta de S_n, 4 ≤ n ≤ 11** (n = 11: 39 916 800 permutaciones, 15,6 s; n = 10: 1,2 s). Ley de N_n = fórmula de inclusión–exclusión en racionales exactos (n = 4..11); r_{n,k} dentro de la cota (máx. 0,86); signos y d_TV de 5.8(ii) correctos; los tres momentos de pares del Lema B.2(a) y E[#ω] = 3(n−2)/(n(n−1)) + 2/n exactos para 6 ≤ n ≤ 11; afirmación "fuera de 𝓔, R = c_ω2^N" sin excepciones para 6 ≤ n ≤ 11 y con 17/8 excepciones en n = 4/5 (m3). Con n ≤ 11 la ley de R_n aún está lejos del primer orden (n·d_TV = 1,77…1,95, P(𝓔) = 0,39 en n = 11), como advierte la salida congelada; coincide con la parte (C) del autor en n = 6, 7, 8 (1,768 / 1,733 / 1,941).
   - **Monte Carlo propio** (splitmix64, semillas 501/1001/2001; exacto por muestra, sin ventana de tamaños; P(R = x) = P(2^{N_n} = x) exacta + media de 1{R=x} − 1{2^N=x}): n = 50 (2·10⁶ muestras), 100 (1,2·10⁶), 200 (3·10⁵), ≈ 40 s de CPU.

     | n | n·P(R≠2^N) | n·P(R no pot. 2) | n(P(R=1)−e⁻¹) [μ = −1,104] | n·P(R=6) [0,368] | n·P(R=12) [0,368] | n(P(R=4)−e⁻¹/2) [0,184] | n·d_TV plug-in [c_2 = 1,184] | n²·P(𝓔) |
     |---|---|---|---|---|---|---|---|---|
     | 50 | 4,963 ± 0,021 | 1,078 ± 0,010 | −1,140 ± 0,012 | 0,384 ± 0,006 | 0,388 ± 0,006 | 0,180 ± 0,016 | 1,271 | 73 |
     | 100 | 4,993 ± 0,039 | 1,049 ± 0,018 | −1,103 ± 0,022 | 0,381 ± 0,011 | 0,382 ± 0,011 | 0,186 ± 0,029 | 1,235 | 79 |
     | 200 | 4,887 ± 0,110 | 1,007 ± 0,051 | −1,049 ± 0,060 | 0,379 ± 0,031 | 0,341 ± 0,030 | 0,193 ± 0,081 | 1,241 | 73 |

     (± = 1,96 EE.) Todos los átomos convergen a μ con desviaciones del orden de 1/n (máx|z| frente a μ: 8,5 / 3,6 / 1,9 en n = 50/100/200, decreciendo como corresponde a un resto O(n⁻²) en P, es decir O(1/n) en n·P). n²·P(𝓔) ≈ 75–80, muy por debajo de 223. Dato útil para el agente que trabaja en la constante: n·d_TV(R_n, 2^Z) − c_2 ≈ +0,09 (n = 50) y +0,05 (n = 100), es decir un segundo orden ≈ +4,5/n² en d_TV.
2. **`bij.py`** (Python): biyección de contracción y descomposición de N_n (sección 0.3), n = 6, 7, 8: 0 fallos.
3. **Compilación** en copia (`latexmk -pdf`, 4 s): 0 errores, 0 advertencias en el log (ni referencias/citas indefinidas ni cajas), `pdftotext | grep -c "??"` = 0, **31 páginas**. Numeración comprobada en `main.aux`: Teoremas 5.8, 5.9, Prop. 5.10, Obs. 5.11 (p. 16–17), Lema B.2 (p. 26), Tabla 11 (p. 28).
4. **SHA-256** y macros: ver 0.7. No relancé `check_sharp_rate.py` (116 s; el autor ya lo reejecutó y mis comprobaciones independientes cubren sus partes A–D y F); no relancé E1–E5f (no cambiaron en v0.7).

## 6. Extensión (31 páginas)

Mapa del PDF: Secciones 1–4 pp. 1–11; Sección 5 pp. 11–18 (de ellas ≈ 3 pp. sobre realizadores y tasas); Sección 6 y tabla de afirmaciones pp. 19–20; p. 21 solo la Figura 3; Apéndice A p. 22; Apéndice B pp. 23–28 (≈ 6 pp.); bibliografía pp. 28–31. El material de realizadores (enunciados + Apéndice B + Tablas 8, 9, 11) ocupa ya ≈ 10 de 31 páginas: el exceso sobre el objetivo de 5–10 páginas **no está justificado por el propósito declarado del paper** (un lenguaje de contabilidad para "geometría fundacional"); la ley de realizadores con sus tasas es un resultado de probabilidad combinatoria autónomo. Recortes concretos sin perder contenido demostrado:

1. Figura 3 `[p]` → `[tb]` junto a E5d (m11): −0,8 p.
2. Retirar la parte de d_TV del Teorema 5.6(b) y el apartado (c), el final del Paso 3 (desde "so |Pr(N_n=j) − e^{-1}/j!| ≤ …") y el Paso 4 (main.tex:405–406, :597–599), dominados por el Teorema 5.8(ii) y la Proposición 5.10 una vez arbitrados: −0,3 p.
3. "Sharpness and data" (main.tex:470, ≈ 600 palabras): suprimir la frase de las z combinadas de E5f y las dos últimas columnas de la Tabla 9 (exceptions, 5/n), superadas por la Tabla 11 y la parte (F) de la salida congelada: −0,4 p.
4. Apéndice B, "Numerical check of the sharp rates" (main.tex:658, ≈ 450 palabras): reducir a ≈ 150 (qué se comprueba y dónde está la salida), dejando el detalle a la salida congelada y al pie de la Tabla 11: −0,3 p.
5. Observación B.1: dejar la fórmula y un ejemplo de razón no multiplicativa: −0,2 p.

Total ≈ −2 p. (≈ 29 pp.). Para volver a ≈ 20 pp. hay que tomar una decisión estructural que corresponde al autor: separar Teoremas 5.6–5.10 y el Apéndice B en una nota propia ("The number of realizers of the causal order of a random 2-dimensional sample") y dejar en MRT001 una página con los enunciados y la cita. Lo recomiendo para la próxima versión.

## 7. Lista final de acciones (prioridad descendente)

1. Corrige la frase de main.tex:658 y la fila de main.tex:546: "agree" solo para n ≥ 100; en n = 50 el resto O(n⁻²) es visible (m2).
2. Añade "For $n\ge6$" a la afirmación estructural de main.tex:626 (m3).
3. Redondea hacia arriba las cotas presentadas como "at most"/"between" en make_numbers.py:367 y :389 (0,98 y 0,96, o tres decimales) (m4).
4. Renombra los pesos de Poisson (q_k) y el patrón (τ) en main.tex:415–466 y :619–654 (m1).
5. Sustituye "gives every error term in closed form" en la Observación 5.11 por el texto de m5; decide si demuestras el límite 3/(4e) (m6) o lo dejas como observación numérica sin presentarlo como difícil.
6. Ajusta la etiqueta del Teorema 5.8 a "elementary consequence of the classical exact law" y haz una búsqueda dirigida de antecedentes (m8).
7. Si el coordinador acepta este informe, cambia "not yet independently refereed" por "checked by an internal referee (round 5)" en todos los lugares de m10 (main.tex, README, FICHA, CONTINUIDAD), manteniendo "open" para la constante C.
8. Mueve la Figura 3 a `[tb]` en la Sección 5 (m11) y aplica los recortes 2–5 de la sección Extensión; plantea la separación del material de realizadores en una nota propia.
9. Opcionales: c_1 = e^{-1} junto a c_2 (m9); nota sobre n ≤ 3 en el Teorema 5.8(ii) (m7); `eprint = {0801.0963}` en `brignall2010` y DOI de DMTCS en `corteel2006` tras confirmarlo.
10. Mantén abiertos los cotejos con fuentes primarias (Gallai, Kaplansky/Wolfowitz, Kleindessner–von Luxburg, página de Brignall, enunciados exactos de CLP y AAK).
