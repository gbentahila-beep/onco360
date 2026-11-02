# Audit des fonctionnalités (étape 3, 02/11/2026) : clics, recherches, tableaux, filtres

Vu sur la copie de test (jeu fictif, médecin, 1 440 px), par des essais automatiques : 60 recherches tapées, 11 parcours comptés, tri et
mémoire des filtres essayés page par page. Rien modifié dans le code. Captures : scratchpad `audit/c4/`.

## Parcours courants (médecin)
| Tâche | Clics | Remarque |
|---|---|---|
| Ouvrir un dossier (recherche du haut) | 1 + nom + 1 | sans rien taper : 8 derniers dossiers ouverts (lot A) ; voir FN1 |
| Nouveau rendez-vous depuis le dossier | 3 (+ Rendez-vous, créneau, Enregistrer) | patient, type, durée et lieu déjà remplis, créneaux libres en boutons |
| Ordonnance d'un médicament | 3 + recherche (Médic., Ajouter, Enregistrer + Imprimer) | |
| Ordonnance type | 3 (Ordo. type, Utiliser, Enregistrer + Imprimer) | |
| Valider une séance de chimio | 2 + bilan (Ouvrir, Valider J15) | séance du jour ouverte d'office, seuils écrits dans les cases (≥ 1,5…) |
| Nouvelle ligne de traitement | 3 + saisie (Nouvelle ligne, protocole, Créer la ligne) | liste déjà filtrée sur la localisation du dossier ; 2e étape chargée (FN6) |
| Nouvelle consultation | 2 + saisie | 15 champs, dont 9 de toxicité |
| Nouvelle tâche | 3 + titre | types en boutons |
| Nouveau patient | 2 + 13 champs | identité seulement, le reste dans le dossier |
| Patient du jour : arrivé → vu | 4 (Mettre en salle, Démarrer, Valider, prix) | relevé à l'audit UX |
| Imprimer un rendez-vous | 2 (⋯, Imprimer) | consultations seulement ; pas pour une séance de chimio ni la RT (D1) |

Les parcours courants sont courts (2 à 4 clics) et déjà bien pensés. Les défauts sont dans les **recherches** et les **tableaux**.

## Recherches
- FN1 (Haute) Recherche du haut sans classement. « test 80 » : les 8 résultats affichés sont TEST 57 à TEST 64 (leur n° 202608057… contient « 80 ») ;
  le bon patient n'est pas dans la liste, et **Entrée ouvre le premier : un autre patient**. Liste coupée à 8 sans dire qu'il y en a d'autres.
  Page Patients : même ordre, le bon patient n'est pas dans les premières lignes. Cause : un mot est cherché n'importe où (aussi au milieu du n°),
  puis les 8 premiers dossiers dans l'ordre de la base sont gardés (`rechercheTete`, v2.js:1603). → classer : nom qui commence par le mot, mot entier,
  n° qui commence par les chiffres, puis le reste ; afficher « 8 sur 23 ». Risque actuel : ouvrir le mauvais dossier.
- FN2 (Moyenne) Deux recherches de patient, deux règles : en haut nom, n°, téléphone ; page Patients nom, n°, date de naissance, localisation, pas le
  téléphone (« 0600000000 » : 0 résultat). Aucune ne trouve la CIN. Téléphone écrit « +212 6… » : 0 résultat. → une seule règle pour les deux.
- FN3 (Moyenne) Protocoles : écritures et synonymes. « 5-FU » 42 protocoles, « 5 FU » 49, « 5FU » 4 ; « fluorouracile » 0 (la bibliothèque écrit
  « fluoro-uracile » : 19) ; « CDDP » 0 ; « Taxol » 0 ; « Herceptin » 17, « trastuzumab » 20. → ignorer tirets et espaces ; table de synonymes
  (DCI, noms commerciaux, abréviations courantes), la même pour Protocoles, Nouvelle ligne et Médic.
- FN4 (Faible) Recherche des Paramètres : « mot de passe », « signature », « droits », « équipe » → rien (ils sont dans Mon compte) ; « prix »,
  « vacances », « protocole » → rien. → mots en plus et renvoi vers Mon compte / Protocoles.
- Bon : accents ignorés partout ; référentiel RT (« stereotaxie » = « stéréotaxie » : 60 ; « prostate 60 » : 3 schémas) ; Médic. par DCI (« paracetamol »).

## Tableaux
- FN5 (Moyenne) Aucun tableau ne se trie en cliquant sur une colonne : Patients (8 colonnes), journal du Bilan (10 colonnes), Tâches, RCP. Seules la Salle
  (menu « Tri »), les Essais du référentiel RT et l'Administration trient. → tri au clic sur l'en-tête (petite flèche), mêmes colonnes, mêmes noms.
- FN6 (Moyenne) Nouvelle ligne, 2e étape : tableau des molécules de 9 colonnes (Produit, ↑, −, Dose, Unité, Jours, Libellé jour, Précision, Voie,
  Soluté + volume) qui dépasse à droite même à 1 440 px ; « Jours » coupé (« 1,8,15,22,2 »). → colonnes rarement remplies (libellé, précision, voie,
  soluté) repliées sous « Détails » pour chaque molécule.

## Filtres
- FN7 (Faible) Mémoire des filtres inégale. On quitte la page puis on revient : Protocoles, Tâches, Bilan et Agenda gardent le choix, Patients l'efface.
  Après rechargement, tout revient au départ (Agenda en Semaine, Bilan en Mois en cours). → même règle partout ; vue d'Agenda préférée gardée par
  personne (`utilisateurs/{uid}`, comme les colonnes de la Salle).
- Rappel : T8 (filtres qui prennent l'écran du téléphone), P3 (menus « — » sans explication).

## Bilan de l'audit des fonctionnalités
7 constats : 1 Haute (FN1, mauvais dossier ouvert), 4 Moyennes, 2 Faibles. Les parcours courants n'ont pas besoin d'être raccourcis ; il faut
fiabiliser les recherches (classement, une règle commune, synonymes) et rendre les tableaux triables.
