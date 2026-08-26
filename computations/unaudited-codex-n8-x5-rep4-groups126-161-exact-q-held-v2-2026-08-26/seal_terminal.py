#!/usr/bin/env python3
import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


paths = [
    HERE / "MANIFEST.sha256",
    HERE / "normalized_dependencies.json",
    HERE / "independent_referee_acceptance.json",
    HERE / "launch_clearance.json",
    HERE / "BATCH_ATTEMPT.json",
    HERE / "batch_result.json",
] + sorted((HERE / "results").glob("group*.json"))
assert len(paths) == 42 and all(path.is_file() for path in paths)
lines = [f"{sha(path)}  {path.relative_to(HERE)}" for path in paths]
(HERE / "TERMINAL_MANIFEST.sha256").write_text("\n".join(lines) + "\n")
print({"status": "SEALED_REP4_FINAL36_TERMINAL", "lines": len(lines), "sha256": sha(HERE / "TERMINAL_MANIFEST.sha256")})
