#!/usr/bin/env python3
"""Exact audits for notes/singular-relation-block-reduction.md."""

from __future__ import annotations

import itertools

import sympy as sp


ORDERED = tuple((c, d) for c in range(3) for d in range(3) if c != d)


def unit(i: int, j: int) -> sp.Matrix:
    matrix = sp.zeros(3)
    matrix[i, j] = 1
    return matrix


def off_diagonal(matrix: sp.Matrix) -> sp.Matrix:
    answer = matrix.copy()
    for index in range(3):
        answer[index, index] = 0
    return answer


def incidence_valid(rows: tuple[int, ...], columns: tuple[int, ...],
                    number_of_lines: int) -> bool:
    if set(rows + columns) != set(range(number_of_lines)):
        return False
    # Each of the row and column triples spans the physical three-space.
    if len(set(rows)) < 2 or len(set(columns)) < 2:
        return False
    # Two equal opposite lines, distinct from the line under inspection,
    # would give the same intersection point twice.
    for row in range(3):
        opposite = [column for column in range(3) if column != row]
        if columns[opposite[0]] == columns[opposite[1]] != rows[row]:
            return False
    for column in range(3):
        opposite = [row for row in range(3) if row != column]
        if rows[opposite[0]] == rows[opposite[1]] != columns[column]:
            return False
    return True


def incidence_orbit(rows: tuple[int, ...], columns: tuple[int, ...],
                    number_of_lines: int) -> tuple[int, ...]:
    candidates = []
    for colour_permutation in itertools.permutations(range(3)):
        permuted_rows = tuple(rows[colour_permutation[index]] for index in range(3))
        permuted_columns = tuple(
            columns[colour_permutation[index]] for index in range(3)
        )
        for line_permutation in itertools.permutations(range(number_of_lines)):
            first = tuple(line_permutation[value] for value in permuted_rows)
            second = tuple(line_permutation[value] for value in permuted_columns)
            candidates.append(first + second)
            candidates.append(second + first)
    return min(candidates)


def audit_rank_three_incidence_orbits() -> None:
    expected = {
        2: {
            (0, 0, 1, 0, 1, 0),
            (0, 0, 1, 1, 1, 0),
        },
        3: {
            (0, 0, 1, 0, 2, 0),
            (0, 0, 1, 1, 2, 0),
            (0, 1, 2, 0, 1, 2),
            (0, 1, 2, 0, 2, 1),
            (0, 1, 2, 1, 2, 0),
        },
    }
    for number_of_lines in (2, 3):
        actual = set()
        for rows in itertools.product(range(number_of_lines), repeat=3):
            for columns in itertools.product(range(number_of_lines), repeat=3):
                if incidence_valid(rows, columns, number_of_lines):
                    actual.add(incidence_orbit(rows, columns, number_of_lines))
        assert actual == expected[number_of_lines]


def graph_orbit(edges: frozenset[tuple[int, int]]) -> tuple[tuple[int, int], ...]:
    candidates = []
    for permutation in itertools.permutations(range(3)):
        candidates.append(tuple(sorted((permutation[c], permutation[d])
                                       for c, d in edges)))
        candidates.append(tuple(sorted((permutation[d], permutation[c])
                                       for c, d in edges)))
    return min(candidates)


def connected_components(edges: frozenset[tuple[int, int]]) -> int:
    vertices = tuple((side, index) for side in (0, 1) for index in range(3))
    unseen = set(vertices)
    count = 0
    while unseen:
        count += 1
        stack = [unseen.pop()]
        while stack:
            side, index = stack.pop()
            if side == 0:
                neighbours = {(1, d) for c, d in edges if c == index}
            else:
                neighbours = {(0, c) for c, d in edges if d == index}
            fresh = neighbours & unseen
            unseen -= fresh
            stack.extend(fresh)
    return count


def audit_rank_two_nonzero_graphs() -> None:
    candidates = set()
    for mask in itertools.product((False, True), repeat=6):
        edges = frozenset(edge for edge, keep in zip(ORDERED, mask) if keep)
        if any(not any(c == row for c, _ in edges) for row in range(3)):
            continue
        if any(not any(d == column for _, d in edges) for column in range(3)):
            continue
        if connected_components(edges) == 1:
            continue
        candidates.add(graph_orbit(edges))
    assert candidates == {
        ((0, 1), (1, 2), (2, 0)),
        ((0, 1), (0, 2), (1, 0), (2, 0)),
        ((0, 1), (0, 2), (1, 0), (2, 1)),
    }


def audit_toric_factor_matching() -> None:
    positive = ((0, 1), (1, 2), (2, 0))
    negative = ((0, 2), (2, 1), (1, 0))
    allowed = []
    for permutation in itertools.permutations(range(3)):
        matching = tuple(zip(positive, (negative[index] for index in permutation)))
        if all(c != e and d != f for (c, d), (e, f) in matching):
            allowed.append(matching)
    assert allowed == [
        (
            ((0, 1), (1, 0)),
            ((1, 2), (2, 1)),
            ((2, 0), (0, 2)),
        )
    ]

    # Incidence type 3c gives the reverse *projective* proportionalities:
    # an off-diagonal cell is the vertex of the two corresponding lines.
    # This deliberately does not assert the product of generator scalars.
    rows = (0, 1, 2)
    columns = (0, 1, 2)
    vertex = lambda first, second: tuple(
        int(index not in (first, second)) for index in range(3)
    )
    values = {(c, d): vertex(rows[c], columns[d]) for c, d in ORDERED}
    assert all(values[c, d] == values[d, c] for c, d in ORDERED)


def audit_type_3c_twisted_kernel() -> None:
    x, y, z, A, B, C = sp.symbols("x y z A B C", nonzero=True)
    matrix = sp.Matrix([[0, x, y], [A * x, 0, z], [B * y, C * z, 0]])
    assert sp.factor(matrix.det()) == x * y * z * (A * C + B)
    assert matrix.adjugate() == sp.Matrix(
        [
            [-C * z**2, C * y * z, x * z],
            [B * y * z, -B * y**2, A * x * y],
            [A * C * x * z, B * x * y, -A * x**2],
        ]
    )

    # The support proof in Proposition 5.2: no two nonzero vectors u,v
    # can make u^T adj(M) v vanish identically.  Once the square
    # coefficients force disjoint supports, every nonempty disjoint
    # support pair leaves a nonzero mixed monomial coefficient.
    coordinates = range(3)
    for support_u_size in range(1, 4):
        for support_u in itertools.combinations(coordinates, support_u_size):
            remaining = tuple(index for index in coordinates if index not in support_u)
            for support_v_size in range(1, len(remaining) + 1):
                for support_v in itertools.combinations(remaining, support_v_size):
                    u = sp.Matrix([sp.Symbol(f"u{index}", nonzero=True)
                                   if index in support_u else 0
                                   for index in coordinates])
                    v = sp.Matrix([sp.Symbol(f"v{index}", nonzero=True)
                                   if index in support_v else 0
                                   for index in coordinates])
                    polynomial = sp.Poly(sp.expand((u.T * matrix.adjugate() * v)[0]),
                                         x, y, z)
                    assert not polynomial.is_zero


def audit_types_3d_3e_compression_quadratics() -> None:
    x, y, z = sp.symbols("x y z")
    A, B, C, D, E = sp.symbols("A B C D E", nonzero=True)
    type_3d = sp.Matrix(
        [[0, B * y + C * z, A * x + D * z],
         [x, 0, E * z],
         [y, z, 0]]
    )
    u_symbols = sp.symbols("u0:3", nonzero=True)
    v_symbols = sp.symbols("v0:3", nonzero=True)

    # The square-coefficient support split in the written proof is exact.
    for support_u_bits in itertools.product((False, True), repeat=3):
        if not any(support_u_bits):
            continue
        for support_v_bits in itertools.product((False, True), repeat=3):
            if not any(support_v_bits):
                continue
            u = sp.Matrix([u_symbols[index] if support_u_bits[index] else 0
                           for index in range(3)])
            v = sp.Matrix([v_symbols[index] if support_v_bits[index] else 0
                           for index in range(3)])
            polynomial = sp.Poly(sp.expand((u.T * type_3d.adjugate() * v)[0]),
                                 x, y, z)
            # If all six coefficients vanished, in particular the three
            # equations (24g) would.  Exhaustively split their zero-product
            # alternatives; no support pattern survives all coefficients.
            square_x = sp.factor(polynomial.coeff_monomial(x**2))
            square_y = sp.factor(polynomial.coeff_monomial(y**2))
            mixed_xy = sp.factor(polynomial.coeff_monomial(x * y))
            structurally_possible = not (
                (support_u_bits[1] and support_v_bits[2])
                or (support_u_bits[2] and support_v_bits[1])
            )
            if structurally_possible and not (
                (support_u_bits[1] and support_v_bits[1])
                or (support_u_bits[2] and support_v_bits[2])
            ):
                assert not polynomial.is_zero
            else:
                assert square_x != 0 or square_y != 0 or mixed_xy != 0

    a, b, c, d, e, f = sp.symbols("a b c d e f", nonzero=True)
    type_3e = sp.Matrix(
        [[0, -a * x - f * z, x],
         [y, 0, -b * x - d * y],
         [-c * y - e * z, z, 0]]
    )
    surviving_support_pairs = 0
    for support_u_bits in itertools.product((False, True), repeat=3):
        if not any(support_u_bits):
            continue
        for support_v_bits in itertools.product((False, True), repeat=3):
            if not any(support_v_bits):
                continue
            # These are precisely the square-coefficient conditions (24i).
            if ((support_u_bits[0] and support_v_bits[2])
                    or (support_u_bits[1] and support_v_bits[0])
                    or (support_u_bits[2] and support_v_bits[1])):
                continue
            surviving_support_pairs += 1
            u = sp.Matrix([u_symbols[index] if support_u_bits[index] else 0
                           for index in range(3)])
            v = sp.Matrix([v_symbols[index] if support_v_bits[index] else 0
                           for index in range(3)])
            polynomial = sp.Poly(sp.expand((u.T * type_3e.adjugate() * v)[0]),
                                 x, y, z)
            assert not polynomial.is_zero
    assert surviving_support_pairs == 12


def audit_types_2a_3a_compression_quadratics() -> None:
    x, y, z = sp.symbols("x y z")
    A, B, C, D, E, F = sp.symbols("A B C D E F")
    matrix = sp.Matrix(
        [[0, A * x + C * y + E * z, B * x + D * y + F * z],
         [x, 0, y],
         [z, 0, 0]]
    )
    assert matrix.adjugate() == sp.Matrix(
        [[0, 0, A * x * y + C * y**2 + E * y * z],
         [y * z, -B * x * z - D * y * z - F * z**2,
          B * x**2 + D * x * y + F * x * z],
         [0, A * x * z + C * y * z + E * z**2,
          -A * x**2 - C * x * y - E * x * z]]
    )

    u0, u1, u2, v0, v1, v2 = sp.symbols("u0 u1 u2 v0 v1 v2")
    u = sp.Matrix([u0, u1, u2])
    v = sp.Matrix([v0, v1, v2])
    polynomial = sp.Poly(sp.expand((u.T * matrix.adjugate() * v)[0]),
                         x, y, z)
    expected_coefficients = {
        x**2: v2 * (-A * u2 + B * u1),
        x * y: v2 * (A * u0 - C * u2 + D * u1),
        x * z: A * u2 * v1 - B * u1 * v1
               - E * u2 * v2 + F * u1 * v2,
        y**2: C * u0 * v2,
        y * z: C * u2 * v1 - D * u1 * v1
               + E * u0 * v2 + u1 * v0,
        z**2: v1 * (E * u2 - F * u1),
    }
    for monomial, coefficient in expected_coefficients.items():
        assert sp.expand(polynomial.coeff_monomial(monomial) - coefficient) == 0

    # The two solution planes in (24l) really annihilate the quadratic.
    family_one = polynomial.as_expr().subs({v0: 1, v1: 0, v2: 0, u1: 0})
    family_two = polynomial.as_expr().subs({u0: 1, u1: 0, u2: 0, v2: 0})
    assert sp.expand(family_one) == 0
    assert sp.expand(family_two) == 0

    # The determinants used in the two nontrivial branches of the proof.
    assert sp.det(sp.Matrix([[B, -A], [D, -C]])) == A * D - B * C
    assert sp.det(sp.Matrix([[-B, A], [-F, E]])) == A * F - B * E


def audit_types_2b_3b_compression_rulings() -> None:
    x, y, z = sp.symbols("x y z")
    A, B, C, D, E, F, G = sp.symbols("A B C D E F G", nonzero=True)
    u0, u1, u2, v0, v1, v2 = sp.symbols("u0 u1 u2 v0 v1 v2")
    u = sp.Matrix([u0, u1, u2])
    v = sp.Matrix([v0, v1, v2])

    type_2b = sp.Matrix(
        [[0, A * x + C * y + E * z, D * y],
         [x, 0, y],
         [F * z, z, 0]]
    )
    polynomial_2b = sp.Poly(
        sp.expand((u.T * type_2b.adjugate() * v)[0]), x, y, z
    )
    assert sp.factor(polynomial_2b.coeff_monomial(x**2)) == -A * u2 * v2
    assert sp.factor(polynomial_2b.coeff_monomial(y**2)) == C * u0 * v2
    assert sp.factor(polynomial_2b.coeff_monomial(z**2)) == E * F * u2 * v1
    reduced_2b = polynomial_2b.as_expr().subs({u2: 0, v2: 0})
    assert sp.expand(
        reduced_2b - y * z * (u0 - F * u1) * (D * v1 - v0)
    ) == 0

    r, s = sp.symbols("r s")
    family_one = polynomial_2b.as_expr().subs(
        {u0: F, u1: 1, u2: 0, v0: r, v1: s, v2: 0}
    )
    family_two = polynomial_2b.as_expr().subs(
        {u0: r, u1: s, u2: 0, v0: D, v1: 1, v2: 0}
    )
    assert sp.expand(family_one) == 0
    assert sp.expand(family_two) == 0

    annihilator_v = sp.Matrix([[-s, r, 0], [0, 0, 1]])
    annihilator_k = sp.Matrix([[1, -F, 0], [0, 0, 1]])
    compression_one = sp.expand(annihilator_v * type_2b * annihilator_k.T)
    expected_compression_one = sp.Matrix(
        [[(A * F * s + r) * x + C * F * s * y + E * F * s * z,
          (r - D * s) * y],
         [0, 0]]
    )
    assert compression_one.equals(expected_compression_one)

    annihilator_l = sp.Matrix([[1, -D, 0], [0, 0, 1]])
    annihilator_u = sp.Matrix([[-s, r, 0], [0, 0, 1]])
    compression_two = sp.expand(annihilator_l * type_2b * annihilator_u.T)
    expected_compression_two = sp.Matrix(
        [[(A * r + D * s) * x + C * r * y + E * r * z, 0],
         [(r - F * s) * z, 0]]
    )
    assert compression_two.equals(expected_compression_two)

    # At the unique crossing of the two rulings the image drops to a
    # nonzero rank-one line; away from it the displayed independent
    # coefficient rows/columns give dimension two.
    assert sp.Matrix(
        [[A * F + D, C * F, E * F], [0, 0, 0]]
    ).rank() == 1
    assert sp.Matrix(
        [[A * F + D, C * F, E * F], [0, 0, 0]]
    )[0, 2] != 0

    type_3b = sp.Matrix(
        [[0, A * x + C * y + E * z, B * x + D * y + F * z],
         [x, 0, y],
         [G * z, z, 0]]
    )
    polynomial_3b = sp.Poly(
        sp.expand((u.T * type_3b.adjugate() * v)[0]), x, y, z
    )
    assert sp.factor(polynomial_3b.coeff_monomial(y**2)) == C * u0 * v2
    assert sp.factor(polynomial_3b.coeff_monomial(x**2)) == v2 * (-A * u2 + B * u1)
    assert sp.factor(polynomial_3b.coeff_monomial(x * y)) == (
        v2 * (A * u0 - C * u2 + D * u1)
    )
    family_3b = polynomial_3b.as_expr().subs(
        {u0: G, u1: 1, u2: 0, v0: r, v1: s, v2: 0}
    )
    assert sp.expand(family_3b) == 0

    annihilator_v = sp.Matrix([[-s, r, 0], [0, 0, 1]])
    annihilator_k = sp.Matrix([[1, -G, 0], [0, 0, 1]])
    compression_3b = sp.expand(annihilator_v * type_3b * annihilator_k.T)
    expected_compression_3b = sp.Matrix(
        [[(A * G * s + r) * x + C * G * s * y + E * G * s * z,
          -B * s * x + (r - D * s) * y - F * s * z],
         [0, 0]]
    )
    assert compression_3b.equals(expected_compression_3b)
    coefficient_matrix = sp.Matrix(
        [[A * G * s + r, C * G * s, E * G * s],
         [-B * s, r - D * s, -F * s]]
    )
    minor_xz = sp.factor(coefficient_matrix[:, (0, 2)].det())
    assert sp.expand(
        minor_xz - (G * s**2 * (B * E - A * F) - F * r * s)
    ) == 0
    assert sp.expand(
        coefficient_matrix[:, (0, 1)].det().subs(r, 0)
        + G * s**2 * (A * D - B * C)
    ) == 0
    assert coefficient_matrix.subs(s, 0)[:, (0, 1)] == sp.diag(r, r)

    # The quotient-map cancellation in (24aa) is identically singular.
    z00, z01, z10, z11 = sp.symbols("z00 z01 z10 z11")
    quotient_image = sp.Matrix(
        [[z11, z10, 0], [z01, 0, z10], [0, -z01, z11]]
    )
    assert sp.expand(quotient_image.det()) == 0


def audit_compression_diagonal_cases() -> None:
    # One common coordinate axis: Delta=C E_00.  The off-diagonal image
    # has the r,s,z basis used in equations (12)--(14).
    e0 = sp.eye(3)[:, 0]
    a = sp.Matrix([0, 1, 1])
    w = sp.Matrix([0, 1, 2])
    r = off_diagonal(e0 * w.T)
    s = off_diagonal(a * e0.T)
    z = off_diagonal(a * w.T)
    assert sp.Matrix.hstack(r.reshape(9, 1), s.reshape(9, 1),
                            z.reshape(9, 1)).rank() == 3
    empty_row_member = z - 3 * s
    assert empty_row_member != sp.zeros(3)
    assert empty_row_member[0, :] == sp.zeros(1, 3)

    # Two common coordinate axes: the entire off-diagonal image is
    # supported on E_01,E_10 and therefore misses row two.
    off_images = [off_diagonal(left * right.T)
                  for left in (sp.eye(3)[:, 0], sp.eye(3)[:, 1])
                  for right in (sp.eye(3)[:, 0], sp.eye(3)[:, 1])]
    assert sp.Matrix.hstack(*(value.reshape(9, 1) for value in off_images)).rank() == 2
    assert all(value[2, :] == sp.zeros(1, 3) for value in off_images)


def relation_space() -> tuple[sp.Matrix, tuple[int, ...]]:
    # D^perp is generated by 1 and a coordinate array whose two entries
    # differ in every row and every column.
    second = (3, 6, 1, 7, 2, 5)
    equations = sp.Matrix([[1] * 6, list(second)])
    basis = sp.Matrix.hstack(*equations.nullspace())
    assert basis.shape == (6, 4)
    return basis, second


def audit_representative_evaluations() -> None:
    basis, _ = relation_space()
    matrices = []
    for column in range(4):
        matrix = sp.zeros(3)
        for coefficient, (c, d) in zip(basis[:, column], ORDERED):
            matrix[c, d] = coefficient
        matrices.append(matrix)
    for w in (
        sp.Matrix([1, 0, 0]),
        sp.Matrix([0, 1, 0]),
        sp.Matrix([0, 0, 1]),
        sp.Matrix([1, 1, 0]),
        sp.Matrix([1, 2, 3]),
    ):
        evaluation = sp.Matrix.hstack(*(matrix * w for matrix in matrices))
        transpose_evaluation = sp.Matrix.hstack(
            *(matrix.T * w for matrix in matrices)
        )
        assert evaluation.rank() >= 2
        assert transpose_evaluation.rank() >= 2


def main() -> None:
    audit_rank_three_incidence_orbits()
    audit_rank_two_nonzero_graphs()
    audit_toric_factor_matching()
    audit_type_3c_twisted_kernel()
    audit_types_3d_3e_compression_quadratics()
    audit_types_2a_3a_compression_quadratics()
    audit_types_2b_3b_compression_rulings()
    audit_compression_diagonal_cases()
    audit_representative_evaluations()
    print("singular relation-block reduction: PASS")


if __name__ == "__main__":
    main()
