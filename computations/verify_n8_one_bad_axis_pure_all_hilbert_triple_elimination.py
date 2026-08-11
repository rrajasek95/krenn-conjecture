#!/usr/bin/env python3
"""Coefficient elimination of all 58 primitive mixed Hilbert triples.

Adjoin one pair-free degree-three circuit at a time to the full symbolic pure
chart, with all fifteen 00 cells retained, and expand q^[3] plus the four
literal response tensors.  The canonical circuit has three independent
private response rows which kill its carriers.  A deterministic exact audit
finds three successive unit rows for all 58 circuits in all 18 chart orbits.

This is a degree-three theorem only; simultaneous non-circuit triples and
degree-four Hilbert elements are outside scope.
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
    "computations/verify_n8_one_bad_axis_pure_mixed_weight_hilbert_circuits.py":
        "3b1737f02c8746ce8964c3b1b53a713961de7f8ab00f0dd8141e5e7b8647d1c2",
    "computations/verify_n8_one_bad_axis_pure_all_opposing_pair_elimination.py":
        "2c7ab786a4b0efeb0a4a02e85268d0decef86de0986c1fb0ae567f013676d97c",
    "computations/verify_n8_one_bad_endpoint_minor_unary_top_completion.py":
        "f0d4c5382cce1ccb8bed5a5ac0afa8cf8662c905bd0c675a56b51f2be7d0b574",
}
EXPECTED_LEDGER_SHA256 = "9c197315dbfdd941856b215705921eb14737466bb0be79341bdc4e9b962c92fa"

SITES = tuple(range(6))
COLOURS = tuple(range(3))
CARRIER_NAMES = ("x", "y", "r")
CANONICAL = (
    (0, 1, 0, 2),
    (2, 4, 1, 2),
    (3, 4, 0, 1),
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"dependency changed: {relative}: {actual}")


def variable(name):
    return Counter({(name,): Fraction(1)})


def build_q(module, triple):
    q_cells = {
        module.source_cell(2, 4, 1, 1): variable("A"),
        module.source_cell(3, 5, 1, 1): variable("B"),
        module.source_cell(0, 5, 2, 2): variable("C"),
        module.source_cell(1, 4, 2, 2): variable("D"),
    }
    for left, right in itertools.combinations(SITES, 2):
        q_cells[module.source_cell(left, right, 0, 0)] = variable(
            f"z{left}{right}"
        )
    for cell, name in zip(triple, CARRIER_NAMES, strict=True):
        q_cells[module.source_cell(*cell)] = variable(name)
    return q_cells


def specialize(polynomial, killed):
    return Counter({term: coefficient for term, coefficient in polynomial.items()
                    if not any(variable in term for variable in killed)})


def eliminate_triple(all_pairs, equations):
    alive = set(CARRIER_NAMES)
    killed = set()
    ledger = []
    while alive:
        found = None
        for sector, word, polynomial in sorted(
                equations, key=lambda item: (item[0], item[1])):
            reduced = specialize(polynomial, killed)
            if len(reduced) != 1:
                continue
            term, coefficient = next(iter(reduced.items()))
            carriers = tuple(name for name in sorted(alive) if name in term)
            if len(carriers) != 1:
                continue
            carrier = carriers[0]
            if not set(term) - {carrier} <= all_pairs.KNOWN_UNITS:
                continue
            require(sector == "top" or word != (0,) * 6,
                    "a response killer used the pure top word")
            found = {
                "carrier": carrier,
                "sector": sector,
                "word": "".join(map(str, word)),
                "monomial": "*".join(term),
                "coefficient": str(coefficient),
                "factor_class": all_pairs.factor_class(term, carrier),
                "direct_safe_mod_top": True,
            }
            break
        require(found is not None,
                f"the triple stalled after killing {sorted(killed)}")
        ledger.append(found)
        killed.add(found["carrier"])
        alive.remove(found["carrier"])
    require(len(ledger) == 3, "the triple elimination length changed")
    return tuple(ledger)


def main():
    pin_dependencies()
    hilbert = importlib.import_module(
        "verify_n8_one_bad_axis_pure_mixed_weight_hilbert_circuits")
    torus = importlib.import_module(
        "verify_n8_one_bad_axis_pure_chart_torus_accessibility")
    all_pairs = importlib.import_module(
        "verify_n8_one_bad_axis_pure_all_opposing_pair_elimination")
    completion = importlib.import_module(
        "verify_n8_one_bad_endpoint_minor_unary_top_completion")
    module = importlib.import_module(
        "verify_n8_one_bad_multisite_permanent_null_defect")

    basis, _pivots = torus.nullspace(torus.equation_matrix())
    cells = tuple(
        (left, right, left_colour, right_colour)
        for left, right in itertools.combinations(SITES, 2)
        for left_colour, right_colour in itertools.product(COLOURS, repeat=2)
        if left_colour != right_colour
    )
    primitive = {
        cell: torus.primitive(torus.quotient_character(cell, basis))
        for cell in cells
    }
    triples = tuple(
        triple for triple in itertools.combinations(cells, 3)
        if hilbert.positive_three_dependence(
            *(primitive[cell] for cell in triple)
        ) is not None
    )
    require(len(triples) == 58 and triples[0] == CANONICAL,
            "the primitive triple universe changed")

    canonical_q = build_q(module, CANONICAL)
    canonical_top, canonical_responses, canonical_equations = (
        all_pairs.source_equations(completion, module, canonical_q)
    )
    canonical_private = {
        "y": ("11", tuple(map(int, "111121")),
              Counter({tuple(sorted(("B", "p0", "s1", "y"))): 1})),
        "r": ("21", tuple(map(int, "212012")),
              Counter({tuple(sorted(("C", "p2", "r", "s1"))): 1})),
        "x": ("22", tuple(map(int, "022200")),
              Counter({tuple(sorted(("p2", "s2", "x", "z45"))): 1})),
    }
    for carrier, (sector, word, expected) in canonical_private.items():
        require(canonical_responses[sector][word] == expected,
                f"the canonical private row for {carrier} changed")
        require(word not in canonical_top,
                f"a binary direct cell can contaminate {sector}@{word}")

    eliminations = {}
    sector_sequences = Counter()
    killer_histogram = Counter()
    for triple in triples:
        q_cells = build_q(module, triple)
        _top, _responses, equations = all_pairs.source_equations(
            completion, module, q_cells
        )
        elimination = eliminate_triple(all_pairs, equations)
        eliminations[str(triple)] = elimination
        sector_sequences[tuple(step["sector"] for step in elimination)] += 1
        for step in elimination:
            killer_histogram[(step["sector"], step["factor_class"])] += 1

    expected_sector_sequences = Counter({
        ("11", "12", "22"): 14,
        ("12", "12", "21"): 10,
        ("11", "21", "22"): 8,
        ("11", "21", "top"): 4,
        ("21", "22", "top"): 4,
        ("12", "12", "top"): 4,
        ("12", "22", "top"): 4,
        ("11", "12", "top"): 4,
        ("12", "21", "21"): 4,
        ("12", "21", "top"): 2,
    })
    require(sector_sequences == expected_sector_sequences,
            f"the triple sector-pattern census changed: {sector_sequences}")
    expected_killers = Counter({
        ("12", "pure-unit+stars"): 30,
        ("11", "old-q+stars"): 26,
        ("21", "old-q+stars"): 26,
        ("12", "old-q+stars"): 26,
        ("22", "old-q+stars"): 26,
        ("top", "old-q-pair"): 22,
        ("21", "pure-unit+stars"): 10,
        ("22", "pure-unit+stars"): 4,
        ("11", "pure-unit+stars"): 4,
    })
    require(killer_histogram == expected_killers
            and sum(killer_histogram.values()) == 3 * len(triples),
            f"the triple unit-row ledger changed: {killer_histogram}")

    group = all_pairs.chart_stabilizer(torus)
    orbits = hilbert.triple_orbits(all_pairs, torus, triples, group)
    require(len(orbits) == 18
            and Counter(map(len, orbits)) == Counter({4: 11, 2: 7}),
            "the primitive triple orbit census changed")

    ledger = {
        "dependencies": PINS,
        "canonical_triple": {
            "cells": CANONICAL,
            "private_rows": {
                carrier: {
                    "sector": sector,
                    "word": "".join(map(str, word)),
                    "polynomial": completion.serial_polynomial(polynomial),
                }
                for carrier, (sector, word, polynomial)
                in canonical_private.items()
            },
            "direct_contamination": 0,
            "verdict": "all three carriers vanish independently",
        },
        "all_triples": {
            "primitive_circuits": len(triples),
            "chart_orbits": len(orbits),
            "transported_canonical_orbit": len(orbits[0]),
            "nontransported_circuits": len(triples) - len(orbits[0]),
            "elimination_length_histogram": {"3": len(triples)},
            "sector_sequence_patterns": {
                "/".join(sequence): count
                for sequence, count in sorted(sector_sequences.items())
            },
            "killer_histogram": {
                f"{sector}:{factor_class}": count
                for (sector, factor_class), count
                in sorted(killer_histogram.items())
            },
            "eliminations": eliminations,
        },
        "verdict": (
            "all 58 primitive degree-three mixed Hilbert circuits are "
            "coefficient-empty on the full symbolic pure chart; each is "
            "eliminated by three successive literal unit rows"
        ),
        "scope": (
            "all fifteen pure z coefficients and one primitive three-cell "
            "circuit at a time, with q^[3] and all four response tensors; "
            "binary direct additions are zero modulo the selected mixed top "
            "rows; simultaneous non-circuit triples and degree-four or "
            "higher Hilbert elements are not classified"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"the Hilbert triple elimination ledger changed: {digest}")

    print("N=8 axis-pure Hilbert triple elimination: PASS")
    print("canonical triple: three independent private response units")
    print("primitive triples/orbits: 58/18")
    print("all triples eliminated in three literal unit rows")
    print("sector-sequence patterns: 10")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
