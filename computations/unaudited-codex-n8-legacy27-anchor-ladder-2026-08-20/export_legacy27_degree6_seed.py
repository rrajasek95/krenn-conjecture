#!/usr/bin/env python3
"""Export the frozen legacy27 degree-six residual for generic Rust closure."""

from __future__ import annotations

from hashlib import sha256
import argparse
import importlib.util
from pathlib import Path


HERE = Path(__file__).resolve().parent
PRODUCER = HERE / "probe_legacy27_k7_residual.py"
SPEC = importlib.util.spec_from_file_location("legacy27_k7_seed", PRODUCER)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
OUT = HERE / "legacy27_degree6_seed.txt"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUT)
    args = parser.parse_args()
    residual = MODULE.frozen_residual()
    require(len(residual) == 29669,
            "legacy27 degree-six residual support changed")
    lines = [
        "KRENN_ANCHOR_K_SEED_V1",
        "DEGREE 6",
        "ANCHORS " + bytes(sorted(MODULE.PROBE.ANCHORS)).hex(),
        "EXPECTED 0 0 0 0 0",
    ]
    for sites, colours in MODULE.PROBE.STABILIZER:
        lines.append(
            "ACTION " + "".join(map(str, sites)) + " "
            + "".join(map(str, colours))
        )
    for row, coefficient in sorted(residual.items()):
        lines.append(
            f"ROW {row.hex()} {coefficient.numerator} "
            f"{coefficient.denominator}"
        )
    payload = "\n".join(lines) + "\n"
    args.output.write_text(payload)
    print("seed rows:", len(residual))
    print("seed bytes:", len(payload))
    print("seed sha256:", sha256(payload.encode("ascii")).hexdigest())


if __name__ == "__main__":
    main()
