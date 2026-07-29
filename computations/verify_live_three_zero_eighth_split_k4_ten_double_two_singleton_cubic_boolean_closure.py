#!/usr/bin/env python3
"""Exact audit of the h=8,k=4 profile 2^10 1^2 closure."""

from itertools import combinations, product
from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import verify_live_three_zero_higher_split_collision_frontier as frontier


def restricted_growth_partitions(size, max_block_size):
    patterns = []

    def extend(prefix, maximum):
        if len(prefix) == size:
            patterns.append(tuple(prefix))
            return
        for label in range(maximum + 2):
            candidate = prefix + [label]
            if candidate.count(label) <= max_block_size:
                extend(candidate, max(maximum, label))

    extend([0], 0)
    return patterns


def main() -> None:
    h, k, p, total = 8, 4, 12, 22
    profile = (2,) * 10 + (1,) * 2
    assert sum(profile) == total == p + h + 2

    # Every formal-five pair-drop core is legal, for every five-set.
    core_count = 0
    doubles = tuple(range(10))
    for chosen_tuple in combinations(doubles, 5):
        chosen = set(chosen_tuple)
        for partial_tuple in combinations(chosen_tuple, 2):
            partial = set(partial_tuple)
            takes = {i: (1 if i in partial else 2) for i in chosen}
            complement = tuple(
                multiplicity - takes.get(i, 0)
                for i, multiplicity in enumerate(profile)
            )
            assert sum(takes.values()) == h
            assert sum(complement) == p + 2 == 14
            assert frontier.leaves_singleton(profile, takes)
            assert complement.count(1) == 4  # two mates and two original singletons
            core_count += 1
    assert core_count == sp.binomial(10, 5) * sp.binomial(5, 2) == 2520

    # After the formal labels are fully removed, A has five double roots
    # and two simple roots; hence S_T is a plane in the cubics.
    complement_multiplicities = (2,) * 5 + (1,) * 2
    assert sum(complement_multiplicities) == k + 8
    assert len(complement_multiplicities) == 7
    assert len(complement_multiplicities) - 4 == 3

    z, mu, r, s = sp.symbols("z mu r s")
    outside = sp.symbols("c0:5")
    selected = sp.symbols("t0:5")
    C_poly = sp.prod(z - value for value in outside)
    Q_poly = sp.prod(z + value for value in selected)
    A_poly = C_poly**2 * (z - r) * (z - s)
    gcd_factor = C_poly
    derivative_factor = sp.cancel(gcd_factor / A_poly**2)
    expected_factor = sp.cancel(1 / (C_poly**3 * (z - r) ** 2 * (z - s) ** 2))
    assert sp.cancel(derivative_factor - expected_factor) == 0

    # Cubic Hermite interpolation at r,s is an isomorphism.  Thus two
    # nonzero first-jet rows supported at the distinct nodes are independent.
    coeffs = sp.symbols("a0:4")
    cubic = sum(coeffs[i] * z**i for i in range(4))
    hermite = sp.Matrix(
        [
            [sp.diff(expr, coefficient) for coefficient in coeffs]
            for expr in (
                cubic.subs(z, r),
                sp.diff(cubic, z).subs(z, r),
                cubic.subs(z, s),
                sp.diff(cubic, z).subs(z, s),
            )
        ]
    )
    assert sp.factor(hermite.det()) in ((r - s) ** 4, -(r - s) ** 4)

    # Division-free cancellation of r and exact killing of the s residue.
    w, f0, f1, f2, H = sp.symbols("w f0 f1 f2 H")
    local_F = f0 + f1 * w + f2 * w**2
    local_L = 1 - H * w
    singleton_residue = sp.diff(local_F * local_L, w).subs(w, 0)
    assert sp.expand(singleton_residue.subs(H, f1 / f0)) == 0
    assert sp.diff(w**2 * local_L, w).subs(w, 0) == 0

    # The outside order-three residue is exactly equation (13).
    b0, b1, b2, d = sp.symbols("b0 b1 b2 d", nonzero=True)
    local_B = b0 + b1 * w + b2 * w**2
    shifted_L = 1 - H * (d + w)
    raw_second = sp.diff(local_B * shifted_L, w, 2).subs(w, 0) / b0
    X = b1 / b0
    Xprime = 2 * b2 / b0 - X**2
    expected_second = (1 - d * H) * (X**2 + Xprime) - 2 * H * X
    assert sp.cancel(raw_second - expected_second) == 0

    u, x = sp.symbols("u x")

    def phi(v, value):
        return 2 / (v + value) + 3 / (v - value)

    def psi(v, value):
        return -2 / (v + value) ** 2 - 3 / (v - value) ** 2

    assert sp.factor(phi(u, x) - (5 * u + x) / (u**2 - x**2)) == 0
    assert sp.factor(sp.diff(phi(u, x), u) - psi(u, x)) == 0

    # Audit the complete third Boolean difference.  The affine X' increments
    # are included; all of them cancel, as do every term below degree three.
    H0, X0, Y0 = sp.symbols("H0 X0 Y0")
    alphas = sp.symbols("alpha0:3")
    betas = sp.symbols("beta0:3")
    gammas = sp.symbols("gamma0:3")
    alternating = 0
    for bits in product((0, 1), repeat=3):
        h_value = H0 + sum(bits[i] * alphas[i] for i in range(3))
        x_value = X0 + sum(bits[i] * betas[i] for i in range(3))
        y_value = Y0 + sum(bits[i] * gammas[i] for i in range(3))
        equation = (
            (1 - d * h_value) * (x_value**2 + y_value)
            - 2 * h_value * x_value
        )
        sign = (-1) ** (3 - sum(bits))
        alternating += sign * equation
    expected_alternating = -2 * d * (
        alphas[0] * betas[1] * betas[2]
        + alphas[1] * betas[0] * betas[2]
        + alphas[2] * betas[0] * betas[1]
    )
    assert sp.expand(alternating - expected_alternating) == 0

    # Every matching of three pairs in a nine-set gives a valid cube of
    # five-subsets: choose one endpoint per pair plus any two of three fillers.
    universe = set(range(9))
    cube_count = 0
    for six_tuple in combinations(range(9), 6):
        six = set(six_tuple)
        first = min(six)
        rest = sorted(six - {first})
        # Pairings are generated uniquely by pairing the smallest remaining
        # vertex recursively.
        pairings = []

        def generate_pairs(remaining, current):
            if not remaining:
                pairings.append(tuple(current))
                return
            a = min(remaining)
            for b in sorted(remaining - {a}):
                generate_pairs(remaining - {a, b}, current + [(a, b)])

        generate_pairs(six, [])
        assert len(pairings) == 15
        fillers = sorted(universe - six)
        for pairing in pairings:
            base_fillers = set(fillers[:2])
            cube = set()
            for bits in product((0, 1), repeat=3):
                subset = base_fillers | {
                    pairing[i][bits[i]] for i in range(3)
                }
                assert len(subset) == 5
                cube.add(tuple(sorted(subset)))
            assert len(cube) == 8
            cube_count += 1
    assert cube_count == sp.binomial(9, 6) * 15 == 1260

    # Exact finite audit of the secant-line selection lemma.  A quadratic
    # fibre pattern is any partition into blocks of size at most two.  In
    # each pattern one can reserve two nonvertical pairs so that the five
    # remaining vertices still occupy at least three fibres.  Their graph of
    # nonvertical comparisons is connected, which is exactly the algebraic
    # assertion that one common secant slope puts all five on one line.
    patterns = restricted_growth_partitions(9, 2)
    assert len(patterns) == 2620
    for pattern in patterns:
        labels = set(pattern)
        assert len(labels) >= 5
        witness = None
        for four in combinations(range(9), 4):
            a, b, c, e = four
            for pairs in (
                ((a, b), (c, e)),
                ((a, c), (b, e)),
                ((a, e), (b, c)),
            ):
                if any(pattern[i] == pattern[j] for i, j in pairs):
                    continue
                remaining = sorted(universe - set(four))
                if len({pattern[i] for i in remaining}) < 3:
                    continue
                witness = (pairs, remaining)
                break
            if witness is not None:
                break
        assert witness is not None
        _, remaining = witness
        adjacency = {
            i: {j for j in remaining if pattern[j] != pattern[i]}
            for i in remaining
        }
        reached = {remaining[0]}
        while True:
            expanded = reached | set().union(*(adjacency[i] for i in reached))
            if expanded == reached:
                break
            reached = expanded
        assert reached == set(remaining)

    # A Phi_u fibre is a nonzero quadratic at worst.
    lam = sp.symbols("lam")
    fibre = sp.expand(lam * (u**2 - x**2) - 5 * u - x)
    assert sp.Poly(fibre, x).degree() <= 2
    assert sp.Poly(fibre, x).coeff_monomial(x) == -1

    # A line in (Phi_u,Phi_s) pulls back to a nonzero quartic at worst.
    K, L = sp.symbols("K L")
    pullback = sp.expand(
        (5 * s + x) * (u**2 - x**2)
        - K * (5 * u + x) * (s**2 - x**2)
        - L * (s**2 - x**2) * (u**2 - x**2)
    )
    poly = sp.Poly(pullback, x)
    assert poly.degree() <= 4
    assert poly.coeff_monomial(x**4) == -L
    after_L = sp.Poly(pullback.subs(L, 0), x)
    assert after_L.coeff_monomial(x**3) == K - 1
    after_LK = sp.Poly(pullback.subs({L: 0, K: 1}), x)
    assert after_LK.coeff_monomial(x**2) == 5 * (u - s)

    counts, residuals = frontier.census(h, p)
    assert counts["R"] == 46
    assert profile in residuals

    print("PASS: exact h=8,k=4 profile 2^10 1^2 cubic-Boolean closure")
    print("2520 legal formal-five cores and cubic relation pencil: exact")
    print("1260 three-swap cubes force a five-point nonzero quartic fibre")


if __name__ == "__main__":
    main()
