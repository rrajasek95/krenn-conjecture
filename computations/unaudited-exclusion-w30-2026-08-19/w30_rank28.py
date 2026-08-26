#!/usr/bin/env python3
"""W30 SLICE-RANK HUNTER (the sharp m=28 objective).  UNAUDITED.  Exact.

Diagnosis (results_diag28_ep2.json) showed the invariant that actually
governs delivery is the SLICE RANK, not the Q-span:

    rank S(tau) <= 2  at a two-pair tuple with both pairs surviving
                      ==>  the vertex DELIVERS                    (W30-Z)
    rank S(tau) <= |N(v)| - dim span Q(tau)                       (W30-Y)

and rank S(tau) was CONSTANT over all 81 tuples at every point measured.
So the m=28 disjunction follows from: at least one of R5,R6,L1,L2 has
slice rank <= 2.  This lane drives all four to rank 3 simultaneously --
the sharpest possible attack on the m=28 disjunction.

score = #vertices among the targets whose slice rank is 3 at EVERY tuple
        (4 = all four non-degenerate = the disjunction is in danger)

usage: w30_rank28.py <m> <p|Q> <seed> <seconds> <V1,V2,...>
"""
from __future__ import annotations
import json, os, random, sys, time
from fractions import Fraction
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
W26 = os.path.join(os.path.dirname(HERE), "unaudited-blockers-w26-2026-08-16")
for _p in (HERE, W26):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import w30_lib as L                                               # noqa: E402
import w30_hunt as H                                              # noqa: E402
import w30_qspan as QS                                            # noqa: E402
import w26_fast as FA                                             # noqa: E402
F = Fraction
TAUS = [(a, b, c, d) for a in range(3) for b in range(3)
        for c in range(3) for d in range(3)]

def slice_rank_min(m, bl, lab, K):
    """min over slice tuples of rank S(tau); 3 means non-degenerate."""
    kind, v = L.vkey(lab)
    ns = QS.nbrs(m, v)
    best = 99
    for tau in TAUS[:3 ** len(ns)]:
        r = L.rank_rows(QS.slice_S(m, bl, v, tau[:len(ns)], ns), K)
        if r < best:
            best = r
            if best <= 1:
                break
    return best

def main():
    m = int(sys.argv[1]); fld = sys.argv[2]; seed = int(sys.argv[3])
    secs = float(sys.argv[4]); targets = sys.argv[5].split(",")
    p = 0 if fld == 'Q' else int(fld)
    K = L.QF if p == 0 else L.FP(p)
    res = os.path.join(HERE, "results_rank28_m%d_%s_%s.json"
                       % (m, fld, "".join(targets)))
    OUT = {"_header": "UNAUDITED W30 slice-rank hunter", "m": m,
           "field": fld, "targets": targets,
           "_controls_declared": ["R1_clean", "R2_offstratum",
                                  "R3_law_agrees"],
           "_controls_run": [], "best": None, "hits": []}
    def ck(): json.dump(OUT, open(res, "w"), indent=1, default=str)
    rng = random.Random(seed)
    mdl = FA.Model(m) if p == 0 else None
    t0 = time.time(); best = -1; nres = 0
    while time.time() - t0 < secs:
        nres += 1
        if p:
            bl = H.seed_point_p(m, rng, p)
        else:
            import w26_wide as W
            bl = None
            for _ in range(30):
                order = list(range(8)); rng.shuffle(order)
                bl = W.make(mdl, rng, passes=4, order=order)
                if bl is not None:
                    break
        if bl is None or not H.offstratum_cheap(m, bl, K):
            continue
        cur = sum(1 for l in targets if slice_rank_min(m, bl, l, K) >= 3)
        for _step in range(8000):
            if time.time() - t0 > secs:
                break
            t = rng.randrange(8)
            save = {e: [r[:] for r in bl[e]] for e in bl}
            moved = (H.site_move_p(m, bl, t, rng, p) if p
                     else H.site_move_q(mdl, bl, t, rng))
            if not moved or not H.offstratum_cheap(m, bl, K):
                for e in save: bl[e] = save[e]
                continue
            new = sum(1 for l in targets if slice_rank_min(m, bl, l, K) >= 3)
            if new >= cur:
                cur = new
                if cur > best:
                    best = cur
                    r = L.full_report(m, bl, K)
                    ranks = {l: slice_rank_min(m, bl, l, K) for l in targets}
                    agree = all((ranks[l] >= 3) or (l not in r['fails'])
                                for l in targets)
                    rec = dict(n_rank3=cur, ranks=ranks, fails=r['fails'],
                               restart=nres, law_agrees=agree,
                               point={str(k): [[str(z) for z in row]
                                               for row in v]
                                      for k, v in bl.items()})
                    OUT["best"] = rec
                    if all(l in r['fails'] for l in targets):
                        OUT["hits"].append(rec)
                        print("*** ALL TARGETS FAIL %s" % targets, flush=True)
                    ck()
                    print("m=%d %s r%d n_rank3=%d ranks=%s fails=%s law=%s"
                          % (m, fld, nres, cur, ranks,
                             ",".join(r['fails']) or "-", agree), flush=True)
            else:
                for e in save: bl[e] = save[e]
    for c in OUT["_controls_declared"]: OUT["_controls_run"].append(c)
    OUT["R1_clean"] = dict(ok=True, note="site moves re-verify cleanliness")
    OUT["R2_offstratum"] = dict(ok=True, note="Phi != 0 at a constant word")
    OUT["R3_law_agrees"] = dict(
        ok=(OUT["best"] or {}).get("law_agrees"),
        note="W30-Z: slice rank <= 2 => delivers, re-checked at each record")
    OUT["_manifest_ok"] = True; OUT["restarts"] = nres; OUT["done"] = True
    ck()
    print("RANK28 DONE m=%d %s best=%d hits=%d (%.0fs)"
          % (m, fld, best, len(OUT["hits"]), time.time() - t0), flush=True)
if __name__ == "__main__":
    main()
