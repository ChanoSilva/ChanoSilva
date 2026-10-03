# Respuesta del autor — LMI001, ronda 2 de revisión interna (03/10/2026)

Informe atendido: `REFEREE_LMI001_ronda2_20261003.md` (veredicto: cambios mayores, solo de texto; 0 bloqueantes, 3 mayores, 15 menores, más 6 puntos de la ronda 1 aplicados a medias o con error nuevo). Manuscrito resultante: **v0.3** (3 October 2026).

Documento escrito de forma incremental durante la sesión; el estado final de cada punto está en su fila.

## Resumen

- **Recuento:** 18 hallazgos nuevos (0 bloqueantes, 3 mayores, 15 menores): **17 aceptados, 1 aceptado con matiz (m6: además de agrandar las fuentes, la figura sale del manuscrito por extensión), 0 rebatidos.** Los 6 puntos de la ronda 1 que el árbitro marcó como aplicados a medias o con error nuevo quedan corregidos.
- **M1, M2 (atribución):** aceptados. El Teorema 3.2(b) y el Lema 3.1 pasan a literatura (Hofmann–Buhmann 1997; Roth et al. 2003; Dhillon–Guan–Kulis TR 2005 y TPAMI 2007); el Teorema 3.2(f) y la Prop. 3.5(i) pasan a literatura (Sejdinovic et al. 2013; França–Rizzo–Vogelstein 2021). Cuatro referencias nuevas, verificadas con WebSearch. Resumen, Introducción, título, README y ficha describen la contribución nueva como **pequeña**.
- **M3 (alcance del Teorema 4.1):** aceptado. Tres funciones concretas, no clases; la media por resorte solo con pesos 1 y 1/n_c; certificado sobre valores, no sobre minimizadores; el patrón 12/12 sale del enunciado.
- **Números:** ninguno cambia. No se repitió ninguna corrida (cambios solo de texto); se regeneraron macros y figura desde los JSON existentes.
- **Compilación:** 13 → 12 páginas, 0 errores, 0 referencias o citas indefinidas, 0 cajas desbordadas, `pdftotext | grep -c "??"` = 0; 35 entradas en `refs.bib`, 35 citadas.

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

### Menores

| Id | Decisión | Qué se cambió y dónde |
|---|---|---|
| m1 (comprobación por (3) en la Prop. 3.5(iii)) | aceptar | Prueba de la Prop. 3.5(iii): "by (3) with K' = K̃ = 2⟨x,y⟩, ΔE = ½(⅔·2·1.5² − 2·2·1²) = −0.5 (equivalently, the bracket of (3), which is ΔJ_{K'} for any symmetric K', with K' = ⟨x,y⟩ and J_{⟨x,y⟩} = SSE)". Recalculado en `scratchpad/check_r2.py`: corchete con 2⟨x,y⟩ = −1.0, ½·corchete = −0.5; corchete con ⟨x,y⟩ = −0.5 (= ΔSSE); ½·corchete con ⟨x,y⟩ = −0.25, como dice el árbitro. |
| m2 (K = σI ∓ A; cita de KDD'04 para 3.2(b)) | aceptar | *Status* de (b): "the ratio association of A, whose maximisation is kernel k-means with K = σI + A [dhillon2005tr, dhillon2007], and minimising E_sp maximises the ratio association of −A, i.e. uses K = σI − A". `dhillon2004` (KDD'04) queda solo en la Def. 2.2 (kernel k-means ponderado). Tabla 2 y resumen citan el TR y TPAMI 2007. |
| m3 (año del TR-04-25) | aceptar | Clave `dhillon2004tr` → `dhillon2005tr`, `year = 2005`, `type = UTCS Technical Report`, `note = Dated 18 February 2005`. Reconfirmado por WebSearch (mismos dos índices que el árbitro); el PDF (people.bu.edu) sigue bloqueado, así que no lo cotejé con el documento. |
| m4 ((d − r)² no es de tipo negativo) | aceptar | Prop. 3.3(iii) dice ahora "(d − r)² is *not* of negative type [proved here (elementary)]", con la prueba de dos puntos (c = (1,−1) da φ(d) ≥ φ(0); φ(r) = 0 < r² = φ(0)). El párrafo *Rest length* demuestra que K̃ no es PD (K̃(x,x) = −2r² si ‖x‖ = r) y que ningún núcleo K̃(x,y) + f(x) + f(y) + a + σ[x = y] con f, a, σ fijos es PD (puntos colineales 0, su, 2su, 3su, c = (1,−1,−1,1): forma cuadrática −8rs + 4σ < 0 si s > σ/2r). Verifiqué la identidad cᵀ(−A)c = −8rs para r ∈ {0.3, 1, 2.5} y s ∈ {0.5, 1, 5, 50} (`check_r2.py`). Queda abierto, y se dice, solo si el Lema 3.1 agota las invariancias (nuevo *Next step* (d)). Tabla 2: "proved here (elementary); other representatives open". E1 pasa a ser una comprobación consistente con lo demostrado. |
| m5 ("every PSD kernel"; dimensión del lift) | aceptar | Remark 3.4(a): "every PD kernel arises this way on finite data". Teorema 3.2(f): "the lift Φ̃∘L takes values in a possibly infinite-dimensional feature space; restricted to the n lifted points it has finite rank, so Definition 2.1 applies with finite D". |
| m6 (fuentes de la Figura 1) | aceptar, y la figura sale del manuscrito | `make_figures.py` dibuja ahora una fila de cinco paneles a 6.3 in (ancho final), con todas las fuentes a 8 pt y caja ajustada (6.21 in de ancho); incluida a `\linewidth` la escala sería 1.01, es decir ≥ 8 pt efectivos. Para llegar a 12 páginas (M8) la figura salió del manuscrito, que remite a `figures/energies.pdf` (opción que el propio árbitro propone en "Extensión", punto 2); la Tabla 1 (E3 por potencial) conserva los números. |
| m7 (nota de continuidad con numeración v0.1) | aceptar | Encabezado "Cómo leer esta nota" que enumera lo que ya no vale; las siete secciones históricas llevan "[histórico v0.1; superado por las rondas 1 y 2]"; en la sección de la ronda 1, "fórmula (6)" → "(3)" (con nota sobre m1) y "M3 Prop. 3.5" → "Prop. 3.5 de v0.1"; nueva sección "Ronda 2". |
| m8 (Estado de la ficha contradice su cabecera) | aceptar | Se elige publicar **solo tras la confirmación**: la cabecera lo dice y el campo Estado ya no lleva "Pendiente de confirmar…". |
| m9 (la redacción de C3a sí cambió) | aceptar | *Disclosure* de E3: "C3a's wording was updated to name the kernel used; its prediction (100%, valid for every PSD representative by Proposition 3.5(ii)), C3b, C3c and all thresholds were written before the pilot and not changed". |
| m10 (*blurring* frente a *mean shift* estándar) | aceptar | Párrafo *The dynamic route*: "mean shift (query points ascend a fixed kernel density estimate) and its blurring variant, in which all data points move [cheng1995]". Tras el Problema 4.2: "For the Gaussian attraction … the flow is a continuous-time, unnormalised form of Gaussian *blurring* mean shift [cheng1995], not of standard mean shift". La Conjetura 4.3 (con su "basins of the density modes", imagen del mean shift estándar) se retira y queda una frase: "We expect no such pair (a, w) to exist for generic (T, ε), but have not tested it" (también es el recorte 6 de "Extensión"). Comprobé el signo: con V(d) = −e^{−d²/2h²}, V'(d) = (d/h²)e^{−d²/2h²} y ż_i = −h⁻²Σ_j e^{−‖z_i−z_j‖²/2h²}(z_i − z_j), atracción hacia una media ponderada sin normalizar. |
| m11 (resumen (vi)) | aceptar | Resumen: "whose fixed points are Voronoi-stable, i.e. Lloyd fixed points with ties broken in favour of the current cluster". |
| m12 (supuesto del control emparejado) | aceptar | Introducción: "We likewise read 'matched kernel control' as kernel k-means on the same affinity matrix with the same optimiser; this too is a reconstruction." También en el resumen, el README y la cabecera de la ficha. |
| m13 (Teorema 4.1: residuo, versiones ensayadas, colapso de tres cuerpos, Cauchy–Binet) | aceptar las cuatro partes | (a) El enunciado define "relative residual ‖b − Πb‖/‖b‖, where b ∈ ℚ⁶³ lists the values of F and Π is the orthogonal projection onto the w-pairwise functions" (coincide con `identity_check.py`: (r²/b²)^{1/2} con b sin centrar; README igual). (b) "Each row is one function F, tested against both families"; la discusión dice que las tres funciones, "all with the per-particle weight 1/n_c inside F (rows 4–6), are neither w_sp- nor w_tot-pairwise; their total-weight versions were not tested". (c) Frase corregida: "restricted to partitions whose clusters all have at least three points, Σ_c w(n_c)/(n_c−2) Σ_{i<j<l}(s_ij+s_jl+s_il) = Σ_c w(n_c) Σ_{i<j} s_ij". (d) Añadido: por Cauchy–Binet sobre las filas (1, x_iᵀ), Σ_{i<j<l∈C} 4·area² = \|C\|·det S_C, así que la fila de tres cuerpos es Σ_c det S_c, una cuártica en los datos. Esbozada en el texto en una frase (Cauchy–Binet; el paso restante es el complemento de Schur de la matriz de momentos); verificada numéricamente para n ∈ {3, 4, 7, 10} (`check_r2.py`). |
| m14 (tiempo de `--fast` en el README) | aceptar | README: "(--fast: ~40 s)". |
| m15 (frase no verificable sobre el representante desplazado) | aceptar (quitar la frase) | E1: "(the shifted representative uses σ up to 4.4×10⁴, so its identity involves cancellation)"; ya no se afirma dónde está el error máximo, que el JSON no guarda por representante. No se repitió la corrida. |

### Puntos de la ronda 1 aplicados a medias o con error (tabla "Verificación de la ronda 1")

| Id (r1) | Estado según el árbitro | Acción en v0.3 |
|---|---|---|
| M2 (comprobación por (3) en 3.5(iii)) | aplicado con error nuevo | Corregido (m1). |
| M5 (sobregeneralización de 4.1; main.tex:65 "genuinely outside the family") | a medias | Frase eliminada; Introducción, resumen, Tabla 2, README y ficha con el alcance exacto (M3). |
| M7 (Prop. 3.6 frente a Dhillon; año del TR) | a medias | Año corregido (m3). El texto ya no dice que Dhillon et al. "observe that a too large diagonal shift degrades the clusters" (no cotejado): dice que "discuss how the diagonal shift affects the practical performance of kernel k-means", que es lo que su resumen de TPAMI 2007 confirma. *Limitations* declara que las atribuciones a França et al. y a la discusión de Dhillon et al. se cotejaron con resúmenes e índices, no con el texto completo. |
| M8 (extensión, 13 páginas) | a medias | 13 → **12 páginas** (véase "Extensión"). |
| m5 (PSD/PD) | a medias | "every PSD kernel" → "every PD kernel … on finite data" (m5). |
| m12 (fuentes de la Figura 1) | a medias | Figura redibujada con fuentes ≥ 8 pt efectivas y movida a `figures/` (m6). |

### Extensión

Antes: 13 páginas (v0.2 recompilada por el árbitro). Después: **12 páginas** a 11 pt, sin quitar ninguna demostración de lo que el manuscrito afirma como propio, y añadiendo las pruebas nuevas (m4, m13(d)) y los párrafos de atribución (M1, M2) y de alcance (M3). Recortes aplicados (numeración del árbitro):
1. Tabla 3 (afirmaciones): **no** se elimina, porque el coordinador pidió actualizarla y el brief exige una tabla de afirmaciones; se compacta (scriptsize, sin el párrafo que repetía las cifras medidas, que ahora es una frase).
2. Figura 1: redibujada (m6) y movida a `figures/energies.pdf`, con una remisión en el texto de E3.
3. E3: las medianas de exceso y la estabilidad medida de los métodos de un movimiento pasan a `results/tables_relaxation.md` (ya estaban allí).
4. Apéndice A: reducido a un párrafo con archivos, semillas, versiones, tiempos y una remisión al README, que recibe la sección "Detalles de implementación" con todo lo que salió (umbrales, tolerancias, clústeres vacíos, propuestas del recocido, generador de E4, eliminación exacta y definición del residuo).
5. Lema CND–PD: la prueba se conserva comprimida en una frase (es de la literatura, pero cuesta dos líneas).
6. Conjetura 4.3: retirada (m10).
Además: la Tabla 1 de E1 (por potencial) sale del manuscrito (sus datos por configuración están en `results/tables_identity.md` y las cifras agregadas siguen en el texto); bibliografía a dos columnas con `\bibsep` menor; resumen y *Next steps* condensados; en el Remark 3.4(b) se quitó la frase sobre el problema de Weber. No se pasó a 10 pt. Llegar a 10 páginas exigiría quitar la Tabla 2 o pruebas; no se hizo.

### Verificación bibliográfica (hecha en esta sesión, con WebSearch; arXiv, PMC, Europe PMC, people.bu.edu y otros espejos están bloqueados por el proxy, así que la verificación es de datos bibliográficos y de resúmenes, no de texto completo)

| Clave | Datos verificados | Fuente de la verificación |
|---|---|---|
| `hofmann1997` (nueva) | T. Hofmann, J. M. Buhmann, "Pairwise data clustering by deterministic annealing", IEEE TPAMI 19(1):1–14, 1997 | WebSearch (índices bibliográficos) |
| `roth2003` (nueva) | V. Roth, J. Laub, M. Kawanabe, J. M. Buhmann, "Optimal cluster preserving embedding of nonmetric proximity data", IEEE TPAMI 25(12):1540–1551, 2003 | WebSearch (IEEE Xplore doc. 1251147; resumen: invariancia del coste de *pairwise clustering* bajo desplazamientos constantes y preservación completa de la estructura de clústeres en la *constant shift embedding*) |
| `sejdinovic2013` (nueva) | D. Sejdinovic, B. Sriperumbudur, A. Gretton, K. Fukumizu, "Equivalence of distance-based and RKHS-based statistics in hypothesis testing", Ann. Statist. 41(5):2263–2291, 2013, doi 10.1214/13-AOS1140 | WebSearch (Project Euclid, ORA Oxford) |
| `franca2021` (nueva) | G. França, M. L. Rizzo, J. T. Vogelstein, "Kernel k-groups via Hartigan's method", IEEE TPAMI 43(12):4411–4425, 2021, doi 10.1109/TPAMI.2020.2998120 | WebSearch (doi.org, PubMed 32750776, PMC8715390). Texto completo no accesible: no pude cotejar si enuncian la inclusión de la Prop. 3.5(ii). |
| `dhillon2004tr` → `dhillon2005tr` | UTCS Technical Report TR-04-25, fechado el 18 de febrero de 2005 (reconfirmado en esta sesión con los mismos dos índices que usó el árbitro; no pude abrir el PDF) | WebSearch (cabecera del PDF de people.bu.edu vía buscador; Bibsonomy). Clave renombrada, `year = 2005`, nota con la fecha. |

No añadí Li & Rizzo (2017, *k-groups*, solo arXiv) porque `franca2021` cubre lo que se le atribuiría y no pude verificar el texto.

### Lista de acciones del árbitro

| Acción | Estado |
|---|---|
| 1. Citar Hofmann–Buhmann y Roth et al.; reetiquetar Tabla 3 y *Status* | hecho (M1) |
| 2. Citar Sejdinovic et al. y França et al.; "proved here" → "literature"; cotejar si França et al. enuncian 3.5(ii) | hecho salvo el cotejo, imposible aquí (texto completo bloqueado); el manuscrito dice "we could not check whether França et al. state it and claim no priority" |
| 3. Corregir main.tex:65, calificar la media por resorte, valores frente a minimizadores, sacar el 12/12 del enunciado | hecho (M3) |
| 4. Comprobación por (3) en 3.5(iii) | hecho (m1) |
| 5. Atribución a Dhillon–Guan–Kulis (K = σI + A; TR 2005, TPAMI 2007) | hecho (m2, m3) |
| 6. (d − r)² no es de tipo negativo; K̃ no PD | hecho (m4) |
| 7. Residuo relativo, versión ensayada, colapso de tres cuerpos | hecho (m13) |
| 8. Nota de continuidad y ficha | hecho (m7, m8) |
| 9. C3a, control emparejado, resumen (vi), PD/lift, blurring mean shift, `--fast`, frase de E1 | hecho (m9, m12, m11, m5, m10, m14, m15) |
| 10. Fuentes de la Figura 1 y recortes 1–6 | hecho con matiz (figura redibujada y movida a `figures/`; Tabla 2 conservada; 12 páginas) |
| 11. Confirmación del autor sobre los supuestos 1 y 2 | **abierto**: no depende de esta sesión; hasta entonces la ficha pública sigue "En pausa" |

### Lo que queda abierto tras la ronda 2

1. Confirmación del autor de la línea sobre los supuestos 1 (familia de pares) y 2 (control emparejado = kernel k-means con la misma matriz y el mismo optimizador).
2. Cotejo con el texto completo de França et al. (2021) —¿enuncian la Prop. 3.5(ii)?— y de Dhillon et al. (TR-04-25, TPAMI 2007) —forma exacta de su discusión del desplazamiento diagonal y fecha del TR—; números de teorema de BCR y SSV.
3. Si el Lema 3.1 agota las invariancias de J (decide si el resorte con longitud de reposo tiene algún representante PD independiente de los datos).
4. Problema abierto 4.2 (vía dinámica, *blurring mean shift*) y caracterización de los pesos de tamaño (Next steps (b), (c)).
5. Extensión: 12 páginas; llegar a 10 exigiría quitar la tabla de afirmaciones o pruebas.

### Cómputo de esta ronda

Sin corridas de experimentos. CPU usada: regeneración de figuras desde JSON (cuatro veces, ~10 s cada una), `check_r2.py` (< 1 s), unas 15 compilaciones de LaTeX (~5 s cada una); en total, del orden de 2 minutos de CPU.
