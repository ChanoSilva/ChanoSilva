[EN CURSO]

# Informe de árbitro interno independiente — MRT001, ronda 5 (03/10/2026)

Versión arbitrada: v0.7 (commit a4c05eb), `manuscript/main.tex` (676 líneas), PDF de 31 páginas.
Prioridad: Teoremas 5.8 (`thm:sharpN`), 5.9 (`thm:sharpR`), Proposición 5.10 (`prop:sharpexplicit`), Observación 5.11 (`rem:sharpopen`), Lema B.2 (`lem:sharpbad`), Tabla 11 (`tab:sharp`).
Trabajo auxiliar (no en la carpeta): `/tmp/claude-0/-home-user-ChanoSilva/6d28bda3-759e-5faa-92d7-8739680d15c2/scratchpad/referee5_MRT001/` (`perm.c`, `find_small.py`, `bij.py`, `analyze_exact.py`, `analyze_mc.py`, salidas `exact.jsonl`, `mc50/100/200.jsonl`).

## 0. Verificación de los teoremas nuevos (prioridad máxima)

He leído cada paso de las pruebas de main.tex:418–466 (enunciados) y main.tex:619–664 (pruebas), contra theory/sharp_rate.tex y theory/sharp_rate_derivation.md solo como apoyo. Resumen: **no encuentro ningún error matemático**. Todas las constantes, signos e identidades que comprobé a mano coinciden, y mi verificación computacional independiente (C + Python, escrita desde cero) las confirma. Los hallazgos son de precisión de enunciado y de redacción (sección 2).

### 0.1 Teorema 5.8 (ley de N_n)

- (i) Inversión de momentos: con E[(N_n)_r] = 1 − r/n, la inclusión–exclusión da p_k = (1/k!) Σ_{s=0}^{n−1−k} (−1)^s/s! (1 − (k+s)/n) (main.tex:597, :621). Serie completa = e^{-1}(1 − (k−1)/n) (usa Σ(−1)^s s/s! = −e^{-1}). Cola T_k: el término s = n−k se anula; con s = n−k+m, T_k = −(1/n)Σ_{m≥1}(−1)^{n−k+m} m/(n−k+m)!, cociente de módulos (m+1)/(m(n−k+m+1)) ≤ 2/(n−k+2) ≤ 2/3 < 1 porque k ≤ n−1; serie alternante ⇒ |T_k| ≤ 1/(n(n−k+1)!). Correcto, y la cota es asintóticamente ajustada (ver 0.6: el cociente |r|·n·k!(n−k+1)! sube a 0,86 en n = 11 y a 0,97 en n = 60 según la salida congelada).
- (ii) Signos: para 2 ≤ k ≤ n−2, |nT_k| ≤ 1/3! = 1/6 < e^{-1} ≤ e^{-1}(k−1); para k = n−1, |nT_k| ≤ 1/2 < 2e^{-1} ≤ e^{-1}(n−2) exige n ≥ 4. Correcto. **La hipótesis n ≥ 4 es un artefacto de la prueba, no del resultado**: calculé la ley exacta para n = 1,…,11 y la identidad d_TV = (p_0−π_0) + (p_1−π_1)^+ y la desigualdad |d_TV − e^{-1}/n| < 2/(n·n!) valen también para n = 1, 2, 3 (en n = 3: p = (1/2, 1/3, 1/6), p_2 = 0,1667 < π_2 = 0,1839). No hay contraejemplo en n = 4, 5, 6: el patrón de signos de p_k − π_k es `++--`, `+----`, `++----` (el de k = 1 alterna con la paridad de n: positivo para n par), siempre p_k < π_k para k ≥ 2.
- Límite: Σ_k |k−1|/k! = 2 (único término negativo k = 0), n·d_TV → e^{-1}. Correcto.

### 0.2 Teorema 5.9 (ley de primer orden de R_n) y medida μ

- μ(2^k) = (π_k − π_{k−1}) [ν] − π_{k−2} [321: masa que sale de 4·2^Z] + 4(π_{k−1} − π_k) [cuatro configuraciones ×2] = −3π_k + 3π_{k−1} − π_{k−2} = −(e^{-1}/k!)(k−1)(k−3); μ(3·2^k) = π_{k−1} [321: masa que llega a 6·2^{Z}]. Verificado a mano y simbólicamente.
- Masa total: −3 + 3 − 1 + 1 = 0. ‖μ‖ = e^{-1}Σ|(k−1)(k−3)|/k! + 1 = e^{-1}(e+1) + 1 = 2 + e^{-1} (Σ(k−1)(k−3)/k! = 2e − 4e + 3e = e; único término negativo k = 2, −1/2). c_2 = 1 + 1/(2e) = 1,18394. Parte positiva = átomos 3·2^k (masa 1) y átomo 4 (e^{-1}/2): suma c_2, coherente.
- Valores particulares (main.tex:446): P(R=1) = e^{-1}(1−3/n), P(R=2) = e^{-1}, P(R=4) = ½e^{-1}(1+1/n), P(R=6) = P(R=12) = e^{-1}/n, P(R≤8) = (8/3)e^{-1} − (3/2)e^{-1}/n (μ(8) = 0), P(no potencia de 2) = 1/n. Todos correctos.
- Cancelación de las excepciones de razón 2: las cuatro configuraciones ×2 (peso 4/n) aportan 4(π_{k−1}−π_k) a átomos que 2^Z ya carga; por eso la constante baja de 5 + e^{-1} (acoplamiento) a 1 + 1/(2e). El razonamiento de main.tex:458 es correcto.
- Descomposición de la prueba (main.tex:648–656): (1) corchete de N_n vía Teorema 5.8(i) con ρ_1 ≤ 2^{n+1}/(n(n+1)!) + 1/n! (comprobado: para k ≥ n, |−π_k − ν(k)/n| = π_k|k−1−n|/n ≤ π_k k/n); (2) fuera de 𝓔, 1{R∈A} − 1{2^N∈A} = Σ_ω 1_ω g_ω(N_n) y |ρ_2| ≤ P(𝓔) + E[#ω; 𝓔] (correcto: se descompone en 1_{𝓔^c} y 1_𝓔); (3) condicionado a ω, N_n = N(p) + N(σ) + δ con δ ≠ 0 solo si σ tiene una sucesión descendente en j* (prob. ≤ 2/(n−2)), y |E g(X) − E g(Y)| ≤ 2 d_TV porque g ∈ {−1,0,1}; (4) pesos (n−2)/(n(n−1)) = 1/n + O(n^{-2}) y 1/n. Todos los errores son uniformes en A, luego d_TV = sup_A|μ(A)|/n + O(n^{-2}) = ‖μ‖/(2n) + O(n^{-2}). Correcto.

### 0.3 Corrección de la definición de "ocurrencia" y biyección de contracción

La definición nueva (main.tex:625: ventana de posiciones + patrón, probabilidad (n−2)!/n! = 1/(n(n−1))) es la correcta: la contracción de J a j* = i con el valor del punto más bajo y los valores superiores rebajados en 2 es una biyección sobre S_{n−2} (inversa: inflar σ en j* con el patrón p); fijar también la ventana de valores fijaría σ(j*) y rompería la uniformidad, como dice el paréntesis. **Comprobado por enumeración exhaustiva para n = 6, 7, 8** (`bij.py`): para cada ventana i y cada patrón 321/231/312 las permutaciones contraídas son exactamente S_{n−2} (0 fallos); en las 288/1800/12960 ocurrencias, δ ≠ 0 en 36/192/1200 casos y **siempre** con una sucesión descendente de σ en j* (0 excepciones); para π(1) = n y π(n) = 1, N_n = N(π') + 1{π(2) = n−1} (resp. 1{π(n−1) = 2}) sin fallos.

### 0.4 Lema B.2 (evento malo) y la constante 223/n²

- (a) Σ_{k=4}^{n−2} E I_k ≤ (24+19+6+3+120)/n² = 172/n² (cada desigualdad para n ≥ 20 comprobada: n ≥ 19 para E I_{n−2}, n² − 19n + 2 ≥ 0 para E I_{n−3}, 200n ≤ (n−1)(n−2)(n−3) para E I_{n−4}, 7n² − 25n − 6 ≥ 0 para el bloque central).
- Momentos de pares: dos 3-intervalos distintos son disjuntos (18(n−4)(n−5)/(n)_4), solapan en dos puntos (la unión es un 4-intervalo con patrón en {1234, 1324, 4231, 4321}: exactamente 4, verificado a mano), o en uno (unión 5-intervalo, valor común = 3, 2·2·2 = 8 patrones). E[I_3 I_{n−1}] = 4(6n−16)/(n(n−1)(n−2)) (I_{n−1} = 1{π(1)∈{1,n}} + 1{π(n)∈{1,n}}; dado π(1) = 1, 6(n−3)/((n−1)(n−2)) + 2/((n−1)(n−2))). E C(I_{n−1},2) = 2/(n(n−1)). Cotas 23, 25 (diferencia (n² − 11n + 50)/(n²(n−1)(n−2)) > 0, discriminante negativo) y 3. Total 172 + 23 + 25 + 3 = 223. **Las tres fórmulas de pares coinciden en aritmética racional exacta con la enumeración completa de S_n para n = 6,…,11** (el autor solo lo comprobó en n = 8, 9).
- (b) Los tres casos (K disjunto de J; K ⊋ J; solape parcial con U = J ∪ K intervalo y a lo sumo dos K por U) y el caso de frontera (π(1) = n: intervalos de π' o [1,k] con [2,k] intervalo inicial de π') son exhaustivos; h_m ≤ 4/m + 18/(m(m−1)) + Σ_{l≥4} E I_l(m) = 8/m + O(m^{-2}). Correcto. Ensamblando las constantes la cota es ≈ (102 + 12 + 36)/n² ≈ 150/n²; la enumeración exacta da n²·E[#ω; 𝓔] = 23,0; 26,2; …; 37,4 para n = 6,…,11.
- Afirmación estructural clave ("fuera de 𝓔 ocurre a lo sumo una ocurrencia y R_n = c_ω 2^{N_n}, o 2^{N_n} si no ocurre ninguna", main.tex:625): **verificada sin excepción para todas las permutaciones de S_n, 6 ≤ n ≤ 11** (4,4·10^7 permutaciones), con R calculado por la fórmula de Gallai validada contra un conteo por fuerza bruta de orientaciones transitivas (vía extensiones lineales, Dushnik–Miller) en todo S_n, n ≤ 7 (0 discrepancias). **Falla en n = 4 (17 permutaciones) y n = 5 (8)**: p. ej. 21453 (un solo 3-intervalo 453 de patrón 231, R = 2 = 2^N, no 2·2^N: la contracción tiene longitud 3 y no es simple) y 32541 (R = 4, N = 2, ocurrencia π(n) = 1 pero R ≠ 2·2^N). No contradice nada enunciado (el lema es para n ≥ 20 y el teorema es asintótico), pero la frase de main.tex:625 no lleva hipótesis sobre n (ver m3).

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
| m6 (d_TV(N_n,Po(1)) = e⁻¹/n + O(n⁻²)) | aplicado bien (superado) | Teorema 5.8(ii) (main.tex:428–431), verificado en 0.1 |
| m7 (cota 24/n² + … derivada) | aplicado bien | main.tex:607: derivación condicionando a π(1) = n; cota 24/n² + 8/(n(n−1)(n−2)), recomprobada |
| m8 (docstring E5f) | aplicado bien | experiments/realizer_law.py:2–27 |
| m9 (CONTINUIDAD, README, FICHA, copias de salida) | aplicado bien | CONTINUIDAD:105 "[Cerrado en v0.6…]", :62 "cota inferior de la extensión"; README:19–20 y main.tex:567 (copias de `results/` = referencia); FICHA:13–14 |
| m10 (DOI Gallai) | aplicado bien | refs.bib:362 |
| Opcional (regla de forzado, dos sentidos) | aplicado bien | main.tex:391 "since a→x→b, like b→x→a, would force the edge ab" |
| Acción 12 (cotejos con fuentes primarias) | abierto, declarado | CONTINUIDAD:167 y RESPUESTA §"Qué queda abierto" 3 |

Recuento: 11/11 bien aplicados (+1 opcional), 0 a medias, 0 no aplicados, ninguno con error nuevo.
