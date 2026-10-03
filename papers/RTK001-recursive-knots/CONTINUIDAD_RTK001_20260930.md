# RTK001 — Continuidad interna, 30/09/2026 (actualizada 03/10/2026: rondas 1, 2 y 3 aplicadas, v0.4)

Documento de trabajo interno. No incorporar al manuscrito ni a entregas institucionales.

## Proyecto y alcance
Línea RTK001, "Geometría de nudos recursivos" / "Geometry of recursive knots", área Matemáticas y estructuras, estado en el CV web: en pausa. Ficha pública: exploración de nudos anidados y de la longitud necesaria para representarlos como tubos sin autointersección; objetivo: construir configuraciones factibles y evaluar qué puede afirmarse sobre sus cotas y optimalidad; hallazgo declarado: hay una cota superior factible para una configuración de profundidad uno; alcance: no se certifica estacionariedad ni optimalidad, y no hay ley de flujo recursiva general.

## Supuesto central (verificar con el autor)
**No existe ningún manuscrito previo de esta línea.** Todo lo que sigue se reconstruyó de la ficha:
1. Qué es un "nudo recursivo": se fijó la familia de cables iterados por desplazamiento en el marco (Definición 2.1 del manuscrito): K_0 círculo de radio 1; K_d(t) = K_{d−1}(t mod 2π) + r_d [cos θ N + sin θ B], θ = q_d t/p_d + φ_d, t ∈ [0, 2π p_d), gcd(p_d, q_d) = 1, con (N, B) marco de Bishop de K_{d−1} cerrado por un giro lineal y normalizado por N_{d−1}(0) = proyección unitaria de e_z sobre el plano normal en K_{d−1}(0) (e_x si |T(0)·e_z| > 0.9; fijado en el texto en la ronda 3, era la convención del código), y K_{d−1} reparametrizada a periodo 2π. Por defecto (p, q) = (2, 3), φ = 0.
2. Qué significa "longitud necesaria": ropelength L/grosor, con grosor en el sentido de Litherland–Simon–Durumeric–Rawdon / Gonzalez–Maddocks.
3. Qué era la "cota superior factible de profundidad uno": se interpreta como una configuración explícita con grosor positivo; aquí se da para profundidades 1, 2 y 3 como polígonos explícitos con grosor poligonal medido.
4. La elección r_d = f · τ_{d−1} (fracción del grosor previo) y la malla f ∈ {0.25, 0.35, 0.5, 0.6} son decisiones de esta sesión.

## Qué se produjo (todo en `papers/RTK001-recursive-knots/`)
1. `PLAN.md`, escrito antes que cualquier código.
2. `experiments/recursive_knots.py` (numérica determinista), `experiments/shrink.py` (sonda opcional) y `experiments/make_numbers.py` (macros LaTeX). Ningún número del manuscrito está escrito a mano.
3. Manuscrito `manuscript/main.tex` (inglés; v0.1: 10 páginas a 11 pt, 10 referencias; v0.2: 11 páginas a 10 pt, 12 referencias; v0.3: 12 páginas a 10 pt, 14 referencias; v0.4: 13 páginas a 10 pt, 14 referencias) compilado a `main.pdf` sin errores ni referencias/citas indefinidas (v0.2 y v0.3 sin cajas desbordadas).
4. README, esta nota y la propuesta de ficha.

## Decisiones tomadas
- **Grosor poligonal.** τ = min(minRad, dcsd/2), con minRad el circunradio mínimo de ternas consecutivas y dcsd la distancia mínima entre pares de vértices doblemente críticos (mínimo local de la distancia en ambos índices; se mantiene la diagonal D_ii = 0 en el test, lo que excluye automáticamente pares casi diagonales). La primera versión usaba "distancia mínima entre segmentos no adyacentes", que tiende a la longitud de arista cuando N crece (segmentos i e i+2 están a una arista de distancia) y es inservible; se descartó antes de correr nada.
- **Contraste independiente.** τ_pt = min sobre pares de vértices del radio punto–tangente de Gonzalez–Maddocks; coincide con τ al 0.01 % en todos los niveles.
- **Sin interpolación.** K_d se evalúa en los vértices de K_{d−1} (N_d = p_d N_{d−1}); el parámetro t es el índice de vértice, por lo que el ángulo del patrón avanza uniformemente en t y no en longitud de arco (la ficha no lo especifica; se declara en el manuscrito).
- **Marco de Bishop discreto.** Transporte paralelo vértice a vértice (rotación de Rodrigues que lleva T_i a T_{i+1}), holonomía α medida como ángulo con signo y eliminada con el giro −α i/N. Se comprobó numéricamente que α = 2π·frac(Wr K_{d−1}) (p. ej. α_2 = −3.027 para f = 0.5 con Wr(K_1) = 3.518), como exige Călugăreanu–White–Fuller; desde v0.2 el código calcula Lk = rint(Wr_{d−1} − α_d/2π) y guarda el residuo, cuyo máximo es 1.1·10⁻³ (resolución fina) y 4.5·10⁻³ (gruesa) sobre los 36 niveles.
- **Término de giro en la cota de longitud.** La fórmula sugerida "L_d ≤ p L_{d−1}(1 + r κ) + 2π q r" omite el giro de cierre; se añadió el término p|α| r ≤ π p r (Lema 3.3). Con él, la cota se cumple en 36 de 36 niveles medidos.
- **Constante c de la hipótesis (H_c).** Se define ρ_d = min(τ_{d−1} − r_d, c r_d sin(π/p_d)). PLAN.md dejó c sin fijar; una primera corrida usó la constante natural c = 1 (media cuerda entre hebras adyacentes) y falló en (f = 1/2, d = 1); **c = 1/2 se eligió después de ver ese dato** (corregido en la ronda 1: v0.1 presentaba (C3) como criterio predefinido y decía que c = 1 "falla exactamente en un nivel"). El JSON guarda ambas (`rho_pred` con c = 1/2, `rho_pred_cone` con c = 1). Resultado: con c = 1/2 la desigualdad se cumple con margen ≥ 1.66 en los 9 niveles por defecto con f ≤ 1/2; con c = 1 falla en 4 de los 15 niveles con f ≤ 1/2 a resolución fina — (2,3) f = 0.5 d = 1 (0.832), (3,2) d = 1 (0.968), (3,2) d = 2 (0.999), (2,5) d = 1 (0.564) — y se alcanza con igualdad en todos los niveles con τ_d = r_d (Prop. 3.5 de v0.2: c = 1 no es mejorable ahí).
- **Resoluciones.** N_0 ∈ {512, 1024} para (2,3) y (2,5); {256, 512} para (3,2), cuyo polígono de profundidad 3 tiene 27 N_0 vértices (13 824). Cambio relativo máximo entre resoluciones: 0.03 %.
- **Paso de gradiente opcional.** Se sustituyó por una sonda más simple (`experiments/shrink.py`): 200 pasos explícitos de acortamiento de curva discreto (cada vértice se mueve una fracción λ = 0.1 hacia el punto medio de sus vecinos) sobre K_1 y K_2 de la cadena (2,3), f = 1/2, N_0 = 512, midiendo L/τ en cada paso (invariante de escala, sin reescalado) y conservando el mejor polígono. No es un flujo gradiente de la longitud a grosor fijo y el tipo de nudo solo se vigila mediante τ > 0. Resultado: K_1 baja de 38.36 a 38.05 (0.8 %, aún decreciendo al final); K_2 sube monótonamente de 155.59 a 156.25. Se reporta como sonda no certificada, marginal en d = 1 y negativa en d = 2. Tiempo: 305 s.
- **Idioma.** Manuscrito en inglés; README, nota de continuidad y ficha en español.

## Resultados de referencia (corrida completa, 278 s de pared en núcleos compartidos)
- (2,3), f = 1/2: L = 15.949 / 32.349 / 64.730, τ = 0.4158 / 0.2079 / 0.1040, L/τ = 38.4 / 155.6 / 622.7 en d = 1 / 2 / 3; cociente por nivel 4.06 y 4.00.
- (2,3), f = 0.25: L/τ = 53.8 / 430.6 / 3444.6; f = 0.35: 40.8 / 233.5 / 1334.6; f = 0.6 (fuera de la hipótesis r ≤ τ/2): 50.9 / 255.6 / 852.1.
- (3,2), f = 1/2: 47.7 / 331.4 / 2296.5; (2,5), f = 1/2: 72.4 / 291.4 / 1166.2.
- Constantes teóricas (c = 1/2, (2,3)): γ = min(1 − f, f/2), A = 2(1 + f) + 4f; f = 1/2: γ = 0.25, A = 5, Λ = 20; cotas condicionales 2πΛ^d = 126 / 2513 / 50265; en la cadena del propio Corolario (r_d = fρ_{d−1}, `experiments/corollary_chain.py`, ronda 2) los polígonos dan L/τ = 38.4 / 256.5 / 2051.9 y τ_d/ρ_d ≥ 1.66 (f = 0.25, 0.35, 0.5).
- Writhe de K_1: 3.127 / 3.257 / 3.518 / 3.710 (f = 0.25 / 0.35 / 0.5 / 0.6) → número de enlace del marco 3 / 3 / 4 / 4 → K_2 = cable (2, 9) / (2, 9) / (2, 11) / (2, 11) del trébol; K_3 = cable (2, 33) / (2, 33) / (2, 39) / (2, 39) de K_2. El caso f = 0.5 se decide por un margen de 0.02 en el writhe (estable al duplicar N, pero estrecho).

## Lo que NO se afirma
- No se certifica el grosor suave de ninguna curva: τ es un proxy poligonal (pares de vértices, test de mínimo local). La evidencia es la estabilidad en N y la coincidencia con τ_pt.
- La cota inferior del grosor de K_d (v0.4, Teorema 3.12; p = 2, familia (2,3), f ≤ 1/2): **demostrado** que todo par doblemente crítico con bases distintas está a distancia ≥ min(2(τ − r), r) en toda profundidad (hebras distintas, Lema 3.7, c_1 ≥ 1/2; misma hebra, Prop. 3.10/Cor. 3.11, c_0′ ≥ 1/2, ronda 2) y que grosor(K_1) ≥ r_1/2 (d = 1 completo). Para d ≥ 2 falta la curvatura: minRad(K_d) ≥ r_d/2 se deduce de (H_3) (derivadas de la velocidad y del vector de curvatura del marco paralelo de la base) y para d ≥ 3 solo está **evaluada en malla con entradas medidas en los polígonos** (1/(rκ̂) = 0.998 en f = 1/2, d = 3), no demostrada; **en d = 2 está demostrada por computador** (ronda 4, Prop. 3.19: r_2 κ_max(K_2) ≤ 1.187, aritmética de intervalos; verificada por el autor y, en la ronda 5, por un árbitro interno independiente: «computer-assisted proof (interval arithmetic); checked by an independent internal referee (round 5)»). En la ronda 3 se integró un resultado **parcial** (Lema 3.14, Prop. 3.15, Cor. 3.16, Prop. 3.17): para d ≥ 3 la curvatura se sigue de una condición de crecimiento explícita sobre ν(K_{d−1}), μ(K_{d−1}), y se demuestra que la cota de derivadas no puede propagarse de un nivel al siguiente usando solo esos datos para una base arbitraria (ninguna función localmente acotada de los datos (H_3) acota μ(K_d)); en la familia, μ crece despacio (4.5 → 7.0 de d = 1 a 4, valores lisos). **(H_3) uniforme en d, y por tanto d ≥ 3, sigue abierto**. Los valores refinados (c_1 ≈ 0.6117, c_0′ = 0.509 / 0.845 / 0.988, etc.) son ínfimos en malla; solo los umbrales ≥ 1/2 y 1/(rκ̄_1) > 0.561 son analíticos. La hipótesis (H_c) es **sobre la familia** (la versión de v0.1, para una base arbitraria, era falsa: Obs. 3.13). La recursión Rop_d ≤ 2πΛ^d es condicional a (H_c).
- No se afirma estacionariedad, optimalidad ni ley de flujo recursiva; f no se optimizó.
- La única cota inferior nueva es interna a la familia (Prop. 3.5: thick(K_d) ≤ r_d para p = 2, luego Rop(K_d) ≥ L(K_d)/r_d ≥ 2π(p(1−f)/f)^d); para el tipo de nudo se citan Buck–Simon (Rop ≥ c_BS Cr^{3/4}) y Cantarella–Kusner–Sullivan; Cr(K_2) ≥ 13 por Kalfagianni–McConkey 2024 (que además determinan Cr de los 2-cables de nudos adecuados; no se han cotejado sus convenciones con el Lema 3.2, así que no se da el valor exacto) y, para d ≥ 3, solo cotas generales de satélites (Lackenby 2014).
- "τ_d = r_d para f ≤ f_*(d)" es conjetura (Conj. 3.25, enunciada desde v0.5 de forma uniforme en las fases; en f = 1/2, d = 2, 3 los márgenes poligonales son 1.4 % y 2.1 % con las fases por defecto, y sus mínimos sobre las fases probadas son ≈ 1.37 % y 0.233 % (barrido conjunto; 0.232 % a N_0 = 512) — evaluaciones de malla sesgadas hacia arriba, no cotas inferiores: en curvas lisas 1.369 % y 0.214 %); el cociente límite Rop_d/Rop_{d−1} → p/f (4.0 en f = 1/2) es consecuencia de esa conjetura y de L_d/L_{d−1} → p, no una constante empírica independiente (v0.1 lo presentaba como tal; corregido en la ronda 1).

## Bibliografía: grado de certeza
**Verificadas en línea** (por los árbitros de las rondas 1 y 2, WebSearch; autor, título, revista, volumen, páginas y año): Buck–Simon 1999 (Topology Appl. 91, 245–257); Cantarella–Kusner–Sullivan 2002 (Invent. Math. 150, 257–286, DOI); Litherland–Simon–Durumeric–Rawdon 1999 (Topology Appl. 91, 233–244); Pierański 1998 (CMST 4, 9–23, DOI); Gonzalez–Maddocks 1999 (PNAS 96, 4769–4773); Bishop 1975 (Amer. Math. Monthly 82(3), 246–251); Călugăreanu 1961 (Czechoslovak Math. J. 11(4), 588–625; DOI 10.21136/CMJ.1961.100486 de DML-CZ, que titula "… et leurs invariants", grafía que se mantiene; EUDML escribe "leur"); White 1969 (Amer. J. Math. 91(3), 693–728, DOI 10.2307/2373348); Fuller 1971 (PNAS 68(4), 815–819, DOI 10.1073/pnas.68.4.815); Rawdon 2003 (Exp. Math. 12(3), 287–302); Fenchel 1929 (Math. Ann. 101, 238–252, DOI 10.1007/BF01454836). Nuevas en v0.3, verificadas por el autor con WebSearch el 03/10/2026: Kalfagianni–McConkey, "Crossing numbers of cable knots", Bull. London Math. Soc. 56(11), 3400–3411 (2024), DOI 10.1112/blms.13140 (Teorema 1.1: Cr(K_{p,q}) ≥ q²Cr(K) + 1 para K adecuado; Cor. 1.2: Cr(K_{p,2}) = 4Cr(K) + 1 si p = 2wr(K) ± 1; el texto completo no fue accesible desde el proxy, por eso no se da Cr(K_2) exacto); Lackenby, "The crossing number of satellite knots", Algebr. Geom. Topol. 14(4), 2379–2409 (2014), DOI 10.2140/agt.2014.14.2379. Lickorish 1997 (GTM 175, Springer, DOI 10.1007/978-1-4612-0691-0): verificada por el árbitro de la ronda 3 (antes "coherente, no buscada"). **Coherente, no buscada:** ninguna. No se añadió Ashton–Cantarella–Piatek–Rawdon 2011: la cifra ≈ 32.7 no se confirmó en los extractos.

## Próximos pasos concretos
1. Cerrar (H_c) para la familia en toda profundidad: acotar M_v = sup|v'| y M_κ = sup|(κ_1, κ_2)'| de K_d en función de los de K_{d−1} para que (H_3) sea uniforme en d (con el Teorema 3.13 esto daría (H_c) con c = 1/2 para (2,3) en todo d y el Corolario 3.16 incondicional); p ≥ 3 (la cota δ_R2 es general; las cotas a priori usan m ≤ 2 y m_1 = 3/2). [Hechos en la ronda 2: d = 1 completo; misma hebra en toda profundidad; curvatura con el ángulo ψ conservado (Prop. 3.12).]
2. Certificar τ con aritmética de intervalos sobre un interpolante C^{1,1} (arcos circulares), para pasar de "verificado numéricamente" a "demostrado" en profundidad 1 (y quizá 2); sustituir el writhe de punto medio por el writhe poligonal exacto (Levitt; Klenin–Langowski).
3. Sustituir la sonda de acortamiento por una minimización de longitud con restricción τ ≥ 1 (gradiente de ropelength o recocido, con comprobación certificada del tipo de nudo) en d = 1, 2, para medir cuán lejos está la familia de configuraciones ajustadas (trébol: 38.4 frente a ≈ 32.7). El acortamiento simple no sirve (empeora K_2).
4. Optimizar f_d por profundidad y parametrizar el patrón en longitud de arco; probar φ_d ≠ 0.
5. Cotejar las convenciones de cable y writhe de Kalfagianni–McConkey 2024 con el Lema 3.2 para obtener Cr(K_2) exacto (cables (2, 9) y (2, 11) del trébol) y atar una cota de Buck–Simon a cada configuración de profundidad 2.
6. Certificar por aritmética de intervalos las constantes del Teorema 3.13 (c_1, c_0′, κ̂_d) y el grosor poligonal. (Las rondas 1 y 2 de revisión interna están aplicadas: véanse las secciones siguientes.)

## Ronda 1 de revisión interna (30/09/2026; aplicada el 03/10/2026)

Informe: `REFEREE_RTK001_ronda1_20260930.md` (cambios mayores; 2 bloqueantes, 6 mayores, 17 menores, 18 acciones). Respuesta punto por punto: `RESPUESTA_RTK001_ronda1_20260930.md`. En paralelo se integró el trabajo teórico de `theory/` (parte demostrada de (H_c) para p = 2), verificado a mano y con `check_Hc.py` antes de pegarlo.

| Hallazgo | Decisión | Acción en v0.2 |
|---|---|---|
| B1 (H_c) falsa para base arbitraria | aceptar | (H_c) reenunciada sobre la familia; Obs. 3.11 reproduce ambos contraejemplos; bloque teórico nuevo (Lema 3.7, Props. 3.8–3.9, Teorema 3.10) con el estado exacto de lo demostrado; Corolario condicional a (H_c) para la familia; resumen, tabla, README y FICHA actualizados |
| B2 (C3) no predefinido; "c = 1 falla en un nivel" falso | aceptar | "Criteria" dice qué se fijó antes y qué después; c = 1/2 declarado post hoc; 4 de 15 fallos con c = 1 listados por macro; tabla con τ_d/ρ_d^{(1)} (c = 1) |
| M1 caso no cubierto no es local | aceptar | párrafo reescrito (bases a < 2τ, par a través del agujero: 103.7°, dist. 1.573); "local" eliminado en todas partes; Next steps (1) reorientado |
| M2 Conjetura trivial; thick ≤ r_d demostrable | aceptar | Prop. 3.5 nueva (thick ≤ r_d, L ≥ pL(1−rκ), Rop ≥ L/r_d ≥ 2π(p(1−f)/f)^d); conjetura reducida; p/f como consecuencia |
| M3 Lk, semientero, cable, writhe del trébol | aceptar | Lema 3.2 con Lk = Wr − α/2π; código `rint(Wr − α/2π)` + residuo (1.1·10⁻³); convención autocontenida; FICHA corregida; r* = 0.4904 |
| M4 precisión del writhe | aceptar con matiz | párrafo "Writhe accuracy" (10⁻⁴ en d = 1; 0.031 en (3,2) d = 3); writhe exacto queda como paso siguiente |
| M5 Corolario | aceptar | ρ_d := γρ_{d−1}; (H_c) para todo r ≤ fτ; inducción explícita |
| M6 artefactos | aceptar | páginas, "wall-clock", frase de la sonda, residuo en esta nota |
| m1–m17 | aceptar (m16 con matiz) | véase RESPUESTA §3 |
| Recortes 1–7 | aplicados | Tabla 3 → `results/convergence.md`; Tablas 1+2 fusionadas; Tabla 4 → frase; Fig. 1 reducida; §6+§7 fusionadas; sonda y protocolo abreviados/movidos |

Cómputo de la ronda: corrida de referencia completa relanzada tras el cambio de código (3 min 06 s de pared, 3 min 05 s de CPU; todos los campos previos idénticos a v0.1), `aux_checks.py` 33 s, `check_Hc.py` 36 s, compilaciones ≈ 1 min. Total ≈ 5 min de CPU.

**Qué quedaba abierto tras la ronda 1** (superado en parte en la ronda 2, véase abajo): (i) caso misma hebra de (H_c) en f = 1/2 (constantes evaluadas en malla 0.32/0.13/0.16; v0.2 las llamaba "demostradas", corregido en la ronda 2) y constante de curvatura a priori en f = 1/2, d = 2 (0.48); (ii) uniformidad en d de (H_3); (iii) p ≥ 3 no tratado en la parte demostrada; (iv) las constantes del Teorema 3.10 distintas de c_1(1/2, 2/3) ≥ 1/2 son ínfimos en malla con corrección Lipschitz estimada, no aritmética de intervalos; (v) writhe poligonal exacto no implementado; (vi) certificación del grosor poligonal; (vii) bibliografía: 7 entradas coherentes pero no verificadas en línea (listadas arriba).

## Ronda 2 de revisión interna (03/10/2026)

Informe: `REFEREE_RTK001_ronda2_20261003.md` (cambios menores; 0 bloqueantes, 4 mayores, 13 menores; ronda 1: 23 puntos bien aplicados, 2 con error nuevo). Respuesta punto por punto: `RESPUESTA_RTK001_ronda2_20261003.md`. En la misma pasada se integró el trabajo terminado de `theory/` sobre el caso "misma hebra" (`same_strand_lemma.tex`, `same_strand_derivation.md`, `check_same_strand.py`), verificado por el autor antes de pegarlo (lectura de cada paso, re-ejecución con salida idéntica byte a byte, formas cerradas recomputadas, censo independiente de pares críticos). Manuscrito → v0.3 (12 páginas a 10 pt; antes 11).

| Hallazgo | Decisión | Acción en v0.3 |
|---|---|---|
| M1 estado de las constantes | aceptar | "demostrado" solo para lo analítico (c_1 ≥ 1/2, c_0′ ≥ 1/2, 1/(rκ̄_1) > 0.561); 0.6117 y demás = "grid value"/"grid evaluation, not certified"; en d = 2, 3 "evaluación en malla con entradas medidas en los polígonos"; resumen, Lema 3.7, Teorema 3.13, Hip. 3.15, tabla de afirmaciones, Limitaciones (4), README, FICHA y esta nota. Además d = 1 queda demostrado analíticamente para todo f ≤ 1/2 (mejor que la opción f ≤ 0.35 que sugería el árbitro) |
| M2 conjetura tautológica | aceptar | Conj. 3.19 con umbrales f_*(d) y condición sobre los demás pares doblemente críticos; márgenes 1.4 % / 2.1 % (f = 1/2, d = 2, 3) generados por macro desde `classify_pairs.py` (1.4 % / 2.0 % con N_0 = 512) |
| M3 lo abierto desfasado | aceptar | lo abierto ya no es "misma hebra" (demostrado) sino (H_3) uniforme en d y la certificación; censo de pares en §4 con el dato reconciliado (véase abajo); Next steps (1) reescrito |
| M4 dependencia de `theory/` | aceptar | `experiments/check_Hc.py`, `experiments/check_same_strand.py` (copias, solo rutas) → `results/check_*_summary.json` (idénticos byte a byte a los de `theory/`); SHA-256 en `results/FROZEN_THEORY_SHA256.txt`; `make_numbers.py` lee solo `results/` y falla si falta un insumo |
| B2/m3 doble listado de (3,2) d = 2 | aceptar | tolerancia única 5·10⁻⁴ (> cambio de τ por resolución, 0.03 %); 0.9989 es estable al duplicar N (0.99889 → 0.99886), así que es fallo, no igualdad; aserción de disjunción en `make_numbers.py` |
| m1 redondeos del Paso 4 | aceptar | β(π/3) < 0.5484, √(1−β²) > 0.8362, P₁ > 0.8169, P₁² > 0.667, suma > 1.01; igualdad Λ = 1 en δ = π/3 señalada |
| m2 citas del Teorema | aceptar | prueba del Teorema 3.13 cita Prop. 3.6(a)/(b), Paso 1 del Lema 3.7, Lema 3.7, Prop. 3.10, Props. 3.8/3.12 |
| m4–m7 | aceptar | resumen precisado ((H_3) con torsión; κ_max(K_{d−1}); hebras relativas al arco); M_v, M_κ y c_BS; cuantificador de (H_c); cadena del Corolario medida (`corollary_chain.py`) |
| m8 números de cruce | aceptar con matiz | Obs. 3.18: Cr(K_2) ≥ 13 (Kalfagianni–McConkey, Teor. 1.1) y que ellos determinan Cr de 2-cables de nudos adecuados, sin dar el valor exacto (convenciones no cotejadas; texto completo inaccesible); Lackenby 2014 para d ≥ 3; FICHA |
| m9–m13 | aceptar | bibliografía unificada (arriba); RESPUESTA ronda 1 §5 corregida ("11 páginas", con nota de corrección); constantes en tabla (Tabla 1); fuente 10 pt mantenida |
| Bibliografía | aceptar | DOIs de Fenchel, White, Fuller, Călugăreanu (y número 4); dos referencias nuevas verificadas |
| Recortes | aplicados en parte | Fig. 1 retirada (queda en `figures/`); estado detallado solo en Tabla 1 y tabla de afirmaciones; "On the constant" condensado; Obs. 3.14 abreviada; sonda de acortamiento a una frase; observaciones de crecimiento y escritura de writhe condensadas; Prop. 3.9 de v0.2 (misma hebra bajo (H_3), c_0) **retirada por superada** (queda en v0.2 y en `theory/Hc_lemma.tex`) |

**Dato reconciliado (pares críticos de la misma hebra).** El árbitro ("ningún par crítico de la misma hebra en d = 1–3") y el agente teórico ("pares de misma hebra con δ < π solo en d = 1, δ ≥ 1.96, distancia ≥ 3.70 r") tenían ambos razón con detectores distintos: con el test de mínimo local de vértices (el del proxy τ) no hay ninguno con arco base < πτ y bases distintas en los 18 niveles; con un test de cambio de signo que detecta también sillas y máximos, los hay solo en d = 1 (f = 1/2: δ ≥ 1.96 > δ_turn = 1.068, distancia ≥ 3.70 r) y ninguno en d = 2, 3 (`experiments/classify_pairs.py`, cómputo propio).

**Números que cambiaron en el texto:** ninguno de los experimentos (no se tocó `recursive_knots.py`; `results.json` intacto). Cambian: lista de igualdades con c = 1 ("(3,2), d = 3; (2,5), d = 2,3"; antes incluía por error (3,2) d = 2); constantes ahora redondeadas hacia abajo (p. ej. 1/(rκ̄) en f = 1/2, d = 2: 0.48, antes 0.49); constantes nuevas (c_0′, 1/(rκ̂), márgenes, censo, cadena del Corolario).

**Cómputo de la ronda 2:** `check_Hc.py` 57 s y `check_same_strand.py` 25 s (pared), `classify_pairs.py` 49 s de CPU, `corollary_chain.py` 26 s de CPU, formas cerradas < 1 s, compilaciones ≈ 1.5 min. Total ≈ 4 min de CPU.

**Qué queda abierto tras la ronda 2:** (i) (H_3) uniforme en d, que con el Teorema 3.13 cerraría (H_c) con c = 1/2 para (2,3) en toda profundidad (en d = 2, 3 solo hay evaluación en malla con entradas medidas); (ii) certificación por intervalos de c_1, c_0′, κ̂_d y del grosor poligonal; (iii) p ≥ 3 y otros patrones; (iv) Conjetura 3.19 (umbral f_*(d)); (v) writhe poligonal exacto; (vi) Cr(K_2) exacto vía Kalfagianni–McConkey con convenciones cotejadas; (vii) bibliografía: Lickorish 1997 coherente pero no buscada.

## Ronda 3 de revisión interna e integración de (H_3) parcial (03/10/2026)

Informe: `REFEREE_RTK001_ronda3_20261003.md` (cambios menores; 0 bloqueantes, 1 mayor, 10 menores; ronda 2: 19 de 20 bien aplicados, extensión a medias). Respuesta punto por punto: `RESPUESTA_RTK001_ronda3_20261003.md`.

En la misma pasada se integró el resultado **parcial** de `theory/` sobre la uniformidad de (H_3) (`H3_uniform_lemma.tex`, `H3_uniform_derivation.md`, `check_H3.py`).

**Verificación del autor antes de integrar.**
- Lectura paso a paso de cada prueba.
- Re-ejecución de `check_H3.py` en una copia: salida idéntica salvo tiempos.
- Script propio `verify_H3.py` en el scratchpad `author3_RTK001/`:
  - cálculo simbólico del marco móvil con sympy (identidades con residuo 0);
  - constantes con mpmath;
  - K₁ liso exacto, marco de Bishop por DOP853 y K₂ espectral; cocientes medido/cota iguales a tres cifras a los poligonales.
- **Correcto tal cual:** Lema 3.14 (velocidad), Prop. 3.15 (curvatura) y Cor. 3.16 (tolerancia, d ≥ 3).
- **Corregido al integrar** (`theory/` no se tocó):
  1. La fórmula de la parte normal de K_d''' en la Prop. 3.17 no era una igualdad (el coeficiente de v'' es (1 − x) sin χ, no −rκ_⊥ sin χ). Se reescribe como «término de cuarto orden −rv sin χ (κ_par''·U) n_χ + resto acotado».
  2. Su cuantificador se restringe a cotas F localmente acotadas.
  3. En la observación final, el umbral de μ pasa de 0.0505 a 0.0504 (estaba redondeado hacia el lado inseguro), y el «O(8^{−d})» del coeficiente perdido pasa a «O(4^{−d}) a priori, ≈ 8^{−d} medido».

| Hallazgo | Decisión | Acción en v0.4 |
|---|---|---|
| M1 normalización del marco no definida | aceptar | Def. 2.1 fija N_{d−1}(0) (convención del código) y dice que rotarla equivale a φ_d + β. Los resultados de la §3 valen para toda normalización. `experiments/phase_margin.py` (142 s de CPU) da: margen en d = 2 de 1.37–21.3 % (12 normales; por defecto, cerca del mínimo); en d = 3, 0.23–13.0 % (20 normales del marco de K₂, con K₁ fijo; mínimo estable a N₀ = 512). L y τ_d = r_d no cambian. Conj. 3.23, §4, tabla de afirmaciones y Limitaciones (3) |
| m1 Θ* | aceptar | 1.112 (redondeo hacia abajo de una condición necesaria); regla general de redondeo escrita en `make_numbers.py` |
| m2 δ_turn | aceptar | `floor_fmt`; Tabla 1 (0.35, d = 1): 1.344 → 1.343 |
| m3 «arco base < πτ» | aceptar | §4, README y esta nota |
| m4 notación | aceptar y ampliar | ϖ, x₀/y₀, A_e, 𝒜, Λ_Rop, s_p; además Γ (arco) y vector curvatura en negrita |
| m5 Limitaciones (4) | aceptar | Formas cerradas del Cor. 3.11 y constantes del Cor. 3.16 listadas como analíticas |
| m6 C^{1,1} | aceptar | Lema 3.9 |
| m7 c* en d = 1 | aceptar | Prueba en f = ½ y transferencia por monotonía; «c₀′ > 0.509 for every f ≤ ½» |
| m8 Kalfagianni–McConkey | aceptar | Su Cor. 1.2 cubre las pendientes 2w ± 1 = ±5, ±7, no 9 ni 11; no se da Cr(K₂); FICHA: «acotado inferiormente» |
| m9 `\SsCzeroAp` | aceptar | Macro eliminada |
| m10 equivalencia en el enunciado | aceptar | Teorema 3.12(c) |
| Lickorish DOI; errata de la RESPUESTA r2 | aceptar | `refs.bib`; nota de corrección en la RESPUESTA r2 |
| Extensión | aceptar con matiz | Recortes 1–5 del árbitro, Fig. 1 retirada, resumen compacto, `longtable`. Resultado: **13 páginas** (antes 12), porque el bloque (H_3) añade ≈ 1.1 páginas con cuatro demostraciones; bajar de 12 exigiría quitar demostraciones |

**Integración de (H_3) parcial.**
- Párrafo «Towards (H_3) uniformly in d» con Lema 3.14, Prop. 3.15, Cor. 3.16 y Prop. 3.17, todos «proved here», y Obs. 3.18 («grid evaluation with polygon inputs; uniformity open»).
- Números por macro desde `results/check_H3_summary.json`, generado por `experiments/check_H3.py`, copia congelada de `theory/check_H3.py` (solo cambia el directorio de salida y se añade el resumen JSON).
- SHA-256 añadidos a `results/FROZEN_THEORY_SHA256.txt`: copia, JSON, salida y cuatro originales de `theory/`; 17/17 OK.
- La uniformidad de (H_3) consta como **abierta** en el resumen, la introducción, la Hip. 3.19, la tabla de afirmaciones, Limitaciones (1) y Next steps (1).

**Números que cambiaron:**
- Ninguno de los experimentos de referencia.
- Redondeos: Θ* 1.12 → 1.112; δ_turn (0.35, 1) 1.344 → 1.343; g(√2) pasa a macro («< 1.0887»).
- Nuevos: márgenes por normalización; constantes del Cor. 3.16 (0.8961, 0.0336, 0.0504); valores de malla de la Obs. 3.18.

**Cómputo de la ronda 3:**

| Tarea | CPU |
|---|---|
| `check_H3.py` (dos corridas) | ≈ 15 s |
| `verify_H3.py` | 2 s |
| `phase_margin.py`: tres corridas, la última es la válida | 366 s |
| Compilaciones | ≈ 1 min |
| **Total** | **≈ 7.5 min** |

**Qué queda abierto tras la ronda 3:**
1. (H_3) uniforme en d. Por la Prop. 3.17 exige controlar todas las derivadas; la vía natural, no hecha, es una inducción por analiticidad en una banda compleja |Im t| < η_d.
2. d = 2. Las constantes a priori no bastan: 1.95 frente a < 0.685. Como K₁ es un polinomio trigonométrico explícito, la forma fina de (11) es un cálculo finito certificable. Una evaluación propia en malla, no certificada y solo en el scratchpad, da r₂·cota = 1.146 < 2 con el mayor r₂ admisible en f = ½.
3. Certificación por intervalos de c₁, c₀′, κ̂_d y del grosor poligonal.
4. Conjetura 3.23: margen de 0.23 % en d = 3 para alguna normalización; queda pendiente un barrido 2-D (β₂, β₃).
5. p ≥ 3.
6. Writhe poligonal exacto.
7. Cr(K₂) exacto, con las pendientes 9 y 11.
8. Extensión de 13 páginas.

## Ronda 4 de revisión interna e integración de d = 2 (03/10/2026)

Informe: `REFEREE_RTK001_ronda4_20261003.md` (cambios menores; 0 bloqueantes, 2 mayores, 8 menores; Lema 3.14, Prop. 3.15, Cor. 3.16 y Prop. 3.17 confirmados correctos). Respuesta: `RESPUESTA_RTK001_ronda4_20261003.md`. Manuscrito v0.4 → **v0.5** (14 páginas). Además se integró el resultado nuevo de `theory/` (caso d = 2 por aritmética de intervalos y barrido conjunto de fases) tras verificarlo (RESPUESTA §4). `theory/` no se modificó.

| Hallazgo | Acción |
|---|---|
| M1 (alcance de la Prop. 3.17) | Aceptado. Resumen, Obs. 3.18, README, FICHA y esta nota dicen ahora que ninguna F localmente acotada de los datos (H_3) de una base **arbitraria** acota μ(K_d). No es un resultado negativo sobre la familia: allí μ crece despacio (4.5 → 7.0 de d = 1 a 4, `smooth_H3.py`). |
| M2 (márgenes de la Conj.) | Aceptado. Conj. 3.25 enunciada de forma uniforme en las fases. Los márgenes se presentan como evaluaciones de malla y no como cotas: el barrido conjunto da un mínimo poligonal de 0.233 % (0.232 % a N_0 = 512). Se declara el sesgo hacia arriba y se cuantifica con un script propio en curvas lisas (`smooth_margin.py`): 1.369 % en d = 2 y 0.214 % en el minimizador conjunto de d = 3. |
| m1 («por separado») | Aceptado: README y Cor. 3.16 dicen que la condición es la suma (12). |
| m2 (r < thick(K_η); ϵ/ε; β) | Aceptado. Frase de semicontinuidad inferior del grosor en C² añadida a la prueba de la Prop. 3.17. Renombrados ϵ → η y el ángulo de la Def. 2.1 β → ϑ (ahora se habla de fases φ_d). |
| m3 (d = 4 a N_0 = 128) | Aceptado: se declara la resolución y se dan los valores lisos 1.36 y 7.0; el lado izquierdo liso de (12) sigue ≤ 0.15. |
| m4 (verify_H3.py) | Aceptado: archivado en `experiments/` con salida y JSON congelados. |
| m5 (afinar la Prop. 3.15) | No aplicado (opcional; no cambia d = 2 a priori, y d = 2 queda resuelto por la Prop. 3.19). |
| m6 (f_*(2), f_*(3) ≥ 0.5) | Aceptado: la evidencia se restringe a f ∈ {0.25, 0.35, 0.5}, con fases barridas solo en f = 1/2. |
| m7 (docstring de `phase_margin.py`) | Aceptado. |
| m8 (CONTINUIDAD:97) | Aceptado: calificador «arco base < πτ y bases distintas». |
| Estado del bloque (H_3) | «proved here; checked by an independent internal referee (round 4)» en el texto, la tabla de afirmaciones, el README y la FICHA. |
| Extensión | Recortes 3, 4 y 5 del árbitro, más compresiones menores; 13 → 14 páginas con la Prop. 3.19 añadida. |
| Integración d = 2 | Prop. 3.19 + Obs. 3.20 [en v0.5: computer-assisted proof (interval arithmetic); not yet checked by an independent referee; desde v0.6: «checked by an independent internal referee (round 5)»]. Hip. 3.21 demostrada en d ≤ 2 y Cor. 3.22 incondicional para d ≤ 2. Scripts congelados con SHA-256. Chequeo propio en `check_certify_d2.py`. |

**Abierto tras la ronda 4.**
1. (H_3) uniforme en d, y con ello (H_c) para d ≥ 3. La ruta concreta para d = 3 está en Next steps (1): intervalos en cajas (s, ángulo, r_2).
2. Revisión independiente de la prueba asistida d = 2 (Prop. 3.19). Hasta ahora solo la ha verificado el autor. → **Cerrado en la ronda 5** (auditoría línea a línea y encierro independiente del árbitro: correcta).
3. Una cota d = 2 más fina, que permitiría minRad(K_2) > r_2 en f = 1/2. Hoy está certificado solo para f ≤ 0.484375; la cota pierde un factor ≈ 3 frente al valor liso.
4. Márgenes de la Conj. 3.25:
   - solo en f = 1/2 se barren fases, y en d = 3 con rejilla y refinamiento local, sin minimización global;
   - no hay ninguna certificación;
   - en d = 3 el margen liso es ≈ 0.21 %, estrecho.
5. Opcional m5: tercer término de la Prop. 3.15.
6. Extensión: 14 páginas frente al objetivo de 10.

## Ronda 5 de revisión interna (03/10/2026)

Informe: `REFEREE_RTK001_ronda5_20261003.md` (cambios menores; 0 bloqueantes, 1 mayor, 8 menores). Respuesta punto por punto:
`RESPUESTA_RTK001_ronda5_20261003.md`. Manuscrito v0.5 → **v0.6** (fecha fija 3 October 2026), 14 → **13 páginas** (márgenes y
letra sin cambios; ninguna demostración suprimida).

**Veredicto del árbitro sobre la prueba asistida d = 2.** Correcta: cadena lógica comprobada paso a paso, código de intervalos
auditado línea a línea (ninguna operación sin redondeo hacia fuera, ningún encierro inválido) y una implementación propia solo con
`mpmath.iv` que certifica la misma desigualdad (< 2) en todo el rango. Desde v0.6 la Prop. 3.19 y la Obs. 3.20 llevan
**«computer-assisted proof (interval arithmetic); checked by an independent internal referee (round 5)»** en el enunciado, la tabla
de afirmaciones, la Limitación (1), el README, la FICHA (ES/EN) y esta nota (l. 41, tabla de la ronda 4, abierto 2 de la ronda 4).

| Hallazgo | Acción |
|---|---|
| M1 (extensión, 14 pp.) | Aceptado con matiz: 13 pp. Recortes del árbitro (1) Obs. 3.20 acortada (segunda corrida y lista de `check_certify_d2.py` → README), (2) §4 «Three further observations» a una frase por resultado (barridos, periodos, refinamientos → README), (3) lista de ν, μ de la Obs. 3.18 abreviada (→ `results/theory_constants.md`), (5) Tabla 1 solo f = ½ (f = 0.25, 0.35 → `results/theory_constants.md`). **No** se fundieron el Lema 3.14 y la Prop. 3.15 (recorte 4): renumeraría la Prop. 3.19 recién arbitrada y todo lo posterior (3.19 → 3.18, 3.20 → 3.19, 3.21 → 3.20, 3.22 → 3.21, 3.25 → 3.24), y el ahorro (≈ 3 líneas efectivas) no compensa la confusión. Para llegar a 13 pp. se comprimieron además: resumen, introducción (historia de revisiones), §2.4 (cocientes segmento–segmento → `aux_checks.json`), historia de v0.2 en la misma hebra, párrafo tras la Prop. 3.6, Obs. 3.4, Obs. 3.23, 3.24, Limitaciones, Next steps, apéndice; la Obs. «growth rate» (antigua 3.26, la última numerada: no renumera nada) pasa a una frase tras la Conj. 3.25; las filas f = 0.25 y la sonda f = 0.6 de la Tabla 2 pasan a `results/tables.md` (ya estaban allí). |
| m1 («K₁ has κ > 0» falso en r₁ = 4/13) | Aceptado. Docstring y comentario de `experiments/certify_d2.py` corregidos (κ(K₁)(π/2) = \|4 − 13r₁\|/(4(1−r₁)² + 9r₁²); el encierro de torsión solo se evalúa en r₁ = 0.25, 0.35, 0.5, donde κ_min = 0.267, 0.197, 0.769, `results/smooth_d2_phases.json`; el encierro de α₂ en r₁ = ½ cruza −π y el «m₂» impreso no es un encierro). Manuscrito: «… where κ > 0» en la Prop. 3.8. **Nota de corrección para `theory/d2_certified_derivation.md:159`** (no editado, regla de no tocar `theory/`): la frase «Como κ(K_1) > 0, el marco de Frenet es periódico» es falsa en r₁ = 4/13 (κ se anula en s = π/2 + 2πk/3); el bono de holonomía por torsión solo vale donde κ > 0 (en r₁ = 0.25, 0.35, 0.5 sí) y su intervalo «reducido a (−π, π]» en r₁ = ½ solo encierra α₂ módulo 2π. Lo mismo vale para el docstring de `theory/certify_d2.py:24–25`. El bono no interviene en la cota ni en el manuscrito. |
| m2 (Prop. 3.15 fuera de f ≤ ½) | Aceptado. La Prop. 3.15 (y el Lema 3.14) se enuncian para todo r > 0 con ε = rκ_max(K) < 1 (sus pruebas no usan τ ni f); la prueba de la Prop. 3.19 lo dice, con «r₂/thick(K₁) may exceed ½» y «ε ≤ 0.355 on every box» (macro `\DtwoCertEpsMax`, de `certify_d2.json["B"]["max_eps_hi"]` = 0.35470, clave añadida en v0.6). |
| m3 (no agudeza) | Aceptado. Obs. 3.20: la pérdida viene de separar los cuatro supremos y del reparto de Minkowski; en r₁ = ½ el m₂ real es 1.98 (macro de `smooth_d2_phases.json`), así que m₂ ≤ 2 apenas cuesta. Valores lisos con r₂ = r₁/2: 0.40 (r₁ = ½, fases por defecto), ≈ 0.41 (máximo sobre 48 fases en r₁ = ½) y ≈ 0.48 (máximo sobre las fases y r₁ ≤ ½ muestreados, 0.4767 en r₁ = 0.4903, justo antes de r₁* ≈ 0.4904, donde α₂ cruza π), de `experiments/smooth_d2_phases.py` (nuevo). Opcional: «The printed constant is that of this interval extension». |
| m4 (base de confianza; fallo explícito) | Aceptado. Obs. 3.20 y docstring: binary64 con redondeo al más cercano sin *flush-to-zero*, `float()` de `mpf` al más cercano, `mpmath.iv`. `certify_d2.py`: `assert_finite` sobre todos los encierros y `assert res["ok"] and np.isfinite(res["total"])` en cada caja (también en el bloque (A) y en el bucle de f_c). Re-ejecutado: salida idéntica salvo tiempos; JSON idéntico salvo tiempos y claves añadidas. SHA-256 re-congelados. Sobre la RESPUESTA de ronda 4, §4.4: el «caso límite ζ' entre SQ2_LO y √2» no puede ocurrir, porque `SQ2_LO` es el mayor flotante < √2. |
| m5 (README sin salvedad) | Aceptado: README con la salvedad y la nueva etiqueta. |
| m6 (`smooth_margin.py`, `phase_margin.py`) | Aceptado: ventana de exclusión documentada (\|ds − π\| ≤ 0.05; el árbitro comprobó que una ventana de 0.004 da los mismos cinco márgenes); atribución de `phase_margin.py` corregida (cálculo del árbitro de la ronda 4, no `smooth_margin.py`). `smooth_margin.py` re-ejecutado: idéntico salvo tiempos. |
| m7 (Limitación (1), fila de la tabla) | Aceptado: «completely at d = 1 and, computer-assisted, at d = 2 …; for d ≥ 3 …»; fila de la Prop. 3.8: «at d = 2 superseded by Prop. 3.19». |
| m8 (salto de m₂ en r₁ ≈ 0.49) | Aceptado: frase en la prueba de la Prop. 3.19. |
| m5 de la ronda 4 (tercer término) | No aplicado: cambiaría la Prop. 3.15 y la cota certificada recién arbitrada; queda abierto. |

**Numeración.** Sin cambios respecto de v0.5 para todo lo numerado hasta la Conj. 3.25 (Lema 3.14, Prop. 3.15, Cor. 3.16,
Prop. 3.17, Obs. 3.18, Prop. 3.19, Obs. 3.20, Hip. 3.21, Cor. 3.22, Obs. 3.23, 3.24, Conj. 3.25). Solo desaparece la antigua
Obs. 3.26 (growth rate), que era la última y pasa a ser texto sin número.

**Código y hashes.** `certify_d2.py` (docstring, comentarios, `assert`, clave `max_eps_hi`), `smooth_margin.py` y
`phase_margin.py` (docstrings), `make_numbers.py` (macros nuevas `\DtwoCertEpsMax` = 0.355, `\DtwoSmoothHalfMax` = 0.41,
`\DtwoSmoothMax` = 0.48, `\DtwoSmoothMaxRone` = 0.490, `\DtwoSmoothMtwoHalf` = 1.98; escribe `results/theory_constants.md`;
la Tabla 2 omite f = 0.25 y 0.6) y el nuevo `smooth_d2_phases.py`. Las 556 macros de v0.5 conservan su valor (comprobado por
programa). `results/FROZEN_THEORY_SHA256.txt` actualizado (hashes v0.5 comentados, nuevos activos);
`sha256sum -c` pasa. `theory/` no se tocó.

**Abierto tras la ronda 5.**
1. (H_3) uniforme en d, y con ello (H_c) para d ≥ 3 (ruta para d = 3: Next steps (1)).
2. Cota d = 2 más fina (la certificada, 1.187, frente a ≈ 0.48 liso): minRad(K_2) > r_2 en f = ½ sigue sin certificar.
3. Márgenes de la Conj. 3.25: solo f = ½, rejilla y refinamiento local, sin certificación; en d = 3 ≈ 0.21 % liso.
4. Opcional m5 de la ronda 4 (tercer término más fino de la Prop. 3.15).
5. Extensión: 13 páginas frente al objetivo original de 5–10; bajar más exigiría quitar demostraciones o tablas de evidencia.
6. Las erratas de `theory/` (m1) quedan anotadas aquí; corregirlas en `theory/` corresponde a quien mantenga esa carpeta.

