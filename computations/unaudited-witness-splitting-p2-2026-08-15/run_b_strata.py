#!/usr/bin/env python3
"""UNAUDITED PROBE (P2, task B) -- witness/splitting map over the 19 census strata.

Pinned HEAD: 86a9479bef38169bbfd8d9100c6d81ce4c66209a

The six-site theorem (proofs/six-site-arbitrary-complex-obstruction.md, eq. 7)
splits a hypothetical exact source by its rank-defect graph
F = {uv : rank A_uv != 1}, which has maximum degree two, hence |F| <= 6, and
falls into nineteen isomorphism types.  Every one of those strata is EMPTY by
the census; here we instantiate each stratum's DEFINING RANK CONDITIONS with
otherwise generic entries (the resulting sources violate GHZ equations -- the
witness/splitting dichotomy is per-source algebra and does not need exactness)
and map, per stratum:

    dead / witness / split-blocked / blocked-other  per pair,

together with the error-span dimension and the minimal blocking L-monomial
degree.

Usage: python3 run_b_strata.py [--samples 6] [--jobs 9]
"""

from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
import json
import random
import time

from wsplit_core import (PAIRS, Source, classify_source, random_matrix,
                         require)


def path(vertices):
    return [(vertices[i], vertices[i + 1]) for i in range(len(vertices) - 1)]


def cycle(vertices):
    return path(vertices) + [(vertices[-1], vertices[0])]


# The nineteen types of display (7) of the six-site obstruction, realised on
# the vertex set {0,...,5}.
STRATA = {
    "6P1": [],
    "P2+4P1": path([0, 1]),
    "2P2+2P1": path([0, 1]) + path([2, 3]),
    "P3+3P1": path([0, 1, 2]),
    "3P2": path([0, 1]) + path([2, 3]) + path([4, 5]),
    "P3+P2+P1": path([0, 1, 2]) + path([3, 4]),
    "P4+2P1": path([0, 1, 2, 3]),
    "C3+3P1": cycle([0, 1, 2]),
    "P5+P1": path([0, 1, 2, 3, 4]),
    "P4+P2": path([0, 1, 2, 3]) + path([4, 5]),
    "P3+P3": path([0, 1, 2]) + path([3, 4, 5]),
    "C3+P2+P1": cycle([0, 1, 2]) + path([3, 4]),
    "C4+2P1": cycle([0, 1, 2, 3]),
    "P6": path([0, 1, 2, 3, 4, 5]),
    "C3+P3": cycle([0, 1, 2]) + path([3, 4, 5]),
    "C4+P2": cycle([0, 1, 2, 3]) + path([4, 5]),
    "C5+P1": cycle([0, 1, 2, 3, 4]),
    "C6": cycle([0, 1, 2, 3, 4, 5]),
    "C3+C3": cycle([0, 1, 2]) + cycle([3, 4, 5]),
}

EXPECTED_SIZES = {"6P1": 0, "P2+4P1": 1, "2P2+2P1": 2, "P3+3P1": 2, "3P2": 3,
                  "P3+P2+P1": 3, "P4+2P1": 3, "C3+3P1": 3, "P5+P1": 4,
                  "P4+P2": 4, "P3+P3": 4, "C3+P2+P1": 4, "C4+2P1": 4,
                  "P6": 5, "C3+P3": 5, "C4+P2": 5, "C5+P1": 5, "C6": 6,
                  "C3+C3": 6}

F_VARIANTS = ("rank3", "rank2", "zero", "mixed")


def stratum_source(name, seed, variant):
    rng = random.Random(seed)
    defect = {tuple(sorted(edge)) for edge in STRATA[name]}
    require(len(defect) == EXPECTED_SIZES[name], f"{name} edge count")
    degrees = Counter()
    for u, v in defect:
        degrees[u] += 1
        degrees[v] += 1
    require(max(degrees.values(), default=0) <= 2, f"{name} max degree")
    blocks = {}
    for pair in PAIRS:
        if pair in defect:
            if variant == "rank3":
                rank = 3
            elif variant == "rank2":
                rank = 2
            elif variant == "zero":
                rank = 0
            else:
                rank = rng.choice([0, 2, 3])
            blocks[pair] = random_matrix(rng, rank=rank)
        else:
            blocks[pair] = random_matrix(rng, rank=1)
    source = Source(blocks)
    for pair in PAIRS:
        expected_defect = pair in defect
        actual = source.rank(*pair) != 1
        require(expected_defect == actual, f"{name} rank pattern at {pair}")
    return source


def analyse(job):
    name, seed, variant = job
    source = stratum_source(name, seed, variant)
    report = classify_source(source, max_degree=4, timeout=30)
    defect = {tuple(sorted(edge)) for edge in STRATA[name]}
    pairs = []
    for pair in PAIRS:
        record = report[pair]
        pairs.append({
            "pair": list(pair),
            "in_F": pair in defect,
            "status": record["status"],
            "span": record["span"],
            "witness": record["witness"],
            "patterns": ["*".join(pattern) for pattern in record["patterns"]],
            "min_block_degree": record["min_block_degree"],
            "error_zero": record["error_zero"],
            "cone_dim": record["cone_dim"],
        })
    return {"stratum": name, "variant": variant, "seed": seed, "pairs": pairs}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=4)
    parser.add_argument("--jobs", type=int, default=9)
    parser.add_argument("--out", default="results_b.json")
    args = parser.parse_args()

    jobs = []
    for name in STRATA:
        for variant in F_VARIANTS:
            for index in range(args.samples):
                jobs.append((name, 7000 + 31 * index, variant))

    start = time.time()
    results = []
    with ProcessPoolExecutor(max_workers=args.jobs) as pool:
        for number, result in enumerate(pool.map(analyse, jobs), 1):
            results.append(result)
            if number % 25 == 0:
                print(f"  {number}/{len(jobs)} ({time.time() - start:.0f}s)",
                      flush=True)

    table = {}
    for result in results:
        key = result["stratum"]
        entry = table.setdefault(key, {"status": Counter(),
                                       "status_on_F": Counter(),
                                       "witness_pairs": 0,
                                       "spans": Counter(),
                                       "instances": 0,
                                       "all_live_blocked": 0})
        entry["instances"] += 1
        blocked_all = True
        for record in result["pairs"]:
            entry["status"][record["status"]] += 1
            entry["spans"][record["span"]] += 1
            if record["in_F"]:
                entry["status_on_F"][record["status"]] += 1
            if record["witness"]:
                entry["witness_pairs"] += 1
                blocked_all = False
        entry["all_live_blocked"] += int(blocked_all)

    summary = {name: {"instances": entry["instances"],
                      "status": dict(entry["status"]),
                      "status_on_F_edges": dict(entry["status_on_F"]),
                      "witness_pairs": entry["witness_pairs"],
                      "instances_with_every_live_pair_blocked":
                          entry["all_live_blocked"],
                      "span_range": [min(entry["spans"]), max(entry["spans"])]}
               for name, entry in table.items()}
    with open(args.out, "w") as handle:
        json.dump({"summary": summary, "results": results}, handle, indent=1)
    for name in STRATA:
        entry = summary[name]
        print(f"{name:10s} |F|={EXPECTED_SIZES[name]} "
              f"inst={entry['instances']:3d} "
              f"witness_pairs={entry['witness_pairs']:3d} "
              f"all_blocked={entry['instances_with_every_live_pair_blocked']:3d} "
              f"span={entry['span_range']} {dict(entry['status'])}")
    print(f"seconds={time.time() - start:.0f}")


if __name__ == "__main__":
    main()
