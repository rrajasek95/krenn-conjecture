#!/usr/bin/env python3
"""Export the complete H0H1H2 target through anchor K-degree six."""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import argparse
import importlib.util
from pathlib import Path


HERE = Path(__file__).resolve().parent
PRODUCER = (HERE.parent / "unaudited-codex-n8-dangerous-chart-bridge-2026-08-20"
            / "probe_degree5_chart26_orbit.py")
SPEC = importlib.util.spec_from_file_location("chart26_orbit", PRODUCER)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
BASE = MODULE.BASE
OUT = HERE / "chart26_cutoff7_target_seed.txt"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cutoff", type=int, default=7)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    output = args.output or (HERE / f"chart26_cutoff{args.cutoff}_target_seed.txt")
    target = Counter()
    actual_by_degree = {}
    orbit_by_degree = {}
    for degree in range(args.cutoff):
        actual = BASE.filtered_target(MODULE.MATCHINGS, degree)
        quotient = Counter()
        for row, coefficient in actual.items():
            quotient[MODULE.canonical_row(row)] += coefficient
        actual_by_degree[degree] = len(actual)
        orbit_by_degree[degree] = len(quotient)
        target.update(quotient)
    if args.cutoff == 7:
        assert actual_by_degree == {0: 1, 1: 0, 2: 36, 3: 96,
                                    4: 612, 5: 2304, 6: 9120}
        assert orbit_by_degree == {0: 1, 1: 0, 2: 7, 3: 9,
                                   4: 78, 5: 160, 6: 762}
        assert len(target) == 1017 and sum(target.values()) == 12169
    if args.cutoff == 8:
        assert actual_by_degree[7] == 25344 and orbit_by_degree[7] == 1708
        assert len(target) == 2725 and sum(target.values()) == 37513
    lines = [
        "KRENN_ANCHOR_K_SEED_V1",
        f"CUTOFF {args.cutoff}",
        "ANCHORS " + bytes(sorted(MODULE.ANCHORS)).hex(),
        "EXPECTED 0 0 0 0 0",
    ]
    for sites, colours in MODULE.STABILIZER:
        lines.append("ACTION " + "".join(map(str, sites)) + " "
                     + "".join(map(str, colours)))
    for row, coefficient in sorted(target.items()):
        lines.append(f"ROW {row.hex()} {coefficient} 1")
    payload = "\n".join(lines) + "\n"
    output.write_text(payload)
    print("target actual by degree:", actual_by_degree)
    print("target orbit by degree:", orbit_by_degree)
    print("target orbit rows/mass:", len(target), sum(target.values()))
    print("seed sha256:", sha256(payload.encode("ascii")).hexdigest())


if __name__ == "__main__":
    main()
