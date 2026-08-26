#!/usr/bin/env python3
"""Fail-closed static validator for the rank-1/rank-2 design inputs."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULT = HERE / "results_rank12_incidence_design.json"


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


result = json.loads(RESULT.read_text())
assert result["schema"] == "KRENN_X5_RECTANGLE_4647_RANK12_INCIDENCE_IDEAL_DESIGN_V1"
assert result["status"] == "PASS_EXACT_MATERIALIZATION_NO_SOLVE"
assert result["scope"] == {"inputs_materialized": 10, "solver_launches": 0, "records_closed": 0}
assert result["chart_census"] == {"raw_per_rank": 27, "S3_orbits_per_rank": 5, "canonical_inputs": 10}
assert result["counts"]["rank1"] == {"variables": 76, "generators": 6571, "canonical_inputs": 5}
assert result["counts"]["rank2"] == {"variables": 80, "generators": 6574, "canonical_inputs": 5}
assert len(result["canonical_inputs"]) == 10
assert sum(group["size"] for group in result["orbit_ledgers"]["rank1"]) == 27
assert sum(group["size"] for group in result["orbit_ledgers"]["rank2"]) == 27

seen = set()
for record in result["canonical_inputs"]:
    key = (record["rank"], record["orbit_index"])
    assert key not in seen
    seen.add(key)
    path = HERE / record["path"]
    source = path.read_text()
    assert sha256(path) == record["sha256"]
    assert path.stat().st_size == record["bytes"]
    assert "slimgb" not in source and "std(" not in source and "groebner" not in source.lower()
    assert source.startswith("// DESIGN INPUT ONLY") and source.rstrip().endswith("quit;")
    ring_line = next(line for line in source.splitlines() if line.startswith("ring r="))
    variables = ring_line.split("(", 1)[1].rsplit(")", 1)[0].split(",")
    assert variables == record["variable_order"]
    assert len(variables) == record["variables"]
    ideal_text = source.split("ideal I=", 1)[1].split(";", 1)[0]
    assert len(ideal_text.split(",\n")) == record["generators"]

assert seen == {(rank, orbit) for rank in (1, 2) for orbit in range(5)}
assert all(result["hostile_tests"].values())
print(json.dumps({"status": "PASS_STATIC_NO_SOLVE", "inputs": 10, "result_sha256": sha256(RESULT)}, sort_keys=True))
