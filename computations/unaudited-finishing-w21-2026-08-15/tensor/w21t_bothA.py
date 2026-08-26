#!/usr/bin/env python3
"""W21-M1-TENSOR -- is 'both reductions in Case A' ever realised at m=28?
UNAUDITED. Exact only.  Case A on BOTH sides is exactly the residual gap."""
import json, os, random, sys
from fractions import Fraction
from itertools import product
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); PAR = os.path.dirname(HERE)
sys.path.insert(0, HERE); sys.path.insert(0, PAR)
import w21_core as K, w21_site as SI, w21_block as B, w21t_core as TT
from w21t_apply import SLOT, to_tensor
from w21t_mirror import full_box_R, N_of

m = 28; T = K.W8_IMMUNE[m]; gam = K.gamma_edges(T); clean = K.clean_words(T)
fbL = B.full_box_words(); fbR = full_box_R()
def profile(bl):
    Ln, Rn, Lf, Rf = set(), set(), set(), set()
    for x in fbL:
        P = B.hafL(bl, x)
        if P == 0: continue
        MT = to_tensor({(i,j): B.M_of(bl,gam,x,i,j,P) for (i,j) in B.LPAIRS})
        Ln.add(sum(1 for p in TT.PAIRS if TT.rank(MT[p]) == 2))
        Lf |= {B.SIG[s-1] for s in TT.any_site_factors(MT)}
    for y in fbR:
        P = B.hafR(bl, gam, y)
        if P == 0: continue
        NT = {(SLOT[i],SLOT[j]): N_of(bl,gam,y,i,j,P) for (i,j) in B.LPAIRS}
        Rn.add(sum(1 for p in TT.PAIRS if TT.rank(NT[p]) == 2))
        Rf |= {s-1 for s in TT.any_site_factors(NT)}
    return sorted(Ln), sorted(Rn), sorted(Lf), sorted(Rf)

out = []; bothA = 0
for seed in range(1, 41):
    rng = random.Random(seed * 977)
    order = list(range(8)); rng.shuffle(order)
    bl = SI.descent(gam, clean, rng, order=order, passes=3)
    if bl is None: continue
    if not all(K.phi_value(bl, gam, w) == 0 for w in clean): continue
    if not all(bl[e][i][j] != 0 for e in gam for i in range(3) for j in range(3)):
        continue
    orig = [t for t in range(8) if K.factors_at(bl, gam, t)]
    Ln, Rn, Lf, Rf = profile(bl)
    ba = (Ln == [6] and Rn == [6])
    bothA += ba
    out.append(dict(seed=seed, original=orig, L_rank2=Ln, R_rank2=Rn,
                    L_fac=Lf, R_fac=Rf, union=sorted(set(Lf)|set(Rf)),
                    union_eq_original=(sorted(set(Lf)|set(Rf)) == orig),
                    both_caseA=ba))
    print("seed %-4d orig=%-16s L#rank2=%-6s R#rank2=%-6s union=%-16s "
          "union==orig:%s bothA:%s" % (seed, orig, Ln, Rn,
          sorted(set(Lf)|set(Rf)), sorted(set(Lf)|set(Rf)) == orig, ba), flush=True)
print("points=%d  both-Case-A=%d  union==original in %d/%d  zero-factoring points=%d"
      % (len(out), bothA, sum(1 for r in out if r["union_eq_original"]), len(out),
         sum(1 for r in out if not r["original"])))
json.dump(out, open(os.path.join(HERE, "results_bothA.json"), "w"), indent=1)
