#!/usr/bin/env python3
"""Bounded resource replay of the read-only structured audit."""

from __future__ import annotations

import hashlib
import json
import os
import resource
import subprocess
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
BINARY = HERE / "target/release/audit_d12_structured_dual"
PROVIDER = ROOT / "computations/unaudited-codex-star-tautology-triangle-replacement-2026-08-22/canonical_triangle_pair_offdiag_full_p32003.ms"
CHECKPOINT = ROOT / "computations/unaudited-codex-n8-affine251-d12-portfolio-gate-2026-08-24/audit660_checkpoint.bin"
PREVIOUS = ROOT / "computations/unaudited-codex-n8-affine251-d12-portfolio-gate-2026-08-24/fixed_checkpoint.bin"
PINS = {
    BINARY: "14fab037e001169f60707b8eb9bb274afeb75edf439680ad2751fdd8c8a7b3e4",
    HERE / "src/main.rs": "fb71c7d46ee7bebad67f1dc42ad408c6fdd0ea7e86758f5c8e1bba99ed5207df",
    PROVIDER: "75a82d82a979d75507e682fd339e83d4ae35949653d624fb541148bd3957dcff",
    CHECKPOINT: "92185737bc273f112f91240ee58eb8d0b4cd842739490838ebd30c870b8b6155",
    PREVIOUS: "c93c211dabbeca652bce848a2a55ba672e6ff5640161449830b7cd88e6e31971",
}


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20): h.update(block)
    return h.hexdigest()


def main() -> None:
    for path, expected in PINS.items(): assert sha(path) == expected, path
    replay_path = HERE / "results_structured_dual_audit_resource_replay.json"
    command = [str(BINARY), "--input", str(PROVIDER), "--checkpoint", str(CHECKPOINT),
               "--previous-checkpoint", str(PREVIOUS),
               "--output", str(replay_path), "--workers", "8"]
    started = time.monotonic()
    completed = subprocess.run(command, cwd=ROOT, capture_output=True, text=True,
                               timeout=120, start_new_session=True)
    elapsed = time.monotonic() - started
    assert completed.returncode == 0 and elapsed < 120
    peak = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
    peak_bytes = int(peak if os.uname().sysname == "Darwin" else peak * 1024)
    assert 0 < peak_bytes < 4 * 1024**3
    primary = json.loads((HERE / "results_structured_dual_audit.json").read_text())
    replay = json.loads(replay_path.read_text())
    for record in (primary, replay): record.pop("elapsed_seconds")
    assert primary == replay
    result = {
        "schema": "KRENN_AFFINE251_D12_ROUND660_STRUCTURED_RESOURCE_REPLAY_V1",
        "status": "PASS",
        "wall_limit_seconds": 120,
        "rss_limit_bytes": 4 * 1024**3,
        "elapsed_seconds": elapsed,
        "peak_rss_bytes": peak_bytes,
        "mathematical_output_equal_excluding_elapsed": True,
        "primary_sha256": sha(HERE / "results_structured_dual_audit.json"),
        "replay_sha256": sha(replay_path),
        "stdout_sha256": hashlib.sha256(completed.stdout.encode()).hexdigest(),
        "stderr_sha256": hashlib.sha256(completed.stderr.encode()).hexdigest(),
    }
    (HERE / "results_resource_replay.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__": main()
