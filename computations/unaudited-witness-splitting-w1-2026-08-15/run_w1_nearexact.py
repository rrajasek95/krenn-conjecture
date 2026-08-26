#!/usr/bin/env python3
"""UNAUDITED PROBE (W1, task A2/B) -- census of the NEAR-EXACT region.

Pinned HEAD: 26ba69f7e643694c6a58464af6e9e1de9ec92f01

The 36 shadows live at 40-50% of the mixed system.  The lemma J.1 question
is about the other end of the axis, so this script samples the near-exact
region directly: take sources from P2's constructible families and from the
nineteen census strata, gauge them to pure = 1, run the exact star push to
its stall (typically 95-100% of the 726 mixed equations satisfied), and
record, at the stall,

    satisfied fraction | live pairs | witness pairs | blocked pairs
    non-coordinate rank-one blocks | singleton mixed fibres | support

The J.1 evidence is the JOINT distribution: is there any source with a high
satisfied fraction, no dead-pair collapse, EVERY live pair blocked, and a
non-coordinate rank-one block?  Such a source is the plan's falsifier.

Usage: python3 run_w1_nearexact.py [--samples 240] [--jobs 12]
"""

from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from fractions import Fraction
import json
import random
import time

from w1_core import (MIXED_WORDS, NMIXED, PAIRS, SITES, Source,
                     all_coefficients, blocking_metrics, exactness_metrics,
                     matrix_rank, push_cycle, random_matrix, random_source,
                     structure_metrics)
from run_b_strata import STRATA
from run_c_pure_hunt import (anchored_source, census_profile_source,
                             family_pure_matching, gauge_pure, rank_floor)


FAMILIES = ("generic", "sparse", "lowrank", "census", "anchored",
            "purematching", "anchored6P1")


def build(kind, seed):
    """One pure-normalised source of the named family (None if it degenerates)."""
    rng = random.Random(seed)
    name = None
    if kind in ("generic", "sparse", "lowrank"):
        source = random_source(rng, kind)
    elif kind == "census":
        source, name = census_profile_source(rng)
    elif kind == "anchored":
        name = rng.choice(list(STRATA))
        source = anchored_source(rng, name)
    elif kind == "purematching":
        source = family_pure_matching(rng)
    elif kind == "anchored6P1":
        # ALL fifteen blocks coordinate rank-one with slice-cover anchors:
        # the purest form of the coordinate/monomial regime J.1 speaks of.
        name = "6P1"
        source = anchored_source(rng, name)
    else:
        raise ValueError(kind)
    if source is None:
        return None, None
    return gauge_pure(source), name


def analyse(job):
    kind, seed = job
    source, name = build(kind, seed)
    if source is None:
        return None
    start = time.time()
    before = {"structure": structure_metrics(source),
              "exactness": exactness_metrics(source)}
    final, _keep, _trace = push_cycle(source, rounds=4)
    structure = structure_metrics(final)
    exactness = exactness_metrics(final)
    blocking = blocking_metrics(final, max_degree=2, timeout=30)
    base_blocking = blocking_metrics(source, max_degree=2, timeout=30)
    return {
        "kind": kind, "seed": seed, "stratum": name,
        "base": {"fraction": round(
                     before["exactness"]["mixed_satisfied_fraction"], 6),
                 "live": base_blocking["live_pairs"],
                 "witness": base_blocking["witness_pairs"],
                 "all_blocked": base_blocking["all_live_blocked"],
                 "noncoordinate": before["structure"]["noncoordinate_rank1"],
                 "rank1": before["structure"]["rank1_blocks"],
                 "singletons": before["exactness"]["singleton_mixed_fibres"],
                 "support": before["structure"]["support_size"]},
        "final": {"fraction": round(exactness["mixed_satisfied_fraction"], 6),
                  "violated": exactness["mixed_violated"],
                  "live": blocking["live_pairs"],
                  "witness": blocking["witness_pairs"],
                  "blocked": blocking["blocked_pairs"],
                  "undecided": len(blocking["undecided_pairs"]),
                  "all_blocked": blocking["all_live_blocked"],
                  "noncoordinate": structure["noncoordinate_rank1"],
                  "rank1": structure["rank1_blocks"],
                  "kinds": structure["kinds"],
                  "singletons": exactness["singleton_mixed_fibres"],
                  "support": structure["support_size"],
                  "rank_floor": rank_floor(final)},
        "seconds": round(time.time() - start, 1),
    }


def bucket(fraction):
    for edge in (0.5, 0.8, 0.9, 0.95, 0.98, 0.99, 0.995, 1.0):
        if fraction < edge:
            return f"<{edge}"
    return "1.0"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=40)
    parser.add_argument("--jobs", type=int, default=12)
    parser.add_argument("--out", default="results_nearexact.json")
    args = parser.parse_args()

    jobs = [(kind, 90000 + 13 * index + 7 * order)
            for order, kind in enumerate(FAMILIES)
            for index in range(args.samples)]
    start = time.time()
    results = []
    with ProcessPoolExecutor(max_workers=args.jobs) as pool:
        for number, result in enumerate(pool.map(analyse, jobs), 1):
            if result is not None:
                results.append(result)
            if number % 25 == 0:
                print(f"  {number}/{len(jobs)} ({time.time()-start:.0f}s)",
                      flush=True)

    rows = [row["final"] for row in results]
    near = [row for row in rows if row["fraction"] >= 0.95]
    near_full = [row for row in near if row["live"] == 15]
    blocked_near = [row for row in near if row["all_blocked"]]
    summary = {
        "instances": len(results),
        "by_family": {kind: len([r for r in results if r["kind"] == kind])
                      for kind in FAMILIES},
        "fraction_buckets": dict(Counter(bucket(row["fraction"])
                                         for row in rows)),
        "base_all_blocked": sum(1 for row in results
                                if row["base"]["all_blocked"]),
        "final_all_blocked": sum(1 for row in rows if row["all_blocked"]),
        "near_exact_instances": len(near),
        "near_exact_all_live": len(near_full),
        "near_exact_all_blocked": len(blocked_near),
        "near_exact_all_blocked_noncoordinate": sum(
            1 for row in blocked_near if row["noncoordinate"] > 0),
        "witness_pairs_near_exact": dict(Counter(row["witness"]
                                                 for row in near)),
        "live_pairs_near_exact": dict(Counter(row["live"] for row in near)),
        "singletons_near_exact": dict(Counter(row["singletons"]
                                              for row in near)),
        "max_fraction_all_blocked": max(
            (row["fraction"] for row in rows if row["all_blocked"]),
            default=None),
        "max_fraction_all_blocked_noncoordinate": max(
            (row["fraction"] for row in rows
             if row["all_blocked"] and row["noncoordinate"] > 0),
            default=None),
        "max_fraction_all_blocked_15live": max(
            (row["fraction"] for row in rows
             if row["all_blocked"] and row["live"] == 15),
            default=None),
    }
    with open(args.out, "w") as handle:
        json.dump({"summary": summary, "results": results}, handle, indent=1)
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
