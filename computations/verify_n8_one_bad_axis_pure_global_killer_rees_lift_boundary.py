#!/usr/bin/env python3
"""Exact target-compatible Rees obstruction after the global killer order.

The common source order is a valid local initial order, but it is not a
target-compatible torus grading: its selected and contaminating terms lie in
the same target character.  More sharply, any chart-compatible landing which
keeps the 54 eliminated carriers nonnegative, makes the 36 survivors positive,
and keeps endpoint/direct corrections nonnegative is infeasible.  A primitive
three-inequality Farkas certificate uses one opposing-pair identity and one
literal killer-row identity and forces the endpoint coefficient p5 negative.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_n8_one_bad_axis_pure_global_killer_weight_order.py":
        "c75d501cdf545080540d8287b04452d7ca57acc87c980f21ec5b7376e74ca287",
    "computations/verify_n8_one_bad_axis_pure_chart_torus_accessibility.py":
        "327dbf6ac8f2d617f78433f25859d8760bec1253d557158425ec8649babd28e9",
}
EXPECTED_LEDGER_SHA256 = "fbbc7345f60da240d6dd46395c25c161ef62f47796b39f65d877bdb4d53571f2"

LEFT_SELECTED = (0, 3, 0, 1)
PAIR_SELECTED = (3, 5, 0, 1)
SURVIVOR = (0, 3, 1, 0)
ANCHOR_03 = (0, 3, 0, 0)
ANCHOR_35 = (3, 5, 1, 1)
P0 = (0, 6, 1, 1)
P5 = (5, 6, 1, 1)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"dependency changed: {relative}: {actual}")


def main():
    pin_dependencies()
    global_order = importlib.import_module(
        "verify_n8_one_bad_axis_pure_global_killer_weight_order")
    torus = importlib.import_module(
        "verify_n8_one_bad_axis_pure_chart_torus_accessibility")
    all_pairs = importlib.import_module(
        "verify_n8_one_bad_axis_pure_all_opposing_pair_elimination")
    triples_checker = importlib.import_module(
        "verify_n8_one_bad_axis_pure_all_hilbert_triple_elimination")
    hilbert = importlib.import_module(
        "verify_n8_one_bad_axis_pure_mixed_weight_hilbert_circuits")
    completion = importlib.import_module(
        "verify_n8_one_bad_endpoint_minor_unary_top_completion")
    module = importlib.import_module(
        "verify_n8_one_bad_multisite_permanent_null_defect")

    basis, _pivots = torus.nullspace(torus.equation_matrix())
    cells = global_order.mixed_cells()
    pairs = all_pairs.opposing_pairs(torus, basis)
    triples = global_order.primitive_triples(hilbert, torus, basis, cells)
    records = global_order.sparse_eliminations(
        all_pairs, triples_checker, completion, module, pairs, triples
    )
    selected = frozenset(record[3] for record in records)
    survivors = tuple(cell for cell in cells if cell not in selected)
    require(len(selected) == 54 and len(survivors) == 36,
            "the global initial carrier partition changed")
    require(LEFT_SELECTED in selected and PAIR_SELECTED in selected
            and SURVIVOR in survivors,
            "the primitive Farkas cells changed class")

    # Literal full-character identities, before quotienting by the chart.
    left = torus.cell_character(LEFT_SELECTED)
    pair = torus.cell_character(PAIR_SELECTED)
    survivor = torus.cell_character(SURVIVOR)
    anchor_03 = torus.cell_character(ANCHOR_03)
    anchor_35 = torus.cell_character(ANCHOR_35)
    p0 = torus.cell_character(P0)
    p5 = torus.cell_character(P5)
    require(torus.add_rows(left, pair)
            == torus.add_rows(anchor_03, anchor_35),
            "the opposing-pair character identity changed")
    require(torus.add_rows(pair, p0) == torus.add_rows(survivor, p5),
            "the killer-row character identity changed")

    # The second identity is carried by one actual original response row.
    _top, _responses, equations = all_pairs.source_equations(
        completion, module, global_order.full_q(module, cells)
    )
    rows = {(sector, "".join(map(str, word))): polynomial
            for sector, word, polynomial in equations}
    source_row = rows[("11", "111011")]
    selected_term = tuple(sorted(("A", "m3501", "p0", "s1")))
    contaminant_term = tuple(sorted(("A", "m0310", "p5", "s1")))
    require(source_row[selected_term] == source_row[contaminant_term] == 1,
            "the two character-equal terms left the literal killer row")

    # Full augmented landing system.  The 72 endpoint directions are the
    # four endpoint rows (p1,p2 at endpoint 6; s1,s2 at endpoint 7), each
    # with 6*3 decorated cells.  The four direct cells lie on edge 67.
    endpoint_cells = frozenset(
        [(site, 6, colour, endpoint_colour)
         for endpoint_colour in (1, 2)
         for site in range(6) for colour in range(3)]
        + [(site, 7, colour, endpoint_colour)
           for endpoint_colour in (1, 2)
           for site in range(6) for colour in range(3)]
    )
    direct_cells = frozenset(
        (6, 7, left_colour, right_colour)
        for left_colour in (1, 2) for right_colour in (1, 2)
    )
    require(len(endpoint_cells) == 72 and len(direct_cells) == 4
            and P5 in endpoint_cells,
            "the endpoint/direct landing universe changed")

    # In the chart kernel every retained anchor has weight zero.  Write
    # a=wt(03:01), b=wt(35:01), r=wt(03:10), e=wt(p5).  The two exact
    # identities give a+b=0 and b=r+e, hence a+r+e=0.  But the augmented
    # landing inequalities contain a>=0, r>=1, e>=0, whose primitive sum
    # has right side 1.  This is a rational/integral Farkas contradiction.
    quotient = {
        "a": torus.quotient_character(LEFT_SELECTED, basis),
        "b": torus.quotient_character(PAIR_SELECTED, basis),
        "r": torus.quotient_character(SURVIVOR, basis),
        "e": torus.quotient_character(P5, basis),
    }
    require(torus.add_rows(quotient["a"], quotient["b"])
            == (Fraction(0),) * len(basis),
            "the pair identity did not descend to the quotient")
    require(quotient["b"]
            == torus.add_rows(quotient["r"], quotient["e"]),
            "the row identity did not descend to the quotient")
    farkas_normal = torus.add_rows(
        quotient["a"], quotient["r"], quotient["e"]
    )
    require(farkas_normal == (Fraction(0),) * len(basis),
            "the primitive Farkas normals stopped summing to zero")

    # The exact separating cocharacter from 1aec4da saturates the boundary:
    # selected cells have weight zero, survivors have weight 1 or 2, and p5
    # is forced to weight -1 by the displayed certificate.
    witness = global_order.REMAINING_COCHARACTER
    pairing = lambda cell: sum(
        left_value * right_value for left_value, right_value in zip(
            torus.quotient_character(cell, basis), witness, strict=True
        )
    )
    require(Counter(pairing(cell) for cell in selected)
            == Counter({Fraction(0): 54}),
            "the associated-graded selected boundary changed")
    require(Counter(pairing(cell) for cell in survivors)
            == Counter({Fraction(1): 32, Fraction(2): 4}),
            "the surviving-ray separator changed")
    require(pairing(P5) == -1,
            "the separator no longer exposes the negative p5 endpoint")

    ledger = {
        "dependencies": PINS,
        "augmented_landing_system": {
            "chart_equations": len(torus.equation_matrix()),
            "selected_carrier_nonnegative": len(selected),
            "surviving_carrier_strict_positive": len(survivors),
            "endpoint_nonnegative": len(endpoint_cells),
            "direct_nonnegative": len(direct_cells),
            "verdict": "infeasible",
        },
        "primitive_farkas_certificate": {
            "character_identities": [
                "chi(03:01)+chi(35:01)=chi(03:00)+chi(35:11)=0",
                "chi(35:01)+chi(p0)=chi(03:10)+chi(p5)",
            ],
            "zero_normal_sum": "chi(03:01)+chi(03:10)+chi(p5)=0",
            "inequalities": ["wt(03:01)>=0", "wt(03:10)>=1", "wt(p5)>=0"],
            "farkas_multipliers": [1, 1, 1],
            "summed_lower_bound": 1,
            "support_size": 3,
        },
        "literal_row": {
            "label": "11@111011",
            "selected": "A*p0*s1*m3501",
            "contaminant": "A*p5*s1*m0310",
            "target_character_equal": True,
        },
        "boundary_witness": {
            "selected_pairings": {"0": 54},
            "survivor_pairings": {"1": 32, "2": 4},
            "p5_pairing": -1,
        },
        "verdict": (
            "the common source initial order cannot be promoted to a "
            "target-compatible nonnegative Rees landing; positivity of the "
            "surviving carrier forces the endpoint coefficient p5 negative"
        ),
        "missing_step": (
            "an equivariant Rees/Weierstrass lift must first prove p5=0 or "
            "replace the 54-variable graph by source-valid coordinates in "
            "which every endpoint/direct parameter is nonnegative; only "
            "then can the pure-chart unit be lifted by Nakayama"
        ),
        "scope": (
            "the fixed 54/36 carrier partition and existing literal row; no "
            "new carrier rows, higher circuits, or support search"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"the Rees lift-boundary ledger changed: {digest}")

    print("N=8 global killer Rees lift boundary: PASS")
    print("augmented landing system: infeasible")
    print("primitive Farkas support: 3 inequalities")
    print("forced endpoint weight: p5=-1 on the separator")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
