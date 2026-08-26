#!/usr/bin/env python3
import hashlib
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


local = [HERE / name for name in ("build_alias.py", "validate.py", "seal_manifest.py", "REPORT.md", "compatibility_result.json")]
external = [
    ROOT / "computations/unaudited-codex-n8-x5-rep4-first25-exact-q-terminal-referee-2026-08-26/FINAL_MANIFEST.sha256",
    ROOT / "computations/unaudited-codex-n8-x5-rep4-first25-exact-q-terminal-referee-2026-08-26/results_referee.json",
]
assert all(path.is_file() for path in local + external)
lines = [f"{sha(path)}  {path.relative_to(HERE)}" for path in local]
lines += [f"{sha(path)}  {os.path.relpath(path, HERE)}" for path in external]
(HERE / "FINAL_MANIFEST.sha256").write_text("\n".join(lines) + "\n")
print({"status": "SEALED_FIRST25_COMPATIBILITY_ALIAS", "lines": len(lines), "sha256": sha(HERE / "FINAL_MANIFEST.sha256")})
