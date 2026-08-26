#!/usr/bin/env python3
"""UNAUDITED PROBE W17 -- T1: is the rank-one (scalar-slice) re-basing
LOSSLESS at h = 2?  Exhaustive over P2's fleet (results_a.json: 300
six-site sources x 15 pairs), plus the anchored strata of results_b*.

For every live pair we decide, exactly (Singular over Q, Rabinowitsch):

    (RK1)  exists (u,v):  E_pq(u (x) v) = 0, u_c v_c != 0, u^T A_pq v != 0

and compare with P2's general-cap verdict `witness`.  Losslessness of the
W14 re-basing at h = 2 is the claim  witness  =>  RK1.

Also recorded for every pair: the STRUCTURAL branch (Theorem W17.1) that
carries the witness, and the rank profile of the eight star blocks
A_pa, A_qa (a in U) -- the only data the h = 2 error depends on.
"""

from __future__ import annotations

import json
import os
import sys
import time
from collections import Counter
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
P2DIR = os.path.abspath(os.path.join(HERE, "..",
                                     "unaudited-witness-splitting-p2-2026-08-15"))
sys.path.insert(0, P2DIR)

import w17_h2 as H2
from w17_core import matrix_rank, oriented


def blocks_of(source):
    return {k: [[x for x in row] for row in v] for k, v in source.blocks.items()}


def star_profile(blocks, p, q, U):
    return {"p_ranks": [matrix_rank(oriented(blocks, p, a)) for a in U],
            "q_ranks": [matrix_rank(oriented(blocks, q, a)) for a in U]}


def main(limit_sources=300, branch_sample=250, files=("results_a.json",)):
    from run_a_dichotomy import build_source
    t0 = time.time()
    stats = Counter()
    detail = []
    losses = []
    branch_checked = 0
    branch_disagree = 0
    branch_counter = Counter()
    for fname in files:
        data = json.load(open(os.path.join(P2DIR, fname)))
        records = data["results"][:limit_sources]
        for n, rec in enumerate(records):
            src = build_source(rec["seed"], rec["mode"])
            blocks = blocks_of(src)
            for pr in rec["pairs"]:
                if not pr["live"] or pr["witness"] is None:
                    stats["skipped"] += 1
                    continue
                p, q = pr["pair"]
                U = tuple(a for a in range(6) if a not in (p, q))
                tag = f"s{rec['seed']}p{p}{q}"
                try:
                    rk1 = H2.decide_rank_one(blocks, p, q, U, tag, timeout=120)
                except Exception as exc:               # noqa: BLE001
                    stats["singular_error"] += 1
                    continue
                if rk1 is None:
                    stats["undecided"] += 1
                    continue
                key = ("W" if pr["witness"] else "B") + ("+R1" if rk1 else "-R1")
                stats[key] += 1
                prof = star_profile(blocks, p, q, U)
                row = {"seed": rec["seed"], "mode": rec["mode"],
                       "pair": [p, q], "witness": pr["witness"],
                       "rank_one": rk1, "status": pr["status"],
                       "min_block_degree": pr.get("min_block_degree"),
                       "p_ranks": prof["p_ranks"], "q_ranks": prof["q_ranks"]}
                if pr["witness"] and not rk1:
                    losses.append(row)
                if len(detail) < 4000:
                    detail.append(row)
                # branch control / classification
                if rk1 and branch_checked < branch_sample:
                    branch_checked += 1
                    found = H2.decide_branches(blocks, p, q, U, tag,
                                               timeout=120)
                    any_branch = any(v for v in found.values() if v is not None)
                    if any_branch != rk1:
                        branch_disagree += 1
                    for name, val in found.items():
                        if val:
                            branch_counter[name[0]] += 1
            if (n + 1) % 25 == 0:
                print(f"  [{time.time() - t0:6.0f}s] {fname} {n + 1} sources; "
                      f"{dict(stats)}")
    print("\n== T1 h=2 losslessness ==")
    for key in ("W+R1", "W-R1", "B+R1", "B-R1", "undecided", "skipped",
                "singular_error"):
        print(f"  {key:16s} {stats[key]}")
    print(f"  branch control: {branch_checked} checked, "
          f"{branch_disagree} disagreements with the direct query")
    print(f"  branch types carrying witnesses: {dict(branch_counter)}")
    if losses:
        print(f"\n  LOSSES (witness but no rank-one witness): {len(losses)}")
        for row in losses[:10]:
            print("   ", row)
    out = {"stats": dict(stats), "branch_checked": branch_checked,
           "branch_disagree": branch_disagree,
           "branch_counter": dict(branch_counter),
           "losses": losses[:200], "detail": detail}
    with open(os.path.join(HERE, "results_t1_h2_fleet.json"), "w") as fh:
        json.dump(out, fh, indent=1, default=str)
    print(f"\nwrote results_t1_h2_fleet.json [{time.time() - t0:.0f}s]")


if __name__ == "__main__":
    main(limit_sources=int(sys.argv[1]) if len(sys.argv) > 1 else 300)
