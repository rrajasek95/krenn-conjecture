#!/usr/bin/env python3
"""Tiny cache-format positive and fail-closed hostile controls; no large input."""

from __future__ import annotations

import json
from pathlib import Path
import struct
import subprocess
import tempfile


PACKAGE = Path(__file__).resolve().parent
BINARY = PACKAGE / "rare_order_index_gate"
PRIME = 1073741827
PROVIDER = 9218588987274412661
OFFSET = 14695981039346656037
MASK = (1 << 64) - 1


def mono(ids: tuple[int, ...]) -> bytes:
    if tuple(sorted(ids)) != ids or len(ids) > 12:
        raise ValueError(ids)
    return bytes([len(ids)]) + bytes(ids) + bytes(12 - len(ids))


def fnv(data: bytes, value: int = OFFSET) -> int:
    for byte in data:
        value = ((value ^ byte) * 1099511628211) & MASK
    return value


def write_cache(path: Path, records: list[tuple[int, tuple[int, ...], list[tuple[tuple[int, ...], int]]]]) -> None:
    payload = bytearray()
    fingerprint = OFFSET
    for word, multiplier, vector in records:
        fields = struct.pack("<H", word) + mono(multiplier) + struct.pack("<Q", len(vector))
        payload += fields
        fingerprint = fnv(fields, fingerprint)
        for row, value in vector:
            fields = mono(row) + struct.pack("<Q", value)
            payload += fields
            fingerprint = fnv(fields, fingerprint)
    header = b"AFF12VEC1\0\0\0" + struct.pack("<QQQQ", PRIME, PROVIDER, fingerprint, len(records))
    path.write_bytes(header + payload)


def run(binary: Path, old: Path, new: Path, output: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            str(binary), "--old-cache", str(old), "--new-cache", str(new),
            "--output", str(output), "--expected-old-records", "2",
            "--expected-new-records", "3", "--expected-new-columns", "1",
            "--wall-seconds", "10", "--rss-gib", "1",
        ],
        capture_output=True,
        text=True,
    )


def main() -> None:
    row_a = tuple([1] * 12)
    row_b = tuple([2] * 12)
    row_c = tuple([3] * 12)
    target = tuple([251] * 12)
    multiplier = tuple([4] * 8)
    old_records = [
        (1, multiplier, [(row_a, 1), (target, 2)]),
        (3, multiplier, [(row_b, 3)]),
    ]
    new_records = [
        old_records[0],
        (2, multiplier, [(row_a, 4), (row_c, 5)]),
        old_records[1],
    ]
    with tempfile.TemporaryDirectory(prefix="rare-order-tiny-") as directory:
        directory = Path(directory)
        old = directory / "old.bin"
        new = directory / "new.bin"
        result = directory / "result.json"
        write_cache(old, old_records)
        write_cache(new, new_records)
        positive = run(BINARY, old, new, result)
        if positive.returncode != 0:
            raise RuntimeError(("positive", positive.stderr))
        parsed = json.loads(result.read_text())
        if parsed["status"] != "PASS_EXACT_ROUND849_850_ORDER_EQUIVALENCE":
            raise RuntimeError("positive status")
        hostile = directory / "hostile.bin"
        damaged = bytearray(new.read_bytes())
        damaged[0] ^= 1
        hostile.write_bytes(damaged)
        hostile_result = directory / "hostile.json"
        rejected = run(BINARY, old, hostile, hostile_result)
        if rejected.returncode == 0 or hostile_result.exists():
            raise RuntimeError("hostile cache magic accepted")
    evidence = {
        "schema": "KRENN_AFF251_D12_RARE_ORDER_INDEX_TINY_HOSTILES_V1",
        "status": "PASS",
        "positive_cache_and_order": True,
        "hostile_bad_magic_rejected": True,
        "large_cache_read": False,
    }
    (PACKAGE / "tiny_hostile_results.json").write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n")
    print(json.dumps(evidence, sort_keys=True))


if __name__ == "__main__":
    main()
