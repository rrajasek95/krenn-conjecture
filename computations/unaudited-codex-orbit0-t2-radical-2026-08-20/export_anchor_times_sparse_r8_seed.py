#!/usr/bin/env python3
"""Export the valid chart-local target a*R8' for whole cutoff<9 closure."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
BRIDGE = HERE.parent / "unaudited-codex-n8-dangerous-chart-bridge-2026-08-20"
R8 = BRIDGE / "results_orbit0_cutoff9_sparse_r8.json"
R8_SEED = HERE / "sparse_r8_seed.txt"
OUT = HERE / "anchor_times_sparse_r8_cutoff9_seed.txt"
RESULTS = HERE / "results_anchor_times_sparse_r8_cutoff9_seed.json"
R8_DIGEST = "877ca35865130bd9ca55f19387b44d9473acd2b47d5eddd2d29c1718831cf968"


def main():
    payload = json.loads(R8.read_text())
    if payload["result_sha256"] != R8_DIGEST:
        raise RuntimeError("sparse R8 changed")
    source = R8_SEED.read_text().splitlines()
    anchor_hex = next(line.split()[1] for line in source
                      if line.startswith("ANCHORS "))
    anchor = bytes.fromhex(anchor_hex)
    actions = [line for line in source if line.startswith("ACTION ")]
    lines = [
        "KRENN_WHOLE_ANCHOR_TIMES_R8_CUTOFF9_SEED_V1",
        "DEGREE 24",
        "CUTOFF 9",
        f"ANCHORS {anchor_hex}",
        *actions,
    ]
    for row_hex, numerator, denominator in payload["residual"]:
        row = bytes(sorted(anchor + bytes.fromhex(row_hex)))
        lines.append(f"TARGET {row.hex()} {numerator} {denominator}")
    text = "\n".join(lines) + "\n"
    OUT.write_text(text)
    result = {
        "status": "exact chart-local a*R8' whole-cutoff9 seed",
        "sparse_r8_logical_sha256": R8_DIGEST,
        "seed_sha256": sha256(text.encode("ascii")).hexdigest(),
        "stabilizer_order": len(actions),
        "target_row_orbits": len(payload["residual"]),
        "target_total_degree": 24,
        "target_K_degree": 8,
        "cutoff": 9,
        "congruence": (
            "a*T is congruent to a*R8' modulo I_mix+K^9 because a has "
            "K-degree zero and T-R8' lies in I_mix+K^9"
        ),
        "scope": (
            "A positive whole-cutoff9 lift advances chart-local saturation. "
            "A negative result is only nonmembership modulo K^9, not a "
            "localized obstruction."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    RESULTS.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("anchor times sparse R8 cutoff9 seed: PASS")
    print("rows/actions:", result["target_row_orbits"], len(actions))
    print("seed sha256:", result["seed_sha256"])
    print("logical sha256:", result["logical_sha256"])


if __name__ == "__main__":
    main()
