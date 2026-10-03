# Informe de árbitro interno independiente — TCD001, ronda 5 (03/10/2026)

Árbitro: independiente y nuevo (no participó en las rondas 1–4). Ronda corta de verificación.
Objeto: `manuscript/main.tex` v0.6. Las fuentes de v0.6 coinciden con HEAD (`git diff HEAD` vacío); el commit `34cc081` sólo contiene `main.pdf`, y las fuentes entraron en los commits WIP anteriores (`bd17c93` y previos). Prioridades: (1) Prop. 5.12 (ANY con signo con S(D) = ∅); (2) refuerzo del Teorema 5.8 (unicidad en toda D∖R) y nueva prueba de pertenencia a NP; (3) aplicación de la respuesta a la ronda 4 y etiquetas de estado; (4) compilación.
Trabajo auxiliar (scripts propios, salidas, copia de reproducción): `/tmp/claude-0/-home-user-ChanoSilva/6d28bda3-759e-5faa-92d7-8739680d15c2/scratchpad/referee5_TCD001/`.

## Veredicto

**Cambios menores.** La Prop. 5.12 es correcta tal como está enunciada. Mi fuerza bruta exacta e independiente (6 877 instancias, 216 302 submuestras, ties resueltos y no omitidos) no encuentra ningún fallo. El refuerzo del Teorema 5.8 y la nueva pertenencia a NP también son correctos. Los nueve menores de la ronda 4 están aplicados. Hay un hallazgo mayor, sólo de redacción: el resumen, la Obs. 5.2(iv), la tabla de afirmaciones, Limitations y CONTINUIDAD presentan el caso S(D) = ∅ como resuelto. La Prop. 5.12 sólo lo resuelve bajo unicidad en las submuestras. En datos enteros, que es el régimen de todas las afirmaciones de complejidad, la desigualdad es estricta en el 9 % de mis instancias.

Recuento: 0 bloqueantes, 1 mayor, 5 menores. Ronda 4: 10/10 puntos aplicados (m1–m9 y la acción opcional 8): 9 bien y 1 aceptado con matiz (m8, extensión, 14 páginas en letra normal), que considero justificado.

---

## 1. Verificación de lo nuevo (prioridad 1–2)

### 1.1 Proposición 5.12 (`main.tex:288–293`), paso a paso

| Paso | Qué comprobé | Resultado |
|---|---|---|
| Hipótesis "S(D) = ∅, i.e. ‖Xᵀy‖_∞ ≤ μ" | S(D) sólo está definido si el minimizador en D es único (`:68`). (⇐) Con ‖Xᵀy‖_∞ ≤ μ, 0 es minimizador por el KKT y, por la norma ℓ1 común, el único. (⇒) Si 0 es el minimizador único, el KKT da ‖Xᵀy‖_∞ ≤ μ. | Correcto. Es aquí donde hace falta "0 minimizador ⇒ único" (ver m2). |
| "β = 0 minimiza en D∖R ⇔ ‖X_Kᵀy_K‖_∞ ≤ μ′" | 0 ∈ −q + μ′∂‖·‖₁(0). | Correcto. |
| "Todos los minimizadores comparten ajuste y valor, luego (μ′ > 0) la norma ℓ1" | Tibshirani (2013, Lema 1) da el ajuste común. Con el mismo valor del objetivo, μ′‖β‖₁ = L* − ½‖y_K − Xβ‖² es común. Si 0 es minimizador, la norma común es 0. El argumento funciona aunque X_K tenga núcleo no trivial, donde el ajuste común solo no basta. | Correcto. Comprobado: en las 216 302 submuestras, cada vez que ‖q‖_∞ ≤ μ′ el minimizador 0 resultó único (0 excepciones, incluidas las submuestras con X_K singular y con columnas repetidas o nulas). |
| "Sii ‖q‖_∞ > μ′ y unicidad" | Def. 2.2: testigo ⇔ minimizador único ∧ soporte con signo ≠ (∅, ∅). Bajo unicidad, β̂ ≠ 0 ⇔ ‖q‖_∞ > μ′. | Correcto (0 fallos del "sii" en 216 302 submuestras). |
| Borde μ′ = ‖X_Kᵀy_K‖_∞ exactamente | 0 es minimizador ⇒ no es testigo. Coincide con la desigualdad estricta del Teorema 5.1(b). | Correcto (17 965 submuestras exactamente en el borde, 0 fallos). |
| Reducción a p columnas y f⁰_j | {R : ‖q‖_∞ > μ′} = ∪_j {R : \|X_{K,j}ᵀy_K\| > μ′}. Para p = 1 el minimizador siempre es único, así que f⁰_j es el menor \|R\| de la unión j-ésima, con \|X_{·j}ᵀy\| ≤ μ (hipótesis del 5.1(b)). μ′ depende de \|R\| igual en ambas instancias (regla P incluida). Una columna nula da f⁰_j = ∞. | Correcto. Mi ordenación propia del 5.1(b) coincide con la búsqueda exhaustiva de min \|R\| con ‖q‖_∞ > μ′ en 6 877/6 877 instancias. |
| f^signed ≥ f⁰; igualdad bajo unicidad en toda submuestra | Los testigos son un subconjunto de la unión. Con unicidad en todas las submuestras son exactamente la unión. | Correcto (≥ en 6 877/6 877; igualdad en 4 912/4 912 instancias con unicidad en todas las submuestras). |
| "Con probabilidad uno para diseños continuos" | Tibshirani (2013, Lema 4) vale para un diseño con densidad, cualquier y y cualquier λ > 0. Las submuestras son finitas y cada X_K tiene densidad. | Correcto. |
| "Entonces se calcula en O(pn log n)" | Ordenar cada columna cuesta O(n log n) más O(np) para Xᵀy. Pero el algoritmo calcula f⁰, y que f⁰ = f^signed depende de una promesa (unicidad) que no se comprueba en tiempo polinomial recorriendo submuestras. | Correcto como enunciado condicional. La redacción es mejorable (M1, m1). |

**Casos borde pedidos.**
- X_K con núcleo no trivial: 4 290 submuestras únicas con X_E de rango deficiente y 13 348 no únicas, todas confirmadas construyendo un segundo minimizador exacto.
- μ′ = ‖q‖ exacto: 17 965 submuestras.
- Empates \|x_1\| = \|x_2\| en submuestras con \|K\| = 1, y columnas repetidas, opuestas, escaladas o nulas: tipos `repeat`, `zerocol`, `onerowtie` y `binary`, unas 1 145 instancias cada uno.
- K pequeño: n desde 2, así que \|K\| = 1 aparece siempre.

Sin fallos en ninguno. En los diseños degenerados la desigualdad es **estricta** con frecuencia (§1.3); eso no contradice la proposición, pero limita lo que puede afirmarse de ella (M1).

### 1.2 Refuerzo del Teorema 5.8 (`:273`, prueba `:436`) y pertenencia a NP (`:440`)

| Pieza | Qué comprobé | Resultado |
|---|---|---|
| Enunciado `:273` | "unique minimiser on D∖R for every R ⊊ [n] (so also on D)": R = ∅ está incluido. | Coincide con la prueba. |
| Testigos (todas las anclas, N = q ≥ 1) | Bloque uI en las filas de ancla. X_{K,0} = Σϑ_eX_{K,e} forzaría ϑ_e = κw y κ/q ≠ ρ/q en una tripleta. Rango completo, luego minimizador único. | Correcto (ya arbitrado en la ronda 4). |
| "For every other K" | Recorrí todos los casos. (i) P̄ ≠ ∅. (ii) P̄ = ∅ y P₂ ≠ ∅. (iii) P̄ = P₂ = ∅ con N ≤ q − 1, incluido N = 0, donde γ₀ = μ + θ − ρ < μ. En todos, 0 ≤ γ₀ < μ estrictamente, así que (β, 0) es minimizador por el Lema 5.3(a), con β el del Lema B.1. Con N = q, P̄ = P₂ = ∅ y 3q incidencias sobre 3q elementos, la familia es una partición: no queda ningún caso fuera. El conjunto de equicorrelación es común a todos los minimizadores porque comparten el residuo. 0 ∉ E. Para e ∈ P̄, c_e = cov_e − Σ_{e′}G_ee′β_e′ ∈ [0, m] y m < μ = m + 1, luego E ⊆ P. X_{K,P} contiene uI, así que X_{K,E} tiene rango completo y el minimizador es único (Tibshirani 2013). Sin anclas, P = ∅ ⇒ E = ∅ ⇒ 0 es el único minimizador. | Correcto. |
| D (R = ∅) | 3m > 3q incidencias ⇒ caso (ii) ⇒ \|γ₀\| < μ, X de rango completo ⇒ minimizador único con 0 ∉ S(D). | Correcto. |
| Pertenencia a NP, p en la entrada (`:440`) | (a) El Lasso en (β⁺, β⁻) ≥ 0 es un QP convexo, con Hessiana [G, −G; −G, G] ⪰ 0. Kozlov–Tarasov–Khachiyan dan una solución óptima exacta en tiempo polinomial en la longitud binaria (verificado, §4), y β⁺ − β⁻ es minimizador del Lasso. (b) M = {β : G(β − β̂) = 0, ‖β‖₁ ≤ ‖β̂‖₁} es exactamente el conjunto de minimizadores: todo β de M tiene el mismo ajuste y una norma no mayor, luego un objetivo no mayor. M está acotado y contiene a β̂, así que los 2p PL son factibles y acotados. Su tamaño es polinomial porque ‖β̂‖₁ sale del QP exacto. Unicidad ⇔ max_M β_k = min_M β_k = β̂_k para todo k. (c) Se comprueba β̂_j ≠ 0. | Correcto. Contrasté además mi criterio exacto de unicidad con estos mismos 2p PL (HiGHS, en coma flotante): 2 756/2 756 coincidencias, con 516 casos no únicos y 168 únicos con X_E de rango deficiente. |
| Lectura como problema con promesa | Las condiciones sobre D (minimizador único, j ∉ S(D)) se deciden con el mismo cómputo, así que la promesa está en P. Con una promesa decidible en P, la versión con promesa y el lenguaje "promesa ∧ sí" son polinomialmente equivalentes, y la reducción produce instancias que cumplen la promesa (unicidad en D y 0 ∉ S(D)). "Equivalently" (`:252`) y "alternatively" (`:440`) son coherentes con los enunciados de los Teoremas 5.4 y 5.8. La segunda lectura es redundante, pero inocua. | Correcto. |

### 1.3 Verificación independiente (código propio; no importa nada de `experiments/` ni de `theory/`)

`ref5_signed.py`, escrito sólo a partir del texto de `main.tex`, trabaja en aritmética racional (`fractions`) y hace lo siguiente en cada R no vacío y propio:
- Encuentra un minimizador exacto enumerando soportes con signo A con X_A de rango completo (siempre existe uno así) y comprobando el KKT exactamente.
- Decide la unicidad **exactamente, resolviendo los empates en lugar de saltarlos**. El conjunto de minimizadores es {supp ⊆ E, X_Eβ_E = ajuste, s_jβ_j ≥ 0}. Es único ⇔ no existe d ≠ 0 con X_Ed = 0 y s_jd_j ≥ 0 en E∖supp β̂ (prueba por rayos extremos del cono).
- Confirma cada veredicto "no único" construyendo β̂ + td y comprobando que el objetivo es idéntico.

Calcula f^signed por búsqueda exhaustiva con la Def. 2.2 literal y f⁰ con mi propia ordenación del Teorema 5.1(b). Las instancias tienen p ∈ {2, 3}, n ∈ {2, …, 7} y ambas reglas, y son de seis tipos:
- `small`: enteros en {−2, …, 2};
- `cont`: racionales con denominadores hasta 97;
- `repeat`: columna 1 = ±columna 0 o 2·columna 0;
- `zerocol`: una columna nula;
- `binary`: diseños 0/1;
- `onerowtie`: \|x_1\| = \|x_2\| en cada fila.

μ se elige de tres maneras: μ = ‖Xᵀy‖_∞ (empate en D); μ igual a un valor \|X_{K,j}ᵀy_K\| de una submuestra, reescalado según la regla, para forzar μ′ = ‖q‖ exacto; o μ libre. A eso se suman 6 casos fijos adversariales (columnas duplicadas; empate con \|K\| = 1; y = 0 en D). Semilla 55555.

| Medida | Resultado |
|---|---|
| Instancias / submuestras | 6 877 / 216 302 (50 s de CPU) |
| Unicidad: rango completo de X_E / única con X_E de rango deficiente / no única (confirmada construyendo otro minimizador) | 72 353 / 4 290 / 13 348 |
| ‖q‖_∞ ≤ μ′ con minimizador 0 no único | **0** |
| Fallos del "sii" de la Prop. 5.12 | **0** |
| Ordenación (5.1(b)) frente a búsqueda exhaustiva de f⁰ | 6 877/6 877 |
| f^signed ≥ f⁰ | 6 877/6 877 |
| Igualdad en instancias con unicidad en toda submuestra | 4 912/4 912 |
| Instancias con alguna submuestra no única | 1 965. Igualdad en 1 325; **f^signed > f⁰ en 640** (9.3 % del total), casi siempre con f^signed = ∞ |
| Subcorrida de 15 s (`ref5_signed_v2.py`, mismo generador) | De 602 instancias con no unicidad: 410 con igualdad, de las cuales **396 quedan certificadas porque el R\* que produce la ordenación tiene minimizador único** (base de m1); 192 estrictas, 18 de ellas con f^signed finito |
| Contraste del criterio exacto de unicidad con los 2p PL de `:440` (`ref5_lpcross.py`, 25 s) | 2 756/2 756 |

Ejemplo mínimo de desigualdad estricta (caso fijo): X = [[1,1],[1,1],[−1,−1]], y = (1,1,1), μ = 1, regla C. En D, q = (1, 1), así que S(D) = ∅. f⁰ = 1 (se quita la fila 3), pero las dos columnas son iguales: toda submuestra con ‖q‖_∞ > μ tiene minimizadores no únicos, y f^signed = ∞.

---

## 2. Verificación de la respuesta a la ronda 4

| Id (ronda 4) | Estado | Evidencia |
|---|---|---|
| m1 "not yet refereed" | aplicado bien | `main.tex:49` (fecha y versión), `:280` (Obs. 5.10), `:363` (tabla: "proved here; checked by internal referee (round 4); verified (exact)"), `:375` ("its review (round 4) was internal"), `:377` ("an external review of …"); README `:5`, `:37`, `:74`; FICHA `:3`, `:13`, `:22`, `:24`; CONTINUIDAD `:43`, `:51`, `:161`, `:169`. Se mantiene [proved here]. Ver m3 sobre la coherencia de etiquetas. |
| m2 Apéndice A | aplicado bien | `:383`: "uniqueness certified on every subsample, as Theorem 5.8 asserts". |
| m3 unicidad en toda submuestra | aplicado bien | Enunciado `:273`, prueba `:436` y tabla `:363`. Correcto (§1.2). |
| m4 NP sin certificados duales; promesa | aplicado bien | `:440` (KTK 1980; QP exacto y 2p PL), `:252` ("equivalently … promise problem"). Correcto (§1.2). `kozlov1980` está en `refs.bib:107` y verificado (§4). |
| m5 Corolario 5.9 | aplicado bien | `:276`: μ incluido en M; "cannot be made polynomial in (n, p, M)"; FPT en p "not addressed". |
| m6 esquema | aplicado bien | `:270`: "a missing anchor costs a fixed amount in the target correlation, and an absorber without its anchor stays inactive because μ exceeds every coverage". Correcto. |
| m7 Conjetura 5.11 | aplicado bien | `:284` sin "{−1,0,1}"; `:286`: "Whether data in {−1,0,1} suffice is open, even for Theorem 5.8". |
| m8 extensión y cuerpo de letra | aplicado con matiz (aceptado) | `\footnotesize` del Apéndice B, `\small` del A y `\enlargethispage` eliminados (diff contra `31fbabf`). Recortes (a)–(f) hechos: prueba de la Prop. 3.1(b) condensada (la rehíce: A′⁻¹U = V_Rᵀ(I − H_R)⁻¹ y r_R + H_Re_R = e_R, correcto), Figura 1 al 64 %. Resultado: 14 páginas. Lo considero aceptable: la Prop. 5.12 ocupa ≈ ¼ de página y es contenido nuevo; el resto son pruebas completas. |
| m9 instancias fijas | aplicado bien | `:417`. Comprobado: con q = 1 y C = (U, U), m = 2 > q y quitar una de las dos copias deja una cubierta (R = {2} es uno de los dos testigos). Con q = 2, los seis pares se cortan (en 2, 1, 0, 4, 3, 5). Ambas cumplen m > q. |
| Acción 8 (`moitra2022`) | aplicado bien | `refs.bib:100`: `@inproceedings`, ICLR 2023, arXiv en `note`. |

Recuento: 9 bien aplicados, 1 con matiz justificado, 0 a medias, 0 no aplicados, 0 con error nuevo.

---

## 3. Hallazgos nuevos

### Bloqueantes

Ninguno.

### Mayores

**M1. El caso S(D) = ∅ se presenta como resuelto, pero la Prop. 5.12 sólo lo resuelve bajo unicidad en las submuestras.**

Ubicaciones:
- Resumen `:56`: "the signed fragility number for p≥2 is open unless nothing is selected on the full data".
- Obs. 5.2(iv) `:240`: "Its complexity for p≥2 is open (…), except when nothing is selected on D".
- Tabla `:365`: la fila abierta dice "with S(D)≠∅", lo que da a entender que S(D) = ∅ está cerrado.
- Limitations `:375`: "whose only algorithmic result for p≥2 assumes an empty support on D".
- CONTINUIDAD `:43`: "para p ≥ 2 sólo se resuelve el caso S(D) = ∅".
- Introducción `:63`: "Proposition 5.12 treats the empty one" (aceptable, pero conviene alinearla).

Problema: sin unicidad, la Prop. 5.12 sólo da una cota inferior. La hipótesis "unique on every subsample" no se comprueba en tiempo polinomial recorriendo submuestras. Además, falla con frecuencia precisamente en datos enteros, el régimen de todas las afirmaciones de complejidad del artículo (Teoremas 5.1, 5.4 y 5.8; Prop. 5.5). Evidencia (§1.3): en 640 de 6 877 instancias con S(D) = ∅ se tiene f^signed > f⁰, casi siempre con f^signed = ∞. Así que la complejidad de f^signed con S(D) = ∅ en general (datos enteros, sin promesa de unicidad) no queda establecida.

Corrección (sólo texto):
- Resumen: "…the signed fragility number for $p\ge2$ is open, except when nothing is selected on the full data and the minimiser is unique on the relevant subsamples (e.g.\ continuous designs)".
- Obs. 5.2(iv): "…except when nothing is selected on $D$: then it is at least the least of $p$ one-column selection-witness numbers, and equal to it under uniqueness (Proposition~\ref{prop:signed-empty}); without uniqueness, as in integer data with repeated or tied columns, the inequality can be strict".
- Tabla `:365`: "complexity of the signed $f_{\tsc{any}}$ for $p\ge2$ with $S(D)\ne\emptyset$, or with $S(D)=\emptyset$ without uniqueness".
- Limitations: "…assumes an empty support on $D$ and uniqueness on the subsamples".
- CONTINUIDAD `:43`: "para p ≥ 2 sólo se resuelve el caso S(D) = ∅ con unicidad en las submuestras (si no, cota inferior)".

### Menores

**m1. Prop. 5.12: afinar la condición de igualdad y el "O(pn log n)" (`:289`).** La igualdad se da sii algún R con \|R\| = f⁰ y ‖X_Kᵀy_K‖_∞ > μ′ tiene minimizador único. Hay además un certificado polinomial que no necesita unicidad global. La ordenación produce, para cada j con f⁰_j = f⁰, un conjunto concreto R\*_j: se quitan las f⁰ filas con a_ij = x_ijy_i más pequeñas o más grandes. Si el minimizador en D∖R\*_j es único, cosa que se decide en tiempo polinomial (prueba de `:440`, o rango de X_E), entonces f^signed = f⁰. En mi subcorrida, este certificado cerró 396 de los 410 casos de igualdad con submuestras no únicas.

Texto propuesto: "…equality holds iff some $R$ with $|R|=f^0$ and $\lVert X_K^{\top}y_K\rVert_\infty>\mu'$ has a unique minimiser, in particular if the minimiser is unique on $D\setminus R^\ast_j$ for one of the removal sets $R^\ast_j$ produced by the sort (checked in polynomial time), or on every subsample (with probability one for continuous designs). $f^0$ and the sets $R^\ast_j$ are computed in $O(pn\log n)$ time."

**m2. Prop. 5.12: dónde se usa "0 minimizador ⇒ único".** Para el "sii" no hace falta, porque la Def. 2.2 ya exige unicidad. Hace falta para que "S(D) = ∅, i.e. ‖Xᵀy‖_∞ ≤ μ" sea una equivalencia bien definida, ya que S(D) sólo se define con minimizador único. Una frase al final de la prueba: "(on $D$ the same argument shows that $S(D)=\emptyset$ iff $\lVert X^{\top}y\rVert_\infty\le\mu$)". Es opcional, pero evita que el lector busque el uso de ese paso.

**m3. Etiquetas de estado tras esta ronda, y su coherencia.**

Cambios por la ronda 5:
- Cambiar "not yet refereed" de la Prop. 5.12 por "proved here; checked by internal referee (round 5); verified (exact)" en la tabla `:364`.
- README `:5` ("aún no revisada") y CONTINUIDAD `:182` ("revisión de la Prop. 5.12"); en Next steps `:377` basta la revisión externa.
- `results/signed_any_notes.md` debe seguir como "not yet refereed": en esta ronda sólo lo hojeé y no lo verifiqué.

Coherencia:
- La etiqueta "checked by internal referee (round 4)" sólo aparece en la fila del Teorema 5.8. Sin embargo, el Teorema 5.1(c), el Lema B.1 y el Corolario 5.9 también se arbitraron en la ronda 4, y el resto de filas en las rondas 1–3.
- O se etiqueta todo, o se añade a la leyenda de la Tabla 3: "All proved results were checked by internal referees (rounds 1–5) unless marked otherwise". Esta segunda opción es más corta.
- El Corolario 5.9 no figura en la tabla: añadir "and $f_{\tsc{enter}}$ strongly NP-hard (Cor.~\ref{cor:strong-f})" a la fila `:363`.

**m4. README `:26`.** La tabla de archivos sigue diciendo `REFEREE_TCD001_ronda{1,2,3}` / "rondas 1–3". Debe pasar a `{1,…,5}`.

**m5. Cita de la programación lineal (`:440`).** "Linear and convex quadratic programmes … [kozlov1980]" es correcto porque la PL es el caso de término cuadrático nulo, pero conviene decirlo: "(linear programmes being the case of a zero quadratic term)". Otra opción es citar a Khachiyan (1979) para la PL. Opcional.

### Lectura de lo cambiado (sin más hallazgos)

Releí lo modificado en v0.6:
- resumen e introducción;
- la Obs. 5.2(iv);
- la Prop. 5.12 y el párrafo que la sigue;
- el Teorema 5.8 y el Corolario 5.9;
- la Obs. 5.10 y la Conjetura 5.11;
- la prueba de la Prop. 3.1(b) condensada;
- E2/E3 recortados;
- tabla, Limitations, Next steps y Apéndices A–B.

La notación es coherente (μ′, K, f⁰_j). La referencia a `results/signed_any_notes.md` describe bien su alcance ("they are not bounds"). No hay sobreafirmaciones nuevas aparte de M1.

---

## 4. Bibliografía

| Entrada | Estado | Corrección |
|---|---|---|
| `kozlov1980` (nueva) | Verificada por búsqueda web: [mathnet.ru](http://www.mathnet.ru/eng/zvmmf5189) y [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/0041555380900981). M. K. Kozlov, S. P. Tarasov, L. G. Khachiyan, "The polynomial solvability of convex quadratic programming", U.S.S.R. Comput. Math. Math. Phys. 20(5) (1980) 223–228; original en Zh. Vychisl. Mat. Mat. Fiz. 20:5, 1319–1323; DOI 10.1016/0041-5553(80)90098-1. El resumen habla de un algoritmo exacto de QP con trabajo polinomial en la longitud binaria, que es lo que usa `:440`. | Ninguna. Opcional: añadir la DOI. |
| `moitra2022` | `@inproceedings`, ICLR 2023 (verificada en las rondas 3 y 4). | Ninguna. |
| `tibshirani2013` (nuevo uso en la Prop. 5.12) | La Prop. 5.12 usa el ajuste común (Lema 1) y la unicidad c.s. para diseños continuos (Lema 4); ambos están en el artículo. | Ninguna. |

---

## 5. Verificación computacional

| Qué | CPU | Resultado |
|---|---|---|
| `ref5_signed.py` (propio; prueba de 8 s y corrida principal de 50 s) | 58 s | §1.3: 0 fallos del "sii", de la desigualdad, de la igualdad bajo unicidad, de la ordenación y de "0 ⇒ único"; 640 casos estrictos en datos degenerados. |
| `ref5_signed_v2.py` (mismo generador, contadores de R\*) | 15 s | 396/410 igualdades certificadas por R\* (m1). |
| `ref5_lpcross.py` (criterio exacto de unicidad frente a los 2p PL de `:440`) | 25 s | 2 756/2 756. |
| Reproducción de `experiments/check_signed_any.py` en una copia (`repro/`) | 3.6 s | Log **idéntico** (SHA-256 `c3e7244d5c447f90…`, `diff` vacío); `signed_any.json` igual salvo `meta`. Coincide con `\SignedEmptyTotal` = 400, `\SignedEmptyGe` = 400, `\SignedEmptyClean` = 397, `\SignedEmptyAgree` = 397 y `\SignedEmptyTies` = 3 (`numbers.tex:570–576`). Su comprobador es conservador: no resuelve las 3 instancias con empates, y su "≥ en 400/400" usa testigos certificados, es decir, una cota superior de f^signed. Mi corrida resuelve los empates exactamente. |
| `latexmk -pdf` en una copia | 4 s | 0 errores, 0 citas o referencias indefinidas, 0 "??" en el texto del PDF, 0 Overfull, 0 Underfull, bibtex sin avisos, 27 referencias, **14 páginas**. |

CPU total de la ronda ≈ 1.8 min (≤ 3 min). La reproducción del autor coincidió exactamente.

---

## 6. Lista final de acciones (por prioridad)

1. Acotar el alcance del caso S(D) = ∅ a "con unicidad en las submuestras" en el resumen `:56`, la Obs. 5.2(iv) `:240`, la tabla `:365`, Limitations `:375` y CONTINUIDAD `:43`, con los textos de M1.
2. Reescribir la última frase del enunciado de la Prop. 5.12 con la condición de igualdad exacta y el certificado polinomial R\*_j (m1), y añadir la frase sobre S(D) = ∅ en D (m2).
3. Cambiar el estado de la Prop. 5.12 a "checked by internal referee (round 5)" en la tabla, README `:5` y CONTINUIDAD `:182`. Dejar `results/signed_any_notes.md` como "not yet refereed" (m3).
4. Unificar las etiquetas de revisión de la tabla mediante una frase en la leyenda y añadir el Corolario 5.9 a la fila del Teorema 5.8 (m3).
5. Actualizar README `:26` a las rondas 1–5 (m4).
6. Opcional: precisar que la PL es el caso de término cuadrático nulo en `:440` (m5).
