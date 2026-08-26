#!/usr/bin/env python3
"""Export the common two-prime residual support from normalized layer one."""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
MATRIX = HERE / "normalized_anchor_all_layer1_matrix.jsonl"
P1009 = HERE / "results_normalized_anchor_all_layer1_p1009.json"
P1013 = HERE / "results_normalized_anchor_all_layer1_p1013.json"
OUT = HERE / "normalized_anchor_layer1_residual_support.txt"
RESULTS = HERE / "results_normalized_anchor_layer1_residual_support.json"


def main():
    first = json.loads(P1009.read_text())
    second = json.loads(P1013.read_text())
    left = dict(first["remainder"])
    right = dict(second["remainder"])
    if left.keys() != right.keys() or len(left) != 96841:
        raise RuntimeError("two-prime residual supports differ")
    with MATRIX.open() as handle:
        header = json.loads(next(handle))
    rows = [header["rows_hex"][int(index)] for index in left]
    histogram = Counter(len(row) // 2 for row in rows)
    OUT.write_text("\n".join(f"ROW {row or '-'}" for row in sorted(rows)) + "\n")
    result = {
        "status": "exact common two-prime support; coefficients remain modular",
        "matrix_sha256": sha256(MATRIX.read_bytes()).hexdigest(),
        "p1009_sha256": sha256(P1009.read_bytes()).hexdigest(),
        "p1013_sha256": sha256(P1013.read_bytes()).hexdigest(),
        "support_sha256": sha256(OUT.read_bytes()).hexdigest(),
        "support_rows": len(rows),
        "degree_histogram": dict(sorted(histogram.items())),
        "scope": (
            "This support seeds target-overlap closure only. Prime-dependent "
            "coefficients are not reconstructed and no exact residual is claimed."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    RESULTS.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("normalized residual support: PASS")
    print("rows/degrees:", len(rows), dict(sorted(histogram.items())))
    print("support sha256:", result["support_sha256"])
    print("logical sha256:", result["logical_sha256"])


if __name__ == "__main__":
    main()
