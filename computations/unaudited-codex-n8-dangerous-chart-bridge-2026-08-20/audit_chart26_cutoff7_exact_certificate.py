#!/usr/bin/env python3
"""Exact-Q referee and singleton backsolve for a cutoff-7 core certificate."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import argparse
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXPORT_PATH = HERE / "export_chart26_cutoff7_seed.py"
SPEC = importlib.util.spec_from_file_location("cutoff7_export", EXPORT_PATH)
EXPORT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(EXPORT)
BASE = EXPORT.BASE
PROBE = EXPORT.PROBE
DEFAULT_INTERFACE = (HERE.parent / "unaudited-codex-anchor-k-rust-2026-08-20"
                     / "results_chart26_cutoff7_direct.jsonl")
DEFAULT_PIVOTS = HERE / "results_chart26_cutoff7_pivots.jsonl"
OUT = HERE / "results_chart26_cutoff7_exact_certificate_audit.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def as_fraction(value):
    if isinstance(value, list) and len(value) == 2:
        return Fraction(value[0], value[1])
    return Fraction(value)


def read_certificate(path):
    data = json.loads(path.read_text())
    raw = data.get("coefficients", data.get("certificate", data.get("solution")))
    require(raw is not None, "certificate has no coefficients/certificate/solution")
    answer = Counter()
    if isinstance(raw, dict):
        iterator = raw.items()
    else:
        iterator = raw
    for item in iterator:
        if len(item) == 3:
            index, numerator, denominator = item
            value = Fraction(numerator, denominator)
        else:
            index, encoded = item
            value = as_fraction(encoded)
        answer[int(index)] += value
    answer = Counter({index: value for index, value in answer.items() if value})
    require(data.get("prime") is None,
            "refusing a modular solution where an exact-Q certificate is required")
    return data, answer


def invariant_column(column):
    answer = Counter()
    for output in BASE.column_rows(column):
        if BASE.row_degree(output, PROBE.ANCHORS) < 7:
            answer[PROBE.canonical_row(output)] += 1
    return answer


def subtract_scaled(left, right, scale):
    for row, value in right.items():
        updated = left.get(row, 0) - scale * value
        if updated:
            left[row] = updated
        else:
            left.pop(row, None)


def audit(certificate_path, interface_path, pivots_path):
    certificate_path = certificate_path.resolve()
    interface_path = interface_path.resolve()
    pivots_path = pivots_path.resolve()
    repo_root = HERE.parent.parent
    certificate_label = str(certificate_path.relative_to(repo_root))
    certificate_data, core_coefficients = read_certificate(certificate_path)
    with interface_path.open() as handle:
        header = json.loads(next(handle))
        require(header["format"]
                == "krenn-anchor-k-truncated-cutoff7-coupled-v1",
                "wrong core interface format")
        require(sha256(interface_path.read_bytes()).hexdigest()
                == "487662cd76c11452bd8bf7feb343f290bffc3a623b18988c974d395ebdf55328",
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
    require(not core_residual, "exact-Q core certificate does not replay")

    # A hostile sign mutation must fail already on the coupled quotient;
    # singleton pivot columns cannot repair a changed core coordinate.
    mutation_index = next(iter(sorted(core_coefficients)))
    mutated = Counter(core_target)
    for index, coefficient in core_coefficients.items():
        if index == mutation_index:
            coefficient = -coefficient
        subtract_scaled(mutated, core_vectors[index], coefficient)
    require(mutated, "core coefficient sign mutation did not fire")

    _actual_target, invariant_target = EXPORT.invariant_target_below_cutoff()
    residual = Counter(invariant_target)
    full_terms = []
    for index, coefficient in sorted(core_coefficients.items()):
        column = core_columns[index]
        subtract_scaled(residual, invariant_column(column), coefficient)
        full_terms.append((coefficient, column, "core", index))
    require(not any(residual.get(row, 0) for row in core_rows),
            "core solution left a coupled row in full orbit coordinates")

    pivot_records = []
    pivot_order = {}
    with pivots_path.open() as handle:
        pivot_header = json.loads(next(handle))
        require(pivot_header == {
            "format": "anchor-k-singleton-pivot-ledger-v1",
            "pivot_count": 204490,
            "type": "header",
        }, "cutoff pivot header changed")
        for expected, line in enumerate(handle):
            record = json.loads(line)
            require(record["order"] == expected, "pivot order has a gap")
            row = bytes.fromhex(record["pivot_row_hex"])
            column = (tuple(map(int, record["word"])),
                      bytes(record["multiplier_cell_ids"]))
            pivot_records.append((row, column, record["coefficient"]))
            pivot_order[row] = expected
    require(len(pivot_records) == 204490
            and len(pivot_order) == len(pivot_records),
            "cutoff pivot ledger row count changed")
    require(sha256(pivots_path.read_bytes()).hexdigest()
            == "1619e4d7335f13c07beaf8105b50e02af85b0cbf9f46871d9380c5aaff97a656",
            "cutoff pivot ledger changed")

    nonzero_pivots = 0
    for order in range(len(pivot_records) - 1, -1, -1):
        row, column, pivot_coefficient = pivot_records[order]
        vector = invariant_column(column)
        require(vector[row] == pivot_coefficient,
                f"pivot coefficient changed at order {order}")
        for output_row in vector:
            require(output_row not in core_row_set,
                    f"pivot column {order} reaches the coupled core")
            require(output_row in pivot_order,
                    f"pivot column {order} reaches an unknown row")
            require(pivot_order[output_row] <= order,
                    f"pivot column {order} reaches a later pivot")
        coefficient = residual.get(row, Fraction(0)) / pivot_coefficient
        if coefficient:
            nonzero_pivots += 1
            subtract_scaled(residual, vector, coefficient)
            full_terms.append((coefficient, column, "pivot", order))
    require(not residual, "reverse singleton backsolve left an exact residual")

    denominators = Counter(value.denominator for value, _column, _kind, _index
                           in full_terms)
    maximum_numerator_bits = max(abs(value.numerator).bit_length()
                                 for value, _column, _kind, _index in full_terms)
    maximum_denominator_bits = max(value.denominator.bit_length()
                                   for value, _column, _kind, _index in full_terms)
    core = {
        "status": "UNAUDITED exact-Q source-faithful cutoff identity",
        "chart": 26,
        "legacy_one_based_chart": 29,
        "cutoff": 7,
        "input_certificate": certificate_label,
        "input_certificate_sha256": sha256(
            certificate_path.read_bytes()
        ).hexdigest(),
        "core_interface_sha256": sha256(interface_path.read_bytes()).hexdigest(),
        "pivot_ledger_sha256": sha256(pivots_path.read_bytes()).hexdigest(),
        "core_certificate_terms": len(core_coefficients),
        "nonzero_reverse_pivot_terms": nonzero_pivots,
        "total_orbit_average_terms": len(full_terms),
        "coefficient_denominator_histogram": {
            str(key): value for key, value in sorted(denominators.items())
        },
        "maximum_numerator_bits": maximum_numerator_bits,
        "maximum_denominator_bits": maximum_denominator_bits,
        "exact_rational_full_orbit_quotient_replay": True,
        "literal_actual_row_lift": (
            "Each source term is the 16-action orbit average. The checked "
            "integer quotient coordinate is its total coefficient on a row "
            "orbit; invariance makes coefficients uniform, so equality of "
            "all orbit totals is literal equality on every actual row."
        ),
        "negative_core_sign_mutation_fired": True,
        "conclusion": "H0*H1*H2 belongs to I_mix + K^7 over Q",
        "full_localized_chart_controlled": False,
        "remaining_K_degrees": [7, 8, 9, 10, 11, 12],
    }
    encoded = json.dumps(core, sort_keys=True, separators=(",", ":"))
    core["result_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    return core


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--interface", type=Path, default=DEFAULT_INTERFACE)
    parser.add_argument("--pivots", type=Path, default=DEFAULT_PIVOTS)
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()
    result = audit(args.certificate, args.interface, args.pivots)
    if args.write_results:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("cutoff7 exact certificate referee: PASS")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
