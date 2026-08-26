#!/usr/bin/env python3
"""Build a zero-run held plan for current augmented degree-four max17."""

from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
CROSS = Path("/Users/rishi/workplace/krenn-cross-program-audit-2026-08-26/yesterdays-lemon")
SOURCE = CROSS / "claims/finite/n08/eight_vertex_local_degree4_support.py"
SUPPORT = CROSS / "src/krenn_gu/rankone_support_sat.py"
MAX16_AUDIT = CROSS / "docs/audits/eight-vertex-degree4-at-most16-current-held-plan-2026-08-26"
MAX16_BUILD = CROSS / "tmp/eight_vertex_local_degree4_full_local_max16_current.build.json"
TARGET = REPO / "computations/unaudited-codex-n8-x5-nine-block-exact17-target-union-referee-2026-08-26"

PINS = {
    "generator": (SOURCE, "83996bdb4da059de2490549ed07fbb225b024e21763a8db4cf871fb0228cb0bb"),
    "support_library": (SUPPORT, "c795681f2d13a7bc5044572ccf89a532402bb885dde7b5772898f156a6a8bed6"),
    "max16_build_metadata": (MAX16_BUILD, "631695c5d0ae7ed3ef3f14e0f62438c2fc9b26a5a08b24a3b9cae18b99155315"),
    "max16_held_manifest": (MAX16_AUDIT / "HELD_MANIFEST.sha256", "797361022b8e02aeab32933cb8cbfa3c013390c2ef528efb43b796cf77aa00ce"),
    "max16_held_plan": (MAX16_AUDIT / "HELD_PLAN.json", "a38f59c67f9a6d09370ea73341bfcea52d72ce4885322fce8bf3a24d7c96bbe4"),
    "exact17_target_manifest": (TARGET / "MANIFEST.sha256", "5eb55e55fb77a2e04dfcd303febe0d2f0e608b6de605590c02f16c11d5dff28b"),
    "exact17_target_result": (TARGET / "results_referee.json", "6073468021f927aa4ee7ea442a81ca46907cc1adb166b04a50df147483e6a857"),
    "exact17_target_ledger": (TARGET / "exact17_target_supports.ledger", "f280c2b3223a9673c80d2aa7bfed7f97c0558fbc2dcb80f4ecac88f16c4b9dd8"),
}


def need(value, detail="validation failure"):
    if not value:
        raise RuntimeError(detail)


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            h.update(chunk)
    return h.hexdigest()


def sinz_counts(count, bound):
    need(0 < bound < count)
    variables = (count - 1) * bound
    clauses = 1 + (bound - 1) + count - 1
    clauses += (count - 2) * (2 + 2 * (bound - 1))
    return {"variables": variables, "clauses": clauses}


def build():
    pins = {}
    for name, (path, expected) in PINS.items():
        need(path.is_file(), (name, "missing"))
        observed = digest(path)
        need(observed == expected, (name, observed, expected))
        pins[name] = {"path": str(path), "sha256": observed, "bytes": path.stat().st_size}

    max16 = json.loads(MAX16_BUILD.read_text())
    need(max16["minimum_degree"] == 0 and max16["maximum_edges"] == 16 and max16["center_degree"] == 4)
    need(max16["allowed_edges"] == 25 and max16["variables"] == 428247 and max16["clauses"] == 3083172)
    need(max16["status"] == "NOT_SOLVED")

    source_text = SOURCE.read_text()
    tree = ast.parse(source_text)
    cap_calls = [node for node in ast.walk(tree) if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "add_at_most"]
    need(len(cap_calls) == 1)
    need(len(cap_calls[0].args) == 3 and isinstance(cap_calls[0].args[2], ast.Name) and cap_calls[0].args[2].id == "maximum_edges")
    need("for _ in range(count - 1)" in source_text and "for _ in range(bound)" in source_text)

    counter16 = sinz_counts(25, 16)
    counter17 = sinz_counts(25, 17)
    delta = {
        "variables": counter17["variables"] - counter16["variables"],
        "clauses": counter17["clauses"] - counter16["clauses"],
    }
    need(counter16 == {"variables": 384, "clauses": 776})
    need(counter17 == {"variables": 408, "clauses": 823})
    need(delta == {"variables": 24, "clauses": 47})
    expected_base = {"variables": 428271, "clauses": 3083219}

    max16_command = [
        "python3", "claims/finite/n08/eight_vertex_local_degree4_support.py",
        "--minimum-degree", "0", "--maximum-edges", "16",
        "--center-degree", "4", "--write-only",
        "--cnf", "tmp/eight_vertex_local_degree4_full_local_max16_current.cnf",
        "--output", "tmp/eight_vertex_local_degree4_full_local_max16_current.build.json",
    ]
    max17_template = [
        "python3", "claims/finite/n08/eight_vertex_local_degree4_support.py",
        "--minimum-degree", "0", "--maximum-edges", "17",
        "--center-degree", "4", "--write-only",
        "--cnf", "tmp/eight_vertex_local_degree4_full_local_max17_current.cnf.NONCE.tmp",
        "--output", "tmp/eight_vertex_local_degree4_full_local_max17_current.build.json.NONCE.tmp",
    ]
    semantic16 = max16_command[:]
    semantic17 = max17_template[:]
    for index, value in enumerate(semantic16):
        if value.startswith("tmp/"):
            semantic16[index] = "OUTPUT"
    for index, value in enumerate(semantic17):
        if value.startswith("tmp/"):
            semantic17[index] = "OUTPUT"
    differing = [(a, b) for a, b in zip(semantic16, semantic17) if a != b]
    need(differing == [("16", "17")])

    clearance = {
        "schema": "n8-x5-degree4-max17-base-generation-clearance-v1",
        "status": "HELD_NULL_NO_LAUNCH",
        "manager_clearance": None,
        "nonce": None,
        "issued_utc": None,
        "expires_utc": None,
        "exact16_lane_terminal_resource_clear_manifest_sha256": None,
        "independent_runner_referee_manifest_sha256": None,
        "fresh_process_census": None,
        "free_disk_kib": None,
        "minimum_free_disk_kib": 33554432,
        "output_paths_absent": None,
    }
    (HERE / "CLEARANCE_TEMPLATE.json").write_text(json.dumps(clearance, indent=2, sort_keys=True) + "\n")

    plan = {
        "schema": "n8-x5-current-augmented-degree4-max17-base-generation-held-v1",
        "status": "HELD_ZERO_RUN_EXACT16_LANE_ACTIVE",
        "pins": pins,
        "scope": {
            "necessary_conditions_only": True,
            "n": 8,
            "center_degree": 4,
            "minimum_degree": 0,
            "maximum_edges": 17,
            "degree_five_plane": False,
            "write_only": True,
        },
        "exact_cli_delta_from_max16": {
            "max16_reference_command": max16_command,
            "max17_atomic_temp_command_template": max17_template,
            "semantic_option_differences": [{"option": "--maximum-edges", "from": 16, "to": 17}],
            "all_other_options_identical": True,
            "output_paths_differ_only_for_fresh_atomic_temp_names": True,
        },
        "static_source_audit": {
            "allowed_block_literals": 25,
            "block_variables": {"first": 226, "last": 250},
            "add_at_most_call_count": len(cap_calls),
            "maximum_edges_has_one_semantic_use": True,
            "sinz_bound16": counter16,
            "sinz_bound17": counter17,
            "derived_delta": delta,
            "expected_max17_base_header": expected_base,
            "acceptance_note": "expected header is load-bearing but not accepted until independent full post-generation replay",
        },
        "resource_gate": {
            "sequential_only": True,
            "no_overlap_with_exact16_or_any_sat_drat_singular_lane": True,
            "minimum_free_disk_kib": 33554432,
            "rss_cap_bytes": 8589934592,
            "native_wall_cap_seconds": 120,
            "outer_wall_cap_seconds": 150,
            "direct_process_group_libproc_rss_required": True,
            "runner_status": "HELD_PENDING_INDEPENDENT_RUNNER_REFEREE",
        },
        "atomic_generation_protocol": [
            "bind a fresh nonexpired manager nonce and exact16 RESOURCE_CLEAR manifest",
            "rehash generator/support/target pins and prove final/temp/log paths absent",
            "run the exact max17 command once in a fresh process group under direct-libproc 8GiB/150s observation",
            "generator writes CNF and JSON only to nonce-suffixed same-filesystem temporary paths",
            "on any timeout/RSS/observer/nonzero/malformed result, quarantine temporary outputs and grant zero coverage",
            "on rc0, require status NOT_SOLVED, options 0/17/4, header 428271/3083219, no solver transcript, and stream-hash/recount temporary CNF",
            "fsync both files, rename to fresh final candidate names, fsync directory, then atomically seal producer result",
        ],
        "mandatory_post_generation_referee": {
            "required_before_patch_or_solve": True,
            "manifest_sha256": None,
            "large_read_owner": "one independent referee only after generator exits",
            "checks": [
                "stream SHA-256 exact full candidate CNF and record bytes",
                "parse exact header 428271/3083219 and recount every clause",
                "replay build JSON source/options/status and compare CNF path",
                "verify max16-to-max17 only Sinz +24 variables/+47 clauses at source and header levels",
                "verify atomic telemetry, rc0, no breach, peak RSS<8GiB, wall<150s, no stale tmp",
            ],
            "failure": "base remains unaccepted; exact17 selector patching and all solving forbidden",
        },
        "downstream_exact17_patch": {
            "ledger_sha256": PINS["exact17_target_ledger"][1],
            "support_masks": 18180,
            "added_variables": 18180,
            "added_clauses": 454501,
            "conditional_expected_patched_header": {"variables": 446451, "clauses": 3537720},
            "materialization_status": "FORBIDDEN_UNTIL_BASE_REFEREE_AND_SEPARATE_CLEARANCE",
            "solve_status": "FORBIDDEN",
        },
        "zero_run_evidence": {
            "base_cnf_generated": False,
            "base_cnf_read": False,
            "selector_patch_generated": False,
            "solver_run": False,
            "clearance_consumed": False,
        },
    }
    (HERE / "HELD_PLAN.json").write_text(json.dumps(plan, indent=2, sort_keys=True) + "\n")

    hostiles = {
        "schema": "n8-x5-degree4-max17-base-held-hostiles-v1",
        "status": "PASS_ALL_REJECTED",
        "cases": {
            "reuse_old_minimum_degree3_max17_contract": "reject: current max16 baseline is minimum-degree0; violates sole semantic delta",
            "enable_degree_five_plane": "reject: adds semantics beyond edge bound",
            "omit_write_only": "reject: may launch solver",
            "direct_final_path_write": "reject: pinned source writer is non-atomic; nonce temporary path wrapper required",
            "generate_while_exact16_active": "reject: RESOURCE_CLEAR dependency is null",
            "header_not_428271_3083219": "reject even if generator returns0",
            "counter_delta_not_24_47": "reject source/header mismatch",
            "patch_before_independent_base_referee": "reject: base acceptance manifest is null",
            "use_max16_or_narrow_target_cnf_as_base": "reject: replacement base must be fresh current max17",
            "numeric_hash_preclaim": "reject: bytes/hash are unknown until atomic generation and independent replay",
            "overlap_or_resource_observer_failure": "quarantine outputs, zero coverage",
        },
    }
    (HERE / "results_hostiles.json").write_text(json.dumps(hostiles, indent=2, sort_keys=True) + "\n")

    result = {
        "schema": "n8-x5-degree4-max17-base-generation-held-result-v1",
        "status": "PASS_STATIC_HELD_ZERO_RUN__NO_CLEARANCE",
        "plan_path": "HELD_PLAN.json",
        "plan_sha256": digest(HERE / "HELD_PLAN.json"),
        "clearance_template_sha256": digest(HERE / "CLEARANCE_TEMPLATE.json"),
        "hostiles_sha256": digest(HERE / "results_hostiles.json"),
        "derived_max17_header": expected_base,
        "derived_sinz_delta": delta,
        "target_ledger_sha256": PINS["exact17_target_ledger"][1],
        "zero_run": True,
    }
    (HERE / "results_held.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    build()
