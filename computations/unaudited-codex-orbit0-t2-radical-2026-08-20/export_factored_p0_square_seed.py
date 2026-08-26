#!/usr/bin/env python3
"""Extract the exact collected P0-square target for the factored subideal J."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "results_sparse_r8_square_collected.json"
R8_SEED = HERE / "sparse_r8_seed.txt"
OUT = HERE / "factored_p0_square_seed.txt"
RESULTS = HERE / "results_factored_p0_square_seed.json"
SOURCE_SHA = "234bfc896116584b8e3c3778771888bd43782a55eea2ebcb30fb85ccc7abee23"
PURE_ZERO_SQUARE = bytes(sorted([0, 117, 198, 243] * 2))


def subtract_factor(row: bytes, factor: bytes) -> bytes:
    remaining = Counter(row)
    remaining.subtract(factor)
    if any(value < 0 for value in remaining.values()):
        raise RuntimeError("collected survivor lacks the pure-zero anchor square")
    answer = bytes(sorted(cell for cell, count in remaining.items()
                          for _ in range(count)))
    if len(answer) != 16:
        raise RuntimeError("factored target row did not have degree sixteen")
    return answer


def main():
    if sha256(SOURCE.read_bytes()).hexdigest() != SOURCE_SHA:
        raise RuntimeError("collected sparse-R8 square changed")
    source = json.loads(SOURCE.read_text())
    if not source["complete"] or source["target_scale"] != "72^2/2304":
        raise RuntimeError("collected target is incomplete or normalization changed")
    lines = R8_SEED.read_text().splitlines()
    anchors = next(line.split()[1] for line in lines if line.startswith("ANCHORS "))
    actions = [line for line in lines
               if line.startswith("ACTION ") and line.split()[2][0] == "0"]
    if len(actions) != 768:
        raise RuntimeError("pure-zero stabilizer is not order 768")

    target = {}
    denominator_histogram = Counter()
    for row_hex, scaled_coefficient in source["target"]:
        row = subtract_factor(bytes.fromhex(row_hex), PURE_ZERO_SQUARE)
        # The full G-orbit contains the three transported pure-colour copies.
        # Its quotient mass is (9/4)c; one G_0 orbit therefore has mass (3/4)c.
        coefficient = Fraction(3 * scaled_coefficient, 4)
        if row in target:
            raise RuntimeError("full-G canonical target split after pure-zero normalization")
        target[row] = coefficient
        denominator_histogram[coefficient.denominator] += 1
    if len(target) != source["target_row_orbits"]:
        raise RuntimeError("factored target support count changed")

    with OUT.open("w") as handle:
        handle.write("KRENN_FACTORED_P0_SQUARE_SEED_V1\n")
        handle.write(f"ANCHORS {anchors}\n")
        handle.write("DEGREE 16\n")
        handle.write("COMMON_FACTOR 00007575c6c6f3f3\n")
        for action in actions:
            handle.write(action + "\n")
        for row, coefficient in sorted(target.items()):
            handle.write(f"TARGET {row.hex()} {coefficient.numerator} "
                         f"{coefficient.denominator}\n")
    result = {
        "status": "exact collected factored P0-square target seed",
        "source_sha256": SOURCE_SHA,
        "seed_sha256": sha256(OUT.read_bytes()).hexdigest(),
        "source_target_scale": source["target_scale"],
        "p0_quotient_normalization": (
            "full-G quotient mass is (9/4)c and consists of three transported "
            "pure-colour copies; the G_0 quotient target mass is (3/4)c"
        ),
        "common_factor": "(x01_00*x23_00*x45_00*x67_00)^2",
        "factored_degree": 16,
        "factored_K_degree": 16,
        "stabilizer_order": len(actions),
        "target_row_orbits": len(target),
        "coefficient_denominator_histogram": dict(sorted(denominator_histogram.items())),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    RESULTS.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("factored P0-square target seed: PASS")
    print("rows/stabilizer:", len(target), len(actions))
    print("seed sha256:", result["seed_sha256"])
    print("logical sha256:", result["logical_sha256"])


if __name__ == "__main__":
    main()
