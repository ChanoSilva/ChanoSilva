# Prerregistro SPD001 — protocolo v0.3 (ronda 2 de revisión interna)

**Fecha:** 3 de octubre de 2026, escrito **antes** de lanzar la corrida completa v0.3. La corrida guarda en `results/results.json` (`meta.preregistration_sha256`) el SHA-256 de este archivo tal como estaba al lanzarla; cualquier cambio posterior lo invalida y debe declararse.

**Qué no es.** No es un prerregistro ciego: al escribirlo se conocían la corrida v0.2 (archivada en `results/v02/`) y la sensibilidad del árbitro de la ronda 2 en moons y moons+ruido (TOD − TD en moons+ruido: +2.67 con k ≤ 30, +0.50 con k ≤ 50, −0.27 con k ≤ 75). Su función es fijar rejillas, reglas de decisión y lo que se informará *antes* de ver los resultados v0.3, de modo que el texto se reescriba según lo que salga y no al revés.

## 1. Lo que no cambia respecto de v0.2

- Semilla maestra 20260930; los mismos 8 conjuntos de E1 (iris, wine, breast cancer, digits submuestreado a 100 por clase, swiss roll, moons, moons + 10 coordenadas de ruido, esferas) y los 5 niveles de E2 (moons con p ∈ {0, 2, 5, 10, 20} coordenadas de ruido), generados igual.
- Validación cruzada estratificada repetida 5×5 con `random_state = 20260930` (mismos pliegues para todos los métodos y los mismos que en v0.2); estandarización con estadísticas del pliegue de entrenamiento.
- Métodos: referencias kNN, NFL, HKNN, LPH, LCD, SD; propuesta TOD; ablaciones TO, TD, OD; componente única T. Definiciones de puntuaciones, del logit condicional (penalización 10⁻³, piso 10⁻⁶) y de la confianza para la exactitud selectiva al 80 %.
- Selección de hiperparámetros por exactitud leave-one-out en el pliegue de entrenamiento (resustitución del logit sobre rasgos leave-one-out para los modelos logit), empates al primer punto de la rejilla.
- Criterio primario **C1**: TOD "aporta información" si y solo si supera a la mejor referencia con IC bootstrap percentil 95 % (10 000 remuestreos de los 25 pliegues) estrictamente por encima de 0 en al menos 5 de 8 conjuntos. C2 (ablaciones), C3 (exactitud selectiva) y E2 con la misma regla. Cada recuento se informa también con el IC de Nadeau–Bengio (inflación 1/25 + 1/4).

## 2. Rejillas v0.3 (para todos los métodos y ablaciones)

Sea `k_cap = min_c (n_c − ⌈n_c/5⌉) − 1` el mayor tamaño de vecindad de clase admisible en todo pliegue de entrenamiento con rasgos leave-one-out (toda la clase menos el punto).

| Hiperparámetro | v0.2 | v0.3 |
|---|---|---|
| tamaño de vecindad de clase `k` (NFL, HKNN, LPH, LCD, SD, T, TOD, TO, TD, OD) | {5, 10, 20, 30} | {5, 10, 20, 30, 50, 75} ∩ [5, k_cap], más `k_cap` si `k_cap < 75`; en digits, tope de coste `k ≤ 50` |
| `k_NN` (kNN) | {1, …, 31, 41} | {1, 3, 5, 7, 9, 11, 15, 21, 31, 41, 61, 81, 121}, con `k_NN ≤ n_train − 1` |
| `λ_rel` (HKNN) | {0, 0.1, 1, 10, 100} | {0, 0.1, 1, 10, 100, 1000, 10 000} |
| dimensión tangente `m` (LPH, T, modelos logit) | {1, 2, 3, 5, 8} | {1, 2, 3, 5, 8, 13, 21}, con `m ≤ min(k − 1, d − 1)` |

Rejillas de `k` resultantes: iris {5, 10, 20, 30, 39}; wine {5, 10, 20, 30, 37}; digits {5, 10, 20, 30, 50} (k_cap = 79, tope de coste 50: con d = 64 la descomposición espectral de las vecindades domina el tiempo de CPU, y k = 75 llevaría la corrida por encima del presupuesto de 10 min); breast cancer, swiss roll, moons, moons+ruido, esferas y todos los niveles de E2 {5, 10, 20, 30, 50, 75}. `k_NN ≤ 81` en iris, `≤ 121` en el resto.

Fronteras naturales (elegir el extremo no es truncamiento): `k = k_cap` (toda la clase), `λ_rel = 10 000` (pesos λ/(s_j² + λ) ≈ 1: distancia al centroide local), `m = min(k − 1, d − 1)` (subespacio tangente completo). Son truncamiento: `k = 75`, el tope de coste `k = 50` en digits, `k_NN` = máximo de su rejilla y `m = 21` cuando `21 < min(k − 1, d − 1)`.

## 3. Cambios de implementación (no de definición)

- **Regla de empate de la mejor referencia.** La mejor referencia se decide con aritmética racional exacta sobre los conteos enteros de aciertos por pliegue (media de `aciertos_j / n_test_j`), no con medias en coma flotante. Ante empate exacto se conservan todas las referencias empatadas: una victoria significativa exige IC > 0 frente a **cada** empatada y una pérdida significativa IC < 0 frente a **cada** empatada (en las dos lecturas); en las tablas se muestra la empatada con el límite superior bootstrap más alto (la menos favorable a una pérdida y la más conservadora para la cota de ganancia), y se nombran todas. Misma regla para la mejor referencia por exactitud selectiva.
- **Bootstrap común.** Una sola matriz de índices de remuestreo (10 000 × 25), sembrada con la semilla maestra, para todas las comparaciones: un mismo par de métodos tiene un único IC.
- **E2:** las filas p = 0 y p = 10 son exactamente moons y moons+ruido de E1 (mismos datos y pliegues); se copian, no se recalculan, y se cuentan una sola vez al contar intervalos (11 intervalos de profundidad distintos en E1 + E2).
- **Rango numérico.** Las direcciones con valor singular al cuadrado < 10⁻¹⁰·s₁² se tratan como nulas; la distancia al casco es entonces la distancia exacta a la envolvente afín también para vecindades no genéricas (p. ej. píxeles constantes en digits). Para vecindades genéricas no cambia nada.
- **Cómputo.** Descomposición espectral de la matriz de Gram menor en lugar de la SVD; NFL, profundidad y distancia media calculadas una vez al k máximo y recortadas (mínimos prefijos, sumas acumuladas); geometría del pliegue de prueba solo en los k elegidos. Validado antes de esta corrida: con las rejillas v0.2, el código v0.3 reproduce pliegue a pliegue las 11 exactitudes y los hiperparámetros elegidos de v0.2 en moons; las puntuaciones coinciden con el código v0.2 a < 10⁻⁸ en datos aleatorios genéricos.

## 4. Qué se informará (fijado ahora)

1. C1, C2, C3 y E2 con la regla de §1 y la regla de empate de §3, en ambas lecturas (bootstrap / NB), aunque contradigan la v0.2.
2. **Saturación residual por método:** para cada conjunto y cada método, porcentaje de pliegues con `k` en el máximo de su rejilla, y para kNN, HKNN (`λ_rel`) y los métodos con `m` el porcentaje en el máximo; distinguiendo frontera natural y truncamiento (§2). Tabla completa en `results/tables_appendix.md`.
3. **Regla de robustez de la atribución C2 (fijada ahora):** un efecto de ablación (TOD − modelo reducido) se usa como apoyo de la atribución solo si (i) su IC bootstrap v0.3 excluye 0 y (ii) ni TOD ni el modelo reducido eligen un `k` de truncamiento en más del 50 % de los pliegues de ese conjunto. Los efectos que no cumplen (ii) se declaran "dependientes de la rejilla"; los que cambian de signo o pierden la significación respecto de v0.2 se nombran.
4. Comparación v0.2 → v0.3 por conjunto (TOD − mejor referencia, TOD − TD, TOD − TO, TOD − OD) en `results/tables_appendix.md`, con los IC v0.2 recalculados con el mismo bootstrap común para que la comparación sea homogénea.
5. Observación 3.2: número de conjuntos con `d < min(k_grid)` y, para HKNN, porcentaje de pliegues cuyo `k` elegido supera `d` (sin término de casco cuando la vecindad es genérica).
6. Lectura complementaria entre conjuntos (Demšar 2006): test de rangos con signo de Wilcoxon y test de signos sobre las 8 diferencias TOD − mejor referencia; no sustituye a C1.

## 5. Presupuesto

Estimado con un pliegue por conjunto (sin mirar exactitudes): ≈ 6–7 min de CPU con BLAS de un hilo para E1 + E2 (digits ≈ 7 s por pliegue). Si la corrida no terminara dentro del presupuesto, se informaría la corrida rápida y se diría.
