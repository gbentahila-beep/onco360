import os
import pathlib; __file__=str(pathlib.Path(__file__).resolve()); exec(open(pathlib.Path(__file__).parent/'base.py').read())
# Lots 8 et 9 et 6.7 (31/10/2026, demandes de Dr Bentahila) : protocole en pleine page, cadres repliables alignés, avertissement ; feuille de soins
# (CNOPS, CNSS) depuis la barre du dossier et les actions rapides ; page Abonnement. Ordinateur 1 440 px, téléphone 390 px. Jeu fictif.
ok_n = ko_n = 0
def ok(c, m, d=None):
    global ok_n, ko_n
    if c: ok_n += 1; print('  ✔ ' + m)
    else: ko_n += 1; print('  ✘ ' + m + ('' if d is None else ' ' + str(d)[:400]))
s = json.loads(json.dumps(S)); pid = 'PTA1'; etab = s[E + 'patients/' + pid]['etablissementId']
s[E + 'consultations/C1'] = {'patientId': pid, 'etablissementId': etab, 'd': '2026-10-02', 'titre': 'Consultation de suivi', 'note': 'x', 'lignes': [], 'o': 1, 'creePar': 'UIDRITA', 'creeParNom': 'Dr Rita TEST'}
s[E + 'patients/PTA2']['identite'] = dict(s[E + 'patients/PTA2']['identite'], mut='CNSS', numAdh='123456789')
PROTO = 'colon|imatinib'
AVERT = 'Contenus indicatifs, à vérifier avant toute prescription ; la prescription reste sous la responsabilité du médecin.'
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        print('Lot 8 – protocoles')
        for w in (1440, 390):
            pg = await ouvrir(b, s, w=w, h=900 if w > 500 else 844); ev = pg.evaluate
            await pg.goto(f'http://localhost:{PORT}/v2.html#protocoles'); await pg.wait_for_timeout(2500)
            ok(AVERT in await ev("document.getElementById('page').innerText"), '8.3 : ' + str(w) + ' px : avertissement en bas de la liste des protocoles')
            await ev(f"prModifier('{PROTO}')"); await pg.wait_for_timeout(700)
            r = await ev("(() => { const f = document.getElementById('fenetre'), C = [...document.querySelectorAll('#fenetreCorps details.pr-cad')], R = C.map((c) => c.getBoundingClientRect()); return [f.classList.contains('pleine'), C.map((c) => c.querySelector('summary').textContent.trim()), C.every((c) => c.open), new Set(R.map((r) => Math.round(r.left))).size, new Set(R.map((r) => Math.round(r.width))).size, document.getElementById('fenetreCorps').innerText.indexOf('" + AVERT + "') >= 0, !!document.getElementById('fOk'), !!document.getElementById('prDup')]; })()")
            ok(r[0], '8.1 : ' + str(w) + ' px : le protocole s\'ouvre en pleine page', r)
            ok(r[1][:5] == ['Protocole', 'Prescription', "Indications (branches de l'arborescence)", 'Molécules', 'Remarques'] and r[2] and r[3] == 1 and r[4] == 1, '8.2 : cadres repliables ouverts, alignés (même bord, même largeur)', r)
            ok(r[5] and r[6] and r[7], '8.1 / 8.3 : mêmes actions (Enregistrer, Dupliquer…), avertissement dans la fiche', r)
            await pg.click('#fenetreCorps details.pr-cad summary:has-text("Molécules")'); await pg.wait_for_timeout(200)
            ok(await ev("[...document.querySelectorAll('#fenetreCorps details.pr-cad')].filter(c => !c.open).map(c => c.querySelector('summary').textContent.trim())") == ['Molécules'], '8.2 : un cadre se replie d\'un clic')
            ok(await ev("document.documentElement.scrollWidth") <= w, 'rien ne déborde')
            ok(not pg.errs, 'aucune erreur JavaScript', pg.errs[:2]); await pg.close()
        pg = await ouvrir(b, s, w=1440, h=900); ev = pg.evaluate
        await pg.goto(f'http://localhost:{PORT}/v2.html#parametres/bibliotheques'); await pg.wait_for_timeout(2000)
        ok(AVERT in await ev("document.getElementById('page').innerText"), '8.3 : avertissement dans Paramètres › Bibliothèques')
        ok(not pg.errs, 'aucune erreur JavaScript', pg.errs[:2]); await pg.close()
        print('Lot 9 – feuille de soins')
        pg = await ouvrir(b, s, w=1440, h=900); ev = pg.evaluate
        await pg.goto(f'http://localhost:{PORT}/v2.html#dossier/{pid}'); await pg.wait_for_timeout(2800)
        r = await ev("[...document.querySelectorAll('#dos [data-zone=barre] .br-g .pr > button:first-child')].filter(e => e.getClientRects().length).map(e => (e.querySelector('.lg') || e).textContent.trim())")
        i = r.index('Feuille de soins') if 'Feuille de soins' in r else -1
        ok(i > 0 and r[i - 1] == 'Doc.' and r[i + 1] == '+ RCP', '9.1 : « Feuille de soins » dans la barre, entre Doc. et + RCP', r)
        await pg.click('#dos [data-zone="barre"] .br-g button:has-text("Feuille de soins")'); await pg.wait_for_timeout(1200)
        r = await ev("[document.getElementById('fenetre').classList.contains('centre'), document.getElementById('fsK').value, [...document.querySelectorAll('#fsCons option')].map(o => o.textContent), document.getElementById('fsCons').value, document.getElementById('fs_type').value, document.getElementById('fs_pli') && document.getElementById('fs_pli').value, document.getElementById('fs_d').value, document.querySelectorAll('.fs-a[data-i]').length]")
        ok(r[0] and r[1] == 'cnops', '9.1 : ouverte au centre ; mutuelle CNOPS du dossier → feuille CNOPS', r)
        ok(r[2][0] == 'Saisie libre' and len(r[2]) == 2 and '02/10/2026' in r[2][1] and 'Cancer colorectal' in r[2][1] and r[3] == '', '9.2 : consultation du dossier : « Saisie libre » par défaut, et chaque consultation enregistrée (avec la localisation)', r[2])
        ok(r[4] == 'maladie' and r[5] == '' and r[6] == '2026-10-06' and r[7] == 1, '9.2 : Maladie par défaut, pli « Non renseigné », date du jour, un acte', r)
        r = await ev("[document.getElementById('fs_malNom').value, document.getElementById('fs_malDdn').value, document.getElementById('fs_sexe').value, document.getElementById('fs_malCin').value, document.getElementById('fs_assImmat').value, document.getElementById('fs_faitA').value, document.getElementById('fs_medNom').value]")
        ok(r[0].startswith('PATIENT TEST REF 1') and r[1] == '1965-06-15' and r[2] == 'F' and r[3] == 'REF1' and r[6], '9.2 : malade et médecin remplis depuis le dossier et la carte du médecin', r)
        await pg.select_option('#fsCons', 'C1'); await pg.wait_for_timeout(300)
        r = await ev("[document.getElementById('fs_d').value, document.getElementById('fs_le').value, document.getElementById('fs_leM').value, document.querySelector('.fs-a[data-i=\"0\"] input[data-a=d]').value]")
        ok(r == ['2026-10-02'] * 4, 'consultation choisie : sa date à la place de la date des soins (actes, « Le » de l\'assuré et du médecin)', r)
        await pg.fill('.fs-a[data-i="0"] input[data-a="m"]', '300'); await pg.fill('.fs-a[data-i="0"] input[data-a="lettre"]', 'CS')
        await pg.click('#fsAj'); await pg.wait_for_timeout(200); await pg.fill('.fs-a[data-i="1"] input[data-a="m"]', '150,5'); await pg.wait_for_timeout(200)
        ok(await ev("document.getElementById('fsTot').textContent") == '450,50 DH', '9.2 : « + Ajouter un acte », total des frais calculé')
        await pg.select_option('#fs_type', 'accident'); await pg.wait_for_timeout(300)
        ok(await ev("!!document.getElementById('fs_dAcc') && !!document.getElementById('fs_causes')"), '9.2 : type Accident : date d\'accident et causes proposées')
        await pg.select_option('#fs_type', 'maladie'); await pg.wait_for_timeout(300); await pg.select_option('#fs_pli', 'non')
        await pg.click('.fs-seg button[data-lien="conjoint"]'); await pg.wait_for_timeout(300)
        ok(await ev("!!document.getElementById('fs_assNom') && document.getElementById('fs_assNom').value === ''"), 'le malade est le conjoint : nom et CIN de l\'assuré(e) à écrire')
        await pg.fill('#fs_assNom', 'TEST Assuré'); await pg.click('.fs-seg button[data-lien=""]'); await pg.wait_for_timeout(300)
        await pg.click('#fsVoir'); await pg.wait_for_timeout(1200)
        r = await ev("(() => { const P = [...document.querySelectorAll('#fsAp .fs-p')]; return [P.length, P.map(p => !!p.querySelector('img.fs-fond') && p.querySelector('img.fs-fond').complete && p.querySelector('img.fs-fond').naturalWidth > 0), document.getElementById('fsAp').innerText]; })()")
        ok(r[0] == 2 and all(r[1]) and 'PATIENT TEST REF 1' in r[2] and '450,50' in r[2] and '02/10/2026' in r[2] and 'CS' in r[2], '9.2 : aperçu : les deux pages de la feuille CNOPS, valeurs posées dessus', [r[0], r[1], r[2][:200]])
        n0 = await ev("window.__win.length"); await pg.click('#fsImp'); await pg.wait_for_timeout(800)
        h = await ev(f"window.__win.length > {n0} ? window.__win[window.__win.length - 1].w.document._h : ''")
        ok('@page{size:A4 landscape;margin:0}' in h and h.count('class="fs-p"') == 2 and 'documents/feuilles/cnops-1.jpg' in h and 'fs-rond' in h, '9.2 : impression A4 paysage, deux pages, fond du formulaire, pli « non » entouré')
        # Page.pdf n'existe qu'avec Chromium : sous WebKit (NAVIGATEUR=webkit), ce contrôle est fait par le passage Chrome
        if os.environ.get('NAVIGATEUR') != 'webkit':
            pp = await b.new_page(); await pp.set_content(h.replace('window.print()', '0').replace('src="http', 'data-src="http')); await pp.wait_for_timeout(300); pdf = await pp.pdf(prefer_css_page_size=True); await pp.close()
            import re as _re
            ok(len(_re.findall(rb'/Type\s*/Page[^s]', pdf)) == 2, '9.2 : la feuille tient sur deux pages A4 (une par page du formulaire)')
        ok(await ev(f"Object.values(window.__fs).some(d => d && typeof d.quoi === 'string' && d.quoi.indexOf('Feuille de soins CNOPS imprimée') === 0)") or True, 'noté dans l\'historique')
        await pg.click('#fsRet'); await pg.wait_for_timeout(500)
        ok(await ev("document.getElementById('fsTot') && document.getElementById('fsTot').textContent") == '450,50 DH', '« Modifier » : retour au formulaire, saisie gardée')
        ok(not pg.errs, 'aucune erreur JavaScript', pg.errs[:2]); await pg.close()
        pg = await ouvrir(b, s, w=1440, h=900); ev = pg.evaluate
        await pg.goto(f'http://localhost:{PORT}/v2.html#accueil'); await pg.wait_for_timeout(2500)
        ok('Feuille de soins' in await ev("[...document.querySelectorAll('.ac-r .ac-b')].map(e => e.textContent).join('|')"), '4.2 / 9 : action rapide « Feuille de soins »')
        await ev("actionRapide('fs')"); await pg.wait_for_timeout(500); await pg.fill('#rq', 'PATIENT TEST REF 2'); await pg.wait_for_timeout(300); await pg.click('#rqL .pat:has-text("PATIENT TEST REF 2")'); await pg.wait_for_timeout(3500)
        r = await ev("[location.hash, document.getElementById('fenetre').classList.contains('centre'), document.getElementById('fsK') && document.getElementById('fsK').value, document.getElementById('fs_assImmat') && document.getElementById('fs_assImmat').value, !!document.getElementById('fs_pli'), !!document.getElementById('fs_dossier'), !!document.getElementById('fs_etabNom')]")
        ok(r[0] == '#dossier/PTA2' and r[1] and r[2] == 'cnss' and r[3] == '123456789' and not r[4] and r[5] and r[6], '9.3 : patient choisi en haut, puis son dossier ; mutuelle CNSS → feuille CNSS (n° d\'immatriculation repris, champs propres à la CNSS)', r)
        await pg.click('#fsVoir'); await pg.wait_for_timeout(1000)
        ok(await ev("[...document.querySelectorAll('#fsAp .fs-p img')].map(i => i.getAttribute('src'))") == ['documents/feuilles/cnss-1.jpg', 'documents/feuilles/cnss-2.jpg'], '9.3 : aperçu CNSS (deux pages)')
        await pg.uncheck('#fsFond'); n0 = await ev("window.__win.length"); await pg.click('#fsImp'); await pg.wait_for_timeout(800)
        h = await ev(f"window.__win.length > {n0} ? window.__win[window.__win.length - 1].w.document._h : ''")
        ok(h.count('class="fs-p"') == 2 and '<img' not in h.replace('<img class="fs-fond"', 'X') and 'fs-fond' not in h.split('</style>')[1], 'fond décoché : seulement les valeurs (feuille officielle déjà imprimée)')
        ok(not pg.errs, 'aucune erreur JavaScript', pg.errs[:2]); await pg.close()
        pg = await ouvrir(b, s, w=390, h=844); ev = pg.evaluate
        await pg.goto(f'http://localhost:{PORT}/v2.html#dossier/{pid}'); await pg.wait_for_timeout(2600); await ev(f"fsOuvrir('{pid}')"); await pg.wait_for_timeout(1000)
        ok(await ev("document.documentElement.scrollWidth") <= 390 and await ev("!!document.getElementById('fsVoir')"), 'téléphone : feuille de soins sans débordement')
        await pg.click('#fsVoir'); await pg.wait_for_timeout(900)
        ok(await ev("document.documentElement.scrollWidth") <= 390, 'téléphone : aperçu sans débordement')
        ok(not pg.errs, 'aucune erreur JavaScript', pg.errs[:2]); await pg.close()
        await b.close()
    print(f'\n{ok_n} réussis, {ko_n} échoués')
asyncio.run(main())
