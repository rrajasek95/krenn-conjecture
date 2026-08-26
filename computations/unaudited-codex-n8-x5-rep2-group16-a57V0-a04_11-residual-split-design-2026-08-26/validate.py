#!/usr/bin/env python3
"""Independent small-file replay of the residual a04_11 split design."""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PARENT = ROOT / "computations/unaudited-codex-n8-x5-rep2-group16-Vt1Vt2Dt0-residual-torus-design-2026-08-26"
TEMPLATE = ROOT / "computations/unaudited-codex-n8-x5-rep2-group16-Dt1-timeout-reduction-design-2026-08-26"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


record = json.loads((HERE / "results_design.json").read_text())
assert record["status"] == "PASS_EXACT_PRIMITIVE_TORUS_DV_COVER"
assert sha(PARENT / "MANIFEST.sha256") == record["parent_binding"]["manifest_sha256"] == "0b355f51e249d82b8a1aea45687a8a6b6ebaab83fd5256e541d9acf7985d1bba"
parent_source = PARENT / "sources/rep2_group16_Dt1_a57_01_V0_Q_design.sing"
assert sha(parent_source) == record["source"]["sha256"] == "15ee90435e4f6148c708525b757de4f8b6ff9a1aba0a66fc2402b8846ffb964c"
assert sha(TEMPLATE / "MANIFEST.sha256") == "aab19d2f51693fed67f587d83fe0d2e108888d626d788e4d00a9362a3be978be"
assert record["source"]["variables"] == 60 and record["source"]["generators"] == 6568
assert record["grading"]["rank"] == 56 and record["grading"]["nullity"] == 4
assert record["factor_census"] == {
    "coordinate": "a04_11",
    "source_generators": 6568,
    "source_generators_divisible_by_coordinate": 504,
}
expected = {
    "D1": ("2998353c04d390b7dadae6a2bb364d5ad9866b1911d39dfb9f039b40cef70bab", 59, 6568, 174407),
    "V0": ("f0bae713992e827d827fd3d6998710cb8e602a607f19ee379d775ee0032294ea", 59, 6064, 157829),
}
for source in record["cover"]["sources"]:
    expected_sha, variables, generators, terms = expected[source["branch"]]
    path = HERE / source["path"]
    assert sha(path) == source["sha256"] == expected_sha
    assert (source["variables"], source["generators"], source["total_terms"]) == (variables, generators, terms)
    text = path.read_text()
    names = text.split("ring r=0,(", 1)[1].split("),dp;", 1)[0].split(",")
    body = text.split("ideal I=", 1)[1].split(';\nprint("INPUT_VARIABLES=', 1)[0]
    depth = 0
    counted = 1
    for character in body:
        if character == "(":
            depth += 1
        elif character == ")":
            depth -= 1
        elif character == "," and depth == 0:
            counted += 1
    assert depth == 0 and len(names) == variables and counted == generators
    assert "a04_11" not in names
    assert "slimgb" not in text and "reduce(" not in text

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
assert hostiles["status"] == "PASS" and hostiles["hostile_count"] == 14 and hostiles["solver_runs"] == 0
assert record["global_cover_update"]["exhaustive"] is True
assert record["conclusion"]["singular_runs"] == 0 and record["conclusion"]["mathematical_coverage"] is False
assert not list(HERE.glob("*.tmp")) and not list(HERE.rglob("__pycache__"))
print(json.dumps({
    "status": "PASS_EXACT_A57V0_A04_11_RESIDUAL_SPLIT_REPLAY",
    "source_shapes": [[source["variables"], source["generators"], source["total_terms"]] for source in record["cover"]["sources"]],
    "hostiles": 14,
    "solver_runs": 0,
}, sort_keys=True))
