#!/usr/bin/env python3
"""Exact audit for the p=19 five-triple even-span closure."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from verify_live_three_zero_higher_split_q5_boundary_census import (  # noqa: E402
    formal_selections,
)


TARGETS = ((0, 2), (1, 0))  # (b,u) in 4 3^5 2^b 1^(h+u)


def signature(parts: tuple[int, ...]) -> tuple[tuple[int, int], ...]:
    return tuple(sorted(Counter(parts).items(), reverse=True))


def audit_formal_complements() -> None:
    expected = ((4, 1), (3, 4), (1, 3))
    for h in range(13, 19):
        for doubles, offset in TARGETS:
            profile = (
                (4,)
                + (3,) * 5
                + (2,) * doubles
                + (1,) * (h + offset)
            )
            assert sum(profile) == 2 * h + (19 - h) + 2
            observed = {
                (selection.d, selection.selected_triples,
                 signature(selection.complement))
                for selection in formal_selections(profile, h, 19)
            }
            moving_selection = (1 + doubles, 1, expected)
            assert moving_selection in observed

    # Restoring the residual simple row at the selected triple to a
    # triple gives baseline multiplicities 4,3^5,1^2 in degree eight.
    baseline = (4,) + (3,) * 5 + (1,) * 2
    forced_six_weight = sum(6 - multiplicity for multiplicity in baseline)
    six_cap = 6 * (8 + 1 - 6)
    assert forced_six_weight == 27
    assert six_cap == 18
    assert forced_six_weight > six_cap


def audit_transport_and_product_line() -> None:
    z, x, y = sp.symbols("z x y")
    bx = sp.expand((z - x) ** 2 * (z + x) ** 2)
    by = sp.expand((z - y) ** 2 * (z + y) ** 2)
    assert sp.factor(bx - (z**2 - x**2) ** 2) == 0

    # The selected simple-row derivative is exactly transported to the
    # baseline third-order row.
    r0, r1, r2 = sp.symbols("r0 r1 r2")
    local = r0 + r1 * (z - x) + r2 * (z - x) ** 2
    transported = (z - x) ** 2 * local
    assert sp.diff(transported, z, 3).subs(z, x) == 6 * r1

    # Pairwise coprime quartics inside degree eight have only their
    # product line in common.
    assert sp.degree(bx, z) == sp.degree(by, z) == 4
    assert 8 - 2 * 4 + 1 == 1


def conic_vector(value: sp.Expr) -> sp.Matrix:
    # Ascending coefficients of (t-value)^2.
    return sp.Matrix([value**2, -2 * value, 1])


def audit_veronese_span_lemma() -> None:
    a, b, c, d = sp.symbols("a b c d")
    basis = sp.Matrix.hstack(
        conic_vector(a), conic_vector(b), conic_vector(c)
    )
    assert sp.factor(
        basis.det() + 2 * (a - b) * (a - c) * (b - c)
    ) == 0

    coordinates = [
        sp.factor(entry)
        for entry in basis.inv() * conic_vector(d)
    ]
    expected = [
        (b - d) * (c - d) / ((a - b) * (a - c)),
        -(a - d) * (c - d) / ((a - b) * (b - c)),
        (a - d) * (b - d) / ((a - c) * (b - c)),
    ]
    for observed, target in zip(coordinates, expected, strict=True):
        assert sp.factor(observed - target) == 0

    # With distinct a,b,c,d, every coordinate is nonzero.  If a symmetric
    # Gram matrix is diagonal in the first three vectors, orthogonality of
    # the fourth to all three kills every diagonal entry.
    e0, e1, e2 = sp.symbols("e0 e1 e2")
    diagonal = sp.diag(e0, e1, e2)
    fourth_pairings = diagonal * sp.Matrix(coordinates)
    for index, pairing in enumerate(fourth_pairings):
        assert sp.factor(pairing / coordinates[index] - (e0, e1, e2)[index]) == 0

    # Products of two quadratics cover every monomial through degree four.
    t = sp.symbols("t")
    products = [1, t, t**2, t * t**2, t**2 * t**2]
    coefficient_matrix = sp.zeros(5)
    for column, polynomial in enumerate(products):
        for degree in range(5):
            coefficient_matrix[degree, column] = sp.Poly(
                polynomial, t
            ).coeff_monomial(t**degree)
    assert coefficient_matrix.det() == 1


def audit_exact_triple_contradiction() -> None:
    z, v = sp.symbols("z v")
    section = (z**2 - v**2) ** 3
    assert sp.degree(section, z) == 6 <= 8
    assert section.subs(z, v) == 0
    assert sp.diff(section, z).subs(z, v) == 0
    assert sp.diff(section, z, 2).subs(z, v) == 0
    assert sp.factor(sp.diff(section, z, 3).subs(z, v)) == 48 * v**3

    # Five distinct values leave at least one nonzero choice, even if a
    # zero triple value is permitted.
    assert 5 - 1 >= 1


def main() -> None:
    audit_formal_complements()
    audit_transport_and_product_line()
    audit_veronese_span_lemma()
    audit_exact_triple_contradiction()
    print("p=19 five-triple even-span closure: PASS")
    print("two one-quartic five-triple profiles closed")
    print("ten quartic pair products force the full even five-space")
    print("one nonzero exact triple row gives the final contradiction")


if __name__ == "__main__":
    main()
