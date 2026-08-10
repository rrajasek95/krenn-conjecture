#!/usr/bin/env python3
"""Close the full relative orbit of the squarefree one-bad rectangle lift.

Permute the 19-cell source-provenant K2,4 rectangle through all site labels
while keeping each of the two sharp star orientations fixed.  There are 180
distinct supports, twelve over each omitted perfect matching.  Relative to
F0=01|24|35, all 168 supports in the six share-one and eight disjoint circuit
classes miss a required pure target response.  Of the twelve aligned
supports, ten also miss a target, one has two forbidden singleton fibres,
and the sole semantic support is the pinned shared-two-zero-fan unit.

The pinned support-11 circuit orbit is also replayed.  Its primitive doubled
coefficient proves that it is not a squarefree single-fibre rectangle lift;
no translated-target unit is claimed for that remaining orbit.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_n8_one_bad_global_debt_circuit_quotient.py":
        "85353d137c38c66e6c93918c44521293d9e2caa6e304d587ca88533a4feff320",
    "computations/verify_n8_one_bad_even_cycle_rectangle_obstruction.py":
        "970d9a8dcd12a7cf49ac3b956b6c398db1b5dc45b2de62ba116e138e72fcc0fb",
    "computations/verify_n8_one_bad_binary_projection_minimal_counterguards.py":
        "2b32c6d50ea1dda5a7b412a0fcd6de2373ab483b5b25eba7352684a5499e8f28",
    "computations/verify_n8_one_bad_first_cross_mate_exchange.py":
        "e1d641d64bf0659d6b28ea64bf8a935e17c4da1c7e2c831f0dfb041fc78eaf0c",
}
EXPECTED_DIGEST = "2b3c2e82fd9c4ecd9702c8d4b8f986c091fb08ae63f9c8d3f99cbb88531449e6"


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def load_pinned(name, relative):
    path = ROOT / relative
    actual = sha256(path.read_bytes()).hexdigest()
    require(actual == PINS[relative],
            f"dependency changed: {relative}: {actual}")
    spec = spec_from_file_location(name, path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def edge(left, right):
    return tuple(sorted((left, right)))


def transform_support(support, permutation):
    transformed = []
    for (left, right), (left_colour, right_colour) in support:
        image_left = permutation[left]
        image_right = permutation[right]
        if image_left < image_right:
            transformed.append(((image_left, image_right),
                                (left_colour, right_colour)))
        else:
            transformed.append(((image_right, image_left),
                                (right_colour, left_colour)))
    return tuple(sorted(transformed))


def fibre_table(first, base, packet, support):
    a_matching, b_matching, b_holes, c_matching, c_holes = packet
    table = {
        ("top", word): coefficient
        for word, coefficient in first.endpoint_tensor(support, 3).items()
    }
    rows = (
        ("bb", base.B, b_holes[0], base.B, b_holes[1]),
        ("bc", base.B, b_holes[0], base.C, c_holes[1]),
        ("cb", base.C, c_holes[0], base.B, b_holes[1]),
        ("cc", base.C, c_holes[0], base.C, c_holes[1]),
    )
    for name, left_colour, left_hole, right_colour, right_hole in rows:
        if left_hole == right_hole:
            continue
        fixed = ((left_hole, left_colour),
                 (right_hole, right_colour))
        for word, coefficient in first.endpoint_tensor(
                support, 2, fixed).items():
            table[name, word] = coefficient
    return table


def support_verdict(first, base, packet, support):
    table = fibre_table(first, base, packet, support)
    required = (
        ("top", (base.A,) * 6),
        ("bb", (base.B,) * 6),
        ("cc", (base.C,) * 6),
    )
    missing = tuple(label for label in required if not table.get(label, 0))
    if missing:
        return "missing_target", missing

    allowed = set(required)
    singleton = tuple(sorted(
        label for label, coefficient in table.items()
        if label not in allowed and coefficient == 1
    ))
    if singleton:
        return "forbidden_singleton", singleton
    return "semantic", ()


def audit_relative_support_orbit(global_debt, fan):
    base = load_pinned(
        "one_bad_binary_base",
        "computations/verify_n8_one_bad_binary_projection_minimal_counterguards.py",
    )
    first = load_pinned(
        "one_bad_first_exchange",
        "computations/verify_n8_one_bad_first_cross_mate_exchange.py",
    )

    canonical = tuple(sorted(
        (physical, (left_colour, right_colour))
        for physical, left_colour, right_colour in fan.SUPPORT
    ))
    distinguished = frozenset({(0, 1), (2, 4), (3, 5)})
    support_to_missing = defaultdict(set)
    for permutation in itertools.permutations(range(6)):
        support = transform_support(canonical, permutation)
        omitted = frozenset(
            edge(permutation[left], permutation[right])
            for left, right in distinguished
        )
        support_to_missing[support].add(omitted)

    require(len(support_to_missing) == 180,
            "the relative rectangle support orbit changed")
    require(Counter(len(values) for values in support_to_missing.values())
            == Counter({1: 180}),
            "a rectangle support acquired an ambiguous omitted matching")

    per_star = []
    semantic_supports = []
    singleton_records = []
    for star_index, packet in enumerate(base.SHARP_REPRESENTATIVES):
        census = Counter()
        for support, values in support_to_missing.items():
            omitted = next(iter(values))
            intersection = len(omitted & distinguished)
            verdict, details = support_verdict(
                first, base, packet, support
            )
            census[intersection, verdict] += 1
            if verdict == "semantic":
                semantic_supports.append((star_index, support))
            elif verdict == "forbidden_singleton":
                singleton_records.append({
                    "star_pattern": star_index,
                    "relative_intersection": intersection,
                    "labels": [[row, list(word)] for row, word in details],
                })

        expected = Counter({
            (0, "missing_target"): 96,
            (1, "missing_target"): 72,
            (3, "missing_target"): 10,
            (3, "forbidden_singleton"): 1,
            (3, "semantic"): 1,
        })
        require(census == expected,
                f"relative support census changed at star {star_index}: {census}")
        per_star.append([
            [intersection, verdict, count]
            for (intersection, verdict), count in sorted(census.items())
        ])

    require(len(semantic_supports) == 2,
            "the two star patterns lost their sole semantic support")
    def binary_cells(support):
        return tuple(cell for cell in support if cell[1] != (base.A, base.A))

    require(all(binary_cells(support) == binary_cells(canonical)
                for _, support in semantic_supports),
            "a sole semantic support lost the canonical binary rectangle")
    require(all(len(support) - len(binary_cells(support)) == 3
                for _, support in semantic_supports),
            "a sole semantic support lost its pure top matching")
    require(len(singleton_records) == 2
            and all(len(record["labels"]) == 2
                    for record in singleton_records),
            "the aligned singleton guard changed")

    fan_result = fan.audit_shared_zero_fans()
    require(len(fan_result["unit_fans"]) == 4
            and fan_result["complete_rectangle_ideal"] == "unit over QQ",
            "the semantic aligned rectangle stopped being a coefficient unit")
    return {
        "support_orbit": len(support_to_missing),
        "supports_per_omitted_matching": 12,
        "sharp_star_patterns": len(base.SHARP_REPRESENTATIVES),
        "per_star_census": per_star,
        "unaligned_supports_per_star": 168,
        "unaligned_verdict": "all miss a required pure response target",
        "aligned_per_star": {
            "missing_target": 10,
            "forbidden_two_singletons": 1,
            "semantic_then_fan_unit": 1,
        },
        "singleton_records": singleton_records,
        "semantic_fan_unit": fan_result,
        "verdict": (
            "every support in the full relative squarefree rectangle orbit "
            "is excluded for both sharp star orientations"
        ),
    }


def audit_multiplicity_scope(global_debt, base):
    incidence, circuits = global_debt.enumerate_circuits()
    orbit = global_debt.audit_multiplicity_orbit(circuits)
    large = [(support, coefficients) for support, coefficients in circuits
             if len(support) == 11]
    require(len(large) == 30,
            "the support-11 circuit orbit changed")
    for support, coefficients in large:
        require(sorted(abs(value) for value in coefficients)
                == [1] * 10 + [2],
                "a support-11 circuit became squarefree")
        # A fixed decorated matching occurs once in a literal hafnian fibre.
        # The coefficient 2 therefore means the matching node must be reused
        # by two exchange moves; this is not a squarefree rectangle packet.
        require(sum(max(value, 0) for value in coefficients) == 6
                and sum(max(-value, 0) for value in coefficients) == 6,
                "the repeated-provenance move count changed")
    sharp_distinguished = []
    for packet in base.SHARP_REPRESENTATIVES:
        a_matching, b_matching, b_holes, c_matching, c_holes = packet
        distinguished = frozenset({
            edge(*a_matching[0]), edge(*b_holes), edge(*c_holes),
        })
        sharp_distinguished.append(distinguished)
    require(len(set(sharp_distinguished)) == 1
            and next(iter(set(sharp_distinguished)))
            == frozenset({(0, 1), (2, 4), (3, 5)}),
            "the two sharp stars lost their common unordered debt datum")
    relative = orbit["relative_to_01_24_35_doubled_matching"]
    return {
        **orbit,
        "sharp_star_patterns": len(base.SHARP_REPRESENTATIVES),
        "per_star_relative_doubled_matching": [
            dict(relative) for packet in base.SHARP_REPRESENTATIVES
        ],
        "single_fibre_squarefree_lift": False,
        "required_next_datum": (
            "two source-labelled grades using the doubled matching, plus a "
            "translated-target identity coupling those grades"
        ),
        "coefficient_verdict": "not decided by the rectangle orbit closure",
    }


def main():
    global_debt = load_pinned(
        "one_bad_global_debt",
        "computations/verify_n8_one_bad_global_debt_circuit_quotient.py",
    )
    fan = load_pinned(
        "one_bad_rectangle_fan",
        "computations/verify_n8_one_bad_even_cycle_rectangle_obstruction.py",
    )
    base = load_pinned(
        "one_bad_binary_base",
        "computations/verify_n8_one_bad_binary_projection_minimal_counterguards.py",
    )
    squarefree = audit_relative_support_orbit(global_debt, fan)
    multiplicity = audit_multiplicity_scope(global_debt, base)
    ledger = {
        "pins": PINS,
        "squarefree_relative_rectangle_orbit": squarefree,
        "multiplicity_2_scope": multiplicity,
        "verdict": (
            "all fourteen unaligned support-8 circuit classes are excluded "
            "on the complete source-provenant rectangle lift for both sharp "
            "star patterns; the support-11 orbit is genuinely repeated-" 
            "provenance and remains the translated-target boundary"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST,
                f"relative rectangle orbit ledger changed: {digest}")

    print("N=8 one-bad relative rectangle orbit closure: PASS")
    print("relative supports / star patterns: 180 / 2")
    print("unaligned supports: 168 per star, all missing a pure target")
    print("aligned: 10 missing + 1 singleton + 1 fan unit per star")
    print("support-11 orbit: repeated provenance; translated target remains")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
