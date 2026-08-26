import os, sys, subprocess, tempfile
HERE=os.path.dirname(os.path.abspath(__file__))
ROOT="/Users/rishi/workplace/krenn-conjecture"
PKG=f"{ROOT}/computations/unaudited-promotion-diag-2026-08-20/certified_package"
CAD=f"{ROOT}/computations/unaudited-hygiene-h1-2026-08-15/tools/cadical/build/cadical"
sys.path[:0]=[HERE, os.path.join(PKG,"encoders"), PKG]
import a9_enc as A, l1_enc as L1, orbit_ledger as LED
from head_laplace_probe import HeadEnc, solve

def sweep(n, z, ys, cls, label, limit=None):
    reps=[t for t,_ in LED.orbit_reps(n)]
    if limit: reps=reps[:limit]
    VP=[x for x in range(n) if x!=z]; Q=[x for x in VP if x not in ys]
    ren=dict(zip(range(3,n-1), Q))
    nu=0
    for Rs in reps:
        Rs2=tuple(tuple(sorted(ren[q] for q in R)) for R in Rs)
        if solve(cls(n,Rs2,k=4,z=z,ys=ys).build())=="UNSAT": nu+=1
    print(f"{label}: {nu}/{len(reps)} UNSAT", flush=True)

# N=8, 20 orbits each, to isolate which restriction breaks it
sweep(8,0,(1,2,3), L1.CanonEnc, "N=8 FULL A3, z=0        ", 20)
sweep(8,7,(0,1,2), HeadEnc,     "N=8 head A3, z=7        ", 20)
sweep(8,7,(0,1,2), L1.CanonEnc, "N=8 FULL A3, z=7 (base) ", 20)
