#!/usr/bin/env python3
"""W30 CALIBRATION + EXHAUSTIVE RE-CENSUS.  UNAUDITED.  Exact only.

CONTROL C1 (engine agreement, one-sided): W26's analyse() samples 40-60
random ambient words, so its DELIVERS is a SUBSET-disjunction of the
exhaustive one.  The required implication is
        W26 says DELIVERS  ==>  W30 says DELIVERS
and any W30-only deliveries are W26 false failures.  A violation of the
implication is an ENGINE BUG (in one of the two).

CONTROL C2 (mutation): perturb one cell of a point; the per-vertex delivery
vector must change on at least one point, else the test is vacuous.

Then: the exhaustive 8x8 co-failure census over all stored + fresh points.
"""
from __future__ import annotations

import json
import os
import random
import sys
import time
from collections import Counter
from fractions import Fraction
from itertools import combinations

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
W26 = os.path.join(os.path.dirname(HERE), "unaudited-blockers-w26-2026-08-16")
for _p in (HERE, W26):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import w30_lib as L                                               # noqa: E402
import w26_core as C                                              # noqa: E402
import w26_disj as DJ                                             # noqa: E402
import w26_pts as PT                                              # noqa: E402
import w26_fast as FA                                             # noqa: E402
import w26_wide as W                                              # noqa: E402

RES = os.path.join(HERE, "results_cal.json")
OUT = {"_header": "UNAUDITED W30 calibration + exhaustive re-census.",
       "_controls_declared": ["C1_engine_implication", "C2_mutation",
                              "C3_index_choice_coverage"],
       "_controls_run": []}


def ck():
    json.dump(OUT, open(RES, "w"), indent=1, default=str)


def main():
    t0 = time.time()
    # ---------------------------------------------------------- C3 coverage
    cov = {}
    for m in (25, 26, 27, 28):
        cov[m] = {lab: len(L.index_choices_cached(m, *L.vkey(lab)))
                  for lab in L.VERTS}
    OUT["C3_index_choice_coverage"] = cov
    OUT["_controls_run"].append("C3_index_choice_coverage")
    print("C3 admissible index choices per vertex:", flush=True)
    for m in cov:
        print("   m=%d %s" % (m, cov[m]), flush=True)
    ck()

    # ------------------------------------------------- C1 + exhaustive census
    pts = []
    for m, tag, bl in PT.stored_points():
        pts.append((m, "stored:" + str(tag)[:26], bl))
    print("stored points: %d" % len(pts), flush=True)
    # W26's OWN fresh points, regenerated from its recorded seeds -- this
    # makes C1 a DIRECT comparison against W26's recorded verdicts.
    d26 = json.load(open(os.path.join(W26, "results_disj.json")))
    want = {}
    for r in d26.get("fresh", []):
        want.setdefault(r["m"], []).append(int(str(r["tag"])[5:]))
    d26e = json.load(open(os.path.join(W26, "results_excl.json")))
    want2 = {}
    for r in d26e.get("Q_fresh", []):
        want2.setdefault(r["m"], []).append(int(str(r["tag"])[1:]))
    for m in (25, 26, 27, 28):
        mdl = FA.Model(m)
        for kk in want.get(m, []):
            rng = random.Random(31_000_000 + 1000 * m + kk)
            order = list(range(8))
            rng.shuffle(order)
            bl = W.make(mdl, rng, passes=4, order=order)
            if bl is not None:
                pts.append((m, "fresh%d" % kk, bl))
        for kk in want2.get(m, []):
            rng = random.Random(52_000_000 + 1000 * m + kk)
            order = list(range(8))
            rng.shuffle(order)
            bl = W.make(mdl, rng, passes=4, order=order)
            if bl is not None:
                pts.append((m, "q%d" % kk, bl))
    print("total points: %d  (%.1fs)" % (len(pts), time.time() - t0),
          flush=True)

    recs = []
    viol = []
    for i, (m, tag, bl) in enumerate(pts):
        r26 = DJ.analyse(m, bl)          # W26's own defaults (nsample=40)
        r30 = L.full_report(m, bl)
        d26 = {l: r26[l]['DELIVERS'] for l in L.VERTS}
        d30 = {l: r30[l]['DELIVERS'] for l in L.VERTS}
        bad = [l for l in L.VERTS if d26[l] and not d30[l]]
        if bad:
            viol.append(dict(m=m, tag=tag, vertices=bad))
        rec = dict(m=m, tag=tag,
                   fails30=r30['fails'],
                   fails26=[l for l in L.VERTS if not d26[l]],
                   disj=r30['DISJUNCTION_holds'],
                   nidx={l: r30[l]['n_idx'] for l in L.VERTS},
                   ndel={l: r30[l]['n_deliver'] for l in L.VERTS})
        recs.append(rec)
        if i % 10 == 0:
            print("  [%3d/%3d] m=%d %-28s fails30=%-22s fails26=%s (%.0fs)"
                  % (i, len(pts), m, tag[:28], ",".join(rec['fails30']) or "-",
                     ",".join(rec['fails26']) or "-", time.time() - t0),
                  flush=True)
            OUT["points"] = recs
            ck()
    OUT["points"] = recs
    OUT["C1_engine_implication"] = dict(
        n_points=len(recs), violations=viol, ok=(len(viol) == 0))
    OUT["_controls_run"].append("C1_engine_implication")
    print("C1: %d points, %d violations of (W26 delivers => W30 delivers)"
          % (len(recs), len(viol)), flush=True)
    ck()

    # -------------------------------------------------------- the 8x8 census
    def census(rr, tag):
        pat = Counter()
        co = Counter()
        solo = Counter()
        for r in rr:
            f = tuple(r['fails30'])
            pat[f] += 1
            for l in f:
                solo[l] += 1
            for a, b in combinations(f, 2):
                co[tuple(sorted((a, b)))] += 1
        return dict(tag=tag, n=len(rr), per_vertex=dict(solo),
                    co_failures={"%s|%s" % k: v for k, v in co.items()},
                    never_together=["%s|%s" % p for p in
                                    combinations(sorted(L.VERTS), 2)
                                    if co[p] == 0],
                    max_simultaneous=max((len(k) for k in pat), default=0),
                    patterns={",".join(k) if k else "(none)": v
                              for k, v in pat.most_common(15)})

    OUT["census_all"] = census(recs, "all")
    for m in (25, 26, 27, 28):
        OUT["census_m%d" % m] = census([r for r in recs if r['m'] == m],
                                       "m=%d" % m)
    print("EXHAUSTIVE census (all): %s" % json.dumps(OUT["census_all"])[:600],
          flush=True)
    for m in (25, 26, 27, 28):
        c = OUT["census_m%d" % m]
        print("  m=%d n=%d per_vertex=%s maxsim=%d"
              % (m, c['n'], c['per_vertex'], c['max_simultaneous']),
              flush=True)
    ck()

    # ------------------------------------------------------------ C2 mutation
    mut = []
    for (m, tag, bl) in pts[:8]:
        base = L.full_report(m, bl)['fails']
        gam = list(C.gamma_edges(C.TEMPLATES[m]))
        rng = random.Random(4242)
        flipped = False
        for _ in range(12):
            e = gam[rng.randrange(len(gam))]
            i, j = rng.randrange(3), rng.randrange(3)
            b2 = {k: [list(r) for r in v] for k, v in bl.items()}
            b2[e][i][j] = b2[e][i][j] + Fraction(rng.randint(1, 5))
            f2 = L.full_report(m, b2)['fails']
            if f2 != base:
                flipped = True
                mut.append(dict(m=m, tag=tag, edge=str(e), cell=[i, j],
                                base=base, mutated=f2))
                break
        if not flipped:
            mut.append(dict(m=m, tag=tag, note="NO FLIP in 12 mutations",
                            base=base))
    OUT["C2_mutation"] = dict(n=len(mut), records=mut,
                              ok=any('mutated' in x for x in mut))
    OUT["_controls_run"].append("C2_mutation")
    print("C2 mutation: %d/%d flipped"
          % (sum(1 for x in mut if 'mutated' in x), len(mut)), flush=True)
    ck()

    # ---------------------------------------------- manifest assertion (L21)
    missing = [c for c in OUT["_controls_declared"]
               if c not in OUT["_controls_run"]]
    OUT["_manifest_ok"] = (missing == [])
    OUT["_manifest_missing"] = missing
    ck()
    assert not missing, "CONTROL MANIFEST FAILURE: %s" % missing
    print("MANIFEST OK: %s" % OUT["_controls_run"], flush=True)
    print("DONE %.1fs" % (time.time() - t0), flush=True)


if __name__ == "__main__":
    main()
