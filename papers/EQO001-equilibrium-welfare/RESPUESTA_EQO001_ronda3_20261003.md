# Respuesta del autor al informe de ronda 3 — EQO001 (03/10/2026)

Estado: **terminado** (03/10/2026).

Objeto: borrador v0.3 → v0.4 (fecha fija 3 October 2026). Atiende (A) el informe `REFEREE_EQO001_ronda3_20261003.md` y (B) la integración del teorema de ruteo de `theory/routing_hardness.tex`, previa verificación independiente.

## 0. Resumen

- **Informe de ronda 3** (veredicto: cambios menores; 0 bloqueantes, 1 mayor, 13 menores). Respuesta: **12 aceptados** (M1, m1–m4, m6, m7, m9–m13), **2 aceptados con matiz** (m5, m8) y **0 rebatidos**. Los tres residuos de la tabla "Verificación de la ronda 2" (M4 a medias, `number={2}` de Vavasis, "Teorema 3.8" en la respuesta de la ronda 1) quedan resueltos dentro de m8, m11 y m10.
  - **M1 (mayor) → aceptado.** La Prop. 5.9 se etiqueta como "in substance the standard MAX-CUT encoding of box-constrained quadratic programming, transported to games by Proposition 5.3". El cambio se aplica en el estado, en el Remark 5.2 (con Murty–Kabadi y Pardalos–Schnitger), en el resumen ("when the number of players is part of the input … a standard reduction"), en `results/CLAIMS.md`, en la ficha (ES/EN) y en el README. Se añade la entrada `pardalosSchnitger1988`.
- **Teorema de ruteo** (`theory/`): verificado a mano paso a paso, re-ejecutado (salida idéntica) y contrastado con un chequeo propio independiente (§1). Los cinco enunciados son correctos. En el Corolario `cor:routingdag` encontré un hueco menor: la cota $f_e\le D+1$ es falsa en el DAG (vale $D+2$), aunque la conclusión se mantiene. Lo reparé al integrarlo, junto con tres precisiones de redacción. Integrado como §5 "Routing" (Lema 5.11, Teorema 5.12, Observación 5.13, Corolario 5.14, Proposición 5.15), con las demostraciones completas en el Apéndice B, el párrafo E8 en §6 y la nueva Pregunta 7.1. La pregunta de ruteo de la v0.3 queda **respondida (co-NP-completa)**. Siguen **abiertos**: (i) un número fijo de mercancías con pesos positivos distintos y (ii) el DAG con $F$ fuertemente monótono.
- **Ningún número existente cambió.** `numbers.tex` sólo gana macros: los de la partición caras/vértices de E6 y los de E8, que se leen de la salida guardada de `theory/check_routing_hardness.py`. No queda ninguna cifra de E8 tipeada a mano.
- **Compilación:** 0 errores, 0 referencias o citas indefinidas, 0 `??`, 0 *Overfull* y 36 `\bibitem`. **Páginas:** la v0.3 tenía 13. La v0.4 tiene **17 en total**, con el **texto principal en ≈ 12.4** (termina en la p. 13); los apéndices ocupan ≈ 3.3 y la bibliografía ≈ 1.3. El teorema de ruteo añade ≈ 4.5 páginas de enunciados y demostraciones, y los recortes de m8 recuperan ≈ 1. Bajar el total a 13 exigiría quitar demostraciones o reducir la letra; no hice ninguna de las dos cosas.
- **Cómputo:** ≈ 3.2 min de CPU (re-ejecución del script de `theory/` 45 s; chequeo propio 135 s; `make_numbers.py` y compilaciones aparte).

## 1. Verificación independiente del teorema de ruteo

> **[Nota de corrección, ronda 4 (03/10/2026), hallazgo m6]** Lo que esta sección llama "verificación independiente" y "chequeo propio independiente" lo hizo quien integró el resultado en el manuscrito; no es independiente en el sentido de un árbitro. La verificación independiente es la del árbitro de la ronda 4 (`REFEREE_EQO001_ronda4_20261003.md`, §1 y §5). El script de §1.3 (`scratchpad/eqo_r3/indep_check.py`) está ahora en el repositorio como `experiments/routing_integrator_check.py`, con su salida en `results/routing_integrator_check_output.txt` (re-ejecutado en la ronda 4: idéntica salvo el tiempo de CPU).

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

   > **[Nota de corrección, ronda 4 (03/10/2026), hallazgo m5]** Este punto 5 describe un plan descartado y contradice §0, §2-m4 y §3 de esta misma respuesta y los archivos de la v0.4. Lo correcto es: (a) los números de E8 **sí** se generan como macros: `make_numbers.py` (líneas 251–285 de la v0.4) lee `theory/check_routing_hardness_output.txt` en modo sólo lectura y escribe los macros `\Rt*` en `numbers.tex` (líneas 182–203 de la v0.4); el manuscrito dice "numbers parsed from its saved output", no que se copien. (b) El estado aplicado en el manuscrito v0.4 fue "proved here, Appendix B; checked in E8", no "independently re-derived by the author". En la v0.5, tras la verificación independiente de la ronda 4, es "proved here, Appendix B; checked by an independent internal referee (round 4) and in E8". Véase `RESPUESTA_EQO001_ronda4_20261003.md`, m5.

## 2. Respuesta punto por punto al informe de ronda 3

Numeración del PDF v0.4: igual a la v0.3 hasta el Remark 5.10; luego Lema 5.11, Teorema 5.12, Observación 5.13, Corolario 5.14, Proposición 5.15, §6 (E1–E8), §7 (Pregunta 7.1 nueva), Apéndice A (reproducibilidad) y Apéndice B (demostraciones de la complejidad).

### Mayor

**M1 (la Prop. 5.9 presentada como propia) → aceptado.** El árbitro tiene razón: las piezas (codificación multilineal de MAX-CUT, pertenencia a NP de la QP, dureza de certificar optimalidad) son conocidas, y lo único específico del juego es que $F$ puede fijarse de antemano (Prop. 5.3). Cambios:
- Estado de la Prop. 5.9: "proved here; in substance the standard MAX-CUT encoding of box-constrained quadratic programming, transported to games by Proposition 5.3 (the equilibrium operator of the reduction does not depend on the instance); proof in Appendix B; checked in E6".
- Remark 5.2: frase nueva ("Proposition 5.9 is likewise standard in substance … cf. Murty–Kabadi 1987, Pardalos–Schnitger 1988 for local optimality; the game adds only that the equilibrium operator can be fixed in advance"). En el mismo lugar digo con cautela que no encontré el Teorema 5.12 en la literatura consultada.
- Resumen: "co-NP-complete when the number of players is part of the input, even for strongly monotone quadratic games (a standard reduction from box-constrained quadratic programming)".
- `results/CLAIMS.md`, ficha (ES/EN) y README: con la redacción propuesta por el árbitro, más el papel de $N$ como parte de la entrada.
- `refs.bib`: `pardalosSchnitger1988` (*Oper. Res. Lett.* 7(1), 33–35, 1988; DOI 10.1016/0167-6377(88)90049-1).

No añadí Pardalos–Vavasis (1991, una sola raíz negativa), que el encargo menciona como alternativa. Pardalos–Schnitger 1988 es la referencia verificada por el árbitro y la pertinente para "certificar optimalidad".

### Menores

- **m1 (enunciado de la Prop. 5.9) → aceptado.** Nuevo enunciado: cajas y $x^*$ racional; "(and, for the first problem, a rational $\lambda\ge0$)"; "when the number of variables (players, or the dimension of their actions) is part of the input"; escalares en $[0,1]$ y también $N=2$; "for membership, $\lambda$ a unit vector". Así queda explícito que **$N$ (o la dimensión) es parte de la entrada**. Con $N$ fijo y acciones escalares, el problema es polinómico (Remark 5.10).
- **m2 (prueba de la dureza) → aceptado.** (a) "We reduce the complement of MAX-CUT, which is co-NP-complete, to membership: YES-instances of MAX-CUT go to non-members". (b) $\sum_{\{i,j\}\in E}$ y $\deg_w(i)=\sum_{j:\{i,j\}\in E}w_{ij}$. (c) "$L\ge\mathrm{cut}$ … because $w\ge0$ (with a negative weight the reduction fails)". El mismo sentido "co-" se escribe en la prueba del Teorema 5.12.
- **m3 (Murty–Kabadi; Schrijver) → aceptado.** "Deciding that a given point is *not* a local minimiser of an indefinite quadratic programme is NP-complete (Murty–Kabadi 1987); see also Pardalos–Schnitger 1988". Schrijver se cita como "Theorem 10.2" en las cuatro apariciones, incluidas las del material de ruteo, que decía "Ch. 10". El número del teorema es de memoria del autor y del árbitro; no pude cotejarlo con el libro (anotado en CONTINUIDAD).
- **m4 (descripción de E6) → aceptado.** El texto dice ahora que la pertenencia se decidió por enumeración de caras en `\HdFacePairs` = 276 pares ($n\le4$) y sólo por vértices en `\HdVertexPairs` = 13 410, lo que presupone la multilinealidad de la prueba, con 36 cruces caras/vértices. Las cifras son macros nuevos de `make_numbers.py`, que suma `results_hardness.json` por `exact_method`.
- **m5 (Pregunta 7.1: pertenencia a co-NP en ruteo) → aceptado con matiz.** La pregunta desaparece, porque el Teorema 5.12 la responde, pero la observación del árbitro se incorpora donde hace falta. (i) Con conjuntos de rutas explícitos, el número de variables de ruta es parte de la entrada y $K$ es un producto de símplices dado por desigualdades explícitas. El argumento de la Prop. 5.9, que ahora se enuncia para cualquier poliedro racional dado por desigualdades (gradiente proyectado sobre el espacio de direcciones de la cara), se aplica directamente. (ii) Con todas las rutas de un DAG (Cor. 5.14), que pueden ser exponencialmente muchas, la prueba trabaja, como propone el árbitro, en los flujos de arco por mercancía, de los que depende cada $C_k$, sobre el politopo de flujos multimercancía, de descripción polinómica.
- **m6 (Remark 5.10) → aceptado.** "candidate tractable subclass that we do not study" y "no explicit description … by polynomially many polynomial inequalities of polynomial size computable in polynomial time". El Remark quedó en cuatro líneas, con el título "Descriptions of $\Lambda(x^*)$".
- **m7 (observación tras la Prop. 5.9) → aceptado.** Párrafo nuevo: $F$ no depende del grafo, de modo que la dureza vive en las externalidades (Prop. 5.3); con $N=2$, $\Lambda$ es poliédrico y difícil, mientras que el Ej. 5.6 es no poliédrico y de tiempo constante. Son fenómenos independientes.
- **m8 (extensión) → aceptado con matiz.**
  - Recortes 1 (§6 condensado; la Tabla 1 pasa a `results/tables_welfare.md`), 2 (Apéndice A a un párrafo) y 3 (Ej. 5.5) aplicados.
  - Recorte 5 (Remark 5.10) aplicado.
  - Recorte 4 (Ej. 5.7), sólo en parte: comprimí la prosa, pero **mantuve el análisis de las cuatro aristas**. Remitir tres aristas a E5 ("dominated (E5)") convertiría un ejemplo "proved here" en uno parcialmente "verificado numéricamente".
  - Además, las demostraciones largas (Prop. 5.9, Teorema 5.12, Corolario 5.14) pasaron al Apéndice B, con un esbozo de pocas líneas en el texto.
  - Resultado: texto principal de ≈ 12.4 páginas (sin el material de ruteo, que ocupa ≈ 1.6 páginas del texto principal, quedaría en ≈ 11) y **17 páginas en total**, porque el teorema de ruteo con sus demostraciones completas añade ≈ 4.5. No cambié la letra (11 pt) ni los márgenes.
- **m9 (referencias a versiones internas) → aceptado.** Retiradas del título del Remark 5.10, de E1 ("E1c of v0.2"), de §7 ("table of v0.2"), de los estados de los Ejemplos 5.6 y 5.8 y de la Prop. 5.9. La línea de fecha queda "Working draft v0.4 --- research line EQO001 --- 3 October 2026". El crédito pasa a un párrafo de agradecimientos (contraejemplo del Ej. 5.6, su variante, el Ej. 5.8, la reducción de la Prop. 5.9 y su reetiquetado). El historial queda en RESPUESTA y CONTINUIDAD. Comprobado con `grep`: no queda "v0.x" ni "internal review" salvo la fecha y los agradecimientos.
- **m10 (archivos acompañantes) → aceptado.**
  - `README.md`: "Teorema 3.5" → "Teorema 3.4"; filas de resultados con `hardness` y `three_commodity`, y fila nueva para `theory/`.
  - `RESPUESTA_EQO001_ronda1_20260930.md:79`: "Teorema 3.8" → "Teorema 3.7" (anotado).
  - `CONTINUIDAD:36`: marcado "[Superado: Prop. 5.9 … Teorema 5.12]".
- **m11 (bibliografía) → aceptado.** `number={2}` en `vavasis1990`; `pardalosSchnitger1988` añadida. Además `kozlovTarasovKhachiyan1980`, que exige la Prop. 5.15(b) (cotejada; véase CONTINUIDAD). `refs.bib`: 36 entradas, todas citadas.
- **m12 (errata) → aceptado.** "Collusion at $(\tfrac14,\tfrac14)$ gives each firm $\tfrac18>\tfrac19$." es ahora una frase propia.
- **m13 (completar los Ejemplos 5.6 y 5.8) → aceptado.**
  - Ej. 5.6: "$\varphi$ decreases to $\varphi(\frac{3}{4(1-\varepsilon)})=0$ with zero slope, so the boundary is tangent to the axis". Lo verifiqué a mano: en $\lambda_1=\frac3{4(1-\varepsilon)}$ se tiene $a=\lambda_1+\frac14=b=1+\varepsilon\lambda_1$, de donde $\varphi=\frac{3}{4(1-\varepsilon)}-\lambda_1=0$, y $\frac{d}{d\lambda}\frac{a^2}{2b}=1-\frac\varepsilon2$, de donde $\varphi'=0$. Es por tanto una afirmación demostrada.
  - Ej. 5.8: la frontera lineal fuera de $(\frac23,\frac32)$ se añade marcada "checked numerically, not used". Sólo demostré la rama convexa $\lambda_1\in(\frac14,\frac23]$, por KKT en $(0,\frac15)$, no el caso indefinido, así que no la presento como demostrada.

### Lista de acciones del árbitro (§6 del informe)

| # | Acción | Estado |
|---|---|---|
| 1 | Reetiquetar la Prop. 5.9 (estado, Remark 5.2, resumen, CLAIMS, ficha, README) | hecho (M1) |
| 2 | Enunciado de la Prop. 5.9 y sentido "co-", suma sobre aristas, $w\ge0$ | hecho (m1, m2) |
| 3 | Murty–Kabadi, Schrijver Thm 10.2, descripción exacta de E6 | hecho (m3, m4) |
| 4 | Dos frases tras la Prop. 5.9 | hecho (m7) |
| 5 | Pregunta 7.1 y Remark 5.10 | hecho; la Pregunta 7.1 queda sustituida por la nueva tras el Teorema 5.12 (m5, m6) |
| 6 | Recortes a ≈ 11 páginas | texto principal ≈ 12.4; total 17 por el teorema de ruteo (m8) |
| 7 | Quitar referencias a versiones y rondas internas | hecho (m9) |
| 8 | Cláusulas de los Ejemplos 5.6 y 5.8 | hecho (m13) |
| 9 | README, RESPUESTA r1:79, CONTINUIDAD:36, Vavasis, Pardalos–Schnitger, errata | hecho (m10–m12) |

## 3. Archivos modificados

- `manuscript/main.tex` (v0.4), `manuscript/refs.bib` (+2 entradas y `number` de Vavasis), `manuscript/numbers.tex` (regenerado, 202 macros) y `manuscript/main.pdf`.
- `experiments/make_numbers.py`: macros de E6 por método y macros de E8 leídos de `theory/check_routing_hardness_output.txt`, sólo lectura.
- `results/CLAIMS.md`, `README.md`, `FICHA_EQO001_propuesta.md`, `CONTINUIDAD_EQO001_20260930.md` y `RESPUESTA_EQO001_ronda1_20260930.md` (línea 79).
- **No** se modificó nada en `theory/` ni en otras carpetas de `papers/`. No se usó git.
