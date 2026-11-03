import pathlib; __file__=str(pathlib.Path(__file__).resolve()); exec(open(pathlib.Path(__file__).parent/'base.py').read())
# IG4 (02/11/2026, phase IG, idées 6, 7 et 8) : page dessinée dès l'ouverture avec le bon titre, menu après les droits ; tableau de bord sans défilement
# dans une carte (5 lignes, puis « Voir les N … › », choix A) ; protocole ouvert en lecture (Modifier, Dupliquer ; Signaler, Supprimer dans ⋯).
import copy
ok_n = ko_n = 0
def ok(c, m, d=None):
    global ok_n, ko_n
    if c: ok_n += 1; print('  ✔ ' + m)
    else: ko_n += 1; print('  ✘ ' + m + ('' if d is None else ' ' + str(d)[:500]))
U = f'http://localhost:{PORT}/v2.html#'
PID = 'P20260928029'
async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        # ───── idée 6 : chargement lent (bibliothèques Firebase retardées de 2 s) ─────
        for route, titre in (('dossier/' + PID + '/chimio', 'Dossier patient'), ('agenda', 'Agenda / Rendez-vous'), ('accueil', 'Tableau de bord')):
            pg = await ouvrir(b, S, w=1440)
            async def lent(r):
                await asyncio.sleep(2.0); await r.fulfill(body=M[r.request.url.split('/')[-1]], content_type='application/javascript')
            await pg.route('https://www.gstatic.com/**', lent)
            await pg.goto(U + route, wait_until='commit')
            try: await pg.wait_for_selector('#page .sq-page', timeout=1500)
            except Exception: pass
            r = await pg.evaluate("[!!document.querySelector('#page .chargement.sq-page .sq'), document.getElementById('titrePage').textContent, getComputedStyle(document.querySelector('nav a')).visibility, document.body.classList.contains('demarrage')]")
            ok(r[0] and r[1] == titre and r[2] == 'hidden' and r[3], f'idée 6 : #{route.split("/")[0]} : forme de la page en gris et titre « {titre} » dès l\'ouverture, menu caché', r)
            await pg.wait_for_timeout(4500)
            r = await pg.evaluate("[!!document.querySelector('#page .chargement'), getComputedStyle(document.querySelector('nav a[data-p=patients]')).visibility, document.body.classList.contains('demarrage'), (document.querySelector('nav a[data-p=documents]') || {}).offsetParent === null]")
            ok(not r[0] and r[1] == 'visible' and not r[2], f'idée 6 : #{route.split("/")[0]} : page remplie, menu affiché une fois les droits lus', r)
            if route == 'accueil': ok(r[3], 'idée 6 : « Documents » jamais montré au médecin (menu affiché après les droits)', r)
            ok(not pg.errs, 'aucune erreur JavaScript', pg.errs); await pg.close()
        # ───── idée 7 : tableau de bord, un seul défilement ─────
        for w in (1440, 1280, 900, 390):
            pg = await ouvrir(b, S, w=w, h=900 if w > 500 else 844); ev = pg.evaluate
            await pg.goto(U + 'accueil'); await pg.wait_for_timeout(2600)
            r = await ev("""[...document.querySelectorAll('.tb-fx > section, .tb-fx .af-g, .sept-l')].filter(e => e.scrollHeight > e.clientHeight + 2).map(e => e.className)""")
            ok(not r, f'idée 7 : {w} px : « À valider » et « Les 7 prochains jours » sans défilement dans la carte, contenu jamais plus haut que la carte', r)
            g = await ev("""[...document.querySelectorAll('.af-g')].map(g => { const L = [...g.querySelectorAll('.af-l')]; const v = g.querySelector('.tb-voir');
              return [g.querySelector('.af-t span').textContent, L.length, L.filter(l => l.offsetParent !== null).length, v ? v.textContent : ''] })""")
            gros = [x for x in g if x[1] > 5]
            ok(gros and all(x[2] == 5 and x[3] == f'Voir les {x[1]} ' + x[0][0].lower() + x[0][1:] + ' ›' for x in gros), f'idée 7 : {w} px : 5 lignes entières, puis « Voir les N … › »', g)
            ok(all(x[2] == x[1] and not x[3] for x in g if x[1] <= 5), f'idée 7 : {w} px : une liste courte reste entière, sans lien', g)
            if w == 1440:
                await pg.click('.af-g .tb-voir'); await pg.wait_for_timeout(300)
                r = await ev("(() => { const g = document.querySelector('.af-g.ouv'); return g ? [g.querySelectorAll('.af-l').length, [...g.querySelectorAll('.af-l')].filter(l => l.offsetParent !== null).length, g.querySelector('.tb-voir').textContent] : null })()")
                ok(r and r[0] == r[1] and r[2] == 'Voir moins', 'idée 7 : « Voir les N » déplie la liste dans la carte ; « Voir moins » la replie', r)
                await pg.click('.af-g.ouv .tb-voir'); await pg.wait_for_timeout(300)
                ok(await ev("!document.querySelector('.af-g.ouv') && document.querySelector('.af-g .tb-voir').textContent.startsWith('Voir les ')"), 'idée 7 : repliée de nouveau, le lien reprend son texte')
                s = await ev("(() => { const l = document.querySelector('.sept-l'); if (!l) return null; const E = [...l.querySelectorAll('.ev')]; const v = document.querySelector('.sept .tb-voir'); return [E.length, E.filter(e => e.offsetParent !== null).length, v ? v.textContent : ''] })()")
                ok(s is None or (s[0] <= 5 and not s[2]) or (s[1] == 5 and s[2].startswith(f'Voir les {s[0]} ')), 'idée 7 : « Les 7 prochains jours » : 5 lignes, puis « Voir les N … › »', s)
                ok(await ev("[...document.querySelectorAll('.af-l.ret')].some(l => getComputedStyle(l).color !== '' )"), 'idée 7 : le rouge des cures en retard est gardé')
            ok(await ev("document.documentElement.scrollWidth <= innerWidth + 1"), f'{w} px : tableau de bord sans débordement')
            ok(not pg.errs, f'{w} px : aucune erreur JavaScript', pg.errs); await pg.close()
        # ───── idée 8 : protocole ouvert en lecture ─────
        pg = await ouvrir(b, S, w=1440); ev = pg.evaluate
        await pg.goto(U + 'protocoles'); await pg.wait_for_timeout(2300)
        nom = await ev("document.querySelector('#prL .pcarte b').textContent")
        await pg.click('#prL .pcarte >> nth=0'); await pg.wait_for_timeout(800)
        r = await ev("""(() => { const z = document.getElementById('fenetreCorps'); const champs = [...z.querySelectorAll('input, select, textarea')].filter(e => e.getBoundingClientRect().width).length;
          const bt = [...z.querySelectorAll('.pr-haut > button')].map(b => b.innerText.trim()); const menu = [...z.querySelectorAll('.pr-haut .mpts .cache button, .pr-haut .mpts button.mini')].map(b => b.textContent.trim());
          const cadres = [...z.querySelectorAll('details.pr-cad summary')].map(s => s.textContent.trim());
          return [champs, bt, menu, cadres, z.innerText.includes('Contenus indicatifs'), document.activeElement && document.activeElement.tagName]; })()""")
        ok(r[0] == 0, 'idée 8 : le protocole s\'ouvre en lecture (aucune case à remplir, curseur nulle part)', r)
        ok(r[1] == ['Modifier', 'Dupliquer'], 'idée 8 : « Modifier » et « Dupliquer » en haut', r[1])
        ok('Signaler une erreur' in r[2] and 'Supprimer le protocole' in r[2], 'idée 8 : « Signaler une erreur » et « Supprimer » dans ⋯', r[2])
        ok(r[3][:3] == ['Protocole', 'Indication', 'Molécules'] and 'Prescription' in r[3] and r[4], 'idée 8 : rubriques Protocole, Indication, Molécules, Prescription ; avertissement', r[3])
        t = await ev("document.getElementById('fenetreCorps').innerText")
        ok('Cycle' in t and 'Nombre de cures proposé' in t and 'Risque émétique' in t, 'idée 8 : valeurs en clair (cycle, nombre de cures, risque émétique)', t[:300])
        await pg.click('#fenetreCorps .pr-haut button:has-text("Modifier")'); await pg.wait_for_timeout(700)
        r = await ev("[[...document.querySelectorAll('#fenetreCorps input')].filter(e => e.getBoundingClientRect().width).length, (document.querySelector('#fenetreCorps input') || {}).value, !!document.getElementById('fOk'), !!document.getElementById('prDup'), document.getElementById('fenetreCorps').innerText.includes('Supprimer le protocole')]")
        ok(r[0] > 3 and r[1] == nom and r[2] and r[3] and r[4], 'idée 8 : « Modifier » ouvre le formulaire d\'avant, inchangé', r)
        await ev("fermerFenetre()"); await pg.wait_for_timeout(300)
        n0 = await ev("Object.keys(window.__fs).filter(k => k.includes('/protocoles/')).map(k => JSON.parse(window.__fs[k].data || '[]').length).reduce((a, b) => a + b, 0)")
        await pg.click('#prL .pcarte >> nth=0'); await pg.wait_for_timeout(700)
        await pg.click('#fenetreCorps .pr-haut button:has-text("Dupliquer")'); await pg.wait_for_timeout(1800)
        r = await ev("[(document.querySelector('#fenetreCorps input') || {}).value, Object.keys(window.__fs).filter(k => k.includes('/protocoles/')).map(k => JSON.parse(window.__fs[k].data || '[]').length).reduce((a, b) => a + b, 0)]")
        ok(r[0] == nom + ' (copie)' and r[1] == n0 + 1, 'idée 8 : « Dupliquer » : la copie est faite et s\'ouvre en modification (comme avant)', [r, n0])
        await ev("fermerFenetre()"); await pg.wait_for_timeout(300)
        await ev("prOuvrir()"); await pg.wait_for_timeout(500)
        ok(await ev("(document.getElementById('fenetreCorps').innerText.includes('Nouveau protocole')) && !!document.getElementById('fOk')"), 'idée 8 : « Créer un protocole » ouvre le formulaire vide')
        ok(not pg.errs, 'aucune erreur JavaScript', pg.errs); await pg.close()
        # secrétaire (sans droit « paramètres ») : lecture, « Signaler une erreur » seulement
        S3 = copy.deepcopy(S); S3[E + 'membres/UIDSEC'] = {'role': 'assistante', 'nom': 'Secrétaire Test', 'actif': True, 'tousEtablissements': True, 'droits': {}}
        for w in (1440, 390):
            pg = await ouvrir(b, S3, w=w, h=900 if w > 500 else 844); await pg.add_init_script("window.__uid='UIDSEC'"); ev = pg.evaluate
            await pg.goto(U + 'protocoles'); await pg.reload(); await pg.wait_for_timeout(2300)
            await pg.click('#prL .pcarte >> nth=0'); await pg.wait_for_timeout(700)
            r = await ev("[[...document.querySelectorAll('#fenetreCorps .pr-haut > button')].map(b => b.innerText.trim()), [...document.querySelectorAll('#fenetreCorps .pr-haut .mpts button.mini')].map(b => b.textContent.trim()).filter(t => t !== '⋯'), document.documentElement.scrollWidth <= innerWidth + 1]")
            ok(r[0] == [] and r[1] == ['Signaler une erreur'] and r[2], f'idée 8 : {w} px : sans droit de modifier : lecture, « Signaler une erreur » seulement, sans débordement', r)
            ok(not pg.errs, f'{w} px : aucune erreur JavaScript', pg.errs); await pg.close()
        await b.close()
    print(f'\n{ok_n} réussis, {ko_n} échoués')
asyncio.run(main())
