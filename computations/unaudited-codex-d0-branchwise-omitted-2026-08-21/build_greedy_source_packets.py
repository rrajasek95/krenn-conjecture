#!/usr/bin/env python3
"""Enumerate compatibility subsets for the exact three-cofactor packets."""

from __future__ import annotations

from itertools import combinations
from pathlib import Path


HERE = Path(__file__).resolve().parent
PRIME = 1073741827


def main():
    for branch in (0, 1):
        source = HERE / f"d0_factor{branch}_source_packet_p{PRIME}.ms"
        lines = source.read_text().splitlines()
        rows = lines[2:]
        assert len(rows) == 9
        # rows 0..3 compatibility, 4 factor, 5..7 omitted, 8 localizer.
        for size in range(1, 5):
            for subset in combinations(range(4), size):
                tag = "".join(str(i) for i in subset)
                chosen = [rows[i].rstrip(",") for i in subset]
                chosen += [row.rstrip(",") for row in rows[4:]]
                target = HERE / f"d0_factor{branch}_greedy_c{tag}_p{PRIME}.ms"
                target.write_text("\n".join(lines[:2]) + "\n" +
                                  ",\n".join(chosen) + "\n")


if __name__ == "__main__":
    main()
