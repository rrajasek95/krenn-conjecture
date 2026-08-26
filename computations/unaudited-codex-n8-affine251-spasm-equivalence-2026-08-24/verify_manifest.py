#!/usr/bin/env python3
"""Strict manifest/status replay; never launches an exporter or solver."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            h.update(block)
    return h.hexdigest()


def main() -> None:
    entries = []
    for number, line in enumerate((HERE / "MANIFEST.sha256").read_text().splitlines(), 1):
        assert line and "  " in line, f"bad manifest line {number}"
        digest, name = line.split("  ", 1)
        assert len(digest) == 64 and all(c in "0123456789abcdef" for c in digest)
        assert name and not name.startswith("/") and ".." not in Path(name).parts
        path = HERE / name
        assert path.is_file() and sha(path) == digest, f"manifest mismatch: {name}"
        entries.append(name)
    assert len(entries) == len(set(entries))
    required = {
        "REPORT.md",
        "results_spasm_equivalence_d10.json",
        "results_spasm_equivalence_d11_gate_failure.json",
        "results_final_audit.json",
        "matrix_d10_integer_AT.sms",
        "matrix_d11_integer_AT.sms",
        "target/release/export_affine251_spasm",
        "target/release/build/affine251-spasm-export-907d4950f29001f9/out/retained_main.rs",
    }
    assert required <= set(entries)
    d10 = json.loads((HERE / "results_spasm_equivalence_d10.json").read_text())
    d11 = json.loads((HERE / "results_spasm_equivalence_d11_gate_failure.json").read_text())
    audit = json.loads((HERE / "results_final_audit.json").read_text())
    assert d10["status"] == "PASS" and d10["degree"] == 10
    assert d11["status"] == "GATE_FAILED_END_TO_END_WALL"
    assert d11["equivalence_accepted"] is False and not d11["solution_artifacts"]
    assert audit["status"] == "PASS_FAIL_CLOSED"
    assert audit["hostile_mutations_rejected"] == 9
    assert audit["d10_result_sha256"] == sha(HERE / "results_spasm_equivalence_d10.json")
    assert audit["d11_failure_sha256"] == sha(HERE / "results_spasm_equivalence_d11_gate_failure.json")
    print(json.dumps({"status": "PASS", "manifest_entries": len(entries)}, sort_keys=True))


if __name__ == "__main__":
    main()
