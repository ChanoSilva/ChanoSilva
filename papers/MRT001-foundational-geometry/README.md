# MRT001 — Foundational Geometry

**Título de trabajo:** *Foundational Geometry: Invariants Across Formalisms and Structures Preceding a Geometric Description*  
**Línea de investigación:** MRT001 — Invariantes y fundamentos geométricos (área "Matemáticas y estructuras")  
**Estado:** v0.6 (03/10/2026): tres rondas de revisión interna aplicadas; Conjetura 5.3 demostrada (ahora Teorema 5.6, con la Proposición 5.7 sobre las excepciones; la prueba usa un único resultado citado, el teorema de Gallai de 1967 sobre grafos de comparabilidad primos). Borrador de trabajo generado en una sesión de Claude Code a partir de la ficha de la línea, no de un manuscrito previo (actas en la nota de continuidad; informe y respuesta de la ronda 3 en esta carpeta).

## Qué contiene

| Ruta | Contenido |
|---|---|
| `manuscript/main.tex`, `manuscript/refs.bib` | Manuscrito en LaTeX (inglés, 26 páginas, con la prueba completa del Teorema 5.6 en el Apéndice B) y bibliografía (44 entradas). |
| `manuscript/main.pdf` | PDF compilado. |
| `manuscript/numbers.tex`, `manuscript/table_*.tex` | Macros y cuerpos de tabla **generados** desde los resultados; ningún número del texto está tipeado a mano. |
| `experiments/formalism_chain.py` | Experimentos E1–E4 y E4b (cadena euclidiana: coordenadas → métrica → orden de distancias → relaciones de Tarski). |
| `experiments/ordinal_class.py` | Experimento E2c: medición directa de la clase ordinal (radio inscrito g/4 y rango de un paseo aleatorio restringido). `--replot` regenera figura y tablas desde el JSON. |
| `experiments/lorentzian_chain.py` | Experimentos E5a–E5e (cadena lorentziana: coordenadas → orden causal → orden causal + conteo; conteo de realizadores). |
| `experiments/realizer_law.py` | Experimento E5f: comprobación en muestras independientes del Teorema 5.6 (realizadores = 2^N salvo excepciones de tasa 5/n, N → Poisson(1)). |
| `theory/` | Prueba del Teorema 5.6 tal como la entregó el agente teórico (`realizer_law_theorem.tex`, notas `realizer_law_derivation.md`, entradas `realizer_law_refs.bib`) y su comprobación numérica `check_realizer_law.py` con su salida. |
| `results/check_realizer_law_output.txt`, `.sha256` | Salida congelada de `check_realizer_law.py`; `make_numbers.py` verifica el SHA-256 antes de leerla. |
| `experiments/make_numbers.py` | Convierte `results/*.json` en `manuscript/numbers.tex` y las tablas. |
| `results/results.json`, `results/results_class.json`, `results/results_lorentz.json`, `results/results_realizer_law.json` | Resultados completos con semilla fija. |
| `results/tables*.md` | Las mismas tablas en Markdown, para lectura rápida. |
| `figures/` | Figuras en PNG y PDF. |
| `CONTINUIDAD_MRT001_20260930.md` | Nota de continuidad interna: supuestos, fuentes, decisiones, actas de las tres rondas de revisión y pendientes. |
| `REFEREE_MRT001_ronda3_20260930.md`, `RESPUESTA_MRT001_ronda3_20260930.md` | Informe de la ronda 3 y respuesta del autor punto por punto. |
| `FICHA_MRT001_propuesta.md` | Texto propuesto para la ficha del CV web. |

## Idea del paper en tres líneas

1. Se define un lenguaje mínimo: *formalismo*, *traducción* entre formalismos, *núcleo* de una traducción, *invariante a lo largo de una traducción* y *profundidad de formalismo* de una cantidad. Con eso, "la estructura X precede a la geometría Y" deja de ser una frase y pasa a ser un predicado comprobable.
2. El lenguaje se aplica por completo a la cadena euclidiana finita, donde todo se demuestra o se calcula: las primitivas de Tarski son vacías en muestras finitas genéricas (Prop. 3.2, verificada con aritmética exacta); el formalismo ordinal no determina la forma para ningún n finito (Prop. 3.4) pero la recupera asintóticamente (teorema de Kleindessner–von Luxburg, enunciado informal; medido en E2 con la advertencia de que el solver solo aproxima la clase ordinal, y en E2c midiendo la clase directamente: su radio inscrito está entre un cuarto y la mitad de la brecha mínima entre distancias consecutivas, exactamente un cuarto con pares extremos disjuntos, Prop. 3.8); las cantidades geométricas usuales se ordenan por profundidad (E4, con testigos explícitos en E4b).
3. El mismo lenguaje se aplica a la cadena lorentziana en 1+1 dimensiones: el núcleo de la traducción al orden causal contiene al grupo conforme (Prop. 5.1) y coincide con él solo cuando el orden tiene un único realizador (Prop. 5.2: clases = uniones de órbitas conformes sobre los realizadores; conteo = mitad de las orientaciones transitivas del grafo de incomparabilidad, 1 para la cadena); para muestras uniformes el realizador es único en cerca de un tercio de los casos (E5e) y se demuestra que el número de realizadores sigue asintóticamente la ley 2^{Poisson(1)}: es 2^N, con N el número de sucesiones descendentes, salvo con probabilidad 5/n + O(n⁻²), y su distancia en variación total a 2^{Po(1)} es O(1/n) (Teorema 5.6 y Proposición 5.7, demostrados aquí salvo el teorema de Gallai, citado; comprobados en E5f); el orden solo estima la dimensión (E5b), y "orden + número" recupera tiempos propios (E5c) y coordenadas (E5d). No se afirma nada físico.

## Reproducir

```bash
pip install -r experiments/requirements.txt
python3 experiments/formalism_chain.py        # ~20 min en 4 núcleos compartidos (1201 s en la corrida de referencia; --fast ~2 min)
python3 experiments/ordinal_class.py          # ~3 min (168 s); --replot solo regenera figura y tablas
python3 experiments/lorentzian_chain.py       # ~5 min (315 s)
python3 experiments/realizer_law.py           # ~2 min (128 s)
python3 theory/check_realizer_law.py          # ~1,5 min (87 s); comprueba numéricamente la prueba del Teorema 5.6
# para actualizar la salida congelada: cp theory/check_realizer_law_output.txt results/ && (cd results && sha256sum check_realizer_law_output.txt > check_realizer_law_output.sha256)
./manuscript/build.sh                          # requiere TeX Live (pdflatex, bibtex, latexmk)
```

Semilla maestra: `20260930` (E5 usa `20260931`, E2c `20260932`, E5f `20260933`). Versiones usadas en las corridas de referencia: Python 3.11, NumPy 2.4, SciPy 1.17, scikit-learn 1.9.
