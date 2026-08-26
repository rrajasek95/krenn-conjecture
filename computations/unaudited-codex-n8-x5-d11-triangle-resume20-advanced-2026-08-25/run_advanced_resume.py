#!/usr/bin/env python3
"""Clearance-gated 20-GiB resume from the advanced D11 triangle checkpoint."""

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
BINARY = HERE / "x5_d11_triangle_resume20"
WATCHDOG = HERE / "watchdog20_600_resume.py"
PROVIDER = REPO / "computations/unaudited-codex-n8-x5-four-blocker-d6-cegar-gate-2026-08-25/provider_triangle_endpoint_colour.ms"
SELECTED = HERE / "sealed_resume_input/selected.tsv"
DUAL = HERE / "sealed_resume_input/dual.tsv"
PINS = {
    "source": "855ef288b03f2c07f4c8988a738aeb3409e5909e208c6c0ef8966eb8c8923035",
    "binary": "9abae41a47cc0b5e0a1c93bbdc9bc13c3497d2f7cd1326dcf69c3831ae121d6a",
    "watchdog": "05917823ff4b8b152d12f16112473af6acd6b8174fa94db6a74e66f35ad01011",
    "provider": "06df5052a50099dc400d622323257fef9b3077a791f918c8f1c46d7bf7a5782c",
    "selected": "9c70caaf26b71345b03565dbdf2edba8c52f06eca4ad74d6e7b888fa8a49cca5",
    "dual": "06ded311e326a66105d69ae7be2eb56c7ba9720ab19718f7cd173c09efb2ce02",
    "checkpoint_audit": "5f5152302fb3f0e48fde944eb8aba7904479e73337ad46d4d1f18c6daa4077fd",
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
    for path, expected in (
        (SOURCE, PINS["source"]), (BINARY, PINS["binary"]), (WATCHDOG, PINS["watchdog"]),
        (PROVIDER, PINS["provider"]), (SELECTED, PINS["selected"]), (DUAL, PINS["dual"]),
        (HERE / "sealed_resume_input/checkpoint_audit.json", PINS["checkpoint_audit"]),
    ):
        assert sha(path) == expected
    audit = json.loads((HERE / "sealed_resume_input/checkpoint_audit.json").read_text())
    assert audit["status"] == "PASS_FAIL_CLOSED_CHECKPOINT_ADVANCED"
    assert audit["selected_columns"] == audit["selected_pairings_replayed"] == 230_091
    assert audit["dual_support"] == 80_922 and audit["pairing_failures"] == 0
    manifest = HERE / "MANIFEST.sha256"
    clearance = json.loads((HERE / "CLEARANCE.json").read_text())
    assert clearance == {
        "schema": "KRENN_X5_D11_TRIANGLE_ADVANCED_RESUME20_CLEARANCE_V1",
        "authorized_manifest_sha256": sha(manifest),
        "launch": True,
    }
    output = HERE / "production_advanced_resume_p1073741827_triangle_endpoint_colour"
    assert not output.exists()
    command = [str(BINARY), "--branch", "triangle_endpoint_colour", "--input", str(PROVIDER),
               "--resume-selected", str(SELECTED), "--resume-dual", str(DUAL),
               "--resume-round-offset", "0", "--output", str(output / "result.json"),
               "--selected", str(output / "selected.tsv"), "--dual", str(output / "dual.tsv"),
               "--prime", "1073741827", "--column-cap", "500000", "--wall-seconds", "590"]
    wrapper = [sys.executable, str(WATCHDOG), "--rss-gib", "20", "--wall-seconds", "600",
               "--poll-seconds", "0.5", "--source", str(SOURCE),
               "--expected-source-sha256", PINS["source"], "--expected-binary-sha256", PINS["binary"],
               "--telemetry", str(output / "watchdog.json"), "--stdout", str(output / "stdout.log"),
               "--stderr", str(output / "stderr.log"), "--", *command]
    completed = subprocess.run(wrapper, cwd=REPO, check=False)
    telemetry = json.loads((output / "watchdog.json").read_text())
    result = json.loads((output / "result.json").read_text()) if (output / "result.json").exists() else None
    summary = {
        "schema": "KRENN_X5_D11_TRIANGLE_ADVANCED_RESUME20_RUN_SUMMARY_V1",
        "status": "PASS_TERMINAL" if telemetry["status"] == "PASS_TERMINAL" else
                  "PASS_RESTART" if telemetry["status"] == "PASS_RESTART_CHECKPOINT" else "FAIL_CLOSED",
        "watchdog_status": telemetry["status"],
        "watchdog_sha256": sha(output / "watchdog.json"),
        "result_status": result["status"] if result else None,
        "result_sha256": sha(output / "result.json") if result else None,
        "restart_pair_available": telemetry["restart_pair_available"],
        "restart_selected_sha256": telemetry["restart_selected_sha256"],
        "restart_dual_sha256": telemetry["restart_dual_sha256"],
        "second_prime_launched": False,
        "other_branch_launched": False,
        "degree_twelve_launched": False,
    }
    atomic(output / "run_summary.json", summary)
    print(json.dumps(summary, sort_keys=True))
    if completed.returncode != 0 or summary["status"] == "FAIL_CLOSED":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
