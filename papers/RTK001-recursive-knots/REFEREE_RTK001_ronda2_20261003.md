# Informe de arbitraje interno — RTK001 "Geometry of Recursive Knots" (ronda 2, 03/10/2026)

Árbitro: agente independiente y nuevo (no es el árbitro de la ronda 1 ni el autor). Material revisado: `README.md`, `FICHA_RTK001_propuesta.md`, `CONTINUIDAD_RTK001_20260930.md`, `PLAN.md`, `REFEREE_RTK001_ronda1_20260930.md`, `RESPUESTA_RTK001_ronda1_20260930.md`, `manuscript/main.tex` (v0.2, 351 líneas), `numbers.tex`, `table_main.tex`, `refs.bib`, `experiments/*.py`, `results/*`, y la versión anterior en git (`b42ff3e`, `1686677`, solo lectura). **No se evaluó `theory/`** (otro agente trabaja allí en paralelo); solo se leyeron, para comprobar la clasificación de hebras que el manuscrito delega en ese código, las líneas 59–93 y 183–200 de `theory/check_Hc.py` y las líneas `[RESULT]`/`[D]` de `check_Hc_output.txt`. No se modificó nada de la carpeta salvo este informe. Scripts y salidas propias en el scratchpad `referee2_RTK001/` (`c1_check.py`, `curv_check.py`, `classify_check.py`, `classify_d23.py`, `macro_check.py`, `corollary_chain.py`, `repro/`, `build/`, `notes.md`). Salvo indicación, "l. N" es línea de `manuscript/main.tex` v0.2; la numeración de enunciados es la del PDF (Lema 3.7, Prop. 3.8, Prop. 3.9, Teorema 3.10, Obs. 3.11, Hip. 3.12, Cor. 3.13, Conj. 3.16).

## Veredicto

**Cambios menores.** Todos los pasos del Lema 3.7 (incluido el Paso 4 analítico), la identidad de curvatura de la Prop. 3.8, las Props. 3.5 y 3.9 y el Corolario 3.13 son correctos (verificados a mano y con código propio independiente de `check_Hc.py`), los 25 puntos de la ronda 1 están aplicados y la reproducción coincide bit a bit; pero hay que corregir el **estado** de varias afirmaciones antes de circular: constantes evaluadas en malla y con entradas medidas en polígonos se presentan como "proved" (resumen, Lema 3.7, Teorema 3.10, tabla de afirmaciones, README), la Conjetura 3.16 es tautológica tal como está escrita, la descripción de lo que queda abierto está desfasada respecto del propio bloque nuevo, y los números del Teorema dependen de un archivo de `theory/` que otro agente está modificando. Todo se resuelve con cambios de texto y de un script, sin demostraciones ni corridas nuevas obligatorias.

Recuento de hallazgos nuevos: **0 bloqueantes, 4 mayores, 13 menores.** Ronda 1: **23 aplicados bien, 0 a medias, 0 no aplicados, 2 aplicados con error nuevo** (B2, M2).

## Verificación de la ronda 1

| Id | Estado | Evidencia |
|---|---|---|
| B1 | aplicado bien | (H_c) reenunciada sobre la familia (l. 242–247); "Throughout" con parametrización heredada y v ∈ [v_min, v_max] (l. 104); pitch como propiedad de la familia (l. 92); Obs. 3.11 con ambos contraejemplos (l. 236–238, verificados: d² = 4r²cos²(qu/4)+v²u² y el término rvκ'); Corolario "conditional on H_c for the family" (l. 253); resumen y FICHA reescritos. El problema de estado del bloque nuevo es un hallazgo nuevo (M1), no un defecto de la aplicación de B1. |
| B2 | **aplicado con error nuevo** | "Criteria" (l. 282) declara que c = 1/2 se fijó tras fallar c = 1; "4 de 15" en l. 251, 284, 325, README, CONTINUIDAD (comprobado: fallan (2,3) f=.5 d=1 0.8316, (3,2) d=1 0.968, (3,2) d=2 0.9989, (2,5) d=1 0.5644). Error nuevo: (3,2) d = 2 aparece a la vez como fallo (`\HypFailOneList`) y como "attained with equality" (`\HypEqOneListOther` = "(3,2), d=2,3; (2,5), d=2,3"), l. 251; causa en `make_numbers.py:176–179` (fallo si ratio < 1−10⁻⁹, igualdad si |ratio−1| < 5·10⁻³: 0.9989 cumple ambas). Ver m3. |
| M1 | aplicado bien | l. 158 reescrita con (i)/(ii) y macros `\CritSepHalf` = 103.7°, `\CritBaseDistHalf` = 1.573 (coinciden con `aux_checks.json`, par [489, 1218], N₀ = 1024); "local" eliminado del resumen, Limitaciones y FICHA; paso interior (1−r)p/q y criterio r ≤ 0.4. Next steps (1) quedó desfasado por el contenido nuevo (M3). |
| M2 | **aplicado con error nuevo** | Prop. 3.5 correcta (l. 140–145; cuerda −2rU ⊥ K_d' por (5); Rop ≥ 2π(p(1−f)/f)^d, macros 12.6/25.1/50.3 correctas); observación de crecimiento p/f (l. 276–278, cocientes comprobados). Error nuevo: la conjetura reducida (l. 272–274) es tautológica (M2 nuevo). |
| M3 | aplicado bien | Lema 3.2 con Lk = Wr − α/2π ∈ ℤ válido en α = π (l. 120–124, signo y semientero comprobados); código `lk_real = Wr − α/2π; n_frame = rint(lk_real)` con residuo guardado (`recursive_knots.py:216–223`); residuo máximo |·| 1.13·10⁻³ fino / 4.55·10⁻³ total (`make_numbers.py:195–198` usa abs); convención de cable autocontenida; FICHA corregida; r* = 0.4904 (`aux_checks.json`). |
| M4 | aplicado bien (variante textual declarada) | Párrafo "Writhe accuracy" (l. 288), tabla (l. 328: "stable to 10⁻⁴"), Limitaciones (5); writhe poligonal exacto no implementado, declarado como paso siguiente. |
| M5 | aplicado bien | l. 254–262: ρ₀ = 1, r_d := fρ_{d−1}, ρ_d := γρ_{d−1}; (H_c) para todo r_d ≤ f·thick; inducción explícita correcta; A = 5, Λ = 20 (c = 1/2) y 10 (c = 1) correctos. |
| M6 | aplicado bien | README "11 páginas a 10 pt" (PDF: 11 páginas, comprobado); "wall-clock" (l. 346); frase de la sonda en d = 2 (l. 290); residuo en CONTINUIDAD l. 25. (La propia RESPUESTA se contradice: §5 dice "12 páginas", el Resumen "11"; ver m10.) |
| m1 | aplicado bien | l. 80. |
| m2 | aplicado bien | l. 106 (r < τ), l. 117. |
| m3 | aplicado bien | l. 104. |
| m4 | aplicado bien | l. 137, `\NoTwistMinRatio` = 1.255 (recalculado: 1.2555). |
| m5 | aplicado bien | l. 158. |
| m6 | aplicado bien | frase del "crossover" eliminada (grep sin resultados). |
| m7 | aplicado bien | l. 282. |
| m8 | aplicado bien | l. 68. |
| m9 | aplicado bien | l. 72, `Fenchel1929` (verificada aquí, ver Bibliografía). |
| m10 | aplicado bien | l. 100 (τ_pt como salvaguarda, segmento–segmento 0.99994/1.00000/0.99993 = `aux_checks.json`). |
| m11 | aplicado bien | † y nota en el pie de la Tabla 1. |
| m12 | aplicado bien | Tabla 4 eliminada; frase en l. 265. |
| m13 | aplicado bien | Fig. 1 en minipage de 0.58\textwidth. |
| m14 | aplicado bien | compilación propia sin cajas desbordadas. |
| m15 | aplicado bien | `Chern1967` eliminada; `Rawdon2003` citada en l. 100; DOIs de CKS y Pierański añadidos. |
| m16 | aplicado bien (con matiz declarado) | "about 32.7 (numerical, uncertified)" (l. 269). Ashton–Cantarella–Piatek–Rawdon 2011 ya está verificada (ver Bibliografía) y puede añadirse. |
| m17 | aplicado bien | `make_numbers.py:47` comenta "wall-clock minutes"; texto l. 346. |

## Hallazgos nuevos

### Bloqueantes

Ninguno. Se verificó paso a paso todo lo nuevo (detalle en "Verificación computacional" y en los hallazgos); no se encontró ningún error matemático que invalide un enunciado.

Resumen de la verificación del bloque nuevo (para que el autor sepa qué se comprobó y qué no):
- **Lema 3.7, Paso 1** (cuerda–arco en curva gruesa): correcto; un mínimo local de g en (0, L) da cuerda ⊥ T(y) y ρ_pt = |x−y|/2 ≥ τ; la monotonía de g en las componentes de {g < 2τ} y la integración de g' ≥ √(1 − g²/4τ²) dan ℓ ≥ 2τ sin(δ/2) y a, b ≤ πτ; la dicotomía δ ≥ π ⇒ |x−y| ≥ 2τ usa σ ≤ L/2 correctamente.
- **Paso 2**: (E2) |T̄ − T(x)| ≤ δ/2; (E3) |w·e| ≤ |w|(δ/2)(σ/ℓ) ≤ |w|β; (E4) con E(δ) por tramos; (E5) U₂ − Ũ₂ = −∫κ_⊥vT, componente ⊥e ≤ ∫κv|T − T̄| ≤ δ²/3; (E6) Δψ = ms + 2πqk/p (rehecha la cancelación de holonomía con N₀ extendido: el ángulo de U₂ respecto de N₀(t₁+s) es ψ(t₁) + ms + 2πqk/p − kα + kα). Todo correcto.
- **Paso 3**: A ≥ ℓ − 2rE/ℓ ≥ Λ (usa |U_i·(y−x)| ≤ E en ambos extremos), |Q| ≥ r[2|cos(u/2)|√(1−β²) − δ²/3]₊, u ≤ δ/Θ_min. Correcto.
- **Paso 4**: correcto en sustancia; dos deslices de redondeo (m1). Ínfimo propio: c₁(1/2, 2/3) = 0.611895 en δ = 1.2332 (malla de 2·10⁶ puntos + refinamiento acotado), compatible con la macro 0.6117 (que es el valor de malla menos una corrección Lipschitz estimada).
- **Paso 5**: correcto: τ_{d−1} ≤ 2^{−(d−1)} por la Prop. 3.5, v_min ≥ 1 por (5) con p(1−f) ≥ 1, m ≤ 2 ⇒ Θ_min ≥ 2^{d−2}; Θ_min = 2/3 en d = 1. Monotonía de c₁ en f y Θ_min correcta.
- **Prop. 3.8**: identidad |K_d'×K_d''|² = b_U²|K_d'|² + (c_W a − c_T b_W)², con a = a₀ − 2rvmκ_W, rederivada a mano (U' = mW − κ_⊥vT, W' = −mU − κ_W vT, T' = v(κ_⊥U + κ_W W)) y comprobada numéricamente en una curva cerrada no plana de velocidad no uniforme (error relativo 1.8·10⁻⁵, del orden de las diferencias finitas); la cota κ̄_d se cumple (cociente κ_max/κ̄ = 0.75 y 0.35 para f = 0.25, 0.5). max g = g(√2) = 1.08866 comprobado.
- **Prop. 3.9**: correcta (σ_d ≥ π/κ̄_d por el argumento de giro del tangente; u ≥ ms₀ y u ≥ δ/Θ_max).
- **Clasificación de hebras**: el texto (l. 165) y el código (`theory/check_Hc.py:187–195`) usan la misma regla (arco base más corto en longitud de arco; k = rint((Δt − s)/2π) mod p). Con código propio: el par crítico de f = 1/2, d = 1 es k = 1 (índices [489, 1218], N₀ = 1024: arco corto −295 pasos, k = (1218 − 489 + 295)/1024 = 1, δ = 1.81), igual que el de (2,5).
- **Corolario 3.13** y **Prop. 3.5**: correctos (inducción y A·L(K_{d−1}) comprobados).

### Mayores

**M1. Constantes evaluadas en malla, y con entradas medidas en polígonos, se presentan como demostradas.**
- *Ubicación:* resumen l. 55 ("this gives c₁ ≥ \HcConeBase > 1/2 at every depth"); enunciado del Lema 3.7 l. 181 ("hence c₁ ≥ \HcConeBase > 1/2 … every such pair is at distance ≥ min(2(τ−r), \HcTwoConeBase r)", con status "proved here"); Teorema 3.10 l. 233 ("satisfies c₁ ≥ \HcConeBase", "the bound with c = 1/2 is proved for f ≤ 0.35 at d = 1 unconditionally and at d = 2,3 under (H₃) with the measured constants"); estado de la Hip. 3.12 l. 249 ("Proved for all d … with c = \HcConeBase"); tabla de afirmaciones l. 321 y l. 323; README ("Parte demostrada: hebras distintas con c₁ = 0.61 …; con c = 1/2 todo el enunciado para f ≤ 0.35 (incondicional en d = 1 …)"); CONTINUIDAD l. 41 y 76 ("constantes demostradas 0.32/0.13/0.16").
- *Problema:* (a) Lo demostrado analíticamente (Paso 4) es c₁(1/2, 2/3) ≥ 1/2. El valor 0.6117 es un mínimo en malla de 20 000 puntos menos 2·Lip·paso con Lip **estimada en la misma malla** (`theory/check_Hc.py:76–93`, docstring "certified"): no es una cota demostrada. Mi cálculo independiente da 0.611895, así que "≥ 0.6117" es numéricamente cierto, pero no está probado; y "\HcTwoConeBase r = 1.223 r" tampoco. (b) En d = 1 (base = círculo, sin hipótesis) las constantes c₀ y 1/(rκ̄) que deciden "c = 1/2 para f ≤ 0.35" son ínfimos en malla: c₀ se calcula en una malla 2-D de 1500 × 400 puntos **sin ninguna corrección** (`check_Hc.py:59–74`), en contra de lo que dice Limitaciones (7) ("with an estimated Lipschitz correction"). Mis valores independientes (c₀ = 0.6512, 1/(rκ̄) = 1.0194 en f = 0.35; 1.3265 y 1.7929 en f = 0.25) coinciden con las macros y el margen sobre 1/2 es amplio, pero "proved … unconditionally" no es exacto. (c) En d = 2, 3 la cota usa τ = thick(K_{d−1}), que **no se conoce** (solo el proxy poligonal no certificado de la §2.4), y V₁, K₁, v_min, v_max medidos por diferencias en el polígono base: lo que hay es una evaluación numérica no certificada de una cota condicional demostrada, no "proved under (H₃)". Es precisamente la distinción demostrado/medido que la línea dice cuidar.
- *Corrección concreta:*
  - Resumen: sustituir "in the default family (2,3) this gives c₁ ≥ \HcConeBase > 1/2 at every depth" por "in the default family (2,3) this gives c₁ ≥ 1/2 at every depth (numerically c₁ ≈ \HcConeBase)".
  - Lema 3.7, l. 181: "Moreover c₁(½, ⅔) ≥ ½ (a grid evaluation gives \HcConeBase), hence c₁ ≥ ½ whenever f ≤ ½ and Θ_min ≥ ⅔. For the default family … every such pair is at distance ≥ min(2(τ−r), r)."
  - Teorema 3.10: status "[proved here, under (H₃); the numerical values below are grid evaluations, not certified]"; sustituir "Hence the bound with c = 1/2 is proved for f ≤ 0.35 at d = 1 unconditionally and at d = 2,3 under (H₃) with the measured constants" por "Hence, at d = 1 (where no hypothesis is needed), a grid evaluation of the explicit one- and two-variable functions c₀, c₁, κ̄ gives c ≥ 0.65 > 1/2 for f ≤ 0.35; at d = 2, 3 the same evaluation with τ, v, V₁, K₁ measured on the polygons gives c ≥ 0.65. Neither is a certified computation."
  - Estado de la Hip. 3.12, l. 249: "Proved for all d for pairs on different strands with c = 1/2 (Lemma 3.7; numerically c₁ ≈ \HcConeBase)…; the curvature and same-strand constants are evaluated on grids at d = 1 and, with polygon-measured inputs, at d = 2, 3".
  - Tabla l. 321: "c₁ ≥ 1/2 (grid value \HcConeBase)" | "proved (c₁ ≥ 1/2); grid value uncertified". l. 323: estado "grid evaluation of proved bounds at d = 1; at d = 2, 3 with polygon-measured inputs (uncertified)".
  - Limitaciones (7): "The constant c₁(½,⅔) ≥ ½ is proved analytically; all other constants of Theorem 3.10 are grid infima (c₁ with a Lipschitz correction estimated on the grid itself, c₀ on a 1500 × 400 grid without correction), not interval-arithmetic bounds."
  - README y CONTINUIDAD: "demostradas" → "evaluadas en malla" para 0.61, 0.32/0.13/0.16, 0.49.
  - Opcional (cierra el punto (b) a coste bajo): repetir para c₀ en d = 1, f = 0.35 el argumento por subintervalos del Paso 4 (es una función explícita de δ con u = 1.5δ, porque en d = 1 Θ_min = Θ_max) y declarar d = 1, f ≤ 0.35 realmente demostrado.

**M2. La Conjetura 3.16 es tautológica tal como está escrita.**
- *Ubicación:* l. 272–274 ("thick(K_d) = r_d exactly whenever the antipodal pair in a normal disc is the doubly critical pair"); tabla l. 330; README; CONTINUIDAD l. 44.
- *Problema:* por (1), thick = min(minRad, dcsd/2). Si el par antipodal (distancia 2r) es el par doblemente crítico que realiza dcsd, entonces thick = min(minRad, r), y la "conjetura" equivale a minRad(K_d) ≥ r_d en esos casos, que no es lo que los números sugieren ni lo que interesa. El contenido real es que, por debajo de un umbral de f, ningún otro par doblemente crítico está más cerca que 2r_d. Además, en f = 1/2, d = 2, 3, que el texto presenta como casos observados (l. 273, l. 286), el margen es muy pequeño: con código propio (`classify_d23.py`, N₀ = 256) los pares doblemente críticos con arco base ≥ πτ ("far") están a 1.014·2r₂ y 1.021·2r₃; es decir, τ_d = r_d en f = 1/2 se decide por un 1.4–2.1 %.
- *Corrección concreta:* "Conjecture 3.16. For the default family there are thresholds f_*(d) > 0, with inf_d f_*(d) > 0, such that for f ≤ f_*(d) every doubly critical pair of K_d other than the antipodal pairs of one normal disc is at distance > 2r_d and minRad(K_d) > r_d; hence thick(K_d) = r_d (the inequality ≤ is Proposition 3.5). Numerically f_*(1) ∈ (0.35, 0.5) and f_*(2), f_*(3) ≥ 0.5, the latter by margins of 1.4 % and 2.1 %." Añadir en l. 286: "at f = 1/2, d = 2, 3 the next-closest doubly critical pairs (base points at arc ≥ πτ) are only 1.4 % and 2.1 % farther than 2r_d, so f = 1/2 is close to the threshold at which τ_d = r_d fails" (generar ambas cifras como macros). Actualizar la fila l. 330.

**M3. La descripción de lo que queda abierto está desfasada respecto del bloque nuevo y no está respaldada por los datos.**
- *Ubicación:* l. 249 ("the measured same-strand doubly critical pairs are far from this bound"); Next steps (1), l. 340 ("At d = 1 the uncovered case is an explicit, certifiable computation: the minimal distance between the strands of T(p,q) on the torus … (the critical pair at f = 1/2 is the pair across the hole, not a local helix pair)"); Limitaciones (1).
- *Problema:* (a) He clasificado todos los pares doblemente críticos de vértices de las cadenas (2,3) con f = 0.35 y 0.5, d = 1, 2, 3 (N₀ = 256, regla del texto). Clases encontradas: mismo disco; "far" (arco ≥ πτ); k = 1 solo en f = 0.5, d = 1 (3 pares, 0.8316). **No hay ningún par doblemente crítico de misma hebra (k = 0) con bases distintas en ningún nivel.** La frase "measured same-strand pairs are far from this bound" no tiene objeto: el caso abierto no tiene instancias en los datos (con la salvedad, ya declarada en l. 100, de que la prueba de mínimo local puede omitir pares de tipo silla). (b) Next steps (1) sigue diciendo que en d = 1 lo no cubierto es el par a través del agujero; pero ese par es de hebras distintas (k = 1, δ = 1.81) y está cubierto por el Lema 3.7 (cota 2c₁r = 0.61 frente a 0.83 medido), como reconoce la propia RESPUESTA (M1). En d = 1 lo único abierto es k = 0, cuya constante c₀ = 0.32 está fijada por la cota inferior crude u ≥ ms₀ (mi ínfimo cae exactamente en δ = 0.392 = s₀, el borde de la restricción).
- *Corrección concreta:* l. 249: sustituir la frase por "no same-strand doubly critical vertex pair with distinct base points is detected at any depth of the (2,3) chains (f = 0.35, 0.5), so the open case is a limitation of the method (the bound u ≥ ms₀ is crude), not an observed near-contact". Next steps (1): "At d = 1 the base is the round circle and only the same-strand case remains: show that the torus knot T(2,3) on the torus (1, r) has no same-strand doubly critical pair with distinct base points at distance < r for r ≤ 1/2 (an explicit two-variable computation, certifiable with interval arithmetic); this would make d = 1 fully proved." Generar la clasificación como macro desde un script de `experiments/` (puede usarse `classify_d23.py` del scratchpad como base).

**M4. Los números del Teorema 3.10 dependen de un archivo de `theory/` que otro agente está modificando.**
- *Ubicación:* `experiments/make_numbers.py:262–275` lee `theory/check_Hc_summary.json` (45 macros `\Hc…`); apéndice l. 346 remite a `theory/check_Hc.py`; README "Reproducir".
- *Problema:* `git status` muestra `theory/same_strand_derivation.md` sin seguimiento y `Hc_lemma.tex` modificado a las 05:20, después de `check_Hc_summary.json` (05:03): la carpeta está viva. Si el agente de teoría relanza o cambia `check_Hc.py`, el siguiente `build.sh` cambia en silencio las constantes del Teorema; si el archivo desaparece, `if os.path.exists(hcp)` omite las macros y el LaTeX falla con macros indefinidas. El manuscrito v0.2 no queda reproducible por sí solo.
- *Corrección concreta:* congelar la evaluación usada en v0.2: copiar `theory/check_Hc.py` a `experiments/check_Hc_v02.py` y su salida a `results/check_Hc_summary.json`, hacer que `make_numbers.py` lea solo `results/`, registrar el SHA-256 de ambos en CONTINUIDAD y en el apéndice, y quitar el `if os.path.exists` (que falle explícitamente).

### Menores

- **m1. Paso 4 del Lema 3.7, dos deslices numéricos** (l. 190). "β ≤ β(π/3) ≤ 0.548" es falso: β(π/3) = (π/3)²/2 = 0.548311. "P₁ ≥ 0.816 and P₁² ≥ 0.666" es falso como implicación: 0.816² = 0.665856. La conclusión sobrevive (con los valores exactos de los extremos: √(1−β²) ≥ 0.83627, δ²/3 ≤ 0.36554, P₁ ≥ 0.81713, P₁² ≥ 0.66770, 4 sin²(0.3) = 0.34933, suma ≥ 1.0170). Texto sustituto: "β ≤ β(π/3) < 0.5484, so √(1−β²) > 0.8362, δ²/3 ≤ 0.3656, hence P₁ ≥ 2·0.7071·0.8362 − 0.3656 > 0.817 and P₁² > 0.667; with 4 sin²(0.3) > 0.349 the sum exceeds 1.01." Los demás números del Paso 4 están bien (φ(1/√2) = 0.29289, φ(1) = 0.42920, φ'(1/√2) = 1.828, φ''(1/√2) = 4, cos 0.45 = 0.90045, β(0.6) = 0.30455, √(1−0.305²) = 0.95235, P₁ ≥ 1.5953 en (0, 0.6]). Nótese que en δ = π/3 el término Λ vale exactamente 1 (cota justa): conviene decir que el argumento usa la desigualdad no estricta.
- **m2. Teorema 3.10: citas incompletas y etiqueta de estado** (l. 228–231). La deducción usa también la Prop. 3.6(a) (pares del mismo disco, que fijan thick ≤ r y por eso c ≤ 1) y (b) junto con el Paso 1 del Lema 3.7 (arco ≥ πτ ⇒ cuerda base ≥ 2τ); la Prop. 3.9 solo trata δ < π. Escribir "by (1), Proposition 3.6, Lemma 3.7 (including Step 1) and Propositions 3.8–3.9". La desigualdad del Teorema está demostrada bajo (H₃); lo "parcial" son los valores. Cambiar el status según M1. (Comprobado que c₁ ≤ 1 siempre, porque el límite δ → 0 da exactamente 1; no hay riesgo de c > 1.)
- **m3. (3,2), d = 2 listado a la vez como fallo y como igualdad** (l. 251). Corregir `make_numbers.py:176–179`: tolerancia común `tol = 5e-3`; fallo si `ratio1 < 1 - tol`, igualdad si `abs(ratio1 - 1) <= tol` y excluir de `eq_one` los niveles que estén en `fails_one`. O, si se quiere conservar 0.999 como fallo, quitar "(3,2), d = 2" de la lista de igualdades.
- **m4. Resumen, precisión** (l. 55). (i) "(H₃) … bound on |K'_{d−1}|' and |κ'_{d−1}|": (H₃) acota √(κ₁'² + κ₂'²) = √(κ'² + v²κ²τ_tors²) (curvaturas del marco paralelo), que incluye la torsión; escribir "on the derivatives of the speed and of the parallel-frame curvature vector of K_{d−1}". (ii) "κ_{d−1}" en la cota de longitud no está definido en el resumen: escribir κ_max(K_{d−1}). (iii) "every pair of points of K_d on different strands": añadir "with distinct base points (strands relative to the shorter base arc)"; para p = 2, K_d es una sola curva y "hebra" solo tiene sentido relativo a un arco (l. 165).
- **m5. Choques de notación.** K₁ es el nudo de profundidad 1 (l. 92) y la constante de (H₃) (l. 196); V₁ análogo; c₀ es la constante universal de Buck–Simon (l. 269) y la constante de misma hebra (l. 218). Renombrar las constantes de (H₃) (p. ej. M_v, M_κ) y la de Buck–Simon (c_BS).
- **m6. Cuantificador de la Hip. 3.12 y la cadena del Corolario.** l. 243: precisar "there is c = c(p,q,f) such that, for every sequence (r_d) with r_d ≤ f·thick(K_{d−1}) and every d ≥ 1, …". La comprobación numérica solo cubre r_d = f·τ_poly(K_{d−1}), no la cadena r_d = fρ_{d−1} del Corolario, de ahí "indicative only" (l. 265). He calculado esa cadena (`corollary_chain.py`, N₀ = 256 y 512, idénticos a 4 cifras): f = 1/2: τ_d/ρ_d^{(c=1/2)} = 1.663, 2.000, 2.000 y L/τ = 38.4, 256.5, 2051.8 frente a la cota 126, 2513, 50265; f = 0.35: 40.8, 466.2, 5328 frente a 147, 3449, 80801; f = 0.25: 53.8, 860.6, 13769 frente a 176, 4926, 137928. Sustituir "(the two chains use different r_d, so the comparison is indicative only)" por esta comparación directa (una línea y tres macros).
- **m7. Limitaciones (7)** (l. 338): "with an estimated Lipschitz correction" no es cierto para c₀ (malla 2-D sin corrección) y la corrección de c₁ usa una constante de Lipschitz estimada en la propia malla. Texto en M1.
- **m8. Remark 3.15 desactualizada sobre números de cruce** (l. 269, y Next steps (5) l. 340). "For the iterated cables of Lemma 3.2 the crossing number is not known in general (crossing numbers of satellites are an open problem), so the only lower bound we have is the one internal to the family": Kalfagianni y McConkey (Bull. London Math. Soc. 2024; arXiv:2309.03814) determinan el número de cruce de los 2-cables de nudos adecuados, y el trébol es alternante, luego adecuado: eso cubre K₂ (comprobar que su convención (p,q) corresponde al cable (2, 9)/(2, 11) del Lema 3.2). Lackenby (Algebr. Geom. Topol. 14 (2014) 2379–2409) da Cr(satélite) ≥ 10⁻¹³ Cr(compañero) en general. Reescribir: "for K₂ the crossing number is known [KalfagianniMcConkey2024], which with [BuckSimon1999] gives a knot-type lower bound at d = 2; for d ≥ 3 only general satellite bounds [Lackenby2014] are available". Actualizar la FICHA ("el número de cruces de los cables iterados no se conoce en general" → "solo se conoce en profundidad 2").
- **m9. CONTINUIDAD l. 47** clasifica Gonzalez–Maddocks, Bishop, Călugăreanu, White, Fuller y Lickorish como "Seguras" y en la misma línea como "Coherentes pero no verificadas en línea". Unificar con la tabla de Bibliografía de este informe (seis de ellas quedan verificadas).
- **m10. RESPUESTA §5** dice "pasa de 10 páginas (11 pt) a 12 páginas a 10 pt"; su Resumen y el README dicen 11. El PDF tiene 11. Corregir §5.
- **m11. README/CONTINUIDAD heredan M1**: README "Parte demostrada: hebras distintas con c₁ = 0.61" y "con c = 1/2 todo el enunciado para f ≤ 0.35 (incondicional en d = 1, bajo (H₃) con constantes medidas en d = 2, 3)"; CONTINUIDAD l. 41 y 76 "constantes demostradas 0.32/0.13/0.16". Aplicar los textos de M1.
- **m12. Teorema 3.10, presentación**: la lista de 27 constantes en prosa (l. 233) es ilegible; pasarla a una tabla 3 × 3 (f × d) con (c₁, c₀, 1/(rκ̄)) o a `results/` con una frase. Ahorra ≈ 8 líneas.
- **m13. Tipo de letra.** La v0.2 bajó de 11 pt a 10 pt (l. 1) para absorber ≈ 2.5 páginas nuevas; 11 páginas a 10 pt equivalen a ≈ 13 a 11 pt. Ver "Extensión".

## Bibliografía

Red: solo WebSearch (no se intentaron Crossref ni arXiv directamente). "Verificada" = autor, título, revista, volumen, páginas y año coinciden con un resultado de búsqueda; "coherente" = no buscada en esta sesión.

| Entrada | Estado | Corrección / nota |
|---|---|---|
| BuckSimon1999 | verificada en la ronda 1 | — |
| CKS2002 | verificada en la ronda 1; DOI presente | — |
| LSDR1999 | verificada en la ronda 1 | — |
| GonzalezMaddocks1999 | **verificada** (PNAS 96, 4769–4773, 1999) | quitar de "no verificadas" en CONTINUIDAD |
| Bishop1975 | **verificada** (Amer. Math. Monthly 82(3), 246–251, 1975) | idem |
| Calugareanu1961 | **verificada** (Czechoslovak Math. J. 11, 588–625; EUDML doc 12099) | EUDML titula "… et leur invariants"; comprobar la grafía del original frente a "leurs" del .bib |
| White1969 | **verificada** (Amer. J. Math. 91(3), 693–728) | añadir DOI 10.2307/2373348 |
| Fuller1971 | **verificada** (PNAS 68(4), 815–819) | añadir DOI 10.1073/pnas.68.4.815 |
| Rawdon2003 | **verificada** (Exp. Math. 12(3), 287–302, Project Euclid) | — |
| Lickorish1997 | coherente (GTM 175, Springer 1997), no buscada | ya no sostiene la convención de cable (autocontenida); bien |
| Pieranski1998 | verificada en la ronda 1; DOI presente | — |
| Fenchel1929 (nueva) | **verificada** (Math. Ann. 101, 238–252, 1929) | añadir DOI 10.1007/BF01454836 |
| *Sugerida:* Ashton, Cantarella, Piatek, Rawdon, "Knot tightening by constrained gradient descent", Exp. Math. 20(1), 57–90 (2011) | verificada (datos bibliográficos; el valor 32.74 del trébol no se confirmó en los extractos) | puede citarse junto a Pierański para el ≈ 32.7 (m16 de la ronda 1) tras comprobar la cifra en el artículo |
| *Sugerida:* Kalfagianni, McConkey, "Crossing numbers of cable knots", Bull. London Math. Soc. (2024), arXiv:2309.03814 | verificada (resumen: Cr de 2-cables de nudos adecuados) | m8 |
| *Sugerida:* Lackenby, "The crossing number of satellite knots", Algebr. Geom. Topol. 14(4), 2379–2409 (2014) | verificada | m8 |

Resumen: de las 12 entradas, 10 verificadas (4 en la ronda 1, 6 aquí), 1 coherente sin buscar (Lickorish), 0 erróneas; 3 DOIs que añadir; 3 referencias sugeridas, verificadas.

## Verificación computacional

Todo en el scratchpad `referee2_RTK001/`, un hilo (`OMP_NUM_THREADS=1`). CPU total ≈ 2.3 min.

| Qué | Tiempo | Resultado |
|---|---|---|
| `c1_check.py`: c₁(f, Θ) desde la definición (8) del texto, malla de 2·10⁶ + refinamiento; subafirmaciones del Paso 4; max g | 5 s | c₁(½,⅔) = 0.611895 (δ = 1.2332); c₁(0.35,⅔) = 0.9661; c₁(0.5,0.4) = 0.4885 [(2,5) d=1, < ½]; c₁(0.5, 2.19) = 0.6993; c₁(0.5, 9.59) = 0.7068; c₁ = 1 en f = 0.25. Coinciden con las macros (0.61, 0.97, 0.49, 0.70, 0.71, 1.00). Paso 4: dos deslices (m1), conclusión correcta (mín. de Λ² + P₁² en (0, π/3] = 1.668; mín. de Λ en [π/3, π/2] = 1; en [π/2, π) = 1.414). |
| `curv_check.py`: identidad y cota de la Prop. 3.8 en K(t) = (cos t + 0.3 cos 2t, sin t − 0.3 sin 2t, 0.4 sin 3t), marco de Bishop por EDO (rtol 10⁻¹²), α = 0.745 | 4 s | |K_d'| fórmula vs diferencias: 2·10⁻⁹; κ fórmula vs diferencias: ≤ 1.8·10⁻⁵; κ_max(K_d) ≤ κ̄_d (cocientes 0.746, 0.351). |
| `classify_check.py` (d = 1, N₀ = 512, base exacta) | 5 s | c₀ = 1.3265 / 0.6512 / 0.3236 y 1/(rκ̄) = 1.7929 / 1.0194 / 0.5615 (f = 0.25/0.35/0.5): coinciden con las macros. Pares doblemente críticos: solo mismo disco y (f = 0.5) 3 pares k = 1 a 0.8316 ≥ 0.6119 = cota. Todos los pares k = 1 (no solo críticos): mín. 0.8316 (f = 0.5), 0.7001 ≥ 0.676 (f = 0.35). |
| `classify_d23.py` (d = 1–3, N₀ = 256) | 8 s | Ningún par doblemente crítico k = 0 con bases distintas en ningún nivel (M3). f = 0.5: "far" a 1.014·2r (d = 2) y 1.021·2r (d = 3) (M2). |
| `macro_check.py`: 60 macros por nivel (Rop, τ, Wr, slope, L) + agregados recalculados desde `results.json` | < 1 s | 0 discrepancias. HypMinTauOverRho 1.663, AllMinTauOverRho 1.129, MinRadOverRMin 1.147, NoTwistMinRatio 1.2555, LenLowerOk 36/36, LenBoundOk 36/36, PtMaxRel 0.011 %, residuo de Lk 1.13·10⁻³ / 4.55·10⁻³, crecimientos 8.007/8.000, 5.728/5.715, 4.056/4.002: todos coinciden. Doble listado de (3,2) d = 2 (m3). |
| Reproducción: copia de `recursive_knots.py --fast` | 67 s pared (44 s user + 22 s sys) | 6 cadenas comunes con `results.json` (N₀ = 512; 256 para (3,2)), 456 campos numéricos: diferencia relativa máxima **0**. |
| `corollary_chain.py`: cadena r_d = fρ_{d−1} del Corolario (f = 0.25/0.35/0.5; N₀ = 256, 512) | 27 s | (H_c) con c = ½ se cumple (márgenes 1.66–2.0); L/τ muy por debajo de 2πΛ^d (m6). |
| Compilación de una copia (`latexmk -pdf`) | 3 s | 11 páginas, 0 errores, 0 "??", 0 referencias/citas indefinidas, 0 cajas desbordadas. |

No se relanzaron `aux_checks.py`, `shrink.py` ni `check_Hc.py` (este último por estar en `theory/`); sus salidas se contrastaron con cálculos propios donde se usan en el texto (par crítico, c₀, c₁, κ̄).

## Extensión y presentación

El PDF tiene 11 páginas a 10 pt (la v0.1 tenía 10 a 11 pt). El bloque teórico nuevo justifica ≈ 2 páginas, pero el estado de las mismas afirmaciones se repite cuatro o cinco veces (final del Teorema 3.10, párrafo de estado bajo la Hip. 3.12, "On the constant", tabla de afirmaciones, Limitaciones (1) y (7)). Recortes concretos, con objetivo de 10 páginas a 10 pt (o 11 a 11 pt):
1. Dejar el estado detallado solo en la tabla de afirmaciones; reducir el párrafo de estado de la Hip. 3.12 a dos líneas y las tres últimas frases del Teorema 3.10 a una tabla 3 × 3 (m12). ≈ 0.4 p.
2. Fusionar "On the constant" con el párrafo "Results" de la §4 (ambos repiten el recuento con c = 1). ≈ 0.2 p.
3. Obs. 3.11: conservar los dos mecanismos en cuatro líneas; la discusión "In the recursive family both quantities are controlled…" ya está en el Lema 3.7 y la Hip. 3.12. ≈ 0.15 p.
4. Sonda de acortamiento (l. 290): una frase y la fila de la tabla; es material de v0.1, negativo y no certificado. ≈ 0.1 p.
5. Fusionar las Observaciones 3.15 (cotas inferiores) y 3.17 (crecimiento). ≈ 0.1 p.
6. Eliminar la Fig. 1 (tres proyecciones xy que no muestran la estructura 3D; ya sugerido en la ronda 1). ≈ 0.3 p.

## Lista final de acciones (por prioridad)

1. Reetiquetar el estado de las constantes (M1): c₁ ≥ ½ demostrado, 0.6117 valor en malla; "proved … unconditionally" en d = 1 y "proved under (H₃) with measured constants" en d = 2, 3 → evaluación en malla / con entradas medidas, no certificada; aplicar en resumen, Lema 3.7, Teorema 3.10, estado de la Hip. 3.12, tabla de afirmaciones, Limitaciones (7), README y CONTINUIDAD.
2. Reescribir la Conjetura 3.16 con un umbral f_* y la condición sobre los demás pares doblemente críticos; reportar el margen de 1.4 %/2.1 % en f = ½, d = 2, 3 (M2).
3. Corregir la descripción de lo abierto: no hay pares doblemente críticos de misma hebra en los datos; en d = 1 solo queda k = 0; reescribir Next steps (1) (M3). Generar la clasificación como macro desde `experiments/`.
4. Congelar `check_Hc.py` y su salida en `experiments/`/`results/` con hash, y que `make_numbers.py` no lea `theory/` (M4).
5. Corregir los dos deslices del Paso 4 (m1) y completar las citas del Teorema 3.10 (m2).
6. Arreglar el doble listado de (3,2) d = 2 en `make_numbers.py` (m3).
7. Precisar el resumen: (H₃) incluye la torsión, κ_max(K_{d−1}), "hebras" relativas al arco (m4).
8. Renombrar las constantes de (H₃) y la de Buck–Simon (m5).
9. Precisar el cuantificador de la Hip. 3.12 e incluir la comparación directa con la cadena del Corolario (m6).
10. Actualizar la Obs. 3.15, Next steps (5) y la FICHA con Kalfagianni–McConkey 2024 y Lackenby 2014 (m8).
11. Añadir DOIs de Fenchel, White y Fuller; revisar la grafía del título de Călugăreanu; actualizar la lista de verificadas en CONTINUIDAD (Bibliografía, m9).
12. Corregir "12 páginas" en la RESPUESTA §5 (m10).
13. Aplicar los recortes 1–6 de "Extensión" y pasar la lista de constantes del Teorema a una tabla (m12, m13).
