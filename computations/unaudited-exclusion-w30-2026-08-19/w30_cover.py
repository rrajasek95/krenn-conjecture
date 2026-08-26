#!/usr/bin/env python3
"""W30 COVER / SUBSET ANALYSIS.  UNAUDITED.  Exact combinatorics.

(1) m=28.  By THEOREM W30-Z a two-firing-letter vertex can only FAIL with
    slice rank 3.  The one-firing-letter vertices (R4,R7,L0,L3) fail freely.
    So

        "all eight vertices fail"  ==>  all four of R5,R6,L1,L2 at rank 3,

    and ANY 2-subset exclusion among those four implies the disjunction.
    This computes which 2-subsets have actually been REACHED at rank 3 in
    the corpus, so the elimination targets the smallest statement that is
    still open.

(2) m=25.  The (b) scale escape needs hafL to vanish on a COVER: for each
    of the 6 two-pair slice tuples at R6, one whole trigger class.  This
    enumerates all 2^6 choices, deduplicates the resulting L-word sets, and
    returns the MINIMAL covers -- one small elimination per minimal cover
    beats one 54-variable saturation.
"""
from __future__ import annotations

import glob
import json
import os
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations, product

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
W26 = os.path.join(os.path.dirname(HERE), "unaudited-blockers-w26-2026-08-16")
for _p in (HERE, W26):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import w30_lib as L                                               # noqa: E402
import w30_qspan as QS                                            # noqa: E402
import w30_side as SD                                             # noqa: E402
import w26_core as C                                              # noqa: E402

F = Fraction
RES = os.path.join(HERE, "results_cover.json")
FOUR = ['R5', 'R6', 'L1', 'L2']
DECL = ["C1_rank3_subset_census", "C2_minimal_covers",
        "C3_cover_is_really_a_cover", "C4_negative_control"]


def slice_rank_profile(m, bl, lab, K):
    kind, v = L.vkey(lab)
    ns = QS.nbrs(m, v)
    rs = set()
    for tau in product(range(3), repeat=len(ns)):
        rs.add(L.rank_rows(QS.slice_S(m, bl, v, tau, ns), K))
    return min(rs), max(rs)


def main():
    OUT = {"_header": "UNAUDITED W30 cover / rank-3 subset analysis",
           "_controls_declared": DECL, "_controls_run": []}

    # ---------------------------------------------------- (1) m=28 subsets
    seen = Counter()
    npt = 0
    prof_all = Counter()
    for src in ["points_hunt.json"] + sorted(
            glob.glob(os.path.join(HERE, "results_rank28_*.json"))):
        path = src if os.path.isabs(src) else os.path.join(HERE, src)
        if not os.path.exists(path):
            continue
        d = json.load(open(path))
        pts = d.get("points") or ([d["best"]] if d.get("best") else [])
        for r in pts:
            m = r.get("m", d.get("m", 28))
            if m != 28:
                continue
            p = r.get("p", 0 if d.get("field") == 'Q'
                      else int(d.get("field", 0) or 0))
            K = L.QF if not p else L.FP(p)
            try:
                if p:
                    bl = {eval(k): [[int(z) % p for z in row] for row in v]
                          for k, v in r["point"].items()}
                else:
                    bl = {eval(k): [[F(z) for z in row] for row in v]
                          for k, v in r["point"].items()}
            except Exception:                                # noqa: BLE001
                continue
            prof = {}
            for lab in FOUR:
                lo, hi = slice_rank_profile(28, bl, lab, K)
                prof[lab] = hi
            r3 = frozenset(l for l in FOUR if prof[l] >= 3)
            seen[r3] += 1
            prof_all[tuple(sorted(prof.items()))] += 1
            npt += 1
            if npt >= 400:
                break
        if npt >= 400:
            break
    pairs_reached = set()
    for s in seen:
        for a, b in combinations(sorted(s), 2):
            pairs_reached.add((a, b))
    allpairs = list(combinations(FOUR, 2))
    OUT["C1_rank3_subset_census"] = dict(
        n_points=npt,
        rank3_sets={",".join(sorted(s)) if s else "(none)": c
                    for s, c in seen.items()},
        max_rank3_simultaneous=max((len(s) for s in seen), default=0),
        pairs_reached=["%s|%s" % p for p in sorted(pairs_reached)],
        pairs_NEVER_reached=["%s|%s" % p for p in allpairs
                             if p not in pairs_reached],
        ok=True,
        note="a 2-subset never reached at rank 3 is a candidate exclusion; "
             "proving ANY ONE of them gives the m=28 disjunction")
    OUT["_controls_run"].append("C1_rank3_subset_census")
    print("m=28 rank-3 sets over %d points: %s" % (npt,
          OUT["C1_rank3_subset_census"]["rank3_sets"]), flush=True)
    print("  pairs reached : %s" % OUT["C1_rank3_subset_census"]
          ["pairs_reached"], flush=True)
    print("  pairs NEVER   : %s" % OUT["C1_rank3_subset_census"]
          ["pairs_NEVER_reached"], flush=True)
    json.dump(OUT, open(RES, "w"), indent=1, default=str)

    # ------------------------------------------------- (2) m=25 min covers
    ns, by, two = SD.realisation(25, 'R6')
    tuples = sorted(two.keys())
    opts = [sorted(two[t].items()) for t in tuples]
    covers = {}
    for pick in product(*opts):
        W = frozenset().union(*[frozenset(X) for (_P, X) in pick])
        key = W
        if key not in covers or len(pick) < len(covers[key][1]):
            covers[key] = (len(W), [(list(tuples[i]), list(pick[i][0]))
                                    for i in range(len(tuples))])
    sizes = sorted(len(w) for w in covers)
    minsz = sizes[0] if sizes else 0
    minimal = [w for w in covers if len(w) == minsz]
    # keep only inclusion-minimal covers
    incmin = [w for w in covers
              if not any(w2 < w for w2 in covers)]
    OUT["C2_minimal_covers"] = dict(
        n_two_pair_tuples=len(tuples), n_distinct_covers=len(covers),
        cover_sizes=sorted(set(sizes)),
        min_size=minsz, n_of_min_size=len(minimal),
        n_inclusion_minimal=len(incmin),
        inclusion_minimal_sizes=sorted(len(w) for w in incmin),
        ok=True)
    OUT["_controls_run"].append("C2_minimal_covers")
    print("m=25 R6: %d two-pair tuples, %d distinct covers, sizes %s, "
          "%d inclusion-minimal (sizes %s)"
          % (len(tuples), len(covers), sorted(set(sizes)), len(incmin),
             sorted(len(w) for w in incmin)), flush=True)

    # C3: verify each inclusion-minimal cover really kills every tuple
    bad = 0
    for w in incmin:
        for t in tuples:
            if not any(set(X) <= set(w) for X in two[t].values()):
                bad += 1
    OUT["C3_cover_is_really_a_cover"] = dict(
        violations=bad, ok=(bad == 0),
        note="every inclusion-minimal cover must annihilate a whole trigger "
             "class at EVERY two-pair tuple")
    OUT["_controls_run"].append("C3_cover_is_really_a_cover")
    # C4 negative control: a PROPER SUBSET of a minimal cover must NOT be a
    # cover, else 'minimal' is meaningless.
    negbad = 0
    ntested = 0
    for w in list(incmin)[:4]:
        wl = sorted(w)
        for drop in wl[:6]:
            w2 = set(wl) - {drop}
            ntested += 1
            if all(any(set(X) <= w2 for X in two[t].values())
                   for t in tuples):
                negbad += 1
    OUT["C4_negative_control"] = dict(
        n_tested=ntested, still_covers=negbad, ok=(negbad == 0),
        note="dropping one word from an inclusion-minimal cover must break "
             "the cover property")
    OUT["_controls_run"].append("C4_negative_control")
    OUT["m25_inclusion_minimal_covers"] = [sorted(list(x) for x in w)
                                           for w in incmin[:40]]
    missing = [c for c in DECL if c not in OUT["_controls_run"]]
    OUT["_manifest_ok"] = (missing == [])
    OUT["done"] = True
    json.dump(OUT, open(RES, "w"), indent=1, default=str)
    assert not missing, "CONTROL MANIFEST FAILURE: %s" % missing
    print("C3 cover violations=%d ; C4 subset-still-covers=%d/%d"
          % (bad, negbad, ntested), flush=True)
    print("COVER DONE; manifest %s" % OUT["_controls_run"], flush=True)


if __name__ == "__main__":
    main()
