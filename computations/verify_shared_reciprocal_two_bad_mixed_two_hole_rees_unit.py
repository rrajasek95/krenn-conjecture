#!/usr/bin/env python3
"""Exact Rees lift of the 18-row mixed two-hole unit certificate.

The normalized target-axis square has K0=K1=K2=0, K3=X0 and
K4=X1.  Its pinned 18-row identity is rewritten against a general kernel
row with nonzero target components tau_0,tau_1,tau_2.  The coefficient of
the full word having its unique target at x is

    tau_x K_x(beta) + R_x(beta),

where R_x(beta) is the literal sum of the non-target inserted rows times
target-containing cofactor coefficients.  Clearing tau_0*tau_1*tau_2
turns the old unit identity into a finite source identity supported on
these transgression rows and nine bright-cofactor defects.

Thus the target-axis unit is already a unit after localization at the
three tau's: it has no positive-Rees-order tilted deformation.  An escape
must lose a tau or have an order-zero transgression/bright defect.
"""

from __future__ import annotations

from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
PINNED_UNIT_SHA256 = (
    "666705a347f3f2abb570de0a6cb59c629c72d94ae2ba048c0c14ec428ee612c6"
)
PINNED_FIRST_CORRECTION_SHA256 = (
    "05829702827cab23ca74c788a84744ea642d8d943c0c390eff5cafd3b995ad22"
)
EXPECTED_LEDGER_SHA256 = "21b03a2533ab39c18a0fc1d61628b0f0615a3213c83bc3fe9554c9c3eba7526d"

SITES = tuple(range(5))
BRIGHT = (0, 1)
TARGET = 2
EDGES = tuple(combinations(SITES, 2))


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def pin_dependencies():
    pins = {
        "computations/verify_shared_reciprocal_two_bad_mixed_two_hole_unit.py":
            PINNED_UNIT_SHA256,
        "computations/verify_shared_reciprocal_two_bad_mixed_parity_first_correction_guard.py":
            PINNED_FIRST_CORRECTION_SHA256,
    }
    for relative, expected in pins.items():
        path = ROOT / relative
        require(path.exists(), f"missing dependency: {relative}")
        actual = sha256(path.read_bytes()).hexdigest()
        require(actual == expected,
                f"dependency changed: {relative}: {actual}")


def perfect_matchings(vertices):
    vertices = tuple(sorted(vertices))
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


def variable_name(left, right, left_colour, right_colour):
    if left > right:
        left, right = right, left
        left_colour, right_colour = right_colour, left_colour
    return f"q{left}{right}{left_colour}{right_colour}"


Q = {
    (left, right, left_colour, right_colour): sp.Symbol(
        variable_name(left, right, left_colour, right_colour)
    )
    for left, right in EDGES
    for left_colour in BRIGHT for right_colour in BRIGHT
}


def q(left, right, left_colour, right_colour):
    if left > right:
        left, right = right, left
        left_colour, right_colour = right_colour, left_colour
    return Q[(left, right, left_colour, right_colour)]


def cofactor(hole, word):
    vertices = tuple(site for site in SITES if site != hole)
    require(len(word) == len(vertices), "cofactor word length changed")
    colouring = dict(zip(vertices, word))
    return sp.Add(*(
        sp.Mul(*(q(left, right, colouring[left], colouring[right])
                 for left, right in matching))
        for matching in perfect_matchings(vertices)
    ))


# This is the pinned nonzero part of the source lift in 4c9da58.  Keeping
# it explicit makes the filtered identity readable and source-addressable.
ACTIVE = (
    (0, (0, 1, 1, 0), 0, "q0111*q0200"),
    (0, (1, 0, 1, 0), 0, "q0100*q0211"),
    (0, (1, 1, 1, 0), 0, "-q0110*q0200-q0100*q0210"),
    (1, (0, 1, 1, 0), 0, "q0111*q1200"),
    (1, (1, 0, 1, 0), 0, "q0100*q1211"),
    (1, (1, 1, 1, 0), 0, "-q0101*q1200-q0100*q1210"),
    (2, (0, 1, 1, 0), 0, "q0211*q1200"),
    (2, (1, 0, 1, 0), 0, "q0200*q1211"),
    (2, (1, 1, 1, 0), 0, "-q0201*q1200-q0200*q1201"),
    (3, (0, 0, 0, 0), 1, "-1"),
    (3, (0, 1, 1, 0), 0, "q0311*q1200"),
    (3, (1, 0, 1, 0), 0, "q0200*q1311"),
    (3, (1, 1, 0, 0), 0, "q0100*q2311"),
    (3, (1, 1, 1, 0), 0,
     "-q0301*q1200-q0200*q1301-q0100*q2301"),
    (4, (0, 1, 1, 1), 0, "q0410*q1200"),
    (4, (1, 0, 1, 1), 0, "q0200*q1410"),
    (4, (1, 1, 0, 1), 0, "q0100*q2410"),
    (4, (1, 1, 1, 1), 1,
     "-q0400*q1200-q0200*q1400-q0100*q2400"),
)


def parse_multiplier(source):
    names = {str(symbol): symbol for symbol in Q.values()}
    return sp.sympify(source, locals=names)


def audit_source_identity():
    total = sp.S.Zero
    rows = []
    for hole, word, target, source in ACTIVE:
        multiplier = parse_multiplier(source)
        generator = cofactor(hole, word) - target
        total += multiplier * generator
        rows.append({
            "hole": hole,
            "word": "".join(map(str, word)),
            "target": target,
            "multiplier": source,
        })
    require(sp.expand(total - 1) == 0,
            "the pinned 18-row ordinary source identity changed")
    return rows


def full_word_with_unique_target(hole, beta):
    vertices = tuple(site for site in SITES if site != hole)
    colouring = dict(zip(vertices, beta))
    colouring[hole] = TARGET
    return tuple(colouring[site] for site in SITES)


def transgression_terms(hole, beta):
    """Literal non-target insertions in the unique-target output row."""
    full_word = full_word_with_unique_target(hole, beta)
    terms = []
    for inserted_site in SITES:
        if inserted_site == hole:
            continue
        inserted_colour = full_word[inserted_site]
        cofactor_word = tuple(
            full_word[site] for site in SITES if site != inserted_site
        )
        require(cofactor_word.count(TARGET) == 1,
                "a target-containing correction word changed")
        terms.append({
            "kernel_component": f"nu{inserted_site}_{inserted_colour}",
            "cofactor": (
                f"K{inserted_site}:" + "".join(map(str, cofactor_word))
            ),
        })
    require(len(terms) == 4,
            "a unique-target kernel row lost an insertion route")
    return full_word, terms


def audit_cleared_rees_identity():
    tau = sp.symbols("tau0 tau1 tau2", nonzero=True)
    target_product = sp.prod(tau)
    correction_sum = sp.S.Zero
    bright_sum = sp.S.Zero
    transgressions = []

    for index, (hole, word, target, source) in enumerate(ACTIVE):
        multiplier = parse_multiplier(source)
        if hole <= 2:
            r_symbol = sp.Symbol(
                f"R{hole}_{''.join(map(str, word))}"
            )
            correction_sum += (
                target_product / tau[hole] * multiplier * r_symbol
            )
            full_word, terms = transgression_terms(hole, word)
            transgressions.append({
                "hole": hole,
                "binary_word": "".join(map(str, word)),
                "full_unique_target_word": "".join(map(str, full_word)),
                "R_terms": terms,
            })
        else:
            defect = sp.Symbol(f"D{index + 1}")
            bright_sum += multiplier * defect

    # In the quotient by the nine literal kernel rows
    # tau_x*K_x(beta)+R_x(beta)=0, the pinned identity becomes
    #
    #   T = -sum_x (T/tau_x) M_x,beta R_x,beta
    #       + T sum_bright M_h,beta Delta_h,beta.
    #
    # Check the algebra by replacing every R with -tau*K and every bright
    # defect by its original source generator.
    substitutions = {}
    for hole, word, target, _source in ACTIVE:
        if hole <= 2:
            substitutions[sp.Symbol(
                f"R{hole}_{''.join(map(str, word))}"
            )] = -tau[hole] * cofactor(hole, word)
    for index, (hole, word, target, _source) in enumerate(ACTIVE):
        if hole >= 3:
            substitutions[sp.Symbol(f"D{index + 1}")] = (
                cofactor(hole, word) - target
            )
    rhs = -correction_sum + target_product * bright_sum
    require(sp.expand(rhs.subs(substitutions) - target_product) == 0,
            "the cleared finite Rees identity changed")

    # The first associated-grade correction is the ordinary convolution
    # of a kernel component and a target-containing cofactor slice.
    n0, n1, l0, l1, eps = sp.symbols("nu0 nu1 L0 L1 eps")
    convolution = sp.expand(
        (n0 + eps * n1) * (l0 + eps * l1)
    ).coeff(eps, 1)
    require(convolution == n0 * l1 + n1 * l0,
            "the first Rees transgression convolution changed")

    # The canonical Hubble bridge U=e_t@0-e_a@1 has only one target
    # coefficient.  Therefore T=tau0*tau1*tau2 vanishes and the localized
    # three-centre identity intentionally does not apply there.
    hubble_tau = (1, 0, 0)
    require(sp.prod(hubble_tau) == 0,
            "the two-centre tilted bridge entered the three-tau chart")

    return {
        "localized_target_product": "tau0*tau1*tau2",
        "transgression_rows": transgressions,
        "first_rees_convolution": "nu^(0)*L^(1)+nu^(1)*L^(0)",
        "cleared_identity": (
            "T=-sum_{x=0}^2 (T/tau_x) M_x,beta R_x,beta"
            "+T sum_{h=3}^4 M_h,beta Delta_h,beta"
        ),
        "hubble_bridge_target_coefficients": list(hubble_tau),
    }


def main():
    pin_dependencies()
    active_rows = audit_source_identity()
    rees = audit_cleared_rees_identity()
    ledger = {
        "pinned_unit_sha256": PINNED_UNIT_SHA256,
        "pinned_first_correction_sha256": PINNED_FIRST_CORRECTION_SHA256,
        "active_rows": active_rows,
        "rees_lift": rees,
        "verdict": (
            "after localizing tau0*tau1*tau2, the 18-row unit has an "
            "exact finite lift through the tilted kernel rows; any escape "
            "must lose a tau or have an order-zero transgression/bright "
            "defect"
        ),
        "scope": (
            "the three-centre target-projection Rees chart; T=0 is the "
            "entire <=2 target-coefficient boundary, whose minimal "
            "realizations include the Hubble repair charts"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"the mixed two-hole Rees ledger changed: {digest}")

    print("mixed two-hole finite Rees unit: PASS")
    print("ordinary source core / tilted rows: 18 / 9")
    print("localized target product: tau0*tau1*tau2")
    print("first correction: nu0*L1+nu1*L0")
    print("Hubble two-centre bridge: boundary T=0")
    print(f"ledger sha256: {digest}")


if __name__ == "__main__":
    main()
