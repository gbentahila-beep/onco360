import pathlib; __file__=str(pathlib.Path(__file__).resolve()); exec(open(pathlib.Path(__file__).parent/'base.py').read())
# IG1 (02/11/2026, phase IG, audit UX / UI) : recherche de patient classée (idée 1), pastille chiffrée entière (idée 4, D4), Types de consultation
# sans cases l'une sur l'autre (idée 9, D5), « traitement systémique » (D3). Jeu fictif seulement.
ok_n = ko_n = 0
def ok(c, m, d=None):
    global ok_n, ko_n
    if c: ok_n += 1; print('  ✔ ' + m)
    else: ko_n += 1; print('  ✘ ' + m + ('' if d is None else ' ' + str(d)[:400]))
U = f'http://localhost:{PORT}/v2.html#'
PID = 'P20260928029'
import copy
S = copy.deepcopy(S)
_i = S[E + 'patients/' + PID]['identite']
_i.update({'tel': '06 61 23 45 87', 'cin': 'BK778899', 'ddn': '1961-03-27'})
CHEV = """() => { const L = [...document.querySelectorAll('.ty-l:not(.ty-h)')]; const bad = [];
  L.forEach((l) => { const c = [...l.querySelectorAll('.ty-s, input.ty-n')].map((e) => e.getBoundingClientRect()).filter((r) => r.width > 0);
    for (let i = 0; i < c.length; i++) for (let j = i + 1; j < c.length; j++) { const a = c[i], b = c[j];
      if (a.left < b.right - 1 && b.left < a.right - 1 && a.top < b.bottom - 1 && b.top < a.bottom - 1) bad.push(l.querySelector('.ty-n').value); }
    l.querySelectorAll('.ty-s select').forEach((s) => { const r = s.getBoundingClientRect(), p = s.closest('.ty-s').getBoundingClientRect(); if (r.right > p.right + 1) bad.push('menu hors de sa case : ' + l.querySelector('.ty-n').value); });
    const n = l.querySelector('.ty-n'); if (n.scrollWidth > n.clientWidth + 2) bad.push('nom coupé : ' + n.value); });
  return { n: L.length, bad: [...new Set(bad)] }; }"""
async def tete(pg, q):
    await pg.fill('#trQ', ''); await pg.type('#trQ', q, delay=10); await pg.wait_for_timeout(400)
    return await pg.evaluate("[...document.querySelectorAll('#trRes button')].map(b => b.querySelector('b').textContent)")
async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await ouvrir(b, S, w=1440); ev = pg.evaluate
        await pg.goto(U + 'accueil'); await pg.wait_for_timeout(2500)
        # ───── idée 1 : recherche du haut ─────
        r = await tete(pg, 'test 80')
        ok(r and r[0] == 'PATIENT TEST 80', 'recherche du haut : « test 80 » → PATIENT TEST 80 en tête', r)
        ok(await ev("document.querySelector('#trRes button mark') && document.querySelector('#trRes button mark').textContent.toLowerCase() === 'test'"), 'partie trouvée surlignée')
        await pg.keyboard.press('Enter'); await pg.wait_for_timeout(1500)
        ok(PID in await ev("location.hash"), 'Entrée ouvre le bon dossier (PATIENT TEST 80)', await ev("location.hash"))
        await pg.goto(U + 'accueil'); await pg.wait_for_timeout(1200)
        await tete(pg, 'test')
        t = await ev("(document.querySelector('#trRes .tr-plus') || {}).textContent || ''")
        ok('8 sur' in t and 'Voir tout dans Patients' in t, '« 8 sur N · Voir tout dans Patients »', t)
        # le jeu fictif donne le même téléphone, CIN et date de naissance à TEST 8, 16, 80… (n° différents)
        for q, lib in (('0661234587', 'téléphone'), ('06 61 23 45 87', 'téléphone avec espaces'), ('+212661234587', 'téléphone +212'), ('27/03/1961', 'date de naissance'), ('bk778899', 'CIN'), ('202610080', 'n° de dossier')):
            r = await tete(pg, q)
            ok(r and r[0] == 'PATIENT TEST 80', f'recherche du haut : {lib} « {q} » → PATIENT TEST 80 en tête', r[:4])
        # « Voir tout dans Patients » : la page Patients reprend la recherche, même classement
        await tete(pg, 'test 8')
        await ev("document.querySelector('#trRes [data-voir]').dispatchEvent(new MouseEvent('mousedown', { bubbles: true }))"); await pg.wait_for_timeout(1500)
        r = await ev("[location.hash, document.getElementById('q') && document.getElementById('q').value, [...document.querySelectorAll('.pt-r b')].slice(0, 2).map(b => b.textContent)]")
        ok(r[0] == '#patients' and r[1] == 'test 8' and r[2][0] == 'PATIENT TEST 8', '« Voir tout » : page Patients avec la même recherche, TEST 8 en tête', r)
        # page Patients : mêmes règles (téléphone, CIN), et la localisation en plus
        for q, att in (('0661234587', 'PATIENT TEST 80'), ('BK77', 'PATIENT TEST 80'), ('test 80', 'PATIENT TEST 80')):
            await pg.fill('#q', q); await ev("document.getElementById('q').dispatchEvent(new Event('input'))"); await pg.wait_for_timeout(300)
            r = await ev("[...document.querySelectorAll('.pt-r b')].map(b => b.textContent)")
            ok(r and r[0] == att, f'page Patients : « {q} » → {att} en tête', r[:4])
        await pg.fill('#q', 'oropharynx'); await ev("document.getElementById('q').dispatchEvent(new Event('input'))"); await pg.wait_for_timeout(300)
        ok(await ev("document.querySelectorAll('.pt-r').length") > 0, 'page Patients : la localisation est encore cherchée')
        # ───── idée 4 (D4) : pastille chiffrée entière ─────
        await pg.goto(U + 'dossier/' + PID); await pg.wait_for_timeout(2500)
        await ev("const b = document.querySelector('.br-g [data-fn=\"prescriptions.medic\"] > button'); b.insertAdjacentHTML('beforeend', '<small class=\"br-n\">3</small>'); 0")
        r = await ev("""(() => { const n = document.querySelector('.br-g [data-fn="prescriptions.medic"] .br-n'), p = n.closest('.pr'), rn = n.getBoundingClientRect(), rp = p.getBoundingClientRect();
          return { ov: getComputedStyle(p).overflow, dehors: rn.top < rp.top, vu: document.elementFromPoint(rn.left + rn.width / 2, rn.top + 2) === n }; })()""")
        ok(r['ov'] == 'visible' and r['dehors'] and r['vu'], 'D4 : la pastille dépasse du bouton et se voit en entier', r)
        # ───── D3 ─────
        await pg.goto(U + 'protocoles'); await pg.wait_for_timeout(1800)
        t = await ev("document.getElementById('titrePage').innerText")
        ok('traitement systémique' in t, 'D3 : sous-titre « Bibliothèque des protocoles de traitement systémique »', t)
        ok(await ev("import('./js/donnees/catalogue.js').then(m => m.BIBLIOTHEQUES[0][1])") == 'Protocoles de traitement systémique', 'D3 : liste des bibliothèques')
        ok(not pg.errs, 'aucune erreur JavaScript', pg.errs)
        await pg.close()
        # ───── idée 9 (D5) : Types de consultation, à plusieurs largeurs ─────
        for w in (1280, 1440, 1600, 1920, 900):
            p2 = await ouvrir(b, S, w=w)
            await p2.goto(U + 'parametres/types'); await p2.wait_for_timeout(2300)
            r = await p2.evaluate(CHEV)
            ok(r['n'] >= 8 and not r['bad'], f'D5 : {w} px, aucune case l\'une sur l\'autre, noms entiers ({r["n"]} types)', r)
            ok(await p2.evaluate("document.documentElement.scrollWidth <= innerWidth + 1"), f'D5 : {w} px, pas de débordement')
            await p2.close()
        p3 = await ouvrir(b, S, w=390, h=844)
        await p3.goto(U + 'parametres/types'); await p3.wait_for_timeout(2300)
        ok(await p3.evaluate("document.documentElement.scrollWidth <= innerWidth + 1"), 'D5 : 390 px, pas de débordement')
        await p3.goto(U + 'accueil'); await p3.wait_for_timeout(1500)
        ok(not p3.errs, 'aucune erreur JavaScript (téléphone)', p3.errs)
        await b.close()
    print(f'\n{ok_n} réussis, {ko_n} échoués')
asyncio.run(main())
