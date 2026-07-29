#!/usr/bin/env python3
"""Exact audit for the h=8, k=3 seven-triple common-pole closure."""

from itertools import combinations
from math import comb
from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import verify_live_three_zero_higher_split_collision_frontier as frontier


def main():
    x, y, mu, w = sp.symbols("x y mu w", nonzero=True)

    def rho(r, value):
        return (1 - w / (value + mu)) ** (-r) * (
            1 + w / (value - mu)
        ) ** (-(r + 1))

    def log_jet(r, value, order):
        return sp.factor(sp.diff(sp.log(rho(r, value)), w, order).subs(w, 0))

    phi3 = log_jet(3, x, 1)
    psi3 = log_jet(3, x, 2)
    chi3 = log_jet(3, x, 3)
    d = sp.factor(phi3 - log_jet(2, x, 1))
    d2 = sp.factor(psi3 - log_jet(2, x, 2))
    d3 = sp.factor(chi3 - log_jet(2, x, 3))

    assert sp.factor(phi3 + (x + 7 * mu) / (x**2 - mu**2)) == 0
    assert sp.factor(d + 2 * mu / (x**2 - mu**2)) == 0
    assert sp.factor(d2 - (d**2 - d / mu)) == 0
    assert sp.factor(d3 - (2 * d**3 - 3 * d**2 / mu)) == 0

    dy = d.xreplace({x: y})
    expected_difference = (
        2 * mu * (x - y) * (x + y)
        / ((x**2 - mu**2) * (y**2 - mu**2))
    )
    assert sp.factor(d - dy - expected_difference) == 0

    T, V, W, D = sp.symbols("T V W D")
    cubic = (
        (T - D) ** 3
        + 3 * (T - D) * (V - D**2 + D / mu)
        + W
        - 2 * D**3
        + 3 * D**2 / mu
    )
    affine = T**3 + 3 * T * V + W + 3 * D * (-T**2 + T / mu - V)
    assert sp.expand(cubic - affine) == 0
    solved_v = T / mu - T**2
    solved_w = 2 * T**3 - 3 * T**2 / mu
    assert sp.factor((-T**2 + T / mu - V).subs(V, solved_v)) == 0
    assert sp.factor((T**3 + 3 * T * V + W).subs({V: solved_v, W: solved_w})) == 0

    alpha, beta = sp.symbols("alpha beta")
    Ai, Aj, Ak, Al = sp.symbols("Ai Aj Ak Al")
    Bi, Bj, Bk, Bl = sp.symbols("Bi Bj Bk Bl")

    def overlap(Az, Bz):
        total = alpha + Ai + Aj + Az
        return beta + Bi + Bj + Bz - (total / mu - total**2)

    overlap_difference = sp.factor(overlap(Ak, Bk) - overlap(Al, Bl))
    claimed = (Bk - Bl) - (Ak - Al) * (
        1 / mu - 2 * alpha - 2 * Ai - 2 * Aj - Ak - Al
    )
    assert sp.factor(overlap_difference - claimed) == 0

    lam = sp.symbols("lam")
    fibre = sp.factor(lam * (x**2 - mu**2) + x + 7 * mu)
    assert sp.Poly(fibre, x).degree() <= 2
    assert sp.Poly(fibre, x).coeff_monomial(x) == 1

    h, k = 8, 3
    counts, residual = frontier.census(h, h + k)
    assert counts["R"] == 46
    assert residual[0] == (4, 4, 4, 3, 3, 3)
    assert residual[1] == (3,) * 7

    five_triple_profiles = (
        (3,) * 7,
        (3,) * 5 + (2,) * 3,
        (3,) * 6 + (2, 1),
        (3,) * 5 + (2, 2, 1, 1),
        (3,) * 5 + (2,) + (1,) * 4,
        (3,) * 5 + (1,) * 6,
    )
    for profile in five_triple_profiles:
        assert profile in residual
        triple_indices = tuple(i for i, multiplicity in enumerate(profile) if multiplicity == 3)
        assert len(triple_indices) >= 5
        legal_count = 0
        for chosen in combinations(triple_indices, 3):
            for partial in chosen:
                takes = [0] * len(profile)
                for idx in chosen:
                    takes[idx] = 2 if idx == partial else 3
                assert sum(takes) == h
                assert sum(t > 0 for t in takes) == 3
                complement = [profile[i] - takes[i] for i in range(len(profile))]
                assert complement.count(1) >= 1
                assert sum(complement) == sum(profile) - h == 13
                legal_count += 1
        assert legal_count == comb(len(triple_indices), 3) * 3

    print("PASS: exact h=8,k=3 seven-triple common-pole closure audit")


if __name__ == "__main__":
    main()
