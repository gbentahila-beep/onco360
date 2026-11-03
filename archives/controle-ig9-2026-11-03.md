# Contrôle IG9 du 03/11/2026 : mesures de l'interface avant / après la phase IG

Étape 8 de l'audit UX / UI du 02/11/2026. Outil : `outils/mesures-ui.py` (depuis `tests/`), jeu de test **fictif**, 14 pages de l'audit
(tableau de bord, agenda, salle d'attente, patients, dossier, documents, tâches, RCP, protocoles, radiothérapie, outils, bilan, paramètres, profil),
4 largeurs (390, 900, 1 280, 1 600 px), médecin ; secrétaire et infirmière à 1 440 px (5 pages chacune).

- **Avant** : commit 900e066 (audit du 02/11, avant IG1), servi à part ; Chrome seulement (l'ancienne version reste bloquée dans Safari pendant la mesure).
- **Après** : version du 03/11 (IG1 à IG9), Chrome ; et une seconde mesure complète Chrome **et** Safari.
- Captures : `captures-ig9/avant/`, `captures-ig9/chrome-apres/`, `captures-ig9/apres/` (Chrome 390 et 1 600 px, Safari 1 280 px ; dossier non versionné).

## Variantes comptées (Chrome, mêmes pages, mêmes largeurs)

| Mesure | Avant | Après | |
|---|---|---|---|
| Boutons (fond, texte, cadre, arrondi, hauteur, taille, graisse) | 106 | 94 | −12 |
| Hauteurs de bouton différentes | 31 | 29 | −2 |
| Couleurs de cadre de bouton | 10 | 9 | −1 |
| Badges et compteurs | 19 | 15 | −4 |
| Cartes | 2 | 2 | = (carte de page, cadre intérieur : la règle) |
| Ombres | 16 | 16 | = |
| Arrondis | 12 | 12 | = |
| Couleurs de texte | 21 | 20 | −1 |
| Polices (famille, taille, graisse) | 36 | 35 | −1 |
| Débordements en largeur, erreurs JavaScript | 0 | 0 | |

Part des boutons aux trois hauteurs du guide (36 / 40 / 44 px) : **36 % → 41 %** ; boutons de moins de 32 px : **15 % → 12 %**.

Mesure complète Chrome + Safari (après) : 100 variantes de boutons, 15 de badges, 2 de cartes ; **0 débordement, 0 erreur JavaScript**,
aussi pour la secrétaire et l'infirmière.

## Ce que les chiffres disent

- La phase IG a réduit les variantes **sans refaire le design** (consigne « identité gardée ») : couleurs, cartes, ombres et arrondis n'ont pas bougé,
  comme prévu. Les gains sont sur les boutons (IG3 : secondaire blanc, 40 px en haut de page ; IG7 : boutons voisins de même taille au téléphone) et
  sur les badges (IG3 : compteurs en pastille).
- Le nombre reste élevé parce que la mesure compte chaque combinaison (une même sorte de bouton à 36 et à 40 px compte deux fois) et parce que
  beaucoup de « boutons » sont des lignes cliquables (cartes de protocole de 96 px, jours de l'agenda, onglets) : ce ne sont pas des écarts au guide.
- Ombres : 16 variantes, mais trois servent à 81 % des éléments (`--ombre`, ombre légère des cadres, anneau intérieur d'un badge) ; les autres sont des
  traits intérieurs de badge colorés (un par sens) : à regrouper si on reprend les badges.
- Arrondis : 8 px, 999 px (pastilles) et 50 % (ronds) dominent ; 14 px (cadres intérieurs) et 10 px restent à ramener à 12 / 8 px (petit lot possible,
  sans changement visible).

## Restes signalés (non corrigés, à décider)

1. Boutons de moins de 32 px (12 %) : petits boutons « mini » et flèches (la mesure ne note pas lesquels : à relever page par page) ; le guide demande 36 px dans une liste.
2. Arrondis 14 / 10 / 9 / 6 px (environ un tiers des éléments arrondis) à ramener à 12 / 8 px.
3. Badges : la pastille rouge des compteurs de menu est à 11 px (mention, pas une information : admis par le guide, § 3).

## Contrôle complet du 03/11/2026

`bash outils/avant-mise-en-ligne.sh --navigateur` : Chrome 85 tests réussis + 5 tests anciens à mettre à jour (ils vérifiaient la mise en page
d'avant IG5 à IG7 : case « Payé » du Bilan, flèches de tri dans les titres, filtres repliés au téléphone, dossier en deux colonnes sur tablette,
bouton « Fermer » du dossier) ; mis à jour, relancés : tous réussis. Safari : 90 tests réussis.
