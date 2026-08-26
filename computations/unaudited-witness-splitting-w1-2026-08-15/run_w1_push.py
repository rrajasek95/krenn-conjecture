#!/usr/bin/env python3
"""UNAUDITED PROBE (W1, task A/B) -- the exactness push on P2's all-blocked shadows.

Pinned HEAD: 26ba69f7e643694c6a58464af6e9e1de9ec92f01

Input: the 36 pure-normalisable all-blocked six-site shadows of
computations/unaudited-witness-splitting-p2-2026-08-15/results_c.json
(hunt records with all_live_blocked and pure_normalisable), plus the
explicit example_all_blocked.json.  Each is gauge-normalised to pure = 1
by P2's own gauge (`gauge_pure`), which P2 verified leaves every pair's
witness/blocking status unchanged.

Five experiments per shadow (all exact; blocking decided by Singular over Q):

 E0 baseline        structure / exactness / blocking metrics of the shadow.
 E1 prefix push     minimal deformation imposing the k most constrained
                    violated mixed equations (fewest support terms first) at
                    one site, for k on a geometric ladder: WHEN does a witness
                    appear, WHEN do the rank-one blocks stop being coordinate,
                    WHEN do singleton mixed fibres appear.
 E2 cyclic push     the same imposition cycled over all six sites until it
                    stalls (unconstrained by blocking): how close to exact can
                    the shadow be pushed at all, and what is the structure at
                    the stall.
 E3 frontier        the same push with ALL-BLOCKED as a hard constraint:
                    the largest fraction of mixed equations reachable while
                    every live pair stays witness-free.
 E4 decoordination  replace one coordinate rank-one block by a non-coordinate
                    rank-one block of the same support pattern: does
                    all-blockedness survive?  (The direct J.1 contrapositive
                    probe at fixed defect stratum.)

Usage: python3 run_w1_push.py [--jobs 9] [--out results_push.json]
       [--limit N] [--skip-frontier]
"""

from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import as_completed, ProcessPoolExecutor
from fractions import Fraction
import json
import os
import random
import time

from w1_core import (MIXED_WORDS, NMIXED, PAIRS, PURE_WORDS, SITES, Source,
                     all_coefficients, apply_star, blocking_metrics,
                     cofactor_tables, exactness_metrics, IncSystem,
                     matrix_rank, push_at_site, push_cycle, require,
                     star_index, star_row, star_vector, STAR_DIM,
                     structure_metrics, support_fibres)
from run_c_pure_hunt import gauge_pure

P2DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                     "unaudited-witness-splitting-p2-2026-08-15")


# ------------------------------------------------------------- shadows


def parse_blocks(table):
    blocks = {}
    for key, matrix in table.items():
        pair = tuple(int(part) for part in key.strip("()").split(","))
        blocks[pair] = [[Fraction(entry) for entry in row] for row in matrix]
    return Source(blocks)


def load_shadows():
    """The 36 pure-normalisable all-blocked hunt hits + the explicit example."""
    with open(os.path.join(P2DIR, "results_c.json")) as handle:
        data = json.load(handle)
    shadows = []
    for record in data["hunts"]:
        if not record.get("all_live_blocked") or not record.get(
                "pure_normalisable"):
            continue
        raw = parse_blocks(record["blocks"])
        gauged = gauge_pure(raw)
        require(gauged is not None, "shadow must be pure-normalisable")
        require(gauged.pure_defects() == [0, 0, 0], "shadow pure = 1")
        shadows.append({"id": f"hunt{record['seed']}", "seed": record["seed"],
                        "stratum": record["stratum"], "source": gauged})
    with open(os.path.join(P2DIR, "example_all_blocked.json")) as handle:
        example = json.load(handle)
    shadows.append({"id": "example", "seed": example["hunt_seed"],
                    "stratum": example["defect_graph"],
                    "source": parse_blocks(example["blocks"])})
    return shadows


def snapshot(source, max_degree=4, timeout=12, with_blocking=True):
    entry = {"structure": structure_metrics(source),
             "exactness": exactness_metrics(source)}
    if with_blocking:
        entry["blocking"] = blocking_metrics(source, max_degree=max_degree,
                                             timeout=timeout)
    return entry


def compact(source, blocking=True, max_degree=2):
    st = structure_metrics(source)
    ex = exactness_metrics(source)
    out = {"satisfied": ex["mixed_satisfied"],
           "fraction": round(ex["mixed_satisfied_fraction"], 6),
           "singletons": ex["singleton_mixed_fibres"],
           "support": st["support_size"],
           "rank1": st["rank1_blocks"],
           "noncoordinate_rank1": st["noncoordinate_rank1"],
           "kinds": st["kinds"]}
    if blocking:
        bl = blocking_metrics(source, max_degree=max_degree, timeout=12)
        out.update({"live": bl["live_pairs"], "witness": bl["witness_pairs"],
                    "blocked": bl["blocked_pairs"],
                    "undecided": len(bl["undecided_pairs"]),
                    "all_blocked": bl["all_live_blocked"],
                    "min_degrees": bl["min_block_degrees"]})
    return out


# ------------------------------------------------------ E1 prefix push


def impose_prefix(source, z, words, keep, x0_shift=None, rng=None):
    """Least-change star at z imposing pure=1, `keep`, and as many of `words`.

    Returns (source, accepted_count) or (None, 0) if the projection is
    impossible (never happens: the current star is always a solution of the
    hard part).
    """
    tables = cofactor_tables(source, z)
    systems = {c: IncSystem(STAR_DIM) for c in range(3)}
    for c in range(3):
        require(systems[c].add_row(star_row(tables, z, PURE_WORDS[c]),
                                   Fraction(1)), "pure row inconsistent")
    for word in keep:
        require(systems[word[z]].add_row(star_row(tables, z, word),
                                         Fraction(0)),
                "kept row inconsistent")
    accepted = 0
    for word in words:
        if systems[word[z]].add_row(star_row(tables, z, word), Fraction(0)):
            accepted += 1
    vectors = {}
    for c in range(3):
        base = star_vector(source, z, c)
        if x0_shift is not None and rng is not None:
            base = [value + Fraction(rng.randint(-x0_shift, x0_shift), 4)
                    for value in base]
        vectors[c] = systems[c].project(base)
    return apply_star(source, z, vectors), accepted


def best_site(source, keep, violated):
    """Site whose star can absorb the most of the violated equations."""
    scores = {}
    for z in SITES:
        moved, accepted = impose_prefix(source, z, violated, keep)
        coefficients = all_coefficients(moved)
        scores[z] = sum(1 for w in MIXED_WORDS if coefficients[w] == 0)
    return max(scores, key=lambda z: scores[z]), scores


def ladder(total):
    steps = []
    value = 1
    while value < total:
        steps.append(value)
        value *= 2
    steps.append(total)
    return steps


def experiment_prefix(source, max_degree=2):
    coefficients = all_coefficients(source)
    keep = [w for w in MIXED_WORDS if coefficients[w] == 0]
    fibres = support_fibres(source)
    violated = sorted((w for w in MIXED_WORDS if coefficients[w] != 0),
                      key=lambda w: (fibres[w], w))
    z, scores = best_site(source, keep, violated)
    out = {"site": z, "site_scores": scores, "violated": len(violated),
           "checkpoints": []}
    for count in ladder(len(violated)):
        moved, accepted = impose_prefix(source, z, violated[:count], keep)
        entry = {"k": count, "accepted_of_k": accepted}
        entry.update(compact(moved, max_degree=max_degree))
        out["checkpoints"].append(entry)
    return out


# ------------------------------------------------------- E3 frontier


def experiment_frontier(source, rounds=4, samples=1, seed=0, max_degree=2,
                        min_live=0):
    """Maximise satisfied mixed equations subject to ALL LIVE PAIRS BLOCKED.

    Batched greedy: at each round try, for every site and every batch size on a
    descending ladder, the least-change imposition of that batch; accept the
    first candidate that increases the satisfied count AND keeps every live
    pair witness-free.  Two extra random points of the affine solution set are
    tried per batch (the projection is only one point of it).

    `min_live` additionally forbids pairs from dying: with min_live equal to the
    starting number of live pairs the search cannot buy blockedness by killing
    edges (the honest version -- the support floor forbids dead edges in the
    real counterexample portrait).
    """
    rng = random.Random(seed)
    current = source
    coefficients = all_coefficients(current)
    best = sum(1 for w in MIXED_WORDS if coefficients[w] == 0)
    trace = [{"round": 0, "satisfied": best,
              "fraction": round(best / NMIXED, 6)}]
    for round_index in range(rounds):
        coefficients = all_coefficients(current)
        keep = [w for w in MIXED_WORDS if coefficients[w] == 0]
        fibres = support_fibres(current)
        violated = sorted((w for w in MIXED_WORDS if coefficients[w] != 0),
                          key=lambda w: (fibres[w], w))
        if not violated:
            break
        improved = False
        sizes, size = [], len(violated)
        while size >= 1 and len(sizes) < 5:
            sizes.append(size)
            size //= 4
        if sizes[-1] != 1:
            sizes.append(1)
        for z in SITES:
            for size in sizes:
                for sample in range(samples):
                    shift = None if sample == 0 else 4
                    moved, _accepted = impose_prefix(
                        current, z, violated[:size], keep,
                        x0_shift=shift, rng=rng)
                    check = all_coefficients(moved)
                    satisfied = sum(1 for w in MIXED_WORDS if check[w] == 0)
                    if satisfied <= best:
                        continue
                    metrics = blocking_metrics(moved, max_degree=max_degree,
                                               timeout=12)
                    if not metrics["all_live_blocked"]:
                        continue
                    if metrics["live_pairs"] < min_live:
                        continue
                    current, best, improved = moved, satisfied, True
                    trace.append({"round": round_index + 1, "site": z,
                                  "batch": size, "sample": sample,
                                  "satisfied": best,
                                  "fraction": round(best / NMIXED, 6),
                                  "live": metrics["live_pairs"]})
                    break
                if improved:
                    break
            if improved:
                break
        if not improved:
            break
    return current, trace


# -------------------------------------------------- E4 decoordination


def spread_block(matrix, mode, rng):
    """Make a coordinate rank-one block non-coordinate, same rank."""
    entries = [(i, j) for i in range(3) for j in range(3) if matrix[i][j]]
    if len(entries) != 1:
        return None
    (a, b), value = entries[0], matrix[entries[0][0]][entries[0][1]]
    x = [Fraction(0)] * 3
    y = [Fraction(0)] * 3
    x[a] = Fraction(1)
    y[b] = value
    if mode in ("rows", "both"):
        other = rng.choice([i for i in range(3) if i != a])
        x[other] = Fraction(rng.choice([1, 2, -1, -2]))
    if mode in ("cols", "both"):
        other = rng.choice([j for j in range(3) if j != b])
        y[other] = value * Fraction(rng.choice([1, 2, -1, -2]))
    return [[x[i] * y[j] for j in range(3)] for i in range(3)]


def experiment_decoordination(source, seed=0, samples=2, max_degree=2):
    """Does all-blockedness survive making one rank-one block non-coordinate?"""
    rng = random.Random(seed)
    survivors = []
    out = []
    for pair in PAIRS:
        matrix = source.blocks[pair]
        if matrix_rank(matrix) != 1:
            continue
        if sum(1 for i in range(3) for j in range(3) if matrix[i][j]) != 1:
            continue                      # already non-coordinate
        for mode in ("cols", "rows", "both"):
            for sample in range(samples):
                spread = spread_block(matrix, mode, rng)
                blocks = {other: [row[:] for row in source.blocks[other]]
                          for other in PAIRS}
                blocks[pair] = spread
                candidate = Source(blocks)
                gauged = gauge_pure(candidate)
                entry = {"pair": list(pair), "mode": mode, "sample": sample,
                         "gaugeable": gauged is not None}
                if gauged is None:
                    out.append(entry)
                    continue
                metrics = blocking_metrics(gauged, max_degree=max_degree,
                                           timeout=12)
                exact = exactness_metrics(gauged)
                entry.update({"live": metrics["live_pairs"],
                              "witness": metrics["witness_pairs"],
                              "all_blocked": metrics["all_live_blocked"],
                              "satisfied": exact["mixed_satisfied"]})
                if metrics["all_live_blocked"]:
                    survivors.append((entry, gauged))
                out.append(entry)
    total = [entry for entry in out if entry.get("all_blocked") is not None]
    return {"trials": out,
            "n_trials": len(total),
            "n_all_blocked": sum(1 for entry in total if entry["all_blocked"]),
            "n_gauge_failed": sum(1 for entry in out if not entry["gaugeable"]),
            "survivors": survivors}


# -------------------------------------------------------------- driver


def analyse(shadow, do_frontier=True):
    start = time.time()
    source = shadow["source"]
    out = {"id": shadow["id"], "seed": shadow["seed"],
           "stratum": shadow["stratum"]}
    out["base"] = snapshot(source, max_degree=4)
    out["prefix"] = experiment_prefix(source)
    seen = {"satisfied": None}

    def cycle_checkpoint(state):
        exact = exactness_metrics(state)
        blocking = exact["mixed_satisfied"] != seen["satisfied"]
        seen["satisfied"] = exact["mixed_satisfied"]
        return compact(state, blocking=blocking, max_degree=2)

    final, keep, trace = push_cycle(source, rounds=4,
                                   checkpoint=cycle_checkpoint)
    out["cycle"] = {"trace": trace, "final": snapshot(final, max_degree=4)}
    base_live = out["base"]["blocking"]["live_pairs"]
    if do_frontier:
        for name, min_live in (("frontier_nodeath", base_live),):
            best, frontier_trace = experiment_frontier(
                source, seed=shadow["seed"], min_live=min_live)
            out[name] = {"trace": frontier_trace,
                         "min_live": min_live,
                         "final": snapshot(best, max_degree=4),
                         "blocks": {str(pair): [[str(v) for v in row]
                                                for row in best.blocks[pair]]
                                    for pair in PAIRS}}
    decoordination = experiment_decoordination(source, seed=shadow["seed"])
    survivors = decoordination.pop("survivors")
    out["decoordination"] = decoordination
    # E5: the same constrained frontier from a NON-COORDINATE all-blocked
    # source of the same defect stratum -- the J.1 comparison.
    out["noncoordinate_frontier"] = []
    if do_frontier:
        for entry, candidate in survivors[:1]:
            best, ftrace = experiment_frontier(
                candidate, rounds=3, seed=shadow["seed"] + 1,
                min_live=base_live)
            out["noncoordinate_frontier"].append(
                {"origin": entry, "trace": ftrace,
                 "final": snapshot(best, max_degree=4)})
    out["seconds"] = round(time.time() - start, 1)
    return out


def verdict(record):
    """Outcome class of one shadow."""
    base = record["base"]
    first_witness = None
    for entry in record["prefix"]["checkpoints"]:
        if entry["witness"] > 0:
            first_witness = entry
            break
    cycle_final = record["cycle"]["final"]
    frontier = record.get("frontier", {}).get("final")
    out = {
        "id": record["id"],
        "stratum": record["stratum"],
        "base_fraction": round(base["exactness"]["mixed_satisfied_fraction"], 4),
        "base_singletons": base["exactness"]["singleton_mixed_fibres"],
        "base_noncoordinate": base["structure"]["noncoordinate_rank1"],
        "base_live": base["blocking"]["live_pairs"],
        "witness_onset_k": first_witness["k"] if first_witness else None,
        "witness_onset_fraction": first_witness["fraction"] if first_witness
                                  else None,
        "witness_onset_of_violated": (
            round(first_witness["k"] / record["prefix"]["violated"], 4)
            if first_witness else None),
        "cycle_fraction": round(
            cycle_final["exactness"]["mixed_satisfied_fraction"], 4),
        "cycle_witness": cycle_final["blocking"]["witness_pairs"],
        "cycle_live": cycle_final["blocking"]["live_pairs"],
        "cycle_singletons": cycle_final["exactness"]["singleton_mixed_fibres"],
        "cycle_noncoordinate": cycle_final["structure"]["noncoordinate_rank1"],
        "decoord_all_blocked": record["decoordination"]["n_all_blocked"],
        "decoord_trials": record["decoordination"]["n_trials"],
    }
    for key, prefix in (("frontier", "frontier"),
                        ("frontier_nodeath", "nodeath")):
        entry = record.get(key, {}).get("final")
        if not entry:
            continue
        out.update({
            f"{prefix}_fraction": round(
                entry["exactness"]["mixed_satisfied_fraction"], 4),
            f"{prefix}_live": entry["blocking"]["live_pairs"],
            f"{prefix}_witness": entry["blocking"]["witness_pairs"],
            f"{prefix}_singletons": entry["exactness"]["singleton_mixed_fibres"],
            f"{prefix}_noncoordinate": entry["structure"]["noncoordinate_rank1"],
            f"{prefix}_support": entry["structure"]["support_size"],
        })
    noncoordinate = record.get("noncoordinate_frontier") or []
    if noncoordinate:
        out["nc_frontier_fractions"] = [
            round(item["final"]["exactness"]["mixed_satisfied_fraction"], 4)
            for item in noncoordinate]
        out["nc_frontier_noncoordinate"] = [
            item["final"]["structure"]["noncoordinate_rank1"]
            for item in noncoordinate]
    if first_witness is not None:
        out["class"] = "witness-appeared"
    elif out.get("frontier_fraction", 0) >= 0.999:
        out["class"] = "frontier-near-exact-blocked"
    else:
        out["class"] = "frontier-stuck"
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--jobs", type=int, default=9)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--skip-frontier", action="store_true")
    parser.add_argument("--out", default="results_push.json")
    args = parser.parse_args()

    shadows = load_shadows()
    if args.limit:
        shadows = shadows[:args.limit]
    print(f"shadows: {len(shadows)}", flush=True)
    jobs = [(shadow, not args.skip_frontier) for shadow in shadows]
    start = time.time()
    results = []
    handle = open(args.out + ".jsonl", "a")
    with ProcessPoolExecutor(max_workers=args.jobs) as pool:
        futures = [pool.submit(_run, job) for job in jobs]
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
    table = [verdict(record) for record in results]
    summary = {
        "shadows": len(results),
        "classes": dict(Counter(row["class"] for row in table)),
        "witness_onset_k": dict(Counter(str(row["witness_onset_k"])
                                        for row in table)),
        "base_all_coordinate": sum(1 for row in table
                                   if row["base_noncoordinate"] == 0),
        "decoordination_all_blocked_total": sum(row["decoord_all_blocked"]
                                                for row in table),
        "decoordination_trials_total": sum(row["decoord_trials"]
                                           for row in table),
        "frontier_fractions": sorted(row.get("frontier_fraction")
                                     for row in table
                                     if row.get("frontier_fraction") is not None),
        "nodeath_fractions": sorted(row.get("nodeath_fraction")
                                    for row in table
                                    if row.get("nodeath_fraction") is not None),
        "nc_frontier_fractions": sorted(
            value for row in table
            for value in row.get("nc_frontier_fractions", [])),
        "cycle_fractions": sorted(row["cycle_fraction"] for row in table),
        "cycle_witness_pairs": sorted(row["cycle_witness"] for row in table),
    }
    with open(args.out, "w") as handle:
        json.dump({"summary": summary, "table": table, "results": results},
                  handle, indent=1)
    print(json.dumps(summary, indent=1))


def _run(job):
    shadow, do_frontier = job
    return analyse(shadow, do_frontier)


if __name__ == "__main__":
    main()
