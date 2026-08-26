#!/usr/bin/env python3
"""W26 -- fast point hunt: how many fresh clean points, and how many lie OFF
the identically-vanishing stratum, per m?  UNAUDITED.  Exact only."""
import sys, os, random, json
from fractions import Fraction
sys.dont_write_bytecode=True
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
import w26_core as C, w26_fast as F
N=int(os.environ.get("N","40")); MS=[int(v) for v in os.environ.get("MS","25,26,27,28").split(",")]
out={}
for m in MS:
    mdl=F.Model(m); got=[]; nvan=0; tried=0
    for k in range(N*20):
        tried+=1
        rng=random.Random(9_000_000+1000*m+k)
        order=list(range(8)); rng.shuffle(order)
        bl=F.make_point(mdl,rng,passes=4,order=order)
        if bl is None: continue
        v=mdl.vanishing(bl); nvan+=v
        got.append((bl,v))
        if len(got)>=N: break
    off=[b for b,v in got if not v]
    print("m=%d: %d clean points from %d tries | on vanishing stratum %d | OFF %d"%(
        m,len(got),tried,nvan,len(off)),flush=True)
    out["m%d"%m]=dict(n=len(got),tried=tried,n_van=nvan,n_off=len(off))
    if off:
        out["m%d_off_example"%m]={str(e):[[str(x) for x in r] for r in v] for e,v in off[0].items()}
    # save all points for downstream use
    out["m%d_points"%m]=[{ "van":v, "bl":{str(e):[[str(x) for x in r] for r in b[e]] for e in b}} for b,v in got]
json.dump(out,open(os.path.join(HERE,"results_hunt.json"),"w"),indent=1)
