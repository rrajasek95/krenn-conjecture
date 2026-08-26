#!/usr/bin/env python3
"""W26 -- control: phi_fast == phi (from-the-definition).  UNAUDITED."""
import sys, os, random, json
from fractions import Fraction
sys.dont_write_bytecode=True
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
import w26_core as C, w26_fast as F
rng=random.Random(777); bad=tot=0
for m in (25,26,27,28):
    gam=C.gamma_edges(C.TEMPLATES[m]); gs=set(gam)
    for _ in range(4):
        bl={e:[[Fraction(rng.randint(-9,9) or 5,rng.randint(1,4)) for _ in range(3)] for _ in range(3)] for e in gam}
        for _k in range(250):
            w=tuple(rng.randrange(3) for _ in range(8)); tot+=1
            bad += (F.phi_fast(bl,m,w)!=C.phi(bl,gs,w))
print("phi_fast vs phi: %d/%d mismatches"%(bad,tot))
# mutation: drop the T=empty term
bad2=0
for _ in range(2):
    m=27; gam=C.gamma_edges(C.TEMPLATES[m]); gs=set(gam)
    bl={e:[[Fraction(rng.randint(-9,9) or 5,rng.randint(1,4)) for _ in range(3)] for _ in range(3)] for e in gam}
    for _k in range(60):
        w=tuple(rng.randrange(3) for _ in range(8))
        x,y=w[:4],w[4:]
        D=[bl[(p,C.SIG[p])][x[p]][y[C.SIG[p]-4]] for p in range(4)]
        bad2 += ((F.phi_fast(bl,m,w)-D[0]*D[1]*D[2]*D[3])!=C.phi(bl,gs,w))
print("MUTATION (drop T=empty term): fails %d/120 (want ~120)"%bad2)
json.dump({"phi_fast_mismatch":bad,"tests":tot,"mutation_fails":bad2},
          open(os.path.join(HERE,"results_fastchk.json"),"w"),indent=1)
assert bad==0
