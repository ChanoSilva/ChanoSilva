# RTK001 — Geometry of Recursive Knots

**Título de trabajo:** *Geometry of Recursive Knots: Iterated Cables by Frame Offsets, Their Thickness and Ropelength*  
**Línea de investigación:** RTK001 — Geometría de nudos recursivos (área "Matemáticas y estructuras")  
**Estado:** borrador de trabajo **v0.3, dos rondas de revisión interna aplicadas** (03/10/2026; v0.2 del 03/10/2026, v0.1 del 30/09/2026), generado en sesiones de Claude Code a partir de la ficha pública de la línea. **No existía ningún manuscrito previo**; la familia de curvas, las definiciones y el protocolo se fijaron en v0.1 (véase la nota de continuidad). Los informes de revisión (`REFEREE_RTK001_ronda1_20260930.md`, `REFEREE_RTK001_ronda2_20261003.md`) y las respuestas punto por punto (`RESPUESTA_RTK001_ronda1_20260930.md`, `RESPUESTA_RTK001_ronda2_20261003.md`) están en esta carpeta. En la ronda 2 se integró además el caso "misma hebra" demostrado en `theory/` (verificado por el autor antes de integrarlo).

## Qué contiene

| Ruta | Contenido |
|---|---|
| `manuscript/main.tex`, `manuscript/refs.bib` | Manuscrito en LaTeX (inglés, 12 páginas a 10 pt) y bibliografía (14 entradas). |
| `manuscript/main.pdf` | PDF compilado (pdflatex + bibtex vía latexmk; sin errores, sin referencias ni citas indefinidas, sin cajas desbordadas). |
| `manuscript/numbers.tex`, `manuscript/table_main.tex` | Macros y cuerpo de tabla **generados** solo desde `results/*.json` (desde v0.3 nada se lee de `theory/`); ningún número del texto está tipeado a mano. |
| `manuscript/build.sh` | Regenera macros y compila. |
| `experiments/recursive_knots.py` | Construye los polígonos K_0..K_3 (cables iterados por desplazamiento en un marco de Bishop cerrado) y mide longitud, minRad, distancia doblemente crítica, grosor poligonal, ropelength, writhe, holonomía y el número de enlace del marco Lk = rint(Wr − α/2π) con su residuo. |
| `experiments/aux_checks.py` | Comprobaciones añadidas en la ronda 1: geometría del par crítico en d = 1, cruce de 3.5 del writhe (bisección), contraste segmento–segmento frente al proxy de vértices. |
| `experiments/shrink.py` | Sonda opcional: acortamiento de curva discreto sobre K_1 y K_2 con seguimiento de L/τ (no certificada). |
| `experiments/check_Hc.py`, `experiments/check_same_strand.py` | Copias congeladas (v0.3) de los scripts de `theory/` (solo cambian rutas): evalúan en los polígonos las constantes de la §3 y comprueban cada desigualdad intermedia de las pruebas. Salidas en `results/check_*` (idénticas byte a byte a las de `theory/`; SHA-256 en `results/FROZEN_THEORY_SHA256.txt`). |
| `experiments/classify_pairs.py` | Censo de pares doblemente críticos de las cadenas (2,3) (mínimos locales y celdas de cambio de signo; clases mismo disco / lejano / hebra distinta / misma hebra) y márgenes de la Conjetura 3.19 → `results/classify_pairs.{json,md}`. |
| `experiments/corollary_chain.py` | Cadena del Corolario 3.16 (r_d = f ρ_{d−1}) → `results/corollary_chain.json`. |
| `experiments/make_numbers.py` | Convierte los JSON de `results/` en `numbers.tex`, la tabla y `results/convergence.md`; falla si falta un insumo. |
| `results/results.json`, `results/tables.md`, `results/convergence.md` | Resultados completos (determinista; semilla 20260930 solo como registro) y comprobación de resolución por nivel. |
| `results/aux_checks.json`, `results/results_shrink.json`, `results/tables_shrink.md` | Resultados de las comprobaciones auxiliares y de la sonda de acortamiento. |
| `theory/Hc_derivation.md`, `theory/Hc_lemma.tex`, `theory/same_strand_derivation.md`, `theory/same_strand_lemma.tex`, `theory/check_*.py` y salidas | Derivaciones de la cota de grosor (p = 2): hebras distintas y curvatura (ronda 1) y misma hebra (ronda 2), versiones LaTeX previas a la integración y sus verificaciones numéricas (originales; el manuscrito usa las copias congeladas de `experiments/` y `results/`). |
| `figures/fig_curves.*`, `figures/fig_rop.*` | Proyecciones de K_1, K_2, K_3 y crecimiento de L/τ con la profundidad. |
| `PLAN.md` | Plan de una página escrito al inicio de la sesión v0.1. |
| `CONTINUIDAD_RTK001_20260930.md` | Nota de continuidad: supuestos, decisiones, limitaciones, pendientes, y la sección de la ronda 1. |
| `FICHA_RTK001_propuesta.md` | Propuesta de actualización de la ficha pública (v0.3). |
| `REFEREE_RTK001_ronda{1,2}_*.md`, `RESPUESTA_RTK001_ronda{1,2}_*.md` | Informes de arbitraje interno y respuestas del autor. |

## Idea del paper en tres líneas

1. Se fija una familia concreta de "nudos recursivos": K_0 es un círculo; K_d es el patrón tórico (p_d, q_d) colocado sobre el tubo de radio r_d alrededor de K_{d−1}, usando un marco de Bishop (de rotación mínima) cerrado con un giro lineal. Por defecto (p, q) = (2, 3) y r_d = f · grosor(K_{d−1}).
2. Se demuestra lo elemental: K_d es una curva cerrada suave y embebida si r_d < grosor(K_{d−1}) (Lema 3.1); el marco cerrado tiene número de enlace Wr − α/2π con su núcleo, lo que identifica K_d como el cable (p, q + p·Lk) de K_{d−1} (Lema 3.2); p L(K_{d−1})(1 − r κ_max) ≤ L(K_d) ≤ p L(K_{d−1})(1 + r κ_max) + r(2πq + p|α|) (Lema 3.3); y, para p = 2, grosor(K_d) ≤ r_d, de donde Rop(K_d) ≥ L(K_d)/r_d (Prop. 3.5, cota inferior interna a la familia). De la cota inferior grosor(K_d) ≥ min(τ − r, c r sin(π/p)) con p = 2: en la familia (2,3) con f ≤ 1/2 **todo par doblemente crítico** de K_d con bases distintas —en hebras distintas (Lema 3.7, constante c_1 ≥ 1/2) o en la misma hebra (Prop. 3.10 y Cor. 3.11, c_0′ ≥ 1/2, por un argumento de giro obtenido en la ronda 2)— está a distancia ≥ min(2(τ − r), r), **en toda profundidad y sin hipótesis adicionales**. Por tanto (H_c) con c = 1/2 queda **demostrada en d = 1** (grosor(K_1) ≥ r_1/2 para todo f ≤ 1/2) y, para d ≥ 2, **reducida a la cota de curvatura** minRad(K_d) ≥ r_d/2, que se deduce de una hipótesis (H_3) sobre las derivadas de la velocidad y del vector de curvatura del marco paralelo de la base (Props. 3.8 y 3.12, Teorema 3.13); las constantes de (H_3) solo se miden en los polígonos (evaluación en malla, no certificada), y sin (H_3) ninguna constante funciona para una base arbitraria (Obs. 3.14). Bajo (H_c), Rop_d ≤ 2π Λ^d con Λ = A/γ explícito (Λ = 20 para (2,3), f = 1/2, c = 1/2; Λ = 10 con c = 1).
3. Numéricamente, polígonos explícitos de hasta 8192 vértices dan L/τ = 38.4, 155.6 y 622.7 en profundidades 1, 2, 3 (patrón (2,3), f = 1/2), estables al 0.03 % al duplicar la resolución. Son cotas superiores verificadas numéricamente para polígonos explícitos, no grosores suaves certificados. No se afirma estacionariedad, optimalidad ni ley de flujo recursiva.

## Resultados de referencia (corrida completa, N_0 ∈ {512, 1024}, 3.1 min de pared / 3.1 min de CPU; comprobaciones auxiliares 33 s; sonda de acortamiento 5.1 min adicionales, v0.1; ronda 2: `check_Hc.py` 57 s, `check_same_strand.py` 25 s, `classify_pairs.py` 49 s de CPU, `corollary_chain.py` 26 s de CPU, de pared en núcleos compartidos salvo indicación)

- **Profundidad 1–3, (2,3), f = 1/2:** L/τ = 38.4 (N = 2048), 155.6 (N = 4096), 622.7 (N = 8192); cocientes Rop_d/Rop_{d−1} = 4.06 y 4.00, que tienden a p/f = 4 como consecuencia de τ_d = r_d (no es una constante empírica independiente). Cota inferior interna a la familia: Rop_d ≥ 2π·2^d = 12.6 / 25.1 / 50.3. Para comparación, el ropelength numérico conocido del trébol es ≈ 32.7 (literatura, no certificado): la construcción no está cerca de ser ajustada ni en profundidad 1.
- **Grosor:** en 36 de 36 niveles el grosor poligonal lo fija la distancia doblemente crítica, nunca el radio de curvatura (minRad/r_d ≥ 1.15); τ coincide con la estimación punto–tangente de Gonzalez–Maddocks al 0.01 % y el contraste segmento–segmento da cocientes ≥ 0.9999. Para f ≤ 0.35, τ(K_d) = r_d exactamente (cuatro cifras) en todas las profundidades; para f = 1/2, τ_1 = 0.4158 < 0.5, realizado por un par **a través del agujero del toro** (bases a 103.7°, no un par local), y τ_d = r_d en d = 2, 3.
- **Cota de grosor (H_c):** con la constante natural c = 1 la desigualdad falla en 4 de los 15 niveles con f ≤ 1/2 ((2,3) f = 0.5 d = 1: 0.832; (3,2) d = 1: 0.968; (3,2) d = 2: 0.999, estable al duplicar N; (2,5) d = 1: 0.564) y se alcanza con igualdad (tolerancia común 0.05 %) donde τ_d = r_d; con c = 1/2 (elegida **después** de ver fallar c = 1) se cumple en los 9 niveles por defecto con margen ≥ 1.66, y también a lo largo de la cadena del Corolario (margen ≥ 1.66). **Demostrado (analítico):** c_1 ≥ 1/2 y c_0′ ≥ 1/2 en toda profundidad de (2,3), f ≤ 1/2; en d = 1 además 1/(r κ̄_1) > 0.561, luego grosor(K_1) ≥ r_1/2. **Evaluado en malla (no certificado):** c_1 ≈ 0.6117 (d = 1, f = 1/2); c_0′ = 0.509 / 0.845 / 0.988 y 1/(r κ̂_d) = 1.419 / 1.034 / 0.998 en f = 1/2, d = 1 / 2 / 3 (en d = 2, 3 con τ, v, M_v, M_κ medidos en los polígonos). **Abierto:** (H_3) uniforme en d y la certificación por intervalos.
- **Pares críticos (censo propio, `classify_pairs.py`, 18 niveles):** ningún par doblemente crítico de vértices (mínimo local) en la misma hebra; con un test de cambio de signo que también detecta sillas y máximos, pares de misma hebra solo en d = 1 (δ ≥ 1.96 > δ_turn = 1.068, distancia ≥ 3.70 r en f = 1/2) y ninguno en d = 2, 3. En f = 1/2, d = 2, 3 el siguiente par doblemente crítico tras los antipodales de un disco está solo un 1.4 % y un 2.1 % más lejos que 2r_d (1.4 % y 2.0 % con N_0 = 512): τ_d = r_d se decide por poco (Conjetura 3.19, umbral f_*(d)).
- **Tipo de nudo:** el writhe de la configuración K_1 cruza el semientero 3.5 dentro de la malla (Wr = 3.127, 3.257, 3.518, 3.710 para f = 0.25, 0.35, 0.5, 0.6; cruce en r* = 0.4904), así que K_2 es el cable (2, 9) del trébol para f ≤ 0.35 pero el cable (2, 11) para f ≥ 0.5. Residuo máximo de Wr_{d−1} − α_d/2π respecto del entero: 1.1·10⁻³ (resolución fina), como exige el Lema 3.2.
- **Convergencia:** cambio relativo máximo de L/τ y de τ entre N_0 y 2N_0: 0.03 % sobre las 12 cadenas; el writhe cambia ≤ 10⁻⁴ en d = 1 de la familia por defecto pero hasta 0.031 en d = 3 de (3,2).
- **Otros patrones (f = 1/2):** (3,2): L/τ = 47.7, 331.4, 2296.5; (2,5): 72.4, 291.4, 1166.2.
- **Sonda de acortamiento (no certificada, N_0 = 512, 200 pasos, λ = 0.1):** en K_1, L/τ baja de 38.36 a 38.05 (0.8 %, aún decreciendo en el paso 200); en K_2 ningún paso mejora: sube monótonamente de 155.59 a 156.25.

## Reproducir

```bash
python3 experiments/recursive_knots.py      # ~3 min (--fast: ~1 min con la mitad de resolución)
python3 experiments/aux_checks.py           # ~30 s
python3 experiments/check_Hc.py             # ~1 min; constantes del Lema 3.7 / Prop. 3.8 y desigualdades intermedias
python3 experiments/check_same_strand.py    # ~25 s; constantes de la Prop. 3.10, Cor. 3.11, Prop. 3.12
python3 experiments/classify_pairs.py       # ~50 s; censo de pares doblemente críticos y márgenes
python3 experiments/corollary_chain.py      # ~30 s; cadena del Corolario 3.16
python3 experiments/shrink.py               # ~5 min; sonda opcional
./manuscript/build.sh                        # requiere TeX Live (pdflatex, bibtex, latexmk)
sha256sum -c <(grep -v '^#' results/FROZEN_THEORY_SHA256.txt)   # comprueba la evaluación congelada
```

Sin aleatoriedad (la semilla 20260930 solo se registra). Versiones usadas: Python 3.11, NumPy 2.4, Matplotlib para las figuras.
