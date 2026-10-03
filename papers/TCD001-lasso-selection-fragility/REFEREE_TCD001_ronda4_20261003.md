[EN CURSO]

# Informe de árbitro interno independiente — TCD001, ronda 4 (03/10/2026)

Árbitro: independiente y nuevo (no participó en las rondas 1–3).
Objeto: `manuscript/main.tex` v0.5 (commit `31fbabf`). Prioridad: Teorema 5.8 (dureza fuerte con p en la entrada, regla C), Lema B.1, Corolario 5.9, Obs. 5.10, Conjetura 5.11 revisada, Apéndice B, y Teorema 5.1(c) (ANY con signo, p = 1). Después: respuesta a la ronda 3 (`RESPUESTA_TCD001_ronda3_20261003.md`), lectura fresca, bibliografía nueva, compilación y extensión.
Trabajo auxiliar (scripts propios y salidas): `/tmp/claude-0/-home-user-ChanoSilva/6d28bda3-759e-5faa-92d7-8739680d15c2/scratchpad/referee4_TCD001/`.

## Veredicto

**Cambios menores.** El Teorema 5.8 y el Teorema 5.1(c) son correctos: rehíce a mano cada paso del Apéndice B y del 5.1(c), y una verificación independiente propia en aritmética racional (30 instancias X3C, 85 446 submuestras, con instancias NO difíciles de cubierta casi exacta; 8 016 casos exactos para el 5.1(c)) no encuentra ningún fallo. Los números de la construcción están polinomialmente acotados (verificado: máx |x_ij| = 72q²m(m+1) ≤ μ = 72q²(m+1)² ≤ 72n⁴) y el margen θ = 1/(24q) es polinomial. No hay bloqueantes ni mayores. Quedan menores de redacción y de estado (tras esta ronda, el "not yet refereed" debe cambiar en ocho lugares), una mejora fácil (unicidad en *toda* submuestra, que la prueba ya casi contiene) y la extensión (13 páginas con el Apéndice B en `\footnotesize`), para la que propongo recortes concretos.

Recuento: 0 bloqueantes, 0 mayores, 9 menores. Ronda 3: 14/14 puntos aplicados (13 bien, 1 aceptado con matiz —m10, extensión— aplicado a medias).

---

## 1. Verificación de los teoremas nuevos (prioridad 0)

### 1.1 Teorema 5.8 y Apéndice B, paso a paso

| Pieza (main.tex) | Qué comprobé | Resultado |
|---|---|---|
| Reducción y casos triviales (`:420`) | X3C no tiene números ⇒ fuertemente NP-completo (Garey–Johnson). m ≤ q: SÍ ⇔ m = q y conjuntos disjuntos (3q elementos distintos en un universo de 3q). Con m > q la construcción da n = m + 3q filas, p = 3q + 1 columnas: tamaño polinomial. | Correcto. Las instancias SÍ/NO fijas existen (p. ej. q = 1, C = {U, U}, que da R = {2}; y una NO con q = 2), pero no se exhiben (m9). |
| Parámetros y (eq:theta) (`:420–423`) | ε := (ηS − θ)/μ = (m/2 − 1/(24q))/(m+1) ∈ (0, ½) ⇒ ρ ∈ (½, 1); θ = ηS − (1−ρ)μ es la definición de ρ; ρμ + ηS = μ + θ; κS + ρ = ρ(S+1) + ηS = μ + θ. | Correcto. |
| Gram y correlaciones (`:420`) | Cada ancla toca sólo su columna e entre los absorbedores ⇒ G_ee = u²·1[e∈P] + cov_e; G_ee′ = nº de tripletas conservadas con e, e′; Σ_{e′≠e}G_ee′ = 2cov_e (cada tripleta con e aporta los otros dos); q_e = u·(S/u)·1[e∈P] + cov_e. | Correcto. |
| Lema B.1 (`:425–430`) | G_PP = u²I + Gram de tripletas ⪰ u²I ⇒ b* único; KKT del problema no negativo ⇒ c_e ≤ μ en P con igualdad si β_e > 0; β_e > 0 ⇒ G_eeβ_e ≤ q_e − μ = cov_e − 1 (porque G_ee′ ≥ 0, β ≥ 0) ⇒ cov_e ≥ 2 y u²β_e ≤ m − 1; acoplamiento Σ_{e′≠e}G_ee′β_e′ ≤ 2cov_e(m−1)/(9m²) ≤ 2cov_e/(9m); e ∈ P̄: c_e ∈ [0, m] ⊂ (−μ, μ); e ∈ P inactivo: c_e ∈ [S, μ]; activo: c_e = μ ⇒ KKT del Lasso con signo + ⇒ minimizador. Soporte = P₂: cov_e ≥ 2, β_e = 0 daría c_e ≥ S + 2(1 − 2/(9m)) ≥ S + 14/9 > μ. Cota inferior: G_eeβ_e ≥ (cov_e − 1) − 2cov_e/(9m) ≥ (5/18)cov_e ≥ 5/9 y G_ee ≤ u² + m ⇒ u²β_e ≥ (5/9)·9m/(9m+1) ≥ ½. | Correcto. El lema afirma bien sólo la existencia de *un* minimizador (sin anclas puede haber columnas repetidas); el teorema sólo usa su residuo, común a todos (Lema 5.3). |
| Columna objetivo y γ₀ (`:433–435`) | Fila de tripleta: ρw·3 = ρ/q; fila de ancla: (ρ + η)wu = κu/(3q) ⇒ X_{K,0} = ρwΣ_eX_{K,e} + ηwuΣ_{e∈P}δ_{a_e}; u·r_{a_e} = S − u²β_e (sólo para e ∈ P, donde se usa). | Correcto. |
| Cotas y casos (i)–(iii) (`:437`) | γ₀ ≥ 0 (c_e ≥ 0, S − u²β_e ≥ 1); γ₀ ≤ μ + θ − ηwS\|P̄\| − ηwΣ_P u²β_e. (i) pérdida ≥ m/(6q) > 1/(24q); (ii) pérdida ≥ ηw·½ = 1/(12q) > θ; (iii) cov_e ≤ 1 ⇒ N ≤ q, β = 0, γ₀ = κS + ρN/q = μ + θ − ρ(q−N)/q: N = q ⇔ cubierta exacta (3q incidencias con cov_e ≤ 1) y γ₀ − μ = θ; N ≤ q − 1 ⇒ pérdida ≥ ρ/q − θ > 0. Lema 5.3(a) ⇒ fuera de esos R no hay testigo (con o sin unicidad). | Correcto. |
| Margen θ (pregunta del encargo) | θ = 1/(24q) y las pérdidas de (i)–(iii) son racionales con numerador y denominador O(poly(m, q)); en datos enteros el margen es αα′θ = 3q(m+1) ≥ 1: **no hace falta precisión exponencial**. Medido (§1.3): γ₀ − μ = 1/48 (q = 2) y 1/72 (q = 3) exactamente en todo testigo; fuera, μ − \|c₀\| ≥ 0.11 (≫ θ). | Correcto. |
| Unicidad y testigos (`:439`) | Anclas conservadas + N ≥ 1: bloque uI en los absorbedores ⇒ independientes; X_{K,0} = Σϑ_eX_{K,e} forzaría ϑ_e = κw y en una tripleta κ/q ≠ ρ/q (η = ½) ⇒ rango p ⇒ estrictamente convexo ⇒ único ⇒ Lema 5.3(b) pone 0 en el soporte. R = [m] ∖ I no vacío (m > q) y propio (anclas). En D: 3m > 3q incidencias ⇒ algún cov_e ≥ 2 ⇒ caso (ii), \|γ₀\| < μ, rango completo ⇒ 0 ∉ S(D) con minimizador único. | Correcto. |
| Regla C exacta y desempate (pregunta del encargo) | μ′ = μ en toda submuestra; los empates \|c_e\| = μ con β_e = 0 (absorbedor anclado cubierto una vez) son por diseño y no afectan: en (iii) entran en γ₀ como c_e = μ exactamente, y la decisión se toma con el margen θ > 0 de la columna 0, no con los absorbedores. La unicidad no depende de los empates: E ⊆ P ∪ {0} y X_{K,P} contiene uI. | Correcto (ver m3: esto da unicidad en *toda* submuestra). |
| Reescalado entero (`:441`) | ρ = (12qm + 24q + 1)/(24q(m+1)); con α = 24q²(m+1), α′ = 3: αρ/q = 12qm + 24q + 1, ακu/(3q) = m(24qm + 36q + 1), αu = 72q²m(m+1) (la mayor entrada, pues 72q² ≥ 36q + 1), y ∈ {3, 1}, μ = 72q²(m+1)² ≤ 72n⁴ (q, m + 1 ≤ n). (αX, α′y, αα′μ) con β = (α′/α)β′ multiplica el objetivo por α′². | Correcto (comprobado también con aserciones de integralidad y cota en mis 30 instancias). |
| Dureza fuerte | Reducción polinomial desde un problema fuertemente NP-completo a instancias con Max(I) ≤ 72n⁴ ⇒ NP-dura en sentido fuerte. | Correcto. |
| Pertenencia a NP, p en la entrada (`:443`) | M = {β : G(β − β̂) = 0, ‖β‖₁ ≤ ‖β̂‖₁} es el conjunto de minimizadores; único ⇔ max_M β_k = min_M β_k = β̂_k ∀k; 2p LP factibles y acotados; con las filas de igualdad independientes el espacio de linealidad del dual es {λ : A_eqᵀλ = 0} = {0} ⇒ dual puntiagudo con valor óptimo finito ⇒ vértice óptimo de tamaño polinomial (Cramer); dualidad débil certifica. | Correcto. Los certificados duales son prescindibles (la programación lineal está en P); y la promesa sobre D con p en la entrada no se discute (m4). |
| Corolario 5.9 (`:285–287`, prueba `:446–448`) | Algoritmo pseudo-polinomial para f_ENTER ⇒ uno para la existencia ⇒ P = NP. f_ENTER(0) = m − q en instancias SÍ (todo testigo es [m] ∖ I con \|I\| = q). | Correcto; matices de redacción en m5. |
| Lema 5.3 fusionado (`:255–257`, prueba `:392`) | (a) (b, 0) cumple KKT suficiente; (b) un minimizador (b, 0) haría b minimizador del problema restringido con residuo r_{−j} (ajuste común) y el KKT en j daría \|γ_j\| ≤ μ′. Vale para todo p, como usa el Teorema 5.8. | Correcto. |
| Enunciado del cuerpo vs apéndice | `:283` dice "NP-complete in the strong sense … NP-hard already for integer data with y_i ∈ {1,3} and \|x_ij\| ≤ μ ≤ 72n⁴, on instances with a unique minimiser on D": coincide con lo probado (y se puede reforzar, m3). El esquema `:280` coincide con la construcción salvo una atribución imprecisa (m6). | Correcto. |

### 1.2 Teorema 5.1(c) (`:238`, prueba `:246`)

Para p = 1 el minimizador es único en todo D∖R (estrictamente convexo si x_K ≠ 0; μ′\|β\| + const si x_K = 0). Si \|T\| ≤ μ (incluye T = 0 y \|T\| = μ exactamente, ambos "no seleccionada"), un testigo ANY con signo es un testigo de selección y se usa (b). Si \|T\| > μ y s = sgn T, el soporte con signo se conserva ⇔ s·Σ_{i∉R}a_i > μ_{\|R\|}; el mínimo de s·Σ_{i∉R}a_i sobre \|R\| = k es sT − σ_k^{(s)} (se quitan los k mayores s·a_i; los empates no importan porque sólo cuenta la suma), luego hay testigo de tamaño k ⇔ sT − σ_k^{(s)} ≤ μ_k, con la igualdad contada como testigo (deselección en el borde \|Σ\| = μ_k). k recorre 1, …, n − 1 (R no vacío y propio; k = 0 y k = n quedan excluidos por la Def. 2.2; con n = 1, f = ∞). El cambio de signo (s·Σ < −μ_k) queda incluido. **Correcto.** Verificación exacta propia en 8 016 casos (§1.3): 0 discrepancias.

### 1.3 Verificación independiente (código propio, sin importar nada de `experiments/` ni `theory/`)

`ref4_strong.py` construye la instancia **desde el texto de `main.tex`** (parámetros del Apéndice B y reescalado α = 24q²(m+1), α′ = 3, con aserciones de integralidad y de la cota \|x_ij\| ≤ μ ≤ 72n⁴), recorre **todas** las submuestras D∖R (R no vacío y propio), y en cada una resuelve el Lasso completo (las p columnas, no el problema restringido del Lema 5.3) así: conjetura de soporte con signo por `sklearn.linear_model.Lasso` (tol = 1e−14) sobre los datos sin escalar, y **pulido exacto por conjunto activo en `fractions` sobre los datos enteros** (sólo se acepta una solución que cumple el KKT exactamente). Testigo ⇔ β̂₀ ≠ 0 y minimizador único; unicidad por rango exacto de X_E y, si fallara, por un criterio necesario y suficiente propio (el minimizador es único ⇔ no existe d ≠ 0 con X_E d = 0 y sgn(c_j)d_j ≥ 0 en E∖S). Además mide γ₀ − μ en los testigos (problema sin la columna 0) y μ − \|c₀\| fuera.

| Lote | Instancias | Submuestras | Resultado |
|---|---|---|---|
| q = 2 a mano (10): SÍ con tripletas repetidas; SÍ con dos cubiertas; **NO "diseño K₄"** ({012,234,145,035} y {012,235,134,045}: cada elemento cubierto dos veces, todo par de tripletas se corta en un punto, toda pareja cubre 5 de 6); NO con elementos sin cubrir; **NO casi-cubierta** {012,012,234,235}; NO "estrella" m = 6; SÍ m = 6 con cubierta única | 10 | 17 388 | equivalencia 10/10; caracterización conjunto a conjunto 0 fallos |
| q = 3 (p = 10): NO casi-cubierta {012,345,567,078} (n = 13); SÍ m = 4; SÍ m = 5 (n = 14) | 3 | 32 762 | 3/3; 0 fallos |
| q = 2 aleatorias (semilla 4004; 8 SÍ, 8 NO; m = 3…6) | 16 | 35 296 | 16/16; 0 fallos |
| Instancia de cronometraje | 1 | 510 | 1/1 |
| **Total** | **30** | **85 956** | **equivalencia 30/30; 0 fallos de caracterización; D: objetivo inactivo con minimizador único 30/30; minimizadores no únicos con β̂₀ ≠ 0: 0; f_ENTER = m − q en todas las SÍ; γ₀ − μ = θ exactamente (1/48, 1/72) en todo testigo; cota 72n⁴ 30/30** |
| Unicidad en **todas** las submuestras (`ref4_uniq_all.py`) | 3 | 13 306 | rango completo de X_E en 13 306/13 306 (base de m3) |
| Controles negativos propios | 4 | — | θ = 0: la instancia SÍ pierde su testigo (equivalencia falla: el margen es necesario); S = 0: 64 "testigos" sin anclas (63 fallos de caracterización); u = 1: no detectado en estas instancias pequeñas (la dominancia de anclas es suficiente, no necesaria aquí; coincide con lo que dice el Apéndice A) |

`ref4_p1.py` (Teorema 5.1(c) y (b)): fuerza bruta exacta sobre todos los R contra la regla por ordenación, ambas reglas, 4 000 instancias aleatorias × 2 reglas + 8 casos borde (n = 1; x = 0; T = 0; \|T\| = μ exacto; μ igual a una suma parcial para forzar sT − σ_k = μ_k; empates en a_i; f = n − 1 y f = ∞): **8 016/8 016**; T = 0 en 912 casos, \|T\| = μ en 2 532, empates en σ_k en 5 626, f = ∞ en 2 357, f = n − 1 en 579.

### 1.4 Etiquetas de estado

Teorema 5.8, Corolario 5.9 y Lema B.1 llevan [proved here], la Obs. 5.10 [computationally verified (exact arithmetic)], la Conjetura 5.11 [conjectural], el 5.1(c) está dentro del Teorema 5.1 [proved here]; la tabla de afirmaciones (`:364–366`) dice "proved here, not yet refereed; verified (exact)" para el 5.8 y "conjectural; open" para la conjetura y el ANY con signo con p ≥ 2. Son honestas. Tras esta ronda debe cambiar "not yet refereed" (m1). README `:66` y la Obs. 5.10 coinciden con `results/strong_hardness.json` (40, 20/20, 81 840, 13, 10, 12 960, 16 200, 35 890, 1 560, 340) y `results/signed_any_p1.json` (2 400/2 400).

---

## 2. Verificación de la respuesta a la ronda 3

| Id (ronda 3) | Estado | Evidencia |
|---|---|---|
| M1 "datos enteros" | aplicado bien | Resumen `main.tex:56` ("weak for integer data (pseudo-polynomial algorithm for every fixed p)"); introducción `:63` ("weakly so for integer data"); Obs. 5.2(i) `:250`; tabla `:364` ("for integer data pseudo-polynomial … so only weakly NP-complete"); Limitations `:376` (incluida la frase sobre denominadores distintos); README `:36`; FICHA `:14`, `:25`. |
| M2 ANY con signo | aplicado bien | Teorema 5.1(c) `:238`, prueba `:246` (correcta, §1.2); Obs. 5.2(iv) `:250`; tabla `:364`, `:366`; introducción `:63`; Limitations `:376`; Next steps `:378`; CONTINUIDAD `:43`, `:51`; script y JSON (2 400/2 400; reproducido, §5). |
| m1 cardinalidad | aplicado bien | `:250` "(with the cardinality as a second state, which rule P needs also for the existence question)". |
| m2 SHA sin tiempo | aplicado bien | `results/check_hardness_output.txt` y `check_strong_output.txt` sin línea `elapsed`; `sha256sum` = `8652338a…` y `157a5db1…`, iguales a los `.sha256` y a `\HardSha`/`\StrongSha`; `hardness.json` `meta.log_has_timing = false`. |
| m3 contador KKT | aplicado bien | `hardness.json` `meta.kkt_guard` = 33 484 llamadas, 0 retrocesos, error activo 1.6·10⁻¹⁴; `\HardKKTFits`; Limitations `:376`. |
| m4 "whenever the gadget is kept" | aplicado bien | `:398`. |
| m5 trozo inicial del segmento | aplicado bien | `:396`. |
| m6 rama t ≥ B | aplicado bien | `:398` (con la razón para t = B). |
| m7 promesa | aplicado bien (para p fijo) | `:262`. Para p en la entrada la promesa no se trata (m4 de esta ronda). |
| m8 CONTINUIDAD `:43` | aplicado bien | `CONTINUIDAD:43`. |
| m9 Δ entero | aplicado bien | `:253`. |
| m10 extensión | aplicado a medias (aceptado con matiz) | Recortes (a)–(d) hechos (`:277`, `:262`, `:333`, `:364`), pero el PDF pasó de 12 a **13** páginas y el Apéndice B se compuso en `\footnotesize` (`:389`) con `\enlargethispage` (`:450`). Ver §3, m8. |
| m11 `\texorpdfstring` | aplicado bien | `:311`, `:332`; 0 avisos "Token not allowed" en mi compilación. |
| m12 Moitra–Rohatgi, Hu et al. | aplicado bien | `:250` (iii), `:296`; `hu2024` en E3 `:316`; ambos verificados (§4). |

Recuento: 13 bien aplicados, 1 a medias (m10), 0 no aplicados, 0 con error nuevo.

---

## 3. Hallazgos nuevos

### Bloqueantes

Ninguno.

### Mayores

Ninguno.

### Menores

**m1. Estado "not yet refereed" tras esta ronda.** Ubicación: fecha del título `main.tex:49`; Obs. 5.10 `:290` ("not yet checked by an independent referee"); tabla `:365` ("proved here, not yet refereed"); Limitations `:376` ("and is not yet refereed"); Next steps `:378` ("have Theorem 5.8 refereed"); README `:5`, `:36`; FICHA `:3`, `:14`, `:25`; CONTINUIDAD `:43`, `:161`. Corrección: sustituir por "independently refereed (internal round 4, exhaustive check in exact arithmetic on 30 further X3C instances)" o equivalente, y en la tabla "proved here; refereed; verified (exact)". Mantener [proved here] (sigue siendo revisión interna).

**m2. Obs. 5.10 y Apéndice A: "uniqueness certified on every subsample".** El Apéndice A (`:385`) lo dice para la verificación, pero el Teorema 5.8 sólo afirma unicidad en D. No es un error; ver m3.

**m3. Reforzar el Teorema 5.8 con unicidad en toda submuestra (dos líneas).** La prueba ya contiene los ingredientes: fuera de los testigos \|γ₀\| < μ estrictamente (casos (i)–(iii)) y los absorbedores sin ancla tienen c_e ≤ m < μ, así que el conjunto de equicorrelación del minimizador (b, 0) cumple E ⊆ P, y X_{K,P} contiene el bloque uI: X_E tiene rango completo y el minimizador es único (Tibshirani 2013); en los testigos, rango completo. Comprobado en 13 306/13 306 submuestras. Corrección (en `:283`): "…on instances with a unique minimiser on $D\setminus R$ for every $R\subsetneq[n]$", y al final de "Uniqueness and the witnesses" (`:439`): "For every other $K$, $|\gamma_0|<\mu$ and the absorbers without anchor have $c_e\le m<\mu$, so the equicorrelation set of the minimiser $(\beta,0)$ lies in $P$, where $X_{K,P}$ contains the block $uI$; hence the minimiser is unique~\citep{tibshirani2013}." Así el teorema queda en paralelo con el 5.4 y la dureza no se apoya en submuestras con minimizador no único.

**m4. Pertenencia a NP con p en la entrada: certificados innecesarios y promesa sin tratar.** (a) `:443`: la verificación de unicidad no necesita certificados duales: los 2p LP se resuelven en tiempo polinomial (Khachiyan). La prueba actual es correcta, pero más larga de lo necesario. (b) `:262` dice que las condiciones sobre D se comprueban en tiempo polinomial "for fixed p"; para p en la entrada (Teorema 5.8) no se dice nada. Corrección: "With $p$ in the input the conditions on $D$ are also checked in polynomial time (an exact minimiser of the convex quadratic programme \eqref{eq:lasso} is computable in polynomial time, and uniqueness by the $2p$ linear programmes of the proof of Theorem~\ref{thm:strong}); alternatively, read \tsc{Selection-Witness} as a promise problem." La cita para el QP convexo exacto sería Kozlov, Tarasov y Khachiyan, "The polynomial solvability of convex quadratic programming", USSR Comput. Math. Math. Phys. 20 (1980) 223–228 (la doy de memoria: verificar antes de añadirla); si no se quiere citar, basta la lectura como problema con promesa.

**m5. Corolario 5.9 (`:286`).** (a) M = max(\|x_ij\|, \|y_i\|) omite μ; en la construcción μ ≤ 72n⁴, así que es inocuo, pero el enunciado limpio es "M = max(|x_ij|, |y_i|, μ) for integer μ". (b) "so the dependence on p in Proposition 5.5 cannot be made polynomial" se lee mejor como "so no algorithm polynomial in $n$, $p$ and $M$ exists, and the exponent of Proposition~\ref{prop:pseudo} cannot be replaced by a polynomial in $p$ times one in $(n,M)$; whether $g(p)\,\mathrm{poly}(n,M)$ is possible (fixed-parameter tractability in $p$ for unary data) is not addressed". La versión actual no es falsa, pero "dependence on p … polynomial" admite la lectura g(p) que la dureza fuerte no excluye.

**m6. Esquema del cuerpo (`:280`): "their offset S keeps inactive an absorber without its anchor".** Lo que mantiene inactivo a un absorbedor sin ancla es μ = S + 1 > m ≥ cov_e; el desplazamiento S hace que cada ancla ausente cueste ηwS = m/(6q) en γ₀ (caso (i)) y que un absorbedor anclado cubierto dos veces supere μ. Escribir: "their offset $S$ (with $\mu=S+1>m$) makes a missing anchor cost $\eta wS$ in the target correlation, while an absorber without its anchor stays inactive."

**m7. Conjetura 5.11 (`:294`): "already for data in {−1, 0, 1} up to a common scale".** Ni siquiera el caso probado (regla C, ENTER) usa datos ternarios (las entradas son ρ/q, κu/(3q), u, 0, 1), y el texto no da evidencia del refuerzo; además "up to a common scale" no aclara si la escala es común a X e y y qué se permite para μ. Corrección: quitar "already for data in {−1,0,1} up to a common scale", o separarlo como pregunta abierta ("Whether ternary data suffice is open, even for Theorem~\ref{thm:strong}").

**m8. Extensión: 13 páginas con el Apéndice B en `\footnotesize` y `\enlargethispage`.** El contenido nuevo está justificado (la prueba completa del 5.8 es lo que hace verificable el resultado), pero componer en la letra más pequeña del documento precisamente la prueba más delicada es mala elección, y `\enlargethispage{2\baselineskip}` (`:450`) es un parche de paginación. Propongo recuperar ≈ 0.7 página de texto redundante y volver el Apéndice B a `\small`, sin quitar ninguna prueba ni tabla:
 (a) E3 `:316`: las 12 cifras de exactitud (`\EthreeAAnyOnestepExact` … `\EthreeBEnterAmipExact`) están todas en la Tabla 2; dejar sólo la conclusión y las cifras que no están en la tabla (≈ 6 líneas).
 (b) Párrafo "Strong hardness with growing p" `:280`: la construcción se repite casi literalmente en el Apéndice B (`:420`); dejar dos frases (absorbedor por elemento, anclas dominantes, la columna objetivo entra sólo con todas las anclas y una cubierta exacta) (≈ 4 líneas).
 (c) Obs. 5.10 `:290`: una frase con remisión al Apéndice A (≈ 3 líneas).
 (d) E2 `:312`: los porcentajes de tipos de cambio (leave/enter/swap/sign) a `results/fragility.md` (≈ 3 líneas).
 (e) Obs. 3.5 `:188`: las dos últimas frases (converso y "We did not search…") en una (≈ 2 líneas).
 (f) Prueba de la Prop. 3.1 `:132–142`: la derivación de (3.2) desde Woodbury puede ir en tres líneas (≈ 4 líneas).
 Con eso el PDF queda en 13 páginas sin `\footnotesize` ni `\enlargethispage`, o en 12 si se mantiene el `\footnotesize`. Para un borrador de trabajo con todas las pruebas, 13 páginas son aceptables; lo que no recomiendo es el cuerpo de letra.

**m9. Casos triviales de la reducción (`:420`).** "a fixed yes- or no-instance is output": decir cuáles (p. ej. la construcción para q = 1, C = (U, U) —SÍ, testigo R = {2}— y para q = 2, C = ({0,1,2},{2,3,4},{1,4,5},{0,3,5}) —NO). Una línea; evita que el lector tenga que comprobar que existen.

### Lectura fresca (sin hallazgos adicionales sustantivos)

Releí el resumen, la introducción, las Secciones 2–5, la tabla de afirmaciones, Limitations y los Apéndices A–B. Resumen e introducción describen bien el alcance (deselección NP-completa con p = 1; selección y ANY con signo por ordenación con p = 1; selección NP-completa para todo p fijo ≥ 2, débil con datos enteros; fuerte con p en la entrada bajo la regla C; ANY con signo con p ≥ 2 abierto). La Obs. 5.2(iv) es correcta: en ambas construcciones hay testigos ANY con signo triviales (comprobé que quitar todas las tripletas deja K = anclas, β = 0 único porque \|c_e\| = S < μ y c₀ = κS = μ + θ − ρ < μ, mientras que en D el soporte es P₂ ≠ ∅). Notación coherente (P̄ en lugar del antiguo B, que choca con B = Σb_i del Teo. 5.4). Sin sobreafirmaciones nuevas.

---

## 4. Bibliografía

| Entrada | Estado | Corrección |
|---|---|---|
| `hu2024` (nueva) | Verificada por búsqueda (actas NeurIPS 2024, página del póster, mlanthology, NSF PAR, arXiv:2409.18153): Yuzheng Hu, Pingbang Hu, Han Zhao, Jiaqi W. Ma, "Most Influential Subset Selection: Challenges, Promises, and Beyond". El resumen dice que las heurísticas voraces basadas en influencia pueden fallar incluso en regresión lineal (errores de la función de influencia y estructura no aditiva) y que la versión adaptativa captura parte de las interacciones: respalda la frase de E3 (`:316`). | Ninguna. |
| `moitra2022` | Verificada por búsqueda (arXiv:2205.14284; ICLR 2023 en mlanthology): algoritmo n^{O(d³)} que decide Stability(X, y) ≤ k y, bajo ETH, inexistencia de algoritmos n^{o(d)} (según los resúmenes de búsqueda, la cota inferior se enuncia para anular/cambiar de signo un coeficiente). El contraste unilateral (signo) / bilateral (ventana \|c_j\| ≤ μ) de la Obs. 5.2(iii) y la frase "does not transfer" (`:296`) son correctos; el paralelo con el Teo. 5.1(c) (ANY con signo, unilateral, fácil para p = 1) es exacto. | Opcional: tipo `@inproceedings`, ICLR 2023 (ahora `@misc` con año 2022 y la sede en `note`). |
| `garey1979` | Usada para "X3C es fuertemente NP-completo" y "un problema fuertemente NP-duro no admite algoritmo pseudo-polinomial salvo P = NP": ambas cosas están en Garey–Johnson (§4.2 y [SP2]). | Ninguna. |
| Kozlov–Tarasov–Khachiyan (1980) | No está en `refs.bib`; sólo la sugiero en m4, de memoria. | Verificar antes de añadir, o usar la lectura como problema con promesa. |
| Resto | Sin cambios respecto de la ronda 3. arxiv.org no se leyó directamente (proxy); las verificaciones se apoyan en resultados de búsqueda concordantes. | — |

---

## 5. Verificación computacional

| Qué | CPU | Resultado |
|---|---|---|
| `ref4_strong.py` (q = 2 a mano, q = 3, aleatorias, cronometraje) | 13.4 + 13.0 + 37.4 + 1.6 s | 30/30 equivalencias, 0 fallos en 85 956 submuestras (§1.3). |
| `ref4_strong.py controls` | 3.8 s | θ = 0 y S = 0 detectados; u = 1 no detectado en estas instancias. |
| `ref4_uniq_all.py` | 9.6 s | unicidad por rango de X_E en 13 306/13 306 submuestras (m3). |
| `ref4_p1.py` (Teorema 5.1(b)–(c)) | 0.6 s | 8 016/8 016. |
| Reproducción de `experiments/check_strong.py` y `check_signed_any_p1.py` del autor en una copia | (pendiente) | (pendiente) |
| `latexmk -pdf` en una copia | 2.7 s | 0 errores, 0 referencias o citas indefinidas, 0 "??" en el texto del PDF, 0 Overfull, 2 Underfull (tabla de afirmaciones, ya conocidos), 0 avisos de hyperref, bibtex sin avisos; **13 páginas** (cuerpo hasta p. 11; Apéndice A p. 11; Apéndice B pp. 11–13; referencias p. 13). |

---

## 6. Lista final de acciones (por prioridad)

1. Cambiar el estado del Teorema 5.8 de "not yet refereed" a revisado en la ronda 4 en `main.tex:49`, `:290`, `:365`, `:376`, `:378`, README, FICHA y CONTINUIDAD (m1).
2. Reforzar el Teorema 5.8 a "unique minimiser on $D\setminus R$ for every $R$" con las dos frases de m3, y alinear el Apéndice A (m2).
3. Tratar la promesa sobre D con p en la entrada (o declarar el problema con promesa) y simplificar la pertenencia a NP usando que la programación lineal está en P (m4).
4. Volver el Apéndice B a `\small`, quitar `\enlargethispage` y recuperar el espacio con los recortes (a)–(f) de m8.
5. Precisar el Corolario 5.9 (μ en M; alcance de "cannot be made polynomial") (m5) y la frase del desplazamiento S en el esquema (m6).
6. Quitar o justificar "already for data in {−1,0,1} up to a common scale" en la Conjetura 5.11 (m7).
7. Exhibir las instancias fijas SÍ/NO de los casos m ≤ q (m9).
8. Opcional: `moitra2022` como `@inproceedings` (ICLR 2023).
