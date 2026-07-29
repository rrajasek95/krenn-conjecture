#!/usr/bin/env python3
"""Enumerate exact two-inactive-cell charts and find frozen collision pairs.

The reference base is the unweighted alternating Hamilton realization of
``2 X + Y`` on six vertices (the first xx edge has weight two).  We add two
same-shore binary scalar cells of unit weight, retain only charts whose
binary output is still exact, and compute all tangent kernels over Q.

A pair of sites is reported as *frozen* when its all-x direct cofactor is
zero and the all-x Hessian pairing vanishes on the product of the two full
one-z tangent kernels.  Such a pair contradicts the required collision
coefficient 1/2.
"""

from __future__ import annotations

import argparse
import itertools
import random
from fractions import Fraction

from verify_color_collision_n_plus_two import (
    X,
    Y,
    bilinear,
    cycle_factors,
    hessian_matrix,
    nullspace,
    q2_cofactor,
    sector_system,
    weighted_matchings,
)


DECORATIONS = tuple(itertools.product((X, Y), repeat=2))


def base_with(n, first, second):
    px, py = cycle_factors(n)
    q0 = {edge + (X, X): Fraction(1) for edge in px}
    q0[(0, 1, X, X)] = 2
    q0.update({edge + (Y, Y): Fraction(1) for edge in py})
    for edge, decoration in (first, second):
        key = edge + decoration
        if key in q0:
            return None
        q0[key] = 1
    return q0


def exact_binary(n, q0):
    vertices = tuple(range(n))
    for coloring in itertools.product((X, Y), repeat=n):
        value = weighted_matchings(q0, vertices, coloring)
        target = 2 if all(c == X for c in coloring) else 1 if all(c == Y for c in coloring) else 0
        if value != target:
            return False
    return True


def frozen_pairs(n, q0, candidates=None):
    vertices = tuple(range(n))
    sectors = {}
    needed_sites = vertices if candidates is None else set(itertools.chain.from_iterable(candidates))
    for site in needed_sites:
        columns, matrix, _ = sector_system(n, q0, site)
        sectors[site] = columns, nullspace(matrix)
    frozen = []
    pairs = itertools.combinations(vertices, 2) if candidates is None else candidates
    for first, second in pairs:
        if q2_cofactor(n, q0, first, second):
            continue
        first_columns, first_kernel = sectors[first]
        second_columns, second_kernel = sectors[second]
        hessian = hessian_matrix(
            n, q0, first, second, first_columns, second_columns
        )
        if all(
            bilinear(left, hessian, right) == 0
            for left in first_kernel
            for right in second_kernel
        ):
            frozen.append((first, second))
    dimensions = tuple(len(sectors[i][1]) for i in sorted(sectors))
    return tuple(frozen), dimensions


def label(cell):
    edge, decoration = cell
    colors = "xy"
    return f"{edge[0]}{edge[1]}:{colors[decoration[0]]}{colors[decoration[1]]}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=6)
    parser.add_argument(
        "--limit", type=int, default=0,
        help="randomly audit at most this many charts (zero means all)",
    )
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument(
        "--all-pairs", action="store_true",
        help="find every frozen pair, rather than only the two extra edges",
    )
    args = parser.parse_args()
    n = args.n
    if n < 6 or n % 2:
        raise SystemExit("n must be even and at least six")
    shores = (tuple(range(0, n, 2)), tuple(range(1, n, 2)))
    inactive_edges = tuple(
        edge for shore in shores for edge in itertools.combinations(shore, 2)
    )
    cells = tuple(itertools.product(inactive_edges, DECORATIONS))
    charts = [
        (first, second)
        for first_index, first in enumerate(cells)
        for second in cells[first_index + 1 :]
    ]
    if args.limit and len(charts) > args.limit:
        charts = random.Random(args.seed).sample(charts, args.limit)
    exact = 0
    failures = []
    endpoint_failures = []
    hist = {}
    for first, second in charts:
        q0 = base_with(n, first, second)
        if q0 is None or not exact_binary(n, q0):
            continue
        exact += 1
        candidates = None if args.all_pairs else tuple(dict.fromkeys((first[0], second[0])))
        frozen, dimensions = frozen_pairs(n, q0, candidates)
        hist[len(frozen)] = hist.get(len(frozen), 0) + 1
        if not frozen:
            failures.append((first, second, dimensions))
        missing = tuple(
            edge for edge in (first[0], second[0]) if edge not in frozen
        )
        if missing:
            endpoint_failures.append((first, second, missing, frozen))
    print(
        f"n={n} audited_charts={len(charts)} exact_charts={exact} "
        f"frozen_histogram={hist}"
    )
    if failures:
        print("charts without a frozen pair:")
        for first, second, dimensions in failures:
            print(label(first), label(second), dimensions)
        raise SystemExit(1)
    if endpoint_failures:
        print(f"charts whose extra endpoint pair is not frozen: {len(endpoint_failures)}")
        for first, second, missing, frozen in endpoint_failures:
            print(label(first), label(second), "missing", missing, "frozen", frozen)
        raise SystemExit(1)
    print("every exact chart has a frozen pair")
    print("indeed, the endpoint pair of each added cell is frozen")


if __name__ == "__main__":
    main()
