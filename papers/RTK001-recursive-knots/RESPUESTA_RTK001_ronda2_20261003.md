# Respuesta del autor a la ronda 2 de revisión interna — RTK001 (03/10/2026)

Informe atendido: `REFEREE_RTK001_ronda2_20261003.md` (cambios menores; 0 bloqueantes, 4 mayores, 13 menores; ronda 1: 23 bien, 2 con error nuevo: B2, M2).
Además, en esta pasada se integra el trabajo de `theory/` sobre el caso "misma hebra" (`theory/same_strand_lemma.tex`, `same_strand_derivation.md`, `check_same_strand.py` y su salida), terminado por el agente teórico durante la ronda 2.

Documento escrito de forma incremental (estado de trabajo al final de cada sección).

## 0. Plan y estado de trabajo

- [ ] Verificación propia del bloque "misma hebra" de `theory/` (lectura de la prueba + corrida de `check_same_strand.py` + cómputo independiente de la clasificación de pares doblemente críticos).
- [ ] M4: congelar los resúmenes de `theory/` en `results/` (con SHA-256) y que `make_numbers.py` lea solo la copia.
- [ ] B2/m3: tolerancia única en `make_numbers.py`.
- [ ] M1: etiquetas de estado (resumen, Lema 3.7, Teorema 3.10, Hip. 3.12, tabla, Limitaciones, README, CONTINUIDAD, FICHA).
- [ ] Integración del bloque misma hebra tras la Prop. 3.9 con estados correctos.
- [ ] M2: Conjetura 3.16 con umbral f_*(d) y márgenes 1.4 % / 2.1 % por macro.
- [ ] M3: lo abierto.
- [ ] Menores m1–m13, bibliografía, recortes.
- [ ] Compilación, páginas, CONTINUIDAD, README, FICHA.

## 1. Verificación propia del bloque "misma hebra" de `theory/` (hecha antes de pegarlo)

**Lectura de la prueba** (`theory/same_strand_lemma.tex`, `same_strand_derivation.md`), paso a paso:
- *Lema lem:turn* (exclusión por giro): correcto. Si a + b < π a lo largo del arco, cos a + cos b = 2 cos((a+b)/2) cos((a−b)/2) > 0 (ambos factores positivos porque |a − b| ≤ a + b < π), luego (X₂ − X₁)·(T₁ + T₂) = ∫ T_γ·(T₁+T₂) > 0, incompatible con un par doblemente crítico; la versión con giro total < π sigue de a(σ) ≤ ∫₀^σ|T'| y b(σ) ≤ ∫_σ^ℓ|T'|.
- *Ángulo de cono χ*: K_d' = v(1 − x)T + rmW con x = rκ_⊥ ∈ [−f, f]; tan χ = rm/(v(1−x)); χ_lo, χ_hi correctos (1/ζ_min = rm/((1−f)v_min)).
- *Ruta R2* (sin (H₃)): rehecha la derivada Y_i' = (vκ_⊥cos χ_i − m sin χ_i)U + vκ_W cos χ_i W − vκ_W sin χ_i T (con U' = mW − vκ_⊥T, W' = −mU − vκ_W T, T' = v(κ_⊥U + κ_W W), (T,U,W) directo) y |Y_i'|² ≤ (vκ + m sin χ_i)² (desarrollando: κ_⊥²cos²χ_i + κ_W² ≤ κ² y −κ_⊥cos χ_i ≤ κ). Desigualdad triangular de ángulos: a(t) ≤ |χ(t) − χ₁| + ∫(vκ + m sin χ₁), análogo para b; suma ≤ 2Δχ + δ + u sin χ_hi con ∫vκ ≤ σ/τ = δ y u = m|s| ≤ δ/Θ_min. Correcto.
- *Ruta R1* (bajo (H₃)): ω = |K_d'×K_d''|/|K_d'|² = κ_d|K_d'|; la división de Minkowski de la Prop. 3.8 multiplicada por |K_d'| = √(A+B) da ω ≤ vκ(A+2B)/(A+B) + rm²/√(A+B) + rm|a₀|/(A+B), y B/(A+B) = sin²χ, rm/√(A+B) = sin χ. Correcto; en d = 1 (círculo) a₀ ≡ 0 y no hace falta ninguna hipótesis.
- *Distancia*: el Paso 3 del Lema 3.7 (A ≥ Λ, |X₂ − X₁| ≥ ℓ₀ − 2r) no usa el índice de hebra; Λ ≥ r en [π/3, π) para f ≤ 1/2 (en [π/3, π/2] Λ = 2(τ−r) sin(δ/2) ≥ τ − r ≥ r; en [π/2, π) es el Paso 4 en f = 1/2 y Λ/r decrece en f). Correcto.
- *Corolario cor:samefamily*: d = 1: τΩ̄ = 1 + 9/13 + 9/(2√13) = 2.94038 < 3, δ_R1 = 1.06843 > π/3 = 1.04720; d ≥ 2: v_min(K₁) ≥ 2√((1−f)² + 9f²/4), thick(K₁) ≤ f (Prop. 3.5), el cociente v_min/thick al menos se duplica por nivel (v_min(K_j) ≥ 2(1−f_j)v_min(K_{j−1}), thick(K_j) ≤ f_j thick(K_{j−1})), m ≤ 2, luego Θ_min ≥ √13·2^{d−3} ≥ 1.8028 y ζ_min ≥ Θ_min; δ_R2^ap(1.8028) = 1.67737 > π/3. Correcto. El umbral de Θ_min para δ_R2^ap ≥ π/3 en f = 1/2 es 1.1121 (bisección propia), así que la cota a priori antigua Θ_min ≥ 2^{d−2} = 1 no bastaría en d = 2: la cota nueva del Corolario es necesaria.
- *Corrección de redondeo* (encontrada en esta verificación): el texto de `theory/` dice "c₀′ ≥ sin(δ_R1/2) = 0.5092"; el valor exacto es 0.509170…, así que como cota inferior debe escribirse "> 0.509" (corregido al integrar; las macros de cotas inferiores se redondean ahora hacia abajo, `floor_fmt` en `make_numbers.py`). En [π/2, π) el argumento φ_c se hace con c = 2 sin(δ_R1/2) exacto: φ_c(1/√2) = 1 − c/√2 = 0.2799, φ_c(1) = 3 − c − π/2 = 0.4109, φ_c'(1/√2) = 2√2 − c = 1.810 (todo en forma cerrada).
- *Prop. prop:curvpsi* (κ̂_d con el ángulo conservado): correcta; para (x, v) fijos la expresión es no decreciente en |a₀| y |κ_W|, y |a₀| ≤ V₁(1 − x) + rvK₁ (más fino que V₁(1+f)). Es una cota bajo (H₃) cuyo valor es un supremo en malla.
- *Observación adicional (propia)*: en d = 1 también la cota de curvatura antigua es analítica: 1/(rκ̄₁) = 1/(f g(√2)/(1−f) + 1/(1+ζ²)), ζ = 2(1−f)/(3f), con max g = g(√2) = 4√2/(3√3) = 1.08866 (derivada de y(y+2)²/(y+1)³ ∝ (y+2)(2−y)), creciente en f; en f = 1/2 vale 0.56149 > 1/2. Junto con c₁ ≥ 1/2 (Paso 4) y c₀′ > 0.509, **en d = 1 (H_c) con c = 1/2 queda demostrada analíticamente para todo f ≤ 1/2** (esto cierra también la opción del punto M1(b) del árbitro, y con más alcance: f ≤ 1/2 en vez de f ≤ 0.35).

**Corridas.** `theory/check_same_strand.py` y `theory/check_Hc.py` se copiaron a `experiments/` (solo cambian la ruta de importación y el directorio de salida) y se relanzaron: 25 s y 57 s de pared; los `*_summary.json` resultantes son **idénticos byte a byte** a los de `theory/` y las salidas de texto solo difieren en las líneas de tiempo. Script propio `verify_closed.py` (scratchpad `author2_RTK001/`) para las formas cerradas: β(π/3) = 0.548311, P₁ ≥ 0.81713, suma del Paso 4 ≥ 1.01703; τΩ̄ = 2.94038; δ_R1 = 1.06843; sin(δ_R1/2) = 0.50917; δ_R2^ap = 1.67737; Θ* = 1.11208; mín Λ/r en [π/3, π) a f = 1/2 = 1 (en δ = π/3, cota justa); 1/(rκ̄₁) = 1.79285 / 1.01936 / 0.56149 (f = 0.25 / 0.35 / 0.5).

**Discrepancia árbitro vs. agente teórico (pares críticos de la misma hebra).** Script propio e independiente de `theory/`: `experiments/classify_pairs.py` → `results/classify_pairs.{json,md}` (18 niveles: (2,3), f ∈ {0.25, 0.35, 0.5}, d = 1–3, N₀ ∈ {256, 512}; 49 s de CPU). Usa dos detectores: (i) pares de vértices doblemente críticos en el sentido de la §2.4 (mínimo local de la distancia en ambos índices) y (ii) celdas 2×2 donde cambian de signo a la vez (X_j − X_i)·T_i y (X_j − X_i)·T_j (necesario para un par doblemente crítico en la celda; detecta también sillas y máximos). Resultado:
- con (i), **ningún** par de misma hebra (k = 0) con bases distintas en ningún nivel (0 en 18 niveles): el dato del árbitro es correcto *para los pares que usa el proxy τ*;
- con (ii), hay pares doblemente críticos de misma hebra con δ < π **solo en d = 1** (f = 0.5: 27 celdas, δ ≥ 1.96, distancia ≥ 3.70 r; f = 0.35: δ ≥ 2.135, ≥ 5.23 r; f = 0.25: δ ≥ 2.356, ≥ 7.29 r), que no son mínimos locales de la distancia (sillas o máximos), y ninguno en d = 2, 3: el dato del agente teórico es correcto *para todos los pares doblemente críticos*.
- **Dato verdadero (el que se escribe):** en las cadenas (2,3) no hay pares doblemente críticos de misma hebra que sean mínimos locales de la distancia; los únicos pares doblemente críticos de misma hebra con δ < π aparecen en d = 1, son de tipo silla/máximo, tienen δ ≥ 1.96 (por encima del umbral demostrado δ_turn = 1.068) y distancia ≥ 3.70 r. Ambas afirmaciones eran ciertas; se referían a detectores distintos.
- Márgenes de M2 (mismo script): en f = 1/2 el siguiente par doblemente crítico (vértices) tras los antipodales de un disco está a 1.0140·2r (d = 2) y 1.0213·2r (d = 3) con N₀ = 256 — 1.4 % y 2.1 %, como dice el árbitro — y a 1.0138 y 1.0203 con N₀ = 512 (1.4 % y 2.0 %). En f = 0.35 los márgenes son 103 % y 109 %.

Estado: verificado. Lo que se integra y con qué etiqueta está en §3.
