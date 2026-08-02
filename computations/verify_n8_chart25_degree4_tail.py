#!/usr/bin/env python3
"""Exact actual-row audit of the chart-25 degree-four certificate tail."""

from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXPECTED_LEDGER_SHA256 = (
    "3148ee5faf5a11f0aa9282e12b31b868d97d44789dc848ee3fce96f66e65d152"
)
QQ = Fraction


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BASE = load("n8_chart25_degree2_tail4", "analyze_n8_chart25_degree2_lift.py")
VERIFY3 = load("n8_chart25_verify3_tail4", "verify_n8_chart25_degree3_lift.py")


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def audit():
    payload, _, _ = VERIFY3.decode_certificate()
    require(len(payload) == 1634, "degree-three certificate size changed")
    actual, _ = BASE.corrected_residual_at_degree(4, {})
    actual = defaultdict(QQ, actual)
    for word_text, multiplier, numerator, denominator in payload:
        column = (tuple(map(int, word_text)), bytes(multiplier))
        require(BASE.canonical_column(column) == column,
                "noncanonical certificate column")
        scalar = QQ(numerator, denominator)
        for actual_column in BASE.column_orbit(column):
            for row in BASE.column_rows(actual_column):
                if BASE.row_degree(row) != 4:
                    continue
                value = actual[row] + scalar
                if value:
                    actual[row] = value
                else:
                    actual.pop(row, None)
    actual = dict(actual)
    quotient = {}
    for row, value in actual.items():
        for transform in BASE.TRANSFORMS:
            image = bytes(sorted(transform[index] for index in row))
            require(actual.get(image) == value,
                    "degree-four tail lost stabilizer invariance")
        if row == BASE.canonical_row(row):
            quotient[row] = value
    histogram = Counter(quotient.values())
    ledger = {
        "certificate_columns": len(payload),
        "actual_rows": len(actual),
        "row_orbits": len(quotient),
        "quotient_value_histogram": sorted(
            (value.numerator, value.denominator, count)
            for value, count in histogram.items()
        ),
    }
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode("ascii")).hexdigest()
    require(digest == EXPECTED_LEDGER_SHA256,
            "degree-four tail ledger changed")
    return ledger, digest


def main():
    ledger, digest = audit()
    print("chart 25 exact degree-four tail: PASS")
    print("actual rows / stabilizer orbits:",
          ledger["actual_rows"], ledger["row_orbits"])
    print("sha256:", digest)


if __name__ == "__main__":
    main()
