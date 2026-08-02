#!/usr/bin/env python3
"""Exact five-parameter common zero of the full n=8 mixed ideal.

All twelve boundary-support coordinates are normalized to one.  Eighteen
additional coordinates are Laurent monomials in five nonzero parameters;
every other one of the 252 endpoint-colour coordinates is zero.  Direct
Laurent-polynomial evaluation proves that all 3^8-3 mixed hafnian
coefficients vanish, while the boundary product is one.  Consequently the
boundary product is not in the radical of the mixed ideal for this n=8
chart.  Setting all five parameters to one gives a rational point.
"""

from collections import Counter, defaultdict
from hashlib import sha256
from itertools import product
import importlib.util
import json
from pathlib import Path


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


HERE = Path(__file__).resolve().parent
FULL_CHECKER = HERE / "verify_n8_full_source_cycle_product_membership.py"
FULL_SPEC = importlib.util.spec_from_file_location("n8_full", FULL_CHECKER)
FULL = importlib.util.module_from_spec(FULL_SPEC)
FULL_SPEC.loader.exec_module(FULL)

SPARSE_CHECKER = HERE / "verify_n8_localized_dual_edge_sparse_no_go.py"
SPARSE_SPEC = importlib.util.spec_from_file_location("n8_sparse", SPARSE_CHECKER)
SPARSE = importlib.util.module_from_spec(SPARSE_SPEC)
SPARSE_SPEC.loader.exec_module(SPARSE)

PARAMETERS = ("a", "b", "c", "d", "e")
ZERO_EXPONENT = (0,) * len(PARAMETERS)


def variable(code):
    require(len(code) == 4 and all(character.isdigit() for character in code),
            f"invalid variable code {code}")
    return tuple(map(int, code))


def encode_variable(coordinate):
    return "".join(map(str, coordinate))


# A nonzero coordinate value is (sign, Laurent exponent vector) and denotes
# sign*a^u0*b^u1*c^u2*d^u3*e^u4.
COORDINATE_VALUES = {
    coordinate: (1, ZERO_EXPONENT) for coordinate in FULL.SUPPORT_PRODUCT
}
COORDINATE_VALUES.update({
    variable("0210"): (1, (1, 0, 0, 0, 0)),       # a
    variable("0211"): (1, (0, 1, 0, 0, 0)),       # b
    variable("0310"): (1, (0, 0, 1, 0, 0)),       # c
    variable("1511"): (1, (0, 0, 0, 1, 0)),       # d
    variable("1610"): (1, (0, 0, 0, 0, 1)),       # e
    variable("2400"): (1, (1, 0, -1, 0, 0)),      # a/c
    variable("2401"): (1, (1, -1, 0, 0, 0)),      # a/b
    variable("2410"): (1, (0, 1, -1, 0, 0)),      # b/c
    variable("2510"): (1, (-1, 1, 0, 0, 0)),      # b/a
    variable("3401"): (1, (0, -1, 1, 0, 0)),      # c/b
    variable("3410"): (1, (0, 0, -1, 0, 0)),      # 1/c
    variable("3411"): (1, (0, -1, 0, 0, 0)),      # 1/b
    variable("3500"): (-1, (-1, 0, 1, 0, 0)),     # -c/a
    variable("3510"): (-1, (-1, 0, 0, 0, 0)),     # -1/a
    variable("5710"): (-1, (0, 0, 0, 1, -1)),     # -d/e
    variable("6701"): (-1, (0, 0, 0, -1, 1)),     # -e/d
    variable("6710"): (1, (0, 0, 0, 0, -1)),      # 1/e
    variable("6711"): (-1, (0, 0, 0, -1, 0)),     # -1/d
})

EXPECTED_LEDGER_SHA256 = (
    "f6660d88d238d84d3d5c6873666b2b53c4a12a95526041430a3b902d5727e99c"
)


def evaluate_word(word):
    """Return a Laurent polynomial as exponent -> integer coefficient."""
    answer = defaultdict(int)
    nonzero_terms = 0
    for matching_term in FULL.word_terms(word):
        sign = 1
        exponent = [0] * len(PARAMETERS)
        for coordinate in matching_term:
            if coordinate not in COORDINATE_VALUES:
                break
            coordinate_sign, coordinate_exponent = COORDINATE_VALUES[coordinate]
            sign *= coordinate_sign
            exponent = [left + right for left, right
                        in zip(exponent, coordinate_exponent)]
        else:
            nonzero_terms += 1
            answer[tuple(exponent)] += sign
    return {
        exponent: coefficient for exponent, coefficient in answer.items()
        if coefficient
    }, nonzero_terms


def encode_laurent(polynomial):
    return [
        {"coefficient": coefficient, "exponent": list(exponent)}
        for exponent, coefficient in sorted(polynomial.items())
    ]


def audit():
    require(len(FULL.SUPPORT_PRODUCT) == 12, "boundary support degree")
    require(len(COORDINATE_VALUES) == 30, "nonzero coordinate count")
    require(FULL.SUPPORT_SET <= frozenset(COORDINATE_VALUES),
            "a boundary coordinate is zero")
    require(frozenset(COORDINATE_VALUES) <= frozenset(SPARSE.DUAL_EDGE_SUPPORT),
            "counterexample escaped the audited 60-edge chart")
    for left, right, left_colour, right_colour in COORDINATE_VALUES:
        require(0 <= left < right < 8, "invalid endpoint pair")
        require(left_colour in FULL.COLOURS and right_colour in FULL.COLOURS,
                "invalid endpoint colour")

    values = {}
    supported_term_histogram = Counter()
    for word in product(FULL.COLOURS, repeat=8):
        value, nonzero_terms = evaluate_word(word)
        values[word] = value
        supported_term_histogram[nonzero_terms] += 1

    mixed_words = tuple(word for word in values if len(set(word)) > 1)
    pure_words = tuple(word for word in values if len(set(word)) == 1)
    require(len(mixed_words) == 3 ** 8 - 3, "mixed word count")
    require(all(not values[word] for word in mixed_words),
            "a mixed coefficient does not vanish identically")
    require(len(pure_words) == 3, "pure word count")
    pure_values = {word[0]: values[word] for word in pure_words}
    require(pure_values == {
        0: {}, 1: {}, 2: {ZERO_EXPONENT: 1},
    }, "pure coefficient tuple changed")

    # At a=b=c=d=e=1, a Laurent monomial is its sign.  This is a literal
    # rational point, not merely a generic-function-field construction.
    rational_specialization = {
        coordinate: sign for coordinate, (sign, _exponent)
        in COORDINATE_VALUES.items()
    }
    require(all(value in (-1, 1)
                for value in rational_specialization.values()),
            "specialized nonzero coordinate is not rational +/-1")
    support_product_value = 1
    for coordinate in FULL.SUPPORT_PRODUCT:
        support_product_value *= rational_specialization[coordinate]
    require(support_product_value == 1,
            "boundary product does not remain one")

    ledger = {
        "vertices": 8,
        "colours": 3,
        "ambient_pair_colour_variables": 28 * 9,
        "parameters": list(PARAMETERS),
        "nonzero_coordinates": len(COORDINATE_VALUES),
        "normalized_boundary_coordinates": len(FULL.SUPPORT_PRODUCT),
        "extra_nonzero_coordinates": (
            len(COORDINATE_VALUES) - len(FULL.SUPPORT_PRODUCT)
        ),
        "coordinate_values": [
            {
                "variable": encode_variable(coordinate),
                "sign": value[0],
                "exponent": list(value[1]),
            }
            for coordinate, value in sorted(COORDINATE_VALUES.items())
        ],
        "mixed_coefficients_checked": len(mixed_words),
        "mixed_nonzero_coefficients": 0,
        "pure_values": {
            str(colour): encode_laurent(value)
            for colour, value in sorted(pure_values.items())
        },
        "supported_matching_term_histogram": dict(sorted(
            supported_term_histogram.items()
        )),
        "rational_specialization": [
            {
                "variable": encode_variable(coordinate),
                "value": value,
            }
            for coordinate, value in sorted(rational_specialization.items())
        ],
        "boundary_product_value": support_product_value,
        "conclusion": "P_G is not in the radical of the full mixed ideal",
    }
    return ledger


def main():
    ledger = audit()
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                "frozen radical-counterexample ledger digest changed")
    print(
        "n=8 localized radical counterexample: PASS; "
        f"nonzero={ledger['nonzero_coordinates']}, "
        f"mixed_checked={ledger['mixed_coefficients_checked']}, "
        f"pure=(0,0,1), P_G={ledger['boundary_product_value']}"
    )
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
