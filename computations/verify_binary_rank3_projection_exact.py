#!/usr/bin/env python3
"""Exact audit of the C3 binary rank-three projection construction."""

from __future__ import annotations

import itertools

import sympy as sp

from verify_binary_spinflip_cycle_identity import perfect_matchings


def require(condition: object, message: str) -> None:
    """Check a load-bearing condition in a way ``python3 -O`` cannot remove."""

    if not condition:
        raise ValueError(message)


I = sp.I
R = 2 ** (-sp.Rational(1, 3))
Q0 = R / sp.sqrt(3)
T = 2 ** sp.Rational(1, 3)
H = sp.Matrix(((0, 1), (-1, 1)))
RHO = (2, 3, 4, 5, 0, 1)
COCYCLE = {
    (0, 1): -I, (2, 3): 1, (4, 5): I,
    (0, 2): I, (2, 4): -1, (0, 4): I,
    (0, 3): -I, (2, 5): I, (1, 4): 1,
    (0, 5): 1, (1, 2): 1, (3, 4): 1,
    (1, 3): -1, (3, 5): -I, (1, 5): -I,
}


def put_oriented(answer, u, v, matrix):
    if u < v:
        answer[u, v] = matrix
    else:
        answer[v, u] = matrix.T


def source():
    d = T * (-sp.sqrt(3) / 9 + I / 6)
    e = T * (sp.sqrt(3) / 36 + I / 12)
    seeds = {
        (0, 1): sp.Matrix(
            ((R - I * Q0, (R - I * Q0) / 2),
             ((R - I * Q0) / 2, -I * Q0))
        ),
        (0, 2): sp.Matrix(((1, 0), (1, 1))),
        (0, 3): sp.Matrix(
            ((Q0, Q0 / 2 + I * R / 2),
             (Q0 / 2 + I * R / 2, Q0 + I * R))
        ),
        (0, 5): sp.Matrix(
            ((I * Q0, R / 2 + I * Q0 / 2),
             (R / 2 + I * Q0 / 2, I * Q0))
        ),
        (1, 3): sp.Matrix(((d, d - e), (e, d))),
    }
    answer = {}
    for (u, v), seed in seeds.items():
        matrix = seed
        for _ in range(3):
            put_oriented(answer, u, v, matrix)
            matrix = COCYCLE[tuple(sorted((u, v)))] * H * matrix * H.T
            u, v = RHO[u], RHO[v]
        require(
            sp.simplify(matrix - seed) == sp.zeros(2),
            "sp.simplify(matrix - seed) == sp.zeros(2)",
        )
    require(
        len(answer) == 15,
        "len(answer) == 15",
    )
    return answer


def reduce_exact(expression):
    # Algebraic simplification is much faster after adjoining the radicals.
    return sp.cancel(
        sp.polys.polytools.cancel(expression, extension=[I, sp.sqrt(3), T])
    )


def main():
    matrices = source()
    require(
        all(reduce_exact(matrix.det()) != 0 for matrix in matrices.values()),
        "all(reduce_exact(matrix.det()) != 0 for matrix in matrice...",
    )
    matchings = tuple(perfect_matchings(tuple(range(6))))
    counts = {}
    for coloring in itertools.product((0, 1), repeat=6):
        coefficient = 0
        for matching in matchings:
            term = 1
            for u, v in matching:
                term *= matrices[u, v][coloring[u], coloring[v]]
            coefficient += term
        expected = 1 + int(not any(coloring)) + int(all(coloring))
        residual = reduce_exact(sp.expand(coefficient - expected))
        require(
            residual == 0,
            (coloring, residual),
        )
        counts[expected] = counts.get(expected, 0) + 1

    require(
        counts == {2: 2, 1: 62},
        "counts == {2: 2, 1: 62}",
    )
    print("verified all 64 exact coefficients of e0^6+e1^6+(e0+e1)^6")
    print("verified 15 finite invertible algebraic C3-equivariant edge matrices")


if __name__ == "__main__":
    main()
