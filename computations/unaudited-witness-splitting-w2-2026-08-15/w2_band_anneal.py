#!/usr/bin/env python3
"""UNAUDITED PROBE (W2) -- annealed adversarial hunt in the monomial regime.

Pinned HEAD: 26ba69f7e643694c6a58464af6e9e1de9ec92f01

Task D, wide regime: search the MONOMIAL regime (every block a scaled partial
permutation matrix; 'cross' variant: every block inside row c U column c) with
a cell budget inside the current support band for a template with

    all three constant fibres nonempty,
    ZERO mixed singleton fibres,

and then decide any such template exactly with the O1/O2 closure.  Uphill
moves are accepted with a Metropolis rule so the search is not a greedy
descent (the greedy version in w2_probe_cells.py never left score >= 5).
"""

from __future__ import annotations

import argparse
from collections import Counter
import json
import math
import random
import sys
import time

from w2_cells import (Q, analyse_cells, cell_fibres, mixed_singletons,
                      neighbours, random_monomial, support_cells)
from w2_monomial import geometry

sys.path.insert(0, "/Users/rishi/workplace/krenn-conjecture/computations")
from search_monomial_no_singleton_sat import colored_triple_orbits  # noqa: E402


def score_of(geo, cells):
    table = cell_fibres(geo, cells)
    penalty = sum(100 for c in range(Q)
                  if not table.get(tuple([c] * geo.size)))
    return mixed_singletons(table) + penalty, table


def anneal(geo, targets, rng, pattern, budget, steps, floor, t0=3.0, t1=0.05):
    cells = random_monomial(geo, targets, rng, pattern, budget)
    score, table = score_of(geo, cells)
    best = (score, cells, table)
    for step in range(steps):
        if score == 0:
            break
        temperature = t0 * (t1 / t0) ** (step / max(1, steps - 1))
        candidate = neighbours(geo, cells, targets, pattern, rng, budget)
        if candidate is None:
            break
        if support_cells(candidate) < floor:
            continue
        new_score, new_table = score_of(geo, candidate)
        delta = new_score - score
        if delta <= 0 or rng.random() < math.exp(-delta / temperature):
            cells, score, table = candidate, new_score, new_table
            if score < best[0]:
                best = (score, cells, table)
    return best


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--restarts", type=int, default=1500)
    parser.add_argument("--steps", type=int, default=1200)
    parser.add_argument("--low", type=int, default=18)
    parser.add_argument("--high", type=int, default=27)
    parser.add_argument("--pattern", default="injection",
                        choices=("injection", "cross"))
    parser.add_argument("--seed", type=int, default=20260815)
    parser.add_argument("--out", default="band_anneal.json")
    args = parser.parse_args()
    print(f"UNAUDITED PROBE (W2) -- annealed band hunt, pattern={args.pattern}, "
          f"budget [{args.low},{args.high}], HEAD 26ba69f", flush=True)
    geo = geometry(8)
    orbits = colored_triple_orbits(8)
    rng = random.Random(args.seed)
    histogram = Counter()
    survivors = []
    killed = Counter()
    best_overall = None
    start = time.time()
    for restart in range(args.restarts):
        targets = orbits[rng.randrange(len(orbits))]
        budget = rng.randint(args.low, args.high)
        score, cells, table = anneal(geo, targets, rng, args.pattern, budget,
                                     args.steps, args.low)
        histogram[min(score, 30)] += 1
        if best_overall is None or score < best_overall[0]:
            best_overall = (score, support_cells(cells), budget)
            print(f"  restart {restart}: new best score={score} "
                  f"support={support_cells(cells)} ({time.time()-start:.0f}s)",
                  flush=True)
        if score == 0:
            verdict = analyse_cells(geo, cells, table=table)
            killed[verdict["verdict"]] += 1
            if verdict["verdict"] == "survivor":
                survivors.append({"support": support_cells(cells),
                                  "cells": [sorted(map(list, e)) for e in cells],
                                  "detail": verdict})
                print("  *** SURVIVOR *** support="
                      f"{support_cells(cells)}", flush=True)
        if restart % 100 == 0:
            print(f"  restart {restart}: best={best_overall} "
                  f"zero_hits={sum(killed.values())} "
                  f"({time.time() - start:.0f}s)", flush=True)
    report = {"pattern": args.pattern, "restarts": args.restarts,
              "steps": args.steps, "band": [args.low, args.high],
              "best": best_overall,
              "score_histogram": {str(k): v for k, v in sorted(histogram.items())},
              "zero_singleton_verdicts": dict(killed),
              "survivors": survivors,
              "seconds": round(time.time() - start, 1)}
    with open(args.out, "w") as handle:
        json.dump(report, handle, indent=1)
    print(json.dumps({k: v for k, v in report.items() if k != "survivors"},
                     indent=1), flush=True)
    print(f"SURVIVORS: {len(survivors)}", flush=True)


if __name__ == "__main__":
    main()
