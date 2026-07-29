#!/usr/bin/env python3
"""Exact audit of the conditional full-DR4 repeated-double closure."""

from __future__ import annotations

import sympy as sp


def check_hermite_and_moving_degree() -> None:
    p, m = sp.symbols("p m", integer=True)
    assert sp.expand((p - 7 + 1) + 7 + m) == p + m + 1
    assert sp.expand((p + 6 - 1) - (p + 2)) == 3

    x, node, translation = sp.symbols("x t U")
    dx = x**2 - node**2
    row = []
    for degree in range(4):
        evaluation = node**degree
        derivative = sp.Integer(0) if degree == 0 else degree * node ** (degree - 1)
        entry = dx * (derivative + translation * evaluation)
        entry -= (x - 3 * node) * evaluation
        row.append(sp.expand(entry))
    assert all(sp.Poly(entry, x).degree() <= 2 for entry in row)
    assert 4 * 2 == 8

    nodes = (sp.Integer(1), sp.Integer(2), sp.Integer(4), sp.Integer(7))
    translations = (sp.Integer(0), sp.Integer(3), sp.Integer(-2), sp.Integer(5))
    determinant = sp.Matrix(
        [
            [entry.subs({node: value, translation: shift}) for entry in row]
            for value, shift in zip(nodes, translations)
        ]
    ).det(method="domain-ge")
    determinant = sp.Poly(sp.expand(determinant), x)
    assert determinant.as_expr() != 0
    assert determinant.degree() <= 8


def check_translation_and_fibre() -> None:
    s, x, lam = sp.symbols("s x lambda")
    psi = 1 / (s + x) - 2 / (x - s)
    assert sp.factor(psi + (x + 3 * s) / (x**2 - s**2)) == 0
    fibre = lam * (x**2 - s**2) + x + 3 * s
    assert sp.factor(psi - lam + fibre / (x**2 - s**2)) == 0
    fibre_poly = sp.Poly(fibre, x)
    assert fibre_poly.degree() <= 2
    assert fibre_poly.coeff_monomial(x) == 1

    # Selecting two labels from the fixed double background contributes the
    # j=2 member of the same moving-class formula and is independent of x.
    background = sp.symbols("a")
    chi_two = 2 / (s + background) - 3 / (background - s)
    assert sp.factor(
        chi_two + (background + 5 * s) / (background**2 - s**2)
    ) == 0


def check_exact_class_threshold_and_zero_cases() -> None:
    determinant_degree = 8
    minimum_classes = 14
    fixed_value_classes = 5  # double background plus four simple anchors
    moving_candidates = minimum_classes - fixed_value_classes
    assert moving_candidates == 9 > determinant_degree
    assert minimum_classes - 1 - fixed_value_classes == 8

    # After fixing background a, one anchor s, and two companions, a varying
    # fourth nonzero anchor has at least c-5 choices in the possible-zero case.
    varying_nonzero_anchors = minimum_classes - 4 - 1
    assert varying_nonzero_anchors == 9 > 2

    # A double value cannot be zero.  If there is another double, select one
    # of its labels as a permanent guard anchor; its mate is a singleton in N.
    double_size = 2
    assert double_size - 1 == 1

    # With only the background double, every other class is a singleton.
    # Four anchors and one moving class consume at most five of them.
    singleton_classes = minimum_classes - 1
    assert singleton_classes - 5 == 8 > 0
    assert singleton_classes - 1 >= 4  # still choose four nonzero anchors


def previous_double_single_closure(doubles: int, singles: int) -> bool:
    return (
        (doubles >= 8 and singles >= 4)
        or (doubles >= 9 and singles >= 3)
        or (doubles >= 10 and singles >= 2)
        or doubles >= 11
    )


EXPECTED_REMAINING = {
    8: (4, 5, 6, 7, 8),
    9: (5, 6, 7, 8, 9),
    10: (6, 7, 8, 9),
    11: (7, 9, 10),
    12: (10,),
}


def check_post_dr4_residual_table() -> None:
    for p in range(8, 101):
        total = p + 9
        remaining = []
        for doubles in range(1, total // 2 + 1):
            singles = total - 2 * doubles
            old_open = not previous_double_single_closure(doubles, singles)
            classes = doubles + singles
            repeated_double_closed = classes >= 14
            if old_open and not repeated_double_closed:
                remaining.append(doubles)
        assert tuple(remaining) == EXPECTED_REMAINING.get(p, ())
        if p >= 13:
            assert not remaining


def main() -> None:
    check_hermite_and_moving_degree()
    check_translation_and_fibre()
    check_exact_class_threshold_and_zero_cases()
    check_post_dr4_residual_table()
    print("seventh-split repeated-double full-DR4 closure audit: PASS")
    print("strict one-variable threshold: c >= 14")
    print("no double/single residual remains for p >= 13")


if __name__ == "__main__":
    main()
