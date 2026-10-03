# Informe de árbitro interno — OMR001, ronda 1 (30/09/2026; emitido 02/10/2026)

Material revisado: `README.md`, `CONTINUIDAD_OMR001_20260930.md`, `FICHA_OMR001_propuesta.md`, `manuscript/main.tex` (421 líneas; las referencias `l.N` son a ese archivo), `manuscript/refs.bib`, `manuscript/numbers.tex` y `table_*.tex`, `experiments/safe_reversion.py`, `experiments/make_numbers.py`, `results/results.json`, `results/tables.md`, `main.pdf` (14 páginas renderizadas). Archivos de trabajo del árbitro en `scratchpad/referee_OMR001/` (`check_constants.py`, `check_macros.py`, `repro/`, `build/`, `notas_*.md`). No se modificó nada en la carpeta salvo la creación de este informe.

## Veredicto

**Cambios mayores.** Las matemáticas son correctas (cada paso del Teorema 3.1, Lema 4.1, Teorema 4.2, Corolario 4.3, Proposiciones 4.4 y 5.1 se verificó a mano y, donde procede, numéricamente) y los 30 números muestreados del texto coinciden con `results.json`; pero (i) la ficha propuesta y el párrafo de cierre afirman más de lo que el cuerpo demuestra, (ii) un enunciado de la Proposición 4.4 repetido en el resumen es falso tal como está escrito, (iii) el barrido en $m$ confunde el efecto de $m$ con el de $\tau$, y (iv) el manuscrito tiene 14 páginas para un objetivo de 5–10.

## Hallazgos bloqueantes

**B1. La ficha cierra la línea y el manuscrito no lo demuestra ni lo decide.**
- Ubicación: `FICHA_OMR001_propuesta.md` l.9 y l.21 ("Estado: Cerrada con nota técnica"); `main.tex` l.235 ("We therefore regard the closing statement of the line as established rather than merely prudent"); l.410 paso (d) ("Decide whether the line should be closed with this note or continued only along (a)–(b)"); `README.md` l.5 ("un cierre honesto: la ficha tenía razón").
- Problema: lo demostrado (Prop. 5.1 + Teorema 4.2) es que la *garantía de seguridad* del estimador con reversión es una garantía de selección entre dos candidatos, indiferente al operador. Eso no demuestra que "no exista diferenciación suficiente" de los operadores frente a combinaciones existentes: esa es una afirmación sobre el conjunto de operadores posibles, de la cual el manuscrito sólo examina tres (EB afín, agrupamiento, $\lambda$ fijo). El propio manuscrito deja dos problemas teóricos abiertos (l.410 (a)–(b): cota finita para el reajuste y para la reversión por SURE) cuya resolución cambiaría la conclusión práctica ("recuperar el costo de la partición con garantía"). El mismo documento no puede decir "established" en l.235 y "decide whether" en l.410; y la ficha, escrita antes que el manuscrito (08:49 frente a 08:55 según las fechas de los archivos), toma la decisión que el manuscrito no toma.
- Corrección: (1) en l.235 sustituir "We therefore regard the closing statement of the line as established rather than merely prudent" por "This explains why no differentiation should be expected from the safety mechanism itself; differentiation, if any, must come from the operator family, which this note does not explore beyond three affine instances." (2) En la ficha, estado "Nota técnica (borrador v0.1, sin revisión externa); línea en pausa salvo los puntos abiertos (a)–(b)" o bien "Cerrada" sólo después de que el autor decida explícitamente (paso (d)) y se eliminen (a)–(b) de los "próximos pasos". (3) En README l.5 sustituir "un cierre honesto: la ficha tenía razón" por "una formalización que hace precisa la conclusión de la ficha".

**B2. Enunciado falso tal como está escrito en la Proposición 4.4 y en el resumen.**
- Ubicación: l.140 ("no held-out check of size $m$ makes the worst-case harm $o(\sigma\E\|C-R\|/\sqrt m)$ uniformly over correction operators"); l.61 (resumen: "so the harm cannot be made $o(m^{-1/2})$ uniformly over operators"); l.72 ("The rate and the dependence on $\|C-R\|$ cannot be improved uniformly over operators").
- Problema: la demostración (l.189–191) construye el par $(R,C)$ para el test unilateral con margen $c=z_{1-\alpha}s$ a nivel $\alpha$ fijo. Un chequeo con margen mayor (en el límite, "nunca usar $C$") tiene daño cero; la afirmación sólo vale dentro de la clase de chequeos de nivel $\alpha$ fijo (o, más en general, con potencia acotada inferiormente). Lo que sí está demostrado y es interesante: dentro de esa clase, la constante $\varphi(z)$ no puede bajarse de $\kappa(\alpha)$ y el peor caso es una corrección *pequeña* ($u^\ast\in[0.34,0.75]$, Tabla 8), no una grande.
- Corrección: en l.140 escribir "and, for the one-sided check at any fixed level $\alpha\in(0,\tfrac12]$, no choice of $m$ makes the worst-case harm $o(\sigma\E\|C-R\|/\sqrt m)$ uniformly over correction operators; a check with a larger margin trades this for the regret term of Theorem 4.2(iv)". Misma cualificación en l.61 y l.72. Verificación numérica del árbitro: $\kappa(\alpha)\le\varphi(z)$ y la cadena de Mills de l.165 se cumplen punto a punto para $u\in\{0.01,\dots,10\}$ y $\alpha\in\{0.5,0.1,0.01\}$; los valores de la Tabla 8 coinciden con una rejilla independiente de $3\cdot10^6$ puntos (`check_constants.py`).

## Hallazgos mayores

**M1. El barrido en $m$ (Tabla 6, l.301–312, texto l.365) confunde $m$ con $\tau$.**
- Evidencia: `safe_reversion.py` l.100–103 define $\tau^2=\mathrm{snr}\cdot\sigma^2/n_e$ con $n_e=n-m$; a snr $=1$ fijo, $\tau^2$ vale 0.0175, 0.0185, 0.0208, 0.0278 para $m=3,6,12,24$, y el desplazamiento "$8\tau$" vale 1.06, 1.09, 1.16, 1.33. Por eso las columnas "always" (0.0448→0.0535) y "SURE" (0.0535→0.0600) de la Tabla 6, que no usan la partición, varían con $m$: coinciden con el riesgo de Bayes oráculo $d/n\cdot n/(n+n_e)$ = 0.0427, 0.0439, 0.0463, 0.0521.
- Corrección: fijar $\tau^2=\sigma^2/48$ (el valor de $m=12$) para todos los $m$ en `run_all()` (l.273–278: pasar `tau2` explícito a `simulate` en lugar de recalcularlo desde $n_e$) y regenerar la Tabla 6; o, como mínimo, añadir a la leyenda "snr is defined relative to $n_e$, so $\tau$ grows with $m$; the always/SURE columns move for that reason only". La conclusión cualitativa (la partición cuesta más de lo que el test recupera) se mantiene, pero los números de l.365 cambiarán.

**M2. La cota $\varphi$ no es uniforme en $\theta$ para operadores de encogimiento, y el texto sugiere que lo es.**
- Ubicación: l.130–131 ("Reversion is meant to cap this term; Section 4 says by how much"); leyenda de la Figura 2 (l.350: "every reverting estimator stays within a bounded factor of the reference"); l.72.
- Evidencia: para $C=\hat\mu+\lambda(R-\hat\mu)$, $\E\|C-R\|=(1-\lambda)\E\|R-\hat\mu\|$ crece linealmente con la desviación; en la Tabla 5 la cota $\varphi$ pasa de 0.0226 ($\kappa=0$) a 0.1204 ($\kappa=16$) y la cota $\alpha$ a 0.1334, mientras el exceso realizado nunca supera 0.0044. El Teorema 4.2 cambia un daño $O(\|\theta-\mu\|^2)$ por una cota $O(\|\theta-\mu\|/\sqrt m)$; el "factor acotado" de la Figura 2 es empírico.
- Corrección: decirlo en l.131 y en la leyenda de la Figura 2 ("the bound of Theorem 4.2 grows with $\E\|C-R\|$; the uniform boundedness seen here is not proved"). Opcional y recomendable: demostrar la cota uniforme en $\theta$, que es elemental con la estructura $C-R$ frente a $\Delta$: $\Delta=\|C-R\|^2+2\langle C-R,R-\theta\rangle\ge\|C-R\|^2-2\|C-R\|\|R-\theta\|$, de modo que $u=\Delta/s\to\infty$ cuando $\|C-R\|\to\infty$ y $\Delta^+\pi\to0$; el supremo en $\|C-R\|$ depende sólo de $\sigma_e\sqrt d$, $\sigma/\sqrt m$ y $\alpha$. Eso daría el "cap" que la Observación 4.6(c) dice no necesitar.

**M3. Corolario 4.3 (l.174–180): "a fraction $m/n_e$ of the reference risk" es incorrecto con la definición de referencia del manuscrito.**
- Evidencia: el costo de partición es $d\sigma^2m/(nn_e)=0.0208$; dividido por el riesgo de $R$ ($d\sigma^2/n_e=0.1042$) da $m/n=0.20$; dividido por el de $\bar X_n$ ($d\sigma^2/n=0.0833$) da $m/n_e=0.25$. En el manuscrito "the reference" es $R=\bar X_e$ (Def. 2.1(a)). El 25 % del resumen (l.61, macro `\SplitCost`), de l.365 y del README es correcto *respecto de $\bar X_n$*.
- Corrección: en l.180 "a fraction $m/n_e$ of the full-data risk $d\sigma^2/n$ (equivalently $m/n$ of the risk of $R$)"; en l.61 y l.365 "of the full-data reference risk".

**M4. Ficha: tres imprecisiones en "Principales hallazgos" (l.11 y l.23).**
- "(demostrado; verificado en 345 configuraciones)" se aplica también a "la constante es óptima salvo un factor explícito": las 345 combinaciones verifican las cotas, no la optimalidad; las constantes $\kappa(\alpha)$ se verifican por optimización escalar en 5 valores de $\alpha$. Separar: "cotas verificadas en 345 combinaciones; constantes calculadas numéricamente".
- "en una o dos dimensiones toda regla que use alguna vez la corrección es peor que la referencia en algún punto" omite la hipótesis del Teorema 3.1(c): fuentes cuya ley no depende de $\theta$ (o, equivalentemente, riesgo frecuentista con $\theta$ libre). Añadir "con fuentes no informativas sobre $\theta$".
- "la probabilidad de transferencia dañina es ≤ α" sin definición: el evento (l.150) es "se usa $C$ y la *pérdida realizada* de $C$ supera la de $R$", y la cota informativa es $\alpha\,\Prob(\Delta>0)$ (a snr $=1$, $\Prob(\Delta>0)=17.7\,\%$ aunque corregir siempre reduce el riesgo un 48 %). Escribir "la probabilidad de usar la corrección cuando su pérdida realizada supera la de la referencia es ≤ α·P(Δ>0) ≤ α".

**M5. Cambio a posteriori en el procedimiento de verificación, no declarado en el manuscrito.**
- Evidencia: `CONTINUIDAD` l.47–48 admite que la verificación de la identidad pasó de test $z$ a intervalo de Poisson en eventos raros después de ver "|z| enormes"; el manuscrito (l.362 y Apéndice A) presenta el intervalo de Poisson como diseño. Los umbrales $|z|\le3$ (`safe_reversion.py` l.234), Poisson 99 % (l.237) y la tolerancia de 2 EE en el criterio S (l.220–225) no constan como prefijados en ningún sitio. No encontré indicios de cambios en el criterio U (umbral 5 %, IC pareado 95 %, denominador $\bar X_n$): el script (l.23–31) y el JSON (`criteria`) lo documentan y las fechas (script 08:42:51 → resultados 08:43:11) son coherentes con una sola corrida final; no existen logs de corridas previas.
- Corrección: una frase en el Apéndice A: "The Poisson comparison for rare acceptance replaced a paired $z$-test after a first run showed that the normal approximation fails there; criteria U and S were fixed before the runs." Diagnóstico del árbitro sobre la identidad: 273 tests $z$ con 15 valores $|z|>1.96$ (esperados 13.7) y 4 con $|z|>2.58$ (esperados 2.7); 2 fallos de 72 intervalos Poisson al 99 % (esperados 0.7, $p\approx0.16$) y re-simulación con $z=+1.27$: compatible con ruido, la identidad se sostiene.

**M6. Extensión: 14 páginas para un objetivo de 5–10** (véase "Recortes propuestos").

## Hallazgos menores

- **m1.** Teorema 3.1(c), l.107 y l.119: la demostración es correcta, incluidos los dos puntos de atención. (i) No se necesita suficiencia: $\tilde\delta(X)=\E[\delta(X,D)\mid X]$ es un estimador legítimo porque la ley condicional de $D$ dado $X$ es $Q$, libre de $\theta$; la identidad $\risk(\theta,\delta)=\risk(\theta,\tilde\delta)+\E\|\delta-\tilde\delta\|^2$ es Pitágoras para la esperanza condicional y necesita riesgo finito (si es infinito, la conclusión es trivial). (ii) Las reglas aleatorizadas están cubiertas porque una aleatorización auxiliar $U$ es un caso particular de $D$. Ninguna de las dos cosas se dice: añadir una frase ("$D$ may include auxiliary randomisation, so randomised rules are covered; estimators with infinite risk satisfy the claim trivially"). La positividad "for all $\theta$ once it is positive for one" vía equivalencia mutua de las $P_\theta$ es correcta; la atribución Blyth (1951) para $d=1$ y Stein (1956) para $d=2$ es la estándar.
- **m2.** Teorema 3.1(b), l.109: añadir $\E\|b(D)\|^2<\infty$ (o leer la igualdad en $[0,\infty]$); el término cruzado necesita integrabilidad (Cauchy–Schwarz).
- **m3.** Lema 4.1 y Teorema 4.2: la independencia $\bar Y\perp\mathcal F\mid\theta$ (l.82, l.143) es exactamente lo que usa la ley condicional $N(\Delta,s^2)$ y se cumple en el diseño simulado (`safe_reversion.py` l.108–121: fuentes, $\bar X_e$ y $\bar Y$ con ruidos independientes dado $\theta$). Correcto. Para el *reajuste* la muestra retenida entra en el estimador final y la hipótesis falla; está declarado (l.240), pero conviene decirlo en la misma frase que presenta la variante ("the independence hypothesis of Theorem 4.2 fails for refit").
- **m4.** Def. 2.1(c) l.96 usa $C$ cuando $\widehat D=-c$; Prop. 5.1 l.208 dice "ties resolved toward $R$". Evento de medida cero, pero inconsistente: cambiar l.208 a "toward $C$" o l.96 a $\widehat D<-c$.
- **m5.** Observación 4.5 l.194: "with a beneficial $v$ this ratio is $\|v\|\sqrt m/(2\sigma)$ whatever the dimension" sólo vale si $\Delta=-\|v\|^2$ (la corrección cancela exactamente el error de $R$); escribirlo.
- **m6.** Observación 3.2 l.125: con $(\mu,\tau^2)$ fijos, la ley de $D$ *no* depende de $\theta$ (los $\theta_s$ son independientes de $\theta$), así que el Teorema 3.1(a) se aplica también al modelo simulado en sentido frecuentista; las fuentes informan sobre el prior, no sobre $\theta$. Reescribir "the sources are informative about θ through μ and τ²" como "the sources are informative about the task distribution, which is what the Bayes risk rewards".
- **m7.** Teorema 4.2(iv), l.171: la rama $\Delta<0$ está acotada por $s(z+\varphi(0))$ pero $\sup_u u\Phi(z-u)$ vale 0.17, 0.44, 0.64, 0.84, 1.26 frente a 0.40, 1.24, 1.68, 2.04, 2.73: la constante del regret es holgada en un factor $\approx2$. No es error; si se quiere, sustituir por $\max\{\varphi(0),\sup_u u\Phi(z-u)\}$ calculado numéricamente.
- **m8.** Tabla 1, fila SURE (l.224): "no finite-sample selection bound in general" no tiene cita; suavizar a "no finite-sample selection bound used here".
- **m9.** Criterio U en el filo: refit $\alpha=0.1$ a snr $=1$ (ganancia +6.1 %, IC inferior +5.8 %), rev $\alpha=0.5$ a snr $=2$ (+7.1 %, inf. +6.5 %), SURE a snr $=8$ (+6.9 %, inf. +6.6 %), refit $\alpha=0.2$ a snr $=4$ (+4.2 %, inf. +4.0 %, no útil). La reproducción rápida ($R=4000$) cambia el primero. Reportar el extremo inferior del IC en las tablas (o añadir "borderline") para que "refit useful up to snr $=1$" (l.365, l.371) no se lea como robusto.
- **m10.** Criterio S frente a la "cota identidad" $\E[\Delta^+\pi]$: en el régimen $\Delta>0$ c.s. compara dos estimadores Monte Carlo de la misma cantidad (34/345 combinaciones exceden la cota sin tolerancia, todas dentro de 2 EE). Decir en l.362 que ahí la verificación es de la identidad (i), no de una cota.
- **m11.** `CONTINUIDAD` l.34 escribe "+0.0042 ± 0.0003" y la Tabla 5 "±0.0002" (JSON: 0.00025). Unificar.
- **m12.** Apéndice A l.417: $\kappa(\alpha)$ se maximiza en $[0,20]$; $u^\ast\le0.76$, correcto, pero decir que el intervalo contiene el máximo.
- **m13.** `\citet[Ch.~8]{devroye1996}` (l.214): no pude verificar el capítulo; la selección por muestra retenida entre $K$ candidatos con $\sqrt{\log K/m}$ está en §8.4 "Selecting classifiers" o en el Cap. 22 "Splitting the data" según la edición; comprobar y citar la sección.
- **m14.** Resumen (l.61) de ~400 palabras con tres fórmulas: reducir a ≤200 palabras y dejar las constantes para el cuerpo.
- **m15.** Cajas desbordadas en la recompilación (`build/manuscript/main.log`): l.88–89 (9.9 pt, margen de la Def. 2.1(c)), l.290–297 (2.4 pt, Tabla 5), l.416–417 (5.9 pt, Apéndice). Tabla 1: columnas `p{}` justificadas producen espaciado irregular ("Reverting estimator (this note)"); usar `>{\raggedright\arraybackslash}p{}`.
- **m16.** Código, sin errores que invaliden resultados: no hay fuga entre fuentes/estimación y muestra retenida (l.108–121), los hiperparámetros del operador se estiman sólo con fuentes (l.110–114), la fórmula SURE (l.140) es correcta para $\hat\lambda_n,\hat\mu$ independientes del objetivo, los números aleatorios comunes se usan sólo dentro de una configuración (l.249–280), los IC son pareados (l.156–162) con denominador de EE relativo <1 % (0.44 %). Única observación de diseño: M1.

## Bibliografía

Crossref (`api.crossref.org`) y arXiv están bloqueados por el proxy de egreso de esta sesión (403/EGRESS_BLOCKED); verificación con WebSearch (Project Euclid, Taylor & Francis, Wiley, IEEE, Springer).

| Entrada | Estado | Corrección |
|---|---|---|
| stein1956 | verificada (Proc. 3rd Berkeley Symp., vol. 1, 197–206; incluye admisibilidad en $d=2$) | — |
| jamesstein1961 | verificada (Proc. 4th Berkeley Symp., vol. 1, 361–379) | — |
| stein1981 | verificada (Ann. Statist. 9(6):1135–1151; DOI 10.1214/aos/1176345632) | — |
| blyth1951 | verificada (Ann. Math. Statist. 22(1):22–42; DOI 10.1214/aoms/1177729690) | — |
| baranchik1970 | verificada (Ann. Math. Statist. 41(2):642–645; DOI 10.1214/aoms/1177697104) | — |
| efronmorris1972 | verificada (JASA 67(337):130–139; DOI 10.1080/01621459.1972.10481215) | — |
| efronmorris1973 | verificada (JASA 68(341):117–130) | — |
| efronmorris1975 | verificada (JASA 70(350):311–319) | — |
| morris1983 | verificada (JASA 78(381):47–55) | — |
| hoeffding1963 | verificada (JASA 58(301):13–30; DOI 10.1080/01621459.1963.10500830) | — |
| arlotcelisse2010 | verificada (Statist. Surv. 4:40–79; DOI 10.1214/09-SS054) | — |
| panyang2010 | verificada (IEEE TKDE 22(10):1345–1359) | — |
| licaili2022 (marcada "de memoria" en la nota) | verificada (JRSS-B 84(1):149–173, 2022) | — |
| devroye1996 | obra verificada (Springer 1996); capítulo citado no verificable en línea | comprobar "Ch. 8" (véase m13) |
| lehmanncasella1998 | no verificable en línea en esta sesión; datos estándar (2.ª ed., Springer, 1998) | — |
| lehmannromano2005 | no verificable en línea en esta sesión; datos estándar (3.ª ed., Springer, 2005) | — |
| virtanen2020 | no verificable en línea en esta sesión; datos estándar (Nat. Methods 17:261–272) | — |
| harris2020 | no verificable en línea en esta sesión; datos estándar (Nature 585:357–362) | — |

Uso de las citas: cada cita respalda la afirmación para la que se usa; la única imprecisión es el capítulo de Devroye et al. (m13). La atribución de la admisibilidad ($d=1$ Blyth 1951, $d=2$ Stein 1956) es correcta.

## Verificación computacional

- `check_constants.py` (<1 s): $\kappa(\alpha)$, $u^\ast$, $\kappa/\varphi$ de la Tabla 8 reproducidos con optimizador y rejilla; cadena de Mills (l.165) verificada punto a punto; constante de Hoeffding $B/\sqrt{em}$ y de Chebyshev $s/(4z)$ exactas; fracciones del costo de partición (M3).
- `check_macros.py` (<1 s): 30 macros de `numbers.tex` recomputadas desde `results.json` de forma independiente de `make_numbers.py`: 30/30 coinciden (`SplitCost`, `CnConfigs`, `MaxExcessOverPhi`, `MaxIdentityZ`, `NIdentityFail`, `SOneAlwaysGain`, `SOneRevTenGain(E)`, `WorstRatioAlways`, `DEightRevTen*`, `MThreeEight*`, `HarmMaxTen`, `UsefulRevTen`, `UsefulSure`, `RecheckZ`, etc.). Sin tolerancia: 0/345 combinaciones violan la cota $\varphi$, 0/345 la cota de frecuencia de eventos dañinos, 34/345 exceden $\E[\Delta^+\pi]$ (todas dentro de 2 EE; m10). Los cuerpos de tabla `table_*.tex` coinciden con `tables.md`.
- Reproducción rápida: copia de `experiments/` en `scratchpad/referee_OMR001/repro/`, `python3 safe_reversion.py --fast` ($R=4000$, 10 semillas de re-chequeo): 9.1 s de pared, 6.5 s de CPU usuario. Mismas versiones (NumPy 2.4.6, SciPy 1.17.1, Matplotlib 3.11.2). Coincidencia: 30 magnitudes comparadas (riesgos de $\bar X_n$, always, rev 0.1, SURE en snr 0/1/4/16; always, rev 0.1, exceso y frecuencia dañina en $\kappa$ 4/8/16) dentro de 3 EE de la corrida completa (máximo 2.98 EE en $\bar X_n$ a snr 0, con flujo aleatorio distinto); banderas de seguridad idénticas (todas verdaderas); máx. exceso/cota $\varphi$ 0.43 frente a 0.42; $|z|_{\max}$ 2.98 frente a 2.96; fallos Poisson 0 frente a 2; conjuntos "útiles" idénticos para rev (todas las $\alpha$), always y SURE; única diferencia: refit $\alpha=0.1$ útil hasta snr 0.5 en vez de 1 (caso en el filo, m9). Constantes idénticas.
- Recompilación en `build/manuscript/` (pdflatex ×2 con el `.bbl` existente): 14 páginas, sin referencias indefinidas ni citas faltantes, 3 cajas desbordadas (m15).
- Fechas de archivos: `safe_reversion.py` 08:42:51 → `results.json` 08:43:11 → figuras 08:43:14 → `FICHA` 08:49 → `make_numbers.py` 08:54 → `main.tex`/`numbers.tex` 08:55:42 → `README`/`CONTINUIDAD` 08:56 → `main.pdf` 08:57. Coherente con una única corrida final; sin logs previos (M5).

## Recortes propuestos para llegar a ≤ 10 páginas

1. Pasar a un apéndice (o a `results/tables.md`) las tablas de verificación 3, 5 y 7 (l.260–271, 288–299, 314–325) y la Tabla 8 de constantes (l.327–338): −1.5 pp. Dejar en el cuerpo las Tablas 2 y 4 y la Figura 3, que bastan para S, U y H.
2. Fusionar las Figuras 1 y 2 en una sola de 2×2 (o suprimir los paneles (b), que repiten las columnas "refit"/"SURE" de las Tablas 2 y 4): −0.5 pp.
3. Sustituir la Tabla 9 (l.375–404, una página) por una lista de seis líneas al final de la Sección 1 o por las etiquetas `\status{}` que ya lleva cada enunciado: −0.8 pp.
4. Fusionar l.214 ("Three consequences follow…") con l.234–235 ("Why the line's conclusion is correct") en un solo párrafo; mover los párrafos "Draws" y "Statistics" del Apéndice (l.416–417) al README: −0.5 pp.
5. Resumen a ≤200 palabras (m14) y lista de la Introducción (l.70–75) a tres líneas: −0.4 pp.
6. Tabla 1 (constructos) a 4 columnas estrechas con `\raggedright` y sin la fila "Hold-out selection" (es la propia construcción, Prop. 5.1): −0.2 pp.

Total estimado: 14 → 10 páginas sin perder ningún número ni demostración.

## Alcance

Coherente con la ficha pública: no se afirma mejora general, garantía de transferencia ni nada sobre poblaciones reales (l.61, l.399, l.407; ficha "Alcance actual"). Las únicas afirmaciones que exceden lo demostrado son las de B1, B2, M2 y M4.

## Lista de acciones (por prioridad)

1. Cambia el estado de la ficha a "Nota técnica (borrador v0.1); en pausa salvo los puntos abiertos (a)–(b)" o decide y documenta explícitamente el cierre en el manuscrito (paso (d), l.410) antes de usar "Cerrada".
2. Reescribe l.235 ("established rather than merely prudent") y README l.5 ("la ficha tenía razón") en términos de "explica por qué no cabía esperar diferenciación del mecanismo de seguridad".
3. Cualifica la Proposición 4.4 (l.140), el resumen (l.61) y l.72: "for the one-sided check at any fixed level α".
4. Fija $\tau^2=\sigma^2/48$ para todos los $m$ en `run_all()` (l.273–278) y regenera la Tabla 6 y los números de l.365; si no, declara en la leyenda que $\tau$ crece con $m$.
5. Corrige el Corolario 4.3 (l.180), l.61 y l.365: el 25 % es fracción del riesgo de $\bar X_n$; respecto de $R$ es $m/n=20\,\%$.
6. Añade en l.131 y en la leyenda de la Figura 2 que la cota del Teorema 4.2 crece con $\E\|C-R\|$ y que la acotación uniforme observada no está demostrada; opcionalmente demuestra la cota uniforme en $\theta$ con $\Delta\ge\|C-R\|^2-2\|C-R\|\,\|R-\theta\|$.
7. Separa en la ficha "cotas verificadas en 345 combinaciones" de "constantes calculadas numéricamente"; añade la hipótesis de fuentes no informativas al enunciado para $d\le2$; define el evento de transferencia dañina (pérdida realizada) y da la cota $\alpha\,P(\Delta>0)$.
8. Declara en el Apéndice A que el intervalo de Poisson sustituyó al test $z$ tras una primera corrida, y que U y S se fijaron antes de las corridas.
9. Añade al Teorema 3.1 la frase sobre aleatorización auxiliar y riesgo finito (m1) y la hipótesis $\E\|b\|^2<\infty$ en (b) (m2).
10. Unifica el tratamiento del empate entre Def. 2.1(c) y Prop. 5.1 (m4); precisa la Observación 4.5 (m5) y la Observación 3.2 (m6).
11. Añade el extremo inferior del IC a las Tablas 2 y 4 o marca los casos en el filo (m9); señala en l.362 que la comparación con $\E[\Delta^+\pi]$ es una prueba de identidad (m10).
12. Aplica los recortes 1–6 para bajar a ≤10 páginas; corrige las tres cajas desbordadas y el espaciado de la Tabla 1.
13. Comprueba el capítulo citado de Devroye–Györfi–Lugosi (§8.4 o Cap. 22) y suaviza la fila SURE de la Tabla 1.
14. Unifica "±0.0003"/"±0.0002" entre la nota de continuidad y la Tabla 5.
