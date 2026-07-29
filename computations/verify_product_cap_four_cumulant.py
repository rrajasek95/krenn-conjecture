#!/usr/bin/env python3
"""Exact product-cap obstruction to replacing an internal gadget by pairs.

There are boundary vertices 0,1,2,3 and capped vertices x,y.  The internal
edge xy has scalar weight one.  Vertices 0,2 connect to x, and 1,3 connect
to y, all by the same one-dimensional basis tensor.  After the product cap,
the scalar boundary signature is one and its two-boundary entries are

    C_01 = C_03 = C_12 = C_23 = 1.

Its four-boundary entry is zero because two internal vertices cannot absorb
four boundary vertices.  Pair edges fixed by the two-boundary data instead
have four-boundary hafnian 2.  Equivalently the degree-four logarithmic
cumulant is -2.  Everything is integer and dependency-free.
"""

from __future__ import annotations

from itertools import combinations


BOUNDARY = (0, 1, 2, 3)
X, Y = 4, 5
EDGES = frozenset({(0, X), (2, X), (1, Y), (3, Y), (X, Y)})


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for position, v in enumerate(vertices[1:], 1):
        edge = tuple(sorted((u, v)))
        if edge not in EDGES:
            continue
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield (edge,) + tail


def boundary_value(subset: tuple[int, ...]) -> int:
    # Boundary sites have no mutual edges in the capped gadget, so its
    # signature is simply the matching count on subset union {x,y}.
    return sum(1 for _ in perfect_matchings(tuple(sorted(subset + (X, Y)))))


def main() -> None:
    assert boundary_value(()) == 1
    pair_values = {
        pair: boundary_value(pair) for pair in combinations(BOUNDARY, 2)
    }
    assert pair_values == {
        (0, 1): 1,
        (0, 2): 0,
        (0, 3): 1,
        (1, 2): 1,
        (1, 3): 0,
        (2, 3): 1,
    }
    assert boundary_value(BOUNDARY) == 0

    # The unique pair-only replacement that preserves the degree-two
    # signature has the following forced four-site coefficient.
    pair_hafnian = (
        pair_values[0, 1] * pair_values[2, 3]
        + pair_values[0, 2] * pair_values[1, 3]
        + pair_values[0, 3] * pair_values[1, 2]
    )
    assert pair_hafnian == 2

    # log(1+C_2) has degree-four term -C_2^2/2.  On all four sites,
    # C_2^2/2 is precisely the pair hafnian above.
    four_cumulant = -pair_hafnian
    assert four_cumulant == -2
    print(
        "verified product cap: C_0123=0, forced pair hafnian=2, "
        "four-cumulant=-2"
    )


if __name__ == "__main__":
    main()
