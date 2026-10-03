# Respuesta del autor — LMI001, ronda 2 de revisión interna (03/10/2026)

Informe atendido: `REFEREE_LMI001_ronda2_20261003.md` (veredicto: cambios mayores, solo de texto; 0 bloqueantes, 3 mayores, 15 menores, más 6 puntos de la ronda 1 aplicados a medias o con error nuevo). Manuscrito resultante: **v0.3** (3 October 2026).

Documento escrito de forma incremental durante la sesión; el estado final de cada punto está en su fila.

## Resumen

(se completa al final)

## Plan de trabajo (orden de aplicación)

1. Verificación bibliográfica con WebSearch de hofmann1997, roth2003, sejdinovic2013, franca2021 y de la fecha del TR-04-25 de Dhillon–Guan–Kulis.
2. Atribución (M1, M2, m2, m3): *Status*, Tabla 3, resumen, Introducción, README, ficha.
3. Alcance del Teorema 4.1 (M3, m13) y Introducción (main.tex:65).
4. Menores m1, m4–m15 y los residuos de la ronda 1.
5. Extensión: ≤ 12 páginas sin perder demostraciones.
6. Compilación, revisión visual, nota de continuidad, README, ficha.

## Respuesta punto por punto

Numeración: "main.tex:N" del árbitro se refiere a la v0.2. En la v0.3 la Tabla 1 (E1) y la Figura 1 salieron del manuscrito (recorte de extensión), de modo que la antigua Tabla 2 (E3 por potencial) es ahora la **Tabla 1** y la antigua Tabla 3 (afirmaciones) es la **Tabla 2**; la Conjetura 4.3 desapareció (m10). El resto de la numeración (Def. 2.1–2.3, Lema 3.1, Teorema 3.2, Prop. 3.3, Remark 3.4, Prop. 3.5, Prop. 3.6, Teorema 4.1, Problema abierto 4.2, ecuaciones (1)–(3)) no cambia.

### Mayores

**M1 (Teorema 3.2(b) y Lema 3.1 = *pairwise clustering* de Hofmann–Buhmann y *constant shift embedding* de Roth et al.) → aceptar.**
El árbitro tiene razón: con diagonal nula, E_sp(C) = Σ_c n_c⁻¹ Σ_{i<j∈C_c} A_ij es exactamente H^pc de Hofmann–Buhmann (1997) para las disimilitudes A_ij, y la reducción a k-means tras un desplazamiento constante es la *constant shift embedding* de Roth et al. (2003). Cambios: (a) párrafo *Status* tras el Teorema 3.2: (b) pasa a "[literature]" con las tres citas (`hofmann1997`, `roth2003`, `dhillon2005tr`, `dhillon2007`) y "Specific to springs is only the constant ½(n−k)φ(0)"; (b) Tabla 2 (antigua 3), fila 2: "literature (Hofmann–Buhmann; constant-shift embedding Roth et al.; ratio association ↔ kernel k-means Dhillon et al.); constant made explicit"; (c) Lema 3.1: el comentario que lo sigue dice ahora "The lemma is elementary and not new" y cita a Roth et al. y Dhillon et al.; en la Tabla 2, "elementary; cf. roth2003, dhillon2007"; (d) E3: el recocido cita a `hofmann1997` junto a `kirkpatrick1983`; (e) Introducción reescrita: la explicación del cribado nulo "is not new … already contained in three literatures"; (f) entradas nuevas en `refs.bib` (verificadas, véase arriba).

**M2 (Teorema 3.2(f), Prop. 3.5(i) y lectura de E3 = estadística de energía) → aceptar.**
Comprobé las identidades: con ρ(x,y) = φ(‖x−y‖) − φ(0) (≥ 0 por el test de dos puntos), el núcleo inducido por la distancia de Sejdinovic et al. con punto base 0 es ½[ρ(x,0)+ρ(y,0)−ρ(x,y)] = K̃/2, su mapa es Φ̃ = Φ/√2, y la dispersión intra-clúster W = Σ_c (n_c/2) g(C_c,C_c) = Σ_c n_c⁻¹ Σ_{i<j} ρ_ij = E_sp − ½(n−k)φ(0), justo la constante del teorema. Cambios: (a) *Status* de (f): "[literature]: ½K̃ is the distance-induced kernel of Sejdinovic et al. …, Φ̃ is its feature map, E_sp − ½(n−k)φ(0) is the within-cluster energy dispersion …, and its equivalence with kernel k-means is in França et al.; we include the short argument"; (b) tras la Prop. 3.5, nuevo *Status*: (i) "[literature]: … kernel k-groups algorithm of França et al."; (ii) "kernel form of the Euclidean inclusion of Telgarsky–Vattani [proved here]; we could not check whether França et al. state it and claim no priority" (no pude leer el texto completo: arXiv, PMC y Europe PMC están bloqueados); (c) Tabla 2: filas de (f) "literature (BCR; Sejdinovic et al.; França et al.); written for spring potentials", Prop. 3.5 dividida en (i) literature y (ii) proved here con la salvedad de prioridad; (d) potenciales (Sección 2): "the string under constant tension, φ(d) = d, whose per-particle energy is the within-cluster dispersion of energy statistics [franca2021]"; (e) lectura de E1–E3: "consistent with França et al., who found Hartigan's method preferable to Lloyd's for kernel k-means". La prueba del lema CND–PD se conserva en una frase (no es nuestra, pero cuesta dos líneas).

**Consecuencia para la contribución (indicación del coordinador) → aceptar.** Tras el cotejo, lo propio es: la síntesis y su lectura para la línea; el mecanismo explícito de la Prop. 3.6 (dos líneas de cálculo; el efecto ya lo discuten Dhillon et al.); la prueba de que (d−r)² no es de tipo negativo y de que ningún núcleo de la clase de invariancias es PD (m4); los certificados exactos del Teorema 4.1 con su alcance acotado (M3); la confirmación computacional E1–E3; y, con salvedad de prioridad no cotejada, la Prop. 3.5(ii). El manuscrito lo dice así: nuevo párrafo *Contribution* en la Introducción ("Its own additions are modest … The new mathematical content is small"), resumen reescrito ("Our own contribution is small: …"), y **título cambiado** de "…: An Equivalence Theorem Behind a Null Screening" a "**Spring-Energy Clustering Is Kernel Clustering: Known Equivalences Behind a Null Screening**". El Teorema 3.2 se titula ahora "Spring energies are kernel objectives; collected from the literature".

**M3 (alcance del Teorema 4.1) → aceptar.**
(1) Introducción (main.tex:65 v0.2): la frase "we certify by exact arithmetic that the ingredients the theorem does not cover are genuinely outside the family" desaparece; el párrafo *Contribution* dice "exact rational certificates that three specific functionals (a triangle-area three-body term, a cluster-mean rest length and a per-spring average) are not pairwise objectives under the per-particle or total normalisation (…; these concern objective values, not minimisers)". (2) Resumen y Tabla 2: la media por resorte se califica ("not pairwise objectives under the per-particle or total normalisation"; en la tabla, "not w-pairwise for w ∈ {1, 1/n_c}"); tras el teorema se dice explícitamente que la media por resorte **sí** es una suma de pares con peso binom(n_c,2)⁻¹. (3) Nuevo párrafo *Values, not minimisers* tras el teorema, con el argumento del árbitro (con A libre toda partición es el minimizador único de alguna función w_tot-pairwise, A_ij = −1 dentro de sus bloques; una transformación creciente no afín en general falla el test sin cambiar minimizadores), y la conclusión de que si estos ingredientes producen un efecto *observable* es otra pregunta. Comprobé el argumento de unicidad: una partición C en k bloques que conserva todos los pares de P es un engrosamiento de P con el mismo número de bloques, luego C = P. (4) La frase del patrón 12/12 sale del enunciado y pasa a la discusión como "a sanity check: one configuration suffices logically". README y ficha se actualizan con el mismo alcance (véase abajo). Además corregí el *Next step* (b), que decía que el método exacto del Teorema 4.1 "applies" al Problema 4.2: el problema trata de minimizadores y el teorema de valores, así que ahora dice que no se aplica directamente.

### Verificación bibliográfica (hecha en esta sesión, con WebSearch; arXiv, PMC, Europe PMC, people.bu.edu y otros espejos están bloqueados por el proxy, así que la verificación es de datos bibliográficos y de resúmenes, no de texto completo)

| Clave | Datos verificados | Fuente de la verificación |
|---|---|---|
| `hofmann1997` (nueva) | T. Hofmann, J. M. Buhmann, "Pairwise data clustering by deterministic annealing", IEEE TPAMI 19(1):1–14, 1997 | WebSearch (índices bibliográficos) |
| `roth2003` (nueva) | V. Roth, J. Laub, M. Kawanabe, J. M. Buhmann, "Optimal cluster preserving embedding of nonmetric proximity data", IEEE TPAMI 25(12):1540–1551, 2003 | WebSearch (IEEE Xplore doc. 1251147; resumen: invariancia del coste de *pairwise clustering* bajo desplazamientos constantes y preservación completa de la estructura de clústeres en la *constant shift embedding*) |
| `sejdinovic2013` (nueva) | D. Sejdinovic, B. Sriperumbudur, A. Gretton, K. Fukumizu, "Equivalence of distance-based and RKHS-based statistics in hypothesis testing", Ann. Statist. 41(5):2263–2291, 2013, doi 10.1214/13-AOS1140 | WebSearch (Project Euclid, ORA Oxford) |
| `franca2021` (nueva) | G. França, M. L. Rizzo, J. T. Vogelstein, "Kernel k-groups via Hartigan's method", IEEE TPAMI 43(12):4411–4425, 2021, doi 10.1109/TPAMI.2020.2998120 | WebSearch (doi.org, PubMed 32750776, PMC8715390). Texto completo no accesible: no pude cotejar si enuncian la inclusión de la Prop. 3.5(ii). |
| `dhillon2004tr` → `dhillon2005tr` | UTCS Technical Report TR-04-25, fechado el 18 de febrero de 2005 (reconfirmado en esta sesión con los mismos dos índices que usó el árbitro; no pude abrir el PDF) | WebSearch (cabecera del PDF de people.bu.edu vía buscador; Bibsonomy). Clave renombrada, `year = 2005`, nota con la fecha. |

No añadí Li & Rizzo (2017, *k-groups*, solo arXiv) porque `franca2021` cubre lo que se le atribuiría y no pude verificar el texto.
