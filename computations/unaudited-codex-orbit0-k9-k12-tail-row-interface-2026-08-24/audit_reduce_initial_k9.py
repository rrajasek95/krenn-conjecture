#!/usr/bin/env python3
"""Independent audit of the exact single-pivot K9 reduction stage."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE_PATH = HERE / "audit_k9_k12_tail_rows.py"
SPEC = importlib.util.spec_from_file_location("tail_rows_base", BASE_PATH)
BASE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BASE)
RESULT = HERE / "results_reduce_initial_k9.json"
ROWS = HERE / "reduce_initial_k9_children.tsv"
OUT = HERE / "results_reduce_initial_k9_audit.json"

PINS = {
    RESULT: "c2ebe427bfe73484b494be6c5db0e0542dcb5e561ff39a361e1425e45d0940d1",
    ROWS: "71c3cef0cfa85edc0647f3f1e7ec1604bcf03069e84f413327dadf1f70256745",
}
EXPECTED_COUNTS = {11: 591214, 12: 1587892, 13: 2979882}
EXPECTED_MASS = {11: 115782912, 12: 308754432, 13: 578914560}
EXPECTED_L1 = {11: 1219600320, 12: 3275510400, 13: 6146793600}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    for path, digest in PINS.items():
        require(sha256(path) == digest, f"pin changed: {path}")
    result = json.loads(RESULT.read_text())
    require(result["status"] == "PASS_EXACT_SINGLE_PIVOT_INITIAL_STAGE", "bad producer status")
    require(result["input_degree"] == 9 and result["input_rows"] == 49988, "input census changed")
    require(result["pivotable_rows"] == 49988 and result["terminal_rows"] == 0, "pivot census changed")
    require(result["raw_children_by_degree"] == {"11": 599856, "12": 1599616, "13": 2999280}, "raw ratios changed")

    anchors, actions = BASE.parse_seed()
    dual = {}
    lines = BASE.DUAL.read_text().splitlines()
    for line in lines[1:]:
        partition, coefficient = line.split("\t")
        dual[tuple(map(int, partition.split(",")))] = int(coefficient)
    require(len(dual) == 77, "dual support changed")

    counts = Counter()
    masses = Counter()
    l1 = Counter()
    charges = Counter()
    total = sum(EXPECTED_COUNTS.values())
    targets = {index * total // 257 for index in range(257)}
    samples = []
    previous = None
    with ROWS.open() as handle:
        require(handle.readline().rstrip("\n") == "degree\trow\tcoefficient", "bad ledger header")
        for ordinal, line in enumerate(handle):
            degree_text, row_hex, coefficient_text = line.rstrip("\n").split("\t")
            degree, coefficient = int(degree_text), int(coefficient_text)
            key = (degree, row_hex)
            require(previous is None or previous < key, "ledger not strictly sorted")
            previous = key
            require(degree in EXPECTED_COUNTS and coefficient != 0, "bad output record")
            row = tuple(bytes.fromhex(row_hex))
            require(len(row) == 24 and tuple(sorted(row)) == row, "bad literal row")
            require(sum(cell not in set(anchors) for cell in row) == degree, "output K-degree mismatch")
            counts[degree] += 1
            masses[degree] += coefficient
            l1[degree] += abs(coefficient)
            charges[degree] += coefficient * dual.get(BASE.cycle_partition(row), 0)
            if ordinal in targets:
                samples.append((ordinal, row))
    require(dict(counts) == EXPECTED_COUNTS, "output counts changed")
    require(dict(masses) == EXPECTED_MASS, "output mass changed")
    require(dict(l1) == EXPECTED_L1, "output L1 changed")
    require(sum(charges.values()) == -18809856, "77-charge was not conserved")
    require(len(samples) == 257, "sample census changed")
    for ordinal, row in samples:
        require(row == min(BASE.transform_row(row, action) for action in actions), f"row {ordinal} not H-minimal")

    payload = {
        "status": "PASS_INDEPENDENT_SINGLE_PIVOT_K9_STAGE_AUDIT",
        "input_rows": 49988,
        "input_charge": -18809856,
        "output_nonzero_orbits_by_degree": EXPECTED_COUNTS,
        "output_mass_by_degree": EXPECTED_MASS,
        "output_l1_by_degree": EXPECTED_L1,
        "output_charge_by_degree": dict(charges),
        "output_charge_total": sum(charges.values()),
        "distributed_natural_H_minimum_checks": len(samples),
        "nonzero_output_to_raw_child_ratio": 5158988 / 5198752,
        "scope": "validates one source-faithful K9 layer; the near-unit row-growth blocks naive full recursion",
        "pins": {str(path.relative_to(ROOT)): digest for path, digest in PINS.items()},
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["logical_sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
