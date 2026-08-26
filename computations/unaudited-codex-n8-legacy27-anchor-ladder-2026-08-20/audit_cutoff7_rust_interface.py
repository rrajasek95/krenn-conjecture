#!/usr/bin/env python3
"""Python source-faithful audit of the legacy27 whole-cutoff Rust interface."""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import argparse
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROBE_PATH = HERE / "probe_legacy27_k6_orbits.py"
SPEC = importlib.util.spec_from_file_location("legacy27_cutoff7_audit", PROBE_PATH)
PROBE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PROBE)
BASE = PROBE.BASE
INTERFACE = HERE / "legacy27_cutoff7_direct.jsonl"
RUST_RESULT = HERE / "results_cutoff7_direct_rust.json"
OUT = HERE / "results_cutoff7_interface_audit.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def target():
    answer = Counter()
    for degree in range(7):
        actual = (Counter({bytes(sorted(PROBE.ANCHORS)): 1})
                  if degree == 0 else PROBE.target_exact(degree))
        for row, coefficient in actual.items():
            answer[PROBE.canonical_row(row)] += coefficient
    require((len(answer), sum(answer.values())) == (2070, 12169),
            "whole-cutoff target changed")
    return answer


def first_layer(seed):
    columns = set()
    rows = set(seed)
    for row in seed:
        for raw in BASE.incident_columns(row):
            column = PROBE.canonical_column(raw)
            if PROBE.column_minimum_degree(column) >= 7:
                continue
            columns.add(column)
            for output in BASE.column_rows(column):
                if BASE.row_degree(output, PROBE.ANCHORS) < 7:
                    rows.add(PROBE.canonical_row(output))
    return len(rows) - len(seed), len(columns)


def audit():
    seed = target()
    layer1 = first_layer(seed)
    require(layer1 == (33600, 7359),
            "Python whole-cutoff first layer disagrees with Rust")
    rust = json.loads(RUST_RESULT.read_text())
    require(rust["closure_layers"][0] == [33600, 7359],
            "frozen Rust first layer changed")
    require((rust["coupled_rows"], rust["coupled_columns"])
            == (44741, 77265), "Rust coupled dimensions changed")

    hasher = sha256()
    projected_histogram = Counter()
    with INTERFACE.open() as handle:
        first = next(handle)
        hasher.update(first.encode("ascii"))
        header = json.loads(first)
        require(header["format"] == "krenn-anchor-k-truncated-cutoff7-coupled-v1",
                "Rust cutoff interface format changed")
        require((header["row_count"], header["column_count"])
                == (44741, 77265), "Rust interface dimensions changed")
        rows = tuple(bytes.fromhex(value) for value in header["rows_hex"])
        require(len(set(rows)) == len(rows), "Rust coupled rows are not unique")
        require(all(PROBE.canonical_row(row) == row for row in rows),
                "Rust coupled row is not canonical")
        require(all(BASE.row_degree(row, PROBE.ANCHORS) < 7 for row in rows),
                "Rust coupled row exceeds cutoff")
        row_index = {row: index for index, row in enumerate(rows)}
        expected_target = Counter({row_index[row]: value
                                   for row, value in seed.items()
                                   if row in row_index})
        actual_target = Counter()
        for index, numerator, denominator in header["target"]:
            require(denominator == 1, "unexpected target denominator")
            actual_target[index] += numerator
        require(actual_target == expected_target,
                "Rust coupled target is not the literal seed restriction")

        count = 0
        for raw in handle:
            hasher.update(raw.encode("ascii"))
            record = json.loads(raw)
            require(record["index"] == count and record["type"] == "column",
                    "Rust column order/type changed")
            column = (
                tuple(map(int, record["word"])),
                bytes(record["multiplier_cell_ids"]),
            )
            require(PROBE.canonical_column(column) == column,
                    "Rust source column is not canonical")
            expected = Counter()
            for output in BASE.column_rows(column):
                if BASE.row_degree(output, PROBE.ANCHORS) >= 7:
                    continue
                representative = PROBE.canonical_row(output)
                if representative in row_index:
                    expected[row_index[representative]] += 1
            actual = Counter()
            for index, value in record["entries"]:
                actual[index] += value
            require(actual == expected,
                    f"Rust column {count} lost a labelled multiplicity")
            require(len(actual) >= 2,
                    "saturated coupled interface retained a singleton")
            projected_histogram[sum(actual.values())] += 1
            count += 1
            if count % 10000 == 0:
                print("audited Rust columns", count, flush=True)
        require(count == header["column_count"],
                "Rust interface column count changed")
    expected_histogram = Counter({int(key): value for key, value in
                                  rust["projected_histogram"].items()
                                  if int(key) >= 2})
    require(projected_histogram == expected_histogram,
            "Rust projected multiplicity histogram changed")
    core = {
        "status": "UNAUDITED exact Python replay of Rust interface",
        "zero_based_chart": 30,
        "legacy_one_based_chart": 27,
        "cutoff": 7,
        "target_rows_mass": [len(seed), sum(seed.values())],
        "python_first_layer": list(layer1),
        "rust_first_layer": rust["closure_layers"][0],
        "coupled_rows_columns": [len(rows), count],
        "interface_sha256": hasher.hexdigest(),
        "all_source_columns_replayed_from_word_multiplier": True,
        "literal_multiplicities_preserved": True,
        "projected_histogram_replayed": True,
        "rank_or_membership_claimed": False,
    }
    encoded = json.dumps(core, sort_keys=True, separators=(",", ":"))
    core["result_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    return core


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()
    result = audit()
    if args.write_results:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("legacy27 cutoff7 Rust interface audit: PASS")
    print("interface sha256:", result["interface_sha256"])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
