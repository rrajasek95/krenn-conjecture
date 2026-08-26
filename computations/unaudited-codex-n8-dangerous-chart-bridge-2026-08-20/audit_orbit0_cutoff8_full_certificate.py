#!/usr/bin/env python3
"""Independent raw-105/orbit-average referee for orbit-0 cutoff 8."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import argparse
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
RUST = IA.RUST
CERTIFICATE = RUST / "results_orbit0_cutoff8_full_quotient_certificate.json"
SOURCE_LEDGER = RUST / "results_orbit0_cutoff8_source_supports.jsonl"
SEED = HERE / "orbit0_cutoff8_seed.txt"
OUT = HERE / "results_orbit0_cutoff8_full_certificate_audit.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def invariant_column(column):
    answer = Counter()
    for output in BASE.column_rows(column):
        if BASE.row_degree(output, EXPORT.ANCHORS) < 8:
            answer[IA.canonical_row(output)] += 1
    return answer


def add_scaled(left, right, scale):
    for row, value in right.items():
        updated = left.get(row, 0) + scale * value
        if updated:
            left[row] = updated
        else:
            left.pop(row, None)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=CERTIFICATE)
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()
    certificate_path = args.certificate.resolve()
    data = json.loads(certificate_path.read_text())
    require(data["cutoff"] == 8
            and data["nonzero_source_terms"] == len(data["terms"]) > 0,
            "cutoff8 certificate metadata changed")
    require(data["max_denominator"] == 1,
            "cutoff8 certificate is no longer integral")
    require(data["seed_sha256"] == sha256(SEED.read_bytes()).hexdigest()
            == "d42b9270c0417dbc6aa879d74426cf743b11f376cda8ad521cf0367d1afdbe3a",
            "cutoff8 seed changed")
    require(data["source_support_ledger_sha256"]
            == sha256(SOURCE_LEDGER.read_bytes()).hexdigest()
            == "ca2d180e08646a121f28f6aa3b1683516064269a99638b4ced496da2e2aa83bf",
            "cutoff8 source ledger changed")

    actual_target = EXPORT.target_actual(8)
    invariant_target = Counter({row: Fraction(value)
                                for row, value in
                                EXPORT.invariant_target(actual_target).items()})
    require(len(actual_target) == sum(actual_target.values()) == 37513,
            "independent raw target census changed")
    require(len(invariant_target) == 58
            and sum(invariant_target.values()) == 37513,
            "independent invariant target census changed")

    replay = Counter()
    seen_columns = set()
    word_histogram = Counter()
    degree_histogram = Counter()
    coefficient_histogram = Counter()
    selected = []
    for number, term in enumerate(data["terms"]):
        coefficient = Fraction(*term["coefficient"])
        require(coefficient, f"zero term at {number}")
        column = (tuple(map(int, term["word"])),
                  bytes(term["multiplier_cell_ids"]))
        require(column not in seen_columns,
                f"duplicate source column at term {number}")
        seen_columns.add(column)
        require(IA.canonical_column(column) == column,
                f"noncanonical source column at term {number}")
        minimum = BASE.column_minimum_degree(column, EXPORT.ANCHORS)
        require(minimum < 8, f"source column {number} lies outside cutoff")
        vector = invariant_column(column)
        add_scaled(replay, vector, coefficient)
        selected.append((column, vector, coefficient))
        word_histogram[term["word"]] += 1
        degree_histogram[minimum] += 1
        coefficient_histogram[coefficient] += 1
    require(replay == invariant_target,
            "raw-105 orbit quotient certificate leaves a residual")

    mutation = Counter(replay)
    _column, first_vector, _coefficient = selected[0]
    add_scaled(mutation, first_vector, Fraction(1))
    require(mutation != invariant_target, "coefficient mutation did not fire")

    result = {
        "status": "UNAUDITED independent exact-Q source-faithful cutoff identity",
        "chart": 0,
        "cutoff": 8,
        "stabilizer_order": len(EXPORT.STABILIZER),
        "input_certificate_sha256": sha256(certificate_path.read_bytes()).hexdigest(),
        "input_certificate_logical_sha256": data["logical_sha256"],
        "source_support_ledger_sha256": sha256(SOURCE_LEDGER.read_bytes()).hexdigest(),
        "seed_sha256": sha256(SEED.read_bytes()).hexdigest(),
        "raw_target_rows": len(actual_target),
        "target_row_orbits": len(invariant_target),
        "source_terms": len(selected),
        "word_histogram": dict(sorted(word_histogram.items())),
        "minimum_degree_histogram": dict(sorted(degree_histogram.items())),
        "coefficient_histogram": {
            str(value): count for value, count in sorted(coefficient_histogram.items())
        },
        "maximum_numerator_bits": max(abs(value.numerator).bit_length()
                                      for value in coefficient_histogram),
        "maximum_denominator_bits": max(value.denominator.bit_length()
                                        for value in coefficient_histogram),
        "exact_raw_105_orbit_quotient_replay": True,
        "literal_actual_row_lift": (
            "Each listed source is a literal mixed H_w times an eight-cell "
            "multiplier. Reynolds averaging it over the 2304 anchor actions "
            "is a literal Q-combination of source columns. Total row-orbit "
            "mass equality and invariance imply equality on every labelled "
            "degree-12 monomial."
        ),
        "negative_coefficient_mutation_fired": True,
        "conclusion": "H0*H1*H2 belongs to I_mix + K_anchor^8 over Q",
        "global_I_mix_membership_proved": False,
        "remaining_K_degrees": [8, 9, 10, 11, 12],
    }
    encoded = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    if args.write_results:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("orbit0 cutoff8 raw-105 exact certificate referee: PASS")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
