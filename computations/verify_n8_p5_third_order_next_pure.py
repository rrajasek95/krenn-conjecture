#!/usr/bin/env python3
"""Compute the third-normal component-local P5 pure coefficients."""

from fractions import Fraction
from hashlib import sha256
from itertools import combinations_with_replacement
import importlib.util
import json
from math import comb
from pathlib import Path


HERE = Path(__file__).resolve().parent


def load_module(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


NEXT = load_module(
    "n8_p5_next_pure_for_third_order",
    "verify_n8_p5_component_local_next_pure.py",
)
COMPONENT = NEXT.COMPONENT
DEG8 = NEXT.DEG8
P5 = NEXT.P5
CUBIC = NEXT.CUBIC
PURE = NEXT.PURE
QQ = Fraction

EXPECTED_LEDGER_SHA256 = (
    "320eabea4a02e275a732589c07eb2091008d97716e95474b5e75060699a8f400"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def add(target, source, scale=QQ(1)):
    CUBIC.add_scaled(target, source, scale)


def multiply(left, right):
    return CUBIC.multiply_polynomials(left, right)


def polynomial_digest(source):
    return PURE.polynomial_digest(source)


def negate(source):
    return {monomial: -coefficient for monomial, coefficient in source.items()}


def third_normal_direction(second):
    """The fourth graph coefficient cancelling the Jacobian pivot equations."""

    reducer = second.reducer
    dual = DEG8.TAILS.normal_directions(reducer)
    answer = {}
    active = 0
    incoming_terms = 0
    for pivot, direction in dual.items():
        functional = reducer.jacobian_functional(pivot)
        quadratic = reducer.functional_hasse(functional, 2)
        cubic = reducer.functional_hasse(functional, 3)
        quartic = reducer.functional_hasse(functional, 4)
        incoming = dict(second.base.restrict(quartic))
        add(incoming, second.base.weighted_derivative(cubic), -1)
        add(incoming, second.n2_derivative(quadratic))
        add(incoming, second.second_w_coefficient(quadratic))
        if not incoming:
            continue
        active += 1
        incoming_terms += len(incoming)
        for coordinate, coefficient in direction.items():
            target = answer.setdefault(coordinate, {})
            add(target, incoming, -coefficient)
            if not target:
                answer.pop(coordinate)
    return answer, {
        "active_third_order_pivots": active,
        "incoming_third_order_terms": incoming_terms,
        "third_order_ambient_coordinates": len(answer),
        "third_order_direction_terms": sum(map(len, answer.values())),
    }


class ThirdOrderProjector:
    """Normal-graph Taylor coefficients through order three."""

    def __init__(self, reducer):
        self.second = DEG8.SecondOrderProjector(
            DEG8.TAILS.FactorizedP5Projector(reducer)
        )
        self.base = self.second.base
        self.reducer = reducer
        self.w = self.second.w
        self.n2 = self.second.n2
        self.n3, self.direction_ledger = third_normal_direction(self.second)
        self.n3_cache = {}
        self.mixed_cache = {}
        self.third_w_cache = {}
        self.coefficient_cache = {}
        self.functional_cache = {}

    @staticmethod
    def cached(cache, source, calculate):
        key = id(source)
        if key not in cache:
            cache[key] = (source, calculate())
        cached_source, answer = cache[key]
        require(cached_source is source, "third-order cache identity collision")
        return answer

    def n3_derivative(self, source):
        return self.second.directional(source, self.n3, self.n3_cache)

    def mixed_w_n2_coefficient(self, source):
        """Return D_w D_n2(source), with no Taylor sign."""

        def calculate():
            answer = {}
            active_w = set(self.w)
            active_n2 = set(self.n2)
            for monomial, coefficient in source.items():
                counts = {coordinate: monomial.count(coordinate)
                          for coordinate in set(monomial)}
                for left in sorted(set(monomial) & active_w):
                    for right in sorted(set(monomial) & active_n2):
                        multiplicity = counts[left] * (
                            counts[right] - (1 if left == right else 0)
                        )
                        if not multiplicity:
                            continue
                        output = list(monomial)
                        output.remove(left)
                        output.remove(right)
                        derivative = {tuple(output): coefficient * multiplicity}
                        restricted = P5.p5_restriction(
                            self.reducer.tangent_restriction(derivative)
                        )
                        if not restricted:
                            continue
                        term = multiply(restricted, self.w[left])
                        term = multiply(term, self.n2[right])
                        add(answer, term)
            return answer

        return self.cached(self.mixed_cache, source, calculate)

    def third_w_coefficient(self, source):
        """Return the coefficient (1/6) D_w^3(source)."""

        def calculate():
            answer = {}
            active = set(self.w)
            for monomial, coefficient in source.items():
                counts = {coordinate: monomial.count(coordinate)
                          for coordinate in set(monomial)}
                coordinates = sorted(set(monomial) & active)
                for selected in combinations_with_replacement(coordinates, 3):
                    chosen = {coordinate: selected.count(coordinate)
                              for coordinate in set(selected)}
                    if any(chosen[coordinate] > counts[coordinate]
                           for coordinate in chosen):
                        continue
                    multiplicity = 1
                    output = list(monomial)
                    for coordinate, amount in chosen.items():
                        multiplicity *= comb(counts[coordinate], amount)
                        for _index in range(amount):
                            output.remove(coordinate)
                    restricted = P5.p5_restriction(
                        self.reducer.tangent_restriction({
                            tuple(output): coefficient * multiplicity
                        })
                    )
                    if not restricted:
                        continue
                    term = restricted
                    for coordinate in selected:
                        term = multiply(term, self.w[coordinate])
                    add(answer, term)
            return answer

        return self.cached(self.third_w_cache, source, calculate)

    def coefficients(self, source):
        def calculate():
            c0 = dict(self.base.restrict(source))
            c1 = negate(self.base.weighted_derivative(source))
            c2 = dict(self.second.n2_derivative(source))
            add(c2, self.second.second_w_coefficient(source))
            c3 = dict(self.n3_derivative(source))
            add(c3, self.mixed_w_n2_coefficient(source), -1)
            add(c3, self.third_w_coefficient(source), -1)
            return c0, c1, c2, c3

        return self.cached(self.coefficient_cache, source, calculate)

    def functional_coefficients(self, functional, degree):
        key = tuple(sorted(functional.items())), degree
        if key not in self.functional_cache:
            ambient = self.reducer.functional_hasse(functional, degree)
            self.functional_cache[key] = self.coefficients(ambient)
        return self.functional_cache[key]

    def residual_coefficients(self, reducer, pure, degree):
        if degree <= 4:
            result = [
                dict(value) for value in self.coefficients(
                    CUBIC.hasse_form(pure, degree)
                )
            ]
        else:
            result = [{}, {}, {}, {}]
        for correction in reducer.corrections:
            equation_degree = degree - correction["degree"]
            if not 0 <= equation_degree <= 4:
                continue
            multiplier = self.coefficients(correction["multiplier"])
            equation = self.functional_coefficients(
                correction["functional"], equation_degree
            )
            for total in range(4):
                for order in range(total + 1):
                    if multiplier[order] and equation[total - order]:
                        add(
                            result[total],
                            multiply(multiplier[order], equation[total - order]),
                            -1,
                        )
        return result


class ThirdStrictProjector:
    """Full tangent-polynomial normal/strict jets of total order three."""

    def __init__(self, third, corrections):
        self.third = third
        self.second = third.second
        self.reducer = third.reducer
        self.corrections = corrections
        prior = COMPONENT.StrictJetProjector(
            third.second, corrections[:2]
        )
        self.w_full = prior.w_full
        self.n2_full = self.full_second_normal_direction()
        self.directional_cache = {}
        self.second_w_cache = {}
        self.source_cache = {}
        self.functional_cache = {}

    @staticmethod
    def cached(cache, source, calculate):
        key = id(source)
        if key not in cache:
            cache[key] = (source, calculate())
        cached_source, answer = cache[key]
        require(cached_source is source,
                "third-strict cache identity collision")
        return answer

    def full_directional_uncached(self, source, direction):
        ambient = {}
        active = set(direction)
        for monomial, coefficient in source.items():
            for coordinate in set(monomial) & active:
                output = list(monomial)
                output.remove(coordinate)
                target = ambient.setdefault(coordinate, {})
                add(target, {
                    tuple(output): coefficient * monomial.count(coordinate)
                })
        answer = {}
        for coordinate, derivative in ambient.items():
            tangent = self.reducer.tangent_restriction(derivative)
            if tangent:
                add(answer, multiply(tangent, direction[coordinate]))
        return answer

    def full_directional(self, source, direction, label):
        key = label, id(source)
        if key not in self.directional_cache:
            self.directional_cache[key] = (
                source, self.full_directional_uncached(source, direction)
            )
        cached_source, answer = self.directional_cache[key]
        require(cached_source is source,
                "third-strict directional cache identity collision")
        return answer

    def full_second_normal_direction(self):
        dual = DEG8.TAILS.normal_directions(self.reducer)
        answer = {}
        for pivot, direction in dual.items():
            functional = self.reducer.jacobian_functional(pivot)
            quadratic = self.reducer.functional_hasse(functional, 2)
            cubic = self.reducer.functional_hasse(functional, 3)
            incoming = dict(self.reducer.tangent_restriction(cubic))
            add(
                incoming,
                self.full_directional_uncached(quadratic, self.w_full),
                -1,
            )
            if not incoming:
                continue
            for coordinate, coefficient in direction.items():
                target = answer.setdefault(coordinate, {})
                add(target, incoming, -coefficient)
                if not target:
                    answer.pop(coordinate)
        for coordinate, value in answer.items():
            require(P5.p5_restriction(value)
                    == self.third.n2.get(coordinate, {}),
                    f"full second normal direction changed at {coordinate}")
        return answer

    def full_second_w_coefficient(self, source):
        def calculate():
            ambient = {}
            active = set(self.w_full)
            for monomial, coefficient in source.items():
                counts = {
                    coordinate: monomial.count(coordinate)
                    for coordinate in set(monomial) & active
                }
                coordinates = sorted(counts)
                for position, left in enumerate(coordinates):
                    if counts[left] >= 2:
                        output = list(monomial)
                        output.remove(left)
                        output.remove(left)
                        target = ambient.setdefault((left, left), {})
                        add(target, {
                            tuple(output): coefficient
                            * comb(counts[left], 2)
                        })
                    for right in coordinates[position + 1:]:
                        output = list(monomial)
                        output.remove(left)
                        output.remove(right)
                        target = ambient.setdefault((left, right), {})
                        add(target, {
                            tuple(output): coefficient
                            * counts[left] * counts[right]
                        })
            answer = {}
            for (left, right), derivative in ambient.items():
                tangent = self.reducer.tangent_restriction(derivative)
                if not tangent:
                    continue
                term = multiply(tangent, self.w_full[left])
                term = multiply(term, self.w_full[right])
                add(answer, term)
            return answer

        return self.cached(self.second_w_cache, source, calculate)

    def source_jets(self, source):
        def calculate():
            base_full = self.reducer.tangent_restriction(source)
            first_full = negate(self.full_directional(
                source, self.w_full, "w"
            ))
            second_full = dict(self.full_directional(
                source, self.n2_full, "n2"
            ))
            add(second_full, self.full_second_w_coefficient(source))
            third_base = dict(self.third.coefficients(source)[3])
            require(P5.p5_restriction(first_full)
                    == self.third.coefficients(source)[1],
                    "full first-normal coefficient changed")
            require(P5.p5_restriction(second_full)
                    == self.third.coefficients(source)[2],
                    "full second-normal coefficient changed")
            full = (base_full, first_full, second_full)
            answer = []
            for normal_order, value in enumerate(full):
                answer.append([
                    P5.coefficient_on_p5_arc(
                        value, self.corrections, strict_order
                    )
                    for strict_order in range(4 - normal_order)
                ])
            answer.append([third_base])
            return answer

        return self.cached(self.source_cache, source, calculate)

    def functional_jets(self, functional, degree):
        key = tuple(sorted(functional.items())), degree
        if key not in self.functional_cache:
            ambient = self.reducer.functional_hasse(functional, degree)
            self.functional_cache[key] = self.source_jets(ambient)
        return self.functional_cache[key]

    @staticmethod
    def product_jets(left, right):
        answer = [[{} for _strict in range(4 - normal)]
                  for normal in range(4)]
        for left_normal, left_group in enumerate(left):
            for right_normal, right_group in enumerate(right):
                normal = left_normal + right_normal
                if normal >= 4:
                    continue
                for left_strict, left_value in enumerate(left_group):
                    for right_strict, right_value in enumerate(right_group):
                        strict = left_strict + right_strict
                        if strict >= 4 - normal:
                            continue
                        if left_value and right_value:
                            add(answer[normal][strict],
                                multiply(left_value, right_value))
        return answer

    def residual_jets(self, reducer, pure, degree):
        if degree <= 4:
            result = [
                [dict(value) for value in group]
                for group in self.source_jets(CUBIC.hasse_form(pure, degree))
            ]
        else:
            result = [[{} for _strict in range(4 - normal)]
                      for normal in range(4)]
        for correction in reducer.corrections:
            equation_degree = degree - correction["degree"]
            if not 0 <= equation_degree <= 4:
                continue
            product = self.product_jets(
                self.source_jets(correction["multiplier"]),
                self.functional_jets(
                    correction["functional"], equation_degree
                ),
            )
            for normal, group in enumerate(product):
                for strict, value in enumerate(group):
                    add(result[normal][strict], value, -1)
        return result


def component_coefficient(strict, reducer, pure, target):
    answer = {}
    for degree in range(1, target + 1):
        jets = strict.residual_jets(reducer, pure, degree)
        for normal_order, group in enumerate(jets):
            strict_order = target - degree - normal_order
            if 0 <= strict_order < len(group):
                add(answer, group[strict_order])
    return answer


def validate_normal_graph(third):
    residual_terms = 0
    for pivot in sorted(third.reducer.jacobian_pivots):
        functional = third.reducer.jacobian_functional(pivot)
        linear = third.reducer.functional_hasse(functional, 1)
        quadratic = third.reducer.functional_hasse(functional, 2)
        cubic = third.reducer.functional_hasse(functional, 3)
        quartic = third.reducer.functional_hasse(functional, 4)
        residual = dict(third.base.restrict(quartic))
        add(residual, third.base.weighted_derivative(cubic), -1)
        add(residual, third.second.n2_derivative(quadratic))
        add(residual, third.second.second_w_coefficient(quadratic))
        add(residual, third.n3_derivative(linear))
        residual_terms += len(residual)
        require(not residual,
                f"normal graph failed at order four for pivot {pivot}")
    return residual_terms


def validate_second_order_strict_jets(strict, reducer, pure, corrections):
    third = strict.third
    old = COMPONENT.StrictJetProjector(third.second, corrections[:2])
    for degree in range(1, 10):
        expected = NEXT.pure_residual_jets(old, reducer, pure, degree)
        normal = strict.residual_jets(reducer, pure, degree)
        for order in range(3):
            require(normal[0][order] == expected[0][order],
                    f"degree {degree} base strict order {order} changed")
        for order in range(2):
            require(normal[1][order] == expected[1][order],
                    f"degree {degree} first-normal strict order {order} changed")
        require(normal[2][0] == expected[2],
                f"degree {degree} second-normal base changed")


def audit():
    compatibility = COMPONENT.COMPAT.compatibility_tail_data(False)
    corrections = compatibility["corrections"][:3]

    h1, h1_pure, _h1_terms, _h1_quotients = NEXT.h1_reducer()
    h1_third = ThirdOrderProjector(h1)
    h1_graph_residual = validate_normal_graph(h1_third)
    h1_strict = ThirdStrictProjector(h1_third, corrections)
    validate_second_order_strict_jets(
        h1_strict, h1, h1_pure, corrections
    )
    h1_degree8 = component_coefficient(
        h1_strict, h1, h1_pure, 8
    )
    expected_h1_degree8 = P5.multiply_many((
        P5.monomial(4, 16, 16, 41, 41, coefficient=2),
        P5.polynomial((((44,), 1), ((45,), 1))),
        P5.polynomial((((9, 25), 1), ((11, 46), -1))),
    ))
    require(h1_degree8 == expected_h1_degree8,
            "H1 degree-eight third-projector regression failed")
    h1_degree9 = component_coefficient(
        h1_strict, h1, h1_pure, 9
    )

    h0, h0_pure, _h0_terms, _h0_quotients, _h0_remainder = NEXT.h0_reducer()
    h0_third = ThirdOrderProjector(h0)
    h0_graph_residual = validate_normal_graph(h0_third)
    h0_strict = ThirdStrictProjector(h0_third, corrections)
    validate_second_order_strict_jets(
        h0_strict, h0, h0_pure, corrections
    )
    h0_degree9 = component_coefficient(
        h0_strict, h0, h0_pure, 9
    )
    old_h0_strict = COMPONENT.StrictJetProjector(
        h0_third.second, corrections[:2]
    )
    _h0_prior, expected_h0_degree9 = NEXT.h0_next_coefficient(
        old_h0_strict, h0, h0_pure
    )
    require(h0_degree9 == expected_h0_degree9,
            "H0 degree-nine third-projector regression failed")
    h0_degree10 = component_coefficient(
        h0_strict, h0, h0_pure, 10
    )

    ledger = {
        "branch": "P5",
        "chart": "b=z44+z45 != 0",
        "H1": {
            "normal_graph": h1_third.direction_ledger,
            "normal_graph_order_four_residual_terms": h1_graph_residual,
            "degree_eight_regression_terms": len(h1_degree8),
            "degree_nine_terms": len(h1_degree9),
            "degree_nine_sha256": polynomial_digest(h1_degree9),
            "degree_nine_component_restrictions": (
                PURE.component_flags(h1_degree9)
            ),
        },
        "H0": {
            "normal_graph": h0_third.direction_ledger,
            "normal_graph_order_four_residual_terms": h0_graph_residual,
            "degree_nine_regression_terms": len(h0_degree9),
            "degree_ten_terms": len(h0_degree10),
            "degree_ten_sha256": polynomial_digest(h0_degree10),
            "degree_ten_component_restrictions": (
                PURE.component_flags(h0_degree10)
            ),
        },
        "scope_guard": (
            "third-normal finite-order pure coefficients before the next "
            "strict mixed compatibility reduction"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "P5 third-order next-pure ledger changed")
    print(json.dumps(ledger, indent=2, sort_keys=True))
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    audit()
