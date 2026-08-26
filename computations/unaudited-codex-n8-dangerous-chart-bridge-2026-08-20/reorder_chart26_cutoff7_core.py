#!/usr/bin/env python3
"""Emit cheap deterministic column reorders for cutoff-7 sparsity probes.

The emitted files are discovery-only modular interfaces.  Their column records
retain ``original_index`` so that any useful support can be pulled back before
an exact-Q reconstruction and literal replay.
"""

from __future__ import annotations

from collections import defaultdict, deque
import argparse
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
DEFAULT_INPUT = (HERE.parent / "unaudited-codex-anchor-k-rust-2026-08-20"
                 / "results_chart26_cutoff7_direct.jsonl")


def read_interface(path):
    with path.open() as handle:
        header = json.loads(next(handle))
        columns = [json.loads(line) for line in handle if line.strip()]
    return header, columns


def bfs_layers(header, columns):
    row_columns = defaultdict(list)
    for column in columns:
        for row, _value in column["entries"]:
            row_columns[row].append(column["index"])
    seen_rows = {row for row, _num, _den in header["target"]}
    seen_columns = set()
    queue = deque(("row", row, 0) for row in sorted(seen_rows))
    layers = {}
    while queue:
        kind, index, distance = queue.popleft()
        if kind == "row":
            for column in row_columns[index]:
                if column not in seen_columns:
                    seen_columns.add(column)
                    layers[column] = distance
                    queue.append(("column", column, distance))
        else:
            for row, _value in columns[index]["entries"]:
                if row not in seen_rows:
                    seen_rows.add(row)
                    queue.append(("row", row, distance + 1))
    if len(seen_columns) != len(columns):
        raise RuntimeError("core is not connected to the target")
    return layers


def ordering(mode, header, columns):
    target = {row for row, _num, _den in header["target"]}
    if mode == "mass-ascending":
        return sorted(columns, key=lambda col: (
            sum(value for _row, value in col["entries"]), col["index"]))
    if mode == "target-overlap":
        return sorted(columns, key=lambda col: (
            -sum(value for row, value in col["entries"] if row in target),
            sum(value for _row, value in col["entries"]), col["index"]))
    if mode in {"bfs", "bfs-mass"}:
        layers = bfs_layers(header, columns)
        if mode == "bfs":
            return sorted(columns, key=lambda col: (layers[col["index"]],
                                                     col["index"]))
        return sorted(columns, key=lambda col: (
            layers[col["index"]],
            sum(value for _row, value in col["entries"]), col["index"]))
    raise ValueError(f"unknown mode {mode}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("mass-ascending", "target-overlap",
                                         "bfs", "bfs-mass"))
    parser.add_argument("output", type=Path)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    args = parser.parse_args()
    header, columns = read_interface(args.input)
    ordered = ordering(args.mode, header, columns)
    with args.output.open("w") as handle:
        header["format"] += f"-reordered-{args.mode}"
        handle.write(json.dumps(header, separators=(",", ":")) + "\n")
        for index, record in enumerate(ordered):
            record["original_index"] = record["index"]
            record["index"] = index
            handle.write(json.dumps(record, separators=(",", ":")) + "\n")


if __name__ == "__main__":
    main()
