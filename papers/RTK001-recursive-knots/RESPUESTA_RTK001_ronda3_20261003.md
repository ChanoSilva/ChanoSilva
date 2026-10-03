# Respuesta del autor al informe de árbitro, ronda 3 — RTK001

Fecha: 03/10/2026. Manuscrito: v0.3 → v0.4 (fecha fija 3 October 2026).
Objeto: (A) informe `REFEREE_RTK001_ronda3_20261003.md` (cambios menores; 0 bloqueantes, 1 mayor, 10 menores; ronda 2: 19 de 20 bien, 1 a medias);
(B) integración del resultado **parcial** sobre la uniformidad de (H_3) (`theory/H3_uniform_lemma.tex`, `theory/H3_uniform_derivation.md`, `theory/check_H3.py` y su salida).

Documento escrito de forma incremental (terminado).

Numeración de v0.4: Lema 3.7 y Prop. 3.8 sin cambios (la antigua Prop. 3.12 es ahora la Prop. 3.8(b)); Lema 3.9; Prop. 3.10; Cor. 3.11; **Teorema 3.12** (antes 3.13); Obs. 3.13 (antes 3.14); bloque nuevo (H_3): Lema 3.14 (velocidad), Prop. 3.15 (curvatura), Cor. 3.16 (tolerancia), Prop. 3.17 (no clausura), Obs. 3.18; Hip. 3.19 (antes 3.15); Cor. 3.20 (antes 3.16); Obs. 3.21–3.22; **Conj. 3.23** (antes 3.19); Obs. 3.24.

## 1. Verificación independiente del lema (H_3)

Hecha **antes** de pegar nada en el manuscrito. Trabajo auxiliar en el scratchpad (`author3_RTK001/`): `check_H3_copy.py` (copia de `theory/check_H3.py` con solo `ROOT` cambiado, para no sobrescribir `theory/check_H3_output.txt`) y `verify_H3.py` (script propio que no usa ningún código del autor ni de `theory/`), con su salida `verify_H3_output.txt`.

### 1.1 Re-ejecución de `check_H3.py`
- Copia ejecutada el 03/10/2026: 7.6 s de pared y unos 7.6 s de CPU (4.4 s de usuario y 3.2 s de sistema).
- Salida **idéntica línea a línea** a `theory/check_H3_output.txt`, salvo las líneas de tiempo (`diff` filtrando `done in` y `total`).

### 1.2 Lectura de cada enunciado y de su prueba (rehecha a mano)
- **Forma en longitud de arco.** ν = sup|v'|/v² es invariante por t ↦ pt (ṽ = p v(p·), ṽ' = p²v'). μ = sup|Π_⊥ dκ/dσ| es geométrica. κ_par' = κ₁'N₀ + κ₂'B₀ es la parte normal de dκ/dt, porque dκ/dt = κ_par' − vκ²T. Se cumplen M_v ≤ ν v_max², M_κ ≤ μ v_max y ε = rκ_max ≤ f. Además ζ' ≥ ζ_min, porque ε ≤ f. **Correcto.**
- **Lema lem:speedrec.**
  - w² = c_T² + r²m², con rm constante.
  - x' = r(κ_par'·U + mκ_W), usando κ·U' = κ·(mW − vκ_⊥T) = mκ_W. Por tanto c_T' = a₀ − rvmκ_W.
  - |w'|/w² = c_T|a₀ − rvmκ_W|/w³ ≤ |a₀ − rvmκ_W|/c_T², porque w ≥ c_T.
  - Se acota con |v'| ≤ νv², |κ_par'| ≤ μv, |κ_W| ≤ κ_max y 1 − x ≥ 1 − ε. **Correcto.**
- **Prop. prop:curvrec.** Es el reparto de Minkowski de la Prop. 3.8, rehecho:
  - Primer término: A(A+B) ≤ (A+2B)², y (A+2B)/(A+B)^{3/2} es decreciente en A ≥ v²(1−ε)². Con ζ = v(1−ε)/(rm) se obtiene κ g(ζ)/(1−ε) ≤ κ_max G(ζ')/(1−ε).
  - Segundo término: rm²/(A+B) ≤ 1/(r(1+ζ'²)).
  - Tercer término: rm|a₀|/(A+B)^{3/2} ≤ rm v²(ν(1+ε) + rμ)/(v³(1−ε)³) ≤ λ(ν(1+ε) + rμ)/(1−ε)³.
  - **Correcto.** La proposición no usa el grosor, salvo para garantizar ε < 1.
- **Cor. cor:tolerance (d ≥ 3).** Ingredientes:
  - ζ' ≥ ζ_min ≥ Θ_min ≥ √13·2^{d−3} ≥ √13, por la cota a priori del Cor. 3.11, que exige f_j ≤ ½ en todo nivel.
  - g es decreciente en [√2, ∞), luego G(ζ') ≤ g(√13).
  - Con ε ≤ ½: ε/(1−ε) ≤ 1, (1+ε)/(1−ε)³ ≤ 12 y (1−ε)^{−3} ≤ 8.
  - r_d ≤ 2^{−d}, por la Prop. 3.5. λ = (1−f_d)/ζ_min ≤ 2^{3−d}/√13.
  - De ahí r_dκ_max(K_d) ≤ g(√13) + 1/14 + (96/√13)4^{−d}ν + (64/√13)8^{−d}μ. El Teorema 3.13(c) concluye.
  - **Correcto.** Constantes recalculadas con mpmath (30 dígitos): g(√13) = 1.0324544, 2 − g(√13) − 1/14 = 0.8961170, 96/√13 = 26.6256, 64/√13 = 17.7504.
- **Prop. prop:noclose.**
  - **El razonamiento es correcto:** la única aparición de una cuarta derivada de K en K_d''' es κ_⊥'' dentro de −r(vκ_⊥)''T, y su coeficiente en la parte normal es −r v sin χ ≠ 0.
  - La perturbación ε^{7/2}Φ((t−t₀)/ε)U(t₀) mantiene acotados (de hecho, convergentes en C³) los datos de (H_3) y sup|v''|, y hace crecer κ_par''·U(t₀) como ε^{−1/2}.
  - Además, Π_⊥K_d''' = 3ww'κ_d + w²Π_⊥ dκ_d/dt (comprobado a mano).

### 1.3 Defectos encontrados (corregidos al integrar; `theory/` no se toca)
1. **Fórmula inexacta en prop:noclose.** El enunciado escribe la parte normal como «−r sin χ (v κ_par''·U + v''κ_⊥ + 2v'κ_⊥')» a lo largo de n_χ. Eso no es una igualdad.
   - El cálculo simbólico (sympy, cálculo del marco móvil (T, U, W)) da estos coeficientes en K_d'''·n_χ:
     - de κ_⊥'', exactamente −r v sin χ (correcto);
     - de v'', (1 − x) sin χ, porque K''' aporta v''T. El enunciado da −r κ_⊥ sin χ.
   - Además faltan términos de orden 3, como v(2mκ_par'·W − m²κ_⊥).
   - La derivación (`H3_uniform_derivation.md` §1) sí escribía «+ R_3». Al pasar al .tex se perdió el resto.
   - **Corrección:** el enunciado integrado dice que Π_⊥K_d''' = −r v sin χ (κ_par''·U) n_χ + R. El resto R está acotado por v_max, κ_max, ν, μ, sup|v''|, r y m. La conclusión no cambia.
2. **Cuantificador de prop:noclose.** «No inequality μ(K_d) ≤ F(…) holds» solo se sigue del argumento para F **localmente acotada** (por ejemplo, continua o monótona): la perturbación hace converger los argumentos de F mientras μ(K_d) → ∞. Para una F arbitraria, F podría explotar a lo largo de la sucesión. **Corrección:** «no locally bounded F».
3. **Redondeo hacia el lado inseguro y tasa no demostrada en rem:H3status.**
   - «μ hasta 0.0505·8^d» redondea **hacia arriba** un umbral suficiente: el valor exacto es 0.0504843. Debe decir 0.0504, redondeado hacia abajo (0.0336 para ν sí es correcto: 0.0336562).
   - Ambos umbrales valen **cada uno por separado**; juntos rige la condición suma (eq:tol).
   - «coefficient r_d sin χ_d = O(8^{−d}) in the family» no está demostrado. A priori, sin χ_d ≤ λ/(1−ε) ≤ 2λ ≤ 2^{4−d}/√13 y r_d ≤ 2^{−d}, luego solo r_d sin χ_d ≤ (16/√13)·4^{−d} = O(4^{−d}). El decaimiento ≈ 8^{−d} es **medido** en los polígonos (0.416, 0.057, 0.0063 y 0.00086 en d = 1, 2, 3 y 4).
   - **Corrección:** «O(4^{−d}) a priori, ≈ 8^{−d} on the polygons».

### 1.4 Comprobación numérica independiente en curvas lisas (`verify_H3.py`, 2 s de CPU)
- **Construcción.** K₁ es un polinomio trigonométrico exacto: ((1 + r₁ sin 3s) cos 2s, (1 + r₁ sin 3s) sin 2s, r₁ cos 3s). El marco de Bishop se integra con DOP853 (rtol 10⁻¹²) desde la normal convencional e_z. K₂ se deriva espectralmente (cola de Fourier ≤ 10⁻¹⁵).
- **Resultados** (cociente medido/cota):

| f₁ | r₂ | ν(K₂)/cota del Lema | κ_max(K₂)/cota de la Prop. |
|---|---|---|---|
| 0.5 | 0.2079 | 0.231 | 0.453 |
| 0.35 | 0.1225 | 0.405 | 0.825 |
| 0.25 | 0.0625 | 0.603 | 0.916 |

- Los cocientes coinciden a tres cifras con los de `check_H3.py` en los polígonos.
- ν(K₁) = 0.4182 y μ(K₁) = 4.544 en f = ½ coinciden con los valores poligonales 0.418 y 4.54.
- En f = ½ y con el **mayor r₂ admisible**, r₂ = r₁/2 = 0.25, se obtiene r₂·cota = 1.146 < 2. Es una evaluación en malla, no una demostración. Sugiere que d = 2 se reduce a un cálculo certificable sobre la curva explícita K₁ (se anota como paso siguiente; d = 2 sigue **abierto**).
- Identidades simbólicas (sympy): K_d' = v(1−x)T + rmW; w' = c_T(a₀ − rvmκ_W)/w; a = a₀ − 2rvmκ_W; b_U, b_W; |K_d'×K_d''|² = b_U²(A+B) + (c_Wa − c_Tb_W)²; c_Wa − c_Tb_W = rma₀ − κ_W v(A+2B). Todas con **residuo 0**.

### 1.5 Veredicto de la verificación
Lema lem:speedrec, Prop. prop:curvrec y Cor. cor:tolerance: **correctos tal como están**. Prop. prop:noclose: **correcta en sustancia**, con la fórmula del enunciado reescrita (resto R) y el cuantificador restringido a F localmente acotada. Observación rem:H3status: dos números corregidos (0.0505 → 0.0504; O(8^{−d}) → O(4^{−d}) a priori). Todo lo integrado lleva «proved here» (las pruebas) o «verified numerically / grid evaluation» (los números de malla). **La uniformidad de (H_3) sigue abierta**, y d = 2 también.


### 1.6 Cómo se integró
- Párrafo «Towards (H_3) uniformly in d (added in v0.4)» tras la Obs. 3.13. Contiene: definiciones de ν y μ; Lema 3.14, Prop. 3.15, Cor. 3.16 y Prop. 3.17 (corregida), con sus pruebas; y la Obs. 3.18 (corregida), etiquetada «grid evaluation with polygon inputs; uniformity open».
- El vector curvatura se escribe en negrita, para no chocar con el índice de hebra k.
- Los números de la Obs. 3.18 salen de macros:
  - los de malla, de `results/check_H3_summary.json`, generado por `experiments/check_H3.py` (copia congelada de `theory/check_H3.py`: solo cambia el directorio de salida y se añade el resumen JSON; salida de texto idéntica salvo tiempos);
  - las formas cerradas (0.8961, 0.0336, 0.0504, 0.685, 16/√13 < 4.44), calculadas en `make_numbers.py` y redondeadas hacia el lado seguro.
- SHA-256 de la copia, del JSON, de la salida y de los cuatro originales de `theory/` añadidos a `results/FROZEN_THEORY_SHA256.txt`: 17/17 OK.
- Estado «open» de la uniformidad de (H_3) y de d = 2 en el resumen, la introducción, el estado de la Hip. 3.19, la tabla de afirmaciones (fila «(H_c) … ; (H_3) uniformly in d; the case d = 2 → open»), Limitaciones (1) y Next steps (1).

## 2. Hallazgos del informe de ronda 3

Recuento: **13 aceptados, 1 aceptado con matiz (extensión), 0 rebatidos.** Los 13 son: M1, m1–m10, el DOI de Lickorish y la errata de la RESPUESTA de ronda 2.

### M1 (mayor) — normalización del marco no fijada → **aceptado**
- **Def. 2.1.** Ahora fija N_{d−1}(0) como la proyección unitaria de e_z sobre el plano normal en K_{d−1}(0) (e_x si |T(0)·e_z| > 0.9), que es la convención de `recursive_knots.py:72–76`. Añade que rotar N_{d−1}(0) un ángulo β equivale a φ_d ↦ φ_d + β. También se cita en la §2.2 («fixed in Definition 2.1») y en el Apéndice A.
- **Tras la Def. 2.1.** Nuevo párrafo: todos los resultados de la §3 valen para toda elección de N_{d−1}(0) y φ_d; L y τ no dependen de ella a la precisión impresa; los márgenes de la Conjetura 3.23 sí dependen.
- **Medición** (`experiments/phase_margin.py` → `results/phase_margin.json` → macros `\Phase*`; 142 s de CPU, dentro de los 3 min). Como φ + π da la misma curva (p = 2, q impar), basta barrer β ∈ [0, π). En f = ½:
  - **d = 2**, 12 normales iniciales del marco de K₁: margen entre **1.37 % y 21.3 %**. Tiene periodo π/3 por la simetría de orden 3 de K₁. La normalización por defecto está cerca del mínimo (1.40 % a N₀ = 256, 1.38 % a N₀ = 512).
  - El rango 1.37–2.28 % del árbitro (cinco β, construcción lisa) cae dentro del nuestro. Su máximo es menor porque sus cinco β no muestrean los picos de 21 % (cerca de π/6 + kπ/3).
  - **d = 3**, 20 normales del marco de K₂ (12 en [0, π) más 8 de refinamiento junto al mínimo), con la de K₁ fija: margen entre **0.23 % y 13.0 %**. El mínimo está en β₃ ≈ 0.465 y es estable al duplicar N₀ (0.239 % → 0.233 %).
  - En los 36 casos, τ_d = r_d y L(K_d) cambia menos de 10⁻⁵ en términos relativos. Ningún par doblemente crítico de misma hebra o de hebras distintas aparece.
- **Conjetura 3.23** (antes 3.19): «f_*(2), f_*(3) ≥ 0.5: by margins of only 1.4 % and 2.1 % for the normalisation of Definition 2.1, and of at least 1.37 % and 0.23 % over the normalisations tested». La §4 y la tabla de afirmaciones lo repiten; Limitaciones (3) declara la dependencia.
- **Dato nuevo, más fino que el del árbitro.** En d = 3, f = ½ queda solo un 0.23 % por debajo del umbral para alguna normalización. El barrido de d = 3 es unidimensional (β₂ fijo); un barrido 2-D (β₂, β₃) excedía el presupuesto y queda abierto.

### Menores
| Id | Decisión | Qué se cambió y dónde |
|---|---|---|
| m1 (Θ* = 1.112, no 1.12) | aceptado | `\SsThetaStar` = `floor_fmt(Θ*, 3)` = 1.112 (Cor. 3.11, d ≥ 2). Además se escribe en `make_numbers.py` la regla general: cotas inferiores y umbrales de condiciones suficientes se redondean hacia abajo; cotas superiores, hacia arriba; una condición necesaria «needs y ≥ a», hacia abajo. Revisadas con esa regla todas las macros ceil/floor (`SsTauOmegaHalf` ↑, `SsDeltaROneHalf` ↓, `SsSinHalf` ↓, `SsPhi*` ↓, `SsThetaAp` ↓, `SsDeltaRTwoAp` ↓, `KbarOneHalf` ↓, `GMax` ↑, nuevas `\Hthree*`). La regla destapó un error análogo en `theory/` (umbral μ 0.0505 → 0.0504; §1.3) |
| m2 (δ_turn redondeado al más cercano) | aceptado | `\SsDturn*` = `floor_fmt(·, 3)`. Cambia en la Tabla 1 (f = 0.35, d = 1): 1.344 → 1.343. Las macros de f = 0.25, que no se imprimen, también cambian (3.016 → 3.015, 3.131 → 3.130) |
| m3 (calificador del censo) | aceptado | §4: «no doubly critical vertex pair on the same strand with base arc < πτ and distinct base points». También en el README y en la CONTINUIDAD |
| m4 (choques de notación) | aceptado y ampliado | ω (giro de cierre) frente a ϖ (tasa de giro, prueba de la Prop. 3.10); x₀, y₀ = puntos base en el Lema 3.7 (x = rκ_⊥ queda para las Props. 3.8, 3.10 y 3.15); A_e = componente en el Paso 3; 𝒜 en el Cor. 3.20; Λ_Rop en el resumen, el Cor. 3.20, la Obs. 3.21 y la tabla de afirmaciones; s_p = cuerda (Prop. 3.6). **Además:** el arco del Lema 3.9 y de la prueba de la Prop. 3.10 pasa a Γ (chocaba con γ del Cor. 3.20), y el vector curvatura del bloque (H_3) va en negrita (chocaba con el índice de hebra k) |
| m5 (Limitaciones (4)) | aceptado | «Only the thresholds c₁ ≥ ½, c₀′ ≥ ½, 1/(rκ̄₁) > 0.561, the closed forms of Corollary 3.11 and the constants of Corollary 3.16 are analytic» |
| m6 (C^{1,1} en el Lema 3.9) | aceptado | «This holds whenever Γ is C^{1,1} and its total turning …», y en la prueba «(T_Γ is Lipschitz, hence absolutely continuous)» |
| m7 (c* en la prueba de d = 1) | aceptado | La prueba se hace en f = ½ con c* := 2 sin(δ_R1(½)/2) fijo. Se transfiere a f < ½ porque [δ_turn(f), π) ⊂ [δ_R1(½), π) y Λ/r crece al bajar f. El enunciado dice «(and c₀′ > 0.509 for every f ≤ ½)» |
| m8 (Kalfagianni–McConkey) | aceptado | Obs. 3.22: «their Corollary 1.2 gives the exact value 4Cr(K)+1 for the slopes 2w ± 1 (w the writhe of a reduced alternating diagram), i.e. ±5, ±7 for the trefoil, and does not cover the slopes 9 and 11 of K₂, so we do not quote Cr(K₂)». Se retira «they determine the crossing numbers of 2-cables» (es del resumen del artículo; no se ha podido cotejar con el texto completo). Precisión propia: la conclusión no depende de la quiralidad, porque \|2w ± 1\| ∈ {5, 7}. FICHA: «acotado inferiormente», ya no «acotado o determinado» |
| m9 (`\SsCzeroAp` 0.74 sin uso) | aceptado | Macro y función auxiliar eliminadas de `make_numbers.py`, con un comentario que explica qué era (½ ínf max(Λ, ℓ₀ − 2r) = 0.7436, no ½ ínf Λ = 0.7148) |
| m10 (equivalencia en el enunciado) | aceptado | Teorema 3.12(c): «for d ≥ 2, (H_c) with c = ½ holds at level d if and only if minRad(K_d) ≥ r_d/2». La prueba tiene una línea más; la tabla de afirmaciones lo recoge |

### Bibliografía
- **Lickorish 1997** — aceptado: DOI 10.1007/978-1-4612-0691-0 añadido a `refs.bib`; pasa a «verificadas» en la CONTINUIDAD (verificación del árbitro de ronda 3).
- **Errata de la RESPUESTA de ronda 2 (§1, «0.509170…»)** — aceptado: se añade una nota de corrección en `RESPUESTA_RTK001_ronda2_20261003.md` (el valor es 0.5091654…). La cota «> 0.509» del texto era correcta.

### Extensión → **aceptado con matiz**
- **Recortes del árbitro aplicados:**
  1. Prop. 3.12 fusionada en la Prop. 3.8 como (b).
  2. Sonda de acortamiento retirada del texto y de la tabla (queda una mención en Next steps (3) y en `results/`).
  3. Filas de la tabla de afirmaciones fusionadas (Lemas 3.1–3.3; hebras distintas y misma hebra).
  4. Obs. 3.24 (tasa de crecimiento) reducida a la consecuencia más un ejemplo.
  5. Apéndice A reducido al protocolo, con el resto remitido al README.
- **Recortes propios:** Figura 1 retirada (sus datos están en la Tabla 2 y la figura queda en `figures/fig_rop.pdf`); resumen más compacto; historia de versiones en una frase; pie de la Tabla 2 abreviado; bibliografía en `\footnotesize`; tabla de afirmaciones en `longtable`, para que no deje media página en blanco.
- **Resultado: 13 páginas** (v0.3: 12).
- **Por qué no baja de 12:** el bloque (H_3) (≈ 1.1 páginas, con cuatro demostraciones) y las precisiones de M1, m7 y m10 suman más que los recortes. Bajar de 12 exigiría quitar demostraciones (la del bloque (H_3) o la del Paso 4) o la Tabla 2. Se deja así y se declara.

### Nota sin acción obligatoria del árbitro ((H_3) normalizada)
Coincide con la forma adoptada en el bloque integrado: ν = sup|v'|/v² y μ = sup|Π_⊥dκ/dσ| son invariantes por la reparametrización t ↦ t/p. Medidas en los polígonos, crecen despacio (ν: 0.42 → 1.35; μ: 4.5 → 6.9, de d = 1 a d = 4). El término dominante de la curvatura pasa a ser εG/(1 − ε), con ε = r_dκ_max(K_{d−1}) → 0, en lugar de f/(1 − f).

## 3. Verificación de la ronda 2 (tabla del árbitro)
19 de 20 puntos bien aplicados. El 20.º (m13, extensión) se atiende arriba, «con matiz».

## 4. Números que cambiaron
- **Ningún resultado de los experimentos de referencia.** `results.json`, `classify_pairs.json`, `corollary_chain.json` y los dos `*_summary.json` congelados no se tocaron.
- **Redondeos:**
  - Θ*: 1.12 → 1.112;
  - δ_turn (Tabla 1, f = 0.35, d = 1): 1.344 → 1.343;
  - g(√2): «= 1.0887» (tipeado a mano) → «< 1.0887» (macro).
- **Nuevos:**
  - márgenes por normalización (d = 2: 1.37–21.3 %; d = 3: 0.23–13.0 %);
  - constantes del bloque (H_3): 0.8961, 0.0336, 0.0504, 0.685, 4.44;
  - valores de malla de la Obs. 3.18: ν, μ; lado izquierdo de (12) ≤ 0.48 y ≤ 0.15; r_d·cota ≤ 0.72, 0.22 y 0.11; cociente cota/medido ≥ 1.01; r_d sin χ_d = 0.057, 0.0063 y 0.00086; lado izquierdo para d = 2 = 1.95, frente a < 0.685.
- **Corrección respecto de `theory/`:** umbral de μ 0.0505 → 0.0504 (§1.3).

## 5. Cómputo
| Tarea | CPU |
|---|---|
| `check_H3.py` (copia en el scratchpad y copia congelada en `experiments/`) | ≈ 15 s |
| `verify_H3.py` (propio) | 2 s |
| `phase_margin.py`: tres corridas, la última es la válida | 96 + 128 + 142 s |
| `make_numbers.py` y compilaciones | ≈ 1 min |
| **Total** | **≈ 7.5 min** (presupuesto: 10) |

## 6. Compilación
- `latexmk`: 0 errores, 0 referencias o citas indefinidas, 0 cajas desbordadas.
- `pdftotext main.pdf - | grep -c '??'` = 0.
- **13 páginas** (antes 12).
- Revisadas en imagen las páginas 9 (bloque (H_3), Obs. 3.18 e Hip. 3.19) y 12 (tabla de afirmaciones en `longtable`, Limitaciones). La Tabla 2 va en la página 11, antes del apéndice.

## 7. Lo que queda abierto
1. **(H_3) uniforme en d.** La Prop. 3.17 muestra que μ no se propaga: hace falta controlar toda la jerarquía de derivadas, por ejemplo por analiticidad en una banda compleja. Sin eso, (H_c) con c = ½ queda demostrada solo en d = 1, y para d ≥ 3 reducida a la condición de crecimiento (12), que los polígonos cumplen en d = 3 y 4.
2. **d = 2.** Las constantes a priori no bastan (1.95 frente a < 0.685). K₁ es un polinomio trigonométrico explícito, así que la forma fina de (11) en d = 2 es un cálculo finito certificable por intervalos.
   - Evaluación propia en malla, no certificada y solo en el scratchpad (no está en el manuscrito): r₂·cota = 1.146 < 2 con el mayor r₂ admisible en f = ½.
3. **Certificación por intervalos** de c₁, c₀′, κ̂_d, del grosor poligonal y del writhe exacto.
4. **Conjetura 3.23**, ahora con dependencia de la normalización: en d = 3 hay un margen de solo 0.23 % para alguna normalización; queda pendiente un barrido 2-D (β₂, β₃).
5. **Otros:** p ≥ 3; Cr(K₂) exacto (pendientes 9 y 11, fuera del Cor. 1.2 de Kalfagianni–McConkey); extensión de 13 páginas.
