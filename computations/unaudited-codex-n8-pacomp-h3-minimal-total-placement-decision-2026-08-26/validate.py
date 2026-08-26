#!/usr/bin/env python3
"""Replay the finite exact decision and fail-closed interface; no solver."""
from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path

H = Path(__file__).resolve().parent


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


completed = subprocess.run([sys.executable, str(H / "verify_minimal_total_placement.py")], cwd=H, env={"PYTHONDONTWRITEBYTECODE": "1"}, text=True, capture_output=True, timeout=30)
assert completed.returncode == 0, completed.stderr
result = json.loads((H / "results_minimal_total_placement.json").read_text())
interface = json.loads((H / "minimal_total_placement_interface.json").read_text())
schema = json.loads((H / "source_interface.schema.json").read_text())
assert result["status"] == "PASS_NO_EXISTING_OR_ONE_BARE_SWITCH_CONSTRUCTION_MINIMAL_TWO_COMPONENT_INTERFACE"
assert result["source_provenance"]["implemented_primitives"] == 128 and result["source_provenance"]["registered_degree_zero_cross_operation_arrows"] == 0
assert result["top_exact_obstruction"]["boundary_rank"] == 3 and result["top_exact_obstruction"]["detector_value"] == 2
assert result["retained_exact_obstruction"]["boundary_rank"] == 3 and result["retained_exact_obstruction"]["detector_value"] == 1
assert result["minimum_theorem"] == {"after_both_missing_lines": 8, "after_either_missing_line": 7, "associated_graded_old_rank": 6, "bare_homogeneous_new_columns_required": 2, "one_bare_cross_operation_sufficient": False, "one_total_constructor_schema_possible_only_if": "it emits two nonzero filtration components and all their source labels; calling this one schema does not make it a one-column construction"}
assert result["scope"] == {"PAComp_promotion": False, "conjecture_promotion": False, "h": 3, "new_physical_constructor_added": False, "pinned_executable_source_only": True, "solves": 0, "uniform_descent_promotion": False}


def check(value, rule):
    assert set(value) == set(rule["required"])
    for key, specification in rule["properties"].items():
        if "const" in specification:
            assert value[key] == specification["const"]
        if specification.get("type") == "object":
            check(value[key], specification)


check(interface, schema)
hostiles = []
mutations = [
    ("extra", "x"),
    ("new_physical_constructor_registered", True),
    ("instances", ["AB/q23"]),
    ("outputs", interface["outputs"][:1]),
    ("required_face_checks", interface["required_face_checks"][:-1]),
    ("status", "CONSTRUCTED"),
    ("acceptance", {**interface["acceptance"], "extra_descendants_allowed": True}),
    ("symmetry", {**interface["symmetry"], "tau": "equivariant"}),
]
for name, replacement in mutations:
    candidate = copy.deepcopy(interface)
    candidate[name] = replacement
    rejected = False
    try:
        check(candidate, schema)
    except (AssertionError, KeyError, TypeError):
        rejected = True
    assert rejected, name
    hostiles.append({"mutation": name, "status": "PASS_REJECTED"})
(H / "results_hostiles.json").write_text(json.dumps({"status": "PASS_ALL_8_HOSTILES", "tests": hostiles, "solves": 0}, indent=2, sort_keys=True) + "\n")
assert not list(H.glob("*.tmp")) and not list(H.rglob("__pycache__"))
if (H / "MANIFEST.sha256").exists():
    for line in (H / "MANIFEST.sha256").read_text().splitlines():
        digest, name = line.split(None, 1)
        path = H / name.strip()
        assert path.is_file() and sha(path) == digest
print(json.dumps({"status": "PASS_REFEREE_READY_MINIMAL_TOTAL_PLACEMENT_DECISION", "physical_construction": False, "interface_components": 2, "instances": 4, "hostiles": 8, "solves": 0}, sort_keys=True))
