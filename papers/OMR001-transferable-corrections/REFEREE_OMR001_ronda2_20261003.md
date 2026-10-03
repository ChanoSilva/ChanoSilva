[EN CURSO]

# Informe de árbitro interno — OMR001, ronda 2 (03/10/2026)

Árbitro nuevo, independiente del de la ronda 1. Material revisado: carpeta `papers/OMR001-transferable-corrections/` en su estado actual (v0.2, commit `2040e2b`): `manuscript/main.tex` (381 líneas; las referencias `l.N` son a ese archivo salvo que se indique otro), `numbers.tex`, `table_*.tex`, `refs.bib`, `experiments/*.py`, `results/results.json`, `results/tables.md`, `README.md`, `FICHA_OMR001_propuesta.md`, `CONTINUIDAD_OMR001_20260930.md`, el informe y la respuesta de la ronda 1. Versión anterior: `git show c51bd2e:…` (solo lectura). Trabajo auxiliar en `scratchpad/referee2_OMR001/` (`check_cor43.py`, `check_sharp_cap.py`, `check_kappa_bound.py`, `check_macros.py` y sus `.out`). No se modificó nada de la carpeta salvo este informe.

## Veredicto

(pendiente)

## Verificación de la ronda 1

| Hallazgo | Estado | Evidencia |
|---|---|---|
| B1 (cierre no demostrado) | aplicado bien | `main.tex` l.248 (párrafo "What this says about the line's conclusion": "is a decision this note does not take"); l.72; frase "established rather than merely prudent" ausente (grep). Ficha l.11/l.22: "Nota técnica (borrador v0.2…); línea en pausa salvo (a)–(b)". README l.5 reescrito. Paso (d) sigue abierto en l.358. |
| B2 (Prop. de optimalidad falsa tal como estaba) | aplicado con error nuevo | La Prop. 4.5 (l.201) está bien cualificada. Pero el resumen (l.63: "the rate $m^{-1/2}$ cannot be improved uniformly over operators") y la tabla de afirmaciones (l.342: "harm not $o(m^{-1/2})$ uniformly over operators") la parafrasean como afirmación de **tasa absoluta**, que la demostración no prueba y que el Corolario 4.3 nuevo contradice en el régimen de esa demostración. Ver M1. |
| M1 ($m$ confundido con $\tau$) | aplicado bien | `safe_reversion.py` l.287–296 (`tau2_fixed`); `results.json`: los 8 registros del barrido en $m$ tienen `tau2`=0.020833 y `tau2_fixed_at_m`=12; "always" con todos los datos 0.0482/0.0481/0.0477/0.0480 y SURE 0.0561/0.0558/0.0554/0.0556 ($\kappa=0$), planos en $m$. Filas de $m=12$ idénticas a v0.1 y barridos de estructura y desviación idénticos (diferencia máxima 0 en todos los riesgos), como dice la respuesta. Los números del texto (l.320) son los de la corrida nueva (verificado: `MThreeZeroRevGain` +3.1 %, `MThreeEightRevGain` −17.9 %, `MThreeEightExcess` +0.0104, `MThreeEightBoundPhi` 0.1146, `MTwentyFourZeroRevGain` −25.0 %, `MTwentyFourEightRevGain` −68.8 %, todos recomputados desde el JSON). |
| M2 (cota $\varphi$ no uniforme en $\theta$) | aplicado bien (con una mejora pendiente, M2 nuevo) | l.127, leyenda de la Fig. 1 (l.305), Corolario 4.3 (l.171–186). La demostración es correcta paso a paso (ver "Corolario 4.3" abajo) y mi verificación independiente la confirma. |
| M3 (25 % respecto de qué) | aplicado a medias | Bien en Cor. 4.4 (l.193), resumen (l.63), l.320, tabla de afirmaciones (l.341), README l.35, CONTINUIDAD l.34. Queda sin referente en l.253 ("a \SplitCost{} split cost"): ver m1. |
| M4 (ficha, tres imprecisiones) | aplicado con error nuevo | (1) y (2) bien (ficha l.13, l.24). (3) "la probabilidad de usar la corrección **cuando** su pérdida realizada supera la de la referencia es ≤ α·P(Δ>0)" se lee como probabilidad condicional, y así usa "when" el propio manuscrito (l.317: "the conditional frequency of using $C$ when it is harmful"); con esa lectura la cota es falsa en la simulación. Ver M3. |
| M5 (cambio a posteriori no declarado) | aplicado a medias | Apéndice A l.364 y docstring l.23–25 declaran el cambio $z$→Poisson. Pero l.364 añade "nothing else was changed after seeing results", que ya no es cierto en v0.2: el protocolo del barrido en $m$ se cambió y se rehízo tras ver los resultados (M1) y la marca "borderline" con margen de 2 puntos se definió después de ver qué casos estaban cerca del umbral (m9). Ver m2. |
| M6 (extensión) | aplicado bien | PDF de 10 páginas (recompilado, ver "Verificación computacional"); recortes 1–6 aplicados; tablas de verificación en `results/tables.md` T1–T4. |
| m1 (aleatorización, riesgo infinito) | aplicado bien | l.105, l.117. |
| m2 ($\E\norm{b}^2<\infty$) | aplicado bien | l.108, l.116. |
| m3 (independencia falla en refit) | aplicado bien | l.253. |
| m4 (empates) | aplicado bien | l.222 "resolved toward $C$ as in Definition 2.1(c)"; coherente con l.93 y con `Dhat <= -z*s` (script l.202). |
| m5 (Obs. 4.5) | aplicado bien | l.208. |
| m6 (Obs. 3.2) | aplicado bien | l.122. |
| m7 (constante del regret) | aplicado con error nuevo (menor) | l.168: "the exact conditional value is $s\sup_{u\ge0}u\Phi(z-u)$" es incorrecto: el valor condicional exacto es $s\,u\Phi(z-u)$ en el $u$ realizado; el supremo es su cota. Ver m3. |
| m8 (fila SURE) | aplicado bien | l.238. |
| m9 (casos en el filo) | aplicado bien | marcas $^{\mathrm u}$ en `table_structure.tex`; l.320 enumera los 4 casos (\BorderlineList coincide con el JSON). |
| m10 (identidad vs cota) | aplicado bien | l.317. |
| m11 (±0.0003/±0.0002) | aplicado bien | CONTINUIDAD l.36 "+0.0042 ± 0.0002 (EE 0.00025)"; `table_departure_check.tex` ±0.0002. |
| m12 (intervalo de $\kappa$) | aplicado bien | l.364. |
| m13 (capítulo de Devroye et al.) | aplicado con matiz (correcto) | l.228 "\S 8.4; see also Ch. 22". Ver Bibliografía. |
| m14 (resumen ≤200 palabras) | aplicado bien | 215 palabras en la fuente LaTeX (≈200 en el PDF), una sola cifra. |
| m15 (cajas desbordadas, Tabla 1) | aplicado bien | columnas `L{}` (l.15, l.232); 0 "Overfull" en mi recompilación. |
| m16 | sin acción | — |

Recuento: 17 aplicados bien (incluido m13 con matiz; m16 no pedía acción y no se cuenta), 2 a medias (M3, M5), 4 aplicados con error nuevo (B2, M4, m7 y, en grado menor, M2 queda bien pero mejorable). Detalle en los hallazgos nuevos.

## Corolario 4.3 (cota uniforme): verificación paso a paso

(en curso)

## Hallazgos nuevos

(en curso)

## Bibliografía

(pendiente)

## Verificación computacional

(pendiente)

## Lista final de acciones

(pendiente)
