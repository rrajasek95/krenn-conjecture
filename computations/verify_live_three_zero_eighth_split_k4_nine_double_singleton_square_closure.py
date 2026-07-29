#!/usr/bin/env python3
"""Exact audit of the h=8,k=4 profile 3 2^9 1 closure."""

from itertools import combinations
from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import verify_live_three_zero_higher_split_collision_frontier as frontier


def main() -> None:
    h, k, p, total = 8, 4, 12, 22
    profile = (3,) + (2,) * 9 + (1,)
    assert sum(profile) == total == p + h + 2

    # All 1260 five-double/two-partial cores are legal.
    core_count = 0
    doubles = tuple(range(1, 10))
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
            assert complement.count(1) == 3  # two partial mates plus r
            core_count += 1
    assert core_count == sp.binomial(9, 5) * sp.binomial(5, 2) == 1260

    # The complement has four doubles, one triple, and one singleton.
    complement_multiplicities = (3,) + (2,) * 4 + (1,)
    assert sum(complement_multiplicities) == k + 8 == 12
    assert len(complement_multiplicities) == 6
    assert len(complement_multiplicities) - 4 == 2

    # Derive the complete derivative factor from g/A^2.  In particular,
    # the outside triple contributes exponent 2-2*3=-4, not -3 or -5.
    z, mu, triple, singleton = sp.symbols("z mu triple singleton")
    outside = sp.symbols("c0:4")
    selected = sp.symbols("t0:5")
    C_poly = sp.prod(z - value for value in outside)
    Q_poly = sp.prod(z + value for value in selected)
    A_poly = C_poly**2 * (z - triple) ** 3 * (z - singleton)
    gcd_factor = C_poly * (z - triple) ** 2
    derivative_factor = sp.cancel(gcd_factor / A_poly**2)
    expected_factor = sp.cancel(
        1 / (C_poly**3 * (z - triple) ** 4 * (z - singleton) ** 2)
    )
    assert sp.cancel(derivative_factor - expected_factor) == 0

    # After the singleton square cancels, this is the exact regular unit
    # above an outside-double triple pole.  Its two logarithmic jets give
    # the coefficients displayed in the note, including -4/(u-a).
    u = sp.symbols("u")
    other_outside = sp.symbols("v0:3")
    B = (
        (z + mu) ** 4
        * Q_poly**2
        / (
            sp.prod(z - value for value in other_outside) ** 3
            * (z - triple) ** 4
        )
    )
    expected_X = (
        4 / (z + mu)
        + 2 * sum(1 / (z + value) for value in selected)
        - 3 * sum(1 / (z - value) for value in other_outside)
        - 4 / (z - triple)
    )
    assert sp.cancel(sp.diff(B, z) / B - expected_X) == 0
    expected_X_prime = (
        -4 / (z + mu) ** 2
        - 2 * sum(1 / (z + value) ** 2 for value in selected)
        + 3 * sum(1 / (z - value) ** 2 for value in other_outside)
        + 4 / (z - triple) ** 2
    )
    assert sp.cancel(sp.diff(expected_X, z) - expected_X_prime) == 0

    # Singleton Robin row kills its square, including r=0.
    w, b0, b1 = sp.symbols("w b0 b1")
    local_unit = b0 + b1 * w
    assert sp.diff(local_unit * w**2, w).subs(w, 0) == 0

    # A unit over a triple pole has residue B''/2.
    a0, a1, a2, a3 = sp.symbols("a0 a1 a2 a3")
    local_B = a0 + a1 * w + a2 * w**2 + a3 * w**3
    assert sp.residue(local_B / w**3, w, 0) == a2
    assert sp.diff(local_B, w, 2).subs(w, 0) / 2 == a2

    x = sp.symbols("x")

    def phi(value):
        return 2 / (u + value) + 3 / (u - value)

    def psi(value):
        return -2 / (u + value) ** 2 - 3 / (u - value) ** 2

    assert sp.factor(phi(x) - (5 * u + x) / (u**2 - x**2)) == 0
    assert sp.factor(sp.diff(phi(x), u) - psi(x)) == 0

    # The exact mixed finite difference of X^2+X'.
    X0, Xp0, da, db, ea, eb = sp.symbols("X0 Xp0 da db ea eb")
    base = X0**2 + Xp0
    first = (X0 + da) ** 2 + Xp0 + ea
    second = (X0 + db) ** 2 + Xp0 + eb
    both = (X0 + da + db) ** 2 + Xp0 + ea + eb
    assert sp.expand(both - first - second + base) == 2 * da * db

    # Every ordered pair of disjoint swaps is realizable in a five-subset
    # of an eight-element universe.
    universe = set(range(8))
    realized = set()
    for subset_tuple in combinations(range(8), 5):
        subset = set(subset_tuple)
        outside = universe - subset
        for a, c in combinations(sorted(subset), 2):
            for b, d in combinations(sorted(outside), 2):
                realized.update(
                    ((a, b, c, d), (a, d, c, b), (c, b, a, d), (c, d, a, b))
                )
    for ordered in __import__("itertools").permutations(range(8), 4):
        assert ordered in realized

    # Exhaust equality patterns satisfying the rectangle law.  They have
    # a block of size at least seven.
    patterns = []

    def restricted_growth(prefix, maximum):
        if len(prefix) == 8:
            patterns.append(tuple(prefix))
            return
        for label in range(maximum + 2):
            prefix.append(label)
            restricted_growth(prefix, max(maximum, label))
            prefix.pop()

    restricted_growth([0], 0)
    valid_sizes = set()
    for pattern in patterns:
        valid = True
        for four in combinations(range(8), 4):
            a, b, c, d = four
            for pair1, pair2 in (
                ((a, b), (c, d)),
                ((a, c), (b, d)),
                ((a, d), (b, c)),
            ):
                if (
                    pattern[pair1[0]] != pattern[pair1[1]]
                    and pattern[pair2[0]] != pattern[pair2[1]]
                ):
                    valid = False
                    break
            if not valid:
                break
        if valid:
            sizes = tuple(
                sorted(
                    (pattern.count(label) for label in set(pattern)),
                    reverse=True,
                )
            )
            valid_sizes.add(sizes)
    assert valid_sizes == {(8,), (7, 1)}

    lam = sp.symbols("lam")
    fibre = sp.expand(lam * (u**2 - x**2) - 5 * u - x)
    assert sp.Poly(fibre, x).degree() <= 2
    assert sp.Poly(fibre, x).coeff_monomial(x) == -1

    counts, residuals = frontier.census(h, p)
    assert counts["R"] == 46
    assert profile in residuals

    print("PASS: exact h=8,k=4 profile 3 2^9 1 singleton-square closure")
    print("1260 formal-five cores and quadratic relation plane: exact")
    print("eight-value two-swap law forces a seven-point quadratic fibre")


if __name__ == "__main__":
    main()
