#!/usr/bin/env python3
"""Verify the first cross-word degree-six cell after the chart-26 d5 orbit.

This is a bounded, source-labelled Buchberger audit.  Start with all 6,558
homogenized normalized generators and the two nonzero reduced cells in the
support-stabilizer orbit of the code-(1,2) degree-five S-polynomial.  Order
their 22 degree-six critical pairs by LCM monomial.  The first two accepted
remainders have squarefree leading terms.  The third has a repeated source
coordinate, giving the first non-squarefree cell in this orbit extension.

The result is deliberately not called a minimal leading generator for the
full ideal: other original-original degree-five S-cells have not all been
adjoined.
"""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
FIRST_PATH = HERE / "verify_n8_chart26_first_homogeneous_spair.py"
SPEC = importlib.util.spec_from_file_location("n8_first_spair", FIRST_PATH)
FIRST = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(FIRST)
D5 = FIRST.D5
QQ = Fraction

EXPECTED_LEDGER_SHA256 = (
    "7199489115634c5d2bab33a6701c32b879bdbd14760ef3aad15b6ab102ea0a03"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def monomial_lcm(first, second):
    return bytes(sorted((Counter(first) | Counter(second)).elements()))


def divides(divisor, dividend):
    return Counter(divisor) <= Counter(dividend)


def s_polynomial(first, second):
    lcm = monomial_lcm(first["lead"], second["lead"])
    first_multiplier = FIRST.quotient(lcm, first["lead"])
    second_multiplier = FIRST.quotient(lcm, second["lead"])
    answer = {}
    for row, value in first["polynomial"].items():
        FIRST.add_value(answer, FIRST.multiply(first_multiplier, row), value)
    for row, value in second["polynomial"].items():
        FIRST.add_value(answer, FIRST.multiply(second_multiplier, row), -value)
    return lcm, answer


def reduce_polynomial(polynomial, basis):
    """Exact division in y-degree/lex order, which is t-last homogeneous."""
    lead_lookup = {item["lead"]: index for index, item in enumerate(basis)}
    require(len(lead_lookup) == len(basis), "basis leading terms collided")
    lead_degrees = tuple(sorted(set(map(len, lead_lookup)), reverse=True))
    work = {row: QQ(value) for row, value in polynomial.items() if value}
    remainder = {}
    certificate = Counter()
    while work:
        row = min(work, key=lambda item: (-len(item), item))
        coefficient = work.pop(row)
        choice = None
        for degree in lead_degrees:
            if degree > len(row):
                continue
            for divisor in FIRST.divisors(row, degree):
                index = lead_lookup.get(divisor)
                if index is not None:
                    choice = divisor, index
                    break
            if choice is not None:
                break
        if choice is None:
            remainder[row] = coefficient
            continue
        lead, index = choice
        reducer = basis[index]["polynomial"]
        multiplier = FIRST.quotient(row, lead)
        factor = coefficient / reducer[lead]
        certificate[(index, multiplier)] += factor
        for term, value in reducer.items():
            output = FIRST.multiply(multiplier, term)
            if output == row:
                continue
            require(
                len(output) < len(row)
                or (len(output) == len(row) and output > row),
                "homogeneous division is not decreasing",
            )
            FIRST.add_value(work, output, -factor * value)
    return remainder, {
        column: value for column, value in certificate.items() if value
    }


def normalize(polynomial):
    lead = FIRST.leading_monomial(polynomial)
    coefficient = polynomial[lead]
    normalized = {row: value / coefficient
                  for row, value in polynomial.items()}
    require(normalized[lead] == 1, "normalization lost its monic lead")
    return normalized, lead


def initial_basis():
    originals, original_leads = FIRST.original_basis()
    basis = []
    for code, polynomial in sorted(originals.items()):
        basis.append({
            "kind": "original",
            "label": code,
            "total_degree": 4,
            "polynomial": {row: QQ(value)
                           for row, value in polynomial.items()},
            "lead": FIRST.leading_monomial(polynomial),
        })
    _lead_a, _lead_b, _lcm, first_spoly = FIRST.s_polynomial(
        1, 2, originals, original_leads
    )
    for transform_index in range(len(D5.VARIABLE_TRANSFORMS)):
        transformed = FIRST.transform_polynomial(
            first_spoly, transform_index
        )
        transformed, _raw_lead = normalize(transformed)
        remainder, _certificate = FIRST.reduce_by_original(
            transformed, originals, original_leads
        )
        if remainder:
            remainder, lead = normalize(remainder)
            basis.append({
                "kind": "degree5_orbit",
                "label": transform_index,
                "total_degree": 5,
                "polynomial": remainder,
                "lead": lead,
            })
    require(len(basis) == 6560, "old-plus-degree5 basis census changed")
    require([item["lead"].hex() for item in basis[-2:]]
            == ["0948cfebf5", "0948d0eaf9"],
            "degree-five orbit leads changed")
    return basis


def degree6_schedule(basis):
    original_count = 6558
    pairs = []
    for new_index in range(original_count, len(basis)):
        for earlier_index in range(new_index):
            first = basis[earlier_index]
            second = basis[new_index]
            if not set(first["lead"]) & set(second["lead"]):
                continue
            lcm = monomial_lcm(first["lead"], second["lead"])
            if len(lcm) == 6:
                pairs.append((lcm, earlier_index, new_index))
    pairs.sort(key=lambda item: (item[0], item[1], item[2]))
    require(len(pairs) == 22, "degree-six critical-pair census changed")
    return pairs


def fraction_histogram(values):
    return [
        [[value.numerator, value.denominator], count]
        for value, count in sorted(Counter(values).items())
    ]


def polynomial_digest(polynomial):
    record = [
        [row.hex(), value.numerator, value.denominator]
        for row, value in sorted(polynomial.items())
    ]
    return sha256(json.dumps(record, separators=(",", ":")).encode()).hexdigest()


def common_monomial(polynomial):
    counters = iter(Counter(row) for row in polynomial)
    answer = next(counters)
    for counter in counters:
        answer &= counter
    return bytes(sorted(answer.elements()))


def audit():
    basis = initial_basis()
    schedule = degree6_schedule(basis)
    accepted_records = []
    for schedule_index, (lcm, first_index, second_index) in enumerate(
            schedule[:3], 1):
        first = basis[first_index]
        second = basis[second_index]
        recomputed_lcm, spoly = s_polynomial(first, second)
        require(recomputed_lcm == lcm, "scheduled LCM changed")
        remainder, certificate = reduce_polynomial(spoly, basis)
        require(remainder, "an accepted degree-six remainder vanished")
        remainder, lead = normalize(remainder)
        require(not any(divides(item["lead"], lead) for item in basis),
                "accepted leading term was already reducible")
        reducer_kinds = Counter(
            basis[index]["kind"] for index, _multiplier in certificate
        )
        record = {
            "schedule_index": schedule_index,
            "first": [first["kind"], first["label"]],
            "second": [second["kind"], second["label"]],
            "lcm": lcm.hex(),
            "lcm_degree": len(lcm),
            "s_polynomial_terms": len(spoly),
            "reduction_columns": len(certificate),
            "reducer_kind_histogram": dict(sorted(reducer_kinds.items())),
            "remainder_terms": len(remainder),
            "remainder_degree_histogram": dict(sorted(
                Counter(map(len, remainder)).items()
            )),
            "remainder_coefficient_histogram": fraction_histogram(
                remainder.values()
            ),
            "remainder_sha256": polynomial_digest(remainder),
            "lead": lead.hex(),
            "lead_squarefree": len(lead) == len(set(lead)),
            "lead_t_exponent": len(lcm) - len(lead),
            "common_monomial": common_monomial(remainder).hex(),
        }
        accepted_records.append(record)
        basis.append({
            "kind": "degree6",
            "label": schedule_index,
            "total_degree": 6,
            "polynomial": remainder,
            "lead": lead,
        })

    require([record["lead"] for record in accepted_records] == [
        "0951abcfebf5", "0951abd0eaf9", "0948cfcfebef"
    ], "first three ordered degree-six leads changed")
    require([record["lead_squarefree"] for record in accepted_records]
            == [True, True, False],
            "first non-squarefree position changed")
    require([record["remainder_terms"] for record in accepted_records]
            == [504, 504, 546], "degree-six remainder sizes changed")
    third_lead = bytes.fromhex(accepted_records[2]["lead"])
    repeated = [value for value, count in Counter(third_lead).items()
                if count > 1]
    require(repeated == [0xcf], "repeated source coordinate changed")
    require(D5.COORDINATES[0xcf] == (4, 6, 0, 0),
            "repeated coordinate decoding changed")
    require(accepted_records[2]["first"] == ["original", 11],
            "first cross-word source generator changed")
    require(accepted_records[2]["second"] == ["degree5_orbit", 0],
            "first cross-word transport cell changed")
    require(D5.decode_word(11) == (0, 0, 0, 0, 0, 1, 0, 2),
            "cross-word code 11 changed")

    ledger = {
        "homogeneous_term_order": "total degree, then y degree, then lex; t last",
        "starting_original_generators": 6558,
        "starting_nonzero_degree5_orbit_cells": 2,
        "degree6_pair_schedule_size": len(schedule),
        "accepted_prefix": accepted_records,
        "first_nonsquarefree_schedule_index": 3,
        "first_nonsquarefree_lead": third_lead.hex(),
        "repeated_coordinate_id": "cf",
        "repeated_coordinate": list(D5.COORDINATES[0xcf]),
        "cross_word_code": 11,
        "cross_word": list(D5.decode_word(11)),
        "conclusion": (
            "the first orbit-extended cross-word compatibility cell has "
            "a repeated source coordinate in its leading monomial"
        ),
        "scope_guard": (
            "this is not a globally minimal initial-ideal generator until "
            "all other original-original degree5 cells are adjoined"
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
                "frozen degree-six compatibility ledger changed")
    print(
        "n=8 chart26 first degree-six compatibility: PASS; "
        "schedule=22, accepted prefix=3, first repeated coordinate=cf"
    )
    print(json.dumps(ledger, sort_keys=True))
    print("sha256:", digest)


if __name__ == "__main__":
    main()
