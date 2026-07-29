#!/usr/bin/env python3
"""Exact audit of the eighth-split ``(4,3,3,3,3,3)`` closure."""

from __future__ import annotations

from itertools import permutations

import sympy as sp


def check_profile_and_legal_selections() -> None:
    h, p, k = 8, 9, 1
    multiplicities = (4,) + (3,) * 5
    assert sum(multiplicities) == p + h + 2 == 19

    # Class zero is selected three times.  Among the five triple classes,
    # one is full and one is selected twice.
    for full, partial in permutations(range(1, 6), 2):
        takes = [0] * 6
        takes[0] = 3
        takes[full] = 3
        takes[partial] = 2
        complement = tuple(m - take for m, take in zip(multiplicities, takes))
        assert sum(takes) == h
        assert sum(complement) == p + 2 == 11
        assert complement[0] == complement[partial] == 1
        assert len([take for take in takes if take]) == 3

        represented = 3
        denominator_degree = (k + 1) + sum(take + 1 for take in takes if take)
        numerator_cap = p + represented - 1
        residual_cap = numerator_cap - sum(complement)
        assert denominator_degree == 13
        assert numerator_cap == 11
        assert residual_cap == 0
        assert denominator_degree - numerator_cap == 2


def check_common_pole_logarithmic_derivative() -> None:
    mu, a, b, c = sp.symbols("mu a b c")
    triples = sp.symbols("x0:5")

    # At z=-mu, an unselected multiplicity-m class contributes
    # -m/(mu+x).  Selecting r labels changes this by Delta_r.
    def delta(r: int, x: sp.Expr) -> sp.Expr:
        return r / (x + mu) - (r + 1) / (x - mu)

    phi = sp.factor(delta(3, b))
    psi = sp.factor(delta(2, c))
    assert sp.factor(
        phi + (b + 7 * mu) / ((b - mu) * (b + mu))
    ) == 0
    assert sp.factor(
        psi + (c + 5 * mu) / ((c - mu) * (c + mu))
    ) == 0

    baseline = -4 / (mu + a) - sum(3 / (mu + x) for x in triples)
    role_form = baseline + delta(3, a) + delta(3, triples[0]) + delta(
        2, triples[1]
    )

    # Reconstruct the same expression directly from the regular cofactor
    # after selecting a^3, x0^3, x1^2.
    direct = -1 / (mu + a) - 4 / (a - mu)
    direct += -4 / (triples[0] - mu)
    direct += -1 / (mu + triples[1]) - 3 / (triples[1] - mu)
    direct += sum(-3 / (mu + x) for x in triples[2:])
    assert sp.factor(role_form - direct) == 0

    # Swapping the full-triple role from b to another triple d changes only
    # Phi(b)-Phi(d); the constants and the partial role stay fixed.
    d = sp.symbols("d")
    assert sp.factor(
        (baseline + delta(3, a) + delta(2, c) + delta(3, b))
        - (baseline + delta(3, a) + delta(2, c) + delta(3, d))
        - (delta(3, b) - delta(3, d))
    ) == 0


def check_fibre_obstruction() -> None:
    x, mu, value = sp.symbols("x mu value")
    phi = 3 / (x + mu) - 4 / (x - mu)
    assert sp.factor(phi + (x + 7 * mu) / (x**2 - mu**2)) == 0

    fibre = sp.expand(value * (x**2 - mu**2) + x + 7 * mu)
    assert sp.Poly(fibre, x).degree() == 2
    assert sp.Poly(fibre, x).coeff_monomial(x) == 1

    # Even if the quadratic coefficient vanishes, the fibre polynomial is
    # nonzero.  Thus any admissible fibre has at most two distinct points;
    # the proof produces four.
    assert sp.expand(fibre.subs(value, 0)) == x + 7 * mu
    number_of_triples = 5
    fixed_partial = 1
    full_role_candidates = number_of_triples - fixed_partial
    assert full_role_candidates == 4 > 2


def main() -> None:
    check_profile_and_legal_selections()
    check_common_pole_logarithmic_derivative()
    check_fibre_obstruction()
    print("eighth-split (4,3,3,3,3,3) common-pole closure: PASS")
    print("twenty legal 3+3+2 selections and constant residual: exact")
    print("full-triple role function Phi=-(x+7mu)/(x^2-mu^2): exact")
    print("four points in a degree-two fibre: impossible")


if __name__ == "__main__":
    main()
