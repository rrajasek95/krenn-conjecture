#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PARENT = ROOT / "computations/unaudited-codex-n8-x5-rep2-group16-a57V0-a04_11-residual-split-design-2026-08-26"
SOURCE = PARENT / "sources/rep2_group16_Dt1_a04_11_V0_Q_design.sing"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


record = json.loads((HERE / "results_design.json").read_text())
assert sha(PARENT / "MANIFEST.sha256") == record["original_parent_binding"]["manifest_sha256"] == "8c4b3e4c82076e7cd8b61cd40e86eaa8a8ea3bd10ace7c1f8ac7f8c4ce52b835"
assert sha(SOURCE) == record["original_parent_binding"]["source_sha256"] == "f0bae713992e827d827fd3d6998710cb8e602a607f19ee379d775ee0032294ea"
assert SOURCE.read_text().split(";\nprint(\"INPUT_VARIABLES=", 1)[0].rsplit(",\n", 1)[1] == "-1-a26_00-a26_02*a57_02"
graph = record["graph_elimination"]
intermediate = HERE / graph["intermediate_path"]
assert sha(intermediate) == graph["intermediate_sha256"] == "ed89147490a0f80d4f8d7aa67e025b6fd0cc6b6b6186db1457b0f2464c38a743"
intermediate_text = intermediate.read_text()
intermediate_variables = intermediate_text.split("ring r=0,(", 1)[1].split("),dp;", 1)[0].split(",")
assert len(intermediate_variables) == 58 and "a26_00" not in intermediate_variables
assert record["source"]["variables"] == 58 and record["source"]["generators"] == 6063
assert record["source"]["sha256"] == sha(intermediate)
expected = {
    "D1": ("f58bc59a586de9eb01a980f41cd54b762fe6d232583a84a3e6e7d3be1496a0be", 57, 1, 1, True),
    "V0": ("53cebaf3d4a6b85d9058374423e91bd02da0c4a6e8c5b70d09c661c27b297535", 57, 6015, 111546, False),
}
for source in record["cover"]["sources"]:
    expected_sha, variables, generators, terms, unit = expected[source["branch"]]
    path = HERE / source["path"]
    assert sha(path) == source["sha256"] == expected_sha
    assert (source["variables"], source["generators"], source["total_terms"], source["unit_ideal_structural"]) == (variables, generators, terms, unit)
    text = path.read_text()
    assert "slimgb" not in text and "reduce(" not in text
    if unit:
        assert text.split("ideal I=", 1)[1].split(";\nprint", 1)[0] == "1"
subprocess.run(
    [sys.executable, str(HERE / "test_design.py")],
    cwd=HERE,
    env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    capture_output=True,
    text=True,
    check=True,
    timeout=20,
)
hostiles = json.loads((HERE / "results_hostiles.json").read_text())
assert hostiles["status"] == "PASS" and hostiles["hostile_count"] == 17 and hostiles["solver_runs"] == 0
assert not list(HERE.glob("*.tmp")) and not list(HERE.rglob("__pycache__"))
print(json.dumps({
    "status": "PASS_EXACT_MONIC_ELIMINATION_AND_FORCED_ZERO_REPLAY",
    "graph": graph["substitution"],
    "forced_zero": record["global_cover_update"]["forced_zero"],
    "nonempty_source": [57, 6015, 111546],
    "hostiles": 17,
    "solver_runs": 0,
}, sort_keys=True))
