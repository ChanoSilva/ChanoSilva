# SVMF001 — Boundary Families

**Título de trabajo:** *Families of Classification Boundaries: Locally Adaptive Support Vector Machines Against Matched Global References, with an Exact Statement of When Local Adaptation Cannot Help*  
**Línea de investigación:** SVMF001 — Familias de fronteras de clasificación (área "Inteligencia artificial y aprendizaje")  
**Estado:** borrador de trabajo v0.1 (30/09/2026), generado en una sesión de Claude Code a partir de la ficha pública de la línea. Las variantes originales de la línea no están disponibles; todo lo que hay aquí es una **reconstrucción autocontenida** y se declara como tal (véase la nota de continuidad).

## Qué contiene

| Ruta | Contenido |
|---|---|
| `manuscript/main.tex`, `manuscript/refs.bib` | Manuscrito en LaTeX (inglés) y bibliografía (26 entradas reales, todas citadas). |
| `manuscript/main.pdf` | PDF compilado con pdflatex/bibtex (sin errores ni referencias indefinidas). |
| `manuscript/numbers.tex`, `manuscript/table_*.tex` | Macros y cuerpos de tabla **generados** desde `results/*.json`; ningún número del texto está tipeado a mano. |
| `experiments/families.py` | Las seis familias en ~300 líneas: SVM lineal y RBF-SVM (referencias); kNN-SVM (SVM lineal local por punto de prueba), cell-SVM (partición dura por k-means), VB-RBF-SVM (núcleo RBF de ancho de banda variable, definido positivo) y LLSVM (mezcla suave de SVM lineales locales). Cada familia local contiene una referencia global como caso particular de su propia rejilla. |
| `experiments/run_comparison.py` | Protocolo completo: 6 conjuntos de datos, condición principal (2×5 pliegues) y dos condiciones de robustez (ruido de etiquetas 20 %, submuestreo 25 %), CV interna de 3 pliegues, diferencias pareadas frente a la mejor referencia global, IC bootstrap 95 %, criterio predefinido. Escribe `results/results.json`, `results/tables.md` y `figures/fig_paired.*`. |
| `experiments/exact_example.py` | Sección teórica: curva de aprendizaje exacta del umbral de centroides en el modelo gaussiano, riesgo exacto de la versión localizada por partición, chequeo Monte Carlo y simulaciones D1–D4 (versiones kNN y curva de aprendizaje de la SVM lineal). Escribe `results/exact_example.*` y `figures/fig_exact.*`. |
| `experiments/posthoc_oracle.py` | Chequeo **post hoc** (definido tras ver los resultados): diferencias frente a la referencia global "oráculo" (la mejor de las dos en cada pliegue de prueba). Solo lee `results.json`. |
| `experiments/make_region_figure.py`, `experiments/make_numbers.py` | Figura de regiones de decisión y generación de macros/tablas. |
| `results/` | Resultados completos con semilla fija (`results.json`, `exact_example.json`, `posthoc_oracle.json`) y sus versiones Markdown. |
| `figures/` | Figuras en PNG y PDF. |
| `CONTINUIDAD_SVMF001_20260930.md` | Nota de continuidad interna: supuestos, decisiones, limitaciones, pendientes. |

## Idea del paper en tres líneas

1. **Enunciado exacto de cuándo la adaptación local no puede ayudar.** Si la clase de la referencia ya contiene la regla de Bayes, la localización solo puede actuar sobre el error de estimación (Lema 3.1, trivial). Para modelos locales ajustados en celdas elegidas **independientemente de las etiquetas**, el riesgo esperado de la regla localizada es la curva de aprendizaje de la referencia promediada en tamaños binomialmente reducidos: nunca menor si la curva es no creciente, estrictamente mayor si es estrictamente decreciente (Prop. 3.3, demostrada). En el modelo gaussiano con umbral de centroides todo es cerrado: con n = 320 y 4 celdas el exceso de riesgo se multiplica por 4.08 (Prop. 3.4 y Cor. 3.5, sumas finitas exactas; Monte Carlo coincide). La localización por vecinos (kNN-SVM) **no** está cubierta por la proposición; solo se ilustra.
2. **Comparación controlada con criterio fijado antes de correr:** mejora pareada sobre la mejor referencia global (elegida por CV interna, sin usar datos de prueba) con IC bootstrap 95 % que excluya 0 en la mayoría de 6 conjuntos (wine, breast cancer, digits par/impar; gaussiano lineal en d = 10; lunas y tablero de ajedrez a dos escalas y dos densidades), o bien en todos los conjuntos de un régimen nombrado sin pérdidas significativas fuera de él. Robustez: exactitud bajo 20 % de ruido en etiquetas de entrenamiento y con 25 % del conjunto de entrenamiento.
3. **Resultado:** ninguna familia cumple el criterio de mayoría. De 24 celdas conjunto×familia, 8 intervalos quedan por debajo de 0 y 1 por encima (VB-RBF-SVM en el gaussiano lineal, +0.75 pp), que es justamente el conjunto donde la teoría dice que no hay ganancia posible: la ganancia es frente a la referencia *seleccionada* (la CV interna eligió RBF cuando la lineal era mejor) y desaparece frente a la mejor de las dos referencias (−0.37 [−1.25, +0.25]). En el régimen multiescala, diseñado para favorecer la adaptación local, VB-RBF-SVM empata con la RBF-SVM. Las tres familias lineales locales pierden entre 10 y 18 pp en los conjuntos multiescala. Nadie es más robusto que la referencia; kNN-SVM es menos robusto. Se reproduce, con protocolo explícito, el hallazgo de la ficha: las mejoras dependen del régimen y el valor añadido exigido no se sostiene. No se afirma superioridad general de ninguna familia.

## Resultados de referencia (semilla 20260930)

- Condición principal, exactitud media (%) de la mejor referencia global / VB-RBF-SVM / kNN-SVM / cell-SVM / LLSVM: wine 99.7 / 99.7 / 99.4 / 98.9 / 99.2; breast cancer 96.5 / 96.2 / 96.3 / 96.2 / 96.2; digits 97.5 / 97.6 / 96.6 / 94.1 / 93.4; gaussiano lineal 93.1 / 93.9 / 92.0 / 93.0 / 93.5; lunas 2 escalas 97.5 / 96.9 / 86.9 / 86.1 / 85.5; tablero 2 escalas 87.0 / 87.0 / 73.9 / 68.8 / 69.3.
- Diferencias pareadas significativas (IC 95 % excluye 0) en la condición principal: negativas para cell-SVM y LLSVM en digits, lunas y tablero, y para kNN-SVM en lunas y tablero (entre −3.4 y −18.3 pp); una positiva, VB-RBF-SVM en el gaussiano lineal (+0.75 [+0.12, +1.50]), que no sobrevive al chequeo post hoc contra la referencia oráculo.
- Robustez (promedios sobre los 6 conjuntos, `results/tables.md`): exactitud media 95.2 % de la mejor referencia global en la condición principal, 89.2 % con 20 % de ruido en etiquetas (caída 6.0 pp) y 89.0 % con el 25 % del entrenamiento (caída 6.2 pp); las familias locales caen 5.1 / 4.8 / 6.9 / 3.7 pp con ruido y 7.3 / 5.9 / 5.1 / 4.4 pp con submuestreo (kNN-SVM / cell-SVM / VB-RBF-SVM / LLSVM), pero parten de exactitudes más bajas (90.9 / 89.5 / 95.2 / 89.5 %), así que las caídas no son comparables entre sí; lo que cuenta es la comparación pareada bajo cada condición: ninguna familia queda significativamente por encima de la referencia (tampoco frente a la referencia oráculo), kNN-SVM queda significativamente por debajo en 4 de 6 conjuntos con ruido y en 3 de 6 con submuestreo (frente a 2 de 6 en la condición principal), y VB-RBF-SVM en 2 de 6 con ruido y en ninguno con submuestreo.
- Ejemplo exacto: riesgo de Bayes 0.0500; umbral de centroides global con n = 320: 0.05025; con 2, 4, 8, 16, 32 celdas independientes de la etiqueta el exceso se multiplica por 2.01, 4.08, 8.38, 17.99, 61.68. Chequeo Monte Carlo (2000 muestras): 0.05024 ± 0.00001 y 0.05105 ± 0.00002 frente a los exactos 0.05025 y 0.05107.
- Ilustración (no demostrada): en d = 2 la versión kNN del umbral de centroides llega a 0.107 de riesgo en k = 20 (el doble del global); la kNN-SVM lineal queda dentro del error de simulación para k ≥ 20; la curva de aprendizaje de la SVM lineal en d = 10 decrece en todos los pasos (0.118 → 0.054) y su versión por celdas independientes crece con M (0.058, 0.066, 0.080, 0.099 para M = 1, 2, 4, 8).
- Cómputo total: 206 s (comparación) + 28 s (ejemplo exacto), un solo hilo, semilla fija.

## Reproducir

```bash
pip install -r experiments/requirements.txt
python3 experiments/run_comparison.py        # ~3.5 min en un núcleo (usar --fast para una prueba de humo)
python3 experiments/exact_example.py         # ~28 s
python3 experiments/posthoc_oracle.py        # < 1 s, lee results.json
python3 experiments/make_region_figure.py    # ~5 s, lee results.json
./manuscript/build.sh                        # requiere TeX Live (pdflatex, bibtex, latexmk)
```

Semilla maestra: `20260930`. Versiones usadas en la corrida de referencia: Python 3.11, NumPy 2.4, SciPy 1.17, scikit-learn 1.9. Los conjuntos se submuestrean (breast cancer a 300, digits a 400 con PCA a 16 componentes ajustada en el pliegue de entrenamiento; sintéticos con 400 puntos) para caber en el presupuesto de cómputo compartido; esto forma parte del diseño declarado.
