#!/usr/bin/env python3
"""Exact sparse filtered syzygy behind the first degree-six Bockstein.

Two invariant mixed-generator columns have exactly the same image through
off-support degree five.  Their first difference is a twelve-row vector in
degree six, with coefficients +/-1.  In particular it evaluates to 1 on the
first zero-frequency row found by the fixed-tail degree-six calculation.

This is a small exact checker: no modular arithmetic or cached matrix is used.
"""

from collections import Counter
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


HERE = Path(__file__).resolve().parent
D5_PATH = HERE / "verify_n8_full_source_pure_product_degree5_lift.py"
SPEC = importlib.util.spec_from_file_location("n8_degree5", D5_PATH)
D5 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(D5)

MAXIMUM_DEGREE = 6
EXPECTED_LEDGER_SHA256 = (
    "e5c5e00e44b2553ffe14a012c2887b7e8d323634e1fdbc3cc03805ab4a8716b9"
)


def make_column(word, multiplier):
    return (
        D5.word_code(word),
        bytes(D5.COORDINATE_ID[coordinate] for coordinate in multiplier),
    )


COLUMN_PLUS = make_column(
    (1, 1, 0, 1, 1, 1, 1, 1),
    (
        (0, 1, 0, 0), (0, 1, 2, 2), (2, 3, 1, 2), (2, 4, 2, 2),
        (3, 4, 0, 0), (5, 6, 2, 2), (5, 7, 0, 2), (6, 7, 0, 0),
    ),
)
COLUMN_MINUS = make_column(
    (1, 1, 1, 1, 1, 2, 1, 2),
    (
        (0, 1, 0, 0), (0, 1, 2, 2), (2, 3, 2, 2), (2, 4, 0, 2),
        (3, 4, 0, 0), (5, 6, 1, 2), (5, 7, 0, 1), (6, 7, 0, 0),
    ),
)

EXPECTED_DEGREE_FIVE_ROW = bytes.fromhex("00043e59767d82a2e3e5f1f3")
EXPECTED_DEGREE_SIX_DIFFERENCE = {
    bytes.fromhex(row): coefficient for row, coefficient in (
        ("00040f597985a2c5e2e9eef3", 1),
        ("000410597785a2c2e2e9eef3", -1),
        ("0004195977859ea2e2e9eef3", -1),
        ("00041a5979859ba2e2e9eef3", 1),
        ("00042a59767d82a2e5f1f3fb", 1),
        ("00042b59767d82a2e3f1f3f8", -1),
        ("00043459767d82a2e3eff1f3", -1),
        ("00043559767d82a2e5ecf1f3", 1),
        ("00043e5976828da2bce5f1f3", 1),
        ("00043e5976828ea2bbe3f1f3", -1),
        ("00043e59768297a2b2e3f1f3", -1),
        ("00043e59768298a2b1e5f1f3", 1),
    )
}
SELECTED_ZERO_FREQUENCY_ROW = bytes.fromhex("00040f597985a2c5e2e9eef3")


def invariant_image(column):
    """Return the exact invariant-orbit image through degree six."""
    answer = Counter()
    for actual_column in D5.column_orbit(column):
        for output in D5.iter_column_outputs(actual_column):
            if D5.row_degree(output) <= MAXIMUM_DEGREE:
                if output == D5.canonical_row(output):
                    answer[output] += 1
    return answer


def audit():
    for column in (COLUMN_PLUS, COLUMN_MINUS):
        require(column == D5.canonical_column(column),
                "sparse witness column is not canonical")
        D5.verify_balanced_column(column)
        require(D5.column_minimum_degree(column) == 5,
                "sparse witness no longer starts in degree five")
        require(len(D5.column_orbit(column)) == 4,
                "sparse witness orbit size changed")

    plus = invariant_image(COLUMN_PLUS)
    minus = invariant_image(COLUMN_MINUS)
    lower_plus = Counter({row: value for row, value in plus.items()
                          if D5.row_degree(row) <= 5})
    lower_minus = Counter({row: value for row, value in minus.items()
                           if D5.row_degree(row) <= 5})
    require(lower_plus == lower_minus,
            "the exact relation fails below degree six")
    require(lower_plus == Counter({EXPECTED_DEGREE_FIVE_ROW: 1}),
            "the common degree-five leading row changed")

    difference = Counter()
    for row in set(plus) | set(minus):
        if D5.row_degree(row) == 6 and plus[row] != minus[row]:
            difference[row] = plus[row] - minus[row]
    require(dict(difference) == EXPECTED_DEGREE_SIX_DIFFERENCE,
            "the exact degree-six Bockstein tail changed")
    require(difference[SELECTED_ZERO_FREQUENCY_ROW] == 1,
            "the sparse relation no longer kills the selected leading dual")

    return {
        "vertices": 8,
        "endpoint_colours": 3,
        "filtration": "off-support coordinate degree",
        "witness_orbit_columns": 2,
        "witness_coefficients": [1, -1],
        "column_orbit_size": 4,
        "common_leading_degree": 5,
        "common_degree_five_rows": len(lower_plus),
        "first_difference_degree": 6,
        "degree_six_tail_rows": len(difference),
        "degree_six_tail_coefficient_histogram": dict(sorted(
            Counter(difference.values()).items()
        )),
        "selected_dual_pairing": difference[SELECTED_ZERO_FREQUENCY_ROW],
        "identity": "image(C_plus-C_minus) lies in J^6 and has the frozen 12-row initial form",
        "arithmetic": "exact integers",
    }


def main():
    ledger = audit()
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                "frozen sparse Bockstein ledger changed")
    print(
        "n=8 full-source degree-six sparse Bockstein: PASS; "
        f"columns={ledger['witness_orbit_columns']}, "
        f"tail={ledger['degree_six_tail_rows']}, "
        f"pairing={ledger['selected_dual_pairing']}"
    )
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
