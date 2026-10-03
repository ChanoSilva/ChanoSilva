# Informe de árbitro interno independiente — EQO001, ronda 4 (03/10/2026)

Objeto: `manuscript/main.tex` v0.4 (commit 3f3e6ca), en especial la parte "Routing" de la §5 (Lema 5.11, Teorema 5.12, Observación 5.13, Corolario 5.14, Proposición 5.15), el Apéndice B, el párrafo E8 y la Pregunta 7.1; además, `RESPUESTA_EQO001_ronda3_20261003.md`. Soy un árbitro nuevo, independiente de las rondas 1–3 y del integrador. El trabajo auxiliar está en el scratchpad `referee4_EQO001/` (`verify_routing.py`, `verify_dag.py`, `edge_cases.py` y sus salidas `out_*.txt`). Los números de línea remiten a `manuscript/main.tex` v0.4.

## 0. Veredicto

**Cambios menores.** Verifiqué a mano cada paso del Teorema 5.12, de la Observación 5.13 y del Corolario 5.14, y los comprobé con un código propio: son correctos, y la reparación $D+2\le2(D+1)$ también. Quedan dos defectos de enunciado o de etiquetado. El primero: el Corolario 5.14 dice que "Theorem 5.12 holds", y con ello hereda dos propiedades que en el DAG son falsas. El segundo: la Pregunta 7.1, el README y la ficha llaman polinómico al caso de pocas mercancías sin limitarlo a rutas explícitas. Hay además unos diez menores. No hay bloqueantes.

Recuento: 0 bloqueantes, 2 mayores, 12 menores.

## 1. Teoremas nuevos: verificación paso a paso (prioridad máxima)

### 1.1 Lema 5.11 (329–334). Correcto

En (eq:phiroute), $g_e$ sólo depende de $f^Q$, y $f_e$ es lineal en todas las rutas, así que para $f^Q$ fijo $\Phi_\lambda$ es afín en $f^R$. El ínfimo de afines es cóncavo, y su mínimo sobre el producto de símplices de $R$ se alcanza en un vértice, es decir, en un perfil puro. Con $\lambda=\mu\mathbf 1_Q$ la expresión $\mu\sum_e\big(a_e(f^Q_e)^2+(a_er_e+b_e)f^Q_e\big)$ es convexa. Una precisión que no afecta a nada: tampoco intervienen las mercancías de $R$ que sólo comparten con $Q$ aristas con $a_e=0$.

### 1.2 Teorema 5.12 y su prueba (338–343, 422–454). Correcto en todos los pasos

- **Identidad (eq:CW), línea 439.** La rehíce arista por arista:
  - $dz$ aporta $a_D(D+1-z)D$; $o$, $b_o(D-\sum t)$; $p_m$, $(b_o-\alpha_m)t_m$.
  - $e^1_m$ aporta $\alpha_m(t_m+x_i)t_m$; $e^2_m$, $\alpha_m(t_m+1-x_j)t_m$; $e^z_m$, $2\alpha_m(t_m+z)t_m$.
  - La suma es $a_DD(D+1-z)+b_oD+\sum_m\alpha_m(4t_m^2+t_m(x_i-x_j+2z))$.
- **Minimización en $t$.** $4t^2+ct$ tiene su mínimo en $t=(-c)_+/8$ y vale $-(c_-)^2/16$. Con $\alpha_m=16w_m$ eso da $-w_m((x_j-x_i-2z)_+)^2$. Además $t_m\le\frac18$ y $\sum t_m\le M/8\le D=M$, de modo que la restricción de demanda queda holgada.
- **$h$ y sus vértices.** $h$ es cóncava, porque es el mínimo en $t$ de funciones afines en $(x,z)$.
  - Con $z=1$: $x_j-x_i-2<0$ y $h=C^\star$.
  - Con $z=0$ y $x$ binario: el par $(i,j)$ aporta $-w_m$ sii $x_i=0$ y $x_j=1$, y cada arista cortada lo hace por exactamente una de sus dos orientaciones. Como $a_DD=k-\frac12$, queda $h=C^\star+k-\frac12-\mathrm{cut}_w(x)$.
  - Por tanto $e_W\in\Lam$ sii $\mathrm{maxcut}<k$. El umbral es exacto: con $k=\mathrm{maxcut}$, el margen es $-\frac12$.
- **Unicidad.**
  - Dominancia de los nodos: $f_{e^2_m}\le D+1$ (aristas de $W$ y del nodo $j$), luego $c_{P_i}\le1+(D+1)\sum\alpha<B\le c_{S_i}$.
  - Dominancia del interruptor: $f_{e^z_m}\le D+1$, luego $c_{Z_1}\le1+2(D+1)\sum\alpha<B\le c_{Z_0}$.
  - Con $x=0$ y $z=1$: $c_{T_m}-c_O=4\alpha_mt_m+2\alpha_m>0$. Correcto.
- **Monotonía fuerte.** $DF=\Delta^\top\mathrm{diag}(a)\Delta$. Sea $h$ tangente con $\sum a_e(\Delta h)_e^2=0$. Entonces $h$ se anula en $s_i,r_i,q_0,q_1$; $e^1_m$ fuerza $h_{T_m}=0$; y la suma cero da $h_O=0$. Para esto hace falta $w_m\ge1$: con un peso $0$, $\alpha_m=0$ y $h_{T_m}$ queda libre (véase §5, casos borde). El enunciado exige $w_{ij}\ge1$ (línea 425), así que está bien.
- **$\Lone$ y vectores unitarios.**
  - Derivadas de $C_W$ en $f^*$: $2a_DD+b_o$ en $O$; $+2\alpha_m$ en $T_m$; $0$ en $S_i$, $P_i$ y $Z_1$; $a_DD$ en $Z_0$. Coinciden con la línea 453.
  - Nodos: $C_i\ge\sigma_i(1-x_i)^2+Bx_i$, con $B\ge2\sigma_i$.
  - Interruptor: $C_z\ge\sigma_zz^2+B(1-z)$, con exceso $(1-z)(B-\sigma_z(1+z))\ge0$, y $B\ge2\sigma_z$ porque $D\ge1$. Correcto.
- **Pertenencia a co-NP.**
  - El certificado de la Prop. 5.9 es correcto. Un máximo local de una cuadrática en el interior relativo de una cara implica concavidad en la envolvente afín de la cara. Entonces todo punto estacionario de la cara es maximizador, y un vértice del politopo de estacionarios tiene tamaño polinómico.
  - Para $\Lam\ne\Lone$ el certificado es un generador extremo de $\Lone$, que es puntiagudo por estar contenido en el ortante, junto con un punto que lo mejora. Comprobar $\lambda\in\Lone$ es lineal. Correcto.
- **Tamaños.** $B$, $a_D$ y el $\varepsilon$ de la Obs. 5.13 son de tamaño polinómico.

### 1.3 Observación 5.13 (345–347). Correcta

Testigo: corte pesado, $z=0$, $t_m\in\{0,\frac18\}$. Las cotas de costo de ruta son:

- $c_{S_i}\le1+B+\frac98\sum\alpha\le2B$;
- $c_{P_i}\le1+\frac98\sum\alpha$;
- $c_{Z_1}=\sum_m2\alpha_mt_m$;
- $c_{Z_0}=1+B+a_D(D+1)\le1+B+2k$.

Todas son $\le\Gamma$. Como las demandas valen 1, $C_h(y)\le\Gamma$, y además $C_h(f^*)\ge0$. Por tanto $\Delta\Phi\le-\frac12+\varepsilon(n+1)\Gamma=-\frac14$. Lo verifiqué en aritmética exacta en 107/107 no miembros (§5).

### 1.4 Corolario 5.14 (349–351, 456–466). Prueba correcta; enunciado impreciso (M1)

- **Aciclicidad.** Correcta. En el nivel 0 sólo hay $q_0\to dz\to\{o,p_m\}$. Cada arco $e^1_m$ (respectivamente $e^2_m$) está en una única cadena, la de la cola (respectivamente de la cabeza). Los conectores suben de nivel o avanzan dentro de la cadena. Lo comprobé además por ordenación topológica en 14/14 instancias.
- **(i) Nodos.** Correcto. Desde la cabeza de $e^1_m$, con $m=(i,j)$, se sale a $e^2_m$, que está en la cadena de $P_j$ con $j\ne i$. Desde el nivel 2 no se vuelve a ninguna cadena de nivel $\le2$ de otro nodo, y $\mathsf d_i$ sólo se alcanza desde el último arco de $S_i$ o de $P_i$.
- **(ii) Rutas de $W$.** Correcto: toda ruta de $W$ distinta de $O$ y de los $T_m$ contiene un conector de cadena.
- **(iii) Rutas del interruptor.** Correcto en lo que se usa: contienen $q_0$ y $dz$. La redacción "then follows arcs of W" es inexacta (m2).
- **Mínimo.** La desigualdad $c_e(f_e)f^W_e-c_e(f_e-\delta)(f^W_e-\delta)\ge\delta c_e(f_e-\delta)$ es correcta porque los $c_e$ son no decrecientes y $f^W_e\ge0$. Su balance es $\le\delta(b_o-H)=-\delta$. Pasar el flujo del interruptor de tipo (iii) a $Z_0$ sólo añade flujo en $dz\to\mathsf d_z$, que $W$ no usa. En la cara resultante, $C_W$ vuelve a ser (eq:CW). Correcto.
- **Cargas y reparación $D+2$.** Calculé, para cada arco, la carga máxima posible, es decir, la suma de las demandas de las mercancías con alguna ruta por él (14/14 instancias):

  | Arco | Carga máxima en el DAG | Comentario |
  |---|---|---|
  | $e^1_m$, $e^2_m$ | exactamente $D+2$ | La cota $D+1$ del teorema es falsa aquí; la reparación es necesaria. |
  | $e^z_m$ | $D+1$ | Los nodos no pueden usarlo. |
  | $dz$ | $D+1$ | |
  | $p_m$, $o$, conectores | — | Costo constante; no intervienen en ninguna cota. |

  Ningún otro arco con pendiente positiva supera la carga supuesta. La desigualdad final $1+(D+2)\sum\alpha<2+2(D+1)\sum\alpha$ es correcta. Además verifiqué con cotas rigurosas (carga máxima frente a costo mínimo, en aritmética exacta) tres hechos, en 14/14 instancias:
  - $\max c_{P_i}<\min c_{S_i}$;
  - $\max c_{Z_1}<\min c_p$ para toda otra ruta $p$ del interruptor;
  - fijados $x=0$ y $z=1$, toda ruta de $W$ distinta de $O$ es estrictamente más cara para **todo** flujo de $W$.
- **$\Lone$ y $e_z$ con $B'$.** Correcto. La cota es $(1-z)(B'-\sigma_z(1+z)-(M-1)H)\ge0$ porque $B'-(M-1)H=B+(M-1)H\ge2\sigma_z$.
- **Co-NP en el DAG.** Correcto: descomposición de flujos en un DAG y QP sobre el politopo de flujos de arco por mercancía. Para $\Lone$ falta decir cómo se obtiene la "proyección de un cono de descripción polinómica"; es dualidad de PL con potenciales de nodo (m8).
- **Lo que el enunciado afirma de más.** "Theorem 5.12 holds, without the strong monotonicity of $F$" trae consigo las condiciones del teorema "every edge is used by at most two commodities" y "all commodities but one have exactly two paths". En el DAG ambas son falsas:
  - los arcos $e^1_m$ y $e^2_m$ están en rutas de tres mercancías ($W$, el nodo y el interruptor por rutas de tipo (iii)): máximo de 3 mercancías por arco en 14/14 instancias mías;
  - el interruptor tiene entre 4 y 15 rutas en mis instancias (hasta 20 en la salida del autor).

  Véase M1.
- **$F$ no es fuertemente monótono en el DAG.** El autor lo afirma y es cierto: el autovalor mínimo de $DF$ en el espacio tangente es $0$ (a $10^{-14}$) en 14/14 instancias. La dirección nula es: $\delta$ del interruptor de $Z_0$ a una ruta de tipo (iii) por $T_m$, y $\delta$ de $W$ de la ruta "$T_m$ prolongada por la cadena $Z_1$" a $O$. Con eso la Pregunta 7.1(ii) queda bien motivada.

### 1.5 Proposición 5.15 (353–362). Correcta

- (a) En las aristas con $a_e>0$, $g_e=\mu_ef_e$; $\Phi_\lambda$ es convexa y basta la Prop. 4.1(a).
- (b) Lema 5.11 más Kozlov–Tarasov–Khachiyan (QP convexa exacta en tiempo polinómico). Vale **sólo con rutas explícitas**, como dice el propio "(Explicit path sets.)" de la línea 356.

### 1.6 Etiquetas de estado y Pregunta 7.1

Las etiquetas "proved here, Appendix B; checked in E8" (339, 346, 350) son correctas. La Pregunta 7.1, en cambio, deja fuera un caso abierto y afirma de más el caso tratable (M2). En `results/CLAIMS.md` la fila del Teorema 5.12 llama "independiente" a la verificación del integrador (m6).

## 2. Verificación de la ronda anterior (ronda 3)

| Hallazgo | Estado | Evidencia |
|---|---|---|
| M1 (Prop. 5.9 como reducción estándar) | aplicado bien | Estado en `main.tex:313`; Remark 5.2 en 243 (Murty–Kabadi, Pardalos–Schnitger); resumen 66; `results/CLAIMS.md` (fila Prop. 5.9); `README.md:43`; `FICHA_EQO001_propuesta.md:13,24`. Detalle: la ficha pública dice "(señalada en la revisión interna)", una referencia a la historia interna, como en m9. |
| m1 (enunciado de la Prop. 5.9) | aplicado bien | 313: $x^*$ racional, "(and, for the first problem, a rational $\lambda\ge0$)", "number of variables … part of the input", $N=2$ y vector unitario sólo para pertenencia. |
| m2 (sentido "co-", $\sum_{\{i,j\}\in E}$, $w\ge0$) | aplicado bien | 418; también 425 para el Teorema 5.12. |
| m3 (Murty–Kabadi; Schrijver Thm 10.2) | aplicado bien | 417, 423, 465. El número del teorema sólo queda corroborado en parte (§4). |
| m4 (descripción de E6) | aplicado bien | 380 (`\HdFacePairs`, `\HdVertexPairs`, `\HdXcheck`). |
| m5 (co-NP en ruteo) | aplicado bien | La pregunta se retiró; el argumento está en 423 (rutas explícitas) y en 465 (flujos de arco en el DAG). |
| m6 (Remark 5.10) | aplicado bien | 319. |
| m7 (dos frases tras la Prop. 5.9) | aplicado bien | 316. |
| m8 (extensión) | aplicado a medias, justificado en parte | Recortes 1, 2, 3 y 5 hechos (§6 condensado en 367–389; Apéndice A en 409–411; Ej. 5.5 en 268; Remark 5.10 en 319). El recorte 4 (Ej. 5.7) se hizo sólo en parte, con una razón aceptable. El total pasó de 13 a 17 páginas por el material de ruteo (§6 de este informe). |
| m9 (referencias a versiones internas) | aplicado bien | `grep "v0\."` sólo encuentra la fecha (59); "internal review" sólo aparece en los agradecimientos (405). |
| m10 (README, RESPUESTA r1, CONTINUIDAD) | aplicado bien | `README.md:18` dice "Teorema 3.4"; `README.md:26–27` incluye hardness y three_commodity; `RESPUESTA_…ronda1:79` y `CONTINUIDAD:36` están anotados. |
| m11 (bibliografía) | aplicado bien | `refs.bib:270` (`number={2}` en Vavasis), 291–300 (Pardalos–Schnitger), 301–310 (KTK). |
| m12 (errata en el Ej. 5.5) | aplicado bien | 268. |
| m13 (cláusulas de los Ej. 5.6 y 5.8) | aplicado bien | 284 (pendiente cero, con demostración); 309 ("checked numerically, not used"). |
| Integración, RESPUESTA §1.4(1): cota $D+2$ | aplicado bien | 463; verificado en §1.4. |
| Integración §1.4(2): $\R^{n+2}_+$ en vez de $\R^m_+$ | aplicado a medias | Sólo en 453. El enunciado (339), el corolario (350) y su prueba (463) siguen diciendo $\R^m_+$, y en el Apéndice B $m$ indexa pares orientados (m1). "At least one edge" está aplicado (425). |
| Integración §1.4(3): cota de $c_{S_i}$ | aplicado bien | 346. |
| Integración §1.4(4): Pregunta 7.1(ii) | aplicado bien | 400. Falta el caso DAG con número fijo de mercancías (M2). |
| Integración §1.4(5): estado y macros | aplicado, pero la RESPUESTA se contradice | Véase m5. |

Recuento: 16 bien aplicados, 3 a medias (m8, $\R^{n+2}_+$ y el punto 5 de §1.4), 0 no aplicados.

## 3. Hallazgos nuevos

### Bloqueantes

Ninguno.

### Mayores

**M1. El enunciado del Corolario 5.14 hereda del Teorema 5.12 dos condiciones que en el DAG son falsas.** (`main.tex:350`; también `results/CLAIMS.md`, fila Corolario 5.14: "lo mismo (sin fuerte monotonía)"; `README.md:44`.)

- *Problema.* "Theorem 5.12 holds, without the strong monotonicity of $F$" incluye "every edge is used by at most two commodities" y "all commodities but one have exactly two paths". En la construcción acíclica:
  - $e^1_m$ y $e^2_m$ están en rutas de $W$, del nodo y del interruptor (rutas de tipo (iii), que la propia prueba describe en 459 y que la Pregunta 7.1(ii) menciona);
  - el interruptor tiene muchas rutas.
- *Evidencia.* En `verify_dag.py` (14/14 instancias), el máximo de mercancías por arco es 3 y el interruptor tiene de 4 a 15 rutas. La salida del autor (`theory/check_routing_hardness_output.txt`, línea "paths of W / of z") da hasta 20 rutas del interruptor.
- *Corrección.* Texto sustituto para 350: "When the input is a directed acyclic graph with origin–destination pairs and $P_k$ is the set of all paths of commodity $k$, both problems are co-NP-complete when the number of commodities is part of the input. Both remain co-NP-hard with $\lambda=e_W$, $f^*$ the unique Wardrop equilibrium (a vertex of $K$), integer demands, $\Lone(f^*)$ the orthant and every arc on paths of at most three commodities. In this construction $F$ is not strongly monotone (Question 7.1(ii))." Ajustar igual CLAIMS y README. Ya que se toca, definir en 339 "used by" como "lies on a path of".

**M2. La frontera de lo tratable se presenta sin la condición "rutas explícitas", y falta un caso abierto.** (`main.tex:400` y 364; `README.md:44`; `FICHA_EQO001_propuesta.md:13` y 24.)

- *Problema.* La Pregunta 7.1 dice "with a fixed number of commodities and weights of the form $\mu\mathbf 1_Q$, membership is polynomial (Proposition 5.15(b))" justo después de mencionar el DAG con todas las rutas. El README dice "$\lambda=\mu\mathbf 1_Q$ con número fijo de mercancías (Prop. 5.15)". La ficha dice "con pocas mercancías y pesos iguales es polinómica". Pero la Prop. 5.15(b) es sólo para rutas explícitas (356). En el marco del Corolario 5.14, todas las rutas de un DAG, un número fijo de mercancías no da un número polinómico de perfiles puros.
- *Por qué el caso no es trivial.* Ya con dos mercancías y $\lambda=e_W$, $\min_K\Phi_\lambda=\min_{f^W}\big[\text{convexa}(f^W)+d_R\cdot\mathrm{SP}_{a\circ f^W}\big]$. Aquí $\mathrm{SP}$ es la longitud del camino más corto con longitudes $a_ef^W_e$, una función cóncava de $f^W$. Es una minimización convexa más cóncava, y el texto no da ninguna cota de complejidad para ella.
- *Corrección.*
  - En 400, escribir "with explicit path sets, a fixed number of commodities and weights of the form $\mu\mathbf 1_Q$, membership is polynomial (Proposition 5.15(b))" y añadir "(iii) the same with all paths of an acyclic network, already for two commodities and $\lambda=e_W$".
  - En 364, escribir "unboundedly many weightless commodities sharing edges with the weighted paths is unavoidable, with explicit path sets, …".
  - En el README y la ficha (ES/EN), añadir "con conjuntos de rutas explícitos".

### Menores

- **m1 (notación; 339, 350, 453, 463, 432, 417).**
  - $\Lone(f^*)=\R^m_+$ aparece en el enunciado y en el corolario, mientras que en el Apéndice B $m$ indexa pares orientados ($m\in A$, $T_m$, $\alpha_m$, y "$\R^m_+$ as before" en 463). La RESPUESTA (§1.4(2)) dice haberlo cambiado, pero sólo lo hizo en 453.
  - $P_i$ es la ruta del nodo $i$ y $P_k$ el conjunto de rutas de la mercancía $k$ (Def. 2.5).
  - $\Phi$ es la cara en la prueba de la Prop. 5.9 y $\Phi_\lambda$ el potencial ponderado.
  - $o$ (arista), $O$ (ruta) y $\mathsf o_k$ (origen) se confunden fácilmente.
  - *Corrección:* escribir "the orthant $\R^{n+2}_+$" en 339, 350 y 463; renombrar los pares a $a\in A$ (con $T_a$ y $\alpha_a$) o la ruta $P_i$ a $U_i$; llamar $\mathcal F$ a la cara.
- **m2 (459 y 400; tipo (iii)).** "it starts $\mathsf o_z\to q_0\to dz$ and then follows arcs of W" es inexacto. Una ruta de tipo (iii) puede usar conectores de cadena de $S_i$ y de $P_j$, y termina por la cola de la cadena $Z_1$ (conectores $e^z\to e^z$ de costo $H$), salvo que entre en $e^z_M$. El argumento no cambia, porque sólo usa $q_0,dz\in p$ y el arco $dz\to\mathsf d_z$. *Corrección:* "…then continues along arcs of $W$ and chain connectors, and reaches $\mathsf d_z$ through the last arcs of $Z_1$". En la Pregunta 7.1(ii), "the last arcs of some $T_m$" debe decir "the arcs $p_m,e^1_m,e^2_m,e^z_m$ of some $T_m$ and the tail of $Z_1$".
- **m3 (463).** En el DAG, "$c_{T_m}-c_O=4\alpha_mt_m+2\alpha_m$" sólo es exacto si $W$ no tiene flujo en rutas de tipo (ii), porque ese flujo carga los $e^1,e^2,e^z$ de otros pares. *Corrección:* "$c_{T_m}-c_O\ge-\alpha_m+\alpha_mf_{e^2_m}+2\alpha_mf_{e^z_m}\ge2\alpha_m>0$, since $f_{e^2_m},f_{e^z_m}\ge1$ when $x=0$, $z=1$". Mi comprobación exacta (§1.4, tercer punto) confirma la desigualdad para todo flujo de $W$.
- **m4 (E8, 388; datos de la corrida).** El texto se lee "40+40 random graphs on 5 and 6 nodes (half with weights in {1,2,3})". Pero `theory/check_routing_hardness.py:448–457` genera 20 grafos unitarios y 10 pesados por cada $n$: son 30+30, y un tercio pesados. Las cuentas cuadran así: $7+63+30+30=130=$ `\RtGraphs`, no $70+80=150$. El "40" sale de una cadena fija del log (`check_routing_hardness.py:473–475`), que `make_numbers.py:266–267` lee como si fuera un dato. *Corrección:* escribir "30+30 random graphs on 5 and 6 nodes (one third with weights in {1,2,3})". Que los macros salgan de las cuentas y no del texto del log; como `theory/` no se toca, basta con fijar los dos macros en `make_numbers.py` con una nota, o calcularlos como `\RtGraphs`$-70$ repartido en partes iguales.
- **m5 (RESPUESTA ronda 3, §1.4 punto 5).** Dice "No se generan macros, porque `make_numbers.py` no lee esa salida… En el texto se dice que se copian". Contradice §0, §2-m4 y §3 de la misma respuesta, y los archivos (`make_numbers.py:251–285`; `numbers.tex:182–203`). También dice que el estado sería "independently re-derived by the author", cuando en 339 es "proved here, Appendix B; checked in E8", que es lo correcto. *Corrección:* añadir una nota de corrección en esa línea de la RESPUESTA.
- **m6 (`results/CLAIMS.md`, fila del Teorema 5.12).** "verificado de forma independiente por el autor en la ronda 3" y "chequeo propio independiente en 54 pares". El integrador no es un verificador independiente, y el chequeo de 54 pares vive en un scratchpad de sesión (`scratchpad/eqo_r3/indep_check.py`, según la RESPUESTA §1.3), no en el repositorio, así que no es reproducible. *Corrección:* "demostrado aquí (Apéndice B); verificado por el integrador (ronda 3) y por el árbitro de la ronda 4; comprobado en E8 (381 pares)". Quitar los 54 pares o incorporar el script.
- **m7 (409; `README.md:17`).** "turns them into the macros and table body used here": la tabla ya no se incluye (`grep table_random main.tex` no da nada). El README sigue describiendo `table_random.tex` como cuerpo de tabla del manuscrito. *Corrección:* "turns them into the macros used here", y en el README "(ya no se incluye en el manuscrito)".
- **m8 (465).** "so $\Lone(f^*)$ is the projection of a rational polyhedral cone of polynomial description" necesita una cláusula. *Texto sustituto:* "…by linear-programming duality, $\lambda\in\Lone(f^*)$ iff there are node potentials $\pi_k$ with nonnegative reduced arc costs for the linearised $\Phi_\lambda$ of each commodity, zero on its used arcs; so $\Lone(f^*)$ is the projection of a rational polyhedral cone…".
- **m9 (resumen, 66).** "the same holds for the per-commodity costs of multi-commodity Wardrop routing with affine costs" no dice "with explicit path sets or all paths of an acyclic network", que es justo donde vive el resultado. Añadirlo; cuesta media línea.
- **m10 (339).** "deciding whether $\lambda\in\Lam(f^*)$" con "a rational Wardrop equilibrium $f^*$" como dato. Conviene decir que comprobar que $f^*$ es un equilibrio de Wardrop es polinómico (rutas explícitas), para que el problema no sea de promesa. Basta media frase.
- **m11 (343, esbozo).** "one with a route $Z_1$ of a switch" mezcla artículos y no dice que $Z_1$ toca **todos** los $T_m$. Escribir: "and one with the route $Z_1$ of a switch commodity, which meets every $T_m$".
- **m12 (Remark 5.2, 243).** "We did not find Theorem 5.12 in the literature we consulted" es honesto, pero no dice qué se consultó. Una búsqueda mía rápida (WebSearch; §4) tampoco encontró un resultado equivalente. Dar dos o tres nombres de lo revisado: complejidad del equilibrio multiclase, peajes y Stackelberg.

## 4. Bibliografía

Método: WebSearch. Springer, Crossref y el PDF de la EPFL están bloqueados por el proxy (`CONNECT tunnel failed, 403`).

| Entrada | Estado | Corrección |
|---|---|---|
| kozlovTarasovKhachiyan1980 | **verificada**: MathNet zvmmf5189 da *Zh. Vychisl. Mat. Mat. Fiz.* 20:5 (1980), 1319–1323, y *U.S.S.R. Comput. Math. Math. Phys.* 20:5 (1980), 223–228; DOI en ScienceDirect 10.1016/0041-5553(80)90098-1. | Opcional: añadir `doi = {10.1016/0041-5553(80)90098-1}`. |
| pardalosSchnitger1988 | **verificada**: *Oper. Res. Lett.* 7, 33–35 (1988), título exacto. El número 1 y el DOI no los vi en la página del editor (bloqueada); son coherentes con el volumen. | Ninguna. |
| schrijver1986, "Theorem 10.2" | **corroborada en parte**: la §10.2 del libro se titula "Vertex and facet complexity" y contiene la cota "facet complexity $\varphi$ ⇒ vertex complexity $\le4n^2\varphi$". No pude ver el número del teorema en una fuente primaria. | Mantener; si no se puede cotejar, citar "Section 10.2", que sí está confirmado. |
| (literatura relacionada con el Teorema 5.12) | Una búsqueda ("multicommodity Wardrop … weighted sum … NP-hard") no encontró un resultado equivalente; sí apareció la PPAD-dificultad del equilibrio multiclase con costos por clase (arXiv 1811.08354), que es otro problema. | Opcional: citar esa entrada en el Remark 5.2 como "related but different". |

Las 36 entradas están citadas (36 `\bibitem` en la compilación).

## 5. Verificación computacional

Código propio, escrito sólo a partir del `.tex` y sin importar nada de `theory/` ni de `experiments/`. Está en el scratchpad (`verify_routing.py`, `verify_dag.py`, `edge_cases.py`).

- **Modelo.** Es un modelo genérico de red (aristas afines y listas de rutas). $C_k=\sum_ec_e(f_e)f^k_e$ se calcula desde los flujos de ruta, nunca con la forma cerrada.
- **Comprobaciones exactas** (con `Fraction`): equilibrio de Wardrop y su estrictez, $\Lone$ por la condición del Lema 2.6, testigo y Observación 5.13.
- **$\min_KC_W$.** Se calcula sobre los perfiles puros de las mercancías sin peso, resolviendo para cada uno el QP convexo en los flujos de $W$ con FISTA y proyección exacta al símplex. La cota inferior se certifica con la brecha de Frank–Wolfe. Lo contrasté de dos formas sin usar el Lema 5.11:
  - gradiente proyectado no convexo con arranques múltiples sobre todo $K$;
  - para $n\le3$, una malla $4^{n+1}$ sobre los flujos sin peso.

**Rutas explícitas (Teorema 5.12, Obs. 5.13): 208 instancias, 53 s de CPU.**

| Conjunto | Valores de $k$ |
|---|---|
| Todos los grafos no isomorfos con al menos una arista y 2–4 nodos, **incluidos los que tienen nodos aislados** | todos de $1$ a $\mathrm{maxcut}+1$, y $\mathrm{maxcut}+3$ |
| Los 33 grafos no isomorfos de 5 nodos | $\mathrm{maxcut}$ y $\mathrm{maxcut}+1$ |
| Variantes con pesos aleatorios en $\{1,2,3\}$ ($n=4$ con al menos 3 aristas, y $n=5$) | $\mathrm{maxcut}$ y $\mathrm{maxcut}+1$ |

Resultados:

| Comprobación | Resultado |
|---|---|
| $f^*$ es equilibrio de Wardrop exacto y estricto | 208/208 |
| Autovalor mínimo de $DF$ en el espacio tangente | $0.99999$ (positivo en todas) |
| Máximo de mercancías por arista | 2 |
| $C_W(f^*)=C^\star$ | 208/208 |
| $\Lone=$ ortante, exacto | 208/208 |
| Todo otro $e_h\in\Lam$ | 208/208 |
| $e_W\in\Lam\iff\mathrm{maxcut}<k$ | 208/208, 0 indecididos; 101 miembros y 107 no miembros |
| Umbral $k=\mathrm{maxcut}$ | 87 casos, todos no miembros con margen exacto $-\frac12$ |
| Desviación respecto de $C^\star+\min(0,k-\frac12-\mathrm{maxcut})$ | $\le5.7\times10^{-13}$ |
| Brecha FW máxima | $1.0\times10^{-11}$ |
| Testigo exacto $=\mathrm{maxcut}-k+\frac12$ | 107/107 |
| Observación 5.13: $\Delta\Phi_{\lambda_\varepsilon}\le-\frac14$ | 107/107 |
| Costos de ruta $\le\Gamma$ | 107/107 |
| Arranques múltiples y malla por debajo del mínimo en vértices | nunca (diferencia mínima $-2.8\times10^{-14}$) |

**DAG (Corolario 5.14): 14 instancias, 33 s de CPU.**

- Grafos: P2, P3, K3, 2K2, P4, K1,3 y K3 con pesos (1, 2, 3); $k\in\{\mathrm{maxcut},\mathrm{maxcut}+1\}$.
- Aciclicidad, estructura de rutas (i)–(iii), Wardrop exacto y estricto, cotas rigurosas de unicidad, $\Lone=$ ortante, $C_W(f^*)=C^\star$ y $e_W\in\Lam\iff\mathrm{maxcut}<k$: 14/14.
- Testigo exacto: 7/7. Otros $e_h\in\Lam$ (sólo $n\le3$, $k=\mathrm{maxcut}+1$): 4/4.
- Cargas máximas: $D+2$ en $e^1,e^2$; $D+1$ en $e^z$ y $dz$.
- Máximo de 3 mercancías por arco (M1). Autovalor mínimo tangente $\approx0$, es decir, sin monotonía fuerte, como dice el texto.
- Mi número de rutas de $W$ en K3 (38) difiere del del autor (37) porque el texto no fija el orden de las cadenas, y eso no altera nada.

**Casos borde (0.3 s de CPU):**

- *Arista de peso 0* (fuera de la hipótesis $w\ge1$): la equivalencia se mantiene, pero el equilibrio deja de ser estricto y $DF$ es singular, así que no hay unicidad ni monotonía fuerte. La hipótesis $w_{ij}\ge1$ (425) es necesaria y está bien puesta.
- *Arista paralela duplicada (multigrafo):* funciona como suma de pesos (3/3).
- *$k=10\gg$ peso total:* miembro.
- *Nodos aislados en el modelo explícito:* no afectan; el supuesto "sin nodos aislados" sólo hace falta para los $\deg(i)-1$ conectores del DAG.

**Compilación.** `latexmk -pdf` en una copia: 0 errores, 0 avisos, 0 referencias o citas indefinidas, 0 `??`, 17 páginas y 36 `\bibitem`.

**CPU total** de este arbitraje: ≈ 4 min. Una corrida previa más pesada se interrumpió a los ≈ 2 min y se rehízo con menos arranques múltiples. No reejecuté E1–E7, que no cambiaron en la v0.4.

## 6. Extensión

- **Distribución actual (compilación propia):** 17 páginas. El texto principal termina en la p. 13 (≈ 12.4), el material de ruteo ocupa pp. 10–11 (≈ 1.6), el Apéndice A ≈ 0.4, el Apéndice B pp. 14–15 (≈ 2.9) y la bibliografía pp. 16–17 (≈ 1.3).
- **Juicio.** El exceso sobre 10 páginas está justificado en parte. El Apéndice B contiene las demostraciones completas del único resultado propio, y quitarlas sería peor. El texto principal, en cambio, puede bajar a unas 11 páginas sin perder ninguna demostración.
- **Recortes concretos:**
  1. Llevar la prueba de la variante fuertemente monótona del Ej. 5.6 (desde "Indeed $x_3=1$…" en 284) al Apéndice B, dejando el enunciado de $\varphi$ (−0.3 p).
  2. Remark 5.2 (243) a la mitad. La frase sobre Dubey y el Ej. 5.5(i) ya está en el Ej. 5.5, y la frase sobre la Prop. 5.9 se repite en 313 y en 315–316 (−0.2 p).
  3. Fundir 315–316 con el estado de la Prop. 5.9: el esbozo de la reducción ya está en el Apéndice B (−0.15 p).
  4. E8 (388) a tres líneas: criterio, 381 pares, 0 discrepancias y la comprobación en el DAG. El resto puede ir en `results/` (−0.2 p).
  5. La Observación 5.13 a enunciado más una línea, con las cotas en el Apéndice B (−0.1 p).
  6. El Ej. 5.7, como pidió la ronda 3, reducido a la arista decisiva. El autor lo rechazó con una razón válida ("proved here"); se puede mantener la prueba moviéndola al Apéndice B (−0.3 p).

  Con esto el total queda en ≈ 15.5 páginas, con ≈ 11 de texto principal.
- **Llegar a 10 páginas** exigiría separar el material de ruteo (Lema 5.11–Prop. 5.15, Apéndice B salvo la Prop. 5.9, E8) en una nota propia. Es defendible, porque es el único resultado nuevo y la nota principal se presenta como un balance de "lo que es y no es un teorema". Lo dejo a decisión del autor, sin exigirlo.

## 7. Lista de acciones (prioridad descendente)

1. Reescribir el enunciado del Corolario 5.14 enumerando lo que vale en el DAG: hasta tres mercancías por arco, $F$ no fuertemente monótono y el interruptor con muchas rutas. Corregir la fila de CLAIMS y el README (M1).
2. Añadir "with explicit path sets" en la Pregunta 7.1 (400), en 364, en el README:44 y en la ficha (ES/EN). Añadir a la Pregunta 7.1 el caso abierto "(iii) número fijo de mercancías en un DAG con todas las rutas, ya con $\lambda=e_W$" (M2).
3. Corregir la descripción de E8 (30+30, un tercio pesados) y hacer que los macros salgan de las cuentas, no de la cadena del log (m4).
4. Sustituir $\R^m_+$ por $\R^{n+2}_+$ en 339, 350 y 463, y deshacer los choques de notación $m$, $P_i/P_k$ y $\Phi$ (m1).
5. Precisar el tipo (iii) en 459 y 400, y escribir la desigualdad de $c_{T_m}-c_O$ en 463 (m2, m3).
6. Añadir la cláusula de dualidad de PL en 465 (m8), "explicit path sets / acyclic" en el resumen (m9) y la media frase sobre la comprobación de Wardrop en 339 (m10).
7. Corregir la fila del Teorema 5.12 en CLAIMS (sin "independiente" ni "54 pares") y la contradicción del punto 5 de §1.4 de la RESPUESTA ronda 3 (m5, m6).
8. Quitar "table body used here" (409) y actualizar `README.md:17` (m7).
9. Ajustar el esbozo (343) y la frase de literatura del Remark 5.2 (m11, m12). Si no se puede cotejar el número de teorema de Schrijver, citar "Section 10.2" (§4).
10. Aplicar los recortes 1–5 de §6 (texto principal ≈ 11 páginas). Decidir si el ruteo va en nota aparte.
