#!/usr/bin/env python3
"""Strictly convert a column-JSONL Macaulay system to SpaSM SMS files.

The source represents an equations-by-unknowns matrix by sparse columns.  SpaSM
solves X*A=B, so we write the transpose directly: one SpaSM row per source
column and one SpaSM column per original equation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import tempfile
from typing import BinaryIO, Iterable


FORMAT = "krenn-macaulay-spasm-export-v1"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def inverse_mod(value: int, prime: int) -> int:
    value %= prime
    if value == 0:
        raise ValueError("zero denominator modulo prime")
    return pow(value, -1, prime)


def atomic_text_path(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    return tempfile.NamedTemporaryFile(
        mode="w", encoding="ascii", newline="\n", dir=path.parent,
        prefix=path.name + ".", suffix=".tmp", delete=False,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output_prefix", type=Path)
    parser.add_argument("prime", type=int)
    args = parser.parse_args()
    if args.prime <= 2:
        raise SystemExit("prime must exceed 2")

    matrix_path = args.output_prefix.with_suffix(".matrix.sms")
    rhs_path = args.output_prefix.with_suffix(".rhs.sms")
    manifest_path = args.output_prefix.with_suffix(".manifest.json")
    source_sha = sha256_file(args.input)

    matrix_tmp = atomic_text_path(matrix_path)
    rhs_tmp = None
    try:
        with args.input.open("r", encoding="utf-8", newline="") as source:
            raw_header = source.readline()
            if not raw_header:
                raise ValueError("empty JSONL input")
            header = json.loads(raw_header)
            row_count = int(header["row_count"])
            column_count = int(header["column_count"])
            if row_count <= 0 or column_count <= 0:
                raise ValueError("matrix dimensions must be positive")
            target_raw = header.get("target")
            if not isinstance(target_raw, list):
                raise ValueError("header target must be a list")

            matrix_tmp.write(f"{column_count} {row_count} M\n")
            matrix_nnz = 0
            for expected_index in range(column_count):
                raw = source.readline()
                if not raw:
                    raise ValueError(f"premature EOF at column {expected_index}")
                record = json.loads(raw)
                if record.get("type") != "column":
                    raise ValueError(f"record {expected_index} is not a column")
                if record.get("index") != expected_index:
                    raise ValueError(
                        f"column index mismatch: expected {expected_index}, got {record.get('index')}"
                    )
                entries = record.get("entries")
                if not isinstance(entries, list) or not entries:
                    raise ValueError(f"column {expected_index} has no entries")
                previous_row = -1
                for entry in entries:
                    if not isinstance(entry, list) or len(entry) != 2:
                        raise ValueError(f"bad entry in column {expected_index}")
                    row, coefficient = map(int, entry)
                    if not 0 <= row < row_count:
                        raise ValueError(f"row {row} out of range in column {expected_index}")
                    if row <= previous_row:
                        raise ValueError(f"rows not strictly increasing in column {expected_index}")
                    if coefficient == 0:
                        raise ValueError(f"zero stored coefficient in column {expected_index}")
                    previous_row = row
                    matrix_tmp.write(f"{expected_index + 1} {row + 1} {coefficient}\n")
                    matrix_nnz += 1
            if source.readline():
                raise ValueError("trailing JSONL records after declared columns")
            matrix_tmp.write("0 0 0\n")
            matrix_tmp.flush()
            os.fsync(matrix_tmp.fileno())
            matrix_tmp.close()

        target: dict[int, int] = {}
        for triple in target_raw:
            if not isinstance(triple, list) or len(triple) != 3:
                raise ValueError("target entries must be row/numerator/denominator triples")
            row, numerator, denominator = map(int, triple)
            if not 0 <= row < row_count:
                raise ValueError(f"target row {row} out of range")
            value = (numerator % args.prime) * inverse_mod(denominator, args.prime) % args.prime
            target[row] = (target.get(row, 0) + value) % args.prime
        target = {row: value for row, value in target.items() if value}

        rhs_tmp = atomic_text_path(rhs_path)
        rhs_tmp.write(f"1 {row_count} M\n")
        for row, value in sorted(target.items()):
            balanced = value if value <= args.prime // 2 else value - args.prime
            rhs_tmp.write(f"1 {row + 1} {balanced}\n")
        rhs_tmp.write("0 0 0\n")
        rhs_tmp.flush()
        os.fsync(rhs_tmp.fileno())
        rhs_tmp.close()

        os.replace(matrix_tmp.name, matrix_path)
        os.replace(rhs_tmp.name, rhs_path)
        manifest = {
            "format": FORMAT,
            "source": str(args.input.resolve()),
            "source_sha256": source_sha,
            "source_format": header.get("format"),
            "prime": args.prime,
            "original_shape": [row_count, column_count],
            "spasm_shape": [column_count, row_count],
            "orientation": "spasm solves X*A=B; A is the transpose of the original Macaulay matrix",
            "matrix_nnz": matrix_nnz,
            "target_nnz": len(target),
            "matrix": str(matrix_path.resolve()),
            "matrix_sha256": sha256_file(matrix_path),
            "rhs": str(rhs_path.resolve()),
            "rhs_sha256": sha256_file(rhs_path),
        }
        manifest_tmp = atomic_text_path(manifest_path)
        try:
            json.dump(manifest, manifest_tmp, indent=2, sort_keys=True)
            manifest_tmp.write("\n")
            manifest_tmp.flush()
            os.fsync(manifest_tmp.fileno())
            manifest_tmp.close()
            os.replace(manifest_tmp.name, manifest_path)
        finally:
            if not manifest_tmp.closed:
                manifest_tmp.close()
            if os.path.exists(manifest_tmp.name):
                os.unlink(manifest_tmp.name)
        print(json.dumps(manifest, sort_keys=True))
    finally:
        if not matrix_tmp.closed:
            matrix_tmp.close()
        if os.path.exists(matrix_tmp.name):
            os.unlink(matrix_tmp.name)
        if rhs_tmp is not None:
            if not rhs_tmp.closed:
                rhs_tmp.close()
            if os.path.exists(rhs_tmp.name):
                os.unlink(rhs_tmp.name)


if __name__ == "__main__":
    main()
