#!/usr/bin/env python3
"""Exact audit of the k=1 constant-core role-swap theorems."""

from __future__ import annotations

import importlib.util
from itertools import combinations
from pathlib import Path
from types import ModuleType

import sympy as sp


def load_frontier_checker() -> ModuleType:
    path = Path(__file__).with_name(
        "verify_live_three_zero_higher_split_collision_frontier.py"
    )
    specification = importlib.util.spec_from_file_location(
        "higher_split_collision_frontier_for_role_swap", path
    )
    assert specification is not None and specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def check_constant_residual_degrees() -> None:
    for h in range(3, 31):
        p, k = h + 1, 1
        for first in range(1, h - 1):
            for second in range(1, h - first):
                third = h - first - second
                denominator_degree = (k + 1) + sum(
                    count + 1 for count in (first, second, third)
                )
                numerator_cap = p + 3 - 1
                complement_degree = p + 2
                assert denominator_degree == h + 5
                assert numerator_cap == complement_degree == h + 3
                assert denominator_degree - numerator_cap == 2


def delta(count: int, value: sp.Expr, mu: sp.Expr) -> sp.Expr:
    return count / (value + mu) - (count + 1) / (value - mu)


def check_role_function_and_direct_baseline() -> None:
    value, mu, multiplicity = sp.symbols("value mu multiplicity")
    for count in range(1, 9):
        baseline = -multiplicity / (value + mu)
        selected = -(multiplicity - count) / (value + mu) - (
            count + 1
        ) / (value - mu)
        assert sp.factor(selected - baseline - delta(count, value, mu)) == 0
        assert sp.factor(
            delta(count, value, mu)
            + (value + (2 * count + 1) * mu) / (value**2 - mu**2)
        ) == 0

    # Reconstruct a complete three-role equation directly from arbitrary
    # full multiplicities; no background term moves with x.
    a, b, x = sp.symbols("a b x")
    ma, mb, mx = sp.symbols("ma mb mx")
    r, s, j = 2, 3, 4
    direct = (
        -(ma - r) / (a + mu)
        - (r + 1) / (a - mu)
        - (mb - s) / (b + mu)
        - (s + 1) / (b - mu)
        - (mx - j) / (x + mu)
        - (j + 1) / (x - mu)
    )
    baseline = -ma / (a + mu) - mb / (b + mu) - mx / (x + mu)
    roles = delta(r, a, mu) + delta(s, b, mu) + delta(j, x, mu)
    assert sp.factor(direct - baseline - roles) == 0


def check_fibre_and_zero_safety() -> None:
    x, mu, fibre_value = sp.symbols("x mu fibre_value")
    for count in range(1, 9):
        phi = delta(count, x, mu)
        expected = -(x + (2 * count + 1) * mu) / (x**2 - mu**2)
        assert sp.factor(phi - expected) == 0

        fibre = sp.expand(
            fibre_value * (x**2 - mu**2) + x + (2 * count + 1) * mu
        )
        assert sp.Poly(fibre, x).degree() == 2
        assert sp.Poly(fibre, x).coeff_monomial(x) == 1
        assert sp.expand(fibre.subs(fibre_value, 0)) == x + (2 * count + 1) * mu

        # If the exceptional value is zero, structural x+mu!=0 gives
        # mu!=0 and the denominator is -mu^2.  If mu=0, structural
        # x!=mu gives x!=0 and the denominator is x^2.
        denominator = x**2 - mu**2
        assert denominator.subs(x, 0) == -mu**2
        assert denominator.subs(mu, 0) == x**2
        assert sp.factor(phi.subs(x, 0) - (2 * count + 1) / mu) == 0
        assert sp.factor(phi.subs(mu, 0) + 1 / x) == 0


def check_unequal_swap_factorization() -> None:
    x, y, mu = sp.symbols("x y mu", nonzero=True)
    for r in range(1, 8):
        for s in range(1, 8):
            if r == s:
                continue
            difference = sp.factor(
                delta(r, x, mu)
                + delta(s, y, mu)
                - delta(s, x, mu)
                - delta(r, y, mu)
            )
            expected = sp.factor(
                2
                * mu
                * (r - s)
                * (x - y)
                * (x + y)
                / ((x**2 - mu**2) * (y**2 - mu**2))
            )
            assert sp.factor(difference - expected) == 0
            cleared = sp.factor(
                difference * (x**2 - mu**2) * (y**2 - mu**2)
            )
            assert cleared == 2 * mu * (r - s) * (x - y) * (x + y)


def moving_role_witness(profile: tuple[int, ...], h: int, leaves_singleton):
    """Literal indexed search for Theorem 1.1."""
    classes = len(profile)
    for fixed_a, fixed_b in combinations(range(classes), 2):
        for take_a in range(1, profile[fixed_a] + 1):
            for take_b in range(1, profile[fixed_b] + 1):
                moving_take = h - take_a - take_b
                if moving_take < 1:
                    continue
                candidates = []
                for moving in range(classes):
                    if moving in (fixed_a, fixed_b):
                        continue
                    if profile[moving] < moving_take:
                        continue
                    takes = {
                        fixed_a: take_a,
                        fixed_b: take_b,
                        moving: moving_take,
                    }
                    if leaves_singleton(profile, takes):
                        candidates.append(moving)
                if len(candidates) >= 3:
                    return (
                        fixed_a,
                        take_a,
                        fixed_b,
                        take_b,
                        moving_take,
                        tuple(candidates),
                    )
    return None


def unequal_swap_witness(profile: tuple[int, ...], h: int, leaves_singleton):
    """Literal indexed search for Theorem 1.2."""
    classes = len(profile)
    for fixed in range(classes):
        for fixed_take in range(1, profile[fixed] + 1):
            others = [index for index in range(classes) if index != fixed]
            for left, right in combinations(others, 2):
                for left_take in range(1, h - fixed_take):
                    right_take = h - fixed_take - left_take
                    if right_take < 1 or left_take == right_take:
                        continue
                    if max(left_take, right_take) > min(
                        profile[left], profile[right]
                    ):
                        continue
                    first = {
                        fixed: fixed_take,
                        left: left_take,
                        right: right_take,
                    }
                    second = {
                        fixed: fixed_take,
                        left: right_take,
                        right: left_take,
                    }
                    if leaves_singleton(profile, first) and leaves_singleton(
                        profile, second
                    ):
                        return (
                            fixed,
                            fixed_take,
                            left,
                            right,
                            left_take,
                            right_take,
                        )
    return None


EXPECTED_MOVING = {
    (4, 4, 3, 2, 2, 2, 2),
    (4, 3, 3, 3, 3, 3),
    (4, 3, 3, 2, 2, 2, 2, 1),
    (4, 3, 3, 2, 2, 1, 1, 1, 1, 1),
    (3, 3, 3, 3, 3, 3, 1),
    (3, 3, 3, 3, 3, 2, 2),
    (3, 3, 3, 3, 3, 2, 1, 1),
    (3, 3, 3, 3, 3, 1, 1, 1, 1),
    (3, 3, 3, 3, 2, 2, 2, 1),
    (3, 3, 3, 3, 2, 1, 1, 1, 1, 1),
    (3, 3, 3, 2, 2, 1, 1, 1, 1, 1, 1),
    (3, 3, 2, 2, 2, 2, 1, 1, 1, 1, 1),
    (3, 3, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1),
}

EXPECTED_SWAP_ONLY = {
    (3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1),
    (3, 3, 3, 2, 2, 2, 2, 2),
    (3, 3, 3, 2, 1, 1, 1, 1, 1, 1, 1, 1),
    (3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
}


def check_exact_frontier_census() -> None:
    frontier = load_frontier_checker()
    counts, residuals = frontier.census(8, 9)
    assert counts["R"] == len(residuals) == 35

    moving = {
        profile
        for profile in residuals
        if moving_role_witness(profile, 8, frontier.leaves_singleton) is not None
    }
    swapped = {
        profile
        for profile in residuals
        if unequal_swap_witness(profile, 8, frontier.leaves_singleton) is not None
    }
    assert moving == EXPECTED_MOVING
    assert len(moving) == 13
    assert len(swapped) == 15
    assert swapped - moving == EXPECTED_SWAP_ONLY
    assert len(moving | swapped) == 17

    # Audit every returned witness literally, including all candidate
    # complements rather than just the first candidate.
    for profile in moving:
        witness = moving_role_witness(profile, 8, frontier.leaves_singleton)
        assert witness is not None
        a, take_a, b, take_b, moving_take, candidates = witness
        assert take_a + take_b + moving_take == 8
        assert len(candidates) >= 3
        for candidate in candidates:
            takes = {a: take_a, b: take_b, candidate: moving_take}
            assert len(takes) == 3
            assert profile[candidate] >= moving_take
            assert frontier.leaves_singleton(profile, takes)

    for profile in swapped:
        witness = unequal_swap_witness(profile, 8, frontier.leaves_singleton)
        assert witness is not None
        fixed, fixed_take, left, right, left_take, right_take = witness
        assert left_take != right_take
        assert fixed_take + left_take + right_take == 8
        assert max(left_take, right_take) <= min(profile[left], profile[right])
        assert frontier.leaves_singleton(
            profile,
            {fixed: fixed_take, left: left_take, right: right_take},
        )
        assert frontier.leaves_singleton(
            profile,
            {fixed: fixed_take, left: right_take, right: left_take},
        )

    # The two previously isolated proofs are both subsumed.
    assert (4, 3, 3, 3, 3, 3) in moving
    assert (3, 3, 3, 2, 2, 2, 2, 2) in swapped


def main() -> None:
    check_constant_residual_degrees()
    check_role_function_and_direct_baseline()
    check_fibre_and_zero_safety()
    check_unequal_swap_factorization()
    check_exact_frontier_census()
    print("k=1 constant-core role-swap theorem: PASS")
    print("moving-role fibre closures among old h=8 R profiles: 13/35")
    print("unequal-role swap closures among old h=8 R profiles: 15/35")
    print("union closure: 17/35, with four swap-only profiles")


if __name__ == "__main__":
    main()
