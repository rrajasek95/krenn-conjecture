#!/usr/bin/env python3
"""Finite exact audit of the signed quotient constant-product reduction.

For small full-rank Laurent systems the entire complex solution set consists
of roots of unity of an explicitly bounded order.  This checker compares the
HNF signed-group reduction used by the n=8 search with exhaustive evaluation
at every such point, using cyclotomic-polynomial reduction to decide whether
a sum of roots of unity is zero.  It also tests rank-deficient systems, where
the constructive reconstructor must specialize a positive-dimensional torus
by its injective mixed-radix substitution.
"""

from __future__ import annotations

from collections import defaultdict
from itertools import product
import random

from sympy import Poly, Symbol, cyclotomic_poly
from sympy.polys.domains import ZZ
from sympy.polys.matrices import DomainMatrix

import search_parallel_binomial_nonzero_constants_cegar as toric
from reconstruct_n8_toric_witness import exact_toric_specialization


X = Symbol("X")


def determinant(rows):
    return int(DomainMatrix.from_list(rows, ZZ).det())


def reduced_product_nonzero(rows, polynomials):
    columns = len(rows[0])
    consistent, lattice = toric.signed_quotient_lattice(rows, columns)
    assert consistent
    classes = defaultdict(int)
    for monomials in product(*polynomials):
        exponent = tuple(
            sum(monomial[column] for monomial in monomials)
            for column in range(columns)
        )
        signed_class = toric.quotient_key(exponent + (0,), lattice)
        classes[signed_class[:-1]] += -1 if signed_class[-1] else 1
    return any(classes.values())


def root_sum_is_zero(order, exponents, cache):
    key = order, tuple(sorted(exponent % order for exponent in exponents))
    answer = cache.get(key)
    if answer is not None:
        return answer
    coefficients = defaultdict(int)
    for exponent in key[1]:
        coefficients[exponent] += 1
    polynomial = Poly.from_dict(
        {(exponent,): coefficient for exponent, coefficient in coefficients.items()},
        (X,),
        domain=ZZ,
    )
    cyclotomic = Poly(cyclotomic_poly(order, X), X, domain=ZZ)
    answer = polynomial.rem(cyclotomic).is_zero
    cache[key] = answer
    return answer


def exhaustive_product_nonzero(rows, polynomials, order, cache):
    columns = len(rows[0])
    assert order % 2 == 0
    for phases in product(range(order), repeat=columns):
        if any(
            sum(coefficient * phase
                for coefficient, phase in zip(row, phases)) % order
            != order // 2
            for row in rows
        ):
            continue
        if all(
            not root_sum_is_zero(
                order,
                [
                    sum(exponent * phase
                        for exponent, phase in zip(monomial, phases))
                    for monomial in polynomial
                ],
                cache,
            )
            for polynomial in polynomials
        ):
            return True
    return False


def specialized_sum_is_zero(order, base, terms):
    """Independently evaluate a ``sum zeta**r * base**p`` exactly."""

    minimum = min(power for _root, power in terms)
    coefficients = defaultdict(int)
    for root, power in terms:
        coefficients[root % order] += base ** (power - minimum)
    polynomial = Poly.from_dict(
        {
            (root,): coefficient
            for root, coefficient in coefficients.items()
            if coefficient
        },
        (X,),
        domain=ZZ,
    )
    cyclotomic = Poly(cyclotomic_poly(order, X), X, domain=ZZ)
    return polynomial.rem(cyclotomic).is_zero


def main():
    rng = random.Random(0x51A6ED)
    cache = {}

    # Force the torsion-component loop to skip its first branch: for
    # x^3=-1, 1+x^2+x^4 vanishes at x=zeta_6 but not at x=-1.
    branch_result = exact_toric_specialization(
        [[3]],
        [[(0,), (2,), (4,)], [(0,)], [(0,)]],
    )
    assert branch_result[0] == 6
    assert branch_result[2] == (3,)
    assert all(
        not specialized_sum_is_zero(
            branch_result[0], branch_result[1], terms
        )
        for terms in branch_result[4]
    )

    # Force the integer-specialization loop to reject base two.  With x=-1
    # and y free, y+x+x specializes to zero at y=2 but not at y=3.
    retry_result = exact_toric_specialization(
        [[1, 0]],
        [
            [(0, 1), (1, 0), (1, 0)],
            [(0, 0)],
            [(0, 0)],
        ],
    )
    assert retry_result[1] == 3
    assert all(
        not specialized_sum_is_zero(
            retry_result[0], retry_result[1], terms
        )
        for terms in retry_result[4]
    )

    checked = 0
    reconstructed = 0
    attempts = 0
    while checked < 1000:
        attempts += 1
        columns = rng.choice((1, 2))
        rows = [
            [rng.randrange(-2, 3) for _ in range(columns)]
            for _ in range(columns)
        ]
        det = abs(determinant(rows))
        if det == 0:
            continue
        consistent, _lattice = toric.signed_quotient_lattice(rows, columns)
        if not consistent:
            continue
        polynomials = [
            [
                tuple(rng.randrange(-2, 3) for _ in range(columns))
                for _ in range(rng.randrange(1, 5))
            ]
            for _ in range(3)
        ]
        # For a square full-rank D, every solution phase has denominator
        # dividing 2*|det(D)| by Cramer's rule, and all solutions occur on
        # this grid.
        order = 2 * det
        reduced = reduced_product_nonzero(rows, polynomials)
        exhaustive = exhaustive_product_nonzero(
            rows, polynomials, order, cache
        )
        assert reduced == exhaustive, (
            rows, polynomials, order, reduced, exhaustive
        )
        try:
            exact_toric_specialization(rows, polynomials)
            has_specialization = True
        except AssertionError:
            has_specialization = False
        assert has_specialization == reduced
        reconstructed += has_specialization
        checked += 1

    free_checked = 0
    free_reconstructed = 0
    while free_checked < 500:
        columns = rng.choice((2, 3, 4))
        number_rows = rng.randrange(1, columns)
        rows = [
            [rng.randrange(-2, 3) for _ in range(columns)]
            for _ in range(number_rows)
        ]
        consistent, _lattice = toric.signed_quotient_lattice(rows, columns)
        if not consistent:
            continue
        rank = DomainMatrix.from_list(rows, ZZ).rank()
        if rank >= columns:
            continue
        polynomials = [
            [
                tuple(rng.randrange(-2, 3) for _ in range(columns))
                for _ in range(rng.randrange(1, 5))
            ]
            for _ in range(3)
        ]
        reduced = reduced_product_nonzero(rows, polynomials)
        try:
            result = exact_toric_specialization(rows, polynomials)
            has_specialization = True
        except AssertionError:
            result = None
            has_specialization = False
        assert has_specialization == reduced
        if result is not None:
            order, base, roots, powers, family_terms = result
            assert all(
                sum(a * b for a, b in zip(row, powers)) == 0
                and sum(a * b for a, b in zip(row, roots)) % order
                == order // 2
                for row in rows
            )
            assert all(
                tuple(
                    (
                        sum(a * b for a, b in zip(monomial, roots)) % order,
                        sum(a * b for a, b in zip(monomial, powers)),
                    )
                    for monomial in polynomial
                )
                == terms
                and not specialized_sum_is_zero(order, base, terms)
                for polynomial, terms in zip(polynomials, family_terms)
            )
            free_reconstructed += 1
        free_checked += 1

    print(
        f"PASS: {checked} exact signed-quotient products equal exhaustive "
        f"root-of-unity evaluation ({len(cache)} cyclotomic sums); "
        f"reconstructed {reconstructed} nonzero specializations; "
        f"{free_checked} rank-deficient quotient checks reconstructed "
        f"{free_reconstructed} nonzero free-torus specializations; "
        "forced torsion-branch and integer-base retries"
    )


if __name__ == "__main__":
    main()
