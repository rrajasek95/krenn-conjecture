#!/usr/bin/env python3
"""Verify the next component-local H1/H0 coefficients on P5."""

from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def load_module(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


COMPONENT = load_module(
    "n8_p5_degree8_components_for_h1",
    "verify_n8_p5_degree8_component_compatibility.py",
)
PURE = load_module(
    "n8_p5_pure_degree7_for_next_h1",
    "verify_n8_p5_degree7_components_next_pure.py",
)
DEG8 = COMPONENT.DEG8
LOCAL = PURE.LOCAL
CUBIC = PURE.CUBIC
P5 = PURE.P5
QQ = Fraction

EXPECTED_LEDGER_SHA256 = (
    "923aa11aeedcb2d89bd9a6777812f4f6106d63b79d3d56a2de7186bf7fd0552c"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def add(target, source, scale=QQ(1)):
    CUBIC.add_scaled(target, source, scale)


def add_obstruction_corrections(reducer, quotients, degree):
    for (pivot, multiplier), coefficient in quotients.items():
        ambient_multiplier = LOCAL.SOURCE.convert_tangent_multiplier(
            multiplier, coefficient, reducer.free_columns
        )
        reducer.add_correction(
            ambient_multiplier,
            reducer.obstruction_functional(pivot),
            f"degree_{degree}_obstruction",
        )


def pure_residual_jets(strict, reducer, pure, degree):
    if degree <= 4:
        groups = strict.source_jets(CUBIC.hasse_form(pure, degree))
        result = (
            [dict(value) for value in groups[0]],
            [dict(value) for value in groups[1]],
            dict(groups[2]),
        )
    else:
        result = ([{}, {}, {}], [{}, {}], {})
    base, first, second = result
    for correction in reducer.corrections:
        equation_degree = degree - correction["degree"]
        if not 0 <= equation_degree <= 4:
            continue
        product = strict.product_jets(
            strict.source_jets(correction["multiplier"]),
            strict.functional_jets(
                correction["functional"], equation_degree
            ),
        )
        for order in range(3):
            add(base[order], product[0][order], -1)
        for order in range(2):
            add(first[order], product[1][order], -1)
        add(second, product[2], -1)
    return base, first, second


def next_coefficient(strict, reducer, pure):
    six = pure_residual_jets(strict, reducer, pure, 6)
    seven = pure_residual_jets(strict, reducer, pure, 7)
    eight = pure_residual_jets(strict, reducer, pure, 8)
    degree_seven = dict(six[0][1])
    add(degree_seven, seven[0][0])
    add(degree_seven, six[1][0])
    degree_eight = dict(six[0][2])
    add(degree_eight, seven[0][1])
    add(degree_eight, six[1][1])
    add(degree_eight, eight[0][0])
    add(degree_eight, seven[1][0])
    add(degree_eight, six[2])
    return degree_seven, degree_eight


def h0_next_coefficient(strict, reducer, pure):
    seven = pure_residual_jets(strict, reducer, pure, 7)
    eight = pure_residual_jets(strict, reducer, pure, 8)
    nine = pure_residual_jets(strict, reducer, pure, 9)
    degree_eight = dict(seven[0][1])
    add(degree_eight, eight[0][0])
    add(degree_eight, seven[1][0])
    degree_nine = dict(seven[0][2])
    add(degree_nine, eight[0][1])
    add(degree_nine, seven[1][1])
    add(degree_nine, nine[0][0])
    add(degree_nine, eight[1][0])
    add(degree_nine, seven[2])
    return degree_eight, degree_nine


def h1_reducer():
    reducer = LOCAL.LocalReducer()
    selected = LOCAL.SECOND.MIXED_WORD_1
    pure = LOCAL.SECOND.PURE_WORD_1
    reducer.add_correction(
        {(): QQ(1)},
        {LOCAL.THIRD.MIXED_WORD_INDEX[selected]: QQ(1)},
        "selected_mixed_coefficient",
    )
    for degree in range(1, 6):
        record = reducer.reduce_degree(pure, degree)
        require(record["complete"], f"H1 failed before degree {degree}")
    tangent6, _stream = reducer.streamed_tangent_residual(pure, 6)
    quotients, remainder, _steps = (
        LOCAL.FOURTH.reduce_by_quadratic_obstructions(
            tangent6, reducer.simple_obstructions
        )
    )
    require(not remainder, "H1 degree-six remainder returned")
    add_obstruction_corrections(reducer, quotients, 6)
    return reducer, pure, len(tangent6), len(quotients)


def h0_reducer():
    reducer = LOCAL.LocalReducer()
    selected = LOCAL.SECOND.MIXED_WORD_0
    pure = LOCAL.SECOND.PURE_WORD_0
    reducer.add_correction(
        {(): QQ(1)},
        {LOCAL.THIRD.MIXED_WORD_INDEX[selected]: QQ(1)},
        "selected_mixed_coefficient",
    )
    for degree in range(1, 7):
        record = reducer.reduce_degree(pure, degree)
        require(record["complete"], f"H0 failed before degree {degree}")
    tangent7, _stream = reducer.streamed_tangent_residual(pure, 7)
    quotients, remainder, _steps = (
        LOCAL.FOURTH.reduce_by_quadratic_obstructions(
            tangent7, reducer.simple_obstructions
        )
    )
    expected = P5.multiply_many((
        P5.monomial(16, 16, 41),
        P5.polynomial((((44,), 1), ((45,), 1))),
        P5.polynomial((((53,), 1), ((51,), -1))),
        P5.polynomial((((9, 25), 1), ((11, 46), -1))),
    ))
    require(remainder == expected, "H0 degree-seven remainder changed")
    add_obstruction_corrections(reducer, quotients, 7)
    return reducer, pure, len(tangent7), len(quotients), len(remainder)


def L_point_first_two_corrections(compatibility):
    point = {index: QQ(index + 2) for index in range(56)}
    for variable in P5.P5_NORMAL_VARIABLES:
        point[variable] = QQ(0)
    point[15] = point[16]
    point[46] = point[9] * point[25] / point[11]
    c1 = COMPONENT.evaluate_correction(
        compatibility["corrections"][0], point
    )
    c1[46] = COMPONENT.constant_polynomial(QQ(2430, 13))
    residual2 = P5.strict_residual(compatibility["parts"], [c1], 2)
    c2, remaining = COMPONENT.solve_transverse_at_point(
        residual2, compatibility["jacobian"], point, "H1 L point order two"
    )
    require(not remaining, "H1 L point failed before second free bend")
    c2[46] = COMPONENT.constant_polynomial(QQ(317140, 13))
    return point, [c1, c2]


def audit():
    compatibility = COMPONENT.COMPAT.compatibility_tail_data(False)
    reducer, pure, tangent_terms, quotient_count = h1_reducer()

    strict = COMPONENT.StrictJetProjector(
        DEG8.SecondOrderProjector(
            DEG8.TAILS.FactorizedP5Projector(reducer)
        ),
        compatibility["corrections"][:2],
    )
    prior, next_form = next_coefficient(strict, reducer, pure)
    require(not prior, "H1 degree-seven P5 regression returned")
    z16 = COMPONENT.restrict_zero(next_form, 16)
    z41 = COMPONENT.restrict_zero(next_form, 41)
    expected_h1 = P5.multiply_many((
        P5.monomial(4, 16, 16, 41, 41, coefficient=2),
        P5.polynomial((((44,), 1), ((45,), 1))),
        P5.polynomial((((9, 25), 1), ((11, 46), -1))),
    ))
    require(next_form == expected_h1, "H1 next component factor changed")
    require(PURE.component_flags(next_form) == {
        "zero_on_z16": True,
        "zero_on_z41": True,
        "zero_on_L": True,
    }, "H1 next component restrictions changed")
    require(not z16 and not z41,
            "H1 next form survived a coordinate component")

    point, point_corrections = L_point_first_two_corrections(compatibility)
    point_strict = COMPONENT.StrictJetProjector(
        DEG8.SecondOrderProjector(
            DEG8.TAILS.FactorizedP5Projector(reducer)
        ),
        point_corrections,
    )
    point_prior, point_next = next_coefficient(
        point_strict, reducer, pure
    )
    require(not COMPONENT.COMPAT.evaluate(point_prior, point),
            "H1 degree-seven exact point regression returned")
    h1_point_value = COMPONENT.COMPAT.evaluate(point_next, point)
    require(not h1_point_value, "H1 next form survived the exact L point")

    h0, h0_pure, h0_tangent, h0_quotients, h0_remainder = h0_reducer()
    h0_strict = COMPONENT.StrictJetProjector(
        DEG8.SecondOrderProjector(
            DEG8.TAILS.FactorizedP5Projector(h0)
        ),
        compatibility["corrections"][:2],
    )
    h0_prior, h0_next = h0_next_coefficient(h0_strict, h0, h0_pure)
    expected_h0_flags = {
        "zero_on_z16": True,
        "zero_on_z41": True,
        "zero_on_L": False,
    }
    require(PURE.component_flags(h0_prior) == expected_h0_flags,
            "raw H0 prior component restrictions changed")
    require(PURE.component_flags(h0_next) == expected_h0_flags,
            "H0 next component restrictions changed")
    require(not COMPONENT.restrict_zero(h0_next, 16)
            and not COMPONENT.restrict_zero(h0_next, 41),
            "H0 next form survived a coordinate component")
    h0_point_strict = COMPONENT.StrictJetProjector(
        DEG8.SecondOrderProjector(
            DEG8.TAILS.FactorizedP5Projector(h0)
        ),
        point_corrections,
    )
    h0_point_prior, h0_point_next = h0_next_coefficient(
        h0_point_strict, h0, h0_pure
    )
    h0_point_prior_value = COMPONENT.COMPAT.evaluate(h0_point_prior, point)
    h0_point_next_value = COMPONENT.COMPAT.evaluate(h0_point_next, point)
    require(not h0_point_prior_value,
            "raw H0 prior survived the bent exact L point")
    require(not h0_point_next_value,
            "H0 next form survived the bent exact L point")

    ledger = {
        "branch": "P5",
        "chart": "b=z44+z45 != 0",
        "H1": {
            "degree_six_tangent_terms": tangent_terms,
            "degree_six_obstruction_quotients": quotient_count,
            "degree_seven_component_regression_terms": len(prior),
            "degree_eight_terms": len(next_form),
            "degree_eight_factor": "2*z4*z16^2*z41^2*b*L",
            "degree_eight_sha256": PURE.polynomial_digest(next_form),
            "degree_eight_component_restrictions": (
                PURE.component_flags(next_form)
            ),
            "exact_L_point_expression_terms": len(point_next),
            "exact_L_point_expression_sha256": (
                PURE.polynomial_digest(point_next)
            ),
            "exact_L_point_value": 0,
        },
        "H0": {
            "degree_seven_tangent_terms": h0_tangent,
            "degree_seven_obstruction_quotients": h0_quotients,
            "degree_seven_remainder_terms": h0_remainder,
            "raw_degree_eight_terms": len(h0_prior),
            "raw_degree_eight_sha256": PURE.polynomial_digest(h0_prior),
            "degree_nine_terms": len(h0_next),
            "degree_nine_sha256": PURE.polynomial_digest(h0_next),
            "degree_nine_component_restrictions": (
                PURE.component_flags(h0_next)
            ),
            "exact_L_point_degree_eight_value": 0,
            "exact_L_point_degree_nine_expression_terms": len(h0_point_next),
            "exact_L_point_degree_nine_expression_sha256": (
                PURE.polynomial_digest(h0_point_next)
            ),
            "exact_L_point_degree_nine_value": 0,
        },
        "verdict": (
            "H1 degree eight and H0 degree nine vanish on z16=0 and z41=0; "
            "both also vanish at the certified bent rational L point"
        ),
        "scope_guard": (
            "the H0 L-component statement is one exact point, not a "
            "symbolic generic-L identity; no all-orders pure membership or "
            "counterexample is certified"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "P5 component-local next-pure ledger changed")
    print(json.dumps(ledger, indent=2, sort_keys=True))
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    audit()
