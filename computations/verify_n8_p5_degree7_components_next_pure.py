#!/usr/bin/env python3
"""Verify the strict degree-seven P5 components and next pure normal forms."""

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


TAILS = load_module(
    "n8_p5_degree7_mixed_for_pure",
    "verify_n8_p5_streamed_degree7_mixed_tails.py",
)
COMPAT = load_module(
    "n8_p5_degree7_compatibility_for_pure",
    "analyze_n8_p5_degree7_compatibility_tails.py",
)
LOCAL = TAILS.LIFTED.LOCAL
P5 = TAILS.P5
CUBIC = P5.CUBIC
QQ = Fraction

EXPECTED_LEDGER_SHA256 = (
    "ebe384530dd3362b32f5719e573a4d95ef6b37aeb334bb7bd3af6aa5cfc5ac97"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def add(target, source, scale=QQ(1)):
    CUBIC.add_scaled(target, source, scale)


def multiply(left, right):
    return CUBIC.multiply_polynomials(left, right)


def polynomial_digest(source):
    encoded = [
        [list(monomial), coefficient.numerator, coefficient.denominator]
        for monomial, coefficient in sorted(source.items())
    ]
    return sha256(json.dumps(encoded, separators=(",", ":")).encode()).hexdigest()


def polynomial_list_digest(sources):
    encoded = [[
        [list(monomial), coefficient.numerator, coefficient.denominator]
        for monomial, coefficient in sorted(source.items())
    ] for source in sources]
    return sha256(json.dumps(encoded, separators=(",", ":")).encode()).hexdigest()


def restrict_zero(source, variable):
    return {
        monomial: coefficient
        for monomial, coefficient in source.items()
        if variable not in monomial
    }


def divide_by_monomial(source, divisor):
    answer = {}
    for monomial, coefficient in source.items():
        output = list(monomial)
        for variable in divisor:
            require(variable in output,
                    f"term {monomial} is not divisible by {divisor}")
            output.remove(variable)
        answer[tuple(output)] = coefficient
    return answer


ELL = P5.polynomial((((9, 25), 1), ((11, 46), -1)))


def divide_by_ell_with_remainder(source):
    """Divide with leading monomial z9*z25 in a lex order with z9 > z11."""

    residual = dict(source)
    quotient = {}
    while True:
        candidates = [
            monomial for monomial in residual
            if 9 in monomial and 25 in monomial
        ]
        if not candidates:
            break
        selected = max(candidates, key=lambda item: (item.count(9), item))
        coefficient = residual[selected]
        output = list(selected)
        output.remove(9)
        output.remove(25)
        output = tuple(output)
        add(quotient, {output: coefficient})
        add(residual, multiply({output: coefficient}, ELL), -1)
    reconstruction = multiply(quotient, ELL)
    add(reconstruction, residual)
    require(reconstruction == source, "L division failed to reconstruct input")
    return quotient, residual


def component_flags(source):
    _ell_quotient, ell_remainder = divide_by_ell_with_remainder(source)
    return {
        "zero_on_z16": not restrict_zero(source, 16),
        "zero_on_z41": not restrict_zero(source, 41),
        "zero_on_L": not ell_remainder,
    }


def pure_projection(reducer, projector, pure_word, degree, differentiate=False):
    if degree <= 4:
        ambient = CUBIC.hasse_form(pure_word, degree)
        answer = (
            projector.weighted_derivative(ambient)
            if differentiate else projector.restrict(ambient)
        )
        answer = dict(answer)
    else:
        answer = {}
    for correction in reducer.corrections:
        equation_degree = degree - correction["degree"]
        if not 0 <= equation_degree <= 4:
            continue
        multiplier = correction["multiplier"]
        functional = correction["functional"]
        multiplier_value = projector.restrict(multiplier)
        equation_value, equation_derivative = projector.functional_factors(
            functional, equation_degree
        )
        if differentiate:
            multiplier_derivative = projector.weighted_derivative(multiplier)
            if multiplier_derivative and equation_value:
                add(answer, multiply(multiplier_derivative, equation_value), -1)
            if multiplier_value and equation_derivative:
                add(answer, multiply(multiplier_value, equation_derivative), -1)
        elif multiplier_value and equation_value:
            add(answer, multiply(multiplier_value, equation_value), -1)
    return answer


def obstruction_correction_projection(
    reducer, projector, obstruction_quotients, equation_degree,
    differentiate=False,
):
    answer = {}
    for (pivot, multiplier), coefficient in obstruction_quotients.items():
        ambient_multiplier = LOCAL.SOURCE.convert_tangent_multiplier(
            multiplier, coefficient, reducer.free_columns
        )
        functional = reducer.obstruction_functional(pivot)
        multiplier_value = projector.restrict(ambient_multiplier)
        equation_value, equation_derivative = projector.functional_factors(
            functional, equation_degree
        )
        if differentiate:
            multiplier_derivative = projector.weighted_derivative(
                ambient_multiplier
            )
            if multiplier_derivative and equation_value:
                add(answer, multiply(multiplier_derivative, equation_value))
            if multiplier_value and equation_derivative:
                add(answer, multiply(multiplier_value, equation_derivative))
        elif multiplier_value and equation_value:
            add(answer, multiply(multiplier_value, equation_value))
    return answer


def h1_degree_seven():
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
    obstruction_quotients, remainder, _steps = (
        LOCAL.FOURTH.reduce_by_quadratic_obstructions(
            tangent6, reducer.simple_obstructions
        )
    )
    require(not remainder, "H1 degree-six obstruction remainder returned")

    projector = TAILS.FactorizedP5Projector(reducer)
    old7 = pure_projection(reducer, projector, pure, 7)
    derivative6 = pure_projection(
        reducer, projector, pure, 6, differentiate=True
    )
    obstruction7 = obstruction_correction_projection(
        reducer, projector, obstruction_quotients, 3
    )
    obstruction6_derivative = obstruction_correction_projection(
        reducer, projector, obstruction_quotients, 2, differentiate=True
    )
    answer = dict(old7)
    add(answer, obstruction7, -1)
    add(answer, derivative6, -1)
    add(answer, obstruction6_derivative)
    return answer, {
        "degree_six_tangent_terms": len(tangent6),
        "degree_six_obstruction_quotients": len(obstruction_quotients),
        "old_degree_seven_terms": len(old7),
        "degree_six_weighted_derivative_terms": len(derivative6),
        "degree_seven_obstruction_tail_terms": len(obstruction7),
        "degree_six_obstruction_weighted_derivative_terms": len(
            obstruction6_derivative
        ),
        "final_terms": len(answer),
    }


def h0_degree_eight(compatibility_data):
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
    obstruction_quotients, remainder, _steps = (
        LOCAL.FOURTH.reduce_by_quadratic_obstructions(
            tangent7, reducer.simple_obstructions
        )
    )
    expected_remainder = P5.multiply_many((
        P5.monomial(16, 16, 41),
        P5.polynomial((((44,), 1), ((45,), 1))),
        P5.polynomial((((53,), 1), ((51,), -1))),
        P5.polynomial((((9, 25), 1), ((11, 46), -1))),
    ))
    require(remainder == expected_remainder,
            "H0 degree-seven remainder changed")

    projector = TAILS.FactorizedP5Projector(reducer)
    old8 = pure_projection(reducer, projector, pure, 8)
    derivative7 = pure_projection(
        reducer, projector, pure, 7, differentiate=True
    )
    obstruction8 = obstruction_correction_projection(
        reducer, projector, obstruction_quotients, 3
    )
    obstruction7_derivative = obstruction_correction_projection(
        reducer, projector, obstruction_quotients, 2, differentiate=True
    )
    before_compatibility = dict(old8)
    add(before_compatibility, obstruction8, -1)
    add(before_compatibility, derivative7, -1)
    add(before_compatibility, obstruction7_derivative)

    h30 = compatibility_data["normalized_compatibility"][29]
    h33 = compatibility_data["normalized_compatibility"][32]
    difference = dict(h30)
    add(difference, h33, -1)
    final_factor = P5.polynomial((((53,), 1), ((51,), -1)))
    compatibility_tail = multiply(final_factor, difference)
    compatibility_tail = {
        monomial: 2 * coefficient
        for monomial, coefficient in compatibility_tail.items()
    }
    answer = dict(before_compatibility)
    add(answer, compatibility_tail)
    return answer, {
        "degree_seven_tangent_terms": len(tangent7),
        "degree_seven_obstruction_quotients": len(obstruction_quotients),
        "degree_seven_remainder_terms": len(remainder),
        "old_degree_eight_terms": len(old8),
        "degree_seven_weighted_derivative_terms": len(derivative7),
        "degree_eight_obstruction_tail_terms": len(obstruction8),
        "degree_seven_obstruction_weighted_derivative_terms": len(
            obstruction7_derivative
        ),
        "before_compatibility_terms": len(before_compatibility),
        "compatibility_tail_terms": len(compatibility_tail),
        "final_terms": len(answer),
    }


def audit():
    compatibility_data = COMPAT.compatibility_tail_data(False)
    compatibility = compatibility_data["normalized_compatibility"]
    nonzero = [
        (index + 1, len(value))
        for index, value in enumerate(compatibility) if value
    ]
    require(nonzero == [
        (1, 4), (4, 4), (10, 6), (11, 2), (14, 4), (16, 4),
        (22, 4), (25, 6), (26, 2), (28, 4), (30, 46), (31, 4),
        (33, 42), (36, 4), (37, 6), (38, 2),
    ], "degree-seven compatibility support changed")

    for _index, value in enumerate(compatibility):
        if value:
            divide_by_monomial(value, (16, 16, 41))
    exceptional = {29, 32}
    for index, value in enumerate(compatibility):
        if value and index not in exceptional:
            _quotient, remainder = divide_by_ell_with_remainder(value)
            require(not remainder,
                    f"compatibility equation {index + 1} lost its L factor")

    h30 = compatibility[29]
    h33 = compatibility[32]
    u = P5.polynomial((((26,), 1), ((45,), 1)))
    v = P5.polynomial((((26,), 1), ((44,), -1)))
    relation = multiply(v, h30)
    add(relation, multiply(u, h33), -1)
    relation_quotient, relation_remainder = divide_by_ell_with_remainder(
        relation
    )
    require(not relation_remainder,
            "exceptional h30/h33 compatibility relation lost its L factor")

    h1, h1_ledger = h1_degree_seven()
    h0, h0_ledger = h0_degree_eight(compatibility_data)
    h1_components = component_flags(h1)
    h0_components = component_flags(h0)
    require(h1_components == {
        "zero_on_z16": False,
        "zero_on_z41": True,
        "zero_on_L": False,
    }, "H1 component restrictions changed")
    require(h0_components == {
        "zero_on_z16": True,
        "zero_on_z41": False,
        "zero_on_L": False,
    }, "H0 component restrictions changed")

    ledger = {
        "p5_free_parameters_retained": 45,
        "chart": "z44+z45 != 0",
        "degree_seven_compatibility_nonzero": nonzero,
        "degree_seven_compatibility_polynomial_sha256": (
            polynomial_list_digest(compatibility)
        ),
        "compatibility_common_factor": "z16^2*z41",
        "L_multiple_equations_one_based": [
            index + 1 for index, value in enumerate(compatibility)
            if value and index not in exceptional
        ],
        "exceptional_equations_one_based": [30, 33],
        "exceptional_L_relation": (
            "(z26-z44)*h30-(z26+z45)*h33 is in (L)"
        ),
        "exceptional_L_relation_terms": len(relation),
        "exceptional_L_quotient_terms": len(relation_quotient),
        "exceptional_L_quotient_sha256": polynomial_digest(
            relation_quotient
        ),
        "strict_components_lift_through_mixed_degree_seven": [
            "z16=0", "z41=0", "L=z9*z25-z11*z46=0",
        ],
        "H1_degree_seven": {
            "stream": h1_ledger,
            "polynomial_sha256": polynomial_digest(h1),
            "component_restrictions": h1_components,
        },
        "H0_degree_eight": {
            "stream": h0_ledger,
            "polynomial_sha256": polynomial_digest(h0),
            "component_restrictions": h0_components,
            "compatibility_tail_used": "2*(z53-z51)*(h30-h33)",
        },
        "generic_component_survivors": {
            "z16=0": ["H1 degree 7"],
            "z41=0": ["H0 degree 8"],
            "L=0": ["H1 degree 7", "H0 degree 8"],
        },
        "scope_guard": (
            "finite filtered formal-local P5 calculation on the b chart; "
            "nonzero pure classes may have further zero subloci and do not "
            "exhibit an all-orders counterexample"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "P5 strict-component/next-pure ledger changed")
    print(json.dumps(ledger, indent=2, sort_keys=True))
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    audit()
