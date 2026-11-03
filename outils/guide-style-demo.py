#!/usr/bin/env python3
# IG8 (03/11/2026) : page de démonstration du guide de style (docs/guide-de-style.md), HORS du site : reprend le CSS et les icônes de
# public/v2.html tels qu'ils sont, et montre chaque composant commun. Jamais publiée (docs/ n'est pas dans public/, fichier non versionné).
# Utilisation : python3 outils/guide-style-demo.py  →  docs/guide-de-style-demo.html (ouvrir dans le navigateur)
import pathlib, re
ICI = pathlib.Path(__file__).resolve().parent.parent
v2 = (ICI / 'public' / 'v2.html').read_text(encoding='utf-8')
css = v2[v2.index('<style>') + 7:v2.index('</style>')].replace('url(vendor/', 'url(../public/vendor/')
deb = v2.index('<svg width="0" height="0" style="position:absolute"')
icones = v2[deb:v2.index('</svg>', deb) + 6]
ic = lambda n: '<svg class="i" aria-hidden="true"><use href="#i-' + n + '"/></svg>'
COUL = ['prim', 'prim-c', 'vert', 'vert-c', 'orange', 'orange-c', 'rouge', 'rouge-c', 'encre', 'doux', 'trait', 'fond']
corps = f'''
<h1>Guide de style d'Onco360</h1><p class="sous">Démonstration des composants communs (phase IG). Règles : docs/guide-de-style.md.</p>
<section class="carte"><h3>Couleurs (une teinte par sens)</h3><div class="demo-c">{''.join(f'<div><i style="background:var(--{c})"></i><code>--{c}</code></div>' for c in COUL)}</div></section>
<section class="carte"><h3>Texte</h3>{''.join(f'<p style="font-size:var(--t{i});margin:4px 0">--t{i} : Patient fictif, cure C2 J8</p>' for i in range(1, 9))}</section>
<section class="carte"><h3>Boutons : 4 sortes × 3 hauteurs</h3>
<div class="demo-l"><button class="b1">{ic('plus')}Principal</button><button class="b2">{ic('actualiser')}Secondaire</button><span class="mpts"><button class="mini sa-plus" title="Autres actions">⋯</button></span><button class="b2 danger">{ic('corbeille')}Supprimer</button></div>
<div class="demo-l"><button class="b2" style="min-height:36px">36 px (liste)</button><button class="b2">40 px (haut de page)</button><button class="b2" style="min-height:44px">44 px (au doigt)</button></div></section>
<section class="carte"><h3>Champs</h3><div class="form" style="grid-template-columns:repeat(3,minmax(0,1fr))"><div><label>Période</label><select><option>Mois en cours</option></select></div>
<div><label>Établissement</label><select><option>Tous</option></select></div><div><label>Recherche</label><input placeholder="ex. FOLFOX, prostate…"></div></div></section>
<section class="carte"><h3>Choix, onglets, badges, compteurs</h3>
<div class="demo-l"><span class="choix"><button class="puce on">Tous <span class="nb">12</span></button><button class="puce">À faire <span class="nb">3</span></button><button class="puce">Faits</button></span></div>
<div class="demo-l"><span class="badge b-ch">Chimio C1/1</span><span class="badge b-rt">RT en cours</span><span class="pc-mol">Cisplatine, 5-fluoro-uracile</span></div></section>
<section class="carte"><h3>Tableau trié</h3><div class="ta-tab"><div class="ta-h" role="row"><span role="columnheader" aria-sort="ascending"><button class="th-tri on">Patient<span class="th-f">▲</span></button></span>
<span role="columnheader" aria-sort="none"><button class="th-tri">Échéance<span class="th-f">↕</span></button></span></div></div></section>
<section class="carte"><h3>État vide</h3><p class="sous">Une illustration, un titre, une phrase qui dit quoi faire.</p></section>
'''
page = f'''<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Guide de style – Onco360</title>
<style>{css}
body{{padding:24px;max-width:1100px;margin:0 auto}}.carte{{margin:0 0 18px}}.demo-l{{display:flex;flex-wrap:wrap;gap:12px;align-items:center;margin:10px 0}}
.demo-c{{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px}}.demo-c div{{display:flex;align-items:center;gap:8px}}.demo-c i{{width:28px;height:28px;border-radius:8px;border:1px solid var(--trait)}}</style></head>
<body>{icones}{corps}</body></html>'''
sortie = ICI / 'docs' / 'guide-de-style-demo.html'
sortie.write_text(page, encoding='utf-8')
print('écrit :', sortie)
