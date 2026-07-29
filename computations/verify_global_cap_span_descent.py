#!/usr/bin/env python3
"""Exact audit for ``notes/global-cap-span-descent.md``.

The script enumerates the four-parameter ternary prism family, checks that
its only mixed fiber is the three-spoke word, verifies the unit saturation
by an exact Groebner calculation, and audits the generic pencil root cover.
"""

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


def matching_tensor(vertices, edges, colors=3):
    answer = {}
    position = {vertex: index for index, vertex in enumerate(vertices)}
    for coloring in itertools.product(range(colors), repeat=len(vertices)):
        value = 0
        for matching in perfect_matchings(vertices):
            term = 1
            for u, v in matching:
                if u > v:
                    u, v = v, u
                cell = (coloring[position[u]], coloring[position[v]])
                term *= edges.get((u, v), {}).get(cell, 0)
                if term == 0:
                    break
            value += term
        value = sp.factor(value)
        if value != 0:
            answer[coloring] = value
    return answer


def prism_family(a, z):
    edges = {}
    for color in range(3):
        other = [index for index in range(3) if index != color]
        x_edge = tuple(sorted(other))
        y_edge = tuple(sorted(index + 3 for index in other))
        edges[x_edge] = {(color, color): a}
        edges[y_edge] = {(color, color): a}
        edges[(color, color + 3)] = {(color, color): z[color]}
    return edges


def two_k4_pair_cap_source(direct):
    """Two canonical K4 sources plus an inactive diagonal cap edge.

    Vertex order is p=0, x_i=1+i, q=4, y_i=5+i.
    """

    edges = {
        (0, 4): {
            (row, column): direct[row, column]
            for row, column in itertools.product(range(3), repeat=2)
        }
    }
    for color in range(3):
        other = [index for index in range(3) if index != color]
        edges[(0, 1 + color)] = {(color, color): 1}
        edges[tuple(sorted(1 + index for index in other))] = {
            (color, color): 1
        }
        edges[(4, 5 + color)] = {(color, color): 1}
        edges[tuple(sorted(5 + index for index in other))] = {
            (color, color): 1
        }
    return edges


def diagonal_pair_cap_degree_two(edges, z):
    """Degree-two cofactor family after capping vertices 0 and 4."""

    boundary = (1, 2, 3, 5, 6, 7)
    scalar = sum(
        z[color] * edges[0, 4][color, color] for color in range(3)
    )
    answer = {}
    for u, v in itertools.combinations(boundary, 2):
        matrix = {}
        for color_u, color_v in itertools.product(range(3), repeat=2):
            value = scalar * edges.get(tuple(sorted((u, v))), {}).get(
                (color_u, color_v), 0
            )
            value += sum(
                z[color]
                * (
                    edges.get(tuple(sorted((0, u))), {}).get(
                        (color, color_u), 0
                    )
                    * edges.get(tuple(sorted((4, v))), {}).get(
                        (color, color_v), 0
                    )
                    + edges.get(tuple(sorted((0, v))), {}).get(
                        (color, color_v), 0
                    )
                    * edges.get(tuple(sorted((4, u))), {}).get(
                        (color, color_u), 0
                    )
                )
                for color in range(3)
            )
            value = sp.factor(value)
            if value != 0:
                matrix[color_u, color_v] = value
        if matrix:
            answer[(boundary.index(u), boundary.index(v))] = matrix
    return scalar, answer


def main() -> None:
    a, z0, z1, z2, t, u = sp.symbols("a z0 z1 z2 t u")
    z = (z0, z1, z2)
    tensor = matching_tensor(tuple(range(6)), prism_family(a, z))

    expected = {
        (0,) * 6: a**2 * z0,
        (1,) * 6: a**2 * z1,
        (2,) * 6: a**2 * z2,
        (0, 1, 2, 0, 1, 2): z0 * z1 * z2,
    }
    assert tensor == expected

    mixed_generator = z0 * z1 * z2
    pure_product = sp.prod(expected[(color,) * 6] for color in range(3))
    assert sp.expand(pure_product - a**6 * mixed_generator) == 0

    # J:h^infinity=(1) iff 1 belongs to J+(1-u*h).  Here the exact
    # Groebner basis is [1], certifying that D(h) misses V(J).
    localization = sp.groebner(
        [mixed_generator, 1 - u * pure_product],
        u,
        a,
        z0,
        z1,
        z2,
        order="lex",
        domain=sp.QQ,
    )
    assert localization.contains(sp.S.One)

    pencil_z = (1 + t, 1 + 2 * t, 1 + 3 * t)
    pencil_tensor = matching_tensor(
        tuple(range(6)), prism_family(sp.S.One, pencil_z)
    )
    mixed = sp.Poly(
        pencil_tensor[(0, 1, 2, 0, 1, 2)], t, domain=sp.QQ
    )
    pure = [
        sp.Poly(pencil_tensor[(color,) * 6], t, domain=sp.QQ)
        for color in range(3)
    ]
    assert mixed.monic() == sp.Poly(
        (t + 1) * (t + sp.Rational(1, 2))
        * (t + sp.Rational(1, 3)),
        t,
        domain=sp.QQ,
    ).monic()
    assert sp.factor(sp.prod(polynomial.as_expr() for polynomial in pure)) == (
        (t + 1) * (2 * t + 1) * (3 * t + 1)
    )
    roots = (-1, -sp.Rational(1, 2), -sp.Rational(1, 3))
    for index, root in enumerate(roots):
        assert mixed.eval(root) == 0
        assert pure[index].eval(root) == 0
        assert all(
            pure[other].eval(root) != 0
            for other in range(3)
            if other != index
        )

    # The same family is the literal degree-two cofactor map of two
    # canonical K4 sources joined by an inactive diagonal cap edge.
    direct = sp.Matrix([[1, 2, 3], [4, 5, 7], [8, 11, 13]])
    source_edges = two_k4_pair_cap_source(direct)
    source_tensor = matching_tensor(tuple(range(8)), source_edges)
    actual_top = {}
    for left_color, right_color in itertools.product(range(3), repeat=2):
        coloring = (
            (left_color,) * 4 + (right_color,) * 4
        )
        actual_top[coloring] = sp.S.One
    assert source_tensor == actual_top

    scalar, capped_family = diagonal_pair_cap_degree_two(source_edges, z)
    assert scalar == z0 + 5 * z1 + 13 * z2
    assert capped_family == prism_family(scalar, z)
    capped_tensor = matching_tensor(tuple(range(6)), capped_family)
    assert capped_tensor == {
        (0,) * 6: scalar**2 * z0,
        (1,) * 6: scalar**2 * z1,
        (2,) * 6: scalar**2 * z2,
        (0, 1, 2, 0, 1, 2): z0 * z1 * z2,
    }

    formal_top = {
        (color,) * 8: sp.S.One for color in range(3)
    }
    for cap_left, cap_right in itertools.product(range(3), repeat=2):
        contracted = {}
        for coloring, value in formal_top.items():
            if coloring[0] == cap_left and coloring[4] == cap_right:
                boundary_coloring = coloring[1:4] + coloring[5:8]
                contracted[boundary_coloring] = (
                    contracted.get(boundary_coloring, 0) + value
                )
        expected_contraction = {}
        if cap_left == cap_right:
            expected_contraction[(cap_left,) * 6] = sp.S.One
        assert contracted == expected_contraction

    print("four-parameter ternary prism identity: PASS")
    print("unit saturation and three-root pure cover: PASS")
    print("actual cofactor map plus all formal GHZ cap identities: PASS")


if __name__ == "__main__":
    main()
