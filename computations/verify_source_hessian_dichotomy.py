#!/usr/bin/env python3
"""Exact finite-field audit for the source-Hessian dichotomy.

This finds deterministic full-rank internal edge families q for which the
kernel of Z -> Z*q^(m-2) consists exactly of the universal vertex gauges.
The theorem itself is characteristic-zero linear algebra; these finite-field
specializations only certify that its genericity hypotheses are nonvacuous.
"""

from itertools import combinations, product
from math import factorial
from random import Random


P = 1_000_003


def det3(a):
    return (
        a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1])
        - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
        + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0])
    ) % P


def random_q(n, rng):
    while True:
        q = {}
        good = True
        for i, j in combinations(range(n), 2):
            a = [[rng.randrange(1, P) for _ in range(3)] for _ in range(3)]
            if not det3(a):
                good = False
                break
            q[i, j] = a
        if good:
            return q


def qentry(q, i, a, j, b):
    if i < j:
        return q[i, j][a][b]
    return q[j, i][b][a]


def hafnian(q, vertices, colors, memo):
    key = tuple(vertices)
    if not key:
        return 1
    if key in memo:
        return memo[key]
    i = key[0]
    total = 0
    for pos in range(1, len(key)):
        j = key[pos]
        rest = key[1:pos] + key[pos + 1 :]
        total += qentry(q, i, colors[i], j, colors[j]) * hafnian(q, rest, colors, memo)
    memo[key] = total % P
    return memo[key]


def multiplication_columns(q, n):
    """Columns of Z -> Z*q^(n/2-1), as sparse row dictionaries."""
    power = n // 2 - 1
    scale = factorial(power) % P
    colorings = tuple(product(range(3), repeat=n))
    columns = []
    labels = []
    for i, j in combinations(range(n), 2):
        remaining = tuple(v for v in range(n) if v not in (i, j))
        for a, b in product(range(3), repeat=2):
            col = {}
            for row, colors in enumerate(colorings):
                if colors[i] != a or colors[j] != b:
                    continue
                value = scale * hafnian(q, remaining, colors, {}) % P
                if value:
                    col[row] = value
            columns.append(col)
            labels.append((i, j, a, b))
    return labels, columns


def sparse_column_rank(columns):
    pivots = {}
    for original in columns:
        col = dict(original)
        while col:
            pivot = min(col)
            if pivot not in pivots:
                inv = pow(col[pivot], P - 2, P)
                col = {r: value * inv % P for r, value in col.items() if value % P}
                pivots[pivot] = col
                break
            factor = col[pivot]
            base = pivots[pivot]
            for row, value in base.items():
                new = (col.get(row, 0) - factor * value) % P
                if new:
                    col[row] = new
                elif row in col:
                    del col[row]
    return len(pivots)


def gauge_columns(q, labels, n):
    """n-1 independent gauges alpha_i=1, alpha_(n-1)=-1."""
    index = {label: k for k, label in enumerate(labels)}
    gauges = []
    for t in range(n - 1):
        alpha = [0] * n
        alpha[t] = 1
        alpha[-1] = -1
        vector = [0] * len(labels)
        for i, j in combinations(range(n), 2):
            scalar = (alpha[i] + alpha[j]) % P
            for a, b in product(range(3), repeat=2):
                vector[index[i, j, a, b]] = scalar * q[i, j][a][b] % P
        gauges.append(vector)
    return gauges


def linear_rank(vectors):
    rows = [list(v) for v in vectors]
    if not rows:
        return 0
    rank = 0
    cols = len(rows[0])
    for col in range(cols):
        pivot = next((i for i in range(rank, len(rows)) if rows[i][col] % P), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inv = pow(rows[rank][col] % P, P - 2, P)
        rows[rank] = [x * inv % P for x in rows[rank]]
        for i in range(len(rows)):
            if i != rank and rows[i][col] % P:
                f = rows[i][col] % P
                rows[i] = [(x - f * y) % P for x, y in zip(rows[i], rows[rank])]
        rank += 1
    return rank


def audit(n, seed):
    rng = Random(seed)
    domain = 9 * (n * (n - 1) // 2)
    expected = domain - (n - 1)
    for trial in range(1, 21):
        q = random_q(n, rng)
        labels, columns = multiplication_columns(q, n)
        rank = sparse_column_rank(columns)
        if rank != expected:
            continue
        gauges = gauge_columns(q, labels, n)
        assert linear_rank(gauges) == n - 1

        # Directly check that every gauge is killed by the multiplication map.
        for gauge in gauges:
            output = {}
            for coefficient, column in zip(gauge, columns):
                if not coefficient:
                    continue
                for row, value in column.items():
                    output[row] = (output.get(row, 0) + coefficient * value) % P
            assert not any(output.values())
        print(
            f"n={n}: trial={trial}, derivative rank={rank}/{domain}, "
            f"kernel=gauge dimension {n - 1}, all {n*(n-1)//2} edges rank 3"
        )
        return
    raise AssertionError(f"no gauge-rigid specialization found for n={n}")


def main():
    audit(4, 20260724)
    audit(6, 20260725)
    print("verified nonvacuous gauge-rigid full-rank internal charts")


if __name__ == "__main__":
    main()
