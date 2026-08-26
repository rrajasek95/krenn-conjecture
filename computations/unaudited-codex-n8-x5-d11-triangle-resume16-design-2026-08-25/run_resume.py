#!/usr/bin/env python3
"""Clearance-gated 16-GiB resume of the sealed D11 triangle checkpoint."""
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
SOURCE = HERE / "src/main.rs"
BINARY = HERE / "x5_d11_triangle_resume16"
WATCHDOG = HERE / "watchdog16_360_resume.py"
PROVIDER = REPO / "computations/unaudited-codex-n8-x5-four-blocker-d6-cegar-gate-2026-08-25/provider_triangle_endpoint_colour.ms"
SEED_SELECTED = HERE / "sealed_resume_input/selected.tsv"
SEED_DUAL = HERE / "sealed_resume_input/dual.tsv"
PINS = {"source": "936ad21fa4aa8ed0ffe78dc090d9e85ddeefa33713be75c1daa1bcd5f7aca142",
        "binary": "2c342802e955a437bb9c6f7fa686a6d1912dad9fe045bec1bf79232b77a97755",
        "watchdog": "5a83fe143da9e4c7f646874f97944a4858b21362e5bbf91da98e3794fd0a3fd4",
        "provider": "06df5052a50099dc400d622323257fef9b3077a791f918c8f1c46d7bf7a5782c",
        "selected": "1f70a3220d6091e0877fd00d86c6ff9f06f25789e03cc854556e6d7ae34fb2a7",
        "dual": "a91f2be59901b4f29c09f64845e700fb40d7f15181bcd7ac8df89022d4e39d93",
        "checkpoint_audit": "37208d8103869d80513f2e3d67b557fbdf71f532e98f3cdada3221cbdc919c06"}

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
                           (PROVIDER, PINS["provider"]), (SEED_SELECTED, PINS["selected"]), (SEED_DUAL, PINS["dual"]),
                           (HERE / "sealed_resume_input/checkpoint_audit.json", PINS["checkpoint_audit"])):
        assert sha(path) == expected
    audit = json.loads((HERE / "sealed_resume_input/checkpoint_audit.json").read_text())
    assert audit["status"] == "PASS_RESTART_PAIR" and audit["selected_columns"] == 94526
    assert audit["dual_support"] == 13116 and audit["pairing_failures"] == 0
    manifest, clearance_path = HERE / "MANIFEST.sha256", HERE / "CLEARANCE.json"
    if not clearance_path.exists():
        raise SystemExit("HOLD: missing explicit exclusive-slot CLEARANCE.json")
    clearance = json.loads(clearance_path.read_text())
    assert clearance == {"schema": "KRENN_X5_D11_TRIANGLE_RESUME16_CLEARANCE_V1",
                         "authorized_manifest_sha256": sha(manifest),
                         "exclusive_slot": True, "launch": True}
    output = HERE / "production_resume_p1073741827_triangle_endpoint_colour"
    assert not output.exists()
    command = [str(BINARY), "--branch", "triangle_endpoint_colour", "--input", str(PROVIDER),
               "--resume-selected", str(SEED_SELECTED), "--resume-dual", str(SEED_DUAL),
               "--resume-round-offset", "0", "--output", str(output / "result.json"),
               "--selected", str(output / "selected.tsv"), "--dual", str(output / "dual.tsv"),
               "--prime", "1073741827", "--column-cap", "500000", "--wall-seconds", "350"]
    wrapper = [sys.executable, str(WATCHDOG), "--rss-gib", "16", "--wall-seconds", "360", "--poll-seconds", "0.5",
               "--source", str(SOURCE), "--expected-source-sha256", PINS["source"],
               "--expected-binary-sha256", PINS["binary"], "--telemetry", str(output / "watchdog.json"),
               "--stdout", str(output / "stdout.log"), "--stderr", str(output / "stderr.log"), "--", *command]
    completed = subprocess.run(wrapper, cwd=REPO, check=False)
    telemetry = json.loads((output / "watchdog.json").read_text())
    result = json.loads((output / "result.json").read_text()) if (output / "result.json").exists() else None
    summary = {"schema": "KRENN_X5_D11_TRIANGLE_RESUME16_RUN_SUMMARY_V1",
               "status": "PASS_TERMINAL" if telemetry["status"] == "PASS_TERMINAL" else "PASS_RESTART" if telemetry["status"] == "PASS_RESTART_CHECKPOINT" else "FAIL_CLOSED",
               "watchdog_status": telemetry["status"], "watchdog_sha256": sha(output / "watchdog.json"),
               "result_status": result["status"] if result else None,
               "result_sha256": sha(output / "result.json") if result else None,
               "restart_pair_available": telemetry["restart_pair_available"],
               "restart_selected_sha256": telemetry["restart_selected_sha256"],
               "restart_dual_sha256": telemetry["restart_dual_sha256"],
               "second_prime_launched": False, "degree_twelve_launched": False}
    atomic(output / "run_summary.json", summary)
    print(json.dumps(summary, sort_keys=True))
    if completed.returncode != 0 or summary["status"] == "FAIL_CLOSED":
        raise SystemExit(1)

if __name__ == "__main__":
    main()
