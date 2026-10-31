import pathlib; __file__=str(pathlib.Path(__file__).resolve()); exec(open(pathlib.Path(__file__).parent/'base.py').read())
# L3 (31/10/2026) : captures du guide de démarrage (public/guide/images), prises sur le jeu de test FICTIF (aucun vrai patient).
# Refaire :  cd tests && .venv/bin/python guide_captures.py   puis   python3 ../outils/guide-html.py
OUT = ICI.parent / 'public' / 'guide' / 'images'
U = f'http://localhost:{PORT}/v2.html#'
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await ouvrir(b, S, w=1280, h=800, t="2026-10-06T10:00:00"); ev = pg.evaluate
        k = next(k for k in S if k.startswith(E + 'patients/')).split('/')[-1]
        async def cap(nom, h, f=None, t=2200):
            await pg.goto(U + h); await pg.wait_for_timeout(t)
            if f: await ev(f); await pg.wait_for_timeout(900)
            await pg.screenshot(path=str(OUT / (nom + '.jpg')), type='jpeg', quality=70)
            print('  ' + nom)
        await cap('tableau-de-bord', 'accueil')
        await cap('nouveau-patient', 'patients', 'window.nouveauPatient()')
        await cap('dossier', 'dossier/' + k, None, 3000)
        await cap('agenda', 'agenda')
        await cap('salle-attente', 'salle')
        await cap('parametres', 'parametres')
        await cap('import-patients', 'parametres/export', "document.getElementById('ipCarte').scrollIntoView()")
        await b.close()
asyncio.run(main())
