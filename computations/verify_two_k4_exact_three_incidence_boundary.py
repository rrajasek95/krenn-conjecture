#!/usr/bin/env python3
"""Exact incidence audit for the three-singular two-K4 boundary.

The companion note proves that the three-star and the two-star-plus-isolated
position orbits are impossible.  It also records the exact projective
row-matroid survivors for the path and matching orbits.  CaDiCaL is used
only for the finite 32-status feasibility tables; all geometry entering
those tables is enumerated here by union-find.
"""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
from itertools import combinations, permutations, product

from pysat.solvers import Cadical153

import verify_two_k4_dead_slice_determinantal_boundary as dense
import verify_two_k4_rank2_three_singular_boundary as boundary


VERTICES = tuple(range(4))
COLORS = tuple(range(3))
LINES = dense.dead_coordinate_lines()
ALL_SINGULAR_TYPES = (
    boundary.RANK_TWO_TYPES
    + boundary.RANK_ONE_TYPES
    + boundary.RANK_ZERO_TYPES
)

POSITION_ORBITS = {
    "star": ((0, 0), (1, 0), (2, 0)),
    "star_isolated": ((0, 0), (1, 0), (2, 1)),
    "path": ((0, 0), (0, 1), (1, 0)),
    "matching": ((0, 0), (1, 1), (2, 2)),
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


def position_orbit(positions):
    answer = set()
    for row_permutation, column_permutation in product(
        permutations(VERTICES), repeat=2
    ):
        image = frozenset(
            (row_permutation[row], column_permutation[column])
            for row, column in positions
        )
        answer.add(image)
        answer.add(frozenset((column, row) for row, column in image))
    return answer


def audit_position_orbits():
    orbits = {
        name: position_orbit(positions)
        for name, positions in POSITION_ORBITS.items()
    }
    assert {name: len(orbit) for name, orbit in orbits.items()} == {
        "star": 32,
        "star_isolated": 288,
        "path": 144,
        "matching": 96,
    }
    assert all(
        not orbits[first] & orbits[second]
        for first, second in combinations(orbits, 2)
    )
    assert len(set().union(*orbits.values())) == 560
    assert sum(map(len, orbits.values())) == len(
        tuple(combinations(product(VERTICES, repeat=2), 3))
    )


@lru_cache(maxsize=None)
def status_masks(exceptional_data):
    """All possible exact rank-one-status masks in one block column.

    ``exceptional_data`` consists of ``(vertex, RowMatroid)`` pairs.  A
    zero coordinate row is absent.  A status holds when the remaining
    selected labels span at most one projective point; in particular, an
    empty or singleton selection is automatically a status.

    The rank-two type with three distinct rows is deliberately relaxed by
    forgetting their linear dependence, so the returned table is an upper
    bound for every actual rank-two block.
    """

    exceptional = dict(exceptional_data)
    classes = {
        vertex: exceptional.get(vertex, boundary.INVERTIBLE).projective_classes
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

    answers = set()
    for seed in range(1 << len(LINES)):
        union_find = UnionFind(active)
        for vertex in VERTICES:
            for projective_class in classes[vertex]:
                labels = tuple((vertex, color) for color in projective_class)
                for label in labels[1:]:
                    union_find.union(labels[0], label)

        for triangle, (_hole, assignment) in enumerate(LINES):
            if not (seed >> triangle & 1):
                continue
            selected = tuple(label for label in assignment if label in active)
            for label in selected[1:]:
                union_find.union(selected[0], label)

        valid = True
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
        if not valid:
            continue

        actual = 0
        for triangle, (_hole, assignment) in enumerate(LINES):
            selected = tuple(label for label in assignment if label in active)
            if len({union_find.find(label) for label in selected}) <= 1:
                actual |= 1 << triangle
        answers.add(actual)
    return tuple(sorted(answers))


def cofactor_constraints(positions, row_matroids):
    """Necessary clean/dirty zero-Per3 status constraints."""

    singulars = tuple(
        (row, column, row_matroid)
        for (row, column), row_matroid in zip(positions, row_matroids)
    )
    row_data = {
        row: tuple(
            (column, row_matroid)
            for block_row, column, row_matroid in singulars
            if block_row == row
        )
        for row in VERTICES
    }
    constraints = []
    for triangle, (hole, assignment) in enumerate(LINES):
        references = row_data[hole]
        # The restricted syzygy theorem presently covers at most one
        # singular reference block in a physical block row.
        if len(references) >= 2:
            continue
        known_cofactors = set(VERTICES)
        if references and references[0][1].rank == 0:
            known_cofactors.remove(references[0][0])

        selected_color = dict(assignment)
        for omitted_column in known_cofactors:
            columns = set(VERTICES) - {omitted_column}
            dirty_columns = {
                column
                for row, column, row_matroid in singulars
                if (
                    row != hole
                    and column in columns
                    and selected_color[row] in row_matroid.zero_colors
                )
            }
            demand = 2 if not dirty_columns else int(
                bool(columns - dirty_columns)
            )
            if demand:
                constraints.append(
                    (triangle, tuple(sorted(columns)), demand)
                )
    return tuple(constraints)


def incidence_feasible(positions, row_matroids):
    singulars = tuple(
        (row, column, row_matroid)
        for (row, column), row_matroid in zip(positions, row_matroids)
    )
    domains = []
    for column in VERTICES:
        exceptional = tuple(
            sorted(
                (row, row_matroid)
                for row, block_column, row_matroid in singulars
                if block_column == column
            )
        )
        domains.append(status_masks(exceptional))

    variable = lambda triangle, column: 1 + 8 * column + triangle
    clauses = []
    for column, domain in enumerate(domains):
        domain = set(domain)
        for mask in range(1 << len(LINES)):
            if mask in domain:
                continue
            clauses.append([
                -variable(triangle, column)
                if mask >> triangle & 1
                else variable(triangle, column)
                for triangle in range(len(LINES))
            ])

    for triangle, columns, demand in cofactor_constraints(
        positions, row_matroids
    ):
        if demand == 1:
            clauses.append([
                variable(triangle, column) for column in columns
            ])
        else:
            assert demand == 2 and len(columns) == 3
            clauses.extend(
                [variable(triangle, first), variable(triangle, second)]
                for first, second in combinations(columns, 2)
            )

    with Cadical153(bootstrap_with=clauses) as solver:
        return solver.solve()


def matroid_survivors(orbit_name):
    positions = POSITION_ORBITS[orbit_name]
    return tuple(
        row_matroids
        for row_matroids in product(ALL_SINGULAR_TYPES, repeat=3)
        if incidence_feasible(positions, row_matroids)
    )


def audit_star_and_matching_classifications():
    star_survivors = matroid_survivors("star")
    assert tuple(
        tuple(row_matroid.name for row_matroid in survivor)
        for survivor in star_survivors
    ) == (("0", "0", "0"),)

    matching_survivors = matroid_survivors("matching")
    assert len(matching_survivors) == 28
    rank_histogram = Counter(
        tuple(row_matroid.rank for row_matroid in survivor)
        for survivor in matching_survivors
    )
    assert rank_histogram == {
        (0, 0, 0): 1,
        (0, 0, 1): 4,
        (0, 0, 2): 1,
        (0, 1, 0): 4,
        (0, 1, 1): 3,
        (0, 2, 0): 1,
        (1, 0, 0): 4,
        (1, 0, 1): 3,
        (1, 1, 0): 3,
        (1, 1, 1): 3,
        (2, 0, 0): 1,
    }

    # A rank-two survivor has the other two blocks zero and one prescribed
    # zero coordinate row.  Two or three rank-one survivors have the same
    # singleton row support.
    for survivor in matching_survivors:
        positive = [item for item in survivor if item.rank]
        if any(item.rank == 2 for item in survivor):
            assert len(positive) == 1
        if len(positive) >= 2:
            assert all(item.rank == 1 for item in positive)
            supports = {item.active_colors for item in positive}
            assert len(supports) == 1
            assert len(next(iter(supports))) == 1


def audit_path_classification():
    path_survivors = matroid_survivors("path")
    assert len(path_survivors) == 74
    rank_histogram = Counter(
        tuple(row_matroid.rank for row_matroid in survivor)
        for survivor in path_survivors
    )
    assert rank_histogram == {
        (0, 0, 0): 1,
        (0, 0, 1): 7,
        (0, 0, 2): 7,
        (0, 1, 0): 3,
        (1, 0, 0): 6,
        (1, 0, 1): 20,
        (1, 0, 2): 6,
        (1, 1, 0): 7,
        (2, 0, 0): 7,
        (2, 0, 1): 7,
        (2, 0, 2): 1,
        (2, 1, 0): 2,
    }

    left_rank_patterns = set(rank_histogram)
    # Transposition fixes the corner and exchanges the two arms.
    two_shore_patterns = {
        pattern
        for pattern in left_rank_patterns
        if (pattern[0], pattern[2], pattern[1]) in left_rank_patterns
    }
    assert two_shore_patterns == {
        (0, 0, 0),
        (0, 0, 1),
        (0, 1, 0),
        (1, 0, 0),
        (1, 0, 1),
        (1, 1, 0),
        (2, 0, 0),
        (2, 0, 1),
        (2, 1, 0),
    }
    assert all(
        second == 0 or third == 0
        for _corner, second, third in two_shore_patterns
    )
    assert all(
        second <= 1 and third <= 1
        for _corner, second, third in two_shore_patterns
    )


def main():
    assert len(LINES) == 8
    assert len(ALL_SINGULAR_TYPES) == 15
    audit_position_orbits()
    audit_star_and_matching_classifications()
    audit_path_classification()
    print(
        "PASS: 560 three-edge positions split 32/288/144/96; "
        "star survivor=000; matching row types=28; path row types=74"
    )


if __name__ == "__main__":
    main()
