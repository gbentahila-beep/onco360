import pathlib; __file__=str(pathlib.Path(__file__).resolve()); exec(open(pathlib.Path(__file__).parent/'base.py').read())
# Lots 5 à 7 (31/10/2026, demandes de Dr Bentahila, document « Onco360 — Demandes à faire ») : RCP en tableau, salle d'attente complète, page
# Documents (dépôt pour plusieurs patients) ; Paramètres (accueil et recherche, familles à une rubrique, téléphone), reçu modifiable dans les
# courriers, Accès en tableau ; Finances (cadres Séance et Radiothérapie, une ligne par lieu, tarif commun), Bilan (espèces, téléphone).
# Ordinateur 1 440 px, téléphone 390 px. Jeu fictif.
src_recu = open(pathlib.Path(__file__).parent / 'test_recu.py').read()
exec(open(pathlib.Path(__file__).parent / 'demo_seed.py').read())
ok_n = ko_n = 0
def ok(c, m, d=None):
    global ok_n, ko_n
    if c: ok_n += 1; print('  ✔ ' + m)
    else: ko_n += 1; print('  ✘ ' + m + ('' if d is None else ' ' + str(d)[:400]))
s = json.loads(json.dumps(S))
pids = [k.split('/')[-1] for k in s if k.startswith(E + 'patients/') and k.count('/') == 3]
pid = pids[0]; etab = s[E + 'patients/' + pid]['etablissementId']
for i in range(3): s[E + 'rcp/R%d' % i] = {'patientId': pid, 'patientNom': 'X', 'etablissementId': etab, 'd': '2026-10-08', 'q': 'Question %d ?' % i, 'ins': '2026-10-01', 'fait': i == 2, 'o': i, 'creePar': 'UIDRITA', 'creeParNom': 'Dr Rita TEST', 'decisionTxt': 'RT adjuvante' if i == 2 else ''}
# 5.2 : 26 rendez-vous le jour du test
n = 0
for k, v in list(s.items()):
    if k.startswith(E + 'patients/') and k.count('/') == 3 and n < 26:
        r = json.loads(v.get('rdvsJson') or '[]'); r.append({'id': 'rS%d' % n, 'type': 'Suivi', 'd': '2026-10-06', 'h': '%02d:%02d' % (8 + n // 4, (n % 4) * 15), 'st': 'prevu'}); v['rdvsJson'] = json.dumps(r); n += 1
VIS = "(e) => !!e && e.getClientRects().length > 0 && getComputedStyle(e).visibility !== 'hidden'"
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        # ───── Lot 5 ─────
        print('Lot 5 – RCP, salle d\'attente, Documents (1 440 px)')
        pg = await ouvrir(b, s, w=1440, h=900); ev = pg.evaluate
        await pg.goto(f'http://localhost:{PORT}/v2.html#rcp'); await pg.wait_for_timeout(2500); await ev("rcpPer('2026-10-05','2026-10-11')"); await pg.wait_for_timeout(300)
        r = await ev("[[...document.querySelectorAll('.rcp-tab .ta-h span')].map(e => e.textContent), document.querySelectorAll('.rcp-tab .rcp-r').length, [...document.querySelectorAll('.rcp-tab .rcp-r select.st')].map(e => e.value)]")
        ok(r[0] == ['Patient', 'Né(e) le', 'Question', 'Décision', 'Inscrit', 'Statut', 'Actions'] and r[1] == 3 and r[2] == ['afaire', 'afaire', 'fait'], '5.1 : RCP en tableau (Patient, Né(e) le, Question, Décision, Inscrit, Statut, Actions)', r)
        r = await ev("(() => { const l = document.querySelector('.rcp-tab .rcp-r'); return [l.querySelector('.c-n').textContent, l.querySelector('.ins').textContent, [...l.querySelectorAll('.c-a button')].map(e => e.title)]; })()")
        ok('ans' in r[0] and 'Dr Rita TEST' in r[1] and r[2] == ['Valider (passé en RCP)', "Modifier l'inscription", "Supprimer l'inscription"], '5.1 : date de naissance (âge), inscrit (date et par qui), actions Valider / Modifier / Supprimer', r)
        await pg.click('.rcp-tab .rcp-r .c-a button[title^="Valider"]'); await pg.wait_for_timeout(700)
        ok(await ev("window.__fs['espaces/cabinet-bentahila/rcp/R0'].fait === true && [...document.querySelectorAll('.rcp-tab .rcp-r select.st')].filter(e => e.value === 'fait').length === 2"), '5.1 : « Valider » passe l\'inscription en Validé (case Fait)')
        await pg.select_option('.rcp-tab .rcp-r select.st >> nth=0', 'afaire'); await pg.wait_for_timeout(700)
        ok(await ev("window.__fs['espaces/cabinet-bentahila/rcp/R0'].fait === false"), '5.1 : statut « En attente » remis depuis le menu')
        for w in (1440, 390):
            if w == 390: await pg.close(); pg = await ouvrir(b, s, w=390, h=844); ev = pg.evaluate
            await pg.goto(f'http://localhost:{PORT}/v2.html#salle'); await pg.wait_for_timeout(2800)
            r = await ev("(() => { const d = document.getElementById('saDef'), L = [...document.querySelectorAll('#saL .sa-l:not(.ent)')], c = d.closest('section'); return [L.length, d.scrollHeight <= d.clientHeight + 1, getComputedStyle(d).overflowY, Math.round(L[L.length - 1].getBoundingClientRect().bottom) <= Math.round(c.getBoundingClientRect().bottom), document.documentElement.scrollWidth <= innerWidth]; })()")
            ok(r[0] == 26 and r[1] and r[2] == 'hidden' and r[3] and r[4], '5.2 : ' + str(w) + ' px : les 26 rendez-vous, sans cadre qui défile, dernière ligne entière dans la carte', r)
        ok(not pg.errs, 'aucune erreur JavaScript', pg.errs[:2]); await pg.close()
        pg = await ouvrir(b, s, w=1440, h=900); ev = pg.evaluate
        await pg.goto(f'http://localhost:{PORT}/v2.html#accueil'); await pg.wait_for_timeout(2500)
        r = await ev("[...document.querySelectorAll('nav a[data-p]')].filter(" + VIS + ").map(a => a.dataset.p)")
        ok('documents' not in r, 'UX2 : « Documents » retiré du menu du médecin (secrétaire seulement, test_ux1_2)', r)
        await pg.goto(f'http://localhost:{PORT}/v2.html#documents'); await pg.wait_for_timeout(1500)
        await pg.set_input_files('#dpF', files=[{'name': 'bio.pdf', 'mimeType': 'application/pdf', 'buffer': b'%PDF-1.4 bio'}, {'name': 'scanner_thorax.pdf', 'mimeType': 'application/pdf', 'buffer': b'%PDF-1.4 scan'}]); await pg.wait_for_timeout(400)
        ok(await ev("document.querySelectorAll('.dp-r').length") == 2, '5.3 : deux fichiers choisis, une ligne chacun')
        await pg.select_option('#dpTT', 'Biologie'); await pg.wait_for_timeout(200)
        await pg.click('#dpOk'); await pg.wait_for_timeout(400)
        r = await ev("[...document.querySelectorAll('.dp-msg')].map(e => e.textContent)")
        ok(r == ['Patient à choisir.', 'Patient à choisir.'] and not await ev("Object.keys(window.__fs).some(k => k.includes('/fichiers/') && window.__fs[k].nom === 'bio.pdf')"), '5.3 : sans patient : rien n\'est envoyé, chaque ligne dit ce qui manque', r)
        await pg.fill('input[data-k="q"][data-i="0"]', 'PATIENT TEST REF 1'); await pg.wait_for_timeout(300); await pg.click('.dp-pl[data-i="0"] .pat >> nth=0'); await pg.wait_for_timeout(300)
        await pg.fill('input[data-k="q"][data-i="1"]', 'PATIENT TEST REF 2'); await pg.wait_for_timeout(300); await pg.click('.dp-pl[data-i="1"] .pat:has-text("PATIENT TEST REF 2")'); await pg.wait_for_timeout(300)
        await pg.select_option('select[data-k="type"][data-i="1"]', 'Imagerie')
        await pg.click('#dpOk'); await pg.wait_for_timeout(1500)
        r = await ev("Object.values(window.__fs).filter(f => f && f.chemin && (f.nom === 'bio.pdf' || f.nom === 'scanner_thorax.pdf')).map(f => [f.nom, f.patientId, f.type, f.titre]).sort()")
        ok(r == [['bio.pdf', 'PTA1', 'Biologie', 'bio'], ['scanner_thorax.pdf', 'PTA2', 'Imagerie', 'scanner thorax']] and await ev("document.querySelectorAll('.dp-r.ok').length") == 2, '5.3 : chaque document rangé dans le dossier de son patient, avec son type et son titre', r)
        await pg.goto(f'http://localhost:{PORT}/v2.html#dossier/PTA2'); await pg.wait_for_timeout(2500); await ev("ongletDossier('PTA2','doc')"); await pg.wait_for_timeout(1200)
        ok('scanner thorax' in await ev("(document.getElementById('op-doc') || document.body).innerText"), '5.3 : le dossier relit tous ses documents (le dépôt n\'a pas remplacé sa liste)')
        ok(not pg.errs, 'aucune erreur JavaScript', pg.errs[:2])
        # ───── Lot 6 ─────
        print('Lot 6 – Paramètres, reçu, Accès')
        await pg.goto(f'http://localhost:{PORT}/v2.html#parametres'); await pg.wait_for_timeout(2000)
        r = await ev("[document.querySelector('.cf-acc h2') && document.querySelector('.cf-acc h2').textContent, !!document.querySelector('.cf-acc .cf-acc-ill'), document.querySelectorAll('.cf-nav .cf-g.ouv').length, document.querySelectorAll('.cf-qc').length, document.body.innerText.indexOf('Que voulez-vous faire ?') >= 0]")
        ok(r[0] == 'Bonjour Dr Test' and r[1] and r[2] == 0 and r[3] >= 5 and r[4], '6.1 : accueil des Paramètres (bonjour, « Que voulez-vous faire ? », dessin), aucune famille ouverte d\'office', r)
        for q, att in (('google agenda', 'Google Agenda'), ('impression', 'Impression'), ('export', 'Export des données'), ('tableau de bord', 'Tableau de bord'), ('mutuelles', 'Listes')):
            await pg.fill('#cfQ', q); await pg.wait_for_timeout(150)
            r = await ev("[...document.querySelectorAll('#cfQr .cf-qi b')].map(e => e.textContent)")
            ok(att in r, '6.1 : recherche « ' + q + ' » → ' + att, r)
        await pg.fill('#cfQ', 'zzzz'); await pg.wait_for_timeout(150)
        ok('Aucun paramètre' in await ev("document.getElementById('cfQr').innerText"), '6.1 : recherche sans résultat : une phrase')
        await pg.click('.cf-nav .cf-gt:has-text("Agenda et rappels")'); await pg.wait_for_timeout(800)
        ok(pg.url.endswith('#parametres/horaires'), '6.1 : un clic sur une famille ouvre sa 1re rubrique', pg.url)
        await pg.click('.cf-nav .cf-gt:has-text("Finances")'); await pg.wait_for_timeout(1000)
        r = await ev("[location.hash, !!document.querySelector('.cf-nav .cf-g.ouv .cf-sous'), document.body.innerText.indexOf('Activités et rémunérations') >= 0]")
        ok(r[0] == '#parametres/activites' and not r[1] and r[2], '6.2 : Finances : le contenu s\'affiche au clic sur la famille, sans sous-onglet unique', r)
        await pg.click('.cf-nav .cf-gt:has-text("Laboratoires")'); await pg.wait_for_timeout(1000)
        ok(await ev("[location.hash, !!document.querySelector('.cf-nav .cf-g.ouv .cf-sous')]") == ['#parametres/laboratoires', False], '6.2 : Laboratoires : pareil')
        # 6.4 : reçu dans Bibliothèques › Courriers
        await pg.goto(f'http://localhost:{PORT}/v2.html#parametres/bibliotheques'); await pg.wait_for_timeout(1800)
        ok(not pg.errs, 'aucune erreur JavaScript', pg.errs[:2]); await pg.close()
        exec(src_recu[src_recu.index('S2, PIDS = avec_demo'):src_recu.index('async def pages')], globals())
        S3 = json.loads(json.dumps(S2))
        pg = await ouvrir(b, S3, w=1440, h=900); ev = pg.evaluate
        await pg.goto(f'http://localhost:{PORT}/v2.html#dossier/{P7}'); await pg.wait_for_timeout(3500)
        h0 = await recu(pg)
        ok('REÇU' in h0 and 'R-2026-0001' in h0 and '400,00 DH' in h0 and 'Visa accueil' in h0, '6.4 : reçu d\'origine inchangé (modèle de départ rempli)')
        r = await ev("(async () => { const m = await import('./js/app/ordonnances.js'); return (await m.modeleRT('recu')).indexOf('{numero}') >= 0; })()")
        ok(r, '6.4 : modèle « Reçu (note d\'honoraires) » proposé dans la bibliothèque des courriers (rt-recu)')
        await pg.close()
        S3[E + 'bibliotheques/courriers'] = {'data': json.dumps([{'id': 'rt-recu', 'rt': 'recu', 'nom': "Reçu (note d'honoraires)", 'html': '<p>NOTE D\'HONORAIRES DU CABINET</p><p>{patient_nom} · {montant} · {mode} · n° {numero}</p>'}])}
        pg = await ouvrir(b, S3, w=1440, h=900); ev = pg.evaluate
        await pg.goto(f'http://localhost:{PORT}/v2.html#dossier/{P7}'); await pg.wait_for_timeout(3500)
        h1 = await recu(pg)
        ok("NOTE D'HONORAIRES DU CABINET" in h1.replace('&#39;', "'") and '400,00 DH' in h1 and 'Espèces' in h1 and 'R-2026-0001' in h1, '6.4 : modèle modifié par le médecin : utilisé au reçu suivant (champs remplis)', h1[-300:])
        await pg.goto(f'http://localhost:{PORT}/v2.html#parametres/bibliotheques'); await pg.wait_for_timeout(1500)
        ok(not pg.errs, 'aucune erreur JavaScript', pg.errs[:2]); await pg.close()
        pg = await ouvrir(b, s, w=1440, h=900); ev = pg.evaluate
        await pg.goto(f'http://localhost:{PORT}/v2.html#profil/acces'); await pg.wait_for_timeout(2500)
        r = await ev("[[...document.querySelectorAll('.ac-tab .ta-h span')].map(e => e.textContent), document.querySelectorAll('.ac-tab .ac-r').length]")
        ok(r[0] == ['Utilisateur', 'Rôle', 'Contact', 'Établissement(s)', 'Actions'] and r[1] >= 1, '6.6 : Accès en tableau (Utilisateur, Rôle, Contact, Établissement(s), Actions)', r)
        ok(not pg.errs, 'aucune erreur JavaScript', pg.errs[:2]); await pg.close()
        pg = await ouvrir(b, s, w=390, h=844); ev = pg.evaluate
        await pg.goto(f'http://localhost:{PORT}/v2.html#parametres/horaires'); await pg.wait_for_timeout(2200)
        r = await ev("(() => { const t = document.querySelector('.cf-tel'), b = [...t.querySelectorAll('button')]; return [getComputedStyle(document.querySelector('.cf-nav')).display, new Set(b.map(e => Math.round(e.getBoundingClientRect().top))).size, t.scrollWidth > t.clientWidth, getComputedStyle(document.querySelector('.cf-telz')).position, (t.querySelector('button.on') || {}).textContent, document.documentElement.scrollWidth <= 390, !!document.querySelector('.defile-cadre .df-fl')]; })()")
        ok(r[0] == 'none' and r[1] == 1 and r[2] and r[3] == 'sticky' and r[4] == 'Agenda et rappels' and r[5] and r[6], '6.3 : téléphone : familles sur une ligne qui défile, avec flèche, collées en haut', r)
        await ev("window.scrollTo(0, 600)"); await pg.wait_for_timeout(300)
        r = await ev("[Math.round(document.querySelector('#btParam').getBoundingClientRect().top), Math.round(document.querySelector('.cf-telz').getBoundingClientRect().top)]")
        ok(r[0] >= 0 and r[0] < 60 and r[1] <= 70, '6.3 : en faisant défiler, la roue Paramètres et les familles restent à leur place', r)
        await pg.goto(f'http://localhost:{PORT}/v2.html#parametres'); await pg.wait_for_timeout(1500)
        ok(await ev("document.documentElement.scrollWidth") <= 390 and await ev("!!document.querySelector('.cf-acc #cfQ')"), '6.1 : accueil des Paramètres sur téléphone, sans débordement')
        ok(not pg.errs, 'aucune erreur JavaScript', pg.errs[:2]); await pg.close()
        # ───── Lot 7 ─────
        print('Lot 7 – Finances, Bilan')
        s7 = json.loads(json.dumps(s)); T = json.loads(s7[E + 'finances/tarifs']['data'])
        T['tauxRT'] = {'retro': 60, 'impot': 10}; T['seanceCommune'] = {'type': 'seance', 'libelle': 'Séance de chimiothérapie', 'historique': [{'depuis': '2000-01-01', 'brut': 500, 'retro': 50, 'impot': 10}]}
        s7[E + 'finances/tarifs'] = {'data': json.dumps(T)}
        pg = await ouvrir(b, s7, w=1440, h=900); ev = pg.evaluate
        await pg.goto(f'http://localhost:{PORT}/v2.html#parametres/activites'); await pg.wait_for_timeout(2500)
        r = await ev("[...document.querySelectorAll('#page section.carte')][0].innerText")
        ok('Séance de chimiothérapie' not in r and 'Radiothérapie (tarif' not in r, '7.1 / 7.2 : ni « Séance de chimiothérapie » ni « Radiothérapie (tarif de l\'acte) » dans le tableau des activités')
        r = await ev("(() => { const c = document.querySelector('.pa-seance'); return [!!c, [...c.querySelectorAll('.pa-lieux tr')].slice(1).map(tr => [tr.querySelector('b').textContent, tr.querySelector('select').value])]; })()")
        ok(r[0] and sorted(r[1]) == [['CIOC', 'pro'], ['HCK', 'com'], ['HGC', 'pro']], '7.1 : cadre « Séance de chimiothérapie » : une ligne par lieu, tarif commun pour HCK (sans ligne propre)', r)
        r = await ev("(() => { const c = document.querySelector('[data-fn=\"rt.tarifs\"]'); return [...c.querySelectorAll('.pa-lieux tr')].slice(1).map(tr => [tr.querySelector('b').textContent, tr.querySelector('select').value, tr.querySelectorAll('input')[0].value]); })()")
        ok(sorted(r) == [['CIOC', 'pro', '60'], ['HCK', 'pro', '70'], ['HGC', 'pro', '60']], '7.2 : cadre « Actes de radiothérapie » : une ligne par lieu d\'exercice (taux propres ou commun)', r)
        r = await ev("(() => { const tr = [...document.querySelectorAll('.pa-seance .pa-lieux tr')].find(t => t.querySelector('b') && t.querySelector('b').textContent === 'HCK'); return [...tr.querySelectorAll('input')].map(e => [e.value, e.disabled]); })()")
        ok(r == [['500', True], ['50', True], ['10', True]], '7.3 : HCK : tarif commun 500 DH, 50 %, 10 % (non modifiable sur sa ligne)', r)
        await pg.select_option('.pa-seance .pa-lieux tr:has(b:text-is("HCK")) select', 'pro'); await pg.wait_for_timeout(400)
        await pg.fill('.pa-seance .pa-lieux tr:has(b:text-is("HCK")) input >> nth=1', '30'); await pg.keyboard.press('Tab'); await pg.wait_for_timeout(300)
        await pg.click('#paOk'); await pg.wait_for_timeout(1000)
        T2 = json.loads(await ev("window.__fs['espaces/cabinet-bentahila/finances/tarifs'].data"))
        a = [x for x in T2['etablissements']['HCK']['activites'] if x['type'] == 'seance']
        ok(len(a) == 1 and a[0]['historique'][-1]['retro'] == 30 and T2['seanceCommune']['historique'][0]['retro'] == 50, '7.3 : « Taux propres » pour HCK : sa ligne enregistrée (30 %), le tarif commun reste', a)
        ok(not pg.errs, 'aucune erreur JavaScript', pg.errs[:2]); await pg.close()
        pg = await ouvrir(b, s, w=1440, h=900); ev = pg.evaluate
        await pg.goto(f'http://localhost:{PORT}/v2.html#bilan'); await pg.wait_for_timeout(4000)
        r = await ev("[...document.querySelectorAll('#biRg select')].map(s => [...s.options].map(o => o.textContent))")
        ok(any('Espèces' in l for l in r), '7.4 : filtre « Mode » : Espèces', r)
        btn = await ev("typeof biRgFiche === 'function'"); await ev("biRgFiche()"); await pg.wait_for_timeout(500)
        ok(btn and 'Espèces' in await ev("[...document.querySelectorAll('#rgMode option')].map(o => o.textContent).join('|')"), '7.4 : « Nouveau versement ou règlement reçu » : mode Espèces')
        await pg.select_option('#rgHop', index=1); await pg.select_option('#rgMode', 'esp'); await pg.fill('#rgM', '1500'); await pg.click('#rgOk'); await pg.wait_for_timeout(1200)
        r = await ev("(() => { const t = [...document.querySelectorAll('#biRg table')][0]; return [[...t.querySelectorAll('th')].map(e => e.textContent), t.innerText]; })()")
        ok('Espèces' in r[0] and '1 500' in r[1].replace('\u202f', ' ').replace('\xa0', ' '), '7.4 : règlement en espèces enregistré, colonne « Espèces » dans les totaux', r)
        ok(not pg.errs, 'aucune erreur JavaScript', pg.errs[:2]); await pg.close()
        pg = await ouvrir(b, s, w=390, h=844); ev = pg.evaluate
        await pg.goto(f'http://localhost:{PORT}/v2.html#bilan'); await pg.wait_for_timeout(4000); await ev("biF('per','perso')"); await pg.wait_for_timeout(800)
        R = "(e) => { const r = e.getBoundingClientRect(); return [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]; }"
        r = await ev("(() => { const R = " + R + ", c = R(document.getElementById('biCor')), a = R(document.querySelector('.bi-act .bt')), m = R(document.querySelector('.bi-act .mpts')), du = R(document.querySelector('.bi-ligne input[type=date]')), au = R([...document.querySelectorAll('.bi-ligne input[type=date]')][1]); return [c, a, m, du, au]; })()")
        c, a_, m, du, au = r
        ok(abs(c[1] - a_[1]) <= 2 and abs(c[3] - a_[3]) <= 2 and a_[0] >= c[2] + 6 and m[2] <= 390 - 12, '7.5 : téléphone : Actualiser et « ⋯ » sur la ligne du menu Référent, alignés avec lui', r)
        ok(abs(du[1] - au[1]) <= 1 and au[0] >= du[2] + 6, '7.5 : Période personnalisée : Du et Au côte à côte, sans se chevaucher', r)
        ok(await ev("document.documentElement.scrollWidth") <= 390, 'rien ne déborde')
        ok(not pg.errs, 'aucune erreur JavaScript', pg.errs[:2]); await pg.close()
        await b.close()
    print(f'\n{ok_n} réussis, {ko_n} échoués')
asyncio.run(main())
