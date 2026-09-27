#!/usr/bin/env python3
"""Replay binary adjugate certificates and the same-color onset criterion."""

from pathlib import Path
import hashlib
import json
import adjugate_response as A

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def main():
    dependencies = json.loads((HERE / "dependencies.json").read_text())
    for name, digest in dependencies.items():
        A.require(hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest,
                  "Pinned dependency: " + name)
    result = dict(
        status="PASS",
        evidence_status="Written proof with exact supporting checks; independent audit pending",
        checks=A.check(),
        dependencies=dependencies,
        conclusions=[
            "Binary adjugate/output contraction equals a quadratic four-site response expression",
            "The contraction norm is at most half the local squared response norm, sharply",
            "A comparable same-color edge component suffices for fifth-power GHZ onset",
            "The combined onset estimate is uniform away from thirty different-color projective axes"],
        limitations=[
            "Unrestricted square-root rate law remains open",
            "The onset theorem concerns full-support single-color six-site zero limits",
            "Perturbations near the thirty remaining axes are not controlled by this theorem",
            "Source-distance onset does not establish the required error-versus-signal inequality",
            "The determinant mechanism predates this application in the repository"])
    paths = [p for p in HERE.iterdir() if p.suffix in (".py", ".md", ".json")
             and p.name != "results.json"]
    paths.append(ROOT / "notes/binary-adjugate-ghz-onset-2026-09-27.md")
    result["sha256"] = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in sorted(paths)}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
