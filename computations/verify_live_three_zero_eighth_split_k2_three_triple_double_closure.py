#!/usr/bin/env python3
"""Exact audit of the k=2 three-triple/two-double closure."""

from __future__ import annotations

from itertools import combinations
from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import verify_live_three_zero_higher_split_collision_frontier as frontier
import verify_live_three_zero_eighth_split_k2_post_role_census as previous


w, x, y, mu = sp.symbols("w x y mu")
X, Y = sp.symbols("X Y")
TOTAL = 20


def normalized_role(count: int, value: sp.Expr) -> sp.Expr:
    return (
        (1 - w / (value + mu)) ** (-count)
        * (1 + w / (value - mu)) ** (-(count + 1))
    )


def log_jets(count: int, value: sp.Expr):
    role = normalized_role(count, value)
    first = sp.factor(sp.diff(role, w).subs(w, 0))
    second = sp.factor(sp.diff(role, w, 2).subs(w, 0) - first**2)
    return first, second


def scaled_phi(count: int, value: sp.Expr):
    return sp.factor(count / (value + 1) - (count + 1) / (value - 1))


def scaled_psi(count: int, value: sp.Expr):
    return sp.factor(count / (value + 1) ** 2 + (count + 1) / (value - 1) ** 2)


PROFILES = (
    (3, 3, 3, 2, 2, 2, 1, 1, 1, 1, 1),
    (3, 3, 3, 2, 2, 1, 1, 1, 1, 1, 1, 1),
)


EXPECTED_FINAL = (
    (2, 2, 2, 2, 2, 2, 2, 2, 2, 2),
    (3, 2, 2, 2, 2, 2, 2, 2, 2, 1),
    (2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1),
    (3, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1),
)


def check_core_legality_and_degrees():
    h, p, k = 8, 10, 2
    for profile in PROFILES:
        assert sum(profile) == 20
        triples = [index for index, part in enumerate(profile) if part == 3]
        doubles = [index for index, part in enumerate(profile) if part == 2]
        singletons = [index for index, part in enumerate(profile) if part == 1]
        assert len(triples) == 3
        assert len(doubles) >= 2
        assert len(singletons) >= 1

        # The three triple-only (3,3,2) permutations.
        for partial in triples:
            takes = {
                index: (2 if index == partial else 3) for index in triples
            }
            assert sum(takes.values()) == h
            assert profile[partial] - takes[partial] == 1
            assert frontier.leaves_singleton(profile, takes)
            _check_constant_residual_degree(profile, takes, p, k)

        # For every double and every omitted triple, use the other two
        # triples fully and the double fully.  Untouched singleton guards
        # make every one of these cores legal.
        mixed_count = 0
        for double in doubles:
            for omitted in triples:
                takes = {double: 2}
                takes.update(
                    {triple: 3 for triple in triples if triple != omitted}
                )
                mixed_count += 1
                assert sum(takes.values()) == h
                assert all(index not in takes for index in singletons)
                assert frontier.leaves_singleton(profile, takes)
                _check_constant_residual_degree(profile, takes, p, k)
        assert mixed_count == 3 * len(doubles)


def _check_constant_residual_degree(profile, takes, p, k):
    complement_size = sum(
        multiplicity - takes.get(index, 0)
        for index, multiplicity in enumerate(profile)
    )
    represented_classes = len(takes)
    denominator_degree = (k + 1) + sum(take + 1 for take in takes.values())
    numerator_cap = p + represented_classes - 1
    residual_cap = numerator_cap - complement_size
    assert represented_classes == 3
    assert complement_size == p + 2 == 12
    assert denominator_degree == 14
    assert numerator_cap == 12
    assert residual_cap == 0


def check_common_background_and_residue_formula():
    z, value = sp.symbols("z value")
    for multiplicity in (1, 2, 3):
        for count in range(multiplicity + 1):
            direct = (z - value) ** (multiplicity - count) / (
                z + value
            ) ** (count + 1 if count else 0)
            if count == 0:
                # An unselected class has no selected-class pole factor.
                baseline = (z - value) ** multiplicity
                assert sp.factor(direct - baseline) == 0
            else:
                baseline = (z - value) ** multiplicity
                raw_role = 1 / (
                    (z - value) ** count * (z + value) ** (count + 1)
                )
                assert sp.factor(direct - baseline * raw_role) == 0

    alpha, beta = sp.symbols("alpha beta")
    background = 1 + alpha * w + (alpha**2 + beta) * w**2 / 2
    values = sp.symbols("v0:3")
    counts = (3, 3, 2)
    regular = background * sp.prod(
        normalized_role(count, value)
        for count, value in zip(counts, values)
    )
    observed = sp.factor(sp.diff(regular, w, 2).subs(w, 0))
    first = sum(log_jets(count, value)[0] for count, value in zip(counts, values))
    second = sum(log_jets(count, value)[1] for count, value in zip(counts, values))
    expected = (alpha + first) ** 2 + beta + second
    assert sp.factor(observed - expected) == 0


def check_triple_totals():
    value, other = sp.symbols("value other")
    phi2, psi2 = log_jets(2, value)
    phi3, psi3 = log_jets(3, value)
    d = sp.factor(phi3 - phi2)
    delta = sp.factor(psi3 - psi2)
    assert sp.factor(d + 2 * mu / (value**2 - mu**2)) == 0
    assert sp.factor(delta - (d**2 - d / mu)) == 0

    d_other = sp.factor(log_jets(3, other)[0] - log_jets(2, other)[0])
    difference = sp.factor(d - d_other)
    expected_difference = sp.factor(
        2
        * mu
        * (value - other)
        * (value + other)
        / ((value**2 - mu**2) * (other**2 - mu**2))
    )
    assert sp.factor(difference - expected_difference) == 0

    T, W, formal_d = sp.symbols("T W formal_d")
    equation = T**2 + W + (1 / mu - 2 * T) * formal_d
    forced_T = sp.Rational(1, 2) / mu
    assert sp.factor((1 / mu - 2 * T).subs(T, forced_T)) == 0
    assert sp.factor(equation.subs(T, forced_T) - (W + 1 / (4 * mu**2))) == 0


def check_mixed_factorization_and_matrix():
    delta_phi = sp.factor(scaled_phi(2, Y) - scaled_phi(3, X))
    scaled_equation = sp.factor(
        delta_phi**2
        + delta_phi
        + scaled_psi(2, Y)
        - scaled_psi(3, X)
    )
    numerator, denominator = sp.fraction(scaled_equation)
    assert sp.factor(denominator - (X**2 - 1) ** 2 * (Y**2 - 1) ** 2) == 0
    assert sp.rem(sp.Poly(numerator, X), sp.Poly(X - Y, X)) == 0
    quotient = sp.factor(numerator / (X - Y))
    assert sp.Poly(quotient, X).degree() <= 3

    expected_coefficients = (
        -(5 * Y - 1) * (7 * Y**2 + 4 * Y + 1),
        -11 * Y**3 - 37 * Y**2 - Y + 1,
        -Y**3 + Y**2 + 37 * Y + 11,
        -(Y - 5) * (Y**2 + 4 * Y + 7),
    )
    observed_coefficients = tuple(
        sp.factor(sp.Poly(quotient, X).coeff_monomial(X**degree))
        for degree in range(4)
    )
    assert all(
        sp.factor(observed - expected) == 0
        for observed, expected in zip(observed_coefficients, expected_coefficients)
    )

    matrix = sp.Matrix(
        [
            [
                sp.Poly(coefficient, Y).coeff_monomial(Y**degree)
                for degree in range(4)
            ]
            for coefficient in expected_coefficients
        ]
    )
    assert matrix == sp.Matrix(
        [
            [1, -1, -13, -35],
            [1, -1, -37, -11],
            [11, 37, 1, -1],
            [35, 13, 1, -1],
        ]
    )
    assert matrix.det() == 1327104

    # Applying M^{-1} to proportional coefficient vectors recovers
    # proportional twisted-cubic points.  Their first coordinate fixes
    # the scale and their second coordinate fixes Y.
    Y1, Y2, scale = sp.symbols("Y1 Y2 scale")
    twisted_1 = sp.Matrix([1, Y1, Y1**2, Y1**3])
    twisted_2 = sp.Matrix([1, Y2, Y2**2, Y2**3])
    recovered = sp.simplify(matrix.inv() * (matrix * twisted_1 - scale * matrix * twisted_2))
    assert recovered == twisted_1 - scale * twisted_2
    assert recovered[0] == 1 - scale
    assert sp.factor(recovered[1].subs(scale, 1) - (Y1 - Y2)) == 0


def check_updated_frontier():
    previous_set = set(previous.EXPECTED_FINAL)
    closed = set(PROFILES)
    assert closed <= previous_set
    final = previous_set - closed
    ordered = tuple(sorted(final, key=lambda item: (len(item), TOTAL - len(item), item)))
    assert ordered == EXPECTED_FINAL
    assert len(ordered) == 4
    assert ordered[0] == (2,) * 10
    assert sum((263, 270, 22, 14, 12, 3, 5, 18, 3, 8, 2, 2, 4, 1)) == 627


def main():
    check_core_legality_and_degrees()
    check_common_background_and_residue_formula()
    check_triple_totals()
    check_mixed_factorization_and_matrix()
    check_updated_frontier()
    print("k=2 three-triple/two-double closure: PASS")
    print("triple totals T3=1/(2mu), W3=-1/(4mu^2): exact")
    print("mixed equation cubic coefficient determinant: 1327104")
    print("twisted-cubic double-role map is projectively injective")
    print("h=8,k=2 frontier: 6 -> 4; next profile (2^10)")


if __name__ == "__main__":
    main()
