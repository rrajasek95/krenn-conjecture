#!/usr/bin/env python3
"""Fail-closed validator for the rep2 F2-core/Q-countermodel package."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PINS = {
    ROOT / "computations/unaudited-codex-n8-x5-seven-block-rep2-incidence-gate-2026-08-25/MANIFEST.sha256":
        "4539834523323399bf969703aef09dc18e578d5c2e0800d592144f048b14c4f5",
    ROOT / "computations/unaudited-codex-n8-x5-seven-block-rank1-incidence-gate-2026-08-25/generate_rank1_gate.py":
        "1fc2a1a62e4092f75cbb330009bbb9649e83e559167f251217a26b7eb3bc7c14",
    Path("/opt/homebrew/bin/z3"):
        "537a502af2f4013a8e887beebe525a0dae84918a61ff545991e36dfda07ed6d7",
    Path("/usr/local/bin/Singular"):
        "9436b32ff7565719240230de8a6fb1d27af5e65f0ca4c9c5b756a77e82409b88",
}


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def load(name):
    path = HERE / name
    spec = importlib.util.spec_from_file_location(path.stem, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    assert __debug__
    for path, digest in PINS.items():
        assert sha256(path) == digest, path
    search = load("search_pair01_f2.py")
    audit = load("audit_tensor_core.py")
    equations, labels = search.constraints()
    core = json.loads((HERE / "results_f2_core43.json").read_text())
    names = [f"amp_{word}" for word in core["amplitude_words"]]
    selected = [equations[labels.index(name)] for name in names]
    variables = (
        list(search.SOURCE.values()) + list(search.U) + list(search.V)
        + [item for name in "xyz" for item in search.DUAL[name]]
        + list(search.RHO) + list(search.SIGMA) + [search.TAU]
    )

    def solve(items, timeout=5):
        lines = [f"(declare-const {variable} Bool)" for variable in variables]
        lines.extend(f"(assert (not {equation}))" for equation in items)
        lines.append("(check-sat)")
        process = subprocess.run(
            ["z3", f"-T:{timeout}", "-in"], input="\n".join(lines) + "\n",
            capture_output=True, text=True, timeout=timeout + 2,
        )
        status = next(
            line for line in process.stdout.splitlines() if line in {"sat", "unsat", "unknown"}
        )
        return process.returncode, status

    # Positive proof replay and all 43 deletion hostiles.
    process = subprocess.run(
        ["z3", str(HERE / core["proof_input"])], capture_output=True, text=True,
        timeout=30,
    )
    assert process.returncode == 0 and process.stdout.splitlines()[0] == "unsat"
    assert solve(selected) == (0, "unsat")
    deletion_statuses = []
    for index in range(len(selected)):
        status = solve(selected[:index] + selected[index + 1 :])
        assert status == (0, "sat")
        deletion_statuses.append(status[1])

    result = json.loads((HERE / "results_tensor_core_audit.json").read_text())
    assert result["status"] == "PASS_F2_ONLY_OBSTRUCTION_AND_EXACT_Q_COUNTERMODEL_TO_CORE_LIFT"
    qpoint = {
        name: audit.Fraction(value)
        for name, value in result["rational_lift_test"]["point"].items()
    }
    qres = []
    for raw in core["amplitude_words"]:
        word = tuple(map(int, raw))
        qres.append(audit.amplitude(word, qpoint) - int(word == (0,) * 8))
    assert not any(qres)

    # Hostile 1: changing the sole half coordinate breaks literal replay.
    hostile_point = dict(qpoint)
    hostile_point["a06_10"] = audit.Fraction(-1)
    hostile_residuals = []
    for raw in core["amplitude_words"]:
        word = tuple(map(int, raw))
        hostile_residuals.append(audit.amplitude(word, hostile_point) - int(word == (0,) * 8))
    assert any(hostile_residuals)
    # Hostile 2: the Q point is not a full pair01 countermodel.
    assert result["rational_lift_test"]["other_pair01_violation_count"] == 13
    # Hostile 3: it is illegal to reduce a denominator 2 point to characteristic 2.
    assert qpoint["a06_10"].denominator == 2
    # Hostile 4: no guard/incidence/rank equation may be smuggled into the core.
    assert all(name.startswith("amp_") for name in names)
    # Hostile 5: simple flattening upper bounds do not establish an obstruction.
    assert result["flattening_census"]["best_binary_sum_rank_bound"] == 21 > 2
    assert result["flattening_census"]["best_ternary_sum_rank_bound"] == 29 > 3

    qrun = json.loads((HERE / "results_core43_q_chart.json").read_text())
    assert qrun["status"] == "PASS_TERMINAL_NONUNIT" and qrun["unit_remainder"] == "1"
    f3run = json.loads((HERE / "results_core43_f3.json").read_text())
    assert f3run["status"] == "sat"
    validation = {
        "schema": "KRENN_X5_REP2_TENSOR_CORE43_VALIDATION_V1",
        "status": "PASS",
        "pins": {str(path): digest for path, digest in PINS.items()},
        "positive_checks": {
            "z3_proof_replay": "unsat",
            "core_direct_replay": "unsat",
            "deletion_sat_count": deletion_statuses.count("sat"),
            "f3_literal_model": "PASS",
            "q_literal_point": "PASS_43_OF_43",
            "q_singular_chart": "NONUNIT",
        },
        "hostile_checks": 5,
        "scope": result["scope"],
    }
    path = HERE / "results_validation.json"
    temporary = path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(validation, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)
    print(json.dumps({
        "status": validation["status"],
        "deletion_sat": deletion_statuses.count("sat"),
        "hostiles": validation["hostile_checks"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
