#!/usr/bin/env python3
"""Held-only launcher; refuses unless a future exact clearance names this seal."""

import hashlib
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
SOURCE = HERE / "src/main.rs"
BINARY = HERE / "x5_d11_partial_batch"
WATCHDOG = HERE / "watchdog38_180_gate.py"
PROVIDER = REPO / "computations/unaudited-codex-n8-x5-four-blocker-d6-cegar-gate-2026-08-25/provider_triangle_endpoint_colour.ms"
SEED_SELECTED = HERE / "seed_selected.tsv"
SEED_DUAL = HERE / "seed_dual.tsv"
OUTPUT = HERE / "held_production_partial_batch"
PINS = {
    "source": "261f03cfcf9bd86de1e97e2f56221e51d8597ed3f2aa9f7ab30aa092b18be889",
    "binary": "72c8a091a2a58a444121fc178ea1b71a16e580d49546e54a996e2508685b7e98",
    "watchdog": "b07ca405b37c821efd7fb622a79bacf7a4f243e1564adba17e0a6f19e0bc2eeb",
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


def main() -> int:
    paths = {"source": SOURCE, "binary": BINARY, "watchdog": WATCHDOG,
             "provider": PROVIDER, "seed_selected": SEED_SELECTED, "seed_dual": SEED_DUAL}
    for name, path in paths.items():
        if sha(path) != PINS[name]:
            raise SystemExit(f"fail closed: {name} pin mismatch")
    clearance_path = HERE / "CLEARANCE.json"
    if not clearance_path.exists():
        raise SystemExit("HELD: exact partial-batch production has no clearance")
    clearance = json.loads(clearance_path.read_text())
    expected = {
        "schema": "KRENN_X5_D11_TRIANGLE_PARTIAL_BATCH_CLEARANCE_V1",
        "status": "CLEARED_ONE_PARTIAL_BATCH",
        "manifest_sha256": sha(HERE / "MANIFEST.sha256"),
        "column_cap": 1_250_001,
        "native_wall_seconds": 170,
        "wrapper_wall_seconds": 180,
        "rss_gib": 38,
        "source_sha256": PINS["source"],
        "binary_sha256": PINS["binary"],
        "provider_sha256": PINS["provider"],
        "seed_selected_sha256": PINS["seed_selected"],
        "seed_dual_sha256": PINS["seed_dual"],
    }
    if clearance != expected:
        raise SystemExit("fail closed: clearance does not exactly match frozen contract")
    if OUTPUT.exists():
        raise SystemExit("fail closed: output already exists")
    command = [
        "python3", str(WATCHDOG), "--rss-gib", "38", "--wall-seconds", "180",
        "--source", str(SOURCE), "--expected-source-sha256", PINS["source"],
        "--expected-binary-sha256", PINS["binary"],
        "--telemetry", str(OUTPUT / "watchdog.json"),
        "--stdout", str(OUTPUT / "stdout.log"), "--stderr", str(OUTPUT / "stderr.log"), "--",
        str(BINARY), "--branch", "triangle_endpoint_colour", "--input", str(PROVIDER),
        "--output", str(OUTPUT / "result.json"), "--selected", str(OUTPUT / "selected.tsv"),
        "--dual", str(OUTPUT / "dual.tsv"), "--resume-selected", str(SEED_SELECTED),
        "--resume-dual", str(SEED_DUAL), "--resume-round-offset", "0",
        "--prime", "1073741827", "--column-cap", "1250001", "--wall-seconds", "170",
    ]
    return subprocess.run(command, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
