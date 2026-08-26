#!/usr/bin/env python3
import hashlib
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


local_names = [
    "V2_REPORT.md",
    "prepare_v2.py",
    "validate_v2.py",
    "seal_v2_manifest.py",
    "authorize_v2.py",
    "v2_pins.json",
    "future_dependencies.json",
    "dependency_verifier.py",
    "normalize_dependencies.py",
    "run_groups126_161.py",
    "source_ledger.json",
    "independent_referee_acceptance.schema.json",
    "launch_clearance.schema.json",
] + [f"sources/rep4_group{i:03d}_Q.sing" for i in range(126, 162)]
external_names = [
    "computations/unaudited-codex-n8-x5-rep4-first25-terminal-compatibility-alias-2026-08-26/FINAL_MANIFEST.sha256",
    "computations/unaudited-codex-n8-x5-rep4-first25-terminal-compatibility-alias-2026-08-26/compatibility_result.json",
    "computations/unaudited-codex-n8-x5-rep4-groups26-75-exact-q-terminal-referee-2026-08-26/FINAL_MANIFEST.sha256",
    "computations/unaudited-codex-n8-x5-rep4-groups26-75-exact-q-terminal-referee-2026-08-26/results_referee.json",
    "computations/unaudited-codex-n8-x5-rep4-groups76-125-exact-q-terminal-referee-2026-08-26/FINAL_MANIFEST.sha256",
    "computations/unaudited-codex-n8-x5-rep4-groups76-125-exact-q-terminal-referee-2026-08-26/results_referee.json",
    "computations/unaudited-codex-n8-x5-rep4-groups126-161-exact-q-conditional-held-2026-08-26/MANIFEST.sha256",
    "computations/unaudited-codex-n8-x5-rep4-groups126-161-exact-q-conditional-held-referee-2026-08-26/FINAL_MANIFEST.sha256",
    "computations/unaudited-codex-n8-x5-rep4-groups126-161-exact-q-conditional-held-referee-2026-08-26/results_referee.json",
]
local = [HERE / name for name in local_names]
external = [ROOT / name for name in external_names]
assert all(path.is_file() for path in local + external)
lines = [f"{sha(path)}  {path.relative_to(HERE)}" for path in local]
lines += [f"{sha(path)}  {os.path.relpath(path, HERE)}" for path in external]
(HERE / "MANIFEST.sha256").write_text("\n".join(lines) + "\n")
print({"status": "SEALED_REP4_FINAL36_V2", "lines": len(lines), "sha256": sha(HERE / "MANIFEST.sha256")})
