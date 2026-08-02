#!/usr/bin/env python3
"""Exact vertex split for the two branch-only weighted d6 cells.

The weighted degree-six census has two exceptional representatives whose
normal forms contain no P6+P2 or P4+P4 term.  Both have a leading coordinate
x=(02:00), encoded by byte 09, with multiplicity two.  This checker rebuilds
only those two source-labelled S-pairs:

* H_1 against the degree-five transport (730,2188);
* the transports (730,1459) and (730,3646).

It then audits the geometric split at x.  On x=0 each normal form is an
explicit combination of restricted members of the complete d4/d5 basis and
reduces exactly to zero.  On x!=0 no power of x creates a lower-basis leading
divisor; localization instead replaces the repeated pivot by the squarefree
Laurent pivot obtained after division by x^2.

No degree-six pair census is performed here.  The only large construction is
the already-certified 6,558/84,005 lower lead dictionary.
"""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CENSUS = load(
    "n8_chart26_branch_weighted",
    "verify_n8_chart26_weighted_degree6_census.py",
)
FIRST = CENSUS.FIRST
COMPLETE = CENSUS.COMPLETE
WEIGHT = CENSUS.WEIGHT
D5 = CENSUS.D5
QQ = Fraction

EXPECTED_LEDGER_SHA256 = (
    "d0413a91abb8a74f46ed1b6235eadcd9426aa6b24f08a212ecd2c1097a0ba566"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def add_value(polynomial, monomial, coefficient):
    value = polynomial.get(monomial, QQ(0)) + coefficient
    if value:
        polynomial[monomial] = value
    else:
        polynomial.pop(monomial, None)


def add_scaled(target, source, scalar=QQ(1), multiplier=b""):
    for monomial, coefficient in source.items():
        add_value(
            target,
            FIRST.multiply(multiplier, monomial),
            scalar * coefficient,
        )


def order_key(monomial):
    return -len(monomial), -WEIGHT.weight(monomial), monomial


def weighted_lead(polynomial):
    return min(polynomial, key=order_key)


def restrict(polynomial, variable):
    return {
        monomial: coefficient
        for monomial, coefficient in polynomial.items()
        if variable not in monomial
    }


def remove_copies(monomial, variable, count):
    result = list(monomial)
    for _index in range(count):
        require(variable in result, "localized pivot lost an x factor")
        result.remove(variable)
    return bytes(result)


def scalar_multiple(first, second):
    if not first or set(first) != set(second):
        return None
    pivot = next(iter(first))
    scalar = first[pivot] / second[pivot]
    return scalar if all(
        first[row] == scalar * second[row] for row in first
    ) else None


def histogram_record(values):
    return [
        [[value.numerator, value.denominator], count]
        for value, count in sorted(Counter(values).items())
    ]


def audit():
    originals, degree4, code_to_lead, degree5, _words = CENSUS.build_leads()
    require(len(degree4) == 6558 and len(degree5) == 84005,
            "the complete weighted lower basis changed")
    require(all(len(lead) == len(set(lead)) == 4 for lead in degree4),
            "a degree-four lower lead stopped being squarefree")
    require(all(len(lead) == len(set(lead)) == 5 for lead in degree5),
            "a degree-five lower lead stopped being squarefree")

    lead_by_code = {code: lead for lead, code in degree4.items()}
    lead_by_pair = {
        tuple(source[:2]): lead for lead, source in degree5.items()
    }
    cache = {}

    def basis_polynomial(kind, lead):
        key = kind, lead
        if key in cache:
            return cache[key]
        if kind == "4":
            polynomial = {
                row: QQ(value)
                for row, value in originals[degree4[lead]].items()
            }
        else:
            first, second, _distance = degree5[lead]
            lcm = bytes(sorted(
                set(code_to_lead[first]) | set(code_to_lead[second])
            ))
            polynomial = {
                row: QQ(value)
                for row, value in COMPLETE.s_polynomial(
                    lcm, first, second, originals, code_to_lead
                ).items()
            }
        pivot = polynomial[lead]
        polynomial = {
            row: value / pivot for row, value in polynomial.items()
        }
        cache[key] = polynomial
        return polynomial

    def source_spoly(first_kind, first, second_kind, second):
        lcm = CENSUS.monomial_lcm(first, second)
        answer = {}
        for kind, lead, sign in (
                (first_kind, first, QQ(1)),
                (second_kind, second, QQ(-1))):
            multiplier = FIRST.quotient(lcm, lead)
            add_scaled(
                answer,
                basis_polynomial(kind, lead),
                sign,
                multiplier,
            )
        return answer

    def reduce_full(polynomial):
        work = dict(polynomial)
        remainder = {}
        certificate = []
        while work:
            row = min(work, key=order_key)
            coefficient = work.pop(row)
            choice = None
            if len(row) >= 5:
                for divisor in FIRST.divisors(row, 5):
                    if divisor in degree5:
                        choice = "5", divisor
                        break
            if choice is None and len(row) >= 4:
                for divisor in FIRST.divisors(row, 4):
                    if divisor in degree4:
                        choice = "4", divisor
                        break
            if choice is None:
                remainder[row] = coefficient
                continue
            kind, lead = choice
            reducer = basis_polynomial(kind, lead)
            multiplier = FIRST.quotient(row, lead)
            factor = coefficient / reducer[lead]
            certificate.append((kind, lead, multiplier, factor))
            for term, value in reducer.items():
                output = FIRST.multiply(multiplier, term)
                if output != row:
                    add_value(work, output, -factor * value)
            require(len(certificate) <= 10000,
                    "a bounded exceptional reduction exceeded its guard")
        return remainder, certificate

    def reduce_restricted(polynomial, reducers):
        normalized = {}
        lead_map = {}
        for label, source in reducers:
            restricted = restrict(source, x)
            require(restricted, "a restricted branch reducer vanished")
            lead = weighted_lead(restricted)
            pivot = restricted[lead]
            normalized[label] = {
                row: value / pivot for row, value in restricted.items()
            }
            require(lead not in lead_map,
                    "two selected restricted branch leads collided")
            lead_map[lead] = label

        work = dict(polynomial)
        remainder = {}
        certificate = []
        while work:
            row = min(work, key=order_key)
            coefficient = work.pop(row)
            choice = None
            for degree in (5, 4):
                if len(row) < degree:
                    continue
                for divisor in FIRST.divisors(row, degree):
                    if divisor in lead_map:
                        choice = divisor, lead_map[divisor]
                        break
                if choice is not None:
                    break
            if choice is None:
                remainder[row] = coefficient
                continue
            lead, label = choice
            reducer = normalized[label]
            multiplier = FIRST.quotient(row, lead)
            factor = coefficient / reducer[lead]
            certificate.append((label, lead, multiplier, factor))
            for term, value in reducer.items():
                output = FIRST.multiply(multiplier, term)
                if output != row:
                    require(order_key(output) > order_key(row),
                            "a restricted branch reduction increased")
                    add_value(work, output, -factor * value)
        return remainder, certificate

    def has_lower_divisor(monomial):
        if len(monomial) >= 5 and any(
                divisor in degree5 for divisor in FIRST.divisors(monomial, 5)):
            return True
        return len(monomial) >= 4 and any(
            divisor in degree4 for divisor in FIRST.divisors(monomial, 4)
        )

    x = D5.COORDINATE_ID[(0, 2, 0, 0)]
    require(x == 0x09 and D5.COORDINATES[x] == (0, 2, 0, 0),
            "the branch coordinate changed")

    specifications = (
        {
            "name": "degree4_degree5",
            "class_size": 8412,
            "first_kind": "4",
            "first_source": 1,
            "second_kind": "5",
            "second_source": (730, 2188),
            "expected_source_terms": 255,
            "expected_remainder_terms": 330,
            "expected_lead": "0309094bc6f4",
            "expected_base_certificate": (
                ("4", "0175c6f4", "0c", 1),
            ),
            "closed_reducers": (
                ("H_1", "4", 1),
                ("H_730", "4", 730),
            ),
            "expected_closed_terms": 150,
            "expected_closed_histogram": {3: 2, 4: 19, 5: 73, 6: 56},
            "expected_closed_lead": "010c123fc6f4",
            "expected_closed_certificate": (
                ("H_1", "123fc6f4", "010c", 1),
                ("H_730", "0175c6f4", "0c", -1),
            ),
            "laurent_pivot": "034bc6f4",
        },
        {
            "name": "degree5_degree5",
            "class_size": 45776,
            "first_kind": "5",
            "first_source": (730, 1459),
            "second_kind": "5",
            "second_source": (730, 3646),
            "expected_source_terms": 330,
            "expected_remainder_terms": 480,
            "expected_lead": "0409094ec6f4",
            "expected_base_certificate": (
                ("5", "020c4bc6f4", "09", -1),
            ),
            "closed_reducers": (
                ("R_730_1459", "5", (730, 1459)),
            ),
            "expected_closed_terms": 150,
            "expected_closed_histogram": {4: 4, 5: 34, 6: 112},
            "expected_closed_lead": "010c2d7375c6",
            "expected_closed_certificate": (
                ("R_730_1459", "012d7375c6", "0c", 1),
            ),
            "laurent_pivot": "044ec6f4",
        },
    )

    records = []
    for specification in specifications:
        def source_lead(kind, source):
            return (lead_by_code[source] if kind == "4"
                    else lead_by_pair[source])

        first_lead = source_lead(
            specification["first_kind"], specification["first_source"]
        )
        second_lead = source_lead(
            specification["second_kind"], specification["second_source"]
        )
        source = source_spoly(
            specification["first_kind"], first_lead,
            specification["second_kind"], second_lead,
        )
        require(len(source) == specification["expected_source_terms"],
                "an exceptional source S-polynomial changed")
        remainder, certificate = reduce_full(source)
        require(len(remainder) == specification["expected_remainder_terms"],
                "an exceptional weighted remainder changed")
        lead = weighted_lead(remainder)
        require(lead.hex() == specification["expected_lead"],
                "an exceptional repeated lead changed")
        require(Counter(lead)[x] == 2,
                "an exceptional lead lost its double branch coordinate")
        frozen_certificate = tuple(
            (kind, reducer.hex(), multiplier.hex(), int(factor))
            for kind, reducer, multiplier, factor in certificate
        )
        require(frozen_certificate
                == specification["expected_base_certificate"],
                "an exceptional lower-basis certificate changed")

        closed = restrict(remainder, x)
        require(len(closed) == specification["expected_closed_terms"],
                "an exceptional closed support changed")
        require(dict(sorted(Counter(map(len, closed)).items()))
                == specification["expected_closed_histogram"],
                "an exceptional closed degree histogram changed")
        require(Counter(closed.values())
                == Counter({QQ(-1): 75, QQ(1): 75}),
                "an exceptional closed coefficient histogram changed")
        require(weighted_lead(closed).hex()
                == specification["expected_closed_lead"],
                "an exceptional closed lead changed")

        selected_reducers = []
        for label, kind, source_label in specification["closed_reducers"]:
            lower_lead = source_lead(kind, source_label)
            selected_reducers.append(
                (label, basis_polynomial(kind, lower_lead))
            )
        closed_remainder, closed_certificate = reduce_restricted(
            closed, selected_reducers
        )
        require(not closed_remainder,
                "a closed exceptional cell did not reduce to zero")
        frozen_closed_certificate = tuple(
            (label, reducer.hex(), multiplier.hex(), int(factor))
            for label, reducer, multiplier, factor in closed_certificate
        )
        require(frozen_closed_certificate
                == specification["expected_closed_certificate"],
                "a closed source-labelled certificate changed")

        # Since every lower lead is squarefree, multiplying by x^k for k>=1
        # never changes the set of possible lower divisors after k=1.  Thus
        # this one finite divisibility test proves lower normality for every
        # positive colon power.
        x_product = {
            FIRST.multiply(bytes((x,)), monomial): coefficient
            for monomial, coefficient in remainder.items()
        }
        require(not any(has_lower_divisor(row) for row in x_product),
                "x times an exceptional remainder gained a lower divisor")

        laurent_pivot = remove_copies(lead, x, 2)
        require(laurent_pivot.hex() == specification["laurent_pivot"],
                "an exceptional Laurent pivot changed")
        require(len(laurent_pivot) == len(set(laurent_pivot)) == 4,
                "an exceptional Laurent pivot is not squarefree")
        exponent_histogram = Counter(
            monomial.count(x) - 2 for monomial in remainder
        )
        laurent_record = [
            [
                monomial.count(x) - 2,
                bytes(value for value in monomial if value != x).hex(),
                coefficient.numerator,
                coefficient.denominator,
            ]
            for monomial, coefficient in sorted(remainder.items())
        ]

        degree6_skeletons = Counter(
            CENSUS.skeleton_type(row)
            for row in remainder if len(row) == 6
        )
        closed_degree6_skeletons = Counter(
            CENSUS.skeleton_type(row)
            for row in closed if len(row) == 6
        )
        for skeletons in (degree6_skeletons, closed_degree6_skeletons):
            require(not skeletons.get("P6+P2")
                    and not skeletons.get("P4+P4"),
                    "a branch-only cell entered the simple forest complex")

        records.append({
            "name": specification["name"],
            "class_size": specification["class_size"],
            "source_labels": [
                [specification["first_kind"],
                 specification["first_source"]],
                [specification["second_kind"],
                 specification["second_source"]],
            ],
            "source_leads": [first_lead.hex(), second_lead.hex()],
            "source_terms": len(source),
            "lower_reduction_certificate": [list(row)
                                              for row in frozen_certificate],
            "remainder_terms": len(remainder),
            "remainder_degree_histogram": dict(sorted(
                Counter(map(len, remainder)).items()
            )),
            "remainder_coefficient_histogram": histogram_record(
                remainder.values()
            ),
            "remainder_lead": lead.hex(),
            "remainder_x_exponent_histogram": dict(sorted(
                Counter(row.count(x) for row in remainder).items()
            )),
            "remainder_degree6_skeletons": dict(sorted(
                degree6_skeletons.items()
            )),
            "closed_terms": len(closed),
            "closed_degree_histogram": dict(sorted(
                Counter(map(len, closed)).items()
            )),
            "closed_lead_before_reduction": weighted_lead(closed).hex(),
            "closed_source_certificate": [list(row)
                                           for row in frozen_closed_certificate],
            "closed_remainder_terms": len(closed_remainder),
            "closed_degree6_skeletons": dict(sorted(
                closed_degree6_skeletons.items()
            )),
            "positive_x_powers_lower_reduced": True,
            "positive_x_power_argument": (
                "all lower leads are squarefree, so x^k has the same "
                "lower divisors as x for every k>=1"
            ),
            "laurent_divisor_power": 2,
            "laurent_pivot": laurent_pivot.hex(),
            "laurent_pivot_squarefree": True,
            "laurent_pivot_skeleton": CENSUS.skeleton_type(laurent_pivot),
            "laurent_x_exponent_histogram": dict(sorted(
                exponent_histogram.items()
            )),
            "laurent_support_sha256": sha256(json.dumps(
                laurent_record, separators=(",", ":")
            ).encode()).hexdigest(),
            "path_forest_terms": (
                degree6_skeletons.get("P6+P2", 0)
                + degree6_skeletons.get("P4+P4", 0)
            ),
        })

    ledger = {
        "split_coordinate_id": f"{x:02x}",
        "split_coordinate": list(D5.COORDINATES[x]),
        "complete_lower_basis": {"degree4": 6558, "degree5": 84005},
        "degree6_pairs_enumerated": 0,
        "records": records,
        "closed_branch_conclusion": (
            "both exceptional cells reduce exactly to zero using their "
            "restricted source-labelled lower cells"
        ),
        "open_branch_conclusion": (
            "no positive x power reduces through the lower basis; x^-2 "
            "instead exposes a squarefree Laurent pivot in each cell"
        ),
        "forest_conclusion": (
            "the closed cells die before path straightening and the open "
            "Laurent cells contain no degree-six P6+P2 or P4+P4 term"
        ),
        "scope_guard": (
            "this proves the split for two frozen representatives, not "
            "uniformity over their 8412 and 45776 coarse classes"
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
                "the frozen branch-elimination ledger changed")
    print(
        "n=8 chart26 d6 branch elimination: PASS; "
        "closed remainders=0/0, open Laurent pivots=034bc6f4/044ec6f4"
    )
    print(json.dumps(ledger, sort_keys=True))
    print("sha256:", digest)


if __name__ == "__main__":
    main()
