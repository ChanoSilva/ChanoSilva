# Conjetura 5.3 (MRT001 v0.5): derivación paso a paso

Notas de trabajo (incrementales). Entregable: `realizer_law_theorem.tex`. Comprobación numérica: `check_realizer_law.py` -> `check_realizer_law_output.txt`.

## 0. Convenciones (fijadas y verificadas contra el código)

* Puntos `(u_i, v_i)` iid uniformes en `(0,1)^2` (coordenadas nulas). Con probabilidad 1 todas las `u` y todas las `v` son distintas.
* Se ordenan los puntos por `u`: la posición `i` es el `u`-rango. `π(i)` = `v`-rango del punto en la posición `i`. Como `u` y `v` son independientes y continuas, las `v` leídas en orden de `u` siguen siendo iid, luego **π es uniforme en S_n**. Es exactamente lo que hace `experiments/realizer_law.py::descending_successions` (`pi = v_rank[order_u]`).
* Orden causal: `i ≺ j ⟺ i<j y π(i)<π(j)` (orden de dominancia `P(π)`), igual que `lorentzian_chain.causal_order_2d`.
* Grafo de incomparabilidad `G_π`: arista `ij` ⟺ `(i−j)(π(i)−π(j)) < 0` (inversión). Es el **grafo de permutación** de π en la convención estándar (aristas = inversiones). Es grafo de comparabilidad (del orden conjugado `i <* j ⟺ i<j, π(i)>π(j)`) y de cocomparabilidad.
* Prop. 5.2 (ya demostrada en main.tex): `R(π)` := nº de realizadores módulo intercambio = 1 si π = id (cadena), y `t(G_π)/2` en otro caso, con `t(G)` = nº de orientaciones transitivas.
* `N(π)` := #{ i : π(i+1) = π(i) − 1 } (sucesiones **descendentes**), como en `realizer_law.py`.
* **Intervalo** de π: conjunto `[a,b]` de posiciones consecutivas cuyo conjunto de valores es un intervalo de enteros. Triviales: longitud 1 y n. π es **simple** si no tiene intervalos no triviales. Sucesión = intervalo de longitud 2 (ascendente `π(i+1)=π(i)+1` o descendente `π(i+1)=π(i)−1`).
* **Módulo** de un grafo G=(V,E): `M ⊆ V` tal que todo `x ∉ M` es adyacente a todos o a ninguno de M. Trivial: `|M| ≤ 1` o `M = V`. G primo si sólo tiene módulos triviales. G y su complemento tienen los mismos módulos.

## 1. Intervalos y módulos

**Lema 1 (intervalo ⇒ módulo).** Todo intervalo `I` de π es módulo de `G_π`.
*Prueba.* Si `x ∉ I`, la posición de x está a un lado de todas las de I y su valor a un lado de todos los de I; luego x forma inversión con todos o con ninguno. ∎

El recíproco **es falso** a nivel de conjuntos (π = id: G_π sin aristas, `{1,3}` es módulo y no intervalo). Lo que sí vale (y es lo que se necesita):

**Lema 2 (A).** Sea n ≥ 3. Si `G_π` tiene un módulo M con `2 ≤ |M| ≤ n−1`, entonces π tiene un intervalo I con `2 ≤ |I| ≤ n−1`. Equivalentemente (con el Lema 1): para n ≥ 3, π simple ⟺ G_π primo.

*Prueba.* Tomar M módulo no trivial de tamaño mínimo.

(a) *Si G[M] es conexo y co-conexo, M es un intervalo.* Sea `a = min M`, `b = max M` (posiciones) y `x ∉ M` con `a < x < b`. Si x no es adyacente a M: cada `m ∈ M` a la izquierda de x tiene `π(m) < π(x)` y cada uno a la derecha `π(m) > π(x)`; ambos grupos son no vacíos (contienen a y b) y no hay inversiones entre ellos ⇒ G[M] disconexo. Si x es adyacente a todo M: los de la izquierda tienen `π(m) > π(x)`, los de la derecha `π(m) < π(x)` ⇒ todas las parejas izquierda–derecha son inversiones ⇒ complemento de G[M] disconexo. Contradicción en ambos casos: no hay posiciones ajenas a M entre a y b. El mismo argumento con valores (x con `min π(M) < π(x) < max π(M)`) muestra que los valores de M son consecutivos. Luego M es intervalo, con `2 ≤ |M| ≤ n−1`.

(b) *Si G[M] es disconexo:* cada componente C de G[M] es módulo de G (un `x ∉ M` ve todo M igual; un `y ∈ M∖C` no es adyacente a nada de C). Por minimalidad todas las componentes son unitarias, es decir M es independiente, y entonces cualquier par de M es módulo; por minimalidad `|M| = 2`: M = {a,b} son **gemelos falsos**. *Si el complemento de G[M] es disconexo:* igual con co-componentes (un `y ∈ M∖C` es adyacente a todo C) ⇒ `|M| = 2`, **gemelos verdaderos**.

(c) *Gemelos ⇒ intervalo.* Sean `a < b` (posiciones) gemelos falsos, así `π(a) < π(b)`. Si `a < x < b`: x adyacente a a exige `π(x) < π(a)`, adyacente a b exige `π(x) > π(b)`; incompatibles, así que x no es adyacente a ninguno y `π(a) < π(x) < π(b)`. Si `π(a) < π(x) < π(b)` con x fuera de `[a,b]`, x sería adyacente a exactamente uno de los dos: imposible. Luego `[a,b]` tiene exactamente los valores `[π(a), π(b)]`: es un intervalo de longitud ≥ 2. Si es todo `[1,n]` entonces `π(1)=1`, y `[2,n]` es un intervalo de longitud `n−1 ≥ 2`. Gemelos verdaderos: idéntico (`π(a) > π(b)`, los x intermedios son adyacentes a ambos), y en el caso extremo `π(1)=n` da `[2,n]`.

Como ningún grafo de 2 o 3 vértices es conexo y co-conexo, (a)–(c) cubren todos los casos. ∎

Corolario: las permutaciones de longitud 3 nunca son simples (toda permutación de longitud 3 tiene una sucesión), y para m ≥ 4, σ simple ⟹ G_σ primo con ≥ 4 vértices (sin vértices aislados ni universales).

**Lema 3 (conexidad).** G_α es conexo ⟺ α no es suma directa (⊕-indescomponible). Análogo con el complemento y la suma sesgada ⊖.
*Prueba.* Las componentes de G_α son conjuntos de posiciones consecutivas: si `i < j < l`, `i,l ∈ C`, `j ∉ C`, algún arista `xy` de un camino de i a l en C salta sobre j (`x<j<y`, `π(x)>π(y)`), y j no adyacente a x ni a y da `π(x)<π(j)<π(y)`, contradicción. Si la componente de la posición 1 es `[1,j]` con `j<n`, no hay inversiones entre `[1,j]` y `[j+1,n]` ⇒ `α([1,j]) = [1,j]` ⇒ ⊕-descomponible. Recíproco: si `α = β ⊕ γ` no hay aristas entre los bloques. El complemento de `G_α` es `G` de la permutación invertida en valores (`α'(i) = n+1−α(i)`), que intercambia ⊕ y ⊖. ∎

## 2. Orientaciones transitivas: fórmula de producto para grafos de permutación

Notación: `T` orientación transitiva (o.t.) de G; escribo `x→y`. Hecho básico (fuerza Γ de Gallai/Golumbic): si `x~a`, `x~b`, `a≁b`, entonces `x→a ⟺ x→b` (si `a→x→b` la transitividad daría la arista `ab`). Restringir una o.t. a un subgrafo inducido da una o.t.

**Teorema clásico usado (Gallai 1967).** Un grafo de comparabilidad primo tiene exactamente dos orientaciones transitivas (una y su inversa). [Gallai, *Transitiv orientierbare Graphen*, Acta Math. Acad. Sci. Hungar. 18 (1967) 25–66; trad. inglesa en Ramírez Alfonsín–Reed (eds.), *Perfect Graphs*, Wiley 2001. Ver también Golumbic 1980, cap. 5; Möhring 1985.] Es el único resultado de teoría de grafos que **no** demuestro; se comprueba numéricamente para todas las permutaciones simples con n ≤ 8 (sección 5).

**Lema 4 (raíz prima).** Sea `π = σ[α_1,…,α_m]` (inflación: la posición j de σ se sustituye por un bloque B_j de posiciones consecutivas con patrón α_j y valores consecutivos, ordenados según σ) con G_σ primo y m ≥ 3. Entonces
`t(G_π) = t(G_σ) · ∏_j t(G_{α_j})`.

*Prueba.* Los bloques son intervalos, luego módulos (Lema 1), y el cociente es G_σ.

(i) *Uniformidad.* Fijo una o.t. T, un bloque B, y defino `S = { y ∉ B : y ~ B, ∃ b1,b2 ∈ B con b1→y→b2 }` (vértices "mixtos"). Afirmo que `B ∪ S` es módulo:
 - si `y ∈ S`, `z ~ y`, `z ∉ B`, `z ≁ B`: en y, `b1→y` y `b1≁z` fuerzan `z→y`; `y→b2` y `b2≁z` fuerzan `y→z`. Contradicción. Así `N(y)∖B ⊆ N(B)`.
 - si `y ∈ S`, `w ∈ N(B)∖B`, `w ≁ y`: en b1, `b1→y`, `y≁w` fuerzan `b1→w`; en b2, `y→b2`, `y≁w` fuerzan `w→b2`. Luego `w ∈ S`.
 - por tanto, `z ∉ B∪S`: si `z ≁ B` entonces `z ≁ S` (primer punto); si `z ~ B` entonces `z ~ S` (segundo punto). Módulo. ✓
Supongamos `S ≠ ∅`. (α) La unión `M''` de los bloques que cortan a `B∪S` es módulo (si M' es módulo y un bloque B' (módulo) corta a M', `M'∪B'` es módulo: un `z` fuera ve M' con un estado s y B' con el mismo estado porque B'∩M'≠∅). `M''` contiene ≥ 2 bloques y su conjunto de índices es módulo de G_σ ⇒ (primo) son todos: `B∪S` corta a todos los bloques. (β) Si existe `z ∉ B∪S`, z ve `B∪S` con un estado constante y `B∪S` tiene un elemento en cada bloque distinto del de z ⇒ el vértice `[z]` de G_σ es universal o aislado ⇒ `V(G_σ)∖{[z]}` es módulo no trivial (m ≥ 3): contradicción. (γ) Si `B∪S = V`, todo vértice fuera de B es adyacente a B ⇒ `[B]` universal en G_σ: contradicción. Luego `S = ∅`: **para todo `y ∉ B` adyacente a B, todas las aristas `y–B` tienen la misma orientación respecto de y.** Aplicando esto a ambos extremos, todas las aristas entre dos bloques adyacentes B, B' tienen la misma dirección.

(ii) *Biyección.* `T ↦ (T restringida a un representante por bloque, T|B_1, …, T|B_m)` es inyectiva por (i). Es sobreyectiva: dada una o.t. T_σ de G_σ y o.t. T_j de cada G[B_j], defino T elevando T_σ a todas las aristas entre bloques y usando T_j dentro de B_j. Transitividad de `a→b→c`: tres bloques distintos → viene de T_σ; `a,b` en el mismo bloque y c fuera → `[b]→[c]` y a está en el bloque de b ⇒ `a→c`; `b,c` en el mismo bloque → análogo; `a,c` en el mismo bloque y b fuera → `[a]→[b]→[a]`, imposible; los tres en un bloque → T_j. ∎

**Lema 5 (raíz serie / paralela).** Si `π = α_1 ⊕ ⋯ ⊕ α_k` entonces `t(G_π) = ∏ t(G_{α_i})` (unión disjunta). Si `π = α_1 ⊖ ⋯ ⊖ α_k` con cada α_i ⊖-indescomponible, entonces `t(G_π) = k! · ∏ t(G_{α_i})`.
*Prueba (⊖).* G_π es la unión completa (join) de los G_{α_i}, cada uno co-conexo (Lema 3). Si `x ∈ H_j` y `a,b ∈ H_i` (i≠j) no adyacentes, la fuerza Γ en x da la misma orientación; por co-conexidad todo H_i se orienta igual respecto de x; aplicándolo en ambos sentidos, todas las aristas entre H_i y H_j tienen la misma dirección. La orientación cociente es una o.t. de K_k, i.e. un orden lineal: k! elecciones; la elevación es transitiva por el mismo análisis de casos del Lema 4. ∎

**Proposición 6 (fórmula exacta).** Para toda π ≠ id,
`R(π) = ½ ∏_{nodos del árbol de sustitución de π} f(nodo)`, con `f(simple) = 2`, `f(⊖ con k hijos) = k!`, `f(⊕) = 1`; y `R(id) = 1`.
*Prueba.* Inducción sobre n con el teorema de descomposición por sustitución (toda π de longitud ≥ 2 es ⊕-descomponible, ⊖-descomponible, o `σ[α_1..α_m]` con σ simple de longitud m ≥ 4; Albert–Atkinson 2005), Lemas 2, 4, 5 y Gallai (t(G_σ)=2). Para el Teorema principal **no se necesita** el teorema de descomposición: allí la σ se construye explícitamente.

Traducción a grafos: ⊕ ↔ nodo paralelo (bloques sin aristas entre sí en G_π), ⊖ ↔ nodo serie, simple ↔ primo. Así la fórmula coincide con la de Gallai `∏ (2 por primo, k! por serie, 1 por paralelo)` sobre el árbol de descomposición modular del grafo de incomparabilidad. **Convención determinada:** una sucesión **descendente** es un módulo K_2 del grafo de incomparabilidad (nodo serie, factor 2! = 2); una **ascendente** es un módulo de dos vértices no adyacentes (nodo paralelo, factor 1).

## 3. El suceso típico y la ley 2^N

**Suceso E_n:** π no tiene intervalos de longitud k con `3 ≤ k ≤ n−1`.

**Lema 7 (estructura en E_n).** Sea n ≥ 5 y π ∈ E_n. Entonces las sucesiones de π son disjuntas dos a dos, la permutación σ obtenida contrayendo cada sucesión a un punto es simple de longitud m ≥ 4, `π = σ[α_1..α_m]` con `α_j ∈ {1, 12, 21}`, y
`t(G_π) = 2^{N(π)+1}`, `R(π) = 2^{N(π)}`.
*Prueba.* Dos sucesiones solapadas `{i,i+1}`, `{i+1,i+2}` forman un intervalo de longitud 3. Contrayendo las s sucesiones queda σ de longitud `m = n − s ≥ ⌈n/2⌉ ≥ 3`. Si J es intervalo de σ con `2 ≤ |J| ≤ m−1`, la unión I de sus bloques es intervalo de π con `|J| ≤ |I| ≤ 2|J|` e `|I| ≤ n−1` (falta un bloque); `|I| ≥ 3` contradice E_n y `|I| = 2` sería una sucesión no contraída. Luego σ simple y, como ninguna permutación de longitud 3 es simple, `m ≥ 4`. Por el Lema 2, G_σ es primo; por Gallai, `t(G_σ) = 2`; por el Lema 4, `t(G_π) = 2 · 2^{#bloques 21}` (t(G_21) = t(K_2) = 2, t(G_12) = t(2K_1) = 1) `= 2^{N+1}`. π ≠ id, así que `R = t/2 = 2^N` (Prop. 5.2). ∎

**Lema 8 (primer momento).** Sea `I_k` el nº de intervalos de longitud k. `E I_k = (n−k+1)^2 k!(n−k)!/n! = (n−k+1)^2 / C(n,k)` (posición inicial, valor inicial, k!(n−k)! ordenaciones). En particular
`E I_2 = 2(n−1)/n`, `E I_3 = 6(n−2)/(n(n−1))`, `E I_{n−1} = 4/n`, `E I_{n−2} = 18/(n(n−1))`, `E I_{n−3} = 96/(n(n−1)(n−2))`, `E I_4 = 24(n−3)/(n(n−1)(n−2))`, `E I_{n−4} = 600/(n(n−1)(n−2)(n−3))`,
y para `5 ≤ k ≤ n−5`, `E I_k ≤ (n−4)^2/C(n,5)`, con `n−9` términos cuya suma es `≤ 120(n−4)(n−9)/(n(n−1)(n−2)(n−3)) ≤ 120/n^2` (pues `n(n−4)(n−9) ≤ (n−1)(n−2)(n−3)` ⟺ `7n^2 − 25n − 6 ≥ 0`). Para n ≥ 20:
`P(E_n^c) ≤ s_n := Σ_{k=3}^{n−1} E I_k ≤ 10/n + 171/n^2`
(6/n + 4/n más `19 + 24 + 5.7 + 2.1 + 120 ≤ 171` sobre n^2). Asintóticamente `s_n = 10/n + O(n^{-2})`. (Comprobado numéricamente en la sección 5.)

**Lema 9 (momentos factoriales de N, exactos).** Para `0 ≤ r ≤ n−1`, `E[(N)_r] = 1 − r/n`; `E[(N)_r] = 0` si r ≥ n.
*Prueba.* Para un conjunto A de r índices de `[n−1]`, el suceso `{π(i+1) = π(i)−1 ∀ i∈A}` dice que cada racha maximal de A (índices consecutivos `i..i+l−1`) ocupa posiciones `i..i+l` con valores consecutivos decrecientes. Contraer cada racha a un elemento es una biyección con `S_{n−r}` (inversa: inflar con bloques decrecientes de las longitudes dadas). Luego la probabilidad es `(n−r)!/n!` sea cual sea A, y `E[(N)_r] = r!·C(n−1,r)·(n−r)!/n! = (n−r)/n`. ∎
(Caso r = 1: `E N = (n−1)/n`, como en main.tex.) Como N ≤ n−1 es acotada, inclusión–exclusión es exacta:
`P(N=j) = (1/j!) Σ_{s=0}^{n−1−j} ((−1)^s/s!) (1 − (j+s)/n)` (verificado a mano para n=2,3: n=3 da 3/6, 2/6, 1/6).
Cota: `|P(N=j) − e^{−1}/j!| ≤ 1/(j!(n−j)!) + e(j+1)/(n·j!)`; sumando, `Σ_j |P(N=j) − e^{−1}/j!| ≤ 2e^2/n + (2^n+1)/n!`, i.e.
`d_TV(N, Poisson(1)) ≤ e^2/n + (2^n+1)/(2·n!)`.
Además `P(N=j) = (e^{−1}/j!)(1 − (j−1)/n) + O(1/(n−j)!)`; p.ej. `P(N=0) ≈ e^{−1}(1+1/n)` (consistente con el conteo clásico de permutaciones sin sucesiones).
Clásico: Wolfowitz (1944), Kaplansky (1945) (sucesiones *ascendentes*; π ↦ π∘reverso intercambia ambos tipos y preserva la uniformidad).

**Teorema (ley de los realizadores).** Sea R_n el nº de realizadores módulo intercambio del orden causal de n puntos iid uniformes del diamante 1+1 y N_n el nº de pares adyacentes en ambos órdenes de coordenadas con direcciones opuestas. Para n ≥ 20:
(a) `P(R_n ≠ 2^{N_n}) ≤ P(E_n^c) ≤ 10/n + 171/n^2`;
(b) `E[(N_n)_r] = 1 − r/n` y `d_TV(N_n, Po(1)) ≤ e^2/n + (2^n+1)/(2 n!)`;
(c) `d_TV(R_n, 2^Z) ≤ (10 + e^2)/n + 172/n^2`, Z ~ Po(1). En particular `P(R_n=1) → e^{−1}`, `P(R_n=2) → e^{−1}`, `P(R_n ≤ 8) → (8/3)e^{−1}`, con error O(1/n).

## 4. Las excepciones: de dónde salen y cuánto valen

Con probabilidad `1 − O(n^{−2})`, π tiene a lo sumo un intervalo J con longitud en `[3, n−1]` y, si existe, `|J| ∈ {3, n−1}` (Lema 8 para longitudes 4..n−2; pares de intervalos de longitud 3 disjuntos: `≤ 18 n^2 (n−4)!/n!`; solapados ⇒ unión de longitud 4 o 5; un intervalo de longitud 3 junto a `π(1) ∈ {1,n}` o `π(n) ∈ {1,n}`: `≤ 24/n^2 + 12/(n(n−1))`; dos intervalos de longitud n−1: `2/(n(n−1))`).

* `|J| = 3` con patrón p: contrayendo J y las sucesiones exteriores, σ es simple (mismo argumento del Lema 7), y por el Lema 4 `t(G_π) = 2·t(G_p)·2^{N_ext}`. Con `N = N_ext + N(p)`: `R/2^N = t(G_p)/2^{N(p)}`:
  * `123`: t=1, N(p)=0 → 1;  `132 = 1⊕21`, `213 = 21⊕1`: t=2, N(p)=1 → 1 (sin excepción);
  * `321 = 1⊖1⊖1`: t = 3! = 6, N(p) = 2 → **3/2**;
  * `231 = 12⊖1`, `312 = 1⊖12`: t = 2! = 2, N(p) = 0 → **2**.
* `|J| = n−1`: `π(1)=1` (`1⊕π'`, factor 1), `π(n)=n` (factor 1), `π(1)=n` (`1⊖π'`, raíz serie con 2 hijos: factor 2!=2, y `π(2) ≠ n−1` en el suceso) → **2**, `π(n)=1` → **2**.
* Factor **3** (y 4, 6, ...): combinaciones de lo anterior o raíz serie con 3 hijos (`π(1)=n` y `π(n)=1`, o `π(1)=n, π(2)=n−1`): probabilidad `O(n^{−2})`.

Cada patrón de longitud 3 aparece con esperanza `(n−2)/(n(n−1))`, y `P(π(1)=n) = P(π(n)=1) = 1/n`. Por tanto
**`P(R_n ≠ 2^{N_n}) = 3(n−2)/(n(n−1)) + 2/n + O(n^{−2}) = 5/n + O(n^{−2})`**
(cota superior: lo anterior; inferior: Bonferroni, con intersecciones O(n^{−2})). Comparación con la Tabla E5f: n=20: 5/n = 0.25 vs 49/200 = 0.245; n=50: 0.10 vs 21/200 = 0.105; n=100: 0.05 vs 8/200 = 0.04; n=200: 0.025 vs 2/100; n=300: 0.017 vs 2/100; n=500: 0.010 vs 1/50.
