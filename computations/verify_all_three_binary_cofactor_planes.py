#!/usr/bin/env python3
"""Exact audits for the all-three-binary cofactor-plane boundary.

The script checks three independent claims:

* the symbolic four-site cofactor-plane tensor has a nonzero 3x3
  flattening minor on the entire cofactor-open locus;
* the displayed cubic Bianchi formula equals direct matching enumeration
  for a dense rational six-site two-jet; and
* the standard six-site three-factor source has all three binary faces and
  every cubic through the color-zero endpoint exact, but escapes through
  twelve zero leading cofactors and one degree-four ternary singleton.
"""

from __future__ import annotations

from fractions import Fraction
from functools import cache, reduce
from itertools import combinations, permutations, product

import sympy as sp


def edge(i: int, j: int) -> tuple[int, int]:
    return (i, j) if i < j else (j, i)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position, partner in enumerate(vertices[1:], 1):
        remainder = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(remainder):
            yield ((first, partner),) + tail


def audit_symbolic_four_site_flattening() -> None:
    vertices = tuple(range(4))
    edges = tuple(combinations(vertices, 2))
    matchings = tuple(perfect_matchings(vertices))
    symbols = sp.symbols("c01 c02 c03 c12 c13 c23")
    leading = dict(zip(edges, symbols))

    def cofactor(i, j):
        remaining = [vertex for vertex in vertices if vertex not in (i, j)]
        return leading[edge(*remaining)]

    # At each site choose the first two neighbor coordinates freely and
    # solve the cofactor-kernel equation in the last coordinate.
    bases = []
    for basis_index in range(2):
        values = {}
        for i in vertices:
            neighbors = [j for j in vertices if j != i]
            values[i, neighbors[0]] = sp.Integer(basis_index == 0)
            values[i, neighbors[1]] = sp.Integer(basis_index == 1)
            values[i, neighbors[2]] = sp.cancel(
                -sum(
                    values[i, neighbors[index]]
                    * cofactor(i, neighbors[index])
                    for index in range(2)
                )
                / cofactor(i, neighbors[2])
            )
            assert sp.cancel(
                sum(values[i, j] * cofactor(i, j) for j in neighbors)
            ) == 0
        bases.append(values)

    def second_lift(left, right):
        answer = {}
        for i, k in edges:
            j, ell = [v for v in vertices if v not in (i, k)]
            answer[i, k] = sp.cancel(
                -(left[i, j] * right[k, ell]
                  + left[i, ell] * right[k, j])
                / cofactor(i, k)
            )
        return answer

    blocks = {
        (left, right): second_lift(bases[left], bases[right])
        for left, right in product(range(2), repeat=2)
    }

    def coefficient(coloring):
        return sp.factor(
            sum(
                sp.prod(
                    blocks[coloring[i], coloring[j]][i, j]
                    for i, j in matching
                )
                for matching in matchings
            )
        )

    tensor = {
        coloring: coefficient(coloring)
        for coloring in product(range(2), repeat=4)
    }
    flattening = sp.Matrix(
        [
            [tensor[left + right] for right in product(range(2), repeat=2)]
            for left in product(range(2), repeat=2)
        ]
    )

    c01, c02, c03, c12, c13, c23 = symbols
    hafnian = c01 * c23 + c02 * c13 + c03 * c12
    expected = sp.Matrix(
        (
            (
                hafnian / (c01**2 * c02 * c03),
                hafnian / (c01**2 * c03 * c12),
                hafnian / (c01**2 * c02 * c13),
                hafnian / (c01**2 * c12 * c13),
            ),
            (0, 0, -hafnian / (c01 * c02 * c12 * c13), 0),
            (0, -hafnian / (c01 * c02 * c03 * c12), 0, 0),
            (
                0,
                -hafnian / (c01 * c02 * c12 * c23),
                -hafnian / (c01 * c02 * c12 * c23),
                0,
            ),
        )
    )
    assert all(
        sp.cancel(left - right) == 0
        for left, right in zip(flattening, expected)
    )
    marked_minor = sp.factor(flattening.extract((0, 1, 2), (0, 1, 2)).det())
    assert marked_minor == (
        -hafnian**3 / (c01**4 * c02**3 * c03**2 * c12**2 * c13)
    )


def audit_six_site_cubic_formula() -> int:
    n = 6
    vertices = tuple(range(n))
    edges = tuple(combinations(vertices, 2))
    matchings = tuple(perfect_matchings(vertices))
    full_mask = (1 << n) - 1
    leading = {
        selected_edge: Fraction(-11, 3)
        if selected_edge == (0, 1)
        else Fraction(1)
        for selected_edge in edges
    }

    @cache
    def hafnian(mask):
        if not mask:
            return Fraction(1)
        first_bit = mask & -mask
        i = first_bit.bit_length() - 1
        remainder = mask ^ first_bit
        answer = Fraction(0)
        while remainder:
            next_bit = remainder & -remainder
            j = next_bit.bit_length() - 1
            answer += leading[edge(i, j)] * hafnian(
                mask ^ first_bit ^ next_bit
            )
            remainder ^= next_bit
        return answer

    def cofactor(*deleted):
        mask = full_mask
        for vertex in deleted:
            mask ^= 1 << vertex
        return hafnian(mask)

    def first_jet(offsets):
        p, q = offsets
        values = {
            (i, j): Fraction(0)
            for i in vertices
            for j in vertices
            if i != j
        }
        for i in vertices:
            j = (i + p) % n
            k = (i + q) % n
            values[i, j] = cofactor(i, k)
            values[i, k] = -cofactor(i, j)
        return values

    first = {1: first_jet((1, 2)), 2: first_jet((1, 3))}

    def second_lift(left, right):
        answer = {}
        for i, k in edges:
            numerator = sum(
                left[i, j] * right[k, ell] * cofactor(i, k, j, ell)
                for j in vertices
                if j not in (i, k)
                for ell in vertices
                if ell not in (i, k, j)
            )
            answer[i, k] = -numerator / cofactor(i, k)
        return answer

    second = {
        (left, right): second_lift(first[left], first[right])
        for left, right in product((1, 2), repeat=2)
    }
    cells = {}
    for i, j in edges:
        cells[i, j, 0, 0] = leading[i, j]
        for color in (1, 2):
            cells[i, j, color, 0] = first[color][i, j]
            cells[i, j, 0, color] = first[color][j, i]
        for left, right in product((1, 2), repeat=2):
            cells[i, j, left, right] = second[left, right][i, j]

    def coefficient(coloring):
        return sum(
            reduce(
                lambda value, selected_edge: value
                * cells[
                    selected_edge
                    + (coloring[selected_edge[0]], coloring[selected_edge[1]])
                ],
                matching,
                Fraction(1),
            )
            for matching in matchings
        )

    def cubic_formula(sites, colors):
        i, k, p = sites
        r, s, t = colors
        outside = [vertex for vertex in vertices if vertex not in sites]
        answer = Fraction(0)
        answer += second[r, s][i, k] * sum(
            first[t][p, j] * cofactor(i, k, p, j) for j in outside
        )
        answer += second[r, t][i, p] * sum(
            first[s][k, j] * cofactor(i, k, p, j) for j in outside
        )
        answer += second[s, t][k, p] * sum(
            first[r][i, j] * cofactor(i, k, p, j) for j in outside
        )
        answer += sum(
            first[r][i, j]
            * first[s][k, ell]
            * first[t][p, q]
            * cofactor(i, k, p, j, ell, q)
            for j, ell, q in permutations(outside)
        )
        return answer

    mixed_nonzero = 0
    for sites in combinations(vertices, 3):
        for colors in product((1, 2), repeat=3):
            coloring = [0] * n
            for site, color in zip(sites, colors):
                coloring[site] = color
            direct = coefficient(tuple(coloring))
            formula = cubic_formula(sites, colors)
            assert direct == formula, (sites, colors, direct, formula)
            if 1 in colors and 2 in colors and direct:
                mixed_nonzero += 1
    assert mixed_nonzero > 0
    return mixed_nonzero


def audit_singular_three_face_boundary() -> None:
    vertices = tuple(range(6))
    matchings = tuple(perfect_matchings(vertices))
    factors = (
        {(0, 1), (2, 3), (4, 5)},
        {(0, 5), (1, 2), (3, 4)},
        {(0, 3), (1, 5), (2, 4)},
    )
    edge_color = {
        selected_edge: color
        for color, factor in enumerate(factors)
        for selected_edge in factor
    }

    def coefficient(coloring):
        return sum(
            all(
                coloring[i] == coloring[j] == edge_color[selected_edge]
                for selected_edge in matching
                for i, j in (selected_edge,)
            )
            for matching in matchings
            if all(selected_edge in edge_color for selected_edge in matching)
        )

    for colors in ((0, 1), (0, 2), (1, 2)):
        for coloring in product(colors, repeat=6):
            expected = int(coloring in ((colors[0],) * 6, (colors[1],) * 6))
            assert coefficient(coloring) == expected

    # Relative to the color-zero factor, only its three own pair cofactors
    # are nonzero; the other twelve vanish.
    leading_edges = factors[0]
    pair_cofactors = {}
    for deleted in combinations(vertices, 2):
        remaining = tuple(vertex for vertex in vertices if vertex not in deleted)
        pair_cofactors[deleted] = sum(
            all(selected_edge in leading_edges for selected_edge in matching)
            for matching in perfect_matchings(remaining)
        )
    assert sum(bool(value) for value in pair_cofactors.values()) == 3
    assert sum(not value for value in pair_cofactors.values()) == 12

    mixed_cubics = [
        coloring
        for coloring in product(range(3), repeat=6)
        if sum(color != 0 for color in coloring) == 3
        and 1 in coloring
        and 2 in coloring
    ]
    assert all(coefficient(coloring) == 0 for coloring in mixed_cubics)

    errors = []
    for coloring in product(range(3), repeat=6):
        value = coefficient(coloring)
        target = int(len(set(coloring)) == 1)
        if value != target:
            errors.append((coloring, value))
    assert errors == [((2, 1, 1, 2, 0, 0), 1)]


def main() -> None:
    audit_symbolic_four_site_flattening()
    mixed_nonzero = audit_six_site_cubic_formula()
    audit_singular_three_face_boundary()
    print("symbolic n=4 cofactor-plane flattening minor: nonzero rank >= 3")
    print(f"dense n=6 cubic Bianchi formula: PASS ({mixed_nonzero} mixed residuals)")
    print(
        "singular n=6 boundary: all three binary faces and all mixed cubics "
        "pass; 12 zero cofactors, one degree-4 singleton: PASS"
    )


if __name__ == "__main__":
    main()
