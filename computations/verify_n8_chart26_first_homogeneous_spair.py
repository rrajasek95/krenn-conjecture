#!/usr/bin/env python3
"""Verify the first new homogeneous Buchberger cell in chart 26.

The twelve support variables are replaced by one homogenizing variable t.
A homogeneous monomial of total degree D is encoded only by its sorted
off-support variables; its t exponent is D minus the encoded length.

For the normalized mixed generators with word codes 1 and 2, the leading
degree-four monomials overlap in three variables.  Their degree-five
S-polynomial is already reduced by all 6,558 original generators.  Its
support-stabilizer orbit has four source identities: two reduce to zero and
two give new squarefree, t-free leading monomials of degree five.
"""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
BASE_PATH = HERE / "verify_n8_normalized_critical_contraction.py"
SPEC = importlib.util.spec_from_file_location("n8_normalized", BASE_PATH)
BASE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BASE)
D5 = BASE.D5
QQ = Fraction

EXPECTED_LEDGER_SHA256 = (
    "70e42a64b34641ad71a25b6e226bfbe60dc500a7e866d3970fb89049bdf1d28f"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def add_value(polynomial, monomial, value):
    result = polynomial.get(monomial, QQ(0)) + value
    if result:
        polynomial[monomial] = result
    else:
        polynomial.pop(monomial, None)


def multiply(left, right):
    return bytes(sorted(left + right))


def quotient(dividend, divisor):
    answer = list(dividend)
    for value in divisor:
        if value not in answer:
            return None
        answer.remove(value)
    return bytes(answer)


def normalized_generator(code):
    return dict(BASE.normalized_generator(code))


def leading_monomial(polynomial):
    maximum_degree = max(map(len, polynomial))
    return min(row for row in polynomial if len(row) == maximum_degree)


def divisors(monomial, degree):
    from itertools import combinations

    seen = set()
    for positions in combinations(range(len(monomial)), degree):
        divisor = bytes(monomial[position] for position in positions)
        if divisor not in seen:
            seen.add(divisor)
            yield divisor


def original_basis():
    polynomials = {}
    lead_to_code = {}
    for code in range(3 ** 8):
        if len(set(D5.decode_word(code))) == 1:
            continue
        polynomial = normalized_generator(code)
        lead = leading_monomial(polynomial)
        require(len(lead) == 4, "an original leading term lost degree four")
        require(lead not in lead_to_code, "original leading terms collided")
        polynomials[code] = polynomial
        lead_to_code[lead] = code
    require(len(polynomials) == 6558, "mixed-generator census changed")
    return polynomials, lead_to_code


def reduce_by_original(polynomial, polynomials, lead_to_code):
    """Exact homogeneous division with t last, encoded by y monomials."""
    work = {row: QQ(value) for row, value in polynomial.items() if value}
    remainder = {}
    certificate = Counter()
    while work:
        row = min(work, key=lambda item: (-len(item), item))
        coefficient = work.pop(row)
        choice = None
        if len(row) >= 4:
            for divisor in divisors(row, 4):
                code = lead_to_code.get(divisor)
                if code is not None:
                    choice = divisor, code
                    break
        if choice is None:
            remainder[row] = coefficient
            continue
        lead, code = choice
        multiplier = quotient(row, lead)
        generator = polynomials[code]
        factor = coefficient / generator[lead]
        certificate[(code, multiplier)] += factor
        for term, value in generator.items():
            output = multiply(multiplier, term)
            if output == row:
                continue
            require(
                len(output) < len(row)
                or (len(output) == len(row) and output > row),
                "original division is not decreasing",
            )
            add_value(work, output, -factor * value)
    return remainder, {
        column: value for column, value in certificate.items() if value
    }


def s_polynomial(code_a, code_b, polynomials, lead_to_code):
    first = polynomials[code_a]
    second = polynomials[code_b]
    lead_a = leading_monomial(first)
    lead_b = leading_monomial(second)
    lcm = bytes(sorted(set(lead_a) | set(lead_b)))
    require(len(lcm) == len(lead_a) + len(lead_b)
            - len(set(lead_a) & set(lead_b)), "LCM encoding changed")
    multiplier_a = quotient(lcm, lead_a)
    multiplier_b = quotient(lcm, lead_b)
    answer = {}
    for row, value in first.items():
        add_value(answer, multiply(multiplier_a, row), QQ(value))
    for row, value in second.items():
        add_value(answer, multiply(multiplier_b, row), -QQ(value))
    return lead_a, lead_b, lcm, answer


def transform_polynomial(polynomial, index):
    transform = D5.VARIABLE_TRANSFORMS[index]
    answer = {}
    for row, value in polynomial.items():
        transformed = bytes(sorted(transform[item] for item in row))
        add_value(answer, transformed, value)
    return answer


def encode_histogram(counter):
    return [[key, value] for key, value in sorted(counter.items())]


def audit():
    polynomials, lead_to_code = original_basis()
    lead_a, lead_b, lcm, spoly = s_polynomial(
        1, 2, polynomials, lead_to_code
    )
    require(D5.decode_word(1) == (0, 0, 0, 0, 0, 0, 0, 1),
            "word code 1 changed")
    require(D5.decode_word(2) == (0, 0, 0, 0, 0, 0, 0, 2),
            "word code 2 changed")
    require(lead_a.hex() == "0948c6f4" and lead_b.hex() == "0948c6f5",
            "first overlapping leading pair changed")
    require(len(lcm) == 5, "first S-pair LCM degree changed")

    remainder, certificate = reduce_by_original(
        spoly, polynomials, lead_to_code
    )
    require(remainder == spoly and not certificate,
            "first S-polynomial is no longer already reduced")
    require(len(remainder) == 180, "first remainder support changed")
    degree_histogram = Counter(map(len, remainder))
    coefficient_histogram = Counter(remainder.values())
    require(degree_histogram == Counter({5: 120, 4: 48, 3: 12}),
            "first remainder degree histogram changed")
    require(coefficient_histogram == Counter({QQ(-1): 90, QQ(1): 90}),
            "first remainder coefficients changed")
    new_lead = leading_monomial(remainder)
    require(new_lead.hex() == "0948cfebf5", "first new leading term changed")
    require(len(new_lead) == len(set(new_lead)) == len(lcm) == 5,
            "first new leading term is not squarefree and t-free")

    orbit_records = []
    distinct_sources = set()
    nonzero_leads = []
    for index in range(len(D5.VARIABLE_TRANSFORMS)):
        transformed = transform_polynomial(spoly, index)
        distinct_sources.add(tuple(sorted(transformed.items())))
        transformed_lead = leading_monomial(transformed)
        lead_coefficient = transformed[transformed_lead]
        transformed = {
            row: value / lead_coefficient
            for row, value in transformed.items()
        }
        reduced, reduction = reduce_by_original(
            transformed, polynomials, lead_to_code
        )
        reduced_lead = leading_monomial(reduced) if reduced else None
        if reduced_lead is not None:
            require(len(reduced_lead) == len(set(reduced_lead)) == 5,
                    "a nonzero orbit remainder lost squarefreeness")
            nonzero_leads.append(reduced_lead.hex())
        orbit_records.append({
            "transform": index,
            "source_lead": transformed_lead.hex(),
            "reduction_columns": len(reduction),
            "remainder_terms": len(reduced),
            "remainder_lead": (
                reduced_lead.hex() if reduced_lead is not None else None
            ),
        })
    require(len(distinct_sources) == 4, "source S-cell orbit size changed")
    require(nonzero_leads == ["0948cfebf5", "0948d0eaf9"],
            "reduced orbit leading terms changed")
    require([record["remainder_terms"] for record in orbit_records]
            == [180, 0, 180, 0], "orbit reduction pattern changed")
    require([record["reduction_columns"] for record in orbit_records]
            == [0, 2, 0, 2], "orbit reduction column census changed")

    pair_orbit = set()
    for index in range(len(D5.WORD_TRANSFORMS)):
        pair_orbit.add(tuple(sorted((
            D5.WORD_TRANSFORMS[index][1],
            D5.WORD_TRANSFORMS[index][2],
        ))))
    require(pair_orbit == {(1, 2), (3, 6), (27, 54), (81, 162)},
            "source word-pair orbit changed")

    remainder_record = [
        [row.hex(), value.numerator, value.denominator]
        for row, value in sorted(remainder.items())
    ]
    ledger = {
        "normalized_variables": 240,
        "homogenizing_variables": 1,
        "mixed_generators": len(polynomials),
        "distinct_degree4_original_leads": len(lead_to_code),
        "word_codes": [1, 2],
        "word_pair_orbit": [list(pair) for pair in sorted(pair_orbit)],
        "word_pair_orbit_size": len(pair_orbit),
        "lead_a": lead_a.hex(),
        "lead_b": lead_b.hex(),
        "lcm_degree": len(lcm),
        "s_polynomial_terms": len(spoly),
        "remainder_degree_histogram": encode_histogram(degree_histogram),
        "remainder_coefficient_histogram": [
            [[value.numerator, value.denominator], count]
            for value, count in sorted(coefficient_histogram.items())
        ],
        "remainder_sha256": sha256(json.dumps(
            remainder_record, separators=(",", ":")
        ).encode()).hexdigest(),
        "new_lead": new_lead.hex(),
        "new_lead_degree": len(new_lead),
        "new_lead_t_exponent": len(lcm) - len(new_lead),
        "new_lead_squarefree": len(new_lead) == len(set(new_lead)),
        "source_cell_orbit_size": len(distinct_sources),
        "reduced_orbit": orbit_records,
        "distinct_nonzero_orbit_leads": nonzero_leads,
        "conclusion": (
            "the original homogenized generators are not a Groebner basis; "
            "their first orbit cell adds two squarefree t-free degree5 leads"
        ),
        "scope_guard": (
            "squarefreeness of this first extension does not certify that "
            "the completed initial ideal is squarefree"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    return ledger, digest


def main():
    ledger, digest = audit()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                "frozen first homogeneous S-cell ledger changed")
    print(
        "n=8 chart26 first homogeneous S-cell: PASS; "
        "pair=(1,2), remainder=180, orbit=4, nonzero orbit leads=2"
    )
    print(json.dumps(ledger, sort_keys=True))
    print("sha256:", digest)


if __name__ == "__main__":
    main()
