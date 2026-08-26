#!/usr/bin/env python3
"""Replay the Q ansatz, its Farkas witnesses, controls, and hostiles."""
from __future__ import annotations

import copy
from fractions import Fraction as Q
import hashlib
import json
import subprocess
import sys
from pathlib import Path

H = Path(__file__).resolve().parent


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dot(left, right):
    return sum((Q(a) * Q(b) for a, b in zip(left, right, strict=True)), Q(0))


completed = subprocess.run([sys.executable, str(H / "solve_coefficient_ansatz.py")], cwd=H, env={"PYTHONDONTWRITEBYTECODE": "1"}, capture_output=True, text=True, timeout=10)
assert completed.returncode == 0, completed.stderr
result = json.loads((H / "results_coefficient_ansatz.json").read_text())
certificate = json.loads((H / "farkas_certificate.json").read_text())
schema = json.loads((H / "farkas_certificate.schema.json").read_text())
assert result["status"] == "PASS_EXACT_Q_INCONSISTENT_FARKAS_CERTIFICATE_FOR_MAXIMAL_PINNED_ANSATZ"
assert result["ansatz"]["total_variables_before_coherence"] == 56 and result["ansatz"]["variables_per_instance"] == 14
assert result["system"]["polynomial_degree"] == 1 and result["system"]["boundary_vector_equation_count"] == 12 and result["system"]["expanded_boundary_scalar_equation_count"] == 20
assert result["system"]["coherence_equation_count"] == 8 and result["system"]["face_check_count"] == 5
assert result["solution"] == {"exists": False, "failure_before_coherence": True, "failure_before_face_checks": True, "valid_Lambda_formula": None, "valid_Pi_formula": None}
assert result["positive_control"]["status"] == "PASS_FORMAL_FREE_EXTENSION_ONLY" and result["positive_control"]["coefficients"] == {"Lambda_retained": 1, "Lambda_top": 1, "Pi_retained": -1}
assert result["scope"] == {"PAComp_promotion": False, "conjecture_promotion": False, "h": 3, "heavy_external_solver_runs": 0, "maximal_pinned_and_formally_granted_switch_ansatz": True, "uniform_descent_promotion": False, "unregistered_primitive_Hom1_excluded": False}
assert set(certificate) == set(schema["required"]) == set(schema["properties"])
for key, rule in schema["properties"].items():
    if "const" in rule:
        assert certificate[key] == rule["const"]
top_columns = tuple(zip(*certificate["top_matrix_rows"], strict=True))
top_witness = certificate["certificates"]["top"]["left_witness"]
assert all(dot(top_witness, column) == 0 for column in top_columns) and dot(top_witness, certificate["top_rhs"]) == 2
retained_columns = tuple(zip(*certificate["retained_matrix_rows"], strict=True))
retained_witness = certificate["certificates"]["lambda_retained"]["left_witness"]
assert all(dot(retained_witness, column) == 0 for column in retained_columns)
assert dot(retained_witness, certificate["lambda_retained_rhs"]) == 1 and dot(retained_witness, certificate["pi_retained_rhs"]) == -1

hostile_specs = [
    ("top_rhs", ["0", "0", "0"]),
    ("top_matrix_rows", [["1", "0", "0", "0", "1", "1"], ["0"] * 6, ["0"] * 6]),
    ("retained_matrix_rows", [["1", "0", "0", "0"]]),
    ("lambda_retained_rhs", ["0"]),
    ("pi_retained_rhs", ["0"]),
    ("field", "F_2"),
    ("status", "UNIT"),
    ("schema", "wrong"),
    ("extra", True),
    ("certificates", {}),
]
hostiles = []
for index, (field, value) in enumerate(hostile_specs):
    candidate = copy.deepcopy(certificate)
    candidate[field] = value
    rejected = False
    try:
        assert set(candidate) == set(schema["required"])
        for key, rule in schema["properties"].items():
            if "const" in rule:
                assert candidate[key] == rule["const"]
        top = tuple(zip(*candidate["top_matrix_rows"], strict=True))
        witness = candidate["certificates"]["top"]["left_witness"]
        assert all(dot(witness, column) == 0 for column in top) and dot(witness, candidate["top_rhs"]) != 0
        retained = tuple(zip(*candidate["retained_matrix_rows"], strict=True))
        witness_r = candidate["certificates"]["lambda_retained"]["left_witness"]
        assert all(dot(witness_r, column) == 0 for column in retained) and dot(witness_r, candidate["lambda_retained_rhs"]) != 0 and dot(witness_r, candidate["pi_retained_rhs"]) != 0
    except (AssertionError, KeyError, TypeError, ValueError):
        rejected = True
    assert rejected, (index, field)
    hostiles.append({"id": index, "mutation": field, "status": "PASS_REJECTED"})
(H / "results_hostiles.json").write_text(json.dumps({"status": "PASS_ALL_10_HOSTILES", "tests": hostiles, "heavy_external_solver_runs": 0}, indent=2, sort_keys=True) + "\n")
assert not list(H.glob("*.tmp")) and not list(H.rglob("__pycache__"))
if (H / "MANIFEST.sha256").exists():
    for line in (H / "MANIFEST.sha256").read_text().splitlines():
        digest, name = line.split(None, 1)
        path = H / name.strip()
        assert path.is_file() and sha(path) == digest
print(json.dumps({"status": "PASS_REFEREE_READY_Q_FARKAS_NO_GO", "variables": 56, "boundary_vector_equations": 12, "coherence_equations": 8, "face_checks": 5, "hostiles": 10, "heavy_external_solver_runs": 0}, sort_keys=True))
