#!/usr/bin/env python3
"""Export the exact multiplier-degree-five boundary of the pinned lambda8."""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
AUDIT_PATH = HERE / "audit_degree8_dual_extension.py"
D8_PATH = HERE / "results_degree8_rust_cegar.json"
OUTPUT = HERE / "results_degree9_initial_census.json"
EXPECTED_D8_DUAL = "561546730a738ad3e3432ae5f5b63456735514148f32b77268debbebdae09d9d"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    audit = load(AUDIT_PATH, "degree9_initial_audit")
    source = audit.load_d7()
    d8 = json.loads(D8_PATH.read_text())
    require(d8["status"] == "EXTENDED_DUAL_EXACT_Q"
            and d8["exact_extended_dual_sha256"] == EXPECTED_D8_DUAL,
            "pinned lambda8 changed")
    record = d8["exact_extended_dual"]
    digest = sha256(json.dumps(record, separators=(",", ":")).encode()).hexdigest()
    require(digest == EXPECTED_D8_DUAL, "lambda8 record digest changed")
    functional = {
        bytes.fromhex(encoded): Fraction(numerator, denominator)
        for encoded, numerator, denominator in record
    }
    candidates = sorted(
        column for column in source.bounded_incident_columns(
            functional, maximum_output_degree=9
        ) if len(column[1]) == 5
    )
    violations = []
    for column in candidates:
        value = audit.pairing(audit.invariant_entries(source, column), functional)
        if value:
            violations.append((column, value))
    result = {
        "format": "n8-chart26-degree9-initial-census-v1",
        "status": "EXACT_BOUNDARY_CENSUS",
        "lambda8_sha256": digest,
        "lambda8_support": len(functional),
        "degree9_new_incident_columns": len(candidates),
        "degree9_boundary_violations": len(violations),
        "boundary_pairing_histogram": [
            [[value.numerator, value.denominator], count]
            for value, count in sorted(Counter(value for _, value in violations).items())
        ],
        "violating_columns": [
            {
                "word_code": column[0],
                "multiplier_hex": column[1].hex(),
                "pairing": [value.numerator, value.denominator],
            }
            for column, value in violations
        ],
        "scope_guard": "initial boundary of this selected lambda8 only; no degree9 conclusion",
    }
    logical = dict(result)
    result["logical_sha256"] = sha256(json.dumps(
        logical, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("degree9 initial candidates", len(candidates), "violations", len(violations),
          "digest", result["logical_sha256"])


if __name__ == "__main__":
    main()
