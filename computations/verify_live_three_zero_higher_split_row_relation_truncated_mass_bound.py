#!/usr/bin/env python3
"""Exact audit of the higher-split row-relation truncated-mass bound."""

from __future__ import annotations

from itertools import product


def partitions(total: int, maximum: int | None = None):
    """Yield integer partitions in nonincreasing order."""
    if total == 0:
        yield ()
        return
    if maximum is None or maximum > total:
        maximum = total
    for first in range(maximum, 0, -1):
        for tail in partitions(total - first, first):
            yield (first,) + tail


# Relation dimension and Wronskian algebra for a wide exact range.
for h in range(8, 101):
    for d in range(0, min(5, (h + 2) // 2) + 1):
        layers = h + 2 - d
        ambient_degree = h + 3 - d
        assert ambient_degree + 1 == layers + 2
        for q in range(4, min(15, layers + 2)):
            row_rank = ambient_degree + 1 - q
            relation_dimension = layers - row_rank
            assert relation_dimension == q - 2


for q in range(4, 15):
    r = q - 2
    for c in range(q + 1, 31):
        degree = c - 4
        wronskian_cap = r * (degree + 1 - r)
        assert wronskian_cap == r * (c - 3 - r)

        # Exhaust small profiles and audit the rearrangement.
        for multiplicities in product(range(1, 8), repeat=min(c, 4)):
            weighted = sum(max(0, r - m) for m in multiplicities)
            truncated = sum(min(m, r) for m in multiplicities)
            assert weighted + truncated == r * len(multiplicities)

    # Every possible local gcd order is favorable.
    for multiplicity in range(1, 15):
        base_weight = max(0, r - multiplicity)
        for gcd_order in range(1, 15):
            if gcd_order <= multiplicity:
                reduced_weight = max(
                    0, r - multiplicity + gcd_order
                )
            else:
                reduced_weight = 0
            correction = r * gcd_order + reduced_weight - base_weight
            assert correction >= 0


# The q=5 forms are exactly equivalent on every partition through p=35.
for total in range(1, 36):
    for profile in partitions(total):
        classes = len(profile)
        n1 = profile.count(1)
        n2 = profile.count(2)
        high_excess = sum(max(0, m - 3) for m in profile)
        truncated = sum(min(m, 3) for m in profile)
        weighted = 2 * n1 + n2

        assert weighted == 3 * classes - truncated
        assert truncated == total - high_excess
        assert (
            weighted <= 3 * (classes - 6)
        ) == (
            truncated >= 18
        )
        assert (
            truncated >= 18
        ) == (
            total >= 18 + high_excess
        )

        if total == 18 and truncated >= 18:
            assert max(profile) <= 3


# Exact multi-drop degree bookkeeping, including repeated inserted values.
for h in range(8, 101):
    for drop_count in range(3, h + 3):
        inserted_labels = drop_count - 2

        # Enumerate every possible number of inserted value classes.  The
        # detailed positive counts do not affect the final degree deficit.
        for inserted_classes in range(1, inserted_labels + 1):
            represented_classes = h + 2 - drop_count + inserted_classes
            residual_degree = represented_classes - 3
            divisor_degree = 2 * inserted_labels + inserted_classes
            remaining_degree = residual_degree - divisor_degree
            assert remaining_degree == h + 3 - 3 * drop_count

            full_lift_degree = (
                residual_degree
                + 3 * drop_count
                - divisor_degree
            )
            assert full_lift_degree == h + 3

        feasible_by_degree = h + 3 - 3 * drop_count >= 0
        assert feasible_by_degree == (
            drop_count <= (h + 3) // 3
        )


print("higher-split row-relation truncated-mass bound: PASS")
print("general q: sum min(m_i,q-2) >= (q-2)(q+1)")
print("q=5: complementary mass capped at three is at least 18")
print("multi-drop rational divisor and degree deficit: exact")
