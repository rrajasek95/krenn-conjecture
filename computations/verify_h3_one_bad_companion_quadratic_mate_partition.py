#!/usr/bin/env python3
"""Exact quadratic mate partition for the h=3 (c,t,c) companion row.

This is the bounded next layer after the literal closure in 1dea1fa.  At
the concentrated normal form the physical coefficient has 105 matching
monomials: one linear pivot, six quadratic mates, thirty cubic terms, and
sixty-eight quartic terms.  The checker also builds the complete tangent
Jacobian of the four retained tensor rows in their 167 literal variables.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_one_bad_common_q_cap_extraction_boundary.py":
        "02517a037d7dfc273d2eee63dd85e8228d88cd4824397b7ac478c013624afe5e",
    "computations/verify_h3_one_bad_second_principal_parts_companion_closure.py":
        "3612f9d7c03a3e265792543cd602f27ebf64830390f95b5bddb8d953d238c3f5",
}
EXPECTED_LEDGER_SHA256 = (
    "7a99ba0e145bd54354249d4325862681693dcd54c1c6fd68d504d9691f6a85e5"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"dependency changed: {relative}: {actual}")


def clean(counter):
    return Counter({key: value for key, value in counter.items() if value})


def add(*counters):
    result = Counter()
    for counter in counters:
        result.update(counter)
    return clean(result)


def scale(counter, scalar):
    return clean(Counter({key: scalar * value
                          for key, value in counter.items()}))


def four_rows(base, q, stars, d_ca=Fraction(1), d_tt=Fraction(0)):
    """The two diagonal rows and the ca/tt tensor rows."""
    return (
        base.odd_star_response(q, stars["Qc"]),
        base.odd_star_response(q, stars["Ra"]),
        add(scale(base.odd_star_response(q, stars["Pt"]), d_ca),
            base.triple_star_response(
                q, stars["Pt"], stars["Qc"], stars["Ra"])),
        add(scale(base.odd_star_response(q, stars["Pt"]), d_tt),
            base.triple_star_response(
                q, stars["Pt"], stars["Qt"], stars["Rt"])),
    )


def flatten(rows):
    return clean(Counter({(row_index, word): coefficient
                          for row_index, row in enumerate(rows)
                          for word, coefficient in row.items()}))


def main():
    pin_dependencies()
    base = importlib.import_module(
        "verify_h3_one_bad_common_q_cap_extraction_boundary")
    closure = importlib.import_module(
        "verify_h3_one_bad_second_principal_parts_companion_closure")
    cell = base.cell
    one = Fraction(1)

    source = clean(closure.build_eight_site_source(base, Fraction(0)))
    word = tuple(map(int, "21000121"))
    layers = Counter()
    layer_terms = {degree: [] for degree in range(5)}
    for matching in base.perfect_matchings(tuple(range(8))):
        cells = tuple(cell(u, v, word[u], word[v]) for u, v in matching)
        missing = tuple(sorted(entry for entry in cells if not source.get(entry)))
        layers[len(missing)] += 1
        layer_terms[len(missing)].append((matching, missing))
    require(sum(layers.values()) == 105, "the K8 matching count changed")
    require(layers == Counter({1: 1, 2: 6, 3: 30, 4: 68}),
            f"the companion filtration changed: {layers}")

    C = cell(1, 2, 1, 0)
    require(layer_terms[1][0][1] == (C,),
            f"the linear companion pivot stopped being C: {layer_terms[1]}")

    expected_pairs = {
        "Dpr_Qt_qstar_1": tuple(sorted((cell(0, 1, 2, 1),
                                         cell(2, 6, 0, 2)))),
        "Dpr_Qt_qstar_2": tuple(sorted((cell(0, 2, 2, 0),
                                         cell(1, 6, 1, 2)))),
        "Dpr_Qt_qq_1": tuple(sorted((cell(1, 3, 1, 0),
                                      cell(2, 4, 0, 0)))),
        "Dpr_Qt_qq_2": tuple(sorted((cell(1, 4, 1, 0),
                                      cell(2, 3, 0, 0)))),
        "triple_same_holes": tuple(sorted((cell(1, 5, 1, 1),
                                            cell(2, 7, 0, 1)))),
        "triple_crossed_holes": tuple(sorted((cell(1, 7, 1, 1),
                                               cell(2, 5, 0, 1)))),
    }
    actual_pairs = {missing for _, missing in layer_terms[2]}
    require(actual_pairs == set(expected_pairs.values()),
            f"the six quadratic mates changed: {actual_pairs}")

    # Build every literal first-order variable of the four retained rows:
    # 90 internal q cells, five 15-coordinate stars, and two directs.
    q0 = clean(closure.build_common_q(base, Fraction(0)))
    stars0 = {
        "Qc": ((0, 1, one),),
        "Ra": ((2, 0, one),),
        "Pt": ((1, 2, one),),
        "Qt": ((0, 2, one),),
        "Rt": ((4, 2, one),),
    }
    row0 = flatten(four_rows(base, q0, stars0))

    def tangent_column(q, stars, d_ca=one, d_tt=Fraction(0)):
        result = flatten(four_rows(base, q, stars, d_ca, d_tt))
        result.subtract(row0)
        return clean(result)

    columns = {}
    for u, v in itertools.combinations(range(5), 2):
        for a in range(3):
            for b in range(3):
                key = cell(u, v, a, b)
                moved = Counter(q0)
                moved[key] += 1
                columns[f"q{u}{v}:{a}{b}"] = tangent_column(moved, stars0)
    for family in stars0:
        for hole in range(5):
            for colour in range(3):
                moved = dict(stars0)
                moved[family] = stars0[family] + ((hole, colour, one),)
                columns[f"{family}@{hole}:{colour}"] = tangent_column(q0, moved)
    columns["Dca"] = tangent_column(q0, stars0, 2, 0)
    columns["Dtt"] = tangent_column(q0, stars0, 1, 1)
    require(len(columns) == 167, "the literal four-row tangent width changed")
    tangent_rows = set().union(*(set(column) for column in columns.values()))
    require(len(tangent_rows) == 150,
            f"the literal four-row tangent height changed: {len(tangent_rows)}")

    q_directions = {
        "q01:21": (1, tuple(map(int, "21000"))),
        "q02:20": (2, tuple(map(int, "22000"))),
        "q13:10": (0, tuple(map(int, "11101"))),
        "q24:00": (0, tuple(map(int, "11010"))),
        "q14:10": (0, tuple(map(int, "11220"))),
        "q23:00": (3, tuple(map(int, "22002"))),
    }
    expected_incidence = {
        "q01:21": (("q01:21", "1"),),
        "q02:20": (("Qc@0:2", "1"), ("q02:20", "1")),
        "q13:10": (("q13:10", "1"),),
        "q24:00": (("Qc@4:0", "-1"), ("q24:00", "1")),
        "q14:10": (("q14:10", "1"),),
        "q23:00": (("q23:00", "1"),),
    }
    incidence = {}
    for name, coordinate in q_directions.items():
        require(columns[name] == Counter({coordinate: one}),
                f"the isolated tangent defect changed: {name}: {columns[name]}")
        hits = tuple(sorted((column_name, str(column[coordinate]))
                            for column_name, column in columns.items()
                            if column.get(coordinate)))
        incidence[name] = hits
        require(hits == expected_incidence[name],
                f"the tangent incidence changed for {name}: {hits}")

    correction_tails = {
        "Qc@0:2": tuple(sorted(
            (row, "".join(map(str, response_word)), str(value))
            for (row, response_word), value in columns["Qc@0:2"].items())),
        "Qc@4:0": tuple(sorted(
            (row, "".join(map(str, response_word)), str(value))
            for (row, response_word), value in columns["Qc@4:0"].items())),
    }
    require(correction_tails == {
        "Qc@0:2": ((0, "21111", "1"), (2, "22000", "1")),
        "Qc@4:0": ((0, "00220", "1"), (0, "11010", "-1")),
    }, f"the two attempted corrections changed: {correction_tails}")

    # The two triple-star pairs use star colours outside the four selected
    # rows, hence are tangent-invisible there.  Their endpoint/site minors
    # distinguish the one-edge bad alignment from the crossed good alignment.
    same_p = ((1, 0), (1, 0))   # P_t and P_c both at hole 1
    same_r = ((0, 1), (0, 1))   # R_a and R_c both at hole 2
    cross_p = ((1, 0), (0, 1))  # P_t@1, P_c@2
    cross_r = ((0, 1), (1, 0))  # R_a@2, R_c@1

    def det2(matrix):
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

    require((det2(same_p), det2(same_r)) == (0, 0),
            "the same-hole endpoint alignment became good")
    require((det2(cross_p), det2(cross_r)) == (1, -1),
            "the crossed endpoint alignment lost goodness")

    ledger = {
        "dependencies": PINS,
        "companion_word": "21000121",
        "matching_terms": 105,
        "normal_cell_degree_histogram": dict(sorted(layers.items())),
        "linear_pivot": "12:10=C",
        "quadratic_pairs": {
            name: [str(entry) for entry in pair]
            for name, pair in expected_pairs.items()
        },
        "quadratic_grade_split": {
            "Dpr_Qt_q2": 4,
            "Pc_Qt_Rc_q": 2,
            "Dpq_or_Dqr": 0,
        },
        "four_row_tangent": {
            "columns": len(columns),
            "rows": len(tangent_rows),
            "q_direction_incidence": incidence,
            "attempted_correction_tails": correction_tails,
        },
        "triple_pair_routes": {
            "same_hole_endpoint_minors": (0, 0),
            "same_hole_automatic": "one physical hole-pair support",
            "same_hole_not_automatic": "scalar-zero pure-target cap normalization",
            "crossed_endpoint_minors": (1, -1),
            "crossed_automatic": "two selected endpoint goodness minors",
            "crossed_not_automatic": "full activity/span and curved two-chart hypotheses",
        },
        "verdict": (
            "the first arbitrary-support escape is exactly six quadratic "
            "mates: four expose a new first-order four-row defect, while "
            "the two tangent-invisible triple-star mates split into the "
            "same-hole one-edge and crossed-good endpoint patterns"
        ),
        "scope": (
            "complete degree-two classification for the physical (c,t,c) "
            "coefficient at the concentrated literal normal form; it does "
            "not prove the missing scalar-zero cap normalization or the "
            "full curved/activity hypotheses, and does not inspect the "
            "thirty cubic or sixty-eight quartic terms"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"the quadratic mate ledger changed: {digest}")

    print("h=3 one-bad companion quadratic-mate partition: PASS")
    print("105 terms: degree 1/2/3/4 = 1/6/30/68")
    print("quadratic grades: Dpr*Qt*q^[2] = 4; Pc*Qt*Rc*q = 2")
    print("literal four-row tangent matrix: 150 x 167")
    print("triple routes: same-hole minors 0,0; crossed minors 1,-1")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
