[EN CURSO]

# Informe de arbitraje interno independiente — MRT001, ronda 4 (verificación de teoremas nuevos)

Fecha: 03/10/2026. Objeto: borrador v0.6 (`manuscript/main.tex`, commit de integración `fe6d0df`/`5d58fb5`), en particular la Sección 5 nueva ("The realizer law": Teorema 5.3 de Gallai, Lemas 5.4 y 5.5, Teorema 5.6, Proposición 5.7), el Apéndice B (pruebas y Observación B.1) y la tabla E5f. Árbitro nuevo, independiente de los anteriores.

## Veredicto

(pendiente)

## Notas de trabajo (se reorganizan al final)

- Lema 5.4 (intervalos ⇔ módulos): prueba leída paso a paso; correcta.
- Lema 5.5 (inflación de simple): prueba leída paso a paso (conjunto S, módulo B∪S, cociente primo sin vértice universal ni aislado); correcta.
- Teorema 5.6(a): constantes verificadas término a término (ver sección "Verificación de las constantes").
- SHA-256 de `results/check_realizer_law_output.txt` coincide con `results/check_realizer_law_output.sha256` (4e011b1e…dc84). La copia `theory/check_realizer_law_output.txt` difiere solo en tiempos.
- Fuerza bruta propia (`scratchpad/referee3_MRT001/bf.py`, run1–run4): R(π) contado desde pares de extensiones lineales para las 5913 permutaciones n ≤ 7 (cuadrático completo n ≤ 6; pareja forzada n = 7), muestras n = 8 (3000) y n = 9 (1500): 0 discrepancias con la fórmula de B.1 (implementación propia); P(R ≠ 2^N) exacta = 1/2, 3/6, 10/24, 53/120, 365/720, 2753/5040 (n = 2..7), 22069/40320 (n = 8), 190555/362880 (n = 9) — coincide con la salida congelada para n ≤ 8.
- Gallai numérico: 3318 permutaciones simples de longitud 4..8 con R = 1 (pares de extensiones lineales).
- Momentos factoriales 1 − r/n exactos para n = 8, 9 (enumeración); d_TV(N_n, Po(1)) exacta = e^{-1}/n a 4 cifras (n = 8..150), cota = 20× mayor.
- Constantes de 5.6(a): todas las cotas término a término valen para n ≥ 20 (fallan para n ≤ 18 las de E I_{n-2}, E I_{n-3}, E I_{n-4}); Σ E I_k / (10/n+166/n²) = 0.704 en n = 20, 0.9957 en n = 3000 (→ 1).
- Prop. 5.7: en n = 8 exhaustivo y en muestras n = 20/40/100 todas las permutaciones con un único intervalo de tamaño 3..n−1 tienen la razón predicha; tasa n·P = 4.96±0.06 (n = 20), 4.79±0.13 (40), 4.58±0.33 (100). Pero en n = 20 la mitad de las excepciones (2373/4964) caen en el evento "O(n^-2)" (≥ 2 intervalos): constante ≈ 50/n².
- Obs. B.1: contraejemplo a la enumeración literal de fuentes de razones ≠ 3/2, 2: bloque interior 563412 (= 12⊖12⊖12, sin intervalos de 3) da razón 6 sin raíz suma sesgada ni casos de 5.7.
