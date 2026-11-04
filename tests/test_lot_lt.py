import pathlib; __file__=str(pathlib.Path(__file__).resolve()); exec(open(pathlib.Path(__file__).parent/'base.py').read())
# Lot LT (04/11/2026, demande de Dr Bentahila) : lieu de traitement d'une ligne de chimio (L.hop), entre la recherche et Favoris / Réinitialiser ;
# séances comptées au lieu de la ligne, consultations au lieu du patient ; équipe d'une clinique : patients traités chez elle ; Paramètres : taux
# commun de la radiothérapie en tableau daté, séance de chimiothérapie aussi dans le modèle. Jeu fictif : deux cliniques (HGC, CIOC) et un cabinet
# (CAB). 1 440 et 390 px. Captures (facultatif) : CAPT=<dossier> python3 tests/test_lot_lt.py
import copy, os
ok_n = ko_n = 0
def ok(c, m, d=None):
    global ok_n, ko_n
    if c: ok_n += 1; print('  ✔ ' + m)
    else: ko_n += 1; print('  ✘ ' + m + ('' if d is None else ' ' + str(d)[:400]))
U = f'http://localhost:{PORT}/v2.html#'
CAPT = os.environ.get('CAPT')
async def cap(pg, nom, sel=None, plein=False):
    if not CAPT: return
    pathlib.Path(CAPT).mkdir(parents=True, exist_ok=True)
    if sel: await pg.locator(sel).first.screenshot(path=f'{CAPT}/{nom}.png')
    else: await pg.screenshot(path=f'{CAPT}/{nom}.png', full_page=plein)

def jeu():
    s = copy.deepcopy(S)
    s[E + 'etablissements/HGC'].update({'nom': 'Clinique de test A', 'modeHab': 'vir'})
    s[E + 'etablissements/CIOC'].update({'nom': 'Clinique de test C', 'modeHab': 'vir'})
    s[E + 'etablissements/CAB'] = {'code': 'CAB', 'nom': 'Cabinet de test', 'actif': True, 'modeHab': 'esp'}
    T = json.loads(s[E + 'finances/tarifs']['data'])
    T['etablissements']['CAB'] = {'activites': [copy.deepcopy(a) for a in T['etablissements']['HGC']['activites'] if a['type'] in ('annonce', 'suivi', 'controle', 'cchimio')]}
    T['tauxRT'] = {'retro': 60, 'impot': 10}
    T['seanceCommune'] = {'type': 'seance', 'libelle': 'Séance de chimiothérapie', 'historique': [{'depuis': '2000-01-01', 'brut': 1000, 'retro': 50, 'impot': 10}]}
    s[E + 'finances/tarifs']['data'] = json.dumps(T)
    # Cas 2 : patient du cabinet, chimio à HGC, radiothérapie à CIOC
    p = copy.deepcopy(s[E + 'patients/PTA1']); p['etablissementId'] = 'CAB'
    p['identite'] = dict(p['identite'], nom='PATIENT FICTIF CABINET', nomF='PATIENT FICTIF CABINET', prenom='Cab', cin='CAB1', numero='202609950')
    L = json.loads(p['lignesJson']); L[0]['hop'] = 'HGC'; p['lignesJson'] = json.dumps(L)
    acte = T['actesRT'][0]['nom'] if T.get('actesRT') else 'RT'
    p['rtsJson'] = json.dumps([{'id': 'rtC1', 'acte': acte, 'hop': 'CIOC', 'nb': 25, 'nbA': 1, 'ryt': '1', 'scan': '2026-08-20', 'cont': '2026-08-22', 'dosi': '2026-08-25', 'deb': '2026-08-27', 'fin': '2026-09-30'}])
    p['lieuxTraitement'] = ['CIOC', 'HGC']
    s[E + 'patients/PTC1'] = p
    f = copy.deepcopy(s[E + 'patientsFinances/PTA1']); f['etablissementId'] = 'CAB'; s[E + 'patientsFinances/PTC1'] = f
    # Patient du cabinet sans traitement à HGC (invisible pour l'infirmière de HGC)
    q = copy.deepcopy(s[E + 'patients/PTA1']); q['etablissementId'] = 'CAB'
    q['identite'] = dict(q['identite'], nom='PATIENT FICTIF AUTRE', nomF='PATIENT FICTIF AUTRE', prenom='Autre', cin='CAB2', numero='202609951')
    q['lignesJson'] = '[]'; q['planningJson'] = '{}'
    s[E + 'patients/PTC2'] = q
    s[E + 'membres/INFH'] = {'role': 'infirmiere', 'nom': 'Infirmière test HGC', 'email': 'infh@test.ma', 'actif': True, 'tousEtablissements': False, 'etablissements': ['HGC'],
        'droits': {'traitements': 'voir', 'radiotherapie': 'voir', 'administrer': True, 'planningChimio': True, 'consultations': False, 'rendezvous': False}}
    s['utilisateurs/INFH'] = {'prenom': 'Infirmière', 'nom': 'TEST'}
    s.setdefault(E + 'parametres/migrations', {})['lieuxTrait1104'] = '2026-11-04'
    for e in T['etablissements'].values():
        for a in e['activites']: a.pop('payeAuto', None)
    s[E + 'finances/tarifs']['data'] = json.dumps(T)
    return s

async def main():
    s = jeu()
    async with async_playwright() as p:
        b = await p.chromium.launch()
        print('Paramètres (ordinateur)')
        pg = await ouvrir(b, s, w=1440, h=900, t="2026-10-09T10:00:00"); ev = pg.evaluate
        await pg.goto(U + 'parametres/lieux'); await pg.wait_for_timeout(2500)
        t = await ev("document.getElementById('page').innerText")
        ok('CAB' in t and 'HGC' in t and 'CIOC' in t, 'Lieux d\'exercice : deux cliniques et le cabinet')
        await cap(pg, '01-lieux-exercice')
        await pg.goto(U + 'parametres/activites'); await pg.wait_for_timeout(2000)
        r = await ev("(() => { const c = [...document.querySelectorAll('#page section.carte')].find(x => /Actes de radiothérapie/.test(x.innerText)); const t = c && c.querySelector('table'); return t ? [...t.querySelectorAll('th')].map(h => h.innerText.trim()) : null; })()")
        ok(r == ["Lieu d'exercice", 'Tarif', 'Rétrocession %', 'Impôt %', 'Net (DH)', 'En vigueur depuis'], 'radiothérapie : taux commun en tableau, mêmes colonnes que la séance', r)
        r = await ev("(() => [...document.querySelectorAll('#page .pa-lieux table')].map(t => { const tr = [...t.querySelectorAll('tr')]; const x = (r) => [...r.children].map(c => Math.round(c.getBoundingClientRect().left)); return tr.length > 2 && tr.slice(1).every(r => JSON.stringify(x(r)) === JSON.stringify(x(tr[0]))) && /Tarif commun/.test(tr[1].innerText); }))()")
        ok(r == [True, True], 'séance et radiothérapie : tarif commun en 1re ligne du tableau des lieux, colonnes alignées', r)
        r = await ev("(() => { const t = document.getElementById('paTauxRT'); return t ? t.innerText.replace(/\\s+/g, ' ') : ''; })()")
        ok('selon le catalogue des actes' in r and '36 % de l\'acte' in r and 'Origine' in r, 'ligne « Lieux sans taux propres » : selon le catalogue, net 36 % de l\'acte, Origine', r)
        await cap(pg, '02-parametres-activites-page-entiere', plein=True)
        await ev("document.getElementById('paEffR').value = '2026-11-01'; paEffet('2026-11-01')"); await pg.wait_for_timeout(300)
        await pg.fill('#paTrR', '55'); await pg.press('#paTrR', 'Tab'); await pg.wait_for_timeout(400)
        r = await ev("document.getElementById('paTauxRT').innerText.replace(/\\s+/g, ' ')")
        ok('01/11/2026' in r and '40,5 % de l\'acte' in r, 'taux modifié avec une date d\'effet : « En vigueur depuis 01/11/2026 », net recalculé', r)
        await ev("paEnregistrer()"); await pg.wait_for_timeout(800)
        T = await ev("JSON.parse(window.__fs['espaces/cabinet-bentahila/finances/tarifs'].data).tauxRT")
        ok(T and T.get('retro') == 60 and len(T.get('historique') or []) == 2 and T['historique'][0]['retro'] == 60 and T['historique'][1] == {'depuis': '2026-11-01', 'retro': 55, 'impot': 10}, 'enregistré : 60 % à l\'origine (valeur du jour), 55 % à partir du 01/11/2026', T)
        await pg.locator('section.carte[data-fn="rt.tarifs"]').first.scroll_into_view_if_needed(); await ev("window.scrollBy(0, -90)"); await pg.wait_for_timeout(200)
        await cap(pg, '03-parametres-radiotherapie-date-effet')
        ok(not pg.errs, 'aucune erreur', pg.errs)
        await pg.close()

        print('Modèle des cabinets neufs (Administration)')
        sb = copy.deepcopy(s); sb[E[:-1]] = dict(sb.get(E[:-1], {}), bibliotheque=True)
        for k in [k for k in sb if k.startswith(E + 'etablissements/') or k.startswith(E + 'patients')]: del sb[k]
        Tb = json.loads(sb[E + 'finances/tarifs']['data']); Tb['etablissements'] = {}; Tb['repli'] = ''; sb[E + 'finances/tarifs']['data'] = json.dumps(Tb)
        pg = await ouvrir(b, sb, w=1440, h=900, t="2026-10-09T10:00:00"); ev = pg.evaluate
        await pg.goto(U + 'parametres/activites'); await pg.wait_for_timeout(2500)
        t = await ev("document.getElementById('page').innerText")
        ok('Séance de chimiothérapie' in t and 'lieux sans taux propres' in t and 'pas dans le modèle' in t, 'modèle : la séance de chimiothérapie (tarif commun) et la radiothérapie en tableau', t[:400])
        await cap(pg, '04-modele-cabinets-neufs', plein=True)
        ok(not pg.errs, 'aucune erreur', pg.errs)
        await pg.close()

        print('Prescription : cas 2 (patient du cabinet)')
        pg = await ouvrir(b, s, w=1440, h=900, t="2026-10-09T10:00:00"); ev = pg.evaluate
        await pg.goto(U + 'dossier/PTC1'); await pg.wait_for_timeout(2800)
        await ev("ongletDossier('PTC1','ch')"); await pg.wait_for_timeout(400)
        await ev("chNouvelleLigne('PTC1')"); await pg.wait_for_timeout(1200)
        r = await ev("(() => { const l = document.getElementById('nlLieu'), c = document.querySelector('#panneau .cascade'), q = document.getElementById('nlQ'), z = document.querySelector('.nl-lieu1'); if (!l || !c) return null; const bl = l.getBoundingClientRect(), bc = c.getBoundingClientRect(), bq = q.getBoundingClientRect(); return [l.value, [...l.options].map(o => o.textContent), bl.bottom <= bc.top, Math.round(bl.width) >= Math.round(bc.width) - 4, bq.top > bc.bottom, Math.round(bl.height)]; })()")
        ok(r and r[0] == 'CAB' and r[1][0].startswith('CAB') and '(lieu du patient)' in r[1][0] and len(r[1]) == 4, 'menu « Lieu de traitement » : tous les lieux, le lieu du patient (cabinet) en premier et choisi', r)
        ok(r and r[2] and r[3] and r[4] and r[5] >= 40, 'sur toute la ligne, en premier : au-dessus de Type de cancer… ; recherche, Favoris et Réinitialiser dessous ; ≥ 40 px', r)
        await cap(pg, '05-nouvelle-ligne-lieu-ordinateur', '#panneau')
        await pg.select_option('#nlLieu', 'HGC'); await pg.wait_for_timeout(200)
        await ev("(() => { const p = document.querySelector('#nlL .proto:not(.off)'); p.click(); })()"); await pg.wait_for_timeout(900)
        r = await ev("(() => { const l = document.getElementById('nlLieuB'), it = document.querySelector('#panneau .nl-int'); return l ? [l.value, l.getBoundingClientRect().bottom <= it.getBoundingClientRect().top] : null; })()")
        ok(r and r[0] == 'HGC' and r[1], 'après le choix du protocole : le lieu choisi, avant l\'intention (modifiable)', r)
        await cap(pg, '06-nouvelle-ligne-protocole-choisi', '#panneau')
        await ev("document.getElementById('fOk').click()"); await pg.wait_for_timeout(1500)
        d = await ev("JSON.parse(window.__fs['espaces/cabinet-bentahila/patients/PTC1'].lignesJson)")
        lt = await ev("window.__fs['espaces/cabinet-bentahila/patients/PTC1'].lieuxTraitement")
        ok(len(d) == 2 and d[1].get('hop') == 'HGC', 'ligne créée avec son lieu de traitement (HGC)', [x.get('hop') for x in d])
        ok(lt == ['CIOC', 'HGC'], 'lieux de traitement du dossier tenus à jour', lt)
        await ev("fermerFenetre()"); await pg.wait_for_timeout(500)
        await ev("ongletDossier('PTC1','ch')"); await pg.wait_for_timeout(500)
        t = await ev("[...document.querySelectorAll('.ch-lieu')].map(b => b.textContent.trim())")
        ok('Lieu : HGC' in t, 'ligne du dossier : bouton « Lieu : HGC »', t)
        await cap(pg, '07-ligne-du-dossier-lieu', '#cChimio')
        await ev("chLieu('PTC1', 1)"); await pg.wait_for_timeout(600)
        await cap(pg, '08-changer-lieu-ligne', '#fenetre')
        await pg.select_option('#chLieuS', 'CIOC'); await ev("document.getElementById('fOk').click()"); await pg.wait_for_timeout(1200)
        d = await ev("JSON.parse(window.__fs['espaces/cabinet-bentahila/patients/PTC1'].lignesJson)")
        ok(d[1].get('hop') == 'CIOC', 'lieu de la ligne changé (CIOC)', d[1].get('hop'))
        await ev("ouvrirRT('PTC1')"); await pg.wait_for_timeout(1000)
        r = await ev("(() => { const s = document.getElementById('rHop'); return s ? [s.value, [...s.options].map(o => o.textContent)] : null; })()")
        ok(r and r[0] == 'CAB' and r[1][1].startswith('CAB'), 'prescription de radiothérapie : lieu du patient en premier, choisi d\'office', r)
        await cap(pg, '09-prescription-rt-lieu', '#panneau')
        ok(not pg.errs, 'aucune erreur', pg.errs)
        await pg.close()

        print('Prescription : cas 1 (patient d\'une clinique)')
        pg = await ouvrir(b, s, w=1440, h=900, t="2026-10-09T10:00:00"); ev = pg.evaluate
        await pg.goto(U + 'dossier/PTA1'); await pg.wait_for_timeout(2800)
        await ev("ongletDossier('PTA1','ch')"); await ev("chNouvelleLigne('PTA1')"); await pg.wait_for_timeout(1200)
        r = await ev("(() => { const l = document.getElementById('nlLieu'); return l ? [l.value, l.options[0].textContent] : null; })()")
        ok(r and r[0] == 'HGC' and r[1].startswith('HGC'), 'patient de HGC : HGC proposée en premier', r)
        await cap(pg, '10-cas1-patient-clinique', '#panneau')
        await pg.close()

        print('Bilan')
        pg = await ouvrir(b, s, w=1440, h=900, t="2026-10-09T10:00:00"); ev = pg.evaluate
        await pg.goto(U + 'bilan'); await pg.wait_for_timeout(3000)
        await ev("biF('per', 'annee')"); await ev("biF('q', 'FICTIF CABINET')"); await pg.wait_for_timeout(800)
        lignes = await ev("[...document.querySelectorAll('#page tr')].map(r => r.innerText.replace(/\\s+/g, ' ').trim()).filter(t => /PATIENT FICTIF CABINET/.test(t))")
        sea = [l for l in lignes if 'Séance chimio' in l]; cc = [l for l in lignes if 'Consultation chimio' in l]; rt = [l for l in lignes if 'RT ' in l]
        ok(sea and all(' HGC ' in ' ' + l + ' ' for l in sea), 'bilan : séance de chimio du patient du cabinet rangée sous HGC', sea)
        ok(cc and all(' CAB ' in ' ' + l + ' ' for l in cc), 'bilan : consultation de chimio sous le cabinet', cc)
        ok(rt and all(' CIOC ' in ' ' + l + ' ' for l in rt), 'bilan : radiothérapie sous CIOC', rt)
        print('    ' + '\n    '.join(lignes))
        await pg.locator('#page tr', has_text='PATIENT FICTIF CABINET').first.scroll_into_view_if_needed(); await ev("window.scrollBy(0, -260)"); await pg.wait_for_timeout(200)
        await cap(pg, '11-bilan-patient-cabinet-tous-lieux')
        await ev("biF('hop', 'HGC')"); await pg.wait_for_timeout(600)
        await pg.locator('#page tr', has_text='Séance chimio').first.scroll_into_view_if_needed(); await ev("window.scrollBy(0, -300)"); await pg.wait_for_timeout(200)
        await cap(pg, '12-bilan-filtre-HGC-a-recevoir')
        await pg.locator('#page tr', has_text='Séance chimio').first.locator('label.bi-pc input').click(); await pg.wait_for_timeout(900)
        t = await ev("(document.querySelector('#page tr label.bi-pc') || {}).innerText || ''")
        ok('Payé' in t and await ev("!!document.querySelector('#page tr label.bi-pc.ok')"), 'séance de HGC cochée « Payé » à réception du virement', t)
        await pg.locator('#page tr', has_text='Séance chimio').first.scroll_into_view_if_needed(); await ev("window.scrollBy(0, -300)"); await pg.wait_for_timeout(200)
        await cap(pg, '12b-bilan-filtre-HGC-paye')
        await ev("biF('hop', 'CAB')"); await pg.wait_for_timeout(600)
        await pg.locator('#page tr', has_text='Consultation').first.scroll_into_view_if_needed(); await ev("window.scrollBy(0, -300)"); await pg.wait_for_timeout(200)
        await cap(pg, '13-bilan-filtre-cabinet')
        ok(not pg.errs, 'aucune erreur', pg.errs)
        await pg.close()

        print('Infirmière de HGC')
        pg = await ouvrir(b, s, w=1440, h=900, t="2026-10-09T10:00:00"); ev = pg.evaluate
        await pg.add_init_script("window.__uid = 'INFH'")
        await pg.goto(U + 'patients'); await pg.wait_for_timeout(3000)
        t = await ev("document.getElementById('page').innerText")
        ok('PATIENT FICTIF CABINET' in t and 'PATIENT FICTIF AUTRE' not in t, 'Patients : le patient du cabinet traité à HGC, pas celui sans traitement à HGC', t[:300])
        await cap(pg, '14-infirmiere-patients')
        await pg.goto(U + 'dossier/PTC1'); await pg.wait_for_timeout(2500)
        ok(not pg.errs, 'infirmière : dossier du patient du cabinet ouvert sans erreur', pg.errs)
        await cap(pg, '15-infirmiere-dossier')
        await pg.goto(U + 'salle'); await pg.wait_for_timeout(2500)
        await ev("saOnglet('avenir')"); await pg.wait_for_timeout(600)
        t = await ev("document.getElementById('page').innerText")
        ok('PATIENT FICTIF CABINET' in t and 'AUTRE' not in t, 'salle d\'attente : la séance de HGC du patient du cabinet', t[:300])
        await cap(pg, '16-infirmiere-salle-attente')
        await pg.goto(U + 'agenda'); await pg.wait_for_timeout(2500)
        await cap(pg, '17-infirmiere-agenda')
        ok(not pg.errs, 'aucune erreur', pg.errs)
        await pg.close()

        print('Téléphone (390 px)')
        pg = await ouvrir(b, s, w=390, h=844, t="2026-10-09T10:00:00"); ev = pg.evaluate
        await pg.goto(U + 'dossier/PTC1'); await pg.wait_for_timeout(2800)
        await ev("ongletDossier('PTC1','ch')"); await ev("chNouvelleLigne('PTC1')"); await pg.wait_for_timeout(1200)
        r = await ev("(() => { const l = document.getElementById('nlLieu'), q = document.getElementById('nlQ'); const W = document.documentElement.clientWidth; const bl = l.getBoundingClientRect(), bq = q.getBoundingClientRect(); const fs = [...document.querySelectorAll('#fenetreCorps *, #panneauCorps *')].filter(e => e.getClientRects().length && e.getBoundingClientRect().right > W + 1).map(e => e.tagName + '#' + e.id + '.' + e.className + ' ' + Math.round(e.getBoundingClientRect().right) + ' ' + (e.parentElement && e.parentElement.className)); return [Math.round(bq.width), Math.round(bl.width), Math.round(bl.height), fs, getComputedStyle(l).fontSize]; })()")
        ok(r[0] >= 330 and r[1] >= 330 and r[2] >= 40 and not r[3] and float(r[4][:-2]) >= 13, 'téléphone : lieu sur toute la largeur en premier, recherche dessous, sans débordement', r)
        await cap(pg, '18-nouvelle-ligne-lieu-telephone')
        await pg.goto(U + 'parametres/activites'); await pg.wait_for_timeout(2000)
        await pg.locator('section.carte[data-fn="rt.tarifs"]').first.scroll_into_view_if_needed(); await ev("window.scrollBy(0, -120)"); await pg.wait_for_timeout(300)
        await cap(pg, '19-parametres-radiotherapie-telephone')
        await pg.locator('section.carte.pa-seance').first.scroll_into_view_if_needed(); await pg.wait_for_timeout(300)
        await cap(pg, '20-parametres-seance-telephone')
        ok(not pg.errs, 'aucune erreur', pg.errs)
        await pg.close()
        await b.close()
    print(f'\n{ok_n} réussi(s), {ko_n} échec(s)')
    raise SystemExit(1 if ko_n else 0)
asyncio.run(main())
