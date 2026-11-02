# Onco360 – Audit UX / UI : inventaire et méthode (02/11/2026)

Exploré dans Chrome, en lecture seule, sur le **cabinet de démonstration** en ligne (compte démo, patients « PATIENT TEST »),
à 1 440 px. Rien n'a été modifié. Légende : ☐ à analyser · ◐ structure relevée (aujourd'hui) · ☑ analysé (audit fait).

## 1. Architecture générale

Trois applications :
1. **Connexion** (`index.html`) : e-mail, mot de passe, « Poste partagé », lien des CGU ; fenêtre d'acceptation des CGU au 1er accès.
2. **Onco360** (`v2.html`) : l'application du cabinet.
3. **Administration** (`admin.html`) : la plateforme (cabinets, abonnements, modèles) ; compte d'administration seulement.

Cadre commun d'Onco360 :
- **Menu latéral** (repliable, 76 px replié) : 11 entrées, pastilles (Tâches 4).
- **Barre du haut** : icône + titre + une ligne d'explication, recherche patient en pilule, roue Paramètres, cloche Alertes (9), menu du compte
  (Mon compte, Guide de démarrage, Déconnexion, choix du cabinet si plusieurs).
- **Quatre formes de fenêtre** : petite fenêtre, pleine page (« ← » + « Échap pour annuler »), panneau au centre du dossier, fenêtres d'avertissement
  (rouge / orange / neutre) ; messages en bas (toasts) ; notifications en haut (temps réel).

## 2. Inventaire

| # | Zone | Ce qu'elle contient | État |
|---|---|---|---|
| A | **Cadre commun** | menu, barre du haut, recherche, alertes, menu du compte, chargement « Chargement de vos données… », toasts, notifications, 4 formes de fenêtre, téléphone (menu burger) | ☑ UX (groupe 1) |
| B | **Tableau de bord** | « Bonjour Dr … », ‹ jour ›, + Rendez-vous, + Patient ; cartes Aujourd'hui (Consultations / Chimio / RT), Actions rapides (6), À valider par le médecin, Les 7 prochains jours (rappels WhatsApp), Activité récente, Derniers documents, Mes tâches, Conflits : rendez-vous à décaler, Statistiques (6 chiffres) ; Premiers pas, abonnement | ☑ UX (groupe 1) |
| C | **Agenda** | Liste / Jour / Semaine / Mois, Aujourd'hui, ‹ ›, Actualiser, + Rendez-vous, mini-calendrier, filtres (établissement, médecin, catégories), glisser-déposer, fenêtre d'un événement, heure d'une séance | ☑ UX (groupe 1) |
| D | **Salle d'attente** | semaine, jour, recherche, tri, colonnes au choix, imprimer, séances du lendemain, clôturer la journée, Matinée / Après-midi / Toute la journée, onglets À venir / En salle / Vus / Absents, Valider / ⋯, reçu et prix, report d'un absent | ☑ UX (groupe 1) |
| E | **Patients** | recherche, 2 filtres, tableau (7 colonnes), + Patient (pleine page), import de patients | ☑ UX (groupe 1) |
| F | **Dossier patient** | *voir F1 à F8* | ☑ UX (groupe 1) |
| F1 | Bandeau | nom, n°, âge, établissement, localisation, pastilles Chimio / RT, ⋯ (Journal…) | ☑ UX (groupe 1) |
| F2 | Colonne Patient | Résumé, **Rendez-vous et tâches à venir**, Identité et administratif, Informations médicales (en lignes), Fiche tumeur, **Historique des RDV**, Tout replier, Voir plus | ☑ UX (groupe 1) |
| F3 | Onglet Consultation | Nouvelle consultation, Notes seulement, ⋯, journal dépliable, Modifier / Supprimer, formulaires par type | ☑ UX (groupe 1) |
| F4 | Onglet Chimiothérapie | + Nouvelle ligne de traitement (menus en cascade), protocole, intention, + 1 cure, Ouvrir, + heure ; fenêtre de cure et de séance, vigilance, report, fiche chimio, ordonnances du protocole | ☑ UX (groupe 1) |
| F5 | Onglet Radiothérapie | + Nouvelle radiothérapie, Modifier, Clôturer, étapes (scanner → contourage → dosimétrie → séances → fin), documents RT (pli, CR, rendez-vous), Référentiel › | ☑ UX (groupe 1) |
| F6 | Onglet / colonne Documents | Ajouter un document, liste, état vide | ☑ UX (groupe 1) |
| F7 | Barre du bas | Médic., Ordo. type, Analyses, Examens compl., Courriers, Doc. (avec ▾ Historique), Feuille de soins, + RCP, + Rendez-vous, + Tâche, minuteur, Valider, Fermer | ☑ UX (groupe 1) |
| F8 | Fenêtres du dossier | 6 fenêtres de prescription (deux colonnes), ordonnance A5 / A4, feuille de soins, + RCP, + Rendez-vous (pleine page), + Tâche, Modifier une partie de la fiche, prix / reçu | ☑ UX (groupe 1) |
| G | **Documents** (menu, secrétaire) | dépôt de fichiers dans les dossiers | ☑ UX (groupe 3) |
| H | **Tâches** | Mes tâches / Toutes, recherche, filtres Statut / Échéance / Type / Lieu, Imprimer, + Tâche, Tâches terminées (repliées), fiche avec fil, tâches automatiques | ☑ UX (groupe 1) |
| I | **RCP** | semaines (S44…), période, statut, patients inscrits, décision RCP | ☑ UX (groupe 2) |
| J | **Protocoles** | recherche, 5 filtres, Favoris, ⋯, Créer un protocole, cartes (12 par page), fiche pleine page, éditeur | ☑ UX (groupe 2) |
| K | **Radiothérapie** (référentiel) | onglets Référentiel, Contourage, Organes à risque, Contraintes, Essais, Calcul BED / EQD2 ; recherche, 4 menus en cascade, Nouveau schéma, favoris ; fiche à onglets (Indication…), modification du cabinet | ☑ UX (groupe 2) |
| L | **Outils cliniques** | Stadification TNM (8 régions), Échelles de toxicité (CTCAE), Calculateurs | ☑ UX (groupe 2) |
| M | **Bilan** | 5 filtres + recherche, Actualiser, ⋯, Relevé, Par établissement, Mois par mois, Journal détaillé, Référents, RT prévisionnelles, Versements et règlements reçus | ☑ UX (groupe 2) |
| N | **Paramètres** | accueil « Que voulez-vous faire ? » + recherche ; 6 familles, 21 rubriques : *Cabinet* (Lieux d'exercice, Journal d'audit, RCP, Impression, Tableau de bord, Export des données + récupération + import) · *Dossier patient* (Fiche patient, Formulaire de consultation, Types de consultation, Affichage du dossier) · *Agenda et rappels* (Horaires, Congés et jours fériés, WhatsApp, Google Agenda, Alertes, Couleurs selon le cabinet) · *Bibliothèques* (Listes, Bibliothèques, Vigilance des molécules) · *Finances* (Activités et rémunérations) · *Laboratoires* | ☑ UX (groupe 2) |
| O | **Mon compte** | Informations, Accès (équipe et droits), Abonnement, Factures ; Guide de démarrage | ☑ UX (groupe 2) |
| P | **Administration** | Cabinets, Nouveau cabinet, Par spécialité (modèle), Modules, Journal, Sauvegardes, Comptabilité, État de la plateforme | ☑ UX (groupe 3) |
| Q | **Connexion et CGU** | connexion, mot de passe oublié, poste partagé, CGU | ☑ UX (groupe 3) |
| R | **Impressions** | ordonnances A5 / A4, fiche chimio, pli / CR / rendez-vous RT, reçu A5, rendez-vous, listes, feuille de soins, exports du Bilan | ☑ UX (groupe 3) |
| S | **Rôles** | médecin, secrétaire, infirmière, comptable, remplaçant : chacun voit d'autres menus, cartes et boutons | ☑ UX (groupe 3) |
| T | **Écrans** | 390 / 900 / 1 280 / 1 600 px, Chrome et Safari | ☑ 390 / 900 / 1 440 / 1 600 px et Safari (WebKit) : audit UI, `audit-ui.md` |

États vides, chargements et erreurs : relevés page par page pendant l'audit UX (étape 1).

## 3. Déjà vu pendant ce tour (demandes décidées)

- **« Imprimer le rendez-vous »** : présent dans le ⋯ des rendez-vous de consultation (`v2.js`, liste des rendez-vous à venir et historique),
  absent pour les **séances de chimio** (⋯ = « Consultation : venu / Séance / Modifier »), le **scanner** et les autres étapes de RT.
- **Bouton ⋯ trop gros** : 36 × 36 px, alors que les lignes de « Rendez-vous et tâches à venir » sont espacées de 34 à 35 px → les boutons se
  touchent (même chose dans « Historique des RDV »). La solution doit garder la zone à toucher à 40 / 44 px au téléphone (règle du projet) : bouton plus
  discret (sans cadre, 28 px visibles) avec une zone à toucher plus large, ou lignes un peu plus hautes.
- À vérifier : le menu « Documents » apparaît pour le compte « Dr Démo » alors qu'il ne devrait être que pour la secrétaire (UX2) ; à contrôler
  avec le rôle du compte de démonstration.

## 4. Méthode

1. **Où** : on regarde dans le cabinet de démonstration en ligne (lecture seule) ; toute action (créer, valider, reporter) se fait sur la copie de test
   locale (jeu fictif), aussi pour les rôles secrétaire / infirmière / comptable. Captures : jeu fictif seulement.
2. **Grille de chaque page** (10 points) : on comprend la page en 5 secondes ; action principale visible ; nombre de clics des tâches courantes ;
   retours après une action (message, chargement, erreur) ; états vides ; cohérence des composants (boutons, cartes, tableaux, fenêtres) ; lisibilité
   (texte ≥ 13 px, contraste) ; zones à toucher (40 / 44 px) ; 390 / 900 / 1 280 / 1 600 px sans débordement ; ce que voit chaque rôle.
3. **Mesures automatiques** par page (script dans le navigateur) : tailles de texte, hauteurs de bouton, couleurs utilisées, cibles trop petites,
   débordements ; pour comparer avant / après.
4. **Ordre** (du plus utilisé au moins utilisé) : Dossier patient → Tableau de bord → Agenda → Salle d'attente → Patients → Tâches et RCP →
   Protocoles → Radiothérapie → Bilan → Paramètres → Mon compte → Outils cliniques → Documents → Connexion → Impressions → Administration.
5. **Fiches IDÉE** (format demandé), présentées par page, réponse OUI / NON / MODIFIER pour chacune ; le silence n'est pas un accord ; liste des
   idées acceptées / refusées / à modifier tenue dans `FEUILLE-DE-ROUTE.md`. La liste « Refusé – ne pas reproposer » est respectée.

## 5. Suivi

| Étape | État |
|---|---|
| 0. Inventaire et méthode | fait le 02/11/2026 |
| 1. Audit UX | fait le 02/11/2026 (groupes 1 à 3, 50 constats) |
| 2. Audit UI | fait le 02/11/2026 (`audit-ui.md`, 17 constats) |
| 3. Audit des fonctionnalités | fait le 02/11/2026 (`audit-fonctions.md`, 7 constats) |
| 4. Propositions visuelles (fiches IDÉE) | lot 1 accepté le 02/11/2026 (`audit-fiches-lot1.md`) ; lot 2 accepté le 02/11/2026 (`audit-fiches-lot2.md`, idées 9 à 20 dont D5, « tout oui ») |
| 5. Plan de refonte | proposé le 02/11/2026 : phase IG (IG1 à IG9) dans `FEUILLE-DE-ROUTE.md`, à valider par Dr Bentahila |
| 6. Exécution par lots | IG1 à IG7, après validation du plan |
| 7. Design system | IG8 (guide de style) |
| 8. Contrôle qualité final | IG9 (avant / après) |
