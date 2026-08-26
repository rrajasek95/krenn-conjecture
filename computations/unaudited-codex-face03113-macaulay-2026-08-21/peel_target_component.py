#!/usr/bin/env python3
"""Peel zero-target row leaves and export the target component.

If a row occurs in one active column and its target coefficient is zero, that
column's coefficient is forced to zero in every representation.  Cascading
this rule and discarding target-free connected components preserves target
membership exactly.  This script refuses to peel a target-bearing row.
"""

from __future__ import annotations

from collections import deque
import argparse
from hashlib import sha256
import json
from pathlib import Path


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    with args.input.open() as source:
        header = json.loads(next(source))
        require(header["type"] == "header", "missing header")
        row_count = header["row_count"]
        column_count = header["column_count"]
        target = {triple[0]: (triple[1], triple[2])
                  for triple in header["target"]}
        columns = []
        row_columns = [[] for _ in range(row_count)]
        for expected, line in enumerate(source):
            if not line.strip():
                continue
            record = json.loads(line)
            require(record["type"] == "column", "non-column record")
            require(record["index"] == expected, "column order changed")
            entries = record["entries"]
            require(entries, "zero column")
            columns.append(record)
            for row, coefficient in entries:
                require(coefficient, "stored zero coefficient")
                row_columns[row].append(expected)
        require(len(columns) == column_count, "column count changed")

    degrees = [len(incident) for incident in row_columns]
    active = [True] * column_count
    queue = deque(row for row, degree in enumerate(degrees) if degree == 1)
    initial_leaves = len(queue)
    removed = []
    while queue:
        row = queue.popleft()
        if degrees[row] != 1:
            continue
        require(row not in target,
                f"refusing to peel target-bearing row {row}")
        column = next((candidate for candidate in row_columns[row]
                       if active[candidate]), None)
        require(column is not None, "leaf has no active column")
        active[column] = False
        removed.append((row, column))
        for touched, _ in columns[column]["entries"]:
            require(degrees[touched] > 0, "degree underflow")
            degrees[touched] -= 1
            if degrees[touched] == 1:
                queue.append(touched)

    # The target rows must survive.  Traverse their full active bipartite
    # component; all other components can be assigned coefficient zero.
    require(all(degrees[row] > 0 for row in target),
            "target was isolated by zero-target peeling")
    component_rows = set(target)
    component_columns = set()
    row_queue = deque(sorted(target))
    while row_queue:
        row = row_queue.popleft()
        for column in row_columns[row]:
            if not active[column] or column in component_columns:
                continue
            component_columns.add(column)
            for touched, _ in columns[column]["entries"]:
                require(degrees[touched] > 0,
                        "active column touches isolated row")
                if touched not in component_rows:
                    component_rows.add(touched)
                    row_queue.append(touched)

    old_rows = sorted(component_rows)
    old_columns = sorted(component_columns)
    row_map = {old: new for new, old in enumerate(old_rows)}
    output_header = dict(header)
    output_header.update({
        "format": "krenn-homogeneous-macaulay-peeled-target-component-v1",
        "row_count": len(old_rows),
        "column_count": len(old_columns),
        "target": [[row_map[row], numerator, denominator]
                   for row, (numerator, denominator) in sorted(target.items())],
        "parent_input": str(args.input),
        "parent_input_sha256": sha256(args.input.read_bytes()).hexdigest(),
        "initial_row_leaves": initial_leaves,
        "zero_target_leaf_columns_removed": len(removed),
        "target_component_original_rows": old_rows,
        "target_component_original_columns": old_columns,
        "peel_ledger_sha256": sha256(json.dumps(
            removed, separators=(",", ":")).encode()).hexdigest(),
        "scope_guard_peel": (
            "Every removed column had a private active row with zero target "
            "coefficient. Target-free active components are assigned zero."
        ),
    })
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w") as output:
        output.write(json.dumps(output_header, sort_keys=True) + "\n")
        for new_index, old_index in enumerate(old_columns):
            record = dict(columns[old_index])
            record["index"] = new_index
            record["original_index"] = old_index
            record["entries"] = [[row_map[row], coefficient]
                                 for row, coefficient in record["entries"]]
            output.write(json.dumps(record, sort_keys=True) + "\n")
    print(json.dumps({
        "input_rows": row_count, "input_columns": column_count,
        "initial_row_leaves": initial_leaves,
        "removed_columns": len(removed),
        "target_rows": len(old_rows), "target_columns": len(old_columns),
        "output": str(args.output),
        "sha256": sha256(args.output.read_bytes()).hexdigest(),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
