# LMI001 — Mechanical Clustering

**Título de trabajo:** *Spring-Energy Clustering Is Kernel Clustering: An Equivalence Theorem Behind a Null Screening*  
**Línea de investigación:** LMI001 — Analogías mecánicas para agrupamiento de datos / Mechanical analogies for data clustering (área "Inteligencia artificial y aprendizaje")  
**Estado:** borrador de trabajo **v0.2 (03/10/2026), una ronda de revisión interna aplicada**. La v0.1 (30/09/2026) se generó en una sesión de Claude Code a partir de la ficha pública de la línea (no existe manuscrito ni código previo: la familia "mecánica" de la Sección 2 es una **reconstrucción** de la ficha, pendiente de confirmación por el autor); la ronda 1 de arbitraje interno independiente está en `REFEREE_LMI001_ronda1_20260930.md` y la respuesta punto por punto en `RESPUESTA_LMI001_ronda1_20260930.md`.

## Qué contiene

| Ruta | Contenido |
|---|---|
| `manuscript/main.tex`, `manuscript/refs.bib` | Manuscrito en LaTeX (inglés, 13 páginas con apéndice y bibliografía) y 31 referencias, todas citadas. |
| `manuscript/main.pdf` | PDF compilado (pdflatex + bibtex vía latexmk; 0 errores, 0 referencias indefinidas, 0 cajas desbordadas). |
| `manuscript/numbers.tex`, `manuscript/table_*.tex` | Macros y cuerpos de tabla **generados** desde los resultados; ningún número del texto está tipeado a mano. |
| `experiments/mechanical.py` | Biblioteca: potenciales (resortes), energías elásticas, forma de traza del objetivo de kernel k-means, optimizadores (Lloyd en espacio de características, relajación partícula a partícula = método de Hartigan, recocido Metropolis) e implementación "física" por fuerza bruta de la relajación. |
| `experiments/identity_check.py` | E1 (identidad energía elástica = objetivo kernel), E2 (misma trayectoria de la implementación física y la kernel; resortes anclados = Lloyd de scikit-learn), E4 (no representabilidad en aritmética racional exacta, dos configuraciones con generador propio). |
| `experiments/relaxation.py` | E3 (relajación de resortes frente a optimizadores de kernel k-means sobre la misma energía). |
| `experiments/make_figures.py`, `experiments/make_numbers.py` | Figuras y conversión de `results/*.json` en macros LaTeX. |
| `results/results_identity.json`, `results/results_relaxation.json` | Resultados completos con semilla fija; `results/tables_*.md` son las mismas tablas en Markdown (incluida la tabla E3 por configuración, que ya no está en el manuscrito). |
| `figures/` | `energies.{png,pdf}` (Figura 1: exceso relativo de energía por optimizador), `partitions.{png,pdf}` (mejores particiones en los conjuntos sintéticos; ilustrativa, fuera del manuscrito desde v0.2). |
| `CONTINUIDAD_LMI001_20260930.md` | Nota interna: supuestos reconstruidos, decisiones, resultados de referencia, limitaciones, pendientes, y la sección de la ronda 1. |
| `FICHA_LMI001_propuesta.md` | Texto propuesto para actualizar la ficha de la línea en el CV web (condicionado a confirmar el supuesto de reconstrucción). |
| `REFEREE_LMI001_ronda1_20260930.md`, `RESPUESTA_LMI001_ronda1_20260930.md` | Informe de árbitro interno y respuesta del autor (ronda 1). |

## Idea del paper en tres líneas

1. Se define con precisión una familia "mecánica" **de pares**, reconstruida de la ficha: puntos unidos por resortes con un potencial de pares arbitrario φ(d), opcionalmente tras un levantamiento L: R^d → R^D, con la energía intra-clúster normalizada por partícula (1/n_c) o sumada; más las variantes de tensión (energía liberada al cortar los resortes entre clústeres) y de resortes anclados a un hub.
2. Se demuestra que toda esa familia es agrupamiento por kernels: resortes de Hooke sin longitud de reposo = k-means exacto (clásico); para cualquier φ la energía por partícula es ½ del objetivo de kernel k-means de la matriz −φ(D) más una constante, y un desplazamiento diagonal la hace semidefinida positiva sin cambiar los minimizadores (es la forma "ratio association" del kernel k-means de Dhillon–Guan–Kulis, escrita para matrices de resortes); si φ(d) = ψ(d²) con ψ función de Bernstein, el teorema de Schoenberg da un kernel definido positivo independiente del conjunto de datos (dadas las escalas), de modo que el resorte es, salvo una constante y un reescalado 1/√2 del mapa de características, un resorte de Hooke sobre una configuración levantada; el levantamiento solo cambia el kernel; la energía total y su dual de tensión son min-sum k-clustering / max-k-cut; y la relajación a temperatura cero del sistema de resortes es el método de Hartigan, cuyos puntos fijos son siempre puntos fijos de Lloyd del problema kernel (Prop. 3.5), mientras que la regla de Lloyd depende del representante PSD (Prop. 3.6).
3. Se certifica con aritmética racional exacta, en dos configuraciones explícitas, que el término de tres cuerpos (área de triángulo), la longitud de reposo adaptativa (media del clúster) y la normalización por resorte ensayados no son objetivos de pares (Teorema 4.1; no se afirma nada sobre las clases "muchos cuerpos" en general), y se formula como problema abierto, no como experimento, la única vía no cerrada: la dinámica sobre posiciones (tipo gravitacional / mean shift). **Lectura para la línea:** *si* las formulaciones cribadas eran de pares, el cribado nulo no fue un experimento fallido sino una consecuencia de la equivalencia; la confirmación de ese supuesto con el autor está pendiente.

## Resultados de la corrida de referencia v0.2 (semillas 20260930, 20260931 y 20260932)

- **E1 (identidad de valores).** En 5 conjuntos × 6 potenciales y 6090 particiones, la energía elástica por partícula coincide con ½·J_K + constante para las tres representaciones del kernel (−φ(D), −φ(D)+σI con σ hasta 4.4×10⁴, y el kernel universal de Schoenberg) en 19 285/19 285 comprobaciones, error relativo máximo 1.1×10⁻¹¹; la energía de Hooke iguala la SSE de k-means a 3.9×10⁻¹⁶. El kernel universal es PSD en los 25/25 casos de tipo negativo y es indefinido en 5/5 casos con longitud de reposo. El cociente energía total / energía por partícula varía en [29.7, 197.5] sobre particiones aleatorias: la normalización es una elección real.
- **E2 (mismo optimizador, misma trayectoria).** Una relajación de resortes por fuerza bruta (solo suma energías de resortes) y la implementación kernel del método de Hartigan, desde las mismas etiquetas y el mismo orden de barrido, producen trayectorias idénticas en 90/90 corridas (energía final igual a 1.4×10⁻¹⁴), en 56 s frente a 0.6 s. Los resortes de Hooke anclados y equilibrados alternadamente reproducen `KMeans(algorithm='lloyd')` de scikit-learn en 15/15 corridas (inercia = energía elástica a 4.3×10⁻¹⁶).
- **E3 (relajación frente a kernel k-means).** Los 600/600 puntos fijos de la relajación y los 150/150 del recocido son estables de Voronoi (puntos fijos de Lloyd) en el espacio de características, como predice la Proposición 3.5. Sobre la misma energía, la relajación alcanza la mejor energía encontrada en 28/30 configuraciones, Lloyd+pulido en 25/30, Lloyd solo en 14/30 y Lloyd sobre el kernel desplazado ingenuamente en 6/30; solo 34 % de los puntos fijos de Lloyd son estables bajo movimientos individuales (6 % con el desplazamiento ingenuo), lo que confirma que la regla de Lloyd depende de la representación (Prop. 3.6) mientras que la energía no. En 6/30 configuraciones las mejores energías de relajación y Lloyd+pulido difieren (diferencia máxima 7.4×10⁻³; el sentido de la diferencia es ruido de optimizador: la corrida rápida da 3–3): un efecto de optimizador, no del componente mecánico. La línea base de Lloyd (kernel canónico K̃) sustituyó a −φ(D)+σI tras una corrida piloto; el manuscrito lo declara.
- **E4 (separación exacta).** Sobre dos configuraciones de 7 puntos enteros (generador propio, semilla 20260932) y 63 particiones en 2 bloques, con mínimos cuadrados en `Fraction`: Hooke por partícula, Hooke total y resorte con longitud de reposo fija son representables bajo su propia normalización (residuo 0 en ambas); la normalización cruzada, la longitud de reposo adaptativa (residuos relativos 0.143/0.109 y 0.157/0.122), el término de tres cuerpos (0.331/0.039 y 0.328/0.037) y la media por resorte (0.185/0.125 y 0.180/0.121) no lo son; el patrón sí/no coincide en las 12 celdas.
- **Cómputo** de la corrida de referencia v0.2: 159 s (E1, E2, E4) y 128 s (E3), en paralelo sobre núcleos compartidos; unos 6–7 minutos de CPU en la ronda incluyendo la prueba rápida, las figuras y las compilaciones.

## Reproducir

```bash
pip install -r experiments/requirements.txt
python3 experiments/identity_check.py     # E1, E2, E4: ~2.5 min (--fast: ~20 s)
python3 experiments/relaxation.py         # E3: ~1-2 min (--fast: ~15 s)
python3 experiments/make_figures.py
./manuscript/build.sh                      # requiere TeX Live (pdflatex, bibtex, latexmk)
```

Semillas: `20260930` (E1, E2), `20260931` (E3) y `20260932` (E4, generador propio). Versiones usadas: Python 3.11.15, NumPy 2.4.6, SciPy 1.17.1, scikit-learn 1.9.1, Matplotlib 3.11.2.
