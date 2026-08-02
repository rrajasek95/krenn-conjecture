#!/usr/bin/env python3
"""Exact seven-orbit boundary dual on localized target chart 25."""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import permutations
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CHARTS = load("n8_charts", "verify_n8_target_triple_localization_orbits.py")
FULL = load("n8_full_source", "verify_n8_full_source_cycle_product_membership.py")
EXPECTED_LEDGER_SHA256 = (
    "707fd2b91a76ed39123bfb4e70f2686d08fc783e221ce9a625d5147ab4e7df66"
)

EXACT_DUAL = (
    (-2, ((0, 1, 0, 0), (0, 2, 1, 1), (0, 2, 2, 2),
          (1, 3, 1, 1), (1, 3, 2, 2), (2, 4, 0, 0),
          (3, 5, 0, 0), (4, 6, 1, 1), (4, 7, 2, 2),
          (5, 6, 2, 2), (5, 7, 1, 1), (6, 7, 0, 0))),
    (4, ((0, 1, 0, 0), (0, 2, 1, 1), (0, 3, 2, 1),
         (1, 2, 1, 2), (1, 3, 2, 2), (2, 4, 0, 0),
         (3, 5, 0, 0), (4, 6, 1, 1), (4, 7, 2, 2),
         (5, 6, 2, 2), (5, 7, 1, 1), (6, 7, 0, 0))),
    (1, ((0, 1, 0, 0), (0, 2, 1, 1), (0, 3, 2, 2),
         (1, 2, 2, 2), (1, 3, 1, 1), (2, 4, 0, 0),
         (3, 5, 0, 0), (4, 6, 1, 1), (4, 7, 2, 2),
         (5, 6, 2, 2), (5, 7, 1, 1), (6, 7, 0, 0))),
    (-2, ((0, 1, 0, 0), (0, 2, 1, 1), (0, 3, 2, 2),
          (1, 2, 2, 2), (1, 3, 1, 1), (2, 4, 0, 0),
          (3, 5, 0, 0), (4, 6, 1, 2), (4, 6, 2, 1),
          (5, 7, 1, 2), (5, 7, 2, 1), (6, 7, 0, 0))),
    (1, ((0, 1, 0, 0), (0, 2, 1, 1), (0, 3, 2, 2),
         (1, 2, 2, 2), (1, 3, 1, 1), (2, 4, 0, 0),
         (3, 5, 0, 0), (4, 6, 1, 2), (4, 7, 2, 1),
         (5, 6, 2, 1), (5, 7, 1, 2), (6, 7, 0, 0))),
    (1, ((0, 1, 0, 0), (0, 2, 1, 1), (0, 3, 2, 2),
         (1, 2, 2, 2), (1, 3, 1, 1), (2, 4, 0, 0),
         (3, 5, 0, 0), (4, 6, 2, 1), (4, 7, 1, 2),
         (5, 6, 1, 2), (5, 7, 2, 1), (6, 7, 0, 0))),
    (1, ((0, 1, 0, 0), (0, 2, 1, 1), (0, 3, 2, 2),
         (1, 2, 2, 2), (1, 3, 1, 1), (2, 4, 0, 0),
         (3, 5, 0, 0), (4, 6, 2, 2), (4, 7, 1, 1),
         (5, 6, 1, 1), (5, 7, 2, 2), (6, 7, 0, 0))),
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def configure_chart25():
    row = tuple(sorted(CHARTS.SOURCE.target_orbit_rows()))[24]
    mate = CHARTS.SOURCE.decode_key(row)
    support = []
    for first, second in CHARTS.SOURCE.mate_edges(mate):
        left, left_colour = divmod(first, 3)
        right, right_colour = divmod(second, 3)
        support.append(FULL.edge(left, right, left_colour, right_colour))
    FULL.SUPPORT_PRODUCT = tuple(sorted(support))
    FULL.SUPPORT_SET = frozenset(support)
    stabilizer = []
    for vertex_permutation in permutations(range(8)):
        for colour_permutation in permutations(range(3)):
            element = vertex_permutation, colour_permutation
            if frozenset(FULL.transform_variable(variable, element)
                         for variable in support) == FULL.SUPPORT_SET:
                stabilizer.append(element)
    require(len(stabilizer) == 8, "chart 25 stabilizer changed")
    FULL.SUPPORT_STABILIZER = tuple(stabilizer)


def audit():
    configure_chart25()
    rows, columns, layers = FULL.truncated_orbit_component(4)
    require(len(rows) == 2870 and len(columns) == 9516,
            "chart 25 truncated component census changed")
    require(layers == ((44, 1), (358, 142), (1088, 1282),
                       (1080, 3539), (277, 3585), (22, 894), (0, 73)),
            "chart 25 truncated component layers changed")
    row_index = {row: index for index, row in enumerate(rows)}
    invariant = {}
    for value, row in EXACT_DUAL:
        require(row in row_index, "dual row left the truncated component")
        require(row == FULL.canonical_row(row), "dual row is not canonical")
        invariant[row_index[row]] = value
    require(len(invariant) == 7 and Counter(invariant.values())
            == {-2: 2, 1: 4, 4: 1}, "dual orbit census changed")
    require(invariant[row_index[FULL.SUPPORT_PRODUCT]] == 1,
            "dual has wrong target value")
    for column in columns:
        entries = FULL.invariant_column_entries(column, row_index, 4)
        require(sum(invariant.get(index, 0) * value
                    for index, value in entries.items()) == 0,
                "exact invariant dual replay failed")

    certificate = [
        {"sign": value, "row": [list(variable) for variable in row]}
        for value, row in EXACT_DUAL
    ]
    expanded = FULL.expanded_rational_functional(certificate)
    require(len(expanded) == 23, "expanded dual support changed")
    require(expanded[FULL.SUPPORT_PRODUCT] == 1,
            "expanded dual has wrong target value")
    require(Counter(expanded.values())
            == {Fraction(1, 2): 14, Fraction(-1, 2): 8, Fraction(1): 1},
            "expanded dual value histogram changed")
    for column in columns:
        require(sum(expanded.get(row, 0) for row in FULL.column_rows(column)) == 0,
                "expanded exact dual replay failed")
    union = frozenset(variable for row in expanded for variable in row)
    require(len(union) == 36 and FULL.SUPPORT_SET <= union,
            "chart 25 dual coordinate support changed")
    ledger = {
        "chart": 25,
        "support_stabilizer": len(FULL.SUPPORT_STABILIZER),
        "maximum_off_support_degree": 4,
        "layers": layers,
        "row_orbits": len(rows),
        "column_orbits": len(columns),
        "dual_orbit_rows": len(invariant),
        "dual_orbit_values": dict(sorted(Counter(invariant.values()).items())),
        "expanded_rows": len(expanded),
        "expanded_values": {
            str(value): count for value, count in
            sorted(Counter(expanded.values()).items())
        },
        "coordinate_union": len(union),
        "normalized_chart_variables": len(union - FULL.SUPPORT_SET),
        "target_value": [1, 1],
    }
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode("ascii")).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "chart 25 boundary-dual ledger changed")
    return ledger, digest


def main():
    ledger, digest = audit()
    print("chart 25 exact boundary dual: PASS")
    print("component:", ledger["row_orbits"], "x", ledger["column_orbits"])
    print("dual orbit rows:", ledger["dual_orbit_rows"])
    print("expanded rows:", ledger["expanded_rows"])
    print("coordinate union:", ledger["coordinate_union"])
    print("normalized chart variables:", ledger["normalized_chart_variables"])
    print("sha256:", digest)


if __name__ == "__main__":
    main()
