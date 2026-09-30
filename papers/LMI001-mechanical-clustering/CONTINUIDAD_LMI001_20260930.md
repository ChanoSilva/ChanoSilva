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
1. Manuscrito LaTeX `manuscript/main.tex` (inglés, 14 páginas con apéndices y 29 referencias), compilado a `main.pdf` con latexmk (pdflatex + bibtex) sin errores ni referencias indefinidas; quedan 6 cajas horizontales desbordadas menores en tablas (revisar tras la edición final).
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
- Extensión: 14 páginas frente a las 5–10 pedidas; 4 de ellas son apéndice de reproducibilidad, tabla por configuración y bibliografía. Si hace falta recortar, la Tabla 5 puede pasar solo a `results/tables_relaxation.md`.

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
