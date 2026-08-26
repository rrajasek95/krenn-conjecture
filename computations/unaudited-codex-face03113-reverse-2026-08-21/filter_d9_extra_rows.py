#!/usr/bin/env python3
"""Filter the full face03113 d9 ledger to selected extra raw rows."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path


BASE = {7, 8, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def raw_index(label):
    if label.startswith("SAT_"):
        return None
    require(label.startswith("raw_"), f"unexpected label {label}")
    return int(label.split("_", 2)[1])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--extra", type=int, action="append", default=[])
    args = parser.parse_args()
    allowed = BASE | set(args.extra)
    with args.input.open() as source:
        header = json.loads(next(source))
        require(header["full_rows"] and header["degree"] == 9,
                "expected full-row degree-9 input")
        retained = []
        for line in source:
            if not line.strip():
                continue
            record = json.loads(line)
            index = raw_index(record["source_label"])
            if index is None or index in allowed:
                retained.append(record)
    generators = [row for row in header["generators"]
                  if raw_index(row["label"]) is None
                  or raw_index(row["label"]) in allowed]
    output_header = dict(header)
    output_header.update({
        "format": "krenn-homogeneous-macaulay-filtered-columns-v1",
        "column_count": len(retained),
        "kept_raw_rows": sorted(allowed),
        "full_rows": False,
        "generators": generators,
        "parent_input": str(args.input),
        "parent_input_sha256": sha256(args.input.read_bytes()).hexdigest(),
        "scope_guard_filter": (
            "Only columns from the displayed raw rows and the unchanged "
            "saturator are retained; row indices and target are unchanged."),
    })
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w") as output:
        output.write(json.dumps(output_header, sort_keys=True) + "\n")
        for new_index, record in enumerate(retained):
            record["original_index"] = record["index"]
            record["index"] = new_index
            output.write(json.dumps(record, sort_keys=True) + "\n")
    print(json.dumps({"kept_raw_rows": sorted(allowed),
                      "columns": len(retained),
                      "output": str(args.output),
                      "sha256": sha256(args.output.read_bytes()).hexdigest()},
                     sort_keys=True))


if __name__ == "__main__":
    main()
