# MRT001 — Foundational Geometry

**Título de trabajo:** *Foundational Geometry: Invariants Across Formalisms and Structures Preceding a Geometric Description*  
**Línea de investigación:** MRT001 — Invariantes y fundamentos geométricos (área "Matemáticas y estructuras")  
**Estado:** v0.8 (03/10/2026): cinco rondas de revisión interna aplicadas. Ley de realizadores demostrada (Teorema 5.6 y Proposición 5.7, verificados por el árbitro de la ronda 4; la prueba es autocontenida salvo el teorema de Gallai de 1967 sobre grafos de comparabilidad primos, y los lemas combinatorios que usa son conocidos y se reprueban). **Tasas exactas de primer orden** (Teoremas 5.8 y 5.9, Proposición 5.10 y Lema B.2: d_TV(N_n, Po(1)) = e⁻¹/n salvo 2/(n·n!), d_TV(R_n, 2^Z) = (1 + 1/(2e))/n + O(n⁻²)): demostradas aquí y **comprobadas por un árbitro interno independiente (ronda 5)**; el Teorema 5.8 es una consecuencia elemental de la ley exacta clásica de Kaplansky. En v0.8 se añadió el **segundo orden** (Teoremas 5.11–5.12, Proposición 5.13: n²·d_TV(N_n, Po(1 − 1/n)) → 3/(4e), la mejor Poisson tiene constante 1/(2e), |d_TV(R_n, 2^Z) − c₂/n| ≤ 422/n² para n ≥ 22), demostrado por el autor y comprobado numéricamente, **aún sin arbitraje independiente**; el término n⁻² de la ley de R_n (κ ≈ 4.29707) es solo numérico y su forma cerrada 7/2 + 13/(6e) es una **conjetura**. Borrador de trabajo generado en sesiones de Claude Code a partir de la ficha de la línea, no de un manuscrito previo (actas en la nota de continuidad; informes y respuestas de las rondas 3, 4 y 5 en esta carpeta).

## Qué contiene

| Ruta | Contenido |
|---|---|
| `manuscript/main.tex`, `manuscript/refs.bib` | Manuscrito en LaTeX (inglés, 33 páginas, con las pruebas completas de la Sección 5 en el Apéndice B) y bibliografía (47 entradas). |
| `manuscript/main.pdf` | PDF compilado. |
| `manuscript/numbers.tex`, `manuscript/table_*.tex` | Macros y cuerpos de tabla **generados** desde los resultados; ningún número del texto está tipeado a mano. |
| `experiments/formalism_chain.py` | Experimentos E1–E4 y E4b (cadena euclidiana: coordenadas → métrica → orden de distancias → relaciones de Tarski). |
| `experiments/ordinal_class.py` | Experimento E2c: medición directa de la clase ordinal (radio inscrito g/4 y rango de un paseo aleatorio restringido). `--replot` regenera figura y tablas desde el JSON. |
| `experiments/lorentzian_chain.py` | Experimentos E5a–E5e (cadena lorentziana: coordenadas → orden causal → orden causal + conteo; conteo de realizadores). |
| `experiments/realizer_law.py` | Experimento E5f: comprobación en muestras independientes del Teorema 5.6 (realizadores = 2^N salvo excepciones de tasa 5/n, N → Poisson(1)). |
| `theory/` | Material del agente teórico: prueba del Teorema 5.6 (`realizer_law_theorem.tex`, `realizer_law_derivation.md`, `realizer_law_refs.bib`, `check_realizer_law.py`) tasas exactas (`sharp_rate.tex`, `sharp_rate_derivation.md`, `check_sharp_rate.py`) y segundo orden (`second_order.tex`, `second_order_derivation.md`, `check_second_order.py`, `second_order_results.json`). Las versiones integradas (corregidas) están en el manuscrito; los `*_output.txt` de `theory/` son registros con tiempos, **no** las salidas de referencia. |
| `results/check_realizer_law_output.txt`, `.sha256` | Salida de referencia (congelada) de `check_realizer_law.py`; `make_numbers.py` verifica el SHA-256 antes de leerla. La copia de `theory/` difiere solo en los tiempos. |
| `results/check_sharp_rate_output.txt`, `.sha256`, `check_sharp_rate_meta.json` | Salida de referencia de `check_sharp_rate.py`, escrita sin líneas de tiempo para que su SHA-256 sea reproducible; el tiempo de la corrida va en el `meta.json`. `make_numbers.py` verifica el SHA-256 y genera de ella todos los números del Apéndice B sobre las tasas exactas. |
| `results/check_second_order_output.txt`, `.sha256`, `second_order_results.json`, `check_second_order_meta.json` | Salida de referencia de `check_second_order.py` (determinista) sin líneas de tiempo y su JSON sin el tiempo de CPU, escritos por `experiments/freeze_second_order.py` (que no modifica `theory/`); `make_numbers.py` verifica ambos SHA-256 y genera de ellos todos los números del segundo orden y la columna "exact" de la Tabla 11. |
| `experiments/make_numbers.py` | Convierte `results/*.json` en `manuscript/numbers.tex` y las tablas. |
| `results/results.json`, `results/results_class.json`, `results/results_lorentz.json`, `results/results_realizer_law.json` | Resultados completos con semilla fija. |
| `results/tables*.md` | Las mismas tablas en Markdown, para lectura rápida. |
| `figures/` | Figuras en PNG y PDF. |
| `CONTINUIDAD_MRT001_20260930.md` | Nota de continuidad interna: supuestos, fuentes, decisiones, actas de las tres rondas de revisión y pendientes. |
| `REFEREE_MRT001_ronda3_20260930.md`, `RESPUESTA_MRT001_ronda3_20260930.md` | Informe de la ronda 3 y respuesta del autor punto por punto. |
| `REFEREE_MRT001_ronda4_20261003.md`, `RESPUESTA_MRT001_ronda4_20261003.md` | Informe de la ronda 4 y respuesta del autor, con la verificación propia de las tasas exactas antes de integrarlas. |
| `REFEREE_MRT001_ronda5_20261003.md`, `RESPUESTA_MRT001_ronda5_20261003.md` | Informe de la ronda 5 (arbitraje de las tasas exactas) y respuesta del autor, con la verificación independiente del segundo orden antes de integrarlo. |
| `FICHA_MRT001_propuesta.md` | Texto propuesto para la ficha del CV web. |

## Idea del paper en tres líneas

1. Se define un lenguaje mínimo: *formalismo*, *traducción* entre formalismos, *núcleo* de una traducción, *invariante a lo largo de una traducción* y *profundidad de formalismo* de una cantidad. Con eso, "la estructura X precede a la geometría Y" deja de ser una frase y pasa a ser un predicado comprobable.
2. El lenguaje se aplica por completo a la cadena euclidiana finita, donde todo se demuestra o se calcula: las primitivas de Tarski son vacías en muestras finitas genéricas (Prop. 3.2, verificada con aritmética exacta); el formalismo ordinal no determina la forma para ningún n finito (Prop. 3.4) pero la recupera asintóticamente (teorema de Kleindessner–von Luxburg, enunciado informal; medido en E2 con la advertencia de que el solver solo aproxima la clase ordinal, y en E2c midiendo la clase directamente: su radio inscrito está entre un cuarto y la mitad de la brecha mínima entre distancias consecutivas, exactamente un cuarto con pares extremos disjuntos, Prop. 3.8); las cantidades geométricas usuales se ordenan por profundidad (E4, con testigos explícitos en E4b).
3. El mismo lenguaje se aplica a la cadena lorentziana en 1+1 dimensiones: el núcleo de la traducción al orden causal contiene al grupo conforme (Prop. 5.1) y coincide con él solo cuando el orden tiene un único realizador (Prop. 5.2: clases = uniones de órbitas conformes sobre los realizadores; conteo = mitad de las orientaciones transitivas del grafo de incomparabilidad, 1 para la cadena); para muestras uniformes el realizador es único con probabilidad que tiende a e⁻¹ ≈ 0,37 (0,34 observado en n = 300, E5e) y se demuestra que el número de realizadores sigue asintóticamente la ley 2^{Poisson(1)}: es 2^N, con N el número de sucesiones descendentes, salvo con probabilidad 5/n + O(n⁻²), (Teorema 5.6 y Proposición 5.7, demostrados aquí salvo el teorema de Gallai, citado; comprobados en E5f); su distancia en variación total a 2^{Po(1)} es (1 + 1/(2e))/n + O(n⁻²) (Teorema 5.9, comprobado por el árbitro interno de la ronda 5), con resto ≤ 422/n² para n ≥ 22 (Proposición 5.13, nueva en v0.8, sin arbitraje todavía); el orden solo estima la dimensión (E5b), y "orden + número" recupera tiempos propios (E5c) y coordenadas (E5d). No se afirma nada físico.

## Reproducir

```bash
pip install -r experiments/requirements.txt
python3 experiments/formalism_chain.py        # ~20 min en 4 núcleos compartidos (1201 s en la corrida de referencia; --fast ~2 min)
python3 experiments/ordinal_class.py          # ~3 min (168 s); --replot solo regenera figura y tablas
python3 experiments/lorentzian_chain.py       # ~5 min (315 s)
python3 experiments/realizer_law.py           # ~2 min (128 s)
python3 theory/check_realizer_law.py          # ~1,5 min (87 s); comprueba numéricamente la prueba del Teorema 5.6
# para actualizar su salida congelada: cp theory/check_realizer_law_output.txt results/ && (cd results && sha256sum check_realizer_law_output.txt > check_realizer_law_output.sha256)
python3 theory/check_sharp_rate.py            # ~2 min (116 s, un núcleo); comprueba las tasas exactas (Teoremas 5.8-5.9, Prop. 5.10)
#   escribe por sí mismo results/check_sharp_rate_output.txt (sin tiempos), su .sha256 y check_sharp_rate_meta.json
python3 experiments/freeze_second_order.py --run   # ~1 min (51 s, un núcleo, determinista); corre theory/check_second_order.py
#   en una copia temporal (no toca theory/) y escribe results/check_second_order_output.txt (sin tiempos), su .sha256,
#   results/second_order_results.json y check_second_order_meta.json; requiere mpmath
./manuscript/build.sh                          # requiere TeX Live (pdflatex, bibtex, latexmk)
```

Semilla maestra: `20260930` (E5 usa `20260931`, E2c `20260932`, E5f `20260933`; las comprobaciones de `theory/` usan `20261003` y `20261004`; `check_second_order.py` no usa números aleatorios). Versiones usadas en las corridas de referencia: Python 3.11, NumPy 2.4, SciPy 1.17, scikit-learn 1.9.
