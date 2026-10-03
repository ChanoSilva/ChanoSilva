# Respuesta del autor al informe de arbitraje interno — MRT001, ronda 5

Manuscrito revisado: v0.7 → **v0.8** (portada "Working draft v0.8 — 3 October 2026", fecha fija). Fecha de la respuesta: 03/10/2026. Informe atendido: `REFEREE_MRT001_ronda5_20261003.md` (veredicto "cambios menores": 0 bloqueantes, 0 mayores, 11 menores, m6–m9 opcionales, 10 acciones). En esta pasada se integra además el trabajo de segundo orden de `theory/` (`second_order.tex`, `second_order_derivation.md`, `check_second_order.py`, `check_second_order_output.txt`, `second_order_results.json`), verificado por mí antes de integrarlo (sección "Verificación independiente del segundo orden"). No se modificó ningún archivo de `theory/`.

Agradezco al árbitro la enumeración exhaustiva en C hasta n = 11, que además me sirvió para contrastar de forma independiente la ley exacta de R_n que calcula el bloque nuevo.

## Recuento

- Bloqueantes: 0. Mayores: 0.
- Menores: 11 → **11 aceptados** (m6 superado por el Teorema 5.11 del bloque de segundo orden; m1 aplicado también a la notación del bloque nuevo). Con matiz: 0. Rebatidos: **0**.
- Acciones de la lista final: las 10 aplicadas, salvo la parte estructural de la 8 (separar el material de realizadores en una nota propia), que por instrucción queda como **decisión pendiente del autor humano**, con el plan concreto en la nota de continuidad.
- Estado autorizado por el árbitro: los Teoremas 5.8–5.9, la Proposición 5.10 y el Lema B.2 llevan ahora "proved here; checked by an independent internal referee (round 5)" en el texto, la tabla de afirmaciones, el resumen, Limitations, README, FICHA y CONTINUIDAD. Los resultados nuevos de segundo orden llevan "not yet independently refereed".
- Números previos que cambiaron: **solo los dos de m4** (`\SharpDevMax` 0.95 → 0.96, `\SharpPieceMax` 0.97 → 0.98); las otras 251 macros de v0.7 tienen el mismo valor (comprobado por programa). Nuevas: 59 macros (53 `\Sec*` del segundo orden, `\HasSecond` y 5 `\SharpFifty*` de m2). Tablas: `table_sharp.tex` gana la columna "exact"; `table_e5f.tex` pierde las columnas "exceptions" y "5/n" (recorte 3).
- Compilación: 0 errores, 0 referencias/citas indefinidas, `pdftotext main.pdf - | grep -c '??'` = 0, 0 Overfull/Underfull. **31 → 33 páginas** (el bloque añade ≈ 3,5; los recortes quitan ≈ 1,5).

## Hallazgos menores

### m1 — Choque de notación π / π_k / p / p_k / p_i. **Aceptado.**
Pesos de Poisson: `q_k = e⁻¹/k!` (`q_k = 0` si k < 0) en el párrafo "Sharp rates", los Teoremas 5.8–5.9, la tabla de afirmaciones y todas las pruebas del Apéndice B. Patrón de tres elementos: `τ` (ω = (J, τ), N(τ), G_τ), también en la prueba de la Proposición 5.7, que usaba `p` con el mismo sentido. Puntos: "the i-th point precedes the j-th iff i < j and π(i) < π(j)" sustituye a `p_i ≺ p_j`. El bloque nuevo usaba `q_k` para Po(1 − 1/n), lo que habría vuelto a chocar: elegí una notación única, `q_k(λ) = e^{−λ}λ^k/k!`, `q_k = q_k(1)`, `q̃_k = q_k(1 − 1/n)`, y reescribí el bloque con ella. (τ ya denota traducciones en la Sección 2 y el tiempo propio en E5c; en el Apéndice B no aparece ninguno de los dos, así que seguí la propuesta del árbitro.)

### m2 — "Agree" en n = 50. **Aceptado** (y resuelto con datos exactos).
Texto nuevo del apéndice: "For n ≥ 100 the estimates of n d_TV(R_n, 2^Z) agree with c₂ = 1.184 and with the first-order law. At n = 50 the estimate 1.261 exceeds the first-order value 1.201 by 0.06 (2.9 standard errors) and the largest standardised atom-wise deviation is 4.4 (at most 3.3 for the larger n): the n⁻² term is visible there, since the exact value is 1.280 (κ/n ≈ 0.086, Remark 5.14)". El valor exacto procede de la ley exacta de R_n del bloque nuevo; la Tabla 11 tiene ahora una columna "exact" (1.280, 1.229, 1.206, 1.195 en n = 50, 100, 200, 400), que confirma los Monte Carlo dentro de sus intervalos. Fila de la tabla de afirmaciones: "Monte Carlo law of R_n agrees with the first-order law for 100 ≤ n ≤ 400; at n = 50 the O(n⁻²) term is visible (Table 11)". Todos los números son macros (`\SharpFiftyMC`, `\SharpFiftyFirst`, `\SharpFiftyExcess`, `\SharpFiftyZ` de la salida congelada de `check_sharp_rate.py`; `\SecExactFifty`, `\SecKappaOverFifty` de la del segundo orden).

### m3 — Hipótesis n ≥ 6. **Aceptado.**
"For n ≥ 6, the proof of Proposition 5.7 shows that outside 𝓔 at most one occurrence happens, …". Los contraejemplos 21453 y 32541 (n = 5) son correctos; el resultado solo se usa con n ≥ 20.

### m4 — Redondeo de cotas hacia abajo. **Aceptado.**
`make_numbers.py` tiene `up(x, d)` y `down(x, d)`; `\SharpDevMax` (0.9521) → 0.96 y `\SharpPieceMax` (0.9731) → 0.98 con `up`, `\SharpRmax` (0.9685 → 0.97) con `up` y `\SharpDevMin` (0.0161 → 0.016, cota inferior) con `down`; estas dos no cambian de valor. Las macros nuevas que son cotas se redondean del mismo modo (el bloque tecleado del agente traía dos redondeos hacia abajo, 0.994 por 0.99414 y 0.19 por 0.1933; ahora 0.9942 y 0.194).

### m5 — "gives every error term in closed form". **Aceptado.**
La Observación 5.11 desaparece: la sustituye el bloque de segundo orden, y la constante C ya no es abierta (Proposición 5.13). La frase ya no existe.

### m6 — El límite 3/(4e) es demostrable. **Aceptado (superado).**
Demostrado en el Teorema 5.11 (del bloque nuevo), con más de lo que pedía el árbitro: d_TV(N_n, Po(1 − 1/n)) = Φ(1/n) + ε_n con Φ explícita y |ε_n| ≤ (2^{n+1} − n − 2)/(n(n+1)!), y n²d_TV = 3/(4e) + 1/(4en) + O(n⁻²). La tabla de afirmaciones ya no lo lista como abierto.

### m7 — n ≥ 4 en el Teorema 5.8(ii). **Aceptado.**
Añadido: "(The identity and the bound also hold for n ≤ 3, by direct computation; n ≥ 4 is used only in the proof.)" Lo comprobé con mi ley exacta para n = 1…6: la identidad se cumple exactamente y n·n!·|d_TV − e⁻¹/n|/2 vale 0.13, 0.16, 0.085, 0.27, 0.063, 0.32 (< 1).

### m8 — Antecedentes del Teorema 5.8. **Aceptado.**
Estado: "proved here, an elementary consequence of the classical exact law [kaplansky1945]; checked by an independent internal referee (round 5)"; en la tabla de afirmaciones, "proved here (elementary from the classical exact law)". Búsqueda dirigida (WebSearch: sucesiones, aproximación de Poisson, variación total, Stein–Chen): no encontré un enunciado explícito de d_TV(N_n, Po(1)) ~ e⁻¹/n para sucesiones; los resultados tratan sobre todo puntos fijos (convergencia superexponencial) y el marco general de Chen–Stein. No cito Barbour–Holst–Janson porque no pude cotejar el capítulo; queda en pendientes.

### m9 — c₂ sin c₁. **Aceptado.**
Teorema 5.8(ii): "n d_TV(N_n, Po(1)) → c₁ = (e⁻¹/2) Σ|k − 1|/k! = e⁻¹".

### m10 — Etiquetas de estado. **Aceptado.**
Cambiado a "proved here; checked by an independent internal referee (round 5)" en: Teorema 5.8, Teorema 5.9, Proposición 5.10, Lema B.2, párrafo "Sharp rates" ("checked by an independent internal referee in round 5 (step by step, and by exhaustive enumeration of S_n for n ≤ 11)"), tabla de afirmaciones, resumen ("a result checked by an independent internal referee"), Limitations ("checked by an internal, not an external, referee"), README (estado e idea en tres líneas), FICHA (estado y hallazgos, en español e inglés) y CONTINUIDAD. Se conserva "internal". La constante C ya no figura como abierta porque ahora está demostrada (Prop. 5.13), pero esa demostración y el resto del segundo orden llevan "not yet independently refereed".

### m11 — Figura 3. **Aceptado.**
`[p]` → `[tb]`, ancho 0.9\linewidth, colocada justo después de la Tabla 7 (E5d): ahora sale en la p. 14 con las Tablas 6 y 7, y desaparece la página de una sola figura.

## Extensión y bibliografía

- Recortes de la sección 6 del informe, todos aplicados: (1) Figura 3; (2) quitada la parte de d_TV del Teorema 5.6(b) y el apartado (c), el final del Paso 3 (desde la cota cruda; queda la fórmula exacta de inclusión–exclusión, que usa el Teorema 5.8) y el Paso 4; el teorema conserva (a) y los momentos factoriales con "hence N_n → Z in law", y la frase de las fracciones (e⁻¹, e⁻¹, 8/3·e⁻¹ con error O(1/n)) pasa a un párrafo tras el teorema que remite al Teorema 5.8 y a la Proposición 5.10; la prueba de la 5.10 escribe ahora el acoplamiento del antiguo Paso 4; (3) "Sharpness and data" sin la frase de las z combinadas de E5f, y Tabla 9 sin las columnas "exceptions" y "5/n" (la observación de n = 20 se conserva dentro de la frase de los intervalos de confianza); (4) "Numerical check of the sharp rates" condensado (detalles de método en la salida congelada); (5) Observación B.1 con la fórmula y un solo ejemplo de razón no multiplicativa (4231 → 6). La tabla de afirmaciones se compactó para que siga cabiendo en una página.
- Resultado: 33 páginas (31 + ≈ 3,5 del segundo orden − ≈ 1,5 de recortes). No se recortó ninguna demostración.
- Separación del material de realizadores en una nota propia: **no se hizo** (decisión del autor humano). En CONTINUIDAD queda el plan concreto: saldrían el párrafo "The realizer law", el Teorema 5.3, los Lemas 5.4–5.5, los Teoremas 5.6–5.12, las Proposiciones 5.7, 5.10 y 5.13, la Observación 5.14, la Conjetura 5.15, el Apéndice B completo, la Tabla 9 y los scripts asociados; en MRT001 quedarían la Proposición 5.2, E5e y una página con los enunciados de 5.6 y 5.9 citando la nota (≈ 21–22 páginas).
- Bibliografía: `brignall2010` con `eprint = {0801.0963}` y `note = {arXiv:0801.0963}` (plainnat no imprime `eprint`). DOI de `corteel2006` no añadido: no lo confirmé. 47 entradas.

## Verificación independiente del segundo orden

Antes de integrar nada leí `theory/second_order.tex` y `second_order_derivation.md` paso a paso y escribí una comprobación propia, `scratchpad/author_r5/my_check_second_order.py`, que no importa ni copia ninguna función de `theory/` ni de `experiments/` (≈ 1 min de CPU en su versión final).

**Teorema S1 (`thm:secondN`, ahora Teorema 5.11). Correcto.**
- (i) A mano: E[(N_n)_r] − (1 − 1/n)^r = −Σ_{i≥2} C(r,i)(−1/n)^i es una serie alternante con módulos decrecientes (cociente (r − i)/((i+1)n) < 1), lo que da θ ∈ [0, 1]. Además, p_k = q_k(1 + c₁x) + r_{n,k} y q̃_k = q_k Σ c_j x^j.
- Lema de signos (`lem:signs`, ahora Lema B.3): h₀ > 0, h₁ = eˣ(1 − x) − 1 < 0, h₂ = (1 − x)h₁ (identidad simbólica), y h₃ > 0 ⇔ φ > 0 con φ' = x(2x + 1)/((1 − x)(1 − 2x)) (identidad simbólica). La convexidad en k la sustituí por la segunda diferencia explícita h_{k+1} − 2h_k + h_{k−1} = eˣ(1 − x)^{k−1}x² > 0 (verificada simbólicamente), que es más directa sobre los enteros. Comprobaciones: aritmética de intervalos sobre h_k(x)/x² mediante su serie con coeficientes racionales exactos, para k ≤ 6, en 4000 celdas que cubren [0, 0.4999], con 0 celdas sin certificar (la evaluación ingenua no certifica cerca de 0 por cancelación); y 400 000 evaluaciones puntuales con 60 dígitos (k ≤ 200, x = t/4000), con 0 violaciones. Signo negativo solo para k = 1, 2, como se afirma.
- (ii) Ley exacta de N_n por una **recurrencia propia** (insertar el máximo n en una palabra de [n−1]: justo después de n−1 suma una sucesión ascendente, dentro de una sucesión la rompe, en los demás n−1−k huecos no cambia nada; la inversión de posiciones da las descendentes), igual a la fuerza bruta para n ≤ 8, con momentos factoriales exactos 1 − r/n para n ≤ 60. Con 450 dígitos, para 3 ≤ n ≤ 200, max |d_TV − Φ(1/n)|/cota = 0.1933 (el agente obtiene el mismo valor). Comprobé a mano que Σ_{k<n} 1/(n k!(n−k+1)!) = (2^{n+1} − n − 2)/(n(n+1)!) y que q₁|h₁| + q₂|h₂| = Φ.
- (iii) d_j = (−j² + 5j − 3)/(2·j!): d₂ = 3/4, d₃ = 1/4, d₄ = 1/48 (serie de sympy). Mejora: Σ_{j≥2} d_j = eΦ(1) = 1, así que **Σ_{j≥5} d_j = −1/48 exactamente** (el agente daba "0.0208…"); de ahí (1 − x)/48 ≤ Σ_{j≥4} d_j x^{j−4} < 1/48, una prueba más limpia. θ_n ∈ [0.763, 0.997] para n ≤ 200 (el agente da [0.763, 0.9994] hasta n = 1000).
- Teorema 5.8(i) hasta n = 200: max |r_{n,k}| n k!(n−k+1)! = 0.990 (≤ 1; se acerca a 1, como observó el árbitro).

**Teorema S2 (`thm:bestpois`, ahora Teorema 5.12). Correcto.** Revisé a mano (i): |c_j(k)| ≤ [x^j]eˣ(1+x)^k, la cola ≤ q_k e 2^k δ³, Σ q_k e 2^k = e², y la identidad −q_k g_a x² + q_k c₂(x² − δ²) = q_k(1 − k)a x² − q_k c₂ δ². También (ii): Σ q_k g_a = 0, la cota L ≥ −2q₁g_a(1) = e⁻¹ con igualdad solo en a = ½, y la fórmula para a ≥ −¼ (g_a(3) = (1 + 4a)/2, g_a(k) ≥ (5 + 6a)/2 para k ≥ 4). Y (iii): los dos casos a > 3/2 y a < −1/2 por monotonía de e^{−λ} y los desarrollos e^{x−3x²/2} = 1 + x − x² + O(x³) y e^{x+x²/2} = 1 + x + x² + O(x³). Numéricamente, la fórmula cerrada de L(a) coincide con la suma directa (diferencia < 10⁻⁶⁰ para a ∈ [−¼, 5]), el mínimo de la rejilla está en a = 0.50, y n²d_TV en a = 0 y a = ½ para n = 100, 200 coincide con la salida del agente (0.27683, 0.18455; 0.27637, 0.18424).

**Proposición S3 (`prop:sharpC`, ahora Proposición 5.13) y Lema `lem:intref` (ahora Lema B.4). Correctos.**
- Lema B.4: recomputé a mano cada valor exacto (E I₄, I₅, I_{m−2}, …, I_{m−5}), la cota del bloque central 720(m−11)(m−5)/(m)₅ ≤ 720/(m)₃ (⇔ 9m ≥ 43), las cotas de los momentos de pares (90/(n)₂ + 944/(n)₃ + …) y s̄, h̄. Comprobado en racionales exactos para 12 ≤ m ≤ 400: razones máximas 0.958 (a), 0.977 (b), 0.998 (s), 0.992 (h). Reformulé (b) como "for n ≥ 12, Pr(𝓔) ≤ P̄(n)" (el original decía "for n = m").
- B(n): revisé cada término contra la prueba del Teorema 5.9 (ρ₁; P(𝓔) + E[#ω; 𝓔]; aproximación de las ocurrencias 4/(n−2) + 2d̄_{n−2} y 2/(n−1) + 2d̄_{n−1}; pesos 3/(n)₂). Mi evaluación independiente (sympy + mpmath) da 22²B(22) = 421.4905, 30²B(30) = 363.1054, 100²B(100) = 285.7965, 1000²B(1000) = 264.7776 y el límite simbólico 259 + 10/e = 262.679, igual que el agente.
- **¿La monotonía de n²B(n) está demostrada o solo comprobada?** Está **demostrada**, aunque el texto del agente lo argumentaba de forma sucinta. Lo verifiqué por programa: tras desarrollar P̄, s̄, h̄, d̄ y cancelar los factores n − 2 de los pesos, los 32 términos sin factorial son todos de la forma c/∏(n − i_j) con c > 0, al menos dos factores y 0 ≤ i_j ≤ 6 (sympy, término a término), y n² por cada uno es no creciente (producto de los factores n/(n − i₁), n/(n − i₂), no crecientes, y de los factores 1/(n − i_j), decrecientes); los 4 términos con factorial, multiplicados por n², decrecen. La prueba integrada escribe este argumento explícitamente y presenta la comprobación numérica (22 ≤ n ≤ 5000 del agente; 22 ≤ n ≤ 2000 mía) como complementaria. El enunciado no necesita la salvedad "checked numerically".

**Ley exacta de R_n (función generatriz del agente).** Contraste independiente: la enumeración exhaustiva en C del árbitro de la ronda 5 (`referee5_MRT001/exact.jsonl`, S_n completo, n = 4…11) da d_TV(R_n, 2^Z) = 0.423787225495, 0.290453892162, 0.294620558829, 0.24257317624, 0.194753377402 en n = 4, 5, 6, 8, 10, **iguales a 12 cifras** a los de la salida del agente.

**Reejecución.** `check_second_order.py` reejecutado en una copia del árbol (`theory/` + `experiments/lorentzian_chain.py`, que importa `check_realizer_law.py`): 54.6 s de CPU; salida idéntica a la guardada salvo las tres líneas con tiempos ("(0.2s)", "(42.9s)" frente a "(46.3s)", total), y JSON idéntico salvo `cpu_seconds`.

**Qué corregí al integrar.**
1. Notación (m1): q_k, q̃_k, q_k(λ), τ.
2. Sobreafirmación en la Observación: "the three extrapolations agreeing to six digits" es falso para el ajuste de grado 2 (4.297100 frente a 4.297071 y 4.297072). Ahora se dan los tres valores por macro, sin afirmar el número de cifras.
3. Números tecleados redondeados hacia abajo en el Bloque 3 (0.19, 0.994): todos los números del bloque, de la Observación 5.14, de la Conjetura 5.15 y de la Proposición 5.13 (422, 286, 262.68, 421.49, 285.80) son ahora macros que `make_numbers.py` genera desde `results/second_order_results.json` y `results/check_second_order_output.txt`, redondeando las cotas del lado seguro. Incluso el umbral 10⁻¹³⁰, los rangos de n y los tamaños de las comprobaciones salen de la salida.
4. κ: "κ ≈ 4.29707" se etiqueta "open; κ computationally verified (extrapolation of exact values), not proved". La forma cerrada κ = 7/2 + 13/(6e) y las de μ₂ van en una **Conjetura 5.15** separada, con estado "conjectural: read off the numbers…". Comprobé la aritmética de la conjetura: μ₂(4) = 1/(2e), μ₂(8) = 5/(3e), Σ_{k≥1}(k+1)q_{k−1} = 3 y la masa ½ fuera de los átomos dan 7/2 + 13/(6e) = 4.297072.
5. Lema de signos por segunda diferencia explícita; Σ_{j≥5} d_j = −1/48 exacto; "which is why its distance … is super-exponentially small" → "consistent with" (los momentos factoriales coincidentes no son por sí solos la causa); Lema B.4(b) reformulado.
6. "Most of the gap comes from the bad event 𝓔, which the proof charges in full although it rarely changes R_n": el árbitro y la parte (F) muestran que 𝓔 explica muchas excepciones en n pequeño, así que lo sustituí por la cuenta exacta de qué parte del límite viene de 𝓔 y de las ocurrencias dentro de él (90 + 150 de 259 + 10/e).

**Congelado.** `experiments/freeze_second_order.py` (nuevo; no modifica `theory/`; con `--run` ejecuta la comprobación en una copia temporal) quita las líneas de tiempo y el `cpu_seconds` y escribe `results/check_second_order_output.txt` (SHA-256 `328efae6b63a2b6c416def43ee34fd21a0d4ce5a45d33a4c5cac9de0e2c4c1b0`, también en `.sha256`), `results/second_order_results.json` (SHA-256 `f84eead08738f043883730d80f46b02287332522807796a447424aecf88dbf35`) y `results/check_second_order_meta.json` (ambos SHA, 51.3 s de la corrida de referencia, versiones). Congelando desde `theory/` (corrida del agente) y desde mi reejecución se obtienen los **mismos** SHA. `make_numbers.py` verifica los dos SHA y aborta si alguna comprobación de la salida no es OK/True o si una razón supera 1.

**Qué se integró y dónde.** Sección 5, en lugar de la Observación 5.11: párrafo "Second order", Teorema 5.11 (`thm:secondN`), Teorema 5.12 (`thm:bestpois`), Proposición 5.13 (`prop:sharpC`), Observación 5.14 (`rem:secondopen`), Conjetura 5.15 (`conj:kappa`); una frase en el esbozo de las pruebas. Apéndice B, tras la prueba de la Prop. 5.10: Lemas B.3 (`lem:signs`) y B.4 (`lem:intref`), pruebas y la ecuación (2) de B(n). Tras "Numerical check of the sharp rates": "Numerical check of the second-order results". Tabla 11: columna "exact". Tabla de afirmaciones: filas del segundo orden (proved here; not yet independently refereed), de la ley exacta (verified, exact computation) y de κ (numerical, not proved; closed form conjectural). Resumen, alcance ("three more" scripts), Limitations y Apéndice A actualizados. `experiments/requirements.txt`: `mpmath`.

## Compilación, números y cómputo

- `latexmk -pdf`: 0 errores, 0 referencias o citas indefinidas, 0 avisos de LaTeX, 0 cajas desbordadas o subllenas; `pdftotext main.pdf - | grep -c '??'` = 0; **33 páginas** (v0.7: 31). Después, `latexmk -c` (se conservan `main.pdf` y `main.bbl`).
- Renderizadas y revisadas: pp. 14 (Figura 3 con las Tablas 6–7), 17–18 (Teoremas 5.9–5.13, Observación 5.14, Conjetura 5.15), 20–21 (Tabla 9 recortada, Limitations, tabla de afirmaciones), 29–31 (prueba de la Prop. 5.13, comprobaciones numéricas, Tabla 11). Una primera compilación dejaba la p. 22 con una sola línea y la tabla de afirmaciones 117 pt más alta que la página; ambas cosas se corrigieron compactando filas y la frase de Limitations.
- Macros: comparación programática de `numbers.tex` (v0.7 frente a v0.8): 253 → 312; cambian solo `\SharpDevMax` y `\SharpPieceMax` (m4); 59 nuevas. `make_numbers.py` es determinista (dos ejecuciones dan el mismo `numbers.tex` byte a byte).
- Cómputo de la ronda: ≈ 6 min de CPU (reejecución de `check_second_order.py` 55 s; mi comprobación ≈ 3,5 min contando una versión intermedia de la aritmética de intervalos que no certificaba y se descartó; `make_numbers.py` y seis compilaciones ≈ 1 min). No se relanzaron E1–E5f, `check_realizer_law.py` ni `check_sharp_rate.py` (no cambian).

## Qué queda abierto

1. **Arbitraje independiente del segundo orden** (Teoremas 5.11–5.12, Proposición 5.13, Lemas B.3–B.4): por ahora solo los verificamos el agente teórico y yo.
2. Prueba del término n⁻² de la ley de R_n (κ ≈ 4.29707) y de la Conjetura 5.15 (κ = 7/2 + 13/(6e)).
3. La constante 422/n² es unas 70 veces holgada (≤ 5.72/n² numérico para n ≥ 22).
4. Cotejos con fuentes primarias (acción 10): Gallai 1967, Wolfowitz 1944, Kaplansky 1945, Kleindessner–von Luxburg, la página de Brignall 2010 y los enunciados exactos de Corteel–Louchard–Pemantle y Albert–Atkinson–Klazar; el DOI de `corteel2006`; los antecedentes del Teorema 5.8 en Barbour–Holst–Janson (1992).
5. Decisión del autor humano sobre separar el material de realizadores en una nota propia (plan en CONTINUIDAD).
