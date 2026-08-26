#!/usr/bin/env python3
"""Export the frozen zero26/d6 residual and stabilizer as a compact text seed."""

from __future__ import annotations

from hashlib import sha256
import argparse
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
PRODUCER = (HERE.parent / "unaudited-codex-n8-dangerous-chart-bridge-2026-08-20"
            / "probe_degree6_chart26_residual.py")
SPEC = importlib.util.spec_from_file_location("degree6_producer", PRODUCER)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
OUT = HERE / "chart26_degree6_seed.txt"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--transfer-jsonl", type=Path)
    parser.add_argument("--output", type=Path, default=OUT)
    args = parser.parse_args()
    residual = MODULE.frozen_residual()
    assert len(residual) == 12705
    lines = [
        "KRENN_ANCHOR_K_SEED_V1",
        "DEGREE 6",
        "ANCHORS " + bytes(sorted(MODULE.PROBE.ANCHORS)).hex(),
        ("EXPECTED 140578 361406 22 7149 8889"
         if args.transfer_jsonl is None else "EXPECTED 0 0 0 0 0"),
    ]
    for sites, colours in MODULE.PROBE.STABILIZER:
        lines.append(
            "ACTION " + "".join(map(str, sites)) + " "
            + "".join(map(str, colours))
        )
    support = set(residual)
    if args.transfer_jsonl is not None:
        with args.transfer_jsonl.open() as handle:
            header = json.loads(next(handle))
            assert header["format"] == "krenn-chart26-degree6-lower-kernel-v1"
            for line in handle:
                record = json.loads(line)
                support.update(bytes.fromhex(row_hex)
                               for row_hex, _value in record["tail6"])
    for row in sorted(support):
        coefficient = residual.get(row, 0)
        if coefficient:
            numerator, denominator = coefficient.numerator, coefficient.denominator
        else:
            numerator, denominator = 0, 1
        lines.append(
            f"ROW {row.hex()} {numerator} {denominator}"
        )
    payload = "\n".join(lines) + "\n"
    args.output.write_text(payload)
    print("seed rows:", len(support))
    print("seed bytes:", len(payload))
    print("seed sha256:", sha256(payload.encode("ascii")).hexdigest())


if __name__ == "__main__":
    main()
