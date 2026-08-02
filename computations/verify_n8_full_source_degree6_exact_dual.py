#!/usr/bin/env python3
"""Exact dual obstruction to exponent-one n=8 pure-product membership.

The frozen half-integral functional is supported on 80 rows of off-support
degree at most five and 20 rows of degree six.  This checker expands every
incident orbit to actual Macaulay columns and verifies over Q that the
functional annihilates them individually while pairing to -1 with
H_0 H_1 H_2.  Columns not incident to a support row pair to zero by support.

Scope: this proves exponent-one nonmembership in the unsaturated ideal.  It
does not by itself obstruct localization at the twelve support variables.
"""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


HERE = Path(__file__).resolve().parent
D6_PATH = HERE / "analyze_n8_full_source_pure_product_degree6_lift.py"
SPEC = importlib.util.spec_from_file_location("n8_degree6", D6_PATH)
D6 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(D6)
D5 = D6.D5

CERTIFICATE_PATH = (
    HERE / "certificates/n8_full_source_degree6_exact_dual.json"
)
EXPECTED_CERTIFICATE_SHA256 = (
    "7f5ba935e260864515833a974f26899879f7153e0ff8ee91acb41c0b4b1c15d3"
)
EXPECTED_LEDGER_SHA256 = (
    "1bf53cd05fb701865505054161a50d44730002435c636ef477005ad94e5af941"
)
QQ = Fraction


def row_orbit(row):
    return {
        bytes(sorted(transform[value] for value in row))
        for transform in D5.VARIABLE_TRANSFORMS
    }


def parse_rows(items):
    answer = {}
    for encoded, numerator, denominator in items:
        row = bytes.fromhex(encoded)
        require(len(row) == 12, "dual row does not have ordinary degree 12")
        require(row == D5.canonical_row(row), "dual row is not canonical")
        require(row not in answer, "duplicate dual row")
        value = QQ(numerator, denominator)
        require(value, "zero coefficient in dual support")
        answer[row] = value
    return answer


def audit():
    raw = CERTIFICATE_PATH.read_bytes()
    require(sha256(raw).hexdigest() == EXPECTED_CERTIFICATE_SHA256,
            "exact degree-six dual certificate digest changed")
    certificate = json.loads(raw)
    require(certificate["format"]
            == "n8-full-source-degree6-exact-dual-v1",
            "exact degree-six dual format changed")
    lower = parse_rows(certificate["lower_rows"])
    degree_six = parse_rows(certificate["degree6_rows"])
    require(len(lower) == 80 and len(degree_six) == 20,
            "exact dual support census changed")
    require(not (set(lower) & set(degree_six)), "dual supports overlap")
    require(all(D5.row_degree(row) <= 5 for row in lower),
            "lower dual support escaped filtration degree five")
    require(all(D5.row_degree(row) == 6 for row in degree_six),
            "leading dual support escaped filtration degree six")
    invariant_weights = lower | degree_six
    full_weights = {
        row: value / len(row_orbit(row))
        for row, value in invariant_weights.items()
    }

    canonical_columns = set()
    leading_incident_columns = set()
    for row in invariant_weights:
        incident = {
            D5.canonical_column(column) for column in D6.incident_columns(row)
        }
        canonical_columns.update(incident)
        if row in degree_six:
            leading_incident_columns.update(incident)
    require(len(canonical_columns)
            == certificate["expected_canonical_incident_columns"] == 180,
            "canonical incident-column census changed")
    require(all(D5.column_minimum_degree(column) <= 5
                for column in leading_incident_columns),
            "degree-six dual support acquired an incident leading column")

    actual_columns = set()
    orbit_size_histogram = Counter()
    minimum_degree_histogram = Counter()
    for column in canonical_columns:
        require(column == D5.canonical_column(column),
                "incident column is not canonical")
        D5.verify_balanced_column(column)
        minimum_degree_histogram[D5.column_minimum_degree(column)] += 1
        orbit = D5.column_orbit(column)
        orbit_size_histogram[len(orbit)] += 1
        for actual_column in orbit:
            actual_columns.add(actual_column)
            pairing = sum(
                full_weights.get(D5.canonical_row(output), QQ(0))
                for output in D5.iter_column_outputs(actual_column)
            )
            require(not pairing,
                    "exact dual does not annihilate an actual mixed column")
    require(len(actual_columns)
            == certificate["expected_actual_incident_columns"] == 706,
            "actual incident-column census changed")

    actual_target, canonical_target = D6.pure_target_rows(6)
    invariant_target_pairing = (
        sum(lower.get(row, QQ(0)) for row in canonical_target
            if D5.row_degree(row) <= 5)
        + sum(degree_six.get(row, QQ(0)) for row in canonical_target
              if D5.row_degree(row) == 6)
    )
    full_target_pairing = sum(
        full_weights.get(D5.canonical_row(row), QQ(0))
        for row in actual_target
    )
    expected_pairing = QQ(*certificate["target_pairing"])
    require(invariant_target_pairing == full_target_pairing
            == expected_pairing == -1,
            "exact dual target pairing changed")

    coefficient_histogram = Counter(invariant_weights.values())
    return {
        "vertices": 8,
        "endpoint_colours": 3,
        "balanced_ordinary_degree": 12,
        "maximum_dual_off_support_degree": 6,
        "lower_dual_rows": len(lower),
        "leading_degree_six_dual_rows": len(degree_six),
        "dual_coefficient_histogram": [
            [[value.numerator, value.denominator], count]
            for value, count in sorted(coefficient_histogram.items())
        ],
        "canonical_incident_columns": len(canonical_columns),
        "actual_incident_columns": len(actual_columns),
        "canonical_columns_by_minimum_degree": dict(
            sorted(minimum_degree_histogram.items())
        ),
        "canonical_column_orbit_size_histogram": dict(
            sorted(orbit_size_histogram.items())
        ),
        "pure_target_actual_rows_through_degree_six": len(actual_target),
        "pure_target_orbits_through_degree_six": len(canonical_target),
        "exact_target_pairing": [
            expected_pairing.numerator, expected_pairing.denominator
        ],
        "arithmetic": "exact rational",
        "identity": "dual annihilates every mixed degree-12 Macaulay column and pairs -1 with H_0 H_1 H_2",
        "conclusion": "H_0 H_1 H_2 is not in the unsaturated mixed ideal at exponent one",
        "scope_guard": "does not decide localization or support-variable saturation",
        "certificate_sha256": EXPECTED_CERTIFICATE_SHA256,
    }


def main():
    ledger = audit()
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                "frozen exact degree-six dual ledger changed")
    print(
        "n=8 full-source degree-six exact dual: PASS; "
        f"support={ledger['lower_dual_rows']}+"
        f"{ledger['leading_degree_six_dual_rows']}, "
        f"columns={ledger['actual_incident_columns']}, pairing=-1"
    )
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
