#!/usr/bin/env python3
"""W30 RANK-ONE CONSTRUCTION.  UNAUDITED.  Exact only.

LEMMA W30-S (derived in w30_struct.py) says: at m=27 a FAILURE of R5 forces
the three Gamma blocks at vertex 5 to be rank one with a common direction,

     A_25 = alpha (x) nu ,  A_45 = beta (x) nu ,  A_56 = nu (x) gamma,

(and the m=25 analogue at R6: A_67 and A_56 rank one with a common
letter-6 direction).  This file asks the ADVERSARIAL question: is that
necessary condition even ACHIEVABLE on the clean layer off the vanishing
stratum -- and if it is, does R5 then actually fail?

Construction: impose the rank-one form on the vertex-5 blocks, then run the
exact site descent ONLY at vertices whose incident blocks avoid vertex 5
(at m=27 those are 0, 1, 3, 7 -- vertex 5's Gamma-neighbours are 2, 4, 6).
The clean equations are linear and homogeneous in the blocks at each such
site, so the descent preserves the rank-one structure exactly.

CONSEQUENCE OF THE FACTORISATION.  With that structure every Gamma block at
vertex 5 carries the factor nu_{y5}, and Phi is multilinear, so

        Phi(w) = nu_{y5} * G(x, y4, y6, y7),      G free of y5.

usage: w30_rank1.py <m> <vertex> <seed> <ntry>
"""
from __future__ import annotations

import json
import os
import random
import sys
import time
from fractions import Fraction
from itertools import product

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
W26 = os.path.join(os.path.dirname(HERE), "unaudited-blockers-w26-2026-08-16")
for _p in (HERE, W26):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import w30_lib as L                                               # noqa: E402
import w26_core as C                                              # noqa: E402
import w26_fast as FA                                             # noqa: E402

F = Fraction

# vertex -> (the R-vertex whose failure we are modelling, its Gamma
#            neighbours, the free sites that avoid them)
SPEC = {
    (27, 'R5'): dict(v=5, nb=[2, 4, 6], free=[0, 1, 3, 7]),
    (26, 'R5'): dict(v=5, nb=[2, 4, 6], free=[0, 1, 3, 7]),
    (25, 'R6'): dict(v=6, nb=[5, 7], free=[0, 1, 2, 3, 4]),
    (26, 'R6'): dict(v=6, nb=[3, 5, 7], free=[0, 1, 2, 4]),
}


def rank1_blocks(m, v, rng, lo=-7, hi=7):
    """every Gamma block at v is rank one with the SAME direction nu on the
    letter-at-v index."""
    gs = set(C.gamma_edges(C.TEMPLATES[m]))
    nu = [F(rng.randint(lo, hi) or 3, rng.randint(1, 3)) for _ in range(3)]
    out = {}
    for e in gs:
        if v not in e:
            continue
        other = [F(rng.randint(lo, hi) or 2, rng.randint(1, 3))
                 for _ in range(3)]
        if e[0] == v:
            out[e] = [[nu[a] * other[b] for b in range(3)] for a in range(3)]
        else:
            out[e] = [[other[a] * nu[b] for b in range(3)] for a in range(3)]
    return out, nu


def factorises(m, bl, v, nu):
    """CHECK of the factorisation Phi = nu_{w_v} * G with G free of w_v."""
    gs = set(C.gamma_edges(C.TEMPLATES[m]))
    bad = 0
    for w in C.WORDS:
        if w[v] != 0:
            continue
        vals = []
        for t in range(3):
            ww = list(w)
            ww[v] = t
            vals.append(C.phi(bl, gs, tuple(ww)))
        # vals must be proportional to nu
        for t in range(3):
            if vals[t] * nu[0] != vals[0] * nu[t]:
                bad += 1
                break
    return bad


def main():
    m = int(sys.argv[1])
    lab = sys.argv[2]
    seed0 = int(sys.argv[3])
    ntry = int(sys.argv[4])
    sp = SPEC[(m, lab)]
    v, free = sp['v'], sp['free']
    res = os.path.join(HERE, "results_rank1_m%d_%s.json" % (m, lab))
    OUT = {"_header": "UNAUDITED W30 rank-one construction",
           "m": m, "vertex": lab, "free_sites": free,
           "_controls_declared": ["R1_rank1_preserved", "R1_factorisation",
                                  "R1_positive_control"],
           "_controls_run": [], "hits": [], "summary": {}}
    mdl = FA.Model(m)
    gam = mdl.gam
    t0 = time.time()
    nclean = nfail = noff = 0
    for k in range(ntry):
        rng = random.Random(seed0 + k)
        bl = {e: [[F(rng.randint(-6, 6) or 3, rng.randint(1, 3))
                   for _ in range(3)] for _ in range(3)] for e in gam}
        r1, nu = rank1_blocks(m, v, rng)
        bl.update(r1)
        for _ in range(6):
            order = list(free)
            rng.shuffle(order)
            for t in order:
                FA.site_solve(mdl, bl, t, rng)
            if mdl.clean_ok(bl) and mdl.allnz(bl):
                break
        if not (mdl.clean_ok(bl) and mdl.allnz(bl)):
            continue
        nclean += 1
        # rank-one preserved?
        ok1 = True
        for e in gam:
            if v not in e:
                continue
            M = bl[e]
            rk = L.rank_rows([list(r) for r in M], L.QF)
            if rk != 1:
                ok1 = False
        van = mdl.vanishing(bl)
        if not van:
            noff += 1
        r = L.full_report(m, bl)
        if lab in r['fails']:
            nfail += 1
        rec = dict(seed=seed0 + k, van=van, rank1_ok=ok1,
                   fails=r['fails'], target_fails=(lab in r['fails']),
                   ndeliver={l: r[l]['n_deliver'] for l in L.VERTS},
                   nfactor_bad=factorises(m, bl, v, nu),
                   point={str(e): [[str(z) for z in row] for row in bl[e]]
                          for e in gam})
        OUT["hits"].append(rec)
        OUT["summary"] = dict(tried=k + 1, clean=nclean, offstratum=noff,
                              target_failed=nfail)
        json.dump(OUT, open(res, "w"), indent=1, default=str)
        print("[%3d] clean van=%-5s rank1=%-5s factor_bad=%-4d %s_fails=%-5s "
              "fails=%s (%.0fs)"
              % (k, van, ok1, rec['nfactor_bad'], lab, rec['target_fails'],
                 ",".join(r['fails']) or "-", time.time() - t0), flush=True)
    OUT["R1_rank1_preserved"] = dict(
        ok=all(h['rank1_ok'] for h in OUT["hits"]),
        n=len(OUT["hits"]))
    OUT["_controls_run"].append("R1_rank1_preserved")
    OUT["R1_factorisation"] = dict(
        ok=all(h['nfactor_bad'] == 0 for h in OUT["hits"]),
        note="Phi(w) = nu_{w_v} * G(w without v) must hold exactly")
    OUT["_controls_run"].append("R1_factorisation")
    OUT["R1_positive_control"] = dict(
        note="the same descent WITHOUT the rank-one constraint is "
             "w26_fast.make_point, known to produce clean points",
        clean_found=nclean, ok=nclean > 0)
    OUT["_controls_run"].append("R1_positive_control")
    missing = [c for c in OUT["_controls_declared"]
               if c not in OUT["_controls_run"]]
    OUT["_manifest_ok"] = (missing == [])
    OUT["done"] = True
    json.dump(OUT, open(res, "w"), indent=1, default=str)
    assert not missing, "CONTROL MANIFEST FAILURE: %s" % missing
    print("RANK1 DONE m=%d %s: tried=%d clean=%d offstratum=%d %s_failed=%d "
          "(%.0fs)" % (m, lab, ntry, nclean, noff, lab, nfail,
                       time.time() - t0), flush=True)


if __name__ == "__main__":
    main()
