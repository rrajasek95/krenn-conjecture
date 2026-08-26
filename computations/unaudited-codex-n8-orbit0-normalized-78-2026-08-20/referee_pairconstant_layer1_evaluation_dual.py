#!/usr/bin/env python3
"""Exact evaluation-dual referee for the 868 x 5,400 first layer.

The matrix is in orbit-total-mass coordinates for the order-2304 orbit-0
anchor stabilizer.  A raw evaluation at the frozen rational common zero is
not orbit invariant, so the dual used here is its exact stabilizer average.
"""

from __future__ import annotations

from array import array
from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MATRIX = (ROOT / "computations" /
          "unaudited-codex-orbit0-t2-radical-2026-08-20" /
          "normalized_anchor_pairconstant_layer1_matrix.jsonl")
BASE_PATH = (ROOT / "computations" /
             "unaudited-codex-n8-dangerous-chart-bridge-2026-08-20" /
             "audit_dangerous_charts.py")
EXPORT_PATH = (ROOT / "computations" /
               "unaudited-codex-n8-dangerous-chart-bridge-2026-08-20" /
               "export_orbit0_cutoff_seed.py")
OUT = HERE / "results_pairconstant_layer1_evaluation_dual.json"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BASE = load_module("n8_pc78_dual_base", BASE_PATH)
EXPORT = load_module("n8_pc78_dual_export", EXPORT_PATH)
Q = Fraction
M0 = ((0, 1), (2, 3), (4, 5), (6, 7))
# Entries are scaled by three, so all orbit-average numerators are integral.
SCALED_CLONE_MATRIX = ((3, -2), (0, -3))


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def scaled_assignment():
    values = {}
    for left, right in M0:
        for colour in BASE.COLORS:
            values[BASE.CELL_ID[(left, right, colour, colour)]] = 3
    for first_pair in range(4):
        for second_pair in range(first_pair + 1, 4):
            for first_clone in range(2):
                for second_clone in range(2):
                    value = SCALED_CLONE_MATRIX[first_clone][second_clone]
                    if not value:
                        continue
                    u = 2 * first_pair + first_clone
                    v = 2 * second_pair + second_clone
                    for colour in BASE.COLORS:
                        values[BASE.CELL_ID[(u, v, colour, colour)]] = value
    return values


def orbit_average_dual(rows):
    """Return exact stabilizer-average evaluations of quotient row reps."""
    scaled_values = scaled_assignment()
    group_order = len(EXPORT.TRANSFORMS)
    require(group_order == 2304, "orbit-0 stabilizer order changed")
    all_actions = (1 << group_order) - 1

    # values_by_cell[cell][action] is in {-3,-2,0,3}; bit masks make the
    # overwhelmingly zero rows cheap to discard before multiplying values.
    values_by_cell = []
    nonzero_action_masks = []
    for cell in range(len(BASE.CELLS)):
        action_values = array(
            "b", (scaled_values.get(transform[cell], 0)
                  for transform in EXPORT.TRANSFORMS)
        )
        mask = 0
        for action, value in enumerate(action_values):
            if value:
                mask |= 1 << action
        values_by_cell.append(action_values)
        nonzero_action_masks.append(mask)

    dual = {}
    live_action_pairs = 0
    degree_live = Counter()
    for row_index, row in enumerate(rows):
        require(not set(row) & EXPORT.ANCHORS,
                "normalized row unexpectedly retains an anchor")
        live = all_actions
        for cell in set(row):
            live &= nonzero_action_masks[cell]
        if not live:
            continue
        live_action_pairs += live.bit_count()
        degree_live[len(row)] += 1
        numerator = 0
        while live:
            lowbit = live & -live
            action = lowbit.bit_length() - 1
            product = 1
            for cell in row:
                product *= values_by_cell[cell][action]
            numerator += product
            live ^= lowbit
        if numerator:
            dual[row_index] = Q(numerator, group_order * 3 ** len(row))
    return dual, live_action_pairs, degree_live


def main():
    digest = sha256()
    with MATRIX.open("rb") as stream:
        header_line = stream.readline()
        digest.update(header_line)
        header = json.loads(header_line)
        require(header["format"] == (
            "krenn-orbit0-normalized-anchor-degree12-"
            "pairconstant-first-layer-v1"), "matrix format changed")
        rows = tuple(bytes.fromhex(item) for item in header["rows_hex"])
        require(len(rows) == header["row_count"] == 283538,
                "matrix row count changed")
        require(header["column_count"] == 5400,
                "matrix column count changed")

        dual, live_action_pairs, degree_live = orbit_average_dual(rows)
        target_pairing = sum(
            Q(numerator, denominator) * dual.get(row_index, 0)
            for row_index, numerator, denominator in header["target"]
        )
        require(target_pairing == Q(512000, 729),
                ("target/dual pairing changed", target_pairing))

        nonzero_column_pairings = []
        column_count = 0
        raw_incidence_count = 0
        for line in stream:
            digest.update(line)
            column = json.loads(line)
            require(column["type"] == "column", "non-column record found")
            require(column["index"] == column_count,
                    "column ordering/index changed")
            pairing = Q(0)
            for row_index, coefficient in column["entries"]:
                raw_incidence_count += 1
                pairing += coefficient * dual.get(row_index, 0)
            if pairing:
                nonzero_column_pairings.append(
                    [column_count, pairing.numerator, pairing.denominator]
                )
            column_count += 1

    require(column_count == header["column_count"],
            "truncated/expanded matrix column stream")
    require(not nonzero_column_pairings,
            ("evaluation dual does not annihilate matrix",
             nonzero_column_pairings[:5]))

    # Must-fire controls: the raw evaluation (without averaging) is not
    # constant on row orbits, and changing the target constant term fires.
    cell = BASE.CELL_ID[(0, 2, 0, 0)]
    row = bytes((cell,))
    raw_values = scaled_assignment()
    raw_orbit_values = {
        raw_values.get(transform[cell], 0)
        for transform in EXPORT.TRANSFORMS
    }
    require(len(raw_orbit_values) > 1,
            "raw evaluation unexpectedly orbit invariant")
    hostile_target_pairing = target_pairing + dual[0]
    require(hostile_target_pairing != target_pairing,
            "hostile target mutation did not fire")

    result = {
        "status": "UNAUDITED exact-Q orbit-averaged evaluation dual",
        "matrix_path": str(MATRIX.relative_to(ROOT)),
        "matrix_sha256": digest.hexdigest(),
        "matrix_format": header["format"],
        "row_count": len(rows),
        "target_row_orbits": len(header["target"]),
        "column_count": column_count,
        "raw_column_incidences": raw_incidence_count,
        "stabilizer_order": len(EXPORT.TRANSFORMS),
        "dual_nonzero_row_orbits": len(dual),
        "dual_live_action_row_pairs_before_cancellation": live_action_pairs,
        "dual_nonzero_degree_histogram": {
            str(degree): sum(1 for row_index in dual
                             if len(rows[row_index]) == degree)
            for degree in sorted({len(rows[index]) for index in dual})
        },
        "rows_with_any_live_action_degree_histogram": {
            str(degree): count for degree, count in sorted(degree_live.items())
        },
        "nonzero_column_pairings": len(nonzero_column_pairings),
        "target_pairing": [target_pairing.numerator,
                           target_pairing.denominator],
        "hostile_target_pairing": [hostile_target_pairing.numerator,
                                   hostile_target_pairing.denominator],
        "raw_evaluation_orbit_values_scaled": sorted(raw_orbit_values),
        "conclusion": (
            "The exact stabilizer-averaged evaluation functional annihilates "
            "all 5,400 serialized pair-constant first-layer columns and "
            "pairs nontrivially with the 868-orbit target. Thus the target "
            "is outside this Macaulay span over Q, independently of the two "
            "reported modular eliminations."
        ),
        "scope": (
            "This is a dual only for the pair-constant 5,400-column layer. "
            "It does not annihilate columns from the other 6,480 mixed words."
        ),
    }
    encoded = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("pair-constant first-layer exact evaluation dual: PASS")
    print("matrix sha256:", result["matrix_sha256"])
    print("nonzero dual rows / live pairs:", len(dual), live_action_pairs)
    print("columns / incidences / nonzero pairings:",
          column_count, raw_incidence_count, len(nonzero_column_pairings))
    print("target pairing:", target_pairing)
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
