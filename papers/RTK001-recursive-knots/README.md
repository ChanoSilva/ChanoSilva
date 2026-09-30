# RTK001 — Geometry of Recursive Knots

**Título de trabajo:** *Geometry of Recursive Knots: Iterated Cables by Frame Offsets, Their Thickness and Ropelength*  
**Línea de investigación:** RTK001 — Geometría de nudos recursivos (área "Matemáticas y estructuras")  
**Estado:** borrador de trabajo v0.1 (30/09/2026), generado en una sesión de Claude Code a partir de la ficha pública de la línea. **No existía ningún manuscrito previo**; la familia de curvas, las definiciones y el protocolo se fijaron aquí (véase la nota de continuidad).

## Qué contiene

| Ruta | Contenido |
|---|---|
| `manuscript/main.tex`, `manuscript/refs.bib` | Manuscrito en LaTeX (inglés, 9 páginas) y bibliografía (10 entradas). |
| `manuscript/main.pdf` | PDF compilado (pdflatex + bibtex vía latexmk; sin referencias indefinidas). |
| `manuscript/numbers.tex`, `manuscript/table_*.tex` | Macros y cuerpos de tabla **generados** desde `results/results.json`; ningún número del texto está tipeado a mano. |
| `manuscript/build.sh` | Regenera macros y compila. |
| `experiments/recursive_knots.py` | Construye los polígonos K_0..K_3 (cables iterados por desplazamiento en un marco de Bishop cerrado) y mide longitud, minRad, distancia doblemente crítica, grosor poligonal, ropelength, writhe y holonomía. |
| `experiments/make_numbers.py` | Convierte `results/results.json` en `numbers.tex` y las tablas. |
| `results/results.json`, `results/tables.md` | Resultados completos (determinista; semilla 20260930 solo como registro). |
| `figures/fig_curves.*`, `figures/fig_rop.*` | Proyecciones de K_1, K_2, K_3 y crecimiento de L/τ con la profundidad. |
| `PLAN.md` | Plan de una página escrito al inicio de la sesión. |
| `CONTINUIDAD_RTK001_20260930.md` | Nota de continuidad: supuestos, decisiones, limitaciones, pendientes. |
| `FICHA_RTK001_propuesta.md` | Propuesta de actualización de la ficha pública. |

## Idea del paper en tres líneas

1. Se fija una familia concreta de "nudos recursivos": K_0 es un círculo; K_d es el patrón tórico (p_d, q_d) colocado sobre el tubo de radio r_d alrededor de K_{d−1}, usando un marco de Bishop (de rotación mínima) cerrado con un giro lineal. Por defecto (p, q) = (2, 3) y r_d = f · grosor(K_{d−1}).
2. Se demuestra lo elemental: K_d es una curva cerrada suave y embebida si r_d ≤ grosor(K_{d−1})/2 (Lema 3.1); el marco cerrado tiene número de enlace round(Wr K_{d−1}) con su núcleo, lo que identifica K_d como el cable (p, q + p·round(Wr)) de K_{d−1} (Lema 3.2); y L(K_d) ≤ p L(K_{d−1})(1 + r κ_max) + r(2πq + p|α|) (Lema 3.3). La cota inferior del grosor de K_d solo se demuestra en dos de tres casos; el caso local queda como hipótesis (H_c) verificada numéricamente. Bajo (H_c), la cota de ropelength cumple una recursión lineal: Rop_d ≤ 2π Λ^d con Λ = A/γ explícito (Λ = 20 para (2,3), f = 1/2, c = 1/2).
3. Numéricamente, polígonos explícitos de hasta 8192 vértices dan L/τ = 38.4, 155.6 y 622.7 en profundidades 1, 2, 3 (patrón (2,3), f = 1/2), estables al 0.03 % al duplicar la resolución. Son cotas superiores verificadas numéricamente para polígonos explícitos, no grosores suaves certificados. No se afirma estacionariedad, optimalidad ni ley de flujo recursiva.

## Resultados de referencia (corrida completa, N_0 ∈ {512, 1024}, 4.6 min de CPU)

- **Profundidad 1–3, (2,3), f = 1/2:** L/τ = 38.4 (N = 2048), 155.6 (N = 4096), 622.7 (N = 8192); factor de crecimiento por nivel ≈ 4.0. Para comparación, el ropelength numérico conocido del trébol es ≈ 32.7 (literatura): la construcción no está cerca de ser ajustada ni en profundidad 1.
- **Grosor:** en 36 de 36 niveles el grosor poligonal lo fija la distancia doblemente crítica, nunca el radio de curvatura; τ coincide con la estimación punto–tangente de Gonzalez–Maddocks al 0.01 %. Para f ≤ 0.35, τ(K_d) = r_d exactamente (cuatro cifras) en todas las profundidades; para f = 1/2, τ_1 = 0.4158 < 0.5 (la curvatura del toro base acerca las hebras interiores) y τ_d = r_d en d = 2, 3.
- **Hipótesis (H_c):** con c = 1/2 se cumple en los 9 niveles por defecto con f ≤ 1/2 (margen τ_d/ρ_d ≥ 1.66) y en todos los patrones probados; con c = 1 falla exactamente en un nivel (f = 1/2, d = 1, cociente 0.83). La cota de longitud del Lema 3.3 se cumple en 36 de 36 niveles.
- **Tipo de nudo:** el writhe de K_1 = T(2,3) cruza el semientero 3.5 dentro de la malla (Wr = 3.127, 3.257, 3.518, 3.710 para f = 0.25, 0.35, 0.5, 0.6), así que K_2 es el cable (2, 9) del trébol para f ≤ 0.35 pero el cable (2, 11) para f ≥ 0.5. La holonomía medida coincide con 2π·frac(Wr) como exige el Lema 3.2.
- **Convergencia:** cambio relativo máximo de L/τ y de τ entre N_0 y 2N_0: 0.03 % sobre las 12 cadenas.
- **Otros patrones (f = 1/2):** (3,2): L/τ = 47.7, 331.4, 2296.5; (2,5): 72.4, 291.4, 1166.2.

## Reproducir

```bash
python3 experiments/recursive_knots.py      # ~5 min en 4 núcleos compartidos (--fast: ~3 min con la mitad de resolución)
./manuscript/build.sh                        # requiere TeX Live (pdflatex, bibtex, latexmk)
```

Sin aleatoriedad (la semilla 20260930 solo se registra). Versiones usadas: Python 3.11, NumPy 2.4, Matplotlib para las figuras.
