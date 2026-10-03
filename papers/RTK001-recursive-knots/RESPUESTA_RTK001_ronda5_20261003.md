# Respuesta del autor a la ronda 5 de revisión interna — RTK001 (v0.5 → v0.6, 03/10/2026)

Informe: `REFEREE_RTK001_ronda5_20261003.md` (cambios menores; 0 bloqueantes, 1 mayor, 8 menores). El árbitro confirma
que la prueba asistida por computador del caso d = 2 (Prop. 3.19, Obs. 3.20) es correcta: comprobó la cadena lógica paso a
paso, auditó línea a línea el código de intervalos y obtuvo un encierro independiente propio (solo `mpmath.iv`). Agradezco
la auditoría; ningún hallazgo afecta al resultado.

## 1. Recuento

9 hallazgos (0 bloqueantes, 1 mayor, 8 menores): 8 aceptados, 1 aceptado con matiz (M1), 0 rebatidos. El m5 opcional de la
ronda 4 sigue sin aplicarse (justificación en §3).

- **M1 (extensión) — aceptado con matiz.** 14 → **13 páginas**, sin cambiar márgenes ni letra y sin quitar demostraciones.
  Apliqué los recortes (1), (2), (3) y (5) del árbitro y varias compresiones más. No apliqué el recorte (4), la fusión del
  Lema 3.14 con la Prop. 3.15: renumeraría la Prop. 3.19, recién arbitrada, y todo lo que la sigue.

## 2. Hallazgo mayor

**M1. Extensión (14 páginas) — aceptado con matiz.**

| Recorte del árbitro | Decisión | Qué se hizo |
|---|---|---|
| (1) Obs. 3.20 más corta | aceptado | Quedan: qué se certifica, la base de confianza completada (m4), quién la revisó (autor; árbitro de la ronda 5) y la frase de no agudeza corregida (m3). La segunda corrida sobre el periodo completo (cinco números) y la lista de comprobaciones de `check_certify_d2.py` pasan al README («Detalles de la prueba asistida del caso d = 2»). |
| (2) §4, «Three further observations» | aceptado | Una frase por resultado: margen por defecto; mínimo sobre las fases (poligonal y liso); censo. Pasan al README: tamaños de los barridos (12 valores de φ₂; malla 18 × 24 y dos refinamientos), periodos (π/3, desviación ≤ 0.05 puntos), L(K₂) constante a 10⁻⁵, márgenes en N₀ = 512 y en f = 0.35. |
| (3) Lista de ν, μ de la Obs. 3.18 | aceptado | En el texto queda «μ goes from 4.5 at d = 1 to 6.9 at d = 4 (smooth: 7.0)», junto con el lado izquierdo de (12) y la razón cota/medido. La lista completa va a `results/theory_constants.md`, que genera `make_numbers.py`. |
| (4) Fundir Lema 3.14 y Prop. 3.15 | no aplicado | Fundirlos renumera todo lo que sigue: 3.19 → 3.18, 3.20 → 3.19, 3.21 → 3.20, 3.22 → 3.21, 3.25 → 3.24. Esos números aparecen en este informe, en los anteriores, en el README, en la FICHA y en la CONTINUIDAD. El ahorro efectivo sería de ≈ 3 líneas (cabecera y entorno de prueba), y las 13 páginas se alcanzaron sin él. Tal como pide la consigna, la numeración de lo arbitrado no cambia. |
| (5) Tabla 1 solo con f = ½ | aceptado | Las filas f = 0.25 y 0.35 pasan a `results/theory_constants.md`; el texto remite allí. |

Compresiones adicionales, todas de registro o de redacción:
- resumen;
- introducción (historia de revisiones);
- §2.4 (los cocientes segmento–segmento quedan en `aux_checks.json`, y en el texto solo el mínimo local);
- párrafo tras la Def. 2.1;
- historia de v0.2 en el párrafo de la misma hebra;
- párrafo tras la Prop. 3.6, incluida la heurística de la hélice, en dos líneas;
- Obs. 3.4: se quita el cociente numérico;
- Obs. 3.23 y 3.24;
- párrafo de estado tras la Hip. 3.21 (los números duplicados de (C3) se quitan);
- «On the constant»;
- Limitaciones, Next steps y apéndice;
- tabla de afirmaciones: tres filas más cortas y columnas 0.55/0.42.

Otros cambios de estructura:
- **Antigua Obs. 3.26 («growth rate»).** Ahora es una frase sin número tras la Conj. 3.25. Era la última numerada, así que no renumera nada.
- **Tabla 2.** Las filas f = 0.25 (mismo comportamiento que f = 0.35) y la sonda f = 0.6 se omiten. Ya estaban en `results/tables.md`, y el pie de tabla remite allí.

**Numeración.** Idéntica a la de v0.5 para todo lo numerado hasta la Conj. 3.25.

## 3. Hallazgos menores

| id | Decisión | Cambio |
|---|---|---|
| m1 («K₁ has κ > 0» es falso en r₁ = 4/13) | aceptado | Lo comprobé: κ(K₁)(π/2) = \|4 − 13r₁\|/(4(1−r₁)² + 9r₁²), que se anula en r₁ = 4/13. Los valores de κ_min(K₁) son 0.267, 0.197, 0 y 0.769 en r₁ = 0.25, 0.35, 4/13 y 0.5, alcanzados en s = π/2 (`results/smooth_d2_phases.json`). **`experiments/certify_d2.py`:** el docstring dice ahora que el bono de holonomía necesita κ > 0, que solo se evalúa en r₁ = 0.25, 0.35, 0.5, que el encierro de α₂ en r₁ = ½ ([−3.69, −2.38]) cruza −π y que el «m₂» impreso no es un encierro de m₂ (contiene valores > 2). Un comentario en la línea de la «reducción a (−π, π]» dice lo mismo. El bono no se usa en la cota ni en el manuscrito. **Manuscrito:** en la Prop. 3.8, «κ₁'² + κ₂'² … is κ'² + v²κ²τ² where κ > 0». **`theory/d2_certified_derivation.md:159`** y el docstring de `theory/certify_d2.py` no se editan (`theory/` no se toca). La nota de corrección está en la CONTINUIDAD, ronda 5, fila m1. No aparecía en el README. |
| m2 (Prop. 3.15 aplicada con f₂ ≈ 0.6 > ½) | aceptado | **Prop. 3.15:** se enuncia «for every r > 0 with ε = rκ_max(K) < 1 (no condition on τ or f)». En el párrafo previo: «Lemma 3.14 and Proposition 3.15 hold for every r > 0 with ε < 1 and m > 0: their proofs use neither τ nor f ≤ ½». La prueba añade «which is algebraic, with \|x\| ≤ ε < 1». **Prop. 3.19, prueba:** «which needs only ε = r₂κ_max(K₁) < 1 and not f ≤ ½ (r₂/thick(K₁) may exceed ½: at r₁ = ½ the polygonal τ₁ = 0.4158 < 2r₂; the script checks ε ≤ 0.355 on every box)». **Origen de 0.355:** sale del JSON. `certify_d2.py` guarda la cota de ε de cada caja y su máximo en `certify_d2.json["B"]["max_eps_hi"]` = 0.354697 (peor caja; 0.25 × 1.41879). La macro es `\DtwoCertEpsMax` = 0.355 (redondeo hacia arriba), y `make_numbers.py` comprueba que ε_max < 1. |
| m3 (explicación de la no agudeza) | aceptado | **Obs. 3.20:** «(11) takes the four suprema separately and splits by Minkowski (at r₁ = ½ the actual m₂ is 1.98, so m₂ ≤ 2 costs little)». **Valores lisos** (no certificados) de r₂κ_max(K₂) con r₂ = r₁/2: ≈ 0.40 en r₁ = ½ con las fases por defecto; ≈ 0.41 como máximo sobre las fases en r₁ = ½; ≈ 0.48 como máximo sobre las fases y los r₁ ≤ ½ muestreados, justo antes de r₁*, frente a 1.187. **Script nuevo** `experiments/smooth_d2_phases.py`, con la misma construcción que `verify_H3.py` y una fase. Barre r₁ ∈ {0.05, …, 0.45} con 24 fases, y r₁ ∈ [0.45, 0.5] con paso 0.0025 más 0.4901–0.4908 con 48 fases, con refinamiento local. Resultado: máximo 0.4767 en r₁ = 0.4903, φ₂ = 0.06 (α₂ = +3.141, m₂ ≈ 1); en r₁ = 0.4904, α₂ = −3.141 y el valor cae a 0.40; en r₁ = ½, 0.3999 (fase por defecto, que allí es el mínimo) y 0.4149 (máximo). Coincide con el 0.476 en r₁ = 0.49 y el 0.414 en r₁ = ½ del árbitro. **Macros:** `\DtwoSmoothHalfMax`, `\DtwoSmoothMax` y `\DtwoSmoothMtwoHalf`; `make_numbers.py` comprueba que el valor en r₁ = ½ con fase 0 coincide con el de `verify_H3.json` (< 10⁻³). **Opcional:** se añade «The printed constant is that of this interval extension». No di la cifra de la implementación del árbitro, porque no sale de un script del paper. Sí la menciona el README. |
| m4 (base de confianza; fallo explícito) | aceptado | **Obs. 3.20 y docstring:** «IEEE-754 binary64 arithmetic in NumPy in round-to-nearest mode without flush-to-zero (the defaults), Python's `float()` of an mpmath number rounding to nearest, mpmath.iv, and about 150 lines of code». **`certify_d2.py`:** nueva `assert_finite(Q)` sobre los cuatro encierros (y la torsión) en `certify_point` y en `certify_continuum`. También `assert res["ok"] and np.isfinite(res["total"])` en cada caja de (B), y lo mismo en el bloque (A) y en el bucle de f_c. La prueba de la Prop. 3.19 lo dice: «the script stops if an endpoint is not finite or ε ≥ 1». **Re-ejecución:** salida idéntica salvo las tres líneas de tiempos; JSON idéntico salvo los tiempos y las claves añadidas `eps_hi` y `max_eps_hi` (comprobado por programa). **RESPUESTA de la ronda 4, §4.4:** el «caso límite ζ' entre SQ2_LO y √2» no puede ocurrir nunca, porque `SQ2_LO` es el mayor flotante menor que √2. La frase de aquella respuesta era innecesaria. Queda dicho aquí y en la CONTINUIDAD, sin editar el archivo histórico. |
| m5 (README sin salvedad; etiqueta) | aceptado | Etiqueta nueva **«computer-assisted proof (interval arithmetic); checked by an independent internal referee (round 5)»** en: el enunciado de la Prop. 3.19; la fila de la tabla de afirmaciones; la Limitación (1); el README (estado, idea, resultados y la nueva sección de detalles); la FICHA ES/EN (hallazgos y estado); y la CONTINUIDAD (l. 41, tabla de la ronda 4, abierto 2 de la ronda 4, que queda «cerrado en la ronda 5»). La introducción lo menciona. |
| m6 (`smooth_margin.py`, `phase_margin.py`) | aceptado | **`smooth_margin.py`, docstring:** ventana de exclusión \|ds − π\| ≤ 0.05 en el parámetro normalizado de K_d (más los pares a menos de r_d/2). En d = 3 incluye pares en hebras opuestas con bases a < 0.1 en el parámetro de K₂ (arco base ≈ 2.5 τ₂). Se cita la comprobación del árbitro con una ventana de 0.004: mismos cinco márgenes. Re-ejecutado: idéntico salvo tiempos. **`phase_margin.py`, docstring:** el mínimo en β₂ = 0 se atribuye al cálculo propio del árbitro de la ronda 4, no a `smooth_margin.py` (que solo evalúa β₂ = 0). |
| m7 (Limitación (1); fila de la tabla) | aceptado | **Limitación (1):** «proved for all doubly critical pairs at every depth, completely at d = 1 and, computer-assisted, at d = 2 (…); for d ≥ 3 the curvature of K_d needs (H₃) …». **Fila de la Prop. 3.8:** «proved under (H₃); unconditional at d = 1; at d = 2 superseded by Prop. 3.19». |
| m8 (salto de m₂ en r₁ ≈ 0.49) | aceptado | En la prueba de la Prop. 3.19: «This covers both sides of r₁ = r₁* ≈ 0.4904, where α₂ crosses π, m₂ jumps from ≈ 1 to ≈ 2 and the cable slope of K₂ jumps (Lemma 3.2, Section 4)». El nuevo barrido liso localiza el cruce entre 0.4903 y 0.4904. |
| m5 de la ronda 4 (opcional) | no aplicado | El tercer término más fino cambiaría el enunciado de la Prop. 3.15 y el cálculo certificado que el árbitro acaba de auditar, y no cambia ninguna conclusión. Sigue abierto. |

## 4. Cambios en el código y en los hashes

- **`experiments/certify_d2.py`:**
  - docstring y dos comentarios (m1, m4);
  - `assert` explícitos (m4);
  - clave `eps_hi` en cada fila y `max_eps_hi` en `B` (m2).
  - Ninguna operación aritmética cambió. Re-ejecutado: `certify_d2_output.txt` idéntico salvo tiempos; `certify_d2.json` idéntico salvo `meta` y las claves añadidas.
  - Ahora difiere de `theory/certify_d2.py`, que no se tocó y cuyo hash se mantiene.
- **`experiments/check_certify_d2.py`** (importa `certify_d2`): re-ejecutado, salida y JSON idénticos salvo tiempos. Conservo los archivos de v0.5, así que sus hashes no cambian.
- **`experiments/smooth_margin.py`, `experiments/phase_margin.py`:** solo docstrings. `smooth_margin.py` re-ejecutado, idéntico salvo tiempos; conservo sus salidas de v0.5. `phase_margin.py` no se re-ejecutó (≈ 2.5 min, solo cambia el docstring).
- **`experiments/smooth_d2_phases.py`** (nuevo) → `results/smooth_d2_phases.{json,_output.txt}`.
- **`experiments/make_numbers.py`:**
  - 5 macros nuevas: `\DtwoCertEpsMax` = 0.355, `\DtwoSmoothHalfMax` = 0.41, `\DtwoSmoothMax` = 0.48, `\DtwoSmoothMaxRone` = 0.490 (definida, no usada) y `\DtwoSmoothMtwoHalf` = 1.98;
  - escribe `results/theory_constants.md`;
  - el cuerpo de la Tabla 2 omite f = 0.25 y 0.6.
  - **Comprobación por programa:** las 556 macros de v0.5 conservan exactamente su valor (561 en total).
- **`results/FROZEN_THEORY_SHA256.txt`:** los hashes de v0.5 de `certify_d2.py`, `certify_d2.json`, `certify_d2_output.txt` y `smooth_margin.py` quedan comentados y los nuevos, activos. Se añade una sección v0.6 que explica qué cambió, más los hashes del script y los resultados nuevos. `sha256sum -c <(grep -v '^#' results/FROZEN_THEORY_SHA256.txt)` pasa sin fallos.
  - `experiments/certify_d2.py`: 950bc8ad…d1c9
  - `results/certify_d2.json`: 9d704c69…c8bc6
  - `results/certify_d2_output.txt`: f4fa00ed…42d5
  - `experiments/smooth_margin.py`: 52ba59a0…8e26
  - `experiments/smooth_d2_phases.py`: 954797fd…61a7 (hashes completos en el archivo)

## 5. Compilación y extensión

- **Compilación:** `manuscript/build.sh` (regenera las macros, `latexmk -pdf` y `latexmk -c`). Da 0 errores, 0 referencias o citas indefinidas, 0 cajas desbordadas y `pdftotext main.pdf - | grep -c '??'` = 0.
- **Extensión:** **13 páginas** (v0.5: 14).
- **Revisión visual:** rendericé y leí las páginas 1 (resumen), 7 (Tabla 1), 8 (bloque (H₃) con m2), 9–10 (Obs. 3.18, Prop. 3.19, Obs. 3.20, Hip. 3.21), 11 (Tabla 2, Conj. 3.25), 12 (observaciones de §4, tabla de afirmaciones) y 13 (Limitaciones, apéndice, bibliografía). No vi problemas tipográficos.
- **Versión:** v0.6, «five rounds of internal review applied», 3 October 2026.

## 6. Lo que queda abierto

1. (H_3) uniforme en d, y con ello (H_c) para d ≥ 3 (ruta para d = 3 en Next steps (1)).
2. Una cota certificada más fina en d = 2: hoy 1.187, frente a ≈ 0.48 en los valores lisos. minRad(K₂) > r₂ en f = ½ sigue sin certificar (solo f ≤ 0.484375).
3. Márgenes de la Conj. 3.25: solo en f = ½, con rejilla y refinamiento local, sin certificación; en d = 3 el margen liso es ≈ 0.21 %.
4. m5 de la ronda 4 (opcional).
5. Extensión: 13 páginas frente al objetivo original de 5–10. Bajar más exigiría quitar demostraciones o las tablas de evidencia.
6. Erratas de `theory/` (m1): anotadas en la CONTINUIDAD, sin editar `theory/`.

## 7. Cómputo

CPU de proceso, en núcleos compartidos:

| Tarea | CPU |
|---|---|
| `certify_d2.py` | 7.7 s |
| `check_certify_d2.py` | 13 s |
| `smooth_d2_phases.py` (dos corridas) | 11.9 s + 11.4 s |
| `smooth_margin.py` | 8.5 s |
| comprobación de κ(K₁) | < 1 s |
| `make_numbers.py` (×5) | ≈ 5 s |
| unas 15 compilaciones con latexmk y los renderizados | ≈ 50 s |

Total ≈ 1.8 min.
