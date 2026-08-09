#!/usr/bin/env python3
"""Stream the 39 degree-seven mixed tails on the full P5 branch.

This is the continuation primitive needed after the degree-six P5
compatibility kills the first H0 class.  It retains no large ambient
degree-six quotient.  Instead, the restriction of every quotient is obtained
as the first normal derivative of the factorized residual.  Contracting those
derivatives with the quadratic parts of the 196 Jacobian equations gives the
entire degree-seven correction in one weighted differential.
"""

from collections import Counter
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


P5 = load_module(
    "n8_p5_degree6_kill_for_degree7",
    "verify_n8_p5_degree6_compatibility_kills_h0.py",
)
LIFTED = P5.LIFTED
CUBIC = P5.CUBIC
QQ = Fraction

EXPECTED_LEDGER_SHA256 = (
    "e995dfca1bfab971279dc88bfad82ef1c9bb53f6522b832371ce24e5e71e717c"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def add(target, source, scale=QQ(1)):
    CUBIC.add_scaled(target, source, scale)


def multiply(left, right):
    return CUBIC.multiply_polynomials(left, right)


def normal_directions(reducer):
    """Dual ambient directions to the 196 echelon linear normal forms."""

    pivots = sorted(reducer.jacobian_pivots)
    answer = {}
    for target in pivots:
        direction = {}
        for pivot in reversed(pivots):
            row = reducer.jacobian_pivots[pivot][0]
            value = QQ(1 if pivot == target else 0)
            value -= sum(
                coefficient * direction.get(coordinate, QQ(0))
                for coordinate, coefficient in row.items()
                if coordinate != pivot
            )
            if value:
                direction[pivot] = value
        answer[target] = direction

    for target, direction in answer.items():
        for pivot, (row, _representative) in reducer.jacobian_pivots.items():
            value = sum(
                coefficient * direction.get(coordinate, QQ(0))
                for coordinate, coefficient in row.items()
            )
            require(
                value == QQ(1 if pivot == target else 0),
                f"normal direction {target} is not dual at pivot {pivot}",
            )
    return answer


def weighted_normal_direction(reducer):
    """Polynomial ambient vector sum_p Q_p^(2)|P5 * d_p."""

    directions = normal_directions(reducer)
    answer = {}
    active_pivots = 0
    quadratic_terms = 0
    for pivot, direction in directions.items():
        quadratic = P5.p5_restriction(
            reducer.tangent_restriction(
                reducer.functional_hasse(
                    reducer.jacobian_functional(pivot), 2
                )
            )
        )
        if not quadratic:
            continue
        active_pivots += 1
        quadratic_terms += len(quadratic)
        for coordinate, coefficient in direction.items():
            if coordinate not in answer:
                answer[coordinate] = {}
            add(answer[coordinate], quadratic, coefficient)
            if not answer[coordinate]:
                answer.pop(coordinate)
    return answer, {
        "normal_directions": len(directions),
        "normal_direction_nonzeros": sum(map(len, directions.values())),
        "maximum_normal_direction_nonzeros": max(
            map(len, directions.values())
        ),
        "active_quadratic_pivots": active_pivots,
        "active_quadratic_terms": quadratic_terms,
        "weighted_ambient_coordinates": len(answer),
        "weighted_direction_terms": sum(map(len, answer.values())),
    }


class FactorizedP5Projector:
    def __init__(self, reducer):
        self.reducer = reducer
        self.weighted_direction, self.direction_ledger = (
            weighted_normal_direction(reducer)
        )
        self.restriction_cache = {}
        self.derivative_cache = {}
        self.functional_restriction_cache = {}
        self.functional_derivative_cache = {}

    def restrict(self, source):
        key = id(source)
        if key not in self.restriction_cache:
            self.restriction_cache[key] = P5.p5_restriction(
                self.reducer.tangent_restriction(source)
            )
        return self.restriction_cache[key]

    def weighted_derivative(self, source):
        key = id(source)
        if key in self.derivative_cache:
            return self.derivative_cache[key]

        ambient_derivatives = {}
        for source_monomial, coefficient in source.items():
            for coordinate in set(source_monomial):
                if coordinate not in self.weighted_direction:
                    continue
                multiplicity = source_monomial.count(coordinate)
                output = list(source_monomial)
                output.remove(coordinate)
                output = tuple(output)
                if coordinate not in ambient_derivatives:
                    ambient_derivatives[coordinate] = {}
                target = ambient_derivatives[coordinate]
                target[output] = (
                    target.get(output, QQ(0))
                    + coefficient * multiplicity
                )

        answer = {}
        for coordinate, derivative in ambient_derivatives.items():
            restricted = P5.p5_restriction(
                self.reducer.tangent_restriction(derivative)
            )
            if restricted:
                add(
                    answer,
                    multiply(restricted, self.weighted_direction[coordinate]),
                )
        self.derivative_cache[key] = answer
        return answer

    def functional_factors(self, functional, degree):
        key = tuple(sorted(functional.items())), degree
        if key not in self.functional_restriction_cache:
            ambient = self.reducer.functional_hasse(functional, degree)
            self.functional_restriction_cache[key] = self.restrict(ambient)
            self.functional_derivative_cache[key] = (
                self.weighted_derivative(ambient)
            )
        return (
            self.functional_restriction_cache[key],
            self.functional_derivative_cache[key],
        )

    def residual_projection(self, state, degree, differentiate=False):
        """P5 restriction or weighted first normal derivative of a residual."""

        if degree <= 4:
            ambient = self.reducer.functional_hasse(
                state["functional"], degree
            )
            answer = (
                self.weighted_derivative(ambient)
                if differentiate else self.restrict(ambient)
            )
            answer = dict(answer)
        else:
            answer = {}

        contributing = 0
        for multiplier, functional in state["corrections"]:
            multiplier_degree = len(next(iter(multiplier)))
            equation_degree = degree - multiplier_degree
            if not 0 <= equation_degree <= 4:
                continue
            contributing += 1
            multiplier_value = self.restrict(multiplier)
            equation_value, equation_derivative = self.functional_factors(
                functional, equation_degree
            )
            if differentiate:
                multiplier_derivative = self.weighted_derivative(multiplier)
                if multiplier_derivative and equation_value:
                    add(
                        answer,
                        multiply(multiplier_derivative, equation_value),
                        -1,
                    )
                if multiplier_value and equation_derivative:
                    add(
                        answer,
                        multiply(multiplier_value, equation_derivative),
                        -1,
                    )
            elif multiplier_value and equation_value:
                add(
                    answer,
                    multiply(multiplier_value, equation_value),
                    -1,
                )
        return answer, contributing


def mixed_tail_data():
    series = LIFTED.NormalObstructionSeries()
    projector = FactorizedP5Projector(series.reducer)

    # Validate the quotient-as-normal-derivative identity one order earlier.
    degree_five_regression_terms = 0
    degree_six = []
    degree_seven = []
    degree_six_terms = 0
    degree_seven_old_terms = 0
    degree_six_derivative_terms = 0
    contributing_degree_six = 0
    contributing_degree_seven = 0
    for number in range(1, 40):
        series.part(number, 3)
        state = series._state(number)
        old_degree_four, _count = projector.residual_projection(state, 4)
        old_degree_five, _count = projector.residual_projection(state, 5)
        degree_four_derivative, _count = projector.residual_projection(
            state, 4, differentiate=True
        )
        predicted_degree_five = dict(old_degree_five)
        add(predicted_degree_five, degree_four_derivative, -1)

        actual_degree_five = P5.p5_restriction(series.part(number, 5))
        require(
            predicted_degree_five == actual_degree_five,
            f"Q{number}: weighted quotient regression failed at degree five",
        )
        degree_five_regression_terms += len(actual_degree_five)

        state = series._state(number)
        old_degree_six, count6 = projector.residual_projection(state, 6)
        old_degree_seven, count7 = projector.residual_projection(state, 7)
        degree_six_derivative, _count = projector.residual_projection(
            state, 6, differentiate=True
        )
        answer = dict(old_degree_seven)
        add(answer, degree_six_derivative, -1)
        degree_six.append(old_degree_six)
        degree_seven.append(answer)
        degree_six_terms += len(old_degree_six)
        degree_seven_old_terms += len(old_degree_seven)
        degree_six_derivative_terms += len(degree_six_derivative)
        contributing_degree_six += count6
        contributing_degree_seven += count7

    ledger = {
        "branch": "P5",
        "p5_free_parameters": 45,
        "mixed_equations": 39,
        "normal_direction_contraction": projector.direction_ledger,
        "degree_five_regression_terms": degree_five_regression_terms,
        "degree_six_restricted_residual_terms": degree_six_terms,
        "degree_seven_old_restricted_terms": degree_seven_old_terms,
        "degree_six_weighted_derivative_terms": degree_six_derivative_terms,
        "degree_seven_final_terms": sum(map(len, degree_seven)),
        "degree_seven_nonzero_equations": sum(bool(item) for item in degree_seven),
        "degree_seven_maximum_terms": max(map(len, degree_seven)),
        "contributing_corrections_degree_six": contributing_degree_six,
        "contributing_corrections_degree_seven": contributing_degree_seven,
        "restriction_cache_entries": len(projector.restriction_cache),
        "weighted_derivative_cache_entries": len(projector.derivative_cache),
        "scope_guard": (
            "these are the 39 mixed degree-seven tails after ambient normal "
            "elimination on P5; P5 Hensel/component reduction and the next "
            "pure H0/H1 normal forms are separate steps"
        ),
    }
    return {
        "series": series,
        "projector": projector,
        "degree_six": degree_six,
        "degree_seven": degree_seven,
        "ledger": ledger,
    }


def audit():
    data = mixed_tail_data()
    ledger = data["ledger"]
    encoded_polynomials = []
    for polynomial in data["degree_seven"]:
        encoded_polynomials.append([
            [
                list(monomial), coefficient.numerator, coefficient.denominator
            ]
            for monomial, coefficient in sorted(polynomial.items())
        ])
    polynomial_payload = json.dumps(
        encoded_polynomials, separators=(",", ":")
    )
    ledger["degree_seven_polynomial_sha256"] = sha256(
        polynomial_payload.encode()
    ).hexdigest()
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    require(digest == EXPECTED_LEDGER_SHA256,
            "P5 degree-seven mixed-tail ledger changed")
    print(json.dumps(ledger, indent=2, sort_keys=True))
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    audit()
