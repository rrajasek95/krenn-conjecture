#!/usr/bin/env python3
import hashlib
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


local = [HERE / name for name in ("REPORT.md", "build_sources.py", "validate.py", "run_three.py", "authorize.py", "seal_manifest.py", "source_ledger.json")]
local += sorted((HERE / "sources").glob("*.sing"))
external_names = [
    "computations/unaudited-codex-n8-x5-rep2-group16-67-timeout-reduction-design-2026-08-26/MANIFEST.sha256",
    "computations/unaudited-codex-n8-x5-rep2-group16-67-timeout-reduction-referee-2026-08-26/MANIFEST.sha256",
    "computations/unaudited-codex-n8-x5-rep2-group16-67-timeout-reduction-referee-2026-08-26/results_referee.json",
    "computations/unaudited-codex-n8-x5-rep2-group16-closed-t-exact-q-terminal-referee-2026-08-26/FINAL_MANIFEST.sha256",
    "computations/unaudited-codex-n8-x5-rep2-group16-closed-t-exact-q-terminal-referee-2026-08-26/results_referee.json",
]
external = [ROOT / name for name in external_names]
assert all(path.is_file() for path in local + external)
lines = [f"{sha(path)}  {path.relative_to(HERE)}" for path in local]
lines += [f"{sha(path)}  {os.path.relpath(path, HERE)}" for path in external]
(HERE / "MANIFEST.sha256").write_text("\n".join(lines) + "\n")
print({"status": "SEALED_TCOVER_COMPLEMENT3_HELD", "lines": len(lines), "sha256": sha(HERE / "MANIFEST.sha256")})
