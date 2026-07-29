#!/usr/bin/env python3
"""Exact audit of the low-rank exact-two singular boundary.

The rank-two audit leaves rank pairs (1,1), (1,0), and (0,0).  This script
uses its conservative good-triangle incidence demand and exact projective
row-matroid capacity to exclude (1,1), and to show that in every orientation
where the rank-one and zero blocks occupy distinct block rows, the rank-one
block has exactly one nonzero row.
"""

from __future__ import annotations

from itertools import product

import verify_two_k4_rank2_three_singular_boundary as boundary


def configuration_statistics(first_rank: int, second_rank: int):
    """Return exact demand/capacity statistics in the two position orbits."""

    statistics = {}
    types = product(
        boundary.TYPES_BY_RANK[first_rank],
        boundary.TYPES_BY_RANK[second_rank],
    )
    type_pairs = tuple(types)

    for same_column in (True, False):
        demand_values = []
        capacity_values = []
        gaps = []
        for first_row, second_row in product(boundary.VERTICES, repeat=2):
            if first_row == second_row:
                continue
            for first_column in boundary.VERTICES:
                second_columns = (
                    (first_column,)
                    if same_column
                    else tuple(
                        column
                        for column in boundary.VERTICES
                        if column != first_column
                    )
                )
                for second_column in second_columns:
                    for first_type, second_type in type_pairs:
                        singulars = (
                            (first_row, first_column, first_type),
                            (second_row, second_column, second_type),
                        )
                        demand = boundary.incidence_demand(singulars)
                        capacity = boundary.incidence_capacity(singulars)
                        demand_values.append(demand)
                        capacity_values.append(capacity)
                        gaps.append(demand - capacity)

        statistics[same_column] = {
            "count": len(gaps),
            "minimum_demand": min(demand_values),
            "maximum_capacity": max(capacity_values),
            "minimum_gap": min(gaps),
            "nonpositive_gaps": sum(gap <= 0 for gap in gaps),
        }
    return statistics


def rank_one_zero_statistics():
    """Refine the (1,0) audit by the row support of the rank-one block."""

    statistics = {}
    zero_type = boundary.RANK_ZERO_TYPES[0]
    for support_size in (1, 2, 3):
        rank_one_types = tuple(
            row_matroid
            for row_matroid in boundary.RANK_ONE_TYPES
            if len(row_matroid.active_colors) == support_size
        )
        for same_column in (True, False):
            demand_values = []
            capacity_values = []
            gaps = []
            for first_row, second_row in product(
                boundary.VERTICES, repeat=2
            ):
                if first_row == second_row:
                    continue
                for first_column in boundary.VERTICES:
                    second_columns = (
                        (first_column,)
                        if same_column
                        else tuple(
                            column
                            for column in boundary.VERTICES
                            if column != first_column
                        )
                    )
                    for second_column in second_columns:
                        for rank_one_type in rank_one_types:
                            singulars = (
                                (first_row, first_column, rank_one_type),
                                (second_row, second_column, zero_type),
                            )
                            demand = boundary.incidence_demand(singulars)
                            capacity = boundary.incidence_capacity(singulars)
                            demand_values.append(demand)
                            capacity_values.append(capacity)
                            gaps.append(demand - capacity)

            statistics[support_size, same_column] = {
                "count": len(gaps),
                "minimum_demand": min(demand_values),
                "maximum_capacity": max(capacity_values),
                "minimum_gap": min(gaps),
                "nonpositive_gaps": sum(gap <= 0 for gap in gaps),
            }
    return statistics


def audit_rank_one_pair() -> None:
    expected = {
        True: {
            "count": 2352,
            "minimum_demand": 16,
            "maximum_capacity": 14,
            "minimum_gap": 4,
            "nonpositive_gaps": 0,
        },
        False: {
            "count": 7056,
            "minimum_demand": 14,
            "maximum_capacity": 12,
            "minimum_gap": 2,
            "nonpositive_gaps": 0,
        },
    }
    actual = configuration_statistics(1, 1)
    assert actual == expected


def audit_rank_one_zero_pair() -> None:
    expected = {
        (1, True): {
            "count": 144,
            "minimum_demand": 12,
            "maximum_capacity": 13,
            "minimum_gap": 0,
            "nonpositive_gaps": 48,
        },
        (2, True): {
            "count": 144,
            "minimum_demand": 15,
            "maximum_capacity": 13,
            "minimum_gap": 2,
            "nonpositive_gaps": 0,
        },
        (3, True): {
            "count": 48,
            "minimum_demand": 18,
            "maximum_capacity": 13,
            "minimum_gap": 5,
            "nonpositive_gaps": 0,
        },
        (1, False): {
            "count": 432,
            "minimum_demand": 11,
            "maximum_capacity": 12,
            "minimum_gap": -1,
            "nonpositive_gaps": 432,
        },
        (2, False): {
            "count": 432,
            "minimum_demand": 14,
            "maximum_capacity": 12,
            "minimum_gap": 2,
            "nonpositive_gaps": 0,
        },
        (3, False): {
            "count": 144,
            "minimum_demand": 18,
            "maximum_capacity": 12,
            "minimum_gap": 6,
            "nonpositive_gaps": 0,
        },
    }
    actual = rank_one_zero_statistics()
    assert actual == expected


def main() -> None:
    assert len(boundary.LINES) == 8
    assert len(boundary.RANK_ONE_TYPES) == 7
    assert len(boundary.RANK_ZERO_TYPES) == 1
    audit_rank_one_pair()
    audit_rank_one_zero_pair()
    print(
        "PASS: exact-two rank(1,1) is impossible; rank(1,0) has singleton "
        "row support whenever the exceptional blocks occupy distinct rows"
    )


if __name__ == "__main__":
    main()
