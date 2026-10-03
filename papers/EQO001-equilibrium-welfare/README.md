# EQO001 — Equilibrium operators and welfare

**Título de trabajo:** *Equilibrium Operators, Variational Inequalities and Welfare: What Is and Is Not a Theorem*  
**Línea de investigación:** EQO001 — Operadores de equilibrio y bienestar (área "Decisiones, redes y operaciones")  
**Estado:** borrador de trabajo **v0.2 (03/10/2026), una ronda de revisión interna aplicada** (informe `REFEREE_EQO001_ronda1_20260930.md`, respuesta punto por punto en `RESPUESTA_EQO001_ronda1_20260930.md`). Generado en sesiones de Claude Code a partir de la ficha pública de la línea (no existe manuscrito previo). Pendiente: ronda 2 de arbitraje antes de actualizar la ficha del CV (`FICHA_EQO001_propuesta.md`).

## Qué es la línea y qué se hizo

La ficha pública de EQO001 dice que la formulación revisada "combina componentes conocidos sin establecer todavía un teorema independiente". Este borrador recoge esa evaluación: una nota de "qué es y qué no es un teorema" en la relación entre operadores de equilibrio $F$, desigualdades variacionales $\mathrm{VI}(F,K)$ y criterios de bienestar $W$, con demostraciones completas de lo clásico, un resultado pequeño (la caracterización del cono de pesos de bienestar bajo los cuales un equilibrio de Nash dado es óptimo), una proposición de imposibilidad ($(F,K)$ por sí solo no determina nada sobre bienestar), cuatro ejemplos calculados exactamente —dos de ellos negativos: el cono no es poliédrico en general, y en redes de dos mercancías no coincide con el cono de primer orden—, verificación numérica con un solver de gradiente proyectado y semilla fija, y dos preguntas abiertas reformuladas tras la revisión. **No se ofrece ningún concepto de equilibrio nuevo ni una "solución general de equilibrio".**

## Qué contiene

| Ruta | Contenido |
|---|---|
| `manuscript/main.tex`, `manuscript/refs.bib` | Manuscrito en LaTeX (inglés) y bibliografía (30 entradas reales, todas citadas; 24 verificadas por el árbitro, 6 añadidas en la v0.2). |
| `manuscript/main.pdf` | PDF compilado con pdflatex/bibtex vía latexmk (14 páginas A4 a 11 pt; véase "Extensión"). |
| `manuscript/numbers.tex`, `manuscript/table_*.tex` | Macros y cuerpos de tabla **generados** desde los resultados (148 macros); ningún número del texto está tipeado a mano, incluida la frase "all criteria hold". |
| `experiments/vi_solver.py` | Proyecciones (caja, simplex) e iteración de gradiente proyectado $x\leftarrow\Pi_K(x-\gamma F(x))$ con paso $\gamma=\mu/L^2$ (contracción demostrada en el Teorema 3.5). |
| `experiments/traffic_poa.py` | E1: ejemplo de Pigou con $c_2=x^d$, precio de la anarquía en redes paralelas afines aleatorias, peajes de costo marginal (comparados con un óptimo calculado de forma independiente por water-filling). |
| `experiments/welfare_cone.py` | E2–E4: ejemplo de dos jugadores con cono exacto, duopolio de Cournot, modificación de Nikaidô–Isoda, **E2c: ejemplo de tres jugadores con cono no poliédrico**, juegos cuadráticos aleatorios cóncavos y no cóncavos (cono de primer orden por programación lineal; pertenencia exacta por enumeración de las $3^N$ caras de la caja). |
| `experiments/commodity_cone.py` | **E5 (nuevo en v0.2):** cono de pesos por mercancía en una red de dos mercancías con costos afines: instancia fija con $\Lambda\ne\Lambda_1$ calculada a mano y 200 instancias aleatorias. |
| `experiments/make_numbers.py` | Convierte `results/*.json` en `manuscript/numbers.tex` y las tablas; genera las frases de criterios a partir de los flags `criteria` de los JSON. |
| `results/results_{traffic,welfare,commodity}.json` | Resultados completos con semilla fija, con un bloque `criteria` (valor, umbral, pass/fail) por experimento. |
| `results/tables_{traffic,welfare,commodity}.md` | Las mismas tablas y criterios en Markdown, para lectura rápida. |
| `figures/` | Figuras en PNG y PDF (`fig_cone_dims` ya no se incluye en el manuscrito; su información está en la Tabla 1). |
| `CONTINUIDAD_EQO001_20260930.md` | Nota de continuidad interna: supuestos, decisiones, resultados de referencia, limitaciones, pendientes, y la sección "Ronda 1 de revisión interna". |
| `REFEREE_EQO001_ronda1_20260930.md`, `RESPUESTA_EQO001_ronda1_20260930.md` | Informe del árbitro interno (v0.1) y respuesta del autor (v0.2). |
| `FICHA_EQO001_propuesta.md` | Propuesta de ficha (ES/EN) para el CV, coherente con la v0.2; no aplicar hasta la ronda 2. |

## Resultados (corrida de referencia v0.2, semilla 20260930)

- **Lo clásico, demostrado en el texto:** potencial por lema de Poincaré en convexos y "VI = puntos estacionarios del potencial, = minimizadores si es convexo" (Beckmann–McGuire–Winsten, Monderer–Shapley); unicidad por monotonía estricta y existencia con convergencia lineal de la iteración proyectada bajo monotonía fuerte (Kinderlehrer–Stampacchia, Facchinei–Pang); Nash ⇔ VI (Rosen) y Wardrop ⇔ VI; Pigou y la cota $4/3$ del precio de la anarquía para costos afines (Roughgarden–Tardos, prueba vía la propia desigualdad variacional).
- **Condición exacta para que un equilibrio sea óptimo de bienestar (Prop. 4.1):** $\nabla W(x^*)$ y $-F(x^*)$ deben estar ambos en el cono normal $N_K(x^*)$; en una cara de un simplex ambos son constantes sobre el soporte (paralelos cuando ninguno es cero); si $W$ es cóncava la condición es también suficiente. Corolario 4.2: los peajes $\tau=\nabla C-F$ convierten a los minimizadores de $C$ en los equilibrios, y el conjunto de peajes constantes que sostienen un $\bar x$ es el cono trasladado $-F(\bar x)-N_K(\bar x)$ (Pigou–Knight–BMW, Hearn–Ramana; optimización inversa de Ahuja–Orlin).
- **Resultado pequeño (Teorema 5.1):** el conjunto $\Lambda(x^*)$ de pesos $\lambda\ge 0$ con $x^*\in\arg\max_K\sum_i\lambda_iu_i$ es siempre un cono convexo cerrado, contenido en el cono de primer orden $\Lambda_1(x^*)=\{\lambda\ge0: G(x^*)^\top\lambda\in N_K(x^*)\}$, con igualdad si los pagos son conjuntamente cóncavos; en forma por bloques, $-\lambda_jF_j(x^*)+\sum_{i\ne j}\lambda_i\nabla_{x_j}u_i(x^*)\in N_{K_j}(x_j^*)$ (en coordenadas interiores: las externalidades marginales ponderadas se anulan). La escalarización es estándar (Geoffrion, Ehrgott; conjunto de pesos de Benson–Sun) y el caso interior es el mecanismo de la ineficiencia genérica de Dubey (1986); lo que se añade es la lectura en términos de $F$, la cara de equilibrio y las externalidades (Remark 5.2).
- **Imposibilidad (Prop. 5.3):** restar a cada $u_i$ su valor de mejor respuesta $v_i(x_{-i})$ (función gap de Nikaidô–Isoda) deja intactos $F$, las mejores respuestas y los equilibrios, pero hace que $x^*$ maximice todo $W_\lambda$; con mejor respuesta única, Danskin da $v_i\in C^1$ y externalidades marginales nulas en $x^*$. Como Cournot tiene $\Lambda=\{0\}$, ninguna propiedad de $(F,K)$ implica ni excluye optimalidad de bienestar.
- **Ejemplo exacto (Ej. 5.4):** dos jugadores en $[0,1]^2$ con daño lineal mutuo $\beta_1,\beta_2$; el equilibrio es la esquina $(1,1)$ y el cono es la cuña $\{(\alpha-1)\lambda_1\ge\beta_2\lambda_2,\ (\alpha-1)\lambda_2\ge\beta_1\lambda_1\}$, no trivial sii $\beta_1\beta_2\le(\alpha-1)^2$. Con $\alpha=2$, $\beta=1/2$: bordes en 26.57° y 63.43°; forma cerrada, test lineal y maximización exacta coinciden en 181/181 direcciones (73 dentro del cono).
- **El cono no es poliédrico en general (Ej. 5.6, contraejemplo señalado en la revisión interna):** $u_1=x_1$, $u_2=x_2$, $u_3=x_3-\tfrac12x_1^2+\tfrac14x_1+\tfrac12x_1x_2-\tfrac12x_2$ en $[0,1]^3$, $x^*=(1,1,1)$; en la rebanada $\lambda_3=1$, $\Lambda=\{\lambda_1\ge\tfrac14,\ \lambda_2\ge\tfrac12(\tfrac34-\lambda_1)_+^2\}$ (frontera parabólica) mientras $\Lambda_1=\{\lambda_1\ge\tfrac14\}$. Verificado (E2c): 0 discrepancias en 7 381 puntos, frontera por bisección a $10^{-8}$ de la parábola, testigo $(0.3,0,1)$ con brecha $0.10125$; la variante fuertemente monótona ($\varepsilon=0.2$) conserva la frontera curva.
- **$\Lambda\ne\Lambda_1$ en redes de dos mercancías con costos afines (Ej. 5.7, nuevo):** enlace privado $f+2$ y compartido $f$ para la mercancía 1, privado $f/4$ y el mismo compartido para la 2; equilibrio de Wardrop $f^*=(1,0)$ con $\Lambda_1(f^*)=\mathbb R^2_+$ pero $\Lambda(f^*)=\{\lambda_2\le40\lambda_1\}$; para $\lambda=(0,1)$ el flujo $(0,1/5)$ baja $C_2$ de $1/4$ a $1/5$. Verificado (E5a): umbral por bisección $0.025000$, brecha $0.0500$. E5b: en 200 instancias aleatorias, 21 tienen testigo certificado de $\Lambda\ne\Lambda_1$ y ninguna viola $\Lambda\subseteq\Lambda_1$.
- **Verificación numérica (todos los criterios pasan, 5 + 12 + 5):** Pigou $d=1$ da PoA $=1.333333$ exacto; 200 redes afines aleatorias: PoA máximo 1.2094, media 1.0305, mediana 1.0027 (86/200 con PoA $=1$ exacto), 0 violaciones de $4/3$, residuo VI máximo $3.4\times10^{-11}$, equilibrio con peajes (solver) = óptimo por water-filling independiente a $8.8\times10^{-11}$. Juegos aleatorios: en 200 juegos cóncavos ($N=3,4$) todos los puntos del cono probados (268/268) y de la rejilla dentro del cono (882/882) están en $\Lambda$, y todos los de fuera (24 718/24 718) fuera; en 200 juegos no cóncavos la inclusión $\Lambda\subseteq\Lambda_1$ nunca falla y 58 de los 103 con cono no trivial (**al menos** 56 %; los testigos sólo se buscan en los puntos del cono) tienen testigo certificado de inclusión estricta (`results/tables_welfare.md`).
- **Preguntas abiertas (reformuladas):** (1) caracterizar, en términos del patrón de caras activas y los hessianos, cuándo $\Lambda=\Lambda_1$ y cuándo $\Lambda$ es poliédrico sin concavidad conjunta, y la complejidad de decidir $\lambda\in\Lambda(x^*)$ ($\Lambda$ es siempre semialgebraico por Tarski–Seidenberg; $N=2$ es trivial); (2) el cono de pesos por mercancía para $m\ge3$ mercancías y las estructuras de red con $\Lambda=\Lambda_1$.

## Extensión

v0.1: 13 páginas. v0.2: 14 páginas a 11 pt con márgenes de 1 in, tras aplicar los recortes del informe (resumen ≤ 200 palabras, protocolos a un apéndice, tabla de Pigou y figura de dimensiones fuera, Remark 3.3 y "Contributions" comprimidos, demostración de la proyección reducida a una línea). Los recortes (≈ −2.5 páginas) quedaron compensados por lo que la propia revisión pidió añadir: dos ejemplos demostrados (5.6 y 5.7, ≈ 1.2 páginas), el experimento E5, la observación de Danskin, el Remark 5.2 sobre literatura y el apéndice de criterios. No se bajó de 10 páginas sin perder demostraciones; no se cambió el tamaño de letra ni los márgenes para cumplir la meta.

## Reproducir

```bash
pip install -r experiments/requirements.txt
python3 experiments/traffic_poa.py        # ~3 s
python3 experiments/welfare_cone.py       # ~80-130 s (enumeración exacta de caras); --figures-only rehace solo las figuras
python3 experiments/commodity_cone.py     # ~4 s
./manuscript/build.sh                      # requiere TeX Live (pdflatex, bibtex, latexmk)
```

Semilla maestra: `20260930`, consumida secuencialmente por un único generador en cada script (reproducible; reordenar los experimentos cambia las instancias). Versiones usadas en la corrida de referencia: Python 3.11, NumPy 2.4, SciPy 1.17. Cada script evalúa sus criterios (docstring) y escribe `criteria.all_pass` en su JSON; no existe registro externo de prerregistro.
