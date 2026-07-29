#!/usr/bin/env python3
"""Exact audits for notes/global-covariance-nonsingularity-boundary.md.

The point is to distinguish the still-plausible ternary statement from its
false palette-uniform and binary-face analogues.  All ranks and determinants
are computed over Q by SymPy.
"""

from __future__ import annotations

import itertools
from fractions import Fraction
from functools import reduce

import sympy as sp

import verify_cofactor_open_color_cloning as clone


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position, second in enumerate(vertices[1:], 1):
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


def entry(cells, u, v, a, b):
    if u < v:
        return cells.get((u, v, a, b), 0)
    return cells.get((v, u, b, a), 0)


def tensor(n, q, cells):
    answer = {}
    matchings = tuple(perfect_matchings(range(n)))
    for coloring in itertools.product(range(q), repeat=n):
        value = sum(
            reduce(
                lambda total, edge: total
                * entry(cells, *edge, coloring[edge[0]], coloring[edge[1]]),
                matching,
                Fraction(1),
            )
            for matching in matchings
        )
        if value:
            answer[coloring] = value
    return answer


def covariance(n, q, cells):
    matrix = sp.zeros(n * q)
    for u, v in itertools.combinations(range(n), 2):
        block = sp.Matrix(
            q,
            q,
            lambda a, b: sp.Rational(entry(cells, u, v, a, b)),
        )
        matrix[q * u : q * (u + 1), q * v : q * (v + 1)] = block
        matrix[q * v : q * (v + 1), q * u : q * (u + 1)] = block.T
    return matrix


def binary_singular_k4():
    # The two color-zero matchings each have product 1/2.  Their unsigned
    # sum is one, while the two rows of the corresponding bipartite block
    # are proportional, making the covariance singular.
    cells = {}
    for edge, value in (
        ((0, 1), 1),
        ((2, 3), Fraction(1, 2)),
        ((0, 2), 1),
        ((1, 3), Fraction(1, 2)),
    ):
        cells[edge + (0, 0)] = value
    for edge in ((0, 3), (1, 2)):
        cells[edge + (1, 1)] = 1
    return cells


def standard_ternary_k4():
    cells = {}
    factors = (
        ((0, 1), (2, 3)),
        ((0, 2), (1, 3)),
        ((0, 3), (1, 2)),
    )
    for color, matching in enumerate(factors):
        for edge in matching:
            cells[edge + (color, color)] = 1
    return cells


def cloned_cofactor_open_k4():
    base = clone.binary_cells()
    scales = (Fraction(1), Fraction(1), Fraction(-1), Fraction(-1))
    return clone.cloned_cells(base, scales)


def three_binary_faces_k6():
    # Rational reweighting of Proposition 3.1 in
    # binary-norm-equality-counterfamily.md.  Each color is an isolated edge
    # plus a four-cycle whose two perfect-matching products are both 1/2.
    families = (
        (((0, 1),), (((2, 3), (4, 5)), ((2, 4), (3, 5)))),
        (((3, 4),), (((0, 2), (1, 5)), ((0, 5), (1, 2)))),
        (((2, 5),), (((0, 3), (1, 4)), ((0, 4), (1, 3)))),
    )
    cells = {}
    for color, (shared, alternatives) in enumerate(families):
        cells[shared[0] + (color, color)] = Fraction(1)
        for first, second in alternatives:
            cells[first + (color, color)] = Fraction(1)
            cells[second + (color, color)] = Fraction(1, 2)
    return cells


def exceptional_rainbow_k6():
    cells = {}
    factors = (
        ((0, 1), (2, 3), (4, 5)),
        ((1, 2), (3, 4), (0, 5)),
        ((0, 3), (1, 5), (2, 4)),
    )
    for color, matching in enumerate(factors):
        for u, v in matching:
            u, v = sorted((u, v))
            cells[u, v, color, color] = 1
    return cells


def prism_border_k6(t=Fraction(2)):
    cells = {}
    rows = (
        (((0, 4), 1), ((1, 2), t), ((3, 5), 1 / t)),
        (((0, 5), 1 / t), ((1, 4), 1 / t), ((2, 3), t * t)),
        (((0, 3), t), ((1, 5), 1), ((2, 4), 1 / t)),
    )
    for color, row in enumerate(rows):
        for edge, value in row:
            cells[edge + (color, color)] = value
    return cells


def assert_binary_face(full_tensor, colors, n):
    face = {
        coloring: value
        for coloring, value in full_tensor.items()
        if set(coloring) <= set(colors)
    }
    assert face == {(colors[0],) * n: 1, (colors[1],) * n: 1}


def main():
    binary = binary_singular_k4()
    assert tensor(4, 2, binary) == {(0,) * 4: 1, (1,) * 4: 1}
    z_binary = covariance(4, 2, binary)
    assert z_binary.rank() == 6 and z_binary.det() == 0
    assert len(z_binary.nullspace()) == 2

    standard = standard_ternary_k4()
    assert tensor(4, 3, standard) == {(c,) * 4: 1 for c in range(3)}
    z_standard = covariance(4, 3, standard)
    assert z_standard.rank() == 12 and z_standard.det() == 1

    cloned = cloned_cofactor_open_k4()
    cloned_tensor = tensor(4, 3, cloned)
    assert all(
        cloned_tensor.get(coloring, 0)
        == int(coloring in ((0,) * 4, (color,) * 4))
        for color in (1, 2)
        for coloring in itertools.product((0, color), repeat=4)
    )
    assert all(
        cloned_tensor.get(coloring, 0) == 0
        for coloring in itertools.product(range(3), repeat=4)
        if 0 in coloring and len(set(coloring)) > 1
    )
    z_cloned = covariance(4, 3, cloned)
    assert z_cloned.rank() == 8 and z_cloned.det() == 0

    three_faces = three_binary_faces_k6()
    three_face_tensor = tensor(6, 3, three_faces)
    for colors in itertools.combinations(range(3), 2):
        assert_binary_face(three_face_tensor, colors, 6)
    mixed = {
        coloring: value
        for coloring, value in three_face_tensor.items()
        if len(set(coloring)) == 3
    }
    assert len(mixed) == 9 and all(value != 0 for value in mixed.values())
    z_three_faces = covariance(6, 3, three_faces)
    assert z_three_faces.rank() == 12 and z_three_faces.det() == 0

    rainbow = exceptional_rainbow_k6()
    rainbow_tensor = tensor(6, 3, rainbow)
    assert rainbow_tensor == {
        (0,) * 6: 1,
        (1,) * 6: 1,
        (2,) * 6: 1,
        (2, 1, 1, 2, 0, 0): 1,
    }
    z_rainbow = covariance(6, 3, rainbow)
    assert z_rainbow.rank() == 18 and z_rainbow.det() == -1

    prism = prism_border_k6()
    prism_tensor = tensor(6, 3, prism)
    assert prism_tensor == {
        (0,) * 6: 1,
        (1,) * 6: 1,
        (2,) * 6: 1,
        (0, 2, 1, 1, 0, 2): 4,
    }
    z_prism = covariance(6, 3, prism)
    assert z_prism.rank() == 18 and z_prism.det() == -1

    print("exact binary GHZ K4: rank(Z)=6/8, nullity=2")
    print("standard exact ternary K4: det(Z)=1")
    print("cofactor-open two-face clone: rank(Z)=8/12")
    print("all-three-binary-face K6 boundary: rank(Z)=12/18")
    print("rainbow and prism near-target K6 models: det(Z)=-1")
    print("global covariance boundary audit: PASS")


if __name__ == "__main__":
    main()
