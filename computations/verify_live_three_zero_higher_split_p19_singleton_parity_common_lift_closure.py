#!/usr/bin/env python3
"""Exact audit for the p=19 singleton-parity common-lift closure."""

from __future__ import annotations

from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import verify_live_three_zero_higher_split_q5_boundary_census as q5


def parameter_families(e: int) -> set[tuple[int, int, int]]:
    """The p=19 symbolic families with e=0 or one quartic."""
    assert e in (0, 1)
    offset = 21 - 4 * e
    out: set[tuple[int, int, int]] = set()
    for a in range(20):
        for b in range(20):
            u = offset - 3 * a - 2 * b
            applicable = (
                u >= 2
                or (u >= 0 and a + b >= 1)
                or (
                    u >= -2
                    and (b >= 2 or (a >= 1 and b >= 1))
                )
            )
            if applicable and not (e == 0 and a == 0 and b == 0):
                out.add((a, b, u))
    return out


def profile_from_parameters(
    h: int, e: int, a: int, b: int, u: int
) -> tuple[int, ...]:
    return (
        (4,) * e
        + (3,) * a
        + (2,) * b
        + (1,) * (h + u)
    )


def selected_data(e: int, a: int, b: int, u: int) -> dict[str, int]:
    d = min(b, 2)
    pool = u - 1 + 2 * d
    remaining_doubles = b - d
    fixed_classes = e + a + remaining_doubles
    classes = pool - 1 + fixed_classes
    relation_degree = classes - 4
    common_degree = classes - 1
    return {
        "d": d,
        "pool": pool,
        "remaining_doubles": remaining_doubles,
        "fixed_classes": fixed_classes,
        "classes": classes,
        "relation_degree": relation_degree,
        "common_degree": common_degree,
    }


def expected_complement(
    e: int, a: int, remaining_doubles: int, pool: int
) -> tuple[int, ...]:
    return tuple(
        sorted(
            (4,) * e
            + (3,) * a
            + (2,) * remaining_doubles
            + (1,) * (pool - 1),
            reverse=True,
        )
    )


def audit_symbolic_census() -> None:
    no_quartic = parameter_families(0)
    one_quartic = parameter_families(1)
    assert len(no_quartic) == 55
    assert len(one_quartic) == 39

    for h in range(13, 19):
        observed = q5.symbolic_survivors(h, 19)
        expected = {
            profile_from_parameters(h, e, a, b, u)
            for e, family in ((0, no_quartic), (1, one_quartic))
            for a, b, u in family
        }
        assert observed == expected
        assert len(observed) == 94


def audit_closed_families() -> None:
    closed: dict[int, set[tuple[int, int, int]]] = {0: set(), 1: set()}
    expected_ranges = {
        0: {
            (a, b, (21 - 3 * a - 2 * b))
            for a, last_b in (
                (0, 7),
                (1, 6),
                (2, 5),
                (3, 4),
                (4, 3),
                (5, 2),
            )
            for b in range(1 if a == 0 else 0, last_b + 1)
        },
        1: {
            (a, b, (17 - 3 * a - 2 * b))
            for a, last_b in (
                (0, 6), (1, 5), (2, 4), (3, 3), (4, 2)
            )
            for b in range(last_b + 1)
        },
    }

    for e in (0, 1):
        for a, b, u in parameter_families(e):
            data = selected_data(e, a, b, u)
            if data["pool"] >= 1 and data["fixed_classes"] <= 5:
                closed[e].add((a, b, u))

                # A formal no-selected-triple choice realizes the count.
                for h in range(13, 19):
                    profile = profile_from_parameters(h, e, a, b, u)
                    complement = expected_complement(
                        e,
                        a,
                        data["remaining_doubles"],
                        data["pool"],
                    )
                    selection = q5.Selection(data["d"], 0, complement)
                    assert selection in q5.formal_selections(
                        profile, h, 19
                    )

                    selected_singletons = h + 2 - 2 * data["d"]
                    total_singletons = h + u
                    assert (
                        total_singletons - (selected_singletons - 1)
                        == data["pool"]
                    )

                    # The q=6 row-kernel branch is strictly excluded.
                    k = 19 - h
                    assert 22 - h + max(0, 6 - k) > 0

                assert sum(complement) == 19
                assert sum(min(part, 5) for part in complement) == 19
                assert len(complement) == data["classes"]
                assert data["relation_degree"] == (
                    data["pool"] + data["fixed_classes"] - 5
                )
                assert data["common_degree"] == (
                    data["relation_degree"] + 3
                )

                # A three-dimensional relation space must fit.
                assert data["relation_degree"] >= 2

                # Every possible common five-space violates its exact
                # row Wronskian cap by ten units at p=19.
                forced_weight = data["pool"] * 4 + sum(
                    max(0, 5 - part)
                    for part in complement
                    if part != 1
                )
                # The preceding comprehension is unsafe when fixed
                # classes themselves have multiplicity one.  Recompute
                # directly from the baseline multiset instead.
                fixed_parts = (
                    (4,) * e
                    + (3,) * a
                    + (2,) * data["remaining_doubles"]
                )
                forced_weight = data["pool"] * 4 + sum(
                    max(0, 5 - part) for part in fixed_parts
                )
                cap = 5 * (data["common_degree"] + 1 - 5)
                assert forced_weight - cap == 10

                # For fixed q there are m pool partners and relation
                # degree n.  C <= 5 is exactly m >= n - 1.
                m = data["pool"] - 1
                n = data["relation_degree"]
                assert m - n == 4 - data["fixed_classes"]
                assert m >= n - 1

    assert closed == expected_ranges
    assert len(closed[0]) == 32
    assert len(closed[1]) == 25
    assert len(closed[0] | {(99 + a, b, u) for a, b, u in closed[1]}) == 57


def audit_uniform_kernel_inequality() -> None:
    # For arbitrary fixed multiplicities, a common five-space can exist
    # only if the formal complement's five-capped mass is at least 29.
    for pool in range(1, 20):
        for fixed_parts in (
            (),
            (1,),
            (2, 3),
            (4, 7),
            (1, 2, 3, 4),
            (8, 9, 10),
        ):
            fixed_classes = len(fixed_parts)
            formal_capped = pool - 1 + sum(
                min(part, 5) for part in fixed_parts
            )
            degree = pool + fixed_classes - 2
            weight = pool * 4 + sum(
                max(0, 5 - part) for part in fixed_parts
            )
            cap = 5 * (degree + 1 - 5)
            assert weight - cap == 29 - formal_capped


def audit_parity_and_square_bound() -> None:
    z = sp.symbols("z")
    coefficients_a = sp.symbols("a0:8")
    coefficients_b = sp.symbols("b0:8")
    a_poly = sum(coefficients_a[i] * z**i for i in range(8))
    b_poly = sum(coefficients_b[i] * z**i for i in range(8))
    delta = sp.expand(a_poly * b_poly.subs(z, -z) - a_poly.subs(z, -z) * b_poly)
    assert sp.expand(delta.subs(z, -z) + delta) == 0
    assert sp.Poly(delta, z).degree() <= 13  # the top odd term is <= 2n-1

    # At the sharp m=n-1 boundary, all minors lie in one polynomial
    # line.  Their coefficients form a 3x3 alternating matrix, whose
    # determinant vanishes and whose rank is at most two.
    l01, l02, l12 = sp.symbols("l01 l02 l12")
    alternating = sp.Matrix(
        [[0, l01, l02], [-l01, 0, l12], [-l02, -l12, 0]]
    )
    assert alternating.det() == 0
    radical = sp.Matrix([l12, -l02, l01])
    assert alternating * radical == sp.zeros(3, 1)

    # At a zero pool point, a plane member z^3 B produces parity order
    # at least three against an arbitrary section.
    generic = sum(coefficients_a[i] * z**i for i in range(5))
    plane_member = z**3 * sum(coefficients_b[i] * z**i for i in range(2))
    zero_delta = sp.expand(
        generic * plane_member.subs(z, -z)
        - generic.subs(z, -z) * plane_member
    )
    assert sp.rem(zero_delta, z**3, domain=sp.QQ.frac_field(*coefficients_a, *coefficients_b)) == 0

    # Once every parity determinant vanishes, the gcd/square-space
    # argument gives m <= n-4 for every possible gcd degree.
    for n in range(2, 80):
        possible = []
        for gcd_degree in range(n + 1):
            square_degree = (n - gcd_degree) // 2
            if square_degree < 2:
                continue
            possible.append((gcd_degree, square_degree))
            # Twice the bound avoids fractions:
            # 2m <= 2g + 3(M-2) <= 2(n-4).
            assert (
                2 * gcd_degree + 3 * (square_degree - 2)
                <= 2 * (n - 4)
            )
        if n >= 4:
            assert possible


def main() -> None:
    audit_symbolic_census()
    audit_closed_families()
    audit_uniform_kernel_inequality()
    audit_parity_and_square_bound()
    print("p=19 singleton-parity common-lift closure: PASS")
    print("exact p=19 census: 55 no-quartic + 39 one-quartic = 94")
    print("new uniform closure: 32 + 25 = 57 families")
    print("five-capped common-kernel and parity/gcd bounds: audited")


if __name__ == "__main__":
    main()
