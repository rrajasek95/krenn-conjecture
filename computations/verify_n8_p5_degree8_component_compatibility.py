#!/usr/bin/env python3
"""Verify next P5 compatibility on two components and an exact L point."""

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


DEG8 = load_module(
    "n8_p5_degree8_for_components",
    "verify_n8_p5_streamed_degree8_mixed_tails.py",
)
COMPAT = load_module(
    "n8_p5_degree7_compatibility_for_degree8",
    "analyze_n8_p5_degree7_compatibility_tails.py",
)
P5 = DEG8.P5
CUBIC = P5.CUBIC
QQ = Fraction

EXPECTED_LEDGER_SHA256 = (
    "7a460d5d9223327e40a657d9236592dd7f2df0c13fd08009627ff9d9bc36c7b7"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def add(target, source, scale=QQ(1)):
    CUBIC.add_scaled(target, source, scale)


def multiply(left, right):
    return CUBIC.multiply_polynomials(left, right)


def polynomial_list_digest(sources):
    encoded = [[
        [list(monomial), coefficient.numerator, coefficient.denominator]
        for monomial, coefficient in sorted(source.items())
    ] for source in sources]
    return sha256(json.dumps(encoded, separators=(",", ":")).encode()).hexdigest()


def correction_digest(corrections):
    encoded = [[
        coordinate,
        [[list(monomial), coefficient.numerator, coefficient.denominator]
         for monomial, coefficient in sorted(value.items())],
    ] for correction in corrections
        for coordinate, value in sorted(correction.items())]
    return sha256(json.dumps(encoded, separators=(",", ":")).encode()).hexdigest()


def restrict_zero(source, variable):
    return {
        monomial: coefficient
        for monomial, coefficient in source.items()
        if variable not in monomial
    }


def restrict_correction(correction, variable):
    answer = {}
    for coordinate, value in correction.items():
        restricted = restrict_zero(value, variable)
        if restricted:
            answer[coordinate] = restricted
    return answer


class StrictJetProjector:
    """Bigraded ambient-normal/P5-strict jets through bidegree (2, 2)."""

    def __init__(self, second, corrections):
        self.second = second
        self.base = second.base
        self.reducer = second.reducer
        self.corrections = corrections
        self.source_cache = {}
        self.functional_cache = {}
        self.w_full = self.full_first_normal_direction()
        self.w_arc_one = {
            coordinate: P5.coefficient_on_p5_arc(
                value, corrections, 1
            )
            for coordinate, value in self.w_full.items()
        }

    def full_first_normal_direction(self):
        answer = {}
        dual = DEG8.TAILS.normal_directions(self.reducer)
        for pivot, direction in dual.items():
            functional = self.reducer.jacobian_functional(pivot)
            quadratic = self.reducer.tangent_restriction(
                self.reducer.functional_hasse(functional, 2)
            )
            if not quadratic:
                continue
            for coordinate, coefficient in direction.items():
                target = answer.setdefault(coordinate, {})
                add(target, quadratic, coefficient)
                if not target:
                    answer.pop(coordinate)
        for coordinate, value in answer.items():
            require(
                P5.p5_restriction(value)
                == self.base.weighted_direction.get(coordinate, {}),
                f"full first normal direction changed at {coordinate}",
            )
        return answer

    @staticmethod
    def cached(cache, source, calculate):
        key = id(source)
        if key not in cache:
            cache[key] = (source, calculate())
        cached_source, answer = cache[key]
        require(cached_source is source, "strict-jet cache identity collision")
        return answer

    def base_arc(self, source):
        tangent = self.reducer.tangent_restriction(source)
        return [
            P5.coefficient_on_p5_arc(tangent, self.corrections, order)
            for order in range(3)
        ]

    def first_normal_arc(self, source):
        derivatives = {}
        active = set(self.w_full)
        for monomial, coefficient in source.items():
            for coordinate in set(monomial) & active:
                output = list(monomial)
                output.remove(coordinate)
                target = derivatives.setdefault(coordinate, {})
                add(target, {
                    tuple(output): coefficient * monomial.count(coordinate)
                })
        answer = [{}, {}]
        for coordinate, derivative in derivatives.items():
            tangent = self.reducer.tangent_restriction(derivative)
            derivative_arc = [
                P5.coefficient_on_p5_arc(
                    tangent, self.corrections, order
                )
                for order in range(2)
            ]
            w_arc = [self.base.weighted_direction.get(coordinate, {}),
                     self.w_arc_one[coordinate]]
            if derivative_arc[0] and w_arc[0]:
                add(answer[0], multiply(derivative_arc[0], w_arc[0]), -1)
            if derivative_arc[1] and w_arc[0]:
                add(answer[1], multiply(derivative_arc[1], w_arc[0]), -1)
            if derivative_arc[0] and w_arc[1]:
                add(answer[1], multiply(derivative_arc[0], w_arc[1]), -1)
        return answer

    def source_jets(self, source):
        def calculate():
            base = self.base_arc(source)
            first = self.first_normal_arc(source)
            second = dict(self.second.n2_derivative(source))
            add(second, self.second.second_w_coefficient(source))
            return base, first, second

        return self.cached(self.source_cache, source, calculate)

    def functional_jets(self, functional, degree):
        key = tuple(sorted(functional.items())), degree
        if key not in self.functional_cache:
            ambient = self.reducer.functional_hasse(functional, degree)
            self.functional_cache[key] = self.source_jets(ambient)
        return self.functional_cache[key]

    @staticmethod
    def product_jets(left, right):
        lb, lc, ld = left
        rb, rc, rd = right
        base = [{}, {}, {}]
        first = [{}, {}]
        second = {}
        for total in range(3):
            for order in range(total + 1):
                if lb[order] and rb[total - order]:
                    add(base[total], multiply(lb[order], rb[total - order]))
        if lc[0] and rb[0]:
            add(first[0], multiply(lc[0], rb[0]))
        if lb[0] and rc[0]:
            add(first[0], multiply(lb[0], rc[0]))
        for left_value, right_value in (
            (lc[1], rb[0]), (lc[0], rb[1]),
            (lb[1], rc[0]), (lb[0], rc[1]),
        ):
            if left_value and right_value:
                add(first[1], multiply(left_value, right_value))
        for left_value, right_value in (
            (ld, rb[0]), (lb[0], rd), (lc[0], rc[0]),
        ):
            if left_value and right_value:
                add(second, multiply(left_value, right_value))
        return base, first, second

    def residual_jets(self, state, degree):
        if degree <= 4:
            result = tuple(
                [dict(value) for value in group] if isinstance(group, list)
                else dict(group)
                for group in self.functional_jets(state["functional"], degree)
            )
        else:
            result = ([{}, {}, {}], [{}, {}], {})
        base, first, second = result
        for multiplier, functional in state["corrections"]:
            multiplier_degree = len(next(iter(multiplier)))
            equation_degree = degree - multiplier_degree
            if not 0 <= equation_degree <= 4:
                continue
            product = self.product_jets(
                self.source_jets(multiplier),
                self.functional_jets(functional, equation_degree),
            )
            for order in range(3):
                add(base[order], product[0][order], -1)
            for order in range(2):
                add(first[order], product[1][order], -1)
            add(second, product[2], -1)
        return base, first, second

    def higher_strict_orders(self, state):
        six = self.residual_jets(state, 6)
        seven = self.residual_jets(state, 7)
        eight = self.residual_jets(state, 8)
        order_five = dict(six[0][1])
        add(order_five, seven[0][0])
        add(order_five, six[1][0])
        order_six = dict(six[0][2])
        add(order_six, seven[0][1])
        add(order_six, six[1][1])
        add(order_six, eight[0][0])
        add(order_six, seven[1][0])
        add(order_six, six[2])
        return order_five, order_six


def normalized_compatibility(residual, jacobian):
    b = P5.polynomial((((44,), 1), ((45,), 1)))
    pivots = [residual[row] for row in P5.B_PIVOT_ROWS]
    answer = []
    for equation, row in enumerate(jacobian):
        value = multiply(b, residual[equation])
        for column in range(11):
            if row[column] and pivots[column]:
                add(value, multiply(row[column], pivots[column]), -1)
        answer.append(COMPAT.divide_by_b(value) if value else {})
    return answer


def constant_polynomial(value):
    return {(): value} if value else {}


def evaluate_correction(correction, point):
    return {
        coordinate: constant_polynomial(COMPAT.evaluate(value, point))
        for coordinate, value in correction.items()
        if COMPAT.evaluate(value, point)
    }


def solve_transverse_at_point(residual, jacobian, point, detail):
    values = [COMPAT.evaluate(value, point) for value in residual]
    b_value = point[44] + point[45]
    require(b_value, f"{detail}: left the b chart")
    correction = {}
    for coordinate, row in zip(P5.P5_NORMAL_VARIABLES, P5.B_PIVOT_ROWS):
        value = -values[row] / b_value
        if value:
            correction[coordinate] = constant_polynomial(value)
    correction_values = {
        coordinate: value.get((), QQ(0))
        for coordinate, value in correction.items()
    }
    remaining = []
    for equation, row in enumerate(jacobian):
        value = values[equation]
        for column, coordinate in enumerate(P5.P5_NORMAL_VARIABLES):
            value += COMPAT.evaluate(row[column], point) * (
                correction_values.get(coordinate, QQ(0))
            )
        if value:
            remaining.append((equation + 1, value))
    return correction, remaining


def generic_L_point_data(
    degree8, compatibility, second_free_bend=None
):
    point = {index: QQ(index + 2) for index in range(56)}
    for variable in P5.P5_NORMAL_VARIABLES:
        point[variable] = QQ(0)
    point[15] = point[16]
    point[46] = point[9] * point[25] / point[11]
    require(point[9] * point[25] - point[11] * point[46] == 0,
            "deterministic point missed L=0")

    h30 = compatibility["normalized_compatibility"][29]
    h30_value = COMPAT.evaluate(h30, point)
    c_value = point[16] ** 2 * point[41]
    u_value = point[26] + point[45]
    s46 = -2 * h30_value / (c_value * u_value * point[11])

    corrections = []
    c1 = evaluate_correction(compatibility["corrections"][0], point)
    c1[46] = constant_polynomial(s46)
    corrections.append(c1)
    parts = compatibility["parts"]
    jacobian = compatibility["jacobian"]

    residual1 = P5.strict_residual(parts, [], 1)
    _check_c1, remaining1 = solve_transverse_at_point(
        residual1, jacobian, point, "L point order one"
    )
    # The pivot solution at order one is unique; add only the chosen free bend.
    require(
        evaluate_correction(compatibility["corrections"][0], point)
        == _check_c1,
        "L point order-one transverse correction changed",
    )
    require(not remaining1, "L point failed at strict order one")

    for order in (2, 3):
        residual = P5.strict_residual(parts, corrections, order)
        next_correction, remaining = solve_transverse_at_point(
            residual, jacobian, point, f"L point order {order}"
        )
        require(not remaining, f"L point failed at strict order {order}")
        if order == 2 and second_free_bend:
            next_correction[46] = constant_polynomial(second_free_bend)
        corrections.append(next_correction)

    residual4 = P5.strict_residual(parts, corrections, 4)
    for equation in range(39):
        add(
            residual4[equation],
            degree8["degree_seven_data"]["degree_six"][equation],
        )
    c4, remaining4 = solve_transverse_at_point(
        residual4, jacobian, point, "L point order four"
    )
    require(not remaining4, "L point failed at strict order four")
    corrections.append(c4)

    strict = StrictJetProjector(degree8["second_projector"], corrections[:2])
    higher_five = []
    higher_six = []
    series = degree8["degree_seven_data"]["series"]
    for number in range(1, 40):
        five, six = strict.higher_strict_orders(series._state(number))
        higher_five.append(five)
        higher_six.append(six)

    residual5 = P5.strict_residual(parts, corrections, 5)
    for equation in range(39):
        add(residual5[equation], higher_five[equation])
    c5, remaining5 = solve_transverse_at_point(
        residual5, jacobian, point, "L point order five"
    )
    require(not remaining5, f"L point failed at strict order five: {remaining5}")
    corrections.append(c5)

    residual6 = P5.strict_residual(parts, corrections, 6)
    for equation in range(39):
        add(residual6[equation], higher_six[equation])
    c6, remaining6 = solve_transverse_at_point(
        residual6, jacobian, point, "L point order six"
    )
    if remaining6 and second_free_bend is None:
        require(
            [equation for equation, _value in remaining6] == [30, 33],
            "L point acquired an unexpected order-six compatibility",
        )
        values = dict(remaining6)
        second_free_bend = (
            -2 * values[30] / (c_value * u_value * point[11])
        )
        v_value = point[26] - point[44]
        require(
            values[33]
            + QQ(1, 2) * c_value * v_value * point[11]
            * second_free_bend == 0,
            "L point order-six exceptional pair has inconsistent ratio",
        )
        return generic_L_point_data(
            degree8, compatibility, second_free_bend
        )
    require(not remaining6, "bent L point failed at strict order six")
    raw30 = -QQ(1, 2) * c_value * u_value * point[11] * second_free_bend
    v_value = point[26] - point[44]
    raw33 = -QQ(1, 2) * c_value * v_value * point[11] * second_free_bend
    require(
        (raw30, raw33) == (QQ(-165689793000), QQ(39765550320)),
        "deterministic L point raw exceptional pair changed",
    )
    return {
        "base_point": [
            [index, value.numerator, value.denominator]
            for index, value in sorted(point.items())
        ],
        "first_free_bend_z46": [s46.numerator, s46.denominator],
        "raw_order_six_compatibility": [
            [30, raw30.numerator, raw30.denominator],
            [33, raw33.numerator, raw33.denominator],
        ],
        "raw_exceptional_ratio": "u:v=-25:6",
        "second_free_bend_z46": [
            second_free_bend.numerator, second_free_bend.denominator
        ],
        "correction_nonzeros_orders_one_to_five": [
            len(value) for value in corrections
        ],
        "corrections_sha256": correction_digest(corrections),
        "strict_order_six_compatibility_after_bend": remaining6,
        "order_six_transverse_correction_nonzeros": len(c6),
        "order_six_transverse_correction_sha256": correction_digest([c6]),
        "scope": (
            "one exact rational point on the generic L open chart; not a "
            "symbolic all-point L-component compatibility identity"
        ),
    }


def component_data(variable, degree8, compatibility, strict, higher_six):
    series = degree8["degree_seven_data"]["series"]
    parts = compatibility["parts"]
    jacobian = [
        [restrict_zero(entry, variable) for entry in row]
        for row in compatibility["jacobian"]
    ]
    corrections = compatibility["corrections"]
    n4 = compatibility["n4"]

    residual5 = [restrict_zero(value, variable)
                 for value in compatibility["residual5"]]
    require(not any(normalized_compatibility(residual5, jacobian)),
            f"z{variable}: degree-seven compatibility no longer vanishes")
    n5 = {}
    for coordinate, incoming in zip(
        P5.P5_NORMAL_VARIABLES,
        (residual5[row] for row in P5.B_PIVOT_ROWS),
    ):
        if incoming:
            quotient = COMPAT.divide_by_b(incoming)
            n5[coordinate] = {
                monomial: -coefficient
                for monomial, coefficient in quotient.items()
            }

    component_corrections = [
        restrict_correction(value, variable)
        for value in corrections + [n4, n5]
    ]
    residual6 = [
        restrict_zero(value, variable)
        for value in P5.strict_residual(parts, component_corrections, 6)
    ]
    for equation in range(39):
        add(residual6[equation], restrict_zero(higher_six[equation], variable))
    compat6 = normalized_compatibility(residual6, jacobian)
    nonzero_compatibility = [
        (index + 1, len(value))
        for index, value in enumerate(compat6) if value
    ]
    require(not nonzero_compatibility,
            f"z{variable}: acquired strict-order-six compatibility")
    return {
        "component": f"z{variable}=0",
        "n5_nonzero_corrections": len(n5),
        "n5_terms": sum(map(len, n5.values())),
        "n5_sha256": correction_digest([n5]),
        "strict_order_six_residual_terms": sum(map(len, residual6)),
        "strict_order_six_residual_maximum_terms": max(map(len, residual6)),
        "strict_order_six_residual_sha256": polynomial_list_digest(residual6),
        "strict_order_six_compatibility": nonzero_compatibility,
    }


def audit():
    degree8 = DEG8.degree_eight_tail_data()
    compatibility = COMPAT.compatibility_tail_data(
        False, degree8["degree_seven_data"]
    )
    corrections = compatibility["corrections"]
    strict = StrictJetProjector(
        degree8["second_projector"], corrections[:2]
    )
    higher_six = []
    for number in range(1, 40):
        five, six = strict.higher_strict_orders(
            degree8["degree_seven_data"]["series"]._state(number)
        )
        higher_six.append(six)
        expected_five = dict(compatibility["q6_n1"][number - 1])
        add(expected_five,
            degree8["degree_seven_data"]["degree_seven"][number - 1])
        require(five == expected_five,
                f"Q{number}: prior strict-order-five regression failed")
    z16 = component_data(16, degree8, compatibility, strict, higher_six)
    z41 = component_data(41, degree8, compatibility, strict, higher_six)
    L_point = generic_L_point_data(
        degree8, compatibility, QQ(317140, 13)
    )
    ledger = {
        "branch": "P5",
        "chart": "b=z44+z45 != 0",
        "mixed_equations": 39,
        "degree_eight_mixed_tail_polynomial_sha256": (
            "bc9606f71e37b99007626e90583b204cc0d2b388a92854ffbf2b5145d2c3d1d9"
        ),
        "prior_strict_order_five_regression_polynomials": 39,
        "symbolic_components": [z16, z41],
        "L_component_exact_point": L_point,
        "verdict": (
            "z16=0 and z41=0 lift symbolically through strict order six; "
            "one exact generic L point lifts through strict order six after "
            "two free bends"
        ),
        "scope_guard": (
            "the full generic L component has not been reduced symbolically, "
            "and no next pure H0/H1 coefficient is certified here"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "P5 degree-eight component ledger changed")
    print(json.dumps(ledger, indent=2, sort_keys=True))
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    audit()
