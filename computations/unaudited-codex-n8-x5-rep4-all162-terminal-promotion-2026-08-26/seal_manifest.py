#!/usr/bin/env python3
import hashlib
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


local = [HERE / name for name in ("REPORT.md", "promote.py", "validate.py", "seal_manifest.py", "results_promotion.json")]
external_names = [
    "computations/unaudited-codex-n8-x5-rep4-all162-terminal-promotion-conditional-design-2026-08-26/MANIFEST.sha256",
    "computations/unaudited-codex-n8-x5-rep4-all162-terminal-promotion-conditional-design-referee-2026-08-26/FINAL_MANIFEST.sha256",
    "computations/unaudited-codex-n8-x5-rep4-first25-exact-q-terminal-referee-2026-08-26/FINAL_MANIFEST.sha256",
    "computations/unaudited-codex-n8-x5-rep4-groups26-75-exact-q-terminal-referee-2026-08-26/FINAL_MANIFEST.sha256",
    "computations/unaudited-codex-n8-x5-rep4-groups76-125-exact-q-terminal-referee-2026-08-26/FINAL_MANIFEST.sha256",
    "computations/unaudited-codex-n8-x5-rep4-groups126-161-exact-q-terminal-referee-v2-2026-08-26/FINAL_MANIFEST.sha256",
]
external = [ROOT / name for name in external_names]
assert all(path.is_file() for path in local + external)
lines = [f"{sha(path)}  {path.relative_to(HERE)}" for path in local]
lines += [f"{sha(path)}  {os.path.relpath(path, HERE)}" for path in external]
(HERE / "FINAL_MANIFEST.sha256").write_text("\n".join(lines) + "\n")
print({"status": "SEALED_REP4_ALL162_TERMINAL_PROMOTION", "lines": len(lines), "sha256": sha(HERE / "FINAL_MANIFEST.sha256")})
