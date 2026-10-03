# SGE001 — Frontier Aggregation

**Título del manuscrito de trabajo:** *Moment-Based Aggregation of Production Frontiers: Second-Order Corrections, Their Failure at Capacity Thresholds, and What Can Be Certified for Comparisons*  
**Línea de investigación:** SGE001 — Agregación dinámica de fronteras productivas / Dynamic aggregation of production frontiers (área "Estadística y medición"). El manuscrito no usa "dynamic" en su título porque no contiene ningún modelo intertemporal (hallazgo M3 de la ronda 1).  
**Estado:** borrador de trabajo v0.2 (03/10/2026): una ronda de revisión interna aplicada (`REFEREE_SGE001_ronda1_20260930.md` → `RESPUESTA_SGE001_ronda1_20260930.md`). Generado en sesiones de Claude Code a partir de la ficha pública de la línea (no existe manuscrito previo). Sin revisión externa.

## Qué contiene

| Ruta | Contenido |
|---|---|
| `manuscript/main.tex`, `manuscript/refs.bib` | Manuscrito en LaTeX (inglés, 12 páginas) y bibliografía (18 entradas citadas de 25). |
| `manuscript/main.pdf` | PDF compilado (pdflatex + bibtex vía latexmk; sin referencias indefinidas ni cajas desbordadas). |
| `manuscript/numbers.tex`, `manuscript/table_*.tex` | Macros y cuerpos de tabla **generados** desde los resultados; ningún número del texto está tipeado a mano. |
| `experiments/frontier_aggregation.py` | Todos los experimentos (E0 autotest de derivadas; E1 barrido de dispersión; E1b términos de eficiencia; E1c exponente frente a N; E2 umbral de capacidad; E3 jerarquía de dos niveles; E4 reversiones de ranking; E5 recalibración escalar; E6 ejemplos cerrados). Un generador aleatorio por experimento (`SeedSequence(20260930).spawn`). |
| `experiments/make_numbers.py` | Convierte `results/results.json` en `manuscript/numbers.tex` y las tablas. |
| `results/results.json`, `results/tables.md` | Resultados completos de la corrida de referencia v0.2 (con intervalos bootstrap sobre réplicas e intervalos de Wilson) y las tablas completas en Markdown. |
| `figures/` | Figuras en PNG y PDF (`dispersion_sweep`, `threshold_hierarchy`, `decision`). |
| `CONTINUIDAD_SGE001_20260930.md` | Nota de continuidad interna: supuestos reconstruidos, decisiones, limitaciones, pendientes, registro de la ronda 1. |
| `FICHA_SGE001_propuesta.md` | Texto propuesto para la ficha pública (ES/EN). |
| `REFEREE_SGE001_ronda1_20260930.md`, `RESPUESTA_SGE001_ronda1_20260930.md` | Informe del árbitro interno y respuesta punto por punto del autor. |

## Idea del paper en tres líneas

1. Se fija el objeto: unidades con insumos $x_i$ y frontera cóncava común $f$; agregado $Y=\sum_i f(x_i)$ frente a la "unidad representativa" $N f(\bar x)$ (orden 1), su corrección con Hessiano y covarianza (orden 2) y el término de tercer momento (orden 3); jerarquía unidades → firmas → sector; frontera con capacidad $\min(f,c)$; error de agregación de orden $k$.
2. Se establece: (i) identidades de resto exactas (Taylor, ensambladas aquí) y cotas del error de orden 2 por el tercer momento absoluto, con constantes calculables para Cobb–Douglas, un factor de mejora del orden 2 sobre el orden 1 que crece como $1/\sigma$ y un certificado observable de mejora ($2B_2<|Q_2|$); (ii) (demostrado aquí) en un cruce de capacidad, $E_2 = -N\,T_u + O(\sigma^2)$, donde $T_u$ es la distancia media unilateral de los productos individuales a la capacidad, lineal en la dispersión: el orden 2 no mejora al orden 1; dos poblaciones con iguales tres primeros momentos pueden tener agregados que difieren a primer orden en $\sigma$; (iii) una condición de margen que certifica el orden de dos agregados, disponible solo en el régimen suave.
3. La simulación (semilla fija, ~30 s) confirma los exponentes y la constante del cruce, y aplica dos criterios predefinidos: el orden 2 reduce el error al menos 5 veces en todo el barrido con insumos simétricos, pero no con insumos log-normales más allá de $\sigma=0.42$ ni en los cruces de umbral; una recalibración escalar del término de segundo orden (global o por régimen) tampoco lo consigue. No se afirma nada sobre sectores reales ni sobre política.

## Resultados de referencia (corrida completa v0.2, semilla 20260930, N = 2000 unidades, 20 réplicas)

- **Régimen suave (E1).** Exponentes del error relativo en la dispersión $\sigma$ (ajuste en $\sigma\le0.05$, error estándar bootstrap entre paréntesis): orden 1 = 2.00; orden 2 = 3.12 (0.26) en CD–LN y 3.18 (0.24) en CES–LN, 4.00 con insumos simétricos; orden 3 = 4.00. El exponente 3–4 con log-normales es un efecto de $N$ finito (el tercer momento muestral fluctúa en $O(\sigma^3N^{-1/2})$): E1c da 3.2 / 3.3 / 4.2 para $N$ = 200 / 2000 / 20000, y 4.00 para el orden 3 en los tres casos. Criterio C1 (mejora ≥ 5× uniforme): se cumple en todo el barrido con insumos simétricos (mínimo 5.87 CD, 5.64 CES en $\sigma=0.5$); con log-normales se cumple en $\sigma=0.42$ y falla en el siguiente punto de malla, 0.56; en $\sigma=1$ el orden 2 es *peor* que el orden 1 (razón 0.31 CD, 0.48 CES). El orden 3 no mejora al orden 2 con insumos log-normales (razón mediana < 1 en 15/17 celdas CD y 13/17 CES). Las cotas certificadas se cumplen en el 100 % de las poblaciones, con $|E_2|/B_2\le0.018$ (conservadoras); el certificado observable $2B_2<|Q_2|$ se cumple en todas las réplicas solo hasta $\sigma=0.056$ (LN) / $0.071$ (SU).
- **Eficiencias idiosincráticas (E1b).** Con $\theta_i\sim U(0.5,1)$ independientes de los insumos, el término de covarianza $N\,\mathrm{Cov}(\theta,f(x))$, de orden $\sigma/\sqrt N$, domina al resto de segundo orden hasta $\sigma=0.18$ (es 7×10³ veces mayor en $\sigma=0.01$).
- **Umbral de capacidad (E2).** Con la media sobre la capacidad, el exponente del error de orden 2 es 1.01 (LN) / 1.00 (SU) frente a 3.52 / 4.00 sin capacidad; amplificación del error 1×10⁶ en $\sigma=0.01$. Constante del corolario: $T_u/(\sigma\tau_z)$ = 0.997 (σ = 0.01), 0.975 (0.1), 0.929 (0.316) con insumos simétricos; con log-normales, la versión con media desplazada $T_u/(\sigma\tau_z(b))$ = 1.000 / 0.976 / 0.910. La identidad exacta de la Proposición se verifica a 2×10⁻¹⁵. La rama en $f(\bar x)=c$ se fija por argumento explícito; la razón mínima $|E_1|/|E_2|$ en la rama "bajo capacidad" es 1.005 en $\sigma=0.01$ (ambas leyes) y en la rama "sobre" es 1 por construcción; la media muestral log-normal cae sobre la capacidad en el 40–55 % de las réplicas.
- **Jerarquía (E3).** La identidad "descendente en dos etapas = agrupado" se verifica exactamente (desviación 0 en coma flotante); el estimador ascendente (firma a firma) es mejor en 16/16 celdas suaves, por factores entre 1.15 y 4473, y su error depende solo de la dispersión intra-firma; con capacidad, las firmas que no la cruzan aportan ≤ 7×10⁻³ del error ascendente (la jerarquía localiza el fallo, no lo elimina).
- **Decisiones (E4).** Sin capacidad, la tasa de reversiones de ranking baja de hasta 46.1 % (orden 1) a ≤ 2.8 % (orden 2); entre las comparaciones certificadas por la condición de margen hubo 0 reversiones, pero el certificado cubre 100 % de los pares en $\sigma=0.02$, 70.9 % en 0.2 y 0 % en 0.4. Con la capacidad en el producto medio, las reversiones de orden 2 son 31–66 %. El orden 3 llega a 90.8 % de reversiones en $\sigma=0.8$. Criterio C2 (orden 2 ≤ 1/5 del orden 1): 23 celdas elegibles (3 sin capacidad, 20 con capacidad); fallan 15 por estimación puntual, todas con capacidad; con intervalos de Wilson al 95 %, 14 fallan claramente, 2 son limítrofes (sin capacidad σ = 0.4; +50 % σ = 0.4) y 7 pasan claramente.
- **Recalibración (E5).** $\lambda$ global = 2.25; por régimen 0.89 (suave), 3.14 (bajo capacidad), 4.72 (en capacidad); sobre capacidad $Q_2\equiv0$ (n/a). Ninguna variante cumple C1 fuera de muestra en los regímenes suave, bajo y en capacidad; la global es peor que la unidad representativa en el régimen suave (razón mínima 0.44) y la de régimen lo es bajo capacidad a dispersión pequeña (0.47).

## Reproducir

```bash
pip install -r experiments/requirements.txt
python3 experiments/frontier_aggregation.py     # ~30 s de pared en la máquina de referencia (30–50 s según la máquina); --fast ~10 s
./manuscript/build.sh                            # requiere TeX Live (pdflatex, bibtex, latexmk)
```

Semilla maestra: `20260930` (un generador por experimento mediante `SeedSequence.spawn`; los resultados de v0.1, con un único flujo compartido, no se reproducen con esta versión). Versiones usadas en la corrida de referencia: Python 3.11.15, NumPy 2.4.6, SciPy 1.17.1, Matplotlib 3.11.2; SHA-256 del script y fecha de la corrida en `results/results.json` (`meta`).
