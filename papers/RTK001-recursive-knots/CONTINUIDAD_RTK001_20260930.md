# RTK001 — Continuidad interna, 30/09/2026 (actualizada 03/10/2026, ronda 1 aplicada)

Documento de trabajo interno. No incorporar al manuscrito ni a entregas institucionales.

## Proyecto y alcance
Línea RTK001, "Geometría de nudos recursivos" / "Geometry of recursive knots", área Matemáticas y estructuras, estado en el CV web: en pausa. Ficha pública: exploración de nudos anidados y de la longitud necesaria para representarlos como tubos sin autointersección; objetivo: construir configuraciones factibles y evaluar qué puede afirmarse sobre sus cotas y optimalidad; hallazgo declarado: hay una cota superior factible para una configuración de profundidad uno; alcance: no se certifica estacionariedad ni optimalidad, y no hay ley de flujo recursiva general.

## Supuesto central (verificar con el autor)
**No existe ningún manuscrito previo de esta línea.** Todo lo que sigue se reconstruyó de la ficha:
1. Qué es un "nudo recursivo": se fijó la familia de cables iterados por desplazamiento en el marco (Definición 2.1 del manuscrito): K_0 círculo de radio 1; K_d(t) = K_{d−1}(t mod 2π) + r_d [cos θ N + sin θ B], θ = q_d t/p_d + φ_d, t ∈ [0, 2π p_d), gcd(p_d, q_d) = 1, con (N, B) marco de Bishop de K_{d−1} cerrado por un giro lineal, y K_{d−1} reparametrizada a periodo 2π. Por defecto (p, q) = (2, 3), φ = 0.
2. Qué significa "longitud necesaria": ropelength L/grosor, con grosor en el sentido de Litherland–Simon–Durumeric–Rawdon / Gonzalez–Maddocks.
3. Qué era la "cota superior factible de profundidad uno": se interpreta como una configuración explícita con grosor positivo; aquí se da para profundidades 1, 2 y 3 como polígonos explícitos con grosor poligonal medido.
4. La elección r_d = f · τ_{d−1} (fracción del grosor previo) y la malla f ∈ {0.25, 0.35, 0.5, 0.6} son decisiones de esta sesión.

## Qué se produjo (todo en `papers/RTK001-recursive-knots/`)
1. `PLAN.md`, escrito antes que cualquier código.
2. `experiments/recursive_knots.py` (numérica determinista), `experiments/shrink.py` (sonda opcional) y `experiments/make_numbers.py` (macros LaTeX). Ningún número del manuscrito está escrito a mano.
3. Manuscrito `manuscript/main.tex` (inglés; v0.1: 10 páginas a 11 pt, 10 referencias; v0.2: 11 páginas a 10 pt, 12 referencias) compilado a `main.pdf` sin errores ni referencias/citas indefinidas (v0.2 sin cajas desbordadas).
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
- Constantes teóricas (c = 1/2, (2,3)): γ = min(1 − f, f/2), A = 2(1 + f) + 4f; f = 1/2: γ = 0.25, A = 5, Λ = 20; cotas condicionales 2πΛ^d = 126 / 2513 / 50265 frente a los valores medidos 38.4 / 155.6 / 622.7 (cadenas con r_d distintos: comparación solo indicativa).
- Writhe de K_1: 3.127 / 3.257 / 3.518 / 3.710 (f = 0.25 / 0.35 / 0.5 / 0.6) → número de enlace del marco 3 / 3 / 4 / 4 → K_2 = cable (2, 9) / (2, 9) / (2, 11) / (2, 11) del trébol; K_3 = cable (2, 33) / (2, 33) / (2, 39) / (2, 39) de K_2. El caso f = 0.5 se decide por un margen de 0.02 en el writhe (estable al duplicar N, pero estrecho).

## Lo que NO se afirma
- No se certifica el grosor suave de ninguna curva: τ es un proxy poligonal (pares de vértices, test de mínimo local). La evidencia es la estabilidad en N y la coincidencia con τ_pt.
- La cota inferior del grosor de K_d está demostrada solo en parte (v0.2, Teorema 3.10): pares en hebras distintas (p = 2) con c_1 ≥ 0.61 en toda la familia (2,3) con f ≤ 1/2; curvatura y misma hebra solo bajo (H_3) (cotas de |K'|' y |κ'| de la base), con constantes medidas en los polígonos para d ≥ 2; en f = 1/2 el caso misma hebra da c_0 = 0.32/0.13/0.16 < 1/2. Lo restante es la hipótesis (H_c) **sobre la familia** (la versión de v0.1, para una base arbitraria, era falsa: Obs. 3.11). La recursión Rop_d ≤ 2πΛ^d es condicional a (H_c).
- No se afirma estacionariedad, optimalidad ni ley de flujo recursiva; f no se optimizó.
- La única cota inferior nueva es interna a la familia (Prop. 3.5: thick(K_d) ≤ r_d para p = 2, luego Rop(K_d) ≥ L(K_d)/r_d ≥ 2π(p(1−f)/f)^d); para el tipo de nudo se citan Buck–Simon (Rop ≥ c_0 Cr^{3/4}) y Cantarella–Kusner–Sullivan; el número de cruces de los cables iterados no se conoce en general.
- "τ_d = r_d para f pequeño" es conjetura; el cociente límite Rop_d/Rop_{d−1} → p/f (4.0 en f = 1/2) es consecuencia de esa conjetura y de L_d/L_{d−1} → p, no una constante empírica independiente (v0.1 lo presentaba como tal; corregido en la ronda 1).

## Bibliografía: grado de certeza
Seguras: Buck–Simon 1999 (Topology Appl. 91, 245–257); Cantarella–Kusner–Sullivan 2002 (Invent. Math. 150, 257–286); Litherland–Simon–Durumeric–Rawdon 1999 (Topology Appl. 91, 233–244); Gonzalez–Maddocks 1999 (PNAS 96, 4769–4773); Bishop 1975 (Amer. Math. Monthly 82, 246–251); Călugăreanu 1961 (Czechoslovak Math. J. 11, 588–625); White 1969 (Amer. J. Math. 91, 693–728); Fuller 1971 (PNAS 68, 815–819); Lickorish 1997 (GTM 175). Verificadas en línea por el árbitro (ronda 1): Buck–Simon, CKS (DOI añadido), LSDR, Pierański 1998 (DOI 10.12921/cmst.1998.04.01.09-23 añadido). **Coherentes pero no verificadas en línea:** Gonzalez–Maddocks, Bishop, Călugăreanu, White, Fuller, Lickorish (la cita de capítulo para la convención de cable se retiró; la convención se enuncia autocontenida), y la entrada nueva Fenchel 1929 (Math. Ann. 101, 238–252). La cita del valor ≈ 32.7 para el ropelength del trébol es al conocimiento numérico de la literatura (Pierański; CKS lo mencionan), no a un teorema; no se añadió Ashton–Cantarella–Piatek–Rawdon 2011 por no poder verificarla. Rawdon 2003 se cita ahora en §2.4; Chern 1967 se eliminó.

## Próximos pasos concretos
1. Cerrar (H_c) para la familia: (a) en d = 1, cálculo explícito y certificable de la distancia mínima entre hebras de T(p,q) sobre el toro (1, r) (el par crítico en f = 1/2 cruza el agujero del toro, no es un par local); (b) caso misma hebra en f = 1/2: afinar la cota de curvatura usando la expresión exacta de |K_d' × K_d''| con el ángulo ψ en vez de κ_⊥² + κ_W² = κ²; (c) acotar sup|v'| y sup|κ'| de K_d en función de los de K_{d−1} para que (H_3) sea uniforme en d; (d) p ≥ 3.
2. Certificar τ con aritmética de intervalos sobre un interpolante C^{1,1} (arcos circulares), para pasar de "verificado numéricamente" a "demostrado" en profundidad 1 (y quizá 2); sustituir el writhe de punto medio por el writhe poligonal exacto (Levitt; Klenin–Langowski).
3. Sustituir la sonda de acortamiento por una minimización de longitud con restricción τ ≥ 1 (gradiente de ropelength o recocido, con comprobación certificada del tipo de nudo) en d = 1, 2, para medir cuán lejos está la familia de configuraciones ajustadas (trébol: 38.4 frente a ≈ 32.7). El acortamiento simple no sirve (empeora K_2).
4. Optimizar f_d por profundidad y parametrizar el patrón en longitud de arco; probar φ_d ≠ 0.
5. Atar una cota inferior a cada configuración concreta cuando se conozca el número de cruces del cable identificado por el Lema 3.2 (p. ej. cable (2, 11) del trébol).
6. Segunda ronda de revisión interna sobre v0.2 (la primera, del 30/09/2026, está aplicada: véase la sección siguiente).

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

**Qué queda abierto tras la ronda 1:** (i) caso misma hebra de (H_c) en f = 1/2 (constantes demostradas 0.32/0.13/0.16) y constante de curvatura a priori en f = 1/2, d = 2 (0.49); (ii) uniformidad en d de (H_3); (iii) p ≥ 3 no tratado en la parte demostrada; (iv) las constantes del Teorema 3.10 distintas de c_1(1/2, 2/3) ≥ 1/2 son ínfimos en malla con corrección Lipschitz estimada, no aritmética de intervalos; (v) writhe poligonal exacto no implementado; (vi) certificación del grosor poligonal; (vii) bibliografía: 7 entradas coherentes pero no verificadas en línea (listadas arriba).
