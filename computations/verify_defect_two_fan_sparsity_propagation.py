#!/usr/bin/env python3
"""Tiny exact audit for defect-two fan sparsity propagation.

This checker has no project imports.  It verifies only the finite support
ledger and the selected-row site-square-zero guard; the uniform theorem is
the hand proof in notes/defect-two-fan-sparsity-propagation.md.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product


SITES = ("x", "1", "2", "3", "4")
SITE_ORDER = {site: index for index, site in enumerate(SITES)}
COLORS = range(3)

# A monomial is an ordered tuple of (physical site, color) pairs.  A
# polynomial is a sparse dictionary with exact rational coefficients.
Monomial = tuple[tuple[str, int], ...]
Polynomial = dict[Monomial, Fraction]


def normalize(items: tuple[tuple[str, int], ...]) -> Monomial:
    return tuple(sorted(items, key=lambda item: SITE_ORDER[item[0]]))


def cell(site: str, color: int) -> Polynomial:
    return {((site, color),): Fraction(1)}


def add(left: Polynomial, right: Polynomial) -> Polynomial:
    answer = dict(left)
    for monomial, coefficient in right.items():
        value = answer.get(monomial, Fraction(0)) + coefficient
        if value:
            answer[monomial] = value
        else:
            answer.pop(monomial, None)
    return answer


def scale(polynomial: Polynomial, scalar: Fraction | int) -> Polynomial:
    scalar = Fraction(scalar)
    return {
        monomial: scalar * coefficient
        for monomial, coefficient in polynomial.items()
        if scalar * coefficient
    }


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    answer: Polynomial = {}
    for left_monomial, left_coefficient in left.items():
        left_sites = {site for site, _ in left_monomial}
        for right_monomial, right_coefficient in right.items():
            right_sites = {site for site, _ in right_monomial}
            if left_sites & right_sites:
                continue
            monomial = normalize(left_monomial + right_monomial)
            coefficient = left_coefficient * right_coefficient
            answer[monomial] = answer.get(monomial, Fraction(0)) + coefficient
    return {monomial: value for monomial, value in answer.items() if value}


def product_of(*polynomials: Polynomial) -> Polynomial:
    answer: Polynomial = {(): Fraction(1)}
    for polynomial in polynomials:
        answer = multiply(answer, polynomial)
    return answer


def divided_square(polynomial: Polynomial) -> Polynomial:
    return scale(multiply(polynomial, polynomial), Fraction(1, 2))


def audit_deleted_support_implication() -> None:
    universe = tuple(range(6))
    # Include one label outside each support to audit the u notin S case.
    deleted_labels = universe + (6,)
    for size in range(len(universe) + 1):
        for support_tuple in combinations(universe, size):
            support = set(support_tuple)
            for deleted in deleted_labels:
                if len(support) >= 3 and len(support - {deleted}) <= 2:
                    assert len(support) == 3
                    assert deleted in support


def audit_sharp_nine_bound() -> None:
    universe = tuple(range(9))
    three_sets = tuple(map(set, combinations(universe, 3)))
    maximum = max(
        len(first | second | third)
        for first, second, third in product(three_sets, repeat=3)
    )
    assert maximum == 9
    sharp_witness = ({0, 1, 2}, {3, 4, 5}, {6, 7, 8})
    assert len(set().union(*sharp_witness)) == 9


def audit_fan_arithmetic() -> None:
    for order in range(18, 102, 2):
        fan_lower_bound = order - 7
        defect_at_least_three = fan_lower_bound - 9
        assert defect_at_least_three == order - 16


def target_word(color: int) -> Polynomial:
    return product_of(*(cell(site, color) for site in SITES))


def audit_selected_row_guard() -> None:
    for center_color in COLORS:
        p = cell("x", center_color)
        q = add(
            product_of(cell("1", center_color), cell("2", center_color)),
            product_of(cell("3", center_color), cell("4", center_color)),
        )
        q_divided_two = divided_square(q)
        expected_q_divided_two = product_of(
            cell("1", center_color),
            cell("2", center_color),
            cell("3", center_color),
            cell("4", center_color),
        )
        assert q_divided_two == expected_q_divided_two

        # The two triples are copies of the coordinate basis at site x.
        s_rows = tuple(cell("x", color) for color in COLORS)
        t_rows = tuple(cell("x", color) for color in COLORS)
        assert len({next(iter(row)) for row in s_rows}) == 3
        assert len({next(iter(row)) for row in t_rows}) == 3

        for d, e in product(COLORS, repeat=2):
            direct = int(d == center_color and e == center_color)
            star_product = multiply(s_rows[d], t_rows[e])
            assert star_product == {}
            response = add(
                scale(q_divided_two, direct),
                multiply(star_product, q),
            )
            left = multiply(p, response)
            right = target_word(center_color) if direct else {}
            assert left == right, (center_color, d, e, left, right)


def main() -> None:
    audit_deleted_support_implication()
    print("PASS deleted-support implication")
    audit_sharp_nine_bound()
    print("PASS sharp three-times-three exceptional bound")
    audit_fan_arithmetic()
    print("PASS N-16 fan arithmetic")
    audit_selected_row_guard()
    print("PASS exact selected-row nine-packet guard")


if __name__ == "__main__":
    main()
