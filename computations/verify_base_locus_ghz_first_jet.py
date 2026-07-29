#!/usr/bin/env python3
"""Verify two primitive Z/4 base-locus sources with first jet ternary GHZ."""

from __future__ import annotations

import itertools


N = 6
Q = 3


def perfect_matchings(vertices=tuple(range(N))):
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for position, v in enumerate(vertices[1:], 1):
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield ((u, v),) + tail


MATCHINGS = tuple(perfect_matchings())
COLORINGS = tuple(itertools.product(range(Q), repeat=N))


def matrix(*rows):
    assert len(rows) == Q and all(len(row) == Q for row in rows)
    return tuple(tuple(row) for row in rows)


SAME = {
    (0, 1): matrix((1, 0, 0), (0, 0, 0), (0, 0, 0)),
    (0, 4): matrix((0, 0, 0), (0, 0, 0), (0, 0, 1)),
    (0, 5): matrix((0, 0, 0), (0, 1, 0), (0, 0, 0)),
    (1, 2): matrix((0, 0, 0), (0, 0, 0), (0, 0, 2)),
    (1, 4): matrix((0, 0, 0), (0, 2, 0), (0, 0, 0)),
    (2, 3): matrix((0, 0, 0), (0, 1, 0), (0, 0, 0)),
    (2, 5): matrix((1, 0, 0), (0, 0, 0), (0, 0, 0)),
    (3, 4): matrix((2, 0, 0), (0, 0, 0), (0, 0, 0)),
    (3, 5): matrix((0, 0, 0), (0, 0, 0), (0, 0, 1)),
}


CROSS = {
    (0, 1): matrix((0, 3, 0), (0, 0, 0), (0, 0, 0)),
    (0, 2): matrix((0, 0, 0), (0, 1, 0), (0, 0, 0)),
    (0, 3): matrix((1, 0, 0), (0, 0, 0), (0, 0, 0)),
    (0, 4): matrix((0, 0, 0), (0, 0, 0), (0, 0, 1)),
    (1, 3): matrix((0, 0, 0), (0, 0, 0), (0, 0, 1)),
    (1, 5): matrix((2, 0, 0), (0, 1, 0), (0, 0, 0)),
    (2, 4): matrix((1, 0, 0), (0, 0, 0), (0, 0, 0)),
    (2, 5): matrix((0, 0, 0), (0, 0, 0), (0, 0, 2)),
    (3, 4): matrix((0, 0, 0), (0, 2, 0), (0, 0, 0)),
    (3, 5): matrix((0, 1, 0), (0, 0, 0), (0, 0, 0)),
}


ZERO = matrix((0, 0, 0), (0, 0, 0), (0, 0, 0))


def coefficients(source):
    answer = {}
    for coloring in COLORINGS:
        total = 0
        for matching in MATCHINGS:
            term = 1
            for u, v in matching:
                term *= source.get((u, v), ZERO)[coloring[u]][coloring[v]]
            total += term
        answer[coloring] = total
    return answer


def verify(name, source, primitive_cell, blocked_coloring):
    values = coefficients(source)
    assert source[primitive_cell[:2]][primitive_cell[2]][primitive_cell[3]] % 2
    for coloring, value in values.items():
        target = 2 if len(set(coloring)) == 1 else 0
        assert value % 4 == target, (name, coloring, value, target)

    reduced = {
        edge: tuple(tuple(value % 2 for value in row) for row in table)
        for edge, table in source.items()
    }
    reduced_values = coefficients(reduced)
    assert all(value % 2 == 0 for value in reduced_values.values())
    for coloring, value in values.items():
        first_jet = (value // 2) % 2
        assert first_jet == int(len(set(coloring)) == 1)
    print(f"verified {name}: primitive, H(A)=2*Delta mod 4, H(A mod 2)=0")

    # A lift has the form A+4C modulo eight.  Its linear correction in a
    # coloring is supported only when two of a matching's three selected
    # base entries are odd.  The blocked coloring has no such pair, while
    # its current mixed coefficient is 4 modulo eight.
    assert values[blocked_coloring] % 8 == 4
    for matching in MATCHINGS:
        selected = [
            source.get(edge, ZERO)[blocked_coloring[edge[0]]][
                blocked_coloring[edge[1]]
            ]
            % 2
            for edge in matching
        ]
        assert sum(selected) <= 1
    print(
        f"verified no mod-8 lift: zero derivative at mixed coloring "
        f"{blocked_coloring}, residual=4"
    )


def main():
    verify("same-color model", SAME, (0, 1, 0, 0), (1, 2, 2, 0, 0, 1))
    verify("cross-color model", CROSS, (0, 1, 0, 1), (0, 1, 2, 1, 1, 2))
    print("verified all 729 coefficients and the divided first GHZ jet")


if __name__ == "__main__":
    main()
