#!/usr/bin/env python3
"""Exact first even-cycle closure of the reduced N=8 one-bad packet.

The canonical 19-cell support has the sharp seven cells plus a K_{2,4}
binary rectangle.  Its pure top fibre is singleton, while every other live
top/response fibre has exactly two matchings.  Thus a private-word proof
cannot be oriented by uniqueness on this support.

Coefficientwise, write T_rs=u_r tensor v_s+u_s tensor v_r.  The two pure
responses are T_24=E_bb and T_35=E_cc.  Already either shared two-zero fan,
for example T_23=T_25=0, is inconsistent.  The checker verifies the support
ledger and all four exact 16-variable fan ideals over QQ.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from hashlib import sha256
import itertools
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_n8_one_bad_binary_projection_minimal_counterguards.py":
        "2b32c6d50ea1dda5a7b412a0fcd6de2373ab483b5b25eba7352684a5499e8f28",
    "computations/verify_n8_one_bad_first_cross_mate_exchange.py":
        "e1d641d64bf0659d6b28ea64bf8a935e17c4da1c7e2c831f0dfb041fc78eaf0c",
}
EXPECTED_LEDGER_SHA256 = "18bc30b370f3bff59d5eb97428dae7d7358ae0202599a606cf6f93aec93faf5e"

SITES = tuple(range(6))
B, C, A = tuple(range(3))


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"dependency changed: {relative}: {actual}")


def perfect_matchings(vertices):
    vertices = tuple(sorted(vertices))
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index, second in enumerate(vertices[1:], 1):
        remaining = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(remaining):
            yield ((first, second),) + tail


def canonical_cell(left, right, left_colour, right_colour):
    if left > right:
        left, right = right, left
        left_colour, right_colour = right_colour, left_colour
    return (left, right), left_colour, right_colour


SUPPORT = frozenset({
    # Unary top matching.
    canonical_cell(0, 1, A, A),
    canonical_cell(2, 3, A, A),
    canonical_cell(4, 5, A, A),
    # K_{2,4}: sites 0,1 carry either b or c; sites 2,4 carry b and
    # sites 3,5 carry c.
    *(canonical_cell(left, right, colour, B)
      for left in (0, 1) for right in (2, 4) for colour in (B, C)),
    *(canonical_cell(left, right, colour, C)
      for left in (0, 1) for right in (3, 5) for colour in (B, C)),
})


def decorated_matching(word, matching):
    return tuple(sorted(
        canonical_cell(left, right, word[left], word[right])
        for left, right in matching
    ))


def supported_matching_fibres():
    fibres = defaultdict(list)
    for word in itertools.product(range(3), repeat=6):
        for matching in perfect_matchings(SITES):
            decorated = decorated_matching(word, matching)
            if set(decorated) <= SUPPORT:
                fibres[("top", word)].append(decorated)

    # Ordered coordinate stars from the first sharp representative:
    # p_b@3,s_b@5 and p_c@2,s_c@4.
    rows = (
        ("bb", B, B, 3, 5),
        ("bc", B, C, 3, 4),
        ("cb", C, B, 2, 5),
        ("cc", C, C, 2, 4),
    )
    for name, left_colour, right_colour, left_hole, right_hole in rows:
        residual = tuple(site for site in SITES
                         if site not in (left_hole, right_hole))
        for residual_word in itertools.product(range(3), repeat=4):
            word = dict(zip(residual, residual_word))
            for matching in perfect_matchings(residual):
                decorated = tuple(sorted(
                    canonical_cell(left, right, word[left], word[right])
                    for left, right in matching
                ))
                if set(decorated) <= SUPPORT:
                    fibres[(name, residual_word)].append(decorated)
    return fibres


def audit_even_cycle_support():
    require(len(SUPPORT) == 19, "the rectangle support size changed")
    fibres = supported_matching_fibres()
    histogram = Counter(len(matchings) for matchings in fibres.values())
    require(histogram == Counter({2: 24, 1: 1}),
            f"the live-fibre histogram changed: {histogram}")
    singleton = [key for key, matchings in fibres.items()
                 if len(matchings) == 1]
    require(singleton == [("top", (A,) * 6)],
            f"a forbidden singleton survived: {singleton}")

    # The 24 double fibres are the four entries of six 2x2 tensors:
    # two diagonal response tensors, two cross responses, and the two
    # mixed top slices obtained by retaining top edges 23 and 45.
    require(sum(1 for key in fibres if len(fibres[key]) == 2
                and key[0] == "top") == 8,
            "the two mixed-top rectangle slices changed")
    require(sum(1 for key in fibres if len(fibres[key]) == 2
                and key[0] != "top") == 16,
            "the four response rectangle slices changed")
    return {
        "support_cells": len(SUPPORT),
        "sharp_cells": 7,
        "rectangle_cells": 16,
        "overlap_cells": 4,
        "live_fibre_histogram": [[size, count]
                                  for size, count in sorted(histogram.items())],
        "unique_fibre": "top:aaaaaa",
        "double_fibres": 24,
        "matching_potential": "fails: every forbidden live fibre has a mate",
    }


RIGHT = (2, 4, 3, 5)
VARIABLE_NAMES = tuple(
    f"{side}{right}{colour}"
    for side in ("u", "v") for right in RIGHT for colour in (B, C)
)
VARIABLES = sp.symbols(" ".join(VARIABLE_NAMES))
VALUE = dict(zip(VARIABLE_NAMES, VARIABLES))


def tensor_pair(left, right):
    return tuple(
        VALUE[f"u{left}{i}"] * VALUE[f"v{right}{j}"]
        + VALUE[f"u{right}{i}"] * VALUE[f"v{left}{j}"]
        for i in (B, C) for j in (B, C)
    )


TARGET_EQUATIONS = tuple(
    entry - int(index == 0)
    for index, entry in enumerate(tensor_pair(2, 4))
) + tuple(
    entry - int(index == 3)
    for index, entry in enumerate(tensor_pair(3, 5))
)
CROSS_PAIRS = ((2, 3), (2, 5), (4, 3), (4, 5))
FANS = (
    ((2, 3), (2, 5)),
    ((2, 3), (4, 3)),
    ((2, 5), (4, 5)),
    ((4, 3), (4, 5)),
)


def is_unit_ideal(equations):
    basis = sp.groebner(
        equations, *VARIABLES, order="grevlex", domain=sp.QQ
    )
    return len(basis.polys) == 1 and basis.polys[0].as_expr() == 1


def audit_shared_zero_fans():
    results = []
    for fan in FANS:
        equations = list(TARGET_EQUATIONS)
        for pair in fan:
            equations.extend(tensor_pair(*pair))
        require(is_unit_ideal(equations),
                f"a shared zero fan became coefficient-feasible: {fan}")

        # Each of the two zero tensors is load-bearing: with only one of
        # them the ideal is proper.  This catches accidental promotion of a
        # single cross row to the two-zero theorem.
        for retained in fan:
            mutation = list(TARGET_EQUATIONS) + list(tensor_pair(*retained))
            require(not is_unit_ideal(mutation),
                    f"a one-zero mutation unexpectedly became unit: {retained}")
        results.append([list(pair) for pair in fan])

    full = list(TARGET_EQUATIONS)
    for pair in CROSS_PAIRS:
        full.extend(tensor_pair(*pair))
    require(is_unit_ideal(full),
            "the complete rectangle coefficient ideal stopped being unit")
    return {
        "variables": len(VARIABLES),
        "target_equations": len(TARGET_EQUATIONS),
        "zero_tensor_equations_per_fan": 8,
        "unit_fans": results,
        "single_zero_tensor_mutations": "all proper",
        "complete_rectangle_ideal": "unit over QQ",
    }


def main():
    pin_dependencies()
    support = audit_even_cycle_support()
    coefficient = audit_shared_zero_fans()
    ledger = {
        "pins": PINS,
        "even_cycle_support": support,
        "shared_zero_fan": coefficient,
        "verdict": (
            "the first complete private-word repair is a genuine even-cycle "
            "support shadow, so uniqueness cannot orient it; its coefficients "
            "are nevertheless impossible by any one of four two-zero fans"
        ),
        "scope": (
            "canonical 19-cell rectangle above a sharp one-bad orbit; the "
            "fan lemma is support-independent, but not every larger one-bad "
            "support is reduced to this rectangle"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"one-bad rectangle ledger changed: {digest}")

    print("N=8 one-bad even-cycle rectangle obstruction: PASS")
    print("support: 19 cells; live fibres: 1 singleton + 24 doubles")
    print("four shared two-zero fan ideals: UNIT over QQ")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
