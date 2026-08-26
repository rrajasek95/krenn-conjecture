#!/usr/bin/env python3
"""Independent metadata/source referee for the held r1641 support-cap promotion."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DESIGN = ROOT / "computations/unaudited-codex-n8-affine251-d12-round1641-support200k-promotion-design-2026-08-25"
OLD = ROOT / "computations/unaudited-codex-n8-affine251-d12-round1641-cap4250-continuation-design-2026-08-25"
SOURCE = ROOT / "computations/unaudited-codex-n8-affine251-d12-hierarchical-v4-rare-index-2026-08-25/sealed_v4_1/main.rs"
EXPECTED_MANIFEST = "aa0b400ee8ec9de33befe02f32737149cc965a822f1aefafc06ec83e2d9d0271"
EXPECTED_SOURCE = "3139689fb546aa1233a366e2dfa1dc007ea2f13399b89c951181d28636f43f59"


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def load(path: Path):
    return json.loads(path.read_text())


assert sha(DESIGN / "MANIFEST.sha256") == EXPECTED_MANIFEST
assert sha(SOURCE) == EXPECTED_SOURCE
plan = load(DESIGN / "PLAN.json")
old = load(OLD / "PLAN.json")
source = SOURCE.read_text()

assert plan["status"].startswith("HELD_")
assert plan["arithmetic_authorized"] is False
assert plan["arithmetic_launched"] is False
assert plan["clone_created"] is False
assert plan["large_endpoint_read_performed"] is False

occurrence_lines = [i + 1 for i, line in enumerate(source.splitlines()) if "support_cap" in line]
assert occurrence_lines == [1630, 1728, 1766, 1797, 3188, 3783]
assert source.count("support_cap") == 7
assert source.count("config.support_cap") == 2
assert source.count("if next.len() > config.support_cap {") == 1

markers = [
    "if columns.len() + new_columns.len() > config.column_cap {",
    "parallel_invariant_columns(&provider, &new_columns, config.prime, config.workers);",
    "columns.extend(new_columns.iter().copied());",
    "let Some((next, selected_strategy, selected_pivot)) = choices.into_iter().next() else {",
    "if next.len() > config.support_cap {",
    "candidate = next;",
    "completed_rounds += 1;",
]
positions = [source.index(marker) for marker in markers]
assert positions == sorted(positions) and len(set(positions)) == len(positions)

old_cfg = old["frozen_engine"]
new_cfg = plan["frozen_candidate"]
same_keys = [
    "source_sha256", "binary_sha256", "watchdog_source_sha256", "prime", "workers",
    "strategy", "pivot", "elimination", "incremental", "portfolio", "column_cap",
    "round_cap", "native_wall_seconds", "wrapper_wall_seconds", "rss_limit_gib",
]
assert all(old_cfg[k] == new_cfg[k] for k in same_keys)
assert old_cfg["support_cap"] == 100000 and new_cfg["support_cap"] == 200000

projection = plan["support_projection"]
assert projection["previous_growth"] == 43912
assert (43912 * 5 + 3) // 4 == 54890
assert 76616 + 54890 == 131506
assert projection["minimum_conservative_inclusive_cap"] == 131506
assert projection["selected_candidate_cap"] == 200000
assert projection["selected_cap_margin_above_projected_support"] == 68494

candidate = plan["frozen_candidate"]
assert candidate["round_cap"] == 1641
assert candidate["required_exact_round_records"] == [1641]
assert candidate["required_round1642_absent"] is True
assert candidate["required_status"] == "INCOMPLETE_SEARCH_CAP"
assert candidate["required_reason"] == "ROUND_CAP"
assert candidate["required_inherited_records"] == 4069711
assert candidate["required_inherited_records_byte_identical"] is True
assert candidate["required_checkpoint_strict_descendant"] is True
assert candidate["required_full_replay_target"] == 1
assert candidate["required_full_replay_failures"] == 0

lower = plan["lower_cap_control_assessment"]
assert lower["recommended"] is False
assert lower["can_produce_unchanged_checkpoint_and_cache"] is False
assert lower["failure_state"].startswith("hybrid clone")

result = {
    "schema": "KRENN_AFFINE251_D12_R1641_SUPPORT200K_INDEPENDENT_DESIGN_AUDIT_V1",
    "status": "APPROVE_HELD_SUPPORT200K_DIRECT_PROMOTION",
    "pins": {
        "producer_design_manifest_sha256": EXPECTED_MANIFEST,
        "superseded_design_manifest_sha256": sha(OLD / "MANIFEST.sha256"),
        "source_sha256": EXPECTED_SOURCE,
        "binary_sha256": new_cfg["binary_sha256"],
        "watchdog_source_sha256": new_cfg["watchdog_source_sha256"],
        "input_independent_manifest_sha256": plan["input"]["independent_manifest_sha256"],
        "input_checkpoint_sha256": plan["input"]["checkpoint_sha256"],
        "input_cache_sha256": plan["input"]["vector_cache_sha256"],
    },
    "source_referee": {
        "support_cap_token_count": 7,
        "occurrence_lines": occurrence_lines,
        "config_reads": 2,
        "sole_semantic_use": "strict next.len() > config.support_cap guard",
        "timing": "after deterministic next choice and column/vector materialization; before candidate and round commit",
        "math_and_choice_noninterference": True,
    },
    "semantic_diff": {
        "only_changed_frozen_literal": "support_cap: 100000 -> 200000",
        "all_other_frozen_fields_equal": same_keys,
    },
    "control_referee": {
        "lower_cap_control_necessary": False,
        "reason": "The static single-use theorem fixes the deterministic choice before the guard; a 100k control would nearly complete the round, then write a non-resumable hybrid clone rather than byte-equivalence evidence.",
    },
    "projection": {
        "current_support": 76616,
        "previous_growth": 43912,
        "ceil_growth_times_5_over_4": 54890,
        "conservative_next_support": 131506,
        "selected_cap": 200000,
        "margin": 68494,
        "classification": "resource projection, not a theorem",
    },
    "acceptance": {
        "fresh_clone_only": True,
        "exact_rounds": [1641],
        "round1642_absent": True,
        "status_reason": "INCOMPLETE_SEARCH_CAP/ROUND_CAP",
        "inherited_records_byte_identical": 4069711,
        "checkpoint_strict_descendant": True,
        "full_replay_target": 1,
        "full_replay_failures": 0,
        "atomic_watchdog_resource_gates": True,
        "independent_postrun_referee_required": True,
    },
    "fail_closed": {
        "SUPPORT_CAP": "quarantine hybrid zero-r1641 clone; never resume",
        "COLUMN_CAP": "zero-r1641 unchanged-input control only",
        "other": "no acceptance without separately audited exact atomic r1641 state",
    },
    "scope": {"metadata_only": True, "large_read": False, "clone": False, "launch": False},
}

(HERE / "results_support200k_design_audit.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps({"status": result["status"], "conservative_next_support": 131506}))
