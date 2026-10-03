[EN CURSO]

# Informe de árbitro interno independiente — RTK001, ronda 5 (v0.5, commit 0cec694)

Árbitro: independiente de las rondas 1–4 y del integrador. Objeto principal: la Proposición 3.19 (`prop:d2cert`, `main.tex:335–348`) y la Observación 3.20 (`rem:d2method`, `:350–352`), una prueba asistida por computador del caso d = 2. Después reviso la respuesta a la ronda 4.

Trabajo auxiliar: `/tmp/claude-0/-home-user-ChanoSilva/6d28bda3-759e-5faa-92d7-8739680d15c2/scratchpad/referee5_RTK001/` (scripts `indep_iv.py`, `indep_cover.py`, `dense_check.py`, `chain_check.py`, `kmin.py`, y sus salidas).

## 1. Prueba asistida por computador del caso d = 2 (Prop. 3.19, Obs. 3.20)

**Conclusión:** la prueba es correcta. La cadena lógica se sostiene paso a paso. El código de intervalos encierra lo que dice encerrar: no encontré ninguna operación sin ensanchar ni ningún encierro inválido. Mi verificación independiente (solo `mpmath.iv`, sin código del autor) certifica r₂κ_max(K₂) ≤ 1.477 < 2 en todo el rango, con una malla 16 veces más gruesa en r₁. En la peor caja r₁ ∈ [0.4990, 0.5] obtengo, con la misma malla en s, 1.1881 frente a 1.1862 del autor. Los defectos que encontré son de redacción y de un "bono" no usado (m1–m4). Ninguno afecta al resultado.

### 1.1 Cadena lógica

| Paso | Veredicto | Comprobación |
|---|---|---|
| Fórmula de K₁ | correcta | Con N₀ = e_z (la proyección de e_z en el plano normal del círculo en (1,0,0)), B₀ = T×N₀ = (cos t, sin t, 0) y holonomía 0, K₁(t) = K₀(t)(1 + r₁ sin θ) + r₁ cos θ e_z. Con t = 2s y θ = 3s sale `main.tex:345`. |
| Prop. 3.15 aplicable con r₂ ≤ r₁/2 | correcta, con una omisión de redacción (m2) | La prueba de (`eq:kaprec`) (`:308`, junto con la de la Prop. 3.8, `:214–217`) usa solo \|x\| ≤ ε, \|κ\| ≤ κ_max, \|κ_W\| ≤ κ_max, \|v'\| ≤ νv², \|κ'_par\| ≤ μv, v ≥ v_min y 1 − ε > 0. No usa τ ni f = r/τ ≤ ½. Esto importa porque, con r₂ = r₁/2, f₂ = r₂/thick(K₁) llega a ≈ 0.6 en r₁ = ½ (thick(K₁) ≈ 0.416). Rehíce la identidad \|K_d'×K_d''\|² = b_U²(A+B) + (c_W a − c_T b_W)², la expresión c_W a − c_T b_W = rm a₀ − κ_W v(A+2B), el reparto de Minkowski, A(A+B) ≤ (A+2B)² y la monotonía en A. Todo correcto. La condición ε < 1 la comprueba el código (`certify_d2.py:230`): ε ≤ 0.355 en la peor caja. |
| Monotonía de Φ | correcta | ε = r₂κ_max y λ = r₂m/v_min crecen con κ_max, r₂ y m, y λ decrece con v_min. ζ' = v_min(1−ε)/(r₂m) decrece con κ_max, r₂ y m, y crece con v_min. G(ζ) = sup_{z≥ζ} g es no creciente por definición, y 1/(1+ζ'²) también decrece con ζ'. r₂·κ_max G/(1−ε), 1/(1+ζ'²) y r₂λ(ν(1+ε)+r₂μ)/(1−ε)³ son crecientes en κ_max, ν, μ, r₂ y m, y decrecientes en v_min. La derivada en m del término intermedio original rm²/(v²(1−x)²+r²m²) es positiva, así que sustituir m por su cota superior es válido también antes de acotar. |
| α ∈ (−π, π] | convención, no teorema | `main.tex:77` elige el representante en (−π, π] y el cierre ω = −αt/2π lo usa. Entonces m = 3/2 − α/2π ∈ [1, 2). La holonomía no depende del punto base: la monodromía del transporte paralelo es una rotación del plano normal, y su ángulo es invariante por conjugación. Mi integración del marco (doble reflexión, n = 4096) da α₂ = −3.0270 en r₁ = ½ (m₂ = 1.982) y α₂ = +3.137 en r₁ = 0.49 (m₂ = 1.0007). Es decir, α₂ cruza π cerca de r₁ ≈ 0.49 (el mismo cruce del writhe por 3.5 de `main.tex:408`, r* = 0.4904), y ahí m₂ salta de ≈1 a ≈2. La cota m ≤ 2 cubre ambos lados. |
| Simetría K₁(s+2π/3) = R_z(4π/3)K₁(s) | exacta | e^{2i(s+2π/3)} = e^{4πi/3}e^{2is}, y sin 3s, cos 3s tienen periodo 2π/3. v, κ, \|v'\|/v² y \|Π_⊥dκ/dσ\| son invariantes por rotaciones y por traslación del parámetro. Mi cálculo con el periodo completo (6144 cajas, sin simetría) da en la peor caja Φ ≤ 1.1992, frente a 1.1909 en el tercio con mi misma fórmula. Los valores difieren porque la extensión natural no es invariante por rotación (efecto envoltura), pero ambos son válidos. |
| Fases y normales arbitrarias | cubiertas | K₁^φ(s) = (e^{2is}(1 + r sin(3s+φ)), r cos(3s+φ)) = R_z(−2φ/3)K₁⁰(s+φ/3). Lo verifiqué a mano: la sustitución s' = s+φ/3 da e^{2i(s'−φ/3)}. Rotar N₀(0) un ángulo ϑ equivale a sustituir φ₁ por φ₁+ϑ (`:90`). φ₂ y la normal inicial de K₁ solo entran por U(t), que la Prop. 3.15 acota por \|U\| = 1, y m no depende de la normal inicial. |
| Rango de r₂ | correcto | El enunciado certifica r₂ ≤ r₁/2. La consecuencia para (H_c) exige r₂ ≤ f·thick(K₁) ≤ f·r₁ ≤ r₁/2 (Prop. 3.5, r₁ < 1). El Teorema 3.12(c) en d = 2 necesita f₁, f₂ ≤ ½, y eso es justo lo que pide la frase «Consequently…» de `:340`. |
| Hip. 3.21 y Cor. 3.22 en d ≤ 2 | correctos | En la cadena del corolario, ρ₁ = γ = f/2, thick(K₁) ≥ ρ₁ (d = 1), r₂ = fρ₁ ≤ f·thick(K₁); la Prop. 3.19 con el Teorema 3.12(c) da thick(K₂) ≥ r₂/2 ≥ ρ₂. La cota de longitud es el Lema 3.3. |
| f_c = 0.484375 | correcto | Con r₁ = f, r₂ ≤ f·thick(K₁) ≤ f², y en la caja [a,b] se usa r₂ = b² (`certify_d2.py:380`), que es válido por la monotonía en r₂. El bucle se detiene en el primer fallo, así que el resultado vale para todo f ≤ f_c. |

### 1.2 Auditoría del código (`experiments/certify_d2.py`, idéntico a `theory/` salvo la ruta de salida; SHA-256 coinciden con `results/FROZEN_THEORY_SHA256.txt`)

Leí el archivo línea por línea.

- **Aritmética (`Iv`, l. 50–108).**
  - `+`, `−`, `×` (los cuatro productos, con min/max exactos), `recip` (que lanza un error si la caja contiene 0), `sq` (con mínimo 0 si la caja contiene 0) y `sqrt` (que recorta por debajo en 0): cada resultado pasa por `np.nextafter` hacia fuera.
  - `neg`, `abs`, `mag`, `np.minimum`/`np.maximum` son exactos.
  - Un ulp basta en redondeo al más cercano, también en el cambio de binada y en el rango subnormal.
  - No hay `np.sum`, `np.dot`, `np.linalg.norm` ni potencias de numpy dentro de la aritmética: `vdot`, `vcross` y `vnorm2` usan el `+` de `Iv`.
  - Las constantes (`5**j`, `2**j`, `3**j`, `0.5`, `3.0`, `1.0`, `2.0`) son exactas.
  - Las cajas en r₁ tienen extremos 0.5·i/512, exactos. `float(b)/2` es exacto.
  - Lo único fuera de `Iv` es `f*rhi` en `certify_point` (l. 259, con f = 0.35 no representable). Solo afecta al bloque (A), que es ilustrativo.
- **Trigonometría (l. 145–157).**
  - Los extremos de las cajas en s son encierros `iv` de 2π·j/(3·2048). `iv.cos` e `iv.sin` incluyen los extremos interiores: lo comprobé en `cos([−0.1, 0.1])`, `sin([1.5, 1.6])` y `cos(5·[3.1, 3.2])`.
  - `mp2f` aplica `float()`, que redondea al más cercano, seguido de un ulp hacia fuera. Es válido.
- **Derivadas (l. 166–185).**
  - Comprobé a mano que (2i)^j e^{2is} + (r/2i)[(5i)^j e^{5is} − (−i)^j e^{−is}] da `Wx`, `Wy` y el signo (−1)^j.
  - Comprobé también que (r/2i)W = (rW_y/2, −rW_x/2) y que las derivadas de r cos 3s son −3S₃, −9C₃ y 27S₃.
- **Cantidades (l. 188–207).**
  - κ = \|D₁×D₂\|/v³ y ν = \|D₁·D₂\|/v³ (a través de `mag`).
  - μ = \|Π_⊥D₃ − 3(D₁·D₂)Π_⊥D₂/v²\|/v³. Rederivé que Π_⊥K''' = 3vv'𝛋 + v²Π_⊥𝛋' y que 𝛋'_par = Π_⊥d𝛋/dt.
  - Ninguna división por una caja que contenga 0: v ≥ 1.66 en todas las cajas, y `recip` lo comprobaría.
  - Ninguna raíz de una caja negativa: las sumas de `sq` son ≥ 0, y `sqrt` recorta por debajo.
  - La dependencia solo ensancha.
- **Cota final (l. 223–241).**
  - Las entradas son extremos de caja en flotante, tratados como intervalos puntuales; es correcto por la monotonía.
  - Para G: si ζ'_lo ≤ `SQ2_LO`, se toma g(√2); si no, g(ζ'_lo). `SQ2_LO` es el mayor flotante < √2, así que no hay ningún flotante en (SQ2_LO, √2) y el «caso límite» que menciona la respuesta (§4.4) no puede darse.
  - t₂ = 1/(1+ζ'_lo²) es una cota superior. ζ' ≥ 2.32 en todas las cajas.
- **Cubrimiento.**
  - 512 cajas en r₁ cubren [0, ½], incluida la caja [0, 1/1024]. En ella r₁ = 0 está dentro, pero nada se divide por r₁ (r₂ = b/2 > 0), y la cota vale 0.00049.
  - Las 2048 cajas en s cubren [0, 2π/3] cerrado.
- **Fallos silenciosos.**
  - Un NaN o una caja con ε ≥ 1 dan `total=None` o NaN. En el primer caso falla la comparación (`TypeError`); en el segundo, `all_below_2` es falso y el `assert` de `make_numbers.py:449` lo detecta.
  - No hay forma de que el script pase en silencio con una caja mala.
  - Aun así, recomiendo un `assert np.all(np.isfinite(...))` explícito (m4).
- **Bono no usado.** El «encierro» de α₂ por la torsión total (l. 24–25, 263–278) supone κ(K₁) > 0. Esa hipótesis es **falsa** en r₁ = 4/13 (m1). Además, el encierro en r₁ = ½ cruza −π, así que su «reducción a (−π, π]» carece de sentido para el intervalo. No interviene en la cota y el manuscrito no lo cita.

### 1.3 Verificación independiente (sin código del autor)

1. **Encierro propio con `mpmath.iv` para todo** (`indep_iv.py`, 64 bits).
   - Uso coordenadas reales y la regla de Leibniz; el autor usa exponenciales complejas.
   - Para μ uso una fórmula distinta, sin proyecciones: \|D₁×D₃ − 3(D₁·D₂)/v²·D₁×D₂\|/v⁴. Mi primera elección, la identidad \|𝛋'_par\|² = κ'² + v²κ²τ², explota en r₁ ≈ 0.3076: κ(K₁) se anula allí (véase m1).
   - Resultados por caja, sobre 2048 cajas en [0, 2π/3]:

| caja r₁ | v_min ≥ (yo / autor) | κ_max ≤ | ν ≤ | μ ≤ | Φ ≤ (yo / autor) |
|---|---|---|---|---|---|
| [0.4990234375, 0.5] | 1.80031 / 1.80029 | 1.41990 / 1.41879 | 0.43135 / 0.42965 | 4.5753 / 4.5775 | **1.18806 / 1.18616** |
| [0.4716796875, 0.47265625] | 1.76482 / — | 1.39720 / — | 0.43543 / — | 4.5074 / — | 1.00504 (también ≥ 1 para el autor: r₁,c = 0.47168) |
| [0.2490234375, 0.25] | 1.67573 / 1.67572 | 1.17708 / 1.17673 | 0.34408 / 0.34249 | 2.0637* / 2.0066 | 0.2243 / 0.2240 |
| [0, 1/1024] | 1.99575 / 1.99622 | 1.01086 / 1.00928 | 0.00565 / 0.00500 | 0.0245* / 0.0302 | 0.00049 / 0.00049 |

   *(con la fórmula de la torsión; es válida allí porque κ > 0)*

   - Mi encierro es algo más ancho en κ: la forma real tiene más dependencia. Por eso la constante 1.187 del texto **no** se reproduce con mi implementación a la misma resolución: obtengo 1.1881 en la peor caja.
   - Es una cota superior más débil, no una contradicción. Al imprimir 1.187, el texto depende de la extensión concreta del autor (véase m3).
2. **Cubrimiento propio de todo el rango** (`indep_cover.py`).
   - 32 cajas en r₁ de anchura 1/64 × 512 cajas en s en [0, 2π/3], solo con `mpmath.iv` y con la fórmula de producto vectorial para μ.
   - Resultado: **máx Φ ≤ 1.477 < 2** (peor caja [0.484, 0.5]). No hizo falta subdividir. 45 s de CPU.
   - Esto certifica de forma independiente minRad(K₂) ≥ 0.677 r₂ > r₂/2 para todo r₁ ≤ ½ y r₂ ≤ r₁/2, y con ello la Hip. 3.21 en d = 2.
3. **Evaluación puntual densa contra los encierros del autor** (`dense_check.py`; los encierros del autor se obtienen ejecutando una copia de `experiments/certify_d2.py` en mi scratchpad, solo como datos).
   - (a) 512 cajas r₁ × 5 valores de r₁ (extremos y 3 aleatorios, semilla 12345) × 24 000 valores de s en [0, 2π), con mis fórmulas en flotante: **0 valores fuera**. Holguras mínimas: v 2.0·10⁻⁴, κ 7.9·10⁻³, ν 3.5·10⁻³, μ 5.8·10⁻³.
   - (b) En la peor caja r₁, 512 cajas s × 5 puntos evaluados en `mpmath` con 40 dígitos contra los encierros caja a caja (v, κ, \|ν\|): **0 violaciones** en 7680 pruebas; holgura mínima 1.1·10⁻³.
   - (c) Los máximos en r₁ = ½, refinados en `mpmath` con 40 dígitos (μ por diferencias centradas del vector curvatura, una tercera vía): κ_max = 1.398315, ν = 0.418194, μ = 4.544379, v_min = 1.802776. Coinciden con los valores flotantes del autor (`certify_d2_output.txt`).
4. **Prueba de extremo a extremo** (`chain_check.py`; no es una prueba).
   - Construí K₂ con un marco de Bishop calculado por doble reflexión, cerrado con el giro lineal, y su curvatura espectral.
   - Rejilla: r₁ ∈ {0.1, 0.25, 4/13, 0.35, 0.4, 0.45, 0.48, 0.5}, φ₁ ∈ {0, 0.7, 2.3}, 7 valores de φ₂, r₂ = r₁/2.
   - Resultado: máx r₂κ_max(K₂) = **0.457**, en r₁ = 0.48 (α₂ ≈ 3.02, m₂ ≈ 1.02); con 24 fases, 0.476 en r₁ = 0.49. Muy por debajo de 1.187.
   - Con φ₂ = 0 y r₁ = ½ reproduzco el 0.39994 de `verify_H3.json`; el máximo sobre las fases es 0.414.
   - El máximo sobre el rango no está en r₁ = ½, sino junto al salto de m₂ en r₁ ≈ 0.49.
5. **Reproducción.** `certify_d2.py`, ejecutado en una copia: salida idéntica a `results/certify_d2_output.txt` salvo los tiempos (7.7 s de CPU).

### 1.4 Honestidad de la base de confianza

- La etiqueta «computer-assisted proof (interval arithmetic); not yet checked by an independent referee» aparece en el enunciado (`:335`), en la tabla de afirmaciones (`:425`) y en la Limitación (1) (`:439`). La FICHA (l. 13) y la CONTINUIDAD (l. 41, 189, 193) dicen lo mismo.
- El README no lo dice (l. 39: «el caso d = 2 queda demostrado por computador», sin salvedad; m5).
- La Obs. 3.20 declara bien la base de confianza: binary64 de NumPy, `mpmath.iv` y el código. Faltan dos supuestos: modo de redondeo al más cercano sin *flush-to-zero*, y la conversión `float()` de `mpf` (m4).
- «about one hundred lines of code» es razonable: el núcleo son unas 150 líneas.
- Tras esta ronda, la etiqueta debe pasar a «computer-assisted proof (interval arithmetic); checked by an independent internal referee (round 5)».

