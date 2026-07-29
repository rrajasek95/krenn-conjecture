#!/usr/bin/env python3
"""Exact audits for the simple-discriminant rooted collision boundary."""

from __future__ import annotations

import itertools
from fractions import Fraction

import verify_color_collision_n_plus_two as low
import verify_dense_diagonal_collision_obstruction as dense


X, Y, Z = low.X, low.Y, low.Z


def trim(poly):
    poly = list(poly)
    while len(poly) > 1 and poly[-1] == 0:
        poly.pop()
    return tuple(poly)


def poly_add(left, right):
    degree = max(len(left), len(right))
    return trim(tuple(
        (left[i] if i < len(left) else 0)
        + (right[i] if i < len(right) else 0)
        for i in range(degree)
    ))


def poly_scale(poly, scalar):
    return trim(tuple(Fraction(scalar) * value for value in poly))


def poly_multiply(left, right):
    answer = [Fraction(0)] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            answer[i + j] += a * b
    return trim(tuple(answer))


def product(factors):
    answer = (Fraction(1),)
    for factor in factors:
        answer = poly_multiply(answer, factor)
    return answer


def rooted_target(n):
    """Formula (18i), as a polynomial for each x/z coloring."""
    answer = {}
    for coloring in itertools.product((X, Z), repeat=n):
        main = (Fraction(1),) if coloring == (X,) * n else (Fraction(0),)
        if coloring[0] != Z:
            entering = (Fraction(0),)
        else:
            first = []
            second = []
            for site in range(1, n):
                if coloring[site] == X:
                    first.append((Fraction(1),))
                    second.append((Fraction(1),))
                else:
                    first.append((Fraction(0),))
                    second.append((Fraction(0), Fraction(-1)))
            difference = poly_add(product(first), poly_scale(product(second), -1))
            entering = poly_multiply((Fraction(0), Fraction(1, 2)), difference)
        answer[coloring] = poly_add(main, entering)
    return answer


def k4_boundary_source():
    """Edge-entry polynomials for the centered a=(2,0,0,0) K4 arc."""
    tables = {
        # Surviving v matching 03|12.
        (0, 3, X, X): (Fraction(1),),
        (0, 3, Z, X): (Fraction(0), Fraction(1, 2)),
        (1, 2, X, X): (Fraction(1),),
        # Entering u matching 01|23.
        (0, 1, Z, X): (Fraction(0), Fraction(-1, 2)),
        (0, 1, Z, Z): (Fraction(0), Fraction(0), Fraction(1, 2)),
        (2, 3, X, X): (Fraction(1),),
        (2, 3, Z, X): (Fraction(0), Fraction(-1)),
        (2, 3, X, Z): (Fraction(0), Fraction(-1)),
        (2, 3, Z, Z): (Fraction(0), Fraction(0), Fraction(1)),
        # y matching 02|13.
        (0, 2, Y, Y): (Fraction(1),),
        (1, 3, Y, Y): (Fraction(1),),
    }
    return tables


def polynomial_output(n, tables):
    answer = {}
    for coloring in itertools.product((X, Y, Z), repeat=n):
        total = (Fraction(0),)
        for matching in low.perfect_matchings(range(n)):
            term = (Fraction(1),)
            for u, v in matching:
                term = poly_multiply(
                    term, tables.get((u, v, coloring[u], coloring[v]), (0,))
                )
            total = poly_add(total, term)
        answer[coloring] = total
    return answer


def audit_exact_boundary_and_k4():
    expected = rooted_target(4)
    actual = polynomial_output(4, k4_boundary_source())
    for coloring, value in actual.items():
        if coloring == (Y,) * 4:
            wanted = (Fraction(1),)
        elif Y in coloring:
            wanted = (Fraction(0),)
        else:
            wanted = expected[coloring]
        assert value == wanted, (coloring, value, wanted)

    q0 = {
        key: polynomial[0]
        for key, polynomial in k4_boundary_source().items()
        if polynomial[0]
    }
    assert len(q0) == 5
    assert q0[(2, 3, X, X)] == 1
    # The extra base cell 23;xx has zero cofactor because 01 has no base cell.
    coloring = (X,) * 4
    assert low.weighted_matchings(q0, (0, 1), coloring) == 0

    minimal = dict(q0)
    minimal.pop((2, 3, X, X))
    assert len(minimal) == 4
    # The rooted coefficient at the same-shore pair 01 is frozen at zero on
    # the complete homogeneous tangent kernels and direct W image.
    assert frozen_pair(4, minimal, 0, 1)
    assert expected[(Z, Z, X, X)][2] == Fraction(1, 2)


def sector_data(n, q0):
    answer = {}
    for site in range(n):
        columns, matrix, _ = low.sector_system(n, q0, site)
        answer[site] = (columns, low.nullspace(matrix))
    return answer


def frozen_pair(n, q0, first, second, data=None):
    if data is None:
        data = sector_data(n, q0)
    first_columns, first_kernel = data[first]
    second_columns, second_kernel = data[second]
    hessian = low.hessian_matrix(
        n, q0, first, second, first_columns, second_columns
    )
    return (
        low.q2_cofactor(n, q0, first, second) == 0
        and all(
            low.bilinear(left, hessian, right) == 0
            for left in first_kernel
            for right in second_kernel
        )
    )


def audit_frozen_edge_cover():
    audits = 0
    for n in (6, 8, 10):
        m = n // 2
        switch_positions = range(1, m // 2 + 1) if n < 10 else (1,)
        for r in switch_positions:
            for mode in ("interior",):
                q0 = low.x_switch_base(n, r, mode)
                data = sector_data(n, q0)
                core = {0, 1, 2 * r, 2 * r + 1}
                tail = set(range(n)) - core
                assert tail
                if mode == "interior":
                    for first in core:
                        for second in tail:
                            pair = tuple(sorted((first, second)))
                            assert frozen_pair(n, q0, *pair, data=data)
                audits += 1

                q0 = low.y_switch_base(n, r, mode)
                data = sector_data(n, q0)
                if mode == "interior":
                    for second in range(2, n):
                        if second != 2 * r - 1:
                            assert frozen_pair(n, q0, 0, second, data=data)
                        if second != 2 * r - 2:
                            assert frozen_pair(n, q0, 1, second, data=data)
                audits += 1
    return audits


def audit_dense_rooted_star():
    """The dense six-site vertex-kernel chart also rejects every root."""
    q0 = dense.dense_base()
    variables, _particular, basis = dense.first_family(q0)
    variable_index = {key: index for index, key in enumerate(variables)}
    pair_index = {pair: index for index, pair in enumerate(dense.PAIRS)}

    for root in range(dense.N):
        rows = []
        colorings = (
            coloring
            for coloring in itertools.product((X, Y, Z), repeat=dense.N)
            if coloring.count(Z) == 2
        )
        for coloring in colorings:
            z_sites = tuple(
                site for site, color in enumerate(coloring) if color == Z
            )
            q2_part = [Fraction(0)] * len(dense.EDGES)
            quadratic = [Fraction(0)] * len(dense.PAIRS)
            constant = -Fraction(
                int(
                    root in z_sites
                    and all(
                        coloring[site] == X
                        for site in range(dense.N)
                        if site not in z_sites
                    )
                )
            )
            for matching in dense.MATCHINGS:
                for position, edge in enumerate(matching):
                    u, v = edge
                    if coloring[u] != Z or coloring[v] != Z:
                        continue
                    coefficient = Fraction(1)
                    for other, (a, b) in enumerate(matching):
                        if other != position:
                            coefficient *= q0.get(
                                (a, b, coloring[a], coloring[b]), 0
                            )
                    q2_part[dense.EDGES.index(edge)] += coefficient

                for first, second in itertools.combinations(range(3), 2):
                    remaining = 3 - first - second
                    a, b = matching[remaining]
                    coefficient = q0.get(
                        (a, b, coloring[a], coloring[b]), 0
                    )
                    if not coefficient:
                        continue
                    u, v = matching[first]
                    c, d = matching[second]
                    left = variable_index.get(
                        (u, v, coloring[u], coloring[v])
                    )
                    right = variable_index.get(
                        (c, d, coloring[c], coloring[d])
                    )
                    if left is None or right is None:
                        continue
                    for i in range(dense.N):
                        for j in range(i, dense.N):
                            value = basis[i][left] * basis[j][right]
                            if i != j:
                                value += basis[j][left] * basis[i][right]
                            quadratic[pair_index[(i, j)]] += coefficient * value
            row = q2_part + quadratic + [constant]
            if any(row):
                rows.append(row)

        reduced, _pivots = dense.rref(rows)
        eliminated = [
            row for row in reduced if not any(row[: len(dense.EDGES)])
        ]
        assert len(eliminated) == len(dense.EDGES)
        constants = {}
        for row in eliminated:
            support = [
                (pair, coefficient)
                for pair, coefficient in zip(
                    dense.PAIRS, row[len(dense.EDGES) : -1], strict=True
                )
                if coefficient
            ]
            assert len(support) == 1 and support[0][0][0] != support[0][0][1]
            pair, coefficient = support[0]
            assert coefficient == 1
            constants[pair] = -row[-1]
        assert set(constants) == set(dense.EDGES)
        assert all(
            constants[pair] != 0
            if root in pair
            else constants[pair] == 0
            for pair in dense.EDGES
        )

        others = [site for site in range(dense.N) if site != root]
        first, second = others[:2]
        # The eliminated equations are
        # t_root*t_first != 0, t_root*t_second != 0, t_first*t_second = 0.
        assert constants[tuple(sorted((root, first)))] != 0
        assert constants[tuple(sorted((root, second)))] != 0
        assert constants[tuple(sorted((first, second)))] == 0


def main():
    audit_exact_boundary_and_k4()
    audits = audit_frozen_edge_cover()
    audit_dense_rooted_star()
    print("verified exact simple-boundary rooted-star target and K4 source")
    print("verified inactive K4 base cell is essential to the rooted jet")
    print(f"verified {audits} switched-base frozen-edge covers for every root")
    print("verified dense six-site elimination rejects every rooted star")


if __name__ == "__main__":
    main()
