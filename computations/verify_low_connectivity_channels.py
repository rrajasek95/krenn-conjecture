#!/usr/bin/env python3
"""Exact finite audit for the low-connectivity support obstructions."""

from __future__ import annotations

from fractions import Fraction
from itertools import product


def valid_separator_channels(side_parity: int, has_ab: bool):
    """Return terminal destinations compatible with parity on X and Y.

    A destination is ``X``, ``Y``, or the pair ``AB`` denoting that the
    separator edge is used.  When AB is used it occupies both terminals.
    Otherwise the tuple records the destinations of a and b.
    """
    channels: list[tuple[str, ...]] = []
    if has_ab and side_parity == 0:
        channels.append(("AB",))
    for destination_a, destination_b in product(("X", "Y"), repeat=2):
        used_x = (destination_a == "X") + (destination_b == "X")
        used_y = 2 - used_x
        # Removing the vertices paired to terminals must leave even sides.
        if used_x % 2 == side_parity and used_y % 2 == side_parity:
            channels.append((destination_a, destination_b))
    return tuple(channels)


def orthogonal_witness(alpha: tuple[Fraction, Fraction, Fraction]):
    support = [index for index, value in enumerate(alpha) if value]
    if len(support) >= 2:
        i, j = support[:2]
        beta = [Fraction(0)] * 3
        beta[i] = alpha[j]
        beta[j] = -alpha[i]
    else:
        free = [index for index in range(3) if index not in support]
        beta = [Fraction(0)] * 3
        beta[free[0]] = 1
        beta[free[1]] = 1
    beta_tuple = tuple(beta)
    assert sum(x * y for x, y in zip(alpha, beta_tuple)) == 0
    assert sum(value != 0 for value in beta_tuple) >= 2
    return beta_tuple


def verify_covector_cases() -> None:
    # Support patterns and unequal rational magnitudes cover every branch in
    # the explicit construction; no numerical rank decision is used.
    for alpha in product((Fraction(0), Fraction(1), Fraction(2)), repeat=3):
        orthogonal_witness(alpha)


def three_separator_channels():
    """Channels for odd X, even Y behind three terminals."""
    channels: list[tuple[str, ...]] = []
    # No separator edge: each terminal enters X or Y.  X receives an odd
    # number and Y an even number.
    for destinations in product(("X", "Y"), repeat=3):
        if destinations.count("X") % 2 == 1:
            channels.append(destinations)
    # One separator edge consumes a pair; parity forces the remaining
    # terminal into X.
    for unmatched in range(3):
        pair = tuple(index for index in range(3) if index != unmatched)
        channels.append((f"X:{unmatched}", f"S:{pair[0]}-{pair[1]}"))
    return tuple(channels)


def main() -> None:
    assert valid_separator_channels(1, False) == (("X", "Y"), ("Y", "X"))
    assert valid_separator_channels(1, True) == (("X", "Y"), ("Y", "X"))
    assert valid_separator_channels(0, False) == (("X", "X"), ("Y", "Y"))
    assert valid_separator_channels(0, True) == (
        ("AB",),
        ("X", "X"),
        ("Y", "Y"),
    )
    channels3 = three_separator_channels()
    assert len(channels3) == 7
    assert channels3[:4] == (
        ("X", "X", "X"),
        ("X", "Y", "Y"),
        ("Y", "X", "Y"),
        ("Y", "Y", "X"),
    )
    verify_covector_cases()
    print("degree-two orthogonal-covector cases verified exactly")
    print("2-separator channels: odd=2; even=2 without ab, 3 with ab")
    print("3-separator channels: XXX + 3 XYY + 3 internal-pair/X")


if __name__ == "__main__":
    main()
