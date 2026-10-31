#!/usr/bin/env python3
# L3 (31/10/2026) : guide/demarrage.md → public/guide/demarrage.html (page du site, ouverte depuis le menu du compte d'Onco360).
# Lancer après toute modification du guide :  python3 outils/guide-html.py
import pathlib, re, markdown
R = pathlib.Path(__file__).resolve().parent.parent
md = (R / 'guide' / 'demarrage.md').read_text(encoding='utf-8').replace('../public/guide/images/', 'images/')
corps = markdown.markdown(md, extensions=['extra'])
# une partie par page imprimée (médecin page 1, page 2, secrétaire page 1, page 2)
corps = re.sub(r'<h2>', '<h2 class="saut">', corps)
page = '''<!DOCTYPE html>
<html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<link rel="icon" type="image/png" href="../onco360-icone.png">
<title>Onco360 – Guide de démarrage</title>
<!-- Page produite par outils/guide-html.py depuis guide/demarrage.md : modifier le .md, puis relancer le script -->
<style>
:root{--n:#3563B0}*{box-sizing:border-box}
body{font-family:Arial,Helvetica,sans-serif;margin:0;background:#F5F7FB;color:#262838;font-size:15px;line-height:1.6}
main{max-width:900px;margin:24px auto;padding:0 16px 40px}
.card{background:#fff;border-radius:16px;padding:22px 26px;box-shadow:0 1px 4px rgba(0,0,0,.08)}
h1{font-size:24px;color:#1D3F94;margin:0 0 8px}h2{font-size:19px;color:var(--n);margin:30px 0 10px;padding-top:10px;border-top:1px solid #E3E7F0}
li{margin:6px 0}img{max-width:100%;height:auto;border:1px solid #E3E7F0;border-radius:10px;margin:10px 0;display:block}
.imp{display:inline-flex;align-items:center;min-height:44px;padding:0 16px;border-radius:8px;border:1px solid var(--n);background:#fff;color:var(--n);font:inherit;font-weight:bold;cursor:pointer}
@media print{body{background:#fff;font-size:12.5px}.card{box-shadow:none;padding:0}.imp{display:none}h2.saut{break-before:page;border:0}h2.saut:first-of-type{break-before:auto}img{max-height:9cm;width:auto}}
@media (max-width:600px){.card{padding:16px}}
</style></head>
<body><main><div class="card">
<p><button type="button" class="imp" onclick="print()">Imprimer le guide</button></p>
''' + corps + '''
</div></main></body></html>
'''
(R / 'public' / 'guide' / 'demarrage.html').write_text(page, encoding='utf-8')
print('public/guide/demarrage.html écrit')
