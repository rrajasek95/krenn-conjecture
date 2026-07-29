#!/usr/bin/env python3
"""Exact audits for aligned-two-plane-boundary-closure.md."""

from __future__ import annotations

from itertools import combinations, permutations, product

import sympy as sp


def odot(x: sp.Matrix, y: sp.Matrix) -> sp.Matrix:
    return x * y.T + y * x.T


def lifted_products(P: tuple[sp.Matrix, ...], S: tuple[sp.Matrix, ...]):
    return tuple(odot(P[c], S[d]) for c in range(3) for d in range(3) if c != d)


def flat(matrix: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(matrix.rows * matrix.cols, 1, tuple(matrix))


def qsquare(linear_form: sp.Matrix) -> sp.Matrix:
    return linear_form * linear_form.T


def qproduct(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return (left * right.T + right * left.T) / 2


def pairing(form: sp.Matrix, tensor: sp.Matrix):
    return sp.expand(sum(form[i, j] * tensor[i, j] for i in range(4) for j in range(4)))


def audit_normal_forms() -> None:
    e = tuple(sp.eye(4).col(i) for i in range(4))

    charts = []

    # The regular support-two chart s_c=p_c+v_c t, v=(0,1,1).
    P = e[:3]
    S = (e[0], e[1] + e[3], e[2] + e[3])
    N = sp.Matrix([[0, -1, 1], [1, 0, 0], [-1, 0, 0]])
    ell = (
        e[0],
        e[1],
        e[2],
        e[1] + e[2] - e[3],
        e[3],
    )
    charts.append((P, S, N, tuple(qsquare(x) for x in ell)))

    # Same missing row and column.
    P = e[:3]
    S = (e[3], e[1], e[2])
    N = sp.zeros(3)
    N[1, 2], N[2, 1] = 1, -1
    forms = tuple(qsquare(x) for x in e) + (qproduct(e[0], e[3]),)
    charts.append((P, S, N, forms))

    # Different missing row and column, for both diagonal orbits.
    for a in (0, 1):
        P = e[:3]
        S = (e[1], e[3], -a * e[1] - e[2])
        N = sp.zeros(3)
        N[1, 0], N[1, 2], N[2, 0] = a, 1, 1
        forms = (
            qsquare(e[0]),
            qsquare(e[2]),
            qsquare(e[3]),
            qproduct(e[1], e[3]),
            qproduct(e[0], e[1] - a * e[2]),
        )
        charts.append((P, S, N, forms))

    for P, S, N, forms in charts:
        intrinsic = sum(
            (N[c, d] * odot(P[c], S[d]) for c in range(3) for d in range(3)),
            sp.zeros(4),
        )
        assert intrinsic == sp.zeros(4)
        assert N.rank() == 2
        assert all(N[i, i] == 0 for i in range(3))

        Z = lifted_products(P, S)
        assert sp.Matrix.hstack(*(flat(tensor) for tensor in Z)).rank() == 5
        assert sp.Matrix.hstack(*(flat(form) for form in forms)).rank() == 5
        assert all(pairing(form, tensor) == 0 for form in forms for tensor in Z)


def audit_cube_section_lemma() -> None:
    vertices = tuple(product((-1, 1), repeat=4))
    feasible = set()
    for chosen in combinations(vertices, 4):
        sign_matrix = sp.Matrix(chosen)
        affine_matrix = sp.Matrix([[1, *vertex] for vertex in chosen])
        kernel = sign_matrix.nullspace()
        if (
            affine_matrix.rank() == 4
            and len(kernel) == 1
            and all(entry != 0 for entry in kernel[0])
        ):
            tetrahedron = tuple(sorted(chosen))
            feasible.add(tetrahedron)
            assert any(
                tuple(-entry for entry in vertex) in tetrahedron
                for vertex in tetrahedron
            )
    assert len(feasible) == 96

    group = tuple(
        (permutation, signs)
        for permutation in permutations(range(4))
        for signs in product((-1, 1), repeat=4)
    )

    def act(tetrahedron, element):
        permutation, signs = element
        return tuple(
            sorted(
                tuple(signs[j] * vertex[permutation[j]] for j in range(4))
                for vertex in tetrahedron
            )
        )

    representative = min(feasible)
    orbit = {act(representative, element) for element in group}
    assert orbit & feasible == feasible
    expected = (
        (-1, -1, -1, -1),
        (-1, -1, 1, 1),
        (-1, 1, -1, 1),
        (1, -1, 1, -1),
    )
    assert expected in feasible


def canonical_projective(vector: sp.Matrix) -> tuple[sp.Expr, ...]:
    entries = tuple(sp.factor(entry) for entry in vector)
    pivot = next(entry for entry in entries if entry != 0)
    return tuple(sp.factor(entry / pivot) for entry in entries)


def audit_support_two_fat_plane() -> None:
    circuit = sp.Matrix([0, 1, 1, -1, -1])
    ell_map = sp.Matrix(
        [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 1, 1, -1],
            [0, 0, 0, 1],
        ]
    )
    named_actual = {
        "p0": sp.Matrix([1, 0, 0, 0]),
        "p1": sp.Matrix([0, 1, 0, 0]),
        "p2": sp.Matrix([0, 0, 1, 0]),
        "s1": sp.Matrix([0, 1, 0, 1]),
        "s2": sp.Matrix([0, 0, 1, 1]),
    }
    named = {name: ell_map * vector for name, vector in named_actual.items()}
    independent_rows = (0, 1, 2, 4)

    def h_coordinates(vector: sp.Matrix) -> sp.Matrix:
        return vector.extract(independent_rows, (0,))

    total_basis_pairs = 0
    for pair in combinations(range(1, 5), 2):
        class_a = (0, *pair)
        class_b = tuple(index for index in range(1, 5) if index not in pair)
        y_a, y_b = sp.zeros(5, 1), sp.zeros(5, 1)
        y_a[0] = 1
        i, j = pair
        y_a[i] = 1
        y_a[j] = -circuit[i] / circuit[j]
        k, ell = class_b
        y_b[k] = 1
        y_b[ell] = -circuit[k] / circuit[ell]
        assert (circuit.T * y_a)[0] == 0
        assert (circuit.T * y_b)[0] == 0

        plane = sp.Matrix.hstack(h_coordinates(y_a), h_coordinates(y_b))
        quotient = sp.Matrix.hstack(*plane.T.nullspace()).T
        assert quotient.shape == (2, 4)

        possible: set[tuple[sp.Expr, ...]] = set()
        for signs in product((-1, 1), repeat=5):
            twist_a = sp.Matrix([signs[q] * y_a[q] for q in range(5)])
            twist_b = sp.Matrix([signs[q] * y_b[q] for q in range(5)])
            sum_a = (circuit.T * twist_a)[0]
            sum_b = (circuit.T * twist_b)[0]
            if sum_a == 0 and sum_b == 0:
                candidates = (twist_a, twist_b)
                quotient_span = sp.Matrix.hstack(
                    quotient * h_coordinates(twist_a),
                    quotient * h_coordinates(twist_b),
                )
                # A continuous sign-twist component has only one quotient
                # direction, so its two generators suffice.
                assert quotient_span.rank() <= 1
            elif sum_a == 0:
                candidates = (twist_a,)
            elif sum_b == 0:
                candidates = (twist_b,)
            else:
                candidates = (sum_b * twist_a - sum_a * twist_b,)

            for candidate in candidates:
                direction = quotient * h_coordinates(candidate)
                if direction != sp.zeros(2, 1):
                    possible.add(canonical_projective(direction))

        assert len(possible) == 3
        named_directions = {
            name: (
                None
                if (direction := quotient * h_coordinates(vector)) == sp.zeros(2, 1)
                else canonical_projective(direction)
            )
            for name, vector in named.items()
        }
        for first, second in combinations(sorted(possible, key=str), 2):
            first_vector, second_vector = sp.Matrix(first), sp.Matrix(second)
            assert sp.Matrix.hstack(first_vector, second_vector).det() != 0
            forced = []
            for name, direction in named_directions.items():
                if direction is None:
                    forced.append(name)
                    continue
                vector = sp.Matrix(direction)
                if (
                    sp.Matrix.hstack(first_vector, vector).det() == 0
                    or sp.Matrix.hstack(second_vector, vector).det() == 0
                ):
                    forced.append(name)
            assert forced
            total_basis_pairs += 1
    assert total_basis_pairs == 18


def audit_different_missing_exception() -> None:
    m, r, s = sp.symbols("m r s", nonzero=True)
    restricted = sp.Matrix([r, s, m * r + s, 0])
    values = sp.Matrix(
        [
            restricted[0] ** 2,
            restricted[2] ** 2,
            restricted[3] ** 2,
            restricted[1] * restricted[3],
            restricted[0] * (restricted[1] - restricted[2]),
        ]
    )
    coefficient_matrix = sp.Matrix(
        [
            [sp.expand(value).coeff(r, 2),
             sp.expand(value).coeff(r, 1).coeff(s, 1),
             sp.expand(value).coeff(s, 2)]
            for value in values
        ]
    )
    assert coefficient_matrix.rank() == 2
    image = sp.Matrix.hstack(
        sp.Matrix([1, m**2, 0, 0, -m]),
        sp.Matrix([0, 1, 0, 0, 0]),
    )
    assert sp.Matrix.hstack(image, coefficient_matrix).rank() == 2

    x0, x1, x2, x3 = sp.symbols("x0 x1 x2 x3")
    outside_value = sp.Matrix(
        [x0**2, x2**2, x3**2, x1 * x3, x0 * (x1 - x2)]
    )
    # Membership in the two-space forces its third coordinate x3^2 to
    # vanish; over C this is exactly x3=0.
    assert image.row(2) == sp.zeros(1, 2)
    assert outside_value[2] == x3**2


def main() -> None:
    audit_normal_forms()
    audit_cube_section_lemma()
    audit_support_two_fat_plane()
    audit_different_missing_exception()
    print("Aligned two-plane boundary closure: PASS")


if __name__ == "__main__":
    main()
