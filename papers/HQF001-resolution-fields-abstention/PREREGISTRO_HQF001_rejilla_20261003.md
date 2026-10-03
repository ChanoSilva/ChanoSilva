# HQF001 — Preregistro de la corrida v0.3 con rejilla ampliada del campo

**Escrito:** 03/10/2026, 10:03 UTC, **antes** de lanzar la corrida v0.3 (el log `results/run_log_v03.txt` registra la hora de inicio).
**Motivo:** hallazgo R2-M4 del árbitro de la ronda 2: los hiperparámetros del campo se seleccionan en el borde superior de la rejilla v0.2 (α = 0.5 y K_m = 80 en 15/15 pliegues de synth-informative, synth-classcov y synth-lda; ≥ 14/15 pliegues en un borde superior en 6 de 8 datasets).

## Qué se sabía al escribir esto (declaración)

- Los resultados v0.1 y v0.2 completos (`results/results_v01.json`, `results/v02/results.json`).
- El análisis de sensibilidad del árbitro con **esta misma rejilla**, solo para Field-aniso y en 6 datasets (synth-classcov, synth-lda, synth-informative, breast-cancer, moons-aniso, wine): el campo baja de 2.77 a 2.07 (synth-classcov) y de 2.83 a 2.24 (synth-lda) en AURC×100, sigue peor que la mejor referencia en los seis, y la selección queda en el borde nuevo (α = 0.9 en synth-classcov, K_m = 320 en synth-lda). No se habían visto resultados con esta rejilla para iris, digits, las ablaciones ni las puntuaciones geométricas.

La rejilla es la del árbitro, adoptada tal cual (no se eligió a la vista de resultados propios); esto permite además comprobar que la corrida reproduce sus números en los seis datasets.

## Qué se corre

- `python3 experiments/selective_benchmark.py` (script v0.3), corrida **completa**: 8 datasets, 3×5 pliegues estratificados, CV interna de 3 pliegues sobre AURC, semilla 20260930, los 13 métodos. Las referencias, sus rejillas, los pliegues, las semillas internas, B = 20 000, los tres intervalos y el criterio **no cambian** (las referencias deben reproducir v0.2 bit a bit).
- **Único cambio de protocolo:** la rejilla de las seis variantes del campo pasa de K_m ∈ {20, 40, 80}, α ∈ {0.05, 0.2, 0.5} a **K_m ∈ {20, 40, 80, 160, 320}, α ∈ {0.05, 0.2, 0.5, 0.7, 0.9}** (las ablaciones isótropa y euclidiana reciben la misma lista de K_m; α = 1 queda reservado a la ablación isótropa, de modo que aniso − iso sigue comparando "métrica anisótropa" con "escala local").
- **Regla de empate para K_m recortado** (decidida aquí, antes de correr): los valores nominales que el tope min(K_m, n_train − 1) hace idénticos se ordenan de mayor a menor, de modo que, entre configuraciones internas idénticas, se conserva el K_m nominal mayor. Efecto: en iris (80 puntos internos de entrenamiento), "todos los puntos internos" se traduce a "todos los puntos externos" (K_m = 320 → 119 de 120) en lugar de "80 de 120". Con la rejilla v0.2 la regla no cambia nada (no hay grupos de más de un valor nominal).
- Se almacena y se tabula la **saturación**: número de pliegues cuyo valor seleccionado está en el extremo inferior o superior de su rejilla, para el campo y para las referencias con rejillas numéricas de al menos 3 valores.

## Análisis y reglas de decisión (fijadas antes de correr)

1. El criterio predefinido (texto en `CRITERIO_HQF001.md`, sin cambios) se evalúa sobre la corrida v0.3 con las tres lecturas (bootstrap, el predefinido; t; Nadeau–Bengio).
2. **Se afirmaría una ganancia residual solo si el criterio se cumpliera tanto en la corrida v0.2 (rejilla predefinida) como en la v0.3.** Si los veredictos difirieran, se informaría la discrepancia como dependiente de la rejilla.
3. Las tablas del manuscrito v0.3 salen de la corrida v0.3 (el campo recibe la rejilla más amplia, que es la comparación más favorable para él). La corrida v0.2 se conserva en `results/v02/` y sus recuentos del criterio y de la ablación aniso − iso se informan junto a los v0.3 mediante macros.
4. Los recuentos de la ablación aniso − iso se informan con las tres lecturas y aplicando la regla de casos límite (un par marcado ° no cuenta como "mejor" ni "peor" en el recuento robusto).
5. Cualquier afirmación cuyo sentido cambie entre v0.2 y v0.3 se declara dependiente de la rejilla.
6. La saturación residual con la rejilla v0.3 se informa tal cual; en esta versión no se amplía más la rejilla.

## Script

`sha256(experiments/selective_benchmark.py) = 35aefc57f5343e3f11bbb183882f22712151dd3c46670cb851c139a1d1cf3a80` (v0.3, 03/10/2026 10:03 UTC). Cómputo previsto: ≈ 6 min de CPU, un hilo.
