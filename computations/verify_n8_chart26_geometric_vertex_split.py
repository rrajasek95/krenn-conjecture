#!/usr/bin/env python3
"""Exact audit of the first chart-26 geometric vertex split.

Let x be normalized coordinate cf=(46:00), and let G be the frozen
546-term degree-six compatibility cell.  This checker does two things.

Closed branch, x=0:

* restricts G and all 6,558 degree-four generators;
* restricts every one of the 84,005 completed degree-five cells;
* reduces every newly degree-four-reducible degree-five restriction exactly;
* checks that the surviving restricted degree-four/degree-five leads do not
  reduce G|x=0; and
* freezes the next, squarefree leading monomial.

Open branch, x invertible:

* reconstructs the exact four-corner Bianchi identity;
* checks that its opposite-order rewrite gives literally the same source
  S-polynomial and hence the same reduced G;
* audits the x-adic support of G; and
* divides the distinguished x^2 pivot in the Laurent ring, recording the
  denominator-two cleared identity x^2 (x^-2 G)=G.

This is a branch-local Buchberger audit.  It is not a radical-membership
certificate for the chart target.
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
    "n8_vertex_split_compatibility",
    "verify_n8_chart26_first_degree6_compatibility.py",
)
BIANCHI = load(
    "n8_vertex_split_bianchi",
    "verify_n8_chart26_cross_vertex_bianchi.py",
)
FIRST = COMPAT.FIRST
COMPLETE = COMPAT.COMPLETE
D5 = COMPAT.D5
QQ = Fraction

EXPECTED_LEDGER_SHA256 = (
    "700cad0cb68a80d27c2493e54724fdefc370fe6a8cffc328fa1c7408434e8a79"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def restrict(polynomial, variable):
    return {
        monomial: QQ(coefficient)
        for monomial, coefficient in polynomial.items()
        if variable not in monomial
    }


def fraction_histogram(values):
    return [
        [[value.numerator, value.denominator], count]
        for value, count in sorted(Counter(values).items())
    ]


def reconstruct_compatibility():
    """Return G, its lead, its source S-polynomial, and reduction data."""
    basis = COMPAT.initial_basis()
    schedule = COMPAT.degree6_schedule(basis)
    frozen = None
    for schedule_index, (_lcm, first_index, second_index) in enumerate(
            schedule[:3], 1):
        _computed_lcm, spoly = COMPAT.s_polynomial(
            basis[first_index], basis[second_index]
        )
        remainder, certificate = COMPAT.reduce_polynomial(spoly, basis)
        require(remainder, "a frozen compatibility remainder vanished")
        raw_lead = FIRST.leading_monomial(remainder)
        require(remainder[raw_lead] == 1,
                "a compatibility cell lost its monic normalization")
        remainder, lead = COMPAT.normalize(remainder)
        basis.append({
            "kind": "degree6",
            "label": schedule_index,
            "total_degree": 6,
            "polynomial": remainder,
            "lead": lead,
        })
        if schedule_index == 3:
            frozen = (
                remainder,
                lead,
                spoly,
                certificate,
                first_index,
                second_index,
            )
    require(frozen is not None, "the third compatibility cell was not built")
    return frozen


def add_scaled(target, polynomial, scalar=QQ(1), multiplier=b""):
    for monomial, coefficient in polynomial.items():
        FIRST.add_value(
            target,
            FIRST.multiply(multiplier, monomial),
            scalar * coefficient,
        )


def remove_copies(monomial, variable, count):
    answer = list(monomial)
    for _ in range(count):
        require(variable in answer, "localized pivot lost an x factor")
        answer.remove(variable)
    return bytes(answer)


def audit():
    g, repeated_lead, source_spoly, source_certificate, first_index, second_index = (
        reconstruct_compatibility()
    )
    x = BIANCHI.coordinate(4, 6, 0, 0)
    require(x == 0xcf and D5.COORDINATES[x] == (4, 6, 0, 0),
            "the vertex-split coordinate changed")
    require(len(g) == 546, "the frozen compatibility support changed")
    require(repeated_lead.hex() == "0948cfcfebef",
            "the repeated compatibility lead changed")
    require(Counter(repeated_lead)[x] == 2,
            "the distinguished lead no longer has x exponent two")

    # Closed branch: first restrict G and the original degree-four basis.
    g_closed = restrict(g, x)
    require(len(g_closed) == 288,
            "the closed-branch compatibility support changed")
    require(Counter(map(len, g_closed))
            == Counter({6: 192, 5: 77, 4: 18, 3: 1}),
            "the closed-branch degree histogram changed")
    require(Counter(g_closed.values())
            == Counter({QQ(-1): 144, QQ(1): 144}),
            "the closed-branch coefficients changed")

    originals, original_lead_to_code = FIRST.original_basis()
    code_to_original_lead = {
        code: lead for lead, code in original_lead_to_code.items()
    }
    restricted_originals = {}
    restricted_lead_to_code = {}
    restricted_d4_basis = []
    restricted_d4_term_histogram = Counter()
    for code, polynomial in sorted(originals.items()):
        restricted_polynomial = restrict(polynomial, x)
        require(restricted_polynomial,
                "a degree-four generator vanished on x=0")
        lead = FIRST.leading_monomial(restricted_polynomial)
        require(len(lead) == len(set(lead)) == 4,
                "a restricted degree-four lead lost squarefreeness")
        require(lead not in restricted_lead_to_code,
                "restricted degree-four leading monomials collided")
        restricted_originals[code] = restricted_polynomial
        restricted_lead_to_code[lead] = code
        restricted_d4_basis.append({
            "kind": "restricted_degree4",
            "label": code,
            "total_degree": 4,
            "polynomial": restricted_polynomial,
            "lead": lead,
        })
        restricted_d4_term_histogram[len(restricted_polynomial)] += 1
    require(len(restricted_d4_basis) == 6558,
            "the restricted degree-four census changed")
    require(restricted_d4_term_histogram
            == Counter({105: 5830, 90: 728}),
            "the restricted degree-four term histogram changed")

    closed_after_d4, closed_d4_certificate = COMPAT.reduce_polynomial(
        g_closed, restricted_d4_basis
    )
    require(closed_after_d4 == g_closed and not closed_d4_certificate,
            "G|x=0 became reducible in restricted degree four")

    # A degree-five cell can reduce G|x=0 exactly when its degree-five lead
    # is one of these finitely many monomial divisors.
    target_degree5_divisors = set()
    for monomial in g_closed:
        if len(monomial) >= 5:
            target_degree5_divisors.update(FIRST.divisors(monomial, 5))

    pairs, _by_core, _core_histogram = COMPLETE.build_pairs(
        code_to_original_lead
    )
    raw_restricted_d5_leads = set()
    raw_restricted_d5_term_histogram = Counter()
    restricted_d5_zero_cells = 0
    restricted_d5_surviving_cells = 0
    restricted_d5_d4_column_histogram = Counter()
    target_d5_dividing_leads = []
    for lcm, first_code, second_code in pairs:
        polynomial = COMPLETE.s_polynomial(
            lcm,
            first_code,
            second_code,
            originals,
            code_to_original_lead,
        )
        restricted_polynomial = restrict(polynomial, x)
        require(restricted_polynomial,
                "a completed degree-five cell vanished termwise")
        raw_restricted_d5_term_histogram[len(restricted_polynomial)] += 1
        lead = FIRST.leading_monomial(restricted_polynomial)
        require(len(lead) == len(set(lead)) == 5,
                "a raw restricted degree-five lead lost squarefreeness")
        require(lead not in raw_restricted_d5_leads,
                "raw restricted degree-five leads collided")
        raw_restricted_d5_leads.add(lead)

        degree4_reducible = any(
            divisor in restricted_lead_to_code
            for monomial in restricted_polynomial
            if len(monomial) >= 4
            for divisor in FIRST.divisors(monomial, 4)
        )
        if degree4_reducible:
            remainder, certificate = COMPAT.reduce_polynomial(
                restricted_polynomial, restricted_d4_basis
            )
            require(not remainder,
                    "a changed restricted degree-five cell left a tail")
            restricted_d5_zero_cells += 1
            restricted_d5_d4_column_histogram[len(certificate)] += 1
        else:
            restricted_d5_surviving_cells += 1
            if lead in target_degree5_divisors:
                target_d5_dividing_leads.append(lead)

    require(len(raw_restricted_d5_leads) == len(pairs) == 84005,
            "the restricted degree-five raw census changed")
    require(raw_restricted_d5_term_histogram == Counter({
        180: 72469,
        165: 5688,
        156: 4731,
        150: 681,
        90: 436,
    }), "the raw restricted degree-five term census changed")
    require(restricted_d5_zero_cells == 653,
            "the restricted degree-five zero-cell census changed")
    require(restricted_d5_surviving_cells == 83352,
            "the restricted degree-five survivor census changed")
    require(restricted_d5_d4_column_histogram
            == Counter({1: 436, 2: 217}),
            "the restricted degree-five reduction-column census changed")
    require(not target_d5_dividing_leads,
            "a surviving restricted degree-five lead now reduces G|x=0")

    closed_lead = FIRST.leading_monomial(g_closed)
    require(closed_lead.hex() == "0951acd9e1f5",
            "the closed-branch leading monomial changed")
    require(len(closed_lead) == len(set(closed_lead)) == 6,
            "the closed-branch leading monomial is not squarefree")

    # Open branch: reconstruct the exact local Bianchi packet.  The source
    # S-polynomial is x*eb*H_11 - B'*Rv(0).  Bianchi rewrites the second
    # term by the opposite-order path, but the resulting polynomial is
    # literally the same source polynomial, not a new mate to subtract.
    a = BIANCHI.coordinate(6, 7, 0, 1)
    a_prime = BIANCHI.coordinate(6, 7, 0, 2)
    b = BIANCHI.coordinate(4, 5, 0, 0)
    b_prime = BIANCHI.coordinate(4, 5, 0, 1)
    eb = BIANCHI.coordinate(5, 7, 0, 1)

    r_v_0 = BIANCHI.transport(a_prime, 1, a, 2, originals)
    r_v_1 = BIANCHI.transport(a_prime, 10, a, 11, originals)
    r_q_1 = BIANCHI.transport(b_prime, 1, b, 10, originals)
    r_q_2 = BIANCHI.transport(b_prime, 2, b, 11, originals)

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
            BIANCHI.variable_multiplier(variable),
        )
    require(not bianchi, "the four-corner Bianchi identity changed")

    direct_source = {}
    add_scaled(direct_source, originals[11], multiplier=bytes(sorted((x, eb))))
    add_scaled(
        direct_source,
        r_v_0,
        -1,
        BIANCHI.variable_multiplier(b_prime),
    )
    require(direct_source == source_spoly,
            "the compatibility source decomposition changed")

    opposite_source = {}
    add_scaled(
        opposite_source,
        originals[11],
        multiplier=bytes(sorted((x, eb))),
    )
    add_scaled(
        opposite_source,
        r_v_1,
        -1,
        BIANCHI.variable_multiplier(b),
    )
    add_scaled(
        opposite_source,
        r_q_1,
        -1,
        BIANCHI.variable_multiplier(a_prime),
    )
    add_scaled(
        opposite_source,
        r_q_2,
        1,
        BIANCHI.variable_multiplier(a),
    )
    require(opposite_source == direct_source,
            "the opposite-order Bianchi mate is not the same source cell")

    x_exponent_histogram = Counter(monomial.count(x) for monomial in g)
    require(x_exponent_histogram == Counter({0: 288, 1: 228, 2: 30}),
            "the compatibility x-adic support changed")
    require(COMPAT.common_monomial(g) == b"",
            "the compatibility cell gained a polynomial common factor")

    localized_pivot = remove_copies(repeated_lead, x, 2)
    require(localized_pivot.hex() == "0948ebef",
            "the Laurent pivot changed")
    require(len(localized_pivot) == len(set(localized_pivot)) == 4,
            "the Laurent pivot is not squarefree")
    laurent_exponent_histogram = Counter(
        monomial.count(x) - 2 for monomial in g
    )
    require(laurent_exponent_histogram
            == Counter({-2: 288, -1: 228, 0: 30}),
            "the denominator-two Laurent support changed")
    laurent_record = []
    for monomial, coefficient in sorted(g.items()):
        exponent = monomial.count(x) - 2
        x_free = bytes(value for value in monomial if value != x)
        laurent_record.append([
            exponent,
            x_free.hex(),
            coefficient.numerator,
            coefficient.denominator,
        ])

    ledger = {
        "split_coordinate_id": f"{x:02x}",
        "split_coordinate": list(D5.COORDINATES[x]),
        "compatibility_terms": len(g),
        "compatibility_lead": repeated_lead.hex(),
        "compatibility_x_exponent_histogram": dict(sorted(
            x_exponent_histogram.items()
        )),
        "compatibility_common_monomial": COMPAT.common_monomial(g).hex(),
        "closed_terms": len(g_closed),
        "closed_degree_histogram": dict(sorted(
            Counter(map(len, g_closed)).items()
        )),
        "closed_coefficient_histogram": fraction_histogram(g_closed.values()),
        "restricted_degree4_cells": len(restricted_d4_basis),
        "restricted_degree4_term_histogram": dict(sorted(
            restricted_d4_term_histogram.items()
        )),
        "closed_degree4_reduction_columns": len(closed_d4_certificate),
        "raw_restricted_degree5_cells": len(raw_restricted_d5_leads),
        "raw_restricted_degree5_term_histogram": dict(sorted(
            raw_restricted_d5_term_histogram.items()
        )),
        "raw_restricted_degree5_distinct_squarefree_leads": len(
            raw_restricted_d5_leads
        ),
        "restricted_degree5_zero_cells": restricted_d5_zero_cells,
        "restricted_degree5_d4_column_histogram": dict(sorted(
            restricted_d5_d4_column_histogram.items()
        )),
        "restricted_degree5_d4_columns_total": sum(
            count * columns
            for columns, count in restricted_d5_d4_column_histogram.items()
        ),
        "restricted_degree5_surviving_cells": restricted_d5_surviving_cells,
        "closed_degree5_dividing_leads": len(target_d5_dividing_leads),
        "closed_total_reduction_columns": 0,
        "closed_lead": closed_lead.hex(),
        "closed_lead_squarefree": True,
        "source_pair_indices": [first_index, second_index],
        "source_reduction_columns": len(source_certificate),
        "bianchi_difference_terms": len(bianchi),
        "opposite_order_source_equals_direct_source": True,
        "opposite_order_reduced_cell_equals_g": True,
        "laurent_divisor_power": 2,
        "laurent_pivot": localized_pivot.hex(),
        "laurent_pivot_squarefree": True,
        "laurent_x_exponent_histogram": dict(sorted(
            laurent_exponent_histogram.items()
        )),
        "laurent_support_sha256": sha256(json.dumps(
            laurent_record, separators=(",", ":")
        ).encode()).hexdigest(),
        "denominator_clearing_identity": "x^2*(x^-2*G)=G",
        "conclusion": (
            "x=0 exposes a squarefree unreduced lead through degree five; "
            "x!=0 makes the repeated pivot squarefree after Laurent "
            "division by x^2, while Bianchi supplies no new polynomial mate"
        ),
        "scope_guard": (
            "this audits the first geometric split cell only; it proves "
            "neither branchwise target radical membership nor termination"
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
                "the frozen geometric vertex-split ledger changed")
    print(
        "n=8 chart26 geometric vertex split: PASS; "
        "closed lead=0951acd9e1f5 squarefree, "
        "open Laurent pivot=0948ebef squarefree"
    )
    print(json.dumps(ledger, sort_keys=True))
    print("sha256:", digest)


if __name__ == "__main__":
    main()
