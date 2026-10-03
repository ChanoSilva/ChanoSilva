# Respuesta del autor a la ronda 2 de revisión interna — RTK001 (03/10/2026)

Informe atendido: `REFEREE_RTK001_ronda2_20261003.md` (cambios menores; 0 bloqueantes, 4 mayores, 13 menores; ronda 1: 23 bien, 2 con error nuevo: B2, M2).
Además, en esta pasada se integra el trabajo de `theory/` sobre el caso "misma hebra" (`theory/same_strand_lemma.tex`, `same_strand_derivation.md`, `check_same_strand.py` y su salida), terminado por el agente teórico durante la ronda 2.

Documento escrito de forma incremental (estado de trabajo al final de cada sección).

## 0. Plan y estado de trabajo (final)

- [x] Verificación propia del bloque "misma hebra" de `theory/` (§1).
- [x] M4: evaluación de `theory/` congelada en `experiments/` + `results/` con SHA-256; `make_numbers.py` lee solo `results/`.
- [x] B2/m3: tolerancia única en `make_numbers.py`.
- [x] M1: etiquetas de estado en resumen, Lema 3.7, Teorema, Hip., tabla, Limitaciones, README, CONTINUIDAD, FICHA.
- [x] Integración del bloque misma hebra tras la antigua Prop. 3.9 (§3).
- [x] M2: Conjetura con umbral f_*(d) y márgenes por macro.
- [x] M3: lo abierto.
- [x] Menores m1–m13, bibliografía, recortes.
- [x] Compilación (12 páginas, 0 errores, 0 indefinidas, 0 "??"), CONTINUIDAD, README, FICHA.

Numeración: "Lema 3.7", "Prop. 3.8" igual que en v0.2; en v0.3 los enunciados nuevos son Lema 3.9 (exclusión por giro), Prop. 3.10 (misma hebra), Cor. 3.11 (familia por defecto), Prop. 3.12 (curvatura con ψ), Teorema 3.13 (antes 3.10), Obs. 3.14 (antes 3.11), Hip. 3.15 (antes 3.12), Cor. 3.16 (antes 3.13), Obs. 3.17–3.18, Conj. 3.19 (antes 3.16), Obs. 3.20. La antigua Prop. 3.9 (misma hebra bajo (H₃), constante c₀) se retira por superada (véase "Extensión").

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

## 2. Respuesta punto por punto al informe

### Verificación de la ronda 1 (puntos aplicados con error nuevo)

| Id | Decisión | Qué se cambió |
|---|---|---|
| B2 (doble listado de (3,2), d = 2) | aceptar | Véase m3: una sola tolerancia; (3,2) d = 2 queda solo como fallo (0.999), y se comprobó que el déficit es real a la precisión de los datos: 0.99889 (N₀ = 256) → 0.99886 (N₀ = 512). La lista de igualdades es ahora "(3,2), d = 3; (2,5), d = 2,3". |
| M2 (conjetura reducida tautológica) | aceptar | Véase M2 nuevo. |

### Mayores

**M1 (estado de las constantes) → aceptar, y con un resultado mejor del pedido.** Criterio aplicado en todo el texto: "proved" solo para desigualdades analíticas (c₁(½, ⅔) ≥ ½; c₀′ ≥ ½; 1/(rκ̄₁) > 0.561 en d = 1; los umbrales δ_turn ≥ π/3); "grid value / grid evaluation, not certified" para 0.6117, 0.509, 0.845, 1.034, etc.; "grid evaluation of a bound proved under (H₃), inputs measured on polygons (uncertified)" para d = 2, 3. Cambios: resumen (c₁ ≥ ½ y no "≥ 0.6117 > ½"; "1.223 r" sustituido por "r"); Lema 3.7 (texto propuesto por el árbitro, con "a grid evaluation gives 0.6117"); Paso 4 (el valor de malla se declara "grid infimum with a Lipschitz constant estimated on the grid itself, not a certified bound", y se menciona que la evaluación independiente del árbitro coincide a cuatro cifras, sin tipear su cifra, que no sale de nuestro código); Teorema 3.13 con estado "[proved here; (b) under (H₃); the values in Table 1 are grid evaluations, not certified]"; las 27 constantes en prosa pasan a la Tabla 1 (m12) con la misma advertencia; estado de la Hip. 3.15; tabla de afirmaciones (filas separadas para lo demostrado y lo evaluado); Limitaciones (4) con el texto del árbitro (incluido que c₀ de v0.2 se evaluaba en una malla 1500 × 400 sin corrección); README, CONTINUIDAD y FICHA ("demostradas" → "evaluadas en malla" para 0.61, 0.32/0.13/0.16, 0.49). La opción que el árbitro dejaba como "opcional" (demostrar d = 1) queda resuelta con más alcance: en d = 1 las tres constantes son analíticamente ≥ ½ para **todo** f ≤ ½ (c₁ por el Paso 4; c₀′ > 0.509 por el Cor. 3.11; 1/(rκ̄₁) = 1/(f g(√2)/(1−f) + 1/(1+ζ²)) > 0.561, creciente en f), así que grosor(K₁) ≥ r₁/2 está demostrado (Teorema 3.13(c)).

**M2 (conjetura tautológica) → aceptar.** Conjetura 3.19 reenunciada con umbrales f_*(d) > 0, inf_d f_*(d) > 0, y la condición "todo par doblemente crítico distinto de los antipodales de un disco está a distancia > 2r_d y minRad(K_d) > r_d". Numéricamente el mayor f_*(1) admisible está en [0.35, 0.5) y f_*(2), f_*(3) ≥ 0.5 por márgenes de solo 1.4 % y 2.1 % (macros `\MarginHalfTwo`, `\MarginHalfThree` desde `experiments/classify_pairs.py`, N₀ = 256; con N₀ = 512, 1.4 % y 2.0 %, también citados). La frase pedida está en la §4 ("but narrowly: …"), y la fila de la tabla de afirmaciones lleva los márgenes.

**M3 (lo abierto, desfasado) → aceptar, actualizado además por la integración.** (a) La frase "the measured same-strand doubly critical pairs are far from this bound" desaparece; en la §4 se escribe el dato reconciliado del censo (§1): ningún par de vértices doblemente crítico de misma hebra en 18 niveles, y con el test de cambio de signo solo en d = 1 (δ ≥ 1.96 > δ_turn, distancia ≥ 3.70 r₁ en f = ½), ninguno en d = 2, 3. (b) Next steps (1) ya no habla del par a través del agujero (cubierto por el Lema 3.7, como dice el árbitro) ni del caso misma hebra (demostrado ahora): lo abierto es (H₃) uniforme en d y la certificación. La clasificación sale de un script de `experiments/` como pidió el árbitro.

**M4 (dependencia de `theory/`) → aceptar.** `theory/check_Hc.py` y `theory/check_same_strand.py` copiados a `experiments/` cambiando solo la ruta de importación y el directorio de salida; relanzados: `results/check_Hc_summary.json` y `results/check_same_strand_summary.json` son idénticos byte a byte a los de `theory/` (SHA-256 `dcc6745b…cdcdc` y `4797be4e…eefd`; lista completa, con los hashes de los scripts y de los originales, en `results/FROZEN_THEORY_SHA256.txt`). `make_numbers.py` ya no lee `theory/`; el `if os.path.exists` se sustituyó por `need()`, que aborta con un mensaje si falta un insumo. Apéndice y README actualizados.

### Menores

| Id | Decisión | Qué se cambió |
|---|---|---|
| m1 | aceptar (con un ajuste) | Paso 4: "β ≤ β(π/3) < 0.5484, √(1−β²) > 0.8362, δ²/3 ≤ 0.3656; P₁ > 2·0.7071·0.8362 − 0.3656 > 0.8169, P₁² > 0.667; con 4 sin²(0.3) > 0.349 la suma > 1.01". Ajuste: el texto sugerido por el árbitro decía "P₁ ≥ 2·0.7071·0.8362 − 0.3656 > 0.817", pero 2·0.7071·0.8362 − 0.3656 = 0.81696 < 0.817; con las cotas truncadas solo se garantiza 0.8169 (el valor exacto 0.81713 sí supera 0.817). Se añade que en δ = π/3, Λ = 1 exactamente (desigualdades no estrictas). |
| m2 | aceptar | La prueba del Teorema 3.13 cita Prop. 3.6(a) (mismo disco), Paso 1 del Lema 3.7 + Prop. 3.6(b) (δ ≥ π), Lema 3.7 (k = 1), Prop. 3.10 (k = 0) y Props. 3.8/3.12 (curvatura); se anota c₁ ≤ 1. |
| m3 | aceptar | `make_numbers.py`: `EQ_TOL = 5e-4` común (fallo si ratio < 1 − tol; igualdad si |ratio − 1| ≤ tol), con aserciones `EQ_TOL > ConvMaxRelTau` y de disjunción. Se eligió 5·10⁻⁴ y no el 5·10⁻³ sugerido porque el déficit de (3,2) d = 2 (1.1·10⁻³) es estable al duplicar N y mayor que la variación de τ por resolución (0.03 %): es un fallo real, no ruido. Macro `\EqTolPct` en el texto. |
| m4 | aceptar | Resumen: (H₃) "on the derivatives of the speed and of the parallel-frame curvature vector of K_{d−1}" (y en la Prop. 3.8 se anota que κ₁'² + κ₂'² incluye la torsión); κ_max(K_{d−1}); hebras "defined relative to the shorter base arc". |
| m5 | aceptar | Constantes de (H₃) → M_v, M_κ; constante de Buck–Simon → c_BS. |
| m6 | aceptar | Cuantificador de (H_c): "for every sequence (r_d) with r_d ≤ f thick(K_{d−1}) and every d ≥ 1". Cadena del Corolario medida con script propio (`experiments/corollary_chain.py`, coincide con el del árbitro): f = ½: L/τ = 38.4, 256.5, 2051.9 frente a 126, 2513, 50265; τ_d/ρ_d ≥ 1.66 para f ∈ {0.25, 0.35, 0.5}; sustituye a "indicative only". |
| m7 | aceptar | Limitaciones (4) reescrita (véase M1). |
| m8 | aceptar con matiz | Verificado por WebSearch: Kalfagianni–McConkey, Bull. LMS 56(11) 3400–3411 (2024), DOI 10.1112/blms.13140: Teor. 1.1, Cr(K_{p,q}) ≥ q²Cr(K) + 1 para K adecuado (q = número de hebras); Cor. 1.2, Cr(K_{p,2}) = 4Cr(K) + 1 si p = 2wr(K) ± 1; el resumen dice que determinan Cr de los 2-cables de nudos adecuados. Lackenby, AGT 14(4) 2379–2409 (2014): Cr(satélite) ≥ 10⁻¹³ Cr(compañero). Matiz: el texto completo de K–M no fue accesible (arXiv, Wiley y ResearchGate bloqueados por el proxy), así que no se cotejó su convención de cable/writhe con el Lema 3.2 y no se da Cr(K₂) exacto; la Obs. 3.18 afirma solo Cr(K₂) ≥ 13 y que el valor está determinado por [K–M]; Next steps (5) pide el cotejo. FICHA: "solo está acotado o determinado en profundidad 2". |
| m9 | aceptar | CONTINUIDAD: lista única de verificadas (10 + 2 nuevas), Lickorish como única coherente no buscada. |
| m10 | aceptar | RESPUESTA de la ronda 1, §5: "11 páginas" con nota de corrección. |
| m11 | aceptar | README/CONTINUIDAD con los textos de M1. |
| m12 | aceptar | Tabla 1 (f ∈ {0.35, 0.5} × d, con c₁, c₀′ (δ_turn), 1/(rκ̂_d), c y τ_d/r_d medido; f = 0.25 en una frase del pie: todos ≥ 0.999). |
| m13 | aceptar con matiz | Se mantiene 10 pt; la extensión sube a 12 páginas por el bloque nuevo (véase "Extensión"). |

### Bibliografía

DOIs añadidos: Fenchel (10.1007/BF01454836), White (10.2307/2373348), Fuller (10.1073/pnas.68.4.815) y Călugăreanu (10.21136/CMJ.1961.100486, número 4). Grafía de Călugăreanu: DML-CZ (el archivo de la revista) titula "… et leurs invariants", que es la del .bib; EUDML escribe "leur"; se mantiene "leurs". Nuevas entradas verificadas: KalfagianniMcConkey2024, Lackenby2014. Ashton–Cantarella–Piatek–Rawdon 2011 no se añade (la cifra 32.7 no se confirmó en los extractos, como dice el árbitro). 14 entradas: 13 verificadas, 1 coherente (Lickorish).

### Extensión y recortes

v0.2: 11 páginas; v0.3: **12 páginas** a 10 pt (el máximo de esta pasada). El bloque de misma hebra (Lema 3.9, Prop. 3.10, Cor. 3.11, Prop. 3.12, Teorema 3.13 nuevo y Tabla 1) ocupa ≈ 1.6 páginas; sin recortes el PDF llegaba a 14. Recortes aplicados: (1) estado detallado solo en la Tabla 1 y la tabla de afirmaciones, párrafo de estado de la Hip. reducido, constantes del Teorema a tabla; (2) "On the constant" condensado y su repetición en "Results" eliminada; (3) Obs. 3.14 abreviada; (4) sonda de acortamiento en una frase; (5) no se fusionaron las Obs. 3.18 y 3.20 (las separa la conjetura), pero la de crecimiento se condensó; (6) Fig. 1 retirada (sigue en `figures/fig_curves.pdf`, citada en la §4). Además: **la antigua Prop. 3.9** (misma hebra bajo (H₃), c₀ = 0.32/0.13/0.16 en f = ½) **se retira por superada** por la Prop. 3.10 (que no necesita (H₃) para d ≥ 2 y da c₀′ ≥ ½); se cita en una frase con sus valores y sigue disponible en la v0.2 y en `theory/Hc_lemma.tex`. También se condensaron la observación del término de giro, "Criteria", la escritura del writhe (que pasó al párrafo de resultados), la tabla de afirmaciones y el apéndice. No se bajó a 10 páginas: haría falta retirar demostraciones (Pasos 1–4 del Lema 3.7 o la Prop. 3.10), que son el contenido verificable nuevo.

## 3. Qué se integró de `theory/` y con qué estado

| Pieza (origen) | Dónde en v0.3 | Estado declarado |
|---|---|---|
| Lema lem:turn (exclusión por giro) | Lema 3.9 | proved here |
| Ángulo de cono χ y rutas R1/R2, Prop. prop:samestrand | párrafo previo + Prop. 3.10 | proved here (δ_R2 sin (H₃); δ_R1 bajo (H₃)) |
| Cor. cor:samefamily, con la cota a priori nueva Θ_min ≥ √13·2^{d−3} | Cor. 3.11 | proved here; los umbrales δ_R1 > 1.0684 (d = 1, f = ½), δ_R2 > 1.677 (d ≥ 2), c₀′ > 0.509 son analíticos (formas cerradas, redondeadas hacia abajo); el valor 0.74 para d ≥ 2 del texto de `theory/` **no** se incluye en el enunciado (es de malla) |
| Prop. prop:curvpsi (κ̂_d con ψ conservado) | Prop. 3.12 | proved here, under (H₃); valores 1/(rκ̂_d) = supremos en malla con corrección por incrementos |
| Obs. rem:samestrand-constants | Tabla 1 + una frase | grid evaluation, not certified (entradas medidas en los polígonos para d ≥ 2) |
| "Consequence for Theorem/Hypothesis" | Teorema 3.13(c), estado de la Hip. 3.15, Cor. 3.16 | proved: ½dcsd(K_d) ≥ min(τ − r, r/2) = r/2 en toda profundidad sin (H₃); grosor(K₁) ≥ r₁/2; para d ≥ 2, (H_c) con c = ½ ⟺ minRad(K_d) ≥ r_d/2, que bajo (H₃) se evalúa en malla en d = 2, 3 (1/(rκ̂) = 1.034, 0.998 en f = ½) |
| `check_same_strand.py` y su salida | `experiments/check_same_strand.py`, `results/check_same_strand_*` | copia congelada, salida idéntica |

Crédito: el resumen, la introducción y el párrafo que abre el bloque dicen que el caso misma hebra "was obtained in the second round of review". Correcciones hechas al integrar: el redondeo "0.5092" → "> 0.509" (cota inferior; el valor es 0.509170); "Θ_min ≥ 1.8028" → "> 1.802"; el argumento φ_c en [π/2, π) se escribe con c_* = 2 sin(δ_R1/2) exacto y valores en forma cerrada; la afirmación "the only [same-strand pairs] with δ < π appear at d = 1, with δ ≥ 1.96 and distance ≥ 3.70 r" se precisa como pares detectados por cambio de signo (sillas/máximos), no mínimos locales (§1).

## 4. Números que cambiaron

- Experimentos: ninguno (no se tocó `recursive_knots.py`; `results.json` sin cambios; no hizo falta relanzar la corrida de referencia).
- `\HypEqOneListOther`: "(3,2), d = 2,3; (2,5), d = 2,3" → "(3,2), d = 3; (2,5), d = 2,3" (B2/m3). `\HypFailOne` sigue en 4.
- Constantes de malla ahora redondeadas hacia abajo (`floor_fmt`): c₁ en la tabla 0.611 / 0.699 / 0.706 (f = ½), 1/(rκ̄) en f = ½, d = 2: 0.48 (v0.2: 0.49).
- Nuevos: c₀′, δ_turn, 1/(rκ̂_d), c (Tabla 1); formas cerradas del Cor. 3.11; márgenes 1.4 / 2.1 % (2.0 % con N₀ = 512) y 103 / 109 % (f = 0.35); censo de pares; cadena del Corolario (38.4 / 256.5 / 2051.9; margen ≥ 1.66); `\WrMarginHalf` = 0.018 (antes tipeado a mano, igual que "10⁻⁴" de la tabla, ahora `\WrDiffDefaultOne`).
- Cifras eliminadas: "1.223 r" (`\HcTwoConeBase`), "c₁ ≥ 0.6117 > ½" como cota demostrada.

## 5. Compilación

`manuscript/build.sh` (make_numbers + latexmk): 0 errores, 0 advertencias en `main.log`, 0 referencias/citas indefinidas, 0 cajas desbordadas, `pdftotext main.pdf - | grep -c "??"` = 0. Páginas: 11 → 12. Revisadas visualmente las páginas con la Tabla 1 (p. 8), la Tabla 2 y la figura (pp. 9–10) y la tabla de afirmaciones (p. 10).

## 6. Qué queda abierto

(i) (H₃) uniforme en d (cerraría (H_c) con c = ½ en toda profundidad para (2,3) y haría incondicional el Corolario 3.16); (ii) certificación por intervalos de c₁, c₀′, κ̂_d y del grosor poligonal; (iii) p ≥ 3 y otros patrones; (iv) Conjetura 3.19; (v) writhe poligonal exacto; (vi) Cr(K₂) exacto (cotejo de convenciones con Kalfagianni–McConkey); (vii) Lickorish 1997 sin buscar.

## 7. Cómputo

`check_Hc.py` 57 s y `check_same_strand.py` 25 s de pared (núcleos compartidos), `classify_pairs.py` 49 s de CPU, `corollary_chain.py` 26 s de CPU, formas cerradas < 1 s, compilaciones ≈ 1.5 min. Total ≈ 4 min de CPU (≤ 10).
