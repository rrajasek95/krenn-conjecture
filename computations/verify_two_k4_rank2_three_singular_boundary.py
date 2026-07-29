#!/usr/bin/env python3
"""Exact incidence audit: a rank-two block forces >=3 singular blocks.

The restricted square-free syzygy theorem in
``verify_two_k4_two_singular_boundary.py`` makes the complementary Per_3
cofactors vanish whenever a block row contains at most one singular block
(with the documented one-cofactor exception for a zero block).  This script
audits the resulting oriented-triangle incidence demand against the exact
projective row-matroid capacity when precisely two blocks are singular and
one has rank two.

All positions, both same/different block-column cases, all seven rank-two
row matroids, all seven rank-one row matroids, and the zero matroid are
enumerated.  The minimum demand-capacity gap is positive in every case.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from itertools import combinations, product

import verify_two_k4_dead_slice_determinantal_boundary as dense
import verify_two_k4_two_singular_boundary as previous


COLORS = tuple(range(3))
VERTICES = tuple(range(4))


@dataclass(frozen=True)
class RowMatroid:
    name: str
    rank: int
    projective_classes: tuple[frozenset[int], ...]

    @property
    def active_colors(self) -> frozenset[int]:
        return frozenset().union(*self.projective_classes)

    @property
    def zero_colors(self) -> frozenset[int]:
        return frozenset(COLORS) - self.active_colors


def matroid(name: str, rank: int, classes) -> RowMatroid:
    return RowMatroid(
        name,
        rank,
        tuple(frozenset(projective_class) for projective_class in classes),
    )


INVERTIBLE = matroid("I", 3, ({0}, {1}, {2}))
RANK_TWO_TYPES = (
    # Three distinct nonzero row points; their linear dependence is relaxed.
    (matroid("D", 2, ({0}, {1}, {2})),)
    + tuple(
        matroid(
            f"P{first}{second}",
            2,
            ({first, second}, set(COLORS) - {first, second}),
        )
        for first, second in combinations(COLORS, 2)
    )
    + tuple(
        matroid(
            f"Z{zero}",
            2,
            tuple({color} for color in COLORS if color != zero),
        )
        for zero in COLORS
    )
)
RANK_ONE_TYPES = tuple(
    matroid(
        "S" + "".join(
            str(color) for color in COLORS if support_mask >> color & 1
        ),
        1,
        (
            {
                color
                for color in COLORS
                if support_mask >> color & 1
            },
        ),
    )
    for support_mask in range(1, 1 << len(COLORS))
)
RANK_ZERO_TYPES = (matroid("0", 0, ()),)
TYPES_BY_RANK = {
    2: RANK_TWO_TYPES,
    1: RANK_ONE_TYPES,
    0: RANK_ZERO_TYPES,
}


class UnionFind:
    def __init__(self, active):
        self.parent = {item: item for item in active}

    def find(self, item):
        if self.parent[item] != item:
            self.parent[item] = self.find(self.parent[item])
        return self.parent[item]

    def union(self, first, second):
        first, second = self.find(first), self.find(second)
        if first != second:
            self.parent[second] = first


LINES = dense.dead_coordinate_lines()


@lru_cache(maxsize=None)
def column_capacity(
    exceptional_data: tuple[tuple[int, RowMatroid], ...]
) -> int:
    """Maximum simultaneous oriented-triangle incidences in one column."""
    exceptional = dict(exceptional_data)
    classes = {
        vertex: exceptional.get(vertex, INVERTIBLE).projective_classes
        for vertex in VERTICES
    }
    active = {
        (vertex, color)
        for vertex in VERTICES
        for projective_class in classes[vertex]
        for color in projective_class
    }
    original_class = {
        (vertex, color): class_number
        for vertex in VERTICES
        for class_number, projective_class in enumerate(classes[vertex])
        for color in projective_class
    }

    maximum = 0
    for mask in range(1 << len(LINES)):
        union_find = UnionFind(active)
        for vertex in VERTICES:
            for projective_class in classes[vertex]:
                for first, second in combinations(projective_class, 2):
                    union_find.union((vertex, first), (vertex, second))

        valid = True
        for line_number, (_hole, assignment) in enumerate(LINES):
            if not (mask >> line_number & 1):
                continue
            if not all(label in active for label in assignment):
                valid = False
                break
            union_find.union(assignment[0], assignment[1])
            union_find.union(assignment[0], assignment[2])
        if not valid:
            continue

        # Triangle equalities may not identify two initially distinct row
        # points belonging to the same physical block.
        for vertex in VERTICES:
            labels = [
                (vertex, color)
                for projective_class in classes[vertex]
                for color in projective_class
            ]
            for first, second in combinations(labels, 2):
                if (
                    union_find.find(first) == union_find.find(second)
                    and original_class[first] != original_class[second]
                ):
                    valid = False
                    break
            if not valid:
                break
        if valid:
            maximum = max(maximum, mask.bit_count())
    return maximum


def minimum_triangle_demand(
    hole: int,
    assignment: tuple[tuple[int, int], ...],
    singulars: tuple[tuple[int, int, RowMatroid], ...],
) -> int:
    """Minimum rank-one incidences forced in one triangle context."""
    selected_color = dict(assignment)
    bad_columns = {
        column
        for row, column, row_matroid in singulars
        if row != hole and selected_color[row] in row_matroid.zero_colors
    }
    good_columns = set(VERTICES) - bad_columns

    # A positive-rank reference block gives all four zero cofactors.  A zero
    # reference block gives the three cofactors except the one omitting its
    # own column, exactly as in the restricted-syzygy theorem.
    known_cofactors = set(VERTICES)
    for row, column, row_matroid in singulars:
        if row == hole and row_matroid.rank == 0:
            known_cofactors.remove(column)

    good_triple_constraints = []
    for omitted_column in known_cofactors:
        triple = set(VERTICES) - {omitted_column}
        if triple <= good_columns:
            good_triple_constraints.append(triple)

    # Lemma 3.1 of the two-singular note says every good zero-Per3 triple
    # contains at least two rank-one maps.  Exhaust the four incidence bits.
    minimum = 5
    for mask in range(1 << 4):
        incidences = {
            column for column in VERTICES if mask >> column & 1
        }
        if not incidences <= good_columns:
            continue
        if all(
            len(incidences & triple) >= 2
            for triple in good_triple_constraints
        ):
            minimum = min(minimum, len(incidences))
    assert minimum <= 4
    return minimum


def incidence_demand(
    singulars: tuple[tuple[int, int, RowMatroid], ...]
) -> int:
    return sum(
        minimum_triangle_demand(hole, assignment, singulars)
        for hole, assignment in LINES
    )


def incidence_capacity(
    singulars: tuple[tuple[int, int, RowMatroid], ...]
) -> int:
    total = 0
    for column in VERTICES:
        exceptional = tuple(
            sorted(
                (row, row_matroid)
                for row, block_column, row_matroid in singulars
                if block_column == column
            )
        )
        total += column_capacity(exceptional)
    return total


def audit_all_two_block_configurations() -> None:
    # If the two blocks originally share a block row, transpose the full
    # equations; their two column indices are distinct, so they then occupy
    # distinct block rows.  It therefore suffices to audit distinct rows.
    expected_statistics = {
        # (minimum demand, maximum capacity, minimum correlated gap)
        (2, True): (20, 16, 6),
        (2, False): (19, 16, 5),
        (1, True): (18, 15, 5),
        (1, False): (16, 14, 3),
        (0, True): (15, 14, 2),
        (0, False): (14, 14, 1),
    }
    actual_statistics = {}
    configuration_count = 0

    for second_rank in (2, 1, 0):
        for same_column in (True, False):
            minimum_gap = 100
            minimum_demand = 100
            maximum_capacity = 0
            for first_row, second_row in product(VERTICES, repeat=2):
                if first_row == second_row:
                    continue
                for first_column in VERTICES:
                    second_columns = (
                        (first_column,)
                        if same_column
                        else tuple(
                            column
                            for column in VERTICES
                            if column != first_column
                        )
                    )
                    for second_column in second_columns:
                        for first_type, second_type in product(
                            RANK_TWO_TYPES, TYPES_BY_RANK[second_rank]
                        ):
                            singulars = (
                                (first_row, first_column, first_type),
                                (second_row, second_column, second_type),
                            )
                            demand = incidence_demand(singulars)
                            capacity = incidence_capacity(singulars)
                            assert demand > capacity
                            minimum_demand = min(minimum_demand, demand)
                            maximum_capacity = max(maximum_capacity, capacity)
                            minimum_gap = min(
                                minimum_gap, demand - capacity
                            )
                            configuration_count += 1
            actual_statistics[second_rank, same_column] = (
                minimum_demand,
                maximum_capacity,
                minimum_gap,
            )

    assert actual_statistics == expected_statistics
    assert configuration_count == 20160
    print(
        "minimum demand-capacity gaps: "
        + ", ".join(
            f"rank(2,{rank})/{'same' if same else 'different'}-column={statistics[2]}"
            for (rank, same), statistics in sorted(
                actual_statistics.items(), reverse=True
            )
        )
    )


def audit_column_capacity_bounds() -> None:
    # The ordinary invertible-column capacity is the known four.  Even two
    # rank-two row matroids in one column do not increase it.  A rank-one or
    # zero second block lowers the joint maxima to three or two.
    assert column_capacity(()) == 4
    joint_maxima = {}
    for second_rank in (2, 1, 0):
        joint_maxima[second_rank] = max(
            column_capacity(((0, first), (1, second)))
            for first, second in product(
                RANK_TWO_TYPES, TYPES_BY_RANK[second_rank]
            )
        )
    assert joint_maxima == {2: 4, 1: 3, 0: 2}


def main() -> None:
    assert len(LINES) == 8
    assert len(RANK_TWO_TYPES) == 7
    assert len(RANK_ONE_TYPES) == 7
    previous.audit_syzygies()
    previous.audit_rank_one_slice()
    audit_column_capacity_bounds()
    audit_all_two_block_configurations()
    print(
        "PASS: exactly two singular blocks with a rank-two member are impossible"
    )


if __name__ == "__main__":
    main()
