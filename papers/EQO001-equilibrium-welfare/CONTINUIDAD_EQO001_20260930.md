# EQO001 — Continuidad interna, 30/09/2026 (actualizada el 03/10/2026 tras las rondas 1, 2 y 3 de revisión interna; v0.4)

Documento de trabajo interno. No incorporar al manuscrito ni a entregas institucionales. Las secciones originales (v0.1) se conservan con correcciones marcadas **[corregido 03/10]**; la sección final recoge la ronda 1.

## Proyecto y alcance
Línea EQO001, "Operadores de equilibrio y bienestar" / "Equilibrium operators and welfare", área Decisiones, redes y operaciones, estado en el CV web: "En pausa". Ficha pública: exploración de formulaciones que conectan operadores de equilibrio, desigualdades variacionales y criterios de bienestar; objetivo: identificar una relación formal que produzca resultados más allá de los enfoques existentes; hallazgos: la formulación revisada combina componentes conocidos sin establecer todavía un teorema independiente; alcance: no se reportan hallazgos empíricos ni una nueva solución de equilibrio general.

Encargo de esta sesión (subagente de Claude Code, 30/09/2026): escribir la nota definitiva de "qué es y qué no es un teorema aquí", con demostraciones, y un resultado pequeño nuevo solo si se puede demostrar. Sin git; el coordinador integra la carpeta.

## Supuestos (qué hubo que reconstruir de la ficha)
1. **No existe manuscrito previo.** Todo el contenido se redactó desde cero a partir de la ficha; no se buscó en Drive, correo ni chats (fuera del alcance de este subagente). Si el autor conserva notas de la "formulación revisada", deben cotejarse con la Proposición 4.1 y el Corolario 4.3, que son nuestra lectura de qué era esa formulación (condición KKT compartida + peajes de costo marginal).
2. **Marco elegido:** dimensión finita, $K$ convexo cerrado, $F$ continuo; equilibrio = solución de $\mathrm{VI}(F,K)$; bienestar = funcional $C^1$ a maximizar; para juegos, la clase de bienestar es $W_\lambda=\sum_i\lambda_iu_i$ con $\lambda\ge0$. Se excluyen estrategias mixtas, juegos atómicos de congestión, dinámica y demanda estocástica.
3. **Interpretación de "grad W proporcional a F en la cara de equilibrio" del encargo:** la versión exactamente demostrable es que ambos vectores están en el cono normal $N_K(x^*)$; sobre una cara de un simplex ambos son constantes en el soporte (de ahí "proporcionales en la cara"); en general (forma estándar $\{x\ge0: Ax=b\}$) ambos restringidos al soporte están en el espacio fila de $A$, no necesariamente proporcionales entre sí. Se escribió la versión correcta (Prop. 4.1(c)), no el eslogan.
4. **"Cono de bienestar" del resultado nuevo:** se definió $\Lambda(x^*)$ como el conjunto exacto de pesos y $\Lambda_1(x^*)$ como el cono de primer orden; la caracterización completa (igualdad) solo se demuestra bajo concavidad conjunta de los pagos, y se muestra con testigos que sin ella la inclusión es estricta.

## Decisiones tomadas
- **Honestidad sobre la novedad.** El Teorema 5.1(a),(e) es escalarización estándar de optimización multiobjetivo (Geoffrion 1968, Ehrgott 2005); la Prop. 5.3 **[corregido 03/10: numeración del PDF]** es un reempaquetado de la función gap de Nikaidô–Isoda (1955). Ambas cosas se dicen en el texto y en la tabla de afirmaciones. Lo específico de la nota es la lectura por bloques en términos de $F(x^*)$, el cono normal y las externalidades marginales, y la conclusión de imposibilidad ($(F,K)$ no determina $\Lambda$).
- **Solver:** solo la iteración de gradiente proyectado con paso $\gamma=\mu/L^2$, para que cada equilibrio calculado venga con demostración de unicidad (Teorema 3.5 **[corregido 03/10]**) y residuo certificado; no se usó extragradiente ni solvers de terceros para los equilibrios. Para el cono de primer orden se usó `scipy.optimize.linprog` (HiGHS); para la pertenencia exacta a $\Lambda$, enumeración de las $3^N$ caras de la caja (exacta salvo redondeo), con contraste por ascenso de gradiente proyectado multi-arranque en 13 instancias cóncavas (discrepancia máxima $1.4\times10^{-17}$).
- **Testigos certificados:** una $\lambda\in\Lambda_1\setminus\Lambda$ se cuenta solo si existe $x\in K$ con $W_\lambda(x)>W_\lambda(x^*)+10^{-6}$, de modo que la inclusión estricta queda demostrada por el testigo y no depende de tolerancias.
- **Familia aleatoria:** pagos cuadráticos con acciones escalares en $[0,1]$; diagonales de $H_i$ elevadas para que la parte simétrica de $M$ tenga autovalor mínimo $1/2$ (monotonía fuerte + concavidad propia, así Nash ⇔ VI). Los coeficientes lineales $N(1,1.5^2)$ ponen 64–75 % de las coordenadas del equilibrio en la frontera; con menos frontera los conos son casi siempre triviales (coordenadas interiores imponen igualdades). Esta elección es arbitraria y se declara como tal; las frecuencias de la Tabla 3 son descriptivas de esta distribución y no tienen significado general.
- **Idioma:** manuscrito en inglés; README y esta nota en español.
- **Extensión:** el manuscrito quedó en 13 páginas a 11pt con 1in de margen (objetivo del brief: 5–10). Se prefirió conservar las demostraciones completas, que son el objeto de la nota; si se exige recortar, los candidatos son la Sección 6 (protocolos) y las demostraciones de los Lemas 2.4–2.7. **[03/10: véase la sección "Ronda 1"; la v0.2 tiene 14 páginas.]**

## Resultados de referencia (semilla 20260930; E1 en 5 s, E2–E4 en 125 s con contención de CPU)
- **E1a Pigou** ($c_1=1$, $c_2=x^d$): PoA $=1.333333$ ($d=1$), $1.6258$ ($d=2$), $2.1505$ ($d=4$), $3.0808$ ($d=8$), $4.7268$ ($d=16$); forma cerrada y búsqueda en rejilla coinciden a $<10^{-9}$.
- **E1b redes paralelas afines** (200 instancias, 2–5 enlaces): PoA máximo 1.2094, media 1.0305, mediana 1.0027; 0 violaciones de $4/3$; 41 % con PoA $>1.01$, 12 % con PoA $>1.10$; residuo VI máximo $3.4\times10^{-11}$; desviación máxima respecto al water-filling exacto $8.8\times10^{-11}$; máximo 2649 iteraciones.
- **E1c peajes de costo marginal:** **[corregido 03/10, hallazgo M1]** en v0.1 se comparaban dos corridas del mismo solver sobre la misma función ($c+\tau$ y $\nabla C$ coinciden para costos afines), de ahí el $2.2\times10^{-16}$ tautológico; en v0.2 se compara el equilibrio con peajes (solver) con el óptimo por water-filling independiente: $\|f_{\text{peaje}}-f_{\text{opt,wf}}\|_\infty\le8.8\times10^{-11}$ en las 200 instancias.
- **E2 ejemplo de dos jugadores** ($\alpha=2$, $\beta_1=\beta_2=1/2$): $x^*=(1,1)$, residuo 0; bordes del cono en 26.57° y 63.43°; 181/181 direcciones con acuerdo entre forma cerrada, test lineal y maximización exacta (73 dentro del cono **[corregido 03/10, hallazgo m8; antes decía 75]**); para $\lambda=(1,3)$ el maximizador exacto es $(0.5,1)$, mejor en 0.1250.
- **E2 Cournot:** interior ($a=1$): $q^*=(1/3,1/3)$, 0/61 direcciones en $\Lambda$ (colusión $(1/4,1/4)$ da $1/8>1/9$); frontera ($a=4$): $q^*=(1,1)$, cono de dimensión 1 (rayo $\lambda_1=\lambda_2$), acuerdo 61/61 entre test lineal y exacto. Modificación de Nikaidô–Isoda: máximo de $W'_\lambda$ sobre rejilla $401\times401$ y 61 direcciones $\le2.8\times10^{-17}$ (=0).
- **E3 juegos cóncavos** ($N=3$: 100; $N=4$: 100): conos no triviales 28 y 33; dimensiones ($N=3$) 1:4, 2:5, 3:19; ($N=4$) 1:2, 2:7, 3:15, 4:9; puntos del cono en $\Lambda$: 115/115 y 153/153; rejilla dentro de $\Lambda_1$ en $\Lambda$: 575/575 y 307/307; rejilla fuera de $\Lambda_1$ fuera de $\Lambda$: 8525/8525 y 16193/16193; residuo máximo $7.7\times10^{-12}$.
- **E4 juegos no cóncavos** ($N=3$, $N=4$, 100 c/u): conos no triviales 57 y 46; puntos del cono en $\Lambda$: 162/206 y 152/246; rejilla dentro: 1025/1063 y 1265/1337; fuera: 8037/8037 y 15163/15163 (la inclusión $\Lambda\subseteq\Lambda_1$ nunca falla); instancias con testigo certificado de inclusión estricta: 23 y 35 (58/103 = 56 % de las que tienen cono no trivial); testigos totales 44 y 94. Ejemplo: instancia 1 de $N=3$, $x^*=(1,1,1)$, $\lambda=(0,0.552,0.448)\in\Lambda_1$, el punto $(0,1,1)$ mejora $W_\lambda$ en 0.215.

## Limitaciones (y lo que NO se afirma)
- No se afirma ningún concepto de equilibrio nuevo, ninguna "solución general de equilibrio", ningún resultado empírico.
- El Teorema 5.1 es de primer orden; su única condición suficiente de igualdad es la concavidad conjunta, que excluye Cournot y la mayoría de juegos con externalidades bilineales.
- La decisión $\lambda\in\Lambda(x^*)$ para $W_\lambda$ no cóncava es un QP no convexo sobre una caja; aquí es tratable solo porque $N\le4$ ($3^N$ caras). No se cita complejidad (se evitó citar Pardalos–Vavasis por no tener certeza bibliográfica completa). **[Superado: Prop. 5.9 de la v0.3 (complejidad en juegos, reducción estándar; se citan Murty–Kabadi 1987, Pardalos–Schnitger 1988 y Vavasis 1990) y Teorema 5.12 de la v0.4 (ruteo).]**
- No se revisó exhaustivamente la literatura de peajes (toll pricing) ni de equilibrio multiobjetivo; la lectura del Teorema 5.1 puede existir ya en otra forma.
- Las frecuencias de conos no triviales y de testigos dependen de la distribución de instancias; no se les atribuye significado general.

## Bibliografía: notas de certeza
Todas las entradas de `refs.bib` corresponden a obras reales. **[03/10]** El árbitro verificó las 24 entradas de v0.1 contra páginas de editorial: Wardrop 1952 corregida a *Proc. ICE Part II* 1(3), 325–362 (discusión 362–378); Hearn–Ramana 1998 y Correa et al. 2004 confirmadas. Entradas añadidas en v0.2: Dubey 1986, Benson–Sun 2000, Ahuja–Orlin 2001, Murty–Kabadi 1987 (verificadas por el árbitro); Danskin 1966 (cotejada por el autor con WebSearch: SIAM J. Appl. Math. 14, 641–664; fascículo omitido); Bochnak–Coste–Roy 1998 (libro estándar; datos por conocimiento del autor, no cotejados en línea). Texto original de v0.1: datos que convenía cotejar: páginas de Wardrop 1952 (325–378, como las citan Roughgarden–Tardos; algunas fuentes dan 325–362); páginas de Hearn–Ramana 1998 (109–124) en el volumen de Marcotte–Nguyen; páginas de Correa–Schulz–Stier-Moses 2004 en *Math. Oper. Res.* 29(4) (961–976). El resto (Rosen 1965, Monderer–Shapley 1996, Roughgarden–Tardos 2002, Dafermos 1980, Smith 1979, Nash 1951, Nikaidô–Isoda 1955, Hartman–Stampacchia 1966, Geoffrion 1968, Knight 1924, Harker–Pang 1990) se cita con volumen y páginas que consideramos correctos.

## Pendientes y próximos pasos concretos (v0.1; estado al 03/10 entre corchetes)
1. **[Hecho: informe del 30/09; m7 resolvió el punto del test exacto]** Revisión arbitral interna independiente del borrador v0.1 (no se hizo en esta sesión), con atención a: enunciado de la Prop. 4.1(c) (uso de Farkas), la afirmación de que el maximizador de una cuadrática sobre una caja es estacionario en el interior relativo de su cara (usada por el test exacto), y la redacción de la Prop. 5.2 (diferenciabilidad de $v_i$ no se necesita y se dice).
2. **[Superado por B1: para $N=2$ todo cono convexo cerrado es poliédrico; para $N=3$ el Ej. 5.6 muestra que no lo es en general]** Pregunta abierta 1 para $N=2$: análisis de casos sobre las 9 caras de $[0,1]^2$ para describir $\Lambda(x^*)$ con condiciones de segundo orden; decidir si es poliédrico.
3. **[Hecho: Ej. 5.7 y E5; $\Lambda\ne\Lambda_1$]** Pregunta abierta 2: formular el cono de pesos por mercancía en una red de Wardrop de dos mercancías con costos afines y calcularlo en un ejemplo pequeño.
4. Extender E4 a $N=5,6$ con un solver global (o enumeración de caras vectorizada) para ver si la fracción de inclusión estricta cambia.
5. **[Parcial: 14 páginas en v0.2, véase abajo]** Decidir destino (nota expositiva; posible arXiv math.OC) y recortar a 10 páginas si se requiere.
6. **[Pospuesto a la ronda 2 (hallazgo M3); propuesta escrita en `FICHA_EQO001_propuesta.md`]** Actualizar la ficha EQO001 del CV web: de "En pausa" a "Cerrada como nota expositiva — borrador v0.1", con el hallazgo reformulado: "se demuestra que $(F,K)$ por sí solo no determina la optimalidad de bienestar del equilibrio; el cono de pesos de bienestar queda caracterizado bajo concavidad conjunta y acotado en general".


## Ronda 1 de revisión interna (30/09/2026) — respuesta aplicada el 03/10/2026 (v0.2)

Informe: `REFEREE_EQO001_ronda1_20260930.md` (cambios mayores; 1 bloqueante, 5 mayores, 18 menores). Respuesta punto por punto: `RESPUESTA_EQO001_ronda1_20260930.md`. Recuento: 21 aceptados, 3 con matiz (M4, m12, m16), 0 rebatidos. Cómputo de la sesión: ≈ 1.5 min de CPU (welfare 81–87 s ×2, traffic 3 s, commodity 4 s ×3) más compilaciones.

| Hallazgo | Acción |
|---|---|
| B1 Pregunta abierta 1 no abierta / mal planteada | Contraejemplo verificado a mano y numéricamente; nuevo Ej. 5.6 (cono no poliédrico, frontera parabólica) con crédito a la revisión; E2c en `welfare_cone.py`; Pregunta 8.1 reformulada (semialgebraico por Tarski–Seidenberg; $N=2$ trivial; quedan caracterización de $\Lambda=\Lambda_1$/poliedralidad y complejidad). |
| M1 E1c tautológico | `traffic_poa.py` compara el equilibrio con peajes con el water-filling independiente ($8.8\times10^{-11}$); texto, Tabla 2, README y esta nota corregidos. |
| M2 Literatura | Dubey 1986, Benson–Sun 2000, Ahuja–Orlin 2001, Danskin 1966 citados donde corresponde; Remark 5.2 nuevo sobre qué es estándar; frase de novedad reescrita. |
| M3 "definitive" | "records the assessment" / "recoge la evaluación"; cambio de ficha pospuesto a ronda 2. |
| M4 Criterios | `check_criteria()` en los tres scripts, bloque `criteria` en JSON/MD, frases generadas por `make_numbers.py`; texto honesto: sin registro externo de prerregistro. |
| M5 56 % | "at least 56 %", "in every tested direction"; los 110 puntos de rejilla en $\Lambda_1\setminus\Lambda$ se mencionan como no contados. |
| m1–m18 | Todos aplicados (detalle en la respuesta). m18 llevó al Ej. 5.7 / E5 (contraejemplo para la segunda mitad de la Pregunta 2). |
| Bibliografía | Wardrop 1952 y Nikaidô–Isoda corregidas; 6 entradas nuevas; 30 en total. |
| Extensión | Recortes del §6 del informe aplicados (resumen ≈ 195 palabras, protocolos al Apéndice B, Fig. 3 y Tabla de Pigou fuera, Remark 3.3 y "Contributions" comprimidos, Lema 3.4 con demostración de una línea). Resultado: 14 páginas (v0.1: 13) porque los añadidos pedidos (dos ejemplos demostrados, E5, Danskin, Remark 5.2, Apéndice B) suman ≈ 3.5 páginas. No se cambió tamaño de letra ni márgenes. |
| Cajas desbordadas | Las dos de v0.1 corregidas (Remark 3.6 reformulado; Tabla de afirmaciones a 0.60/0.34 con `\raggedright`); compilación final sin errores ni referencias indefinidas. |

### Resultados de referencia añadidos en v0.2 (semilla 20260930)
- **E2c (Ej. 5.6):** residuo 0 en $x^*=(1,1,1)$; rebanada $\lambda_3=1$: 7 381 puntos, 0 discrepancias con la parábola; frontera por bisección a $1.0\times10^{-8}$ de la parábola; $(0.3,0,1)\in\Lambda_1\setminus\Lambda$, testigo $(0.55,0,1)$, brecha $0.10125$. Variante $\varepsilon=0.2$: $\mu=0.2$, $x^*=(1,1,1)$, segundas diferencias de la frontera en $\lambda_1\in[0.35,0.75]$ todas positivas (mín. $1.7\times10^{-3}$).
- **E5a (Ej. 5.7):** $f^*=(1,0)$, residuo 0, $C(f^*)=(1,0.25)$; 91/91 direcciones en $\Lambda_1$, 89/91 en $\Lambda$; umbral $\lambda_1=0.025000$ en $\lambda_2=1$ (predicho $1/40$); $\lambda=(0,1)$: minimizador $(0,0.2)$, costos $(3,0.2)$, brecha $0.0500$; $\lambda=(1,1)\in\Lambda$.
- **E5b:** 200 instancias; 33 equilibrios en esquina; la rejilla de 91 direcciones toca $\Lambda_1$ en 90 instancias, $\Lambda_1=\mathbb R^2_+$ en 9; 21 instancias con testigo certificado; 0 violaciones de $\Lambda\subseteq\Lambda_1$; 3 desacuerdos a nivel de tolerancia (instancia 96, coordenada interior; violación de primer orden $\le5.1\times10^{-5}$, brecha del QP $3$–$9\times10^{-9}<10^{-8}$), registrados en el JSON; residuo máximo $3.8\times10^{-12}$.
- **E1 y E3–E4:** idénticos a v0.1 salvo el campo nuevo de E1c y los contadores de PoA $=1$ (86/200).

### Lo que queda abierto tras la ronda 1
1. **[Resuelto en la ronda 2: Prop. 5.9 y Remark 5.10 de la v0.3]** Pregunta 8.1 reformulada: caracterización de $\Lambda=\Lambda_1$ y de la poliedralidad por patrón de caras y hessianos; complejidad de decidir $\lambda\in\Lambda(x^*)$ (sólo se cita la dureza de la optimalidad local, Murty–Kabadi 1987; la complejidad exacta de la pertenencia no se ha establecido); descripción de tamaño polinómico bajo monotonía fuerte. Próximo paso concreto: análisis de las 27 caras para $N=3$ con el Ej. 5.6 como guía.
2. **[Resuelto en la ronda 2: Ej. 5.8 de la v0.3; la segunda parte se sustituye por la Pregunta 7.1]** Pregunta 8.2 reformulada: $m\ge3$ mercancías (para $m=2$ el cono es poliédrico por trivialidad); estructuras de red con $\Lambda=\Lambda_1$ (sin enlaces compartidos es inmediato).
3. **[Resuelto en la ronda 2: forma cerrada $\varphi$ demostrada]** La variante fuertemente monótona del Ej. 5.6 está verificada sólo numéricamente.
4. Prerregistro: los criterios se evalúan por máquina desde v0.2, pero no hay evidencia externa de que se fijaran antes de la primera corrida (sólo las marcas de tiempo de la sesión del 30/09).
5. Extensión: 14 páginas; bajar a 10 exigiría quitar demostraciones o los ejemplos nuevos.
6. Ronda 2 de arbitraje sobre la v0.2 (atención a los Ej. 5.6–5.7, E5 y las preguntas reformuladas); después, actualizar la ficha del CV con `FICHA_EQO001_propuesta.md`.
7. Pendiente 4 de v0.1 (E4 con $N=5,6$ y solver global) sigue abierto; E5 con $m=3$ también.


## Ronda 2 de revisión interna (03/10/2026) — respuesta aplicada el 03/10/2026 (v0.3)

Informe: `REFEREE_EQO001_ronda2_20261003.md` (cambios mayores de alcance acotado; 0 bloqueantes, 4 mayores, 12 menores; reproducción completa idéntica; Ej. 5.7 verificado). Respuesta punto por punto: `RESPUESTA_EQO001_ronda2_20261003.md`. Recuento: 13 aceptados, 3 aceptados con matiz (M2, M4, m6), 0 rebatidos. Numeración del PDF v0.3 (la Prop. 3.1 de la v0.2 pasó a un párrafo, de modo que el Teorema 3.2 es ahora 3.1, etc.).

| Hallazgo | Acción |
|---|---|
| M1 Pregunta 8.1(ii) no abierta | Nueva **Prop. 5.9** (co-NP-completitud de decidir $\lambda\in\Lambda(x^*)$ y $\Lambda=\Lambda_1$; difícil aun con $F$ fuertemente monótono, $x^*$ vértice, $\lambda$ unitario, $\Lambda_1=\mathbb R^N_+$, y con $N=2$ y acciones vectoriales), con pertenencia a co-NP demostrada (cara del maximizador + vértice de un politopo racional, Schrijver 1986; Vavasis 1990 cotejado en línea) y reducción desde MAX-CUT (Karp 1972). E6 nuevo (`hardness_maxcut.py`): 1696 grafos, 13 686 pares $(G,k)$, 0 discrepancias. Pregunta 8.1 retirada (Remark 5.10): la parte (i) no tiene respuesta comprobable eficientemente salvo P = NP. |
| M2 expectativa $m\ge3$ | Instancia del árbitro verificada (`confirm_m3.py`: $v''\approx0.0055$–$0.0115$ en $[1.6,2.6]$; brecha 0.00321 con L-BFGS-B independiente). Se encontró una instancia racional y se **demostró** a mano (Ej. 5.8): $\Lambda(y^*)=\{\lambda_3+m\ge0\}$, frontera $\psi(\lambda_1)=\lambda_1(\lambda_1+1)/(4(4-\lambda_1)(4\lambda_1-1))$. E7 nuevo (`three_commodity.py`). La reformulación sugerida por el árbitro ("¿$\Lambda=\Lambda_1$ con $b\equiv0$?") **no** se adoptó: E5b ya contiene 4 contraejemplos (de 27 instancias con $b\equiv0$). Nueva Pregunta 7.1: complejidad de la pertenencia en ruteo multimercancía. |
| M3 variante fuertemente monótona | Forma cerrada $\varphi$ demostrada en el Ej. 5.6 (sin la restricción "mientras el hessiano sea indefinido": el caso semidefinido negativo se cubre con $\lambda\in\Lambda_1$); E2c compara con $\varphi$ ($1.1\times10^{-8}$; criterio $10^{-7}$ nuevo). |
| M4 extensión | 14 → 13 páginas. Todos los recortes propuestos aplicados, más figuras remitidas por ruta y bibliografía a dos columnas; no se llega a 11 porque la ronda pidió ≈2 páginas de demostraciones nuevas. |
| m1 E1c | Fusionado con E1b (código, criterio y texto); E1 pasa de 5 a 4 criterios. |
| m2 $\gamma=\mu/L^2$ | Remark 3.5 y §6: excepción de E2c ($\gamma=1$, unicidad por dominancia). |
| m3 "never determines" | Prop. 5.3 ampliada con el argumento general ($N\ge2$, algún $K_{-i}$ no puntual); resumen: "does not determine it". |
| m4/m5/m9 Motzkin, Dubey, Morris–Ui | Teorema 5.1(e): eficiencia débil local ⇒ $\Lambda_1\ne\{0\}$ (Gordan–Motzkin); Remark 5.2 reescrito (alcance de Dubey; Prop. 5.3 como reempaquetado; Morris–Ui 2004). |
| m6 E5b | Desglose por patrón de caras; $\dim\Lambda_1$ por PL (16 bidimensionales, 75 rayos); testigos: 8 instancias con alguna dirección de pesos positivos, 13 sólo en ejes; porcentaje retirado. |
| m7, m8 | Coordenadas reducidas en el Ej. 5.7; observación de separabilidad en la Pregunta 7.1. |
| m10–m12 | Ficha con estado condicional y preguntas actualizadas; `table_pigou.tex` ya no se genera; recuento de macros corregido (177). |
| Bibliografía | `roughgarden2005` citada (Teorema 3.7); Danskin con `number={4}` y DOI; Murty–Kabadi con `number={2}` (de memoria; cotejo pendiente); Bochnak–Coste–Roy con serie "(3)"; añadidas Morris–Ui 2004 y Vavasis 1990 (cotejadas en línea), Karp 1972 y Schrijver 1986 (de conocimiento del autor, no cotejadas en línea). 34 entradas, todas citadas. |

### Resultados de referencia añadidos en v0.3 (semilla 20260930)
- **E2c variante:** frontera bisecada a $1.1\times10^{-8}$ de $\varphi$ en 9 puntos $\lambda_1\in[0.35,0.75]$ ($\varepsilon=0.2$).
- **E5b desglose:** $\Lambda_1$ bidimensional en 16 (ortante en 9), rayo en 75, trivial en 109; 21 instancias con testigo (8 con dirección interior, 13 sólo de eje); 0 de 62 con equilibrio interior; 4 de 27 con $b\equiv0$.
- **E6:** todos los grafos de 3, 4, 5 nodos con pesos unitarios (8, 64, 1024) y 300 + 300 grafos aleatorios de 6 nodos (pesos unitarios; pesos en {1,2,3}); 13 686 pares, 3598 miembros, 10 088 no miembros, 0 discrepancias; cruce vértices/caras en 36 casos, diferencia 0; 85 s.
- **E7:** $y^*=(0,0,1)$, residuo 0; frontera a $1.0\times10^{-8}$ de $\psi$ en 16 puntos de $[0.7,1.45]$; 0 discrepancias en 1878 puntos; brecha del testigo $(1,1,1/20)$ igual a $1/180$.
- **E1, E2–E4, E5a:** idénticos a la v0.2 campo a campo (se comprobó contra una copia de los JSON de la v0.2).
- **Cómputo de la sesión:** ≈ 4 min de CPU (E2–E4 106 s, E6 76 s, E5 8 s, E1 3 s, E7 3 s, verificación de la instancia del árbitro 38 s) más compilaciones.

### Lo que queda abierto tras la ronda 2
1. Pregunta 7.1: ¿es co-NP-difícil decidir $\lambda\in\Lambda(f^*)$ en ruteo multimercancía con costos afines? (La pertenencia a co-NP sí está demostrada.)
2. Extensión: 13 páginas frente a la meta de 10–11; bajar más exige quitar demostraciones.
3. Bibliografía no cotejada en línea en esta ronda: Karp 1972, Schrijver 1986 (datos de conocimiento del autor), `number={2}` de Murty–Kabadi.
4. Pendientes antiguos: E4 con $N=5,6$ y solver global; prerregistro externo inexistente; confirmar con el autor qué era la "formulación revisada".
5. Decisión del autor sobre la ficha propuesta (`FICHA_EQO001_propuesta.md`, estado condicional).


## Ronda 3 de revisión interna y teorema de ruteo (03/10/2026) — v0.4

Informe: `REFEREE_EQO001_ronda3_20261003.md` (cambios menores; 0 bloqueantes, 1 mayor, 13 menores; los tres resultados nuevos de la v0.3 verificados por el árbitro). Respuesta punto por punto, con la verificación independiente del teorema de ruteo: `RESPUESTA_EQO001_ronda3_20261003.md`. Recuento: 12 aceptados, 2 con matiz (m5, m8), 0 rebatidos. Además se integró el resultado de `theory/routing_hardness.tex` (otro agente), después de verificarlo. Numeración del PDF v0.4: igual a la v0.3 hasta 5.10; nuevos Lema 5.11, Teorema 5.12, Obs. 5.13, Cor. 5.14 y Prop. 5.15; Pregunta 7.1 nueva; Apéndice B con las demostraciones de la complejidad.

| Hallazgo | Acción |
|---|---|
| M1 Prop. 5.9 presentada como propia | Reetiquetada como "in substance the standard MAX-CUT encoding of box-constrained QP, transported to games by Prop. 5.3" en el estado, el Remark 5.2, el resumen ("when the number of players is part of the input … a standard reduction"), CLAIMS, ficha y README; `pardalosSchnitger1988` añadida. |
| m1 Enunciado de la 5.9 | $x^*$ racional, cajas, "number of variables (players, or the dimension of their actions) is part of the input", alcance de "unit vector", $N=2$. |
| m2 Prueba de la 5.9 | Complemento de MAX-CUT (sentido "co-"), $\sum_{\{i,j\}\in E}$, necesidad de $w\ge0$. |
| m3 Citas | Murty–Kabadi con la formulación exacta ("not a local minimiser … NP-complete"); Schrijver "Theorem 10.2" en todas las apariciones. |
| m4 E6 | 276 pares por caras ($n\le4$) y 13 410 sólo por vértices, ahora con macros generados (`\HdFacePairs`, `\HdVertexPairs`). |
| m5 Pregunta 7.1 | Sustituida (respondida por el Teorema 5.12). Rutas explícitas: argumento de la 5.9 en flujos de ruta; DAG: flujos de arco por mercancía, como propuso el árbitro. |
| m6 Remark 5.10 | "candidate tractable subclass"; descripción "polynomially many polynomial inequalities of polynomial size"; cuatro líneas; título sin referencias a versiones. |
| m7 | Dos frases tras la 5.9: $F$ independiente de la instancia; dureza y no poliedralidad son independientes. |
| m8 Extensión | §6 condensado, Tabla 1 → `results/tables_welfare.md`, Apéndice A y Ej. 5.5 abreviados, Remark 5.10 a cuatro líneas; Ej. 5.7 comprimido **sin** remitir aristas a E5; demostraciones de 5.9, 5.12 y 5.14 al Apéndice B. Texto principal ≈ 12.4 pp; total 17 pp (el teorema de ruteo añade ≈ 4.5). |
| m9 | Fuera del manuscrito toda referencia a v0.x y a rondas; párrafo de agradecimientos con el crédito. |
| m10 | README (Teorema 3.4; filas de resultados; fila `theory/`); `RESPUESTA…ronda1:79` → Teorema 3.7; línea 36 de esta nota marcada como superada. |
| m11 | `vavasis1990` con `number={2}`; `pardalosSchnitger1988` y `kozlovTarasovKhachiyan1980` añadidas (36 entradas, todas citadas). |
| m12 | Errata del Ej. 5.5 corregida. |
| m13 | Ej. 5.6: $\varphi(\frac{3}{4(1-\varepsilon)})=0$ con pendiente cero (demostrado a mano); Ej. 5.8: frontera lineal fuera de $(\frac23,\frac32)$, marcada "checked numerically, not used". |
| Teorema de ruteo (`theory/`) | Verificado a mano, re-ejecutado (salida idéntica salvo tiempos de CPU) y con un chequeo propio independiente (`scratchpad/eqo_r3/indep_check.py`, 54 pares y 16 DAG). **Hueco reparado:** en el Cor. 5.14 la cota $f_e\le D+1$ en $e^1_m,e^2_m$ es falsa en el DAG (vale $D+2$: flujo del interruptor por rutas de tipo (iii); se alcanza en 84 arcos), pero la conclusión se mantiene porque $D+2\le2(D+1)$; el programa lineal de dominancia en el peor caso da $-449<0$. Precisiones: $\mathbb R^{n+2}_+$ en lugar de $\mathbb R^m_+$; grafo con al menos una arista y sin nodos aislados; cota explícita de $c_{S_i}$ en la Obs. 5.13; sentido "co-" explícito; la Pregunta 7.1 incluye la variante DAG fuertemente monótona. Los archivos de `theory/` no se tocaron. |

### Resultados de referencia añadidos en v0.4
- **E8** (`theory/check_routing_hardness.py`, semilla 20261003; números leídos por `make_numbers.py` de la salida guardada): 130 grafos (todos los etiquetados con ≥ 1 arista en 3 y 4 nodos; 40 + 40 aleatorios en 5 y 6 nodos, la mitad con pesos en {1,2,3}); 381 pares $(G,k)$, 130 miembros y 251 no miembros, 0 discrepancias, margen exacto 1/2; brecha de Frank–Wolfe ≤ $9.6\times10^{-11}$; valores por vértice frente a $h$, $2.7\times10^{-12}$; autovalor mínimo de $DF$ en el espacio tangente ≥ 1; enumeración de caras en 14 pares (hasta 30 861 caras), diferencia $5.7\times10^{-14}$; DAG en 16 pares (hasta 66 rutas de $W$). CPU: 27 s en la corrida guardada; 45.4 s en la re-ejecución (con contención).
- **Chequeo propio** (no publicado en el manuscrito; scratchpad de la sesión, semilla 4242, 135 s de CPU): forma cerrada (eq:CW) frente a $C_W$ arista por arista, $6.2\times10^{-16}$; SLSQP desde 25 arranques sin el lema: ningún punto por debajo del mínimo predicho y 54/54 decisiones correctas; gradiente proyectado converge a $f^*$ en 54/54; Obs. 5.13 en 36/36; DAG: estructura 16/16, dominancia de peor caso por programación lineal $<0$, $\max f_{e^2_m}=D+2$.
- **E1–E7:** sin cambios; ningún número existente de `numbers.tex` cambió (sólo se añadieron 25 macros).

### Bibliografía: notas de certeza (v0.4)
- `pardalosSchnitger1988`: *Oper. Res. Lett.* 7(1), 33–35, 1988, DOI 10.1016/0167-6377(88)90049-1. La cotejó el árbitro de la ronda 3; yo la confirmé con WebSearch (un primer resultado resumido daba "33–45", que atribuyo a un error del resumen; la búsqueda dirigida da 33–35 y el DOI).
- `kozlovTarasovKhachiyan1980`: el título de la ficha de Math-Net.Ru (vista con WebSearch) da "Zh. Vychisl. Mat. Mat. Fiz., 20:5 (1980), 1319–1323; U.S.S.R. Comput. Math. Math. Phys., 20:5 (1980), 223–228", lo que coincide con la entrada; añadí el original ruso como `note`. ScienceDirect, Crossref y arXiv están bloqueados por el proxy, así que **no pude abrir la página de la editorial** y el DOI no se incluye.
- `schrijver1986`, "Theorem 10.2" (complejidad de vértices ≤ $4n^2\varphi$): número del teorema de memoria del autor y del árbitro; **no verificable desde la sesión**.
- `vavasis1990`: `number={2}` según el árbitro (verificado por él).

### Lo que queda abierto tras la ronda 3
1. **Pregunta 7.1 (v0.4):** (i) complejidad de $\lambda\in\Lambda(f^*)$ en ruteo con un número fijo de mercancías (ya dos) y pesos positivos distintos; (ii) si el Cor. 5.14 (DAG con todas las rutas) vale con $F$ fuertemente monótono. La construcción actual no lo es: una ruta del interruptor por $q_0$, $dz$ y el último tramo de $T_M$, combinada con un movimiento de $W$ de $T_M$ a $O$, da una dirección tangente con $h^\top DFh=0$.
2. Extensión: 17 páginas en total (texto principal ≈ 12.4). Bajar a 13 exigiría quitar demostraciones o reducir la letra; queda a decisión del autor.
3. Ej. 5.8: la frontera lineal fuera de $(\frac23,\frac32)$ está sólo comprobada numéricamente (rama convexa $(\frac14,\frac23]$ demostrable por KKT; caso indefinido no escrito).
4. Bibliografía: Schrijver Teorema 10.2 y la página editorial de KTK no verificables desde la sesión.
5. Pendientes antiguos: E4 con $N=5,6$ y un solver global; prerregistro externo inexistente; confirmar con el autor qué era la "formulación revisada"; decisión del autor sobre la ficha propuesta (estado condicional, ahora v0.4).
6. Una cuarta ronda de arbitraje debería centrarse en el Apéndice B (Teorema 5.12 y Cor. 5.14), que sólo verificó su autor y el autor de esta respuesta.
