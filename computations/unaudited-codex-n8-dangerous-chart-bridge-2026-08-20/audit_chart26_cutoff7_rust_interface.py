#!/usr/bin/env python3
"""Independent Python referee for the Rust mixed cutoff-7 interface."""

from __future__ import annotations

from collections import Counter
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
DEFAULT_CENSUS = (HERE.parent / "unaudited-codex-anchor-k-rust-2026-08-20"
                  / "results_chart26_cutoff7_direct.json")
OUT = HERE / "results_chart26_cutoff7_rust_interface_audit.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def first_layer(target):
    rows = set(target)
    columns = set()
    new_rows = set()
    for row in sorted(rows):
        for raw_column in BASE.incident_columns(row):
            column = PROBE.canonical_column(raw_column)
            if column in columns:
                continue
            if BASE.column_minimum_degree(column, PROBE.ANCHORS) >= 7:
                continue
            columns.add(column)
            for output in BASE.column_rows(column):
                if BASE.row_degree(output, PROBE.ANCHORS) < 7:
                    representative = PROBE.canonical_row(output)
                    if representative not in rows:
                        new_rows.add(representative)
    return len(new_rows), len(columns)


def audit(interface, census_path):
    interface_bytes = interface.read_bytes()
    with interface.open() as handle:
        header = json.loads(next(handle))
        require(header["format"]
                == "krenn-anchor-k-truncated-cutoff7-coupled-v1",
                "unexpected Rust cutoff interface format")
        require((header["row_count"], header["column_count"])
                == (13697, 25561), "Rust cutoff core dimensions changed")
        rows = tuple(bytes.fromhex(value) for value in header["rows_hex"])
        require(rows == tuple(sorted(set(rows))),
                "core row labels are not unique/sorted")
        require(all(PROBE.canonical_row(row) == row for row in rows),
                "core contains a noncanonical row")
        require(all(BASE.row_degree(row, PROBE.ANCHORS) < 7 for row in rows),
                "core contains a row outside cutoff")
        row_index = {row: index for index, row in enumerate(rows)}

        _actual_target, invariant_target = (
            EXPORT.invariant_target_below_cutoff()
        )
        expected_target = {
            row_index[row]: [value.numerator, value.denominator]
            for row, value in invariant_target.items() if row in row_index
        }
        observed_target = {
            index: [numerator, denominator]
            for index, numerator, denominator in header["target"]
        }
        require(observed_target == expected_target,
                "Rust core target differs from independent target")

        seen_columns = set()
        prior_key = None
        min_degree_histogram = Counter()
        support_histogram = Counter()
        for expected_index, line in enumerate(handle):
            record = json.loads(line)
            require(record["index"] == expected_index,
                    "Rust core column order has an index gap")
            column = (
                tuple(map(int, record["word"])),
                bytes(record["multiplier_cell_ids"]),
            )
            require(PROBE.canonical_column(column) == column,
                    "Rust emitted a noncanonical column")
            require(column not in seen_columns, "duplicate Rust core column")
            seen_columns.add(column)
            key = repr(column)
            require(prior_key is None or prior_key < key,
                    "Rust core columns left Python repr order")
            prior_key = key
            minimum = BASE.column_minimum_degree(column, PROBE.ANCHORS)
            require(minimum < 7, "Rust core column has minimum degree >=7")
            min_degree_histogram[minimum] += 1
            expected_entries = Counter()
            for output in BASE.column_rows(column):
                if BASE.row_degree(output, PROBE.ANCHORS) >= 7:
                    continue
                representative = PROBE.canonical_row(output)
                if representative in row_index:
                    expected_entries[row_index[representative]] += 1
            observed_entries = Counter(dict(record["entries"]))
            require(observed_entries == expected_entries,
                    f"literal cutoff entries differ at column {expected_index}")
            require(len(expected_entries) >= 2,
                    "Rust core retained a singleton/zero column")
            support_histogram[sum(expected_entries.values())] += 1
        require(len(seen_columns) == header["column_count"],
                "Rust core column line count changed")

    census = json.loads(census_path.read_text())
    require(census["seed_rows"] == 1017, "cutoff seed count changed")
    require(census["closure_rows"]
            == census["seed_rows"] + sum(a for a, _b in census["closure_layers"]),
            "Rust closure row layers do not add up")
    require(census["closure_columns"]
            == sum(b for _a, b in census["closure_layers"]),
            "Rust closure column layers do not add up")
    require(census["closure_rows"] - census["saturated_pivot_rows"]
            == census["coupled_rows"], "Rust peel row counts do not add up")
    require(sum(map(int, census["projected_histogram"].values()))
            == census["closure_columns"],
            "Rust projected histogram does not count all columns")
    require(census["closure_columns"]
            - census["projected_histogram"]["0"]
            == census["coupled_columns"],
            "Rust projected nonzero columns do not match core")
    observed_first_layer = first_layer(invariant_target)
    require(observed_first_layer == tuple(census["closure_layers"][0]),
            "Python/Rust first cutoff layer differs")

    core = {
        "status": "UNAUDITED exact Python referee of Rust interface",
        "chart": 26,
        "legacy_one_based_chart": 29,
        "cutoff": 7,
        "target_row_orbits": len(invariant_target),
        "python_first_layer_rows_columns": list(observed_first_layer),
        "rust_closure_rows_columns_layers": [
            census["closure_rows"], census["closure_columns"],
            len(census["closure_layers"]),
        ],
        "rust_core_rows_columns": [header["row_count"],
                                    header["column_count"]],
        "all_core_columns_literal_python_replay": True,
        "core_column_min_degree_histogram": {
            str(key): value for key, value in sorted(min_degree_histogram.items())
        },
        "core_column_retained_mass_histogram": {
            str(key): value for key, value in sorted(support_histogram.items())
        },
        "interface_bytes": len(interface_bytes),
        "interface_sha256": sha256(interface_bytes).hexdigest(),
    }
    encoded = json.dumps(core, sort_keys=True, separators=(",", ":"))
    core["result_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    return core


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--interface", type=Path, default=DEFAULT_INTERFACE)
    parser.add_argument("--census", type=Path, default=DEFAULT_CENSUS)
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()
    result = audit(args.interface, args.census)
    if args.write_results:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("cutoff7 Rust interface referee: PASS")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
