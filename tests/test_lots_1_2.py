import pathlib; __file__=str(pathlib.Path(__file__).resolve()); exec(open(pathlib.Path(__file__).parent/'base.py').read())
# Lots 1 et 2 (31/10/2026, demandes de Dr Bentahila, document « Onco360 — Demandes à faire ») : mise en page seulement (aucune police ni couleur changée).
# Lot 1 : boutons « + Patient », « + Rendez-vous », « + Tâche » à la même place sur chaque page ; icônes centrées sur leur texte ; mêmes écarts entre cartes
# (18 px) et entre champs côte à côte (12 px, mêmes hauteurs) ; menus déroulants assez larges ; tableaux alignés ; états vides à une seule image ; bulles « ? » ;
# listes qui ne s'ouvrent pas d'elles-mêmes ; « O » de « Onco360 (automatique) » ; titre sur une ligne au téléphone.
# Lot 2 : Nouveau patient en pleine page (trois sous-parties), N° d'immatriculation / d'adhérent (champ de base, reprise de l'ancien champ du cabinet),
# Nouveau rendez-vous en pleine page (patient existant ou nouveau, rendez-vous dessous), Patients en tableau, menus sous la recherche, période de l'agenda
# entre les flèches. Ordinateur (1280, 1600, 900 px) et téléphone (390 px). Jeu fictif.
ok_n = ko_n = 0
def ok(c, m, d=None):
    global ok_n, ko_n
    if c: ok_n += 1; print('  ✔ ' + m)
    else: ko_n += 1; print('  ✘ ' + m + ('' if d is None else ' ' + str(d)[:400]))
s = json.loads(json.dumps(S)); P = sorted([k.split('/')[-1] for k in s if k.startswith(E + 'patients/') and k.count('/') == 3])
pid = [k.split('/')[-1] for k, v in s.items() if k.startswith(E + 'patients/') and len(v.get('lignesJson') or '') > 50][0]
# 2.2 : ancien champ « N° d'immatriculation » propre au cabinet (Paramètres › Fiche patient), avec une valeur dans un dossier
s[E + 'parametres/formulaires'] = {'data': json.dumps({'fiche': {'ajouts': [{'id': 'xim001', 'lib': "N° d'immatriculation", 'type': 'texte', 'partie': 'identite', 'entete': True}], 'ordre': None}})}
fo = json.loads(s[E + 'parametres/formulaires']['data']); del fo['fiche']['ordre']; s[E + 'parametres/formulaires']['data'] = json.dumps(fo)
PIM = P[1]; s[E + 'patients/' + PIM]['identite'].setdefault('extra', {})['xim001'] = '123456789'
def tache(i, **o):
    d = {'titre': 'Tâche %d' % i, 'desc': '', 'type': 'Administratif', 'urgent': False, 'ech': '2026-10-0%d' % (i % 9 + 1), 'h': '', 'patientId': '', 'patientNom': '', 'etablissementId': '', 'de': 'UIDRITA', 'deNom': 'Dr TEST',
         'pour': 'UIDRITA', 'pourNom': 'Dr TEST', 'qui': ['UIDRITA'], 'statut': 'afaire', 'fil': [{'le': '2026-10-05T10:00:00Z', 'par': 'UIDRITA', 'parNom': 'Dr TEST', 'txt': 'Créée'}], 'o': i}
    d.update(o); return d
for i in (1, 2): s[E + 'taches/T%d' % i] = tache(i)
s[E + 'taches/T4'] = tache(4, statut='fait', titre='Terminée', de='onco360', deNom='Onco360 (automatique)')
s2 = json.loads(json.dumps(s)); s2[E + 'taches/T1']['statut'] = s2[E + 'taches/T2']['statut'] = 'fait'  # 1.7 : toutes terminées
s[E + 'taches/T5'] = tache(5, statut='fait')
VIS = "(e) => !!e && e.getClientRects().length > 0 && getComputedStyle(e).visibility !== 'hidden'"
B1 = "[...document.querySelectorAll('#page .b1')].filter(" + VIS + ").map(e => { const r = e.getBoundingClientRect(); return [e.textContent.trim(), Math.round(r.top), Math.round(r.right)]; })"
# 1.4 : écart entre deux cartes voisines (au-dessus / au-dessous ou côte à côte, sans autre carte entre elles)
GAPS = """(() => { const v = (e) => e.getClientRects().length > 0 && getComputedStyle(e).visibility !== 'hidden' && ['fixed', 'sticky'].indexOf(getComputedStyle(e).position) < 0;
  const out = [], cs = [...document.querySelectorAll('#page .carte')].filter(v), R = (e) => e.getBoundingClientRect();
  for (const a of cs) for (const b of cs) { if (a === b || a.contains(b) || b.contains(a)) continue; const A = R(a), B = R(b), hov = Math.min(A.right, B.right) - Math.max(A.left, B.left), vov = Math.min(A.bottom, B.bottom) - Math.max(A.top, B.top);
    const entre = (f) => cs.some((c) => c !== a && c !== b && !c.contains(a) && !c.contains(b) && !a.contains(c) && !b.contains(c) && f(R(c)));
    if (hov > 20 && B.top >= A.bottom - 1 && B.top - A.bottom < 60 && !entre((C) => C.top >= A.bottom - 1 && C.bottom <= B.top + 1 && Math.min(C.right, A.right) - Math.max(C.left, A.left) > 20)) out.push(Math.round(B.top - A.bottom));
    if (vov > 20 && B.left >= A.right - 1 && B.left - A.right < 60) out.push(Math.round(B.left - A.right)); }
  return out; })()"""
# 1.4 : champs côte à côte : écart et hauteurs
CHAMPS = """(() => { const L = [...document.querySelectorAll('#fenetreCorps input:not([type=checkbox]):not([type=radio]):not([type=hidden]), #fenetreCorps select, #page .form input:not([type=checkbox]):not([type=radio]):not([type=hidden]), #page .form select')].filter(e => e.getClientRects().length);
  const out = []; for (const a of L) for (const b of L) { const A = a.getBoundingClientRect(), B = b.getBoundingClientRect();
    if (a !== b && Math.abs(A.top - B.top) < 30 && B.left > A.right - 1 && B.left - A.right < 40 && !L.some(c => c !== a && c !== b && c.getBoundingClientRect().left >= A.right - 1 && c.getBoundingClientRect().right <= B.left + 1 && Math.abs(c.getBoundingClientRect().top - A.top) < 30)) out.push([Math.round(B.left - A.right), Math.round(A.height), Math.round(B.height), Math.round(A.top - B.top), a.id, b.id]); }
  return out; })()"""
# 1.5 : le libellé choisi tient dans son menu, place gardée pour la flèche
MENUS = """(() => { const c = document.createElement('canvas').getContext('2d'), out = [];
  for (const s of document.querySelectorAll('#page select, #fenetreCorps select')) { if (!s.getClientRects().length || s.multiple || s.size > 1) continue; const cs = getComputedStyle(s), o = s.options[s.selectedIndex]; if (!o) continue;
    c.font = cs.fontWeight + ' ' + cs.fontSize + ' ' + cs.fontFamily; const tw = c.measureText(o.text).width, dispo = s.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight);
    if (tw > dispo + 1 || (cs.backgroundImage !== 'none' && parseFloat(cs.paddingRight) < 26)) out.push([s.id || s.className, o.text, Math.round(tw), Math.round(dispo)]); }
  return out; })()"""
# 1.6 : tableaux de mêmes colonnes (même en-tête) sur une page : colonnes à la même place
TABLES = """(() => { const T = [...document.querySelectorAll('#page .ta-tab, #page .pt-tab, #page table')].filter(e => e.getClientRects().length), G = {}, out = [];
  T.forEach(t => { const h = t.matches('table') ? [...(t.querySelector('tr') || { children: [] }).children] : [...(t.querySelector('.ta-h, .pt-h') || { children: [] }).children]; const v = h.filter(e => e.getClientRects().length);
    if (v.length < 2 || !v.every(e => e.getBoundingClientRect().width > 0)) return; const k = v.map(e => e.textContent.trim()).join('|'); (G[k] = G[k] || []).push(v.map(e => [Math.round(e.getBoundingClientRect().left), Math.round(e.getBoundingClientRect().right)])); });
  Object.entries(G).forEach(([k, l]) => { for (let i = 1; i < l.length; i++) if (l[i].some((c, j) => Math.abs(c[0] - l[0][j][0]) > 1 || Math.abs(c[1] - l[0][j][1]) > 1)) out.push([k.slice(0, 60), l[0], l[i]]); });
  return out; })()"""
# 1.3 : centre de chaque icône contre le milieu des capitales du texte qui la suit (écart ≤ 2,5 px)
ICONES = r'''(() => { const out = [], vu = (e) => e.getClientRects().length > 0 && getComputedStyle(e).visibility !== 'hidden';
  for (const s of document.querySelectorAll('#page svg.i, #page svg.pi, #fenetreCorps svg.i, #fenetreCorps svg.pi, #panneauCorps svg.i')) {
    if (!vu(s) || getComputedStyle(s).position === 'absolute') continue;
    const p = s.parentElement; let t = null;
    // premier texte voisin (frère direct, ou texte d'un frère élément en ligne)
    for (let n = s.nextSibling; n && !t; n = n.nextSibling) { if (n.nodeType === 3 && n.textContent.trim()) t = n; else if (n.nodeType === 1 && n.tagName !== 'svg' && vu(n) && n.textContent.trim() && getComputedStyle(n).display.indexOf('inline') === 0) { const w = document.createTreeWalker(n, NodeFilter.SHOW_TEXT); let z; while ((z = w.nextNode())) if (z.textContent.trim()) { t = z; break; } } }
    if (!t) continue;
    const r = document.createRange(); r.setStart(t, 0); r.setEnd(t, Math.min(t.textContent.length, Math.max(1, t.textContent.search(/\S/) + 1)));
    const R = r.getClientRects()[0]; if (!R) continue; const S = s.getBoundingClientRect();
    // centre de la ligne de texte (hauteur des capitales ≈ 0,7 em, centrée sur la boîte du texte) contre centre de l'icône
    const fs = parseFloat(getComputedStyle(t.parentElement).fontSize), base = R.bottom - (R.height - fs) / 2 - fs * 0.22, cText = base - fs * 0.36, cIc = S.top + S.height / 2;
    if (Math.abs(R.top + R.height / 2 - (S.top + S.height / 2)) > 8) continue; // pas sur la même ligne
    const d = Math.round((cIc - cText) * 10) / 10;
    if (Math.abs(d) > 2.5) out.push([d, (p.tagName + '.' + (p.className && p.className.baseVal === undefined ? p.className : '')).slice(0, 30), t.textContent.trim().slice(0, 24)]);
  }
  return out; })()'''
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        # ───── Lot 1 ─────
        for w in (1600, 1280, 900):
            print('Lot 1 – bouton principal (' + str(w) + ' px)')
            pg = await ouvrir(b, s, w=w, h=900); ev = pg.evaluate
            r = {}
            for hs in ('accueil', 'patients', 'agenda', 'salle', 'taches'):
                await pg.goto(f'http://localhost:{PORT}/v2.html#{hs}'); await pg.wait_for_timeout(2300); r[hs] = await ev(B1)
            ok([x[0][0] for x in r.values()] == ['Patient', 'Patient', 'Rendez-vous', 'Rendez-vous', 'Tâche'] and all(len(x) == 1 for x in r.values()), '1.1 : « + Patient », « + Patient », « + Rendez-vous » (agenda, salle d\'attente), « + Tâche » ; un seul bouton principal par page', r)
            hauts, droites = [x[0][1] for x in r.values()], [x[0][2] for x in r.values()]
            ok(max(hauts) - min(hauts) <= 1 and max(droites) - min(droites) <= 1, '1.2 : bouton principal à la même hauteur et au même bord droit sur les cinq pages', r)
            await pg.goto(f'http://localhost:{PORT}/v2.html#accueil'); await pg.wait_for_timeout(2200)
            a = await ev("[...document.querySelectorAll('.accueil .actions button')].map(e => e.textContent.trim() + ':' + e.className)")
            ok(a == ['Rendez-vous:b2', 'Patient:b1'], '1.2 : tableau de bord : « + Rendez-vous » puis « + Patient » (principal, le plus à droite)', a)
            ok(not pg.errs, 'aucune erreur JavaScript', pg.errs[:2]); await pg.close()
        print('Lot 1 – mise en page commune (1440 px)')
        pg = await ouvrir(b, s, w=1440, h=900); ev = pg.evaluate
        await pg.goto(f'http://localhost:{PORT}/v2.html#salle'); await pg.wait_for_timeout(2300)
        r = await ev("(() => { const a = document.getElementById('saAct').getBoundingClientRect(), n = document.querySelector('.sa-nouv').getBoundingClientRect(), p = document.getElementById('saPlus').getBoundingClientRect(); return [Math.abs((a.top + a.bottom) / 2 - (n.top + n.bottom) / 2) <= 2, n.left > p.right, document.getElementById('saSuiv').className.indexOf('b2') >= 0]; })()")
        ok(all(r), '1.2 : salle d\'attente : « + Rendez-vous » au bout de la ligne d\'Actualiser et de « ⋯ » ; « Patient suivant » secondaire', r)
        # 1.3 icônes centrées sur leur texte
        for hs in ('parametres/whatsapp', 'bilan', 'patients', 'dossier/' + pid, 'taches', 'agenda'):
            await pg.goto(f'http://localhost:{PORT}/v2.html#{hs}'); await pg.wait_for_timeout(2300)
            r = await ev(ICONES); ok(not r, '1.3 : icônes centrées sur leur texte : ' + hs.split('/')[0], r[:4])
        # 1.4 écarts entre cartes
        for hs in ('accueil', 'agenda', 'bilan', 'rcp', 'dossier/' + pid, 'parametres/rcp', 'parametres/impression', 'parametres/export', 'parametres/whatsapp', 'parametres/vigilances', 'parametres/fermetures', 'parametres/couleurs', 'parametres/alertes', 'parametres/activites', 'parametres/affichage'):
            await pg.goto(f'http://localhost:{PORT}/v2.html#{hs}'); await pg.wait_for_timeout(2300)
            g = await ev(GAPS); ok(set(g) <= {18}, '1.4 : 18 px entre les cartes : ' + hs, sorted(set(g)))
        await pg.goto(f'http://localhost:{PORT}/v2.html#parametres/rcp'); await pg.wait_for_timeout(2300)
        c = await ev(CHAMPS); ok(c and all(x[0] == 12 and x[1] == x[2] and x[3] == 0 for x in c), '1.4 : Paramètres › RCP : Heure et Lieu à 12 px, même hauteur, même ligne', c)
        # 1.5 menus déroulants
        for hs in ('taches', 'bilan', 'protocoles', 'parametres/types', 'parametres/consultation', 'patients'):
            await pg.goto(f'http://localhost:{PORT}/v2.html#{hs}'); await pg.wait_for_timeout(2300)
            if hs == 'taches': await ev("document.getElementById('taFst').value='tous';document.getElementById('taFst').dispatchEvent(new Event('change',{bubbles:true}))"); await pg.wait_for_timeout(400)
            m = await ev(MENUS); ok(not m, '1.5 : libellé entier dans chaque menu, flèche à part : ' + hs, m[:3])
        # 1.6 tableaux alignés (tâches terminées sous les tâches à faire)
        await pg.goto(f'http://localhost:{PORT}/v2.html#taches'); await pg.wait_for_timeout(2300)
        await ev("document.getElementById('taFst').value='ouv';document.getElementById('taFst').dispatchEvent(new Event('change',{bubbles:true}))"); await pg.wait_for_timeout(400)
        if not await ev("!!document.querySelector('.ta-finies .ta-tab')"): await ev("taTerminees()"); await pg.wait_for_timeout(400)
        n = await ev("document.querySelectorAll('.ta-tab').length"); t = await ev(TABLES)
        ok(n == 2 and not t, '1.6 : tâches terminées : colonnes alignées sur le tableau du dessus', t)
        # 1.10 auteur automatique : « O »
        av = await ev("[...document.querySelectorAll('.ta-finies .ta-av')].map(e => e.textContent)")
        ok('O' in av and not any('(' in x for x in av), '1.10 : « Onco360 (automatique) » : pastille « O »', av)
        for hs in ('bilan', 'patients', 'parametres/fermetures', 'parametres/activites'):
            await pg.goto(f'http://localhost:{PORT}/v2.html#{hs}'); await pg.wait_for_timeout(2300)
            t = await ev(TABLES); ok(not t, '1.6 : tableaux de mêmes colonnes alignés : ' + hs, t)
        # 1.7 états vides : une seule image
        await pg.goto(f'http://localhost:{PORT}/v2.html#accueil'); await pg.wait_for_timeout(2300)
        ok(await ev("!document.querySelector('.ev-rond') && document.querySelectorAll('.ev-mini').length > 0"), '1.7 : « Aucune consultation prévue aujourd\'hui » : plus d\'icône répétée avant la phrase')
        p2 = await ouvrir(b, s2, w=1440, h=900); await p2.goto(f'http://localhost:{PORT}/v2.html#taches'); await p2.wait_for_timeout(2300)
        f = await p2.evaluate("(() => { const z = document.querySelector('#taL .ev-vide'); return z ? [z.querySelector('h4').textContent, !!z.querySelector('svg.ev-ill rect[x=\"110\"][y=\"25\"]'), !z.querySelector('path[d^=\"M74 92l36-30\"]')] : null; })()")
        ok(f and f[0] == 'Toutes les tâches sont terminées' and f[1] and f[2], '1.7 : « Toutes les tâches sont terminées » : dessin d\'Onco360 (presse-papiers coché), plus le cône de fête', f); await p2.close()
        # 1.8 bulles « ? »
        await pg.goto(f'http://localhost:{PORT}/v2.html#dossier/{pid}'); await pg.wait_for_timeout(2500)
        await ev("document.querySelector('.dos-tabs [data-o=chimio], [data-onglet=chimio], button[onclick*=\"chimio\"]')?.click()"); await pg.wait_for_timeout(600)
        await ev("""(() => { const q = document.createElement('button'); q.className = 'q-aide'; q.id = 'qT'; q.textContent = '?'; q.dataset.txt = 'Explication fictive assez longue pour tenir sur plusieurs lignes : elle ne doit jamais être coupée par le bas de l\\'écran.'; q.style.cssText = 'position:fixed;left:200px;bottom:4px;z-index:90'; document.body.appendChild(q); })()""")
        await pg.hover('#qT'); await pg.wait_for_timeout(200)
        r = await ev("(() => { const b = document.getElementById('bulleAide'); if (!b) return null; const R = b.getBoundingClientRect(); return [Math.round(R.top), Math.round(R.bottom), innerHeight, b.textContent.length > 40, document.body.classList.contains('voir-aides')]; })()")
        ok(r and r[0] >= 0 and r[1] <= r[2] and r[3] and not r[4], '1.8 : « ? » en bas de l\'écran : bulle entière au survol, au-dessus, jamais coupée ; rien n\'est affiché en bas de la page', r)
        await pg.mouse.move(700, 300); await pg.wait_for_timeout(200)
        ok(await ev("!document.getElementById('bulleAide')"), '1.8 : la bulle disparaît quand la souris s\'en va')
        q = await ev("(() => { const q = document.querySelector('.aide-b.q-aide'); return q ? q.getAttribute('onclick') : 'absent'; })()")
        ok(q is None or q == 'absent', '1.8 : « ? » des lignes de chimio : bulle, plus d\'affichage des explications au clic', q)
        # 1.9 liste d'un champ déjà rempli : fermée à l'ouverture, ouverte après 2 lettres tapées
        await ev(f"dosRubrique('{pid}','id')"); await pg.wait_for_timeout(700)
        await ev("(() => { const m = document.getElementById('fMut'); m.value = 'CNOPS'; m.focus(); m.click(); })()"); await pg.wait_for_timeout(300)
        ok(await ev("!document.querySelector('.lst-sug')"), '1.9 : champ « Mutuelle » déjà rempli : la liste ne s\'ouvre ni à l\'arrivée ni au clic')
        await ev("document.getElementById('fMut').value = ''"); await pg.type('#fMut', 'C'); await pg.wait_for_timeout(200)
        un = await ev("!!document.querySelector('.lst-sug')"); await pg.type('#fMut', 'N'); await pg.wait_for_timeout(300)
        ok(not un and await ev("!!document.querySelector('.lst-sug')"), '1.9 : la liste s\'ouvre après la 2e lettre tapée')
        ok(not pg.errs, 'aucune erreur JavaScript', pg.errs[:2]); await pg.close()
        # 1.11 téléphone : titre sur une ligne
        print('Lot 1 – téléphone (390 px)')
        pg = await ouvrir(b, s, w=390, h=844); ev = pg.evaluate
        for hs, t in (('accueil', 'Tableau de bord'), ('agenda', 'Agenda'), ('salle', "Salle d'attente"), ('patients', 'Patients'), ('parametres', 'Paramètres'), ('taches', 'Tâches')):
            await pg.goto(f'http://localhost:{PORT}/v2.html#{hs}'); await pg.wait_for_timeout(2200)
            r = await ev("(() => { const h = document.getElementById('titrePage'); return [h.innerText.trim(), h.getBoundingClientRect().height, h.scrollWidth <= h.clientWidth + 1, document.documentElement.scrollWidth]; })()")
            ok(r[0] == t and r[1] <= 28 and r[2] and r[3] <= 390, '1.11 : titre « ' + t + ' » sur une ligne, entier ; rien ne déborde', r)
        ok(not pg.errs, 'aucune erreur JavaScript', pg.errs[:2]); await pg.close()
        # ───── Lot 2 ─────
        for w in (1280, 390):
            print('Lot 2 (' + str(w) + ' px)')
            pg = await ouvrir(b, s, w=w, h=900 if w > 500 else 844); ev = pg.evaluate
            await pg.goto(f'http://localhost:{PORT}/v2.html#patients'); await pg.wait_for_timeout(2600)
            # 2.2 reprise de l'ancien champ du cabinet
            m = await ev(f"(() => {{ const p = window.__fs['espaces/cabinet-bentahila/patients/{PIM}'].identite, f = JSON.parse(window.__fs['espaces/cabinet-bentahila/parametres/formulaires'].data).fiche || {{}}; return [p.numAdh, !!(p.extra && 'xim001' in p.extra), (f.ajouts || []).length, (f.entetes || {{}}).numAdh]; }})()")
            ok(m == ['123456789', False, 0, True], '2.2 : ancien « N° d\'immatriculation » du cabinet repris dans le champ de base (valeur, en-tête), retiré de la fiche du cabinet', m)
            # 2.4 / 2.5 Patients
            r = await ev("(() => { const q = document.querySelector('.pt-q').getBoundingClientRect(), b = document.querySelector('.pt-l1 .b1').getBoundingClientRect(), f = document.querySelector('.pt-f').getBoundingClientRect(); return [Math.abs((q.top + q.bottom) / 2 - (b.top + b.bottom) / 2) <= 3, f.top >= q.bottom, q.width > (innerWidth > 500 ? 600 : 200), [...document.querySelectorAll('.pt-h > span')].filter(e => e.getClientRects().length).map(e => e.textContent)]; })()")
            ok(r[0] and r[1] and r[2], '2.5 : « + Patient » à la hauteur de la recherche (élargie), menus sur la ligne suivante', r[:3])
            # n° de dossier : sa colonne à partir de 1 400 px, sous le nom en dessous (place)
            if w > 500: ok([x.rstrip('↕▲▼') for x in r[3]] == ['Nom Prénom', 'Date de naissance', 'Établissement', 'Cancer', 'Dernières nouvelles', 'Traitement en cours'] and await ev("getComputedStyle(document.querySelector('.pt-num-s')).display") == 'block', '2.4 : patients en tableau : Nom Prénom (n° de dossier dessous à 1 280 px), date de naissance, établissement, cancer, dernières nouvelles, traitement', r[3])
            ok(await ev("document.querySelectorAll('#lst .pt-r').length") == len(P) and await ev("document.documentElement.scrollWidth") <= w, '2.4 : un patient par rangée ; rien ne déborde')
            # 2.1 Nouveau patient
            await ev("nouveauPatient()"); await pg.wait_for_timeout(600)
            r = await ev("(() => { const f = document.getElementById('fenetre'), g = [...document.querySelectorAll('#fenetreCorps .fp-g')].map(z => [z.dataset.g, z.querySelector('.fp-gt').textContent, [...z.querySelectorAll('[data-champ]')].map(c => c.dataset.champ)]); return [f.classList.contains('pleine'), g, [...document.querySelectorAll('#fenetreCorps .boutons button')].map(e => e.textContent.trim())]; })()")
            ok(r[0], '2.1 : Nouveau patient en pleine page (menu et barre du haut gardés)')
            ok([z[1] for z in r[1]] == ['Identité', 'Contact', 'Couverture et parcours de soins'] and set(['nom', 'prenom', 'ddn', 'sexe', 'cin']) <= set(r[1][0][2]) and set(['tel', 'tel2', 'email', 'adresse']) <= set(r[1][1][2]) and set(['mut', 'numAdh', 'ald', 'etab', 'cor']) <= set(r[1][2][2]), '2.1 : trois sous-parties et leurs champs', r[1])
            ok(r[2] == ['Annuler', 'Créer le patient'], '2.1 : en bas : Annuler, Créer le patient', r[2])
            if w > 500:
                l = await ev("(() => { const t = (k) => { const e = document.querySelector('#fenetreCorps [data-champ=' + k + ']'); return e ? Math.round(e.getBoundingClientRect().top) : null; }; return [['nom', 'prenom'], ['tel', 'tel2'], ['email', 'adresse'], ['mut', 'numAdh'], ['etab', 'cor']].map(([a, b]) => t(a) !== null && t(a) === t(b)); })()")
                ok(all(l), '2.1 / 2.2 : côte à côte : nom et prénom, téléphones, e-mail et adresse, mutuelle et n° d\'immatriculation, établissement et correspondant', l)
                c = await ev(CHAMPS); ok(c and all(x[0] == 12 and x[1] == x[2] for x in c), '1.4 : champs côte à côte à 12 px et à la même hauteur', [x for x in c if x[0] != 12 or x[1] != x[2]])
                tr = await ev("(() => { const z = [...document.querySelectorAll('#fenetreCorps .fp-gf')]; return z.map(g => { const c = [...g.children].flatMap(e => e.classList.contains('fp-p') ? [...e.children] : [e]).filter(e => e.getClientRects().length); const rows = {}; c.forEach(e => { const t = Math.round(e.getBoundingClientRect().top); rows[t] = (rows[t] || 0) + (e.classList.contains('large') ? 2 : 1); }); const v = Object.values(rows); return v.slice(0, -1).every(n => n === 2); }); })()")
                ok(all(tr), '2.1 : aucun trou (chaque ligne pleine, sauf la dernière de chaque sous-partie)', tr)
            await pg.click('#fenetreCorps .fp-seg button[data-v=H]'); await pg.fill('#fNomF', 'zzlot'); await pg.fill('#fPrenom', 'Deux'); await pg.fill('#fNumAdh', 'AD-778')
            sx = await ev("[document.getElementById('fSexe').value, document.querySelector('.fp-seg button.on').textContent]")
            ok(sx == ['H', 'Masculin'], '2.1 : sexe en deux boutons Masculin / Féminin', sx)
            await pg.click('#fOk'); await pg.wait_for_timeout(1500)
            nv = await ev("(() => { const k = Object.keys(window.__fs).find(k => k.startsWith('espaces/cabinet-bentahila/patients/') && (window.__fs[k].identite || {}).nomF === 'ZZLOT'); return k ? [window.__fs[k].identite.sexe, window.__fs[k].identite.numAdh, location.hash.indexOf('#dossier/') === 0] : null; })()")
            ok(nv == ['H', 'AD-778', True], '2.1 : « Créer le patient » : sexe et n° d\'immatriculation enregistrés, dossier ouvert', nv)
            # même formulaire au centre du dossier (Identité et administratif)
            if w > 500:
                await ev(f"dosRubrique('{pid}','id')"); await pg.wait_for_timeout(700)
                g = await ev("[...document.querySelectorAll('#panneauCorps .fp-g .fp-gt')].map(e => e.textContent)")
                ok(g == ['Identité', 'Contact', 'Couverture et parcours de soins'], '2.1 : « Identité et administratif » ouvert au centre : le même formulaire', g)
                await ev("fermerFenetre()")
            # 2.3 Nouveau rendez-vous en pleine page
            await pg.goto(f'http://localhost:{PORT}/v2.html#agenda'); await pg.wait_for_timeout(2300)
            await ev("document.querySelector('.ag-nouv').click()"); await pg.wait_for_timeout(600)
            r = await ev("[document.getElementById('fenetre').classList.contains('pleine'), [...document.querySelectorAll('.rq-seg button')].map(e => e.textContent), !!document.getElementById('fType') && !!document.getElementById('fD') && !!document.getElementById('fMo') && !!document.getElementById('fDu'), [...document.querySelectorAll('#fenetreCorps .boutons button')].map(e => e.textContent.trim())]")
            ok(r[0] and r[1] == ['Patient existant', '+ Patient'] and r[2] and r[3] == ['Annuler', 'Enregistrer'], '2.3 : Nouveau rendez-vous en pleine page : patient existant ou nouveau, rendez-vous dessous tout de suite, Annuler / Enregistrer', r)
            await pg.fill('#fMo', 'Motif gardé'); await pg.click('#fOk'); await pg.wait_for_timeout(300)
            ok('Choisissez le patient' in await ev("document.getElementById('fErr').textContent"), '2.3 : Enregistrer sans patient : « Choisissez le patient »')
            await pg.click('#rqNv'); await pg.wait_for_timeout(500)
            ok(await ev("document.querySelector('#fenetreCorps h3').textContent") == 'Nouveau patient', '2.3 : « Nouveau patient » ouvre le formulaire 2.1')
            await pg.click('#fAnn'); await pg.wait_for_timeout(500)
            ok(await ev("document.getElementById('fMo') && document.getElementById('fMo').value") == 'Motif gardé', '2.3 : Annuler ramène au rendez-vous tel qu\'il était rempli')
            await pg.click('#rqNv'); await pg.wait_for_timeout(500); await pg.fill('#fNomF', 'zzrdv'); await pg.fill('#fPrenom', 'Trois'); await pg.click('#fOk'); await pg.wait_for_timeout(1500)
            r = await ev("[document.querySelector('#fenetreCorps h3') && document.querySelector('#fenetreCorps h3').textContent, document.getElementById('rqSel') && document.getElementById('rqSel').textContent, document.getElementById('fMo') && document.getElementById('fMo').value]")
            ok(r[0] == 'Nouveau rendez-vous' and 'ZZRDV' in (r[1] or '') and r[2] == 'Motif gardé', '2.3 : « Créer le patient » ramène au rendez-vous, ce patient choisi, saisie gardée', r)
            await pg.fill('#fH', '11:30'); await pg.click('#fOk'); await pg.wait_for_timeout(1500)
            if await ev("!!document.getElementById('fenetre') && !document.getElementById('fenetre').classList.contains('cache') && /WhatsApp/.test(document.getElementById('fenetreCorps').textContent)"): await ev("fermerFenetre()")
            rv = await ev("(() => { const k = Object.keys(window.__fs).find(k => (window.__fs[k].identite || {}).nomF === 'ZZRDV'); return k ? JSON.parse(window.__fs[k].rdvsJson || '[]').map(r => [r.mo, r.h]) : null; })()")
            ok(rv == [['Motif gardé', '11:30']], '2.3 : rendez-vous enregistré pour le nouveau patient', rv)
            # depuis un dossier : patient déjà choisi
            await ev(f"ouvrirRdv('{pid}')"); await pg.wait_for_timeout(600)
            r = await ev("[document.getElementById('fenetre').classList.contains('pleine'), !document.getElementById('rqSel').classList.contains('cache'), !document.querySelector('.rq-seg'), document.getElementById('rqCh').classList.contains('cache')]")
            ok(all(r), '2.3 : depuis un dossier : patient déjà choisi', r)
            await ev("fermerFenetre()")
            # 2.6 Agenda : la période entre les flèches
            await ev("agVue('semaine')"); await pg.wait_for_timeout(600)
            r = await ev("(() => { const n = document.querySelector('.ag-nav'), k = [...n.children].map(e => e.tagName + (e.getAttribute('aria-label') ? ':' + e.getAttribute('aria-label') : '')); return [k, n.querySelector('b').textContent]; })()")
            ok(r[0][-3:] == ['BUTTON:Précédent', 'B', 'BUTTON:Suivant'] and ' – ' in r[1], '2.6 : agenda : ‹ période › (date entre les flèches)', r)
            ok(await ev("document.documentElement.scrollWidth") <= w, 'rien ne déborde')
            ok(not pg.errs, 'aucune erreur JavaScript', pg.errs[:2]); await pg.close()
        await b.close()
    print(f'\n{ok_n} réussis, {ko_n} échoués')
asyncio.run(main())
