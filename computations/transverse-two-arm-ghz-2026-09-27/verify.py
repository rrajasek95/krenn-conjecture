#!/usr/bin/env python3
"""Replay exact support for transverse and coherent two-arm GHZ estimates."""

from pathlib import Path
import hashlib
import json
import transverse_arms as T

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def main():
    dependencies = json.loads((HERE / "dependencies.json").read_text())
    for name, digest in dependencies.items():
        T.require(hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest,
                  "Pinned dependency: " + name)
    result = dict(
        status="PASS",
        evidence_status="Written proof with exact supporting checks; independent audit pending",
        checks=T.check(),
        dependencies=dependencies,
        conclusions=[
            "Fifth-power GHZ onset for every uniformly injective two-arm attachment map",
            "One invertible arm suffices without a ground endpoint-row condition",
            "Two rank-one arms with different center lines are covered",
            "Near a shared-center pair, the remaining contribution is bounded by t times the squared closing-edge norm"],
        limitations=[
            "Unrestricted square-root rate law remains open",
            "Unconditional onset near single edges and shared-center rank-one two-arm stars remains open",
            "Source-distance onset does not imply the required error-versus-signal estimate",
            "The full-output scope example is an auxiliary product-output family"])
    paths = [p for p in HERE.iterdir() if p.suffix in (".py", ".md", ".json")
             and p.name != "results.json"]
    paths += [ROOT / "notes/transverse-two-arm-ghz-onset-2026-09-27.md"]
    result["sha256"] = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in sorted(paths)}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
