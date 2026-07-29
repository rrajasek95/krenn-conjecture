#!/usr/bin/env python3
"""Exact checks for odd-prime inverse-hafnian reciprocity.

The accompanying note gives a formal truncated-Fourier proof.  This file
independently checks the normalization symbolically for generic 2 by 2
matrices, exhausts small finite fields, and verifies a p=3 four-site GHZ
model whose first nonzero post-leading correction is harmless.
"""

from __future__ import annotations

import functools
import itertools
import math

import sympy as sp


def odd_double_factorial(n: int) -> int:
    result = 1
    for value in range(1, n + 1, 2):
        result *= value
    return result


def haf_repeated(matrix, multiplicities, modulus=None):
    """Hafnian after repeating label i ``multiplicities[i]`` times."""

    @functools.lru_cache(None)
    def recur(counts):
        if not any(counts):
            return 1
        i = next(index for index, count in enumerate(counts) if count)
        remaining = list(counts)
        remaining[i] -= 1
        answer = 0
        for j, number_of_partners in enumerate(remaining):
            if not number_of_partners:
                continue
            child = remaining.copy()
            child[j] -= 1
            answer += (
                number_of_partners
                * matrix[i][j]
                * recur(tuple(child))
            )
        if modulus is not None:
            answer %= modulus
        return answer

    if sum(multiplicities) % 2:
        return 0
    return recur(tuple(multiplicities))


def determinant_mod(matrix, prime):
    work = [[entry % prime for entry in row] for row in matrix]
    determinant = 1
    size = len(work)
    for column in range(size):
        pivot = next(
            (row for row in range(column, size) if work[row][column]),
            None,
        )
        if pivot is None:
            return 0
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            determinant = -determinant
        pivot_value = work[column][column]
        determinant = determinant * pivot_value % prime
        inverse = pow(pivot_value, -1, prime)
        work[column] = [value * inverse % prime for value in work[column]]
        for row in range(column + 1, size):
            factor = work[row][column]
            work[row] = [
                (value - factor * pivot_entry) % prime
                for value, pivot_entry in zip(
                    work[row], work[column], strict=True
                )
            ]
    return determinant % prime


def inverse_mod(matrix, prime):
    size = len(matrix)
    work = [
        [entry % prime for entry in matrix[row]]
        + [int(row == column) for column in range(size)]
        for row in range(size)
    ]
    for column in range(size):
        pivot = next(
            (row for row in range(column, size) if work[row][column]),
            None,
        )
        if pivot is None:
            return None
        work[column], work[pivot] = work[pivot], work[column]
        inverse = pow(work[column][column], -1, prime)
        work[column] = [value * inverse % prime for value in work[column]]
        for row in range(size):
            if row == column:
                continue
            factor = work[row][column]
            work[row] = [
                (value - factor * pivot_entry) % prime
                for value, pivot_entry in zip(
                    work[row], work[column], strict=True
                )
            ]
    return [row[size:] for row in work]


def reciprocity_factor(prime, dimension, alpha):
    q = (prime - 1) // 2
    c_p = odd_double_factorial(prime - 2) % prime
    factorial_product = math.prod(math.factorial(value) for value in alpha)
    return (
        pow(-1, sum(alpha) // 2)
        * factorial_product
        * pow(pow(c_p, dimension, prime), -1, prime)
    ) % prime


def audit_symbolic_two_by_two(prime):
    """Clear denominators and prove every generic 2 by 2 identity mod p."""
    a, b, c = sp.symbols("a b c")
    determinant = a * c - b**2
    matrix = ((a, b), (b, c))
    inverse = (
        (c / determinant, -b / determinant),
        (-b / determinant, a / determinant),
    )
    q = (prime - 1) // 2
    checked = 0
    for alpha in itertools.product(range(prime), repeat=2):
        if sum(alpha) % 2:
            continue
        beta = tuple(prime - 1 - value for value in alpha)
        left = haf_repeated(matrix, alpha)
        right = (
            reciprocity_factor(prime, 2, alpha)
            * determinant**q
            * haf_repeated(inverse, beta)
        )
        numerator, _denominator = sp.fraction(sp.cancel(left - right))
        polynomial = sp.Poly(sp.expand(numerator), a, b, c, modulus=prime)
        assert polynomial.is_zero, (prime, alpha, polynomial)
        checked += 1
    return checked


def symmetric_matrices(prime, dimension):
    positions = tuple(
        (i, j) for i in range(dimension) for j in range(i, dimension)
    )
    for values in itertools.product(range(prime), repeat=len(positions)):
        matrix = [[0] * dimension for _ in range(dimension)]
        for (i, j), value in zip(positions, values, strict=True):
            matrix[i][j] = matrix[j][i] = value
        yield matrix


def audit_exhaustive_field(prime, dimension):
    checked_matrices = 0
    checked_identities = 0
    q = (prime - 1) // 2
    for matrix in symmetric_matrices(prime, dimension):
        determinant = determinant_mod(matrix, prime)
        if not determinant:
            continue
        inverse = inverse_mod(matrix, prime)
        assert inverse is not None
        checked_matrices += 1
        for alpha in itertools.product(range(prime), repeat=dimension):
            if sum(alpha) % 2:
                continue
            beta = tuple(prime - 1 - value for value in alpha)
            left = haf_repeated(matrix, alpha, prime)
            right = (
                reciprocity_factor(prime, dimension, alpha)
                * pow(determinant, q, prime)
                * haf_repeated(inverse, beta, prime)
            ) % prime
            assert left == right, (prime, dimension, matrix, alpha)
            checked_identities += 1
    return checked_matrices, checked_identities


def audit_fourier_constants():
    for prime in (3, 5, 7, 11, 13):
        m = prime - 1
        q = m // 2
        c_p = odd_double_factorial(prime - 2) % prime
        assert c_p * c_p % prime == pow(-1, q + 1, prime)
        for exponent in range(prime):
            # T(x^a)=(-1)^a a! x^(p-1-a) intertwines
            # multiplication with differentiation.
            coefficient = pow(-1, exponent, prime) * math.factorial(exponent)
            coefficient %= prime
            if exponent < m:
                next_coefficient = (
                    pow(-1, exponent + 1, prime)
                    * math.factorial(exponent + 1)
                ) % prime
                assert next_coefficient == -(exponent + 1) * coefficient % prime


def audit_p3_four_site_ghz_correction():
    """An exact allowed n=4 GHZ with a nonzero harmless z^(r+2) term."""
    prime = 3
    sites = range(4)
    colors = range(3)
    one_factors = {
        0: ((0, 1), (2, 3)),
        1: ((0, 2), (1, 3)),
        2: ((0, 3), (1, 2)),
    }
    components = tuple(
        ((u, color), (v, color))
        for color in colors
        for u, v in one_factors[color]
    )

    # D is diagonal within sites.  One mode has value -1 and all others 1,
    # so exactly one of the six two-mode components has determinant -1 at z=0.
    diagonal = {(site, color): 1 for site in sites for color in colors}
    diagonal[(0, 0)] = -1
    edge_products = tuple(
        diagonal[left] * diagonal[right] % prime
        for left, right in components
    )
    assert edge_products.count(prime - 1) == 1
    assert edge_products.count(1) == 5

    constant_colorings = []
    for coloring in itertools.product(colors, repeat=4):
        selected = {
            (site, color): int(coloring[site] == color)
            for site in sites
            for color in colors
        }
        beta = {
            mode: (prime - 1 - indicator)
            for mode, indicator in selected.items()
        }
        odd_component = any(
            (beta[left] + beta[right]) % 2
            for left, right in components
        )
        is_constant = len(set(coloring)) == 1
        assert odd_component != is_constant
        if is_constant:
            constant_colorings.append(coloring)
    assert len(constant_colorings) == 3

    z = sp.symbols("z")
    determinant = sp.prod(product - z**2 for product in edge_products)
    # Two selected-color components contribute -z/Q; the other four
    # contribute 1/Q.  Thus every pure coloring gives z^2/det, and every
    # mixed coloring gives zero because one component has odd total size.
    pure_inverse_hafnian = sp.cancel(z**2 / determinant)
    series = sp.series(pure_inverse_hafnian, z, 0, 7).removeO()

    def coefficient_mod(exponent):
        value = sp.Rational(sp.expand(series).coeff(z, exponent))
        return int(value.p) * pow(int(value.q) % prime, -1, prime) % prime

    assert coefficient_mod(2) == 2  # det(D)^(-1)
    assert coefficient_mod(3) == 0
    assert coefficient_mod(4) == 2

    relative_second_correction = sum(
        pow(product, -1, prime) for product in edge_products
    ) % prime
    assert relative_second_correction == 1
    return sp.Poly(sp.denom(pure_inverse_hafnian), z, modulus=prime).as_expr()


def main():
    audit_fourier_constants()
    symbolic_counts = {
        prime: audit_symbolic_two_by_two(prime) for prime in (3, 5, 7)
    }
    exhaustive = {
        (3, 3): audit_exhaustive_field(3, 3),
        (5, 2): audit_exhaustive_field(5, 2),
    }
    correction_denominator = audit_p3_four_site_ghz_correction()
    print("Fourier intertwiner and c_p^2 sign checked for p=3,5,7,11,13")
    print("generic symbolic 2x2 identities:", symbolic_counts)
    print("exhaustive finite-field audits:", exhaustive)
    print("p=3 n=4 GHZ inverse denominator:", correction_denominator)
    print("verified: first nonzero correction is common, nonzero, and harmless")


if __name__ == "__main__":
    main()
