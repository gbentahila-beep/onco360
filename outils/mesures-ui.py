#!/usr/bin/env python3
# IG9 (03/11/2026, étape 8 de l'audit UX / UI) : mesures de l'interface sur les 14 pages de l'audit du 02/11/2026, jeu fictif des tests,
# 390 / 900 / 1 280 / 1 600 px, Chrome et Safari (WebKit), médecin (secrétaire et infirmière : 1 440 px). Compte les variantes de boutons, badges,
# cartes, ombres, arrondis, couleurs de texte, polices ; débordements et erreurs JavaScript ; captures.
# Utilisation (depuis tests/) : .venv/bin/python ../outils/mesures-ui.py <dossier de sortie> [port d'un autre serveur, ex. version d'avant]
# Navigateurs : NAVS=chromium (ou webkit) pour n'en mesurer qu'un ; par défaut les deux.
import sys, os, pathlib, json, collections
__file__ = str(pathlib.Path(__file__).resolve().parent.parent / 'tests' / 'mesures.py')
exec(open(pathlib.Path(__file__).parent / 'base.py').read())
SORTIE = pathlib.Path(sys.argv[1]); SORTIE.mkdir(parents=True, exist_ok=True)
P = int(sys.argv[2]) if len(sys.argv) > 2 else PORT
PID = 'P20260928029'
PAGES = ['accueil', 'agenda', 'salle', 'patients', 'dossier/' + PID, 'documents', 'taches', 'rcp', 'protocoles', 'radiotherapie', 'outils', 'bilan', 'parametres', 'profil']
LARGEURS = [390, 900, 1280, 1600]
S2 = json.loads(json.dumps(S))
for u, r in [('SEC', 'assistante'), ('INF', 'infirmiere')]:
    S2[E + 'membres/' + u] = {'role': r, 'nom': u, 'email': u.lower() + '@test.ma', 'actif': True, 'tousEtablissements': True, 'etablissements': [], 'droits': {}}
    S2['utilisateurs/' + u] = {'nom': u, 'prenom': 'Test'}
MESURE = r"""(() => {
  const vis = (e) => { const r = e.getBoundingClientRect(); if (!r.width || !r.height) return false; const s = getComputedStyle(e); return s.visibility !== 'hidden' && s.display !== 'none' && +s.opacity > 0; };
  const sty = (e) => getComputedStyle(e), o = { boutons: [], hauteurs: [], bordBt: [], badges: [], cartes: [], ombres: [], arrondis: [], textes: [], polices: [] };
  const zone = document.querySelector('main, #page') || document.body, tous = [...document.querySelectorAll('#page *, #tete *, nav *, #fenetre *')].filter(vis);
  tous.filter(e => e.matches('button, .bt, .b1, .b2, .b3, a.bt, summary.bt, summary.b3, summary.mini, .mini')).forEach(e => { const s = sty(e), h = Math.round(e.getBoundingClientRect().height);
    o.boutons.push([s.backgroundColor, s.color, parseFloat(s.borderTopWidth) ? s.borderTopColor : 'aucune', s.borderTopLeftRadius, h, s.fontSize, s.fontWeight].join('|')); o.hauteurs.push(h);
    if (parseFloat(s.borderTopWidth) && s.borderTopColor !== 'rgba(0, 0, 0, 0)') o.bordBt.push(s.borderTopColor); });
  tous.filter(e => e.matches('.badge, .nb, .n, .pastille, .cpt, .bd-n, .rtr-pas')).forEach(e => { const s = sty(e); o.badges.push([s.backgroundColor, s.color, s.fontSize, s.fontWeight, s.borderTopLeftRadius].join('|')); });
  tous.filter(e => e.matches('.carte, section.carte, .sq-c, .pcarte, .rtr-carte')).forEach(e => { const s = sty(e); o.cartes.push([s.borderTopLeftRadius, s.boxShadow, s.borderTopWidth + ' ' + s.borderTopColor, s.backgroundColor].join('|')); });
  tous.forEach(e => { const s = sty(e); if (s.boxShadow !== 'none') o.ombres.push(s.boxShadow); const r = s.borderTopLeftRadius;
    if (r !== '0px' && (s.backgroundColor !== 'rgba(0, 0, 0, 0)' || parseFloat(s.borderTopWidth))) o.arrondis.push(parseFloat(r) >= 100 ? 'rond' : r);
    if ([...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) { o.textes.push(s.color); o.polices.push([s.fontFamily.split(',')[0].replace(/"/g, ''), s.fontSize, s.fontWeight].join(' ')); } });
  o.deborde = document.documentElement.scrollWidth > innerWidth + 1;
  return o; })()"""
async def main():
    tot = collections.defaultdict(collections.Counter); par = {}; pb = []
    async with async_playwright() as pw:
        for nav in os.environ.get('NAVS', 'chromium,webkit').split(','):
            b = await getattr(pw, nav).launch()
            for w in LARGEURS:
                for page in PAGES:
                    pg = await ouvrir(b, S2, w=w, h=900 if w > 500 else 844)
                    if page == 'documents': await pg.add_init_script("window.__uid='SEC'")
                    await pg.goto(f'http://localhost:{P}/v2.html#' + page); await pg.wait_for_timeout(3000)
                    m = await pg.evaluate(MESURE)
                    for k, v in m.items():
                        if isinstance(v, list): tot[k].update(v); par.setdefault(k, collections.defaultdict(set))[page.split('/')[0]].update(map(str, v))
                    if m['deborde']: pb.append(f'{nav} {w} px {page} : débordement')
                    if pg.errs: pb.append(f'{nav} {w} px {page} : erreur JavaScript {pg.errs[0][:120]}')
                    if (nav == 'chromium' and w in (390, 1600)) or (nav == 'webkit' and w == 1280):
                        await pg.screenshot(path=str(SORTIE / f'{page.split("/")[0]}-{w}-{nav}.png'))
                    await pg.close()
            for uid in ('SEC', 'INF'):
                for page in ('accueil', 'salle', 'dossier/' + PID, 'taches', 'agenda'):
                    pg = await ouvrir(b, S2, w=1440); await pg.add_init_script(f"window.__uid='{uid}'")
                    await pg.goto(f'http://localhost:{P}/v2.html#' + page); await pg.wait_for_timeout(3000)
                    m = await pg.evaluate(MESURE)
                    if m['deborde']: pb.append(f'{nav} {uid} {page} : débordement')
                    if pg.errs: pb.append(f'{nav} {uid} {page} : erreur JavaScript {pg.errs[0][:120]}')
                    await pg.close()
            await b.close()
    res = {k: {'variantes': len(c), 'detail': c.most_common()} for k, c in tot.items()}
    res['problemes'] = pb
    (SORTIE / 'mesures.json').write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')
    for k, c in tot.items(): print(f'{k} : {len(c)} variantes')
    print('hauteurs de bouton :', sorted(set(tot['hauteurs'])))
    print('problèmes :', len(pb)); [print('  ' + x) for x in pb[:30]]
asyncio.run(main())
