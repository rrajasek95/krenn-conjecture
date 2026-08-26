#!/usr/bin/env python3
"""Seal small dependency/contract metadata; never opens the base CNF."""

import json
from pathlib import Path

from contract import *

HERE = Path(__file__).resolve().parent
PATCH_PACKAGE = Path("/Users/rishi/workplace/krenn-conjecture/computations/unaudited-codex-n8-x5-eight-nine-exact16-selector-patch-held-2026-08-26")
TERMINAL = Path("/Users/rishi/workplace/krenn-cross-program-audit-2026-08-26/yesterdays-lemon/docs/audits/eight-vertex-degree4-exact16-target-union-terminal-unsat-2026-08-26")

PINS = {
    "patch_package_manifest": (PATCH_PACKAGE / "MANIFEST.sha256", PATCH_PACKAGE_MANIFEST_SHA256),
    "patch_fragment": (PATCH_PACKAGE / "selector_patch.cnfpart", PATCH_SHA256),
    "terminal_manifest": (TERMINAL / "FINAL_MANIFEST.sha256", TERMINAL_MANIFEST_SHA256),
    "terminal_result": (TERMINAL / "TERMINAL_AUDIT_RESULT.json", TERMINAL_RESULT_SHA256),
}


def canonical(value):
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def build():
    pins = {}
    for name, (path, expected) in PINS.items():
        need(path.is_file(), (name, "missing"))
        observed = sha256_file(path)
        need(observed == expected, (name, observed, expected))
        pins[name] = {"path": str(path), "sha256": observed, "bytes": path.stat().st_size}
    validate_patch(PINS["patch_fragment"][0])
    terminal = json.loads(PINS["terminal_result"][0].read_text())
    need(terminal["status"] == "PASS_VERIFIED_UNSAT_AND_EIGHT_BLOCK_SUPPORT_FRONTIER_ONLY")
    need(terminal["checker"]["status"] == "VERIFIED" and terminal["checker"]["exit"] == 0)

    plan = {
        "schema": "n8-x5-combined-exact16-streaming-materializer-held-v1",
        "status": "LAUNCH_READY_HELD__DEPENDENCIES_BOUND__MANAGER_CLEARANCE_NULL",
        "pins": pins,
        "materializer": {
            "script": "materialize.py",
            "default_action": "small preflight only; no base path access",
            "execute_action": "stream original base body under replacement header, append exact patch, fsync and atomically rename",
            "base": {"relative_path": BASE_RELATIVE, "sha256": BASE_SHA256, "bytes": BASE_BYTES, "header": BASE_HEADER.decode().strip()},
            "forbidden_narrow_base": {"relative_path": NARROW_RELATIVE, "sha256": NARROW_SHA256},
            "patch": {"sha256": PATCH_SHA256, "bytes": PATCH_BYTES, "clauses": PATCH_CLAUSES},
            "target": {"relative_path": OUTPUT_RELATIVE, "header": TARGET_HEADER.decode().strip(), "bytes": TARGET_BYTES},
            "result": RESULT_RELATIVE,
            "refuse_overwrite": True,
            "atomic_same_filesystem_temp": True,
            "solver_launch": False,
        },
        "clearance": {
            "schema_path": "CLEARANCE.schema.json",
            "template_path": "CLEARANCE_TEMPLATE.json",
            "terminal_manifest_bound": TERMINAL_MANIFEST_SHA256,
            "manager_clearance": None,
            "nonce": None,
            "expires_utc": None,
            "materializer_manifest_sha256": None,
            "resource_clear": None,
            "fresh_process_census": None,
            "minimum_free_disk_kib": MINIMUM_FREE_DISK_KIB,
        },
        "post_materialization": {
            "status": "INDEPENDENT_FULL_REPLAY_REQUIRED_BEFORE_ANY_SOLVE",
            "checks": ["stream output SHA and bytes", "header464139/3980473", "recount3980473 clauses", "base-prefix/body equality", "patch suffix equality", "atomic/no tmp/no overlap"],
        },
        "zero_run": {"large_base_read": False, "target_materialized": False, "solver_run": False, "clearance_consumed": False},
    }
    (HERE / "HELD_PLAN.json").write_text(canonical(plan))
    result = {
        "schema": "n8-x5-combined-exact16-streaming-materializer-held-result-v1",
        "status": "PASS_LAUNCH_READY_HELD_ZERO_RUN",
        "plan_sha256": sha256_file(HERE / "HELD_PLAN.json"),
        "materializer_sha256": sha256_file(HERE / "materialize.py"),
        "clearance_schema_sha256": sha256_file(HERE / "CLEARANCE.schema.json"),
        "clearance_template_sha256": sha256_file(HERE / "CLEARANCE_TEMPLATE.json"),
        "terminal_manifest_sha256": TERMINAL_MANIFEST_SHA256,
        "patch_sha256": PATCH_SHA256,
        "target_header": {"variables": TARGET_VARIABLES, "clauses": TARGET_CLAUSES},
        "zero_run": True,
    }
    (HERE / "results_held.json").write_text(canonical(result))


if __name__ == "__main__":
    build()
