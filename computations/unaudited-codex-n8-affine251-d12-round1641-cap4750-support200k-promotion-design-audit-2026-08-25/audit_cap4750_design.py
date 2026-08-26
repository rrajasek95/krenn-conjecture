#!/usr/bin/env python3
"""Independent metadata referee for the held r1641 cap4.75m design."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DESIGN = ROOT / "computations/unaudited-codex-n8-affine251-d12-round1641-cap4750-support200k-promotion-design-2026-08-25"
DIAG = ROOT / "computations/unaudited-codex-n8-affine251-d12-round1641-support200k-column-cap-diagnostic-audit-2026-08-25"
STATIC = ROOT / "computations/unaudited-codex-n8-affine251-d12-round1640-cap4250-exhaustion-promotion-design-2026-08-25"
CONTROL = ROOT / "computations/unaudited-codex-n8-affine251-d12-round1641-support200k-promotion-design-2026-08-25"


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def load(path: Path):
    return json.loads(path.read_text())


assert sha(DESIGN / "MANIFEST.sha256") == "134b8c101c6c6cdbf9347777926404e2af8653804cbcb25306f851b7d32c76ae"
assert sha(DIAG / "results_independent_diagnostic_audit.json") == "d6b31a8c2f0bc6f487ed568fc9dca954e57c95e91078d4df82bde5ca2375664d"
assert sha(DIAG / "FINAL_MANIFEST.sha256") == "edc643bb4c555f2bfdc2e807c3df1c9f9231b85525526401461b1a0b8923707d"
assert sha(STATIC / "audit_column_cap_source.py") == "b029ba545621edd5794a3538d5cd9e4dba2848f86174a5a6f887e10860020c31"
assert sha(STATIC / "results_static_column_cap_audit.json") == "1cab0b83362ab8a984f4ee81c480c79d04bf80c035c53e60ce0f425e29fe79e2"

plan = load(DESIGN / "PLAN.json")
options = load(DESIGN / "CAP_OPTIONS.json")
diag = load(DIAG / "results_independent_diagnostic_audit.json")
static = load(STATIC / "results_static_column_cap_audit.json")
control_wd = load(CONTROL / "candidate_r1641_support200k/watchdog.json")

assert plan["status"].startswith("HELD_")
assert not plan["arithmetic_authorized"] and not plan["arithmetic_launched"]
assert not plan["clone_created"] and not plan["large_endpoint_read_performed"]
assert diag["status"] == "PASS_ZERO_COVERAGE_COLUMN_CAP_UNCHANGED_R1640"
assert diag["guard_referee"]["new_columns_lower_bound"] == 180290
assert diag["guard_referee"]["exact_next_columns_known"] is False
assert static["status"] == "PASS_COLUMN_CAP_ONLY_PRE_ARITHMETIC_CAPACITY_GUARD"
assert static["proof"]["capacity_guard_before_column_arithmetic"] is True
assert static["proof"]["enumeration_scoring_and_elimination_do_not_read_column_cap"] is True

bound = (180290 * 2 * 5 + 3) // 4
assert bound == 450725
assert 4069711 + bound == 4520436
assert 4500000 - 4069711 == 430289
assert bound - 430289 == 20436
assert 4750000 - 4069711 == 680289
assert 680289 - bound == 229564
assert options["selected_column_cap"] == 4750000
assert options["shock_aware_policy"]["conservative_new_column_bound"] == bound
assert options["shock_aware_policy"]["classification"].endswith("not a mathematical bound on the frontier")

candidate = plan["frozen_candidate"]
assert candidate["column_cap"] == 4750000 and candidate["support_cap"] == 200000
assert candidate["round_cap"] == 1641 and candidate["required_r1642_absent"] is True
assert candidate["required_exact_round_records"] == [1641]
assert candidate["required_status"] == "INCOMPLETE_SEARCH_CAP" and candidate["required_reason"] == "ROUND_CAP"
assert candidate["required_inherited_records"] == 4069711
assert candidate["required_inherited_records_byte_identical"] is True
assert candidate["required_checkpoint_strict_descendant"] is True
assert candidate["required_full_replay_target"] == 1 and candidate["required_full_replay_failures"] == 0

# Compare the complete normalized semantic/resource argument list with the
# exhausted cap4.25 lane: exactly the column-cap literal changes.
command = control_wd["command"]
flag_values = {command[i]: command[i + 1] for i in range(1, len(command) - 1, 2) if command[i].startswith("--")}
expected = {
    "--prime": str(candidate["prime"]), "--workers": str(candidate["workers"]),
    "--pivot": candidate["pivot"], "--strategy": candidate["strategy"],
    "--elimination": candidate["elimination"], "--incremental": "no",
    "--support-cap": str(candidate["support_cap"]), "--round-cap": str(candidate["round_cap"]),
    "--wall-seconds": str(candidate["native_wall_seconds"]), "--rss-gib": str(candidate["rss_limit_gib"]),
}
assert all(flag_values[k] == v for k, v in expected.items())
assert flag_values["--column-cap"] == "4250000"

storage = plan["storage"]
assert storage["minimum_preclone_free_kib"] == 96 * 1024 * 1024
assert storage["design_time_free_kib"] > storage["minimum_preclone_free_kib"]
assert storage["remeasure_and_rehash_immediately_before_clone"] is True

result = {
    "schema": "KRENN_AFFINE251_D12_R1641_CAP4750_SUPPORT200K_INDEPENDENT_DESIGN_AUDIT_V1",
    "status": "APPROVE_HELD_CAP4750_SUPPORT200K_ONE_ROUND",
    "pins": {
        "producer_design_manifest_sha256": sha(DESIGN / "MANIFEST.sha256"),
        "column_cap_diagnostic_referee_sha256": sha(DIAG / "results_independent_diagnostic_audit.json"),
        "column_cap_diagnostic_manifest_sha256": sha(DIAG / "FINAL_MANIFEST.sha256"),
        "static_column_cap_script_sha256": sha(STATIC / "audit_column_cap_source.py"),
        "static_column_cap_result_sha256": sha(STATIC / "results_static_column_cap_audit.json"),
        "input_checkpoint_sha256": plan["input"]["checkpoint_sha256"],
        "input_cache_sha256": plan["input"]["vector_cache_sha256"],
    },
    "dependency_binding": {
        "producer_plan_placeholders_were_null": True,
        "this_audit_binds_the_independent_diagnostic": True,
        "launch_must_pin_both_producer_design_and_this_audit_manifest": True,
    },
    "column_cap_theorem": {
        "sole_semantic_use": "pre-invariant-arithmetic whole-next-set capacity guard",
        "deterministic_enumeration_independent_of_cap": True,
        "sole_normalized_command_diff": "--column-cap 4250000 -> 4750000",
    },
    "shock_policy": {
        "strict_observed_lower_bound": 180290,
        "formula": "ceil(180290*2*5/4)",
        "declared_bound": bound,
        "minimum_total_cap": 4520436,
        "cap4500000_shortfall": 20436,
        "cap4750000_margin": 229564,
        "classification": "resource policy only; not a frontier theorem",
    },
    "acceptance": {
        "fresh_r1640_clone": True,
        "column_cap": 4750000,
        "support_cap": 200000,
        "exact_rounds": [1641],
        "r1642_absent": True,
        "inherited_records_byte_identical": 4069711,
        "strict_checkpoint_descendant": True,
        "full_replay_target": 1,
        "full_replay_failures": 0,
        "atomic_watchdog_resource_pass": True,
        "independent_postrun_referee_required": True,
    },
    "storage": {
        "preclone_floor_kib": storage["minimum_preclone_free_kib"],
        "design_time_pass": True,
        "fresh_measurement_required": True,
    },
    "fail_closed": plan["fail_closed_outcomes"],
    "scope": {"metadata_only": True, "large_candidate_read": False, "clone": False, "launch": False},
}

(HERE / "results_cap4750_design_audit.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps({"status": result["status"], "bound": bound, "margin": 229564}))
