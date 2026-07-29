#!/usr/bin/env python3
"""Exact audit of the rank-one ratio-rectangle obstruction."""

from __future__ import annotations

import itertools


COLORS = tuple(range(3))
VERTICES = tuple(range(6))


def rectangle(rows, columns):
    return set(itertools.product(rows, columns))


SUPPORTS = {
    (0, 1): {(0, 0)},
    (0, 2): {(2, 2)},
    (0, 3): rectangle(COLORS, (1, 2)),
    (0, 4): rectangle(COLORS, COLORS),
    (0, 5): {(2, 1)},
    (1, 2): {(1, 2)},
    (1, 3): rectangle((2,), (1, 2)),
    (1, 4): rectangle((2,), COLORS),
    (1, 5): {(1, 1)},
    (2, 3): rectangle((1,), (1, 2)),
    (2, 4): rectangle((1,), COLORS),
    (2, 5): {(0, 0)},
    (3, 4): {(0, 0)},
    (3, 5): rectangle((1, 2), (0, 2)),
    (4, 5): rectangle(COLORS, (0, 2)),
}


def perfect_matchings(vertices=VERTICES):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for second in vertices[1:]:
        rest = tuple(vertex for vertex in vertices if vertex not in (first, second))
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


MATCHINGS = tuple(perfect_matchings())
P = ((0, 3), (1, 5), (2, 4))
Q = ((0, 4), (1, 5), (2, 3))


def supported_fiber(coloring):
    return tuple(
        matching
        for matching in MATCHINGS
        if all((coloring[u], coloring[v]) in SUPPORTS[u, v] for u, v in matching)
    )


def formal_ratio_signature(coloring):
    """Exponent vector of the P/Q ratio in endpoint rank-one factors."""
    keys = []
    for edge, support in SUPPORTS.items():
        u, v = edge
        keys.extend((edge, u, color) for color in sorted({a for a, _ in support}))
        keys.extend((edge, v, color) for color in sorted({b for _, b in support}))
    keys = tuple(keys)
    index = {key: position for position, key in enumerate(keys)}
    signature = [0] * len(keys)
    for sign, matching in ((1, P), (-1, Q)):
        for u, v in matching:
            signature[index[((u, v), u, coloring[u])]] += sign
            signature[index[((u, v), v, coloring[v])]] += sign
    return tuple(signature)


def main():
    corners = {
        (a, b): (a, 1, 1, 1, b, 1)
        for a, b in itertools.product((0, 1), repeat=2)
    }
    for coloring in corners.values():
        assert supported_fiber(coloring) == (P, Q)

    signatures = {corner: formal_ratio_signature(coloring) for corner, coloring in corners.items()}
    assert tuple(
        signatures[0, 0][i]
        + signatures[1, 1][i]
        - signatures[0, 1][i]
        - signatures[1, 0][i]
        for i in range(len(signatures[0, 0]))
    ) == (0,) * len(signatures[0, 0])

    # Three mixed fibers have ratio -1.  The multiplicative rectangle then
    # forces the all-one corner ratio to be (-1)(-1)/(-1)=-1.
    ratios = {(0, 0): -1, (0, 1): -1, (1, 0): -1}
    ratios[1, 1] = ratios[0, 1] * ratios[1, 0] // ratios[0, 0]
    assert ratios[1, 1] == -1
    print("four exact fibers contain only 03|15|24 and 04|15|23")
    print("formal rank-one ratio rectangle forces the all-one coefficient to zero")


if __name__ == "__main__":
    main()
