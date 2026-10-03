# Respuesta del autor al informe de ronda 3 — EQO001 (03/10/2026)

**[EN CURSO]** — documento en redacción; este marcador se retira al terminar.

Objeto: borrador v0.3 → v0.4 (fecha fija 3 October 2026). Atiende (A) el informe `REFEREE_EQO001_ronda3_20261003.md` y (B) la integración del teorema de ruteo de `theory/routing_hardness.tex`, previa verificación independiente.

## 0. Resumen

(pendiente)

## 1. Verificación independiente del teorema de ruteo

Material verificado: `theory/routing_hardness.tex` (Lema `lem:concave`, Teorema `thm:routinghard`, Observación `rem:interior`, Corolario `cor:routingdag`, Proposición `prop:routingeasy`, Pregunta `q:multi` nueva), su derivación `theory/routing_hardness_derivation.md` y el script `theory/check_routing_hardness.py`. Los archivos de `theory/` no se modificaron: el script se copió al scratchpad y se ejecutó allí (escribe su salida junto a sí mismo).

### 1.1 Verificación a mano, paso a paso

**Lema `lem:concave`. Correcto.** Con $g_e=\sum_k\lambda_kf^k_e$, las mercancías de peso cero no entran en $g_e$ y entran linealmente en $f_e$, así que $\Phi_\lambda=\sum_e(a_ef_e+b_e)g_e$ es afín en $f^R$ para $f^Q$ fijo. Como $K=K^Q\times K^R$, $f^R\mapsto\min_{f^Q}\Phi_\lambda$ es un ínfimo de afines (cóncava), con mínimo en un vértice del producto de símplices (una ruta por mercancía). Con $\lambda=\mu\mathbf 1_Q$: $g_e=\mu f^Q_e$ y $\Phi_\lambda=\mu\sum_e(a_e(f^Q_e)^2+(a_er_e+b_e)f^Q_e)$, convexa en $f^Q$. Correcto.

**Teorema `thm:routinghard`. Correcto; dos precisiones de redacción.**
- *Pertenencia a co-NP.* El argumento de la Prop. 5.9 sólo usa que el objetivo es cuadrático y $K$ un poliedro racional dado por desigualdades: el maximizador está en el interior relativo de una cara, la restricción es convexa allí y el politopo de puntos estacionarios en la cara (gradiente constante en el soporte de cada mercancía: ecuaciones lineales racionales) tiene un vértice de tamaño polinómico. Con rutas explícitas, el número de variables es parte de la entrada. Para $\Lambda\ne\Lambda_1$: eliminando $\gamma_k$ (el valor en una ruta usada) en el Lema 2.5, $\Lambda_1(f^*)$ se describe por desigualdades lineales racionales explícitas en $\lambda$, es puntiagudo (está en el ortante) y sus rayos extremos tienen generadores de tamaño polinómico (Schrijver, Teorema 10.2). Correcto.
- *Identidad (eq:CW).* La rehíce arista por arista: $dz$ aporta $a_DD(D+1-z)$; $o$, $b_o(D-\sum t)$; $p_m$, $(b_o-\alpha_m)t_m$; $e^1_m$, $\alpha_m(t_m+x_i)t_m$; $e^2_m$, $\alpha_m(t_m+1-x_j)t_m$; $e^z_m$, $2\alpha_m(t_m+z)t_m$. La suma es exactamente $a_DD(D+1-z)+b_oD+\sum_m\alpha_m(4t_m^2+t_m(x_i-x_j+2z))$.
- *Minimización en $t$.* El mínimo de $4t^2+ct$ en $t\ge0$ está en $t=(-c)_+/8$ y vale $-(c_-)^2/16$. Además $t_m\le\frac18$ y $\sum t\le M/8\le D$ no está activa. Por tanto $h=C^\star+a_DD(1-z)-\sum_mw_m((x_j-x_i-2z)_+)^2$. $h$ es cóncava (mínimo de afines en $(x,z)$; también directamente, porque $-(s)_+^2$ es cóncava). Vértices: con $z=1$ vale $C^\star$; con $z=0$, cada arista cortada cuenta exactamente por una de sus dos orientaciones, y queda $C^\star+k-\frac12-\mathrm{cut}_w(x)$. Correcto. El testigo mejora en exactamente $\mathrm{cut}_w(x)-k+\frac12$ (comprobado).
- *Unicidad del equilibrio.* $f_{e^2_m}\le D+1$ y $f_{e^z_m}\le D+1$ en todo flujo factible, de donde $c_{P_i}\le1+(D+1)\sum\alpha<B\le c_{S_i}$ y $c_{Z_1}\le1+2(D+1)\sum\alpha<B\le c_{Z_0}$. Fijados $x=0$ y $z=1$, $c_{T_m}-c_O=4\alpha_mt_m+2\alpha_m>0$. Correcto. $F$ es afín, con $DF=\Delta^\top\mathrm{diag}(a)\Delta$. Si $h$ es tangente y $\sum_ea_e(\Delta h)_e^2=0$, las aristas privadas de pendiente 1 anulan $h$ en las rutas de nodos y del interruptor, $e^1_m$ anula $h_{T_m}$, y $h_O=-\sum h_{T_m}=0$. Por tanto $DF$ es definida positiva en el espacio tangente y $F$ es fuertemente monótono. Correcto.
- *$\Lambda_1$ y vectores unitarios.* Recalculé las derivadas de $C_W$ por ruta en $f^*$: $O$: $2a_DD+b_o$; $T_m$: $2a_DD+b_o+2\alpha_m$; $S_i$ y $P_i$: $0$; $Z_1$: $0$; $Z_0$: $a_DD$. Coinciden. Las cotas $C_i\ge\sigma_i(1-x_i)^2+Bx_i$ (porque $f_{e^2_m}\ge1-x_i$ en las aristas que entran en $i$) y $C_z\ge\sigma_zz^2+B(1-z)$ (porque $f_{e^z_m}\ge z$) son correctas. También lo son $B\ge2\sigma_i$ y, usando $D\ge1$, $B\ge2\sigma_z$. Correcto.
- *Precisiones (no afectan a la validez):* (i) el enunciado escribe $\Lone(f^*)=\R^m_+$, pero en la reducción $m$ designa los pares orientados; el número de mercancías es $n+2$. En el manuscrito se escribe $\R^{n+2}_+$ y "the orthant". (ii) $a_D=(2k-1)/(2D)$ exige $E_G\ne\emptyset$; un grafo sin aristas es trivialmente una instancia NO de MAX-CUT con $k\ge1$ y se envía a una instancia SÍ fija. Se añade "with at least one edge".

**Observación `rem:interior`. Correcta; completé una cota.** En el testigo ($x$ corte pesado, $z=0$, $t_m\in\{0,\frac18\}$): $c_{S_i}\le1+B+\frac98\sum\alpha\le2B$, $c_{P_i}\le1+\frac98\sum\alpha$, $c_{Z_1}\le\frac14\sum\alpha$ y $c_{Z_0}\le1+B+a_D(D+1)\le1+B+2k$. Todas son $\le\Gamma=2B+2k+1$. Como cada mercancía distinta de $W$ tiene demanda 1, $0\le C_h(y)\le\Gamma$, y $\Phi_{\lambda_\varepsilon}(y)-\Phi_{\lambda_\varepsilon}(f^*)\le-\frac12+\varepsilon(n+1)\Gamma=-\frac14$. El texto sólo mostraba la cota de $Z_0$; en el manuscrito añado la de $S_i$, que es la única que necesita una línea.

**Corolario `cor:routingdag`. Correcto tras reparar una cota.**
- Aciclicidad: los arcos suben de nivel o avanzan dentro de cadenas disjuntas, y en el nivel 0 sólo hay $q_0\to dz\to\{o,p_m\}$. Correcto.
- Estructura de rutas, puntos (i)–(iii). Correcta: desde $S_i$ sólo se sale hacia $P_j$ ($j\ne i$), hacia $Z_1$ o hacia $\mathsf d_W$, sin retorno.
- Paso "Minimum". Correcto: $c_e(f_e)f^W_e-c_e(f_e-\delta)(f^W_e-\delta)\ge\delta c_e(f_e-\delta)$; el conector de cadena da $\ge\delta H$ y $O$ gana $\delta b_o$, con balance $\le-\delta<0$. Mover el flujo del interruptor a $Z_0$ no aumenta $C_W$.
- **Hueco encontrado.** El paso "Equilibrium" dice que la dominancia $c_{P_i}<c_{S_i}$ "no cambia", pero en el DAG un arco $e^1_m$ o $e^2_m$ puede llevar, además de $W$ y del nodo, flujo del interruptor por una ruta de tipo (iii). La cota del teorema ($f\le D+1$) deja entonces de valer para todo flujo factible; la correcta es $f\le D+2$. La conclusión se mantiene: $1+(D+2)\sum\alpha<B$ porque $D+2\le2(D+1)$. En $e^z_m$ sigue valiendo $D+1$. En el manuscrito la frase se reescribe con la cota $D+2$.
- Precisión: "$\deg(i)-1$ conectores de cadena" presupone que no hay nodos aislados. Se supone sin pérdida de generalidad que $G$ no tiene nodos aislados (se pueden borrar sin cambiar el corte máximo).
- El resto (cota de $e_z$ con $B'$; derivadas de $C_W$ $\ge H-b_o$ en tipo (ii) y $\ge a_DD$ en tipo (iii); pertenencia a co-NP por descomposición de flujos en un DAG, que hace de $C_k$ una función de los flujos de arco por mercancía sobre un politopo de descripción polinómica) es correcto. Detalle: $\Lambda_1$ es la proyección de un cono racional en $(\lambda,\pi)$ por dualidad de PL; sus generadores tienen tamaño polinómico por la complejidad de vértices de Schrijver (Teorema 10.2), que se aplica también a poliedros no puntiagudos.

**Proposición `prop:routingeasy`. Correcta.** (a) En aristas con $a_e>0$, $g_e=\mu_ef_e$; $\Phi_\lambda$ es convexa y se aplica la Prop. 4.1(a). (b) Por el Lema `lem:concave`, basta enumerar los perfiles puros de las $r$ mercancías relevantes (a lo sumo $(\max|P_k|)^r$, polinómico con rutas explícitas y $r$ fijo) y resolver un QP convexo para cada uno; la resolución exacta en tiempo polinómico es Kozlov–Tarasov–Khachiyan. Precisión: (b) es para rutas explícitas (con todas las rutas de un DAG, $|P_k|$ puede ser exponencial); se dice en el texto.

**Pregunta `q:multi` nueva.** El enunciado es correcto. La derivación deja además abierta la variante "DAG con $F$ fuertemente monótono" (la construcción en DAG no da fuerte monotonía: las rutas de tipo (iii) no se distinguen por arcos de pendiente positiva propios). Se añade a la pregunta, y se retira la referencia "left open in v0.3" (m9).

### 1.2 Re-ejecución del script de verificación

`python3 check_routing_hardness.py` (copia en el scratchpad, versión completa, no reducida): 36 s de pared y 45.4 s de CPU (frente a los 27.0 s registrados; la diferencia se debe a la contención de núcleos). La salida es **idéntica línea a línea** a `theory/check_routing_hardness_output.txt`, salvo las líneas de tiempo de CPU: 381 pares, 0 discrepancias, `ALL CHECKS PASS: True`.

### 1.3 Chequeo propio independiente

Script `scratchpad/eqo_r3/indep_check.py` (135 s de CPU, semilla 4242), escrito sólo a partir del `.tex`; no importa nada de `theory/` ni de `experiments/`. Usa otros grafos (18 aleatorios con 3–5 nodos, sin nodos aislados, pesos en {1,2,3} en la mitad de los casos), otro método de minimización y otro solver de equilibrio:
- $C_W$ calculado arista por arista frente a la forma cerrada (eq:CW) en 20 puntos aleatorios por par: error relativo máximo $6.2\times10^{-16}$ en 54 pares $(G,k)$.
- Minimización de $C_W$ sobre $K$ en flujos de ruta con SLSQP desde 25 arranques, **sin usar el lema de concavidad**: en ningún par aparece un punto por debajo del mínimo predicho $C^\star+\min(0,k-\frac12-\mathrm{maxcut})$, y la pertenencia decidida coincide con la predicha en 54/54. El mínimo predicho se alcanza en 39/54; en los demás, SLSQP se queda en un mínimo local, pero ya por debajo de $C^\star$ cuando corresponde.
- Gradiente proyectado (iteración de Beckmann) desde 3 arranques aleatorios: converge a $f^*$ en 54/54, lo que es coherente con la unicidad.
- Observación `rem:interior`: para el testigo de un corte máximo, $\Phi_{\lambda_\varepsilon}(y)-\Phi_{\lambda_\varepsilon}(f^*)\le-\frac14$ y $C_h(y)\le\Gamma$ en 36/36 no miembros.
- DAG (16 pares): estructura de rutas 16/16. El programa lineal $\max_f\,[c_{P_i}(f)-c_{S_i}(f)]$ sobre **todos** los flujos factibles da $-449<0$, y $\max_f\,[c_{Z_1}-c_p]$, para toda otra ruta $p$ del interruptor, da $-52.5<0$: la dominancia vale. Pero $\max_f f_{e^2_m}=D+2$ se alcanza en 84 arcos, lo que **confirma el hueco de §1.1**: la cota $D+1$ del texto es falsa en el DAG, aunque la conclusión se mantiene.

### 1.4 Veredicto e integración

Los cinco enunciados son correctos. No se degrada ninguno. Correcciones aplicadas al integrarlos en el manuscrito (v0.4, §5.3 nueva y Apéndice B):
1. `cor:routingdag`: cota $f_e\le D+2$ en los arcos $e^1_m$ y $e^2_m$, y una frase que justifica que la dominancia sigue valiendo ($D+2\le2(D+1)$); "sin nodos aislados" se añade como supuesto sin pérdida de generalidad.
2. `thm:routinghard`: $\R^{n+2}_+$ en lugar de $\R^m_+$ (choque de notación); "graph with at least one edge"; el sentido "co-" escrito como en la Prop. 5.9 (complemento de MAX-CUT, m2).
3. `rem:interior`: cota explícita de $c_{S_i}$.
4. `q:multi`: se añade la variante "DAG con $F$ fuertemente monótono" y se retira la referencia a la v0.3.
5. Estado: "proved here (independently re-derived by the author, §1 of this response); checked in E8". Los números de E8 son literales de `theory/check_routing_hardness_output.txt`, reproducida idéntica. No se generan macros, porque `make_numbers.py` no lee esa salida y `theory/` no se toca. En el texto se dice que se copian de esa salida.

## 2. Respuesta punto por punto al informe de ronda 3

(pendiente)
