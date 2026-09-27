#!/usr/bin/env python3
"""Replay the balanced six-site cancellation bound and constrained Hessian."""

from pathlib import Path
import hashlib
import json
import balanced_hessian
from quadratic_field import require

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def main():
    dependencies = json.loads((HERE/"dependencies.json").read_text())
    for name, digest in dependencies.items():
        require(hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == digest,
                "Pinned dependency: "+name)
    result = dict(
        status="PASS",
        evidence_status="Written proof with exact supporting checks; independent audit pending",
        checks=balanced_hessian.check(),
        dependencies=dependencies,
        conclusions=[
            "Sharp scalar cost 117/2 in the symmetric two-triple cancellation family",
            "A second strict scalar local minimum with 21 positive transverse directions",
            "Strict exact-W rate bound 16/1053 for the family and a neighborhood of its minimum"],
        limitations=[
            "Unrestricted global W optimum remains open",
            "The new local minimum is for the scalar relaxation",
            "No explicit local-neighborhood radius"])
    paths = [p for p in HERE.iterdir() if p.suffix in (".py", ".md", ".json")
             and p.name != "results.json"]
    paths += [ROOT/"notes/w-state-balanced-three-plus-three-2026-09-27.md"]
    result["sha256"] = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in sorted(paths)}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
