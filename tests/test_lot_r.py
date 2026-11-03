import pathlib; __file__=str(pathlib.Path(__file__).resolve()); exec(open(pathlib.Path(__file__).parent/'base.py').read())
# Lot R (31/10/2026, demande de Dr Bentahila) : reçu et encaissement à la validation « Venu ». Fenêtre « Nouveau reçu » (patient, prestation, prix des
# Paramètres, remise en DH pour cette consultation, total, mode, « Réglé en totalité ») ; mode habituel du lieu (remplace « Les consultations sont payées ») ;
# non réglé : à encaisser (secrétaire, salle d'attente › Vus) ou à payer (virement de l'établissement, Bilan) ; hospitalisation en jours ouvrés ;
# consultation d'un jour de chimio avec la même fenêtre (la séance, elle, se valide sans fenêtre). Ordinateur 1 440 px, téléphone 390 px. Jeu fictif.
import re, html as H
ok_n = ko_n = 0
def ok(c, m, d=None):
    global ok_n, ko_n
    if c: ok_n += 1; print('  ✔ ' + m)
    else: ko_n += 1; print('  ✘ ' + m + ('' if d is None else ' ' + str(d)[:400]))
T = '2026-10-06'
def seed(mode_hgc):
    s = json.loads(json.dumps(S)); d = s[E + 'patients/PTA1']; rd = json.loads(d['rdvsJson'])
    rd += [{'id': 'rN1', 'type': 'Suivi', 'd': T, 'h': '09:00', 'st': 'prevu'}, {'id': 'rN2', 'type': 'Suivi', 'd': T, 'h': '09:30', 'st': 'prevu'},
           {'id': 'rH1', 'type': 'Hospitalisation', 'd': '2026-10-05', 'f': '2026-10-09', 'st': 'prevu'}]
    d['rdvsJson'] = json.dumps(rd)
    if mode_hgc: s[E + 'etablissements/HGC'] = dict(s[E + 'etablissements/HGC'], modeHab=mode_hgc)
    return s
def M_de(fs, pid='PTA1'): return json.loads(fs[E + 'patientsFinances/' + pid]['montantsJson'])
def En_de(fs, pid='PTA1'): return json.loads(fs[E + 'encaissements/' + pid]['data'])
num = lambda v: float(str(v or '0').replace(' ', '').replace('\xa0', '').replace(' ', '').replace(',', '.') or 0)
async def venu(pg, rid):
    await pg.evaluate(f"statutRdv('PTA1', '{rid}', 'fait')"); await pg.wait_for_timeout(1500)
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        print('Lieux d\'exercice')
        pg = await ouvrir(b, seed(None)); ev = pg.evaluate
        await pg.goto(f'http://localhost:{PORT}/v2.html#parametres/lieux'); await pg.wait_for_timeout(2500)
        t = await ev("document.getElementById('page').innerText")
        ok('Les consultations sont payées' not in t and 'Payé par l\'établissement (virement)' in t, 'liste des lieux : mode habituel affiché, plus « Les consultations sont payées »', t[:300])
        await ev("pfLieu('HGC')"); await pg.wait_for_timeout(700)
        r = await ev("[...document.querySelectorAll('#lPay option')].map(o => o.textContent + '=' + o.value).concat([document.getElementById('lPay').value, document.getElementById('fenetreCorps').innerText.indexOf('Les consultations sont payées')])")
        ok(r[:4] == ['Espèces=esp', 'Carte bancaire=carte', 'Chèque=chq', "Virement (payé par l'établissement)=vir"] and r[4] == 'vir' and r[5] < 0, 'fiche du lieu : « Mode de paiement habituel » (espèces, carte, chèque, virement) ; sans réglage = virement', r)
        await pg.select_option('#lPay', 'esp'); await pg.click('#fOk'); await pg.wait_for_timeout(900)
        e = await ev(f"window.__fs['{E}etablissements/HGC']")
        ok(e.get('modeHab') == 'esp' and 'paiement' not in e, 'enregistré : modeHab = esp (ancien champ « paiement » retiré)', e)
        ok(not pg.errs, 'aucune erreur JavaScript', pg.errs[:2]); await pg.close()

        print('Lieu payé par virement (ex. HCK) : à payer')
        pg = await ouvrir(b, seed('vir')); ev = pg.evaluate
        await pg.goto(f'http://localhost:{PORT}/v2.html#dossier/PTA1'); await pg.wait_for_timeout(3000)
        await venu(pg, 'rN1')
        r = await ev("[document.querySelector('#fenetreCorps h3').textContent, document.getElementById('pvPat').value, document.getElementById('pvPat').readOnly, document.getElementById('pvPrest').value, document.getElementById('pvPx').value, document.getElementById('pvPx').readOnly, document.getElementById('pvM').value, document.getElementById('pvMode').value, document.getElementById('pvRegle').checked, document.getElementById('fOk').textContent, document.getElementById('fOkR').classList.contains('cache'), [...document.querySelectorAll('#pvMode option')].map(o => o.value).join(',')]")
        px = num(r[4])
        ok(r[0] == 'Nouveau reçu' and r[1].startswith('PATIENT TEST REF 1') and r[2] and 'Consultation' in r[3], 'fenêtre « Nouveau reçu » : patient pré-rempli (non modifiable), prestation', r[:4])
        ok(px > 0 and r[5] and num(r[6]) == px, 'prix des Paramètres (tarif du lieu), non modifiable ; total = prix', r[4:7])
        ok(r[7] == 'vir' and not r[8] and r[9].endswith('Valider : venu') and r[10] and r[11] == 'esp,carte,chq,vir', 'mode habituel du lieu (virement) ; « Réglé en totalité » décoché ; pas de reçu à imprimer tant que ce n\'est pas réglé', r[7:])
        await pg.fill('#pvRem', '50'); await pg.wait_for_timeout(200)
        r = await ev("[document.getElementById('pvM').value, document.getElementById('pvEtat').innerText]")
        ok(num(r[0]) == px - 50 and 'à payer' in r[1], 'remise de 50 DH : total recalculé ; statut « à payer par l\'établissement »', r)
        await pg.click('#fOk'); await pg.wait_for_timeout(1500)
        fs = await ev("window.__fs"); o = M_de(fs)['rdv']['rN1']; en = En_de(fs)['rdv']['rN1']
        ok(o.get('brut') == px - 50 and o.get('rem') == 50 and o.get('px') == px and o.get('mode') == 'ap' and en.get('mode') == 'ap' and en.get('rem') == 50, 'enregistré : brut = prix − remise, remise, prix affiché, mode « ap » (montants et encaissements)', (o, en))
        rd = {v['id']: v for v in json.loads(fs[E + 'patients/PTA1']['rdvsJson'])}
        ok(rd['rN1'].get('st') == 'fait', 'rendez-vous « Venu »')
        await pg.goto(f'http://localhost:{PORT}/v2.html#bilan'); await pg.wait_for_timeout(2500)
        r = await ev("[...document.querySelectorAll('table.bilan tr')].filter(t => t.innerText.indexOf('06/10/2026') === 0 && /PATIENT TEST REF 1/.test(t.innerText)).map(t => { const l = t.querySelector('td:last-child label.bi-pc'); return [l && l.querySelector('span').textContent, l && l.title]; })")
        ok(any(x[0] == 'À payer' and 'virement' in x[1] for x in r), 'Bilan : « À payer » (cliquer quand le virement est reçu)', r)
        ok('à payer par les établissements' in await ev("document.getElementById('page').innerText"), 'Bilan : « À recevoir » détaillé (à payer par les établissements)')
        ok(not pg.errs, 'aucune erreur JavaScript', pg.errs[:2]); await pg.close()

        print('Lieu payé au cabinet (espèces) : à encaisser, puis encaissé')
        pg = await ouvrir(b, seed('esp')); ev = pg.evaluate
        await pg.goto(f'http://localhost:{PORT}/v2.html#dossier/PTA1'); await pg.wait_for_timeout(3000)
        await venu(pg, 'rN1')
        ok(await ev("document.getElementById('pvMode').value") == 'esp', 'mode habituel du lieu : espèces')
        await pg.fill('#pvRem', '20'); await pg.click('#fOk'); await pg.wait_for_timeout(1500)
        o = M_de(await ev("window.__fs"))['rdv']['rN1']
        ok(o.get('mode') == 'ae', 'non réglé, espèces : « à encaisser » (ae)', o)
        await venu(pg, 'rN2'); await pg.check('#pvRegle'); await pg.wait_for_timeout(200)
        ok(not await ev("document.getElementById('fOkR').classList.contains('cache')") and 'encaissé' in await ev("document.getElementById('pvEtat').innerText"), 'réglé coché : « Enregistrer et imprimer le reçu », statut encaissé')
        n0 = await ev("window.__win.length"); await pg.click('#fOkR'); await pg.wait_for_timeout(2000)
        o = M_de(await ev("window.__fs"))['rdv']['rN2']
        ok(o.get('mode') == 'esp' and 'rem' not in o and await ev("window.__win.length") == n0 + 1, 'réglé en totalité : mode espèces, reçu imprimé', o)
        # salle d'attente › Vus : « Encaisser » sur la consultation à encaisser
        await pg.goto(f'http://localhost:{PORT}/v2.html#salle'); await pg.wait_for_timeout(2500); await ev("window.saOnglet('vus')"); await pg.wait_for_timeout(400)
        r = await ev("[...document.querySelectorAll('#saL .sa-l')].map(l => l.innerText.replace(/\\s+/g, ' '))")
        l9 = [x for x in r if '09:00' in x]
        ok(l9 and 'Encaisser' in l9[0], 'salle d\'attente › Vus : « Encaisser » sur la consultation à encaisser', r)
        await pg.locator('#saL .sa-l:has-text("09:00") .actr >> text=Encaisser').first.click(); await pg.wait_for_timeout(1500)
        r = await ev("[document.querySelector('#fenetreCorps h3').textContent, document.getElementById('pvRegle').checked, document.getElementById('pvRem').value, document.getElementById('fOk').textContent]")
        ok(r[0] == 'Encaisser' and r[1] and num(r[2]) == 20 and r[3].endswith('Encaisser'), 'fenêtre « Encaisser » : réglé coché, remise du médecin gardée', r)
        n0 = await ev("window.__win.length"); await pg.click('#fOkR'); await pg.wait_for_timeout(2200)
        fs = await ev("window.__fs"); o = M_de(fs)['rdv']['rN1']
        h = await ev(f"window.__win.length > {n0} ? window.__win[window.__win.length - 1].w.document._h : ''"); t = H.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', h)))
        ok(o.get('mode') == 'esp' and o.get('rem') == 20, 'encaissé : mode espèces, remise gardée', o)
        ok('remise 20,00 DH' in t and 'Espèces' in t and 'REÇU' in t, 'facture (reçu) imprimée : prix, remise, total, mode', t[t.find('Encaissement'):][:160])
        await pg.goto(f'http://localhost:{PORT}/v2.html#bilan'); await pg.wait_for_timeout(2500)
        r = await ev("[...document.querySelectorAll('table.bilan tr')].filter(t => t.innerText.indexOf('06/10/2026') === 0 && /PATIENT TEST REF 1/.test(t.innerText)).map(t => { const l = t.querySelector('td:last-child label.bi-pc'); return l && l.classList.contains('ok') && l.querySelector('input').checked ? '✓ ' + l.querySelector('span').textContent : ''; })")
        ok(r.count('✓ Encaissé') == 2, 'Bilan : les deux consultations « ✓ Encaissé »', r)
        ok(not pg.errs, 'aucune erreur JavaScript', pg.errs[:2]); await pg.close()

        print('Hospitalisation (jours ouvrés)')
        pg = await ouvrir(b, seed('vir')); ev = pg.evaluate
        await pg.goto(f'http://localhost:{PORT}/v2.html#dossier/PTA1'); await pg.wait_for_timeout(3000)
        await venu(pg, 'rH1')
        r = await ev("[document.getElementById('pvNj') && document.getElementById('pvNj').value, document.getElementById('pvPx').value, document.getElementById('pvM').value, document.querySelector('label[for=pvPx]').textContent]")
        tj = num(r[1])
        ok(r[0] == '5' and r[3] == 'Prix par jour (DH)' and num(r[2]) == 5 * tj, 'hospitalisation du 05 au 09/10 : 5 jours ouvrés (hors samedi et dimanche), prix par jour, total', r)
        await pg.fill('#pvRem', '100'); await pg.click('#fOk'); await pg.wait_for_timeout(1500)
        o = M_de(await ev("window.__fs"))['rdv']['rH1']
        ok(o.get('tj') == tj and o.get('rem') == 100 and o.get('mode') == 'ap' and 'brut' not in o, 'enregistré : prix par jour, remise, à payer', o)
        await pg.goto(f'http://localhost:{PORT}/v2.html#bilan'); await pg.wait_for_timeout(2500)
        r = await ev("[...document.querySelectorAll('table.bilan tr')].filter(t => /Hospitalisation du 05\\/10\\/2026/.test(t.innerText)).map(t => [...t.querySelectorAll('td')].map(c => c.innerText))")
        ok(r and num(r[0][5].replace('DH', '')) == 5 * tj - 100, 'Bilan : brut = 5 × prix par jour − remise', r)
        ok(not pg.errs, 'aucune erreur JavaScript', pg.errs[:2]); await pg.close()

        print('Consultation d\'un jour de chimio : avec la fenêtre')
        s2 = seed('esp'); pg = await ouvrir(b, s2); ev = pg.evaluate
        lid = json.loads(s2[E + 'patients/PTA2']['lignesJson'])[0]['id']
        await pg.goto(f'http://localhost:{PORT}/v2.html#dossier/PTA2'); await pg.wait_for_timeout(3000)
        await ev(f"chVenuChimio('PTA2','{lid}',1,1)"); await pg.wait_for_timeout(1500)
        r = await ev("[document.querySelector('#fenetreCorps h3').textContent, document.getElementById('pvPx').value, document.getElementById('pvPx').readOnly, document.getElementById('fOk').textContent]")
        ok(r[0] == 'Nouveau reçu' and r[1] == '250' and r[2] and r[3].endswith('Valider : venu'), 'J1 : fenêtre « Nouveau reçu » au tarif de la consultation de chimio des Paramètres', r)
        await pg.click('#fOk'); await pg.wait_for_timeout(1500)
        M = M_de(await ev("window.__fs"), 'PTA2'); c = M['cures'][lid]['1']
        ok(c['consJ'].get('1') == 250 and c.get('consModeJ', {}).get('1') == 'ae', 'validée : 250 DH, « à encaisser » (non réglé)', c)
        await ev(f"chVenuChimio('PTA2','{lid}',1,8)"); await pg.wait_for_timeout(1500)
        ok(await ev("document.getElementById('pvPx').value") == '0' and not await ev("document.getElementById('pvPx').readOnly"), 'J8 : 0 DH proposé, modifiable')
        await ev("fermerFenetre()")
        await ev(f"chVenuChimio('PTA2','{lid}',1,1)"); await pg.wait_for_timeout(1500)
        ok(await ev("document.querySelector('#fenetreCorps h3').textContent") == 'Reçu de la consultation', '« Modifier le prix » : fenêtre du reçu (remise, mode, réglé)')
        await pg.fill('#pvRem', '50'); await pg.check('#pvRegle'); await pg.click('#fOk'); await pg.wait_for_timeout(1500)
        fs = await ev("window.__fs"); c = M_de(fs, 'PTA2')['cures'][lid]['1']; ec = En_de(fs, 'PTA2')['cons'][lid + '|1|1']
        ok(c['consRemJ'].get('1') == 50 and c['consModeJ'].get('1') == 'esp' and ec.get('rem') == 50 and ec.get('mode') == 'esp', 'remise et réglé : montants et encaissements', (c, ec))
        ok(not pg.errs, 'aucune erreur JavaScript', pg.errs[:2]); await pg.close()

        print('Téléphone')
        pg = await ouvrir(b, seed('esp'), w=390, h=844); ev = pg.evaluate
        await pg.goto(f'http://localhost:{PORT}/v2.html#dossier/PTA1'); await pg.wait_for_timeout(3000)
        await venu(pg, 'rN1')
        r = await ev("[document.documentElement.scrollWidth, document.getElementById('pvRegle').getBoundingClientRect().height, document.querySelector('.pv-regle').getBoundingClientRect().height, getComputedStyle(document.getElementById('pvRem')).fontSize]")
        ok(r[0] <= 390 and r[2] >= 40 and float(r[3][:-2]) >= 13, '390 px : fenêtre sans débordement, case « Réglé » ≥ 40 px, texte ≥ 13 px', r)
        ok(not pg.errs, 'aucune erreur JavaScript', pg.errs[:2]); await pg.close()
        await b.close()
    print(f'\n{ok_n} réussis, {ko_n} échoués')
asyncio.run(main())
