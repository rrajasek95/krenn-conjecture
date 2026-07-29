#!/usr/bin/env python3
"""Exact audit of the cyclic-character ansatz for the K_{5,5} tensor.

No floating-point cyclotomic arithmetic is used.  A sum of fifth roots is
recorded by its five integer multiplicities.  The mixed coefficient exhibited
below has multiplicities (40,20,20,20,20), hence equals 20 exactly.
"""

from __future__ import annotations

import itertools


MODULUS = 5
PERMUTATIONS = tuple(itertools.permutations(range(MODULUS)))


def inverse(permutation: tuple[int, ...]) -> tuple[int, ...]:
    answer = [0] * MODULUS
    for source, target in enumerate(permutation):
        answer[target] = source
    return tuple(answer)


def phase_histogram(right_characters: tuple[int, ...]) -> tuple[int, ...]:
    """Histogram of sum_j q_j(sigma^{-1}(j)-j) modulo five."""
    counts = [0] * MODULUS
    for permutation in PERMUTATIONS:
        permutation_inverse = inverse(permutation)
        phase = sum(
            right_characters[j] * (permutation_inverse[j] - j)
            for j in range(MODULUS)
        )
        counts[phase % MODULUS] += 1
    return tuple(counts)


def affine_normalization(character_set: frozenset[int]) -> tuple[int, int]:
    """Find ax+b carrying a three-set of F_5 to {0,1,2}."""
    target = frozenset((0, 1, 2))
    for multiplier in range(1, MODULUS):
        for shift in range(MODULUS):
            image = frozenset(
                (multiplier * value + shift) % MODULUS
                for value in character_set
            )
            if image == target:
                return multiplier, shift
    raise AssertionError("the affine group should be transitive on three-sets")


def verify_all_character_triples() -> None:
    # At right vertices 0,...,4, use normalized character values 0,0,2,1,2.
    # The weighted position sum is zero, making the exact coefficient rational.
    normalized_pattern = (0, 0, 2, 1, 2)
    expected = (40, 20, 20, 20, 20)
    assert phase_histogram(normalized_pattern) == expected

    # Every three distinct characters are an affine image of {0,1,2}.  Pull
    # the same mixed coloring back to the given three output-color labels and
    # check that its fifth-root sum is still nonzero.  Affine scaling may
    # permute the four light bins, while translation cancels identically.
    for ordered_characters in itertools.permutations(range(MODULUS), 3):
        multiplier, shift = affine_normalization(frozenset(ordered_characters))
        color_for_normalized_character = {}
        for color, character in enumerate(ordered_characters):
            normalized = (multiplier * character + shift) % MODULUS
            color_for_normalized_character[normalized] = color
        color_pattern = tuple(
            color_for_normalized_character[value]
            for value in normalized_pattern
        )
        pulled_back_characters = tuple(
            ordered_characters[color] for color in color_pattern
        )
        histogram = phase_histogram(pulled_back_characters)
        # In Q[zeta_5], a nonnegative sum vanishes iff all five bins agree:
        # Phi_5(x)=1+x+x^2+x^3+x^4 is the minimal polynomial.
        assert len(set(histogram)) > 1
        assert histogram == expected


def main() -> None:
    verify_all_character_triples()
    print("K5,5 cyclic-character obstruction verified exactly")
    print("base mixed phase histogram: (40, 20, 20, 20, 20), value: 20")
    print("all 60 ordered triples of distinct F_5 characters audited")


if __name__ == "__main__":
    main()
