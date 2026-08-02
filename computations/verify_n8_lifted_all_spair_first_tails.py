#!/usr/bin/env python3
"""Exact first-tail audit for all overlapping n=8 tangent critical pairs.

This extends the nine-cubic audit to the 39 quadratic--quadratic and 39 by 9
quadratic--cubic pair classes.  For each overlapping leading-monomial pair,
the tangent S-polynomial is divided by the 48-element tangent standard basis,
that division is lifted to the literal mixed equations, and the next filtered
tail is divided again.  Every calculation is over the rationals.

The result is the full *first-tail* Schreyer audit.  It is not an all-orders
standard-basis theorem: a finite contracting/unit-loop certificate is still
needed to control all subsequent tails.
"""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import json

import verify_n8_lifted_cubic_spair_first_tails as CUBIC_PAIR


CUBIC = CUBIC_PAIR.CUBIC
FOURTH = CUBIC_PAIR.FOURTH
QQ = Fraction

EXPECTED_LEDGER_SHA256 = (
    "a6828635ec68425f05212b8c3f4503c14fbd8950be2b642f122241605e068ea9"
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


def audit():
    series = CUBIC_PAIR.NormalObstructionSeries()
    reducer = series.reducer

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
    cubic_definitions = {
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
        for signed_variable, quadratic_name in cubic_definitions[number]:
            variable = abs(signed_variable)
            add(
                answer,
                multiply(
                    monomial_polynomial((variable,)),
                    series.part(quadratic_number[quadratic_name], degree - 1),
                ),
                -1 if signed_variable < 0 else 1,
            )
        return answer

    cubic_parts = {
        number: {degree: cubic_part(number, degree) for degree in (3, 4)}
        for number in cubic_definitions
    }
    for number, leading_monomial in cubic_leads.items():
        require(
            cubic_parts[number][3] == {leading_monomial: QQ(1)},
            f"compact lift C{number} changed",
        )

    # Cache the one higher filtered part of every quadratic lift.
    for number in range(1, 40):
        series.part(number, 3)

    def reduce_by_48(polynomial):
        quadratic_quotients, remainder, quadratic_steps = (
            FOURTH.reduce_by_quadratic_obstructions(
                polynomial, reducer.simple_obstructions
            )
        )
        cubic_quotients = {}
        final_remainder = {}
        for monomial, coefficient in sorted(remainder.items()):
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
            quadratic_quotients, reducer.simple_obstructions
        )
        for (number, multiplier), coefficient in cubic_quotients.items():
            add(
                replay,
                monomial_polynomial(
                    tuple(sorted(multiplier + cubic_leads[number])), coefficient
                ),
            )
        add(replay, final_remainder)
        require(replay == polynomial, "48-generator division did not replay")
        return (
            quadratic_quotients,
            cubic_quotients,
            final_remainder,
            quadratic_steps,
        )

    def quadratic_part(number, degree):
        return series.part(number, degree)

    def generator_part(kind, number, leading_degree, offset):
        degree = leading_degree + offset
        return (
            quadratic_part(number, degree)
            if kind == "quadratic"
            else cubic_parts[number][degree]
        )

    def audit_pair(pair_class, left, right):
        left_kind, left_number, left_lead = left
        right_kind, right_number, right_lead = right
        common = CUBIC_PAIR.multiset_lcm(left_lead, right_lead)
        left_multiplier = CUBIC_PAIR.quotient_monomial(left_lead, common)
        right_multiplier = CUBIC_PAIR.quotient_monomial(right_lead, common)
        left_degree = len(left_lead)
        right_degree = len(right_lead)

        tangent_spair = multiply(
            monomial_polynomial(left_multiplier),
            generator_part(left_kind, left_number, left_degree, 0),
        )
        add(
            tangent_spair,
            multiply(
                monomial_polynomial(right_multiplier),
                generator_part(right_kind, right_number, right_degree, 0),
            ),
            -1,
        )
        q0, c0, initial_remainder, initial_steps = reduce_by_48(tangent_spair)
        require(
            not initial_remainder,
            f"tangent S-pair failed for {pair_class} {left_number},{right_number}",
        )

        first_tail = multiply(
            monomial_polynomial(left_multiplier),
            generator_part(left_kind, left_number, left_degree, 1),
        )
        add(
            first_tail,
            multiply(
                monomial_polynomial(right_multiplier),
                generator_part(right_kind, right_number, right_degree, 1),
            ),
            -1,
        )
        for (pivot, multiplier), coefficient in q0.items():
            add(
                first_tail,
                multiply(
                    monomial_polynomial(multiplier, coefficient),
                    quadratic_part(series.pivot_to_number[pivot], 3),
                ),
                -1,
            )
        for (number, multiplier), coefficient in c0.items():
            add(
                first_tail,
                multiply(
                    monomial_polynomial(multiplier, coefficient),
                    cubic_parts[number][4],
                ),
                -1,
            )
        q1, c1, first_remainder, first_steps = reduce_by_48(first_tail)
        require(
            not first_remainder,
            f"lifted first tail failed for {pair_class} "
            f"{left_number},{right_number}",
        )
        return {
            "pair_class": pair_class,
            "pair": [left_number, right_number],
            "lcm_degree": len(common),
            "tangent_spair_terms": len(tangent_spair),
            "tangent_quadratic_quotients": len(q0),
            "tangent_cubic_quotients": len(c0),
            "tangent_quadratic_steps": initial_steps,
            "first_tail_degree": len(common) + 1,
            "first_tail_terms": len(first_tail),
            "first_tail_quadratic_quotients": len(q1),
            "first_tail_cubic_quotients": len(c1),
            "first_tail_quadratic_steps": first_steps,
            "first_tail_remainder_terms": len(first_remainder),
        }

    quadratic_generators = [
        ("quadratic", number, series.items[number - 1][0])
        for number in range(1, 40)
    ]
    cubic_generators = [
        ("cubic", number, cubic_leads[number])
        for number in range(40, 49)
    ]

    rows = []
    for left_index, left in enumerate(quadratic_generators):
        for right in quadratic_generators[left_index + 1:]:
            if set(left[2]) & set(right[2]):
                rows.append(audit_pair("quadratic-quadratic", left, right))
    for left in quadratic_generators:
        for right in cubic_generators:
            if set(left[2]) & set(right[2]):
                rows.append(audit_pair("quadratic-cubic", left, right))

    class_counts = Counter(row["pair_class"] for row in rows)
    require(class_counts == {
        "quadratic-quadratic": 201,
        "quadratic-cubic": 107,
    }, f"overlapping pair census changed: {class_counts}")
    require(all(row["first_tail_remainder_terms"] == 0 for row in rows),
            "a lifted first tail did not reduce to zero")

    return {
        "quadratic_generators": 39,
        "cubic_generators": 9,
        "quadratic_quadratic_total_pairs": 39 * 38 // 2,
        "quadratic_quadratic_overlapping_pairs": class_counts[
            "quadratic-quadratic"
        ],
        "quadratic_quadratic_product_criterion_pairs": (
            39 * 38 // 2 - class_counts["quadratic-quadratic"]
        ),
        "quadratic_cubic_total_pairs": 39 * 9,
        "quadratic_cubic_overlapping_pairs": class_counts["quadratic-cubic"],
        "quadratic_cubic_product_criterion_pairs": (
            39 * 9 - class_counts["quadratic-cubic"]
        ),
        "audited_pairs": len(rows),
        "tangent_spair_total_terms": sum(
            row["tangent_spair_terms"] for row in rows
        ),
        "tangent_quadratic_quotients": sum(
            row["tangent_quadratic_quotients"] for row in rows
        ),
        "tangent_cubic_quotients": sum(
            row["tangent_cubic_quotients"] for row in rows
        ),
        "first_tail_total_terms": sum(
            row["first_tail_terms"] for row in rows
        ),
        "first_tail_quadratic_quotients": sum(
            row["first_tail_quadratic_quotients"] for row in rows
        ),
        "first_tail_cubic_quotients": sum(
            row["first_tail_cubic_quotients"] for row in rows
        ),
        "first_tail_nonzero_remainders": sum(
            bool(row["first_tail_remainder_terms"]) for row in rows
        ),
        "combined_with_cubic_cubic_first_tail_audit": {
            "overlapping_pair_classes": 3,
            "overlapping_pairs": len(rows) + 36,
            "nonzero_first_tail_remainders": 0,
        },
        "scope_guard": (
            "all overlapping pair classes through their first lifted tails; "
            "higher tails still require a finite contracting/unit-loop proof"
        ),
    }


def main():
    ledger = audit()
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                "frozen all-pair first-tail ledger changed")
    print(
        "n=8 lifted all-pair first tails: PASS; "
        "201 Q-Q and 107 Q-C overlaps close, hence 344/344 with C-C"
    )
    print(json.dumps(ledger, sort_keys=True))
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
