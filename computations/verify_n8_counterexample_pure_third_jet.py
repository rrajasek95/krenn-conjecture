#!/usr/bin/env python3
"""Exact third-jet lock at the n=8 one-pure mixed torus.

At the rational specialization of the five-parameter mixed-ideal family,
the two missing pure coefficients already vanish through order two on every
mixed-fibre arc.  This checker constructs the full 56-dimensional tangent
kernel and the exact second-order obstruction map.  A canonical right
inverse for the mixed Jacobian then gives the two cubic pure outputs.  The
colour-zero output is identically zero, while the colour-one output is a
single tangent parameter times one scalar second-order obstruction.  Hence
both outputs vanish on every second-order-liftable tangent direction, and
H_0,H_1 are O(t^4) on every formal mixed-fibre arc through the point.
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
SECOND_JET_CHECKER = HERE / "verify_n8_counterexample_pure_second_jet.py"
SPEC = importlib.util.spec_from_file_location("n8_second_jet", SECOND_JET_CHECKER)
SECOND = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SECOND)

TANGENT = SECOND.TANGENT
FULL = SECOND.FULL
COORDINATE_VALUES = SECOND.COORDINATE_VALUES
PURE_WORD_0 = SECOND.PURE_WORD_0
PURE_WORD_1 = SECOND.PURE_WORD_1
MIXED_WORD_0 = SECOND.MIXED_WORD_0
MIXED_WORD_1 = SECOND.MIXED_WORD_1
QQ = Fraction

OBSTRUCTION_WORD = (1, 1, 0, 0, 1, 0, 0, 1)

EXPECTED_LEDGER_SHA256 = (
    "948b5d65f5b236d1fca15536344362c02aea6c1d427e2bb6d7b2d886ceb6bab2"
)


AMBIENT_COORDINATES = tuple(
    (left, right, left_colour, right_colour)
    for left, right in combinations(range(8), 2)
    for left_colour in FULL.COLOURS
    for right_colour in FULL.COLOURS
)
COORDINATE_INDEX = {
    coordinate: index for index, coordinate in enumerate(AMBIENT_COORDINATES)
}
MIXED_WORDS = tuple(
    word for word in product(FULL.COLOURS, repeat=8)
    if len(set(word)) > 1
)
MIXED_WORD_INDEX = {word: index for index, word in enumerate(MIXED_WORDS)}
POINT = {
    coordinate: QQ(sign)
    for coordinate, (sign, _exponent) in COORDINATE_VALUES.items()
}


def encode_coordinate(coordinate):
    return "".join(map(str, coordinate))


def clean(vector):
    return {index: value for index, value in vector.items() if value}


def add_scaled(target, source, scale=QQ(1)):
    for index, coefficient in source.items():
        value = target.get(index, QQ(0)) + scale * coefficient
        if value:
            target[index] = value
        else:
            target.pop(index, None)


def exact_row_echelon(vectors):
    pivots = {}
    for incoming in vectors:
        vector = {index: QQ(value) for index, value in incoming.items() if value}
        while vector:
            pivot = min(vector)
            value = vector[pivot]
            if pivot not in pivots:
                pivots[pivot] = {
                    index: coefficient / value
                    for index, coefficient in vector.items()
                }
                break
            add_scaled(vector, pivots[pivot], -value)
    return pivots


def exact_column_echelon_with_representatives(rows):
    columns = [dict() for _coordinate in AMBIENT_COORDINATES]
    for row_index, row in enumerate(rows):
        for column_index, coefficient in row.items():
            columns[column_index][row_index] = QQ(coefficient)

    pivots = {}
    representatives = {}
    for column_index, incoming in enumerate(columns):
        vector = dict(incoming)
        representative = {column_index: QQ(1)}
        while vector:
            pivot = min(vector)
            value = vector[pivot]
            if pivot not in pivots:
                pivots[pivot] = {
                    index: coefficient / value
                    for index, coefficient in vector.items()
                }
                representatives[pivot] = {
                    index: coefficient / value
                    for index, coefficient in representative.items()
                }
                break
            add_scaled(vector, pivots[pivot], -value)
            add_scaled(representative, representatives[pivot], -value)
    return pivots, representatives


def decompose_in_column_span(target, pivots, representatives):
    """Write target=J(preimage)+residual in the fixed echelon quotient."""
    target = {index: QQ(value) for index, value in target.items() if value}
    preimage = {}
    residual = {}
    while target:
        pivot = min(target)
        value = target[pivot]
        if pivot not in pivots:
            residual[pivot] = value
            target.pop(pivot)
            continue
        add_scaled(target, pivots[pivot], -value)
        add_scaled(preimage, representatives[pivot], value)
    return preimage, residual


def mixed_jacobian_rows():
    rows = []
    for word in MIXED_WORDS:
        gradient = TANGENT.specialized_gradient(word)
        rows.append({
            COORDINATE_INDEX[coordinate]: QQ(value)
            for coordinate, value in gradient.items()
        })
    return tuple(rows)


def quadratic_pair_columns(words):
    """Hasse coefficient of tangent-coordinate pairs, indexed by words."""
    answer = defaultdict(lambda: defaultdict(int))
    for row_index, word in enumerate(words):
        for matching_term in FULL.word_terms(word):
            point_values = [POINT.get(coordinate, QQ(0))
                            for coordinate in matching_term]
            indices = [COORDINATE_INDEX[coordinate]
                       for coordinate in matching_term]
            for first, second in combinations(range(4), 2):
                remaining = [position for position in range(4)
                             if position not in (first, second)]
                coefficient = (point_values[remaining[0]]
                               * point_values[remaining[1]])
                if coefficient:
                    pair = tuple(sorted((indices[first], indices[second])))
                    answer[pair][row_index] += coefficient
    return {pair: clean(column) for pair, column in answer.items()}


def cubic_triple_columns(words):
    """Hasse coefficient of tangent-coordinate triples, indexed by words."""
    answer = defaultdict(lambda: defaultdict(int))
    for row_index, word in enumerate(words):
        for matching_term in FULL.word_terms(word):
            point_values = [POINT.get(coordinate, QQ(0))
                            for coordinate in matching_term]
            indices = [COORDINATE_INDEX[coordinate]
                       for coordinate in matching_term]
            for selected in combinations(range(4), 3):
                remaining = next(position for position in range(4)
                                 if position not in selected)
                coefficient = point_values[remaining]
                if coefficient:
                    triple = tuple(sorted(indices[position]
                                          for position in selected))
                    answer[triple][row_index] += coefficient
    return {triple: clean(column) for triple, column in answer.items()}


def quadratic_value(vector, pair_columns):
    answer = {}
    for left, right in combinations(sorted(vector), 2):
        scale = vector[left] * vector[right]
        if scale:
            add_scaled(answer, pair_columns.get((left, right), {}), scale)
    return answer


def bilinear_value(left_vector, right_vector, pair_columns):
    answer = {}
    # Ordered support pairs produce the two polar terms without scanning all
    # 11,646 ambient coordinate-pair columns for every small tangent vector.
    for left, left_value in left_vector.items():
        for right, right_value in right_vector.items():
            if left == right:
                continue
            pair = tuple(sorted((left, right)))
            column = pair_columns.get(pair)
            if column:
                add_scaled(answer, column, left_value * right_value)
    return answer


def add_polynomial_term(polynomial, monomial, coefficient):
    monomial = tuple(sorted(monomial))
    value = polynomial.get(monomial, QQ(0)) + coefficient
    if value:
        polynomial[monomial] = value
    else:
        polynomial.pop(monomial, None)


def corrected_bilinear(vector, second_vector, special_pair_columns):
    values = bilinear_value(vector, second_vector, special_pair_columns)
    return (
        values.get(0, QQ(0)) - values.get(3, QQ(0)),
        values.get(1, QQ(0)) - values.get(4, QQ(0)),
    )


def multiply_by_parameter(polynomial, parameter, scale=QQ(1)):
    answer = {}
    for monomial, coefficient in polynomial.items():
        add_polynomial_term(answer, monomial + (parameter,),
                            scale * coefficient)
    return answer


def audit():
    jacobian_rows = mixed_jacobian_rows()
    nonzero_rows = tuple(row for row in jacobian_rows if row)
    row_pivots = exact_row_echelon(nonzero_rows)
    free_columns, tangent_basis = SECOND.exact_kernel(
        row_pivots, len(AMBIENT_COORDINATES)
    )
    require(len(row_pivots) == 196, "mixed Jacobian rank changed")
    require(len(tangent_basis) == 56, "mixed tangent dimension changed")
    require(all(value in (QQ(-1), QQ(1))
                for vector in tangent_basis for value in vector.values()),
            "exact tangent basis ceased to be signed")

    column_pivots, column_representatives = (
        exact_column_echelon_with_representatives(jacobian_rows)
    )
    require(len(column_pivots) == 196,
            "row and column Jacobian ranks diverged")

    mixed_pair_columns = quadratic_pair_columns(MIXED_WORDS)
    special_words = (
        PURE_WORD_0, PURE_WORD_1, (2,) * 8, MIXED_WORD_0, MIXED_WORD_1,
    )
    special_pair_columns = quadratic_pair_columns(special_words)
    special_triple_columns = cubic_triple_columns(special_words)

    quadratic_coefficients = {}
    obstruction_coefficients = {}
    second_coefficients = {}
    for left, left_vector in enumerate(tangent_basis):
        for right in range(left, len(tangent_basis)):
            right_vector = tangent_basis[right]
            if left == right:
                coefficient = quadratic_value(left_vector, mixed_pair_columns)
            else:
                coefficient = bilinear_value(
                    left_vector, right_vector, mixed_pair_columns
                )
            monomial = (left, right)
            quadratic_coefficients[monomial] = coefficient
            preimage, residual = decompose_in_column_span(
                coefficient, column_pivots, column_representatives
            )
            obstruction_coefficients[monomial] = residual
            second_coefficients[monomial] = {
                index: -value for index, value in preimage.items()
            }

    obstruction_rank = len(exact_row_echelon(
        obstruction_coefficients.values()
    ))
    obstructed_cross_monomials = sum(
        bool(residual) for monomial, residual in obstruction_coefficients.items()
        if monomial[0] != monomial[1]
    )
    require(obstruction_rank == 39,
            "exact second-order obstruction rank changed")
    require(obstructed_cross_monomials == 59,
            "obstructed tangent-basis pair count changed")
    require(all(not obstruction_coefficients[index, index]
                for index in range(len(tangent_basis))),
            "a tangent-basis axis stopped lifting to second order")

    cubic_outputs = [dict(), dict()]
    for tangent_parameter, tangent_vector in enumerate(tangent_basis):
        for quadratic_monomial, second_vector in second_coefficients.items():
            output = corrected_bilinear(
                tangent_vector, second_vector, special_pair_columns
            )
            for colour in range(2):
                add_polynomial_term(
                    cubic_outputs[colour],
                    (tangent_parameter,) + quadratic_monomial,
                    output[colour],
                )

    coordinate_forms = defaultdict(dict)
    for tangent_parameter, tangent_vector in enumerate(tangent_basis):
        for coordinate, coefficient in tangent_vector.items():
            coordinate_forms[coordinate][tangent_parameter] = coefficient
    for ambient_triple, word_values in special_triple_columns.items():
        differences = (
            word_values.get(0, QQ(0)) - word_values.get(3, QQ(0)),
            word_values.get(1, QQ(0)) - word_values.get(4, QQ(0)),
        )
        if differences == (0, 0):
            continue
        forms = [coordinate_forms[index] for index in ambient_triple]
        for left_parameter, left_value in forms[0].items():
            for middle_parameter, middle_value in forms[1].items():
                for right_parameter, right_value in forms[2].items():
                    monomial = (
                        left_parameter, middle_parameter, right_parameter
                    )
                    scale = left_value * middle_value * right_value
                    for colour in range(2):
                        add_polynomial_term(
                            cubic_outputs[colour], monomial,
                            scale * differences[colour],
                        )

    free_labels = tuple(
        encode_coordinate(AMBIENT_COORDINATES[index])
        for index in free_columns
    )
    label_index = {label: index for index, label in enumerate(free_labels)}
    obstruction_row = MIXED_WORD_INDEX[OBSTRUCTION_WORD]
    selected_obstruction = clean({
        monomial: residual.get(obstruction_row, QQ(0))
        for monomial, residual in obstruction_coefficients.items()
    })
    expected_obstruction = {
        tuple(sorted((label_index["0410"], label_index["1311"]))): QQ(2),
        tuple(sorted((label_index["0410"], label_index["3711"]))): QQ(-2),
        tuple(sorted((label_index["0411"], label_index["1311"]))): QQ(-2),
        tuple(sorted((label_index["0411"], label_index["3711"]))): QQ(2),
    }
    require(selected_obstruction == expected_obstruction,
            "selected scalar obstruction no longer factors as expected")
    require(not cubic_outputs[0],
            "the colour-zero cubic output ceased to vanish identically")
    expected_colour_one = multiply_by_parameter(
        selected_obstruction, label_index["3511"], QQ(-1)
    )
    require(cubic_outputs[1] == expected_colour_one,
            "the colour-one cubic output lost its obstruction factor")

    encoded_obstruction = [
        {
            "parameters": [free_labels[index] for index in monomial],
            "coefficient": [coefficient.numerator, coefficient.denominator],
        }
        for monomial, coefficient in sorted(selected_obstruction.items())
    ]
    encoded_cubic_one = [
        {
            "parameters": [free_labels[index] for index in monomial],
            "coefficient": [coefficient.numerator, coefficient.denominator],
        }
        for monomial, coefficient in sorted(cubic_outputs[1].items())
    ]
    return {
        "ambient_variables": len(AMBIENT_COORDINATES),
        "mixed_coefficients": len(MIXED_WORDS),
        "mixed_jacobian_nonzero_rows": len(nonzero_rows),
        "mixed_jacobian_rank": len(row_pivots),
        "mixed_tangent_dimension": len(tangent_basis),
        "second_obstruction_rank": obstruction_rank,
        "tangent_basis_axes_second_liftable": len(tangent_basis),
        "tangent_basis_cross_monomials": len(tangent_basis)
        * (len(tangent_basis) - 1) // 2,
        "obstructed_tangent_basis_cross_monomials": obstructed_cross_monomials,
        "selected_obstruction_word": list(OBSTRUCTION_WORD),
        "selected_obstruction_terms": encoded_obstruction,
        "selected_obstruction_factorization": (
            "2*(z_0410-z_0411)*(z_1311-z_3711)"
        ),
        "colour_zero_cubic_output_terms": 0,
        "colour_one_cubic_output_terms": encoded_cubic_one,
        "colour_one_cubic_factorization": "-z_3511*selected_obstruction",
        "formal_arc_conclusion": "H_0,H_1 are O(t^4) on every mixed-fibre arc",
    }


def main():
    ledger = audit()
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                "frozen third-jet ledger digest changed")
    print(
        "n=8 counterexample pure third jet: PASS; "
        f"Jrank={ledger['mixed_jacobian_rank']}, "
        f"Tdim={ledger['mixed_tangent_dimension']}, "
        f"obsrank={ledger['second_obstruction_rank']}, "
        "cubic=(0,-z_3511*obstruction), H0,H1=O(t^4)"
    )
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
