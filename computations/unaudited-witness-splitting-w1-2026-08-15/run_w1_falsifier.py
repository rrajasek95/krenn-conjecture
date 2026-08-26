#!/usr/bin/env python3
"""UNAUDITED PROBE (W1, task A2/B) -- the falsifier hunt from the exact end.

Pinned HEAD: 26ba69f7e643694c6a58464af6e9e1de9ec92f01

The push experiments walk from the all-blocked shadows towards exactness.
This script walks the other way: it starts at the near-exact stall points
(95-100% of the 726 mixed equations satisfied, typically 7-10 witness pairs)
and hill-climbs to REMOVE witnesses while holding the satisfied fraction
above a threshold.

    objective (lexicographic):  minimise witness pairs, then maximise the
                                satisfied fraction
    hard constraints:           satisfied fraction >= threshold,
                                live pairs >= min_live

Reaching zero witness pairs at a high satisfied fraction is exactly the
plan's falsifier for J.1 ("shadows reach exactness still blocked and
non-coordinate").  The move set deliberately includes both directions of
the coordinate axis (monomialise / spread a rank-one block), so the search
is not biased towards J.1's conclusion.

Usage: python3 run_w1_falsifier.py [--runs 24] [--steps 40] [--jobs 12]
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
                     matrix_rank, push_cycle, structure_metrics)
from run_c_pure_hunt import gauge_pure
from run_w1_nearexact import build, FAMILIES


def state_metrics(source, max_degree=2):
    structure = structure_metrics(source)
    exact = exactness_metrics(source)
    blocking = blocking_metrics(source, max_degree=max_degree, timeout=30)
    return {"fraction": exact["mixed_satisfied_fraction"],
            "satisfied": exact["mixed_satisfied"],
            "singletons": exact["singleton_mixed_fibres"],
            "witness": blocking["witness_pairs"],
            "live": blocking["live_pairs"],
            "all_blocked": blocking["all_live_blocked"],
            "noncoordinate": structure["noncoordinate_rank1"],
            "rank1": structure["rank1_blocks"],
            "support": structure["support_size"],
            "kinds": structure["kinds"]}


def monomialise(matrix, rng):
    """Keep one nonzero entry of a block (towards the coordinate regime)."""
    entries = [(i, j) for i in range(3) for j in range(3) if matrix[i][j]]
    if len(entries) <= 1:
        return None
    keep = rng.choice(entries)
    return [[matrix[i][j] if (i, j) == keep else Fraction(0)
             for j in range(3)] for i in range(3)]


def spread(matrix, rng):
    """Add a second nonzero entry (away from the coordinate regime)."""
    zeros = [(i, j) for i in range(3) for j in range(3) if not matrix[i][j]]
    if not zeros:
        return None
    i, j = rng.choice(zeros)
    scale = next((abs(matrix[a][b]) for a in range(3) for b in range(3)
                  if matrix[a][b]), Fraction(1))
    out = [row[:] for row in matrix]
    out[i][j] = scale * Fraction(rng.choice([1, -1, 2, -2]), rng.choice([1, 2]))
    return out


def perturb(matrix, rng):
    entries = [(i, j) for i in range(3) for j in range(3) if matrix[i][j]]
    if not entries:
        return None
    i, j = rng.choice(entries)
    out = [row[:] for row in matrix]
    if rng.random() < 0.35:
        out[i][j] = Fraction(0)
    else:
        out[i][j] = out[i][j] * Fraction(rng.choice([2, 3, -1, -2]),
                                         rng.choice([1, 2, 3]))
    return out


MOVES = ("monomialise", "spread", "perturb")


def mutate(source, rng):
    for _ in range(20):
        pair = rng.choice(PAIRS)
        move = rng.choice(MOVES)
        matrix = source.blocks[pair]
        if move == "monomialise":
            new = monomialise(matrix, rng)
        elif move == "spread":
            new = spread(matrix, rng)
        else:
            new = perturb(matrix, rng)
        if new is None:
            continue
        blocks = {other: [row[:] for row in source.blocks[other]]
                  for other in PAIRS}
        blocks[pair] = new
        candidate = Source(blocks)
        gauged = gauge_pure(candidate)
        if gauged is None:
            continue
        return gauged, move, pair
    return None, None, None


def better(new, old):
    """Lexicographic: fewer witnesses first, then more satisfied equations."""
    if new["witness"] != old["witness"]:
        return new["witness"] < old["witness"]
    return new["satisfied"] > old["satisfied"]


def run(job):
    kind, seed, steps, threshold, min_live = job
    rng = random.Random(seed)
    source, name = build(kind, seed)
    if source is None:
        return None
    start = time.time()
    source, _keep, _trace = push_cycle(source, rounds=3)
    current = state_metrics(source)
    if current["fraction"] < threshold:
        return {"kind": kind, "seed": seed, "stratum": name,
                "skipped": "start below threshold",
                "start": {k: v for k, v in current.items() if k != "kinds"}}
    best_source, best = source, current
    trace = [{"step": 0, "witness": best["witness"],
              "fraction": round(best["fraction"], 6),
              "live": best["live"], "noncoordinate": best["noncoordinate"]}]
    accepted = 0
    for step in range(steps):
        candidate, move, pair = mutate(best_source, rng)
        if candidate is None:
            continue
        candidate, _keep, _trace = push_cycle(candidate, rounds=2)
        metrics = state_metrics(candidate)
        if metrics["fraction"] < threshold or metrics["live"] < min_live:
            continue
        if not better(metrics, best):
            continue
        best_source, best = candidate, metrics
        accepted += 1
        trace.append({"step": step + 1, "move": move, "pair": list(pair),
                      "witness": best["witness"],
                      "fraction": round(best["fraction"], 6),
                      "live": best["live"],
                      "noncoordinate": best["noncoordinate"],
                      "singletons": best["singletons"]})
        if best["witness"] == 0:
            break
    final = state_metrics(best_source, max_degree=4)
    return {"kind": kind, "seed": seed, "stratum": name, "steps": steps,
            "threshold": threshold, "min_live": min_live,
            "accepted_moves": accepted, "trace": trace,
            "final": {k: v for k, v in final.items()},
            "blocks": ({str(pair): [[str(value) for value in row]
                                    for row in best_source.blocks[pair]]
                        for pair in PAIRS} if final["witness"] == 0 else None),
            "seconds": round(time.time() - start, 1)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs", type=int, default=4)
    parser.add_argument("--steps", type=int, default=40)
    parser.add_argument("--threshold", type=float, default=0.95)
    parser.add_argument("--min-live", type=int, default=6)
    parser.add_argument("--jobs", type=int, default=12)
    parser.add_argument("--out", default="results_falsifier.json")
    args = parser.parse_args()

    jobs = [(kind, 60000 + 11 * index + 5 * order, args.steps,
             args.threshold, args.min_live)
            for order, kind in enumerate(FAMILIES)
            for index in range(args.runs)]
    start = time.time()
    results = []
    with ProcessPoolExecutor(max_workers=args.jobs) as pool:
        for number, result in enumerate(pool.map(run, jobs), 1):
            if result is not None:
                results.append(result)
            if number % 5 == 0:
                print(f"  {number}/{len(jobs)} ({time.time()-start:.0f}s)",
                      flush=True)
    done = [row for row in results if "final" in row]
    summary = {
        "runs": len(results),
        "completed": len(done),
        "start_witness": dict(Counter(row["trace"][0]["witness"]
                                      for row in done)),
        "final_witness": dict(Counter(row["final"]["witness"] for row in done)),
        "min_final_witness": min((row["final"]["witness"] for row in done),
                                 default=None),
        "reached_all_blocked": sum(1 for row in done
                                   if row["final"]["all_blocked"]),
        "final_fractions": sorted(round(row["final"]["fraction"], 4)
                                  for row in done),
        "final_noncoordinate": dict(Counter(row["final"]["noncoordinate"]
                                            for row in done)),
        "final_live": dict(Counter(row["final"]["live"] for row in done)),
        "accepted_moves": dict(Counter(row["accepted_moves"] for row in done)),
        "move_counts": dict(Counter(entry.get("move") for row in done
                                    for entry in row["trace"]
                                    if entry.get("move"))),
    }
    with open(args.out, "w") as handle:
        json.dump({"summary": summary, "results": results}, handle, indent=1)
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
