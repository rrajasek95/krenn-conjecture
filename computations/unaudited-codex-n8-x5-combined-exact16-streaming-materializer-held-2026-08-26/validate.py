#!/usr/bin/env python3
"""Replay the held materializer without accessing the large base."""

import json
from pathlib import Path
import subprocess

from contract import *

HERE = Path(__file__).resolve().parent
CROSS = Path("/Users/rishi/workplace/krenn-cross-program-audit-2026-08-26/yesterdays-lemon")

run = subprocess.run(["python3", str(HERE / "materialize.py")], capture_output=True, text=True, check=False)
need(run.returncode == 0 and "HELD_SMALL_PREFLIGHT_PASS" in run.stdout, (run.returncode, run.stdout, run.stderr))

plan = json.loads((HERE / "HELD_PLAN.json").read_text())
result = json.loads((HERE / "results_held.json").read_text())
template = json.loads((HERE / "CLEARANCE_TEMPLATE.json").read_text())
schema = json.loads((HERE / "CLEARANCE.schema.json").read_text())
need(plan["status"] == "LAUNCH_READY_HELD__DEPENDENCIES_BOUND__MANAGER_CLEARANCE_NULL")
need(plan["pins"]["terminal_manifest"]["sha256"] == TERMINAL_MANIFEST_SHA256)
need(plan["materializer"]["forbidden_narrow_base"]["sha256"] == NARROW_SHA256)
need(plan["materializer"]["target"]["header"] == "p cnf 464139 3980473")
need(plan["materializer"]["target"]["bytes"] == TARGET_BYTES)
need(all(value is False for value in plan["zero_run"].values()), "zero run")
need(template["exact16_terminal_manifest_sha256"] == TERMINAL_MANIFEST_SHA256)
need(template["status"] == "HELD_DEPENDENCIES_BOUND_MANAGER_CLEARANCE_NULL")
for field in ("nonce", "issued_utc", "expires_utc", "materializer_manifest_sha256", "resource_clear", "no_overlap", "fresh_process_census", "free_disk_kib", "authorized_action"):
    need(template[field] is None, (field, "must remain null"))
need(schema["properties"]["exact16_terminal_manifest_sha256"]["const"] == TERMINAL_MANIFEST_SHA256)
need(result["status"] == "PASS_LAUNCH_READY_HELD_ZERO_RUN" and result["zero_run"] is True)
need(result["plan_sha256"] == sha256_file(HERE / "HELD_PLAN.json"))
need(result["materializer_sha256"] == sha256_file(HERE / "materialize.py"))
need(not (CROSS / OUTPUT_RELATIVE).exists(), "target unexpectedly materialized")
need(not (CROSS / RESULT_RELATIVE).exists(), "result unexpectedly materialized")

print("PASS launch-ready held streaming materializer; zero large read")
