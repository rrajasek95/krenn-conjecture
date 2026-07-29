#!/usr/bin/env python3
"""Tiny exact audit for the centered rank-one overlap packet.

This dependency-free checker verifies the contracted target table, the
five-site common-q relaxation, and the finite incidence/channel guards in
the minimal-private proof.  It does not search source parameters.
"""

from collections import Counter
from fractions import Fraction
from itertools import combinations, product


COLOURS = range(3)
Y = frozenset(range(5))
PORTS = (0, 1, 2)
EMPTY = (-1,) * 5


def cell(left, right, left_colour, right_colour):
    word = [-1] * 5
    word[left] = left_colour
    word[right] = right_colour
    return Counter({tuple(word): 1})


def monomer(site, colour):
    word = [-1] * 5
    word[site] = colour
    return Counter({tuple(word): 1})


def add(*polynomials):
    answer = Counter()
    for polynomial in polynomials:
        answer.update(polynomial)
    return Counter({word: value for word, value in answer.items() if value})


def multiply(left, right):
    answer = Counter()
    for left_word, left_value in left.items():
        for right_word, right_value in right.items():
            if any(a != -1 and b != -1
                   for a, b in zip(left_word, right_word)):
                continue
            word = tuple(b if a == -1 else a
                         for a, b in zip(left_word, right_word))
            answer[word] += left_value * right_value
    return Counter({word: value for word, value in answer.items() if value})


def pure_word(colour, missing=None):
    return tuple(-1 if site == missing else colour for site in range(5))


def audit_contracted_table():
    f = (1, 0, 0)
    h = (0, 1, -1)
    basis = {"f": f, "h": h}
    expected = {
        ("f", "f"): (1, 0, 0),
        ("f", "h"): (0, 0, 0),
        ("h", "f"): (0, 0, 0),
        ("h", "h"): (0, 1, 1),
    }
    checked = 0
    for left, right in product(basis, repeat=2):
        coefficients = tuple(basis[left][e] * basis[right][e]
                             for e in COLOURS)
        assert coefficients == expected[left, right]
        checked += 3
    return checked


def audit_common_q_relaxation():
    q = add(cell(3, 4, 0, 0), cell(2, 4, 1, 1), cell(1, 3, 2, 2))
    z_ff = cell(1, 2, 0, 0)
    z_hh = add(cell(0, 3, 1, 1), cell(0, 4, 2, 2))
    zero = Counter()
    cofactors = {
        ("f", "f"): multiply(z_ff, q),
        ("f", "h"): zero,
        ("h", "f"): zero,
        ("h", "h"): multiply(z_hh, q),
    }
    assert cofactors["f", "f"] == Counter({pure_word(0, 0): 1})
    assert cofactors["h", "h"] == Counter({
        pure_word(1, 1): 1,
        pure_word(2, 2): 1,
    })

    stars = (monomer(0, 0), monomer(1, 1), monomer(2, 2))
    target_coefficients = {
        ("f", "f"): (1, 0, 0),
        ("f", "h"): (0, 0, 0),
        ("h", "f"): (0, 0, 0),
        ("h", "h"): (0, 1, 1),
    }
    checked = 0
    for key, cofactor in cofactors.items():
        for colour, star in enumerate(stars):
            actual = multiply(star, cofactor)
            expected = (Counter({(colour,) * 5: 1})
                        if target_coefficients[key][colour] else Counter())
            assert actual == expected
            checked += 1
    return checked


def private_designs():
    options = []
    for port in PORTS:
        complement = Y - {port}
        choices = []
        for chosen in combinations(sorted(complement), 2):
            d_set = frozenset(chosen)
            choices.append((d_set, complement - d_set))
        options.append(choices)

    answer = []
    for design in product(*options):
        if all(design[c][0] & design[d][1]
               for c, d in product(COLOURS, repeat=2) if c != d):
            answer.append(design)
    return answer


def cell_divides_word(sites, colour, word):
    return all(word[site] == colour for site in sites)


def q_divisors(design, word):
    return [colour for colour in COLOURS
            if cell_divides_word(design[colour][1], colour, word)]


def q2_divisors(design, word):
    answer = []
    for left, right in combinations(COLOURS, 2):
        left_sites = design[left][1]
        right_sites = design[right][1]
        if (left_sites.isdisjoint(right_sites)
                and cell_divides_word(left_sites, left, word)
                and cell_divides_word(right_sites, right, word)):
            answer.append((left, right))
    return answer


def audit_private_incidence():
    designs = private_designs()
    assert len(designs) == 24
    case_one_checks = 0
    case_two = []
    for design in designs:
        active = [colour for colour in (1, 2) if 0 in design[colour][0]]
        if not active:
            case_two.append(design)
            continue
        for colour in active:
            other = 3 - colour
            word = [colour] * 5
            word[PORTS[colour]] = -1
            swapped = list(word)
            swapped[0] = other
            assert q_divisors(design, tuple(word)) == [colour]
            assert q_divisors(design, tuple(swapped)) == [colour]
            assert not q2_divisors(design, tuple(word))
            assert not q2_divisors(design, tuple(swapped))
            case_one_checks += 1
    assert case_one_checks == 24
    assert len(case_two) == 2

    expected = {
        (
            (frozenset({3, 4}), frozenset({1, 2})),
            (frozenset({2, 3}), frozenset({0, 4})),
            (frozenset({1, 4}), frozenset({0, 3})),
        ),
        (
            (frozenset({3, 4}), frozenset({1, 2})),
            (frozenset({2, 4}), frozenset({0, 3})),
            (frozenset({1, 3}), frozenset({0, 4})),
        ),
    }
    assert set(case_two) == expected
    return len(designs), case_one_checks, len(case_two)


def rational_rank(vectors):
    matrix = [[Fraction(value) for value in vector] for vector in vectors]
    rank = 0
    for column in range(3):
        pivot = next((row for row in range(rank, len(matrix))
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        scale = matrix[rank][column]
        matrix[rank] = [value / scale for value in matrix[rank]]
        for row in range(len(matrix)):
            if row != rank and matrix[row][column]:
                scale = matrix[row][column]
                matrix[row] = [left - scale * right
                               for left, right in zip(matrix[row], matrix[rank])]
        rank += 1
    return rank


def audit_transversality():
    f = (1, 0, 0)
    h = (0, 1, -1)
    e1 = (0, 1, 0)
    e2 = (0, 0, 1)
    assert rational_rank((f, h)) == 2
    assert rational_rank((f, h, e1)) == 3
    assert rational_rank((f, h, e2)) == 3
    return 2


def main():
    table = audit_contracted_table()
    products = audit_common_q_relaxation()
    designs, channels, residual = audit_private_incidence()
    transverse = audit_transversality()
    print("centered rank-one overlap packet: PASS")
    print(f"contracted cells={table}; common-q products={products}; "
          f"private designs={designs} ({channels} case-one channels, "
          f"{residual} residual designs); transversality={transverse}")


if __name__ == "__main__":
    main()
