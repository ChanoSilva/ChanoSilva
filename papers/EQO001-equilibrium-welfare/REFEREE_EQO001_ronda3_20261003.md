# Informe de arbitraje interno — EQO001 (ronda 3, 03/10/2026)

Árbitro: agente independiente (Claude Code), distinto de los de las rondas 1 y 2, sin acceso al autor. Objeto: borrador v0.3 (commit `83f2303`; `manuscript/main.tex`, 381 líneas; PDF de 13 páginas A4). Prioridad: Proposición 5.9, Ejemplo 5.8 y forma cerrada de la variante fuertemente monótona del Ejemplo 5.6. Versión anterior consultada con `git show a20cd39:…` (solo lectura). Trabajo auxiliar en `scratchpad/referee3_EQO001/` (`notes.md`, `check_hardness_r3.py`, `check_merged.py`, `check_three_r3.py` y sus salidas `.out`, compilación en `repro/`, reproducción en `run3/`). Las líneas citadas son de `manuscript/main.tex` v0.3 salvo indicación.

## 0. Veredicto

**Cambios menores.** Los tres resultados nuevos son correctos: verifiqué cada paso a mano y con chequeos propios independientes (exactos en aritmética racional donde era posible), y no encontré contraejemplos en los bordes de las hipótesis. Lo que queda es de etiquetado y precisión. La Proposición 5.9 es en sustancia la dureza clásica de certificar la optimalidad global en programación cuadrática en caja (la codificación de MAX-CUT), trasladada a un juego por la Proposición 5.3, y la nota, cuyo objeto es separar lo nuevo de lo conocido, la presenta como "proved here" sin decirlo (M1). Hay además media docena de imprecisiones en el enunciado y la prueba, y la extensión sigue en 13 páginas.

## 1. Teoremas nuevos: verificación paso a paso (prioridad máxima)

### 1.1 Proposición 5.9 (líneas 309–315)

**Problema de decisión.** Entrada: $N$, pagos cuadráticos $u_i(v)=-\tfrac12v^\top H_iv+h_i^\top v$ con coeficientes racionales y cóncavos en la acción propia (coeficiente de $v_i^2$ no positivo, comprobable), $x^*\in[0,1]^N$ y $\lambda\in\mathbb Q^N_+$. Pregunta: ¿$x^*\in\arg\max_K W_\lambda$? Está bien definido si $x^*$ es **racional**, cosa que el enunciado no dice ("given with a Nash equilibrium $x^*$"). Que $x^*$ sea de Nash se comprueba en tiempo polinómico (signo de la derivada propia), así que no hace falta plantearlo como problema con promesa. Para "$\Lambda=\Lone$" la entrada no incluye $\lambda$. La cláusula "$\lambda$ is a unit vector" del enunciado solo tiene sentido para el primer problema (m1).

**Pertenencia a co-NP (línea 313). Correcta.**
- Si $\lambda\notin\Lam(x^*)$, sea $\hat x$ un maximizador de $W_\lambda$ en la caja y $\Phi$ la cara que lo contiene en su interior relativo. Un entorno de $\hat x$ en $\operatorname{aff}\Phi$ está en $\Phi\subseteq K$, así que $\hat x$ es máximo local de la cuadrática restringida. Su hessiano restringido es entonces semidefinido negativo y la restricción es cóncava. Todo punto estacionario en $\operatorname{aff}\Phi$ alcanza el máximo sobre $\operatorname{aff}\Phi$, que es $\ge W_\lambda(\hat x)=\max_K W_\lambda$.
- El conjunto $P=\{x\in\Phi:\ (H_\lambda x-h_\lambda)_i=0,\ i\ \text{libre}\}$ es un poliedro definido por (in)ecuaciones cuyos coeficientes son entradas de $H_\lambda=\sum_i\lambda_iH_i$ y $h_\lambda$, de tamaño polinómico en la entrada. Es no vacío (contiene $\hat x$) y acotado, luego tiene vértices.
- **Por qué un vértice es un certificado de tamaño polinómico:** un vértice es la solución única de un subsistema cuadrado no singular de esas restricciones. Por Cramer y Hadamard, o por Schrijver (1986), Teorema 10.2 (complejidad de facetas $\varphi$ ⇒ complejidad de vértices $\le4n^2\varphi$), su codificación es polinómica. El verificador solo comprueba $W_\lambda(v)>W_\lambda(x^*)$ en aritmética exacta, sin necesidad de comprobar que $v$ es maximizador.
- Para $\Lam\ne\Lone$: $\Lone=\{\lambda\ge0: G(x^*)^\top\lambda\in N_K(x^*)\}$ es un cono poliédrico racional contenido en el ortante, luego puntiagudo y generado por rayos extremos de tamaño polinómico (mismo teorema). Como $\Lam\subseteq\Lone$ (Teorema 5.1(b)) y $\Lam$ es un cono convexo, $\Lam\ne\Lone$ si y solo si algún generador está fuera de $\Lam$. Con $\Lone=\{0\}$ no hay nada que certificar. Correcto.
- Chequeo empírico del tamaño del certificado: en mis 144 no-miembros exactos (§5) el maximizador hallado tiene denominador 1, es decir, es un vértice de la caja, como predice la multilinealidad.

**Dureza (línea 314). Correcta, con tres imprecisiones de redacción.**
- $\mathrm{cut}$ y $q$ son multilineales (no hay términos $x_i^2$), así que su máximo en la caja se alcanza en un vértice. En los vértices con $y=0$, $q=\mathrm{cut}(x)$. Con $y=1$, $q=\mathrm{cut}-L+k-\tfrac12\le k-\tfrac12=q(0,1)$, porque $\mathrm{cut}\le L$ en la caja si $w\ge0$. Por tanto $\max q=\max(\mathrm{maxcut},k-\tfrac12)$ y $(0,1)$ es maximizador si y solo si $\mathrm{maxcut}<k$. Si no lo es, la brecha es $\ge\tfrac12$. Lo comprobé **exactamente** (igualdad de racionales, no solo la decisión) en 214 pares (§5).
- **Convención del sumatorio:** $\sum_{ij}$ (línea 314) debe ser la suma sobre aristas no ordenadas. Si se lee sobre pares ordenados, $\mathrm{cut}$ se duplica, $\mathrm{cut}\le L$ deja de valer y la reducción falla (m2). El docstring de `hardness_maxcut.py` sí escribe $\sum_{ij\in E}$.
- **$w\ge0$ es necesario y está en el texto.** Contraejemplo de borde: con una arista de peso $-1$ y $k=1$ se tiene $\mathrm{maxcut}=0<k$, pero $\max q=\tfrac52>\tfrac12=q(0,1)$ en $(1,1,1)$.
- **Juego.** $F(v)=\varepsilon v+(\mathbf 1_n,-1,-1)$, de jacobiano $\varepsilon I$, luego $\varepsilon$-fuertemente monótono. $x^*=(0,\dots,0,1,1)$ es el único equilibrio, en estrategias estrictamente dominantes. Requiere $\varepsilon<1$: con $\varepsilon=\tfrac32$, $x^*$ deja de ser equilibrio (comprobado). $W_{e_{n+2}}=u_{n+2}$ se separa en $z$. $\nabla_xq(0,1)=\deg_w-\deg_w=0$ y $\partial_yq=k-\tfrac12>0$, así que por (5.1) se cumple $\Lone=\mathbb R^{n+2}_+$, como comprobé coordenada a coordenada. Los $e_j$, $j\le n+1$, están en $\Lam$ porque $u_j$ solo depende de $v_j$. Por convexidad, $\Lam=\Lone$ si y solo si $e_{n+2}\in\Lam$. Correcto.
- **Codificación polinómica:** los coeficientes son $w_{ij}$, $\deg_w(i)$, $k-\tfrac12$ y $\varepsilon$ racional fijo; hay $n+2$ jugadores, $x^*$ es entero y $\lambda=e_{n+2}$. Es polinómica.
- **Sentido "co-":** la reducción manda las instancias SÍ de MAX-CUT a instancias NO de pertenencia. Reduce, por tanto, el complemento de MAX-CUT (co-NP-completo) a la pertenencia, que resulta co-NP-difícil. El sentido es el correcto, pero "We reduce from MAX-CUT" no lo dice (m2).
- **"Fuertemente monótono" se preserva:** $F$ no depende ni del grafo ni de $k$. Toda la dureza vive en la externalidad $q$, que es la Prop. 5.3 en acción. El texto no lo observa y es lo más interesante de la construcción (m7).
- **Fusión a $N=2$:** $U_A=\sum_{i\le n+1}u_i$ con acción $(x,y)\in[0,1]^{n+1}$ y $U_B=u_{n+2}$. $U_A$ es separable y estrictamente cóncava, $F$ no cambia, $x^*$ sigue siendo el único equilibrio, $e_A\in\Lam$, $e_B\in\Lam$ si y solo si $\mathrm{maxcut}<k$, y $\Lone=\mathbb R^2_+$ por la condición por bloques con bloque vectorial. Lo comprobé exactamente (§5). Precisión: la clase deja de ser la del enunciado ("scalar actions"). Es la de acciones vectoriales en cajas, para la que la pertenencia a co-NP vale con la misma prueba. Así debe decirse (m1).
- Consecuencia que conviene escribir: con $N=2$, $\Lam$ es poliédrico (Remark 5.10) y aun así la pertenencia es co-NP-difícil, mientras que el Ej. 5.6 es no poliédrico con $N=3$ fijo y decidible en tiempo constante. Dureza y no poliedralidad son fenómenos independientes (m7).

**Enunciado frente a prueba.** La prueba demuestra exactamente lo enunciado, añadiendo que $x^*$ está en estrategias estrictamente dominantes y que $F$ es fijo. Falta decir que la dureza requiere que $N$ (o la dimensión de las acciones) forme parte de la entrada. Con acciones escalares y $N$ fijo el problema es polinómico ($3^N$ caras), como reconoce el Remark 5.10. El resumen ("co-NP-complete, even for strongly monotone quadratic games") y la ficha no lo precisan (m1, M1).

**Citas.** Karp (1972) prueba MAX CUT NP-completo con pesos (reducción desde PARTITION, que da pesos no negativos): respalda lo que se usa. Para Schrijver (1986) conviene precisar "Theorem 10.2" en lugar de "Ch. 10". Vavasis (1990) dice lo que se le atribuye. Murty–Kabadi (1987) prueban que decidir que un punto dado **no** es mínimo local es NP-completo. "Deciding even local optimality … is NP-hard" (línea 313) es por tanto aceptable solo bajo reducciones de Turing; en una nota tan cuidadosa con el "co-" debe decirse con precisión (m3).

**Novedad.** Véase M1.

### 1.2 Ejemplo 5.8 (líneas 296–307). Correcto en todos sus pasos

- $C_k$ a partir de la red: $C_{1,2}=\tfrac14(1-y_k)^2+y_kS$ y $C_3=2(1-y_3)+y_3S$. Correcto.
- **Equilibrio:** el potencial de Beckmann, derivado por mí, es $S^2/2+(1-y_1)^2/8+(1-y_2)^2/8+2(1-y_3)$. Minimizado con 30 arranques de L-BFGS-B da $y^*=(0,0,1)$, con costos de camino $1\le2$ y $\tfrac14\le1$. El jacobiano reducido $\operatorname{diag}(\tfrac14,\tfrac14,0)+\mathbf 1\mathbf 1^\top$ es definido positivo, porque $v^\top Jv=\tfrac14(v_1^2+v_2^2)+(\mathbf 1^\top v)^2$. Hay unicidad.
- **Gradientes** en $y^*$ por diferencias centrales: $(\tfrac12,0,0)$, $(0,\tfrac12,0)$, $(1,1,0)$. Con $N=\mathbb R_-\times\mathbb R_-\times\mathbb R_+$, $-\sum\lambda_k\nabla C_k=(-\tfrac12\lambda_1-\lambda_3,-\tfrac12\lambda_2-\lambda_3,0)\in N$ para todo $\lambda\ge0$, así que $\Lone=\mathbb R^3_+$.
- **Expansión** $\Phi_\lambda(y)-\Phi_\lambda(y^*)=P+\lambda_3+t(c-2\lambda_3)+\lambda_3t^2$: rehecha término a término, correcta.
- Rama interior ($c<2\lambda_3$, que fuerza $\lambda_3>0$): $t=1-c/(2\lambda_3)\in(0,1]$, con valor $P+c-c^2/(4\lambda_3)$. Como $c^2/(4\lambda_3)<c/2$, el valor es $\ge P+c/2\ge P+\tfrac12(\lambda_1u+\lambda_2w)=\tfrac14(\lambda_1u^2+\lambda_2w^2)+(u+w)(\lambda_1u+\lambda_2w)\ge0$.
- De ahí la caracterización exacta $\Lam=\{\lambda_3+m\ge0\}$ en las dos direcciones. Para "solo si" basta evaluar $\Phi_\lambda$ en el minimizador de $P$ con $t=0$.
- **Rebanada $\lambda_2=1$:** $P=\tfrac54\lambda_1u^2+\tfrac54w^2+(1+\lambda_1)uw-\tfrac{\lambda_1}2u-\tfrac12w$, con determinante del hessiano $\propto(4-\lambda_1)(4\lambda_1-1)$. Es estrictamente convexa en $(\tfrac14,4)\supset(\tfrac23,\tfrac32)$. El minimizador $\big(3\lambda_1-2,\ \lambda_1(3-2\lambda_1)\big)/((4-\lambda_1)(4\lambda_1-1))$ es interior exactamente en $(\tfrac23,\tfrac32)$. $m=-\tfrac14(\lambda_1u+w)=-\psi$. Todo coincide con mi derivación.
- $\psi(1)=\tfrac1{18}$; la brecha del testigo $(1,1,\tfrac1{20})$ en $(\tfrac19,\tfrac19,0)$ es exactamente $\tfrac1{180}$ (aritmética racional).
- Que $\psi$ es racional y no afín, y por tanto no poliédrica, es correcto, y $\psi>0$ en el intervalo.
- **Fuera del intervalo** (no afirmado en el texto; lo comprobé): la frontera en la rebanada es lineal, $\lambda_3=\tfrac1{20}$ para $\lambda_1\le\tfrac23$ y $\lambda_3=\lambda_1/20$ para $\lambda_1\ge\tfrac32$, y empalma con $\psi$ ($\psi(\tfrac23)=\tfrac1{20}$, $\psi(\tfrac32)=\tfrac3{40}$). Decirlo completa la figura (m13).
- **Comparación numérica independiente:** minimización 3-D por rejilla $41^3$ más L-BFGS-B, sin enumeración de caras. La frontera bisecada en 12 puntos de $[0.7,1.45]$ está a $7.1\times10^{-13}$ de $\psi$. La descripción $\{\lambda_3+m\ge0\}$ coincide con la minimización directa en 150 $\lambda$ aleatorios con los tres pesos libres (0 discrepancias).

### 1.3 Variante fuertemente monótona del Ejemplo 5.6 (líneas 277–281). Correcta

- $\Lone\cap\{\lambda_3=1\}=\{\lambda_1\ge\frac1{4(1-\varepsilon)}\}$, porque $\nabla u_3(x^*)=(-\tfrac14,0,1-\varepsilon)$.
- En la arista $x_2=0$ el máximo está en $x_1=(\lambda_1+\tfrac14)/(1+\varepsilon\lambda_1)\le1$, que equivale a $\lambda_1\le\frac3{4(1-\varepsilon)}$. Esto da $\varphi$. Con $\varepsilon=0$, $\varphi=\tfrac12(\lambda_1-\tfrac34)^2$.
- $\varphi''$: con $a=\lambda+\tfrac14$ y $b=1+\varepsilon\lambda$, $(a^2/b)''=2(b-\varepsilon a)^2/b^3$ y $b-\varepsilon a=1-\varepsilon/4$. Coincide con la fórmula impresa.
- Recíproco: si el hessiano en $(x_1,x_2)$ es semidefinido negativo, $\lambda\in\Lone$ basta. Si no, la entrada $(1,1)$ negativa obliga a que sea indefinido, sin máximo interior. Aristas:
  - $x_1=1$: derivada $\lambda_2(1-\varepsilon x_2)\ge0$;
  - $x_2=1$: derivada $\ge\lambda_1(1-\varepsilon)-\tfrac14\ge0$;
  - $x_1=0$: valor $\le(1+\lambda_2)(1-\tfrac\varepsilon2)<W_\lambda(x^*)$, que equivale a $\lambda_1(1-\tfrac\varepsilon2)>\tfrac14$, implicado por $\lambda_1\ge\frac1{4(1-\varepsilon)}$.
  
  La mejora del autor frente a la ronda 2 (sin la restricción "mientras el hessiano sea indefinido") es correcta.
- Comprobé además que $\varphi(\frac3{4(1-\varepsilon)})=0$ y $\varphi'(\frac3{4(1-\varepsilon)})=0$ (esta última porque $g'=2-\varepsilon$ donde $a=b$). Así $\varphi>0$ en todo el intervalo y la frontera es tangente al eje, como la parábola. Conviene una cláusula (m13).
- **Numérico independiente**, por rejilla y L-BFGS-B con $\varepsilon\in\{0.05,0.2,0.5,0.8\}$ y 7 puntos cada uno: $|\text{bisección}-\varphi|\le9.6\times10^{-8}$; el umbral de semidefinición nunca queda por debajo de $\varphi$ (coherencia de las dos ramas de la prueba).

### 1.4 Etiquetado en resumen, tabla de afirmaciones, README y ficha

- El Ej. 5.8 y la variante figuran como "demostrado; verificado (E7/E2c)" en `results/CLAIMS.md`, README y FICHA. Correcto.
- La Prop. 5.9 figura como "demostrado (reducción señalada en la revisión interna 2)" y la ficha la presenta entre los "principales hallazgos" sin calificar su novedad ni el papel de $N$ como parte de la entrada. Véase M1.

## 2. Verificación de la ronda 2

| Id | Estado | Evidencia |
|---|---|---|
| M1 (8.1(ii) no abierta) | **aplicado bien, con un problema nuevo de etiquetado** | Prop. 5.9 en 309–315, Remark 5.10 en 317–319, E6 en 336–338; Pregunta 8.1 retirada. Matemáticamente correcta (§1.1). Etiquetada como "proved here" sin decir que es la reducción estándar de QP en caja: M1 de este informe. |
| M2 (expectativa $m\ge3$) | **aplicado bien; el matiz del autor es correcto** | Ej. 5.8 (296–307) demostrado y verificado por mí (§1.2); E7 en 340–342; Pregunta 7.1 en 364–366. El rechazo de la reformulación del árbitro está justificado: `results_commodity.json`, `E5b_rows`, tiene 4 de 27 instancias con $b\equiv0$ y testigo. Comprobé a mano la segunda ($a=(0.0783,0.6126)$, $a_s=0.2107$, $y^*=(0,0.7441)$, $\lambda=(1,0)\in\Lone$ por un margen de $10^{-4}$, brecha $0.0212$ en $(0.271,0)$). |
| M3 (variante fuertemente monótona) | **aplicado bien** | 277–281; prueba verificada (§1.3); E2c compara con $\varphi$ (`results_welfare.json`: `max_abs_boundary_minus_phi` $=1.11\times10^{-8}$ = `\NPsmPhiDiff`). |
| M4 (extensión) | **aplicado a medias, justificado en parte** | 14 → 13 páginas (mi compilación: 13). Todos los recortes listados están hechos, y el argumento de que la ronda 2 pidió unas 2 páginas de pruebas es razonable. Quedan recortes sin pérdida de demostraciones: m8. |
| m1 (E1c) | aplicado bien | `traffic_poa.py:10–11, 193`; texto 325; la reproducción de E1 da un JSON idéntico. |
| m2 ($\gamma=\mu/L^2$) | aplicado bien | 161. |
| m3 ("never determines") | aplicado bien | Resumen 63 ("does not determine it"); argumento en 244 y 247, verificado (el término $c\ip{d}{x_{-i}-x^*_{-i}}$ no cambia $F$ y saca $e_i$). |
| m4 (Motzkin) | aplicado bien | 227 y 236; separación del cono $\{sG(x-x^*)\}$ del ortante abierto, correcta. |
| m5 (Morris–Ui) | aplicado bien | 240 y 244. |
| m6 (E5b) | aplicado bien | 333; `numbers.tex`: `CmRandLoneDimTwo`=16, `CmRandLoneFull`=9, `CmRandLoneRay`=75, `CmRandWitInterior`=8, `CmRandWitAxisOnly`=13. |
| m7 (coordenadas reducidas) | aplicado bien | 289. |
| m8 (sin enlaces compartidos) | aplicado bien | 365. |
| m9 (Dubey) | aplicado bien | 240. |
| m10 (ficha y README) | aplicado bien | Ficha condicional; README "demostrada". Quedan referencias obsoletas nuevas (m10 de este informe). |
| m11 (`table_pigou.tex`) | aplicado bien | `make_numbers.py:58`; el archivo no existe. |
| m12 (recuento de macros) | aplicado bien | `grep -c '\\newcommand' numbers.tex` = 177. |
| Bib.: `roughgarden2005` | aplicado bien | Citada en 171; `main.bbl` tiene 34 `\bibitem`. |
| Bib.: Danskin | aplicado bien | `refs.bib:238–247`. |
| Bib.: Murty–Kabadi `number={2}` | aplicado bien | `refs.bib:234`. Lo cotejé yo (vol. 39, n.º 2, pp. 117–129, según una referencia bibliográfica de SCIRP; Springer está bloqueado por el proxy). |
| Bib.: Bochnak–Coste–Roy | aplicado bien | `refs.bib:251`. |
| Bib.: Morris–Ui, Vavasis | aplicado; a Vavasis le falta `number={2}` | `refs.bib:257–272`. |
| Nota de corrección en `RESPUESTA_…ronda1` | aplicado bien (detalle) | `RESPUESTA_EQO001_ronda1_20260930.md:79`; dice "Teorema 3.8", que en la v0.3 es el 3.7. |

Recuento: **20 bien aplicados, 1 bien aplicado con un problema nuevo (M1), 2 a medias (M4, Vavasis), 0 no aplicados.**

## 3. Hallazgos nuevos

### Bloqueantes
Ninguno. Las tres demostraciones nuevas son correctas y los números de E6, E7 y E2c coinciden con los JSON.

### Mayores

**M1. La Proposición 5.9 se presenta como resultado propio cuando es, en sustancia, la dureza clásica de certificar la optimalidad global de un vértice en programación cuadrática en caja (MAX-CUT), trasladada a juegos por la Proposición 5.3.** (estado en 310; Remark 5.2 en 239–241; resumen 63; §7 en 359; `results/CLAIMS.md`; `FICHA_EQO001_propuesta.md`; README)
- *Problema.* Las piezas son conocidas: la codificación de MAX-CUT como maximización de una función multilineal en $[0,1]^n$ (cuyo máximo está en un vértice), la pertenencia a NP de la programación cuadrática (Vavasis 1990, citado) y la dureza de comprobar optimalidad incluso local (Murty–Kabadi 1987, citado; Pardalos–Schnitger 1988, no citado). Lo único específico del juego es que $F$ puede fijarse de antemano, independiente de la instancia, con $x^*$ en estrategias estrictamente dominantes. Eso es la Prop. 5.3: el operador no ve la externalidad. La nota tiene como objeto declarado separar "what is standard and what is not" (Remark 5.2), pero el Remark no menciona la Prop. 5.9. El estado dice "proved here; pointed out in the internal review", y la ficha la lista entre los "principales hallazgos" sin calificarla. Además, ni el resumen ni la ficha dicen que la dureza requiere que $N$ (o la dimensión de las acciones) forme parte de la entrada; con $N$ fijo y acciones escalares el problema es polinómico.
- *Corrección.*
  - Estado (310): `\status{proved here; in substance the standard MAX-CUT encoding of box-constrained quadratic programming, transported to games by Proposition~\ref{prop:notdet}: $F$ below does not depend on the instance; pointed out in the internal review, round 2; checked in E6}`.
  - Añadir al Remark 5.2: "Proposition~\ref{prop:hard} is likewise standard in substance: certifying global optimality of a given point of a box-constrained indefinite quadratic programme is co-NP-complete (cf.\ \citealp{murtyKabadi1987,pardalosSchnitger1988} for local optimality); the game adds only that the equilibrium operator can be fixed in advance."
  - Resumen: "deciding $\lambda\in\Lam(x^*)$ is co-NP-complete when the number of players is part of the input, even for strongly monotone quadratic games (a standard reduction)".
  - `CLAIMS.md`: "demostrado; reducción estándar MAX-CUT ↔ QP en caja, inmersa en un juego vía la Prop. 5.3".
  - Ficha (ES/EN): "Decidir si un peso dado hace óptimo al equilibrio es co-NP-completo cuando el número de jugadores forma parte de la entrada, aun con $F$ fuertemente monótono: es la dureza clásica de la programación cuadrática en caja trasladada a juegos (señalada en la revisión interna)."

### Menores

- **m1 (enunciado de la Prop. 5.9, 310).** (a) Falta "rational $x^*$". (b) "$\lambda$ is a unit vector" se aplica solo al problema de pertenencia. (c) La versión con $N=2$ (paréntesis de 314) sale de la clase del enunciado ("scalar actions"). *Texto sustituto:* "For games whose players have actions in boxes and quadratic payoffs with rational coefficients, given with a rational Nash equilibrium $x^*$ (and, for the first problem, a rational $\lambda\ge0$), deciding $\lambda\in\Lam(x^*)$ is co-NP-complete, and so is deciding $\Lam(x^*)=\Lone(x^*)$, when the number of variables is part of the input. Hardness holds with scalar actions in $[0,1]$, and also with $N=2$; and when $F$ is strongly monotone and independent of the instance, $x^*$ is a vertex in strictly dominant strategies, $\Lone(x^*)=\R^N_+$ and (for membership) $\lambda$ is a unit vector."
- **m2 (prueba de la dureza, 314).** (a) "We reduce from MAX-CUT" → "We reduce the complement of MAX-CUT, which is co-NP-complete \citep{karp1972}, to membership: YES-instances of MAX-CUT go to non-members". (b) $\sum_{ij}$ → $\sum_{\{i,j\}\in E}$ y $\deg_w(i)=\sum_{j:\{i,j\}\in E}w_{ij}$. Con pares ordenados, $\mathrm{cut}\le L$ falla y la reducción también. (c) Una frase: "$w\ge0$ is needed for $\mathrm{cut}\le L$" (con una arista de peso $-1$ y $k=1$, $(0,1)$ no es maximizador aunque $\mathrm{maxcut}=0<k$).
- **m3 (Murty–Kabadi, 313).** "deciding even local optimality in an indefinite quadratic programme is NP-hard" → "deciding that a given point is *not* a local minimiser of an indefinite quadratic programme is NP-complete \citep{murtyKabadi1987}". Citar Schrijver como "Theorem 10.2" en vez de "Ch. 10".
- **m4 (descripción de E6, 337).** "decided by exact maximisation" es inexacto para 13 410 de los 13 686 pares (98 %): para $n=5,6$ el script enumera solo los **vértices** de la caja (docstring de `hardness_maxcut.py`; `results_hardness.json`, `exact_method: vertices`). Eso presupone el paso de la prueba que se quiere comprobar (multilinealidad ⇒ máximo en un vértice) y verifica solo la identidad combinatoria. La enumeración de caras cubre 276 pares ($n\le4$) más 36 cruces. *Texto sustituto:* "…decided by exact maximisation over the faces of the box for $n\le4$ and, for $n=5,6$, over its vertices (which relies on the multilinearity used in the proof; 36 face-enumeration cross-checks)". Mi chequeo exacto de §5 cubre la parte continua para $n\le4$ y la de punto flotante para $n=5,6$.
- **m5 (Pregunta 7.1, 365).** "Membership … is in co-NP by the argument of Proposition 5.9": ese argumento está escrito para cajas ("free coordinates"). En ruteo, $K$ es un producto de símplices o, si los caminos son exponencialmente muchos, conviene trabajar en flujos de arista por mercancía, de los que $C_k$ depende y que tienen una descripción poliédrica de tamaño polinómico. *Texto sustituto:* "…is in co-NP by Vavasis' theorem applied to the commodity-wise edge flows, on which each $C_k$ depends".
- **m6 (Remark 5.10, 318).** (a) "Tractable subclasses (…; supermodular $W_\lambda$ …)": la tratabilidad del caso supermodular no se demuestra ni se cita. Escribir "candidate tractable subclasses" o dar una referencia. (b) "no polynomial-time computable description … by polynomial inequalities" → "no explicit description by polynomially many polynomial inequalities of polynomial size computable in polynomial time".
- **m7 (observación que falta tras la Prop. 5.9).** Dos frases que valen más que su espacio. "In the reduction $F$ does not depend on the graph: the hardness lives entirely in the externalities, as Proposition 5.3 predicts. With $N=2$, $\Lam(x^*)$ is polyhedral and membership is still hard, while Example 5.6 is non-polyhedral with $N=3$ fixed: hardness and non-polyhedrality are independent phenomena."
- **m8 (extensión: 13 páginas; la meta es 10).** El exceso está justificado en parte (unas 2 páginas de demostraciones pedidas por la ronda 2). Recortes concretos que no quitan ninguna demostración nueva:
  1. §6: los propios autores dicen que los experimentos "verify statements proved above; they discover nothing". Reducir E2–E7 a un párrafo con el criterio cumplido y la cifra clave por experimento y mover la Tabla 1 a `results/tables_welfare.md` (−1 p).
  2. Apéndice A, párrafo "Exact tests and random families": a tres líneas que remitan a los docstrings (−0.3 p).
  3. Ej. 5.5 (Cournot): la parte (i) ya está en el Remark 5.2 y la (ii) es un ejemplo más de "la concavidad basta, no es necesaria"; dejar tres líneas (−0.2 p).
  4. Ej. 5.7: tras el Ej. 5.8, su único papel es "$\Lam\ne\Lone$ ya con dos mercancías"; basta el umbral 40 con la arista decisiva $f_B=0$ y "the other three edges are dominated (E5)" (−0.3 p).
  5. Remark 5.10 a cuatro líneas (−0.1 p).
  
  Total ≈ −1.9 p: unas 11 páginas. Llegar a 10 exigiría remitir a la literatura las pruebas de los Teoremas 3.4 y 3.7, lo que contradice el propósito declarado de la nota; prefiero 11 páginas a eso.
- **m9 (referencias a versiones internas dentro del manuscrito).** El título del Remark 5.10 ("Question 8.1 of v0.2"), 325 ("the separate 'E1c' of v0.2"), 359 ("the claim-by-claim table of v0.2") y los estados "pointed out in the internal review, round 2" no tienen sentido para un lector externo. Antes de circular, dejar el crédito en una nota de agradecimientos y mover el historial a RESPUESTA y CONTINUIDAD. Título sugerido para 5.10: "Remark (Descriptions of $\Lam(x^*)$)".
- **m10 (archivos acompañantes obsoletos).**
  - `README.md:18`: "Teorema 3.5" → "Teorema 3.4".
  - `README.md:25`: la fila `results/results_{traffic,welfare,commodity}.json` omite `results_hardness.json`, `results_three_commodity.json` y sus `tables_*.md`.
  - `RESPUESTA_EQO001_ronda1_20260930.md:79`: "Teorema 3.8" → "Teorema 3.7".
  - `CONTINUIDAD_EQO001_20260930.md:36`: "No se cita complejidad (se evitó citar Pardalos–Vavasis…)" ya no es cierto; anotar "[superado: Prop. 5.9]".
- **m11 (bibliografía).** Añadir `number={2}` a `vavasis1990`. Si se adopta M1, añadir `pardalosSchnitger1988` (*Oper. Res. Lett.* 7(1), 33–35, 1988; cotejada, §4).
- **m12 (tipografía, 265).** "…Remark 5.2). (collusion at…": frase que empieza en minúscula tras punto. Escribir "Collusion at $(\tfrac14,\tfrac14)$ gives each firm $\tfrac18>\tfrac19$."
- **m13 (Ejemplos 5.6 y 5.8: completar la figura en una cláusula cada uno).** En la variante del 5.6: "$\varphi$ decreases to $\varphi(\frac{3}{4(1-\varepsilon)})=0$ with zero slope, so the boundary is tangent to the axis as for $\varepsilon=0$". En el 5.8: "outside $(\tfrac23,\tfrac32)$ the minimiser of $P$ lies on an edge and the boundary is linear, $\lambda_3=\tfrac1{20}$ for $\lambda_1\le\tfrac23$ and $\lambda_3=\lambda_1/20$ for $\lambda_1\ge\tfrac32$". Ambas las verifiqué numéricamente.

## 4. Bibliografía

Método: WebSearch. Springer (`link.springer.com`) está bloqueado por el proxy; no intenté Crossref ni arXiv. Entradas nuevas de la ronda anterior y las que el autor declaró no cotejadas:

| Entrada | Estado | Corrección |
|---|---|---|
| karp1972 | **verificada**: Miller y Thatcher (eds.), *Complexity of Computer Computations*, Plenum, Nueva York, 1972, pp. 85–103 (reseña en *J. Symbolic Logic*, Cambridge Core). MAX CUT, con pesos, figura en la lista y se prueba desde PARTITION. | Ninguna. |
| schrijver1986 | **verificada**: Wiley, Chichester, 1986; el cap. 10 se titula "Sizes and the theoretical complexity of linear inequalities and linear programming" (Semantic Scholar, AbeBooks, Internet Archive). | Citar "Theorem 10.2" (de memoria; cotejar el número del teorema con el libro). |
| vavasis1990 | **verificada**: *Inf. Process. Lett.* 36(2), 73–77 (Semantic Scholar; citas en otros artículos). | Añadir `number={2}`. |
| murtyKabadi1987 | **verificada**: *Math. Program.* 39(2), 117–129. Resumen: comprobar que un punto factible dado **no** es mínimo local es NP-completo. | Ajustar la frase de 313 (m3). |
| morrisUi2004, danskin1966, bochnakCosteRoy1998, roughgarden2005 | verificadas en la ronda 2; datos sin cambios | — |
| (nueva, opcional) pardalosSchnitger1988 | **verificada**: Pardalos y Schnitger, "Checking local optimality in constrained quadratic programming is NP-hard", *Oper. Res. Lett.* 7(1), 33–35, 1988 | Añadir si se adopta M1. |

Ninguna entrada queda "no verificada". Las 24 de la v0.1 y las 6 de la v0.2 fueron verificadas en rondas anteriores y no las rehice.

## 5. Verificación computacional

Todo el código es mío y no importa nada de `experiments/` (solo leí los JSON para comparar).

- **`check_hardness_r3.py`** (33 s de CPU): reducción de la Prop. 5.9.
  - *Método A, exacto (`fractions.Fraction`):* enumeración de las $3^m$ caras resolviendo la estacionariedad por eliminación gaussiana exacta; las caras con hessiano restringido singular se omiten, lo que es legítimo porque siempre hay un maximizador global en una cara de dimensión mínima, donde el hessiano restringido es no singular. Todos los grafos salvo isomorfismo con $n=2,3,4$, pesos unitarios con todos los $k$, más muestras con pesos en $\{0,\dots,5\}$: **214 pares, 0 discrepancias** entre "$(0,1)$ maximiza $q$" y "maxcut $<k$". Además **$\max q=\max(\mathrm{maxcut},k-\tfrac12)$ exactamente en 214/214**. 70 miembros, 144 no miembros, certificados con denominador 1.
  - *Juego completo con $z$* ($n=2,3$; $\varepsilon\in\{0,\tfrac9{10}\}$; 26 juegos, exacto): $x^*$ es de Nash, $\Lone$ es el ortante (condición de bloque exacta), los vectores unitarios se comportan como predice la prueba, y un $\lambda$ positivo aleatorio está en $\Lam$ cuando maxcut $<k$.
  - *Fusión $N=2$* (`check_merged.py`, exacto): $e_A\in\Lam$ siempre; $e_B\in\Lam$ si y solo si maxcut $<k$; $\Lone=\mathbb R^2_+$; los $\lambda$ positivos están en $\Lam$ cuando maxcut $<k$. Con maxcut $\ge k$, 40 de 48 $\lambda$ positivos siguen en $\Lam$ (cono poliédrico propio, como debe ser).
  - *Método B, coma flotante:* caras para los 34 grafos de 5 nodos salvo isomorfismo (unitarios y con pesos en $\{1,\dots,4\}$) y 24 grafos de 6 nodos: 417 pares, 0 discrepancias, $|\max q-\max(\mathrm{maxcut},k-\tfrac12)|=0$.
  - *Método C:* L-BFGS-B con 60 arranques, sin caras, en 20 instancias de 6 nodos: 0 discrepancias.
  - *Bordes:* con peso negativo la reducción falla (por eso $w\ge0$); con $\varepsilon=\tfrac32$, $x^*$ no es equilibrio (por eso $\varepsilon<1$).
- **`check_three_r3.py`** (396 s de CPU según `process_time`, que suma los hilos de BLAS): Ejemplo 5.8 y variante del 5.6, con los resultados de §1.2 y §1.3. Equilibrio por Beckmann multiarranque; gradientes por diferencias; frontera de 5.8 a $7.1\times10^{-13}$ de $\psi$; 150/150 coincidencias de la descripción; brecha exacta $\tfrac1{180}$; frontera lineal fuera de $(\tfrac23,\tfrac32)$; $|\text{bisección}-\varphi|\le9.6\times10^{-8}$ para cuatro valores de $\varepsilon$.
- **Reproducción** (copia en `run3/`): `three_commodity.py` 3.0 s, `traffic_poa.py` 3.5 s y `commodity_cone.py` 8.4 s de pared. Los tres JSON son **idénticos campo a campo** a los publicados (salvo `seconds`) y pasan todos sus criterios. No volví a correr `welfare_cone.py` (114 s) ni `hardness_maxcut.py` (85 s) porque mis chequeos propios ya habían agotado el presupuesto. En su lugar contrasté los macros de E6, E7 y E2c con los JSON: `HdGraphs` 1696 = 8+64+1024+300+300; `HdPairs` 13 686, `HdMember` 3598 y `HdNonmember` 10 088 suman por familias; `TcBoundaryDiff` = $1.0\times10^{-8}$; `TcDescTests` = 1878; `NPsmPhiDiff` = $1.1\times10^{-8}$. Todos coinciden.
- **`numbers.tex` v0.2 → v0.3:** solo cambian o desaparecen los macros que corresponde (E1c fusionado, porcentaje de E5b retirado, recuentos de criterios, segundos). Ningún número de la v0.2 cambió, como dice la RESPUESTA.
- **Compilación** (`latexmk` en una copia, `repro/manuscript/`, tras borrar `main.bbl`): 13 páginas, 0 *Overfull*, 0 referencias o citas indefinidas, `pdftotext | grep -c "??"` = 0, 34 `\bibitem`. Numeración coherente con README y RESPUESTA (Prop. 5.9, Remark 5.10, Pregunta 7.1), salvo los detalles de m10.
- **CPU total del árbitro:** ≈ 7.5 min, **por encima del presupuesto de 5 min**. El exceso se debe a `check_three_r3.py` (bisecciones con L-BFGS-B multiarranque y BLAS multihilo); debí usar menos arranques. Ningún resultado depende de ese exceso.

## 6. Lista de acciones (prioridad descendente)

1. Reetiqueta la Prop. 5.9 como lo que es: la dureza estándar de la QP en caja trasladada a juegos por la Prop. 5.3. Hazlo en el estado de 310, en el Remark 5.2, en el resumen (añadiendo "when the number of players is part of the input"), en `CLAIMS.md`, en la ficha (ES/EN) y en el README (M1).
2. Precisa el enunciado de la Prop. 5.9: $x^*$ racional, cajas, "$N$ parte de la entrada", alcance de "unit vector" y versión con $N=2$ (m1). En la prueba, explicita el sentido "co-", la suma sobre aristas no ordenadas y la necesidad de $w\ge0$ (m2).
3. Corrige la frase sobre Murty–Kabadi y cita Schrijver por su Teorema 10.2 (m3). Describe con exactitud qué parte de E6 es enumeración de vértices (m4).
4. Añade tras la Prop. 5.9 las dos frases de m7 (F independiente de la instancia; dureza e independencia de la poliedralidad).
5. Ajusta la Pregunta 7.1 (pertenencia a co-NP vía Vavasis en flujos de arista por mercancía, m5) y el Remark 5.10 ("candidate" tractable subclasses; descripción de tamaño polinómico, m6).
6. Recorta a unas 11 páginas con los cinco recortes de m8 (§6 a un párrafo y Tabla 1 fuera, Apéndice A, Ej. 5.5, Ej. 5.7, Remark 5.10).
7. Quita del manuscrito las referencias a versiones y rondas internas (m9).
8. Completa los Ejemplos 5.6 y 5.8 con las cláusulas de m13.
9. Actualiza README (Teorema 3.4; filas de resultados de E6 y E7), la nota de `RESPUESTA_…ronda1:79` (Teorema 3.7) y `CONTINUIDAD:36` (m10). Añade `number={2}` a Vavasis y, con M1, Pardalos–Schnitger (m11). Corrige la errata de 265 (m12).
