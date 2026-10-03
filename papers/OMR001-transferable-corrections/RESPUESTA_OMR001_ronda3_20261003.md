# Respuesta del autor a la ronda 3 de revisión interna — OMR001 (v0.4 → v0.5)

Fecha: 03/10/2026. Informe: `REFEREE_OMR001_ronda3_20261003.md` (cambios menores; 0 bloqueantes, 2 mayores, 9 menores; Teorema 5.1 (i)–(iv) y Corolario 5.2 confirmados correctos). Manuscrito resultante: **v0.5** (fecha fija 3 October 2026), 12 páginas con letra normal en todo el documento (incluidos los apéndices).

**Recuento (11 hallazgos):** 9 aceptados, 2 aceptados con matiz (m3, m6), 0 rebatidos. Las acciones de maquetación (§5 del informe) y el cambio de estado (acción 11) se aplicaron.

## Verificación propia previa (antes de aceptar)

Script propio en el scratchpad (`omr001_r3_author/verify_author.py`). No forma parte del paper, no importa código del paper ni del árbitro, y ningún número del texto sale de él.

- **Fórmula del oráculo (M1).** Cuadratura frente a Monte Carlo con observaciones crudas (400 000 réplicas, $d=5$, $n=60$): $m=12,\alpha=0.1$: −0.00541 frente a −0.00546 ± 0.00003; $m=24,\alpha=0.1$: +0.00982 frente a +0.00978 ± 0.00004; $m=24,\alpha=0.2$: +0.00609 frente a +0.00612 ± 0.00005; $m=12,\alpha=0.5$: −0.03416 frente a −0.03414 ± 0.00007. Para la partición con oráculo: −0.00657, −0.00120, −0.02447 y −0.05576 frente a −0.00673 ± 0.00007, −0.00126 ± 0.00010, −0.02449 ± 0.00009 y −0.05575 ± 0.00008. Las cifras del árbitro son correctas.
- **Peor caso exacto de la partición (m1).** Cuadratura frente a MC de la construcción $u(\xi)$ ($\alpha=0.1$): 0.02643 frente a 0.02629 ± 0.00026 ($m=3$); 0.01577 frente a 0.01571 ± 0.00015 ($m=6$); 0.00999 frente a 0.01010 ± 0.00009 ($m=12$).
- **Reducción colineal (m2).** En 60 casos $(\alpha,\eta,\xi)$, el supremo 2-D en rejilla nunca supera al 1-D sobre $c=\pm1$, y el argmax 2-D tiene siempre $|c|=1$.

Después, todos los números del texto se generaron con el código del paper: las secciones nuevas (d)–(h) de `theory/check_refit.py` escriben en `results/refit_check.json` y `experiments/make_numbers.py` genera las macros a partir de ese archivo.

## Mayores

**M1 — "removes the split cost for each given correction" es falso como comparación por corrección. → Aceptado.**
El árbitro tiene razón: el Teorema 5.1(ii) habla de la *cota*, no del riesgo. Con $C=\theta$ ($w=-e$, $\Delta=-\|e\|^2$, $u=-\xi/2$), la identidad (i) da exactamente $(\sigma^2/m)E[-(1-2\eta)\xi^2\Phi(\xi/2-z)+2\eta\xi\varphi(z-\xi/2)]$. Lo rederivé y lo comprobé (arriba).

Cambios:
- **Resumen.** (iv) dice ahora "removes the additive split cost from the bound, which becomes proportional to the correction, but not from the risk: even the oracle correction $C=\theta$ can lose to the split, or to the full-data mean for large $m$, and uniformly in $C$ at least $4\alpha$ times the split cost remains".
- **Introducción.** "the additive split cost leaves the bound but not the risk; even the oracle correction can lose to the split…".
- **Obs. 5.3(a).** Pasa a titularse "*The bound has no split-cost term*" y añade "This compares bounds, not risks… see (e)".
- **Nueva Obs. 5.3(e).** Da la fórmula exacta del oráculo y la de la partición, con cifras generadas: con $m=12$, $\alpha=0.1$, la partición da −0.0066 y el reajuste −0.0054; con $m=24$, el reajuste da **+0.0098** (11.8 % del riesgo de $\bar X_n$) frente a −0.0012 de la partición. Añade la lista generada de celdas: la partición gana con $\alpha\in\{0.5,0.2,0.1\}$ en todo $m$; el reajuste es dañino con $m=24$ y $\alpha\le0.2$, y con $m=12$ y $\alpha=0.01$. Explica los dos efectos que señala el árbitro (selección y "$w$ corrige el error de $R$, no el de $\bar X_n$"). Añade que con $m\ge n_e$ ambos términos son no negativos, de modo que el oráculo transportado nunca mejora a $\bar X_n$.
- **Tabla 1.** Nuevo bloque inferior "oracle correction $C=\theta$" (5 α × 4 m, reajuste frente a partición, con marca H donde el reajuste es dañino), generado en `table_oracle.tex`.
- **Resultados.** Fila EB del barrido en $m$ con $m=24$, $\kappa=0$: exceso **+0.0035 ± 0.0002** sobre $\bar X_n$ (ganancia −4.2 %), desde `results.json` (las mismas réplicas que el resto). Se retiró además "the transported refit does not pay the split" (l.405 de v0.4), que sobreafirmaba lo mismo; ahora dice "pays much less than the split estimator at $m=12$, but it is not harmless".
- **Veredicto, tabla de afirmaciones (fila nueva "Not better than the split for every correction"), README, ficha (ES/EN) y CONTINUIDAD** (nota en la sección de integración v0.4): la misma corrección.

**M2 — Resultado adversarial desfavorable del cross-fitting sin reportar. → Aceptado.**
- **Resultados (Sec. 7), en el mismo párrafo que el resultado favorable.** "It is not free of the split cost either: on the adversarial grid its excess reaches 9.4 times the split cost (fixed additive correction $\|v\|=2\sigma/\sqrt m$, $m=3$, $\alpha=0.5$; 0.50 of the risk of $\bar X_n$), and 0.07–0.25 times at $\alpha=0.1$".
- **Macros y otras ubicaciones.** Se usan `\RfAcfMaxSplit` y `\RfAcfTenMin`/`\RfAcfTenMax`, más dos nuevas: `\RfAcfMaxSplitV`, extraída por programa del nombre de la familia, y `\RfAcfMaxOverRn`. Lo mismo, abreviado, en la Obs. 5.3(d), el veredicto, una fila nueva de la tabla de afirmaciones ("empirical (MC)"), README y ficha.

## Menores

**m1 — Peor caso exacto de la partición. → Aceptado.**
Demostrado como **Prop. 4.5(c)**, con la prueba escrita en el texto. El exceso condicional es $(\sigma^2/m)\,2\omega u\Phi(-(z+u))$ con $|2u-\omega|\le2\xi$. Para $u>0$ es lineal creciente en $\omega$, así que el máximo cae en $\omega=2(u+\xi)$, lo que da $M_0$. El supremo se alcanza (salvo ε) con $C=\theta_0-(1+2u(\xi)/\xi)(R-\theta_0)$ y $u(\cdot)$ escalonada; el error es ≤ $8\kappa h$ porque $g(u,\cdot)$ es $4\kappa$-Lipschitz. La parte (b) pasa a ser consecuencia de (c) ($u\equiv u^\ast$ para la cota inferior, $(u^2+\xi u)\Phi\le\kappa_2+\xi\kappa$ para la superior).
- **Tabla 1.** Compara ahora valores exactos: reajuste frente a partición, sin corchetes. `make_numbers.py` comprueba por aserción que cada valor exacto cae dentro del corchete de (b) y que no queda ninguna celda "inconclusa".
- **Celdas antes inconclusas.** Con $\alpha=0.1$ y $m=3$ el reajuste es peor (0.0322 frente a 0.0308); con $m=6$ es mejor (0.0241 frente a 0.0250).
- **Textos generados.** `\RfBetterText`/`\RfWorseText` se regeneran y la tabla de afirmaciones dice "below for α=0.1 (m∈{6,12,24}), α=0.05, α=0.01; above for α=0.5, α=0.2, α=0.1 (m∈{3})".
- **Punto (h) de CONTINUIDAD: cerrado.** Valor exacto 0.0100 en el diseño, dentro de [0.0096, 0.0106], citado en la Prop. 4.5(c) y en "Results: safety".

**m2 — En (iv) sobra $d\ge2$. → Aceptado.**
Verifiqué el argumento. Para $u$ fijo, $f_\eta=\eta\Phi\,\omega^2+2\omega[(1-\eta)u\Phi+\eta\varphi]$ es cuadrática convexa en $\omega$ sobre $(2(u-\xi)^+,2(u+\xi)]$, así que el supremo está en un extremo ($c=\mp1$) o en el límite $\omega\to0$ (valor 0).
- **Enunciado.** (iv) vale ahora para todo $d\ge1$, con el peor $C=R+\lambda(R-\theta_0)$ (infla o encoge el error de $R$, como en la Prop. 4.5(c)).
- **Prueba.** Se reescribió en el Apéndice B con $w=(\sigma/\sqrt m)\,\omega c\,\hat e$, $c\in\{\pm1\}$, sin $\hat e_\perp$.
- **Definición de $M_\eta$.** Se dice que el supremo es unidimensional.
- **Código.** `check_refit.py` §(d) recalcula $M_\eta$ por la reducción 1-D y lo compara con la búsqueda 2-D que alimenta las tablas. La diferencia máxima es $1\cdot10^{-5}$ en $M$ y $7\cdot10^{-7}$ relativa en el tope exacto, y el argmax 2-D tiene siempre $|c|=1$.
- **Matiz de implementación.** Las tablas siguen usando la búsqueda 2-D, para no cambiar ningún valor ya publicado; la diferencia es invisible a 4 decimales.

**m3 — Contexto de los fallos de umbral. → Aceptado con matiz.**
- **Mismo fallo que el de la Sec. 7.** Lo comprobé por programa en lugar de darlo por supuesto. `check_refit.py` registra ahora la configuración que falla (`design.identity_fail_at`) y `make_numbers.py` comprueba por aserción que coincide con `worst_rare_config` de `results.json`: full pooling, α = 0.05, m = 6, desviación 8τ.
- **Texto.** Dice que es "the acceptance-count test of Section 7 on the same replicates and in the same configuration, and does not test the term $\eta s\varphi(z+u)$".
- **Excedencias esperadas** de $|z|>3$, generadas: 0.74 en 274 pruebas (diseño) y 1.2 en 440 (rejilla adversarial).
- **Matiz.** La verificación opcional de la identidad por cuadratura condicional (como hizo el árbitro) no se hizo. La identidad queda comprobada a mano, por el árbitro (720 pares) y por MC.

**m4 — Cocientes adversariales > 1 por ruido Monte Carlo. → Aceptado.**
`check_refit.py` §(g) calcula por cuadratura exacta las familias que dependen de $R$ solo a través de $\xi$, y la tabla de afirmaciones y el texto ya no citan el cociente 1.09 de MC crudo.
- **Familia del maximizador de $M_\eta$:** 0.9996–1.0000 del tope exacto.
- **Construcción de la Prop. 4.5(b):** 0.34–0.993. El 0.989 del árbitro es una de las seis celdas que calculó; en las 20 celdas el rango es 0.34–0.993.
- **Reflexión:** igual a su forma cerrada a 6 cifras.
- **Familias que no son función de $\xi$** (desplazamientos fijos, encogimientos): estimador de Rao–Blackwell, ya calculado en el script (columna `rb`), con máximo 0.70 del tope.
- **Comentario.** El estimador de Rao–Blackwell de la familia del maximizador da 1.0043, que es ruido de muestreo de $e$. Por eso, para las familias colineales se usa la cuadratura y no Rao–Blackwell.

**m5 — Máximos redondeados hacia abajo en macros nuevas. → Aceptado.**
Nueva función `up()` en `make_numbers.py`, aplicada a todos los máximos de las macros v0.4 (`Rf*`, `*Tr*`) y a los nuevos. Cambian 9 macros: `DepTrTenMax` 1.11→1.12, `RfDesignMaxBc` 0.86→0.87, `RfSimMaxCap` 0.65→0.66, `RfCfMaxCap` 0.09→0.10, `RfAdvMaxB` 1.02→1.03, `RfAdvMaxCapc` 0.91→0.92, `RfAdvWorstMax` 1.07→1.08, `RfAdvReflMax` 1.08→1.09, `RfAcfTenMax` 0.24→0.25. De ellas, cuatro se citan en el texto (`DepTrTenMax`, `RfDesignMaxBc`, `RfSimMaxCap`, `RfAcfTenMax`). `RfAdvWorstMax` y `RfAdvReflMax` ya no se citan, porque se sustituyeron por los valores exactos de m4. `RfCfMaxCap`, `RfAdvMaxB` y `RfAdvMaxCapc` se generan pero no se citaban tampoco en v0.4. Las macros de v0.3 no se tocaron: el árbitro las da por bien aplicadas.

**m6 — Resumen largo y desordenado. → Aceptado con matiz.**
- **Extensión.** 227 palabras (v0.4: 277; meta ≤ 230). Para recortar, se condensaron (i)–(iii), salió del resumen la frase sobre SURE y el operador reaplicado (sigue en el cuerpo) y la simulación quedó en una frase.
- **Orden.** (iv) va inmediatamente después de (iii) y antes de la simulación.
- **Matiz.** El paréntesis "with plain hold-out the worst case is worse than with the split" salió del resumen en lugar de calificarse allí, por extensión. En el cuerpo (Obs. 5.3(b)) dice: "worse in this design and, numerically, in all 36 other designs we tried ($d\in\{1,2,5,50\}$, $n_e\in\{2,10,1000\}$, $m\in\{1,3,30\}$; ratio 1.001–3.28); this is not proved". Los 36 diseños los calcula el propio `check_refit.py` §(h), con los mismos diseños que el árbitro, y coinciden con su 36/36. La tabla de afirmaciones dice "numerical (quadrature); not proved in general".

**m7 — Holgura de la forma cerrada de (iii). → Aceptado.** Obs. 5.3(b): "it does not vanish as $\alpha\to0$ and is informative only for moderate $\alpha$ and $m\ll n_e$; for small $\alpha$ the exact cap should be used".

**m8 — Apéndice B poco legible. → Aceptado.** Apéndice B en cuerpo normal (se quitó `\small`), con cada parte (i)–(iv) en su propio párrafo. La prueba de (iv) se simplificó (m2) y el párrafo de la ruta de la Obs. 5.3(c) salió del apéndice (véase maquetación).

**m9 — Diseño $m/n_e$. → Aceptado.** Limitaciones: "The transported refit adds to $\bar X_n$ a vector calibrated for $R$: when $m\ge n_e$ ($\eta\ge\frac12$) even the oracle correction is never better than $\bar X_n$ (accepted always, its risk is $d\sigma^2m/(nn_e)$ against $d\sigma^2/n$); the design ($m/n_e=12/48$) is on the favourable side". Verificado: el error del oráculo aceptado es $\eta(h-e)$, con riesgo $\eta^2d\sigma^2(1/m+1/n_e)=d\sigma^2m/(nn_e)$. "Never better" es exacto también en $m=n_e$, donde ambos riesgos coinciden.

## Bibliografía

`hunter2007`, verificada por el árbitro, queda marcada así en CONTINUIDAD. El DOI opcional no se añadió, porque ninguna otra entrada lleva DOI. `refs.bib` no cambió.

## Maquetación (§5 del informe) → Aplicada

| Recorte propuesto | Hecho |
|---|---|
| 1. Fig. 2 fuera del texto | Sí. `figures/excess_vs_bounds.*` sigue en la carpeta (README) y sus cifras están en el texto. |
| 2. Tabla 6 (constantes) a `results/tables.md` | Sí (ya existía como T5). Las referencias del texto apuntan a T5 y las macros citadas se mantienen. |
| 3. Obs. 5.3(c) en una frase; derivación fuera | Sí. La derivación pasó sin cambios a `theory/refit_derivation.md`; la cuadratura sigue en `check_refit.py` §(c). |
| 4. Párrafo de seguridad abreviado | Sí; los detalles de la re-verificación Poisson remiten a `results/tables.md`. |
| 5. Fundir Obs. 4.6 y 4.7 | Sí ("Detectability, not estimability; variants of the check"). |

Medidas adicionales para llegar a 12 páginas con letra normal:
- Bibliografía a dos columnas (sigue en `\footnotesize`, como en v0.3–v0.4), con `\bibsep` en 0pt.
- `titlesec` compacto.
- Colocación `[htb]` de la tabla de construcciones. La barrera de sección dejaba ≈40 % de la página 7 en blanco; esta fue la ganancia decisiva.
- Figura 1 al 66 % del ancho (antes 68 %).
- Algunas frases condensadas: primer párrafo de la introducción, "Three consequences", "What this says about the line's conclusion" y el procedimiento.

Se retiraron tres detalles menores del texto:
- la lista explícita de las marcas "borderline": las marcas siguen en la Tabla 3 y el recuento en el texto;
- la fórmula de SURE para el operador afín;
- la observación entre paréntesis sobre $\sup_u u\Phi(z-u)$ en la prueba de 4.2(iv).

Los márgenes son 0.8in/0.75in, como en v0.4. Probé 0.7in en vertical y lo descarté. Resultado: **12 páginas** (v0.4: 12, con el Apéndice B en letra menor). La tabla del barrido de desviación (Tabla 4) se mantiene en el texto.

## Estado del Teorema 5.1 y del Corolario 5.2 (acción 11)

Pasa a "proved here; checked by an independent internal referee (round 3)" en las etiquetas de estado de ambos, en la tabla de afirmaciones ("proved here; independent internal referee (round 3)…"), en limitaciones, en el veredicto, en la línea de fecha ("three rounds of internal review applied"), en README y en la ficha (ES/EN). En "Next steps" (a) se quitó "an independent referee of Theorem 5.1" y se añadió "conditions on the correction under which the transported refit beats the split". En CONTINUIDAD, el punto (a4) queda cerrado.

## Código, resultados y comprobación de macros

- `experiments/safe_reversion.py`: **no se tocó ni se reejecutó**; `results/results.json` no cambió.
- `theory/check_refit.py`: se añadieron las secciones **(d)–(h)**, que solo usan cuadratura y rejillas deterministas, sin extracciones aleatorias nuevas. Calculan la reducción colineal, el peor caso exacto de la partición, el oráculo, las familias adversariales sin ruido retenido y los 36 diseños con $\alpha=0.5$; además, la configuración del fallo Poisson se registra en el JSON. Se reejecutó: 82 s de pared, 86 s de CPU. Comprobado por programa: **todas las hojas previas de `results/refit_check.json` son idénticas** salvo `meta.seconds` y `meta.seconds_cpu`, y la salida de texto es idéntica hasta la sección (c).
- **SHA-256 congelado.** Cambia, porque el JSON gana claves nuevas y tiempos nuevos: `11939bb0…` → `944fc82f9ad3a6fe3b4f2bae1d44747a1233e6d79a55b5d4fcde9da43343231a`, registrado en `results/refit_check.json.sha256` y documentado en README y CONTINUIDAD.
- `experiments/make_numbers.py`: genera 777 macros (antes 635; ninguna eliminada) y 10 cuerpos de tabla. Es nuevo `table_oracle.tex`; cambian `table_worst_refit.tex` y `table_worst_split.tex`, que ahora escribe la fila completa porque `\multicolumn` no puede ir tras `\input`. Los otros 7 cuerpos son idénticos byte a byte. Se añadieron aserciones (corchete de (b), ausencia de celdas inconclusas, mismo fallo Poisson, 36/36 diseños, reducción, cocientes exactos ≤ 1).
- **Macros previas que cambian de valor (todas esperadas):** `RfSHA`, `RfSeconds` (89→82) y `RfCPU` (85→86) por la reejecución; `RfBetterText`, `RfWorseText` y `RfUnclearText` (m1: clasificación con el peor caso exacto); los 9 máximos de m5. Ninguna otra macro cambió.

## Compilación

`latexmk -pdf`: 0 errores, 0 referencias o citas indefinidas, 0 cajas desbordadas, `pdftotext main.pdf - | grep -c '??'` = 0. **12 páginas.** Revisé visualmente las páginas renderizadas 1 y 4–12 (Prop. 4.5(c), Tabla 1 con el bloque del oráculo, Obs. 5.3, tablas 2–4, Fig. 1, tabla de afirmaciones y apéndices). Se ejecutó `latexmk -c` (queda `main.pdf`).

## Queda abierto

Igual que tras la ronda 2, con estos cambios:
- **Cerrados:** (a4) árbitro independiente del Teorema 5.1; (h) peor caso exacto de la Prop. 4.5.
- **(a5), nuevo:** condiciones bajo las cuales el reajuste transportado mejora a la partición para una corrección dada.
- **(a6), nuevo:** demostrar o refutar que con $\alpha=0.5$ el peor caso del reajuste es siempre peor que el de la partición (solo numérico).
- **Siguen abiertos:** (a1)–(a3), (b)–(d), (f), (g) e (i) (véase CONTINUIDAD).

## Cómputo

- Script propio de verificación: ≈110 s de CPU.
- `check_refit.py`: 86 s.
- `make_numbers.py` y comparaciones: ≈5 s.
- Compilaciones LaTeX: ≈2 min en total.
- **Total: ≈5 min de CPU.**
