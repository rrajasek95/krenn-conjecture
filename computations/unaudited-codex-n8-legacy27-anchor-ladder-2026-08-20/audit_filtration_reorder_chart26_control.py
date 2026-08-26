#!/usr/bin/env python3
"""Reorder the frozen chart26 cutoff-seven core as a permutation control."""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
RUST = HERE.parent / "unaudited-codex-anchor-k-rust-2026-08-20"
SOURCE = RUST / "results_chart26_cutoff7_direct.jsonl"
SEED = RUST / "chart26_cutoff7_target_seed.txt"
REFERENCE = RUST / "results_chart26_cutoff7_solution_p1009.json"
OUT = HERE / "chart26_cutoff7_filtration_ordered_control.jsonl"
RESULT = HERE / "results_chart26_filtration_order_control.json"


def require(condition: bool, detail: str) -> None:
    if not condition:
        raise RuntimeError(detail)


def read_anchors() -> frozenset[int]:
    for line in SEED.read_text().splitlines():
        if line.startswith("ANCHORS "):
            return frozenset(bytes.fromhex(line.split()[1]))
    raise RuntimeError("chart26 seed lacks anchors")


def main() -> None:
    anchor_set = read_anchors()
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
        columns = []
        for expected, raw in enumerate(handle):
            source_hasher.update(raw.encode("ascii"))
            record = json.loads(raw)
            require(record["index"] == expected,
                    "frozen chart26 source column order changed")
            entries = sorted((old_to_new[index], value)
                             for index, value in record["entries"])
            minimum_degree = min(old_degrees[index]
                                 for index, _value in record["entries"])
            columns.append((minimum_degree, len(entries),
                            sum(value for _index, value in entries),
                            expected, entries, record))

    columns.sort(key=lambda item: item[:4])
    target = sorted((old_to_new[index], numerator, denominator)
                    for index, numerator, denominator in header["target"])
    output_hasher = sha256()
    with OUT.open("w") as handle:
        new_header = {
            **header,
            "format": "krenn-anchor-k-chart26-filtration-control-v1",
            "rows_hex": [old_rows[old].hex() for old in new_to_old],
            "target": target,
            "source_interface_sha256": source_hasher.hexdigest(),
            "row_order": "K-degree, then row bytes",
            "column_order": (
                "minimum remaining K-degree, distinct support, mass, old index"
            ),
        }
        raw = json.dumps(new_header, sort_keys=True,
                         separators=(",", ":")) + "\n"
        handle.write(raw)
        output_hasher.update(raw.encode("ascii"))
        for new_index, (degree, _support, _mass, old_index,
                        entries, record) in enumerate(columns):
            output = {
                **record,
                "index": new_index,
                "entries": entries,
                "source_original_index": old_index,
                "minimum_remaining_K_degree": degree,
            }
            raw = json.dumps(output, sort_keys=True,
                             separators=(",", ":")) + "\n"
            handle.write(raw)
            output_hasher.update(raw.encode("ascii"))

    reference = json.loads(REFERENCE.read_text())
    core = {
        "status": "UNAUDITED permutation control awaiting reordered solve",
        "source_interface_sha256": source_hasher.hexdigest(),
        "ordered_interface_sha256": output_hasher.hexdigest(),
        "rows_columns": [header["row_count"], header["column_count"]],
        "row_K_degree_histogram": dict(sorted(Counter(old_degrees).items())),
        "column_minimum_remaining_K_degree_histogram": dict(sorted(
            Counter(item[0] for item in columns).items())),
        "row_bijection_verified": len(set(new_to_old)) == len(old_rows),
        "column_bijection_verified": (
            len({item[3] for item in columns}) == header["column_count"]
        ),
        "target_reindexed_exactly": True,
        "reference_prime": reference["prime"],
        "reference_rank": reference["rank"],
        "reference_target_in_image": reference["target_in_image"],
    }
    encoded = json.dumps(core, sort_keys=True, separators=(",", ":"))
    core["result_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    RESULT.write_text(json.dumps(core, indent=2, sort_keys=True) + "\n")
    print(json.dumps(core, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
