#!/usr/bin/env python3
"""Count the unary gr16 reductions on R8^2 without expanding its monomials.

For a word constant on each of the four orbit-0 physical anchor pairs, H_w
has a unique K-degree-zero term: the four matching anchor cells.  The three
mixed pair-colour partitions (3,1), (2,2), and (2,1,1) are precisely the
word orbits 00000011, 00001111, and 00001122.  A degree-16 multiplier times
this leading term is therefore a unary associated-graded source column.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import argparse
import importlib.util
from itertools import product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
BRIDGE = HERE.parent / "unaudited-codex-n8-dangerous-chart-bridge-2026-08-20"
EXPORT_PATH = BRIDGE / "export_orbit0_cutoff_seed.py"
SPEC = importlib.util.spec_from_file_location("orbit0_export", EXPORT_PATH)
EXPORT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(EXPORT)
BASE = EXPORT.BASE
R8_PATH = BRIDGE / "results_orbit0_cutoff8_leading_residual.json"
OUT = HERE / "results_r8_square_unary_packet_reduction.json"


ANCHOR_BIT = {cell: bit for bit, cell in enumerate(sorted(EXPORT.ANCHORS))}
PAIR_INDEX = {edge: index for index, edge in enumerate(EXPORT.M0)}


def require(condition: bool, detail: str) -> None:
    if not condition:
        raise RuntimeError(detail)


def anchor_pattern(row):
    masks = [0, 0, 0, 0]
    for cell_id in row:
        if cell_id not in ANCHOR_BIT:
            continue
        u, v, a, b = BASE.CELLS[cell_id]
        require(a == b, "orbit0 anchor cell is not diagonal-colour")
        masks[PAIR_INDEX[(u, v)]] |= 1 << a
    return tuple(masks)


def mixed_assignment_profile(assignment):
    counts = sorted(Counter(assignment).values(), reverse=True)
    return tuple(counts)


def divisors(pattern):
    profiles = Counter()
    for assignment in product(BASE.COLORS, repeat=4):
        if all(pattern[pair] & (1 << colour)
               for pair, colour in enumerate(assignment)):
            profile = mixed_assignment_profile(assignment)
            if profile != (4,):
                profiles[profile] += 1
    return profiles


DIVISORS = {pattern: divisors(pattern)
            for pattern in product(range(8), repeat=4)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--residual", type=Path, default=R8_PATH)
    parser.add_argument("--output", type=Path, default=OUT)
    args = parser.parse_args()
    residual_path = args.residual.resolve()
    raw = json.loads(residual_path.read_text())
    orbits = []
    labelled_rows = 0
    labelled_coefficient_mass = Fraction(0)
    for row_hex, numerator, denominator in raw["residual"]:
        representative = bytes.fromhex(row_hex)
        orbit = tuple(EXPORT.row_orbit(representative))
        quotient_mass = Fraction(numerator, denominator)
        actual_coefficient = quotient_mass / len(orbit)
        pattern_histogram = Counter(anchor_pattern(row) for row in orbit)
        orbits.append((representative, len(orbit), pattern_histogram,
                       actual_coefficient))
        labelled_rows += len(orbit)
        labelled_coefficient_mass += quotient_mass

    category_ordered_pairs = Counter()
    category_weighted_mass = Counter()
    divisor_count_histogram = Counter()
    divisor_profile_presence = Counter()
    orbit_pair_census = []
    for left_index, (left, left_orbit_size, _left_patterns,
                     left_coefficient) in enumerate(orbits):
        left_pattern = anchor_pattern(left)
        for right_index in range(left_index, len(orbits)):
            (_right, right_orbit_size, right_patterns,
             right_coefficient) = orbits[right_index]
            symmetry = 1 if left_index == right_index else 2
            local_categories = Counter()
            local_divisor_counts = Counter()
            for right_pattern, pattern_count in right_patterns.items():
                joined = tuple(a | b for a, b in
                               zip(left_pattern, right_pattern))
                available = DIVISORS[joined]
                total_divisors = sum(available.values())
                if total_divisors:
                    category = "unary_reducible"
                    for profile in available:
                        divisor_profile_presence[profile] += (
                            left_orbit_size * symmetry * pattern_count
                        )
                elif any(mask == 0 for mask in joined):
                    category = "survivor_missing_physical_pair"
                else:
                    category = "survivor_only_one_pure_assignment"
                    require(joined in ((1, 1, 1, 1), (2, 2, 2, 2),
                                       (4, 4, 4, 4)),
                            "full pair support lacks a mixed divisor for an "
                            "unclassified reason")
                local_categories[category] += pattern_count
                local_divisor_counts[total_divisors] += pattern_count

            pair_factor = left_orbit_size * symmetry
            coefficient_factor = (left_coefficient * right_coefficient
                                  * pair_factor)
            for category, count in local_categories.items():
                category_ordered_pairs[category] += pair_factor * count
                category_weighted_mass[category] += coefficient_factor * count
            for count, occurrences in local_divisor_counts.items():
                divisor_count_histogram[count] += pair_factor * occurrences
            if local_categories.get("unary_reducible", 0) != right_orbit_size:
                orbit_pair_census.append({
                    "left_orbit": left_index,
                    "right_orbit": right_index,
                    "symmetry": symmetry,
                    "relative_rows": right_orbit_size,
                    "categories": dict(sorted(local_categories.items())),
                    "divisor_count_histogram": dict(sorted(
                        local_divisor_counts.items())),
                })

    total_ordered_pairs = sum(category_ordered_pairs.values())
    total_weighted_mass = sum(category_weighted_mass.values(), Fraction(0))
    require(total_ordered_pairs == labelled_rows**2,
            "ordered pair count does not square labelled support")
    require(total_weighted_mass == labelled_coefficient_mass**2,
            "weighted mass does not square R8 coefficient mass")
    require("unary_reducible" in category_ordered_pairs
            and set(category_ordered_pairs) <= {
        "unary_reducible", "survivor_missing_physical_pair",
        "survivor_only_one_pure_assignment",
    }, "unary categories changed")

    result = {
        "status": "UNAUDITED exact double-orbit incidence census",
        "input_r8_path": str(residual_path),
        "input_r8_sha256": sha256(residual_path.read_bytes()).hexdigest(),
        "stabilizer_order": len(EXPORT.STABILIZER),
        "r8_invariant_row_orbits": len(orbits),
        "r8_labelled_rows": labelled_rows,
        "r8_labelled_coefficient_mass": [labelled_coefficient_mass.numerator,
                                         labelled_coefficient_mass.denominator],
        "ordered_row_pairs": total_ordered_pairs,
        "ordered_pair_categories": dict(sorted(category_ordered_pairs.items())),
        "ordered_pair_category_weighted_mass": {
            key: [value.numerator, value.denominator]
            for key, value in sorted(category_weighted_mass.items())
        },
        "mixed_anchor_divisor_count_histogram_on_ordered_pairs": dict(sorted(
            divisor_count_histogram.items())),
        "unary_word_orbits": {
            "(3,1)": "00000011",
            "(2,2)": "00001111",
            "(2,1,1)": "00001122",
        },
        "unary_reduction_theorem": (
            "A grade-16 R8^2 row is hit by a singleton leading source from "
            "the three selected word orbits iff its anchor factors contain "
            "one cell on each physical anchor pair in a non-pure colour "
            "assignment. The only survivors either miss a physical pair or "
            "admit exactly one, pure, assignment."
        ),
        "orbit_pairs_with_some_survivor": len(orbit_pair_census),
        "orbit_pair_survivor_census": orbit_pair_census,
        "soundness_scope": (
            "This counts ordered summand pairs before collecting coincident "
            "degree-24 monomials. Signed residuals may cancel after collection; "
            "this is not yet a row-orbit support census or a full "
            "associated-graded membership proof."
        ),
    }
    encoded = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("R8^2 unary packet reduction: PASS")
    print("ordered categories:", dict(sorted(category_ordered_pairs.items())))
    print("weighted categories:", {
        key: str(value) for key, value in sorted(category_weighted_mass.items())
    })
    print("orbit pairs with survivor:", len(orbit_pair_census))
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
