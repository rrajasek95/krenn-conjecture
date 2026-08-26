#!/usr/bin/env python3
"""DO NOT USE: exporter for an incomplete chosen-section transfer family.

The 9,954 staged transfers omit the internal minimum-degree-five kernel.  The
entry point fails deliberately so this file cannot seed a misleading closure.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import argparse
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
D6_PATH = HERE / "probe_legacy27_k7_residual.py"
SPEC = importlib.util.spec_from_file_location("legacy27_k7_sound_seed", D6_PATH)
D6 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(D6)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def main():
    raise RuntimeError(
        "INCOMPLETE transfer family: internal minimum-degree-five kernel omitted"
    )
    parser = argparse.ArgumentParser()
    parser.add_argument("--prime", type=int, default=1009,
                        choices=(1009, 1013))
    args = parser.parse_args()
    stage = HERE / f"k7_lower_kernel_transfers_p{args.prime}.jsonl"
    out = HERE / f"legacy27_k7_sound_p{args.prime}_seed.txt"
    residual = D6.frozen_residual()
    require(len(residual) == 29669, "frozen K6 residual support changed")
    seed = {row: Fraction(value) for row, value in residual.items()}
    transfer_rows = set()
    with stage.open() as handle:
        header = json.loads(next(handle))
        require(header["format"] == "krenn-legacy27-degree6-lower-kernel-v1"
                and header["prime"] == args.prime
                and header["kernel_dimension"] == 9954,
                "legacy27 lower-kernel stage header changed")
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
        "EXPECTED 0 0 0 0 0",
    ]
    for sites, colours in D6.PROBE.STABILIZER:
        lines.append(
            "ACTION " + "".join(map(str, sites)) + " "
            + "".join(map(str, colours))
        )
    for row, coefficient in sorted(seed.items()):
        lines.append(
            f"ROW {row.hex()} {coefficient.numerator} "
            f"{coefficient.denominator}"
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
