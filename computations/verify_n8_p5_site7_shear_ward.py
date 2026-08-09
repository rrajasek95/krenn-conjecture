#!/usr/bin/env python3
"""Certify the exact site-7 shear acting on the P5 Rees chart.

The bend direction z46 is not the orbit tangent of the translated centre:
the centre has zero 27 and 37 edge blocks.  There is nevertheless an exact
and useful fixed-point action.  The square-zero site-7 shear E20+E21 fixes the
centre and sends z44,z45 to z46 (and z52,z53 to z54).  This checker also
exports its induced action on the 196-dimensional ambient-normal quotient and
checks the corresponding Ward identities on every matching coefficient.
"""

from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
QQ = Fraction


def load_module(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


AFFINITY = load_module(
    "n8_p5_affinity_for_site7_ward",
    "verify_n8_p5_rees_chart_affinity.py",
)
TAILS = load_module(
    "n8_p5_tails_for_site7_ward",
    "verify_n8_p5_streamed_degree7_mixed_tails.py",
)
LOCAL = AFFINITY.LOCAL
P5 = AFFINITY.P5
FACTOR = LOCAL.FACTOR
FULL = LOCAL.SOURCE.FULL

EXPECTED_LEDGER_SHA256 = (
    "957abd7f8456dda477050cd438f15d442a0a3614fb5b98dca126b0e098cb810a"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def add_vector(target, source, scale=QQ(1)):
    for coordinate, coefficient in source.items():
        value = target.get(coordinate, QQ(0)) + scale * coefficient
        if value:
            target[coordinate] = value
        else:
            target.pop(coordinate, None)


def site7_nilpotent(vector):
    """Infinitesimal A_{u7} -> A_{u7}(I+rho(E20+E21))^T."""

    answer = {}
    for coordinate, coefficient in vector.items():
        left, right, left_colour, right_colour = (
            FACTOR.AMBIENT_COORDINATES[coordinate]
        )
        if right == 7 and right_colour in (0, 1):
            output = FACTOR.COORDINATE_INDEX[
                (left, right, left_colour, 2)
            ]
            answer[output] = answer.get(output, QQ(0)) + coefficient
    return {coordinate: coefficient for coordinate, coefficient in answer.items()
            if coefficient}


def tangent_coordinates(reducer, vector):
    coefficients = {
        parameter: vector.get(coordinate, QQ(0))
        for parameter, coordinate in enumerate(reducer.free_columns)
        if vector.get(coordinate, QQ(0))
    }
    replay = {}
    for parameter, coefficient in coefficients.items():
        add_vector(replay, reducer.data["tangent_basis"][parameter], coefficient)
    require(replay == vector, "vector left the mixed tangent space")
    return coefficients


def normal_coordinates(reducer, vector):
    answer = {}
    for pivot, (row, _representative) in reducer.jacobian_pivots.items():
        value = sum(
            coefficient * vector.get(coordinate, QQ(0))
            for coordinate, coefficient in row.items()
        )
        if value:
            answer[pivot] = value
    return answer


def ward_derivative_word(word):
    if word[7] != 2:
        return {}
    return {
        word[:7] + (0,): QQ(1),
        word[:7] + (1,): QQ(1),
    }


def source_derivative_terms(word):
    """Differentiate the literal 105 matching monomials under the shear."""

    answer = {}
    for term in FULL.word_terms(word):
        for position, coordinate in enumerate(term):
            left, right, left_colour, right_colour = coordinate
            if right != 7 or right_colour != 2:
                continue
            for input_colour in (0, 1):
                output = list(term)
                output[position] = (
                    left, right, left_colour, input_colour
                )
                monomial = tuple(sorted(output))
                answer[monomial] = answer.get(monomial, 0) + 1
    return {monomial: coefficient for monomial, coefficient in answer.items()
            if coefficient}


def word_polynomial(word):
    answer = {}
    for term in FULL.word_terms(word):
        monomial = tuple(sorted(term))
        answer[monomial] = answer.get(monomial, 0) + 1
    return answer


def ward_polynomial(word):
    answer = {}
    for replacement, coefficient in ward_derivative_word(word).items():
        source = word_polynomial(replacement)
        for monomial, value in source.items():
            answer[monomial] = answer.get(monomial, 0) + coefficient * value
    return {monomial: coefficient for monomial, coefficient in answer.items()
            if coefficient}


def encoded_action(action):
    return [
        {
            "source_index": source,
            "source_cell": list(FACTOR.AMBIENT_COORDINATES[source]),
            "targets": [
                {
                    "target_index": target,
                    "target_cell": list(FACTOR.AMBIENT_COORDINATES[target]),
                    "numerator": coefficient.numerator,
                    "denominator": coefficient.denominator,
                }
                for target, coefficient in sorted(targets.items())
            ],
        }
        for source, targets in sorted(action.items())
    ]


def functional_ward_pure_terms(reducer, one_based_row):
    pivot = tuple(reducer.data["obstruction_pivots"])[one_based_row - 1]
    functional = reducer.obstruction_functional(pivot)
    answer = {}
    for word_index, coefficient in functional.items():
        word = LOCAL.THIRD.MIXED_WORDS[word_index]
        for output, ward_coefficient in ward_derivative_word(word).items():
            if len(set(output)) == 1:
                answer[output] = (
                    answer.get(output, QQ(0))
                    + coefficient * ward_coefficient
                )
    return {word: coefficient for word, coefficient in answer.items()
            if coefficient}


def audit():
    reducer = LOCAL.LocalReducer()

    point = {
        FACTOR.COORDINATE_INDEX[coordinate]: QQ(value)
        for coordinate, value in FACTOR.POINT.items()
    }
    require(not site7_nilpotent(point),
            "the site-7 shear stopped fixing the translated centre")
    require(all(
        not (
            FACTOR.POINT.get((u, 7, left_colour, 0), 0)
            + FACTOR.POINT.get((u, 7, left_colour, 1), 0)
        )
        for u in range(7) for left_colour in range(3)
    ), "site-7 fixed-point cancellation changed")

    tangent_action = {}
    for parameter, direction in enumerate(reducer.data["tangent_basis"]):
        image = site7_nilpotent(direction)
        if image:
            tangent_action[parameter] = tangent_coordinates(reducer, image)
        require(not site7_nilpotent(image),
                f"site-7 tangent action stopped being square-zero at z{parameter}")
    expected_tangent_action = {
        44: {46: QQ(1)},
        45: {46: QQ(1)},
        52: {54: QQ(1)},
        53: {54: QQ(1)},
    }
    require(tangent_action == expected_tangent_action,
            "P5 tangent shear action changed")
    require(all(
        not site7_nilpotent(reducer.data["tangent_basis"][parameter])
        for parameter in P5.P5_NORMAL_VARIABLES
    ), "a transverse P5 direction acquired a site-7 shear image")

    directions = TAILS.normal_directions(reducer)
    normal_action = {}
    tangent_remainders = {}
    for source, direction in directions.items():
        image = site7_nilpotent(direction)
        coordinates = normal_coordinates(reducer, image)
        if coordinates:
            normal_action[source] = coordinates
        remainder = dict(image)
        for target, coefficient in coordinates.items():
            add_vector(remainder, directions[target], -coefficient)
        if remainder:
            tangent_remainders[source] = tangent_coordinates(
                reducer, remainder
            )

    require(len(normal_action) == 31, "normal shear source count changed")
    require(sum(map(len, normal_action.values())) == 31,
            "normal shear stopped being a 31-arrow partial matching")
    require(all(
        coefficient == QQ(1)
        for targets in normal_action.values()
        for coefficient in targets.values()
    ), "normal shear acquired a nonunit arrow")
    normal_square = {}
    for source, middle_targets in normal_action.items():
        for middle, left_coefficient in middle_targets.items():
            for target, right_coefficient in normal_action.get(middle, {}).items():
                normal_square[target] = (
                    normal_square.get(target, QQ(0))
                    + left_coefficient * right_coefficient
                )
    require(not {key: value for key, value in normal_square.items() if value},
            "normal quotient shear stopped being square-zero")
    require(tangent_remainders == {
        FACTOR.COORDINATE_INDEX[(0, 7, 2, 0)]: {24: QQ(1)},
        FACTOR.COORDINATE_INDEX[(0, 7, 2, 1)]: {24: QQ(1)},
    }, "normal shear tangent remainders changed")

    ward_words = 0
    ward_nonzero = 0
    for word in __import__("itertools").product(FULL.COLOURS, repeat=8):
        word = tuple(word)
        require(source_derivative_terms(word) == ward_polynomial(word),
                f"site-7 Ward identity failed at {word}")
        ward_words += 1
        ward_nonzero += bool(ward_derivative_word(word))
    require(ward_words == 3 ** 8 and ward_nonzero == 3 ** 7,
            "site-7 Ward word counts changed")

    # In the quotient by mixed output coordinates, these are the two
    # exceptional length-two Ward modules: delta(m_a)=H_a.
    near_pure_0 = (0,) * 7 + (2,)
    near_pure_1 = (1,) * 7 + (2,)
    require(ward_derivative_word(near_pure_0) == {
        (0,) * 8: QQ(1),
        (0,) * 7 + (1,): QQ(1),
    }, "colour-zero Ward pair changed")
    require(ward_derivative_word(near_pure_1) == {
        (1,) * 7 + (0,): QQ(1),
        (1,) * 8: QQ(1),
    }, "colour-one Ward pair changed")

    # Exact counterguards for an over-strong promotion claim.
    # On P5, delta=b*d/dz46+(z52+z53)*d/dz54, hence
    # delta(z9*z25-z11*z46)=-z11*b.  The dense generic-L centre is therefore
    # transverse, not invariant, under the constant shear.
    generic_l_derivative = "-z11*(z44+z45)"
    raw_rows_pure = {
        str(row): functional_ward_pure_terms(reducer, row)
        for row in (30, 33)
    }
    require(not any(raw_rows_pure.values()),
            "raw Q30/Q33 unexpectedly acquired a pure Ward term")

    ledger = {
        "site_action": "N=E20+E21 at site 7; N^2=0",
        "translated_center_fixed": True,
        "bare_orbit_tangent_is_z46": False,
        "tangent_action": {
            "z44": "z46", "z45": "z46",
            "z52": "z54", "z53": "z54",
        },
        "finite_p5_action": (
            "z46 -> z46+rho*(z44+z45), "
            "z54 -> z54+rho*(z52+z53)"
        ),
        "normal_quotient": {
            "dimension": len(directions),
            "nonzero_source_coordinates": len(normal_action),
            "arrows": sum(map(len, normal_action.values())),
            "square_zero": True,
            "action": encoded_action(normal_action),
            "tangent_remainders": [
                {
                    "source_index": source,
                    "source_cell": list(FACTOR.AMBIENT_COORDINATES[source]),
                    "tangent": {f"z{key}": str(value)
                                for key, value in sorted(targets.items())},
                }
                for source, targets in sorted(tangent_remainders.items())
            ],
        },
        "ward_audit": {
            "words": ward_words,
            "nonzero_derivatives": ward_nonzero,
            "rule": "delta H_(w,2)=H_(w,0)+H_(w,1)",
            "pure_modules_mod_mixed": [
                "delta H_00000002 = H_00000000 (mod I_mix)",
                "delta H_11111112 = H_11111111 (mod I_mix)",
            ],
        },
        "promotion_guards": {
            "generic_L_derivative": generic_l_derivative,
            "generic_L_is_constant_shear_invariant": False,
            "raw_M30_M33_pure_Ward_terms": {
                row: len(values) for row, values in raw_rows_pure.items()
            },
            "consequence": (
                "the constant shear and its equivariant normal coordinates "
                "do not alone prove the all-order Nakayama recurrence; a "
                "filtered Koszul correction after the Schur graph is needed"
            ),
        },
        "scope_guard": (
            "exact source/tangent/normal-quotient covariance and Ward "
            "transgression; no full-germ mixed or pure membership"
        ),
    }
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "P5 site-7 shear/Ward ledger changed")
    print(json.dumps(ledger, indent=2, sort_keys=True))
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    audit()
