# Informe de árbitro interno independiente — RTK001, ronda 5 (v0.5, commit 0cec694)

Árbitro: independiente de las rondas 1–4 y del integrador. Objeto principal: la Proposición 3.19 (`prop:d2cert`, `main.tex:335–348`) y la Observación 3.20 (`rem:d2method`, `:350–352`), una prueba asistida por computador del caso d = 2. Después reviso la respuesta a la ronda 4.

Trabajo auxiliar: `/tmp/claude-0/-home-user-ChanoSilva/6d28bda3-759e-5faa-92d7-8739680d15c2/scratchpad/referee5_RTK001/` (scripts `indep_iv.py`, `indep_cover.py`, `dense_check.py`, `chain_check.py`, `kmin.py`, y sus salidas).

**Veredicto: cambios menores.** La prueba asistida del caso d = 2 (Prop. 3.19) es correcta: la cadena lógica se sostiene, el código de intervalos encierra lo que dice, y una implementación independiente mía (solo `mpmath.iv`) certifica r₂κ_max(K₂) ≤ 1.477 < 2 en todo el rango y 1.1881 en la peor caja. La respuesta a la ronda 4 está bien aplicada. Quedan un problema mayor de presentación (14 páginas) y ocho menores.

Recuento: 0 bloqueantes, 1 mayor, 8 menores. Ronda 4: 9 aplicados bien, 1 a medias (extensión), 1 no aplicado (m5, opcional, justificado).

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

## 2. Verificación de la ronda anterior (ronda 4)

| Hallazgo | Estado | Evidencia |
|---|---|---|
| M1 (alcance de la Prop. 3.17) | aplicado bien | Resumen `main.tex:56` («cannot be bounded by any locally bounded function of the (H₃) data of an arbitrary base … in this sense; in the family μ grows slowly»). Enunciado `:323` («for all smooth bases K»). Obs. 3.18 `:330` («cannot be obtained from the (H₃) data of K_{d−2} alone … or use the explicit structure of the family»; «Proposition 3.17 says nothing about the family itself»). README:39, FICHA:13 y :24, CONTINUIDAD:41 usan la redacción propuesta. Los valores lisos 4.5 → 7.0 salen de `results/smooth_H3.json` (4.544, 5.015, 6.221, 6.972; d = 1 coincide con mi cálculo en mpmath: μ = 4.544379). |
| M2 (márgenes que no son cotas; barrido conjunto) | aplicado bien | La Conj. 3.25 es uniforme en las fases (`:387`). Los márgenes figuran como «polygonal margins ≥ 1.37 % … ≥ 0.233 % …, smooth values being slightly smaller» (`:387`), «grid evaluations on vertex pairs, not bounds, and biased upwards» (`:408`) y en la tabla de afirmaciones (`:433`). El barrido conjunto (`joint_phase_sweep.py`) está integrado y declarado (`:408`). README:47, FICHA:25 y CONTINUIDAD:44 dicen lo mismo. Ya no aparece «at least» con márgenes en ningún archivo (grep). |
| m1 («por separado») | aplicado bien | `main.tex:316`; README:39 («la condición (12), que combina ambos términos…»). |
| m2 (K_{d,η} definida; notación) | aplicado bien | `:326`: «r < thick(K)», «For small η … r < thick(K_η)», más un argumento de semicontinuidad inferior bajo convergencia C² que he comprobado (minRad continuo; pares doblemente críticos a distancia ≤ 2r convergen a uno de K; los que colapsan quedan excluidos por el Lema 3.9). ε → η; β → ϑ en `:90`. |
| m3 (ν, μ en d = 4) | aplicado bien (con el matiz declarado) | `:330`: «d = 4 at N₀ = 128, slightly below the smooth values 1.36, 7.0»; «≤ 0.15 with the smooth data». Las macros salen de `smooth_H3.json` (1.3596 → 1.36, 6.9718 → 7.0, 0.1438 → ⌈0.15⌉). |
| m4 (`verify_H3.py`) | aplicado bien | `experiments/verify_H3.py`, `results/verify_H3.{json,_output.txt}`. `\DtwoSmoothRK` = 0.40 sale de ahí. Reproduzco 0.39994 (r₁ = ½, r₂ = ¼, φ₂ = 0) con mi construcción. |
| m5 (tercer término más fino) | no aplicado (opcional; justificación aceptable) | RESPUESTA §3. |
| m6 (evidencia solo en la malla de f) | aplicado bien | `:387` «Evidence, at the grid values f ∈ {0.25, 0.35, 0.5} only». |
| m7 (docstring de `phase_margin.py`) | aplicado bien, con una atribución inexacta | `phase_margin.py:3–4` atribuye a `smooth_margin.py` que el mínimo en d = 2 está en β₂ = 0, pero ese script solo evalúa la fase por defecto en d = 2 (véase m6 nuevo). |
| m8 (`CONTINUIDAD:97`) | aplicado bien | CONTINUIDAD:97 («con arco base < πτ y bases distintas»). |
| Extensión (rondas 3 y 4) | aplicado a medias | Se hicieron los recortes (3)–(5) y otros, pero la Prop. 3.19 añade una página: 14 páginas (v0.4: 13). Véase M1. |

## 3. Hallazgos nuevos

### Bloqueantes

Ninguno.

### Mayores

**M1. Extensión: 14 páginas frente a un objetivo de 5–10.**
- *Ubicación:* el PDF entero; las secciones más largas son §3 (p. 3–11) y §4 (p. 11–12).
- *Problema:* el exceso de 4 páginas se justifica en parte, porque son pruebas completas. Pero hay material de registro y de historia que no es necesario para leer los resultados.
- *Corrección:* recortes concretos, juntos ≈ 1.5 páginas.
  1. Obs. 3.20: llevar al README la frase de la segunda corrida (periodo completo, cinco números) y la enumeración de lo que comprueba `check_certify_d2.py`. Dejar la base de confianza y la frase de no agudeza (≈ 6 líneas).
  2. §4, «Three further observations» (`:408`): dejar una frase por resultado (margen por defecto; mínimo sobre las fases, poligonal y liso; censo) y llevar al README los detalles del barrido, los periodos y los refinamientos (≈ 12 líneas).
  3. Obs. 3.18: llevar a la Tabla 1 o al README la lista de ν, μ por profundidad y las cotas/medido (≈ 5 líneas).
  4. Fundir el Lema 3.14 y la Prop. 3.15 (sugerencia de la ronda 4). Ahora que la Prop. 3.19 depende solo de (`eq:kaprec`), la fusión es aún más natural (≈ 8 líneas).
  5. Tabla 1: limitarla a f = ½, porque las filas de f = 0.35 no se usan en el texto (≈ 4 líneas).

### Menores

- **m1. «K₁ has κ > 0» es falso en r₁ = 4/13.**
  - *Ubicación:* `experiments/certify_d2.py:24–25` (docstring del bono) y `theory/d2_certified_derivation.md:159` («Como κ(K₁) > 0, el marco de Frenet es periódico»). Con menos peso, el paréntesis de `main.tex:197` (κ₁'²+κ₂'² = κ'²+v²κ²τ², que necesita κ > 0).
  - *Evidencia:* en s = π/2, D₁ = (0, −2(1−r), 3r) y D₂ = (4−13r, 0, 0), así que κ(π/2) = \|4−13r₁\|/(4(1−r₁)²+9r₁²). Se anula en r₁ = 4/13 ≈ 0.3077, en los tres puntos s = π/2 + 2πk/3 (`kmin.py`; mi primer encierro de μ por la fórmula de la torsión explotó justo ahí).
  - *Efecto:* ninguno sobre la prueba ni sobre el manuscrito, porque el bono no se usa y en r₁ ∈ {0.25, 0.35, 0.5} κ_min = 0.267, 0.197, 0.769 > 0.
  - *Defecto añadido del bono:* el encierro de α₂ en r₁ = ½ ([−3.69, −2.38]) cruza −π. «Reducir a (−π, π]» un intervalo así no tiene sentido, y el «m₂ ∈ [1.879, 2.088]» de `certify_d2.json` contiene valores > 2 imposibles por definición.
  - *Corrección:* en el docstring y en el .md, «K₁ has κ > 0 for r₁ ∉ {4/13} (κ vanishes at s = π/2 + 2πk/3 when r₁ = 4/13); the torsion enclosure is evaluated only at r₁ = 0.25, 0.35, 0.5, where κ > 0, and is not reduced to (−π, π] when it straddles ±π». O bien eliminar el bono. En `:197`, añadir «(where κ > 0)».
- **m2. La Prop. 3.15 se aplica fuera de la hipótesis f ≤ ½, y la prueba no lo dice.**
  - *Ubicación:* `main.tex:343` («By Proposition 3.15 with K = K₁, r = r₂»).
  - *Problema:* con r₂ = r₁/2 y thick(K₁) ≈ 0.416 en r₁ = ½, f₂ = r₂/thick(K₁) ≈ 0.60 > ½. El enunciado de la Prop. 3.15 remite a las hipótesis de la Prop. 3.8, formuladas con f = r/τ. La prueba solo usa ε = r₂κ_max(K₁) < 1, y eso se cumple: ε ≤ 0.355 en todas las cajas (`certify_d2.py:230`).
  - *Corrección:* «By the proof of Proposition 3.15, which uses neither τ nor f but only ε := r₂κ_max(K₁) < 1 (ε ≤ 0.355 on every box, checked by the script), with K = K₁, r = r₂, …». Opcionalmente, enunciar la Prop. 3.15 para todo r con rκ_max(K) < 1.
- **m3. Explicación de la no agudeza (Obs. 3.20, `:351`).**
  - «uses m₂ ≤ 2» no es una causa relevante en r₁ = ½: allí m₂ = 1.982 (α₂ = −3.027; `verify_H3.json` y mi integración). La pérdida (≈ 3×) viene de separar los cuatro supremos y del reparto de Minkowski.
  - El valor liso citado (0.40) es el de la fase por defecto en r₁ = ½. Con 24 fases obtengo 0.414 en r₁ = ½, y el máximo sobre r₁ ≤ ½ está cerca de r₁ ≈ 0.49, donde α₂ cruza π y m₂ salta de ≈ 1 a ≈ 2: allí vale 0.476 (`chain_check.py`; mismo cruce que el writhe por 3.5 de `:408`, r* = 0.4904).
  - *Corrección:* «The bound is not sharp: (kaprec) takes the four suprema separately (at r₁ = ½ the actual m₂ = 1.98, so m₂ ≤ 2 costs little); smooth values of r₂κ_max(K₂) are ≈ 0.40 at the default phases and below 0.5 over the phases and r₁ ≤ ½ sampled, against 1.187». Para eso hace falta un barrido liso propio, por ejemplo una extensión de `verify_H3.py` a φ₂ ∈ [0, π) y r₁ ∈ [0.45, 0.5].
  - Opcional: decir que la constante 1.187 depende de la extensión de intervalos concreta. Una implementación distinta, con la misma malla, da 1.1881 (§1.3). Imprimir «≤ 1.19» sería más robusto. 1.187 es correcta como cota certificada por el script.
- **m4. Base de confianza incompleta y fallo no explícito.**
  - *Base de confianza (Obs. 3.20):* añadir los supuestos «round-to-nearest mode without flush-to-zero (NumPy defaults), Python's `float()` of an `mpf` rounding to nearest».
  - *Fallo explícito (`certify_d2.py`):* hoy una caja con ε ≥ 1 o con NaN solo hace fallar el script por `TypeError` o por el `assert` de `make_numbers.py`. Sustituirlo por un fallo explícito: `assert res["ok"] and np.isfinite(res["total"])` en cada caja de `certify_continuum`, y `assert np.all(np.isfinite(Q[k].lo)) and np.all(np.isfinite(Q[k].hi))`.
  - *Respuesta, §4.4:* «Hay un caso límite teórico: ζ' entre SQ2_LO y √2» no puede ocurrir nunca, porque `SQ2_LO` es el mayor flotante menor que √2. Basta con decirlo.
- **m5. El README no lleva la salvedad de la Prop. 3.19.** README:39 dice «el caso d = 2 queda demostrado por computador» sin «aún no revisada por un árbitro independiente»; la FICHA (l. 13, 24) y la CONTINUIDAD (l. 41, 189) sí la llevan. Tras esta ronda, cambiar la etiqueta en todas partes (`main.tex:335`, `:425`, `:439`, README, FICHA ES/EN, CONTINUIDAD:41, :189, :193) a «computer-assisted proof (interval arithmetic); checked by an independent internal referee (round 5)», como se hizo con el bloque (H₃) en la ronda 4.
- **m6. Documentación de `smooth_margin.py` y `phase_margin.py`.**
  - *Ventana de exclusión:* el docstring de `smooth_margin.py` (l. 10) dice «antipodal pairs of one normal disc excluded». En realidad, la etapa de malla excluye \|ds − π\| ≤ 0.05 (l. 122) en el parámetro normalizado de K_d. En d = 3 eso son pares en hebras opuestas con bases a menos de 0.1 en el parámetro de K₂: arco base ≈ 0.5 ≈ 2.5 τ₂.
  - *Efecto de la ventana:* lo comprobé con una ventana de 0.004: los cinco márgenes son idénticos (1.3692, 2.0162, 0.2162, 0.2146, 0.2144), así que no cambia nada. Aun así, hay que documentarla o reducirla.
  - *Atribución en `phase_margin.py`:* `phase_margin.py:3–4` atribuye a `smooth_margin.py` que el mínimo en d = 2 está en β₂ = 0, pero ese script solo evalúa β₂ = 0. Atribuirlo al cálculo del árbitro de la ronda 4, o añadir a `smooth_margin.py` un barrido de φ₂ en d = 2.
- **m7. Limitación (1) (`:439`) y frase de estado.**
  - «completely at d = 1; for d ≥ 2 the curvature of K_d needs (H₃), whose constants are only measured» contradice la frase siguiente («d = 2 is settled …»).
  - *Corrección:* «completely at d = 1 and, computer-assisted, at d = 2; for d ≥ 3 the curvature of K_d needs (H₃) …».
  - En la misma línea: el Teorema 3.12 y la tabla de afirmaciones (`:423`) siguen bien, pero la fila `:422` («proved under (H₃); unconditional at d = 1») podría añadir «; at d = 2 superseded by Prop. 3.19».
- **m8. Discontinuidad de la familia en r₁ ≈ 0.4904 (sugerencia de presentación).** Con la convención α ∈ (−π, π], m₂ salta de ≈ 1 a ≈ 2 cuando α₂ cruza π: K₂ cambia de tipo (cable (2, 9) → (2, 11)) y su curvatura salta. La Prop. 3.19 cubre ambos lados por usar m ≤ 2, y conviene decirlo en una frase en la prueba («the bound m₂ < 2 covers both sides of r₁ ≈ 0.49, where α₂ crosses π and the cable slope of K₂ jumps; Lemma 3.2»). Así el lector no se pregunta si el salto se escapa del certificado.

## 4. Scripts nuevos `smooth_margin.py` y `smooth_H3.py`

- **`smooth_margin.py` es correcto.**
  - *Marco:* el marco de Bishop se obtiene integrando espectralmente la 1-forma de conexión. Comprobé que N' no tiene componente normal si φ' = −e₁'·e₂.
  - *Holonomía:* `antider0` ya incluye el término medio, de modo que `ph = th0 − I − αs/2π` es periódico. α se lleva a (−π, π] y la normalización es la de la Def. 2.1.
  - *Pares críticos:* el Newton usa el gradiente (dv·d₁, −dv·d₂) y el hessiano exactos de ½\|P₁−P₂\|², e incluye pares críticos de todo tipo.
  - *Radios:* r₂ = ½τ₁ (polígono N₀ = 512) y r₃ = r₂/2, como en la cadena.
  - *Reserva:* la de m6. La corrida con la ventana reducida da los mismos cinco valores.
- **`smooth_H3.py` es correcto.**
  - v' = D₁·D₂/v, 𝛋 = (D₂ − v'T)/v², μ = \|Π_⊥ d𝛋/dt\|/v, y el lado izquierdo de (12) usa los datos de K_{d−1}.
  - En d = 1 coincide con mi `mpmath` a 7 cifras.
- **Macros.**
  - `make_numbers.py:487–498` lee `smooth_margin.json` y `smooth_H3.json`, y redondea en el sentido correcto (por ejemplo ⌈0.1438⌉₂ = 0.15).
  - Al regenerar `numbers.tex` y `table_main.tex` en una copia, salen idénticos a los del repositorio (556 macros).
  - `\SmoothMarginThreeOneD` y `\SmoothMarginThreeB` están definidas pero no se usan en el texto (inofensivo).

## 5. Bibliografía

`refs.bib` no cambió desde v0.4 (`git diff 24d4385 HEAD`, vacío; 14 entradas, todas marcadas como verificadas en CONTINUIDAD:47 por rondas anteriores). No hay entradas nuevas que verificar. No usé WebSearch.

## 6. Compilación y extensión

- *Compilación:* `latexmk -pdf` en una copia compila sin errores. Hay 0 referencias o citas indefinidas, 0 cajas desbordadas y 0 «??» en `pdftotext`.
- *Extensión:* 14 páginas. El PDF solo difiere del del repositorio en metadatos.
- *Lectura de las páginas cambiadas:* leí las p. 9–11 (Prop. 3.19, Obs. 3.20, Hip. 3.21, Cor. 3.22, Conj. 3.25) en el PDF. No encontré problemas tipográficos. La numeración del texto, de la RESPUESTA y del README es coherente (Prop. 3.19, Obs. 3.20, Hip. 3.21, Cor. 3.22, Conj. 3.25).

## 7. Verificación computacional (CPU ≈ 4.7 min en total, núcleos compartidos)

| Qué | Tiempo de CPU | Resultado |
|---|---|---|
| `certify_d2.py` (copia del autor, en el scratchpad) | 7.7 s | Salida idéntica a `results/certify_d2_output.txt` salvo tiempos. Los SHA-256 de `experiments/` y `theory/` coinciden con `FROZEN_THEORY_SHA256.txt`. |
| `indep_iv.py`: encierro propio, solo `mpmath.iv`, 6 cajas r₁ × 2048 cajas s, más la peor caja con el periodo completo (6144 cajas) | 33 s + 16 s + 11 s | Peor caja: Φ ≤ 1.18806 (autor 1.18616); los cuatro datos coinciden con los del autor a ≤ 1.2·10⁻³. Periodo completo sin simetría: 1.1992. |
| `indep_cover.py`: cubrimiento propio de r₁ ∈ [0, ½] (32 × 512 cajas) | 45 s (más ≈ 60 s de un primer intento abortado con la fórmula de la torsión, que es singular en r₁ = 4/13) | máx Φ ≤ **1.477 < 2**, sin subdivisiones. |
| `dense_check.py`: puntos densos contra los encierros del autor | 92 s | 0 violaciones en 512 × 5 × 24 000 puntos (flotante, fórmulas propias); 0 en 7680 puntos con 40 dígitos en la peor caja; extremos en r₁ = ½ refinados en `mpmath`, iguales a los del autor. |
| `chain_check.py`: K₂ real con marco por doble reflexión, 24 configuraciones (r₁, φ₁) × 7 φ₂, más 3 r₁ × 24 φ₂ | 5 s | máx r₂κ_max(K₂) = 0.476 (r₁ = 0.49) ≤ 1.187. Holonomía α₂(½) = −3.0270, igual a `verify_H3.json`. |
| `smooth_margin.py` con ventana 0.004 (copia) | 7 s | Márgenes idénticos a `results/smooth_margin.json`. |
| `make_numbers.py` (copia) y `latexmk` (copia) | ≈ 5 s | `numbers.tex` y `table_main.tex` idénticos; PDF de 14 páginas sin advertencias. |

No ejecuté nada en `theory/` ni en la carpeta del paper.

## 8. Lista de acciones (por prioridad)

1. Cambiar la etiqueta de la Prop. 3.19 a «computer-assisted proof (interval arithmetic); checked by an independent internal referee (round 5)» en `main.tex:335`, `:425` y `:439`, en el README, en la FICHA ES/EN y en la CONTINUIDAD (l. 41, 189, 193). Añadir la salvedad que hoy le falta al README:39 (m5).
2. En la prueba de la Prop. 3.19, decir que se usa la prueba de la Prop. 3.15 con solo ε = r₂κ_max(K₁) < 1 (ε ≤ 0.355), fuera de f ≤ ½ (m2). Añadir una frase sobre el salto de m₂ en r₁ ≈ 0.49 (m8).
3. Corregir la explicación de la no agudeza en la Obs. 3.20 (m3). Completar la base de confianza y añadir `assert` explícitos de finitud y de `ok` en `certify_d2.py` (m4).
4. Corregir «K₁ has κ > 0» (falso en r₁ = 4/13) en el docstring de `certify_d2.py` y en `theory/d2_certified_derivation.md`, o eliminar el bono de la holonomía. No reducir a (−π, π] un intervalo que cruza ±π (m1).
5. Ajustar la Limitación (1) y la fila `:422` (m7).
6. Documentar la ventana de exclusión de `smooth_margin.py` y la atribución de `phase_margin.py:3–4` (m6).
7. Recortar ≈ 1.5 páginas según M1.
