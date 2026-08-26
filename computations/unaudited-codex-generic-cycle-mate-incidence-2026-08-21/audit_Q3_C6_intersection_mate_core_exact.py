#!/usr/bin/env python3
"""Referee the exact-Q eight-row Q3=C6 intersection mate unit."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import subprocess
import tempfile


HERE = Path(__file__).resolve().parent
MINER = HERE / "mine_Q3_C6_intersection_mate_core.py"
MINED = HERE / "results_Q3_C6_intersection_mate_core.json"
SIGNATURE = HERE / "results_localizer_face_signatures.json"
INPUT = HERE / "Q3_C6_intersection_mate_core_exact.msolve"
FROZEN_OUTPUT = HERE / "results_Q3_C6_intersection_mate_core_exact.full.gb.out"
OUT = HERE / "results_Q3_C6_intersection_mate_core_exact_audit.json"
EXPECTED_ALIASES = [
    ["mate_t_123"],
    ["mate_cofactor_0"],
    ["mate_cofactor_5"],
    ["mate_cofactor_8"],
    ["mate_cofactor_9"],
    ["mate_cofactor_15"],
    ["mate_Q_15"],
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
    signature = json.loads(SIGNATURE.read_text())
    intersections = signature["Q3_C6_intersections"]
    require(len(intersections) == 2 and
            all(record["H_nonzero"] for record in intersections),
            "Q3=C6 exact H-live point list changed")
    require(len({tuple(record["entry_support"])
                 for record in intersections}) == 1 and
            len({tuple(record["cofactor_support"])
                 for record in intersections}) == 1 and
            len({tuple(record["Q_support"])
                 for record in intersections}) == 1,
            "Q3=C6 point signatures ceased to agree")
    require(mined["active_aliases"] == EXPECTED_ALIASES,
            "Q3=C6 exact core labels changed")
    require(mined["ordinary_row_count"] == 8,
            "Q3=C6 exact core row count changed")
    lines = INPUT.read_text().splitlines()
    require(lines[1] == "0" and len(lines[0].split(",")) == 18,
            "Q3=C6 exact input header changed")
    require(len("\n".join(lines[2:]).split(",\n")) == 9,
            "Q3=C6 exact input row count changed")
    require(is_unit_basis(FROZEN_OUTPUT),
            "frozen Q3=C6 exact basis is not [1]")
    with tempfile.TemporaryDirectory(prefix="q3-c6-exact-referee-") as tmp:
        replay = Path(tmp) / "replay.gb.out"
        completed = subprocess.run(
            ["msolve", "-f", str(INPUT), "-o", str(replay), "-t", "4",
             "-g", "2", "-v", "0", "-l", "2"],
            capture_output=True, text=True, timeout=30, check=False)
        require(completed.returncode == 0 and is_unit_basis(replay),
                "Q3=C6 exact msolve replay failed")
        replay_sha = sha256(replay.read_bytes()).hexdigest()
    result = {
        "status": "UNAUDITED exact-Q Q3=C6 mate core UNIT audit PASS",
        "ordinary_rows": EXPECTED_ALIASES,
        "ordinary_row_count": 8,
        "mate_H_rabinowitsch": "u*H_mate-1",
        "exact_basis": "[1]",
        "literal_replay": True,
        "intersection_point_count": 2,
        "common_H_live_signature": True,
        "input_sha256": sha256(INPUT.read_bytes()).hexdigest(),
        "frozen_output_sha256": sha256(FROZEN_OUTPUT.read_bytes()).hexdigest(),
        "replay_output_sha256": replay_sha,
        "conclusion": (
            "Neither exact H-live Q3=C6 component point admits an H-live "
            "mate under the universal incidence consequences."
        ),
        "scope_guard": (
            "The polynomial unit is exact over Q for the common incidence "
            "signature derived at both algebraic intersection points. "
            "Transport to C10,C14,C18 uses the separately frozen exact "
            "component stabilizer."
        ),
        "source_hashes": {
            "miner": sha256(MINER.read_bytes()).hexdigest(),
            "mined": sha256(MINED.read_bytes()).hexdigest(),
            "signature": sha256(SIGNATURE.read_bytes()).hexdigest(),
        },
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print("Q3=C6 exact mate core audit PASS")
    print("result", result["result_sha256"])


if __name__ == "__main__":
    main()
