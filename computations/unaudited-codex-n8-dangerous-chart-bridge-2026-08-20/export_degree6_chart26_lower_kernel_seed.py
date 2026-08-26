#!/usr/bin/env python3
"""Export residual plus modular lower-kernel d6 support for Rust closure."""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import argparse
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
D6_PATH = HERE / "probe_degree6_chart26_residual.py"
SPEC = importlib.util.spec_from_file_location("degree6_residual", D6_PATH)
D6 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(D6)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prime", type=int, default=1009)
    args = parser.parse_args()
    stage = HERE / f"degree6_lower_kernel_transfers_p{args.prime}.jsonl"
    out = HERE / f"degree6_lower_kernel_seed_p{args.prime}.txt"

    residual = D6.frozen_residual()
    seed = {row: Fraction(value) for row, value in residual.items()}
    transfer_rows = set()
    with stage.open() as handle:
        header = json.loads(next(handle))
        if (header["format"] != "krenn-chart26-degree6-lower-kernel-v1"
                or header["prime"] != args.prime
                or header["kernel_dimension"] != 3274):
            raise RuntimeError("lower-kernel stage header changed")
        for line in handle:
            record = json.loads(line)
            for row_hex, value in record["tail6"]:
                if value % args.prime:
                    transfer_rows.add(bytes.fromhex(row_hex))
    for row in transfer_rows:
        seed.setdefault(row, Fraction(0))

    lines = [
        "KRENN_ANCHOR_K_SEED_V1",
        "DEGREE 6",
        "ANCHORS " + bytes(sorted(D6.PROBE.ANCHORS)).hex(),
        # Unknown until Rust finishes.  The current Rust control binary writes
        # its matrix/results before rejecting this sentinel mismatch.
        "EXPECTED 0 0 0 0 0",
    ]
    for sites, colours in D6.PROBE.STABILIZER:
        lines.append(
            "ACTION " + "".join(map(str, sites)) + " "
            + "".join(map(str, colours))
        )
    for row, coefficient in sorted(seed.items()):
        lines.append(
            f"ROW {row.hex()} {coefficient.numerator} {coefficient.denominator}"
        )
    payload = "\n".join(lines) + "\n"
    out.write_text(payload)
    print("prime:", args.prime)
    print("residual rows:", len(residual))
    print("transfer support rows:", len(transfer_rows))
    print("union seed rows:", len(seed))
    print("seed bytes:", len(payload))
    print("seed sha256:", sha256(payload.encode("ascii")).hexdigest())
    print("path:", out.relative_to(HERE.parent.parent))


if __name__ == "__main__":
    main()
