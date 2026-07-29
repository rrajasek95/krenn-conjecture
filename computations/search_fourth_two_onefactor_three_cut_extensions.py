#!/usr/bin/env python3
"""Exact reconnaissance after adding two diagonal one-factors to BASE.

This is a finite falsification search, not a theorem about arbitrary edge
tensors.  It starts from ``BASE`` in
``search_fourth_onefactor_three_cut_extensions.py`` and adds two decorated
one-factors.  Each added factor has one colour and one scalar weight; if two
decorated factors use the same underlying edge, their edge-cell contributions
are both retained (and hence add in every matching expansion).

The targeted scan first reconstructs all maximizers from the corresponding
one-extra search, then appends every candidate from the requested pool.  The
full scan enumerates unordered pairs from that pool.  Every reported cut is
tested exactly over Q using the existing ``cut_record`` routine.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
from itertools import combinations_with_replacement
from multiprocessing import Pool

from search_fourth_onefactor_three_cut_extensions import (
    ALL_MATCHINGS,
    BASE,
    cut_record,
)


Extra = tuple[tuple[tuple[int, int], ...], int, int]


def make_edge_cells(extras: tuple[Extra, ...]):
    cells: dict[tuple[int, int], list[tuple[int, Fraction]]] = {}
    for colour, matching in enumerate(BASE):
        for pair in matching:
            cells.setdefault(pair, []).append((colour, Fraction(1)))
    for matching, colour, weight in extras:
        for pair in matching:
            cells.setdefault(pair, []).append((colour, Fraction(weight)))
    return cells


def replay(extras: tuple[Extra, ...]):
    records = tuple(cut_record(z, make_edge_cells(extras)) for z in range(6))
    good = tuple(
        z for z, (complete, defect) in enumerate(records)
        if complete and defect
    )
    return good, records


def pool(weights: tuple[int, ...]) -> tuple[Extra, ...]:
    return tuple(
        (matching, colour, weight)
        for weight in weights
        for colour in range(3)
        for matching in ALL_MATCHINGS
    )


def one_extra_maximizers(candidates: tuple[Extra, ...]):
    best = -1
    maximizers: list[tuple[Extra, tuple[int, ...], tuple[tuple[bool, int], ...]]] = []
    for extra in candidates:
        good, records = replay((extra,))
        if len(good) > best:
            best = len(good)
            maximizers = [(extra, good, records)]
        elif len(good) == best:
            maximizers.append((extra, good, records))
    return best, maximizers


def evaluate_pair(pair):
    first, second = pair
    good, records = replay((first, second))
    return first, second, good, records


def scan_pairs(pairs, stop_at: int | None, workers: int):
    scanned = 0
    best = -1
    maximizers = []
    first_hit = None
    process_pool = Pool(workers) if workers > 1 else None
    iterator = (
        process_pool.imap(evaluate_pair, pairs, chunksize=64)
        if process_pool is not None
        else map(evaluate_pair, pairs)
    )
    for first, second, good, records in iterator:
        scanned += 1
        item = (first, second, good, records)
        if len(good) > best:
            best = len(good)
            maximizers = [item]
        elif len(good) == best:
            maximizers.append(item)
        if stop_at is not None and len(good) >= stop_at:
            first_hit = item
            break
    if process_pool is not None:
        if first_hit is not None:
            process_pool.terminate()
        else:
            process_pool.close()
        process_pool.join()
    return scanned, best, maximizers, first_hit


def describe(item) -> str:
    first, second, good, records = item
    return (
        f"first={first} second={second} cuts={good} records={records}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--weights",
        default="-3,-2,-1,1,2,3",
        help="comma-separated nonzero integer weights",
    )
    parser.add_argument(
        "--mode", choices=("targeted", "full", "cross"), default="targeted"
    )
    parser.add_argument(
        "--stop-at", type=int, default=3,
        help="stop at the first configuration with this many active cuts; 0 disables",
    )
    parser.add_argument(
        "--workers", type=int, default=1,
        help="number of exact-Q worker processes",
    )
    args = parser.parse_args()
    weights = tuple(int(value) for value in args.weights.split(","))
    if not weights or 0 in weights or len(set(weights)) != len(weights):
        raise SystemExit("weights must be a nonempty list of distinct nonzero integers")
    candidates = pool(weights)
    stop_at = args.stop_at or None

    if args.mode == "targeted":
        one_best, seeds = one_extra_maximizers(candidates)
        print(
            f"one_extra_pool={len(candidates)} one_extra_best={one_best} "
            f"one_extra_maximizers={len(seeds)}"
        )
        pairs = (
            (seed[0], candidate)
            for seed in seeds
            for candidate in candidates
        )
        nominal = len(seeds) * len(candidates)
    elif args.mode == "full":
        pairs = combinations_with_replacement(candidates, 2)
        nominal = len(candidates) * (len(candidates) + 1) // 2
    else:
        if len(weights) != 2:
            raise SystemExit("cross mode requires exactly two weights")
        first_pool = pool((weights[0],))
        second_pool = pool((weights[1],))
        pairs = (
            (first, second) for first in first_pool for second in second_pool
        )
        nominal = len(first_pool) * len(second_pool)

    if args.workers < 1:
        raise SystemExit("workers must be positive")
    scanned, best, maximizers, hit = scan_pairs(pairs, stop_at, args.workers)
    if hit is None:
        assert scanned == nominal
    print(
        f"mode={args.mode} weights={weights} pool={len(candidates)} "
        f"nominal_pairs={nominal} scanned={scanned} "
        f"max_active_complete_cuts={best} stopped={hit is not None}"
    )
    for item in maximizers[:20]:
        print(describe(item))
    print(f"maximizing_records_seen={len(maximizers)}")


if __name__ == "__main__":
    main()
