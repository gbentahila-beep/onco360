# Fiches IDÉE, lot 1 (étape 4, 02/11/2026)

Page publiée (privée) : https://claude.ai/artifact/5kuQDn8gjMgimsCHWfFMZP — avant / après sur la copie de test (jeu fictif), maquettes = style posé
le temps de la capture (scripts du scratchpad `audit/fiches*.py`), rien de changé dans le code.

| N° | Idée | Constats | Priorité | Complexité | Réponse |
|---|---|---|---|---|---|
| 1 | Recherche de patient fiable (classement, « 6 sur 23 », une règle : nom, n°, tél., ddn, CIN) | FN1, FN2 | Critique | Faible || **OUI** |
| 2 | Imprimer chaque rendez-vous (⋯ de chaque ligne) + feuille A5 complète (« À savoir » réglable) | D1, IM1, IM2 | Haute | Moyenne || **OUI, modifié** : en-tête = « Dr … » + spécialité seulement (ni cabinet, ni adresse, ni téléphone) ; pas de n° de dossier ; « En cas d’empêchement, prévenez le plus tôt possible. » ; format A4 ou A5 au choix dans Paramètres › Impression (demande du 02/11) |
| 3 | ⋯ discret dans les listes du dossier (sans cadre, lignes 40 px, 44 px au téléphone) | D2 | Haute | Faible || **OUI** |
| 4 | Pastille chiffrée entière (`.pr{overflow:hidden}` v2.html:294) | D4 | Haute | Faible || **OUI** |
| 5 | 4 sortes de boutons × 3 hauteurs ; cadre fin de la ligne ouverte ; bordure des champs ~3:1 | T2, U8, U3, F6 | Haute | Moyenne || **OUI** |
| 6 | Squelette de la page demandée pendant le chargement, bon titre, menu après les droits | T1 | Haute | Moyenne à élevée || **OUI** |
| 7 | Un seul défilement (tableau de bord) : A = 5 lignes + « Voir les 45 » ; B = tout, sans défilement interne | T5 | Haute | Faible || **OUI, choix A** (5 lignes + « Voir les N … › » qui déplie) |
| 8 | Protocole ouvert en lecture (Modifier, Dupliquer ; Signaler, Supprimer dans ⋯) | P1, P2 | Haute | Moyenne || **OUI** |

Déjà accepté : D3 (traitement systémique, sous-titre + liste des bibliothèques).
Écartés du lot (liste « Refusé ») : FN6 (molécules repliées, trop proche de U6 refusé le 20/10). Idée 7 : U24 refusé (RT repliée) signalé dans la fiche.
Lot 2 prévu : FN3 synonymes, FN5 tri, U2 pastilles, T4 majuscules, U9 onglets, U10 compteurs, U14 tablette, T8 / F1 téléphone, CO1, PA1, FN4.

Réponses de Dr Bentahila le 02/11/2026 : tout accepté (2 modifié, 7 choix A). Lot 2 demandé.
