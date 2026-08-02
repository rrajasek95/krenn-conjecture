#!/usr/bin/env python3
"""Factor the C4 exchange cells and test the two path-bearing d6 classes.

The un-divided matching-row identities in
``verify_n8_chart26_c4_exchange_3cell.py`` have large monomial factors.  This
checker removes their exact common factors in the full aggregate ring,
passes to the normalized chart-26 homogeneous encoding, and reduces the
result against the complete 6,558 degree-four plus 84,005 degree-five
weighted basis.

Only the two path-bearing nonsquarefree representatives are tested:

* H_1 versus the transport (1,10), class size 42,754;
* H_1 versus the transport (1,37), class size 38,702.

The calculation is deliberately bounded.  It proves that the C4 three-cell
is coherent but does not yet kill either primitive degree-six normal form.
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


WDC = load(
    "n8_c4_primitive_weighted",
    "verify_n8_chart26_weighted_degree6_census.py",
)
C4 = load(
    "n8_c4_primitive_exchange",
    "verify_n8_chart26_c4_exchange_3cell.py",
)
FIRST = WDC.FIRST
COMPLETE = WDC.COMPLETE
WEIGHT = WDC.WEIGHT
D5 = WDC.D5
QQ = Fraction

EXPECTED_LEDGER_SHA256 = (
    "a5c14aff114eb4dc43e4b10e223d6bcb4571d06fffa8f31190d1821b53f8de36"
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


def multiply_full(polynomial, multiplier, scalar=1):
    answer = {}
    for monomial, coefficient in polynomial.items():
        add_value(
            answer,
            bytes(sorted(monomial + multiplier)),
            scalar * coefficient,
        )
    return answer


def normalize_quotient(polynomial, divisor):
    """Divide in the full ring, then encode support variables as t powers."""
    answer = {}
    for monomial, coefficient in polynomial.items():
        quotient = C4.quotient(monomial, divisor)
        encoded = bytes(
            variable for variable in quotient if D5.IS_OFF_SUPPORT[variable]
        )
        add_value(answer, encoded, QQ(coefficient))
    return answer


def scalar_multiple(first, second):
    if not first or not second or set(first) != set(second):
        return None
    pivot = next(iter(first))
    scalar = first[pivot] / second[pivot]
    return scalar if all(
        first[row] == scalar * second[row] for row in first
    ) else None


def audit():
    originals, degree4, code_to_lead, degree5, _words = WDC.build_leads()
    require(len(degree4) == 6558 and len(degree5) == 84005,
            "complete lower weighted basis changed")
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
        coefficient = polynomial[lead]
        polynomial = {
            row: value / coefficient for row, value in polynomial.items()
        }
        cache[key] = polynomial
        return polynomial

    def order_key(row):
        return -len(row), -WEIGHT.weight(row), row

    def reduce_polynomial(polynomial):
        work = dict(polynomial)
        remainder = {}
        steps = 0
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
            for term, value in reducer.items():
                output = FIRST.multiply(multiplier, term)
                if output != row:
                    add_value(work, output, -factor * value)
            steps += 1
            require(steps <= 200000,
                    "primitive C4 reduction exceeded its guard")
        return remainder, steps

    def source_spoly(first_kind, first, second_kind, second):
        lcm = WDC.monomial_lcm(first, second)
        first_multiplier = FIRST.quotient(lcm, first)
        second_multiplier = FIRST.quotient(lcm, second)
        answer = {}
        for row, value in basis_polynomial(first_kind, first).items():
            add_value(
                answer, FIRST.multiply(first_multiplier, row), value
            )
        for row, value in basis_polynomial(second_kind, second).items():
            add_value(
                answer, FIRST.multiply(second_multiplier, row), -value
            )
        return answer

    bad_records = (
        {
            "pair": (1, 10),
            "degree5_lead": bytes.fromhex("0948c6d9e4"),
            "expected_terms": 504,
            "expected_lead": "0951acc6f4f4",
            "class_size": 42754,
            "c4_variables": ("c6", "c7", "d9", "e4", "e7", "f4"),
        },
        {
            "pair": (1, 37),
            "degree5_lead": bytes.fromhex("0948c6dce4"),
            "expected_terms": 552,
            "expected_lead": "0952acc6f4f4",
            "class_size": 38702,
            "c4_variables": ("c6", "ca", "d9", "dc", "e4", "e7", "f4"),
        },
    )
    original_lead = bytes.fromhex("0948c6f4")
    bad_remainders = {}
    colon_records = []
    for record in bad_records:
        source = source_spoly(
            "4", original_lead, "5", record["degree5_lead"]
        )
        remainder, steps = reduce_polynomial(source)
        lead = min(remainder, key=order_key)
        require(len(remainder) == record["expected_terms"]
                and lead.hex() == record["expected_lead"]
                and steps == 3,
                "a path-bearing bad representative changed")
        bad_remainders[record["pair"]] = remainder

        variable_results = []
        for encoded in record["c4_variables"]:
            multiplier = bytes.fromhex(encoded)
            product = {
                FIRST.multiply(multiplier, row): value
                for row, value in remainder.items()
            }
            reduced, product_steps = reduce_polynomial(product)
            require(reduced == product and product_steps == 0,
                    "a C4 coordinate stopped being a colon obstruction")
            variable_results.append({
                "variable": encoded,
                "remainder_terms": len(reduced),
                "remainder_lead": min(reduced, key=order_key).hex(),
                "reduction_steps": product_steps,
            })
        colon_records.append({
            "source_pair": list(record["pair"]),
            "class_size": record["class_size"],
            "degree6_remainder_terms": len(remainder),
            "degree6_remainder_lead": lead.hex(),
            "c4_coordinate_products": variable_results,
        })

    def exchange_components(pair, endpoint):
        a = {
            code: C4.matching_monomial(C4.M, code) for code in pair
        }
        b = {
            code: C4.matching_monomial(C4.N, code) for code in pair
        }
        h = {code: C4.hafnian(code) for code in pair}
        p_m = C4.pair_minor(a, h, *pair)
        p_n = C4.pair_minor(b, h, *pair)
        delta = C4.scalar_minor(a, b, *pair)
        first = multiply_full(p_m, b[endpoint])
        second = multiply_full(p_n, a[endpoint], -1)
        third = {}
        for monomial, coefficient in delta.items():
            piece = multiply_full(h[endpoint], monomial, -coefficient)
            for output, value in piece.items():
                add_value(third, output, value)
        identity = {}
        for component in (first, second, third):
            for output, value in component.items():
                add_value(identity, output, value)
        require(not identity, "an un-divided E2 identity changed")
        common = C4.common_monomial((first, second, third))
        primitive = tuple(
            normalize_quotient(component, common)
            for component in (first, second, third)
        )
        identity = {}
        for component in primitive:
            for output, value in component.items():
                add_value(identity, output, value)
        require(not identity, "a primitive normalized E2 identity changed")
        return common, primitive

    e2_records = []
    for record in bad_records:
        pair = record["pair"]
        g = bad_remainders[pair]
        for endpoint in pair:
            common, primitive = exchange_components(pair, endpoint)
            reductions = [reduce_polynomial(part) for part in primitive]
            reduced_sum = {}
            for reduced, _steps in reductions:
                for row, value in reduced.items():
                    add_value(reduced_sum, row, value)
            require(not reduced_sum,
                    "separately reduced E2 components stopped cancelling")
            component_records = []
            for reduced, steps in reductions:
                component_records.append({
                    "terms": len(reduced),
                    "lead": (
                        min(reduced, key=order_key).hex() if reduced else None
                    ),
                    "steps": steps,
                })

            if pair == (1, 10):
                require(len(common) == 6
                        and common.hex() == "09094848d9f4",
                        "the degree-six E2 factor changed")
                require(all(not reduced for reduced, _steps in reductions),
                        "the degree-six E2 face left the lower source span")
            elif endpoint == 1:
                require(len(common) == 5
                        and common.hex() == "09094848f4",
                        "the first degree-seven E2 factor changed")
                require([len(reduced) for reduced, _steps in reductions]
                        == [330, 552, 714],
                        "the first degree-seven E2 normal forms changed")
                c6_g = {
                    FIRST.multiply(bytes.fromhex("c6"), row): value
                    for row, value in g.items()
                }
                require(scalar_multiple(reductions[1][0], c6_g) == 1,
                        "E2 stopped carrying c6 times the bad remainder")
            else:
                require(len(common) == 5
                        and common.hex() == "09094848f4",
                        "the second degree-seven E2 factor changed")
                require([len(reduced) for reduced, _steps in reductions]
                        == [0, 552, 552],
                        "the second degree-seven E2 normal forms changed")
                ca_g = {
                    FIRST.multiply(bytes.fromhex("ca"), row): value
                    for row, value in g.items()
                }
                require(scalar_multiple(reductions[1][0], ca_g) == 1
                        and scalar_multiple(reductions[2][0], ca_g) == -1,
                        "E2 stopped carrying the +/-ca colon pair")

            e2_records.append({
                "source_pair": list(pair),
                "endpoint": endpoint,
                "full_common_factor": common.hex(),
                "full_common_factor_degree": len(common),
                "primitive_total_degree": 12 - len(common),
                "primitive_component_terms": [
                    len(component) for component in primitive
                ],
                "component_normal_forms": component_records,
            })

    # The four E3 determinants have one uniform factor: the square of the
    # common matching core (02:00)(13:00).  Their primitive degree is eight,
    # so no E3 leading term can divide either homogeneous degree-six bad
    # remainder.  The E4 tetrahedron survives division by this common factor.
    states = C4.STATES
    a = {code: C4.matching_monomial(C4.M, code) for code in states}
    b = {code: C4.matching_monomial(C4.N, code) for code in states}
    h = {code: C4.hafnian(code) for code in states}
    primitive_c = {}
    e3_records = []
    for omitted in range(4):
        triple = tuple(
            state for index, state in enumerate(states) if index != omitted
        )
        determinant = C4.triple_minor(a, b, h, *triple)
        common = C4.common_monomial((determinant,))
        require(common.hex() == "09094848" and len(common) == 4,
                "the E3 common core changed")
        primitive = normalize_quotient(determinant, common)
        require(len(primitive) == 498,
                "the primitive normalized E3 support changed")
        primitive_c[omitted] = primitive
        e3_records.append({
            "states": list(triple),
            "full_common_factor": common.hex(),
            "primitive_total_degree": 8,
            "primitive_terms": len(primitive),
        })

    for row_name, row in (("M", a), ("N", b)):
        tetrahedron = {}
        for omitted, state in enumerate(states):
            normalized_multiplier = bytes(
                variable for variable in row[state]
                if D5.IS_OFF_SUPPORT[variable]
            )
            for monomial, coefficient in primitive_c[omitted].items():
                add_value(
                    tetrahedron,
                    FIRST.multiply(normalized_multiplier, monomial),
                    (1 if omitted % 2 == 0 else -1) * coefficient,
                )
        require(not tetrahedron,
                f"the primitive normalized {row_name} tetrahedron failed")

    ledger = {
        "lower_degree4_leads": len(degree4),
        "lower_degree5_leads": len(degree5),
        "bad_representatives": colon_records,
        "primitive_E2": e2_records,
        "primitive_E3": e3_records,
        "primitive_E4_tetrahedra": 2,
        "conclusion": (
            "the C4 exchange is primitively coherent but does not reduce "
            "either path-bearing degree6 curvature representative"
        ),
        "colon_obstruction": (
            "every decorated C4 coordinate times either degree6 remainder "
            "is already irreducible by the complete degree4/degree5 basis"
        ),
        "scope_guard": (
            "this tests two frozen representatives, not every member of "
            "their coarse classes or later Buchberger layers"
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
                "frozen primitive C4 colon ledger changed")
    print(
        "n=8 chart26 primitive C4 colon: PASS; "
        "bad classes=42754/38702, no primitive reduction"
    )
    print(json.dumps(ledger, sort_keys=True))
    print("sha256:", digest)


if __name__ == "__main__":
    main()
