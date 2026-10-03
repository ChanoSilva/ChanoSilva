# Respuesta del autor a la ronda 4 de revisión interna — RTK001 (03/10/2026)


Manuscrito: v0.4 → v0.5 (fecha fija 3 October 2026). Informe atendido: `REFEREE_RTK001_ronda4_20261003.md`
(cambios menores; 0 bloqueantes, 2 mayores, 8 menores). Además se integra el resultado nuevo de `theory/`
(caso d = 2 por aritmética de intervalos y barrido conjunto de normalizaciones), después de verificarlo de forma
independiente (sección 4). `theory/` no se modificó: todo se ejecutó en copias en `experiments/`.

## 1. Recuento

10 hallazgos (0 bloqueantes, 2 mayores, 8 menores). 8 aceptados, 1 aceptado con matiz (m3), 0 rebatidos y 1 opcional no aplicado (m5, con justificación).
- **M1 — aceptado.** La Prop. 3.17 se presenta en todas partes como lo que prueba: no hay F localmente acotada para una base **arbitraria**. No es un resultado negativo sobre la familia.
- **M2 — aceptado.** La Conj. 3.25 pasa a ser uniforme en las fases. Los márgenes se presentan como evaluaciones de malla sesgadas hacia arriba, y el sesgo se cuantifica en curvas lisas con un script propio del paper.

## 2. Hallazgos mayores

**M1 (alcance de la Prop. 3.17) — aceptado.** Cambios:
- Resumen: «μ(K_d) … cannot be bounded by any locally bounded function of the (H_3) data of an arbitrary base (one derivative is lost per depth in this sense; in the family μ grows slowly on the computed levels)».
- Obs. 3.18: «an a priori bound on μ(K_{d−1}) cannot be obtained from the (H_3) data of K_{d−2} alone; a recursive argument must carry higher derivatives (e.g. all of them, via analyticity) or use the explicit structure of the family … Proposition 3.17 says nothing about the family itself, where μ grows slowly».
- README, FICHA (ES y EN) y CONTINUIDAD:41 usan la redacción propuesta por el árbitro, con «en la familia, μ crece despacio (4.5 → 7.0 de d = 1 a 4)». Estos valores son lisos y salen de `experiments/smooth_H3.py` → `results/smooth_H3.json`: 4.544, 5.015, 6.221, 6.972. Coinciden con los del árbitro.

**M2 (márgenes de la Conj. 3.23, ahora 3.25) — aceptado.**
- (a) **Enunciado uniforme en las fases.** «for f ≤ f_*(d) and every choice of the phases φ_1, …, φ_d (equivalently, of the frame normalisations)». Así la conjetura deja de depender de la normalización por proyección de e_z.
- (b) **La evidencia se presenta como evaluación de malla y no como cota.** Ya no aparece «at least 1.37 % and 0.23 %». La conjetura dice «polygonal margins ≥ 1.37 % (d = 2) and ≥ 0.233 % (d = 3, joint scan), smooth values being slightly smaller».
- (c) **Barrido conjunto.** Se integra `joint_phase_sweep.py` (copia congelada del script de `theory/`, re-ejecutada). §4 y tabla de afirmaciones dicen: 594 pares (φ_2, φ_3) a N_0 = 256, en una rejilla 18 × 24 con dos refinamientos locales. Mínimo poligonal 0.233 % en (1.058, 0.671), 0.232 % a N_0 = 512. Máximo 13.2 %. Ningún margen negativo y τ_3 = r_3 siempre.
- (d) **Sesgo hacia arriba declarado y cuantificado.** «biased upwards (vertex pairs overestimate the distance near a critical pair; the minimum can fall between grid nodes)». El número liso sale de un script del paper, `experiments/smooth_margin.py` → `results/smooth_margin.json`. Está adaptado de la construcción lisa independiente del árbitro (marco de Bishop espectral, pares críticos de todos los tipos refinados por Newton). Valores:
  - d = 2, fases por defecto: 1.369 %;
  - d = 3, fases por defecto: 2.016 %;
  - d = 3, (0, 0.4654): 0.216 %;
  - d = 3, (0, 0.49): 0.215 %;
  - d = 3, minimizador del barrido conjunto: **0.214 %**.

  Coinciden con los del árbitro a 4 cifras (1.3692, 2.0162, 0.2162, 0.2146).
- La tabla de afirmaciones, las Limitaciones (3), el README, la FICHA y la CONTINUIDAD:44 se actualizaron en el mismo sentido.

## 3. Hallazgos menores

| id | Decisión | Cambio |
|---|---|---|
| m1 | aceptado | Cor. 3.16: «(Each term may take the whole right-hand side only if the other vanishes: … in general the joint condition (12) applies.)». En el README: «la condición (12), que combina ambos términos (cada umbral … es el que corresponde cuando el otro término es nulo)». |
| m2 | aceptado | Prueba de la Prop. 3.17: «For small η the support lies in one period, K_η is regular and r < thick(K_η), so K_{d,η} is defined and embedded». Añadí la justificación de la semicontinuidad inferior del grosor en C²: minRad es continuo, y los pares doblemente críticos a distancia ≤ 2r convergen, tras extraer una subsucesión, a uno de K. Los pares que colapsan quedan excluidos por el Lema 3.9, porque un arco con giro total < π no contiene pares doblemente críticos. Notación: ϵ → η; el ángulo de la Def. 2.1 pasa de β a ϑ, y la normalización se describe como elección de fases φ_d (§4 y Conj. hablan de (φ_2, φ_3)). La franja compleja de Next steps (1) ya no usa η_d. |
| m3 | aceptado con matiz | Se mantienen los valores poligonales (son los de `check_H3.py`), pero se declara la resolución y se dan los lisos: «d = 4 at N_0 = 128, slightly below the smooth values 1.36, 7.0 of experiments/smooth_H3.py». También: «≤ 0.15 with the smooth data» (lado izquierdo liso de (12) en d = 4: 0.1438). |
| m4 | aceptado | `verify_H3.py` archivado en `experiments/`. Solo se le añadió el volcado JSON; la salida es idéntica a la del scratchpad. Salida en `results/verify_H3_output.txt` y `results/verify_H3.json`. El texto lo cita por su ruta. |
| m5 | no aplicado (opcional) | El tercer término más fino (λ[ν/(1−ε)² + rμ/(1−ε)³]) es correcto, pero no cambia ninguna conclusión. En d = 2 no bastaba a priori, y d = 2 queda resuelto ahora por la Prop. 3.19, cuya cota usa (11) tal como está. Queda en abiertos. |
| m6 | aceptado | Conj. 3.25: «Evidence, at the grid values f ∈ {0.25, 0.35, 0.5} only: … at f = 0.25, 0.35 for the default phases and at f = 1/2 for every phase tested». |
| m7 | aceptado | Docstring de `phase_margin.py`: Conjetura 3.25; nota de que d = 2 no se refina y de que el mínimo está en β = 0 salvo discretización. |
| m8 | aceptado | CONTINUIDAD:97: «no hay ninguno con arco base < πτ y bases distintas en los 18 niveles». |
| Ronda 3, extensión (a medias) | aceptado con matiz | Recortes aplicados: (3) detalles de writhe y residuo de Lk → una frase que remite a la Limitación (5) y a `results/convergence.md`; (4) filas fundidas en la tabla de afirmaciones; (5) frase histórica de v0.1 en la Obs. 3.13. Además: valores poligonales de r_d sin χ_d y r_d·cota fuera de la Obs. 3.18, historia de c_0 en v0.2 condensada, Obs. 3.24 condensada, abstract e introducción comprimidos, `\bibsep` reducido (márgenes y letra sin cambios). No se fundieron el Lema 3.14 y la Prop. 3.15: habría renumerado todo el bloque recién arbitrado. Resultado: 14 páginas con la Prop. 3.19 y la Obs. 3.20 nuevas (v0.4: 13). |
| Estado del bloque (H_3) | aplicado | Lema 3.14, Prop. 3.15, Cor. 3.16 y Prop. 3.17 llevan «proved here; checked by an independent internal referee (round 4)», también en su fila (fundida) de la tabla de afirmaciones, en el README y en la FICHA. |

## 4. Verificación independiente de la prueba asistida d = 2

Objeto: `theory/certify_d2.py` (Prop. `prop:d2cert` de `theory/d2_certified.tex`). Copia congelada en
`experiments/certify_d2.py`; el único cambio es la ruta de salida (`results/certify_d2.json`).

1. **Monotonía de la cota de la Prop. 3.15 (ec. (kaprec), multiplicada por r_2).**
   Φ = r κ_max G(ζ')/(1−ε) + 1/(1+ζ'²) + r λ (ν(1+ε) + r μ)/(1−ε)³, con ε = r κ_max, λ = r m/v_min,
   ζ' = v_min(1−ε)/(r m) y G(ζ) = sup_{z≥ζ} g(z), que es no creciente.
   - κ_max ↑: ε ↑, 1/(1−ε) ↑, ζ' ↓ ⇒ G(ζ') y 1/(1+ζ'²) ↑. El tercer término también ↑.
   - v_min ↑: ζ' ↑ y λ ↓ ⇒ Φ ↓.
   - ν, μ: solo en el tercer término, con coeficientes ≥ 0 ⇒ ↑.
   - m ↑: ζ' ↓ y λ ↑ ⇒ ↑.
   - r ↑: ε ↑, ζ' ↓, λ ↑, y los factores r ↑ ⇒ ↑.
   - Además, la cota de la Prop. 3.15 vale con cualquier mayorante de κ_max, ν, μ y m y cualquier minorante de
     v_min. Su prueba solo usa |κ| ≤ κ_max, |v'| ≤ ν v², |κ_par'| ≤ μ v, v ≥ v_min y 1 − ε > 0.
   - Prueba numérica adicional: 24 000 diferencias finitas en mpmath (50 dígitos) sobre
     κ ∈ [0.5, 3], v ∈ [0.5, 3], ν ∈ [0, 2], μ ∈ [0, 8], r ∈ [0.01, 0.3] y m ∈ [1, 2]. Resultado: 0 violaciones
     (`check_certify_d2.py`, §4).
   **Correcto.**
2. **m < 2 a priori.**
   - La holonomía se define en (−π, π] (§2.2 del manuscrito: «a holonomy angle α ∈ (−π, π]»; el cierre
     ω = −αt/2π usa ese representante). Por tanto m = q/p − α/2π = 3/2 − α/2π ∈ [1, 2).
   - No hace falta ningún rango demostrado de α más allá de esa convención. El encierro de α_2 por la torsión
     (bono del script) es demasiado ancho para mejorarlo y no se usa.
   - Como Φ es creciente en m, m = 2 da una cota válida para todo marco de K_1. **Correcto.**
3. **Cubrimiento y simetría.**
   - Cajas en r_1: [0.5 i/512, 0.5 (i+1)/512], i = 0, …, 511. Los extremos son binarios exactos y cubren [0, ½].
   - Cajas en s: iv.mpf([j, j+1])·(2π/3)/2048, j = 0, …, 2047. Son encierros mpmath de [2πj/6144, 2π(j+1)/6144]
     y su unión cubre [0, 2π/3].
   - Simetría: K_1(s + 2π/3) = R_z(4π/3) K_1(s) es exacta, porque e^{2i(s+2π/3)} = e^{4πi/3} e^{2is} y sin 3s,
     cos 3s tienen periodo 2π/3. v, κ, |v'|/v² y |Π_⊥ dκ/dσ| son invariantes por rotaciones y por traslaciones del
     parámetro.
   - Comprobación: los supremos en flotante sobre [0, 2π) y sobre [0, 2π/3) coinciden a 2·10⁻¹⁶.
   - Las fases φ_1 y la normal inicial de K_0 solo producen una congruencia más una traslación del parámetro
     (verificado: K_1^φ(s) = R_z(−2φ/3) K_1^0(s + φ/3)).
   - El marco de K_1 y φ_2 solo entran por |U| = 1.
   **Correcto.**
4. **Redondeo.** Revisé cada operación de `certify_d2.py`:
   - `__add__`, `__sub__`, `__mul__` (cuatro productos), `recip` (que rechaza 0), `sq`, `sqrt`: todas pasan por
     `np.nextafter` hacia fuera.
   - `__neg__` y `min`/`max`/`np.minimum.reduce` son exactos.
   - Las sumas de componentes (`vdot`, `vnorm2`, `vcross`) se hacen con el `+` de `Iv`, que está ensanchado. No hay
     ninguna suma de arrays de numpy (`np.sum`) dentro de la aritmética.
   - Las únicas «potencias» son productos `Iv` y constantes enteras exactas (`float(5**j)`, `0.5`, `3.0`).
   - sin y cos se encierran con `mpmath.iv` (80 bits) y luego se redondean hacia fuera.
   - La cota final se evalúa en la misma aritmética. G = g(√2) si ζ'_lo ≤ √2 y G = g(ζ'_lo) en otro caso. Hay un
     caso límite teórico: ζ' entre `SQ2_LO` y √2. No ocurre: ζ' ≥ 2.32 en todas las cajas.
   - La suma de la holonomía (bono) se hace en racionales exactos (`Fraction`).
   - No encontré ninguna operación sin ensanchar, así que **no hubo nada que corregir**.
   - Prueba unitaria de `Iv` contra aritmética racional exacta: 14 229 pruebas, 0 violaciones.
   - `mpmath.iv.cos` sobre una caja que contiene un extremo devuelve −1 como cota inferior.
5. **Re-ejecución.**
   - `experiments/certify_d2.py`: 8 s. La salida y el JSON son idénticos a `theory/` salvo los tiempos.
   - `experiments/joint_phase_sweep.py`: 249 s de CPU de proceso, 188 s de pared, con la máquina compartida. La
     salida y el JSON son idénticos a `theory/` salvo `meta`.
6. **Chequeo propio** (`experiments/check_certify_d2.py`, 13 s de CPU). Usa fórmulas independientes: derivadas con
   sympy, y ν y μ calculadas derivando simbólicamente v y el vector curvatura, no con las formas cerradas del
   script.
   - (a) En cada una de las 512 cajas r_1, en r_1 ∈ {extremo inferior, centro, extremo superior} y en 6000 puntos
     de todo el periodo [0, 2π): 0 valores fuera de los encierros. Holguras mínimas: v 2·10⁻⁴, κ 8·10⁻³, ν 4·10⁻³,
     μ 6·10⁻³.
   - (b) Contención caja a caja en 5 cajas r_1 × 2048 cajas s × 9 puntos × 4 cantidades (368 640 pruebas):
     0 violaciones.
   - (c) Φ recalculada en mpmath con 50 dígitos desde los datos de las cajas: máximo 1.186164302669, igual a la
     salida redondeada hacia fuera del script.
   - (d) Monotonía: 0 violaciones (punto 1).
   - (e) Prueba unitaria de `Iv`: 0 violaciones (punto 4).

**Conclusión de la verificación:** la prueba es correcta tal como está. Se integra con la etiqueta «computer-assisted
proof (interval arithmetic); not yet checked by an independent referee». En consecuencia, el Cor. 3.20 pasa a ser
incondicional para d ≤ 2 (en su cadena, r_2 = fρ_1 ≤ f·thick(K_1) porque thick(K_1) ≥ ρ_1 está demostrado).
Agudeza de la cota: en el cálculo liso (no certificado) de `experiments/verify_H3.py`, r_2 κ_max(K_2) vale 0.40 en
r_2 = ¼ (f = ½, normalización por defecto), frente a la cota certificada 1.202. La Prop. 3.15 pierde un factor ≈ 3.

## 5. Números que cambiaron

No cambió ningún número de v0.4 (las corridas de referencia no se repitieron; `make_numbers.py` regenera las mismas macros). Hay macros nuevas (todas desde JSON):
- **Prueba d = 2 (redondeo hacia el lado seguro).** r_2 κ_max(K_2) ≤ 1.187 (↑); minRad(K_2) ≥ 0.842 r_2 (↓). En r_1 = ½: v_min ≥ 1.798, κ_max ≤ 1.427, ν ≤ 0.433, μ ≤ 4.638, Φ ≤ 1.202. f_c = 0.484375. Cajas 512 × 2048 (y 4096 sin simetría).
- **Barrido conjunto.** 594 evaluaciones; mínimo 0.233 % en (1.058, 0.671), 0.232 % a N_0 = 512; máximo 13.2 %; periodo π/3 a 0.05 puntos.
- **Lisos.** Márgenes 1.369, 2.016, 0.216, 0.215 y 0.214 %. d = 4: ν = 1.36, μ = 7.0. Lado izquierdo de (12) en d = 4 ≤ 0.15. Valor liso r_2 κ_max(K_2) = 0.40 (f = ½, r_2 = ¼).
- **Desaparecen del texto** (siguen en `numbers.tex`): r_d sin χ_d poligonales (\HthreeLoss*), r_d·cota (\HthreeSharp*), los valores 1/(r κ̄_d) de v0.2 (\HcCkappaHalf*) y el residuo grueso de Lk.
- **Numeración.** Se insertan la Prop. 3.19 y la Obs. 3.20, así que Hip. 3.19 → 3.21, Cor. 3.20 → 3.22, Conj. 3.23 → 3.25. El README y la CONTINUIDAD se actualizaron.

## 6. Compilación

`latexmk` con `make_numbers.py`: 0 errores, 0 referencias o citas indefinidas, 0 cajas desbordadas, `pdftotext main.pdf - | grep -c '??'` = 0. **14 páginas** (v0.4: 13; límite ≤ 14), sin cambiar márgenes ni letra. Revisé visualmente las páginas 8–15 durante los recortes y las páginas 9–13 en la versión final (Prop. 3.17 y Obs. 3.18, Prop. 3.19 y Obs. 3.20, Hip. 3.21, Conj. 3.25, §4, tabla de afirmaciones, limitaciones). `latexmk -c` deja solo `main.pdf`.

## 7. Abiertos

1. (H_3) uniforme en d, y con ello (H_c) para d ≥ 3. Ruta para d = 3 en Next steps (1).
2. Arbitraje independiente de la Prop. 3.19. Su etiqueta es «not yet checked by an independent referee».
3. Cota d = 2 más fina: minRad(K_2) > r_2 en f = ½ no se alcanza (la cota pierde ≈ 3×).
4. Márgenes de la Conj. 3.25 solo en f = ½, con rejilla y refinamiento local, sin certificación; en d = 3 son estrechos (≈ 0.21 % liso).
5. m5 opcional.
6. Extensión: 14 frente a 10 páginas.

## 8. Cómputo

CPU de proceso, en núcleos compartidos:
- `certify_d2.py`: 8 s;
- `joint_phase_sweep.py`: 249 s (188 s de pared);
- `check_certify_d2.py`: 13 s;
- `smooth_margin.py`: 8 s (más ≈ 5 s de una corrida abortada por un error de índice en r_d, corregido antes de usarla);
- `smooth_H3.py`: 2 × 2 s (la primera con el mismo error, descartada);
- `verify_H3.py`: 2 s;
- compilaciones: ≈ 20 s.

Total ≈ 5.2 min de CPU (≤ 10 min).
