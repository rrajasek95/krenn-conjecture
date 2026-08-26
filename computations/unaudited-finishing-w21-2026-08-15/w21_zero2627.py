#!/usr/bin/env python3
"""W21 -- does the ZERO-FACTORING phenomenon reach m = 26 and m = 27?
UNAUDITED.  Exact only.  Replicates the search that found the m=28 witnesses
(full RANDOM-ORDER block-coordinate descents inside the clean layer) at all
three m, and records the minimum number of factoring sites reached."""
import json, os, random, sys, time
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction
import w21_core as K, w21_site as SI

DEADLINE=time.time()+3300
res={"_header":"UNAUDITED W21 zero-factoring search at m=26,27,28 (random-order descents)."}
for m in (28,26,27):
    T=K.W8_IMMUNE[m]; gam=K.gamma_edges(T); clean=K.clean_words(T)
    best=8; hits=[]; n=0; hist={}
    lim = DEADLINE - (2200 if m==28 else (1100 if m==26 else 0))
    while time.time()<lim:
        n+=1
        rng=random.Random(900000+m*1013+n)
        order=list(range(8)); rng.shuffle(order)
        bl=SI.descent(gam, clean, rng, order=order, passes=3)
        if bl is None: continue
        fac=[t for t in range(8) if K.factors_at(bl,gam,t)]
        hist[len(fac)]=hist.get(len(fac),0)+1
        if len(fac)<best:
            best=len(fac)
            ok=all(K.phi_value(bl,gam,w)==0 for w in clean)
            nz=all(bl[e][i][j]!=0 for e in gam for i in range(3) for j in range(3))
            print("m=%d run %d: NEW MIN %d factoring %s clean=%s nonzero=%s"%(m,n,len(fac),fac,ok,nz),flush=True)
            if len(fac)==0 and ok and nz:
                hits.append({str(e):[[str(x) for x in r] for r in bl[e]] for e in gam})
    res["m%d"%m]=dict(n_descents=n,min_factoring=best,
                      hist={str(k):v for k,v in sorted(hist.items())},
                      zero_factoring_points=hits[:3],n_zero=len(hits))
    print("m=%d: %d random-order descents, min factoring %d, histogram %s, zero-factoring hits %d"
          %(m,n,best,sorted(hist.items()),len(hits)),flush=True)
json.dump(res,open("results_zero2627.json","w"),indent=1,default=str)
