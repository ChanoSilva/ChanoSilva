# EQO001 — Afirmaciones y su estado (v0.3, 03/10/2026)

Tabla movida desde el manuscrito (Tabla 2 de la v0.2) por recorte de extensión (ronda 2, M4). Los números citados están en `results/tables_*.md` y en `manuscript/numbers.tex`, generados por los scripts; aquí sólo se registra el estado de cada afirmación. Numeración del PDF v0.3.

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
| Decidir $\lambda\in\Lambda(x^*)$ y decidir $\Lambda=\Lambda_1$ es co-NP-completo, incluso con $F$ fuertemente monótono, $x^*$ vértice, $\lambda$ unitario (Prop. 5.9). | demostrado (reducción señalada en la revisión interna 2); comprobado por fuerza bruta (E6) |
| $\Lambda=\Lambda_1$ en juegos cóncavos aleatorios. | teorema; verificado en toda dirección probada (E3) |
| $\Lambda\subsetneq\Lambda_1$ ocurre sin concavidad conjunta. | testigos certificados (E4); la frecuencia es una cota inferior y sólo descriptiva |
| Concepto de equilibrio nuevo o solución general de equilibrio. | no se afirma |
| Pregunta 7.1 (complejidad de la pertenencia en ruteo multimercancía). | abierta |
