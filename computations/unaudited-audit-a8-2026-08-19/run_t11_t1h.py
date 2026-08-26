#!/usr/bin/env python3
"""A8 T11 -- the pending T1h ideal, re-derived and re-encoded independently.

THE REDUCTION (re-derived here, not taken from W28).  Let A be an X_4 point at
N = 8 whose K_7 background at the solve site z is monochrome-diagonal.  By
W28-DEC the colour-c system reduces to the 7 unknowns x^{(c)}_y, and

    sum_{y in V'} haf(t^c | V' - y) x^{(c)}_y = 1                    (constant)
    haf(t^d|S1) haf(t^e|S2) * x^{(c)}_y = 0     ({d,e} = {0,1,2} - c,
                                                 (S1,S2) an even split of V'-y)

The constant equation needs a y with BOTH x^{(c)}_y != 0 AND
haf(t^c|V'-y) != 0.  Call it y_c.  Then

  (i)  haf(t^d|S1) haf(t^e|S2) = 0  for EVERY even split of V' - y_c;
  (ii) haf(t^c | V' - y_c) != 0.

y_0, y_1, y_2 are pairwise distinct: (i) at y_c with (S1,S2) = (V'-y_c, empty)
gives haf(t^d | V' - y_c) = 0, contradicting (ii) for colour d.  The
UNRESTRICTED diagonal family is invariant under S_7 acting on sites with
TRIVIAL colour action, so we may relabel y_0,y_1,y_2 = 0,1,2 -- and that orbit
reduction IS sound here (unlike on the sigma slice, where the colour action is
nontrivial).  Hence

    the whole diagonal-background family is killed  <=>  1 is in
      < haf(t^d|S1) haf(t^e|S2) : c, (S1,S2) an even split of V' - c >
    + < zt_c * haf(t^c|V' - c) - 1 : c = 0,1,2 >

in 63 + 3 variables.  Only the (6,2,0) and (4,2,2) word shapes are used.

argv: <kmax> <char> <timeout>
"""
import json
import sys
import time
from itertools import combinations

BASE = "/Users/rishi/workplace/krenn-conjecture/computations/unaudited-audit-a8-2026-08-19"
sys.path.insert(0, BASE)
import a8_sym as S
from a8_sing import decide_unit

kmax = int(sys.argv[1]) if len(sys.argv) > 1 else 4
CH = int(sys.argv[2]) if len(sys.argv) > 2 else 0
TMO = int(sys.argv[3]) if len(sys.argv) > 3 else 3600
METHOD = sys.argv[4] if len(sys.argv) > 4 else "std"
YS = (0, 1, 2)
NP = 63
nv = NP + 3
t = S.full_t(nvar=nv)
VP = S.VP


def lift(p):
    return p


gens, tags = [], []
for c in range(3):
    d, e = [x for x in range(3) if x != c]
    y = YS[c]
    W = tuple(x for x in VP if x != y)
    for (S1, S2) in S.even_splits(W):
        if S.offcount8(S.word8(S1, S2)) > kmax:
            continue
        g = S.haf_poly(t[d], S1, nv) * S.haf_poly(t[e], S2, nv)
        if g:
            gens.append(g)
            tags.append(("FREE", c, y, S1, S2))
for c in range(3):
    W = tuple(x for x in VP if x != YS[c])
    g = S.haf_poly(t[c], W, nv) * S.P.var(nv, NP + c) - S.P.const(nv, 1)
    gens.append(g)
    tags.append(("RAB", c))

used = sorted({i for p in gens for k in p.t for i, ex in enumerate(k) if ex})
ridx = {v: i for i, v in enumerate(used)}
nvc = len(used)
names = []
EPl = S.EP
for v in used:
    if v < NP:
        c, ei = divmod(v, 21)
        names.append(f"zzt{c}_{EPl[ei][0]}{EPl[ei][1]}")
    else:
        names.append(f"zzr{v - NP}")


def squash(p):
    return S.P(nvc, {tuple(k[v] for v in used): val for k, val in p.t.items()})


polys = [squash(p).to_singular(names) for p in gens]
print(f"T1h k={kmax}: {len(gens)} generators, {nv} -> {nvc} variables, "
      f"char {CH}, method {METHOD}", flush=True)
t0 = time.time()
r = decide_unit(names, polys, char=CH, timeout=TMO, method=METHOD)
print(f"   -> {r} ({time.time()-t0:.0f}s)", flush=True)
out = dict(kmax=kmax, char=CH, method=METHOD, ngens=len(gens), nvars=nvc,
           result=r, seconds=round(time.time() - t0, 1),
           reduction_soundness="re-derived independently; the S_7 relabelling "
                               "is sound because the unrestricted diagonal "
                               "family has trivial colour action")
with open(f"{BASE}/results_t11_t1h_k{kmax}_c{CH}_{METHOD}.json", "w") as fh:
    json.dump(out, fh, indent=1, default=str)
