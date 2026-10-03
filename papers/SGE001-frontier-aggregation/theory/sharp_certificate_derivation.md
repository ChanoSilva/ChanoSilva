# SGE001 — Certificado fino de mejora del segundo orden (Next step (a))

Documento de trabajo del agente de teoría (3 de octubre de 2026).

## 0. Convenciones (verificadas en `manuscript/main.tex`, Def. 2.2 y Prop. 3.1)

- Población $x_1,\dots,x_N\in U\subseteq\mathbb R^d_{>0}$, media $\bar x$, desviaciones $h_i=x_i-\bar x$.
- $\Sigma=\frac1N\sum_i h_ih_i^\top$, $\mu_3=\frac1N\sum_i h_i^{\otimes3}$ (tensor de tercer momento central **con signo**; es el $T_3$ del encargo), $m_3=\frac1N\sum_i\|h_i\|^3$.
- $\hat Y_1=Nf(\bar x)$, $\hat Y_2=\hat Y_1+Q_2$ con $Q_2=\frac N2\operatorname{tr}(H_f(\bar x)\Sigma)$, $\hat Y_3=\hat Y_2+\frac N6\langle D^3f(\bar x),\mu_3\rangle$.
- $E_k=Y-\hat Y_k$, de modo que $E_1=E_2+Q_2$.
- Norma de un $k$-tensor simétrico: $\|T\|=\sup_{\|h\|=1}|T[h,\dots,h]|$; la norma de Frobenius del arreglo la domina.
- Prop. 3.1(e) actual: si $(k+1)B_2<|Q_2|$ entonces $|E_1|\ge|Q_2|-B_2>kB_2\ge k|E_2|$, con
  $B_2=\frac16\sum_iM_3^{(i)}\|h_i\|^3$ (micro-data) o $B_2\le\frac N6M_3m_3$ (moment-and-range, $M_3$ sobre la caja de coordenadas de la población).

Diferencia con el encargo: el encargo escribe $T_3$ para el tensor de tercer momento central; en el manuscrito ese tensor se llama $\mu_3$ y ya entra en $\hat Y_3$. Por eso el término con signo es exactamente $C_3:=\frac N6\langle D^3f(\bar x),\mu_3\rangle=\hat Y_3-\hat Y_2$, y el resto de cuarto orden es exactamente $E_3=Y-\hat Y_3$.

## 1. Enunciado y demostración

**Proposición (certificado de cuarto orden; demostrado aquí, Taylor ensamblado).** Sea $f\in C^4(U)$, $U$ abierto y convexo, $x_1,\dots,x_N\in U$. Sea $S$ una aplicación lineal invertible de $\mathbb R^d$ (en la práctica $S=I$, la norma euclídea del manuscrito, o $S=\mathrm{diag}(\bar x)$, desviaciones relativas). Para un 4-tensor simétrico $T$ sea $\|T\|_S=\|T[S\cdot,\dots,S\cdot]\|=\sup_{\|v\|=1}|T[Sv,Sv,Sv,Sv]|$; sea $M^{(i)}_{4,S}=\sup_{t\in[0,1]}\|D^4f(\bar x+th_i)\|_S$ y $m_4^S=\frac1N\sum_i\|S^{-1}h_i\|^4$.

(a) $E_2=C_3+E_3$, con $E_3=Y-\hat Y_3=\sum_i\int_0^1\frac{(1-t)^3}{6}D^4f(\bar x+th_i)[h_i^{4}]\,dt$.

(b) $|E_3|\le B_3:=\frac1{24}\sum_iM^{(i)}_{4,S}\|S^{-1}h_i\|^4\le\frac N{24}M_{4,S}\,m_4^S$ si $M_{4,S}\ge\max_iM^{(i)}_{4,S}$ (por ejemplo, el supremo de $\|D^4f\|_S$ en una región convexa conocida $R\subseteq U$ que contenga la población: la caja de coordenadas del rango). Luego $|E_2|\le|C_3|+B_3$.

(c) Certificado: $|E_1|\ge|Q_2+C_3|-B_3\ge|Q_2|-|C_3|-B_3$. Si $(k+1)(|C_3|+B_3)<|Q_2|$, o más en general $|Q_2+C_3|-B_3>k(|C_3|+B_3)$, entonces $|E_1|>k(|C_3|+B_3)\ge k|E_2|$.

(d) Datos: $\bar x$, $\Sigma$ (para $Q_2$), $\mu_3$ **completo** (para $C_3$; 4 números si $d=2$), $m_4^S$ y la región $R$ ("moment-and-range" de cuarto orden). Observación: $m_4^S=\sum_{j,l}(\mu_4^S)_{jjll}$ es una contracción del tensor de cuarto momento central (un momento polinomial), a diferencia de $m_3=\frac1N\sum\|h_i\|^3$, que es un momento absoluto. La versión por segmento ($B_3$ con $M^{(i)}_{4,S}$) necesita los $x_i$ ("micro-data", diagnóstico).

(e) Comparaciones: $|(Y^A-Y^B)-(\hat Y_3^A-\hat Y_3^B)|\le B_3^A+B_3^B$. Si $|\hat Y_2^A-\hat Y_2^B|>(|C_3^A|+B_3^A)+(|C_3^B|+B_3^B)$ (la Prop. del margen con las cotas de (b)), entonces $|\hat Y_3^A-\hat Y_3^B|>B_3^A+B_3^B$ y $\hat Y_2^A-\hat Y_2^B$, $\hat Y_3^A-\hat Y_3^B$ y $Y^A-Y^B$ tienen el mismo signo. La condición "de intervalo" $|\hat Y_3^A-\hat Y_3^B|>B_3^A+B_3^B$ es más débil (certifica más) y certifica el orden verdadero; certifica el orden de segundo orden cuando además los signos de las dos diferencias coinciden.

**Demostración, paso a paso.**

1. El segmento $\{\bar x+th_i: t\in[0,1]\}$ está en $U$ por convexidad ($\bar x\in U$ por convexidad también). Luego $\varphi_i(t)=f(\bar x+th_i)$ es $C^4$ en $[0,1]$ y, por la regla de la cadena, $\varphi_i^{(r)}(t)=D^rf(\bar x+th_i)[h_i,\dots,h_i]$.
2. Taylor con resto integral de orden 4: $\varphi_i(1)=\varphi_i(0)+\varphi_i'(0)+\frac12\varphi_i''(0)+\frac16\varphi_i'''(0)+\int_0^1\frac{(1-t)^3}{3!}\varphi_i^{(4)}(t)\,dt$.
3. Suma en $i$: $\sum_iDf(\bar x)[h_i]=Df(\bar x)[\sum_ih_i]=0$; $\frac12\sum_iD^2f(\bar x)[h_i,h_i]=\frac12\langle H_f(\bar x),\sum_ih_ih_i^\top\rangle=\frac N2\mathrm{tr}(H_f\Sigma)=Q_2$; $\frac16\sum_iD^3f(\bar x)[h_i,h_i,h_i]=\frac16\sum_{jkl}\partial_{jkl}f(\bar x)\sum_ih_{ij}h_{ik}h_{il}=\frac N6\langle D^3f(\bar x),\mu_3\rangle=C_3$.
4. Por tanto $Y=Nf(\bar x)+Q_2+C_3+\sum_i\int_0^1\frac{(1-t)^3}{6}\varphi_i^{(4)}(t)dt$ y, como $\hat Y_3=Nf(\bar x)+Q_2+C_3$, el último término es $E_3$; $E_2=Y-\hat Y_2=C_3+E_3$. Esto es (a).
5. Cota: con $v_i=S^{-1}h_i$, $D^4f(y)[h_i^4]=D^4f(y)[Sv_i,\dots,Sv_i]$, y por definición de $\|\cdot\|_S$ (homogeneidad de grado 4) $|D^4f(y)[h_i^4]|\le\|D^4f(y)\|_S\|v_i\|^4$. Con $\int_0^1\frac{(1-t)^3}{6}dt=\frac1{24}$ sale $|E_3|\le B_3$. La forma de momentos usa $M^{(i)}_{4,S}\le M_{4,S}$. **Cuidado con la región:** el supremo debe tomarse donde viven los segmentos $[\bar x,x_i]$; la caja de coordenadas $[\min_ix_i,\max_ix_i]$ es convexa y contiene a todos los $x_i$ y a $\bar x$, luego a todos los segmentos; la caja entre $\bar x$ y $x_i$ contiene el segmento $i$ (versión por segmento). Esto es (b).
6. Certificado: $E_1=E_2+Q_2=Q_2+C_3+E_3$, así que $|E_1|\ge|Q_2+C_3|-|E_3|\ge|Q_2+C_3|-B_3\ge|Q_2|-|C_3|-B_3$. Si $(k+1)(|C_3|+B_3)<|Q_2|$: $|E_1|>(k+1)(|C_3|+B_3)-(|C_3|+B_3)=k(|C_3|+B_3)\ge k|E_2|$. **Desigualdad exacta necesaria:** como en (e) del manuscrito, basta $|E_1|\ge|Q_2|-\bar B$ y $|E_2|\le\bar B$ con $\bar B=|C_3|+B_3$; la condición $(k+1)\bar B<|Q_2|$ es exactamente la de la Prop. 3.1(e) con $B_2$ sustituido por $\bar B$. La versión con signo ($|Q_2+C_3|-B_3>k\bar B$) es implicada por la anterior y no es peor; en E1 coincide con ella porque en LN $C_3$ y $Q_2$ tienen signos opuestos en el umbral (y en SU $C_3=0$).
7. Comparaciones: $Y^A-Y^B=(\hat Y_3^A-\hat Y_3^B)+E_3^A-E_3^B$ y $|E_3^A-E_3^B|\le B_3^A+B_3^B$. Como $|(\hat Y_3^A-\hat Y_3^B)-(\hat Y_2^A-\hat Y_2^B)|=|C_3^A-C_3^B|\le|C_3^A|+|C_3^B|$, la hipótesis de margen con $\bar B$ implica $|\hat Y_3^A-\hat Y_3^B|>B_3^A+B_3^B$ con el signo de $\hat Y_2^A-\hat Y_2^B$, y entonces el signo de $Y^A-Y^B$ es ése. ∎

Nota sobre la norma tensorial: $\|T\|$ es la del manuscrito (supremo en la esfera euclídea); se acota por la norma de Frobenius del arreglo, $|T[h^4]|=|\langle T,h^{\otimes4}\rangle|\le\|T\|_F\|h\|^4$. Con $S=\mathrm{diag}(s)$ el arreglo es $(s_js_ks_ls_m\,\partial_{jklm}f)$ y la misma desigualdad da $\|T\|_S\le\|(s^e\partial^ef)\|_F$.

Nota honesta: quien tiene $\mu_3$ puede calcular $\hat Y_3$, y (b) da también $|E_3|\le B_3$, una cota del error de tercer orden. El certificado se refiere a $\hat Y_2$ frente a $\hat Y_1$, que es lo que el manuscrito estudia; en LN el tercer orden empeora al segundo en la mayoría de celdas (E1), así que certificar el segundo orden sigue teniendo sentido. Ambas cotas de $E_2$ son válidas, de modo que la mejor es $\min(B_2,|C_3|+B_3)$: a dispersión grande la antigua puede ser menor (ver §4–5).

## 2. Cobb–Douglas: $D^4f$ en forma cerrada y supremo en una caja

$f(x)=A\prod_mx_m^{a_m}$, $0<a_m<1$. Como $f$ es producto de potencias de una variable, para la multiplicidad $e=(e_1,\dots,e_d)$ ($\sum e_m=k$):
$$\partial^ef(x)=A\prod_m(a_m)_{e_m}x_m^{a_m-e_m}=f(x)\frac{\kappa_e}{\prod_mx_m^{e_m}},\qquad\kappa_e=\prod_m(a_m)_{e_m},$$
con $(a)_n=a(a-1)\cdots(a-n+1)$ (factorial descendente). Coincide con la recursión del código ($C=aa^\top-\mathrm{diag}(a)$, $K_3[j,k,l]=C[j,k](a_l-\delta_{jl}-\delta_{kl})$; comprobado: diferencia relativa $3.8\times10^{-16}$), y $K_4[j,k,l,m]=K_3[j,k,l](a_m-\delta_{jm}-\delta_{km}-\delta_{lm})$.

Para $d=2$, $(\alpha,\beta)=(0.3,0.5)$ (diseño del manuscrito), los cinco coeficientes distintos de orden 4 son
$\kappa_{(4,0)}=\alpha(\alpha-1)(\alpha-2)(\alpha-3)=-0.9639$, $\kappa_{(3,1)}=\alpha(\alpha-1)(\alpha-2)\beta=0.1785$, $\kappa_{(2,2)}=\alpha(\alpha-1)\beta(\beta-1)=0.0525$, $\kappa_{(1,3)}=\alpha\beta(\beta-1)(\beta-2)=0.1125$, $\kappa_{(0,4)}=\beta(\beta-1)(\beta-2)(\beta-3)=-0.9375$ (constantes en forma cerrada; multiplicidades de índices 1, 4, 6, 4, 1).

**Monotonía por esquinas.** El exponente de $x_m$ es $a_m-e_m$: positivo si $e_m=0$ (creciente) y negativo si $e_m\ge1$ (decreciente, pues $a_m<1$); el coeficiente no depende de $x$. Por tanto en la caja $[\ell,u]$ el supremo de $|\partial^ef|$ está en la esquina $c^e_m=u_m$ si $e_m=0$ y $c^e_m=\ell_m$ si $e_m\ge1$ (mismo argumento que el manuscrito para $D^3$). Con escala $s$: $\sup_{[\ell,u]}\|D^4f\|_S\le\big(\sum_{j,k,l,m}(s^e|\partial^ef(c^e)|)^2\big)^{1/2}$.

**Verificación:** $D^4f$ en forma cerrada contra diferencias centrales de la tercera derivada analítica del experimento en 40 puntos: desviación relativa máxima $3.0\times10^{-10}$; la cota de caja coincide exactamente con `box_bounds` del experimento para $k=2,3$ y domina la norma de Frobenius en 800 puntos aleatorios de cajas aleatorias para $k=3,4$ (0 violaciones). Salida: `theory/check_sharp_certificate_output.txt`, §1.

## 3. Orden de magnitud (heurístico, primer orden, momentos poblacionales)

Coordenadas escaladas por $\bar x$ ($v=h/\bar x$), entradas log-normales $x=\bar x\odot e^{\sigma z-\sigma^2/2}$, $z$ gaussiano con correlación $\rho=0.5$. Con $v=\sigma z+\frac{\sigma^2}2(z^2-1)+O(\sigma^3)$ y momentos de Isserlis:
- $|Q_2|/N\approx\frac f2|q|\sigma^2$, $q=\sum_{jk}\kappa_{2,jk}\rho_{jk}=-0.31$;
- $E[v_jv_kv_l]=\sigma^4(\rho_{jk}\rho_{jl}+\rho_{jk}\rho_{kl}+\rho_{jl}\rho_{kl})+O(\sigma^5)$ (asimetría $\approx3\sigma$ por coordenada), luego $C_3/N\approx\frac f6c_3\sigma^4$, $c_3=1.521$;
- $B_2/N\approx\frac f6\|\kappa_3\|_F\,E\|z\|^3\sigma^3$, $B_3/N\approx\frac f{24}\|\kappa_4\|_F\,E\|z\|^4\sigma^4$ ($\|\kappa_3\|_F=0.564$, $\|\kappa_4\|_F=1.415$, $E\|z\|^3=3.944$, $E\|z\|^4=9$);
- el error verdadero: $E_2/N\approx f\sigma^4(c_3/6+e_4/24)$ con $e_4=\langle\kappa_4,\mu_4^z\rangle=-3.486$.

Cocientes (valores del script, §3 de la salida): $B_2/|Q_2|\approx2.39\,\sigma$; $(|C_3|+B_3)/|Q_2|\approx5.06\,\sigma^2$; $|E_2|/|Q_2|\approx0.70\,\sigma^2$.

**¿Cambia la escala o sólo la constante?** Cambia la escala en el límite: el cociente cota/$|Q_2|$ pasa de $O(\sigma)$ a $O(\sigma^2)$, el mismo orden que el error verdadero (la cota nueva es "de orden óptimo"; la antigua pierde un orden porque usa $m_3$ absoluto donde el error cancela). Consecuencia: el $\sigma$ certificado pasa de $\propto1/(k+1)$ a $\propto1/\sqrt{k+1}$, y la ganancia es mayor para $k=5$ (C1) que para $k=1$. Sin inflación por rango: $\sigma^*$ antiguo $0.209$ ($k=1$), $0.070$ ($k=5$); nuevo $0.314$, $0.182$; la condición con el error verdadero valdría hasta $0.85$ y $0.49$ (coherente con la mejora quíntuple observada hasta $0.42$).

**Pero** a $N$ finito los supremos se toman sobre el rango muestral, que crece como $\bar x\odot e^{\pm\sigma z_{\max}}$ con $z_{\max}\approx\sqrt{2\log N}$ ($3.76$ = mediana del máximo de $|z|$ en $2N=4000$ normales). En la esquina inferior $\|D^kf\|$ crece como $e^{(k-a_m)\sigma z_{\max}}$, más rápido para $k=4$ que para $k=3$. Esa inflación, no el orden, limita la ganancia práctica. Predicción con momentos poblacionales y la caja del rango mediano (moment-and-range, escalado), contra lo medido en E1 (grid):

| ley, k | predicho antiguo | predicho nuevo | medido antiguo | medido nuevo |
|---|---|---|---|---|
| LN, 1 | 0.082 | 0.130 | 0.075 | 0.100 |
| LN, 5 | 0.042 | 0.098 | 0.032 | 0.075 |
| SU, 1 | 0.124 | 0.204 | 0.094 | 0.164 |
| SU, 5 | 0.060 | 0.150 | 0.054 | 0.124 |

(Lo medido está limitado por la rejilla logarítmica de E1; el siguiente punto falla.) La predicción reproduce el orden y la razón nuevo/antiguo. **Conclusión honesta:** el beneficio no es sólo una constante en la teoría asintótica (cambia el exponente), pero en el diseño del manuscrito ($N=2000$, $\sigma$ hasta 1) el alcance certificado crece en un factor ≈1.8 ($k=1$) y ≈3 ($k=5$) en LN; el resto de la distancia a lo observado ($0.75$ y $0.42$) es una constante grande (desigualdad de normas $\|\kappa_4\|_FE\|z\|^4=12.7$ frente a $|e_4|=3.5$) multiplicada por la inflación del rango, que crece exponencialmente en $\sigma$.

Efecto de $N$ finito sobre $C_3$: el tercer momento muestral tiene una fluctuación $O(\sigma^3N^{-1/2})$, pero $C_3$ se calcula con signo y exactamente: no añade holgura; sólo hace que $|C_3|/|Q_2|$ no sea $O(\sigma^2)$ para $\sigma\lesssim N^{-1/2}$, donde el certificado vale con mucha holgura igualmente.

## 4. Verificación numérica en E1 (Cobb–Douglas; `check_sharp_certificate.py`, salida §2)

Reproducción: mismo generador que la corrida de referencia (`SeedSequence(20260930).spawn(12)`, hijo "E1", mismo orden de sorteos CD-LN, CD-SU, CES-LN, CES-SU), **todas** las réplicas (20) y celdas (17 LN, 15 SU), $N=2000$. El mínimo de $|E_1|/|E_2|$ por celda coincide con `results.json` (diferencia relativa 0), $B_2$ y $B_2^{\rm box}$ coinciden a $4\times10^{-16}$, y los $\sigma$ certificados antiguos (0.042/0.056/0.018/0.018 LN; 0.053/0.071/0.023/0.023 SU) se reproducen exactamente (asserts del script).

Comprobaciones (todas pasan en todas las réplicas y celdas, ambas leyes, las 8 variantes): identidad $E_2=C_3+E_3$ a $3\times10^{-15}$ relativo; $|E_3|\le B_3$; $|E_2|\le|C_3|+B_3$; y cada certificado implica la mejora que certifica ($|E_1|/|E_2|>k$ en toda réplica certificada).

Mayor $\sigma$ de la rejilla hasta el cual el certificado vale en **todas** las réplicas y en todos los $\sigma$ menores:

| variante (CD) | LN k=1 | LN k=5 | SU k=1 | SU k=5 | máx $\lvert E_2\rvert/B$ LN |
|---|---|---|---|---|---|
| antiguo, moment-and-range, euclídea (manuscrito, `\EoneCertBoxSigmaCDLN`) | 0.042 | 0.018 | 0.053 | 0.023 | 0.0061 |
| antiguo, micro-data, euclídea (manuscrito) | 0.056 | 0.018 | 0.071 | 0.023 | 0.018 |
| antiguo, moment-and-range, escalada por $\bar x$ | 0.075 | 0.032 | 0.094 | 0.054 | 0.018 |
| antiguo, micro-data, escalada | 0.133 | 0.056 | 0.164 | 0.071 | 0.046 |
| **nuevo, moment-and-range, euclídea** | **0.075** | **0.056** | **0.124** | **0.071** | 0.18 |
| **nuevo, micro-data, euclídea** | **0.100** | **0.075** | **0.164** | **0.094** | 0.19 |
| nuevo, moment-and-range, escalada | 0.100 | 0.075 | 0.164 | 0.124 | 0.56 |
| nuevo, micro-data, escalada | 0.178 | 0.133 | 0.216 | 0.164 | 0.59 |
| observado: $\min\lvert E_1\rvert/\lvert E_2\rvert>1$ / $\ge5$ | 0.75 / 0.42 | | 0.5 / 0.5 | | |

Lectura:
- En la misma norma que el manuscrito, el certificado moment-and-range pasa de 0.042 a 0.075 (LN, $k=1$; ×1.8) y de 0.018 a 0.056 (LN, $k=5$; ×3.2); en SU de 0.053 a 0.124 (×2.3) y de 0.023 a 0.071 (×3.1). Micro-data: 0.056→0.100 y 0.018→0.075 (LN); 0.071→0.164 y 0.023→0.094 (SU).
- Medir las desviaciones en coordenadas relativas ($S=\mathrm{diag}(\bar x)$) mejora **también** el certificado antiguo (0.042→0.075 LN $k=1$). Para no atribuir al cuarto orden lo que es de la norma: en coordenadas escaladas el paso de tercer a cuarto orden lleva 0.075→0.100 ($k=1$) y 0.032→0.075 ($k=5$). La ganancia propia del cuarto orden es, pues, ≈×1.3–1.8 para $k=1$ y ≈×2.4–3.2 para $k=5$ (LN).
- La versión con signo de (c) da los mismos $\sigma^*$ (columnas "signed" de la salida).
- La cota nueva es mucho más ajustada (máx. $|E_2|/(|C_3|+B_3)=0.18$ frente a $0.006$ para la antigua, moment-and-range LN), pero sigue lejos de lo observado: certificado 0.075 frente a mejora observada hasta 0.75; quíntuple certificada 0.056 frente a 0.42.
- A dispersión grande la cota nueva es **peor** que la antigua (por ejemplo LN $\sigma=0.316$: $B_3^{\rm box,s}/|Q_2|=60$ frente a $B_2^{\rm box,s}/|Q_2|=28$): la inflación del rango crece con la potencia $k-a_m$. Ambas son válidas y conviene usar el mínimo; en E1 esto no cambia los $\sigma^*$ (el nuevo domina en el umbral).

## 5. Margen (Prop. 3.12) en E4 (salida §4)

Celdas sin capacidad de E4, **los 1000 ensayos** por celda, mismos sorteos (hijo "E4"; las fracciones antiguas 70.9 % y 6.5 % se reproducen exactamente, assert). Porcentaje de comparaciones certificadas:

| $\sigma$ | antiguo micro | antiguo m&r | antiguo micro esc. | antiguo m&r esc. | nuevo micro | nuevo m&r | nuevo micro esc. | nuevo m&r esc. | intervalo m&r esc. |
|---|---|---|---|---|---|---|---|---|---|
| 0.02 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 |
| 0.05 | 99.7 | 99.6 | 99.9 | 99.9 | 100 | 100 | 100 | 100 | 100 |
| 0.1 | 97.0 | 94.4 | 99.1 | 97.9 | 99.3 | 98.0 | 99.9 | 99.6 | 99.6 |
| 0.2 | 70.9 | 6.5 | 90.0 | 56.7 | 83.0 | 11.5 | 95.7 | 71.6 | 72.5 |
| 0.4 | 0 | 0 | 3.4 | 0 | 0 | 0 | 1.2 | 0 | 0 |
| 0.8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

"nuevo": margen $|\hat Y_2^A-\hat Y_2^B|>(|C_3^A|+B_3^A)+(|C_3^B|+B_3^B)$; "intervalo": $|\hat Y_3^A-\hat Y_3^B|>B_3^A+B_3^B$ con el mismo signo que la diferencia de segundo orden (Prop. (e)). Ninguna comparación certificada es una reversión (0 en todas las variantes, como garantiza la proposición). Lectura: en $\sigma=0.2$, la versión observable (moment-and-range) pasa de 6.5 % a 11.5 % en norma euclídea y a 71.6 % en coordenadas escaladas (el tercer orden escalado da 56.7 %); en $\sigma=0.4$ nada se certifica con momentos y rango, y con micro-datos escalados el tercer orden certifica más (3.4 %) que el cuarto (1.2 %): de nuevo, usar el mínimo de las dos cotas.

## 6. CES (opcional): supremo certificado de $\|D^3f\|$ y $\|D^4f\|$ en una caja

$f=A\,S(x)^{\beta}$, $S=\sum_ja_jx_j^{\rho}$, $\beta=\nu/\rho$; aquí $\rho=-1$, $\nu=0.8$, $\beta=-0.8$. Como $S$ es separable, Faà di Bruno da para cada tupla de índices
$$\partial_{j_1\cdots j_k}f=A\sum_{\pi}(\beta)_{|\pi|}S^{\beta-|\pi|}\prod_{B\in\pi}\big[\text{índices de }B\text{ iguales a }j_B\big]\,a_{j_B}(\rho)_{|B|}\,x_{j_B}^{\rho-|B|},$$
suma sobre particiones $\pi$ de las $k$ posiciones. Implementado para cualquier $k$ y comprobado: coincide con el Hessiano y el tensor de tercer orden del experimento ($1.4\times10^{-15}$, $5.1\times10^{-14}$) y $D^4$ con diferencias centrales ($7.3\times10^{-8}$).

Encierro riguroso en una caja $[\ell,u]$: con $\rho<0$ y $\beta<0$ cada término es coeficiente × $S^{\beta-r}\prod_jx_j^{\text{exp}<0}$, factores positivos monótonos ($S$ decrece en cada $x_j$, así que $S\in[S(u),S(\ell)]$); cada término está entre sus valores en dos esquinas y la entrada entre la suma de los intervalos. Para reducir el problema de dependencia se toma el mínimo de ese intervalo ingenuo y la forma centrada $|g(c)|+\sum_m\sup|\partial_mg|\,w_m$ (valor exacto en el centro más la derivada de orden $k+1$ encerrada igual, por la semianchura), y la caja global se subdivide en 4×4. Redondeo: margen relativo $10^{-9}$ y absoluto $10^{-12}\sum|\text{términos}|$ por entrada. Comprobación: 0 violaciones en 800 puntos aleatorios. Holgura frente al máximo de la norma de Frobenius en una rejilla 41×41 de la misma caja (LN, 1.ª réplica): 1.07 ($D^3$) y 1.16 ($D^4$) en $\sigma=0.01$; 8.8 y 29.9 en $\sigma=0.1$ (SU: 1.02/1.04 y 2.2/5.8). Ajustado para cajas finas; flojo para cajas anchas (subdividir más lo mejoraría, a más coste de CPU).

Certificados CES en E1 (mismos sorteos, nuevos: el manuscrito no tenía ninguno para CES), $\sigma^*$ con $k=1$ / $k=5$:

| variante (CES) | LN | SU |
|---|---|---|
| antiguo m&r, euclídea | 0.024 / 0.013 | 0.040 / 0.023 |
| antiguo micro, euclídea | 0.032 / 0.018 | 0.040 / 0.018 |
| nuevo m&r, euclídea | 0.032 / 0.032 | 0.053 / 0.053 |
| nuevo micro, euclídea | 0.042 / 0.032 | 0.053 / 0.040 |
| nuevo m&r, escalada | 0.056 / 0.042 | 0.094 / 0.071 |
| nuevo micro, escalada | 0.075 / 0.056 | 0.094 / 0.071 |

Todas las cotas valen en todas las réplicas. Advertencia: para CES la versión micro-data no es siempre más ajustada que la de caja (SU $k=5$: 0.018 frente a 0.023), porque la caja global se subdivide y las cajas por segmento no (por coste).

## 7. Qué queda abierto

1. La distancia entre lo certificado (0.075 LN, moment-and-range, euclídea; 0.10 escalada) y lo observado (0.75; quíntuple 0.42) es ahora una constante por la inflación del rango: hace falta una región más fina que la caja de coordenadas, o controlar la cola con momentos (p. ej. separar las pocas unidades extremas y acotarlas aparte), lo que exige datos además de momentos.
2. Una versión de quinto orden ($\mu_4$ con signo y resto con $M_5$) daría $O(\sigma^3)$ en el cociente para la parte de cuarto momento, pero sufriría todavía más la inflación del rango; no se ha intentado.
3. La elección de norma importa tanto como el orden: $S=\mathrm{diag}(\bar x)$ es natural para Cobb–Douglas (deriva de la homogeneidad), pero no se ha optimizado $S$.
4. CES: el encierro es flojo para cajas anchas; subdividir más o usar aritmética de intervalos con redondeo dirigido (p. ej. `mpmath.iv`) daría una cota más ajustada y un redondeo formalmente certificado (aquí el redondeo se cubre con márgenes generosos, no con redondeo dirigido).
5. El certificado vale para la población dada; no dice nada sobre momentos estimados con error (limitación ya declarada en el manuscrito).

## 8. Reproducción y coste

`python3 theory/check_sharp_certificate.py` (no escribe nada fuera de `theory/`; no genera `.pyc` en `experiments/`). Escribe `theory/check_sharp_certificate_output.txt` y `theory/sharp_certificate_results.json` (claves listadas en la cabecera de `sharp_certificate.tex`). CPU de la corrida de referencia: 259 s (de ellos ≈200 s en los encierros CES por segmento, con derivadas de orden 5); el resto de la sesión (corridas previas del mismo script, compilación de prueba) ≈2 min. El bloque `sharp_certificate.tex` compiló en una copia de `main.tex` en el scratchpad (pdflatex + bibtex, sin errores, sin referencias ni citas indefinidas, 0 cajas sobrellenas); el PDF de prueba pasa de 11 a 12 páginas.
