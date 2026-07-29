#!/usr/bin/env python3
"""Exact verifier for the six-site cancellation example in small-tensor-findings.md."""

from itertools import product


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for pos in range(1, len(vertices)):
        second = vertices[pos]
        rest = vertices[1:pos] + vertices[pos + 1 :]
        for matching in perfect_matchings(rest):
            yield ((first, second),) + matching


# Each aggregate edge is a dictionary (color_at_small_endpoint,
# color_at_large_endpoint) -> integer weight.  These are exactly the sums of
# weights of parallel decorated sources with that endpoint-color pair.
edge = {
    (1, 2): {(1, 1): 1, (2, 1): 1},
    (3, 4): {(1, 1): 1},
    (5, 6): {(1, 1): 1},
    (1, 3): {(2, 1): -1},
    (2, 4): {(1, 1): 1},
    (1, 6): {(2, 2): 1},
    (2, 3): {(2, 2): 1},
    (4, 5): {(2, 2): 1},
}


def edge_value(i, j, coloring):
    if i > j:
        i, j = j, i
    return edge.get((i, j), {}).get((coloring[i - 1], coloring[j - 1]), 0)


def coefficient(coloring):
    total = 0
    for matching in perfect_matchings(range(1, 7)):
        term = 1
        for i, j in matching:
            term *= edge_value(i, j, coloring)
        total += term
    return total


for coloring in product((1, 2), repeat=6):
    expected = int(len(set(coloring)) == 1)
    actual = coefficient(coloring)
    assert actual == expected, (coloring, actual, expected)

supported = []
for matching in perfect_matchings(range(1, 7)):
    if all((min(i, j), max(i, j)) in edge for i, j in matching):
        supported.append(tuple(sorted((min(i, j), max(i, j)) for i, j in matching)))

assert supported == [
    ((1, 2), (3, 4), (5, 6)),
    ((1, 3), (2, 4), (5, 6)),
    ((1, 6), (2, 3), (4, 5)),
]

print("verified all 64 coefficients exactly")
print("supported perfect matchings:")
for matching in supported:
    print(matching)
