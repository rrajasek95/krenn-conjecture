#!/usr/bin/env python3
"""Finite reselection audit for the same-hole internal-q carrier repairs.

The carrier cover e326827 leaves a shared C/A repair and two middle A/T
repair matchings.  This checker inserts each repair into the literal fixed
star/direct packet, expands all four complete common-q tensor rows, and
enumerates every rank-one physical shared-pair reselection touching a repair
edge.  The shared repair and the right middle repair already expose an
active (3,3,3,3) pair.  The left middle repair first forces one further
two-cell matching, after which the same conclusion holds.

The audit is deliberately the finite carrier-only chart.  Arbitrary extra
endpoint-star components and arbitrary extra residue support are excluded.
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
    "computations/verify_h3_one_bad_same_hole_unit_loss_carrier_cover.py":
        "12c7bafd7b2f75a29cf69877d0fd04496e5c251b1a4f485925582d597447e080",
    "computations/verify_h3_one_bad_crossed_quadratic_oo_landing_guard.py":
        "9c629cd7ee51241f6170619c354b1417b636cd53b1faba35629cb57a2ae83281",
    "computations/verify_shared_reciprocal_flat_bicase_unit.py":
        "ea7ca9b3de2bc2e7d71d45cfba35fb62d77309819d9b6a910307b91061dd7a18",
}
EXPECTED_LEDGER_SHA256 = (
    "6aae430e1c40ac7a881e230af82e5c5e2111add45dcc492d8efa3357ab853b90"
)

A, C, T = range(3)
P, Q, R = 5, 6, 7
COLORS = tuple(range(3))
VERTICES = tuple(range(8))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"dependency changed: {relative}: {actual}")


def clean(counter):
    return Counter({key: value for key, value in counter.items() if value})


def fixed_stars():
    one = Fraction(1)
    return {
        "Qc": ((0, C, one),),
        "Ra": ((2, A, one),),
        "Pt": ((1, T, one),),
        "Qt": ((0, T, one),),
        "Rt": ((4, T, one),),
    }


def outer_source(cell):
    """The fixed same-hole endpoint-star/direct normal form."""
    return Counter({
        cell(P, Q, A, A): 1,
        cell(P, R, C, C): 1,
        cell(Q, R, C, A): 1,
        cell(1, P, T, T): 1,
        cell(0, Q, C, C): 1,
        cell(0, Q, T, T): 1,
        cell(2, R, A, A): 1,
        cell(4, R, T, T): 1,
        cell(1, P, C, C): 3,
        cell(2, R, A, C): -2,
    })


def common_packets(cell):
    shared = Counter({
        cell(1, 2, C, C): 1,
        cell(3, 4, C, C): 1,
        cell(0, 1, A, A): 1,
        cell(3, 4, A, A): 1,
        cell(2, 3, T, T): 1,
        cell(1, 3, C, A): 1,
        cell(2, 4, C, A): -1,
    })
    middle_left = Counter({
        cell(1, 2, C, C): 1,
        cell(3, 4, C, C): 1,
        cell(0, 3, A, A): 1,
        cell(1, 4, A, A): 1,
        cell(2, 3, T, T): 1,
        cell(1, 2, A, T): 1,
        cell(3, 4, T, A): -1,
    })
    middle_right = Counter({
        cell(1, 2, C, C): 1,
        cell(3, 4, C, C): 1,
        cell(0, 3, A, A): 1,
        cell(1, 4, A, A): 1,
        cell(2, 3, T, T): 1,
        cell(1, 3, A, T): 1,
        cell(2, 4, T, A): -1,
    })
    middle_left_secondary = Counter(middle_left)
    middle_left_secondary.update({
        cell(1, 3, A, C): 1,
        cell(2, 4, T, C): -1,
    })
    return {
        "shared_CA": shared,
        "middle_AT_left": middle_left,
        "middle_AT_right": middle_right,
        "middle_AT_left_secondary": middle_left_secondary,
    }


def row_residuals(base, mate, q):
    rows = mate.four_rows(base, q, fixed_stars())
    targets = (
        Counter({(C,) * 5: 1}),
        Counter({(A,) * 5: 1}),
        Counter(),
        Counter({(T,) * 5: 1}),
    )
    answer = []
    for row, target in zip(rows, targets, strict=True):
        residual = Counter(row)
        residual.subtract(target)
        answer.append(clean(residual))
    return tuple(answer)


def activity_terms(base, source, arm):
    residual = tuple(vertex for vertex in VERTICES if vertex not in arm)
    return len(base.hafnian_tensor(source, residual))


def repair_touching_census(base, oo, source, repair_edges):
    answer = []
    for head in VERTICES:
        neighbours = [
            vertex for vertex in VERTICES if vertex != head
            and oo.rational_rank(oo.direct_matrix(source, head, vertex)) == 1
        ]
        for first, second in itertools.combinations(neighbours, 2):
            arms = {tuple(sorted((head, first))),
                    tuple(sorted((head, second)))}
            if not arms.intersection(repair_edges):
                continue
            ranks = tuple(
                oo.star_rank(source, endpoint, deleted)
                for endpoint, deleted in (
                    (head, first), (first, head),
                    (head, second), (second, head),
                )
            )
            activity = (
                activity_terms(base, source, (head, first)),
                activity_terms(base, source, (head, second)),
            )
            answer.append((head, first, second, ranks, activity))
    return tuple(answer)


def direct_entries(oo, source, arm):
    head, outer = arm
    return tuple(
        (head_colour, outer_colour, str(oo.entry(
            source, head, outer, head_colour, outer_colour)))
        for head_colour in COLORS for outer_colour in COLORS
        if oo.entry(source, head, outer, head_colour, outer_colour)
    )


def serial_rows(rows):
    return tuple({"".join(map(str, word)): str(value)
                  for word, value in sorted(row.items())}
                 for row in rows)


def serial_census(census):
    return tuple({
        "pair": (head, first, second),
        "star_ranks": ranks,
        "cofactor_terms": activity,
    } for head, first, second, ranks, activity in census)


def main():
    pin_dependencies()
    base = importlib.import_module(
        "verify_h3_one_bad_common_q_cap_extraction_boundary")
    mate = importlib.import_module(
        "verify_h3_one_bad_companion_quadratic_mate_partition")
    oo = importlib.import_module(
        "verify_oo_doubly_good_two_anchor_counterguard")
    carrier = importlib.import_module(
        "verify_h3_one_bad_same_hole_unit_loss_carrier_cover")
    cell = base.cell

    packets = common_packets(cell)
    rows = {name: row_residuals(base, mate, q)
            for name, q in packets.items()}
    expected_rows = {
        "shared_CA": (
            {},
            {"00011": "1"},
            {"12000": "1", "12011": "1"},
            {},
        ),
        "middle_AT_left": (
            {"10211": "1", "11120": "-1"},
            {},
            {"12011": "1", "12020": "-1"},
            {},
        ),
        "middle_AT_right": (
            {},
            {},
            {"02200": "-1", "12011": "1"},
            {},
        ),
        "middle_AT_left_secondary": (
            {"11120": "-1"},
            {},
            {"02201": "-1", "12011": "1", "12020": "-1"},
            {},
        ),
    }
    require({name: serial_rows(value) for name, value in rows.items()}
            == expected_rows, "the complete four-row residual ledger changed")

    # The first cross word created by the left A/T repair has only two
    # matchings after the tt block.  Since its first product is a unit, the
    # secondary q13:01*q24:21 product is forced to be a unit as well.
    left_cross_word = (C, A, T, C, C)
    left_cross = carrier.reduce_tt(
        carrier.odd_fixed_star(base, 0, C, left_cross_word))
    left_unit = carrier.monomial(
        carrier.q_name(1, 2, A, T), carrier.q_name(3, 4, C, C))
    secondary = carrier.monomial(
        carrier.q_name(1, 3, A, C), carrier.q_name(2, 4, T, C))
    require(left_cross == Counter({left_unit: 1, secondary: 1}),
            f"the left-repair secondary equation changed: {left_cross}")

    outer = outer_source(cell)
    sources = {}
    for name, q in packets.items():
        source = Counter(q)
        source.update(outer)
        sources[name] = source

    repair_edges = {
        "shared_CA": {(1, 3), (2, 4)},
        "middle_AT_left": {(1, 2), (3, 4)},
        "middle_AT_right": {(1, 3), (2, 4)},
        "middle_AT_left_secondary": {(1, 2), (3, 4), (1, 3), (2, 4)},
    }
    censuses = {
        name: repair_touching_census(base, oo, sources[name], edges)
        for name, edges in repair_edges.items()
    }
    require(tuple(map(len, (censuses["shared_CA"],
                            censuses["middle_AT_left"],
                            censuses["middle_AT_right"],
                            censuses["middle_AT_left_secondary"])))
            == (7, 0, 11, 7),
            "the repair-touching reselection counts changed")

    selected = {
        "shared_CA": (1, 2, 3),
        "middle_AT_right": (1, 3, 4),
        "middle_AT_left_secondary": (1, 3, 4),
    }
    selected_ledgers = {}
    for name, triple in selected.items():
        hit = next(entry for entry in censuses[name] if entry[:3] == triple)
        head, first, second, ranks, activity = hit
        require(ranks == (3, 3, 3, 3),
                f"{name} selected pair stopped being doubly good: {ranks}")
        require(all(activity), f"{name} selected pair became inactive")
        first_entries = direct_entries(oo, sources[name], (head, first))
        second_entries = direct_entries(oo, sources[name], (head, second))
        require(len(first_entries) == len(second_entries) == 1,
                f"{name} selected direct block stopped being literal rank one")
        require(first_entries[0][1] != second_entries[0][1],
                f"{name} outer target lines stopped being distinct")
        selected_ledgers[name] = {
            "pair": triple,
            "first_direct": first_entries,
            "second_direct": second_entries,
            "star_ranks": ranks,
            "cofactor_terms": activity,
        }

    # The known endpoint-star crossed calibration is rank-deficient at two
    # deleted stars.  These repair-induced pairs have the genuinely different
    # (3,3,3,3) signature, so they are not a relabel of that affine chart.
    known_crossed_ranks = (2, 2, 3, 3)
    require(all(value["star_ranks"] != known_crossed_ranks
                for value in selected_ledgers.values()),
            "an internal repair collapsed to the known crossed rank packet")

    # For an exact source, the pinned flat-bicase theorem makes every such
    # active shared rank-one pair with distinct outer target lines nonflat.
    # Together with (3,3,3,3), this is exactly the curved doubly-good route.
    ledger = {
        "dependencies": PINS,
        "complete_four_row_residuals": expected_rows,
        "left_repair_forced_secondary": {
            "word": "".join(map(str, left_cross_word)),
            "polynomial": ["*".join(term) for term in sorted(left_cross)],
            "forced_product": "q13:01*q24:21",
        },
        "repair_touching_reselection_census": {
            name: serial_census(census) for name, census in censuses.items()
        },
        "selected_packets": selected_ledgers,
        "known_crossed_affine_star_ranks": known_crossed_ranks,
        "verdict": (
            "shared C/A and right A/T repairs directly expose active doubly-"
            "good rank-one pairs; the left A/T repair has no rank-one "
            "repair-edge reselection but its first complete Qc cross row "
            "forces a secondary product that exposes the same packet"
        ),
        "exact_source_consequence": (
            "on an exact completion of one of these finite carrier charts, "
            "the shared-reciprocal flat-bicase unit forces nonflatness, so "
            "the selected (3,3,3,3) active packet enters the curved doubly-"
            "good overlap route; this does not itself construct an active "
            "clean cap, and transport of an arbitrary curved doubly-good "
            "packet remains open"
        ),
        "scope": (
            "finite carrier-only fixed-star/direct calibrations and their "
            "complete four common-q tensor rows; no arbitrary extra endpoint-"
            "star components or general extra-support layer is included"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"the internal-repair reselection ledger changed: {digest}")

    print("h=3 same-hole internal repair reselection: PASS")
    print("repair-touching pair counts: shared/left/right/left+2 = 7/0/11/7")
    print("selected repair packets: active, star ranks (3,3,3,3)")
    print("left A/T route: Qc(10211) forces q13:01*q24:21")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
