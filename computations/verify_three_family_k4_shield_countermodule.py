#!/usr/bin/env python3
"""Exact audit of the order-eight simultaneous K4-shield countermodule."""

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


def add_common_entries(weights) -> None:
    for u, v in combinations(range(4), 2):
        weights[u, v] = Fraction(-2 if (u, v) == (0, 1) else 1)
    weights[4, 5] = Fraction(1)
    weights[6, 7] = Fraction(1)


def add_columns(weights, outside_vertices, columns) -> None:
    for outside, column in zip(outside_vertices, columns):
        for inside, value in enumerate(column):
            weights[edge(inside, outside)] = value


def matrices():
    x = (Fraction(1), Fraction(1), Fraction(0), Fraction(-1, 2))
    y = (Fraction(1), Fraction(0), Fraction(1), Fraction(1))
    p = (Fraction(1), Fraction(2), Fraction(1, 2), Fraction(1, 2))
    q = (Fraction(0), Fraction(2), Fraction(-1), Fraction(-1))

    color_zero = blank_matrix()
    add_common_entries(color_zero)
    add_columns(color_zero, (4, 5), (x, x))
    add_columns(color_zero, (6, 7), (y, y))

    def shield(target_pair, other_pair):
        weights = blank_matrix()
        add_common_entries(weights)
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
        Fraction(2),
        Fraction(30),
        Fraction(30),
    )
    for hafnian in hafnians:
        assert hafnian(S) == 0
        assert hafnian(S | A) == 0
        assert hafnian(S | B) == 0
    assert hafnians[1](A) == 1
    assert hafnians[2](B) == 1

    for u, v in combinations(range(4), 2):
        selected_pair = (1 << u) | (1 << v)
        assert hafnians[1](A | selected_pair) == 0
        assert hafnians[2](B | selected_pair) == 0

    # Independently check both recurrence-support implications everywhere.
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

    # Every coloring constant on each coarse block S,A,B fails unless it is
    # one of the three excluded globally constant colorings.
    for block_colors in product(range(3), repeat=3):
        coloring = (
            (block_colors[0],) * 4
            + (block_colors[1],) * 2
            + (block_colors[2],) * 2
        )
        if len(set(coloring)) == 1:
            continue
        masks = masks_of_coloring(coloring)
        assert not all(hafnians[color](masks[color]) for color in range(3))

    feasible_colorings = []
    for coloring in product(range(3), repeat=N):
        masks = masks_of_coloring(coloring)
        if any(mask.bit_count() % 2 for mask in masks) or FULL in masks:
            continue
        values = tuple(hafnians[color](masks[color]) for color in range(3))
        if all(values):
            feasible_colorings.append((coloring, masks, values))
    assert len(feasible_colorings) == 955

    witness_coloring = (0, 0, 0, 0, 0, 1, 0, 1)
    witness_masks = masks_of_coloring(witness_coloring)
    assert witness_masks == (95, 160, 0)
    assert tuple(
        hafnians[color](witness_masks[color]) for color in range(3)
    ) == (Fraction(11, 2), Fraction(1), Fraction(1))

    print(
        "three-family K4 shields: full=(2,30,30), all coarse repairs zero, "
        "955 transversal feasible colorings: PASS"
    )


if __name__ == "__main__":
    main()
