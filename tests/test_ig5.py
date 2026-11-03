import pathlib; __file__=str(pathlib.Path(__file__).resolve()); exec(open(pathlib.Path(__file__).parent/'base.py').read())
# IG5 (03/11/2026, phase IG) : recherche souple (synonymes, tirets, espaces) dans Protocoles, Nouvelle ligne et Médic., « Cherché aussi : … » ;
# Paramètres : « mot de passe » trouve Mon compte ; tri au clic sur le titre d'une colonne (Patients, Tâches, RCP, journal du Bilan), gardé par
# personne ; « Payé » du Bilan en vraie case à cocher ; Listes en lecture, ✎ pour modifier une ligne. Ordinateur et 390 px.
ok_n = ko_n = 0
def ok(c, m, d=None):
    global ok_n, ko_n
    if c: ok_n += 1; print('  ✔ ' + m)
    else: ko_n += 1; print('  ✘ ' + m + ('' if d is None else ' ' + str(d)[:500]))
U = f'http://localhost:{PORT}/v2.html#'
PID = 'P20260928029'
import copy, functools
S2 = copy.deepcopy(S); ETAB = S2[E + 'patients/' + PID]['etablissementId']
for i, (t, ech) in enumerate((('Bilan à demander', '2026-10-09'), ('Appeler le correspondant', '2026-10-07'), ('Courrier de sortie', '2026-10-12'))):
    S2[E + 'taches/T%d' % i] = {'titre': t, 'desc': '', 'type': 'Autre', 'ech': ech, 'patientId': PID, 'patientNom': 'PATIENT TEST', 'etablissementId': ETAB, 'pour': 'UIDRITA', 'pourNom': 'Dr Test',
        'de': 'UIDRITA', 'deNom': 'Dr Test', 'qui': ['UIDRITA'], 'statut': 'afaire', 'fil': [], 'o': i}
    S2[E + 'rcp/R%d' % i] = {'patientId': PID, 'patientNom': 'PATIENT TEST', 'etablissementId': ETAB, 'd': '2026-10-08', 'q': 'Question %d ?' % i, 'ins': '2026-10-0%d' % (i + 1), 'fait': False, 'o': i, 'creePar': 'UIDRITA', 'creeParNom': 'Dr Test'}
def nat(a, b):
    import re
    k = lambda s: [int(x) if x.isdigit() else x for x in re.split(r'(\d+)', s.lower())]
    return (k(a) > k(b)) - (k(a) < k(b))
croissant = lambda L: all(nat(L[i], L[i + 1]) <= 0 for i in range(len(L) - 1))
NOMS = "[...document.querySelectorAll('#lst .pt-r .c-n b')].map(b => b.textContent)"
async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        print('Recherche souple')
        pg = await ouvrir(b, S, w=1440); ev = pg.evaluate
        await pg.goto(U + 'protocoles'); await pg.wait_for_timeout(2300)
        async def cherche(q):
            await pg.fill('#prQ', q); await pg.wait_for_timeout(300)
            return await ev("[document.querySelectorAll('#prL .pcarte').length, (document.querySelector('#prL .ch-aussi') || {}).textContent || '', (document.querySelector('#prL') || {}).textContent]")
        t = await cherche('taxol')
        ok(t[0] > 0 and t[1] == 'Cherché aussi : Paclitaxel', 'Protocoles : « taxol » trouve le paclitaxel, « Cherché aussi : Paclitaxel » à côté du nombre', t)
        p = await cherche('paclitaxel')
        ok(p[0] == t[0] and not p[1], 'Protocoles : « paclitaxel » donne les mêmes protocoles, sans « Cherché aussi »', [p, t])
        r = [await cherche(q) for q in ('5-FU', '5FU', '5 fu')]
        ok(r[0][0] > 0 and r[0][0] == r[1][0] == r[2][0], 'Protocoles : « 5-FU », « 5FU » et « 5 fu » donnent le même nombre', [x[0] for x in r])
        z = await cherche('zzzqqq')
        ok(z[0] == 0, 'Protocoles : rien pour un mot inconnu', z)
        await pg.goto(U + 'dossier/' + PID); await pg.wait_for_timeout(2500)
        await ev(f"ordMedicaments('{PID}')"); await pg.wait_for_timeout(1200)
        await pg.fill('#mdQ', 'zophren'); await pg.wait_for_timeout(400)
        m = await ev("[[...document.querySelectorAll('#mdListe .md-t tr')].map(t => t.textContent).join(' | '), (document.querySelector('#mdListe .ch-aussi') || {}).textContent || '']")
        ok('ondansétron' in m[0].lower() and m[1] == 'Cherché aussi : Ondansétron', 'Médic. : « zophren » trouve l\'ondansétron, « Cherché aussi : Ondansétron »', m)
        await pg.fill('#mdQ', 'ondansetron'); await pg.wait_for_timeout(400)
        ok(await ev("document.querySelector('#mdListe').textContent.toLowerCase().includes('ondansétron') && !document.querySelector('#mdListe .ch-aussi')"), 'Médic. : « ondansetron » sans accent trouve aussi, sans « Cherché aussi »')
        ok(not pg.errs, 'aucune erreur JavaScript', pg.errs[:2]); await pg.close()

        print('Paramètres : « mot de passe »')
        pg = await ouvrir(b, S, w=1440); ev = pg.evaluate
        await pg.goto(U + 'parametres'); await pg.wait_for_timeout(2300)
        await pg.fill('#cfQ', 'mot de passe'); await pg.wait_for_timeout(400)
        r = await ev("[...document.querySelectorAll('#cfQr .cf-qi')].map(b => b.textContent)")
        ok(any('Informations' in x and 'Mon compte' in x for x in r), 'Paramètres : « mot de passe » propose « Informations · Mon compte »', r)
        await ev("[...document.querySelectorAll('#cfQr .cf-qi')].find(b => b.textContent.includes('Mon compte')).click()"); await pg.wait_for_timeout(1200)
        ok(await ev("location.hash") == '#profil/infos', 'un clic ouvre Mon compte › Informations', await ev("location.hash"))
        ok(not pg.errs, 'aucune erreur JavaScript', pg.errs[:2]); await pg.close()

        print('Tri des colonnes')
        pg = await ouvrir(b, S2, w=1440); ev = pg.evaluate
        await pg.goto(U + 'patients'); await pg.wait_for_timeout(2500)
        n0 = await ev(NOMS)
        await pg.click('#lst .pt-h .th-tri >> nth=0'); await pg.wait_for_timeout(400)
        n1 = await ev(NOMS)
        ok(len(n1) == len(n0) > 3 and sorted(n1) == sorted(n0) and croissant(n1), 'Patients : 1er clic sur « Nom Prénom » = ordre alphabétique', n1[:6])
        a = await ev("[...document.querySelectorAll('#lst .pt-h [role=columnheader]')].map(e => e.getAttribute('aria-sort'))")
        ok(a[0] == 'ascending' and all(x == 'none' for x in a[1:]), 'Patients : aria-sort ascendant sur la colonne triée, flèche ▲', a)
        await pg.click('#lst .pt-h .th-tri >> nth=0'); await pg.wait_for_timeout(400)
        n2 = await ev(NOMS)
        ok(croissant(list(reversed(n2))) and sorted(n2) == sorted(n0), 'Patients : 2e clic = ordre inverse ▼', n2[:6])
        fs = await ev("(window.__fs['utilisateurs/UIDRITA'] || {}).tris")
        ok(fs and fs.get('patients') == {'k': 'nom', 's': -1}, 'tri gardé dans utilisateurs/{uid}.tris', fs)
        await pg.goto(U + 'accueil'); await pg.wait_for_timeout(1200); await pg.goto(U + 'patients'); await pg.wait_for_timeout(1500)
        ok(await ev(NOMS) == n2 and await ev("document.querySelector('#lst .pt-h .th-tri.on .th-f').textContent") == '▼', 'retour sur Patients : tri retrouvé')
        await pg.click('#lst .pt-h .th-tri >> nth=0'); await pg.wait_for_timeout(400)
        ok(await ev(NOMS) == n0 and not await ev("!!document.querySelector('#lst .pt-h .th-tri.on')"), 'Patients : 3e clic = ordre par défaut', (await ev(NOMS))[:6])
        await pg.click('#lst .pt-h .th-tri >> nth=1'); await pg.wait_for_timeout(400)
        ok(await ev("document.querySelector('#lst .pt-h [aria-sort=ascending] .th-tri').textContent.startsWith('Date de naissance')"), 'Patients : tri par date de naissance')
        for page, sel in (('taches', '#page .th-tri'), ('rcp', '#page .th-tri'), ('bilan', '#page .th-tri')):
            await pg.goto(U + page); await pg.wait_for_timeout(2300)
            n = await ev(f"document.querySelectorAll('{sel}').length")
            if not n: ok(False, f'{page} : titres de colonnes triables'); continue
            await ev(f"document.querySelector('{sel}').click()"); await pg.wait_for_timeout(500)
            r = await ev(f"[document.querySelectorAll('{sel}').length, (document.querySelector('#page [aria-sort=ascending] .th-tri, #page th[aria-sort=ascending] .th-tri') || {{}}).textContent || '']")
            ok(r[0] == n and r[1], f'{page} : {n} colonnes triables, un clic trie (▲)', r)
        fs = await ev("(window.__fs['utilisateurs/UIDRITA'] || {}).tris")
        ok(fs and all(k in fs for k in ('patients', 'taches', 'rcp', 'bilan')), 'chaque page garde son tri', fs)
        r = await ev("[document.querySelectorAll('#page .bi-pc input[type=checkbox]').length, document.querySelectorAll('[onclick^=biPaye]').length]")
        ok(r[0] > 0 and r[0] == r[1], 'Bilan : « Payé » est une vraie case à cocher', r)
        ok(not pg.errs, 'aucune erreur JavaScript', pg.errs[:2]); await pg.close()

        print('Listes : lecture, ✎ pour modifier')
        pg = await ouvrir(b, S, w=1440); ev = pg.evaluate
        await pg.goto(U + 'parametres/listes'); await pg.wait_for_timeout(2300)
        await ev("cfLs('mut')"); await pg.wait_for_timeout(500)
        r = await ev("[document.querySelectorAll('#cfLl .it').length, document.querySelectorAll('#cfLl .it .it-n').length, document.querySelectorAll('#cfLl .it.ed').length]")
        ok(r[0] > 0 and r[1] == r[0] and r[2] == 0, 'Mutuelles : chaque ligne en lecture, sans champ ouvert', r)
        nom = await ev("document.querySelector('#cfLl .it .it-n').textContent")
        await pg.click('#cfLl .it-ed >> nth=0'); await pg.wait_for_timeout(300)
        r = await ev("[document.querySelectorAll('#cfLl .it.ed').length, document.activeElement && document.activeElement.closest('.it.ed') ? document.activeElement.value : null]")
        ok(r[0] == 1 and r[1] == nom, '✎ : la ligne devient un champ, curseur dedans', r)
        await pg.keyboard.press('Enter'); await pg.wait_for_timeout(300)
        ok(await ev("document.querySelectorAll('#cfLl .it.ed').length") == 0, 'en quittant le champ, la ligne revient en lecture')
        ok(not pg.errs, 'aucune erreur JavaScript', pg.errs[:2]); await pg.close()

        print('Téléphone (390 px)')
        for page in ('patients', 'taches', 'rcp', 'bilan', 'parametres/listes'):
            pg = await ouvrir(b, S, w=390, h=844); ev = pg.evaluate
            await pg.goto(U + page); await pg.wait_for_timeout(2300)
            ok(await ev("document.documentElement.scrollWidth <= innerWidth + 1"), f'390 px : {page} sans débordement', await ev("document.documentElement.scrollWidth"))
            ok(not pg.errs, f'390 px : {page} : aucune erreur JavaScript', pg.errs[:2]); await pg.close()
        await b.close()
    print(f'\n{ok_n} réussis, {ko_n} échoués')
asyncio.run(main())
