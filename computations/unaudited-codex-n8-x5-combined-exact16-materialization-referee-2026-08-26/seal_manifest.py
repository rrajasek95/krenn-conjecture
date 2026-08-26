#!/usr/bin/env python3
"""Write the deterministic small-artifact manifest for this referee package."""

import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
FILES = (
    "HELD_SOLVER_PLAN.json",
    "REPORT.md",
    "SOLVER_CLEARANCE.schema.json",
    "SOLVER_CLEARANCE_TEMPLATE.json",
    "audit_stream.py",
    "results_referee.json",
    "seal_manifest.py",
    "validate.py",
)


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


text = "".join(f"{sha256(HERE / name)}  {name}\n" for name in FILES)
(HERE / "MANIFEST.sha256").write_text(text)
print(hashlib.sha256(text.encode()).hexdigest())
