#!/usr/bin/env python3
"""Export the exact invariant P^2 target rows for the Rust closure engine."""

from __future__ import annotations

import pickle
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = Path("/tmp/diagonal_power2_v2.pkl")
OUTPUT = Path(__file__).with_name("p2_target_seed.txt")


def main():
    if SOURCE.exists():
        with SOURCE.open("rb") as handle:
            data = pickle.load(handle)
    else:
        sys.path.insert(0, str(ROOT / "computations"))
        from test_diagonal_power2 import build_matrix
        data = build_matrix(SOURCE)
    assert data["version"] == 2 and data["shape"] == (874, 5530)
    rows = []
    for index, coefficient in enumerate(data["b"]):
        coefficient = int(coefficient)
        if coefficient:
            gs = data["row_reps"][index]
            rows.append((*gs, coefficient))
    assert len(rows) == 663
    with OUTPUT.open("w", encoding="ascii") as handle:
        handle.write("KRENN_P2_TARGET_V1\n")
        for g0, g1, g2, coefficient in rows:
            handle.write(f"ROW {g0} {g1} {g2} {coefficient}\n")
    print(f"wrote {OUTPUT}: {len(rows)} target row orbits")


if __name__ == "__main__":
    main()
