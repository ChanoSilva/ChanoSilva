# Respuesta del autor — LMI001, ronda 2 de revisión interna (03/10/2026)

Informe atendido: `REFEREE_LMI001_ronda2_20261003.md` (veredicto: cambios mayores, solo de texto; 0 bloqueantes, 3 mayores, 15 menores, más 6 puntos de la ronda 1 aplicados a medias o con error nuevo). Manuscrito resultante: **v0.3** (3 October 2026).

Documento escrito de forma incremental durante la sesión; el estado final de cada punto está en su fila.

## Resumen

(se completa al final)

## Plan de trabajo (orden de aplicación)

1. Verificación bibliográfica con WebSearch de hofmann1997, roth2003, sejdinovic2013, franca2021 y de la fecha del TR-04-25 de Dhillon–Guan–Kulis.
2. Atribución (M1, M2, m2, m3): *Status*, Tabla 3, resumen, Introducción, README, ficha.
3. Alcance del Teorema 4.1 (M3, m13) y Introducción (main.tex:65).
4. Menores m1, m4–m15 y los residuos de la ronda 1.
5. Extensión: ≤ 12 páginas sin perder demostraciones.
6. Compilación, revisión visual, nota de continuidad, README, ficha.

## Respuesta punto por punto

(en construcción)

### Verificación bibliográfica (hecha en esta sesión, con WebSearch; arXiv, PMC, Europe PMC, people.bu.edu y otros espejos están bloqueados por el proxy, así que la verificación es de datos bibliográficos y de resúmenes, no de texto completo)

| Clave | Datos verificados | Fuente de la verificación |
|---|---|---|
| `hofmann1997` (nueva) | T. Hofmann, J. M. Buhmann, "Pairwise data clustering by deterministic annealing", IEEE TPAMI 19(1):1–14, 1997 | WebSearch (índices bibliográficos) |
| `roth2003` (nueva) | V. Roth, J. Laub, M. Kawanabe, J. M. Buhmann, "Optimal cluster preserving embedding of nonmetric proximity data", IEEE TPAMI 25(12):1540–1551, 2003 | WebSearch (IEEE Xplore doc. 1251147; resumen: invariancia del coste de *pairwise clustering* bajo desplazamientos constantes y preservación completa de la estructura de clústeres en la *constant shift embedding*) |
| `sejdinovic2013` (nueva) | D. Sejdinovic, B. Sriperumbudur, A. Gretton, K. Fukumizu, "Equivalence of distance-based and RKHS-based statistics in hypothesis testing", Ann. Statist. 41(5):2263–2291, 2013, doi 10.1214/13-AOS1140 | WebSearch (Project Euclid, ORA Oxford) |
| `franca2021` (nueva) | G. França, M. L. Rizzo, J. T. Vogelstein, "Kernel k-groups via Hartigan's method", IEEE TPAMI 43(12):4411–4425, 2021, doi 10.1109/TPAMI.2020.2998120 | WebSearch (doi.org, PubMed 32750776, PMC8715390). Texto completo no accesible: no pude cotejar si enuncian la inclusión de la Prop. 3.5(ii). |
| `dhillon2004tr` → `dhillon2005tr` | UTCS Technical Report TR-04-25, fechado el 18 de febrero de 2005 (reconfirmado en esta sesión con los mismos dos índices que usó el árbitro; no pude abrir el PDF) | WebSearch (cabecera del PDF de people.bu.edu vía buscador; Bibsonomy). Clave renombrada, `year = 2005`, nota con la fecha. |

No añadí Li & Rizzo (2017, *k-groups*, solo arXiv) porque `franca2021` cubre lo que se le atribuiría y no pude verificar el texto.
