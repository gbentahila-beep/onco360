# Audit UX – groupe 1 (02/11/2026) : dossier patient, tableau de bord, agenda, salle d'attente, patients, tâches

Cadre décidé le 02/11/2026 : **identité gardée** (mêmes pages, colonnes, noms, bleu Onco360 ; finition modernisée, guide de style commun).
Vu sur le cabinet de démonstration en ligne (lecture seule, 1 440 px) et sur la copie de test locale (jeu fictif, 1 440 et 390 px, mesures).

## Demandes décidées (à mettre au plan, sans attendre l'audit)
- D1. « Imprimer le rendez-vous » dans le ⋯ de chaque ligne de « Rendez-vous et tâches à venir » (séances de chimio, scanner, étapes de RT,
  autres rendez-vous) ; impression de la liste entière inchangée.
- D2. Bouton ⋯ trop gros dans « Rendez-vous et tâches à venir » et « Historique des RDV » (36 px pour des lignes de 34-35 px : ils se touchent).
- D3. Protocoles : « Bibliothèque des protocoles de chimiothérapie » → « … de traitement systémique » (v2.js:1159) ; **accepté le 02/11/2026** : même
  changement dans la liste des bibliothèques (« Protocoles de chimiothérapie », catalogue.js:329 et admin.js:380).
- D4. Pastille chiffrée coupée en haut des boutons Médic., Ordo. type, Analyses, Examens compl., Courriers, Doc. (barre du bas du dossier) :
  cause vérifiée le 02/11 : chaque bouton double « Médic. + ▾ » a `.pr{overflow:hidden}` (v2.html:294), qui coupe la pastille posée à -8 px.

## Constats (gravité : Haute / Moyenne / Faible) — liste « Refusé » respectée (libellés coupés des rendez-vous, titre de ligne en étiquettes,
## barre du bas en groupes, tuiles, etc. ne sont pas reproposés)

### Partout
- T1 (Haute) Chargement : 4 à 8 s de page vide « Chargement de vos données… », titre « Tableau de bord » même quand on ouvre un dossier.
- T2 (Haute) Boutons de toutes les hauteurs : dossier 12 hauteurs (19 à 52 px), tableau de bord 9, agenda 10 (UX6 visait 36 / 40 / 44).
- T3 (Moyenne) Textes sous 13 px : pastilles 11 px (cloche, menu, barre du dossier), « à jour à … » 11 px (agenda, salle), compteurs des onglets
  de la salle 12 px, mini-calendrier 12 px, statut des cures au téléphone 12 px.
- T4 (Moyenne) Titres écrits en MAJUSCULES (colonne Patient : RENDEZ-VOUS ET TÂCHES À VENIR, IDENTITÉ…, HISTORIQUE DES RDV ; agenda : RDV À VENIR),
  à côté de « Résumé du patient » en minuscules ; ailleurs les majuscules ont été retirées (UX7).
- T5 (Haute) Défilements imbriqués : cartes du tableau de bord (À valider, Les 7 prochains jours) et colonne Patient défilent dans une page qui
  défile ; la molette s'accroche, les listes sont coupées au milieu d'une ligne.
- T6 (Moyenne) « Actualiser » + « à jour à … » (agenda, salle) : au téléphone le texte « à jour à 09 h 00 » chevauche le bouton « + Rendez-vous ».
- T7 (Faible) Cartes dans des cartes (Aujourd'hui > Consultations / Chimio / RT) : effet chargé.

### Dossier patient
- F1 (Haute, téléphone) Le bouton flottant « + Prescrire » recouvre le bas du contenu (bouton « Ouvrir » et ⋯ d'une cure, fin de liste).
- F2 (Moyenne, téléphone) Onglets : seul « Patient » a une icône ; « Patient » et « Chimio » collés, espacement inégal.
- F3 (Moyenne) Minuteur « 0 min / 1 h 21 » dans la barre, sans libellé : on ne sait pas ce qu'il compte.
- F4 (Faible) Auteur des consultations : « Dr Démo Onco360 » sur la consultation ouverte, initiales « DO » sur les autres.
- F5 (Faible) « Tout replier » isolé entre le résumé et les rubriques.
- F6 (Faible) Ligne de chimio ouverte entourée d'un cadre bleu marine épais ; « annuler » (dosimétrie) en lien rouge souligné, style unique.

### Tableau de bord
- B1 (Moyenne) « Les 7 prochains jours » : un gros bouton WhatsApp vert plein à chaque ligne, couleur la plus forte de la page pour une action secondaire.
- B2 (Faible, téléphone) Titre coupé « Tableau de … ».

### Agenda
- A1 (Moyenne, téléphone) 4 rangées de commandes avant la grille (vues, date, Actualiser / + Rendez-vous, établissement) : ~300 px avant le 1er créneau.
- A2 (Moyenne) Filtre d'établissement : pastille grise « DEMO » sans libellé sur ordinateur, menu « Tous les établissements » au téléphone.
- A3 (Faible) Grille au quart d'heure, toutes les heures écrites : dense ; événements de 15 min coupés.

### Salle d'attente
- S1 (Faible) Deux façons de choisir le jour (menu ▾ de la date et bouton « Calendrier »).
- Bon état général (6 hauteurs de bouton, aucune cible trop petite sur ordinateur).

### Patients, Tâches
- Bon état (Patients : 4 hauteurs de bouton, 1 seule cible trop petite). Téléphone : trois menus de filtre empilés avant la liste (Faible).

## Mesures (copie de test, jeu fictif) : tailles de texte / hauteurs de bouton / couleurs de bouton
dossier 8 / 12 / 9 · tableau de bord 10 / 9 / 10 · agenda 7 / 10 / 10 · salle 8 / 6 / 7 · patients 6 / 4 / 3 · tâches 6 / 5 / 5. Aucun débordement
horizontal à 390 et 1 440 px, aucune erreur JavaScript.
