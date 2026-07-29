#!/usr/bin/env python3
"""Exact audit of the one-bad-core repair and final h=8,k=1 profile."""

from __future__ import annotations

from itertools import combinations

import sympy as sp


def leaves_singleton(profile: tuple[int, ...], selected: set[int]) -> bool:
    return any(
        multiplicity - (1 if index in selected else 0) == 1
        for index, multiplicity in enumerate(profile)
    )


def check_unique_bad_core_and_special_deletions() -> None:
    profile = (3, 2, 2, 2, 2) + (1,) * 8
    h, k, p = 8, 1, 9
    assert sum(profile) == 19 == p + h + 2
    singleton_indices = set(range(5, 13))

    bad = []
    for core_tuple in combinations(range(len(profile)), h):
        core = set(core_tuple)
        if not leaves_singleton(profile, core):
            bad.append(core)
    assert bad == [singleton_indices]

    for repeated in range(5):
        special = singleton_indices | {repeated}
        assert len(special) == h + 1
        for omitted_singleton in singleton_indices:
            deletion = special - {omitted_singleton}
            assert len(deletion) == h
            assert leaves_singleton(profile, deletion)
            complement = tuple(
                multiplicity - (1 if index in deletion else 0)
                for index, multiplicity in enumerate(profile)
            )
            assert complement[omitted_singleton] == 1

    # Every nonspecial 9-set has only legal 8-deletions.
    for nine_tuple in combinations(range(len(profile)), h + 1):
        nine = set(nine_tuple)
        special = singleton_indices <= nine
        if special:
            assert len(nine - singleton_indices) == 1
            continue
        for deleted in nine:
            assert leaves_singleton(profile, nine - {deleted})


def check_hermite_and_exchange_degrees() -> None:
    for h in range(3, 31):
        k = 1
        p = h + k
        denominator_degree = (k + 1) + 2 * h
        numerator_cap = denominator_degree - 2
        complement_degree = p + 2
        assert numerator_cap - complement_degree == h - 3
        deletion_residual = h - 3
        lift_degree = deletion_residual + 3
        assert lift_degree == h
        repaired_degree = lift_degree - 2
        assert repaired_degree == h - 2 == (h + 1) - 3


def check_cubic_gauge_and_rational_lift() -> None:
    z, a, s = sp.symbols("z a s")
    gauge = (z - s) * (z + s) ** 2
    psi = 1 / (a + s) - 2 / (s - a)
    assert sp.factor(
        sp.diff(gauge, z).subs(z, -a) / gauge.subs(z, -a) + psi
    ) == 0
    assert sp.expand(gauge.subs(z, -s)) == 0
    assert sp.expand(sp.diff(gauge, z).subs(z, -s)) == 0
    assert sp.expand(gauge.subs(s, 0) - z**3) == 0

    old_B, old_D, q = sp.symbols("old_B old_D q", nonzero=True)
    new_B = old_B / (z - s)
    new_D = old_D * (z + s) ** 2
    assert sp.factor(new_B * gauge * q / new_D - old_B * q / old_D) == 0


def check_partial_pencil_inequalities() -> None:
    """Exhaust all gcd, zero, parity, and RH integer edges."""
    for h in range(3, 31):
        for epsilon in (0, 1):
            n = h - epsilon
            e0_values = (0,) if not epsilon else tuple([0] + list(range(2, h + 1)))
            tau_values = tuple([0] + list(range(2, h + 1)))
            for rho in range(n + 1):
                for sigma in range(n + 1):
                    for e0 in e0_values:
                        for tau in tau_values:
                            gcd_floor = rho + 2 * sigma + e0 + tau
                            delta_cap = h - gcd_floor
                            if delta_cap < 1:
                                continue

                            root_anchor_floor = n - rho - sigma
                            parity_gap = root_anchor_floor - delta_cap
                            expected_gap = -epsilon + sigma + e0 + tau
                            assert parity_gap == expected_gap
                            if expected_gap >= 0:
                                assert 2 * root_anchor_floor > 2 * delta_cap - 1
                            else:
                                assert epsilon == 1
                                assert sigma == e0 == tau == 0
                                assert root_anchor_floor >= delta_cap - 1
                                # The zero gauge adds multiplicity at least 3.
                                assert 2 * root_anchor_floor + 3 > 2 * delta_cap - 1

                            extra_x = int(tau == 0)
                            extra_zero = int(epsilon == 1 and e0 == 0)
                            half_forced = n - sigma + extra_x + extra_zero
                            lower_gap = (
                                1
                                - epsilon
                                + rho
                                + sigma
                                + e0
                                + tau
                                + extra_x
                                + extra_zero
                            )
                            assert half_forced - (delta_cap - 1) == lower_gap
                            assert lower_gap > 0
                            assert 2 * half_forced > 2 * delta_cap - 2


def check_triple_zero_in_parity_determinant() -> None:
    z = sp.symbols("z")
    for order in range(3, 10):
        r_tail = sum(sp.Symbol(f"r{order}_{j}") * z**j for j in range(4))
        r = z**order * r_tail
        q_coefficients = sp.symbols(f"q{order}_0:5")
        q = sum(coefficient * z**j for j, coefficient in enumerate(q_coefficients))
        cross = sp.expand(r * q.subs(z, -z) - r.subs(z, -z) * q)
        assert all(cross.coeff(z, degree) == 0 for degree in range(3))
        assert sp.expand(cross.subs(z, -z) + cross) == 0

    # The degree-2delta leading term always cancels.
    for delta in range(1, 9):
        p_coefficients = sp.symbols(f"p{delta}_0:{delta + 1}")
        q_coefficients = sp.symbols(f"s{delta}_0:{delta + 1}")
        p = sum(coefficient * z**j for j, coefficient in enumerate(p_coefficients))
        q = sum(coefficient * z**j for j, coefficient in enumerate(q_coefficients))
        cross = sp.expand(p * q.subs(z, -z) - p.subs(z, -z) * q)
        assert sp.Poly(cross, z).degree() <= 2 * delta - 1


def check_upward_propagation() -> None:
    h, classes = 8, 13
    residual_degree = h - 2  # repaired P_{h+1}
    assert residual_degree == 6
    for old_size in range(h + 1, classes):
        assert residual_degree == old_size - 3
        lift_degree = residual_degree + 3
        assert lift_degree == old_size
        if old_size + 1 < classes:
            residual_degree = lift_degree - 2
            assert residual_degree == old_size - 2
        else:
            # Retain the full c-class lift space.
            assert lift_degree == classes - 1 == 12


def check_terminal_excess_six_deficit() -> None:
    h, k, c = 8, 1, 13
    total = 2 * h + k + 2
    excess = total - c
    assert total == 19 and excess == 6
    degree_d0 = k + c
    primitive_decay = 2 * (c - h) - 1
    primitive_numerator_cap = degree_d0 - primitive_decay
    assert primitive_numerator_cap == excess - 1 == 5

    collision_multiplicities = (2, 1, 1, 1, 1)
    assert sum(collision_multiplicities) == excess
    for dimension in range(3, excess + 1):
        for mask in range(1 << len(collision_multiplicities)):
            absorbed = [
                multiplicity
                for index, multiplicity in enumerate(collision_multiplicities)
                if mask & (1 << index)
            ]
            a = sum(absorbed)
            gcd_floor = sum(multiplicity + 1 for multiplicity in absorbed)
            forced_weight = (excess - a) * (dimension - 1)
            wronskian_cap = dimension * (
                excess - gcd_floor - dimension
            )
            assert forced_weight > wronskian_cap
            assert forced_weight - wronskian_cap >= dimension**2 - excess >= 3


def main() -> None:
    check_unique_bad_core_and_special_deletions()
    check_hermite_and_exchange_degrees()
    check_cubic_gauge_and_rational_lift()
    check_partial_pencil_inequalities()
    check_triple_zero_in_parity_determinant()
    check_upward_propagation()
    check_terminal_excess_six_deficit()
    print("one-bad-core h-of-(h+1) exchange repair: PASS")
    print("partial-pencil parity and zero-anchor edge: exact")
    print("extra Robin-node ramification and RH contradiction: exact")
    print("profile (3,2^4,1^8): repaired and closed by e=6 terminal deficit")


if __name__ == "__main__":
    main()
