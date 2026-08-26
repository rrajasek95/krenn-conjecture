#!/usr/bin/env python3
"""Exact-Q, source-faithful dual for the orbit-0 cutoff-9 obstruction."""

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
RUST = IA.RUST
INTERFACE = RUST / "results_orbit0_cutoff9_direct.jsonl"
SOURCE_LEDGER = RUST / "results_orbit0_cutoff9_source_supports.jsonl"
P1009 = RUST / "results_orbit0_cutoff9_overlap_p1009.json"
P1013 = RUST / "results_orbit0_cutoff9_overlap_p1013.json"
SEED = HERE / "orbit0_cutoff9_seed.txt"
OUT = HERE / "results_orbit0_cutoff9_exact_dual_audit.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def rational_lift(left, right):
    values = set()
    for denominator in range(1, 33):
        for numerator in range(-512, 513):
            value = Fraction(numerator, denominator)
            if (value.numerator * pow(value.denominator, -1, 1009) % 1009
                    == left
                    and value.numerator * pow(value.denominator, -1, 1013) % 1013
                    == right):
                values.add(value)
    require(len(values) == 1,
            f"two-prime coefficient has {len(values)} small rational lifts")
    return values.pop()


def main():
    mod1009 = json.loads(P1009.read_text())
    mod1013 = json.loads(P1013.read_text())
    require(mod1009["prime"] == 1009 and mod1013["prime"] == 1013,
            "wrong modular inputs")
    require(mod1009["rank"] == mod1013["rank"] == 50420,
            "two-prime ranks differ")
    require(not mod1009["target_in_image"]
            and not mod1013["target_in_image"],
            "a modular target unexpectedly entered the image")
    left = dict(mod1009["left_dual"])
    right = dict(mod1013["left_dual"])
    require(set(left) == set(right) and len(left) == 37,
            "two-prime dual supports differ")
    dual = {row: rational_lift(left[row], right[row]) for row in left}

    with INTERFACE.open() as handle:
        header = json.loads(next(handle))
        require((header["row_count"], header["column_count"])
                == (80894, 115839), "cutoff9 core dimensions changed")
        rows = tuple(bytes.fromhex(value) for value in header["rows_hex"])
        target = Counter({row: Fraction(numerator, denominator)
                          for row, numerator, denominator in header["target"]})
        for expected, line in enumerate(handle):
            record = json.loads(line)
            require(record["index"] == expected, "core column index gap")
            pairing = sum(dual.get(row, 0) * value
                          for row, value in record["entries"])
            require(pairing == 0,
                    f"exact dual hits core column {expected} by {pairing}")
    target_pairing = sum(dual.get(row, 0) * value
                         for row, value in target.items())
    require(target_pairing == 2304,
            f"exact target pairing changed to {target_pairing}")

    dual_by_row = {rows[index]: value for index, value in dual.items()}
    actual_target = EXPORT.target_actual(9)
    invariant_target = EXPORT.invariant_target(actual_target)
    invariant_pairing = sum(dual_by_row.get(row, 0) * value
                            for row, value in invariant_target.items())
    require(invariant_pairing == target_pairing == 2304,
            "raw invariant target pairing differs from core target")

    # Exhaust every literal source-column orbit which could possibly pair
    # nontrivially.  A column outside this incident union has no output in the
    # 37-row support and hence pairs zero tautologically.
    incident_columns = set()
    for row in dual_by_row:
        for raw_column in BASE.incident_columns(row):
            column = IA.canonical_column(raw_column)
            if BASE.column_minimum_degree(column, EXPORT.ANCHORS) < 9:
                incident_columns.add(column)
    touched_rows = Counter()
    for number, column in enumerate(sorted(incident_columns, key=repr)):
        pairing = Fraction()
        for output in BASE.column_rows(column):
            if BASE.row_degree(output, EXPORT.ANCHORS) >= 9:
                continue
            representative = IA.canonical_row(output)
            coefficient = dual_by_row.get(representative, 0)
            if coefficient:
                touched_rows[representative] += 1
                pairing += coefficient
        require(pairing == 0,
                f"exact dual hits literal incident column {number} by {pairing}")
    require(set(touched_rows) == set(dual_by_row),
            "some dual row was not exercised by a source column")

    # The source ledger supplies an independent cheap all-column check in the
    # closed component.  Extend the core cochain by zero on all peeled rows.
    ledger_columns = 0
    ledger_pairing_nonzeros = 0
    with SOURCE_LEDGER.open() as handle:
        ledger_header = json.loads(next(handle))
        require(ledger_header == {
            "core_count": 115839,
            "format": "anchor-k-source-support-ledger-v1",
            "pivot_count": 71492,
            "type": "header",
        }, "source ledger header changed")
        for line in handle:
            record = json.loads(line)
            ledger_columns += 1
            pairing = sum(dual_by_row.get(bytes.fromhex(row), 0) * value
                          for row, value in record["original_entries"])
            if pairing:
                ledger_pairing_nonzeros += 1
    require(ledger_columns == 187331 and ledger_pairing_nonzeros == 0,
            "zero-extended dual hits a closed source-ledger column")

    mutation_row = min(dual)
    mutated = dict(dual)
    mutated[mutation_row] += 1
    mutation_fired = False
    with INTERFACE.open() as handle:
        next(handle)
        for line in handle:
            record = json.loads(line)
            if sum(mutated.get(row, 0) * value
                   for row, value in record["entries"]):
                mutation_fired = True
                break
    require(mutation_fired, "dual coefficient mutation did not fire")

    degree_histogram = Counter(BASE.row_degree(row, EXPORT.ANCHORS)
                               for row in dual_by_row)
    result = {
        "status": "UNAUDITED independent exact-Q source-faithful dual",
        "chart": 0,
        "cutoff": 9,
        "stabilizer_order": len(EXPORT.STABILIZER),
        "interface_sha256": sha256(INTERFACE.read_bytes()).hexdigest(),
        "source_ledger_sha256": sha256(SOURCE_LEDGER.read_bytes()).hexdigest(),
        "seed_sha256": sha256(SEED.read_bytes()).hexdigest(),
        "mod1009_sha256": sha256(P1009.read_bytes()).hexdigest(),
        "mod1013_sha256": sha256(P1013.read_bytes()).hexdigest(),
        "core_rows": len(rows),
        "core_columns": header["column_count"],
        "common_modular_rank": 50420,
        "dual_terms": len(dual),
        "dual_degree_histogram": dict(sorted(degree_histogram.items())),
        "dual": [[index, value.numerator, value.denominator]
                 for index, value in sorted(dual.items())],
        "target_pairing": [target_pairing.numerator, target_pairing.denominator],
        "literal_incident_column_orbits_checked": len(incident_columns),
        "closed_source_ledger_columns_checked": ledger_columns,
        "exact_core_annihilation": True,
        "exact_literal_incident_source_annihilation": True,
        "exact_zero_extended_full_component_annihilation": True,
        "negative_dual_mutation_fired": True,
        "conclusion": "H0*H1*H2 does not belong to I_mix + K_anchor^9 over Q",
        "global_exponent_one_consequence": (
            "Since I_mix is contained in I_mix+K_anchor^9, this proves "
            "H0*H1*H2 is not in I_mix. No other anchor chart can complete "
            "the exponent-one K^13 ladder; the remaining proof must use a "
            "target power/radical or a genuinely localized unit identity."
        ),
    }
    encoded = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("orbit0 cutoff9 exact dual referee: PASS")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
