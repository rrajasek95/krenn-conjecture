#!/usr/bin/env python3
"""Replay the selected-chart reduction design without invoking Singular."""
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
SOURCE = ROOT / "computations/unaudited-codex-n8-x5-rep5-k2-t1-open84-torus-cover-design-2026-08-26/sources/rep5_k2_t1_gauge_yn11_yn21_t01_t20_Q_design.sing"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


assert sha(SOURCE) == "13c204f73bb82e263267ec977c19a10dba045541921375c2e7568ba48d5baba0"
result = json.loads((HERE / "results_design.json").read_text())
assert result["status"] == "PASS_EXACT_TWO_CHART_RESIDUAL_ONE_TORUS_COVER"
assert result["grading"]["rank"] == 72 and result["grading"]["nullity"] == 1
assert result["grading"]["nonzero_weights"] == [{"a04_20": 1, "a04_21": 1, "a04_22": 1, "a35_21": -1, "a35_22": -1, "a37_20": -1}]
cover = result["residual_torus_cover"]
assert cover["identity"] == "D(q) union V(q)" and cover["root_free"] is True
assert (cover["selected_coordinate"], cover["selected_weight"]) == ("a37_20", -1)
assert len(cover["candidate_ledger"]) == 6 and len(cover["sources"]) == 2
for source in cover["sources"]:
    path = HERE / source["path"]
    assert path.is_file() and sha(path) == source["sha256"]
    text = path.read_text()
    assert "ring r=0,(" in text and "a37_20" not in text.split("ring r=0,(", 1)[1]
    variables = text.split("ring r=0,(", 1)[1].split("),dp;", 1)[0].split(",")
    body = text.split("ideal I=", 1)[1].split(';\nprint("INPUT_VARIABLES=', 1)[0]
    depth = 0
    generators = 1
    for character in body:
        if character == "(": depth += 1
        elif character == ")": depth -= 1
        elif character == "," and depth == 0: generators += 1
    assert depth == 0 and len(variables) == source["variables"] == 72 and generators == source["generators"] == 6561
    assert source["inactive"] == [] and source["monic_graph_substitutions"] == []
assert [source["grading_nullity_over_Q"] for source in cover["sources"]] == [0, 1]
assert result["linear_reduction"]["amplitude_inactive_coordinates"] == []
assert result["linear_reduction"]["unit_coefficient_graph_substitutions"] == []
assert result["block_structure"]["component_sizes"] == [73]
tree = ast.parse((HERE / "analyze.py").read_text())
assert not any(isinstance(node, (ast.Import, ast.ImportFrom)) and any(alias.name == "subprocess" for alias in node.names) for node in ast.walk(tree))
attempt = subprocess.run([sys.executable, str(HERE / "test_design.py")], cwd=HERE, capture_output=True, text=True, timeout=15, check=True, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
hostiles = json.loads((HERE / "results_hostiles.json").read_text())
assert hostiles["status"] == "PASS" and hostiles["hostile_count"] == 12 and hostiles["solver_runs"] == 0
assert not list(HERE.glob("*.tmp")) and not list(HERE.rglob("__pycache__"))
print(json.dumps({"status": "PASS_EXACT_TWO_CHART_DESIGN_REPLAY", "charts": 2, "hostiles": 12, "solver_runs": 0}, sort_keys=True))
