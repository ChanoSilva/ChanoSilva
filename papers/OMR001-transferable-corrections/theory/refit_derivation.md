# OMR001 — Derivación: reversión con reajuste y con cross-fitting (punto abierto (a))

Nota de trabajo, 03/10/2026. Manuscrito de referencia: `manuscript/main.tex` v0.3 (no modificado). Entregable: `theory/refit_bound.tex`. Comprobación: `theory/check_refit.py` → `theory/check_refit_output.txt` (82 s de CPU).

Notación de main.tex: $R=\bar X_e$, $e=R-\theta\sim N(0,\sigma^2 I/n_e)$, $h=\bar Y-\theta\sim N(0,\sigma^2 I/m)$ independiente de $\mathcal F$, $\bar X_n-\theta=e_n=(1-\rho)e+\rho h$ con $\rho=m/n$. Para $C$ $\mathcal F$-medible: $w=C-R$, $\Delta=\|w\|^2+2\langle w,e\rangle$, $s=2\sigma\|w\|/\sqrt m$, $u=\Delta/s$, $z=z_{1-\alpha}$, $A=\mathbf 1\{\hat D\le -zs\}$, $\pi=\Phi(-(z+u))$, $a=\sqrt m\,\|e\|/\sigma$.

## Paso 0. Qué variante analizar

Hay tres candidatos de "reajuste":

* **(V1) la ruta sugerida en el brief:** $\hat\theta=A\,C+(1-A)\bar X_n$ (si el chequeo pasa se usa $C$; si no, la referencia con todos los datos).
* **(V2) la variante de la simulación:** $\hat\theta=A\,C(\bar X_n)+(1-A)\bar X_n$, con el operador reaplicado a $\bar X_n$ (y $\lambda_n\neq\lambda_e$ en el operador EB).
* **(V3) reajuste con corrección transportada:** $\hat\theta_{\rm rf}=\bar X_n+A\,(C-R)$: se suma a la media con todos los datos el vector de corrección propuesto en la muestra de estimación. Para una corrección aditiva $C=R+v$ coincide con V2.

V1 se descarta (Paso 6): **no** elimina el costo de la partición ni siquiera para correcciones que tienden a cero. V2 no se cubre (Paso 7). Se demuestra todo para V3, y el cross-fitting se reduce a V3 por convexidad.

## Paso 1. Reducción a un problema escalar

Por el Lema 4.1, $\hat D-\Delta=-2\langle w,h\rangle$; dado $\mathcal F$, $\langle w,h\rangle=(s/2)Z$ con $Z\sim N(0,1)$. Entonces $A=\mathbf 1\{Z\ge z+u\}$, $\mathbb E[A\mid\mathcal F]=\pi$ y, por $\mathbb E[Z\mathbf 1\{Z\ge\tau\}]=\varphi(\tau)$ (identidad de Stein para la indicadora de una semirrecta):
$$\mathbb E[A\langle w,h\rangle\mid\mathcal F]=\tfrac s2\,\varphi(z+u)\ \ (\ge 0).$$
Esta es la covarianza entre decisión y muestra retenida: el chequeo pasa justo cuando $\bar Y$ ya se movió en la dirección de $w$, y $\bar X_n$ hereda $\rho$ de ese movimiento.

## Paso 2. Identidad exacta (Teorema R(i))

$\ell(\hat\theta_{\rm rf})-\ell(\bar X_n)=A(\|w\|^2+2\langle w,e_n\rangle)$ y $\|w\|^2+2\langle w,e_n\rangle=(1-\rho)\Delta+\rho\|w\|^2+2\rho\langle w,h\rangle$. Condicionando en $\mathcal F$ (Paso 1):
$$\mathcal R(\hat\theta_{\rm rf})-\mathcal R(\bar X_n)=\mathbb E\big[((1-\rho)\Delta+\rho\|w\|^2)\pi+\rho\,s\,\varphi(z+u)\big]=\mathbb E[\Delta\pi]+\rho\,\mathbb E\big[s\varphi(z+u)-2\langle w,e\rangle\pi\big].$$
El primer término es exactamente el del Teorema 4.2(i). No aparece ningún término independiente de $C$: si $w=0$ el exceso es $0$, frente a $d\sigma^2 m/(nn_e)$ del Corolario 4.4. Comprobado réplica a réplica: $z$ pareado máx. 2.90 en 274 combinaciones del diseño, Poisson 99 % en 71 (1 fuera, el mismo patrón de eventos raros que en el manuscrito); rejilla adversarial: máx. $|z|=3.09$ en 440 puntos (uno por encima del umbral 3 prefijado; con 440 comparaciones es compatible con azar).

## Paso 3. Cota proporcional a la corrección (Teorema R(ii))

Como $\|w\|^2-\Delta=-2\langle w,e\rangle\le 2\|w\|\|e\|$: $(1-\rho)\Delta+\rho\|w\|^2\le\Delta+2\rho\|w\|\|e\|=s(u+\rho a)$ (usa $2\|w\|\|e\|=sa$). Luego
$$\mathbb E[\cdot\mid\mathcal F]\le s\,g(u),\qquad g(u)=(u+x)\Phi(-(z+u))+\rho\varphi(z+u),\ x=\rho a,$$
y $\mathcal R(\hat\theta_{\rm rf})-\mathcal R(\bar X_n)\le\mathbb E[s\,\Psi_\rho(\rho a)]$ con $\Psi_\rho(x)=\sup_u g(u)$ (convexa, no decreciente, pendiente $\le1$). Formas cerradas:
* $\Psi_\rho(x)\le\Psi_\rho(0)+x$ (trivial) $\Rightarrow$ cota $\Psi_\rho(0)\frac{2\sigma}{\sqrt m}\mathbb E\|C-R\|+2\rho\,\mathbb E[\|C-R\|\|R-\theta\|]$.
* $\Psi_\rho(x)\le\bar\kappa_\rho+x\Phi(x-z)$, $\bar\kappa_\rho=\max\{\kappa(\alpha)+\rho\varphi(z),\rho\varphi(0)\}$. Prueba por casos: $u\ge0$ ($\le\kappa+\rho\varphi(z)+x\alpha$); $-x\le u<0$ ($\le\rho\varphi(0)+x\Phi(x-z)$); $u<-x$ (primer sumando negativo, $\le\rho\varphi(0)$). Holgura numérica en rejilla: $-4\times10^{-3}$ (válida).

Comparación de constantes ($\alpha=0.1$, $\rho=0.2$): $\Psi_\rho(0)=0.0405$ frente a $\kappa=0.0188$: la pendiente frente a $\mathbb E\|C-R\|$ es ≈2 veces la del Teorema 4.2(ii), más el término en $\rho\|w\|\|e\|$. Lo que se gana es que no hay término constante.

## Paso 4. Cota uniforme en $\theta$ y $C$ (Teorema R(iii)) y su exactitud (iv)

En unidades $\|w\|=\frac{\sigma}{\sqrt m}\omega$, $\Delta=\frac{\sigma^2}{m}\delta$: el exceso condicional es $\frac{\sigma^2}{m}f(\omega,\delta)$, $f=((1-\rho)\delta+\rho\omega^2)\Phi(-(z+\tfrac{\delta}{2\omega}))+2\rho\omega\varphi(z+\tfrac\delta{2\omega})$, con la única restricción $|\delta-\omega^2|\le2a\omega$. Por tanto el exceso es $\le\frac{\sigma^2}{m}\mathbb E[M_\rho(a)]$, $M_\rho(a)=\sup f$, **y esto es exacto**: para $d\ge2$ toda pareja factible $(\omega,\delta)$ se realiza con $w=\frac{\sigma}{\sqrt m}\omega(c\hat e+\sqrt{1-c^2}\,\hat e_\perp)$, $c=(\delta-\omega^2)/(2a\omega)$, medible en $R$; con la parametrización $(\omega,c)\in[0,\infty)\times[-1,1]$ la función es continua en $(a,\omega,c)$ y decae en $\omega$, así que $M_\rho$ es continua y una elección constante a trozos en $a$ da un $C$ medible a distancia $\varepsilon$. Monte Carlo (familia "worst"): cociente exceso/cota 0.985–1.073 en los 20 pares $(m,\alpha)$.

Forma cerrada (casos $\omega\le2a$ y $\omega>2a$, este último con $u\ge\omega/2-a$, como en la prueba del Corolario 4.3):
$$M_\rho(a)\le4a\bar\kappa_\rho+4\rho a^2\Phi(\rho a-z)+4\kappa_2+4\rho(a\kappa+\lambda_1),\quad \lambda_1=\sup_{u\ge0}u\varphi(z+u)\le\varphi(1).$$
Con $\mathbb Ea=c_d\sqrt{m/n_e}$, $\mathbb Ea^2=dm/n_e$, $\mathbb E[a^2\Phi(\rho a-z)]\le\alpha\mathbb Ea^2+\rho\varphi(0)\mathbb Ea^3$ (Lipschitz) y $\mathbb Ea^3=\mu_{3,d}(m/n_e)^{3/2}$:
$$\mathcal R(\hat\theta_{\rm rf})-\mathcal R(\bar X_n)\le\frac{4\sigma^2(\bar\kappa_\rho+\rho\kappa)c_d}{\sqrt{n_em}}+4\alpha\,\frac{d\sigma^2m}{nn_e}+\frac{4\rho^2\varphi(0)\mu_{3,d}\sigma^2\sqrt m}{n_e^{3/2}}+\frac{4\sigma^2(\kappa_2+\rho\lambda_1)}{m}.$$
**El costo de la partición reaparece con coeficiente $4\alpha$, y eso es inevitable para V3:** con $C=2\theta_0-R$ (reflexión de $R$ por $\theta_0$; $\Delta=0$, $\pi=\alpha$, $\|w\|^2=4\|e\|^2$) la identidad da exactamente $4\alpha\,d\sigma^2m/(nn_e)+4\rho\varphi(z)\sigma^2c_d/\sqrt{n_em}$ (MC: cociente 0.99–1.08). Validez de la forma cerrada en rejilla: $\max_a[M_\rho-B]=-1.1\times10^{-4}$. Es holgada: entre 1.08 y 13.6 veces la cota exacta (lo peor con $\alpha$ pequeño y $\rho$ grande, porque $\bar\kappa_\rho\ge\rho\varphi(0)$).

## Paso 5. Cross-fitting (Corolario R)

$n=Km$, pliegues $I_k$, $R_k$ = media fuera de $I_k$ ($n_e=n-m$), $C_k$ $\mathcal F_k$-medible, $A_k$ el chequeo de nivel $\alpha$ sobre $I_k$. Como $\frac1K\sum_kR_k=\bar X_n$, $\hat\theta_{\rm cf}=\frac1K\sum_k[A_kC_k+(1-A_k)R_k]=\bar X_n+\frac1K\sum_kA_kw_k$. Si ningún chequeo pasa, $\hat\theta_{\rm cf}=\bar X_n$ (no hay costo de partición). Por convexidad de $\|\cdot\|^2$, $\ell(\hat\theta_{\rm cf})\le\frac1K\sum_k\ell(\bar X_n+A_kw_k)$, y cada sumando es V3 con el pliegue $k$ como muestra retenida y $\rho=1/K$. Todas las cotas del Teorema R valen promediadas sobre pliegues. Desigualdad de Jensen comprobada camino a camino (285/285).

La cota es holgada para el cross-fitting: en el diseño, exceso/cota ≤ 0.155 (II) y ≤ 0.091 (tope); con la reflexión $C_k=2\theta_0-R_k$ en todos los pliegues el promedio cancela ($\frac1K\sum_k e_k=e_n$), así que la cota inferior de 4α no se transfiere al cross-fitting. En la rejilla adversarial el peor caso del cross-fitting, en múltiplos del costo de partición, fue 0.24 ($m=3$), 0.11 ($m=6$) y 0.07 ($m=12$) con $\alpha=0.1$, pero 9.4 con $\alpha=0.5$ y $m=3$ (correcciones aditivas fijas $\|v\|=2\sigma/\sqrt m$).

## Paso 6. Por qué no V1 (la ruta del brief)

$\mathcal R(V1)-\mathcal R(\bar X_n)=\mathbb E[A\Delta]+\mathbb E[A(\|e\|^2-\|e_n\|^2)]$. El segundo término es el costo de partición ponderado por la decisión. Con un paso infinitesimal hacia $\theta_0$ ($C=R-t(R-\theta_0)$, $t\to0$): $u\to-a$, $\pi\to\Phi(a-z)$, y el cálculo exacto (con $\mathbb E[Z^2\mathbf 1\{Z\ge\tau\}]=\Phi(-\tau)+\tau\varphi(\tau)$) da un límite
$\frac{\sigma^2}{m}\mathbb E\big[\Phi(a-z)((2\rho-\rho^2)a^2-\rho^2d)+2\rho(1-\rho)a\varphi(z-a)-\rho^2(z-a)\varphi(z-a)\big]$,
que en el diseño vale 1.06 veces el costo de partición ($m=12$, $\alpha=0.1$; 1.23 con $\alpha=0.5$, 0.45 con $\alpha=0.01$; cuadratura, sin Monte Carlo). Una corrección que tiende a cero hace pagar a V1 todo el costo de la partición: el chequeo detecta la mejora de $C$ sobre $R$ (no sobre $\bar X_n$) y entonces se renuncia a $\bar X_n$. Por eso la mejora tiene que transportarse a $\bar X_n$ (V3).

## Paso 7. Qué no se cubre

* V2 (la variante "refit" de la simulación, con el operador reaplicado y $\lambda_n$): sin teorema. Empíricamente queda por debajo de las cotas de V3 (máx. 0.85 de (II) y 0.65 del tope), y en el diseño sus riesgos se reproducen exactamente desde `results.json` (diferencia 0).
* Forma $\alpha$ (análoga a $\alpha\mathbb E\Delta^+$) y la probabilidad del evento dañino para V3: no demostradas. En la región $\Delta<0<(1-\rho)\Delta+\rho\|w\|^2$ el chequeo no controla el nivel.
* Una cota para el cross-fitting que aproveche el promedio (sin Jensen): abierta; la MC muestra que Jensen pierde un factor ≥ 6 en el diseño.
* Formas cerradas finas con $\alpha$ pequeño (aquí hasta 13.6 veces la cota exacta).

## Números del diseño ($d=5$, $n=60$; costo de partición 0.0208 con $m=12$)

Peor caso sobre $(\theta,C)$ del exceso sobre $\bar X_n$, V3 (exacto) frente al estimador con partición (Corolario 4.4 + Proposición 4.5(b)):

| $\alpha$ | $m=3$ | $m=6$ | $m=12$ | $m=24$ |
|---|---|---|---|---|
| 0.5 | 0.348 vs [0.285, 0.336] | 0.223 vs [0.175, 0.200] | 0.172 vs [0.124, 0.136] | 0.199 vs [0.126, 0.132] |
| 0.1 | 0.0322 vs [0.0282, 0.0326] | 0.0241 vs [0.0239, 0.0261] | 0.0244 vs [0.0304, 0.0315] | 0.0450 vs [0.0624, 0.0630] |
| 0.01 | 0.0022 vs [0.0058, 0.0061] | 0.0020 vs [0.0102, 0.0103] | 0.0028 vs [0.0214, 0.0215] | 0.0090 vs [0.0560, 0.0560] |

Lectura: en el peor caso V3 es mejor que la partición para $\alpha\le0.1$ y $m\ge12$, comparable con $m\le6$ y $\alpha=0.1$, y **peor con $\alpha=0.5$** (coeficiente $4\alpha=2$ sobre el costo de partición). En casos típicos (barrido de estructura, EB, $\alpha=0.1$, $m=12$) el exceso de V3 sobre $\bar X_n$ es negativo en todos los snr (de −0.0056 a −0.0004), mientras que el estimador con partición va de −0.0064 a +0.0181; el cross-fitting ($K=5$) llega a −0.0245 en snr 0 (29 % del riesgo de $\bar X_n$) y en el barrido de desviación no pasa de +0.0011.


## Ruta "C si el chequeo pasa, si no $\bar X_n$" (Observación 5.3(c) del manuscrito; trasladado del Apéndice B en v0.5)

En v0.5 (ronda 3 de revisión interna, recorte de extensión §5.3 del árbitro) esta derivación salió del Apéndice B del manuscrito; el texto queda aquí sin cambios (LaTeX). El valor citado en el manuscrito (1.06 veces el costo de partición con $m=12$, $\alpha=0.1$; rango en la rejilla) lo calcula `theory/check_refit.py`, sección (c), por cuadratura.

Para $\tilde\theta=JC+(1-J)\bar X_n$:

For $\tilde\theta=JC+(1-J)\bar X_n$, $\ell(\tilde\theta)-\ell(\bar X_n)=J\big(\Delta+\norm e^2-\norm{\bar X_n-\theta}^2\big)$. Take $\theta=\theta_0$ and $C=R-t\,e$: then $|\Delta|\le(2t+t^2)\norm e^2\to0$ in $L^1$, $u\to-\xi$ and, with $Z=-\sqrt m\ip{\hat e,h}/\sigma\sim N(0,1)$ given $e$, $J\to\mathbf 1\{Z\ge z-\xi\}$ almost surely. Writing $\norm h^2=(\sigma^2/m)(Z^2+W)$ with $W\sim\chi^2_{d-1}$ independent of $Z$, using $\E[Z\mathbf 1\{Z\ge\tau\}]=\varphi(\tau)$ and $\E[Z^2\mathbf 1\{Z\ge\tau\}]=\Phi(-\tau)+\tau\varphi(\tau)$, and dominated convergence, the excess tends to
\[
\frac{\sigma^2}{m}\,\E\Big[\Phi(\xi-z)\big((2\eta-\eta^2)\xi^2-\eta^2d\big)+2\eta(1-\eta)\,\xi\,\varphi(z-\xi)-\eta^2(z-\xi)\,\varphi(z-\xi)\Big],
\]
which \path{theory/check_refit.py} evaluates by quadrature over $\xi\sim\sqrt{m/n_e}\,\chi_d$ (no Monte Carlo).

## Nota v0.5 (ronda 3 de revisión interna, 03/10/2026)

- La comparación del peor caso "comparable con $m\le6$ y $\alpha=0.1$" de la tabla de arriba quedó **resuelta**: el peor caso del estimador con partición es exactamente $d\sigma^2m/(nn_e)+(\sigma^2/m)E[M_0(\alpha;\xi)]$, $M_0(\alpha;\xi)=4\sup_{u\ge0}(u^2+\xi u)\Phi(-(z+u))$ (Prop. 4.5(c) del manuscrito, demostrada allí). Con $\alpha=0.1$: $m=3$, reajuste 0.0322 frente a partición 0.0308 (el reajuste es **peor**); $m=6$, 0.0241 frente a 0.0250 (mejor). Valores generados por `theory/check_refit.py`, sección (e).
- El supremo que define $M_\eta$ se alcanza con $c=\pm1$ (para $u$ fijo, $f_\eta$ es cuadrática convexa en $\omega$): el peor caso es colineal con $R-\theta$ y vale para todo $d\ge1$ (Teorema 5.1(iv) del manuscrito); la construcción con $\hat e_\perp$ de este documento ya no es necesaria. `check_refit.py`, sección (d), lo comprueba frente a la búsqueda 2-D.
- "Para cada corrección dada desaparece el costo de partición" (lectura de este pase teórico) es cierto de la **cota**, no del riesgo: con la corrección oráculo $C=\theta$ la partición es mejor con $\alpha\ge0.1$ y el reajuste es dañino con $m=24$ (Obs. 5.3(e) del manuscrito; sección (f) del script).
