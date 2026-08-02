#!/usr/bin/env python3
"""Exact conormal certificate for the corrected colour-zero cubic jet.

Start with F=H_0-H_00000010 at the rational n=8 mixed-torus point.  The
quadratic conormal factorization supplies linear multipliers times mixed
equations which kill F through degree two.  This checker proves that the
remaining 166-term cubic is again in the mixed Jacobian ideal: sparse
triangular division gives 33 conormal factors and 159 quadratic multiplier
terms.  It then constructs the next, 1936-term quartic residual and proves
by an exact tangent witness that this residual is not zero on all ker J.
"""

from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import importlib.util
import json
from math import prod
from pathlib import Path


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


HERE = Path(__file__).resolve().parent
FACTOR_CHECKER = HERE / "verify_n8_counterexample_quadratic_conormal_factorization.py"
SPEC = importlib.util.spec_from_file_location("n8_conormal_factor", FACTOR_CHECKER)
FACTOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(FACTOR)

THIRD_JET_CHECKER = HERE / "verify_n8_counterexample_pure_third_jet.py"
THIRD_SPEC = importlib.util.spec_from_file_location(
    "n8_third_jet", THIRD_JET_CHECKER
)
THIRD = importlib.util.module_from_spec(THIRD_SPEC)
THIRD_SPEC.loader.exec_module(THIRD)

SECOND = FACTOR.SECOND
TANGENT = FACTOR.TANGENT
FULL = FACTOR.FULL
QQ = Fraction

EXPECTED_LEDGER_SHA256 = (
    "454e27b47b6f6292d796d8a87b5534dad4b044d0253c034f4383ee290fe3a0f9"
)


def clean(polynomial):
    return {monomial: coefficient for monomial, coefficient in polynomial.items()
            if coefficient}


def add_scaled(target, source, scalar=QQ(1)):
    for monomial, coefficient in source.items():
        value = target.get(monomial, QQ(0)) + scalar * coefficient
        if value:
            target[monomial] = value
        else:
            target.pop(monomial, None)


def multiply_polynomials(left, right):
    answer = defaultdict(QQ)
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            monomial = tuple(sorted(left_monomial + right_monomial))
            answer[monomial] += left_coefficient * right_coefficient
    return clean(answer)


def hasse_form(word, degree):
    """Degree-d part of H_word(p+z), in ambient coordinate indices."""
    answer = defaultdict(QQ)
    for matching_term in FULL.word_terms(word):
        indices = [FACTOR.COORDINATE_INDEX[coordinate]
                   for coordinate in matching_term]
        for selected in combinations(range(4), degree):
            coefficient = prod(
                FACTOR.POINT.get(matching_term[position], 0)
                for position in range(4) if position not in selected
            )
            if coefficient:
                monomial = tuple(sorted(indices[position]
                                        for position in selected))
                answer[monomial] += coefficient
    return clean(answer)


def represented_hasse_form(representation, degree):
    answer = {}
    for coefficient, word_name in representation:
        word = tuple(map(int, word_name))
        require(len(set(word)) > 1, "correction used a pure equation")
        add_scaled(answer, hasse_form(word, degree), QQ(coefficient))
    return answer


def mixed_rows():
    answer = []
    for word in product(FULL.COLOURS, repeat=8):
        if len(set(word)) == 1:
            continue
        gradient = TANGENT.specialized_gradient(word)
        if gradient:
            answer.append((word, {
                FACTOR.COORDINATE_INDEX[coordinate]: QQ(value)
                for coordinate, value in gradient.items()
            }))
    return tuple(answer)


def echelon_with_representatives(rows):
    """Normalized triangular row basis plus actual mixed-row provenance."""
    pivots = {}
    for row_index, (_word, source) in enumerate(rows):
        row = dict(source)
        representative = {row_index: QQ(1)}
        while row:
            pivot = min(row)
            value = row[pivot]
            if pivot not in pivots:
                pivots[pivot] = (
                    {index: coefficient / value
                     for index, coefficient in row.items()},
                    {index: coefficient / value
                     for index, coefficient in representative.items()},
                )
                break
            basis_row, basis_representative = pivots[pivot]
            add_scaled(row, basis_row, -value)
            add_scaled(representative, basis_representative, -value)
    return pivots


def reconstruct_echelon_rows(rows, pivots):
    for pivot, (basis_row, representative) in pivots.items():
        reconstructed = {}
        for row_index, coefficient in representative.items():
            add_scaled(reconstructed, rows[row_index][1], coefficient)
        require(reconstructed == basis_row,
                f"mixed-row provenance failed at pivot {pivot}")


def divide_by_echelon_linear_forms(polynomial, pivots):
    """Triangularly write a homogeneous polynomial as sum L_p Q_p+R."""
    residual = dict(polynomial)
    quotients = defaultdict(dict)
    steps = 0
    while True:
        selected = next(
            (monomial for monomial in sorted(residual)
             if any(index in pivots for index in monomial)),
            None,
        )
        if selected is None:
            break
        pivot = min(index for index in selected if index in pivots)
        coefficient = residual[selected]
        quotient_monomial = list(selected)
        quotient_monomial.remove(pivot)
        quotient_monomial = tuple(quotient_monomial)
        value = quotients[pivot].get(quotient_monomial, QQ(0)) + coefficient
        if value:
            quotients[pivot][quotient_monomial] = value
        else:
            quotients[pivot].pop(quotient_monomial, None)
        basis_row, _representative = pivots[pivot]
        for index, linear_coefficient in basis_row.items():
            monomial = tuple(sorted(quotient_monomial + (index,)))
            value = (residual.get(monomial, QQ(0))
                     - coefficient * linear_coefficient)
            if value:
                residual[monomial] = value
            else:
                residual.pop(monomial, None)
        steps += 1
    return {pivot: clean(quotient) for pivot, quotient in quotients.items()
            if clean(quotient)}, clean(residual), steps


def reconstruct_division(quotients, pivots):
    answer = {}
    for pivot, quotient in quotients.items():
        linear_form = {
            (index,): coefficient
            for index, coefficient in pivots[pivot][0].items()
        }
        add_scaled(answer, multiply_polynomials(linear_form, quotient))
    return answer


def first_correction_part(degree):
    """Degree-d part of the five linear-multiplier mixed corrections."""
    answer = {}
    # A linear multiplier times degree-(d-1) of its represented equation.
    for (_normal, multiplier), representation in zip(
            FACTOR.FACTORS_0, FACTOR.NORMAL_REPRESENTATIONS_0):
        multiplier_polynomial = {
            (index,): coefficient for index, coefficient in multiplier.items()
        }
        represented = represented_hasse_form(representation, degree - 1)
        add_scaled(answer, multiply_polynomials(
            multiplier_polynomial, represented
        ))
    return answer


def tangent_restriction(polynomial, tangent_basis):
    coordinate_forms = [dict() for _coordinate in FACTOR.AMBIENT_COORDINATES]
    for parameter, vector in enumerate(tangent_basis):
        for coordinate_index, coefficient in vector.items():
            coordinate_forms[coordinate_index][parameter] = coefficient
    answer = {}
    for ambient_monomial, coefficient in polynomial.items():
        contribution = {(): coefficient}
        for coordinate_index in ambient_monomial:
            linear_form = {
                (parameter,): value
                for parameter, value in coordinate_forms[coordinate_index].items()
            }
            contribution = multiply_polynomials(contribution, linear_form)
            if not contribution:
                break
        add_scaled(answer, contribution)
    return answer


def evaluate(polynomial, vector):
    return sum(
        coefficient * prod(vector.get(index, 0) for index in monomial)
        for monomial, coefficient in polynomial.items()
    )


def find_small_witness(polynomial):
    """Find a deterministic {1,-1}-valued witness from a term support."""
    supports = sorted({tuple(sorted(set(monomial))) for monomial in polynomial},
                      key=lambda support: (len(support), support))
    for support in supports:
        # All plus, then the nontrivial sign patterns in binary order.
        for mask in range(1 << len(support)):
            vector = {
                parameter: (-1 if mask & (1 << position) else 1)
                for position, parameter in enumerate(support)
            }
            value = evaluate(polynomial, vector)
            if value:
                return vector, value
    raise RuntimeError("quartic tangent restriction has no witness")


def second_lift_obstruction_basis():
    """Reconstruct the rank-39 quadratic obstruction space on ker J."""
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
    obstruction_pivots = THIRD.exact_row_echelon(
        coordinate_polynomials.values()
    )
    return free_columns, tangent_basis, obstruction_pivots


def audit():
    rows = mixed_rows()
    pivots = echelon_with_representatives(rows)
    require(len(rows) == 1312, "mixed Jacobian nonzero-row count changed")
    require(len(pivots) == 196, "mixed Jacobian rank changed")
    reconstruct_echelon_rows(rows, pivots)

    cubic = hasse_form(SECOND.PURE_WORD_0, 3)
    add_scaled(cubic, hasse_form(SECOND.MIXED_WORD_0, 3), -1)
    add_scaled(cubic, first_correction_part(3), -1)
    require(len(cubic) == 166, "corrected ambient cubic support changed")
    require(set(cubic.values()) == {QQ(-1), QQ(1)},
            "corrected cubic coefficients changed")

    quotients, remainder, division_steps = divide_by_echelon_linear_forms(
        cubic, pivots
    )
    require(not remainder, "corrected cubic escaped the mixed conormal ideal")
    require(reconstruct_division(quotients, pivots) == cubic,
            "cubic conormal division did not replay")
    require(len(quotients) == 33, "cubic conormal-factor count changed")
    require(sum(map(len, quotients.values())) == 159,
            "cubic multiplier-term count changed")
    require(division_steps == 159, "cubic division-step count changed")
    require({coefficient for quotient in quotients.values()
             for coefficient in quotient.values()} == {
                 QQ(-2), QQ(-1), QQ(1), QQ(2)
             }, "cubic quotient coefficients changed")

    # Subtract the corresponding quadratic-multiplier mixed equations and
    # inspect the degree-four residual.
    quartic = hasse_form(SECOND.PURE_WORD_0, 4)
    add_scaled(quartic, hasse_form(SECOND.MIXED_WORD_0, 4), -1)
    add_scaled(quartic, first_correction_part(4), -1)
    for pivot, quotient in quotients.items():
        represented_quadratic = {}
        for row_index, coefficient in pivots[pivot][1].items():
            add_scaled(
                represented_quadratic,
                hasse_form(rows[row_index][0], 2),
                coefficient,
            )
        add_scaled(
            quartic,
            multiply_polynomials(quotient, represented_quadratic),
            -1,
        )
    require(len(quartic) == 1936, "corrected ambient quartic support changed")
    require(set(quartic.values()) == {
        QQ(-4), QQ(-2), QQ(-1), QQ(-1, 2),
        QQ(1, 2), QQ(1), QQ(2), QQ(4),
    }, "corrected quartic coefficients changed")

    tangent_pivots = {pivot: row for pivot, (row, _rep) in pivots.items()}
    free_columns, tangent_basis = SECOND.exact_kernel(
        tangent_pivots, len(FACTOR.AMBIENT_COORDINATES)
    )
    require(len(tangent_basis) == 56, "mixed tangent dimension changed")
    restricted_quartic = tangent_restriction(quartic, tangent_basis)
    free_labels = tuple(
        "".join(map(str, FACTOR.AMBIENT_COORDINATES[index]))
        for index in free_columns
    )
    label_index = {label: index for index, label in enumerate(free_labels)}
    # -2*z_0400*z_1601*(z_3710+z_3711)*(z_6701-z_6711).
    expected_restricted_quartic = {
        tuple(sorted((label_index["0400"], label_index["1601"],
                      label_index["3710"], label_index["6701"]))): QQ(-2),
        tuple(sorted((label_index["0400"], label_index["1601"],
                      label_index["3710"], label_index["6711"]))): QQ(2),
        tuple(sorted((label_index["0400"], label_index["1601"],
                      label_index["3711"], label_index["6701"]))): QQ(-2),
        tuple(sorted((label_index["0400"], label_index["1601"],
                      label_index["3711"], label_index["6711"]))): QQ(2),
    }
    require(restricted_quartic == expected_restricted_quartic,
            "quartic tangent rectangle changed")
    witness, witness_value = find_small_witness(restricted_quartic)
    ambient_witness = {}
    for parameter, scalar in witness.items():
        add_scaled(ambient_witness, tangent_basis[parameter], scalar)
    for _word, row in rows:
        require(sum(coefficient * ambient_witness.get(index, 0)
                    for index, coefficient in row.items()) == 0,
                "quartic witness escaped ker J")
    require(evaluate(quartic, ambient_witness) == witness_value,
            "ambient and restricted quartic witness values diverged")

    obstruction_free_columns, obstruction_tangent_basis, obstruction_pivots = (
        second_lift_obstruction_basis()
    )
    require(obstruction_free_columns == free_columns,
            "second-lift calculation changed the free tangent coordinates")
    require(obstruction_tangent_basis == tangent_basis,
            "second-lift calculation changed the tangent basis")
    require(len(obstruction_pivots) == 39,
            "second-lift obstruction rank changed")
    quartic_obstruction = {
        tuple(sorted((label_index["0400"], label_index["3710"]))): QQ(1),
        tuple(sorted((label_index["0400"], label_index["3711"]))): QQ(1),
    }
    obstruction_pivot = min(quartic_obstruction)
    require(obstruction_pivots.get(obstruction_pivot) == quartic_obstruction,
            "the selected second-lift obstruction changed")
    obstruction_multiplier = {
        tuple(sorted((label_index["1601"], label_index["6701"]))): QQ(-2),
        tuple(sorted((label_index["1601"], label_index["6711"]))): QQ(2),
    }
    require(
        multiply_polynomials(quartic_obstruction, obstruction_multiplier)
        == restricted_quartic,
        "quartic residual lost its one-obstruction factorization",
    )

    witness_labels = {
        free_labels[parameter]: int(value)
        for parameter, value in sorted(witness.items())
    }
    maximum_provenance = max(
        len(representative) for _row, representative in pivots.values()
    )
    return {
        "ambient_variables": len(FACTOR.AMBIENT_COORDINATES),
        "mixed_jacobian_nonzero_rows": len(rows),
        "mixed_jacobian_rank": len(pivots),
        "mixed_tangent_dimension": len(tangent_basis),
        "maximum_echelon_conormal_provenance": maximum_provenance,
        "corrected_cubic_ambient_terms": len(cubic),
        "corrected_cubic_coefficient_set": [-1, 1],
        "cubic_echelon_conormal_factors": len(quotients),
        "cubic_quadratic_multiplier_terms": sum(map(len, quotients.values())),
        "cubic_division_steps": division_steps,
        "cubic_multiplier_coefficient_set": [-2, -1, 1, 2],
        "cubic_remainder_terms": len(remainder),
        "cubic_formal_arc_conclusion": (
            "H_0 is O(t^4) before imposing second-liftability"
        ),
        "corrected_quartic_ambient_terms": len(quartic),
        "corrected_quartic_tangent_terms": len(restricted_quartic),
        "corrected_quartic_tangent_factorization": (
            "-2*z_0400*z_1601*(z_3710+z_3711)*(z_6701-z_6711)"
        ),
        "quartic_tangent_witness": witness_labels,
        "quartic_tangent_witness_value": [
            witness_value.numerator, witness_value.denominator
        ],
        "second_lift_obstruction_rank": len(obstruction_pivots),
        "selected_quartic_obstruction": (
            "z_0400*(z_3710+z_3711)"
        ),
        "quartic_obstruction_multiplier": (
            "-2*z_1601*(z_6701-z_6711)"
        ),
        "quartic_interpretation": (
            "the tangent rectangle is one quadratic multiplier times "
            "a second-lift obstruction"
        ),
        "formal_arc_conclusion": "H_0 is O(t^5) on every mixed-fibre arc",
        "higher_arc_coefficient_independence": (
            "after full-equation corrections the residual starts in "
            "degree four, so its t^4 coefficient is R4(v) and contains "
            "neither the second arc coefficient w nor the third u"
        ),
    }


def main():
    ledger = audit()
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                "frozen cubic-conormal ledger digest changed")
    print(
        "n=8 colour-zero cubic conormal: PASS; "
        "cubic=166 terms -> 33 conormals/159 multipliers/remainder 0; "
        f"quartic={ledger['corrected_quartic_ambient_terms']} terms, "
        "R4=-2*z1601*(z6701-z6711)*O3, H0=O(t^5)"
    )
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
