#!/usr/bin/env python3
"""Export the orbit0 anchor product a=m0*m1*m2 for whole cutoff<13."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
R8_SEED = HERE / "sparse_r8_seed.txt"
OUT = HERE / "anchor_product_cutoff13_seed.txt"
RESULTS = HERE / "results_anchor_product_cutoff13_seed.json"


def main():
    source = R8_SEED.read_text().splitlines()
    anchor_hex = next(line.split()[1] for line in source
                      if line.startswith("ANCHORS "))
    actions = [line for line in source if line.startswith("ACTION ")]
    if len(actions) != 2304:
        raise RuntimeError("orbit0 stabilizer changed")
    lines = [
        "KRENN_ANCHOR_K_CUTOFF_SEED_V1",
        "DEGREE 12",
        "CUTOFF 13",
        f"ANCHORS {anchor_hex}",
        "EXPECTED 0 0 0 0 0",
        *actions,
        f"TARGET {anchor_hex} 1 1",
    ]
    text = "\n".join(lines) + "\n"
    OUT.write_text(text)
    result = {
        "status": "exact orbit0 anchor-product cutoff13 seed",
        "seed_sha256": sha256(text.encode("ascii")).hexdigest(),
        "stabilizer_order": len(actions),
        "target_row_orbits": 1,
        "target": anchor_hex,
        "target_total_degree": 12,
        "target_K_degree": 0,
        "cutoff": 13,
        "scope": (
            "Since total degree is twelve, K^13 has no degree-12 component. "
            "A positive cutoff13 lift is literal a in I_mix; a modular "
            "negative result still needs an exact dual."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    RESULTS.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("anchor product cutoff13 seed: PASS")
    print("seed sha256:", result["seed_sha256"])
    print("logical sha256:", result["logical_sha256"])


if __name__ == "__main__":
    main()
