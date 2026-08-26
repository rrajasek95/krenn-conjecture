#!/usr/bin/env python3
"""Write and verify a manifest over this package only."""

import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
NAMES = [
    "REPORT.md",
    "affine_dependencies_mod1000003.json",
    "analyze_symbolic.py",
    "build_design.py",
    "extract_affine_dependencies.py",
    "held_deduplicated_Q_plan.json",
    "hostile_results.json",
    "hostiles.json",
    "make_hostiles.py",
    "rep1114_rank1_z1_fulltorus_dedup_Q.sing",
    "results_symbolic_reduction.json",
    "symbolic_diagnostics.json",
    "validate.py",
] + [f"hostile_{name}.json" for name in (
    "closed", "minor", "monic", "orbits", "rank", "rank_profiles",
    "relation_count", "relation_sign", "removed", "site", "solve_count", "status",
)]


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            h.update(chunk)
    return h.hexdigest()


if len(NAMES) != len(set(NAMES)):
    raise RuntimeError("duplicate manifest member")
for name in NAMES:
    if not (HERE / name).is_file():
        raise RuntimeError(("missing manifest member", name))
text = "".join(f"{digest(HERE / name)}  {name}\n" for name in sorted(NAMES))
(HERE / "MANIFEST.sha256").write_text(text)
for line in text.splitlines():
    expected, name = line.split("  ", 1)
    if digest(HERE / name) != expected:
        raise RuntimeError(("manifest replay", name))
print(digest(HERE / "MANIFEST.sha256"))
