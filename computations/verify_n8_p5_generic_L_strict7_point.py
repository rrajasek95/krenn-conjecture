#!/usr/bin/env python3
"""Test P5 strict order seven on the deterministic generic-L point.

This is a deliberately point-local first pass.  It retains a symbolic third
free z46 bend while specializing the 45 base P5 parameters, so a successful
root proves that the new mixed compatibility does not kill the previously
found H0 degree-ten survivor everywhere on the dense L component.
"""

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


THIRD = load_module(
    "n8_p5_third_order_for_strict7_point",
    "verify_n8_p5_third_order_next_pure.py",
)
GENERIC = load_module(
    "n8_p5_generic_L_for_strict7_point",
    "verify_n8_p5_generic_L_h0_degree9.py",
)
P5 = THIRD.P5
CUBIC = THIRD.CUBIC
COMPAT = THIRD.COMPONENT.COMPAT
QQ = Fraction

THIRD_BEND = 58
EXPECTED_LEDGER_SHA256 = (
    "466ebdf963f95fe70bd9c2b6493257b7bde3be2fa99cefa6ee00198b3b74a81e"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def add(target, source, scale=QQ(1)):
    CUBIC.add_scaled(target, source, scale)


def multiply(left, right):
    return CUBIC.multiply_polynomials(left, right)


def constant(value):
    return {(): QQ(value)} if value else {}


def negate(source):
    return {monomial: -coefficient for monomial, coefficient in source.items()}


def polynomial_digest(source):
    encoded = polynomial_encoding(source)
    return sha256(json.dumps(encoded, separators=(",", ":")).encode()).hexdigest()


def polynomial_encoding(source):
    return [
        [list(monomial), coefficient.numerator, coefficient.denominator]
        for monomial, coefficient in sorted(source.items())
    ]


def linear_root(source):
    require(set(source).issubset({(), (THIRD_BEND,)}),
            f"third-bend compatibility is not linear: {source}")
    slope = source.get((THIRD_BEND,), QQ(0))
    require(slope, f"third-bend compatibility has zero slope: {source}")
    return -source.get((), QQ(0)) / slope


def base_point():
    point = {index: QQ(index + 2) for index in range(56)}
    for variable in P5.P5_NORMAL_VARIABLES:
        point[variable] = QQ(0)
    point[15] = point[16]
    point[46] = point[9] * point[25] / point[11]
    require(point[9] * point[25] == point[11] * point[46],
            "deterministic point left L=0")
    return point


def partial_evaluate(source, point):
    """Evaluate the base P5 variables and retain bend variables >= 56."""

    answer = {}
    for monomial, coefficient in source.items():
        retained = []
        value = coefficient
        for variable in monomial:
            if variable in point:
                value *= point[variable]
            else:
                retained.append(variable)
        key = tuple(retained)
        answer[key] = answer.get(key, QQ(0)) + value
        if not answer[key]:
            answer.pop(key)
    return answer


def evaluate_correction(correction, point):
    return {
        coordinate: value
        for coordinate, source in correction.items()
        if (value := partial_evaluate(source, point))
    }


def transverse(residual, jacobian, b, detail):
    correction = {}
    for coordinate, row in zip(P5.P5_NORMAL_VARIABLES, P5.B_PIVOT_ROWS):
        if residual[row]:
            correction[coordinate] = {
                monomial: -coefficient / b
                for monomial, coefficient in residual[row].items()
            }
    image = P5.jacobian_times(jacobian, correction)
    compatibility = [dict(value) for value in residual]
    for equation in range(39):
        add(compatibility[equation], image[equation])
    for row in P5.B_PIVOT_ROWS:
        require(not compatibility[row],
                f"{detail}: pivot reconstruction failed at Q{row + 1}: "
                f"residual={residual[row]} image={image[row]}")
    return correction, compatibility


def third_from_second(reducer, second):
    """Reuse the streamed second projector instead of duplicating its caches."""

    third = object.__new__(THIRD.ThirdOrderProjector)
    third.second = second
    third.base = second.base
    third.reducer = reducer
    third.w = second.w
    third.n2 = second.n2
    third.n3, third.direction_ledger = THIRD.third_normal_direction(second)
    third.n3_cache = {}
    third.mixed_cache = {}
    third.third_w_cache = {}
    third.coefficient_cache = {}
    third.functional_cache = {}
    return third


def state_residual_jets(strict, state, degree):
    if degree <= 4:
        result = [
            [dict(value) for value in group]
            for group in strict.functional_jets(state["functional"], degree)
        ]
    else:
        result = [[{} for _strict in range(4 - normal)]
                  for normal in range(4)]
    for multiplier, functional in state["corrections"]:
        multiplier_degree = len(next(iter(multiplier)))
        equation_degree = degree - multiplier_degree
        if not 0 <= equation_degree <= 4:
            continue
        product = strict.product_jets(
            strict.source_jets(multiplier),
            strict.functional_jets(functional, equation_degree),
        )
        for normal, group in enumerate(product):
            for strict_order, value in enumerate(group):
                add(result[normal][strict_order], value, -1)
    return result


def higher_mixed_coefficients(strict, state, targets):
    jets = {
        degree: state_residual_jets(strict, state, degree)
        for degree in range(6, max(targets) + 1)
    }
    answers = {}
    for target in targets:
        answer = {}
        for degree in range(6, target + 1):
            for normal_order, group in enumerate(jets[degree]):
                strict_order = target - degree - normal_order
                if 0 <= strict_order < len(group):
                    add(answer, group[strict_order])
        answers[target] = answer
    return answers


def clear_state_caches(strict):
    strict.source_cache.clear()
    strict.functional_cache.clear()
    strict.directional_cache.clear()
    strict.second_w_cache.clear()
    third = strict.third
    third.n3_cache.clear()
    third.mixed_cache.clear()
    third.third_w_cache.clear()
    third.coefficient_cache.clear()
    third.functional_cache.clear()
    third.second.n2_cache.clear()
    third.second.s2_cache.clear()
    third.second.factor_cache.clear()
    third.second.functional_cache.clear()
    third.base.restriction_cache.clear()
    third.base.derivative_cache.clear()
    third.base.functional_restriction_cache.clear()
    third.base.functional_derivative_cache.clear()


def pure_point_coefficient(label, reducer, pure, target, corrections, point):
    third = THIRD.ThirdOrderProjector(reducer)
    require(not THIRD.validate_normal_graph(third),
            f"{label} third normal graph regression returned")
    strict = THIRD.ThirdStrictProjector(third, corrections[:3])
    source = THIRD.component_coefficient(strict, reducer, pure, target)
    answer = partial_evaluate(source, point)
    require(all(set(monomial).issubset({THIRD_BEND}) for monomial in answer),
            f"{label} point coefficient retained a non-bend variable")
    return answer


def initial_corrections(compatibility, point):
    parts = compatibility["parts"]
    jacobian = [
        [partial_evaluate(value, point) for value in row]
        for row in compatibility["jacobian"]
    ]
    b = point[44] + point[45]

    c1 = evaluate_correction(compatibility["corrections"][0], point)
    first = P5.polynomial((
        ((9, 29, 44), -1),
        ((0, 11, 46), 1),
        ((11, 24, 46), -1),
        ((11, 26, 54), 1),
    ))
    first_value = COMPAT.evaluate(first, point)
    first_bend = -first_value / point[11]
    c1[46] = constant(first_bend)

    residual2 = P5.strict_residual(parts, [c1], 2)
    residual2 = [partial_evaluate(value, point) for value in residual2]
    c2, compatibility2 = transverse(residual2, jacobian, b, "order two")
    require(not any(compatibility2), "order-two compatibility returned")
    second_bend = QQ(317140, 13)
    c2[46] = constant(second_bend)

    residual3 = P5.strict_residual(parts, [c1, c2], 3)
    residual3 = [partial_evaluate(value, point) for value in residual3]
    c3, compatibility3 = transverse(residual3, jacobian, b, "order three")
    require(not any(compatibility3), "order-three compatibility returned")
    c3[46] = P5.monomial(THIRD_BEND)
    return [c1, c2, c3], jacobian, b, first_bend, second_bend


def audit():
    point = base_point()
    degree8 = THIRD.DEG8.degree_eight_tail_data()
    compatibility = COMPAT.compatibility_tail_data(
        False, degree8["degree_seven_data"]
    )
    corrections, jacobian, b, first_bend, second_bend = initial_corrections(
        compatibility, point
    )

    series = degree8["degree_seven_data"]["series"]
    third = third_from_second(series.reducer, degree8["second_projector"])
    require(not THIRD.validate_normal_graph(third),
            "third normal graph regression returned")
    strict = THIRD.ThirdStrictProjector(third, corrections)

    higher = {7: [], 8: [], 9: []}
    for number in range(1, 40):
        state = series._state(number)
        values = higher_mixed_coefficients(strict, state, higher)
        for target, value in values.items():
            higher[target].append(partial_evaluate(value, point))
        clear_state_caches(strict)
        print("Q", number, "higher terms",
              tuple(len(higher[target][-1]) for target in higher), flush=True)

    parts = compatibility["parts"]
    residual4 = P5.strict_residual(parts, corrections, 4)
    residual4 = [partial_evaluate(value, point) for value in residual4]
    degree6 = degree8["degree_seven_data"]["degree_six"]
    for equation in range(39):
        add(residual4[equation], partial_evaluate(degree6[equation], point))
    c4, compatibility4 = transverse(residual4, jacobian, b, "order four")
    require(not any(compatibility4), "order-four compatibility returned")
    corrections.append(c4)

    compatibility_orders = {}
    for order, tail_target in ((5, 7), (6, 8), (7, 9)):
        residual = P5.strict_residual(parts, corrections, order)
        residual = [partial_evaluate(value, point) for value in residual]
        for equation in range(39):
            add(residual[equation], higher[tail_target][equation])
        correction, remaining = transverse(
            residual, jacobian, b, f"order {order}"
        )
        compatibility_orders[order] = remaining
        nonzero = [(index + 1, len(value), polynomial_digest(value))
                   for index, value in enumerate(remaining) if value]
        print("ORDER", order, "COMPATIBILITY", nonzero, flush=True)
        if order < 7:
            require(not nonzero, f"order-{order} compatibility returned")
            corrections.append(correction)

    order7 = compatibility_orders[7]
    require(all(
        set(monomial).issubset({THIRD_BEND})
        for value in order7 for monomial in value
    ), "strict-order-seven point compatibility is not univariate")
    nonzero_order7 = [value for value in order7 if value]
    require(len(nonzero_order7) == 2,
            "strict-order-seven exceptional pair changed")
    roots = [linear_root(value) for value in nonzero_order7]
    require(roots[0] == roots[1],
            f"strict-order-seven exceptional roots disagree: {roots}")
    third_bend = roots[0]

    h1, h1_pure, _terms, _quotients = THIRD.NEXT.h1_reducer()
    h1_degree9 = pure_point_coefficient(
        "H1", h1, h1_pure, 9, corrections, point
    )
    h1_value = sum(
        coefficient * third_bend ** monomial.count(THIRD_BEND)
        for monomial, coefficient in h1_degree9.items()
    )
    print("H1 DEGREE 9", polynomial_encoding(h1_degree9),
          "VALUE", h1_value, flush=True)

    h0, h0_pure, _terms, _quotients, _remainder = THIRD.NEXT.h0_reducer()
    h0_degree10 = pure_point_coefficient(
        "H0", h0, h0_pure, 10, corrections, point
    )
    h0_value = sum(
        coefficient * third_bend ** monomial.count(THIRD_BEND)
        for monomial, coefficient in h0_degree10.items()
    )
    print("H0 DEGREE 10", polynomial_encoding(h0_degree10),
          "VALUE", h0_value, flush=True)
    require(
        h0_degree10 == {
            monomial: QQ(-124, 25) * coefficient
            for monomial, coefficient in nonzero_order7[0].items()
        },
        "H0 degree ten lost its Q30 proportionality",
    )
    require(
        h0_degree10 == {
            monomial: QQ(62, 3) * coefficient
            for monomial, coefficient in nonzero_order7[1].items()
        },
        "H0 degree ten lost its Q33 proportionality",
    )
    require(not h1_value and not h0_value,
            "a pure coefficient survived the strict-order-seven lift")
    ledger = {
        "branch": "P5",
        "scope": "deterministic exact point on dense generic L",
        "third_bend": "r=z46^(3)",
        "first_bend": [first_bend.numerator, first_bend.denominator],
        "second_bend": [second_bend.numerator, second_bend.denominator],
        "third_normal_direction": third.direction_ledger,
        "higher_mixed_nonzeros": {
            str(target): sum(bool(value) for value in values)
            for target, values in higher.items()
        },
        "strict_order_seven_compatibility": [
            [index + 1, polynomial_encoding(value), polynomial_digest(value)]
            for index, value in enumerate(order7) if value
        ],
        "third_bend_solution": [third_bend.numerator, third_bend.denominator],
        "pure_coefficients_on_lifted_jet": {
            "H1_degree_nine": {
                "polynomial": polynomial_encoding(h1_degree9),
                "sha256": polynomial_digest(h1_degree9),
                "value": [h1_value.numerator, h1_value.denominator],
            },
            "H0_degree_ten": {
                "polynomial": polynomial_encoding(h0_degree10),
                "sha256": polynomial_digest(h0_degree10),
                "value": [h0_value.numerator, h0_value.denominator],
            },
        },
        "scope_guard": (
            "point-local mixed strict-order-seven and pure-coefficient test; "
            "the symbolic generic-L component and all-order lift are separate"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "P5 generic-L strict7 point ledger changed")
    print(json.dumps(ledger, indent=2, sort_keys=True))
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    audit()
