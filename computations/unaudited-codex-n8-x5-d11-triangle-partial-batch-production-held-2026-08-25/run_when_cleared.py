#!/usr/bin/env python3
"""Execute the frozen command exactly once only after explicit resource clearance."""

import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
ACCEPTANCE = HERE / "LAUNCH_ACCEPTANCE.json"
CLEARANCE = HERE / "CLEARANCE.json"
OUTPUT = HERE / "production_partial_batch_p107"
DESIGN = REPO / "computations/unaudited-codex-n8-x5-d11-triangle-partial-batch-held-2026-08-25"
PINS = {
    "acceptance": "cdfe4d47dcc9d11e05be0bfb65bda269ca5ec5f5d9003ae7fc57db19da4c90c0",
    "design_manifest": "54c4d29df4c77ffc3b678d72e01a60ac694a866f29c280501108314ab3365e7a",
    "source": "261f03cfcf9bd86de1e97e2f56221e51d8597ed3f2aa9f7ab30aa092b18be889",
    "binary": "72c8a091a2a58a444121fc178ea1b71a16e580d49546e54a996e2508685b7e98",
    "watchdog": "4c703cbd748fabeff19e3daf790808de02d69a96048090f41f19112c9d4621a5",
    "provider": "06df5052a50099dc400d622323257fef9b3077a791f918c8f1c46d7bf7a5782c",
    "seed_selected": "81b4c5b8f929b26a8a7dc839a3638c8be9bd7973df843c131e4fc0b1056313c8",
    "seed_dual": "c2c0d95e2063e1437e05b42169879d018031a6b5625955bd548cbca4880ca284",
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


def main() -> int:
    paths = {
        "acceptance": ACCEPTANCE,
        "design_manifest": DESIGN / "MANIFEST.sha256",
        "source": DESIGN / "src/main.rs",
        "binary": DESIGN / "x5_d11_partial_batch",
        "watchdog": HERE / "watchdog38_600.py",
        "provider": REPO / "computations/unaudited-codex-n8-x5-four-blocker-d6-cegar-gate-2026-08-25/provider_triangle_endpoint_colour.ms",
        "seed_selected": DESIGN / "seed_selected.tsv",
        "seed_dual": DESIGN / "seed_dual.tsv",
    }
    for name, path in paths.items():
        if sha(path) != PINS[name]:
            raise SystemExit(f"fail closed: {name} pin mismatch")
    acceptance = json.loads(ACCEPTANCE.read_text())
    if not CLEARANCE.exists():
        raise SystemExit("HELD: awaiting explicit D12_RESOURCE_CLEAR after r1587 hashing")
    expected_clearance = {
        "schema": "KRENN_X5_D11_TRIANGLE_PARTIAL_BATCH_PRODUCTION_CLEARANCE_V1",
        "status": "CLEARED_ONE_EXACT_RUN",
        "launch_acceptance_sha256": PINS["acceptance"],
        "d12_resource_clear": True,
        "r1587_producer_hashing_complete": True,
        "authorized_one_exact_run": True,
        "automatic_relaunch": False,
    }
    if json.loads(CLEARANCE.read_text()) != expected_clearance:
        raise SystemExit("fail closed: clearance does not exactly match frozen scope")
    if acceptance["status"] != "HELD_PENDING_D12_RESOURCE_CLEAR":
        raise SystemExit("fail closed: unexpected launch-acceptance status")
    if OUTPUT.exists():
        raise SystemExit("fail closed: output already exists; automatic relaunch forbidden")
    command = acceptance["command"]
    if command[-2:] != ["--wall-seconds", "590"]:
        raise SystemExit("fail closed: native wall command drift")
    started = time.monotonic()
    completed = subprocess.run(command, cwd=REPO, check=False)
    result_path = OUTPUT / "result.json"
    watchdog_path = OUTPUT / "watchdog.json"
    summary = {
        "schema": "KRENN_X5_D11_TRIANGLE_PARTIAL_BATCH_PRODUCTION_RUN_SUMMARY_V1",
        "returncode": completed.returncode,
        "elapsed_seconds": time.monotonic() - started,
        "launch_acceptance_sha256": PINS["acceptance"],
        "clearance_sha256": sha(CLEARANCE),
        "result_exists": result_path.exists(),
        "result_sha256": sha(result_path) if result_path.exists() else None,
        "watchdog_exists": watchdog_path.exists(),
        "watchdog_sha256": sha(watchdog_path) if watchdog_path.exists() else None,
        "automatic_relaunch": False,
        "second_prime_launched": False,
        "other_branch_launched": False,
        "degree_twelve_read": False,
    }
    atomic(OUTPUT / "run_summary.json", summary)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
