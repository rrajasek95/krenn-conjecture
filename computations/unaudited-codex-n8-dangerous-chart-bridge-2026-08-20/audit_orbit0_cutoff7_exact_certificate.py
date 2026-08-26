#!/usr/bin/env python3
"""Exact-Q raw-105 referee for the orbit-0 cutoff-7 certificate."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import argparse
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
INTERFACE_AUDIT_PATH = HERE / "audit_orbit0_cutoff7_rust_interface.py"
SPEC = importlib.util.spec_from_file_location("orbit0_interface_audit",
                                              INTERFACE_AUDIT_PATH)
IA = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(IA)
EXPORT = IA.EXPORT
BASE = IA.BASE
RUST = IA.RUST
DEFAULT_CERTIFICATE = RUST / "results_orbit0_cutoff7_exact_core_certificate.json"
DEFAULT_INTERFACE = RUST / "results_orbit0_cutoff7_direct.jsonl"
DEFAULT_PIVOTS = RUST / "results_orbit0_cutoff7_pivots.jsonl"
OUT = HERE / "results_orbit0_cutoff7_exact_certificate_audit.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def subtract_scaled(left, right, scale):
    for row, value in right.items():
        updated = left.get(row, 0) - scale * value
        if updated:
            left[row] = updated
        else:
            left.pop(row, None)


def invariant_column(column):
    answer = Counter()
    for output in BASE.column_rows(column):
        if BASE.row_degree(output, EXPORT.ANCHORS) < 7:
            answer[IA.canonical_row(output)] += 1
    return answer


def audit(certificate_path, interface_path, pivots_path):
    certificate_data = json.loads(certificate_path.read_text())
    require(certificate_data.get("exact_integer_replay") is True,
            "certificate is not marked exact integer")
    require(certificate_data.get("matrix_sha256")
            == "bcd16826c7a30f7d1f0c1eb82229fde1ed5fdcf6f5b1f2a33244370b0d322f6d",
            "certificate names the wrong core interface")
    core_coefficients = Counter({
        int(index): Fraction(value)
        for index, value in certificate_data["solution"] if value
    })
    require(0 < len(core_coefficients) <= 1519,
            "exact core certificate support is empty or out of range")

    with interface_path.open() as handle:
        header = json.loads(next(handle))
        require(sha256(interface_path.read_bytes()).hexdigest()
                == "bcd16826c7a30f7d1f0c1eb82229fde1ed5fdcf6f5b1f2a33244370b0d322f6d",
                "core interface changed")
        core_rows = tuple(bytes.fromhex(value) for value in header["rows_hex"])
        core_row_set = set(core_rows)
        core_target = Counter({index: Fraction(numerator, denominator)
                               for index, numerator, denominator
                               in header["target"]})
        core_vectors = {}
        core_columns = {}
        for line in handle:
            record = json.loads(line)
            index = record["index"]
            if index not in core_coefficients:
                continue
            core_vectors[index] = Counter(dict(record["entries"]))
            core_columns[index] = (
                tuple(map(int, record["word"])),
                bytes(record["multiplier_cell_ids"]),
            )
    require(set(core_coefficients) == set(core_columns),
            "certificate references an absent core column")
    core_residual = Counter(core_target)
    for index, coefficient in core_coefficients.items():
        subtract_scaled(core_residual, core_vectors[index], coefficient)
    require(not core_residual, "exact-Z core certificate does not replay")

    mutation_index = min(core_coefficients)
    mutation = Counter(core_target)
    for index, coefficient in core_coefficients.items():
        if index == mutation_index:
            coefficient = -coefficient
        subtract_scaled(mutation, core_vectors[index], coefficient)
    require(mutation, "core sign mutation did not fire")

    actual_target = EXPORT.target_actual(7)
    invariant_target = EXPORT.invariant_target(actual_target)
    residual = Counter({row: Fraction(value)
                        for row, value in invariant_target.items()})
    full_terms = []
    for index, coefficient in sorted(core_coefficients.items()):
        column = core_columns[index]
        subtract_scaled(residual, invariant_column(column), coefficient)
        full_terms.append((coefficient, column, "core", index))
    require(not any(residual.get(row, 0) for row in core_rows),
            "core solution left a coupled row in raw-105 quotient")

    pivot_records = []
    pivot_order = {}
    with pivots_path.open() as handle:
        pivot_header = json.loads(next(handle))
        require(pivot_header == {
            "format": "anchor-k-singleton-pivot-ledger-v1",
            "pivot_count": 2075,
            "type": "header",
        }, "pivot header changed")
        for expected, line in enumerate(handle):
            record = json.loads(line)
            require(record["order"] == expected, "pivot order gap")
            row = bytes.fromhex(record["pivot_row_hex"])
            column = (tuple(map(int, record["word"])),
                      bytes(record["multiplier_cell_ids"]))
            pivot_records.append((row, column, record["coefficient"]))
            pivot_order[row] = expected
    require(len(pivot_records) == len(pivot_order) == 2075,
            "pivot ledger size changed")
    require(sha256(pivots_path.read_bytes()).hexdigest()
            == "40daf028bf76471de90fe84798d9446a5dde78667a3ec05335d11dcbfacdae69",
            "pivot ledger changed")

    nonzero_pivots = 0
    for order in range(len(pivot_records) - 1, -1, -1):
        row, column, pivot_coefficient = pivot_records[order]
        vector = invariant_column(column)
        require(vector[row] == pivot_coefficient,
                f"pivot coefficient changed at {order}")
        for output_row in vector:
            require(output_row not in core_row_set,
                    f"pivot {order} reaches coupled core")
            require(output_row in pivot_order,
                    f"pivot {order} reaches unknown row")
            require(pivot_order[output_row] <= order,
                    f"pivot {order} reaches later row")
        coefficient = residual.get(row, Fraction(0)) / pivot_coefficient
        if coefficient:
            nonzero_pivots += 1
            subtract_scaled(residual, vector, coefficient)
            full_terms.append((coefficient, column, "pivot", order))
    require(not residual, "reverse singleton backsolve left residual")

    denominator_histogram = Counter(value.denominator
                                    for value, _col, _kind, _index in full_terms)
    core_word_histogram = Counter(
        "".join(map(str, core_columns[index][0]))
        for index in core_coefficients
    )
    full_word_histogram = Counter(
        "".join(map(str, column[0]))
        for _value, column, _kind, _index in full_terms
    )
    core_minimum_degree_histogram = Counter(
        BASE.column_minimum_degree(core_columns[index], EXPORT.ANCHORS)
        for index in core_coefficients
    )
    full_minimum_degree_histogram = Counter(
        BASE.column_minimum_degree(column, EXPORT.ANCHORS)
        for _value, column, _kind, _index in full_terms
    )
    result = {
        "status": "UNAUDITED independent exact-Q source-faithful cutoff identity",
        "chart": 0,
        "cutoff": 7,
        "stabilizer_order": len(EXPORT.STABILIZER),
        "input_certificate_sha256": sha256(certificate_path.read_bytes()).hexdigest(),
        "core_interface_sha256": sha256(interface_path.read_bytes()).hexdigest(),
        "pivot_ledger_sha256": sha256(pivots_path.read_bytes()).hexdigest(),
        "raw_target_rows": len(actual_target),
        "target_row_orbits": len(invariant_target),
        "core_certificate_terms": len(core_coefficients),
        "nonzero_reverse_pivot_terms": nonzero_pivots,
        "total_orbit_average_terms": len(full_terms),
        "coefficient_denominator_histogram": {
            str(key): value for key, value in sorted(denominator_histogram.items())
        },
        "core_word_histogram": dict(sorted(core_word_histogram.items())),
        "full_word_histogram": dict(sorted(full_word_histogram.items())),
        "core_minimum_degree_histogram": dict(sorted(
            core_minimum_degree_histogram.items()
        )),
        "full_minimum_degree_histogram": dict(sorted(
            full_minimum_degree_histogram.items()
        )),
        "full_certificate": [
            {
                "coefficient": [value.numerator, value.denominator],
                "word": "".join(map(str, column[0])),
                "multiplier_cell_ids": list(column[1]),
                "provenance": kind,
                "provenance_index": index,
            }
            for value, column, kind, index in full_terms
        ],
        "maximum_numerator_bits": max(abs(value.numerator).bit_length()
                                      for value, _col, _kind, _index in full_terms),
        "maximum_denominator_bits": max(value.denominator.bit_length()
                                        for value, _col, _kind, _index in full_terms),
        "exact_rational_full_orbit_quotient_replay": True,
        "literal_actual_row_lift": (
            "Each term is the Reynolds average of one literal 105-output "
            "source column over the 2304 chart actions. Quotient coordinates "
            "are total row-orbit masses; invariance therefore lifts the zero "
            "quotient residual to zero on every labelled degree-12 monomial."
        ),
        "negative_core_sign_mutation_fired": True,
        "conclusion": "H0*H1*H2 belongs to I_mix + K_anchor^7 over Q",
        "global_I_mix_membership_proved": False,
        "remaining_K_degrees": [7, 8, 9, 10, 11, 12],
    }
    encoded = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=DEFAULT_CERTIFICATE)
    parser.add_argument("--interface", type=Path, default=DEFAULT_INTERFACE)
    parser.add_argument("--pivots", type=Path, default=DEFAULT_PIVOTS)
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()
    result = audit(args.certificate.resolve(), args.interface.resolve(),
                   args.pivots.resolve())
    if args.write_results:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("orbit0 cutoff7 exact certificate referee: PASS")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
