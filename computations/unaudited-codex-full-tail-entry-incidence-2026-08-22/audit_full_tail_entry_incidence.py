#!/usr/bin/env python3
"""Audit the full 168-cell 611 packet and fixed-entry carrier cover.

This is a finite source-label/count checker.  The unit-ideal implication uses
the separately certified N8-DIAGONAL theorem; this script does not reprove it.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).with_name("results_full_tail_entry_incidence.json")
SITES = tuple(range(8))
COLORS = (0, 1, 2)


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    a = vertices[0]
    for pos in range(1, len(vertices)):
        b = vertices[pos]
        rest = vertices[1:pos] + vertices[pos + 1 :]
        for tail in perfect_matchings(rest):
            yield ((a, b),) + tail


PM8 = tuple(perfect_matchings(SITES))


def cell_label(u: int, v: int, cu: int, cv: int) -> str:
    if u < v:
        return f"A_{u}{v}[{cu},{cv}]"
    return f"A_{v}{u}[{cv},{cu}]"


def monomial_for_word(word: tuple[int, ...], matching) -> tuple[str, ...]:
    return tuple(sorted(cell_label(u, v, word[u], word[v]) for u, v in matching))


def third_color(i: int, j: int) -> int:
    return 3 - i - j


def row_record(u: int, v: int, i: int, j: int):
    assert u < v and i != j
    k = third_color(i, j)
    word = tuple(i if a == u else j if a == v else k for a in SITES)
    tail = cell_label(u, v, i, j)
    linear = []
    quadratic = []
    for matching in PM8:
        monomial = monomial_for_word(word, matching)
        if any({a, b} == {u, v} for a, b in matching):
            assert tail in monomial
            remainder = tuple(x for x in monomial if x != tail)
            assert len(remainder) == 3
            linear.append(remainder)
        else:
            cross = [
                x
                for x in monomial
                if not (x.endswith(f"[{k},{k}]") or x.endswith(f"[{k},{k}]"))
            ]
            # Exactly the two edges incident with the singleton-colour sites
            # are cross-colour; the other two edges are k-diagonal.
            assert len(cross) == 2
            quadratic.append(monomial)
    assert len(linear) == 15
    assert len(set(linear)) == 15
    assert len(quadratic) == 90
    assert len(set(quadratic)) == 90
    return {
        "edge": [u, v],
        "endpoint_colors": [i, j],
        "majority_color": k,
        "word": "".join(map(str, word)),
        "tail_cell": tail,
        "linear_hafnian_terms": len(linear),
        "quadratic_terms": len(quadratic),
        "linear_terms": [list(x) for x in sorted(linear)],
    }


def orbit_of_cross_cell():
    # It is enough to use every ordered site image of (0,6) and every ordered
    # distinct colour image of (0,1); storage canonicalizes the edge.
    orbit = set()
    for a, b in itertools.permutations(SITES, 2):
        for i, j in itertools.permutations(COLORS, 2):
            orbit.add(cell_label(a, b, i, j))
    return orbit


def orbit_of_star_carrier():
    # A star carrier is an unordered cap pair and a residual centre outside it.
    return {
        (tuple(sorted((p, q))), a)
        for p, q in itertools.combinations(SITES, 2)
        for a in SITES
        if a not in (p, q)
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()

    rows = [
        row_record(u, v, i, j)
        for u, v in itertools.combinations(SITES, 2)
        for i, j in itertools.permutations(COLORS, 2)
    ]
    assert len(rows) == 168
    assert len({r["tail_cell"] for r in rows}) == 168
    assert len({(tuple(r["edge"]), r["majority_color"]) for r in rows}) == 84

    representative = next(
        r
        for r in rows
        if r["edge"] == [0, 6] and r["endpoint_colors"] == [0, 1]
    )
    assert representative["word"] == "02222212"

    cross_orbit = orbit_of_cross_cell()
    star_orbit = orbit_of_star_carrier()
    assert len(cross_orbit) == 168
    assert len(star_orbit) == 168
    assert representative["tail_cell"] in cross_orbit
    assert ((6, 7), 0) in star_orbit

    payload = {
        "status": "PASS",
        "scope": (
            "Finite source-label audit of the 168 literal 6+1+1 rows and "
            "the fixed-entry/four-star-blocker cover. The integral unit-ideal "
            "step is a formal corollary of certified N8-DIAGONAL. The star "
            "cover is now known to be tautological on normalized X5 by the "
            "universal five-set annihilator correction."
        ),
        "source_ring": {
            "edge_blocks": 28,
            "cells_per_block": 9,
            "variables": 252,
            "diagonal_cells": 84,
            "cross_cells": 168,
            "full_words": 6561,
            "pure_normalizations": 3,
            "mixed_rows_X5": 6558,
        },
        "full_611_packet": {
            "rows": 168,
            "linear_hafnian_terms_per_row": 15,
            "quadratic_terms_per_row": 90,
            "distinct_cofactor_factors": 84,
            "cofactor_multiplicity": 2,
            "identity": "F_e = h_e*T_e + Q_e with Q_e in J_cross^2",
            "principal_open_consequence": (
                "After inverting the product of the 84 h_e, "
                "J_cross = J_cross^2 in R/I_X5."
            ),
        },
        "certified_diagonal_consequence": {
            "dependency": "N8-DIAGONAL",
            "integral_relation": "1 in I_X5 + J_cross",
            "quotient_relation": "J_cross = R/I_X5",
            "pointwise": "Every normalized X5 point has a nonzero cross cell.",
        },
        "fixed_entry_cover": {
            "status": "TAUTOLOGICAL_ON_NORMALIZED_X5",
            "bridge_value": "NONE",
            "correction": (
                "Every exact star carrier has at least one diagonal blocker; "
                "see unaudited-codex-star-tautology-triangle-replacement."
            ),
            "cross_cell_orbit_size": len(cross_orbit),
            "star_carrier_orbit_size": len(star_orbit),
            "representative_cell": representative["tail_cell"],
            "representative_word": representative["word"],
            "matched_carrier": {"cap_pair": [6, 7], "star_centre": 0},
            "blockers": ["K00", "K11", "K22", "<K,A_67>"],
            "branches": 4,
            "witness_encoding": {
                "source_variables": 252,
                "rowspan_witness_variables": 90,
                "inverse_variables": 1,
                "total_variables": 343,
                "mixed_equations": 6558,
                "pure_equations": 3,
                "membership_coordinates": 9,
                "inverse_equation": 1,
                "total_equations": 6571,
            },
        },
        "representative_row": representative,
        "dependency_files": [
            "certification/SUPERSESSIONS.md",
            "proofs/eight-site-diagonal-obstruction.md",
            "computations/unaudited-codex-response-star-2026-08-20/REPORT.md",
            "computations/unaudited-codex-tail-polar-source-lift-2026-08-21/REPORT.md",
        ],
    }
    logical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["logical_sha256"] = hashlib.sha256(logical.encode()).hexdigest()
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.write_results:
        OUT.write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
