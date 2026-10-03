# TCD001 — Fragility of Lasso Variable Selection

**Título de trabajo:** *Fragility of Lasso Variable Selection: Removal Witnesses, Exact Deletion Tests, Non-Monotonicity and Computational Status*  
**Línea de investigación:** TCD001 — Fragilidad de la selección de variables con Lasso (área "Estadística y medición")  
**Estado:** borrador de trabajo **v0.2, una ronda de revisión interna aplicada** (informe `REFEREE_TCD001_ronda1_20260930.md`, respuesta `RESPUESTA_TCD001_ronda1_20260930.md`, 03/10/2026). El v0.1 (30/09/2026) se generó en una sesión de Claude Code a partir de la ficha pública de la línea (no existía manuscrito previo). Ficha original: "estudio de cómo cambia el conjunto de variables seleccionadas al eliminar observaciones; hallazgos: cambios no monótonos y conexiones con problemas combinatorios conocidos; alcance: novedad, ventaja computacional y algunos certificados no quedaron suficientemente establecidos". Este borrador fija las definiciones, demuestra lo que se puede demostrar, declara qué certificados son holgados y muestra que, en instancias sintéticas pequeñas, el criterio de ventaja computacional prefijado no se cumple porque la búsqueda exhaustiva con el test cerrado ya es barata; no se reclama novedad.

## Qué contiene

| Ruta | Contenido |
|---|---|
| `manuscript/main.tex`, `manuscript/refs.bib` | Manuscrito en LaTeX (inglés) y bibliografía (23 entradas reales). |
| `manuscript/main.pdf` | PDF compilado (PAGES_PLACEHOLDER páginas; 0 errores, sin referencias ni citas indefinidas). |
| `manuscript/numbers.tex`, `manuscript/table_*.tex` | Macros y cuerpos de tabla **generados** por `experiments/make_numbers.py` desde `results/*.json`; ningún número del texto está tipeado a mano. |
| `experiments/lasso_fragility.py` | Biblioteca: solver (homotopía LARS de scikit-learn con verificación KKT y retroceso a descenso por coordenadas), test exacto de eliminación (Prop. 3.1) vectorizado sobre subconjuntos, índice de inestabilidad (Cor. 3.2), certificado para k eliminaciones (Prop. 3.4), búsqueda exhaustiva de testigos mínimos, tres heurísticas, generador de instancias. |
| `experiments/exact_examples.py` | E0: ejemplos de no monotonía con p=1 (a mano; objetivos "sale" y "entra") y p=2 (búsqueda sembrada, competencia entre variables) verificados en aritmética racional exacta. |
| `experiments/run_validation.py` | E1: validación del test exacto y de los certificados contra reajustes. |
| `experiments/run_fragility.py` | E2/E3/E5: números de fragilidad exactos (n ≤ 14), heurísticas vs exacto con criterio predefinido, frecuencia de pares no monótonos. |
| `experiments/run_scaling.py` | E4: escalamiento con n (exacto hasta n=34 con \|R\| ≤ 6; cotas greedy y certificadas hasta n=400). |
| `experiments/check_b1_counterexample.py` | Comprobación ejecutable del contraejemplo del árbitro al Cor. 3.2 (h_i = 1) y del empate exacto que hace fallar a `lars_path` (ronda 1). |
| `experiments/make_figures.py`, `experiments/make_numbers.py` | Figuras y macros. |
| `results/*.json`, `results/*.md` | Resultados completos con semilla fija y tablas Markdown por celda (las tablas por celda de E1, E2, E4 y E5 viven aquí, no en el PDF). |
| `figures/` | Figuras en PDF y PNG (`fig_combined` es la del manuscrito). |
| `CONTINUIDAD_TCD001_20260930.md` | Nota de continuidad interna: supuestos, decisiones, limitaciones, pendientes, ronda 1 de revisión. |
| `FICHA_TCD001_propuesta.md` | Propuesta de actualización de la ficha pública. |
| `REFEREE_TCD001_ronda1_20260930.md`, `RESPUESTA_TCD001_ronda1_20260930.md` | Informe del árbitro interno y respuesta punto por punto del autor. |

## Idea del paper en cuatro líneas

1. **Definiciones.** Para datos (X, y), penalización μ y una regla que fija la penalización en submuestras (constante, o proporcional = `alpha` fijo de scikit-learn), un *testigo de eliminación* para un cambio objetivo (una variable sale, una entra, o cualquier cambio del soporte) es un conjunto propio no vacío R de observaciones tal que el Lasso sobre D∖R tiene minimizador único y exhibe el cambio; el *número de fragilidad* es el mínimo |R|. La *no monotonía* es la existencia de R ⊂ R' con R testigo y R' no.
2. **Test exacto y certificados (demostrados).** Por KKT y Woodbury, si (S, s) es el soporte con signos en D, el candidato sobre D∖R tiene forma cerrada (β̃_S = β̂_S − V_R^T (I − H_R)^{-1} r_R, más un término explícito si la penalización cambia) y (S, s) se conserva si y solo si el candidato cumple KKT: costo O(|R|³ + p|R|) por conjunto, sin reajustar (Prop. 3.1). Para |R| = 1 con h_i < 1 y regla constante es la fórmula DFBETA de Belsley–Kuh–Welsch con el residuo del Lasso, y da un certificado O(np) de que ninguna eliminación individual cambia el soporte (Cor. 3.2; si h_i = 1 el soporte no se conserva y el índice es +∞); para k eliminaciones hay un certificado polinomial (sumas de los k mayores), correcto pero holgado (Prop. 3.4). El test decide "(S, s) se conserva"; identifica un testigo de "cualquier cambio" cuando el minimizador en D∖R es único (c.s. en diseños continuos; certificado en exacto para los ejemplos enteros).
3. **No monotonía y estatus computacional (demostrados).** Ejemplo con p=1 verificable a mano y ejemplo con p=2 (competencia entre variables) verificado en aritmética exacta. Decidir si existe un testigo de *deselección* es NP-completo ya con p=1 (reducción directa desde Subset Sum, bajo ambas reglas; dureza débil: existen algoritmos pseudo-polinomiales); la dirección de *selección* con p=1 se resuelve en O(n log n); para p ≥ 2 solo hay una conjetura.
4. **Experimentos (verificados, solo en dos familias sintéticas elegidas tras un barrido piloto).** El test exacto hace viable la búsqueda exhaustiva (1.1 μs por subconjunto frente a 442 μs por reajuste, ×399 en esta corrida) hasta n=34 con |R| ≤ 6. Ninguna de las tres heurísticas cumple el criterio de "ventaja computacional" fijado antes de correr, porque a n ≤ 14 ninguna baja de un décimo del coste exhaustivo (el mínimo cociente de coste mediano es 0.46; 0.26 descontando el ajuste inicial de la heurística).

## Resultados de referencia (corrida v0.2, 03/10/2026, semillas 20260930 y 20260931)

Todos los números no temporales coinciden con los de v0.1; solo cambiaron los tiempos y los cocientes de coste (máquina compartida).

- **E1.** El test exacto coincide con el reajuste en 2760/2760 eliminaciones individuales y 7200/7200 eliminaciones múltiples (ambas reglas); coeficientes en forma cerrada a 10⁻¹⁵ del reajuste. La condición suficiente del Cor. 3.2 certifica 1216 de 2114 eliminaciones individuales realmente estables (58%). El certificado para k eliminaciones da k* ≥ 1 en el 30% de las instancias de la familia A con f ≥ 2 (n ≤ 14), brecha media f − 1 − k* = 1.2: es correcto pero holgado.
- **E2 (n ≤ 14, 60 instancias por celda).** Familia B ("ruidosa": p=8, b=2, ρ=0.5, c=1): el soporte cambia al quitar **una sola observación en el 92%** de las 240 instancias (máximo f = 3; 8 instancias con soporte vacío, 2 sin testigo dentro del tope). Familia A ("señal fuerte": p=4, b=4, ρ=0, c=1.5): f = 1 en el 52%, máximo 4, media 1.73. Los testigos mínimos de "cualquier cambio" son en su mayoría eventos simples: sale una variable (51% A / 54% B), entra una (43% / 25%), intercambio simultáneo (6% / 20%); ningún cambio solo de signo.
- **E3 (heurísticas vs exacto, criterio predefinido: exactitud ≥ 90% y costo mediano ≤ 10% del exhaustivo).** 0 de 18 combinaciones (familia × objetivo × heurística) lo cumplen. El greedy de un paso es el más preciso: 97%/100% exacto para "cualquier cambio", 95%/98% para "sale la más débil", 86%/88% para "entra la más fuerte" (A/B; estimaciones puntuales sobre 206–240 instancias con errores típicos de 0.4–3.1 puntos: el déficit en "entra" queda a 1.7 y 1.1 errores típicos del umbral), pero su costo mediano es 0.5–1.3 veces el de la búsqueda exhaustiva con el test cerrado. La predicción lineal tipo AMIP del número de eliminaciones acierta en el 70% (A) y 99% (B) de los casos de "cualquier cambio".
- **E4 (escalamiento).** Familia A: media censurada de f de 1.43 (n=10) a 4.00 (n=34, 1 de 20 instancias por encima del tope y excluida); familia B: f = 1 en el 75% de las instancias a n=34. A n=34 el greedy cuesta el 7.0% del exhaustivo con 89% de exactitud. Con n ≥ 50 solo hay horquillas: a n=400 en A el testigo greedy mediano tiene 10 observaciones (g/n ≈ 0.028), la cota inferior certificada mediana es k*+1 con k* = 5, y la razón media (k*+1)/g es 0.57.
- **E5 (no monotonía).** Añadir una observación a un testigo mínimo de "sale la variable más débil" la hace volver al soporte en el 7.1% (A) y 10.5% (B) de los 6960/8092 pares, con al menos un par no monótono en el 51%/72% de las instancias; para "cualquier cambio", el soporte original se restaura en el 14.9%/9.3% de los pares.

## Reproducir

```bash
pip install -r experiments/requirements.txt
python3 experiments/check_b1_counterexample.py   # < 1 s, comprobación del contraejemplo de la ronda 1
python3 experiments/exact_examples.py     # ~2 s
python3 experiments/run_validation.py     # ~8 s
python3 experiments/run_fragility.py      # ~40 s   (--fast para ~7 s)
python3 experiments/run_scaling.py        # ~35 s   (--fast para ~15 s)
python3 experiments/make_figures.py
./manuscript/build.sh                     # requiere TeX Live (pdflatex, bibtex, latexmk)
```

Cómputo total de la corrida de referencia v0.2: 84 s de CPU de Python (≈1.4 min; 89 s de pared, los cuatro scripts en una sola sesión, `results/run_session_v02_start.txt`) en un núcleo de una máquina compartida de cuatro. Versiones: Python 3.11, NumPy 2.4, SciPy 1.17, scikit-learn 1.9.
