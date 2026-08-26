#!/usr/bin/env python3
"""W21 MOVE 1 -- THE DICTIONARY between original factoring and the reduced
K_4 problem.  UNAUDITED.  Exact only.

For each full-box L-word x the clean layer gives an identically-vanishing
K_4 hafnian in the modified R-blocks M^(x); define
   rcd_R(a, x) = dim span of the columns (indexed by the colour at a) of the
                 three M^(x) incident to the R-site a.
Mirror: rcd_L(i, y) for the four full-box R-words y.
MEASURED CLAIM under test [CONJECTURED]:
   site a of R factors  <=>  rcd_R(a,x) = 1 for the full-box x's;
   site i of L factors  <=>  rcd_L(i,y) = 1;
and hence "some site factors" <=> "some reduced site has col-dim 1".
"""
import json, os, sys
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction
from itertools import product
import w21_core as K, w21_block as B
from w21_pf import load_w20_points

def box_R(y):
    out={i:set(range(3)) for i in B.L}
    for (i,j),(a,b) in B.SINGLES.items():
        if y[j-4]==b: out[i].discard(a)
    return out
FBY=[y for y in product(range(3),repeat=4) if all(len(v)==3 for v in box_R(y).values())]

def N_of(bl,gam,y,i,j,P):
    e=(min(i,j),max(i,j))
    Ap=[[bl[e][r][s] for s in range(3)] for r in range(3)]
    k,l=[z for z in B.L if z not in (i,j)]
    a,b=B.SIG[k],B.SIG[l]; e2=(min(a,b),max(a,b))
    coef = bl[e2][y[e2[0]-4]][y[e2[1]-4]] if e2 in set(gam) else Fraction(0)
    ci=[bl[(i,B.SIG[i])][r][y[B.SIG[i]-4]] for r in range(3)]
    cj=[bl[(j,B.SIG[j])][r][y[B.SIG[j]-4]] for r in range(3)]
    g=coef/P
    return [[Ap[r][s]+g*ci[r]*cj[s] for s in range(3)] for r in range(3)]

def coldims(Ms, side):
    out={}
    for i in B.L:
        cols=[]
        for j in B.L:
            if j==i: continue
            key=(min(i,j),max(i,j)); Mm=Ms[key]
            if key[0]==i: cols+=[[Mm[r][s] for r in range(3)] for s in range(3)]
            else: cols+=[[Mm[s][r] for r in range(3)] for s in range(3)]
        out[B.SIG[i] if side=='R' else i]=K.rank_of(cols,3)
    return out

res={"_header":"UNAUDITED W21 reduced/original factoring dictionary. Exact."}
pts=load_w20_points()
extra={}
if os.path.exists('results_break.json'):
    d=json.load(open('results_break.json'))
    for m in (26,27,28):
        for rec in d.get('m%d'%m,[]):
            if 'point' in rec:
                bl={}
                for k,v in rec['point'].items():
                    e=tuple(int(z) for z in k.strip('()').split(','))
                    bl[e]=[[Fraction(z) for z in row] for row in v]
                extra.setdefault(m,[]).append(("break seed %d"%rec['seed'],bl))
rows=[]
for m in (26,27,28):
    T=K.W8_IMMUNE[m]; gam=K.gamma_edges(T); clean=K.clean_words(T)
    for tag,bl in [pts[m][0]]+extra.get(m,[]):
        assert all(K.phi_value(bl,gam,w)==0 for w in clean)
        fac=[t for t in range(8) if K.factors_at(bl,gam,t)]
        rcdR={}; rcdL={}
        for x in B.full_box_words():
            P=B.hafL(bl,x)
            if P==0: continue
            Ms={pr:B.M_of(bl,gam,x,pr[0],pr[1],P) for pr in B.LPAIRS}
            for a,v in coldims(Ms,'R').items(): rcdR.setdefault(a,set()).add(v)
        for y in FBY:
            P=B.hafR(bl,gam,y)
            if P==0: continue
            Ns={pr:N_of(bl,gam,y,pr[0],pr[1],P) for pr in B.LPAIRS}
            for i,v in coldims(Ns,'L').items(): rcdL.setdefault(i,set()).add(v)
        redfac=sorted([a for a,v in rcdR.items() if v=={1}]+[i for i,v in rcdL.items() if v=={1}])
        agree = (redfac==fac)
        rows.append(dict(m=m,tag=tag,factoring=fac,reduced_coldim1=redfac,agree=agree,
                         rcdR={str(k):sorted(v) for k,v in rcdR.items()},
                         rcdL={str(k):sorted(v) for k,v in rcdL.items()}))
        print("m=%d %-16s factoring %-14s | reduced col-dim-1 sites %-14s | agree %s"
              % (m,tag,fac,redfac,agree), flush=True)
res["rows"]=rows
res["dictionary_agreement"] = "%d/%d" % (sum(1 for r in rows if r["agree"]), len(rows))
print("dictionary agreement: %s" % res["dictionary_agreement"])
json.dump(res,open("results_dict.json","w"),indent=1,default=str)

# --- extension: the dictionary on the extra points (results_more.json) ---
if os.path.exists('results_more.json'):
    dm=json.load(open('results_more.json')); rows2=[]
    for m in (26,27,28):
        T=K.W8_IMMUNE[m]; gam=K.gamma_edges(T); clean=K.clean_words(T)
        for rec in dm.get('m%d'%m,[]):
            bl={}
            for k,v in rec['point'].items():
                e=tuple(int(z) for z in k.strip('()').split(','))
                bl[e]=[[Fraction(z) for z in row] for row in v]
            fac=[t for t in range(8) if K.factors_at(bl,gam,t)]
            rcdR={}; rcdL={}
            for x in B.full_box_words():
                P=B.hafL(bl,x)
                if P==0: continue
                Ms={pr:B.M_of(bl,gam,x,pr[0],pr[1],P) for pr in B.LPAIRS}
                for a,v in coldims(Ms,'R').items(): rcdR.setdefault(a,set()).add(v)
            for y in FBY:
                P=B.hafR(bl,gam,y)
                if P==0: continue
                Ns={pr:N_of(bl,gam,y,pr[0],pr[1],P) for pr in B.LPAIRS}
                for i,v in coldims(Ns,'L').items(): rcdL.setdefault(i,set()).add(v)
            redfac=sorted([a for a,v in rcdR.items() if v=={1}]+[i for i,v in rcdL.items() if v=={1}])
            rows2.append(dict(m=m,order=rec['order'],seed=rec['seed'],factoring=fac,
                              reduced=redfac,agree=(redfac==fac)))
            print("EXTRA m=%d %-7s s%d factoring %-16s reduced %-16s agree %s"
                  % (m,rec['order'],rec['seed'],fac,redfac,redfac==fac), flush=True)
    print("EXTRA dictionary agreement: %d/%d" % (sum(1 for r in rows2 if r['agree']),len(rows2)))
    d0=json.load(open('results_dict.json')); d0['extra_rows']=rows2
    d0['extra_agreement']="%d/%d"%(sum(1 for r in rows2 if r['agree']),len(rows2))
    json.dump(d0,open('results_dict.json','w'),indent=1,default=str)
