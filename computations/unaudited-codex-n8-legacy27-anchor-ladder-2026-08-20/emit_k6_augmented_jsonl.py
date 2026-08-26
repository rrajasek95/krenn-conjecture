#!/usr/bin/env python3
"""Losslessly convert the frozen legacy27 augmented JSON to Rust JSONL."""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "k6_augmented_matrix.json"
OUT = HERE / "k6_augmented_matrix.jsonl"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def main():
    payload = json.loads(SOURCE.read_text())
    require(payload["matrix_sha256"] ==
            "78a62528fc5dce57f5c20f4000b3b35bfe0b2f6679ebd1285f7de97fb9d0fb92",
            "frozen augmented JSON changed")
    hasher = sha256()
    with OUT.open("w") as handle:
        header = {
            "type": "header",
            "format": "krenn-legacy27-anchor-k6-augmented-v1",
            "row_count": payload["total_rows"],
            "column_count": payload["lower_column_orbits"],
            "lower_row_orbits": payload["lower_row_orbits"],
            "quotient_dual_rows": payload["quotient_dual_rows"],
            "source_matrix_sha256": payload["matrix_sha256"],
            "target": [
                [index, Fraction(value).numerator, Fraction(value).denominator]
                for index, value in payload["target"]
            ],
        }
        line = json.dumps(header, sort_keys=True, separators=(",", ":")) + "\n"
        handle.write(line)
        hasher.update(line.encode("ascii"))
        for index, column in enumerate(payload["columns"]):
            entries = []
            for row, value in column["entries"]:
                coefficient = Fraction(value)
                require(coefficient.denominator == 1,
                        "Rust column interface requires integral entries")
                entries.append([row, coefficient.numerator])
            record = {
                "type": "column",
                "index": index,
                "entries": entries,
                "word": column["word"],
                "multiplier_cell_ids": list(bytes.fromhex(
                    column["multiplier_hex"]
                )),
                "column_orbit_size": column["column_orbit_size"],
            }
            line = json.dumps(record, sort_keys=True,
                              separators=(",", ":")) + "\n"
            handle.write(line)
            hasher.update(line.encode("ascii"))
    print(json.dumps({
        "path": str(OUT),
        "bytes": OUT.stat().st_size,
        "sha256": hasher.hexdigest(),
        "rows": payload["total_rows"],
        "columns": payload["lower_column_orbits"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
