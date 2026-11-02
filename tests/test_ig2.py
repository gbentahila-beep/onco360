import pathlib; __file__=str(pathlib.Path(__file__).resolve()); exec(open(pathlib.Path(__file__).parent/'base.py').read())
# IG2 (02/11/2026, phase IG, idée 2 et D1) : « Imprimer le rendez-vous » sur chaque ligne de « Rendez-vous et tâches à venir » et de l'historique
# (consultation, séance de chimio, étapes de radiothérapie) ; une seule feuille : médecin et spécialité en haut, nom du patient sans n° de dossier,
# date avec l'année, heure en grand, type, lieu, « À savoir », « Imprimé le » ; A5 ou A4 et texte « À savoir » dans Paramètres › Impression.
import copy, json as _j
ok_n = ko_n = 0
def ok(c, m, d=None):
    global ok_n, ko_n
    if c: ok_n += 1; print('  ✔ ' + m)
    else: ko_n += 1; print('  ✘ ' + m + ('' if d is None else ' ' + str(d)[:500]))
U = f'http://localhost:{PORT}/v2.html#'
FAUX = "window.__impr=[]; window.open=()=>({document:{open(){},write(h){window.__impr.push(h)},close(){}},focus(){},print(){}}); 0"
# toutes les lignes (rubrique entière, au centre) : clic sur chaque « Imprimer le rendez-vous », feuille relevée
TOUT = """async (k) => { document.querySelector('details.dp[data-p="' + k + '"] .dp-t').click(); await new Promise(r => setTimeout(r, 500));
  const z = document.querySelector('[data-rub="' + k + '"]'); if (!z) return null; const out = [];
  for (const c of z.querySelectorAll('.rc')) { const bt = [...c.querySelectorAll('button')].find(b => b.textContent === 'Imprimer le rendez-vous'); const ty = (c.querySelector('.rl-ty') || {}).textContent;
    if (!bt) { out.push({ ty, sans: true }); continue; } window.__impr = []; bt.click(); out.push({ ty, h: window.__impr[0] || '' }); }
  return out; }"""
async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await ouvrir(b, S, w=1440); ev = pg.evaluate
        for pid, att in (('P20260928029', ['Séance de chimiothérapie · C1 J22', 'Dernière séance de radiothérapie']), ('P20260928015', ['Première séance de radiothérapie', 'Dernière séance de radiothérapie', 'Consultation de fin de radiothérapie'])):
            await pg.goto(U + 'dossier/' + pid); await pg.wait_for_timeout(2200); await ev(FAUX)
            nom = await ev("document.querySelector('.bp-id h2').textContent")
            L = await ev(TOUT, 'avenir')
            ok(L and all(not l.get('sans') for l in L if 'en retard' not in (l['ty'] or '')), f'{nom} : « Imprimer le rendez-vous » sur chaque ligne à venir, sauf une séance en retard ({len(L or [])})', [l['ty'] for l in (L or []) if l.get('sans')])
            tout = ' '.join(l.get('h', '') for l in L or [])
            ok(all(t in tout for t in att), f'{nom} : feuilles « {" », « ".join(att)} »', [l['ty'] for l in L or []])
            for l in (L or []):
                if l.get('sans') or l['ty'] == 'Tâche' or l['ty'] == 'RCP': continue
                h = l['h']
                bon = (nom in h and 'N° ' not in h and '2026' in h and 'À savoir' in h and 'Imprimé le' in h and 'fr-dr' in h and 'size:A5' in h and 'prévenez le plus tôt possible' in h and 'cabinet le plus' not in h)
                ok(bon, f'{nom} : feuille « {l["ty"]} » (nom, sans n° de dossier, année, À savoir, A5)', h[-700:])
            await ev("fermerFenetre && fermerFenetre(); 0"); await pg.wait_for_timeout(300)
            P = await ev(TOUT, 'passe')
            ok(P is not None and all(not l.get('sans') for l in P), f'{nom} : historique, « Imprimer le rendez-vous » sur chaque ligne ({len(P or [])})', [l['ty'] for l in (P or []) if l.get('sans')])
            await ev("fermerFenetre && fermerFenetre(); 0"); await pg.wait_for_timeout(300)
        # liste imprimée : inchangée (titre, n° de dossier)
        await ev(FAUX); await ev("dosImprimerListe('P20260928015', 'avenir')")
        h = await ev("window.__impr[0] || ''")
        ok('Rendez-vous et tâches à venir' in h and '<table>' in h, 'impression de la liste inchangée')
        ok(not pg.errs, 'aucune erreur JavaScript', pg.errs)
        await pg.close()
        # réglage du cabinet : A4 et texte « À savoir » à soi
        S2 = copy.deepcopy(S)
        rg = _j.loads((S2.get(E + 'parametres/reglages') or {}).get('data') or '{}'); rg.setdefault('impression', {}).update({'rdvA4': True, 'rdvSavoir': 'Apportez votre scanner.'})
        S2[E + 'parametres/reglages'] = {'data': _j.dumps(rg)}
        pg = await ouvrir(b, S2, w=1440); ev = pg.evaluate
        await pg.goto(U + 'dossier/P20260928029'); await pg.wait_for_timeout(2200); await ev(FAUX)
        L = await ev(TOUT, 'avenir'); h = next((l['h'] for l in L if not l.get('sans') and l['ty'] != 'Tâche'), '')
        ok('size:A4' in h and 'Apportez votre scanner.' in h and 'Venez 15 minutes' not in h, 'réglage : feuille en A4, texte « À savoir » du cabinet', h[-400:])
        await pg.close()
        # Paramètres › Impression : la secrétaire règle la feuille (droit « secrétariat »)
        S3 = copy.deepcopy(S); S3[E + 'membres/UIDSEC'] = {'role': 'assistante', 'nom': 'Secrétaire Test', 'actif': True, 'tousEtablissements': True, 'droits': {'secretariat': True, 'rendezvous': True}}
        for w in (1440, 390):
            p = await ouvrir(b, S3, w=w, h=900); await p.add_init_script("window.__uid='UIDSEC'")
            await p.goto(U + 'parametres/impression'); await p.reload(); await p.wait_for_timeout(2300)
            r = await p.evaluate("[!!document.getElementById('cfRdvS'), document.getElementById('cfRdvS') && document.getElementById('cfRdvS').disabled, document.getElementById('cfRdvS') && document.getElementById('cfRdvS').placeholder, document.documentElement.scrollWidth <= innerWidth + 1]")
            ok(r[0] and not r[1] and 'Venez 15 minutes' in (r[2] or '') and r[3], f'{w} px : Paramètres › Impression, « Feuille de rendez-vous » modifiable par la secrétaire, sans débordement', r)
            if w == 1440:
                await p.fill('#cfRdvS', 'Texte essai'); await p.wait_for_timeout(200)
                ok(await p.evaluate("!document.getElementById('cfMod') || !document.getElementById('cfMod').classList.contains('cache')"), 'texte saisi : « Enregistrer » proposé')
            ok(not p.errs, f'{w} px : aucune erreur JavaScript', p.errs)
            await p.close()
        await b.close()
    print(f'\n{ok_n} réussis, {ko_n} échoués')
asyncio.run(main())
