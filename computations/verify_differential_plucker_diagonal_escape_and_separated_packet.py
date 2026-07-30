#!/usr/bin/env python3
"""Exact audit of the differential-Plücker separated defect-three packet."""

from fractions import Fraction as F
from itertools import combinations, combinations_with_replacement, permutations


COLORS = range(3)
P = tuple(tuple(range(8 * c, 8 * c + 3)) for c in COLORS)
M = tuple(tuple(range(8 * c + 3, 8 * c + 8)) for c in COLORS)
SITES = tuple(range(24))
E = tuple(tuple(F(a == c) for a in COLORS) for c in COLORS)
ZERO = tuple(tuple(F(0) for _ in COLORS) for _ in COLORS)
I3 = tuple(tuple(F(a == b) for b in COLORS) for a in COLORS)
GROUPS = P + M
TYPE_PAIRS = tuple(
    (GROUPS[g][0], GROUPS[h][1 if g == h else 0])
    for g, h in combinations_with_replacement(range(6), 2)
)


def outer(x, y):
    return tuple(tuple(x[a] * y[b] for b in COLORS) for a in COLORS)


def add(*matrices):
    return tuple(tuple(sum(A[a][b] for A in matrices)
                       for b in COLORS) for a in COLORS)


def scale(s, A):
    return tuple(tuple(s * A[a][b] for b in COLORS) for a in COLORS)


def transpose(A):
    return tuple(tuple(A[b][a] for b in COLORS) for a in COLORS)


def determinant(A):
    return (
        A[0][0] * (A[1][1] * A[2][2] - A[1][2] * A[2][1])
        - A[0][1] * (A[1][0] * A[2][2] - A[1][2] * A[2][0])
        + A[0][2] * (A[1][0] * A[2][1] - A[1][1] * A[2][0])
    )


X = tuple(tuple(E[c] if i in P[c] else (F(0),) * 3 for i in SITES)
          for c in COLORS)


def q_block(i, j):
    if i > j:
        return transpose(q_block(j, i))
    for c in COLORS:
        if (i in P[c] and j in M[c]) or (j in P[c] and i in M[c]):
            return I3
    for c, d in combinations(COLORS, 2):
        if i in P[c] and j in P[d]:
            return outer(E[c], E[d])
    return ZERO


ZETA = tuple(tuple(F(1) if i in P[c] else F(-1) if i in M[c] else F(0)
                   for i in SITES) for c in COLORS)


def alpha(c, d):
    omitted = 3 - c - d
    coeff = tuple(F(-1, 2) if k == omitted else F(1, 2) for k in COLORS)
    return tuple(sum(coeff[k] * ZETA[k][i] for k in COLORS) for i in SITES)


def product_block(x, y, i, j):
    return add(outer(x[i], y[j]), outer(y[i], x[j]))


def gamma_block(weights, i, j):
    return scale(weights[i] + weights[j], q_block(i, j))


def k_block(weights, A, i, j):
    return scale(sum(weights) - weights[i] - weights[j], A)


def rank(rows):
    rows = [list(row) for row in rows]
    out = 0
    for col in range(len(rows[0])):
        pivot = next((r for r in range(out, len(rows)) if rows[r][col]), None)
        if pivot is None:
            continue
        rows[out], rows[pivot] = rows[pivot], rows[out]
        value = rows[out][col]
        rows[out] = [x / value for x in rows[out]]
        for r in range(len(rows)):
            if r != out and rows[r][col]:
                value = rows[r][col]
                rows[r] = [x - value * y for x, y in zip(rows[r], rows[out])]
        out += 1
    return out


def audit():
    rank_three = tuple(pair for pair in combinations(SITES, 2)
                       if determinant(q_block(*pair)))
    expected = {tuple(sorted((i, j))) for c in COLORS for i in P[c] for j in M[c]}
    assert set(rank_three) == expected
    incidence = [tuple(F(site in edge) for site in SITES) for edge in rank_three]
    assert rank(incidence) == 21  # Three bipartite-component defects.

    primitives = [alpha(c, d) for c, d in combinations(COLORS, 2)]
    assert rank(primitives) == 3
    assert [sum(z) for z in ZETA] == [F(-2)] * 3
    assert all(sum(any(v) for v in X[c]) == 3 for c in COLORS)

    response_rows = [
        tuple(value for i, j in combinations(SITES, 2)
              for row in product_block(X[c], X[d], i, j) for value in row)
        for c, d in combinations(COLORS, 2)
    ]
    assert rank(response_rows) == 3

    for c, d in permutations(COLORS, 2):
        weights = alpha(c, d)
        assert sum(weights) == -1
        for i, j in TYPE_PAIRS:
            assert product_block(X[c], X[d], i, j) == gamma_block(weights, i, j)

    closure_checks = 0
    for a, b, d in permutations(COLORS, 3):
        ab, ad = alpha(a, b), alpha(a, d)
        bd, bb = (X[b], X[d]), (X[b], X[b])
        dd, db = (X[d], X[d]), (X[d], X[b])
        for i, j in TYPE_PAIRS:
            first = add(k_block(ab, product_block(*bd, i, j), i, j),
                        scale(-1, k_block(ad, product_block(*bb, i, j), i, j)))
            second = add(k_block(ab, product_block(*dd, i, j), i, j),
                         scale(-1, k_block(ad, product_block(*db, i, j), i, j)))
            assert first == scale(-1, gamma_block(alpha(b, d), i, j))
            assert second == gamma_block(alpha(d, b), i, j)
            closure_checks += 2

    # The selected 01 planes vanish on P_2, while response 02 does not.
    i, j = P[0][0], P[2][0]
    assert X[0][i] and X[2][j]
    assert X[0][j] == X[1][j] == (F(0),) * 3
    assert product_block(X[0], X[2], i, j) != ZERO

    # Every M_c vertex has q-neighbours only in the smaller shore P_c.
    for c in COLORS:
        neighbours = {j for i in M[c] for j in SITES if i != j and q_block(i, j) != ZERO}
        assert neighbours == set(P[c])
        assert len(M[c]) == len(P[c]) + 2

    # Every two-site deletion leaves a strict Hall deficit in at least one
    # component, so every pair complement is inactive.
    for deleted in combinations(SITES, 2):
        removed = set(deleted)
        assert any(len(set(M[c]) - removed) > len(set(P[c]) - removed)
                   for c in COLORS)

    print(f"Differential Plücker separated packet: PASS ({closure_checks} orbit blocks)")


if __name__ == "__main__":
    audit()
