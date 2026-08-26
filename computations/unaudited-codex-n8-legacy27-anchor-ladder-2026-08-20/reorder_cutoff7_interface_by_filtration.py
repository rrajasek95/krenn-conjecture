#!/usr/bin/env python3
"""Losslessly reorder the cutoff-seven core by K-degree to reduce fill-in."""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import argparse
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "legacy27_cutoff7_direct.jsonl"
SEED = HERE / "legacy27_cutoff7_target_seed.txt"
OUT = HERE / "legacy27_cutoff7_filtration_ordered.jsonl"
RESULT = HERE / "results_cutoff7_filtration_order.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def anchors():
    for line in SEED.read_text().splitlines():
        if line.startswith("ANCHORS "):
            return frozenset(bytes.fromhex(line.split()[1]))
    raise RuntimeError("seed lacks anchors")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()
    anchor_set = anchors()
    source_hasher = sha256()
    with SOURCE.open() as handle:
        raw_header = next(handle)
        source_hasher.update(raw_header.encode("ascii"))
        header = json.loads(raw_header)
        old_rows = tuple(bytes.fromhex(value) for value in header["rows_hex"])
        old_degrees = tuple(sum(cell not in anchor_set for cell in row)
                            for row in old_rows)
        new_to_old = tuple(sorted(range(len(old_rows)),
                                  key=lambda index: (old_degrees[index],
                                                     old_rows[index])))
        old_to_new = {old: new for new, old in enumerate(new_to_old)}
        new_rows = tuple(old_rows[old] for old in new_to_old)
        columns = []
        for expected, raw in enumerate(handle):
            source_hasher.update(raw.encode("ascii"))
            record = json.loads(raw)
            require(record["index"] == expected, "source column order changed")
            entries = sorted((old_to_new[index], value)
                             for index, value in record["entries"])
            minimum_degree = min(old_degrees[index]
                                 for index, _value in record["entries"])
            columns.append((
                minimum_degree, len(entries), sum(value for _index, value in entries),
                expected, entries, record,
            ))
    columns.sort(key=lambda item: item[:4])
    target = sorted((old_to_new[index], numerator, denominator)
                    for index, numerator, denominator in header["target"])
    hasher = sha256()
    with OUT.open("w") as handle:
        new_header = {
            **header,
            "format": "krenn-anchor-k-truncated-cutoff7-filtration-ordered-v1",
            "rows_hex": [row.hex() for row in new_rows],
            "target": target,
            "source_interface_sha256": source_hasher.hexdigest(),
            "row_order": "K-degree, then row bytes",
            "column_order": (
                "minimum remaining K-degree, distinct support, mass, old index"
            ),
        }
        line = json.dumps(new_header, sort_keys=True, separators=(",", ":")) + "\n"
        handle.write(line)
        hasher.update(line.encode("ascii"))
        old_indices = []
        for new_index, (degree, _support, _mass, old_index,
                        entries, record) in enumerate(columns):
            old_indices.append(old_index)
            output = {
                **record,
                "index": new_index,
                "entries": entries,
                "source_original_index": old_index,
                "minimum_remaining_K_degree": degree,
            }
            line = json.dumps(output, sort_keys=True,
                              separators=(",", ":")) + "\n"
            handle.write(line)
            hasher.update(line.encode("ascii"))
    require(len(set(old_indices)) == header["column_count"],
            "column reorder lost provenance")
    row_histogram = Counter(old_degrees)
    column_histogram = Counter(item[0] for item in columns)
    core = {
        "status": "UNAUDITED lossless interface permutation; no rank claim",
        "source_interface_sha256": source_hasher.hexdigest(),
        "ordered_interface_sha256": hasher.hexdigest(),
        "rows_columns": [header["row_count"], header["column_count"]],
        "row_K_degree_histogram": dict(sorted(row_histogram.items())),
        "column_minimum_remaining_K_degree_histogram":
            dict(sorted(column_histogram.items())),
        "row_bijection_verified": len(set(new_to_old)) == len(old_rows),
        "column_bijection_verified": len(set(old_indices)) == len(columns),
        "target_reindexed_exactly": True,
        "provenance_old_column_index_retained": True,
    }
    encoded = json.dumps(core, sort_keys=True, separators=(",", ":"))
    core["result_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    if args.write_results:
        RESULT.write_text(json.dumps(core, indent=2, sort_keys=True) + "\n")
    print("legacy27 cutoff7 filtration reorder: PASS")
    print("ordered sha256:", core["ordered_interface_sha256"])
    print("result sha256:", core["result_sha256"])


if __name__ == "__main__":
    main()
