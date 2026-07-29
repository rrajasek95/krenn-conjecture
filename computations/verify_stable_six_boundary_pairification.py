#!/usr/bin/env python3
"""Exact audit for ``notes/stable-six-boundary-pairification.md``.

The first part treats a completely generic scalar six-boundary signature
and verifies, in the square-free subset algebra, that three dilated copies
with elementary symmetric data

    e1 = 1, e2 = 1/2, e3 = 1/6

have product ``s^3 exp(F2/s)``.  These are the Vieta data of the roots of
``z^3-z^2+z/2-1/6``.

The second part independently enumerates the rational binary eight-site
source.  Product caps at pairs 23 and 16 both have scalar one and top tensor
Delta_(6,2), while the hafnians of their degree-two boundary components are
Delta_(6,2) and Delta_(6,2)-2 e_001000, respectively.
"""

from __future__ import annotations

import itertools
import sys
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from verify_n8_pair_cap_obstruction import (  # noqa: E402
    VERTICES,
    edge_entry,
    matching_tensor,
    source,
)


def squarefree_product(left, right):
    answer = {}
    for support_left, value_left in left.items():
        for support_right, value_right in right.items():
            if support_left & support_right:
                continue
            support = support_left | support_right
            answer[support] = answer.get(support, 0) + value_left * value_right
    return answer


def dilate(signature, z):
    return {
        support: z ** (len(support) // 2) * value
        for support, value in signature.items()
    }


def audit_generic_pairification() -> None:
    vertices = tuple(range(6))
    scalar = sp.symbols("s", nonzero=True)
    signature = {frozenset(): scalar}
    for size in (2, 4, 6):
        for support in itertools.combinations(vertices, size):
            name = "f" + "".join(map(str, support))
            signature[frozenset(support)] = sp.symbols(name)

    z = sp.symbols("z1:4")
    product = {frozenset(): sp.S.One}
    for parameter in z:
        product = squarefree_product(product, dilate(signature, parameter))

    degree_two = {
        support: value
        for support, value in signature.items()
        if len(support) == 2
    }
    degree_two_squared = squarefree_product(degree_two, degree_two)
    degree_two_cubed = squarefree_product(degree_two_squared, degree_two)

    expected = {frozenset(): scalar**3}
    expected.update(
        {support: scalar**2 * value for support, value in degree_two.items()}
    )
    expected.update(
        {
            support: scalar * value / 2
            for support, value in degree_two_squared.items()
        }
    )
    expected.update(
        {support: value / 6 for support, value in degree_two_cubed.items()}
    )

    # Every component is symmetric in z1,z2,z3.  Rewrite it in the three
    # elementary symmetric polynomials and substitute the Vieta data of
    # z^3-z^2+z/2-1/6.
    for support in set(product) | set(expected):
        difference = sp.expand(product.get(support, 0) - expected.get(support, 0))
        symmetric, remainder, mapping = sp.symmetrize(difference, z, formal=True)
        assert remainder == 0
        elementary = [formal for formal, _actual in mapping]
        reduced = sp.factor(
            symmetric.subs(
                {
                    elementary[0]: sp.S.One,
                    elementary[1]: sp.Rational(1, 2),
                    elementary[2]: sp.Rational(1, 6),
                }
            )
        )
        assert reduced == 0

    # Newton sums at the Vieta data of the cubic.
    assert 1**2 - 2 * sp.Rational(1, 2) == 0
    assert (
        1**3
        - 3 * 1 * sp.Rational(1, 2)
        + 3 * sp.Rational(1, 6)
        == 0
    )


def product_pair_boundary(edges, p, q):
    """Return scalar, boundary order, and F_2 for cap epsilon_p epsilon_q."""

    colors = range(2)
    boundary = tuple(vertex for vertex in VERTICES if vertex not in (p, q))
    scalar = sp.factor(
        sum(edge_entry(edges, p, q, i, j) for i in colors for j in colors)
    )

    # The degree-two boundary component has either one internal pq edge and
    # one old boundary edge, or the two cross edges from p,q to the named
    # boundary pair.
    degree_two = {}
    for a, b in itertools.combinations(boundary, 2):
        matrix = {}
        for color_a, color_b in itertools.product(colors, repeat=2):
            value = scalar * edge_entry(edges, a, b, color_a, color_b)
            value += sum(
                edge_entry(edges, p, a, i, color_a)
                * edge_entry(edges, q, b, j, color_b)
                + edge_entry(edges, p, b, i, color_b)
                * edge_entry(edges, q, a, j, color_a)
                for i, j in itertools.product(colors, repeat=2)
            )
            value = sp.factor(value)
            if value != 0:
                matrix[color_a, color_b] = value
        if matrix:
            degree_two[a, b] = matrix
    return scalar, boundary, degree_two


def cap_top(tensor, vertices, p, q):
    boundary = tuple(vertex for vertex in vertices if vertex not in (p, q))
    positions = {vertex: index for index, vertex in enumerate(vertices)}
    answer = {}
    for coloring in itertools.product(range(2), repeat=len(boundary)):
        boundary_colors = dict(zip(boundary, coloring, strict=True))
        value = sp.S.Zero
        for color_p, color_q in itertools.product(range(2), repeat=2):
            full = []
            for vertex in vertices:
                if vertex == p:
                    full.append(color_p)
                elif vertex == q:
                    full.append(color_q)
                else:
                    full.append(boundary_colors[vertex])
            value += tensor.get(tuple(full), 0)
        value = sp.factor(value)
        if value != 0:
            answer[coloring] = value
    assert positions  # also audits that the named vertex order is explicit
    return boundary, answer


def audit_equal_top_separation() -> None:
    edges = source()
    full = matching_tensor(VERTICES, edges)
    assert full == {(0,) * 8: sp.S.One, (1,) * 8: sp.S.One}

    records = {}
    for pair in ((2, 3), (1, 6)):
        scalar, boundary, degree_two = product_pair_boundary(edges, *pair)
        capped_boundary, top = cap_top(full, VERTICES, *pair)
        assert boundary == capped_boundary
        assert scalar == 1
        assert top == {(0,) * 6: sp.S.One, (1,) * 6: sp.S.One}
        records[pair] = (boundary, degree_two, matching_tensor(boundary, degree_two))

    clean_boundary, _clean_f2, clean_top = records[2, 3]
    assert clean_boundary == (1, 4, 5, 6, 7, 8)
    assert clean_top == {(0,) * 6: sp.S.One, (1,) * 6: sp.S.One}

    dirty_boundary, _dirty_f2, dirty_top = records[1, 6]
    assert dirty_boundary == (2, 3, 4, 5, 7, 8)
    assert dirty_top == {
        (0,) * 6: sp.S.One,
        (0, 0, 1, 0, 0, 0): -sp.Integer(2),
        (1,) * 6: sp.S.One,
    }


def main() -> None:
    audit_generic_pairification()
    print("generic three-copy boundary pairification: PASS")
    audit_equal_top_separation()
    print("equal-scalar/equal-top exact binary separation: PASS")


if __name__ == "__main__":
    main()
