#!/usr/bin/env python3
"""Independent six-chart replay and scope validation."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DESIGN = ROOT / "computations/unaudited-codex-n8-x5-rep2-sparse-pair01-quadruple-hitting-design-2026-08-25"


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    result = json.loads((HERE / "results_size7.json").read_text())
    design = json.loads((DESIGN / "hitting_support_ledger.json").read_text())
    assert result["status"] == "PASS_ALL_SIX_UNIT"
    assert result["unit_count"] == 6 and result["nonunit_count"] == result["failure_count"] == 0
    assert [item["support"] for item in result["attempts"]] == design["minimum_fixed_base_hitting_supports"]
    assert result["scope"]["base_coordinates_movable"] is True
    assert result["scope"]["fixed_base_hitting_theorem_used_as_filter"] is False
    replays = []
    for item in result["attempts"]:
        source = HERE / item["input"]
        assert sha256(source) == item["input_sha256"]
        assert sha256(HERE / item["stdout"]) == item["stdout_sha256"]
        process = subprocess.run(
            ["gtimeout", "10", "Singular", str(source)], capture_output=True,
            text=True, timeout=12,
        )
        stdout = process.stdout + process.stderr
        assert process.returncode == 0 and "STATUS=UNIT_IDEAL" in stdout
        assert "UNIT_REMAINDER=0" in stdout and "STATUS=NONUNIT" not in stdout
        replays.append("UNIT_IDEAL")
    validation = {
        "schema": "KRENN_X5_REP2_SIZE7_HEURISTIC_VALIDATION_V1",
        "status": "PASS",
        "result_sha256": sha256(HERE / "results_size7.json"),
        "independent_unit_replays": len(replays),
        "scope_hostiles": [
            "six supports only",
            "movable base is not fixed-base hitting theorem",
            "no guard/adjoint/incidence conclusion",
        ],
    }
    output = HERE / "results_validation.json"
    temporary = output.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(validation, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, output)
    print(json.dumps(validation, sort_keys=True))


if __name__ == "__main__":
    main()
