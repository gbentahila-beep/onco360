import pathlib; __file__=str(pathlib.Path(__file__).resolve()); exec(open(pathlib.Path(__file__).parent/'base.py').read())
# IG6 (03/11/2026, phase IG, idées 18 et 20) : « Fermer » à droite de la barre du dossier pour tous les rôles (médecin, secrétaire, infirmière,
# remplaçant), retour à la page d'où le dossier a été ouvert ; page de connexion : polices et champs d'Onco360, réussite en vert avec ✓, erreurs
# en rouge, « Afficher » dans le champ du mot de passe ; 390 et 1 440 px.
ok_n = ko_n = 0
def ok(c, m, d=None):
    global ok_n, ko_n
    if c: ok_n += 1; print('  ✔ ' + m)
    else: ko_n += 1; print('  ✘ ' + m + ('' if d is None else ' ' + str(d)[:500]))
U = f'http://localhost:{PORT}/'
PID = 'P20260928029'
S2 = json.loads(json.dumps(S)); TIT = S2[E + 'membres/UIDRITA']
for u, r in [('SEC', 'assistante'), ('INF', 'infirmiere')]:
    S2[E + 'membres/' + u] = {'role': r, 'nom': u, 'email': u.lower() + '@test.ma', 'actif': True, 'tousEtablissements': True, 'etablissements': [], 'droits': {}}
    S2['utilisateurs/' + u] = {'nom': u, 'prenom': 'Test'}
S2[E + 'membres/UREM'] = {'role': 'remplacant', 'nom': 'Dr Ali REMPLA', 'email': 'rem@test.ma', 'actif': True, 'remplace': 'UIDRITA', 'tousEtablissements': TIT.get('tousEtablissements', True),
    'etablissements': TIT.get('etablissements', []), 'droits': dict(TIT.get('droits', {})), 'remplaceDu': '', 'remplaceAu': '', 'remplaceDebMs': 0, 'remplaceFinMs': 0}
S2['utilisateurs/UREM'] = {'email': 'rem@test.ma', 'nom': 'REMPLA', 'prenom': 'Ali', 'titre': 'Dr'}
FERMER = """(() => { const b = document.querySelector('#barreDroite .br-fermer'); if (!b || !b.offsetParent) return null; const r = b.getBoundingClientRect(), d = document.querySelector('#dos > [data-zone=barre]').getBoundingClientRect();
  return [b.textContent.trim(), Math.round(d.right - r.right), Math.round(r.height), b.title] })()"""
async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        print('« Fermer » du dossier')
        for uid, role in (('', 'médecin'), ('SEC', 'secrétaire'), ('INF', 'infirmière'), ('UREM', 'remplaçant')):
            pg = await ouvrir(b, S2, w=1440); ev = pg.evaluate
            if uid: await pg.add_init_script(f"window.__uid='{uid}'")
            await pg.goto(U + 'v2.html#patients'); await pg.wait_for_timeout(2600)
            await ev(f"location.hash='dossier/{PID}'"); await pg.wait_for_timeout(1500)
            r = await ev(FERMER)
            ok(r and r[0] == 'Fermer' and r[1] <= 24 and r[2] >= 40 and 'Patients' in r[3], f'{role} : « Fermer » à droite de la barre du dossier ({r and r[3]})', r)
            await pg.click('#barreDroite .br-fermer'); await pg.wait_for_timeout(1000)
            ok(await ev("location.hash") == '#patients', f'{role} : « Fermer » ramène à la liste des patients', await ev("location.hash"))
            ok(not pg.errs, f'{role} : aucune erreur JavaScript', pg.errs[:2]); await pg.close()
        pg = await ouvrir(b, S2, w=1440); ev = pg.evaluate
        await pg.goto(U + 'v2.html#agenda'); await pg.wait_for_timeout(2600)
        await ev(f"location.hash='dossier/{PID}/chimio'"); await pg.wait_for_timeout(1500)
        ok('Agenda' in ((await ev(FERMER)) or ['', 0, 0, ''])[3], 'ouvert depuis l\'Agenda : « Fermer » annonce le retour à l\'Agenda')
        await ev(f"location.hash='dossier/{PID}/consultation'"); await pg.wait_for_timeout(1000)
        await pg.click('#barreDroite .br-fermer'); await pg.wait_for_timeout(1000)
        ok(await ev("location.hash") == '#agenda', 'changer d\'onglet dans le dossier ne change pas la page de retour : Agenda', await ev("location.hash"))
        ok(not pg.errs, 'aucune erreur JavaScript', pg.errs[:2]); await pg.close()
        pg = await ouvrir(b, S2, w=1440); ev = pg.evaluate
        await pg.goto(U + 'v2.html#dossier/' + PID); await pg.wait_for_timeout(2600)
        await pg.click('#barreDroite .br-fermer'); await pg.wait_for_timeout(1000)
        ok(await ev("location.hash") == '#patients', 'dossier ouvert directement par son adresse : « Fermer » → Patients', await ev("location.hash"))
        ok(not pg.errs, 'aucune erreur JavaScript', pg.errs[:2]); await pg.close()
        pg = await ouvrir(b, S2, w=390, h=844); ev = pg.evaluate
        await pg.goto(U + 'v2.html#dossier/' + PID); await pg.wait_for_timeout(2600)
        r = await ev("[!!(document.querySelector('.br-fermer') || {}).offsetParent, getComputedStyle(document.querySelector('#dos > [data-zone=barre]')).backgroundColor, document.documentElement.scrollWidth <= innerWidth + 1]")
        ok(not r[0] and r[1] in ('rgba(0, 0, 0, 0)', 'transparent') and r[2], '390 px : barre du téléphone inchangée (« + Prescrire » seul, sans fond), rien ne déborde', r)
        ok(not pg.errs, '390 px : aucune erreur JavaScript', pg.errs[:2]); await pg.close()

        print('Page de connexion')
        for w in (1440, 390):
            pg = await ouvrir(b, S2, w=w, h=900 if w > 500 else 844); ev = pg.evaluate
            await pg.add_init_script("window.__deconnecte = true")
            await pg.goto(U + 'index.html'); await pg.wait_for_timeout(900)
            await pg.wait_for_function("document.fonts.status === 'loaded'")
            r = await ev("""[getComputedStyle(document.querySelector('h2')).fontFamily, getComputedStyle(document.body).fontFamily, document.fonts.check('700 20px Montserrat'), document.fonts.check('16px Roboto'),
              ...['email', 'mdp', 'btnConnexion'].map(i => Math.round(document.getElementById(i).getBoundingClientRect().height)), document.documentElement.scrollWidth <= innerWidth + 1]""")
            ok(r[0].startswith('Montserrat') and r[1].startswith('Roboto') and r[2] and r[3], f'{w} px : titre en Montserrat, texte en Roboto (polices du site)', r[:4])
            ok(all(h >= 44 for h in r[4:7]) and r[7], f'{w} px : champs et bouton de 44 px au moins, rien ne déborde', r[4:])
            r = await ev("(() => { const v = document.getElementById('voirMdp'), m = document.getElementById('mdp').getBoundingClientRect(), b = v.getBoundingClientRect(); return [v.textContent, b.right <= m.right && b.left >= m.left && b.top >= m.top && b.bottom <= m.bottom, document.getElementById('mdp').type] })()")
            ok(r == ['Afficher', True, 'password'], f'{w} px : « Afficher » dans le champ du mot de passe', r)
            await pg.fill('#mdp', 'secret'); await pg.click('#voirMdp')
            r = await ev("[document.getElementById('mdp').type, document.getElementById('voirMdp').textContent, document.getElementById('voirMdp').getAttribute('aria-pressed'), document.activeElement.id]")
            ok(r == ['text', 'Masquer', 'true', 'mdp'], 'un clic montre le mot de passe (« Masquer »), le curseur reste dans le champ', r)
            await pg.click('#voirMdp'); ok(await ev("document.getElementById('mdp').type") == 'password', 'un 2e clic le cache de nouveau')
            await pg.fill('#mdp', ''); await pg.click('#btnConnexion'); await pg.wait_for_timeout(200)
            r = await ev("(() => { const m = document.getElementById('erreur'), s = getComputedStyle(m); return [m.className, m.textContent, s.color, getComputedStyle(m, '::before').content] })()")
            ok(r[0] == 'msg err' and 'Saisissez' in r[1] and r[2] == 'rgb(184, 0, 61)' and r[3] in ('none', 'normal'), f'{w} px : erreur en rouge, sans ✓', r)
            await pg.fill('#email', 'medecin@test.ma'); await pg.fill('#mdp', 'secret'); await pg.click('#btnConnexion'); await pg.wait_for_timeout(400)
            r = await ev("(() => { const m = document.getElementById('erreur'), s = getComputedStyle(m); return [m.className, m.textContent, s.color, getComputedStyle(m, '::before').content, m.getAttribute('role')] })()")
            ok(r[0] == 'msg ok' and r[1].startswith('Connexion réussie') and r[2] == 'rgb(0, 128, 106)' and '✓' in r[3] and r[4] == 'status', f'{w} px : connexion réussie en vert avec ✓', r)
            await pg.click('#lienOubli'); await pg.wait_for_timeout(300)
            ok(await ev("document.getElementById('erreur').className") == 'msg ok', 'mot de passe oublié : e-mail envoyé = message vert')
            r = await ev("[!!document.getElementById('partage'), !!document.querySelector('#lienCgu[href=\"cgu.html\"]'), !!document.querySelector('header img')]")
            ok(r == [True, True, True], 'logo, « Poste partagé » et lien des CGU gardés', r)
            ok(not pg.errs, 'aucune erreur JavaScript', pg.errs[:2])
            await pg.close()
        csp = json.load(open(ICI.parent / 'firebase.json'))
        v = [h['value'] for x in csp['hosting']['headers'] for h in x.get('headers', []) if h['key'] == 'Content-Security-Policy']
        ok(v and "font-src 'self'" in v[0] and "style-src 'self' 'unsafe-inline'" in v[0], 'Content-Security-Policy : polices du site et style de la page permis', v[:1])
        await b.close()
    print(f'\n{ok_n} réussis, {ko_n} échoués')
asyncio.run(main())
