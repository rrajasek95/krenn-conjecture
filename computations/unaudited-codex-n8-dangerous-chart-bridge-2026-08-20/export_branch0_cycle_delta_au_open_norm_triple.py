#!/usr/bin/env python3
"""Assemble the three p1009 non-live pair-norm factors for msolve.

Each input factor was produced by the source-derived quotient-resultant
probe for LR, LT, or RT.  Their common zero set contains the parameter
projection of any solution of Q=L=R=T=0 on the declared open chart.  This
is a modular discovery interface, not a characteristic-zero theorem.
"""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
TOOLKIT = HERE.parent / "toolkit" / "groebner"
PAIRS = ("LR", "LT", "RT")
INPUTS = {
    pair: HERE / f"branch0_cycle_delta_au_open_norm_{pair}_p1009.factor"
    for pair in PAIRS
}
OUTPUT = HERE / "branch0_cycle_delta_au_open_norm_triple_p1009.msolve"
LABELS = HERE / "branch0_cycle_delta_au_open_norm_triple_labels.json"
RESULT = HERE / "results_branch0_cycle_delta_au_open_norm_triple_export.json"

if str(TOOLKIT) not in sys.path:
    sys.path.append(str(TOOLKIT))
from msolve_io import read_msolve_input  # noqa: E402


def main():
    factors = [INPUTS[pair].read_text().strip() for pair in PAIRS]
    OUTPUT.write_text("d1,x\n1009\n" + ",\n".join(factors) + "\n")
    labels = [f"norm_{pair}_nonlive" for pair in PAIRS]
    LABELS.write_text(json.dumps({"labels": labels}, indent=2) + "\n")
    parsed = read_msolve_input(OUTPUT, strict=True)
    result = {
        "status": "UNAUDITED p1009 pair-norm triple export",
        "prime": 1009,
        "variables": ["d1", "x"],
        "labels": labels,
        "factor_files": {
            pair: {
                "path": INPUTS[pair].name,
                "sha256": sha256(INPUTS[pair].read_bytes()).hexdigest(),
            }
            for pair in PAIRS
        },
        "factor_bytes": [len(value) for value in factors],
        "input_file": OUTPUT.name,
        "input_file_sha256": parsed.file_sha256,
        "input_logical_sha256": parsed.logical_sha256,
        "scope": (
            "A common zero is necessary for the projected three-minor "
            "packet on the A-open chart. Modular unit would be discovery "
            "evidence only; any survivor must be filtered by all live "
            "factors and replayed in the exact full packet."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("branch-0 Delta Au-open norm triple export: PASS")
    print("factor bytes:", result["factor_bytes"])
    print("input sha256:", result["input_file_sha256"])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
