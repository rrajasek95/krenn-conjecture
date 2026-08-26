#!/usr/bin/env python3
"""UNAUDITED PROBE (W2) -- the monomial regime beyond one cell per edge.

Pinned HEAD: 26ba69f7e643694c6a58464af6e9e1de9ec92f01

Three probes:

 A  ONE-EDGE UPGRADES.  Take every one of the 28 exhausted full-support
    one-cell templates and add ONE extra cell on one edge, keeping the block
    a monomial matrix.  Exhaustive: does adding a rank-two block break the
    odd holonomy?
 B  TWO-EDGE UPGRADES.  Same, two extra cells (exhaustive over pairs).
 C  BAND HUNT.  Simulated annealing over the monomial regime with a cell
    budget in [18, 27] (the current support band), minimising the number of
    mixed singleton fibres; any template reaching zero is decided exactly.
"""

from __future__ import annotations

import argparse
from collections import Counter
import json
import random
import sys
import time

from w2_cells import (Q, analyse_cells, all_partial_injections, cell_fibres,
                      mixed_singletons, neighbours, random_monomial,
                      support_cells)
from w2_monomial import geometry

sys.path.insert(0, "/Users/rishi/workplace/krenn-conjecture/computations")
from search_monomial_no_singleton_sat import colored_triple_orbits  # noqa: E402


def load_models(path):
    with open(path) as handle:
        blob = json.load(handle)
    out = []
    for orbit, result in blob["results"].items():
        for model in result.get("models", []):
            out.append((orbit, model))
    return out


def to_cells(geo, labels):
    return [frozenset() if label is None else frozenset({tuple(label)})
            for label in labels]


def upgrade_options(geo, cells, index):
    """Extra cells keeping edge `index` a monomial matrix."""
    current = set(cells[index])
    rows = {a for a, _ in current}
    columns = {b for _, b in current}
    return [(a, b) for a in range(Q) for b in range(Q)
            if a not in rows and b not in columns]


def probe_upgrades(models, depth, limit=None):
    geo = geometry(8)
    verdicts = Counter()
    survivors = []
    total = 0
    for orbit, model in models:
        base = to_cells(geo, model["labels"])
        slots = [(index, cell) for index in range(len(geo.edges))
                 for cell in upgrade_options(geo, base, index)]
        from itertools import combinations
        for choice in combinations(slots, depth):
            if len({index for index, _ in choice}) != len(choice):
                # two cells on the same edge: recheck the injection condition
                pass
            cells = [set(entry) for entry in base]
            ok = True
            for index, cell in choice:
                rows = {a for a, _ in cells[index]}
                columns = {b for _, b in cells[index]}
                if cell[0] in rows or cell[1] in columns:
                    ok = False
                    break
                cells[index].add(cell)
            if not ok:
                continue
            cells = [frozenset(entry) for entry in cells]
            table = cell_fibres(geo, cells)
            total += 1
            if mixed_singletons(table):
                verdicts["O2-literal-singleton"] += 1
                continue
            verdict = analyse_cells(geo, cells, table=table)
            verdicts[verdict["verdict"]] += 1
            if verdict["verdict"] == "survivor":
                survivors.append({"orbit": orbit, "depth": depth,
                                  "support": support_cells(cells),
                                  "cells": [sorted(map(list, entry))
                                            for entry in cells]})
            if limit and total >= limit:
                return verdicts, survivors, total
    return verdicts, survivors, total


def probe_band(orbits, restarts, steps, budget_low, budget_high, pattern,
               seed=4242):
    geo = geometry(8)
    rng = random.Random(seed)
    best_overall = None
    survivors = []
    reached_zero = 0
    histogram = Counter()
    for restart in range(restarts):
        targets = orbits[rng.randrange(len(orbits))]
        budget = rng.randint(budget_low, budget_high)
        cells = random_monomial(geo, targets, rng, pattern, budget)
        table = cell_fibres(geo, cells)
        score = mixed_singletons(table)
        if any(not table.get(tuple([c] * 8)) for c in range(Q)):
            score += 100
        for _ in range(steps):
            if score == 0:
                break
            candidate = neighbours(geo, cells, targets, pattern, rng, budget)
            if candidate is None:
                break
            if support_cells(candidate) < budget_low:
                continue
            table2 = cell_fibres(geo, candidate)
            score2 = mixed_singletons(table2)
            if any(not table2.get(tuple([c] * 8)) for c in range(Q)):
                score2 += 100
            if score2 <= score:
                cells, table, score = candidate, table2, score2
        histogram[min(score, 40)] += 1
        if best_overall is None or score < best_overall[0]:
            best_overall = (score, support_cells(cells))
        if score == 0:
            reached_zero += 1
            verdict = analyse_cells(geo, cells, table=table)
            if verdict["verdict"] == "survivor":
                survivors.append({"support": support_cells(cells),
                                  "cells": [sorted(map(list, entry))
                                            for entry in cells],
                                  "detail": verdict})
                print(f"  *** BAND SURVIVOR support={support_cells(cells)}",
                      flush=True)
            else:
                histogram[f"zero-killed-{verdict['verdict']}"] += 1
    return {"best_score_support": best_overall, "reached_zero": reached_zero,
            "score_histogram": {str(k): v for k, v in histogram.items()},
            "survivors": survivors}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--models", default="hunt8_models.json")
    parser.add_argument("--restarts", type=int, default=400)
    parser.add_argument("--steps", type=int, default=250)
    parser.add_argument("--low", type=int, default=18)
    parser.add_argument("--high", type=int, default=27)
    parser.add_argument("--pattern", default="injection",
                        choices=("injection", "cross"))
    parser.add_argument("--out", default="cells_probe.json")
    args = parser.parse_args()
    print("UNAUDITED PROBE (W2) -- monomial regime beyond one cell/edge, "
          "HEAD 26ba69f", flush=True)
    report = {}
    models = load_models(args.models)
    print(f"base templates: {len(models)}", flush=True)
    for depth in (1, 2):
        start = time.time()
        verdicts, survivors, total = probe_upgrades(models, depth)
        report[f"upgrade_depth{depth}"] = {
            "templates": total, "verdicts": dict(verdicts),
            "survivors": survivors, "seconds": round(time.time() - start, 1)}
        print(f"depth {depth}: {total} templates, verdicts={dict(verdicts)}, "
              f"survivors={len(survivors)} ({time.time() - start:.0f}s)",
              flush=True)
        with open(args.out, "w") as handle:
            json.dump(report, handle, indent=1)
    orbits = colored_triple_orbits(8)
    start = time.time()
    report["band_hunt"] = probe_band(orbits, args.restarts, args.steps,
                                     args.low, args.high, args.pattern)
    report["band_hunt"]["seconds"] = round(time.time() - start, 1)
    report["band_hunt"]["pattern"] = args.pattern
    print(f"band hunt: {json.dumps(report['band_hunt'])[:1200]}", flush=True)
    with open(args.out, "w") as handle:
        json.dump(report, handle, indent=1)


if __name__ == "__main__":
    main()
