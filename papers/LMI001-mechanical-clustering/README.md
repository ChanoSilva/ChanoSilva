# LMI001 — Mechanical Clustering

**Título de trabajo:** *Mechanical Analogies for Data Clustering Are Kernel Clustering: An Equivalence Theorem Behind a Null Screening*  
**Línea de investigación:** LMI001 — Analogías mecánicas para agrupamiento de datos / Mechanical analogies for data clustering (área "Inteligencia artificial y aprendizaje")  
**Estado:** borrador de trabajo v0.1 (30/09/2026), generado en una sesión de Claude Code a partir de la ficha pública de la línea (no existe manuscrito previo), con una relectura arbitral interna por el mismo agente (véase la nota de continuidad).

## Qué contiene

| Ruta | Contenido |
|---|---|
| `manuscript/main.tex`, `manuscript/refs.bib` | Manuscrito en LaTeX (inglés, 14 páginas con apéndices y bibliografía) y 29 referencias. |
| `manuscript/main.pdf` | PDF compilado (pdflatex + bibtex vía latexmk; sin referencias indefinidas). |
| `manuscript/numbers.tex`, `manuscript/table_*.tex` | Macros y cuerpos de tabla **generados** desde los resultados; ningún número del texto está tipeado a mano. |
| `experiments/mechanical.py` | Biblioteca: potenciales (resortes), energías elásticas, forma de traza del objetivo de kernel k-means, optimizadores (Lloyd en espacio de características, relajación partícula a partícula = método de Hartigan, recocido Metropolis) e implementación "física" por fuerza bruta de la relajación. |
| `experiments/identity_check.py` | E1 (identidad energía elástica = objetivo kernel), E2 (misma trayectoria de la implementación física y la kernel; resortes anclados = Lloyd de scikit-learn), E4 (no representabilidad en aritmética racional exacta). |
| `experiments/relaxation.py` | E3 (relajación de resortes frente a optimizadores de kernel k-means sobre la misma energía). |
| `experiments/make_figures.py`, `experiments/make_numbers.py` | Figuras y conversión de `results/*.json` en macros LaTeX. |
| `results/results_identity.json`, `results/results_relaxation.json` | Resultados completos con semilla fija; `results/tables_*.md` son las mismas tablas en Markdown. |
| `figures/` | `energies.{png,pdf}` (exceso relativo de energía por optimizador), `partitions.{png,pdf}` (mejores particiones en los conjuntos sintéticos). |
| `CONTINUIDAD_LMI001_20260930.md` | Nota interna: supuestos reconstruidos de la ficha, decisiones, resultados de referencia, limitaciones, pendientes. |
| `FICHA_LMI001_propuesta.md` | Texto propuesto para actualizar la ficha de la línea en el CV web. |

## Idea del paper en tres líneas

1. Se define con precisión la familia "mecánica": puntos unidos por resortes con un potencial de pares arbitrario φ(d), opcionalmente tras un levantamiento L: R^d → R^D, con la energía intra-clúster normalizada por partícula (1/n_c) o sumada; más las variantes de tensión (energía liberada al cortar los resortes entre clústeres) y de resortes anclados a un hub.
2. Se demuestra que toda esa familia es agrupamiento por kernels: resortes de Hooke sin longitud de reposo = k-means exacto (identidad clásica); para cualquier φ la energía por partícula es ½ del objetivo de kernel k-means de la matriz −φ(D) más una constante, y un desplazamiento diagonal la hace semidefinida positiva sin cambiar los minimizadores; si φ(d) = ψ(d²) con ψ función de Bernstein, el teorema de Schoenberg da un kernel definido positivo independiente del conjunto de datos, de modo que el resorte es literalmente un resorte de Hooke sobre una configuración levantada; el levantamiento solo cambia el kernel; la energía total y su dual de tensión son min-sum k-clustering / max-k-cut; y la relajación a temperatura cero del sistema de resortes es el método de Hartigan, cuyos puntos fijos son siempre puntos fijos de Lloyd del problema kernel.
3. Se certifica con aritmética racional exacta qué ingredientes salen de la familia (términos de muchos cuerpos, longitudes de reposo dependientes de la asignación, normalización por resorte) y se formula como problema abierto, no como experimento, la única vía no cerrada: la dinámica sobre posiciones (tipo gravitacional / mean shift). Conclusión para la línea: el cribado nulo no fue un experimento fallido sino una consecuencia de la equivalencia.

## Resultados de la corrida de referencia (semillas 20260930 y 20260931)

- **E1 (identidad de valores).** En 5 conjuntos × 6 potenciales y 6090 particiones, la energía elástica por partícula coincide con ½·J_K + constante para las tres representaciones del kernel (−φ(D), −φ(D)+σI, y el kernel universal de Schoenberg) en 19 285/19 285 comprobaciones, error relativo máximo 1.1×10⁻¹¹; la energía de Hooke iguala la SSE de k-means a 3.8×10⁻¹⁶. El kernel universal es PSD en los 25/25 casos de tipo negativo y es indefinido en 5/5 casos con longitud de reposo. El cociente energía total / energía por partícula varía en [29.7, 205.3] sobre particiones aleatorias: la normalización es una elección real.
- **E2 (mismo optimizador, misma trayectoria).** Una relajación de resortes por fuerza bruta (solo suma energías de resortes) y la implementación kernel del método de Hartigan, desde las mismas etiquetas y el mismo orden de barrido, producen trayectorias idénticas en 90/90 corridas (energía final igual a 2.7×10⁻¹⁴), en 86 s frente a 0.7 s. Los resortes de Hooke anclados y equilibrados alternadamente reproducen `KMeans(algorithm='lloyd')` de scikit-learn en 15/15 corridas (inercia = energía elástica a 4.3×10⁻¹⁶).
- **E3 (relajación frente a kernel k-means).** Los 600/600 puntos fijos de la relajación y los 150/150 del recocido son estables de Voronoi (puntos fijos de Lloyd) en el espacio de características, como predice la Proposición 3.7. Sobre la misma energía, la relajación alcanza la mejor energía encontrada en 28/30 configuraciones, Lloyd+pulido en 25/30, Lloyd solo en 14/30 y Lloyd sobre el kernel desplazado ingenuamente en 6/30; solo 34 % de los puntos fijos de Lloyd son estables bajo movimientos individuales (6 % con el desplazamiento ingenuo), lo que confirma que la regla de Lloyd depende de la representación (Prop. 3.8) mientras que la energía no. En 6/30 configuraciones las mejores energías de relajación y Lloyd+pulido difieren (5 a favor de la relajación, 1 en contra; diferencia máxima 7.4×10⁻³): un efecto de optimizador, no del componente mecánico.
- **E4 (separación exacta).** Sobre 7 puntos enteros y 63 particiones en 2 bloques, con mínimos cuadrados en `Fraction`: Hooke por partícula, Hooke total y resorte con longitud de reposo fija son representables bajo su propia normalización (residuo 0); la normalización cruzada, la longitud de reposo adaptativa (residuos relativos 0.181 / 0.110), el término de tres cuerpos (0.327 / 0.056) y la media por resorte (0.203 / 0.148) no lo son.
- **Cómputo total** de la corrida de referencia: 150 s (E1, E2, E4) + 68 s (E3) en núcleos compartidos; unos 6 minutos incluyendo las corridas rápidas de prueba y las figuras.

## Reproducir

```bash
pip install -r experiments/requirements.txt
python3 experiments/identity_check.py     # E1, E2, E4: ~2.5 min (--fast: ~45 s)
python3 experiments/relaxation.py         # E3: ~1 min (--fast: ~15 s)
python3 experiments/make_figures.py
./manuscript/build.sh                      # requiere TeX Live (pdflatex, bibtex, latexmk)
```

Semillas: `20260930` (E1, E2, E4) y `20260931` (E3). Versiones usadas: Python 3.11.15, NumPy 2.4.6, SciPy 1.17.1, scikit-learn 1.9.1, Matplotlib 3.11.2.
