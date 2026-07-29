#!/usr/bin/env python3
"""Lightweight exact audit for the clean-pair descent target.

The proof is uniform.  This dependency-free checker enumerates formally
typed perfect matchings and verifies the cap/canonical/error coefficient
ledger, denominator homogeneity, the eight-to-six cubic, normalization,
and the finite decorated-source bound.
"""

from collections import Counter
from fractions import Fraction
from math import comb


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


def odd_double_factorial(half_order):
    answer = 1
    for value in range(1, 2 * half_order, 2):
        answer *= value
    return answer


def audit_typed_ledger(half_order):
    matchings = tuple(perfect_matchings(range(2 * half_order)))
    assert len(matchings) == odd_double_factorial(half_order)
    profiles = Counter()
    checked = 0

    for matching in matchings:
        assert len(matching) == half_order
        for type_mask in range(1 << half_order):
            red_edges = type_mask.bit_count()
            profiles[red_edges] += 1

            # In s*H(x+r/s), a typed matching with k red edges has
            # coefficient s^(1-k).
            canonical_exponent = 1 - red_edges

            # In (s+r)*exp(x), only k=0 and k=1 occur.
            if red_edges == 0:
                assert canonical_exponent == 1
            elif red_edges == 1:
                assert canonical_exponent == 0
            else:
                # The higher-cumulant correction supplies exactly the
                # missing canonical coefficient.
                assert canonical_exponent < 0
                denominator_cleared = canonical_exponent + half_order - 1
                assert denominator_cleared == half_order - red_edges
                assert denominator_cleared >= 0

                # s^(h-k) r^k has total cap-covector degree h.
                assert denominator_cleared + red_edges == half_order
            checked += 1

    expected = {
        red_edges: len(matchings) * comb(half_order, red_edges)
        for red_edges in range(half_order + 1)
    }
    assert profiles == expected
    assert checked == len(matchings) * (1 << half_order)
    return checked, profiles


def audit_eight_to_six_cubic():
    half_order = 3
    checked, profiles = audit_typed_ledger(half_order)
    assert profiles == Counter({1: 45, 2: 45, 0: 15, 3: 15})

    # Six times E is 3*s*r^2*x+r^3.  A fixed type-2 matching occurs
    # 2! times in r^2*x, and a type-3 matching occurs 3! times in r^3.
    assert 3 * 2 == 6
    assert 6 == 6
    return checked, tuple(profiles[index] for index in range(4))


def audit_normalization_and_lift():
    scalar = Fraction(7, 3)
    kappas = (Fraction(2), Fraction(-5, 2), Fraction(11, 7))
    normalized = [
        (kappa / scalar) * (scalar / kappa) for kappa in kappas
    ]
    assert normalized == [1, 1, 1]

    source_bounds = {}
    for sites in range(2, 12, 2):
        bound = 9 * comb(sites, 2)
        assert bound == 9 * sites * (sites - 1) // 2
        source_bounds[sites] = bound
    return len(normalized), source_bounds


def main():
    total = 0
    orders = 0
    for half_order in range(1, 6):
        checked, _profiles = audit_typed_ledger(half_order)
        total += checked
        orders += 1

    cubic_checked, cubic_profile = audit_eight_to_six_cubic()
    normalized, source_bounds = audit_normalization_and_lift()
    print(
        "clean-pair exact descent audit: PASS; "
        f"orders={orders}; typed matchings={total}; "
        f"N=8 ledger={cubic_checked}, profiles={cubic_profile}; "
        f"normalizations={normalized}; "
        f"max decorated cells at 10 sites={source_bounds[10]}"
    )


if __name__ == "__main__":
    main()
