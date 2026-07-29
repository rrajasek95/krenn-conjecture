#!/usr/bin/env python3
"""Tiny exact audit for the two-star pure-response obstruction.

The proof is uniform.  This dependency-free script checks its combinatorial
bookkeeping: the binary Hamming-level incidence identity, pure-product
levels, contraction at a unique exceptional site, extraction of the two
x-slices, and the order/rank-graph counts.  It is not a bounded search for
the theorem.
"""

from collections import Counter
from itertools import product
from math import comb


def insert(word, site, value):
    answer = list(word)
    answer.insert(site, value)
    return tuple(answer)


def audit_hamming_levels(max_sites=7):
    variables = 0
    identities = 0
    for sites in range(1, max_sites + 1):
        a_levels = [Counter() for _ in range(sites + 1)]
        b_levels = [Counter() for _ in range(sites + 1)]
        for missing in range(sites):
            for word in product(range(2), repeat=sites - 1):
                variable = (missing, word)
                a_word = insert(word, missing, 0)
                b_word = insert(word, missing, 1)
                a_levels[sum(a_word)][variable] += 1
                b_levels[sum(b_word)][variable] += 1
                variables += 1

        for weight in range(sites):
            assert a_levels[weight] == b_levels[weight + 1]
            assert len(a_levels[weight]) == (
                sites * comb(sites - 1, weight)
            )
            identities += 1
        assert not a_levels[sites]
    return variables, identities


def polynomial_product(factors):
    coefficients = [1]
    for alpha, beta in factors:
        updated = [0] * (len(coefficients) + 1)
        for degree, value in enumerate(coefficients):
            updated[degree] += alpha * value
            updated[degree + 1] += beta * value
        coefficients = updated
    return coefficients


def audit_pure_levels(max_sites=7):
    formal_terms = 0
    for sites in range(1, max_sites + 1):
        levels = [Counter() for _ in range(sites + 1)]
        for bits in product(range(2), repeat=sites):
            monomial = tuple(
                ("beta" if bit else "alpha", site)
                for site, bit in enumerate(bits)
            )
            levels[sum(bits)][monomial] += 1
            formal_terms += 1
        assert [len(level) for level in levels] == [
            comb(sites, weight) for weight in range(sites + 1)
        ]

    examples = (
        ((1, 1), (1, -1)),
        ((0, 2), (3, 0), (1, -1)),
        ((1, 2), (-2, 1), (3, 5), (7, -4)),
    )
    for factors in examples:
        assert all(pair != (0, 0) for pair in factors)
        assert any(polynomial_product(factors))
    assert polynomial_product(examples[0]) == [1, 0, -1]
    return formal_terms, len(examples)


def dense_cofactor(sites, colours=3):
    answer = Counter()
    for missing in range(sites):
        for assignment in product(range(colours), repeat=sites - 1):
            word = insert(assignment, missing, -1)
            coefficient = 1 + (
                missing
                + sum((site + 1) * (colour + 2)
                      for site, colour in enumerate(word)
                      if colour >= 0)
            ) % 11
            answer[missing, word] = coefficient
    return answer


def multiply_star(star, cofactor):
    answer = Counter()
    for (missing, word), coefficient in cofactor.items():
        assert word[missing] == -1
        for colour, star_coefficient in enumerate(star[missing]):
            if not star_coefficient:
                continue
            full_word = list(word)
            full_word[missing] = colour
            answer[tuple(full_word)] += coefficient * star_coefficient
    return Counter({word: value for word, value in answer.items() if value})


def contract_top(polynomial, site, covector):
    answer = Counter()
    for word, coefficient in polynomial.items():
        answer[word[:site] + word[site + 1:]] += (
            coefficient * covector[word[site]]
        )
    return Counter({word: value for word, value in answer.items() if value})


def contract_cofactor(cofactor, site, covector):
    answer = Counter()
    for (missing, word), coefficient in cofactor.items():
        if missing == site:
            continue
        new_missing = missing - (missing > site)
        new_word = word[:site] + word[site + 1:]
        answer[new_missing, new_word] += coefficient * covector[word[site]]
    return Counter({key: value for key, value in answer.items() if value})


def audit_unique_site_contraction():
    sites = 5
    exceptional = 2
    cofactor = dense_cofactor(sites)
    covector = (0, 1, 0)

    a_star = []
    b_star = []
    for site in range(sites):
        if site == exceptional:
            a_star.append((3, 0, 0))
            b_star.append((-2, 0, 0))
        else:
            a_star.append((site + 1, 2 - site, 1))
            b_star.append((1, site + 2, 3 - site))

    reduced = contract_cofactor(cofactor, exceptional, covector)
    reduced_a = a_star[:exceptional] + a_star[exceptional + 1:]
    reduced_b = b_star[:exceptional] + b_star[exceptional + 1:]

    assert contract_top(
        multiply_star(a_star, cofactor), exceptional, covector
    ) == multiply_star(reduced_a, reduced)
    assert contract_top(
        multiply_star(b_star, cofactor), exceptional, covector
    ) == multiply_star(reduced_b, reduced)

    expected_terms = (sites - 1) * 3 ** (sites - 2)
    assert len(reduced) == expected_terms
    return len(cofactor), len(reduced)


def extract_slices(cofactor, site, colours=3):
    slices = [Counter() for _ in range(colours)]
    for (missing, word), coefficient in cofactor.items():
        if missing == site:
            continue
        colour = word[site]
        new_missing = missing - (missing > site)
        new_word = word[:site] + word[site + 1:]
        slices[colour][new_missing, new_word] += coefficient
    return slices


def top_slice(polynomial, site, colour):
    return Counter({
        word[:site] + word[site + 1:]: coefficient
        for word, coefficient in polynomial.items()
        if word[site] == colour
    })


def audit_overlap_slices():
    sites = 5
    x_site = 0
    cofactor = dense_cofactor(sites)
    slices = extract_slices(cofactor, x_site)
    stars = (
        [(0, 0, 0), (1, 2, 0), (0, 1, 3), (2, 0, 1), (1, -1, 2)],
        [(0, 0, 0), (0, 1, 2), (3, 1, 0), (1, 2, -1), (2, 1, 1)],
    )
    checked = 0
    for star in stars:
        full_product = multiply_star(star, cofactor)
        reduced_star = star[1:]
        for colour in range(3):
            assert top_slice(full_product, x_site, colour) == multiply_star(
                reduced_star, slices[colour]
            )
            checked += 1
    return checked


def audit_degrees_and_graph():
    orders = 0
    for m in range(3, 13):
        total_sites = 2 * m
        y_sites = total_sites - 3
        z_sites = total_sites - 4
        f_degree = 2 * (m - 2)
        g_degree = f_degree - 1
        assert f_degree == y_sites - 1
        assert g_degree == z_sites - 1
        assert (total_sites - 1) - (3 + 2) == total_sites - 6
        orders += 1

    total_sites = 8
    z_sites = 4
    named_singular = 3
    exported_singular = 2
    rank_three_degree = (
        total_sites - 1 - named_singular - exported_singular
    )
    assert z_sites == 4
    assert rank_three_degree == 2
    return orders, rank_three_degree


def main():
    variables, levels = audit_hamming_levels()
    formal_terms, examples = audit_pure_levels()
    original, reduced = audit_unique_site_contraction()
    slices = audit_overlap_slices()
    orders, degree = audit_degrees_and_graph()
    print(
        "two-star pure-response audit: "
        f"cube variables={variables}, level identities={levels}, "
        f"pure terms={formal_terms}, examples={examples}; "
        f"contraction={original}->{reduced}; slices={slices}; "
        f"orders={orders}, N=8 degree bound={degree}"
    )


if __name__ == "__main__":
    main()
