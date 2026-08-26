#!/usr/bin/env python3
"""Replay the sealed failure manifest without launching export or SpaSM."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20): h.update(block)
    return h.hexdigest()


def main() -> None:
    entries = []
    for line in (HERE / "MANIFEST.sha256").read_text().splitlines():
        digest, name = line.split("  ", 1)
        assert len(digest) == 64 and name and ".." not in Path(name).parts
        assert sha(HERE / name) == digest, name
        entries.append(name)
    assert len(entries) == len(set(entries))
    required = {"REPORT.md", "results_cegar635_spasm_gate_failure.json",
                "results_final_audit.json", "matrix_cegar635_left_orientation.sms",
                "target/release/cegar635_spasm_bridge"}
    assert required <= set(entries)
    result = json.loads((HERE / "results_cegar635_spasm_gate_failure.json").read_text())
    audit = json.loads((HERE / "results_final_audit.json").read_text())
    assert result["status"] == "GATE_FAILED_WALL_NO_SOLUTION"
    assert result["equivalence_accepted"] is False and result["solution_artifacts"] == []
    assert result["scope"]["second_prime_run"] is False
    assert result["scope"]["full_closure_run"] is False
    assert audit["status"] == "PASS_FAIL_CLOSED" and audit["hostile_mutations_rejected"] == 9
    assert audit["failure_result_sha256"] == sha(HERE / "results_cegar635_spasm_gate_failure.json")
    print(json.dumps({"status": "PASS", "entries": len(entries)}, sort_keys=True))


if __name__ == "__main__": main()
