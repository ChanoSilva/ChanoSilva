[EN CURSO]

# Informe de árbitro interno independiente — LMI001, ronda 3 (v0.4, commit a9c615c)

Fecha: 03/10/2026. Objeto: teoremas nuevos de v0.4 (Prop. 3.2, Cor. 3.3, Cor. 3.6, Rem. 3.7, Prop. 4.2, Prop. 4.3, Problema 4.4, Rem. 4.5, Apéndice B), cambio de alcance, respuesta a la ronda 2, lectura fresca.

(Informe en redacción; secciones se completan a medida que avanza la verificación.)

## 0. Verificación de los resultados nuevos de v0.4 (prioridad máxima)

Leí cada enunciado y cada paso de prueba (cuerpo, `main.tex` l. 115–126, 174–189, 254–282; Apéndice B, l. 356–376) y escribí chequeos propios desde cero (Fractions/numpy; ninguna función del autor ni de `theory/`), en `scratchpad/referee3_LMI001/r3_*.py`.

### Prop. 3.2 (prop:invcomplete) — correcta
- Reducción a diagonal cero (`e = Δ − f1ᵀ − 1fᵀ`, `J_e = −2𝓔`): correcta; además comprobé `J_K(C) = Σ_c n_c⁻¹ Σ_{i<j∈C_c} D(K)_ij` (l. 119).
- k ≥ 3: `|R| = n−3 ≥ k−2` usa k ≤ n−1; la diferencia ½(e_pi − e_pj) es correcta.
- k = 2: la diferencia `(|P|+1)⁻¹Σ_Pγ − (|Q|+1)⁻¹Σ_Qγ` es correcta; P = ∅ da Σγ = 0 y P = {p} da γ_p(½ + 1/(n−2)) = 0 (con n = 3, Q = ∅ y el término es 0: sigue valiendo).
- Encadenamiento e_ab = e_ad = e_cd, `e = σI − σ11ᵀ`, `g = f − σ/2·1`: correcto. Unicidad de (σ, g) con n ≥ 3: correcta.
- "Cualquier número de clusters": correcto si la familia incluye k = 1 o k = n (o n ≥ 4); con k ∈ {1,…,n} como está escrito, α = 0 sale de k = n.
- Formas equivalentes: ker D = ker(M ↦ PMP) = {g1ᵀ+1gᵀ} (dimensión n en ambos casos: dim Sym_n − dim Sym(1⊥) = n), D(σI) = 2σ(11ᵀ − I), P(σI)P = σP. Correcto.
- **Chequeo exacto independiente:** núcleo de Δ ↦ (J_Δ(C) − J_Δ(C₀))_C sobre ℚ para **todo** n = 3,…,7 y **todo** 2 ≤ k ≤ n−1 (15 casos; hasta 350 particiones × 28 incógnitas): dimensión n+1 en los 15 casos, y rank[base explícita de V; base del núcleo] = n+1 (el núcleo es exactamente {σI + g1ᵀ + 1gᵀ}). 1,5 s de CPU.

### Cor. 3.3 (cor:reps) — correcto
`P(K+σI)P = K + σI + g1ᵀ + 1gᵀ` con `g = −(K1+σ1)/n + (1ᵀK1+σn)/(2n²)·1`: comprobado a mano. La identificación con el desplazamiento mínimo de Roth et al. depende de la convención: si las disimilitudes son A (resortes, diagonal 0), su d₀* = −2λ_min(−½PAP) = σ*; si son D(K) (como en la Prop. 3.2), d₀* = 2σ*. El texto dice "the threshold is … the minimal constant shift"; conviene fijar la convención (m6).

### Cor. 3.6 (cor:rest) — correcto
- (a) restricción a submatrices principales + unicidad de la Prop. 3.2 + comparación vía X ∪ X′: correcto (usa |X| ≥ 3, garantizado).
- (b) Σ c_i c_j φ(d_ij) = 4φ(0) + 2[φ(3s) − φ(s) − 2φ(2s)] = 8rs: **verificado en aritmética exacta** para 9 pares (r, s); `−8rs + 4σ` correcto (los términos en g se anulan por Σc = 0, el término σ da σ‖c‖² = 4σ). σ*(−A[X_s]) ≥ 2rs con c/2: correcto; numéricamente σ* = 2rs exacto para s ≥ r (s = 1, 5, 50 con r = 1) y σ* = 0,58 > 2rs = 0,2 para s = 0,1.
- (c) (λ_X − λ_Y)A[X] ∈ V; A[X_s] ∉ V_{4,2} porque (s−r)² = (2s−r)² exige s = 2r/3 y (2s−r)² = (3s−r)² exige s = 2r/5: correcto. El paso "el mismo argumento da un σ para todos los X_s" es correcto porque X_s ∪ X_{s′} contiene a ambos y λ es común.

### Remark 3.7 (rem:argmin) — correcto, con un detalle de notación
(a) correcto (`J_{λI−Δ} = λ(n−k) − J_Δ`, argmax propio porque Δ ∉ V). (b) correcto: la matriz de bloques B de C* tiene J_B(C*) = 0 y J_B(C) > 0 si C ≠ C* (comprobado a mano). (c) `J_K({i},{j,l}) = ½D(K)_jl` correcto. Detalle: "for every PD … K" aplica "PD" a una matriz, contra la convención fijada en l. 75 (PSD para matrices) (m3).

### Prop. 4.2 (prop:weights) — correcta
- dim 𝒢_ω ≤ C(n,2) y constantes en 𝒢_ω (K = diag(1/ω) da n − k): correcto.
- (iii)⇒(i), (i)⇒(ii), (ii)⇒(i) (polarización M(e_a+e_b) − M(e_a) − M(e_b) = −2(E_ab+E_ba) y argumento polinomial): correctos.
- (i)⇒(iii): dependencia lineal de C(n,2)+1 funciones en un espacio de dimensión ≤ C(n,2) ⇒ e ≠ 0 con F^w_e constante; intercambio ponderado w(2)(e_pi − e_pj) = 0; tamaños (m+1,1,ρ) vs (m,2,ρ) con 1 ≤ m ≤ n−k: correctos. Caso k = 2: w(n−1)Σγ = 0 y (w(2)+w(n−2))γ_x = 0, correcto; n = 4 da 3w(3) = 2w(2).
- **Chequeo exacto independiente** (n = 4,…,7, todos los k): rango de {F^w_{E_ab}} ∪ {1} = C(n,2) para w = 1/m y C(n,2)+1 para w ∈ {1, 1/m², C(m,2)⁻¹, aleatorio} en todos los casos con k ≤ n−2; dim 𝒢_ω = C(n,2) exactamente (ω = 1 y ω aleatorio racional). Para k = n−1 todo tiene rango C(n,2) (= número de particiones): (i) vale para cualquier w, y (iii) es vacuo, así que la equivalencia también vale con k = n−1; la cota k ≤ n−2 es innecesaria pero no errónea (m7).

### Prop. 4.3 (prop:weightsdd) — correcta; la frase sobre distancias es inexacta y el resultado admite una cota cuantitativa (ver M1)
- Σν = 0: correcto (cada par t<u lo separan exactamente dos de los tres cortes 2+2).
- ν aniquila 𝒢_ω: t = u da (1 − 2 + 1)(Ω̂ − ω̂_t) = 0; t ≠ u da 0. Correcto.
- ⟨ν, E_tot⟩ = 2Σ_{t<u} Â_tu ω̂_v ω̂_z ≥ 2A_ab ω̂₃ω̂₄ > 0 para **todo** ω ∈ (0,∞)ⁿ y todo A ≥ 0 no nulo fuera de la diagonal: correcto (el coeficiente de Â_tu es −ω̂(tu)ω̂(vz) + ω̂_z(Ω̂−ω̂_z) + ω̂_v(Ω̂−ω̂_v) = 2ω̂_vω̂_z).
- Versión con pesos de tamaño (grupos unitarios; posible exactamente si k ≥ 3 o n = 4): coeficiente (w(3)−w(2))ω̂(tu)ω̂(vz) + 2w(3)ω̂_vω̂_z, correcto.
- k ≤ n−2 es necesario: con k = n−1, E_tot(C) = A_pq es J^ω_K con D(K)_pq = A_pq(ω_p+ω_q)/(ω_pω_q).
- **Chequeo exacto independiente:** 60 casos aleatorios (n = 4,…,8; 2 ≤ k ≤ n−2; A ≥ 0 racional con muchos ceros; ω racional aleatorio; agrupaciones no unitarias aleatorias): Σν = 0, ν ⊥ J^ω_{E_ij+E_ji} para **todas** las entradas (i ≤ j), ⟨ν, E_tot⟩ igual a la fórmula y > 0: 0 fallos. 60 casos de la versión con pesos de tamaño (w(3) ≥ w(2), w(3) > 0): 0 fallos.
- **Casos degenerados de ω.** El enunciado exige ω ∈ (0,∞)ⁿ y es cierto tal cual; el certificado prueba no pertenencia exacta para cada ω. Búsqueda de contraejemplos (L-BFGS sobre log ω ∈ [−15,15]ⁿ, 6–12 arranques; n ≤ 6): para A **densas** (Hooke, cuerda φ = d, uniforme) la distancia relativa mínima encontrada es 0,08–0,90, nunca cercana a 0; para A con **un solo par** no nulo baja a 10⁻⁶–10⁻⁹ (y para n = 4, k = 2 esto es exacto: el aniquilador es único y la distancia es 2A_ab ω₃ω₄/‖ν‖ → 0 si ω₃, ω₄ → 0). Con cotas [−40,40] la distancia ℓ² "numérica" llegó a 0 para A densa con n = 4, pero es un artefacto de mal condicionamiento: contradice la cota rigurosa de M1, y el LP de distancia uniforme en el mismo ω da 0,027 ≥ minA/2 = 0,021 y 0,1035 ≥ 0,1034 (cota prácticamente alcanzada). El README (sección "Teoría integrada…", "pequeño cuando ω degenera") puede estar recogiendo ese artefacto.

### Problema 4.4 y Remark 4.5 — correctos
La reformulación con "unique minimiser" resuelve la trivialidad de v0.3 (a ≡ 0). En el Remark 4.5 comprobé a mano que a = −1 dentro de los bloques de P hace de P el **único** minimizador para w = 1 (cuenta de pares co-agrupados; igualdad sólo si C engrosa P, y con k bloques C = P) y para w = 1/n_c (Σ_b m_cb(m_cb−1)/(2n_c) ≤ (n_c−1)/2 con igualdad sólo si C_c ⊆ un bloque). El esquema Farkas es correcto para w fijo.
