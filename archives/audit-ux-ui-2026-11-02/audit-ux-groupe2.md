# Audit UX – groupe 2 (02/11/2026) : Protocoles, Radiothérapie, Bilan, RCP, Outils cliniques, Paramètres, Mon compte

Cadre : identité gardée. Vu sur le cabinet de démonstration en ligne (lecture seule) et sur la copie de test (jeu fictif, 1 440 et 390 px).
Rien d'enregistré ni de modifié (fiches ouvertes puis fermées par Échap).

## Partout (complète T1 à T7 du groupe 1)
- T8 (Haute, téléphone) Les filtres occupent tout le premier écran avant le contenu : Bilan (6 champs + boutons, ~470 px), Protocoles (recherche,
  statut, ⋯, Créer, puis 4 menus en cascade : la 1re carte arrive au bas de l'écran), RCP (calendrier + période + boutons : la liste est sous
  l'écran). La Salle d'attente a déjà la bonne solution : un bouton « Filtres » qui ouvre le panneau.
- T9 (Moyenne) Pastille de choix sélectionnée en bleu marine (Listes « Mutuelles », Horaires « Par défaut (tous) », Activités « DEMO », RCP « Tous »),
  alors que UX6 a retiré le bleu marine des boutons ; les pastilles non choisies ont trois styles (gris-bleu, bleu clair, contour).
- T10 (Moyenne) Compteurs placés de trois façons : à côté du mot (« Consultation 4 »), en exposant au-dessus de l'onglet (fiche RT : Contraintes 19,
  Essais 2, Points d'attention 6), entre parenthèses (« Mutuelles (36) »).
- T11 (Faible) Étiquettes en MAJUSCULES grises (molécules des cartes de protocole, « HYPOFRACTIONNÉ », essais des cartes RT), texte de 11-12 px.

## Protocoles
- P1 (Haute) Cliquer sur un protocole ouvre directement le formulaire de modification (curseur dans le nom) ; dans le Référentiel RT, la fiche
  s'ouvre en lecture avec un bouton « Modifier ». Deux bibliothèques, deux comportements ; risque de modifier un protocole par mégarde.
- P2 (Moyenne) Dans la fiche, « Supprimer le protocole » (rouge) est juste à côté de « Annuler » en bas ; trois façons de revenir (« ‹ Protocoles »,
  ✕ en haut à droite, Annuler).
- P3 (Faible) Menus Localisation / Situation / Sous-groupe affichés « — » tant que le précédent n'est pas choisi, sans explication.
- P4 (Faible) Badge « Validé » vert sur toutes les cartes : il n'apporte rien quand tout est validé (on remarquerait mieux « Brouillon »).
- D3 (déjà décidé) Sous-titre « Bibliothèque des protocoles de chimiothérapie » → « traitement systémique ».

## Radiothérapie (référentiel)
- Bon modèle : fiche en lecture, « Retour à la liste », « Modifier », onglets. À reprendre ailleurs (Protocoles).
- R1 (Faible) La fiche s'ouvre sur « Prescription » alors que le 1er onglet est « Indication » (dernier onglet vu gardé ? à vérifier).

## Bilan
- B3 (Moyenne) Colonne « Paiement » du journal : « Payé » et « À encaisser » sont des boutons à contour, « ✓ Encaissé » un bouton vert plein : on ne
  sait pas si c'est un état ou une action (cliquer change l'état).
- B4 (Faible) « Tous les centres » dans le filtre Établissement (le vocabulaire décidé est « Établissement(s) ») ; statuts mélangés « Validée /
  Encaissée / Venu ».
- B5 (Faible) « Versements et règlements reçus » : trois filtres affichés au-dessus de « Aucun versement ni règlement enregistré ».

## RCP
- C1 (Moyenne, téléphone) Calendrier + période + boutons occupent tout l'écran (voir T8).
- C2 (Faible) « Aucun jour de RCP réglé : Paramètres › RCP. » en texte simple : pas de lien pour y aller.

## Outils cliniques
- O1 (Faible) Bouton « Importer des tableaux (fichier) » collé au libellé « Localisation » en dessous.
- O2 (Faible) Cartes CTCAE : la définition est coupée au milieu d'une ligne, sans « … ».
- Bonne structure (menu à gauche comme les Paramètres).

## Paramètres
- PA1 (Moyenne) Listes : chaque élément est une case modifiable (36 mutuelles = 36 champs), le ⋯ flotte loin à droite : lourd, et on modifie un nom
  sans le vouloir. Lecture d'abord, modification au ✎ (comme les informations médicales du dossier) serait plus sûr.
- PA2 (Faible) « Bonjour Dr … » répété (tableau de bord et accueil des Paramètres).
- Bon : menu des familles à gauche, recherche, pied fixe « Valeurs par défaut / Enregistrer », adresse propre de chaque rubrique (#parametres/…).

## Mon compte
- M1 (Moyenne) Photo : champ du navigateur en anglais « Choose File / No file chosen ».
- M2 (Faible) Champs IF, TP, ICE avec « Reçus » écrit dedans en gris (on croit à une valeur) : à remplacer par une phrase sous le champ
  (« Imprimé sur les reçus »).
- M3 (Faible) Champs en lecture seule (e-mail, rôle) sur fond gris-bleu foncé, peu lisible.

## Mesures (copie de test) : tailles de texte / hauteurs de bouton / couleurs de bouton
protocoles 7 / 7 / 6 · radiothérapie 6 / 6 / 6 · bilan 7 / 6 / 5 · RCP 8 / 6 / 9 · outils 7 / 7 / 5 · paramètres 6 / 5 / 4 · mon compte 9 / 5 / 5.
Aucun débordement horizontal, aucune erreur JavaScript.
