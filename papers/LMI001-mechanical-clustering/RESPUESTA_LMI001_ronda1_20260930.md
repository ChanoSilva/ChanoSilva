# Respuesta del autor al informe de árbitro interno — LMI001, ronda 1 (30/09/2026)

Respuesta redactada el 03/10/2026. Las líneas citadas sin más son las de `manuscript/main.tex` v0.1 (las que usa el informe); "v0.2" se refiere al manuscrito revisado. Decisiones posibles: **aceptado**, **aceptado con matiz**, **rebatido**.

**Recuento:** 26 hallazgos (2 bloqueantes, 8 mayores, 16 menores): 22 aceptados, 4 aceptados con matiz (M5, M7, M8, m6), 0 rebatidos. Las 17 acciones de la lista final están atendidas (la 15, extensión, parcialmente: 15 → 13 páginas; véase M8).

**Qué se rehízo.** Corrida de referencia completa repetida con el código revisado (semillas 20260930 / 20260931 / 20260932 para E4), `numbers.tex` y `table_*.tex` regenerados con `make_numbers.py`, figura regenerada, manuscrito recompilado (0 errores, 0 referencias indefinidas, 0 cajas desbordadas, `pdftotext | grep -c "??"` = 0). Ningún número del texto está escrito a mano.

**Renumeración en v0.2** (afecta a las referencias cruzadas del informe): Corolario 3.4 + Proposición 3.5 → Remark 3.4 (a)/(b); Proposición 3.7 (Hartigan) → **Proposición 3.5**; Proposición 3.8 (regla de Lloyd) → **Proposición 3.6**; Tabla 1 (datasets) eliminada, Tabla 2 (E1) → Tabla 1, Tabla 3 (E3) → Tabla 2, Tabla 4 (afirmaciones) → Tabla 3; Tabla 5 y Figura 2 eliminadas del manuscrito.

## Resumen de decisiones

| Id | Decisión | Dónde se cambió |
|---|---|---|
| B1 | aceptado | resumen, Introducción, "Reading of E1–E3", Limitations, Next steps (a) |
| B2 | aceptado | `FICHA_LMI001_propuesta.md`, `README.md` |
| M1 | aceptado | párrafo *Status* tras el Teorema 3.2, Tabla 3, Introducción |
| M2 | aceptado | Prop. 3.5(iii) y su prueba |
| M3 | aceptado | Remark 3.4(b) |
| M4 | aceptado | Teorema 3.2(f) y prueba, resumen, README, ficha |
| M5 | aceptado con matiz | resumen, Teorema 4.1 (dos configuraciones), texto tras 4.1, Tabla 3, README, ficha |
| M6 | aceptado | E3 (*Disclosure*), macro `\EoneMaxSigma`, docstring de `relaxation.py`, E1 usa K̃ |
| M7 | aceptado con matiz | Prop. 3.6 (etiqueta y nota), `refs.bib` (+dhillon2004tr), nota de continuidad |
| M8 | aceptado con matiz | recortes 1–6 y 8 aplicados; 15 → 13 páginas a 11 pt |
| m1–m16 | aceptados (m6 con matiz) | véase la sección de menores |

## Hallazgos bloqueantes

### B1 — La familia es una reconstrucción no confirmada presentada como hecho
**Aceptado.** Es cierto: el manuscrito v0.1 no decía en ninguna parte lo que la nota de continuidad reconocía. Cambios en v0.2:
- Resumen, segunda frase: "No manuscript or code of that screening was available to us; Section 2 reconstructs the family from the line's public summary as *pairwise* spring energies (…), and this note shows that, for that pairwise family, the null result is a theorem."
- Introducción, en cursiva tras la descripción de la línea: "The definitions of Section 2 are a reconstruction from the line's public summary; no manuscript or code of the original screening was available to us, and the conclusions below apply to objectives of that pairwise form."
- Párrafo "Reading of E1–E3": "If the screened formulations were of the pairwise kind of Definition 2.1, the screening could not have found a mechanical effect: …".
- Limitations, primera frase, y Next steps (a): confirmar con el autor; si no se confirma, el énfasis pasa a la Sección 4.
- Título acotado (m3) en el mismo sentido.
Queda abierto, y así se dice en la nota de continuidad y en la ficha: la confirmación del supuesto por el autor de la línea antes de cualquier difusión.

### B2 — La ficha cierra la línea y afirma más de lo demostrado
**Aceptado.** Ficha: Estado → "Activa — borrador v0.2 en revisión interna (una ronda aplicada); mantener 'En pausa' en el CV hasta confirmar el supuesto de reconstrucción". Hallazgos → "Con aritmética exacta se certifica, en dos configuraciones explícitas, que el término de tres cuerpos (área de triángulo), la longitud de reposo adaptativa (media del clúster) y la normalización por resorte ensayados no son objetivos de pares". Alcance → "Si las formulaciones cribadas eran de pares, el cribado nulo es consecuencia de la equivalencia…". README: la "Conclusión para la línea" se condiciona igual y se añade la advertencia de que la familia es una reconstrucción. El contraejemplo del árbitro (términos de tres cuerpos que colapsan a sumas de pares) se incorpora al manuscrito con un matiz (véase M5).

## Hallazgos mayores

### M1 — Teorema 3.2(b) y (e) etiquetados "proved here"
**Aceptado.** (b) es la lectura "ratio association ↔ kernel k-means" de Dhillon–Guan–Kulis aplicada a la afinidad −A; lo propio es solo la identificación E_sp = ½·(ratio association) − ½kφ(0) con la constante explícita. En v0.2: párrafo *Status* tras el enunciado del Teorema 3.2 con las etiquetas (a),(d) elementales; (c) clásico; (b) **literature** (Dhillon et al. 2004, 2007); (e) **classical** (k-means en espacio de características, Zha et al. 2001, Girolami 2002); (f) proved here a partir del lema CND–PD de BCR. Tabla 3 con las mismas etiquetas. En la Introducción, "the trace form of kernel k-means and its ratio-association reading" con las cuatro citas. La nota de continuidad ya no llama "demostrado" a (b).

### M2 — Error aritmético en la Prop. 3.7(iii) (ahora 3.5(iii))
**Aceptado.** Comprobado: clústeres {0} y {2, 3.4, 3.6}, centroide 3, SSE = 0 + 1 + 0.16 + 0.36 = 1.52; y por (6) con K' = ⟨x,y⟩, ΔSSE = (2/3)·1.5² − 2·1² = −0.5, luego 2.02 − 0.5 = 1.52. Corregido en el enunciado y en la prueba; la prueba incluye ahora la comprobación por (6). La conclusión (el recíproco falla) no cambia.

### M3 — La Prop. 3.5 enunciaba una no representabilidad que no probaba
**Aceptado.** Corolario 3.4 y Proposición 3.5 se fundieron en el Remark 3.4 (a)/(b) (también por extensión, recorte 6). En (b): "For a general φ, min_y Σ φ(‖x_i − y‖) is a Weber-type location problem; with φ(d) = d the anchored objective is the k-median objective (geometric medians as hubs) [classical]. We make no claim about whether these anchored objectives are of the form (1)."

### M4 — Factor ½ perdido en el Teorema 3.2(f) y en el resumen
**Aceptado.** Comprobación: ‖Φ(x)−Φ(y)‖² = K̃(x,x)+K̃(y,y)−2K̃(x,y) = 2φ(d) − 2φ(0), de modo que E_sp = ½·Hooke(Φ) + ½(n−k)φ(0). Se adoptó la primera opción del árbitro: Φ̃ = Φ/√2, con ‖Φ̃(x)−Φ̃(y)‖² = φ(d) − φ(0) y la identidad exacta E_sp(C) = E_{d²,Φ̃∘L,sp}(C) + ½(n−k)φ(0); el enunciado añade entre paréntesis que sin reescalar E_sp es la *mitad* de la energía de Hooke de Φ más la constante, y la prueba incluye el paso "scaling a configuration by 1/√2 halves every squared distance" y el caso Hooke (K̃ = 2⟨x,y⟩, Φ = √2 x, Φ̃ = x). Resumen: (ii) "up to an additive constant and a factor ½"; (iii) "up to an additive constant, the Hooke energy of a lifted configuration (feature map rescaled by 1/√2)". README y ficha: se eliminó "literalmente".

### M5 — Sobregeneralización del Teorema 4.1
**Aceptado con matiz.** Aceptado: en resumen, Tabla 3, texto tras el Teorema 4.1, Limitations, README y ficha se habla ahora de "the three-body (triangle-area) term, the cluster-mean rest length and the per-spring average tested here", y el texto dice explícitamente que el teorema certifica los tres funcionales ensayados, no las clases. Segunda configuración: E4 usa ahora un generador propio (`default_rng(SEED+2)` = 20260932, véase m8) que produce dos configuraciones, P₁ = (5,10),(6,2),(4,4),(2,2),(3,7),(0,6),(8,8) y P₂ = (0,2),(7,4),(8,7),(5,0),(2,8),(2,3),(4,10); el patrón sí/no coincide en las 12 celdas (macro `\EfourCellsSame`), la tabla del teorema muestra los residuos relativos de ambas (P₁; P₂) y `results/tables_identity.md` las dos tablas completas. Las configuraciones de la corrida v0.1 (maestra y `--fast`) ya no se usan porque dependían del estado del generador tras E1–E2; el patrón de representabilidad es el mismo que en aquellas. *Matiz:* el contraejemplo del árbitro Σ_{i<j<l}(s_ij+s_jl+s_il) = (n_c−2)Σ_{i<j}s_ij (válido para n_c ≥ 3) lleva el peso de tamaño (n_c−2), de modo que, tal cual, no es w-pairwise para w ∈ {1, 1/n_c} (la definición del Teorema 4.1); lo que demuestra es que "términos de tres cuerpos" como clase no es lo que sale de la familia, porque una suma de tres cuerpos con un peso de tamaño adecuado colapsa a una energía de pares. Así se escribió en el manuscrito ("The class statements would be false: for clusters of size n_c ≥ 3, …, so a three-body sum with a suitable size weight collapses to a pairwise energy").

### M6 — Cambio a posteriori de la línea base de E3 no revelado; "σ up to 10⁴"
**Aceptado.** (1) En E3, nuevo inciso *Disclosure*: "a pilot run used −A+σI as the only Lloyd kernel and found it inert (Proposition 3.6); K̃ then replaced it as the baseline, which favours the kernel side of the comparison, and the naive shift was kept as a control. C3a–C3c and their thresholds were written before the pilot and were not changed; every number reported comes from the final code." (2) "σ is up to 10⁴" → macro `\EoneMaxSigma` generada desde `results_identity.json` (máximo de `E1.rows[].sigma`): 4.4×10⁴. (3) Docstring de `relaxation.py` reescrito (métodos, historial de la línea base, C3a referida al kernel usado). (4) Opcional adoptado: en E1 las particiones "de kernel k-means" se generan ahora con Lloyd y relajación sobre K̃ (desplazado mínimamente si es indefinido), como en E3; el texto de E1 lo dice. Esto cambió las particiones no aleatorias de E1 y el estado del generador para E2, por lo que la corrida de referencia se repitió completa (véase "Verificación computacional"); las conclusiones no cambian.

### M7 — Novedad de la Prop. 3.8 (ahora 3.6) frente a Dhillon et al.
**Aceptado con matiz.** No pude leer el texto de dhillon2007 ni de dhillon2004 (dominios `cs.utexas.edu`, `bigdata.oden.utexas.edu`, `people.bu.edu`, `dl.acm.org` bloqueados por el proxy de esta sesión, como le ocurrió al árbitro). La búsqueda web devolvió resúmenes del informe técnico UTCS TR-04-25 ("A unified view of kernel k-means, spectral clustering and graph cuts", Dhillon, Guan y Kulis, 2004; versión previa del artículo de 2007) que confirman la observación del árbitro: "although adding a diagonal shift does not change the global optimal clustering, adding too large a shift may result in a decrease in quality of the clusters produced", con una fórmula para la distancia de un punto al centroide de su propio clúster bajo el desplazamiento. En consecuencia: la Prop. 3.6 pasa a "[proved here; explicit form of an effect noted by Dhillon et al. 2004 (TR), 2007]", con una frase tras la prueba ("already observe that a too large diagonal shift degrades the clusters that kernel k-means finds; the proposition is the explicit mechanism and E3 quantifies it"); misma etiqueta en la Tabla 3; se añadió la entrada `dhillon2004tr` a `refs.bib`. *Matiz:* la atribución se basa en resúmenes de buscador, no en el texto; la nota de continuidad lo deja marcado como pendiente de verificación (números de sección y la fórmula exacta de los autores, que el resumen presenta con signo distinto al nuestro para el clúster propio).

### M8 — Extensión: 15 páginas frente a 5–10
**Aceptado con matiz.** Aplicados los recortes 1–6 y 8 del árbitro: Apéndice B (Tabla 5) eliminado y remitido a `results/tables_relaxation.md`; Figura 2 eliminada del manuscrito (el archivo `figures/partitions.*` se conserva y el README lo menciona); Tabla de afirmaciones reducida a las afirmaciones matemáticas (14 filas) con lo "verified" en una frase; Apéndice A fundido en un párrafo; Sección 2 compactada (Definiciones 2.1 y 2.2 fundidas, Ejemplo 2.3 en prosa, Tabla 1 de datasets eliminada y su contenido en el párrafo "Data and potentials"); Sección 3 (Corolario 3.4 y Prop. 3.5 → Remark 3.4; observación "Rest length" dentro de la prueba de la Prop. 3.3); Introducción fundida en un párrafo; bibliografía en `\footnotesize` con `abbrvnat`. Figura 1 en 2×3 paneles (m12). Resultado: **13 páginas** a 11 pt (cuerpo hasta la página 11, bibliografía 1.6 páginas). Las adiciones que exige el propio informe (declaraciones B1 y M6, párrafo *Status*, segunda configuración de E4, matices de M3/M5/M7) cuestan alrededor de una página. Bajar a ≤ 10 exigiría, además, pasar a 10 pt (≈ −1.8 páginas) o suprimir contenido verificable (la prueba incluida del lema CND–PD, los detalles de la prueba de la Prop. 3.5, la tabla de afirmaciones); no lo hice. El ejemplo de referencia del repositorio (MRT001) tiene 18 páginas a 11 pt, así que entiendo el tope de 10 como orientativo; si el coordinador prefiere 10 pt, es un cambio de una línea en `\documentclass`.

## Hallazgos menores

- **m1** — aceptado. Prop. 3.5(ii): "…so it is a fixed point of Lloyd's algorithm for K' with ties broken in favour of the current cluster"; en la prueba, "(not necessarily strictly, whence the tie rule)". Se cita a Selim–Ismail (1984) sobre la relación entre puntos fijos de Lloyd y optimalidad local (con ello la entrada deja de ser huérfana, m11).
- **m2** — aceptado. En la prueba: "if J_{K'} = J_K + const on partitions then ΔJ_{K'} = ΔJ_K for every move, and the identity holds for both matrices, so the right-hand side of (6) is the same for every such K'"; el cálculo explícito con σI se conserva porque alimenta la Prop. 3.6.
- **m3** — aceptado. Título: "Spring-Energy Clustering Is Kernel Clustering: An Equivalence Theorem Behind a Null Screening" (la propuesta del árbitro). Sección 2 renombrada "The pairwise spring family"; README y ficha actualizados.
- **m4** — aceptado. Teorema 3.2(f): "a PD kernel on R^D that does not depend on the dataset (given the scales ℓ, r, s that enter φ and L)"; resumen: "that does not depend on the dataset once the scales are fixed".
- **m5** — aceptado. Convención fijada en el preámbulo de la Sección 2: "PSD" siempre para matrices; "positive definite (PD)" para kernels cuyas matrices de Gram son PSD (convención de BCR). Enunciados y Tabla 1 (E1) usan "PSD" para matrices y "PD" para kernels.
- **m6** — aceptado con matiz. Se citan BCR Cap. 3 §2 Lema 2.1 (lema CND–PD, en la prueba de 3.2(f)) y Teorema 2.2 (Schoenberg, en la prueba de la Prop. 3.3), y la representación de Lévy–Khintchine como [ssv2012, Thm. 3.2] en la Definición 2.3. Los números coinciden con mi recuerdo y con el del árbitro, pero no pude cotejarlos con los libros en esta sesión; la prueba de la Prop. 3.3 mantiene "we do not vouch for the exact numbering of the composition result" y la nota de continuidad los lista como pendientes de verificación.
- **m7** — aceptado. `relaxation.py` llama a `is_hartigan_stable()` para lloyd+relax, relax y anneal (antes `hartigan=True`); resultado medido 600/600, 600/600 y 150/150, reportado en E3 como "(measured; expected by construction)"; `tables_relaxation.md` ahora refleja una medición. Docstring explicado.
- **m8** — aceptado. E4 usa `np.random.default_rng(SEED + 2)` (20260932) y produce dos configuraciones, independientes de `--fast` y del estado del generador tras E1–E2; el Apéndice A y el enunciado del Teorema 4.1 lo dicen. Consecuencia: la configuración cambió respecto de v0.1 (véase M5).
- **m9** — aceptado. README y ficha ya no destacan el reparto 5/1; el manuscrito lo reporta con la aclaración "the split is optimiser noise: the --fast run gives 3–3 with the same 6/30".
- **m10** — aceptado. Docstrings y comentarios de `mechanical.py`, `identity_check.py` y `relaxation.py` alineados con la numeración de v0.2 (Teorema 3.2(b)/(f), Prop. 3.3, Prop. 3.5(ii), Prop. 3.6, Teorema 4.1); las etiquetas `kernel_used` del JSON pasan de `theorem1f(+shift)` a `canonical(+shift)` y `make_numbers.py` las lee así.
- **m11** — aceptado. `refs.bib`: eliminadas aloise2009, shimalik2000 y vonluxburg2007; selim1984 se cita (m1); añadida dhillon2004tr (M7); 31 entradas, 31 citadas. Macros: `make_numbers.py` ya no genera `\EoneFailures`, `\EthreeMaxBestExcess*`, `\EthreeMeanFracReach*`, `\EthreeAriMin` ni `\EfourNconfigs`; quedan 8 macros no usadas por el manuscrito (las Runs/Voronoi/Hartigan/MedianExcess de lloyd, naive y anneal), generadas sistemáticamente por método, y así consta en la cabecera de `numbers.tex`.
- **m12** — aceptado. Figura 1 en 2×3 paneles con leyenda en el sexto panel y fuentes de 8–9 pt (`make_figures.py`), a 0.8 del ancho de texto; Figura 2 fuera del manuscrito (el archivo se conserva).
- **m13** — aceptado. 0 cajas desbordadas en `results/log_build.txt`: ecuación de la prueba de (b) partida en dos, tablas con `\tabcolsep` menor y columnas `p{}` con `\raggedright` en la tabla de afirmaciones, lista de puntos de E4 en `gather*`.
- **m14** — aceptado. Fecha fija: "Working draft v0.2 (one round of internal review applied) — research line LMI001 — 3 October 2026".
- **m15** — aceptado. "no experiment on objective values can separate them (experiments on optimisers can, Section 5)".
- **m16** — aceptado. Cabecera de la Tabla 1 (E1): "neg. type (Prop. 3.3)", y el pie dice "a label, not a computation".

## Bibliografía
- Verificadas por el árbitro (sahni1976, wright1977, telgarsky2010, zha2001, bcr1984): sin cambios de datos; bcr1984 ahora con números de lema/teorema (m6); zha2001 se deja con year 2002 / NIPS 2001 (MIT Press 2002).
- ssv2012: se añadió la referencia al teorema de representación (Thm. 3.2) en la Definición 2.3 (número no verificado en esta sesión).
- dhillon2004, dhillon2007: ahora respaldan también 3.2(b) (M1) y la Prop. 3.6 (M7). Nueva entrada dhillon2004tr (informe técnico UTCS TR-04-25, 2004): existencia confirmada por la búsqueda web (título y PDF en `people.bu.edu/bkulis/pubs/spectral_techreport.pdf`), año y número tomados de la numeración del informe; marcada como no verificable en la nota de continuidad.
- Entradas sin citar: aloise2009, shimalik2000, vonluxburg2007 eliminadas; selim1984 citada.
- Las 24 entradas "no verificables en línea" del informe siguen marcadas así en la nota de continuidad; no se inventó ni se borró ninguna que se cite con razón.

## Verificación computacional (corrida de referencia repetida, 03/10/2026)
- `identity_check.py` (E1, E2, E4): 159 s de pared (en paralelo con E3, 4 núcleos compartidos), salida 0. `relaxation.py` (E3): 128 s, salida 0. Prueba previa `--fast` en una copia aislada: 21 s. Compilaciones: 4 pasadas de `build.sh`. Cómputo total de la ronda ≈ 6–7 minutos de CPU.
- E1: 19 285/19 285 comprobaciones, error máximo 1.1×10⁻¹¹ (igual), Hooke vs SSE 3.9×10⁻¹⁶ (antes 3.8), cociente total/por partícula en [29.7, 197.5] (antes 205.3; cambian las particiones no aleatorias por M6(4)), K̃ PSD 25/25 e indefinido 5/5, σ máximo 4.4×10⁴.
- E2: 90/90 trayectorias idénticas, discrepancia final 1.4×10⁻¹⁴ (antes 2.7×10⁻¹⁴), media 4.9 barridos, máximo 11 (antes 10), 56 s frente a 0.6 s (antes 86 / 0.7; cambian los sorteos por M6(4)); anclados 15/15, inercia a 4.3×10⁻¹⁶.
- E3: idéntico a v0.1 en todas las cifras (el flujo del generador no cambió): Voronoi 600/600 y 150/150; alcanzan E* 28/25/14/20/6; distinguibles 6/30 (5/1, máx. 7.4×10⁻³); ARI = 1 en 24/30; estabilidad de un movimiento de Lloyd 204/600 (34 %) y 38/600 (6 %); recomputación directa 4.3×10⁻¹³. Nuevo: estabilidad de un movimiento **medida** en relax, lloyd+relax y anneal: 600/600, 600/600, 150/150.
- E4: dos configuraciones (seed 20260932); rangos 21 (w_sp) y 22 (w_tot) en ambas; residuos relativos (P₁; P₂): Hooke-sp sí (0; 0) / no (0.017; 0.015); Hooke-tot no (0.179; 0.179) / sí (0; 0); reposo fijo sí (0; 0) / no (0.026; 0.030); reposo adaptativo no (0.143; 0.157) / no (0.109; 0.122); tres cuerpos no (0.331; 0.328) / no (0.039; 0.037); por resorte no (0.185; 0.180) / no (0.125; 0.121). Patrón idéntico en 12/12 celdas y coincidente con el de las configuraciones de v0.1.
- Manuscrito: 13 páginas, 0 errores, 0 referencias/citas indefinidas, 0 cajas desbordadas; páginas 7–11 (tablas y figura) revisadas visualmente.

## Lo que queda abierto
1. Confirmación por el autor de la línea de que las formulaciones cribadas eran de pares (B1); hasta entonces la ficha debe seguir "En pausa".
2. Verificación contra el texto de Dhillon–Guan–Kulis (TR-04-25 y TPAMI 2007) de la observación sobre el desplazamiento diagonal y de los datos del informe técnico (M7); verificación de los números de BCR (Cap. 3 §2, Lema 2.1, Teorema 2.2) y de SSV (Thm. 3.2) (m6).
3. Extensión: 13 páginas a 11 pt frente al objetivo de 10 (M8); opciones descritas arriba.
4. Problema abierto 4.2 y Conjetura 4.3: sin cambios (formulados, no probados ni testeados).
