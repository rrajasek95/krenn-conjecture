#!/usr/bin/env python3
"""Exact audit for the pair-suspension obstruction of the n=8 border core.

The internal quadratic is the twelve-cell, three-matching seed from
``verify_n8_border_seed_direct_repair.py``, with every cell specialized to
one.  This script constructs its eight-site matching tensor and its complete
quadratic response map.  It checks that singleton response rows expose every
quadratic cell outside the twelve-cell seed and reconstructs the five
remaining incidence rows used in the proof.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction

from verify_n8_border_seed_direct_repair import (
    MATCHINGS,
    N,
    Q,
    SEED,
    TARGET_MATCHINGS,
    perfect_matchings,
)


CELLS = tuple(
    (u, v, a, b)
    for u in range(N)
    for v in range(u + 1, N)
    for a in range(Q)
    for b in range(Q)
)


def matching_tensor_rows():
    """Return the coefficient table of H_8(q)."""

    rows = Counter()
    for matching in MATCHINGS:
        word = [None] * N
        ok = True
        for u, v in matching:
            choices = [cell for cell in SEED if cell[:2] == (u, v)]
            if not choices:
                ok = False
                break
            # The three selected one-factors are edge-disjoint, so a physical
            # seed edge carries exactly one decorated cell.
            assert len(choices) == 1
            _u, _v, a, b = choices[0]
            word[u], word[v] = a, b
        if ok:
            rows[tuple(word)] += 1
    return rows


def quadratic_response_rows():
    """Rows of Z -> Z q^3/3!, represented as integer column counters."""

    rows = defaultdict(Counter)
    for column in CELLS:
        u, v, a, b = column
        remaining = tuple(i for i in range(N) if i not in (u, v))
        for matching in perfect_matchings(remaining):
            word = [None] * N
            word[u], word[v] = a, b
            ok = True
            for i, j in matching:
                choices = [cell for cell in SEED if cell[:2] == (i, j)]
                if not choices:
                    ok = False
                    break
                assert len(choices) == 1
                _i, _j, c, d = choices[0]
                word[i], word[j] = c, d
            if ok:
                rows[tuple(word)][column] += 1
    return rows


def rational_rank(matrix):
    """Tiny exact row reduction over Q."""

    a = [[Fraction(x) for x in row] for row in matrix]
    if not a:
        return 0
    m, n = len(a), len(a[0])
    rank = col = 0
    while rank < m and col < n:
        pivot = next((i for i in range(rank, m) if a[i][col]), None)
        if pivot is None:
            col += 1
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        scale = a[rank][col]
        a[rank] = [x / scale for x in a[rank]]
        for i in range(m):
            if i == rank or not a[i][col]:
                continue
            scale = a[i][col]
            a[i] = [x - scale * y for x, y in zip(a[i], a[rank])]
        rank += 1
        col += 1
    return rank


def main():
    assert len(CELLS) == 252 and len(SEED) == 12

    hq = matching_tensor_rows()
    errors = {
        (2, 2, 1, 0, 1, 0, 0, 0),
        (0, 1, 0, 0, 2, 1, 0, 2),
    }
    pure = {(r,) * N for r in range(Q)}
    special = pure | errors
    assert hq == Counter({word: 1 for word in special})

    rows = quadratic_response_rows()
    singleton_rows = {
        word: next(iter(row))
        for word, row in rows.items()
        if word not in special and len(row) == 1
        and next(iter(row.values())) == 1
    }
    exposed = set(singleton_rows.values())
    assert len(singleton_rows) == 358
    assert len(exposed) == 240
    assert exposed == set(CELLS) - set(SEED)

    # Only the five matching words survive after restriction to the seed
    # coordinates.  Each is the incidence row of its unique seed matching.
    restricted = {}
    for word, row in rows.items():
        seed_row = Counter({cell: value for cell, value in row.items() if cell in SEED})
        if seed_row:
            restricted[word] = seed_row
    assert set(restricted) == special
    assert all(set(row.values()) == {1} and len(row) == 4 for row in restricted.values())

    expected_matchings = {
        (r,) * N: frozenset(
            (u, v, r, r) for u, v in TARGET_MATCHINGS[r]
        )
        for r in range(Q)
    }
    expected_matchings[(2, 2, 1, 0, 1, 0, 0, 0)] = frozenset({
        (0, 1, 2, 2), (2, 4, 1, 1),
        (3, 6, 0, 0), (5, 7, 0, 0),
    })
    expected_matchings[(0, 1, 0, 0, 2, 1, 0, 2)] = frozenset({
        (0, 2, 0, 0), (1, 5, 1, 1),
        (3, 6, 0, 0), (4, 7, 2, 2),
    })
    for word, matching in expected_matchings.items():
        assert frozenset(restricted[word]) == matching

    matrix = [
        [restricted[word].get(cell, 0) for cell in sorted(SEED)]
        for word in sorted(special)
    ]
    assert rational_rank(matrix) == 5

    # The allowed local-port pairs are precisely a matching on the 24 ports:
    # every site/color port occurs on its color one-factor exactly once.
    allowed_ports = {
        frozenset(((u, r), (v, r)))
        for r, matching in enumerate(TARGET_MATCHINGS)
        for u, v in matching
    }
    assert len(allowed_ports) == 12
    degree = Counter(port for edge in allowed_ports for port in edge)
    assert set(degree) == {(i, r) for i in range(N) for r in range(Q)}
    assert set(degree.values()) == {1}

    print("PASS: n=8 border pair-suspension response audit")
    print(f"  response rows={len(rows)}, singleton rows={len(singleton_rows)}")
    print(f"  exposed nonseed cells={len(exposed)}, seed response rank=5")


if __name__ == "__main__":
    main()
