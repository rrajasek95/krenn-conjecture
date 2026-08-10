#!/usr/bin/env python3
"""Exact first primitive two-transition gate in the tilted mixed chart.

The coefficient-complete 04 block contains a nonzero tt cell.  Together
with 12:aa, the existing mixed cell 02:ta has one unique primitive
same-transition partner: 14:at.  Adjoining that partner alone creates a
private mixed coefficient in K_2, so X_c leaves im(Phi).

The obstruction can be repaired source-faithfully by three coordinates.
The displayed rational packet has both bright pure images and the primitive
cycle, but still has only the original tilted kernel and excludes X_t from
im(Phi) plus every kernel product.  It is a sharp guard, not a Krenn
counterexample.
"""

from __future__ import annotations

from hashlib import sha256
import itertools
import json
from pathlib import Path

import sympy as sp

import verify_shared_reciprocal_two_bad_mixed_bright_completion as chart


ROOT = Path(__file__).resolve().parents[1]
PINNED_CHART_SHA256 = (
    "dad47bd8b73ffe7c56264038ac1720f8283e90f0df03b6aedb720277698d46f2"
)
EXPECTED_DIGEST = "cbcb78393ffb64bb63989c9a486f9bfea509679eb981e3c7aa05294273caa41b"


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def pin_dependency():
    path = ROOT / (
        "computations/"
        "verify_shared_reciprocal_two_bad_mixed_bright_completion.py"
    )
    require(sha256(path.read_bytes()).hexdigest() == PINNED_CHART_SHA256,
            "the mixed bright-completion dependency changed")


def matching_words(vertices, word):
    terms = []
    for matching in chart.perfect_matchings(vertices):
        terms.append(tuple(
            (tuple(sorted(edge)), word[edge[0]], word[edge[1]])
            for edge in matching
        ))
    return terms


def audit_unique_partner():
    existing = ((0, 2), chart.T, chart.A)
    pure_tt = ((0, 4),)
    pure_aa = ((1, 2), (0, 3))
    records = []
    for tt_edge, aa_edge in itertools.product(pure_tt, pure_aa):
        if not set(tt_edge).isdisjoint(aa_edge):
            continue
        vertices = tuple(sorted(set(tt_edge) | set(aa_edge)))
        word = {
            **{site: chart.T for site in tt_edge},
            **{site: chart.A for site in aa_edge},
        }
        terms = matching_words(vertices, word)
        for term in terms:
            if existing not in term:
                continue
            partner = next(cell for cell in term if cell != existing)
            records.append({
                "tt_edge": tt_edge,
                "aa_edge": aa_edge,
                "existing": existing,
                "partner": partner,
            })
    require(records == [{
        "tt_edge": (0, 4),
        "aa_edge": (1, 2),
        "existing": ((0, 2), chart.T, chart.A),
        "partner": ((1, 4), chart.A, chart.T),
    }], "the primitive same-transition partner changed")
    return records


def symbolic_unrepaired_gate():
    cells = chart.representative_cells()
    z = sp.Symbol("z", nonzero=True)
    y = sp.Symbol("y", nonzero=True)
    for left, right in itertools.product(range(3), repeat=2):
        value = z if (left, right) == (chart.T, chart.T) else sp.Symbol(
            f"b{left}{right}")
        chart.put(cells, 0, 4, left, right, value)
    chart.put(cells, 1, 4, chart.A, chart.T, y)

    phi, cofactors = chart.phi_matrix(cells)
    pure_word = (chart.C,) * 5
    private_word = (chart.A, chart.A, chart.C, chart.A, chart.T)
    pure_row = chart.WORDS.index(pure_word)
    private_row = chart.WORDS.index(private_word)
    pure_columns = [
        (chart.LABELS[column], sp.factor(phi[pure_row, column]))
        for column in range(phi.cols) if phi[pure_row, column] != 0
    ]
    private_columns = [
        (chart.LABELS[column], sp.factor(phi[private_row, column]))
        for column in range(phi.cols) if phi[private_row, column] != 0
    ]
    require(pure_columns == [((2, chart.C), 1)],
            "the pure-c pivot column changed")
    require(private_columns == [((2, chart.C), y)],
            "the primitive partner lost its private mixed word")

    k2_sites = tuple(site for site in chart.SITES if site != 2)
    require(cofactors[2][(chart.A, chart.A, chart.A, chart.T)] == y,
            "the private K_2 coefficient changed")
    return {
        "pure_word": pure_word,
        "private_word": private_word,
        "forced_column": (2, chart.C),
        "pure_coefficient": "1",
        "private_coefficient": "y",
        "k2_sites": k2_sites,
    }


def repaired_cells():
    cells = chart.representative_cells()
    # The selected pure tt/aa term and its primitive 02:ta,14:at cycle.
    chart.put(cells, 0, 4, chart.T, chart.T, 1)
    chart.put(cells, 1, 4, chart.A, chart.T, 1)
    # First path switch repairs K_2; the second repairs the induced K_4
    # term and simultaneously cancels the other K_2 word.
    chart.put(cells, 0, 4, chart.A, chart.T, -1)
    chart.put(cells, 1, 3, chart.A, chart.A, 1)
    chart.put(cells, 0, 3, chart.T, chart.A, -1)
    return cells


def audit_repaired_packet():
    cells = repaired_cells()
    audit = chart.full_audit(cells)
    expected_summary = (14, 1, 16, 2, (True, True, False), False)
    require(audit["summary"] == expected_summary,
            f"the repaired primitive-cycle packet changed: {audit['summary']}")

    expected_cofactors = {
        0: {(chart.A, chart.A, chart.C, chart.C): 1},
        1: {(chart.T, chart.A, chart.C, chart.C): 1},
        2: {(chart.C, chart.C, chart.C, chart.C): 1},
        3: {
            (chart.T, chart.A, chart.A, chart.T): 2,
            (chart.A, chart.A, chart.A, chart.T): -1,
        },
        4: {(chart.A, chart.A, chart.A, chart.A): 1},
    }
    require(audit["cofactors"] == expected_cofactors,
            f"the repaired literal cofactors changed: {audit['cofactors']}")

    kernel = sp.zeros(len(chart.LABELS), 1)
    kernel[chart.LABELS.index((0, chart.T))] = 1
    kernel[chart.LABELS.index((1, chart.A))] = -1
    require(audit["phi"] * kernel == sp.zeros(len(chart.WORDS), 1),
            "the repaired packet lost the tilted bridge")
    require(audit["kernel"] == [-kernel] or audit["kernel"] == [kernel],
            "the repaired packet acquired a second kernel direction")
    return {
        "cells": [
            [list(edge), left, right, str(value)]
            for (edge, left, right), value in sorted(cells.items())
        ],
        "summary": list(expected_summary[:4]),
        "cofactor_support_sizes": {
            str(hole): len(tensor)
            for hole, tensor in audit["cofactors"].items()
        },
    }


def main():
    pin_dependency()
    partner = audit_unique_partner()
    unrepaired = symbolic_unrepaired_gate()
    repaired = audit_repaired_packet()
    ledger = {
        "pinned_chart_sha256": PINNED_CHART_SHA256,
        "unique_primitive_partner": partner,
        "unrepaired_private_gate": unrepaired,
        "repaired_rational_packet": repaired,
        "verdict": (
            "the unique primitive second transition alone kills X_c; its "
            "smallest displayed source-faithful path-switch repair restores "
            "both bright classes but still excludes the pure kernel product"
        ),
        "scope": (
            "exact canonical tilted chart; not an exhaustive classification "
            "of every non-direct bright lift"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST,
                f"mixed primitive-cycle ledger changed: {digest}")

    print("shared reciprocal two-bad mixed primitive cycle: PASS")
    print("unique second transition: 14:at paired with existing 02:ta")
    print("unrepaired cycle: private K_2 word excludes X_c")
    print("repaired rational packet: rank 14, nullity 1, pure span <X_a,X_c>")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
