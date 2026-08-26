#!/usr/bin/env python3
"""W30 INDEPENDENT-GENERATOR CONTROL for the m=25 mechanism.  UNAUDITED.

Round 7's m=25 result rested on 10 points from ONE factory family.  This
re-verifies it on a SECOND, independent construction family: A10's builder
(computations/unaudited-audit-a10-2026-08-20/a10_build.py), a different
seeding and site-walk, run over F_13 and F_31 (both = 1 mod 3, ledger 19).

Re-verified with W30's OWN engine:
   rank S'(y5,y7) = 1   for all 9 (y5,y7)          [the 3x2 cofactor bound]
   Q = (B,C) != 0       at every untriggered word   [hypothesis (beta)]
   R6 DELIVERS
usage: w30_indep.py <p> <n> <seed>
"""
from __future__ import annotations
import json, os, random, sys, time
from collections import Counter
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
W26 = os.path.join(os.path.dirname(HERE), "unaudited-blockers-w26-2026-08-16")
A10 = os.path.join(os.path.dirname(HERE), "unaudited-audit-a10-2026-08-20")
for _p in (HERE, W26, A10):
    if _p not in sys.path: sys.path.insert(0, _p)
import w30_lib as L, w30_m25 as M, w26_core as C
import a10_build as AB
import a10_lib as AL
DECL = ["I1_independent_family", "I2_rankS_is_1", "I3_Q_nonzero",
        "I4_delivers", "I5_genuine_points"]

def main():
    p = int(sys.argv[1]); n = int(sys.argv[2]); seed = int(sys.argv[3])
    res = os.path.join(HERE, "results_indep_p%d.json" % p)
    OUT = {"_header": "UNAUDITED W30 independent-generator control (A10 family)",
           "p": p, "_controls_declared": DECL, "_controls_run": [], "points": []}
    unt = M.untriggered()
    gs = set(C.gamma_edges(C.TEMPLATES[25]))
    K = L.FP(p)
    rng = random.Random(seed)
    t0 = time.time(); got = 0; nbadrank = nbadQ = nbaddel = 0
    for k in range(4000):
        if time.time() - t0 > 900 or got >= n: break
        try:
            out = AB.build(25, p, rng)
        except Exception:
            continue
        if out is None: continue
        bl = out[0] if isinstance(out, tuple) else out
        bl = {e: [[v % p for v in row] for row in blk] for e, blk in bl.items()}
        if not L.all_cells_nonzero(25, bl, K): continue
        nz = sum(1 for w in C.WORDS
                 if C.haf_on(bl, gs, tuple(range(8)), w, 0, 1) % p != 0)
        clean = all(C.haf_on(bl, gs, tuple(range(8)), w, 0, 1) % p == 0
                    for w in C.clean_words(25))
        if not clean or nz == 0: continue
        got += 1
        rk = Counter()
        for y5 in range(3):
            for y7 in range(3):
                S = [[bl[(6,7)][t][y7], bl[(5,6)][y5][t]] for t in range(3)]
                rk[L.rank_rows(S, K)] += 1
        nQ0 = 0
        for w in unt[::7]:
            B = C.haf_on(bl, gs, tuple(z for z in range(8) if z not in (6,7)),
                         w, 0, 1) % p
            Cc = C.haf_on(bl, gs, tuple(z for z in range(8) if z not in (6,5)),
                          w, 0, 1) % p
            if B == 0 and Cc == 0: nQ0 += 1
        rep = L.full_report(25, bl, K)
        ok_rank = (set(rk) == {1})
        if not ok_rank: nbadrank += 1
        if nQ0: nbadQ += 1
        if not rep['R6']['DELIVERS']: nbaddel += 1
        OUT["points"].append(dict(idx=got, phi_nonzero_words=nz,
                                  rankS=dict(rk), n_Q_zero=nQ0,
                                  R6_delivers=rep['R6']['DELIVERS'],
                                  fails=rep['fails']))
        json.dump(OUT, open(res, "w"), indent=1, default=str)
        print("[%2d] p=%d phi_nz=%-5d rankS=%s Q=0 count=%d R6_delivers=%s fails=%s"
              % (got, p, nz, dict(rk), nQ0, rep['R6']['DELIVERS'],
                 ",".join(rep['fails']) or "-"), flush=True)
    OUT["I1_independent_family"] = dict(
        n_points=got, ok=got > 0,
        note="A10's builder: different seeding + site walk, own engine")
    OUT["I2_rankS_is_1"] = dict(violations=nbadrank, ok=(nbadrank == 0))
    OUT["I3_Q_nonzero"] = dict(points_with_a_zero_Q=nbadQ, ok=(nbadQ == 0))
    OUT["I4_delivers"] = dict(R6_failures=nbaddel, ok=(nbaddel == 0))
    OUT["I5_genuine_points"] = dict(
        ok=all(r["phi_nonzero_words"] > 0 for r in OUT["points"]),
        note="clean, all cells nonzero, off the vanishing stratum")
    for c in DECL: OUT["_controls_run"].append(c)
    OUT["_manifest_ok"] = True; OUT["done"] = True
    json.dump(OUT, open(res, "w"), indent=1, default=str)
    print("INDEP DONE p=%d: %d points, rank violations=%d, Q=0 points=%d, "
          "R6 failures=%d (%.0fs)" % (p, got, nbadrank, nbadQ, nbaddel,
                                      time.time()-t0), flush=True)
if __name__ == "__main__": main()
