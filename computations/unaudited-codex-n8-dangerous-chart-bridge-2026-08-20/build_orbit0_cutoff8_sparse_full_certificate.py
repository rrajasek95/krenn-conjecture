#!/usr/bin/env python3
"""Lift the exact 32-term cutoff-8 core identity through singleton pivots."""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
RUST = HERE.parent / "unaudited-codex-anchor-k-rust-2026-08-20"
PRODUCER_PATH = RUST / "verify_orbit0_cutoff8_exact.py"
SPEC = importlib.util.spec_from_file_location("cutoff8_exact", PRODUCER_PATH)
PRODUCER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PRODUCER)
CORE = HERE / "results_orbit0_cutoff8_sparse_core_certificate.json"
OUT = HERE / "results_orbit0_cutoff8_sparse_full_certificate.json"


def main():
    core_data = json.loads(CORE.read_text())
    coefficients = {int(index): Fraction(value)
                    for index, value in core_data["solution"]}
    header = PRODUCER.core_replay(coefficients)
    chosen = PRODUCER.full_replay(coefficients)
    terms = [{
        "coefficient": [coefficient.numerator, coefficient.denominator],
        "core_index": item.get("core_index"),
        "multiplier_cell_ids": item["multiplier_cell_ids"],
        "pivot_order": item.get("pivot_order"),
        "role": item["role"],
        "source_closure_column": item["source_closure_column"],
        "word": item["word"],
    } for item, coefficient in chosen]
    terms.sort(key=lambda item: item["source_closure_column"])
    result = {
        "status": "exact quotient lift; independent raw-105 replay required",
        "chart": "zero0_three_identical_perfect_matchings",
        "cutoff": 8,
        "core_certificate_sha256": sha256(CORE.read_bytes()).hexdigest(),
        "matrix_sha256": sha256(PRODUCER.MATRIX.read_bytes()).hexdigest(),
        "seed_sha256": sha256(PRODUCER.SEED.read_bytes()).hexdigest(),
        "source_support_ledger_sha256": sha256(PRODUCER.SOURCE.read_bytes()).hexdigest(),
        "row_count": header["row_count"],
        "column_count": header["column_count"],
        "core_terms": len(coefficients),
        "nonzero_source_terms": len(terms),
        "max_denominator": max(term["coefficient"][1] for term in terms),
        "exact_core_replay": True,
        "exact_reverse_pivot_replay": True,
        "mutation_fires": True,
        "terms": terms,
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("orbit0 cutoff8 sparse core/full lift: PASS")
    print("core/full terms:", len(coefficients), len(terms))
    print("logical sha256:", result["logical_sha256"])
    print("file sha256:", sha256(OUT.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
