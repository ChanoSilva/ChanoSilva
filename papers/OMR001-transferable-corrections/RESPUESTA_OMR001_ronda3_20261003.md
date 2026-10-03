# Respuesta del autor a la ronda 3 de revisión interna — OMR001 (v0.4 → v0.5) [EN CURSO]

Fecha: 03/10/2026. Informe: `REFEREE_OMR001_ronda3_20261003.md` (cambios menores; 0 bloqueantes, 2 mayores, 9 menores; Teorema 5.1 (i)–(iv) y Corolario 5.2 confirmados). Manuscrito resultante: v0.5 (fecha fija 3 October 2026).

## Verificación propia previa (antes de aceptar)

- Script propio en el scratchpad (`omr001_r3_author/verify_author.py`, no forma parte del paper ni importa código del paper): cuadratura de la fórmula del oráculo frente a Monte Carlo con observaciones crudas (400 000 réplicas): $m=12,\alpha=0.1$: −0.00541 (cuadratura) frente a −0.00546 ± 0.00003 (MC); $m=24,\alpha=0.1$: +0.00982 frente a +0.00978 ± 0.00004; $m=24,\alpha=0.2$: +0.00609 frente a +0.00612 ± 0.00005; partición con oráculo: −0.00657/−0.00120/−0.02447 frente a −0.00673 ± 0.00007/−0.00126 ± 0.00010/−0.02449 ± 0.00009.
- Peor caso exacto de la partición: cuadratura frente a MC de la construcción $u(\xi)$: 0.02643 frente a 0.02629 ± 0.00026 ($m=3$), 0.01577 frente a 0.01571 ± 0.00015 ($m=6$), 0.00999 frente a 0.01010 ± 0.00009 ($m=12$), $\alpha=0.1$.
- Reducción colineal (m2): en 60 casos $(\alpha,\eta,\xi)$ el supremo 2-D en rejilla nunca supera al 1-D sobre $c=\pm1$, y el argmax 2-D tiene siempre $|c|=1$.

(Detalle punto por punto: en redacción.)
