#!/usr/bin/env python3
"""Exact checker for z*q^3/3! = Delta_(8,3).

The quadratic q and the distinguished quadratic z have only unit
same-colour cells.  The checker enumerates all 105 underlying perfect
matchings and every possible choice of the distinguished z edge, retaining
parallel colour cells on a common underlying pair literally.
"""

from __future__ import annotations

from collections import Counter
from itertools import product


VERTICES = tuple(range(8))

PURE_MATCHINGS = (
    ((0, 1), (2, 3), (4, 5), (6, 7)),
    ((0, 1), (2, 4), (3, 6), (5, 7)),
    ((0, 2), (1, 4), (3, 7), (5, 6)),
)
DISTINGUISHED = ((0, 1), (2, 4), (3, 7))


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        remaining = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(remaining):
            yield ((first, second),) + tail


def build_cells():
    q_cells = {}
    z_cells = {}
    for colour, matching in enumerate(PURE_MATCHINGS):
        distinguished = DISTINGUISHED[colour]
        for edge in matching:
            edge = tuple(sorted(edge))
            target = z_cells if edge == distinguished else q_cells
            target.setdefault(edge, []).append(colour)
    return q_cells, z_cells


def expand_polarized_tensor(q_cells, z_cells):
    coefficients = Counter()
    witnesses = []
    underlying = tuple(perfect_matchings(VERTICES))
    assert len(underlying) == 105

    for matching in underlying:
        for distinguished_edge in matching:
            edge = tuple(sorted(distinguished_edge))
            for z_colour in z_cells.get(edge, ()):
                q_edges = [other for other in matching if other != distinguished_edge]
                colour_options = [q_cells.get(tuple(sorted(other)), ()) for other in q_edges]
                for q_colours in product(*colour_options):
                    word = [None] * len(VERTICES)
                    u, v = distinguished_edge
                    word[u] = word[v] = z_colour
                    for (a, b), colour in zip(q_edges, q_colours):
                        word[a] = word[b] = colour
                    assert all(value is not None for value in word)
                    word = tuple(word)
                    coefficients[word] += 1
                    witnesses.append((word, matching, distinguished_edge, z_colour, q_colours))
    return coefficients, witnesses


def main():
    q_cells, z_cells = build_cells()
    assert sum(map(len, q_cells.values())) == 9
    assert sum(map(len, z_cells.values())) == 3
    # The pair 01 deliberately carries a q-cell of colour 1 and a z-cell of
    # colour 0.  They are distinct endpoint-colour cells, not combined.
    assert q_cells[(0, 1)] == [1]
    assert z_cells[(0, 1)] == [0]

    # This model cannot secretly have the pair-cap form z=a*q+4*p*s.  On
    # row modes (0,0),(2,1),(3,2) and column modes (1,0),(4,1),(7,2), the
    # cross matrix of z-a*q is I_3 for every a: the three diagonal entries
    # are precisely the distinguished z cells and every selected q entry is
    # absent.  A product p*s has cross matrix P*S^T+S*P^T, of rank at most 2.
    row_modes = ((0, 0), (2, 1), (3, 2))
    column_modes = ((1, 0), (4, 1), (7, 2))
    selected = []
    for row_site, row_colour in row_modes:
        row = []
        for column_site, column_colour in column_modes:
            edge = tuple(sorted((row_site, column_site)))
            z_value = int(row_colour == column_colour and row_colour in z_cells.get(edge, ()))
            q_value = int(row_colour == column_colour and row_colour in q_cells.get(edge, ()))
            row.append((z_value, q_value))
        selected.append(tuple(row))
    assert selected == [
        ((1, 0), (0, 0), (0, 0)),
        ((0, 0), (1, 0), (0, 0)),
        ((0, 0), (0, 0), (1, 0)),
    ]

    coefficients, witnesses = expand_polarized_tensor(q_cells, z_cells)
    expected = {tuple([colour] * 8): 1 for colour in range(3)}
    assert dict(coefficients) == expected
    assert len(witnesses) == 3
    for colour, witness in enumerate(witnesses):
        word, matching, distinguished_edge, z_colour, q_colours = witness
        assert word == tuple([colour] * 8)
        assert matching == PURE_MATCHINGS[colour]
        assert distinguished_edge == DISTINGUISHED[colour]
        assert z_colour == colour
        assert q_colours == (colour, colour, colour)

    # Directly audit the stronger deletion statement: after choosing z_r,
    # its six remaining sites have exactly one decorated q-perfect matching.
    for colour, edge in enumerate(DISTINGUISHED):
        remaining = tuple(vertex for vertex in VERTICES if vertex not in edge)
        decorated = 0
        underlying = 0
        for matching in perfect_matchings(remaining):
            multiplicity = 1
            for q_edge in matching:
                multiplicity *= len(q_cells.get(tuple(sorted(q_edge)), ()))
            if multiplicity:
                underlying += 1
                decorated += multiplicity
                assert set(matching) == set(PURE_MATCHINGS[colour]) - {edge}
        assert underlying == decorated == 1

    print("polarized eight-site unrestricted counterexample: PASS")
    print("105 matchings and all distinguished-edge choices: PASS")
    print("9 q-cells, 3 z-cells, exactly three supported terms: PASS")
    print("z*q^3/3! = Delta_(8,3) over Z: PASS")
    print("rank-3 cross minor excludes z=a*q+4*p*s for every a: PASS")


if __name__ == "__main__":
    main()
