# Mise en ligne depuis GitHub (11/11/2026)

But : mettre Onco360 en ligne depuis Claude Code sur le web ou le téléphone, sans le Mac.
L'action `.github/workflows/mise-en-ligne.yml` lance le contrôle complet (`avant-mise-en-ligne.sh --navigateur`, et `--regles` pour les règles)
sur la branche **main**, puis met en ligne **seulement si tout est bon** : site, règles Firestore, et (depuis le 11/11/2026) fonctions serveur
et index, avec une seconde clé et l'approbation de Dr Bentahila (plus besoin du Mac).

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

### 3. Fonctions serveur : seconde clé, avec approbation
Les fonctions serveur tournent avec tous les droits sur la base : une clé qui les met en ligne vaut un accès complet. D'où une clé à part,
utilisable seulement après un clic d'approbation de Dr Bentahila (site GitHub ou application GitHub du téléphone).
1. GitHub : https://github.com/gbentahila-beep/onco360/settings/environments › « New environment » : nom **`fonctions`** › « Configure environment ».
2. Cocher **« Required reviewers »**, ajouter son propre compte GitHub, « Save protection rules ».
3. Plus bas, « Environment secrets » › « Add environment secret » : nom **`FIREBASE_CLE_FONCTIONS`** (valeur : voir 4 et 5).
4. Google Cloud (même page qu'au 1.) : compte de service `deploiement-fonctions`, rôles **Éditeur** (Editor) et **Utilisateur du compte de
   service** (Service Account User) ; onglet Clés › clé JSON.
5. Coller tout le fichier dans le secret du 3., puis supprimer le fichier de l'ordinateur et de la corbeille.
6. Conseillé : double authentification activée sur le compte GitHub (Settings › Password and authentication).

### 4. Mettre l'action sur main
L'action n'apparaît dans GitHub qu'une fois sur la branche main (demander à Claude d'ouvrir la demande de fusion, puis la fusionner).

## Ensuite
- Dire à Claude « mets en ligne le site » (ou « les règles », « le site et les règles », « les fonctions », « tout ») : Claude pousse le code
  sur main et lance l'action. Pour les fonctions, GitHub envoie une demande d'approbation : « Review deployments » › cocher `fonctions` › « Approve ».
- Ou à la main : GitHub › Actions › « Mise en ligne » › « Run workflow » › choisir › « Run workflow ».
- Durée : 30 à 90 minutes (parcours dans Chrome et Safari). En rouge : rien n'est mis en ligne, le détail est dans « Détail des erreurs ».
- Après : recharger sans cache (Cmd + Maj + R) et faire les 3 vérifications habituelles.

## En cas de clé perdue ou volée
Google Cloud › Comptes de service › `deploiement-github` › Clés › supprimer la clé ; en créer une autre et remplacer le secret `FIREBASE_CLE`.
