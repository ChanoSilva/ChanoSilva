# Informe de árbitro interno independiente — MRT001, ronda 6 (03/10/2026)

**Veredicto: cambios menores.** Las pruebas del Teorema 5.11, del Lema B.3, del Teorema 5.12, de la Proposición 5.13 y del Lema B.4 son correctas: las he comprobado paso a paso y con cálculos propios independientes. Quedan precisiones de enunciado y de etiquetado, sobre todo la uniformidad en a del Teorema 5.12(i) y el estado de κ, además de la extensión.

Recuento: 0 bloqueantes, 0 mayores, 9 menores (m6–m9 opcionales). Ronda 5: 11/11 puntos bien aplicados (+ los recortes de la sección "Extensión"), 0 a medias, 0 no aplicados, ninguno con error nuevo.

Versión arbitrada: v0.8 (commit d59af48; árbol de trabajo limpio para la carpeta), `manuscript/main.tex` (791 líneas), PDF de 33 páginas.
Prioridad: Teorema 5.11 (`thm:secondN`, main.tex:474–492), Teorema 5.12 (`thm:bestpois`, :496–504), Proposición 5.13 (`prop:sharpC`, :506–512), Observación 5.14 (:516–521), Conjetura 5.15 (:524–526); pruebas en el Apéndice B, :709–760 (Lemas B.3 `lem:signs` :715, B.4 `lem:intref` :744, ecuación (2) `eq:Bn` :751–757); comprobación numérica en :785–786.
Trabajo auxiliar (fuera de la carpeta): `/tmp/claude-0/-home-user-ChanoSilva/6d28bda3-759e-5faa-92d7-8739680d15c2/scratchpad/referee6_MRT001/`, con `bruteN.c`, `lawN.py`, `check_thm511.py`, `check_thm512.py`, `check_Bn.py`, `rmc.c`, `ana_mc.py`, `cmp_R.py` y `notes.md`. No reutilicé ninguna función del autor ni del agente teórico, ni ejecuté nada de `theory/`.

## 0. Verificación de los resultados nuevos (prioridad máxima)

He leído los enunciados del cuerpo y las pruebas del apéndice. `theory/second_order.tex` y `second_order_derivation.md` los usé solo como apoyo de lectura. **No encuentro ningún error matemático.** Detallo cada paso a continuación.

### 0.1 Teorema 5.11(i)

- E[(N_n)_r] = 1 − r/n vale para 0 ≤ r ≤ n−1, según el Teorema 5.6(b), main.tex:413. Lo comprobé además en racionales exactos con mi propia ley para n = 5, 12 y 40.
- Para Po(λ) se tiene E[(X)_r] = λ^r, así que la diferencia es 1 − rx − (1−x)^r = −Σ_{i≥2} C(r,i)(−x)^i. Es una serie alternante cuyo primer término es −C(r,2)x². El cociente de módulos es (r−i)x/(i+1) = (r−i)/((i+1)n) < 1, de modo que el resto desde i = 3 está entre 0 y C(r,3)x³. Esto da θ ∈ [0,1]. Correcto.
- q̃_k = e^{−1+x}(1−x)^k/k! = q_k e^x(1−x)^k = q_k Σ_j c_j(k)x^j. Con p_k = q_k(1 + c_1(k)x) + r_{n,k} (Teorema 5.8(i), y 1 − (k−1)/n = 1 + (1−k)x) se obtiene la primera igualdad.
- c_2(k) = ½ − k + C(k,2) = (k² − 3k + 1)/2. Para k fijo, r_{n,k} = O(n^{−∞}) y Σ_{j≥3} c_j(k)x^j = O_k(x³). Correcto.

### 0.2 Lema B.3 (signos)

- h_0 = e^x − 1 − x > 0. h_1 = e^x(1−x) − 1 < 0 porque 1 − x < e^{−x} para x ≠ 0. h_2 = e^x(1−x)² − 1 + x = (1−x)h_1 < 0; la identidad es exacta.
- k = 3. Para x < ½ es 1 − 2x > 0, y tomando logaritmos h_3 > 0 ⇔ φ(x) = x + 3 log(1−x) − log(1−2x) > 0. Con denominador común, φ' = [(1−x)(1−2x) − 3(1−2x) + 2(1−x)]/((1−x)(1−2x)) = (2x² + x)/((1−x)(1−2x)) > 0, y φ(0) = 0. Correcto.
- Convexidad en k. La parte lineal −1 − (1−k)x tiene segunda diferencia nula. La exponencial da e^x(1−x)^{k−1}[(1−x)² − 2(1−x) + 1] = e^x(1−x)^{k−1}x² > 0 para k ≥ 1. Por tanto los incrementos h_{j+1} − h_j son no decrecientes, y h_k = h_3 + Σ_{j=3}^{k−1}(h_{j+1} − h_j) ≥ h_3 + (k−3)(h_3 − h_2) > 0. Correcto. Es más limpio que la "convexidad" del borrador del agente.
- Casos k = 1, 2: no hay más negativos en 0 < x < ½. Fuera de ese rango el lema no afirma nada, y el teorema solo lo usa con x ≤ 1/3.

### 0.3 Teorema 5.11(ii), incluido el resto heredado y la cota de ε_n

- d_TV = Σ_k (p_k − q̃_k)^+. Para k ≥ n, p_k = 0 y el término es nulo. Para k ≤ n−1, (1) da p_k − q̃_k = −q_k h_k(x) + r_{n,k}; lo comprobé: q_k(1 + (1−k)x) − q̃_k = −q_k h_k.
- Como t ↦ t^+ es 1-Lipschitz, se tiene |(y_k + r)^+ − y_k^+| ≤ |r|. Con n ≥ 3 (x ≤ 1/3 < ½), el Lema B.3 da y_k^+ = q_k|h_k| solo para k = 1, 2, ambos ≤ n−1. **La prueba no necesita que el soporte de (p_k − q̃_k)^+ sea {1, 2}, y de hecho no lo es para n pequeño.** Mi ley exacta da {2} en n = 3, {1, 3} en n = 4 y {1, 2, 4} en n = 5 (coincide con la salida congelada, parte A4); la diferencia la absorbe ε_n. Es correcto tal como está escrito.
- El resto r_{n,k} es el del Teorema 5.8(i) (|r_{n,k}| ≤ 1/(n k!(n−k+1)!) para 0 ≤ k ≤ n−1, n ≥ 1), que arbitró la ronda 5. Por eso Σ_{k=0}^{n−1}|r_{n,k}| ≤ (1/(n(n+1)!)) Σ_{k=0}^{n−1} C(n+1,k) = (2^{n+1} − (n+1) − 1)/(n(n+1)!). Correcto.
- Φ: q_1|h_1| + q_2|h_2| = e^{−1}(1 − e^x(1−x))(1 + (1−x)/2) = ½e^{−1}(3−x)(1 − (1−x)e^x). Correcto.

### 0.4 Teorema 5.11(iii)

- 1 − (1−x)e^x = Σ_{j≥1}x^j(1/(j−1)! − 1/j!) = Σ_{j≥2}(j−1)x^j/j!. El coeficiente de x^j en ½(3−x)Σ_j a_j x^j es ½(3a_j − a_{j−1}) = (−j² + 5j − 3)/(2·j!). Da d_2 = 3/4, d_3 = 1/4 y d_4 = 1/48. Para j ≥ 5, d_j < 0 porque −j(j−5) − 3 < 0. Σ_{j≥2} d_j = eΦ(1) = 1, luego Σ_{j≥5} d_j = −1/48 exactamente.
- Para 0 < x ≤ 1/3: Σ_{j≥5} d_j x^{j−4} ∈ [x Σ_{j≥5} d_j, 0) = [−x/48, 0). Por tanto (1−x)/48 ≤ Σ_{j≥4} d_j x^{j−4} < 1/48, y 0 < n²Φ(1/n) − 3/(4e) − 1/(4en) ≤ 1/(48en²). Correcto, y la cota es ajustada: θ_n ∈ [0.7635, 0.9994] (cálculo propio, n = 3…200 y n ∈ {300, 500, 700, 1000}).
- El texto que sigue al teorema (main.tex:494) también es correcto. Σ_k ν(k)(k)_r = 1 − E[(Z+1)_r] = −r, por Vandermonde: (Z+1)_r = (Z)_r + r(Z)_{r−1}. Y ½Σ q_k|c_2(k)| = q_1/2 + q_2/2 = 3/(4e).

### 0.5 Teorema 5.12: forma de L(a), su mínimo y paso al ínfimo sobre λ

- (i) |c_j(k)| ≤ Σ_i C(k,i)/(j−i)! = [x^j]e^x(1+x)^k. Para 0 ≤ δ ≤ 1, la cola de orden ≥ 3 vale a lo sumo q_k δ³ e 2^k, y Σ_k q_k e 2^k = e·e^{−1}·e² = e².
- La identidad c_1(k)(x−δ) = (1−k)ax² y la reescritura −q_k g_a x² + q_k c_2(x² − δ²) son correctas, lo comprobé a mano. Para k ≥ n, la discrepancia está acotada por q_k(λ) + q_k|g_a|x², que es superexponencialmente pequeña. Además Σ_k q_k|c_2(k)| = 3/(2e) y |x² − δ²| = |a|x²(2x − ax²) = O(x³).
- La conclusión es |2d_TV − x²L(a)| = O(x³), uniformemente para a en compactos (también λ > 0 y 0 < δ ≤ 1 lo son para n grande).
- (ii) Σ_k q_k g_a(k) = ½E[Z² − 3Z + 1] + aE[Z − 1] = 0. Con f = −1 en k = 1 y f = +1 en el resto, L(a) ≥ Σ q_k g_a f = −2q_1 g_a(1) = e^{−1}. La igualdad exige g_a(k) ≥ 0 para k ≠ 1. Como g_a(0) = ½ − a y g_a(2) = a − ½, eso fuerza a = ½, y g_{1/2}(k) = k(k−2)/2 ≥ 0 para k ≠ 1.
- Fórmula para a ≥ −¼: g_a(k) = ½[(k−1)(k−2+2a) − 1], g_a(3) = ½(1+4a) ≥ 0, y g_a(k) ≥ ½(5+6a) > 0 para k ≥ 4, porque (k−1)(k−2+2a) crece en k cuando k − 2 + 2a > 0. Entonces L = 2Σ q_k g_a^− = e^{−1}(1 + (2a−1)^+ + (½−a)^+). Correcto.
- Numéricamente, la fórmula y la suma directa difieren en < 1.4·10⁻¹⁷ para a ∈ [−¼, 5]. El mínimo en la rejilla [−6, 6] está en a = 0.5 con L = e^{−1}. En a = −1 la fórmula no aplica: L(−1) = 1.119 frente a 0.920 de la fórmula, y el enunciado la restringe correctamente a a ≥ −¼.
- (iii) **El paso del límite al ínfimo es correcto y uniforme, y cubre λ lejos de 1.** Todo λ > 0 se escribe λ = 1 − x + ax² con a = a(n, λ) real, y los tres casos forman una partición:
  - a ∈ [−½, 3/2], un compacto: la uniformidad de (i) y L ≥ e^{−1} dan n²d_TV ≥ 1/(2e) − O(1/n), uniformemente.
  - a > 3/2, lo que incluye todo λ > 1 − x + 1.5x², hasta λ → ∞: d_TV ≥ p_0 − e^{−λ} ≥ e^{−1}(1 + x − e^{x−3x²/2}) − |r_{n,0}| = e^{−1}x² + O(x³), con una constante que no depende de λ, porque e^{−λ} decrece.
  - a < −½, lo que incluye λ → 0⁺: d_TV ≥ e^{−λ} − p_0 ≥ e^{−1}(e^{x+x²/2} − 1 − x) − |r_{n,0}| = e^{−1}x² + O(x³), también uniforme.

  Los desarrollos e^{x−3x²/2} = 1 + x − x² + O(x³) y e^{x+x²/2} = 1 + x + x² + O(x³) son correctos. La cota superior la da (i) con a = ½.
- **Precisión de enunciado (m1):** la prueba de (iii) usa que (i) vale uniformemente en a sobre compactos, y eso solo está en la prueba (main.tex:732), no en el enunciado (:499).

### 0.6 Lema B.4 (`lem:intref`), cadena de cotas y forma cerrada de B(n)

- (a) Con E I_k(m) = (m−k+1)²/C(m,k):
  - E I_4 = 24(m−3)/(m)_3 ≤ 24/(m)_2.
  - E I_{m−2} = 9/C(m,2) = 18/(m)_2.
  - E I_{m−3} = 16/C(m,3) = 96/(m)_3.
  - E I_{m−4} = 25/C(m,4) = 600/(m)_4.
  - E I_5 = 120(m−4)/(m)_4 ≤ 120/(m)_3.
  - E I_{m−5} = 36·120/(m)_5 = 4320/(m)_5.

  Los índices {4, 5, m−5, …, m−2} son distintos si m ≥ 11. El bloque central, con m − 11 valores, está acotado por 720(m−11)(m−5)/(m)_5 ≤ 720/(m)_3 ⇔ 9m ≥ 43. En total, 42/(m)_2 + 936/(m)_3 + 600/(m)_4 + 4320/(m)_5 = F̄(m). Correcto.
- (b) Pr(𝓔) ≤ Σ_{k=4}^{n−2} E I_k + E C(I_3,2) + E[I_3 I_{n−1}] + E C(I_{n−1},2), donde las tres últimas son las fórmulas exactas del Lema B.2(a), verificadas en la ronda 5. Las simplificaciones (n−4)(n−5) ≤ (n−2)(n−3), n−3 ≤ n−2, n−4 ≤ n−3 y 6n−16 ≤ 6(n−2) dan 22/(n)_2 + 8/(n)_3, 24/(n)_2 y 2/(n)_2. Sumando, P̄(n) = 90/(n)_2 + 944/(n)_3 + 600/(n)_4 + 4320/(n)_5. Correcto.
- (c) E I_3(m) = 6(m−2)/(m)_2 ≤ 6/m y E I_{m−1}(m) = 4/m, de donde s̄. En h_m, el término l = 2 vale 2·E I_2/(m−1) = 4/m y el l = 3 vale 3·E I_3/(m−2) = 18/(m)_2. Para l ≥ 4 el factor es ≤ 1, lo que da 8/m + 18/(m)_2 + F̄(m). Correcto.
- Mis cocientes exactos (Fraction, 12 ≤ m ≤ 400) son 0.9579 (a), 0.9773 (b), 0.9981 (s) y 0.9921 (h). El autor obtuvo 0.958 / 0.977 / 0.998 / 0.992, y la salida congelada hasta m = 3000 da 0.9941 / 0.9969 / 0.9998 / 0.9990, que se acercan a 1 por la izquierda, como corresponde al orden dominante 42/m².
- **B(n), término a término contra la prueba del Teorema 5.9:**
  1. ρ_1 ≤ Σ_{k<n}|r_{n,k}| + Σ_{k≥n} q_k k/n ≤ 2^{n+1}/(n(n+1)!) + 1/n!, porque (e^{−1}/n)Σ_{j≥n−1}1/j! < 1/n! para n ≥ 2.
  2. |ρ_2| ≤ E[(1 + #ω)1_𝓔] = Pr(𝓔) + E[#ω; 𝓔]. La primera parte es P̄(n). La segunda es la cota desplegada del Lema B.2(b); revisé otra vez su derivación, con los casos K ∩ J = ∅, K ⊋ J y solape parcial (U = J ∪ K, a lo sumo dos K por U, U = [1, n] solo si i ∈ {1, n−2}): 3(n−2)/(n)_2·(s̄_{n−2} + 3h̄_{n−2}) + 12/(n)_2 + (2/n)(s̄_{n−1} + h̄_{n−1}). El 12/(n)_2 sale de 2 ventanas × 3 patrones × 2 K × 1/(n(n−1)).
  3. Aproximación de cada ocurrencia: |E[g|ω] − E g(N(τ) + Z)| ≤ 2Pr(δ ≠ 0 | ω) + 2d_TV(N_{n−2}, Z). Como g ∈ {−1, 0, 1}, sup_{|f|≤1}|Ef(X) − Ef(Y)| = 2d_TV. Pr(δ ≠ 0 | ω) ≤ 2/(n−2), con P(σ(j+1) = σ(j) − 1) = 1/m, y d_TV(N_m, Z) ≤ d̄_m = e^{−1}/m + 2/(m·m!) para m ≥ 4.
  4. Pesos: 1/n − (n−2)/(n(n−1)) = 1/(n(n−1)), por 3 patrones.

  No falta ninguna pieza.
- Límite: 90 + (102 + 12 + 36) + (12 + 6/e + 4 + 4/e) + 3 = 259 + 10/e = 262.679. Correcto.
- **Monotonía de n²B(n): demostrada, no solo comprobada.** Desarrollé a mano la estructura. Los factores n−2 de los pesos se cancelan con 1/(n−2) de s̄_{n−2}, h̄_{n−2}, 4/(n−2) y e^{−1}/(n−2). Los términos sin factorial son c/∏(n − i_j) con c > 0, al menos dos factores e i_j ∈ {0, …, 6}; el i_j = 6 viene de (n−2)_5 en F̄(n−2). Entonces n²·(término) = c·[n/(n−i_1)]·[n/(n−i_2)]·∏_{j≥3} 1/(n−i_j), producto de funciones positivas no crecientes.
- Los cuatro términos con factorial son n·2^{n+1}/(n+1)!, n²/n!, 12n²/n! y 8n²/((n−1)n!), y sus cocientes consecutivos son < 1 para n ≥ 2. Correcto.
- **Valores (cálculo propio, mpmath a 50 dígitos):** 22²B(22) = 421.4905, 30²B(30) = 363.1054, 100²B(100) = 285.7965 y 1000²B(1000) = 264.7776; n²B(n) es no creciente en 14 ≤ n ≤ 2000. Coinciden con `\SecBtwentytwo` = 421.49, `\SecBhundred` = 285.80 y las cotas `\SecCtwentytwo` = 422 y `\SecChundred` = 286, redondeadas hacia arriba.
- Observación: todos los ingredientes valen ya para n ≥ 14 (Lema B.4 con m = n − 2 ≥ 12), con 14²B(14) = 618.4. El umbral n ≥ 22 es una elección, no una necesidad (opcional, m8).
- Las cuatro piezas en n = 1000 de la salida congelada (91.04 / 151.04 / 19.70 / 3.00) cuadran con 90 / 150 / 16 + 10/e / 3. La frase "90 + 150 of the limit" (main.tex:514) es correcta.

### 0.7 Observación 5.14 y Conjetura 5.15: estado y aritmética

- Etiquetado. En la Observación: "open; κ computationally verified (extrapolation of exact values), not proved"; en la Conjetura: "conjectural"; en la tabla de afirmaciones (main.tex:602): "numerical, not proved; closed form conjectural". En el resumen (:71): "only computed … its closed form is conjectural". En README:5: "solo numérico … conjetura". **Están etiquetados como no demostrados en todos los sitios.** Matiz (m2): "computationally verified" no encaja con un límite extrapolado.
- Aritmética de la conjetura, comprobada a mano:
  - μ_2(2) = −8q_1 < 0, así que no cuenta.
  - μ_2(4) = q_2·1 = 1/(2e).
  - μ_2(8) = 10q_3 = 5/(3e) > 0, que cuenta aunque μ(8) = 0.
  - Σ_{k≥1}(k+1)q_{k−1} = E[Z+2] = 3.
  - Total: 7/2 + 13/(6e) = 4.297072.
- **Comprobación adicional que el texto no usa:** la masa total de segundo orden se anula con las formas conjeturadas. Σ_k μ_2(2^k) = 12E C(Z,4) − 12E C(Z,3) + 12E C(Z,2) − 3E Z − 5 = ½ − 2 + 6 − 3 − 5 = −7/2, Σ_k μ_2(3·2^k) = 3, y la masa fuera de los átomos es ½: −7/2 + 3 + ½ = 0.
- La masa ½ tiene además una explicación heurística sencilla. A orden n⁻², la única razón R/2^N fuera de {2^a, 3·2^a} es (3/2)² = 9/4, que aparece con dos ocurrencias 321 disjuntas. Las demás combinaciones dan razones 3, 4 o 6, y los intervalos de 4 elementos dan t(G_τ) ∈ {1, 2, 4, 6, 24}. El número esperado de pares disjuntos es ≈ C(n,2)·(1/n²)² ≈ 1/(2n²). Ambas comprobaciones refuerzan la conjetura y conviene añadirlas (m2).
- Extrapolación propia, rápida, con los valores congelados n²(d_TV − c_2/n) en n = 250, 300, 400, 500: grado 1 da 4.2959 y grado 2 da 4.29709. Es coherente con 4.29707.

### 0.8 Verificación computacional independiente (resumen; detalle en la sección 5)

- Ley exacta de N_n por una **recurrencia propia**: insertar n en una permutación de [n−1] justo delante de n−1 suma 1, dentro de una de las k sucesiones descendentes resta 1, y en los n−1−k huecos restantes no cambia nada. Es decir, a(n,k) = a(n−1,k−1) + (k+1)a(n−1,k+1) + (n−1−k)a(n−1,k). Coincide con la **fuerza bruta en C sobre todo S_n, n ≤ 11**, y la usé hasta n = 1000.
- Teorema 5.11(ii) con 460 dígitos para **todo** 3 ≤ n ≤ 200: max |d_TV − Φ(1/n)|/cota = 0.19333 (en n = 4). En n = 6, 10 y 20 el cociente vale −0.083, −0.018 y −8·10⁻⁵. Teorema 5.8(i): max |r_{n,k}| n k!(n−k+1)! = 0.9902.
- n²d_TV frente a 3/(4e) + 1/(4en): 0.2768300 / 0.2768293 (n = 100) y 0.2760016 / 0.2760016 (n = 1000).
- Minimización propia sobre λ (rejilla en a = n²(λ − 1 + 1/n) ∈ [−6, 6] más sección áurea; barrido grueso λ ∈ (0, 6]):

| n | a* | n²·mín d_TV | n²d_TV(a = 0) | n²d_TV(a = ½) |
|---|---|---|---|---|
| 6 | 0.4528 | 0.18069 | 0.27958 | 0.19784 |
| 10 | 0.4690 | 0.17810 | 0.28517 | 0.18946 |
| 20 | 0.4839 | 0.18095 | 0.28053 | 0.18685 |
| 50 | 0.4934 | 0.18273 | 0.27775 | 0.18514 |
| 100 | 0.4967 | 0.18333 | 0.27683 | 0.18455 |
| 200 | 0.4983 | 0.18363 | 0.27637 | 0.18425 |
| 500 | 0.4993 | 0.18382 | 0.27609 | 0.18406 |
| 1000 | 0.4997 | 0.18388 | 0.27600 | 0.18400 |

  El límite es 1/(2e) = 0.18394, y n = 1000 coincide con `\SecBestA` = 0.4997 y `\SecBestMin` = 0.18388. En el barrido grueso no hay otros mínimos lejos de λ ≈ 1. El mínimo finito queda por debajo del límite, lo cual es compatible con un límite.
- Ley de R_n. Mi propia implementación en C de R(π) por descomposición por sustitución (½ ∏: 2 por nodo simple, k! por nodo sesgado, 1 por nodo directo; R(id) = 1) coincide, en la distribución completa de S_n para n ≤ 9, con la enumeración del árbitro de la ronda 5. Con ella hice un Monte Carlo con variable de control (ley exacta de 2^{N_n} más la media de 1{R = x} − 1{2^N = x}):
  - n = 22 (10⁷ muestras): n·d_TV = 1.4436 ± 0.0065, frente al "exacto" congelado 1.4439; n²(d_TV − c_2/n) = 5.71, frente a 5.72 congelado y la cota 421.49.
  - n = 50 (5·10⁶): 1.2803 ± 0.014, frente a 1.2798.
  - n = 100 (2·10⁶): 1.2259 ± 0.031, frente a 1.2292.
  - Los átomos en n = 50 coinciden con la parte D2 congelada a ±0.004.

  Además, la d_TV(R_n, 2^Z) congelada para n = 4, 5, 6, 8, 10 coincide en 12 cifras con la que calculo a partir de la enumeración exhaustiva de la ronda 5. **La "ley exacta" de R_n que sostiene la Observación 5.14, la columna "exact" de la Tabla 11 y la cifra 5.72 queda corroborada de forma independiente.**

## 1. Verificación de la ronda anterior (ronda 5)

| id | estado | evidencia |
|---|---|---|
| m1 (notación q_k, τ) | aplicado bien | main.tex:425 "Write $p_k=\Pr(N_n=k)$ and $q_k=e^{-1}/k!$ … $q_k=0$ for $k<0$"; :679 "$\omega=(J,\tau)$ … $\tau\in\{321,231,312\}$"; :472 notación única $q_k(\lambda)$, $\tilde q_k$. `grep` de `\pi_k`, `\pi_{k-`, `p\in\{321`, `p_i\prec`: 0 restos |
| m2 ("agree" en n = 50) | aplicado bien (ver m5 nueva) | main.tex:768 "For $n\ge100$ … agree … At $n=50$ the estimate 1.261 exceeds the first-order value 1.201 by 0.06 (2.9 standard errors) … exact value is 1.280"; 0.06/(0.041/1.96) = 2.87 ✓; tabla de afirmaciones :599; `table_sharp.tex` con columna "exact" (1.280, 1.229, 1.206, 1.195), que mi Monte Carlo confirma (0.8) |
| m3 (n ≥ 6) | aplicado bien | main.tex:679 "For $n\ge6$, the proof of Proposition~\ref{prop:exceptions} shows …" |
| m4 (redondeo del lado seguro) | aplicado bien | experiments/make_numbers.py:23–31 (`up`, `down`), :486 y :508; numbers.tex:225 `\SharpDevMax` 0.96, :236 `\SharpPieceMax` 0.98. Las macros nuevas que son cotas también: `\SecSOneRatio` 0.194 (0.19333), `\SecThetaLo` 0.763 (0.76346, hacia abajo), `\SecThetaHi` 0.9994 (0.99940), `\SecRatioB` 0.0163 (0.016279), `\SecAtomsMax` 3.15 (3.1469), `\SecDtvMaxTT` 5.72 (5.7191), `\SecIntrefA` 0.9942 (0.99414), `\SecCtwentytwo` 422, `\SecChundred` 286 |
| m5 ("closed form") | aplicado bien | la Observación 5.11 desaparece; la frase ya no existe (`grep "closed form"` solo la encuentra en la Conjetura 5.15 y en Φ) |
| m6 (3/(4e) demostrable) | aplicado bien (superado) | Teorema 5.11, verificado en 0.1–0.4 |
| m7 (n ≤ 3) | aplicado bien | main.tex:438. Comprobado a mano: n = 1, d_TV = 1 − e⁻¹; n = 2, 2(½ − e⁻¹); n = 3, p = (½, ⅓, ⅙), d_TV = ½ − e⁻¹. La identidad y la cota 2/(n·n!) se cumplen |
| m8 (antecedentes) | aplicado bien | main.tex:440 "an elementary consequence of the classical exact law~\citep{kaplansky1945}"; tabla :598. Mi búsqueda (WebSearch, ver sección 4) tampoco encuentra un enunciado explícito |
| m9 (c_1) | aplicado bien | main.tex:438 "$\to c_1=\tfrac{e^{-1}}2\sum_{k\ge0}|k-1|/k!=e^{-1}$" |
| m10 (etiquetas) | aplicado bien | "checked by an independent internal referee (round~5)" solo en: Teorema 5.8 (:440), 5.9 (:457), Prop. 5.10 (:466), Lema B.2 (:682), párrafo "Sharp rates" (:425) y fila de la tabla (:598). El segundo orden lleva "not yet independently refereed": :472, :491, :503, :511, fila :600; resumen :71 "not yet refereed"; Limitations :614; README:5, :36; FICHA:11, :13, :22, :24. No hay ninguna etiqueta de la ronda 5 en material que esa ronda no arbitró |
| m11 (Figura 3) | aplicado bien | main.tex:382 `\begin{figure}[tb]`; `main.aux`: fig:e5 en p. 14, con la Tabla 7 (p. 14) |
| Recortes de "Extensión" (1–5) | aplicados bien | Teorema 5.6 sin la parte de d_TV ni (c) (main.tex:409–416); párrafo :418 que remite a 5.8 y 5.10; Tabla 9 sin "exceptions" ni "5/n" (`table_e5f.tex`, 7 columnas); "Numerical check of the sharp rates" condensado (:768); Observación B.1 con un solo ejemplo (4231 → 6, :664) |
| Bibliografía (brignall2010 eprint) | aplicado bien | refs.bib:415–416 `eprint = {0801.0963}`, `note = {arXiv:0801.0963}` (verificado, sección 4) |
| Macros previas | sin cambios indebidos | comparación propia de numbers.tex entre a4c05eb y la versión actual: 253 → 312; cambian solo `\SharpDevMax` y `\SharpPieceMax`; ninguna eliminada; 59 nuevas |
| Separación del material de realizadores | decisión pendiente del autor (no se reabre) | CONTINUIDAD:180 (plan concreto); RESPUESTA ronda 5:55 |

Recuento: 11/11 bien aplicados (+ recortes y bibliografía), 0 a medias, 0 no aplicados, ninguno con error nuevo.

## 2. Hallazgos nuevos

### Bloqueantes
Ninguno.

### Mayores
Ninguno. Los Teoremas 5.11–5.12, la Proposición 5.13 y los Lemas B.3–B.4 son correctos tal como están escritos (sección 0).

### Menores

**m1. La uniformidad en a del Teorema 5.12(i) se usa en (iii) pero no está en el enunciado** (main.tex:499: "For every fixed $a$, …"; uso en :736: "(i) (uniform in $a$)").
*Problema:* (iii) necesita (i) con error O(1/n) uniforme en a ∈ [−½, 3/2], y eso solo lo establece la última frase de la prueba de (i) (:732). Un lector que cite solo el enunciado no puede reconstruir (iii).
*Corrección:* "(i) For every compact set $K\subset\mathbb R$, $n^2d_{\mathrm{TV}}(N_n,\mathrm{Po}(1-1/n+a/n^2))=L(a)/2+O(1/n)$ uniformly in $a\in K$." En (iii): "If $a\in[-\tfrac12,\tfrac32]$, (i) with $K=[-\tfrac12,\tfrac32]$ and (ii) give …".

**m2. Observación 5.14 y Conjetura 5.15: "verified" y "converges" para una extrapolación; la masa ½ queda fuera de lo conjeturado** (main.tex:517, :525).
*Problema:* que n²(·) "converges" para cada átomo y que κ esté "computationally verified" no se puede verificar con valores hasta n = 600. Es una estimación por extrapolación, como dice la tabla de afirmaciones ("numerical, not proved", :602), y las dos etiquetas no coinciden. Además, la fórmula de κ en la Conjetura usa "the mass ½ outside these atoms", que también es solo numérica (`\SecUntracked` = 0.500000), y además supone que la parte positiva de segundo orden viene solo de μ_2(4), μ_2(8) y los átomos 3·2^k.
*Corrección:*
- Observación 5.14: "…the fits indicate that $n^2(\dots)$ converges for each of the 24 atoms…"; estado "open; $\kappa$ estimated numerically (extrapolation of exact values for $n\le600$), not proved".
- Conjetura 5.15: escribir "(a) $\mu_2(2^k)=\dots$, $\mu_2(3\cdot2^k)=\dots$, $\mu_2(3)=0$; (b) $n^2\Pr(R_n\notin\{2^k,3\cdot2^k\})\to\tfrac12$; (c) hence $\kappa=\dots$".
- Añadir el apoyo de 0.7: la masa total de (a)+(b) es −7/2 + 3 + ½ = 0, y (b) es lo que predice el par de ocurrencias 321 (razón 9/4, número esperado ≈ 1/(2n²)).

**m3. Estado de los Lemas B.3 y B.4** (main.tex:716 y :745: "\status{proved here}").
*Problema:* el resto del bloque de segundo orden lleva "not yet independently refereed"; estos dos lemas son igual de nuevos.
*Corrección:* si el coordinador acepta este informe, poner en los Teoremas 5.11–5.12, la Proposición 5.13 y los Lemas B.3–B.4 "proved here; checked by an independent internal referee (round~6)". Hay que hacerlo en main.tex:471–472 (párrafo "Second order"), :491, :503, :511, :716, :745, la fila :600, el resumen :71 ("not yet refereed"), Limitations :614, README:5 y :36, FICHA:11, :13, :22, :24 y CONTINUIDAD. La Observación 5.14 y la Conjetura 5.15 deben seguir "open"/"conjectural". Si no se acepta, añadir al menos "not yet independently refereed" a B.3–B.4.

**m4. La comprobación numérica del Teorema 5.11(ii) no tiene precisión suficiente para n ≳ 100** (main.tex:786: "…wherever that bound exceeds $10^{-130}$, and below $10^{-130}$ elsewhere"; salida congelada, parte A4: en n = 200 el valor calculado |d_TV − Φ| = 5.2·10⁻¹⁵² es ruido y supera la cota 1.0·10⁻³¹⁹).
*Problema:* el texto lo dice con honestidad, pero la comprobación no cubre el rango anunciado (n hasta 1000). Con 150 dígitos solo se comprueba la desigualdad para n ≲ 95.
*Corrección:* usar mp.dps = ⌈log10((n+1)!)⌉ + 30 por cada n. Mi comprobación con 460 dígitos cubre todo 3 ≤ n ≤ 200 en 5 s, con un cociente máximo de 0.1933. Alternativa sin código: "…for $3\le n\le 95$ (where 150 digits suffice), at most 0.194 times the bound".

**m5. "Agree" en n ≥ 100 ahora que hay columna "exact"** (main.tex:768: "For $n\ge100$ the estimates of $n\,d_{\mathrm{TV}}(R_n,2^Z)$ agree with $c_2$ … and with the first-order law"; fila :599).
*Evidencia:* Tabla 11, exacto frente a primer orden: 1.229 − 1.192 = 0.037 (n = 100), 1.206 − 1.188 = 0.018 (200) y 1.195 − 1.186 = 0.009 (400), ≈ κ/n. Los Monte Carlo "coinciden" con el primer orden solo porque sus intervalos (±0.06 a ±0.15) son más anchos que el término n⁻².
*Corrección:* "For $n\ge100$ the estimates agree, within their sampling error, with $c_2$ and with the first-order law; the exact column shows that the $n^{-2}$ term ($\approx\kappa/n$) is present at every $n$ but below the Monte Carlo resolution for $n\ge100$." Fila de la tabla: "… agrees with the first-order law within sampling error for $100\le n\le400$; the exact law shows the $n^{-2}$ term at every $n$".

**m6. "Exact computation" para la ley de R_n hasta n = 600** (tabla de afirmaciones main.tex:601, "verified (exact computation)"; método en :786). *Opcional.*
*Problema:* hasta n = 30 la evaluación es en enteros exactos. Para 30 < n ≤ 600 es en coma flotante, con un error relativo de 1.1·10⁻¹⁵ estimado contra los enteros en n ≤ 30. El sistema de funciones generatrices solo se describe en una frase y no se demuestra; la validación es empírica (n ≤ 8 y n ≤ 6 por el autor; n ≤ 11 por la ronda 5; mi Monte Carlo en n = 22, 50, 100).
*Corrección:* "verified (generating function; exact for $n\le30$, floating point up to $n=600$)". Añadir en :786 una referencia a la derivación (`theory/second_order_derivation.md`, sección correspondiente) o dos líneas con las ecuaciones.

**m7. Umbral n ≥ 22 de la Proposición 5.13** (main.tex:507; prueba :761 "with $m=n-2\ge20$"). *Opcional.*
Todos los ingredientes valen para n ≥ 14: el Lema B.4 exige m = n − 2 ≥ 12, P̄ exige n ≥ 12, d̄ exige m ≥ 4 y la afirmación estructural exige n ≥ 6. Mi cálculo da 14²B(14) = 618.4. No hay error, pero conviene decir que 22 es una elección, o enunciar "for $n\ge14$ … $\le619/n^2$; for $n\ge22$, $\le422/n^2$".

**m8. Soporte de la parte positiva para n pequeño** (main.tex:726). *Opcional, de claridad.*
La prueba es correcta porque no necesita que {k : p_k > q̃_k} = {1, 2}, y de hecho no se cumple en n = 3, 4, 5 ({2}, {1, 3}, {1, 2, 4}). Una frase evitaría la confusión: "(the identity does not require $p_k\le\tilde q_k$ for $k\ne1,2$, which fails for $n\le5$; the difference is absorbed by $\varepsilon_n$)".

**m9. Extensión (33 páginas).** No reabro la decisión pendiente, solo constato lo que cambia. El bloque de segundo orden añade ≈ 3.5 páginas: los enunciados en pp. 17–18, y las pruebas y la comprobación en pp. 27–30. Todo él trata de N_n (sucesiones descendentes) y de la constante del Teorema 5.9, sin ninguna conexión con la pregunta del paper. El material de realizadores y tasas ocupa ya ≈ 13–14 de 33 páginas. Esto refuerza el plan de CONTINUIDAD:180 y RESPUESTA ronda 5:55, que ya incluye 5.11–5.15 y B.3–B.4 en la nota separada, y no requiere cambios mientras la decisión siga abierta. Recortes menores que no dependen de ella:
1. Fundir "Numerical check of the second-order results" (:785–786, ≈ 400 palabras) en la salida congelada y dejar ≈ 150 palabras: −0.3 p.
2. La frase de comparación con la versión 0.7 ("version~0.7 reported this limit only numerically", :494) sobra en un manuscrito: −2 líneas.

## 3. Lectura fresca de las secciones nuevas y encaje con el resto

- La notación del bloque (q_k(λ), q̃_k, c_j(k), h_k, g_a, x = 1/n) es coherente con la de las tasas de primer orden y no choca con π, τ ni p_k. c_j(k) se define antes de usarse (:472), y (1) (`eq:pkqk`, :711) enlaza bien con el Teorema 5.8(i).
- El texto que sigue al Teorema 5.11 (:494) es correcto (ver 0.4), y "consistent with" (en lugar de "which is why") es la redacción adecuada.
- Proposición 5.13 y su párrafo (:514): los valores 5.72 y 8.01 coinciden con la salida congelada (5.7191 y 8.0028, redondeados hacia arriba) y con mi Monte Carlo en n = 22 (5.71). "Most of the gap comes from 𝓔" con 90 + 150 es correcto.
- Resumen (:71): fiel. "at most 422/n² for n ≥ 22", "(3/(4e)+o(1))/n² from Po(1−1/n)" y "n⁻² term … only computed … closed form conjectural" coinciden con lo demostrado. No menciona el Teorema 5.12, cosa aceptable.
- El "Outline of the proofs" (:528) describe bien el método nuevo ("signs of e^x(1−x)^k − 1 − (1−k)x").
- Table 11: el pie (:779) es coherente con la columna nueva, y la cota 422/n de Prop. 5.13 vale en todas las filas (n ≥ 50 ≥ 22).
- README, FICHA y CONTINUIDAD: estados correctos y coherentes con el manuscrito. CONTINUIDAD:151 conserva la lista "Queda abierto tras la ronda 4", con 3/(4e) aún abierto; es histórica, y la lista vigente (tras la ronda 5) está más abajo. No requiere cambio.

## 4. Bibliografía

| entrada | estado | corrección |
|---|---|---|
| `brignall2010` (eprint/note añadidos en v0.8) | verificada por WebSearch: arxiv.org/abs/0801.0963, "A Survey of Simple Permutations", R. Brignall; versión de Cambridge (Permutation Patterns, LMS LNS 376) en cambridge.org/core | ninguna |
| `corteel2006` (DOI) | sigue sin DOI; el autor lo declara pendiente (CONTINUIDAD, "Queda abierto tras la ronda 5", punto 4) | ninguna nueva |
| Antecedentes de 5.11–5.12 | una búsqueda ("number of successions random permutation Poisson approximation total variation rate second order") no encuentra un enunciado explícito de n²d_TV(N_n, Po(1−1/n)) → 3/(4e) ni del mejor parámetro de Poisson para sucesiones. El manuscrito no reivindica novedad para 5.11–5.12 (solo "proved here"), lo cual es adecuado | mantener; la consulta de Barbour–Holst–Janson (1992) sigue pendiente, como declara el autor |

En v0.8 no se añadieron entradas nuevas (47 entradas). WebSearch funcionó a través del proxy; no descargué PDFs de editores.

## 5. Verificación computacional (independiente)

Todo en `/tmp/claude-0/-home-user-ChanoSilva/6d28bda3-759e-5faa-92d7-8739680d15c2/scratchpad/referee6_MRT001/`. Ninguna función del autor, del agente teórico ni de la ronda 5 reutilizada; de la ronda 5 solo leí su `exact.jsonl` como dato de contraste. **CPU total ≈ 65 s**, dentro del presupuesto de 5 min.

1. `bruteN.c`: ley de N_n por fuerza bruta en todo S_n, n ≤ 11, en 0.4 s.
2. `lawN.py`: recurrencia propia (0.8). Coincide con 1 para n ≤ 11, y los momentos factoriales exactos son 1 − r/n (n = 5, 12, 40).
3. `check_thm511.py` (4.9 s): Teorema 5.11(ii)–(iii) y 5.8(i) con mpmath a 460 dígitos (n ≤ 200) y 60 dígitos (n ∈ {300, 500, 700, 1000}). Resultados en 0.3, 0.4 y 0.8. Todos coinciden con `\SecSOneRatio`, `\SecThetaLo/Hi` y `\SecNthousandVal/Pred`.
4. `check_thm512.py` (21.5 s): minimización sobre λ (tabla en 0.8) y fórmula de L(a) (0.5).
5. `check_Bn.py` (3.1 s): Lema B.4 en racionales exactos (12 ≤ m ≤ 400; también que (a) vale ya para 6 ≤ m ≤ 11) y B(n) con mpmath (0.6). Monotonía comprobada en 14 ≤ n ≤ 2000.
6. `rmc.c` + `ana_mc.py` (≈ 30 s): R(π) por descomposición por sustitución, validado contra la distribución completa de S_n (n ≤ 9) de la ronda 5. Monte Carlo con variable de control en n = 22, 50 y 100 (0.8): coincide con la "ley exacta" congelada dentro de 1 EE.
7. `cmp_R.py`: d_TV(R_n, 2^Z) a partir de la enumeración exhaustiva de la ronda 5 frente a la salida congelada en n = 4, 5, 6, 8, 10: 12 cifras iguales.
8. SHA-256: `results/check_second_order_output.txt` = 328efae6…c4c1b0 = `.sha256` = `meta.json` = prefijo de `\SecSha`; `second_order_results.json` = f84eead0…dbf35 = meta ✓. La copia de `theory/` difiere solo en los tiempos ("(0.2s)" y "(42.9s)" en las líneas C1 y C4, y la línea "total CPU time"), que el congelado elimina. No afecta a ningún número.
9. Macros `\Sec*` contrastadas con `second_order_results.json` (C_table, E1, E2, S1_maxratio, theta, best_*, dtvR_*, kappa_*, mu2_conj_maxdev, untracked): todas iguales, con el redondeo del lado seguro en las cotas (sección 1, m4).
10. Compilación en copia (`latexmk -pdf`, 3.4 s, tres pasadas de pdflatex y dos de bibtex): 0 errores, 0 advertencias en el log (sin referencias ni citas indefinidas, sin cajas), `pdftotext | grep -c "??"` = 0, **33 páginas**. Numeración comprobada en `main.aux`: Teorema 5.11 (p. 17), 5.12, Prop. 5.13, Obs. 5.14 y Conj. 5.15 (p. 18); Lema B.3 (p. 27), B.4 (p. 28), ecuación (2) (p. 29), Tabla 11 (p. 30).
11. No relancé `check_second_order.py` (51 s y en `theory/`, que no debo tocar): mis comprobaciones 3–7 cubren de forma independiente sus partes A, E y D (salvo el ajuste de κ, del que repetí solo una extrapolación rápida, 0.7). Tampoco relancé E1–E5f ni `check_sharp_rate.py`, porque no cambiaron.

## 6. Lista final de acciones (prioridad descendente)

1. Enuncia el Teorema 5.12(i) con su uniformidad en a sobre compactos (O(1/n)) y cítala así en (iii) (m1).
2. Cambia "computationally verified" por "estimated numerically (extrapolation …), not proved" en la Observación 5.14 y "converges" por "the fits indicate convergence". Separa en la Conjetura 5.15 la parte (b), masa ½ fuera de los átomos, y añade el cierre de masa −7/2 + 3 + ½ = 0 y la heurística del par 321 → 9/4 (m2).
3. Si el coordinador acepta este informe, cambia a "proved here; checked by an independent internal referee (round 6)" el estado de los Teoremas 5.11–5.12, la Proposición 5.13 y los Lemas B.3–B.4 en todos los lugares de m3 (main.tex, README, FICHA, CONTINUIDAD). Mantén "open"/"conjectural" para la Observación 5.14 y la Conjetura 5.15. Si no lo acepta, añade al menos "not yet independently refereed" a B.3–B.4.
4. Sube la precisión de la parte A4 de `check_second_order.py` a ⌈log10((n+1)!)⌉ + 30 dígitos, o restringe la frase de main.tex:786 a n ≤ 95 (m4).
5. Matiza "agree" en main.tex:768 y en la fila :599 con "within sampling error" y menciona que la columna exacta muestra el término n⁻² (m5).
6. Opcionales: "exact for n ≤ 30, floating point to 600" en la fila :601 y una referencia a la derivación de la función generatriz (m6); umbral n ≥ 14 o nota sobre la elección de 22 (m7); frase sobre el soporte de la parte positiva para n ≤ 5 (m8); recortes de m9.
7. Mantén abiertos los cotejos con fuentes primarias, el DOI de `corteel2006` y la consulta de Barbour–Holst–Janson; la separación del material de realizadores sigue siendo decisión del autor.
