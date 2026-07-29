#!/usr/bin/env python3
"""Exact finite audit for live-three-zero-extra-singular-axis-capacity.md."""

from __future__ import annotations

from itertools import combinations_with_replacement


COLORS = frozenset(range(3))
MISSED = tuple(
    frozenset(color for color in COLORS if mask >> color & 1)
    for mask in range(1, 1 << 3)
)


def admissible(extra: tuple[frozenset[int], ...]) -> bool:
    # Base centres: two type-22 sites miss {0,1}; two type-10 sites miss {2}.
    missed = (frozenset({0, 1}),) * 2 + (frozenset({2}),) * 2 + extra
    single = {
        color: sum(color in item for item in missed) for color in COLORS
    }
    pair = {
        (left, right): sum({left, right} <= item for item in missed)
        for left in COLORS
        for right in COLORS
        if left < right
    }
    return all(value <= 3 for value in single.values()) and all(
        value <= 2 for value in pair.values()
    )


def main() -> None:
    admissible_families = []
    for size in range(5):
        for family in combinations_with_replacement(MISSED, size):
            if admissible(family):
                admissible_families.append(family)
                assert size <= 3
                assert all(not {0, 1} <= item for item in family)
                assert all(
                    left.isdisjoint(right)
                    for index, left in enumerate(family)
                    for right in family[index + 1 :]
                )

    maximal = tuple(
        family
        for family in admissible_families
        if not any(
            len(larger) > len(family)
            and all(item in larger for item in family)
            for larger in admissible_families
        )
    )
    assert max(map(len, admissible_families)) == 3
    assert any(
        set(family) == {frozenset({0}), frozenset({1}), frozenset({2})}
        for family in maximal
    )
    print("Live three-zero extra-singular axis capacity: PASS")
    print(f"admissible missed-axis multisets={len(admissible_families)}")
    print("maximum additional nonzero singular sites=3")


if __name__ == "__main__":
    main()
