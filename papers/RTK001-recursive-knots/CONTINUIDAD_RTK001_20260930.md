# RTK001 — Continuidad interna, 30/09/2026

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
3. Manuscrito `manuscript/main.tex` (inglés, 9 páginas, 10 referencias) compilado a `main.pdf` sin errores ni referencias/citas indefinidas (un aviso de caja horizontal desbordada en el apéndice, de 17 pt, en una línea con nombres de archivo en monoespaciado).
4. README, esta nota y la propuesta de ficha.

## Decisiones tomadas
- **Grosor poligonal.** τ = min(minRad, dcsd/2), con minRad el circunradio mínimo de ternas consecutivas y dcsd la distancia mínima entre pares de vértices doblemente críticos (mínimo local de la distancia en ambos índices; se mantiene la diagonal D_ii = 0 en el test, lo que excluye automáticamente pares casi diagonales). La primera versión usaba "distancia mínima entre segmentos no adyacentes", que tiende a la longitud de arista cuando N crece (segmentos i e i+2 están a una arista de distancia) y es inservible; se descartó antes de correr nada.
- **Contraste independiente.** τ_pt = min sobre pares de vértices del radio punto–tangente de Gonzalez–Maddocks; coincide con τ al 0.01 % en todos los niveles.
- **Sin interpolación.** K_d se evalúa en los vértices de K_{d−1} (N_d = p_d N_{d−1}); el parámetro t es el índice de vértice, por lo que el ángulo del patrón avanza uniformemente en t y no en longitud de arco (la ficha no lo especifica; se declara en el manuscrito).
- **Marco de Bishop discreto.** Transporte paralelo vértice a vértice (rotación de Rodrigues que lleva T_i a T_{i+1}), holonomía α medida como ángulo con signo y eliminada con el giro −α i/N. Se comprobó numéricamente que α = 2π·frac(Wr K_{d−1}) (p. ej. α_2 = −3.027 para f = 0.5 con Wr(K_1) = 3.518), como exige Călugăreanu–White–Fuller.
- **Término de giro en la cota de longitud.** La fórmula sugerida "L_d ≤ p L_{d−1}(1 + r κ) + 2π q r" omite el giro de cierre; se añadió el término p|α| r ≤ π p r (Lema 3.3). Con él, la cota se cumple en 36 de 36 niveles medidos.
- **Constante c de la hipótesis (H_c).** Se define ρ_d = min(τ_{d−1} − r_d, c r_d sin(π/p_d)) y se usa c = 1/2 en el texto y en las tablas. Una primera versión del código calculaba, por error de convención, la variante c = 1 bajo el nombre "c = 1/2"; se corrigió y ahora el JSON guarda ambas (`rho_pred` con c = 1/2, `rho_pred_cone` con c = 1). Resultado: con c = 1/2 la desigualdad se cumple con margen ≥ 1.66 en los 9 niveles por defecto con f ≤ 1/2; con c = 1 falla exactamente en (f = 1/2, d = 1), cociente 0.83.
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
- No se demuestra la cota inferior del grosor de K_d en el caso local (hebras sobre un tubo curvado) ni la cota de curvatura de K_d: es la hipótesis (H_c). La recursión Rop_d ≤ 2πΛ^d es condicional a (H_c).
- No se afirma estacionariedad, optimalidad ni ley de flujo recursiva; f no se optimizó.
- No se deriva ninguna cota inferior nueva: se citan Buck–Simon (Rop ≥ c_0 Cr^{3/4}) y Cantarella–Kusner–Sullivan; el número de cruces de los cables iterados no se conoce en general.
- Los valores de Λ_* ≈ 4.0 y "τ_d = r_d para f pequeño" son conjeturas.

## Bibliografía: grado de certeza
Seguras: Buck–Simon 1999 (Topology Appl. 91, 245–257); Cantarella–Kusner–Sullivan 2002 (Invent. Math. 150, 257–286); Litherland–Simon–Durumeric–Rawdon 1999 (Topology Appl. 91, 233–244); Gonzalez–Maddocks 1999 (PNAS 96, 4769–4773); Bishop 1975 (Amer. Math. Monthly 82, 246–251); Călugăreanu 1961 (Czechoslovak Math. J. 11, 588–625); White 1969 (Amer. J. Math. 91, 693–728); Fuller 1971 (PNAS 68, 815–819); Lickorish 1997 (GTM 175). **Por verificar:** Pierański 1998, "In search of ideal knots", Comput. Methods Sci. Technol. 4, 9–23 (existe el artículo; volumen y páginas no reverificados). La cita del valor ≈ 32.7 para el ropelength del trébol es al conocimiento numérico de la literatura (Pierański; CKS lo mencionan), no a un teorema. La entrada Rawdon 2003 (Experimental Math. 12, 287–302) y Chern 1967 están en `refs.bib` pero no se citan en el texto.

## Próximos pasos concretos
1. Demostrar (H_c) con constantes explícitas: para p = 2, analizar el par antipodal sobre un tubo curvado usando (5) y su derivada; controlar κ(K_d) ≤ 1/ρ_d.
2. Certificar τ con aritmética de intervalos sobre un interpolante C^{1,1} (arcos circulares), para pasar de "verificado numéricamente" a "demostrado" en profundidad 1 (y quizá 2).
3. Sustituir la sonda de acortamiento por una minimización de longitud con restricción τ ≥ 1 (gradiente de ropelength o recocido, con comprobación certificada del tipo de nudo) en d = 1, 2, para medir cuán lejos está la familia de configuraciones ajustadas (trébol: 38.4 frente a ≈ 32.7). El acortamiento simple no sirve (empeora K_2).
4. Optimizar f_d por profundidad y parametrizar el patrón en longitud de arco; probar φ_d ≠ 0.
5. Atar una cota inferior a cada configuración concreta cuando se conozca el número de cruces del cable identificado por el Lema 3.2 (p. ej. cable (2, 11) del trébol).
6. Revisión arbitral interna independiente del borrador v0.1 (no se hizo en esta sesión por presupuesto de tiempo).
