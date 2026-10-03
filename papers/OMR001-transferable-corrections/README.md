# OMR001 — Transferable Corrections (correcciones con reversión segura)

**Título de trabajo:** *Corrections with Safe Reversion Across Estimation Tasks: What a Held-Out Check Can and Cannot Guarantee*  
**Línea de investigación:** OMR001 — Correcciones transferibles entre tareas de estimación (área "Estadística y medición")  
**Estado:** borrador de trabajo **v0.2, una ronda de revisión interna aplicada** (informe del 30/09/2026, respuesta del 03/10/2026; véase `REFEREE_OMR001_ronda1_20260930.md` y `RESPUESTA_OMR001_ronda1_20260930.md`). Generado en sesiones de Claude Code a partir de la ficha pública de la línea. No existe manuscrito previo accesible: las definiciones del operador de corrección y de la "referencia segura" se **reconstruyeron** (véase la nota de continuidad). El resultado principal es una formalización que hace precisa la conclusión de la ficha: explica por qué no cabía esperar diferenciación *del mecanismo de seguridad*; la diferenciación por la familia de operadores no se explora más allá de tres instancias afines, y la decisión de cerrar la línea queda abierta.

## Qué contiene

| Ruta | Contenido |
|---|---|
| `manuscript/main.tex`, `manuscript/refs.bib` | Manuscrito en LaTeX (inglés, 10 pp. a 10 pt con 5 tablas y 2 figuras) y bibliografía (18 entradas reales). |
| `manuscript/main.pdf` | PDF compilado con pdflatex/bibtex (sin errores, referencias indefinidas ni cajas desbordadas). |
| `manuscript/numbers.tex`, `manuscript/table_*.tex` | Macros y cuerpos de tabla **generados** desde `results/results.json`; ningún número del texto está tipeado a mano. |
| `experiments/safe_reversion.py` | Simulación completa (barridos de estructura, de desviación del objetivo y de tamaño de la muestra retenida con τ² fijo; tres operadores; constantes del teorema; cota uniforme; verificaciones de la identidad). `--fast` para una corrida reducida. |
| `experiments/make_numbers.py` | Convierte `results/results.json` en `numbers.tex` y las tablas. |
| `experiments/check_uniform_cap.py` | Comprobación numérica independiente, en rejilla, de la desigualdad del Corolario 4.3 (cota uniforme); unos segundos. |
| `results/results.json`, `results/tables.md` | Resultados completos con semilla fija y las tablas en Markdown (T1–T5). Las tablas de verificación por configuración y la del barrido en m solo están aquí (recorte de extensión pedido por el árbitro). |
| `figures/` | Figuras en PNG y PDF (`sweeps` es la figura fusionada del manuscrito). |
| `CONTINUIDAD_OMR001_20260930.md` | Nota de continuidad interna: supuestos, decisiones, resultados de referencia, limitaciones, próximos pasos y la ronda de revisión. |
| `FICHA_OMR001_propuesta.md` | Propuesta de actualización de la ficha del CV web. |
| `REFEREE_OMR001_ronda1_20260930.md`, `RESPUESTA_OMR001_ronda1_20260930.md` | Informe del árbitro interno y respuesta punto por punto. |

## Idea en tres líneas

1. **Se formaliza** "corrección con reversión segura": estimador de referencia $R$ (media de la tarea), operador de corrección $C$ aprendido en tareas fuente (encogimiento hacia el centro común, tipo Efron–Morris), y una regla que usa $C$ solo si la diferencia de pérdidas en una muestra retenida de tamaño $m$ pasa un test unilateral de nivel $\alpha$.
2. **Se demuestra** qué no puede garantizarse (ninguna corrección aprendida en fuentes cuya ley no depende del parámetro objetivo mejora el riesgo minimax; en $d\le 2$, con fuentes no informativas, toda regla que use alguna vez la corrección es peor que la referencia en algún punto) y qué sí: el riesgo del estimador con reversión excede al de la referencia en a lo sumo $\min\{\alpha\,E[\Delta^+],\ \varphi(z_{1-\alpha})\,2\sigma\,E\|C-R\|/\sqrt{m}\}$ y además en a lo sumo una cota **uniforme en el parámetro** (nueva en v0.2), la probabilidad de usar la corrección cuando su pérdida realizada supera la de la referencia es $\le\alpha\,P(\Delta>0)\le\alpha$, dentro de la clase de chequeos unilaterales a nivel fijo la constante es óptima salvo un factor explícito, y el estimador está a $(z_{1-\alpha}+\varphi(0))\,2\sigma E\|C-R\|/\sqrt m$ del mejor de los dos candidatos.
3. **Se concluye** que el estimador con reversión **es** selección por muestra retenida entre dos candidatos con penalización de cambio (una línea de demostración): la garantía es de selección, indiferente al operador, y la ganancia depende solo de la estructura compartida. Eso explica por qué no cabía esperar diferenciación del mecanismo de seguridad; si hay diferenciación, debe venir de la familia de operadores, que aquí no se explora.

## Resultados de la corrida de referencia (semilla 20260930, 20 000 réplicas por configuración, 11 s de cómputo, 14 s de pared)

Los números de este README y de la nota de continuidad están copiados a mano de `results/tables.md` y `results/results.json`; los del manuscrito son macros generadas por `experiments/make_numbers.py`.

- **Seguridad:** en las 345 combinaciones (configuración × operador × $\alpha$) el exceso de riesgo Monte Carlo respeta las tres cotas del Teorema 4.2, la cota uniforme del Corolario 4.3 y la cota de frecuencia de eventos dañinos; el cociente máximo exceso/cota cerrada $\varphi$ es 0.40 y exceso/cota uniforme 0.38. La identidad exacta $E[\Delta\,\pi]$ se verificó réplica a réplica (273 combinaciones con test $z$ pareado, $|z|_{\max}=2.83$; 72 con conteo de Poisson, 1 fuera del intervalo del 99 %, re-simulada con 50 semillas independientes: 1882 aceptaciones frente a 1869.7 esperadas, $z=+0.29$).
- **Transferencia dañina:** al desplazar el objetivo $16\tau$ del centro común, corregir siempre multiplica el riesgo de la referencia por 13.8; el estimador con reversión ($\alpha=0.1$) queda en 1.26× la referencia con todos los datos, con exceso sobre la referencia de la muestra de estimación 0.0012 frente a cotas 0.120 ($\varphi$), 0.133 ($\alpha$) y 0.146 (uniforme). La frecuencia de eventos dañinos nunca supera 3.4 % con $\alpha=0.1$ (25.3 % con $\alpha=0.5$, 0.25 % con $\alpha=0.01$).
- **Utilidad (criterio predefinido U: ganancia $\ge5\,\%$ frente a la media con *todos* los datos, IC 95 %):** corregir siempre es útil para $\mathrm{snr}\le 8$; el estimador con reversión **con garantía** solo para $\mathrm{snr}\le 2$ con $\alpha=0.5$, $\mathrm{snr}\le0.5$ con $\alpha=0.2$, $\mathrm{snr}=0$ con $\alpha=0.1$ y nunca con $\alpha\le0.05$. La causa es el costo de la partición ($m=12$ de $n=60$: 25 % del riesgo de la media con todos los datos, 20 % del riesgo de $R$), que la garantía no cubre, más la ganancia que el test no detecta. Cuatro de las marcas están en el filo (extremo inferior del IC a menos de 2 puntos del umbral): $\alpha=0.1$ en snr 0, refit en snr 1, $\alpha=0.5$ en snr 2, SURE en snr 8.
- **Variantes sin garantía:** reajustar con todos los datos tras el chequeo es útil hasta $\mathrm{snr}=1$ ($\alpha=0.1$; en la corrida reducida `--fast`, hasta 0.5); la reversión por SURE (sin partición) es útil hasta $\mathrm{snr}=8$ y queda a pocos puntos de corregir siempre. Son construcciones clásicas (Bayes empírico + selección por SURE; validación cruzada + reajuste) y aquí no se demuestra ninguna cota para ellas.
- **Tamaño retenido ($\tau^2$ fijo en $\sigma^2/48$, snr 1 respecto de $n_e=48$, $\alpha=0.1$):** $m=3$: +3.1 % ($\kappa=0$) / −17.9 % ($\kappa=8$); $m=6$: +0.2 / −19.6 %; $m=12$: −6.5 / −29.9 %; $m=24$: −25.0 / −68.8 %. Las columnas que no usan la partición son planas en $m$ (corrección de la ronda 1).
- **Constantes:** $\kappa(\alpha)/\varphi(z_{1-\alpha})$ = 0.43, 0.16, 0.11, 0.08, 0.05 para $\alpha$ = 0.5, 0.2, 0.1, 0.05, 0.01: dentro de la clase de chequeos unilaterales a nivel fijo, la cota cerrada es óptima salvo ese factor.

## Reproducir

```bash
pip install -r experiments/requirements.txt
python3 experiments/safe_reversion.py        # ~15 s (usar --fast para ~5 s)
./manuscript/build.sh                        # requiere TeX Live (pdflatex, bibtex, latexmk)
```

Semilla maestra: `20260930` (re-verificaciones: `20260931` y `20260930+1000+i`). Versiones usadas en la corrida de referencia: Python 3.11, NumPy 2.4, SciPy 1.17, Matplotlib 3.11.

**Sorteos por réplica** (trasladado del apéndice del manuscrito): parámetros fuente $\theta_s\sim N(0,\tau^2 I_d)$ y medias fuente $\bar X_s\sim N(\theta_s,\sigma^2 I_d/n_s)$; parámetro objetivo $\theta\sim N(\kappa\tau e_1,\tau^2 I_d)$; $\bar X_e\sim N(\theta,\sigma^2 I_d/n_e)$ y $\bar Y\sim N(\theta,\sigma^2 I_d/m)$ independientes; $\bar X_n=(n_e\bar X_e+m\bar Y)/n$. El centro $\mu=0$ sin pérdida de generalidad, porque los operadores lo estiman. Se usan números aleatorios comunes entre valores de $\alpha$ y entre operadores dentro de una configuración; entre configuraciones (y entre valores de $m$) no se comparte nada. En los barridos de estructura y desviación $\tau^2=\mathrm{snr}\cdot\sigma^2/n_e$ con $n_e=48$; en el barrido en $m$, $\tau^2$ se fija en ese mismo valor para todo $m$.
