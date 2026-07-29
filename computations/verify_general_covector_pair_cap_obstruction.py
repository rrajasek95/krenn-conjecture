#!/usr/bin/env python3
"""Exact all-covector obstruction for a tensor-active binary pair cap.

The rational six-vertex source from ``notes/induction-route.md`` realizes
Delta_(6,2).  Cap the active coordinate edge 13 by the completely general
bilinear covector K=(k_ij).  On U=(2,4,5,6), this script verifies

    H_U(R_K)_(1,0,1,1) = k10*k11 = -s(K)*kappa_1(K).

Thus H_U(R_K) cannot vanish when the edge cap scalar s and both target
diagonal values kappa_0,kappa_1 are nonzero.  This uses all four entries of
K and is stronger than testing one cap or a scalar X/R repair.
"""

from __future__ import annotations

import itertools

import sympy as sp


COLORS = (0, 1)
VERTICES = (1, 2, 3, 4, 5, 6)
ZERO = ((0, 0), (0, 0))


X = {
    (1, 2): ((1, 0), (1, 0)),
    (3, 4): ((1, 0), (0, 0)),
    (5, 6): ((1, 0), (0, 0)),
    (2, 4): ((1, 0), (0, 0)),
    (1, 3): ((0, 0), (-1, 0)),
    (1, 6): ((0, 0), (0, 1)),
    (2, 3): ((0, 0), (0, 1)),
    (4, 5): ((0, 0), (0, sp.Rational(3, 4))),
    (1, 5): ((0, 0), (0, sp.Rational(1, 2))),
    (4, 6): ((0, 0), (0, sp.Rational(1, 2))),
}

K00, K01, K10, K11 = sp.symbols("k00 k01 k10 k11")
K = ((K00, K01), (K10, K11))


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for matching in perfect_matchings(rest):
            yield ((first, second),) + matching


def entry(matrices, u: int, v: int, color_u: int, color_v: int):
    if u < v:
        return matrices.get((u, v), ZERO)[color_u][color_v]
    return matrices.get((v, u), ZERO)[color_v][color_u]


def matching_tensor(vertices: tuple[int, ...], matrices):
    result = {}
    for coloring in itertools.product(COLORS, repeat=len(vertices)):
        local = dict(zip(vertices, coloring, strict=True))
        value = 0
        for matching in perfect_matchings(vertices):
            term = 1
            for u, v in matching:
                term *= entry(matrices, u, v, local[u], local[v])
            value += term
        value = sp.factor(value)
        if value != 0:
            result[coloring] = value
    return result


def first_jet(p: int, q: int):
    remaining = tuple(v for v in VERTICES if v not in (p, q))
    result = {}
    for a, b in itertools.combinations(remaining, 2):
        matrix = [[0, 0], [0, 0]]
        for color_a, color_b in itertools.product(COLORS, repeat=2):
            value = 0
            for color_p, color_q in itertools.product(COLORS, repeat=2):
                value += K[color_p][color_q] * (
                    entry(X, p, a, color_p, color_a)
                    * entry(X, q, b, color_q, color_b)
                    + entry(X, p, b, color_p, color_b)
                    * entry(X, q, a, color_q, color_a)
                )
            matrix[color_a][color_b] = sp.factor(value)
        frozen = tuple(tuple(row) for row in matrix)
        if frozen != ZERO:
            result[a, b] = frozen
    return remaining, result


def main() -> None:
    assert matching_tensor(VERTICES, X) == {
        (0,) * 6: sp.S.One,
        (1,) * 6: sp.S.One,
    }

    # Every displayed edge is tensor-active: its induced four-site cofactor
    # is nonzero.
    for edge in X:
        complement = tuple(v for v in VERTICES if v not in edge)
        assert matching_tensor(complement, X), edge

    p, q = 1, 3
    scalar = sp.factor(
        sum(
            K[i][j] * entry(X, p, q, i, j)
            for i, j in itertools.product(COLORS, repeat=2)
        )
    )
    assert scalar == -K10

    remaining, effective = first_jet(p, q)
    assert remaining == (2, 4, 5, 6)
    assert effective == {
        (2, 4): ((K00 + K10, 0), (0, 0)),
        (2, 5): ((0, 0), (0, K11 / 2)),
        (2, 6): ((0, 0), (0, K11)),
        (4, 5): ((0, K10 / 2), (0, 0)),
        (4, 6): ((0, K10), (0, 0)),
    }

    correction = matching_tensor(remaining, effective)
    assert correction == {(1, 0, 1, 1): K10 * K11}
    assert sp.factor(correction[(1, 0, 1, 1)] + scalar * K11) == 0

    print("verified exact Delta_(6,2) and activity of the capped edge 13")
    print("general cap scalar s =", scalar)
    print("H_4(R_K)[1011] =", correction[(1, 0, 1, 1)], "= -s*kappa_1")
    print("no K with s*kappa_0*kappa_1 != 0 has vanishing higher cumulant")


if __name__ == "__main__":
    main()
