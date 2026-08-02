#!/usr/bin/env python3
"""Exact translated-ring certificates H_0,H_1 in I_mix + m_p^5.

The jet checkers prove fifth-order vanishing on formal mixed-fibre arcs.
This checker proves the stronger finite local-algebra statement.  It keeps
provenance through the Jacobian and second-obstruction eliminations, lifts
every obstruction basis form used by the quartic reductions to a literal
rational combination of mixed hafnian equations, and finally divides the
remaining ambient quartics through the mixed conormals.  The corrected
pure coefficients have no translated homogeneous part of degree below 5.
"""

from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
from heapq import heapify, heappop, heappush
import importlib.util
import json
from pathlib import Path


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


HERE = Path(__file__).resolve().parent
FOURTH_CHECKER = HERE / "verify_n8_counterexample_pure_fourth_jet.py"
SPEC = importlib.util.spec_from_file_location("n8_fourth_jet", FOURTH_CHECKER)
FOURTH = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(FOURTH)

CUBIC = FOURTH.CUBIC
FACTOR = FOURTH.FACTOR
SECOND = FOURTH.SECOND
THIRD = FOURTH.THIRD
TANGENT = FOURTH.TANGENT
FULL = FOURTH.FULL
QQ = Fraction

EXPECTED_LEDGER_SHA256 = (
    "193291f9356f4d8d56bf0404247ae3f9dd1c1a15772bc420e1ac12d1adeda7ac"
)


def first_correction(colour, degree):
    factors = FACTOR.FACTORS_0 if colour == 0 else FACTOR.FACTORS_1
    representations = (
        FACTOR.NORMAL_REPRESENTATIONS_0
        if colour == 0 else FACTOR.NORMAL_REPRESENTATIONS_1
    )
    answer = {}
    for (_normal, multiplier), representation in zip(
            factors, representations):
        multiplier_polynomial = {
            (index,): coefficient for index, coefficient in multiplier.items()
        }
        represented = CUBIC.represented_hasse_form(
            representation, degree - 1
        )
        CUBIC.add_scaled(
            answer,
            CUBIC.multiply_polynomials(multiplier_polynomial, represented),
        )
    return answer


def echelon_with_named_representatives(named_polynomials):
    """Sparse normalized row basis retaining input-name provenance."""
    pivots = {}
    for name, source in named_polynomials:
        row = dict(source)
        representative = {name: QQ(1)}
        while row:
            pivot = min(row)
            value = row[pivot]
            if pivot not in pivots:
                pivots[pivot] = (
                    {monomial: coefficient / value
                     for monomial, coefficient in row.items()},
                    {key: coefficient / value
                     for key, coefficient in representative.items()},
                )
                break
            basis_row, basis_representative = pivots[pivot]
            CUBIC.add_scaled(row, basis_row, -value)
            CUBIC.add_scaled(representative, basis_representative, -value)
    return pivots


def obstruction_data():
    """Rank-39 O_2 basis with provenance in cokernel coordinates."""
    jacobian_rows = THIRD.mixed_jacobian_rows()
    nonzero_rows = tuple(row for row in jacobian_rows if row)
    row_pivots = THIRD.exact_row_echelon(nonzero_rows)
    free_columns, tangent_basis = SECOND.exact_kernel(
        row_pivots, len(FACTOR.AMBIENT_COORDINATES)
    )
    column_pivots, column_representatives = (
        THIRD.exact_column_echelon_with_representatives(jacobian_rows)
    )
    pair_columns = THIRD.quadratic_pair_columns(THIRD.MIXED_WORDS)
    coordinate_polynomials = defaultdict(dict)
    for left, left_vector in enumerate(tangent_basis):
        for right in range(left, len(tangent_basis)):
            if left == right:
                coefficient = THIRD.quadratic_value(
                    left_vector, pair_columns
                )
            else:
                coefficient = THIRD.bilinear_value(
                    left_vector, tangent_basis[right], pair_columns
                )
            _preimage, residual = THIRD.decompose_in_column_span(
                coefficient, column_pivots, column_representatives
            )
            for cokernel_coordinate, value in residual.items():
                coordinate_polynomials[cokernel_coordinate][left, right] = value

    obstruction_pivots = echelon_with_named_representatives(
        sorted(coordinate_polynomials.items())
    )
    require(len(row_pivots) == 196, "mixed Jacobian rank changed")
    require(len(tangent_basis) == 56, "mixed tangent dimension changed")
    require(len(obstruction_pivots) == 39,
            "second-lift obstruction rank changed")
    return {
        "jacobian_rows": jacobian_rows,
        "column_pivots": column_pivots,
        "free_columns": free_columns,
        "tangent_basis": tangent_basis,
        "obstruction_pivots": obstruction_pivots,
    }


def literal_cokernel_lift(cokernel_representative, data):
    """Lift a residual-coordinate functional to literal mixed equations."""
    functional = dict(cokernel_representative)
    # Back substitution makes the functional annihilate every Jacobian
    # pivot column, without changing its values on nonpivot residual rows.
    for pivot in sorted(data["column_pivots"], reverse=True):
        column = data["column_pivots"][pivot]
        tail = sum(
            coefficient * functional.get(row_index, QQ(0))
            for row_index, coefficient in column.items()
            if row_index != pivot
        )
        if tail:
            functional[pivot] = -tail

    combined_gradient = {}
    for row_index, coefficient in functional.items():
        CUBIC.add_scaled(
            combined_gradient,
            data["jacobian_rows"][row_index],
            coefficient,
        )
    require(not combined_gradient,
            "literal obstruction lift does not annihilate the Jacobian")
    return functional


def represented_literal_hasse(functional, degree):
    answer = {}
    for row_index, coefficient in functional.items():
        CUBIC.add_scaled(
            answer,
            CUBIC.hasse_form(THIRD.MIXED_WORDS[row_index], degree),
            coefficient,
        )
    return answer


def jacobian_represented_hasse(rows, jacobian_pivots, pivot, degree):
    answer = {}
    for row_index, coefficient in jacobian_pivots[pivot][1].items():
        CUBIC.add_scaled(
            answer,
            CUBIC.hasse_form(rows[row_index][0], degree),
            coefficient,
        )
    return answer


def fast_divide_by_echelon_linear_forms(polynomial, pivots):
    """Heap implementation of the triangular division used for quartics."""
    residual = dict(polynomial)
    heap = list(residual)
    heapify(heap)
    quotients = defaultdict(dict)
    remainder = {}
    steps = 0
    while heap:
        monomial = heappop(heap)
        if monomial not in residual:
            continue
        coefficient = residual[monomial]
        candidates = [index for index in monomial if index in pivots]
        if not candidates:
            remainder[monomial] = coefficient
            residual.pop(monomial)
            continue
        pivot = min(candidates)
        quotient_monomial = list(monomial)
        quotient_monomial.remove(pivot)
        quotient_monomial = tuple(quotient_monomial)
        value = (quotients[pivot].get(quotient_monomial, QQ(0))
                 + coefficient)
        if value:
            quotients[pivot][quotient_monomial] = value
        else:
            quotients[pivot].pop(quotient_monomial, None)
        for index, linear_coefficient in pivots[pivot][0].items():
            output_monomial = tuple(sorted(quotient_monomial + (index,)))
            old_value = residual.get(output_monomial, QQ(0))
            new_value = old_value - coefficient * linear_coefficient
            if new_value:
                residual[output_monomial] = new_value
                if not old_value:
                    heappush(heap, output_monomial)
            else:
                residual.pop(output_monomial, None)
        steps += 1
    return dict(quotients), remainder, steps


def divide_and_replay(polynomial, jacobian_pivots, detail):
    quotients, remainder, steps = fast_divide_by_echelon_linear_forms(
        polynomial, jacobian_pivots
    )
    require(not remainder, f"{detail}: nonzero Jacobian remainder")
    require(
        CUBIC.reconstruct_division(quotients, jacobian_pivots) == polynomial,
        f"{detail}: Jacobian division did not replay",
    )
    return quotients, steps


def convert_tangent_multiplier(multiplier, coefficient, free_columns):
    return {
        tuple(sorted(free_columns[parameter] for parameter in multiplier)):
        coefficient
    }


def lift_obstruction_reduction(
        quartic, tangent_quartic, obstruction_quotients, data,
        obstruction_lift_cache):
    lifted_quartic = {}
    used_literal_words = set()
    maximum_literal_support = 0
    for (pivot, multiplier), coefficient in obstruction_quotients.items():
        if pivot not in obstruction_lift_cache:
            obstruction_row, cokernel_representative = (
                data["obstruction_pivots"][pivot]
            )
            functional = literal_cokernel_lift(
                cokernel_representative, data
            )
            quadratic = represented_literal_hasse(functional, 2)
            require(
                CUBIC.tangent_restriction(
                    quadratic, data["tangent_basis"]
                ) == obstruction_row,
                "literal mixed lift lost its quadratic obstruction",
            )
            obstruction_lift_cache[pivot] = functional, quadratic
        functional, quadratic = obstruction_lift_cache[pivot]
        used_literal_words.update(functional)
        maximum_literal_support = max(maximum_literal_support, len(functional))
        ambient_multiplier = convert_tangent_multiplier(
            multiplier, coefficient, data["free_columns"]
        )
        CUBIC.add_scaled(
            lifted_quartic,
            CUBIC.multiply_polynomials(ambient_multiplier, quadratic),
        )

    residual = dict(quartic)
    CUBIC.add_scaled(residual, lifted_quartic, -1)
    require(
        not CUBIC.tangent_restriction(residual, data["tangent_basis"]),
        "lifted obstruction correction left a tangent quartic",
    )
    require(
        FOURTH.reconstruct_obstruction_division(
            obstruction_quotients,
            {pivot: row for pivot, (row, _rep)
             in data["obstruction_pivots"].items()},
        ) == tangent_quartic,
        "quadratic obstruction reduction did not replay",
    )
    return residual, used_literal_words, maximum_literal_support


def base_colour_data(colour, rows, jacobian_pivots):
    pure_word = SECOND.PURE_WORD_0 if colour == 0 else SECOND.PURE_WORD_1
    mixed_word = SECOND.MIXED_WORD_0 if colour == 0 else SECOND.MIXED_WORD_1

    constant = CUBIC.hasse_form(pure_word, 0)
    CUBIC.add_scaled(constant, CUBIC.hasse_form(mixed_word, 0), -1)
    require(not constant, f"H{colour}: constant term changed")
    linear = CUBIC.hasse_form(pure_word, 1)
    CUBIC.add_scaled(linear, CUBIC.hasse_form(mixed_word, 1), -1)
    require(not linear, f"H{colour}: selected first conormal changed")
    quadratic = CUBIC.hasse_form(pure_word, 2)
    CUBIC.add_scaled(quadratic, CUBIC.hasse_form(mixed_word, 2), -1)
    CUBIC.add_scaled(quadratic, first_correction(colour, 2), -1)
    require(not quadratic, f"H{colour}: quadratic correction changed")

    cubic = CUBIC.hasse_form(pure_word, 3)
    CUBIC.add_scaled(cubic, CUBIC.hasse_form(mixed_word, 3), -1)
    CUBIC.add_scaled(cubic, first_correction(colour, 3), -1)
    cubic_quotients, cubic_remainder, cubic_steps = (
        CUBIC.divide_by_echelon_linear_forms(cubic, jacobian_pivots)
    )
    reconstructed_cubic = CUBIC.reconstruct_division(
        cubic_quotients, jacobian_pivots
    )
    CUBIC.add_scaled(reconstructed_cubic, cubic_remainder)
    require(reconstructed_cubic == cubic,
            f"H{colour}: cubic normal form did not replay")

    quartic = CUBIC.hasse_form(pure_word, 4)
    CUBIC.add_scaled(quartic, CUBIC.hasse_form(mixed_word, 4), -1)
    CUBIC.add_scaled(quartic, first_correction(colour, 4), -1)
    for pivot, quotient in cubic_quotients.items():
        represented_quadratic = jacobian_represented_hasse(
            rows, jacobian_pivots, pivot, 2
        )
        CUBIC.add_scaled(
            quartic,
            CUBIC.multiply_polynomials(quotient, represented_quadratic),
            -1,
        )
    return {
        "pure_word": pure_word,
        "mixed_word": mixed_word,
        "cubic": cubic,
        "cubic_quotients": cubic_quotients,
        "cubic_remainder": cubic_remainder,
        "cubic_steps": cubic_steps,
        "quartic": quartic,
    }


def audit():
    rows = CUBIC.mixed_rows()
    jacobian_pivots = CUBIC.echelon_with_representatives(rows)
    require(len(jacobian_pivots) == 196, "mixed Jacobian rank changed")
    data = obstruction_data()
    require(
        data["free_columns"] == SECOND.exact_kernel(
            {pivot: row for pivot, (row, _rep) in jacobian_pivots.items()},
            len(FACTOR.AMBIENT_COORDINATES),
        )[0],
        "Jacobian and obstruction free coordinates diverged",
    )
    simple_obstruction_pivots = {
        pivot: row for pivot, (row, _rep)
        in data["obstruction_pivots"].items()
    }
    obstruction_lift_cache = {}
    coordinate_names = {
        "".join(map(str, coordinate)): index
        for index, coordinate in enumerate(FACTOR.AMBIENT_COORDINATES)
    }
    ledgers = []

    # Colour zero: the cubic remainder is already zero.  Its quartic is a
    # single O_2 multiple before the ambient normal-coordinate cleanup.
    zero = base_colour_data(0, rows, jacobian_pivots)
    require(not zero["cubic_remainder"], "H0 cubic remainder returned")
    zero_tangent_quartic = CUBIC.tangent_restriction(
        zero["quartic"], data["tangent_basis"]
    )
    zero_obstruction_quotients, zero_obstruction_remainder, zero_obs_steps = (
        FOURTH.reduce_by_quadratic_obstructions(
            zero_tangent_quartic, simple_obstruction_pivots
        )
    )
    require(not zero_obstruction_remainder,
            "H0 quartic escaped the O_2 ideal")
    zero_ambient_quartic, zero_literal_words, zero_max_literal = (
        lift_obstruction_reduction(
            zero["quartic"], zero_tangent_quartic,
            zero_obstruction_quotients, data, obstruction_lift_cache
        )
    )
    zero_normal_quotients, zero_normal_steps = divide_and_replay(
        zero_ambient_quartic, jacobian_pivots, "H0 quartic"
    )
    ledgers.append({
        "pure_colour": 0,
        "cubic_ambient_terms": len(zero["cubic"]),
        "cubic_jacobian_factors": len(zero["cubic_quotients"]),
        "cubic_multiplier_terms": sum(map(len, zero["cubic_quotients"].values())),
        "cubic_remainder_terms": len(zero["cubic_remainder"]),
        "quartic_before_obstruction_lift_terms": len(zero["quartic"]),
        "quartic_tangent_terms": len(zero_tangent_quartic),
        "quadratic_obstruction_multiplier_terms": len(zero_obstruction_quotients),
        "quadratic_obstruction_reduction_steps": zero_obs_steps,
        "literal_obstruction_mixed_words": len(zero_literal_words),
        "maximum_literal_obstruction_support": zero_max_literal,
        "quartic_after_obstruction_lift_terms": len(zero_ambient_quartic),
        "quartic_normal_factors": len(zero_normal_quotients),
        "quartic_normal_multiplier_terms": sum(map(len, zero_normal_quotients.values())),
        "quartic_normal_division_steps": zero_normal_steps,
        "degree_below_five_remainder_terms": 0,
    })

    # Colour one: first lift the four-term cubic obstruction by the literal
    # mixed equation H_11001001-H_11000001, then clear its ambient normal
    # cubic, reduce the resulting quartic by O_2, and clear ambient normals.
    one = base_colour_data(1, rows, jacobian_pivots)
    literal_one_functional = {
        THIRD.MIXED_WORD_INDEX[FOURTH.LITERAL_LIFT_WORD_POSITIVE]: QQ(1),
        THIRD.MIXED_WORD_INDEX[FOURTH.LITERAL_LIFT_WORD_NEGATIVE]: QQ(-1),
    }
    literal_one_quadratic = represented_literal_hasse(
        literal_one_functional, 2
    )
    literal_one_cubic = represented_literal_hasse(
        literal_one_functional, 3
    )
    one_linear_multiplier = {
        (coordinate_names["3511"],): QQ(-1)
    }
    one_cubic_normal = dict(one["cubic_remainder"])
    CUBIC.add_scaled(
        one_cubic_normal,
        CUBIC.multiply_polynomials(
            one_linear_multiplier, literal_one_quadratic
        ),
        -1,
    )
    one_extra_cubic_quotients, one_extra_cubic_steps = divide_and_replay(
        one_cubic_normal, jacobian_pivots, "H1 literal cubic lift"
    )
    one_quartic = dict(one["quartic"])
    CUBIC.add_scaled(
        one_quartic,
        CUBIC.multiply_polynomials(
            one_linear_multiplier, literal_one_cubic
        ),
        -1,
    )
    for pivot, quotient in one_extra_cubic_quotients.items():
        CUBIC.add_scaled(
            one_quartic,
            CUBIC.multiply_polynomials(
                quotient,
                jacobian_represented_hasse(
                    rows, jacobian_pivots, pivot, 2
                ),
            ),
            -1,
        )
    one_tangent_quartic = CUBIC.tangent_restriction(
        one_quartic, data["tangent_basis"]
    )
    one_obstruction_quotients, one_obstruction_remainder, one_obs_steps = (
        FOURTH.reduce_by_quadratic_obstructions(
            one_tangent_quartic, simple_obstruction_pivots
        )
    )
    require(not one_obstruction_remainder,
            "H1 quartic escaped the O_2 ideal")
    one_ambient_quartic, one_literal_words, one_max_literal = (
        lift_obstruction_reduction(
            one_quartic, one_tangent_quartic,
            one_obstruction_quotients, data, obstruction_lift_cache
        )
    )
    one_normal_quotients, one_normal_steps = divide_and_replay(
        one_ambient_quartic, jacobian_pivots, "H1 quartic"
    )
    ledgers.append({
        "pure_colour": 1,
        "cubic_ambient_terms": len(one["cubic"]),
        "cubic_jacobian_factors": len(one["cubic_quotients"]),
        "cubic_multiplier_terms": sum(map(len, one["cubic_quotients"].values())),
        "cubic_initial_remainder_terms": len(one["cubic_remainder"]),
        "literal_cubic_lift_equation": "H_11001001-H_11000001",
        "cubic_after_literal_lift_terms": len(one_cubic_normal),
        "extra_cubic_normal_factors": len(one_extra_cubic_quotients),
        "extra_cubic_normal_multiplier_terms": sum(
            map(len, one_extra_cubic_quotients.values())
        ),
        "quartic_before_obstruction_lift_terms": len(one_quartic),
        "quartic_tangent_terms": len(one_tangent_quartic),
        "quadratic_obstruction_multiplier_terms": len(one_obstruction_quotients),
        "quadratic_obstruction_reduction_steps": one_obs_steps,
        "literal_obstruction_mixed_words": len(one_literal_words),
        "maximum_literal_obstruction_support": one_max_literal,
        "quartic_after_obstruction_lift_terms": len(one_ambient_quartic),
        "quartic_normal_factors": len(one_normal_quotients),
        "quartic_normal_multiplier_terms": sum(map(len, one_normal_quotients.values())),
        "quartic_normal_division_steps": one_normal_steps,
        "degree_below_five_remainder_terms": 0,
    })

    return {
        "ambient_variables": len(FACTOR.AMBIENT_COORDINATES),
        "translated_point_nonzero_coordinates": len(FACTOR.POINT),
        "mixed_jacobian_rank": len(jacobian_pivots),
        "mixed_tangent_dimension": len(data["tangent_basis"]),
        "second_lift_obstruction_rank": len(data["obstruction_pivots"]),
        "colours": ledgers,
        "literal_obstruction_lifts_cached": len(obstruction_lift_cache),
        "local_membership": [
            "H_0 belongs to I_mix + m_p^5",
            "H_1 belongs to I_mix + m_p^5",
        ],
        "localized_orbit_conclusion": (
            "port-torus transport gives the same mod-m^5 membership "
            "at every generic point of the five-parameter Laurent orbit"
        ),
    }


def main():
    ledger = audit()
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                "frozen local mod-m5 ledger digest changed")
    print(
        "n=8 local mod-m^5 membership: PASS; "
        "H0,H1 in I_mix+m_p^5; literal O2 lifts=yes, "
        "ambient quartic Jacobian remainders=(0,0)"
    )
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
