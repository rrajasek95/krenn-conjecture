#!/usr/bin/env python3
"""W24 -- structural dump of the residual linear system at m = 25..28.
UNAUDITED.  Exact only.

For every m we record, POINT-INDEPENDENTLY:
  * Gamma, the twelve singles, |clean words|;
  * the combinatorial degree D(w) of H_w in z (max size of a partial
    matching of active singles whose complement has a Gamma perfect
    matching) -- this is an upper bound for the degree at any point, so
    the "combinatorial k<=1 rows"  D(w) <= 1  are a POINT-INDEPENDENT
    subset of w21_resid's rows.  A proof using only these is stronger.
  * for each such w: which singles appear, and the type
      (k0)  no active single       -> the row is the constant Phi_w
      (k1)  exactly the listed singles appear linearly.
  * the check that 'clean == no active single' (every active single must
    extend to a supported matching).
"""
from __future__ import annotations

import json
import os
import sys
from itertools import combinations

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w24_core as C                                              # noqa: E402


def comb_degree(T, w, gam_set, sing):
    """max |S|, S a partial matching of singles active at w whose
    complement carries a Gamma perfect matching."""
    act = [e for e in sing if w[e[0]] == sing[e][0] and w[e[1]] == sing[e][1]]
    best = 0
    if C.has_pm(gam_set, tuple(range(8))):
        best = 0
    else:
        best = -1                       # no k=0 term at all
    # k = 1
    ones = []
    for e in act:
        rest = tuple(v for v in range(8) if v not in e)
        if C.has_pm(gam_set, rest):
            ones.append(e)
    if ones:
        best = max(best, 1)
    # k >= 2
    kmax = best
    for k in (2, 3, 4):
        found = False
        for S in combinations(act, k):
            vs = [v for e in S for v in e]
            if len(set(vs)) != 2 * k:
                continue
            rest = tuple(v for v in range(8) if v not in set(vs))
            if C.has_pm(gam_set, rest):
                found = True
                break
        if found:
            kmax = k
        else:
            break
    return max(best, kmax), ones, act


def main():
    out = {"_header": "UNAUDITED W24 structural dump of the residual system."}
    for m in (24, 25, 26, 27, 28):
        T = C.TEMPLATES[m]
        gam = C.gamma_edges(T)
        gam_set = set(gam)
        sing = C.single_edges(T)
        clean = C.clean_words(T)
        # verify: every active single extends to a supported matching
        extend_fail = []
        for e in sing:
            rest = tuple(v for v in range(8) if v not in e)
            if not C.has_pm(gam_set, rest):
                extend_fail.append(e)
        hist = {}
        rows = []
        for w in C.MIXED:
            d, ones, act = comb_degree(T, w, gam_set, sing)
            hist[d] = hist.get(d, 0) + 1
            if d <= 1:
                rows.append((w, tuple(sorted(ones)), tuple(sorted(act))))
        # per-single coverage: which words give a row containing z_e
        cover = {str(e): 0 for e in sing}
        solo = {str(e): 0 for e in sing}
        for w, ones, act in rows:
            for e in ones:
                cover[str(e)] += 1
                if len(ones) == 1:
                    solo[str(e)] += 1
        ent = dict(
            m=m,
            gamma=[list(e) for e in gam], n_gamma=len(gam),
            singles={str(e): list(v) for e, v in sing.items()},
            n_singles=len(sing),
            n_clean=len(clean),
            singles_that_do_not_extend=[list(e) for e in extend_fail],
            comb_degree_hist={str(k): v for k, v in sorted(hist.items())},
            n_comb_deg_le1_rows=len(rows),
            n_rows_with_no_variable=sum(1 for _, o, _ in rows if not o),
            per_single_rows=cover,
            per_single_solo_rows=solo,
        )
        out["m%d" % m] = ent
        print("m=%d |Gamma|=%d singles=%d clean=%d degree-hist=%s "
              "deg<=1 rows=%d (const-only %d)"
              % (m, len(gam), len(sing), len(clean),
                 sorted(hist.items()), len(rows),
                 ent["n_rows_with_no_variable"]), flush=True)
        print("   singles that do NOT extend to a supported matching:",
              extend_fail)
        print("   rows containing z_e, per single:")
        for e in sorted(sing):
            print("      %-8s appears in %4d rows, %4d of them SOLO"
                  % (str(e), cover[str(e)], solo[str(e)]))
    json.dump(out, open(os.path.join(HERE, "results_struct.json"), "w"),
              indent=1, default=str)


if __name__ == "__main__":
    main()
