# Respuesta del autor al informe de la ronda 2 — OMR001 (03/10/2026)

Informe atendido: `REFEREE_OMR001_ronda2_20261003.md` (veredicto "cambios menores"; 0 bloqueantes, 3 mayores, 13 menores; verificación de la ronda 1: 18 bien, 2 a medias, 3 con error nuevo).
Versión resultante: manuscrito v0.3 (3 October 2026).

> Archivo escrito de forma incremental durante la revisión. Estado: EN CURSO.

## Registro de trabajo

- Lectura completa del informe, del manuscrito, de los scripts, del README, de la ficha, de la nota de continuidad y de los scripts del árbitro (`check_cor43.py`, `check_sharp_cap.py`, `check_kappa_bound.py`, `check_macros.py`).
- Verificación propia (antes de adoptar nada) de M1(b) y M2: demostración a mano (ver la respuesta a M1 y M2) y `experiments/check_uniform_cap.py` reescrito desde cero para la ronda 2 (10 s de CPU; salida en el scratchpad de la sesión): (1) la desigualdad puntual con $(\kappa,\kappa_2)$ se cumple en toda la rejilla ($m\in\{1,3,12,100\}$, cinco $\alpha$, 200×121×81 puntos) con cociente máximo 1.0000, alcanzado en $e=0$; la forma $\varphi$ antigua da 0.6849; además $\kappa\le\varphi(z)$ y $\kappa_2\le\varphi(1)$ en los cinco $\alpha$. (2) La construcción con $n_e$ fijo ($d\in\{1,5,20\}$, $m\in\{3,12,48\}$, tres $\alpha$, 400 000 réplicas con la muestra retenida simulada) da un exceso Monte Carlo igual al valor exacto $\tfrac{4\sigma}{\sqrt m}\kappa\,\E\norm{R-\theta}+\tfrac{4\sigma^2}{m}u^\ast\kappa$ dentro de ≈2 EE en los 27 casos; exceso$\times\sqrt m$ = 0.0432, 0.0331, 0.0281 para $m$ = 3, 12, 48 ($d=5$, $n_e=48$, $\alpha=0.1$), acotado lejos de 0, es decir orden $m^{-1/2}$.
- Discrepancia detectada en una cifra del informe (m6 y brief): con $\alpha=0.5$ el máximo del barrido de desviación es 1.93× en $\kappa=12$, no 1.83× en $\kappa=8$ (este último es el valor en $\kappa=8$, no el máximo). Se usa una macro generada con el máximo.
