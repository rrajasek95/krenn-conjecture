#!/usr/bin/env python3
"""Exact second-jet audit at the n=8 one-pure mixed torus.

At the rational specialization of the five-parameter mixed-ideal family,
the first differentials of H_0 and H_1 are selected mixed differentials.
This checker proves more: the corresponding quadratic differences vanish
on the entire 56-dimensional mixed tangent space.  Hence every formal arc
in the mixed fibre through this point has H_0,H_1 = O(t^3).
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
TANGENT_CHECKER = HERE / "verify_n8_counterexample_pure_tangent.py"
SPEC = importlib.util.spec_from_file_location("n8_tangent", TANGENT_CHECKER)
TANGENT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(TANGENT)

FULL = TANGENT.FULL
COORDINATE_VALUES = TANGENT.COORDINATE_VALUES

PURE_WORD_0 = (0,) * 8
PURE_WORD_1 = (1,) * 8
MIXED_WORD_0 = TANGENT.MIXED_CONORMAL_WORD_0
MIXED_WORD_1 = TANGENT.MIXED_CONORMAL_WORD_1

EXPECTED_LEDGER_SHA256 = (
    "6b0e0c42f352708e65ed720bfbc939eb8bba6e21d30b65a1dfb58d3ac2fb3666"
)


def exact_kernel(pivots, dimension):
    """Back-substitute in a normalized left-echelon row basis."""
    free_columns = tuple(index for index in range(dimension)
                         if index not in pivots)
    basis = []
    for free in free_columns:
        vector = {free: Fraction(1)}
        for pivot in sorted(pivots, reverse=True):
            value = -sum(
                coefficient * vector.get(index, Fraction(0))
                for index, coefficient in pivots[pivot].items()
                if index != pivot
            )
            if value:
                vector[pivot] = value
        basis.append(vector)
    return free_columns, tuple(basis)


def quadratic_form(word, coordinate_index, point):
    """Coefficient of t^2 in H_word(point+t*v), as pairs -> scalar."""
    answer = defaultdict(int)
    for matching_term in FULL.word_terms(word):
        for first, second in combinations(range(4), 2):
            coefficient = 1
            for position, coordinate in enumerate(matching_term):
                if position not in (first, second):
                    coefficient *= point.get(coordinate, 0)
            if coefficient:
                pair = tuple(sorted((
                    coordinate_index[matching_term[first]],
                    coordinate_index[matching_term[second]],
                )))
                answer[pair] += coefficient
    return {pair: coefficient for pair, coefficient in answer.items()
            if coefficient}


def subtract(left, right):
    return {
        pair: left.get(pair, 0) - right.get(pair, 0)
        for pair in left.keys() | right.keys()
        if left.get(pair, 0) != right.get(pair, 0)
    }


def evaluate_quadratic(form, vector):
    return sum(
        coefficient * vector.get(left, 0) * vector.get(right, 0)
        for (left, right), coefficient in form.items()
    )


def evaluate_polar(form, left_vector, right_vector):
    return sum(
        coefficient * (
            left_vector.get(left, 0) * right_vector.get(right, 0)
            + left_vector.get(right, 0) * right_vector.get(left, 0)
        )
        for (left, right), coefficient in form.items()
    )


def coefficient_value(word, point):
    return sum(
        prod(point.get(coordinate, 0) for coordinate in matching_term)
        for matching_term in FULL.word_terms(word)
    )


def audit():
    ambient_coordinates = tuple(
        (left, right, left_colour, right_colour)
        for left, right in combinations(range(8), 2)
        for left_colour in FULL.COLOURS
        for right_colour in FULL.COLOURS
    )
    coordinate_index = {coordinate: index
                        for index, coordinate in enumerate(ambient_coordinates)}
    point = {coordinate: sign for coordinate, (sign, _exponent)
             in COORDINATE_VALUES.items()}

    mixed_rows = []
    for word in product(FULL.COLOURS, repeat=8):
        if len(set(word)) == 1:
            continue
        gradient = TANGENT.specialized_gradient(word)
        if gradient:
            mixed_rows.append(gradient)

    pivots = TANGENT.exact_sparse_rank(mixed_rows, coordinate_index)
    free_columns, tangent_basis = exact_kernel(pivots, len(ambient_coordinates))
    require(len(pivots) == 196, "mixed Jacobian rank changed")
    require(len(tangent_basis) == 56, "mixed tangent dimension changed")

    # Replay the complete tangent-kernel assertion against every nonzero row.
    for row in mixed_rows:
        indexed_row = {coordinate_index[coordinate]: Fraction(value)
                       for coordinate, value in row.items()}
        for vector in tangent_basis:
            require(
                sum(coefficient * vector.get(index, Fraction(0))
                    for index, coefficient in indexed_row.items()) == 0,
                "constructed vector escaped the mixed tangent kernel",
            )
    require(all(value in (Fraction(-1), Fraction(1))
                for vector in tangent_basis for value in vector.values()),
            "unexpected coefficient in the exact tangent basis")

    pairs = ((PURE_WORD_0, MIXED_WORD_0), (PURE_WORD_1, MIXED_WORD_1))
    quadratic_ledgers = []
    for pure_word, mixed_word in pairs:
        require(coefficient_value(pure_word, point) == 0,
                "selected pure coefficient does not vanish at the point")
        require(coefficient_value(mixed_word, point) == 0,
                "selected mixed coefficient does not vanish at the point")
        require(TANGENT.specialized_gradient(pure_word)
                == TANGENT.specialized_gradient(mixed_word),
                "selected pure and mixed first differentials diverged")

        pure_quadratic = quadratic_form(pure_word, coordinate_index, point)
        mixed_quadratic = quadratic_form(mixed_word, coordinate_index, point)
        difference = subtract(pure_quadratic, mixed_quadratic)
        require(difference, "quadratic ambient difference unexpectedly vanished")

        diagonal_checks = 0
        polar_checks = 0
        for position, vector in enumerate(tangent_basis):
            require(evaluate_quadratic(difference, vector) == 0,
                    "quadratic difference survives on a tangent basis vector")
            diagonal_checks += 1
            for other in tangent_basis[:position]:
                require(evaluate_polar(difference, vector, other) == 0,
                        "polar quadratic difference survives on tangent space")
                polar_checks += 1

        quadratic_ledgers.append({
            "pure_colour": pure_word[0],
            "mixed_word": list(mixed_word),
            "ambient_quadratic_difference_terms": len(difference),
            "tangent_diagonal_checks": diagonal_checks,
            "tangent_polar_checks": polar_checks,
            "restricted_quadratic_rank": 0,
        })

    return {
        "ambient_variables": len(ambient_coordinates),
        "mixed_jacobian_nonzero_rows": len(mixed_rows),
        "mixed_jacobian_rank": len(pivots),
        "mixed_tangent_dimension": len(tangent_basis),
        "free_tangent_columns": len(free_columns),
        "maximum_tangent_basis_support": max(map(len, tangent_basis)),
        "tangent_basis_coefficient_set": [-1, 1],
        "quadratic_locks": quadratic_ledgers,
        "formal_arc_conclusion": "H_0,H_1 are O(t^3) on every mixed-fibre arc",
    }


def main():
    ledger = audit()
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                "frozen second-jet ledger digest changed")
    print(
        "n=8 counterexample pure second jet: PASS; "
        f"Jrank={ledger['mixed_jacobian_rank']}, "
        f"Tdim={ledger['mixed_tangent_dimension']}, "
        "restricted quadratics=(0,0), H0,H1=O(t^3)"
    )
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
