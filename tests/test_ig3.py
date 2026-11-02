import pathlib; __file__=str(pathlib.Path(__file__).resolve()); exec(open(pathlib.Path(__file__).parent/'base.py').read())
# IG3 (02/11/2026, phase IG, idées 3, 5, 12, 13, 14 et D2) : composants communs. Boutons (secondaire blanc à cadre gris-bleu), bordure des champs
# (3,2 pour 1, bleue quand on écrit), ⋯ sans cadre, plus de majuscules (titres de la colonne Patient, molécules), un seul groupe de choix (bleu
# Onco360), compteurs en pastille après le mot ; pages à 390, 900, 1 280 et 1 600 px sans débordement ni erreur.
ok_n = ko_n = 0
def ok(c, m, d=None):
    global ok_n, ko_n
    if c: ok_n += 1; print('  ✔ ' + m)
    else: ko_n += 1; print('  ✘ ' + m + ('' if d is None else ' ' + str(d)[:500]))
U = f'http://localhost:{PORT}/v2.html#'
PID = 'P20260928029'
CONTRASTE = """([a, b]) => { const L = (c) => { const m = c.match(/\\d+(\\.\\d+)?/g).slice(0, 3).map(Number).map((v) => v / 255).map((v) => v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4)); return 0.2126 * m[0] + 0.7152 * m[1] + 0.0722 * m[2]; };
  const x = L(a), y = L(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); }"""
async def aller(pg, r, t=2300):
    await pg.goto(U + r); await pg.reload(); await pg.wait_for_timeout(t)
async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await ouvrir(b, S, w=1440); ev = pg.evaluate
        # ───── dossier : ⋯ sans cadre, titres sans majuscules, ligne ouverte, boutons secondaires ─────
        await aller(pg, 'dossier/' + PID + '/chimio', 2800)
        r = await ev("""(() => { const p = document.querySelector('#dos .rc .mpts > .sa-plus'), s = getComputedStyle(p), q = p.getBoundingClientRect();
          return [s.borderTopColor, s.backgroundColor, Math.round(q.width), Math.round(q.height)]; })()""")
        ok(r[0] in ('rgba(0, 0, 0, 0)', 'transparent') and r[1] in ('rgba(0, 0, 0, 0)', 'transparent') and r[2] == 40 and r[3] == 40, 'D2 : ⋯ des listes du dossier sans cadre, 40 × 40 px', r)
        r = await ev("[...document.querySelectorAll('details.dp > summary .dp-t')].map(e => getComputedStyle(e).textTransform)")
        ok(r and all(t == 'none' for t in r), 'idée 12 : titres de la colonne Patient en écriture normale', r)
        r = await ev("(() => { const e = document.querySelector('.acc.on'); if (!e) return null; const s = getComputedStyle(e); return [s.borderTopWidth, s.borderTopColor]; })()")
        ok(r and r[0] == '1px' and r[1] == 'rgb(53, 99, 176)', 'idée 5 : cadre fin bleu pour la ligne de chimio ouverte', r)
        r = await ev("(() => { const e = [...document.querySelectorAll('#dos .bt.clair')].find(b => b.getBoundingClientRect().width); const s = getComputedStyle(e); return [s.color, s.borderTopColor, s.backgroundColor, Math.round(e.getBoundingClientRect().height)]; })()")
        ok(r[0] == 'rgb(0, 38, 76)' and r[1] == 'rgb(183, 198, 218)' and r[2] == 'rgb(255, 255, 255)' and 36 <= r[3] <= 40, 'idée 5 : bouton secondaire blanc, cadre gris-bleu, texte foncé', r)
        r = await ev("(() => { const e = document.querySelector('.m3 > summary.mini'); if (!e) return null; const s = getComputedStyle(e); return [s.borderTopColor, s.backgroundColor]; })()")
        ok(r and r[0] in ('rgba(0, 0, 0, 0)', 'transparent'), 'idée 5 : ⋯ de la ligne de chimio discret (sans cadre)', r)
        r = await ev("(() => { const e = document.querySelector('.o-barre .n'); const s = getComputedStyle(e); return [s.color, s.backgroundColor, e.closest('button').classList.contains('on')]; })()")
        c = await ev(CONTRASTE, [r[0], r[1]])
        ok(c >= 4.5, f'idée 14 : compteur des onglets du dossier lisible ({c:.2f} pour 1)', r)
        # champs : bordure 3,2 pour 1, bleue quand on écrit
        await ev("document.getElementById('nTxt') && document.getElementById('nTxt').focus()"); await pg.wait_for_timeout(250)
        r = await ev("(() => { const t = document.getElementById('nTxt'); return t ? getComputedStyle(t).borderTopColor : null; })()")
        await ev("document.activeElement && document.activeElement.blur()"); await pg.wait_for_timeout(250)
        r2 = await ev("(() => { const t = [...document.querySelectorAll('#trQ, input[type=date], select')].map(e => getComputedStyle(e).borderTopColor); const s = document.querySelector('select:not(.st)'); return s ? getComputedStyle(s).borderTopColor : null; })()")
        ok(r == 'rgb(53, 99, 176)' and r2 == 'rgb(128, 145, 170)', 'idée 5 : bordure des champs gris-bleu (3,2 pour 1), bleue quand on écrit', [r, r2])
        ok(await ev(CONTRASTE, ['rgb(128, 145, 170)', 'rgb(255, 255, 255)']) >= 3, 'bordure des champs ≥ 3 pour 1 sur blanc')
        # ───── protocoles : molécules en écriture normale, 13 px ─────
        await aller(pg, 'protocoles')
        r = await ev("[...document.querySelectorAll('.pc-mol')].slice(0, 12).map(e => [e.textContent, getComputedStyle(e).fontSize, getComputedStyle(e).textTransform])")
        ok(r and all(x[1] == '13px' and x[2] == 'none' for x in r), 'idée 12 : molécules des cartes en 13 px, sans majuscules forcées', r[:2])
        ok(r and not any(x[0] == x[0].upper() and len(x[0]) > 8 for x in r) and any(x[0][0].isupper() for x in r), 'idée 12 : molécules écrites « Cisplatine, … » (plus TOUT EN CAPITALES)', [x[0] for x in r[:4]])
        # ───── un seul groupe de choix ─────
        await aller(pg, 'agenda')
        r = await ev("(() => { const g = document.querySelector('.ag-vues:not(.defile)'), o = g.querySelector('button.on'); return [getComputedStyle(g).backgroundColor, getComputedStyle(o).backgroundColor, getComputedStyle(o).color, document.querySelector('.mcal .lbl') ? document.querySelector('.mcal .lbl').textContent : ''] })()")
        ok(r[0] == 'rgb(238, 243, 250)' and r[1] == 'rgb(53, 99, 176)' and r[2] == 'rgb(255, 255, 255)', 'idée 13 : Agenda, groupe bleu très clair, choix en cours bleu Onco360', r)
        ok(r[3] == 'Rendez-vous à venir', 'idée 12 : « Rendez-vous à venir » (plus « RDV À VENIR »)', r[3])
        await aller(pg, 'parametres/listes')
        r = await ev("(() => { const g = document.querySelector('.puces .choix'), o = g && g.querySelector('.puce.on'); return g ? [getComputedStyle(g).backgroundColor, getComputedStyle(o).backgroundColor, o.innerText.replace(/\\s+/g, ' ').trim(), !!o.querySelector('.nb'), /\\(\\d+\\)/.test(g.innerText)] : null })()")
        ok(r and r[0] == 'rgb(238, 243, 250)' and r[1] == 'rgb(53, 99, 176)', 'idée 13 : Paramètres › Listes, même groupe de choix', r)
        ok(r and r[3] and not r[4] and r[2].startswith('Mutuelles '), 'idée 14 : « Mutuelles 35 » en pastille (plus « (35) »)', r)
        for route, lib in (('parametres/horaires', 'Horaires'), ('parametres/rcp', 'Dates de RCP'), ('taches/rcp', 'RCP'), ('salle', 'Salle (période)')):
            await aller(pg, route)
            r = await ev("(() => { const g = document.querySelector('.choix, .sa-per'); if (!g) return null; const o = g.querySelector('.on'); return [getComputedStyle(g).backgroundColor, o ? getComputedStyle(o).backgroundColor : '-'] })()")
            ok(r and r[0] == 'rgb(238, 243, 250)' and r[1] in ('rgb(53, 99, 176)', '-'), f'idée 13 : {lib}, même groupe de choix', r)
        # compteur du référentiel RT : après le mot (plus en exposant)
        r = await ev("""(() => { const d = document.createElement('div'); d.className = 'ag-vues defile rtr-ong'; d.innerHTML = '<button class="on">Contraintes <span class="n rtr-pas">19</span></button><button>Essais <span class="n rtr-pas">2</span></button>';
          document.getElementById('page').appendChild(d); const n = d.querySelector('.rtr-pas'), s = getComputedStyle(n); const r = [s.position, Math.abs(n.getBoundingClientRect().top - d.querySelector('button').getBoundingClientRect().top) > 6]; d.remove(); return r; })()""")
        ok(r[0] == 'static' and r[1], 'idée 14 : compteurs de la fiche RT après le mot, sur la même ligne', r)
        ok(not pg.errs, 'aucune erreur JavaScript', pg.errs)
        await pg.close()
        # ───── toutes les pages touchées, quatre largeurs ─────
        PAGES = ['accueil', 'dossier/' + PID + '/chimio', 'salle', 'agenda', 'patients', 'taches', 'taches/rcp', 'protocoles', 'radiotherapie', 'bilan', 'parametres/listes', 'parametres/horaires', 'parametres/activites', 'parametres/impression', 'outils']
        for w in (390, 900, 1280, 1600):
            p = await ouvrir(b, S, w=w, h=900); deb = []
            for r in PAGES:
                await p.goto(U + r); await p.reload(); await p.wait_for_timeout(1700)
                if not await p.evaluate("document.documentElement.scrollWidth <= innerWidth + 1"): deb.append(r)
            ok(not deb, f'{w} px : {len(PAGES)} pages sans débordement', deb)
            ok(not p.errs, f'{w} px : aucune erreur JavaScript', p.errs)
            await p.close()
        await b.close()
    print(f'\n{ok_n} réussis, {ko_n} échoués')
asyncio.run(main())
