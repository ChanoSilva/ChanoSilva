# LMI001: invariancias de J y pesos de tamaño (Next steps (d), (c) y (b))

Fecha: 03/10/2026. Trabajo de teoría sobre el manuscrito v0.3 (`manuscript/main.tex`, que **no** se modificó). Esta carpeta contiene:

- `invariances.tex`: bloques LaTeX listos para pegar (P, A, B, C, D). La cabecera indica dónde va cada uno y qué frases de la v0.3 cambian.
- `check_invariances.py`: verificación con rangos exactos sobre ℚ (`fractions.Fraction`). Su salida está en `check_invariances_output.txt` (22 s de CPU, semilla 20261003).
- Este documento: la derivación completa, en español.

Notación: J_K(C) = tr K − Σ_c 1_cᵀK1_c/n_c (Def. 2.2 de main.tex, verificada). Los clústeres son no vacíos. P = I − 11ᵀ/n. D(K)_ij = K_ii + K_jj − 2K_ij es la disimilitud inducida.

---

## (d) ¿Agota el Lema 3.1 las invariancias de J?

### Resultado (Proposición `prop:invcomplete`, demostrada aquí)

Sean n ≥ 3, 2 ≤ k ≤ n−1 y Δ simétrica. J_Δ es constante sobre las k-particiones si y solo si Δ = σI + g1ᵀ + 1gᵀ. En ese caso J_Δ ≡ σ(n−k).

- dim V_{n,k} = n+1, y V_{n,k} no depende de k.
- k ∈ {1, n}: hay una sola partición y V = Sym_n, de dimensión n(n+1)/2.
- No hay más excepciones: k = n−1 y n = 3 **no** son excepcionales.
- El espacio W_n de las Δ con J_Δ(C) = α + β(n−k) para todas las particiones, con cualquier k, coincide con V_{n,2}. Además α = 0 y β = σ.
- 11ᵀ no aporta una dimensión aparte: 11ᵀ = g1ᵀ + 1gᵀ con g = ½·1.
- Forma equivalente: J_K − J_{K'} es constante ⇔ D(K) − D(K') es constante fuera de la diagonal ⇔ P(K−K')P ∈ ℝP.

### Demostración paso a paso

1. **Suficiencia.** Es el Lema 3.1: σI aporta σ(n−k), y g1ᵀ+1gᵀ aporta 0.
2. **Unicidad de (σ, g).** Supongamos σI + g1ᵀ + 1gᵀ = 0. Fuera de la diagonal, g_i + g_j = 0 para i ≠ j. Con un tercer índice l, g_i = ½[(g_i+g_j) + (g_i+g_l) − (g_j+g_l)] = 0, así que g = 0 y luego σ = 0. Por tanto dim = n+1.
3. **Reducción a diagonal nula.** Sea f = ½ diag(Δ) y e = Δ − f1ᵀ − 1fᵀ. Entonces diag(e) = 0 y J_e = J_Δ por el Lema 3.1. Con diagonal nula, J_e(C) = −2 Σ_c (1/n_c) Σ_{i<j∈C_c} e_ij = −2·𝓔(C), que es la energía por partícula con "resortes" e_ij. Hay que probar que, si 𝓔 es constante, e es constante fuera de la diagonal.
4. **Intercambio, caso k ≥ 3.** Tomemos p, i, j distintos y R = [n] ∖ {p,i,j}. Como |R| = n−3 ≥ k−2 ≥ 1, fijamos una partición de R en k−2 bloques no vacíos. Comparamos {{p,i},{j},R} con {{p,j},{i},R}: 𝓔 cambia en ½(e_pi − e_pj). Como 𝓔 es constante, e_pi = e_pj.
5. **Intercambio, caso k = 2.** Sea U = [n] ∖ {i,j} y γ_x = e_ix − e_jx. Para P ⊆ U y Q = U∖P comparamos {P∪{i}, Q∪{j}} con {P∪{j}, Q∪{i}}. La diferencia es (1/(|P|+1)) Σ_P γ − (1/(|Q|+1)) Σ_Q γ = 0.
   - Con P = ∅ se obtiene Σ_U γ = 0.
   - Con P = {p}: γ_p/2 + γ_p/(n−2) = 0, luego γ_p = 0.
6. **Conclusión.** En ambos casos, dos aristas que comparten un vértice tienen el mismo peso. Cualquier par de aristas queda enlazado así (e_ab = e_ad = e_cd), de modo que e_ij = −σ para todo i ≠ j. Entonces e = σI − σ11ᵀ y Δ = σI + g1ᵀ + 1gᵀ con g = f − (σ/2)1.
7. **Formas equivalentes.** D es lineal, su núcleo es {g1ᵀ+1gᵀ} y D(σI) = 2σ(11ᵀ − I). El centrado M ↦ PMP tiene el mismo núcleo y P(σI)P = σP. Además, J_K(C) = Σ_c (1/n_c) Σ_{i<j∈C_c} D(K)_ij, que es el coste de *pairwise clustering* de Hofmann–Buhmann para D(K). Por tanto la proposición es el **recíproco de la invariancia por desplazamiento de Roth et al. (2003)**: el coste determina las disimilitudes fuera de la diagonal salvo una constante aditiva.

**Literatura.** La suficiencia es Roth et al. (2003) / Dhillon–Guan–Kulis (ya citados en el Lema 3.1). No conocemos un enunciado publicado del recíproco, pero la búsqueda no fue exhaustiva (no se consultaron bases en esta sesión). Etiqueta propuesta: "proved here (elementary)", sin reclamar prioridad.

### Corolario: todos los representantes y el desplazamiento mínimo (`cor:reps`)

Las K' con J_{K'} − J_K constante son exactamente K + σI + g1ᵀ + 1gᵀ. Existe una PSD con coeficiente σ si y solo si σ ≥ σ_*(K) := max{−cᵀKc : c ⊥ 1, ‖c‖ = 1}.

- Necesidad: para c ⊥ 1, cᵀK'c = cᵀKc + σ‖c‖².
- Suficiencia: P(K+σI)P pertenece a la clase y es PSD si y solo si σ ≥ σ_*.

En el lenguaje de disimilitudes, este umbral es el desplazamiento mínimo de Roth et al. (2003). Lo recordamos así, pero **no lo cotejamos con el texto**; por eso la etiqueta remite a ellos.

### Consecuencia para el resorte con longitud de reposo (`cor:rest`, demostrada aquí)

Un núcleo κ independiente de los datos es un *representante* si, para todo conjunto X de n ≥ 3 puntos distintos y algún (equivalentemente, todo) k ∈ [2, n−1], J_{κ[X]} − J_{−A[X]} es constante.

(a) Los representantes son exactamente κ(x,y) = −φ(‖x−y‖) + g(x) + g(y) + σ[x=y], con g una función y σ una constante globales.
- Para cada X la proposición da un único (σ_X, g_X).
- Si X ⊆ Y, la restricción de la descomposición de Y es una descomposición de X; por unicidad, σ_X = σ_Y y g_X = g_Y|_X.
- Pasando por X ∪ X', σ es una sola constante y g está bien definida.
- Esta es exactamente la clase "K̃ + f + f + a + σδ" de m4 (ronda 2).

(b) Para φ = (d−r)², ningún representante es PD.
- Sobre X_s = {0, su, 2su, 3su}, con c = (1,−1,−1,1), la forma cuadrática vale −8rs + 4σ (verificado exactamente por el script), que es negativa para s > σ/2r.
- Cuantitativamente, σ_*(−A[X_s]) ≥ 2rs. El script obtiene numéricamente σ_* = 2rs exactamente para r = 1 y s ∈ {0.5, 1, 5, 50}.
- Por tanto, el desplazamiento mínimo del Teorema 3.2(b) no está acotado sobre conjuntos de datos.

(c) Sigue valiendo si solo se exige J_{κ[X]} = λ_X J_{−A[X]} + cte con λ_X > 0 dependiente de X.
- Por restricción, (λ_X − λ_Y)A[X] ∈ V.
- A[X_s] ∉ V porque (s−r)², (2s−r)², (3s−r)² nunca son las tres iguales con s > 0. Entonces λ es común a todos los X_s, σ también, y se aplica (b).

**Conclusión para el manuscrito.** La frase abierta de la Prop. 3.3 ("Whether Lemma 3.1 lists all…, we leave open") queda cerrada en el sentido de *valores salvo constante*: el resorte con longitud de reposo no tiene ningún representante PD independiente de los datos. Para cada conjunto de datos sí existe uno, K + σI con σ ≥ σ_*(X), pero σ_* crece al menos como 2rs.

### Sentido débil: "mismos minimizadores" (`rem:argmin`)

- **Lo que se puede decir.**
  1. Si una Δ fija conserva argmin J para toda K (incluso solo para toda K PD), entonces Δ ∈ V. Basta tomar K = λI − Δ con λ grande: J_{K+Δ} es constante, así que todo es minimizador, mientras que argmin J_K = argmax J_Δ es un subconjunto propio. Como transformación uniforme de la matriz, "mismos minimizadores" no añade nada.
  2. Sobre un conjunto de datos fijo, la noción es vacía. Hay representantes PSD con los mismos minimizadores: K+σI, o la matriz de bloques de un minimizador único.
  3. Las reparametrizaciones afines positivas, con factor dependiente de los datos, quedan excluidas (cor:rest(c)).
- **Lo que no.** No sabemos si existe un κ PD independiente de los datos con los mismos minimizadores que −A[X] para todo X y todo k. Hay una condición necesaria: en ternas con k = 2, J_K({i},{j,l}) = ½D(K)_jl, así que el par más cercano en la métrica de características de κ debe ser el par cuya distancia está más cerca de r. Es una condición ordinal, y el álgebra lineal usada aquí no la alcanza. Queda abierta.

---

## (c) Pesos de tamaño y k-means con núcleo ponderado

Definiciones:

- J^ω_K(C) = Σ_i ω_iK_ii − Σ_c (Σ_{i,j∈C_c} ω_iω_jK_ij)/ω(C_c), con ω > 0 fijado antes de la partición (Dhillon–Guan–Kulis 2004, 2007).
- F^w_A(C) = Σ_c w(n_c) Σ_{i<j∈C_c} A_ij. Solo intervienen w(2), …, w(n−k+1); w(1) es irrelevante.

**Hechos previos.**

1. 𝒢_ω = {J^ω_K} es un espacio lineal de dimensión ≤ C(n,2). El núcleo de K ↦ J^ω_K contiene {g1ᵀ+1gᵀ}, que tiene dimensión n.
2. 𝒢_ω contiene las constantes: J^ω_{diag(1/ω)} ≡ n−k. Por eso "salvo constante y signo (o factor positivo)" no añade nada.
3. Las matrices de Hooke en ℝ, M(x)_ij = (x_i−x_j)², generan todas las simétricas de diagonal nula: M(e_a+e_b) − M(e_a) − M(e_b) = −2(E_ab+E_ba). Como M es polinómica, basta un abierto de configuraciones con puntos distintos. Así, "para toda A" y "para toda A de resorte de Hooke" son la misma condición lineal.

### Proposición `prop:weights` (pesos por punto fijos; demostrada aquí)

Sean n ≥ 5, 3 ≤ k ≤ n−2 y w(2) ≠ 0. Existe ω > 0 tal que toda F^w_A es J^ω_K + cte ⇔ w(m) = 2w(2)/m para m = 2, …, n−k+1 (es decir, w ∝ 1/m). En ese caso basta ω = 1 y K = −w(2)A.

Demostración de (⇒):
1. Las C(n,2) funciones F^w_{E_ab} y la constante viven en 𝒢_ω, de dimensión ≤ C(n,2). Por tanto son linealmente dependientes: existe e ≠ 0 con F^w_e constante.
2. El intercambio {p,i},{j},R ↔ {p,j},{i},R da w(2)(e_pi − e_pj) = 0, así que e ≡ ε ≠ 0.
3. Entonces Σ_c h(n_c) es constante sobre los vectores de tamaños, con h(m) = w(m)·C(m,2) y h(1) = 0.
4. Comparando (m+1, 1, ρ) con (m, 2, ρ), donde ρ tiene k−2 ≥ 1 partes: h(m+1) − h(m) = h(2). Luego h(m) = (m−1)h(2), es decir, w(m) = 2w(2)/m.

**Caso k = 2.** El argumento da solo que h(a) + h(n−a) es constante (si w(n−1) ≠ 0 y w(2)+w(n−2) ≠ 0).
- Con n = 4, eso equivale de nuevo a w ∝ 1/m.
- Con n ≥ 5 hay pesos w no proporcionales a 1/m que cumplen esa simetría. Para ellos el conteo de dimensiones no decide; queda abierto.
- Ninguno de los candidatos probados (1, 1/m², 1/(m−1), 1/C(m,2), m) está en ese caso para n ≤ 7 (salida (ii')).

**Como familia.** Si w es una sola función de todos los tamaños y se exige la representación para todo n y k, entonces w(m) ∝ 1/m para todo m ≥ 2 (basta tomar k = 3 y n grande).

**Observación numérica (no es teorema).** Con w = 1/m y un ω aleatorio no uniforme, W_w ⊄ 𝒢_ω en todos los casos n ≤ 7. El peso 1/m necesita, en esos ejemplos, el ω uniforme.

### Proposición `prop:weightsdd` (pesos dependientes de A; demostrada aquí)

Sean 2 ≤ k ≤ n−2 y A ≥ 0 fuera de la diagonal, no nula. Por ejemplo, cualquier resorte con φ(d) > 0 para d > 0 sobre puntos distintos. Entonces E_tot no es J^ω_K + cte para **ningún** ω > 0, aunque ω dependa de A. Lo mismo vale para F^w_A si w(3) > 0, w(3) ≥ w(2) y (k ≥ 3 o (n,k) = (4,2)).

Certificado (anulador explícito):
1. Partimos [n] en k+2 grupos, con a y b (A_ab > 0) en grupos distintos. Fijamos k−2 grupos como clústeres y llamamos G_1, …, G_4 a los otros cuatro.
2. Para cada una de las 7 biparticiones {X, Y} de {1,2,3,4} definimos ν(C_X) = ε(X)·ω̂(X)·ω̂(Y), con ε = +1 si |X| ∈ {1,3} y ε = −1 si |X| = 2. Fuera de esas 7 particiones, ν = 0.
3. Σν = 0, porque cada par de grupos queda separado en exactamente 2 de los 3 cortes 2+2.
4. ν ⟂ 𝒢_ω: basta Σ_{S∋t,u} ε(S)ω̂(Sᶜ) = 0 para todo t, u. Se comprueba en dos líneas: el caso t = u y el caso t ≠ u.
5. ⟨ν, E_tot⟩ = 2 Σ_{t<u} Â_tu ω̂_v ω̂_z ≥ 2A_ab ω̂_3 ω̂_4 > 0, donde {v,z} es el par complementario.
6. Con grupos unitarios y peso w, el emparejamiento es ⟨ν, F⟩ = Σ_{t<u} A_tu [(w(3)−w(2)) ω̂(tu) ω̂(vz) + 2w(3) ω̂_v ω̂_z].

El script verifica la anulación y la fórmula del emparejamiento exactamente, con 200 pares (ω, A) racionales aleatorios.

**Consecuencias.**
- La energía total (máx-k-corte / min-sum k-clustering) **no** es un k-means con núcleo ponderado para matrices de resortes no negativas, ni siquiera con pesos que dependan de los datos. Esto la distingue de la *ratio association* y del corte normalizado (Dhillon et al.).
- Para pesos decrecientes con w(3) < w(2) (1/m², 1/C(m,2)), el corchete cambia de signo, el certificado no aplica, y **no sabemos** si pesos dependientes de los datos los representan.
- La Prop. `prop:weights` sí excluye pesos fijos para ellos.

**Expectativa del encargo frente a resultado.** El encargo esperaba que w ≡ 1 "funcionara vía otra construcción". El resultado es el contrario: w ≡ 1 **no** es k-means con núcleo ponderado, ni con pesos fijos (Prop. weights, con k ≥ 3, o k = 2 para n ≤ 7 por rango exacto) ni con pesos dependientes de los datos para A ≥ 0 (Prop. weightsdd). El manuscrito ya la trata por separado, como máx-k-corte (Thm 3.2(d)), y eso es correcto. Lo que conviene **no** decir es que sea un kernel k-means.

**Literatura.** Las equivalencias positivas (ratio association, ratio cut, corte normalizado ↔ k-means con núcleo ponderado) son de Dhillon–Guan–Kulis. No conocemos un enunciado de los recíprocos y la búsqueda no fue exhaustiva.

---

## (b) Problema abierto 4.2 (opcional; no resuelto)

**Hallazgo.** El enunciado actual es **trivial**: con a ≡ 0, toda partición minimiza (y con w = 1/n_c, también cualquier a constante). Hay que exigir "minimizador **único**" (bloque D de `invariances.tex`).

Con unicidad:
- Una configuración aislada con todas las distancias distintas nunca es contraejemplo. Con a = −1 en las distancias internas de P y a = 0 en las demás, P es el minimizador único para w ∈ {1, 1/n_c}: para w = 1/n_c es ½J_{B_P} + cte, y para w = 1 cuenta los pares de P que se mantienen juntos.
- Un contraejemplo necesita distancias repetidas: dentro de una configuración, o entre varias configuraciones que comparten distancias (subconjuntos de una red).
- Para un número finito de configuraciones, la condición es un sistema finito de desigualdades estrictas lineales en los valores de a. Normalizando F(C) − F(P) ≥ 1, su infactibilidad se certifica exactamente con un certificado de Farkas sobre ℚ.

**No se hizo** en esta sesión, por presupuesto. Queda descrito el método.

---

## Verificación (`check_invariances.py`, salida en `check_invariances_output.txt`)

| Bloque | Qué comprueba | Resultado |
|---|---|---|
| (i) | dim V_{n,k} por rango exacto, para 2 ≤ n ≤ 7 y todo k (27 casos) | coincide con la fórmula en 27/27; span{I, g1ᵀ+1gᵀ} ⊆ V con rango n+1 |
| (i') | dim W_n = n+1, para n = 2..7 | 6/6 |
| (ii) | Para n = 4..7, 2 ≤ k ≤ n−2 y seis pesos: rango de {F^w_{E_ab}} ∪ {1} | C(n,2)+1 (completo) para todo w ≠ 1/m; C(n,2) para 1/m |
| (ii) | rango de 𝒢_1 y de 𝒢_ω (ω aleatorio) | C(n,2) en todos los casos |
| (ii) | W_w ⊆ 𝒢_1 | solo para 1/m |
| (ii'') | Datos aleatorios en coma flotante | E_sp = ½J_{−A} hasta 8.9e−16; para w = 1, A ≥ 0 y ω aleatorio, residuo relativo de mínimos cuadrados ∈ [0.15, 0.24] |
| (ii''') | Anulador ν con n = 4 (exacto, 200 casos) | correcto |
| (iii) | Forma cuadrática del resorte con reposo | −8rs exacto; σ_* = 2rs (numérico) |

CPU: 22 s.

## Compilación

Se copió `manuscript/` en el scratchpad, se pegaron los bloques P, A, B, C y D en sus lugares, se sustituyó la frase de la Prop. 3.3 y se compiló con `latexmk -pdf`.

- Resultado: 0 errores, 0 referencias o citas indefinidas, 0 cajas desbordadas, `pdftotext | grep -c "??"` = 0.
- El PDF pasa de 12 a 16 páginas. Para recortar, se pueden mover al apéndice las demostraciones de `prop:weightsdd` y `cor:rest`(c).

## Qué queda abierto

1. k = 2 con pesos fijos, cuando h(a)+h(n−a) es constante y w no es ∝ 1/m (n ≥ 5).
2. Pesos dependientes de los datos para w decrecientes distintos de 1/m.
3. Un κ PD independiente de los datos con los mismos *minimizadores* para el resorte con reposo.
4. Problema 4.2 (con "único"): buscar o certificar un contraejemplo con el método LP/Farkas descrito.
5. Cotejar con el texto de Roth et al. (2003) que su desplazamiento mínimo coincide con σ_*. Comprobar también que el recíproco (Prop. invcomplete) no está ya publicado.
