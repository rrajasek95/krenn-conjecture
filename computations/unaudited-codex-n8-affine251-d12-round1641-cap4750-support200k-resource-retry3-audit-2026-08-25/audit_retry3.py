#!/usr/bin/env python3
"""Independent metadata audit of retry2 failure and final held retry3."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
R2 = ROOT / "computations/unaudited-codex-n8-affine251-d12-round1641-cap4750-support200k-resource-retry-design-2026-08-25"
R3 = ROOT / "computations/unaudited-codex-n8-affine251-d12-round1641-cap4750-support200k-resource-retry3-design-2026-08-25"


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def load(path: Path):
    return json.loads(path.read_text())


assert sha(R2 / "RETRY2_MANIFEST.sha256") == "0cc47ec23182027756b625793d5973ceb45ada49ce618124637c54bb60e33915"
assert sha(R3 / "MANIFEST.sha256") == "590b08fafb0813ef87c177feef7d359c9cd06bbc4543cbf68c952f03ff9883d2"
failure = load(R2 / "RETRY2_FAILURE.json")
watchdog = load(R2 / "candidate_r1641_cap4750_support200k_retry2/watchdog.json")
plan = load(R3 / "PLAN.json")
diff = load(R3 / "RESOURCE_DIFF.json")

assert failure["status"] == "REJECT_HARD_WALL_ZERO_COVERAGE" and failure["accepted_coverage"] == 0
assert failure["watchdog"]["breach"] == "WALL_CAP" and failure["watchdog"]["returncode"] == -15
assert failure["watchdog"]["abort_final_output_absent"] is True
assert failure["output_census"] == {
    "result_absent": True, "dual_absent": True, "temporary_outputs_absent": True,
    "stdout_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "stderr_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "r1641_absent": True, "r1642_absent": True,
}
assert failure["unchanged_clone"]["checkpoint_equals_audited_r1640"] is True
assert failure["unchanged_clone"]["vector_cache_equals_audited_r1640"] is True
assert failure["disposition"]["may_resume_or_reuse"] is False
assert watchdog["result_sha256"] is None and watchdog["abort_final_output_absent"] is True

assert plan["status"].startswith("HELD_")
assert not plan["arithmetic_authorized"] and not plan["arithmetic_launched"]
assert not plan["clone_created"] and not plan["large_endpoint_read_performed"]
assert diff["only_changes"] == {
    "native_wall_seconds": {"retry2": 300, "retry3": 450},
    "wrapper_wall_seconds": {"retry2": 360, "retry3": 540},
}
unchanged = diff["unchanged"]
assert unchanged["source_sha256"] == "3139689fb546aa1233a366e2dfa1dc007ea2f13399b89c951181d28636f43f59"
assert unchanged["binary_sha256"] == "79410bc8f73f2e486c97749a446c1ee7cf6e96982cd2c6fbe54619b60f675048"
assert unchanged["watchdog_source_sha256"] == "75bccbb64d2c9110707bc498fdb71791abe60d7ac3bdf1df942c5a2f63c5c997"
assert unchanged["support_cap"] == 200000 and unchanged["column_cap"] == 4750000
assert unchanged["round_cap"] == 1641 and unchanged["rss_limit_gib"] == 36
assert unchanged["workers"] == 16 and unchanged["pivot"] == "rare" and unchanged["strategy"] == "cold"
assert unchanged["elimination"] == "hierarchical" and unchanged["incremental"] == "no"

retry = plan["retry3"]
assert retry["fresh_distinct_clone_from_exact_audited_r1640"] is True
assert retry["attempt1_or_retry2_resume_reuse_forbidden"] is True
assert retry["native_wall_seconds"] == 450 and retry["wrapper_wall_seconds"] == 540
assert retry["last_permitted_wall_escalation"] is True
assert retry["if_retry3_fails"].startswith("STOP_THIS_GEOMETRY")
assert diff["classification"] == "RESOURCE_ONLY_LAST_PERMITTED_WALL_ESCALATION"
assert diff["retry3_failure_terminal"] is True and diff["generic_relaxation"] is False
assert plan["acceptance"]["exact_rounds"] == [1641] and plan["acceptance"]["r1642_absent"] is True
assert plan["acceptance"]["inherited_records_byte_identical"] == 4069711
assert plan["acceptance"]["strict_checkpoint_descendant"] is True
assert plan["acceptance"]["full_replay_target"] == 1 and plan["acceptance"]["full_replay_failures"] == 0
assert plan["storage"]["minimum_preclone_free_kib"] == 96 * 1024 * 1024
assert "escalate wall limits again if retry3 fails" in plan["forbidden"]

result = {
    "schema": "KRENN_AFFINE251_D12_R1641_FINAL_RETRY3_INDEPENDENT_AUDIT_V1",
    "status": "APPROVE_HELD_FINAL_RESOURCE_RETRY3",
    "pins": {
        "retry2_failure_manifest_sha256": sha(R2 / "RETRY2_MANIFEST.sha256"),
        "retry2_failure_evidence_sha256": sha(R2 / "RETRY2_FAILURE.json"),
        "retry2_watchdog_sha256": sha(R2 / "candidate_r1641_cap4750_support200k_retry2/watchdog.json"),
        "retry3_design_manifest_sha256": sha(R3 / "MANIFEST.sha256"),
        "prior_resource_referee_sha256": plan["approved_math_contract"]["retry2_resource_referee_sha256"],
        "prior_resource_referee_manifest_sha256": plan["approved_math_contract"]["retry2_resource_referee_manifest_sha256"],
    },
    "retry2": {
        "verdict": "REJECT_HARD_WALL_ZERO_COVERAGE",
        "elapsed_seconds": failure["watchdog"]["elapsed_seconds"],
        "peak_rss_kib": failure["watchdog"]["peak_rss_kib"],
        "result_dual_tmp_r1641_r1642_absent": True,
        "checkpoint_cache_claim_sealed_equal_r1640": True,
        "large_rehash_repeated_by_this_metadata_audit": False,
        "may_resume_or_reuse": False,
    },
    "retry3_diff": {
        "only_changes": ["native wall 300 -> 450", "wrapper wall 360 -> 540"],
        "unchanged": unchanged,
        "last_permitted_escalation": True,
        "any_failure_action": "STOP_THIS_GEOMETRY; no fourth wall escalation",
    },
    "acceptance": {
        "fresh_distinct_audited_r1640_clone": True,
        "both_prior_attempts_reuse_forbidden": True,
        "exact_rounds": [1641], "r1642_absent": True,
        "status_reason": "INCOMPLETE_SEARCH_CAP/ROUND_CAP",
        "inherited_records_byte_identical": 4069711,
        "strict_checkpoint_descendant": True,
        "full_replay_target": 1, "full_replay_failures": 0,
        "atomic_watchdog_resource_pass": True,
        "independent_postrun_referee_required": True,
    },
    "storage": {"preclone_floor_kib": 100663296, "fresh_remeasure_rehash_required": True},
    "scope": {"metadata_only": True, "large_payload_rehash": False, "clone": False, "launch": False},
}

(HERE / "results_retry3_audit.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps({"status": result["status"], "terminal": True}))
