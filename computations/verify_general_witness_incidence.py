#!/usr/bin/env python3
"""Exact incidence audit for a general invertible deleted pair at n=8.

For an invertible A_pq, each color has at least two outside zero-cross
witnesses.  The reverse-star and hard-annihilator obstructions now show
that their union has at least five sites.  This script classifies the raw
colorwise incidence multisets, removes the three- and four-site strata, isolates the seven
incidence-minimal subcores, and checks sharp local block models for every
possible witness multiplicity at one site.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations_with_replacement, permutations

import sympy as sp

from verify_witness_incidence_k8_countermodel import K


E = tuple(sp.eye(3)[:, r] for r in range(3))
ZERO = sp.zeros(3, 3)


def permute_mask(mask, permutation):
    out = 0
    for color in range(3):
        if mask & (1 << color):
            out |= 1 << permutation[color]
    return out


def canonical_multiset(masks):
    return min(
        tuple(sorted(permute_mask(mask, permutation) for mask in masks))
        for permutation in permutations(range(3))
    )


def color_degrees(masks):
    return tuple(
        sum(bool(mask & (1 << color)) for mask in masks)
        for color in range(3)
    )


def enumerate_incidence_orbits():
    representatives = set()
    for masks in combinations_with_replacement(range(8), 6):
        if min(color_degrees(masks)) < 2:
            continue
        if sum(mask != 0 for mask in masks) < 3:
            continue
        representatives.add(canonical_multiset(masks))

    assert len(representatives) == 228
    assert Counter(sum(mask != 0 for mask in masks) for masks in representatives) == {
        3: 6,
        4: 23,
        5: 61,
        6: 138,
    }
    assert Counter(sum(mask.bit_count() for mask in masks) for masks in representatives) == {
        6: 7,
        7: 13,
        8: 28,
        9: 36,
        10: 41,
        11: 34,
        12: 30,
        13: 17,
        14: 11,
        15: 6,
        16: 3,
        17: 1,
        18: 1,
    }

    union_three = sorted(
        masks
        for masks in representatives
        if sum(mask != 0 for mask in masks) == 3
    )
    assert union_three == [
        (0, 0, 0, 1, 6, 7),
        (0, 0, 0, 1, 7, 7),
        (0, 0, 0, 3, 5, 6),
        (0, 0, 0, 3, 5, 7),
        (0, 0, 0, 3, 7, 7),
        (0, 0, 0, 7, 7, 7),
    ]

    # Choose exactly two witnesses of each color.  Up to site and color
    # symmetry there are seven minimal incidence cores.
    minimal_cores = sorted(
        masks
        for masks in representatives
        if color_degrees(masks) == (2, 2, 2)
    )
    assert minimal_cores == [
        (0, 0, 0, 1, 6, 7),
        (0, 0, 0, 3, 5, 6),
        (0, 0, 1, 1, 6, 6),
        (0, 0, 1, 2, 4, 7),
        (0, 0, 1, 2, 5, 6),
        (0, 1, 1, 2, 4, 6),
        (1, 1, 2, 2, 4, 4),
    ]

    # The reversed-star theorem eliminates union size three, and the
    # hard-annihilator theorem eliminates union size four.  Thus the strict
    # stratum begins at union size five.
    eliminated_minimum_candidate = (0, 0, 0, 3, 5, 6)
    assert eliminated_minimum_candidate in union_three
    strict_representatives = {
        masks
        for masks in representatives
        if sum(mask != 0 for mask in masks) >= 5
    }
    assert len(strict_representatives) == 199

    # If the full pattern itself has exactly two incidences per color, its
    # The five cores on at most four sites are impossible; two full minimal
    # patterns remain at union size at least five.
    strict_full_minimal = [
        masks
        for masks in minimal_cores
        if sum(mask != 0 for mask in masks) >= 5
    ]
    assert strict_full_minimal == minimal_cores[5:]

    return (
        representatives,
        strict_representatives,
        minimal_cores,
        strict_full_minimal,
        eliminated_minimum_candidate,
    )


def local_blocks_for_mask(mask):
    colors = [color for color in range(3) if mask & (1 << color)]
    if not colors:
        return sp.eye(3), sp.eye(3)
    if len(colors) == 1:
        color = colors[0]
        return E[0] * E[color].T, sp.eye(3)
    if len(colors) == 2:
        first, second = colors
        return E[0] * E[first].T, E[1] * E[second].T
    return E[0] * E[0].T, E[1] * E[0].T


def witness_mask(P, Q):
    mask = 0
    for color in range(3):
        if P * K[color] * Q.T == ZERO:
            mask |= 1 << color
    return mask


def fixed_common_annihilator_dimension(P, Q):
    return 3 - sp.Matrix.vstack(P, Q).rank()


def audit_local_witness_types():
    dimensions = {}
    for mask in range(8):
        P, Q = local_blocks_for_mask(mask)
        assert witness_mask(P, Q) == mask
        dimensions[mask] = fixed_common_annihilator_dimension(P, Q)

    # These sharp models show what incidence alone guarantees in the worst
    # case: no fixed annihilator at an empty or singleton witness site; a
    # coordinate line at an exact double witness; and a plane when both
    # triple-witness blocks share a nonzero row line.
    assert dimensions == {
        0: 0,
        1: 0,
        2: 0,
        3: 1,
        4: 0,
        5: 1,
        6: 1,
        7: 2,
    }

    # A triple witness need not have any fixed annihilator at all: one
    # block may vanish while the other is invertible.
    assert witness_mask(ZERO, sp.eye(3)) == 7
    assert fixed_common_annihilator_dimension(ZERO, sp.eye(3)) == 0

    # At an exact double witness, the fixed line is the missing coordinate.
    for mask in (3, 5, 6):
        P, Q = local_blocks_for_mask(mask)
        missing = next(color for color in range(3) if not mask & (1 << color))
        assert P * E[missing] == sp.zeros(3, 1)
        assert Q * E[missing] == sp.zeros(3, 1)
        assert fixed_common_annihilator_dimension(P, Q) == 1

    return dimensions


def main():
    (
        representatives,
        strict_representatives,
        minimal_cores,
        strict_full_minimal,
        eliminated,
    ) = enumerate_incidence_orbits()
    dimensions = audit_local_witness_types()
    print("classified raw six-site witness incidence orbits", len(representatives))
    print("classified strict union-at-least-five orbits", len(strict_representatives))
    print("classified incidence-minimal subcores", len(minimal_cores))
    print("classified surviving full minimal patterns", len(strict_full_minimal))
    print("recorded the eliminated minimum-union candidate", eliminated)
    print("verified sharp fixed-annihilator dimensions", dimensions)


if __name__ == "__main__":
    main()
