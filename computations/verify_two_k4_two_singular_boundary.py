#!/usr/bin/env python3
"""Exact audit that one singular cross block is still impossible.

The proof is in ``notes/two-k4-two-singular-boundary.md``.  This checker
audits the square-free syzygy ranks, the zero-diagonal slice determinant,
the rank-one incidence demand, and every projective row-matroid capacity
used in the count.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations, permutations, product

from flint import fmpz_mat

import verify_two_k4_dead_slice_determinantal_boundary as dense


def square_free_syzygy_matrix(dimensions):
    """Matrix of sum_j x_j C_j for factors of the given dimensions.

    Every vector ``x_j`` takes values in the matching coordinate subspace
    of a common three-dimensional output.  Dimensions are therefore at most
    three.  Each ``C_j`` is square-free of degree one in all other factors.
    """

    columns = []
    for missing in range(len(dimensions)):
        other_ranges = [
            range(dimensions[factor])
            for factor in range(len(dimensions)) if factor != missing
        ]
        for indices in product(*other_ranges):
            columns.append((missing, indices))

    row_index = {}
    entries = []
    for column, (missing, indices) in enumerate(columns):
        full = [None] * len(dimensions)
        iterator = iter(indices)
        for factor in range(len(dimensions)):
            if factor != missing:
                full[factor] = next(iterator)
        for output_coordinate in range(dimensions[missing]):
            full[missing] = output_coordinate
            key = (output_coordinate, tuple(full))
            row = row_index.setdefault(key, len(row_index))
            entries.append((row, column))

    rows = [[0] * len(columns) for _ in row_index]
    for row, column in entries:
        rows[row][column] = 1
    return fmpz_mat(rows)


def audit_syzygies():
    three_vector = square_free_syzygy_matrix((3, 3, 3))
    assert (three_vector.ncols(), three_vector.rank()) == (27, 27)

    expected = {
        1: (54, 53),
        2: (81, 80),
        3: (108, 107),
    }
    for first_dimension, (columns, rank) in expected.items():
        matrix = square_free_syzygy_matrix(
            (first_dimension, 3, 3, 3)
        )
        assert (matrix.ncols(), matrix.rank()) == (columns, rank)


def polynomial_add(answer, monomial, coefficient):
    answer[monomial] = answer.get(monomial, 0) + coefficient
    if answer[monomial] == 0:
        del answer[monomial]


def audit_rank_one_slice():
    # Determinant of [[0,a2,a1],[a2,0,a0],[a1,a0,0]].
    entries = (
        (None, (0, 0, 1), (0, 1, 0)),
        ((0, 0, 1), None, (1, 0, 0)),
        ((0, 1, 0), (1, 0, 0), None),
    )
    determinant = {}
    for sigma in permutations(range(3)):
        if any(entries[row][sigma[row]] is None for row in range(3)):
            continue
        inversions = sum(
            sigma[i] > sigma[j]
            for i, j in combinations(range(3), 2)
        )
        exponent = tuple(
            sum(entries[row][sigma[row]][coordinate] for row in range(3))
            for coordinate in range(3)
        )
        polynomial_add(determinant, exponent, (-1) ** inversions)
    assert determinant == {(1, 1, 1): 2}

    # If every three-subset of four maps needs at least two rank-one maps,
    # at least three of the four maps are rank one.
    valid_all_triples = []
    valid_three_triples = []
    for mask in range(1 << 4):
        all_triples = all(
            sum(bool(mask & (1 << index)) for index in triple) >= 2
            for triple in combinations(range(4), 3)
        )
        if all_triples:
            valid_all_triples.append(mask)

        # Rank-zero B_00 at a hole-zero line gives only the triples that
        # contain right column zero.
        selected = ((0, 1, 2), (0, 1, 3), (0, 2, 3))
        three_triples = all(
            sum(bool(mask & (1 << index)) for index in triple) >= 2
            for triple in selected
        )
        if three_triples:
            valid_three_triples.append(mask)
    assert min(mask.bit_count() for mask in valid_all_triples) == 3
    assert min(mask.bit_count() for mask in valid_three_triples) == 3


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


def valid_incidence_masks(lines, active_colors_at_zero, rank_one_at_zero):
    active = {
        (vertex, color)
        for vertex in range(4) for color in range(3)
        if vertex != 0 or color in active_colors_at_zero
    }
    answers = []
    for mask in range(1 << len(lines)):
        union_find = UnionFind(active)
        active_zero = sorted(active_colors_at_zero)
        if rank_one_at_zero and active_zero:
            for color in active_zero[1:]:
                union_find.union((0, active_zero[0]), (0, color))

        valid = True
        for index, (_hole, assignment) in enumerate(lines):
            if not (mask & (1 << index)):
                continue
            if not all(label in active for label in assignment):
                valid = False
                break
            union_find.union(assignment[0], assignment[1])
            union_find.union(assignment[0], assignment[2])
        if not valid:
            continue

        # Invertible blocks at vertices 1,2,3 have three distinct row
        # points.  At vertex zero, prescribed rank-one identifications are
        # allowed; in the rank-two cases all active points are required
        # distinct below.
        if any(
            union_find.find((vertex, first))
            == union_find.find((vertex, second))
            for vertex in (1, 2, 3)
            for first, second in combinations(range(3), 2)
        ):
            continue
        if not rank_one_at_zero and any(
            union_find.find((0, first)) == union_find.find((0, second))
            for first, second in combinations(sorted(active_colors_at_zero), 2)
        ):
            continue
        answers.append(mask)
    return answers


def audit_incidence_capacities():
    lines = dense.dead_coordinate_lines()
    assert len(lines) == 8

    # A good block column: all four local row triples are projectively
    # distinct.  This recovers the 1,8,16,8,2 table.
    good = valid_incidence_masks(lines, {0, 1, 2}, False)
    assert Counter(mask.bit_count() for mask in good) == {
        0: 1, 1: 8, 2: 16, 3: 8, 4: 2
    }

    # Rank two at B_00.  Its possibilities are three distinct nonzero row
    # points, one proportional pair, or one zero row plus two distinct row
    # points.  The first and third are checked directly.  Pre-unioning one
    # pair only lowers the maximum (checked separately here).
    rank_two_maxima = []
    rank_two_maxima.append(max(mask.bit_count() for mask in good))
    for zero_color in range(3):
        active = set(range(3)) - {zero_color}
        masks = valid_incidence_masks(lines, active, False)
        rank_two_maxima.append(max(mask.bit_count() for mask in masks))

    # One proportional pair with all rows nonzero: a dedicated version of
    # the finite table, allowing precisely that pre-existing equality.
    for pair in combinations(range(3), 2):
        active = {(vertex, color) for vertex in range(4) for color in range(3)}
        valid_masks = []
        for mask in range(1 << len(lines)):
            union_find = UnionFind(active)
            union_find.union((0, pair[0]), (0, pair[1]))
            for index, (_hole, assignment) in enumerate(lines):
                if mask & (1 << index):
                    union_find.union(assignment[0], assignment[1])
                    union_find.union(assignment[0], assignment[2])
            valid = True
            for vertex in (1, 2, 3):
                valid &= all(
                    union_find.find((vertex, first))
                    != union_find.find((vertex, second))
                    for first, second in combinations(range(3), 2)
                )
            third = next(color for color in range(3) if color not in pair)
            valid &= union_find.find((0, pair[0])) != union_find.find((0, third))
            if valid:
                valid_masks.append(mask)
        rank_two_maxima.append(max(mask.bit_count() for mask in valid_masks))
    assert max(rank_two_maxima) == 4

    # Rank one: every nonzero row of B_00 is one projective point.  Audit
    # all seven nonempty supports.  Rank zero is the empty support.
    rank_one_maxima = []
    for support_mask in range(1, 1 << 3):
        support = {
            color for color in range(3) if support_mask & (1 << color)
        }
        masks = valid_incidence_masks(lines, support, True)
        rank_one_maxima.append(max(mask.bit_count() for mask in masks))
    rank_zero = valid_incidence_masks(lines, set(), True)
    assert max(rank_one_maxima) == 2
    assert max(mask.bit_count() for mask in rank_zero) == 2

    # Each zero colour row occurs in two non-hole triangle contexts.
    non_hole_color_counts = Counter(
        dict(assignment)[0]
        for hole, assignment in lines if hole != 0
    )
    assert non_hole_color_counts == {0: 2, 1: 2, 2: 2}

    # Demand 24-2z versus capacity of three good columns and the bad one.
    rank_data = {
        2: (1, 4),  # z <= 1, exceptional-column capacity <= 4
        1: (2, 2),  # z <= 2, exceptional-column capacity <= 2
        0: (3, 2),  # z = 3, exceptional-column capacity <= 2
    }
    for rank, (maximum_zero_rows, exceptional_capacity) in rank_data.items():
        demand = 24 - 2 * maximum_zero_rows
        capacity = 3 * 4 + exceptional_capacity
        assert demand > capacity, (rank, demand, capacity)


def main():
    audit_syzygies()
    audit_rank_one_slice()
    audit_incidence_capacities()
    print(
        "PASS: restricted syzygies=27/27,53/54,80/81,107/108; "
        "incidence demand rank2/1/0 >=22/20/18 > capacity 16/14/14"
    )


if __name__ == "__main__":
    main()
