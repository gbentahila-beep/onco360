# Guide de style d'Onco360

IG8 (03/11/2026, étape 7 de l'audit UX / UI du 02/11/2026). Ce document fixe ce que la phase IG a mis en place (IG3 : composants communs ;
IG5 à IG7 : tableaux, filtres, téléphone). **Tout nouvel écran suit ces règles** ; une exception se décide avec Dr Bentahila et s'écrit ici.

Les valeurs vivent dans `public/v2.html` (variables de `:root`, bloc « Phase IG, IG3 ») : ce guide les nomme, il ne les recopie pas toutes.
Page de démonstration (hors du site, jamais publiée) : `python3 outils/guide-style-demo.py`, puis ouvrir `docs/guide-de-style-demo.html`.

## 1. Identité gardée

- Fond `#F1F5FB` (`--fond`), cartes blanches arrondies, couleur d'action `#3563B0` (`--prim`), logo et menu inchangés.
- Polices du site seulement (`vendor/polices`, jamais Google Fonts) : **Montserrat 700** pour les titres (h1 à h4), **Roboto** 400 / 500 / 700 pour le texte.
- Aucun émoji à l'écran : icônes dessinées `ic("nom")` (symboles SVG de v2.html).
- Pas de majuscules d'affichage (`text-transform`) ni d'espacement de lettres : on écrit les mots comme on les lit.

## 2. Couleurs : une teinte par sens

| Sens | Variable | Fond clair | Exemple |
|---|---|---|---|
| Action, choix en cours, lien | `--prim` #3563B0 | `--prim-c` | bouton principal, onglet actif, ▲ / ▼ du tri |
| Réussi, payé, validé | `--vert` #00806A | `--vert-c` | badge « Validé », « Connexion réussie » ✓ |
| À surveiller, à recevoir | `--orange` #AA6709 (texte `--orange-t`) | `--orange-c` | « À recevoir », retard léger |
| Danger, erreur, suppression | `--rouge` #E5004C (texte `--rouge-t`) | `--rouge-c` | « Supprimer », erreur de saisie, cure en retard |
| Texte | `--encre` #00264C, secondaire `--doux` #294056 | — | |
| Traits | `--trait` (cartes), `--bord-ch` (champs), `--bord-bt` (boutons secondaires) | — | |

Règles : jamais une couleur écrite en dur dans un nouvel écran (une variable de `:root`) ; un texte coloré sur fond clair garde un contraste
d'au moins 4,5 pour 1 (d'où les variantes `-t`) ; le rouge n'annonce que le danger.

## 3. Texte

- Huit tailles `--t1` (11 px) … `--t8` (26 px), mais **5 tailles de texte + 3 titres** suffisent :
  texte courant `--t4` (14 px) ou `--t5` (15 px), petit `--t3` (13 px, jamais moins pour une information), champ `--t6` (16 px, évite le zoom de l'iPhone) ;
  titres de carte `--t6`, de page `--t7`, de nom du patient `--t8`.
- `--t1` / `--t2` (11–12 px) : seulement pour une mention qui n'est pas une information (« à jour à 09 h 00 », pastille).

## 4. Boutons : 4 sortes × 3 hauteurs

| Sorte | Classe | Aspect | Usage |
|---|---|---|---|
| Principal | `b1` (ou `bt` plein) | bleu plein, texte blanc | **une** action principale par zone (Enregistrer, Créer un protocole) |
| Secondaire | `b2`, `bt clair`, `bt gris` | blanc, cadre `--bord-bt`, texte foncé ; survol : fond `--prim-c`, cadre bleu | Annuler, Fermer, Actualiser, Filtres |
| Discret | `b3`, ⋯ (`mpts > .sa-plus`, `rtr-pts3 > summary`) | sans cadre ni fond, fond léger au survol | plus d'actions, icône seule |
| Danger | `mini rouge`, `bt rouge-t`, `b2 danger` | texte rouge, cadre rose ; survol : fond `--rouge-c` | Supprimer, Retirer (toujours derrière une confirmation) |

Hauteurs : **36 px** dans une liste ou un tableau, **40 px** en haut d'une page ou dans un pied de fenêtre, **44 px** au doigt (`pointer:coarse`
ou largeur ≤ 640 px). Un bouton d'icône seule a un `title` et un `aria-label`.

Sur une même ligne, des boutons voisins ont **la même hauteur et, au téléphone, la même largeur** (« Filtres » | « Actualiser » | ⋯ de 44 px ;
« Filtres » | « Favoris » | ⋯) ; la recherche et le bouton principal prennent toute la largeur de leur ligne.

## 5. Champs

- Hauteur 44 px, cadre `--bord-ch` (3,2 pour 1), plus foncé au survol, bleu quand on écrit ; anneau de focus `--anneau` (le seul : `:focus-visible`).
- Libellé au-dessus du champ, jamais à l'intérieur seulement. Erreur : `erreur(texte, champ)` (cadre rouge, `aria-invalid`).
- Menus d'un même filtre : cases de même largeur, écart de 12 px (`--ecart-champs`) ; le premier choix d'un menu de filtre dit « Tous » quand le titre
  au-dessus nomme déjà le filtre (Bilan).
- Mot de passe : « Afficher » / « Masquer » dans le champ.

## 6. Choix, onglets, badges, compteurs

- **Un seul groupe de choix** (`.choix`, `.ag-vues`) : fond `--choix-f`, choix en cours en bleu plein. **Onglets soulignés** (`.o-barre`, `.rtr-ong`) pour
  changer de partie d'une même page ; rien d'autre.
- **Deux badges** : badge d'état (`.badge` + sens : vert validé, orange à vérifier, rouge danger, bleu information) et étiquette grise (`.pc-mol`, molécules,
  établissement). Badges d'un titre : juste après le titre, sur la même ligne (fiches de protocole).
- **Compteurs** : pastille après le mot (`.n`, `.nb`), texte foncé sur `--cpt-f` ; sur un choix actif, pastille claire.

## 7. Cartes, ombres, arrondis

- **Deux cartes** : carte de page (`.carte` : blanc, `--r-l` 12 px, `--ombre`, trait `--gris-c`) et cadre intérieur sans ombre (`.pr-cad`, `.avert-ind`
  sur fond blanc avec trait `--trait`).
- **Trois ombres** : `--ombre` (cartes), `--ombre-rond` (menus ⋯, bulles), aucune (cadres intérieurs, boutons).
- **Trois arrondis** : 12 px (cartes, fenêtres), 8 px (boutons, champs, menus), 999 px (pastilles, recherche du haut).
- Écart entre cartes `--ecart` (18 px), entre champs `--ecart-champs` (12 px).

## 8. Tableaux et listes

- Titre de colonne cliquable pour trier (`A.enteteTri` / `A.thTri`) : flèche ↕ discrète, ▲ / ▼ en bleu sur la colonne choisie, 3e clic = ordre par défaut ;
  tri gardé par personne (`utilisateurs/{uid}.tris`).
- Ligne de 44 px à partir de 768 px ; bandeau bleu en tête (`A.bandeau`) avec le nombre.
- Liste longue d'une carte du tableau de bord : 5 lignes, puis « Voir les N … › » (jamais de défilement dans une carte).
- Liste en lecture, ✎ pour modifier une ligne, ⋯ pour retirer (Paramètres › Listes).
- État vide : `A.etatVide({ ill, titre, txt })`.

## 9. Pages, fenêtres, fiches

- Haut de page : icône, titre et explication (`hautDePage`), jamais de second titre dans la page.
- Fenêtre pleine page : « ← Retour à … » en haut, pied collant avec « Échap pour annuler » à gauche et les boutons à droite (« Fermer » / « Enregistrer »).
- Fiche ouverte en lecture d'abord : « Retour à la liste » en haut, titre + badges, étoile de favori puis ⋯ à droite (Modifier, Dupliquer,
  Imprimer, Signaler, Supprimer en rouge à la fin) ; avertissement dans un cadre en bas.
- Dossier patient : « Fermer » à droite de la barre du bas pour tous les rôles (retour à la page d'origine).
- Questions : `confirmer`, `alerte`, `saisir` (dialogues.js), jamais `confirm` / `alert` / `prompt` du navigateur.

## 10. Tailles d'écran

Toujours vérifier **390, 900, 1 280 et 1 600 px**, dans Chrome et Safari (`bash outils/avant-mise-en-ligne.sh --navigateur`).

- Téléphone (≤ 640 px) : filtres repliés derrière « Filtres » + résumé du choix (`A.enteteFiltres`, zone `.ftel`, filtres `.ftel-z`) ; zones à toucher ≥ 44 px ;
  rien ne déborde en largeur ; rien sous « + Prescrire ».
- Tablette (dossier de 720 à 1 279 px) : deux colonnes, colonne Patient de 290 px à gauche, onglets visibles sans défiler.
- Ordinateur (≥ 1 280 px) : trois colonnes du dossier ; les filtres d'une page tiennent sur une ligne quand c'est possible.

## 11. Avant de livrer un nouvel écran

1. Couleurs, tailles, ombres et arrondis pris dans `:root` ; aucune valeur en dur.
2. Une seule action principale par zone ; boutons voisins de même hauteur.
3. Libellés en français, sans majuscules d'affichage ; icônes dessinées.
4. Les quatre largeurs, Chrome et Safari ; un test dans `tests/` qui mesure ce qui compte (hauteurs, alignements, débordement).
5. Ce guide mis à jour si une règle change.
