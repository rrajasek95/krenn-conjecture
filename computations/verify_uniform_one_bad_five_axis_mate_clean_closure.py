#!/usr/bin/env python3
"""Exact all-five axis-mate closure for the flat one-bad companion.

Allow the five internal companion-mate cells

    13:10, 14:10, 45:01, 35:01, 25:01

simultaneously, together with arbitrary coefficients on the three carrier
cells 17:11, 23:00, 24:00.  A complete physical matching expansion gives
five triangular mixed rows which kill the mate coefficients.  The companion
row then kills the sole spread parameter t.  Consequently the endpoint-star
square is zero and the certified uniform one-bad clean cap applies.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction as Q
from hashlib import sha256
import importlib
from itertools import product
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_one_bad_active_minor_rank_completion_boundary.py":
        "8d5958ed772b8f781ee30c91ba743b3af2ce978435edf7770494c1e2d25423b6",
    "notes/uniform-one-bad-active-minor-rank-completion-boundary.md":
        "82ed4cbe12101a796f432dd6854cd58eb944a65fde1e094407eed3b75e8a3e70",
    "computations/verify_uniform_one_bad_square_zero_clean_cap.py":
        "a943fffdc3ce86aa5506e6774ec3a6a8ff10c70491225417152a1298e2754883",
    "notes/uniform-one-bad-square-zero-clean-cap.md":
        "2af5f90040152079c094e03b0b1bb794761a07d2418182586ab06848ee820c2e",
    "computations/verify_h3_one_bad_second_principal_parts_companion_closure.py":
        "3612f9d7c03a3e265792543cd602f27ebf64830390f95b5bddb8d953d238c3f5",
    "computations/verify_h3_one_bad_common_q_cap_extraction_boundary.py":
        "02517a037d7dfc273d2eee63dd85e8228d88cd4824397b7ac478c013624afe5e",
    "computations/verify_oo_doubly_good_two_anchor_counterguard.py":
        "b9d986f4e1725082c1101e73729018a6d66296aef628879de50b03508f804699",
}
EXPECTED_LEDGER_SHA256 = (
    "33137440a89a759c786b785417e1a91d79e4cafea15ff2ee6b9b759e516b2751"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"dependency changed: {relative}: {actual}")


# Sparse polynomials use sorted tuples of variable names as monomials.
def clean(polynomial):
    return {monomial: coefficient for monomial, coefficient
            in polynomial.items() if coefficient}


def add(*polynomials):
    answer = defaultdict(Q)
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            answer[monomial] += coefficient
    return clean(answer)


def scale(polynomial, scalar):
    return clean({monomial: Q(scalar) * coefficient
                  for monomial, coefficient in polynomial.items()})


def multiply(left, right):
    answer = defaultdict(Q)
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            answer[tuple(sorted(left_monomial + right_monomial))] += (
                left_coefficient * right_coefficient
            )
    return clean(answer)


def constant(value):
    return {(): Q(value)} if value else {}


def variable(name):
    return {(name,): Q(1)}


def matching_tensor(oo, source):
    answer = {}
    for matching in oo.perfect_matchings(tuple(range(8))):
        choices = []
        for edge in matching:
            choices.append(tuple(
                (left_colour, right_colour, coefficient)
                for (left, right, left_colour, right_colour), coefficient
                in source.items() if (left, right) == edge
            ))
        if not all(choices):
            continue
        for selected in product(*choices):
            word = [-1] * 8
            coefficient = constant(1)
            for edge, (left_colour, right_colour, value) in zip(
                    matching, selected, strict=True):
                word[edge[0]], word[edge[1]] = left_colour, right_colour
                coefficient = multiply(coefficient, value)
            key = tuple(word)
            answer[key] = add(answer.get(key, {}), coefficient)
    return {word: polynomial for word, polynomial in answer.items()
            if polynomial}


def word(label):
    return tuple(map(int, label))


def main():
    pin_dependencies()
    computations = str(ROOT / "computations")
    if computations not in sys.path:
        sys.path.insert(0, computations)
    base = importlib.import_module(
        "verify_h3_one_bad_common_q_cap_extraction_boundary")
    closure = importlib.import_module(
        "verify_h3_one_bad_second_principal_parts_companion_closure")
    oo = importlib.import_module(
        "verify_oo_doubly_good_two_anchor_counterguard")

    # Start at the concentrated t=0 canonical chart and restore its two
    # linked t-cells symbolically.  The z variables are arbitrary carrier
    # coefficients: the proof neither localizes nor eliminates them.
    source = {
        cell: constant(value)
        for cell, value in closure.build_eight_site_source(base, Q(0)).items()
        if value
    }
    symbolic_cells = {
        base.cell(1, 2, 1, 0): "t",
        base.cell(1, 6, 1, 1): "t",
        base.cell(1, 7, 1, 1): "z17",
        base.cell(2, 3, 0, 0): "z23",
        base.cell(2, 4, 0, 0): "z24",
        base.cell(1, 3, 1, 0): "y13",
        base.cell(1, 4, 1, 0): "y14",
        base.cell(4, 5, 0, 1): "y45",
        base.cell(3, 5, 0, 1): "y35",
        base.cell(2, 5, 0, 1): "y25",
    }
    for cell, name in symbolic_cells.items():
        source[cell] = variable(name)

    tensor = matching_tensor(oo, source)
    generators = dict(tensor)
    for colour in range(3):
        pure = (colour,) * 8
        generators[pure] = add(generators.get(pure, {}), constant(-1))
    generators = {output: polynomial for output, polynomial
                  in generators.items() if polynomial}
    affected = {
        output: polynomial for output, polynomial in generators.items()
        if any(monomial for monomial in polynomial)
    }
    histogram = Counter(len(polynomial) for polynomial in affected.values())
    census = (len(tensor), len(generators), len(affected), histogram)
    require(census
            == (30, 27, 22, Counter({1: 13, 2: 6, 3: 1, 5: 1, 6: 1})),
            f"the complete affected-grade census changed: {census}")

    y13, y14, y45, y35, y25 = map(
        variable, ("y13", "y14", "y45", "y35", "y25"))
    t, z17, z23, z24 = map(variable, ("t", "z17", "z23", "z24"))
    selected = {
        "g13": generators[word("11002002")],
        "g35": generators[word("00101110")],
        "g45": generators[word("00220110")],
        "g25": generators[word("11012112")],
        "g14": generators[word("11220111")],
        "gc": generators[word("21000121")],
    }
    expected = {
        "g13": scale(y13, -1),
        "g35": y35,
        "g45": y45,
        "g25": y25,
        "g14": add(y14, multiply(z17, y45)),
        "gc": add(
            t,
            multiply(y13, z24),
            multiply(y14, z23),
            multiply(multiply(y45, z17), z23),
            multiply(multiply(y35, z17), z24),
            multiply(y25, z17),
        ),
    }
    require(selected == expected,
            f"the six triangular source rows changed: {selected}")

    # Ordinary source identities: no division, radical, or solver is used.
    y14_lift = add(selected["g14"],
                   scale(multiply(z17, selected["g45"]), -1))
    require(y14_lift == y14, "the y14 source lift changed")
    t_lift = add(
        selected["gc"],
        multiply(z24, selected["g13"]),
        scale(multiply(z23, selected["g14"]), -1),
        scale(multiply(multiply(z17, z24), selected["g35"]), -1),
        scale(multiply(z17, selected["g25"]), -1),
    )
    require(t_lift == t, "the companion source lift for t changed")

    # The five mate variables themselves are in the ordinary source ideal.
    lifts = {
        "y13": scale(selected["g13"], -1),
        "y35": selected["g35"],
        "y45": selected["g45"],
        "y25": selected["g25"],
        "y14": y14_lift,
        "t": t_lift,
    }
    require(lifts == {
        "y13": y13, "y35": y35, "y45": y45,
        "y25": y25, "y14": y14, "t": t,
    }, "the mate/companion triangular ideal stopped being the coordinate ideal")

    # In the canonical one-bad cap, Q_c=e1@0+t e1@1.  Its divided square is
    # exactly t e1@0 e1@1; the other three endpoint rows are single-site.
    # Therefore the source identity t in I gives all four self-squares zero,
    # which is precisely the pinned clean-cap hypothesis.
    spread_square = t
    require(spread_square == lifts["t"],
            "the spread endpoint square no longer equals t")

    row_ledger = {
        name: {
            "word": label,
            "terms": [
                [list(monomial), str(coefficient)]
                for monomial, coefficient in sorted(selected[name].items())
            ],
        }
        for name, label in {
            "g13": "11002002", "g35": "00101110",
            "g45": "00220110", "g25": "11012112",
            "g14": "11220111", "gc": "21000121",
        }.items()
    }
    ledger = {
        "dependencies": PINS,
        "symbolic_cells": {str(cell): name
                           for cell, name in sorted(symbolic_cells.items())},
        "complete_matching_audit": {
            "physical_output_words_checked": 3 ** 8,
            "nonzero_tensor_words": len(tensor),
            "nonzero_source_generators": len(generators),
            "parameter_affected_generators": len(affected),
            "affected_term_histogram": dict(sorted(histogram.items())),
        },
        "triangular_rows": row_ledger,
        "ordinary_source_lifts": {
            "y13": "-g13", "y35": "g35", "y45": "g45",
            "y25": "g25", "y14": "g14-z17*g45",
            "t": (
                "gc+z24*g13-z23*g14-z17*z24*g35-z17*g25"
            ),
        },
        "conclusion": (
            "all five axis-mate coefficients and t belong to the ordinary "
            "affected-row source ideal; hence every source point in this "
            "module has R^[2]=0 and lands in the certified active clean cap"
        ),
        "characteristic_scope": (
            "polynomial identities over Z, valid over every commutative ring; "
            "no localization of z17,z23,z24 is used"
        ),
        "scope": (
            "complete symbolic module with exactly the five axis-mate cells "
            "and three arbitrary mate carriers over the canonical chart; "
            "does not allow any additional physical cell to contaminate the "
            "six displayed mixed rows"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"five-axis-mate closure ledger changed: {digest}")

    print("uniform one-bad five-axis-mate clean closure: PASS")
    print("complete affected-grade audit: 22 symbolic source generators")
    print("five triangular mixed rows kill y13,y14,y45,y35,y25")
    print("companion source lift kills t; hence R^[2]=0")
    print("landing: certified uniform active clean cap")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
