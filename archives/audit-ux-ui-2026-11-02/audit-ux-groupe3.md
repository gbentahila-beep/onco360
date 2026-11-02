# Audit UX – groupe 3 (02/11/2026) : rôles, Documents, connexion et CGU, impressions, Administration — et bilan de l'audit UX

Vu sur la copie de test (jeu fictif ; secrétaire, infirmière, comptable ajoutés pour l'essai ; fonctions serveur de l'Administration simulées
comme dans test_abonnements). Rien modifié dans le code ni en ligne.

## Rôles
- R1 (Moyenne) Secrétaire et infirmière : pas de bouton « Fermer » dans la barre du bas du dossier (le médecin a « Valider » + « Fermer ») ;
  on sort par « ‹ Patients » en haut. Infirmière : barre presque vide (« + Tâche » seul, au milieu).
- R2 (Faible) Même personne appelée « Assistante » (profil, menu du compte) et « secrétaire » (carte « À faire par la secrétaire », droits).
- R3 (à vérifier) En ligne, le compte « Dr Démo » voit le menu « Documents », que la copie de test ne montre pas au médecin (UX2 : secrétaire
  seulement) ; le rôle du compte de démonstration est sans doute différent (remplaçant ?).
- Bon : pages interdites expliquées (« Le bilan est réservé au droit « finances » », « Vous n'avez pas le droit de déposer… ») ; comptable =
  Bilan seul ; tableau de bord de la secrétaire adapté (rappels WhatsApp, rendez-vous à décaler, consultations non clôturées).

## Documents (secrétaire)
- DO1 (Faible) La page ne montre que la zone de dépôt : rien sur les derniers documents déposés (ils sont dans la carte « Derniers documents »
  du tableau de bord).

## Connexion et CGU
- CO1 (Moyenne) « Un e-mail de réinitialisation vient d'être envoyé » s'affiche en rouge (même zone et même couleur que les erreurs).
- CO2 (Faible) La page de connexion n'a pas l'allure d'Onco360 (police du système, titre bleu clair, petits libellés) ; pas de bouton pour
  afficher le mot de passe tapé.
- Bon : fenêtre des CGU claire (case + « Continuer » grisé tant qu'elle n'est pas cochée, « Se déconnecter »), 390 px correct.

## Impressions
- IM1 (Moyenne, lié à D1) Rendez-vous imprimé : petit texte gris en haut d'une page vide, date sans l'année (« Mercredi 30 septembre »), sans
  téléphone ni adresse du cabinet, sans consigne pour le patient. À revoir en faisant D1 (une même feuille pour tous les rendez-vous).
- IM2 (Faible) Liste des rendez-vous à venir : colonne « Heure » vide pour les séances de chimio sans heure.
- Bon : fiche de chimiothérapie (A4 paysage) nette et complète.

## Administration (admin.html)
- AD1 (Moyenne) Autre allure que l'application : police du système, menus déroulants du navigateur, onglets en haut, largeur fixe ;
  « Supprimer » en lien rouge souligné sur chaque ligne des packs, à côté de « Modifier » et « Dupliquer ».
- AD2 (Faible) Tableau des packs dense (limites en 4 lignes de petit texte).
- Bon : chiffres en tête, alerte du cabinet sans abonnement, « Le cabinet reçoit / ne reçoit jamais » dans Nouveau cabinet.

---

# Bilan de l'audit UX (groupes 1 à 3)

**50 constats** : 6 graves (Haute), 19 moyens, 25 légers (groupe 1 : 20, groupe 2 : 21, groupe 3 : 9) ; + 4 demandes décidées (D1 à D4) ; 1 point à vérifier (R3).

## Les 6 graves (+ 2 demandes décidées qui sont aussi des défauts visibles)
| N° | Où | Constat |
|---|---|---|
| T1 | partout | 4 à 8 s de page vide au chargement, mauvais titre affiché |
| T2 | partout | jusqu'à 12 hauteurs de bouton par page (19 à 52 px) |
| T5 | tableau de bord, dossier | listes qui défilent dans une page qui défile, coupées au milieu d'une ligne |
| T8 | téléphone : Bilan, Protocoles, RCP | les filtres prennent tout le premier écran |
| F1 | dossier, téléphone | « + Prescrire » recouvre « Ouvrir » et le ⋯ des cures |
| P1 | Protocoles | la fiche s'ouvre directement en modification |
| (D2) | dossier | ⋯ qui se touchent (Rendez-vous à venir, Historique des RDV) |
| (D4) | dossier | pastille chiffrée coupée sur Médic., Ordo. type… |

## Les thèmes qui reviennent (base du guide de style, étape 7)
1. Boutons : trop de hauteurs et de styles (T2, T9, B1, F6, B3, AD1).
2. Petits textes et majuscules (T3, T4, T11).
3. Téléphone : place prise avant le contenu (T8, A1, T6, F1).
4. Lecture d'abord, modification ensuite (P1, PA1).
5. Messages : succès / erreur / état / action à distinguer (CO1, B3, T6).
6. Compteurs et pastilles : une seule forme (T10, D4).

## Suite
Étape 2 (audit UI : couleurs, typographie, composants, mise en page) puis étape 3 (fonctionnalités, clics), puis les fiches IDÉE (étape 4).
