#!/usr/bin/env python3
"""Stream degree-eight P5 mixed tails on the second normal graph."""

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
    "n8_p5_degree7_for_degree8_prototype",
    "verify_n8_p5_streamed_degree7_mixed_tails.py",
)
P5 = TAILS.P5
CUBIC = P5.CUBIC
QQ = Fraction

EXPECTED_LEDGER_SHA256 = (
    "13ca39b753cae39c5d36bdee7fd8ce0d5bc8822a4b7a45f1fcaad847de9e5dc3"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def add(target, source, scale=QQ(1)):
    CUBIC.add_scaled(target, source, scale)


def multiply(left, right):
    return CUBIC.multiply_polynomials(left, right)


def second_normal_direction(projector):
    """The t^3 normal coefficient on the mixed-Jacobian zero graph."""

    reducer = projector.reducer
    dual = TAILS.normal_directions(reducer)
    answer = {}
    incoming_terms = 0
    active = 0
    for pivot, direction in dual.items():
        functional = reducer.jacobian_functional(pivot)
        quadratic = reducer.functional_hasse(functional, 2)
        cubic = reducer.functional_hasse(functional, 3)
        incoming = dict(projector.restrict(cubic))
        add(incoming, projector.weighted_derivative(quadratic), -1)
        if not incoming:
            continue
        active += 1
        incoming_terms += len(incoming)
        for coordinate, coefficient in direction.items():
            if coordinate not in answer:
                answer[coordinate] = {}
            add(answer[coordinate], incoming, -coefficient)
            if not answer[coordinate]:
                answer.pop(coordinate)
    return answer, {
        "active_second_order_pivots": active,
        "incoming_second_order_terms": incoming_terms,
        "second_order_ambient_coordinates": len(answer),
        "second_order_direction_terms": sum(map(len, answer.values())),
    }


class SecondOrderProjector:
    def __init__(self, base):
        self.base = base
        self.reducer = base.reducer
        self.w = base.weighted_direction
        self.n2, self.direction_ledger = second_normal_direction(base)
        self.n2_cache = {}
        self.s2_cache = {}
        self.factor_cache = {}
        self.functional_cache = {}

    @staticmethod
    def cached(cache, source, calculate):
        key = id(source)
        if key not in cache:
            cache[key] = (source, calculate())
        cached_source, answer = cache[key]
        require(cached_source is source, "second-order cache identity collision")
        return answer

    def directional(self, source, direction, cache):
        def calculate():
            ambient = {}
            for monomial, coefficient in source.items():
                for coordinate in set(monomial):
                    if coordinate not in direction:
                        continue
                    multiplicity = monomial.count(coordinate)
                    output = list(monomial)
                    output.remove(coordinate)
                    output = tuple(output)
                    target = ambient.setdefault(coordinate, {})
                    add(target, {output: coefficient * multiplicity})
            answer = {}
            for coordinate, derivative in ambient.items():
                restricted = P5.p5_restriction(
                    self.reducer.tangent_restriction(derivative)
                )
                if restricted:
                    add(answer, multiply(restricted, direction[coordinate]))
            return answer

        return self.cached(cache, source, calculate)

    def n2_derivative(self, source):
        return self.directional(source, self.n2, self.n2_cache)

    def second_w_coefficient(self, source):
        def calculate():
            ambient = {}
            active = set(self.w)
            for monomial, coefficient in source.items():
                counts = {
                    coordinate: monomial.count(coordinate)
                    for coordinate in set(monomial) & active
                }
                coordinates = sorted(counts)
                for position, left in enumerate(coordinates):
                    left_count = counts[left]
                    if left_count >= 2:
                        output = list(monomial)
                        output.remove(left)
                        output.remove(left)
                        key = (left, left)
                        target = ambient.setdefault(key, {})
                        add(target, {
                            tuple(output): coefficient * left_count
                            * (left_count - 1) / 2
                        })
                    for right in coordinates[position + 1:]:
                        output = list(monomial)
                        output.remove(left)
                        output.remove(right)
                        key = (left, right)
                        target = ambient.setdefault(key, {})
                        add(target, {
                            tuple(output): coefficient * left_count
                            * counts[right]
                        })
            answer = {}
            for (left, right), derivative in ambient.items():
                restricted = P5.p5_restriction(
                    self.reducer.tangent_restriction(derivative)
                )
                if not restricted:
                    continue
                term = multiply(restricted, self.w[left])
                term = multiply(term, self.w[right])
                add(answer, term)
            return answer

        return self.cached(self.s2_cache, source, calculate)

    def factors(self, source):
        def calculate():
            return (
                self.base.restrict(source),
                self.base.weighted_derivative(source),
                self.n2_derivative(source),
                self.second_w_coefficient(source),
            )

        return self.cached(self.factor_cache, source, calculate)

    def functional_factors(self, functional, degree):
        key = tuple(sorted(functional.items())), degree
        if key not in self.functional_cache:
            ambient = self.reducer.functional_hasse(functional, degree)
            self.functional_cache[key] = self.factors(ambient)
        return self.functional_cache[key]

    def residual_factors(self, state, degree):
        if degree <= 4:
            answer = [
                dict(value) for value in self.functional_factors(
                    state["functional"], degree
                )
            ]
        else:
            answer = [{}, {}, {}, {}]
        contributing = 0
        for multiplier, functional in state["corrections"]:
            multiplier_degree = len(next(iter(multiplier)))
            equation_degree = degree - multiplier_degree
            if not 0 <= equation_degree <= 4:
                continue
            contributing += 1
            m0, mw, mn2, ms2 = self.factors(multiplier)
            e0, ew, en2, es2 = self.functional_factors(
                functional, equation_degree
            )
            if m0 and e0:
                add(answer[0], multiply(m0, e0), -1)
            if mw and e0:
                add(answer[1], multiply(mw, e0), -1)
            if m0 and ew:
                add(answer[1], multiply(m0, ew), -1)
            if mn2 and e0:
                add(answer[2], multiply(mn2, e0), -1)
            if m0 and en2:
                add(answer[2], multiply(m0, en2), -1)
            if ms2 and e0:
                add(answer[3], multiply(ms2, e0), -1)
            if m0 and es2:
                add(answer[3], multiply(m0, es2), -1)
            if mw and ew:
                add(answer[3], multiply(mw, ew), -1)
        return answer, contributing


def degree_eight_tail_data(verbose=False):
    data = TAILS.mixed_tail_data()
    series = data["series"]
    second = SecondOrderProjector(data["projector"])
    normal_graph_order_two_terms = 0
    normal_graph_order_three_terms = 0
    for pivot in sorted(series.reducer.jacobian_pivots):
        functional = series.reducer.jacobian_functional(pivot)
        linear = series.reducer.functional_hasse(functional, 1)
        quadratic = series.reducer.functional_hasse(functional, 2)
        cubic = series.reducer.functional_hasse(functional, 3)
        order_two = dict(second.base.restrict(quadratic))
        add(order_two, second.base.weighted_derivative(linear), -1)
        require(not order_two,
                f"normal graph failed at order two for pivot {pivot}")
        order_three = dict(second.base.restrict(cubic))
        add(order_three, second.base.weighted_derivative(quadratic), -1)
        add(order_three, second.n2_derivative(linear))
        require(not order_three,
                f"normal graph failed at order three for pivot {pivot}")
        normal_graph_order_two_terms += len(order_two)
        normal_graph_order_three_terms += len(order_three)

    totals = [0, 0, 0, 0, 0]
    maximum = 0
    degree_eight = []
    contributing_degree_eight = 0
    for number in range(1, 40):
        state = series._state(number)
        factors6, _count = second.residual_factors(state, 6)
        factors7, _count = second.residual_factors(state, 7)
        factors8, count8 = second.residual_factors(state, 8)
        regression7 = dict(factors7[0])
        add(regression7, factors6[1], -1)
        require(regression7 == data["degree_seven"][number - 1],
                f"Q{number}: degree-seven second-projector regression failed")
        answer = dict(factors8[0])
        add(answer, factors7[1], -1)
        add(answer, factors6[2])
        add(answer, factors6[3])
        degree_eight.append(answer)
        contributing_degree_eight += count8
        totals[0] += len(factors8[0])
        totals[1] += len(factors7[1])
        totals[2] += len(factors6[2])
        totals[3] += len(factors6[3])
        totals[4] += len(answer)
        maximum = max(maximum, len(answer))
        if verbose:
            print("Q", number, "terms", tuple(map(len, (
                factors8[0], factors7[1], factors6[2], factors6[3], answer,
            ))))
    ledger = {
        "branch": "P5",
        "p5_free_parameters": 45,
        "mixed_equations": 39,
        "normal_graph_second_direction": second.direction_ledger,
        "normal_graph_order_two_residual_terms": (
            normal_graph_order_two_terms
        ),
        "normal_graph_order_three_residual_terms": (
            normal_graph_order_three_terms
        ),
        "degree_seven_regression_polynomials": 39,
        "degree_eight_old_restricted_terms": totals[0],
        "degree_seven_weighted_derivative_terms": totals[1],
        "degree_six_second_direction_derivative_terms": totals[2],
        "degree_six_first_direction_square_terms": totals[3],
        "degree_eight_final_terms": totals[4],
        "degree_eight_nonzero_equations": sum(bool(item) for item in degree_eight),
        "degree_eight_maximum_terms": maximum,
        "contributing_corrections_degree_eight": contributing_degree_eight,
        "n2_derivative_cache_entries": len(second.n2_cache),
        "second_direction_square_cache_entries": len(second.s2_cache),
        "scope_guard": (
            "these are the 39 normal-eliminated mixed degree-eight tails "
            "on the full P5 branch; componentwise strict compatibility is "
            "a separate calculation"
        ),
    }
    return {
        "degree_seven_data": data,
        "second_projector": second,
        "degree_eight": degree_eight,
        "ledger": ledger,
    }


def audit():
    data = degree_eight_tail_data()
    ledger = data["ledger"]
    encoded = [[
        [list(monomial), coefficient.numerator, coefficient.denominator]
        for monomial, coefficient in sorted(polynomial.items())
    ] for polynomial in data["degree_eight"]]
    ledger["degree_eight_polynomial_sha256"] = sha256(
        json.dumps(encoded, separators=(",", ":")).encode()
    ).hexdigest()
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "P5 degree-eight mixed-tail ledger changed")
    print(json.dumps(ledger, indent=2, sort_keys=True))
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    audit()
