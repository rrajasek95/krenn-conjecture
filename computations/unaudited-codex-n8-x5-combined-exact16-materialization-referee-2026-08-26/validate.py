#!/usr/bin/env python3
"""Small-artifact replay for the sealed materialization referee and held solver plan."""

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
MATERIALIZER = Path("/Users/rishi/workplace/krenn-conjecture/computations/unaudited-codex-n8-x5-combined-exact16-streaming-materializer-held-2026-08-26")
CROSS = Path("/Users/rishi/workplace/krenn-cross-program-audit-2026-08-26/yesterdays-lemon")
OUTPUT = CROSS / "tmp/eight_vertex_local_degree4_full_local_max16_combined_exact16_target_union_current.cnf"
BUILD = Path(str(OUTPUT) + ".build.json")


def need(value, detail):
    if not value:
        raise RuntimeError(detail)


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


result = json.loads((HERE / "results_referee.json").read_text())
plan = json.loads((HERE / "HELD_SOLVER_PLAN.json").read_text())
template = json.loads((HERE / "SOLVER_CLEARANCE_TEMPLATE.json").read_text())
schema = json.loads((HERE / "SOLVER_CLEARANCE.schema.json").read_text())
producer_plan = json.loads((MATERIALIZER / "HELD_PLAN.json").read_text())
producer_validator = (MATERIALIZER / "validate.py").read_text()
build = json.loads(BUILD.read_text())

need(result["status"] == "PASS_EXACT_STREAM_DERIVATION_HELD_NO_SOLVER", "result status")
need(result["scope"] == "materialization correctness and held solver contract only; no SAT/UNSAT theorem claim", "scope")
need(result["dependencies"]["exact16_terminal_manifest_sha256"] == "bcd2cc5f92bd2ddb7e52decfc65b68e430b2312281d5b1d181fa639c35d6416e", "terminal binding")
need(result["dependencies"]["materializer_manifest_sha256"] == "cf720d0e1d8516f9f5a942be72bc20de5e14104eb9832607472385f7c9733f37", "materializer binding")
need(result["dependencies"]["clearance_sha256"] == "477098f5fb987dba245da3ff2db0ec994c6e33da17e9fa5b32209027bb1419e9", "clearance binding")
need(result["patch"] == {
    "bytes": 13136474,
    "clauses": 897301,
    "global_or_clauses": 1,
    "implications_per_support": 25,
    "semantic_replay": "PASS_BYTE_EXACT_ALL_IMPLICATIONS_AND_GLOBAL_OR",
    "sha256": "2ac0e05c9599f09066fc6b0bdd5812ac78e85328ec3928ef3f3f6498e7af2059",
    "supports": 35892,
}, "patch replay")
need(result["output"] == {
    "bytes": 244617151,
    "clauses": 3980473,
    "maximum_variable_replayed": 464139,
    "sha256": "c96d4ac1ac70abd8bfcf3b2b7228a94963a8c0fc52c8a891e502122be857da12",
    "variables": 464139,
}, "output replay")
need(result["derivation"] == {
    "all_dimacs_clause_lines_replayed": 3980473,
    "header_replacement_only": True,
    "original_base_body_byte_identical": True,
    "patch_suffix_byte_identical": True,
    "trailing_bytes": 0,
}, "derivation")
need(result["runtime"] == {"solver_plan_held": True, "solver_runs": 0}, "zero solver")

zero_run = producer_plan["zero_run"]
need(set(zero_run) == {"clearance_consumed", "large_base_read", "solver_run", "target_materialized"}, "zero-run key census")
need(all(value is False for value in zero_run.values()), "zero-run values")
for key in zero_run:
    hostile = dict(zero_run)
    hostile[key] = True
    need(not all(value is False for value in hostile.values()), ("validator hostile", key))
need('all(value is False for value in plan["zero_run"].values())' in producer_validator, "validator fix source")
need('target unexpectedly materialized' in producer_validator, "terminal separation")
need(result["validator_fix"]["single_true_hostiles_rejected"] == 4, "validator hostile result")

need(sha256(HERE / "results_referee.json") == "3252bf5d73b35eae9996d12dc811f8466c657e57666f560b979fb17a2616f36f", "result hash")
need(plan["status"] == "HELD_ZERO_RUN_AWAITING_FRESH_MANAGER_CLEARANCE", "plan held")
need(plan["launch_authorized"] is False and plan["solver_runs"] == 0, "plan zero run")
need(plan["input"] == {
    "bytes": 244617151,
    "clauses": 3980473,
    "path": "tmp/eight_vertex_local_degree4_full_local_max16_combined_exact16_target_union_current.cnf",
    "sha256": "c96d4ac1ac70abd8bfcf3b2b7228a94963a8c0fc52c8a891e502122be857da12",
    "target_class_union": {"eight_classes": 16, "nine_classes": 85, "overlap": 9, "union": 92},
    "target_supports": 35892,
    "variables": 464139,
}, "solver input")
execution = plan["execution"]
need((execution["cadical_wall_cap_seconds"], execution["cadical_rss_cap_bytes"]) == (7200, 17179869184), "solver gates")
need(execution["lanes"] == 1 and execution["no_relaunch"] is True and execution["fresh_input_rehash_required"] is True, "one lane")
need(plan["toolchain"]["cadical_binary_sha256"] == "379aee3d6c61ba729f051584e96db71b7f444f0d4016ef6072f87e4b554f858e", "cadical pin")
need(plan["toolchain"]["drat_trim_binary_sha256"] == "f58f63b0f76945d4c4c9ff6e87afaf870f579e67c0f7cca589492df8fc7ebd47", "drat pin")
need(sha256(plan["toolchain"]["cadical_path"]) == plan["toolchain"]["cadical_binary_sha256"], "cadical replay")
need(sha256(plan["toolchain"]["drat_trim_path"]) == plan["toolchain"]["drat_trim_binary_sha256"], "drat replay")
need(template["status"] == "HELD_MANAGER_CLEARANCE_NULL", "clearance held")
need(all(template[key] is None for key in template if key not in {"schema", "status"}), "clearance null")
need(schema["additionalProperties"] is False and schema["properties"]["fresh_input_sha256"]["const"] == result["output"]["sha256"], "clearance schema")

need(OUTPUT.is_file() and OUTPUT.stat().st_size == 244617151, "materialized output stat")
need(build["output_sha256"] == result["output"]["sha256"] and build["solver_run"] is False, "build result")
need(not (CROSS / plan["artifact_policy"]["solver_log"]).exists(), "solver log exists")
need(not (CROSS / plan["artifact_policy"]["proof"]).exists(), "proof exists")
need(not (CROSS / plan["artifact_policy"]["checker_log"]).exists(), "checker log exists")

print("PASS combined exact16 materialization referee and held solver plan")
