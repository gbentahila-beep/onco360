# Audit UI (étape 2, 02/11/2026) : couleurs, typographie, composants, mise en page, écrans

Cadre : identité gardée (bleu Onco360, Montserrat + Roboto, mêmes pages). On ne change pas l'allure : on réduit le nombre de variantes
et on corrige ce qui gêne la lecture. Mesuré sur la copie de test (jeu fictif), 14 pages, à 900 et 1 600 px (Chrome) et 1 440 px (Safari / WebKit),
en plus des mesures à 390 et 1 440 px de l'audit UX. Rien modifié dans le code.

## Chiffres de départ
| Élément | Variantes mesurées à l'écran | Cible proposée (guide de style) |
|---|---|---|
| Boutons (fond, texte, bordure, arrondi, hauteur, taille, graisse) | 77 | 4 sortes × 3 tailles |
| Hauteurs de bouton | 27 (19 à 165 px) | 36 / 40 / 44 |
| Couleurs de bordure de bouton | 11 | 2 (pâle, bleue) |
| Badges et pastilles | 15 | 2 formes (état, compteur) |
| Cartes (arrondi, ombre, bordure, marge) | 12 | 2 (carte, sous-cadre) |
| Ombres | 16 | 3 (carte, menu, fenêtre) |
| Arrondis | 14 (6 à 20 px, 999 px, rond) | 3 + rond |
| Couleurs de texte | 22 | 8 (encre, doux, bleu, blanc + 4 états) |
| Police / taille / graisse | 37 | ~10 |
| Couleurs écrites dans le code | 151 (v2.html) + 71 (js/app) | variables seulement |

Aucun débordement horizontal à 900 et 1 600 px. Safari : même rendu que Chrome sur les 14 pages (polices chargées, pas de décalage vu).

## Couleurs
- U1 (Moyenne) Une même signification a plusieurs teintes : 4 bleus de texte (#3563B0, #107ACA, #045FAE, #2F5597), 4 verts, 5 rouges, 3 orangés.
  Ça ne se voit pas page par page mais donne un léger flou d'ensemble. → une seule teinte par sens, en variables.
- U2 (corrigé le 02/11) Pastilles d'état mesurées à l'écran : 5,2 à 6,0 pour 1 (gris 5,76, rouge 6,05, vert 5,21, bleu 5,77, ambre 5,24) : bon.
  Seul le compteur gris #55607A sur #C9D9E8 est à 4,36 pour 1 (sous 4,5) → réglé par la fiche « Compteurs d'une seule forme » (lot 2, idée 14).
- U3 (Moyenne) Champs et menus déroulants bordés de #294056 (presque la couleur du texte, 10 pour 1) alors que les cartes ont une bordure à peine
  visible (#C9D9E8 sur le fond, 1,3 pour 1) : les champs paraissent lourds, les cartes flottent. → bordure de champ moyenne (≈ 3 pour 1), plus
  foncée au survol, bleue au clic.
- U4 (retiré le 02/11) Le rouge de « prévue le … » (À valider par le médecin) ne marque que les cures en retard (v2.js:1269) : il est justifié ;
  dans le jeu fictif toutes les cures sont en retard. Rien à changer.
- U5 (Faible) Jours hors du mois (mini-calendrier, RCP, Agenda › Mois) en #B9C0CE : 1,8 pour 1. → un peu plus foncé (3 pour 1), toujours discret.
- Correction : le gris-bleu #7599BD cité le 02/11 (2,98 pour 1) existe en variable mais n'est utilisé nulle part ; les textes « doux » sont en #294056,
  bien lisibles.

## Typographie
- U6 (Moyenne) 37 combinaisons : Roboto en 9 tailles (11 à 30 px) et 4 graisses (normal, moyen, demi-gras, gras) ; titres Montserrat en 10 tailles
  (13 à 26 px). Les variables `--t1` à `--t8` existent mais beaucoup de tailles sont écrites à la main. → 5 tailles de texte, 3 de titre, 3 graisses.
- U7 (Moyenne) Boutons en 3 graisses et 9 tailles : barre du dossier en gras 13 px, Actions rapides en moyen 14 px, onglets Radiothérapie en gras 14 px.
  → une graisse (moyen) et une taille par hauteur de bouton.
- Rappel (audit UX) : textes de 11-12 px (T3), étiquettes en MAJUSCULES (T4, T11).

## Composants
- U8 (Haute, détaille T2) Boutons : 77 variantes. Bordure pâle (64), bleue (23), foncée (« Décaler », ⋯, « Calendrier »), verte (Valider), verte
  WhatsApp, bleu nuit. Sur une même ligne de la Salle d'attente : « Calendrier » bordure foncée, « Actualiser » bordure bleue, ⋯ bordure foncée,
  « Rendez-vous » plein. → 4 sortes : principal (bleu plein), secondaire (contour), discret (sans cadre, ex. ⋯), danger (rouge) ; 3 hauteurs.
- U9 (Moyenne, complète T9) Onglets et choix en 4 styles : soulignés (dossier, Salle), groupe sur fond blanc avec choisi bleu plein (Radiothérapie),
  pilule bleu nuit (Agenda Liste/Jour/Semaine/Mois, Horaires « Par défaut (tous) », RCP « Tous »), pastilles gris-bleu (CIOC, HCK, HGC).
  → 2 styles : onglets soulignés (changer de vue) et choix segmentés (filtrer), choisi en bleu Onco360.
- U10 (Moyenne, complète T10) Badges : 15 variantes en 3 familles (pilule 13 px, compteur arrondi 12 px gras, pastille rouge 11 px), 5 couleurs
  de fond pour les compteurs. → pilule d'état (5 couleurs) + compteur (une forme, gris ou bleu ; rouge seulement pour « en retard »).
- U11 (Faible) Cartes : 12 variantes (arrondi 8 / 12 / 14 / 16 px ; avec ou sans bordure ; marge 0 à 20 px) ; cartes des protocoles et du
  référentiel avec bordure + ombre, cartes du tableau de bord sans bordure ; cartes dans des cartes (T7).
- U12 (Faible) 16 ombres et 14 arrondis différents (6, 8, 9, 10, 12, 14, 16, 20 px…). → 3 ombres, 3 arrondis.
- U13 (Faible) Contour au clic (focus) de plusieurs formes : double trait foncé épais sur la recherche du référentiel, trait bleu ailleurs.
  → un seul anneau bleu, visible au clavier.

## Mise en page et écrans
- U14 (Moyenne) Entre 768 et ~1 100 px (tablette, petit portable), menu en burger et dossier sur une colonne : résumé et rubriques d'abord,
  onglets Consultation / Chimiothérapie / Radiothérapie en bas de l'écran (à 900 px, ils commencent à 845 px de haut). → deux colonnes dès
  ~900 px, ou les onglets en premier comme au téléphone.
- U15 (Faible) « + Chimiothérapie » (Actions rapides) passe sur deux lignes, « + » seul en haut, à 900 et 1 600 px.
- U16 (Faible) Agenda : week-ends hachurés bleus très présents ; titres d'événement coupés « PATIENT TE… » en semaine (lié à A3).
- U17 (Faible, à vérifier) Champs du navigateur dans la langue du navigateur : heures « 08:30 AM », « Choose File » (M1) sur un navigateur réglé en
  anglais (copie de test). Sur un Mac en français : 24 h et « Choisir un fichier ». À contrôler sur les postes du cabinet ; le bouton de fichier peut
  être remplacé par un bouton Onco360.
- Bon : 1 600 px bien rempli (grilles de 4 cartes, tableaux pleine largeur), titres de page clairs, pagination nette, état vide de la Salle illustré.

## Bilan de l'audit UI
16 constats : 1 Haute (U8 boutons), 8 Moyennes, 7 Faibles (dont 1 à vérifier) ; U4 retiré ; 1 correction d'un chiffre donné le 02/11 (#7599BD).
Ils tiennent presque tous dans un **guide de style** (étape 7) qui fixe : couleurs par sens, 3 bordures, 8 tailles de texte, 4 boutons × 3 hauteurs,
2 onglets, 2 badges, 2 cartes, 3 ombres, 3 arrondis, 1 focus. Le reste (U14 tablette, U15, U16) va dans les fiches IDÉE des pages.
