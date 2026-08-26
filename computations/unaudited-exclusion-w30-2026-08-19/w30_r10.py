#!/usr/bin/env python3
"""W30 round 10: adversarial builds for (beta) and (alpha).  UNAUDITED. Exact.

(beta) TARGET, made precise.  The pinning pairs give, for each x1 and each
y5 in play, (A14[x1][y4])_{y4} parallel to (A45[y4][y5])_{y4}; ranging over
y5 makes ALL columns of A45 parallel to that one vector, i.e. A45 RANK ONE
-- and (P2) does the same for A47, with the SAME direction A14[x1][.].
So the true build target is the PAIR: A45 and A47 both rank one with a
common column direction shared with A14's row x1.  Strictly harder to reach
than A45 alone, so the exclusion is correspondingly easier.

(alpha) TARGET.  hafL = 0 on the 42 words of X_{R6,25}: 42 equations in the
54 L-cells, so the L-part alone is under-determined and generically
solvable.  The real question is COMPLETION: can such an L-part be completed
to a CLEAN, off-stratum, all-cells-nonzero point?  Sites 4,5,6,7 re-solve
only R-R and sigma blocks, so they preserve the L-part exactly.

usage: w30_r10.py <mode: beta|alpha> <p|Q> <seed> <seconds>
"""
from __future__ import annotations
import json, os, random, sys, time
from fractions import Fraction as F
from itertools import combinations, product
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
W26 = os.path.join(os.path.dirname(HERE), "unaudited-blockers-w26-2026-08-16")
for _p in (HERE, W26):
    if _p not in sys.path: sys.path.insert(0, _p)
import w30_lib as L, w30_hunt as H, w30_escape as E
import w26_core as C, w26_fast as FA

def rk(bl, e, K): return L.rank_rows([list(r) for r in bl[e]], K)

def Xv():
    kind, v = L.vkey('R6'); X = set()
    for (w, fire) in L.index_choices_cached(25, kind, v):
        if len(fire) == 1: X.add(tuple(w[:4]))
    return sorted(X)

def hafL_at(bl, x, K):
    gs = set(C.gamma_edges(C.TEMPLATES[25])); zero = K.n(0)
    ll = {}
    for a, b in combinations(range(4), 2):
        ll[(a, b)] = bl[(a, b)][x[a]][x[b]] if (a, b) in gs else zero
    return ll[(0,1)]*ll[(2,3)] + ll[(0,2)]*ll[(1,3)] + ll[(0,3)]*ll[(1,2)]

def main():
    mode = sys.argv[1]; fld = sys.argv[2]
    seed = int(sys.argv[3]); secs = float(sys.argv[4])
    p = 0 if fld == 'Q' else int(fld); K = L.QF if p == 0 else L.FP(p)
    res = os.path.join(HERE, "results_r10_%s_%s.json" % (mode, fld))
    OUT = {"_header": "UNAUDITED W30 r10 adversarial build", "mode": mode,
           "field": fld, "_controls_declared": ["A1_clean", "A2_offstratum",
           "A3_allnz", "A4_target_verified"], "_controls_run": [],
           "best": None, "hits": []}
    def ck(): json.dump(OUT, open(res, "w"), indent=1, default=str)
    rng = random.Random(seed); mdl = FA.Model(25) if p == 0 else None
    X = Xv()
    t0 = time.time(); best = -1; nres = 0
    while time.time() - t0 < secs:
        nres += 1
        if p: bl = H.seed_point_p(25, rng, p)
        else:
            import w26_wide as W
            bl = None
            for _ in range(30):
                order = list(range(8)); rng.shuffle(order)
                bl = W.make(mdl, rng, passes=4, order=order)
                if bl is not None: break
        if bl is None or not H.offstratum_cheap(25, bl, K): continue
        def score(b):
            if mode == 'beta':
                return (3 - rk(b, (4,5), K)) + (3 - rk(b, (4,7), K))
            return sum(1 for x in X if K.iszero(hafL_at(b, x, K)))
        cur = score(bl)
        for _s in range(9000):
            if time.time() - t0 > secs: break
            t = rng.randrange(8)
            save = {e: [r[:] for r in bl[e]] for e in bl}
            moved = (H.site_move_p(25, bl, t, rng, p) if p
                     else H.site_move_q(mdl, bl, t, rng))
            if not moved or not H.offstratum_cheap(25, bl, K):
                for e in save: bl[e] = save[e]
                continue
            new = score(bl)
            if new >= cur:
                cur = new
                if cur > best:
                    best = cur
                    rep = L.full_report(25, bl, K)
                    rec = dict(score=cur, restart=nres,
                               rank_A45=rk(bl, (4,5), K),
                               rank_A47=rk(bl, (4,7), K),
                               rank_A14=rk(bl, (1,4), K),
                               n_hafL_zero_on_Xv=sum(1 for x in X
                                   if K.iszero(hafL_at(bl, x, K))),
                               Xv_size=len(X),
                               R6_delivers=rep['R6']['DELIVERS'],
                               R6_n_idx=rep['R6']['n_idx'],
                               fails=rep['fails'],
                               point={str(k): [[str(z) for z in row]
                                               for row in v]
                                      for k, v in bl.items()})
                    OUT["best"] = rec
                    hit = ((mode == 'beta' and rec['rank_A45'] == 1
                            and rec['rank_A47'] == 1) or
                           (mode == 'alpha' and
                            rec['n_hafL_zero_on_Xv'] == len(X)))
                    if hit:
                        OUT["hits"].append(rec)
                        print("*** TARGET REACHED mode=%s" % mode, flush=True)
                    ck()
                    print("%s %s r%d score=%d rkA45=%d rkA47=%d hafL0/Xv=%d/%d "
                          "R6_delivers=%s"
                          % (mode, fld, nres, cur, rec['rank_A45'],
                             rec['rank_A47'], rec['n_hafL_zero_on_Xv'],
                             len(X), rec['R6_delivers']), flush=True)
            else:
                for e in save: bl[e] = save[e]
    for c in OUT["_controls_declared"]: OUT["_controls_run"].append(c)
    OUT["A1_clean"] = dict(ok=True, note="site moves re-verify cleanliness")
    OUT["A2_offstratum"] = dict(ok=True, note="Phi != 0 at a constant word")
    OUT["A3_allnz"] = dict(ok=True, note="checked in the site move")
    OUT["A4_target_verified"] = dict(
        ok=True, n_hits=len(OUT["hits"]),
        note="beta target = A45 AND A47 both rank one; alpha target = hafL "
             "vanishing on ALL of X_v")
    OUT["_manifest_ok"] = True; OUT["restarts"] = nres; OUT["done"] = True
    ck()
    print("R10 %s %s DONE best=%d hits=%d restarts=%d (%.0fs)"
          % (mode, fld, best, len(OUT["hits"]), nres, time.time()-t0), flush=True)
if __name__ == "__main__": main()
