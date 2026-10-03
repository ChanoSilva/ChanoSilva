# Informe de árbitro interno independiente — SGE001, ronda 3 (03/10/2026)

Versión arbitrada: manuscrito v0.4 (commit c45dddf, 12 páginas). Árbitro nuevo, independiente de las rondas 1 y 2 y del agente teórico. Prioridad: Prop. 3.3 (certificado de cuarto orden), Lema 3.4 (derivadas de Cobb–Douglas) y Obs. 3.5, que ningún árbitro había leído.

**Veredicto: cambios menores.** La Prop. 3.3 y el Lema 3.4 son correctos tal como están enunciados y probados (revisión paso a paso y chequeo numérico propio sin código del autor: todos los σ certificados y las fracciones de E4 se reproducen exactamente); quedan un hueco de enunciado (el certificado de tercer orden en la norma escalada se usa pero no está enunciado), una extensión de 12 páginas frente al objetivo de 10, y ajustes de redacción y de documentos auxiliares.

Recuento: 0 bloqueantes, 2 mayores (M1 hueco de enunciado de la norma escalada; M2 extensión), 10 menores.

---

## 1. Verificación de los resultados nuevos (prioridad máxima)

### 1.1 Proposición 3.3 (main.tex:126–134; prueba en el Apéndice A, main.tex:370–372)

| paso | comprobación | estado |
|---|---|---|
| (a) resto de Taylor de orden 4 | $\varphi_i(t)=f(\bar x+th_i)$ es $C^4$ en $[0,1]$ si $f\in C^4(U)$ y el segmento está en $U$ ($U$ convexo); $\varphi(1)=\sum_{r\le3}\varphi^{(r)}(0)/r!+\int_0^1\frac{(1-t)^3}{3!}\varphi^{(4)}$ es la forma integral estándar. Al sumar: $r=1$ se anula ($\sum h_i=0$), $r=2$ da $Q_2$, $r=3$ da $\frac16\langle D^3f(\bar x),\sum_ih_i^{\otimes3}\rangle=\frac N6\langle D^3f(\bar x),\mu_3\rangle=C_3$, y $\hat Y_3=Nf(\bar x)+Q_2+C_3$ por la Def. 2.2. | correcto |
| (b) norma escalada | $\|T\|_S:=\|T[S\cdot,\dots,S\cdot]\|$; con $v=S^{-1}h$, $|T[h^4]|=|T[(Sv)^4]|\le\|T\|_S\|v\|^4$ por homogeneidad de grado 4 en la definición de $\|\cdot\|$ (main.tex:66). $\int_0^1(1-t)^3/6=1/24$. $S$ puede depender de la población ($S=\operatorname{diag}(\bar x)$): la desigualdad es puntual, no hay problema. | correcto |
| (b) región | Una región convexa $R$ que contiene a la población contiene a $\bar x$ (combinación convexa) y a cada segmento $[\bar x,x_i]$; la caja de coordenadas del rango es convexa y, con insumos positivos, está en $U=\R^2_{>0}$ (SU: $1-0.5\sqrt3=0.134>0$). La caja entre $\bar x$ y $x_i$ contiene el segmento $i$. | correcto |
| (b) mínimo | $|E_2|\le B_2$ (Prop. 3.1(c), sólo requiere $C^3$) y $|E_2|\le|C_3|+|E_3|\le|C_3|+B_3$. | correcto, **pero** véase M1: el $B_2$ citado es el euclídeo; el texto usa también un $B_2$ escalado que no está enunciado |
| (c) certificado | $E_1=Q_2+C_3+E_3$ ⇒ $|E_1|\ge|Q_2+C_3|-B_3\ge|Q_2|-|C_3|-B_3$; si $(k+1)(|C_3|+B_3)<|Q_2|$, el último término es $>k(|C_3|+B_3)\ge k|E_2|$. La forma con signo: $|Q_2+C_3|-B_3>k(|C_3|+B_3)$ ⇒ $|E_1|>k(|C_3|+B_3)\ge k|E_2|$. | correcto |
| (d) comparaciones | $(Y^A-Y^B)-(\hat Y_3^A-\hat Y_3^B)=E_3^A-E_3^B$. Si $|\hat Y_2^A-\hat Y_2^B|>\sum(|C_3|+B_3)$, entonces $|C_3^A-C_3^B|<|\Delta\hat Y_2|$ fija el signo de $\Delta\hat Y_3$ y da $|\Delta\hat Y_3|>B_3^A+B_3^B$, que fija el de $\Delta Y$. | correcto |

Observaciones sin error: (i) la condición (c) no aprovecha el mínimo de (b); el certificado combinado $\max(|Q_2|-B_2,\ |Q_2+C_3|-B_3)>k\min(B_2,|C_3|+B_3)$ también es válido; en la rejilla de E1 certifica exactamente los mismos σ que la forma enunciada (comprobado, 8 variantes × k ∈ {1,5} × 2 leyes), de modo que no hace falta añadirlo. (ii) La afirmación "unlike $m_3$, $m_4^S=\sum_{j,l}(\mu_4^S)_{jjll}$ is a polynomial moment" (main.tex:136) es correcta ($\frac1N\sum_i(\sum_jv_{ij}^2)^2=\sum_{j,l}\frac1N\sum_iv_{ij}^2v_{il}^2$), pero $\mu_4^S$ no está definido (m9).

### 1.2 Lema 3.4 (main.tex:138–140; prueba main.tex:373–374)

- $\partial^ef=A\prod_m(a_m)_{e_m}x_m^{a_m-e_m}$: correcto (contrastado con sympy en 50 puntos aleatorios, $k=1..4$: desviación relativa máxima $4.6\times10^{-16}$).
- Regla de esquinas. Con $0<a_m<1$: si $e_m=0$ el exponente es $a_m>0$ (creciente, esquina $u_m$); si $e_m\ge1$ es $a_m-e_m<0$ (decreciente, esquina $\ell_m$). **$a_m-e_m=0$ y $(a_m)_{e_m}=0$ son imposibles bajo la hipótesis** (un factorial descendente $(a)_n$ con $n\ge1$ se anula sólo si $a\in\{0,\dots,n-1\}$). Búsqueda de contraejemplos (verify_A.py, A3): 9600 pruebas (caja, multiíndice), $d\in\{2,3\}$, $a_m\in[10^{-4},0.9999]$, esquinas inferiores hasta $10^{-8}$, cajas de hasta 4 décadas: **0 violaciones**. Fuera de la hipótesis: con $a_1=1$ no hay violaciones (exponente 0: constante; o factorial nulo: entrada idénticamente 0); con $a_1\in\{1.5,2,2.5,3\}$ la regla tal como está escrita falla en 400–700 de 1400 pruebas (con $e_1=1$ y $a_1>1$ el exponente es positivo y el máximo está en $u_1$). La hipótesis $a_m<1$ es, pues, necesaria para la regla enunciada; la regla "por el signo del exponente" del Apéndice B (main.tex:378) es la general (m2).
- Cota de norma: $|D^kf(y)[Sv,\dots,Sv]|=|\langle(s^e\partial^ef(y)),v^{\otimes k}\rangle|\le\|(s^e\partial^ef(y))\|_F\|v\|^k$ (Cauchy–Schwarz) y cada entrada se acota por su valor en su esquina. Correcto. Comprobación (A4): en 60 cajas aleatorias con $S=I$ y $S$ diagonal aleatoria, $\sup_y\sup_{\|v\|=1}|D^4f(y)[(Sv)^4]|$ (7×7 puntos $y$ × 3600 direcciones) dividido por la cota está en $[0.708,\ 0.99999999927]$: nunca la supera, y es casi exacta cuando una entrada domina.
- Detalle: $\|\cdot\|_S$ se define en la Prop. 3.3 sólo para formas 4-lineales; el lema la usa para todo $k$ (parte de M1).

### 1.3 Observación 3.5 (main.tex:142–144)

Recalculé las constantes por mi cuenta (Isserlis y fórmula exacta de los momentos log-normales): $|q|=|\kappa_{20}+2\kappa_{11}\rho+\kappa_{02}|=0.31$; $\|\kappa_3\|_F=0.5639$; $\|\kappa_4\|_F=1.4151$; $E\|z\|^4=9$; $E\|z\|^3=3.938$ (cuadratura exacta; el agente usó 3.944 por Monte Carlo); $c_3=1.521$; $e_4=-3.486$. Resultan $B_2/|Q_2|\approx2.39\sigma$, $(|C_3|+B_3)/|Q_2|\approx5.06\sigma^2$, $|E_2|/|Q_2|\approx0.70\sigma^2$: coinciden con `\SharpAold`, `\SharpAnew`, `\SharpAtrue`. La observación se declara heurística en el texto ("These orders are heuristic; the certificate is exact") y en la tabla de afirmaciones ("orders heuristic"): bien etiquetada. Dos precisiones (m9): las constantes son las de las cotas de Frobenius del Lema 3.4, no las de la norma de operador de las Props. 3.1 y 3.3; y "at leading order (population moments)" omite el término muestral $O(\sigma/\sqrt N)$ de $|C_3|/|Q_2|$ que la Obs. 3.2 sí discute (irrelevante en la frontera certificada: $\sigma/\sqrt N=0.002$ frente a $5\sigma^2=0.05$ en σ = 0.1, N = 2000).

### 1.4 Cifras nuevas: recomputación independiente

Código propio (scratchpad `referee3_SGE001/verify_{A,B,C,D}.py`): derivadas con sympy y regla de esquinas implementada por mí; los sorteos se regeneran desde `SeedSequence(20260930).spawn(12)` (hijo 1 = E1, hijo 6 = E4) con la ley documentada en el Apéndice B; ninguna función del autor ni del agente teórico se importa.

- **Resto integral frente a $Y-\hat Y_3$** (A1; Gauss–Legendre de 24 nodos, poblaciones propias de N = 200, CD y CES, LN y SU, σ ∈ {0.02, 0.1, 0.3, 0.6}): diferencia relativa ≤ $7\times10^{-11}$ para σ ≥ 0.1 y ≤ $2\times10^{-8}$ en σ = 0.02 (cancelación en doble precisión). La identidad (a) se verifica como identidad analítica, no sólo algebraica (el integrador señaló con razón que el chequeo del agente era algebraico).
- **E1, Cobb–Douglas, las 20 réplicas y las 17 + 15 celdas**: $|E_3|\le B_3$, $|E_2|\le|C_3|+B_3$ y $|E_2|\le B_2$ en las 8 variantes (euclídea/escalada × caja/segmento × orden 3/4) y ambas leyes. **Los 40 σ certificados del texto coinciden exactamente** con los míos: LN 0.075/0.100/0.056/0.075 (euclídea), 0.100/0.075/0.178/0.133 (escalada), tercer orden escalado 0.075/0.032/0.133/0.056, tercer orden euclídeo 0.042/0.056/0.018/0.018; SU 0.124/0.164/0.071/0.094, 0.164/0.124/0.216/0.164, 0.094/0.053/0.164/0.071, 0.053/0.071/0.023/0.023; observados 0.75 y 0.42. $\max|E_2|/(|C_3|+B_3)$ (caja euclídea) = 0.1752 (LN) y 0.054 (SU); $\max|E_3|/B_3$ = 0.0556 / 0.054. La forma con signo certifica los mismos σ (`\SharpSignedSame` = yes, correcto).
- **E4, sin capacidad, 1000 pares por celda**: fracciones certificadas con la Prop. 3.3(d): σ = 0.1: 99.3 / 98.0 / 99.9 / 99.6 % (tercer orden escalado 99.1 / 97.9); σ = 0.2: **83.0 / 11.5 / 95.7 / 71.6 %** (tercer orden escalado 90.0 / 56.7; euclídeo 70.9 / 6.5); σ = 0.4: escalada por segmento 1.2 % frente a 3.4 %. Todas idénticas a las macros; 0 inversiones entre comparaciones certificadas en todas las variantes. Con $\min(B_2^S,|C_3|+B_3^S)$ (segmento, escalada): 95.7 % en σ = 0.2 y **4.2 %** en σ = 0.4 (cifra que el texto recomienda usar pero no da; m4).
- **¿Cuándo es menor $B_2$?** (verify_D): mediana de $B_2/(|C_3|+B_3)$ en E1-LN, caja euclídea: 37.8 en σ = 0.01, 2.8 en 0.1, 1.15 en 0.178, **0.65 en 0.237**, 0.001 en σ = 1; caja escalada: cruza 1 en σ ≈ 0.24; segmento escalado: en σ ≈ 0.42. SU: cruza en σ ≈ 0.29 (caja euclídea). El mínimo de (b) es, por tanto, relevante y la Obs. 3.5 lo dice; el README no (m5).
- **CES (no riguroso, sólo coherencia)**: con el supremo por rejilla 33×33 de cada entrada sobre la caja (estimación inferior de cualquier encierro válido), el certificado $k=1$, LN, momentos y rango llega a σ = 0.042 (tercer orden) y 0.100 (cuarto orden), y a 0.100 en la norma escalada; el texto da 0.024, 0.032 y 0.056 (`\SharpCES*`). Coherente (un encierro válido no puede certificar más que la rejilla) y coherente con los factores de holgura del JSON de teoría (1.07–1.16 en σ = 0.01, 8.8 y **29.9** en σ = 0.1, todos ≥ 1). Consecuencia: el certificado CES de cuarto orden está limitado por la holgura del encierro, no por el orden (m6).

### 1.5 Etiquetado y sobreafirmación

- Tabla de afirmaciones (main.tex:344–345): Prop. 3.3 + Lema 3.4 "[proved here; not yet checked by an independent referee]; orders heuristic; figures verified numerically"; CES "computational; rounding not directed". Correcto para v0.4; tras esta ronda puede pasar a "proved here; checked by an independent referee (round 3)" (m10).
- Limitaciones (main.tex:364): "with rounding covered by generous margins, not directed rounding: not a computer-assisted proof". Correcto y suficiente.
- Brecha certificado/observado: declarada en el resumen (0.075 frente a 0.75 y 0.42), en E1 (main.tex:256) y en §5 (main.tex:362). Correcto.
- README:5 y :35, FICHA:11, :13, :22, :24: "demostrado aquí; aún no revisado por un árbitro independiente". Coherente. FICHA:13/24 presenta como hecho la causa heurística ("porque ahora lo limita el crecimiento de las derivadas") (m5).

---

## 2. Verificación de la ronda anterior (respuesta a la ronda 2 frente a los archivos de v0.4)

| id (ronda 2) | estado | evidencia |
|---|---|---|
| M1 certificados micro-data / moment-and-range; forma graduada; C1 con $k=5$ | aplicado bien | main.tex:115 (Prop. 3.1(e), "(Certificates; under the hypothesis of (c).)", $(k+1)B_2<|Q_2|$, dos certificados nombrados); :254 (0.042/0.053, 0.056/0.071, 0.018/0.023, 0.75, 0.42; recomputados por mí); :309 (E4 70.9 / 6.5 %); :343; :378 |
| M2 C1 y C2 separados | aplicado bien | main.tex:53 ("Two criteria were fixed in advance…"), :311, :354; FICHA:13, :24 |
| M3 E1c 60 réplicas con s.e. | aplicado bien | main.tex:228 (`\EonecReps`, cuatro N, s.e.); :53 ("moves towards 4 as N grows") |
| M4 artefacto de mediana de la razón desplazada | aplicado bien | main.tex:266, :271 (última columna = mediana de |·−1|), :282 ([0.997, 1.003], 50 %) |
| m1 "jerárquica" | aplicado bien | main.tex:62; :53; FICHA:14, :25 |
| m2 huecos impresos con su valor | aplicado bien | make_numbers.py:16; numbers.tex:143 (2×10⁻¹⁵), :196 (2×10⁻¹⁶) |
| m3 definición de $B_1$ | aplicado bien | main.tex:109 |
| m4 (e) bajo la hipótesis de (c) | aplicado bien | main.tex:115 |
| m5 "at least like" | aplicado bien | main.tex:53, :123, :362 |
| m6 s.e. de los exponentes de E2 | aplicado bien | main.tex:282 (`\EtwoSlopeCappedSeLN`, `\EtwoSlopeTransitionSe`) |
| m7 lectura de E5 | aplicado bien | main.tex:332 |
| m8 atribución "σ_W only" | aplicado bien | main.tex:288, :160 |
| m9 E1b | aplicado bien (con matiz aceptable) | main.tex:364; results.json `se_median_abs_normal_R` = 0.176; tables.md:108 |
| m10 "as it guarantees" | aplicado bien | main.tex:53, :309 |
| m11 números tecleados | aplicado bien | main.tex:364 (`\EoneLooseMin/Max`), :62, :378 |
| m12 tiempos | aplicado bien | main.tex:378 (`\MetaSeconds…\MetaCpuSecondsTotal`) |
| m13 bootstrap por experimento | aplicado bien | frontier_aggregation.py:1079 |
| Extensión (≤ 10 pp.) | **no aplicado (empeora)** | v0.3: 11 páginas; v0.4: 12 (pdfinfo de ambas versiones); véase M2 |
| Bibliografía | aplicado bien | refs.bib:8, :149 (DOI de jensen1906 y farrell1957); CONTINUIDAD, sección "Bibliografía: estado" |

Recuento: 18 aplicados bien (M1–M4, m1–m13, bibliografía), 0 a medias, 1 no aplicado (extensión, por contenido nuevo), 0 con error nuevo. `results/results.json` no cambió entre v0.3 y v0.4 (`git diff --stat ebbb788 c45dddf`), de modo que la reproducción bit a bit de la ronda 2 sigue valiendo para E0–E6.

---

## 3. Hallazgos nuevos

### Bloqueantes
Ninguno.

### Mayores

**M1. El certificado de tercer orden en la norma escalada se usa y se reporta como certificado, pero no está enunciado.**
- Ubicación: main.tex:256 ("with deviations measured relative to the mean ($S=\operatorname{diag}(\bar x)$) the *third*-order moment-and-range certificate (LN) already reaches 0.075 ($k=1$) and 0.032 ($k=5$) … micro data: from 0.133 and 0.056"); main.tex:309 ("third order: 90.0 %, 56.7 %"; "so the smaller bound should be used"); README (viñeta del certificado); macros `\OldCert*Sc*`, `\OldEfour*Sc*`.
- Problema: la Prop. 3.1(c)/(e) está enunciada sólo con la norma euclídea ($B_2=\frac16\sum_iM_3^{(i)}\|h_i\|^3$), y $\|\cdot\|_S$ se define en la Prop. 3.3 sólo "for a symmetric 4-linear form". El código del agente calcula `B2box_s` $=\frac N6\sup_R\|D^3f\|_S\,\frac1N\sum\|S^{-1}h_i\|^3$ y `B2seg_s` (check_sharp_certificate.py:260–261) y el texto los presenta como certificados; el "$\min(B_2,\cdot)$" de la Prop. 3.3(b), en la forma en que se usa en E4, también requiere ese $B_2^S$. El resultado es cierto (misma prueba con homogeneidad de grado 3; lo he comprobado numéricamente: las cotas escaladas valen en todas las réplicas), pero un certificado vale lo que el enunciado que lo respalda, y aquí falta el enunciado. El Lema 3.4, además, usa $\|D^kf\|_S$ para todo $k$.
- Corrección (texto sustituto): en main.tex:127, sustituir "write $\|T\|_S=\|T[S\,\cdot,\dots,S\,\cdot]\|$ for a symmetric $4$-linear form $T$" por "write $\|T\|_S=\|T[S\,\cdot,\dots,S\,\cdot]\|$ for a symmetric $k$-linear form $T$ (so $\|T\|_I=\|T\|$)", y añadir al final de (b): "The same argument with $k=3$ gives $|E_2|\le B_2^S:=\frac16\sum_iM_{3,S}^{(i)}\|S^{-1}h_i\|^3\le\frac N6M_{3,S}m_3^S$, $m_3^S=\frac1N\sum_i\|S^{-1}h_i\|^3$; $B_2=B_2^I$ is the bound of Proposition 3.1(c), and in the minimum $B_2$ may be replaced by $B_2^S$." En la prueba (main.tex:371, (b)) añadir "and likewise with $k=3$ and $\int_0^1\frac{(1-t)^2}{2}=\frac16$". En E1 (main.tex:256) decir "the third-order certificate with $B_2^S$ (Proposition 3.3(b))".

**M2. Extensión: 12 páginas (v0.3: 11) frente al objetivo de ≤ 10 aceptado en la ronda 2; buena parte del exceso es redundancia, no contenido.**
- Evidencia: pdfinfo de la compilación en copia = 12 páginas; la página 12 está llena (Apéndice B continúa y la bibliografía entera); el resumen tiene ≈ 450 palabras (main.tex:53). La idea "lo que limita ahora es el crecimiento de $\|D^4f\|$ en el rango" aparece tres veces (Obs. 3.5, main.tex:143; Limitaciones, :364; Next steps (a), :366); la regla de esquinas aparece dos veces (Lema 3.4 y Apéndice B, :378); el párrafo de cierre de §5 (:362) repite el resumen.
- Recortes concretos (estimación ≈ 1.3–1.6 páginas, suficiente para volver a 10 u 11):
  1. Resumen a ≤ 250 palabras: quitar las cifras de E1c ("3.16 at N = 200, 3.96 at N = 200000"), los factores de la jerarquía, la constante del cruce y el paréntesis "(fivefold improvement: …)"; dejar una frase por resultado (≈ −0.25 p.).
  2. Apéndice B: sustituir las frases "Bounds: for a Cobb–Douglas frontier … bounds $\|D^kf\|$ on the box" por "Bounds use Lemma 3.4"; mover a README la lista de versiones/tiempos/hashes salvo el hash del script y la semilla (≈ −0.3 p.).
  3. Suprimir el párrafo de cierre de §5 ("Table 5 separates … supplies it", main.tex:362), redundante con el resumen y la tabla (≈ −0.15 p.).
  4. Obs. 3.5: conservar las dos primeras frases y la última; la de inflación por el rango queda sólo en Limitaciones; en Next steps (a) basta "Done in part (v0.4, Proposition 3.3)" más la lista de abiertos (≈ −0.15 p.).
  5. E1, párrafo "Fourth-order certificate" (main.tex:256): dar en el texto sólo la forma de momentos y rango (euclídea y escalada, $k=1,5$) y mover las cifras de microdatos a `tables.md`; o sustituir todo por una tabla 4×4 (orden × norma × $k$) de 6 líneas (≈ −0.15 p.).
  6. E4 (main.tex:309): dejar σ = 0.2 con caja y segmento escalados y la cifra del mínimo en σ = 0.4 (m4); el resto a `tables.md` (≈ −0.1 p.).
  7. Obs. 3.10(iii) (uniformidad en N) al Apéndice A o a Limitaciones (≈ −0.1 p.).
- Si tras esto queda en 11 páginas con la bibliografía en la última, el exceso es defendible (un teorema nuevo con prueba); 12 no lo es.

### Menores

**m1. "Closed forms" de los supremos.** main.tex:123 ("For Cobb–Douglas frontiers the suprema $M_k^{(i)}$ have closed forms (Lemma 3.4)") y :364 ("The derivative suprema have closed forms for Cobb–Douglas"). El Lema 3.4 da una **cota** en forma cerrada (Frobenius de los supremos por entrada), no el supremo de la norma de operador (el cociente supremo/cota baja hasta 0.71 en mis pruebas). Sustituir por "have closed-form upper bounds (Lemma 3.4)".

**m2. Regla de esquinas: enunciarla por el signo del exponente.** main.tex:139. Tal como está, la regla requiere $a_m<1$ (con $a_1=1.5$ falla en 400 de 1400 pruebas); el Apéndice B (:378) ya usa la regla general "corner given by the sign of each exponent", que vale para todo $a_m>0$. Texto sustituto: "$|\partial^ef|$ is largest at the corner $c^e$ with $c^e_m=u_m$ if $a_m-e_m>0$ and $c^e_m=\ell_m$ if $a_m-e_m<0$ (either if $a_m=e_m$); when $0<a_m<1$ this is $u_m$ for $e_m=0$ and $\ell_m$ otherwise." Añadir "$(a)_0=1$". Así el lema cubre rendimientos crecientes en un insumo sin cambiar nada más.

**m3. Paso de la rejilla SU.** main.tex:256: "adjacent ones differ by a factor $10^{1/8}$" es exacto para LN (`logspace(-2,0,17)`), no para SU (`logspace(-2,log10 0.5,15)`: factor $50^{1/14}\approx1.32$). Escribir "a factor $10^{1/8}$ (LN) and $50^{1/14}$ (SU), about 1.33".

**m4. E4: "the smaller bound should be used" sin la cifra; el certificado (c) no usa el mínimo.** main.tex:309. Reportar la fracción con $B=\min(B_2^S,|C_3|+B_3^S)$ (mi cálculo, segmento escalado: 95.7 % en σ = 0.2 y 4.2 % en σ = 0.4, frente a 1.2 % y 3.4 % de cada cota por separado), como macro generada; el integrador lo dejó abierto (CONTINUIDAD, "Lo que queda abierto tras la integración", punto 4). Requiere M1. Opcional: una frase tras la Prop. 3.3(c) diciendo que con $\max(|Q_2|-B_2,|Q_2+C_3|-B_3)>k\min(B_2,|C_3|+B_3)$ también se certifica (en E1 no cambia ningún σ).

**m5. README y FICHA: "mucho más ajustada" y causa heurística presentada como hecho.** README, viñeta "Certificado de cuarto orden": "La cota $|E_2|\le|C_3|+B_3$ … es mucho más ajustada". Sólo a dispersión pequeña o moderada: en mediana $B_2<|C_3|+B_3$ desde σ ≈ 0.24 (LN, caja euclídea o escalada) y σ ≈ 0.42 (segmento escalado); en σ = 1 es 1000 veces mayor. Añadir "para σ ≲ 0.2 (LN); a dispersión grande la cota de tercer orden es menor, y se usa el mínimo". FICHA:13 y :24 ("porque ahora lo limita el crecimiento de las derivadas en el rango de los insumos"): añadir "según una heurística (Obs. 3.5)".

**m6. CES: decir que el límite es el encierro.** main.tex:364. Con una estimación por rejilla (no rigurosa), el certificado CES de cuarto orden ($k=1$, LN, momentos y rango) llegaría a σ ≈ 0.10, como Cobb–Douglas, frente a 0.032 con el encierro (holgura 29.9 en σ = 0.1). Añadir: "the CES certified range is limited by the looseness of the enclosure (a grid estimate, not rigorous, would give $\sigma\approx0.1$), not by Proposition 3.3", y precisar "thin boxes ($\sigma=0.01$)" / "wide ones ($\sigma=0.1$)".

**m7. CONTINUIDAD con numeración y estado de v0.3 bajo un encabezado "v0.4"; colisión "Lema 3.4".** CONTINUIDAD_SGE001_20260930.md:1 dice "actualizada 03/10/2026, v0.4", pero: l. 12 ("Prop. 3.5 y la Obs. 3.7(i)", ahora Prop. 3.8 y Obs. 3.10(i)); ll. 25–32 ("Lema 3.3", "Lema 3.4 (… identidad de bisagra)", "Prop. 3.5", "Cor. 3.6", "Obs. 3.7", "Ej. 3.8", "Prop. 3.9", "Ej. 3.10", "Obs. 3.11"), mientras ll. 150–162 usan "Lema 3.4" para el lema de Cobb–Douglas; l. 20 ("11 páginas en v0.3", "356 macros"); l. 48 ("Para CES no se certifica ninguna cota", contradicho por v0.4); l. 55 (región certificada sólo hasta 0.042). El aviso "Las referencias a números en las secciones anteriores de esta nota son a v0.3" está en la l. 151, después de esas secciones. Corrección: actualizar a la numeración de v0.4 las secciones de estado actual (Supuestos, Qué se produjo, Resultados matemáticos, Decisiones, Limitaciones) y dejar con v0.3 sólo los registros de ronda, con el aviso al principio. En `RESPUESTA_SGE001_ronda{1,2}` y `REFEREE_SGE001_ronda{1,2}` basta una línea inicial "Numeración de enunciados: v0.x". README:38 ("Lema 3.6(ii) de v0.4") es correcto; las referencias internas del manuscrito son todas `\ref` y compilan sin indefinidas.

**m8. "Section 3.3" y "Proposition 3.3" a la vez.** El contador de enunciados es por sección y la subsección "Threshold crossings" es la 3.3 (main.aux: `sec:threshold -> 3.3`, `prop:sharp -> 3.3`); "Section 3.3" (main.tex:160) y "Proposition 3.3" conviven. Cosmético; opciones: `\newtheorem{theorem}{Theorem}[subsection]`, o no numerar las subsecciones de §3 (`\subsection*`), o citar la subsección por nombre.

**m9. Precisión de notación en la Obs. 3.5 y tras la Prop. 3.3.** (i) main.tex:143: añadir "(with the Frobenius bounds of Lemma 3.4)" tras "at leading order", porque 2.39 y 5.06 dependen de $\|\kappa_3\|_F$, $\|\kappa_4\|_F$; y "(the sampling part of $C_3$, of relative order $\sigma/\sqrt N$, is negligible at the certified dispersions)". (ii) main.tex:136: definir $\mu_4^S=\frac1N\sum_i(S^{-1}h_i)^{\otimes4}$ o escribir directamente $m_4^S=\frac1N\sum_i\|S^{-1}h_i\|^4$, que ya está definido.

**m10. Etiquetas de estado tras esta ronda.** main.tex:344 y :358, README:5 y :35, FICHA:11, :13, :22, :24: sustituir "not yet checked by an independent referee" por "checked by an independent internal referee (round 3)" una vez aplicados M1 y m2; mantener "orders heuristic" y, para CES, "computational; rounding not directed".

---

## 4. Lectura fresca (resto del manuscrito)

Sin errores matemáticos nuevos fuera de §3.1. Comprobé de nuevo el Lema 3.7 (bisagra), la identidad (1) de la Prop. 3.8, el Cor. 3.9 (constantes $M_2/2$ y la cota final) y el Ej. 3.11 (momentos 0, σ², 0; agregados $4c-2\sigma$ y $4c-\sqrt2\sigma$): correctos. Las cifras del cuerpo que no cambiaron proceden de `results/results.json`, idéntico al de v0.3. La notación $B_2$/$B_3$ para la forma por segmento y su versión de momentos (con "≤") es coherente entre las Props. 3.1 y 3.3.

## 5. Bibliografía

v0.4 no añade entradas ni citas (`refs.bib` no cambió entre ebbb788 y c45dddf; la prueba nueva remite a la Prop. 3.1, que cita a Dieudonné). Las 18 entradas citadas fueron verificadas en las rondas 1 (8) y 2 (10); no quedan entradas marcadas como no verificadas. No hice búsquedas web porque no hay nada nuevo que cotejar.

| entrada | estado | corrección |
|---|---|---|
| (ninguna nueva) | — | — |

## 6. Verificación computacional

| qué | cómo | CPU | resultado |
|---|---|---|---|
| Resto integral de orden 4, Lema 3.4, regla de esquinas, cota de norma | verify_A.py (sympy; 24 nodos de Gauss–Legendre; 9600 + 7000 pruebas de esquinas; 60 cajas × 3600 direcciones) | ≈ 5 s | véase §1.2 y §1.4: sin violaciones con la hipótesis; contraejemplos fuera de ella (a ≥ 1.5) |
| E1 completo (CD, 20 réplicas, 32 celdas, 8 variantes) + CES por rejilla | verify_B.py | ≈ 3 s | 40 σ certificados y los máximos 0.18 / 0.054 / 0.056 coinciden; CES coherente |
| E4 sin capacidad (1000 pares, σ ≤ 0.4) | verify_C.py | ≈ 6 s | todas las fracciones coinciden; 0 inversiones certificadas; mínimo: 4.2 % en σ = 0.4 |
| Comparación $B_2$ frente a $|C_3|+B_3$ | verify_D | ≈ 3 s | cruce en σ ≈ 0.24 (LN) |
| `make_numbers.py` en una copia | regenera 425 macros y 4 cuerpos de tabla | < 1 s | `numbers.tex` y `table_e{1,2,4,5}.tex` idénticos byte a byte; al alterar un byte del JSON de teoría se detiene (SHA-256 c7bbd… frente al congelado a75d9e…) |
| Hashes congelados | `sha256sum` | — | JSON a75d9e3f… y script 8b636617… coinciden con `results/sharp_certificate.sha256` |
| Compilación | latexmk en una copia | ≈ 3 s | 12 páginas; 0 errores, 0 referencias/citas indefinidas, 0 "Overfull", 0 "??" |
| Experimento principal | no relanzado: `results.json` no cambió desde v0.3 (reproducido bit a bit en la ronda 2) | — | — |
| `theory/check_sharp_certificate.py` | no ejecutado (259 s de CPU, fuera de presupuesto); sustituido por la recomputación independiente de la parte Cobb–Douglas | — | — |

CPU total ≈ 25 s.

## 7. Lista de acciones (por prioridad)

1. Enunciar el certificado de tercer orden en la norma escalada: definir $\|\cdot\|_S$ para formas $k$-lineales y añadir $B_2^S$ a la Prop. 3.3(b) y a su prueba (M1).
2. Recortar a ≤ 11 páginas (idealmente 10) con los recortes 1–7 de M2, empezando por el resumen (≤ 250 palabras), el Apéndice B y el párrafo de cierre de §5.
3. Reportar la fracción certificada de E4 con el mínimo de las dos cotas (95.7 % / 4.2 %) como macro, y opcionalmente el certificado combinado (m4).
4. Enunciar la regla de esquinas por el signo del exponente y definir $(a)_0=1$ (m2); cambiar "closed forms" por "closed-form upper bounds" (m1).
5. Añadir a Limitaciones que el certificado CES está limitado por el encierro (m6) y corregir el paso de la rejilla SU (m3).
6. Precisar la Obs. 3.5 (constantes de Frobenius, término muestral) y definir o eliminar $\mu_4^S$ (m9).
7. Calificar "mucho más ajustada" en el README y la causa heurística en la FICHA (m5).
8. Actualizar la numeración y el estado de las secciones vigentes de CONTINUIDAD y añadir la nota de numeración a las respuestas e informes anteriores (m7); resolver la ambigüedad "Section 3.3"/"Proposition 3.3" (m8).
9. Tras aplicar 1 y 4, cambiar las etiquetas de estado de la Prop. 3.3 y el Lema 3.4 a "checked by an independent internal referee (round 3)" en el manuscrito, el README y la FICHA (m10).
