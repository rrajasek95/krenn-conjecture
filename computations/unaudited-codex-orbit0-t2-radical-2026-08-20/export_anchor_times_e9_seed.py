#!/usr/bin/env python3
"""Export the next chart-local residual a*E9 for whole cutoff<10 closure."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
TAIL = HERE / "results_sparse_r8_k9_tail.json"
R8_SEED = HERE / "sparse_r8_seed.txt"
OUT = HERE / "anchor_times_e9_cutoff10_seed.txt"
RESULTS = HERE / "results_anchor_times_e9_cutoff10_seed.json"
TAIL_SHA = "6b85cca58d6da26f426404eb785b2d9bf7858a4c758a651e1e9aa66729b08132"


def main():
    if sha256(TAIL.read_bytes()).hexdigest() != TAIL_SHA:
        raise RuntimeError("K9 tail changed")
    tail = json.loads(TAIL.read_text())
    source = R8_SEED.read_text().splitlines()
    anchor_hex = next(line.split()[1] for line in source
                      if line.startswith("ANCHORS "))
    anchor = bytes.fromhex(anchor_hex)
    actions = [line for line in source if line.startswith("ACTION ")]
    lines = [
        "KRENN_WHOLE_ANCHOR_TIMES_E9_CUTOFF10_SEED_V1",
        "DEGREE 24",
        "CUTOFF 10",
        f"ANCHORS {anchor_hex}",
        *actions,
    ]
    for row_hex, coefficient in tail["tail"]:
        row = bytes(sorted(anchor + bytes.fromhex(row_hex)))
        lines.append(f"TARGET {row.hex()} {coefficient} 1")
    text = "\n".join(lines) + "\n"
    OUT.write_text(text)
    result = {
        "status": "exact chart-local a*E9 whole-cutoff10 seed",
        "tail_file_sha256": TAIL_SHA,
        "seed_sha256": sha256(text.encode("ascii")).hexdigest(),
        "stabilizer_order": len(actions),
        "target_row_orbits": len(tail["tail"]),
        "target_total_degree": 24,
        "target_K_degree": 9,
        "cutoff": 10,
        "scope": (
            "This is the exact next residual after the three-packet grade8 "
            "cleanup of a*R8'. A positive whole-cutoff10 lift advances the "
            "orbit0 chart target; a negative result is cutoff-relative only."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    RESULTS.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("anchor times E9 cutoff10 seed: PASS")
    print("rows/actions:", result["target_row_orbits"], len(actions))
    print("seed sha256:", result["seed_sha256"])
    print("logical sha256:", result["logical_sha256"])


if __name__ == "__main__":
    main()
