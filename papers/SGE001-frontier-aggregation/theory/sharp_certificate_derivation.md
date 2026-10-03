[EN CURSO]

# SGE001 — Certificado fino de mejora del segundo orden (Next step (a))

Documento de trabajo del agente de teoría (3 de octubre de 2026). Se completa por pasos; mientras
aparezca la marca de arriba, el contenido no está terminado.

## 0. Convenciones (verificadas en `manuscript/main.tex`, Def. 2.2 y Prop. 3.1)

- Población $x_1,\dots,x_N\in U\subseteq\mathbb R^d_{>0}$, media $\bar x$, desviaciones $h_i=x_i-\bar x$.
- $\Sigma=\frac1N\sum_i h_ih_i^\top$, $\mu_3=\frac1N\sum_i h_i^{\otimes3}$ (tensor de tercer momento central **con signo**; es el $T_3$ del encargo), $m_3=\frac1N\sum_i\|h_i\|^3$.
- $\hat Y_1=Nf(\bar x)$, $\hat Y_2=\hat Y_1+Q_2$ con $Q_2=\frac N2\operatorname{tr}(H_f(\bar x)\Sigma)$, $\hat Y_3=\hat Y_2+\frac N6\langle D^3f(\bar x),\mu_3\rangle$.
- $E_k=Y-\hat Y_k$, de modo que $E_1=E_2+Q_2$.
- Norma de un $k$-tensor simétrico: $\|T\|=\sup_{\|h\|=1}|T[h,\dots,h]|$; la norma de Frobenius del arreglo la domina.
- Prop. 3.1(e) actual: si $(k+1)B_2<|Q_2|$ entonces $|E_1|\ge|Q_2|-B_2>kB_2\ge k|E_2|$, con
  $B_2=\frac16\sum_iM_3^{(i)}\|h_i\|^3$ (micro-data) o $B_2\le\frac N6M_3m_3$ (moment-and-range, $M_3$ sobre la caja de coordenadas de la población).
