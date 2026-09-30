# SGE001 — Frontier Aggregation

**Título de trabajo:** *Dynamic Aggregation of Production Frontiers: Second-Order Moment Corrections, Their Failure at Capacity Thresholds, and What Can Be Certified for Comparisons*  
**Línea de investigación:** SGE001 — Agregación dinámica de fronteras productivas / Dynamic aggregation of production frontiers (área "Estadística y medición")  
**Estado:** borrador de trabajo v0.1 (30/09/2026), generado en una sesión de Claude Code a partir de la ficha pública de la línea (no existe manuscrito previo). Sin revisión externa.

## Qué contiene

| Ruta | Contenido |
|---|---|
| `manuscript/main.tex`, `manuscript/refs.bib` | Manuscrito en LaTeX (inglés) y bibliografía (25 entradas). |
| `manuscript/main.pdf` | PDF compilado (pdflatex + bibtex vía latexmk; sin referencias indefinidas). |
| `manuscript/numbers.tex`, `manuscript/table_*.tex` | Macros y cuerpos de tabla **generados** desde los resultados; ningún número del texto está tipeado a mano. |
| `experiments/frontier_aggregation.py` | Todos los experimentos (E0 autotest de derivadas; E1 barrido de dispersión; E1b términos de eficiencia; E2 umbral de capacidad; E3 jerarquía de dos niveles; E4 reversiones de ranking; E5 recalibración escalar; E6 ejemplos cerrados). |
| `experiments/make_numbers.py` | Convierte `results/results.json` en `manuscript/numbers.tex` y las tablas. |
| `results/results.json`, `results/tables.md` | Resultados completos de la corrida de referencia (semilla 20260930) y las mismas tablas en Markdown. |
| `figures/` | Figuras en PNG y PDF. |
| `CONTINUIDAD_SGE001_20260930.md` | Nota de continuidad interna: supuestos reconstruidos, decisiones, limitaciones, pendientes. |

## Idea del paper en tres líneas

1. Se fija el objeto: unidades con insumos $x_i$ y frontera cóncava común $f$; agregado $Y=\sum_i f(x_i)$ frente a la "unidad representativa" $N f(\bar x)$ (orden 1), su corrección con Hessiano y covarianza (orden 2) y el término de tercer momento (orden 3); jerarquía unidades → firmas → sector; frontera con capacidad $\min(f,c)$; error de agregación de orden $k$.
2. Se demuestra: (i) identidades de resto exactas y cotas del error de orden 2 por el tercer momento absoluto, con constantes calculables para Cobb–Douglas, y factor de mejora del orden 2 sobre el orden 1 que crece como $1/\sigma$ (régimen suave); (ii) en un cruce de capacidad, $E_2 = -N\,T_u + O(\sigma^2)$, donde $T_u$ es la distancia media unilateral de los productos individuales a la capacidad, que es lineal en la dispersión: el orden 2 no mejora al orden 1; dos poblaciones con iguales media y covarianza pueden tener agregados que difieren a primer orden en $\sigma$; (iii) una condición de margen que certifica el orden de dos agregados, disponible solo en el régimen suave.
3. La simulación (semilla fija, ~40 s de CPU) confirma los exponentes y la constante, y aplica dos criterios predefinidos: el orden 2 reduce el error al menos 5 veces en todo el barrido con insumos simétricos, pero no con insumos log-normales por encima de $\sigma\approx0.42$ ni en los cruces de umbral; una recalibración escalar del término de segundo orden (global o por régimen) tampoco lo consigue. No se afirma nada sobre sectores reales ni sobre política.

## Resultados de referencia (corrida completa, semilla 20260930, N = 2000 unidades, 20 réplicas)

- **Régimen suave (E1).** Exponentes del error relativo en la dispersión $\sigma$: orden 1 = 2.00; orden 2 = 3.78 (log-normal) y 4.00 (simétrico); orden 3 = 4.00. Criterio C1 (mejora ≥ 5× uniforme): se cumple en todo el barrido con insumos simétricos (mínimo 5.97 CD, 5.65 CES en $\sigma=0.5$); con log-normales se cumple hasta $\sigma=0.42$ y en $\sigma=1$ el orden 2 es *peor* que el orden 1 (razón 0.75 CD, 0.65 CES). El orden 3 no mejora al orden 2 con insumos log-normales (razón mediana < 1 en 17/17 celdas CD y 14/17 CES): el tercer momento log-normal es $O(\sigma^4)$, del mismo orden que el resto despreciado. Las cotas certificadas se cumplen en el 100 % de las poblaciones, con $|E_2|/B_2\le 0.020$ (conservadoras), y solo certifican mejora sobre el orden 1 hasta $\sigma=0.10$ (LN) / $0.12$ (SU).
- **Eficiencias idiosincráticas (E1b).** Con $\theta_i\sim U(0.5,1)$ independientes de los insumos, el término de covarianza $N\,\mathrm{Cov}(\theta,f(x))$, de orden $\sigma/\sqrt N$, domina al resto de segundo orden hasta $\sigma=0.18$ (es 8.9×10³ veces mayor en $\sigma=0.01$).
- **Umbral de capacidad (E2).** Con la media sobre la capacidad, el exponente del error de orden 2 es 1.00 (frente a 3.36 / 4.00 sin capacidad); $-E_2/(N T_u)=1.0000$ en $\sigma=0.01$ y permanece en $[0.85,1.08]$ en todo el barrido; amplificación del error 7×10⁵ en $\sigma=0.01$; razón $|E_1|/|E_2|=1.00$ en todo el barrido. La cota bilateral de la Proposición 3 se cumple en 168/168 celdas.
- **Jerarquía (E3).** La identidad "descendente en dos etapas = agrupado" se verifica a 2×10⁻¹⁶; el estimador ascendente (firma a firma) es mejor en 16/16 celdas suaves, por factores entre 1.16 y 4005, y su error depende solo de la dispersión intra-firma; con capacidad, las firmas que no la cruzan aportan ≤ 4×10⁻³ del error ascendente (la jerarquía localiza el fallo, no lo elimina).
- **Decisiones (E4).** Sin capacidad, la tasa de reversiones de ranking baja de hasta 45.2 % (orden 1) a ≤ 3.3 % (orden 2); entre las comparaciones certificadas por la condición de margen hubo 0 reversiones, pero el certificado cubre 100 % de los pares en $\sigma=0.02$, 70.8 % en 0.2 y 0 % en 0.4. Con la capacidad en el producto medio, las reversiones son 28–70 % en todos los órdenes. El orden 3 llega a 89.2 % de reversiones en $\sigma=0.8$. Criterio C2 (orden 2 ≤ 1/5 del orden 1): falla en 15 de 23 celdas elegibles, todas con capacidad (15 de 20).
- **Recalibración (E5).** $\lambda$ global = 2.68; por régimen 0.90 (suave), 3.11 (bajo capacidad), 4.65 (en capacidad), indefinido sobre capacidad ($Q_2\equiv0$). Ninguna variante cumple C1 fuera de muestra; la global es peor que la unidad representativa en el régimen suave (razón mínima 0.38).

## Reproducir

```bash
pip install -r experiments/requirements.txt
python3 experiments/frontier_aggregation.py     # ~45 s (usar --fast para ~10 s)
./manuscript/build.sh                            # requiere TeX Live (pdflatex, bibtex, latexmk)
```

Semilla maestra: `20260930`. Versiones usadas en la corrida de referencia: Python 3.11.15, NumPy 2.4.6, SciPy 1.17.1, Matplotlib 3.11.2.
