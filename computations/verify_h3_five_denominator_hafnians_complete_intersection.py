#!/usr/bin/env python3
"""Certify that the five universal denominator hafnians are a CI.

The checker is dependency-free.  It computes a Groebner basis over Q with
degree-reverse-lexicographic order, verifies Buchberger's criterion, and
computes the height of the initial monomial ideal by exhaustive vertex
covers.  Since the polynomial ring is Cohen--Macaulay and the ideal has
five generators and height five, the generators form a regular sequence.
"""

from fractions import Fraction
from itertools import combinations
import hashlib
import json


VARS = ("x12", "x13", "x14", "x15", "x23",
        "x24", "x25", "x34", "x35", "x45")
N = len(VARS)
ZERO_MON = (0,) * N


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def monomial(*names):
    exponents = [0] * N
    for name in names:
        exponents[VARS.index(name)] += 1
    return tuple(exponents)


def poly(*terms):
    result = {}
    for coefficient, names in terms:
        exponent = monomial(*names)
        result[exponent] = result.get(exponent, Fraction(0)) + Fraction(coefficient)
    return {term: coefficient for term, coefficient in result.items() if coefficient}


def add(left, right, scale=Fraction(1)):
    result = dict(left)
    for term, coefficient in right.items():
        result[term] = result.get(term, Fraction(0)) + scale * coefficient
        if not result[term]:
            del result[term]
    return result


def mul_monomial(value, exponent, scale=Fraction(1)):
    return {
        tuple(a + b for a, b in zip(term, exponent, strict=True)): scale * coefficient
        for term, coefficient in value.items()
        if scale * coefficient
    }


def order_key(exponent):
    # Degree reverse lexicographic order with VARS[0] > ... > VARS[-1].
    return (sum(exponent),) + tuple(-value for value in reversed(exponent))


def leading(value):
    exponent = max(value, key=order_key)
    return exponent, value[exponent]


def divides(left, right):
    return all(a <= b for a, b in zip(left, right, strict=True))


def quotient_monomial(numerator, denominator):
    require(divides(denominator, numerator), "nondivisible monomial quotient")
    return tuple(a - b for a, b in zip(numerator, denominator, strict=True))


def normal_form(value, basis):
    remainder = {}
    work = dict(value)
    while work:
        lead_mon, lead_coefficient = leading(work)
        for divisor in basis:
            divisor_mon, divisor_coefficient = leading(divisor)
            if divides(divisor_mon, lead_mon):
                factor = quotient_monomial(lead_mon, divisor_mon)
                work = add(
                    work,
                    mul_monomial(divisor, factor,
                                 -lead_coefficient / divisor_coefficient),
                )
                break
        else:
            remainder[lead_mon] = lead_coefficient
            del work[lead_mon]
    return remainder


def monic(value):
    _, coefficient = leading(value)
    return {term: entry / coefficient for term, entry in value.items()}


def s_polynomial(left, right):
    left_mon, left_coefficient = leading(left)
    right_mon, right_coefficient = leading(right)
    common = tuple(max(a, b) for a, b in zip(left_mon, right_mon, strict=True))
    first = mul_monomial(
        left, quotient_monomial(common, left_mon), Fraction(1, 1) / left_coefficient
    )
    second = mul_monomial(
        right, quotient_monomial(common, right_mon), Fraction(1, 1) / right_coefficient
    )
    return add(first, second, Fraction(-1))


def buchberger(generators):
    basis = [monic(value) for value in generators]
    pairs = [(left, right) for right in range(len(basis)) for left in range(right)]
    cursor = 0
    while cursor < len(pairs):
        left, right = pairs[cursor]
        cursor += 1
        reduced = normal_form(s_polynomial(basis[left], basis[right]), basis)
        if reduced:
            new_index = len(basis)
            basis.append(monic(reduced))
            pairs.extend((old_index, new_index) for old_index in range(new_index))
    return basis


def minimal_vertex_cover_size(leading_monomials):
    supports = [
        {index for index, exponent in enumerate(term) if exponent}
        for term in leading_monomials
    ]
    for size in range(N + 1):
        for choice in combinations(range(N), size):
            chosen = set(choice)
            if all(chosen & support for support in supports):
                return size, tuple(VARS[index] for index in choice)
    raise AssertionError("monomial ideal has no vertex cover")


def main():
    # h_v is the hafnian of the four sites complementary to v in K_5.
    generators = [
        poly((1, ("x23", "x45")), (1, ("x24", "x35")), (1, ("x25", "x34"))),
        poly((1, ("x13", "x45")), (1, ("x14", "x35")), (1, ("x15", "x34"))),
        poly((1, ("x12", "x45")), (1, ("x14", "x25")), (1, ("x15", "x24"))),
        poly((1, ("x12", "x35")), (1, ("x13", "x25")), (1, ("x15", "x23"))),
        poly((1, ("x12", "x34")), (1, ("x13", "x24")), (1, ("x14", "x23"))),
    ]
    basis = buchberger(generators)
    require(all(not normal_form(s_polynomial(left, right), basis)
                for left, right in combinations(basis, 2)),
            "Buchberger criterion failed")

    leading_monomials = [leading(value)[0] for value in basis]
    height, cover = minimal_vertex_cover_size(leading_monomials)
    require(height == 5, "the initial ideal stopped having height five")
    require(len(generators) == height,
            "generator count and certified height no longer agree")

    # In a polynomial ring, an ideal generated by height-many elements is a
    # complete intersection.  Its minimal resolution is therefore Koszul.
    betti = [1, 5, 10, 10, 5, 1]
    ledger = {
        "variables": list(VARS),
        "generator_count": len(generators),
        "groebner_basis_size": len(basis),
        "initial_ideal_height": height,
        "one_minimum_vertex_cover": list(cover),
        "complete_intersection": True,
        "koszul_betti_numbers": betti,
        "no_non_koszul_first_syzygy": True,
        "proof_consequence": (
            "a denominator-only correction of the five h_v faces cannot "
            "supply a unit aggregate; a successful cap lift must use extra "
            "endpoint/full-source data or specialization-created Tor"
        ),
    }
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":")).encode()
    digest = hashlib.sha256(encoded).hexdigest()
    print(json.dumps(ledger, indent=2, sort_keys=True))
    print(f"ledger_sha256={digest}")
    print("five denominator hafnians form a height-five complete intersection: PASS")


if __name__ == "__main__":
    main()
