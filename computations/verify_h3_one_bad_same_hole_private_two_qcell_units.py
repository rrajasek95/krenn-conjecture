#!/usr/bin/env python3
"""Exact units on the six first two-q-cell contamination supports.

Audit only the two-cell private-row frontiers listed in dae10d3.  In every
case the pure and mixed private coefficients acquire the same second
matching.  After factoring R_a versus R_c, their two-term common tails agree
exactly, so the original determinant-cleared two-row unit survives.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_one_bad_same_hole_three_carrier_one_qcell_stability.py":
        "056e95e6692e1f709a43d9dabe43f594793cd2bec60163c628a2ca4286afeb8c",
    "computations/verify_h3_one_bad_same_hole_shared_carrier_fullword_unit.py":
        "191336312c54249a719def2e3cce12162321c9a7a9dc869b095adf3f2d16f1d9",
}
EXPECTED_LEDGER_SHA256 = (
    "b6d9967ec9be989773ecf7aea504a0185824bbca934d7ebea2fb00a4d0f4777c"
)

PURE = (0,) * 8
MIXED = tuple(map(int, "00000001"))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"dependency changed: {relative}: {actual}")


def factor_variable(poly, variable):
    answer = Counter()
    for monomial, coefficient in poly.items():
        factors = list(monomial)
        require(factors.count(variable) == 1,
                f"private variable {variable} stopped being a simple factor")
        factors.remove(variable)
        answer[tuple(factors)] += coefficient
    return answer


def serial_poly(poly):
    return tuple("*".join(monomial) for monomial in sorted(poly))


def main():
    pin_dependencies()
    base = importlib.import_module(
        "verify_h3_one_bad_common_q_cap_extraction_boundary")
    repair = importlib.import_module(
        "verify_h3_one_bad_same_hole_internal_repair_reselection")
    fullword = importlib.import_module(
        "verify_h3_one_bad_same_hole_shared_carrier_fullword_unit")

    cases = {
        "shared_plus_A2": ("shared_CA", ((0, 3, 0, 0), (1, 4, 0, 0))),
        "shared_plus_A3": ("shared_CA", ((0, 4, 0, 0), (1, 3, 0, 0))),
        "middle_right_plus_A1": (
            "middle_AT_right", ((0, 1, 0, 0), (3, 4, 0, 0))),
        "middle_right_plus_A3": (
            "middle_AT_right", ((0, 4, 0, 0), (1, 3, 0, 0))),
        "middle_left_plus_A1": (
            "middle_AT_left_secondary", ((0, 1, 0, 0), (3, 4, 0, 0))),
        "middle_left_plus_A3": (
            "middle_AT_left_secondary", ((0, 4, 0, 0), (1, 3, 0, 0))),
    }
    expected_summaries = {
        "shared_plus_A2": (19, 34, 38, Counter({1: 30, 2: 4})),
        "shared_plus_A3": (19, 35, 39, Counter({1: 31, 2: 4})),
        "middle_right_plus_A1": (19, 34, 38, Counter({1: 30, 2: 4})),
        "middle_right_plus_A3": (19, 27, 31, Counter({1: 23, 2: 4})),
        "middle_left_plus_A1": (21, 51, 57, Counter({1: 45, 2: 6})),
        "middle_left_plus_A3": (21, 40, 46, Counter({1: 34, 2: 6})),
    }

    ra = fullword.variable_name(base.cell(2, 7, 0, 0))
    rc = fullword.variable_name(base.cell(2, 7, 0, 1))
    fixed_values = {
        fullword.variable_name(cell): Fraction(value)
        for cell, value in repair.outer_source(base.cell).items()
    }
    ledgers = {}
    for name, (packet_name, additions) in cases.items():
        source = Counter(repair.common_packets(base.cell)[packet_name])
        source.update(repair.outer_source(base.cell))
        added_cells = tuple(base.cell(*cell) for cell in additions)
        require(not any(cell in source for cell in added_cells),
                f"{name} did not add two new cells")
        source.update({cell: 1 for cell in added_cells})

        rows, live = fullword.full_word_rows(base, source)
        summary = (len(source), len(rows), sum(map(len, rows.values())),
                   Counter(map(len, rows.values())))
        require(summary == expected_summaries[name],
                f"{name} full-word summary changed: {summary}")
        require(len(rows[PURE]) == len(rows[MIXED]) == 2,
                f"{name} private tails stopped having two terms")
        require(live[PURE] == live[MIXED] and len(live[PURE]) == 2,
                f"{name} pure/mixed matching lists separated")

        pure_tail = factor_variable(rows[PURE], ra)
        mixed_tail = factor_variable(rows[MIXED], rc)
        require(pure_tail == mixed_tail and len(pure_tail) == 2,
                f"{name} two-term common tail changed")
        pure_generator = fullword.add(
            (rows[PURE], 1), (Counter({(): Fraction(1)}), -1))
        mixed_generator = rows[MIXED]
        localized = fullword.add(
            (fullword.multiply_variable(mixed_generator, ra), 1),
            (fullword.multiply_variable(pure_generator, rc), -1),
        )
        require(localized == Counter({(rc,): 1}),
                f"{name} localized private-row unit changed: {localized}")

        fixed_pure = fullword.specialize(pure_generator, fixed_values)
        fixed_mixed = fullword.specialize(mixed_generator, fixed_values)
        ordinary = fullword.add((fixed_mixed, Fraction(-1, 2)),
                                (fixed_pure, -1))
        require(ordinary == Counter({(): 1}),
                f"{name} ordinary private-row unit changed: {ordinary}")

        ledgers[name] = {
            "base_packet": packet_name,
            "added_cells": tuple(fullword.variable_name(cell)
                                   for cell in added_cells),
            "support_cells": len(source),
            "nonzero_physical_rows": len(rows),
            "physical_monomials": sum(map(len, rows.values())),
            "row_size_histogram": dict(sorted(summary[3].items())),
            "private_matchings": live[PURE],
            "common_tail_terms": serial_poly(pure_tail),
            "localized_identity": "ra*Gmixed-rc*Gpure=rc",
            "fixed_identity": "1=(-1/2)*Gmixed-Gpure",
            "classification": "original_two_row_unit_survives",
        }

    ledger = {
        "dependencies": PINS,
        "cases": ledgers,
        "classification_counts": {
            "original_two_row_unit_survives": 6,
            "replacement_literal_unit": 0,
            "coefficient_feasible_packet": 0,
        },
        "verdict": (
            "all six explicit first two-q-cell contamination supports are "
            "empty; the added matching enters the pure and mixed private "
            "rows with the same tail, so the original two-row unit survives"
        ),
        "scope": (
            "only the six two-cell supports listed in dae10d3; no third cell, "
            "endpoint-star enlargement, or arbitrary support completion"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"the two-q-cell unit ledger changed: {digest}")

    print("h=3 same-hole private two-q-cell units: PASS")
    print("explicit frontier supports audited: 6")
    print("classifications: original unit survives/replacement/guard = 6/0/0")
    print("all private tails have the same two physical matchings in both rows")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
