#!/usr/bin/env python3
"""Replay exact support for balanced responses and rank-free GHZ cofactor tests."""

from pathlib import Path
import hashlib
import json
import balanced_response as B

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def main():
    dependencies = json.loads((HERE / "dependencies.json").read_text())
    for name, digest in dependencies.items():
        B.require(hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest,
                  "Pinned dependency: " + name)
    result = dict(
        status="PASS",
        evidence_status="Written proof with exact supporting checks; independent audit pending",
        checks=B.check(),
        dependencies=dependencies,
        conclusions=[
            "Balanced bilinear responses have at most one weak input direction in any finite local dimensions",
            "The uniform perpendicular singular-value factor 1/sqrt(2) is sharp",
            "A common anchored neighbor or an outside anchored four-cycle proves fifth-power GHZ onset without matrix-rank assumptions",
            "Both zero endpoint cofactor rows are covered for every edge matrix rank",
            "Ground cofactor tests reduce the thirty projective candidates to sixteen for the displayed exact ground fixture"],
        limitations=[
            "Unrestricted square-root rate law remains open",
            "The onset theorem concerns full-support single-color six-site limits",
            "Some different-color single-cell perturbation directions remain open",
            "The source-distance estimate does not establish the required error-versus-signal inequality",
            "General inequalities rely on the written proof; finite exact fixtures alone do not prove them",
            "Independent audit is pending"])
    paths = [p for p in HERE.iterdir() if p.suffix in (".py", ".md", ".json")
             and p.name != "results.json"]
    paths.append(ROOT / "notes/balanced-response-ghz-onset-2026-09-27.md")
    result["sha256"] = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in sorted(paths)}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
