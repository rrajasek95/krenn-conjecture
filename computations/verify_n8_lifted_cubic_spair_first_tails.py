#!/usr/bin/env python3
"""Exact first-tail audit for the nine cubic n=8 tangent generators.

The 39 quadratic second-lift obstructions have nine cubic S-polynomials in
their reduced tangent Groebner basis.  Each cubic has a two-term lift to the
literal mixed ideal.  This checker eliminates the 196 normal directions to
one further order and verifies that the first post-cancellation tail of all
36 cubic-cubic critical pairs reduces to zero through the 39 quadrics and
nine cubics.  It also follows the first pair through one additional order.

This is a bounded filtered-standard-basis certificate.  It does not audit
quadratic-quadratic or quadratic-cubic pairs, nor all higher tails.
"""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import json

import analyze_n8_counterexample_local_standard_basis as LOCAL


CUBIC = LOCAL.CUBIC
SOURCE = LOCAL.SOURCE
FOURTH = LOCAL.FOURTH
QQ = Fraction

EXPECTED_LEDGER_SHA256 = (
    "8db7c798d7bc0ba6ef2d0423d28757e53d2f52f3f38f8a1c1ac6acbe593ba6b1"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def add(target, source, scale=QQ(1)):
    CUBIC.add_scaled(target, source, scale)


def multiply(left, right):
    return CUBIC.multiply_polynomials(left, right)


def monomial_polynomial(monomial, coefficient=QQ(1)):
    return {tuple(monomial): coefficient}


def multiset_lcm(left, right):
    left_counts = Counter(left)
    right_counts = Counter(right)
    answer = []
    for variable in sorted(set(left_counts) | set(right_counts)):
        answer.extend(
            [variable] * max(left_counts[variable], right_counts[variable])
        )
    return tuple(answer)


def quotient_monomial(divisor, dividend):
    answer = list(dividend)
    for variable in divisor:
        answer.remove(variable)
    return tuple(answer)


class NormalObstructionSeries:
    """Normal-coordinate elimination of the 39 literal obstruction lifts."""

    def __init__(self):
        self.reducer = LOCAL.LocalReducer()
        self.items = list(self.reducer.data["obstruction_pivots"].items())
        self.pivot_to_number = {
            pivot: number
            for number, (pivot, _value) in enumerate(self.items, 1)
        }
        self.states = {}

    def number_with_leading_form(self, form):
        matches = [
            number
            for number, (_pivot, (row, _representative))
            in enumerate(self.items, 1)
            if row == form
        ]
        require(len(matches) == 1, f"obstruction-form match changed: {matches}")
        return matches[0]

    def _state(self, number):
        if number not in self.states:
            pivot, (row, representative) = self.items[number - 1]
            functional = SOURCE.literal_cokernel_lift(
                representative, self.reducer.data
            )
            self.states[number] = {
                "pivot": pivot,
                "row": row,
                "functional": functional,
                "corrections": [],
                "parts": {},
                "maximum_degree": 1,
            }
        return self.states[number]

    def part(self, number, requested_degree):
        state = self._state(number)
        for degree in range(state["maximum_degree"] + 1,
                            requested_degree + 1):
            residual = (
                SOURCE.represented_literal_hasse(state["functional"], degree)
                if degree <= 4 else {}
            )
            for multiplier, jacobian_functional in state["corrections"]:
                multiplier_degree = len(next(iter(multiplier)))
                equation_degree = degree - multiplier_degree
                if not 0 <= equation_degree <= 4:
                    continue
                add(
                    residual,
                    multiply(
                        multiplier,
                        SOURCE.represented_literal_hasse(
                            jacobian_functional, equation_degree
                        ),
                    ),
                    -1,
                )
            quotients, remainder, _steps = (
                SOURCE.fast_divide_by_echelon_linear_forms(
                    residual, self.reducer.jacobian_pivots
                )
            )
            replay = CUBIC.reconstruct_division(
                quotients, self.reducer.jacobian_pivots
            )
            add(replay, remainder)
            require(replay == residual,
                    f"normal-series replay failed at Q{number}, degree {degree}")
            tangent = self.reducer.tangent_polynomial(remainder)
            state["parts"][degree] = tangent
            for pivot, multiplier in quotients.items():
                state["corrections"].append(
                    (multiplier, self.reducer.jacobian_functional(pivot))
                )
            state["maximum_degree"] = degree

        require(
            state["parts"][2] == state["row"],
            f"Q{number} lost its quadratic tangent leading form",
        )
        return state["parts"].get(requested_degree, {})


def audit():
    series = NormalObstructionSeries()

    # Singular's input numbering for the sparse quadrics used in the compact
    # identities below.  Resolve by exact leading form, not dict order.
    desired_quadrics = {
        1: {(12, 25): QQ(1), (18, 46): QQ(-1)},
        5: {(12, 46): QQ(1)},
        6: {(13, 25): QQ(1), (19, 46): QQ(-1)},
        10: {(13, 46): QQ(1)},
        11: {(14, 25): QQ(1), (20, 46): QQ(-1)},
        14: {(14, 46): QQ(1)},
        24: {(18, 25): QQ(1)},
        28: {(19, 25): QQ(1)},
        32: {(20, 25): QQ(1)},
    }
    quadratic_number = {
        name: series.number_with_leading_form(form)
        for name, form in desired_quadrics.items()
    }

    # A signed variable is followed by a quadratic name.  Thus, for example,
    # C40=-z46*Q11+z25*Q14.  Here z46=a, z25=e and z18,z19,z20=r,s,t.
    definitions = {
        40: ((-46, 11), (25, 14)),
        41: ((-46, 6), (25, 10)),
        42: ((-46, 1), (25, 5)),
        43: ((-20, 11), (14, 32)),
        44: ((-20, 6), (13, 32)),
        45: ((-20, 1), (12, 32)),
        46: ((-19, 6), (13, 28)),
        47: ((-19, 1), (12, 28)),
        48: ((-18, 1), (12, 24)),
    }
    cubic_leads = {
        40: (20, 46, 46),
        41: (19, 46, 46),
        42: (18, 46, 46),
        43: (20, 20, 46),
        44: (19, 20, 46),
        45: (18, 20, 46),
        46: (19, 19, 46),
        47: (18, 19, 46),
        48: (18, 18, 46),
    }

    def cubic_part(number, degree):
        answer = {}
        for signed_variable, quadratic_name in definitions[number]:
            variable = abs(signed_variable)
            term = multiply(
                monomial_polynomial((variable,)),
                series.part(quadratic_number[quadratic_name], degree - 1),
            )
            add(answer, term, -1 if signed_variable < 0 else 1)
        return answer

    for number, expected in cubic_leads.items():
        require(
            cubic_part(number, 3) == {expected: QQ(1)},
            f"compact lift C{number} lost its cubic leading monomial",
        )

    def reduce_by_48(polynomial):
        quadratic_quotients, remainder, quadratic_steps = (
            FOURTH.reduce_by_quadratic_obstructions(
                polynomial, series.reducer.simple_obstructions
            )
        )
        work = dict(remainder)
        cubic_quotients = {}
        final_remainder = {}
        while work:
            monomial = min(work)
            coefficient = work.pop(monomial)
            selected = None
            for number, leading_monomial in cubic_leads.items():
                multiplier = FOURTH.divides(leading_monomial, monomial)
                if multiplier is not None:
                    selected = number, multiplier
                    break
            if selected is None:
                final_remainder[monomial] = coefficient
                continue
            value = cubic_quotients.get(selected, QQ(0)) + coefficient
            if value:
                cubic_quotients[selected] = value
            else:
                cubic_quotients.pop(selected, None)

        replay = FOURTH.reconstruct_obstruction_division(
            quadratic_quotients, series.reducer.simple_obstructions
        )
        for (number, multiplier), coefficient in cubic_quotients.items():
            add(
                replay,
                monomial_polynomial(
                    tuple(sorted(multiplier + cubic_leads[number])), coefficient
                ),
            )
        add(replay, final_remainder)
        require(replay == polynomial, "48-generator tangent division did not replay")
        return (
            quadratic_quotients,
            cubic_quotients,
            final_remainder,
            quadratic_steps,
        )

    pair_rows = []
    pair_reductions = {}
    for left in sorted(cubic_leads):
        for right in sorted(cubic_leads):
            if right <= left:
                continue
            common = multiset_lcm(cubic_leads[left], cubic_leads[right])
            left_multiplier = quotient_monomial(cubic_leads[left], common)
            right_multiplier = quotient_monomial(cubic_leads[right], common)
            tail = multiply(
                monomial_polynomial(left_multiplier), cubic_part(left, 4)
            )
            add(
                tail,
                multiply(
                    monomial_polynomial(right_multiplier),
                    cubic_part(right, 4),
                ),
                -1,
            )
            q_quotients, c_quotients, remainder, q_steps = reduce_by_48(tail)
            require(not remainder,
                    f"first lifted tail of C{left},C{right} did not close")
            pair_reductions[left, right] = (
                common, left_multiplier, right_multiplier,
                q_quotients, c_quotients,
            )
            pair_rows.append({
                "pair": [left, right],
                "lcm_degree": len(common),
                "tail_degree": len(common) + 1,
                "tail_terms": len(tail),
                "quadratic_quotients": len(q_quotients),
                "cubic_quotients": len(c_quotients),
                "quadratic_steps": q_steps,
            })

    require(len(pair_rows) == 36, "cubic-cubic pair count changed")

    # Follow C40,C41 one order beyond its certified first-tail reduction.
    common, left_multiplier, right_multiplier, q5, c5 = (
        pair_reductions[40, 41]
    )
    next_tail = multiply(
        monomial_polynomial(left_multiplier), cubic_part(40, 5)
    )
    add(
        next_tail,
        multiply(monomial_polynomial(right_multiplier), cubic_part(41, 5)),
        -1,
    )
    for (pivot, multiplier), coefficient in q5.items():
        quadratic_number_at_pivot = series.pivot_to_number[pivot]
        add(
            next_tail,
            multiply(
                monomial_polynomial(multiplier, coefficient),
                series.part(quadratic_number_at_pivot, 3),
            ),
            -1,
        )
    for (number, multiplier), coefficient in c5.items():
        add(
            next_tail,
            multiply(
                monomial_polynomial(multiplier, coefficient),
                cubic_part(number, 4),
            ),
            -1,
        )
    q6, c6, remainder6, q6_steps = reduce_by_48(next_tail)
    require(not remainder6, "C40,C41 lifted degree-six tail did not close")

    lcm_counts = Counter(row["lcm_degree"] for row in pair_rows)
    ledger = {
        "literal_quadratic_lifts": 39,
        "compact_cubic_lifts": len(definitions),
        "compact_cubic_lift_terms": sum(map(len, definitions.values())),
        "cubic_cubic_pairs": len(pair_rows),
        "pair_lcm_degree_counts": {
            str(degree): count for degree, count in sorted(lcm_counts.items())
        },
        "first_tail_total_terms": sum(row["tail_terms"] for row in pair_rows),
        "first_tail_quadratic_quotients": sum(
            row["quadratic_quotients"] for row in pair_rows
        ),
        "first_tail_cubic_quotients": sum(
            row["cubic_quotients"] for row in pair_rows
        ),
        "first_tail_nonzero_remainders": 0,
        "deep_pair": [40, 41],
        "deep_pair_checked_through_degree": 6,
        "deep_pair_degree_six_terms": len(next_tail),
        "deep_pair_degree_six_quadratic_quotients": len(q6),
        "deep_pair_degree_six_cubic_quotients": len(c6),
        "deep_pair_degree_six_quadratic_steps": q6_steps,
        "deep_pair_degree_six_remainder_terms": len(remainder6),
        "covered_critical_pair_class": "cubic-cubic first tails only",
        "unresolved_critical_pair_classes": [
            "quadratic-quadratic lifted tails",
            "quadratic-cubic lifted tails",
            "higher tails or a finite maximal-ideal unit-loop",
        ],
    }
    return ledger


def main():
    ledger = audit()
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                "frozen lifted cubic S-pair ledger changed")
    print(
        "n=8 lifted cubic S-pairs: PASS; 9 compact lifts, "
        "36/36 first tails reduce to zero; C40,C41 closes through degree 6"
    )
    print(json.dumps(ledger, sort_keys=True))
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
