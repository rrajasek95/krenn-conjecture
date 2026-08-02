#!/usr/bin/env python3
"""Exact first contraction of the n=8 exponent-one dual after localization.

Set the twelve boundary-support variables to one.  The 100 rows in the exact
balanced dual descend to 100 distinct normalized monomials, but the dual no
longer annihilates the normalized mixed ideal.  This checker exhausts all
normalized columns incident to those monomials and verifies a six-column
half-integral relation whose critical projection is exactly the constant 1.

The resulting 564-orbit positive-degree tail is a seed for a well-founded
Morse/Groebner contraction.  The finite projection alone is not a proof of
localized ideal membership because the normalized ideal is inhomogeneous.
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
DUAL_PATH = HERE / "verify_n8_full_source_degree6_exact_dual.py"
SPEC = importlib.util.spec_from_file_location("n8_exact_dual", DUAL_PATH)
DUAL = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(DUAL)
D5 = DUAL.D5
QQ = Fraction
EXPECTED_LEDGER_SHA256 = (
    "b4aba17d10448e97c7915841282a81fe0cc7e2b56f70cc189ac13f5e87ca906d"
)

# Coefficient, word code, and normalized off-support multiplier.
CONTRACTION = (
    (QQ(-1, 2), 5, bytes.fromhex("0f5d")),
    (QQ(-1, 2), 2919, bytes.fromhex("4f80e1")),
    (QQ(-1, 2), 3002, bytes.fromhex("0f4be2")),
    (QQ(-1, 2), 3064, bytes.fromhex("05ae")),
    (QQ(1, 2), 3780, b""),
    (QQ(-1, 2), 3780, bytes.fromhex("0fec")),
)


def canonical_monomial(monomial):
    return min(
        bytes(sorted(transform[value] for value in monomial))
        for transform in D5.VARIABLE_TRANSFORMS
    )


def column_orbit(column):
    code, multiplier = column
    return tuple(sorted(set(
        (
            D5.WORD_TRANSFORMS[index][code],
            bytes(sorted(D5.VARIABLE_TRANSFORMS[index][value]
                         for value in multiplier)),
        )
        for index in range(len(D5.GROUP))
    )))


def canonical_column(column):
    return column_orbit(column)[0]


def normalized_generator(code):
    return Counter(
        bytes(value for value in term if D5.IS_OFF_SUPPORT[value])
        for term in D5.iter_word_terms(code)
    )


def invariant_column_image(column, polynomials):
    answer = Counter()
    for code, multiplier in column_orbit(column):
        for term, coefficient in polynomials[code].items():
            row = bytes(sorted(multiplier + term))
            if row == canonical_monomial(row):
                answer[row] += coefficient
    return answer


def multiset_divisors(monomial, maximum_degree=4):
    groups = tuple(Counter(monomial).items())
    answer = []

    def visit(position, partial):
        if position == len(groups):
            answer.append(bytes(partial))
            return
        value, multiplicity = groups[position]
        for count in range(min(multiplicity,
                               maximum_degree - len(partial)) + 1):
            visit(position + 1, partial + [value] * count)

    visit(0, [])
    return answer


def quotient(monomial, divisor):
    answer = list(monomial)
    for value in divisor:
        answer.remove(value)
    return bytes(answer)


def critical_target(pure, critical_rows):
    """Compute the pure-product coefficients only on the critical support."""
    first, second, third = pure
    third_lookup = dict(third)
    answer = {}
    for target in critical_rows:
        coefficient = 0
        for left, left_coefficient in first.items():
            if not Counter(left) <= Counter(target):
                continue
            remainder = quotient(target, left)
            for middle, middle_coefficient in second.items():
                if not Counter(middle) <= Counter(remainder):
                    continue
                last = quotient(remainder, middle)
                coefficient += (
                    left_coefficient * middle_coefficient
                    * third_lookup.get(last, 0)
                )
        if coefficient:
            answer[target] = coefficient
    return answer


def audit():
    certificate = json.loads(DUAL.CERTIFICATE_PATH.read_bytes())
    descended = {}
    for encoded, numerator, denominator in (
            certificate["lower_rows"] + certificate["degree6_rows"]):
        balanced = bytes.fromhex(encoded)
        monomial = canonical_monomial(bytes(
            value for value in balanced if D5.IS_OFF_SUPPORT[value]
        ))
        require(monomial not in descended,
                "balanced dual rows collide after normalization")
        descended[monomial] = QQ(numerator, denominator)
    require(len(descended) == 100, "normalized critical support changed")
    degree_histogram = Counter(map(len, descended))
    require(degree_histogram
            == Counter({0: 1, 2: 1, 3: 4, 4: 27, 5: 47, 6: 20}),
            "normalized critical degree histogram changed")

    polynomials = {}
    term_index = defaultdict(dict)
    constant_mixed_words = 0
    for code in range(3 ** 8):
        if len(set(D5.decode_word(code))) == 1:
            continue
        polynomial = normalized_generator(code)
        polynomials[code] = polynomial
        if polynomial.get(b""):
            constant_mixed_words += 1
        for term, coefficient in polynomial.items():
            term_index[term][code] = coefficient
    require(len(polynomials) == 6558, "normalized mixed-word census changed")
    require(len(term_index) == 688059,
            "normalized mixed-term key census changed")
    require(constant_mixed_words == 2,
            "constant-term normalized generator census changed")

    incident_columns = set()
    for row in descended:
        for term in multiset_divisors(row):
            for code in term_index.get(term, {}):
                incident_columns.add(canonical_column(
                    (code, quotient(row, term))
                ))
    require(len(incident_columns) == 1091,
            "normalized critical incident-column census changed")

    restricted_support_histogram = Counter()
    violating_columns = 0
    for column in incident_columns:
        image = invariant_column_image(column, polynomials)
        restricted = {
            row: coefficient for row, coefficient in image.items()
            if row in descended and coefficient
        }
        restricted_support_histogram[len(restricted)] += 1
        pairing = sum(
            descended[row] * coefficient
            for row, coefficient in restricted.items()
        )
        if pairing:
            violating_columns += 1
    require(restricted_support_histogram
            == Counter({1: 889, 2: 177, 3: 8, 4: 12, 5: 2, 6: 3}),
            "normalized restricted-column support histogram changed")
    require(violating_columns == 903,
            "old exact dual violation census changed after normalization")

    contraction_image = defaultdict(QQ)
    actual_image = defaultdict(QQ)
    for scalar, code, multiplier in CONTRACTION:
        column = (code, multiplier)
        require(column == canonical_column(column),
                "contraction column is not canonical")
        for row, coefficient in invariant_column_image(
                column, polynomials).items():
            contraction_image[row] += scalar * coefficient
        for actual_code, actual_multiplier in column_orbit(column):
            for term, coefficient in polynomials[actual_code].items():
                row = bytes(sorted(actual_multiplier + term))
                actual_image[row] += scalar * coefficient
    contraction_image = {
        row: value for row, value in contraction_image.items() if value
    }
    actual_image = {row: value for row, value in actual_image.items() if value}
    critical_projection = {
        row: value for row, value in contraction_image.items()
        if row in descended
    }
    require(critical_projection == {b"": QQ(1)},
            "six-column contraction no longer kills the critical support")
    require(actual_image.get(b"") == 1,
            "six-column contraction lost its constant term")

    invariant_tail = dict(contraction_image)
    actual_tail = dict(actual_image)
    require(invariant_tail.pop(b"") == 1 and actual_tail.pop(b"") == 1,
            "contraction tail retained the wrong constant")
    invariant_tail = {row: value for row, value in invariant_tail.items()
                      if value}
    actual_tail = {row: value for row, value in actual_tail.items() if value}
    require(len(invariant_tail) == 564 and len(actual_tail) == 2240,
            "contraction tail census changed")
    invariant_tail_degrees = Counter(map(len, invariant_tail))
    actual_tail_degrees = Counter(map(len, actual_tail))
    require(invariant_tail_degrees
            == Counter({2: 6, 3: 16, 4: 48, 5: 104, 6: 254, 7: 136}),
            "invariant contraction tail degrees changed")
    require(actual_tail_degrees
            == Counter({2: 20, 3: 56, 4: 188, 5: 416,
                        6: 1016, 7: 544}),
            "actual contraction tail degrees changed")

    pure = tuple(
        normalized_generator(D5.word_code((colour,) * 8))
        for colour in range(3)
    )
    target_on_critical = critical_target(pure, set(descended))
    require(target_on_critical == {b"": 1},
            "normalized pure target acquired another critical monomial")
    target_pairing = sum(
        descended[row] * coefficient
        for row, coefficient in target_on_critical.items()
    )
    require(target_pairing == -1,
            "old dual target pairing changed after normalization")

    ledger = {
        "vertices": 8,
        "endpoint_colours": 3,
        "support_variables_set_to_one": 12,
        "normalized_variables": 240,
        "descended_critical_monomials": len(descended),
        "critical_degree_histogram": dict(sorted(degree_histogram.items())),
        "distinct_mixed_words": len(polynomials),
        "distinct_normalized_term_keys": len(term_index),
        "constant_term_mixed_generators": constant_mixed_words,
        "critical_incident_column_orbits": len(incident_columns),
        "old_dual_violating_columns": violating_columns,
        "restricted_column_support_histogram": dict(
            sorted(restricted_support_histogram.items())
        ),
        "normalized_target_pairing_with_old_dual": [-1, 1],
        "contraction_column_orbits": len(CONTRACTION),
        "contraction_coefficient_set": [
            [value.numerator, value.denominator]
            for value in sorted(set(item[0] for item in CONTRACTION))
        ],
        "invariant_positive_degree_tail": len(invariant_tail),
        "actual_positive_degree_tail": len(actual_tail),
        "invariant_tail_degree_histogram": dict(
            sorted(invariant_tail_degrees.items())
        ),
        "actual_tail_degree_histogram": dict(
            sorted(actual_tail_degrees.items())
        ),
        "conclusion": "the exact balanced dual does not descend to the normalized chart",
        "scope_guard": "the finite contraction seed is not yet a localized membership certificate",
    }
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    return ledger, sha256(encoded.encode()).hexdigest()


def main():
    ledger, digest = audit()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                "frozen normalized critical-contraction ledger changed")
    print(
        "n=8 normalized critical contraction: PASS; "
        f"columns={ledger['critical_incident_column_orbits']}, "
        f"violations={ledger['old_dual_violating_columns']}, "
        f"tail={ledger['invariant_positive_degree_tail']}"
    )
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
