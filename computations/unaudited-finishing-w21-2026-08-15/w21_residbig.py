#!/usr/bin/env python3
"""W21 (RE-AIMED) -- LARGE-SCALE test of the residual linear kill at
m = 24..28.  UNAUDITED.  Exact only.

For every clean point (all Gamma cells nonzero) reached by a random-order
exact block-coordinate descent, decide the residual system
   { H_w = 0 : w mixed, H_w of degree <= 1 in the non-Gamma cells }
exactly.  KILLED means: inconsistent, OR some non-Gamma occupied cell is
IDENTICALLY ZERO on the affine solution set (which contradicts the
exact-source requirement that every occupied cell be nonzero).
Per LEDGER 18 the points are constructed OUTSIDE any asserted locus: the
sample deliberately spans 0,1,2,3,4,5 factoring sites.
"""
import json, os, random, sys, time
sys.dont_write_bytecode = True
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from fractions import Fraction
import w21_core as K, w21_site as SI
from w21_resid import residual_linear_test

DEADLINE=time.time()+3000
res={"_header":"UNAUDITED W21 large-scale residual linear kill test."}
for m in (28,27,26,25,24):
    T=K.W8_IMMUNE[m]; gam=K.gamma_edges(T); clean=K.clean_words(T)
    tested=0; killed=0; byfac={}; surv=[]
    lim=DEADLINE-(2400 if m==28 else 2400-(28-m)*600)
    n=0
    while time.time()<lim:
        n+=1
        rng=random.Random(3000000+m*7717+n)
        order=list(range(8)); rng.shuffle(order)
        bl=SI.descent(gam,clean,rng,order=order,passes=3)
        if bl is None: continue
        if any(K.phi_value(bl,gam,w)!=0 for w in clean): continue
        if not all(bl[e][i][j]!=0 for e in gam for i in range(3) for j in range(3)): continue
        fac=tuple(t for t in range(8) if K.factors_at(bl,gam,t))
        r=residual_linear_test(T,bl)
        kill = r["inconsistent"] or bool(r.get("forced_zero_cells"))
        tested+=1; killed+=kill
        k=len(fac); byfac.setdefault(k,[0,0]); byfac[k][0]+=1; byfac[k][1]+=kill
        if not kill:
            surv.append(dict(factoring=list(fac),
                             point={str(e):[[str(x) for x in row] for row in bl[e]] for e in gam},
                             detail=r))
            print("m=%d SURVIVOR (not killed) factoring %s  %s"%(m,fac,r),flush=True)
    res["m%d"%m]=dict(tested=tested,killed=killed,
                      by_n_factoring={str(k):v for k,v in sorted(byfac.items())},
                      survivors=surv[:3],n_survivors=len(surv))
    print("m=%d: %d clean points tested, %d KILLED by the residual linear system "
          "(by #factoring sites: %s)"%(m,tested,killed,sorted(byfac.items())),flush=True)
json.dump(res,open("results_residbig.json","w"),indent=1,default=str)
