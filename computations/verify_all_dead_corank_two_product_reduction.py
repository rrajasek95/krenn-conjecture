#!/usr/bin/env python3
"""Exact audits for all-dead-corank-two-product-reduction.md."""

from __future__ import annotations

from itertools import combinations, permutations, product

import sympy as sp


ORDERED = tuple((c, d) for c in range(3) for d in range(3) if c != d)
SITE_PAIRS = ((0, 1), (0, 2), (1, 2))


def square_free_product(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        [left[i] * right[j] + left[j] * right[i] for i, j in SITE_PAIRS]
    )


def product_matrix(P: sp.Matrix, S: sp.Matrix, ordered=ORDERED) -> sp.Matrix:
    return sp.Matrix.hstack(
        *(square_free_product(P.row(c).T, S.row(d).T) for c, d in ordered)
    )


def coordinate_plane(indices: list[int]) -> sp.Matrix:
    answer = sp.zeros(6, len(indices))
    for column, index in enumerate(indices):
        answer[index, column] = 1
    return answer


def audit_symmetric_three_site_model() -> None:
    # The displayed vectors in the note are site-colour columns.  Rows are
    # the three global colour elements.
    V = sp.Matrix([[1, 1, 7], [2, 1, -8], [3, -3, -1]])
    P = V
    S = P
    H = sp.Matrix([[0, 1, 1], [1, 0, 1], [1, 1, 0]])

    assert V.T * H * V == sp.diag(22, -10, -110)

    unique = {
        (0, 1): square_free_product(P.row(0).T, P.row(1).T),
        (0, 2): square_free_product(P.row(0).T, P.row(2).T),
        (1, 2): square_free_product(P.row(1).T, P.row(2).T),
    }
    assert unique[0, 1] == sp.Matrix([3, 6, -1])
    assert unique[0, 2] == sp.Matrix([0, 20, -22])
    assert unique[1, 2] == sp.Matrix([-3, -26, 23])
    assert sum(unique.values(), sp.zeros(3, 1)) == sp.zeros(3, 1)
    assert sp.Matrix.hstack(*unique.values()).rank() == 2

    off = product_matrix(P, S)
    assert off.rank() == 2
    kernel = sp.Matrix.hstack(*off.nullspace())
    assert kernel.shape == (6, 4)
    for fixed_first in (True, False):
        for colour in range(3):
            indices = [
                index
                for index, (c, d) in enumerate(ORDERED)
                if (c if fixed_first else d) == colour
            ]
            assert off[:, indices].rank() == 2
            assert sp.Matrix.hstack(
                kernel, coordinate_plane(indices)
            ).rank() == 6

    all_products = product_matrix(
        P, S, tuple(product(range(3), repeat=2))
    )
    assert all_products.rank() == 3
    assert all(P[c, i] != 0 for c, i in product(range(3), repeat=2))


def audit_asymmetric_three_site_model() -> None:
    # A second exact model shows that equality of the two stars is not
    # responsible for raw rank three.
    H = sp.Matrix([[0, 1, 1], [1, 0, 1], [1, 1, 0]])
    P = sp.Matrix([[1, 1, 1], [1, 2, 3], [1, 4, 9]])
    S = (H.inv() * P.inv()).T
    assert P * H * S.T == sp.eye(3)
    assert all(entry != 0 for entry in P)
    assert all(entry != 0 for entry in S)

    off = product_matrix(P, S)
    assert off.rank() == 2
    for fixed_first in (True, False):
        for colour in range(3):
            indices = [
                index
                for index, (c, d) in enumerate(ORDERED)
                if (c if fixed_first else d) == colour
            ]
            assert off[:, indices].rank() == 2

    all_products = product_matrix(
        P, S, tuple(product(range(3), repeat=2))
    )
    assert all_products.rank() == 3


def audit_cap_quotient_dimensions() -> None:
    X = sp.eye(4)[:, :3]
    q_outside = sp.eye(4)[:, 3]
    q_inside = X[:, 0] + 2 * X[:, 1] - 3 * X[:, 2]

    assert X.rank() == 3
    assert sp.Matrix.hstack(X, q_outside).rank() - 1 == 3
    assert sp.Matrix.hstack(X, q_inside).rank() - 1 == 2


def audit_transition_symmetry_identity() -> None:
    d0, d1, d2 = sp.symbols("d0 d1 d2")
    entries = sp.symbols("t0:9")
    T = sp.Matrix(3, 3, entries)
    D = sp.diag(d0, d1, d2)
    skew = D * T - T.T * D
    for i in range(3):
        for j in range(3):
            assert sp.expand(skew[i, j]) == sp.expand(
                [d0, d1, d2][i] * T[i, j]
                - [d0, d1, d2][j] * T[j, i]
            )

    a, b, c = sp.symbols("a b c", nonzero=True)
    relation = sp.Matrix([[0, a, b], [a, 0, c], [b, c, 0]])
    assert sp.factor(relation.det()) == 2 * a * b * c


def audit_site_kernel_dimension_patterns() -> None:
    # For a three-space, kernel dimensions below three can only be zero,
    # one site line, or two site lines.  A nondegenerate block tensor has
    # rank three and therefore forces the site intersections to span.
    patterns = []
    for d0 in range(4):
        for d1 in range(4 - d0):
            for d2 in range(4 - d0 - d1):
                dims = tuple(d for d in (d0, d1, d2) if d)
                if sum(dims) <= 3:
                    kernel_dim = sum(d * (d + 1) // 2 for d in dims)
                    patterns.append((tuple(sorted(dims, reverse=True)), kernel_dim))
    assert ((1,), 1) in patterns
    assert ((1, 1), 2) in patterns
    assert ((1, 1, 1), 3) in patterns
    assert ((2,), 3) in patterns
    assert all(
        dims == (1, 1)
        for dims, kernel_dim in patterns
        if kernel_dim == 2
    )


def audit_intersection_one_determinant() -> None:
    # In bases adapted to a one-dimensional intersection, the ordinary
    # lifted tensor has blocks H, P', S' of sizes 1, 2, 2.
    entries = sp.symbols("m0:9")
    M = sp.Matrix(3, 3, entries)
    a = M[:1, :1]
    b = M[:1, 1:]
    c = M[1:, :1]
    d = M[1:, 1:]
    lifted = sp.Matrix.vstack(
        sp.Matrix.hstack(a + a.T, c.T, b),
        sp.Matrix.hstack(c, sp.zeros(2), d),
        sp.Matrix.hstack(b.T, d.T, sp.zeros(2)),
    )
    assert sp.factor(lifted.det() - 2 * M.det() * d.det()) == 0

    # The final coordinate calculation in Lemma 8.1.
    x0, x1, x2, x3 = sp.symbols("x0:4")
    top = sp.Matrix([[x0, x1], [x2, x3]])
    J = sp.Matrix([[0, -1], [1, 0]])
    candidate = J.T * top.adjugate()
    equations = list(candidate + candidate.T)
    solution = sp.solve(equations, (x0, x1, x2, x3), dict=True)
    assert solution == [{x0: x3, x1: 0, x2: 0}]


def audit_four_line_cube_lemma() -> None:
    vertices = tuple(product((-1, 1), repeat=3))
    tetrahedra = {
        tuple(sorted(chosen))
        for chosen in combinations(vertices, 4)
        if sp.Matrix([[*vertex, 1] for vertex in chosen]).det() != 0
    }
    assert len(tetrahedra) == 58

    group = tuple(
        (permutation, signs)
        for permutation in permutations(range(3))
        for signs in product((-1, 1), repeat=3)
    )

    def act(tetrahedron, element):
        permutation, signs = element
        return tuple(
            sorted(
                tuple(
                    signs[j] * vertex[permutation[j]]
                    for j in range(3)
                )
                for vertex in tetrahedron
            )
        )

    unseen = set(tetrahedra)
    representatives = []
    orbit_sizes = []
    while unseen:
        representative = min(unseen)
        orbit = {act(representative, element) for element in group}
        orbit &= tetrahedra
        representatives.append(representative)
        orbit_sizes.append(len(orbit))
        unseen -= orbit
    assert orbit_sizes == [8, 24, 24, 2]

    observed = []
    for representative in representatives:
        sign_matrix = sp.Matrix([[*vertex, 1] for vertex in representative])
        first = representative[0]
        cases = []
        for branches in product((0, 1), repeat=3):
            equations = []
            for vertex, reflected in zip(
                representative[1:], branches, strict=True
            ):
                if reflected:
                    equations.append(
                        [vertex[j] + first[j] for j in range(3)] + [-2]
                    )
                else:
                    equations.append(
                        [vertex[j] - first[j] for j in range(3)] + [0]
                    )
            nullspace = sp.Matrix(equations).nullspace()
            if len(nullspace) != 1:
                continue
            magnitudes = nullspace[0]
            if any(value == 0 for value in magnitudes):
                continue
            scaled_inverse = sp.diag(
                *(1 / value for value in magnitudes)
            ) * sign_matrix.inv()
            p_supports = tuple(
                sum(scaled_inverse[c, i] != 0 for i in range(4))
                for c in range(3)
            )
            s_supports = tuple(
                sum(
                    sp.simplify(
                        scaled_inverse[c, i] + scaled_inverse[3, i]
                    )
                    != 0
                    for i in range(4)
                )
                for c in range(3)
            )
            cases.append((p_supports, s_supports))
        observed.append(cases)

    assert observed[0] == [((2, 2, 2), (4, 4, 4))]
    assert observed[1] == []
    assert observed[2] == [((4, 2, 2), (4, 2, 2))]
    assert len(observed[3]) == 4
    assert all(case == ((4, 4, 4), (2, 2, 2)) for case in observed[3])


def audit_fat_plane_sign_tables() -> None:
    t = sp.symbols("t", nonzero=True)
    circuit = sp.Matrix([1, 1, 1, -1, -1])

    global_vectors = {}
    for c in range(3):
        p = sp.zeros(5, 1)
        p[c] = 1
        p[3] = 1
        global_vectors[f"p{c}"] = p
        s = sp.zeros(5, 1)
        s[c] = 1
        s[4] = 1
        global_vectors[f"s{c}"] = s
    assert all((circuit.T * value)[0] == 0 for value in global_vectors.values())

    cases = {
        "PP": (
            (
                sp.Matrix([1, -1, 0, 0, 0]),
                sp.Matrix([0, 0, t + 1, 1, t]),
            ),
            (
                sp.Matrix([t, t, -t - 1, -1, t]),
                sp.Matrix([1, 1, -t - 1, 1, -t]),
                sp.Matrix([t + 1, t + 1, -t - 1, 1, t]),
            ),
            {
                (0, 1): {"p0", "p1", "s0", "s1"},
                (0, 2): {"s0", "s1"},
                (1, 2): {"p0", "p1"},
            },
        ),
        "PN": (
            (
                sp.Matrix([-1, 0, 0, -1, 0]),
                sp.Matrix([0, 1, t, 0, t + 1]),
            ),
            (
                sp.Matrix([-t - 1, 1, t, t + 1, -t - 1]),
                sp.Matrix([t, 1, -t, -t, t + 1]),
                sp.Matrix([-1, 1, -t, 1, -t - 1]),
                sp.Matrix([t + 1, -1, -t, -t - 1, t + 1]),
            ),
            {
                (0, 1): {"p0", "p2", "s0"},
                (0, 2): {"p0", "p1", "s0"},
                (0, 3): None,
                (1, 2): {"p0", "p1", "p2"},
                (1, 3): {"p0", "p2", "s0"},
                (2, 3): {"p0", "p1", "s0"},
            },
        ),
        "NN": (
            (
                sp.Matrix([0, 0, 0, -1, 1]),
                sp.Matrix([1, t, -t - 1, 0, 0]),
            ),
            (
                sp.Matrix([-1, -t, -t - 1, -t - 1, -t - 1]),
                sp.Matrix([-1, t, t + 1, t, t]),
                sp.Matrix([-1, t, -t - 1, -1, -1]),
            ),
            {
                (0, 1): {"p1", "p2", "s1", "s2"},
                (0, 2): {"p0", "p2", "s0", "s2"},
                (1, 2): {"p0", "p1", "s0", "s1"},
            },
        ),
    }

    def square(vector: sp.Matrix) -> sp.Matrix:
        return vector.applyfunc(lambda entry: sp.expand(entry**2))

    for plane, outside, expected in cases.values():
        plane_squares = sp.Matrix.hstack(*(square(vector) for vector in plane))
        assert plane_squares.rank() == 2
        for vector in (*plane, *outside):
            assert sp.factor((circuit.T * vector)[0]) == 0
        for vector in outside:
            augmented = sp.Matrix.hstack(plane_squares, square(vector))
            assert all(
                sp.factor(augmented.extract(rows, (0, 1, 2)).det()) == 0
                for rows in combinations(range(5), 3)
            )

        for pair, forced in expected.items():
            basis = sp.Matrix.hstack(*plane, outside[pair[0]], outside[pair[1]])
            minors = {
                rows: sp.factor(basis.extract(rows, range(4)).det())
                for rows in combinations(range(5), 4)
            }
            nonzero_rows = next(
                (rows for rows, determinant in minors.items() if determinant != 0),
                None,
            )
            if forced is None:
                assert nonzero_rows is None
                continue
            assert nonzero_rows is not None
            determinant = minors[nonzero_rows]
            assert sp.factor(
                determinant / (4 * t * (t + 1))
            ) in (-1, 1)
            square_basis = basis.extract(nonzero_rows, range(4))
            actually_forced = set()
            for name, vector in global_vectors.items():
                coordinates = square_basis.inv() * vector.extract(nonzero_rows, (0,))
                coordinates = tuple(sp.factor(value) for value in coordinates)
                support = int(coordinates[0] != 0 or coordinates[1] != 0)
                support += int(coordinates[2] != 0) + int(coordinates[3] != 0)
                if support <= 2:
                    actually_forced.add(name)
            assert actually_forced == forced


def main() -> None:
    audit_symmetric_three_site_model()
    audit_asymmetric_three_site_model()
    audit_cap_quotient_dimensions()
    audit_transition_symmetry_identity()
    audit_site_kernel_dimension_patterns()
    audit_intersection_one_determinant()
    audit_four_line_cube_lemma()
    audit_fat_plane_sign_tables()
    print("All-dead corank-two product reduction: PASS")


if __name__ == "__main__":
    main()
