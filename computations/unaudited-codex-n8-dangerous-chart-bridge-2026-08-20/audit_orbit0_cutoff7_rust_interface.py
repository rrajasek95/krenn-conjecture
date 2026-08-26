#!/usr/bin/env python3
"""Independent Python referee for the orbit-0 mixed cutoff-7 Rust core."""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
from hashlib import sha256
import argparse
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXPORT_PATH = HERE / "export_orbit0_cutoff_seed.py"
SPEC = importlib.util.spec_from_file_location("orbit0_export", EXPORT_PATH)
EXPORT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(EXPORT)
BASE = EXPORT.BASE
RUST = HERE.parent / "unaudited-codex-anchor-k-rust-2026-08-20"
DEFAULT_RAW_SEED = RUST / "zero0_cutoff7_raw_seed.txt"
DEFAULT_INTERFACE = RUST / "results_orbit0_cutoff7_direct.jsonl"
DEFAULT_CENSUS = RUST / "results_orbit0_cutoff7_closure.json"
OUT = HERE / "results_orbit0_cutoff7_rust_interface_audit.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


@lru_cache(maxsize=None)
def canonical_row(row):
    return min(bytes(sorted(transform[cell] for cell in row))
               for transform in EXPORT.TRANSFORMS)


def transform_column(column, action):
    word, multiplier = column
    sites, colours = EXPORT.STABILIZER[action]
    transformed_word = [None] * BASE.N
    for site, colour in enumerate(word):
        transformed_word[sites[site]] = colours[colour]
    transformed_multiplier = bytes(sorted(
        EXPORT.TRANSFORMS[action][cell] for cell in multiplier
    ))
    return tuple(transformed_word), transformed_multiplier


@lru_cache(maxsize=None)
def canonical_column(column):
    return min((transform_column(column, action)
                for action in range(len(EXPORT.STABILIZER))), key=repr)


def parse_raw_seed(path):
    lines = path.read_text().splitlines()
    require(lines[0] == "KRENN_ANCHOR_K_SEED_V1", "wrong raw seed magic")
    require(lines[1] == "CUTOFF 7", "wrong raw seed cutoff")
    anchors = bytes.fromhex(lines[2].split()[1])
    actions = []
    target = Counter()
    for line in lines[3:]:
        fields = line.split()
        if fields[0] == "EXPECTED":
            require(tuple(map(int, fields[1:])) == (0, 0, 0, 0, 0),
                    "raw seed controls changed")
        elif fields[0] == "ACTION":
            actions.append((tuple(map(int, fields[1])),
                            tuple(map(int, fields[2]))))
        elif fields[0] == "ROW":
            require(int(fields[3]) == 1, "raw seed has fractional target")
            target[bytes.fromhex(fields[1])] += int(fields[2])
        else:
            raise RuntimeError(f"unknown raw seed record {fields[0]}")
    return anchors, tuple(actions), target


def first_layer(target):
    rows = set(target)
    columns = set()
    new_rows = set()
    for row in sorted(rows):
        for raw_column in BASE.incident_columns(row):
            column = canonical_column(raw_column)
            if column in columns:
                continue
            if BASE.column_minimum_degree(column, EXPORT.ANCHORS) >= 7:
                continue
            columns.add(column)
            for output in BASE.column_rows(column):
                if BASE.row_degree(output, EXPORT.ANCHORS) >= 7:
                    continue
                representative = canonical_row(output)
                if representative not in rows:
                    new_rows.add(representative)
    return len(new_rows), len(columns)


def audit(raw_seed_path, interface_path, census_path):
    raw_anchors, raw_actions, raw_target = parse_raw_seed(raw_seed_path)
    expected_actual = EXPORT.target_actual(7)
    require(raw_anchors == bytes(sorted(EXPORT.ANCHORS)),
            "raw seed anchors differ from independent orbit-0 anchors")
    require(raw_actions == EXPORT.STABILIZER,
            "raw seed actions differ from independent 2304 stabilizer")
    require(raw_target == expected_actual,
            "raw seed target differs from independent H0H1H2 expansion")
    invariant_target = EXPORT.invariant_target(expected_actual)
    require(len(invariant_target) == 36 and sum(invariant_target.values()) == 12169,
            "independent invariant target census changed")

    with interface_path.open() as handle:
        header = json.loads(next(handle))
        require(header["format"] == "krenn-anchor-k-truncated-cutoff7-coupled-v1",
                "unexpected core format")
        require((header["row_count"], header["column_count"]) == (363, 1519),
                "orbit-0 core dimensions changed")
        rows = tuple(bytes.fromhex(value) for value in header["rows_hex"])
        require(rows == tuple(sorted(set(rows))), "core rows not unique/sorted")
        require(all(canonical_row(row) == row for row in rows),
                "core contains noncanonical row")
        require(all(BASE.row_degree(row, EXPORT.ANCHORS) < 7 for row in rows),
                "core row lies outside cutoff")
        row_index = {row: index for index, row in enumerate(rows)}

        seen = set()
        prior_key = None
        minimum_degree_histogram = Counter()
        support_histogram = Counter()
        for expected_index, line in enumerate(handle):
            record = json.loads(line)
            require(record["index"] == expected_index,
                    "core column index gap")
            column = (tuple(map(int, record["word"])),
                      bytes(record["multiplier_cell_ids"]))
            require(canonical_column(column) == column,
                    f"noncanonical core column {expected_index}")
            require(column not in seen, f"duplicate core column {expected_index}")
            seen.add(column)
            key = repr(column)
            require(prior_key is None or prior_key < key,
                    "core columns not in Python repr order")
            prior_key = key
            minimum = BASE.column_minimum_degree(column, EXPORT.ANCHORS)
            require(minimum < 7, f"core column {expected_index} outside cutoff")
            minimum_degree_histogram[minimum] += 1
            expected_entries = Counter()
            for output in BASE.column_rows(column):
                if BASE.row_degree(output, EXPORT.ANCHORS) >= 7:
                    continue
                representative = canonical_row(output)
                if representative in row_index:
                    expected_entries[row_index[representative]] += 1
            observed_entries = Counter(dict(record["entries"]))
            require(observed_entries == expected_entries,
                    f"literal entries differ at core column {expected_index}")
            require(len(expected_entries) >= 2,
                    f"core retained zero/singleton column {expected_index}")
            support_histogram[sum(expected_entries.values())] += 1
        require(len(seen) == 1519, "core column line count changed")

    census = json.loads(census_path.read_text())
    require(census["seed_rows"] == len(invariant_target) == 36,
            "Rust seed orbit count changed")
    require(census["stabilizer_order"] == 2304,
            "Rust stabilizer order changed")
    require(census["closure_rows"]
            == census["seed_rows"] + sum(left for left, _right
                                          in census["closure_layers"]),
            "closure row layers do not add up")
    require(census["closure_columns"]
            == sum(right for _left, right in census["closure_layers"]),
            "closure column layers do not add up")
    require(census["closure_rows"] - census["saturated_pivot_rows"] == 363,
            "peel row arithmetic changed")
    require(census["closure_columns"]
            - int(census["projected_histogram"]["0"]) == 1519,
            "peel column arithmetic changed")
    observed_first_layer = first_layer(invariant_target)
    require(observed_first_layer == tuple(census["closure_layers"][0]),
            "independent first layer differs from Rust")

    result = {
        "status": "UNAUDITED independent exact seed/first-layer/core-interface audit",
        "chart": 0,
        "cutoff": 7,
        "stabilizer_order": 2304,
        "raw_seed_sha256": sha256(raw_seed_path.read_bytes()).hexdigest(),
        "core_interface_sha256": sha256(interface_path.read_bytes()).hexdigest(),
        "raw_target_rows": len(raw_target),
        "raw_target_mass": sum(raw_target.values()),
        "target_row_orbits": len(invariant_target),
        "first_layer": list(observed_first_layer),
        "closure_rows": census["closure_rows"],
        "closure_columns": census["closure_columns"],
        "pivot_rows": census["saturated_pivot_rows"],
        "core_rows": len(rows),
        "core_columns": len(seen),
        "core_minimum_degree_histogram": dict(sorted(minimum_degree_histogram.items())),
        "core_support_mass_histogram": dict(sorted(support_histogram.items())),
        "literal_core_columns_replayed": True,
        "exact_certificate_replayed": False,
    }
    encoded = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw-seed", type=Path, default=DEFAULT_RAW_SEED)
    parser.add_argument("--interface", type=Path, default=DEFAULT_INTERFACE)
    parser.add_argument("--census", type=Path, default=DEFAULT_CENSUS)
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()
    result = audit(args.raw_seed, args.interface, args.census)
    if args.write_results:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("orbit0 cutoff7 Rust interface audit: PASS")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
