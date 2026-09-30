# MRT001 — Foundational Geometry

**Título de trabajo:** *Foundational Geometry: Invariants Across Formalisms and Structures Preceding a Geometric Description*  
**Línea de investigación:** MRT001 — Invariantes y fundamentos geométricos (área "Matemáticas y estructuras")  
**Estado:** borrador de trabajo v0.2 (30/09/2026), generado en una sesión de Claude Code a partir de la ficha de la línea, no de un manuscrito previo, y revisado una vez por un árbitro interno independiente (véase la nota de continuidad).

## Qué contiene

| Ruta | Contenido |
|---|---|
| `manuscript/main.tex`, `manuscript/refs.bib` | Manuscrito en LaTeX (inglés) y bibliografía. |
| `manuscript/main.pdf` | PDF compilado. |
| `manuscript/numbers.tex`, `manuscript/table_*.tex` | Macros y cuerpos de tabla **generados** desde los resultados; ningún número del texto está tipeado a mano. |
| `experiments/formalism_chain.py` | Experimentos E1–E4 y E4b (cadena euclidiana: coordenadas → métrica → orden de distancias → relaciones de Tarski). |
| `experiments/ordinal_class.py` | Experimento E2c: medición directa de la clase ordinal (radio inscrito g/4 y paseo aleatorio restringido). |
| `experiments/lorentzian_chain.py` | Experimentos E5 (cadena lorentziana: coordenadas → orden causal → orden causal + conteo). |
| `experiments/make_numbers.py` | Convierte `results/*.json` en `manuscript/numbers.tex` y las tablas. |
| `results/results.json`, `results/results_class.json`, `results/results_lorentz.json` | Resultados completos con semilla fija. |
| `results/tables.md`, `results/tables_class.md`, `results/tables_lorentz.md` | Las mismas tablas en Markdown, para lectura rápida. |
| `figures/` | Figuras en PNG y PDF. |
| `CONTINUIDAD_MRT001_20260930.md` | Nota de continuidad interna: supuestos, fuentes, decisiones y pendientes. |

## Idea del paper en tres líneas

1. Se define un lenguaje mínimo: *formalismo*, *traducción* entre formalismos, *núcleo* de una traducción, *invariante a lo largo de una traducción* y *profundidad de formalismo* de una cantidad. Con eso, "la estructura X precede a la geometría Y" deja de ser una frase y pasa a ser un predicado comprobable.
2. El lenguaje se aplica por completo a la cadena euclidiana finita, donde todo se demuestra o se calcula: las primitivas de Tarski son vacías en muestras finitas genéricas (Prop. 3.2, verificada con aritmética exacta); el formalismo ordinal no determina la forma para ningún n finito (Prop. 3.4) pero la recupera asintóticamente (teorema de Kleindessner–von Luxburg, medido en E2 con la advertencia de que el solver solo aproxima la clase ordinal, y en E2c midiendo la clase directamente: su radio inscrito es un cuarto de la brecha mínima entre distancias consecutivas, Prop. 3.8); las cantidades geométricas usuales se ordenan por profundidad (E4, con testigos explícitos en E4b).
3. El mismo lenguaje se aplica a la cadena lorentziana en 1+1 dimensiones: el núcleo de la traducción al orden causal contiene al grupo conforme (Prop. 5.1) y es estrictamente mayor a n finito (Prop. 5.2: uniones de órbitas conformes sobre los realizadores del orden), el orden solo ya estima la dimensión (E5b), y "orden + número" recupera tiempos propios (E5c) y coordenadas (E5d). No se afirma nada físico.

## Reproducir

```bash
pip install -r experiments/requirements.txt
python3 experiments/formalism_chain.py        # ~11 min en 4 núcleos (usar --fast para ~2 min)
python3 experiments/ordinal_class.py          # ~5 min
python3 experiments/lorentzian_chain.py       # < 1 min
./manuscript/build.sh                          # requiere TeX Live (pdflatex, bibtex, latexmk)
```

Semilla maestra: `20260930` (E5 usa `20260931`). Versiones usadas en la corrida de referencia: Python 3.11, NumPy 2.4, SciPy 1.17, scikit-learn 1.9.
