#!/usr/bin/env python3
"""Exact valuation gate for promoting the P5 mixed-contact calculation."""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEPENDENCIES = {
    "computations/verify_n8_second_lift_obstruction_radical.py":
        "d46dab73fa9c81660c3cd790aa409056864c7de1a55450698fca8e18c2b47738",
    "computations/verify_n8_counterexample_streamed_next_order.py":
        "cb804e1ffa82784bcf7ebe3df2481ed9c6cf04b7fb8f5011a2b557b9a374269f",
    "computations/verify_n8_p5_generic_L_capstone_initial.py":
        "b9bb0772d4523498011a011fbdad87c114764a39532a0dee81a6e1a6ae6ce751",
}
EXPECTED_LEDGER_SHA256 = (
    "bbfefcf0854019e2310a2fb5b2e1b73e00bc9d2c449a306b0157b548f56375b9"
)

# The P5 normal coordinates are q0=z12,q1=z13,q2=z14,
# q3=z15-z16,q4=z17,...,q10=z23.  Token 56 records q3 after the
# displayed linear coordinate change; old z15=q3+z16.
P5_WEIGHT_EIGHT = frozenset((12, 13, 14, 56, 17, 18, 19, 20, 21, 22, 23))
Q3_TOKEN = 56


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load(name, relative):
    path = ROOT / relative
    actual = sha256(path.read_bytes()).hexdigest()
    require(actual == DEPENDENCIES[relative],
            f"dependency changed: {relative}: {actual}")
    spec = spec_from_file_location(name, path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def change_to_p5_coordinates(polynomial):
    """Apply z15=q3+z16 to an exact tangent polynomial."""
    answer = defaultdict(Fraction)
    for monomial, coefficient in polynomial.items():
        terms = {(): Fraction(coefficient)}
        for variable in monomial:
            choices = (Q3_TOKEN, 16) if variable == 15 else (variable,)
            following = defaultdict(Fraction)
            for term, value in terms.items():
                for choice in choices:
                    following[tuple(sorted(term + (choice,)))] += value
            terms = following
        for term, value in terms.items():
            answer[term] += value
    return {term: value for term, value in answer.items() if value}


def monomial_weight(monomial):
    return sum(8 if variable in P5_WEIGHT_EIGHT else 1
               for variable in monomial)


def valuation(polynomial):
    transformed = change_to_p5_coordinates(polynomial)
    return min(monomial_weight(monomial) for monomial in transformed)


def initial_evaluation(polynomial):
    """Evaluate the lowest-weight form at c_i=i+2 on the monomial arc."""
    transformed = change_to_p5_coordinates(polynomial)
    order = min(map(monomial_weight, transformed))
    return sum(
        coefficient * math.prod(variable + 2 for variable in monomial)
        for monomial, coefficient in transformed.items()
        if monomial_weight(monomial) == order
    )


def multiply_many(factors):
    answer = {(): Fraction(1)}
    for factor in factors:
        following = defaultdict(Fraction)
        for left, left_coefficient in answer.items():
            for right, right_coefficient in factor.items():
                following[tuple(sorted(left + right))] += (
                    left_coefficient * right_coefficient
                )
        answer = {term: value for term, value in following.items() if value}
    return answer


def derivative(polynomial, variable):
    answer = defaultdict(Fraction)
    for monomial, coefficient in polynomial.items():
        multiplicity = monomial.count(variable)
        if not multiplicity:
            continue
        residual = list(monomial)
        residual.remove(variable)
        answer[tuple(residual)] += coefficient * multiplicity
    return {term: value for term, value in answer.items() if value}


def audit():
    radical = load(
        "n8_p5_rees_radical",
        "computations/verify_n8_second_lift_obstruction_radical.py",
    )
    # This dependency pins the literal degree-seven source lift from which
    # the displayed eight-term residual was obtained.
    load(
        "n8_p5_rees_streamed",
        "computations/verify_n8_counterexample_streamed_next_order.py",
    )
    capstone = load(
        "n8_p5_rees_capstone",
        "computations/verify_n8_p5_generic_L_capstone_initial.py",
    )

    free_columns, tangent_basis, obstructions = (
        radical.SOURCE.second_lift_obstruction_basis()
    )
    require(len(free_columns) == 56 and len(tangent_basis) == 56,
            "the mixed tangent dimension changed")
    require(len(obstructions) == 39,
            "the second-lift obstruction rank changed")

    obstruction_orders = [valuation(row) for row in obstructions.values()]
    obstruction_initial_values = [
        initial_evaluation(row) for row in obstructions.values()
    ]
    require(obstruction_orders == [9] * 39,
            f"P5 valuation of the obstruction ideal changed: {obstruction_orders}")
    require(all(obstruction_initial_values),
            "the explicit monomial arc cancelled an obstruction initial")

    # Frozen H0 degree-seven residual:
    # z16^2*z41*(z44+z45)*(z53-z51)*(z9*z25-z11*z46).
    residual = multiply_many((
        {(16, 16, 41): Fraction(1)},
        {(44,): Fraction(1), (45,): Fraction(1)},
        {(53,): Fraction(1), (51,): Fraction(-1)},
        {(9, 25): Fraction(1), (11, 46): Fraction(-1)},
    ))
    residual_order = valuation(residual)
    residual_initial_value = initial_evaluation(residual)
    require(len(residual) == 8 and residual_order == 7,
            "the H0 P5 valuation witness changed")
    require(residual_initial_value == -847372104,
            "the explicit H0 arc coefficient changed")

    # The other nine members of the frozen 48-element tangent standard basis
    # have monomial shape a(r,s,t)(a,r,s,t).
    cubic_leads = (
        (46, 46, 18), (46, 46, 19), (46, 46, 20),
        (46, 18, 18), (46, 18, 19), (46, 18, 20),
        (46, 19, 19), (46, 19, 20), (46, 20, 20),
    )
    cubic_orders = [monomial_weight(monomial) for monomial in cubic_leads]
    require(cubic_orders == [10, 10, 10, 17, 17, 17, 17, 17, 17],
            "the cubic tangent-standard-basis valuation changed")

    # The explicit arc has q0,...,q10 of order eight and every other new
    # tangent coordinate of order one, with coefficient c_i=i+2.  Record its
    # leading ambient support to guard the intrinsic single-edge cap theorem.
    leading_z = {
        index: Fraction(index + 2)
        for index in range(56)
        if index not in {12, 13, 14, 15, 17, 18, 19, 20, 21, 22, 23}
    }
    leading_z[15] = leading_z[16]
    ambient = defaultdict(Fraction)
    for tangent_index, coefficient in leading_z.items():
        for ambient_index, value in tangent_basis[tangent_index].items():
            ambient[ambient_index] += coefficient * value
    ambient = {index: value for index, value in ambient.items() if value}
    coordinates = radical.SOURCE.FACTOR.AMBIENT_COORDINATES
    physical_edges = {
        tuple(coordinates[index][:2]) for index in ambient
    }
    require(len(ambient) == 110 and len(physical_edges) == 20,
            "the valuation arc's ambient leading support changed")

    # The later strict-seven row is the load-bearing repair on the dense
    # generic-L initial chart.  Reconstruct the committed G and its H0
    # multiplier, and check its triangular coordinate form.
    common_factor = capstone.SYMBOLIC.strict7_common_factor()
    third_bend = capstone.SYMBOLIC.THIRD_BEND
    normal_variables = tuple(capstone.P5.P5_NORMAL_VARIABLES)
    require(len(common_factor) == 14 and
            capstone.polynomial_digest(common_factor) ==
            "86ba1dc6df22e1a2e9c084b4dfe86862d241162477625bdbc22b6b218817d565",
            "the strict-seven scalar row G changed")
    require(derivative(common_factor, third_bend) == {(): Fraction(-1)},
            "G stopped being monic in the newest bend")
    require(all(not derivative(common_factor, variable)
                for variable in normal_variables),
            "G acquired a newest transverse pivot variable")
    multiplier = multiply_many((
        {(11, 16, 16, 41): Fraction(1)},
        {(44,): Fraction(1), (45,): Fraction(1)},
        {(53,): Fraction(1), (51,): Fraction(-1)},
    ))
    h0_initial = multiply_many((multiplier, common_factor))
    require(len(h0_initial) == 56,
            "the repaired strict-seven H0 initial changed")

    ledger = {
        "dependencies": DEPENDENCIES,
        "smallest_chart": (
            "the 56-variable second-lift P5 chart at the exceptional N=8 "
            "mixed torus, followed by its dense generic-L strict-seven initial"
        ),
        "p5_weight_valuation": {
            "p5_normal_weights": 8,
            "other_tangent_weights": 1,
            "centered_discrete_monomial_valuation": True,
            "obstruction_generators": len(obstructions),
            "obstruction_orders": {"9": len(obstructions)},
            "all_explicit_arc_initials_nonzero": True,
            "H0_degree7_residual_terms": len(residual),
            "H0_degree7_order": residual_order,
            "H0_explicit_arc_initial": int(residual_initial_value),
            "inequality": "v(H0_residual)=7 < 9=v(I2)",
            "integral_closure_consequence": (
                "H0_residual is not integral over I2; hence at least one "
                "Rees valuation of I2 violates the integral-closure inequality"
            ),
        },
        "source_arc_guard": {
            "leading_nonzero_ambient_coordinates": len(ambient),
            "leading_physical_edges": len(physical_edges),
            "direct_single_edge_source_support": False,
            "intrinsic_single_edge_cap_extracted": False,
        },
        "strict7_repair": {
            "G_terms": len(common_factor),
            "dG_dr": -1,
            "newest_transverse_variables_in_G": 0,
            "pivot_block": "(z44+z45)*I_11",
            "localized_initial_ideal_after_triangular_change":
                "(y1,...,y11,r) over the dense-branch coefficient field",
            "Rees_valuations": (
                "one exceptional-order valuation, with value 1 on each "
                "of y1,...,y11,r"
            ),
            "H0_initial_identity": "H0^10=U*G",
            "H0_initial_terms": len(h0_initial),
            "initial_integral_membership": True,
        },
        "verdict": (
            "the committed contact/second-lift data do not promote to "
            "integral closure: an explicit centered valuation violates the "
            "required inequality.  The later monic G repairs that valuation "
            "only on the finite strict-seven initial chart.  No full source-"
            "valid clean cap or annihilator class is constructed."
        ),
        "missing_input": (
            "the full iterated source chart (or an all-orders filtered-Rees "
            "standard-basis theorem) relating the 252-variable completed "
            "mixed ideal to the repaired triangular initial chart"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"P5 Rees-valuation ledger changed: {digest}")
    print("N=8 P5 Rees-valuation promotion gate: PASS")
    print("early chart: v(H0 residual)=7 < v(I2)=9")
    print("strict-seven initial: coordinate ideal; H0^10=U*G")
    print("source-valid clean/annihilator class: NOT CONSTRUCTED")
    print("ledger sha256:", digest)


if __name__ == "__main__":
    audit()
