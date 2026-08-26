#!/usr/bin/env python3
"""Replay the compact combined selector patch held package."""

import hashlib
import json
from pathlib import Path

from contract import *

HERE = Path(__file__).resolve().parent
CROSS = Path("/Users/rishi/workplace/krenn-cross-program-audit-2026-08-26/yesterdays-lemon")
PATCH_SHA = "2ac0e05c9599f09066fc6b0bdd5812ac78e85328ec3928ef3f3f6498e7af2059"

ledger = (HERE / "combined_target_supports.ledger").read_bytes()
supports = parse_ledger(ledger)
patch = (HERE / "selector_patch.cnfpart").read_bytes()
validate_patch(patch, supports)
need(hashlib.sha256(patch).hexdigest() == PATCH_SHA, "patch hash")
need(len(patch) == 13136474, "patch bytes")

plan = json.loads((HERE / "HELD_PLAN.json").read_text())
result = json.loads((HERE / "BUILD_RESULT.json").read_text())
clearance = json.loads((HERE / "CLEARANCE_TEMPLATE.json").read_text())
hostiles = json.loads((HERE / "HOSTILES.json").read_text())

need(plan["status"] == "HELD_PATCH_MATERIALIZED_ZERO_BASE_READ_ZERO_SOLVER", "status")
need(plan["base"] == {
    "bytes": 231480677,
    "clauses": 3083172,
    "read_here": False,
    "required_relative_path": BASE_RELATIVE_PATH,
    "sha256": BASE_SHA256,
    "variables": 428247,
}, "base")
target = plan["target_union"]
need((target["eight_classes"], target["nine_classes"], target["class_overlap"], target["class_union"]) == (16, 85, 9, 92), "classes")
need(target["normalized_supports"] == 35892, "supports")
need(target["selector_first"] == 428248 and target["selector_last"] == 464139, "selectors")
need(target["implications_per_selector"] == 25 and target["added_implication_clauses"] == 897300, "implications")
need(target["global_selector_or"] == 1 and target["added_clauses"] == 897301, "clauses")
need(target["target_header"] == {"variables": 464139, "clauses": 3980473}, "header")

guard = plan["replacement_guard"]
need(guard["replacement_only"] is True, "replacement")
need(guard["forbidden_append_base"] == {"relative_path": NARROW_RELATIVE_PATH, "sha256": NARROW_SHA256}, "narrow guard")
need("reuse IDs428248..433755" in guard["reason"], "alias explanation")
need(plan["launch_authorized"] is False and plan["future_materialization"]["solver_launch"] is False, "launch")
need(plan["future_materialization"]["requires_patch_sha256"] == PATCH_SHA, "future patch pin")

need(clearance["status"] == "HELD_NULL_POST_CHECKER_CLEARANCE_REQUIRED", "clearance")
for field in ("manager_clearance", "nonce", "expires_utc", "exact16_drat_checker_terminal_manifest_sha256", "resource_clear", "no_overlap", "held_manifest_sha256", "authorized_action"):
    need(clearance[field] is None, (field, "must be null"))
need(clearance["referee_manifest_sha256"] == REFEREE_MANIFEST_SHA256, "referee clearance pin")

need(result == {
    "base_cnf_read": False,
    "clearance_consumed": False,
    "ledger_sha256": LEDGER_SHA256,
    "schema": "n8-x5-combined-exact16-selector-patch-held-result-v1",
    "selector_patch_bytes": 13136474,
    "selector_patch_clauses": 897301,
    "selector_patch_sha256": PATCH_SHA,
    "solver_run": False,
    "status": "PASS_COMPACT_PATCH_MATERIALIZED__HELD_NO_BASE_READ_NO_SOLVER",
    "target_cnf_materialized": False,
    "target_header": {"clauses": 3980473, "variables": 464139},
}, "result")
need(hostiles["status"] == "PASS_ALL_REJECTED", "hostiles")
need("replacement guard" in hostiles["cases"]["append_to_narrow_cnf"], "append hostile")

full_output = CROSS / plan["future_materialization"]["output_relative_path"]
need(not full_output.exists(), ("unexpected full output", str(full_output)))
need(not any(path.suffix in {".cnf", ".drat", ".proof"} for path in HERE.iterdir()), "unexpected runtime artifact")

# Exact byte equality must reject a missing clause and a flipped literal.
for bad in (patch[:-1], b"1" + patch[1:]):
    try:
        validate_patch(bad, supports)
    except RuntimeError:
        pass
    else:
        raise RuntimeError("patch hostile accepted")

print("PASS combined exact16 compact selector patch held replay")
