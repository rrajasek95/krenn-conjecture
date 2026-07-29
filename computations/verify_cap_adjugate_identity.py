#!/usr/bin/env python3
"""Exact audit of the universal eight-to-six cap-adjugate identity."""

from __future__ import annotations

import itertools

import sympy as sp


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        for matching in perfect_matchings(rest):
            yield ((first, second),) + matching


def permutation_sign(permutation):
    inversions = sum(
        permutation[i] > permutation[j]
        for i in range(len(permutation))
        for j in range(i + 1, len(permutation))
    )
    return -1 if inversions % 2 else 1


def edge_value(edges, u, v, color_u, color_v):
    if u < v:
        return edges[(u, v)][color_u, color_v]
    return edges[(v, u)][color_v, color_u]


def matching_tensor(vertices, edges, colors=3):
    vertices = tuple(vertices)
    position = {vertex: index for index, vertex in enumerate(vertices)}
    answer = {}
    for coloring in itertools.product(range(colors), repeat=len(vertices)):
        value = 0
        for matching in perfect_matchings(vertices):
            term = 1
            for u, v in matching:
                term *= edge_value(
                    edges,
                    u,
                    v,
                    coloring[position[u]],
                    coloring[position[v]],
                )
            value += term
        if value:
            answer[coloring] = sp.expand(value)
    return answer


def deterministic_dense_source():
    edges = {}
    for u, v in itertools.combinations(range(8), 2):
        matrix = sp.zeros(3, 3)
        for i, j in itertools.product(range(3), repeat=2):
            matrix[i, j] = ((17 * u + 29 * v + 11 * i + 7 * j + 3) % 9) - 4
        edges[u, v] = matrix
    return edges


def cap_family(edges, cap_i, cap_j):
    """B_ij on abstract boundary sites 0,...,5 for deleted pair 0,1."""

    boundary = tuple(range(2, 8))
    direct = edges[0, 1][cap_i, cap_j]
    family = {}
    for abstract_u, abstract_v in itertools.combinations(range(6), 2):
        u, v = boundary[abstract_u], boundary[abstract_v]
        matrix = sp.zeros(3, 3)
        for color_u, color_v in itertools.product(range(3), repeat=2):
            matrix[color_u, color_v] = sp.expand(
                direct * edge_value(edges, u, v, color_u, color_v)
                + edge_value(edges, 0, u, cap_i, color_u)
                * edge_value(edges, 1, v, cap_j, color_v)
                + edge_value(edges, 0, v, cap_i, color_v)
                * edge_value(edges, 1, u, cap_j, color_u)
            )
        family[abstract_u, abstract_v] = matrix
    return family


def product_of_three_families(families):
    """Top square-free product Y0*Y1*Y2 on six abstract sites."""

    answer = {}
    matchings = tuple(perfect_matchings(range(6)))
    for coloring in itertools.product(range(3), repeat=6):
        value = 0
        for matching in matchings:
            for assignment in itertools.permutations(range(3)):
                term = 1
                for edge_index, family_index in enumerate(assignment):
                    u, v = matching[edge_index]
                    term *= families[family_index][u, v][
                        coloring[u], coloring[v]
                    ]
                value += term
        if value:
            answer[coloring] = sp.expand(value)
    return answer


def add_scaled(target, source, scale):
    for key, value in source.items():
        target[key] = sp.expand(target.get(key, 0) + scale * value)
        if target[key] == 0:
            del target[key]


def determinant_boundary_tensor(families):
    answer = {}
    for permutation in itertools.permutations(range(3)):
        product = product_of_three_families(
            [families[row][permutation[row]] for row in range(3)]
        )
        add_scaled(answer, product, permutation_sign(permutation))
    return answer


def cofactor_matrix(matrix):
    return sp.Matrix(
        3,
        3,
        lambda i, j: (-1) ** (i + j) * matrix.minor_submatrix(i, j).det(),
    )


def verify_universal_identity():
    edges = deterministic_dense_source()
    full_tensor = matching_tensor(tuple(range(8)), edges)
    families = [
        [cap_family(edges, i, j) for j in range(3)] for i in range(3)
    ]
    left = determinant_boundary_tensor(families)

    direct = edges[0, 1]
    cofactors = cofactor_matrix(direct)
    right = {}
    for i, j in itertools.product(range(3), repeat=2):
        boundary_slice = {
            coloring: value
            for coloring in itertools.product(range(3), repeat=6)
            if (value := full_tensor.get((i, j) + coloring, 0)) != 0
        }
        add_scaled(right, boundary_slice, 2 * cofactors[i, j])
    assert left == right


def two_k4_source(direct):
    edges = {}
    for u, v in itertools.combinations(range(8), 2):
        edges[u, v] = sp.zeros(3, 3)
    edges[0, 4] = sp.Matrix(direct)
    for color in range(3):
        other = [index for index in range(3) if index != color]
        edges[0, 1 + color][color, color] = 1
        edges[tuple(sorted(1 + index for index in other))][color, color] = 1
        edges[4, 5 + color][color, color] = 1
        edges[tuple(sorted(5 + index for index in other))][color, color] = 1
    return edges


def cap_family_pair_04(edges, cap_i, cap_j):
    boundary = (1, 2, 3, 5, 6, 7)
    direct = edges[0, 4][cap_i, cap_j]
    family = {}
    for abstract_u, abstract_v in itertools.combinations(range(6), 2):
        u, v = boundary[abstract_u], boundary[abstract_v]
        matrix = sp.zeros(3, 3)
        for color_u, color_v in itertools.product(range(3), repeat=2):
            matrix[color_u, color_v] = (
                direct * edge_value(edges, u, v, color_u, color_v)
                + edge_value(edges, 0, u, cap_i, color_u)
                * edge_value(edges, 4, v, cap_j, color_v)
                + edge_value(edges, 0, v, cap_i, color_v)
                * edge_value(edges, 4, u, cap_j, color_u)
            )
        family[abstract_u, abstract_v] = matrix
    return family


def verify_six_cross_row_detection():
    direct = sp.Matrix([[1, 2, 3], [4, 5, 7], [8, 11, 13]])
    cofactors = cofactor_matrix(direct)
    assert direct.det() == 8
    assert cofactors == sp.Matrix([[-12, 4, 4], [7, -11, 5], [-1, 5, -3]])
    assert all(cofactors[i, j] != 0 for i, j in itertools.product(range(3), repeat=2))

    edges = two_k4_source(direct)
    actual = matching_tensor(tuple(range(8)), edges)
    expected_actual = {
        (left,) * 4 + (right,) * 4: sp.S.One
        for left, right in itertools.product(range(3), repeat=2)
    }
    assert actual == expected_actual

    families = [
        [cap_family_pair_04(edges, i, j) for j in range(3)]
        for i in range(3)
    ]
    determinant_tensor = determinant_boundary_tensor(families)
    expected_determinant = {
        (left,) * 3 + (right,) * 3: 2 * cofactors[left, right]
        for left, right in itertools.product(range(3), repeat=2)
    }
    assert determinant_tensor == expected_determinant

    formal_rhs = {
        (color,) * 6: 2 * cofactors[color, color] for color in range(3)
    }
    discrepancy = dict(determinant_tensor)
    add_scaled(discrepancy, formal_rhs, -1)
    assert discrepancy == {
        (left,) * 3 + (right,) * 3: 2 * cofactors[left, right]
        for left, right in itertools.product(range(3), repeat=2)
        if left != right
    }


def symbolic_minor_hierarchy():
    """Audit the d=1,2,3 identities for several arbitrary complement sizes."""

    x = sp.symbols("x")
    a_symbols = sp.symbols("a0:9")
    left_symbols = sp.symbols("l0:3")
    right_symbols = sp.symbols("m0:3")
    direct = sp.Matrix(3, 3, a_symbols)
    response = sp.Matrix(
        3,
        3,
        lambda i, j: left_symbols[i] * right_symbols[j],
    )

    subsets = {
        1: [((0,), (1,)), ((2,), (2,))],
        2: [((0, 1), (0, 2)), ((0, 2), (1, 2)), ((1, 2), (1, 2))],
        3: [((0, 1, 2), (0, 1, 2))],
    }
    for matching_size in range(3, 8):
        for minor_size, index_pairs in subsets.items():
            for rows, columns in index_pairs:
                direct_minor = direct.extract(rows, columns)
                response_minor = response.extract(rows, columns)
                scaled = x * direct_minor + sp.Rational(
                    matching_size, minor_size
                ) * response_minor
                left = (
                    sp.Rational(minor_size, sp.factorial(matching_size))
                    * x ** (matching_size - minor_size)
                    * scaled.det()
                )

                cofactors = cofactor_matrix(direct_minor) if minor_size == 3 else sp.Matrix(
                    minor_size,
                    minor_size,
                    lambda i, j: (-1) ** (i + j)
                    * direct_minor.minor_submatrix(i, j).det(),
                )
                right = 0
                for local_i, actual_i in enumerate(rows):
                    for local_j, actual_j in enumerate(columns):
                        top_slice = (
                            direct[actual_i, actual_j]
                            * x**matching_size
                            / sp.factorial(matching_size)
                            + response[actual_i, actual_j]
                            * x ** (matching_size - 1)
                            / sp.factorial(matching_size - 1)
                        )
                        right += cofactors[local_i, local_j] * top_slice
                assert sp.expand(left - right) == 0

    # For a 2x2 minor whose row and column sets meet only at i, the GHZ
    # specialization retains exactly the complementary entry a_(k,l) E_i.
    rows, columns = (0, 1), (0, 2)
    direct_minor = direct.extract(rows, columns)
    cofactors = sp.Matrix(
        2,
        2,
        lambda i, j: (-1) ** (i + j)
        * direct_minor.minor_submatrix(i, j).det(),
    )
    assert cofactors[0, 0] == direct[1, 2]

    # After GL normalization a=I, B=xI+c*l*m^T.  Its determinant and
    # adjugate retain only the first rank-one update, but no nonzero scalar
    # combination alpha*x+beta*rho can have a cube proportional to
    # x^2*(x+rho) as a universal polynomial.
    rho, alpha, beta, scale = sp.symbols("rho alpha beta scale")
    normalized = x * sp.eye(3) + sp.Matrix(left_symbols) * sp.Matrix(
        1, 3, right_symbols
    )
    rho_expression = sum(
        left_symbols[i] * right_symbols[i] for i in range(3)
    )
    assert sp.expand(normalized.det() - x**2 * (x + rho_expression)) == 0
    expected_adjugate = x**2 * sp.eye(3) + x * (
        rho_expression * sp.eye(3)
        - sp.Matrix(left_symbols) * sp.Matrix(1, 3, right_symbols)
    )
    assert normalized.adjugate().applyfunc(sp.expand) == expected_adjugate.applyfunc(
        sp.expand
    )
    cube_difference = sp.Poly(
        sp.expand((alpha * x + beta * rho) ** 3 - scale * x**2 * (x + rho)),
        x,
        rho,
    )
    equations = [coefficient for _, coefficient in cube_difference.terms()]
    groebner = sp.groebner(equations + [1 - sp.symbols("w") * scale],
                           sp.symbols("w"), scale, alpha, beta,
                           order="lex")
    assert groebner.contains(sp.S.One)


def main():
    verify_universal_identity()
    verify_six_cross_row_detection()
    symbolic_minor_hierarchy()
    print("universal dense cap-adjugate identity: PASS")
    print("all six formal cross-row corrections detected exactly: PASS")
    print("all d=1,2,3 minor identities and normalized no-cube test: PASS")


if __name__ == "__main__":
    main()
