#!/usr/bin/env python3
"""Exact audit of the h=8,k=4 six-exact-triple closure."""

from itertools import combinations, product
from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import verify_live_three_zero_higher_split_collision_frontier as frontier


def perfect_matchings(items):
    items = tuple(items)
    if not items:
        yield ()
        return
    first = items[0]
    for index in range(1, len(items)):
        second = items[index]
        rest = items[1:index] + items[index + 1 :]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


def main() -> None:
    x, y, mu, w = sp.symbols("x y mu w", nonzero=True)

    def rho(role, value):
        return (1 - w / (value + mu)) ** (-role) * (
            1 + w / (value - mu)
        ) ** (-(role + 1))

    def log_jet(role, value, order):
        return sp.factor(
            sp.diff(sp.log(rho(role, value)), w, order).subs(w, 0)
        )

    differences = [
        sp.factor(log_jet(3, x, order) - log_jet(2, x, order))
        for order in range(1, 5)
    ]
    d = differences[0]
    expected = (
        d,
        d**2 - d / mu,
        2 * d**3 - 3 * d**2 / mu,
        6 * d**4 - 12 * d**3 / mu + 3 * d**2 / mu**2,
    )
    for observed, target in zip(differences, expected):
        assert sp.factor(observed - target) == 0
    assert sp.factor(d + 2 * mu / (x**2 - mu**2)) == 0

    dy = d.xreplace({x: y})
    expected_difference = (
        2 * mu * (x - y) * (x + y)
        / ((x**2 - mu**2) * (y**2 - mu**2))
    )
    assert sp.factor(d - dy - expected_difference) == 0

    T, V, W, X, D = sp.symbols("T V W X D")

    def bell4(t, v, third, fourth):
        return t**4 + 6 * t**2 * v + 3 * v**2 + 4 * t * third + fourth

    dropped = sp.expand(
        bell4(
            T - D,
            V - (D**2 - D / mu),
            W - (2 * D**3 - 3 * D**2 / mu),
            X - (6 * D**4 - 12 * D**3 / mu + 3 * D**2 / mu**2),
        )
    )
    affine = bell4(T, V, W, X) + D * (
        -4 * T**3 + 6 * T**2 / mu - 12 * T * V + 6 * V / mu - 4 * W
    )
    assert sp.expand(dropped - affine) == 0
    assert sp.Poly(dropped, D).degree() == 1

    solved_w = -T**3 + 3 * T**2 / (2 * mu) - 3 * T * V + 3 * V / (2 * mu)
    slope = sp.diff(affine, D)
    assert sp.factor(slope.subs(W, solved_w)) == 0

    # Exact Boolean third difference of the triple identity.
    alpha, beta, gamma = sp.symbols("alpha beta gamma")
    A0, A1, A2, A3, A4, A5 = sp.symbols("A0:6")
    B0, B1, B2, B3, B4, B5 = sp.symbols("B0:6")
    C0, C1, C2, C3, C4, C5 = sp.symbols("C0:6")
    As = (A0, A1, A2, A3, A4, A5)
    Bs = (B0, B1, B2, B3, B4, B5)
    Cs = (C0, C1, C2, C3, C4, C5)

    def triple_identity(indices):
        tsum = alpha + sum(As[i] for i in indices)
        bsum = beta + sum(Bs[i] for i in indices)
        csum = gamma + sum(Cs[i] for i in indices)
        return (
            csum
            + tsum**3
            - 3 * tsum**2 / (2 * mu)
            + 3 * tsum * bsum
            - 3 * bsum / (2 * mu)
        )

    cube_difference = 0
    for bits in product((0, 1), repeat=3):
        indices = tuple(2 * axis + bit for axis, bit in enumerate(bits))
        cube_difference += (-1) ** sum(bits) * triple_identity(indices)
    target_cube = 6 * (A0 - A1) * (A2 - A3) * (A4 - A5)
    assert sp.expand(cube_difference - target_cube) == 0

    phi3 = log_jet(3, x, 1)
    assert sp.factor(phi3 + (x + 7 * mu) / (x**2 - mu**2)) == 0
    lam = sp.symbols("lam")
    fibre = lam * (x**2 - mu**2) + x + 7 * mu
    assert sp.Poly(fibre, x).degree() <= 2
    assert sp.Poly(fibre, x).coeff_monomial(x) == 1

    # Every colouring of six indices with fibre blocks of size at most two
    # has a perfect matching across unequal colours.
    matchings = tuple(perfect_matchings(range(6)))
    assert len(matchings) == 15
    for colours in product(range(6), repeat=6):
        if max(colours.count(colour) for colour in set(colours)) > 2:
            continue
        assert any(
            all(colours[i] != colours[j] for i, j in matching)
            for matching in matchings
        )

    h, k = 8, 4
    counts, residual_tuple = frontier.census(h, h + k)
    assert counts["R"] == 46
    residuals = set(residual_tuple)
    six_triple_profiles = {
        profile for profile in residuals if profile.count(3) >= 6
    }
    assert six_triple_profiles == {
        (4, 3, 3, 3, 3, 3, 3),
        (3, 3, 3, 3, 3, 3, 3, 1),
    }
    for profile in six_triple_profiles:
        triple_indices = tuple(
            i for i, multiplicity in enumerate(profile) if multiplicity == 3
        )
        for chosen in combinations(triple_indices, 3):
            for partial in chosen:
                takes = {
                    i: (2 if i == partial else 3)
                    for i in chosen
                }
                assert sum(takes.values()) == h
                assert frontier.leaves_singleton(profile, takes)

    print("PASS: exact h=8,k=4 six-triple common-pole closure")
    print("fourth Bell role-drop coefficient is affine")
    print("third Boolean difference is 6 times three role-jet differences")
    print("six exact triples force three disjoint unequal fibre pairs")


if __name__ == "__main__":
    main()
