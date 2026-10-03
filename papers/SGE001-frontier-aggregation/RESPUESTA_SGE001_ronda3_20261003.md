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
- [hecho] `experiments/e4_min_bound.py` (nuevo; m4): regenera los sorteos de E4 sin capacidad (generador 'E4', mismo bucle que `run_E4`), importa en sólo lectura las funciones de cota de `theory/check_sharp_certificate.py` tras comprobar su SHA-256 congelado (no ejecuta su `main()`, no escribe nada en `theory/`) y calcula la fracción certificada con $\min(B_2,|C_3|+B_3)$ en las cuatro formas (segmento/caja × euclídea/escalada). Comprueba por `assert` que las fracciones con una sola cota coinciden exactamente con el JSON de teoría congelado y con `results/results.json`, y que hay 0 reversiones certificadas. Resultado (microdatos, escalada): **95.7 % en σ = 0.2 y 4.2 % en σ = 0.4** (frente a 1.2 % y 3.4 % con cada cota por separado): coincide con el árbitro. 12.6 s de CPU.
- [hecho] `experiments/ces_grid_estimate.py` (nuevo; m6): estimación **no rigurosa** (máximo de cada entrada de $D^kf$ en una rejilla geométrica 33×33 de la caja) de hasta dónde llegarían los certificados CES de momentos y rango si se conocieran los supremos: LN, $k=1$: tercer orden 0.042, cuarto orden 0.100 (euclídea y escalada), frente a 0.024 / 0.032 / 0.056 con los encierros; comprueba por `assert` que la estimación nunca certifica menos que los encierros. Coincide con el árbitro (0.042 y 0.100). 7.4 s de CPU.
- [hecho] Ambos scripts escriben JSON deterministas (sin campo de tiempo; re-ejecutados: SHA-256 idénticos) y quedan congelados en `results/round3_checks.sha256` (JSON y scripts). `make_numbers.py` comprueba esos SHA-256 y se detiene si no coinciden; genera 23 macros nuevas (`\MinEfour*`, `\CesGrid*`); **las 425 macros de v0.4 conservan su valor** (comparación por programa con la copia de v0.4) y los cuatro cuerpos de tabla son idénticos byte a byte. `results/results.json` y `theory/` no se tocaron.
- [hecho] Manuscrito, primera pasada: resumen (≈ 450 → 249 palabras, contando cada fórmula como una palabra), fecha/versión v0.5, $\|\cdot\|_S$ para formas $k$-lineales en §2, Prop. 3.3 con $M_{k,S}$, $m_k^S$ y $B_2^S$ en (b), $\mu_4^S$ eliminado, Lema 3.4 con $a_m>0$ y regla por el signo del exponente, Obs. 3.2 "closed-form upper bounds", Obs. 3.5 recortada y precisada, párrafo de E1 del cuarto orden recortado (con $B_2^S$ y paso de la rejilla SU), frase de E4 con el mínimo, fila de la tabla de afirmaciones y pie, párrafo de cierre de §5 suprimido.
