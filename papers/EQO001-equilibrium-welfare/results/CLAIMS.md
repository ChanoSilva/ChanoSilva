# EQO001 — Afirmaciones y su estado (v0.4, 03/10/2026)

Tabla movida desde el manuscrito (Tabla 2 de la v0.2) por recorte de extensión (ronda 2, M4). Los números citados están en `results/tables_*.md` y en `manuscript/numbers.tex`, generados por los scripts; aquí sólo se registra el estado de cada afirmación. Numeración del PDF v0.4 (idéntica a la v0.3 hasta el Remark 5.10; la v0.4 añade 5.11–5.15 y reemplaza la Pregunta 7.1).

| Afirmación | Estado |
|---|---|
| Campo $C^1$ con jacobiano simétrico en un abierto convexo es un gradiente (Poincaré; párrafo antes del Teorema 3.1). | clásico; prueba de una línea en el texto |
| Soluciones de la VI de un campo gradiente = puntos estacionarios del potencial; minimizadores si es convexo (Teorema 3.1). | clásico (Beckmann–McGuire–Winsten 1956, Monderer–Shapley 1996); demostrado |
| Equilibrios de Nash y de Wardrop son soluciones de la VI (Lemas 2.4, 2.7). | clásico; demostrado |
| Monotonía estricta: unicidad; fuerte + Lipschitz: existencia y convergencia lineal (Teorema 3.4). | clásico (Kinderlehrer–Stampacchia, Facchinei–Pang); demostrado |
| Pigou: PoA $=4/3$ para $d=1$, no acotado en $d$ (Ej. 3.6); PoA $\le 4/3$ con costos afines (Teorema 3.7). | clásico (Roughgarden–Tardos 2002; Roughgarden 2005); demostrado; verificado (E1) |
| Equilibrio maximizador de $W$ sólo si $\nabla W(x^*), -F(x^*) \in N_K(x^*)$; sii si $W$ cóncava (Prop. 4.1). | demostrado; elemental |
| Peajes de costo marginal; conjunto de peajes $=-F(\bar x)-N_K(\bar x)$ (Cor. 4.2). | clásico (Pigou, Knight, BMW, Hearn–Ramana; optimización inversa); demostrado; solver contra water-filling (E1; el antiguo E1c se fusionó en E1b) |
| $\Lambda(x^*)$ cono convexo cerrado, $\Lambda\subseteq\Lambda_1$, igualdad con concavidad conjunta, forma por bloques, vínculo con Pareto; eficiencia débil local ⇒ $\Lambda_1\ne\{0\}$ sin concavidad (Teorema 5.1). | demostrado; (a),(e) escalarización estándar; la última implicación es la alternativa de Gordan–Motzkin |
| $(F,K)$ no determina $\Lambda(x^*)$: compatible con el ortante siempre, y con $e_i\notin\Lambda$ si $N\ge2$ y algún $K_{-i}$ no es un punto (Prop. 5.3). | demostrado; reempaquetado de Nikaidô–Isoda; equivalencia de mejor respuesta (Morris–Ui 2004); Danskin para el caso $C^1$ |
| Cono exacto en cuña (Ej. 5.4). | demostrado; verificado (E2) |
| $\Lambda(x^*)$ no poliédrico en general, también con $F$ fuertemente monótono (Ej. 5.6, forma cerrada $\varphi$). | demostrado (contraejemplo y forma cerrada señalados en las revisiones internas 1 y 2); verificado (E2c) |
| $\Lambda\ne\Lambda_1$ con dos mercancías y costos afines (Ej. 5.7). | demostrado; verificado (E5) |
| $\Lambda(y^*)$ no poliédrico con tres mercancías y costos afines; descripción exacta $\{\lambda_3+m\ge0\}$ (Ej. 5.8). | demostrado; verificado (E7) |
| Decidir $\lambda\in\Lambda(x^*)$ y decidir $\Lambda=\Lambda_1$ en juegos cuadráticos en cajas es co-NP-completo **cuando el número de variables (jugadores o dimensión de las acciones) forma parte de la entrada**, incluso con $F$ fuertemente monótono e independiente de la instancia, $x^*$ vértice en estrategias estrictamente dominantes, $\lambda$ unitario, y también con $N=2$ (Prop. 5.9). Con $N$ fijo y acciones escalares es polinómico ($3^N$ caras). | demostrado; **en sustancia, reducción estándar MAX-CUT ↔ QP en caja (Murty–Kabadi 1987; Pardalos–Schnitger 1988; pertenencia por Vavasis 1990), inmersa en un juego vía la Prop. 5.3**; comprobado por fuerza bruta (E6: 276 pares por enumeración de caras, 13 410 sólo por vértices) |
| Lema 5.11: las mercancías de peso cero entran afínmente en $\Phi_\lambda$; el mínimo se alcanza con ellas en rutas puras. | demostrado; elemental |
| **Teorema 5.12:** en ruteo de Wardrop multimercancía con costos afines y conjuntos de rutas explícitos, decidir $\lambda\in\Lambda(f^*)$ y decidir $\Lambda(f^*)=\Lambda_1(f^*)$ es co-NP-completo cuando el número de mercancías forma parte de la entrada; difícil aun con $\lambda$ unitario, $f^*$ único equilibrio y vértice, $F$ fuertemente monótono, $\Lambda_1$ = ortante, aristas compartidas por ≤ 2 mercancías y todas las mercancías salvo una con 2 rutas. | demostrado aquí (Apéndice B; reducción desde el complemento de MAX-CUT; verificado de forma independiente por el autor en la ronda 3); comprobado numéricamente (E8: 381 pares, 0 discrepancias; chequeo propio independiente en 54 pares) |
| Observación 5.13: la dureza vale también para $\lambda$ en el interior del ortante. | demostrado aquí; comprobado (E8) |
| Corolario 5.14: lo mismo (sin fuerte monotonía) en un DAG con todas las rutas origen–destino. | demostrado aquí (Apéndice B; en la v0.4 se corrigió una cota, $f_e\le D+2$ en los arcos $e^1_m,e^2_m$, sin cambio de conclusión); comprobado en grafos pequeños (E8) |
| Prop. 5.15: casos tratables: $\lambda$ constante por arista con $a_e>0$ (incluye $\lambda=\mathbf 1$), test lineal; $\lambda=\mu\mathbf 1_Q$ con pocas mercancías de peso cero que compartan aristas con $Q$, polinómico (Kozlov–Tarasov–Khachiyan 1980). | demostrado; elemental + literatura |
| $\Lambda=\Lambda_1$ en juegos cóncavos aleatorios. | teorema; verificado en toda dirección probada (E3) |
| $\Lambda\subsetneq\Lambda_1$ ocurre sin concavidad conjunta. | testigos certificados (E4); la frecuencia es una cota inferior y sólo descriptiva |
| Concepto de equilibrio nuevo o solución general de equilibrio. | no se afirma |
| Pregunta 7.1 de la v0.3 (complejidad de la pertenencia en ruteo multimercancía). | **respondida**: co-NP-completa (Teorema 5.12, Corolario 5.14) |
| Pregunta 7.1 de la v0.4: (i) número fijo de mercancías (ya dos) con pesos positivos distintos; (ii) DAG con todas las rutas y $F$ fuertemente monótono. | abierta |
