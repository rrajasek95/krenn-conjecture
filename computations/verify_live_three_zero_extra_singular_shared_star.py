#!/usr/bin/env python3
"""Audit the extra-singular shared-star incidence reduction."""

from __future__ import annotations

from itertools import combinations


COLOURS = frozenset(range(3))
BASE_22_COVER = frozenset({2})
ALLOWED_MISSED = (
    frozenset({0}),
    frozenset({1}),
    frozenset({2}),
    frozenset({0, 2}),
    frozenset({1, 2}),
)


def admissible(family: tuple[frozenset[int], ...]) -> bool:
    return all(left.isdisjoint(right) for left, right in combinations(family, 2))


def main() -> None:
    families: list[tuple[frozenset[int], ...]] = []
    for size in range(4):
        for family in combinations(ALLOWED_MISSED, size):
            if admissible(family):
                families.append(family)

    for family in families:
        unresolved = [missed for missed in family if missed == frozenset({2})]
        assert len(unresolved) <= 1
        for missed in family:
            if missed == frozenset({2}):
                continue
            binary_missed = missed & frozenset({0, 1})
            assert binary_missed
            assert len(binary_missed) == 1
            cover = BASE_22_COVER | (COLOURS - missed)
            assert len(cover) == 2
            assert COLOURS - cover == binary_missed

    print("Live three-zero extra-singular shared-star reduction: PASS")
    print(f"admissible labelled-free families={len(families)}")
    print("unresolved rank-three rescue types per family<=1")


if __name__ == "__main__":
    main()
