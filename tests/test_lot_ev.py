import pathlib; __file__=str(pathlib.Path(__file__).resolve()); exec(open(pathlib.Path(__file__).parent/'base.py').read()); exec(open(pathlib.Path(__file__).parent/'demo_seed.py').read())
# Lot EV (06/11/2026, demandes de Dr Bentahila) : (1) images des états vides redessinées (donnees/illustrations.js : 12 images + accueil des Paramètres) ;
# (2) EV.1 : « Rien à valider » et son image restent affichés quand la carte n'a plus que « N alertes vues » ; (3) protocoles de traitement systémique :
# plus aucun nom de médecin sous la fiche ni dans le formulaire (« Validé par … – source : … · modifié par … » retiré), source toujours affichée.
# Jeu fictif ; 1 440 et 390 px.
ok_n = ko_n = 0
def ok(c, m, d=None):
    global ok_n, ko_n
    if c: ok_n += 1; print('  ✔ ' + m)
    else: ko_n += 1; print('  ✘ ' + m + ('' if d is None else ' ' + str(d)[:400]))
U = f'http://localhost:{PORT}/v2.html#'
S2, PIDS = avec_demo(S, E); P1 = PIDS[0]
# un seul patient (le 1er fictif), jour du test avant sa 3e cure : rien d'autre à valider que l'alerte de poids
for k in [k for k in S2 if k.startswith(E + 'patients/') and k.split('/')[-1] != P1]: del S2[k]
L = json.loads(S2[E + 'patients/' + P1]['lignesJson']); L[0]['cures'][0]['poids'] = '70'; L[0]['cures'][1]['poids'] = '60'; S2[E + 'patients/' + P1]['lignesJson'] = json.dumps(L)
# Protocole validé et modifié par un médecin nommé (nom fictif)
K = E + 'protocoles/lib_0'; B0 = json.loads(S2[K]['data']); PR = B0[0]
PR.update({'st': 'ok', 'version': 2, 'src': 'ESSAI-TEMOIN 2012', 'majParNom': 'Dr Témoin', 'majPar': 'UIDRITA', 'majLe': '2026-10-18T10:00:00Z',
           'valide': {'par': 'UIDRITA', 'parNom': 'Dr Témoin', 'le': '2026-10-18T10:00:00Z', 'version': 2}})
S2[K] = dict(S2[K], data=json.dumps(B0))
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await ouvrir(b, S2, t="2026-09-20T10:00:00"); ev = pg.evaluate
        await pg.goto(U + 'accueil'); await pg.wait_for_timeout(3500)
        print('Images')
        r = await ev("import('/js/donnees/illustrations.js').then(m => [Object.keys(m.ILL_VIDE).sort().join(), Object.values(m.ILL_VIDE).every(s => s.startsWith('<svg class=\"ev-ill\" viewBox=\"0 0 260 170\"') && s.endsWith('</svg>')), m.ILL_PARAM.startsWith('<svg class=\"cf-acc-ill\"')])")
        ok(r[0] == 'agenda,agendaOk,chimio,consult,document,dossier,fete,notif,patients,rcp,rt,salle,taches' and r[1] and r[2], '13 images des états vides et celle des Paramètres, même format (260 × 170)', r)
        print('EV.1 : « Rien à valider » avec seulement des alertes vues')
        carte = "document.querySelector('section.carte.afaire')"
        alerte = "[...document.querySelectorAll('.af-l')].filter(l => /Perte de poids/.test(l.innerText))"
        ok(await ev(alerte + ".length") == 1, 'au départ : une alerte clinique à voir')
        await ev(alerte + "[0].querySelector('.af-vu').click()"); await pg.wait_for_timeout(1200)
        r = await ev("(() => { const c = " + carte + "; return [c.querySelectorAll('.af-l').length, !!c.querySelector('.ev-vide svg.ev-ill'), c.innerText, !!c.querySelector('button.af-vues')]; })()")
        if r[0] == 0:
            ok(r[1] and 'Rien à valider' in r[2] and r[3], 'plus rien à valider : image et « Rien à valider », avec « 1 alerte vue » dessous', r[2][:200])
            ok(await ev("(() => { const c = " + carte + ", i = c.querySelector('.ev-vide').getBoundingClientRect(), v = c.querySelector('button.af-vues').getBoundingClientRect(); return v.top >= i.bottom - 2; })()"), 'l\'image est au-dessus de « 1 alerte vue »')
        else:
            ok(False, 'jeu de test : il reste des lignes à valider, EV.1 non vérifiable', r[2][:300])
        print('Accueil des Paramètres')
        await pg.goto(U + 'parametres'); await pg.wait_for_timeout(1500)
        ok(await ev("(() => { const s = document.querySelector('svg.cf-acc-ill'); return !!s && !!s.querySelector('g[transform^=translate]') && s.getBoundingClientRect().width >= 150; })()"), 'nouvelle image (avec personnage) en haut des Paramètres')
        print('Protocoles : aucun nom de médecin')
        await pg.goto(U + 'protocoles'); await pg.wait_for_timeout(1500)
        await ev(f"prOuvrir('{PR['id']}')"); await pg.wait_for_timeout(800)
        t = await pg.inner_text('#fenetreCorps')
        ok('Témoin' not in t and 'Validé par' not in t and 'modifié par' not in t, 'fiche : plus de « Validé par … · modifié par … »', t[:400])
        ok('ESSAI-TEMOIN 2012' in t, 'fiche : la source reste affichée (Source)')
        bulle = await ev("[...document.querySelectorAll('#fenetreCorps .badge.b-ch, #page .badge.b-ch')].map(b => b.title).join(' | ')")
        ok('Témoin' not in bulle and ' par ' not in bulle, 'bulle du badge « Validé » : sans nom', bulle[:200])
        await ev(f"prModifier('{PR['id']}')"); await pg.wait_for_timeout(800)
        t = await pg.inner_text('#fenetreCorps')
        ok('Témoin' not in t and 'Validé par' not in t and 'modifié par' not in t, 'formulaire de modification : aucun nom non plus', t[:300])
        ok(not pg.errs, 'aucune erreur JavaScript', pg.errs[:2]); await pg.close()
        print('Téléphone (390 px)')
        pg = await ouvrir(b, S2, w=390, h=820); ev = pg.evaluate
        await pg.goto(U + 'parametres'); await pg.wait_for_timeout(2500)
        ok(await ev("document.documentElement.scrollWidth <= 392") and await ev("(() => { const s = document.querySelector('svg.cf-acc-ill'); return !!s && s.getBoundingClientRect().width <= 390; })()"), 'Paramètres : image sans débordement')
        await pg.goto(U + 'taches'); await pg.wait_for_timeout(1800)
        ok(await ev("document.documentElement.scrollWidth <= 392"), 'Tâches : sans débordement')
        ok(not pg.errs, 'aucune erreur JavaScript (téléphone)', pg.errs[:2])
        await pg.close(); await b.close()
    print(f'\n{ok_n} réussis, {ko_n} échoués')
asyncio.run(main())
