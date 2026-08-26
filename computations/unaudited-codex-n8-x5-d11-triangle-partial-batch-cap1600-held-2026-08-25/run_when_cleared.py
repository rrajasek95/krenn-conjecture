#!/usr/bin/env python3
"""Held single-run launcher for the exact cap-1.6m continuation."""

import hashlib
import json
from pathlib import Path
import subprocess

if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
ACCEPTANCE = HERE / "LAUNCH_ACCEPTANCE.json"
CLEARANCE = HERE / "CLEARANCE.json"
OUTPUT = HERE / "production_cap1600_p107"
PARENT = REPO / "computations/unaudited-codex-n8-x5-d11-triangle-partial-batch-production-held-2026-08-25"
PINS = {
    "acceptance": "c17c8dc7b1fcd9506e35a84ede66a2770dc4f094bddd783f68a277c99dd2fd5b",
    "parent_manifest": "6a392f8f65d9ef921227b57d3fcb560e85f327eeb3b03d5750ee26d9d9bbe88b",
    "source": "a5d91a457e1cfdac45b033e31b32a52f65ff1d7f3f86fa229e28f68e20f21e5f",
    "binary": "224f5d0ad9043b62946fc68a70d18b9885f59c4cf1262d9417f5b160e82ae1a8",
    "watchdog": "4c703cbd748fabeff19e3daf790808de02d69a96048090f41f19112c9d4621a5",
    "provider": "06df5052a50099dc400d622323257fef9b3077a791f918c8f1c46d7bf7a5782c",
    "seed_selected": "3218c0c3b2dd357a12dc87fb8bc139e03379d5ef434166b6d481db9a34af98b5",
    "seed_dual": "6ba8e603921e0c7c3eb1e92026e46aa42dde94bc18ed8452acf272d193cfbcdd",
}


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> int:
    paths = {
        "acceptance": ACCEPTANCE,
        "parent_manifest": PARENT / "PRODUCTION_MANIFEST.sha256",
        "source": HERE / "src/main.rs",
        "binary": HERE / "x5_d11_partial_batch_cap1600",
        "watchdog": HERE / "watchdog38_600.py",
        "provider": REPO / "computations/unaudited-codex-n8-x5-four-blocker-d6-cegar-gate-2026-08-25/provider_triangle_endpoint_colour.ms",
        "seed_selected": PARENT / "production_partial_batch_p107/selected.tsv",
        "seed_dual": PARENT / "production_partial_batch_p107/dual.tsv",
    }
    for name, path in paths.items():
        if sha(path) != PINS[name]:
            raise SystemExit(f"fail closed: {name} pin mismatch")
    if not CLEARANCE.exists():
        raise SystemExit("HELD: cap-1.6m continuation has no clearance")
    expected = {
        "schema": "KRENN_X5_D11_TRIANGLE_PARTIAL_BATCH_CAP1600_CLEARANCE_V1",
        "status": "CLEARED_ONE_EXACT_RUN",
        "launch_acceptance_sha256": PINS["acceptance"],
        "d12_resource_clear": True,
        "authorized_one_exact_run": True,
        "automatic_relaunch": False,
    }
    if json.loads(CLEARANCE.read_text()) != expected:
        raise SystemExit("fail closed: clearance mismatch")
    if OUTPUT.exists():
        raise SystemExit("fail closed: output exists; automatic relaunch forbidden")
    command = json.loads(ACCEPTANCE.read_text())["command"]
    return subprocess.run(command, cwd=REPO, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
