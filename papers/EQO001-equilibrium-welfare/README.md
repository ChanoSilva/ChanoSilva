# EQO001 — Equilibrium operators and welfare

**Título de trabajo:** *Equilibrium Operators, Variational Inequalities and Welfare: What Is and Is Not a Theorem*  
**Línea de investigación:** EQO001 — Operadores de equilibrio y bienestar (área "Decisiones, redes y operaciones")  
**Estado:** borrador de trabajo v0.1 (30/09/2026), generado en una sesión de Claude Code a partir de la ficha pública de la línea (no existe manuscrito previo); no ha pasado aún por revisión arbitral interna.

## Qué es la línea y qué se hizo

La ficha pública de EQO001 dice que la formulación revisada "combina componentes conocidos sin establecer todavía un teorema independiente". Este borrador es la versión definitiva de esa evaluación: una nota de "qué es y qué no es un teorema" en la relación entre operadores de equilibrio $F$, desigualdades variacionales $\mathrm{VI}(F,K)$ y criterios de bienestar $W$, con demostraciones completas de lo clásico, un resultado pequeño (la caracterización del cono de pesos de bienestar bajo los cuales un equilibrio de Nash dado es óptimo), una proposición de imposibilidad ($(F,K)$ por sí solo no determina nada sobre bienestar), dos ejemplos calculados exactamente, verificación numérica con un solver de gradiente proyectado sobre juegos monótonos aleatorios con semilla fija, y dos preguntas abiertas precisas. **No se ofrece ningún concepto de equilibrio nuevo ni una "solución general de equilibrio".**

## Qué contiene

| Ruta | Contenido |
|---|---|
| `manuscript/main.tex`, `manuscript/refs.bib` | Manuscrito en LaTeX (inglés) y bibliografía (25 entradas reales). |
| `manuscript/main.pdf` | PDF compilado con pdflatex/bibtex vía latexmk. |
| `manuscript/numbers.tex`, `manuscript/table_*.tex` | Macros y cuerpos de tabla **generados** desde los resultados; ningún número del texto está tipeado a mano. |
| `experiments/vi_solver.py` | Proyecciones (caja, simplex) e iteración de gradiente proyectado $x\leftarrow\Pi_K(x-\gamma F(x))$ con paso $\gamma=\mu/L^2$ (contracción demostrada en el Teorema 3.4). |
| `experiments/traffic_poa.py` | E1: ejemplo de Pigou con $c_2=x^d$, precio de la anarquía en redes paralelas afines aleatorias, peajes de costo marginal. |
| `experiments/welfare_cone.py` | E2–E4: ejemplo de dos jugadores con cono exacto, duopolio de Cournot, modificación de Nikaidô–Isoda, juegos cuadráticos aleatorios cóncavos y no cóncavos (cono de primer orden por programación lineal; pertenencia exacta por enumeración de las $3^N$ caras de la caja). |
| `experiments/make_numbers.py` | Convierte `results/*.json` en `manuscript/numbers.tex` y las tablas. |
| `results/results_traffic.json`, `results/results_welfare.json` | Resultados completos con semilla fija. |
| `results/tables_traffic.md`, `results/tables_welfare.md` | Las mismas tablas en Markdown, para lectura rápida. |
| `figures/` | Figuras en PNG y PDF. |
| `CONTINUIDAD_EQO001_20260930.md` | Nota de continuidad interna: supuestos, decisiones, resultados de referencia, limitaciones y pendientes. |

## Resultados (corrida de referencia, semilla 20260930)

- **Lo clásico, demostrado en el texto:** potencial por lema de Poincaré en convexos y "VI = puntos estacionarios del potencial, = minimizadores si es convexo" (Beckmann–McGuire–Winsten, Rosen, Monderer–Shapley); unicidad por monotonía estricta y existencia con convergencia lineal de la iteración proyectada bajo monotonía fuerte (Kinderlehrer–Stampacchia, Facchinei–Pang); Nash ⇔ VI y Wardrop ⇔ VI; Pigou y la cota $4/3$ del precio de la anarquía para costos afines (Roughgarden–Tardos, prueba vía la propia desigualdad variacional).
- **Condición exacta para que un equilibrio sea óptimo de bienestar (Prop. 4.1):** $\nabla W(x^*)$ y $-F(x^*)$ deben estar ambos en el cono normal $N_K(x^*)$; en una cara de un simplex ambos son constantes sobre el soporte (proporcionales "en la cara de equilibrio"); si $W$ es cóncava la condición es también suficiente. Corolario: los peajes $\tau=\nabla C-F$ convierten a los minimizadores de $C$ en los equilibrios, y el conjunto de peajes constantes que sostienen un $\bar x$ es el cono trasladado $-F(\bar x)-N_K(\bar x)$ (Pigou–Knight–BMW, Hearn–Ramana).
- **Resultado pequeño (Teorema 5.1):** el conjunto $\Lambda(x^*)$ de pesos $\lambda\ge 0$ con $x^*\in\arg\max_K\sum_i\lambda_iu_i$ es siempre un cono convexo cerrado, contenido en el cono de primer orden $\Lambda_1(x^*)=\{\lambda\ge0: G(x^*)^\top\lambda\in N_K(x^*)\}$, con igualdad si los pagos son conjuntamente cóncavos; en forma por bloques, $-\lambda_jF_j(x^*)+\sum_{i\ne j}\lambda_i\nabla_{x_j}u_i(x^*)\in N_{K_j}(x_j^*)$ (en coordenadas interiores: las externalidades marginales ponderadas se anulan). La parte de escalarización es estándar (Geoffrion, Ehrgott); lo específico es la lectura en términos de $F$, la cara de equilibrio y las externalidades.
- **Imposibilidad (Prop. 5.2):** restar a cada $u_i$ su valor de mejor respuesta $v_i(x_{-i})$ (función gap de Nikaidô–Isoda) deja intactos $F$, las mejores respuestas y los equilibrios, pero hace que $x^*$ maximice todo $W_\lambda$; como Cournot tiene $\Lambda=\{0\}$, ninguna propiedad de $(F,K)$ implica ni excluye optimalidad de bienestar.
- **Ejemplo exacto (Ej. 5.3):** dos jugadores en $[0,1]^2$ con daño lineal mutuo $\beta_1,\beta_2$; el equilibrio es la esquina $(1,1)$ y el cono es la cuña $\{\beta_2\lambda_2\le\lambda_1\le\lambda_2/\beta_1\}$ (para $\alpha=2$), no trivial sii $\beta_1\beta_2\le1$. Con $\beta=1/2$: bordes en 26.57° y 63.43°; forma cerrada, test lineal y maximización exacta coinciden en 181/181 direcciones.
- **Verificación numérica:** Pigou $d=1$ da PoA $=1.333333$ exacto; 200 redes afines aleatorias: PoA máximo 1.2094, 0 violaciones de $4/3$, residuo VI máximo $3.4\times10^{-11}$, equilibrio con peajes = óptimo a $2\times10^{-16}$. Juegos aleatorios: en 200 juegos cóncavos ($N=3,4$) todos los puntos del cono probados (268/268) y de la rejilla dentro del cono (882/882) están en $\Lambda$, y todos los de fuera (24 718/24 718) fuera; en 200 juegos no cóncavos la inclusión $\Lambda\subseteq\Lambda_1$ nunca falla, pero hay testigos certificados de inclusión estricta en una fracción sustancial de los juegos con cono no trivial (véase `results/tables_welfare.md` para las cifras exactas de $N=4$).
- **Preguntas abiertas formuladas:** (1) descripción finita (de segundo orden) de $\Lambda(x^*)$ para juegos cuadráticos en poliedros, y si es siempre poliédrico; (2) el cono de pesos por mercancía en redes multi-mercancía de Wardrop.

## Reproducir

```bash
pip install -r experiments/requirements.txt
python3 experiments/traffic_poa.py        # ~5 s
python3 experiments/welfare_cone.py       # ~2 min (enumeración exacta de caras); --figures-only rehace solo las figuras
./manuscript/build.sh                      # requiere TeX Live (pdflatex, bibtex, latexmk)
```

Semilla maestra: `20260930`. Versiones usadas en la corrida de referencia: Python 3.11, NumPy 2.4, SciPy 1.17.
