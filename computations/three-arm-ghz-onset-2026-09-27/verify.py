#!/usr/bin/env python3
"""Replay exact support for the weighted extension and three-arm GHZ theorem."""

from pathlib import Path
import hashlib
import json
import weighted_extensions
from algebra import require

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
        checks=weighted_extensions.check(),
        dependencies=dependencies,
        consequence="Three comparable arms suffice for uniform fifth-power GHZ onset",
        unresolved=["Unrestricted GHZ square-root rate law",
                    "Onset near stars with at most two arms"])
    paths = [p for p in HERE.iterdir() if p.suffix in (".py", ".md", ".json")
             and p.name != "results.json"]
    paths += [ROOT/"notes/three-arm-ghz-distance-bound-2026-09-27.md"]
    result["sha256"] = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in sorted(paths)}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
