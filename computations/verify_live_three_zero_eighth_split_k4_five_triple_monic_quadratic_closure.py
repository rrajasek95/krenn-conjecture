#!/usr/bin/env python3
"""Exact audit of the h=8,k=4 five-exact-triple closure."""

from __future__ import annotations

from itertools import combinations
from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import verify_live_three_zero_higher_split_collision_frontier as frontier
import verify_live_three_zero_eighth_split_k4_updated_census as census


def restricted_growth_strings(length: int):
    """Set partitions whose blocks all have size at most two."""

    def recur(word: tuple[int, ...]):
        if len(word) == length:
            yield word
            return
        for value in range(max(word) + 2):
            if word.count(value) == 2:
                continue
            yield from recur(word + (value,))

    if length == 0:
        yield ()
    else:
        yield from recur((0,))


def check_fourth_bell_affinity() -> None:
    mu = sp.symbols("mu", nonzero=True)
    T, V, W, X, D = sp.symbols("T V W X D")

    def bell4(t, v, third, fourth):
        return t**4 + 6 * t**2 * v + 3 * v**2 + 4 * t * third + fourth

    delta_jets = (
        D,
        D**2 - D / mu,
        2 * D**3 - 3 * D**2 / mu,
        6 * D**4 - 12 * D**3 / mu + 3 * D**2 / mu**2,
    )
    dropped = sp.expand(
        bell4(
            T - delta_jets[0],
            V - delta_jets[1],
            W - delta_jets[2],
            X - delta_jets[3],
        )
    )
    slope = -4 * T**3 + 6 * T**2 / mu - 12 * T * V + 6 * V / mu - 4 * W
    assert sp.expand(dropped - bell4(T, V, W, X) - D * slope) == 0
    assert sp.Poly(dropped, D).degree() == 1

    solved_third = -T**3 + 3 * T**2 / (2 * mu) - 3 * T * V + 3 * V / (2 * mu)
    assert sp.factor(slope.subs(W, solved_third)) == 0


def check_rectangle_identity() -> None:
    mu = sp.symbols("mu", nonzero=True)
    alpha, beta, gamma = sp.symbols("alpha beta gamma")
    As = sp.symbols("A0:5")
    Bs = sp.symbols("B0:5")
    Cs = sp.symbols("C0:5")

    def identity(indices):
        t = alpha + sum(As[index] for index in indices)
        v = beta + sum(Bs[index] for index in indices)
        third = gamma + sum(Cs[index] for index in indices)
        return third + t**3 - 3 * t**2 / (2 * mu) + 3 * t * v - 3 * v / (2 * mu)

    # Indices are e,a,b,c,d = 0,1,2,3,4.
    alternating = sp.expand(
        identity((0, 1, 3))
        - identity((0, 1, 4))
        - identity((0, 2, 3))
        + identity((0, 2, 4))
    )
    delta1 = As[1] - As[2]
    delta2 = As[3] - As[4]
    eta1 = Bs[1] - Bs[2]
    eta2 = Bs[3] - Bs[4]
    t0 = alpha + As[0] + As[2] + As[4]
    rectangle = delta1 * delta2 * (
        2 * t0 + delta1 + delta2 - 1 / mu
    ) + delta1 * eta2 + delta2 * eta1
    assert sp.expand(alternating - 3 * rectangle) == 0

    divided = sp.factor(rectangle / (delta1 * delta2))
    total_a = sum(As)
    constant = 1 / mu - 2 * alpha - total_a
    collected = eta1 / delta1 + eta2 / delta2 + As[0] - constant
    assert sp.factor(divided - collected) == 0

    # If the first A-secant is vertical and the second is not, the
    # undivided rectangle is exactly delta2*eta1.
    assert sp.factor(rectangle.subs(As[1], As[2]) - delta2 * eta1) == 0


def check_five_point_secant_lemma() -> None:
    # There are only three possible fibre-multiplicity types.  Merely
    # computing the generic rank of their secant systems would not exclude
    # a rank drop at a special configuration of distinct A-coordinates, so
    # the checks below follow the division-free proof in each type.
    patterns = tuple(restricted_growth_strings(5))
    assert len(patterns) == 26
    assert {
        tuple(
            sorted(
                (
                    pattern.count(block)
                    for block in range(max(pattern) + 1)
                ),
                reverse=True,
            )
        )
        for pattern in patterns
    } == {
        (1, 1, 1, 1, 1),
        (2, 1, 1, 1),
        (2, 2, 1),
    }

    k0 = sp.symbols("k0")

    # Type (1,1,1,1,1).  For a triple i,j,l, keep the complementary
    # edge fixed in the three rectangles.  Pairwise subtraction says that
    # its three internal slopes agree.  Applying this to 012, 013, and 014
    # puts all five points on the line through points 0 and 1.
    avals = sp.symbols("a0:5")
    cvals = sp.symbols("c0:5")

    def slope(i, j):
        return (cvals[i] - cvals[j]) / (avals[i] - avals[j])

    def rectangle(pair1, pair2):
        return slope(*pair1) + slope(*pair2) - k0

    q = slope(0, 1)
    for index, outside_pair in ((2, (3, 4)), (3, (2, 4)), (4, (2, 3))):
        through_index = rectangle((0, index), outside_pair)
        through_one = rectangle((0, 1), outside_pair)
        assert sp.factor(through_index - through_one - (slope(0, index) - q)) == 0
        r = cvals[0] - q * avals[0]
        line_residual = cvals[index] - q * avals[index] - r
        assert sp.factor(
            line_residual - (avals[index] - avals[0]) * (slope(index, 0) - q)
        ) == 0

    # Type (2,1,1,1).  Points 0,1 have common coordinates (X,CX), and
    # points 2,3,4 have coordinates Y,Z,W.  The three displayed
    # rectangles are exactly those obtained by fixing Y,Z,W in turn.
    x, y, z, w = sp.symbols("x y z w")
    cx, cy, cz, cw = sp.symbols("cx cy cz cw")
    sxy = (cx - cy) / (x - y)
    sxz = (cx - cz) / (x - z)
    sxw = (cx - cw) / (x - w)
    fix_y = sxz + sxw - k0
    fix_z = sxy + sxw - k0
    fix_w = sxy + sxz - k0
    assert sp.factor((fix_z + fix_w - fix_y) / 2 - (sxy - k0 / 2)) == 0
    assert sp.factor((fix_y + fix_w - fix_z) / 2 - (sxz - k0 / 2)) == 0
    assert sp.factor((fix_y + fix_z - fix_w) / 2 - (sxw - k0 / 2)) == 0

    # Type (2,2,1).  Points 0,1 lie over X, points 2,3 over Y, and point
    # 4 over Z.  Fixing Z gives twice the X--Y slope; fixing one copy of
    # X and then one copy of Y gives the other two slopes.
    x, y, z = sp.symbols("x y z")
    cx, cy, cz = sp.symbols("cx cy cz")
    sxy = (cx - cy) / (x - y)
    syz = (cy - cz) / (y - z)
    sxz = (cx - cz) / (x - z)
    fix_z = 2 * sxy - k0
    fix_x = sxy + syz - k0
    fix_y = sxy + sxz - k0
    assert sp.factor(fix_z / 2 - (sxy - k0 / 2)) == 0
    assert sp.factor(fix_x - fix_z / 2 - (syz - k0 / 2)) == 0
    assert sp.factor(fix_y - fix_z / 2 - (sxz - k0 / 2)) == 0


def check_exact_jets_and_quartic_pullback() -> None:
    x, mu, w = sp.symbols("x mu w", nonzero=True)

    rho3 = (1 - w / (x + mu)) ** -3 * (1 + w / (x - mu)) ** -4
    first = sp.factor(sp.diff(sp.log(rho3), w).subs(w, 0))
    second = sp.factor(sp.diff(sp.log(rho3), w, 2).subs(w, 0))
    expected_first = -(x + 7 * mu) / (x**2 - mu**2)
    expected_second = 3 / (x + mu) ** 2 + 4 / (x - mu) ** 2
    assert sp.factor(first - expected_first) == 0
    assert sp.factor(second - expected_second) == 0

    lam = sp.symbols("lam")
    fibre = sp.Poly(lam * (x**2 - mu**2) + x + 7 * mu, x)
    assert fibre.degree() <= 2
    assert fibre.coeff_monomial(x) == 1

    q, r = sp.symbols("q r")
    pullback = sp.expand(
        3 * (x - mu) ** 2
        + 4 * (x + mu) ** 2
        - (x + 7 * mu) ** 2
        + q * (x + 7 * mu) * (x**2 - mu**2)
        - r * (x**2 - mu**2) ** 2
    )
    polynomial = sp.Poly(pullback, x)
    assert polynomial.degree() <= 4
    assert polynomial.coeff_monomial(x**4) == -r
    assert sp.Poly(pullback.subs(r, 0), x).coeff_monomial(x**3) == q
    residual = sp.expand(pullback.subs({r: 0, q: 0}))
    assert residual == 6 * x**2 - 12 * mu * x - 42 * mu**2
    assert residual != 0


def check_legal_cores_and_census_increment() -> None:
    h, p = 8, 12
    counts, residual_tuple = frontier.census(h, p)
    assert counts["R"] == 46
    residuals = set(residual_tuple)
    five_or_more = {
        profile for profile in residuals if profile.count(3) >= 5
    }
    assert five_or_more == {
        (4,) + (3,) * 6,
        (3,) * 7 + (1,),
        (3,) * 5 + (2,) * 3 + (1,),
        (3,) * 5 + (2,) * 2 + (1,) * 3,
        (3,) * 5 + (2,) + (1,) * 5,
        (3,) * 5 + (1,) * 7,
    }

    core_count = 0
    for profile in five_or_more:
        triples = tuple(
            index
            for index, multiplicity in enumerate(profile)
            if multiplicity == 3
        )
        for chosen in combinations(triples, 3):
            for partial in chosen:
                takes = {
                    index: (2 if index == partial else 3)
                    for index in chosen
                }
                assert sum(takes.values()) == h
                assert frontier.leaves_singleton(profile, takes)
                core_count += 1
    assert core_count == 285

    expected_increment = {
        (3,) * 5 + (2,) + (1,) * 5,
        (3,) * 5 + (1,) * 7,
    }
    assert census.EXPECTED_FIVE_TRIPLE_MONIC_QUADRATIC == expected_increment
    post_route_residuals = set(census.EXPECTED_RESIDUALS)
    assert not post_route_residuals & expected_increment
    pre_route_residuals = post_route_residuals | expected_increment
    sequential_increment = {
        profile for profile in pre_route_residuals if profile.count(3) >= 5
    }
    assert sequential_increment == expected_increment


def main() -> None:
    check_fourth_bell_affinity()
    check_rectangle_identity()
    check_five_point_secant_lemma()
    check_exact_jets_and_quartic_pullback()
    check_legal_cores_and_census_increment()
    print("PASS: exact h=8,k=4 five-triple monic-quadratic closure")
    print("fourth Bell role drop is affine and yields the triple identity")
    print("all three degree-two fibre types force C affine in A")
    print("the exact jet pullback is a nonzero quartic")
    print("sequential census increment: 2 profiles")


if __name__ == "__main__":
    main()
