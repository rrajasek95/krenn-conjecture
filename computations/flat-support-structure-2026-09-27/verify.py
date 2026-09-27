#!/usr/bin/env python3
"""Exact support for the flat-support classification and rank-free star bound."""

from pathlib import Path
import hashlib
import json
import stars
import graph_census
from algebra import require

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def main():
    dependencies = json.loads((HERE/"dependencies.json").read_text())
    for name, digest in dependencies.items():
        require(hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == digest,
                "Pinned dependency: "+name)
    census = graph_census.check()
    require(census["total_graphs"] == 32768 and census["realized_supports"] == 348,
            "This package must run the complete census, not the earlier restricted graph")
    result = dict(status="PASS",
                  evidence_status="Written proofs with exact supporting checks; independent audit pending",
                  star_bound=stars.check(), supports=census, dependencies=dependencies,
                  unresolved=["Unrestricted GHZ square-root rate law",
                              "Disappearing star arms and singular four-site critical cores"])
    paths = [p for p in HERE.iterdir() if p.suffix in (".md", ".py", ".json")
             and p.name != "results.json"]
    paths += [ROOT/"notes"/name for name in (
        "rank-free-star-response-bound-2026-09-27.md",
        "four-site-flat-support-classification-2026-09-27.md")]
    result["sha256"] = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in sorted(paths)}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
