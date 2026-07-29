#!/usr/bin/env python3
"""Exhaust the contracted two-hole lemma through nine blocks.

The Hamilton path is encoded by its block order x_0,...,x_{m-1}, with
x_0=0.  Odd path edges are O--O chords and even path edges are E--E
chords.  The proof of Lemma 3.2 says that forbidding an E/O interlacing
already leaves only 0,-1,1,-2,2,...; the second Hamilton-cycle condition
is not needed.
"""

from __future__ import annotations

import argparse
import itertools


def interlace(e_edge: tuple[int, int], o_edge: tuple[int, int], m: int) -> bool:
    """Return whether E_aE_b and O_cO_d alternate on the lifted 2m-cycle."""
    a, b = sorted(2 * value for value in e_edge)
    c, d = (2 * value + 1 for value in o_edge)
    return (a < c < b) != (a < d < b)


def admissible(order: tuple[int, ...]) -> bool:
    m = len(order)
    o_edges = [
        (order[index - 1], order[index])
        for index in range(1, m, 2)
    ]
    e_edges = [
        (order[index - 1], order[index])
        for index in range(2, m, 2)
    ]
    return not any(
        interlace(e_edge, o_edge, m)
        for e_edge in e_edges
        for o_edge in o_edges
    )


def zigzag(m: int) -> tuple[int, ...]:
    answer = [0]
    for step in range(1, m):
        radius = (step + 1) // 2
        answer.append((-radius if step % 2 else radius) % m)
    return tuple(answer)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("m", nargs="*", type=int, default=(3, 5, 7, 9))
    args = parser.parse_args()

    for m in args.m:
        if m < 3 or m % 2 == 0:
            raise ValueError("each m must be odd and at least three")
        survivors = []
        for tail in itertools.permutations(range(1, m)):
            order = (0,) + tail
            if admissible(order):
                survivors.append(order)
        expected = zigzag(m)
        assert survivors == [expected], (m, survivors, expected)
        print(f"m={m}: unique order {expected}")


if __name__ == "__main__":
    main()
