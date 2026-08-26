#!/usr/bin/env python3
"""Reindex lower-kernel d6 tails onto a Rust singleton-peeled core."""

from __future__ import annotations

from hashlib import sha256
import argparse
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("basis", type=Path,
                        help="Rust orbit_closure coupled JSONL")
    parser.add_argument("--prime", type=int, default=1009)
    args = parser.parse_args()
    stage = HERE / f"degree6_lower_kernel_transfers_p{args.prime}.jsonl"
    out = HERE / f"degree6_lower_kernel_transfers_core_p{args.prime}.jsonl"

    with args.basis.open() as handle:
        basis_header = json.loads(next(handle))
    if basis_header["type"] != "header":
        raise RuntimeError("Rust basis lacks header")
    rows = tuple(bytes.fromhex(value) for value in basis_header["rows_hex"])
    row_index = {row: index for index, row in enumerate(rows)}
    if len(row_index) != basis_header["row_count"]:
        raise RuntimeError("Rust core row labels are not unique")

    with stage.open() as source, out.open("w") as target:
        stage_header = json.loads(next(source))
        if (stage_header["format"]
                != "krenn-chart26-degree6-lower-kernel-v1"
                or stage_header["prime"] != args.prime
                or stage_header["kernel_dimension"] != 3274):
            raise RuntimeError("lower-kernel stage header changed")
        header = {
            "type": "header",
            "format": "krenn-chart26-degree6-lower-kernel-core-v1",
            "prime": args.prime,
            "row_count": len(rows),
            "column_count": 3274,
            "target": basis_header["target"],
            "source_basis_path": str(args.basis),
            "source_basis_format": basis_header["format"],
            "source_stage_sha256": sha256(stage.read_bytes()).hexdigest(),
            "corrected_lower_definition_sha256": stage_header[
                "corrected_lower_definition_sha256"
            ],
        }
        line = json.dumps(header, sort_keys=True, separators=(",", ":")) + "\n"
        target.write(line)
        hasher = sha256(line.encode("ascii"))
        kept_nnz = 0
        dropped_pivot_nnz = 0
        nonzero_columns = 0
        for expected, raw in enumerate(source):
            record = json.loads(raw)
            if record["index"] != expected:
                raise RuntimeError("transfer order changed")
            entries = []
            for row_hex, value in record["tail6"]:
                index = row_index.get(bytes.fromhex(row_hex))
                if index is None:
                    dropped_pivot_nnz += 1
                else:
                    entries.append([index, value])
            entries.sort()
            if entries:
                nonzero_columns += 1
            kept_nnz += len(entries)
            output = {
                "type": "column",
                "index": expected,
                "entries": entries,
                "source_transfer_index": expected,
                "corrected_lower_relation": record[
                    "corrected_lower_relation"
                ],
            }
            line = json.dumps(output, sort_keys=True,
                              separators=(",", ":")) + "\n"
            target.write(line)
            hasher.update(line.encode("ascii"))
        if expected + 1 != 3274:
            raise RuntimeError("transfer count changed")

    print("prime:", args.prime)
    print("core rows:", len(rows))
    print("transfer columns/nonzero:", 3274, nonzero_columns)
    print("kept/dropped-pivot nnz:", kept_nnz, dropped_pivot_nnz)
    print("bytes:", out.stat().st_size)
    print("sha256:", hasher.hexdigest())
    print("path:", out.relative_to(HERE.parent.parent))


if __name__ == "__main__":
    main()
