#!/usr/bin/env python3
"""Exclude every one-cell off-axis extension of the affine support-28 orbit.

The diagonal support-28 occurrence guard is the three-coordinate cut system
on the affine cube.  Its 48 diagonal cells are localized units.  Adjoin one
ordered off-diagonal cell on an arbitrary physical edge.  This checker proves
that at least one of the 96 literal permanent-triangle certificates is
unchanged by that cell, in both normalized target charts.  Hence the mixed
source ideal is still the unit ideal.  In particular this covers all six
off-diagonal coordinates at the endpoint-polarized cap pair 67.

The conclusion is deliberately one-cell sharp: two or more off-diagonal
cells may meet different rows of every chosen triangle and are not excluded
by this audit.
"""

from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import importlib.util
from itertools import product
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/audit_n8_support28_cube_cut_permanent_triangle_unit_independent.py":
        "cdad1bb93dba4f56cc441adab049d5eb35c16c55f5622badc6272b1e6f878489",
    "computations/verify_h3_endpoint_polarized_nine_coordinate_cap_evaluation_gate.py":
        "401a3b33b8e0082b75fe86b1476bbc94b8ab61266c2241aa86e168ce8c91f1ab",
}
EXPECTED_LEDGER_SHA256 = (
    "303fcc8d6c406ce33e5da585fe97b83735e7e9fceae1820121f75224d7a99b67"
)

FULL_TARGET_CUBE_BITS = {
    0: (0, 0, 0),
    1: (1, 1, 1),
    2: (0, 0, 1),
    3: (1, 1, 0),
    4: (1, 0, 1),
    5: (0, 1, 1),
    6: (0, 1, 0),
    7: (1, 0, 0),
}
CAP_EDGE = (6, 7)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def cut_support(base, bits):
    return {
        endpoints: tuple(
            colour for colour in base.COLORS
            if bits[endpoints[0]][colour] != bits[endpoints[1]][colour]
        )
        for endpoints in base.EDGES
    }


def triangle_words(base, triangle):
    colour, rows, columns, completions = triangle
    return tuple(
        base.word_for_minor(colour, rows, pair, completions[pair])
        for pair in ((columns[0], columns[1]),
                     (columns[0], columns[2]),
                     (columns[1], columns[2]))
    )


def augmented_hafnian(base, word, support, marked_edge, ordered_colours):
    """Literal coefficient after adjoining exactly one off-diagonal cell."""
    answer = Counter()
    offdiagonal_variable = (
        f"z{marked_edge[0]}{marked_edge[1]}_"
        f"{ordered_colours[0]}{ordered_colours[1]}"
    )
    for matching in base.MATCHINGS:
        cells = []
        for endpoints in matching:
            left, right = endpoints
            endpoint_colours = (word[left], word[right])
            if (endpoints == marked_edge
                    and endpoint_colours == ordered_colours):
                cells.append(offdiagonal_variable)
            elif (endpoint_colours[0] == endpoint_colours[1]
                  and endpoint_colours[0] in support[endpoints]):
                cells.append(base.variable(endpoint_colours[0], endpoints))
            else:
                break
        else:
            answer[tuple(sorted(cells))] += 1
    return dict(answer)


def one_cell_chart_audit(base, chart_name, support):
    triangles = base.permanent_triangles(support)
    require(len(triangles) == 96, (chart_name, len(triangles)))
    require(Counter(item[0] for item in triangles) == {0: 32, 1: 32, 2: 32},
            chart_name)

    untouched_histogram = Counter()
    endpoint_records = []
    minimum_untouched = len(triangles)
    for marked_edge in base.EDGES:
        for ordered_colours in product(base.COLORS, repeat=2):
            if ordered_colours[0] == ordered_colours[1]:
                continue
            untouched = []
            for triangle in triangles:
                words = triangle_words(base, triangle)
                require(all(
                    all(word.count(colour) % 2 == 0
                        for colour in base.COLORS)
                    for word in words
                ), ("permanent-triangle word lost even parity", triangle))
                if all(
                    augmented_hafnian(
                        base, word, support, marked_edge, ordered_colours
                    ) == base.hafnian_coefficient(word, support)
                    for word in words
                ):
                    untouched.append((triangle, words))
            require(untouched,
                    ("one cell met every permanent triangle", chart_name,
                     marked_edge, ordered_colours))
            minimum_untouched = min(minimum_untouched, len(untouched))
            untouched_histogram[len(untouched)] += 1

            # Replay an actual polynomial Laurent-unit certificate, rather
            # than merely checking that the marked endpoint colours differ.
            triangle, words = untouched[0]
            unit = base.audit_selected_unit(
                triangle,
                support,
                expected_shape=triangle[:3],
                expected_words=words,
            )
            require(unit["rhs_coefficient"] == 2
                    and unit["row_term_counts"] == (2, 2, 2),
                    (chart_name, marked_edge, ordered_colours, unit))

            if marked_edge == CAP_EDGE:
                endpoint_records.append({
                    "coordinate": "".join(map(str, ordered_colours)),
                    "untouched_triangles": len(untouched),
                    "certificate_words": list(unit["words"]),
                    "certificate_colour": triangle[0],
                })

    require(len(endpoint_records) == 6, (chart_name, endpoint_records))
    return {
        "chart": chart_name,
        "diagonal_cells": sum(map(len, support.values())),
        "permanent_triangles": len(triangles),
        "one_offdiagonal_cells_audited": len(base.EDGES) * 6,
        "minimum_untouched_triangles": minimum_untouched,
        "untouched_triangle_count_histogram": sorted(
            untouched_histogram.items()
        ),
        "cap_edge": list(CAP_EDGE),
        "cap_endpoint_offdiagonal_records": endpoint_records,
        "localized_consequence": (
            "one unchanged three-row permanent-triangle identity has RHS "
            "twice a monomial in the 48 diagonal support units"
        ),
        "parity_reason": (
            "one off-diagonal ab cell has colour-incidence parity e_a+e_b, "
            "so it cannot occur in any all-even permanent-triangle word"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("structural", "full", "exhaustive"),
                        default="structural")
    arguments = parser.parse_args()
    pin_dependencies()
    base = load(
        "computations/audit_n8_support28_cube_cut_permanent_triangle_unit_independent.py",
        "n8_support28_one_cell_base",
    )
    polarized = load(
        "computations/verify_h3_endpoint_polarized_nine_coordinate_cap_evaluation_gate.py",
        "n8_support28_one_cell_endpoint_polarization",
    )

    pair_support = cut_support(base, base.CUBE_BITS)
    full_support = cut_support(base, FULL_TARGET_CUBE_BITS)
    require(pair_support == base.SUPPORT, "pair-target cube support changed")
    require(sum(map(len, pair_support.values())) == 48
            and sum(map(len, full_support.values())) == 48,
            "affine diagonal support no longer has 48 cells")

    endpoint_evaluation = polarized.nine_coordinate_word_and_support_audit()
    require(endpoint_evaluation["coordinate_word_map_rank"] == 9
            and endpoint_evaluation["common_physical_pair"] == list(CAP_EDGE),
            endpoint_evaluation)

    charts = (
        one_cell_chart_audit(base, "pair-target-12", pair_support),
        one_cell_chart_audit(base, "full-target-012", full_support),
    )
    ledger = {
        "mode_independent": True,
        "dependencies": PINS,
        "endpoint_polarized_evaluation": {
            "physical_pair": endpoint_evaluation["common_physical_pair"],
            "coordinate_rank": endpoint_evaluation["coordinate_word_map_rank"],
            "word_family": endpoint_evaluation["cap_word_family"],
        },
        "charts": charts,
        "theorem": (
            "on either unique affine support-28 orbit, adjoining one genuine "
            "ordered off-diagonal cell leaves a literal three-row Laurent "
            "unit; hence an exact source must instead drop a diagonal unit "
            "and enter a smaller diagonal-support chart"
        ),
        "scope": (
            "this is an exact one-cell theorem; simultaneous additions of "
            "two or more off-diagonal cells are not classified; the first "
            "possible even-row repair uses two disjoint physical edges with "
            "the same unordered endpoint-colour pair"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger changed", digest, EXPECTED_LEDGER_SHA256))

    print("N=8 support-28 one-offdiagonal-cell gate: PASS")
    print("mode", arguments.mode)
    for chart in charts:
        print(chart["chart"], "cells / min untouched / histogram",
              chart["one_offdiagonal_cells_audited"],
              chart["minimum_untouched_triangles"],
              chart["untouched_triangle_count_histogram"])
    print("cap endpoint polarization rank", 9, "at edge", CAP_EDGE)
    print("consequence: mixed-row Laurent unit or diagonal support <= 47")
    print("sha256:", digest)


if __name__ == "__main__":
    main()
