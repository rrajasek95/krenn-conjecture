#!/usr/bin/env python3
"""Exact orbit-product and unary-reduction cost census for sparse R8'."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import product
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
T2_PATH = HERE / "audit_orbit0_t2_pivot_setup.py"
SPEC = importlib.util.spec_from_file_location("orbit0_t2_cost", T2_PATH)
T2 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(T2)
INPUT = HERE / "results_orbit0_cutoff9_sparse_r8.json"
OUT = HERE / "results_orbit0_cutoff9_sparse_r8_square_cost.json"
GROUP_ORDER = 2304

ANCHOR_BIT = {cell: bit for bit, cell in enumerate(sorted(T2.ANCHORS))}
PAIR_INDEX = {edge: index for index, edge in enumerate(T2.M0)}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def cycle_type(permutation):
    unseen = set(range(len(permutation)))
    lengths = []
    while unseen:
        current = min(unseen)
        length = 0
        while current in unseen:
            unseen.remove(current)
            length += 1
            current = permutation[current]
        lengths.append(length)
    return tuple(sorted(lengths, reverse=True))


def conjugacy_key(action):
    sites, colours = T2.ACTIONS[action]
    pair_permutation = []
    flips = []
    for pair in range(4):
        left_image = sites[2 * pair]
        right_image = sites[2 * pair + 1]
        require(left_image // 2 == right_image // 2,
                "action does not preserve physical pairs")
        pair_permutation.append(left_image // 2)
        flips.append(left_image % 2)
    unseen = set(range(4))
    positive, negative = [], []
    while unseen:
        current = min(unseen)
        length = 0
        sign = 0
        while current in unseen:
            unseen.remove(current)
            length += 1
            sign ^= flips[current]
            current = pair_permutation[current]
        (negative if sign else positive).append(length)
    return (tuple(sorted(positive, reverse=True)),
            tuple(sorted(negative, reverse=True)), cycle_type(colours))


def anchor_pattern(row):
    masks = [0, 0, 0, 0]
    for cell_id in row:
        if cell_id not in ANCHOR_BIT:
            continue
        u, v, a, b = T2.BASE.CELLS[cell_id]
        require(a == b, "orbit0 anchor is not diagonal")
        masks[PAIR_INDEX[(u, v)]] |= 1 << a
    return tuple(masks)


def divisor_assignments(pattern):
    answer = []
    for assignment in product(T2.BASE.COLORS, repeat=4):
        if (len(set(assignment)) > 1
                and all(pattern[pair] & (1 << colour)
                        for pair, colour in enumerate(assignment))):
            answer.append(assignment)
    return tuple(answer)


DIVISORS = {pattern: divisor_assignments(pattern)
            for pattern in product(range(8), repeat=4)}


def category(row):
    pattern = anchor_pattern(row)
    if DIVISORS[pattern]:
        return "unary_reducible"
    if any(mask == 0 for mask in pattern):
        return "survivor_missing_physical_pair"
    return "survivor_only_one_pure_assignment"


def main():
    raw = json.loads(INPUT.read_text())
    rows = tuple(bytes.fromhex(item[0]) for item in raw["residual"])
    masses = tuple(Fraction(item[1], item[2]) for item in raw["residual"])
    require(len(rows) == 120, "sparse residual row count changed")

    class_keys = tuple(conjugacy_key(action) for action in range(GROUP_ORDER))
    class_sizes = Counter(class_keys)
    require(len(class_sizes) == 60, "conjugacy class count changed")
    stabilizers, characters, orbits, sizes = [], [], [], []
    for row in rows:
        stabilizer = tuple(action for action in range(GROUP_ORDER)
                           if T2.move_row(row, T2.TRANSFORMS[action]) == row)
        orbit = T2.row_orbit(row)
        require(len(stabilizer) * len(orbit) == GROUP_ORDER,
                "orbit-stabilizer failed")
        intersections = Counter(class_keys[action] for action in stabilizer)
        character = {}
        for key, class_size in class_sizes.items():
            value = Fraction(GROUP_ORDER, class_size) * intersections[key] / len(stabilizer)
            require(value.denominator == 1, "nonintegral permutation character")
            character[key] = value.numerator
        stabilizers.append(stabilizer)
        characters.append(character)
        orbits.append(orbit)
        sizes.append(len(orbit))

    pair_histogram = Counter()
    total_blocks = 0
    min_relative_candidates = 0
    max_relative_candidates = 0
    unary_relative = Counter()
    unary_blocks = Counter()
    unary_weighted_mass = Counter()
    controls = []
    for left in range(len(rows)):
        for right in range(left, len(rows)):
            blocks = sum(class_sizes[key] * characters[left][key] * characters[right][key]
                         for key in class_sizes)
            require(blocks % GROUP_ORDER == 0, "nonintegral double-coset count")
            blocks //= GROUP_ORDER
            pair_histogram[blocks] += 1
            total_blocks += blocks
            min_relative_candidates += min(sizes[left], sizes[right])
            max_relative_candidates += max(sizes[left], sizes[right])

            # Enumerate the smaller labelled orbit and partition it by the
            # stabilizer of the fixed representative.  These are literal
            # H_fixed\G/H_enumerated double-coset blocks.
            if sizes[left] >= sizes[right]:
                fixed, enumerated = left, right
            else:
                fixed, enumerated = right, left
            fixed_row = rows[fixed]
            enumerated_set = set(orbits[enumerated])
            unseen = set(enumerated_set)
            local_blocks = Counter()
            local_relative = Counter()
            symmetry = 1 if left == right else 2
            coefficient_per_relative = (symmetry * masses[fixed]
                                        * masses[enumerated] / sizes[enumerated])
            while unseen:
                seed = min(unseen)
                block = {T2.move_row(seed, T2.TRANSFORMS[action])
                         for action in stabilizers[fixed]}
                block &= enumerated_set
                require(block and block <= unseen,
                        "double-coset partition overlapped a previous block")
                joined = bytes(sorted(fixed_row + seed))
                kind = category(joined)
                require(all(category(bytes(sorted(fixed_row + item))) == kind
                            for item in block),
                        "unary category is not constant on a double-coset block")
                local_blocks[kind] += 1
                local_relative[kind] += len(block)
                unary_weighted_mass[kind] += coefficient_per_relative * len(block)
                unseen.difference_update(block)
            require(sum(local_blocks.values()) == blocks,
                    "direct/character double-coset counts differ")
            unary_blocks.update(local_blocks)
            unary_relative.update(local_relative)
            if len(controls) < 8 and any(key.startswith("survivor")
                                         for key in local_blocks):
                controls.append({
                    "pair": [left, right],
                    "sizes": [sizes[left], sizes[right]],
                    "double_cosets": blocks,
                    "block_categories": dict(sorted(local_blocks.items())),
                    "relative_categories": dict(sorted(local_relative.items())),
                })

    require(sum(unary_blocks.values()) == total_blocks,
            "unary block census lost double cosets")
    require(sum(unary_relative.values()) == min_relative_candidates,
            "unary relative census lost candidate rows")
    total_mass = sum(masses)
    require(sum(unary_weighted_mass.values()) == total_mass * total_mass,
            "signed unary mass does not square sparse residual mass")

    result = {
        "status": "UNAUDITED exact sparse-R8 orbit-product/unary cost census",
        "input_sha256": sha256(INPUT.read_bytes()).hexdigest(),
        "input_logical_sha256": raw["result_sha256"],
        "group_order": GROUP_ORDER,
        "conjugacy_classes": len(class_sizes),
        "residual_orbits": len(rows),
        "labelled_support": sum(sizes),
        "unordered_orbit_pairs": len(rows) * (len(rows) + 1) // 2,
        "minimum_relative_product_candidates": min_relative_candidates,
        "maximum_relative_product_candidates": max_relative_candidates,
        "total_double_coset_blocks": total_blocks,
        "double_coset_count_histogram": dict(sorted(pair_histogram.items())),
        "unary_relative_candidate_categories": dict(sorted(unary_relative.items())),
        "unary_double_coset_block_categories": dict(sorted(unary_blocks.items())),
        "unary_signed_weighted_mass": {
            key: [value.numerator, value.denominator]
            for key, value in sorted(unary_weighted_mass.items())
        },
        "signed_square_mass": [(total_mass * total_mass).numerator,
                               (total_mass * total_mass).denominator],
        "direct_partition_controls": controls,
        "scope_guard": (
            "Unary categories are exact on relative rows and double-coset "
            "blocks, but R8' is signed. Coincident canonical product rows must "
            "be collected before declaring nonzero survivor target support; "
            "the census is a work bound, not a membership result."
        ),
        "baseline_301_orbits": {
            "residual_orbits": 301,
            "labelled_support": 453600,
            "unordered_orbit_pairs": 45451,
            "minimum_relative_product_candidates": 48742344,
            "total_double_coset_blocks": 45367466,
            "unary_survivor_relative_candidates": 5642268,
        },
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("sparse R8 square cost census: PASS")
    print("pairs/candidates/blocks:", result["unordered_orbit_pairs"],
          min_relative_candidates, total_blocks)
    print("unary relative:", dict(sorted(unary_relative.items())))
    print("unary blocks:", dict(sorted(unary_blocks.items())))
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
