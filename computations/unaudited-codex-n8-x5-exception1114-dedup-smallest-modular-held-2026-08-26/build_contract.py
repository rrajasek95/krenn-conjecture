#!/usr/bin/env python3
"""Materialize the zero-run held/refusal interfaces for the sole modular lane."""

import hashlib
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PINS = {
    "rank1_refinement_manifest_sha256": "aea0841b7b1b6fe0773cfb5087a930329c4da5d94951ad23d559de6d61cddb46",
    "symbolic_reduction_manifest_sha256": "785ec6cb6a5d790ece4fa3aed3801b48c3c51423e4378cd761ad8b50cd2d22b9",
    "q_source_sha256": "ed6a47ec38fca48e6b7396e36c61e3eca8004089bd2964476e1dcdd45b69de1f",
    "modular_source_sha256": "4789b9cef4c3db41eb63819d66c7bd86f24f46a647a2665daf65c0b2b15beda3",
    "source_derivation_sha256": "7d2817c82cc0cfcbc6785fa8f47c2d122e84cc0523d72aea5c0240bd30baf34d",
    "runner_sha256": "545e9fb222bb3623ec8c3b5a09b45eec52a62489f79fcb91855e712463839c3c",
    "singular_sha256": "9436b32ff7565719240230de8a6fb1d27af5e65f0ca4c9c5b756a77e82409b88",
    "gtimeout_sha256": "1e26c50fa8c439fe1f4e6c6edd106e95030e16582c1c8c32e73d8a889cdf5b95",
}


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            h.update(chunk)
    return h.hexdigest()


def atomic(path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


checks = {
    HERE / "rep1114_rank1_z1_fulltorus_dedup_p32003.sing": PINS["modular_source_sha256"],
    HERE / "source_derivation.json": PINS["source_derivation_sha256"],
    HERE / "run_one_lane.py": PINS["runner_sha256"],
    ROOT / "computations/unaudited-codex-n8-x5-exception1114-rank1-refinement-design-2026-08-26/MANIFEST.sha256": PINS["rank1_refinement_manifest_sha256"],
    ROOT / "computations/unaudited-codex-n8-x5-exception1114-rank1-symbolic-reduction-design-2026-08-26/MANIFEST.sha256": PINS["symbolic_reduction_manifest_sha256"],
    ROOT / "computations/unaudited-codex-n8-x5-exception1114-rank1-symbolic-reduction-design-2026-08-26/rep1114_rank1_z1_fulltorus_dedup_Q.sing": PINS["q_source_sha256"],
    Path("/usr/local/bin/Singular"): PINS["singular_sha256"],
    Path("/usr/local/bin/gtimeout"): PINS["gtimeout_sha256"],
}
for path, expected in checks.items():
    if not path.is_file() or sha(path) != expected:
        raise RuntimeError((path, expected))

held = {
    "schema": "KRENN_X5_EXCEPTION1114_DEDUP_MODULAR_HELD_V1",
    "status": "HELD_ZERO_RUN_PENDING_INDEPENDENT_AUDIT_AND_FRESH_CLEARANCE",
    "pins": PINS,
    "source": {"path": "rep1114_rank1_z1_fulltorus_dedup_p32003.sing", "field": "F_32003", "variables": 58, "generators": 6533, "sha256": PINS["modular_source_sha256"]},
    "execution": {
        "maximum_lane_count": 1, "native_wall_seconds": 300, "wrapper_wall_seconds": 315,
        "rss_cap_bytes": 8 * 1024**3, "direct_libproc_group_rss": True,
        "fresh_libproc_process_census": True, "atomic_result": True,
        "exclusive_attempt_marker": True, "strict_stop_after_any_outcome": True,
        "combined_sat_or_checker_overlap_forbidden": True,
    },
    "authorization": {"independent_acceptance_present": False, "fresh_clearance_present": False, "exact_Q_authorized": False, "automatic_relaunch_authorized": False},
    "acceptance": "modular UNIT is diagnostic only and requires exact shape plus GROEBNER_SIZE=1, UNIT_REMAINDER=0, STATUS=UNIT_IDEAL; every other outcome is fail-closed/noncoverage",
    "scope": {"attempts": 0, "results": 0, "solver_runs": 0, "mathematical_coverage": False, "record1114_closed": False},
}
atomic(HERE / "held_pilot.json", held)

acceptance_schema = {
    "schema": "KRENN_X5_EXCEPTION1114_DEDUP_MODULAR_ACCEPTANCE_V1",
    "status": "PASS_APPROVE_ONE_P32003_DIAGNOSTIC_ONLY",
    "held_manifest_sha256": "<64 lowercase hex: future sealed held manifest>",
    "source_derivation_sha256": PINS["source_derivation_sha256"],
    "source_sha256": PINS["modular_source_sha256"],
    "runner_sha256": PINS["runner_sha256"],
    "rank1_refinement_manifest_sha256": PINS["rank1_refinement_manifest_sha256"],
    "symbolic_reduction_manifest_sha256": PINS["symbolic_reduction_manifest_sha256"],
    "prime": 32003, "variables": 58, "generators": 6533, "maximum_lane_count": 1,
    "exact_Q_authorized": False, "automatic_relaunch_authorized": False,
}
atomic(HERE / "independent_referee_acceptance.schema.json", acceptance_schema)

clearance_schema = {
    "schema": "KRENN_X5_EXCEPTION1114_DEDUP_MODULAR_CLEARANCE_V1",
    "status": "CLEARED_ONE_P32003_DIAGNOSTIC_ONLY",
    "held_manifest_sha256": "<64 lowercase hex>",
    "independent_referee_acceptance_sha256": "<64 lowercase hex>",
    "source_sha256": PINS["modular_source_sha256"], "runner_sha256": PINS["runner_sha256"],
    "singular_sha256": PINS["singular_sha256"], "gtimeout_sha256": PINS["gtimeout_sha256"],
    "nonce": "<32 lowercase hex>", "issued_at_utc": "<ISO8601Z>", "expires_at_utc": "<ISO8601Z, <=600 seconds after issue>",
    "maximum_lane_count": 1, "native_wall_seconds": 300, "wrapper_wall_seconds": 315,
    "rss_cap_bytes": 8 * 1024**3, "no_overlap_confirmed": True,
    "manager_clearance_confirmed": True, "resource_clearance_confirmed": True,
    "census_policy_sha256": "<runner-computed policy SHA>", "expected_census_match_count": 0,
    "exact_Q_authorized": False, "automatic_relaunch_authorized": False,
}
atomic(HERE / "launch_clearance.schema.json", clearance_schema)

conditional_q = {
    "schema": "KRENN_X5_EXCEPTION1114_DEDUP_EXACT_Q_CONDITIONAL_V1",
    "status": "HELD_DEPENDENCIES_ABSENT_NO_RUNNER_NO_LAUNCH",
    "q_source": {"path": "computations/unaudited-codex-n8-x5-exception1114-rank1-symbolic-reduction-design-2026-08-26/rep1114_rank1_z1_fulltorus_dedup_Q.sing", "sha256": PINS["q_source_sha256"], "variables": 58, "generators": 6533},
    "required_future_dependencies": {
        "modular_terminal_status": "UNIT_IDEAL_MODULAR_DIAGNOSTIC",
        "modular_terminal_manifest_sha256": None,
        "independent_modular_terminal_audit_manifest_sha256": None,
        "future_exact_q_design_referee_manifest_sha256": None,
        "fresh_exact_q_resource_clearance": None,
    },
    "authorization": {"exact_Q_authorized": False, "runner_materialized": False, "launch_clearance_present": False, "automatic_followup": False},
    "scope_guard": "a modular UNIT is only a diagnostic prerequisite; it supplies no characteristic-zero proof and cannot itself authorize Q arithmetic",
}
atomic(HERE / "exact_Q_followup_conditional.json", conditional_q)

refusal = {
    "schema": "KRENN_X5_EXCEPTION1114_DEDUP_MODULAR_REFUSAL_V1",
    "status": "REFUSE_UNTIL_ACCEPTANCE_AND_FRESH_CLEARANCE",
    "missing_by_design": ["independent_referee_acceptance.json", "launch_clearance.json"],
    "terminal_markers_forbid_relaunch": ["RUN_EXCLUSIVE.lock", "ATTEMPT.json", "result.json", "result.json.tmp"],
    "overlap_forbidden_executables": ["Singular", "gtimeout", "cadical", "drat-trim", "kissat", "sparse_d12_dual", "sparse_d12_dual_v4_1", "sparse_d12_dual_fixed_lane", "sparse_d12_dual_portfolio_audit"],
    "exact_Q_separately_conditional": True,
}
atomic(HERE / "refusal_contract.json", refusal)
print(json.dumps({"status": held["status"], "source": held["source"], "attempts": 0}, sort_keys=True))
