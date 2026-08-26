#!/usr/bin/env python3
"""Seal this referee and the exact explicit input interface only."""
import hashlib
import os
from pathlib import Path

H = Path(__file__).resolve().parent
ROOT = H.parents[1]
PROD = ROOT / "computations/unaudited-codex-n8-x5-rep5-k2-t1-open84-torus-cover-design-2026-08-26"
DES = ROOT / "computations/unaudited-codex-n8-x5-rep5-rank-stratified-guard-pivot-design-v2-2026-08-25"
MOD = ROOT / "computations/unaudited-codex-n8-x5-rep5-rank2-open-smallest-modular-held-2026-08-26"
MODREF = ROOT / "computations/unaudited-codex-n8-x5-rep5-rank2-open-smallest-modular-terminal-referee-2026-08-26"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


local = [H / name for name in ("REPORT.md", "audit.py", "results_referee.json", "seal_manifest.py", "validate.py")]
external = [
    PROD / "MANIFEST.sha256", PROD / "results_design.json", PROD / "results_hostiles.json",
    PROD / "build_design.py", PROD / "test_design.py",
    DES / "MANIFEST.sha256", DES / "rep5_p00_guardpivot_k2_rank2_t1_Q.sing",
    MOD / "MANIFEST.sha256", MOD / "rep5_rank2_k2_t1_p32003.sing", MOD / "ATTEMPT.json",
    MOD / "result.json", MOD / "TERMINAL_MANIFEST.sha256",
    MODREF / "results_referee.json", MODREF / "FINAL_MANIFEST.sha256",
] + sorted((PROD / "sources").glob("*.sing"))
paths = local + external
assert len(list((PROD / "sources").glob("*.sing"))) == 16 and all(path.is_file() for path in paths)
lines = [f"{sha(path)}  {os.path.relpath(path, H)}" for path in sorted(paths, key=lambda p: os.path.relpath(p, H))]
temporary = H / "MANIFEST.sha256.tmp"
temporary.write_text("\n".join(lines) + "\n")
os.replace(temporary, H / "MANIFEST.sha256")
print(f"sealed {len(lines)} explicit files")
