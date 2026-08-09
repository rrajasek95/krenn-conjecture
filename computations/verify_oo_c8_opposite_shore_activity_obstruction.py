#!/usr/bin/env python3
"""Exact activity obstruction for the alternating-C8 OO packet.

The two-arm packet in ``verify_oo_doubly_good_two_anchor_counterguard``
has inactive arms.  This checker adds arbitrary endpoint-coloured cells on
the opposite shore and proves that every cell capable of activating an arm
creates a mixed coefficient owned by that cell alone.  Since a matching can
use at most one such new cell, this excludes all 2^54 opposite-shore support
extensions at once (with arbitrary nonzero complex weights).
"""

from collections import Counter, defaultdict
from fractions import Fraction as F
from itertools import combinations, product

import verify_oo_doubly_good_two_anchor_counterguard as base


LEFT = (0, 2, 4, 6)
RIGHT = (1, 3, 5, 7)
ARMS = ((base.P, base.Q), (base.P, base.R))
PURE_WORDS = {tuple([colour] * 8) for colour in base.COLORS}


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def contributions_using_cell(blocks, cell):
    """Return the tensor terms that use the specified new cell.

    ``cell`` has canonical endpoint order.  It is absent from ``blocks``.
    Coefficients returned here omit its symbolic weight, so they are the
    coefficient multiplying that weight.
    """

    u0, v0, i0, j0 = cell
    terms = defaultdict(F)
    physical_use_counts = Counter()
    for matching in base.perfect_matchings(base.VERTICES):
        if (u0, v0) not in matching:
            continue
        choices = []
        for u, v in matching:
            if (u, v) == (u0, v0):
                choices.append(((i0, j0, F(1)),))
                continue
            available = tuple(
                (i, j, value)
                for i in base.COLORS
                for j in base.COLORS
                if (value := base.entry(blocks, u, v, i, j))
            )
            if not available:
                choices = []
                break
            choices.append(available)
        if not choices:
            continue
        physical_use_counts[tuple(matching)] += 1
        for selected in product(*choices):
            word = [None] * 8
            coefficient = F(1)
            for (u, v), (i, j, value) in zip(matching, selected, strict=True):
                word[u], word[v] = i, j
                coefficient *= value
            terms[tuple(word)] += coefficient
    return dict(terms), physical_use_counts


def arm_activity(blocks, cell):
    extended = dict(blocks)
    extended[cell] = F(1)
    return tuple(
        arm
        for arm in ARMS
        if base.supported_cofactor_matchings(extended, arm)
    )


def main():
    blocks = base.build_packet()
    require(
        all(not base.supported_cofactor_matchings(blocks, arm) for arm in ARMS),
        "the base OO arms are no longer inactive",
    )

    cells = tuple(
        base.key(u, v, i, j)
        for u, v in combinations(RIGHT, 2)
        for i in base.COLORS
        for j in base.COLORS
    )
    require(len(cells) == 54 and len(set(cells)) == 54, "right-shore cell census changed")

    word_owners = defaultdict(list)
    activity_census = Counter()
    term_census = Counter()
    productive = set()
    active = set()
    for cell in cells:
        terms, matching_uses = contributions_using_cell(blocks, cell)
        activity = arm_activity(blocks, cell)
        activity_census[activity] += 1
        term_census[len(terms)] += 1
        if terms:
            productive.add(cell)
        if activity:
            active.add(cell)
        require(
            all(count == 1 for count in matching_uses.values()),
            f"unexpected duplicate decoration for {cell}",
        )
        require(
            all(coefficient == 1 for coefficient in terms.values()),
            f"non-unit contribution coefficient for {cell}",
        )
        require(
            not (set(terms) & PURE_WORDS),
            f"new cell {cell} contributes a pure target word",
        )
        for word, coefficient in terms.items():
            word_owners[word].append((cell, coefficient))

    require(term_census == Counter({2: 45, 0: 9}), "per-cell term census changed")
    require(len(word_owners) == 90, "global word census changed")
    require(
        all(len(owners) == 1 for owners in word_owners.values()),
        "two opposite-shore cells acquired a common output word",
    )
    require(active <= productive, "an arm-active cell has no tensor contribution")

    expected_activity = Counter(
        {
            (): 9,
            (ARMS[0],): 9,
            (ARMS[1],): 18,
            ARMS: 18,
        }
    )
    require(activity_census == expected_activity, "arm-activity census changed")

    # Shore parity is the global support argument: every full matching uses
    # at most one new RIGHT--RIGHT edge, because the old packet has only the
    # LEFT triangle 02,04,24 and vertex 6 has no LEFT--LEFT neighbour.
    left_internal = {
        tuple(sorted((u, v)))
        for u, v in combinations(LEFT, 2)
        if any(base.entry(blocks, u, v, i, j) for i in base.COLORS for j in base.COLORS)
    }
    require(left_internal == {(0, 2), (0, 4), (2, 4)}, "left triangle changed")
    require(all(6 not in edge for edge in left_internal), "vertex 6 gained a left-shore edge")

    print("alternating-C8 opposite-shore activity obstruction: PASS")
    print("candidate cells=54; productive=45; inert=9; contribution words=90")
    print("per-cell term census: 45 cells x2 mixed words, 9 cells x0")
    print("activity census: neither=9, pq-only=9, pr-only=18, both=18")
    print("all 90 mixed words have one cell owner and coefficient +1")
    print("therefore every arm-activating support extension has a mixed singleton")


if __name__ == "__main__":
    main()
