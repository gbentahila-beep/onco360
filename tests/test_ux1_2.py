import pathlib; __file__=str(pathlib.Path(__file__).resolve()); exec(open(pathlib.Path(__file__).parent/'base.py').read())
# UX1 et UX2 (01/11/2026, phase UX) : défauts trouvés au tour et décisions de Dr Bentahila sur le dossier, le tableau de bord et le menu.
import copy
ok_n = ko_n = 0
def ok(c, m, d=None):
    global ok_n, ko_n
    if c: ok_n += 1; print('  ✔ ' + m)
    else: ko_n += 1; print('  ✘ ' + m + ('' if d is None else ' ' + str(d)[:400]))
U = f'http://localhost:{PORT}/v2.html#'
S2 = copy.deepcopy(S)
S2[E + 'membres/SEC'] = {"role": "assistante", "nom": "SEC", "email": "sec@test.ma", "actif": True, "tousEtablissements": True, "etablissements": [], "droits": {}}
S2[E + 'historique/HADM'] = {'parUid': 'onco360-admin', 'parNom': "Administration d'Onco360", 'le': '2026-10-06T23:00:00Z', 'patientId': '', 'patient': '', 'quoi': 'RÉGLAGE ADMIN'}
S2[E + 'historique/HMED'] = {'parUid': 'UIDRITA', 'parNom': 'Dr TEST', 'le': '2026-10-06T22:00:00Z', 'patientId': 'PTA1', 'patient': 'PATIENT TEST REF 1', 'quoi': 'Consultation ajoutée : Suivi'}
S2[E + 'patients/PTA1']['clinique'] = dict(S2[E + 'patients/PTA1'].get('clinique') or {}, diag='Sein')
CHIMIO = "[...document.querySelectorAll('#dos [data-zone=travail] button')].find(b=>/^Chimioth/.test(b.textContent.trim())).click()"
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        # UX1 : Salle d'attente à 1 280 px, patient en salle : la colonne des boutons ne recouvre plus PRIX ; « En salle » entier
        pg = await ouvrir(b, S2, w=1280, t="2026-09-30T10:00:00"); ev = pg.evaluate
        await pg.goto(U + 'salle'); await pg.wait_for_timeout(2500)
        await ev("[...document.querySelectorAll('#saDef [data-k] button')].find(x=>/Arriv/i.test(x.textContent)).click()"); await pg.wait_for_timeout(1200)
        await ev("[...document.querySelectorAll('button,[role=tab]')].find(x=>/En salle d/.test(x.textContent)).click()"); await pg.wait_for_timeout(800)
        r = await ev("(()=>{const l=document.querySelector('#saDef [data-k]'), g=(s)=>l.querySelector(s).getBoundingClientRect(); const st=l.querySelector('.c-st'); return {px:g('.px').right, act:g('.actr').left, st:st.scrollWidth<=st.clientWidth+1, txt:st.innerText, h:l.getBoundingClientRect().height, nm:l.querySelector('.nm').scrollHeight<=l.getBoundingClientRect().height+1}})()")
        ok(r['act'] >= r['px'] - 1, 'salle : boutons à droite de PRIX, sans chevauchement', r)
        ok('En salle' in r['txt'] and r['st'], 'salle : statut « En salle » entier', r)
        ok(r['nm'], 'salle : nom du patient sur deux lignes, ligne assez haute (rien de coupé)', r)
        await pg.close()
        # Dossier (médecin, 1 440 px)
        pg = await ouvrir(b, S2, w=1440); ev = pg.evaluate
        await pg.goto(U + 'dossier/PTA1'); await pg.wait_for_timeout(2500)
        ok(await ev("document.getElementById('dos').classList.contains('agrandi')"), 'UX2 : centre déplié d\'emblée (sans choix gardé)')
        ok(await ev("(document.querySelector('.bn-loc')||{}).textContent") == 'Sein', 'UX2 : localisation dans l\'en-tête du dossier')
        ok(not await ev("!!document.querySelector('.bp .bn-al')"), 'UX2 : pas d\'allergie dans l\'en-tête sans « oui »')
        # UX1 : prescription de RT, « Lieu de la radiothérapie » dans sa case
        await ev("ouvrirRT('PTA1')"); await pg.wait_for_timeout(900)
        r = await ev("(()=>{const h=document.getElementById('rHop'), c=h.parentNode.getBoundingClientRect(), t=document.getElementById('rTech').getBoundingClientRect(), hr=h.getBoundingClientRect(); return {hr:hr.right, cr:c.right, tl:t.left, tt:t.top, ht:hr.top}})()")
        ok(r['hr'] <= r['cr'] + 1 and (r['tt'] != r['ht'] or r['hr'] <= r['tl']), 'prescription RT : le lieu ne chevauche plus « Technique »', r)
        await ev("fermerFenetre()"); await pg.wait_for_timeout(400)
        await ev("dosAgrandir()"); await pg.wait_for_timeout(400)
        ok(not await ev("document.getElementById('dos').classList.contains('agrandi')"), '⤢ ramène la colonne Documents')
        # UX1 : tableau des cures dans sa colonne en disposition trois colonnes
        for w in (1280, 1440, 1600):
            await pg.set_viewport_size({'width': w, 'height': 900}); await pg.wait_for_timeout(300)
            await ev(CHIMIO); await pg.wait_for_timeout(600)
            r = await ev("(()=>{const t=document.querySelector('#dos [data-zone=travail] table.t-lig'); return t ? [t.scrollWidth, t.parentNode.clientWidth] : null})()")
            ok(r and r[0] <= r[1] + 1, 'cures en trois colonnes à %d px : le tableau tient (%s)' % (w, r))
        await ev("dosAgrandir()"); await pg.wait_for_timeout(300)
        # UX1 : « Journal » du dossier → retour au dossier
        await ev("auditPatient('PTA1')"); await pg.wait_for_timeout(2000)
        ok(await ev("!!document.querySelector('.au-ret')"), 'Journal d\'audit ouvert depuis le dossier : bouton « Retour au dossier »')
        if await ev("!!document.querySelector('.au-ret')"):
            await pg.click('.au-ret'); await pg.wait_for_timeout(1500)
            ok((await ev("location.hash")).startswith('#dossier/PTA1'), 'retour au dossier du patient')
        # UX2 : tableau de bord
        await pg.set_viewport_size({'width': 1440, 'height': 900}); await pg.goto(U + 'accueil'); await pg.wait_for_timeout(2500)
        r = await ev("(()=>{const r=document.querySelector('.tb-rang.tb-r1'); if(!r) return null; const g=r.querySelector('.tb-g').getBoundingClientRect(), d=r.querySelector('.tb-d').getBoundingClientRect(); return {h:r.getBoundingClientRect().height, g:g.height, d:d.height}})()")
        ok(r and r['h'] >= 620 and abs(r['g'] - r['d']) < 2, 'tableau de bord : 1re rangée plus haute, gauche et droite de même hauteur', r)
        await pg.wait_for_timeout(800)
        await ev("actTout()"); await pg.wait_for_timeout(800)
        t = await ev("document.querySelector('#accAct').innerText")
        ok('RÉGLAGE ADMIN' not in t and 'Consultation ajoutée' in t, 'Activité récente : sans les réglages de l\'Administration', t)
        ok(await ev("document.querySelector('nav a[data-p=documents]').classList.contains('cache')"), 'menu « Documents » caché pour le médecin')
        ok(pg.errs == [], 'aucune erreur JavaScript (médecin)', pg.errs)
        await pg.close()
        # UX2 : la secrétaire garde le menu « Documents »
        ps = await ouvrir(b, S2, w=1440); await ps.add_init_script("window.__uid='SEC'"); await ps.goto(U + 'accueil'); await ps.wait_for_timeout(2500)
        ok(not await ps.evaluate("document.querySelector('nav a[data-p=documents]').classList.contains('cache')"), 'menu « Documents » visible pour la secrétaire')
        # UX1 : le message en bas (toast) se pose au-dessus de la barre du dossier (ici : RT sans le droit de la modifier)
        for w in (1440, 390):
            await ps.set_viewport_size({'width': w, 'height': 900}); await ps.goto(U + 'dossier/PTA1'); await ps.wait_for_timeout(2200)
            await ps.evaluate("ouvrirRT('PTA1')"); await ps.wait_for_timeout(300)
            r = await ps.evaluate("(()=>{const t=document.getElementById('toast'), b=document.querySelector('#dos > [data-zone=barre]').getBoundingClientRect(); return {tb:t.getBoundingClientRect().bottom, bt:b.top, vu:!t.classList.contains('cache'), txt:t.textContent}})()")
            ok(r['vu'] and r['tb'] <= r['bt'] + 1, 'toast au-dessus de la barre du dossier à %d px' % w, r)
        await ps.close()
        # Téléphone (390 px) : rien ne déborde
        pt = await ouvrir(b, S2, w=390, h=844)
        for h in ('accueil', 'dossier/PTA1', 'salle'):
            await pt.goto(U + h); await pt.wait_for_timeout(2000)
            sw = await pt.evaluate("document.documentElement.scrollWidth")
            ok(sw <= 390, '390 px : %s sans débordement (%s)' % (h, sw))
        ok(pt.errs == [], 'aucune erreur JavaScript (téléphone)', pt.errs)
        await b.close()
    print('\n%d réussis, %d échoués' % (ok_n, ko_n)); sys.exit(1 if ko_n else 0)
import sys
asyncio.run(main())
