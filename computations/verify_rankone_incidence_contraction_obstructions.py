#!/usr/bin/env python3
"""Exact audits for rank-one incidence contraction obstructions.

The script checks two finite shadows of the proofs in
notes/rankone-incidence-contraction-obstructions.md:

1. the one-center and one-hole identities on the exact K4 three-color
   one-factorization, using rational annihilator covectors; and
2. the constructive isolated zero-sum word for arbitrary directed Fourier
   labels, exhaustively for all normalized labelings at n=4 and on seeded
   samples at n=6,8.

No floating-point arithmetic is used.
"""

from __future__ import annotations

from itertools import product
from random import Random

import sympy as sp


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    v = vertices[0]
    for index in range(1, len(vertices)):
        w = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        for matching in perfect_matchings(rest):
            yield ((v, w),) + matching


def k4_source():
    """The three one-factors of K4, with coordinate half-vectors."""
    factors: dict[tuple[int, int], tuple[sp.Matrix, sp.Matrix]] = {}
    one_factors = (
        ((0, 1), (2, 3)),
        ((0, 2), (1, 3)),
        ((0, 3), (1, 2)),
    )
    for color, matching in enumerate(one_factors):
        e = sp.eye(3)[:, color]
        for u, v in matching:
            factors[u, v] = (e, e)
    return factors


def half_vector(factors, v: int, u: int) -> sp.Matrix:
    if v < u:
        return factors[v, u][0]
    return factors[u, v][1]


def matrix_at(factors, u: int, v: int) -> sp.Matrix:
    if u < v:
        left, right = factors[u, v]
        return left * right.T
    left, right = factors[v, u]
    return right * left.T


def matching_tensor_coefficient(factors, vertices, coloring):
    total = sp.Integer(0)
    for matching in perfect_matchings(tuple(vertices)):
        term = sp.Integer(1)
        for u, v in matching:
            term *= matrix_at(factors, u, v)[coloring[u], coloring[v]]
        total += term
    return sp.expand(total)


def audit_k4_contractions():
    factors = k4_source()
    vertices = tuple(range(4))
    for coloring in product(range(3), repeat=4):
        expected = int(len(set(coloring)) == 1)
        assert matching_tensor_coefficient(factors, vertices, coloring) == expected

    # Center p=0.  Its opposite endpoint factors on 01,02,03 are e0,e1,e2.
    p = 0
    annihilators = {
        1: sp.Matrix([0, 2, 3]),
        2: sp.Matrix([5, 0, 7]),
        3: sp.Matrix([11, 13, 0]),
    }
    for u, alpha in annihilators.items():
        assert (alpha.T * half_vector(factors, u, p))[0] == 0
    no_hole = sp.Matrix(
        [sp.prod(annihilators[u][r] for u in (1, 2, 3)) for r in range(3)]
    )
    assert no_hole == sp.zeros(3, 1)

    # Leave w=1 open.  The remaining e0-coordinate product is nonzero,
    # and the identity is a nonzero multiple of E00 on both sides.
    w = 1
    contracted = [u for u in vertices if u not in (p, w)]
    diagonal = sp.diag(
        *[sp.prod(annihilators[u][r] for u in contracted) for r in range(3)]
    )
    assert diagonal == sp.diag(55, 0, 0)
    cofactor = matrix_at(factors, 2, 3)
    h = sum(
        annihilators[2][a] * cofactor[a, b] * annihilators[3][b]
        for a in range(3)
        for b in range(3)
    )
    right = h * matrix_at(factors, p, w)
    assert right == diagonal


def isolated_zero_sum_word(labels: list[list[int]], v: int, a: int):
    """Construct the unsupported zero-sum word from Section 6."""
    n = len(labels)
    S = [u for u in range(n) if u != v and labels[v][u] == a]
    assert len(S) < n - 1
    outside = next(u for u in range(n) if u != v and u not in S)
    c = [0] * n
    c[v] = a
    for u in S:
        c[u] = (labels[u][v] + 1) % 3
    # All remaining sites except ``outside`` stay zero; outside repairs sum.
    c[outside] = (-sum(c)) % 3
    assert sum(c) % 3 == 0
    for u in range(n):
        if u == v:
            continue
        assert not (labels[v][u] == c[v] and labels[u][v] == c[u])
    return tuple(c)


def audit_fourier_isolation():
    # Exhaust all directed labelings at n=4 after fixing the three labels
    # out of vertex zero to 0,1,2.  The other nine directed labels are free.
    n = 4
    positions = [(v, u) for v in range(n) for u in range(n) if v != u and v != 0]
    for values in product(range(3), repeat=len(positions)):
        labels = [[-1] * n for _ in range(n)]
        labels[0][1], labels[0][2], labels[0][3] = 0, 1, 2
        for (v, u), value in zip(positions, values):
            labels[v][u] = value
        for v in range(n):
            used = {labels[v][u] for u in range(n) if u != v}
            if used != {0, 1, 2}:
                break
        else:
            for v in range(n):
                for a in range(3):
                    isolated_zero_sum_word(labels, v, a)

    rng = Random(20260724)
    for n in (6, 8):
        checked = 0
        while checked < 200:
            labels = [[-1] * n for _ in range(n)]
            for v in range(n):
                row = [0, 1, 2] + [rng.randrange(3) for _ in range(n - 4)]
                rng.shuffle(row)
                for u, value in zip((u for u in range(n) if u != v), row):
                    labels[v][u] = value
            for v in range(n):
                for a in range(3):
                    isolated_zero_sum_word(labels, v, a)
            checked += 1


def main():
    audit_k4_contractions()
    audit_fourier_isolation()
    print("PASS: rank-one contraction and Fourier-isolation audits")


if __name__ == "__main__":
    main()
