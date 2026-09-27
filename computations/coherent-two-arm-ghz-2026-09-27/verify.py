#!/usr/bin/env python3
"""Replay exact support for the unrestricted-matrix-rank two-arm onset theorem."""

from pathlib import Path
import hashlib
import json
import coherent_arms as C

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
            "Two comparable arms of arbitrary matrix rank suffice for fifth-power GHZ onset",
            "Ground-selected center or leaf anchors control the shared-center rank-one case",
            "The fifth-power source-distance bound is uniform away from single-edge directions"],
        limitations=[
            "Unrestricted square-root rate law remains open",
            "The theorem concerns full-support single-color six-site zero limits",
            "Uniform onset near single-edge directions remains open",
            "Error-versus-signal control remains open even on onset-controlled families",
            "Exact fixtures and scalar certificates support, but do not replace, the analytic proof"])
    paths = [p for p in HERE.iterdir() if p.suffix in (".py", ".md", ".json")
             and p.name != "results.json"]
    paths.append(ROOT / "notes/coherent-two-arm-ghz-onset-2026-09-27.md")
    result["sha256"] = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in sorted(paths)}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
