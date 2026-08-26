#!/usr/bin/env python3
"""Expand the 301 invariant R8 rows to labelled orbit data exactly."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import argparse
import importlib.util
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
OUT = HERE / "results_r8_orbit_expansion.json"


def require(condition: bool, detail: str) -> None:
    if not condition:
        raise RuntimeError(detail)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--residual", type=Path, default=R8_PATH)
    parser.add_argument("--output", type=Path, default=OUT)
    args = parser.parse_args()
    residual_path = args.residual.resolve()
    raw = json.loads(residual_path.read_text())
    records = []
    actual_coefficients = Counter()
    total_labelled_rows = 0
    stabilizer_histogram = Counter()
    orbit_size_histogram = Counter()
    for row_hex, numerator, denominator in raw["residual"]:
        row = bytes.fromhex(row_hex)
        require(BASE.row_degree(row, EXPORT.ANCHORS) == 8,
                "R8 row has wrong K degree")
        orbit = EXPORT.row_orbit(row)
        require(min(orbit) == row, "R8 row is not canonical")
        orbit_size = len(orbit)
        stabilizer_size = len(EXPORT.STABILIZER) // orbit_size
        quotient_coefficient = Fraction(numerator, denominator)
        actual_coefficient = quotient_coefficient / orbit_size
        total_labelled_rows += orbit_size
        stabilizer_histogram[stabilizer_size] += 1
        orbit_size_histogram[orbit_size] += 1
        actual_coefficients[actual_coefficient] += orbit_size
        records.append({
            "row": row_hex,
            "quotient_coefficient": [numerator, denominator],
            "orbit_size": orbit_size,
            "row_stabilizer_order": stabilizer_size,
            "actual_row_coefficient": [actual_coefficient.numerator,
                                       actual_coefficient.denominator],
        })
    expected_orbits = raw.get("residual_quotient_orbits", len(raw["residual"]))
    require(len(records) == expected_orbits > 0,
            "residual invariant support changed during replay")

    result = {
        "status": "UNAUDITED exact orbit-normalization audit",
        "input_r8_path": str(residual_path),
        "input_r8_sha256": sha256(residual_path.read_bytes()).hexdigest(),
        "stabilizer_order": len(EXPORT.STABILIZER),
        "invariant_row_orbits": len(records),
        "labelled_rows": total_labelled_rows,
        "row_orbit_size_histogram": dict(sorted(orbit_size_histogram.items())),
        "row_stabilizer_order_histogram": dict(sorted(
            stabilizer_histogram.items())),
        "labelled_row_coefficient_histogram": {
            str(value): count for value, count in sorted(actual_coefficients.items())
        },
        "normalization": (
            "R8 quotient coefficients are total row-orbit masses; the "
            "coefficient of each labelled row is quotient_mass/orbit_size"
        ),
        "all_actual_coefficients_integral": all(
            value.denominator == 1 for value in actual_coefficients
        ),
        "orbits": records,
    }
    encoded = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("R8 labelled orbit expansion: PASS")
    print("orbits/labelled rows:", len(records), total_labelled_rows)
    print("orbit sizes:", dict(sorted(orbit_size_histogram.items())))
    print("actual coefficients:", {
        str(value): count for value, count in sorted(actual_coefficients.items())
    })
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
