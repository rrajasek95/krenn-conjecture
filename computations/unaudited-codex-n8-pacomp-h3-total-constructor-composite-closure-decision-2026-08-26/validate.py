#!/usr/bin/env python3
"""Replay the composite closure and hostile-test the primitive contract."""
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


completed = subprocess.run([sys.executable, str(H / "audit_composite_closure.py")], cwd=H, env={"PYTHONDONTWRITEBYTECODE": "1"}, capture_output=True, text=True, timeout=30)
assert completed.returncode == 0, completed.stderr
result = json.loads((H / "results_composite_closure_decision.json").read_text())
contract = json.loads((H / "primitive_completion_contract.json").read_text())
schema = json.loads((H / "primitive_completion_contract.schema.json").read_text())
assert result["status"] == "PASS_NO_COMPOSITE_CONSTRUCTOR_PRIMITIVE_TWO_COMPONENT_DECISION_IS_MINIMAL"
assert result["source_derived_closure"]["actual_atoms"] == 128 and result["source_derived_closure"]["operation_changing_atoms"] == 0
assert result["source_derived_closure"]["composable_word_counts_length_1_to_4"] == {"1": 128, "2": 10678, "3": 1017578, "4": 100456978}
assert result["mapping_cylinder"]["standard_interchange_rank"] == 8 and result["mapping_cylinder"]["standard_interchange_detector_signature"] == [0, 0]
assert result["actual_constructor_search"] == {"Lambda01_Pi_pair_found": False, "existing_candidate_records": 0, "known_underived_or_Tate_commutators": "objectwise or without physical descent/Gamma projection", "smallest_unexcluded_sort": "primitive Hom^1_Gamma(response,cap) modulo eight standard interchanges"}
assert len(result["finite_source_decision"]["boundary_equations"]) == 12 and len(result["finite_source_decision"]["coherence_equations"]) == 8 and len(result["finite_source_decision"]["face_exactness"]) == 5
assert result["scope"] == {"PAComp_promotion": False, "actual_callable_and_source_derived_free_closure": True, "conjecture_promotion": False, "heavy_solver_runs": 0, "new_constructor_added": False, "uniform_descent_promotion": False, "unwritten_full_physical_complex_classified": False, "h": 3}


def check(value, rule):
    assert set(value) == set(rule["required"])
    for key, specification in rule["properties"].items():
        if "const" in specification:
            assert value[key] == specification["const"]
        if specification.get("type") == "object":
            check(value[key], specification)


check(contract, schema)
mutations = [
    ("extra", True),
    ("status", "CLOSED"),
    ("required_operation_sort", "Hom0"),
    ("unknown_records", ["Lambda_01"]),
    ("instances", contract["instances"][:-1]),
    ("detector_signature_matrix", [[2, 1]]),
    ("candidate_source_records", ["fabricated"]),
    ("acceptance", {**contract["acceptance"], "extra_faces_allowed": True}),
    ("acceptance", {**contract["acceptance"], "coherence_equations_required": 7}),
    ("acceptance", {**contract["acceptance"], "literal_source_provenance_required": False}),
]
hostiles = []
for index, (field, value) in enumerate(mutations):
    candidate = copy.deepcopy(contract)
    candidate[field] = value
    rejected = False
    try:
        check(candidate, schema)
    except (AssertionError, KeyError, TypeError):
        rejected = True
    assert rejected, (index, field)
    hostiles.append({"id": index, "field": field, "status": "PASS_REJECTED"})
(H / "results_hostiles.json").write_text(json.dumps({"status": "PASS_ALL_10_HOSTILES", "tests": hostiles, "heavy_solver_runs": 0}, indent=2, sort_keys=True) + "\n")
assert not list(H.glob("*.tmp")) and not list(H.rglob("__pycache__"))
if (H / "MANIFEST.sha256").exists():
    for line in (H / "MANIFEST.sha256").read_text().splitlines():
        digest, name = line.split(None, 1)
        path = H / name.strip()
        assert path.is_file() and sha(path) == digest
print(json.dumps({"status": "PASS_REFEREE_READY_COMPOSITE_CLOSURE_DECISION", "actual_candidates": 0, "boundary_equations": 12, "coherence_equations": 8, "hostiles": 10, "heavy_solver_runs": 0}, sort_keys=True))
