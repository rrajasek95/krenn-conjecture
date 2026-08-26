#!/usr/bin/env python3
"""Build guarded p1 branch inputs for subsets of omitted literal cofactors."""

from __future__ import annotations

from itertools import combinations
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
BASE = HERE.parent / "unaudited-codex-d0-c0-eliminant-audit-2026-08-21"
PRIMES = (1073741827, 536870909)


def main() -> None:
    rows = json.loads((HERE / "d0_omitted_rows.json").read_text())["rows"]
    by_label = {row["source_label"]: row["polynomial"] for row in rows}
    labels = tuple(by_label)
    for branch in (0, 1):
        for prime in PRIMES:
            base = BASE / f"d0_factor{branch}_p{prime}_resat.ms"
            lines = base.read_text().splitlines()
            assert not lines[-1].endswith(",")
            for size in range(2, len(labels) + 1):
                for subset in combinations(labels, size):
                    tag = "_".join(label.split("_")[1] for label in subset)
                    target = HERE / f"d0_factor{branch}_subset_{tag}_p{prime}.ms"
                    extra = [by_label[label] + "," for label in subset]
                    target.write_text("\n".join(lines[:-1] + extra +
                                                 [lines[-1]]) + "\n")


if __name__ == "__main__":
    main()
