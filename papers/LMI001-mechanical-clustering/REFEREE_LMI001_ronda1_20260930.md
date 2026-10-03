# Informe de árbitro interno independiente — LMI001, ronda 1 (30/09/2026)

Objeto: `papers/LMI001-mechanical-clustering/` (manuscrito `manuscript/main.tex` v0.1, código `experiments/`, resultados `results/`, README, nota de continuidad, ficha propuesta). Revisado todo el material listado en el brief; páginas del PDF renderizadas y revisadas (1, 6, 8, 9, 10, 11, 12). Archivos de trabajo del árbitro en el scratchpad (`referee_LMI001/`), no en esta carpeta. Las referencias a líneas son de `manuscript/main.tex` salvo indicación.

## Veredicto

**Cambios mayores.** Las matemáticas centrales son correctas (Lema 3.1, Teorema 3.2(a)–(f), Prop. 3.3, fórmula (6) y Prop. 3.8 verificadas paso a paso; E1–E3 reproducidos en modo rápido con las mismas magnitudes), pero el manuscrito (i) presenta como hecho una reconstrucción no confirmada de lo que hizo la línea y deriva de ahí su tesis ("el cribado nulo es un teorema"); (ii) etiqueta "proved here" el núcleo del Teorema 3.2(b), que es la equivalencia ratio association ↔ kernel k-means de Dhillon–Guan–Kulis; (iii) contiene un error aritmético en una prueba, una afirmación no demostrada dentro de un enunciado y un factor ½ perdido en un teorema y en el resumen; (iv) sobregeneraliza el Teorema 4.1 en resumen, tabla de afirmaciones, README y ficha; (v) no revela en el texto el cambio a posteriori de la línea base de E3; y (vi) la ficha propuesta cierra la línea con un borrador no revisado. Todo es corregible sin rehacer experimentos.

## Hallazgos bloqueantes

**B1. La familia "mecánica" es una reconstrucción no confirmada y el manuscrito la presenta como lo que la línea hizo.**
- Ubicación: línea 61 ("The research line … studied formulations of a more elementary kind: points connected by springs, with tension and lifting terms, clustered by minimising an elastic energy"); línea 63 ("A control that matches the kernel therefore matches the objective exactly, and no experiment can separate them"); línea 304 ("The screening could not have found a mechanical effect"); resumen línea 56 ("the null result is a theorem, not an accident").
- Problema: `CONTINUIDAD_LMI001_20260930.md`, "Supuestos reconstruidos (verificar con el autor)", punto 1, reconoce que no existe manuscrito ni código previo y que la definición de la familia y del "control emparejado" se dedujo de la ficha pública. El manuscrito no lo dice en ninguna parte; la tesis del resumen y de la Sección 5 depende de ese supuesto. Si la línea original usó términos de muchos cuerpos, longitudes de reposo adaptativas o dinámica de posiciones (todos admitidos por la propia Sección 4), la conclusión no se sigue.
- Corrección: (a) en la Introducción, tras la línea 61, añadir: "The definitions of Section 2 are a reconstruction from the line's public summary; no manuscript or code of the original screening was available to us. The conclusions below apply to objectives of that pairwise form." (b) Reescribir la línea 304 como "If the screened formulations were of the pairwise kind of Definition 2.1, the screening could not have found a mechanical effect: …". (c) En el resumen, "This note shows that, for the pairwise family defined below, the null result is a theorem". (d) Antes de cualquier difusión, obtener del autor la confirmación del supuesto 1 de la nota de continuidad; si no se confirma, mover el énfasis a la Sección 4 como la propia nota prevé.

**B2. La ficha propuesta cierra la línea y afirma más de lo demostrado.**
- Ubicación: `FICHA_LMI001_propuesta.md`, campo "Estado: Cerrada con resultado — Borrador v0.1" (español e inglés); campo "Principales hallazgos", frase final ("Con aritmética exacta se certifica que términos de muchos cuerpos, longitudes de reposo adaptativas y normalización por resorte salen de la familia"); campo "Alcance actual", primera frase. `README.md`, línea "Conclusión para la línea: el cribado nulo no fue un experimento fallido sino una consecuencia de la equivalencia."
- Problema: "Cerrada con resultado" sobre un borrador v0.1 sin revisión independiente y con el supuesto B1 sin confirmar es prematuro y además contradictorio con "Borrador v0.1" en el mismo campo. "Términos de muchos cuerpos" en general no está certificado: el Teorema 4.1 prueba un solo término de tres cuerpos (4·area²) y una sola regla de longitud de reposo adaptativa (media del clúster) en una instancia; existen términos de tres cuerpos que sí son de pares (p. ej. Σ_{i<j<l∈C_c}(s_ij+s_jl+s_il) = (n_c−2)Σ_{i<j} s_ij).
- Corrección: Estado → "Activa — borrador v0.1 en revisión interna" (o mantener "En pausa" hasta confirmar B1). Hallazgos → "…certifica, en una configuración explícita, que el término de tres cuerpos, la longitud de reposo adaptativa y la normalización por resorte ensayados no son objetivos de pares". Alcance → "Si las formulaciones cribadas eran de pares, el cribado nulo es consecuencia de la equivalencia". Misma corrección en la frase del README.

## Hallazgos mayores

**M1. Teorema 3.2(b) etiquetado "proved here" es la equivalencia ratio association ↔ kernel k-means de Dhillon–Guan–Kulis.**
- Ubicación: líneas 127 y 318 (Tabla 4, fila 2: "proved here"); línea 119 (se cita a Dhillon solo por el desplazamiento diagonal).
- Problema: E_sp = ½Σ_c 1_cᵀA1_c/n_c − ½kφ(0) es exactamente la "ratio association" de la matriz de afinidad A = φ(D); Dhillon, Guan y Kulis (2004, Tabla de objetivos; 2007, Sec. 2–3) demuestran que minimizar/maximizar ratio association es kernel k-means con K = σI ± A. La aportación propia de (b) es la identificación "energía de resortes = ratio association", no la equivalencia.
- Corrección: en la fila de la Tabla 4 y tras el enunciado, "literature (ratio association ↔ kernel k-means, Dhillon et al. 2004, 2007), stated here for spring matrices with the explicit constant"; en la línea 67 añadir "ratio association" a la lista de lo que es clásico. Lo mismo, en menor grado, para (e): es la identidad (c) aplicada en el espacio de características (clásica desde Girolami 2002 / Zha et al. 2001); etiquetar "classical".

**M2. Error aritmético en la prueba de la Prop. 3.7(iii).**
- Ubicación: línea 188 ("moving the point 2 gives SSE = 1.72") y línea 192 ("SSE = 0+1+0.16+0.16 = 1.72").
- Problema: con clústeres {0} y {2, 3.4, 3.6} (centroide 3), (3.6−3)² = 0.36, no 0.16. SSE = 0 + 1 + 0.16 + 0.36 = **1.52**. Comprobación con (6): ΔJ = (2/3)(1.5)² − 2·(1)² = −0.5, luego 2.02 − 0.5 = 1.52. La conclusión (el recíproco falla) sobrevive.
- Corrección: sustituir 1.72 por 1.52 en ambas líneas y "0.16+0.16" por "0.16+0.36".

**M3. La Prop. 3.5 enuncia una no representabilidad que su prueba declara no demostrar.**
- Ubicación: línea 169 ("For a general φ … the resulting objective is not of the form (1)") frente a línea 172 ("we do not prove a non-representability statement for anchored objectives"); etiqueta "[classical]".
- Problema: un enunciado contiene una afirmación sin prueba (y falsa tal cual para φ = d², que es "general" también). La etiqueta "classical" no la cubre.
- Corrección: reescribir "…is a Weber-type location problem; with φ(d) = d it is the k-median objective. We make no claim about whether these anchored objectives are of the form (1)." y mantener "[classical]" solo para la primera frase.

**M4. Factor ½ perdido en el Teorema 3.2(f) y en el resumen.**
- Ubicación: línea 135 ("so the spring energy is, up to the constant, the per-particle Hooke energy of (Φ(Lx_i))_i"); línea 146 (última frase); resumen línea 56, puntos (ii) y (iii) ("is, up to an additive constant, the kernel k-means objective"; "literally the Hooke energy of a lifted configuration").
- Problema: de ‖Φ(x)−Φ(y)‖² = 2(φ(d)−φ(0)) se sigue E_{d²,Φ,sp} = 2E_sp − (n−k)φ(0), es decir E_sp = ½·Hooke(Φ) + const, no Hooke(Φ) + const. Para Hooke, K̃ = 2⟨x,y⟩, Φ = √2·x y Hooke(Φ) = 2·SSE. El propio (b) tiene el ½ explícito; (f) y el resumen lo omiten.
- Corrección: definir el mapa con Φ̃ = Φ/√2 (entonces ‖Φ̃(x)−Φ̃(y)‖² = φ(d)−φ(0) y E_sp = E_{d²,Φ̃,sp} + ½(n−k)φ(0)), o escribir "half the per-particle Hooke energy". En el resumen: "is, up to an additive constant and a factor ½, the kernel k-means objective of −φ(D)" y "is, up to a constant and a rescaling, the Hooke energy of a lifted configuration".

**M5. Sobregeneralización del Teorema 4.1 (una instancia, un término de cada tipo).**
- Ubicación: resumen línea 56 ("many-body terms, assignment-dependent rest lengths and per-spring normalisation are not pairwise objectives"); Tabla 4 línea 330 ("Adaptive rest length, three-body term, per-spring normalisation and cross-normalisation are not pairwise objectives"); README línea de E4 e "Idea del paper" punto 3; ficha (véase B2).
- Problema: el teorema está bien acotado en su enunciado (configuración P explícita) y la frase de la línea 224 ("A single instance suffices, since the claims are that these ingredients are not in general pairwise") es correcta para los tres funcionales concretos ensayados; pero "many-body terms" como clase no está certificado (contraejemplo en B2), y "assignment-dependent rest lengths" solo se probó con ρ_c = media del clúster.
- Corrección: en todos los lugares, "the three-body (triangle-area) term, the cluster-mean rest length and the per-spring average tested here are not pairwise objectives (one explicit configuration, exact arithmetic)". Añadido positivo: la corrida `--fast` genera otra configuración (puntos (2,4),(6,0),(2,8),(10,6),(6,7),(3,6),(6,2)) con el mismo patrón de representabilidad en las 12 celdas; conviene reportar ambas instancias y decir "two explicit configurations".

**M6. Cambio a posteriori de la línea base de E3 no revelado en el manuscrito.**
- Ubicación: línea 272 ("Criteria (predefined)"); `experiments/relaxation.py` líneas 13–15 (C3a: "Voronoi-stable in the feature space of the PSD-shifted kernel", redacción de la versión antigua); `CONTINUIDAD`, "Decisiones tomadas", segundo punto ("en un primer intento se había usado como baseline [−φ(D)+σI] y resultaba inerte (σ hasta 4e4)").
- Problema: los criterios C3a–C3c se escribieron cuando la línea base de Lloyd era −φ(D)+σI; tras ver que ese Lloyd era inerte se cambió la base a K̃ y se dejó la antigua como "control". Los umbrales (10⁻⁶, 10⁻⁹) no cambiaron, y el cambio es conservador respecto a la tesis del paper (favorece al kernel k-means), pero el texto solo dice "predefined". Comprobé con las fechas de modificación que todos los números del manuscrito provienen de la versión final del código (`relaxation.py` 08:46 < `results_relaxation.json` 08:50; `identity_check.py` 08:42 < `results_identity.json` 08:49): **ningún número del manuscrito procede de la versión antigua**. Residuos de la versión antigua: (a) `identity_check.py` líneas 93–94 generan las particiones "kernel k-means" de E1 con Lloyd sobre Ks = −φ(D)+σI (inofensivo para la identidad, pero el texto de la línea 254 las llama "outputs of kernel k-means" y, por la Prop. 3.8, son casi las etiquetas iniciales de k-means++); (b) docstring de `relaxation.py` líneas 6 y 13–15; (c) el texto de la línea 254 dice "σ is up to 10⁴" cuando el máximo es 4.4×10⁴ (`results_identity.json`, E1.rows, blobs/hooke).
- Corrección: en la línea 272 añadir "The canonical kernel K̃ replaced −A+σI as the Lloyd baseline after a pilot run showed the latter to be inert (Proposition 3.8); the thresholds of C3a–C3c were fixed before that pilot and were not changed." Corregir "up to 10⁴" → "up to 4.4×10⁴". Actualizar el docstring. Opcional: en E1 usar Ks = K̃ para generar las particiones de kernel k-means (no cambia la conclusión).

**M7. Novedad de la Prop. 3.8 sin cotejar con Dhillon et al. (2007).**
- Ubicación: línea 197 "[proved here]", línea 202, Tabla 4 línea 328; `CONTINUIDAD` ("es el hallazgo colateral más útil de la sesión").
- Problema: la prueba es correcta y de una línea. Según mi recuerdo, Dhillon, Guan y Kulis (2007, en la discusión del desplazamiento diagonal) ya observan que un σ grande hace que los puntos tiendan a quedarse en su clúster y degrada los óptimos locales; no pude verificar el texto (dominios `cs.utexas.edu`, `people.bu.edu` y `dl.acm.org` bloqueados por el proxy de esta sesión).
- Corrección: antes de presentarla como aportación, leer dhillon2007 (sección sobre "enforcing positive definiteness" y los experimentos) y dhillon2004; si la observación está, citarla y dejar la Prop. 3.8 como "cuantificación explícita de un efecto señalado por [7]".

**M8. Extensión: 15 páginas frente a 5–10.** Véase la sección "Recortes".

## Hallazgos menores

- **m1.** Prop. 3.7(ii), líneas 187 y 192: "fixed point of Lloyd's algorithm" solo vale con empates resueltos a favor del clúster actual (la estabilidad demostrada es δ(i,c) ≥ δ(i,a), no estricta). Añadir "with ties broken in favour of the current cluster". Los clústeres vacíos no son problema (la relajación exige n_a ≥ 2; los singletons cumplen δ(i,a) = 0). El código `lloyd()` usa `argmin` (primer índice), es decir, otra convención de empate; es coherente porque `is_voronoi_stable` usa ≤ con tolerancia.
- **m2.** Prop. 3.7, línea 184 ("the right-hand side does not depend on the representative K'"): la prueba (línea 192) solo trata las tres invariancias del Lema 3.1; para un K' PSD arbitrario con J_{K'} = J_K + const basta observar que ΔJ_{K'} = ΔJ_K y que la identidad algebraica vale para todo K' simétrico. Añadir esa frase.
- **m3.** Título (línea 44) "Mechanical Analogies for Data Clustering Are Kernel Clustering": más general que el contenido (la vía dinámica queda fuera). Propuesta: "Spring-Energy Clustering Is Kernel Clustering: An Equivalence Theorem Behind a Null Screening".
- **m4.** Teorema 3.2(f) "independent of the dataset": las escalas ℓ, r, s se derivan de los datos (línea 239), de modo que el kernel es independiente del conjunto dadas las escalas. Decirlo en una frase.
- **m5.** Nomenclatura: "positive definite kernel" (sentido Berg–Christensen–Ressel, matrices PSD) frente a "PSD" para matrices (líneas 98, 131, Tabla 2). Fijar una convención en la Definición 2.5.
- **m6.** Prop. 3.3(ii), línea 157: dar los números de resultado. Según mi recuerdo del libro, el lema CND↔PD es BCR Cap. 3, §2, Lema 2.1, y el teorema de Schoenberg es Cap. 3, §2, Teorema 2.2; la composición con funciones de Bernstein está en el Cap. 3 §2 / Cap. 4 (confirmar en el libro; no verificable en línea en esta sesión). El esbozo incluido es correcto y autocontenido.
- **m7.** `relaxation.py` líneas 89, 95 y 101: `hartigan=True` está escrito a mano para lloyd+relax, relax y anneal, no medido; `results/tables_relaxation.md` lo reporta como "single-move-stable 600/600" como si fuera una medición. Llamar a `is_hartigan_stable()` o etiquetar "by construction". El manuscrito no usa esas cifras (las macros `\EthreeHartiganRelax` etc. están sin usar).
- **m8.** `identity_check.py` líneas 253–257: la configuración de E4 se extrae del generador maestro después de E1 y E2, así que depende de `--fast` (en modo rápido salen otros puntos). Apéndice A línea 353 ("with the master seed") debe decirlo, o usar un generador propio `default_rng(SEED + 2)`.
- **m9.** README ("5 a favor de la relajación, 1 en contra") y línea 272: en la corrida rápida el reparto es 3 a 3 con el mismo 6/30 de configuraciones distinguibles; la dirección es ruido de optimizador, como el propio texto sostiene. No destacar el reparto en README ni ficha.
- **m10.** Docstrings y comentarios del código numeran "Theorem 1(b)", "Theorem 1(f)", "Proposition 3" (`mechanical.py` líneas 13, 38, 156; `relaxation.py` líneas 15, 26); el manuscrito usa 3.2 y 3.7. Alinear.
- **m11.** `refs.bib` tiene 4 entradas no citadas (aloise2009, selim1984, shimalik2000, vonluxburg2007; README dice "29 referencias", correcto para las citadas). `numbers.tex` define 27 macros no usadas (lista en el scratchpad del árbitro). Limpiar o dejar constancia.
- **m12.** Figura 1 (p. 9): a tamaño de impresión, etiquetas del eje x y leyenda ilegibles (~5 pt). Subir fuentes a ≥ 7 pt, usar 2×3 paneles o una figura por fila. Figura 2 (p. 10): media página en blanco y títulos internos diminutos; ver "Recortes".
- **m13.** Cuatro cajas horizontales desbordadas (1.4–7.9 pt; el log las repite 3 veces por pasada, de ahí "12" en `log_build.txt`): líneas 145 (ecuación en la prueba de (b)), 211–218 (tabla del Teorema 4.1), 277–286 (Tabla 3), 313–338 (Tabla 4). Partir la ecuación de la línea 144 en dos líneas; reducir `\tabcolsep`.
- **m14.** Fecha con `\today` (línea 49): cambia en cada compilación; fijar "30 September 2026".
- **m15.** Línea 63 "no experiment can separate them": E3 separa optimizadores (6/30). Precisar "no experiment on objective values".
- **m16.** Tabla 2, columna "negative type": es la etiqueta de la Prop. 3.3, no una comprobación (bien explicado en el pie); renombrar "negative type (Prop. 3.3)".

## Bibliografía

Red: `api.crossref.org`, `proceedings.mlr.press`, `dl.acm.org`, `cs.utexas.edu` y `people.bu.edu` bloqueados por el proxy de salida; la verificación se hizo con WebSearch (resúmenes de dblp/ACM/Semantic Scholar). "No verificable" significa que no pude contrastarla de forma independiente en esta sesión; los datos son coherentes con mi conocimiento.

| Entrada | Estado | Corrección / nota |
|---|---|---|
| sahni1976 | verificada (J. ACM 23, 555–565, 1976) | Atribución del min-sum k-clustering ("k-min cluster"/"k-max cut") a este trabajo es la aceptada en la literatura (Guttmann-Beck & Hassin 1998; Bartal, Charikar & Raz 2001). Sin cambios. |
| wright1977 | verificada (Pattern Recognition 9, 151–166, 1977) | Número (3) no confirmado; mantener. |
| telgarsky2010 | verificada (AISTATS 2010, JMLR W&CP 9, 820–827) | Sin cambios. |
| zha2001 | verificada (NIPS 14, 1057–1064) | `year = {2002}` con `booktitle` "NIPS 2001": aceptable (MIT Press 2002); unificar si la revista lo exige. |
| bcr1984 | verificada (GTM 100, Springer 1984) | Añadir números de lema/teorema (m6). |
| dhillon2004, dhillon2007 | no verificables en línea; datos correctos según mi conocimiento | Respaldan el desplazamiento diagonal; deben citarse además para (b) (M1) y posiblemente para la Prop. 3.8 (M7). |
| schoenberg1935, schoenberg1938 | no verificables en línea; datos correctos según mi conocimiento | El uso (CND ⇔ e^{−tN} PD; inmersión en Hilbert) es correcto. |
| ssv2012 | no verificable en línea; datos correctos según mi conocimiento | Añadir el teorema de representación (Lévy–Khintchine) citado en la Def. 2.5. |
| hartigan1975, hartiganwong1979, lloyd1982, macqueen1967, arthur2007, girolami2002, scholkopf1998 | no verificables en línea; datos correctos según mi conocimiento | Respaldan lo que se les atribuye. |
| rose1990, rose1998, blatt1996, horn2002, durbin1987, yuille1990, fukunaga1975, cheng1995, comaniciu2002, kirkpatrick1983, pedregosa2011, virtanen2020 | no verificables en línea; datos correctos según mi conocimiento | Solo contextuales. |
| aloise2009, selim1984, shimalik2000, vonluxburg2007 | no citadas en el texto | Eliminar del .bib o citar (selim1984 sería pertinente en la Prop. 3.7 para puntos fijos de Lloyd). |

Resumen: 5 verificadas (sahni1976, wright1977, telgarsky2010, zha2001, bcr1984), 0 corregidas, 24 no verificables en esta sesión (sin indicios de error), 4 sin citar.

## Verificación computacional

- Entorno: Python 3.11.15, NumPy 2.4.6, SciPy 1.17.1, scikit-learn 1.9.1, Matplotlib 3.11.2 (idénticas a las del manuscrito); 4 núcleos. Copia aislada del código en el scratchpad; la carpeta del paper no se modificó.
- `identity_check.py --fast`: 42.7 s de pared, 44.9 s de CPU, salida 0. `relaxation.py --fast`: 10.7 s de pared, 13.6 s de CPU, salida 0. Total ≈ 59 s de CPU.
- Macros frente a JSON: 32 comparaciones (`numbers.tex` vs `results_*.json`, incluidos recuentos independientes por corrida de la estabilidad de Voronoi, de la estabilidad de un movimiento de Lloyd y de las configuraciones distinguibles): 0 discrepancias. Las tablas `table_*.tex` coinciden con los JSON y con los logs.
- Coincidencias de la corrida rápida (n = 150 por conjunto, 50 particiones aleatorias, 2 inicializaciones E2, R = 4): E1 5035/5035 comprobaciones, error máximo 7.6×10⁻¹² (ref. 1.1×10⁻¹¹), Hooke vs SSE 3.9×10⁻¹⁶, K̃ PSD 25/25 e indefinido 5/5; E2 60/60 trayectorias idénticas (2.7×10⁻¹⁴ → 1.8×10⁻¹⁴), anclados 10/10; E3 Voronoi 240/240 y 60/60, Lloyd estable bajo un movimiento 33 % (ref. 34 %), desplazamiento ingenuo 6 % (ref. 6 %), distinguibles 6/30 (ref. 6/30), ARI = 1 en 24/30 (ref. 24/30), alcanzan E*: relax 26, lloyd+relax 24, lloyd 12, naive 5 (ref. 28/25/14/6).
- No coincide (y es informativo): el reparto de las 6 configuraciones distinguibles es 3–3 en la corrida rápida frente a 5–1 en la de referencia (m9); E4 usa otra configuración de 7 puntos en modo rápido (m8) con idéntico patrón de representabilidad en las 12 celdas (refuerza el Teorema 4.1; M5).
- Código: no encontré fugas, ajuste con datos de prueba ni errores de índice que invaliden E1–E4. Semillas correctamente fijadas; E2 comparte el orden de barrido y la escala de tolerancia entre las dos implementaciones; la relajación nunca vacía un clúster; el refill de Lloyd es coherente. E4: mínimos cuadrados exactos vía ecuaciones normales sobre ℚ, residuo nulo ⇔ pertenencia al subespacio (correcto); el rango 21 bajo w_sp corresponde a la colinealidad de A = 11ᵀ con la constante, consistente con el Lema 3.1.
- Estadística: E3 es descriptivo (recuentos sobre 30 configuraciones × 20 reinicios); no hay intervalos ni tests, y el texto no hace afirmaciones inferenciales. El recocido tiene 5 reinicios frente a 20 de los demás: no comparable en "alcanza E*", y el texto correctamente lo omite de esa comparación; decirlo en una frase.

## Recortes propuestos (15 → ≤ 10 páginas)

1. Apéndice B (Tabla 5, 1 página): eliminar; ya está en `results/tables_relaxation.md`; citar ese archivo en el Apéndice A. (−1 p.)
2. Figura 2 (1 página, mayoritariamente blanca): eliminar o reducir a una fila de tres paneles a 0.4 de página; el pie ya dice que "no evalúa". (−0.6 p.)
3. Tabla 4 (1 página): reducir a las filas "proved/classical/literature/conjectural" (9 filas) y mover las filas "verified" a una frase al final de la Sección 5; o convertirla en lista compacta. (−0.5 p.)
4. Apéndice A: fundir los cuatro párrafos "Energies/Relaxation/Stability tests/E4" en el párrafo de E1–E3 y en el Teorema 4.1 (dos frases cada uno). (−0.4 p.)
5. Sección 2: Definiciones 2.1–2.5 en prosa continua; Ejemplo 2.3 como lista en línea; Tabla 1 (datasets) en el pie de la Tabla 2. (−0.5 p.)
6. Sección 3: Corolario 3.4 y Prop. 3.5 como un solo "Remark" de cinco líneas; Observación "Rest length" dentro de la prueba de la Prop. 3.3. (−0.4 p.)
7. Figura 1: 2×3 paneles con fuentes mayores ocupa lo mismo pero se lee; mantener.
8. Introducción: fundir los dos primeros párrafos y la lista numerada (−0.3 p.). Bibliografía: con las 29 citadas y `plainnat` ocupa 2 páginas; sin cambios necesarios.
Estimación: 15 → 10–10.5 páginas sin perder contenido verificable.

## Lista de acciones (por prioridad)

1. Añade en la Introducción y el resumen que la familia de la Sección 2 es una reconstrucción de la ficha pública y condiciona la conclusión ("if the screened formulations were pairwise") (B1); confirma el supuesto con el autor antes de difundir.
2. Cambia en la ficha "Cerrada con resultado" por "Activa — borrador v0.1 en revisión interna" y acota la frase sobre muchos cuerpos (B2).
3. Reetiqueta Teorema 3.2(b) como "literature (ratio association ↔ kernel k-means, Dhillon et al. 2004, 2007)" y (e) como "classical" en la Tabla 4 y en el texto (M1).
4. Corrige 1.72 → 1.52 y "0.16+0.16" → "0.16+0.36" en la Prop. 3.7(iii) (M2).
5. Elimina de la Prop. 3.5 la frase "the resulting objective is not of the form (1)" o reemplázala por "we make no claim" (M3).
6. Reescala Φ (Φ/√2) o escribe "half the Hooke energy" en el Teorema 3.2(f), y añade "and a factor ½" en el resumen (M4).
7. Sustituye "many-body terms … are not pairwise objectives" por "the three-body, cluster-mean rest-length and per-spring energies tested" en resumen, Tabla 4, README y ficha; reporta la segunda configuración de E4 (M5).
8. Declara en E3 el cambio de línea base tras la corrida piloto y corrige "σ up to 10⁴" → "4.4×10⁴"; actualiza el docstring de `relaxation.py` (M6).
9. Coteja la Prop. 3.8 con dhillon2007/dhillon2004 y cita si el efecto ya está descrito (M7).
10. Añade "with ties broken in favour of the current cluster" en la Prop. 3.7(ii) y la frase sobre K' PSD arbitrario en la prueba (m1, m2).
11. Acota el título a la familia de resortes/pares (m3).
12. Mide `is_hartigan_stable()` en lugar de `hartigan=True` en `relaxation.py` o etiqueta "by construction" en `tables_relaxation.md` (m7).
13. Usa un generador propio para E4 o documenta que la instancia depende del estado del generador tras E1–E2 (m8).
14. Quita del README el reparto "5 a favor / 1 en contra" o indica que la corrida rápida da 3–3 (m9).
15. Aplica los recortes 1–6 para llegar a ≤ 10 páginas (M8); agranda las fuentes de la Figura 1 y elimina o reduce la Figura 2 (m12).
16. Añade números de lema/teorema de BCR en la Prop. 3.3 y la Def. 2.5 (m6); unifica "positive definite kernel"/"PSD" (m5); aclara "dataset-independent given the scales" (m4).
17. Alinea la numeración de teoremas en los docstrings (m10); elimina o cita las 4 entradas bib sin usar y las 27 macros sin usar (m11); fija la fecha (m14); resuelve las 4 cajas desbordadas (m13); precisa "no experiment on objective values" (m15).
