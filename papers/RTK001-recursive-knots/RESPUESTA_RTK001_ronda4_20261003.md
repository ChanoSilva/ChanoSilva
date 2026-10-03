# Respuesta del autor a la ronda 4 de revisión interna — RTK001 (03/10/2026)

**[EN CURSO]**

Manuscrito: v0.4 → v0.5 (fecha fija 3 October 2026). Informe atendido: `REFEREE_RTK001_ronda4_20261003.md`
(cambios menores; 0 bloqueantes, 2 mayores, 8 menores). Además se integra el resultado nuevo de `theory/`
(caso d = 2 por aritmética de intervalos y barrido conjunto de normalizaciones), después de verificarlo de forma
independiente (sección 4). `theory/` no se modificó: todo se ejecutó en copias en `experiments/`.

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
