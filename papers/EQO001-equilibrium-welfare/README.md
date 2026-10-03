# EQO001 — Equilibrium operators and welfare

**Título de trabajo:** *Equilibrium Operators, Variational Inequalities and Welfare: What Is and Is Not a Theorem*  
**Línea de investigación:** EQO001 — Operadores de equilibrio y bienestar (área "Decisiones, redes y operaciones")  
**Estado:** borrador de trabajo **v0.3 (3 October 2026), dos rondas de revisión interna aplicadas** (informes `REFEREE_EQO001_ronda1_20260930.md` y `REFEREE_EQO001_ronda2_20261003.md`; respuestas punto por punto en `RESPUESTA_EQO001_ronda1_20260930.md` y `RESPUESTA_EQO001_ronda2_20261003.md`). Generado en sesiones de Claude Code a partir de la ficha pública de la línea (no existe manuscrito previo). La propuesta de ficha del CV (`FICHA_EQO001_propuesta.md`) está actualizada a la v0.3 y queda a decisión del autor.

## Qué es la línea y qué se hizo

La ficha pública de EQO001 dice que la formulación revisada "combina componentes conocidos sin establecer todavía un teorema independiente". Este borrador recoge esa evaluación: una nota de "qué es y qué no es un teorema" en la relación entre operadores de equilibrio $F$, desigualdades variacionales $\mathrm{VI}(F,K)$ y criterios de bienestar $W$, con demostraciones completas de lo clásico, un resultado pequeño (la caracterización del cono de pesos de bienestar bajo los cuales un equilibrio de Nash dado es óptimo), una proposición de imposibilidad ($(F,K)$ por sí solo no determina el cono de pesos), cinco ejemplos calculados exactamente —tres negativos: el cono no es poliédrico en general (tres jugadores, también con $F$ fuertemente monótono; tres mercancías con costos afines) y en redes de dos mercancías no coincide con el cono de primer orden—, la co-NP-completitud de decidir la pertenencia al cono, verificación numérica con semilla fija y una única pregunta abierta concreta. **No se ofrece ningún concepto de equilibrio nuevo ni una "solución general de equilibrio".**

## Qué contiene

| Ruta | Contenido |
|---|---|
| `manuscript/main.tex`, `manuscript/refs.bib` | Manuscrito en LaTeX (inglés) y bibliografía (34 entradas reales, todas citadas: 24 verificadas en la ronda 1, 6 añadidas en la v0.2, 4 en la v0.3 —Morris–Ui 2004 y Vavasis 1990, cotejadas en línea; Karp 1972 y Schrijver 1986, por conocimiento del autor—). |
| `manuscript/main.pdf` | PDF compilado con pdflatex/bibtex vía latexmk (13 páginas A4 a 11 pt; véase "Extensión"). |
| `manuscript/numbers.tex`, `manuscript/table_random.tex` | Macros y cuerpo de tabla **generados** desde los resultados (177 `\newcommand`, incluidos los indicadores `\Has*`); ningún número del texto está tipeado a mano, incluida la frase "all criteria hold". |
| `experiments/vi_solver.py` | Proyecciones (caja, simplex) e iteración de gradiente proyectado $x\leftarrow\Pi_K(x-\gamma F(x))$ con paso $\gamma=\mu/L^2$ (contracción demostrada en el Teorema 3.5). |
| `experiments/traffic_poa.py` | E1: ejemplo de Pigou con $c_2=x^d$, precio de la anarquía en redes paralelas afines aleatorias, peajes de costo marginal (comparados con un óptimo calculado de forma independiente por water-filling). |
| `experiments/welfare_cone.py` | E2–E4: ejemplo de dos jugadores con cono exacto, duopolio de Cournot, modificación de Nikaidô–Isoda, **E2c: ejemplo de tres jugadores con cono no poliédrico**, juegos cuadráticos aleatorios cóncavos y no cóncavos (cono de primer orden por programación lineal; pertenencia exacta por enumeración de las $3^N$ caras de la caja). |
| `experiments/commodity_cone.py` | E5: cono de pesos por mercancía en una red de dos mercancías con costos afines: instancia fija con $\Lambda\ne\Lambda_1$ calculada a mano y 200 instancias aleatorias (v0.3: desglose por patrón de caras, dimensión de $\Lambda_1$ por programación lineal, testigos de eje frente a interiores). |
| `experiments/hardness_maxcut.py` | **E6 (nuevo en v0.3):** comprobación por fuerza bruta de la reducción desde MAX-CUT de la Proposición 5.9 (todos los grafos de 3–5 nodos con pesos unitarios y muestras de grafos de 6 nodos). |
| `experiments/three_commodity.py` | **E7 (nuevo en v0.3):** el ejemplo de tres mercancías con cono no poliédrico (Ej. 5.8). |
| `experiments/make_numbers.py` | Convierte `results/*.json` en `manuscript/numbers.tex` y las tablas; genera las frases de criterios a partir de los flags `criteria` de los JSON. |
| `results/results_{traffic,welfare,commodity}.json` | Resultados completos con semilla fija, con un bloque `criteria` (valor, umbral, pass/fail) por experimento. |
| `results/tables_{traffic,welfare,commodity}.md` | Las mismas tablas y criterios en Markdown, para lectura rápida. |
| `results/CLAIMS.md` | Tabla de afirmaciones y su estado (sacada del manuscrito en la v0.3 por extensión). |
| `figures/` | Figuras en PNG y PDF; desde la v0.3 ninguna se incluye en el manuscrito (se remiten por ruta): `fig_cone_2player` (Ej. 5.4), `fig_poa` (histograma de E1; el panel de Pigou contra $d$ se eliminó), `fig_cone_dims`. |
| `CONTINUIDAD_EQO001_20260930.md` | Nota de continuidad interna: supuestos, decisiones, resultados de referencia, limitaciones, pendientes, y la sección "Ronda 1 de revisión interna". |
| `REFEREE_EQO001_ronda{1,2}_*.md`, `RESPUESTA_EQO001_ronda{1,2}_*.md` | Informes de los árbitros internos (v0.1, v0.2) y respuestas del autor (v0.2, v0.3). |
| `FICHA_EQO001_propuesta.md` | Propuesta de ficha (ES/EN) para el CV, coherente con la v0.3. |

## Resultados (corrida de referencia v0.3, semilla 20260930)

- **Lo clásico, demostrado en el texto:** potencial por lema de Poincaré en convexos y "VI = puntos estacionarios del potencial, = minimizadores si es convexo" (Beckmann–McGuire–Winsten, Monderer–Shapley); unicidad por monotonía estricta y existencia con convergencia lineal de la iteración proyectada bajo monotonía fuerte (Kinderlehrer–Stampacchia, Facchinei–Pang); Nash ⇔ VI (Rosen) y Wardrop ⇔ VI; Pigou y la cota $4/3$ del precio de la anarquía para costos afines (Roughgarden–Tardos, prueba vía la propia desigualdad variacional).
- **Condición exacta para que un equilibrio sea óptimo de bienestar (Prop. 4.1) y peajes (Cor. 4.2):** $\nabla W(x^*)$ y $-F(x^*)$ deben estar ambos en el cono normal $N_K(x^*)$; si $W$ es cóncava la condición es también suficiente; los peajes $\tau=\nabla C-F$ convierten a los minimizadores de $C$ en los equilibrios.
- **Resultado pequeño (Teorema 5.1):** el conjunto $\Lambda(x^*)$ de pesos $\lambda\ge0$ con $x^*\in\arg\max_K\sum_i\lambda_iu_i$ es un cono convexo cerrado contenido en el cono de primer orden $\Lambda_1(x^*)$, con igualdad si los pagos son conjuntamente cóncavos; forma por bloques en términos de $F$, la cara de equilibrio y las externalidades marginales; sin concavidad, eficiencia de Pareto débil local ⇒ $\Lambda_1\ne\{0\}$ (alternativa de Gordan–Motzkin), que es el mecanismo de primer orden del teorema de Dubey (equilibrios interiores, genericidad en los pagos).
- **Imposibilidad (Prop. 5.3):** restar a cada $u_i$ su valor de mejor respuesta (función gap de Nikaidô–Isoda; equivalencia de mejor respuesta de Morris–Ui) deja intactos $F$ y los equilibrios y hace óptimo a $x^*$ para todo $\lambda$; si $N\ge2$ y algún $K_{-i}$ no es un punto, añadir a $u_i$ un término lineal en $x_{-i}$ tampoco cambia $F$ y saca $e_i$ del cono. Por tanto $(F,K)$ no determina $\Lambda(x^*)$ (con $N=1$ sí: siempre $\mathbb R_+$).
- **No poliedralidad (Ej. 5.6, contraejemplo de la ronda 1):** tres jugadores en $[0,1]^3$ con frontera parabólica en la rebanada $\lambda_3=1$; **v0.3:** la variante fuertemente monótona ($u_i-\tfrac\varepsilon2x_i^2$) tiene frontera $\lambda_2=\varphi(\lambda_1)$ en forma cerrada, estrictamente convexa, **demostrada** (E2c la reproduce a $1.1\times10^{-8}$; tolerancia del test $10^{-8}$).
- **$\Lambda\ne\Lambda_1$ en redes de dos mercancías (Ej. 5.7):** $\Lambda_1=\mathbb R^2_+$ pero $\Lambda=\{\lambda_2\le40\lambda_1\}$ (umbral bisecado 0.025000, brecha 0.0500). E5b (200 instancias aleatorias): $\Lambda_1$ bidimensional en 16 (el ortante en 9) y un rayo en 75; 21 instancias con testigo certificado de $\Lambda\ne\Lambda_1$, en 8 de ellas con algún testigo de pesos ambos positivos y en 13 sólo en un eje; ninguna con equilibrio interior (62), pero 4 de las 27 con todos los $b_e=0$ (donde el equilibrio es óptimo del sistema).
- **No poliedralidad con tres mercancías y costos afines (Ej. 5.8, nuevo en v0.3, demostrado):** enlaces privados $f/4$, $f/4$, $2$ y uno compartido $f$; $y^*=(0,0,1)$, $\Lambda_1=\mathbb R^3_+$ y $\Lambda=\{\lambda_3+m(\lambda_1,\lambda_2)\ge0\}$; en $\lambda_2=1$, $2/3<\lambda_1<3/2$, la frontera es $\psi(\lambda_1)=\lambda_1(\lambda_1+1)/(4(4-\lambda_1)(4\lambda_1-1))$. E7: frontera bisecada a $1.0\times10^{-8}$ de $\psi$, 0 discrepancias en 1878 puntos, testigo $(1,1,1/20)$ con brecha $1/180$.
- **Complejidad (Prop. 5.9, nueva en v0.3, señalada en la ronda 2):** decidir $\lambda\in\Lambda(x^*)$ y decidir $\Lambda=\Lambda_1$ son co-NP-completos para juegos cuadráticos en cajas, aun con $F$ fuertemente monótono, $x^*$ vértice y $\lambda$ unitario (reducción desde MAX-CUT; también con $N=2$ y acciones vectoriales). E6: 1696 grafos y 13 686 pares $(G,k)$, 0 discrepancias.
- **Verificación numérica (todos los criterios pasan: 4 + 13 + 5 + 5 + 5):** Pigou $d=1$ da PoA $=1.333333$; 200 redes afines: PoA máximo 1.2094, 0 violaciones de $4/3$, solver = water-filling a $8.8\times10^{-11}$ (el antiguo E1c, que repetía esta comparación, se fusionó). Juegos aleatorios: en los 200 cóncavos toda dirección probada confirma $\Lambda=\Lambda_1$; en los 200 no cóncavos la inclusión nunca falla y 58 de los 103 con cono no trivial (cota inferior) tienen testigo de inclusión estricta.
- **Preguntas abiertas:** las dos de la v0.2 quedan resueltas o retiradas (véase CONTINUIDAD). Queda una pregunta concreta: ¿es co-NP-difícil la pertenencia $\lambda\in\Lambda(f^*)$ en ruteo multimercancía con costos afines, donde la Prop. 5.9 no se aplica?

## Extensión

v0.1: 13 páginas; v0.2: 14; **v0.3: 13** (11 pt, márgenes de 1 in; bibliografía a dos columnas en letra pequeña). Se aplicaron todos los recortes del informe de la ronda 2 (Apéndice B a un párrafo, tabla de afirmaciones a `results/CLAIMS.md`, pruebas de Poincaré y de los Lemas 2.6 y 3.3 a una línea o cita, Prop. 4.1(c) a una frase, cifras duplicadas fuera de §6, panel de Pigou fuera; además, las dos figuras se remiten por ruta). No se llegó a 11 páginas porque la ronda 2 pidió añadir ≈2 páginas de demostraciones nuevas (Prop. 5.9 con pertenencia a co-NP, Ej. 5.8, forma cerrada de la variante del Ej. 5.6, alternativa de Motzkin, argumento de la Prop. 5.3); bajar más exigiría quitar demostraciones.

## Reproducir

```bash
pip install -r experiments/requirements.txt
python3 experiments/traffic_poa.py        # E1, ~3 s
python3 experiments/welfare_cone.py       # E2-E4, ~110 s (enumeración exacta de caras); --figures-only rehace solo las figuras
python3 experiments/commodity_cone.py     # E5, ~8 s
python3 experiments/hardness_maxcut.py    # E6, ~85 s
python3 experiments/three_commodity.py    # E7, ~3 s
./manuscript/build.sh                      # regenera numbers.tex y compila (pdflatex, bibtex, latexmk)
```

Semilla maestra: `20260930`, consumida secuencialmente por un único generador en cada script (reproducible; reordenar los experimentos cambia las instancias). Versiones usadas en la corrida de referencia: Python 3.11, NumPy 2.4, SciPy 1.17 (las cifras de E1–E4 de la v0.3 son idénticas a las de la v0.2). Cada script evalúa sus criterios (docstring) y escribe `criteria.all_pass` en su JSON; no existe registro externo de prerregistro.
