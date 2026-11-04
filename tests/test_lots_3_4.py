import pathlib; __file__=str(pathlib.Path(__file__).resolve()); exec(open(pathlib.Path(__file__).parent/'base.py').read())
# Lots 3 et 4 (31/10/2026, demandes de Dr Bentahila, document « Onco360 — Demandes à faire ») : dossier patient (boutons d'ajout à gauche, barre du bas
# ouverte au centre, Doc., états vides, ordre des radiothérapies, notes seulement, résumé, « modifiée le », ligne de chimio, impression, téléphone) et
# tableau de bord (disposition en rangées, Actions rapides, Activité récente, Derniers documents). Ordinateur 1 440 px, téléphone 390 px. Jeu fictif.
ok_n = ko_n = 0
def ok(c, m, d=None):
    global ok_n, ko_n
    if c: ok_n += 1; print('  ✔ ' + m)
    else: ko_n += 1; print('  ✘ ' + m + ('' if d is None else ' ' + str(d)[:400]))
s = json.loads(json.dumps(S))
pid = [k.split('/')[-1] for k, v in s.items() if k.startswith(E + 'patients/') and len(v.get('lignesJson') or '') > 50][0]
VIDE = [k.split('/')[-1] for k, v in s.items() if k.startswith(E + 'patients/') and k.count('/') == 3 and not json.loads(v.get('rtsJson') or '[]') and not json.loads(v.get('lignesJson') or '[]')][0]
# 3.5 : deux radiothérapies (la plus ancienne créée d'abord)
PRT = 'PTA3'; rts = json.loads(s[E + 'patients/' + PRT]['rtsJson']); rts.insert(0, dict(rts[0], id='rtAncienne', acte='Sein (ancienne)', cree='2025-03-01')); s[E + 'patients/' + PRT]['rtsJson'] = json.dumps(rts)
# 3.6 / 3.8 : deux consultations, la 2e modifiée deux fois
etab = s[E + 'patients/' + pid]['etablissementId']
for i in (1, 2): s[E + 'consultations/C%d' % i] = {'patientId': pid, 'etablissementId': etab, 'd': '2026-10-0%d' % i, 'titre': 'Consultation', 'note': 'Note fictive %d' % i, 'lignes': [], 'o': 1759300000000 + i, 'creePar': 'UIDRITA', 'creeParNom': 'Dr Rita TEST'}
s[E + 'consultations/C2']['modifs'] = [{'le': '2026-10-03T10:00:00Z', 'par': 'UIDX', 'parNom': 'Dr Rita TEST'}, {'le': '2026-10-05T10:00:00Z', 'par': 'UIDX', 'parNom': 'Dr Rita TEST'}]
# 4.3 : sept actions dans l'historique ; 4.4 : six documents déposés
for i in range(7): s[E + 'historique/H%d' % i] = {'parUid': 'UIDRITA', 'parNom': 'Dr TEST', 'le': '2026-10-0%dT0%d:00:00Z' % (1 + i % 5, i), 'patientId': pid, 'patient': 'PATIENT TEST REF 1', 'quoi': ['Patient créé', 'Consultation ajoutée : Suivi', 'Ordonnance (Médic.)', 'Document ajouté (Scanner)', 'Prix de la consultation du 01/10/2026 : 500 DH', 'Rendez-vous ajouté', 'Inscrit(e) en RCP du 08/10/2026'][i]}
for i in range(6): s[E + 'fichiers/F%d' % i] = {'patientId': pid, 'etablissementId': etab, 'titre': 'Document %d' % i, 'd': '2026-10-01', 'type': 'Imagerie', 'nom': 'doc%d.pdf' % i, 'taille': 1000, 'mime': 'application/pdf', 'chemin': 'x', 'o': 1759300000000 + i * 1000, 'creePar': 'UIDRITA', 'creeParNom': 'Dr TEST'}
# modifier un rendez-vous : un patient qui en a un
RPID, RRID = next((k.split('/')[-1], json.loads(v['rdvsJson'])[0]['id']) for k, v in s.items() if k.startswith(E + 'patients/') and k.count('/') == 3 and json.loads(v.get('rdvsJson') or '[]') and json.loads(v['rdvsJson'])[0].get('id'))
VIS = "(e) => !!e && e.getClientRects().length > 0 && getComputedStyle(e).visibility !== 'hidden'"
R = "(e) => { const r = e.getBoundingClientRect(); return [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]; }"
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        print('Lot 3 – dossier patient (1 440 px)')
        pg = await ouvrir(b, s, w=1440, h=900); ev = pg.evaluate; await pg.add_init_script("localStorage.setItem('onco360.dossierAgrandi','false')")  # UX2 : dossier en trois colonnes pour ces vérifications
        await pg.goto(f'http://localhost:{PORT}/v2.html#dossier/{pid}'); await pg.wait_for_timeout(2600)
        # 3.1 boutons d'ajout à gauche
        r = {}
        for k in ('co', 'ch', 'rt', 'doc'):
            await ev(f"ongletDossier('{pid}','{k}')"); await pg.wait_for_timeout(300)
            r[k] = await ev(f"(() => {{ const p = document.getElementById('op-{k}'), b = [...p.querySelectorAll('button')].find(e => (" + VIS + ")(e) && /^Nouvelle|^Ajouter/.test(e.textContent.trim())); if (!b) return null; const P = p.getBoundingClientRect(), B = b.getBoundingClientRect(); return [b.textContent.trim(), Math.round(B.left - P.left) <= 30]; })()")
        ok(r == {'co': ['Nouvelle consultation', True], 'ch': ['Nouvelle ligne de traitement', True], 'rt': ['Nouvelle radiothérapie', True], 'doc': ['Ajouter un document', True]}, '3.1 : boutons d\'ajout à gauche dans les quatre onglets, noms du 02/11 (UX11 C13, UX12 R15)', r)
        await ev(f"ongletDossier('{pid}','rt')"); await pg.wait_for_timeout(200)
        ok(await ev("(() => { const a = document.querySelector('#op-rt a.mp-lien'); return !!a && !!a.closest('.mpts .cache'); })()"), '3.1 : « Référentiel › » sous « ⋯ » à droite')
        await ev(f"ongletDossier('{pid}','doc')"); await pg.wait_for_timeout(200)
        ok(await ev("(() => { const f = document.querySelector('#op-doc .fi-barre'); const v = [...f.children].filter(e => e.getClientRects().length); return v.length >= 3 && v[0].tagName === 'BUTTON' && v[1].classList.contains('recherche') && v[2].tagName === 'SELECT' && v[0].getBoundingClientRect().left < v[1].getBoundingClientRect().left; })()"), '3.1 : Documents : « + Ajouter un document », puis la recherche, puis les types')
        # 3.9 ligne de chimio
        await ev(f"ongletDossier('{pid}','ch')"); await pg.wait_for_timeout(300)
        c = await ev("(() => { const a = document.querySelector('#op-ch .acc-c > .actr'); if (!a) return null; const b = a.querySelector('button').getBoundingClientRect(), m = a.querySelector('.m3 > summary').getBoundingClientRect(); return [!a.querySelector('.aide-b'), Math.round(m.top - b.top), Math.round(m.bottom - b.bottom)]; })()")
        ok(c and c[0] and abs(c[1]) <= 1 and abs(c[2]) <= 1, '3.9 : ligne de chimio : plus de « ? », « ⋯ » aligné sur les boutons', c)
        # 3.6 notes seulement ; 3.8 modifiée le
        await ev(f"ongletDossier('{pid}','co')"); await pg.wait_for_timeout(600)
        sig = await ev("[...document.querySelectorAll('#op-co .cs-sig')].map(e => e.textContent).join('|')")
        ok('modifiée le 05/10/2026' in sig and '03/10' not in sig and ' et le ' not in sig, '3.8 : « modifiée le … » : seulement la dernière date', sig)
        await ev(f"csNotesSeules('{pid}')"); await pg.wait_for_timeout(500)
        n = await ev("[...document.querySelectorAll('#op-co .cs-t .in')].map(e => e.textContent)")
        ok(n and all(x == 'Dr Rita TEST' for x in n), '3.6 : « Notes seulement » : « Dr Prénom Nom », plus d\'initiales', n)
        await ev(f"csNotesSeules('{pid}')"); await pg.wait_for_timeout(300)
        # 3.7 résumé et note
        r = await ev("(() => { const z = document.getElementById('nTxt'); z.value = Array(30).fill('Ligne de résumé assez longue pour passer à la ligne suivante.').join('\\n'); z.dispatchEvent(new Event('input', { bubbles: true })); const cs = getComputedStyle(z), n = document.querySelector('#op-co textarea.cs-note'), cn = n ? getComputedStyle(n) : null; return [z.scrollHeight <= z.clientHeight + 2, parseFloat(cs.paddingLeft) >= 12, cs.borderTopColor, cn ? cn.borderTopWidth : null, cn ? parseFloat(cn.paddingLeft) >= 10 : null]; })()")
        ok(r[0] and r[1] and r[3] == '0px' and r[4], '3.7 : résumé de toute sa hauteur (sans défilement), texte décollé du bord ; note de consultation sans trait autour', r)
        # 3.2 barre du bas : au centre (centre et colonne de droite), pas de fenêtre
        for sel, lib in (('.br-g .pr button[onclick^="csPrescrire"]', 'Médicaments'), ('.br-g button[onclick^="ouvrirRdv"]', 'Nouveau rendez-vous'), ('.br-g button[onclick^="taNouvelle"]', 'tâche'), ('.br-g button[onclick^="rcpInscrire"]', 'RCP')):
            await ev("fermerFenetre()"); await pg.wait_for_timeout(200)
            await pg.click(sel); await pg.wait_for_timeout(900)
            r = await ev("(() => { const f = document.getElementById('fenetre'), b = document.getElementById('fenetreCorps').getBoundingClientRect(), t = document.querySelector('#dos > [data-zone=travail]').getBoundingClientRect(), d = document.querySelector('#dos > [data-zone=documents]').getBoundingClientRect(), p = document.querySelector('#dos > [data-zone=patient]').getBoundingClientRect();"
                         " const el = document.elementFromPoint(p.left + p.width / 2, p.top + p.height / 2); return [f.classList.contains('centre') && !f.classList.contains('cache'), Math.abs(b.left - t.left) <= 2 && Math.abs(b.right - d.right) <= 2 && (() => { const ob = document.querySelector('#dos > [data-zone=travail] .o-barre'); return ob ? Math.abs(b.top - ob.getBoundingClientRect().bottom - 8) <= 2 : Math.abs(b.top - t.top) <= 2; })(), !!el && !!el.closest('[data-zone=patient]'), document.getElementById('fenetreCorps').textContent.slice(0, 80)]; })()")
            ok(r[0] and r[1] and r[2] and lib.lower() in r[3].lower(), '3.2 : ' + lib + ' : à la place du centre et de la colonne de droite, sous la barre des onglets (lot DM) ; la colonne Patient reste visible', r)
        await ev("fermerFenetre()"); await pg.wait_for_timeout(200)
        ok(await ev("!document.getElementById('fenetre').classList.contains('centre')"), '3.2 : fermé : plus rien au centre')
        await ev(f"ongletDossier('{pid}','ch')"); await pg.wait_for_timeout(200)
        await ev("document.querySelector('#op-ch .acc-c .actr button').click()"); await pg.wait_for_timeout(600)
        ok(await ev("!document.getElementById('fenetre').classList.contains('centre')"), '3.2 : seulement la barre du bas (le reste du dossier : comme avant)')
        await ev("fermerFenetre()"); await pg.wait_for_timeout(200)
        # 3.3 Doc.
        await pg.click('.br-g .pr button[onclick*="\'doc\'"]'); await pg.wait_for_timeout(1200)
        r = await ev("(() => { const t = document.querySelector('#dcListe tr:not(.dc-sep) td.act'); if (!t) return null; return [...t.children].filter(e => e.getClientRects().length).map(e => e.tagName === 'DETAILS' ? '⋯' : e.classList.contains('etoile') ? '★' : e.textContent.trim()); })()")
        ok(r and r[-2:] == ['Remettre', '⋯'] and 'Ouvrir' not in r, '3.3 : Doc. : l\'étoile, « Remettre » et « ⋯ » (Ouvrir, Modifier, Supprimer dessous)', r)
        await ev("fermerFenetre()"); await pg.wait_for_timeout(200)
        # 3.10 impression
        await ev(f"dosRubrique('{pid}','avenir')"); await pg.wait_for_timeout(500)
        await ev("[...document.querySelectorAll('#panneauCorps .boutons button')].find(b => /Imprimer/.test(b.textContent)).click()"); await pg.wait_for_timeout(600)
        w = await ev("window.__win.length ? window.__win[window.__win.length - 1].w.document._h : ''")
        ok('Rendez-vous et tâches à venir' in w and '<table>' in w, '3.10 : « Rendez-vous et tâches à venir » imprimable (ouvert au centre)', w[:120])
        await ev("fermerFenetre()"); await pg.wait_for_timeout(200)
        m = await ev("[...document.querySelectorAll('#dos .mpts .cache button')].map(b => b.textContent).filter(t => /Imprimer le rendez-vous/.test(t)).length")
        rid = await ev(f"(JSON.parse(window.__fs['espaces/cabinet-bentahila/patients/{pid}'].rdvsJson || '[]')[0] || {{}}).id")
        ok(m > 0, '3.10 : « Imprimer le rendez-vous » dans le « ⋯ » des rendez-vous', m)
        if rid:
            await ev(f"imprimerRdv('{pid}','{rid}')"); await pg.wait_for_timeout(500)
            w = await ev("window.__win[window.__win.length - 1].w.document._h")
            ok('PATIENT TEST REF 1' in w and 'size:A5' in w and 'Imprimé le' in w, '3.10 : un rendez-vous imprimé (A5, feuille d\'IG2)', w[:120])
        # 3.4 états vides
        await pg.goto(f'http://localhost:{PORT}/v2.html#dossier/{VIDE}'); await pg.wait_for_timeout(2400)
        v = {}
        for k in ('co', 'ch', 'rt'):
            await ev(f"ongletDossier('{VIDE}','{k}')"); await pg.wait_for_timeout(300)
            v[k] = await ev(f"(() => {{ const z = document.querySelector('#op-{k} .ev-vide'); return z ? [!!z.querySelector('svg.ev-ill'), z.querySelector('h4').textContent] : null; }})()")
        ok(all(v.values()) and all(x[0] for x in v.values()), '3.4 : aucune consultation, chimio, radiothérapie : dessin et phrase', v)
        # 3.5 ordre des radiothérapies
        await pg.goto(f'http://localhost:{PORT}/v2.html#dossier/{PRT}'); await pg.wait_for_timeout(2400); await ev(f"ongletDossier('{PRT}','rt')"); await pg.wait_for_timeout(300)
        o = await ev("[...document.querySelectorAll('#op-rt .acc, #op-rt .rt-b, #op-rt [data-rt]')].map(e => e.textContent.replace(/\\s+/g, ' ').trim().slice(0, 40))")
        t = await ev("document.getElementById('op-rt').innerText")
        ok(t.find('Sein (ancienne)') >= 0 and t.find('Sein (ancienne)') < t.find('Cavum'), '3.5 : radiothérapies : la plus ancienne en haut, la plus récente en bas', o[:3])
        ok(not pg.errs, 'aucune erreur JavaScript', pg.errs[:2]); await pg.close()
        print('Lot 3 – téléphone (390 px)')
        pg = await ouvrir(b, s, w=390, h=844); ev = pg.evaluate
        await pg.goto(f'http://localhost:{PORT}/v2.html#dossier/{pid}'); await pg.wait_for_timeout(2600)
        r = await ev("(() => { const t = [...document.querySelectorAll('.dos-trav .o-barre [role=tab]')].filter(e => e.getClientRects().length), o = document.querySelector('.dos-trav .o-barre'); return [t.length, new Set(t.map(e => Math.round(e.getBoundingClientRect().top))).size, o.scrollWidth <= o.clientWidth + 1, Math.round(innerWidth - t[t.length - 1].getBoundingClientRect().right), getComputedStyle(document.querySelector('.dos-fab')).borderRadius]; })()")
        ok(r[0] == 5 and r[1] == 1 and r[2] and r[3] >= 8 and r[4] == '8px', '3.11 : téléphone : cinq onglets sur une ligne sans défilement, « Docs » décollé du bord ; « + Prescrire » rectangulaire', r)
        ok(await ev("document.documentElement.scrollWidth") <= 390, 'rien ne déborde')
        ok(not pg.errs, 'aucune erreur JavaScript', pg.errs[:2]); await pg.close()
        # ───── Lot 4 ─────
        print('Lot 4 – tableau de bord (1 440 px)')
        pg = await ouvrir(b, s, w=1440, h=900); ev = pg.evaluate
        await pg.goto(f'http://localhost:{PORT}/v2.html#accueil'); await pg.wait_for_timeout(2800)
        r = await ev("[...document.querySelectorAll('.tb-rang')].map(g => { const v = (c) => [...g.querySelectorAll(c + ' .tb-c')].filter(e => e.getClientRects().length); const G = v('.tb-g'), Dd = v('.tb-d'), b = (l) => Math.round(Math.max(...l.map(e => e.getBoundingClientRect().bottom))), t = (l) => Math.round(Math.min(...l.map(e => e.getBoundingClientRect().top)));"
                     " return [G.map(e => e.dataset.carte), Dd.map(e => e.dataset.carte), Math.abs(t(G) - t(Dd)) <= 1 && Math.abs(b(G) - b(Dd)) <= 1]; })")
        ok(len(r) >= 2 and r[0][0] == ['jour'] and r[0][1][:2] == ['actions', 'afaire'] and r[1][0] == ['sept'] and r[1][1][:2] == ['activite', 'documents'] and r[0][2] and r[1][2], '4.1 : Aujourd\'hui | Actions rapides, À valider ; Les 7 prochains jours | Activité récente, Derniers documents ; colonnes de même hauteur', r)
        o = await ev("(() => { const h = (t) => [...document.querySelectorAll('#page section h3')].find(e => e.textContent.indexOf(t) >= 0); const a = h('Conflits'), s2 = h('Statistiques'), r = [...document.querySelectorAll('.tb-rang')].pop(); return [!!a && !!s2 && a.getBoundingClientRect().top > r.getBoundingClientRect().bottom && s2.getBoundingClientRect().top > a.getBoundingClientRect().top, a ? Math.round(a.closest('section').getBoundingClientRect().width) : 0]; })()")
        ok(o[0] and o[1] > 1000, '4.1 : puis Conflits sur toute la largeur, puis Statistiques', o)
        fx = await ev("(() => { const z = document.querySelector('[data-carte=afaire] > section'); return [getComputedStyle(z).overflowY, z.scrollHeight > z.clientHeight]; })()")
        ok(fx[0] == 'visible' and not fx[1], '4.1 (IG4, 02/11/2026) : « À valider » sans défilement dans la carte (5 lignes, puis « Voir les N »)', fx)
        a = await ev("[...document.querySelectorAll('.ac-r .ac-b')].map(e => e.textContent.trim())")
        ok(a == ['+ Consultation', 'Ordonnances', '+ Document', 'Feuille de soins', '+ Radiothérapie', '+ Chimiothérapie'], '4.2 : Actions rapides (et « Feuille de soins », lot 9)', a)
        act = await ev("[...document.querySelectorAll('#accAct .act-i b')].map(e => e.textContent)")
        ok(len(act) == 5 and act[0] == 'Prix de la consultation du 01/10/2026 : 500 DH', '4.3 : Activité récente : les 5 dernières actions, la plus récente en haut', act)
        await ev("actTout()"); await pg.wait_for_timeout(500)
        n = await ev("document.querySelectorAll('#accAct .act-i').length"); ok(n >= 7, '4.3 : « Voir tout » : la suite', n)
        doc = await ev("[...document.querySelectorAll('#accDocs .act-i b')].map(e => e.textContent)")
        ok(doc == ['Document 5', 'Document 4', 'Document 3', 'Document 2', 'Document 1'], '4.4 : Derniers documents : les 5 derniers, du plus récent au plus ancien', doc)
        await ev("docsTout()"); await pg.wait_for_timeout(500)
        ok(await ev("document.querySelectorAll('#accDocs .act-i').length") == 6, '4.4 : « Voir tout »')
        # 4.2 : Ordonnances → patient puis type → le dossier, au centre
        await ev("actionRapide('ordo')"); await pg.wait_for_timeout(500)
        ok(await ev("document.getElementById('fenetre').classList.contains('pleine')"), '4.2 : le patient se choisit en haut d\'une page')
        await pg.fill('#rq', 'test ref 1'); await pg.wait_for_timeout(300); await ev("document.querySelector('#rqL [data-id]').click()"); await pg.wait_for_timeout(200)
        await ev("document.querySelector('.ac-t [data-t=medic]').click()"); await pg.wait_for_timeout(3200)
        r = await ev("[location.hash, document.getElementById('fenetre').classList.contains('centre'), (document.querySelector('#fenetreCorps h3') || {}).textContent || '']")
        ok(r[0].startswith('#dossier/') and r[1] and 'Médicaments' in r[2], '4.2 : Ordonnances › Médic. : dans le dossier du patient, au centre (rangé dans son dossier)', r)
        await ev("fermerFenetre()"); await pg.goto(f'http://localhost:{PORT}/v2.html#accueil'); await pg.wait_for_timeout(1500)
        await ev("actionRapide('consult')"); await pg.wait_for_timeout(500)
        await pg.fill('#rq', 'test ref 1'); await pg.wait_for_timeout(300); await ev("document.querySelector('#rqL [data-id]').click()"); await pg.wait_for_timeout(3200)
        r = await ev("[location.hash, (document.querySelector('#fenetreCorps h3') || {}).textContent || '']")
        ok(r[0].startswith('#dossier/') and 'Nouvelle consultation' in r[1], '4.2 : + Consultation : la consultation s\'ouvre dans le dossier', r)
        ok(not pg.errs, 'aucune erreur JavaScript', pg.errs[:2]); await pg.close()
        # sans document : un dessin et une phrase, sans bouton
        s2 = json.loads(json.dumps(s)); [s2.pop(k) for k in [k for k in s2 if '/fichiers/' in k]]
        pg = await ouvrir(b, s2, w=1440, h=900); ev = pg.evaluate
        await pg.goto(f'http://localhost:{PORT}/v2.html#accueil'); await pg.wait_for_timeout(2600)
        ok(await ev("(() => { const z = document.querySelector('#accDocs .ev-vide'); return !!z && !!z.querySelector('svg') && !z.querySelector('button'); })()"), '4.4 : aucun document : un dessin et une phrase, sans bouton')
        ok(not pg.errs, 'aucune erreur JavaScript', pg.errs[:2]); await pg.close()
        # 4.1 : une fois, l'ordre et les colonnes réglés avant sont remis au nouvel ordre (les cartes cachées restent cachées)
        s3 = json.loads(json.dumps(s)); s3[E + 'parametres/migrations'].pop('accueil1031', None); s3[E + 'parametres/accueil'] = {'data': json.dumps({'ordre': ['stats', 'jour', 'afaire', 'sept'], 'col': {'conflits': 'd'}, 'cartes': {'rappels': False}})}
        pg = await ouvrir(b, s3, w=1440, h=900); ev = pg.evaluate
        await pg.goto(f'http://localhost:{PORT}/v2.html#accueil'); await pg.wait_for_timeout(3500)
        m = await ev("[JSON.parse(window.__fs['espaces/cabinet-bentahila/parametres/accueil'].data), !!window.__fs['espaces/cabinet-bentahila/parametres/migrations'].accueil1031, [...document.querySelectorAll('#page .tb-c')].filter(e => e.getClientRects().length).map(e => e.dataset.carte).slice(0, 3)]")
        ok(m[0] == {'cartes': {'rappels': False}} and m[1] and m[2] == ['jour', 'actions', 'afaire'], '4.1 : disposition du cabinet remise une fois au nouvel ordre, cartes cachées gardées', m)
        ok(not pg.errs, 'aucune erreur JavaScript', pg.errs[:2]); await pg.close()
        # 31/10 (suite) : modifier un rendez-vous en pleine page, comme un nouveau
        print('Modifier un rendez-vous ; « Établissement » au lieu d\'« Hôpital »')
        pg = await ouvrir(b, s, w=1440, h=900); ev = pg.evaluate
        await pg.goto(f'http://localhost:{PORT}/v2.html#dossier/{RPID}'); await pg.wait_for_timeout(2600)
        await ev(f"ouvrirRdv('{RPID}', '{RRID}')"); await pg.wait_for_timeout(700)
        r = await ev("(() => { const f = document.getElementById('fenetre'); return [f.classList.contains('pleine'), !f.classList.contains('cache'), (document.querySelector('#fenetreCorps h3') || {}).textContent, !!document.querySelector('#fenetreCorps .rq-pat #rqSel .tx'), !document.getElementById('rqChg') && !document.getElementById('rq'), [...document.querySelectorAll('#fenetreCorps .pg-sec h4')].map(e => e.textContent)]; })()")
        ok(r[0] and r[1] and r[2] == 'Modifier le rendez-vous' and r[3] and r[4] and r[5] == ['Patient', 'Rendez-vous'], 'modifier un rendez-vous : pleine page, patient en haut (sans le changer), rendez-vous dessous', r)
        await pg.fill('#fMo', 'Motif modifié'); await pg.click('#fOk'); await pg.wait_for_timeout(1200)
        r = await ev(f"[document.getElementById('fenetre').classList.contains('cache'), JSON.parse(window.__fs['{E}patients/{RPID}'].rdvsJson || '[]').filter(v => v.id === '{RRID}').map(v => v.mo)]")
        ok(r[0] and r[1] == ['Motif modifié'], 'modifier un rendez-vous : Enregistrer garde le même rendez-vous, modifié', r)
        txt = []
        for h in ('patients', 'bilan', 'parametres/lieux', 'accueil'):
            await pg.goto(f'http://localhost:{PORT}/v2.html#' + h); await pg.wait_for_timeout(1800)
            t = await ev("[document.body.innerText, [...document.querySelectorAll('[aria-label],[title],option')].map(e => (e.getAttribute('aria-label') || '') + ' ' + (e.getAttribute('title') || '') + ' ' + e.textContent).join(' ')].join(' ')")
            txt += [h + ' : ' + m for m in __import__('re').findall(r'.{0,30}[Hh][oô]pita(?:l|ux)(?! de jour| de test).{0,30}', t)]
        await pg.goto(f'http://localhost:{PORT}/v2.html#dossier/{pid}'); await pg.wait_for_timeout(2400)
        t = await ev("document.body.innerText"); txt += ['dossier : ' + m for m in __import__('re').findall(r'.{0,30}[Hh][oô]pita(?:l|ux)(?! de jour| de test).{0,30}', t)]
        ok(not txt, '« Hôpital » / « hôpitaux » n\'apparaissent plus (Patients, Bilan, Lieux d\'exercice, tableau de bord, dossier ; noms des lieux fictifs et « hôpital de jour » à part)', txt[:4])
        ok(not pg.errs, 'aucune erreur JavaScript', pg.errs[:2]); await pg.close()
        s4 = json.loads(json.dumps(s)); s4[E + 'parametres/migrations'].pop('etab1031', None)
        fo = json.loads((s4.get(E + 'parametres/formulaires') or {}).get('data') or '{}'); fo.setdefault('fiche', {}).setdefault('libs', {})['etab'] = 'Hôpital'
        s4[E + 'parametres/formulaires'] = dict(s4.get(E + 'parametres/formulaires') or {}, data=json.dumps(fo))
        pg = await ouvrir(b, s4, w=1440, h=900); ev = pg.evaluate
        await pg.goto(f'http://localhost:{PORT}/v2.html#accueil'); await pg.wait_for_timeout(3500)
        m = await ev("[((JSON.parse(window.__fs['espaces/cabinet-bentahila/parametres/formulaires'].data).fiche || {}).libs || {}).etab || null, !!window.__fs['espaces/cabinet-bentahila/parametres/migrations'].etab1031]")
        ok(m == [None, True], 'nom « Hôpital » réglé par le cabinet retiré une fois (le champ reprend « Établissement »)', m)
        ok(not pg.errs, 'aucune erreur JavaScript', pg.errs[:2]); await pg.close()
        for w in (900, 390):
            pg = await ouvrir(b, s, w=w, h=900 if w > 500 else 844); ev = pg.evaluate
            await pg.goto(f'http://localhost:{PORT}/v2.html#accueil'); await pg.wait_for_timeout(2600)
            o = await ev("[...document.querySelectorAll('#page .tb-c')].filter(e => e.getClientRects().length).map(e => e.dataset.carte)")
            ok(o[:6] == ['jour', 'actions', 'afaire', 'sept', 'activite', 'documents'] and await ev("document.documentElement.scrollWidth") <= w, '4.1 : ' + str(w) + ' px : une colonne, dans l\'ordre ; rien ne déborde', o)
            ok(not pg.errs, 'aucune erreur JavaScript', pg.errs[:2]); await pg.close()
        await b.close()
    print(f'\n{ok_n} réussis, {ko_n} échoués')
asyncio.run(main())
