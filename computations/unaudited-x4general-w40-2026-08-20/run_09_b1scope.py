#!/usr/bin/env python3
"""W40 / T9 -- how much of branch (B1) does the inventory actually contain?

Branch (B1) is "both diagonal supports are perfect matchings and their union
is NOT Hamiltonian (a 4+4)".  W33-D5 settled the sub-case with exactly 4
cross cells (one realisable orbit class, the twisted 4+4, now DEAD at full
exactness by W40/T3b).  Sub-cases with >= 5 cross cells were never decided.
This file measures what the 19,528 stored exact d=2 sources contain, so the
open part of (B1) is stated by size rather than guessed at.

TARGET STATEMENT (ledger 27, verbatim):
    the stored inventory's sources whose two diagonal supports are disjoint
    perfect matchings with NON-Hamiltonian union, tallied by cross-cell
    count and cross-referenced with the level-5 sweep's verdicts.

CONTROLS (ledger 21/31):
  exactness       every counted source is re-verified exact (inherited DP).
  d5_present      the twisted 4+4 must be FOUND by this classifier when fed
                  in directly (ledger 28: a witness that passes the filter).
  two_view        the by-size tally sums to the total 4+4 count.
"""
from __future__ import annotations

import json
import os
import sys
import time
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
W33 = os.path.join(os.path.dirname(HERE), "unaudited-x4general-w33-2026-08-20")
sys.path.insert(0, HERE)
from w40_core import (  # noqa: E402
    EDG, Manifest, N, d5_point, ekey, is_exact2, kernel_bases, n_cross,
    require, zero_source,
)

OUT = os.path.join(HERE, "results_t9_b1scope.json")


def to_source(entry):
    src = zero_source(N, 2)
    for k, m in entry["cells"].items():
        u, v = int(k[0]), int(k[1])
        e = ekey(u, v)
        for a in range(2):
            for b in range(2):
                q = Fraction(m[a][b])
                if u < v:
                    src[e][a][b] = q
                else:
                    src[e][b][a] = q
    return src


def classify(src):
    D0 = [e for e in EDG if src[e][0][0] != 0]
    D1 = [e for e in EDG if src[e][1][1] != 0]
    isPM = (len(D0) == 4 and len(D1) == 4
            and sorted(x for e in D0 for x in e) == list(range(N))
            and sorted(x for e in D1 for x in e) == list(range(N))
            and not (set(D0) & set(D1)))
    if not isPM:
        return None
    adj = {i: [] for i in range(N)}
    for e in D0 + D1:
        adj[e[0]].append(e[1])
        adj[e[1]].append(e[0])
    cur, prev, seen = 0, None, [0]
    for _ in range(N - 1):
        nxt = [x for x in adj[cur] if x != prev]
        if not nxt:
            break
        prev, cur = cur, nxt[0]
        if cur in seen:
            break
        seen.append(cur)
    return {"pm_pair": True, "hamiltonian": len(seen) == N,
            "cycle_len_at_0": len(seen), "ncross": n_cross(src),
            "D0": [list(e) for e in D0], "D1": [list(e) for e in D1]}


def main():
    t0 = time.time()
    MAN = Manifest(["d5_present", "exactness", "two_view", "main_tally"])
    R = {"status": "UNAUDITED",
         "pinned_head": open(os.path.join(HERE, "PINNED_HEAD.txt")).read()
         .strip(),
         "target": ("stored exact d=2 sources with disjoint-PM diagonal "
                    "supports of NON-Hamiltonian union, tallied by cross "
                    "count"),
         "_controls_run": []}

    def ran(n):
        MAN.mark(n)
        R["_controls_run"].append(n)

    c = classify(d5_point())
    dp = {"classified": c is not None,
          "pm_pair": bool(c and c["pm_pair"]),
          "non_hamiltonian": bool(c and not c["hamiltonian"]),
          "ncross": c and c["ncross"]}
    dp["ok"] = dp["pm_pair"] and dp["non_hamiltonian"] and dp["ncross"] == 4
    R["d5_present"] = dp
    require(dp["ok"], f"classifier fails on the twisted 4+4: {dp}")
    ran("d5_present")

    tally44, tallyH, exact_checked, notexact = {}, {}, 0, 0
    reps44 = []
    keys44 = []
    for pc, nm in (("A", "results_t2_A.json"), ("B", "results_t2_B.json")):
        pool = json.load(open(os.path.join(W33, nm)))["pool"]
        for i, entry in enumerate(pool):
            src = to_source(entry)
            c = classify(src)
            if c is None:
                continue
            okx, _ = is_exact2(src, N)
            exact_checked += 1
            if not okx:
                notexact += 1
                continue
            k = str(c["ncross"])
            if c["hamiltonian"]:
                tallyH[k] = tallyH.get(k, 0) + 1
            else:
                tally44[k] = tally44.get(k, 0) + 1
                keys44.append({"pool": pc, "i": i, "ncross": c["ncross"],
                               "cycle_len_at_0": c["cycle_len_at_0"]})
                if len(reps44) < 12:
                    kb = kernel_bases(src)
                    reps44.append({
                        "pool": pc, "i": i, "ncross": c["ncross"],
                        "kerprof": [kb[j]["dim"] for j in range(N)],
                        "D0": c["D0"], "D1": c["D1"],
                        "cells": entry["cells"]})
    R["exactness"] = {"pm_pair_sources_checked": exact_checked,
                      "not_exact": notexact, "ok": notexact == 0}
    ran("exactness")
    R["tally_hamiltonian_by_ncross"] = tallyH
    R["tally_4plus4_by_ncross"] = tally44
    R["n_pm_pair_sources"] = exact_checked - notexact
    R["n_4plus4"] = sum(tally44.values())
    R["n_hamiltonian"] = sum(tallyH.values())
    R["examples_4plus4"] = reps44
    R["all_4plus4_keys"] = keys44
    tv = {"sum_by_size": sum(tally44.values()) + sum(tallyH.values()),
          "pm_pair_total": exact_checked - notexact}
    tv["reconciles"] = tv["sum_by_size"] == tv["pm_pair_total"]
    tv["ok"] = tv["reconciles"]
    R["two_view"] = tv
    ran("two_view")
    ran("main_tally")
    R["manifest"] = MAN.assert_complete()
    R["elapsed"] = time.time() - t0
    with open(OUT, "w") as fh:
        json.dump(R, fh, indent=1, sort_keys=True)
    print("PM-pair sources:", R["n_pm_pair_sources"],
          "| 4+4:", R["n_4plus4"], tally44,
          "| Hamiltonian:", R["n_hamiltonian"], tallyH)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
