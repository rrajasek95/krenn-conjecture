#!/usr/bin/env python3
"""Strict terminal audit of the cleared D11 triangle recovery attempt."""
import hashlib
import json
import os
from pathlib import Path

if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "production_p1073741827_triangle_endpoint_colour"
DESIGN_MANIFEST_SHA = "d3591fd2505dcea01214a25018557644a8788470bd64e6fd65f28a03c3747ab9"

def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()

def atomic(path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)

def main():
    assert sha(HERE / "MANIFEST.sha256") == DESIGN_MANIFEST_SHA
    clearance = json.loads((HERE / "CLEARANCE.json").read_text())
    assert clearance == {"schema": "KRENN_X5_D11_TRIANGLE_RECOVERY_CLEARANCE_V1",
                         "authorized_manifest_sha256": DESIGN_MANIFEST_SHA,
                         "exclusive_slot": True, "launch": True}
    watch = json.loads((OUTPUT / "watchdog.json").read_text())
    summary = json.loads((OUTPUT / "run_summary.json").read_text())
    checkpoint = json.loads((OUTPUT / "checkpoint_audit.json").read_text())
    assert watch["status"] == "FAIL_CLOSED_CHECKPOINT_AVAILABLE"
    assert watch["breach"] == "RSS_CAP" and watch["result_exists"] is False
    assert watch["elapsed_seconds"] < 600 and watch["peak_rss_kib"] > 12 * 1024 * 1024
    assert watch["restart_pair_available"] is True
    assert summary["status"] == "FAIL_CLOSED" and summary["result_status"] is None
    assert checkpoint["status"] == "PASS_RESTART_PAIR" and checkpoint["pairing_failures"] == 0
    assert checkpoint["selected_columns"] == 94526 and checkpoint["dual_support"] == 13116
    assert checkpoint["selected_sha256"] == watch["restart_selected_sha256"]
    assert checkpoint["dual_sha256"] == watch["restart_dual_sha256"]
    assert not (OUTPUT / "result.json").exists()
    assert not any("p1000000007" in path.name for path in HERE.iterdir())
    assert not any("third_colour" in path.name or "cap_endpoint_colour" in path.name for path in HERE.iterdir())
    result = {"schema": "KRENN_X5_D11_TRIANGLE_RECOVERY_FINAL_AUDIT_V1",
              "status": "FAIL_CLOSED_RESTART_PAIR_SEALED", "branch": "triangle_endpoint_colour",
              "prime": 1073741827, "native_wall_seconds": 590, "wrapper_wall_seconds": 600,
              "rss_limit_kib": 12 * 1024 * 1024, "breach": watch["breach"],
              "elapsed_seconds": watch["elapsed_seconds"], "peak_rss_kib": watch["peak_rss_kib"],
              "result_emitted": False, "accepted_mathematical_coverage": 0,
              "restart_pair_status": checkpoint["status"], "restart_selected_columns": checkpoint["selected_columns"],
              "restart_dual_support": checkpoint["dual_support"],
              "restart_selected_sha256": checkpoint["selected_sha256"],
              "restart_dual_sha256": checkpoint["dual_sha256"],
              "restart_pairings_replayed": checkpoint["selected_pairings_replayed"],
              "restart_pairing_failures": 0, "global_incident_scan_performed": False,
              "mathematical_verdict": None, "second_prime_launched": False,
              "other_branch_launched": False, "degree_twelve_launched": False}
    atomic(HERE / "results_recovery_audit.json", result)
    print(json.dumps(result, sort_keys=True))

if __name__ == "__main__":
    main()
