#!/usr/bin/env python3
"""Small replay of the sealed referee result and held solver contract."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
CROSS = Path("/Users/rishi/workplace/krenn-cross-program-audit-2026-08-26")
ROOT = CROSS / "yesterdays-lemon"


def need(value, detail="validation failure"):
    if not value:
        raise RuntimeError(detail)


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


result = json.loads((HERE / "MATERIALIZATION_REFEREE_RESULT.json").read_text())
plan = json.loads((HERE / "HELD_SOLVER_PLAN.json").read_text())
hostiles = json.loads((HERE / "HOSTILES.json").read_text())
clearance = json.loads((HERE / "CLEARANCE_TEMPLATE.json").read_text())

need(result["status"] == "PASS_EXACT_STREAM_COMPOSITION_SELECTOR_SEMANTICS_NO_SOLVER")
need(result["target"] == {"bytes": 244617151, "clauses": 3980473, "path": str(ROOT / "tmp/eight_vertex_local_degree4_full_local_max16_combined_exact16_target_union_current.cnf"), "sha256": "c96d4ac1ac70abd8bfcf3b2b7228a94963a8c0fc52c8a891e502122be857da12", "variables": 464139})
need(result["stream_derivation"] == {"base_body_lines_byte_identical": 3083172, "header_only_replaced": True, "patch_lines_byte_identical": 897301, "trailing_bytes": 0})
need(result["patch"]["selectors"] == 35892 and result["patch"]["implications_checked"] == 897300 and result["patch"]["global_or_checked"] is True)
need(result["semantic_coverage"] == {"every_selector_cube_checked": True, "generic_skeleton_excluded_by_global_or": True, "graph_class_intersection": 9, "graph_class_union": 92, "support_intersection": 3492, "support_union": 35892})
need(all(result["replacement_guard"][key] is True for key in ("original_base_required", "append_to_narrow_forbidden", "actual_target_is_fresh_replacement")))
need(hostiles["status"] == "PASS_ALL_REJECTED" and len(hostiles["cases"]) == 7)

need(plan["status"] == "HELD_ZERO_RUN_AWAITING_FRESH_MANAGER_CLEARANCE")
need(plan["launch_authorized"] is False and plan["solver_runs"] == 0)
need(plan["execution"]["lanes"] == 1 and plan["execution"]["sequential_only"] is True and plan["execution"]["no_relaunch"] is True)
need(plan["input"]["sha256"] == result["target"]["sha256"])
need(plan["input"]["materialization_referee_result_sha256"] == sha(HERE / "MATERIALIZATION_REFEREE_RESULT.json"))
need(plan["input"]["materialization_referee_manifest_sha256"] is None)
need(sha(plan["toolchain"]["cadical_path"]) == plan["toolchain"]["cadical_binary_sha256"])
need(sha(plan["toolchain"]["drat_trim_path"]) == plan["toolchain"]["drat_trim_binary_sha256"])
need(plan["terminal_contract"]["sat"]["required_exit"] == 10 and "all3980473 clauses" in plan["terminal_contract"]["sat"]["full_replay"])
need(plan["terminal_contract"]["unsat"]["required_exit"] == 20 and "s VERIFIED" in plan["terminal_contract"]["unsat"]["independent_replay"])

need(clearance["status"] == "HELD_MANAGER_CLEARANCE_NULL")
for field in ("manager_clearance", "authorized_action", "nonce", "issued_utc", "expires_utc", "resource_clear", "no_overlap", "fresh_process_census", "free_disk_kib", "materialization_referee_manifest_sha256"):
    need(clearance[field] is None, (field, "must remain null"))
need(clearance["materialization_referee_result_sha256"] == sha(HERE / "MATERIALIZATION_REFEREE_RESULT.json"))

target = ROOT / plan["input"]["path"]
need(target.stat().st_size == 244617151)
for relative in (plan["artifact_policy"]["solver_log"], plan["artifact_policy"]["proof"], plan["artifact_policy"]["checker_log"]):
    need(not (ROOT / relative).exists(), ("unexpected runtime artifact", relative))

print("PASS_COMBINED_EXACT16_MATERIALIZATION_REFEREE_AND_HELD_SOLVER_PLAN")
