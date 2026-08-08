#!/usr/bin/env python3
"""Exact torus-orbit feasibility audit for two-cell additions at N=8.

Let A be the sixteen-source anchored family from the one-cell four-cut gate,
and add nonzero weights at two distinct coordinates outside its support.  The
characters are computed modulo the base-support and Delta-stabilizer
characters over Q.

Pairs of quotient rank two have a zero-dimensional coefficient quotient over
C: both weights can be normalized simultaneously to one.  The checker tests
all such representatives by rebuilding the full tensor and all relevant cut
spaces exactly.  Rank-zero and rank-one pairs retain respectively two and one
continuous coefficient moduli, so the checker certifies their census but does
not pretend that a finite coefficient sample eliminates them.
"""

from __future__ import annotations

import importlib.util
from collections import Counter
from fractions import Fraction
from itertools import combinations
from pathlib import Path


Q = Fraction


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load_one_cell_elimination():
    path = Path(__file__).with_name(
        "verify_n8_four_cut_arbitrary_weight_one_cell_elimination.py"
    )
    spec = importlib.util.spec_from_file_location("one_cell_elimination", path)
    require(spec is not None and spec.loader is not None, "cannot load one-cell audit")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def quotient_remainder(vector, basis):
    """Return the exact normal form modulo a row-echelon sparse basis."""
    remainder = {index: Q(value) for index, value in vector.items() if value}
    # rational_basis inserts pivots in source order, not necessarily numerical
    # order.  Numerical order is required because each pivot row may contain
    # only indices strictly above its pivot.
    for pivot in sorted(basis):
        coefficient = remainder.get(pivot, Q(0))
        if not coefficient:
            continue
        for index, value in basis[pivot].items():
            updated = remainder.get(index, Q(0)) - coefficient * value
            if updated:
                remainder[index] = updated
            else:
                remainder.pop(index, None)
    require(
        not set(remainder).intersection(basis),
        "quotient reduction left a constrained pivot",
    )
    return remainder


def projective_key(vector):
    if not vector:
        return ()
    pivot = min(vector)
    scale = vector[pivot]
    return tuple(sorted((index, value / scale) for index, value in vector.items()))


def pair_quotient_rank(left_key, right_key):
    if not left_key:
        return 0 if not right_key else 1
    if not right_key:
        return 1
    return 1 if left_key == right_key else 2


def build_character_census(one_cell, module, base):
    support = one_cell.support_coordinates(base)
    require(len(support) == 16, "anchored support size changed")
    absent = tuple(
        coordinate
        for coordinate in one_cell.all_coordinates()
        if coordinate not in support
    )
    require(len(absent) == 236, "absent-coordinate count changed")

    constraint_vectors = [
        one_cell.coordinate_character(coordinate) for coordinate in sorted(support)
    ]
    constraint_vectors.extend(one_cell.target_characters())
    constraint_basis = module.rational_basis(constraint_vectors)
    require(len(constraint_basis) == 15, "constraint rank changed")

    keys = {
        coordinate: projective_key(
            quotient_remainder(
                one_cell.coordinate_character(coordinate), constraint_basis
            )
        )
        for coordinate in absent
    }
    classes = {}
    for coordinate, key in keys.items():
        classes.setdefault(key, []).append(coordinate)

    dependent = tuple(classes.get((), ()))
    require(
        set(dependent) == set(one_cell.DEPENDENT_WITNESSES),
        "dependent-coordinate set changed",
    )
    nonzero_histogram = Counter(
        len(coordinates) for key, coordinates in classes.items() if key
    )
    require(
        nonzero_histogram
        == Counter({1: 10, 2: 46, 6: 2, 7: 8, 8: 6, 12: 1}),
        "projective quotient-character histogram changed",
    )
    require(
        sum(nonzero_histogram.values()) == 73,
        "projective quotient-character class count changed",
    )

    pair_records = []
    rank_counts = Counter()
    basis_vectors = list(constraint_basis.values())
    for left, right in combinations(absent, 2):
        quotient_rank = pair_quotient_rank(keys[left], keys[right])
        direct_rank = (
            len(
                module.rational_basis(
                    basis_vectors
                    + [
                        one_cell.coordinate_character(left),
                        one_cell.coordinate_character(right),
                    ]
                )
            )
            - len(constraint_basis)
        )
        require(
            quotient_rank == direct_rank,
            f"projective/direct pair rank mismatch at {(left, right)}",
        )
        pair_records.append((left, right, quotient_rank))
        rank_counts[quotient_rank] += 1

    require(
        rank_counts == Counter({0: 15, 1: 1858, 2: 25857}),
        "two-cell quotient-rank census changed",
    )
    require(sum(rank_counts.values()) == 27730, "pair census is incomplete")

    same_nonzero_line_pairs = sum(
        len(coordinates) * (len(coordinates) - 1) // 2
        for key, coordinates in classes.items()
        if key
    )
    require(same_nonzero_line_pairs == 478, "same-line pair count changed")
    require(
        rank_counts[1] == len(dependent) * (len(absent) - len(dependent))
        + same_nonzero_line_pairs,
        "rank-one pair decomposition changed",
    )
    require(
        rank_counts[0] == len(dependent) * (len(dependent) - 1) // 2,
        "rank-zero pair decomposition changed",
    )
    return pair_records, rank_counts, nonzero_histogram


def add_two_cells(module, base, left, right):
    cells = {edge: list(entries) for edge, entries in base.items()}
    module.add_sources(cells, ((*left, Q(1)), (*right, Q(1))))
    return cells


def audit_zero_dimensional_orbits(one_cell, unit_gate, module, base, records):
    counts = Counter()
    for left, right, quotient_rank in records:
        if quotient_rank != 2:
            continue
        counts["representatives"] += 1
        cells = add_two_cells(module, base, left, right)
        tensor = module.matching_tensor(module.B, cells)
        if unit_gate.pure_tuple(module, tensor) != (1, 1, 1):
            continue
        counts["pure"] += 1
        if not all(
            unit_gate.active_complete(module.cut_record(z, cells))
            for z in unit_gate.THREE_CUTS
        ):
            continue
        counts["triple"] += 1
        for z in unit_gate.FOURTH_CUT_CANDIDATES:
            if unit_gate.active_complete(module.cut_record(z, cells)):
                counts["fourth"] += 1
                raise RuntimeError(
                    "four-cut two-cell falsifier found in a rank-two orbit: "
                    f"cells={(left, right)}, cut={z}"
                )

    require(
        counts
        == Counter(
            {
                "representatives": 25857,
                "pure": 25857,
                "triple": 89,
                "fourth": 0,
            }
        ),
        "zero-dimensional two-cell orbit census changed",
    )
    return counts


def main() -> None:
    one_cell = load_one_cell_elimination()
    unit_gate = one_cell.load_unit_gate()
    module = unit_gate.load_three_cut_verifier()
    base = unit_gate.build_base(module)
    unit_gate.audit_base(module, base)

    records, rank_counts, class_histogram = build_character_census(
        one_cell, module, base
    )
    search_counts = audit_zero_dimensional_orbits(
        one_cell, unit_gate, module, base, records
    )

    print("N=8 two-cell torus-orbit feasibility audit: PASS")
    print("absent-cell pairs: 27,730")
    print(
        "quotient ranks: "
        f"rank-2={rank_counts[2]}, rank-1={rank_counts[1]}, rank-0={rank_counts[0]}"
    )
    print(
        "nonzero projective character classes: "
        f"73; size histogram={dict(sorted(class_histogram.items()))}"
    )
    print(
        "rank-2 exact representatives: "
        f"pure={search_counts['pure']}, triple-active={search_counts['triple']}, "
        f"fourth-cut={search_counts['fourth']}"
    )
    print(
        "stopping verdict: 1,873 positive-dimensional pair families remain; "
        "the full two-cell problem is not a finite orbit enumeration"
    )


if __name__ == "__main__":
    main()
