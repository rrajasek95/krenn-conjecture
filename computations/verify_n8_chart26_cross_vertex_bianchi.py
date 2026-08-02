#!/usr/bin/env python3
"""Verify the cross-vertex transport square and its chart-26 consequence.

The universal identity is a four-corner Koszul commutator.  This checker
specializes it to color changes at vertices 7 and 5, verifies the two
direct-double diagonals, reconstructs the provisional degree-six cell, and
scans the complete degree-five Buchberger layer.  No degree-five lead
divides the repeated degree-six lead, so the Bianchi identity cancels that
lead only between opposite-order compositions; it cannot reduce either
composition individually.
"""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


COMPAT = load(
    "n8_degree6_compatibility",
    "verify_n8_chart26_first_degree6_compatibility.py",
)
COMPLETE = load(
    "n8_complete_degree5",
    "verify_n8_chart26_complete_degree5_buchberger.py",
)
FIRST = COMPAT.FIRST
D5 = COMPAT.D5
QQ = Fraction

EXPECTED_LEDGER_SHA256 = (
    "19252751b0b463f3f9055156d36996ab34781b094fa21ef07ca99f8a5c07687f"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def add_scaled(target, polynomial, scalar=QQ(1), multiplier=b""):
    for row, coefficient in polynomial.items():
        FIRST.add_value(
            target, FIRST.multiply(multiplier, row), scalar * coefficient
        )


def coordinate(left, right, left_colour, right_colour):
    return D5.COORDINATE_ID[(left, right, left_colour, right_colour)]


def variable_multiplier(variable):
    # A normalized support coordinate is the homogenizing variable t.  Its
    # exponent is implicit in this fixed-total-degree representation.
    return bytes((variable,)) if D5.IS_OFF_SUPPORT[variable] else b""


def multiplied_generator(variable, code, originals):
    answer = {}
    add_scaled(
        answer,
        originals[code],
        multiplier=variable_multiplier(variable),
    )
    return answer


def transport(left_variable, left_code, right_variable, right_code,
              originals):
    answer = multiplied_generator(left_variable, left_code, originals)
    add_scaled(
        answer,
        multiplied_generator(right_variable, right_code, originals),
        -1,
    )
    return answer


def normalized_cell(polynomial, originals, original_leads):
    remainder, certificate = FIRST.reduce_by_original(
        polynomial, originals, original_leads
    )
    require(remainder, "a one-end transport unexpectedly reduced to zero")
    lead = FIRST.leading_monomial(remainder)
    coefficient = remainder[lead]
    return (
        {row: QQ(value) / coefficient for row, value in remainder.items()},
        lead,
        certificate,
    )


def provisional_third_cell():
    basis = COMPAT.initial_basis()
    schedule = COMPAT.degree6_schedule(basis)
    accepted = []
    for schedule_index, (_lcm, first_index, second_index) in enumerate(
            schedule[:3], 1):
        _computed_lcm, spoly = COMPAT.s_polynomial(
            basis[first_index], basis[second_index]
        )
        remainder, _certificate = COMPAT.reduce_polynomial(spoly, basis)
        require(remainder, "a frozen degree-six prefix cell vanished")
        remainder, lead = COMPAT.normalize(remainder)
        accepted.append((remainder, lead))
        if schedule_index < 3:
            basis.append({
                "kind": "degree6",
                "label": schedule_index,
                "total_degree": 6,
                "polynomial": remainder,
                "lead": lead,
            })
    return accepted[2]


def audit():
    originals, original_leads = FIRST.original_basis()

    # Write H_{ij} with i in {1,2} the color at vertex 7 and j in
    # {0,1} the color at vertex 5.  The repository word codes are
    # H_10=1, H_20=2, H_11=10, H_21=11.
    require(D5.decode_word(1) == (0, 0, 0, 0, 0, 0, 0, 1),
            "H_10 word changed")
    require(D5.decode_word(2) == (0, 0, 0, 0, 0, 0, 0, 2),
            "H_20 word changed")
    require(D5.decode_word(10) == (0, 0, 0, 0, 0, 1, 0, 1),
            "H_11 word changed")
    require(D5.decode_word(11) == (0, 0, 0, 0, 0, 1, 0, 2),
            "H_21 word changed")

    a = coordinate(6, 7, 0, 1)       # f4
    a_prime = coordinate(6, 7, 0, 2) # f5
    b = coordinate(4, 5, 0, 0)       # c6
    b_prime = coordinate(4, 5, 0, 1) # c7

    r_v_0 = transport(a_prime, 1, a, 2, originals)
    r_v_1 = transport(a_prime, 10, a, 11, originals)
    r_q_1 = transport(b_prime, 1, b, 10, originals)
    r_q_2 = transport(b_prime, 2, b, 11, originals)

    # B'R_v(0)-B R_v(1)-A'R_q(1)+A R_q(2)=0.
    bianchi = {}
    for variable, polynomial, sign in (
        (b_prime, r_v_0, 1),
        (b, r_v_1, -1),
        (a_prime, r_q_1, -1),
        (a, r_q_2, 1),
    ):
        add_scaled(
            bianchi,
            polynomial,
            sign,
            variable_multiplier(variable),
        )
    require(not bianchi, "the cross-vertex Bianchi square is not exact")

    local_cells = {}
    for label, polynomial in (
        ("Rv0", r_v_0),
        ("Rv1", r_v_1),
        ("Rq1", r_q_1),
        ("Rq2", r_q_2),
    ):
        reduced, lead, certificate = normalized_cell(
            polynomial, originals, original_leads
        )
        require(not certificate and len(reduced) == 180,
                "a local star cell ceased to be originally reduced")
        local_cells[label] = (reduced, lead)
    require(
        {label: lead.hex() for label, (_polynomial, lead)
         in local_cells.items()} == {
            "Rv0": "0948cfebf5",
            "Rv1": "0948cfeff4",
            "Rq1": "0948c6d9e4",
            "Rq2": "0948c6cfef",
        },
        "local opposite-order leading terms changed",
    )

    # The two diagonals use the color coordinate of the opposite corner.
    eb = coordinate(5, 7, 0, 1)
    ec = coordinate(5, 7, 0, 2)
    ee = coordinate(5, 7, 1, 1)  # a chart-support coordinate, hence t
    ef = coordinate(5, 7, 1, 2)
    direct_diagonals = (
        transport(ef, 1, eb, 11, originals),
        transport(ee, 2, ec, 10, originals),
    )
    diagonal_records = []
    for polynomial in direct_diagonals:
        remainder, certificate = FIRST.reduce_by_original(
            polynomial, originals, original_leads
        )
        require(not remainder and len(certificate) == 2,
                "a direct-double diagonal stopped reducing to zero")
        diagonal_records.append([len(polynomial), len(certificate)])
    require(diagonal_records == [[180, 2], [180, 2]],
            "direct-double diagonal census changed")

    third, repeated_lead = provisional_third_cell()
    require(len(third) == 546, "provisional degree-six support changed")
    require(repeated_lead.hex() == "0948cfcfebef",
            "provisional repeated leading monomial changed")
    require(Counter(repeated_lead)[coordinate(4, 6, 0, 0)] == 2,
            "the repeated chart coordinate changed")

    # The complete local Bianchi square is not a reducer for the third cell.
    local_basis = COMPAT.initial_basis()
    for label in ("Rv1", "Rq1", "Rq2"):
        polynomial, lead = local_cells[label]
        local_basis.append({
            "kind": "opposite_star",
            "label": label,
            "total_degree": 5,
            "polynomial": polynomial,
            "lead": lead,
        })
    local_remainder, local_certificate = COMPAT.reduce_polynomial(
        third, local_basis
    )
    require(local_remainder == third and not local_certificate,
            "the opposite-order square unexpectedly reduced the d6 cell")

    # Scan the complete degree-five layer, not only the local square.
    code_to_lead = {code: lead for lead, code in original_leads.items()}
    pairs, _by_core, _core_histogram = COMPLETE.build_pairs(code_to_lead)
    all_leads = set()
    dividing_leads = []
    for lcm, first_code, second_code in pairs:
        polynomial = COMPLETE.s_polynomial(
            lcm, first_code, second_code, originals, code_to_lead
        )
        lead = FIRST.leading_monomial(polynomial)
        require(len(lead) == len(set(lead)) == 5,
                "a complete degree-five lead lost squarefreeness")
        all_leads.add(lead)
        if Counter(lead) <= Counter(repeated_lead):
            dividing_leads.append(lead)
    require(len(pairs) == len(all_leads) == 84005,
            "complete degree-five lead census changed")
    require(not dividing_leads,
            "a complete degree-five lead now divides the repeated d6 lead")
    lead_digest = sha256(b"".join(sorted(all_leads))).hexdigest()
    require(lead_digest
            == "69e806955f6b9e33de683cb98e36d89ccb0cda82f311b7ef88006a803b831ed4",
            "complete degree-five lead digest changed")

    original_divisors = [
        lead.hex() for lead in original_leads
        if Counter(lead) <= Counter(repeated_lead)
    ]
    require(not original_divisors,
            "an original lead divides the repeated d6 lead")

    ledger = {
        "chart_words": [1, 2, 10, 11],
        "cross_vertex_bianchi_remainder_terms": len(bianchi),
        "local_star_leads": {
            label: lead.hex()
            for label, (_polynomial, lead) in sorted(local_cells.items())
        },
        "local_star_terms_each": 180,
        "direct_double_diagonals": diagonal_records,
        "provisional_degree6_terms": len(third),
        "provisional_degree6_lead": repeated_lead.hex(),
        "local_opposite_order_reduction_columns": len(local_certificate),
        "complete_degree5_cells": len(pairs),
        "complete_degree5_distinct_leads": len(all_leads),
        "complete_degree5_lead_sha256": lead_digest,
        "degree5_leads_dividing_repeated_degree6_lead": len(dividing_leads),
        "original_leads_dividing_repeated_degree6_lead": len(original_divisors),
        "conclusion": (
            "the Bianchi difference is zero, but no complete degree5 lead "
            "reduces the minimal repeated-coordinate degree6 lead"
        ),
        "scope_guard": (
            "this certifies the first non-squarefree initial generator in "
            "chart 26; it does not complete higher Buchberger layers"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    return ledger, digest


def main():
    ledger, digest = audit()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                "frozen cross-vertex Bianchi ledger changed")
    print(
        "n=8 chart26 cross-vertex Bianchi: PASS; "
        "d5 cells=84005, d5 divisors=0, repeated d6 lead survives"
    )
    print(json.dumps(ledger, sort_keys=True))
    print("sha256:", digest)


if __name__ == "__main__":
    main()
