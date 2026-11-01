# Lot 6c RTX : essais récents d'Estes (Key Studies 2025, rubrique « Recent ») comparés au référentiel (01/11/2026)

Règle : une fiche ou une correction n'entre que si l'article est dans la Bibliothèque (`~/Downloads/Bibliothèque Onco360/Radiothérapie`).
Key Studies : 784 essais (hors pédiatrie, lymphome, pharmacologie) ; 159 déjà cités par le référentiel. Bibliothèque : dossiers comparés aux localisations.

## Fait
- **Rein (localisation neuve)** : stéréotaxie du cancer du rein primitif, 26 Gy / 1 fx (≤ 4 cm) et 42 Gy / 3 fx (4 à 10 cm), d'après FASTRACK II
  (Lancet Oncol 2024), IROCK à 5 ans (Lancet Oncol 2022), consensus IROCK (2016). Les contraintes de FASTRACK II sont dans l'annexe de
  l'article, absente de la Bibliothèque : base de contraintes appliquée. Diagnostic « Cancer du rein » relié.

## Essais récents qui touchent le référentiel, article absent de la Bibliothèque (à télécharger pour corriger la fiche)
| Fiche | Essai | Ce qui changerait |
|---|---|---|
| Méningiome grade 2 | ROAM (Lancet 2026) | 60 Gy après exérèse complète : DFS 80 vs 64 % |
| Métastases cérébrales, cavité | ALLIANCE A071801 (ASTRO 2026) | Cavité en 27 Gy / 3 fx ou 25 Gy / 5 fx plutôt qu'en séance unique |
| CBPC étendu | TREASURE (JAMA Oncol), Gronberg (ASCO 2026) | RT thoracique sous immunothérapie : pas de bénéfice, plus de toxicité |
| CBPC, encéphale | MAVERICK, NRG CC009 (ASTRO 2026) | Surveillance IRM au lieu de l'IPC ; SRS au lieu de l'encéphale in toto |
| Vessie | BART (IJROBP 2024) | RT adjuvante après cystectomie 50,4 Gy / 28 fx (situation absente) |
| Sein, reconstruction | RT CHARM (JCO 2026), FABREC (JAMA Oncol 2024) | 42,56 Gy / 16 fx sur paroi reconstruite |
| ORL | UPGRADE-RT (JCO 2025), NRG HN-005 | Aires électives 43 Gy ; 60 Gy dans l'oropharynx HPV+ non retenu |
| Vésicule biliaire | POLCAGB (ASCO 2025) | RCT néoadjuvante 55–57 Gy / 25 fx |
| Vulve | GOG 279 (JCO 2024) | RCT néoadjuvante 64 Gy |
| Foie, palliatif | CCTG HE1 (Lancet Oncol 2024) | 8 Gy / 1 fx sur le foie douloureux |
| Prostate, boost | GETUG P05 (ASTRO 2026) | Boost de curiethérapie vs 80 Gy externe : même contrôle, plus de toxicité urinaire |
| Peau (épidermoïde) | C-POST (NEJM 2025) | Cémiplimab après la RT adjuvante |
| Sein, aires ganglionnaires | NSABP B-51 (NEJM 2025), SUPREMO (NEJM 2025) | Pas de bénéfice de l'irradiation ganglionnaire si ypN0 ; PMRT intermédiaire |

## Dans la Bibliothèque, à intégrer au prochain lot
STAR-TREC (rectum, préservation d'organe), STELLAR (rectum 25 Gy / 5 fx + chimiothérapie), LORD-KNEA (gonarthrose 3 Gy / 6 fx),
Côlon et Ovaire (un article chacun, sans localisation dans le référentiel).

## Lot 6d (01/11/2026)
- **Rattrapage de la prostate** : COPORT = NRG-GU003, déjà présent (62,5 Gy / 25 fx) ; complété avec le protocole (contraintes du bras HYPORT,
  simulation, PTV 7–10 mm). SHARE ajouté : 65 Gy / 26 fx (protocole version 1.8). SPPORT était déjà présent.
- **Tous les onglets des Key Studies** croisés avec la Bibliothèque (auteur et année, 1 098 PDF) : `estes-key-studies-croisement.tsv`
  (868 essais hors pédiatrie et lymphomes ; colonne « Article dans la Bibliothèque » = fichier trouvé, à confirmer à l'ouverture).
- **Onglet Essais** : 139 fiches ajoutées pour les sources qui n'y étaient pas (contraintes de dose, jeux de contraintes, contourage,
  définitions des organes à risque, atlas des volumes ; `essais_sources.py`) ; 17 complétées d'après Estes (NRG BR002, RTOG 0126, PREMER…).
  Les sources des contraintes venues de RadOncCalc n'ont que leur nom (ni revue ni année ajoutées). 8 lignes de contraintes ont pour source
  « Source à préciser » et 12 « Pratique usuelle ».
