#!/usr/bin/env python3
"""Exact support for the four-arm kernel classification and GHZ distance estimate."""

from pathlib import Path
import hashlib
import json
import four_arm_kernels
import ground_projection
from algebra import require

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def main():
    dependencies = json.loads((HERE/"dependencies.json").read_text())
    for name, digest in dependencies.items():
        require(hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == digest,
                "Pinned dependency: "+name)
    result = dict(status="PASS",
                  evidence_status="Written proofs with exact supporting checks; independent audit pending",
                  four_arm_kernels=four_arm_kernels.check(),
                  ghz_projection=ground_projection.check(), dependencies=dependencies,
                  consequence="Fifth-power source-distance onset when four non-ground arms stay comparable",
                  unresolved=["Unrestricted GHZ square-root rate law",
                              "Remaining onset geometry on at most four active sites"])
    paths = [p for p in HERE.iterdir() if p.suffix in (".py", ".md", ".json")
             and p.name != "results.json"]
    paths += [ROOT/"notes"/name for name in (
        "four-arm-star-response-2026-09-27.md", "four-arm-ghz-distance-bound-2026-09-27.md")]
    result["sha256"] = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in sorted(paths)}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
