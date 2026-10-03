# SPD001 — Support Geometry and Nearest Neighbours

**Título de trabajo:** *Support Geometry and Nearest Neighbours: Does the Tangential–Orthogonal–Depth Decomposition Add Information Beyond Feature Lines, Local Hulls and Depth?*
**Línea de investigación:** SPD001 — Geometría del soporte y vecinos cercanos (área "Inteligencia artificial y aprendizaje")
**Estado:** borrador de trabajo **v0.2 (03/10/2026), una ronda de revisión interna aplicada** (informe `REFEREE_SPD001_ronda1_20260930.md`, respuesta `RESPUESTA_SPD001_ronda1_20260930.md`). La v0.1 (30/09/2026) se generó en una sesión de Claude Code a partir de la ficha pública de la línea (no existía manuscrito previo). Resultado principal **negativo** bajo un criterio fijado antes de la primera corrida completa y documentado en el código (sin prerregistro externo): la línea puede cerrarse con ese hallazgo.

## Qué es la línea

La ficha pública de SPD001 planteaba explorar las componentes *ortogonal*, *tangencial* y de *profundidad* de una consulta respecto de sus vecinos más cercanos, y preguntaba si esa descomposición aporta información más allá de las líneas de rasgos (nearest feature line), los cascos locales (HKNN) y las medidas de profundidad. La ficha decía que la comparación que aísla una contribución específica estaba pendiente y que no se había validado mejora alguna en exactitud. Este trabajo hace esa comparación.

## Qué contiene

| Ruta | Contenido |
|---|---|
| `manuscript/main.tex`, `manuscript/refs.bib` | Manuscrito en LaTeX (inglés, 10 páginas con bibliografía, cuerpo de 10 pt) y bibliografía (27 entradas reales, todas citadas). |
| `manuscript/main.pdf` | PDF compilado con pdflatex + bibtex (sin errores ni referencias indefinidas). |
| `manuscript/numbers.tex`, `manuscript/table_*.tex` | Macros y cuerpos de tabla **generados** desde los resultados; ningún número del texto está tipeado a mano. Desde v0.2 incluyen los IC con varianza de Nadeau–Bengio, las fracciones de pliegues en el borde de la rejilla y la moda determinista de hiperparámetros, recalculados desde las listas por pliegue. |
| `manuscript/build.sh` | Regenera macros y compila. |
| `experiments/support_geometry.py` | Todo el experimento (E1 comparación aislante, E2 barrido de régimen). `--fast` para una corrida reducida. |
| `experiments/make_numbers.py` | Convierte `results/*.json` en `numbers.tex`, las tablas del manuscrito y `results/tables_appendix.md`. |
| `experiments/make_figures.py` | Figuras (esquema de la descomposición, forest plot con IC bootstrap y NB, barrido de régimen). |
| `results/results.json`, `results/results_regime.json` | Resultados completos por pliegue, hiperparámetros elegidos, pesos ajustados, comparaciones y veredicto (corrida de referencia del 30/09/2026; no se recorrió en la ronda 1). |
| `results/tables.md` | Las tablas en Markdown escritas por la corrida de referencia. |
| `results/tables_appendix.md` | Tablas suplementarias generadas por `make_numbers.py`: TOD frente a cada referencia, ablaciones, exactitud selectiva (también frente a la mejor referencia por exactitud selectiva), hiperparámetros con fracciones en el borde y barrido de régimen, todas con IC bootstrap y NB. |
| `results/tables_run1_narrow_grids.md` | Tablas de la primera corrida completa con rejillas más estrechas (mismo veredicto). |
| `figures/` | Figuras en PDF y PNG. |
| `CONTINUIDAD_SPD001_20260930.md` | Nota de continuidad interna: supuestos, decisiones, limitaciones, próximos pasos, y la sección de la ronda 1 con lo que queda abierto. |
| `FICHA_SPD001_propuesta.md` | Texto propuesto para actualizar la ficha pública de la línea. |
| `REFEREE_SPD001_ronda1_20260930.md`, `RESPUESTA_SPD001_ronda1_20260930.md` | Informe del árbitro interno y respuesta del autor punto por punto. |

## Qué se hizo

1. **Definiciones precisas.** Para una consulta `q` y sus `k` vecinos de entrenamiento de la clase `c`: SVD centrada de la vecindad, subespacio tangente `T_m` (primeras `m` direcciones principales), distancia tangencial `T = |P r|`, distancia ortogonal `O = |(I−P) r|` con `r = q − centroide`, distancia al casco local, distancia HKNN penalizada (puntuación = valor del objetivo penalizado, lectura declarada en el texto), distancia a líneas de rasgos restringida a la vecindad y profundidad espacial local (Vardi–Zhang/Serfling) sobre la vecindad.
2. **Proposiciones elementales (demostradas aquí).** (i) `|r|² = T² + O²` y `O` con `m = rango` es la distancia al casco (HKNN con λ = 0); cuando `k > d` (los tres conjuntos con `d ≤ 3`) esa distancia es idénticamente cero. (ii) La distancia HKNN regularizada es exactamente `h_λ² = O² + Σ_j λ t_j²/(s_j² + λ)`: una combinación ponderada de la componente ortogonal y de las coordenadas tangenciales, monótona en λ, entre la distancia al casco y la distancia al centroide local. (iii) La profundidad espacial local no es función de `(T, O)` (ejemplo bidimensional explícito), así que formalmente podría aportar.
3. **Comparación aislante con criterio predefinido.** 8 conjuntos (iris, wine, breast cancer, digits submuestreado a 1000; swiss roll con clases a lo largo de la variedad, moons, moons + 10 coordenadas de ruido, esferas anidadas). Validación cruzada estratificada repetida 5×5, mismos pliegues para todos; hiperparámetros por leave-one-out en el pliegue de entrenamiento. Referencias: kNN, NFL, HKNN, casco PCA local (LPH), distancia media a la clase (LCD), profundidad espacial (SD). Propuesta: logit condicional con pesos compartidos sobre `(log T, log O, log(1−profundidad))` (TOD) y sus ablaciones TO, TD, OD. Criterio C1: la descomposición "aporta información" solo si TOD supera a la mejor referencia de cada conjunto en ≥ 5 de 8 con IC bootstrap 95 % por pares (sobre pliegues) estrictamente por encima de 0. Secundarios: atribución por ablación (C2), exactitud selectiva al 80 % de cobertura (C3) y barrido de régimen con `p ∈ {0, 2, 5, 10, 20}` coordenadas de ruido (E2). Como los pliegues de validación cruzada repetida comparten datos, cada recuento se da en dos lecturas: bootstrap (anticonservador) y varianza de Nadeau–Bengio (conservadora).

## Resultados (corrida de referencia, semilla 20260930)

- **C1 no se cumple: 0 de 8 victorias significativas (se exigían 5), en las dos lecturas.** TOD − mejor referencia va de −0.77 (moons, vs HKNN) a +0.23 puntos (esferas, vs HKNN), dentro de 1 punto en los 8 conjuntos y con media positiva solo en wine y esferas. El IC bootstrap queda por debajo de 0 en digits (−0.34 [−0.64, −0.06], vs NFL) y moons (−0.77 [−1.27, −0.27]); ninguna de esas pérdidas sobrevive a la corrección de Nadeau–Bengio (p = 0.41 y 0.29; IC NB [−1.18, +0.50] y [−2.23, +0.70]). **Cota de potencia:** el mayor límite superior del IC en todos los conjuntos es **+1.33 puntos con bootstrap y +3.54 con la varianza de Nadeau–Bengio** (ambos en wine): el estudio excluye ganancias de más de ~1.3 puntos solo bajo la lectura anticonservadora y de más de ~3.5 bajo la cautelosa; no excluye ganancias menores. En iris y wine un error de prueba vale 3.33 y 2.78 puntos.
- **Frente a HKNN,** la referencia más cercana: de −0.77 a +0.40 puntos, ningún IC por encima de 0 (ambas lecturas). HKNN, LPH, TOD, TO y OD nunca difieren entre sí en más de 1.3 puntos: se comportan como una sola familia, como predice la Proposición (ii). La mejor referencia es un método de soporte local (HKNN, LPH o NFL) en los 8 conjuntos.
- **Atribución (C2): la información está en la componente ortogonal.** Quitarla cuesta de +0.66 (wine) a +5.10 puntos (digits), IC > 0 en **7 de 8 con bootstrap y 2 de 8 con NB** (digits [+3.0, +7.2], esferas [+0.0, +7.1]); la atribución descansa en el tamaño de los efectos y en los pesos ajustados, no en el recuento. Quitar la profundidad cambia la exactitud entre −0.35 y +0.53 puntos (IC > 0 en 0 de 8 en ambas lecturas; en breast cancer el IC bootstrap queda marginalmente por debajo de 0). Quitar la tangencial: entre −0.23 y +0.53 (0 de 8). Pesos ajustados medios: `w_O` ∈ [1.52, 3.93], `w_T` ∈ [0.17, 1.38], `w_D` ∈ [−1.15, 1.81] con signo negativo en 3 conjuntos. La única victoria bootstrap de TOD sobre el casco PCA puro es en esferas (+0.87 [+0.17, +1.53]; NB [−1.2, +2.9]), donde la profundidad ayuda (+0.47 [−0.03, +0.97] sobre TO), pero HKNN cierra esa misma brecha con su penalización (TOD − HKNN = +0.23).
- **Abstención (C3):** exactitud selectiva al 80 % de cobertura, TOD − mejor referencia (por exactitud) entre −1.04 y +0.20 puntos (1 IC bootstrap > 0, digits, NB [−0.2, +0.6]; 2 por debajo, moons y moons+ruido; 0 y 0 con NB). Frente a la mejor referencia por exactitud selectiva (la comparación natural): de −3.2 a +0.1 puntos, 0 IC > 0 y 2 < 0. La posterior del logit no es mejor señal de abstención que los márgenes de las referencias.
- **Régimen con ruido fuera de la variedad (E2):** con `p` de 0 a 20 coordenadas de ruido en moons, la mejor referencia es HKNN o LCD en cada `p`; TOD − mejor referencia va de −0.77 a −0.07 puntos, 0 IC > 0. La contribución de la profundidad (TOD − TO) tiene un único IC bootstrap > 0 en todo el estudio, en `p = 2` (+0.90 [+0.33, +1.50]; NB [−0.8, +2.6], p = 0.28; 1 de 13 intervalos de profundidad examinados), y ahí TOD sigue 0.07 puntos por debajo de la mejor referencia: la profundidad ayuda al logit a alcanzar a las referencias, no a superarlas.
- **Hiperparámetros en el borde:** tras ampliar las rejillas, el `k` elegido sigue en el máximo (30) en 56–68 % de los pliegues en moons y en 84–96 % en moons+ruido (TOD / HKNN), frente a ≤ 52 % en los demás conjuntos; la comparación es simétrica pero las exactitudes absolutas allí pueden estar algo por debajo del óptimo. La ampliación costaría ≈ 2× la corrida de referencia y queda como paso siguiente.
- **Cómputo:** 294 s de CPU (310 s de pared) la corrida de referencia; 147 s la primera corrida con rejillas más estrechas; ronda 1 de revisión ≈ 45 s de CPU (medición del coste de ampliar las rejillas, figuras, compilaciones), sin recorrer el benchmark.

## Reproducir

```bash
pip install -r experiments/requirements.txt
python3 experiments/support_geometry.py      # ~5 min de CPU con BLAS de un hilo (fijado dentro del script); --fast para ~1 min
python3 experiments/make_figures.py
./manuscript/build.sh                        # requiere TeX Live (pdflatex, bibtex, latexmk); regenera numbers.tex, table_*.tex y results/tables_appendix.md
```

Semilla maestra: `20260930`. Versiones usadas en la corrida de referencia: Python 3.11, NumPy 2.4, SciPy 1.17, scikit-learn 1.9. Nota: `support_geometry.py` v0.2 devuelve además `nb_lo`/`nb_hi` en cada comparación y usa una moda determinista de hiperparámetros; `results/results.json` es todavía la corrida del 30/09 (sin esos campos), y `make_numbers.py` los recalcula desde las listas por pliegue, así que el manuscrito no depende de recorrer.
