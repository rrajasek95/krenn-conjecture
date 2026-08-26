#!/usr/bin/env python3
"""UNAUDITED PROBE (P2, task A) -- dichotomy validation on random six-site sources.

Pinned HEAD: 86a9479bef38169bbfd8d9100c6d81ce4c66209a

For each source and each of the 15 pairs (p,q) we decide, exactly:

  * WITNESS   -- does there exist K over C with E_pq(K)=0 and
                 s kappa_0 kappa_1 kappa_2 != 0?   (Singular, Rabinowitsch)
  * SPLIT     -- does some product l_1 l_2, l_i in {s,kappa_0,kappa_1,kappa_2},
                 lie in the degree-2 part of the error ideal?  (exact linear
                 algebra over Q; at most 10 patterns)
  * higher-degree L-monomial membership in degrees 3 and 4.

The dichotomy of the plan asserts these are complementary on live pairs:
  witness  XOR  split-blocked  (with the r-degenerate case E == 0 giving a
  generic witness).  Both directions are counted here.

Usage: python3 run_a_dichotomy.py [--sources 300] [--jobs 9] [--out a.json]
"""

from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
import json
import random
import time

from wsplit_core import PAIRS, classify_source, random_source

MODES = ("generic", "sparse", "lowrank", "diagonal", "binary", "mixed")


def build_source(seed, mode):
    rng = random.Random(seed)
    if mode != "mixed":
        return random_source(rng, mode)
    from wsplit_core import PAIRS as ALL, Source, random_matrix
    blocks = {}
    for pair in ALL:
        pick = rng.choice(["generic", "sparse", "rank1", "rank2", "zero",
                           "diagonal"])
        if pick == "generic":
            blocks[pair] = random_matrix(rng)
        elif pick == "sparse":
            blocks[pair] = random_matrix(rng, density=0.4)
        elif pick == "rank1":
            blocks[pair] = random_matrix(rng, rank=1)
        elif pick == "rank2":
            blocks[pair] = random_matrix(rng, rank=2)
        elif pick == "zero":
            blocks[pair] = [[0] * 3 for _ in range(3)]
        else:
            matrix = [[0] * 3 for _ in range(3)]
            for c in range(3):
                matrix[c][c] = rng.randint(-4, 4)
            blocks[pair] = matrix
    return Source(blocks)


def analyse(job):
    seed, mode = job
    source = build_source(seed, mode)
    report = classify_source(source, max_degree=4)
    out = []
    for pair in PAIRS:
        record = report[pair]
        out.append({
            "pair": list(pair),
            "status": record["status"],
            "live": record["live"],
            "error_zero": record["error_zero"],
            "span": record["span"],
            "span_is_W": record["span_is_W"],
            "in_W": record["all_components_in_W"],
            "patterns": ["*".join(pattern) for pattern in record["patterns"]],
            "witness": record["witness"],
            "cone_dim": record["cone_dim"],
            "variety_empty": record["variety_empty"],
            "min_block_degree": record["min_block_degree"],
            "blocking_monomials": sorted(
                f"{degree}:{name}"
                for (degree, name), value in record["mem"].items() if value),
        })
    return {"seed": seed, "mode": mode, "pairs": out}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sources", type=int, default=300)
    parser.add_argument("--jobs", type=int, default=9)
    parser.add_argument("--out", default="results_a.json")
    args = parser.parse_args()

    jobs = []
    for index in range(args.sources):
        mode = MODES[index % len(MODES)]
        jobs.append((1000 + index, mode))

    start = time.time()
    results = []
    with ProcessPoolExecutor(max_workers=args.jobs) as pool:
        for number, result in enumerate(pool.map(analyse, jobs), 1):
            results.append(result)
            if number % 20 == 0:
                print(f"  {number}/{len(jobs)} sources "
                      f"({time.time() - start:.0f}s)", flush=True)

    status = Counter()
    by_mode = {mode: Counter() for mode in MODES}
    span_hist = Counter()
    violations_pattern_but_witness = []
    violations_nowitness_nopattern = []
    higher_degree_rescue = Counter()
    in_W_failures = 0
    live_pairs = 0
    for result in results:
        for record in result["pairs"]:
            status[record["status"]] += 1
            by_mode[result["mode"]][record["status"]] += 1
            span_hist[record["span"]] += 1
            if not record["in_W"]:
                in_W_failures += 1
            if not record["live"]:
                continue
            live_pairs += 1
            if record["patterns"] and record["witness"]:
                violations_pattern_but_witness.append(
                    (result["seed"], record["pair"]))
            if not record["witness"] and not record["patterns"]:
                violations_nowitness_nopattern.append(
                    (result["seed"], result["mode"], record["pair"],
                     record["min_block_degree"], record["cone_dim"],
                     record["span"]))
                higher_degree_rescue[record["min_block_degree"]] += 1

    summary = {
        "head": "86a9479bef38169bbfd8d9100c6d81ce4c66209a",
        "sources": len(results),
        "pairs_total": len(results) * len(PAIRS),
        "live_pairs": live_pairs,
        "status": dict(status),
        "status_by_mode": {mode: dict(counter)
                           for mode, counter in by_mode.items()},
        "span_histogram": dict(sorted(span_hist.items())),
        "components_outside_W": in_W_failures,
        "pattern_but_witness": violations_pattern_but_witness,
        "nowitness_nopattern_count": len(violations_nowitness_nopattern),
        "nowitness_nopattern_min_degree": {
            str(key): value for key, value in higher_degree_rescue.items()},
        "nowitness_nopattern_examples": violations_nowitness_nopattern[:25],
        "seconds": round(time.time() - start, 1),
    }
    with open(args.out, "w") as handle:
        json.dump({"summary": summary, "results": results}, handle, indent=1)
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
