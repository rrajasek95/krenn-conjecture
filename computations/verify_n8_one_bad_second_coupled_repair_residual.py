#!/usr/bin/env python3
"""Exact second-route residual above the sharp one-bad N=8 packets.

For each of the eight first-mate charts, and for each private mixed top word
created by that mate, adjoin one of the other fourteen decorated perfect
matchings of the same word.  These are the 168 literal direct second routes.

The old cross equation forces the first mate product nonzero.  The selected
mixed top equation then forces the second-route product nonzero.  We audit
the complete top tensor and all four binary response rows and show that
every resulting chart still has a forbidden singleton fibre.  Its monomial
uses only base, first-mate, and second-route cells, all of which are forced
nonzero.  Thus it is a multiplication-safe obstruction on the chart, not
an unsigned-support heuristic.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIRST = "computations/verify_n8_one_bad_first_cross_mate_exchange.py"
FIRST_HASH = "e1d641d64bf0659d6b28ea64bf8a935e17c4da1c7e2c831f0dfb041fc78eaf0c"
EXPECTED_DIGEST = "f992ba8a9e6ba72fe3fe6c7ddc860e5e4d4630e05028b88df177fd54d3e6d996"


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def load_first():
    path = ROOT / FIRST
    actual = sha256(path.read_bytes()).hexdigest()
    require(actual == FIRST_HASH, f"dependency changed: {FIRST}: {actual}")
    spec = spec_from_file_location("one_bad_first_mate", path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def cell_from_json(item):
    edge, colours = item
    return tuple(edge), tuple(colours)


def decompositions(first, cells, number, fixed, word):
    answer = []
    for selected in itertools.combinations(cells, number):
        if first.endpoint_tensor(selected, number, fixed).get(tuple(word)):
            answer.append(tuple(selected))
    return answer


def defect_fibres(first, base, packet, cells):
    a_matching, b_matching, b_holes, c_matching, c_holes = packet
    defects = []

    top = first.endpoint_tensor(cells, 3)
    for word, coefficient in sorted(top.items()):
        if word == (base.A,) * 6:
            continue
        routes = decompositions(first, cells, 3, (), word)
        require(len(routes) == coefficient,
                "top coefficient/decomposition count changed")
        if len(routes) == 1:
            defects.append(("top", word, routes[0]))

    rows = (
        ("bb", base.B, b_holes[0], base.B, b_holes[1]),
        ("bc", base.B, b_holes[0], base.C, c_holes[1]),
        ("cb", base.C, c_holes[0], base.B, b_holes[1]),
        ("cc", base.C, c_holes[0], base.C, c_holes[1]),
    )
    for name, left_colour, left_hole, right_colour, right_hole in rows:
        if left_hole == right_hole:
            response = Counter()
        else:
            fixed = ((left_hole, left_colour),
                     (right_hole, right_colour))
            response = first.endpoint_tensor(cells, 2, fixed)
        target = ((left_colour,) * 6
                  if left_colour == right_colour else None)
        for word, coefficient in sorted(response.items()):
            if word == target:
                continue
            routes = decompositions(first, cells, 2, fixed, word)
            require(len(routes) == coefficient,
                    "response coefficient/decomposition count changed")
            if len(routes) == 1:
                defects.append((name, word, routes[0]))
    return defects


def audit_second_routes(first):
    base = first.load_base()
    first_audit = first.audit_mates(base)
    require(len(first_audit["charts"]) == 8,
            "first-mate chart count changed")

    records = []
    size_census = Counter()
    defect_count_census = Counter()
    fresh_defect_count_census = Counter()
    defect_row_census = Counter()
    orbit_census = Counter()
    smallest = None

    for first_index, chart in enumerate(first_audit["charts"]):
        orbit = chart["sharp_orbit"]
        packet = base.SHARP_REPRESENTATIVES[orbit]
        a_matching, b_matching, b_holes, c_matching, c_holes = packet
        source = (
            tuple((edge, (base.A, base.A)) for edge in a_matching)
            + tuple((edge, (base.B, base.B)) for edge in b_matching)
            + tuple((edge, (base.C, base.C)) for edge in c_matching)
        )
        mate = tuple(cell_from_json(item) for item in chart["mate"])
        first_cells = source + mate
        require(len(set(first_cells)) == 9,
                "a first mate reused a decorated cell")

        for witness_index, witness in enumerate(chart["private_top_witnesses"]):
            word = tuple(witness["word"])
            trigger = tuple(cell_from_json(item)
                            for item in witness["matching"])
            require(decompositions(first, first_cells, 3, (), word)
                    == [trigger],
                    "the selected first-mate top word stopped being private")

            alternatives = []
            for physical in base.perfect_matchings(base.SITES):
                route = tuple(
                    (edge, (word[edge[0]], word[edge[1]]))
                    for edge in physical
                )
                if frozenset(route) == frozenset(trigger):
                    continue
                missing = tuple(cell for cell in route
                                if cell not in first_cells)
                require(missing,
                        "a second top route was already supported")
                alternatives.append((route, missing))
            require(len(alternatives) == 14,
                    "a private top word lost a perfect-matching route")

            for alternative_index, (route, missing) in enumerate(alternatives):
                second_cells = first_cells + missing
                require(len(set(second_cells)) == len(second_cells),
                        "a second route added a duplicate cell")
                selected_routes = decompositions(
                    first, second_cells, 3, (), word
                )
                selected_sets = {frozenset(value) for value in selected_routes}
                require(frozenset(trigger) in selected_sets and
                        frozenset(route) in selected_sets,
                        "the direct second route failed to repair its target")
                require(len(selected_routes) >= 2,
                        "the selected top fibre remained private")

                defects = defect_fibres(
                    first, base, packet, second_cells
                )
                require(defects,
                        "a direct second-route chart removed every singleton")

                # Every cell is forced nonzero on this chart: the seven base
                # cells occur in the nonzero pure/diagonal anchors; both mate
                # cells are forced by cancellation of the old private cross
                # monomial; every missing cell occurs in the selected second
                # route, whose product must cancel the nonzero trigger.
                forced_nonzero = set(second_cells)
                require(all(set(monomial) <= forced_nonzero
                            for row, defect_word, monomial in defects),
                        "a residual singleton used an unforced cell")
                fresh_defects = [
                    defect for defect in defects
                    if set(defect[2]) & set(missing)
                ]
                require(fresh_defects,
                        "a direct second route created no fresh singleton")

                size = len(missing)
                size_census[size] += 1
                defect_count_census[len(defects)] += 1
                fresh_defect_count_census[len(fresh_defects)] += 1
                defect_row_census.update(row for row, _, _ in defects)
                orbit_census[orbit] += 1
                record = {
                    "first_chart": first_index,
                    "sharp_orbit": orbit,
                    "witness": witness_index,
                    "second_route": alternative_index,
                    "new_cells": [
                        [list(edge), list(colours)]
                        for edge, colours in missing
                    ],
                    "new_cell_count": size,
                    "selected_word": list(word),
                    "residual_singletons": [
                        {
                            "row": row,
                            "word": list(defect_word),
                            "monomial": [
                                [list(edge), list(colours)]
                                for edge, colours in monomial
                            ],
                        }
                        for row, defect_word, monomial in defects
                    ],
                    "fresh_second_route_singletons": [
                        {
                            "row": row,
                            "word": list(defect_word),
                            "monomial": [
                                [list(edge), list(colours)]
                                for edge, colours in monomial
                            ],
                        }
                        for row, defect_word, monomial in fresh_defects
                    ],
                }
                records.append(record)
                key = (size, len(defects), first_index,
                       witness_index, alternative_index)
                if smallest is None or key < smallest[0]:
                    smallest = (key, record)

    require(len(records) == 168,
            f"direct second-route census changed: {len(records)}")
    require(orbit_census == Counter({0: 112, 1: 56}),
            f"second-route orbit census changed: {orbit_census}")
    require(sum(size_census.values()) == 168,
            "second-route size census changed total")
    require(sum(defect_count_census.values()) == 168,
            "residual singleton census changed total")
    smallest_record = smallest[1]
    require((smallest_record["first_chart"], smallest_record["witness"],
             smallest_record["second_route"],
             smallest_record["new_cell_count"]) == (0, 1, 9, 2),
            "the smallest second-route residual chart changed")
    require([
        (item["row"], item["word"])
        for item in smallest_record["fresh_second_route_singletons"]
    ] == [
        ("top", [0, 0, 0, 1, 2, 2]),
        ("top", [1, 1, 2, 2, 0, 1]),
    ], "the two fresh multiplication-safe residuals changed")
    return {
        "first_mate_charts": 8,
        "private_top_witnesses": 12,
        "alternate_routes_per_witness": 14,
        "direct_second_route_charts": len(records),
        "sharp_orbit_charts": dict(sorted(orbit_census.items())),
        "new_cell_count_census": dict(sorted(size_census.items())),
        "residual_singleton_count_census": dict(
            sorted(defect_count_census.items())
        ),
        "fresh_second_route_singleton_count_census": dict(
            sorted(fresh_defect_count_census.items())
        ),
        "residual_singleton_row_census": dict(
            sorted(defect_row_census.items())
        ),
        "smallest_residual": smallest_record,
        "verdict": (
            "every direct second route leaves a forbidden singleton whose "
            "monomial consists entirely of forced-nonzero chart cells"
        ),
        "scope": (
            "one first alternate-K4 mate plus one direct alternate perfect "
            "matching for one induced private top word; simultaneous third "
            "routes or different leading supports are not excluded"
        ),
    }


def main():
    first = load_first()
    audit = audit_second_routes(first)
    ledger = {
        "first_mate_dependency": {"path": FIRST, "sha256": FIRST_HASH},
        "second_coupled_repair": audit,
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    print(json.dumps(audit, indent=2, sort_keys=True))
    print("sha256:", digest)
    require(EXPECTED_DIGEST == "TO_BE_FILLED" or digest == EXPECTED_DIGEST,
            f"second-route ledger changed: {digest}")


if __name__ == "__main__":
    main()
