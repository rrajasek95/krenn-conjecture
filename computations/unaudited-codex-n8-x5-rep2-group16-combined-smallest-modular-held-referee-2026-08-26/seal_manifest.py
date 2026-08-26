#!/usr/bin/env python3
import hashlib
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
local = [HERE / name for name in (
    "referee.py", "validate.py", "seal_manifest.py", "REPORT.md",
    "results_referee.json", "independent_referee_acceptance.json",
)]
external = [
    ROOT / "computations/unaudited-codex-n8-x5-rep2-group16-combined-smallest-modular-held-2026-08-26/MANIFEST.sha256",
    ROOT / "computations/unaudited-codex-n8-x5-rep2-group16-combined-smallest-modular-held-2026-08-26/rep2_group016_torus_zerozero_guardpivot_k0_p32003.sing",
    ROOT / "computations/unaudited-codex-n8-x5-rep2-group16-combined-smallest-modular-held-2026-08-26/run_one_lane.py",
    ROOT / "computations/unaudited-codex-n8-x5-rep2-group16-torus-gauge-referee-comparison-2026-08-26/rep2_group016_torus_A67zero_A12zero_guardpivot_k0_Q.sing",
    ROOT / "computations/unaudited-codex-n8-x5-rep2-first25-exact-q-terminal-referee-2026-08-26/FINAL_MANIFEST.sha256",
    ROOT / "computations/unaudited-codex-n8-x5-rep2-group16-torus-gauge-decomposition-design-2026-08-26/MANIFEST.sha256",
    ROOT / "computations/unaudited-codex-n8-x5-rep2-group16-torus-gauge-referee-comparison-2026-08-26/MANIFEST.sha256",
    ROOT / "computations/unaudited-codex-n8-x5-rep2-group16-isomorphism-guard-pivot-design-2026-08-26/MANIFEST.sha256",
]
assert all(path.is_file() for path in local + external)
lines = [f"{sha(path)}  {path.relative_to(HERE)}" for path in local]
lines += [f"{sha(path)}  {os.path.relpath(path, HERE)}" for path in external]
(HERE / "FINAL_MANIFEST.sha256").write_text("\n".join(lines) + "\n")
print({"status": "SEALED_PASS_HELD_ONLY", "lines": len(lines), "sha256": sha(HERE / "FINAL_MANIFEST.sha256")})
