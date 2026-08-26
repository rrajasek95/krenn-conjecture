#!/usr/bin/env python3
"""Independent metadata referee for r1641 attempt1 and resource-only retry2."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = ROOT / "computations/unaudited-codex-n8-affine251-d12-round1641-cap4750-support200k-promotion-design-2026-08-25"
RETRY = ROOT / "computations/unaudited-codex-n8-affine251-d12-round1641-cap4750-support200k-resource-retry-design-2026-08-25"


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def load(path: Path):
    return json.loads(path.read_text())


assert sha(BASE / "FAILURE_MANIFEST_ATTEMPT1.sha256") == "24f42c1417114a52720402fcde98d469ddf1cb33656c24dc5fb538bad1a008b1"
assert sha(RETRY / "MANIFEST.sha256") == "3e1c193b38974793de4d723b22985a550a14953b4a2229ae193ec3dcf76e7feb"
failure = load(BASE / "FAILURE_EVIDENCE_ATTEMPT1.json")
watchdog = load(BASE / "candidate_r1641_cap4750_support200k/watchdog.json")
plan = load(RETRY / "PLAN.json")
diff = load(RETRY / "RESOURCE_DIFF.json")

assert failure["status"] == "REJECT_HARD_WALL_ZERO_COVERAGE"
assert failure["accepted_coverage"] == 0 and failure["accepted_r1641"] is False
attempt = failure["attempt"]
assert attempt["watchdog_status"] == "FAIL" and attempt["watchdog_breach"] == "WALL_CAP"
assert attempt["watchdog_returncode"] == -15 and attempt["result_present"] is False
assert attempt["dual_present"] is False and attempt["tmp_files"] == 0
assert attempt["abort_final_output_absent"] is True
assert failure["unchanged_clone"]["checkpoint_equal_input"] is True
assert failure["unchanged_clone"]["vector_cache_equal_input"] is True
assert failure["classification"]["may_resume_from_attempt"] is False
assert watchdog["result_sha256"] is None and watchdog["abort_final_output_absent"] is True

assert plan["status"].startswith("HELD_")
assert not plan["arithmetic_authorized"] and not plan["arithmetic_launched"]
assert not plan["clone_created"] and not plan["large_endpoint_read_performed"]
changed = diff["changed"]
assert changed == {
    "solver_native_wall_seconds": {"before": 210, "after": 300},
    "watchdog_hard_wall_seconds": {"before": 240, "after": 360},
}
unchanged = diff["unchanged"]
expected_unchanged = {
    "source_sha256": "3139689fb546aa1233a366e2dfa1dc007ea2f13399b89c951181d28636f43f59",
    "binary_sha256": "79410bc8f73f2e486c97749a446c1ee7cf6e96982cd2c6fbe54619b60f675048",
    "watchdog_source_sha256": "75bccbb64d2c9110707bc498fdb71791abe60d7ac3bdf1df942c5a2f63c5c997",
    "prime": 1073741827, "workers": 16, "strategy": "cold", "pivot": "rare",
    "elimination": "hierarchical", "incremental": "no", "portfolio": False,
    "support_cap": 200000, "column_cap": 4750000, "round_cap": 1641,
    "rss_limit_gib": 36,
    "input_checkpoint_sha256": "12f79c86f8d8d20d3f9b83c634e82d689461796df60f9cd63feed9d86545ca8d",
    "input_vector_cache_sha256": "1d7ce92a7df3a6382332f1af85af4dd1f4a9b7d49c6a6d206066dcce9d36de12",
}
assert unchanged == expected_unchanged

retry = plan["retry2"]
assert retry["fresh_distinct_apfs_clone_from_exact_audited_r1640"] is True
assert retry["must_not_copy_resume_or_reuse_attempt1"] is True
assert retry["native_wall_seconds"] == 300 and retry["wrapper_wall_seconds"] == 360
assert retry["required_exact_round_records"] == [1641] and retry["required_r1642_absent"] is True
assert retry["required_status"] == "INCOMPLETE_SEARCH_CAP" and retry["required_reason"] == "ROUND_CAP"
assert retry["required_inherited_records"] == 4069711
assert retry["required_inherited_records_byte_identical"] is True
assert retry["required_checkpoint_strict_descendant"] is True
assert retry["required_full_replay_target"] == 1 and retry["required_full_replay_failures"] == 0
assert plan["storage"]["minimum_preclone_free_kib"] == 96 * 1024 * 1024
assert plan["storage"]["remeasure_and_rehash_immediately_before_clone"] is True

result = {
    "schema": "KRENN_AFFINE251_D12_R1641_CAP4750_RESOURCE_RETRY_INDEPENDENT_AUDIT_V1",
    "status": "APPROVE_HELD_RESOURCE_ONLY_RETRY2",
    "pins": {
        "attempt1_failure_manifest_sha256": sha(BASE / "FAILURE_MANIFEST_ATTEMPT1.sha256"),
        "attempt1_failure_evidence_sha256": sha(BASE / "FAILURE_EVIDENCE_ATTEMPT1.json"),
        "attempt1_watchdog_sha256": sha(BASE / "candidate_r1641_cap4750_support200k/watchdog.json"),
        "retry_design_manifest_sha256": sha(RETRY / "MANIFEST.sha256"),
        "approved_math_design_referee_sha256": plan["approved_math_contract"]["design_referee_sha256"],
        "approved_math_design_manifest_sha256": plan["approved_math_contract"]["design_referee_manifest_sha256"],
    },
    "attempt1": {
        "verdict": "REJECT_HARD_WALL_ZERO_COVERAGE",
        "wall_seconds": attempt["watchdog_elapsed_seconds"],
        "peak_rss_kib": attempt["peak_rss_kib"],
        "result_absent": True, "dual_absent": True, "tmp_absent": True,
        "r1641_absent": True, "r1642_absent": True,
        "checkpoint_cache_equal_audited_r1640": True,
        "may_resume_or_reuse": False,
    },
    "retry_diff": {
        "only_changes": ["native wall 210 -> 300", "wrapper wall 240 -> 360"],
        "unchanged": unchanged,
    },
    "retry_acceptance": {
        "fresh_distinct_r1640_clone": True,
        "attempt1_reuse_forbidden": True,
        "exact_rounds": [1641], "r1642_absent": True,
        "status_reason": "INCOMPLETE_SEARCH_CAP/ROUND_CAP",
        "inherited_records_byte_identical": 4069711,
        "strict_checkpoint_descendant": True,
        "full_replay_target": 1, "full_replay_failures": 0,
        "atomic_watchdog_resource_pass": True,
        "independent_postrun_referee_required": True,
    },
    "storage": {"preclone_floor_kib": 100663296, "fresh_remeasure_rehash_required": True},
    "scope": {"metadata_only": True, "large_payload_replay": False, "clone": False, "launch": False},
}

(HERE / "results_resource_retry_audit.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps({"status": result["status"], "attempt1": result["attempt1"]["verdict"]}))
