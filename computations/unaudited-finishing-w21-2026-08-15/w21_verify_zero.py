#!/usr/bin/env python3
"""W21 -- INDEPENDENT VERIFICATION of the claimed ZERO-FACTORING clean points
at m=28.  UNAUDITED.  Exact only.  Uses (a) the W21 engine, (b) W20's engine
(itself cross-checked against W19), and (c) a from-the-definition hafnian."""
import json, os, sys, glob
sys.dont_write_bytecode = True
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
sys.path.insert(0,"/Users/rishi/workplace/krenn-conjecture/computations/unaudited-lasttwo-w20-2026-08-15")
from fractions import Fraction
from itertools import combinations
import w21_core as K
import w20_core as W20C

def brute_phi(bl, gam, w):
    """from the definition: sum over perfect matchings of Gamma."""
    ES=set(gam); tot=Fraction(0)
    for M in K.PMS:
        if all(e in ES for e in M):
            p=Fraction(1)
            for (u,v) in M: p*=bl[(u,v)][w[u]][w[v]]
            tot+=p
    return tot

def load(path):
    d=json.load(open(path))
    # find the block dict anywhere in the json
    def walk(o):
        if isinstance(o,dict):
            ks=list(o.keys())
            if ks and all(k.startswith("(") and "," in k for k in ks):
                try:
                    return {tuple(int(z) for z in k.strip("()").split(",")):
                            [[Fraction(x) for x in row] for row in v] for k,v in o.items()}
                except Exception: pass
            for v in o.values():
                r=walk(v)
                if r: return r
        if isinstance(o,list):
            for v in o:
                r=walk(v)
                if r: return r
        return None
    return walk(d)

T=K.W8_IMMUNE[28]; gam=K.gamma_edges(T); clean=K.clean_words(T)
fullm=W20C.full_pm_indices(T)
out={"_header":"UNAUDITED W21 independent verification of the zero-factoring points."}
for path in sorted(glob.glob(os.path.join(HERE,"tensor","results_zero*.json"))):
    bl=load(path)
    if bl is None: print("no block dict in",path); continue
    keys_ok = sorted(bl.keys())==sorted(gam)
    nz=sum(1 for e in gam for i in range(3) for j in range(3) if bl[e][i][j]!=0)
    c21=sum(1 for w in clean if K.phi_value(bl,gam,w)!=0)
    c20=sum(1 for w in clean if W20C.phi_value(bl,fullm,w)!=0)
    cbr=sum(1 for w in clean if brute_phi(bl,gam,w)!=0)
    f21=[t for t in range(8) if K.factors_at(bl,gam,t)]
    f20=[t for t in range(8) if W20C.site_factors(bl,gam,t)]
    # explicit column-span rank per site
    ranks={}
    for t in range(8):
        cols=[]
        for s in K.neighbours(gam,t):
            e=(min(t,s),max(t,s))
            for d in range(3):
                cols.append([bl[e][c][d] if e[0]==t else bl[e][d][c] for c in range(3)])
        ranks[t]=K.rank_of([[cols[k][i] for k in range(len(cols))] for i in range(3)],len(cols))
    rec=dict(path=os.path.basename(path), gamma_keys_match=keys_ok,
             nonzero_cells="%d/144"%nz, clean_failures_W21=c21,
             clean_failures_W20engine=c20, clean_failures_bruteforce=cbr,
             factoring_W21=f21, factoring_W20=f20, site_column_span_rank=ranks)
    out[os.path.basename(path)]=rec
    print(json.dumps(rec, indent=1, default=str))
json.dump(out,open(os.path.join(HERE,"results_verify_zero.json"),"w"),indent=1,default=str)
