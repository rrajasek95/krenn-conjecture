#!/usr/bin/env python3
"""Export the certified 9,607 source terms for exact K9-tail expansion."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
BRIDGE = HERE.parent / "unaudited-codex-n8-dangerous-chart-bridge-2026-08-20"
SOURCE = BRIDGE / "results_orbit0_cutoff9_sparse_r8.json"
R8_SEED = HERE / "sparse_r8_seed.txt"
OUT = HERE / "sparse_r8_k9_tail_terms.txt"
RESULTS = HERE / "results_sparse_r8_k9_tail_terms.json"
EXPECTED = "877ca35865130bd9ca55f19387b44d9473acd2b47d5eddd2d29c1718831cf968"


def main():
    payload = json.loads(SOURCE.read_text())
    if payload["result_sha256"] != EXPECTED:
        raise RuntimeError("sparse R8 certificate changed")
    seed = R8_SEED.read_text().splitlines()
    anchors = next(line for line in seed if line.startswith("ANCHORS "))
    actions = [line for line in seed if line.startswith("ACTION ")]
    if len(actions) != 2304 or len(payload["terms"]) != 9607:
        raise RuntimeError("source/action count changed")
    lines = ["KRENN_SPARSE_R8_K9_TAIL_TERMS_V1", anchors, *actions]
    for index, term in enumerate(payload["terms"]):
        numerator, denominator = term["coefficient"]
        if denominator != 1:
            raise RuntimeError("source coefficient unexpectedly nonintegral")
        multiplier = bytes(term["multiplier_cell_ids"]).hex()
        lines.append(
            f"TERM {index} {numerator} {term['word']} {multiplier} "
            f"{term['source_closure_column']} {term['role']}"
        )
    text = "\n".join(lines) + "\n"
    OUT.write_text(text)
    result = {
        "status": "exact source-term interface for sparse-R8 K9 tail",
        "source_logical_sha256": EXPECTED,
        "source_file_sha256": sha256(SOURCE.read_bytes()).hexdigest(),
        "interface_sha256": sha256(text.encode("ascii")).hexdigest(),
        "stabilizer_order": len(actions),
        "source_terms": len(payload["terms"]),
        "pivot_terms": sum(term["role"] == "pivot" for term in payload["terms"]),
        "core_terms": sum(term["role"] == "core" for term in payload["terms"]),
        "coefficient_denominator": 1,
        "tail_formula": "E9=(H0*H1*H2)_K9-(sum certificate_source_terms)_K9",
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    RESULTS.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("sparse R8 K9 tail terms: PASS")
    print("terms/actions:", len(payload["terms"]), len(actions))
    print("interface sha256:", result["interface_sha256"])
    print("logical sha256:", result["logical_sha256"])


if __name__ == "__main__":
    main()
