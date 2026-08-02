#!/usr/bin/env python3
"""Exact multidegree/type check for the first h=3 reset syzygy.

This is a deliberately small universal calculation.  It treats the eight-site
EqSystem coefficients at the mixed word 01211222 and the pure word 00000000
as universal hafnian polynomials.  It checks the first possible fine
site-colour multidegree, the resulting two-row Koszul syzygy, and the five
quadratic obstructions to making the bare reset P_12112 a map on the universal
odd quotient R_5/(R_1 q^[2]).
"""

from collections import Counter
from fractions import Fraction as Q
from functools import lru_cache
from hashlib import sha256
import json


ZERO = Q(0)
ONE = Q(1)
SITES = tuple(range(8))
ODD = (1, 2, 3, 4, 5)
PURE = (0,) * 8
MIXED = (0, 1, 2, 1, 1, 2, 2, 2)
ODD_TAG = MIXED[1:6]
EXPECTED_DIGEST = "84daa7132cdec9ee4d2c81c2bd6c2dacb995e4b9dc1404190d489ad0ba72b55b"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


@lru_cache(maxsize=None)
def matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position, second in enumerate(vertices[1:], start=1):
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in matchings(rest):
            answer.append(((first, second),) + tail)
    return tuple(answer)


def edge_variable(left, right, left_colour, right_colour):
    if left < right:
        return ("w", left, right, left_colour, right_colour)
    return ("w", right, left, right_colour, left_colour)


def monomial(*variables):
    return tuple(sorted(variables))


def poly_add(*polynomials):
    result = {}
    for polynomial in polynomials:
        for term, coefficient in polynomial.items():
            result[term] = result.get(term, ZERO) + coefficient
            if result[term] == ZERO:
                del result[term]
    return result


def poly_scale(scalar, polynomial):
    return {
        term: scalar * coefficient
        for term, coefficient in polynomial.items()
        if scalar * coefficient
    }


def poly_multiply(left, right):
    result = {}
    for left_term, left_coefficient in left.items():
        for right_term, right_coefficient in right.items():
            term = tuple(sorted(left_term + right_term))
            result[term] = (
                result.get(term, ZERO) + left_coefficient * right_coefficient
            )
            if result[term] == ZERO:
                del result[term]
    return result


def hafnian_polynomial(vertices, colouring):
    result = {}
    for matching in matchings(tuple(vertices)):
        term = monomial(*(
            edge_variable(left, right, colouring[left], colouring[right])
            for left, right in matching
        ))
        result[term] = result.get(term, ZERO) + ONE
    return result


def row_degree(colouring):
    return Counter((site, colour) for site, colour in enumerate(colouring))


def degree_sum(left, right):
    result = Counter(left)
    result.update(right)
    return result


def degree_lcm(left, right):
    return Counter({key: max(left[key], right[key]) for key in left.keys() | right.keys()})


def degree_subtract(left, right):
    result = Counter(left)
    result.subtract(right)
    require(all(value >= 0 for value in result.values()), "negative multidegree")
    return +result


def degree_size(degree):
    return sum(degree.values())


def internal_hafnian_after_deleting(site):
    remaining = tuple(vertex for vertex in ODD if vertex != site)
    colouring = {vertex: ODD_TAG[ODD.index(vertex)] for vertex in ODD}
    return hafnian_polynomial(remaining, colouring)


def specialize_to_guard_support(polynomial):
    # At the 12112 word, the direct-free guard has only the internal odd
    # edges 12 and 14.  Every four-site perfect matching therefore vanishes.
    supported = {(1, 2), (1, 4)}
    result = {}
    for term, coefficient in polynomial.items():
        if all((variable[1], variable[2]) in supported for variable in term):
            result[term] = coefficient
    return result


def main():
    pure_degree = row_degree(PURE)
    mixed_degree = row_degree(MIXED)
    least_common = degree_lcm(pure_degree, mixed_degree)
    common_slots = sum(
        min(pure_degree[key], mixed_degree[key])
        for key in pure_degree.keys() | mixed_degree.keys()
    )
    require(common_slots == 1, "the two words no longer agree at exactly one site")
    require(degree_size(least_common) == 15, "fine lcm slot count changed")
    require(
        degree_size(degree_subtract(least_common, pure_degree)) == 7
        and degree_size(degree_subtract(least_common, mixed_degree)) == 7,
        "fine lcm deficits changed",
    )

    # Polynomial coefficients are products of edges, hence have even slot
    # degree.  Seven slots are impossible; the first possible coefficient has
    # eight slots, i.e. edge degree four.  The natural homogenized degree is
    # the sum of the two row degrees.
    first_degree = degree_sum(pure_degree, mixed_degree)
    pure_coefficient_degree = degree_subtract(first_degree, pure_degree)
    mixed_coefficient_degree = degree_subtract(first_degree, mixed_degree)
    require(
        degree_size(pure_coefficient_degree)
        == degree_size(mixed_coefficient_degree)
        == 8,
        "first coefficient slot degree changed",
    )

    h_pure = hafnian_polynomial(SITES, PURE)
    h_mixed = hafnian_polynomial(SITES, MIXED)
    require(len(h_pure) == len(h_mixed) == 105, "eight-site hafnian size changed")
    pure_variables = {variable for term in h_pure for variable in term}
    mixed_variables = {variable for term in h_mixed for variable in term}
    require(
        pure_variables.isdisjoint(mixed_variables),
        "pure and mixed hafnians unexpectedly share an edge variable",
    )

    # Homogenize H_0-1 as H_0-u, where u has fine degree mu(00000000)
    # and matching degree four.  The two-row Koszul cell is
    #
    #   H_m r_0 - (H_0-u) r_m.
    #
    # Its coefficient on r_m is u-H_0, so after u=1 its lowest target term
    # is +r_m.  The boundary below is checked as a literal sparse polynomial.
    u = {monomial(("u",)): ONE}
    f_pure = poly_add(h_pure, poly_scale(-ONE, u))
    f_mixed = h_mixed
    coefficient_r_pure = f_mixed
    coefficient_r_mixed = poly_scale(-ONE, f_pure)
    boundary = poly_add(
        poly_multiply(coefficient_r_pure, f_pure),
        poly_multiply(coefficient_r_mixed, f_mixed),
    )
    require(boundary == {}, "the universal two-row Koszul boundary is nonzero")
    require(coefficient_r_mixed.get(monomial(("u",))) == ONE, "leading symbol changed")

    # The reset epsilon_12112 descends through R_1 q^[2] only if each of the
    # following five universal quadratic hafnians vanishes.  None does.
    denominator_defects = {}
    for site in ODD:
        defect = internal_hafnian_after_deleting(site)
        require(len(defect) == 3, f"site {site}: four-site hafnian changed")
        require(all(coefficient == ONE for coefficient in defect.values()), "bad defect coefficient")
        require(defect, f"site {site}: universal reset defect vanished")
        require(
            specialize_to_guard_support(defect) == {},
            f"site {site}: direct-free guard no longer kills the reset defect",
        )
        denominator_defects[str(site)] = [
            [list(variable) for variable in term]
            for term in sorted(defect)
        ]

    ledger = {
        "mixed_word": "01211222",
        "pure_word": "00000000",
        "common_slots": common_slots,
        "lcm_slots": degree_size(least_common),
        "first_coefficient_edge_degree": degree_size(pure_coefficient_degree) // 2,
        "hafnian_terms": [len(h_pure), len(h_mixed)],
        "koszul_boundary_terms": len(boundary),
        "koszul_mixed_leading_target_coefficient": "1",
        "universal_denominator_defects": denominator_defects,
        "guard_specialized_defect_terms": [
            len(specialize_to_guard_support(internal_hafnian_after_deleting(site)))
            for site in ODD
        ],
    }
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode()).hexdigest()
    require(digest == EXPECTED_DIGEST, f"ledger digest changed: {digest}")
    print("h=3 direct-free first-syzygy multidegree gate: PASS")
    print("edge coefficient degrees 0,1,2,3 excluded; first possible degree: 4")
    print("degree-4 two-row Koszul lift: exact, leading symbol +r_(22,012112)")
    print("universal bare-reset denominator defects: 5 nonzero quadrics")
    print("the sparse direct-free guard specializes all 5 defects to zero")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
