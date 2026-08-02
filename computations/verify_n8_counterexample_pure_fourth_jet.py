#!/usr/bin/env python3
"""Exact fourth-jet lock for the missing colour-one coefficient at n=8.

The quadratic conormal products and a triangular cubic correction turn
F_1=H_1-H_11000111 into a residual whose cubic tangent part is the known
-z_3511 times a quadratic lift obstruction.  This checker computes the
true fourth arc coefficient in tangent variables z and free second-jet
variables s.  It proves

    P_4 + z_3511 K_3 in (O_2),

where O_2 is the rank-39 second-lift obstruction space and K_3 is the
third-lift obstruction of the literal mixed equation
H_11001001-H_11000001.  Hence H_1 is O(t^5) on every mixed-fibre arc.
"""

from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import product
import importlib.util
import json
from pathlib import Path


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


HERE = Path(__file__).resolve().parent
CUBIC_CHECKER = HERE / "verify_n8_counterexample_pure_cubic_conormal.py"
SPEC = importlib.util.spec_from_file_location("n8_cubic_conormal", CUBIC_CHECKER)
CUBIC = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CUBIC)

FACTOR = CUBIC.FACTOR
SECOND = CUBIC.SECOND
THIRD = CUBIC.THIRD
TANGENT = CUBIC.TANGENT
FULL = CUBIC.FULL
QQ = Fraction

LITERAL_LIFT_WORD_POSITIVE = (1, 1, 0, 0, 1, 0, 0, 1)
LITERAL_LIFT_WORD_NEGATIVE = (1, 1, 0, 0, 0, 0, 0, 1)

EXPECTED_LEDGER_SHA256 = (
    "ada590fdab7c203662e5a341bd68d6023a5b3b02e1a3156d852b654ec953ff01"
)


def colour_one_first_correction(degree):
    """Degree-d part of the nine linear-multiplier mixed corrections."""
    answer = {}
    for (_normal, multiplier), representation in zip(
            FACTOR.FACTORS_1, FACTOR.NORMAL_REPRESENTATIONS_1):
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


def second_order_data():
    """Tangent basis, canonical w(z), and the exact O_2 row basis."""
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

    canonical_second_forms = defaultdict(dict)
    obstruction_coordinate_polynomials = defaultdict(dict)
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
            preimage, residual = THIRD.decompose_in_column_span(
                coefficient, column_pivots, column_representatives
            )
            monomial = (left, right)
            for coordinate, value in preimage.items():
                canonical_second_forms[coordinate][monomial] = -value
            for cokernel_coordinate, value in residual.items():
                obstruction_coordinate_polynomials[cokernel_coordinate][
                    monomial
                ] = value

    obstruction_pivots = THIRD.exact_row_echelon(
        obstruction_coordinate_polynomials.values()
    )
    require(len(row_pivots) == 196, "mixed Jacobian rank changed")
    require(len(tangent_basis) == 56, "mixed tangent dimension changed")
    require(len(obstruction_pivots) == 39,
            "second-lift obstruction rank changed")
    require(not (set(canonical_second_forms) & set(free_columns)),
            "canonical second lift acquired a free tangent coordinate")
    return (
        free_columns,
        tangent_basis,
        canonical_second_forms,
        obstruction_pivots,
    )


def tangent_and_second_forms(tangent_basis):
    tangent_forms = defaultdict(dict)
    free_second_forms = defaultdict(dict)
    offset = len(tangent_basis)
    for parameter, vector in enumerate(tangent_basis):
        for coordinate, coefficient in vector.items():
            tangent_forms[coordinate][parameter,] = coefficient
            free_second_forms[coordinate][offset + parameter,] = coefficient
    return tangent_forms, free_second_forms


def literal_third_lift_obstruction(
        tangent_basis, canonical_second_forms):
    """Coefficient t^3 of G(p+tv+t^2(w_can+s)) for literal mixed G."""
    positive_gradient = TANGENT.specialized_gradient(LITERAL_LIFT_WORD_POSITIVE)
    negative_gradient = TANGENT.specialized_gradient(LITERAL_LIFT_WORD_NEGATIVE)
    require(positive_gradient == negative_gradient,
            "literal lift equation difference acquired a linear term")

    quadratic = CUBIC.hasse_form(LITERAL_LIFT_WORD_POSITIVE, 2)
    CUBIC.add_scaled(
        quadratic,
        CUBIC.hasse_form(LITERAL_LIFT_WORD_NEGATIVE, 2),
        -1,
    )
    cubic = CUBIC.hasse_form(LITERAL_LIFT_WORD_POSITIVE, 3)
    CUBIC.add_scaled(
        cubic,
        CUBIC.hasse_form(LITERAL_LIFT_WORD_NEGATIVE, 3),
        -1,
    )

    tangent_forms, free_second_forms = tangent_and_second_forms(tangent_basis)
    obstruction = CUBIC.tangent_restriction(cubic, tangent_basis)
    for (left, right), coefficient in quadratic.items():
        for first, second in ((left, right), (right, left)):
            CUBIC.add_scaled(
                obstruction,
                CUBIC.multiply_polynomials(
                    tangent_forms[first], canonical_second_forms[second]
                ),
                coefficient,
            )
            CUBIC.add_scaled(
                obstruction,
                CUBIC.multiply_polynomials(
                    tangent_forms[first], free_second_forms[second]
                ),
                coefficient,
            )
    quadratic_tangent = CUBIC.tangent_restriction(
        quadratic, tangent_basis
    )
    return quadratic_tangent, obstruction


def divides(divisor, monomial):
    counts = Counter(monomial)
    divisor_counts = Counter(divisor)
    if any(counts[index] < multiplicity
           for index, multiplicity in divisor_counts.items()):
        return None
    remainder = list(monomial)
    for index in divisor:
        remainder.remove(index)
    return tuple(remainder)


def reduce_by_quadratic_obstructions(polynomial, obstruction_pivots):
    """Triangular weighted-degree-four division by the O_2 row basis."""
    work = dict(polynomial)
    remainder = {}
    quotients = {}
    steps = 0
    while work:
        monomial = min(work)
        coefficient = work[monomial]
        selected = None
        for pivot, row in sorted(obstruction_pivots.items()):
            multiplier = divides(pivot, monomial)
            if multiplier is not None:
                selected = pivot, row, multiplier
                break
        if selected is None:
            remainder[monomial] = coefficient
            work.pop(monomial)
            continue
        pivot, row, multiplier = selected
        quotient_key = (pivot, multiplier)
        value = quotients.get(quotient_key, QQ(0)) + coefficient
        if value:
            quotients[quotient_key] = value
        else:
            quotients.pop(quotient_key, None)
        for quadratic_monomial, quadratic_coefficient in row.items():
            output_monomial = tuple(sorted(quadratic_monomial + multiplier))
            value = (work.get(output_monomial, QQ(0))
                     - coefficient * quadratic_coefficient)
            if value:
                work[output_monomial] = value
            else:
                work.pop(output_monomial, None)
        steps += 1
    return quotients, remainder, steps


def reconstruct_obstruction_division(quotients, obstruction_pivots):
    answer = {}
    for (pivot, multiplier), coefficient in quotients.items():
        multiplier_polynomial = {multiplier: coefficient}
        CUBIC.add_scaled(
            answer,
            CUBIC.multiply_polynomials(
                obstruction_pivots[pivot], multiplier_polynomial
            ),
        )
    return answer


def audit():
    rows = CUBIC.mixed_rows()
    jacobian_pivots = CUBIC.echelon_with_representatives(rows)
    free_columns, tangent_basis = SECOND.exact_kernel(
        {pivot: row for pivot, (row, _rep) in jacobian_pivots.items()},
        len(FACTOR.AMBIENT_COORDINATES),
    )
    free_position = {coordinate: position
                     for position, coordinate in enumerate(free_columns)}
    free_labels = tuple(
        "".join(map(str, FACTOR.AMBIENT_COORDINATES[coordinate]))
        for coordinate in free_columns
    )
    label_index = {label: index for index, label in enumerate(free_labels)}

    cubic = CUBIC.hasse_form(SECOND.PURE_WORD_1, 3)
    CUBIC.add_scaled(cubic, CUBIC.hasse_form(SECOND.MIXED_WORD_1, 3), -1)
    CUBIC.add_scaled(cubic, colour_one_first_correction(3), -1)
    quotients, cubic_remainder, cubic_steps = (
        CUBIC.divide_by_echelon_linear_forms(cubic, jacobian_pivots)
    )
    require(len(cubic) == 1084, "corrected H1 cubic support changed")
    require(len(quotients) == 68, "H1 cubic conormal-factor count changed")
    require(sum(map(len, quotients.values())) == 1535,
            "H1 cubic multiplier-term count changed")
    require(cubic_steps == 1535, "H1 cubic division-step count changed")

    cubic_remainder_tangent = {
        tuple(sorted(free_position[index] for index in monomial)): coefficient
        for monomial, coefficient in cubic_remainder.items()
    }
    selected_quadratic_obstruction = {
        tuple(sorted((label_index["0410"], label_index["1311"]))): QQ(2),
        tuple(sorted((label_index["0410"], label_index["3711"]))): QQ(-2),
        tuple(sorted((label_index["0411"], label_index["1311"]))): QQ(-2),
        tuple(sorted((label_index["0411"], label_index["3711"]))): QQ(2),
    }
    expected_cubic_remainder = CUBIC.multiply_polynomials(
        {(label_index["3511"],): QQ(-1)},
        selected_quadratic_obstruction,
    )
    require(cubic_remainder_tangent == expected_cubic_remainder,
            "H1 cubic remainder lost its obstruction factor")

    quartic = CUBIC.hasse_form(SECOND.PURE_WORD_1, 4)
    CUBIC.add_scaled(quartic, CUBIC.hasse_form(SECOND.MIXED_WORD_1, 4), -1)
    CUBIC.add_scaled(quartic, colour_one_first_correction(4), -1)
    for pivot, quotient in quotients.items():
        represented_quadratic = {}
        for row_index, coefficient in jacobian_pivots[pivot][1].items():
            CUBIC.add_scaled(
                represented_quadratic,
                CUBIC.hasse_form(rows[row_index][0], 2),
                coefficient,
            )
        CUBIC.add_scaled(
            quartic,
            CUBIC.multiply_polynomials(quotient, represented_quadratic),
            -1,
        )
    require(len(quartic) == 22026, "corrected H1 ambient quartic changed")
    quartic_arc_output = CUBIC.tangent_restriction(quartic, tangent_basis)
    require(len(quartic_arc_output) == 24,
            "H1 tangent quartic support changed")

    # The degree-three remainder contributes its directional derivative in
    # the free tangent part s of the second arc coefficient.
    offset = len(tangent_basis)
    for monomial, coefficient in cubic_remainder_tangent.items():
        for position, parameter in enumerate(monomial):
            output_monomial = list(monomial)
            output_monomial[position] = offset + parameter
            output_monomial = tuple(sorted(output_monomial))
            value = quartic_arc_output.get(output_monomial, QQ(0)) + coefficient
            if value:
                quartic_arc_output[output_monomial] = value
            else:
                quartic_arc_output.pop(output_monomial, None)
    require(len(quartic_arc_output) == 36,
            "true H1 fourth arc output support changed")

    (
        obstruction_free_columns,
        obstruction_tangent_basis,
        canonical_second_forms,
        obstruction_pivots,
    ) = second_order_data()
    require(obstruction_free_columns == free_columns,
            "second-order free coordinates changed")
    require(obstruction_tangent_basis == tangent_basis,
            "second-order tangent basis changed")

    literal_quadratic, literal_third = literal_third_lift_obstruction(
        tangent_basis, canonical_second_forms
    )
    require(literal_quadratic == selected_quadratic_obstruction,
            "literal mixed equation lost the selected O_2 obstruction")
    require(len(literal_third) == 34,
            "literal third-lift obstruction support changed")

    third_factor = CUBIC.multiply_polynomials(
        {(label_index["3511"],): QQ(1)}, literal_third
    )
    ideal_target = dict(quartic_arc_output)
    CUBIC.add_scaled(ideal_target, third_factor)
    obstruction_quotients, obstruction_remainder, obstruction_steps = (
        reduce_by_quadratic_obstructions(ideal_target, obstruction_pivots)
    )
    require(not obstruction_remainder,
            "H1 fourth output escaped the O_2 plus K_3 ideal")
    require(obstruction_steps == 19,
            "H1 fourth obstruction-reduction step count changed")
    require(
        reconstruct_obstruction_division(
            obstruction_quotients, obstruction_pivots
        ) == ideal_target,
        "H1 fourth obstruction factorization did not replay",
    )

    return {
        "ambient_variables": len(FACTOR.AMBIENT_COORDINATES),
        "mixed_jacobian_rank": len(jacobian_pivots),
        "mixed_tangent_dimension": len(tangent_basis),
        "second_lift_obstruction_rank": len(obstruction_pivots),
        "corrected_H1_cubic_ambient_terms": len(cubic),
        "H1_cubic_conormal_factors": len(quotients),
        "H1_cubic_quadratic_multiplier_terms": sum(
            map(len, quotients.values())
        ),
        "H1_cubic_remainder_terms": len(cubic_remainder_tangent),
        "H1_cubic_remainder_factorization": "-z_3511*O_2_selected",
        "selected_O2_factorization": (
            "2*(z_0410-z_0411)*(z_1311-z_3711)"
        ),
        "corrected_H1_quartic_ambient_terms": len(quartic),
        "H1_quartic_tangent_terms": 24,
        "H1_true_fourth_arc_output_terms": len(quartic_arc_output),
        "literal_third_lift_equation": (
            "H_11001001-H_11000001"
        ),
        "literal_third_lift_obstruction_terms": len(literal_third),
        "fourth_jet_identity": (
            "P4+z_3511*K3 belongs to the ideal generated by O2"
        ),
        "O2_multiplier_terms": len(obstruction_quotients),
        "O2_reduction_steps": obstruction_steps,
        "O2_remainder_terms": len(obstruction_remainder),
        "higher_arc_coefficient_independence": (
            "the corrected residual begins in degree three, so its t^4 "
            "coefficient depends on v and the free tangent part s of w, "
            "but not on the third arc coefficient u"
        ),
        "formal_arc_conclusion": "H_1 is O(t^5) on every mixed-fibre arc",
    }


def main():
    ledger = audit()
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                "frozen fourth-jet ledger digest changed")
    print(
        "n=8 counterexample pure fourth jet: PASS; "
        "H1 cubic=-z3511*O2; P4+z3511*K3 in (O2), "
        "O2 remainder=0, H1=O(t^5)"
    )
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
