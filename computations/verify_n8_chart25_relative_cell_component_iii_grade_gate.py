#!/usr/bin/env python3
"""Exact grade/target gate for the chart-25 relative-cell candidate.

For each hidden A_i in the five-row chart-25 fibre, remove its unique
pure-zero matching divisor M0 and compare:

    e_i  = an incident mixed column with a balanced 4+4 full word,
    a_i  = (A_i/M0) * (H_0 - 1).

The local five-row projection of e_i-a_i is D.  The checker retains the
complete source terms and proves that this does not give the rootless h=3
relative attaching cell: the candidate has balanced product-anchor fine
degree, a nonzero multiplier-labelled pure target, and 207 off-fibre rows.
All four possible four-sums have at least 818 off-fibre rows and four
distinct target labels; none lies in one selected endpoint ordering.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
EXPECTED_LEDGER_SHA256 = "bb5cdfc01142d733eede3f45b3a04877c8d5afb29f2c91ae65afb3155a57a179"
PINS = {
    "computations/verify_n8_chart25_relative_4d_obstruction.py":
        "afb3ff04ec4c2c487b577d8d332f993e4fcf469244da8c77f5c51ff04b3753c5",
    "computations/verify_n8_chart25_degree4_exact_dual.py":
        "d7287c45eff9ada8d2d41bb060d75049f2f53e847c71ff2c7e99e122211d1649",
    "computations/verify_h3_rootless_component_iii_complete_typed_inventory.py":
        "3e2b5912f58646169547b418bb4975a27635dcd8d548a010eb4c2e265412f465",
}
EXPECTED_BALANCED_WORDS = (
    ("21212112",),
    ("11122122", "21221121"),
    ("12112212", "22211211"),
    ("12121221",),
)
EXPECTED_MULTIPLIERS = (
    "0d114c62bcdce0e5",
    "0d114d62b8dce0e6",
    "0d114f5ebcdce0e8",
    "0d11505eb8dce0e9",
)


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"pinned dependency changed: {relative}")


def signed_difference(positive, negative):
    answer = Counter(positive)
    answer.subtract(negative)
    return {key: value for key, value in answer.items() if value}


def add_signed(target, source) -> None:
    for key, value in source.items():
        updated = target.get(key, 0) + value
        if updated:
            target[key] = updated
        else:
            target.pop(key, None)


def divide_monomial(row: bytes, divisor: bytes) -> bytes:
    remainder = list(row)
    for coordinate in divisor:
        require(coordinate in remainder, "claimed divisor is absent")
        remainder.remove(coordinate)
    return bytes(sorted(remainder))


def site_colour_degree(row: bytes, coordinates) -> tuple[tuple[int, ...], ...]:
    degree = [[0, 0, 0] for _ in range(8)]
    for coordinate in row:
        left, right, left_colour, right_colour = coordinates[coordinate]
        degree[left][left_colour] += 1
        degree[right][right_colour] += 1
    return tuple(tuple(values) for values in degree)


def endpoint_fine_degree(row: bytes, coordinates, endpoints=(0, 1)):
    degree = site_colour_degree(row, coordinates)
    return degree[endpoints[0]], degree[endpoints[1]]


def main() -> None:
    pin_dependencies()
    relative = load(
        "chart25_relative_cell_grade_base",
        "verify_n8_chart25_relative_4d_obstruction.py",
    )
    base = relative.BASE
    dual = relative.DUAL

    expanded, _ = dual.expanded_functional()
    degree_two_columns = dual.actual_incident_source_columns(expanded)[2]
    local_rows = relative.frozen_rows()
    a_rows = local_rows[:4]
    d_row = local_rows[4]

    m0_edges = ((0, 1), (2, 4), (3, 5), (6, 7))
    m0 = bytes(sorted(
        base.COORDINATE_ID[(left, right, 0, 0)]
        for left, right in m0_edges
    ))
    require(tuple(base.COORDINATES[index][:2] for index in m0) == m0_edges,
            "M0 physical matching changed")

    balanced = ((1, 1, 1), (1, 1, 1))
    localized_terminal_degrees = {
        (tuple(3 if colour == left else 0 for colour in range(3)),
         tuple(3 if colour == right else 0 for colour in range(3)))
        for left in range(3) for right in range(3)
    }
    underived_attaching_degrees = {
        (tuple(4 if colour == left else 0 for colour in range(3)),
         tuple(4 if colour == right else 0 for colour in range(3)))
        for left in range(3) for right in range(3)
    }
    require(balanced not in localized_terminal_degrees
            and balanced not in underived_attaching_degrees,
            "balanced product-anchor degree became a selected terminal grade")

    candidate_records = []
    balanced_options = []
    target_multipliers = []

    selected_midpoint_words = {}
    for endpoints in ((2, 1), (1, 2)):
        selected_midpoint_words[endpoints] = {
            endpoints + residual
            for residual in itertools.product((1, 2), repeat=6)
            if residual.count(1) == residual.count(2) == 3
        }
        require(len(selected_midpoint_words[endpoints]) == 20,
                "selected midpoint word count changed")

    for index, a_row in enumerate(a_rows):
        pure_zero_cells = bytes(sorted(
            coordinate for coordinate in a_row
            if base.COORDINATES[coordinate][2:] == (0, 0)
        ))
        require(pure_zero_cells == m0,
                f"A{index + 1} lost its unique pure-zero divisor")
        # There are exactly four pure-zero cells and they form a perfect
        # matching, hence M0 is the unique pure-zero perfect-matching divisor.
        require(len(pure_zero_cells) == 4
                and {site for coordinate in pure_zero_cells
                     for site in base.COORDINATES[coordinate][:2]}
                == set(range(8)),
                "pure-zero divisor stopped being a perfect matching")
        multiplier = divide_monomial(a_row, m0)

        incident = []
        for column in degree_two_columns:
            outputs = base.column_rows(column)
            if a_row not in outputs or d_row not in outputs:
                continue
            word = column[0]
            if word.count(1) == word.count(2) == 4:
                incident.append(column)
        incident.sort(key=lambda column: "".join(map(str, column[0])))
        require(len(incident) == (1, 2, 2, 1)[index],
                f"A{index + 1} balanced incident count changed")
        pure_column = ((0,) * 8, multiplier)
        pure_outputs = tuple(base.column_rows(pure_column))
        require(len(pure_outputs) == 105, "pure hafnian term count changed")
        fine_degree = endpoint_fine_degree(a_row, base.COORDINATES)
        require(fine_degree == balanced
                and fine_degree not in localized_terminal_degrees
                and fine_degree not in underived_attaching_degrees,
                "candidate entered a repeated selected response grade")

        option_records = []
        for mixed_column in incident:
            mixed_outputs = tuple(base.column_rows(mixed_column))
            require(len(mixed_outputs) == 105,
                    "mixed hafnian term count changed")
            shared = set(mixed_outputs) & set(pure_outputs)
            require(shared == {a_row},
                    f"e{index + 1} and a{index + 1} share more than A_i")
            difference = signed_difference(mixed_outputs, pure_outputs)
            local_trace = {
                row: difference.get(row, 0) for row in local_rows
                if difference.get(row, 0)
            }
            require(local_trace == {d_row: 1},
                    f"local trace of e{index + 1}-a{index + 1} is not D")
            require(len(difference) == 208
                    and Counter(difference.values())
                    == Counter({1: 104, -1: 104}),
                    "one relative candidate global row census changed")
            off_fibre = {row: value for row, value in difference.items()
                         if row not in local_rows}
            require(len(off_fibre) == 207
                    and Counter(off_fibre.values())
                    == Counter({1: 103, -1: 104}),
                    "one relative candidate off-fibre census changed")

            degrees = {
                site_colour_degree(row, base.COORDINATES)
                for row in mixed_outputs + pure_outputs
            }
            require(len(degrees) == 1,
                    "a candidate column stopped being site-colour homogeneous")
            degree, = degrees
            require(all(site_degree == (1, 1, 1) for site_degree in degree),
                    "chart25 candidate left product-of-three-anchors degree")

            word = mixed_column[0]
            word_text = "".join(map(str, word))
            midpoint_membership = [
                "".join(map(str, endpoints))
                for endpoints, words in selected_midpoint_words.items()
                if word in words
            ]
            option_records.append({
                "mixed_word": word_text,
                "mixed_endpoint_sector": list(word[:2]),
                "residual_colour_counts": [
                    word[2:].count(1), word[2:].count(2),
                ],
                "selected_midpoint_orderings": midpoint_membership,
                "local_trace": "D",
                "global_monomial_rows": len(difference),
                "off_fibre_rows": len(off_fibre),
                "global_coefficients": {"-1": 104, "1": 104},
            })

        target_multipliers.append(multiplier)
        balanced_options.append(tuple(incident))
        candidate_records.append({
            "A_index": index + 1,
            "balanced_options": option_records,
            "pure_anchor_word": "00000000",
            "target_multiplier": multiplier.hex(),
            "endpoint_fine_degree": [list(values) for values in fine_degree],
            "literal_target": (
                "+target_multiplier in the e_i-a_i convention; nonzero"
            ),
        })

    actual_words = tuple(
        tuple(option["mixed_word"] for option in record["balanced_options"])
        for record in candidate_records
    )
    require(actual_words == EXPECTED_BALANCED_WORDS,
            "canonical balanced mixed words changed")
    require(tuple(multiplier.hex() for multiplier in target_multipliers)
            == EXPECTED_MULTIPLIERS, "target multiplier labels changed")
    require(len(set(target_multipliers)) == 4,
            "four pure target multiplier labels collapsed")

    coverage = {
        "21": [record["A_index"] for record in candidate_records
               if any("21" in option["selected_midpoint_orderings"]
                      for option in record["balanced_options"])],
        "12": [record["A_index"] for record in candidate_records
               if any("12" in option["selected_midpoint_orderings"]
                      for option in record["balanced_options"])],
    }
    require(coverage == {"21": [1, 2], "12": [3, 4]},
            "selected midpoint endpoint-order coverage changed")

    # Exhaust the 1*2*2*1 choices.  Each projects to 4D, but none has one
    # endpoint ordering and each retains a large literal off-fibre defect.
    sum_records = []
    for combination in itertools.product(*balanced_options):
        total_boundary = {}
        sectors = Counter()
        for a_row, mixed_column, multiplier in zip(
                a_rows, combination, target_multipliers, strict=True):
            pure_column = ((0,) * 8, multiplier)
            difference = signed_difference(
                base.column_rows(mixed_column), base.column_rows(pure_column)
            )
            add_signed(total_boundary, difference)
            sectors[tuple(mixed_column[0][:2])] += 1
        local_sum = {
            row: total_boundary.get(row, 0) for row in local_rows
            if total_boundary.get(row, 0)
        }
        require(local_sum == {d_row: 4},
                "a four-candidate trace stopped projecting to 4D")
        off_fibre = {row: value for row, value in total_boundary.items()
                     if row not in local_rows}
        require(len(off_fibre) in (818, 820),
                "four-candidate off-fibre size changed")
        require(len(sectors) >= 2,
                "a four-sum entered one endpoint ordering")
        sum_records.append({
            "words": ["".join(map(str, column[0]))
                      for column in combination],
            "endpoint_sectors": {
                "".join(map(str, sector)): count
                for sector, count in sorted(sectors.items())
            },
            "local_projection": "4D",
            "global_monomial_rows": len(total_boundary),
            "off_fibre_rows": len(off_fibre),
            "coefficient_histogram": {
                str(value): count for value, count
                in sorted(Counter(total_boundary.values()).items())
            },
        })
    require(len(sum_records) == 4
            and Counter(record["off_fibre_rows"] for record in sum_records)
            == Counter({818: 2, 820: 2}),
            "four-sum option census changed")

    # The formal chart25 target quotient assigns weight 1/4 to each of the
    # four distinct multiplier-labelled pure targets.  Only after this
    # quotient and deletion of 820 off-fibre rows does the four-sum read as
    # the familiar relative 4D-tau class.
    target_quotient_value = sum((Q(1, 4) for _ in target_multipliers), Q(0))
    require(target_quotient_value == 1,
            "formal normalized target quotient changed")

    ledger = {
        "pins": PINS,
        "M0": {
            "physical_edges": [list(edge) for edge in m0_edges],
            "coordinate_ids": list(m0),
            "hex": m0.hex(),
        },
        "candidate_records": candidate_records,
        "four_sum": {
            "balanced_choice_counts": [1, 2, 2, 1],
            "selected_midpoint_leaf_coverage": coverage,
            "combinations": sum_records,
            "literal_target_labels": len(set(target_multipliers)),
            "formal_target_quotient": "tau",
        },
        "component_iii_grade": {
            "chart25_endpoint_degree": [[1, 1, 1], [1, 1, 1]],
            "localized_terminal_required": "3*e_a on left and 3*e_b on right",
            "underived_K_required": "4*e_a on left and 4*e_b on right",
            "compatible": False,
        },
        "earliest_failures": [
            "balanced product-anchor endpoint degree is not repeated selected response degree",
            "no fixed endpoint ordering contains all four A-leaf midpoint representatives",
            "e_i-a_i has a nonzero multiplier-labelled pure target",
            "every four-sum retains at least 818 literal off-fibre rows and four distinct targets",
        ],
        "verdict": (
            "chart25 e_i-a_i realizes only the projected relative 4D-tau "
            "mapping-cylinder class; it does not realize the source-valid "
            "Component III C_rel row"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    require(EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED",
            f"pin EXPECTED_LEDGER_SHA256={digest}")
    require(digest == EXPECTED_LEDGER_SHA256,
            f"chart25 Component III grade ledger changed: {digest}")
    print("chart25 relative cell / Component III grade gate: PASS")
    print("balanced choices per A leaf: 1,2,2,1; four combinations")
    print("selected midpoint coverage: order21 -> A1,A2; order12 -> A3,A4")
    print("four-sums: local 4D; >=818 off-fibre rows; 4 distinct targets")
    print(f"ledger sha256: {digest}")


if __name__ == "__main__":
    main()
