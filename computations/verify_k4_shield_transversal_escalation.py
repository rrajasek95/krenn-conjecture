#!/usr/bin/env python3
"""Audit the escalation from coarse K4 transversals to a pivot cofactor."""

from __future__ import annotations

from fractions import Fraction
from functools import cache
from itertools import combinations, product


N = 8
FULL = (1 << N) - 1
S = sum(1 << vertex for vertex in range(4))
A = (1 << 4) | (1 << 5)
B = (1 << 6) | (1 << 7)


def edge(u: int, v: int) -> tuple[int, int]:
    return (u, v) if u < v else (v, u)


def blank_matrix():
    return {
        selected_edge: Fraction(0)
        for selected_edge in combinations(range(N), 2)
    }


def add_core(weights) -> None:
    for u, v in combinations(range(4), 2):
        weights[u, v] = Fraction(-2 if (u, v) == (0, 1) else 1)


def add_columns(weights, outside_vertices, columns) -> None:
    for outside, column in zip(outside_vertices, columns):
        for inside, value in enumerate(column):
            weights[edge(inside, outside)] = value


def matrices():
    common = (Fraction(1), Fraction(1), Fraction(2), Fraction(5, 2))
    color_zero = blank_matrix()
    add_core(color_zero)
    add_columns(color_zero, (4, 5, 6, 7), (common,) * 4)

    p = (Fraction(1), Fraction(2), Fraction(1, 2), Fraction(1, 2))
    q = (Fraction(0), Fraction(2), Fraction(-1), Fraction(-1))
    y = (Fraction(1), Fraction(0), Fraction(1), Fraction(1))

    def shield(target_pair, other_pair):
        weights = blank_matrix()
        add_core(weights)
        weights[4, 5] = Fraction(1)
        weights[6, 7] = Fraction(1)
        add_columns(weights, target_pair, (p, q))
        add_columns(weights, other_pair, (y, y))
        for left in (4, 5):
            for right in (6, 7):
                weights[left, right] = Fraction(1)
        return weights

    return color_zero, shield((4, 5), (6, 7)), shield((6, 7), (4, 5))


def hafnian_function(weights):
    @cache
    def hafnian(mask: int) -> Fraction:
        if mask == 0:
            return Fraction(1)
        first_bit = mask & -mask
        u = first_bit.bit_length() - 1
        answer = Fraction(0)
        remainder = mask ^ first_bit
        while remainder:
            next_bit = remainder & -remainder
            v = next_bit.bit_length() - 1
            answer += weights[edge(u, v)] * hafnian(
                mask ^ first_bit ^ next_bit
            )
            remainder ^= next_bit
        return answer

    return hafnian


def masks_of_coloring(coloring):
    masks = [0, 0, 0]
    for vertex, color in enumerate(coloring):
        masks[color] |= 1 << vertex
    return tuple(masks)


def main() -> None:
    weights = matrices()
    hafnians = tuple(hafnian_function(matrix) for matrix in weights)
    even_masks = tuple(
        mask for mask in range(1 << N) if mask.bit_count() % 2 == 0
    )

    assert tuple(hafnian(FULL) for hafnian in hafnians) == (
        Fraction(120),
        Fraction(30),
        Fraction(30),
    )
    assert all(hafnian(S) == 0 for hafnian in hafnians)
    assert hafnians[1](A) == 1 and hafnians[2](B) == 1

    for u, v in combinations(range(4), 2):
        selected_pair = (1 << u) | (1 << v)
        assert hafnians[1](A | selected_pair) == 0
        assert hafnians[2](B | selected_pair) == 0

    # Every coarse transversal containing the whole core is canceled.
    for u, v in combinations(range(4, 8), 2):
        assert hafnians[0](S | (1 << u) | (1 << v)) == 0

    # Audit the two support implications of the recurrence at every pivot.
    for color, hafnian in enumerate(hafnians):
        for mask in even_masks:
            if mask.bit_count() < 4:
                continue
            for pivot in range(N):
                if not (mask >> pivot) & 1:
                    continue
                term_count = sum(
                    weights[color][edge(pivot, other)] != 0
                    and hafnian(mask ^ (1 << pivot) ^ (1 << other)) != 0
                    for other in range(N)
                    if other != pivot and (mask >> other) & 1
                )
                if hafnian(mask) != 0:
                    assert term_count >= 1
                else:
                    assert term_count != 1

    pivot_edge = (3, 7)
    complement = FULL ^ (1 << 3) ^ (1 << 7)
    assert complement == 119
    assert weights[0][pivot_edge] == Fraction(5, 2)
    assert hafnians[0](complement) == 12
    assert weights[1][pivot_edge] == 1
    assert hafnians[1]((1 << 3) | (1 << 7)) == 1

    feasible_colorings = []
    for coloring in product(range(3), repeat=N):
        masks = masks_of_coloring(coloring)
        if any(mask.bit_count() % 2 for mask in masks) or FULL in masks:
            continue
        values = tuple(hafnians[color](masks[color]) for color in range(3))
        if all(values):
            feasible_colorings.append((coloring, masks, values))
    assert len(feasible_colorings) == 924

    witness = (0, 0, 0, 1, 0, 0, 0, 1)
    witness_masks = masks_of_coloring(witness)
    assert witness_masks == (119, 136, 0)
    assert tuple(
        hafnians[color](witness_masks[color]) for color in range(3)
    ) == (Fraction(12), Fraction(1), Fraction(1))

    print(
        "K4 shield escalation: all S+outside-pair cofactors zero, "
        "pivot cover 119|136|0=(12,1,1), 924 covers: PASS"
    )


if __name__ == "__main__":
    main()
