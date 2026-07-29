#!/usr/bin/env python3
"""Explore the four-singular position boundary in the two-K4 chart.

This is a conservative incidence pass.  Every exceptional block is erased
completely (the zero row-matroid), which weakens both the projective status
conditions and the available reference-row cofactors.  Therefore an orbit
which is infeasible here is impossible for singular blocks of arbitrary
rank.  Survivors are only candidates for a later rank-aware audit.
"""

from __future__ import annotations

import argparse
from collections import Counter
from itertools import combinations, permutations, product

import verify_two_k4_exact_three_incidence_boundary as E3
import verify_two_k4_rank2_three_singular_boundary as boundary


VERTICES = tuple(range(4))
POSITIONS = tuple(product(VERTICES, repeat=2))
ZERO = boundary.RANK_ZERO_TYPES[0]


def canonical(positions):
    positions = tuple(positions)
    images = []
    for row_permutation, column_permutation in product(
        permutations(VERTICES), repeat=2
    ):
        image = tuple(sorted(
            (row_permutation[row], column_permutation[column])
            for row, column in positions
        ))
        images.append(image)
        images.append(tuple(sorted((column, row) for row, column in image)))
    return min(images)


def degree_profile(positions):
    rows = Counter(row for row, _ in positions)
    columns = Counter(column for _, column in positions)
    return tuple(sorted(rows.values(), reverse=True)), tuple(
        sorted(columns.values(), reverse=True)
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rank-aware", action="store_true")
    parser.add_argument("--orbit", type=int)
    args = parser.parse_args()

    orbit_members = {}
    for positions in combinations(POSITIONS, 4):
        representative = canonical(positions)
        orbit_members.setdefault(representative, 0)
        orbit_members[representative] += 1

    assert sum(orbit_members.values()) == 1820
    print(f"position orbits={len(orbit_members)} labelled supports=1820")

    survivors = []
    for index, (positions, size) in enumerate(sorted(orbit_members.items())):
        if args.orbit is not None and index != args.orbit:
            continue
        feasible = E3.incidence_feasible(positions, (ZERO,) * 4)
        profile = degree_profile(positions)
        print(
            f"{index:02d} size={size:4d} profile={profile} "
            f"zero_relaxation={'SURVIVE' if feasible else 'KILLED'} "
            f"positions={positions}"
        )
        if feasible:
            survivors.append((positions, size, profile))

        if args.rank_aware:
            matroid_survivors = []
            rank_histogram = Counter()
            for row_matroids in product(E3.ALL_SINGULAR_TYPES, repeat=4):
                if E3.incidence_feasible(positions, row_matroids):
                    matroid_survivors.append(row_matroids)
                    rank_histogram[tuple(item.rank for item in row_matroids)] += 1
            print(
                f"{index:02d} row-matroid survivors={len(matroid_survivors)} "
                f"rank patterns={len(rank_histogram)} histogram={dict(sorted(rank_histogram.items()))}"
            )

    if args.orbit is None:
        print(
            f"zero-relaxation survivors={len(survivors)}/{len(orbit_members)} "
            f"labelled={sum(size for _, size, _ in survivors)}/1820"
        )


if __name__ == "__main__":
    main()
