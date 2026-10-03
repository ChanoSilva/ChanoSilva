# RTK001 — Geometry of Recursive Knots

**Título de trabajo:** *Geometry of Recursive Knots: Iterated Cables by Frame Offsets, Their Thickness and Ropelength*  
**Línea de investigación:** RTK001 — Geometría de nudos recursivos (área "Matemáticas y estructuras")  
**Estado:** borrador de trabajo **v0.2, una ronda de revisión interna aplicada** (03/10/2026; v0.1 del 30/09/2026), generado en sesiones de Claude Code a partir de la ficha pública de la línea. **No existía ningún manuscrito previo**; la familia de curvas, las definiciones y el protocolo se fijaron en v0.1 (véase la nota de continuidad). La ronda 1 de revisión (`REFEREE_RTK001_ronda1_20260930.md`) y la respuesta punto por punto (`RESPUESTA_RTK001_ronda1_20260930.md`) están en esta carpeta.

## Qué contiene

| Ruta | Contenido |
|---|---|
| `manuscript/main.tex`, `manuscript/refs.bib` | Manuscrito en LaTeX (inglés, 11 páginas a 10 pt) y bibliografía (12 entradas). |
| `manuscript/main.pdf` | PDF compilado (pdflatex + bibtex vía latexmk; sin errores, sin referencias ni citas indefinidas, sin cajas desbordadas). |
| `manuscript/numbers.tex`, `manuscript/table_main.tex` | Macros y cuerpo de tabla **generados** desde `results/*.json` y `theory/check_Hc_summary.json`; ningún número del texto está tipeado a mano. |
| `manuscript/build.sh` | Regenera macros y compila. |
| `experiments/recursive_knots.py` | Construye los polígonos K_0..K_3 (cables iterados por desplazamiento en un marco de Bishop cerrado) y mide longitud, minRad, distancia doblemente crítica, grosor poligonal, ropelength, writhe, holonomía y el número de enlace del marco Lk = rint(Wr − α/2π) con su residuo. |
| `experiments/aux_checks.py` | Comprobaciones añadidas en la ronda 1: geometría del par crítico en d = 1, cruce de 3.5 del writhe (bisección), contraste segmento–segmento frente al proxy de vértices. |
| `experiments/shrink.py` | Sonda opcional: acortamiento de curva discreto sobre K_1 y K_2 con seguimiento de L/τ (no certificada). |
| `experiments/make_numbers.py` | Convierte los JSON en `numbers.tex`, la tabla y `results/convergence.md`. |
| `results/results.json`, `results/tables.md`, `results/convergence.md` | Resultados completos (determinista; semilla 20260930 solo como registro) y comprobación de resolución por nivel. |
| `results/aux_checks.json`, `results/results_shrink.json`, `results/tables_shrink.md` | Resultados de las comprobaciones auxiliares y de la sonda de acortamiento. |
| `theory/Hc_derivation.md`, `theory/Hc_lemma.tex`, `theory/check_Hc.py`, `theory/check_Hc_output.txt`, `theory/check_Hc_summary.json` | Derivación de la parte demostrada de la cota de grosor (p = 2), versión LaTeX previa a la integración, y su verificación numérica en los polígonos. |
| `figures/fig_curves.*`, `figures/fig_rop.*` | Proyecciones de K_1, K_2, K_3 y crecimiento de L/τ con la profundidad. |
| `PLAN.md` | Plan de una página escrito al inicio de la sesión v0.1. |
| `CONTINUIDAD_RTK001_20260930.md` | Nota de continuidad: supuestos, decisiones, limitaciones, pendientes, y la sección de la ronda 1. |
| `FICHA_RTK001_propuesta.md` | Propuesta de actualización de la ficha pública (v0.2). |
| `REFEREE_RTK001_ronda1_20260930.md`, `RESPUESTA_RTK001_ronda1_20260930.md` | Informe de arbitraje interno y respuesta del autor. |

## Idea del paper en tres líneas

1. Se fija una familia concreta de "nudos recursivos": K_0 es un círculo; K_d es el patrón tórico (p_d, q_d) colocado sobre el tubo de radio r_d alrededor de K_{d−1}, usando un marco de Bishop (de rotación mínima) cerrado con un giro lineal. Por defecto (p, q) = (2, 3) y r_d = f · grosor(K_{d−1}).
2. Se demuestra lo elemental: K_d es una curva cerrada suave y embebida si r_d < grosor(K_{d−1}) (Lema 3.1); el marco cerrado tiene número de enlace Wr − α/2π con su núcleo, lo que identifica K_d como el cable (p, q + p·Lk) de K_{d−1} (Lema 3.2); p L(K_{d−1})(1 − r κ_max) ≤ L(K_d) ≤ p L(K_{d−1})(1 + r κ_max) + r(2πq + p|α|) (Lema 3.3); y, para p = 2, grosor(K_d) ≤ r_d, de donde Rop(K_d) ≥ L(K_d)/r_d (Prop. 3.5, cota inferior interna a la familia). De la cota inferior del grosor, grosor(K_d) ≥ min(τ − r, c r sin(π/p)), se demuestra la parte de pares en hebras distintas (p = 2) con constante c_1 ≥ 0.61 en toda la familia (2,3) con f ≤ 1/2 (Lema 3.7); la curvatura y los pares en la misma hebra se controlan solo bajo una hipótesis (H_3) sobre |K'|' y |κ'| de la base (Props. 3.8–3.9, Teorema 3.10), y se demuestra que sin ella ninguna constante funciona para una base arbitraria (Obs. 3.11: la hipótesis de v0.1 era falsa tal como estaba). Lo que queda sin demostrar es la Hipótesis (H_c) sobre la familia (caso misma hebra en f = 1/2; uniformidad en d), verificada numéricamente; bajo ella, Rop_d ≤ 2π Λ^d con Λ = A/γ explícito (Λ = 20 para (2,3), f = 1/2, c = 1/2; Λ = 10 con c = 1).
3. Numéricamente, polígonos explícitos de hasta 8192 vértices dan L/τ = 38.4, 155.6 y 622.7 en profundidades 1, 2, 3 (patrón (2,3), f = 1/2), estables al 0.03 % al duplicar la resolución. Son cotas superiores verificadas numéricamente para polígonos explícitos, no grosores suaves certificados. No se afirma estacionariedad, optimalidad ni ley de flujo recursiva.

## Resultados de referencia (corrida completa, N_0 ∈ {512, 1024}, 3.1 min de pared / 3.1 min de CPU; comprobaciones auxiliares 33 s; verificación de la teoría 36 s; sonda de acortamiento 5.1 min adicionales, v0.1)

- **Profundidad 1–3, (2,3), f = 1/2:** L/τ = 38.4 (N = 2048), 155.6 (N = 4096), 622.7 (N = 8192); cocientes Rop_d/Rop_{d−1} = 4.06 y 4.00, que tienden a p/f = 4 como consecuencia de τ_d = r_d (no es una constante empírica independiente). Cota inferior interna a la familia: Rop_d ≥ 2π·2^d = 12.6 / 25.1 / 50.3. Para comparación, el ropelength numérico conocido del trébol es ≈ 32.7 (literatura, no certificado): la construcción no está cerca de ser ajustada ni en profundidad 1.
- **Grosor:** en 36 de 36 niveles el grosor poligonal lo fija la distancia doblemente crítica, nunca el radio de curvatura (minRad/r_d ≥ 1.15); τ coincide con la estimación punto–tangente de Gonzalez–Maddocks al 0.01 % y el contraste segmento–segmento da cocientes ≥ 0.9999. Para f ≤ 0.35, τ(K_d) = r_d exactamente (cuatro cifras) en todas las profundidades; para f = 1/2, τ_1 = 0.4158 < 0.5, realizado por un par **a través del agujero del toro** (bases a 103.7°, no un par local), y τ_d = r_d en d = 2, 3.
- **Cota de grosor (H_c):** con la constante natural c = 1 la desigualdad falla en 4 de los 15 niveles con f ≤ 1/2 ((2,3) f = 0.5 d = 1: 0.832; (3,2) d = 1: 0.968; (3,2) d = 2: 0.999; (2,5) d = 1: 0.564) y se alcanza con igualdad donde τ_d = r_d; con c = 1/2 (constante elegida **después** de ver fallar c = 1) se cumple en los 9 niveles por defecto con margen ≥ 1.66. Parte demostrada: hebras distintas con c_1 = 0.61 (toda la familia (2,3), f ≤ 1/2); con c = 1/2 todo el enunciado para f ≤ 0.35 (incondicional en d = 1, bajo (H_3) con constantes medidas en d = 2, 3); constantes demostradas en f = 1/2 para misma hebra: 0.32 / 0.13 / 0.16 (abierto).
- **Tipo de nudo:** el writhe de la configuración K_1 cruza el semientero 3.5 dentro de la malla (Wr = 3.127, 3.257, 3.518, 3.710 para f = 0.25, 0.35, 0.5, 0.6; cruce en r* = 0.4904), así que K_2 es el cable (2, 9) del trébol para f ≤ 0.35 pero el cable (2, 11) para f ≥ 0.5. Residuo máximo de Wr_{d−1} − α_d/2π respecto del entero: 1.1·10⁻³ (resolución fina), como exige el Lema 3.2.
- **Convergencia:** cambio relativo máximo de L/τ y de τ entre N_0 y 2N_0: 0.03 % sobre las 12 cadenas; el writhe cambia ≤ 10⁻⁴ en d = 1 de la familia por defecto pero hasta 0.031 en d = 3 de (3,2).
- **Otros patrones (f = 1/2):** (3,2): L/τ = 47.7, 331.4, 2296.5; (2,5): 72.4, 291.4, 1166.2.
- **Sonda de acortamiento (no certificada, N_0 = 512, 200 pasos, λ = 0.1):** en K_1, L/τ baja de 38.36 a 38.05 (0.8 %, aún decreciendo en el paso 200); en K_2 ningún paso mejora: sube monótonamente de 155.59 a 156.25.

## Reproducir

```bash
python3 experiments/recursive_knots.py      # ~3 min (--fast: ~1 min con la mitad de resolución)
python3 experiments/aux_checks.py           # ~30 s
python3 theory/check_Hc.py                  # ~40 s; constantes del Teorema 3.10 y verificación de las desigualdades intermedias
python3 experiments/shrink.py               # ~5 min; sonda opcional
./manuscript/build.sh                        # requiere TeX Live (pdflatex, bibtex, latexmk)
```

Sin aleatoriedad (la semilla 20260930 solo se registra). Versiones usadas: Python 3.11, NumPy 2.4, Matplotlib para las figuras.
