# Informe de árbitro interno independiente — LMI001, ronda 3 (v0.4, commit a9c615c)

Árbitro interno independiente (no ha participado en rondas previas ni en la integración). Fecha: 03/10/2026. Objeto: teoremas nuevos de v0.4 (Prop. 3.2, Cor. 3.3, Cor. 3.6, Rem. 3.7, Prop. 4.2, Prop. 4.3, Problema 4.4, Rem. 4.5, Apéndice B), cambio de alcance, respuesta a la ronda 2, lectura fresca.

**Veredicto: cambios menores.** Los siete resultados nuevos (Prop. 3.2, Cor. 3.3, Cor. 3.6, Rem. 3.7, Prop. 4.2, Prop. 4.3, Rem. 4.5) son correctos paso a paso y pasan mis chequeos exactos independientes; lo que falta es de texto y de extensión: 0 bloqueantes, 3 mayores (mayores por su peso en la lectura, no por su coste: M1 la Prop. 4.3 sí acota la distancia para A densa y el texto dice lo contrario; M2 la tensión reconstruida cae fuera del alcance acotado y no se dice; M3 17 páginas), 12 menores.

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

### Etiquetas de estado de lo nuevo
Las etiquetas "not yet refereed" están en la Tabla 2 (filas l. 325, 332, 338, 339 y pie l. 343), en *Limitations* (l. 347) y en el resumen (l. 62), pero **en los enunciados** sólo el Remark 4.5 (l. 281) lleva "proved here; not yet checked by an independent referee"; Prop. 3.2 (l. 116), Cor. 3.3 (l. 122), Cor. 3.6 (l. 181), Remark 3.7(a) (l. 188), Prop. 4.2 (l. 263) y Prop. 4.3 (l. 269) dicen sólo "proved here" (m1). La atribución a Roth et al. es prudente ("as we recall it (not checked against their text)", "not found in the literature we know (not searched exhaustively)"); falta fijar la convención del factor (m6).

## 1. Verificación de la ronda anterior (ronda 2 → v0.3, comprobada en v0.4)

Líneas de `manuscript/main.tex` v0.4 salvo indicación. Nada de lo aplicado en v0.3 se perdió al integrar v0.4, salvo la extensión.

| Hallazgo r2 | Estado | Evidencia |
|---|---|---|
| M1 (Hofmann–Buhmann, Roth et al., Dhillon et al.) | aplicado bien | l. 67, 113 ("elementary and not new"), 150 (*Status* (b) [literature]), 294 (recocido cita hofmann1997), 326 (Tabla 2) |
| M2 (Sejdinovic et al., França et al.) | aplicado bien | l. 85, 150 (*Status* (f)), 214 (*Status* de 3.9), 312, 330, 334–335 |
| M3 (alcance del Teorema 4.1) | aplicado bien | l. 69, 250 (media por resorte con peso C(n_c,2)⁻¹; 12/12 fuera del enunciado), 252 (*Values, not minimisers*), 337 |
| m1 (comprobación por (3)) | aplicado bien | l. 212 (ΔE = −0,5; recalculado: con K′ = 2⟨x,y⟩ el corchete es −1, ½·corchete = −0,5) |
| m2 (K = σI ∓ A) | aplicado bien | l. 150 |
| m3 (TR-04-25, 2005) | aplicado bien | `refs.bib`:46–54 |
| m4 ((d−r)² no de tipo negativo) | aplicado bien y ampliado en v0.4 | l. 166, 170–171, Cor. 3.6 |
| m5 (PD/lift) | aplicado bien | l. 146, 192 |
| m6 (fuentes figura) | aplicado con matiz (figura fuera del manuscrito) | l. 294 remite a `figures/energies.pdf` |
| m7 (CONTINUIDAD) | aplicado bien | `CONTINUIDAD`:3 (añade además la tabla de renumeración v0.4) |
| m8 (FICHA) | aplicado bien | `FICHA`:3 |
| m9 (C3a) | aplicado bien | l. 294 |
| m10 (blurring mean shift) | aplicado bien | l. 274, 284 |
| m11 (resumen (vi)) | aplicado bien | l. 62 |
| m12 (control emparejado) | aplicado bien | l. 62, 67 |
| m13 (Teorema 4.1: residuo, Cauchy–Binet) | aplicado bien | l. 234, 250 |
| m14 (`--fast`) | aplicado bien | README, bloque "Reproducir" |
| m15 (frase de E1) | aplicado bien | l. 290 |
| r1-M2, r1-M5, r1-M7, r1-m5, r1-m12 (residuos de la ronda 1) | aplicados bien | l. 212; 69/250; 222 y 347; 192; figura fuera |
| r1-M8 / Extensión (13 → 12 págs. en v0.3) | **revertido en v0.4** | 17 págs. (texto principal hasta la p. 14); ver M3 |

Recuento: 23 bien aplicados (uno con matiz aceptable), 0 a medias, 0 no aplicados; 1 revertido por la integración de v0.4 (extensión).

## 2. Hallazgos nuevos

Bloqueantes: ninguno. Ninguna demostración nueva falla.

### Mayores

**M1. Prop. 4.3: el comentario "bounds no distance" es inexacto; el propio certificado da una cota uniforme cuando todas las A_ij > 0.** Ubicación: l. 272 ("It excludes exact representation for every ω, but bounds no distance: in small numerical examples the distance from E_tot to 𝒢_ω becomes small as ω degenerates"); README, sección "Teoría integrada…" ("siempre > 0, pero pequeño cuando ω degenera"); `CONTINUIDAD`:166 ("no da una cota uniforme de la distancia").
*Problema y evidencia.* Para todo g ∈ 𝒢_ω + ℝ, ⟨ν, E_tot − g⟩ = ⟨ν, E_tot⟩, y por Hölder max_C |E_tot(C) − g(C)| ≥ ⟨ν,E_tot⟩/‖ν‖₁. Aquí ‖ν‖₁ = Σ_t ω̂_t(Ω̂−ω̂_t) + Σ_{2+2}ω̂(X)ω̂(Y) = 2ê₂ + 2ê₂ = 4ê₂ (ê₂ = Σ_{t<u}ω̂_tω̂_u) y ⟨ν,E_tot⟩ = 2Σ_{t<u}Â_tuω̂_vω̂_z ≥ 2(min_{t<u}Â_tu)ê₂. Luego, **para todo ω ∈ (0,∞)ⁿ, todo K simétrico y todo c ∈ ℝ, max_C |E_tot(C) − J^ω_K(C) − c| ≥ ½ min_{t<u} Â_tu ≥ ½ min_{i≠j} A_ij** (y, en ℓ², ≥ (2/√7)·min A, porque |ν(C)| ≤ ê₂ en cada una de las 7 particiones). Para matrices de resortes de puntos distintos con φ > 0 en (0,∞) (el caso que el enunciado pone de ejemplo) la cota es positiva y no depende de ω: los ω degenerados **no** acercan E_tot a 𝒢_ω por debajo de ella. Numéricamente (LP de distancia uniforme en el ω casi óptimo): 0,1035 ≥ 0,1034 (n = 4, k = 2, φ = d; la cota es casi alcanzada), 0,027 ≥ 0,021, 1,08 ≥ 0,26, 3,38 ≥ 0,08, etc. (8/8 casos). Para A con ceros la cota se anula y la distancia sí puede tender a 0: con un solo par no nulo y n = 4, k = 2 el aniquilador es único y la distancia es 2A_ab ω₃ω₄/‖ν‖₂ → 0 si ω₃, ω₄ → 0; mi búsqueda da 10⁻⁶–10⁻⁹ para n = 4,…,6. Además, con log ω ∈ [−40,40] mi propio cálculo ℓ² "encontró" distancia 0 para A densa: es un artefacto de mal condicionamiento (contradice la cota rigurosa), y los "residuos pequeños con log ω de ±10 a ±30" del integrador pueden serlo en parte.
*Corrección.* Sustituir en l. 272 la frase por: "The certificate also bounds the distance when all off-diagonal $A_{ij}$ are positive: since $\lVert\nu\rVert_1=4\sum_{t<u}\hat\omega_t\hat\omega_u$, for every $\omega\in(0,\infty)^n$, every symmetric $K$ and every $c\in\R$ some $k$-partition has $|E_\tot(C)-J^\omega_K(C)-c|\ge\tfrac12\min_{i\ne j}A_{ij}$. When $A$ has zero entries the bound can vanish, and the distance can tend to $0$ as $\omega$ degenerates (e.g.\ a single non-zero spring, $n=4$, $k=2$)." Opcionalmente, añadirlo al enunciado como parte (b) [proved here]. Corregir README y CONTINUIDAD en el mismo sentido (retirar "pequeño cuando ω degenera" para A densa).

**M2. El cambio de alcance es correcto pero incompleto: la "tensión" de la línea cae en la parte no explicada, y la Sección 4 sigue presentando {1, 1/n_c} como "dentro de la familia".** El acotamiento a la normalización por partícula es correcto y necesario (la Prop. 4.3 lo justifica; título, resumen, Introducción, lectura de E1–E3, *Next step* (f), README y ficha son coherentes entre sí). Quedan tres incoherencias:
(a) La ficha de la línea habla de objetivos construidos con "springs, tension and lifting" (l. 62). En la reconstrucción, la tensión es la tensión liberada T(C) sin normalizar (l. 82), y por el Teorema 3.4(d) maximizar T **es** minimizar E_tot: las formulaciones de tensión quedan, por construcción, fuera de la explicación. Ni el resumen, ni la lectura de E1–E3 (l. 312), ni *Next step* (a)/(f) lo dicen. Corrección (tras la última frase de l. 312): "In particular, tension formulations as reconstructed here (maximising the released tension $T$) are the total normalisation in disguise (Theorem~\ref{thm:main}(d)) and are not covered by this explanation; a per-particle tension $\sum_c T_c/n_c$ with $T_c$ the springs cut by cluster $c$ is ratio cut, a kernel $k$-means objective~\citep{dhillon2007}." (y en *Next step* (a): "…and with which normalisation of the energy and of the tension").
(b) l. 226: "Theorem 3.4 covers every objective that is a sum over within-cluster pairs … weighted by a function of the cluster size in {1,1/n_c}. An ingredient can escape only by breaking one of these three features" sugiere que todo lo que está dentro de la familia es kernel. Corrección: "Theorem 3.4(b) makes every per-particle pairwise objective a kernel $k$-means objective; the total normalisation is already outside weighted kernel $k$-means (Proposition~\ref{prop:weightsdd}). Within the per-particle family an ingredient can escape only by breaking …".
(c) *Limitations* (l. 347): "if the original screening used many-body terms, assignment-dependent parameters or a dynamics on positions, Section 4 applies" → añadir "or the total normalisation (including the released tension)".

**M3. Extensión: 17 páginas (texto principal hasta la p. 14), frente a 12 en v0.3 y al objetivo de 5–10.** Compilado en copia: 17 págs., p. 15–17 bibliografía. Mover demostraciones al Apéndice B no reduce el total. Lo nuevo (Prop. 3.2–Cor. 3.6, Rem. 3.7, Prop. 4.2–4.3, Problema 4.4/Rem. 4.5, Apéndice B, filas nuevas de la Tabla 2) explica casi todo el crecimiento de 12 a 17 páginas y es el único contenido matemático genuinamente nuevo del trabajo. Propuesta, por orden:
1. **Nota aparte** (recomendado): "Invariances of the kernel $k$-means trace form, and size weights" con Prop. 3.2, Cor. 3.3, Cor. 3.6, Rem. 3.7, Prop. 4.2, Prop. 4.3 (con la cota de M1) y el Apéndice B. Es un objeto autocontenido, más fácil de arbitrar y de datar (prioridad frente a Roth et al. y a la literatura de *shift of pairwise similarities*). En LMI001 dejar sólo los enunciados que sostienen la lectura de la línea —Prop. 3.2 (una línea de prueba: "exchange two points"), Cor. 3.6(b) con el cálculo de cuatro puntos, y Prop. 4.3 con su certificado (12 líneas)— y citar la nota para lo demás. Ahorro estimado: ≈ 3 págs.
2. Tabla 1 (E3 por potencial) a `results/tables_relaxation.md` (ya está allí por configuración): ≈ ⅓ pág.
3. E3 condensado (l. 294, 26 líneas): dejar criterios, la *Disclosure* en dos frases, C3a y C3b con sus números, y remitir el resto (alcanzar E*, C3c, recocido) a `results/tables_relaxation.md`: ≈ ⅓ pág.
4. Teorema 3.4(f): la parte del mapa Φ̃ = Φ/√2 y "half the Hooke energy" (l. 142–146 y la mitad final de su prueba) es literatura; reducir a una frase: ≈ ¼ pág.
5. Resumen de ≈ 330 palabras a ≈ 200 (m5); Remark 3.8 y Prop. 3.9(iii) condensados: ≈ ¼ pág.
Con 2–5 sin la nota aparte se llega a ≈ 15–16 págs.; con 1–5, a ≈ 13. Llegar a 10 exige además quitar la Tabla 2 o mover la bibliografía a una columna más densa; no lo recomiendo.

### Menores

- **m1.** Etiquetas en los enunciados (l. 116, 122, 181, 188, 263, 269): uniformarlas. Tras esta ronda, propongo "[proved here; checked by one internal referee (round 3)]" para Prop. 3.2, Cor. 3.3, Cor. 3.6, Rem. 3.7(a), Prop. 4.2, Prop. 4.3 y Rem. 4.5, y actualizar el pie de la Tabla 2 (l. 343), *Limitations* (l. 347), el resumen (l. 62), README y ficha. El pie dice "checked by exact ranks for small n", que no aplica a Cor. 3.6, Rem. 3.7 ni Rem. 4.5.
- **m2.** l. 67: "the summed energy is min-sum clustering, which is not a weighted kernel $k$-means objective" → añadir "for non-negative springs". FICHA (ES y EN): "el resorte con longitud de reposo no tiene ningún núcleo PD independiente de los datos" / "has no dataset-independent PD kernel" es más fuerte de lo probado (el Remark 3.7(c) deja abierto un núcleo con los mismos minimizadores): escribir "ningún núcleo PD independiente de los datos que reproduzca sus valores salvo constante (y factor positivo)". La FICHA tampoco dice "3 ≤ k ≤ n−2" al afirmar que 1/n_c es el único peso.
- **m3.** Remark 3.7(a) (l. 188): "for every PD (a fortiori every symmetric) K" usa "PD" para una matriz contra la convención de l. 75 y el "a fortiori" se lee al revés; escribir "for every positive definite matrix $K$ (in particular, if it holds for every symmetric $K$)" y recordar n ≥ 3, 2 ≤ k ≤ n−1.
- **m4.** Resumen (l. 62): "All of this concerns objective values, not minimisers" abarca también el mecanismo de congelamiento de Lloyd, que es algorítmico; restringir a "The certificates and the size-weight results concern objective values, not minimisers".
- **m5.** Resumen demasiado largo (≈ 330 palabras); ver M3.5.
- **m6.** Cor. 3.3 (l. 122): fijar la convención: con disimilitudes A_ij (diagonal 0) el desplazamiento mínimo de Roth et al. es d₀* = σ*; con D(K) es 2σ*. Texto: "for $\sigma_*\ge0$ it equals the minimal off-diagonal shift of the dissimilarities $A_{ij}$ in \citet{roth2003} (twice that for $D(K)$), as we recall their construction (not checked against their text)".
- **m7.** Prop. 4.2: la cota k ≤ n−2 no es necesaria (con k = n−1 sólo entra w(2), (iii) es vacuo y (i) vale; rango completo = número de particiones en mi chequeo). Basta una frase o ampliar a 3 ≤ k ≤ n−1. En cambio, en la Prop. 4.3 k ≤ n−2 sí es necesaria (con k = n−1, E_tot(C) = A_pq es J^ω_K con D(K)_pq = A_pq(ω_p+ω_q)/(ω_pω_q)); conviene decirlo en una frase.
- **m8.** l. 272: "(fixed weights are excluded by Proposition 4.2)" vale sólo para 3 ≤ k ≤ n−2 (y n = 4, k = 2); añadir el rango.
- **m9.** Apéndice A (l. 353): "an independent re-check, not part of the repository" se refiere al chequeo del integrador, que no es independiente de la integración ni reproducible desde la carpeta. Escribir "the integrator's own re-check (separate code, not in the repository)" y citar este informe como la verificación independiente.
- **m10.** `experiments/identity_check.py`:405 y `results/tables_identity.md`:40 conservan "Theorem-3.2(f)". Cambiar la cadena en el código y corregir la cabecera del `.md` (cambio de una etiqueta, sin repetir la corrida, documentado en README), en lugar de una advertencia permanente.
- **m11.** `franca2021`: existe preprint arXiv:1710.09859 (confirmado por WebSearch); añadirlo en `note` y, si el proxy lo permite, cotejar allí si enuncian la inclusión de la Prop. 3.9(ii) (pendiente desde la ronda 2).
- **m12.** Para el *Next step* (e) (¿es conocida la Prop. 3.2?), revisar además la literatura sobre desplazamientos de similitudes en *pairwise clustering* (aparece, p. ej., "Shift of pairwise similarities for data clustering", Chehreghani; no verifiqué sus datos ni su contenido).

## 3. Bibliografía

v0.4 no añade entradas (`refs.bib` sin cambios entre 0631bda y a9c615c). Re-verifiqué con WebSearch las nuevas de la ronda 2; arXiv y Crossref no se consultaron directamente.

| Entrada | Estado | Corrección |
|---|---|---|
| roth2003 | correcta (IEEE TPAMI 25:1540–1551, 2003; Roth, Laub, Kawanabe, Buhmann) | ninguna; ver m6 para la convención del desplazamiento |
| franca2021 | correcta (IEEE TPAMI 43(12):4411–4425, 2021; doi 10.1109/TPAMI.2020.2998120) | añadir arXiv:1710.09859 (m11) |
| hofmann1997 | correcta (IEEE TPAMI 19(1):1–14, 1997) | ninguna |
| sejdinovic2013, dhillon2005tr | no re-verificadas en esta ronda (verificadas en la ronda 2 por árbitro y autor) | ninguna |

## 4. Verificación computacional (propia, independiente; scratchpad `referee3_LMI001/`)

| Script | Qué comprueba | CPU | Resultado |
|---|---|---|---|
| `r3_common.py` + `r3_dims.py` | dim V_{n,k} exacta (ℚ) n = 3..7, todo k; rangos de {F^w_{E_ab}} ∪ {1} para 5 pesos, dim 𝒢_ω (ω = 1 y aleatorio), n = 4..7 | 4,9 s | dim V = n+1 en 15/15; núcleo = span{I, g1ᵀ+1gᵀ}; rango C(n,2) sólo para w = 1/m (k ≤ n−2); dim 𝒢_ω = C(n,2) |
| `r3_prop43_exact.py` | aniquilador ν exacto, 60 casos con grupos no unitarios (n = 4..8) + 60 con pesos de tamaño | 2,0 s | 0 fallos |
| `r3_prop43_num.py` | min sobre ω de la distancia relativa de E_tot a 𝒢_ω (n ≤ 6, 4 tipos de A) | ≈ 100 s | A densa: 0,08–0,90; un solo par: 10⁻⁶–10⁻⁹ |
| `r3_prop43_bound.py` | cota de M1 con LP de distancia uniforme (log ω ∈ [−40,40]) | ≈ 29 s (+100 s por re-ejecutar por error el script anterior al importarlo) | 8/8 por encima de ½ min A; ℓ² numérica = 0 en n = 4 identificada como artefacto |
| `r3_cor36.py` | 8rs exacto (9 pares (r,s)); σ*(−A[X_s]) | < 0,1 s | 8rs exacto; σ* = 2rs para s ≥ r |
| compilación `latexmk` en copia | | 2,5 s | 17 págs., 0 errores, 0 referencias/citas indefinidas, 0 "??", sin avisos de cajas |

Total ≈ 4,5 min de CPU (presupuesto 5). Reproducción de E1–E4: no procede; v0.4 no regeneró resultados (`results/` y `numbers.tex` idénticos entre v0.3 y v0.4 según `git diff --stat`). Muestreé 9 macros de `numbers.tex` (E1 checks 19285, max_rel_err 1,1×10⁻¹¹, 6090 particiones, E2 90/90, E3 600, 28/30, 6/30, 34 %) contra los JSON: coinciden.

## 5. Lista final de acciones (por prioridad)

1. Reescribir el comentario de la Prop. 4.3 (l. 272) con la cota uniforme ½ min_{i≠j} A_ij y el caso de A con ceros; corregir README y CONTINUIDAD (M1).
2. Decir explícitamente que la tensión reconstruida (T sin normalizar) es la normalización total y queda fuera de la explicación; corregir l. 226 y *Limitations*; ampliar *Next step* (a) (M2).
3. Decidir la extensión: preferentemente sacar la teoría de invariancias y pesos a una nota aparte; en todo caso aplicar los recortes 2–5 de M3.
4. Uniformar las etiquetas de estado de los enunciados nuevos y actualizarlas tras esta ronda (m1).
5. Calificar l. 67 y la FICHA (m2); corregir Remark 3.7(a) (m3), resumen (m4, m5), convención de Cor. 3.3 (m6), rangos de k (m7, m8), Apéndice A (m9).
6. Corregir la cadena "Theorem-3.2(f)" en código y tabla (m10); añadir arXiv a `franca2021` y cotejar Prop. 3.9(ii) (m11); ampliar la búsqueda de prioridad de la Prop. 3.2 (m12).
7. Mantener abierta la confirmación del autor de la línea (familia de pares, control emparejado y **normalización**, incluida la de la tensión).
