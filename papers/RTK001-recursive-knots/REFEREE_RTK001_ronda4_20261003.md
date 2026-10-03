# [EN CURSO] Informe de arbitraje interno independiente — RTK001, ronda 4 (03/10/2026)

Versión arbitrada: v0.4 (commit 82cc500, `manuscript/main.tex`, 434 líneas). Árbitro interno, independiente de las rondas 1–3. Trabajo auxiliar en el scratchpad (`referee4_RTK001/`): `consts.py` (mpmath, 30 dígitos), `smooth.py` + `run_smooth.py` (construcción lisa propia, sin código del autor), `noclose_test.py` (prueba de la Prop. 3.17), `margin_smooth.py` (márgenes de la Conj. 3.23 en curvas lisas).

## 1. Verificación de los teoremas nuevos (bloque (H_3), l. 287–331)

### Definiciones (l. 287)
- ν = sup|v'|/v² es invariante por t ↦ t/p; μ = sup|κ_par'|/v con κ_par' = κ₁'N₀ + κ₂'B₀ = Π_⊥(dκ/dt) (porque dκ/dt = κ_par' − vκ²T). Es invariante por rotación constante del marco y geométrica (= sup|Π_⊥dκ/dσ|). M_v ≤ νv_max², M_κ ≤ μv_max, ε = rκ_max ≤ f, ζ' ≥ ζ_min. **Correcto.**

### Lema 3.14 (velocidad), l. 289–299: correcto
- Rederivado: U' = mW − vκ_⊥T, κ_⊥' = κ_par'·U + mκ_W (pues κ·U' = mκ_W), c_T' = a₀ − rvmκ_W, w' = c_Tc_T'/w.
- |w'|/w² ≤ |c_T'|/c_T² porque c_T³ ≤ w³. En el término de v', el factor (1−x) se cancela: |v'|(1−x)/(v²(1−x)²) ≤ ν/(1−ε). Los otros dos: rμ/(1−ε)² y λκ_max/(1−ε)². **Coincide con (13).**
- Comprobación lisa (identidad puntual de w' y de K_d' = c_TT + rmW, en t base): error relativo ≤ 1.3·10⁻¹¹ en los 10 niveles (f ∈ {0.25, 0.35, 0.5}, d = 1–3, y d = 4 en f = ½). En los polígonos del autor el error era ≈ 10⁻³: la identidad es exacta.

### Prop. 3.15 (curvatura), l. 301–309: correcta
- Rederivé K_d'' = aT + b_UU + b_WW, |K_d'×K_d''|² = b_U²(A+B) + (c_Wa − c_Tb_W)², c_Wa − c_Tb_W = rma₀ − vκ_W(A+2B), el reparto de Minkowski y la monotonía de (A+2B)(A+B)^{-3/2} en A (derivada ∝ −(A/2 + 2B)).
- Tercer término: rm|a₀|/(A+B)^{3/2} ≤ λ[ν/(1−x)² + rμ/(1−x)³]. El texto usa (1+ε)/(1−ε)³ en lugar de 1/(1−ε)² para ν: válido pero más flojo (no es error).

### Cor. 3.16 (tolerancia, d ≥ 3), l. 311–320: correcto
- ζ' ≥ ζ_min = (1−f_d)Θ_min/f_d ≥ Θ_min ≥ √13·2^{d−3} (cadena del Cor. 3.11: v_min/thick ≥ √13 en K₁ y se duplica por nivel; m ≤ 2). G(ζ') ≤ g(√13), 1/(1+ζ'²) ≤ 1/14, εG/(1−ε) ≤ G, (1+ε)/(1−ε)³ ≤ 12, (1−ε)^{−3} ≤ 8, r_d ≤ 2^{−d}, λ ≤ 2^{3−d}/√13. Los coeficientes 12·2^{−d}·2^{3−d}/√13 = 96/√13·4^{−d} y 8·4^{−d}·2^{3−d}/√13 = 64/√13·8^{−d} son correctos.
- Constantes (mpmath, 30 dígitos): g(√13) = 1.032454405, 2 − g(√13) − 1/14 = 0.896117023 (macro 0.8961 ↓, correcto), umbral ν = 0.033656207 (0.0336 ↓), umbral μ = 0.050484311 (0.0504 ↓). Análogo d = 2: g(√13/2) = 1.080233369, 2 − g − 4/17 = 0.684472513 (macro «< 0.685», correcto), 6/√13 = 1.66410, 1/√13 = 0.27735; 16/√13 = 4.437602 (macro 4.44 ↑, correcto).

### Prop. 3.17 (no clausura), l. 322–327: correcta tal como está enunciada ahora
- U''' = mW'' − (vκ_⊥)''T − 2(vκ_⊥)'T' − vκ_⊥T''. W'' y T'' solo tienen derivadas de orden ≤ 3 de K. κ_⊥'' = κ_par''·U + 2mκ_par'·W − m²κ_⊥ (rederivado). T = cos χ T_d + sin χ n_χ. Coeficiente de v'' en la parte normal: (1−x) sin χ, porque K''' = v''T + 3vv'κ + v²dκ/dt. **Las dos correcciones del integrador son correctas.**
- Cuantificador: con F localmente acotada, la familia K_ε → K en C³ (perturbaciones de K'', K''', K'''' de orden ε^{3/2}, ε^{1/2}, ε^{−1/2}) mantiene los argumentos en un compacto, mientras que μ(K_{d,ε}) ≥ (rv sin χ|κ_par''·U| − |R| − 3w|w'|κ_d)/w³ → ∞. Correcto. (Si α(K) = π, m puede saltar en el límite, pero sigue en un compacto: no afecta.)
- **Comprobación independiente del coeficiente** (`noclose_test.py`). Perturbé la base lisa K₁ (f = ½) con h·cos(ns)·a, con hn⁴ = 0.1, y comparé la variación de n_χ·K₂''' (calculada espectralmente) con la del término principal −rv sin χ(κ_par''·U). Cociente max|ΔQ − ΔP|/max|ΔQ| = 1.03, 1.03, 0.82, 0.42, 0.21 para n = 16, 32, 64, 128, 256: decae como 1/n. Confirma que el resto es de orden 3 y que el coeficiente es exactamente −rv sin χ.
- **Comprobación de la conclusión.** Con amplitud 30·n^{−3.5} y n = 32, 128, 512, los datos de la base convergen (ν: 0.441 → 0.419; κ_max: 1.422 → 1.399; μ: 5.28 → 4.74; sup|v''|: 12.1 → 9.1), mientras μ(K₂) crece: 6.35, 6.39, 8.54 (sin perturbar: 5.01).

### Comparación de las cotas con curvas lisas (marco de Bishop espectral exacto, sin código del autor)
Construcción: K₁ es un polinomio trigonométrico exacto (2048 muestras). El marco de Bishop de cada nivel se obtiene integrando espectralmente la 1-forma de conexión θ' = −e₁'·e₂ en el marco normal periódico (e₁ = U, e₂ = T×U), con la normalización de la Def. 2.1. Cola de Fourier ≤ 1.2·10⁻¹⁶ en todos los niveles. r_d tomados de la cadena del autor (r₂ = 0.207911, r₃ = 0.103955; d = 4: r₃/2). La 1-forma da α(K₁) = −3.02699 y m₂ = 1.98176.

| f | d | ν(K_d) | μ(K_d) | κ_max(K_d) | ν/cota (Lema 3.14) | κ_max/cota (Prop. 3.15) | r_d·cota | r_d sin χ_d |
|---|---|---|---|---|---|---|---|---|
| 0.5 | 1 | 0.41819 | 4.5444 | 1.39831 | 0.139 | 0.393 | 1.781 | 0.416 |
| 0.5 | 2 | 0.71742 | 5.0148 | 1.56570 | 0.231 | 0.453 | 0.7186 | 0.0568 |
| 0.5 | 3 | 1.12366 | 6.2214 | 1.83753 | 0.654 | 0.905 | 0.2111 | 0.00626 |
| 0.5 | 4 | 1.35962 | 6.9718 | 2.02670 | 0.813 | 0.979 | 0.1076 | 0.00086 |
| 0.35 | 3 | 0.56143 | 3.8834 | 1.48061 | 0.775 | 0.971 | 0.0654 | 0.00061 |
| 0.25 | 3 | 0.35411 | 2.1006 | 1.23710 | 0.898 | 0.989 | 0.0196 | 0.00009 |

- Las cotas se cumplen en todos los niveles. El cociente máximo es 0.989 (texto: «bound/measured ≥ 1.01»). Los valores coinciden con los del autor (`check_H3_summary.json`, N₀ = 256/512) a 3–4 cifras.
- Lado izquierdo de (12) con datos lisos: 0.4723 (d = 3) y 0.1438 (d = 4). Macros «≤ 0.48» y «≤ 0.15»: correctas. Análogo d = 2: 1.6641·0.41819 + 0.27735·4.5444 = 1.9563. Macro 1.95: correcta.
- **Desviación menor:** en d = 4 el texto imprime ν = 1.35 y μ = 6.9 (N₀ = 128: 1.3547 y 6.927), pero los valores lisos son 1.3596 y 6.972. A N₀ = 128 se subestiman en un 0.4–0.6 %. No cambia ninguna conclusión (véase m3).

**Veredicto sobre el bloque:** los cuatro enunciados son correctos tal como están en v0.4. Los hallazgos de esta sección tratan de lo que el texto *dice* que prueban (M1, m1, m2), no de las pruebas.

