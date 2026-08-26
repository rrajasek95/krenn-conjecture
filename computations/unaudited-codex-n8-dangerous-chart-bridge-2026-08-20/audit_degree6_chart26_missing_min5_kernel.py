#!/usr/bin/env python3
"""Exact counterexample to completeness of chosen min5 corrections."""

from __future__ import annotations

from hashlib import sha256
import argparse
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
DUAL_PATH = HERE / "probe_degree6_chart26_relative_dual.py"
SPEC = importlib.util.spec_from_file_location("relative_dual", DUAL_PATH)
DUAL = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(DUAL)
LK = DUAL.LK
BASE = DUAL.BASE
OUT = HERE / "results_degree6_chart26_missing_min5_kernel.json"


def column_record(column):
    return {
        "word": BASE.word_name(column[0]),
        "multiplier_cell_ids": list(column[1]),
        "multiplier": [BASE.cell_name(BASE.CELLS[cell])
                       for cell in column[1]],
    }


def audit():
    component = LK.build_frozen_degree5_component(1009)
    seen = {}
    witness = None
    for column in component["columns5"]:
        tail5 = LK.degree_tail(column, 5)
        if sum(tail5.values()) != 1:
            continue
        row = next(iter(tail5))
        scalar = (LK.degree_tail(column, 6).get(DUAL.R_PLUS, 0)
                  - LK.degree_tail(column, 6).get(DUAL.R_MINUS, 0))
        if row in seen and seen[row][0] != scalar:
            witness = (row, seen[row][1], seen[row][0], column, scalar)
            break
        seen.setdefault(row, (scalar, column))
    if witness is None:
        raise RuntimeError("missing-min5-kernel witness disappeared")
    row, column_a, scalar_a, column_b, scalar_b = witness
    tail5_a = LK.degree_tail(column_a, 5)
    tail5_b = LK.degree_tail(column_b, 5)
    if tail5_a != tail5_b or tail5_a != {row: 1}:
        raise RuntimeError("witness is not a literal singleton difference")
    pairing = scalar_a - scalar_b
    if not pairing:
        raise RuntimeError("witness no longer defeats the proposed dual")
    core = {
        "status": "UNAUDITED exact integer counterexample",
        "chart": 26,
        "legacy_one_based_chart": 29,
        "shared_degree5_row": row.hex(),
        "column_a": column_record(column_a),
        "column_b": column_record(column_b),
        "kernel_direction": "column_a - column_b",
        "degree_below_5_boundary_is_zero": True,
        "degree5_boundary_is_zero": True,
        "d6_lambda_rows": {
            "minus": DUAL.R_MINUS.hex(),
            "plus": DUAL.R_PLUS.hex(),
        },
        "lambda_tail_on_column_a": scalar_a,
        "lambda_tail_on_column_b": scalar_b,
        "lambda_tail_on_kernel_direction": pairing,
        "conclusion": (
            "the chosen-singleton 3274-transfer family is not the full "
            "through-degree5 source kernel"
        ),
    }
    encoded = json.dumps(core, sort_keys=True, separators=(",", ":"))
    core["result_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    return core


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()
    result = audit()
    if args.write_results:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("missing min5 kernel counterexample: PASS")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
