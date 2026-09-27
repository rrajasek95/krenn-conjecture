#!/usr/bin/env python3
"""Exact supporting checks; the general claims also require the written proofs."""

from pathlib import Path
import hashlib
import json
import cores
import projections
import star_identity
import supports
from algebra import require

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
NOTES = (
    "flat-four-response-five-clique-2026-09-27.md",
    "star-response-identity-and-binary-flat-cores-2026-09-27.md",
    "rank25-critical-directions-2026-09-27.md",
    "ghz-critical-direction-normal-form-2026-09-27.md",
)


def main():
    dependencies = json.loads((HERE/"dependencies.json").read_text())
    for name, expected in dependencies.items():
        require(hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == expected,
                "Pinned dependency: "+name)
    result = dict(status="PASS",
                  evidence_status="Written proofs with exact supporting checks; independent audit pending",
                  cores=cores.check(), star_identity=star_identity.check(),
                  rank25_supports=supports.check(), ghz_projections=projections.check(),
                  dependencies=dependencies,
                  unresolved=["Unrestricted GHZ square-root rate law",
                              "Uniform stability through rank-degenerate critical families"])
    files = [p for p in HERE.iterdir() if p.suffix in (".py", ".md", ".json")
             and p.name != "results.json"]
    files += [ROOT/"notes"/name for name in NOTES]
    result["sha256"] = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in sorted(files)}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
