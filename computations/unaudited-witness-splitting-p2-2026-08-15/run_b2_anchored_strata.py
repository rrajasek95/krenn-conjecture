#!/usr/bin/env python3
"""UNAUDITED PROBE (P2, task B, second family) -- the 19 strata, anchored.

Pinned HEAD: 86a9479bef38169bbfd8d9100c6d81ce4c66209a

run_b_strata.py instantiates each census stratum with GENERIC rank-one blocks
on the R-edges.  A real exact source cannot be that generic: the forced
incident-edge theorem of notes/slice-cover.md supplies, at every vertex and
colour, an incident rank-one edge whose factor at the opposite endpoint is a
coordinate vector, and at |F| = 6 the defect budget of
notes/six-vertex-rank-graph.md forces EVERY R-edge to be a coordinate
tensor-coordinate basis tensor.  This script instantiates each stratum in that
anchored coordinate family instead, and maps the same statuses.

Usage: python3 run_b2_anchored_strata.py [--samples 8] [--jobs 8]
"""

from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
import json
import random
import time

from wsplit_core import PAIRS, classify_source
from run_b_strata import EXPECTED_SIZES, STRATA
from run_c_pure_hunt import anchor_ok, anchored_source, gauge_pure, rank_floor


def analyse(job):
    name, seed = job
    rng = random.Random(seed)
    source = None
    for _ in range(40):
        source = anchored_source(rng, name)
        if source is not None:
            break
    if source is None:
        return None
    gauged = gauge_pure(source)
    pure_ok = gauged is not None
    if pure_ok:
        source = gauged
    report = classify_source(source, max_degree=4, timeout=30)
    pairs = []
    for pair in PAIRS:
        record = report[pair]
        pairs.append({"pair": list(pair), "status": record["status"],
                      "span": record["span"], "witness": record["witness"],
                      "patterns": ["*".join(p) for p in record["patterns"]],
                      "min_block_degree": record["min_block_degree"]})
    live = [record for record in pairs if record["status"] != "dead"]
    return {"stratum": name, "seed": seed, "pure_normalised": pure_ok,
            "rank_floor": rank_floor(source), "anchored": anchor_ok(source),
            "live_pairs": len(live),
            "witness_pairs": sum(1 for r in live if r["witness"]),
            "all_live_blocked": all(r["witness"] is False for r in live),
            "pairs": pairs}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=8)
    parser.add_argument("--jobs", type=int, default=8)
    parser.add_argument("--out", default="results_b2.json")
    args = parser.parse_args()
    jobs = [(name, 33000 + 41 * index)
            for name in STRATA for index in range(args.samples)]
    start = time.time()
    results = []
    with ProcessPoolExecutor(max_workers=args.jobs) as pool:
        for number, result in enumerate(pool.map(analyse, jobs), 1):
            if result is not None:
                results.append(result)
            if number % 40 == 0:
                print(f"  {number}/{len(jobs)} ({time.time() - start:.0f}s)",
                      flush=True)
    summary = {}
    for name in STRATA:
        rows = [row for row in results if row["stratum"] == name]
        if not rows:
            continue
        summary[name] = {
            "defect_edges": EXPECTED_SIZES[name],
            "instances": len(rows),
            "all_live_blocked": sum(row["all_live_blocked"] for row in rows),
            "witness_pairs": sum(row["witness_pairs"] for row in rows),
            "live_pairs": sum(row["live_pairs"] for row in rows),
            "status": dict(Counter(r["status"] for row in rows
                                   for r in row["pairs"])),
            "min_block_degree": dict(Counter(
                str(r["min_block_degree"]) for row in rows
                for r in row["pairs"] if r["status"] != "dead"
                and r["witness"] is False)),
        }
    with open(args.out, "w") as handle:
        json.dump({"summary": summary, "results": results}, handle, indent=1)
    for name in STRATA:
        entry = summary.get(name)
        if not entry:
            continue
        print(f"{name:10s} |F|={entry['defect_edges']} inst={entry['instances']:2d} "
              f"all_blocked={entry['all_live_blocked']:2d} "
              f"witness={entry['witness_pairs']:3d}/{entry['live_pairs']:3d} "
              f"{dict(entry['status'])} mindeg={entry['min_block_degree']}")
    print(f"seconds={time.time() - start:.0f}")


if __name__ == "__main__":
    main()
