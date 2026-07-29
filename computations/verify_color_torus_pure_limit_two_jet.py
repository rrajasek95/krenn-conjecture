#!/usr/bin/env python3
"""Audit the dense pure-limit simultaneous two-jet countermodule."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from functools import cache, reduce
from itertools import combinations, product


N = 6
VERTICES = tuple(range(N))
FULL = (1 << N) - 1


def edge(u: int, v: int) -> tuple[int, int]:
    return (u, v) if u < v else (v, u)


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        remainder = vertices[1:index] + vertices[index + 1 :]
        for matching in perfect_matchings(remainder):
            yield ((first, second),) + matching


MATCHINGS = tuple(perfect_matchings(VERTICES))
LEADING = {
    selected_edge: Fraction(-11, 3) if selected_edge == (0, 1) else Fraction(1)
    for selected_edge in combinations(VERTICES, 2)
}


@cache
def leading_hafnian(mask: int) -> Fraction:
    if mask == 0:
        return Fraction(1)
    first_bit = mask & -mask
    u = first_bit.bit_length() - 1
    answer = Fraction(0)
    remainder = mask ^ first_bit
    while remainder:
        next_bit = remainder & -remainder
        v = next_bit.bit_length() - 1
        answer += LEADING[edge(u, v)] * leading_hafnian(
            mask ^ first_bit ^ next_bit
        )
        remainder ^= next_bit
    return answer


def cofactor(*deleted: int) -> Fraction:
    mask = FULL
    for vertex in deleted:
        mask ^= 1 << vertex
    return leading_hafnian(mask)


def first_jet(offsets: tuple[int, int]):
    p, q = offsets
    values = {
        (i, j): Fraction(0)
        for i in VERTICES
        for j in VERTICES
        if i != j
    }
    for i in VERTICES:
        j = (i + p) % N
        k = (i + q) % N
        values[i, j] = cofactor(i, k)
        values[i, k] = -cofactor(i, j)
    return values


def second_jet(left, right):
    values = {}
    for i, k in combinations(VERTICES, 2):
        pairing = sum(
            (
                left[i, j]
                * right[k, ell]
                * cofactor(i, k, j, ell)
            )
            for j in VERTICES
            if j not in (i, k)
            for ell in VERTICES
            if ell not in (i, k, j)
        )
        values[i, k] = -pairing / cofactor(i, k)
    return values


def scalar_hafnian(weights) -> Fraction:
    return sum(
        reduce(
            lambda answer, selected_edge: answer * weights[selected_edge],
            matching,
            Fraction(1),
        )
        for matching in MATCHINGS
    )


def build_cells(first_jets, second_jets):
    cells = {}
    for u, v in combinations(VERTICES, 2):
        cells[u, v, 0, 0] = LEADING[u, v]
        for color in (1, 2):
            row = first_jets[color]
            cells[u, v, color, 0] = row[u, v]
            cells[u, v, 0, color] = row[v, u]
        for left, right in product((1, 2), repeat=2):
            cells[u, v, left, right] = second_jets[left, right][u, v]
    return cells


def coefficient(cells, coloring: tuple[int, ...]) -> Fraction:
    return sum(
        reduce(
            lambda answer, selected_edge: answer
            * cells.get(
                (
                    selected_edge[0],
                    selected_edge[1],
                    coloring[selected_edge[0]],
                    coloring[selected_edge[1]],
                ),
                Fraction(0),
            ),
            matching,
            Fraction(1),
        )
        for matching in MATCHINGS
    )


def main() -> None:
    assert leading_hafnian(FULL) == 1
    two_hole = {
        edge(i, j): cofactor(i, j) for i, j in combinations(VERTICES, 2)
    }
    assert set(two_hole.values()) == {Fraction(3), Fraction(-5, 3)}
    assert all(two_hole.values())
    for i in VERTICES:
        assert sum(
            LEADING[edge(i, j)] * cofactor(i, j)
            for j in VERTICES
            if j != i
        ) == 1

    first_jets = {1: first_jet((1, 2)), 2: first_jet((1, 3))}
    for color, values in first_jets.items():
        assert any(values.values())
        for i in VERTICES:
            assert sum(
                values[i, j] * cofactor(i, j)
                for j in VERTICES
                if j != i
            ) == 0, (color, i)

    second_jets = {
        (left, right): second_jet(first_jets[left], first_jets[right])
        for left, right in product((1, 2), repeat=2)
    }
    for i, k in combinations(VERTICES, 2):
        for left, right in product((1, 2), repeat=2):
            pairing = sum(
                first_jets[left][i, j]
                * first_jets[right][k, ell]
                * cofactor(i, k, j, ell)
                for j in VERTICES
                if j not in (i, k)
                for ell in VERTICES
                if ell not in (i, k, j)
            )
            assert (
                second_jets[left, right][i, k] * cofactor(i, k)
                + pairing
                == 0
            )

    pure_hafnians = {
        color: scalar_hafnian(second_jets[color, color])
        for color in (1, 2)
    }
    assert pure_hafnians == {
        1: Fraction(-190, 3),
        2: Fraction(250, 3),
    }

    cells = build_cells(first_jets, second_jets)
    spectrum = Counter()
    witnesses = {}
    for coloring in product(range(3), repeat=N):
        value = coefficient(cells, coloring)
        if not value:
            continue
        degree = sum(color != 0 for color in coloring)
        spectrum[degree] += 1
        witnesses.setdefault(degree, (coloring, value))

    # This independently audits every one- and two-hole coefficient, rather
    # than relying only on the closed formulas above.
    assert spectrum[0] == 1
    assert spectrum[1] == spectrum[2] == 0
    assert spectrum == Counter({3: 100, 4: 231, 5: 172, 6: 64, 0: 1})
    assert coefficient(cells, (0, 0, 0, 2, 1, 1)) == -10
    assert coefficient(cells, (1,) * N) == Fraction(-190, 3)
    assert coefficient(cells, (2,) * N) == Fraction(250, 3)

    print(
        "pure color-torus limit: dense haf=1, simultaneous first jets, "
        "degrees 1/2 vanish, pure terminal=(-190/3,250/3), "
        "first mixed degree 3: PASS"
    )


if __name__ == "__main__":
    main()
