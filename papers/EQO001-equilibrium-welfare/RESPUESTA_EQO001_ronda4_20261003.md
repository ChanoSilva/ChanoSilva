# Respuesta del autor al informe de ronda 4 — EQO001 (03/10/2026)

Estado: **terminado** (03/10/2026).

Objeto: borrador v0.4 → v0.5 (fecha fija 3 October 2026). Atiende el informe `REFEREE_EQO001_ronda4_20261003.md` (veredicto: cambios menores; 0 bloqueantes, 2 mayores, 12 menores). El árbitro confirma, con verificación a mano y código propio, el Teorema 5.12, la Observación 5.13 y el Corolario 5.14 (208/208 instancias con rutas explícitas y 14/14 DAG, 0 discrepancias).

## 0. Resumen

- **Recuento:** 12 aceptados (M1, M2, m2–m12), 2 aceptados con matiz (m1, por la elección de símbolos, y los recortes de extensión de §6, por el resultado en páginas) y 0 rebatidos. Todos los puntos de la lista de acciones (§7 del informe) están aplicados. También se corrigieron los tres residuos de la tabla "Verificación de la ronda 3": m8 de la ronda 3 (extensión), $\mathbb R^{n+2}_+$ a medias y el punto 5 de §1.4 de la RESPUESTA de la ronda 3.
  - **M1 → aceptado.** El enunciado del Cor. 5.14 ya no dice "Theorem 5.12 holds". Ahora enumera lo que vale en el DAG:
    - co-NP-completitud con todas las rutas;
    - dureza con $\lambda=e_W$, $f^*$ único equilibrio y vértice de $K$, $\Lambda_1$ igual al ortante, demandas enteras;
    - cada arco en rutas de **a lo sumo tres** mercancías;
    - todas las mercancías salvo **dos** ($W$ y el interruptor, que tiene más de dos rutas) con exactamente dos rutas;
    - $F$ **no** fuertemente monótono.

    La prueba añade los dos hechos nuevos: (iv) a lo sumo tres mercancías por arco, y al menos $M+2$ rutas del interruptor. Añade también una dirección tangente explícita con $DF\,h=0$, de modo que $F$ ni siquiera es estrictamente monótono. Se mantiene la reparación $f_e\le D+2$ con su justificación $D+2\le2(D+1)$.
  - **M2 → aceptado.** El caso polinómico "número fijo de mercancías, pesos $\mu\mathbf 1_Q$" lleva ahora "with explicit path sets" en la Pregunta 7.1, en la frase tras la Prop. 5.15, en el README y en la ficha (ES/EN). La Pregunta 7.1 gana la parte (iii): DAG con todas las rutas y número fijo de mercancías, ya con dos y $\lambda=e_W$, que es minimizar una cuadrática convexa más $d_R$ veces una longitud de camino más corto, que es cóncava.
- **Estado de los resultados de ruteo.** Con M1 y M2 aplicados, y como autoriza el árbitro, el Teorema 5.12, la Obs. 5.13 y el Cor. 5.14 pasan a "proved here, Appendix B; checked by an independent internal referee (round 4) and in E8". El cambio está en el texto, en `results/CLAIMS.md`, en el README y en la ficha.
- **Números:** sólo cambian `\RtRandFive` y `\RtRandSix` (40 → 30), por m4. Se añaden cuatro macros (`\RtAllLabelled` = 70, `\RtRandWeighted` = 20, `\RtDagMinPathsZ` = 4, `\RtDagMaxPathsZ` = 20). Los otros 200 macros de la v0.4 son idénticos, comprobado por programa contra la copia de `numbers.tex` de la v0.4 (§3).
- **Compilación:** `latexmk -pdf` con 0 errores, 0 avisos, 0 referencias o citas indefinidas y 0 *Overfull*; `pdftotext main.pdf - | grep -c '??'` = 0; 36 `\bibitem`.
- **Páginas:** el texto principal baja de ≈ 12.4 a **≈ 11.5** (termina hacia la mitad de la p. 12). El total sube de 17 a **18**, la última con un cuarto de página de bibliografía. Mover demostraciones al apéndice no ahorra páginas totales, y M1 y M2 añaden enunciados y una pregunta. No se quitó ninguna demostración ni se tocaron márgenes ni letra.
- **Cómputo:** ≈ 2.8 min de CPU. La re-ejecución del chequeo del integrador costó 141 s; `make_numbers.py` (con la reproducción del generador de E8, ≈ 1 s), unas siete compilaciones y los renderizados de páginas, el resto. E1–E8 no se re-ejecutaron porque su código no cambió.

## 1. Mayores

### M1 (el Corolario 5.14 hereda condiciones falsas) → aceptado

El árbitro tiene razón. "Theorem 5.12 holds, without the strong monotonicity of $F$" arrastraba dos condiciones del teorema, "every edge is used by at most two commodities" y "all commodities but one have exactly two paths", y las dos son falsas en el DAG.

- $e^1_\ell$ y $e^2_\ell$ están en rutas de $W$, del nodo y del interruptor (tipo (iii)).
- El interruptor tiene entre 4 y 20 rutas en E8 (`\RtDagMinPathsZ`–`\RtDagMaxPathsZ`, leídos ahora de la salida).

Cambios en `main.tex`:

- **Enunciado del Cor. 5.14** (texto sustituto del árbitro, completado):
  - "When the input is a directed acyclic graph … both problems of Theorem 5.12 are co-NP-complete when the number of commodities is part of the input."
  - "They remain co-NP-hard when $\lambda=e_W$, $f^*$ is the unique Wardrop equilibrium and a vertex of $K$, $\Lambda_1(f^*)$ is the whole orthant, demands are integers, every arc lies on paths of at most three commodities, and all commodities but two ($W$ and a switch, which has more than two paths) have exactly two paths."
  - "In this construction $F$ is not strongly monotone (Question 7.1(ii))."
- **Prueba (Apéndice B), punto "Paths":**
  - (iii) dice que para cada $\ell$ hay una ruta $q_0,dz,p_\ell,e^1_\ell,e^2_\ell,e^z_\ell$ seguida de la cola de $Z_1$, de modo que el interruptor tiene al menos $M+2$ rutas. La cota se cumple en E8: con $M=2$, 4 rutas; con 2K2 ($M=4$), 6.
  - (iv) nuevo: por (i), un arco está en rutas de a lo sumo un nodo, y por tanto de a lo sumo tres mercancías.
- **Párrafo nuevo "$F$ is not strongly monotone".**
  - La dirección mueve una unidad del interruptor de $Z_0$ a la ruta de tipo (iii) $\mathsf o_z\to q_0\to dz\to p_M\to e^1_M\to e^2_M\to e^z_M\to\mathsf d_z$, y una unidad de $W$ de $T_M$ a $O$.
  - Los arcos de pendiente positiva no cambian de flujo: $dz$ y $q_0$ están en las dos rutas de cada mercancía, y los arcos de $T_M$ ganan al interruptor y pierden a $W$. Por tanto $DF\,h=0$ y $F(f+\tau h)=F(f)$.
  - Es la dirección nula que el árbitro encontró numéricamente (§1.4 de su informe). El enunciado sólo afirma "not strongly monotone".
- **Reparación $D+2$:** se mantiene en "Equilibrium and $\Lambda_1$", ahora con la desigualdad escrita completa: $1+(D+2)\sum_\ell\alpha_\ell<2+2(D+1)\sum_\ell\alpha_\ell=B$.
- **"Used by":** se sustituye por "lies on paths of" también en el enunciado y en la construcción del Teorema 5.12 ("every edge lies on paths of at most two commodities").
- **Archivos acompañantes.**
  - `results/CLAIMS.md`: fila del Cor. 5.14 reescrita con lo que vale y lo que **no** se afirma (fuerte monotonía, ≤ 2 mercancías por arco, "todas salvo una con 2 rutas").
  - `README.md`: viñeta de complejidad en ruteo.
  - Ficha (ES/EN): "con conjuntos de rutas explícitos o con todas las rutas de una red acíclica".

### M2 (frontera de lo tratable sin "rutas explícitas"; caso abierto) → aceptado

Es correcto. La Prop. 5.15(b) enumera perfiles puros y sólo es polinómica con rutas listadas. En un DAG con todas las rutas, un número fijo de mercancías no da un número polinómico de perfiles.

- **Pregunta 7.1:** "with explicit path sets, a fixed number of commodities and weights of the form $\mu\mathbf 1_Q$, membership is polynomial (Proposition 5.15(b))". Además, "Three questions remain", con la nueva (iii): "What is the complexity with all paths of an acyclic network and a fixed number of commodities, already for two commodities and $\lambda=e_W$? Then $\min_K\Phi_\lambda$ is the minimum over $W$'s arc flows of a convex quadratic plus $d_R$ times the shortest-path length of the other commodity $R$ for the arc lengths $a_ef^W_e$, a concave function, and Proposition 5.15(b) does not apply because the paths may be exponentially many."
  - Comprobación del autor: con $\lambda=e_W$, $C_W=\sum_e(a_e(f^W_e)^2+b_ef^W_e)+\sum_ea_ef^R_ef^W_e$. La segunda suma es lineal en el flujo de arco $f^R$ de valor $d_R$, y su mínimo es $d_R\cdot\mathrm{SP}_{a\circ f^W}$, un mínimo de funciones lineales en $f^W$, y por tanto cóncavo.
- **Frase tras la Prop. 5.15** (antes la línea 364): "… unboundedly many weightless ones sharing edges with the weighted paths, which, with explicit path sets, is unavoidable, unless P = NP, for weights of the form $\mu\mathbf 1_Q$ (Proposition 5.15(b)) … With all paths of an acyclic network, the case of few commodities is open (Question 7.1(iii))."
- **Archivos acompañantes.**
  - `README.md`: viñeta de ruteo, donde la antigua línea 44 dice ahora "con conjuntos de rutas explícitos"; viñeta de preguntas abiertas con (iii).
  - `FICHA_EQO001_propuesta.md`: ES "con conjuntos de rutas explícitos, pocas mercancías y pesos iguales"; EN "with explicit path sets, few commodities and equal weights"; "Alcance" y "Current scope" con la pregunta en tres partes.
  - `results/CLAIMS.md`: fila de la Prop. 5.15 y de la Pregunta 7.1.

## 2. Menores

- **m1 (notación) → aceptado con matiz.**
  - $\mathbb R^m_+$ desaparece del manuscrito (`grep` = 0). En los enunciados (Teorema 5.12, Cor. 5.14) se escribe "$\Lambda_1(f^*)$ is the whole orthant", porque allí $n$ no está definido. En las pruebas se escribe $\mathbb R^{n+2}_+$.
  - Los pares orientados pasan de $m$ a $\ell$: $\ell\in A$, $T_\ell$, $\alpha_\ell$, $t_\ell$, $w_\ell$, $p_\ell$, $e^{1,2,z}_\ell$. No usé la sugerencia $a\in A$, porque $a$ ya designa las pendientes $a_e$ y $a_D$ del mismo apéndice. Con $\ell$, la letra $m$ queda sólo como número de mercancías (Def. 2.5).
  - La ruta del nodo pasa de $P_i$ a $U_i$, para no chocar con $P_k$, el conjunto de rutas.
  - La arista $o$ pasa a $e^o$, de modo que $O$ (ruta) y $\mathsf o_k$ (origen) ya no se confunden con ella.
  - La cara de la prueba de la Prop. 5.9 pasa de $\Phi$ a $\mathcal F$.
  - Comprobado con `grep`: no queda `T_m`, `alpha_m`, `P_i` ni `\Phi` sin subíndice $\lambda$.
- **m2 (tipo (iii)) → aceptado.**
  - Prueba del Cor. 5.14: "… so it starts $\mathsf o_z\to q_0\to dz$, then continues along arcs of $W$ and chain connectors, and reaches $\mathsf d_z$ through the tail of the chain $Z_1$, ending with $e^z_M$".
  - Pregunta 7.1(ii): "a path of the switch through $q_0$, $dz$, the arcs $p_\ell,e^1_\ell,e^2_\ell,e^z_\ell$ of some $T_\ell$ and the tail of $Z_1$".
- **m3 ($c_{T_\ell}-c_O$ en el DAG) → aceptado.** "Given $x=0$ and $z=1$, for every flow of $W$, $c_{T_\ell}-c_O\ge-\alpha_\ell+\alpha_\ell f_{e^2_\ell}+2\alpha_\ell f_{e^z_\ell}\ge2\alpha_\ell>0$, since $f_{e^2_\ell},f_{e^z_\ell}\ge1$". Lo rehíce: $c_{T_\ell}-c_O=-\alpha_\ell+\alpha_\ell(f_{e^1_\ell}+f_{e^2_\ell}+2f_{e^z_\ell})$, porque los conectores de $T_\ell$ cuestan 0 y $dz$ es común. Además, con $x=0$ el nodo cabeza carga $e^2_\ell$ y con $z=1$ el interruptor carga $e^z_\ell$.
- **m4 (E8: 30+30, un tercio con pesos) → aceptado.**
  - El generador (`theory/check_routing_hardness.py:448–457`) hace 20 grafos unitarios y 10 con pesos para cada $n\in\{5,6\}$. El "40" venía de una frase fija del log.
  - `make_numbers.py` ya no lee esa frase. Reproduce el generador (misma semilla, mismo orden de sorteos `rng.random()` y `rng.integers`) y calcula el corte máximo por enumeración. Antes de escribir macros comprueba que los totales coinciden con los que el script de `theory/` sí calculó: 130 grafos, 381 pares, 130 miembros y 251 no miembros. Si no coinciden, aborta. `theory/` sólo se lee.
  - Macros: `\RtAllLabelled` = 70, `\RtRandFive` = `\RtRandSix` = 30, `\RtRandWeighted` = 20.
  - Texto de E8: "the 70 labelled graphs with unit weights on 3 and 4 nodes, and 30 + 30 random graphs on 5 and 6 nodes, 20 of them with weights in {1,2,3}". Cuadra: $70+60=130=$ `\RtGraphs`.
  - La frase errónea sigue en `theory/check_routing_hardness_output.txt`, porque `theory/` no se toca. Queda anotada en el README y en CONTINUIDAD.
- **m5 (contradicción en la RESPUESTA de la ronda 3, §1.4 punto 5) → aceptado.** Añadí bajo ese punto una "Nota de corrección, ronda 4". Dice que los macros de E8 sí se generan (`make_numbers.py` 251–285 y `numbers.tex` 182–203 de la v0.4), que el texto no dice que se copien, y que el estado aplicado era "proved here, Appendix B; checked in E8", no "independently re-derived by the author". Añadí otra nota bajo el título de §1 de esa respuesta, por m6.
- **m6 (CLAIMS: "independiente", 54 pares) → aceptado, incorporando el script.**
  - Recuperé `scratchpad/eqo_r3/indep_check.py` y lo copié como `experiments/routing_integrator_check.py`. Sólo cambia el docstring, que dice que es el chequeo del integrador y no una verificación independiente.
  - Lo re-ejecuté (141 s de CPU, un hilo). La salida (`results/routing_integrator_check_output.txt`) es idéntica a la de la ronda 3 salvo las líneas de tiempo, comprobado con `diff`.
  - Fila del Teorema 5.12 en CLAIMS: "demostrado aquí (Apéndice B); comprobado por un árbitro interno independiente (ronda 4: código propio, 208 instancias explícitas, 0 discrepancias); además comprobado por el integrador del resultado en la ronda 3 (no independiente: `experiments/routing_integrator_check.py`, 54 pares …) y en E8 (381 pares, 0 discrepancias)".
- **m7 ("table body used here") → aceptado.** Apéndice A: "turns them into the macros used here". README: `table_random.tex` "se sigue generando, pero ya no se incluye en el manuscrito".
- **m8 (dualidad de PL para $\Lambda_1$ en el DAG) → aceptado.** "By linear-programming duality, $\lambda\in\Lambda_1(f^*)$ iff there are node potentials $\pi_k$ with nonnegative reduced arc costs for the linearised $\Phi_\lambda$ of each commodity $k$, zero on the arcs used by $k$; so $\Lambda_1(f^*)$ is the projection of a rational polyhedral cone in $(\lambda,\pi)$ of polynomial description …".
- **m9 (resumen) → aceptado.** "… with affine costs, with explicit path sets or all paths of an acyclic network, when the number of commodities is part of the input …".
- **m10 (problema de promesa) → aceptado.**
  - Teorema 5.12: "a rational Wardrop equilibrium $f^*$ in path flows (a property checked in polynomial time, the paths being listed)".
  - Cor. 5.14, en la prueba de pertenencia: "(that $f^*$ is a Wardrop equilibrium is checked by shortest paths)".
- **m11 (esbozo) → aceptado.** "… and one with the route $Z_1$ of a switch commodity, which meets every $T_\ell$". También "the route $S_i$ of node $i$" y "the other route $U_j$".
- **m12 (qué literatura se consultó) → aceptado.** Remark 5.2: "We did not find Theorem 5.12 in the work we consulted on the complexity of multiclass and multi-commodity equilibria, on toll design (Hearn–Ramana) and on Stackelberg routing". No añadí la entrada arXiv 1811.08354 que sugiere el árbitro como opcional, porque no pude cotejar sus datos bibliográficos en esta sesión. Queda anotada en CONTINUIDAD.

### Bibliografía (§4 del informe)

- **Schrijver:** "Theorem 10.2" → **"Section 10.2"** en las tres apariciones (pertenencia en la Prop. 5.9, en el Teorema 5.12 y en el Cor. 5.14). El número de teorema no se pudo cotejar con una fuente primaria; la sección sí está confirmada.
- **`kozlovTarasovKhachiyan1980`:** añadido `doi = {10.1016/0041-5553(80)90098-1}`, verificado por el árbitro.
- **`pardalosSchnitger1988`:** sin cambios.
- Siguen 36 entradas, todas citadas. `dubey1986` se cita ahora en el Ej. 5.5, porque el Remark 5.2 recortado ya no lo menciona.

### Extensión (§6 del informe) → aceptado con matiz

Recortes aplicados (texto principal):

| # | Recorte del árbitro | Aplicado |
|---|---|---|
| 1 | Prueba de la variante fuertemente monótona del Ej. 5.6 al Apéndice B | sí; queda el enunciado de $\varphi$ y "(proof in Appendix B)" |
| 2 | Remark 5.2 a la mitad | sí; sin la frase de Dubey (pasa al Ej. 5.5) ni la de la Prop. 5.9 (queda "is a standard reduction (see its status)") |
| 3 | Fundir el párrafo tras la Prop. 5.9 con su estado | sí; se quita el esbozo, que ya está en el Apéndice B, y queda la observación sobre externalidades y no poliedralidad (3 líneas) |
| 4 | E8 a pocas líneas | sí; criterio, familias de grafos (m4), 381 pares, 0 discrepancias, comprobaciones exactas y DAG. El detalle está en la salida guardada |
| 5 | Obs. 5.13 a enunciado más una línea | sí; las cotas de costo de ruta pasan al Apéndice B (párrafo "Interior weights") |
| 6 | Ej. 5.7: prueba al Apéndice B | sí; en el texto queda el resultado y el testigo decisivo $\lambda=(0,1)$, $y=(0,\frac15)$ |
| — | Adicional | pruebas de la descripción de $\Lambda(y^*)$ (Ej. 5.8), del Lema 5.11 y de la Prop. 5.15 al Apéndice B, que pasa a llamarse "Deferred proofs" |

- **Resultado.** El texto principal baja de ≈ 12.4 a ≈ 11.5 páginas y termina hacia la mitad de la p. 12. No llega a las ≈ 11 estimadas por el árbitro porque M1, M2 y m10 añaden unas 10 líneas de enunciado y la Pregunta 7.1(iii).
- **Total.** Pasa de 17 a 18 páginas. La estimación de ≈ 15.5 del árbitro no es alcanzable moviendo pruebas, porque lo que sale del texto principal entra en el Apéndice B.
- **Lo que no se hizo.** No se quitó ninguna demostración ni se cambiaron letra ni márgenes. Separar el material de ruteo en una nota propia, que el árbitro deja a decisión del autor, no se hizo en esta pasada. Queda anotado como opción en CONTINUIDAD.

### Verificación de la ronda 3 (§2 del informe): residuos

- $\mathbb R^{n+2}_+$ a medias: resuelto en m1.
- Punto 5 de §1.4: resuelto en m5.
- m8 de la ronda 3 (extensión): resuelto en los recortes de arriba.
- La ficha decía "(señalada en la revisión interna)", una referencia a la historia interna (detalle de la fila M1). La quité en ES y EN.

### Lista de acciones del árbitro (§7)

| # | Acción | Estado |
|---|---|---|
| 1 | Reescribir el Cor. 5.14; CLAIMS y README | hecho (M1) |
| 2 | "with explicit path sets" en la Pregunta 7.1, en la línea 364, en el README y en la ficha; Pregunta 7.1(iii) | hecho (M2) |
| 3 | E8 (30+30, un tercio con pesos) y macros desde las cuentas | hecho (m4); los macros salen de reproducir el generador, cotejado con los totales calculados |
| 4 | $\mathbb R^{n+2}_+$ y choques de notación | hecho (m1, con $\ell$ en lugar de $a$) |
| 5 | Tipo (iii) y desigualdad de $c_{T_\ell}-c_O$ | hecho (m2, m3) |
| 6 | Dualidad de PL, resumen, comprobación de Wardrop | hecho (m8, m9, m10) |
| 7 | CLAIMS (Teorema 5.12) y RESPUESTA de la ronda 3 | hecho (m5, m6); script de 54 pares incorporado |
| 8 | "table body" y README:17 | hecho (m7) |
| 9 | Esbozo, literatura del Remark 5.2 y Schrijver "Section 10.2" | hecho (m11, m12, bibliografía) |
| 10 | Recortes 1–5 (y 6) | hechos; texto principal ≈ 11.5 pp; la nota aparte para el ruteo queda como opción |

## 3. Números que cambiaron (comprobación por programa)

Comparé `manuscript/numbers.tex` regenerado con la copia de la v0.4 (`scratchpad/eqo_r4/v04/numbers.tex`), macro a macro, con un script que lee cada `\newcommand`. La v0.4 tenía 202 macros y la v0.5 tiene 206.

- **Cambiados (2):**
  - `\RtRandFive` 40 → 30;
  - `\RtRandSix` 40 → 30.

  Motivo: m4. Los valores de la v0.4 venían de una frase fija del log, y los nuevos salen de reproducir el generador.
- **Añadidos (4):**
  - `\RtAllLabelled` = 70 (texto de E8);
  - `\RtRandWeighted` = 20 (texto de E8);
  - `\RtDagMinPathsZ` = 4 (sólo CLAIMS/README; leído de la salida, no se cita en el PDF);
  - `\RtDagMaxPathsZ` = 20 (texto de E8, por M1).
- **Eliminados:** ninguno.
- **Sin cambio:** los otros 200 macros de la v0.4. Algunos de E8 ya no aparecen en el texto tras el recorte 4 (`\RtFWgap`, `\RtHdiff`, `\RtFaceMax`, `\RtFaceDiff`, `\RtFacePairs`, `\RtNonmembers`), pero siguen generándose.

## 4. Archivos modificados

- `manuscript/main.tex` (v0.5), `manuscript/refs.bib` (DOI de KTK), `manuscript/numbers.tex` (regenerado, 206 macros), `manuscript/main.pdf` (18 pp) y `manuscript/table_random.tex` (regenerado; no se incluye en el PDF).
- `experiments/make_numbers.py`: m4 (reproducción del generador de E8 con cotejo) y macros de rutas del interruptor.
- `experiments/routing_integrator_check.py` (nuevo, m6) y `results/routing_integrator_check_output.txt` (nuevo).
- `results/CLAIMS.md`, `README.md`, `FICHA_EQO001_propuesta.md`, `CONTINUIDAD_EQO001_20260930.md` (sección "Ronda 4 de revisión interna (03/10/2026)") y `RESPUESTA_EQO001_ronda3_20261003.md` (dos notas de corrección).
- **No** se modificó nada en `theory/` ni en otras carpetas de `papers/`. No se usó git.
