# Lot 5 RTX : comparaison des protocoles avec les tables d'Estes (01/11/2026)

Sources de comparaison : « Rad Onc Tables – Oral Boards Estes 2026 » (colonnes Dose et Chemo) et « Rad Onc Tables – Key Studies Estes 2025 »
(Bibliothèque › Radiothérapie › Général). Les tables d'Estes servent de contrôle ; une correction n'est faite que si un article de la
Bibliothèque l'établit (script `docs/radiotherapie/construction/corrections_lot5.py`).

## Corrections faites
| Schéma | Avant | Après | Source |
|---|---|---|---|
| se-iia-30 (séminome IIA) | 30 Gy, fractions non précisées | 30 Gy / 15 fx de 2 Gy, 5 par semaine | Classen 2003 |
| se-iib-36 (séminome IIB) | 36 Gy, fractions non précisées | 36 Gy / 18 fx de 2 Gy | Classen 2003 |
| ep-g2-54 (épendymome grade 2) | 54 Gy, fractions non précisées | 54 Gy / 30 fx de 1,8 Gy | Wee 2020 (dose médiane) |
| ep-g3-594 (épendymome grade 3) | 59,4 Gy, fractions non précisées | 59,4 Gy / 33 fx de 1,8 Gy | Wee 2020 (dose médiane) |
| md-csi-352-552 (médulloblastome), craniospinal | 35,2 Gy, fractions non précisées | 35,2 Gy / 22 fx de 1,6 Gy | NOA-07 (Beier 2017) |

## Conformes à Estes (aucun écart de dose, de fractionnement ou de chimiothérapie)
Prostate (60/20, 70/28, 78/39, 36,25/5, 42,7/7, FLAME 77/35 + 95, POP-RT 68/25 + 50, LDR 145 / 110, HDR 27/2 et 15/1, loge 66–70 Gy),
vessie (55/20, 64/32, 5FU + mitomycine), séminome I (20/10, 30/15), col (45 Gy + HDR 7 × 4, 5,5 × 5, 6 × 5 ; cisplatine 40 mg/m²
hebdomadaire), endomètre (curiethérapie 7 × 3 à 5 mm, PORTEC-3), vulve (GOG 205 57,6/32), œsophage (CROSS 41,4/23, 50–50,4 Gy),
estomac (INT-0116 45 Gy), pancréas (PREOPANC 36/15, SMART 50/5, 50,4/28), foie, rectum (25/5, 50/25, 50,4/28, RAPIDO, PRODIGE 23),
canal anal (RTOG 0529 42 / 50,4 / 54 Gy), ORL (70/35, 66/33 post-opératoire, cisplatine), poumon (60/30, stéréotaxie 54/3, 48/4,
50/5, PORT 54/27, CBPC 45/30 bifractionné, 66/33, 30/10 étendu, PCI 25/10), mésothéliome (50 + 60 Gy), thymome (50–54 Gy, 60 Gy
macroscopique), sein (40/15, 26/5, 28,5/5 hebdomadaire, 50/25, SIB IMPORT HIGH 48/40/36 en 15 fx, IPB 40/15 et 30/5, complément
10–16 Gy), glioblastome (60/30, 40/15, 34/10, 25/5), gliomes (50,4–54 Gy, 59,4/33), méningiome, hypophyse, craniopharyngiome,
sarcome des membres (50/25, complément 10–16 Gy post-opératoire).

## Écarts relevés, non corrigés
- **Médulloblastome, complément de la fosse postérieure** : la fiche donne 20 Gy (cumul 55,2 Gy, HIT 2000) ; NOA-07 (Beier 2017, de la
  même fiche) donne un complément en 1,8 Gy jusqu'à 55 Gy (soit 19,8 Gy / 11 fx). L'article HIT 2000 n'est pas dans la Bibliothèque :
  laissé tel quel.
- **PORTEC-3** : Estes écrit « cisplatine J1 et J29 » ; l'essai PORTEC-3 donne le cisplatine les semaines 1 et 4 (fiche juste).
- **Sarcome du rétropéritoine** : Estes ne recommande pas de RT préopératoire (« 0 Gy », d'après STRASS) ; la fiche cite déjà le
  résultat négatif de STRASS dans ses points d'attention.
- **Doses non chiffrées** (curiethérapie après RT externe) : CTV-HR du vagin (vagin-rch-curie) et complément tumoral de la vulve
  (vulve-excl-curie) ; aucune dose dans les articles de la Bibliothèque pour ces schémas.
- **Fractions non précisées** (« selon le centre ») : Merkel 50 et 56 Gy, peau 60–70 Gy ; aucun article de la Bibliothèque ne fixe le
  nombre de séances.
