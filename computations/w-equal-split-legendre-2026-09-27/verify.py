#!/usr/bin/env python3
"""Replay the equal-split all-even W-design gap with rational arithmetic."""

from pathlib import Path
import hashlib
import json
from algebra import check, require

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def main():
    dependencies = json.loads((HERE / "dependencies.json").read_text())
    for name, digest in dependencies.items():
        require(hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest,
                "Pinned dependency: " + name)
    result = dict(
        status="PASS",
        evidence_status="Written proof with exact supporting checks; independent audit pending",
        checks=check(),
        dependencies=dependencies,
        conclusions=[
            "Equal-size two-group ground family has scalar cost at least (81/80) F_star for all n=2m>=6",
            "Every colored exact-W completion has rate strictly below (80/81) R_star",
            "Explicit geometric rate loss for the family from n=16 onward",
            "Exact family scalar minimum is a finite minimum of Legendre quadrature-weight expressions"],
        limitations=[
            "Unrestricted global W optimum remains open",
            "Ground weights are constant within each group and across the groups, up to site phases",
            "No higher-dimensional local-minimum classification",
            "Rate upper bounds are not asserted attained"])
    paths = [p for p in HERE.iterdir() if p.suffix in (".py", ".md", ".json")
             and p.name != "results.json"]
    paths += [ROOT / "notes/w-state-equal-split-legendre-2026-09-27.md"]
    result["sha256"] = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in sorted(paths)}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
