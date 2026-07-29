#!/usr/bin/env python3
"""Independent audit of the exact-nine two-K4 frontier reduction.

This intentionally reimplements the position rules, the full
S4-by-S4-by-transpose action, the padded-pair containments, the disjoint
literal-zero logic, and the K3,3 local countermodel without importing the
frontier checker.
"""

from __future__ import annotations

import itertools

import sympy as sp
from sympy.polys.matrices import DomainMatrix


SITES = tuple(range(4))
COLORS = tuple(range(3))
CELLS = tuple(itertools.product(SITES, repeat=2))
EDGES = tuple(itertools.combinations(SITES, 2))
WORDS = tuple(itertools.product(COLORS, repeat=4))
PERMUTATIONS = tuple(itertools.permutations(SITES))


def row_support(description: str) -> frozenset[tuple[int, int]]:
    return frozenset(
        (row, int(column))
        for row, columns in enumerate(description.split("|"))
        for column in columns
    )


REPRESENTATIVES = tuple(
    map(
        row_support,
        (
            "0123|01|02|0",
            "012|012|012|",
            "012|012|03|3",
            "012|013|023|",
            "012|013|02|2",
            "012|01|03|23",
            "012|013|23|2",
            "012|01|23|23",
            "012|03|13|23",
        ),
    )
)
EXPECTED_ORBIT_SIZES = (288, 16, 288, 192, 576, 576, 576, 144, 96)


def transpose(support) -> frozenset[tuple[int, int]]:
    return frozenset((column, row) for row, column in support)


def degrees(support, side: int) -> tuple[int, ...]:
    return tuple(
        sum(position[side] == vertex for position in support)
        for vertex in SITES
    )


def survives_position_rules(support) -> bool:
    # Pre-seven full-row/two-defect and two-singleton rules.
    for side in (0, 1):
        local = degrees(support, side)
        if any(
            local[vertex] == 0
            and any(
                other != vertex and local[other] <= 2
                for other in SITES
            )
            for vertex in SITES
        ):
            return False
        if sum(value <= 1 for value in local) >= 2:
            return False

    # Separated singleton-plus-degree-two rule on either shore.
    for oriented in (support, transpose(support)):
        local = degrees(oriented, 0)
        for singleton in (
            vertex for vertex in SITES if local[vertex] == 1
        ):
            singleton_column = next(
                column
                for row, column in oriented
                if row == singleton
            )
            for degree_two in (
                vertex for vertex in SITES if local[vertex] == 2
            ):
                exceptions = {
                    column
                    for row, column in oriented
                    if row == degree_two
                }
                if singleton_column not in exceptions:
                    return False
    return True


def full_orbit(support) -> set[frozenset[tuple[int, int]]]:
    orbit = set()
    for row_permutation, column_permutation in itertools.product(
        PERMUTATIONS,
        repeat=2,
    ):
        image = frozenset(
            (row_permutation[row], column_permutation[column])
            for row, column in support
        )
        orbit.add(image)
        orbit.add(transpose(image))
    return orbit


def perfect_matchings_in_complement(support) -> int:
    return sum(
        all((row, permutation[row]) not in support for row in SITES)
        for permutation in PERMUTATIONS
    )


def audit_census() -> None:
    survivors = {
        frozenset(support)
        for support in itertools.combinations(CELLS, 9)
        if survives_position_rules(frozenset(support))
    }
    assert len(survivors) == 2752

    orbits = tuple(full_orbit(support) for support in REPRESENTATIVES)
    assert tuple(map(len, orbits)) == EXPECTED_ORBIT_SIZES
    assert sum(map(len, orbits)) == len(set().union(*orbits))
    assert set().union(*orbits) == survivors
    assert tuple(map(perfect_matchings_in_complement, REPRESENTATIVES)) == (
        0,
        0,
        0,
        1,
        1,
        1,
        2,
        2,
        2,
    )


def exceptional_set(support, row: int) -> frozenset[int]:
    return frozenset(
        column for current_row, column in support if current_row == row
    )


def audit_padded_overlap_cases() -> None:
    # orbit, transpose first, row pair, selected pairs, common site
    cases = (
        (0, False, 1, 2, {0, 1}, {0, 2}, 0),
        (2, False, 2, 3, {0, 3}, {1, 3}, 3),
        (3, True, 1, 2, {0, 1}, {0, 2}, 0),
        (4, False, 2, 3, {0, 2}, {1, 2}, 2),
        (5, False, 1, 2, {0, 1}, {0, 3}, 0),
        (6, False, 2, 3, {2, 3}, {0, 2}, 2),
        (8, False, 1, 2, {0, 3}, {1, 3}, 3),
    )
    for orbit, use_transpose, first, second, first_pair, second_pair, common in cases:
        support = REPRESENTATIVES[orbit]
        if use_transpose:
            support = transpose(support)
        first_pair = frozenset(first_pair)
        second_pair = frozenset(second_pair)
        assert exceptional_set(support, first) <= first_pair
        assert exceptional_set(support, second) <= second_pair
        assert first_pair & second_pair == {common}
        # Exact singular support makes every unselected component invertible.
        assert all(
            (first, site) not in support
            for site in frozenset(SITES) - first_pair
        )
        assert all(
            (second, site) not in support
            for site in frozenset(SITES) - second_pair
        )


def audit_disjoint_branches_and_certificate() -> None:
    disjoint = REPRESENTATIVES[7]
    # Each local disjoint argument can fail to contradict only if every
    # block in the corresponding four-cell union is literally zero.
    forced_zero_unions = (
        frozenset(((1, 0), (1, 1), (2, 2), (2, 3))),
        frozenset(((1, 0), (1, 1), (3, 2), (3, 3))),
        frozenset(((0, 0), (1, 0), (2, 3), (3, 3))),
        frozenset(((0, 1), (1, 1), (2, 3), (3, 3))),
    )
    assert all(union <= disjoint for union in forced_zero_unions)

    survivors = set()
    positions = tuple(sorted(disjoint))
    for mask in range(1 << len(positions)):
        nonzero = frozenset(
            position
            for index, position in enumerate(positions)
            if mask & (1 << index)
        )
        if all(not (nonzero & union) for union in forced_zero_unions):
            survivors.add(nonzero)
    assert survivors == {frozenset(), frozenset(((0, 2),))}

    alpha, beta = sp.symbols("alpha beta", nonzero=True)
    u, w, v_1, v_2 = sp.symbols("u w v_1 v_2")
    f_11 = alpha + u * v_1
    f_12 = u * v_2
    g_22 = beta + w * v_2
    certificate = sp.expand(
        beta * f_11 - v_1 * (u * g_22 - w * f_12)
    )
    assert certificate == alpha * beta


def internal_color(left: int, right: int) -> int:
    return (1, 2, 3).index(left ^ right)


def audit_k33_residual() -> None:
    k33 = REPRESENTATIVES[1]
    assert degrees(k33, 0) == (3, 3, 3, 0)
    assert degrees(k33, 1) == (3, 3, 3, 0)
    for oriented in (k33, transpose(k33)):
        assert tuple(
            row
            for row in SITES
            if len(exceptional_set(oriented, row)) <= 2
        ) == (3,)

    identity = sp.eye(3)
    rank_one = sp.diag(1, 0, 0)
    first = (rank_one, rank_one, rank_one, identity)
    second = (rank_one, rank_one, rank_one, identity)
    domain = tuple(
        (edge, left_color, right_color)
        for edge in EDGES
        for left_color in COLORS
        for right_color in COLORS
    )
    rows = []
    for x, y in itertools.product(COLORS, repeat=2):
        if (x, y) == (0, 0):
            continue
        for output in WORDS:
            row = []
            for (u, v), left_color, right_color in domain:
                if (
                    output[u] != left_color
                    or output[v] != right_color
                ):
                    row.append(0)
                    continue
                i, j = tuple(
                    site for site in SITES if site not in (u, v)
                )
                row.append(
                    first[i][output[i], x] * second[j][output[j], y]
                    + second[i][output[i], y] * first[j][output[j], x]
                )
            rows.append(row)
    matrix = sp.Matrix(rows)
    incident_columns = tuple(
        column
        for column, (edge, _left_color, _right_color) in enumerate(domain)
        if 3 in edge
    )
    assert len(incident_columns) == 27
    assert matrix[:, incident_columns] == sp.zeros(matrix.rows, 27)
    assert DomainMatrix.from_Matrix(matrix).rank() == 19


def main() -> None:
    audit_census()
    audit_padded_overlap_cases()
    audit_disjoint_branches_and_certificate()
    audit_k33_residual()
    print("independent exact-nine census: 2752 = nine disjoint full orbits")
    print("seven padded overlap-one applications: legal")
    print("disjoint literal-zero reduction: {empty, B_02}")
    print("weighted residual certificate: alpha*beta")
    print("K3,3 local residual: rank 19 with 27 invisible columns")
    print("independent exact-nine audit: PASS")


if __name__ == "__main__":
    main()
