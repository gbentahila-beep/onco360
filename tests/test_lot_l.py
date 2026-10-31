import pathlib; __file__=str(pathlib.Path(__file__).resolve()); exec(open(pathlib.Path(__file__).parent/'base.py').read())
# Lot L (31/10/2026) : CGU acceptées (L0), « Poste partagé » et lien des CGU à la connexion (L7), journal des erreurs (L1), import des patients par
# fichier Excel (L2), contrôle des dossiers (L5), cabinet suspendu en lecture seule et avis de l'Administration (L6), invitation (L6 e),
# Administration › État de la plateforme (L1, L9), politique de sécurité du site appliquée sans violation (L7). Jeu fictif ; 1 440 et 390 px.
import copy, re, tempfile
ok_n = ko_n = 0
def ok(c, m, d=None):
    global ok_n, ko_n
    if c: ok_n += 1; print('  ✔ ' + m)
    else: ko_n += 1; print('  ✘ ' + m + ('' if d is None else ' ' + str(d)[:400]))
U = f'http://localhost:{PORT}/'
DEB = "document.documentElement.scrollWidth > innerWidth + 1"
FB = json.load(open(ICI.parent / 'firebase.json'))
ENTETES = {h['key']: h['value'] for r in FB['hosting']['headers'] if r['source'] == '**' for h in r['headers']}
CSP = ENTETES.get('Content-Security-Policy') or ENTETES.get('Content-Security-Policy-Report-Only')
async def avec_csp(pg):
    # en-têtes du site (firebase.json) ajoutés aux pages servies en local ; violations notées dans window.__csp
    async def f(route):
        r = await route.fetch(); h = dict(r.headers); h['content-security-policy'] = CSP; h['permissions-policy'] = ENTETES.get('Permissions-Policy', '')
        await route.fulfill(response=r, headers=h)
    await pg.route(re.compile(r'http://localhost:\d+/[a-z0-9-]*\.html.*'), f)
    await pg.add_init_script("window.__csp=[];document.addEventListener('securitypolicyviolation',e=>window.__csp.push(e.violatedDirective+' '+e.blockedURI));")
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        print('L0 : conditions générales')
        pg = await ouvrir(b, S); await pg.add_init_script('window.__cguVierge=true'); ev = pg.evaluate
        await pg.goto(U + 'v2.html#accueil'); await pg.wait_for_timeout(2500)
        ok(await ev("!!document.getElementById('cguFond')"), 'fenêtre des CGU à la première connexion')
        ok(await ev("!document.getElementById('cguCase').checked && document.getElementById('cguOk').disabled"), 'case non cochée, « Continuer » désactivé')
        ok(await ev("document.getElementById('cguLien').getAttribute('href') === 'cgu.html' && document.getElementById('cguLien').target === '_blank'"), 'lien vers le texte (nouvel onglet)')
        r = await ev("(() => { const b = document.getElementById('cguOk').getBoundingClientRect(), c = document.querySelector('.cgu-case').getBoundingClientRect(); return [b.height, c.height, parseFloat(getComputedStyle(document.querySelector('.cgu-boite p')).fontSize)]; })()")
        ok(r[0] >= 44 and r[1] >= 44 and r[2] >= 13, 'boutons et case ≥ 44 px, texte ≥ 13 px', r)
        await pg.click('#cguCase'); ok(await ev("!document.getElementById('cguOk').disabled"), 'case cochée : « Continuer » actif')
        await pg.click('#cguOk'); await pg.wait_for_timeout(600)
        c = await ev("window.__fs['utilisateurs/UIDRITA'].cgu")
        ok(c and c.get('version') == CGU_V and c.get('espace') == 'cabinet-bentahila' and c.get('email') == 'ritabentahila@gmail.com' and 'le' in c, 'acceptation enregistrée (version, date du serveur, e-mail, cabinet)', c)
        ok(await ev("!document.getElementById('cguFond') && (() => { const h = window.__fs['utilisateurs/UIDRITA'].cguHist || []; return (h.__au || h).length === 1 && (h.__au || h)[0].version === '" + CGU_V + "'; })()"), 'fenêtre fermée, historique noté')
        await ev("location.hash = '#profil'"); await pg.wait_for_timeout(1500)
        ok(await ev("!!document.querySelector('#pfCgu a[href=\"cgu.html\"]') && /acceptées \\(version/.test(document.getElementById('pfCgu').innerText)"), 'Mon compte : CGU acceptées et lien du texte')
        await pg.close()
        for v, m in [(CGU_V, False), ('0.9', True)]:
            s = copy.deepcopy(S); s['utilisateurs/UIDRITA'] = dict(s.get('utilisateurs/UIDRITA', {}), cgu={'version': v})
            pg = await ouvrir(b, s); await pg.add_init_script('window.__cguVierge=true'); ev = pg.evaluate
            await pg.goto(U + 'v2.html#accueil'); await pg.wait_for_timeout(2500)
            r = await ev("[!!document.getElementById('cguFond'), /ont changé/.test((document.getElementById('cguFond') || {}).innerText || '')]")
            ok(r == [m, m], 'nouvelle version : de nouveau présentée' if m else 'version acceptée : pas redemandée', r)
            await pg.close()
        pg = await ouvrir(b, S); ev = pg.evaluate
        await pg.goto(U + 'cgu.html'); await pg.wait_for_timeout(600)
        t = await ev("document.body.innerText")
        ok('Conditions générales d\'utilisation' in t and 'Version 1.0 du 31 octobre 2026' in t, 'page des CGU : titre et version', t[:120])
        ok(all(x in t for x in ['09-08', 'CNDP', '446', '131-13', '232', '268', '2-00', 'tribunal de commerce de Casablanca', 'Union européenne', 'Poste partagé']), 'page des CGU : textes de loi, hébergement, juridiction')
        ok(not re.search(r'\[[^\]]*\]|…\s*$|XXX|à compléter|TODO', t), 'page des CGU : aucun trou ni texte à compléter')
        ok('Rita' not in t and 'Bentahila' not in t, "page des CGU : l'éditeur n'est pas nommé")
        await pg.set_viewport_size({'width': 390, 'height': 800}); await pg.wait_for_timeout(200)
        ok(not await ev(DEB), 'page des CGU sans débordement à 390 px')
        await pg.close()

        print('L7 : connexion')
        pg = await ouvrir(b, S); ev = pg.evaluate
        await pg.add_init_script("window.__deconnecte = true")
        await pg.goto(U + 'index.html'); await pg.wait_for_timeout(800)
        r = await ev("[!!document.getElementById('partage'), document.getElementById('partage') && document.getElementById('partage').checked, !!document.querySelector('#lienCgu[href=\"cgu.html\"]')]")
        ok(r == [True, False, True], 'case « Poste partagé » (non cochée) et lien des CGU', r)
        await pg.close()

        print('L2 : import des patients')
        pg = await ouvrir(b, S); ev = pg.evaluate
        await pg.goto(U + 'v2.html#parametres/export'); await pg.wait_for_timeout(2500)
        ok(await ev("!!document.getElementById('ipCarte')"), 'Paramètres › Export des données : « Importer des patients »')
        async with pg.expect_download() as dl: await pg.click('#ipModele')
        ok((await dl.value).suggested_filename == 'Onco360_modele_import_patients.xlsx', 'modèle Excel téléchargé')
        n0 = await ev("Object.keys(window.__fs).filter(k => /^espaces\\/cabinet-bentahila\\/patients\\//.test(k)).length")
        f = tempfile.NamedTemporaryFile('w', suffix='.csv', delete=False, encoding='utf-8')
        f.write('Nom,Prénom,Date de naissance (JJ/MM/AAAA),Sexe (F ou H),Téléphone,Mutuelle,N° de dossier d\'origine\n'
                'FICTIF-IMPORT,Amina,12/03/1971,F,600001111,CNOPS,ANC-001\n'
                'FICTIF-IMPORT,amina,12/03/1971,F,,CNOPS,ANC-002\n'
                ',Sans nom,01/01/1980,H,,,\n'
                'FICTIF-DEUX,Karim,31/02/1960,H,,,\n'
                'FICTIF-TROIS,Youssef,05/05/1955,H,0661000000,CNSS,ANC-003\n'); f.close()
        await pg.set_input_files('#ipFichier', f.name); await pg.wait_for_timeout(1500)
        t = await ev("document.getElementById('ipCorps').innerText")
        ok('2 prête(s)' in t and '1 doublon(s)' in t and '2 erreur(s)' in t, 'aperçu : 2 prêtes, 1 doublon, 2 erreurs', t[:300])
        ok('même patient que la ligne 2' in t and 'nom manquant' in t and 'date de naissance' in t, 'aperçu : doublon et erreurs expliqués')
        await pg.click('#ipGo'); await pg.wait_for_timeout(2500)
        nv = await ev("Object.keys(window.__fs).filter(k => /^espaces\\/cabinet-bentahila\\/patients\\//.test(k)).map(k => window.__fs[k].identite).filter(i => /^FICTIF-(IMPORT|TROIS)$/.test(i.nomF))")
        n1 = await ev("Object.keys(window.__fs).filter(k => /^espaces\\/cabinet-bentahila\\/patients\\//.test(k)).length")
        ok(n1 - n0 == 2 and len(nv) == 2, '2 dossiers créés (doublon et erreurs non importés)', [n0, n1, nv])
        a = next((i for i in nv if i['nomF'] == 'FICTIF-IMPORT'), {})
        ok(a.get('prenom') == 'Amina' and a.get('ddn') == '1971-03-12' and a.get('tel') == '0600001111' and a.get('mut') == 'CNOPS' and a.get('numOrig') == 'ANC-001', 'fiche remplie, ancien numéro gardé', a)
        ok('2 dossier(s) créé(s)' in await ev("document.getElementById('ipCorps').innerText"), 'compte rendu à l\'écran')
        async with pg.expect_download() as dl: await pg.click('#ipCR')
        ok((await dl.value).suggested_filename.startswith('Onco360_import_compte_rendu_'), 'compte rendu en Excel')
        await pg.goto(U + 'v2.html#patients'); await pg.wait_for_timeout(1500)
        await pg.fill('#q', 'ANC-003'); await pg.wait_for_timeout(800)
        t = await ev("document.getElementById('page').innerText")
        ok('FICTIF-TROIS' in t and 'ancien : ANC-003' in t, 'Patients : recherche et affichage de l\'ancien numéro', t[:300])
        await pg.set_viewport_size({'width': 390, 'height': 800}); await pg.goto(U + 'v2.html#parametres/export'); await pg.wait_for_timeout(2000)
        ok(not await ev(DEB), 'import : sans débordement à 390 px')
        ok(not pg.errs, 'aucune erreur JavaScript', pg.errs)
        await pg.close()

        print('L5 : contrôle des dossiers ; L1 : journal des erreurs')
        s = copy.deepcopy(S); k = next(k for k in s if k.startswith(E + 'patients/'))
        s[k]['rdvsJson'] = json.dumps([{'id': 'rz1', 'd': '2026-13-45', 'type': 'Consultation'}])
        pg = await ouvrir(b, s); ev = pg.evaluate
        await ev("0"); await pg.add_init_script("window.__fonctions = Object.assign(window.__fonctions || {}, { noterErreur: async (d) => { (window.__err = window.__err || []).push(d); return { ok: true }; } })")
        await pg.goto(U + 'v2.html#dossier/' + k.split('/')[-1]); await pg.wait_for_timeout(5500)
        ok('À vérifier dans ce dossier' in await ev("document.getElementById('page').innerText"), 'dossier : anomalie montrée au médecin')
        er = await ev("window.__err || []")
        ok(any(x.get('type') == 'controle' and 'rdv:date' in x.get('msg', '') for x in er), 'anomalie notée au journal des erreurs (type seulement)', er)
        ok(all('PATIENT' not in json.dumps(x) for x in er), 'aucun nom de patient envoyé')
        # erreur levée dans Onco360 (horloge des tests figée : déclenchée directement)
        await ev("window.dispatchEvent(new ErrorEvent('error', { message: \"Uncaught TypeError: Cannot read properties of null (reading 'x')\", filename: location.origin + '/js/app/chimio.js?v=1', lineno: 42, colno: 7 }))"); await pg.wait_for_timeout(800)
        er = await ev("window.__err || []")
        ok(any('null' in x.get('msg', '') and x.get('type') == 'erreur' and x.get('ligne') == 42 for x in er), 'erreur JavaScript envoyée (message, fichier, ligne)', er[-1:])
        e1 = next((x for x in er if 'null' in x.get('msg', '')), {})
        ok(e1.get('page') == '#dossier' and re.match(r'^\d{8}[a-z]$', e1.get('version', '')) is not None, 'page sans identifiant, version de l\'application', e1)
        await pg.close()

        print('L6 : cabinet suspendu, avis de l\'Administration, invitation')
        s = copy.deepcopy(S); s[E[:-1]] = dict(s.get(E[:-1], {}), actif=False, titulaire='UIDRITA', suppressionPrevue='2026-11-30T10:00:00.000Z')
        s[E + 'avisAdmin/a1'] = {'ms': 1761900000000, 'txt': 'Réglage du cabinet modifié', 'type': 'reglage'}
        s['invitations/UIDRITA_cab-x'] = {'uid': 'UIDRITA', 'espace': 'cab-x', 'cabinet': 'Cabinet X', 'role': 'medecin', 'parNom': 'Dr X'}
        pg = await ouvrir(b, s); ev = pg.evaluate
        await pg.add_init_script("window.__fonctions = Object.assign(window.__fonctions || {}, { repondreInvitation: async (d) => { window.__inv = d; return { ok: true }; } })")
        await pg.goto(U + 'v2.html#accueil'); await pg.wait_for_timeout(3000)
        t = await ev("(document.getElementById('bandLS') || {}).innerText || ''")
        ok('lecture seule' in t and '30/11/2026' in t and 'export' in t.lower(), 'bandeau « Cabinet suspendu : lecture seule », date d\'effacement', t)
        ok('Réglage du cabinet modifié' in await ev("(document.getElementById('bandAvis') || {}).innerText || ''"), 'avis de l\'Administration au titulaire')
        await ev("document.getElementById('avisVu').click()"); await pg.wait_for_timeout(400)
        ok(await ev("!document.getElementById('bandAvis') && window.__fs['utilisateurs/UIDRITA'].avisAdminVu === 1761900000000"), '« Vu » : avis retiré et noté')
        ok(await ev("!!document.getElementById('invFond') && /Dr X/.test(document.getElementById('invFond').innerText) && /Cabinet X/.test(document.getElementById('invFond').innerText)"), 'invitation proposée')
        await pg.click('#invOui'); await pg.wait_for_timeout(600)
        ok(await ev("window.__inv && window.__inv.espace === 'cab-x' && window.__inv.accepter === true && !document.getElementById('invFond')"), 'invitation acceptée (fonction serveur)')
        await pg.set_viewport_size({'width': 390, 'height': 800}); await pg.wait_for_timeout(300)
        ok(not await ev(DEB), 'bandeaux sans débordement à 390 px')
        await pg.close()

        print('L1, L9 : Administration › État de la plateforme')
        s = copy.deepcopy(S); s['administrateurs/UIDRITA'] = {'email': 'x'}
        pg = await ouvrir(b, s); ev = pg.evaluate
        etat = {'nuits': [{'k': 'releveNuit', 'lib': 'Relevé du comptable', 'le': '2026-10-31T01:45:00Z', 'ok': True, 'n': 2, 'duree': 12, 'alerte': ''}, {'k': 'agendaNuit', 'lib': 'Google Agenda (remise à plat)', 'alerte': 'jamais exécuté depuis la mise en place du suivi'}],
                'erreurs': [{'jour': '2026-10-31', 'total': 3, 'debordement': 0, 'l': [{'n': 3, 'msg': 'TypeError: x is null', 'src': 'js/app/v2.js', 'ligne': 120, 'page': 'dossier', 'roles': {'medecin': 3}, 'cabinets': ['Cabinet A'], 'version': '20261031f'}]}],
                'exports': [{'espace': 'cab-a', 'nom': 'Cabinet A', 'actif': True, 'le': '2026-10-26T00:30:00Z', 'ok': True, 'drive': 'déposé'}], 'agenda': {'comptes': 2, 'revoques': 0, 'refus': 1}, 'lu': '2026-10-31T12:00:00Z'}
        usage = {'mois': [{'mois': '2026-10', 'le': '2026-10-31T03:45:00Z', 'cabinets': {'cab-a': {'cabinet': 'Cabinet A', 'actif': True, 'dossiers': 12, 'curesValidees': 4, 'seancesValidees': 6, 'consultations': 9, 'membres': 2}}}]}
        await pg.add_init_script("window.__fonctions = Object.assign(window.__fonctions || {}, { listeCabinets: async () => ({ cabinets: [], formules: {}, bibliotheques: [], specialites: {}, archives: [], factures: [] }), etatPlateforme: async () => (" + json.dumps(etat) + "), usageLire: async () => (" + json.dumps(usage) + ") })")
        await pg.goto(U + 'admin.html#etat'); await pg.wait_for_timeout(2500)
        t = await ev("document.getElementById('page').innerText")
        ok('Traitements de nuit' in t and 'Relevé du comptable' in t and 'jamais exécuté' in t, 'traitements de nuit et alertes', t[:300])
        ok('TypeError: x is null' in t and 'js/app/v2.js:120' in t, 'erreurs des utilisateurs regroupées')
        ok('Cabinet A' in t and '1 compte(s) avec des événements refusés' in t, 'exports de la semaine et Google Agenda')
        ok('Registre d\'usage' in t and '12' in t, 'registre d\'usage du mois')
        await pg.set_viewport_size({'width': 390, 'height': 800}); await pg.wait_for_timeout(300)
        ok(not await ev(DEB), 'État de la plateforme sans débordement à 390 px')
        await pg.close()

        print('L7 : politique de sécurité du site (CSP) appliquée, sans violation')
        ok('Content-Security-Policy' in ENTETES and 'Content-Security-Policy-Report-Only' not in ENTETES, 'CSP appliquée (plus en simple observation)')
        ok('camera=()' in ENTETES.get('Permissions-Policy', '') and 'microphone=()' in ENTETES.get('Permissions-Policy', ''), 'politique des permissions : caméra et micro refusés')
        pg = await ouvrir(b, S); ev = pg.evaluate; await avec_csp(pg)
        for h in ['accueil', 'patients', 'agenda', 'salle', 'taches', 'protocoles', 'radiotherapie', 'outils', 'parametres', 'parametres/export', 'bilan', 'profil', 'documents']:
            await pg.goto(U + 'v2.html#' + h); await pg.wait_for_timeout(1300)
        k = next(k for k in S if k.startswith(E + 'patients/'))
        await pg.goto(U + 'v2.html#dossier/' + k.split('/')[-1]); await pg.wait_for_timeout(2000)
        v = await ev("window.__csp")
        ok(v == [], 'aucune violation dans Onco360 (13 pages et un dossier)', v)
        await pg.goto(U + 'cgu.html'); await pg.wait_for_timeout(500)
        ok(await ev("window.__csp") == [], 'aucune violation sur la page des CGU')
        print('L3 : guide de démarrage')
        await pg.goto(U + 'v2.html#accueil'); await pg.wait_for_timeout(2000)
        ok(await ev("!!document.querySelector('#menuCompte a#mcGuide[href=\"guide/demarrage.html\"][target=_blank]')"), 'lien « Guide de démarrage » dans le menu du compte')
        await pg.goto(U + 'guide/demarrage.html'); await pg.wait_for_timeout(1200)
        t = await ev("document.body.innerText")
        ok(all(x in t for x in ['Médecin – page 1', 'Médecin – page 2', 'Secrétaire – page 1', 'Secrétaire – page 2']), 'quatre pages : deux pour le médecin, deux pour la secrétaire')
        r = await ev("[...document.images].map(i => [i.getAttribute('src'), i.complete && i.naturalWidth > 0])")
        ok(len(r) >= 6 and all(x[1] for x in r), 'captures chargées', r)
        ok(await ev("window.__csp") == [], 'aucune violation sur le guide')
        await pg.set_viewport_size({'width': 390, 'height': 800}); await pg.wait_for_timeout(300)
        ok(not await ev(DEB), 'guide sans débordement à 390 px')
        await pg.close()
        await b.close()
    print(f'\n{ok_n} réussis, {ko_n} échoués'); raise SystemExit(1 if ko_n else 0)
asyncio.run(main())
