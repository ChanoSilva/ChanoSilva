# Respuesta del autor al informe de árbitro interno — SPD001, ronda 2 (03/10/2026)

Objeto: `REFEREE_SPD001_ronda2_20261003.md` (0 bloqueantes, 3 mayores, 11 menores, 15 acciones; verificación de la ronda 1 con 2 puntos "a medias" y 1 "aplicado con error nuevo"). Este archivo se escribe de forma incremental mientras se aplican los cambios; la sección "Estado" al final dice qué está hecho y qué queda abierto.

Convención: **aceptado** = se aplicó tal como lo propone el árbitro (o el coordinador); **aceptado con matiz** = se aplicó una versión y se explica la diferencia; **rebatido** = no se aplica, con la demostración o el cálculo.

Indicación del coordinador que modifica la propuesta del árbitro en M1: en lugar de una "sensibilidad declarada" que deje intacta la corrida de referencia, se escribe primero un prerregistro fechado (`PREREGISTRO_SPD001_ronda2.md`) con rejillas ampliadas para *todos* los métodos y ablaciones, y se vuelve a correr la corrida completa (E1 y E2) con ellas; la corrida v0.2 se conserva en `results/v02/` para comparar. El texto, el resumen, la tabla de afirmaciones, README y FICHA se reescriben según lo que salga.

## Estado

- 03/10/2026, paso 0: leídos el informe, el brief, todo el material de la carpeta y la respuesta de la ronda 1. Corrida v0.2 archivada en `results/v02/` (JSON, tablas, registro, `support_geometry_v02.py`, `make_numbers_v02.py`, `main.tex`/`numbers.tex`/tablas y `main_v02.pdf`, 10 páginas). Saturación v0.2 por método tabulada (scratchpad `spd001_r2/sat_v02.py`): además de lo que señala el árbitro, `m = 8` (máximo de la rejilla de dimensión tangente) se elige en 13–16 de 25 pliegues en digits (TOD, TO, OD, LPH) y en 14/25 en wine (TOD); `k_NN = 41` en 20/25 en E2 p = 20; `λ_rel = 100` en 16/25 en E2 p = 20.
