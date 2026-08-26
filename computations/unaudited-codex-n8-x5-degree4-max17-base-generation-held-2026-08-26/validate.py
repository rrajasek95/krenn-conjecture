#!/usr/bin/env python3
"""Validate the zero-run max17 base-generation held plan."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def need(value, detail):
    if not value:
        raise RuntimeError(detail)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


plan = json.loads((HERE / "HELD_PLAN.json").read_text())
clearance = json.loads((HERE / "CLEARANCE_TEMPLATE.json").read_text())
hostiles = json.loads((HERE / "results_hostiles.json").read_text())
result = json.loads((HERE / "results_held.json").read_text())

need(plan["status"] == "HELD_ZERO_RUN_EXACT16_LANE_ACTIVE", "plan status")
need(plan["scope"] == {
    "center_degree": 4,
    "degree_five_plane": False,
    "maximum_edges": 17,
    "minimum_degree": 0,
    "n": 8,
    "necessary_conditions_only": True,
    "write_only": True,
}, "scope")
need(plan["exact_cli_delta_from_max16"]["semantic_option_differences"] == [
    {"from": 16, "option": "--maximum-edges", "to": 17}
], "CLI delta")
need(plan["exact_cli_delta_from_max16"]["all_other_options_identical"] is True, "other options")

audit = plan["static_source_audit"]
need(audit["allowed_block_literals"] == 25, "block count")
need(audit["block_variables"] == {"first": 226, "last": 250}, "block vars")
need(audit["sinz_bound16"] == {"variables": 384, "clauses": 776}, "counter16")
need(audit["sinz_bound17"] == {"variables": 408, "clauses": 823}, "counter17")
need(audit["derived_delta"] == {"variables": 24, "clauses": 47}, "delta")
need(audit["expected_max17_base_header"] == {"variables": 428271, "clauses": 3083219}, "base header")

need(clearance["status"] == "HELD_NULL_NO_LAUNCH", "clearance status")
for key in (
    "manager_clearance", "nonce", "issued_utc", "expires_utc",
    "exact16_lane_terminal_resource_clear_manifest_sha256",
    "independent_runner_referee_manifest_sha256", "fresh_process_census",
    "free_disk_kib", "output_paths_absent",
):
    need(clearance[key] is None, (key, "must remain null"))
need(clearance["minimum_free_disk_kib"] == 33554432, "disk floor")

need(plan["resource_gate"]["rss_cap_bytes"] == 8589934592, "RSS")
need(plan["resource_gate"]["outer_wall_cap_seconds"] == 150, "wall")
need(plan["mandatory_post_generation_referee"]["required_before_patch_or_solve"] is True, "referee")
need(plan["mandatory_post_generation_referee"]["manifest_sha256"] is None, "referee must be absent")
need(plan["downstream_exact17_patch"] == {
    "added_clauses": 454501,
    "added_variables": 18180,
    "conditional_expected_patched_header": {"clauses": 3537720, "variables": 446451},
    "ledger_sha256": "f280c2b3223a9673c80d2aa7bfed7f97c0558fbc2dcb80f4ecac88f16c4b9dd8",
    "materialization_status": "FORBIDDEN_UNTIL_BASE_REFEREE_AND_SEPARATE_CLEARANCE",
    "solve_status": "FORBIDDEN",
    "support_masks": 18180,
}, "downstream patch")
need(all(value is False for value in plan["zero_run_evidence"].values()), "zero run")

need(hostiles["status"] == "PASS_ALL_REJECTED", "hostiles")
need("minimum-degree0" in hostiles["cases"]["reuse_old_minimum_degree3_max17_contract"], "minimum degree hostile")
need("non-atomic" in hostiles["cases"]["direct_final_path_write"], "atomic hostile")
need(result["status"] == "PASS_STATIC_HELD_ZERO_RUN__NO_CLEARANCE" and result["zero_run"] is True, "result")
need(result["plan_sha256"] == digest(HERE / "HELD_PLAN.json"), "plan hash")
need(result["clearance_template_sha256"] == digest(HERE / "CLEARANCE_TEMPLATE.json"), "clearance hash")
need(result["hostiles_sha256"] == digest(HERE / "results_hostiles.json"), "hostiles hash")

for suffix in (".cnf", ".drat", ".proof", ".log", ".tmp"):
    need(not any(path.name.endswith(suffix) for path in HERE.iterdir()), ("unexpected runtime artifact", suffix))

print("PASS max17 base-generation held-plan replay; zero run")
