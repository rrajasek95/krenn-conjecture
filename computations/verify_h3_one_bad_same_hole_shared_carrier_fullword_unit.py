#!/usr/bin/env python3
"""Literal full-word unit on the canonical shared-C/A carrier packet.

Take exactly the 17 physical cells in f057798's shared-C/A carrier
calibration, with no extra residue support.  The pure word 00000000 and the
mixed word 00000001 have the same unique physical matching; only the R_a/R_c
decoration on edge 27 changes.  Their two source rows give R_c in the ideal,
so localization at the forced R_c unit makes the complete full-word ideal the
unit ideal.  At the fixed same-hole normalization the identity is ordinary.
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
    "computations/verify_h3_one_bad_same_hole_internal_repair_reselection.py":
        "1bb3893ca00863752f2deb5a715369647c9a0f351cdef0f2ad0985a18d672452",
}
EXPECTED_LEDGER_SHA256 = (
    "1e3ba378f134854f2e6e4a73baa7524ad41bef5486e4b4e731da1126dcfbd454"
)

VERTICES = tuple(range(8))
COLORS = tuple(range(3))
PURE = (0,) * 8
MIXED = tuple(map(int, "00000001"))
MATCHING = ((0, 1), (2, 7), (3, 4), (5, 6))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"dependency changed: {relative}: {actual}")


def clean(poly):
    return Counter({monomial: coefficient
                    for monomial, coefficient in poly.items() if coefficient})


def add(*terms):
    answer = Counter()
    for poly, scalar in terms:
        for monomial, coefficient in poly.items():
            answer[monomial] += scalar * coefficient
    return clean(answer)


def multiply_variable(poly, variable):
    return clean(Counter({tuple(sorted(monomial + (variable,))): coefficient
                          for monomial, coefficient in poly.items()}))


def specialize(poly, values):
    answer = Counter()
    for monomial, coefficient in poly.items():
        kept = []
        for variable in monomial:
            if variable in values:
                coefficient *= values[variable]
            else:
                kept.append(variable)
        answer[tuple(kept)] += coefficient
    return clean(answer)


def variable_name(cell):
    u, v, a, b = cell
    return f"x{u}{v}_{a}{b}"


def full_word_rows(base, support):
    names = {cell: variable_name(cell) for cell in support}
    rows = {}
    live = {}
    for word in itertools.product(COLORS, repeat=8):
        polynomial = Counter()
        matchings = []
        for matching in base.perfect_matchings(VERTICES):
            cells = tuple(base.cell(u, v, word[u], word[v])
                          for u, v in matching)
            if not all(cell in support for cell in cells):
                continue
            polynomial[tuple(sorted(names[cell] for cell in cells))] += 1
            matchings.append(matching)
        polynomial = clean(polynomial)
        if polynomial:
            rows[word] = polynomial
            live[word] = tuple(matchings)
    return rows, live


def serial_poly(poly):
    return {"*".join(monomial) if monomial else "1": str(coefficient)
            for monomial, coefficient in sorted(poly.items())}


def main():
    pin_dependencies()
    base = importlib.import_module(
        "verify_h3_one_bad_common_q_cap_extraction_boundary")
    repair = importlib.import_module(
        "verify_h3_one_bad_same_hole_internal_repair_reselection")

    common = repair.common_packets(base.cell)["shared_CA"]
    source = Counter(common)
    source.update(repair.outer_source(base.cell))
    require(len(source) == 17 and all(source.values()),
            "the canonical carrier support/units changed")

    physical_rows, live = full_word_rows(base, source)
    require(len(physical_rows) == 29,
            f"the nonzero full-word row count changed: {len(physical_rows)}")
    require(sum(map(len, physical_rows.values())) == 31,
            "the full-word monomial count changed")
    require(Counter(map(len, physical_rows.values()))
            == Counter({1: 27, 2: 2}),
            "the full-word row-size histogram changed")

    target_words = {(colour,) * 8 for colour in COLORS}
    unique_mixed = tuple(sorted(
        word for word, polynomial in physical_rows.items()
        if word not in target_words and len(polynomial) == 1
    ))
    require(len(unique_mixed) == 24,
            f"the localized one-row unit count changed: {len(unique_mixed)}")

    require(live[PURE] == (MATCHING,) and live[MIXED] == (MATCHING,),
            f"the two-row matching changed: {live[PURE]}, {live[MIXED]}")
    base_monomial = tuple(sorted((
        variable_name(base.cell(0, 1, 0, 0)),
        variable_name(base.cell(3, 4, 0, 0)),
        variable_name(base.cell(5, 6, 0, 0)),
    )))
    ra = variable_name(base.cell(2, 7, 0, 0))
    rc = variable_name(base.cell(2, 7, 0, 1))
    expected_pure = Counter({tuple(sorted(base_monomial + (ra,))): 1})
    expected_mixed = Counter({tuple(sorted(base_monomial + (rc,))): 1})
    require(physical_rows[PURE] == expected_pure
            and physical_rows[MIXED] == expected_mixed,
            "the pure/mixed common tail changed")

    pure_generator = add((physical_rows[PURE], 1), (Counter({(): 1}), -1))
    mixed_generator = physical_rows[MIXED]
    # ra*G_mixed - rc*G_pure = rc.  Since rc is one of the fixed nonzero
    # same-hole stars, the localized full-word ideal contains one.
    localized_certificate = add(
        (multiply_variable(mixed_generator, ra), 1),
        (multiply_variable(pure_generator, rc), -1),
    )
    require(localized_certificate == Counter({(rc,): 1}),
            f"the determinant-cleared localized unit changed: {localized_certificate}")

    # On the exact fixed-star normalization used by f057798,
    # ra=1, rc=-2 and the pq direct coefficient is one.  The same two rows
    # give the ordinary rational identity (-1/2)G_mixed-G_pure=1.
    fixed_values = {
        variable_name(cell): Fraction(value)
        for cell, value in repair.outer_source(base.cell).items()
    }
    fixed_pure = specialize(pure_generator, fixed_values)
    fixed_mixed = specialize(mixed_generator, fixed_values)
    ordinary_unit = add((fixed_mixed, Fraction(-1, 2)),
                        (fixed_pure, -1))
    require(ordinary_unit == Counter({(): 1}),
            f"the fixed-star ordinary unit changed: {ordinary_unit}")

    # The global ideal has all 3^8 literal word generators.  Exactly 29 have
    # a physical tail on this support; the other 6532 mixed rows are literal
    # zeros.  Target subtraction is performed only on the three pure rows.
    generator_count = 3 ** 8
    require(generator_count - len(physical_rows) == 6532,
            "the zero full-word row count changed")

    ledger = {
        "dependencies": PINS,
        "support_cells": len(source),
        "localized_cells": tuple(sorted(variable_name(cell) for cell in source)),
        "full_word_ideal": {
            "generators": generator_count,
            "nonzero_physical_rows": len(physical_rows),
            "literal_zero_rows": generator_count - len(physical_rows),
            "physical_monomials": sum(map(len, physical_rows.values())),
            "row_size_histogram": dict(sorted(Counter(
                map(len, physical_rows.values())).items())),
            "unique_mixed_monomial_rows": len(unique_mixed),
        },
        "two_row_certificate": {
            "pure_word": "00000000",
            "mixed_word": "00000001",
            "unique_matching": MATCHING,
            "pure_generator": serial_poly(pure_generator),
            "mixed_generator": serial_poly(mixed_generator),
            "determinant_cleared_identity": "ra*Gmixed-rc*Gpure=rc",
            "fixed_star_identity": "1=(-1/2)*Gmixed-Gpure",
        },
        "verdict": (
            "the exact 17-cell canonical shared-C/A carrier packet is empty: "
            "its localized full-word ideal is the unit ideal, and at the "
            "fixed same-hole normalization two literal rows give an ordinary "
            "rational source unit"
        ),
        "scope": (
            "exact carrier-only support from f057798 with fixed endpoint "
            "stars/directs; no arbitrary residue support, no general curved-"
            "OO transport, and no conclusion for larger support strata"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"the full-word unit ledger changed: {digest}")

    print("h=3 same-hole shared-carrier full-word unit: PASS")
    print("literal full-word ideal: 6561 rows; 29 nonzero tails; 31 monomials")
    print("localized monomial units: 24 mixed rows")
    print("ordinary two-row unit: 1=(-1/2)G_00000001-G_00000000")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
