#!/usr/bin/env python3
"""Exact four-row dual for the chart-25 source-faithful d<=4 block.

The checker is support-local.  A column can pair nontrivially with the dual
only if one of its matching terms is one of the four displayed rows.
``incident_columns`` enumerates every such factorization, so checking the
nine recovered canonical columns proves annihilation of the complete source
families (913,608 degree-four and 59,488 older column orbits), and hence of
all 31,584 transferred lower-kernel tails.
"""

from collections import Counter
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
QQ = Fraction
EXPECTED_LEDGER_SHA256 = (
    "fa4d75330185f38e60a755395e4feb8851758138ade398ddb52e9b0db01e259a"
)


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BASE = load("n8_chart25_d4_exact_base",
            "analyze_n8_chart25_degree2_lift.py")
VERIFY3 = load("n8_chart25_d4_exact_verify3",
               "verify_n8_chart25_degree3_lift.py")


FUNCTIONAL = {
    bytes((0, 13, 17, 76, 98, 126, 171, 188, 220, 224, 229, 243)): -2,
    bytes((0, 13, 17, 77, 98, 126, 171, 184, 220, 224, 230, 243)): -1,
    bytes((0, 13, 17, 79, 94, 126, 171, 188, 220, 224, 232, 243)): -1,
    bytes((0, 13, 17, 94, 98, 126, 171, 184, 188, 220, 224, 243)): 1,
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def column_pairing(column):
    value = 0
    for actual_column in BASE.column_orbit(column):
        for row in BASE.column_rows(actual_column):
            # This is exactly the invariant quotient convention used by the
            # filtered Macaulay matrices: retain one canonical output row.
            if row == BASE.canonical_row(row):
                value += FUNCTIONAL.get(row, 0)
    return value


def expanded_functional():
    """Lift the quotient functional to individual actual monomial rows."""
    expanded = {}
    orbit_sizes = Counter()
    for representative, value in FUNCTIONAL.items():
        orbit = {
            bytes(sorted(transform[index] for index in representative))
            for transform in BASE.TRANSFORMS
        }
        orbit_sizes[len(orbit)] += 1
        for row in orbit:
            require(row not in expanded, "functional row orbits overlap")
            # For an invariant vector, summing these actual-row weights gives
            # the stored quotient coordinate.
            expanded[row] = QQ(value, len(orbit))
    return expanded, orbit_sizes


def actual_incident_source_columns(expanded):
    families = {2: set(), 3: set(), 4: set()}
    for row in expanded:
        for column in BASE.incident_columns(row):
            degree = BASE.column_minimum_degree(column)
            if degree in families:
                families[degree].add(column)
    return families


def incident_source_columns():
    families = {2: set(), 3: set(), 4: set()}
    for row in FUNCTIONAL:
        for raw_column in BASE.incident_columns(row):
            column = BASE.canonical_column(raw_column)
            degree = BASE.column_minimum_degree(column)
            if degree in families:
                families[degree].add(column)
    return families


@lru_cache(maxsize=None)
def pure_terms(colour):
    return Counter(BASE.word_terms((colour,) * 8))


def pure_product_coefficient(row):
    groups = [[] for _ in range(3)]
    for coordinate in row:
        _, _, left_colour, right_colour = BASE.COORDINATES[coordinate]
        if left_colour != right_colour:
            return 0
        groups[left_colour].append(coordinate)
    value = 1
    for colour, group in enumerate(groups):
        value *= pure_terms(colour)[bytes(sorted(group))]
    return value


def raw_target_coefficient(row):
    """Coefficient of seed average minus H_0 H_1 H_2 at one row."""
    degree = BASE.row_degree(row)
    value = QQ(0)
    for seed in BASE.seed_columns():
        orbit = BASE.column_orbit(seed)
        hits = sum(output == row
                   for column in orbit
                   for output in BASE.column_rows(column)
                   if BASE.row_degree(output) == degree)
        value += QQ(hits, len(orbit))
    value -= pure_product_coefficient(row)
    return value


def frozen_degree3_tail_contribution(row):
    payload, _, _ = VERIFY3.decode_certificate()
    value = QQ(0)
    hit_columns = 0
    for word_text, multiplier, numerator, denominator in payload:
        column = (tuple(map(int, word_text)), bytes(multiplier))
        hits = sum(output == row
                   for actual_column in BASE.column_orbit(column)
                   for output in BASE.column_rows(actual_column))
        if hits:
            hit_columns += 1
            value += QQ(numerator, denominator) * hits
    return value, hit_columns


def early_stop_regression():
    """The minimal overlap that invalidated the first modular rank ledger."""
    prime = 1009
    higher = {2: {2: 1}}
    tails = ({1: 1, 2: 1}, {1: 1})

    def subtract(vector, reducer, scalar):
        for index, coefficient in reducer.items():
            value = (vector.get(index, 0) - scalar * coefficient) % prime
            if value:
                vector[index] = value
            else:
                vector.pop(index, None)

    # Reproduce the old two-stage early-stop algorithm.  Each higher reduction
    # stops at free row 1.  After the two tails cancel there, higher pivot 2 is
    # exposed but is incorrectly counted as a second transfer pivot.
    false_transfers = {}
    for source in tails:
        vector = dict(source)
        while vector and min(vector) in higher:
            pivot = min(vector)
            subtract(vector, higher[pivot], vector[pivot])
        while vector:
            pivot = min(vector)
            if pivot not in false_transfers:
                inverse = pow(vector[pivot], -1, prime)
                false_transfers[pivot] = {
                    index: coefficient * inverse % prime
                    for index, coefficient in vector.items()
                }
                break
            subtract(vector, false_transfers[pivot], vector[pivot])

    # A common echelon reduces against both families whenever a pivot is
    # exposed.  The second tail is dependent, so the true added rank is one.
    common = dict(higher)
    true_transfer_rank = 0
    for source in tails:
        vector = dict(source)
        while vector:
            pivot = min(vector)
            if pivot not in common:
                inverse = pow(vector[pivot], -1, prime)
                common[pivot] = {
                    index: coefficient * inverse % prime
                    for index, coefficient in vector.items()
                }
                true_transfer_rank += 1
                break
            subtract(vector, common[pivot], vector[pivot])
    require(len(false_transfers) == 2, "early-stop regression did not fire")
    require(true_transfer_rank == 1, "common-echelon regression changed")
    require(set(false_transfers) & set(higher) == {2},
            "regression no longer exposes the overlapping pivot")
    return len(false_transfers), true_transfer_rank


def encode_fraction(value):
    return [value.numerator, value.denominator]


def audit():
    degrees = Counter()
    for row, value in FUNCTIONAL.items():
        require(len(row) == 12 and row == BASE.canonical_row(row),
                "functional row is not a canonical balanced monomial")
        require(value, "zero stored functional value")
        degrees[BASE.row_degree(row)] += 1
    require(degrees == {2: 3, 4: 1}, "functional degree support changed")

    families = incident_source_columns()
    incident_counts = {degree: len(columns)
                       for degree, columns in families.items()}
    require(incident_counts == {2: 9, 3: 0, 4: 0},
            "incident source-column census changed")
    violations = []
    for degree, columns in families.items():
        for column in columns:
            pairing = column_pairing(column)
            if pairing:
                violations.append((degree, repr(column), pairing))
    require(not violations, "exact source-column annihilation failed")

    expanded, row_orbit_sizes = expanded_functional()
    actual_families = actual_incident_source_columns(expanded)
    actual_incident_counts = {
        degree: len(columns) for degree, columns in actual_families.items()
    }
    require(actual_incident_counts == {2: 56, 3: 0, 4: 0},
            "actual incident source-column census changed")
    actual_violations = []
    for degree, columns in actual_families.items():
        for column in columns:
            pairing = sum((expanded.get(row, QQ(0))
                           for row in BASE.column_rows(column)), QQ(0))
            if pairing:
                actual_violations.append((degree, repr(column), pairing))
    require(not actual_violations,
            "expanded actual source-column annihilation failed")

    rows2 = tuple(row for row in FUNCTIONAL if BASE.row_degree(row) == 2)
    row4, = (row for row in FUNCTIONAL if BASE.row_degree(row) == 4)
    degree2_target = tuple(raw_target_coefficient(row) for row in rows2)
    raw_degree4 = raw_target_coefficient(row4)
    certificate_tail, hit_columns = frozen_degree3_tail_contribution(row4)
    degree4_target = raw_degree4 + certificate_tail
    target_pairing = (
        sum((FUNCTIONAL[row] * coefficient
             for row, coefficient in zip(rows2, degree2_target)), QQ(0))
        + FUNCTIONAL[row4] * degree4_target
    )
    require(degree2_target == (QQ(-1), QQ(0), QQ(0)),
            "degree-two target coordinates changed")
    require(raw_degree4 == -1 and certificate_tail == 2
            and degree4_target == 1 and hit_columns == 3,
            "degree-four target coordinate changed")
    require(target_pairing == 3, "exact target pairing changed")

    false_rank, true_rank = early_stop_regression()
    ledger = {
        "functional_rows": len(FUNCTIONAL),
        "functional_degree_histogram": sorted(degrees.items()),
        "functional_value_histogram": sorted(Counter(
            FUNCTIONAL.values()).items()),
        "functional_row_orbit_size_histogram": sorted(
            row_orbit_sizes.items()
        ),
        "expanded_actual_functional_rows": len(expanded),
        "source_column_orbits": {"2": 3690, "3": 55798, "4": 913608},
        "incident_source_column_orbits": {
            str(degree): count for degree, count in incident_counts.items()
        },
        "source_column_violations": len(violations),
        "incident_actual_source_columns": {
            str(degree): count
            for degree, count in actual_incident_counts.items()
        },
        "actual_source_column_violations": len(actual_violations),
        "lower_kernel_tails_annihilated": 31584,
        "degree2_target_coordinates": [
            encode_fraction(value) for value in degree2_target
        ],
        "raw_degree4_target_coordinate": encode_fraction(raw_degree4),
        "degree3_certificate_hit_columns": hit_columns,
        "degree3_certificate_tail_coordinate": encode_fraction(
            certificate_tail
        ),
        "degree4_target_coordinate": encode_fraction(degree4_target),
        "target_pairing": encode_fraction(target_pairing),
        "early_stop_false_transfer_rank": false_rank,
        "common_echelon_true_transfer_rank": true_rank,
    }
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode("ascii")).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "chart25 degree-four exact-dual ledger changed")
    return ledger, digest


def main():
    ledger, digest = audit()
    print("chart 25 degree-four exact source-faithful dual: PASS")
    print("functional rows:", ledger["functional_rows"])
    print("incident source columns:",
          ledger["incident_source_column_orbits"])
    print("all source-column violations:",
          ledger["source_column_violations"])
    print("expanded actual rows / incident columns / violations:",
          ledger["expanded_actual_functional_rows"],
          ledger["incident_actual_source_columns"],
          ledger["actual_source_column_violations"])
    print("annihilated lower-kernel tails:",
          ledger["lower_kernel_tails_annihilated"])
    print("exact target pairing:", ledger["target_pairing"])
    print("sha256:", digest)


if __name__ == "__main__":
    main()
