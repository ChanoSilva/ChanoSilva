# Respuesta del autor a la ronda 5 de revisión interna — TCD001 (03/10/2026)

**Estado: terminada.** Manuscrito v0.6 → **v0.7** (fecha fija 3 October 2026; 14 páginas, letra normal).

Informe: `REFEREE_TCD001_ronda5_20261003.md`. Árbitro nuevo e independiente; dictamen de cambios menores: 0 bloqueantes, 1 mayor de redacción y 5 menores. Confirmó como correctos la Prop. 5.12, el refuerzo del Teorema 5.8 y la pertenencia a NP.

**Recuento.**
- Aceptados: 5 (M1, m2, m3, m4, m5).
- Aceptado con matiz: 1 (m1). La condición de igualdad propuesta omitía el caso f⁰ = ∞.
- Rebatidos: 0.

**Números.**
- Ninguna de las 575 macros de v0.6 cambia de valor, salvo `\SignedSha`: es el prefijo del SHA-256 del log re-congelado y el cambio está documentado abajo.
- Se comprobó por programa, comparando con una copia de `numbers.tex` v0.6.
- Las siete `table_*.tex` quedan idénticas byte a byte.
- Se añaden 5 macros: `\SignedEmptyFinite` = 361, `\SignedEmptyInf` = 39, `\SignedCertOk` = 361, `\SignedCertTies` = 3 y `\SignedTiesEqual` = 3.

---

## M1 (mayor). El caso S(D) = ∅ se presentaba como resuelto → **aceptado**

El árbitro tiene razón. Sin unicidad en las submuestras, la Prop. 5.12 sólo da la cota inferior f^signed ≥ f⁰. La unicidad no es una propiedad genérica en datos enteros, que es el régimen de todas las afirmaciones de complejidad. El árbitro encontró f^signed > f⁰ en 640 de sus 6 877 instancias degeneradas, casi siempre con f^signed = ∞.

En nuestras 400 instancias no aparece ninguna desigualdad estricta (ver m1). Eso se debe a que nuestro generador produce pocas submuestras degeneradas, no a la proposición.

Cambios, con los textos del árbitro y recortes mínimos para no pasar de 14 páginas:

| Lugar | Antes (v0.6) | Ahora (v0.7) |
|---|---|---|
| Resumen | "…open unless nothing is selected on the full data" | "…open, except when nothing is selected on the full data and the minimiser is unique on the relevant subsamples (e.g. continuous designs)" |
| Introducción | "(Proposition 5.12 treats the empty one)" | "(Proposition 5.12 treats the empty one under uniqueness)" |
| Obs. 5.2(iv) | "then it is at least, and under uniqueness equal to, …" | "then it is at least the least of p one-column selection-witness numbers, and equal to it under uniqueness (Proposition 5.12); without uniqueness (e.g. integer data with repeated or tied columns) it can be strict" |
| Tabla 3, fila abierta | "…for p ≥ 2 with S(D) ≠ ∅" | "…with S(D) ≠ ∅, or with S(D) = ∅ without uniqueness" |
| Limitations | "…assumes an empty support on D" | "…assumes an empty support on D and uniqueness on the subsamples" |
| Next steps (a) | "…when S(D) ≠ ∅" | "…when S(D) ≠ ∅, or S(D) = ∅ without uniqueness" |
| CONTINUIDAD (Limitaciones, Pendientes 2, Resultados) | "para p ≥ 2 sólo se resuelve el caso S(D) = ∅" | "…el caso S(D) = ∅ con unicidad en las submuestras (si no, cota inferior)…" |
| README (estado, idea en cuatro líneas), FICHA (es/en: hallazgos y alcance) | "bajo unicidad se calcula"; "sólo se resuelve el caso sin variables seleccionadas" | Cota inferior; igualdad bajo unicidad con un certificado polinomial; puede ser estricta sin unicidad; "…y con unicidad en las submuestras" |

**Añadido: ejemplo mínimo demostrado a mano, tras la prueba de la Prop. 5.12.**
- Sean p = 2 y X_{·1} = X_{·2}, y sea (b₁, b₂) un minimizador no nulo.
- Debe cumplirse b₁b₂ ≥ 0. Si no, (b₁ + b₂, 0) tendría el mismo ajuste y una norma ℓ1 menor.
- Por tanto (b₁ + b₂, 0) y (0, b₁ + b₂) son minimizadores distintos: ninguna submuestra tiene un minimizador no nulo único, y f^signed = ∞.
- Con X_{·1} = X_{·2} = (1, 1, −1)ᵀ, y = (1, 1, 1)ᵀ, μ = 1 y regla C se tiene Xᵀy = (1, 1) y S(D) = ∅. Quitando la fila 3, q = (2, 2), así que f⁰ = 1.
- Es el ejemplo mínimo del informe, ahora con prueba en el texto.

## m1. Condición de igualdad exacta y certificado polinomial R\*_j → **aceptado con matiz**

Matiz: la redacción propuesta ("igualdad sii algún R con |R| = f⁰ y ‖X_Kᵀy_K‖_∞ > μ′ tiene minimizador único") omite el caso f⁰ = ∞. En ese caso no existe tal R, pero la igualdad ∞ = ∞ se cumple. El enunciado dice ahora "iff f⁰ = ∞ or some R …".

**Enunciado (v0.7).**
- f^signed ≥ f⁰ := min_j f⁰_j.
- Hay igualdad sii f⁰ = ∞ o algún R con |R| = f⁰ y ‖X_Kᵀy_K‖_∞ > μ_{|R|} tiene minimizador único en D∖R.
- En particular, hay igualdad si uno de los conjuntos R\*_j que produce la ordenación tiene minimizador único (comprobación polinomial), o si el minimizador es único en toda submuestra (con probabilidad uno para diseños continuos).
- "f⁰ and the R\*_j take O(pn log n) time." El O(pn log n) es ahora el coste de f⁰ y de los R\*_j, no el de f^signed.

**Prueba.** La primera parte de la Prop. 5.12, ya arbitrada, dice que R es testigo sii (1) ‖X_Kᵀy_K‖_∞ > μ′ y (2) el minimizador en D∖R es único.

- Sea B el conjunto de los R no vacíos y propios que cumplen (1), y W ⊆ B el de los que además cumplen (2), es decir, los testigos.
- B es la unión de los B_j = {R : |X_{K,j}ᵀy_K| > μ′}. Con p = 1 el minimizador siempre es único, así que min{|R| : R ∈ B_j} = f⁰_j (Teorema 5.1(b), aplicable porque |X_{·j}ᵀy| ≤ μ). Luego min{|R| : R ∈ B} = f⁰.
- Como W ⊆ B, f^signed = min_W |R| ≥ min_B |R| = f⁰.
- Si f⁰ = ∞, entonces B = ∅, W = ∅ y f^signed = ∞ = f⁰.
- Si f⁰ < ∞, hay igualdad sii W contiene algún R de tamaño f⁰, es decir, sii algún R ∈ B con |R| = f⁰ tiene minimizador único.

**Certificado.**
- Sea j con f⁰_j = f⁰ < ∞, y sean a_ij = x_ij y_i y T_j = Σ_i a_ij.
- La ordenación del Teorema 5.1(b) encuentra el menor k para el que T_j − σ⁻_k > μ_k o T_j − σ⁺_k < −μ_k. Los extremos se alcanzan quitando los k menores a_ij (en el primer caso) o los k mayores (en el segundo).
- R\*_j es ese conjunto, con k = f⁰. Cumple |X_{K,j}ᵀy_K| = |T_j − σ^∓_{f⁰}| > μ_{f⁰}, luego R\*_j ∈ B y |R\*_j| = f⁰.
- Por la primera parte, R\*_j es testigo sii su minimizador es único. Si lo es, f^signed ≤ f⁰ y, con la cota inferior, hay igualdad.

**Coste.**
- La unicidad en D∖R\*_j se decide en tiempo polinomial en la longitud binaria, también con p en la entrada. Es el procedimiento de la prueba de pertenencia a NP del Teorema 5.8: un QP convexo exacto (Kozlov–Tarasov–Khachiyan) seguido de 2p programas lineales sobre el politopo de minimizadores. El rango completo de X_E es una condición suficiente más barata (Tibshirani 2013).
- Las p ordenaciones cuestan O(pn log n), tras O(np) productos. Hay a lo sumo 2p conjuntos R\*_j.
- El certificado es suficiente, no necesario. Si ningún R\*_j tiene minimizador único, otro conjunto de tamaño f⁰ puede tenerlo; en la subcorrida del árbitro, 14 de 410 igualdades no las cierra R\*.

**Código.** `experiments/check_signed_any.py` (parte A) añade los contadores del certificado:
- `rstar_sets` calcula los R\*_j, rompiendo empates de la ordenación por índice de fila.
- `status_xe` resuelve los empates |c_j| = μ′ con la condición de Tibshirani: un punto KKT exacto, el conjunto de equicorrelación E y la comprobación de que G_EE es no singular.
- `exhaustive_signed_xe` repite la búsqueda exhaustiva sólo en las instancias con submuestras empatadas, con el mismo certificado de unicidad.
- Los contadores nuevos no consumen números aleatorios y se registran después de las líneas existentes de la parte A.

Resultados en las 400 instancias:

| Recuento | Valor |
|---|---|
| Instancias con f⁰ = ∞ (igualdad trivial) | 39 |
| Instancias con f⁰ finito | 361 |
| El certificado R\*_j cierra f^signed = f⁰ | **361/361** |
| …de ellas, con submuestras empatadas | 3/3 |
| Desacuerdos con la búsqueda exhaustiva | 0 |
| Instancias empatadas re-buscadas con unicidad por rango de X_E: f^signed = f⁰ | 3/3 |

Así, en las 400 instancias la igualdad queda **certificada**: 39 de forma trivial y 361 por R\*_j.
- v0.6 dejaba 3 instancias con empates sin resolver.
- En una de ellas (ensayo 284 en base 0; p = 3, n = 5, regla C), el comprobador conservador de v0.6 daba un testigo certificado de tamaño 2 frente a f⁰ = 1. Era una cota superior.
- La submuestra que deja fuera R\*_j = {fila 5} tiene un empate exacto (|c₁| = μ′ = 3) pero X_E de rango completo (G_EE = diag(4, 16)): el minimizador es único y f^signed = 1 = f⁰.

**Reproducibilidad.**
- Log re-congelado: SHA-256 `c3e7244d5c447f90…` (v0.6) → `b80f98cc974cbd05…` (v0.7).
- Las 16 líneas del log de v0.6 se conservan idénticas (`diff` contra una copia: sólo 3 líneas insertadas al final de la parte A).
- Las claves antiguas de `signed_any.json` no cambian.
- Dos corridas del código final (una en el repositorio y otra en una copia en el scratchpad) dan el mismo hash. CPU: 3.6 s.
- `make_numbers.py` comprueba el hash y añade las aserciones `cert_fail == 0`, `cert_ok + cert_open == f0_finite` y `f0_finite + f0_infinite == total`.
- El cambio queda documentado en el docstring del script, el Apéndice A ("copies of the derivation-time originals in theory/ (check_signed_any.py adds the counters for R\*_j)"), el README, `results/signed_any_notes.md` (prefijo nuevo y antiguo) y CONTINUIDAD.
- No se tocó `theory/`.

Texto en el Apéndice A: "the certificate R\*_j (uniqueness by full rank of X_E) closes the equality in 361/361 instances with f⁰ < ∞ (3 tied; f⁰ = ∞ in 39), as the exhaustive search confirms". Fila de la Tabla 3: "…; R\*_j closes 361/361".

## m2. Dónde se usa "0 minimizador ⇒ único" → **aceptado**

Frase al final de la prueba: "As 0, when a minimiser, is the only one, the case R = ∅ shows that S(D) is defined and empty iff ‖Xᵀy‖_∞ ≤ μ; the 'iff' above needs no such step, as Definition 2.2 requires uniqueness."

## m3. Etiquetas de estado → **aceptado**

- Tabla 3, fila de la Prop. 5.12: "proved here; checked by internal referee (round 5); verified (exact)".
- README (estado) y CONTINUIDAD: la sección "Queda abierto (tras la ronda 4)" queda anotada con "hecha internamente en la ronda 5"; la nueva sección de la ronda 5 deja sólo la revisión externa.
- Next steps sigue pidiendo "an external review of Theorem 5.8 and Proposition 5.12".
- `results/signed_any_notes.md` sigue como "Not yet refereed" y lo dice expresamente ("Proposition 5.12 itself was checked by the internal referee of round 5; these notes were not").
- Leyenda de la Tabla 3: "Every result marked 'proved here' was checked by internal referees in rounds 1–5 (Theorem 5.1(c), Lemma B.1 and Corollary 5.9 in round 4), not externally".
  - Antes de escribirla se comprobó en los informes 1–4 que cada fila "proved here" fue arbitrada. Por ejemplo, la Obs. 3.5 (stability selection) en la ronda 1.
  - La Prop. 5.12 lo fue en la ronda 5.
- Fila del Teorema 5.8: se añade "and f_enter strongly NP-hard (Cor. 5.9)". Conserva su etiqueta "checked by internal referee (round 4)".
- Fecha del manuscrito: "Working draft v0.7 (five rounds of internal review applied)". Se acortó para no pasar de 14 páginas; el detalle está en la tabla y en su leyenda.

## m4. README :26 → **aceptado**

`REFEREE_TCD001_ronda{1,…,5}_*.md`, `RESPUESTA_TCD001_ronda{1,…,5}_*.md`, "rondas 1–5", con lo que verificó cada ronda. También la fila de CONTINUIDAD ("rondas 1–5") y la lista de rondas del estado.

## m5 (opcional). PL como caso de término cuadrático nulo → **aceptado**

"Convex quadratic programmes with rational data, linear programmes being the case of a zero quadratic term, are solved exactly in time polynomial in their bit length [kozlov1980]". La DOI de `kozlov1980` ya figuraba en la nota de continuidad; no se añadió al .bib.

---

## Extensión

Las adiciones (enunciado, prueba, ejemplo, filas y leyenda de la tabla, Apéndice A) llevaban el PDF a 15 páginas, con unas 11 líneas de referencias en la p. 15. Se recuperaron sin quitar contenido verificable:
- "together with its minimal size" → "(a witness) and its minimal size";
- la frase de comprobación del Teorema 5.1(c), más corta;
- "cover every element exactly once" → "partition the elements";
- "; its review (round 4) was internal" en Limitations, ahora redundante con la leyenda;
- tres filas de la tabla resumidas ("full rank", "checked (Rem. 5.7)", "their one-element supersets");
- la descripción entre paréntesis de las identidades de `results/signed_any_notes.md`, abreviada;
- la línea de fecha y versión.

Resultado: **14 páginas** en letra normal: cuerpo hasta la p. 11, Apéndice A en la p. 11, Apéndice B en pp. 12–14 y referencias en la p. 14.

## Compilación

`latexmk -pdf`, con el resultado siguiente:
- 0 errores y 0 referencias o citas indefinidas;
- bibtex sin avisos;
- 0 cajas Overfull o Underfull;
- `pdftotext main.pdf - | grep -c '??'` = 0;
- 14 páginas.

Se renderizaron y revisaron las páginas 7–8 (Prop. 5.12, prueba y ejemplo) y 10–11 (Limitations, Tabla 3 y Apéndice A). `latexmk -c` deja `main.pdf`.

## CPU

| Paso | CPU |
|---|---|
| `check_signed_any.py`: 4 corridas (2 de desarrollo y 2 del código final con hash idéntico) | ≈ 15 s |
| Repetición de los RNG para inspeccionar las 3 instancias empatadas (scratchpad) | ≈ 4 s |
| `make_numbers.py` | < 2 s |
| Compilaciones | ≈ 25 s |
| **Total** | **< 1 min** |

## Queda abierto

- (i) Revisión externa del Teorema 5.8 y de la Prop. 5.12.
- (ii) ANY con signo para p ≥ 2:
  - con S(D) ≠ ∅;
  - con S(D) = ∅ cuando ningún R\*_j certifica la unicidad. ¿Es difícil decidir si existe un conjunto de tamaño f⁰ que selecciona y tiene minimizador único?
- (iii) Conjetura 5.11.
- (iv) Dureza paramétrica en p.
- (v) Extensión: 14 páginas frente al objetivo de 13.
- (vi) Entradas clásicas de la bibliografía sin verificar en red.
- (vii) `results/signed_any_notes.md` sin arbitrar.
