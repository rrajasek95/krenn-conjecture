#!/usr/bin/env python3
"""Exact minimal X1-anchor/activity audit for the alternating-C8 OO chart."""

from collections import Counter

import verify_oo_c8_two_cell_activity_frontier as frontier
import verify_oo_doubly_good_two_anchor_counterguard as base


PURE_ONE = (1,) * 8
BASE_ONE_EDGES = ((0, 4), (2, 4))


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def minimal_anchor_completions(blocks):
    completions = set()
    for anchor in BASE_ONE_EDGES:
        require(base.entry(blocks, *anchor, 1, 1) == 1, f"missing base X1 edge {anchor}")
        residual = tuple(vertex for vertex in base.VERTICES if vertex not in anchor)
        for matching in base.perfect_matchings(residual):
            cells = tuple(sorted(base.key(u, v, 1, 1) for u, v in matching))
            require(all(cell not in blocks for cell in cells), "completion reused an old cell")
            completions.add(cells)
    return tuple(sorted(completions))


def main():
    blocks = base.build_packet()
    completions = minimal_anchor_completions(blocks)
    require(len(completions) == 30, "minimal X1 completion census changed")

    activity = Counter()
    support_types = Counter()
    both_active_types = Counter()
    disposition = Counter()
    unit_histogram = Counter()
    first_active_unit = None
    for added in completions:
        support_type = tuple(sorted(frontier.shore_type(cell) for cell in added))
        support_types[support_type] += 1
        active_arms = tuple(
            arm
            for arm in frontier.ARMS
            if frontier.is_support_active(blocks, added, arm)
        )
        activity[active_arms] += 1
        if active_arms == frontier.ARMS:
            both_active_types[support_type] += 1

        tensor = frontier.tensor_polynomials(blocks, added)
        residuals = frontier.target_residuals(tensor)
        require(
            residuals.get(PURE_ONE) == {0: -1, 7: 1},
            f"third-anchor equation changed for {added}",
        )
        unit_rows = tuple(
            (word, polynomial)
            for word, polynomial in residuals.items()
            if len(polynomial) == 1
        )
        unit_histogram[len(unit_rows)] += 1
        if unit_rows:
            disposition["torus_monomial_unit"] += 1
            if active_arms == frontier.ARMS and first_active_unit is None:
                first_active_unit = (added, unit_rows[0])
        else:
            disposition["no_monomial_unit"] += 1

    both_active = activity[frontier.ARMS]
    require(
        support_types == Counter({("LR", "LR", "RR"): 24, ("LL", "RR", "RR"): 6}),
        "completion shore-type census changed",
    )
    require(
        activity
        == Counter({frontier.ARMS: 19, (frontier.ARMS[1],): 8, (frontier.ARMS[0],): 3}),
        "arm-activity census changed",
    )
    require(
        both_active_types
        == Counter({("LR", "LR", "RR"): 14, ("LL", "RR", "RR"): 5}),
        "both-active shore-type census changed",
    )
    require(both_active == 19, "both-active completion count changed")
    require(
        disposition["torus_monomial_unit"] == len(completions),
        "a minimal third-anchor completion survived the monomial-unit test",
    )
    require(first_active_unit is not None, "missing replayable active unit")
    require(
        unit_histogram == Counter({7: 8, 5: 8, 6: 5, 4: 4, 8: 4, 3: 1}),
        "unit-row histogram changed",
    )

    print("alternating-C8 minimal third-anchor activity audit: PASS")
    print(f"minimal X1 completions={len(completions)}")
    print(f"completion shore types={dict(sorted(support_types.items()))}")
    print(f"arm-activity census={dict(sorted(activity.items(), key=str))}")
    print(f"both-active shore types={dict(sorted(both_active_types.items()))}")
    print(f"full-target disposition={dict(sorted(disposition.items()))}")
    print(f"unit-row-count histogram={dict(sorted(unit_histogram.items()))}")
    print(f"first active replayable unit={first_active_unit}")


if __name__ == "__main__":
    main()
