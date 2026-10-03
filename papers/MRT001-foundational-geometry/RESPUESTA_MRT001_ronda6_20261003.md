# Respuesta del autor al informe de arbitraje interno — MRT001, ronda 6

Manuscrito revisado: v0.8 → **v0.9** (portada "Working draft v0.9 — 3 October 2026", fecha fija). Fecha de la respuesta: 03/10/2026. Informe atendido: `REFEREE_MRT001_ronda6_20261003.md` (veredicto "cambios menores": 0 bloqueantes, 0 mayores, 9 menores, m6–m9 opcionales, 7 acciones). No se modificó ningún archivo de `theory/`.

Agradezco al árbitro que comprobara las pruebas paso a paso y con cálculos propios: la recurrencia propia para la ley de N_n, la comprobación a 460 dígitos, el Monte Carlo con variable de control de R_n y la observación de que el umbral de la Proposición 5.13 podía bajar a 14.

## Recuento

- Bloqueantes: 0. Mayores: 0.
- Menores: 9. **8 aceptados** (m1–m8; m7 en su forma fuerte, con el enunciado extendido a n ≥ 14) y **1 aceptado con matiz** (m9: recorte 2 aplicado; recorte 1 no, porque m4 y m6 añaden contenido a ese párrafo; la separación no se reabre). Rebatidos: **0**.
- Acciones de la lista final: aplicadas las 1–6. La 7 (cotejos con fuentes primarias, DOI de `corteel2006`, Barbour–Holst–Janson y separación del material de realizadores) sigue abierta, como pide el propio árbitro.
- Estado autorizado por el árbitro (m3): los Teoremas 5.11–5.12, la Proposición 5.13 y los Lemas B.3–B.4 llevan ahora "proved here; checked by an independent internal referee (round 6)". La Observación 5.14 sigue "open" y la Conjetura 5.15 sigue "conjectural".
- Números previos: **ninguno cambió**. Las 312 macros de v0.8 conservan su valor (comprobado por programa contra la copia de v0.8). Hay 14 macros nuevas (`\SecPrec*` y `\HasPrec`), generadas desde la salida congelada del script nuevo `experiments/check_second_order_precision.py`. Las 11 tablas generadas (`table_*.tex`) son idénticas byte a byte.
- Compilación: 0 errores, 0 referencias o citas indefinidas, `pdftotext main.pdf - | grep -c '??'` = 0, 0 cajas desbordadas y 0 avisos en el log. Quedan **33 páginas**, las mismas que en v0.8. `latexmk -c` deja `main.pdf`.
- Cómputo: ≈ 4 min de CPU. El script nuevo tarda ≈ 2 min en un núcleo y se corrió dos veces (véase m4); la compilación y `make_numbers.py` suman unos segundos.

## Hallazgos menores

### m1 — Uniformidad en a del Teorema 5.12(i). **Aceptado.**
Enunciado nuevo: "(i) For every compact set K ⊂ ℝ, n²d_TV(N_n, Po(1 − 1/n + a/n²)) = L(a)/2 + O(1/n) uniformly in a ∈ K."

En la prueba de (i):
- "Let a ∈ K and δ = 1 − λ = x − ax², so 0 < δ ≤ 1 for n large, uniformly in a ∈ K";
- termina con "|2d_TV − x²L(a)| ≤ … = O(x³), uniformly for a ∈ K, which is (i)".

En (iii): "If a ∈ [−½, 3/2], (i) with K = [−½, 3/2] and (ii) give n²d_TV ≥ 1/(2e) − O(1/n)".

Los tres términos de error de la prueba (|x² − δ²|, δ³ y Σ|r_{n,k}|) se controlan con sup_K |a|, así que la uniformidad ya estaba demostrada. Faltaba en el enunciado.

### m2 — Observación 5.14 y Conjetura 5.15. **Aceptado.**
- **Observación 5.14.**
  - El texto dice ahora "the fits indicate that n²(Pr(R_n = x) − Pr(2^Z = x) − μ(x)/n) converges for each of the 24 atoms …, that n²Pr(R_n ∉ {2^k, 3·2^k}) tends to 0.500000, and that n²(d_TV(R_n, 2^Z) − c₂/n) → κ ≈ 4.29707". Para ganar espacio, la ecuación desplegada pasa al texto corrido.
  - Estado: "open; κ estimated numerically (extrapolation of exact values for n ≤ 600), not proved".
  - Fila de la tabla de afirmaciones: "estimated numerically (extrapolation), not proved; closed form conjectural". Las dos etiquetas coinciden ahora.
- **Conjetura 5.15**, en tres partes:
  - (a) μ₂(2^k) = q_k[12C(k,4) − 12C(k,3) + 12C(k,2) − 3k − 5] para k ≥ 0, μ₂(3·2^k) = (k+1)q_{k−1} para k ≥ 1, y μ₂(3) = 0;
  - (b) n²Pr(R_n ∉ {2^k, 3·2^k}_{k≥0}) → ½;
  - (c) κ = μ₂(4) + μ₂(8) + Σ_{k≥1}μ₂(3·2^k) + ½ = 7/2 + 13/(6e). El enunciado hace explícito el supuesto que señalaba el árbitro: μ > 0 exactamente en 4 y en 3·2^k (k ≥ 1), μ = 0 en 2, 3 y 8, y μ₂(2) < 0 < μ₂(8).
  - El estado separa las tres partes: (a) se lee de los números (desviación ≤ 1.4·10⁻⁶ en los 24 átomos); (b) es una extrapolación (0.500000); (c) supone además que los límites pueden sumarse sobre los átomos.
- **Apoyos heurísticos**, en un párrafo nuevo tras la conjetura que empieza "Two heuristic checks, not proofs, support (a) and (b)". Comprobé la aritmética a mano:
  - *Cierre de masa.* Para Z ~ Po(1), E C(Z,r) = 1/r!. Por tanto Σ_k μ₂(2^k) = 12/24 − 12/6 + 12/2 − 3 − 5 = ½ − 2 + 6 − 3 − 5 = −7/2, y Σ_{k≥1}(k+1)q_{k−1} = Σ_{j≥0}(j+2)q_j = E[Z+2] = 3. Así −7/2 + 3 + ½ = 0, que es lo que se espera porque Pr(R_n ∈ ·) − Pr(2^Z ∈ ·) − μ/n tiene masa total 0 para cada n.
  - *Pares 321.* Cada intervalo 321 multiplica el conteo por 3/2, así que dos disjuntos dan R = (9/4)·2^N = 9·2^{N−2}, que no es ni 2^k ni 3·2^k. Hay ≈ n²/2 pares de ventanas disjuntas y cada par es un par de intervalos 321 con probabilidad (n−4)!/n! ≈ n⁻⁴. Número esperado: ≈ C(n,2)n⁻⁴ ≈ 1/(2n²), es decir n²·Pr → ½.
  - *Las demás configuraciones de orden n⁻² quedan en los átomos.* Los otros pares de ocurrencias dan razones (3/2)·2 = 3 o 2·2 = 4. Para los intervalos de cuatro elementos, comprobé por fuerza bruta en los 24 τ ∈ S₄ que t(G_τ) ∈ {1, 2, 4, 6, 24} (como dice el árbitro) y que t(G_τ)/2^{N(τ)} ∈ {1, 3/2, 2, 3, 6}; el texto da esta segunda lista.
  - El párrafo dice expresamente que son heurísticas y no pruebas.

### m3 — Estados de B.3–B.4 y del bloque de segundo orden. **Aceptado** (el coordinador acepta el informe).
"proved here; checked by an independent internal referee (round 6)" aparece en:
- los Teoremas 5.11 y 5.12, la Proposición 5.13 (con "using Theorem 5.3") y los Lemas B.3 y B.4;
- el párrafo "Second order": "Theorems 5.11–5.12 and Proposition 5.13 (added in version 0.8) are proved and checked numerically in Appendix B, and were checked by an independent internal referee (round 6); Remark 5.14 and Conjecture 5.15 are open";
- la fila de la tabla de afirmaciones;
- el resumen: "These results were checked by independent internal referees; the n⁻² term of the realizer law is only estimated numerically, from the exact law, and its closed form is conjectural";
- Limitations: "… were checked by internal, not external, referees (rounds 5 and 6)";
- README (estado, punto 3 de "Idea del paper" y fila nueva de la ronda 6), FICHA (estado y hallazgos, en español e inglés) y CONTINUIDAD.

`grep "not yet\|computationally verified\|only computed"` sobre main.tex: 0 resultados.

### m4 — Precisión de la comprobación del Teorema 5.11(ii). **Aceptado** (la opción preferida: subir la precisión).
Script nuevo **`experiments/check_second_order_precision.py`**, del paper y no de `theory/`. Es determinista y no importa nada de `theory/` ni de otros scripts.

Qué hace:
- **P1.** Calcula la ley exacta de N_n hasta n = 1000 en enteros por dos vías: la forma cerrada de Kaplansky C(n−1,k)(D_{n−k} + D_{n−k−1}) y la recurrencia de inserción del máximo. Las dos coinciden. Además coincide con la fuerza bruta para n ≤ 8, y los momentos factoriales son exactos para n ≤ 100.
- **P2–P3.** Para **cada** n usa mp.dps = ⌈log₁₀((n+1)!)⌉ + 30, entre 32 dígitos (n = 3) y 2601 (n = 1000).
- **P4.** Evalúa B(n) (véase m7).

Resultados:
- Para **todo 3 ≤ n ≤ 1000**, |d_TV(N_n, Po(1 − 1/n)) − Φ(1/n)| ≤ 0.19333 veces la cota (`\SecPrecRatio` = 0.194, redondeado hacia arriba). El máximo está en n = 4, el mismo valor que la salida de la ronda 5 para n ≤ 80 y que el cálculo del árbitro para n ≤ 200.
- En n = 200 el cociente real es 6·10⁻⁵⁷, y en n = 1000 es 2·10⁻²⁹⁶.
- Todos los signos de p_k − q̃_k quedan resueltos con un margen de al menos 10²⁹ unidades de redondeo.
- Teorema 5.8(i) hasta n = 1000: |r_{n,k}| n k!(n−k+1)! ≤ 0.998 (`\SecPrecRmax` = 0.999). En n = 200 da 0.9902, igual que el árbitro.
- θ_n ∈ [0.7634589, 0.9993997] para 3 ≤ n ≤ 1000, coherente con `\SecThetaLo/Hi`.

Congelado:
- `results/check_second_order_precision_output.txt` (sin líneas de tiempo, SHA-256 `52f6d7ffdd8f4ffede41f3fff91e0f7cbd0147b9ce561333b89cee9c41ab8a28`), más su `.sha256`, `check_second_order_precision.json` (SHA-256 `0cb90108…c18c`) y `check_second_order_precision_meta.json` (118 s en un núcleo).
- `make_numbers.py` verifica ambos SHA-256 y la línea "ALL CHECKS PASSED: True" antes de generar las macros.

Texto del apéndice: "These digits resolve the bound of Theorem 5.11(ii) only while it exceeds 10⁻¹³⁰, so the bound is checked by experiments/check_second_order_precision.py, with ⌈log₁₀((n+1)!)⌉ + 30 digits for each n (32 to 2601): for every 3 ≤ n ≤ 1000, |d_TV − Φ(1/n)| is at most 0.194 times the bound (the maximum is at n = 4), and |r_{n,k}| n k!(n−k+1)! ≤ 0.999." El script también figura en el Apéndice A y en el README, con el comando para reproducirlo, y el párrafo "Scope" de la introducción cuenta ahora "four more" (antes "three more") scripts que comprueban numéricamente las pruebas de la Sección 5.

Nota de transparencia: la primera corrida (en una copia en el scratchpad) etiquetaba como "31 to 2601 digits (n=3 …)" un mínimo que en realidad correspondía a n = 1, porque la parte P2 empieza en n = 1. Lo corregí (el rango de dígitos se registra solo desde n = 3) y repetí la corrida en la carpeta. Por eso el cómputo total se duplica. Los números son idénticos en las dos corridas.

### m5 — "Agree" para n ≥ 100. **Aceptado.**
Apéndice: "For n ≥ 100 the estimates of n d_TV(R_n, 2^Z) agree, within their sampling error, with c₂ = 1.184 and with the first-order law; the exact column shows that the n⁻² term (≈ κ/n) is present at every n, but for n ≥ 100 it is below the Monte Carlo resolution." Tras esto viene, sin cambios, la frase sobre n = 50.

Fila de la tabla de afirmaciones: "Monte Carlo law of R_n agrees with the first-order law within sampling error for 100 ≤ n ≤ 400; the exact law shows the n⁻² term at every n (Table 11)".

Las diferencias exacto − primer orden (0.037, 0.018, 0.009 en n = 100, 200, 400) son ≈ κ/n, como dice el árbitro.

### m6 — "Exact computation" para la ley de R_n. **Aceptado.**
- Fila de la tabla de afirmaciones: "verified (exact for n ≤ 30, floating point to 600)". Ambos números salen de macros (`\SecExactNmax`, `\SecFloatNmax`).
- Apéndice: "… with the floating-point computation (relative error 1.1·10⁻¹⁵) that is used for 30 < n ≤ 600; the system and its derivation are in theory/second_order_derivation.md, Section 5".
- Escribí la referencia en lugar de las dos líneas de ecuaciones, para no alargar el apéndice. CONTINUIDAD anota como abierto que el sistema no se demuestra en el manuscrito y que su validación es empírica.

### m7 — Umbral n ≥ 22 de la Proposición 5.13. **Aceptado, en la forma fuerte: enunciado extendido a n ≥ 14.**
Comprobé que la prueba vale tal cual desde n = 14:
- el Lema B.4(c) se usa con m = n − 2 ≥ 12 y m = n − 1 ≥ 13, y el lema pide m ≥ 12;
- P̄(n) pide n ≥ 12;
- d̄_m pide m ≥ 4;
- la afirmación estructural "outside 𝓔 at most one occurrence" pide n ≥ 6;
- el argumento de monotonía (términos c/∏(n − i_j) con i_j ≤ 6, y términos con factorial cuyo cociente consecutivo es < 1 para n ≥ 3) vale para n ≥ 7.

Numéricamente (script nuevo, parte P4, implementación propia de (2) con mpmath a 50 dígitos):
- n²B(n) es no creciente en 14 ≤ n ≤ 5000;
- 14²B(14) = 618.45 (el árbitro da 618.4);
- 22²B(22) y 100²B(100) coinciden con `C_table` de la salida congelada de la ronda 5.

Cambios en el texto:
- Enunciado: "For every n ≥ 14 … ≤ 619/n² (n ≥ 14), ≤ 422/n² (n ≥ 22), ≤ 286/n² (n ≥ 100)".
- (2): "for n ≥ 14".
- Prueba: "m = n − 2 ≥ 12"; "Hence n²B(n) is non-increasing for n ≥ 14; this was also checked numerically for 14 ≤ n ≤ 5000. Evaluating, 14²B(14) = 618.45, …".

Macros nuevas: `\SecPrecCfourteen` = 619 (⌈618.45⌉) y `\SecPrecBfourteen`. El resumen, el README y la FICHA conservan la forma "422/n² para n ≥ 22", que sigue siendo cierta y es la más legible. La cota empírica de 14 ≤ n ≤ 21 ya la cubre el "≤ 8.01 for 4 ≤ n ≤ 600" del texto.

### m8 — Soporte de la parte positiva para n pequeño. **Aceptado.**
Frase en la prueba del Teorema 5.11(ii): "(The argument does not need p_k ≤ q̃_k for k ∉ {1,2}; this holds for 6 ≤ n ≤ 1000 but not for smaller n, where {k : p_k > q̃_k} is {2}, {1,3} and {1,2,4} for n = 3,4,5; the difference is absorbed by ε_n.)"

El rango ("6 ≤ n ≤ 1000") y los conjuntos son macros (`\SecPrecPosNlo`, `\SecPrecNmax`, `\SecPrecPosSets`) generadas por el script nuevo. Este comprueba el signo de p_k − q̃_k para todo k y todo 3 ≤ n ≤ 1000 con la precisión de m4. Los conjuntos coinciden con los del árbitro y con la parte A4 de la salida de la ronda 5.

### m9 — Extensión. **Aceptado con matiz.**
- La separación del material de realizadores no se reabre.
- **Recorte 2 aplicado:** se elimina "version 0.7 reported this limit only numerically".
- **Recorte 1 no aplicado:** m4 y m6 añaden información a ese mismo párrafo (precisión por n, script nuevo, rango exacto/flotante y referencia a la derivación). Condensarlo ahora quitaría justo lo que piden m4 y m6.
- Para no crecer, la cita de Corteel–Louchard–Pemantle y Albert–Atkinson–Klazar del "Outline of the proofs", que repetía literalmente la del Paso 2 del Apéndice B, queda en "This first-moment computation is classical [2, 10]".
- El Apéndice A ya no empieza en página nueva (se quitó un `\clearpage`). Sin eso, los ≈ 10 renglones netos añadidos por m2, m7 y m8 habrían dejado una página casi vacía y el total habría pasado a 34.
- Resultado: **33 páginas, como en v0.8**.
- La nota de continuidad tiene la estimación actualizada: el material de realizadores y tasas ocupa ≈ 13,5–14 de 33 páginas, y el segundo orden ≈ 2 en el cuerpo y ≈ 3 en el apéndice. Con el plan de la ronda 5, MRT001 quedaría en ≈ 20–21 páginas y la nota en ≈ 15–16.

## Lista final de acciones del árbitro

| acción | estado |
|---|---|
| 1. Uniformidad de 5.12(i) (m1) | hecha |
| 2. "Estimated numerically", Conjetura en (a)/(b)/(c), cierre de masa y heurística 321 (m2) | hecha |
| 3. Estados de 5.11–5.13 y B.3–B.4 en todos los lugares; 5.14 y 5.15 abiertas (m3) | hecha |
| 4. Precisión de A4 o restricción de la frase (m4) | hecha: script nuevo en `experiments/` con la precisión que cada n requiere, para todo 3 ≤ n ≤ 1000 (más que el rango 3 ≤ n ≤ 200 propuesto) |
| 5. "Within sampling error" y término n⁻² visible en la columna exacta (m5) | hecha |
| 6. Opcionales m6, m7, m8, m9 | m6, m7 (forma fuerte) y m8 hechas; m9 con matiz (recorte 2; recorte 1 no) |
| 7. Cotejos con fuentes primarias, DOI de `corteel2006`, Barbour–Holst–Janson, separación | abiertos (CONTINUIDAD, "Queda abierto tras la ronda 6") |

## Verificación de la ronda 5 y bibliografía
El árbitro da 11/11 puntos de la ronda 5 bien aplicados y ninguno con error nuevo, así que no requieren acción. La bibliografía no cambia: 47 entradas, `brignall2010` verificada por el árbitro, `corteel2006` sigue sin DOI confirmado.

## Comprobaciones finales
- Macros: 312 de v0.8 con el mismo valor (comparación por programa del `numbers.tex` de v0.8, copiado antes de empezar, con el nuevo). Ninguna eliminada; 14 añadidas: `\SecPrecNmax` 1000, `\SecPrecDigitsLo` 32, `\SecPrecDigitsHi` 2601, `\SecPrecRatio` 0.194, `\SecPrecRatioN` 4, `\SecPrecRmax` 0.999, `\SecPrecPosNlo` 6, `\SecPrecPosSets`, `\SecPrecBNmax` 5000, `\SecPrecBfourteen` 618.45, `\SecPrecCfourteen` 619, `\SecPrecSeconds` 118, `\SecPrecSha` y `\HasPrec`.
- Tablas generadas: idénticas a las de v0.8.
- Ningún número nuevo está escrito a mano. Las constantes que aparecen en el texto nuevo (½ − 2 + 6 − 3 − 5, 9/4, {1, 3/2, 2, 3, 6}, 1/(2n²)) son aritmética demostrable a mano, como las del resto de las pruebas.
- Páginas revisadas tras renderizar: 17–19 (Teoremas 5.11–5.12, Proposición 5.13, Observación 5.14, Conjetura 5.15 y párrafo heurístico), 21 (tabla de afirmaciones), 22 (Limitations, Next steps y Apéndice A), 28–29 (pruebas de 5.11–5.13, Lemas B.3–B.4, (2)) y 30–31 (comprobaciones numéricas y Tabla 11). Sin cajas desbordadas ni flotantes descolocados.
