# MRT001 — Continuidad interna, 30/09/2026

Documento de trabajo interno. No incorporar al manuscrito ni a entregas institucionales.

## Proyecto y alcance
Línea MRT001, "Invariantes y fundamentos geométricos" / "Invariants and geometric foundations", área Matemáticas y estructuras, estado en el CV web: "En pausa — Desarrollo conceptual suspendido". Objetivo declarado en la ficha: precisar qué afirmaciones pueden formularse y contrastarse dentro de marcos matemáticos definidos. Alcance declarado: sin teoría física contrastada; no se presenta como teoría unificada ni como evidencia experimental.

Pedido del usuario en la sesión de Claude Code (session_01MTmjU2K8b4sgpjjL3JTtDz, repositorio ChanoSilva/ChanoSilva, rama `claude/charming-pasteur-2cajqb`): "Seguir con el Paper: Foundational Geometry", luego "sigamos todo … con todo".

## Supuesto central (verificar con el autor)
No se encontró ningún manuscrito previo titulado "Foundational Geometry". Se asumió que el paper corresponde a la línea MRT001 y se redactó un **borrador nuevo desde cero** a partir de la ficha del CV. Si existe un manuscrito anterior (en la Biblioteca de ChatGPT, en un chat de Claude.ai o en archivos locales), este borrador debe fusionarse con él, no reemplazarlo.

## Dónde se buscó el manuscrito original (sin éxito)
- GitHub: `ChanoSilva/ChanoSilva` y `ChanoSilva/Colab`, ambos vacíos en el remoto. Resto de repositorios: forks o tesis 2015–2020.
- Google Drive: título y texto completo ("Foundational Geometry", "Geometr", "invariantes", "fundamentos geométricos", `.tex`, `.bib`, Google Docs y Markdown recientes, carpetas de papers). Único hallazgo relacionado: la ficha MRT001 en `CV_Web/investigacion.html` (Drive) y en el sitio publicado `luciano-silva-alarco.luxian80.chatgpt.site`.
- Artifacts, Claude Docs y sesiones previas de Claude Code: ninguno.
- Web (arXiv, Zenodo, SSRN): nada con ese título a nombre del autor.
- Gmail: el conector exigía reautorización; no se pudo revisar correo.
- Observación: en Drive existe `Information.txt` con datos personales de cuentas al alcance del conector; no se usó ni se copió.

## Qué se produjo (todo en `papers/MRT001-foundational-geometry/`)
1. Manuscrito LaTeX `manuscript/main.tex` (inglés, ~13 páginas) con bibliografía real de 34 entradas (`refs.bib`), compilado a `main.pdf`.
2. Dos scripts de experimentos con semilla fija y salida JSON/Markdown, más `make_numbers.py`, que inyecta cada número del texto como macro LaTeX. Ningún número del paper está escrito a mano.
3. Este README y esta nota.

## Resultados de referencia (corrida completa, semilla 20260930; E1–E4 en 1201 s con contención de CPU, E2c en 168 s, E5 en 315 s en la corrida v0.4 que incluye E5e, E5f en 128 s)
- E1 (aritmética exacta int64, rejilla 2^30): 0 instancias de betweenness y 0 de congruencia en 4000 configuraciones aleatorias (n ∈ {5,10,20,50}, d ∈ {2,3}); rejillas enteras 3×3/4×4/5×5: 8/44/152 betweenness y 138/976/4242 congruencias.
- E2 (MDS no métrico sobre rangos, tolerancia 1e-13, + Procrustes): disparidad mediana en el plano 8.2e-3 (n=8) → 2.1e-10 (n=256), 7.6 órdenes de magnitud; en el espacio 4.2e-2 (n=8) → 4.1e-9 (n=128). Exponentes locales entre duplicaciones: 6.7 → 3.0 (no hay una ley de potencia única). Discordancia de Kendall entre el orden de entrada y el de la salida: 2.1e-2 (n=8) → 4.3e-6 (n=256): la reconstrucción está solo aproximadamente en la clase. E2b: la identidad de las reconstrucciones ordinales bajo D^p es tautológica (mismo rango de entrada); la métrica cambia (disparidad mediana 0.045).
- E3: en la recta, 4 puntos realizan 120 de los 720 órdenes de sus 6 distancias; en el plano y el espacio, los 720. Ejemplos: {0,1,3} vs {0,1,2.5}; triángulos (3,4,5) vs (3,4,6).
- E4 (300 ensayos, n=30): MST, grafo k-NN, grafo de vecindad relativa y par diametral invariantes bajo distorsión monótona de la matriz de distancias (fracción 1.00); diámetro (0.00), dimensión afín (0.35, esencialmente la probabilidad de que p∈(1,2)) y grafo de Gabriel (0.03) no. E4b: testigos exactos de no ordinalidad sobre Coord (colineal perturbado: mismo patrón, dimensiones 1 y 2; triángulo rectángulo perturbado: mismo patrón, arista de Gabriel presente/ausente).
- E5a: 200/200 reparametrizaciones conformes (que cambian los tiempos propios en una mediana del 23%) y 200/200 boosts preservan el orden; la rotación euclidiana cambia la relación de ~20% de los pares.
- E5b: fracción de pares comparables 0.499/0.230/0.101 frente a 0.500/0.229/0.100 esperado (D=2,3,4); estimación de dimensión 2.00±0.05, 3.00±0.09, 4.00±0.14.
- E5c: correlación L–τ 0.967 (n=250) → 0.990 (n=2000); pendiente L/(√n τ) 1.73 → 1.85 (límite 2); error relativo mediano de τ̂ (τ>1/4) 14% → 8% frente a τ, pero 23% → 17% frente al τ' de la configuración reparametrizada (el conteo fija el factor conforme).
- E5d: RMSE de coordenadas 0.073 (n=250) → 0.031 (n=2000), aproximadamente n^-0.39 (más lento que n^-1/2 por el mal condicionamiento de las raíces cerca de u=v); desacuerdo de comparabilidad 7.6% → 3.7%.

## Revisión arbitral interna (30/09/2026, misma sesión)
Un subagente revisor independiente leyó el borrador v0.1 completo (texto, código y resultados) y produjo 18 hallazgos. Todos se atendieron en la revisión v0.2:
1. Núcleo del orden causal: el resumen decía "es el grupo conforme"; se corrigió a "contiene al grupo conforme y es estrictamente mayor a n finito" y se añadió la Proposición 5.2 (las clases del núcleo son uniones de órbitas conformes sobre los realizadores de Dushnik–Miller del orden; ejemplo de la anticadena).
2. E5d: la frase "los pares relacionados no restringen el signo" era falsa; se corrigió el texto y el código ahora usa los votos de pares comparables e incomparables (el efecto numérico es <1%).
3. E2: las disparidades estaban limitadas por la tolerancia del solver (1e-9). Se rehízo con tolerancia 1e-13, se añadió la discordancia de Kendall entre el orden de entrada y el de salida (la reconstrucción solo está aproximadamente en la clase), se eliminó el exponente único (~n^-2.9) del resumen y de la tabla de afirmaciones, y se reportan exponentes locales.
4. E4: la explicación de la fracción 0.35 de la dimensión afín era errónea (el mecanismo real depende del rango de p: p<1 euclidiano en dimensión n-1; 1<p<2 exactamente dos autovalores positivos; p>2 muchos). Se añadió E4b con dos testigos explícitos de no ordinalidad (colineal perturbado; triángulo rectángulo perturbado para el grafo de Gabriel) y se aclaró que la columna de distorsión monótona prueba la fórmula sobre Met, condición suficiente para la profundidad ordinal.
5. E2b: se reescribió como verificación de la tubería (la identidad de reconstrucciones es tautológica).
6. Prop. 5.1 y texto: mapas conformes del diamante (no de Minkowski), boosts como mapas de R^{1,1}, grupo de Lorentz ortócrono en Zeeman.
7. E5d: tasa reportada como n^-0.4 observada, no n^-1/2; explicación por mal condicionamiento de las raíces cerca de u=v.
8. Coord(n,d) restringido a configuraciones inyectivas; Prop. 3.4 con puntos distintos.
9. Leyenda de la Tabla 1: una instancia de betweenness es un par (b,{a,c}).
10. Caus+N declarado como formalismo más modelo de muestreo; "segunda cadena" reemplazado por "traducción seguida de un paso estadístico".
11. Columna asintótica de la Sección 4 restringida a invariantes continuos.
12. E5c: N=(n-2)τ², pendiente por el origen, cita Baik–Deift–Johansson para la corrección N^{1/6}, columna τ' presentada como ilustración.
13. Definiciones 2.4 (profundidad 0) y 2.6 (fidelidad asintótica con distancia y cuantificador explícitos); observación de meaningfulness con dos tipos de escala.
14. Teorema 3.5 etiquetado "enunciado informal"; Terada–von Luxburg con hipótesis (grafo k-NN no ponderado, k→∞, k/n→0).
15. Hawking–King–McCarthy/Malament enunciados con precisión.
16. Bollobás–Brightwell 1991 (box-spaces) añadido para cadenas en dimensión arbitraria; 1992 queda para la concentración.
17. Fórmula de Myrheim–Meyer escrita como Γ(D+1)Γ(D/2)/(2Γ(3D/2)) y explicada como el doble del cociente ⟨R⟩/N².
18. Bibliografía: Klein citado como 1872 (con nota de la reimpresión de 1893); eslogan "orden + número" atribuido a Sorkin; Kronheimer–Penrose y Dushnik–Miller ahora citados.

## Añadido tras la revisión (v0.3): medición directa de la clase ordinal (E2c)
- Nueva Proposición (radio inscrito de la clase ordinal): si g(X) es la brecha mínima entre distancias consecutivas ordenadas, toda perturbación de cada punto menor que g/4 conserva el patrón; con pares extremos disjuntos, un desplazamiento explícito de g/4 produce un empate. Radio inscrito en [g/4, g/2], igual a g/4 en el caso disjunto. Demostración elemental (desigualdad triangular).
- Script `experiments/ordinal_class.py`: verifica ambas partes numéricamente, mide g(X) frente a n (corrida completa: escala ~n^-4.2, coherente con el espaciamiento mínimo entre ~n²/2 valores: ~n^-4; 2240/2240 perturbaciones bajo g/4 conservan el patrón y 91/91 desplazamientos explícitos lo rompen; la cifra "92/92" de versiones anteriores de esta nota era un error de transcripción) y corre un paseo aleatorio restringido a la clase que da una cota inferior del radio en disparidad de Procrustes (~n^-8.0). En n=64 esa cota es dos órdenes de magnitud menor que la disparidad a la que se detuvo el solver de E2: el residuo del solver es pertenencia aproximada, no tamaño de clase.
- Interpretación cuidada: el radio inscrito acota el grosor de la clase por arriba (ninguna bola de radio > g/2 cabe dentro); el paseo solo da una cota inferior del radio y muestra anisotropía. No hay cota superior del diámetro.
- Pendiente teórico: demostrar la ley n^-4 de la brecha mínima y una cota superior del diámetro de la clase.
- Segunda ronda de revisión arbitral interna realizada sobre v0.3 (véase la sección siguiente).

## Segunda ronda de revisión arbitral interna (v0.3 → v0.4)
Hallazgos confirmados y acciones:
1. Prop. 5.2 sobreenunciaba "estrictamente mayor que una órbita a n finito": una cadena tiene un único realizador y, para muestras uniformes, el número de realizadores módulo el intercambio es 1, 2, 4 u 8 en la gran mayoría de los casos (unicidad en alrededor de un tercio). Se reescribió la proposición (conteo = mitad de las orientaciones transitivas del grafo de incomparabilidad), se añadió E5e (conteo por clases de implicación de Golumbic, verificado por fuerza bruta en n=6) y se corrigieron resumen, texto y tabla de afirmaciones.
2. El "radio" del paseo restringido crece linealmente con el presupuesto de pasos (no está saturado): se renombró "rango del paseo", se eliminó la inferencia sobre el residuo del solver y se reformuló qué acota cada medición (grosor en X por arriba; extensión por abajo; sin cota del diámetro).
3. La comprobación numérica de la Prop. 3.8(i) usaba desplazamientos en caja (norma euclidiana hasta √2·g/4): corregida a desplazamientos uniformes en la bola euclidiana y relanzada.
4. "Ninguna bola de radio > g/2 cabe en la clase" era falso sin "centrada en X" (la clase contiene todas las semejanzas): corregido; "contenido finito del Teorema 3.7" reemplazado por "acota el grosor, no el diámetro módulo semejanza".
5. Resumen y tabla de afirmaciones: el radio inscrito lleva norma y condición (g/4 con pares disjuntos; [g/4, g/2] en general).
6. Prop. 3.8(ii): Y está fuera de la clase (empate); la prueba numérica detecta la inversión estricta justo más allá de g/4; se añadió la inyectividad (g ≤ D_min para n ≥ 3) y una observación sobre el caso de punto compartido.
7. Prop. 5.2: hipótesis explícita de coordenadas u y v distintas dos a dos; ejemplo de la anticadena escrito con desigualdades.
8. Consistencia: "dos secuencias" en vez de "dos cadenas"; tres scripts; semillas (E5: +1, E2c: +2); fecha v0.3; "less than one percent" reemplazado por una ablación reproducible (E5d con votos solo de pares incomparables); revista de Kronheimer–Penrose; "of dimension at most n−1".
Verificado por el árbitro sin cambios: numeración y referencias cruzadas, macros frente a JSON, parámetros del apéndice, las 10 ordenaciones de la recta, n!/2 para la anticadena, fracciones esperadas de E5b, las tres referencias nuevas y Klein 1872.

## Ronda 3 de revisión arbitral interna (v0.4 → v0.5, 03/10/2026)
Informe: `REFEREE_MRT001_ronda3_20260930.md` (veredicto "cambios menores": 0 bloqueantes, 4 mayores, 9 menores, 13 acciones). Respuesta punto por punto: `RESPUESTA_MRT001_ronda3_20260930.md`. Recuento: 11 hallazgos aceptados, 2 aceptados con matiz (M4, m8), 0 rebatidos; las 13 acciones aplicadas (la 13, opcional, también).

| hallazgo | acción aplicada |
|---|---|
| M1 Prop. 5.2: la fórmula de conteo falla para la cadena | enunciado: "1 for a chain and otherwise equals half the number of transitive orientations" (el código ya devolvía 1) |
| M2 hueco en la prueba de la Prop. 5.2 | prueba completada: T = <_u ∩ inc(≺) es orientación transitiva (a∥b, b∥c, a<_u b<_u c ⇒ v_a>v_b>v_c ⇒ a∥c); para toda orientación transitiva T, ≺ ∪ T es un orden lineal (caso mixto excluido por contradicción); la cláusula "for which ≺ ∪ T is transitive" se eliminó por automática |
| M3 Golumbic usado sin cita | `golumbic1977` (y `golumbic1980`) añadidos y citados en E5e y en el apéndice; E5e explica por qué la enumeración 2^k es exhaustiva |
| M4 Teorema 3.7 más débil que el original | añadidos la condición de regularidad de Ω, "all comparisons over quadruples" y "same dimension d"; identificación con la Def. 2.6 con C_n = segmentos iniciales de una sucesión densa fija y alineación uniforme en i ≤ n; Terada–vL con "at a rate specified there"; tabla de afirmaciones: "literature (informal statement)". **Cotejo con los PDF originales pendiente**: desde el contenedor están bloqueados tml.cs.uni-tuebingen.de, proceedings.mlr.press, dl.acm.org y projecteuclid.org; el cotejo se hizo con resúmenes secundarios (reformulación de Arias-Castro), que coinciden con las hipótesis añadidas |
| m1 observación del caso de punto compartido (Prop. 3.8) | sustituida por la fórmula g/(2(1+sin(θ/2))) a primer orden, g/4 exacto en el caso colineal con a en medio, → g/2 cuando θ → 0, y el argumento de que el radio inscrito es el mínimo de los desplazamientos de cierre sobre pares consecutivos; verificada numéricamente por el autor (coincidencia a 5 cifras en 180°, 150°, 120°, 90°, 60°) |
| m2 "at most 3g²/8" | "of order 3g²/8" con la justificación E‖X_c‖²_F = n/6; macro `\EtwocBoundNsixtyfour` renombrado `\EtwocDispEstNsixtyfour` (mismo valor) |
| m3 "(Schoenberg)" sin referencia | `schoenberg1937` añadido y citado |
| m4 fuente de los realizadores extra | "typically come from"; mecanismo formulado con la fórmula producto de Golumbic sobre módulos (par de gemelos incomparables = módulo; factor 2 cuando esos pares son los únicos módulos no triviales y el cociente es primo); nueva **Conjetura 5.3**: realizadores = 2^N con probabilidad → 1, N → Poisson(1) (predicciones 0.368/0.368/0.981 frente a 0.34/0.37/0.98 en n = 300); nuevo experimento **E5f** (`experiments/realizer_law.py`, semilla 20260933, 128 s): count = 2^N en 151/200, 179/200, 192/200, 98/100, 98/100, 49/50 para n = 20, 50, 100, 200, 300, 500 (767/850; 437/450 con n ≥ 100); las excepciones difieren de 2^N por factores 3/2, 2 o 3 (módulos mayores). Tabla E5f, párrafo E5f del apéndice, fila "conjectural" en la tabla de afirmaciones, cita `kaplansky1945` para la ley de Poisson de las sucesiones |
| m5 versiones, tiempos y recuentos | portada "v0.5 — 3 October 2026" (fecha fija, sin `\today`); README y ficha a v0.5 con tres rondas; en esta nota 92/92 → 91/91 y 149 s → 315 s |
| m6 restos de "walk radius" | `ordinal_class.py`: docstring, mensajes, leyenda de la figura, cabecera de `tables_class.md` y claves JSON (`walk_range_*`, `slope_walk_range`, `raw.ranges`); `make_numbers.py` adaptado; nuevo modo `--replot` que regenera figura y tablas desde el JSON existente y migra las claves antiguas (anotado en `meta.keys_renamed`; valores intactos). La corrida de 168 s no se relanzó porque ningún valor cambia |
| m7 `\EfiveDablation` imprimía "less than one percent" | imprime siempre el porcentaje con signo y un decimal (+0.4 %); el texto da además los dos RMSE (0.0312 → 0.0313) |
| m8 `meyer1988` | año 1989 con `note = {MIT handle 1721.1/14328; often cited as 1988}`; clave renombrada `meyer1989`; el registro del MIT no pudo consultarse desde el contenedor (dato tomado del informe) |
| m9 inyectividad en Prop. 3.8(ii) | adelantada al enunciado ("an injective configuration Y … because g ≤ min D_ab") |
| acción 13 (opcional) | DOI de `sorkin2005`; número `CERN-TH-2538` y URL del registro CDS 293594 en `myrheim1978` |

Los dos puntos "parciales" de la verificación del árbitro sobre las rondas 1 y 2 (leyenda "walk radius"; portada v0.3 y "less than one percent") quedan cerrados con m6, m5 y m7.

Estado tras la ronda 3: manuscrito v0.5 de 20 páginas (v0.4: 18; el aumento son la prueba completa de la Prop. 5.2, el párrafo del caso compartido, la conjetura con la Tabla E5f y una página de flotantes con la Figura 3 y la tabla de afirmaciones); 0 errores, 0 referencias o citas indefinidas, 0 cajas desbordadas; 41 entradas en `refs.bib` (37 + golumbic1977, golumbic1980, schoenberg1937, kaplansky1945). Ningún número previo del texto cambió; se añadieron los de E5f. Cómputo de la ronda: ≈ 4 min de CPU (E5f 128 s, verificaciones del autor, `--replot` y cinco compilaciones), sin relanzar E1–E5.

Queda abierto tras la ronda 3:
1. Cotejar el Teorema 3.7 (número de teorema, condición exacta de regularidad, modo de convergencia: uniforme en i ≤ n o puntual) y la frase sobre Terada–von Luxburg (condición exacta sobre k) con los PDF originales.
2. Confirmar en el registro del MIT el año de la tesis de Meyer y, en Kaplansky 1945, el parámetro (1 para sucesiones en una dirección fija; 2 en cualquier orden según las fuentes secundarias consultadas).
3. Demostrar la Conjetura 5.3: con probabilidad → 1 los únicos módulos no triviales del grafo de incomparabilidad de una permutación uniforme son las sucesiones descendentes (bloques de tamaño 2) y el cociente es primo; el conteo esperado de bloques de tamaño ≥ 3 es O(1/n).

## Integración de la Conjetura 5.3 demostrada (03/10/2026)
Un agente teórico dejó en `theory/` una prueba de la Conjetura 5.3 (`realizer_law_theorem.tex`, notas `realizer_law_derivation.md`), su comprobación numérica (`check_realizer_law.py` y su salida) y tres entradas bibliográficas nuevas. El agente integrador la verificó antes de pasarla a `main.tex` (v0.5 → v0.6).

**Qué se verificó.**
- Lectura paso a paso de toda la prueba. Lema de intervalos y módulos: la ruta inicial "módulos de G_π = intervalos de π" es falsa (π = id, {1,3} es módulo y no intervalo); lo que se usa, y es correcto, es "π simple ⇔ G_π primo" (n ≥ 3). Lema de inflación: el argumento del conjunto S de vértices "mixtos" es correcto (B ∪ S es módulo; S ≠ ∅ obligaría a un vértice universal o aislado en el cociente primo). Paso 1: sucesiones disjuntas, contracción a una σ simple con m ≥ 4, t(G_π) = 2·2^N.
- Constantes del Paso 2, una por una: E I_3 = 6(n−2)/(n(n−1)) ≤ 6/n − 6/n², E I_{n−1} = 4/n, E I_4 ≤ 24/n² (siempre), E I_{n−2} ≤ 19/n² (n ≥ 19), E I_{n−3} ≤ 6/n² (n ≥ 19), E I_{n−4} ≤ 3/n² (n ≥ 20), los n−9 términos centrales ≤ 120/n² (⇔ 7n² − 25n − 6 ≥ 0); total 10/n + 166/n². Momentos factoriales: biyección por contracción de rachas, r!·C(n−1,r)·(n−r)!/n! = 1 − r/n exacto; cota de inclusión–exclusión y masa de Poisson más allá de n−1 (≤ 2/n!) correctas; paso 4 (acoplamiento) correcto.
- Clasificación de excepciones: 123, 132, 213 → factor 1; 321 → 3/2; 231, 312 → 2; π(1)=n o π(n)=1 → 2 (vértice universal, fuente o sumidero porque el complemento de G_{π'} es conexo); π(1)=1 o π(n)=n → 1. Cota de pares de intervalos de 3 elementos disjuntos recomputada de forma exacta: 18(n−4)(n−5)(n−4)!/n! ≤ 18n²(n−4)!/n!. Tasa 3(n−2)/(n(n−1)) + 2/n = 5/n + O(n⁻²).
- `check_realizer_law.py` reejecutado (81 s de CPU, 88 s de pared): salida idéntica a la del agente teórico salvo los tiempos (0 discrepancias fórmula/fuerza bruta en las 5913 permutaciones con n ≤ 7; 3318 permutaciones simples con n = 4…8, todas con un solo realizador; n·P(R ≠ 2^N) entre 4,83 y 5,40 para n = 20…2000). Salida congelada en `results/check_realizer_law_output.txt`, SHA-256 `4e011b1e04312e479b3de9ebeb1d27625d287ec152ddc0cd139e608022e0dc84` (en `results/check_realizer_law_output.sha256`; `make_numbers.py` la verifica antes de leerla).
- Fuerza bruta propia en n = 7 de cuatro casos (π(1)=n y π(n)=1; π(1)=n y π(2)=n−1; π(1)=n solo; bloque 321).

**Qué se corrigió.** (1) Enunciado de Gallai: "con al menos tres vértices" (el grafo de dos vértices sin aristas es primo con la definición usada y tiene una sola orientación). (2) Observación final sobre la fórmula exacta: los dos lemas no bastan por sí solos (falta el paso de las sumas sesgadas, factor k!, ahora esbozado y marcado como clásico), y el ejemplo de factor 3 era erróneo: π(1)=n con π(n)=1 da factor 6; π(1)=n con π(2)=n−1 da 3 (comprobado por fuerza bruta). (3) La frase "las excepciones difieren de 2^N en un factor 3/2, 2 o 3" se sustituyó por los cocientes observados, generados desde el JSON: 3/2, 2, 3, 4 y 6 en total, y solo 3/2 y 2 para n ≥ 100, como predice la Proposición 5.7.

**Qué se integró en `main.tex`.** Sección 5: la Conjetura 5.3 se sustituye por el párrafo "The realizer law" (definiciones), el Teorema 5.3 (Gallai, [literature]), los Lemas 5.4 y 5.5, el Teorema 5.6 (ley de realizadores, [proved here, using Theorem 5.3]) y la Proposición 5.7 (excepciones), un esquema de las pruebas y un párrafo "Sharpness and data"; el párrafo de E5e ya no dice "which suggests the following" y cita el Lema 5.5 y el Teorema 5.3 en lugar de la fórmula de producto. Apéndice B nuevo con las pruebas completas, la Observación B.1 (fórmula exacta, clásica) y la descripción de la comprobación numérica. Tabla E5f: dos columnas nuevas (fracción observada de excepciones y 5/n, generadas por `make_numbers.py` desde `results/results_realizer_law.json`) y pie actualizado. Tabla de afirmaciones: fila de Gallai (literature), fila del Teorema 5.6 (proved here, uses Gallai), fila nueva de la Proposición 5.7 y fila "verified" de E5f. Resumen, introducción (punto 3 y alcance), limitaciones y apéndice de reproducibilidad actualizados. Portada: v0.6, 3 October 2026.

**Bibliografía.** Añadidas `gallai1967`, `albert2005`, `wolfowitz1944`. Gallai: volumen 18, páginas 25–66, 1967 y la traducción de Maffray–Preissmann confirmados por WebSearch solo en fuentes secundarias; el enunciado ("un grafo primo tiene a lo sumo dos orientaciones transitivas, una inversa de la otra") también confirmado en fuentes secundarias; número del teorema **no verificado en línea** (Springer, arXiv y Crossref bloqueados por el proxy), por eso no se cita número. Albert–Atkinson 2005 (Discrete Math. 300(1–3):1–15) confirmado por WebSearch; número de la proposición no verificado (no se cita). Wolfowitz 1944: datos confirmados por el agente teórico en Project Euclid, no recomprobados por el integrador.

**Compilación.** `manuscript/build.sh`: 0 errores, 0 referencias o citas indefinidas, `pdftotext main.pdf - | grep -c "??"` = 0, sin cajas desbordadas; 20 → 26 páginas (unas 1,5 páginas en la Sección 5 y 3 de apéndice; se añadió `\clearpage` antes de los apéndices para que la figura 4 y la tabla de afirmaciones no queden detrás de la bibliografía).

**Qué queda abierto.** (a) Cotejar el teorema de Gallai con el original o la traducción inglesa (número y enunciado exacto). (b) La cota de d_TV es holgada: e²/n frente a n·d_TV(N, Po(1)) = 0,368 ≈ e⁻¹ numérico, y la cota (a) 10/n es el doble de la tasa real 5/n; afinar ambas constantes queda pendiente (no se afirma ninguna constante óptima). (c) La tasa 5/n en E5f se contrasta con muestras pequeñas (13 excepciones observadas frente a 14,7 esperadas para n ≥ 100); el apoyo cuantitativo es la comprobación con 10 000–20 000 permutaciones por n. (d) El paso de sumas sesgadas de la fórmula exacta (Observación B.1) solo está esbozado; no se usa en las pruebas. (e) El contenido de Wolfowitz 1944 y Kaplansky 1945 no se cotejó más allá del título.

## Decisiones tomadas
- Objetos etiquetados en todos los formalismos (sin cociente por reetiquetado), para mantener las demostraciones elementales.
- E1 con aritmética exacta y no con tolerancia flotante: la tolerancia 1e-9 produce ~1 triple espurio por configuración en n=50 (la brecha de betweenness es cuadrática en la distancia a la recta). Se menciona en el texto como advertencia metodológica.
- Cadena lorentziana solo en 1+1 y fondo plano, presentada como modelo matemático; la sección deja explícito qué no se afirma.
- Idioma del manuscrito: inglés (los títulos de la línea en el CV están en inglés); README y nota de continuidad en español.

## Pendientes y próximos pasos sugeridos
1. Confirmar con el autor la identificación paper ≡ MRT001 y si existe un manuscrito previo que deba integrarse.
2. Revisión del autor de las Proposiciones 3.2, 3.4 y 5.1 (verificadas línea a línea por el árbitro en la ronda 3) y cotejo del Teorema 3.7 (enunciado informal de Kleindessner–von Luxburg) con el enunciado exacto del artículo (véase "Queda abierto tras la ronda 3").
3. Cota finita para el diámetro de las clases ordinales bajo muestreo uniforme (explicaría la caída ~n^-3.6 observada en E2).
4. Extender E5d a 2+1 dimensiones (grupo conforme finito-dimensional) y a densidades no uniformes.
5. Decidir destino: arXiv (math.MG / math.HO) o revista; ajustar formato.
6. Actualizar la ficha MRT001 del CV web: de "En pausa" a "En desarrollo — borrador v0.6" (texto en `FICHA_MRT001_propuesta.md`).
7. Hecho en v0.6: la Conjetura 5.3 está demostrada (Teorema 5.6). Queda cotejar el teorema de Gallai con la fuente original y, si interesa, afinar las constantes (véase "Integración de la Conjetura 5.3 demostrada").
