#!/usr/bin/env python3
"""W21 -- more exact clean points at m=26,27,28 with varied factoring sets,
for the dictionary test.  UNAUDITED.  Exact only."""
import json, os, random, sys
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction
import w21_core as K, w21_site as SI

ORDERS = {"fwd": list(range(8)), "rev": list(range(7,-1,-1)),
          "inter": [0,4,1,5,2,6,3,7], "Rfirst": [4,5,6,7,0,1,2,3]}
res = {"_header": "UNAUDITED W21 extra exact clean points. Exact only."}
for m in (26,27,28):
    T=K.W8_IMMUNE[m]; gam=K.gamma_edges(T); clean=K.clean_words(T)
    out=[]
    for name,order in ORDERS.items():
        for seed in (11,23):
            rng=random.Random(50000+seed*13+m)
            bl=SI.descent(gam, clean, rng, order=order, passes=3)
            if bl is None: continue
            ok=all(K.phi_value(bl,gam,w)==0 for w in clean)
            nz=all(bl[e][i][j]!=0 for e in gam for i in range(3) for j in range(3))
            fac=[t for t in range(8) if K.factors_at(bl,gam,t)]
            out.append(dict(order=name,seed=seed,clean=ok,nonzero=nz,factoring=fac,
                            point={str(e):[[str(x) for x in r] for r in bl[e]] for e in gam}))
            print("m=%d order=%-7s seed %d -> factoring %s clean=%s nz=%s" % (m,name,seed,fac,ok,nz), flush=True)
    res["m%d"%m]=out
json.dump(res,open("results_more.json","w"),indent=1,default=str)
