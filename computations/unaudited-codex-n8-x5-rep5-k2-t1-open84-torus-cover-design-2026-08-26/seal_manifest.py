#!/usr/bin/env python3
"""Seal local design artifacts and immutable external provenance."""
import hashlib
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


local = [
    HERE / "build_design.py", HERE / "test_design.py", HERE / "validate.py",
    HERE / "seal_manifest.py", HERE / "REPORT.md", HERE / "results_design.json",
    HERE / "results_hostiles.json",
] + sorted((HERE / "sources").glob("*.sing"))
external = [
    ROOT / "computations/unaudited-codex-n8-x5-rep5-rank-stratified-guard-pivot-design-v2-2026-08-25/MANIFEST.sha256",
    ROOT / "computations/unaudited-codex-n8-x5-rep5-rank-stratified-guard-pivot-design-v2-2026-08-25/rep5_p00_guardpivot_k2_rank2_t1_Q.sing",
    ROOT / "computations/unaudited-codex-n8-x5-rep5-rank2-open-smallest-modular-held-2026-08-26/result.json",
    ROOT / "computations/unaudited-codex-n8-x5-rep5-rank2-open-smallest-modular-held-2026-08-26/ATTEMPT.json",
    ROOT / "computations/unaudited-codex-n8-x5-rep5-rank2-open-smallest-modular-held-2026-08-26/TERMINAL_MANIFEST.sha256",
    ROOT / "computations/unaudited-codex-n8-x5-rep5-rank2-open-smallest-modular-terminal-referee-2026-08-26/results_referee.json",
    ROOT / "computations/unaudited-codex-n8-x5-rep5-rank2-open-smallest-modular-terminal-referee-2026-08-26/FINAL_MANIFEST.sha256",
]
assert len(local) == 23 and all(path.is_file() for path in local + external)
lines = [f"{sha(path)}  {path.relative_to(HERE)}" for path in local]
lines += [f"{sha(path)}  {os.path.relpath(path, HERE)}" for path in external]
(HERE / "MANIFEST.sha256").write_text("\n".join(lines) + "\n")
print({"status": "SEALED_EXACT_DESIGN_ZERO_RUN", "lines": len(lines), "manifest_sha256": sha(HERE / "MANIFEST.sha256")})
