[EN CURSO]

# Informe de árbitro interno independiente — SGE001, ronda 3 (03/10/2026)

Versión arbitrada: v0.4 (commit c45dddf). Árbitro nuevo, independiente de las rondas 1 y 2.

(Informe en construcción; las secciones se completan de forma incremental.)

## Notas de trabajo (se reordenan al final)

- Prop. 3.3 (a)-(d) y Lema 3.4: revisados paso a paso; sin error matemático en lo que el enunciado afirma (detalle más abajo).
- Chequeo independiente (scratchpad referee3_SGE001/verify_A.py, verify_B.py, verify_C.py; derivadas con sympy, generadores reimplementados desde la semilla, ninguna función del autor importada):
  - A1: E3 = Y - Yhat3 frente al resto integral por Gauss-Legendre (24 nodos): diferencia relativa <= 7e-11 (sigma >= 0.1), CD y CES, LN y SU.
  - A2: forma cerrada del Lema 3.4 frente a sympy: 4.6e-16.
  - A3: regla de esquinas: 0 violaciones en 9600 pruebas (caja, multiíndice) con 0<a<1, incluidas esquinas inferiores hasta 1e-8 y cajas de 4 décadas; fuera de la hipótesis (a_1 = 1.5, 2, 2.5, 3) falla en 400-700 de 1400; con a_1 = 1 no falla (exponente 0 o factorial nulo).
  - A4: sup_caja ||D^4 f||_S / cota de Frobenius en [0.708, 0.99999999927] (<= 1).
  - B: E1, CD, las 20 réplicas, 17+15 celdas: TODOS los sigma certificados (8 variantes x k in {1,5} x 2 leyes) coinciden con las macros; max|E2|/(|C3|+B3) = 0.1752 (LN, caja euclídea) y 0.054 (SU); todas las cotas valen.
  - C: E4 sin capacidad, 1000 ensayos: todas las fracciones certificadas coinciden (83.0/11.5/95.7/71.6; 90.0/56.7; 1.2 frente a 3.4); 0 inversiones certificadas. Con min(B2,|C3|+B3) a sigma=0.4 (escalado, micro): 4.2 %.
  - CES (rejilla 33x33, estimación inferior del supremo): sigma* k=1 LN caja 0.042 (3.er orden) y 0.100 (4.º) frente a 0.024 y 0.032 del texto: el certificado CES está limitado por la holgura del encierro, no por el orden.
