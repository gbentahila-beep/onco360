import pathlib; __file__=str(pathlib.Path(__file__).resolve()); exec(open(pathlib.Path(__file__).parent/'base.py').read())
# UX10 (01/11/2026) : Outils cliniques › Stadification, « Importer des tableaux (fichier) » (fiches du cabinet préparées depuis son manuel).
# Fichier d'essai fictif ; ONCO360_TNM=<chemin> importe en plus un vrai fichier (jamais dans le dépôt) et vérifie toutes ses fiches.
import json, os, sys, tempfile
ok_n = ko_n = 0
def ok(c, m, d=None):
    global ok_n, ko_n
    if c: ok_n += 1; print('  ✔ ' + m)
    else: ko_n += 1; print('  ✘ ' + m + ('' if d is None else ' ' + str(d)[:400]))
U = f'http://localhost:{PORT}/v2.html#'
FICT = {"larynx": {"source": "Manuel fictif", "edition": "Édition d'essai", "note": "",
  "c": {"t": [{"cat": "T1 a", "def": "Définition fictive"}, {"cat": "T2 b", "def": "Définition fictive 2"}], "n": [{"cat": "N0", "def": "Fictif"}], "m": [{"cat": "M0", "def": "Fictif"}],
        "stades": [{"stade": "I", "t": "T1 a", "n": "N0", "m": "M0"}, {"stade": "II", "t": "T2 b", "n": "Tout", "m": "M0"}]},
  "p": {"t": [], "n": [], "m": [], "stades": []}, "annexes": [{"titre": "Notes", "lignes": [{"a": "Note", "b": "Texte fictif"}]}]},
  "inconnu-xyz": {"c": {}}}
import re
SRC = (pathlib.Path(__file__).parent.parent / 'public/js/donnees/outilscliniques.js').read_text()
LOC = {}
for m in re.finditer(r'\{ id: "([^"]+)", nom: "[^"]+", sous: \[(.*?)\] \}', SRC, re.S):
    for sid in re.findall(r'\["([^"]+)", "', m.group(2)): LOC[sid] = m.group(1)
async def importer(pg, chemin, oui=True):
    await pg.set_input_files('.oc-imp input[type=file]', chemin); await pg.wait_for_timeout(600)
    t = await pg.evaluate("document.querySelector('.or-dlg') ? document.querySelector('.or-dlg').innerText : ''")
    await pg.click('.or-dlg .bt.plein' if oui else '.or-dlg .bt.gris'); await pg.wait_for_timeout(1200)
    return t
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await ouvrir(b, S); ev = pg.evaluate
        f = pathlib.Path(tempfile.gettempdir()) / 'tnm-fictif.json'; f.write_text(json.dumps(FICT, ensure_ascii=False))
        await pg.goto(U + 'outils/tnm'); await pg.wait_for_timeout(2200)
        ok(await ev("!!document.querySelector('.oc-imp input[type=file]')"), 'bouton « Importer des tableaux (fichier) » pour le médecin')
        t = await importer(pg, str(f), oui=False)
        ok('Importer 1 fiche' in t and 'Larynx' in t, 'confirmation : 1 fiche reconnue (la clé inconnue est ignorée)', t)
        ok('Rempli' not in await ev("document.querySelector('.oc-carte[onclick*=larynx]').innerText"), 'Annuler : rien d\'importé')
        await importer(pg, str(f))
        ok("Rempli · Édition d'essai" in await ev("document.querySelector('.oc-carte[onclick*=larynx]').innerText"), 'importé : carte « Rempli » avec l\'édition')
        await pg.goto(U + 'outils/tnm/orl/larynx'); await pg.wait_for_timeout(1800)
        tx = await ev("document.getElementById('ocMain').innerText")
        ok('Définition fictive' in tx and 'Texte fictif' in tx and 'Manuel fictif' in tx, 'fiche : définitions, annexes et source affichées')
        await pg.select_option('#ocSt', 'T2 b'); await pg.select_option('#ocSn', 'N0'); await pg.select_option('#ocSm', 'M0'); await pg.wait_for_timeout(200)
        ok('Stade : II' in await ev("document.getElementById('ocStadeR').innerText"), 'calcul du stade (« Tout » dans N)')
        await pg.goto(U + 'outils/tnm'); await pg.wait_for_timeout(1800)
        t = await importer(pg, str(f), oui=False)
        ok('déjà remplie sera remplacée' in t, 'nouvel import : la fiche déjà remplie est signalée', t)
        vrai = os.environ.get('ONCO360_TNM')
        if vrai:
            J = json.load(open(vrai)); await pg.goto(U + 'outils/tnm'); await pg.wait_for_timeout(1800)
            t = await importer(pg, vrai)
            n = await ev("document.querySelectorAll('.oc-carte .b-ch').length")
            ok(n == len(J), f'vrai fichier : {len(J)} fiches importées', n)
            fautes = []
            for sid, F in J.items():
                await pg.goto(U + 'outils/tnm/' + LOC[sid] + '/' + sid); await pg.wait_for_timeout(700)
                for r in F['c']['stades'][:40]:
                    v = [r[k].split(', ')[0] if r[k] != 'Tout' else None for k in 'tnm']
                    if None in v: continue
                    await pg.select_option('#ocSt', v[0]); await pg.select_option('#ocSn', v[1]); await pg.select_option('#ocSm', v[2])
                    res = await ev("document.getElementById('ocStadeR').innerText")
                    if r['stade'] not in res: fautes.append((sid, v, r['stade'], res))
            ok(not fautes, 'vrai fichier : chaque ligne de stade se retrouve par le calcul', fautes[:5])
        ok(not pg.errs, 'aucune erreur JavaScript', pg.errs[:2]); await pg.close()
        pg = await ouvrir(b, S, w=390)
        await pg.goto(U + 'outils/tnm'); await pg.wait_for_timeout(1800)
        ok(not await pg.evaluate("document.documentElement.scrollWidth > innerWidth + 1"), '390 px : page Stadification sans débordement'); await pg.close()
        await b.close()
    print(f'\n{ok_n} réussis, {ko_n} échoués'); sys.exit(1 if ko_n else 0)
asyncio.run(main())
