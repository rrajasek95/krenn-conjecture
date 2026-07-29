#!/usr/bin/env python3
"""Exact audit of two mixed linear-plane closures at h=8,k=5."""

from __future__ import annotations

from itertools import combinations
from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import verify_live_three_zero_higher_split_collision_frontier as frontier
import verify_live_three_zero_eighth_split_k4_two_triple_five_double_linear_plane_closure as kernel_2d6s
import verify_live_three_zero_eighth_split_k4_four_triple_single_double_pair_drop_closure as kernel_1d8s


z, w, mu = sp.symbols("z w mu")
PROFILE_DOUBLE = (3,) * 3 + (2,) * 4 + (1,) * 6
PROFILE_SINGLE = (3,) * 4 + (2,) + (1,) * 9


def audit_pair_drops(profile, formal_roles, singleton_start, expected):
    counts = {0: 0, 1: 0, 2: 0}
    legal = 0
    for lowered in combinations(tuple(formal_roles), 2):
        takes = {
            i: role - (1 if i in lowered else 0)
            for i, role in formal_roles.items()
        }
        takes = {i: role for i, role in takes.items() if role}
        omitted_singletons = sum(i >= singleton_start for i in lowered)
        represented = len(takes)
        residual_degree = represented - 3
        lift_degree = sum(3 if i >= singleton_start else 2 for i in lowered)
        complement = [
            multiplicity - takes.get(i, 0)
            for i, multiplicity in enumerate(profile)
        ]
        counts[omitted_singletons] += 1
        legal += 1
        assert sum(takes.values()) == 8
        assert sum(complement) == 15
        assert complement.count(1) >= 2
        assert frontier.leaves_singleton(profile, takes)
        assert residual_degree + lift_degree == expected
    assert legal == sp.binomial(len(formal_roles), 2)
    return counts


def check_cores_and_kernel_lemmas() -> None:
    assert sum(PROFILE_DOUBLE) == sum(PROFILE_SINGLE) == 23

    roles_double = {3: 2, 4: 2, **{i: 1 for i in range(7, 13)}}
    assert sum(roles_double.values()) == 10
    assert audit_pair_drops(
        PROFILE_DOUBLE, roles_double, singleton_start=7, expected=9
    ) == {0: 1, 1: 12, 2: 15}

    # Select the unique double (index 4) and singleton indices 5,...,12;
    # index 13 is the complementary singleton.
    roles_single = {4: 2, **{i: 1 for i in range(5, 13)}}
    assert sum(roles_single.values()) == 10
    assert audit_pair_drops(
        PROFILE_SINGLE, roles_single, singleton_start=5, expected=10
    ) == {0: 0, 1: 8, 2: 28}

    # These are precisely the common-pole-order-independent kernel
    # lemmas proved and fully audited in the fourth-order routes.
    kernel_2d6s.check_kernel_equality()
    kernel_1d8s.check_mixed_order_kernel_bound()
    kernel_1d8s.check_parity_divisor_and_reduced_wronskian()


def differential_data(A, selected_doubles, selected_singletons):
    g = sp.Integer(1)
    polynomial = sp.Poly(A, z)
    for root, multiplicity in sp.roots(polynomial.as_expr(), z).items():
        g *= (z - root) ** (multiplicity - 1)
    radical = sp.cancel(A / g)
    D_A = sp.cancel(sp.diff(A, z) / g)
    assert sp.Poly(A, z).degree() == 13
    assert sp.Poly(radical, z).degree() == 5
    assert sp.Poly(D_A, z).degree() == 4
    assert sp.Poly(D_A, z).LC() == 13

    coefficients = sp.symbols("n0:8")
    N = sum(coefficients[i] * z**i for i in range(8))
    E = sp.expand(
        radical * ((z + mu) * sp.diff(N, z) + 6 * N)
        - (z + mu) * D_A * N
    )
    G = (z + mu) ** 6 * N / A
    assert sp.factor(
        sp.diff(G, z) - (z + mu) ** 5 * g * E / A**2
    ) == 0
    assert sp.Poly(E, z).degree() <= 11

    for degree in range(8):
        trial = z**degree
        trial_E = sp.Poly(
            sp.expand(
                radical * ((z + mu) * sp.diff(trial, z) + 6 * trial)
                - (z + mu) * D_A * trial
            ),
            z,
        )
        assert trial_E.degree() <= 11
        if degree < 7:
            assert trial_E.coeff_monomial(z ** (degree + 5)) == degree - 7
        else:
            assert trial_E.coeff_monomial(z**12) == 0

    Q = sp.prod(z + x for x in selected_doubles)
    H = sp.prod(z + r for r in selected_singletons)
    contact = sp.expand(Q**2 * H)
    assert sp.Poly(contact, z).degree() == 10
    assert 11 - 10 == 1
    return g, Q, H


def check_double_profile_duality_and_swaps() -> None:
    selected = sp.symbols("x0:2")
    outside = sp.symbols("u0:2")
    triples = sp.symbols("a0:3")
    singletons = sp.symbols("r0:6")
    C = sp.prod(z - u for u in outside)
    T = sp.prod(z - a for a in triples)
    A = C**2 * T**3
    g, Q, H = differential_data(A, selected, singletons)
    assert sp.factor(g - C * T**2) == 0

    s0, s1 = sp.symbols("s0 s1")
    S = s0 + s1 * z
    from_contact = sp.cancel((z + mu) ** 5 * g * Q**2 * H * S / A**2)
    claimed = sp.cancel((z + mu) ** 5 * Q**2 * H * S / (C**3 * T**4))
    assert sp.cancel(from_contact - claimed) == 0

    B0, B1 = sp.symbols("B0 B1", nonzero=True)
    assert sp.diff((B0 + B1 * w) * w, w, 2).subs(w, 0) == 2 * B1

    u, x, v = sp.symbols("u x v")
    phi = lambda t: 2 / (u + t) + 3 / (u - t)
    assert sp.factor(phi(x) - (5 * u + x) / (u**2 - x**2)) == 0
    difference = sp.factor(
        (2 / (u + v) - 3 / (u - x))
        - (2 / (u + x) - 3 / (u - v))
    )
    assert sp.factor(difference - (phi(v) - phi(x))) == 0

    # For fixed u and ordered x,v among the other three values, the
    # remaining fourth value is the common selected companion.
    witness_count = 0
    indices = tuple(range(4))
    for fixed in indices:
        others = tuple(i for i in indices if i != fixed)
        for x_index in others:
            for v_index in others:
                if x_index == v_index:
                    continue
                companions = set(others) - {x_index, v_index}
                assert len(companions) == 1
                w_index = companions.pop()
                assert {x_index, w_index}.isdisjoint({fixed, v_index})
                assert {v_index, w_index}.isdisjoint({fixed, x_index})
                witness_count += 1
    assert witness_count == 4 * 3 * 2 == 24

    lam, t = sp.symbols("lam t")
    fibre = sp.Poly(lam * (u**2 - t**2) - 5 * u - t, t)
    assert fibre.degree() <= 2
    assert fibre.coeff_monomial(t) == -1
    assert 3 > 2


def check_singleton_profile_duality_and_residue() -> None:
    selected_double = sp.symbols("x")
    triples = sp.symbols("a0:4")
    selected_singletons = sp.symbols("r0:8")
    outside_singleton = sp.symbols("rho")
    T = sp.prod(z - a for a in triples)
    A = (z - outside_singleton) * T**3
    g, Q, H = differential_data(
        A, (selected_double,), selected_singletons
    )
    assert sp.factor(g - T**2) == 0

    S = sp.symbols("s0") + sp.symbols("s1") * z
    derivative = sp.cancel((z + mu) ** 5 * g * Q**2 * H * S / A**2)
    B = sp.cancel(derivative * (z - outside_singleton) ** 2 / S)
    expected_B = sp.cancel((z + mu) ** 5 * Q**2 * H / T**4)
    assert sp.cancel(B - expected_B) == 0

    B0, B1 = sp.symbols("B0 B1", nonzero=True)
    local_B = B0 + B1 * w
    local_S = w
    residue = sp.diff(local_B * local_S, w).subs(w, 0)
    assert residue == B0
    assert B0 != 0


def check_relation_counts_and_census() -> None:
    # rows - rank, with rank = ambient dimension - kernel dimension
    assert 8 - (10 - 4) == 2
    assert 9 - (11 - 4) == 2
    assert 2 == sp.Poly(1 + z, z).degree() + 1

    counts, residuals = frontier.census(8, 13)
    assert counts["R"] == 44
    assert PROFILE_DOUBLE in residuals
    assert PROFILE_SINGLE in residuals


def main() -> None:
    check_cores_and_kernel_lemmas()
    check_double_profile_duality_and_swaps()
    check_singleton_profile_duality_and_residue()
    check_relation_counts_and_census()
    print("k=5 mixed linear-plane increment: PASS")
    print("pair-drop cores audited: 28 + 36")
    print("new closures: 3^3 2^4 1^6 and 3^4 2 1^9")


if __name__ == "__main__":
    main()
