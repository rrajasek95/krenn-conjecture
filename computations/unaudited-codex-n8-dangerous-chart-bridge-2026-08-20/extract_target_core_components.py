#!/usr/bin/env python3
"""Extract exactly the post-peel core components meeting target support."""

from __future__ import annotations

from hashlib import sha256
import argparse
import json
from pathlib import Path


class UnionFind:
    def __init__(self, size):
        self.parent = list(range(size))
        self.weight = [1] * size

    def find(self, value):
        while self.parent[value] != value:
            self.parent[value] = self.parent[self.parent[value]]
            value = self.parent[value]
        return value

    def union(self, left, right):
        left, right = self.find(left), self.find(right)
        if left == right:
            return
        if self.weight[left] < self.weight[right]:
            left, right = right, left
        self.parent[right] = left
        self.weight[left] += self.weight[right]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    with args.input.open() as handle:
        header = json.loads(next(handle))
        columns = [json.loads(line) for line in handle if line.strip()]
    row_count = header["row_count"]
    column_count = header["column_count"]
    if len(columns) != column_count:
        raise RuntimeError("column line count differs from header")
    uf = UnionFind(row_count + column_count)
    for index, column in enumerate(columns):
        if column["index"] != index:
            raise RuntimeError("input column order has a gap")
        vertex = row_count + index
        for row, _value in column["entries"]:
            uf.union(row, vertex)
    target_rows = {int(row) for row, _num, _den in header["target"]}
    target_roots = {uf.find(row) for row in target_rows}
    kept_rows = [row for row in range(row_count)
                 if uf.find(row) in target_roots]
    kept_columns = [index for index in range(column_count)
                    if uf.find(row_count + index) in target_roots]
    row_map = {old: new for new, old in enumerate(kept_rows)}
    new_header = dict(header)
    new_header["format"] += "-target-components-v1"
    new_header["row_count"] = len(kept_rows)
    new_header["column_count"] = len(kept_columns)
    new_header["rows_hex"] = [header["rows_hex"][row] for row in kept_rows]
    new_header["target"] = [
        [row_map[int(row)], numerator, denominator]
        for row, numerator, denominator in header["target"]
        if int(row) in row_map
    ]
    with args.output.open("w") as handle:
        handle.write(json.dumps(new_header, separators=(",", ":")) + "\n")
        for new_index, old_index in enumerate(kept_columns):
            column = dict(columns[old_index])
            column["original_index"] = old_index
            column["index"] = new_index
            column["entries"] = [
                [row_map[row], value] for row, value in column["entries"]
            ]
            handle.write(json.dumps(column, separators=(",", ":")) + "\n")
    print("input rows/columns:", row_count, column_count)
    print("all components:", len({uf.find(index)
                                  for index in range(row_count + column_count)}))
    print("target components:", len(target_roots))
    print("output rows/columns:", len(kept_rows), len(kept_columns))
    print("output sha256:", sha256(args.output.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
