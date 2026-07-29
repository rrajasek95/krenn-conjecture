#!/usr/bin/env python3
"""Exact obstruction for the 26-cell n=8 selector candidate.

The audit enumerates every perfect matching and every decoration supported by
``CELLS``, hence all 3^8 output coefficients (missing fibers have coefficient
zero).  It then checks the three factorizations which already contradict the
three-color GHZ target over every field.
"""

from __future__ import annotations

import itertools
from collections import defaultdict


CELLS = (
    (0, 1, 0, 0), (0, 2, 1, 0), (0, 2, 1, 1), (0, 3, 2, 2),
    (0, 6, 1, 1), (0, 7, 0, 0), (1, 4, 1, 0), (1, 4, 1, 1),
    (1, 5, 2, 2), (1, 6, 0, 0), (1, 7, 1, 1), (2, 3, 0, 0),
    (2, 3, 0, 1), (2, 3, 1, 0), (2, 3, 1, 1), (2, 6, 2, 2),
    (3, 6, 0, 1), (3, 6, 1, 1), (4, 5, 0, 0), (4, 5, 0, 1),
    (4, 5, 1, 0), (4, 5, 1, 1), (4, 7, 2, 2), (5, 7, 0, 1),
    (5, 7, 1, 1), (6, 7, 0, 0),
)


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for pos, v in enumerate(vertices[1:], 1):
        rest = vertices[1:pos] + vertices[pos + 1 :]
        for tail in perfect_matchings(rest):
            yield ((u, v),) + tail


def enumerate_fibers() -> dict[tuple[int, ...], tuple[tuple[int, ...], ...]]:
    by_edge: dict[tuple[int, int], list[tuple[int, int, int]]] = defaultdict(list)
    for index, (u, v, a, b) in enumerate(CELLS):
        by_edge[u, v].append((a, b, index))

    fibers: dict[tuple[int, ...], list[tuple[int, ...]]] = defaultdict(list)
    for matching in perfect_matchings(tuple(range(8))):
        choices = [by_edge[edge] for edge in matching]
        if any(not choice for choice in choices):
            continue
        for decoration in itertools.product(*choices):
            coloring = [-1] * 8
            monomial = []
            for (u, v), (a, b, index) in zip(matching, decoration):
                coloring[u], coloring[v] = a, b
                monomial.append(index)
            fibers[tuple(coloring)].append(tuple(sorted(monomial)))

    # Materialize all 3^8 coefficients, including the identically zero ones.
    return {
        coloring: tuple(sorted(fibers.get(coloring, ())))
        for coloring in itertools.product(range(3), repeat=8)
    }


def product(*indices: int) -> tuple[int, ...]:
    return tuple(sorted(indices))


def main() -> None:
    fibers = enumerate_fibers()
    assert len(fibers) == 3**8
    assert sum(bool(monomials) for monomials in fibers.values()) == 41
    assert sum(map(len, fibers.values())) == 113

    one = (1,) * 8
    two = (2,) * 8
    mixed = (1, 2, 1, 1, 2, 2, 1, 2)

    # Put A=x2*x17+x4*x14 and B=x7*x24+x10*x21.  The exact
    # enumerated fibers below say [1^8]=A*B, [mixed]=x8*x22*A,
    # and [2^8]=x3*x8*x15*x22.
    expected_one = {
        product(2, 17, 7, 24),
        product(2, 17, 10, 21),
        product(4, 14, 7, 24),
        product(4, 14, 10, 21),
    }
    expected_mixed = {
        product(8, 22, 2, 17),
        product(8, 22, 4, 14),
    }
    expected_two = {product(3, 8, 15, 22)}
    assert set(fibers[one]) == expected_one
    assert set(fibers[mixed]) == expected_mixed
    assert set(fibers[two]) == expected_two

    print("enumerated 105 perfect matchings and all 3^8 output coefficients")
    print("nonzero formal fibers: 41; decorated matching monomials: 113")
    print("[1^8] = (x2*x17+x4*x14)(x7*x24+x10*x21) = 1")
    print("[12112212] = x8*x22(x2*x17+x4*x14) = 0")
    print("[2^8] = x3*x8*x15*x22 = 1")
    print("verified: the 26-cell selector support is impossible over every field")


if __name__ == "__main__":
    main()
