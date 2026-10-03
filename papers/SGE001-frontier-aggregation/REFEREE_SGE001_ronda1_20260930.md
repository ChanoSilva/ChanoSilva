# Informe de arbitraje interno — SGE001 "Dynamic Aggregation of Production Frontiers" (ronda 1, 30/09/2026)

> Numeración de enunciados: v0.1 (Lema 3.4 jerarquía, Lema 3.5 bisagra, Prop. 3.6 capacidad, Cor. 3.7, Obs. 3.8, Ej. 3.9, Prop. 3.10 margen); en v0.4–v0.5 son Lema 3.6, Lema 3.7, Prop. 3.8, Cor. 3.9, Obs. 3.10, Ej. 3.11, Prop. 3.12. [Nota añadida en la ronda 3.]

Árbitro independiente (sesión Claude Code; no es el autor del borrador). Material revisado íntegramente: `README.md`, `CONTINUIDAD_SGE001_20260930.md`, `FICHA_SGE001_propuesta.md`, `manuscript/main.tex` (421 líneas), `refs.bib`, `numbers.tex`, `table_*.tex`, `main.pdf` (15 páginas, renderizado y revisado), `experiments/frontier_aggregation.py` (842 líneas), `experiments/make_numbers.py`, `results/results.json`, `results/tables.md`. Archivos de trabajo del árbitro (scripts y corrida de reproducción) en el scratchpad de la sesión, carpeta `referee_SGE001/` (`check_math.py`, `check_slope.py`, `check_cert.py`, `check_tau.py`, `repro/`). No se modificó nada en la carpeta del paper salvo la creación de este informe.

Las referencias a líneas son de `manuscript/main.tex`; "Prop. 3.x" sigue la numeración del PDF.

---

## Veredicto

**Cambios mayores.** Todos los enunciados marcados "proved here" son correctos (verificados paso a paso y, donde procede, numéricamente) y la corrida de referencia se reproduce bit a bit (4700 valores idénticos); pero el resumen, la sección E1/E2 y la ficha contienen afirmaciones cuantitativas que no dicen lo que el cuerpo mide (un "certificado computable" que usa el error verdadero y omite un factor 2; un exponente 3.78 presentado como predicho cuando es un efecto de N finito; una "constante a cuatro cifras" que es una identidad algebraica; un "15 de 23" erróneo en la ficha), el título anuncia una dinámica que el trabajo no contiene, no hay ninguna medida de incertidumbre y el manuscrito tiene 15 páginas frente a un objetivo de 5–10.

Recuento: 2 bloqueantes, 8 mayores, 15 menores.

---

## Hallazgos bloqueantes

**B1. Número erróneo en la ficha pública propuesta.**
- Ubicación: `FICHA_SGE001_propuesta.md`, "Principales hallazgos" (ES: "falla en 15 de 23 celdas con capacidad"; EN: "fails in 15 of 23 capacity cells").
- Problema: las celdas elegibles para C2 son 23 en total (3 sin capacidad + 20 con capacidad) y las que fallan son 15, todas con capacidad. "15 de 23 celdas con capacidad" es falso.
- Evidencia: `results.json` → `E4.summary`: `C2_eligible_cells=23`, `C2_eligible_smooth_cells=3`, `C2_eligible_capped_cells=20`, `C2_failing_capped_cells=15`. El resumen del manuscrito ("15 of the 20 threshold cells") y el README ("15 de 23 celdas elegibles, todas con capacidad (15 de 20)") lo dicen bien.
- Corrección: ES: "falla en 15 de las 20 celdas elegibles con capacidad (23 elegibles en total; las 3 sin capacidad pasan)". EN: "fails in 15 of the 20 eligible capacity cells (23 eligible in all; the 3 cells without capacity pass)". Véase además M5 sobre la fragilidad estadística de "las 3 sin capacidad pasan".

**B2. El "certificado de mejora" de E1 no es computable desde los momentos y omite un factor 2; la región certificada real es la mitad.**
- Ubicación: `main.tex` líneas 260 ("The bound is smaller than the first-order error, and therefore *certifies* that the second order improves on the first, only for σ ≤ 0.10 (LN) and σ ≤ 0.12 (SU)"), resumen ("comes with a computable, conservative certificate", línea 371 y abstract), y código `frontier_aggregation.py` línea 339 (`sigma_largest_bound2_le_e1`: compara la mediana de `bound2_rel_med` con la mediana de `e1_med`).
- Problema: (i) la condición usada, B₂ < |E₁|, emplea el error verdadero E₁, que el usuario de momentos no observa; (ii) lo que sí se puede certificar desde (x̄, Σ, cotas de derivadas) es |E₂| ≤ B₂ y |E₁| = |E₂ + Q₂| ≥ |Q₂| − B₂, de modo que la mejora queda certificada sólo si **2B₂ < |Q₂|**; (iii) la comparación se hace entre medianas sobre réplicas, no réplica a réplica.
- Evidencia: `check_cert.py` (mismo diseño, misma semilla, N = 2000, 20 réplicas): mayor σ con el test del artículo = 0.100 (LN) / 0.124 (SU); mayor σ con 2B₂ < |Q₂| en todas las réplicas = 0.056 (LN) / 0.071 (SU) (idéntico con la mediana). El factor ~2 en σ es el esperado: B₂ ∝ σ³, |Q₂| ∝ σ².
- Corrección: sustituir en E1 por: "The improvement is certifiable from moments alone when 2B₂ < |Q₂| (then |E₂| ≤ B₂ < |Q₂| − B₂ ≤ |E₁|); this holds in every replication only for σ ≤ 0.056 (LN) and σ ≤ 0.071 (SU), whereas the improvement itself is observed up to σ ≈ 0.42." Añadir al código la macro correspondiente (`largest sigma with all(2*B2 < |Q2|)`), y en el resumen cambiar "comes with a computable, conservative certificate" por "comes with a computable certificate that is very conservative (valid only for σ ≲ 0.06)". En E4 el certificado sí es el correcto (|Ŷ₂ᴬ − Ŷ₂ᴮ| > B₂ᴬ + B₂ᴮ): no cambiar.

---

## Hallazgos mayores

**M1. El exponente "3.78" (CD–LN) y "3.21" (CES–LN) no son exponentes predichos: son un efecto de N finito, y la explicación de la nota de continuidad es incorrecta.**
- Ubicación: abstract ("Simulation confirms both regimes to the predicted exponents (3.78–4.00 against 1.00)"); `main.tex` línea 227 ("between 3 and 4 on log-normal inputs"); `CONTINUIDAD` ("el 3.78 … es intermedio entre 3 y 4 porque el tercer momento log-normal es O(σ⁴) solo asintóticamente"); README ("orden 2 = 3.78 (log-normal)", omite 3.21 de CES).
- Problema: por la propia Obs. 3.2, E₂ = (σ³/6)N⟨D³f, μ₃ᶻ⟩ + O(σ⁴) con μ₃ᶻ el tercer momento **muestral** de la configuración. Para la ley LN a N fijo, μ₃ᶻ no se anula: su fluctuación muestral es O(N^{-1/2}) (≈ √6 σ³/√N por coordenada), comparable a la asimetría poblacional 3σ⁴ cuando σ ≈ 1/√N. A N fijo y σ → 0 el exponente es exactamente 3; la ventana de ajuste [0.01, 0.042] con N = 2000 cae en el cruce entre los regímenes σ³ (ruido) y σ⁴ (asimetría), de ahí 3.78 (y 3.21 para CES, cuyo D³f contrae de otro modo el ruido).
- Evidencia: `check_slope.py`, CD–LN, misma semilla, 6 réplicas, ajuste en σ ≤ 0.05: pendiente de |e₂| = **2.90 (N = 200), 3.76 (N = 2000), 4.21 (N = 20000)**; pendiente de |e₃| = 4.00 en los tres casos (el orden 3 elimina el momento muestral exactamente).
- Corrección: en el abstract escribir "to the predicted exponents (2, 4 and 4 for symmetric inputs; 1 at a crossing)"; en E1 añadir: "On log-normal inputs the fitted exponent (3.78 CD, 3.21 CES) lies between 3 and 4 because the sample third central moment of a finite population does not vanish: its O(N^{-1/2}) sampling fluctuation contributes a σ³ term that dominates the O(σ⁴) population skewness for σ ≲ N^{-1/2}; the exponent is 2.9 at N = 200 and 4.2 at N = 20000." Corregir la frase de la nota de continuidad.

**M2. "To four digits in the constant" es una identidad algebraica, no una verificación; la verificación de Cor. 3.7 (T_u = στ_z + O(σ²)) no se reporta.**
- Ubicación: abstract; `main.tex` línea 281 ("The ratio −E₂/(N T_u) is 1.0000 at the smallest dispersion"); Tabla 6 ("−E₂/(N T_u) = 1.0000 at σ = 0.01 … verified"); FICHA ("verificado a cuatro cifras").
- Problema: por la Prop. 3.6, E₂(f_c) + N T_u = E₂(f) − N[(ū−c)₊ − (f(x̄)−c)₊] (+Q₂ si f(x̄) > c). En la rama "below" el término es E₂(f) ~ 10⁻⁹ relativo; en la rama "above" con ū > c es **exactamente cero**. El 1.0000 (de hecho 1 − 3·10⁻¹⁴, `E2.summary.LN_delta0_ratio_smallest_sigma`) es la identidad verificada a precisión de máquina, no una prueba de la aproximación. La afirmación con contenido, T_u/(στ_z) → 1 (Cor. 3.7), no aparece en ninguna parte. Lo mismo vale para "the two-sided bound holds in 168/168 cells": por ser (1) exacta, sólo re-comprueba B₁ ≥ |E₁(f)| y B₂ ≥ |E₂(f)|, ya comprobado en E1.
- Evidencia: `check_tau.py` sobre el diseño de E2 (N = 2000, 20 réplicas, δ = 0, τ_z = (1/2N)Σ|g·z_i| con z_i = x̄⊙shock_i): SU: mediana de T_u/(στ_z) = **0.9973, 0.9917, 0.9747, 0.9287** para σ = 0.01, 0.0316, 0.1, 0.316 (desviación lineal en σ, como dice el corolario). LN: 0.970, 0.974, 0.978, 0.918 — no tiende a 1 porque en LN f(x̄_muestral) ≠ c (véase M4).
- Corrección: reemplazar "and to four digits in the constant" por "and the crossing term to T_u/(στ_z) = 0.997 at σ = 0.01 on symmetric inputs"; en E2 añadir la columna o macro T_u/(στ_z); reescribir la frase sobre la cota bilateral: "(1) is an identity; the two-sided bound (2) reduces to the smooth bounds B₁, B₂, which hold in every cell".

**M3. "Dynamic" en el título no está respaldado por nada en el trabajo.**
- Ubicación: título; `main.tex` línea 73 (Scope: "'Dynamic' is read as the behaviour of the error along a continuous sweep of the input dispersion and through the levels of a hierarchy"); `CONTINUIDAD` supuesto 2.
- Problema: un barrido en σ no es dinámica, y la jerarquía tampoco. La reconstrucción está declarada con honestidad, pero el título promete lo que la ficha pública de la línea promete y el borrador no entrega; un lector externo lo leerá como sobreafirmación. "Jerárquica" sí es defendible (dos niveles, Lema 3.4), aunque véase M8.
- Corrección (elegir una, confirmando con el autor): (a) retitular el borrador "Moment-based aggregation of production frontiers: second-order corrections, their failure at capacity thresholds, and what can be certified for comparisons", con nota a pie: "research line SGE001, 'dynamic aggregation of production frontiers'"; o (b) añadir el elemento dinámico mínimo que la teoría ya cubre: una trayectoria σ_t o una media x̄_t que se acerca a la capacidad (δ_t → 0), con E₂(t) dado por la Prop. 3.6 y el cruce de régimen de la Obs. 3.8, y el experimento E2 reinterpretado como esa trayectoria. Hasta entonces, quitar "Dynamic" del título del PDF.

**M4. Hipótesis del Cor. 3.7 y de la Obs. 3.2: configuración fija vs. diseño LN; regularidad; uniformidad en N.**
- Ubicación: Cor. 3.7 (líneas 182–192), Obs. 3.2 (línea 131), Obs. 3.8, E2 (línea 281: "as Corollary 3.7 states").
- Problema: (i) El corolario supone x_i = x̄ + σz_i con (z_i) fija y f(x̄) = c. El diseño SU lo cumple exactamente (pares antitéticos: media muestral = x̄, z_i = x̄⊙w_i). El diseño LN **no**: x_i = x̄⊙exp(σz_i − σ²/2), la configuración centrada depende de σ y f(x̄_muestral) − c = O(σ N^{-1/2}) ≠ 0 (medido: |f(x̄)−c|/c hasta 3.6·10⁻⁴ en σ = 0.01, 1.1·10⁻² en σ = 0.3; 12 de 20 réplicas con x̄ por encima). El enunciado aplicable a LN es la Obs. 3.8 con b aleatorio de orden N^{-1/2}; eso explica el 0.97 de M2. (ii) Obs. 3.2 afirma E₂ = (σ³/6)N⟨D³f, μ₃ᶻ⟩ + O(σ⁴); con f ∈ C³ sólo se obtiene o(σ³); O(σ⁴) requiere D³f Lipschitz (C⁴), cierto para CD y CES pero no enunciado. (iii) La pregunta "¿O(σ²) uniforme en N?" se responde afirmativamente sólo si s_z², m₃ᶻ, M₂, M₃ están acotados uniformemente en N; M₂, M₃ son supremos sobre el casco convexo de la población, que para z gaussiano crece como σ√(log N) y para Cobb–Douglas D^k f diverge en 0. El texto no lo dice.
- Corrección: añadir tras Cor. 3.7: "The corollary applies verbatim to the SU design; for the LN design the centred configuration depends on σ and f(x̄) − c = O(σN^{-1/2}), so Remark 3.8 with a random b of order N^{-1/2} is the applicable statement. The constants depend on the population only through s_z², m₃ᶻ and the derivative suprema over its convex hull; the relative error bound is uniform in N whenever these are." En Obs. 3.2 cambiar "f ∈ C³" por "f ∈ C⁴ (or D³f Lipschitz)" para el O(σ⁴).

**M5. Ninguna medida de incertidumbre; el criterio C2 por celdas con 1000 ensayos es frágil justo donde importa.**
- Ubicación: E4 (línea 328: "0 of the former [smooth cells fail]"; Tabla 4; Tabla 6 "Predefined C2 fails in 15 of 23 eligible cells, all with a capacity"); E1 (exponentes por mínimos cuadrados sobre 6 puntos sin error estándar; medianas sobre 20 réplicas sin intervalo).
- Problema: con 1000 ensayos, la celda suave σ = 0.4 pasa C2 por 3.3 % ≤ 17.5 %/5 = 3.5 %; intervalo de Wilson al 95 % de rev₂: [2.4, 4.6] %, y de rev₁/5: [3.05, 4.00] %. La afirmación "todas las celdas con capacidad" (y "0 de las suaves") depende de ~2 reversiones. La celda (+50 %, σ = 0.4) falla por 6.5 % > 27.3 %/5 = 5.5 %, con intervalos solapados ([5.1, 8.2] vs [4.9, 6.0]). El resto de fallos son masivos y la conclusión cualitativa sobrevive, pero el recuento "15 de 23" y "0 de 3" no son robustos.
- Evidencia: `check_tau.py` (función `wilson`), valores en el bloque anterior.
- Corrección: reportar intervalos de Wilson para todas las tasas de la Tabla 4 y declarar C2 "falla / pasa / indeterminado" cuando los intervalos se solapan; añadir intervalos bootstrap sobre réplicas a las medianas de E1–E3 y errores estándar a los exponentes; reformular: "C2 fails clearly in 14 capacity cells, is borderline in one capacity cell and in the smooth cell σ = 0.4, and passes in the remaining cells".

**M6. La rama en f(x̄) = c la decide el redondeo de coma flotante (SU) o el azar de la media muestral (LN); E2 no lo declara y "min |E₁|/|E₂| = 1.00" es en parte artefacto.**
- Ubicación: Def. 2.4 ("at f(x̄) = c we adopt the 'below capacity' branch"); código `aggregate`, línea 215 (`below = fb <= cap`); E2 (línea 281: "the minimum improvement ratio |E₁|/|E₂| at δ = 0 is 1.00 over the entire sweep: the second order buys nothing"); E5 lo reconoce sólo de pasada ("or, for the symmetric law, rounds").
- Problema: en SU con δ = 0, f(x̄_muestral) − c ∈ ±1.5·10⁻¹⁵ y la comparación `fb <= cap` cae en "below" en 12/11/13 réplicas y en "above" en 8/9/7 (σ = 0.01/0.1/0.3). En la rama "above" Ŷ₂ ≡ Ŷ₁ por construcción, así que el mínimo sobre réplicas de |E₁|/|E₂| es 1 exactamente por definición, no por la teoría (en la rama "below" el cociente es 1.003 en σ = 0.01). El resultado cualitativo no cambia (la diferencia entre ramas es O(σ²)), pero el diseño no debe depender del redondeo.
- Evidencia: `check_slope.py`, bloque "SU delta=0".
- Corrección en código: en `aggregate` añadir un argumento `branch_at_equality="below"` y usar `below = fb <= cap * (1 + 1e-12)` (o pasar explícitamente la rama en δ = 0); en E2 y E5 reportar ambas convenciones en una fila. En el texto de E2: "at δ = 0 the sample mean lies on either side of the capacity (LN: by sampling; SU: by rounding, which we fix to the below branch); the ratio is 1.003 at σ = 0.01 in the below branch and exactly 1 in the above branch, where Ŷ₂ = Ŷ₁ by construction".

**M7. En E5 los regímenes "above" y "at" no informan sobre la recalibración, pero cuentan como fallos de C1.**
- Ubicación: Tabla 5 (filas "above": 1.00, 1.00, 1.00; filas "at": 1.00); línea 357 ("No variant meets C1 (order 2: no; global: no; by regime: no)"); `E5.summary`.
- Problema: en "above", Q₂ ≡ 0 y no hay nada que recalibrar; además en σ = 0.03 nadie cruza y e₁ = 2·10⁻¹⁶ (`E5.rows`, LN above σ = 0.03): "razón mínima 1.00" significa 0/0, no un fallo. En "at", la razón 1.00 es el artefacto de M6. El fallo real y sustantivo de C1 está en "smooth" (global 0.38–0.60; régimen 4.65–6.66) y "below" (0.47–0.60 a σ pequeño): eso basta para la conclusión.
- Corrección: marcar "above" como "n/a (Q₂ ≡ 0)" en la Tabla 5 y excluirlo de la cuenta de C1; en "at" reportar la razón en la rama "below" y la fracción de réplicas en cada rama; reescribir la conclusión de E5 apoyándola en "smooth" y "below".

**M8. Etiquetas de estado demasiado generosas en la Tabla 6 y un estimador definido para que el lema sea trivial.**
- Ubicación: Tabla 6 (filas "Exact remainder identities and bounds … (Prop. 3.1) — proved here"; "Top-down two-stage … (Lem. 3.4) — proved here; verified"); Def. 2.3; línea 157 ("hierarchy buys exactly one thing"); `CONTINUIDAD` ("Resultados matemáticos (todos con demostración completa)").
- Problema: Prop. 3.1(a)–(c) son las formas de Lagrange e integral del resto de Taylor (Dieudonné, cap. VIII) sumadas sobre i; (d) es una línea. Lema 3.4(i) es la ley de covarianza total (clásica) y el estimador "top-down" de la Def. 2.3 está construido evaluando la corrección intra-firma en la media sectorial precisamente para que coincida con el agrupado: la identidad es por definición, y la "tercera" alternativa no existe. El Lema 3.5 es elemental. Nada de esto es incorrecto, pero "proved here" sugiere aportación original. Lo original (y modesto) del trabajo es la combinación Prop. 3.6 + Cor. 3.7 + Ej. 3.9 + Prop. 3.10.
- Corrección: en la Tabla 6 usar "classical (Taylor), assembled here" para Prop. 3.1; "elementary (law of total covariance); by construction of Def. 2.3" para Lem. 3.4(i); "elementary" para Lem. 3.5; mantener "proved here" para Prop. 3.6, Cor. 3.7, Ej. 3.9, Prop. 3.10. En la Def. 2.3 decir que TD se define así y que, por tanto, sólo hay dos estimadores distintos (agrupado y ascendente), que es lo que se compara en E3.

---

## Hallazgos menores

**m1.** `main.tex` línea 328: "the capped cells that pass are those at the largest dispersion". Son 5: (+50 %, 0.8), (+20 %, 0.8), (+10 %, 0.8), (+5 %, 0.8) y **(+50 %, σ = 0.2)**, donde ninguna unidad alcanza la capacidad (celda suave de hecho). Además las filas +50/+20/+10 % en σ = 0.8 son idénticas (48.1 / 0.1 / 92.1 %) porque la media muestral queda bajo la capacidad y las aproximaciones no ven el tope; sólo la verdad cambia. Decirlo: "four cells at σ = 0.8, where the approximations do not see the capacity (the sample mean stays below it) and the second order is right because Q₂ᴬ is large, and the +50 % cell at σ = 0.2, where no unit reaches the capacity".

**m2.** Ej. 3.9 es más fuerte de lo enunciado: las dos poblaciones tienen también **tercer momento central igual (0)**; difieren en el cuarto (σ⁴ vs 2σ⁴). Enunciar "identical first three moments" y en el abstract "identical first and second moments" → "identical first three moments". (Verificado: medias c, varianzas σ², agregados 4c − 2σ y 4c − √2σ.)

**m3.** Numeración obsoleta en figuras y código: leyenda de la Fig. 1 "certified bound on order 2 (Prop. 1)" y título del panel derecho de la Fig. 2 "(Prop. 3)" (código `fig_E1`, `fig_E2`); comentarios del código "Prop. 1", "Prop. 3", "Prop. 4" (`aggregate`, `run_E6`). En el PDF son Prop. 3.1 y Prop. 3.6.

**m4.** `table_e1b.tex` y `table_e5b.tex` se generan (`make_numbers.py`) pero no se usan en `main.tex`; eliminarlas o usarlas (E1b no tiene tabla en el texto).

**m5.** Tiempos inconsistentes: `results.json` `meta.seconds` = 35.5, `\MetaSeconds` = 36, README "~45 s" y "~42 s", nota de continuidad "~42 s"; mi corrida: 47.6 s de pared / 43.2 s de CPU. Unificar ("35–50 s según la máquina").

**m6.** Línea 326: "the decision is close to a coin toss at every order" para tasas entre 28 % y 70 %: 28 % no es una moneda y 70 % es peor que una. Escribir "between 28 % and 70 % at every order".

**m7.** C1 en LN: "holds up to σ = 0.42 and fails beyond" (línea 243) y "above a dispersion of 0.42" (abstract). Se cumple en el punto de malla 0.4217 (razón 6.32 CD, 5.83 CES) y falla en el siguiente, 0.5623 (3.40, 3.06): el umbral está en (0.42, 0.56). Decir "holds at σ = 0.42 and fails at the next grid point, σ = 0.56".

**m8.** Un único flujo `rng` compartido por E0–E5 (`main`): los sorteos de E2 dependen de que E1 haya corrido antes con el mismo N. Usar `np.random.SeedSequence(SEED).spawn(k)` con un generador por experimento; no cambia resultados actuales si se documenta como nueva corrida de referencia.

**m9.** Bibliografía: `harris2020` y `virtanen2020` con "and others" — poner la lista completa (son las fichas oficiales de NumPy/SciPy). Nataf 1948: volumen y páginas confirmados; número (3) no confirmado en línea (es el número de julio; mantener).

**m10.** README y abstract omiten el exponente CES–LN 3.21 (dicen "3.78 (log-normal)" / "3.78–4.00"); tras M1, escribir "3.2–3.8 on log-normal inputs at N = 2000 (finite-N effect)".

**m11.** Obs. 3.12 y E1b: "the second-order remainder, of order σ⁴" — para LN a N fijo es σ³–σ⁴ (M1); escribir "of order σ³–σ⁴".

**m12.** Fig. 2 (derecha): el eje y está recortado a [0, 2] y la curva δ = −0.30 cae fuera a σ grande (donde E₂(f) domina a T_u); ampliar el eje o decirlo en el pie. Tabla 2: filas con e₁ = 2.0·10⁻¹⁶ (δ = +0.10, σ ≤ 0.0316: nadie cruza, error exactamente 0) deben mostrarse como 0, no como ruido de máquina.

**m13.** "Both criteria were fixed before the runs" (línea 233): no hay forma de verificarlo (no hay log con fecha, ni git, ni versión previa del código); tampoco hay indicio de cambio a posteriori (umbrales 5 y 2 % codificados con comentario, sin alternativas comentadas). Registrar en la nota de continuidad la fecha y un hash del script antes de la próxima corrida. El resumen "for σ ≤ 0.2 the minimum ratio is at least 34/69/33/63" (macro `EoneRtoMinLeTwo`) es un resaltado descriptivo elegido después; etiquetarlo como tal o quitarlo.

**m14.** Def. 2.4: en f(x̄) = c el Hessiano de f_c no existe; decir explícitamente que "second-order approximation" en ese punto es una convención (una de las dos derivadas laterales), no una propiedad de f_c.

**m15.** E2, línea 281: "its lower-bound form … is informative (positive) in 32 of them, the others being either without crossing or at dispersions where the smooth bounds are large" — correcto (32/168), pero conviene decir que la cota inferior es informativa exactamente cuando N T_u > B₁ + B₂, es decir σ ≲ 0.15–0.2, y que fuera de ese rango la Prop. 3.6 sigue siendo una identidad exacta.

---

## Bibliografía

Crossref está bloqueado por el proxy de red de la sesión (403 / EGRESS_BLOCKED); se verificó con WebSearch (JSTOR, OUP, RePEc, Wiley, Econometric Society, Experts@Minnesota). Las entradas no listadas abajo son obras canónicas cuyos datos coinciden con el conocimiento del árbitro, pero no se verificaron en línea.

| Entrada | Estado | Corrección |
|---|---|---|
| nataf1948 (Econometrica 16(3), 232–244) | verificada (vol. 16, pp. 232–244; año 1948); número no confirmado | ninguna |
| vangarderen2000 (J. Econometrics 95(2), 285–331) | verificada | ninguna |
| lewbel1992 (RES 59(3), 635–642) | verificada | ninguna |
| houthakker1955 (RES 23(1), 27–31) | verificada (DOI 10.2307/2296148; vol. 23 es 1955–56) | opcional: `year = {1955--1956}` o nota |
| cobbdouglas1928 (AER 18(1, Supplement), 139–165) | verificada | ninguna |
| oehlert1992 (Am. Stat. 46(1), 27–29) | verificada (DOI 10.1080/00031305.1992.10475842) | ninguna |
| klein1946 (Econometrica 14(2), 93–108) | verificada (JSTOR 1905362) | ninguna |
| stoker1984 (Econometrica 52(4), 887–907) | verificada (JSTOR 1911190) | ninguna |
| felipefisher2003 (Metroeconomica 54(2–3), 208–262) | verificada (DOI 10.1111/1467-999X.00166) | ninguna |
| meeusen1977 (IER 18(2), 435–444) | verificada (DOI 10.2307/2525757) | ninguna |
| harris2020, virtanen2020 | datos de revista correctos; lista de autores truncada | sustituir "and others" por la lista completa (BibTeX oficial de NumPy/SciPy) |
| jensen1906, theil1954, gorman1953, fisher1969, jones2005, stoker1993, hildenbrand1994, acms1961, farrell1957, aigner1977, ccr1978, kumbhakarlovell2000, dieudonne1960 | no verificables en línea en esta sesión; coherentes con el conocimiento del árbitro | ninguna propuesta |

Uso de las citas: todas respaldan la afirmación para la que se usan (Jensen → brecha de Jensen; Oehlert → método delta de segundo orden; Lewbel y van Garderen et al. → expansiones por momentos; Houthakker/Jones → formas agregadas desde la distribución; Dieudonné cap. VIII → fórmula de Taylor; Cobb–Douglas y ACMS → fronteras; Farrell → eficiencia). La frase introductoria sobre fronteras cita cinco trabajos (farrell, aigner, meeusen, ccr, kumbhakarlovell) para una sola idea; dos bastan.

Resumen: 10 verificadas, 0 corregidas (2 con lista de autores por completar), 13 no verificables en línea.

---

## Verificación computacional

1. **Corrida completa** (`frontier_aggregation.py` sin `--fast`, copiado al scratchpad con rutas redirigidas; Python 3.11.15, NumPy 2.4.6, SciPy 1.17.1, Matplotlib 3.11.2 — las mismas versiones de la referencia): **47.6 s de pared, 43.2 s de CPU de usuario**. Comparación hoja a hoja con `results/results.json`: **4700 valores numéricos, diferencia relativa máxima 0.0** (idénticos); `tables.md` idéntico salvo la línea de runtime. Dentro del presupuesto de 5 min de CPU.
2. **Macros**: `make_numbers.py` ejecutado contra el JSON de referencia hacia el scratchpad: `numbers.tex` (204 macros) y las 7 tablas son **idénticas** a las de `manuscript/`. Muestreo independiente adicional de ~60 números (E1 filas CD–LN y CES–LN, E2 δ = 0, E3 con capacidad, E4 36 celdas, E5 36 filas, E1b 9 filas) contra el texto del PDF: todos coinciden.
3. **Compilación LaTeX** en el scratchpad (pdflatex + bibtex, 3 pasadas): 15 páginas, **0 cajas desbordadas (Overfull)**, 0 referencias indefinidas.
4. **Matemáticas numéricas** (`check_math.py`, Cobb–Douglas, N = 7, σ = 0.35): identidades integrales (b) y (c) por cuadratura coinciden con E₂ directo a 4·10⁻¹³; supremos por esquina (Frobenius) ≥ supremo real de la norma de operador sobre cada segmento (cocientes 0.993 para D², 0.997 para D³; 0 violaciones; 0 violaciones entrada a entrada en 2000 puntos por caja); B₁ = 0.2511 ≥ |E₁| = 0.0564, B₂ = 0.0698 ≥ |E₂| = 0.0047, iguales a las del código; identidad (1) de la Prop. 3.6 a 10⁻¹⁵ para σ ∈ [0.005, 0.2]; T_u/(στ_z) = 0.998 (σ = 0.01) → 1.
5. **Pendiente vs N** (`check_slope.py`): véase M1. **Rama en δ = 0**: véase M6. **Certificado observable** (`check_cert.py`): véase B2. **T_u/(στ_z) e intervalos de Wilson** (`check_tau.py`): véanse M2 y M5.
6. Código: no hay fuga entre entrenamiento y prueba en E5 (choques nuevos del mismo flujo); sin ajuste de hiperparámetros con prueba; semilla única y determinista; empates imposibles en E4 (`sign` de diferencias continuas); tolerancias y unidades correctas; fórmulas de derivadas del apéndice coinciden con `CobbDouglas.K3` y con el autotest E0 (1.8·10⁻¹⁰, 1.9·10⁻⁹). Diseño SU: x > 0 garantizado para σ ≤ 0.5 (|w| ≤ √3). Concavidad: CD con Σa = 0.8 < 1 y CES con ρ = −1, ν = 0.8: correcto.

---

## Recortes propuestos para llegar a ≤ 10 páginas (actual: 15, de las cuales 1.5 son bibliografía)

1. Introducción (p. 1–2): reducir el párrafo de literatura a las 8–10 citas que el texto usa; quitar ccr1978, kumbhakarlovell2000, meeusen1977 (dejar farrell y aigner), hildenbrand1994, klein1946 (dejar nataf y felipefisher), stoker1993 (dejar stoker1984), jones2005 o houthakker1955 (dejar uno), y mover harris/virtanen a una nota al pie del apéndice. Ahorro ≈ 0.8 página.
2. Teoría (p. 3–6): fusionar Obs. 3.2 y 3.3 en una; comprimir la prueba de la Prop. 3.1 a cuatro líneas citando Taylor; prueba del Lema 3.4 en dos líneas; quitar la Obs. 3.8 como enunciado separado y ponerla como frase final del Cor. 3.7. Ahorro ≈ 0.7 página.
3. Experimentos (p. 6–12): Tabla 2 (E2) y Tabla 3 (E3) → apéndice o `results/tables.md` (ya existen allí), dejando en el texto una fila cada una; fusionar Fig. 2 y Fig. 3 en una figura 2×2; Fig. 4 reducir a tres paneles (sin capacidad, +10 %, +0 %); E1b a un párrafo dentro de E1 sin subsección; E3 y E5 a la mitad (los mecanismos ya están en la teoría); eliminar el párrafo "Common protocol" duplicado por el apéndice. Ahorro ≈ 2.5 páginas.
4. Apéndice A: las fórmulas de derivadas de CD y CES al docstring del código (E0 las comprueba); dejar solo la lista de diseños. Ahorro ≈ 0.5 página.
5. Tabla 6 (claims): mantener, pero a 12 filas y sin repetir números que ya están en el texto. Ahorro ≈ 0.2 página.

Total estimado: 15 → 10 páginas sin perder ningún enunciado ni ningún número verificable (los que salen del cuerpo quedan en apéndice/Markdown).

---

## Lista de acciones (por prioridad, en imperativo)

1. Corrige la ficha (ES y EN): "15 de las 20 celdas elegibles con capacidad (23 elegibles en total)" (B1).
2. Sustituye el test B₂ < |E₁| (medianas) por el certificado observable 2B₂ < |Q₂| en todas las réplicas; actualiza macro, texto de E1 (σ ≤ 0.056 LN / 0.071 SU) y abstract (B2).
3. Reescribe el abstract: quita "to the predicted exponents (3.78–4.00…)" y "to four digits in the constant"; pon exponentes 2/4/4 (SU) y 1 (cruce), y T_u/(στ_z) = 0.997 (M1, M2).
4. Añade en E1 la explicación del exponente 3–4 en LN como efecto de N finito con los valores 2.9/3.8/4.2 (N = 200/2000/20000), y corrige la frase de la nota de continuidad (M1).
5. Añade a E2 la columna/macro T_u/(στ_z) y reescribe la frase sobre la cota bilateral como identidad (M2).
6. Decide con el autor el título: quita "Dynamic" o añade la trayectoria σ_t/δ_t que la Prop. 3.6 ya cubre (M3).
7. Añade tras el Cor. 3.7 la nota sobre diseño SU (exacto) vs LN (Obs. 3.8 con b = O(N^{-1/2})), la dependencia de las constantes y la condición de uniformidad en N; cambia C³ por C⁴ en la Obs. 3.2 para el O(σ⁴) (M4).
8. Añade intervalos de Wilson a la Tabla 4, bootstrap sobre réplicas a las medianas y errores estándar a los exponentes; reformula C2 como "14 fallos claros, 2 celdas limítrofes" (M5).
9. Fija la rama en f(x̄) = c por argumento explícito/tolerancia en `aggregate` y reporta ambas ramas en E2 y E5; declara en E2 cómo se reparten las réplicas (M6).
10. Marca "above" como n/a en la Tabla 5 y apoya la conclusión de E5 en "smooth" y "below" (M7).
11. Reetiqueta la Tabla 6: Prop. 3.1 "classical (Taylor), assembled here"; Lem. 3.4(i) "elementary; by construction"; Lem. 3.5 "elementary"; di en la Def. 2.3 que solo hay dos estimadores distintos (M8).
12. Corrige la frase de E4 sobre las celdas que pasan (cuatro en σ = 0.8 y la de +50 % en σ = 0.2) y explica las filas idénticas (m1).
13. Enuncia el Ej. 3.9 con "tres primeros momentos iguales" (m2).
14. Actualiza "Prop. 1"/"Prop. 3" en leyendas de figuras y comentarios del código a 3.1/3.6 (m3).
15. Elimina o usa `table_e1b.tex` y `table_e5b.tex` (m4).
16. Unifica los tiempos de ejecución en README, nota y PDF (m5).
17. Sustituye "close to a coin toss" por "between 28 % and 70 %" (m6).
18. Escribe el umbral de C1 en LN como "holds at 0.42, fails at the next grid point 0.56" (m7).
19. Usa un generador por experimento (`SeedSequence.spawn`) y declara nueva corrida de referencia (m8).
20. Completa las listas de autores de harris2020 y virtanen2020 (m9).
21. Incluye el exponente CES–LN en README y abstract (m10) y corrige "of order σ⁴" en Obs. 3.12 (m11).
22. Amplía el eje de la Fig. 2 derecha o anótalo; muestra 0 en vez de 2·10⁻¹⁶ en la Tabla 2 (m12).
23. Registra fecha y hash del script con los criterios C1/C2 en la nota de continuidad antes de la próxima corrida; etiqueta el resumen "σ ≤ 0.2" como descriptivo (m13).
24. Aplica los recortes de la sección anterior hasta ≤ 10 páginas.
