#!/usr/bin/env python3
"""Seal explicit v2 package and provenance pins; never scan computations."""
from __future__ import annotations
import hashlib, os
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
LOCAL=["REPORT.md","build_held_pilot.py","held_pilot.json","independent_referee_acceptance.schema.json","launch_clearance.schema.json","refusal_contract.json","rep5_all_equal_y_i0_p00_x0_y0_d01_p32003.sing","run_one_lane.py","seal_manifest.py","validate.py"]
EXTERNAL=[
ROOT/"computations/unaudited-codex-n8-x5-rep5-guard-minor-contraction-design-2026-08-25/MANIFEST.sha256",
ROOT/"computations/unaudited-codex-n8-x5-rep5-guard-minor-contraction-design-2026-08-25/results_rep5_contraction_design.json",
ROOT/"computations/unaudited-codex-n8-x5-rep5-guard-minor-contraction-design-2026-08-25/rep5_guard_minor_tiny_y_p32003.sing",
ROOT/"computations/unaudited-codex-n8-x5-rep5-guard-minor-contraction-referee-2026-08-25/FINAL_MANIFEST.sha256",
ROOT/"computations/unaudited-codex-n8-x5-rep5-guard-minor-contraction-referee-2026-08-25/HELD_MODULAR_PILOT.json",
ROOT/"computations/unaudited-codex-n8-x5-rep5-all-equal-y-modular-held-referee-2026-08-25/FINAL_MANIFEST.sha256",
ROOT/"computations/unaudited-codex-n8-x5-rep5-all-equal-y-modular-held-referee-2026-08-25/results_referee.json",
ROOT/"computations/unaudited-codex-n8-x5-rep5-all-equal-y-modular-held-2026-08-25/MANIFEST.sha256",
Path("/usr/local/bin/Singular"),Path("/usr/local/bin/gtimeout")]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
lines=[]
for name in LOCAL:
 p=HERE/name; assert p.is_file(); lines.append(f"{sha(p)}  {name}")
for p in EXTERNAL:
 assert p.is_file(); display=str(p if str(p).startswith('/usr/') else Path(os.path.relpath(p,HERE))); lines.append(f"{sha(p)}  {display}")
assert len(lines)==20
tmp=HERE/"MANIFEST.sha256.tmp"; tmp.write_text("\n".join(lines)+"\n"); os.replace(tmp,HERE/"MANIFEST.sha256")
print(sha(HERE/"MANIFEST.sha256"))
