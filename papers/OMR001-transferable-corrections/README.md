# OMR001 — Transferable Corrections (correcciones con reversión segura)

**Título de trabajo:** *Corrections with Safe Reversion Across Estimation Tasks: What a Held-Out Check Can and Cannot Guarantee*  
**Línea de investigación:** OMR001 — Correcciones transferibles entre tareas de estimación (área "Estadística y medición")  
**Estado:** borrador de trabajo v0.1 (30/09/2026), generado en una sesión de Claude Code a partir de la ficha pública de la línea. No existe manuscrito previo accesible: las definiciones del operador de corrección y de la "referencia segura" se **reconstruyeron** (véase la nota de continuidad). El resultado principal es una formalización con demostraciones y un cierre honesto: la ficha tenía razón.

## Qué contiene

| Ruta | Contenido |
|---|---|
| `manuscript/main.tex`, `manuscript/refs.bib` | Manuscrito en LaTeX (inglés, 14 pp. con 9 tablas y 3 figuras) y bibliografía (18 entradas reales). |
| `manuscript/main.pdf` | PDF compilado con pdflatex/bibtex (sin errores ni referencias indefinidas). |
| `manuscript/numbers.tex`, `manuscript/table_*.tex` | Macros y cuerpos de tabla **generados** desde `results/results.json`; ningún número del texto está tipeado a mano. |
| `experiments/safe_reversion.py` | Simulación completa (barridos de estructura, de desviación del objetivo, de tamaño de la muestra retenida; tres operadores; constantes del teorema; verificaciones de la identidad). `--fast` para una corrida reducida. |
| `experiments/make_numbers.py` | Convierte `results/results.json` en `numbers.tex` y las tablas. |
| `results/results.json`, `results/tables.md` | Resultados completos con semilla fija y las mismas tablas en Markdown. |
| `figures/` | Figuras en PNG y PDF. |
| `CONTINUIDAD_OMR001_20260930.md` | Nota de continuidad interna: supuestos, decisiones, resultados de referencia, limitaciones y próximos pasos. |
| `FICHA_OMR001_propuesta.md` | Propuesta de actualización de la ficha del CV web. |

## Idea en tres líneas

1. **Se formaliza** "corrección con reversión segura": estimador de referencia $R$ (media de la tarea), operador de corrección $C$ aprendido en tareas fuente (encogimiento hacia el centro común, tipo Efron–Morris), y una regla que usa $C$ solo si la diferencia de pérdidas en una muestra retenida de tamaño $m$ pasa un test unilateral de nivel $\alpha$.
2. **Se demuestra** qué no puede garantizarse (ninguna corrección mejora el riesgo minimax sobre todos los desplazamientos de la media; en $d\le 2$ toda regla que use alguna vez la corrección es peor que la referencia en algún punto) y qué sí: el riesgo del estimador con reversión excede al de la referencia en a lo sumo $\min\{\alpha\,E[\Delta^+],\ \varphi(z_{1-\alpha})\,2\sigma\,E\|C-R\|/\sqrt{m}\}$, la probabilidad de una transferencia dañina es $\le\alpha$, la constante es óptima salvo un factor explícito y el estimador está a $(z_{1-\alpha}+\varphi(0))\,2\sigma E\|C-R\|/\sqrt m$ del mejor de los dos candidatos.
3. **Se concluye** que el estimador con reversión **es** selección por muestra retenida entre dos candidatos con penalización de cambio (una línea de demostración): la garantía es de selección, no del operador, y la ganancia depende solo de la estructura compartida. Eso hace precisa la conclusión de la ficha ("no se ha demostrado diferenciación suficiente").

## Resultados de la corrida de referencia (semilla 20260930, 20 000 réplicas por configuración, 17 s)

Los números de este README y de la nota de continuidad están copiados a mano de `results/tables.md` y `results/results.json`; los del manuscrito son macros generadas por `experiments/make_numbers.py`.

- **Seguridad:** en las 345 combinaciones (configuración × operador × $\alpha$) el exceso de riesgo Monte Carlo respeta las tres cotas del Teorema B y la cota de frecuencia de eventos dañinos; el cociente máximo exceso/cota cerrada es 0.42. La identidad exacta $E[\Delta\,\pi]$ se verificó réplica a réplica (273 combinaciones con test $z$ pareado, $|z|_{\max}=2.96$; 72 con conteo de Poisson, 2 fuera del intervalo del 99 %, ambas del mismo lote; re-simuladas con 50 semillas independientes: $z=+1.27$).
- **Transferencia dañina:** al desplazar el objetivo $16\tau$ del centro común, corregir siempre multiplica el riesgo de la referencia por 13.8; el estimador con reversión ($\alpha=0.1$) queda en 1.26× la referencia con todos los datos, con exceso sobre la referencia de la muestra de estimación 0.0012 frente a cotas 0.120 ($\varphi$) y 0.133 ($\alpha$). La frecuencia de eventos dañinos nunca supera 3.4 % con $\alpha=0.1$ (25.3 % con $\alpha=0.5$, 0.25 % con $\alpha=0.01$).
- **Utilidad (criterio predefinido U: ganancia $\ge5\,\%$ frente a la media con *todos* los datos, IC 95 %):** corregir siempre es útil para $\mathrm{snr}\le 8$; el estimador con reversión **con garantía** solo para $\mathrm{snr}\le 2$ con $\alpha=0.5$, $\mathrm{snr}\le0.5$ con $\alpha=0.2$, $\mathrm{snr}=0$ con $\alpha=0.1$ y nunca con $\alpha\le0.05$. La causa es el costo de la partición (25 % del riesgo de referencia con $m=12$ de $n=60$), que la garantía no cubre, más la ganancia que el test no detecta.
- **Variantes sin garantía:** reajustar con todos los datos tras el chequeo es útil hasta $\mathrm{snr}=1$ ($\alpha=0.1$); la reversión por SURE (sin partición) es útil hasta $\mathrm{snr}=8$ y queda a pocos puntos de corregir siempre. Son construcciones clásicas (Bayes empírico + selección por SURE; validación cruzada + reajuste) y aquí no se demuestra ninguna cota para ellas.
- **Constantes:** $\kappa(\alpha)/\varphi(z_{1-\alpha})$ = 0.43, 0.16, 0.11, 0.08, 0.05 para $\alpha$ = 0.5, 0.2, 0.1, 0.05, 0.01: la cota cerrada es óptima salvo ese factor.

## Reproducir

```bash
pip install -r experiments/requirements.txt
python3 experiments/safe_reversion.py        # ~20 s (usar --fast para ~5 s)
./manuscript/build.sh                        # requiere TeX Live (pdflatex, bibtex, latexmk)
```

Semilla maestra: `20260930` (re-verificaciones: `20260931` y `20260930+1000+i`). Versiones usadas en la corrida de referencia: Python 3.11, NumPy 2.4, SciPy 1.17, Matplotlib 3.11.
