#!/usr/bin/env python3
"""UNAUDITED PROBE (P2, task C) -- the all-pairs-blocked hunt on pure-exact sources.

Pinned HEAD: 86a9479bef38169bbfd8d9100c6d81ce4c66209a

A six-site source cannot be exact (Theorem 1.1 of
proofs/six-site-arbitrary-complex-obstruction.md), so the closest
constructible shadows are used:

  F1 pure-matching   three distinct perfect matchings carry the three
                     diagonal colours with product-one weights, all
                     off-diagonal entries generic (the three PURE GHZ
                     equations hold exactly, mixed ones do not);
  F2 pure-gauged     an arbitrary source normalised by ONE local diagonal
                     gauge at a single site, which multiplies the pure
                     coefficient of colour c by mu_c and therefore sets all
                     three to one whenever they are nonzero;
  F3 census-profile  the rank floor that the forced-anchor theorem imposes on
                     a real exact source (d_R(v) >= 3, i.e. F of maximum
                     degree two), plus the pure normalisation;
  F4 anchored        every block a coordinate rank-one tensor
                     w * e_a (x) e_b with the slice-cover anchor condition
                     at every (vertex, colour), plus the pure normalisation.

For each family we count how many instances have EVERY live pair blocked
(no clean-cap witness anywhere) -- the six-site shadow of the counterexample
portrait -- and run a hill-climb hunt for such a configuration inside the
rank-floor families.

Usage: python3 run_c_pure_hunt.py [--samples 40] [--climb 200] [--jobs 9]
"""

from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from fractions import Fraction
import json
import random
import time

from wsplit_core import (PAIRS, SITES, PairData, Source, classify_source,
                         matrix_rank, perfect_matchings, random_matrix,
                         require)
from run_b_strata import STRATA

ALL_MATCHINGS = perfect_matchings(SITES)


def zero():
    return [[Fraction(0)] * 3 for _ in range(3)]


def gauge_pure(source, site=0):
    """Local diagonal gauge at one site making all pure coefficients one.

    Every perfect matching uses exactly one edge at `site`, and the pure
    coefficient of colour c only sees the (c,c) entries, so scaling row c of
    every block at `site` by mu_c multiplies that coefficient by mu_c.
    Returns None if some pure coefficient already vanishes.
    """
    pure = [source.coefficient((c,) * 6) for c in range(3)]
    if any(value == 0 for value in pure):
        return None
    mu = [Fraction(1) / value for value in pure]
    blocks = {}
    for (u, v) in PAIRS:
        table = [row[:] for row in source.blocks[(u, v)]]
        if u == site:
            table = [[mu[i] * table[i][j] for j in range(3)] for i in range(3)]
        elif v == site:
            table = [[mu[j] * table[i][j] for j in range(3)] for i in range(3)]
        blocks[(u, v)] = table
    out = Source(blocks)
    require(out.pure_defects() == [0, 0, 0], "gauge must normalise pure")
    return out


def family_pure_matching(rng):
    """Three matchings carry the diagonal colours; off-diagonal generic."""
    chosen = rng.sample(ALL_MATCHINGS, 3)
    blocks = {pair: zero() for pair in PAIRS}
    for pair in PAIRS:
        for i in range(3):
            for j in range(3):
                if i != j:
                    blocks[pair][i][j] = Fraction(rng.randint(-4, 4))
    for colour, matching in enumerate(chosen):
        weights = [Fraction(rng.choice([-3, -2, -1, 1, 2, 3])) for _ in range(2)]
        weights.append(Fraction(1) / (weights[0] * weights[1]))
        for weight, (u, v) in zip(weights, matching):
            key = (min(u, v), max(u, v))
            blocks[key][colour][colour] = weight
    source = Source(blocks)
    require(source.pure_defects() == [0, 0, 0], "F1 pure equations")
    return source


def family_pure_gauged(rng, mode="generic"):
    from wsplit_core import random_source
    for _ in range(40):
        source = random_source(rng, mode)
        gauged = gauge_pure(source)
        if gauged is not None:
            return gauged
    return None


def census_profile_source(rng, name=None):
    name = name or rng.choice(list(STRATA))
    defect = {tuple(sorted(edge)) for edge in STRATA[name]}
    blocks = {}
    for pair in PAIRS:
        if pair in defect:
            blocks[pair] = random_matrix(rng, rank=rng.choice([0, 2, 3]))
        else:
            blocks[pair] = random_matrix(rng, rank=1)
    return Source(blocks), name


def family_census_pure(rng):
    for _ in range(40):
        source, name = census_profile_source(rng)
        gauged = gauge_pure(source)
        if gauged is not None:
            return gauged, name
    return None, None


def disjoint_matching_triple(rng, forbidden):
    """Three pairwise disjoint perfect matchings avoiding `forbidden` edges."""
    for _ in range(200):
        chosen = []
        used = set(forbidden)
        for _colour in range(3):
            options = [matching for matching in ALL_MATCHINGS
                       if all(tuple(sorted(edge)) not in used
                              for edge in matching)]
            if not options:
                break
            matching = rng.choice(options)
            chosen.append(matching)
            used.update(tuple(sorted(edge)) for edge in matching)
        if len(chosen) == 3:
            return chosen
    return None


def anchored_source(rng, defect_name="6P1"):
    """Coordinate rank-one blocks with anchors AND nonzero pure coefficients.

    Edge uv carries w * e_a (x) e_b; it supplies vertex u with anchor colour b
    and vertex v with anchor colour a.  The slice-cover anchor condition is
    that every vertex receives all three colours.  Three pairwise disjoint
    perfect matchings are dedicated to the three diagonal colours so that the
    pure coefficients do not vanish identically.
    """
    defect = {tuple(sorted(edge)) for edge in STRATA[defect_name]}
    live = [pair for pair in PAIRS if pair not in defect]
    triple = disjoint_matching_triple(rng, defect)
    if triple is None:
        return None
    colours = {}
    for colour, matching in enumerate(triple):
        for edge in matching:
            colours[tuple(sorted(edge))] = (colour, colour)
    for _ in range(400):
        for pair in live:
            if pair not in colours:
                colours[pair] = (rng.randrange(3), rng.randrange(3))
        supplied = {v: set() for v in SITES}
        for (u, v) in live:
            a, b = colours[(u, v)]
            supplied[u].add(b)
            supplied[v].add(a)
        if all(len(values) == 3 for values in supplied.values()):
            break
        for pair in live:
            if pair not in {tuple(sorted(edge)) for matching in triple
                            for edge in matching}:
                colours.pop(pair, None)
    else:
        return None
    blocks = {}
    for pair in PAIRS:
        if pair in defect:
            blocks[pair] = random_matrix(rng, rank=rng.choice([0, 2, 3]))
        else:
            a, b = colours[pair]
            table = zero()
            table[a][b] = Fraction(rng.choice([-3, -2, -1, 1, 2, 3]))
            blocks[pair] = table
    return Source(blocks)


def family_anchored(rng):
    for _ in range(60):
        name = rng.choice(list(STRATA))
        source = anchored_source(rng, name)
        if source is None:
            continue
        gauged = gauge_pure(source)
        if gauged is not None:
            return gauged, name
    return None, None


def rank_floor(source):
    """min over vertices of the number of incident rank-one blocks."""
    counts = {v: 0 for v in SITES}
    for (u, v) in PAIRS:
        if source.rank(u, v) == 1:
            counts[u] += 1
            counts[v] += 1
    return min(counts.values())


def pattern_blocked_pairs(source):
    """Cheap sufficient blocking test (no Singular): live pairs with a
    degree-2 splitting pattern, plus the dead ones."""
    blocked, live = 0, 0
    for (p, q) in PAIRS:
        pd = PairData(source, p, q)
        if not pd.is_live():
            continue
        live += 1
        patterns, _ = pd.split_patterns()
        if patterns:
            blocked += 1
    return blocked, live


def analyse_instance(job):
    kind, seed = job
    rng = random.Random(seed)
    name = None
    if kind == "F1":
        source = family_pure_matching(rng)
    elif kind == "F2":
        source = family_pure_gauged(rng, "generic")
    elif kind == "F2s":
        source = family_pure_gauged(rng, "sparse")
    elif kind == "F3":
        source, name = family_census_pure(rng)
    elif kind == "F4":
        source, name = family_anchored(rng)
    else:
        raise ValueError(kind)
    if source is None:
        return None
    report = classify_source(source, max_degree=4, timeout=30)
    pairs = []
    for pair in PAIRS:
        record = report[pair]
        pairs.append({"pair": list(pair), "status": record["status"],
                      "span": record["span"], "witness": record["witness"],
                      "patterns": ["*".join(p) for p in record["patterns"]],
                      "min_block_degree": record["min_block_degree"]})
    live = [record for record in pairs if record["status"] != "dead"]
    return {"kind": kind, "seed": seed, "stratum": name,
            "pure_defects": [str(value) for value in source.pure_defects()],
            "rank_floor": rank_floor(source),
            "live_pairs": len(live),
            "witness_pairs": sum(1 for record in live if record["witness"]),
            "all_live_blocked": all(not record["witness"] for record in live),
            "pairs": pairs}


def blocked_score(source, timeout=30):
    """(live pairs with NO clean-cap witness, live pairs) -- exact."""
    report = classify_source(source, max_degree=2, timeout=timeout)
    live = [record for record in report.values() if record["live"]]
    blocked = sum(1 for record in live if record["witness"] is False)
    return blocked, len(live), report


def mutate_anchored(rng, source):
    """Change one coordinate rank-one block, or re-randomise a defect block."""
    blocks = {pair: [row[:] for row in source.blocks[pair]] for pair in PAIRS}
    pair = rng.choice(PAIRS)
    if matrix_rank(blocks[pair]) == 1:
        table = zero()
        table[rng.randrange(3)][rng.randrange(3)] = Fraction(
            rng.choice([-3, -2, -1, 1, 2, 3]))
        blocks[pair] = table
    else:
        blocks[pair] = random_matrix(rng, rank=rng.choice([0, 2, 3]))
    return Source(blocks)


def anchor_ok(source):
    """Slice-cover anchor condition: every vertex sees all three colours on
    the opposite endpoints of its incident rank-one blocks."""
    supplied = {v: set() for v in SITES}
    for (u, v) in PAIRS:
        matrix = source.blocks[(u, v)]
        if matrix_rank(matrix) != 1:
            continue
        rows = [i for i in range(3) if any(matrix[i][j] for j in range(3))]
        cols = [j for j in range(3) if any(matrix[i][j] for i in range(3))]
        if len(rows) == 1:
            supplied[v].add(rows[0])
        if len(cols) == 1:
            supplied[u].add(cols[0])
    return all(len(values) == 3 for values in supplied.values())


def run_hunt(seed, steps=60):
    """Hill-climb for an anchored rank-floor source with EVERY live pair blocked."""
    rng = random.Random(seed)
    source = None
    while source is None:
        name = rng.choice(list(STRATA))
        source = anchored_source(rng, name)
    best = source
    best_blocked, best_live, _ = blocked_score(best)
    trace = [(best_blocked, best_live)]
    for _ in range(steps):
        if best_blocked == best_live:
            break
        candidate = mutate_anchored(rng, best)
        if rank_floor(candidate) < 3 or not anchor_ok(candidate):
            continue
        blocked, live, _ = blocked_score(candidate)
        if blocked - (live - blocked) >= best_blocked - (
                best_live - best_blocked):
            best, best_blocked, best_live = candidate, blocked, live
            trace.append((blocked, live))
    record = {"seed": seed, "stratum": name,
              "blocked": best_blocked, "live": best_live,
              "rank_floor": rank_floor(best), "anchored": anchor_ok(best),
              "all_live_blocked": best_blocked == best_live,
              "trace": trace}
    if best_blocked == best_live:
        gauged = gauge_pure(best)
        record["pure_normalisable"] = gauged is not None
        record["blocks"] = {str(pair): [[str(value) for value in row]
                                        for row in best.blocks[pair]]
                            for pair in PAIRS}
    return record


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=40)
    parser.add_argument("--climb", type=int, default=64)
    parser.add_argument("--jobs", type=int, default=9)
    parser.add_argument("--out", default="results_c.json")
    args = parser.parse_args()

    kinds = ("F1", "F2", "F2s", "F3", "F4")
    jobs = [(kind, 20000 + 17 * index + 3 * order)
            for order, kind in enumerate(kinds)
            for index in range(args.samples)]
    start = time.time()
    results = []
    with ProcessPoolExecutor(max_workers=args.jobs) as pool:
        for number, result in enumerate(pool.map(analyse_instance, jobs), 1):
            if result is not None:
                results.append(result)
            if number % 25 == 0:
                print(f"  families {number}/{len(jobs)} "
                      f"({time.time() - start:.0f}s)", flush=True)

    summary = {}
    for kind in kinds:
        rows = [result for result in results if result["kind"] == kind]
        if not rows:
            continue
        summary[kind] = {
            "instances": len(rows),
            "all_live_blocked": sum(row["all_live_blocked"] for row in rows),
            "witness_pairs": sum(row["witness_pairs"] for row in rows),
            "live_pairs": sum(row["live_pairs"] for row in rows),
            "rank_floor_ge3": sum(row["rank_floor"] >= 3 for row in rows),
            "all_blocked_with_rank_floor": sum(
                row["all_live_blocked"] and row["rank_floor"] >= 3
                for row in rows),
            "status": dict(Counter(record["status"] for row in rows
                                   for record in row["pairs"])),
        }

    hunts = []
    with ProcessPoolExecutor(max_workers=args.jobs) as pool:
        for number, result in enumerate(
                pool.map(run_hunt, range(50000, 50000 + args.climb)), 1):
            hunts.append(result)
            if number % 16 == 0:
                print(f"  hunt {number}/{args.climb} "
                      f"({time.time() - start:.0f}s)", flush=True)
    hunt_summary = {
        "runs": len(hunts),
        "best_blocked_fraction": max(
            (row["blocked"] / row["live"] if row["live"] else 0)
            for row in hunts),
        "runs_with_every_live_pair_blocked": sum(
            1 for row in hunts if row["all_live_blocked"]),
        "pure_normalisable_hits": sum(
            1 for row in hunts if row.get("pure_normalisable")),
        "blocked_live_histogram": dict(Counter(
            f"{row['blocked']}/{row['live']}" for row in hunts)),
        "strata_of_hits": dict(Counter(row["stratum"] for row in hunts
                                       if row["all_live_blocked"])),
    }
    with open(args.out, "w") as handle:
        json.dump({"summary": summary, "hunt": hunt_summary,
                   "results": results, "hunts": hunts}, handle, indent=1)
    print(json.dumps({"families": summary, "hunt": hunt_summary}, indent=1))


if __name__ == "__main__":
    main()
