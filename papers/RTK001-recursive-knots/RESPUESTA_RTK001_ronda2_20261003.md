# Respuesta del autor a la ronda 2 de revisión interna — RTK001 (03/10/2026)

Informe atendido: `REFEREE_RTK001_ronda2_20261003.md` (cambios menores; 0 bloqueantes, 4 mayores, 13 menores; ronda 1: 23 bien, 2 con error nuevo: B2, M2).
Además, en esta pasada se integra el trabajo de `theory/` sobre el caso "misma hebra" (`theory/same_strand_lemma.tex`, `same_strand_derivation.md`, `check_same_strand.py` y su salida), terminado por el agente teórico durante la ronda 2.

Documento escrito de forma incremental (estado de trabajo al final de cada sección).

## 0. Plan y estado de trabajo

- [ ] Verificación propia del bloque "misma hebra" de `theory/` (lectura de la prueba + corrida de `check_same_strand.py` + cómputo independiente de la clasificación de pares doblemente críticos).
- [ ] M4: congelar los resúmenes de `theory/` en `results/` (con SHA-256) y que `make_numbers.py` lea solo la copia.
- [ ] B2/m3: tolerancia única en `make_numbers.py`.
- [ ] M1: etiquetas de estado (resumen, Lema 3.7, Teorema 3.10, Hip. 3.12, tabla, Limitaciones, README, CONTINUIDAD, FICHA).
- [ ] Integración del bloque misma hebra tras la Prop. 3.9 con estados correctos.
- [ ] M2: Conjetura 3.16 con umbral f_*(d) y márgenes 1.4 % / 2.1 % por macro.
- [ ] M3: lo abierto.
- [ ] Menores m1–m13, bibliografía, recortes.
- [ ] Compilación, páginas, CONTINUIDAD, README, FICHA.
