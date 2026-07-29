#!/usr/bin/env python3
"""Exact quotient analysis of the first Laurent-compatible path-edge support.

This is reconnaissance, not a frozen theorem checker.  It reduces the
remaining target and cubic weight equations modulo all forced zero-q2
binomials of the 48-cell support.
"""

from __future__ import annotations

from collections import Counter, defaultdict

from search_mixed_endpoint_one_site_support import (
    PM6,
    ROW_GEOMETRIES,
    SupportSystem,
    active_square_terms,
    cell_variable,
    forced_zero_two_term_target,
    zero_binomial_exponent_rows,
)
from search_parallel_binomial_nonzero_constants_cegar import (
    quotient_key,
    signed_quotient_lattice,
)


ACTIVE = (
    6, 9, 13, 15, 16, 18, 31, 32, 34, 35, 40, 41, 42, 43, 44, 45,
    52, 54, 61, 62, 70, 71, 82, 83, 88, 89, 100, 101, 102, 106,
    107, 108, 109, 110, 112, 113, 118, 119, 120, 121, 122, 123,
    127, 128, 129, 130, 131, 132,
)


def exponent(term, location):
    output = [0] * len(location)
    for variable in term:
        output[location[variable]] += 1
    return output


def exponent_difference(left, right, location):
    output = exponent(left, location)
    for variable in right:
        output[location[variable]] -= 1
    return output


def reduce_terms(terms, location, lattice):
    classes = defaultdict(lambda: [0, 0])
    for term in terms:
        signed = quotient_key(tuple(exponent(term, location)) + (0,), lattice)
        assert signed[-1] in (0, 1)
        classes[signed[:-1]][signed[-1]] += 1
    remainder = {}
    for key, (positive, negative) in classes.items():
        coefficient = positive - negative
        if coefficient:
            remainder[key] = coefficient
    return remainder


def cube_terms(word, active):
    output = []
    for matching in PM6:
        term = tuple(
            cell_variable(u, v, word[u], word[v])
            for u, v in matching
        )
        if set(term) <= active:
            output.append(term)
    return tuple(output)


def main():
    active = set(ACTIVE)
    location = {variable: index for index, variable in enumerate(ACTIVE)}
    system = SupportSystem(ROW_GEOMETRIES["path-edge"])

    zero_binomials = []
    target_terms = []
    for pair, word, target, _indicators in system.square_records:
        terms = active_square_terms(system, active, pair, word)
        if not terms:
            continue
        assert len(terms) == 2
        if target:
            target_terms.append((pair, word, terms))
        else:
            zero_binomials.append((pair, word, terms))

    rows = [
        exponent_difference(terms[0], terms[1], location)
        for _pair, _word, terms in zero_binomials
    ]
    consistent, lattice = signed_quotient_lattice(rows, len(ACTIVE))
    assert consistent
    primary, exact_rows, exact_records = zero_binomial_exponent_rows(
        system, active
    )
    assert tuple(tuple(row) for row in rows) == exact_rows
    target_certificate = forced_zero_two_term_target(
        system, active, primary, exact_rows
    )
    assert target_certificate is not None

    cube_fibres = []
    for word, _indicators in system.cube_records:
        terms = cube_terms(word, active)
        if terms:
            assert len(terms) == 8
            cube_fibres.append((word, terms))

    target_remainders = [
        (pair, word, reduce_terms(terms, location, lattice))
        for pair, word, terms in target_terms
    ]
    cube_remainders = [
        (word, reduce_terms(terms, location, lattice))
        for word, terms in cube_fibres
    ]

    print(
        "active", len(ACTIVE),
        "zero_q2_binomials", len(zero_binomials),
        "target_binomials", len(target_terms),
        "q3_eight_term_fibres", len(cube_fibres),
    )
    print(
        "quotient_hnf_rows", len(lattice[0]),
        "quotient_pivots", lattice[1],
    )
    target_record, target_coefficients, target_epsilon = target_certificate
    print(
        "first_target_zero_certificate",
        target_record[:2],
        "support", sum(value != 0 for value in target_coefficients),
        "coefficient_sum", sum(target_coefficients),
        "epsilon", target_epsilon,
    )
    print(
        "target_reduced_term_histogram",
        Counter(len(remainder) for _pair, _word, remainder in target_remainders),
    )
    print(
        "cube_reduced_term_histogram",
        Counter(len(remainder) for _word, remainder in cube_remainders),
    )
    print(
        "cube_reduced_coefficient_histogram",
        Counter(
            tuple(sorted(remainder.values()))
            for _word, remainder in cube_remainders
        ),
    )

    monomial_obstructions = [
        (word, remainder)
        for word, remainder in cube_remainders
        if len(remainder) == 1
    ]
    print("q3_monomial_obstructions", len(monomial_obstructions))
    for word, remainder in monomial_obstructions[:10]:
        print(" ", word, next(iter(remainder.values())))


if __name__ == "__main__":
    main()
