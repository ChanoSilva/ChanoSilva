# Respuesta del autor al informe de árbitro interno — OMR001, ronda 1 (informe del 30/09/2026, emitido 02/10/2026; respuesta del 03/10/2026)

Documento de trabajo. Se escribe de forma incremental mientras se aplican los cambios; cada entrada indica **decisión** (aceptar / aceptar con matiz / rebatir), **qué se cambió y dónde** (archivo y lugar), o por qué no.

Estado de esta respuesta: COMPLETA (03/10/2026). Todos los cambios descritos están aplicados en la carpeta; `manuscript/main.pdf` es la compilación final.

## Resumen de decisiones

| Hallazgo | Decisión | Estado |
|---|---|---|
| B1 | aceptar | hecho (manuscrito, ficha, README) |
| B2 | aceptar | hecho (Prop. 4.5, resumen, introducción, tabla de afirmaciones) |
| M1 | aceptar (fijar τ² = σ²/48 y regenerar) | hecho (código, corrida completa, textos) |
| M2 | aceptar; además se demuestra la cota uniforme en θ sugerida | hecho (Obs. 3.2, Cor. 4.3 nuevo, leyenda de figura) |
| M3 | aceptar | hecho (Cor. 4.4, resumen, Sección 6, README, CONTINUIDAD) |
| M4 | aceptar | hecho (ficha ES/EN; criterio H del manuscrito) |
| M5 | aceptar | hecho (Apéndice A, docstring, Sección 6) |
| M6 | aceptar (recortes 1–6 + cuerpo a 10 pt) | hecho: 10 páginas |
| m1–m6, m8–m12, m14, m15 | aceptar | hecho |
| m7, m13 | aceptar con matiz | hecho (ver detalle) |
| m16 | sin acción pedida | — |

Recuento: 24 aceptados, 2 aceptados con matiz, 0 rebatidos (m16 no pedía acción). Numeración en v0.2 (cambia respecto del informe por el corolario nuevo): Teorema 3.1, Lema 4.1, Teorema 4.2, **Corolario 4.3 = cota uniforme (nuevo)**, Corolario 4.4 = precio de la partición (antes 4.3), Proposición 4.5 = sharpness (antes 4.4), Observaciones 4.6–4.7, Proposición 5.1; la simulación es la Sección 6 y las afirmaciones la Sección 7. En esta respuesta los hallazgos se citan con la numeración del informe (la de v0.1) y los cambios con la de v0.2.

## Detalle punto por punto

### Cambios de código y nueva corrida de referencia (hechos primero; afectan a M1, M2, M5, m9, m11)

- **M1 — aceptar.** `experiments/safe_reversion.py`: `simulate()` acepta ahora `tau2` explícito; `run_all()` pasa al barrido en $m$ el valor fijo $\tau^2=\mathrm{snr}_{\rm dep}\cdot\sigma^2/n_{e,0}=\sigma^2/48=0.0208$ para los cuatro $m$ (antes se recalculaba con $n_e=n-m$, de modo que $\tau^2$ y el desplazamiento $8\tau$ crecían con $m$). Se registran `tau2`, `tau2_fixed_at_m` y `snr_vs_own_ne` (1.19, 1.13, 1.00, 0.75) en cada fila. También se corrigió una inconsistencia derivada que el árbitro no señaló: `identity_recheck()` re-simulaba la configuración rara del barrido en $m$ sin pasar `tau2`; ahora reutiliza el mismo valor. Corrida completa regenerada (semilla 20260930, $R=20\,000$): 14.5 s de pared, 13.8 s de CPU. Los barridos de estructura y de desviación **no cambian** (mismo flujo aleatorio, consumido en el mismo orden); cambia la Tabla del barrido en $m$ (ahora las columnas "always" y "SURE" son planas en $m$, como predijo el árbitro: 0.048 y 0.056), los textos que la citan y el recuento de fallos del intervalo de Poisson (1 en vez de 2; re-simulación de ese caso con 50 semillas: 1882 aceptaciones frente a 1869.7 esperadas, $z=+0.29$).
- **M5 — aceptar.** Docstring del script: "U and S were fixed before the runs; the Poisson comparison … replaced a paired z-test after a first run showed that the normal approximation fails there". Misma frase en el Apéndice A del manuscrito (ver abajo).
- **M2 (parte opcional) — aceptar y demostrar.** Se añade al script la cota uniforme en $\theta$ (nuevo Corolario "uniform cap" en el manuscrito): para toda $C$ $\mathcal F$-medible y todo $\theta$,
  $\risk(\hat\theta_{\rm rev})-\risk(R)\le \tfrac{4\sigma}{\sqrt m}\varphi(z_{1-\alpha})\,\E\|R-\theta\|+\tfrac{4\varphi(1)\sigma^2}{m}$, con $\E\|R-\theta\|\le\sigma_e\sqrt d$. Demostración (en el manuscrito): $\Delta=\|C-R\|^2+2\langle C-R,R-\theta\rangle\ge a(a-2\|e\|)$ con $a=\|C-R\|$, $e=R-\theta$; si $a\le2\|e\|$ se usa la cadena de Mills del Teorema 4.2(ii), $\Delta^+\pi\le s\varphi(z)\le 4\sigma\|e\|\varphi(z)/\sqrt m$; si $a>2\|e\|$, $u=\Delta/s\ge w:=\sqrt m(a-2\|e\|)/(2\sigma)$ y $\Delta^+\pi\le s\varphi(z+w)=(4\sigma\|e\|/\sqrt m)\varphi(z+w)+(4\sigma^2/m)\,w\varphi(z+w)$, y $\sup_{x\ge0}x\varphi(x)=\varphi(1)$. Verificación numérica independiente (`experiments/check_uniform_cap.py`, incluido en la carpeta; unos segundos): la desigualdad puntual $\Delta^+\pi\le$ cota se cumple en una rejilla logarítmica de $a\in[10^{-3},10^3]$, $\|e\|\in\{0\}\cup[10^{-3},50]$, $\Delta$ en todo su rango, $m\in\{3,6,12,24,100\}$, cinco $\alpha$: cociente máximo 0.68 (una primera versión con rejilla 70 veces mayor dio 0.685). En la simulación: se cumple en las 345 combinaciones (`safe_uniform_all`), cociente máximo exceso/cota 0.38. Valor en el diseño ($m=12$, $\alpha=0.1$): 0.146, es decir 1.40 veces el riesgo de $R$; la cota $\varphi$ llega a ser 2.4 veces mayor que esta cota en la rejilla, así que el "cap" es real pero holgado.
- **Presupuesto de CPU.** Dos corridas completas (13.9 s + 13.8 s de CPU) y el chequeo de rejilla, que por un error de operación (`pkill -f` que mató el propio shell antes de reducir la rejilla) corrió dos veces con la rejilla grande (~2×(70 s usuario + 66 s sistema)). Total ≈ 5 min de CPU.

### Bloqueantes

- **B1 — aceptar.** (1) `manuscript/main.tex`: el párrafo "Why the line's conclusion is correct" (antes l.234–235) pasa a titularse "What this says about the line's conclusion" y dice que la Prop. 5.1 y el Teorema 4.2 *explican por qué no cabía esperar diferenciación del mecanismo de seguridad en sí*, que la diferenciación, si la hay, debe venir de la familia de operadores, que esta nota no explora más allá de tres instancias afines, y que la decisión de cerrar o continuar la línea (paso (d)) *no la toma esta nota*. Se eliminó la frase "established rather than merely prudent". El resumen y la introducción (lista de l.70–75 convertida en párrafo) usan la misma formulación; la fila correspondiente de la tabla de afirmaciones dice ahora "no differentiation is to be expected from the safety mechanism itself (proved here)" y añade la fila "Differentiation through the operator family — not explored beyond three affine instances". (2) `FICHA_OMR001_propuesta.md`: estado "Nota técnica (borrador v0.2, una ronda de revisión interna aplicada, sin revisión externa); línea en pausa salvo los puntos abiertos (a)–(b)" (ES y EN), con una nota al pie de la cabecera explicando el cambio. (3) `README.md` l.5: "un cierre honesto: la ficha tenía razón" sustituido por "una formalización que hace precisa la conclusión de la ficha: explica por qué no cabía esperar diferenciación del mecanismo de seguridad". El paso (d) de "Next steps" se mantiene como decisión abierta.
- **B2 — aceptar.** Prop. 4.4 (ahora 4.5): "Consequently, *for the one-sided check at any fixed level α∈(0,1/2]*, the second bound … cannot be improved beyond φ(z)/κ(α), and no choice of m makes the worst-case harm o(σE‖C−R‖/√m) uniformly over correction operators. The statement is about this class of checks: a check with a larger margin (in the limit, never using C) has smaller worst-case harm and pays for it through the regret term of Theorem 4.2(iv). The worst case within the class is a *small* correction, u*<1 in Table [constantes], not a large one." Resumen: "within one-sided checks at a fixed level, the rate m^{-1/2} cannot be improved uniformly over operators". Introducción (antes l.72): "sharpness of the constant within the class of one-sided checks at a fixed level". Tabla de afirmaciones: fila cualificada igual. La demostración no cambia (el árbitro la verificó).

### Mayores

- **M1 — aceptar.** Ver "Cambios de código". Texto: protocolo ("m∈{3,6,12,24} is also swept, with τ² held at its m=12 value (τ²=0.0208=σ²/48) so that only the split moves"); el párrafo de utilidad cita los números regenerados (m=3: +3.1 % / −17.9 %, exceso +0.0104 frente a cota 0.1146; m=24: −25.0 % / −68.8 %). La Tabla 6 sale del cuerpo por extensión (M6) y queda íntegra en `results/tables.md` T3, con el encabezado "tau^2 fixed at snr=1.0 relative to n_e=48"; las filas del JSON llevan `tau2`, `tau2_fixed_at_m` y `snr_vs_own_ne`. La conclusión cualitativa no cambia.
- **M2 — aceptar, y demostrar la cota uniforme sugerida.** (a) Observación 3.2 (antes l.131): "Section 4 gives two bounds: one of order E‖C−R‖/√m, which for the shrinkage operator grows linearly with ‖θ−μ‖ and so trades a quadratic harm for a linear one, and a cap uniform in θ (Corollary 4.3)". (b) Nuevo **Corolario 4.3 (A cap uniform in the parameter)** con demostración completa (ver arriba la derivación y las dos verificaciones numéricas); frase posterior: "Theorem 4.2(ii) is the sharper statement when E‖C−R‖ is small; the corollary takes over when it is large, where the φ-bound grows without limit although the harm does not". (c) Leyenda de la figura fusionada: "The bound of Theorem 4.2(ii) grows with E‖C−R‖, linearly in κ for the shrinkage operator, so it does not by itself give a bounded factor; what is proved for every κ is the cap of Corollary 4.3, which allows up to 3.0 times the full-data reference at α=0.1 and 4.0 at α=0.5, far above what is observed". (d) Resultados S: la cota uniforme se cumple en las 345 combinaciones (cociente máximo 0.38); al nivel de diseño el cap es 0.146 = 1.40 × riesgo de R. Tabla 1 y tabla de afirmaciones actualizadas.
- **M3 — aceptar.** Cor. 4.4 (antes 4.3): "a fraction m/n_e of the full-data risk dσ²/n (equivalently m/n of the risk of R)". Resumen: "the split costs 25 % of the full-data reference risk". Párrafo de utilidad: "the split cost of Corollary 4.4 (25.0 % of the full-data risk, 20.0 % of the risk of R)". Nueva macro `\SplitCostR` (m/n) en `make_numbers.py`; `\SplitCost` sigue siendo m/n_e con el comentario de a qué riesgo se refiere. README y CONTINUIDAD corregidos ("25 % del riesgo con todos los datos; 20 % del de R").
- **M4 — aceptar (tres puntos).** Ficha (ES y EN): "(todo demostrado; las cotas se verificaron en 345 combinaciones de la simulación y las constantes se calcularon numéricamente)"; "en una o dos dimensiones, con fuentes no informativas sobre θ, toda regla…"; "la probabilidad de usar la corrección cuando su pérdida realizada supera la de la referencia es ≤ α·P(Δ>0) ≤ α". En el manuscrito, el criterio (H) define ahora el evento en palabras ("the correction is used and its realised loss exceeds that of the reference") y el resumen dice "the probability of a harmful use of the correction is at most αP(Δ>0)".
- **M5 — aceptar.** Apéndice A, párrafo "Procedure": "Criteria U and S were fixed before the runs. The Poisson comparison used for the identity check where acceptance is rare replaced a paired z-test after a first run showed that the normal approximation fails there (huge |z| for counts of a few units); nothing else was changed after seeing results." Misma declaración en el docstring del script y una remisión en el párrafo de criterios de la Sección 6. Los umbrales |z|≤3 y Poisson 99 % no estaban prefijados por escrito; se dice así en la nota de continuidad (no se afirma lo contrario en el manuscrito).
- **M6 — aceptar; ver "Extensión" al final.**

### Menores

- **m1 — aceptar.** Teorema 3.1: "D may include auxiliary randomisation, so randomised rules are covered, and an estimator with infinite risk satisfies (a) and (c) trivially". En la prueba de (c), "parallelogram identity" sustituido por "Since δ̃ is the conditional expectation of δ given X and δ̃−θ is X-measurable, … (Pythagoras; we may assume the left side finite)".
- **m2 — aceptar.** Teorema 3.1(b): "with E‖b(D)‖²<∞"; prueba: "the cross term is finite by Cauchy–Schwarz and vanishes because…".
- **m3 — aceptar.** Protocolo: "refit, which applies the same check but then builds the final estimate from all n observations, *so that the independence hypothesis of Theorem 4.2 fails*".
- **m4 — aceptar.** Prop. 5.1: "(ties, a null event, resolved toward C as in Definition 2.1(c))"; la Def. 2.1(c) y el script (`Dhat <= -z s`) no cambian.
- **m5 — aceptar.** Observación 4.5: "with a beneficial v that cancels the error of R exactly (R−θ=−v, so Δ=−‖v‖²) this ratio is ‖v‖√m/(2σ) whatever the dimension".
- **m6 — aceptar.** Observación 3.2: "with (μ,τ²) fixed, the law of the source data still does not depend on the realised θ, so part (a) applies to the frequentist risk even in the hierarchical model; the sources are informative about the task distribution, which is what the Bayes risk over tasks rewards".
- **m7 — aceptar con matiz.** Se mantiene la constante cerrada z+φ(0) y se añade al final de la prueba de (iv): "On {Δ<0} the exact conditional value is s·sup_u uΦ(z−u), smaller than s(z+φ(0)); we keep the closed form". No se tabula el supremo (sería una constante más sin uso en el texto).
- **m8 — aceptar.** Tabla 1, fila SURE: "no finite-sample selection bound used here".
- **m9 — aceptar.** `make_numbers.py` marca con U mayúscula los casos que cumplen U con margen y con u minúscula los "borderline" (extremo inferior del IC a menos de 2 puntos del umbral del 5 %); la leyenda de la Tabla 2 lo explica y el texto los enumera: α=0.1 en snr=0 (7.6 %, inf. 6.9 %), refit 0.1 en snr=1 (6.1 %, inf. 5.8 %), α=0.5 en snr=2 (7.1 %, inf. 6.5 %), SURE en snr=8 (6.9 %, inf. 6.6 %), con la frase "'refit useful up to snr=1' should not be read as robust". En la Tabla 4 (desviación) se marcan con H los casos dañinos respecto de X̄_n (extremo superior del IC de la ganancia por debajo de cero), que son los que el texto enumera. No se añade una columna de extremos inferiores a las tablas de riesgos (doblaría su anchura); los IC completos están en el JSON.
- **m10 — aceptar.** Resultados S: "Where Δ>0 almost surely, the comparison with E[Δ⁺π] is a check of identity (i) between two Monte Carlo estimates of the same quantity, not of a bound."
- **m11 — aceptar.** CONTINUIDAD unificada a "+0.0042 ± 0.0002" (EE 0.00025; la tabla usa cuatro decimales). Nueva macro `\DEightRevTenExcessSE`.
- **m12 — aceptar.** Apéndice A: "on [0,20], an interval that contains the maximiser (u*<1, Table [constantes])".
- **m13 — aceptar con matiz.** Búsqueda web en esta sesión: el índice en línea confirma la sección 8.4 "Selecting classifiers" dentro del capítulo 8 "Error Estimation" y un capítulo titulado "Splitting the Data" (p. 387); el número de ese capítulo (22) procede de memoria y es coherente con el orden del índice. Se cita "\S 8.4; see also Ch.~22". Queda anotado en la nota de continuidad como "sección verificada; número del capítulo 22 no verificado en línea".
- **m14 — aceptar.** Resumen reescrito (≈200 palabras según el texto del PDF; sin constantes numéricas salvo el 25 % del coste de partición).
- **m15 — aceptar.** Tabla 1 con columnas `>{\raggedright\arraybackslash}p{}` (tipo `L`) y sin la fila "Hold-out selection" (es la construcción misma, Prop. 5.1; la leyenda lo dice). Las tres cajas desbordadas desaparecieron (la de la Def. 2.1 al pasar a 10 pt; la de la Tabla 5 porque la tabla salió del cuerpo; la del Apéndice porque se reescribió). Última compilación: 0 "Overfull".
- **m16 — sin acción (el árbitro no pide ninguna).** Se agradece la verificación del código.

### Bibliografía

- Se aplican las correcciones verificadas (ninguna entrada necesitaba cambio de datos). `devroye1996`: sección citada corregida (m13). Entradas "no verificables en línea" según el árbitro (`lehmanncasella1998`, `lehmannromano2005`, `virtanen2020`, `harris2020`): se mantienen (datos estándar) y quedan marcadas como tales en la nota de continuidad.

### Acciones de la lista final del árbitro

| # | Acción | Estado |
|---|---|---|
| 1 | Estado de la ficha | hecho (B1) |
| 2 | l.235 y README l.5 | hecho (B1) |
| 3 | Cualificar Prop. 4.4, resumen, l.72 | hecho (B2) |
| 4 | τ² fijo en `run_all()`, regenerar | hecho (M1) |
| 5 | Cor. 4.3, l.61, l.365 | hecho (M3) |
| 6 | l.131 y leyenda Fig. 2; cota uniforme | hecho, incluida la demostración (M2) |
| 7 | Ficha: tres precisiones | hecho (M4) |
| 8 | Apéndice A: Poisson/z y criterios prefijados | hecho (M5) |
| 9 | Teorema 3.1: aleatorización, riesgo finito, E‖b‖²<∞ | hecho (m1, m2) |
| 10 | Empate, Obs. 4.5, Obs. 3.2 | hecho (m4, m5, m6) |
| 11 | IC inferior / borderline; identidad vs cota | hecho (m9, m10) |
| 12 | Recortes 1–6; cajas desbordadas; Tabla 1 | hecho; ver "Extensión" |
| 13 | Devroye–Györfi–Lugosi; fila SURE | hecho (m13, m8) |
| 14 | ±0.0003/±0.0002 | hecho (m11) |

### Extensión (M6, acción 12)

Recortes del árbitro aplicados: (1) las tablas de verificación 3, 5 y 7 salen del cuerpo y quedan íntegras en `results/tables.md` (T1, T2, T4), con remisión explícita en el texto; la Tabla 8 (constantes) pasa al apéndice; además, la Tabla 6 (barrido en m) sale también al Markdown (T3) y sus números clave siguen en el texto como macros. (2) Figuras 1 y 2 fusionadas en una de 1×2 con solo los estimadores con garantía (`figures/sweeps.pdf`); los paneles (b) duplicaban las columnas "refit"/"SURE" de las tablas. (3) La tabla de afirmaciones no se suprime (el brief común la exige) pero se comprime a 12 filas en `footnotesize`, con filas nuevas para la cota uniforme y para "diferenciación por la familia de operadores: no explorada". (4) Párrafos de l.214 y l.234–235 fusionados en uno más un párrafo breve de conclusión; "Draws"/"Statistics" del apéndice trasladados al README (queda un párrafo "Procedure" con lo exigido por M5 y m12). (5) Resumen a ≈200 palabras; lista de la Introducción convertida en un párrafo de cinco líneas. (6) Tabla 1 con `\raggedright` y sin la fila "Hold-out selection".

Resultado: con 11 pt y todos los recortes, 12 páginas (medido en una copia; el Corolario 4.3 nuevo y las cualificaciones de B1/B2/M2 añaden ≈0.6 pp.). Para cumplir el objetivo de ≤10 páginas sin perder demostraciones ni números verificables se pasó el cuerpo a 10 pt (precedente en HQF001 y TCD001 del mismo repositorio): **10 páginas**, 0 errores, 0 referencias o citas indefinidas, `pdftotext main.pdf - | grep -c "??"` = 0, 0 cajas desbordadas. Compilado con `manuscript/build.sh` (regenera `numbers.tex` y las tablas con `make_numbers.py` y corre `latexmk`).

### Estado final y lo que queda abierto

- Páginas: 14 (v0.1, 11 pt) → 10 (v0.2, 10 pt; 12 a 11 pt).
- Números que cambiaron: solo el barrido en m (τ² fijo) y los recuentos de verificación que dependen de él (fallos Poisson 2→1; |z|max 2.96→2.83; máx. exceso/cota φ 0.42→0.40; re-simulación del caso raro 2488/2426, z=+1.27 → 1882/1869.7, z=+0.29). Estructura y desviación: idénticos a v0.1. Nuevos: cota uniforme (0.146 en el diseño, α=0.1; cociente máximo exceso/cota 0.38), coste de partición respecto de R (20 %), marcas borderline (4).
- Abierto (también en la nota de continuidad): (a) cota en muestra finita para el reajuste / cross-fitting; (b) cota de selección para la reversión por SURE; (c) definiciones originales de los operadores; (d) decisión de cierre de la línea, que el manuscrito no toma; (e) constante de la cota uniforme holgada; (f) número de capítulo 22 de Devroye–Györfi–Lugosi y cuatro entradas bibliográficas sin verificación externa; (g) umbrales de las comprobaciones de identidad/seguridad no prefijados por escrito (declarado).
- Cómputo de la ronda: ≈6 min de CPU en total (dos corridas completas de ≈14 s, una `--fast` de 5 s, el chequeo de rejilla de la cota uniforme ≈2 min corrido dos veces por error de operación, y ≈1 min de compilaciones LaTeX).
