#!/usr/bin/env python3
"""Verify the sharp K8 countermodel to color-stabilizer matroid closure."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from itertools import combinations, product


VERTICES = tuple(range(8))
COLORS = tuple(range(3))
EDGES = tuple(combinations(VERTICES, 2))

MATCHINGS = {
    0: ((0, 1), (2, 3), (4, 5), (6, 7)),
    1: ((0, 2), (1, 3), (4, 6), (5, 7)),
    2: ((0, 3), (1, 2), (4, 7), (5, 6)),
}

SIGMA = {
    0: (1, -1, 1),
    1: (1, -1, 1),
    2: (1, 1, -1),
    3: (-1, 1, -1),
    4: (1, -1, 1),
    5: (-1, 1, 1),
    6: (1, 1, -1),
    7: (-1, 1, 1),
}

def build_supports():
    supports = {}
    for color, matching in MATCHINGS.items():
        for edge in matching:
            assert edge not in supports
            supports[edge] = ((color, color),)
    for edge in EDGES:
        if edge in supports:
            continue
        u, v = edge
        plus_u = tuple(r for r in COLORS if SIGMA[u][r] == 1)
        minus_v = tuple(r for r in COLORS if SIGMA[v][r] == -1)
        supports[edge] = tuple(product(plus_u, minus_v))
    assert set(supports) == set(EDGES)
    return supports


def port_row(edge, cell):
    row = [0] * 24
    (u, v), (i, j) = edge, cell
    row[3 * u + i] += 1
    row[3 * v + j] += 1
    return tuple(row)


def color_sum_row(color):
    return tuple(int(index % 3 == color) for index in range(24))


def add_rows(rows):
    rows = tuple(rows)
    return tuple(sum(row[index] for row in rows) for index in range(24))


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for index in range(1, len(vertices)):
        v = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        for matching in perfect_matchings(rest):
            yield ((min(u, v), max(u, v)),) + matching


def decorated_colorings(matching, supports):
    for chosen_cells in product(*(supports[edge] for edge in matching)):
        coloring = {}
        for edge, cell in zip(matching, chosen_cells):
            u, v = edge
            i, j = cell
            coloring[u] = i
            coloring[v] = j
        yield tuple(coloring[v] for v in sorted(coloring))


def main():
    supports = build_supports()

    # The three perfect-matching flow identities sum exactly to the three
    # affine color-sum rows.  They prove the universal lower bound of three.
    flat_matchings = [edge for matching in MATCHINGS.values() for edge in matching]
    assert len(set(flat_matchings)) == 12
    for color, matching in MATCHINGS.items():
        assert sorted(sum(([u, v] for u, v in matching), [])) == list(VERTICES)
        lhs = add_rows(port_row(edge, supports[edge][0]) for edge in matching)
        assert lhs == color_sum_row(color)

    # Every vertex/color has a same-color coordinate rank-one anchor.
    for vertex in VERTICES:
        for color in COLORS:
            incident = [edge for edge in MATCHINGS[color] if vertex in edge]
            assert len(incident) == 1
            assert supports[incident[0]] == ((color, color),)

    # Every nonmatching edge has a Cartesian support, hence is rank one,
    # and at least one of its two factors is generally noncoordinate.
    matching_edges = set(flat_matchings)
    asymmetric = 0
    for edge in EDGES:
        left = {i for i, _ in supports[edge]}
        right = {j for _, j in supports[edge]}
        assert set(supports[edge]) == set(product(left, right))
        if edge not in matching_edges and (len(left) > 1 or len(right) > 1):
            asymmetric += 1
    assert asymmetric >= 12

    # The displayed affine point has all target color sums equal to one.
    alpha = {
        (vertex, color): Fraction(SIGMA[vertex][color], 2)
        for vertex in VERTICES
        for color in COLORS
    }
    for color in COLORS:
        assert sum(alpha[vertex, color] for vertex in VERTICES) == 1
    assert all({SIGMA[v][r] for r in COLORS} == {-1, 1} for v in VERTICES)

    survivors = []
    for edge in EDGES:
        u, v = edge
        multipliers = {
            alpha[u, i] + alpha[v, j] for i, j in supports[edge]
        }
        if multipliers != {0}:
            survivors.append((edge, multipliers))
    assert survivors == [((0, 1), {1}), ((4, 7), {1}), ((5, 7), {1})]

    # With coefficient one, every complementary tensor is nonzero.  We audit
    # this directly by counting its decorated perfect-matching monomials.
    cofactor_support_sizes = {}
    for removed_edge in EDGES:
        remaining = tuple(v for v in VERTICES if v not in removed_edge)
        coefficients = Counter()
        for matching in perfect_matchings(remaining):
            coefficients.update(decorated_colorings(matching, supports))
        assert coefficients
        assert all(value > 0 for value in coefficients.values())
        cofactor_support_sizes[removed_edge] = len(coefficients)

    # K8 has no nontrivial tight odd cut: explicitly find a perfect matching
    # crossing each 3- or 5-shore at least three times.
    for shore_size in (3, 5):
        for shore in combinations(VERTICES, shore_size):
            shore = set(shore)
            crossing_counts = [
                sum((u in shore) != (v in shore) for u, v in matching)
                for matching in perfect_matchings(VERTICES)
            ]
            assert max(crossing_counts) >= 3

    assert all(sum(vertex in edge for edge in EDGES) == 7 for vertex in VERTICES)
    print(
        "verified sharp K8 color-stabilizer countermodel: "
        f"28 active rank-one edges ({asymmetric} asymmetric), "
        "universal minimum >=3, witness minimum =3"
    )
    print(
        "cofactor decorated-support sizes:",
        sorted(Counter(cofactor_support_sizes.values()).items()),
    )


if __name__ == "__main__":
    main()
