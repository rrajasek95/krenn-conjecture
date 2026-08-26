#!/usr/bin/env python3
"""Freeze the exact post-unary T-square residual for whole cutoff<17 closure."""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "results_sparse_r8_square_collected.json"
R8_SEED = HERE / "sparse_r8_seed.txt"
OUT = HERE / "whole_cutoff17_seed.txt"
RESULTS = HERE / "results_whole_cutoff17_seed.json"
SOURCE_SHA = "234bfc896116584b8e3c3778771888bd43782a55eea2ebcb30fb85ccc7abee23"


def main():
    if sha256(SOURCE.read_bytes()).hexdigest() != SOURCE_SHA:
        raise RuntimeError("collected sparse-R8 square changed")
    source = json.loads(SOURCE.read_text())
    if not source["complete"] or source["target_scale"] != "72^2/2304":
        raise RuntimeError("collected target is incomplete or normalization changed")
    seed_lines = R8_SEED.read_text().splitlines()
    anchors = next(line for line in seed_lines if line.startswith("ANCHORS "))
    actions = [line for line in seed_lines if line.startswith("ACTION ")]
    if len(actions) != 2304:
        raise RuntimeError("orbit0 stabilizer order changed")
    denominator_histogram = {}
    with OUT.open("w") as handle:
        handle.write("KRENN_WHOLE_CUTOFF17_T2_SEED_V1\n")
        handle.write("DEGREE 24\nCUTOFF 17\n")
        handle.write(anchors + "\n")
        for action in actions:
            handle.write(action + "\n")
        for row_hex, stored_coefficient in source["target"]:
            coefficient = Fraction(9 * stored_coefficient, 4)
            denominator_histogram[coefficient.denominator] = (
                denominator_histogram.get(coefficient.denominator, 0) + 1
            )
            handle.write(f"TARGET {row_hex} {coefficient.numerator} "
                         f"{coefficient.denominator}\n")
    result = {
        "status": "exact post-unary target seed for whole degree24 cutoff<17 closure",
        "source_sha256": SOURCE_SHA,
        "seed_sha256": sha256(OUT.read_bytes()).hexdigest(),
        "stabilizer_order": len(actions),
        "degree": 24,
        "cutoff": 17,
        "target_K_degree": 16,
        "target_row_orbits": len(source["target"]),
        "target_coefficient_denominator_histogram": denominator_histogram,
        "normalization": (
            "stored convolution coefficient c represents full-G quotient "
            "mass (72^2/2304)c=(9/4)c; unary source provenance is the "
            "lex-first mixed anchor assignment rule frozen upstream"
        ),
        "scope": (
            "Closure must add every incident H_w times degree-20 monomial "
            "with minimum K-degree below 17 and every output row of K-degree "
            "below 17; no staged leading-form correction is permitted."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    RESULTS.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("whole cutoff17 seed: PASS")
    print("rows/actions:", result["target_row_orbits"], len(actions))
    print("seed sha256:", result["seed_sha256"])
    print("logical sha256:", result["logical_sha256"])


if __name__ == "__main__":
    main()
