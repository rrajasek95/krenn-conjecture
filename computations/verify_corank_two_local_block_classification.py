#!/usr/bin/env python3
"""Exact coordinate audits for corank-two-local-block-classification.md."""

from __future__ import annotations

import sympy as sp


ORDERED = tuple((c, d) for c in range(3) for d in range(3) if c != d)


def unit(i: int, j: int) -> sp.Matrix:
    matrix = sp.zeros(3)
    matrix[i, j] = 1
    return matrix


def block_map(A: sp.Matrix, B: sp.Matrix) -> sp.Matrix:
    columns = []
    for c, d in ORDERED:
        M = unit(c, d)
        columns.append((M * B.T + A * M.T).reshape(9, 1))
    return sp.Matrix.hstack(*columns)


def vector(matrix: sp.Matrix) -> sp.Matrix:
    return matrix.reshape(9, 1)


def audit_generator_formula_and_diagonal_form() -> None:
    a = sp.symbols("a0:9")
    b = sp.symbols("b0:9")
    A = sp.Matrix(3, 3, a)
    B = sp.Matrix(3, 3, b)
    for c, d in ORDERED:
        expected = sp.eye(3)[:, c] * B[:, d].T + A[:, d] * sp.eye(3)[:, c].T
        actual = unit(c, d) * B.T + A * unit(c, d).T
        assert actual == expected

    d0, d1, d2 = sp.symbols("d0 d1 d2", nonzero=True)
    D = sp.diag(d0, d1, d2)
    T = block_map(D, D)
    assert T.rank() == 3
    for column in T.columnspace():
        matrix = column.reshape(3, 3)
        assert matrix == matrix.T
        assert all(matrix[i, i] == 0 for i in range(3))


def audit_repeated_row_line_rank_two_case() -> None:
    x, y, t01, t10, u, v, alpha, beta = sp.symbols(
        "x y t01 t10 u v alpha beta"
    )
    N = sp.Matrix([[0, x, 0], [y, 0, 0], [0, 0, 0]])
    A = sp.Matrix(
        [[t10 * x, -u, 0], [-v, t01 * y, 0], [0, 0, 0]]
    )
    B = sp.Matrix(
        [[t10 * y, u, 0], [v, t01 * x, 0], [0, 0, 0]]
    )

    outputs = {}
    for c, d in ORDERED:
        outputs[c, d] = unit(c, d) * B.T + A * unit(c, d).T

    assert outputs[0, 1] == t01 * N
    assert outputs[1, 0] == t10 * N
    assert outputs[0, 2] == sp.zeros(3)
    assert outputs[1, 2] == sp.zeros(3)

    expected20 = sp.Matrix(
        [[0, 0, t10 * x], [0, 0, -v], [t10 * y, v, 0]]
    )
    expected21 = sp.Matrix(
        [[0, 0, -u], [0, 0, t01 * y], [u, t01 * x, 0]]
    )
    assert outputs[2, 0] == expected20
    assert outputs[2, 1] == expected21
    assert sp.factor((alpha * N + beta * expected20).det()) == 0
    assert sp.factor((alpha * N + beta * expected21).det()) == 0


def audit_repeated_alternating_row_line_case() -> None:
    """Check the extra family present when the repeated line is alternating."""
    t01, t02, t10, t12, u, v = sp.symbols("t01 t02 t10 t12 u v")
    N = unit(0, 1) - unit(1, 0)
    A = sp.Matrix(
        [[t10, -u, t12], [-v, -t01, -t02], [0, 0, 0]]
    )
    B = sp.Matrix(
        [[-t10, u, -t12], [v, t01, t02], [0, 0, 0]]
    )
    assert B == -A

    outputs = {}
    for c, d in ORDERED:
        outputs[c, d] = unit(c, d) * B.T + A * unit(c, d).T
        assert outputs[c, d].T == -outputs[c, d]
        assert sp.factor(outputs[c, d].det()) == 0

    assert outputs[0, 1] == t01 * N
    assert outputs[0, 2] == t02 * N
    assert outputs[1, 0] == t10 * N
    assert outputs[1, 2] == t12 * N


def audit_skew_opposite_edge_determinant() -> None:
    z, x, y, aa, bb = sp.symbols("z x y aa bb")
    matrix = sp.Matrix(
        [[0, z, x * bb], [-z, 0, y * bb], [x * aa, y * aa, 0]]
    )
    assert sp.factor(matrix.det()) == 0


def audit_diagonal_pair_equations() -> None:
    ac, ad, bc, bd = sp.symbols("ac ad bc bd")
    first = sp.Matrix([bd, ad])
    second = sp.Matrix([ac, bc])
    assert sp.factor(sp.Matrix.hstack(first, second).det()) == bc * bd - ac * ad

    r0, r1, r2 = sp.symbols("r0 r1 r2", nonzero=True)
    # The three equations r_c r_d=1 imply equality and a common square one.
    groebner = sp.groebner(
        [r0 * r1 - 1, r0 * r2 - 1, r1 * r2 - 1], r0, r1, r2
    )
    for consequence in (r0 - r1, r1 - r2, r0**2 - 1):
        assert groebner.reduce(consequence)[1] == 0


def audit_rank_one_dead_form() -> None:
    u0, u1 = sp.symbols("u0 u1")
    v = sp.Matrix([u0, u1, 0])
    A = v * sp.eye(3)[:, 2].T
    B = -A
    T = block_map(A, B)
    alternating = vector(unit(0, 1) - unit(1, 0))
    for column in range(T.cols):
        candidate = T[:, column]
        assert sp.Matrix.hstack(alternating, candidate).rank() <= 1
    assert T.rank() == 1


def audit_sharp_four_plane() -> None:
    # An exact model of the live normal form.  The preimage of a generic
    # invertible line has dimension four and avoids all row/column planes.
    D = sp.diag(2, 3, 5)
    T = block_map(D, D)
    H = sp.Matrix([[0, 7, 11], [7, 0, 13], [11, 13, 0]])
    assert H.det() != 0

    kernel = T.nullspace()
    assert len(kernel) == 3
    # T(E_cd)=d_d(E_cd+E_dc), so this is one exact preimage of H.
    m0 = sp.zeros(6, 1)
    coordinates = {pair: index for index, pair in enumerate(ORDERED)}
    m0[coordinates[0, 1]] = sp.Rational(7, 3)
    m0[coordinates[0, 2]] = sp.Rational(11, 5)
    m0[coordinates[1, 2]] = sp.Rational(13, 5)
    assert T * m0 == vector(H)

    relation_basis = sp.Matrix.hstack(*kernel, m0)
    assert relation_basis.rank() == 4
    for fixed_first in (True, False):
        for colour in range(3):
            indices = [
                index
                for index, (c, d) in enumerate(ORDERED)
                if (c if fixed_first else d) == colour
            ]
            coordinate_plane = sp.zeros(6, 2)
            coordinate_plane[indices[0], 0] = 1
            coordinate_plane[indices[1], 1] = 1
            # A zero intersection is equivalent to the concatenated six
            # vectors spanning all of C^6.
            assert sp.Matrix.hstack(relation_basis, coordinate_plane).rank() == 6


def main() -> None:
    audit_generator_formula_and_diagonal_form()
    audit_repeated_row_line_rank_two_case()
    audit_repeated_alternating_row_line_case()
    audit_skew_opposite_edge_determinant()
    audit_diagonal_pair_equations()
    audit_rank_one_dead_form()
    audit_sharp_four_plane()
    print("Corank-two local block classification: PASS")


if __name__ == "__main__":
    main()
