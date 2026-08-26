#!/usr/bin/env python3
"""A11 adversarial builder (ledger 20) against M25-CONDITIONAL.  UNAUDITED.

Sole purpose: BUILD the object the theorem forbids, or the escape it is
conditional on.  Two targets, scored jointly:

  T-FAIL    a clean, off-stratum, all-cells-nonzero m=25 point at which R6
            FAILS.  That would refute the CONCLUSION.
  T-ESCAPE  a point at which (beta) fails: every untriggered word of every
            live tuple has Q = (B,C) = 0.  That is round 10's exception
            object (the independent family's idx 5 at F_13), which is NOT
            stored on disk and so cannot be re-traced from the corpus.

A failed search is NOT evidence (ledger 18) and is reported as such.
Checkpointed; detached-safe.

usage: a11_t8.py <p> <seconds> <seed>
"""
from __future__ import annotations

import json
import os
import random
import sys
import time
from collections import Counter
from itertools import product

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
W30 = os.path.join(os.path.dirname(HERE), "unaudited-exclusion-w30-2026-08-19")
sys.path.insert(0, HERE)
import a11_lib as A      # noqa: E402
import a11_m25 as M      # noqa: E402

DECL = ["H1_points_are_genuine", "H2_target_fail", "H3_target_escape",
        "H4_failed_search_disclaimer"]


def score(tm, bl, K, unt):
    """(n tuples with rank S' >= 2, n template-untriggered words with Q = 0)"""
    r2 = 0
    for tau in product(range(3), repeat=2):
        if A.rank(A.slice_S(tm, bl, 6, tau, K), K) >= 2:
            r2 += 1
    q0 = 0
    for w in unt:
        B, C = M.BC_closed(tm, bl, w, K)
        if K.iszero(B) and K.iszero(C):
            q0 += 1
    return r2, q0


def main():
    p = int(sys.argv[1])
    secs = float(sys.argv[2])
    seed = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    K = A.Modp(p)
    tm = A.T(25)
    unt = M.untriggered_template(25, 6)
    rng = random.Random(seed)
    res = os.path.join(HERE, "results_t8_p%d.json" % p)
    man = A.Manifest(DECL)
    dat = json.load(open(os.path.join(W30, "points_m25_wide.json")))
    srcs = [r for r in dat["points"] if not r.get("van")]
    t0 = time.time()
    best = (-1, -1)
    bestrec = None
    npts = nfail = nesc = 0
    hits = []
    while time.time() - t0 < secs:
        r0 = srcs[rng.randrange(len(srcs))]
        try:
            bl = A.load_point(r0["point"], K)
        except Exception:
            continue
        order = list(range(8))
        for _ps in range(2):
            rng.shuffle(order)
            for u in order:
                M.site_resolve(25, bl, u, K, rng)
        if not A.all_cells_nonzero(tm, bl, K):
            continue
        if A.n_phi_nonzero(tm, bl, K) == 0:
            continue
        if not A.is_clean_point(tm, bl, K):
            continue
        npts += 1
        sc = score(tm, bl, K, unt)
        ver = A.verdict(tm, bl, 'R6', K)
        if not ver['DELIVERS']:
            nfail += 1
            hits.append(dict(kind="R6_FAILS", seed_from=r0["seed"],
                             point={str(e): [[str(z) for z in row]
                                             for row in bl[e]]
                                    for e in sorted(bl)}))
        if sc[1] == len(unt):
            nesc += 1
            hits.append(dict(kind="FULL_TEMPLATE_ESCAPE", seed_from=r0["seed"],
                             point={str(e): [[str(z) for z in row]
                                             for row in bl[e]]
                                    for e in sorted(bl)}))
        if sc > best:
            best = sc
            bestrec = dict(n_tuples_rank_ge2=sc[0], n_Q_zero=sc[1],
                           n_untriggered_template=len(unt),
                           R6_delivers=ver['DELIVERS'],
                           from_seed=r0["seed"],
                           point={str(e): [[str(z) for z in row]
                                           for row in bl[e]]
                                  for e in sorted(bl)})
            with open(res, "w") as fh:
                json.dump(dict(_header="UNAUDITED A11 adversarial builder",
                               p=p, best=bestrec, n_points=npts,
                               n_R6_failures=nfail, n_escapes=nesc,
                               hits=hits[:4], done=False), fh, indent=1,
                          default=str)
            print("p=%d pts=%d best rank>=2 tuples=%d Q0=%d/%d deliver=%s"
                  % (p, npts, sc[0], sc[1], len(unt), ver['DELIVERS']),
                  flush=True)
    man.record("H1_points_are_genuine", dict(
        n_points=npts, ok=npts > 0,
        note="each point re-verified: clean by raw evaluation at all 2624 "
             "clean words, all Gamma cells nonzero, off the vanishing "
             "stratum"))
    man.record("H2_target_fail", dict(n_R6_failures=nfail, ok=True,
                                      note="R6 FAILING would refute the "
                                           "conclusion of M25-CONDITIONAL"))
    man.record("H3_target_escape", dict(
        n_full_escapes=nesc, best=bestrec, ok=True,
        note="Q = 0 at EVERY template-untriggered word would be the (beta) "
             "escape"))
    man.record("H4_failed_search_disclaimer", dict(
        ok=True,
        note="ledger 18: reaching neither target is a FAILED SEARCH and is "
             "not evidence that either object is unreachable"))
    man.finish(res, extra={"_header": "UNAUDITED A11 adversarial builder",
                           "p": p, "best": bestrec, "n_points": npts,
                           "n_R6_failures": nfail, "n_escapes": nesc,
                           "hits": hits[:4],
                           "elapsed_s": round(time.time() - t0, 1)})
    print("T8 p=%d DONE: %d points, %d R6 failures, %d escapes"
          % (p, npts, nfail, nesc))


if __name__ == "__main__":
    main()
