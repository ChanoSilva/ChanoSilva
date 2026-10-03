[EN CURSO]

# Informe de árbitro interno independiente — OMR001, ronda 3 (v0.4)

Fecha: 03/10/2026. Objeto: manuscrito v0.4 (commit `bfeefde`), con prioridad en la Sección 5 nueva (Teorema 5.1 `thm:refit`, Corolario 5.2 `cor:crossfit`, Observación 5.3 `rem:refitcost`, Tabla 1 `tab:worstrefit`, Apéndice B). Árbitro nuevo, independiente de los de las rondas 1 y 2 y del pase teórico que integró la Sección 5. Los números de línea se refieren a `manuscript/main.tex` de v0.4 salvo indicación. Trabajo auxiliar (scripts y salidas) en el scratchpad de la sesión, `referee3_OMR001/` (`indep_core.py`, `t1_identity_M.py` … `t10_misc.py`, `notes.md`); ninguno importa código del autor.

## Veredicto

**Cambios menores.** Las cuatro partes del Teorema 5.1 y el Corolario 5.2 son correctos: los verifiqué paso a paso y con un chequeo independiente (cuadratura condicional, Monte Carlo con observaciones crudas, optimización propia de $\Psi_\eta$ y $M_\eta$), sin contraejemplos en los bordes. Lo que falla es la lectura que el texto hace del resultado: "removes the split cost for each given correction" es falso para la corrección oráculo $C=\theta$ en el punto principal del diseño (M1), y un resultado adversarial desfavorable del cross-fitting se calculó pero no se reporta (M2). Ambos se corrigen con texto y con números que ya existen o que doy abajo. Una vez aplicados M1 y M2, el estado de `thm:refit` y `cor:crossfit` puede pasar a "proved here; checked by an independent referee (round 3)".

Recuento: 0 bloqueantes, 2 mayores, 9 menores. Ronda 2: 16 de 16 puntos bien aplicados (los 5 puntos de la ronda 1 que quedaron a medias o con error nuevo también están corregidos).

## 0. Verificación del Teorema 5.1 y del Corolario 5.2 (prioridad máxima)

### Paso a paso (lectura de firma)

| Paso | Ubicación | Resultado |
|---|---|---|
| Descomposición $\bar X_n-\theta=(1-\eta)e+\eta h$ y $\ell(\hat\theta_{\rm rf})-\ell(\bar X_n)=J((1-\eta)\Delta+\eta\|w\|^2+2\eta\langle w,h\rangle)$ | l.472 | Correcta ($J^2=J$; $2\langle w,e\rangle=\Delta-\|w\|^2$). |
| Integrabilidad (diferencia $\ge-\ell(\bar X_n)$) | l.474 | Correcta. |
| (i) $\langle w,h\rangle=(s/2)Z$, $J=\mathbf 1\{Z\ge z+u\}$, $E[J\langle w,h\rangle\mid\mathcal F]=(s/2)\varphi(z+u)$; segunda forma | l.253–254, l.475 | Correctas. La comprobé de forma independiente: integré $E_Z[J\cdot(\ldots)]$ directamente, sin pasar por la fórmula cerrada, en 720 pares $(e,w)$ con $\alpha\in\{10^{-6},10^{-3},0.01,0.1,0.3,0.5\}$ y $(n_e,m,d)\in\{(1,1,1),(1,99,3),(48,12,5),(2,1,50),(500,3,2),(5,5,200)\}$, incluidas la reflexión y $w=-0.3e$. La diferencia relativa máxima es $5\cdot10^{-7}$ (precisión de cuadratura). |
| (ii) $(1-\eta)\Delta+\eta\|w\|^2\le s(u+\eta\xi)$; $\Psi_\eta(\alpha;x)\le\Psi_\eta(\alpha;0)+x$; forma cerrada en tres casos | l.256–260, l.476 | Correctas. La desigualdad puntual $f\le2\omega\Psi_\eta(\alpha;\eta\xi)$ se cumple en 252 000 puntos aleatorios (máx. $-4\cdot10^{-13}$), y $\Psi_\eta\le\bar\kappa_\eta+x\Phi(x-z)$ en $\alpha\in[10^{-6},0.5]$ y $\eta\in[10^{-3},0.99]$ (máx. $-1.5\cdot10^{-5}$). |
| (iii) cambio de escala $\|w\|=\sigma\omega/\sqrt m$, $\Delta=\sigma^2\delta/m$; restricción $|\delta-\omega^2|\le2\xi\omega$ | l.261, l.477 | Correctos. La restricción implica $\delta\ge-\xi^2$ (es decir, $\ell(C)\ge0$), de modo que no falta ninguna restricción. |
| (iii) cota de $M_\eta$: casos $\omega\le2\xi$ y $\omega>2\xi$ ($u\ge\omega/2-\xi>0$) | l.261, l.477 | Correctos. $M_\eta\le$ forma cerrada en toda la rejilla de bordes (máx. relativo $\le0$). |
| (iii) forma promediada: $E\xi=c_d\sqrt{m/n_e}$, $E\xi^2=dm/n_e$, $E\xi^3=\mu_{3,d}(m/n_e)^{3/2}$, $\Phi(\eta\xi-z)\le\alpha+\eta\xi\varphi(0)$, término $4\alpha\,d\sigma^2m/(nn_e)$ | l.262–266, l.477 | Correctas, término a término. Comprobé la forma cerrada frente al tope exacto en 8 diseños de borde × 3 valores de $\alpha$ ($d$ hasta 200, $n_e=1$, $m=1$, $m=99$): siempre $\ge$ el exacto, con holgura entre ×1.01 y ×96 (m8). |
| (iv) reflexión $C=2\theta_0-R$: $w=-2e$, $\Delta=0$, $\pi=\alpha$, valor exacto | l.268, l.478 | Correctos. MC con observaciones crudas ($d=3$, $n_e=4$, $m=2$, $\sigma=1.3$, 200 000 réplicas, dos semillas): 1.3568 ± 0.0044 y 1.3550 ± 0.0043 frente a 1.352 exacto con $\alpha=0.5$; 0.3983 ± 0.0031 frente a 0.3921 con $\alpha=0.1$. El enunciado "no bound uniform in $C$ can be smaller than $4\alpha$ times the split cost" es exactamente lo que prueba la construcción. |
| (iv) alcance de $(\sigma^2/m)E[M_\eta]$ (selección medible, truncación en $\xi$, continuidad uniforme) | l.478 | Correcto, aunque la hipótesis $d\ge2$ sobra: el máximo está siempre en $c=\pm1$ (m2). |
| Cor. 5.2: $\frac1K\sum_kR_k=\bar X_n$ (requiere $n=Km$), Jensen, $\eta=1/K$, misma ley de $\xi$ | l.273–279, l.482 | Correctos. $\sum_kR_k=(Kn\bar X_n-n\bar X_n)/(n-m)=K\bar X_n$. Los $C_k$ deben ser independientes del pliegue $k$ dado $\theta$, y lo son por hipótesis. |
| Obs. 5.3(c), límite de la ruta "$C$ si pasa, si no $\bar X_n$" | l.284, l.485–488 | Lo rederivé. Mi cuadratura propia coincide con el MC con $t=10^{-6}$: 0.02199 ± 0.00005 frente a 0.02208 ($m=12$, $\alpha=0.1$; 1.06 veces el costo de partición) y 0.00874 frente a 0.00872 ($m=3$, $\alpha=0.5$). Con $t=10^{-3}$ el MC queda un 1 % por debajo; es el término $O(t)$ $-2tE[\|e\|^2J]$, no un error. |
| Tabla 1 (`table_worst_refit.tex`) | l.234–247 | Recalculé las 20 celdas del reajuste con mi propio $M_\eta$ y cuadratura sobre $\chi_d$, y las 20 coinciden a 4 decimales (p. ej. 0.0244, 0.1720, 0.3479, 0.0022). Los costos de partición (0.0044, 0.0093, 0.0208, 0.0556) también coinciden. |
| Pendiente $\Psi_{0.2}(0.1;0)=0.0405$ (Obs. 5.3(a)) | l.282 | Coincide. |

**Bordes explorados sin contraejemplo:** $n_e=1$; $m=1$; $m=99$ con $n_e=1$ ($\eta=0.99$); $\alpha=10^{-6}$ y $\alpha=0.5$; $d=1$ y $d=200$; reflexión, desplazamiento fijo, encogimiento hacia un centro erróneo, oráculo y familia del peor caso. Con "distribución de la prueba retenida" no encontré nada que señalar, porque el teorema exige observaciones retenidas gaussianas y lo dice (l.250). Para el umbral $z$ del chequeo, el teorema cubre $\alpha\le1/2$ ($z\ge0$), y el cierre usa $z\ge0$ en dos sitios (monotonía de $\varphi$ en $[0,\infty)$ y $\kappa_\varphi\le\varphi(1)$). Para $\alpha>1/2$ el cierre no vale tal cual, pero ese caso está excluido.

**Etiquetas de estado.** Dicen "proved here; not yet checked by an independent referee" (o su equivalente en español) en todos los sitios que revisé: fecha de portada (l.57), resumen (l.64), estado del Teorema 5.1 (l.270), Corolario 5.2 (l.278), veredicto (l.410), tabla de afirmaciones (l.430), limitaciones (l.442), README l.5 y l.41, FICHA l.3, l.11, l.13, l.22 y l.24, CONTINUIDAD l.113 y l.129. La variante "refit" de la simulación (operador reaplicado) se declara sin garantía en l.227, l.328, l.405, l.433, README l.5 y l.37 y FICHA l.11, l.22 y l.24. Todo está correcto.

## 1. Verificación de la ronda anterior (ronda 2)

| Hallazgo r2 | Estado | Evidencia (v0.4) |
|---|---|---|
| M1 (tasa $m^{-1/2}$ con $n_e$ fijo) | aplicado bien | Prop. 4.5(b) l.200–205 y prueba l.210; resumen l.64 "attained in order $m^{-1/2}$ for a fixed estimation sample"; tabla de afirmaciones l.426. |
| M2 (constantes $\kappa,\kappa_2$ óptimas) | aplicado bien | l.144, l.175–178, l.199; Tabla 6. |
| M3 (probabilidad conjunta del evento dañino) | aplicado bien | l.148; FICHA l.13 y l.24. |
| m1 (costo de partición, ¿respecto de qué?) | aplicado bien | l.328. |
| m2 (procedimiento) | aplicado bien | l.331, l.451. |
| m3 (valor condicional del regret) | aplicado bien | l.169. |
| m4 ("Theorem B") | aplicado bien | `grep "Theorem B" experiments/safe_reversion.py` no devuelve nada; las figuras están regeneradas. |
| m5 ("nearly identical") | aplicado bien | l.64, l.410; FICHA l.13. |
| m6 (leyenda de la Fig. 1(b)) | aplicado bien | l.380 (1.93 en $\kappa=12$, macro generada). |
| m7 (máximos redondeados hacia arriba) | aplicado bien en v0.3 | `pct_up` en `make_numbers.py` l.28. **Regresión en el contenido nuevo de v0.4** (véase m5). |
| m8 (dobles negaciones) | aplicado bien | l.397. |
| m9 ("Reversion also caps") | aplicado bien | l.394. |
| m10 (`\DSixteenAlwaysRatio`) | aplicado bien | l.400. |
| m11 (cifras de README/CONTINUIDAD) | aplicado bien | README l.30 y l.34; CONTINUIDAD l.40 y l.63. |
| m12 (estado de la ficha) | aplicado bien | FICHA l.11 y l.22; main l.445(c). |
| m13 (cita de Matplotlib) | aplicado bien | `hunter2007` en l.449; la entrada está verificada (Bibliografía). |
| Puntos de la ronda 1 que la ronda 2 dejó a medias o con error nuevo (B2, M3, M4, M5, m7) | aplicados bien | Se resolvieron mediante r2-M1, m1, M3, m2 y m3, ya verificados arriba. |

## 2. Hallazgos nuevos

### Bloqueantes

Ninguno.

### Mayores

**M1. "Removes the split cost for each given correction" es falso como comparación por corrección; el contraejemplo es el oráculo.**
*Ubicación:* resumen l.64 ("removes the split cost for each given correction"), introducción l.73 ("it can for each given correction"), Obs. 5.3(a) l.282 ("For each given correction the split cost is gone"), veredicto l.410, README l.41, FICHA l.13 y l.24, CONTINUIDAD l.125.
*Problema:* lo que demuestra el Teorema 5.1(ii) es que la **cota** no tiene término aditivo y se anula cuando $C\to R$. Eso no implica que el reajuste transportado pague menos que la partición para una corrección dada. El término $\eta\,E[s\varphi(z+u)-2\langle w,e\rangle\pi]$ de la identidad (i) es un efecto de selección: el chequeo pasa preferentemente cuando el ruido retenido apunta en la dirección que perjudica a $\bar X_n+w$. Además, $w=C-R$ corrige el error de $R$ y no el de $\bar X_n$. Para la corrección perfecta $C=\theta$ ($w=-e$, $\Delta=-\|e\|^2$, $u=-\xi/2$), la identidad (i) da exactamente
$$\mathcal R(\hat\theta_{\rm rf})-\mathcal R(\bar X_n)=\frac{\sigma^2}{m}\,E\Big[-(1-2\eta)\,\xi^2\,\Phi(\xi/2-z)+2\eta\,\xi\,\varphi(z-\xi/2)\Big],\qquad \xi\sim\sqrt{m/n_e}\,\chi_d,$$
frente a $\frac{d\sigma^2m}{nn_e}-\frac{\sigma^2}{m}E[\xi^2\Phi(\xi/2-z)]$ para el estimador con partición.
*Evidencia* (`t7_oracle.py`; la fórmula coincide con el MC de observaciones crudas, por ejemplo +0.0786 ± 0.0006 frente a +0.0775 con $d=3$, $n_e=4$, $m=2$, $\alpha=0.1$). Diseño $d=5$, $n=60$, riesgo de $\bar X_n$ = 0.0833, exceso sobre $\bar X_n$:

| $m$ | $\alpha$ | reajuste transportado, $C=\theta$ | partición, $C=\theta$ |
|---|---|---|---|
| 12 | 0.5 | −0.0342 | **−0.0558** |
| 12 | 0.1 | −0.0054 | **−0.0066** |
| 12 | 0.01 | +0.0002 | +0.0158 |
| 24 | 0.2 | **+0.0061** (dañino) | −0.0245 |
| 24 | 0.1 | **+0.0098** (dañino, 12 % del riesgo de $\bar X_n$) | −0.0012 |
| 24 | 0.05 | +0.0101 | +0.0166 |

En el punto principal del diseño ($m=12$, $\alpha=0.1$) y con la mejor corrección posible, la partición es **mejor** que el reajuste transportado; con $m=24$ y $\alpha\le0.2$, el reajuste transportado del oráculo es peor que no corregir. Con el operador EB ocurre lo mismo en la jerarquía sin desviación: con $m=24$, snr = 1 y $\kappa=0$, el reajuste da un exceso de +0.0035 ± 0.0002 sobre $\bar X_n$ (`theory/check_refit_output.txt`, fila "m_sw snr=1.0 dep=0.0 m=24"). Esto no se menciona; los párrafos de resultados solo reportan $m=12$ (l.405).
*Corrección:*
1. Resumen: sustituir "removes the split cost for each given correction, but in the worst case at least the fraction $4\alpha$ of it remains" por "removes the additive split cost from the bound, which becomes proportional to the size of the correction, but it is not better than the split for every correction (even the oracle correction $C=\theta$ can lose to the split, or to $\bar X_n$ when $m$ is large), and uniformly in $C$ at least $4\alpha$ times the split cost remains".
2. Obs. 5.3(a): "*The bound has no split-cost term*: …" en lugar de "For each given correction the split cost is gone". Añadir una Obs. 5.3(e) con la fórmula del oráculo de arriba y dos cifras generadas (por ejemplo, $m=12$, $\alpha=0.1$: −0.0054 frente a −0.0066; $m=24$, $\alpha=0.1$: +0.0098 frente a −0.0012). Las dos se pueden calcular por cuadratura en `check_refit.py` sin Monte Carlo.
3. Introducción l.73, veredicto l.410, README l.41, FICHA l.13 y l.24, CONTINUIDAD l.125: la misma corrección.
4. l.405: añadir la fila $m=24$, $\kappa=0$ (exceso +0.0035) para que el lector vea que el reajuste transportado puede ser dañino en la jerarquía.

**M2. Resultado adversarial desfavorable del cross-fitting calculado pero no reportado.**
*Ubicación:* l.403 ("satisfies Corollary 5.2 in all … adversarial combinations, loosely") y l.405 ("Cross-fitting … gains +29.4 % … never exceeds +0.0011"); README l.41 ("Cross-fitting … ganancia +29.4 % en snr 0").
*Problema:* `results/refit_check.json` → `adversarial_crossfit.max_over_split` = 9.39: con una corrección aditiva fija $\|v\|=2\sigma/\sqrt m$, $m=3$ y $\alpha=0.5$, el exceso del estimador con cross-fitting sobre $\bar X_n$ es 9.4 veces el costo de partición, es decir, la mitad del riesgo de $\bar X_n$. La macro `\RfAcfMaxSplit` (y `\RfAcfTenMin`/`\RfAcfTenMax` = 0.07–0.24 con $\alpha=0.1$) se genera pero no se usa en `main.tex`. El texto reporta solo los resultados favorables del cross-fitting (la ganancia en la jerarquía y el máximo en el barrido de desviación). La Obs. 5.3(d) dice que la cota inferior "does not carry over", y un lector puede entender que el cross-fitting no tiene ese problema.
*Evidencia:* lo reproduje con MC propio (100 000 réplicas, medias por pliegue): 0.04155 ± 0.00019, 9.47 veces el costo de partición 0.00439. Con $\alpha=0.1$ el valor es 0.25 veces, y con $m=12$, $\alpha=0.5$, 0.82 veces.
*Corrección:* en l.403, después de "loosely (…)", añadir "; it is not free of the split cost either: on the adversarial grid its excess reaches \RfAcfMaxSplit{} times the split cost (fixed additive correction, $m=\RfAcfMaxSplitM$, $\alpha=\RfAcfMaxSplitAlpha$), and \RfAcfTenMin–\RfAcfTenMax{} times at $\alpha=0.1$". Añadir lo mismo en una línea del README.

### Menores

**m1. El peor caso del estimador con partición es calculable exactamente: cierra el punto abierto (h) y resuelve las celdas "inconclusas" de la Tabla 1.**
El exceso condicional del estimador con partición sobre $R$ es $(\sigma^2/m)f_0(\omega,\delta)$, que es $f_\eta$ con $\eta=0$ (Teorema 4.2(i)). Con la reducción de m2, $M_0(\alpha;\xi)=4\sup_{u\ge0}(u^2+\xi u)\Phi(-(z+u))$, de modo que el peor caso sobre $\theta$ y $C$ es **exactamente** $\frac{d\sigma^2m}{nn_e}+\frac{\sigma^2}{m}E[M_0(\alpha;\xi)]$ y se alcanza con la misma construcción que en (iv). Los valores exactos sobre $R$ en el diseño (`t10_misc.py`) caen dentro de los corchetes de la Prop. 4.5(b): con $\alpha=0.1$, 0.0264 [0.0238, 0.0282], 0.0158 [0.0147, 0.0169], **0.0100 [0.0096, 0.0106]** y 0.0070 [0.0069, 0.0074] para $m=3,6,12,24$. Este último cierra el punto (h) de CONTINUIDAD. En la Tabla 1, $\alpha=0.1$ y $m=3$ da reajuste 0.0322 frente a partición exacta **0.0308** (el reajuste es peor), y $m=6$ da 0.0241 frente a **0.0250** (el reajuste es mejor). *Corrección:* añadir el enunciado exacto como Prop. 4.5(c) o como observación tras el Teorema 5.1, sustituir los corchetes de la Tabla 1 por el valor exacto (conservando el corchete en el texto si se desea) y actualizar `\RfBetterText`/`\RfWorseText`/`\RfUnclearText` y la fila de la tabla de afirmaciones (l.431): "below for $\alpha\le0.05$ and for $\alpha=0.1$ with $m\ge6$, above otherwise".

**m2. En (iv) sobra "$d\ge2$": el peor caso es colineal con $e$.**
Para $u$ fijo, $f_\eta=\eta\Phi(-(z+u))\,\omega^2+2\omega[(1-\eta)u\Phi(-(z+u))+\eta\varphi(z+u)]$ es una cuadrática convexa en $\omega$ sobre el intervalo admisible $\omega\in(\,2(u-\xi)^+,\,2(u+\xi)]$. Su máximo está en un extremo, es decir, en $c=-1$ o $c=+1$. Mi optimización bidimensional en $(\omega,c)$ y la unidimensional en $u$ coinciden (diferencia máxima $1.7\cdot10^{-15}$ en 96 casos), y el argmax de la rejilla 2-D tiene siempre $|c|=1$. *Corrección:* enunciar (iv) para todo $d\ge1$ y sustituir en la prueba la construcción con $\hat e_\perp$ por $w=(\sigma/\sqrt m)\,\omega(\xi)\,c(\xi)\,\hat e$, $c\in\{\pm1\}$. Conviene añadir la interpretación: el peor $C$ es $R+\lambda(\xi)(R-\theta_0)$, es decir, inflar o encoger el error de $R$, igual que en la Prop. 4.5(b). Además, $M_\eta$ pasa a ser un supremo unidimensional, lo que simplifica `check_refit.py`.

**m3. El "1 fallo Poisson en 71" del reajuste es el mismo fallo que el de la Sección 6, y no prueba el término nuevo; el $|z|=3.09$ es el número de excedencias esperado.**
(a) `theory/check_refit.py` l.280–285 compara el número de aceptaciones $\sum_iJ_i$ con $\sum_i\pi_i$, la misma prueba que `experiments/safe_reversion.py` l.302–312, con las mismas réplicas (el script lo verifica: "replica max diff 0.0") y el mismo $J$. El fallo es, por tanto, el ya declarado en l.394 (full pooling, $\alpha=0.05$, $m=6$, desviación $8\tau$: 19 aceptaciones frente a 37 esperadas, no reproducido con 50 semillas), y en las 71 combinaciones de aceptación rara el término $\eta s\varphi(z+u)$ de la identidad 5.1(i) no se prueba. (b) Con 440 pruebas $z$ y umbral 3, el número esperado de excedencias bajo identidad exacta es $440\cdot0.0027=1.19$ (P(al menos una) = 0.70), así que una excedencia es lo esperado; lo mismo vale para las 274 del diseño (0.74 esperadas). *Juicio:* están declaradas con honestidad, pero l.403 las presenta como evidencia separada sin contexto. *Corrección:* en l.403 escribir "… and the 1 Poisson failure among 71 rare-acceptance combinations, which is the acceptance-count test of Section 6 on the same replicates (same configuration; it does not test the term $\eta s\varphi(z+u)$) … (1 above the per-test threshold 3; 1.2 expected among 440 tests if the identity holds exactly)". Opcional: verificar la identidad por cuadratura condicional, como hice yo (720 pares, error relativo $\le5\cdot10^{-7}$), en lugar de hacerlo por Monte Carlo.

**m4. Los cocientes adversariales > 1 son ruido Monte Carlo; reportar valores exactos.**
l.403 cita "largest ratio 1.09 to the exact cap, at $\alpha=0.01$" y "0.98–1.07", "0.99–1.08". La familia "Prop4.5b" ($w=-2e-(2\sigma u^\ast/\sqrt m)\hat e$) es colineal y su exceso es una integral unidimensional sobre $\xi$. El valor exacto es **0.989** del tope con $m=3$, $\alpha=0.01$ (y 0.907–0.989 en otras celdas; `t8_adv.py`), no 1.086. *Corrección:* calcular por cuadratura el exceso de las familias colineales (reflexión, Prop4.5b, worst($M_\eta$)) y, para las demás, usar el estimador de Rao–Blackwell $E[\text{(i)}]$ (varianza solo de $e$). Así el texto puede decir "the worst family attains 0.99–1.00 of the exact cap" sin depender de "within two standard errors".

**m5. Máximos redondeados hacia abajo en las macros nuevas (regresión de r2-m7).**
`\DepTrTenMax` = 1.11 cuando el máximo es 1.1140 ($\kappa=8$, `gain_transported_vs_Rn` = −0.1140), y `\RfDesignMaxBc` = 0.86 cuando es 0.8619. Las frases correspondientes, "with risk at most 1.11 times" (l.405) y "largest ratios", citan cotas superiores. *Corrección:* usar `pct_up`/`ceil` también en las macros `Rf*` y `*Tr*`.

**m6. El resumen ha crecido y mezcla el orden.**
El resumen tiene 277 palabras en la fuente (v0.3: 222; r1-m14 pedía ≈200). El punto "(iv)" aparece detrás de la frase de la simulación ("…of the full-data reference risk; (iv)~Refitting…"), lo que rompe la enumeración. El paréntesis "(with plain hold-out the worst case is worse than with the split)" no lleva calificación, aunque la tabla de afirmaciones (l.431) lo etiqueta "numerical, design-specific". Mi barrido (`t5_general.py`) muestra que con $\alpha=0.5$ el reajuste es peor en el peor caso en los 36 diseños probados ($d\in\{1,2,5,50\}$, $n_e\in\{2,10,1000\}$, $m\in\{1,3,30\}$; cociente 1.001–3.28). La afirmación es, pues, robusta, pero no está probada. *Corrección:* mover (iv) justo detrás de (iii), escribir "(numerically, in every design we tried, the plain hold-out worst case is worse than with the split)" y recortar el resumen (por ejemplo, la frase sobre SURE y el operador reaplicado puede ir solo en el cuerpo).

**m7. Holgura de la forma cerrada de (iii) fuera de la rejilla.**
La forma cerrada no tiende a 0 cuando $\alpha\to0$, por el residuo $4\sigma^2\eta\varphi(0)c_d/\sqrt{n_em}+4\eta^2\varphi(0)\mu_{3,d}\sigma^2\sqrt m/n_e^{3/2}$, mientras que el tope exacto sí tiende a 0. En el diseño, con $\alpha=0.001$ y $m=12$, es ×94 el exacto; con $n_e$ pequeño, ×10–15 (`t3_bounds.py`). *Corrección:* añadir media frase en la Obs. 5.3(b): "the closed form is informative only for moderate $\alpha$ and $m\ll n_e$; for small $\alpha$ use the exact cap".

**m8. Apéndice B poco legible.**
La prueba del Teorema 5.1 (l.469–479) es un único párrafo de unas 40 líneas en `\small`, con márgenes de 0.8in. *Corrección:* separar (i)–(iv) en párrafos (`\par\noindent\textit{(ii)}`…) y volver al cuerpo normal tras los recortes de la sección 5.

**m9. Fórmula de M1 y diseño $m/n_e$.**
La limitación (l.442) debería decir que el reajuste transportado añade a $\bar X_n$ un vector calibrado para $R$, de modo que, cuando $m\ge n_e$ ($\eta\ge1/2$), incluso el oráculo aceptado siempre es peor que $\bar X_n$: su riesgo es $d\sigma^2m/(nn_e)$ frente a $d\sigma^2/n$. El diseño ($m/n_e=1/4$) está del lado favorable. Basta una frase.

## 3. Bibliografía

| Entrada | Estado | Corrección |
|---|---|---|
| `refs.bib` (19 entradas) | Sin cambios desde v0.3 (`git diff 1812e4c -- refs.bib` vacío); la Sección 5 no cita nada nuevo. | — |
| `hunter2007` (añadida en la ronda 2 "con datos que el autor conoce", no verificada en línea) | **Verificada** (búsqueda web: [Semantic Scholar](https://www.semanticscholar.org/paper/Matplotlib:-A-2D-Graphics-Environment-Hunter/412a0bb5a3baa91b62053d82c562bc172df0439f), [Citing Matplotlib](https://matplotlib.org/stable/project/citing.html)): Hunter, J. D., "Matplotlib: A 2D Graphics Environment", *Computing in Science & Engineering* 9(3):90–95, 2007, DOI 10.1109/MCSE.2007.55. Coincide con la entrada. | Ninguna; puede añadirse el DOI. |
| Resto | Verificadas en las rondas 1–2 según CONTINUIDAD l.55; ninguna sigue marcada "no verificada". | — |

## 4. Verificación computacional

Todo con scripts propios en `referee3_OMR001/`, sin importar código del autor. CPU total ≈ 2.7 min.

- **Identidad (i):** cuadratura directa sobre $Z$ frente a la fórmula cerrada en 720 pares de borde; error relativo máx. $5\cdot10^{-7}$ (15 s).
- **Reducción de $M_\eta$:** 2-D frente a 1-D en 96 casos; diferencia máx. $1.7\cdot10^{-15}$; argmax siempre con $|c|=1$.
- **Cotas (ii)/(iii) y formas cerradas:** puntuales en 252 000 puntos y en 6 × 6 × 7 valores $(\alpha,\eta,\xi)$; promediadas en 24 diseños de borde. Sin violaciones (67 s).
- **Tabla 1:** 20/20 celdas del reajuste coinciden a 4 decimales; peor caso exacto de la partición (m1) (16 s).
- **MC con observaciones crudas** ($d=3$, $n_e=4$, $m=2$, $\sigma=1.3$, 200 000 réplicas; reglas reflexión, $v$ fijo, EB hacia centro erróneo, oráculo y peor familia; $\alpha\in\{0.5,0.1,0.01\}$): identidad con $|z|\le2.35$ (otra semilla, $|z|\le1.73$) y tope respetado en 15/15 casos (6 s).
- **Cross-fitting** (MC propio): 9.47 veces el costo de partición reproducido (autor 9.39); cotas respetadas.
- **Obs. 5.3(c):** cuadratura propia frente a MC; coincide (véase la tabla de §0).
- **Reproducción:** `experiments/safe_reversion.py` completo en una copia: 14.1 s de pared y 13.9 s de CPU (el autor declara 14 s). `results.json` es **idéntico** al del repositorio en las 22 998 hojas (salvo tiempos). Frente a v0.3 oficial (`1812e4c`), las 19 854 hojas comunes son idénticas y hay 3 144 hojas nuevas (reajuste transportado), así que ningún número de v0.3 cambió. Nota: `bfeefde~1` (= `81f907d`, snapshot WIP) ya contiene el `results.json` de v0.4, de modo que la comparación pedida contra ese commit es trivialmente idéntica; la comparación relevante es contra `1812e4c`. `make_numbers.py` regenera las 635 macros y las 9 tablas idénticas byte a byte, y el SHA-256 de `refit_check.json` coincide (`11939bb0…`). No reejecuté `theory/check_refit.py` (85 s de CPU) por presupuesto; lo sustituye la verificación independiente anterior.
- **Compilación:** `latexmk -pdf` en una copia: 12 páginas, 0 avisos, 0 referencias o citas indefinidas, 0 "??".
- **Coincidencia observada:** `max_excess_over_bound_phi` = `max_regret_over_bound` = 0.40179… La revisé: ambas se alcanzan con $\alpha=0.5$ (pool, barrido en $m$), donde $z=0$ hace que la cota φ y la del regret coincidan y el oráculo elige $R$. No es un error.

## 5. Extensión y presentación

v0.4 tiene 12 páginas (objetivo 5–10). La Sección 5 justifica parte del exceso, pero no la forma de absorberlo: márgenes de 0.8/0.75in con líneas de unos 110 caracteres y pruebas en `\small` empeoran la lectura del resultado nuevo, que es justamente lo que hay que leer. Propongo volver a cuerpo normal en el Apéndice B y recortar:

1. **Figura 2** (exceso frente a cotas): sus números ya están en el texto (l.388, l.400). Pasarla a `results/` ahorra ≈1/3 de página.
2. **Tabla 6** (constantes) a `results/tables.md`; las macros que se citan ($\kappa$, $u^\ast$, $\varphi/\kappa$) siguen en el texto. Ahorra ≈1/4 de página.
3. **Obs. 5.3(c) y el párrafo final del Apéndice B** (ruta "$C$ si pasa, si no $\bar X_n$"): dejar una frase con la cifra 1.06 y mover la derivación a `theory/refit_derivation.md`. Ahorra ≈1/4 de página.
4. **Párrafo "Results: safety"** (l.394): los detalles de la re-verificación Poisson ya están en README y en `results/tables.md`. Ahorra ≈1/4 de página.
5. Fundir las Obs. 4.6 y 4.7.

Con 1–4 el texto queda en ≈11 páginas con el Apéndice B en cuerpo normal (o 10–11 conservando 0.8in). Los márgenes de 0.8in son aceptables para un borrador de trabajo; la letra menor en las pruebas nuevas no lo es.

## 6. Acciones, por prioridad

1. Reescribir "removes the split cost for each given correction" en el resumen, la introducción, la Obs. 5.3(a), el veredicto, README, FICHA y CONTINUIDAD; añadir la Obs. 5.3(e) con la fórmula del oráculo y las cifras $m=12$ y $m=24$, y la fila $m=24$, $\kappa=0$ del operador EB (M1).
2. Reportar en l.403 y en el README el máximo adversarial del cross-fitting (9.4 veces el costo de partición) con las macros ya generadas (M2).
3. Sustituir los corchetes de la Tabla 1 y de la Prop. 4.5(b) por el peor caso exacto de la partición, $\frac{d\sigma^2m}{nn_e}+\frac{4\sigma^2}{m}E[\sup_{u\ge0}(u^2+\xi u)\Phi(-(z+u))]$; cerrar el punto (h) y actualizar la fila l.431 (m1).
4. Enunciar el Teorema 5.1(iv) para todo $d$, con el peor caso colineal, y simplificar la prueba (m2).
5. Describir en l.403 el fallo Poisson como la misma prueba y configuración de la Sección 6, y dar el número esperado de excedencias $|z|>3$ (m3).
6. Calcular por cuadratura o por Rao–Blackwell los excesos de las familias adversariales y retirar los cocientes > 1 (m4).
7. Redondear hacia arriba las macros de máximos nuevas (m5).
8. Recortar el resumen a ≈220 palabras, reordenar (iv) y calificar el paréntesis de $\alpha=0.5$ (m6).
9. Añadir la frase sobre la holgura de la forma cerrada y la frase sobre $m\ge n_e$ en limitaciones (m7, m9).
10. Aplicar los recortes 1–4 de §5 y devolver el Apéndice B a cuerpo normal, en párrafos por parte (m8).
11. Tras 1–4, cambiar el estado de `thm:refit` y `cor:crossfit` (l.270, l.278, l.430, l.442, resumen, README, FICHA, CONTINUIDAD) a "proved here; checked by an independent referee (round 3)". Las cuatro partes y el corolario quedan confirmados por este informe.
