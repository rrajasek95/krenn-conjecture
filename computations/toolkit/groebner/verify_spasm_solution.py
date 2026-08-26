#!/usr/bin/env python3
"""Independently replay a SpaSM solution against the source Macaulay JSONL."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import tempfile


FORMAT = "krenn-macaulay-spasm-solution-audit-v1"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_solution(path: Path, expected_columns: int, prime: int) -> list[int]:
    values = [0] * expected_columns
    with path.open("r", encoding="ascii") as handle:
        header = handle.readline().split()
        if header != ["1", str(expected_columns), "M"]:
            raise ValueError(f"unexpected solution header: {header}")
        previous = 0
        terminated = False
        for line_number, line in enumerate(handle, 2):
            fields = line.split()
            if len(fields) != 3:
                raise ValueError(f"bad SMS line {line_number}")
            row, column, coefficient = map(int, fields)
            if (row, column, coefficient) == (0, 0, 0):
                terminated = True
                if handle.readline():
                    raise ValueError("trailing data after SMS terminator")
                break
            if row != 1 or not 1 <= column <= expected_columns:
                raise ValueError(f"solution coordinate out of range on line {line_number}")
            if column <= previous:
                raise ValueError("solution columns are not strictly increasing")
            previous = column
            values[column - 1] = coefficient % prime
        if not terminated:
            raise ValueError("solution SMS lacks terminator")
    return values


def inverse_mod(value: int, prime: int) -> int:
    value %= prime
    if value == 0:
        raise ValueError("zero denominator modulo prime")
    return pow(value, -1, prime)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("solution", type=Path)
    parser.add_argument("report", type=Path)
    parser.add_argument("prime", type=int)
    args = parser.parse_args()

    with args.source.open("r", encoding="utf-8") as handle:
        header = json.loads(handle.readline())
        row_count = int(header["row_count"])
        column_count = int(header["column_count"])
        solution = parse_solution(args.solution, column_count, args.prime)
        image = [0] * row_count
        source_nnz = 0
        for expected_index in range(column_count):
            record = json.loads(handle.readline())
            if record.get("index") != expected_index or record.get("type") != "column":
                raise ValueError(f"bad column record {expected_index}")
            scalar = solution[expected_index]
            for row, coefficient in record["entries"]:
                source_nnz += 1
                if scalar:
                    image[row] = (image[row] + scalar * coefficient) % args.prime
        if handle.readline():
            raise ValueError("trailing source records")

    target = [0] * row_count
    for row, numerator, denominator in header["target"]:
        target[row] = (
            target[row]
            + numerator * inverse_mod(denominator, args.prime)
        ) % args.prime
    mismatches = [index for index, (left, right) in enumerate(zip(image, target)) if left != right]
    selected = [index for index, value in enumerate(solution) if value]
    report = {
        "format": FORMAT,
        "source": str(args.source.resolve()),
        "source_sha256": sha256_file(args.source),
        "solution": str(args.solution.resolve()),
        "solution_sha256": sha256_file(args.solution),
        "prime": args.prime,
        "row_count": row_count,
        "column_count": column_count,
        "source_nnz": source_nnz,
        "solution_nnz": len(selected),
        "selected_columns": selected,
        "mismatch_count": len(mismatches),
        "first_mismatches": mismatches[:20],
        "verified": not mismatches,
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", dir=args.report.parent,
        prefix=args.report.name + ".", suffix=".tmp", delete=False,
    ) as temp:
        json.dump(report, temp, indent=2, sort_keys=True)
        temp.write("\n")
        temp.flush()
        os.fsync(temp.fileno())
        temp_name = temp.name
    os.replace(temp_name, args.report)
    print(json.dumps({key: value for key, value in report.items() if key != "selected_columns"}, sort_keys=True))
    if mismatches:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
