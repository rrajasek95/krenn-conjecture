#!/usr/bin/env python3
"""Export a deterministic CSR pairing slice from the frozen D12 vector cache."""

from __future__ import annotations

import argparse
import array
import hashlib
import json
import os
import struct
import sys
from collections import Counter
from pathlib import Path

SOURCE_MAGIC = b"AFF12VEC1\0\0\0"
OUTPUT_MAGIC = b"D12CSRSLICEV1\0\0\0"
SOURCE_PRIME = 1_073_741_827
SOURCE_PROVIDER_FINGERPRINT = 9_218_588_987_274_412_661
SOURCE_RECORDS = 147_230
MAX_CENTERED_COEFFICIENT = 1_440
HEADER = struct.Struct("<16sIIIIQQ32s32s")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def read_exact(stream, size: int) -> bytes:
    value = stream.read(size)
    require(len(value) == size, "truncated source cache")
    return value


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def atomic_write(path: Path, payload: bytes) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_bytes(payload)
    os.replace(temporary, path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--expect-sha256", required=True)
    parser.add_argument("--records", type=int, default=32_768)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--ledger", type=Path, required=True)
    args = parser.parse_args()

    require(sys.byteorder == "little", "little-endian exporter required")
    require(1 <= args.records <= SOURCE_RECORDS, "record count out of range")
    source_sha = sha256_file(args.input)
    require(source_sha == args.expect_sha256, "source cache SHA-256 mismatch")
    source_size = args.input.stat().st_size

    row_offsets = array.array("I", [0])
    column_indices = array.array("I")
    coefficients = array.array("i")
    row_ids: dict[int, int] = {}
    coefficient_histogram: Counter[int] = Counter()
    row_size_histogram: Counter[int] = Counter()
    column_digest = hashlib.sha256()
    first_column = None
    last_column = None
    previous_column = None

    with args.input.open("rb") as stream:
        require(read_exact(stream, 12) == SOURCE_MAGIC, "bad source cache magic")
        prime, provider_fingerprint, vector_fingerprint, total_records = struct.unpack(
            "<QQQQ", read_exact(stream, 32)
        )
        require(prime == SOURCE_PRIME, "source prime changed")
        require(provider_fingerprint == SOURCE_PROVIDER_FINGERPRINT,
                "source provider fingerprint changed")
        require(total_records == SOURCE_RECORDS, "source record count changed")

        for record_index in range(args.records):
            word_bytes = read_exact(stream, 2)
            word = struct.unpack("<H", word_bytes)[0]
            multiplier = read_exact(stream, 13)
            size_bytes = read_exact(stream, 8)
            size = struct.unpack("<Q", size_bytes)[0]
            require(word < 6561, "bad source word")
            require(multiplier[0] == 8, "bad source multiplier degree")
            require(1 <= size <= 700_000, "bad source vector size")
            column_key = (word, multiplier)
            require(previous_column is None or previous_column < column_key,
                    "source columns not strictly ordered")
            previous_column = column_key
            encoded_column = word_bytes + multiplier + size_bytes
            column_digest.update(encoded_column)
            column_label = f"{word}:{multiplier[1:].hex()}"
            first_column = first_column or column_label
            last_column = column_label
            row_size_histogram[int(size)] += 1

            previous_row = None
            for _ in range(size):
                row = read_exact(stream, 13)
                raw_value_bytes = read_exact(stream, 8)
                raw_value = struct.unpack("<Q", raw_value_bytes)[0]
                require(row[0] == 12, "bad source row degree")
                require(previous_row is None or previous_row < row,
                        "source vector rows not strictly ordered")
                previous_row = row
                require(0 < raw_value < SOURCE_PRIME, "bad source residue")
                centered = (raw_value if raw_value <= SOURCE_PRIME // 2
                            else raw_value - SOURCE_PRIME)
                require(abs(centered) <= MAX_CENTERED_COEFFICIENT,
                        "source residue lacks a unique bounded integral lift")
                row_key = int.from_bytes(row[1:], "little")
                dense_id = row_ids.get(row_key)
                if dense_id is None:
                    dense_id = len(row_ids)
                    require(dense_id < 2**32, "dense row ID overflow")
                    row_ids[row_key] = dense_id
                column_indices.append(dense_id)
                coefficients.append(centered)
                coefficient_histogram[centered] += 1
                column_digest.update(row)
                column_digest.update(raw_value_bytes)
            require(len(column_indices) < 2**32, "slice NNZ exceeds u32 CSR")
            row_offsets.append(len(column_indices))

        selected_end_offset = stream.tell()

    require(len(row_offsets) == args.records + 1, "CSR row pointer count")
    require(len(column_indices) == len(coefficients), "CSR payload lengths")
    require(row_offsets[-1] == len(column_indices), "CSR terminal offset")

    row_bytes = row_offsets.tobytes()
    column_bytes = column_indices.tobytes()
    coefficient_bytes = coefficients.tobytes()
    payload = row_bytes + column_bytes + coefficient_bytes
    payload_sha = hashlib.sha256(payload).digest()
    header = HEADER.pack(
        OUTPUT_MAGIC,
        1,
        SOURCE_PRIME,
        args.records,
        len(row_ids),
        len(column_indices),
        source_size,
        bytes.fromhex(source_sha),
        payload_sha,
    )
    require(len(header) == 112, "CSR header size")
    atomic_write(args.output, header + payload)

    result = {
        "status": "PASS_EXACT_D12_PERSISTED_VECTOR_TO_CSR_SLICE",
        "schema": "KRENN_AFFINE251_D12_CSR_SLICE_V1",
        "source": {
            "path": str(args.input),
            "sha256": source_sha,
            "bytes": source_size,
            "magic": SOURCE_MAGIC.hex(),
            "prime": prime,
            "provider_fingerprint": provider_fingerprint,
            "vector_fingerprint": vector_fingerprint,
            "records": total_records,
        },
        "selection": {
            "rule": "first N records in the source cache's strict canonical column order",
            "records": args.records,
            "selected_end_offset": selected_end_offset,
            "first_column": first_column,
            "last_column": last_column,
            "literal_prefix_sha256": column_digest.hexdigest(),
        },
        "csr": {
            "path": str(args.output),
            "sha256": hashlib.sha256((header + payload)).hexdigest(),
            "payload_sha256": payload_sha.hex(),
            "rows": args.records,
            "columns": len(row_ids),
            "nnz": len(column_indices),
            "row_nnz_min": min(row_size_histogram),
            "row_nnz_max": max(row_size_histogram),
            "coefficient_min": min(coefficient_histogram),
            "coefficient_max": max(coefficient_histogram),
            "max_abs_coefficient": max(map(abs, coefficient_histogram)),
            "offset_type": "u32-le",
            "index_type": "u32-le",
            "coefficient_type": "centered-i32-le",
        },
        "row_size_histogram": {str(key): value for key, value in sorted(row_size_histogram.items())},
        "coefficient_histogram": {str(key): value for key, value in sorted(coefficient_histogram.items())},
        "scope": "A deterministic regular CSR pairing slice only; no closure expansion, rank, membership, or higher-degree computation.",
    }
    atomic_write(args.ledger, (json.dumps(result, indent=2, sort_keys=True) + "\n").encode())
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
