# Respuesta del autor al informe de árbitro, ronda 3 — RTK001 [EN CURSO]

Fecha: 03/10/2026. Manuscrito: v0.3 → v0.4 (fecha fija 3 October 2026).
Objeto: (A) informe `REFEREE_RTK001_ronda3_20261003.md` (cambios menores; 0 bloqueantes, 1 mayor, 10 menores; ronda 2: 19 de 20 bien, 1 a medias);
(B) integración del resultado **parcial** sobre la uniformidad de (H_3) (`theory/H3_uniform_lemma.tex`, `theory/H3_uniform_derivation.md`, `theory/check_H3.py` y su salida).

Documento escrito de forma incremental.

## 1. Verificación independiente del lema (H_3)

Hecha **antes** de pegar nada en el manuscrito. Trabajo auxiliar en el scratchpad (`author3_RTK001/`): `check_H3_copy.py` (copia de `theory/check_H3.py` con solo `ROOT` cambiado, para no sobrescribir `theory/check_H3_output.txt`) y `verify_H3.py` (script propio que no usa ningún código del autor ni de `theory/`), con su salida `verify_H3_output.txt`.

### 1.1 Re-ejecución de `check_H3.py`
- Copia ejecutada el 03/10/2026: 7.6 s de pared y unos 7.6 s de CPU (4.4 s de usuario y 3.2 s de sistema).
- Salida **idéntica línea a línea** a `theory/check_H3_output.txt`, salvo las líneas de tiempo (`diff` filtrando `done in` y `total`).

### 1.2 Lectura de cada enunciado y de su prueba (rehecha a mano)
- **Forma en longitud de arco.** ν = sup|v'|/v² es invariante por t ↦ pt (ṽ = p v(p·), ṽ' = p²v'). μ = sup|Π_⊥ dκ/dσ| es geométrica. κ_par' = κ₁'N₀ + κ₂'B₀ es la parte normal de dκ/dt, porque dκ/dt = κ_par' − vκ²T. Se cumplen M_v ≤ ν v_max², M_κ ≤ μ v_max y ε = rκ_max ≤ f. Además ζ' ≥ ζ_min, porque ε ≤ f. **Correcto.**
- **Lema lem:speedrec.**
  - w² = c_T² + r²m², con rm constante.
  - x' = r(κ_par'·U + mκ_W), usando κ·U' = κ·(mW − vκ_⊥T) = mκ_W. Por tanto c_T' = a₀ − rvmκ_W.
  - |w'|/w² = c_T|a₀ − rvmκ_W|/w³ ≤ |a₀ − rvmκ_W|/c_T², porque w ≥ c_T.
  - Se acota con |v'| ≤ νv², |κ_par'| ≤ μv, |κ_W| ≤ κ_max y 1 − x ≥ 1 − ε. **Correcto.**
- **Prop. prop:curvrec.** Es el reparto de Minkowski de la Prop. 3.8, rehecho:
  - Primer término: A(A+B) ≤ (A+2B)², y (A+2B)/(A+B)^{3/2} es decreciente en A ≥ v²(1−ε)². Con ζ = v(1−ε)/(rm) se obtiene κ g(ζ)/(1−ε) ≤ κ_max G(ζ')/(1−ε).
  - Segundo término: rm²/(A+B) ≤ 1/(r(1+ζ'²)).
  - Tercer término: rm|a₀|/(A+B)^{3/2} ≤ rm v²(ν(1+ε) + rμ)/(v³(1−ε)³) ≤ λ(ν(1+ε) + rμ)/(1−ε)³.
  - **Correcto.** La proposición no usa el grosor, salvo para garantizar ε < 1.
- **Cor. cor:tolerance (d ≥ 3).** Ingredientes:
  - ζ' ≥ ζ_min ≥ Θ_min ≥ √13·2^{d−3} ≥ √13, por la cota a priori del Cor. 3.11, que exige f_j ≤ ½ en todo nivel.
  - g es decreciente en [√2, ∞), luego G(ζ') ≤ g(√13).
  - Con ε ≤ ½: ε/(1−ε) ≤ 1, (1+ε)/(1−ε)³ ≤ 12 y (1−ε)^{−3} ≤ 8.
  - r_d ≤ 2^{−d}, por la Prop. 3.5. λ = (1−f_d)/ζ_min ≤ 2^{3−d}/√13.
  - De ahí r_dκ_max(K_d) ≤ g(√13) + 1/14 + (96/√13)4^{−d}ν + (64/√13)8^{−d}μ. El Teorema 3.13(c) concluye.
  - **Correcto.** Constantes recalculadas con mpmath (30 dígitos): g(√13) = 1.0324544, 2 − g(√13) − 1/14 = 0.8961170, 96/√13 = 26.6256, 64/√13 = 17.7504.
- **Prop. prop:noclose.**
  - **El razonamiento es correcto:** la única aparición de una cuarta derivada de K en K_d''' es κ_⊥'' dentro de −r(vκ_⊥)''T, y su coeficiente en la parte normal es −r v sin χ ≠ 0.
  - La perturbación ε^{7/2}Φ((t−t₀)/ε)U(t₀) mantiene acotados (de hecho, convergentes en C³) los datos de (H_3) y sup|v''|, y hace crecer κ_par''·U(t₀) como ε^{−1/2}.
  - Además, Π_⊥K_d''' = 3ww'κ_d + w²Π_⊥ dκ_d/dt (comprobado a mano).

### 1.3 Defectos encontrados (corregidos al integrar; `theory/` no se toca)
1. **Fórmula inexacta en prop:noclose.** El enunciado escribe la parte normal como «−r sin χ (v κ_par''·U + v''κ_⊥ + 2v'κ_⊥')» a lo largo de n_χ. Eso no es una igualdad.
   - El cálculo simbólico (sympy, cálculo del marco móvil (T, U, W)) da estos coeficientes en K_d'''·n_χ:
     - de κ_⊥'', exactamente −r v sin χ (correcto);
     - de v'', (1 − x) sin χ, porque K''' aporta v''T. El enunciado da −r κ_⊥ sin χ.
   - Además faltan términos de orden 3, como v(2mκ_par'·W − m²κ_⊥).
   - La derivación (`H3_uniform_derivation.md` §1) sí escribía «+ R_3». Al pasar al .tex se perdió el resto.
   - **Corrección:** el enunciado integrado dice que Π_⊥K_d''' = −r v sin χ (κ_par''·U) n_χ + R. El resto R está acotado por v_max, κ_max, ν, μ, sup|v''|, r y m. La conclusión no cambia.
2. **Cuantificador de prop:noclose.** «No inequality μ(K_d) ≤ F(…) holds» solo se sigue del argumento para F **localmente acotada** (por ejemplo, continua o monótona): la perturbación hace converger los argumentos de F mientras μ(K_d) → ∞. Para una F arbitraria, F podría explotar a lo largo de la sucesión. **Corrección:** «no locally bounded F».
3. **Redondeo hacia el lado inseguro y tasa no demostrada en rem:H3status.**
   - «μ hasta 0.0505·8^d» redondea **hacia arriba** un umbral suficiente: el valor exacto es 0.0504843. Debe decir 0.0504, redondeado hacia abajo (0.0336 para ν sí es correcto: 0.0336562).
   - Ambos umbrales valen **cada uno por separado**; juntos rige la condición suma (eq:tol).
   - «coefficient r_d sin χ_d = O(8^{−d}) in the family» no está demostrado. A priori solo se tiene r_d sin χ_d ≤ 2^{−d}·2λ/(1−ε)·… = O(4^{−d}), y en concreto r_d sin χ_d ≤ (16/√13)·4^{−d}. El decaimiento ≈ 8^{−d} es **medido** en los polígonos (0.416, 0.057, 0.0063, 0.00086 en d = 1…4).
   - **Corrección:** «O(4^{−d}) a priori, ≈ 8^{−d} on the polygons».

### 1.4 Comprobación numérica independiente en curvas lisas (`verify_H3.py`, 2 s de CPU)
- **Construcción.** K₁ es un polinomio trigonométrico exacto: ((1 + r₁ sin 3s) cos 2s, (1 + r₁ sin 3s) sin 2s, r₁ cos 3s). El marco de Bishop se integra con DOP853 (rtol 10⁻¹²) desde la normal convencional e_z. K₂ se deriva espectralmente (cola de Fourier ≤ 10⁻¹⁵).
- **Resultados** (cociente medido/cota):

| f₁ | r₂ | ν(K₂)/cota del Lema | κ_max(K₂)/cota de la Prop. |
|---|---|---|---|
| 0.5 | 0.2079 | 0.231 | 0.453 |
| 0.35 | 0.1225 | 0.405 | 0.825 |
| 0.25 | 0.0625 | 0.603 | 0.916 |

- Los cocientes coinciden a tres cifras con los de `check_H3.py` en los polígonos.
- ν(K₁) = 0.4182 y μ(K₁) = 4.544 en f = ½ coinciden con los valores poligonales 0.418 y 4.54.
- En f = ½ y con el **mayor r₂ admisible**, r₂ = r₁/2 = 0.25, se obtiene r₂·cota = 1.146 < 2. Es una evaluación en malla, no una demostración. Sugiere que d = 2 se reduce a un cálculo certificable sobre la curva explícita K₁ (se anota como paso siguiente; d = 2 sigue **abierto**).
- Identidades simbólicas (sympy): K_d' = v(1−x)T + rmW; w' = c_T(a₀ − rvmκ_W)/w; a = a₀ − 2rvmκ_W; b_U, b_W; |K_d'×K_d''|² = b_U²(A+B) + (c_Wa − c_Tb_W)²; c_Wa − c_Tb_W = rma₀ − κ_W v(A+2B). Todas con **residuo 0**.

### 1.5 Veredicto de la verificación
Lema lem:speedrec, Prop. prop:curvrec y Cor. cor:tolerance: **correctos tal como están**. Prop. prop:noclose: **correcta en sustancia**, con la fórmula del enunciado reescrita (resto R) y el cuantificador restringido a F localmente acotada. Observación rem:H3status: dos números corregidos (0.0505 → 0.0504; O(8^{−d}) → O(4^{−d}) a priori). Todo lo integrado lleva «proved here» (las pruebas) o «verified numerically / grid evaluation» (los números de malla). **La uniformidad de (H_3) sigue abierta**, y d = 2 también.

(Secciones siguientes en construcción.)
