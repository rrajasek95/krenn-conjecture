#!/usr/bin/env python3
"""Seal only the explicit files in this held package and replay the manifest."""

import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
NAMES = [
    "REPORT.md", "build_contract.py", "build_source.py", "exact_Q_followup_conditional.json",
    "held_pilot.json", "hostile_tests.py", "independent_referee_acceptance.schema.json",
    "launch_clearance.schema.json", "refusal_contract.json",
    "rep1114_rank1_z1_fulltorus_dedup_p32003.sing", "results_hostiles.json",
    "results_self_audit.json", "run_one_lane.py", "source_derivation.json", "validate.py",
    "seal_manifest.py",
]


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            h.update(chunk)
    return h.hexdigest()


if len(NAMES) != len(set(NAMES)):
    raise RuntimeError("duplicate manifest member")
for name in NAMES:
    if not (HERE / name).is_file():
        raise RuntimeError(("missing", name))
text = "".join(f"{sha(HERE / name)}  {name}\n" for name in sorted(NAMES))
(HERE / "MANIFEST.sha256").write_text(text)
for line in text.splitlines():
    expected, name = line.split("  ", 1)
    if sha(HERE / name) != expected:
        raise RuntimeError(("replay", name))
print(sha(HERE / "MANIFEST.sha256"))
