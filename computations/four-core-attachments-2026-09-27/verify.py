#!/usr/bin/env python3
"""Replay exact support for the four-core attachment and GHZ onset theorems."""

from pathlib import Path
import hashlib
import json
import core_attachments
import six_site_split
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
        attachment_theorem=core_attachments.check(),
        output_identities=six_site_split.check(),
        dependencies=dependencies,
        consequence="Fifth-power GHZ onset near every non-star four-active-site flat core",
        unresolved=["Unrestricted GHZ square-root rate law",
                    "Onset near triangles and stars with at most three arms"])
    paths = [p for p in HERE.iterdir() if p.suffix in (".py", ".md", ".json")
             and p.name != "results.json"]
    paths += [ROOT/"notes/four-core-attachment-ghz-bound-2026-09-27.md"]
    result["sha256"] = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in sorted(paths)}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
