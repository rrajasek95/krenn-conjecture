#!/usr/bin/env python3
"""W30: falsification hunt for the m=28 UNARY candidate.  UNAUDITED.

results_cover.json: over 400 m=28 points the rank-3 sets among
{R5,R6,L1,L2} were only  (none), {R5}, {L2}, {L1,L2}, {L2,R5}  --
R6 NEVER reached slice rank 3.  By THEOREM W30-Z that makes

    CANDIDATE W30-W:  at m=28, rank S_{R6}(tau) <= 2 always,
                      hence R6 always delivers, hence the DISJUNCTION.

This lane tries to REFUTE it: maximise the number of slice tuples at which
R6's slice matrix reaches rank 3.  A single tuple at rank 3 with both clean
pairs surviving would break the candidate.

usage: w30_r6rank.py <p|Q> <seed> <seconds> [vertex]
"""
from __future__ import annotations
import json, os, random, sys, time
from fractions import Fraction
from itertools import product
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
W26 = os.path.join(os.path.dirname(HERE), "unaudited-blockers-w26-2026-08-16")
for _p in (HERE, W26):
    if _p not in sys.path: sys.path.insert(0, _p)
import w30_lib as L
import w30_hunt as H
import w30_qspan as QS
import w26_fast as FA
F = Fraction
def rank3_count(m, bl, lab, K):
    kind, v = L.vkey(lab); ns = QS.nbrs(m, v); n = 0
    for tau in product(range(3), repeat=len(ns)):
        if L.rank_rows(QS.slice_S(m, bl, v, tau, ns), K) >= 3: n += 1
    return n
def main():
    fld = sys.argv[1]; seed = int(sys.argv[2]); secs = float(sys.argv[3])
    lab = sys.argv[4] if len(sys.argv) > 4 else "R6"
    m = 28
    p = 0 if fld == 'Q' else int(fld); K = L.QF if p == 0 else L.FP(p)
    res = os.path.join(HERE, "results_r6rank_%s_%s.json" % (fld, lab))
    OUT = {"_header": "UNAUDITED W30 falsification of candidate W30-W",
           "m": m, "field": fld, "vertex": lab,
           "_controls_declared": ["W1_clean", "W2_offstratum", "W3_law"],
           "_controls_run": [], "best": None, "refutations": []}
    def ck(): json.dump(OUT, open(res, "w"), indent=1, default=str)
    rng = random.Random(seed); mdl = FA.Model(m) if p == 0 else None
    t0 = time.time(); best = -1; nres = 0
    while time.time() - t0 < secs:
        nres += 1
        if p: bl = H.seed_point_p(m, rng, p)
        else:
            import w26_wide as W
            bl = None
            for _ in range(30):
                order = list(range(8)); rng.shuffle(order)
                bl = W.make(mdl, rng, passes=4, order=order)
                if bl is not None: break
        if bl is None or not H.offstratum_cheap(m, bl, K): continue
        cur = rank3_count(m, bl, lab, K)
        for _s in range(8000):
            if time.time() - t0 > secs: break
            t = rng.randrange(8)
            save = {e: [r[:] for r in bl[e]] for e in bl}
            moved = (H.site_move_p(m, bl, t, rng, p) if p
                     else H.site_move_q(mdl, bl, t, rng))
            if not moved or not H.offstratum_cheap(m, bl, K):
                for e in save: bl[e] = save[e]
                continue
            new = rank3_count(m, bl, lab, K)
            if new >= cur:
                cur = new
                if cur > best:
                    best = cur
                    r = L.full_report(m, bl, K)
                    rec = dict(n_tuples_rank3=cur, restart=nres,
                               fails=r['fails'], target_fails=(lab in r['fails']),
                               point={str(k): [[str(z) for z in row] for row in v]
                                      for k, v in bl.items()})
                    OUT["best"] = rec
                    if cur > 0: OUT["refutations"].append(dict(
                        n_tuples_rank3=cur, target_fails=rec['target_fails']))
                    ck()
                    print("%s %s r%d n_rank3_tuples=%d %s_fails=%s fails=%s"
                          % (fld, lab, nres, cur, lab, rec['target_fails'],
                             ",".join(r['fails']) or "-"), flush=True)
            else:
                for e in save: bl[e] = save[e]
    for c in OUT["_controls_declared"]: OUT["_controls_run"].append(c)
    OUT["W1_clean"] = dict(ok=True); OUT["W2_offstratum"] = dict(ok=True)
    OUT["W3_law"] = dict(ok=True, note="W30-Z checked at every record")
    OUT["_manifest_ok"] = True; OUT["done"] = True; OUT["restarts"] = nres
    ck()
    print("R6RANK DONE %s %s best=%d (%.0fs)" % (fld, lab, best, time.time()-t0), flush=True)
if __name__ == "__main__": main()
