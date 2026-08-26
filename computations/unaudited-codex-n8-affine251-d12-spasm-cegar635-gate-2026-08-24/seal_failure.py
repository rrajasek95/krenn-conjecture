#!/usr/bin/env python3
"""Seal the fail-closed round-635 SpaSM gate; performs no solver/export run."""

from __future__ import annotations

import copy
import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
PORTFOLIO = ROOT / "computations/unaudited-codex-n8-affine251-d12-portfolio-gate-2026-08-24"
PRIME = 1_073_741_827
PINS = {
    PORTFOLIO / "tree635_checkpoint.bin": "761804372a3f7e12b1915dd2718f7f69ef00b799dc6f90cd083b2fa7d2fc3c88",
    PORTFOLIO / "tree635_vectors.bin": "dd74d7392a005fb9c7726d9a0cc5c86e5b16d987bcb707d1c3a0f90e6e4d9e40",
    PORTFOLIO / "results_tree_round635.json": "f0441129b01ad8c2af9ae90ed2c02834ddd35dbb3d11f4e26081cdd41e215702",
    ROOT / "computations/unaudited-codex-n8-affine251-orbit-membership-2026-08-24/src/main.rs":
        "241ffd55f4f403d28d06f2e5dda3be1040e5c77675c9d05e2a7b70fc81ed36a0",
    HERE / "src/main.rs": "dbcb02373f8c82586af06ac5f87e20ce6f1935d3709caf7934abb2d03757e622",
    HERE / "target/release/cegar635_spasm_bridge":
        "76d52f1bb42e0c445e996bb0316eb6eab7f202c3424c5ef89d1c04acd6170b51",
    ROOT / "computations/toolkit/vendor/spasm/tools/solve.c":
        "c06d07ff6a311b88721c13ab10ca8aececb07f4f7eed07118d58e96214909758",
    ROOT / "computations/toolkit/vendor/spasm-build-x86/tools/solve":
        "c7991174857aa1ee77c6d125c33fed7e71d9353e7606d068230708da9602ff18",
}


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            h.update(block)
    return h.hexdigest()


def validate(report: dict) -> None:
    assert report["schema"] == "KRENN_AFFINE251_D12_CEGAR635_SPASM_GATE_FAILURE_V1"
    assert report["status"] == "GATE_FAILED_WALL_NO_SOLUTION"
    assert report["scope"] == {"degree": 12, "round": 635, "prime": PRIME,
                               "second_prime_run": False, "full_closure_run": False}
    assert report["equivalence_accepted"] is False
    assert report["promotion"] == "DO_NOT_PROMOTE"
    assert report["solution_artifacts"] == [] and report["rank_available"] is False
    assert report["warm_solve_run"] is False
    export = report["export"]
    assert export["status"] == "PASS" and export["equations_cached_columns"] == 222_676
    assert export["variables_excluding_target"] == 14_814_561
    assert export["matrix_nnz"] == 22_539_255 and export["rhs_nnz"] == 2
    assert export["retained_tree_candidate_verified_all_columns"] is True
    assert report["matrix_sha256"] == sha(HERE / "matrix_cegar635_left_orientation.sms")
    assert report["rhs_sha256"] == sha(HERE / "rhs_cegar635_minus_target.sms")
    assert report["cold_diagnostic"]["last_schur_row"] < report["cold_diagnostic"]["schur_rows"]
    assert report["cold_diagnostic"]["solver_killed_at_end_to_end_wall"] is True
    assert report["comparison"]["rust_tree_solve_seconds"] == 6.230818


def hostile(report: dict) -> int:
    mutations = []
    for key, value in [
        ("status", "PASS_EXACT_PROMOTED"), ("equivalence_accepted", True),
        ("promotion", "PROMOTE_SPASM_WARM_SOLVER"), ("warm_solve_run", True),
        ("rank_available", True), ("solution_artifacts", ["forged.sms"]),
    ]:
        forged = copy.deepcopy(report); forged[key] = value; mutations.append(forged)
    forged = copy.deepcopy(report); forged["scope"]["second_prime_run"] = True; mutations.append(forged)
    forged = copy.deepcopy(report); forged["export"]["equations_cached_columns"] -= 1; mutations.append(forged)
    forged = copy.deepcopy(report); forged["matrix_sha256"] = "0" * 64; mutations.append(forged)
    rejected = 0
    for forged in mutations:
        try: validate(forged)
        except AssertionError: rejected += 1
    assert rejected == len(mutations)
    return rejected


def main() -> None:
    pins = {}
    for path, expected in PINS.items():
        actual = sha(path)
        assert actual == expected, f"stale input {path}: {actual}"
        pins[str(path.relative_to(ROOT))] = actual
    export = json.loads((HERE / "export_cegar635.json").read_text())
    matrix = HERE / "matrix_cegar635_left_orientation.sms"
    rhs = HERE / "rhs_cegar635_minus_target.sms"
    stderr_path = HERE / "spasm_cold.stderr.log"
    stderr = stderr_path.read_text(errors="replace").replace("\r", "\n")
    progress = [(int(a), int(b)) for a, b in re.findall(r"Schur complement: (\d+)/(\d+)", stderr)]
    assert progress and "rank =" not in stderr and "Solving XA == B" not in stderr
    last_row, schur_rows = progress[-1]
    assert (last_row, schur_rows) == (12_604_048, 14_591_895)
    assert not list(HERE.glob("solution*.sms")) and not list(HERE.glob("solution*.tmp"))
    assert not (HERE / "spasm_warm.stderr.log").exists()
    tree = json.loads((PORTFOLIO / "results_tree_round635.json").read_text())
    report = {
        "schema": "KRENN_AFFINE251_D12_CEGAR635_SPASM_GATE_FAILURE_V1",
        "status": "GATE_FAILED_WALL_NO_SOLUTION",
        "scope": {"degree": 12, "round": 635, "prime": PRIME,
                  "second_prime_run": False, "full_closure_run": False},
        "equivalence_accepted": False,
        "promotion": "DO_NOT_PROMOTE",
        "pins": pins,
        "export": export,
        "matrix_sha256": sha(matrix), "matrix_bytes": matrix.stat().st_size,
        "rhs_sha256": sha(rhs), "rhs_bytes": rhs.stat().st_size,
        "resource_contract": {
            "cold_end_to_end_wall_seconds": 180,
            "rss_acceptance_limit_gib": 8,
            "rss_peak": "not captured for terminated process; no result accepted",
            "sandbox_setrlimit_preflight_failed_before_first process": True,
        },
        "cold_diagnostic": {
            "export_elapsed_seconds_internal": export["elapsed_seconds"],
            "solver_timeout_budget_seconds": 163.27767308300827,
            "solver_killed_at_end_to_end_wall": True,
            "last_schur_row": last_row, "schur_rows": schur_rows,
            "last_schur_fraction": last_row / schur_rows,
            "rank_available": False, "solution_available": False,
            "stderr_sha256": sha(stderr_path),
            "stdout_sha256": sha(HERE / "spasm_cold.stdout.log"),
        },
        "rank_available": False,
        "solution_artifacts": [],
        "warm_solve_run": False,
        "comparison": {
            "rust_tree_solve_seconds": tree["rounds"][-1]["solve_seconds"],
            "spasm_cold_export_plus_solve": ">=180 seconds; incomplete",
            "spasm_warm_solve_seconds": None,
            "materially_faster": False,
        },
        "exactness_retained": {
            "checkpoint_vector_column_order_equal": True,
            "vector_internal_fnv_verified": True,
            "retained_tree_support": tree["dual_support"],
            "retained_tree_candidate_target_value": 1,
            "retained_tree_candidate_annihilated_all_cached_columns_during_export": True,
            "spasm_solution_replay": "not applicable: no solution was produced",
        },
        "stop_reason": (
            "The exact 14,814,561-variable SpaSM orientation did not finish in the "
            "180-second export+solve gate. No warm timing or equivalence claim is inferred."
        ),
    }
    validate(report)
    output = HERE / "results_cegar635_spasm_gate_failure.json"
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    audit = {
        "schema": "KRENN_AFFINE251_D12_CEGAR635_SPASM_FAILURE_AUDIT_V1",
        "status": "PASS_FAIL_CLOSED",
        "failure_result_sha256": sha(output),
        "hostile_mutations_rejected": hostile(report),
        "scope": {"round635_only": True, "second_prime": False, "full_closure": False},
    }
    (HERE / "results_final_audit.json").write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n")
    print(json.dumps(audit, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
