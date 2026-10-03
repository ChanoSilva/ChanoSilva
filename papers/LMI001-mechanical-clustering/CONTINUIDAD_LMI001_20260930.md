# LMI001 — Continuidad interna, 30/09/2026

Documento de trabajo interno. No incorporar al manuscrito ni a entregas institucionales.

**Cómo leer esta nota (añadido en la ronda 2, 03/10/2026).** Las secciones marcadas "[histórico v0.1]" describen la v0.1 con su numeración y sus etiquetas de estado de entonces, y se conservan como registro; están **superadas** por las secciones "Ronda 1" y "Ronda 2" del final. Desde la v0.4 (sección "Integración de la teoría…", al final) la numeración del manuscrito cambió: Teorema 3.2 → 3.4, Prop. 3.3 → 3.5, Remark 3.4 → 3.8, Prop. 3.5 → 3.9, Prop. 3.6 → 3.10, Problema 4.2 → 4.4; las secciones de las rondas 1 y 2 usan la numeración v0.2/v0.3. Desde la v0.5 (sección "Ronda 3", al final) la Tabla 1 de E3 salió del manuscrito y la tabla de afirmaciones es la **Tabla 1** (antes Tabla 2); la Prop. 4.3 tiene partes (a) y (b). En particular, ya no son válidas: la numeración Prop. 3.7/3.8, Tabla 5, Figura 2; las etiquetas "(demostrado)" de 3.2(b) y 3.2(e) (hoy literatura y clásico); "(f) demostrado" (hoy literatura: Sejdinovic et al. 2013, França et al. 2021); y la frase "no son objetivos de pares" sin calificativo para la media por resorte (hoy: no es de pares con los pesos 1 ni 1/n_c, y el certificado es sobre valores, no minimizadores).

## Proyecto y alcance
Línea LMI001, "Analogías mecánicas para agrupamiento de datos" / "Mechanical analogies for data clustering", área Inteligencia artificial y aprendizaje, estado en el CV web: "En pausa". Ficha pública: estudio de formulaciones de agrupamiento inspiradas en tensión, levantamiento y sistemas mecánicos; objetivo: determinar si el componente mecánico produce un efecto distinguible frente a controles de kernel emparejados; hallazgo: el análisis de cribado no encontró ningún componente mecánico que sobreviviera a esas comparaciones controladas; alcance: la analogía mecánica por sí sola no establece una ventaja algorítmica.

Encargo de esta sesión: convertir el cribado negativo en un teorema que lo explique, más una confirmación computacional, sin cambiar el alcance declarado.

## Supuestos reconstruidos (verificar con el autor)
No existe manuscrito previo ni código de la línea en el repositorio; todo lo que sigue se reconstruyó de la ficha.
1. **Qué es "formulación mecánica".** Se asumió: puntos unidos por resortes con un potencial de pares φ(d) (Hooke con y sin longitud de reposo, cuerda a tensión constante, resorte saturante, resorte logarítmico), opcionalmente tras un levantamiento L (se usó el paraboloide (x, |x|²/s)), con la energía intra-clúster normalizada por partícula (1/n_c) o total. "Tensión" se interpretó como la energía liberada al cortar los resortes entre clústeres; "levantamiento" como una aplicación L previa a los resortes. Se añadió la variante de resortes anclados a un hub porque es la lectura mecánica natural de Lloyd. Si la línea original usaba otra cosa (por ejemplo, láminas elásticas con energía de flexión, o dinámica de partículas), ese caso cae en la Sección 4 del manuscrito ("lo que sale de la familia") y el teorema no lo cubre; el manuscrito lo dice.
2. **Qué es "control de kernel emparejado".** Se asumió: kernel k-means con la misma matriz de afinidad y el mismo optimizador/inicialización. Con esa lectura el teorema dice que control y formulación mecánica son el mismo objetivo.
3. **Normalización.** La identidad exacta con k-means exige la normalización 1/n_c; se decidió tratar la normalización como parte de la definición de la familia y demostrar por separado que la energía total es min-sum k-clustering / max-k-cut. E4 certifica que ambas normalizaciones son objetivos distintos.

## Qué se produjo (todo en `papers/LMI001-mechanical-clustering/`) [histórico v0.1; superado por las rondas 1 y 2]
1. Manuscrito LaTeX `manuscript/main.tex` (inglés, 15 páginas con apéndices y 29 referencias), compilado a `main.pdf` con latexmk (pdflatex + bibtex) sin errores ni referencias indefinidas; quedan 4 cajas horizontales desbordadas menores (≤ 8 pt) (revisar tras la edición final).
2. Biblioteca `experiments/mechanical.py` y dos scripts de experimentos con semilla fija, salida JSON/Markdown, más `make_numbers.py` (macros) y `make_figures.py`. Ningún número del manuscrito está escrito a mano.
3. README, esta nota y una propuesta de ficha.

## Resultados matemáticos (estado) [histórico v0.1; superado por las rondas 1 y 2]
- Lema 3.1 (invariancias de la forma de traza J bajo σI, a·11ᵀ y f1ᵀ+1fᵀ): demostrado, elemental.
- Teorema 3.2: (a) trivial; (b) E_sp = ½J_{−A} + ½(n−k)φ(0), y desplazamiento diagonal ("demostrado" en v0.1; hoy literatura: Hofmann–Buhmann 1997, Roth et al. 2003, Dhillon et al.); (c) Hooke = SSE (clásico); (d) energía total + tensión liberada = constante ⇒ min-sum / max-k-cut (demostrado, elemental); (e) todo objetivo kernel k-means es energía de Hooke de una configuración levantada ("demostrado" en v0.1; hoy clásico); (f) para φ de tipo negativo, kernel universal PD K̃(x,y) = φ(|x|)+φ(|y|)−φ(|x−y|)−φ(0) ("demostrado" en v0.1 a partir del lema clásico CND↔PD; hoy literatura: Sejdinovic et al. 2013, França et al. 2021).
- Proposición 3.3: d² de tipo negativo (clásico, una línea); ψ∘N CND para ψ Bernstein (literatura: Berg–Christensen–Ressel 1984, cap. 3; Schilling–Song–Vondraček 2012; se incluye esbozo vía Lévy–Khintchine y teorema de Schoenberg).
- Proposición 3.7 (v0.1; hoy Prop. 3.5): relajación partícula a partícula = método de Hartigan; fórmula ΔE invariante de representación; todo punto fijo de un movimiento simple es punto fijo de Lloyd para cualquier representante PSD (demostrado; generaliza Telgarsky–Vattani 2010); contraejemplo explícito al recíproco {0, 2, 3.4, 3.6}.
- Proposición 3.8 (v0.1; hoy Prop. 3.6): la regla de Lloyd depende del representante PSD (el desplazamiento σI congela Lloyd para σ grande). Demostrada; es el hallazgo colateral más útil de la sesión: "kernel k-means con Lloyd" no es un algoritmo único para una energía de resortes; la relajación de un movimiento sí lo es.
- Teorema 4.1 (asistido por computadora, aritmética racional exacta, una instancia en v0.1, dos desde v0.2): longitud de reposo adaptativa, término de tres cuerpos, media por resorte y normalización cruzada no son objetivos de pares (alcance acotado en la ronda 2: con pesos 1 y 1/n_c, sobre valores y no sobre minimizadores).
- Problema abierto 4.2 y Conjetura 4.3 (dinámica sobre posiciones): formulados, no probados ni testeados (la Conjetura se retiró en la ronda 2).

## Resultados de referencia (semillas 20260930 / 20260931; 150 s + 68 s) [histórico v0.1; superado por las rondas 1 y 2]
- E1: 19 285/19 285 comprobaciones a 1e−9 (máximo 1.1e−11, en la representación desplazada con σ ~ 1e4); Hooke vs SSE 3.8e−16; K̃ PSD en 25/25 casos de tipo negativo (λ_min/λ_max ≥ −3.2e−16) e indefinido en 5/5 casos de longitud de reposo (hasta λ_min/λ_max = −5.5); cociente total/por-partícula en [29.7, 205.3]; factor n/k exacto en particiones de igual tamaño (2.2e−16).
- E2: 90/90 trayectorias idénticas (media 4.9 barridos, máximo 10; energía final a 2.7e−14); 86 s (fuerza bruta) vs 0.7 s (kernel). Resortes anclados vs `KMeans(lloyd, tol=0)`: 15/15 idénticos, inercia a 4.3e−16.
- E3 (30 configuraciones, 10 inicializaciones aleatorias + 10 k-means++ por configuración, recocido en 5): estabilidad de Voronoi 600/600 (relajación) y 150/150 (recocido); alcanzan E* en 28/30 (relajación), 25/30 (Lloyd+pulido), 20/30 (recocido), 14/30 (Lloyd), 6/30 (Lloyd con desplazamiento ingenuo); puntos fijos de Lloyd estables bajo un movimiento: 204/600 (34 %); con desplazamiento ingenuo 38/600 (6 %); configuraciones "distinguibles" (|ΔE*| > 1e−6): 6/30 (5 a favor de la relajación, 1 en contra, máximo 7.4e−3); ARI = 1 entre mejores particiones en 24/30 (mínimo 0.12, siempre en configuraciones con energías distintas); recomputación resorte a resorte de las mejores energías: 4.3e−13.
- E4: puntos (9,1), (10,2), (5,3), (6,2), (4,0), (2,4), (8,3); 63 particiones, 22 incógnitas, rangos 21 (w = 1/n_c) y 22 (w = 1). Residuos relativos: Hooke-sp 0 / 0.023; Hooke-tot 0.180 / 0; reposo fijo 0 / 0.042; reposo adaptativo 0.181 / 0.110; tres cuerpos 0.327 / 0.056; por resorte 0.203 / 0.148.

## Decisiones tomadas [histórico v0.1; superado por las rondas 1 y 2]
- Escalas de los potenciales fijadas desde los datos antes de correr (ℓ = mediana de la distancia al 7.º vecino; r = percentil 10 de las distancias; s = mediana de |x|²). Con esa ℓ el resorte saturante aísla un núcleo denso en "blobs" (Figura 2 de v0.1; hoy `figures/partitions.*`, fuera del manuscrito): es una propiedad del objetivo gaussiano a esa escala, no del optimizador; se dice en el pie de figura y no se afirma nada sobre calidad de agrupamiento.
- Para el control de Lloyd se usa el kernel canónico K̃ del Teorema 3.2(f) (para Hooke es 2⟨x,y⟩ y reproduce el k-means ordinario), desplazado mínimamente solo cuando es indefinido (longitud de reposo). Lloyd sobre −φ(D)+σI se conserva únicamente como control de la Proposición 3.8 (v0.1; hoy 3.6): en un primer intento se había usado como baseline y resultaba inerte (σ hasta 4e4), lo que habría sesgado la comparación contra kernel k-means.
- El criterio de "distinguible" en E3 se definió antes de correr como diferencia > 1e−6 relativa entre las mejores energías de la relajación y de Lloyd+pulido, dejando explícito que cualquier diferencia es de optimizador, no de objetivo.
- E4 en aritmética racional exacta (`fractions.Fraction`, eliminación gaussiana propia porque no hay sympy) con distancias al cuadrado para mantener todo racional.
- Idioma: manuscrito en inglés; README, nota y ficha en español.

## Limitaciones y lo que NO se afirma [histórico v0.1; superado por las rondas 1 y 2]
- No se afirma nada sobre calidad de agrupamiento en datos reales; los ARI frente a la verdad de terreno están en las tablas Markdown solo como contexto.
- El teorema cubre objetivos de pares con pesos de tamaño en {1, 1/n_c}. Otros pesos (1/n_c², etc.) quedan fuera de la identidad exacta; solo se certifica que no son de pares bajo los dos pesos estándar.
- Teorema 4.1 es un certificado de una instancia (suficiente para "no en general"); no mide cuán lejos de "de pares" están esas energías en datos típicos.
- La composición de Bernstein se cita, no se reprueba por completo.
- No se prueba que la longitud de reposo carezca de un representante PSD independiente de los datos; solo que K̃ es indefinido en los 5 conjuntos.
- No se prueba la no representabilidad de los objetivos anclados no cuadráticos (k-median); solo se señala que son clásicos.
- E3 es una comparación de optimizadores con presupuestos modestos; no es un benchmark.
- La conjetura sobre la dinámica de posiciones no se testeó, por diseño (el encargo pedía formularla, no probarla).
- Extensión: 15 páginas frente a las 5–10 pedidas; 5 de ellas son apéndice de reproducibilidad, tabla por configuración y bibliografía. Si hace falta recortar, la Tabla 5 puede pasar solo a `results/tables_relaxation.md` (hecho en v0.2).

## Dudas bibliográficas (todas las referencias son reales; las dudas son de atribución o de dato menor) [histórico v0.1; superado por las rondas 1 y 2]
- Sahni & Gonzalez (1976, J. ACM 23(3), 555–565) se cita como origen del problema min-sum k-clustering; el artículo es real y trata problemas de aproximación P-completos incluidos los de agrupamiento, pero la atribución específica del "min-sum k-clustering" a ese trabajo se hace de memoria: cotejar.
- Berg–Christensen–Ressel (1984): se cita el capítulo 3 para el lema CND↔PD y la composición con funciones de Bernstein, sin número de teorema, y el manuscrito lo dice.
- Wright (1977, Pattern Recognition 9(3), 151–166), Zha et al. (NIPS 14, pp. 1057–1064) y Telgarsky–Vattani (AISTATS 2010, pp. 820–827): las páginas se reprodujeron de memoria; verificar antes de enviar.
- Schoenberg (1938): el enunciado usado (N CND ⇔ e^{−tN} PD para todo t > 0) está en ese artículo; la equivalencia con la inmersión en Hilbert está en Schoenberg (1935), que también se cita.

## Pendientes y próximos pasos sugeridos [histórico v0.1; superado por las rondas 1 y 2]
1. Confirmar con el autor la reconstrucción de la familia mecánica (supuesto 1) y del control emparejado (supuesto 2). Si la línea original usó términos de muchos cuerpos o dinámica de posiciones, mover el énfasis del manuscrito de la Sección 3 a la Sección 4.
2. Resolver el Problema abierto 4.2 al menos para el flujo gaussiano: calcular P_{T,ε} en una configuración racional pequeña y aplicar el mismo test exacto de E4.
3. Caracterizar los pesos de tamaño w para los que Σ_c w(n_c) Σ A_ij es un kernel k-means ponderado en el sentido de Dhillon–Guan–Kulis (2007).
4. Verificar los datos bibliográficos listados arriba.
5. Actualizar la ficha LMI001 del CV web con el texto de `FICHA_LMI001_propuesta.md` (de "no sobrevivió ningún componente mecánico" a "ningún componente mecánico de tipo de pares puede sobrevivir; quedan abiertos los ingredientes de muchos cuerpos y la dinámica de posiciones").

## Ronda 1 de revisión interna (30/09/2026; respuesta aplicada el 03/10/2026)

Informe: `REFEREE_LMI001_ronda1_20260930.md`. Respuesta punto por punto: `RESPUESTA_LMI001_ronda1_20260930.md`. Resultado: manuscrito **v0.2** (13 páginas, 0 errores, 0 referencias indefinidas, 0 cajas desbordadas), corrida de referencia repetida con el código revisado. Las secciones anteriores de esta nota describen la v0.1 y se conservan como historia; donde difieren, manda esta sección.

**Renumeración v0.1 → v0.2:** Cor. 3.4 + Prop. 3.5 → Remark 3.4(a)/(b); Prop. 3.7 → Prop. 3.5; Prop. 3.8 → Prop. 3.6; Tablas 2/3/4 → 1/2/3; Tabla 1 (datasets), Tabla 5 y Figura 2 eliminadas del manuscrito.

| Hallazgo | Acción |
|---|---|
| B1 reconstrucción no declarada | Declarada en resumen, Introducción, lectura de E1–E3, Limitations y Next steps; conclusión condicionada ("if the screened formulations were pairwise"); título acotado a resortes/pares. |
| B2 ficha cierra la línea | Ficha: "Activa — borrador v0.2 en revisión interna; mantener 'En pausa' hasta confirmar el supuesto"; hallazgos y alcance acotados; README igual. |
| M1 etiquetas de 3.2(b), (e) | (b) literature (ratio association ↔ kernel k-means, Dhillon et al. 2004, 2007), (e) classical; párrafo *Status* y Tabla 3. |
| M2 aritmética 3.7(iii) | 1.72 → 1.52; 0.16+0.16 → 0.16+0.36; comprobación por la fórmula (3) añadida (en la ronda 2 se corrigió su factor ½: m1). |
| M3 Prop. 3.5 de v0.1 | Fundida en Remark 3.4(b); "we make no claim" sobre representabilidad de los objetivos anclados. |
| M4 factor ½ | Φ̃ = Φ/√2 en 3.2(f); resumen corregido ("and a factor ½"; "feature map rescaled by 1/√2"); README y ficha sin "literalmente". |
| M5 sobregeneralización 4.1 | "the three-body (triangle-area) term, the cluster-mean rest length and the per-spring average tested" en todas partes; E4 con dos configuraciones (generador propio, seed 20260932), patrón 12/12; observación de que una suma de tres cuerpos con peso (n_c−2) colapsa a pares. |
| M6 línea base de E3 | *Disclosure* en E3; σ máximo como macro (4.4×10⁴); docstring de `relaxation.py`; E1 genera sus particiones de Lloyd/relajación sobre K̃. |
| M7 Prop. 3.8 vs Dhillon | Etiqueta "proved here; explicit form of an effect noted by Dhillon et al. (TR 2004, 2007)"; entrada dhillon2004tr añadida; verificación textual pendiente (abajo). |
| M8 extensión | Recortes 1–6 y 8 aplicados; 15 → 13 páginas a 11 pt; ≤ 10 exigiría 10 pt o suprimir pruebas (no hecho). |
| m1–m16 | Todos aplicados (m6 con números de BCR/SSV sin cotejar); detalle en la respuesta. |

**Cambios de código (v0.2):** `relaxation.py` mide `is_hartigan_stable()` en todos los métodos y renombra `kernel_used` a `canonical(+shift)`; `identity_check.py` usa K̃ (desplazado mínimamente si es indefinido) para las particiones de Lloyd/relajación de E1 y un generador propio `default_rng(SEED+2)` para E4 con dos configuraciones; `make_numbers.py` añade `\EoneMaxSigma`, `\EfourSeed`, `\EfourPointsB`, `\EfourCells`, `\EfourCellsSame`, elimina la columna "Voronoi-stable relax" de la tabla E3 (afirma 100/100 por potencial) y poda macros sin uso; `make_figures.py` dibuja la Figura 1 en 2×3 paneles; docstrings con la numeración de v0.2.

**Resultados de referencia v0.2 (semillas 20260930 / 20260931 / 20260932; 159 s + 128 s en paralelo):**
- E1: 19 285/19 285, máximo 1.1e−11; Hooke vs SSE 3.9e−16; cociente total/por partícula [29.7, 197.5]; K̃ PSD 25/25, indefinido 5/5; σ máximo 4.4e4.
- E2: 90/90 trayectorias idénticas (4.9 barridos de media, máximo 11; energía final a 1.4e−14; 56 s frente a 0.6 s); anclados 15/15 (4.3e−16).
- E3: sin cambios respecto de v0.1 (600/600 y 150/150 Voronoi; E* en 28/25/14/20/6; distinguibles 6/30, 5/1, máx. 7.4e−3; ARI = 1 en 24/30; Lloyd estable a un movimiento 204/600, ingenuo 38/600); estabilidad de un movimiento medida en relax/lloyd+relax/anneal: 600/600, 600/600, 150/150.
- E4: P₁ = (5,10),(6,2),(4,4),(2,2),(3,7),(0,6),(8,8); P₂ = (0,2),(7,4),(8,7),(5,0),(2,8),(2,3),(4,10); rangos 21/22; residuos (P₁; P₂): Hooke-sp 0;0 / 0.017;0.015 — Hooke-tot 0.179;0.179 / 0;0 — reposo fijo 0;0 / 0.026;0.030 — adaptativo 0.143;0.157 / 0.109;0.122 — tres cuerpos 0.331;0.328 / 0.039;0.037 — por resorte 0.185;0.180 / 0.125;0.121.

**Bibliografía (estado tras la ronda):** verificadas por el árbitro: sahni1976, wright1977, telgarsky2010, zha2001, bcr1984. Eliminadas: aloise2009, shimalik2000, vonluxburg2007. Añadida: dhillon2004tr (UTCS TR-04-25, 2004; existencia confirmada por buscador, año/número no cotejados; en la ronda 2 pasó a `dhillon2005tr`, fechado el 18/02/2005). No verificables en esta sesión (datos coherentes con lo que sabemos): dhillon2004, dhillon2007, schoenberg1935, schoenberg1938, ssv2012 (Thm. 3.2 = Lévy–Khintchine, de memoria), hartigan1975, hartiganwong1979, lloyd1982, macqueen1967, arthur2007, girolami2002, scholkopf1998, selim1984, rose1990, rose1998, blatt1996, horn2002, durbin1987, yuille1990, fukunaga1975, cheng1995, comaniciu2002, kirkpatrick1983, pedregosa2011, virtanen2020. Números de BCR citados (Cap. 3 §2, Lema 2.1 y Teorema 2.2): de memoria, coincidentes con el árbitro, sin cotejar con el libro.

**Queda abierto tras la ronda 1:**
1. Confirmar con el autor el supuesto de reconstrucción (B1); hasta entonces la ficha pública sigue "En pausa".
2. Cotejar con el texto de Dhillon–Guan–Kulis (TR-04-25; TPAMI 2007, sección sobre positividad) la observación sobre el desplazamiento diagonal citada en la Prop. 3.6, y los números de teorema de BCR y SSV.
3. Extensión (13 páginas); decidir si se pasa a 10 pt o se recorta contenido.
4. Problema abierto 4.2 / Conjetura 4.3 y la caracterización de los pesos de tamaño (Next steps (b), (c)): sin cambios.

## Ronda 2 de revisión interna (03/10/2026)

Informe: `REFEREE_LMI001_ronda2_20261003.md` (cambios mayores, solo de texto; 0 bloqueantes, 3 mayores, 15 menores). Respuesta punto por punto: `RESPUESTA_LMI001_ronda2_20261003.md`. Resultado: manuscrito **v0.3** (3 October 2026; 12 páginas, 0 errores, 0 referencias o citas indefinidas, 0 cajas desbordadas, 35/35 referencias citadas). **Ningún número cambió** y no se repitió ninguna corrida; solo se redibujó `figures/energies.*` desde el JSON y se regeneraron las macros. Recuento: 17 aceptados, 1 aceptado con matiz, 0 rebatidos.

**Cambio de fondo: atribución.** Lo que cierra el cribado nulo para la familia de pares ya está en la literatura: coste de *pairwise clustering* (Hofmann–Buhmann 1997), *constant shift embedding* (Roth et al. 2003), *ratio association* ↔ kernel k-means (Dhillon–Guan–Kulis, TR-04-25 de 2005 y TPAMI 2007), núcleo inducido por la distancia (Sejdinovic et al. 2013) y agrupamiento por estadística de energía = kernel k-means con Hartigan (*kernel k-groups*, França–Rizzo–Vogelstein 2021). Título nuevo: *Spring-Energy Clustering Is Kernel Clustering: Known Equivalences Behind a Null Screening*. La contribución propia, pequeña y así declarada: la síntesis y su lectura para la línea; Prop. 3.6 (mecanismo explícito del desplazamiento diagonal sobre Lloyd); prueba de que (d − r)² no es de tipo negativo y de que ningún núcleo de la clase de invariancias es PD; certificados exactos del Teorema 4.1 con alcance acotado; Prop. 3.5(ii) con salvedad de prioridad no cotejada; confirmación computacional E1–E3.

**Renumeración v0.2 → v0.3:** Tabla 1 (E1) y Figura 1 salen del manuscrito (a `results/tables_identity.md` y `figures/energies.pdf`); Tabla 2 (E3 por potencial) → Tabla 1; Tabla 3 (afirmaciones) → Tabla 2; Conjetura 4.3 retirada (queda una frase de expectativa no ensayada). Def. 2.1–2.3, Lema 3.1, Teorema 3.2, Prop. 3.3, Remark 3.4, Prop. 3.5, Prop. 3.6, Teorema 4.1, Problema abierto 4.2 y ecuaciones (1)–(3) no cambian.

| Hallazgo | Acción |
|---|---|
| M1 3.2(b) y Lema 3.1 = Hofmann–Buhmann / Roth et al. | *Status*, Lema 3.1, Tabla 2, Introducción, E3 (recocido) citan `hofmann1997`, `roth2003`; (b) "[literature]". |
| M2 3.2(f) y 3.5(i) = estadística de energía | *Status* de (f) y de la Prop. 3.5 "[literature]" con `sejdinovic2013`, `franca2021`; definición de la cuerda a tensión constante; lectura de E3 coherente con França et al.; 3.5(ii) "proved here … claim no priority". |
| M3 alcance del Teorema 4.1 | Introducción sin "genuinely outside the family"; resumen, Tabla 2, README y ficha: tres funciones, media por resorte solo con pesos 1 y 1/n_c; párrafo *Values, not minimisers*; 12/12 fuera del enunciado. *Next step* (b) corregido (el método del Teorema 4.1 no se aplica directamente a minimizadores). |
| m1 | Comprobación por (3) con K' = K̃ = 2⟨x,y⟩: ΔE = −0.5. |
| m2, m3 | K = σI + A (maximizar la ratio association de A; aquí −A); `dhillon2004tr` → `dhillon2005tr` (18/02/2005). |
| m4 | (d − r)² no es de tipo negativo (dos puntos); ningún K̃ + f + f + a + σδ es PD (cuatro puntos colineales, −8rs + 4σ); "proved here", queda abierto solo si el Lema 3.1 agota las invariancias. |
| m5 | "every PD kernel … on finite data"; lift de dimensión posiblemente infinita, rango finito sobre los n puntos. |
| m6 | Figura redibujada (una fila, fuentes ≥ 8 pt efectivas) y movida fuera del manuscrito. |
| m7 | Esta nota: secciones históricas marcadas; "(6)" → "(3)"; "Prop. 3.5 de v0.1". |
| m8 | Ficha: se publica solo tras la confirmación; Estado sin la cláusula "pendiente". |
| m9 | *Disclosure* de E3: la redacción de C3a cambió, su predicción y los umbrales no. |
| m10 | *Blurring* mean shift (Cheng 1995) frente a mean shift estándar; Conjetura 4.3 retirada. |
| m11 | Resumen: "Voronoi-stable, i.e. Lloyd fixed points with ties broken in favour of the current cluster". |
| m12 | Supuesto 2 (control emparejado) declarado en el resumen y la Introducción. |
| m13 | Residuo relativo definido; versiones con peso 1/n_c ensayadas, totales no; colapso de tres cuerpos corregido; Cauchy–Binet: la fila de tres cuerpos es Σ_c det S_c. |
| m14 | README: `--fast` ~40 s. |
| m15 | Frase no verificable de E1 retirada. |
| Extensión (M8 r1) | 13 → 12 páginas: Tabla E1 y Figura fuera; apéndice a un párrafo (detalles al README); bibliografía a dos columnas; Conjetura retirada; E3 y *Next steps* condensados. Ninguna demostración de lo propio se quitó. |

**Bibliografía (estado tras la ronda 2):** nuevas y verificadas con WebSearch (datos bibliográficos y resúmenes): `hofmann1997` (IEEE TPAMI 19(1):1–14), `roth2003` (IEEE TPAMI 25(12):1540–1551), `sejdinovic2013` (Ann. Statist. 41(5):2263–2291, doi 10.1214/13-AOS1140), `franca2021` (IEEE TPAMI 43(12):4411–4425, doi 10.1109/TPAMI.2020.2998120). Corregida: `dhillon2005tr` (antes `dhillon2004tr`; UTCS TR-04-25, fechado el 18/02/2005 según la cabecera del PDF y Bibsonomy, vistos a través del buscador; PDF no abierto). **No verificables en esta sesión** (texto completo bloqueado por el proxy: arXiv, PMC, Europe PMC, people.bu.edu): si França et al. enuncian la Prop. 3.5(ii); la forma exacta en que Dhillon et al. discuten el efecto del desplazamiento diagonal; números de teorema de BCR (Cap. 3 §2, Lema 2.1, Teorema 2.2) y SSV (Teorema 3.2). El resto, sin cambios respecto de la ronda 1.

**Queda abierto tras la ronda 2:**
1. Confirmar con el autor los supuestos 1 y 2; hasta entonces la ficha pública sigue "En pausa" y `FICHA_LMI001_propuesta.md` no se publica.
2. Cotejar con el texto completo: França et al. 2021 (¿Prop. 3.5(ii)?; definición exacta de W y del núcleo), Dhillon et al. (TR-04-25 y TPAMI 2007, discusión del desplazamiento diagonal; si el mecanismo explícito de la Prop. 3.6 ya está allí, degradarla a literatura), BCR y SSV.
3. Decidir si el Lema 3.1 agota las invariancias de J (representante PD del resorte con longitud de reposo).
4. Problema abierto 4.2 (vía dinámica) y caracterización de los pesos de tamaño (Next steps (b), (c)).
5. Extensión: 12 páginas; 10 exigiría quitar la tabla de afirmaciones o pruebas.
6. La subcarpeta `theory/`, si aparece con trabajo de otro agente, no se tocó ni se integró en esta pasada.

## Integración de la teoría de invariancias y pesos de tamaño (03/10/2026)

Integrador: lleva el manuscrito de v0.3 a v0.4 con el material de `theory/` (`invariances.tex`, `invariances_derivation.md`, `check_invariances.py`, `check_invariances_output.txt`), que **no** se modifica. Plan: (1) verificación independiente de cada demostración y chequeo propio en el scratchpad; (2) integración de los bloques P, A, B, C, D y de las frases indicadas en la cabecera de `invariances.tex`; (3) etiquetas "[proved here; not yet checked by an independent referee]"; (4) demostraciones largas a un apéndice, objetivo ≤ 14 páginas; (5) compilación y revisión visual; (6) esta sección, README y ficha.

### 1. Verificación independiente (hecha)

**Lectura de las demostraciones, paso a paso** (sobre `theory/invariances.tex`):
- `prop:invcomplete`. Reducción a diagonal nula (e = Δ − f1ᵀ − 1fᵀ, f = ½diag Δ; J_e = J_Δ por el Lema 3.1; con diagonal nula J_e = −2𝓔). Intercambio k ≥ 3: R = [n]∖{p,i,j} tiene n−3 ≥ k−2 ≥ 1 elementos porque k ≤ n−1; la diferencia de energías es ½(e_pi − e_pj). Intercambio k = 2: comprobé la fórmula de la diferencia (los pares internos de P y Q se cancelan); P = ∅ da Σ_U γ = 0 (|Q|+1 = n−1) y P = {p} da γ_p(½ + 1/(n−2)) = 0 (|Q|+1 = n−2). Enlace de aristas (e_ab = e_ad = e_cd), forma final Δ = σI + g1ᵀ + 1gᵀ con g = f − (σ/2)1, unicidad (necesita n ≥ 3), valor σ(n−k), versión "todo k" (α = 0, β = σ) y formas equivalentes (núcleos de D y de M ↦ PMP; dimensión del núcleo de PMP = n). **Correcta.**
- `cor:reps`. cᵀK'c = cᵀKc + σ para c ⊥ 1 unitario; P(K+σI)P = K + σI + g1ᵀ + 1gᵀ con g = −M1/n + (1ᵀM1/2n²)1. **Correcta.** Matiz: el desplazamiento de Roth et al. se escribe con λ_min de la matriz centrada completa, que incluye el autovalor 0 en la dirección de 1; coincide con σ_* cuando σ_* ≥ 0. El texto lo dice ahora así y sigue marcado "recordado, no cotejado".
- `cor:rest`. (a) unicidad de la descomposición entre conjuntos anidados (X ⊆ Y, |X| ≥ 3) y paso por X ∪ X'; la clase coincide con K̃ + f + f + a + σδ (g = φ(‖x‖) + f + (a − φ(0))/2). (b) recalculé a mano Σc_ic_jφ(d_ij) = 8rs (pares: −φ(s) − 2φ(2s) + φ(3s) = 4rs − 2r², por dos, más 4r² de la diagonal) y σ_* ≥ 2rs con c/2. (c) restricción (λ_X − λ_Y)A[X] ∈ V; (s−r)², (2s−r)², (3s−r)² nunca son iguales (la única coincidencia de las dos primeras, s = 2r/3, da r²/9 ≠ r²). **Correcta.**
- `rem:argmin`. (a) K = λI − Δ; (b) la matriz de bloques B_P tiene a P como minimizador único (Σ_d|C_c∩P_d|²/|C_c| ≤ |C_c| con igualdad sii C_c está dentro de un bloque; mismo número de bloques ⇒ C = P); (c) J_K({i},{j,l}) = ½D(K)_jl. **Correcta.**
- `prop:weights`. 𝒢_ω lineal, núcleo ⊇ {g1ᵀ+1gᵀ} (comprobado: J^ω anula g1ᵀ+1gᵀ), constantes dentro (K = diag(1/ω)); generación por matrices de Hooke (M(e_a+e_b) − M(e_a) − M(e_b) = −2(E_ab+E_ba), abierto denso por polinomialidad); dependencia lineal con e ≠ 0; intercambio ponderado w(2)(e_pi − e_pj); comparación (m+1,1,ρ) vs (m,2,ρ) válida para 1 ≤ m ≤ n−k. Caso k = 2: coeficientes w(n−1) y w(2)+w(n−2). **Correcta.** (Para k = n−1 la condición (iii) es vacía; el enunciado con k ≤ n−2 es correcto.)
- `prop:weightsdd`. Σν = 0; ν ⟂ 𝒢_ω vía Σ_{S∋t,u} ε(S)ω̂(Sᶜ) = 0 (casos t = u: (1−3+1+1)(Ω̂−ω̂_t) = 0; t ≠ u: −ω̂({t,u}ᶜ) + ω̂({t,u}ᶜ) = 0); ⟨ν, E_tot⟩: el par {t,u} aporta −ω̂(tu)ω̂(vz) + ω̂_z(Ω̂−ω̂_z) + ω̂_v(Ω̂−ω̂_v) = 2ω̂_vω̂_z; versión con w y grupos unitarios: (w(3)−w(2))ω̂(tu)ω̂(vz) + 2w(3)ω̂_vω̂_z. **Correcta.** El enunciado exacto es "w(3) > 0 y w(3) ≥ w(2)" (no exige w(2) > 0), con k ≥ 3 o (n,k) = (4,2) para la segunda parte, y 2 ≤ k ≤ n−2 para E_tot.
- Bloque D. Con a ≡ 0 toda partición minimiza (y con w = 1/n_c cualquier a constante, porque Σ_c(n_c−1)/2 = (n−k)/2): el Problema 4.2 de la v0.3 era trivial. La construcción a = −1 en los pares de P da minimizador único para w = 1 (C(·,2) es estrictamente superaditivo, luego C engrosa a P) y para w = 1/n_c (½J_{B_P} + cte). **Correcta.**

**Chequeo propio** (`scratchpad/integ/my_check.py`, escrito desde cero con `sympy` exacto y sin importar nada de `theory/`; 21.5 s de CPU):
1. dim V_{n,k} por espacio nulo exacto para 3 ≤ n ≤ 6 y todo k: n+1 si 2 ≤ k ≤ n−1, n(n+1)/2 si k ∈ {1,n}; cada vector nulo está en span{I, g1ᵀ+1gᵀ} y su valor es σ(n−k). 18/18.
2. Rangos exactos de {F^w_{E_ab}} ∪ {1} para n = 5, 6, k = 2..n−2 y cinco pesos (1/m, 1, 1/m², 1/binom(m,2), 1/(m+1)): completo (C(n,2)+1) salvo 1/m; rango de 𝒢_ω = C(n,2) y constantes dentro, para ω = 1 y ω aleatorio. Coincide con la Prop. `weights`.
3. Caso abierto k = 2 (n = 5) con un peso que cumple h(a)+h(n−a) constante sin ser ∝ 1/m (w(2) = w(3) = 1, w(4) = 2/3): el rango es deficiente (10 de 11), así que el conteo de dimensiones no decide; no está en 𝒢_1 y, con 20 ω aleatorios, el residuo de mínimos cuadrados es ≥ 0.18. Indicio, no prueba: el caso k = 2 sigue abierto.
4. E_tot con A ≥ 0 (Hooke y longitud de reposo, n = 5, 6, k = 2, 3, 4): residuo de mínimos cuadrados frente a 𝒢_ω + constantes **minimizado sobre ω** (Nelder–Mead en log ω): siempre > 0 (entre 0.006 y 0.22). Los residuos pequeños (n = 5, k = 2) aparecen con ω degenerados (log ω_i de ±10 a ±30): el certificado excluye la representación exacta para cada ω > 0, pero no da una cota uniforme de la distancia. Se añade esa salvedad al manuscrito. **[Corregido en la ronda 3: la conclusión "no da una cota uniforme" era falsa para A con todas las entradas fuera de la diagonal positivas; el mismo certificado da max_C |E_tot − J^ω_K − c| ≥ ½·min_{i≠j} A_ij para todo ω (Prop. 4.3(b) de v0.5). Los residuos pequeños con log ω de ±10 a ±30 eran, por debajo de esa cota, artefactos de condicionamiento; solo con entradas nulas la distancia puede tender a 0. Véase la sección "Ronda 3".]**
5. Anulador ν con grupos **no unitarios** (n = 7, k = 3, G₁ = {0,1}, G₂ = {2}, G₃ = {3,4}, G₄ = {5}, R₁ = {6}), exacto, 30 tripletas aleatorias (ω, K, A): Σν = 0, ⟨ν, J^ω_K⟩ = 0, ⟨ν, E_tot⟩ > 0 en todas. (El script del agente solo probaba n = 4 con grupos unitarios.)
6. Resorte con longitud de reposo: cᵀ(−A)c = −8rs simbólico exacto; σ_* = λ_max(PAP) = 2rs **exacto** (autovalores simbólicos) para (r,s) = (1,½), (1,1), (1,5), (2,7). Es decir, la cota σ_* ≥ 2rs es una igualdad en esos casos (no se afirma en general).
7. Minimizador único de J_{B_P}, de E_tot y de E_sp con a = −1 en los pares de P: 20/20 por enumeración. Ejemplo de `rem:argmin`(a): J_{K+Δ} constante, argmin J_K con 1 de 15 particiones.

**Re-ejecución de `theory/check_invariances.py`:** salida idéntica a `check_invariances_output.txt` salvo la línea de CPU (22.8 s frente a 21.9 s).

**Correcciones o degradaciones:** ninguna demostración falla. Cambios de redacción al integrar: (i) `prop:weightsdd` y su comentario dicen "as functions of the partition, up to an additive constant" (valores, no minimizadores; con A libre toda partición es minimizador único de algún objetivo kernel) y llevan la salvedad del punto 4; (ii) el umbral de `cor:reps` se relaciona con el desplazamiento de Roth et al. solo "for σ_* ≥ 0, as we recall it; not checked against their text"; (iii) todo lo nuevo lleva "[proved here; not yet checked by an independent referee]" en la tabla de afirmaciones.

### 2. Qué se integró y dónde (manuscrito v0.4, 3 October 2026)

Numeración v0.3 → v0.4 (comprobada en `main.aux`): Teorema 3.2 → **3.4**; Prop. 3.3 → **3.5**; Remark 3.4 → **3.8**; Prop. 3.5 → **3.9**; Prop. 3.6 → **3.10**; Problema abierto 4.2 → **4.4**. Sin cambio: Def. 2.1–2.3, Lema 3.1, Teorema 4.1, Tablas 1–2, ecuaciones (1)–(3), Apéndice A.

| Bloque / cambio | Dónde | Notas |
|---|---|---|
| P (`corollary`) | preámbulo, tras `conjecture` | |
| A: Prop. 3.2 (`prop:invcomplete`), Cor. 3.3 (`cor:reps`) | §3.1, tras el párrafo que sigue al Lema 3.1 | demostración de la Prop. 3.2 en el Apéndice B; la del Cor. 3.3 queda en el texto; el estado del Cor. 3.3 relaciona σ_* con Roth et al. solo para σ_* ≥ 0 "as we recall it (not checked against their text)" |
| Frase del "Rest length" (Prop. 3.5) | prueba de la Prop. 3.5 | reemplazada según la cabecera; el cálculo de cuatro puntos (−8rs + 4σ) se movió a la prueba del Cor. 3.6(b), escrito completo (Σc_ic_jφ = 4r² + 2(4rs − 2r²) = 8rs), para no duplicarlo |
| B: Cor. 3.6 (`cor:rest`), Remark 3.7 (`rem:argmin`) | tras la prueba de la Prop. 3.5 | (a), (b) se prueban en el texto; (c) en el Apéndice B |
| Nota en la Prop. 3.9 (Hartigan) | primera línea | "by Corollary 3.3 these are exactly the PSD matrices K + σI + g1ᵀ + 1gᵀ" |
| C: párrafo *Size weights*, Prop. 4.2 (`prop:weights`), Prop. 4.3 (`prop:weightsdd`) | §4, entre *Values, not minimisers* y *The dynamic route* | demostraciones en el Apéndice B; el comentario de la Prop. 4.3 añade "values, not minimisers" y la salvedad de que el certificado no acota la distancia (ω degenerados) |
| D: Problema 4.4 (con "unique") y Remark 4.5 (`rem:dyn`) | sustituye al Problema 4.2 de v0.3 | |
| Tabla 2 | §6 | fila del Lema 3.1 fusionada con Prop. 3.2/Cor. 3.3; fila del resorte con reposo reemplazada (Cor. 3.6 + Remark 3.7); fila de pesos (Prop. 4.2 y 4.3); fila del Problema 4.4/Remark 4.5; "not yet refereed" definido en el pie |
| *Next steps* | §6 | (c) y (d) viejos eliminados; nuevos (c) k = 2 / pesos dependientes de los datos, (d) núcleo PD con los mismos minimizadores, (e) cotejo con Roth et al.; (b) reescrito con unicidad y Farkas; (f) = antiguo (e), acotado a "pairwise, per-particle" |
| *Limitations* | §6 | 1/n_c es el único peso con pesos fijos; lista de resultados no arbitrados; cotejos pendientes |
| Apéndice B "Proofs of the results on invariances and size weights" | tras el Apéndice A | Prop. 3.2, Cor. 3.6(c), Prop. 4.2, Prop. 4.3, sin quitar pasos (solo dos displays pasados a texto en línea) |
| Apéndice A | reproducibilidad | menciona `theory/check_invariances.py` y el chequeo independiente |

**Coherencia sobre la energía total (pedido explícito).** El texto de v0.3 no decía que E_tot fuera un k-means con núcleo, pero el **título** ("Spring-Energy Clustering Is Kernel Clustering"), el título del Teorema 3.4 ("Spring energies are kernel objectives"), la lectura de E1–E3 ("If the screened formulations were of the pairwise kind…") y el resumen ("For that family the null result follows…") abarcaban también la normalización total, lo que la Prop. 4.3 vuelve inexacto. Cambios: título → "**Per-Particle** Spring-Energy Clustering Is Kernel Clustering" (decisión del integrador; revertible por el autor); Teorema 3.4 → "Spring energies and kernel objectives; collected from the literature" y su *Status* dice que E_tot no es k-means con núcleo ponderado; resumen, Introducción, *Contribution*, lectura de E1–E3 y *Next step* (f) acotan el cribado nulo a la normalización por partícula y dicen que, con la total, un control de kernel optimiza otra función y un nulo sería un hallazgo empírico. README y ficha, igual.

**Otros archivos.** `experiments/*.py`: solo docstrings y comentarios renumerados (3.2 → 3.4, 3.3 → 3.5, 3.5(ii) → 3.9(ii), 3.6 → 3.10); se dejó sin tocar la cadena de `identity_check.py`:405 que genera la cabecera "Theorem-3.2(f) kernel" de `results/tables_identity.md`, para no desalinear código y resultados sin repetir la corrida (el README lo advierte). Ningún experimento se relanzó (E1–E4 no cambian); `numbers.tex` se regeneró con `build.sh` desde los mismos JSON y es idéntico. Ningún número nuevo entra al texto salvo el "about 22 s" del script teórico (Apéndice A), copiado de su salida guardada. `theory/` no se modificó.

### 3. Compilación y extensión

- `manuscript/build.sh` (make_numbers + latexmk + latexmk -c): 0 errores, 0 referencias o citas indefinidas, 0 cajas desbordadas, `pdftotext main.pdf - | grep -c '??'` = 0; 35/35 referencias citadas; `main.pdf` conservado.
- Páginas: **12 (v0.3) → 17 (v0.4)**. El texto principal (§1–§6, con las Tablas 1–2) termina en la p. 14; Apéndice A y Apéndice B (demostraciones) ocupan las pp. 14–15 y la bibliografía las pp. 15–17 (unas 7 líneas por columna en la p. 17). Con todos los bloques en línea la cuenta era 17 páginas; se pasaron al Apéndice B las demostraciones de las Prop. 3.2, 4.2, 4.3 y del Cor. 3.6(c), y se condensó la redacción nueva (resumen reescrito, comentarios, Remark 3.7, filas de la Tabla 2). **No se alcanzó el objetivo de ≤ 14 páginas en total**: mover demostraciones al apéndice no reduce el total, y bajar de 17 exigiría quitar material (p. ej. la Tabla 1 de E3, cuyo agregado por potencial solo existe en `table_e3_agg.tex`, o resumir texto ya arbitrado), cosa que no se hizo. Márgenes y tamaño de letra sin cambios.
- Revisión visual de las páginas nuevas (pp. 4, 6–7, 9–11, 13–15): sin problemas de composición; el título queda en tres líneas.

### 4. Abiertos (tras la integración)

1. k = 2 en la Prop. 4.2 cuando h(a)+h(n−a) es constante y w no es ∝ 1/m (n ≥ 5). Indicio (no prueba): con n = 5 y w = (1, 1, 2/3) el rango es deficiente, no está en 𝒢_1 y el residuo con 20 ω aleatorios es ≥ 0.18.
2. Pesos dependientes de los datos para w decreciente con w(3) < w(2), distinto de 1/m (1/m², 1/binom(m,2)): el certificado de la Prop. 4.3 no aplica.
3. Núcleo PD independiente de los datos con los **mismos minimizadores** que el resorte con longitud de reposo (Remark 3.7(c)); condición necesaria ordinal en ternas.
4. Problema 4.4 con unicidad: buscar o certificar un contraejemplo con distancias repetidas (sistema lineal estricto + certificado de Farkas sobre ℚ); no ejecutado.
5. Cotejar con el texto de Roth et al. (2003) la relación entre su desplazamiento mínimo y σ_* (coinciden si σ_* ≥ 0, según lo que recordamos) y si el recíproco (Prop. 3.2) ya está publicado; búsqueda bibliográfica no exhaustiva.
6. Revisión por un árbitro independiente de todo lo marcado "not yet refereed" (Prop. 3.2, Cor. 3.3, Cor. 3.6, Remark 3.7, Prop. 4.2, Prop. 4.3, Remark 4.5).
7. Siguen abiertos los puntos de la ronda 2: confirmación del autor (supuestos 1 y 2, y ahora también **qué normalización** se usó en el cribado), cotejos de França et al., Dhillon et al., BCR y SSV.
8. Extensión: 17 páginas; decidir si se acepta o qué se recorta.

### 5. Cómputo

`my_check.py` 22 s de CPU; re-ejecución de `theory/check_invariances.py` 23 s; sondeo de ω degenerados (Nelder–Mead, `probe_omega.py`) unos 30 s; unas 14 compilaciones de LaTeX (~4–5 s cada una). Total del orden de 2–3 minutos de CPU. Sin corridas de E1–E4.

## Ronda 3 de revisión interna (03/10/2026)

Informe: `REFEREE_LMI001_ronda3_20261003.md` (árbitro interno independiente, sobre la v0.4; veredicto: cambios menores; 0 bloqueantes, 3 mayores, 12 menores; los siete resultados nuevos —Prop. 3.2, Cor. 3.3, Cor. 3.6, Rem. 3.7, Prop. 4.2, Prop. 4.3, Rem. 4.5— confirmados correctos con chequeos exactos propios). Respuesta punto por punto: `RESPUESTA_LMI001_ronda3_20261003.md`. Resultado: manuscrito **v0.5** (3 October 2026; **15 páginas**, antes 17; 0 errores, 0 referencias o citas indefinidas, 0 cajas desbordadas, 0 "??", 35/35 referencias citadas). **Ningún número de E1–E4 cambió** y no se repitió ninguna corrida; `numbers.tex` es idéntico (md5 comprobado). Recuento: 13 aceptados, 2 aceptados con matiz (M3 sin la nota aparte; m11 sin el cotejo de França et al., bloqueado por el proxy), 0 rebatidos.

**Renumeración v0.4 → v0.5:** Tabla 1 (E3 por potencial) fuera del manuscrito (a `results/tables_e3_by_potential.md`, generada por `make_numbers.py` desde el JSON); la tabla de afirmaciones pasa de Tabla 2 a **Tabla 1**; Prop. 4.3 → partes (a) (enunciado de v0.4) y (b) (cota nueva). El resto no cambia.

| Hallazgo | Acción |
|---|---|
| M1 Prop. 4.3 "bounds no distance" | Cota uniforme verificada (prueba propia y PL propio, `experiments/check_bound_prop43.py`, 0 violaciones; constante ½ óptima: A ≡ 1, k = n−2) y añadida como Prop. 4.3(b) con versión para F^w_A; prueba en el Apéndice B, paso (4); comentario reescrito (entradas nulas: la distancia puede tender a 0, ejemplo n = 4, k = 2 con un solo resorte); README y esta nota corregidos. |
| M2 tensión fuera de la explicación | Texto del árbitro en la lectura de E1–E3 (tensión T = normalización total disfrazada; tensión por partícula = *ratio cut*, objetivo de k-means con núcleo, Dhillon et al. 2007); apertura de la Sección 4 reescrita (Teorema 3.4(b) cubre lo por partícula; la total ya está fuera); *Limitations* (incluye la normalización total y la tensión liberada); *Next step* (a) ("normalisation of the energy and of the tension"); resumen, Introducción, README y ficha coherentes. |
| M3 extensión (17 págs.) | Recortes 2–5 aplicados (Tabla 1 fuera, E3 condensado, Teorema 3.4(f) sin el mapa Φ̃ = Φ/√2, resumen 330 → 219 palabras) y otros condensados de texto (Introducción, *Contribution*, *Status* del Teorema 3.4, Remark 3.8, Prop. 3.9(iii), comentario de la Prop. 3.5, tabla de afirmaciones con filas fusionadas, Apéndice A, listas de autores de SciPy y scikit-learn abreviadas con "et al."): **17 → 15 páginas**, sin cambiar márgenes ni letra y sin quitar ninguna demostración de resultados propios. La **nota aparte** (recorte 1) **no** se hizo por decisión del autor humano: plan abajo. |
| m1 etiquetas | Todos los enunciados nuevos: "[proved here; checked by an independent internal referee (round 3)]" (macro `\rthree`); Prop. 4.3(b): "suggested by that referee, proof re-derived and checked by linear programming by the author"; pie de la tabla de afirmaciones reescrito ("r3", sin "checked by exact ranks"); *Limitations*, resumen, README y ficha. |
| m2 | l. 67 (Introducción): "for non-negative springs"; ficha: "ningún núcleo PD independiente de los datos reproduce sus valores salvo una constante (y factor positivo); mismos minimizadores, abierto"; "con al menos tres clústeres" para 1/n_c. |
| m3 | Rem. 3.7(a): "for every positive definite matrix K (in particular, if it does so for every symmetric K; n ≥ 3, 2 ≤ k ≤ n−1)". |
| m4, m5 | Resumen reescrito (219 palabras): "for values rather than minimisers" solo para invariancias, pesos y certificados; el mecanismo de Lloyd queda fuera de esa calificación. |
| m6 | Cor. 3.3: convención fijada (K = −A con diagonal nula: σ_* = desplazamiento mínimo de Roth et al. para disimilitudes A_ij; 2σ_* para D(K) = 2A), "as we recall their construction (not checked against their text)". |
| m7 | Prop. 4.2 ampliada a n ≥ 4, 3 ≤ k ≤ n−1 ("for k = n−1 only w(2) enters and (i)–(iii) hold for every w"; PL: rango = número de particiones); Prop. 4.3: frase sobre la necesidad de k ≤ n−2 (D(K)_pq = A_pq(ω_p+ω_q)/(ω_pω_q)). |
| m8 | "fixed weights are excluded by Proposition 4.2 for 3 ≤ k ≤ n−2 and (n,k) = (4,2)". |
| m9 | Apéndice A: "the integrator's own re-check (not in the repository) … the independent check is the round-3 internal referee report". |
| m10 | "Theorem-3.2(f)" → "Theorem-3.4(f)" en `identity_check.py`:405 y en la cabecera de `results/tables_identity.md` (sustitución de texto; regenerar exigiría repetir E1; ningún número cambia). |
| m11 | `franca2021`: `note = {Preprint arXiv:1710.09859}`. Cotejo de la Prop. 3.9(ii) en el preprint: **no hecho** (arXiv devuelve 403 en el proxy). |
| m12 | *Next step* (e) amplía la búsqueda de prioridad a la literatura de desplazamientos de similitudes en *pairwise clustering* (sin citar a Chehreghani: datos no verificados). |

**Plan de la nota aparte (decisión pendiente del autor humano; no ejecutado).** Propuesta del árbitro (M3.1), concretada:
1. Nota nueva, título de trabajo *Invariances of the kernel k-means trace form, and size weights*: Prop. 3.2 con prueba completa, Cor. 3.3 (con la convención de Roth et al.), Cor. 3.6 (a)–(c), Rem. 3.7, Prop. 4.2, Prop. 4.3 (a)+(b), el Apéndice B entero, `theory/check_invariances.py` y `experiments/check_bound_prop43.py`; sección de prioridad (Roth et al. 2003, Hofmann–Buhmann 1997, Dhillon et al., literatura de *shift of pairwise similarities*), que es la que más gana con una nota corta y fechada.
2. En LMI001 quedarían solo: Prop. 3.2 con la prueba de una línea ("reduce to zero diagonal and exchange two points between clusters"), Cor. 3.6(b) con el cálculo de cuatro puntos (8rs), Prop. 4.3 con el certificado (~12 líneas) y la cota (b); el resto se citaría a la nota. Ahorro estimado por el árbitro ≈ 3 páginas (v0.5 pasaría de 15 a ≈ 12–13).
3. Antes de separar: decidir código y carpeta de la nota (¿sub-nota de LMI001 o línea propia?), una ronda de árbitro para la nota y una revisión de la tabla de afirmaciones de LMI001 para que remita a ella.
Mientras no se decida, la v0.5 conserva todo el material y sus demostraciones.

**Cómputo de la ronda 3:** PL de la Prop. 4.3(b) dos veces (scratchpad y repositorio, salidas idénticas salvo la línea de CPU): 67 + 69 s; `make_numbers.py` y ~8 compilaciones de LaTeX (unos 5 s cada una). Total ≈ 3 minutos de CPU. Sin corridas de E1–E4.

**Queda abierto tras la ronda 3:**
1. Confirmación del autor de la línea: familia de pares, control emparejado y **normalización** (de la energía y de la tensión); hasta entonces la ficha pública sigue "En pausa".
2. Decisión sobre la nota aparte (plan arriba).
3. Cotejos con texto completo: Roth et al. 2003 (convención del desplazamiento mínimo y si la Prop. 3.2 ya está publicada), França et al. 2021 / arXiv:1710.09859 (Prop. 3.9(ii)), Dhillon et al. (efecto del desplazamiento diagonal), BCR y SSV (numeración); búsqueda de prioridad en la literatura de desplazamientos de similitudes.
4. Matemática abierta: k = 2 en la Prop. 4.2 con h(a)+h(n−a) constante; pesos dependientes de los datos para w decreciente con w(3) < w(2), distinto de 1/m (la Prop. 4.3 no aplica); núcleo PD con los mismos minimizadores para el resorte con longitud de reposo (Rem. 3.7(c)); Problema 4.4 (Farkas, no ejecutado).
5. Extensión: 15 páginas frente al objetivo original de 5–10; bajar más exige la nota aparte o quitar la tabla de afirmaciones.
