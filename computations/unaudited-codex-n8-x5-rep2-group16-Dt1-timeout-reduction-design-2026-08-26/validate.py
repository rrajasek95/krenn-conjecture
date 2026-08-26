#!/usr/bin/env python3
"""Static replay of the exact rep2 D(t1) timeout reduction."""
from __future__ import annotations

import ast
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
UPSTREAM = ROOT / "computations/unaudited-codex-n8-x5-rep2-group16-tcover-complement3-exact-q-held-2026-08-26"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


result = json.loads((HERE / "results_design.json").read_text())
assert result["status"] == "PASS_EXACT_MAXIMAL_GLOBAL_UNIT_TORUS_GAUGE"
assert result["source"]["sha256"] == sha(UPSTREAM / "sources/rep2_group016_67_Dt1_runtime_Q.sing") == "f0212ca6edfec2941b68a0161d8a4f81c9455f3729d94150e16eafb057043244"
assert result["timeout_binding"]["result_sha256"] == sha(UPSTREAM / "results/lane2_Dt1.json") == "b4656dd9e74e31b38a63af40404e8b0d0291f5a5d31e471dde104ab59d2e0c8f"
assert result["timeout_binding"]["terminal_manifest_sha256"] == sha(UPSTREAM / "TERMINAL_MANIFEST.sha256") == "5d9fdcbfea5aab0245ffde35ab62b4ab3626c99d8b88d09b5a8554ae8bd49551"
assert result["grading"]["rank"] == 58 and result["grading"]["nullity"] == 6
cover = result["cover"]
assert cover["maximal_primitive_global_gauge_coordinates"] == ["it1", "sat"]
assert cover["maximal_primitive_global_gauge_weight_rows"] == [[0, 0, 0, 0, 0, -1], [0, 0, 0, 0, 1, 0]]
assert cover["global_gauge_assignments_including_inverse_partners"] == {"it1": 1, "sat": 1, "t1": 1}
assert cover["global_unit_witnesses"]["sat"]["equation_indices"] == [6567]
assert set(cover["global_unit_witnesses"]) == {"it1", "sat", "t1"}
assert len(cover["sources"]) == 1
source = cover["sources"][0]
path = HERE / source["path"]
assert path.is_file() and sha(path) == source["sha256"] == "32707a25c384ea038790e393e18654e3e41a34f59aa4303bc4eb74115d073e37"
text = path.read_text()
variables = text.split("ring r=0,(", 1)[1].split("),dp;", 1)[0].split(",")
body = text.split("ideal I=", 1)[1].split(';\nprint("INPUT_VARIABLES=', 1)[0]
depth = 0
generators = 1
for character in body:
    if character == "(":
        depth += 1
    elif character == ")":
        depth -= 1
    elif character == "," and depth == 0:
        generators += 1
assert depth == 0 and len(variables) == source["variables"] == 61 and generators == source["generators"] == 6568
assert not ({"it1", "sat", "t1"} & set(variables))
assert source["total_terms"] == 244567 and source["inactive"] == []
tree = ast.parse((HERE / "analyze.py").read_text())
assert not any(isinstance(node, (ast.Import, ast.ImportFrom)) and any(alias.name == "subprocess" for alias in node.names) for node in ast.walk(tree))
subprocess.run([sys.executable, str(HERE / "test_design.py")], cwd=HERE, capture_output=True, text=True, timeout=15, check=True, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
hostiles = json.loads((HERE / "results_hostiles.json").read_text())
assert hostiles["status"] == "PASS" and hostiles["hostile_count"] == 12 and hostiles["solver_runs"] == 0
assert result["conclusion"] == {"mathematical_coverage": False, "old_chart_relaunch": False, "old_timeout_consumed": True, "singular_runs": 0}
assert not list(HERE.glob("*.tmp")) and not list(HERE.rglob("__pycache__"))
print(json.dumps({"status": "PASS_EXACT_GLOBAL_UNIT_GAUGE_REPLAY", "shape": [61, 6568], "hostiles": 12, "solver_runs": 0}, sort_keys=True))
