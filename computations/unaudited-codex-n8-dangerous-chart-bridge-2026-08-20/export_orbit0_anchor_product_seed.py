#!/usr/bin/env python3
"""Export the exact orbit-0 anchor-product membership problem.

The target is the product of the twelve named anchor cells.  It has total
degree 12 and anchor-adic degree zero.  Using cutoff 13 therefore retains
every degree-12 row, so target membership in the resulting closed component
is literal membership in the degree-12 part of I_mix, not a truncated claim.
"""

from __future__ import annotations

from hashlib import sha256
import argparse
import importlib.util
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXPORT_PATH = HERE / "export_orbit0_cutoff_seed.py"
SPEC = importlib.util.spec_from_file_location("orbit0_cutoff", EXPORT_PATH)
ORBIT0 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ORBIT0)


def incident_mixed_words() -> tuple[tuple[int, ...], ...]:
    """Words whose M0 term divides the twelve-anchor target."""
    words = []
    for c01 in ORBIT0.BASE.COLORS:
        for c23 in ORBIT0.BASE.COLORS:
            for c45 in ORBIT0.BASE.COLORS:
                for c67 in ORBIT0.BASE.COLORS:
                    word = (c01, c01, c23, c23, c45, c45, c67, c67)
                    if len(set(word)) > 1:
                        words.append(word)
    return tuple(words)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path,
                        default=HERE / "orbit0_anchor_product_cutoff13_seed.txt")
    args = parser.parse_args()

    target = bytes(sorted(ORBIT0.ANCHORS))
    orbit = ORBIT0.row_orbit(target)
    incident = incident_mixed_words()
    assert len(target) == 12
    assert ORBIT0.BASE.row_degree(target, ORBIT0.ANCHORS) == 0
    assert orbit == {target}
    assert len(incident) == 3 ** 4 - 3 == 78

    lines = [
        "KRENN_ANCHOR_K_CUTOFF_SEED_V1",
        "CUTOFF 13",
        "ANCHORS " + target.hex(),
    ]
    for sites, colours in ORBIT0.STABILIZER:
        lines.append("ACTION " + "".join(map(str, sites)) + " "
                     + "".join(map(str, colours)))
    lines.append(f"TARGET {target.hex()} 1 1")
    payload = "\n".join(lines) + "\n"
    args.output.write_text(payload)

    print("orbit: 0")
    print("total degree / cutoff: 12 / 13")
    print("stabilizer:", len(ORBIT0.STABILIZER))
    print("target orbit size / mass: 1 / 1")
    print("target K-degree: 0")
    print("literal incident mixed words:", len(incident))
    print("seed bytes:", len(payload))
    print("seed sha256:", sha256(payload.encode("ascii")).hexdigest())
    print("path:", args.output)


if __name__ == "__main__":
    main()
