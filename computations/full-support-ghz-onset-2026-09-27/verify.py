#!/usr/bin/env python3
"""Replay exact support for uniform full-support single-color GHZ onset."""

from pathlib import Path
import hashlib
import json
import cycle_balance as C

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def main():
    dependencies = json.loads((HERE / "dependencies.json").read_text())
    for name, digest in dependencies.items():
        C.require(hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest,
                  "Pinned dependency: " + name)
    result = dict(
        status="PASS",
        evidence_status="Written proof with exact supporting checks; independent audit pending",
        checks=C.check(),
        dependencies=dependencies,
        conclusions=[
            "Every full-support single-color six-site zero has a uniform fifth-power GHZ onset bound in all source directions",
            "A balanced flat four-cycle has attachment response Gram equal to twice the identity in arbitrary finite local dimensions",
            "Two anchored triangles joined by an anchored bridge give fifth-power GHZ onset in every nearby source direction",
            "Site scaling and quartet-specific bounds control attachments without matrix-rank assumptions",
            "Any anchored four-cycle suffices for onset by projection at a large outside edge",
            "No critical non-ground directions remain for the full-support single-color source-distance onset theorem"],
        limitations=[
            "Unrestricted square-root rate law remains open",
            "Other zero-output boundary types remain relevant to the unrestricted rate law",
            "Source-distance onset does not prove the required error-versus-signal inequality",
            "Compactness and absorption use the written proof; finite fixtures alone do not prove the theorem",
            "Independent audit is pending"])
    paths = [p for p in HERE.iterdir() if p.suffix in (".py", ".md", ".json")
             and p.name != "results.json"]
    paths.append(ROOT / "notes/full-support-ghz-onset-2026-09-27.md")
    result["sha256"] = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in sorted(paths)}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
