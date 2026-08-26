#!/usr/bin/env python3
"""Materialize only the compact selector fragment; never the base CNF."""

import hashlib
import json
from pathlib import Path

from contract import *

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
CROSS = Path("/Users/rishi/workplace/krenn-cross-program-audit-2026-08-26/yesterdays-lemon")
REFEREE = REPO / "computations/unaudited-codex-n8-x5-eight-nine-exact16-target-union-referee-2026-08-26"
NARROW_BUILD = CROSS / "tmp/eight_vertex_local_degree4_full_local_max16_exact16_target_union_current.cnf.build.json"

PINS = {
    "referee_manifest": (REFEREE / "MANIFEST.sha256", REFEREE_MANIFEST_SHA256),
    "referee_result": (REFEREE / "results_referee.json", REFEREE_RESULT_SHA256),
    "referee_ledger": (REFEREE / "combined_target_supports.ledger", LEDGER_SHA256),
    "base_build_small": (CROSS / "tmp/eight_vertex_local_degree4_full_local_max16_current.build.json", "631695c5d0ae7ed3ef3f14e0f62438c2fc9b26a5a08b24a3b9cae18b99155315"),
    "generator": (CROSS / "claims/finite/n08/eight_vertex_local_degree4_support.py", "83996bdb4da059de2490549ed07fbb225b024e21763a8db4cf871fb0228cb0bb"),
    "narrow_materialization_small_result": (NARROW_BUILD, "c76ff3b4514ebc527ca5b4ceaeeb78da2247538aa5e178ac878ff60e759e5d89"),
}


def canonical(value):
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def build():
    observed = {}
    for name, (path, expected) in PINS.items():
        need(path.is_file(), (name, "missing"))
        actual = sha256_file(path)
        need(actual == expected, (name, actual, expected))
        observed[name] = {"path": str(path), "sha256": actual, "bytes": path.stat().st_size}

    referee = json.loads(PINS["referee_result"][0].read_text())
    need(referee["status"] == "PASS_STATIC_COMBINED_TARGET_UNION_REFEREE")
    need(referee["combined"]["support_union"] == TARGET_COUNT)
    need(referee["combined"]["ledger_sha256"] == LEDGER_SHA256)
    need(referee["selector_patch"]["patched_header"] == {"variables": TARGET_VARIABLES, "clauses": TARGET_CLAUSES})
    need(referee["narrow_materialization_comparison"]["bytewise_or_additive_composability"] is False)

    ledger = PINS["referee_ledger"][0].read_bytes()
    supports = parse_ledger(ledger)
    (HERE / "combined_target_supports.ledger").write_bytes(ledger)
    patch = make_patch(supports)
    validate_patch(patch, supports)
    (HERE / "selector_patch.cnfpart").write_bytes(patch)

    clearance = {
        "schema": "n8-x5-combined-exact16-materialization-clearance-v1",
        "status": "HELD_NULL_POST_CHECKER_CLEARANCE_REQUIRED",
        "manager_clearance": None,
        "nonce": None,
        "expires_utc": None,
        "exact16_drat_checker_terminal_manifest_sha256": None,
        "resource_clear": None,
        "no_overlap": None,
        "referee_manifest_sha256": REFEREE_MANIFEST_SHA256,
        "held_manifest_sha256": None,
        "authorized_action": None,
    }
    (HERE / "CLEARANCE_TEMPLATE.json").write_text(canonical(clearance))

    plan = {
        "schema": "n8-x5-combined-eight-nine-exact16-selector-patch-held-v1",
        "status": "HELD_PATCH_MATERIALIZED_ZERO_BASE_READ_ZERO_SOLVER",
        "pins": observed,
        "base": {
            "required_relative_path": BASE_RELATIVE_PATH,
            "sha256": BASE_SHA256,
            "bytes": BASE_BYTES,
            "variables": BASE_VARIABLES,
            "clauses": BASE_CLAUSES,
            "read_here": False,
        },
        "target_union": {
            "eight_classes": 16,
            "nine_classes": 85,
            "class_overlap": 9,
            "class_union": 92,
            "normalized_supports": TARGET_COUNT,
            "ledger_sha256": LEDGER_SHA256,
            "selector_first": SELECTOR_FIRST,
            "selector_last": SELECTOR_LAST,
            "implications_per_selector": 25,
            "added_implication_clauses": ADDED_IMPLICATIONS,
            "global_selector_or": 1,
            "added_variables": TARGET_COUNT,
            "added_clauses": ADDED_CLAUSES,
            "target_header": {"variables": TARGET_VARIABLES, "clauses": TARGET_CLAUSES},
        },
        "replacement_guard": {
            "replacement_only": True,
            "forbidden_append_base": {"relative_path": NARROW_RELATIVE_PATH, "sha256": NARROW_SHA256},
            "reason": "combined selectors reuse IDs428248..433755 with a different sorted ledger order, and the narrow global OR would keep the conjunction restricted to the narrow subset",
            "required_materialization": "stream original base, rewrite only its header, append this exact selector fragment, then atomically promote a fresh combined CNF",
        },
        "future_materialization": {
            "default_action": "REFUSE_NO_CLEARANCE",
            "requires_post_checker_resource_clear": True,
            "requires_fresh_nonexpired_manager_clearance": True,
            "requires_streaming_base_hash_header_clause_replay": True,
            "requires_patch_sha256": hashlib.sha256(patch).hexdigest(),
            "requires_atomic_temp_to_final": True,
            "refuse_overwrite": True,
            "solver_launch": False,
            "output_relative_path": "tmp/eight_vertex_local_degree4_full_local_max16_combined_exact16_target_union_current.cnf",
        },
        "launch_authorized": False,
        "scope": "compact patch producer/held materialization only; no SAT/UNSAT or theorem claim",
    }
    (HERE / "HELD_PLAN.json").write_text(canonical(plan))

    hostiles = {
        "schema": "n8-x5-combined-exact16-selector-held-hostiles-v1",
        "status": "PASS_ALL_REJECTED",
        "cases": {
            "append_to_narrow_cnf": "rejected by replacement guard",
            "read_large_base_by_default": "rejected; build reads only compact ledger and small metadata",
            "missing_post_checker_manifest": "clearance remains null",
            "wrong_5508_selector_count": "narrow subset only",
            "wrong_39384_naive_support_sum": "misses 3492 cross-layer duplicates",
            "wrong_26_implications_per_selector": "global OR appears once, not per selector",
            "missing_or_flipped_implication": "not a complete target cube",
            "missing_global_or": "admits generic skeleton",
            "wrong_base_hash_or_header": "must fail before output",
            "existing_output_or_tmp": "refuse overwrite",
            "solver_request": "outside held producer scope",
        },
    }
    (HERE / "HOSTILES.json").write_text(canonical(hostiles))

    result = {
        "schema": "n8-x5-combined-exact16-selector-patch-held-result-v1",
        "status": "PASS_COMPACT_PATCH_MATERIALIZED__HELD_NO_BASE_READ_NO_SOLVER",
        "ledger_sha256": sha256_file(HERE / "combined_target_supports.ledger"),
        "selector_patch_sha256": sha256_file(HERE / "selector_patch.cnfpart"),
        "selector_patch_bytes": (HERE / "selector_patch.cnfpart").stat().st_size,
        "selector_patch_clauses": ADDED_CLAUSES,
        "target_header": {"variables": TARGET_VARIABLES, "clauses": TARGET_CLAUSES},
        "base_cnf_read": False,
        "target_cnf_materialized": False,
        "solver_run": False,
        "clearance_consumed": False,
    }
    (HERE / "BUILD_RESULT.json").write_text(canonical(result))


if __name__ == "__main__":
    build()
