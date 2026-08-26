#!/usr/bin/env python3
"""Held, clearance-gated D11 triangle continuation with cap 1,250,001."""

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
SOURCE = HERE / "src/main.rs"
BINARY = HERE / "x5_d11_triangle_resume38_cap1250001"
WATCHDOG = HERE / "watchdog38_600_resume.py"
PROVIDER = REPO / "computations/unaudited-codex-n8-x5-four-blocker-d6-cegar-gate-2026-08-25/provider_triangle_endpoint_colour.ms"
SELECTED = HERE / "sealed_resume_input/selected.tsv"
DUAL = HERE / "sealed_resume_input/dual.tsv"
PINS = {
    "source": "1f6fdab1da6b0821f7188efac30c7b4d5597b18414b52947eb50278b6894390d",
    "binary": "f49fc3aa5b4bc93d06ada200d4c32eb30b2c2a5b67475431390f3aedbb610c82",
    "watchdog": "854042e448cca17a6a1154934bb229dec794f72f8f528c265b7d2de0ebb107a3",
    "provider": "06df5052a50099dc400d622323257fef9b3077a791f918c8f1c46d7bf7a5782c",
    "selected": "81b4c5b8f929b26a8a7dc839a3638c8be9bd7973df843c131e4fc0b1056313c8",
    "dual": "c2c0d95e2063e1437e05b42169879d018031a6b5625955bd548cbca4880ca284",
    "checkpoint_audit": "68170d3b81f3e71e40ad2d00f6c034172deb88723f6764a4df7aa8838dee5669",
}


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def atomic(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


def main() -> None:
    for path, expected in ((SOURCE, PINS["source"]), (BINARY, PINS["binary"]),
                           (WATCHDOG, PINS["watchdog"]), (PROVIDER, PINS["provider"]),
                           (SELECTED, PINS["selected"]), (DUAL, PINS["dual"]),
                           (HERE / "sealed_resume_input/checkpoint_audit.json", PINS["checkpoint_audit"])):
        assert sha(path) == expected
    audit = json.loads((HERE / "sealed_resume_input/checkpoint_audit.json").read_text())
    assert audit["status"] == "PASS_FAIL_CLOSED_COLUMN_CAP_CHECKPOINT_CAP1250_NO_PROGRESS"
    assert audit["selected_columns"] == audit["selected_pairings_replayed"] == 913_636
    assert audit["dual_support"] == 924_170 and audit["pairing_failures"] == 0
    clearance_path = HERE / "CLEARANCE.json"
    if not clearance_path.exists():
        raise SystemExit("HOLD: explicit cap-1,250,001 clearance required")
    clearance = json.loads(clearance_path.read_text())
    assert clearance == {
        "schema": "KRENN_X5_D11_TRIANGLE_CAP1250001_RESUME38_CLEARANCE_V1",
        "authorized_manifest_sha256": sha(HERE / "MANIFEST.sha256"),
        "launch": True,
    }
    output = HERE / "production_cap1250001_resume_p1073741827_triangle_endpoint_colour"
    assert not output.exists()
    command = [str(BINARY), "--branch", "triangle_endpoint_colour", "--input", str(PROVIDER),
               "--resume-selected", str(SELECTED), "--resume-dual", str(DUAL),
               "--resume-round-offset", "0", "--output", str(output / "result.json"),
               "--selected", str(output / "selected.tsv"), "--dual", str(output / "dual.tsv"),
               "--prime", "1073741827", "--column-cap", "1250001", "--wall-seconds", "590"]
    wrapper = [sys.executable, str(WATCHDOG), "--rss-gib", "38", "--wall-seconds", "600",
               "--poll-seconds", "0.5", "--source", str(SOURCE),
               "--expected-source-sha256", PINS["source"], "--expected-binary-sha256", PINS["binary"],
               "--telemetry", str(output / "watchdog.json"), "--stdout", str(output / "stdout.log"),
               "--stderr", str(output / "stderr.log"), "--", *command]
    completed = subprocess.run(wrapper, cwd=REPO, check=False)
    telemetry = json.loads((output / "watchdog.json").read_text())
    result = json.loads((output / "result.json").read_text()) if (output / "result.json").exists() else None
    summary = {
        "schema": "KRENN_X5_D11_TRIANGLE_CAP1250001_RESUME38_RUN_SUMMARY_V1",
        "status": "PASS_TERMINAL" if telemetry["status"] == "PASS_TERMINAL" else
                  "PASS_RESTART" if telemetry["status"] == "PASS_RESTART_CHECKPOINT" else "FAIL_CLOSED",
        "watchdog_status": telemetry["status"], "watchdog_sha256": sha(output / "watchdog.json"),
        "result_status": result["status"] if result else None,
        "result_sha256": sha(output / "result.json") if result else None,
        "restart_pair_available": telemetry["restart_pair_available"],
        "restart_selected_sha256": telemetry["restart_selected_sha256"],
        "restart_dual_sha256": telemetry["restart_dual_sha256"],
        "second_prime_launched": False, "other_branch_launched": False,
        "degree_twelve_launched": False,
    }
    atomic(output / "run_summary.json", summary)
    print(json.dumps(summary, sort_keys=True))
    if completed.returncode != 0 or summary["status"] == "FAIL_CLOSED":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
