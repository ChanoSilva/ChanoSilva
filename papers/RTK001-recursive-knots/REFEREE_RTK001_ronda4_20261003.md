# Informe de arbitraje interno independiente — RTK001, ronda 4 (03/10/2026)

## Veredicto

**Cambios menores.** Las pruebas del Lema 3.14, la Prop. 3.15, el Cor. 3.16 y la Prop. 3.17 son correctas tal como están en v0.4. Las constantes coinciden a 30 dígitos y las cotas se cumplen en curvas lisas con marco exacto. Quedan dos problemas de interpretación: el resumen, el README, la FICHA y la CONTINUIDAD dicen más de lo que prueba la Prop. 3.17 (M1), y los márgenes «at least 1.37 % / 0.23 %» de la Conj. 3.23 no son cotas inferiores de los márgenes lisos (M2; el signo sí es robusto).

Recuento: 0 bloqueantes, 2 mayores, 8 menores. Ronda 3: 13 puntos bien aplicados, 2 a medias (m3 en la CONTINUIDAD; extensión), 0 no aplicados.

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


## 2. `phase_margin.py` y Conjetura 3.23 (márgenes frente a la normalización)

Lectura del script (`experiments/phase_margin.py`, 94 líneas):
- Construye la cadena con `bishop_frame` + `offset(..., beta)`, con r_d = f·τ_poly(K_{d−1}).
- Barre β₂ (12 valores de [0, π)) y luego β₃ (12 valores + 8 de refinamiento con paso 0.058 alrededor del mínimo), con **β₂ = 0 fijo**.
- El margen es el de los pares de **vértices** que son mínimo local en i y en j (`level_census(...)["vertex"]`).
- La equivalencia «rotar N(0) un ángulo β = φ_d + β» es correcta: el transporte es lineal, la holonomía no cambia y el giro de cierre tampoco. φ + π da la misma curva (p = 2, q impar).

Verificación propia con curvas lisas (`margin_smooth.py`). La construcción es la de la §1. Busco **todos** los pares doblemente críticos (no solo los mínimo–mínimo) con distancia < 1.15·2r_d: tomo como candidatos los mínimos locales de h₁² + h₂² en la malla, con h_i = (X₁ − X₂)·T_i, y los refino con Newton sobre el interpolante de Fourier (tolerancia 10⁻¹³ en el parámetro).

| configuración (β₂, β₃) | margen liso | autor N₀ = 256 | autor N₀ = 512 |
|---|---|---|---|
| d = 2, β₂ = 0 (por defecto) | **1.3692 %** | 1.3956 % | 1.3795 % |
| d = 2, β₂ = 2π/3 | 1.3692 % (periodo π/3 confirmado) | 1.3760 % | 1.3759 % |
| d = 2, β₂ = π/12 | 6.6297 % | 6.6764 % | — |
| d = 3, (0, 0) (por defecto) | **2.0162 %** | 2.1283 % | 2.0271 % |
| d = 3, (0, 0.4654) (mínimo del autor) | 0.2162 % | 0.2388 % | 0.2329 % |
| d = 3, (0, 0.49) | **0.2146 %** | — | — |

- En todos los casos el par más cercano tras los antipodales es de tipo mínimo–mínimo. No aparece ningún par de silla o máximo por debajo. Esto respalda que el censo de vértices basta para *estas* configuraciones.
- **Barrido 2-D reducido (β₂, β₃)** (`scan2d.py`, `scan2d_ref.py`): malla gruesa de 8 × 8 en [0, π/3) × [0, π) (el periodo π/3 en β₂ está comprobado en d = 2), con mínimo 0.262 % en (0, π/8). Malla fina de 9 × 6 en β₂ ∈ [−0.25, 0.15], β₃ ∈ [0.35, 0.60]: hay un valle diagonal con valores de 0.215–0.25 %. **Mínimo 0.2146 % cerca de (0, 0.49)**; ningún punto queda por debajo de 0.214 %. Las zonas no refinadas de la malla gruesa (p. ej., (0.26, π/4): 0.52 %) no se exploraron con detalle.
- **Respuesta a las preguntas del encargo.**
  - (i) El 0.23 % **no** es robusto como cifra. Baja con la resolución (0.2388 → 0.2329 → 0.216 liso) y con el refinamiento en β₃ (mínimo cerca de 0.49, no en 0.4654). Sí es robusto el **signo**: el margen liso es ≥ 0.21 % en todo lo barrido.
  - (ii) La Conj. 3.23 es sobre la familia por defecto, así que un margen pequeño, incluso uno negativo, en otra normalización no la contradiría. Pero la normalización por proyección de e_z no es geométrica, y una conjetura que dependiera de ella sería frágil (véase M2).
  - (iii) El manuscrito **no** declara que falta el barrido conjunto. Solo dice «(that of K₁ fixed)» en l. 387. La RESPUESTA (§2, M1 y §7.4) y el docstring del script sí lo dicen.

## 3. Verificación de la ronda anterior (ronda 3)

| Hallazgo | Estado | Evidencia |
|---|---|---|
| M1 (normalización del marco) | aplicado bien (residuo: M2 nuevo) | `main.tex:86` (N_{d−1}(0) = proyección de e_z; e_x si \|T(0)·e_z\| > 0.9, igual que `recursive_knots.py:72–76`), `:90` (β ↔ φ_d + β, correcto), `:93`, `:366`, `:387`, `:414`, `:420`, `:428` |
| m1 (Θ* = 1.112) | aplicado bien | `numbers.tex:463` `\SsThetaStar` = 1.112; `main.tex:258` |
| m2 (δ_turn hacia abajo) | aplicado bien | `numbers.tex:423` 1.343 (valor 1.34399) |
| m3 (calificador «arco base < πτ») | aplicado a medias | `main.tex:387` y README:44, correctos. `CONTINUIDAD:97` sigue diciendo «no hay ninguno en los 18 niveles» sin el calificador |
| m4 (notación) | aplicado bien (nuevos choques: m2) | ϖ `:247`; x₀, y₀ `:185`; A_e `:189`; 𝒜 `:349`; Λ_Rop; s_p `:150`; Γ `:223`; vector curvatura en negrita `:287` |
| m5 (Limitaciones (4)) | aplicado bien | `main.tex:420` |
| m6 (C^{1,1}) | aplicado bien | `main.tex:223`, `:226` |
| m7 (c* en f = ½) | aplicado bien | `main.tex:253`, `:256` |
| m8 (Kalfagianni–McConkey) | aplicado bien | `main.tex:362` |
| m9 (`\SsCzeroAp`) | aplicado bien | eliminada; comentario en `make_numbers.py:351` |
| m10 (equivalencia en 3.12(c)) | aplicado bien | `main.tex:262`, `:265`, `:403` |
| DOI de Lickorish | aplicado bien | `refs.bib:103`, `main.bbl:73`; CONTINUIDAD:47 la pasa a verificadas |
| Errata de la RESPUESTA r2 (0.5091654…) | aplicado bien | `RESPUESTA_RTK001_ronda2_20261003.md:31` |
| Correcciones del integrador a `theory/` (0.0505 → 0.0504; O(8^{−d}) → O(4^{−d}) a priori; fórmula y cuantificador de la Prop. 3.17) | aplicado bien | `numbers.tex:495`; `main.tex:330` («≤ 4.44·4^{−d} a priori … roughly 8^{−d}»); `:323`. Las tres correcciones son correctas (§1) |
| Extensión | aplicado a medias | 13 páginas (antes 12). Los recortes pedidos se aplicaron, pero el bloque nuevo los supera (§6) |

## 4. Hallazgos nuevos

### Bloqueantes
Ninguno.

### Mayores

**M1. La Prop. 3.17 se presenta como un resultado negativo sobre la familia, y no lo es.**
- *Ubicación:*
  - resumen `main.tex:56`: «the derivative bound itself is not propagated (one derivative is lost per depth)»;
  - Obs. 3.18 `:330`: «an a priori bound on μ(K_{d−1}) requires the whole hierarchy of derivatives»;
  - README:36: «la cota de derivadas no se propaga (se pierde una derivada por nivel)»;
  - FICHA:3: «se demuestra que la cota de derivadas no se propaga de un nivel al siguiente»;
  - CONTINUIDAD:41: «μ no se propaga de un nivel al siguiente».
- *Problema:* la Prop. 3.17 prueba que **ninguna F localmente acotada de los datos (H_3) de una base lisa arbitraria** acota μ(K_d). No prueba que μ(K_d) no esté acotado en la familia: los valores medidos crecen despacio, 4.54 / 5.01 / 6.22 / 6.97, y coinciden en mi construcción lisa. Tampoco prueba que toda demostración necesite controlar todas las derivadas, porque la estructura explícita de la familia (K₁ es un polinomio trigonométrico) puede bastar. «Se demuestra que la cota … no se propaga», en la FICHA pública, se lee como lo primero.
- *Corrección (texto):*
  - Resumen: «…but that $\mu(K_d)$ cannot be bounded by any locally bounded function of the $(\mathrm H_3)$ data of an arbitrary base (one derivative is lost per depth in this sense)».
  - Obs. 3.18: «…an a priori bound on $\mu(K_{d-1})$ cannot be obtained from the $(\mathrm H_3)$ data of $K_{d-2}$ alone; a recursive argument must carry higher derivatives (e.g.\ all of them, via analyticity) or use the explicit structure of the family».
  - FICHA, README y CONTINUIDAD: «…y se demuestra que la cota de derivadas no puede propagarse de un nivel al siguiente usando solo esos datos para una base arbitraria; en la familia, μ crece despacio (4.5 → 7.0 de d = 1 a 4)».

**M2. Los márgenes «at least 1.37 % and 0.23 % over the normalisations tested» no son cotas inferiores de los márgenes lisos, y el barrido conjunto no se declara.**
- *Ubicación:* Conj. 3.23 `main.tex:366`; §4 `:387`; tabla de afirmaciones `:414`; README:44; FICHA:14, 25; CONTINUIDAD:44.
- *Problema:* son valores de **pares de vértices** a N₀ = 256/512, redondeados hacia abajo, y aun así superan el valor liso. En d = 2: 1.3692 % liso frente a «at least 1.37». En d = 3: 0.2146 % liso, en (0, 0.49), frente a «at least 0.23». La causa es doble: el sesgo hacia arriba de la distancia entre vértices (0.2388 → 0.2329 → 0.2162 en el mismo β₃) y la malla en β₃, cuyo mínimo cae entre nodos. Además, el texto no dice que β₂ y β₃ no se barrieron conjuntamente. En mi barrido 2-D reducido el mínimo sigue siendo ≈ 0.21 %, positivo.
- *Corrección:*
  - Escribir «≈ 1.37 % and ≈ 0.21 % (vertex-pair values 1.38 % and 0.23 % at $N_0=512$, which overestimate the smooth margin by ≈ 0.02 points)», o calcular el margen liso (curva lisa y refinamiento continuo) y citarlo.
  - Añadir en l. 387: «the joint dependence on $(\beta_2,\beta_3)$ was scanned only in reduced form (independent smooth computation in the round-4 review: minimum ≈ 0.21 %, near $(0,0.49)$)», o hacer el barrido 2-D.
  - Opcional, más limpio: enunciar la Conj. 3.23 de forma uniforme en las fases φ_d. Los datos la apoyan, y así deja de depender de una normalización no geométrica.

### Menores

- **m1. README:36: «basta … ν(K_{d−1}) ≤ 0.0336·4^d o μ(K_{d−1}) ≤ 0.0504·8^d por separado».** Es falso como condición suficiente. Cada umbral vale solo si el otro término es nulo; la condición es la suma (12). `main.tex:316` («The thresholds for each term alone») es ambiguo en el mismo sentido.
  - Corrección en el README: «la condición (12), que combina ambos términos (cada umbral, 0.0336·4^d para ν y 0.0504·8^d para μ, es el que corresponde cuando el otro término es nulo)».
  - Corrección en `main.tex:316`: «…(each with the other term set to zero; jointly, \eqref{eq:tol} applies)».
- **m2. Detalles de la prueba y de la notación de la Prop. 3.17 (`main.tex:326`).**
  - Falta una frase: para ϵ pequeño, sop Φ((t−t₀)/ϵ) cabe en un periodo, K_ϵ es regular y r < thick(K_ϵ), porque el grosor es continuo bajo perturbaciones pequeñas en C². Así K_{d,ϵ} está definida y embebida.
  - Choques nuevos: ϵ (parámetro de perturbación) frente a ε = rκ_max, en el mismo bloque, y β (ángulo de normalización, l. 90) frente a β(δ) (l. 166). Renombrar a η y a β₀ (o ϑ).
- **m3. Obs. 3.18: ν = 1.35 y μ = 6.9 en d = 4 son valores a N₀ = 128.** Los valores lisos son 1.3596 y 6.9718 (subestimación del 0.4–0.6 %). No cambia nada: el lado izquierdo liso de (12) en d = 4 es 0.1438 ≤ 0.15. Pero son entradas de una condición suficiente: escribir «1.36, 7.0 (smooth)» o declarar la resolución.
- **m4. `main.tex:287`: «an independent smooth computation».** Se refiere a `verify_H3.py`, que está en el scratchpad del integrador y no en el repositorio. Añadirlo a `experiments/` (con su salida) o quitar la mención.
- **m5. Prop. 3.15 (mejora opcional).** El tercer término admite λ[ν/(1−ε)² + rμ/(1−ε)³] en lugar de λ[ν(1+ε) + rμ]/(1−ε)³. En el Cor. 3.16, el coeficiente de ν baja de 96/√13 a 32/√13 (umbral de ν: 0.1010·4^d). En d = 2 no basta (lado izquierdo 1.49 frente a 0.684 con los valores lisos).
- **m6. Conj. 3.23: «f_*(2), f_*(3) ≥ 0.5».** f_* se define por «para todo f ≤ f_*», pero la evidencia es solo en f ∈ {0.25, 0.35, 0.5}. Añadir «at the grid values f ∈ {0.25, 0.35, 0.5}».
- **m7. Docstring de `phase_margin.py`:** habla de «Conjecture 3.19» (ahora 3.23). En d = 2 no refina alrededor del mínimo, aunque el periodo π/3 y mi cálculo liso indican que el mínimo está en β₂ = 0.
- **m8. `CONTINUIDAD:97`** sin el calificador «arco base < πτ» (véase la tabla de la §3).

## 5. Bibliografía

| Entrada | Estado | Corrección |
|---|---|---|
| Lickorish1997 | verificada (WebSearch: link.springer.com/book/10.1007/978-1-4612-0691-0 = *An Introduction to Knot Theory*, GTM 175, Springer 1997). DOI correcto en `refs.bib:103` y en el .bbl | ninguna |
| Resto (15) | sin cambios desde la ronda 3, todas verificadas allí | — |

No hay entradas nuevas en v0.4.

## 6. Extensión

13 páginas a 10 pt (objetivo: 10). El bloque (H_3) (≈ 1.1 pp.) es contenido verificable nuevo y justifica parte del exceso; las otras ≈ 2 pp. no. Recortes concretos (≈ 1.3 pp.):
1. Fundir el Lema 3.14 y la Prop. 3.15 en una proposición con una sola prueba: comparten notación y el reparto de Minkowski (≈ 8 líneas).
2. Pasar los valores poligonales de la Obs. 3.18 (ν, μ, r_d sin χ_d, cotas por nivel) a una fila de la Tabla 1 o al README, y dejar solo la conclusión (≈ 8 líneas).
3. §4, «Three further observations»: llevar los detalles del writhe (WrDiff…, LkResidual…) al apéndice o al README (≈ 8 líneas).
4. Tabla de afirmaciones: fundir las dos filas de (H_3) (l. 404–405) y las dos numéricas (l. 406–407) (≈ 4 líneas).
5. Obs. 3.13: quitar la frase histórica sobre v0.1 (≈ 2 líneas).

## 7. Verificación computacional

Todo en `referee4_RTK001/`, sin importar código del autor salvo para leer los JSON. CPU total ≈ 2.3 min (pared ≈ 1.2 min).

| Script | Qué hace | Tiempo |
|---|---|---|
| `consts.py` | mpmath, 30 dígitos: todas las constantes del bloque (H_3) (§1) | < 1 s |
| `run_smooth.py` | cadenas lisas f ∈ {0.25, 0.35, 0.5}, d ≤ 3 (d ≤ 4 en f = ½); marco de Bishop por integración espectral exacta de la 1-forma de conexión; identidades de w' y K_d' (error ≤ 1.3·10⁻¹¹); cotas del Lema 3.14 y la Prop. 3.15 (cociente ≤ 0.989); lado izquierdo de (12) | ≈ 1 s |
| `noclose_test.py` | coeficiente principal de la Prop. 3.17 (convergencia en 1/n) y crecimiento de μ(K₂) con los datos de la base convergentes | ≈ 2 s |
| `margin_smooth.py`, `scan2d.py`, `scan2d_ref.py` | márgenes lisos de la Conj. 3.23, todos los tipos de pares críticos, barrido 2-D reducido | ≈ 128 s |
| `sha256sum -c results/FROZEN_THEORY_SHA256.txt` | integridad de las copias congeladas | 17/17 OK |
| `diff theory/check_H3.py experiments/check_H3.py` | — | solo ruta de salida y resumen JSON, como se declara |
| `latexmk` en una copia | compilación | 0 avisos, 0 indefinidas, 0 «??», 13 páginas, texto idéntico al `main.pdf` entregado |

**Coincidencias:**
- ν, μ y κ_max lisos frente a los poligonales del autor: 3–4 cifras.
- r_d·cota: 0.7186 / 0.2111 / 0.1076 (macros ↑ 0.72 / 0.22 / 0.11).
- r_d sin χ_d: 0.0568 / 0.00626 / 0.00086 (macros 0.057 / 0.0063 / 0.00086).
- Lado izquierdo para d = 2: 1.9563 (macro 1.95).

No relancé `phase_margin.py` (142 s de CPU): el cálculo liso independiente lo sustituye y es más preciso. Discrepancias: M2 y m3.

## 8. Lista final de acciones (por prioridad)

1. Reescribir en el resumen, la Obs. 3.18, el README, la FICHA y la CONTINUIDAD el alcance de la Prop. 3.17: no hay F localmente acotada para una base arbitraria; no es un resultado negativo sobre la familia (M1).
2. Sustituir «at least 1.37 % and 0.23 %» por valores lisos o con el sesgo declarado (≈ 1.37 %, ≈ 0.21 %). Declarar en §4 que el barrido conjunto (β₂, β₃) solo existe en forma reducida, o hacerlo. Considerar enunciar la Conj. 3.23 de forma uniforme en φ_d (M2).
3. Corregir el «o … por separado» del README y precisar «each term alone» en `main.tex:316` (m1).
4. Añadir a la prueba de la Prop. 3.17 que K_{d,ϵ} está definida (r < thick(K_ϵ)) y renombrar ϵ → η y el ángulo β de la Def. 2.1 (m2).
5. Archivar `verify_H3.py` en `experiments/` o quitar la mención (m4). Dar ν, μ de d = 4 con su resolución (m3).
6. Precisar la evidencia de f_*(2), f_*(3) ≥ 0.5 a las tres f de la malla (m6). Actualizar el docstring de `phase_margin.py` (m7) y `CONTINUIDAD:97` (m8).
7. Opcional: afinar el tercer término de la Prop. 3.15 (m5).
8. Recortar ≈ 1.3 pp. según la §6.
