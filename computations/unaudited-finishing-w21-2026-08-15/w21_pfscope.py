#!/usr/bin/env python3
"""W21 -- SCOPE of the Pfaffian frame: how general is 'Gamma is Pfaffian'?
UNAUDITED.  Exact (GF(2)) only.  A Pfaffian signing exists iff the GF(2)
system 'all perfect matchings get the same sign' is consistent."""
import json, os, random, sys
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import w21_core as K
from itertools import combinations

def is_pf(gam):
    eps, com = K.pfaffian_signing(list(gam))
    return eps is not None

res = {"_header": "UNAUDITED W21 Pfaffian-frame scope. Exact GF(2)."}
# named graphs
named = {
 "C_8": [(0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(6,7),(0,7)],
 "K4+K4+PM (m=28 Gamma)": K.gamma_edges(K.W8_IMMUNE[28]),
 "K_{3,3} + isolated edge": [(0,3),(0,4),(0,5),(1,3),(1,4),(1,5),(2,3),(2,4),(2,5),(6,7)],
 "K_{4,4}": [(i,j) for i in range(4) for j in range(4,8)],
 "K_8": list(combinations(range(8),2)),
 "cube Q_3": [(0,1),(1,2),(2,3),(0,3),(4,5),(5,6),(6,7),(4,7),(0,4),(1,5),(2,6),(3,7)],
 "Petersen-minus (5-reg rand)": None,
}
for name, g in named.items():
    if g is None: continue
    npm = len(K.pms_inside(list(g)))
    res[name] = dict(edges=len(g), n_PM=npm, pfaffian=bool(is_pf(g)))
    print("%-28s |E|=%2d  #PM=%3d  Pfaffian=%s" % (name, len(g), npm, is_pf(g)))
# random sweep by edge count
rng = random.Random(2026)
ALL = list(combinations(range(8),2))
tab = {}
for ne in range(8, 25):
    ok = tot = 0
    for _ in range(400):
        g = rng.sample(ALL, ne)
        if not K.pms_inside(g): continue
        tot += 1
        ok += is_pf(g)
    tab[ne] = dict(sampled_with_a_PM=tot, pfaffian=ok)
    print("  |E|=%2d : %d/%d sampled graphs (with >=1 PM) are Pfaffian" % (ne, ok, tot))
res["random_sweep"] = tab
json.dump(res, open("results_pfscope.json","w"), indent=1, default=str)
