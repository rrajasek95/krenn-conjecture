#!/usr/bin/env python3
"""Verify the full two-dense/one-edge diagonal collision obstruction.

Up to block/vertex permutations and nonzero diagonal gauges, the DDE chart
has y matching 01|23|45 and x cross-blocks

    lambda H,  [[1,1],[s,-s]],  [[1,0],[0,0]],
    lambda = -2/(s+1).

The chart conditions are s != 0,-1.  For s != 1 this script verifies the
complete tangent kernels and a three-pair cofactor-quotient certificate.
At s=1 it verifies directly that pair 23 is frozen on the enlarged tangent
kernels.
"""

from __future__ import annotations

import itertools

import sympy as sp

import explore_sparse_diagonal_collision_quotients as low
from verify_color_collision_n_plus_two import (
    X,
    Y,
    bilinear,
    hessian_matrix,
    nullspace,
    q2_cofactor,
    sector_system,
    weighted_matchings,
)


S = sp.symbols("s")
LAMBDA = -sp.Rational(2) / (S + 1)


def family_base():
    q0 = {}
    blocks = (
        ((LAMBDA, LAMBDA), (LAMBDA, -LAMBDA)),
        ((1, 1), (S, -S)),
        ((1, 0), (0, 0)),
    )
    for (left_index, right_index), matrix in zip(low.BLOCK_PAIRS, blocks):
        left, right = low.BLOCKS[left_index], low.BLOCKS[right_index]
        for row, u in enumerate(left):
            for column, v in enumerate(right):
                value = sp.sympify(matrix[row][column])
                if value != 0:
                    q0[(u, v, X, X)] = value
    for edge in low.BLOCKS:
        q0[edge + (Y, Y)] = sp.Integer(1)
    return q0


def verify_binary_output(q0):
    for coloring in itertools.product((X, Y), repeat=low.N):
        value = sp.factor(weighted_matchings(q0, low.VERTICES, coloring))
        target = 2 if coloring == (X,) * low.N else int(coloring == (Y,) * low.N)
        assert sp.factor(value - target) == 0, (coloring, value)


def generic_tangent_forms():
    a, b, u, c, d, v, f, g = sp.symbols("a b u c d v f g")
    forms = {
        (site, other, color): sp.Integer(0)
        for site in low.VERTICES
        for other in low.VERTICES
        if site != other
        for color in (X, Y)
    }

    def add(site, parameter, coefficients):
        for other, value in coefficients.items():
            forms[(site, other, X)] += parameter * value

    add(0, a, {2: 2 / (S * (S + 1)), 3: 2 / (S * (S + 1)), 4: 1, 5: 1})
    add(1, b, {2: -2 / (S + 1), 3: 2 / (S + 1), 4: -1, 5: 1})
    add(2, u, {0: 1, 1: 1})
    add(2, c, {4: (S - 1) / (S + 1), 5: 1})
    add(3, d, {0: 2 * (S - 1) / (S + 1) ** 2,
                1: -2 * (S - 1) / (S + 1) ** 2, 4: 1})
    add(4, v, {0: 1 / S, 1: 1})
    add(4, f, {2: -(S - 1) / (S + 1), 3: 1})
    add(5, g, {0: (S - 1) / (S + 1),
                1: -S * (S - 1) / (S + 1), 2: 1})
    return (a, b, u, c, d, v, f, g), forms


def verify_generic_kernels(q0, parameters, forms):
    expected_nullities = (1, 1, 2, 1, 2, 1)
    for site, expected in enumerate(expected_nullities):
        columns, matrix, _ = sector_system(low.N, q0, site)
        vector = [forms[(site, other, color)] for other, color in columns]
        for row in matrix:
            assert sp.factor(sum(sp.sympify(x) * y for x, y in zip(row, vector))) == 0

    # Fixed maximal minors prove that the displayed independent vectors are
    # the complete kernels away from s=0,-1,1.
    row_sets = (
        (0, 1, 3, 4, 11, 12, 14, 15, 31),
        (0, 1, 3, 4, 11, 12, 14, 15, 31),
        (0, 1, 2, 3, 11, 19, 27, 31),
        (0, 1, 2, 3, 8, 16, 24, 27, 31),
        (0, 2, 4, 6, 14, 22, 30, 31),
        (0, 2, 4, 6, 8, 16, 24, 30, 31),
    )
    column_sets = (
        (0, 1, 2, 3, 4, 5, 6, 7, 9),
        (0, 1, 2, 3, 4, 5, 6, 7, 9),
        (0, 1, 3, 4, 5, 6, 7, 9),
        (0, 1, 2, 3, 4, 5, 7, 8, 9),
        (0, 1, 3, 4, 5, 7, 8, 9),
        (0, 1, 2, 3, 5, 6, 7, 8, 9),
    )
    expected_determinants = (
        8 * S**4 / (S + 1) ** 3,
        -8 / (S + 1) ** 3,
        -64 * (S - 1) / (S + 1) ** 4,
        8 * S * (S - 1) / (S + 1),
        -8 * S**2 * (S - 1) / (S + 1),
        -32 * (S - 1) / (S + 1) ** 3,
    )
    for site in low.VERTICES:
        _, matrix, _ = sector_system(low.N, q0, site)
        minor = sp.Matrix(matrix).extract(row_sets[site], column_sets[site])
        assert sp.factor(minor.det() - expected_determinants[site]) == 0


def row(q0, forms, first, second, tail):
    coloring = {}
    tail_iter = iter(tail)
    for vertex in low.VERTICES:
        if vertex not in (first, second):
            coloring[vertex] = next(tail_iter)
    cofactor = sp.factor(low.complement_cofactor(q0, first, second, coloring))
    hessian = sp.factor(low.hessian_component(q0, forms, first, second, coloring))
    target = sp.Rational(1, 2) if all(color == X for color in tail) else 0
    return cofactor, sp.factor(hessian - target)


def verify_triangle_certificate(q0, parameters, forms):
    a, _, _, c, d, _, _, _ = parameters

    # Pair 02: compare complement colors xxyy and xxxx.
    c_pivot, r_pivot = row(q0, forms, 0, 2, (X, X, Y, Y))
    c_x, r_x = row(q0, forms, 0, 2, (X, X, X, X))
    wedge_02 = sp.factor(c_pivot * r_x - c_x * r_pivot)
    f02 = 8 * a * c - (S + 1)
    assert sp.factor(wedge_02 - f02 / (S + 1) ** 2) == 0

    # Pair 03: compare xxxx and xxyy.
    c_pivot, r_pivot = row(q0, forms, 0, 3, (X, X, X, X))
    c_mixed, r_mixed = row(q0, forms, 0, 3, (X, X, Y, Y))
    wedge_03 = sp.factor(c_pivot * r_mixed - c_mixed * r_pivot)
    f03 = 8 * a * d + (S + 1)
    assert sp.factor(wedge_03 + f03 / (S + 1) ** 2) == 0

    # Pair 23: the yyyy cofactor is one, while yyxx has zero cofactor.
    c_pivot, r_pivot = row(q0, forms, 2, 3, (Y, Y, Y, Y))
    c_mixed, r_mixed = row(q0, forms, 2, 3, (Y, Y, X, X))
    f23 = c * d
    assert (c_pivot, r_pivot, c_mixed) == (1, 0, 0)
    assert sp.factor(r_mixed - f23) == 0

    certificate = 8 * a * c * f03 - 64 * a**2 * f23 - (S + 1) * f02
    assert sp.expand(certificate - (S + 1) ** 2) == 0
    return f02, f03, f23


def verify_rank_drop_frozen_pair(q0):
    specialized = {
        key: sp.Rational(value.subs(S, 1)) if hasattr(value, "subs") else value
        for key, value in q0.items()
    }
    sectors = {}
    for site in low.VERTICES:
        columns, matrix, _ = sector_system(low.N, specialized, site)
        sectors[site] = columns, nullspace(matrix)
    assert tuple(len(sectors[site][1]) for site in low.VERTICES) == (1, 1, 3, 2, 3, 2)
    first_columns, first_kernel = sectors[2]
    second_columns, second_kernel = sectors[3]
    hessian = hessian_matrix(
        low.N, specialized, 2, 3, first_columns, second_columns
    )
    assert q2_cofactor(low.N, specialized, 2, 3) == 0
    assert all(
        bilinear(left, hessian, right) == 0
        for left in first_kernel
        for right in second_kernel
    )


def verify_nonfrozen_rational_point(q0):
    specialized = {
        key: sp.Rational(value.subs(S, -2)) if hasattr(value, "subs") else value
        for key, value in q0.items()
    }
    sectors = {}
    for site in low.VERTICES:
        columns, matrix, _ = sector_system(low.N, specialized, site)
        sectors[site] = columns, nullspace(matrix)

    for first, second in low.EDGES:
        remaining = tuple(v for v in low.VERTICES if v not in (first, second))
        full_cofactor_nonzero = any(
            weighted_matchings(
                specialized, remaining, dict(zip(remaining, coloring))
            )
            for coloring in itertools.product((X, Y), repeat=4)
        )
        assert full_cofactor_nonzero

        if q2_cofactor(low.N, specialized, first, second):
            continue
        first_columns, first_kernel = sectors[first]
        second_columns, second_kernel = sectors[second]
        hessian = hessian_matrix(
            low.N, specialized, first, second, first_columns, second_columns
        )
        assert any(
            bilinear(left, hessian, right) != 0
            for left in first_kernel
            for right in second_kernel
        ), (first, second)


def main():
    q0 = family_base()
    verify_binary_output(q0)
    parameters, forms = generic_tangent_forms()
    verify_generic_kernels(q0, parameters, forms)
    equations = verify_triangle_certificate(q0, parameters, forms)
    verify_rank_drop_frozen_pair(q0)
    verify_nonfrozen_rational_point(q0)
    print("verified symbolic DDE base H(q0)=2X+Y")
    print("verified complete generic tangent kernels and maximal minors")
    print("generic pair equations:", equations)
    print("verified localized certificate equals (s+1)^2")
    print("verified s=1 rank-drop frozen pair 23")
    print("verified s=-2 has all full cofactors nonzero and no frozen pair")


if __name__ == "__main__":
    main()
