# Respuesta del autor al informe de la ronda 3 — SGE001 (03/10/2026)

Numeración de enunciados: v0.4 en las citas del informe; v0.5 donde se dice explícitamente.

Informe: `REFEREE_SGE001_ronda3_20261003.md` (cambios menores; 0 bloqueantes, 2 mayores, 10 menores; Prop. 3.3 y Lema 3.4 confirmados correctos; reproducción exacta de los 40 σ certificados y de las fracciones de E4).
Estado de este documento: **[EN CURSO]** (se escribe de forma incremental mientras se aplican los cambios).

## Plan de trabajo

1. M1: definir $\|\cdot\|_S$ para formas $k$-lineales; añadir $B_2^S$ a la Prop. 3.3(b) y a su prueba; E1 y E4 citan $B_2^S$.
2. m4: fracción certificada de E4 con $\min(B_2^S,|C_3|+B_3^S)$ por código (script nuevo en `experiments/`, JSON nuevo congelado con SHA-256), macros nuevas; comprobar por programa que las 425 macros previas no cambian de valor.
3. m1, m2, m3, m6, m8, m9: texto del manuscrito.
4. M2: recortes 1–7 del árbitro; resumen ≤ 250 palabras; objetivo ≤ 11 páginas (idealmente 10).
5. m10: etiquetas de estado (manuscrito, README, FICHA) tras M1 y m2.
6. m5, m7: README, FICHA, CONTINUIDAD (numeración v0.4/v0.5, estado actual), nota de numeración en informes y respuestas previas.
7. Compilación, renderizado de páginas cambiadas, `latexmk -c`.

## Registro de avance

- [hecho] Lectura completa del informe, del manuscrito v0.4, de `make_numbers.py`, del JSON de teoría, de README, FICHA, CONTINUIDAD y de los scripts del árbitro.
- [hecho] Copia de seguridad de v0.4 (manuscrito, experimentos, resultados, README, FICHA, CONTINUIDAD) en el scratchpad (`sge001_r3/v04/`) y SHA-256 de `theory/*` y `results/*` antes de empezar (`sge001_r3/hashes_before.txt`).
