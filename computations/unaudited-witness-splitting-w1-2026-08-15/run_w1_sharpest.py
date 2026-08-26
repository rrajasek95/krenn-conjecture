#!/usr/bin/env python3
"""UNAUDITED PROBE (W1, task A2/B/C) -- the sharpest six-site shadows.

Pinned HEAD: 26ba69f7e643694c6a58464af6e9e1de9ec92f01

The monomial (coordinate rank-one) regime is intrinsically NEAR-EXACT: each
of the fifteen perfect matchings contributes to exactly one word, so at most
twelve mixed words can be violated at all (three matchings must sit in the
pure classes), i.e. every monomial source satisfies at least 714 of the 726
mixed equations by construction.  This is the regime lemma J.1 claims
blocking forces, and it is where the counterexample portrait would have to
live if J.1 were true -- so it is where the sharpest six-site shadows are.

This script samples the regime, pushes the fifteen WEIGHTS toward exactness
with the support-preserving star push (so the source stays monomial), and
asks the two questions that decide the J.1/J.2 bridge at six sites:

  * how far toward exactness does a monomial source go?  (answer: to
    726 - #singleton-classes, the exhaustive bound of run_w1_monomial.py);
  * is any near-exact monomial source ALL-BLOCKED?  -- the constrained
    version of the same push, with "every live pair witness-free" as a hard
    constraint, records the frontier.

Usage: python3 run_w1_sharpest.py [--samples 60] [--jobs 10]
"""

from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import as_completed, ProcessPoolExecutor
from fractions import Fraction
import json
import random
import time

from w1_core import (MIXED_WORDS, NMIXED, PAIRS, SITES, Source,
                     all_coefficients, blocking_metrics, exactness_metrics,
                     impose_words, matrix_rank, push_cycle, require,
                     structure_metrics, support_fibres)
from run_c_pure_hunt import gauge_pure
from run_w1_monomial import (EDGES, MATCHING_EDGES, STATES, classes,
                             disjoint_triples, half_edge_colours)

TRIPLES = disjoint_triples()


def monomial_source(rng, dead_probability=0.0):
    """A random monomial source with three disjoint monochromatic matchings."""
    triple = rng.choice(TRIPLES)
    used = set()
    for index in triple:
        used |= set(MATCHING_EDGES[index])
    free_edges = tuple(edge for edge in EDGES if edge not in used)
    assignment = tuple(None if rng.random() < dead_probability
                       else (rng.randrange(3), rng.randrange(3))
                       for _ in free_edges)
    colours = half_edge_colours(triple, assignment, free_edges)
    blocks = {}
    for edge in EDGES:
        table = [[Fraction(0)] * 3 for _ in range(3)]
        if (edge, edge[0]) in colours:
            table[colours[(edge, edge[0])]][colours[(edge, edge[1])]] = Fraction(
                rng.choice([-3, -2, -1, 1, 2, 3]))
        blocks[edge] = table
    source = Source(blocks)
    table = classes(colours)
    singletons = [word for word, members in table.items()
                  if len(members) == 1 and len(set(word)) > 1]
    return gauge_pure(source), len(singletons), sum(
        1 for state in assignment if state is None)


def compact(source, max_degree=2, blocking=True):
    structure = structure_metrics(source)
    exact = exactness_metrics(source)
    out = {"satisfied": exact["mixed_satisfied"],
           "fraction": round(exact["mixed_satisfied_fraction"], 6),
           "violated": exact["mixed_violated"],
           "singletons": exact["singleton_mixed_fibres"],
           "support": structure["support_size"],
           "kinds": structure["kinds"],
           "noncoordinate": structure["noncoordinate_rank1"]}
    if blocking:
        metrics = blocking_metrics(source, max_degree=max_degree, timeout=30)
        out.update({"live": metrics["live_pairs"],
                    "witness": metrics["witness_pairs"],
                    "blocked": metrics["blocked_pairs"],
                    "all_blocked": metrics["all_live_blocked"],
                    "min_degrees": metrics["min_block_degrees"]})
    return out


def constrained_push(source, rounds=4, seed=0, max_degree=2, min_live=0):
    """Support-preserving push with ALL LIVE PAIRS BLOCKED as a hard constraint."""
    rng = random.Random(seed)
    current = source
    coefficients = all_coefficients(current)
    best = sum(1 for w in MIXED_WORDS if coefficients[w] == 0)
    trace = [{"round": 0, "satisfied": best}]
    for round_index in range(rounds):
        coefficients = all_coefficients(current)
        keep = [w for w in MIXED_WORDS if coefficients[w] == 0]
        fibres = support_fibres(current)
        violated = sorted((w for w in MIXED_WORDS if coefficients[w] != 0),
                          key=lambda w: (fibres[w], w))
        if not violated:
            break
        sizes, size = [], len(violated)
        while size >= 1:
            sizes.append(size)
            size //= 2
        improved = False
        for z in SITES:
            for size in sizes:
                moved, _accepted = impose_words(current, z, violated[:size],
                                                keep, preserve_support=True)
                check = all_coefficients(moved)
                satisfied = sum(1 for w in MIXED_WORDS if check[w] == 0)
                if satisfied <= best:
                    continue
                metrics = blocking_metrics(moved, max_degree=max_degree,
                                           timeout=30)
                if not metrics["all_live_blocked"]:
                    continue
                if metrics["live_pairs"] < min_live:
                    continue
                current, best, improved = moved, satisfied, True
                trace.append({"round": round_index + 1, "site": z,
                              "batch": size, "satisfied": best,
                              "live": metrics["live_pairs"]})
                break
            if improved:
                break
        if not improved:
            break
    return current, trace


def monomial_neighbour(source, rng):
    """Recolour or kill one block, staying monomial and pure-normalisable."""
    for _ in range(20):
        pair = rng.choice(PAIRS)
        blocks = {other: [row[:] for row in source.blocks[other]]
                  for other in PAIRS}
        table = [[Fraction(0)] * 3 for _ in range(3)]
        if rng.random() > 0.12:
            table[rng.randrange(3)][rng.randrange(3)] = Fraction(
                rng.choice([-3, -2, -1, 1, 2, 3]))
        blocks[pair] = table
        candidate = gauge_pure(Source(blocks))
        if candidate is not None:
            return candidate
    return None


def analyse(job):
    """Hunt an ALL-BLOCKED monomial source, then push it toward exactness."""
    seed, dead_probability, tries = job
    rng = random.Random(seed)
    start = time.time()
    attempts = []
    chosen = None
    best_source, best_witness, best_data = None, None, None
    for _ in range(tries):
        source, singleton_classes, dead = monomial_source(rng, dead_probability)
        if source is None:
            continue
        metrics = compact(source, max_degree=2)
        require(metrics["violated"] <= 12,
                "a monomial source can violate at most twelve mixed equations")
        require(metrics["violated"] >= 1,
                "run_w1_monomial: some mixed class is always a singleton")
        attempts.append({"witness": metrics["witness"],
                         "live": metrics["live"],
                         "violated": metrics["violated"],
                         "singletons": metrics["singletons"],
                         "all_blocked": metrics["all_blocked"]})
        if best_witness is None or metrics["witness"] < best_witness:
            best_source, best_witness = source, metrics["witness"]
            best_data = (singleton_classes, dead)
        if metrics["all_blocked"]:
            chosen = (source, singleton_classes, dead)
            break
    climb_steps = 0
    if chosen is None and best_source is not None:
        # hill-climb inside the monomial regime towards all-blocked
        current, witness = best_source, best_witness
        for _step in range(tries):
            candidate = monomial_neighbour(current, rng)
            if candidate is None:
                continue
            climb_steps += 1
            metrics = compact(candidate, max_degree=2)
            if metrics["violated"] < 1 or metrics["witness"] > witness:
                continue
            current, witness = candidate, metrics["witness"]
            if metrics["all_blocked"]:
                chosen = (current, best_data[0], best_data[1])
                break
    out_climb = {"climb_steps": climb_steps, "best_witness": best_witness}
    out = {"seed": seed, "dead_probability": dead_probability,
           "attempts": len(attempts),
           "attempt_all_blocked": sum(1 for row in attempts
                                      if row["all_blocked"]),
           "attempt_witness_histogram": dict(Counter(row["witness"]
                                                     for row in attempts)),
           "attempt_violated_range": [min(row["violated"] for row in attempts),
                                      max(row["violated"] for row in attempts)],
           "found_all_blocked": chosen is not None}
    out.update(out_climb)
    if chosen is None:
        out["seconds"] = round(time.time() - start, 1)
        return out
    source, singleton_classes, dead = chosen
    out.update({"singleton_classes": singleton_classes, "dead_edges": dead})
    base = compact(source, max_degree=4)
    out["base"] = base
    pushed, _keep, _trace = push_cycle(source, rounds=4, preserve_support=True)
    out["free_push"] = compact(pushed, max_degree=4)
    constrained, trace = constrained_push(source, seed=seed)
    out["blocked_push"] = compact(constrained, max_degree=4)
    nodeath, live_trace = constrained_push(source, seed=seed,
                                           min_live=base["live"])
    out["blocked_push_nodeath"] = compact(nodeath, max_degree=4)
    out["trace"] = trace
    out["nodeath_trace"] = live_trace
    out["blocks"] = {str(pair): [[str(value) for value in row]
                                 for row in nodeath.blocks[pair]]
                     for pair in PAIRS}
    out["seconds"] = round(time.time() - start, 1)
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=30)
    parser.add_argument("--jobs", type=int, default=10)
    parser.add_argument("--tries", type=int, default=12)
    parser.add_argument("--out", default="results_sharpest.json")
    args = parser.parse_args()

    jobs = [(40000 + 7 * index + 3 * order, probability, args.tries)
            for order, probability in enumerate((0.0, 0.2))
            for index in range(args.samples)]
    start = time.time()
    results = []
    handle = open(args.out + ".jsonl", "a")
    with ProcessPoolExecutor(max_workers=args.jobs) as pool:
        futures = [pool.submit(analyse, job) for job in jobs]
        for number, future in enumerate(as_completed(futures), 1):
            try:
                result = future.result()
            except Exception as error:                      # keep partials
                print(f"  job failed: {type(error).__name__} {error}",
                      flush=True)
                continue
            if result is None:
                continue
            results.append(result)
            handle.write(json.dumps(result) + "\n")
            handle.flush()
            print(f"  {number}/{len(futures)} ({time.time()-start:.0f}s)",
                  flush=True)
    handle.close()

    hits = [row for row in results if row.get("found_all_blocked")]

    def stats(key):
        rows = [row[key] for row in hits]
        if not rows:
            return {}
        blocked = [row for row in rows if row["all_blocked"]]
        return {
            "fraction_range": [min(row["fraction"] for row in rows),
                               max(row["fraction"] for row in rows)],
            "violated_range": [min(row["violated"] for row in rows),
                               max(row["violated"] for row in rows)],
            "all_blocked": len(blocked),
            "max_fraction_all_blocked": max(
                (row["fraction"] for row in blocked), default=None),
            "witness_histogram": dict(Counter(row["witness"] for row in rows)),
            "live_histogram": dict(Counter(row["live"] for row in rows)),
            "singleton_range": [min(row["singletons"] for row in rows),
                                max(row["singletons"] for row in rows)],
        }

    summary = {
        "instances": len(results),
        "monomial_sources_tested": sum(row["attempts"] for row in results),
        "monomial_all_blocked_found": len(hits),
        "attempt_witness_histogram": dict(Counter(
            witness for row in results
            for witness, count in row["attempt_witness_histogram"].items()
            for _ in range(count))),
        "base": stats("base"),
        "free_push": stats("free_push"),
        "blocked_push": stats("blocked_push"),
        "blocked_push_nodeath": stats("blocked_push_nodeath"),
        "violated_equals_singletons_after_free_push": sum(
            1 for row in hits
            if row["free_push"]["violated"] == row["free_push"]["singletons"]),
        "max_satisfied_all_blocked": max(
            (row[key]["satisfied"] for row in hits
             for key in ("base", "free_push", "blocked_push",
                         "blocked_push_nodeath")
             if row[key]["all_blocked"]), default=None),
    }
    with open(args.out, "w") as handle:
        json.dump({"summary": summary, "results": results}, handle, indent=1)
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
