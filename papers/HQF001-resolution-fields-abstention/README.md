# HQF001 — Resolution Fields and Abstention

**Título de trabajo:** *Local Resolution and Abstention: A Controlled Comparison of Anisotropic Resolution Fields with Local-Metric and Prototype Baselines under a Predefined Criterion*  
**Línea de investigación:** HQF001 — Resolución local e incertidumbre en aprendizaje / Local resolution and uncertainty in learning (área "Inteligencia artificial y aprendizaje")  
**Estado:** borrador de trabajo v0.1 (30/09/2026), generado en una sesión de Claude Code a partir de la ficha pública de la línea (no existía manuscrito previo). Resultado principal **negativo con criterio predefinido**: la línea queda cerrada con números, salvo que se retome por las vías concretas que se listan al final.

## Qué contiene

| Ruta | Contenido |
|---|---|
| `manuscript/main.tex`, `manuscript/refs.bib` | Manuscrito en LaTeX (inglés, 10 páginas) y bibliografía (24 entradas reales). |
| `manuscript/main.pdf` | PDF compilado con pdflatex + bibtex (sin errores ni referencias indefinidas). |
| `manuscript/numbers.tex`, `manuscript/table_*.tex` | Macros y cuerpos de tabla **generados** desde `results/`; ningún número del texto está tipeado a mano. |
| `experiments/selective_benchmark.py` | Benchmark de clasificación selectiva: campo de resolución anisótropo (y 5 variantes/ablaciones) frente a 7 referencias ajustadas por CV interna, en 8 datasets, 15 folds pareados, bootstrap. |
| `experiments/lda_identity.py` | Verificación numérica de la Proposición 1 (margen de resolución vs. margen posterior de LDA). |
| `experiments/make_figures.py`, `experiments/make_numbers.py` | Figuras y macros a partir de los JSON. |
| `results/results.json`, `results/tables.md` | Resultados completos del benchmark (semilla fija) y tablas legibles. |
| `results/results_identity.json`, `results/tables_identity.md` | Resultados de la verificación de la proposición. |
| `figures/` | Figuras en PNG y PDF. |
| `CONTINUIDAD_HQF001_20260930.md` | Nota de continuidad interna: supuestos reconstruidos, decisiones, resultados de referencia, limitaciones, pendientes. |
| `FICHA_HQF001_propuesta.md` | Texto propuesto para actualizar la ficha pública de la línea. |

## Qué es la línea y qué se hizo

La ficha pública de HQF001 proponía representar la incertidumbre mediante un **campo de resolución anisótropo**: una matriz definida positiva $A(x)$ en cada punto del espacio de entrada, estimada de la geometría local de los datos, con una regla de abstención derivada de ella. El objetivo declarado era comprobar si esa representación añade información más allá de las métricas locales y los métodos de prototipos; el hallazgo declarado, que las comparaciones disponibles no establecían una ganancia residual. Aquí se reconstruyó una versión precisa de la idea (covarianza local de $K_m$ vecinos con contracción $\alpha$ hacia la identidad escalada; prototipos locales por clase; tres puntuaciones: margen de Mahalanobis bajo $A(x)$, log-volumen del elipsoide y anisotropía), se demostró un enunciado exacto sobre lo que la anisotropía podría aportar, y se corrió la **comparación controlada que faltaba, con criterio de éxito fijado antes de correr**: "ganancia residual" = AURC menor que la mejor referencia en la mayoría (≥5 de 8) de los datasets, con intervalo pareado al 95 % que excluya 0.

## Resultados (corrida de referencia, semilla 20260930, 3×5 folds estratificados, CV interna de 3 folds sobre AURC, bootstrap B = 2000)

- **Criterio predefinido no cumplido.** El campo anisótropo es mejor que la mejor referencia en **0 de 8** datasets; peor con IC 95 % que excluye 0 en **6 de 8** (diferencia de AURC×100: iris +0.20, breast-cancer +0.58, synth-informative +1.30, moons-aniso +0.56, synth-classcov +0.43, synth-lda +1.25) y no concluyente en 2 (wine +0.05 [−0.00, +0.10]; digits +0.01 [−0.11, +0.13]). Las cinco variantes restantes (isótropa, euclidiana, volumen, anisotropía, prototipos globales) son peores en 8 de 8.
- **La anisotropía sí añade información respecto a la ablación isótropa del propio campo**, pero no de forma uniforme: mejor en 3 datasets (iris −0.28, wine −0.20, digits −0.78), peor en 2 (breast-cancer +0.37, synth-classcov +0.16), no concluyente en 3. El ajuste elige la contracción más fuerte disponible (α = 0.5) en el 72 % de los casos.
- **Ganancia específica de régimen, nombrada con precisión:** en synth-classcov (dos gaussianas con covarianzas rotadas distintas y medias coincidentes; error de Bayes 7.7 %) el campo supera a k-NN (−0.29), DANN (−0.37) y random forest (−1.08), pero no a QDA (+0.43 [+0.32, +0.55]); y su ablación euclidiana (AURC×100 = 1.23) es mejor que el campo completo (1.40), de modo que la ganancia sobre los métodos locales proviene de los prototipos locales con margen, **no** de la anisotropía.
- **Las puntuaciones puramente geométricas no informan:** ordenar por log-volumen es peor que un orden aleatorio de las mismas predicciones en 3 de 8 datasets; ordenar por anisotropía, en 5 de 8. La información está en el margen (dónde están los prototipos respecto al elipsoide), no en el tamaño ni la forma del elipsoide.
- **Enunciado exacto (demostrado):** con la métrica igual a la inversa de la covarianza compartida (marco LDA) y dos clases equiprobables, el margen de resolución $s$ cumple $m = \tanh(s/4)$ con el margen posterior $m$, así que ambas reglas de abstención coinciden (verificado: desviación máxima 2.8×10⁻¹⁶, diferencia de AURC 0). Con priors distintos la identidad falla para el margen sin signo y se restaura con la corrección por priors. Con $K \ge 3$, $s = 2\log(p_{(1)}/p_{(2)})$ pero $s$ no es función de $p_{(1)}-p_{(2)}$ ni del máximo posterior (contraejemplo explícito). Para un campo arbitrario, $s_A - s = 2\,(x-\bar m)^{\top}(A(x)-\Sigma^{-1})\,\delta$: solo la componente de la métrica a lo largo de la diferencia de prototipos $\delta$ puede cambiar la puntuación.
- **Cómputo:** 449 s de CPU (7.5 min, un hilo) para el benchmark; ~1 s para la verificación. El alcance es computacional; no se afirma nada sobre fenómenos físicos ni cuánticos (se reproduce la salvedad de la ficha).

## Reproducir

```bash
pip install -r experiments/requirements.txt
python3 experiments/selective_benchmark.py     # ~7.5 min CPU (usar --fast para ~2.5 min)
python3 experiments/lda_identity.py            # ~1 s
python3 experiments/make_figures.py
./manuscript/build.sh                          # requiere TeX Live (pdflatex, bibtex, latexmk)
```

Semilla maestra: `20260930`. Versiones usadas en la corrida de referencia: Python 3.11, NumPy 2.4, SciPy 1.17, scikit-learn 1.9, Matplotlib 3.11.
