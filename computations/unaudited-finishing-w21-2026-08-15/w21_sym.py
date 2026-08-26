#!/usr/bin/env python3
"""W21 MOVE 1(b) -- the SYMMETRY GROUP of the clean-layer problem.
UNAUDITED.  Exact finite group computation with constraint propagation.

Aut(Gamma, clean set): sigma with sigma(Gamma) = Gamma together with per-site
colour permutations pi_v in S_3 whose induced action maps the CLEAN WORD SET
to itself.  Since the clean set is exactly the forbidden-pair set
   FP = { (i, j, alpha, beta) } (12 items, one per non-matching cross edge),
the condition is that (sigma i, sigma j, pi_i(alpha), pi_j(beta)) in FP for
every item -- a constraint system solved here by propagation.
This is the group that acts on the residual-1 question (which is stated
purely in terms of Gamma and the clean set); it can be LARGER than
Aut(T), the symmetry group of the full template that W20 reported.
"""
import json, os, sys
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import w21_core as K
from itertools import permutations, product

SINGLES = {(0,4):(0,0),(0,5):(0,1),(0,6):(0,2),(1,5):(1,0),(1,6):(1,1),
           (1,7):(0,2),(2,4):(1,0),(2,6):(2,1),(2,7):(1,2),(3,4):(2,0),
           (3,5):(2,1),(3,7):(2,2)}
FPD = {(i,j):(a,b) for (i,j),(a,b) in SINGLES.items()}

def graph_auts(gam):
    E=set(gam); out=[]
    for s in permutations(range(8)):
        if len(gam)==sum(1 for (u,v) in gam if (min(s[u],s[v]),max(s[u],s[v])) in E):
            out.append(s)
    return out

def completions(partial):
    """number of bijections [3]->[3] extending the partial map (dict)."""
    if len(set(partial.values()))!=len(partial): return 0
    out=[]
    for p in permutations(range(3)):
        if all(p[k]==v for k,v in partial.items()): out.append(p)
    return out

res={"_header":"UNAUDITED W21 clean-layer symmetry groups. Exact."}
for m in (26,27,28):
    T=K.W8_IMMUNE[m]; gam=K.gamma_edges(T); clean=set(K.clean_words(T))
    gauts=graph_auts(gam)
    total=0; ex=[]
    for s in gauts:
        part={v:{} for v in range(8)}; ok=True
        for (i,j),(a,b) in FPD.items():
            ii,jj=s[i],s[j]
            key=(ii,jj) if (ii,jj) in FPD else ((jj,ii) if (jj,ii) in FPD else None)
            if key is None: ok=False; break
            aa,bb=FPD[key]
            if key==(ii,jj): tgt_i,tgt_j=aa,bb
            else: tgt_i,tgt_j=bb,aa
            if part[i].get(a,tgt_i)!=tgt_i or part[j].get(b,tgt_j)!=tgt_j: ok=False; break
            part[i][a]=tgt_i; part[j][b]=tgt_j
        if not ok: continue
        opts=[completions(part[v]) for v in range(8)]
        if any(not o for o in opts): continue
        cnt=1
        for o in opts: cnt*=len(o)
        # verify a sample explicitly against the clean set
        for pis in product(*opts):
            img={tuple(pis[v][w[v]] for v in range(8)) for w in list(clean)[:400]}
            # map site positions too
            good=True
            for w in list(clean)[:400]:
                w2=[0]*8
                for v in range(8): w2[s[v]]=pis[v][w[v]]
                if tuple(w2) not in clean: good=False; break
            if good:
                total+=1
                if len(ex)<6: ex.append((list(s),[list(p) for p in pis]))
    res["m%d"%m]=dict(n_graph_auts=len(gauts), aut_clean_layer=total,
                      examples=ex)
    print("m=%d: |Aut(Gamma)|=%d   |Aut(Gamma, clean set)|=%d" % (m,len(gauts),total))
    for s,pis in ex[:6]:
        print("     sigma=%s  colours=%s" % (s,pis))
json.dump(res,open("results_sym.json","w"),indent=1,default=str)
