#!/usr/bin/env python3
"""Lightweight exact check of the six-site pure-binary common-power guard."""

from itertools import product
from math import prod


SITES = tuple(range(6))
COLORS = tuple(range(3))

# Keys are (smaller endpoint, larger endpoint, common endpoint colour).
R = {
    (0, 1, 0): 1,
    (2, 3, 0): 1,
    (4, 5, 0): 1,
    (1, 2, 1): 1,
    (3, 4, 1): 1,
    (0, 5, 1): 1,
    (0, 2, 2): 1,
}

Q = {
    (2, 3, 0): 1,
    (4, 5, 0): 1,
    (3, 4, 1): -1,
    (0, 5, 1): -1,
    (1, 4, 2): 1,
    (3, 5, 2): 1,
}


def perfect_matchings(vertices):
    """Generate each unordered perfect matching exactly once."""
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    x = vertices[0]
    for offset, y in enumerate(vertices[1:], start=1):
        remainder = vertices[1:offset] + vertices[offset + 1 :]
        for matching in perfect_matchings(remainder):
            yield ((x, y),) + matching


MATCHINGS = tuple(perfect_matchings(SITES))


def edge(table, x, y, color):
    return table.get((min(x, y), max(x, y), color), 0)


def cube_coefficient(table, word):
    """Coefficient of ``word`` in the third divided matching power."""
    return sum(
        prod(
            edge(table, x, y, word[x]) if word[x] == word[y] else 0
            for x, y in matching
        )
        for matching in MATCHINGS
    )


def tangent_coefficient(response, common, word):
    """Coefficient of ``word`` in response * common^[2]."""
    total = 0
    for matching in MATCHINGS:
        for response_index, (x, y) in enumerate(matching):
            if word[x] != word[y]:
                continue
            term = edge(response, x, y, word[x])
            for common_index, (u, v) in enumerate(matching):
                if common_index == response_index:
                    continue
                term *= edge(common, u, v, word[u]) if word[u] == word[v] else 0
            total += term
    return total


def main():
    nonzero_cube = {}
    nonzero_tangent = {}
    for word in product(COLORS, repeat=len(SITES)):
        cube = cube_coefficient(R, word)
        tangent = tangent_coefficient(R, Q, word)
        if cube:
            nonzero_cube[word] = cube
        if tangent:
            nonzero_tangent[word] = tangent

    expected_cube = {(color,) * 6: 1 for color in (0, 1)}
    expected_tangent = {(color,) * 6: 1 for color in COLORS}
    assert nonzero_cube == expected_cube
    assert nonzero_tangent == expected_tangent

    # The six alternating cycle cells give an invertible even/odd shore
    # matrix.  The colour-two port (site 0, colour 2) is dark against the
    # entire odd-shore basis but has a unit edge to (site 2, colour 2).
    cycle_edges = set(R) - {(0, 2, 2)}
    assert len(cycle_edges) == 6
    assert R[(0, 2, 2)] == 1
    assert all(
        (min(0, odd), max(0, odd), 2) not in R for odd in (1, 3, 5)
    )

    print("curved pure-binary common-power guard: PASS")


if __name__ == "__main__":
    main()
