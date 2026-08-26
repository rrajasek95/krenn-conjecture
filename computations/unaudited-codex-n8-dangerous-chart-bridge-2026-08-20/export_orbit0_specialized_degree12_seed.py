#!/usr/bin/env python3
"""Export orbit-0 anchors=1 target for the bounded degree-12 Macaulay test."""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import importlib.util
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXPORT_PATH = HERE / "export_orbit0_cutoff_seed.py"
SPEC = importlib.util.spec_from_file_location("special_seed_base", EXPORT_PATH)
ORBIT0 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ORBIT0)
BASE = ORBIT0.BASE
OUT = HERE / "orbit0_specialized_degree12_seed.txt"


def specialized(term: bytes) -> bytes:
    return bytes(cell for cell in term if cell not in ORBIT0.ANCHORS)


def encoded(row: bytes) -> str:
    return row.hex() if row else "-"


def main() -> None:
    pure = [[specialized(term) for term in BASE.word_terms((colour,) * 8)]
            for colour in BASE.COLORS]
    target = set()
    for left in pure[0]:
        for middle in pure[1]:
            prefix = left + middle
            for right in pure[2]:
                target.add(bytes(sorted(prefix + right)))
    if len(target) != 105 ** 3:
        raise RuntimeError("specialized target collision census changed")

    quotient = Counter()
    unseen = set(target)
    while unseen:
        row = unseen.pop()
        orbit = {bytes(sorted(transform[cell] for cell in row))
                 for transform in ORBIT0.TRANSFORMS}
        if not orbit <= target:
            raise RuntimeError("specialized target is not invariant")
        quotient[min(orbit)] = len(orbit)
        unseen.difference_update(orbit)
    if len(quotient) != 868 or sum(quotient.values()) != 105 ** 3:
        raise RuntimeError("specialized quotient target census changed")

    lines = [
        "KRENN_ANCHOR_SPECIALIZED_MACAULAY_SEED_V1",
        "MAX_TOTAL_DEGREE 12",
        "MAX_MULTIPLIER_DEGREE 8",
        "ANCHORS " + bytes(sorted(ORBIT0.ANCHORS)).hex(),
    ]
    for sites, colours in ORBIT0.STABILIZER:
        lines.append("ACTION " + "".join(map(str, sites)) + " "
                     + "".join(map(str, colours)))
    for row, mass in sorted(quotient.items()):
        lines.append(f"TARGET {encoded(row)} {mass} 1")
    payload = "\n".join(lines) + "\n"
    OUT.write_text(payload)
    print("stabilizer:", len(ORBIT0.STABILIZER))
    print("target labelled/orbits/mass:", len(target), len(quotient),
          sum(quotient.values()))
    print("target orbit degree histogram:",
          dict(sorted(Counter(map(len, quotient)).items())))
    print("seed bytes:", len(payload))
    print("seed sha256:", sha256(payload.encode("ascii")).hexdigest())
    print("path:", OUT)


if __name__ == "__main__":
    main()
