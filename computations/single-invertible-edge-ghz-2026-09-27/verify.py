#!/usr/bin/env python3
"""Replay edge identities and support for single-invertible-edge GHZ onset."""

from pathlib import Path
import hashlib
import json
import edge_projection as E

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def main():
    dependencies = json.loads((HERE / "dependencies.json").read_text())
    for name, digest in dependencies.items():
        E.require(hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest,
                  "Pinned dependency: " + name)
    result = dict(
        status="PASS",
        evidence_status="Written proof with exact supporting checks; independent audit pending",
        checks=E.check(),
        dependencies=dependencies,
        conclusions=[
            "One uniformly invertible edge suffices for fifth-power GHZ onset",
            "The combined onset estimate is uniform away from single rank-one edges",
            "Conditioned bilinear responses leave a controlled rank-one product remainder",
            "A determinant-tangent plane retains at least one quarter of binary GHZ squared norm, sharply"],
        limitations=[
            "Unrestricted square-root rate law remains open",
            "The onset theorem concerns full-support single-color six-site zero limits",
            "Uniform onset near single rank-one edge directions remains open",
            "Source-distance onset does not give the required error-versus-signal bound",
            "Auxiliary product examples are not GHZ counterexamples"])
    paths = [p for p in HERE.iterdir() if p.suffix in (".py", ".md", ".json")
             and p.name != "results.json"]
    paths.append(ROOT / "notes/single-invertible-edge-ghz-onset-2026-09-27.md")
    result["sha256"] = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in sorted(paths)}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
