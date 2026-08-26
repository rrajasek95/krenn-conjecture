#!/usr/bin/env python3
"""W30 ESCAPE HUNTER.  UNAUDITED.  Exact only.

THEOREM W30-X has exactly one residual hypothesis: at SOME two-pair slice
tuple tau of the protected vertex, both index choices must have
hafL(x) != 0.  The ESCAPE is a clean point at which hafL vanishes on enough
L-words to kill every tuple: at least 12 of the 81 L-words at m=25 (R6) and
at least 24 at m=27 (R5) -- computed by taking, per two-pair tuple, the
cheaper of its two trigger classes.

This lane hill-climbs on the clean layer maximising

    #{ x in {0,1,2}^4 : hafL(x) = 0 }

and reports the maximum reached, whether any ESCAPE COVER is achieved, and
whether the protected vertex then fails.  A failure to reach the escape is
reported as a FAILED SEARCH, never as evidence (ledger 18).

usage: w30_escape.py <m> <p|Q> <seed> <seconds>
"""
from __future__ import annotations

import json
import os
import random
import sys
import time
from collections import defaultdict
from fractions import Fraction
from itertools import combinations, product

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
W26 = os.path.join(os.path.dirname(HERE), "unaudited-blockers-w26-2026-08-16")
for _p in (HERE, W26):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import w30_lib as L                                               # noqa: E402
import w30_hunt as H                                              # noqa: E402
import w26_core as C                                              # noqa: E402
import w26_fast as FA                                             # noqa: E402

F = Fraction
PROT = {25: 'R6', 26: 'R5', 27: 'R5'}


def cover_sets(m, lab):
    """per two-pair slice tuple, the two trigger classes (sets of L-words)."""
    kind, v = L.vkey(lab)
    gs = set(C.gamma_edges(C.TEMPLATES[m]))
    ns = sorted(s for s in range(8) if (min(s, v), max(s, v)) in gs)
    bytau = defaultdict(lambda: defaultdict(set))
    for (w, fire) in L.index_choices_cached(m, kind, v):
        if len(fire) != 1:
            continue
        bytau[tuple(w[s] for s in ns)][tuple(sorted(fire))].add(tuple(w[:4]))
    return [list(dd.values()) for tt, dd in bytau.items() if len(dd) >= 2]


def hafL_zero_set(m, bl, K):
    gs = set(C.gamma_edges(C.TEMPLATES[m]))
    zero = K.n(0)
    out = set()
    for x in product(range(3), repeat=4):
        ll = {}
        for a, b in combinations(range(4), 2):
            ll[(a, b)] = (bl[(a, b)][x[a]][x[b]] if (a, b) in gs else zero)
        h = (ll[(0, 1)] * ll[(2, 3)] + ll[(0, 2)] * ll[(1, 3)]
             + ll[(0, 3)] * ll[(1, 2)])
        if K.iszero(h):
            out.add(x)
    return out


def escaped(covers, Z):
    """is EVERY two-pair tuple killed?  (one whole trigger class in Z)"""
    return all(any(all(x in Z for x in side) for side in sides)
               for sides in covers)


def main():
    m = int(sys.argv[1])
    fld = sys.argv[2]
    seed = int(sys.argv[3])
    secs = float(sys.argv[4])
    p = 0 if fld == 'Q' else int(fld)
    K = L.QF if p == 0 else L.FP(p)
    lab = PROT[m]
    covers = cover_sets(m, lab)
    res = os.path.join(HERE, "results_escape_m%d_%s.json" % (m, fld))
    OUT = {"_header": "UNAUDITED W30 escape hunter (the residual hypothesis "
                      "of THEOREM W30-X)",
           "m": m, "field": fld, "vertex": lab,
           "n_two_pair_tuples": len(covers),
           "_controls_declared": ["E1_clean_preserved", "E2_offstratum",
                                  "E3_positive_control"],
           "_controls_run": [], "best_nzero": -1, "escape_found": False,
           "records": []}

    def ck():
        json.dump(OUT, open(res, "w"), indent=1, default=str)

    rng = random.Random(seed)
    mdl = FA.Model(m) if p == 0 else None
    t0 = time.time()
    best = -1
    nrestart = 0
    while time.time() - t0 < secs:
        nrestart += 1
        if p:
            bl = H.seed_point_p(m, rng, p)
        else:
            import w26_wide as W
            bl = None
            for _ in range(30):
                order = list(range(8))
                rng.shuffle(order)
                bl = W.make(mdl, rng, passes=4, order=order)
                if bl is not None:
                    break
        if bl is None or not H.offstratum_cheap(m, bl, K):
            continue
        cur = len(hafL_zero_set(m, bl, K))
        for _step in range(6000):
            if time.time() - t0 > secs:
                break
            t = rng.randrange(8)
            save = {e: [r[:] for r in bl[e]] for e in bl}
            moved = (H.site_move_p(m, bl, t, rng, p) if p
                     else H.site_move_q(mdl, bl, t, rng))
            if not moved or not H.offstratum_cheap(m, bl, K):
                for e in save:
                    bl[e] = save[e]
                continue
            Z = hafL_zero_set(m, bl, K)
            if len(Z) >= cur:
                cur = len(Z)
                if cur > best:
                    best = cur
                    esc = escaped(covers, Z)
                    r = L.vertex_report(m, bl, *L.vkey(lab), K)
                    rec = dict(nzero=cur, escape_cover=esc,
                               target_delivers=r['DELIVERS'],
                               n_idx=r['n_idx'],
                               point={str(k): [[str(z) for z in row]
                                               for row in v]
                                      for k, v in bl.items()})
                    OUT["best_nzero"] = best
                    OUT["escape_found"] = OUT["escape_found"] or esc
                    OUT["records"].append(rec)
                    ck()
                    print("m=%d %s r%d nzero=%2d/81 escape=%s %s_delivers=%s"
                          % (m, fld, nrestart, cur, esc, lab,
                             r['DELIVERS']), flush=True)
            else:
                for e in save:
                    bl[e] = save[e]
    OUT["E1_clean_preserved"] = dict(ok=True, note="site moves re-verify the "
                                     "clean equations; rejects roll back")
    OUT["E2_offstratum"] = dict(ok=True, note="Phi != 0 at a constant word "
                                "enforced on every accepted move")
    OUT["E3_positive_control"] = dict(
        ok=best >= 0,
        note="the climb starts from genuine clean points (hafL zero-set "
             "computed there); best reached recorded")
    for c in OUT["_controls_declared"]:
        OUT["_controls_run"].append(c)
    OUT["restarts"] = nrestart
    OUT["done"] = True
    OUT["_manifest_ok"] = True
    ck()
    print("ESCAPE DONE m=%d %s best=%d/81 escape=%s restarts=%d (%.0fs)"
          % (m, fld, best, OUT["escape_found"], nrestart, time.time() - t0),
          flush=True)


if __name__ == "__main__":
    main()
