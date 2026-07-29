#!/usr/bin/env python3
"""Exact audit that the two-K4 dead slabs forbid exactly two singular blocks.

The proof is in ``notes/two-k4-no-exact-two-singular.md``.  It uses two
small weighted incidence certificates after erasing the row vectors from
the two exceptional blocks.  Erasure is a relaxation: any genuine rank-one
local map remains rank at most one after one of its vectors is deleted.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations

import verify_two_k4_dead_slice_determinantal_boundary as dense
import verify_two_k4_two_singular_boundary as previous


VERTICES = tuple(range(4))
LINES = dense.dead_coordinate_lines()


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


@dataclass(frozen=True)
class CofactorConstraint:
    triangle: int
    omitted_column: int
    demand: int

    @property
    def columns(self):
        return frozenset(VERTICES) - {self.omitted_column}


def selected_labels(triangle: int, erased_vertices=frozenset()):
    """Selected projective row labels after the declared erasures."""

    _hole, assignment = LINES[triangle]
    return tuple(
        label for label in assignment if label[0] not in erased_vertices
    )


def statuses_are_compatible(triangles, erased_vertices=frozenset()):
    """Whether the displayed relaxed rank-one statuses can coexist.

    All non-erased physical blocks are invertible, so their three row
    labels must remain in distinct projective classes.
    """

    active = {
        (vertex, colour)
        for vertex in VERTICES if vertex not in erased_vertices
        for colour in range(3)
    }
    union_find = UnionFind(active)
    for triangle in triangles:
        labels = selected_labels(triangle, erased_vertices)
        for label in labels[1:]:
            union_find.union(labels[0], label)
    return all(
        union_find.find((vertex, first))
        != union_find.find((vertex, second))
        for vertex in VERTICES if vertex not in erased_vertices
        for first, second in combinations(range(3), 2)
    )


def exact_capacity(triangles, erased_vertices=frozenset()):
    triangles = tuple(triangles)
    return max(
        len(subset)
        for mask in range(1 << len(triangles))
        if statuses_are_compatible(
            subset := tuple(
                triangle
                for index, triangle in enumerate(triangles)
                if mask >> index & 1
            ),
            erased_vertices,
        )
    )


def universal_cofactor_is_known(
    constraint: CofactorConstraint, singular_positions
):
    """C_j is known zero without using the ranks of the singular blocks.

    A nonsingular reference row supplies all four cofactors.  A reference
    row containing one singular block supplies every cofactor except
    possibly the one omitting that block's own column; positive rank would
    supply that last cofactor too, but the relaxation deliberately forgets
    it.
    """

    hole, _assignment = LINES[constraint.triangle]
    return all(
        not (row == hole and column == constraint.omitted_column)
        for row, column in singular_positions
    )


def expected_demand(constraint, singular_positions):
    """Universal demand from the clean/dirty zero-Per3 lemmas."""

    hole, _assignment = LINES[constraint.triangle]
    dirty_columns = {
        column
        for row, column in singular_positions
        if row != hole and column in constraint.columns
    }
    if not dirty_columns:
        return 2
    if constraint.columns - dirty_columns:
        return 1
    return 0


def audit_aligned_certificate():
    # The erased exceptional blocks are B_00 and B_10.  For triangles 4
    # and 6, C_0 is a clean zero cofactor on columns 1,2,3.
    singular_positions = ((0, 0), (1, 0))
    constraints = (
        CofactorConstraint(4, 0, 2),
        CofactorConstraint(6, 0, 2),
    )
    assert all(
        universal_cofactor_is_known(constraint, singular_positions)
        for constraint in constraints
    )
    assert all(
        expected_demand(constraint, singular_positions)
        == constraint.demand
        for constraint in constraints
    )

    capacities = []
    for column in (1, 2, 3):
        participating = tuple(
            constraint.triangle
            for constraint in constraints if column in constraint.columns
        )
        assert participating == (4, 6)
        # The two statuses share row (0,0) but use distinct rows 1 and 2
        # at vertex 1, so they cannot coexist in an invertible block column.
        assert not statuses_are_compatible(participating)
        capacities.append(exact_capacity(participating))
    assert sum(constraint.demand for constraint in constraints) == 4
    assert capacities == [1, 1, 1]
    assert sum(capacities) == 3


def audit_disjoint_certificate():
    # The erased exceptional blocks are B_00 and B_11.
    singular_positions = ((0, 0), (1, 1))
    constraints = (
        CofactorConstraint(0, 1, 2),
        CofactorConstraint(1, 1, 2),
        CofactorConstraint(2, 0, 2),
        CofactorConstraint(3, 0, 2),
        CofactorConstraint(5, 2, 1),
        CofactorConstraint(7, 2, 1),
    )
    assert all(
        universal_cofactor_is_known(constraint, singular_positions)
        for constraint in constraints
    )
    assert all(
        expected_demand(constraint, singular_positions)
        == constraint.demand
        for constraint in constraints
    )

    # Each tuple partitions all statuses counted in that physical column
    # into incompatible pairs.  Hence its length is a capacity bound.
    pair_certificates = {
        0: ((0, 7), (1, 5)),
        1: ((2, 7), (3, 5)),
        2: ((0, 3), (1, 2)),
        3: ((0, 3), (1, 2), (5, 7)),
    }
    capacities = []
    for column in VERTICES:
        participating = tuple(
            constraint.triangle
            for constraint in constraints if column in constraint.columns
        )
        pairs = pair_certificates[column]
        assert sorted(item for pair in pairs for item in pair) \
            == sorted(participating)
        erased_vertices = frozenset(
            row
            for row, block_column in singular_positions
            if block_column == column
        )
        assert all(
            not statuses_are_compatible(pair, erased_vertices)
            for pair in pairs
        )
        capacity = exact_capacity(participating, erased_vertices)
        assert capacity == len(pairs)
        capacities.append(capacity)

    assert sum(constraint.demand for constraint in constraints) == 10
    assert capacities == [2, 2, 2, 3]
    assert sum(capacities) == 9


def main():
    assert len(LINES) == 8
    previous.audit_syzygies()
    previous.audit_rank_one_slice()
    audit_aligned_certificate()
    audit_disjoint_certificate()
    print(
        "PASS: exact-two singular blocks are impossible; "
        "aligned certificate 4>3, disjoint certificate 10>9"
    )


if __name__ == "__main__":
    main()
