# LMI001 — Continuidad interna, 30/09/2026

Documento de trabajo interno. No incorporar al manuscrito ni a entregas institucionales.

## Proyecto y alcance
Línea LMI001, "Analogías mecánicas para agrupamiento de datos" / "Mechanical analogies for data clustering", área Inteligencia artificial y aprendizaje, estado en el CV web: "En pausa". Ficha pública: estudio de formulaciones de agrupamiento inspiradas en tensión, levantamiento y sistemas mecánicos; objetivo: determinar si el componente mecánico produce un efecto distinguible frente a controles de kernel emparejados; hallazgo: el análisis de cribado no encontró ningún componente mecánico que sobreviviera a esas comparaciones controladas; alcance: la analogía mecánica por sí sola no establece una ventaja algorítmica.

Encargo de esta sesión: convertir el cribado negativo en un teorema que lo explique, más una confirmación computacional, sin cambiar el alcance declarado.

## Supuestos reconstruidos (verificar con el autor)
No existe manuscrito previo ni código de la línea en el repositorio; todo lo que sigue se reconstruyó de la ficha.
1. **Qué es "formulación mecánica".** Se asumió: puntos unidos por resortes con un potencial de pares φ(d) (Hooke con y sin longitud de reposo, cuerda a tensión constante, resorte saturante, resorte logarítmico), opcionalmente tras un levantamiento L (se usó el paraboloide (x, |x|²/s)), con la energía intra-clúster normalizada por partícula (1/n_c) o total. "Tensión" se interpretó como la energía liberada al cortar los resortes entre clústeres; "levantamiento" como una aplicación L previa a los resortes. Se añadió la variante de resortes anclados a un hub porque es la lectura mecánica natural de Lloyd. Si la línea original usaba otra cosa (por ejemplo, láminas elásticas con energía de flexión, o dinámica de partículas), ese caso cae en la Sección 4 del manuscrito ("lo que sale de la familia") y el teorema no lo cubre; el manuscrito lo dice.
2. **Qué es "control de kernel emparejado".** Se asumió: kernel k-means con la misma matriz de afinidad y el mismo optimizador/inicialización. Con esa lectura el teorema dice que control y formulación mecánica son el mismo objetivo.
3. **Normalización.** La identidad exacta con k-means exige la normalización 1/n_c; se decidió tratar la normalización como parte de la definición de la familia y demostrar por separado que la energía total es min-sum k-clustering / max-k-cut. E4 certifica que ambas normalizaciones son objetivos distintos.

## Qué se produjo (todo en `papers/LMI001-mechanical-clustering/`)
1. Manuscrito LaTeX `manuscript/main.tex` (inglés, 15 páginas con apéndices y 29 referencias), compilado a `main.pdf` con latexmk (pdflatex + bibtex) sin errores ni referencias indefinidas; quedan 4 cajas horizontales desbordadas menores (≤ 8 pt) (revisar tras la edición final).
2. Biblioteca `experiments/mechanical.py` y dos scripts de experimentos con semilla fija, salida JSON/Markdown, más `make_numbers.py` (macros) y `make_figures.py`. Ningún número del manuscrito está escrito a mano.
3. README, esta nota y una propuesta de ficha.

## Resultados matemáticos (estado)
- Lema 3.1 (invariancias de la forma de traza J bajo σI, a·11ᵀ y f1ᵀ+1fᵀ): demostrado, elemental.
- Teorema 3.2: (a) trivial; (b) E_sp = ½J_{−A} + ½(n−k)φ(0), y desplazamiento diagonal (demostrado); (c) Hooke = SSE (clásico); (d) energía total + tensión liberada = constante ⇒ min-sum / max-k-cut (demostrado, elemental); (e) todo objetivo kernel k-means es energía de Hooke de una configuración levantada (demostrado); (f) para φ de tipo negativo, kernel universal PD K̃(x,y) = φ(|x|)+φ(|y|)−φ(|x−y|)−φ(0) (demostrado a partir del lema clásico CND↔PD, con la prueba incluida).
- Proposición 3.3: d² de tipo negativo (clásico, una línea); ψ∘N CND para ψ Bernstein (literatura: Berg–Christensen–Ressel 1984, cap. 3; Schilling–Song–Vondraček 2012; se incluye esbozo vía Lévy–Khintchine y teorema de Schoenberg).
- Proposición 3.7: relajación partícula a partícula = método de Hartigan; fórmula ΔE invariante de representación; todo punto fijo de un movimiento simple es punto fijo de Lloyd para cualquier representante PSD (demostrado; generaliza Telgarsky–Vattani 2010); contraejemplo explícito al recíproco {0, 2, 3.4, 3.6}.
- Proposición 3.8: la regla de Lloyd depende del representante PSD (el desplazamiento σI congela Lloyd para σ grande). Demostrada; es el hallazgo colateral más útil de la sesión: "kernel k-means con Lloyd" no es un algoritmo único para una energía de resortes; la relajación de un movimiento sí lo es.
- Teorema 4.1 (asistido por computadora, aritmética racional exacta, una instancia): longitud de reposo adaptativa, término de tres cuerpos, media por resorte y normalización cruzada no son objetivos de pares.
- Problema abierto 4.2 y Conjetura 4.3 (dinámica sobre posiciones): formulados, no probados ni testeados.

## Resultados de referencia (semillas 20260930 / 20260931; 150 s + 68 s)
- E1: 19 285/19 285 comprobaciones a 1e−9 (máximo 1.1e−11, en la representación desplazada con σ ~ 1e4); Hooke vs SSE 3.8e−16; K̃ PSD en 25/25 casos de tipo negativo (λ_min/λ_max ≥ −3.2e−16) e indefinido en 5/5 casos de longitud de reposo (hasta λ_min/λ_max = −5.5); cociente total/por-partícula en [29.7, 205.3]; factor n/k exacto en particiones de igual tamaño (2.2e−16).
- E2: 90/90 trayectorias idénticas (media 4.9 barridos, máximo 10; energía final a 2.7e−14); 86 s (fuerza bruta) vs 0.7 s (kernel). Resortes anclados vs `KMeans(lloyd, tol=0)`: 15/15 idénticos, inercia a 4.3e−16.
- E3 (30 configuraciones, 10 inicializaciones aleatorias + 10 k-means++ por configuración, recocido en 5): estabilidad de Voronoi 600/600 (relajación) y 150/150 (recocido); alcanzan E* en 28/30 (relajación), 25/30 (Lloyd+pulido), 20/30 (recocido), 14/30 (Lloyd), 6/30 (Lloyd con desplazamiento ingenuo); puntos fijos de Lloyd estables bajo un movimiento: 204/600 (34 %); con desplazamiento ingenuo 38/600 (6 %); configuraciones "distinguibles" (|ΔE*| > 1e−6): 6/30 (5 a favor de la relajación, 1 en contra, máximo 7.4e−3); ARI = 1 entre mejores particiones en 24/30 (mínimo 0.12, siempre en configuraciones con energías distintas); recomputación resorte a resorte de las mejores energías: 4.3e−13.
- E4: puntos (9,1), (10,2), (5,3), (6,2), (4,0), (2,4), (8,3); 63 particiones, 22 incógnitas, rangos 21 (w = 1/n_c) y 22 (w = 1). Residuos relativos: Hooke-sp 0 / 0.023; Hooke-tot 0.180 / 0; reposo fijo 0 / 0.042; reposo adaptativo 0.181 / 0.110; tres cuerpos 0.327 / 0.056; por resorte 0.203 / 0.148.

## Decisiones tomadas
- Escalas de los potenciales fijadas desde los datos antes de correr (ℓ = mediana de la distancia al 7.º vecino; r = percentil 10 de las distancias; s = mediana de |x|²). Con esa ℓ el resorte saturante aísla un núcleo denso en "blobs" (Figura 2): es una propiedad del objetivo gaussiano a esa escala, no del optimizador; se dice en el pie de figura y no se afirma nada sobre calidad de agrupamiento.
- Para el control de Lloyd se usa el kernel canónico K̃ del Teorema 3.2(f) (para Hooke es 2⟨x,y⟩ y reproduce el k-means ordinario), desplazado mínimamente solo cuando es indefinido (longitud de reposo). Lloyd sobre −φ(D)+σI se conserva únicamente como control de la Proposición 3.8: en un primer intento se había usado como baseline y resultaba inerte (σ hasta 4e4), lo que habría sesgado la comparación contra kernel k-means.
- El criterio de "distinguible" en E3 se definió antes de correr como diferencia > 1e−6 relativa entre las mejores energías de la relajación y de Lloyd+pulido, dejando explícito que cualquier diferencia es de optimizador, no de objetivo.
- E4 en aritmética racional exacta (`fractions.Fraction`, eliminación gaussiana propia porque no hay sympy) con distancias al cuadrado para mantener todo racional.
- Idioma: manuscrito en inglés; README, nota y ficha en español.

## Limitaciones y lo que NO se afirma
- No se afirma nada sobre calidad de agrupamiento en datos reales; los ARI frente a la verdad de terreno están en las tablas Markdown solo como contexto.
- El teorema cubre objetivos de pares con pesos de tamaño en {1, 1/n_c}. Otros pesos (1/n_c², etc.) quedan fuera de la identidad exacta; solo se certifica que no son de pares bajo los dos pesos estándar.
- Teorema 4.1 es un certificado de una instancia (suficiente para "no en general"); no mide cuán lejos de "de pares" están esas energías en datos típicos.
- La composición de Bernstein se cita, no se reprueba por completo.
- No se prueba que la longitud de reposo carezca de un representante PSD independiente de los datos; solo que K̃ es indefinido en los 5 conjuntos.
- No se prueba la no representabilidad de los objetivos anclados no cuadráticos (k-median); solo se señala que son clásicos.
- E3 es una comparación de optimizadores con presupuestos modestos; no es un benchmark.
- La conjetura sobre la dinámica de posiciones no se testeó, por diseño (el encargo pedía formularla, no probarla).
- Extensión: 15 páginas frente a las 5–10 pedidas; 5 de ellas son apéndice de reproducibilidad, tabla por configuración y bibliografía. Si hace falta recortar, la Tabla 5 puede pasar solo a `results/tables_relaxation.md`.

## Dudas bibliográficas (todas las referencias son reales; las dudas son de atribución o de dato menor)
- Sahni & Gonzalez (1976, J. ACM 23(3), 555–565) se cita como origen del problema min-sum k-clustering; el artículo es real y trata problemas de aproximación P-completos incluidos los de agrupamiento, pero la atribución específica del "min-sum k-clustering" a ese trabajo se hace de memoria: cotejar.
- Berg–Christensen–Ressel (1984): se cita el capítulo 3 para el lema CND↔PD y la composición con funciones de Bernstein, sin número de teorema, y el manuscrito lo dice.
- Wright (1977, Pattern Recognition 9(3), 151–166), Zha et al. (NIPS 14, pp. 1057–1064) y Telgarsky–Vattani (AISTATS 2010, pp. 820–827): las páginas se reprodujeron de memoria; verificar antes de enviar.
- Schoenberg (1938): el enunciado usado (N CND ⇔ e^{−tN} PD para todo t > 0) está en ese artículo; la equivalencia con la inmersión en Hilbert está en Schoenberg (1935), que también se cita.

## Pendientes y próximos pasos sugeridos
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
| M2 aritmética 3.7(iii) | 1.72 → 1.52; 0.16+0.16 → 0.16+0.36; comprobación por la fórmula (6) añadida. |
| M3 Prop. 3.5 | Fundida en Remark 3.4(b); "we make no claim" sobre representabilidad de los objetivos anclados. |
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

**Bibliografía (estado tras la ronda):** verificadas por el árbitro: sahni1976, wright1977, telgarsky2010, zha2001, bcr1984. Eliminadas: aloise2009, shimalik2000, vonluxburg2007. Añadida: dhillon2004tr (UTCS TR-04-25, 2004; existencia confirmada por buscador, año/número no cotejados). No verificables en esta sesión (datos coherentes con lo que sabemos): dhillon2004, dhillon2007, schoenberg1935, schoenberg1938, ssv2012 (Thm. 3.2 = Lévy–Khintchine, de memoria), hartigan1975, hartiganwong1979, lloyd1982, macqueen1967, arthur2007, girolami2002, scholkopf1998, selim1984, rose1990, rose1998, blatt1996, horn2002, durbin1987, yuille1990, fukunaga1975, cheng1995, comaniciu2002, kirkpatrick1983, pedregosa2011, virtanen2020. Números de BCR citados (Cap. 3 §2, Lema 2.1 y Teorema 2.2): de memoria, coincidentes con el árbitro, sin cotejar con el libro.

**Queda abierto tras la ronda 1:**
1. Confirmar con el autor el supuesto de reconstrucción (B1); hasta entonces la ficha pública sigue "En pausa".
2. Cotejar con el texto de Dhillon–Guan–Kulis (TR-04-25; TPAMI 2007, sección sobre positividad) la observación sobre el desplazamiento diagonal citada en la Prop. 3.6, y los números de teorema de BCR y SSV.
3. Extensión (13 páginas); decidir si se pasa a 10 pt o se recorta contenido.
4. Problema abierto 4.2 / Conjetura 4.3 y la caracterización de los pesos de tamaño (Next steps (b), (c)): sin cambios.
