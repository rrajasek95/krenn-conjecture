#!/usr/bin/env python3
"""Export the complete invariant target below K^7 for mixed-degree closure."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
from pathlib import Path


HERE = Path(__file__).resolve().parent
D5_PATH = HERE / "audit_degree5_chart26.py"
SPEC = importlib.util.spec_from_file_location("degree5_audit", D5_PATH)
D5 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(D5)
PROBE = D5.PROBE
BASE = D5.BASE
OUT = HERE / "chart26_cutoff7_seed.txt"


def invariant_target_below_cutoff():
    actual = D5.target_actual((0, 2, 3, 4, 5, 6))
    target = Counter()
    for row, coefficient in actual.items():
        representative = PROBE.canonical_row(row)
        if row == representative:
            target[representative] = (
                Fraction(coefficient) * D5.row_orbit_size(representative)
            )
    return actual, target


def main():
    actual, target = invariant_target_below_cutoff()
    histogram = Counter(BASE.row_degree(row, PROBE.ANCHORS)
                        for row in target)
    lines = [
        "KRENN_ANCHOR_K_CUTOFF_SEED_V1",
        "CUTOFF 7",
        "ANCHORS " + bytes(sorted(PROBE.ANCHORS)).hex(),
    ]
    for sites, colours in PROBE.STABILIZER:
        lines.append(
            "ACTION " + "".join(map(str, sites)) + " "
            + "".join(map(str, colours))
        )
    for row, coefficient in sorted(target.items()):
        lines.append(
            f"TARGET {row.hex()} {coefficient.numerator} "
            f"{coefficient.denominator}"
        )
    payload = "\n".join(lines) + "\n"
    OUT.write_text(payload)
    print("cutoff: 7")
    print("actual target rows:", len(actual))
    print("target row orbits:", len(target))
    print("target orbit degree histogram:", dict(sorted(histogram.items())))
    print("seed bytes:", len(payload))
    print("seed sha256:", sha256(payload.encode("ascii")).hexdigest())
    print("path:", OUT.relative_to(HERE.parent.parent))


if __name__ == "__main__":
    main()
