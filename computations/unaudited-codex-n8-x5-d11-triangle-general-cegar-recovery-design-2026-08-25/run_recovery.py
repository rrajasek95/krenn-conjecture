#!/usr/bin/env python3
"""Clearance-gated launcher for the sole D11 triangle p107 recovery."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
PARENT = REPO / "computations/unaudited-codex-n8-x5-four-d11-seeded-support-repair-2026-08-25"
SOURCE = HERE / "src/main.rs"
BINARY = HERE / "x5_d11_triangle_recovery"
WATCHDOG = HERE / "watchdog12_600_recovery.py"
PROVIDER = REPO / "computations/unaudited-codex-n8-x5-four-blocker-d6-cegar-gate-2026-08-25/provider_triangle_endpoint_colour.ms"
SEED_SELECTED = PARENT / "seed_triangle_endpoint_colour_p1073741827/selected.tsv"
SEED_DUAL = PARENT / "seed_triangle_endpoint_colour_p1073741827/transported_d10_dual.tsv"
PINS = {
    "source": "521e8f503f900c15b9b0668f60095fae120b6f47e44666076179fbc2058d9120",
    "binary": "a2ce6120a4d04683ef4238ef3ec2b4733ad1c2df186e5a838f740fd524f4d5f8",
    "watchdog": "4418ffadb5cc45ec4bdec1427850810d66438d7d09679520eab7d5fba142291e",
    "provider": "06df5052a50099dc400d622323257fef9b3077a791f918c8f1c46d7bf7a5782c",
    "seed_selected": "3eab0267866718ca21259e9daffac6f15161438b6348a25fe3de3ded08aaf10a",
    "seed_dual": "4eb560af124b6f046ae67b447988c0b0713822da852f2a1f6fa0307f6ca390b0",
}

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
    for path, expected in ((SOURCE, PINS["source"]), (BINARY, PINS["binary"]), (WATCHDOG, PINS["watchdog"]),
                           (PROVIDER, PINS["provider"]), (SEED_SELECTED, PINS["seed_selected"]), (SEED_DUAL, PINS["seed_dual"])):
        assert sha(path) == expected
    manifest = HERE / "MANIFEST.sha256"
    clearance_path = HERE / "CLEARANCE.json"
    if not clearance_path.exists():
        raise SystemExit("HOLD: missing explicit exclusive-slot CLEARANCE.json")
    clearance = json.loads(clearance_path.read_text())
    assert clearance == {"schema": "KRENN_X5_D11_TRIANGLE_RECOVERY_CLEARANCE_V1",
                         "authorized_manifest_sha256": sha(manifest),
                         "exclusive_slot": True, "launch": True}
    output = HERE / "production_p1073741827_triangle_endpoint_colour"
    assert not output.exists()
    command = [str(BINARY), "--branch", "triangle_endpoint_colour", "--input", str(PROVIDER),
               "--resume-selected", str(SEED_SELECTED), "--resume-dual", str(SEED_DUAL),
               "--resume-round-offset", "0", "--output", str(output / "result.json"),
               "--selected", str(output / "selected.tsv"), "--dual", str(output / "dual.tsv"),
               "--prime", "1073741827", "--column-cap", "500000", "--wall-seconds", "590"]
    wrapper = [sys.executable, str(WATCHDOG), "--rss-gib", "12", "--wall-seconds", "600", "--poll-seconds", "0.5",
               "--source", str(SOURCE), "--expected-source-sha256", PINS["source"],
               "--expected-binary-sha256", PINS["binary"], "--telemetry", str(output / "watchdog.json"),
               "--stdout", str(output / "stdout.log"), "--stderr", str(output / "stderr.log"), "--", *command]
    completed = subprocess.run(wrapper, cwd=REPO, check=False)
    telemetry = json.loads((output / "watchdog.json").read_text())
    result = json.loads((output / "result.json").read_text()) if (output / "result.json").exists() else None
    summary = {"schema": "KRENN_X5_D11_TRIANGLE_RECOVERY_RUN_SUMMARY_V1",
               "status": "PASS_TERMINAL" if telemetry["status"] == "PASS_TERMINAL" else "FAIL_CLOSED",
               "watchdog_status": telemetry["status"], "watchdog_sha256": sha(output / "watchdog.json"),
               "result_status": result["status"] if result else None,
               "result_sha256": sha(output / "result.json") if result else None,
               "restart_pair_available": telemetry["restart_pair_available"],
               "restart_selected_sha256": telemetry["restart_selected_sha256"],
               "restart_dual_sha256": telemetry["restart_dual_sha256"],
               "second_prime_launched": False, "degree_twelve_launched": False}
    atomic(output / "run_summary.json", summary)
    print(json.dumps(summary, sort_keys=True))
    if completed.returncode != 0 or summary["status"] != "PASS_TERMINAL":
        raise SystemExit(1)

if __name__ == "__main__":
    main()
