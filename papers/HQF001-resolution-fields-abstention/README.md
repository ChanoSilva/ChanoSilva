# HQF001 — Resolution Fields and Abstention

**Título de trabajo:** *Local Resolution and Abstention: A Controlled Comparison of Anisotropic Resolution Fields with Local-Metric and Prototype Baselines under a Predefined Criterion*  
**Línea de investigación:** HQF001 — Resolución local e incertidumbre en aprendizaje / Local resolution and uncertainty in learning (área "Inteligencia artificial y aprendizaje")  
**Estado:** borrador de trabajo **v0.2 (03/10/2026), una ronda de revisión interna aplicada** (informe `REFEREE_HQF001_ronda1_20260930.md`, respuesta `RESPUESTA_HQF001_ronda1_20260930.md`). v0.1 (30/09/2026) se generó en una sesión de Claude Code a partir de la ficha pública de la línea (no existía manuscrito previo). Resultado principal **negativo con criterio predefinido**: la formulación reconstruida (campo no supervisado) queda descartada con números; se propone cerrar la línea salvo las tres vías concretas del §6 del manuscrito.

## Qué contiene

| Ruta | Contenido |
|---|---|
| `manuscript/main.tex`, `manuscript/refs.bib` | Manuscrito en LaTeX (inglés, PAGES_PLACEHOLDER páginas con referencias) y bibliografía (26 entradas reales). |
| `manuscript/main.pdf` | PDF compilado con pdflatex + bibtex (sin errores ni referencias indefinidas). |
| `manuscript/numbers.tex`, `manuscript/table_*.tex` | Macros y cuerpos de tabla **generados** desde `results/`; ningún número del texto está tipeado a mano. |
| `experiments/selective_benchmark.py` | Benchmark de clasificación selectiva (v0.2): campo de resolución anisótropo (y 5 variantes/ablaciones) frente a 7 referencias ajustadas por CV interna, en 8 datasets, 15 folds pareados; por cada par: IC bootstrap percentil (B = 20 000, el del criterio), IC t de Student, IC t con corrección de Nadeau–Bengio, victorias/empates/derrotas, p de Wilcoxon, indicador de caso límite. |
| `experiments/lda_identity.py` | Verificación numérica de las Proposiciones 3.1 y 3.2 (margen de resolución vs. margen posterior de LDA; descomposición con prototipos arbitrarios). |
| `experiments/make_figures.py`, `experiments/make_numbers.py` | Figuras y macros a partir de los JSON. |
| `results/results.json`, `results/tables.md`, `results/run_log_v02.txt` | Resultados completos de la corrida v0.2 (semilla fija), tablas legibles con los tres IC, y log de la corrida. |
| `results/results_v01.json`, `results/tables_v01.md` | Corrida v0.1 (synth-classcov con medias coincidentes), conservada para contraste. |
| `results/results_identity.json`, `results/tables_identity.md` | Resultados de la verificación de las proposiciones. |
| `figures/` | Figuras en PNG y PDF (incluye `fig_rc_curves`, que ya no va en el PDF). |
| `CRITERIO_HQF001.md` | Registro fechado del criterio predefinido, con el hash del script que lo evalúa. |
| `CONTINUIDAD_HQF001_20260930.md` | Nota de continuidad interna: supuestos reconstruidos, decisiones, resultados de referencia, limitaciones, ronda 1 de revisión, pendientes. |
| `FICHA_HQF001_propuesta.md` | Texto propuesto para actualizar la ficha pública de la línea. |

## Qué es la línea y qué se hizo

La ficha pública de HQF001 proponía representar la incertidumbre mediante un **campo de resolución anisótropo**: una matriz definida positiva $A(x)$ en cada punto del espacio de entrada, estimada de la geometría local de los datos, con una regla de abstención derivada de ella. El objetivo declarado era comprobar si esa representación añade información más allá de las métricas locales y los métodos de prototipos; el hallazgo declarado, que las comparaciones disponibles no establecían una ganancia residual. Aquí se reconstruyó una versión precisa de la idea (covarianza local de $K_m$ vecinos con contracción $\alpha$ hacia la identidad escalada; prototipos locales por clase; tres puntuaciones: margen de Mahalanobis bajo $A(x)$, log-volumen del elipsoide y anisotropía), se demostró un enunciado exacto sobre lo que la anisotropía podría aportar, y se corrió la **comparación controlada que faltaba, con criterio de éxito fijado antes de correr** (`CRITERIO_HQF001.md`): "ganancia residual" = AURC menor que la mejor referencia en la mayoría (≥5 de 8) de los datasets, con intervalo bootstrap pareado al 95 % que excluya 0.

## Resultados (corrida v0.2, semilla 20260930, 3×5 folds estratificados, CV interna de 3 folds sobre AURC; IC al 95 %: bootstrap percentil B = 20 000 / t de Student sobre pliegues)

- **Criterio predefinido no cumplido, en las tres lecturas.** El campo anisótropo es mejor que la mejor referencia en **0 de 8** datasets; peor con IC que excluye 0 en **6 de 8 con bootstrap y 5 con IC t** (diferencia de AURC×100: iris +0.20 [+0.05, +0.43] bootstrap, [−0.03, +0.43] t, 1/6/8 victorias/empates/derrotas; breast-cancer +0.58 [+0.34, +0.89] / [+0.26, +0.90], 0/0/15; synth-informative +1.30 [+0.78, +1.86] / [+0.69, +1.92], 2/0/13; moons-aniso +0.56 [+0.35, +0.75] / [+0.33, +0.80], 2/0/13; synth-classcov +1.08 [+0.86, +1.33] / [+0.81, +1.35], 0/0/15; synth-lda +1.25 [+1.04, +1.50] / [+0.98, +1.52], 0/0/15) y no concluyente en el resto (wine +0.05 [−0.005, +0.10], caso límite, 4/4/7; digits +0.01 [−0.11, +0.14], 7/0/8). Con la corrección de Nadeau–Bengio: 0 mejor / 3 peor / 5 no concluyente. Las cinco variantes restantes son peores en 8 de 8 (bootstrap).
- **La anisotropía frente a la ablación isótropa del propio campo: sugerente, no establecida.** Mejor en 3 datasets con bootstrap (iris −0.28, wine −0.20, digits −0.78), **2 con IC t** (wine, digits), 0 con Nadeau–Bengio; peor en 2 (breast-cancer +0.37, synth-classcov +0.47) con ambos IC. Victorias/empates/derrotas por folds: digits 15/0/0, wine 8/5/2, iris 8/4/3. En todo caso es redundante dadas las referencias. El ajuste elige la contracción más fuerte disponible (α = 0.5) en el 72 % de los casos.
- **Régimen de covarianzas distintas (synth-classcov, recalibrado en v0.2: desplazamiento 1.54, error de Bayes 9.9 %):** el campo (AURC×100 2.77) vence a NCM, LDA y regresión logística (8.51, 6.30, 5.96) y al random forest (3.42), es no concluyente frente a DANN (2.83), peor que k-NN (2.55; bootstrap, caso límite) y claramente peor que QDA (1.69, +1.08 [+0.86, +1.33]); y sus ablaciones isótropa (2.30) y euclidiana (2.31) son mejores que el campo completo: lo que ayuda ahí es el margen a prototipos locales, **no** la anisotropía. (En v0.1 las medias coincidían por un fallo de calibración y NCM/LDA/LogReg estaban al nivel del azar, 48 % de error; esas "victorias" eran consecuencia del diseño.)
- **Las puntuaciones puramente geométricas no informan:** ordenar por log-volumen es peor que un orden aleatorio de las mismas predicciones en 3 de 8 datasets; ordenar por anisotropía, en 5 de 8. La información está en el margen (dónde están los prototipos respecto al elipsoide), no en el tamaño ni la forma del elipsoide.
- **Enunciado exacto (demostrado):** con la métrica igual a la inversa de la covarianza compartida (marco LDA) y dos clases equiprobables, el margen de resolución $s$ cumple $m = \tanh(s/4)$ con el margen posterior $m$, así que ambas reglas de abstención coinciden (verificado: desviación máxima 2.8×10⁻¹⁶, diferencia de AURC 0). Con priors distintos la identidad falla para el margen sin signo y se restaura con la corrección por priors. Con $K \ge 3$ clases **equiprobables**, $s = 2\log(p_{(1)}/p_{(2)})$ (con priors desiguales hay que restar $2\log(\pi_{(1)}/\pi_{(2)})$; verificado), pero $s$ no es función de $p_{(1)}-p_{(2)}$ ni del máximo posterior (contraejemplo explícito). Para un campo arbitrario con prototipos fijos, $s_A - s = 2\,(x-\bar m)^{\top}(A(x)-\Sigma^{-1})\,\delta$: solo la componente de la métrica a lo largo de la diferencia de prototipos $\delta$ puede cambiar la puntuación; con prototipos locales aparecen dos términos más (Prop. 3.2(c)), de modo que esa lectura es heurística para el método tal como se corre.
- **Cómputo:** 284.5 s de CPU (4.7 min, un hilo) para la corrida v0.2; < 1 s para la verificación. El alcance es computacional; no se afirma nada sobre fenómenos físicos ni cuánticos (se reproduce la salvedad de la ficha).

## Reproducir

```bash
pip install -r experiments/requirements.txt
python3 experiments/selective_benchmark.py     # ~5 min CPU (usar --fast para una corrida reducida; --resummarise recalcula solo las estadísticas)
python3 experiments/lda_identity.py            # ~1 s
python3 experiments/make_figures.py
./manuscript/build.sh                          # requiere TeX Live (pdflatex, bibtex, latexmk)
```

Semilla maestra: `20260930`. Versiones usadas en la corrida de referencia: Python 3.11, NumPy 2.4, SciPy 1.17, scikit-learn 1.9, Matplotlib 3.11.
