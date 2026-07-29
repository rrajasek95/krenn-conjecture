#!/usr/bin/env python3
"""Audit the uniform polystable binary bad-reduction construction.

The calculation is exact in Q(sqrt(3)).  It checks the full matching tensor
for several even orders, strict target-torus balance, moment-map balance,
and the negative color-balanced two-adic Farkas vector.
"""

from __future__ import annotations

import itertools

import sympy as sp


def edge(u: int, v: int) -> tuple[int, int]:
    return tuple(sorted((u, v)))


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for position, v in enumerate(vertices[1:], 1):
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield (edge(u, v),) + tail


def source(n: int):
    p0 = tuple((2 * k, 2 * k + 1) for k in range(n // 2))
    p0_prime = (edge(0, 2), edge(1, 3)) + p0[2:]
    p1 = tuple(edge(k, k + 1) for k in range(1, n - 1, 2)) + (
        edge(0, n - 1),
    )

    cells: dict[tuple[tuple[int, int], int], sp.Expr] = {}
    for e in (edge(0, 1), edge(2, 3)):
        cells[e, 0] = sp.Rational(1, 2)
    for e in (edge(0, 2), edge(1, 3)):
        cells[e, 0] = sp.sqrt(3) / 2
    for e in p0[2:]:
        cells[e, 0] = sp.S.One
    for e in p1:
        cells[e, 1] = sp.S.One
    return (p0, p0_prime, p1), cells


def matching_tensor(n: int, cells):
    fibers: dict[tuple[int, ...], sp.Expr] = {}
    supported = []
    for matching in perfect_matchings(tuple(range(n))):
        choices = []
        for e in matching:
            choices.append(
                tuple((a, value) for (f, a), value in cells.items() if f == e)
            )
        for selection in itertools.product(*choices):
            coloring = [None] * n
            value = sp.S.One
            for e, (a, factor) in zip(matching, selection):
                coloring[e[0]] = coloring[e[1]] = a
                value *= factor
            key = tuple(coloring)
            fibers[key] = sp.simplify(fibers.get(key, 0) + value)
            supported.append((frozenset(matching), key, sp.simplify(value)))
    return fibers, supported


def verify_order(n: int) -> None:
    expected_matchings, cells = source(n)
    fibers, supported = matching_tensor(n, cells)

    assert {item[0] for item in supported} == {
        frozenset(matching) for matching in expected_matchings
    }
    assert sp.simplify(fibers[(0,) * n] - 1) == 0
    assert sp.simplify(fibers[(1,) * n] - 1) == 0
    assert all(
        sp.simplify(value) == 0
        for coloring, value in fibers.items()
        if len(set(coloring)) > 1
    )

    # Squared magnitudes give a strictly positive balancing vector and
    # actual moment-map zero: every port incidence is one.
    for v in range(n):
        for a in range(2):
            incidence = sum(
                abs(value) ** 2
                for (e, color), value in cells.items()
                if color == a and v in e
            )
            assert sp.simplify(incidence - 1) == 0

    # Normalize nu(2)=1.  Both 1/2 and sqrt(3)/2 have valuation -1;
    # all unit cells have valuation zero.  The integer Farkas vector has
    # weight one on the switched C4 and two on every tail edge.
    multiplicity = {}
    for e in (edge(0, 1), edge(2, 3), edge(0, 2), edge(1, 3)):
        multiplicity[e, 0] = 1
    for e in expected_matchings[0][2:]:
        multiplicity[e, 0] = 2

    port_degrees = {(v, a): 0 for v in range(n) for a in range(2)}
    valuation_pairing = 0
    for (e, a), amount in multiplicity.items():
        port_degrees[e[0], a] += amount
        port_degrees[e[1], a] += amount
        valuation_pairing += amount * (-1 if e in {
            edge(0, 1), edge(2, 3), edge(0, 2), edge(1, 3)
        } else 0)

    assert [port_degrees[v, 0] for v in range(n)] == [2] * n
    assert [port_degrees[v, 1] for v in range(n)] == [0] * n
    assert valuation_pairing == -4


def main() -> None:
    for n in (4, 6, 8, 10, 12):
        verify_order(n)
    print("verified exact binary GHZ matching tensors for n=4,6,8,10,12")
    print("verified strict torus balance and unit moment-map incidence")
    print("verified color-balanced Farkas vector with pairing -4*nu(2)")


if __name__ == "__main__":
    main()
