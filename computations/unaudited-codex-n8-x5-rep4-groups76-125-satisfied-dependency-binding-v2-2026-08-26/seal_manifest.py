#!/usr/bin/env python3
import hashlib, os
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
local = [HERE / name for name in (
    "build_binding.py", "referee.py", "validate.py", "seal_manifest.py", "REPORT.md",
    "normalized_dependencies.json", "independent_referee_acceptance.json",
    "results_binding.json", "results_referee.json",
)]
external = [ROOT / name for name in (
    "computations/unaudited-codex-n8-x5-rep4-groups76-125-exact-q-conditional-held-2026-08-26/MANIFEST.sha256",
    "computations/unaudited-codex-n8-x5-rep4-groups76-125-exact-q-conditional-held-2026-08-26/source_ledger.json",
    "computations/unaudited-codex-n8-x5-rep4-groups76-125-exact-q-conditional-held-2026-08-26/run_groups76_125.py",
    "computations/unaudited-codex-n8-x5-rep4-groups76-125-exact-q-conditional-held-referee-2026-08-26/FINAL_MANIFEST.sha256",
    "computations/unaudited-codex-n8-x5-rep4-first25-exact-q-held-2026-08-26/TERMINAL_MANIFEST.sha256",
    "computations/unaudited-codex-n8-x5-rep4-first25-exact-q-terminal-referee-2026-08-26/results_referee.json",
    "computations/unaudited-codex-n8-x5-rep4-first25-exact-q-terminal-referee-2026-08-26/FINAL_MANIFEST.sha256",
    "computations/unaudited-codex-n8-x5-rep4-groups26-75-exact-q-conditional-held-2026-08-26/TERMINAL_MANIFEST.sha256",
    "computations/unaudited-codex-n8-x5-rep4-groups26-75-exact-q-terminal-referee-2026-08-26/results_referee.json",
    "computations/unaudited-codex-n8-x5-rep4-groups26-75-exact-q-terminal-referee-2026-08-26/FINAL_MANIFEST.sha256",
)]
assert all(path.is_file() for path in local + external)
lines = [f"{sha(path)}  {path.relative_to(HERE)}" for path in local]
lines += [f"{sha(path)}  {os.path.relpath(path, HERE)}" for path in external]
(HERE / "FINAL_MANIFEST.sha256").write_text("\n".join(lines) + "\n")
print({"status": "SEALED_SATISFIED_BINDING", "lines": len(lines), "sha256": sha(HERE / "FINAL_MANIFEST.sha256")})
