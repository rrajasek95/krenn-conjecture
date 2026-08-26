#!/usr/bin/env python3
"""Verify package manifest, authoritative pins, and terminal status."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20): h.update(block)
    return h.hexdigest()


def main() -> None:
    names = []
    for line in (HERE / "MANIFEST.sha256").read_text().splitlines():
        digest, name = line.split("  ", 1)
        assert len(digest) == 64 and name and ".." not in Path(name).parts
        assert sha(HERE / name) == digest, name
        names.append(name)
    assert len(names) == len(set(names))
    required = {"REPORT.md", "PINS.json", "results_structured_dual_audit.json",
                "results_resource_replay.json", "results_final_audit.json",
                "target/release/audit_d12_structured_dual"}
    assert required <= set(names)
    pins = json.loads((HERE / "PINS.json").read_text())
    assert pins["prime"] == 1_073_741_827
    for name, digest in pins["files"].items(): assert sha(ROOT / name) == digest, name
    result = json.loads((HERE / "results_structured_dual_audit.json").read_text())
    resource = json.loads((HERE / "results_resource_replay.json").read_text())
    audit = json.loads((HERE / "results_final_audit.json").read_text())
    assert result["status"] == "PASS_NEGATIVE_STRUCTURAL_DIAGNOSIS"
    assert result["global_incidence_closed"] is False
    assert resource["status"] == "PASS" and resource["peak_rss_bytes"] < 4 * 1024**3
    assert audit["status"] == "PASS_NEGATIVE_DIAGNOSIS_SEALED"
    assert audit["result_sha256"] == sha(HERE / "results_structured_dual_audit.json")
    print(json.dumps({"status":"PASS", "manifest_entries":len(names), "external_pins":len(pins["files"])}, sort_keys=True))


if __name__ == "__main__": main()
