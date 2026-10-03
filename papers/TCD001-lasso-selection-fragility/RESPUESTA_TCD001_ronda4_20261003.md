# Respuesta del autor — TCD001, ronda 4 de revisión interna (03/10/2026)

Objeto: informe `REFEREE_TCD001_ronda4_20261003.md` (cambios menores; 0 bloqueantes, 0 mayores, 9 menores; Teorema 5.8, Lema B.1, Corolario 5.9 y Teorema 5.1(c) confirmados correctos; dureza fuerte verificada como fuerte) e integración concisa del avance parcial de `theory/` sobre el objetivo ANY con signo para p ≥ 2 (`signed_any.tex`, `signed_any_derivation.md`, `check_signed_any.py`). Versión resultante: borrador v0.6 (3 October 2026).

## Resumen

- **Recuento:** 9 hallazgos menores → 8 aceptados, 1 aceptado con matiz (m8, extensión), 0 rebatidos. Acción opcional 8 (`moitra2022` como `@inproceedings`): aceptada. No hay bloqueantes ni mayores.
- **Teorema 5.8:** reforzado (m3) a "minimizador único en D∖R para todo R ⊊ [n]", verificado a mano; la comprobación por programa ya estaba en la corrida congelada de `check_strong.py` (unicidad certificada por rango de X_E en las 81 840 submuestras). Estado: "proved here; checked by an independent internal referee (round 4)".
- **Integración de `theory/` (B):** sólo la Prop. 5.12 (ANY con signo con S(D) = ∅) entra en el cuerpo, con prueba corta y una frase en la Obs. 5.2(iv); el Lema de Cauchy–Binet y la observación sobre los gadgets van a `results/signed_any_notes.md`. La complejidad del ANY con signo para p ≥ 2 con S(D) ≠ ∅ sigue abierta, y así se dice.
- **Números:** ninguna de las 568 macros previas cambia de valor (comprobado por programa contra una copia de `numbers.tex` v0.5); se añaden 7 (`\SignedEmptyTotal` = 400, `\SignedEmptyGe` = 400, `\SignedEmptyClean` = 397, `\SignedEmptyAgree` = 397, `\SignedEmptyTies` = 3, `\SignedSeconds` = 4, `\SignedSha` = `c3e7244d5c447f90`). No se volvió a correr ningún experimento E0–E5 ni `check_strong.py`/`check_hardness.py`.
- **Compilación:** 14 páginas (v0.5: 13 con el Apéndice B en `\footnotesize`, el A en `\small` y `\enlargethispage`); ahora todo el texto en letra normal y sin `\enlargethispage`. 0 errores, 0 referencias o citas indefinidas, 0 "??", 0 Overfull, 0 Underfull (los 2 Underfull conocidos de la tabla de afirmaciones desaparecen con `\raggedright` en la columna de estado), bibtex sin avisos; 27 referencias.

## Verificación propia de la Proposición 5.12 (theory/ → main.tex)

Enunciado: p ≥ 1, cualquier regla, S(D) = ∅ (‖Xᵀy‖_∞ ≤ μ). Un R ≠ ∅ propio es testigo ANY con signo sii ‖X_Kᵀy_K‖_∞ > μ′ y el minimizador en D∖R es único; f^signed ≥ f⁰ := min_j f⁰_j (f⁰_j: número de testigo de selección de la instancia de una columna (X_{·j}, y, μ), Teorema 5.1(b)), con igualdad si hay unicidad en toda submuestra; entonces O(pn log n).

| Paso | Comprobación | Resultado |
|---|---|---|
| β = 0 minimizador ⇔ ‖q‖_∞ ≤ μ′ | KKT: 0 ∈ −q + μ′∂‖·‖₁(0). | Correcto. |
| "Si 0 es minimizador, es el único" | **Qué comparten los minimizadores.** Todos los minimizadores del Lasso comparten el ajuste Xβ (Tibshirani 2013, Lema 1) y, como comparten también el valor del objetivo, comparten μ′‖β‖₁ y por tanto (μ′ > 0) la norma ℓ1. Si 0 es minimizador, la norma común es 0, luego todo minimizador es β = 0. El argumento necesita la norma ℓ1 compartida: el ajuste común Xβ = 0 por sí solo no basta cuando X_K tiene núcleo. El texto de `theory/` decía "share the fit and the ℓ1 norm"; en el manuscrito escribo "share the fit and the objective value, hence, as μ′ > 0, the ℓ1 norm", que hace explícito de dónde sale. | Correcto. |
| Si ‖q‖_∞ > μ′ | Ningún minimizador es 0, el soporte con signo deja de ser (∅, ·); R es testigo sii el minimizador es único (Def. 2.2). | Correcto. |
| Reducción a p columnas | {R : ‖q‖_∞ > μ′} = ∪_j {R : \|X_{K,j}ᵀy_K\| > μ′}; el mínimo sobre la unión es el mínimo de los mínimos; con p = 1 el minimizador siempre es único, así que f⁰_j es exactamente el menor \|R\| con \|X_{K,j}ᵀy_K\| > μ′, y \|X_{·j}ᵀy\| ≤ μ por hipótesis, que es la situación del Teorema 5.1(b). μ′ depende de \|R\| igual en ambas instancias (regla P incluida). | Correcto. |
| Igualdad bajo unicidad | Si el minimizador es único en toda submuestra, testigos = {R : ‖q‖_∞ > μ′}. Para diseños continuos, cada X_K está en posición general c.s. (finitas submuestras) y el minimizador es único (Tibshirani 2013). | Correcto. |

Verificación computacional: `theory/check_signed_any.py` se volvió a correr **en una copia** (scratchpad): log y JSON idénticos a los de `theory/` (3.6 s de CPU). Para congelarlo como `check_strong.py`, `experiments/check_signed_any.py` es una copia con los mismos cálculos y semilla (sólo cambian las rutas de salida y se añade el bloque `meta`): log `results/check_signed_any_output.txt` idéntico al de `theory/` (`diff` vacío), SHA-256 `c3e7244d5c447f90…` en `results/check_signed_any_output.sha256`, recuentos de `results/signed_any.json` idénticos a `theory/signed_any_results.json`; `make_numbers.py` comprueba el SHA, que el log no tiene líneas de tiempo, y con aserciones que f^signed ≥ f⁰ en todas, la igualdad en todas las certificadas y las identidades de las notas. Resultado: 400 instancias con S(D) = ∅ (p ∈ {2, 3}, n ≤ 8, ambas reglas): f^signed ≥ f⁰ en 400/400; igualdad en 397/397 instancias con todas las submuestras certificadas (3 con submuestras empatadas, no certificadas por el comprobador conservador).

También rehíce a mano el Lema de Cauchy–Binet (G₁₁(c₂ − μ′) = (G₁₁q₂ − G₁₂q₁) + μ′(G₁₂ − G₁₁), con G₁₁q₂ − G₁₂q₁ = det([X₁, X₂]ᵀ[X₁, y]) = Σ_{i<l} m_il m′_il; forma de ítems e y₁(NΣb² − σ²)) y la identidad del gadget X3C (push-through con C_K1 = 3·1); ambas correctas. Van a `results/signed_any_notes.md` (en inglés, con pruebas, estado "proved here (identities); not bounds; not yet refereed" y los recuentos del JSON), no al PDF: no cabían en el Apéndice B sin pasar de 14 páginas.

## Hallazgos menores

| Id | Decisión | Qué se cambió y dónde |
|---|---|---|
| m1 | Aceptado | `main.tex`: fecha/versión ("v0.6 (four rounds of internal review applied; strong hardness with growing p proved here and checked by an independent internal referee in round 4)"); Obs. 5.10 ("Theorem 5.8 was checked by an independent internal referee (round 4), by hand and with a separate exact computation"); tabla de afirmaciones ("proved here; checked by internal referee (round 4); verified (exact)"); Limitations ("its review (round 4) was internal"); Next steps (a) ("an external review of Theorem 5.8 and Proposition 5.12" en lugar de "have Theorem 5.8 refereed"). README `:5`, `:36`; FICHA `:3`, `:11`, `:14`, `:22`, `:24`, `:25`; CONTINUIDAD (título, `:43`, `:51`, nota al "Queda abierto" de la ronda 3, sección nueva). Se mantiene [proved here]. En el texto no cito las cifras del árbitro (30 instancias, 85 956 submuestras) porque no salen de los scripts del repositorio; sí están, atribuidas, en README y CONTINUIDAD. |
| m2 | Aceptado | Apéndice A: "uniqueness certified on every subsample, as Theorem 5.8 asserts". |
| m3 | Aceptado | Verificación propia: para K que no es testigo, los casos (i)–(iii) dan \|γ₀\| < μ estrictamente (incluido N = 0 con anclas: γ₀ = μ + θ − ρ < μ, E = ∅), así que (β, 0) es minimizador por el Lema 5.3(a), con correlaciones c_e y γ₀; para e ∈ P̄, c_e ∈ [0, cov_e] ⊆ [0, m] y m < μ = m + 1, luego el conjunto de equicorrelación (común a todos los minimizadores, porque comparten el ajuste) cumple E ⊆ P; X_{K,P} contiene en las filas de ancla el bloque uI, luego X_E tiene rango completo y el minimizador es único (Tibshirani 2013). En los testigos (y con N ≥ 1 y todas las anclas) X_K tiene rango completo. Cambios: Teorema 5.8 "on instances with a unique minimiser on D∖R for every R ⊊ [n] (so also on D)"; en "Uniqueness and the witnesses" las dos frases propuestas; fila de la tabla de afirmaciones. Comprobación por programa: ya presente en la corrida congelada de `check_strong.py` (`uncertified = 0` en 81 840 submuestras, unicidad por rango de X_E del Lasso completo, aserción en `make_numbers.py`); no hizo falta tocar el script ni su SHA. |
| m4 | Aceptado | (a) Pertenencia a NP con p en la entrada reescrita sin certificados duales: el certificado es R; los programas lineales y cuadráticos convexos con datos racionales se resuelven exactamente en tiempo polinomial en su longitud binaria (Kozlov, Tarasov y Khachiyan 1980), así que el verificador calcula un minimizador β̂ (el Lasso es un QP convexo en (β⁺, β⁻)), decide la unicidad con los 2p LP y comprueba β̂_j ≠ 0. (b) "The same computation checks the conditions on D; alternatively, Selection-Witness is read as a promise problem, whose promise the reduction satisfies"; y tras el Teorema 5.4: "The conditions on D are checked in polynomial time (proof of membership in NP) … equivalently, the problem may be read as a promise problem". **Cita verificada** por búsqueda (mathnet.ru y ScienceDirect): M. K. Kozlov, S. P. Tarasov, L. G. Khachiyan, "The polynomial solvability of convex quadratic programming", USSR Computational Mathematics and Mathematical Physics 20(5) (1980) 223–228 (original: Zh. Vychisl. Mat. Mat. Fiz. 20:5, 1319–1323), DOI 10.1016/0041-5553(80)90098-1; el resumen describe un algoritmo exacto de QP con trabajo polinomial en la longitud binaria. Añadida a `refs.bib` como `kozlov1980` (sin DOI, como el resto). |
| m5 | Aceptado | Corolario 5.9: "no algorithm runs in time polynomial in n, p and M = max_{i,j}(\|x_ij\|, \|y_i\|, μ) (integer data and μ), so the bound of Proposition 5.5 cannot be made polynomial in (n, p, M). Whether a bound g(p)·poly(n, M) is possible (fixed-parameter tractability in p for unary data) is not addressed." |
| m6 | Aceptado | Esquema del cuerpo (acortado por m8(b)): "a missing anchor costs a fixed amount in the target correlation, and an absorber without its anchor stays inactive because μ exceeds every coverage". |
| m7 | Aceptado | Conjetura 5.11 sin "already for data in {−1,0,1} up to a common scale"; en el párrafo siguiente: "Whether data in {−1,0,1} suffice is open, even for Theorem 5.8." |
| m8 | Aceptado con matiz | Quitados `\footnotesize` del Apéndice B, `\small` del Apéndice A y `\enlargethispage` (letra normal en todo el texto; tablas, leyendas y bibliografía conservan su cuerpo). Recortes: (a) E3 sin las 12 cifras de exactitud que repite la Tabla 2 (queda la conclusión, el exceso máximo, los errores estándar y k_pred); (b) esquema de la dureza fuerte en tres frases; (c) Obs. 5.10 en dos frases con remisión al Apéndice A; (d) E2 sin los porcentajes de tipos de cambio (remisión a `results/fragility.md`, que los tiene por celda; las macros siguen definidas); (e) Obs. 3.5: las dos últimas frases en una; (f) prueba de la Prop. 3.1 (b) en cuatro líneas (A′⁻¹ = A⁻¹ + V_Rᵀ(I − H_R)⁻¹V_R, A′⁻¹Uᵀ = V_Rᵀ(I − H_R)⁻¹ porque V_RUᵀ = H_R, A′⁻¹s = z; rehecha a mano). Además: resumen, segundo párrafo de la introducción y Limitations más cortos; Figura 1 al 64 % del ancho. **Matiz:** 14 páginas, no 13. Devolver ambos apéndices a letra normal cuesta ≈ 1.5 páginas y la Prop. 5.12 ≈ 0.25; los recortes recuperan ≈ 1. La p. 14 tiene el final de la prueba del Cor. 5.9 y la bibliografía (≈ 45 % de página); llegar a 13 exigiría quitar ≈ 30 líneas de contenido (no de redundancia), lo que no hice. Con el Apéndice B en `\small` (propuesta del árbitro) cabría en 13, pero el encargo pide letra normal en todo el documento. |
| m9 | Aceptado | "with U = {0,…,3q−1}, we output the construction below for q = 1, C = (U, U) (yes; witness R = {2}) or for q = 2, C = ({0,1,2},{2,3,4},{1,4,5},{0,3,5}) (no: any two of these sets meet)". Comprobado: los seis pares del segundo ejemplo se cortan (en 2, 1, 0, 4, 3, 5). |
| Acción 8 (opcional) | Aceptado | `moitra2022` pasa a `@inproceedings`, ICLR 2023, con arXiv en `note` (la clave no cambia). |

## Integración de `theory/` (B): qué entra y dónde

- **Cuerpo:** Proposición 5.12 (enunciado y prueba de cuatro frases) al final de la Sección 5, tras el párrafo que sigue a la Conjetura 5.11; una frase que remite a `results/signed_any_notes.md` para el caso S(D) ≠ ∅ ("two identities … that explain why the gadgets of Theorems 5.4 and 5.8 do not adapt to the signed target; they are not bounds").
- **Obs. 5.2(iv):** "… except when nothing is selected on D: then it is at least, and under uniqueness equal to, the least of p one-column selection-witness numbers (Proposition 5.12)". Resumen e introducción: "open unless nothing is selected on the full data".
- **Apéndice A:** la comprobación exacta de la Prop. 5.12 con las macros (`\SignedEmptyGe/\SignedEmptyTotal`, `\SignedEmptyAgree/\SignedEmptyClean`, `\SignedEmptyTies`, `\SignedSeconds`, `\SignedSha`).
- **Tabla de afirmaciones:** fila nueva "Signed f_ANY for any p when S(D) = ∅: at least f⁰, equal under uniqueness, O(pn log n) (Prop. 5.12); exhaustive check, 397/397 instances — proved here; verified (exact); not yet refereed"; la fila abierta dice ahora "complexity of the signed f_ANY for p ≥ 2 with S(D) ≠ ∅ — conjectural; open".
- **Limitations:** "No hardness result covers the signed ANY target of the experiments, whose only algorithmic result for p ≥ 2 assumes an empty support on D". **Next steps (a):** "Settle the complexity of the signed fragility number for p ≥ 2 when S(D) ≠ ∅ …".
- **Fuera del PDF:** Lema de Cauchy–Binet y observación sobre los gadgets → `results/signed_any_notes.md`. Las rutas exploradas y no cerradas (§4–§5 de la derivación) no se mencionan en el manuscrito; quedan en `theory/signed_any_derivation.md` y en CONTINUIDAD como pistas.
- `theory/` no se modificó.

## Bibliografía

| Entrada | Estado | Acción |
|---|---|---|
| `kozlov1980` (nueva) | Verificada por búsqueda (mathnet.ru, ficha del artículo; ScienceDirect, pii 0041555380900981): autores, título, revista, vol. 20(5), pp. 223–228, 1980; resumen: algoritmo exacto de QP con trabajo polinomial en la longitud binaria. | Citada en la pertenencia a NP con p en la entrada (m4). |
| `moitra2022` | Verificada en la ronda 3 y por el árbitro de la ronda 4 (ICLR 2023). | `@inproceedings`, ICLR 2023. |
| Resto | Sin cambios; las clásicas siguen "no verificadas en red" (CONTINUIDAD). | — |

## Cómputo y compilación

| Paso | CPU |
|---|---|
| `theory/check_signed_any.py` en una copia (scratchpad); `diff` del log y comparación del JSON con `theory/`: idénticos | 3.6 s |
| `experiments/check_signed_any.py` (copia congelada; log idéntico, SHA `c3e7244d…`) | 3.7 s |
| `make_numbers.py` (varias veces) + comparación programática de macros con v0.5 (568 iguales, 7 nuevas) | < 10 s |
| `latexmk` (≈ 6 compilaciones, incluidas pruebas de paginación) | ≈ 25 s |
| **Total** | **≈ 45 s** |

Páginas: 13 (v0.5, apéndices en letra menor, `\enlargethispage`) → 15 (primer intento de v0.6 con letra normal) → **14** (v0.6 tras los recortes). Revisé visualmente las páginas cambiadas: Sección 5 (Teorema 5.8, Cor. 5.9, Obs. 5.10, Conj. 5.11, Prop. 5.12; p. 7), Figura 1 y tabla de afirmaciones (p. 10), Limitations/Next steps/Apéndice A (p. 11) y Apéndice B (pp. 12–14). `latexmk -c` deja `main.pdf`.

## Lo que queda abierto

1. Revisión externa (no interna) del Teorema 5.8; revisión de la Prop. 5.12 (nueva en v0.6, "not yet refereed").
2. Complejidad del número de fragilidad con signo para p ≥ 2 con S(D) ≠ ∅ (fijo o en la entrada); rutas candidatas no cerradas en `theory/signed_any_derivation.md` §4–§5.
3. Conjetura 5.11, y si bastan datos en {−1, 0, 1} (incluso para el Teorema 5.8).
4. Dureza paramétrica en p (W[1]) o algoritmo g(p)·poly(n, M) con datos unarios.
5. Extensión: 14 páginas con letra normal frente al objetivo de 13.
6. Las entradas bibliográficas clásicas siguen sin verificar en red.
