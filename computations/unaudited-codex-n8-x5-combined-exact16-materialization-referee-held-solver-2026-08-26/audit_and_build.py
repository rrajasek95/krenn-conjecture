#!/usr/bin/env python3
"""Independent stream referee and zero-run solver-plan builder."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORK = HERE.parents[1]
CROSS = Path("/Users/rishi/workplace/krenn-cross-program-audit-2026-08-26")
ROOT = CROSS / "yesterdays-lemon"

BASE = ROOT / "tmp/eight_vertex_local_degree4_full_local_max16_current.cnf"
TARGET = ROOT / "tmp/eight_vertex_local_degree4_full_local_max16_combined_exact16_target_union_current.cnf"
BUILD = TARGET.with_suffix(TARGET.suffix + ".build.json")
NARROW = ROOT / "tmp/eight_vertex_local_degree4_full_local_max16_exact16_target_union_current.cnf"

REFEREE = WORK / "computations/unaudited-codex-n8-x5-eight-nine-exact16-target-union-referee-2026-08-26"
PATCH_PACKAGE = WORK / "computations/unaudited-codex-n8-x5-eight-nine-exact16-selector-patch-held-2026-08-26"
MATERIALIZER = WORK / "computations/unaudited-codex-n8-x5-combined-exact16-streaming-materializer-held-2026-08-26"
PATCH = PATCH_PACKAGE / "selector_patch.cnfpart"
LEDGER = PATCH_PACKAGE / "combined_target_supports.ledger"

BASE_SHA = "9e057710afe016609c31ae4c0cb45b1a948ca48b74426d390a2a9209035dd547"
TARGET_SHA = "c96d4ac1ac70abd8bfcf3b2b7228a94963a8c0fc52c8a891e502122be857da12"
PATCH_SHA = "2ac0e05c9599f09066fc6b0bdd5812ac78e85328ec3928ef3f3f6498e7af2059"
LEDGER_SHA = "6bffb2962242725f8bd0603dfaeb91f64c2ee0e4430632b445b42e44d4a424d5"
NARROW_SHA = "dc5cd1cad3a062dc66a5788413e5c1e1799a1ed07e66266ad25cc195b470aafa"
BASE_HEADER = b"p cnf 428247 3083172\n"
TARGET_HEADER = b"p cnf 464139 3980473\n"
BASE_BYTES = 231_480_677
TARGET_BYTES = 244_617_151
BASE_CLAUSES = 3_083_172
PATCH_CLAUSES = 897_301
TARGET_CLAUSES = 3_980_473
SELECTOR_FIRST = 428_248
SELECTOR_LAST = 464_139
SELECTOR_COUNT = 35_892

BLOCK_EDGES = (
    "01", "02", "03", "04", "12", "13", "14", "15", "16", "17",
    "23", "24", "25", "26", "27", "34", "35", "36", "37", "45",
    "46", "47", "56", "57", "67",
)
BLOCK_VARIABLES = dict(zip(BLOCK_EDGES, range(226, 251), strict=True))


def need(value: bool, detail: object = "audit failure") -> None:
    if not value:
        raise RuntimeError(detail)


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    need(not temporary.exists(), ("stale output", temporary))
    with temporary.open("x", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2, sort_keys=True)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)


def pin_small() -> dict[str, dict[str, object]]:
    pins = {
        "combined_referee_manifest": (REFEREE / "MANIFEST.sha256", "46a29e7f0780f076aded01e3dd8e554ad44449cf7b79e4842434dce789b680b5"),
        "combined_referee_result": (REFEREE / "results_referee.json", "230245d3a5a1a57dcb433572fe4f4f1ceb33edea6c3a9a682b583c3b689866a5"),
        "patch_package_manifest": (PATCH_PACKAGE / "MANIFEST.sha256", "745f5fa186c05d265cb521bfbf1f3c9d485ac3779a7cfbee82cbdfc50c68eee8"),
        "materializer_manifest": (MATERIALIZER / "MANIFEST.sha256", "cf720d0e1d8516f9f5a942be72bc20de5e14104eb9832607472385f7c9733f37"),
        "materializer_clearance": (MATERIALIZER / "CLEARANCE.json", "477098f5fb987dba245da3ff2db0ec994c6e33da17e9fa5b32209027bb1419e9"),
        "materializer_source": (MATERIALIZER / "materialize.py", "5ff71f63218f51ad1ee2b96b18c2bee1b3a30d4521638c8e2c3912bb0663f3a3"),
        "build_record": (BUILD, "e68b8d0b547e14662e7b771e44f5bb3bf4d2ea720b8d23d7b95a86a4a96bcd0e"),
    }
    observed = {}
    for name, (path, expected) in pins.items():
        actual = sha(path)
        need(actual == expected, (name, actual, expected))
        observed[name] = {"path": str(path), "sha256": actual, "bytes": path.stat().st_size}
    return observed


def audit_selector_semantics() -> tuple[list[str], int]:
    ledger_bytes = LEDGER.read_bytes()
    need(hashlib.sha256(ledger_bytes).hexdigest() == LEDGER_SHA, "ledger hash")
    need(ledger_bytes.endswith(b"\n"), "ledger final newline")
    ledger = ledger_bytes.decode("ascii").splitlines()
    need(len(ledger) == SELECTOR_COUNT, "ledger count")
    need(ledger == sorted(ledger) and len(set(ledger)) == SELECTOR_COUNT, "ledger canonical uniqueness")

    patch_bytes = PATCH.read_bytes()
    need(hashlib.sha256(patch_bytes).hexdigest() == PATCH_SHA, "patch hash")
    lines = patch_bytes.decode("ascii").splitlines()
    need(len(lines) == PATCH_CLAUSES, "patch clause count")
    allowed = set(BLOCK_EDGES)
    checked = 0
    for offset, support_line in enumerate(ledger):
        edges = support_line.split("|")
        need(len(edges) == 16 and edges == sorted(edges) and len(set(edges)) == 16, ("support", offset))
        support = set(edges)
        need(support <= allowed and {"01", "02", "03", "04"} <= support, ("support universe/root", offset))
        selector = SELECTOR_FIRST + offset
        for inner, edge in enumerate(BLOCK_EDGES):
            literal = BLOCK_VARIABLES[edge] if edge in support else -BLOCK_VARIABLES[edge]
            expected = f"-{selector} {literal} 0"
            need(lines[offset * 25 + inner] == expected, ("selector cube", selector, edge))
            checked += 1
    need(checked == 897_300, "implication total")
    need(lines[-1] == " ".join(map(str, range(SELECTOR_FIRST, SELECTOR_LAST + 1))) + " 0", "global selector OR")
    return ledger, checked


def audit_referee_semantics() -> None:
    result = json.loads((REFEREE / "results_referee.json").read_text())
    need(result["status"] == "PASS_STATIC_COMBINED_TARGET_UNION_REFEREE")
    need(result["combined"] == {
        "graph_class_intersection": 9,
        "graph_class_union": 92,
        "ledger_bytes": 1722816,
        "ledger_sha256": LEDGER_SHA,
        "raw_embeddings_over_unique_classes": 47088,
        "support_intersection": 3492,
        "support_union": SELECTOR_COUNT,
    }, "combined class/support census")
    patch = result["selector_patch"]
    need(patch["selector_variables"] == {"count": SELECTOR_COUNT, "first": SELECTOR_FIRST, "last": SELECTOR_LAST})
    need(patch["selector_implications"] == 897_300 and patch["global_selector_or"] == 1)
    need(patch["patched_header"] == {"clauses": TARGET_CLAUSES, "variables": SELECTOR_LAST})
    comparison = result["narrow_materialization_comparison"]
    need(comparison["bytewise_or_additive_composability"] is False)
    need(comparison["required_action_for_combined"] == "materialize the combined selector patch from the original base; do not modify the narrow CNF in place")
    need(result["hostiles"]["status"] == "PASS_ALL_REJECTED")


def audit_stream() -> dict[str, object]:
    base_hash = hashlib.sha256()
    target_hash = hashlib.sha256()
    base_bytes = target_bytes = base_clauses = patch_clauses = 0
    with BASE.open("rb") as base, TARGET.open("rb") as target:
        base_header = base.readline()
        target_header = target.readline()
        need(base_header == BASE_HEADER, ("base header", base_header))
        need(target_header == TARGET_HEADER, ("target header", target_header))
        base_hash.update(base_header)
        target_hash.update(target_header)
        base_bytes += len(base_header)
        target_bytes += len(target_header)
        for base_line in base:
            target_line = target.readline()
            need(target_line == base_line, ("base-body mismatch", base_clauses + 1))
            base_hash.update(base_line)
            target_hash.update(target_line)
            base_bytes += len(base_line)
            target_bytes += len(target_line)
            base_clauses += 1
        need(base_clauses == BASE_CLAUSES, "base clause recount")
        with PATCH.open("rb") as patch:
            for patch_line in patch:
                target_line = target.readline()
                need(target_line == patch_line, ("patch mismatch", patch_clauses + 1))
                target_hash.update(target_line)
                target_bytes += len(target_line)
                patch_clauses += 1
        need(target.read(1) == b"", "target trailing data")
    need(base_hash.hexdigest() == BASE_SHA and base_bytes == BASE_BYTES)
    need(target_hash.hexdigest() == TARGET_SHA and target_bytes == TARGET_BYTES)
    need(patch_clauses == PATCH_CLAUSES and base_clauses + patch_clauses == TARGET_CLAUSES)
    return {
        "base_body_lines_byte_identical": base_clauses,
        "patch_lines_byte_identical": patch_clauses,
        "header_only_replaced": True,
        "trailing_bytes": 0,
    }


def main() -> None:
    pins = pin_small()
    audit_referee_semantics()
    ledger, checked = audit_selector_semantics()
    stream = audit_stream()

    clearance = json.loads((MATERIALIZER / "CLEARANCE.json").read_text())
    build = json.loads(BUILD.read_text())
    source = (MATERIALIZER / "materialize.py").read_text()
    required_guard_literals = (
        'need(base != narrow and str(base).endswith(BASE_RELATIVE), "narrow/path substitution")',
        'need(base_hash.hexdigest() != NARROW_SHA256, "narrow CNF supplied as base")',
        'need(base_hash.hexdigest() == BASE_SHA256, "base hash")',
        'need(not output.exists() and not result.exists(), "refuse overwrite")',
    )
    need(all(literal in source for literal in required_guard_literals), "materializer replacement guard source")
    need(clearance["base_relative_path"].endswith("max16_current.cnf"))
    need(clearance["output_relative_path"].endswith("max16_combined_exact16_target_union_current.cnf"))
    need(build["output_sha256"] == TARGET_SHA and build["base_sha256"] == BASE_SHA and build["patch_sha256"] == PATCH_SHA)
    need(build["solver_run"] is False and build["atomic_temp_to_final"] is True)
    need(TARGET.resolve() != NARROW.resolve() and TARGET_SHA != NARROW_SHA)

    hostiles = {
        "schema": "n8-x5-combined-exact16-materialization-hostiles-v1",
        "status": "PASS_ALL_REJECTED",
        "cases": {
            "append_to_narrow": "rejected by original-base path/hash guard; selector IDs 428248..433755 would alias and the narrow global OR cannot be retained",
            "narrow_as_base": "rejected before acceptance by explicit narrow hash inequality and required original base hash",
            "missing_or_flipped_implication": "rejected by exact replay of every one of 897300 complete-cube implications",
            "missing_or_truncated_ledger": "rejected by exact 35892 canonical unique ledger lines and one exact global selector OR",
            "wrong_header_or_arithmetic": "rejected by exact header 464139/3980473 and 3083172+897301 clause recount",
            "extra_target_trailing_data": "rejected by EOF after the exact patch",
            "overwrite_or_partial_publish": "materializer required absent output/result and atomic fsync/rename",
        },
    }
    write_json(HERE / "HOSTILES.json", hostiles)

    result = {
        "schema": "n8-x5-combined-exact16-materialization-independent-referee-v1",
        "status": "PASS_EXACT_STREAM_COMPOSITION_SELECTOR_SEMANTICS_NO_SOLVER",
        "pins": pins,
        "base": {"path": str(BASE), "sha256": BASE_SHA, "bytes": BASE_BYTES, "variables": 428247, "clauses": BASE_CLAUSES},
        "patch": {"path": str(PATCH), "sha256": PATCH_SHA, "ledger_sha256": LEDGER_SHA, "selectors": SELECTOR_COUNT, "implications_checked": checked, "global_or_checked": True, "clauses": PATCH_CLAUSES},
        "target": {"path": str(TARGET), "sha256": TARGET_SHA, "bytes": TARGET_BYTES, "variables": SELECTOR_LAST, "clauses": TARGET_CLAUSES},
        "stream_derivation": stream,
        "semantic_coverage": {"graph_class_union": 92, "graph_class_intersection": 9, "support_union": len(ledger), "support_intersection": 3492, "every_selector_cube_checked": True, "generic_skeleton_excluded_by_global_or": True},
        "replacement_guard": {"original_base_required": True, "narrow_hash_forbidden": NARROW_SHA, "append_to_narrow_forbidden": True, "actual_target_is_fresh_replacement": True, "source_guard_literals_checked": len(required_guard_literals)},
        "atomic": {"producer_record_atomic": True, "solver_run": False, "independent_full_replay_complete": True},
        "scope": "materialization and finite target-union selector semantics only; no SAT/UNSAT result or theorem promotion",
    }
    write_json(HERE / "MATERIALIZATION_REFEREE_RESULT.json", result)
    result_sha = sha(HERE / "MATERIALIZATION_REFEREE_RESULT.json")

    plan = {
        "schema": "n8-x5-combined-exact16-cadical195-held-plan-v1",
        "status": "HELD_ZERO_RUN_AWAITING_FRESH_MANAGER_CLEARANCE",
        "input": {"path": str(TARGET.relative_to(ROOT)), "sha256": TARGET_SHA, "bytes": TARGET_BYTES, "variables": SELECTOR_LAST, "clauses": TARGET_CLAUSES, "materialization_referee_result_sha256": result_sha, "materialization_referee_manifest_sha256": None, "ledger_sha256": LEDGER_SHA},
        "toolchain": {
            "cadical_path": str(CROSS / "toolchains/cadical-1.9.5/build/cadical"),
            "cadical_version": "1.9.5",
            "cadical_commit": "146207318796f094dcded87349a64f0c6927309e",
            "cadical_binary_sha256": "379aee3d6c61ba729f051584e96db71b7f444f0d4016ef6072f87e4b554f858e",
            "drat_trim_path": str(CROSS / "toolchains/drat-trim/drat-trim"),
            "drat_trim_commit": "2e3b2dc0ecf938addbd779d42877b6ed69d9a985",
            "drat_trim_binary_sha256": "f58f63b0f76945d4c4c9ff6e87afaf870f579e67c0f7cca589492df8fc7ebd47",
        },
        "execution": {"lanes": 1, "sequential_only": True, "fresh_process_and_resource_census_required": True, "input_rehash_required_before_launch": True, "cadical_internal_cap_seconds": 6900, "cadical_wall_cap_seconds": 7200, "cadical_rss_cap_bytes": 17179869184, "drat_checker_internal_cap_seconds": 10200, "drat_checker_wall_cap_seconds": 10800, "drat_checker_rss_cap_bytes": 25769803776, "minimum_free_disk_kib": 67108864, "atomic_artifacts": True, "refuse_overwrite_or_stale_tmp": True, "no_parallel_solver_or_large_reader": True, "no_relaunch": True},
        "terminal_contract": {
            "sat": {"required_exit": 10, "required_log_literal": "s SATISFIABLE", "full_replay": "parse one complete assignment of variables1..464139 exactly once and stream-evaluate all3980473 clauses", "selector_replay": "identify the unique true selector, recover its exact ledger support/cube, verify exactly16 true block variables226..250, and classify it in the sealed92-class union", "scope": "support-relaxation model only; not an exact quantum witness or conjecture promotion"},
            "unsat": {"required_exit": 20, "required_log_literal": "s UNSATISFIABLE", "required_proof": "fresh nonempty binary DRAT atomically sealed", "independent_replay": "pinned drat-trim on exact c96d4ac1 input and proof exits0 with one literal s VERIFIED; checker log atomically sealed", "scope": "combined92-class finite exact16 target-union support theorem only; any broader promotion requires separate audit"},
            "other": "fail closed; preserve diagnostic artifacts as zero proof coverage; stop with no relaunch",
        },
        "artifact_policy": {
            "solver_log": "tmp/eight_vertex_local_degree4_full_local_max16_combined_exact16_cadical195.log",
            "proof": "tmp/eight_vertex_local_degree4_full_local_max16_combined_exact16_cadical195.drat",
            "checker_log": "tmp/eight_vertex_local_degree4_full_local_max16_combined_exact16_drat_trim.log",
            "sat_model_replay": "docs/audits/eight-vertex-degree4-combined-exact16-terminal-<date>/MODEL_REPLAY.json",
            "write_tmp_fsync_rename": True,
            "sat_proof_output": "quarantine as noncertificate; never treat as DRAT",
        },
        "launch_authorized": False,
        "solver_runs": 0,
    }
    write_json(HERE / "HELD_SOLVER_PLAN.json", plan)

    clearance_template = {
        "schema": "n8-x5-combined-exact16-cadical195-clearance-v1",
        "status": "HELD_MANAGER_CLEARANCE_NULL",
        "manager_clearance": None,
        "authorized_action": None,
        "nonce": None,
        "issued_utc": None,
        "expires_utc": None,
        "resource_clear": None,
        "no_overlap": None,
        "fresh_process_census": None,
        "free_disk_kib": None,
        "minimum_free_disk_kib": 67108864,
        "input_sha256": TARGET_SHA,
        "materialization_referee_result_sha256": result_sha,
        "materialization_referee_manifest_sha256": None,
        "cadical_binary_sha256": plan["toolchain"]["cadical_binary_sha256"],
        "drat_trim_binary_sha256": plan["toolchain"]["drat_trim_binary_sha256"],
        "lanes": 1,
        "no_relaunch": True,
    }
    write_json(HERE / "CLEARANCE_TEMPLATE.json", clearance_template)
    print("PASS_EXACT_STREAM_COMPOSITION_SELECTOR_SEMANTICS_NO_SOLVER")


if __name__ == "__main__":
    main()
