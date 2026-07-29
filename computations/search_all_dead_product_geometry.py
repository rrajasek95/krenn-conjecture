#!/usr/bin/env python3
"""Exact reconnaissance for the all-dead corank-two product geometry.

This is not used as a proof.  It performs three reproducible checks:

1. the rational three-site symmetric model from the note has
   off-diagonal rank two, every row/column pair has rank two, and total
   all-nine rank three;
2. over F_3, no four-scalar-site model with both star triples of rank
   three, all six forms supported on at least three sites, and the
   row/column basis property exists;
3. in the normalized aligned-k=2 four-space, all 63,180 decompositions
   of type 2+1+1 over F_3 are checked.  Whenever the five-space of lifted
   off-diagonal products has a block-diagonal intersection of dimension
   at least three, one of the six named star vectors misses a summand.
"""

from itertools import combinations, permutations, product

import sympy as sp


Q = 3


def rank_mod(rows: list[tuple[int, ...] | list[int]]) -> int:
    if not rows:
        return 0
    a = [list(row) for row in rows]
    m, n = len(a), len(a[0])
    r = 0
    for c in range(n):
        pivot = next((i for i in range(r, m) if a[i][c] % Q), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        scale = pow(a[r][c], -1, Q)
        a[r] = [(scale * x) % Q for x in a[r]]
        for i in range(m):
            if i != r and a[i][c] % Q:
                scale = a[i][c] % Q
                a[i] = [(x - scale * y) % Q for x, y in zip(a[i], a[r])]
        r += 1
    return r


def rref_key(rows: list[tuple[int, ...]]) -> tuple[tuple[int, ...], ...] | None:
    a = [list(row) for row in rows]
    m, n = len(a), len(a[0])
    r = 0
    for c in range(n):
        pivot = next((i for i in range(r, m) if a[i][c] % Q), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        scale = pow(a[r][c], -1, Q)
        a[r] = [(scale * x) % Q for x in a[r]]
        for i in range(m):
            if i != r and a[i][c] % Q:
                scale = a[i][c] % Q
                a[i] = [(x - scale * y) % Q for x, y in zip(a[i], a[r])]
        r += 1
    if r != m:
        return None
    return tuple(tuple(row) for row in a)


def canonical_line(v: tuple[int, ...]) -> tuple[int, ...]:
    for x in v:
        if x % Q:
            scale = pow(x, -1, Q)
            return tuple((scale * y) % Q for y in v)
    raise ValueError("zero vector")


def inverse_mod(a: list[list[int]]) -> list[list[int]] | None:
    n = len(a)
    aug = [
        list(row) + [int(i == j) for j in range(n)]
        for i, row in enumerate(a)
    ]
    for c in range(n):
        pivot = next((i for i in range(c, n) if aug[i][c] % Q), None)
        if pivot is None:
            return None
        aug[c], aug[pivot] = aug[pivot], aug[c]
        scale = pow(aug[c][c], -1, Q)
        aug[c] = [(scale * x) % Q for x in aug[c]]
        for i in range(n):
            if i != c and aug[i][c] % Q:
                scale = aug[i][c] % Q
                aug[i] = [
                    (x - scale * y) % Q for x, y in zip(aug[i], aug[c])
                ]
    return [row[n:] for row in aug]


def rational_model() -> None:
    p = sp.Matrix([[1, 2, 3], [1, 1, -3], [7, -8, -1]])
    edges = list(combinations(range(3), 2))

    def mul(c: int, d: int) -> sp.Matrix:
        return sp.Matrix(
            [p[i, c] * p[j, d] + p[i, d] * p[j, c] for i, j in edges]
        )

    directed = [(0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1)]
    off = sp.Matrix.hstack(*(mul(c, d) for c, d in directed))
    diag = sp.Matrix.hstack(*(mul(c, c) for c in range(3)))
    assert p.det() == -110
    assert off.rank() == 2
    assert all(
        sp.Matrix.hstack(*(mul(c, d) for d in range(3) if d != c)).rank()
        == 2
        for c in range(3)
    )
    assert all(
        sp.Matrix.hstack(*(mul(c, d) for c in range(3) if c != d)).rank()
        == 2
        for d in range(3)
    )
    assert sp.Matrix.hstack(off, diag).rank() == 3


def scalar_four_site_search() -> None:
    edges = list(combinations(range(4), 2))

    def mul(x: tuple[int, ...], y: tuple[int, ...]) -> tuple[int, ...]:
        return tuple(
            (x[i] * y[j] + y[i] * x[j]) % Q for i, j in edges
        )

    forms = sorted(
        {
            canonical_line(v)
            for v in product(range(Q), repeat=4)
            if sum(x != 0 for x in v) >= 3
        }
    )
    triples = [
        triple
        for triple in permutations(forms, 3)
        if rank_mod(list(triple)) == 3
    ]
    solutions = 0
    for p in triples:
        buckets: list[dict[tuple[tuple[int, ...], ...], list[tuple[int, ...]]]]
        buckets = []
        for d in range(3):
            cs = [c for c in range(3) if c != d]
            bucket: dict[tuple[tuple[int, ...], ...], list[tuple[int, ...]]]
            bucket = {}
            for s in forms:
                key = rref_key([mul(p[cs[0]], s), mul(p[cs[1]], s)])
                if key is not None:
                    bucket.setdefault(key, []).append(s)
            buckets.append(bucket)
        for key in set(buckets[0]) & set(buckets[1]) & set(buckets[2]):
            for s0 in buckets[0][key]:
                for s1 in buckets[1][key]:
                    for s2 in buckets[2][key]:
                        if rank_mod([s0, s1, s2]) == 3:
                            solutions += 1
    assert solutions == 0


def aligned_two_plane_decomposition_search() -> None:
    lines = sorted(
        {
            canonical_line(v)
            for v in product(range(Q), repeat=4)
            if any(v)
        }
    )
    planes = sorted(
        {
            key
            for x, y in combinations(lines, 2)
            if (key := rref_key([x, y])) is not None
        }
    )
    assert len(lines) == 40
    assert len(planes) == 130

    # Coordinates are (p_0,p_1,p_2,t), with v=(1,1,1).
    # Z has zero diagonal and
    # q_23=q_01+q_02+q_12-q_03-q_13.
    edge_pairs = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    z_basis: list[list[list[int]]] = []
    for k in range(5):
        values = [0] * 6
        values[k] = 1
        values[5] = (
            values[0] + values[1] + values[3] - values[2] - values[4]
        ) % Q
        matrix = [[0] * 4 for _ in range(4)]
        for value, (i, j) in zip(values, edge_pairs):
            matrix[i][j] = matrix[j][i] = value
        z_basis.append(matrix)

    def bilinear(matrix: list[list[int]], x: tuple[int, ...],
                 y: tuple[int, ...]) -> int:
        return sum(
            x[i] * matrix[i][j] * y[j]
            for i in range(4)
            for j in range(4)
        ) % Q

    def matvec(matrix: list[list[int]], x: tuple[int, ...]) -> list[int]:
        return [
            sum(matrix[i][j] * x[j] for j in range(4)) % Q
            for i in range(4)
        ]

    named = [
        (1, 0, 0, 0),
        (0, 1, 0, 0),
        (0, 0, 1, 0),
        (1, 0, 0, 1),
        (0, 1, 0, 1),
        (0, 0, 1, 1),
    ]
    decompositions = 0
    low_cross_rank = 0
    dense_low_cross_rank = 0
    for plane in planes:
        for y, z in combinations(lines, 2):
            change = [
                [plane[0][i], plane[1][i], y[i], z[i]] for i in range(4)
            ]
            inverse = inverse_mod(change)
            if inverse is None:
                continue
            decompositions += 1
            cross_rows = [
                [
                    bilinear(matrix, plane[0], y),
                    bilinear(matrix, plane[1], y),
                    bilinear(matrix, plane[0], z),
                    bilinear(matrix, plane[1], z),
                    bilinear(matrix, y, z),
                ]
                for matrix in z_basis
            ]
            if rank_mod(cross_rows) > 2:
                continue
            low_cross_rank += 1
            support_counts = []
            for vector in named:
                coordinates = matvec(inverse, vector)
                support_counts.append(
                    int(bool(coordinates[0] or coordinates[1]))
                    + int(bool(coordinates[2]))
                    + int(bool(coordinates[3]))
                )
            if min(support_counts) >= 3:
                dense_low_cross_rank += 1

    assert decompositions == 63_180
    assert low_cross_rank == 30
    assert dense_low_cross_rank == 0


def main() -> None:
    rational_model()
    scalar_four_site_search()
    aligned_two_plane_decomposition_search()
    print("all-dead product-geometry reconnaissance: PASS")


if __name__ == "__main__":
    main()
