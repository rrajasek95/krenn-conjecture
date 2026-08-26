#!/usr/bin/env python3
"""Referee the exact-Q nine-row Q3-exception mate unit."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import subprocess
import tempfile


HERE = Path(__file__).resolve().parent
MINER = HERE / "mine_Q3_fixed_left_mate_core.py"
MINED = HERE / "results_Q3_fixed_left_mate_core.json"
INPUT = HERE / "Q3_fixed_left_mate_core_exact.msolve"
FROZEN_OUTPUT = HERE / "results_Q3_fixed_left_mate_core_exact.full.gb.out"
OUT = HERE / "results_Q3_fixed_left_mate_core_exact_audit.json"
EXPECTED_ALIASES = [
    ["mate_t_123"],
    ["mate_cofactor_9"],
    ["mate_cofactor_11"],
    ["mate_cofactor_15"],
    ["mate_cofactor_19"],
    ["mate_cofactor_22"],
    ["mate_Q_15"],
    ["mate_Q_9"],
    ["mate_Q_0"],
]


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def is_unit_basis(path):
    text = path.read_text()
    return ("#field characteristic: 0" in text and
            "#length of basis:      1 element" in text and
            text.rstrip().endswith("[1]:"))


def main():
    mined = json.loads(MINED.read_text())
    require(mined["active_aliases"] == EXPECTED_ALIASES,
            "Q3 exact core labels changed")
    require(mined["ordinary_row_count"] == 9,
            "Q3 exact core row count changed")
    require(all(not record["unit"]
                for record in mined["minimality_mutations"]),
            "Q3 modular inclusion-minimality mutation changed")
    lines = INPUT.read_text().splitlines()
    require(lines[1] == "0" and len(lines[0].split(",")) == 17,
            "Q3 exact input header changed")
    require(len("\n".join(lines[2:]).split(",\n")) == 10,
            "Q3 exact input row count changed")
    require(is_unit_basis(FROZEN_OUTPUT), "frozen Q3 exact basis is not [1]")
    with tempfile.TemporaryDirectory(prefix="q3-exact-referee-") as tmp:
        replay = Path(tmp) / "replay.gb.out"
        completed = subprocess.run(
            ["msolve", "-f", str(INPUT), "-o", str(replay), "-t", "4",
             "-g", "2", "-v", "0", "-l", "2"],
            capture_output=True, text=True, timeout=30, check=False)
        require(completed.returncode == 0 and is_unit_basis(replay),
                "Q3 exact msolve replay failed")
        replay_sha = sha256(replay.read_bytes()).hexdigest()
    result = {
        "status": "UNAUDITED exact-Q Q3-exception mate core UNIT audit PASS",
        "ordinary_rows": EXPECTED_ALIASES,
        "ordinary_row_count": 9,
        "mate_H_rabinowitsch": "u*H_mate-1",
        "exact_basis": "[1]",
        "literal_replay": True,
        "modular_inclusion_minimality_mutations": True,
        "input_sha256": sha256(INPUT.read_bytes()).hexdigest(),
        "frozen_output_sha256": sha256(FROZEN_OUTPUT.read_bytes()).hexdigest(),
        "replay_output_sha256": replay_sha,
        "conclusion": (
            "Any left presentation with the minimal nested Q3-exception "
            "incidence signature has no H-live mate. The second observed "
            "signature adds one directional cofactor row and is subsumed."
        ),
        "scope_guard": (
            "The polynomial unit is exact over Q for the declared incidence "
            "signature. Application to the full Q3=0 source divisor still "
            "requires covering special sub-strata where one of the left "
            "entry/cofactor/Q localizers defining this signature vanishes."
        ),
        "source_hashes": {
            "miner": sha256(MINER.read_bytes()).hexdigest(),
            "mined": sha256(MINED.read_bytes()).hexdigest(),
        },
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print("Q3 exact mate core audit PASS")
    print("result", result["result_sha256"])


if __name__ == "__main__":
    main()
