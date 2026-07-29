#!/usr/bin/env python3
"""Exact audit of the two four-edge stabilizers in the f=0 residual chart.

This checks only finite support/mask claims.  The tensor contradictions are
proved in proofs/four-edge-partition-rigidity.md.
"""

from __future__ import annotations

import itertools

import sympy as sp


VERTICES = tuple(range(6))
COLORS = tuple(range(3))
EDGES = tuple(itertools.combinations(VERTICES, 2))
FULL_EDGES = {(0, 3), (0, 5), (1, 4), (1, 5), (2, 3), (2, 4)}
BASIS_LABELS = {
    (0, 1): (2, 1),
    (0, 2): (0, 0),
    (0, 4): (0, 2),
    (1, 2): (1, 1),
    (1, 3): (1, 0),
    (2, 5): (0, 2),
    (3, 4): (2, 0),
    (3, 5): (2, 2),
    (4, 5): (1, 1),
}
SUPPORTS = {
    edge: (
        set(itertools.product(COLORS, repeat=2))
        if edge in FULL_EDGES
        else {BASIS_LABELS[edge]}
    )
    for edge in EDGES
}


def mask(alpha, edge):
    u, v = edge
    return sp.Matrix(
        3, 3, lambda row, column: alpha[u][row] + alpha[v][column]
    )


def supported_cells(edge):
    return tuple(SUPPORTS[edge])


def assert_stabilizer(alpha, survivors):
    assert all(
        sum(alpha[vertex][color] for vertex in VERTICES) == 1
        for color in COLORS
    )
    for edge in EDGES:
        matrix = mask(alpha, edge)
        if edge not in survivors:
            assert all(matrix[row, column] == 0 for row, column in supported_cells(edge))
        else:
            assert any(matrix[row, column] != 0 for row, column in supported_cells(edge))


def contains_axis(column_matrix, color):
    axis = sp.eye(3)[:, color]
    return column_matrix.row_join(axis).rank() == column_matrix.rank()


def audit_path_witness():
    alpha = (
        (0, 1, 0),
        (-1, 0, 1),
        (0, 0, 0),
        (0, 0, 0),
        (0, 0, 0),
        (2, 0, 0),
    )
    survivors = {(0, 3), (0, 5), (1, 4), (1, 5)}
    assert_stabilizer(alpha, survivors)
    matrices = {edge: mask(alpha, edge) for edge in survivors}
    assert [matrices[edge].rank() for edge in sorted(survivors)] == [1, 2, 1, 2]

    at_0_03 = matrices[(0, 3)]
    at_0_05 = matrices[(0, 5)]
    at_1_14 = matrices[(1, 4)]
    at_1_15 = matrices[(1, 5)]
    assert [contains_axis(at_0_03, color) for color in COLORS] == [False, True, False]
    assert [contains_axis(at_0_05, color) for color in COLORS] == [False, True, False]
    assert [contains_axis(at_1_14, color) for color in COLORS] == [False, False, False]
    assert [contains_axis(at_1_15, color) for color in COLORS] == [False, False, False]
    print("path witness: killed 11 edges; ranks 1,2,1,2; local axis audit passed")


def audit_two_path_witness():
    alpha = (
        (0, 0, 0),
        (1, 0, 1),
        (0, 0, 0),
        (0, 1, 0),
        (0, 0, 0),
        (0, 0, 0),
    )
    survivors = {(0, 3), (1, 4), (1, 5), (2, 3)}
    assert_stabilizer(alpha, survivors)
    matrices = {edge: mask(alpha, edge) for edge in survivors}
    assert all(matrix.rank() == 1 for matrix in matrices.values())

    # Row spaces are the factor spaces at the second endpoint.  Both edges
    # ending at vertex 3 select exactly its color-one coordinate line.
    e_1_row = sp.Matrix([[0, 1, 0]])
    for edge in ((0, 3), (2, 3)):
        matrix = matrices[edge]
        assert matrix.col_join(e_1_row).rank() == matrix.rank()

    # On 14 and 15 the second-endpoint mask factor is (1,1,1), hence after
    # Hadamard multiplication it is the original full-support factor.
    full_row = sp.Matrix([[1, 1, 1]])
    for edge in ((1, 4), (1, 5)):
        matrix = matrices[edge]
        assert matrix.col_join(full_row).rank() == matrix.rank()
    print("two-path witness: killed 11 edges; four rank-one masks; repeated-line audit passed")


def audit_additional_witnesses():
    cases = (
        (
            "paw-015+03",
            (
                (0, 1, 1),
                (0, 0, 0),
                (0, 0, 0),
                (0, 0, 0),
                (0, 0, 0),
                (1, 0, 0),
            ),
            {(0, 1), (0, 3), (0, 5), (1, 5)},
            [1, 1, 2, 1],
        ),
        (
            "three-star+leaf",
            (
                (0, 0, 0),
                (0, 0, 0),
                (0, 0, 1),
                (1, 1, 0),
                (0, 0, 0),
                (0, 0, 0),
            ),
            {(0, 3), (1, 3), (2, 3), (2, 4)},
            [1, 1, 2, 1],
        ),
        (
            "paw-145+05",
            (
                (0, 0, 0),
                (-1, 0, 1),
                (0, 0, 0),
                (0, 0, 0),
                (0, 0, 0),
                (2, 1, 0),
            ),
            {(0, 5), (1, 4), (1, 5), (4, 5)},
            [1, 1, 2, 1],
        ),
        (
            "paw-145+24",
            (
                (0, 0, 0),
                (1, 0, 1),
                (0, 0, 0),
                (0, 0, 0),
                (0, 1, 0),
                (0, 0, 0),
            ),
            {(1, 4), (1, 5), (2, 4), (4, 5)},
            [2, 1, 1, 1],
        ),
    )
    for name, alpha, survivors, expected_ranks in cases:
        assert_stabilizer(alpha, survivors)
        ranks = [mask(alpha, edge).rank() for edge in sorted(survivors)]
        assert ranks == expected_ranks, (name, ranks)
    print("four additional witnesses: exact killing and rank audits passed")


def equation_row(edge, row, column):
    u, v = edge
    result = [0] * 18
    result[3 * u + row] = 1
    result[3 * v + column] = 1
    return result


def affine_consistent(killed):
    rows = []
    rhs = []
    for edge in killed:
        for row, column in supported_cells(edge):
            rows.append(equation_row(edge, row, column))
            rhs.append(0)
    for color in COLORS:
        rows.append(
            [int(index % 3 == color) for index in range(18)]
        )
        rhs.append(1)
    matrix = sp.polys.matrices.DomainMatrix.from_list_sympy(
        len(rows), 18, rows
    ).to_field()
    augmented = sp.polys.matrices.DomainMatrix.from_list_sympy(
        len(rows), 19, [row + [value] for row, value in zip(rows, rhs)]
    ).to_field()
    return matrix.rank() == augmented.rank()


def audit_exhaustive_survivor_sets():
    expected = {
        frozenset({(0, 1), (0, 3), (0, 5), (1, 5)}),
        frozenset({(0, 3), (0, 5), (1, 4), (1, 5)}),
        frozenset({(0, 3), (1, 3), (2, 3), (2, 4)}),
        frozenset({(0, 3), (1, 4), (1, 5), (2, 3)}),
        frozenset({(0, 5), (1, 4), (1, 5), (4, 5)}),
        frozenset({(1, 4), (1, 5), (2, 4), (4, 5)}),
    }
    feasible = set()
    for survivor_count in range(5):
        for survivors_tuple in itertools.combinations(EDGES, survivor_count):
            survivors = frozenset(survivors_tuple)
            killed = tuple(edge for edge in EDGES if edge not in survivors)
            if affine_consistent(killed):
                feasible.add(survivors)
    assert feasible == expected
    print("survivor enumeration: no <=3-edge set; exactly six 4-edge sets")


def main():
    assert set(EDGES) == FULL_EDGES | set(BASIS_LABELS)
    audit_path_witness()
    audit_two_path_witness()
    audit_additional_witnesses()
    audit_exhaustive_survivor_sets()


if __name__ == "__main__":
    main()
