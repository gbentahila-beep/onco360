# Lecture du PDF officiel CTCAE v6.0 du NCI (domaine public) → public/donnees-outils/ctcae-v6.json (lot RT.15, 31/10/2026).
# Usage : python3 outils/ctcae-pdf.py ctcae-v6.pdf public/donnees-outils/ctcae-v6.json (pdfplumber).
import pdfplumber, json, re, sys
F=sys.argv[1]; OUT=sys.argv[2]
pdf=pdfplumber.open(F)
termes=[]; cur=None; soc=None; mode=None; cols=None
def joint(ws):
    s=''
    for w in ws:
        t=w['text']
        if not s: s=t
        elif s.endswith('-') and len(s)>1 and s[-2] not in ' <>' and not re.search(r'\d-$', s): s+=t
        else: s+=' '+t
    return s.strip()
def fin():
    global cur
    if cur:
        cur['g']=[joint(sorted(c,key=lambda w:(round(w['top']),w['x0']))) if False else ' '.join(cur['gl'][i]).strip() for i,c in enumerate(cur['gw'])]
        termes.append({'terme':cur['terme'],'soc':cur['soc'],'def':cur['def'].strip(),'note':cur['note'].strip(),'g':cur['g']})
    cur=None
for pn in range(4, len(pdf.pages)+1):
    p=pdf.pages[pn-1]; H=p.height
    ws=[w for w in p.extract_words(extra_attrs=['fontname','size']) if 45 < w['top'] < H-50 or (w['size']>13)]
    # lignes
    lignes={}
    for w in ws: lignes.setdefault(round(w['top']),[]).append(w)
    keys=sorted(lignes)
    # fusion de lignes à 1-2 px
    L=[]
    for k in keys:
        if L and k-L[-1][0]<=2: L[-1][1].extend(lignes[k])
        else: L.append([k,list(lignes[k])])
    for top,lw in L:
        lw.sort(key=lambda w:w['x0']); f=lw[0]['fontname']; sz=lw[0]['size']; txt=' '.join(w['text'] for w in lw)
        if sz>13 and 'Bold' in f: fin(); soc=txt; mode=None; continue
        if 'SemiBold' in f and lw[0]['x0']<50:
            if mode=='nom' and cur: cur['terme']+=' '+txt; continue
            fin(); cur={'terme':txt,'soc':soc,'def':'','note':'','gw':[[] for _ in range(5)],'gl':[[] for _ in range(5)]}; mode='nom'; continue
        if cur is None: continue
        if lw[0]['text']=='Grade' and 'Bold' in f:
            cols=[w['x0'] for w in lw if w['text']=='Grade']; mode='grade'; continue
        if txt.startswith('Definition:'): cur['def']=txt[len('Definition:'):]; mode='def'; continue
        if txt.startswith('Navigational Note:'): cur['note']=txt[len('Navigational Note:'):]; mode='note'; continue
        if mode=='grade' and cols:
            par=[[] for _ in range(5)]
            for w in lw:
                i=max([j for j,c in enumerate(cols) if w['x0']>=c-6] or [0]); par[i].append(w)
            for i in range(5):
                if par[i]:
                    t=joint(par[i]); gl=cur['gl'][i]
                    if gl and gl[-1].endswith('-') and len(gl[-1])>1 and not gl[-1].endswith(' -') and not re.search(r'[\d<>=] ?-$', gl[-1]): gl[-1]=gl[-1]+t
                    else: gl.append(t)
        elif mode=='def': cur['def']+=' '+txt
        elif mode=='note': cur['note']+=' '+txt
fin()
for t in termes:
    t['g']=[re.sub(r'\s+',' ',x).strip() for x in t['g']]
    t['g']=['' if x=='-' else x for x in t['g']]
    for k in ('def','note'):
        t[k]=re.sub(r'\s+',' ',t[k]).strip()
        if t[k]=='-': t[k]=''
    if not t['note']: del t['note']
json.dump(termes, open(OUT,'w'), ensure_ascii=False)
print(len(termes), len(set(t['soc'] for t in termes)))
