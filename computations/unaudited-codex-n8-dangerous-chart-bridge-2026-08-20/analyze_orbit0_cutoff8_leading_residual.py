#!/usr/bin/env python3
"""Extract the exact K-degree-8 residual of the sparse cutoff-8 lift."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
IA_PATH = HERE / "audit_orbit0_cutoff7_rust_interface.py"
SPEC = importlib.util.spec_from_file_location("orbit0_interface_audit", IA_PATH)
IA = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(IA)
EXPORT = IA.EXPORT
BASE = IA.BASE
CERTIFICATE = HERE / "results_orbit0_cutoff8_sparse_full_certificate.json"
DUAL = HERE / "results_orbit0_cutoff9_exact_dual_audit.json"
OUT = HERE / "results_orbit0_cutoff8_leading_residual.json"


def add_scaled(left, right, scale):
    for row, value in right.items():
        updated = left.get(row, 0) + scale * value
        if updated:
            left[row] = updated
        else:
            left.pop(row, None)


def main():
    data = json.loads(CERTIFICATE.read_text())
    target_all = EXPORT.invariant_target(EXPORT.target_actual(9))
    residual = Counter({row: Fraction(value) for row, value in target_all.items()
                        if BASE.row_degree(row, EXPORT.ANCHORS) == 8})
    for term in data["terms"]:
        coefficient = Fraction(*term["coefficient"])
        column = (tuple(map(int, term["word"])),
                  bytes(term["multiplier_cell_ids"]))
        degree8 = Counter()
        for output in BASE.column_rows(column):
            if BASE.row_degree(output, EXPORT.ANCHORS) == 8:
                degree8[IA.canonical_row(output)] += 1
        add_scaled(residual, degree8, -coefficient)
    residual += Counter()

    dual_data = json.loads(DUAL.read_text())
    with (IA.RUST / "results_orbit0_cutoff9_direct.jsonl").open() as handle:
        header = json.loads(next(handle))
    rows = tuple(bytes.fromhex(value) for value in header["rows_hex"])
    dual = {rows[index]: Fraction(numerator, denominator)
            for index, numerator, denominator in dual_data["dual"]}
    pairing = sum(dual.get(row, 0) * value for row, value in residual.items())
    if pairing != 2304:
        raise RuntimeError(f"leading residual pairs {pairing}, expected 2304")

    coefficient_histogram = Counter(residual.values())
    support_degree_histogram = Counter(BASE.row_degree(row, EXPORT.ANCHORS)
                                       for row in residual)
    result = {
        "status": "exact invariant-quotient leading residual",
        "chart": 0,
        "input_certificate_sha256": sha256(CERTIFICATE.read_bytes()).hexdigest(),
        "dual_audit_sha256": sha256(DUAL.read_bytes()).hexdigest(),
        "K_degree": 8,
        "support_rows": len(residual),
        "support_degree_histogram": dict(sorted(support_degree_histogram.items())),
        "coefficient_histogram": {
            str(value): count for value, count in sorted(coefficient_histogram.items())
        },
        "dual_pairing": [pairing.numerator, pairing.denominator],
        "residual": [[row.hex(), value.numerator, value.denominator]
                     for row, value in sorted(residual.items())],
        "next_target_power_route": (
            "Modulo I_mix, T is represented by this K-degree-8 class plus "
            "higher K-degree terms. Hence T^2 starts in K-degree 16. Test "
            "the square of this leading class in the degree-24 associated "
            "graded source before constructing a full target-square closure."
        ),
    }
    encoded = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("orbit0 cutoff8 leading residual: PASS")
    print("support/pairing:", len(residual), pairing)
    print("coefficient histogram:", dict(sorted(coefficient_histogram.items())))
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
