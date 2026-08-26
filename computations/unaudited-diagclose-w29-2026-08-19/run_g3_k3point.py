#!/usr/bin/env python3
"""W29 G3 -- the k=3 NOT-UNIT control discharged by an EXPLICIT EXACT POINT.

The mandated control is "any formulation that returns unit at k = 3 is wrong".
The Groebner route timed out, so discharge it the way ledger 13 prescribes
instead: exhibit an exact rational point of the k = 3 case ideal.  The three
pairwise disjoint perfect matchings of K_8 are an exact X_3 diagonal source;
solve at each site z, relabel to the W29-B2 normal form, and evaluate EVERY
generator of the corresponding T1i k=3 case ideal (Rabinowitsch form) at it.
All must vanish -- so that ideal is provably NOT the unit ideal.
"""
import json, sys
from fractions import Fraction
BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-diagclose-w29-2026-08-19")
sys.path.insert(0, BASE)
import w29_core as C
import w29_t1i as T
import run_c2_unified as U
import run_g1_x3control as G1
OUT = f"{BASE}/results_g3_k3point.json"
RES = {"per_site": {}}
ts, idx = G1.structured_x3()
assert ts is not None and not G1.x3_violations(ts)
RES["x3_source"] = {c: [list(e) for e in ts[c]] for c in range(3)}
N = 8
allok = True
for z in range(N):
    co = U.case_of(ts, N, z, kmax=3)
    if co is None:
        RES["per_site"][z] = {"normal_form": False}; allok = False; continue
    ts2 = U.relabel(ts, co["perm"])
    Rs = tuple(tuple(x) for x in co["Rs"])
    case = T.Case(Rs, kmax=3, norm=False)
    # background on V' = {0..6} and the star x^c_y = t^c_{z y}, z relabelled 7
    vals = [Fraction(0)] * case.nv
    bg = [{}, {}, {}]
    for c in range(3):
        for (a, b), v in ts2[c].items():
            if 7 in (a, b):
                y = a if b == 7 else b
                if (c, y) in case.xpos:
                    vals[case.xpos[(c, y)]] = v
            else:
                vals[T.widx(c, (a, b))] = v
                bg[c][(a, b)] = v
    for c in range(3):
        h = C.haf(bg[c], tuple(x for x in range(7) if x != c))
        xv = ts2[c].get(C.ekey(7, c), Fraction(0))
        if c in case.rpos:
            vals[case.rpos[c]] = Fraction(1) / (h * xv) if h * xv else 0
    bad = {}
    for (tag, g) in case.build():
        v = g.subs_num(vals)
        if v != 0:
            bad[tag[0]] = bad.get(tag[0], 0) + 1
    RES["per_site"][z] = {"normal_form": True, "Rs": co["Rs"],
                          "n_gens": len(case.build()), "violated": bad,
                          "PASS": not bad}
    if bad: allok = False
    print(f"  [z={z}] Rs={co['Rs']}: {len(case.build())} generators, "
          f"violated {bad or 0} (want 0)", flush=True)
RES["PASS"] = allok
RES["CONCLUSION"] = ("the T1i k=3 case ideal has an explicit exact rational "
                     "point at every solve site -- it is NOT the unit ideal, "
                     "so the formulation is calibrated" if allok else
                     "control FAILED")
json.dump(RES, open(OUT, "w"), indent=1, default=str)
print(">>> " + RES["CONCLUSION"])
