# Informe de árbitro independiente: RTK001, ronda 3 (verificación de los teoremas nuevos)

Fecha: 03/10/2026. Árbitro nuevo e independiente: no participé en las rondas 1 y 2.
Objeto: manuscrito v0.3 (`manuscript/main.tex`, commit e7a21ab, 12 pp.). Teoremas nuevos: Lema 3.9, Prop. 3.10, Cor. 3.11, Prop. 3.12 y Teorema 3.13. También reviso la respuesta a la ronda 2 (`RESPUESTA_RTK001_ronda2_20261003.md`).
Trabajo auxiliar: `/tmp/claude-0/-home-user-ChanoSilva/6d28bda3-759e-5faa-92d7-8739680d15c2/scratchpad/referee3_RTK001/`, con los scripts `closed_forms.py`, `indep_check.py`, `turning.py` y `phase_len.py`, sus registros y una compilación en `build/`.

## Veredicto

**Cambios menores.** Los cinco enunciados nuevos son correctos tal como están escritos. Rehíce cada paso a mano y recalculé con 30 dígitos todas las constantes analíticas. Un detector propio de pares doblemente críticos, independiente del código del autor, confirma el censo reconciliado. Queda un problema de definición: la familia «por defecto» no está unívocamente fijada en el texto (M1), y hay varios deslices de redondeo, de precisión y de notación.

Recuento: 0 bloqueantes, 1 mayor, 10 menores. Ronda 2: 19 de 20 puntos bien aplicados, 1 a medias (extensión), 0 sin aplicar.

---

## 1. Verificación de los teoremas nuevos (prioridad máxima)

### Lema 3.9 (exclusión por giro), l. 217–222: correcto
- Como a, b ∈ [0, π] y a + b < π, se tiene |a − b|/2 ≤ (a + b)/2 < π/2. Por tanto cos a + cos b = 2 cos((a+b)/2) cos((a−b)/2) > 0. Integrando, (X₂ − X₁)·(T₁ + T₂) > 0, lo que es incompatible con (X₂ − X₁)·T_i = 0. Comprobado.
- La versión con giro total se sigue de a(σ) ≤ ∫₀^σ|T'| y b(σ) ≤ ∫_σ^ℓ|T'|. Exige que T_γ sea absolutamente continua (C^{1,1}), no solo C¹ (menor m6). Para K_d, que es C^∞, no tiene consecuencias.

### Prop. 3.10 (misma hebra, p = 2, f ≤ ½), l. 224–245: correcta
- **Descomposición.** Rederivé K_d' = v(1−x)T + rmW con U' = mW − vκ_⊥T, W' = −mU − vκ_W T y T' = v(κ_⊥U + κ_W W), donde U = cos ψ N₀ + sin ψ B₀ y W = T × U. De ahí tan χ = rm/(v(1−x)) con |x| = r|κ_⊥| ≤ f. Además χ_lo = arctan(rm/(v_max(1+f))) y χ_hi = arctan(1/ζ_min), con 1/ζ_min = rm/((1−f)v_min). Correcto.
- **Ruta R2 (sin (H₃)).** Las cuentas se verifican:
  - Y_i' = (vκ_⊥cos χ_i − m sin χ_i)U + vκ_W cos χ_i W − vκ_W sin χ_i T.
  - |Y_i'|² = (vκ_⊥cos χ_i − m sin χ_i)² + v²κ_W².
  - La cota |Y_i'|² ≤ (vκ + m sin χ_i)² se obtiene desarrollando y usando κ_⊥²cos²χ_i + κ_W² ≤ κ², −κ_⊥cos χ_i ≤ κ y m sin χ_i ≥ 0.
  - La desigualdad triangular esférica da a(t) ≤ |χ(t) − χ₁| + ∫|Y₁'|.
  - Al sumar: ∫vκ ≤ σ/τ = δ, m[(t−t₁)sin χ₁ + (t₂−t)sin χ₂] ≤ u sin χ_hi y u ≤ δ/Θ_min.
  - La fórmula de δ_R2 es exacta. Con k = 0, el arco de K_d sobre el arco base más corto une X₁ con X₂, porque t₂ − t₁ − s ∈ 2πpℤ.
- **Ruta R1 (con (H₃)).** Se cumple ω = |K_d'×K_d''|/|K_d'|² ≤ vκ(A+2B)/(A+B) + rm²/√(A+B) + rm|a₀|/(A+B), con B/(A+B) = sin²χ y rm/√(A+B) = sin χ. Dividiendo por v y usando |a₀| ≤ M_v(1+f) + rvM_κ y A+B ≥ v_min²(1−f)² + r²m², se obtiene la fórmula de τΩ̄. Correcto.
- **Distancia.** El Paso 3 del Lema 3.7 no usa el índice de hebra: A ≥ ℓ − 2rE/ℓ ≥ Λ y |X₂−X₁| ≥ ℓ₀ − 2r.
  - En [π/3, π/2] se tiene Λ = 2(τ−r)sin(δ/2) ≥ τ − r ≥ r.
  - En [π/2, π) se aplica el Paso 4 con φ(ς) = 4ς² − ς − 1 + π/2 − 2 arcsin ς ≥ 0, más la monotonía de Λ/r en f.
  - Mínimo propio de Λ/r en [π/3, π) a f = ½: exactamente 1, alcanzado en δ = π/3. La cota es justa y el texto ya lo dice.
  - Conclusión: c₀′ ≥ ½ si δ_turn ≥ π/3. Correcto.

### Cor. 3.11 (familia (2,3), toda profundidad), l. 247–254: correcto

**d = 1.** Base circular: v ≡ 1, κ ≡ 1, α = 0, m = 3/2, Θ = 2/3, M_v = M_κ = 0. Con f = ½ y ζ = 2/3, recalculado con mpmath a 30 dígitos:

| Cantidad | Valor exacto | Cota del texto |
|---|---|---|
| τΩ̄ = 1 + 9/13 + 9/(2√13) | 2.940383 | < 2.9404 |
| δ_R1 | 1.0684297 | > 1.0684 (margen 3·10⁻⁵) |
| sin(δ_R1/2) | 0.5091654 | > 0.509 |
| c* | 1.0183309 | — |
| φ_{c*}(1/√2) | 0.279931 | > 0.279 |
| φ_{c*}(1) | 0.410873 | > 0.410 |
| φ′_{c*}(1/√2) = 2√2 − c* | 1.810096 | > 1.81 |
| φ_{c*} en malla de 2001 puntos (mínimo) | 0.27993, en el extremo | coherente con el argumento de concavidad |

- En d = 1, R2 solo da δ_R2 = 0.93560 < π/3, así que **R1 es imprescindible en d = 1**. La prueba lo usa correctamente: (H₃) se cumple trivialmente.
- Errata menor de la RESPUESTA (§1): dice «0.509170…»; el valor es 0.5091654. La cota «> 0.509» del texto es correcta.

**d ≥ 2: cota a priori Θ_min ≥ √13·2^{d−3}.** Comprobada paso a paso:
- (i) |K₁'|² = (1−x)² + r₁²m₁² con x ∈ [−f, f]. El factor 2 viene de la reparametrización t ↦ t/p. Por tanto v_min(K₁) ≥ 2√((1−f)² + 9f²/4). Medido: 1.802776 en f = ½ y 1.67108 en f = 0.35. **La cota se alcanza con igualdad** (ecuador interior).
- (ii) Grosor(K₁) ≤ r₁ = f₁ por la Prop. 3.5. Medido: τ₁ = 0.41582 ≤ 0.5.
- (iii) Para f ≤ ½, (1−f)/f ≥ 1, luego v_min/grosor ≥ 2√(1 + 9/4) = √13. Para j ≥ 2, v_min(K_j) ≥ 2(1−f_j)v_min(K_{j−1}) y grosor(K_j) ≤ f_j·grosor(K_{j−1}), de modo que el cociente al menos se duplica.
- (iv) m_d = 3/2 − α/2π ∈ [1, 2). Medido: m₂ = 1.982 en f = ½, **casi la cota**.
- (v) ζ_min/Θ_min = (1−f)/f ≥ 1.
- Θ_min medido: 2.188 en d = 2 (cota 1.803) y 9.598 en d = 3 (cota 3.606). La cota a priori es bastante ajustada: la única holgura está en τ₁ ≤ r₁.
- δ_R2^ap(√13/2) = 1.6773739 > 1.677. Es creciente en Θ y en ζ, y quitar χ_lo ≥ 0 solo empeora la cota. Correcto.
- Desliz: «needs Θ_min ≥ 1.12» (m1). El umbral exacto es 1.112080.

### Prop. 3.12 (κ̂_d con ψ conservado), l. 256–264: correcta
- Rederivé la identidad |K_d'×K_d''|² = b_U²(A+B) + (c_W a − c_T b_W)² en la base directa (T, U, W). Para ello: c_T' = v'(1−x) − rv(κ₁'cos ψ + κ₂'sin ψ) − rvmκ_W, de donde a = a₀ − 2rvmκ_W, y c_W a − c_T b_W = rma₀ − κ_W v(A + 2B).
- Para (x, v) fijos, la expresión es monótona en |a₀| ≤ M_v(1−x) + rvM_κ y en |κ_W| ≤ √(τ⁻² − x²/r²). El supremo en (x, v) es una cota válida punto a punto.

### Teorema 3.13, l. 266–271: correcto
- (a) La lista de casos es completa:
  - mismo punto base: 2r;
  - δ ≥ π: 2(τ−r), por el Paso 1 y la Prop. 3.6(b);
  - δ < π con k = 1: Lema 3.7;
  - δ < π con k = 0: Prop. 3.10.
  - Como c₁ ≤ 1 (su límite cuando δ → 0 es 1), el par antipodal no rompe el mínimo.
- (b) Es la Prop. 3.12.
- (c) Usa c₁ ≥ ½ (Paso 4 y monotonía, con Θ_min ≥ 2/3 a priori por el Paso 5), c₀′ ≥ ½ (Cor. 3.11) y τ − r ≥ r.
- En d = 1, rκ̄₁ = fG(ζ)/(1−f) + 1/(1+ζ²) es creciente en f y vale g(√2) + 9/13 en f = ½. Por tanto 1/(rκ̄₁) = 0.5614918 > 0.561. Valores en f = 0.35 y 0.25: 1.019357 y 1.792851, iguales a los del autor.
- La equivalencia «para d ≥ 2, (H_c) con c = ½ ⟺ minRad(K_d) ≥ r_d/2» se sigue de grosor = min(minRad, ½dcsd) y de ½dcsd ≥ r/2. Está en el párrafo de estado (l. 301), no en el enunciado: sugerencia en m10.

### ¿Lo marcado «proved» depende de constantes de malla? No.
- Todo lo etiquetado como demostrado se apoya en desigualdades en forma cerrada que recalculé: Paso 4, δ_R1, δ_R2^ap, √13/2, sin(δ_R1/2), φ_{c*} y κ̄₁.
- Los valores de malla están etiquetados como tales: 0.6117, la Tabla 1, 1.034 y 0.998.
- «0.74» (macro `\SsCzeroAp`): no se usa en el manuscrito. El valor es correcto (0.743630 = ½·inf_{δ ≥ 1.6774} max(Λ, ℓ₀ − 2r) en f = ½). Ver m9 sobre su descripción en `theory/`.
- La tabla de afirmaciones (l. 360–378), el resumen, el README, la FICHA y la CONTINUIDAD etiquetan bien cada resultado. Hay una sola subestimación, en Limitaciones (4) (m5).

### Correspondencia con `theory/`
No hay apéndice de demostraciones: las pruebas están en el cuerpo. Los enunciados del cuerpo coinciden con `theory/same_strand_lemma.tex`. La única diferencia es que «c₀′ ≥ 0.74 para d ≥ 2» se omitió deliberadamente, y la omisión es correcta.

---

## 2. Verificación de la ronda anterior

| Id (ronda 2) | Estado | Evidencia |
|---|---|---|
| B2 de r1 (doble listado (3,2), d = 2) | aplicado bien | `numbers.tex:275` `\HypEqOneListOther` = «(3,2), d=3; (2,5), d=2,3»; tolerancia única `make_numbers.py:163–189` (`EQ_TOL = 5e-4`, aserción contra la variación de τ) |
| M2 de r1 → M2 de r2 | aplicado bien | véase M2 |
| M1 (constantes de malla presentadas como demostradas) | aplicado bien | `main.tex:55` (resumen sin 0.6117 ni 1.223 r), 181 (texto propuesto), 190 («grid infimum … not a certified bound»), 266 (estado del Teorema), 294/301 (Hip.), 365–371 (tabla), 384 (Limitaciones (4)); README «Demostrado (analítico) / Evaluado en malla»; CONTINUIDAD:41; FICHA. Residuo: m5 |
| M2 (conjetura tautológica) | aplicado bien | `main.tex:325` (umbrales f_*(d), «other than the antipodal pairs»), 338 (márgenes por macro 1.4/2.1 % y 1.4/2.0 % a N₀ = 512), 376. Reproduzco 1.37 % (d = 2) y 2.0 % (d = 3) con curvas lisas. Pero los márgenes dependen de la convención de marco no declarada (M1) |
| M3 (lo abierto, desfasado) | aplicado bien | `main.tex:338` (censo reconciliado), 384 (1), 386 Next steps (1). Censo confirmado de forma independiente (§4). Residuo de precisión: m3 |
| M4 (dependencia de `theory/`) | aplicado bien | `sha256sum -c results/FROZEN_THEORY_SHA256.txt`: 10/10 OK; `diff` entre `theory/` y `experiments/` solo en rutas; `need()` en `make_numbers.py`. Relancé `check_same_strand.py` en una copia: summary con SHA-256 4797be4e…eefd, idéntico byte a byte |
| m1 (Paso 4) | aplicado bien | `main.tex:190`. Valores verificados: 0.5484, 0.8362, 0.3656 y 0.8169 (0.8169² = 0.6673 > 0.667); suma > 1.016 |
| m2 (citas del Teorema) | aplicado bien | `main.tex:270` |
| m3 (tolerancia) | aplicado bien | `make_numbers.py:163–206`; `\EqTolPct` = 0.05 |
| m4 (precisión del resumen) | aplicado bien | `main.tex:55` |
| m5 (choques K₁ y c₀) | aplicado bien | M_v, M_κ (l. 196); c_BS (l. 321). Quedan otros choques: m4 |
| m6 (cuantificador y cadena del Corolario) | aplicado bien | `main.tex:295`, 317 (38.4 / 256.5 / 2051.9; margen ≥ 1.66) |
| m7 (Limitaciones) | aplicado bien | `main.tex:384` |
| m8 (Kalfagianni–McConkey, Lackenby) | aplicado bien (matiz correcto) | `main.tex:321`; FICHA «acotado o determinado en profundidad 2». Cita verificada (véase Bibliografía) |
| m9 (CONTINUIDAD bibliografía) | aplicado bien | CONTINUIDAD:47, lista única |
| m10 (páginas en RESPUESTA r1) | aplicado bien | RESPUESTA r1:79, 93 |
| m11 (README y CONTINUIDAD heredaban M1) | aplicado bien | README §Resultados; CONTINUIDAD:41, 76 |
| m12 (constantes a tabla) | aplicado bien | Tabla 1, `main.tex:275–286`. Revisada contra `results/check_same_strand_summary.json`. Excepción de redondeo: m2 |
| m13 (tipo de letra y extensión) | aplicado a medias | 10 pt y 12 páginas (eran 11). Véase «Extensión» |
| Bibliografía (DOIs) | aplicado bien | `refs.bib:60, 71, 82, 122` |

---

## 3. Hallazgos nuevos

### Bloqueantes
Ninguno.

### Mayores

**M1. La familia «por defecto» no está unívocamente definida en el texto. Los números finos de d ≥ 2 dependen de una convención que solo está en el código.**
- *Ubicación:* Def. 2.1 (l. 85–89): «let (N_{d−1}, B_{d−1}) be its closed Bishop frame … φ_d = 0». §2.2 (l. 76) dice que el marco es «unique up to a constant rotation in the normal plane».
- *Problema:* sin fijar N_{d−1}(0), «φ_d = 0» no tiene sentido: rotar N₀(0) un ángulo β equivale a φ_d ↦ φ_d + β. En d = 1 la simetría del círculo lo hace irrelevante; en d ≥ 2 no. La convención real (proyección de e_z sobre el plano normal en t = 0, o de e_x si |T₀·e_z| > 0.9) solo está en `experiments/recursive_knots.py:72–76`.
- *Evidencia:* lo medí con mi construcción lisa (`phase_len.py`, `indep_check.py`, f = ½, cinco normales iniciales β ∈ {0, 0.7, 1.4, 2.1, 2.8}):
  - L(K₂) y L(K₃) no cambian a 10⁻⁵ (L/r = 155.59 y 622.68). Tampoco cambian α ni τ_d = r_d.
  - minRad(K₂)/r₂ varía entre 3.034 y 3.072, y minRad(K₃)/r₃ entre 5.154 y 5.235.
  - **El margen de la Conjetura 3.19 en d = 2 varía entre 1.37 % (β = 0) y 2.28 % (β = 0.7)**, con 1.95 % en β = 2.1.
  - Los teoremas no se ven afectados, porque son uniformes en φ_d. Lo que no se puede reproducir desde el texto son las cifras de la Conjetura 3.19 y de la §4 («1.4 % and 2.1 %»).
- *Corrección:*
  - En la Def. 2.1, añadir: «The closed Bishop frame of K_{d−1} is normalised by N_{d−1}(0) = the unit projection of e_z onto the normal plane at K_{d−1}(0) (of e_x if |T(0)·e_z| > 0.9); φ_d is measured from it. All results of Section 3 hold for every choice of N_{d−1}(0) and φ_d.»
  - En la §4, tras los márgenes: «L and τ do not depend on this normalisation at the printed precision, but the margins do (1.4–2.3 % at d = 2 over five initial normals), so f_*(2) ≥ 1/2 holds for every normalisation tested, by at least 1.4 %.»

### Menores

- **m1. Cor. 3.11, l. 253: «δ_R2 ≥ π/3 needs Θ_min ≥ \SsThetaStar = 1.12».**
  - Como condición necesaria es falsa: el umbral es Θ* = 1.112080 (bisección propia con mpmath; la RESPUESTA da 1.11208). Θ_min = 1.115 ya basta.
  - Causa: `make_numbers.py:363` usa `ceil_fmt(hi_, 2)`.
  - Corrección: `mac("SsThetaStar", floor_fmt(hi_, 3))` y texto «needs Θ_min ≥ 1.112». O mantener la redondez con «needs Θ_min > 1.11».

- **m2. Tabla 1, columna δ_turn.** El pie dice «rounded down», pero `make_numbers.py:324` usa `f"{lv['delta_turn']:.3f}"`, que redondea al más cercano.
  - Ejemplo: (f = 0.35, d = 1) vale 1.34399 en `check_same_strand_summary.json` y se imprime «1.344», por encima del valor.
  - Corrección: `mac("SsDturn" + k, floor_fmt(lv["delta_turn"], 3))`.

- **m3. El censo de «misma hebra» necesita el calificador δ < π.**
  - *Ubicación:* `main.tex:338` («no doubly critical vertex pair on the same strand with distinct base points occurs»), README §«Pares críticos» y CONTINUIDAD:97.
  - *Problema:* la l. 165 define el índice k para cualquier par, también los lejanos. Con esa definición sí hay pares de misma hebra que son mínimos locales en d = 2 y 3. Mi censo da 34 y 144 raíces con k = 0 y δ ≥ π en f = ½. **El par no-disco más cercano en d = 2 es k = 0, δ = 13.27, mínimo local.** El script del autor solo asigna hebra si el arco es < πτ (`results/classify_pairs.md`, cabecera), así que el dato es correcto pero el texto no lo dice.
  - *Corrección:* «…no doubly critical vertex pair on the same strand with base arc < πτ and distinct base points occurs…». Lo mismo en el README.

- **m4. Choques de notación en el bloque nuevo.**
  - ω designa el giro de cierre (l. 76–80) y la tasa de giro de T_d (l. 242).
  - x designa el punto base K(0) (Lema 3.7) y rκ_⊥ (Props. 3.8, 3.10, 3.12).
  - A tiene tres significados: componente de X₂ − X₁ (Paso 3), v²(1−x)² (Prop. 3.8) y p(1+f) + f(q + p/2) (Cor. 3.16).
  - Λ designa Λ(δ) (l. 167) y A/γ (Cor. 3.16).
  - s designa la cuerda 2r sin(π/p) (l. 149) y la diferencia de parámetro base (l. 165).
  - Corrección: renombrar la tasa de giro ϖ, el punto base x₀, A del Corolario 𝒜, Λ del Corolario Λ_Rop y la cuerda s_p.

- **m5. Limitaciones (4), l. 384:** «Only the thresholds c₁ ≥ ½, c₀′ ≥ ½ and 1/(rκ̄₁) > 0.561 are analytic; every other constant … is a grid infimum». Subestima lo demostrado: δ_R1 > 1.0684, δ_R2 > 1.677, Θ_min ≥ √13·2^{d−3} y c₀′ > 0.509 son formas cerradas.
  - Corrección: «Only the thresholds …, and the closed forms of Corollary 3.11, are analytic; …».

- **m6. Lema 3.9, l. 218:** «Let γ be a C¹ arc … This holds whenever the total turning ∫|T_γ'| is < π». Para la segunda frase hace falta que T_γ sea absolutamente continua.
  - Corrección: «…whenever γ is C^{1,1} and its total turning…».

- **m7. Cor. 3.11, prueba en d = 1 (l. 251): ambigüedad en c*.**
  - Si c* = 2 sin(δ_R1(f)/2) se lee con δ_R1 dependiente de f, el argumento φ_{c*} falla para f pequeño. En f = 0.25, δ_R1 = 1.679 > π/2, c* = 1.489 > √2 y φ_{c*}(1/√2) = −0.053.
  - La prueba es correcta si se hace en f = ½ y se transfiere por monotonía, que es lo que dice la última frase.
  - Corrección: «We argue at f = ½, with c* := 2 sin(δ_R1(½)/2); for f < ½ the interval [δ_turn, π) shrinks and Λ/r increases, so c₀′(f) ≥ c₀′(½) > 0.509.» Cambiar también «(larger for smaller f)» por «(and c₀′ > 0.509 for every f ≤ ½)».

- **m8. Obs. 3.18 (Kalfagianni–McConkey).** La cita es exacta, pero conviene decir que su Cor. 1.2 (c(K_{p,2}) = 4c + 1) solo cubre las pendientes p = 2wr ± 1, es decir ±5 o ±7 para el trébol. Las pendientes 9 y 11 de K₂ no son de esa forma, así que la Cor. 1.2 no da Cr(K₂).
  - Corrección: añadir «(their Corollary 1.2 treats the slopes 2wr ± 1; the slopes 9 and 11 of K₂ are not of this form)».
  - Si se coteja la convención, el valor saldría del caso adecuado del mismo artículo. Mi conjetura, no verificada: 4·3 + |pendiente − 2wr|.

- **m9. `\SsCzeroAp` (0.74) está definida y no se usa.** `theory/same_strand_lemma.tex:107` la describe como «½r⁻¹ inf_{δ ≥ 1.677} Λ». En realidad es el ínfimo de max(Λ, ℓ₀ − 2r): 0.74363, frente a 0.71478 con Λ solo.
  - Corrección: borrar la macro de `make_numbers.py:353`, o comentarla como «max(Λ, ℓ₀−2r)». (El archivo de `theory/` no es mío y no lo toco.)

- **m10. Teorema 3.13 (c).** La equivalencia «para d ≥ 2, (H_c) con c = ½ en el nivel d ⟺ minRad(K_d) ≥ r_d/2», que el resumen y la FICHA presentan como resultado, solo aparece en el párrafo de estado (l. 301).
  - Corrección: añadirla al enunciado (c): «…; for d ≥ 2, (H_c) with c = ½ holds at level d iff minRad(K_d) ≥ r_d/2.»

**Nota sin acción obligatoria** (útil para lo abierto, (H₃) uniforme en d). Con los insumos medidos por el autor (`check_same_strand_summary.json`), las constantes de (H₃) normalizadas de forma invariante por escala decrecen con d en f = ½:
- M_v·τ/v_max²: 0.090 (base K₁) y 0.042 (base K₂);
- M_κ·τ²/v_max: 0.42 y 0.085.

En cambio, 1/(rκ̂_d) baja de 1.419 a 1.034 y 0.998, mientras que el minRad/r real sube: 1.43, 3.07 y 5.24 en mi construcción lisa. Una (H₃) normalizada (M_v ≤ C v²/τ, M_κ ≤ C v/τ²) parece la forma natural de buscar una recursión, y el término dominante de κ̂ es el geométrico fG/(1−f), no el de a₀.

---

## 4. Verificación computacional

**Formas cerradas** (`closed_forms.py`, mpmath a 30 dígitos, < 1 s). Todo lo listado en §1 está recalculado. Coinciden con el texto todos los valores salvo Θ* (m1). También en f = 0.25, 0.35, 0.5:
- 2√((1−f)²/f² + 9/4) = 6.708, 4.775 y 3.606, siempre ≥ √13.

**Chequeo independiente** (`indep_check.py`; no usa ninguna función del autor).
- *Construcción:* curvas lisas por muestras, con derivadas espectrales (FFT, hasta orden 9). El marco de Bishop se obtiene por RK4 de N' = −(N·T')T, con datos en medios nodos por sobremuestreo espectral; la holonomía se elimina con un giro lineal; normal inicial con la misma convención que el código, para poder comparar.
- *Resolución:* N = 512, 1024 y 4096 en d = 1, 2, 3; cola espectral < 2·10⁻¹⁴.
- *Detector:* ceros comunes de F₁ = (X₂−X₁)·X₁' y F₂ = (X₂−X₁)·X₂', buscados por cambio de signo de G = F/(|X₂−X₁| sin w), con w = u₂ − u₁ − π, en una malla desplazada medio paso.
  - Esta regularización elimina los dos conjuntos degenerados: la diagonal, donde G → −∞ a ambos lados, y la familia antipodal, donde F/sin w es suave.
  - Después, Newton sobre F/sin w con evaluación de Taylor y clasificación por la hessiana de la distancia (mínimo, silla o máximo).
  - El arco base se mide en longitud de arco y k es relativo al arco más corto. r_{d+1} = f·τ_d con mi propio τ_d = min(minRad, ½dcsd).
- *Tiempo:* 7 min 59 s de pared y 7 min 46 s de CPU. **Excede el presupuesto de 5 min**: el Newton en Python sobre 9 170 y 18 349 celdas candidatas en d = 3. La reproducción y las sondas de fase añaden unos 70 s. Total ≈ 9 min de CPU.

| f | d | τ_d/r_d | Θ_min | m | siguiente par no-disco / r | minRad/r | k = 0, δ < π (raíces; tipos; δ mín; dist mín/r) | k = 1, δ < π |
|---|---|---|---|---|---|---|---|---|
| 0.5 | 1 | 0.83164 | 0.6667 | 1.5 | 1.6633 (k = 1, δ = 1.812, mínimo) | 1.430 | 9; silla/máx; 1.9669; 3.7014 | 15; mín 1.663 r |
| 0.5 | 2 | 1.0000 | 2.1877 | 1.982 | 2.0274 (lejano) | 3.072 | 0 | 0 |
| 0.5 | 3 | 1.0000 | 9.598 | 1.511 | 2.0403 (lejano) | 5.235 | 0 | 0 |
| 0.35 | 1 | 1.0000 | 0.6667 | 1.5 | 5.2346 (k = 0, silla) | 2.276 | 9; silla/máx; 2.1483; 5.2346 | 3; mín 7.40 r |
| 0.35 | 2 | 1.0000 | 3.840 | 1.243 | 4.0511 (lejano) | 5.759 | 0 | 0 |
| 0.35 | 3 | 1.0000 | 25.80 | 1.008 | 4.1691 (lejano) | 15.75 | 0 | 0 |

Qué coincidió con el autor:
- τ₁/r₁ = 0.832; el par crítico a 103.7°, k = 1; Θ_min = 2.19 y 9.59; márgenes de 1.4 % y 2.0 % (este último, a N₀ = 512).
- **Censo reconciliado confirmado.** Con el test de mínimo local no hay ningún par de misma hebra con δ < π. Con un detector de todos los ceros (sillas y máximos incluidos) solo los hay en d = 1: δ ≥ 1.967 > δ_turn = 1.068 y distancia ≥ 3.70 r₁ en f = ½; δ ≥ 2.148 y ≥ 5.23 r en f = 0.35. En d = 2 y 3 no hay ninguno.
- Dato adicional: en d = 2, 3 **no hay ningún par doblemente crítico genuino con δ < π**, ni siquiera de hebras distintas.
- Las d = 1 de la tabla anterior proceden de la misma corrida independiente.

**Sondas de borde:**
- *Giro real frente a la cota* (`turning.py`, 1.7 s). En d = 1, f = ½, la tasa de giro máxima por unidad de arco base es 1.639/τ, frente a τΩ̄ = 2.940. El δ mínimo con giro acumulado ≥ π es 1.9635, y el δ mínimo con max(a + b) ≥ π (la cantidad exacta del Lema 3.9) es 1.9696. Ambos coinciden con el primer par de misma hebra (1.967). El mecanismo de exclusión por giro es el que opera; la cota demostrada 1.068 tiene un factor de holgura ≈ 1.84. En d = 2 el giro nunca llega a π en arcos base < 5.85τ.
- *Normal inicial / fase* (β ∈ {0, 0.7, 1.4, 2.1, 2.8}, f = ½, d ≤ 2 con censo y d ≤ 3 con longitudes). El censo es igual y τ₂ = r₂ en todos los casos; los márgenes varían (M1).

**Reproducción del autor.**
- `check_same_strand.py` en una copia del scratchpad: 24 s de pared y 14 s de CPU; summary idéntico byte a byte (SHA-256 4797be4e…eefd).
- `sha256sum -c results/FROZEN_THEORY_SHA256.txt`: 10/10 OK.
- No relancé `check_Hc.py`, `classify_pairs.py` ni la corrida de referencia, para no superar aún más el presupuesto. Sus magnitudes quedan cubiertas por mi chequeo independiente.

**Compilación.** `latexmk` en una copia (`build/`): 0 avisos y 0 indefinidas en `main.log`; `pdftotext | grep -c "??"` = 0; 12 páginas. Texto idéntico al PDF entregado. Numeración comprobada en `main.aux`: Lema 3.9, Prop. 3.10, Cor. 3.11, Prop. 3.12, Teorema 3.13.

**Números del texto frente a `results/*.json`.** Revisé `\Ss*`, `\Hc*`, `\Cls*`, `\Margin*` y `\KbarOneHalf` contra `check_same_strand_summary.json`, `check_Hc_summary.json`, `classify_pairs.md` y mis valores. Todos coinciden, salvo los redondeos de m1 y m2.

---

## 5. Bibliografía

| Entrada | Estado | Corrección |
|---|---|---|
| KalfagianniMcConkey2024 | verificada (WebSearch: Bull. LMS 56(11), 3400–3411, 2024, DOI 10.1112/blms.13140; arXiv:2309.03814). El resumen dice «crossing number of a (p,q)-cable of an adequate knot with crossing number c is larger than q²c» y «determine the crossing number of 2-cables of adequate knots»; Cor. 1.2: c(K_{p,2}) = 4c + 1 si p = 2wr ± 1. El uso en l. 321 es correcto | precisión de m8. arXiv y Wiley están bloqueados por el proxy, así que el texto completo no es accesible |
| Lackenby2014 | verificada (AGT 14(4), 2379–2409, 2014, DOI 10.2140/agt.2014.14.2379; «at least 10⁻¹³ times the crossing number of its companion») | ninguna |
| Lickorish1997 (la única «coherente, no buscada») | verificada (GTM 175, Springer 1997, ISBN 978-0387982540, DOI 10.1007/978-1-4612-0691-0) | añadir el DOI y pasarla a «verificadas» en la CONTINUIDAD |
| Resto (13) | verificadas en rondas anteriores; los DOIs nuevos están presentes | — |

---

## 6. Extensión y presentación

12 páginas a 10 pt, por encima del objetivo de 10. El bloque nuevo (≈ 1.6 pp.) contiene el contenido verificable de la ronda, así que **parte del exceso está justificada**; una página no. Recortes concretos, con ≈ 1 página en total:
1. Fusionar la Prop. 3.12 con la Prop. 3.8 como apartado (b), con la prueba en dos líneas: ≈ 6 líneas.
2. Retirar la sonda de acortamiento (párrafo l. 340 y fila l. 377): resultado negativo, no certificado y de v0.1. Ahorra ≈ 4 líneas.
3. Tabla de afirmaciones: unir las filas l. 360–362 (embebimiento, marco, longitud) y l. 365–366 (hebras distintas y misma hebra): ≈ 4 líneas.
4. Obs. 3.20 (tasa de crecimiento): dejar solo la frase de la consecuencia y remitir los cocientes a `results/tables.md`: ≈ 5 líneas.
5. Apéndice A: dejar el protocolo de construcción y remitir lo demás al README: ≈ 6 líneas.

---

## 7. Lista final de acciones (por prioridad)

1. Fijar en la Def. 2.1 la normalización de N_{d−1}(0) y declarar que los resultados de la §3 son uniformes en ella. En la §4, añadir la dependencia de los márgenes respecto de esa elección (M1).
2. Corregir «needs Θ_min ≥ 1.12» por «≥ 1.112», usando `floor_fmt(·, 3)` para `\SsThetaStar` (m1).
3. Usar `floor_fmt` para `\SsDturn*`, de acuerdo con el pie de la Tabla 1 (m2).
4. Añadir «with base arc < πτ» al censo de misma hebra en la §4, el README y la CONTINUIDAD (m3).
5. Reescribir la prueba de d = 1 del Cor. 3.11 «at f = ½ and by monotonicity», con c* fijo (m7).
6. Añadir a Limitaciones (4) las formas cerradas del Cor. 3.11 como analíticas (m5).
7. Añadir la equivalencia d ≥ 2 al enunciado 3.13(c) (m10).
8. Escribir «C^{1,1}» en la segunda frase del Lema 3.9 (m6).
9. Renombrar ω, x, A, Λ y s donde chocan (m4).
10. Precisar en la Obs. 3.18 que la Cor. 1.2 de Kalfagianni–McConkey no cubre las pendientes 9 y 11 (m8). Añadir el DOI de Lickorish y moverla a verificadas.
11. Borrar o describir bien `\SsCzeroAp` (m9).
12. Aplicar los recortes 1–5 para bajar a 11 páginas.
