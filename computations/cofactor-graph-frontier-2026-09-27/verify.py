#!/usr/bin/env python3
"""Replay exhaustive cofactor graphs, exact examples, and matching identities."""

from pathlib import Path
import hashlib
import json
import cofactor_graphs as G

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def main():
    dependencies = json.loads((HERE / "dependencies.json").read_text())
    for name, digest in dependencies.items():
        G.require(hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest,
                  "Pinned dependency: " + name)
    result = dict(
        status="PASS",
        evidence_status="Written proof and exact exhaustive graph certificate; independent audit pending",
        checks=G.check(),
        dependencies=dependencies,
        conclusions=[
            "All 32768 six-vertex support graphs are classified by two independent exact tests",
            "Degree-four anchors and a six-cycle of anchors each give onset in all nearby source directions",
            "Only three cofactor graph types retain unresolved different-color single-cell directions",
            "At most sixteen projective onset directions remain at any full-support single-color ground zero",
            "Two anchor configurations suffice for the remaining full-support single-color onset problem",
            "Both residual anchor configurations occur in exact full-support ground examples"],
        limitations=[
            "Unrestricted square-root rate law remains open",
            "The residual configurations are continuous families, not finitely many source matrices",
            "The graph condition is necessary; not all admissible graphs are claimed to be ground-realizable",
            "The fifth-power onset estimate does not give the required error-versus-signal comparison",
            "Analytic estimates use the written proof and prior response proofs",
            "Independent audit is pending"])
    paths = [p for p in HERE.iterdir() if p.suffix in (".py", ".md", ".json")
             and p.name != "results.json"]
    paths.append(ROOT / "notes/cofactor-graph-ghz-frontier-2026-09-27.md")
    result["sha256"] = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in sorted(paths)}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
