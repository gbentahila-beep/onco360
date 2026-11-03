import pathlib; __file__=str(pathlib.Path(__file__).resolve()); exec(open(pathlib.Path(__file__).parent/'base.py').read())
# IG7 (03/11/2026, phase IG, idées 15 et 16) : dossier en deux colonnes dès la tablette (colonne Patient de 290 px à gauche, onglets visibles
# sans défiler ; rien ne change à 1 280 px et plus ni au téléphone) ; téléphone : « Filtres » + résumé du choix (Bilan, Protocoles, RCP), rien
# sous « + Prescrire » ; Salle à 390 px : « à jour à … » ne touche plus « + Rendez-vous ».
ok_n = ko_n = 0
def ok(c, m, d=None):
    global ok_n, ko_n
    if c: ok_n += 1; print('  ✔ ' + m)
    else: ko_n += 1; print('  ✘ ' + m + ('' if d is None else ' ' + str(d)[:500]))
U = f'http://localhost:{PORT}/v2.html#'
PID = 'P20260928029'
ZONES = """(() => { const d = document.getElementById('dos'), z = {}; ['bandeau', 'travail', 'patient', 'barre'].forEach(k => { const e = d.querySelector('[data-zone=' + k + ']'); const r = e.getBoundingClientRect();
  z[k] = [Math.round(r.left), Math.round(r.top), Math.round(r.width), Math.round(r.bottom), !!e.offsetParent] }); const o = document.querySelector('#dos .o-barre').getBoundingClientRect();
  return [z, Math.round(o.bottom), innerHeight, document.documentElement.scrollWidth <= innerWidth + 1] })()"""
async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        print('Dossier sur tablette')
        for w, h in ((768, 1024), (900, 1000), (1024, 768), (1180, 820)):
            pg = await ouvrir(b, S, w=w, h=h); ev = pg.evaluate
            await pg.goto(U + 'dossier/' + PID); await pg.wait_for_timeout(2600)
            z, ob, ih, deb = await ev(ZONES)
            ok(z['patient'][2] == 290 and z['patient'][0] < z['travail'][0] and z['patient'][1] == z['travail'][1], f'{w} px : colonne Patient de 290 px à gauche, onglets et contenu à droite', z)
            ok(ob < ih and z['barre'][4], f'{w} px : onglets du dossier visibles sans défiler, barre en bas', [ob, ih])
            ok(deb, f'{w} px : rien ne déborde')
            ok(not pg.errs, f'{w} px : aucune erreur JavaScript', pg.errs[:2]); await pg.close()
        pg = await ouvrir(b, S, w=1440, h=900); ev = pg.evaluate
        await pg.goto(U + 'dossier/' + PID); await pg.wait_for_timeout(2600)
        z, ob, ih, deb = await ev(ZONES)
        large = z['barre'][2] >= 1280
        ok((z['patient'][2] == 300 and z['bandeau'][2] == 300) if large else (z['patient'][2] == 290 and z['patient'][0] < z['travail'][0]), '1 440 px : dossier de 1 280 px et plus inchangé (colonne Patient de 300 px), sinon deux colonnes', [large, z])
        await pg.close()
        pg = await ouvrir(b, S, w=900, h=1000); ev = pg.evaluate
        await pg.goto(U + 'dossier/' + PID + '/chimio'); await pg.wait_for_timeout(2600)
        await ev("document.querySelector('.dos-sw button:nth-child(2), .dos-sw [data-v=docs]') && document.querySelector('.dos-sw button:nth-child(2), .dos-sw [data-v=docs]').click()"); await pg.wait_for_timeout(500)
        r = await ev("(() => { const e = document.querySelector('#dos [data-zone=documents]'); if (!e || !e.offsetParent) return null; const r = e.getBoundingClientRect(); return [Math.round(r.left), Math.round(r.width)] })()")
        ok(r and r[1] == 290, '900 px : « Documents » s\'affiche dans la colonne de gauche', r)
        ok(not pg.errs, '900 px : aucune erreur JavaScript', pg.errs[:2]); await pg.close()

        print('Téléphone : « Filtres »')
        for page, zone in (('bilan', '#page .carte.ftel'), ('protocoles', '#page .ftel'), ('rcp', '#page .rcp-haut.ftel')):
            pg = await ouvrir(b, S, w=390, h=844); ev = pg.evaluate
            await pg.goto(U + page); await pg.wait_for_timeout(2600)
            await pg.wait_for_selector(zone + ' .ftel-b', timeout=8000)
            r = await ev(f"""(() => {{ const z = document.querySelector('{zone}'); if (!z) return null; const b = z.querySelector('.ftel-b'), cach = [...z.querySelectorAll('.ftel-z')];
              return [!!b.offsetParent, Math.round(b.getBoundingClientRect().height), z.querySelector('.ftel-r').textContent, cach.length, cach.every(e => !e.offsetParent && getComputedStyle(e).display === 'none')] }})()""")
            ok(r and r[0] and r[1] >= 44 and r[2] and r[3] and r[4], f'390 px : {page} : « Filtres » (44 px) et résumé « {r and r[2]} », filtres repliés', r)
            if page == 'bilan':
                k = await ev("(() => { const k = document.querySelector('.kpi .k'); const r = k.getBoundingClientRect(); return r.bottom <= innerHeight })()")
                ok(k, '390 px : bilan : 1re carte des chiffres visible sans défiler')
            if page == 'protocoles':
                ok(await ev("!!document.querySelector('#prQ').offsetParent && !!document.querySelector('#prL .pcarte').offsetParent"), '390 px : protocoles : recherche et liste visibles')
            await pg.click(zone + ' .ftel-b'); await pg.wait_for_timeout(300)
            r = await ev(f"[document.querySelector('{zone}').classList.contains('ouv'), [...document.querySelectorAll('{zone} .ftel-z')].every(e => !!e.offsetParent || (getComputedStyle(e).display === 'contents' && [...e.children].some(c => !!c.offsetParent))), document.querySelector('{zone} .ftel-b').getAttribute('aria-expanded')]")
            ok(r == [True, True, 'true'], f'390 px : {page} : un clic ouvre les filtres', r)
            if page == 'bilan':
                await pg.select_option('#biHop', index=1); await pg.wait_for_timeout(700)
                r = await ev("[document.querySelector('.carte.ftel').classList.contains('ouv'), document.querySelector('.ftel-r').textContent, document.querySelector('.ftel-b .n').textContent]")
                ok(r[0] and ' · ' in r[1] and r[2] == '1', '390 px : bilan : un choix laisse les filtres ouverts, résumé et nombre de filtres à jour', r)
                await ev("biF('hop','tous')"); await pg.wait_for_timeout(500)
            if page == 'protocoles':
                c = await ev("[...document.querySelector('.pr-casc select').options].map(o => o.value).filter(Boolean)[0]")
                await pg.select_option('.pr-casc select', c); await pg.wait_for_timeout(500)
                r = await ev("[document.querySelector('.ftel-r').textContent, document.querySelector('.ftel-b .n').textContent]")
                ok(r[0].startswith(c) and r[1] == '1', f'390 px : protocoles : résumé « {r[0]} » et nombre à jour', r)
            if page == 'rcp':
                await ev("rcpFiltre('afaire')"); await pg.wait_for_timeout(400)
                ok(await ev("document.querySelector('.ftel-r').textContent.endsWith('À faire') && document.querySelector('.rcp-haut').classList.contains('ouv')"), '390 px : rcp : « À faire » dans le résumé, filtres restés ouverts')
            await pg.click(zone + ' .ftel-b'); await pg.wait_for_timeout(300)
            ok(await ev(f"[...document.querySelectorAll('{zone} .ftel-z')].every(e => !e.offsetParent)"), f'390 px : {page} : un 2e clic les replie')
            ok(await ev("document.documentElement.scrollWidth <= innerWidth + 1"), f'390 px : {page} : rien ne déborde')
            ok(not pg.errs, f'390 px : {page} : aucune erreur JavaScript', pg.errs[:2]); await pg.close()
        for page in ('bilan', 'protocoles', 'rcp'):
            pg = await ouvrir(b, S, w=1440, h=900); ev = pg.evaluate
            await pg.goto(U + page); await pg.wait_for_timeout(2600)
            r = await ev("[[...document.querySelectorAll('.ftel-t')].some(e => !!e.offsetParent), [...document.querySelectorAll('.ftel-z')].every(e => !!e.offsetParent || getComputedStyle(e).display === 'contents')]")
            ok(r == [False, True], f'1 440 px : {page} : filtres affichés comme avant, sans bouton « Filtres »', r)
            await pg.close()

        print('Téléphone : dossier et Salle')
        for o in ('consultation', 'chimio', 'patient', 'radiotherapie'):
            pg = await ouvrir(b, S, w=390, h=844); ev = pg.evaluate
            await pg.goto(U + 'dossier/' + PID + '/' + o); await pg.wait_for_timeout(2600)
            await ev("window.scrollTo(0, document.documentElement.scrollHeight)"); await pg.wait_for_timeout(400)
            r = await ev("""(() => { const f = document.querySelector('.dos-fab').getBoundingClientRect(); const bas = [...document.querySelectorAll('#dos [data-zone=travail] .carte, #dos [data-zone=patient] .carte')]
              .filter(e => e.offsetParent).map(e => e.getBoundingClientRect().bottom); return [Math.round(f.top), Math.round(Math.max(...bas))] })()""")
            ok(r[1] <= r[0], f'390 px : dossier › {o} : en bas de page, rien sous « + Prescrire »', r)
            await pg.close()
        pg = await ouvrir(b, S, w=390, h=844); ev = pg.evaluate
        await pg.goto(U + 'salle'); await pg.wait_for_timeout(2600)
        r = await ev("""(() => { const a = document.getElementById('saAjour').getBoundingClientRect(), b = [...document.querySelectorAll('#page button')].find(x => x.textContent.includes('Rendez-vous')).getBoundingClientRect();
          return [document.getElementById('saAjour').textContent, Math.round(a.bottom), Math.round(b.top)] })()""")
        ok(r[0].startswith('à jour') and r[1] <= r[2], '390 px : Salle : « à jour à … » au-dessus de « + Rendez-vous », sans le toucher', r)
        r = await ev("[...['saFtr', 'saAct'].map(i => { const b = document.getElementById(i).getBoundingClientRect(); return [Math.round(b.top), Math.round(b.height)] }), Math.round(document.getElementById('saAjour').getBoundingClientRect().top), Math.round(document.getElementById('saAct').getBoundingClientRect().bottom)]")
        ok(r[0] == r[1] and r[0][1] >= 44 and r[2] >= r[3], '390 px : Salle : « Filtres » et « Actualiser » alignés (même haut, même hauteur), « à jour à … » dessous', r)
        ok(not pg.errs, 'aucune erreur JavaScript', pg.errs[:2]); await pg.close()
        print('Bilan sur ordinateur : une seule ligne')
        for w in (900, 1024, 1280, 1440):
            pg = await ouvrir(b, S, w=w, h=800); ev = pg.evaluate
            await pg.goto(U + 'bilan'); await pg.wait_for_timeout(2600)
            r = await ev("""(() => { const e = [...document.querySelectorAll('.bi-ligne select'), document.querySelector('.bi-act .bp-maj > .bt'), document.querySelector('.bi-act .mpts > .sa-plus')].map(x => x.getBoundingClientRect());
              return [e.map(x => Math.round(x.top)), e.slice(1).map((x, i) => Math.round(x.left - e[i].right)), e.map(x => Math.round(x.height))] })()""")
            ok(len(set(r[0])) == 1 and all(g >= 11 for g in r[1]) and all(h == 44 for h in r[2]), f'{w} px : Bilan : filtres, « Actualiser » et « ⋯ » sur une ligne, écart de 12 px au moins, hauteur 44 px', r)
            await pg.close()
        print('Téléphone : boutons du haut alignés')
        TAILLE = "(s) => { const e = document.querySelector(s); if (!e) return null; const r = e.getBoundingClientRect(); return [Math.round(r.top), Math.round(r.width), Math.round(r.height)] }"
        for page, sels in (('salle', ['#saFtr', '#saAct', '.sa-pts']), ('bilan', ['.ftel-b', '.bi-act .bp-maj > .bt', '.bi-act .mpts > .sa-plus']), ('protocoles', ['.ftel-b', '.pr-rech > .bt', '.pr-act .mpts > .sa-plus'])):
            pg = await ouvrir(b, S, w=390, h=844); ev = pg.evaluate
            await pg.goto(U + page); await pg.wait_for_timeout(2600)
            r = await ev(f"(() => {{ const t = {TAILLE}; return {json.dumps(sels)}.map(t) }})()")
            ok(all(r) and r[0][0] == r[1][0] == r[2][0] and r[0][1] == r[1][1] and r[0][2] == r[1][2] == r[2][2] == 44 and r[2][1] == 44,
               f'390 px : {page} : « Filtres » et le 2e bouton de même largeur, « ⋯ » carré de 44 px, sur une ligne', r)
            if page == 'protocoles':
                r2 = await ev(f"(() => {{ const t = {TAILLE}; return ['#prQ', '.pr-act .b1'].map(t) }})()")
                ok(r2[0][1] == r2[1][1] == r[0][1] + r[1][1] + r[2][1] + 20, '390 px : protocoles : recherche et « Créer un protocole » sur toute la largeur', [r, r2])
            await pg.close()
        await b.close()
    print(f'\n{ok_n} réussis, {ko_n} échoués')
asyncio.run(main())
