#!/usr/bin/env python3
"""Exact pure-map tangent audit at the n=8 mixed-ideal torus family.

At the five-parameter family from verify_n8_localized_radical_counterexample,
this checker proves in Kahler differentials that dH_0 and dH_1 lie in the
mixed conormal, whereas dH_2 is nonzero on the mixed tangent space.  Thus
the differential of the pure-coefficient map has rank exactly one and all
its 2 by 2 wedges vanish.  It also computes the exact generic mixed
Jacobian rank (196), using the fact that the Laurent family is a port-torus
orbit of its rational specialization.
"""

from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import importlib.util
import json
from pathlib import Path


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


HERE = Path(__file__).resolve().parent
COUNTEREXAMPLE_CHECKER = HERE / "verify_n8_localized_radical_counterexample.py"
SPEC = importlib.util.spec_from_file_location("n8_counterexample", COUNTEREXAMPLE_CHECKER)
COUNTEREXAMPLE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(COUNTEREXAMPLE)

FULL = COUNTEREXAMPLE.FULL
COORDINATE_VALUES = COUNTEREXAMPLE.COORDINATE_VALUES
PARAMETERS = COUNTEREXAMPLE.PARAMETERS
ZERO_EXPONENT = COUNTEREXAMPLE.ZERO_EXPONENT

MIXED_CONORMAL_WORD_0 = (0, 0, 0, 0, 0, 0, 1, 0)
MIXED_CONORMAL_WORD_1 = (1, 1, 0, 0, 0, 1, 1, 1)
MIXED_EQUALS_PURE_0_WORD = (2, 1, 0, 0, 0, 0, 1, 2)

EXPECTED_LEDGER_SHA256 = (
    "dd0eabe59c842ace287675100dfe98c35c50809deb4a31f4388eacc7f083f021"
)


def clean(polynomial):
    return {exponent: coefficient for exponent, coefficient
            in polynomial.items() if coefficient}


def add_term(polynomial, exponent, coefficient):
    value = polynomial.get(exponent, 0) + coefficient
    if value:
        polynomial[exponent] = value
    else:
        polynomial.pop(exponent, None)


def laurent_gradient(word):
    """Gradient as coordinate -> Laurent polynomial."""
    gradient = defaultdict(dict)
    for matching_term in FULL.word_terms(word):
        for differentiated, coordinate in enumerate(matching_term):
            sign = 1
            exponent = [0] * len(PARAMETERS)
            for position, other in enumerate(matching_term):
                if position == differentiated:
                    continue
                if other not in COORDINATE_VALUES:
                    break
                other_sign, other_exponent = COORDINATE_VALUES[other]
                sign *= other_sign
                exponent = [left + right for left, right
                            in zip(exponent, other_exponent)]
            else:
                add_term(gradient[coordinate], tuple(exponent), sign)
    return {coordinate: clean(polynomial)
            for coordinate, polynomial in gradient.items() if clean(polynomial)}


def shift_gradient(gradient, sign, exponent_shift):
    return {
        coordinate: {
            tuple(left + right for left, right
                  in zip(exponent, exponent_shift)): sign * coefficient
            for exponent, coefficient in polynomial.items()
        }
        for coordinate, polynomial in gradient.items()
    }


def specialized_gradient(word):
    """Gradient at a=b=c=d=e=1 as a sparse integer coordinate vector."""
    point = {coordinate: sign for coordinate, (sign, _exponent)
             in COORDINATE_VALUES.items()}
    gradient = defaultdict(int)
    for matching_term in FULL.word_terms(word):
        values = [point.get(coordinate, 0) for coordinate in matching_term]
        for differentiated, coordinate in enumerate(matching_term):
            value = 1
            for position, other_value in enumerate(values):
                if position != differentiated:
                    value *= other_value
            gradient[coordinate] += value
    return {coordinate: value for coordinate, value in gradient.items() if value}


def exact_sparse_rank(rows, coordinate_index):
    pivots = {}
    for row in rows:
        vector = {coordinate_index[coordinate]: Fraction(value)
                  for coordinate, value in row.items()}
        while vector:
            pivot = min(vector)
            value = vector[pivot]
            if pivot not in pivots:
                pivots[pivot] = {
                    index: coefficient / value
                    for index, coefficient in vector.items()
                }
                break
            basis = pivots[pivot]
            for index, coefficient in basis.items():
                new_value = vector.get(index, Fraction(0)) - value * coefficient
                if new_value:
                    vector[index] = new_value
                else:
                    vector.pop(index, None)
    return pivots


def solve_port_weights(parameter_index):
    """Express every coordinate exponent as a sum of two port weights."""
    ports = tuple(product(range(8), range(3)))
    port_index = {port: index for index, port in enumerate(ports)}
    pivots = {}
    for (left, right, left_colour, right_colour), (_sign, exponent) in (
            COORDINATE_VALUES.items()):
        vector = {
            port_index[left, left_colour]: Fraction(1),
            port_index[right, right_colour]: Fraction(1),
        }
        rhs = Fraction(exponent[parameter_index])
        while vector:
            pivot = min(vector)
            value = vector[pivot]
            if pivot not in pivots:
                vector = {index: coefficient / value
                          for index, coefficient in vector.items()}
                pivots[pivot] = (vector, rhs / value)
                break
            basis, basis_rhs = pivots[pivot]
            for index, coefficient in basis.items():
                new_value = vector.get(index, Fraction(0)) - value * coefficient
                if new_value:
                    vector[index] = new_value
                else:
                    vector.pop(index, None)
            rhs -= value * basis_rhs
        else:
            require(not rhs, "coordinate exponents are not port-torus weights")
    solution = [Fraction(0)] * len(ports)
    for pivot in sorted(pivots, reverse=True):
        row, rhs = pivots[pivot]
        solution[pivot] = rhs - sum(
            coefficient * solution[index]
            for index, coefficient in row.items() if index != pivot
        )
    for (left, right, left_colour, right_colour), (_sign, exponent) in (
            COORDINATE_VALUES.items()):
        require(
            solution[port_index[left, left_colour]]
            + solution[port_index[right, right_colour]]
            == exponent[parameter_index],
            "port-weight replay failed",
        )
    return {
        f"{vertex}{colour}": [weight.numerator, weight.denominator]
        for (vertex, colour), weight in zip(ports, solution) if weight
    }, len(pivots)


def restricted_matching_monomials(word):
    """Polynomial support after zeroing every coordinate outside the family."""
    answer = []
    for matching_term in FULL.word_terms(word):
        if all(coordinate in COORDINATE_VALUES for coordinate in matching_term):
            answer.append(tuple(sorted(
                coordinate for coordinate in matching_term
                if coordinate not in FULL.SUPPORT_SET
            )))
    return tuple(sorted(answer, key=repr))


def audit():
    pure_gradients = {
        colour: laurent_gradient((colour,) * 8) for colour in FULL.COLOURS
    }
    mixed_gradient_0 = laurent_gradient(MIXED_CONORMAL_WORD_0)
    mixed_gradient_1 = laurent_gradient(MIXED_CONORMAL_WORD_1)
    require(
        pure_gradients[0] == shift_gradient(
            mixed_gradient_0, 1, (0, 0, 0, 0, 1)
        ),
        "dH_0 is not e times the selected mixed differential",
    )
    require(
        pure_gradients[1] == shift_gradient(
            mixed_gradient_1, 1, (-1, 0, 0, 0, 0)
        ),
        "dH_1 is not a^-1 times the selected mixed differential",
    )

    # Four standard coordinate directions witness that dH_2 survives in
    # the tangent quotient: all mixed derivatives in these columns vanish.
    pure_two_columns = tuple(sorted(pure_gradients[2]))
    require(len(pure_two_columns) == 4, "pure-two gradient support")
    mixed_laurent_gradients = []
    for word in product(FULL.COLOURS, repeat=8):
        if len(set(word)) == 1:
            continue
        gradient = laurent_gradient(word)
        if gradient:
            mixed_laurent_gradients.append(gradient)
        require(not any(coordinate in gradient
                        for coordinate in pure_two_columns),
                "a mixed differential meets the pure-two tangent columns")
    require(all(pure_gradients[2][coordinate] == {ZERO_EXPONENT: 1}
                for coordinate in pure_two_columns),
            "pure-two tangent value changed")

    # Exact rational Jacobian rank.  The parameter exponents are port-torus
    # weights, so the generic matrix is obtained from this one by invertible
    # row and column diagonal scalings and has the same rank.
    ambient_coordinates = tuple(
        (left, right, left_colour, right_colour)
        for left, right in combinations(range(8), 2)
        for left_colour in FULL.COLOURS
        for right_colour in FULL.COLOURS
    )
    coordinate_index = {coordinate: index
                        for index, coordinate in enumerate(ambient_coordinates)}
    mixed_specialized_rows = []
    for word in product(FULL.COLOURS, repeat=8):
        if len(set(word)) == 1:
            continue
        gradient = specialized_gradient(word)
        if gradient:
            mixed_specialized_rows.append(gradient)
    pivots = exact_sparse_rank(mixed_specialized_rows, coordinate_index)
    require(len(mixed_specialized_rows) == 1312,
            "nonzero mixed Jacobian row count")
    require(len(pivots) == 196, "exact mixed Jacobian rank changed")
    require(all(value in (Fraction(-1), Fraction(1))
                for row in pivots.values() for value in row.values()),
            "unexpected coefficient growth in exact Jacobian basis")

    port_weights = {}
    for parameter_index, parameter in enumerate(PARAMETERS):
        weights, equation_rank = solve_port_weights(parameter_index)
        require(equation_rank == 17, "port-weight equation rank changed")
        port_weights[parameter] = weights

    # On this 18-extra coordinate torus, one mixed generator literally
    # restricts to H_0.  Hence saturating this stratum by H_0 H_1 H_2 gives
    # the unit ideal, independently of the chosen torus parametrization.
    require(
        restricted_matching_monomials((0,) * 8)
        == restricted_matching_monomials(MIXED_EQUALS_PURE_0_WORD),
        "restricted H_0 is no longer a mixed generator",
    )

    ledger = {
        "ambient_variables": len(ambient_coordinates),
        "mixed_jacobian_nonzero_rows": len(mixed_specialized_rows),
        "generic_mixed_jacobian_rank": len(pivots),
        "generic_mixed_tangent_dimension": len(ambient_coordinates) - len(pivots),
        "pure_map_tangent_rank": 1,
        "pure_wedge_rank": 0,
        "conormal_identities": [
            {
                "pure_colour": 0,
                "mixed_word": list(MIXED_CONORMAL_WORD_0),
                "factor_sign": 1,
                "factor_exponent": [0, 0, 0, 0, 1],
            },
            {
                "pure_colour": 1,
                "mixed_word": list(MIXED_CONORMAL_WORD_1),
                "factor_sign": 1,
                "factor_exponent": [-1, 0, 0, 0, 0],
            },
        ],
        "pure_two_tangent_columns": [
            COUNTEREXAMPLE.encode_variable(coordinate)
            for coordinate in pure_two_columns
        ],
        "port_weights": port_weights,
        "exceptional_torus_pure_zero_generator": {
            "pure_colour": 0,
            "equal_mixed_word": list(MIXED_EQUALS_PURE_0_WORD),
        },
        "local_pure_product_saturation": "unit ideal on the 18-extra torus stratum",
    }
    return ledger


def main():
    ledger = audit()
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                "frozen pure-tangent ledger digest changed")
    print(
        "n=8 counterexample pure tangent: PASS; "
        f"Jrank={ledger['generic_mixed_jacobian_rank']}, "
        f"Tdim={ledger['generic_mixed_tangent_dimension']}, "
        f"rank(dpi)={ledger['pure_map_tangent_rank']}, wedges=0"
    )
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
