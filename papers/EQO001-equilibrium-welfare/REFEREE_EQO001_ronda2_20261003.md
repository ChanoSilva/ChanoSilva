[EN CURSO]

# Informe de arbitraje interno — EQO001 (ronda 2, 03/10/2026)

Árbitro: agente independiente (Claude Code), distinto del de la ronda 1, sin acceso al autor. Objeto: borrador v0.2 de *Equilibrium Operators, Variational Inequalities and Welfare: What Is and Is Not a Theorem* (commit `a20cd39`; `manuscript/main.tex`, 417 líneas; PDF de 14 páginas A4). Versión anterior consultada con `git show` (solo lectura). Trabajo auxiliar en `scratchpad/referee2_EQO001/` (notas, reproducción `run2/`, compilación `repro/`, scripts `check_ex57.py`, `search2_m3.py`, `confirm_m3.py`).

## 0. Veredicto

**Cambios mayores (de alcance acotado).** Todo lo que la ronda 1 pidió está aplicado, la reproducción coincide bit a bit y el Ejemplo 5.7 es correcto (umbral 40 y brecha 1/20 verificados a mano y con un cálculo independiente); pero las dos preguntas abiertas reformuladas vuelven a declarar abierto lo que se resuelve en pocas líneas: la complejidad de la Pregunta 8.1(ii) es co-NP-completa por una reducción directa desde MAX-CUT con la misma plantilla del Ejemplo 5.6 (también con $F$ fuertemente monótono), y la "expectativa" de no poliedralidad de la Pregunta 8.2 para $m\ge3$ la confirma una búsqueda aleatoria de 30 s. A eso se suma que la variante fuertemente monótona del Ejemplo 5.6 admite una prueba cerrada de diez líneas que el texto deja como "numérica", y que la nota sigue en 14 páginas.

## 1. Verificación de la ronda 1

Líneas referidas a `manuscript/main.tex` v0.2 salvo indicación.

| Id | Estado | Evidencia |
|---|---|---|
| B1 (Pregunta 1: poliedralidad / descripción finita) | **aplicado bien, con un problema nuevo en la reformulación** | Ej. 5.6 en 284–294 con el cálculo completo de la parábola (verificado a mano: la identidad $\tfrac14-\lambda_1+\tfrac12(\lambda_1+\tfrac14)^2=\tfrac12(\lambda_1-\tfrac34)^2$, las dos ramas $x_2\in\{0,1\}$, el testigo $(0.55,0,1)$ con brecha $0.10125$). Pregunta 8.1 reformulada (390–392) con Tarski–Seidenberg, las $3^N$ caras y la trivialidad de $N=2$; "Next steps" sin "at least for $N=2$" (398); resumen (62) y Tabla 2 (378) actualizados. **Pero** la parte (ii) de la nueva pregunta (complejidad) se resuelve en cinco líneas y la parte (i) queda acotada por esa misma reducción: véase M1. |
| M1 (E1c tautológico) | **aplicado, pero E1c queda redundante** | `traffic_poa.py:94` compara ahora `f_toll` con `f_opt_wf` (water-filling independiente); texto 314 y 409 honesto ("checks the solver ..., not the identity"). Pero `f_toll` y `f_opt` son la misma llamada al solver con la misma función: `dev_tolled_vs_opt_wf` coincide bit a bit con `dev_opt_vs_waterfill` en 170/200 instancias (máx. diferencia $2.2\times10^{-16}$; ambos máximos $8.7995\times10^{-11}$). E1c repite el control "solver vs. water-filling" de E1b; véase m1. |
| M2 (literatura; novedad) | aplicado bien | Dubey en 256 y 281; Benson–Sun en 245 y 256; Ahuja–Orlin en 218; Danskin en 266; "new only in its packaging" sustituido por la remisión al Remark 5.2 (69). Precisiones en m4, m5 y m9. |
| M3 ("definitive") | aplicado bien | Resumen 62 ("records that assessment"); README "recoge la evaluación"; la ficha se presenta como propuesta pendiente de esta ronda. |
| M4 (criterios) | aplicado bien | `check_criteria` en los tres scripts (p. ej. `commodity_cone.py:164–183`, `welfare_cone.py:530–565`); flags en los JSON; `\CritTraffic`, `\CritWelfare`, `\CritCommodity` generados; texto 311 sin "fixed before the runs" y con la salvedad de que no hay prerregistro externo. |
| M5 (56 % cota inferior) | aplicado bien | 62 ("at least"), 333 (cota inferior y los 110 puntos no contados), 349 (pie), 376 (Tabla 2), docstring de `welfare_cone.py:30–32`. |
| m1 (Rosen fuera del Teorema 3.2) | aplicado bien | 141 y Tabla 2 (364). |
| m2 ($c_e\in C^1$) | aplicado bien | 148 (teorema fundamental del cálculo) y 218. |
| m3 (unicidad en Pigou) | aplicado bien | 178. |
| m4 ("at most one point") | aplicado bien | 218. |
| m5 ("proportional") | aplicado bien | 202. |
| m6 (Prop. 5.3 fuera de la clase; Danskin) | aplicado bien | 266 y 277. |
| m7 (sistemas singulares) | aplicado bien | 405. |
| m8 (73, no 75) | aplicado bien | README, CONTINUIDAD:28. |
| m9 (formatos) | aplicado bien | `numbers.tex`: `\PigouPoASixteen`=4.7268, `\WitGap`=0.215. |
| m10 (PoA $=1$ en 86/200) | aplicado bien | 314; JSON `n_poa_equals_one`=86. |
| m11 (forma cerrada con $\alpha-1$) | aplicado bien | `welfare_cone.py:358–359, 368–369`. |
| m12 (ficha) | aplicado bien | `FICHA_EQO001_propuesta.md` existe (ES/EN). Matices en m10 de este informe. |
| m13 ("Lemma 3.1 of") | aplicado bien | 172. |
| m14 (resumen ≤200 palabras) | aplicado bien | 196 palabras (recuento sobre el fuente). |
| m15 (numeración) | aplicado bien | README y CONTINUIDAD usan Prop. 5.3, Ej. 5.4–5.7, Teorema 3.5, coherentes con el PDF recompilado. |
| m16 (cajas desbordadas) | aplicado bien | Recompilación propia: 0 *Overfull*, 0 referencias indefinidas, 0 "??". |
| m17 (Figura 1) | aplicado bien | Pie de 320 (cuña rellena, fronteras, una de cada cinco direcciones); `make_figures` coherente. |
| m18 (representante de flujos de camino) | aplicado bien | 395. |
| Bibliografía (Wardrop, Nikaidô–Isoda, nuevas entradas) | aplicado, con un error nuevo | `refs.bib:1–9` y `:128–136` corregidos; seis entradas nuevas. Pero `roughgarden2005` está en `refs.bib:69` y **no se cita** (el PDF lista 29 referencias), mientras README y RESPUESTA §4 dicen "30 entradas, todas citadas". Véase §3. |
| Recortes a ≤10 páginas (§6 del informe 1) | aplicado a medias | 13 → 14 páginas. Varios recortes hechos, pero el Apéndice B y la Tabla 2 (los dos mayores) siguen en el cuerpo. Véase §2, M4. |

Recuento: 22 bien aplicados, 3 a medias o con un problema nuevo (B1, M1, recortes), 1 aplicado con un error nuevo (bibliografía), 0 no aplicados.

## 2. Hallazgos nuevos

### Bloqueantes
Ninguno. Las demostraciones del cuerpo son correctas y los números coinciden con los JSON.

### Mayores

**M1. La Pregunta 8.1(ii) no es abierta: decidir $\lambda\in\Lambda(x^*)$ es co-NP-completo para pagos cuadráticos en una caja, incluso con $F$ fuertemente monótono, $x^*$ un vértice y $\lambda$ un vector unitario. La misma reducción muestra que decidir $\Lambda=\Lone$ es co-NP-difícil, lo que acota lo que puede pedir la parte (i).** (main.tex:391; ficha; README; CONTINUIDAD:76)
- *Reducción (verificada a mano).* Sea $G=(V,E,w)$ un grafo con pesos enteros, $\mathrm{cut}(x)=\sum_{ij\in E}w_{ij}(x_i+x_j-2x_ix_j)$, $L(x)=\sum_i\deg_w(i)\,x_i$ y $q(x,y)=\mathrm{cut}(x)+y\,(k-\tfrac12-L(x))$ en $[0,1]^{n+1}$. La función $q$ es multilineal, así que su máximo sobre la caja se alcanza en un vértice; en los vértices con $y=0$ vale $\mathrm{cut}(x)$ y con $y=1$ vale $\mathrm{cut}(x)-L(x)+k-\tfrac12\le k-\tfrac12$ (porque $\mathrm{cut}\le L$), con igualdad en $x=0$. Por tanto $p=(0,1)$ es maximizador global de $q$ si y solo si $\mathrm{maxcut}(G)<k$. Juego con $n+2$ jugadores escalares en $[0,1]$: $u_i=-x_i-\tfrac\varepsilon2x_i^2$ ($i\le n$), $u_{n+1}=y-\tfrac\varepsilon2y^2$, $u_{n+2}=z-\tfrac\varepsilon2z^2+q(x,y)$, con $0\le\varepsilon<1$. Cada pago es cóncavo en la variable propia (clase de la Def. 2.3), $F$ es $\varepsilon$-fuertemente monótono, $x^*=(0,\dots,0,1,1)$ es el único equilibrio (estrategias dominantes) y $W_{e_{n+2}}=z-\tfrac\varepsilon2z^2+q(x,y)$ es separable en $z$. Luego $e_{n+2}\in\Lambda(x^*)\iff\mathrm{maxcut}(G)<k$. La pertenencia a co-NP se sigue de que un $\lambda\notin\Lambda$ tiene como certificado un maximizador racional de tamaño polinómico (enumeración de caras; Vavasis 1990). Además $\nabla_xq(p)=0$ y $\partial_yq(p)=k-\tfrac12>0$, así que $\Lone(x^*)=\mathbb R^{n+2}_+$, y $\Lambda=\Lone$ si y solo si $e_{n+2}\in\Lambda$: decidir $\Lambda=\Lone$ también es co-NP-difícil.
- *Consecuencias.* (a) La parte (ii) está resuelta, salvo la cuestión de la descripción de tamaño polinómico. Una descripción con coeficientes de tamaño polinómico daría un test de pertenencia polinómico, lo que es imposible salvo que coNP ⊆ P/poly; queda abierto, como mucho, contar inecuaciones sin acotar grados ni coeficientes. (b) La parte (i), "caracterizar ... en términos del patrón de caras activas y los hessianos cuándo $\Lambda=\Lone$", no puede tener una respuesta comprobable en tiempo polinómico salvo que P = NP; tal como está escrita no es una pregunta matemática con criterio de éxito. (c) La cita de Murty–Kabadi (dureza de la optimalidad *local*) ya no es lo que importa: la dureza relevante es la de la optimalidad *global* en caja, y aquí se demuestra directamente.
- *Corrección.* Convertir (ii) en una proposición demostrada (texto sugerido: "**Proposition 5.8.** Deciding $\lambda\in\Lam(x^*)$ for quadratic payoffs on a box is co-NP-complete, even when $F$ is strongly monotone, $x^*$ is a vertex and $\lambda$ is a unit vector; so is deciding $\Lam(x^*)=\Lone(x^*)$." con la reducción anterior, unas 8 líneas). Reescribir la Pregunta 8.1 como una pregunta con criterio de éxito, por ejemplo: "¿Para qué clases de juegos (potenciales, supermodulares, hessianos $H_i$ con estructura de signo dada, $N$ fijo) es polinómica la pertenencia, y es entonces $\Lambda$ poliédrico?". Si no, eliminarla. Actualizar resumen, Tabla 2 (fila "Open questions"), "Next steps" (el "case analysis on the 27 faces" no tiene sentido general a la vista de la dureza), README, ficha y CONTINUIDAD:76.

**M2. La expectativa de la Pregunta 8.2 ("non-polyhedral in general" para $m\ge3$) se confirma numéricamente con una búsqueda aleatoria corta, y la segunda parte ("identify the network structures for which $\Lambda=\Lone$") hereda la dureza de M1.** (main.tex:395)
- *Evidencia.* `search2_m3.py` (28 s, 29 equilibrios en esquina examinados; tres mercancías con demanda unitaria, cada una con un enlace privado $a_kf+b_k$ y un enlace compartido común $a_sf$). Instancia $a=(0.091,0.137,0.525)$, $b=(0,0,1.473)$, $a_s=0.393$: el equilibrio de Wardrop es $y^*=(0,0,1)$ (residuo 0; costos de camino $0.091\le0.393$, $0.137\le0.393$ y $0.393\le1.473$) y $\Lone(y^*)=\mathbb R^3_+$, pero en la rebanada $\lambda_2=1$, $\Lambda=\{\lambda_3\ge v(\lambda_1)\}$ con $v''\approx0.0055$–$0.0115>0$ en $\lambda_1\in[1.6,2.6]$ (15 puntos bisecados, `confirm_m3.py`). La cara competidora es $\{y_3=0\}$ con $y_1,y_2$ interiores (p. ej. $(0.095,0.153,0)$ en $\lambda_1=2$), cuyo mínimo es una función racional de $\lambda$. Esto confirma el mecanismo: la frontera es curva cuando el competidor tiene coordenadas libres interiores cuyo minimizador depende de $\lambda$. Una multisalida independiente con L-BFGS-B (60 arranques, sin el código del autor) confirma la brecha $0.00321$ a $2\times10^{-3}$ por debajo de la frontera en tres puntos.
- *Corrección.* O bien (preferible) sustituir la conjetura por un ejemplo con frontera calculada en forma cerrada (el mínimo cuadrático sobre la cara $\{y_3=0\}$ es explícito), o bien escribir "a random three-commodity instance with one shared edge has a curved boundary (numerically)" y quitar "we expect". Reformular la segunda parte con un criterio comprobable (p. ej. "¿es $\Lambda=\Lone$ en redes serie-paralelo con un solo enlace compartido y costos lineales sin término constante?"; con $b=0$ el equilibrio es el óptimo del sistema y $\Lone$ contiene la diagonal, véase m6).

**M3. La variante fuertemente monótona del Ejemplo 5.6 se puede demostrar en forma cerrada; el texto la deja como "numéricamente" (293, 332) y CONTINUIDAD:78 la lista como pendiente.**
- *Cálculo.* Con $u_i\mapsto u_i-\tfrac\varepsilon2x_i^2$, $0<\varepsilon<1$, y $\lambda_3=1$: $x_3=1$ (creciente en $[0,1]$); $\Lone\cap\{\lambda_3=1\}=\{\lambda_1\ge\tfrac{1}{4(1-\varepsilon)}\}$. En $(x_1,x_2)$ el hessiano de $W_\lambda$ es $\begin{psmallmatrix}-(1+\varepsilon\lambda_1)&\frac12\\\frac12&-\varepsilon\lambda_2\end{psmallmatrix}$, indefinido si $\varepsilon\lambda_2(1+\varepsilon\lambda_1)<\tfrac14$, así que el máximo está en una arista. En $x_1=1$, $W$ crece en $x_2$; en $x_2=1$ el máximo está en $x_1=1$ porque $\lambda_1\ge\tfrac1{4(1-\varepsilon)}$; en $x_1=0$ el valor es $\le0<W_\lambda(x^*)$ en el rango considerado. En $x_2=0$ el máximo es $(\lambda_1+\tfrac14)^2/(2(1+\varepsilon\lambda_1))$, alcanzado en $x_1=(\lambda_1+\tfrac14)/(1+\varepsilon\lambda_1)\le1$. Por tanto, en el rango del texto,
  $\Lambda\cap\{\lambda_3=1\}=\{\lambda_2\ge\varphi(\lambda_1)\}$ con $\varphi(\lambda_1)=\dfrac{(\lambda_1+\frac14)^2/(2(1+\varepsilon\lambda_1))+\frac14}{1-\varepsilon/2}-\lambda_1$,
  estrictamente convexa porque $\tfrac{d^2}{d\lambda^2}\tfrac{(\lambda+1/4)^2}{1+\varepsilon\lambda}=\tfrac{2(1-\varepsilon/4)^2}{(1+\varepsilon\lambda)^3}>0$.
- *Evidencia.* $\varphi$ coincide con las nueve fronteras bisecadas por el autor (`results_welfare.json`, `strongly_monotone_variant.boundary_lambda2`) a $1.1\times10^{-8}$ (la tolerancia del test es $10^{-8}$). Comprobado además que en esos puntos $\lambda_2+\tfrac12x_1-\tfrac12<0$ (entre $-0.105$ y $-0.054$), es decir, $x_2=0$ es óptimo para el $x_1$ competidor.
- *Corrección.* Sustituir "and the boundary of the slice remains curved (E2c in Section 6, numerically)" por "and on the slice $\lambda_3=1$ the boundary becomes $\lambda_2=\varphi(\lambda_1)$ [fórmula], strictly convex, for $\tfrac1{4(1-\varepsilon)}\le\lambda_1\le\dots$ (proof as above, three lines; E2c checks it to $10^{-8}$)". Que E2c compare con $\varphi$ en lugar de las segundas diferencias. Cerrar el pendiente 3 de CONTINUIDAD.

**M4. Extensión: 14 páginas frente a la meta de 10; el exceso solo está justificado en parte.** Lo que la revisión exigió (Ej. 5.6 y 5.7 con sus cálculos, unas 1.2 páginas) justifica 11 páginas, no 14. Recortes concretos, sin perder ninguna demostración nueva:
1. Apéndice B (p. 12–13, unas 0.8 páginas): ya figura literalmente en los docstrings y en los `tables_*.md`. Dejar 5 líneas con los umbrales y remitir a los docstrings (−0.6 p).
2. Tabla 2 de afirmaciones (p. 11, casi una página): los estados ya van en línea con `\status{}`. Dejar los "three lines" de §7 y mover la tabla a `results/CLAIMS.md` (−0.8 p).
3. Prop. 3.1 (Poincaré) y su prueba, la prueba del Lema 2.6 (cono normal del simplex) y la del Lema 3.4: dejar el enunciado y la cita (Kinderlehrer–Stampacchia, cap. I; Rockafellar) (−0.4 p).
4. Prop. 4.1(c) (forma estándar): dejar solo la frase sobre el simplex, sin el sistema desplegado (−0.2 p).
5. Párrafos E2–E5 de §6: muchas cifras repiten las de la Tabla 1 y los `tables_*.md`. Dejar por experimento el criterio cumplido y la cifra clave (−0.5 p).
6. Figura 2, panel izquierdo (Pigou contra $d$): es la fórmula cerrada del Ej. 3.7. Dejar solo el histograma (−0.15 p).
7. Pregunta 8.1, tras M1: queda en cuatro líneas (−0.15 p).
Total ≈ −2.8 p, más ≈ +0.3 p por la Proposición de M1: unas 11 páginas. Si la meta de 10 es firme, mover también el Ejemplo 5.5 (Cournot) a un remark de tres líneas.

### Menores

- **m1 (E1c redundante; main.tex:314, 409; `traffic_poa.py:88–94`).** `f_toll` se calcula con `cost(f)+a*f`, que es en coma flotante la misma función que `mcost` de `f_opt`, con los mismos `x0`, `mu`, `L`; las dos desviaciones respecto del water-filling coinciden bit a bit en 170/200 instancias. Lo que se comprueba es el "solver vs. water-filling" de E1b. *Corrección:* fusionar E1c con E1b ("the optimum, equivalently the tolled equilibrium, matches water-filling to $8.8\times10^{-11}$") y quitar el criterio duplicado, o dar a E1c contenido propio: costos no afines (p. ej. BPR $c_e=b_e(1+0.15(f/\kappa)^4)$), donde $c+\tau$ y $\nabla C$ no son la misma expresión.
- **m2 (Remark 3.6, main.tex:172, y §6, 311).** "All solvers in Section 6 are the iteration of Theorem 3.5(b) with $\gamma=\mu/L^2$, so each computed equilibrium comes with a uniqueness proof" contradice el Apéndice A (404) y `welfare_cone.py:461–463`: en E2c, $F$ es constante ($\mu=L=0$), se usa $\gamma=1$ y la unicidad viene de las estrategias dominantes. *Corrección:* añadir "except E2c, where $F$ is constant, $\gamma=1$ is used and uniqueness follows from dominance".
- **m3 (resumen 62; README "Imposibilidad").** "$(F,K)$ alone never determines it" y "ninguna propiedad de $(F,K)$ implica ni excluye optimalidad" van más allá de lo demostrado: la Prop. 5.3 muestra que ninguna $(F,K)$ *excluye* $\Lambda=\mathbb R^N_+$, pero solo se exhibe *un* par (Cournot (i)) compatible con dos conos distintos, y con $N=1$ el cono es siempre $\mathbb R_+$. *Corrección (dos líneas, a la Prop. 5.3):* "If $N\ge2$ and some $K_{-i}$ is not a singleton, adding to $u_i$ a linear function $c\ip{d}{x_{-i}}$ with $d$ pointing into $K_{-i}$ from $x^*_{-i}$ and $c$ large leaves $F$ unchanged and removes $e_i$ from $\Lam(x^*)$". O escribir "does not in general determine".
- **m4 (Remark 5.2, Dubey).** La frase "any $\lambda\in\Lone(x^*)\setminus\{0\}$ must annihilate every weighted externality" enlaza con Dubey a través de una implicación que el texto no enuncia: *débil eficiencia de Pareto (incluso local) ⇒ $\Lone(x^*)\ne\{0\}$*, por el teorema de la alternativa de Gordan/Motzkin, sin concavidad. Así la conexión con Dubey es un corolario y no una analogía. *Corrección:* añadir a 5.1(e): "Conversely, without any concavity, if $x^*$ is locally weakly Pareto efficient then $\Lone(x^*)\ne\{0\}$ (no $d$ in the tangent cone has $G(x^*)d>0$; Motzkin's alternative)".
- **m5 (Remark 5.2 y Prop. 5.3; literatura).** La transformación $u_i\mapsto u_i-v_i(x_{-i})$ es un caso de *equivalencia de mejor respuesta* (Morris–Ui 2004, *GEB* 49, 260–287, verificada), que estudia justamente qué juegos son equivalentes a juegos de interés idéntico. Citarla junto a Nikaidô–Isoda. La RESPUESTA (M2) dice que el Remark 5.2 lista la Prop. 5.3 entre lo "reempaquetado", pero el texto del Remark no la menciona: alinear las dos cosas.
- **m6 (E5b, main.tex:337).** (a) 19 de los 21 testigos son $\lambda=(1,0)$ o $(0,1)$, pesos que ignoran una mercancía; solo 2 son pesos interiores. (b) "The direction grid meets $\Lone$ in 90" mezcla conos de dimensión completa con rayos: en 21 instancias con equilibrio interior y $b\equiv0$, $\Lone$ es la diagonal $\lambda_1=\lambda_2$ (con costos lineales homogéneos el equilibrio de Wardrop es el óptimo del sistema) y la rejilla la toca solo porque incluye $45^\circ$; en otros casos el rayo es un eje. El 23 % depende de la rejilla. *Corrección:* informar por patrón de caras activas y separar testigos interiores de los de eje, o quitar el porcentaje.
- **m7 (Ej. 5.7, notación).** $\NC_K(f^*)=\R_+\times\R_-$ está escrito en las coordenadas reducidas $y=(f_B,f_D)\in[0,1]^2$, no en $\R^P$ como en la Def. 2.5. Añadir "in the reduced coordinates $y$ (the cones $\Lam,\Lone$ are invariant under this affine reparametrisation)".
- **m8 (Pregunta 8.2, "with equality when no edge is shared").** Correcto, pero entonces el problema se separa por mercancías y $\Lam$ es un producto de ortantes recortados por condiciones por mercancía; decirlo evita que parezca un resultado.
- **m9 (Remark 5.2, "in general position").** Dubey (1986) trata equilibrios interiores de juegos suaves y su genericidad es en el espacio de pagos. Precisar "for interior equilibria, generically in the payoffs" para no sugerir más.
- **m10 (FICHA y README).** La ficha dice "Estado: Cerrada como nota expositiva" y a la vez "no aplicar hasta la ronda 2": escribir el estado propuesto como condicional. Ficha y README listan como pregunta abierta "la complejidad de decidir $\lambda\in\Lambda$" (véase M1) y el README dice que la variante fuertemente monótona "conserva la frontera curva" sin decir "numéricamente" (véase M3). Actualizar ambos tras M1–M3.
- **m11 (`make_numbers.py:58`).** Sigue generando `table_pigou.tex`, que `main.tex` ya no usa. Quitarlo o anotarlo.
- **m12 (README, tabla de contenidos).** "148 macros": `numbers.tex` tiene 150 `\newcommand` (incluidos los flags `\Has*`). Corregir o decir "≈150".

## 3. Bibliografía

Método: WebSearch (resultados de editoriales, Semantic Scholar, AbeBooks, RePEc). No intenté Crossref ni arXiv, que según la ronda 1 bloquea el proxy. Entradas nuevas de la ronda 1 y estado:

| Entrada | Estado | Corrección |
|---|---|---|
| dubey1986 | verificada (MOR 11(1), 1–8) | Precisar el alcance (equilibrios interiores; genericidad en pagos), m9. |
| bensonSun2000 | verificada en la ronda 1 (JOTA 105(1), 17–36); no la volví a buscar | — |
| ahujaOrlin2001 | verificada en la ronda 1 (OR 49(5), 771–783); no la volví a buscar | — |
| murtyKabadi1987 | verificada en la ronda 1 (Math. Prog. 39, 117–129) | Añadir `number={2}`. Tras M1, su uso en 8.1 debe cambiar (dureza global en caja, no local). |
| danskin1966 | verificada (SIAM J. Appl. Math. 14, 641–664; DOI 10.1137/0114053) | Añadir `number={4}` y `doi`. |
| bochnakCosteRoy1998 | verificada (Springer, Ergebnisse 3. Folge, vol. 36, 1998) | Opcional: `series={Ergebnisse der Mathematik und ihrer Grenzgebiete (3)}`. |
| roughgarden2005 | **no citada** | Citarla (p. ej. en el Teorema 3.6 o en el Ej. 3.7) o borrarla; corregir "30 entradas, todas citadas" en README y RESPUESTA. |
| (nueva) morrisUi2004 | verificada (GEB 49, 260–287) | Añadir para la Prop. 5.3 (m5). |
| (nueva, opcional) Vavasis 1990, "Quadratic programming is in NP", *Inf. Process. Lett.* 36, 73–77 | de memoria; cotejar | Para la pertenencia a co-NP en la Proposición de M1. |

Ninguna entrada de la ronda 1 quedó "no verificada". Las 24 restantes fueron verificadas en la ronda 1 y no las rehice.

## 4. Verificación computacional

- **Reproducción completa** (copia limpia en `scratchpad/referee2_EQO001/run2/`): `commodity_cone.py` 7.0 s de pared / 5.5 s de CPU; `traffic_poa.py` 5.1 / 4.2 s; `welfare_cone.py` 1 min 59.7 s / 1 min 46.7 s. Los tres JSON son **idénticos campo a campo** a los publicados (salvo `seconds`); los `tables_*.md` son idénticos salvo la línea de tiempo; `make_numbers.py` sobre los JSON reproducidos da un `numbers.tex` idéntico salvo los tres macros de segundos, y `table_random.tex` idéntico. Ningún "CRITERION FAILED".
- **Compilación** (`latexmk` en una copia, `repro/manuscript/`): 14 páginas, 0 *Overfull*, 0 referencias o citas indefinidas, `pdftotext | grep -c "??"` = 0; la bibliografía impresa tiene 29 entradas (falta `roughgarden2005`).
- **Ejemplo 5.7, a mano:** $C_1=3-4f_B+2f_B^2+f_Bf_D$ y $C_2=\tfrac14-\tfrac12f_D+\tfrac54f_D^2+f_Bf_D$ (hessianos de determinante $-1$); equilibrio $(1,0)$ con jacobiano reducido $\begin{psmallmatrix}2&1\\1&5/4\end{psmallmatrix}\succ0$; gradientes $(0,1)$ y $(0,\tfrac12)$, luego $\Lone=\R^2_+$; las cuatro aristas como en el texto (en $f_D=1$, $\min_s(3-3s+2s^2)=\tfrac{15}8$; en $f_B=0$, $t=\tfrac15$ con valor $\tfrac15$); umbral $\lambda_1+\tfrac14\le3\lambda_1+\tfrac15\iff\lambda_1\ge\tfrac1{40}$. Comprobación de coherencia que el texto no hace explícita: la región en que el hessiano es semidefinido positivo, $\lambda_1\in[4-\sqrt{15},4+\sqrt{15}]\approx[0.127,7.87]$, está contenida en $\{\lambda_1\ge\tfrac1{40}\}$, y para $\lambda_1>7.87$ el análisis por aristas también da pertenencia; no hay contradicción. $f^*$ es además el único óptimo utilitario (hessiano con autovalores $1.11$ y $5.39$).
- **Ejemplo 5.7, cálculo independiente** (`check_ex57.py`, sin el código del autor: rejilla $1001^2$ más L-BFGS-B, 3 s): umbral bisecado $0.0249999999995$; brecha para $\lambda=(0,1)$ igual a $0.05$ en $(0,0.2)$; brecha $0.01=\tfrac1{20}-2\lambda_1$ en $\lambda_1=0.02$; 89/91 direcciones en $\Lam$ (frontera en $\arctan40=88.57^\circ$); pertenencia para $\lambda_1\in\{0.03,0.1,5,10,50,1000\}$. Todo coincide con E5a.
- **Ejemplo 5.6:** cálculo a mano repetido (correcto). La variante con $\varepsilon=0.2$ coincide con la forma cerrada $\varphi$ de M3 a $1.1\times10^{-8}$ (solo lectura de los JSON).
- **Tres mercancías** (M2): `search2_m3.py` 28 s y `confirm_m3.py` 5 s.
- **Datos de E1c y E5b** (m1, m6): lectura de los JSON, sin cómputo apreciable.
- **CPU total del árbitro:** ≈ 3 min 10 s (reproducción ≈ 1 min 56 s; búsquedas de M2 ≈ 50 s; el resto, pocos segundos). Dentro del presupuesto de 5 min.

## 5. Lista de acciones (prioridad descendente)

1. Sustituye la Pregunta 8.1(ii) por una proposición demostrada: la co-NP-completitud de decidir $\lambda\in\Lam(x^*)$, y la co-NP-dificultad de decidir $\Lam=\Lone$, por la reducción de M1, válida con $F$ fuertemente monótono. Reescribe 8.1(i) con un criterio de éxito comprobable (clases concretas de juegos) o elimínala. Actualiza resumen, Tabla 2, "Next steps", README, ficha y CONTINUIDAD:76.
2. Resuelve la expectativa de la Pregunta 8.2: incluye un ejemplo de tres mercancías con frontera curva, calculando en forma cerrada el mínimo sobre la cara competidora (punto de partida: la instancia de M2) o, como mínimo, informa el hallazgo numérico. Reformula la parte "identify the network structures" con un criterio comprobable.
3. Demuestra la variante fuertemente monótona del Ej. 5.6 con la fórmula $\varphi$ de M3. Cambia "numerically" en 293 y 332, haz que E2c compare con $\varphi$ y cierra CONTINUIDAD:78.
4. Recorta a ≤11 páginas (o a 10): Apéndice B a cinco líneas, Tabla 2 a `results/CLAIMS.md`, pruebas de la Prop. 3.1 y de los Lemas 2.6 y 3.4 a citas, Prop. 4.1(c) a una frase, párrafos de §6 sin cifras duplicadas, panel izquierdo de la Figura 2 fuera.
5. Fusiona E1c con E1b o dale contenido propio con costos no afines (m1); corrige el Remark 3.6 y §6 sobre $\gamma=\mu/L^2$ en E2c (m2).
6. Suaviza "never determines" en el resumen y "ni implica ni excluye" en el README, o añade a la Prop. 5.3 el argumento de dos líneas de m3.
7. Añade a 5.1(e) la implicación "débil eficiencia local ⇒ $\Lone\ne\{0\}$" (Motzkin) y precisa el alcance de Dubey (m4, m9). Cita Morris–Ui (2004) en la Prop. 5.3 y alinea la RESPUESTA con el Remark 5.2 (m5).
8. Informa E5b por patrón de caras activas y separa los testigos de eje de los interiores (m6). Aclara las coordenadas reducidas en el Ej. 5.7 (m7) y la observación de m8 en la Pregunta 8.2.
9. Bibliografía: cita o borra `roughgarden2005` y corrige "30 entradas, todas citadas"; añade `number={4}` y `doi` a Danskin y `number={2}` a Murty–Kabadi; añade Morris–Ui (2004) y, si se usa M1, Vavasis (1990) tras cotejarla.
10. Ficha y README: estado condicional, preguntas abiertas actualizadas tras 1–3, "numéricamente" donde corresponda (m10). Quita `table_pigou.tex` de `make_numbers.py` (m11) y corrige "148 macros" (m12).
