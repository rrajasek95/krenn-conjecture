#!/usr/bin/env python3
"""Exact two-vertex cap showing sharpness of the radical defect dichotomy.

This is a local boundary model, not an eight-site GHZ realization.  It
constructs genuine aggregate matrices on eight vertices and one entangled
cap K on the last two vertices such that

    K | H_8 = Delta_(6,3),

the direct-edge scalar and all three target cap coefficients are one, and
the effective pair family has tensor Delta_(6,2) on colors 1 and 2.  Thus
the top higher-boundary defect is the *constant* color-0 ray: every mixed
defect component vanishes, but one effective color is lost exactly as the
six-site radical identity predicts.
"""

from __future__ import annotations

import itertools
from fractions import Fraction


Q = 3
U = tuple(range(6))
P, R = 6, 7
ALL = U + (P, R)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for k in range(1, len(vertices)):
        v = vertices[k]
        rest = vertices[1:k] + vertices[k + 1 :]
        for tail in perfect_matchings(rest):
            yield ((u, v),) + tail


def zero_matrix():
    return [[Fraction(0) for _ in range(Q)] for _ in range(Q)]


def add_entry(edges, u, v, a, b, value):
    if u > v:
        u, v, a, b = v, u, b, a
    matrix = edges.setdefault((u, v), zero_matrix())
    matrix[a][b] += Fraction(value)


def coefficient(edges, vertices, coloring):
    color = dict(zip(vertices, coloring))
    total = Fraction(0)
    for matching in perfect_matchings(vertices):
        term = Fraction(1)
        for u, v in matching:
            matrix = edges.get((min(u, v), max(u, v)))
            if matrix is None:
                term = 0
                break
            if u < v:
                term *= matrix[color[u]][color[v]]
            else:
                term *= matrix[color[v]][color[u]]
        total += term
    return total


def tensor(edges, vertices):
    return {
        coloring: value
        for coloring in itertools.product(range(Q), repeat=len(vertices))
        if (value := coefficient(edges, vertices, coloring))
    }


def main():
    edges = {}

    # Unit specialization of the three-colored prism border chart.  The
    # fourth prism matching is 04|15|23 and has coloring 021102.
    matchings = (
        ((0, 4), (1, 2), (3, 5)),
        ((0, 5), (1, 4), (2, 3)),
        ((0, 3), (1, 5), (2, 4)),
    )
    for color, matching in enumerate(matchings):
        for u, v in matching:
            add_entry(edges, u, v, color, color, 1)

    mixed = (0, 2, 1, 1, 0, 2)
    delta3_plus_mixed = {(i,) * 6: Fraction(1) for i in range(Q)}
    delta3_plus_mixed[mixed] = Fraction(1)
    assert tensor(edges, U) == delta3_plus_mixed

    # K=sum_i e_i^* tensor e_i^*.  The direct edge gives s=1 through
    # color 2.  Two diagonal channels of K induce
    #
    #       r_04=-e_0 e_0,    r_12=+e_0 e_0.
    #
    # No other effective edge is induced at this particular cap.
    add_entry(edges, P, R, 2, 2, 1)
    add_entry(edges, 0, P, 0, 0, -1)
    add_entry(edges, 4, R, 0, 0, 1)
    add_entry(edges, 1, P, 0, 1, 1)
    add_entry(edges, 2, R, 0, 1, 1)

    effective = {edge: [row[:] for row in matrix]
                 for edge, matrix in edges.items() if edge[1] < 6}
    add_entry(effective, 0, 4, 0, 0, -1)
    add_entry(effective, 1, 2, 0, 0, 1)

    # The effective family kills the color-0 and fourth-prism matchings,
    # leaving exactly the other two constant rays.
    assert tensor(effective, U) == {
        (1,) * 6: Fraction(1),
        (2,) * 6: Fraction(1),
    }

    # Contract the actual eight-site tensor by K at P,R.  This independently
    # checks the direct term plus the two-cross-edge first derivative.
    capped = {}
    for coloring in itertools.product(range(Q), repeat=6):
        value = sum(
            coefficient(edges, ALL, coloring + (i, i))
            for i in range(Q)
        )
        if value:
            capped[coloring] = value
    assert capped == {(i,) * 6: Fraction(1) for i in range(Q)}

    # Hence E = capped - H_6(effective) is precisely the missing constant
    # color.  In particular E_mixed=0 while s*kappa_0*kappa_1*kappa_2=1.
    defect = dict(capped)
    for coloring, value in tensor(effective, U).items():
        defect[coloring] = defect.get(coloring, 0) - value
        if not defect[coloring]:
            defect.pop(coloring)
    assert defect == {(0,) * 6: Fraction(1)}

    print("verified exact two-vertex cap with s=kappa_0=kappa_1=kappa_2=1")
    print("effective tensor = e_1^6 + e_2^6; defect = e_0^6")
    print("all 726 mixed defect coordinates vanish")


if __name__ == "__main__":
    main()
