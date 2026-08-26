#!/usr/bin/env python3
"""Independent fail-closed audit of terminal retry3 SUPPORT_CAP package."""

from __future__ import annotations

import hashlib
import json
import struct
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PKG = ROOT / "computations/unaudited-codex-n8-affine251-d12-round1641-cap4750-support200k-resource-retry3-design-2026-08-25"
CAND = PKG / "candidate_r1641_cap4750_support200k_retry3"


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def load(path: Path):
    return json.loads(path.read_text())


assert sha(PKG / "RETRY3_MANIFEST.sha256") == "19b00378da4cba56a22a19c4d7167622afb83f2550c4622ef283d7d19fc8da1c"
failure = load(PKG / "RETRY3_FAILURE.json")
result = load(CAND / "result.json")
watchdog = load(CAND / "watchdog.json")
plan = load(PKG / "PLAN.json")

assert failure["status"] == "REJECT_SUPPORT_CAP_ZERO_COVERAGE_STOP_THIS_GEOMETRY"
assert failure["accepted_coverage"] == 0
assert result["status"] == "INCOMPLETE_SEARCH_CAP" and result["incomplete_reason"] == "SUPPORT_CAP"
assert result["rounds_completed"] == 1640 and result["rounds"] == []
assert result["column_orbits_exposed"] == 4293039
assert result["column_orbits_exposed"] - 4069711 == 223328
assert result["dual_support"] == 464887 and result["dual_support"] > result["support_cap"] == 200000
assert result["dual_support"] - result["support_cap"] == 264887
assert result["global_annihilation"] is None and result["target_pairing"] is None

# Parse only fixed headers; the full payload hashes were independently replayed
# via the producer manifest before this script was sealed.
with (CAND / "checkpoint.bin").open("rb") as f:
    header = f.read(44)
assert header[:9] == b"AFF12CEG1"
prime = struct.unpack_from("<Q", header, 12)[0]
round_index = struct.unpack_from("<Q", header, 20)[0]
checkpoint_columns = struct.unpack_from("<Q", header, 28)[0]
checkpoint_support = struct.unpack_from("<Q", header, 36)[0]
assert prime == 1073741827 and round_index == 1640
assert checkpoint_columns == 4293039 and checkpoint_support == 76616

with (CAND / "vectors.bin").open("rb") as f:
    vector_header = f.read(44)
assert vector_header[:9] == b"AFF12VEC1"
vector_columns = struct.unpack_from("<Q", vector_header, 36)[0]
assert vector_columns == 4293039

names = {p.name for p in CAND.iterdir() if p.is_file()}
assert "dual.tsv" not in names
assert not any(name.endswith(".tmp") for name in names)
assert not any("1641" in name or "1642" in name for name in names)

assert watchdog["status"] == "PASS" and watchdog["returncode"] == 0 and watchdog["breach"] is None
assert watchdog["atomic_outputs_clean"] is True
assert watchdog["elapsed_seconds"] < watchdog["wall_limit_seconds"] == 540
assert watchdog["peak_rss_kib"] < watchdog["rss_limit_kib"]
assert watchdog["result_sha256"] == sha(CAND / "result.json")

disposition = failure["disposition"]
assert disposition["may_claim_r1641"] is False
assert disposition["may_claim_descendant_or_replay_acceptance"] is False
assert disposition["fourth_escalation_forbidden"] is True
assert disposition["continuation_forbidden"] is True
assert disposition["geometry_status"] == "STOPPED"
assert plan["retry3"]["last_permitted_wall_escalation"] is True
assert "escalate wall limits again if retry3 fails" in plan["forbidden"]

output = {
    "schema": "KRENN_AFFINE251_D12_R1641_RETRY3_SUPPORT_CAP_TERMINAL_INDEPENDENT_AUDIT_V1",
    "status": "PASS_TERMINAL_SUPPORT_CAP_ZERO_COVERAGE_STOP_GEOMETRY",
    "pins": {
        "producer_terminal_manifest_sha256": sha(PKG / "RETRY3_MANIFEST.sha256"),
        "producer_failure_sha256": sha(PKG / "RETRY3_FAILURE.json"),
        "result_sha256": sha(CAND / "result.json"),
        "watchdog_sha256": sha(CAND / "watchdog.json"),
        "checkpoint_sha256": failure["quarantined_hybrid"]["output_checkpoint_sha256"],
        "vector_cache_sha256": failure["quarantined_hybrid"]["output_vector_cache_sha256"],
        "independent_retry3_design_referee_sha256": failure["bound_contract"]["independent_referee_sha256"],
        "independent_retry3_design_manifest_sha256": failure["bound_contract"]["independent_referee_manifest_sha256"],
    },
    "census": {
        "input_columns": 4069711,
        "new_columns_exposed": 223328,
        "hybrid_columns": 4293039,
        "computed_rejected_support": 464887,
        "support_cap": 200000,
        "support_excess": 264887,
        "accepted_r1641_coverage": 0,
    },
    "hybrid_headers": {
        "checkpoint_round": round_index,
        "checkpoint_columns": checkpoint_columns,
        "checkpoint_old_candidate_support": checkpoint_support,
        "vector_cache_columns": vector_columns,
        "computed_next_support_not_committed": 464887,
    },
    "filesystem": {
        "result_present": True, "dual_absent": True, "temporary_outputs_absent": True,
        "r1641_absent": True, "r1642_absent": True,
    },
    "resource": {
        "watchdog_status": "PASS", "breach": None,
        "elapsed_seconds": watchdog["elapsed_seconds"],
        "peak_rss_kib": watchdog["peak_rss_kib"],
        "atomic_outputs_clean": True,
    },
    "disposition": {
        "quarantined_non_resumable": True,
        "not_a_descendant_or_replay_candidate": True,
        "geometry_status": "STOPPED",
        "fourth_escalation_forbidden": True,
        "new_D12_arithmetic_authorized": False,
    },
}

(HERE / "results_terminal_audit.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
print(json.dumps({"status": output["status"], "new_columns": 223328, "support": 464887}))
