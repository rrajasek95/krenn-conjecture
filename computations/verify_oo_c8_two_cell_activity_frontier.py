#!/usr/bin/env python3
"""Exact two-cell activity frontier for the alternating-C8 OO packet.

This is the first completion layer outside the opposite-shore obstruction:
one new RIGHT--RIGHT cell is necessary for activity, while a second cell
may lie anywhere.  We retain the two symbolic weights and test the literal
full GHZ tensor equations for a torus monomial unit before any coefficient
elimination.
"""

from collections import Counter, defaultdict
from fractions import Fraction as F
from itertools import combinations, product

import verify_oo_doubly_good_two_anchor_counterguard as base


LEFT = frozenset((0, 2, 4, 6))
RIGHT = frozenset((1, 3, 5, 7))
ARMS = ((base.P, base.Q), (base.P, base.R))


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def physical_pair(cell):
    return cell[:2]


def shore_type(cell):
    endpoints = frozenset(cell[:2])
    if endpoints <= LEFT:
        return "LL"
    if endpoints <= RIGHT:
        return "RR"
    return "LR"


def all_unoccupied_cells(blocks):
    return tuple(
        base.key(u, v, i, j)
        for u, v in combinations(base.VERTICES, 2)
        for i in base.COLORS
        for j in base.COLORS
        if base.key(u, v, i, j) not in blocks
    )


def tensor_polynomials(blocks, added):
    """Return word -> {variable mask: integer coefficient}."""

    added_by_pair = defaultdict(list)
    for index, cell in enumerate(added):
        u, v, i, j = cell
        added_by_pair[(u, v)].append((i, j, 1 << index))

    tensor = defaultdict(lambda: defaultdict(F))
    for matching in base.perfect_matchings(base.VERTICES):
        choices = []
        for u, v in matching:
            available = [
                (i, j, 0, value)
                for i in base.COLORS
                for j in base.COLORS
                if (value := base.entry(blocks, u, v, i, j))
            ]
            available.extend(
                (i, j, mask, F(1))
                for i, j, mask in added_by_pair[(u, v)]
            )
            if not available:
                choices = []
                break
            choices.append(available)
        if not choices:
            continue
        for selected in product(*choices):
            word = [None] * 8
            mask = 0
            coefficient = F(1)
            for (u, v), (i, j, local_mask, value) in zip(
                matching, selected, strict=True
            ):
                word[u], word[v] = i, j
                mask |= local_mask
                coefficient *= value
            tensor[tuple(word)][mask] += coefficient
    return {
        word: {mask: value for mask, value in polynomial.items() if value}
        for word, polynomial in tensor.items()
        if any(polynomial.values())
    }


def target_residuals(tensor):
    words = set(tensor)
    words.update(tuple([colour] * 8) for colour in base.COLORS)
    residuals = {}
    for word in words:
        polynomial = dict(tensor.get(word, {}))
        target = F(1) if len(set(word)) == 1 else F(0)
        polynomial[0] = polynomial.get(0, F(0)) - target
        polynomial = {mask: value for mask, value in polynomial.items() if value}
        if polynomial:
            residuals[word] = polynomial
    return residuals


def cofactor_polynomials(blocks, added, deleted_pair):
    residual = tuple(v for v in base.VERTICES if v not in deleted_pair)
    added_by_pair = defaultdict(list)
    for index, cell in enumerate(added):
        u, v, i, j = cell
        added_by_pair[(u, v)].append((i, j, 1 << index))
    tensor = defaultdict(lambda: defaultdict(F))
    for matching in base.perfect_matchings(residual):
        choices = []
        for u, v in matching:
            available = [
                (i, j, 0, value)
                for i in base.COLORS
                for j in base.COLORS
                if (value := base.entry(blocks, u, v, i, j))
            ]
            available.extend(
                (i, j, mask, F(1))
                for i, j, mask in added_by_pair[(u, v)]
            )
            if not available:
                choices = []
                break
            choices.append(available)
        if not choices:
            continue
        for selected in product(*choices):
            word = [None] * len(residual)
            mask = 0
            coefficient = F(1)
            for position, ((u, v), (i, j, local_mask, value)) in enumerate(
                zip(matching, selected, strict=True)
            ):
                word[residual.index(u)] = i
                word[residual.index(v)] = j
                mask |= local_mask
                coefficient *= value
            tensor[tuple(word)][mask] += coefficient
    return {
        word: {mask: value for mask, value in polynomial.items() if value}
        for word, polynomial in tensor.items()
        if any(polynomial.values())
    }


def is_support_active(blocks, added, arm):
    return bool(cofactor_polynomials(blocks, added, arm))


def main():
    blocks = base.build_packet()
    candidates = all_unoccupied_cells(blocks)
    by_shore = Counter(map(shore_type, candidates))
    require(by_shore == Counter({"LR": 136, "RR": 54, "LL": 51}), "cell census changed")

    pairs = []
    for added in combinations(candidates, 2):
        if not any(shore_type(cell) == "RR" for cell in added):
            continue
        if not all(is_support_active(blocks, added, arm) for arm in ARMS):
            continue
        pairs.append(added)

    # The loop above chooses each unordered pair containing an RR cell once.
    require(len(pairs) == len(set(pairs)), "duplicate two-cell supports")

    disposition = Counter()
    pair_types = Counter()
    unit_row_counts = Counter()
    unit_masks = Counter()
    first_unit = None
    first_survivor = None
    survivor_data = None
    for added in pairs:
        pair_types[tuple(sorted(map(shore_type, added)))] += 1
        residuals = target_residuals(tensor_polynomials(blocks, added))
        unit_rows = tuple(
            (word, polynomial)
            for word, polynomial in residuals.items()
            if len(polynomial) == 1
        )
        if unit_rows:
            disposition["torus_monomial_unit"] += 1
            unit_row_counts[len(unit_rows)] += 1
            unit_masks.update(next(iter(polynomial)) for _, polynomial in unit_rows)
            if first_unit is None:
                first_unit = (added, unit_rows[0])
            continue
        disposition["no_monomial_unit"] += 1
        if first_survivor is None:
            first_survivor = added
            survivor_data = residuals

    print("alternating-C8 two-cell active frontier: PASS")
    print(f"unoccupied cells by shore={dict(sorted(by_shore.items()))}")
    print(f"two-cell supports with both arm cofactors support-active={len(pairs)}")
    print(f"support types={dict(sorted(pair_types.items()))}")
    print(f"full-target disposition={dict(sorted(disposition.items()))}")
    print(f"unit-row-count histogram={dict(sorted(unit_row_counts.items()))}")
    print(f"unit monomial masks={dict(sorted(unit_masks.items()))}")
    if first_survivor is None:
        print("every active two-cell support has a literal torus monomial unit")
        print(f"first replayable unit={first_unit}")
    else:
        print(f"first no-unit support={first_survivor}")
        print(f"residual row count={len(survivor_data)}")

    require(
        pair_types
        == Counter({("LR", "RR"): 2934, ("RR", "RR"): 963, ("LL", "RR"): 918}),
        "active support-type census changed",
    )
    require(
        disposition == Counter({"torus_monomial_unit": 4815}),
        "two-cell target disposition changed",
    )
    require(
        unit_row_counts == Counter({4: 2304, 5: 1800, 3: 567, 6: 144}),
        "unit-row-count histogram changed",
    )


if __name__ == "__main__":
    main()
