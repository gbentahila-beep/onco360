# Lot 4 RTX (01/11/2026) : page Contourage du référentiel de radiothérapie (#radiotherapie/contourage[/<localisation>]) : menus Région et Localisation,
# tableaux sourcés de donnees-rt/contourage/<région>.json, sources numérotées, phrase « pas d'atlas publié », lien depuis l'onglet Contourage de la fiche.
import pathlib; __file__=str(pathlib.Path(__file__).resolve()); exec(open(pathlib.Path(__file__).parent/'base.py').read())
ok_n = ko_n = 0
def ok(c, m, d=None):
    global ok_n, ko_n
    if c: ok_n += 1; print('  ✔ ' + m)
    else: ko_n += 1; print('  ✘ ' + m + ('' if d is None else ' ' + str(d)[:300]))
REG = json.loads((pathlib.Path(__file__).parent.parent / 'public/donnees-rt/index.json').read_text())['regions']
DEBORDE = "document.documentElement.scrollWidth > window.innerWidth + 1"
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await ouvrir(b, S); ev = pg.evaluate
        await pg.goto(f'http://localhost:{PORT}/v2.html#radiotherapie/contourage/oropharynx'); await pg.wait_for_timeout(3000)
        t = await ev("document.getElementById('rtrSous').innerText")
        ok('Contourage' in await ev("document.querySelector('.rtr-sous .on').innerText"), 'sous-page Contourage sélectionnée')
        ok('Niveaux ganglionnaires cervicaux' in t and 'Biau' in t and 'Grégoire' in t and 'CTV de la tumeur (CTV-P2) selon le T : oropharynx' in t and 'larynx (glotte' not in t, 'oropharynx : limites, CTV-P par T, sélection, sources ; pas les tableaux du larynx')
        ok(await ev("document.querySelectorAll('.rtr-cts table').length") >= 4 and await ev("document.querySelectorAll('.rtr-cts a[href^=\"https://doi.org/\"]').length") >= 3, 'tableaux et liens DOI des sources')
        await pg.select_option('#rtrCl', 'glandes_salivaires'); await pg.wait_for_timeout(1200)
        ok("Pas d'atlas publié" in await ev("document.getElementById('rtrSous').innerText"), 'glandes salivaires : pas d\'atlas publié')
        for r in REG:
            await pg.goto(f'http://localhost:{PORT}/v2.html#radiotherapie'); await pg.wait_for_timeout(300)
            await pg.goto(f'http://localhost:{PORT}/v2.html#radiotherapie/contourage'); await pg.wait_for_timeout(1500)
            await pg.select_option('#rtrCr', r['id']); await pg.wait_for_timeout(1200)
            n = await ev("document.querySelectorAll('.rtr-cts table').length")
            ok(n > 0 or r['id'] == 'autres', f"région {r['nom']} : {n} tableau(x)")
        await pg.goto(f'http://localhost:{PORT}/v2.html#radiotherapie/s/pro-fav-60-20/contourage'); await pg.wait_for_timeout(2500)
        await pg.click("text=Atlas de contourage de la localisation"); await pg.wait_for_timeout(2000)
        ok((await ev("location.hash")).endswith('contourage/prostate') and await ev("document.getElementById('rtrCl').value") == 'prostate', 'lien de la fiche vers la page, localisation choisie')
        ok(not pg.errs, 'aucune erreur JavaScript', pg.errs[:2]); await pg.close()
        for w, h in [(1280, 900), (390, 800)]:
            pg = await ouvrir(b, S, w=w, h=h); ev = pg.evaluate
            await pg.goto(f'http://localhost:{PORT}/v2.html#radiotherapie/contourage/larynx'); await pg.wait_for_timeout(2500)
            ok(not await ev(DEBORDE), f'{w} px : sans débordement'); await pg.close()
        await b.close()
    print(f'\n{ok_n} réussis, {ko_n} échoués')
asyncio.run(main())
