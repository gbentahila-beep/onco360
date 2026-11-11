# Mise en ligne depuis GitHub (11/11/2026)

But : mettre Onco360 en ligne depuis Claude Code sur le web ou le téléphone, sans le Mac.
L'action `.github/workflows/mise-en-ligne.yml` lance le contrôle complet (`avant-mise-en-ligne.sh --navigateur`, et `--regles` pour les règles)
sur la branche **main**, puis met en ligne **seulement si tout est bon**. Elle met en ligne le site et / ou les règles Firestore ; les fonctions
serveur restent mises en ligne depuis le Mac (`firebase deploy --only functions`).

## À faire une fois (Dr Bentahila, environ 10 minutes)

### 1. Créer le compte de service (Google Cloud)
1. Ouvrir https://console.cloud.google.com/iam-admin/serviceaccounts?project=chimio-hgc (compte Google du projet).
2. « + Créer un compte de service » : nom `deploiement-github` → « Créer et continuer ».
3. Ajouter ces 4 rôles (champ « Sélectionner un rôle », taper le nom) :
   - **Administrateur Firebase Hosting** (Firebase Hosting Admin)
   - **Administrateur des règles Firebase** (Firebase Rules Admin)
   - **Lecteur de clés API** (API Keys Viewer)
   - **Consommateur Service Usage** (Service Usage Consumer)
   → « Continuer » → « OK ». Aucun accès aux données des patients.
4. Cliquer sur le compte créé › onglet « Clés » › « Ajouter une clé » › « Créer une clé » › **JSON** → un fichier se télécharge.

### 2. Ranger la clé dans GitHub (jamais dans la conversation)
1. Ouvrir https://github.com/gbentahila-beep/onco360/settings/secrets/actions
2. « New repository secret » : nom **`FIREBASE_CLE`**, valeur = tout le contenu du fichier JSON (l'ouvrir avec TextEdit, tout copier).
3. « Add secret », puis **supprimer le fichier JSON** de l'ordinateur (et de la corbeille).

### 3. Mettre l'action sur main
L'action n'apparaît dans GitHub qu'une fois sur la branche main (demander à Claude d'ouvrir la demande de fusion, puis la fusionner).

## Ensuite
- Dire à Claude « mets en ligne le site » (ou « les règles », « le site et les règles ») : Claude pousse le code sur main et lance l'action.
- Ou à la main : GitHub › Actions › « Mise en ligne » › « Run workflow » › choisir › « Run workflow ».
- Durée : 30 à 90 minutes (parcours dans Chrome et Safari). En rouge : rien n'est mis en ligne, le détail est dans « Détail des erreurs ».
- Après : recharger sans cache (Cmd + Maj + R) et faire les 3 vérifications habituelles.

## En cas de clé perdue ou volée
Google Cloud › Comptes de service › `deploiement-github` › Clés › supprimer la clé ; en créer une autre et remplacer le secret `FIREBASE_CLE`.
