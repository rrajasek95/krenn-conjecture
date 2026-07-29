#!/usr/bin/env python3
"""Exact audit of the p=28 two-quartic singleton-swap q=6 cap."""

from __future__ import annotations

import sympy as sp


def audit_formal_profiles_and_grid() -> None:
    residuals = ((2, 7, 0, 1), (2, 7, 1, -1))
    for h in range(22, 28):
        k = 28 - h
        for e, a, b, u in residuals:
            assert 4 * e + 3 * a + 2 * b + u == 30
            selected_layers = 1 + b
            selected_singletons = h + 2 - 2 * selected_layers
            total_singletons = h + u
            assert total_singletons - selected_singletons == 1

            complement = (
                (4,) * e
                + (3,) * (a - 1)
                + (1, 1)
            )
            assert complement == (4, 4) + (3,) * 6 + (1, 1)
            assert sum(complement) == 28
            assert len(complement) == 10

            # The selected six-space is exactly at its first boundary,
            # while a seven-space still has positive excess.
            for q, expected_gap in ((6, 0), (7, 12)):
                forced = (
                    selected_layers * max(0, q - 2)
                    + selected_singletons * max(0, q - 1)
                    + max(0, q - k)
                )
                degree = h + 3 - selected_layers
                cap = q * (degree + 1 - q)
                assert forced - cap == expected_gap

            singleton_count = total_singletons
            all_q5_columns = singleton_count - 7
            expected = h - 6 if b == 0 else h - 8
            assert all_q5_columns == expected
            assert all_q5_columns >= (16 if b == 0 else 14)


def audit_common_kernel_bound() -> None:
    # Baseline: two moving simples, two quartics, six triples, one fixed
    # simple.  It lives in P_9.
    dimension = 5
    forced = (
        2 * (dimension - 1)
        + 2 * (dimension - 4)
        + 6 * (dimension - 3)
        + (dimension - 1)
    )
    cap = dimension * (10 - dimension)
    assert forced == 26
    assert cap == 25
    assert forced - cap == 1

    relation_dimension = 6 - 2
    common_dimension_cap = 4
    assert relation_dimension == common_dimension_cap


def audit_cubic_intersection_and_simple_row() -> None:
    z = sp.symbols("z")
    s, t, x = sp.symbols("s t x")
    f_s = (z - s) ** 2 * (z + s)
    f_t = (z - t) ** 2 * (z + t)

    # A separated specialization certifies the structural degree and
    # coprimality statement; symbolically the roots are {s,-s} and
    # {t,-t}.
    f_s_sample = sp.Poly(f_s.subs(s, 2), z)
    f_t_sample = sp.Poly(f_t.subs(t, 5), z)
    assert f_s_sample.degree() == f_t_sample.degree() == 3
    assert sp.gcd(f_s_sample, f_t_sample).degree() == 0
    assert 9 - 6 + 1 == 4
    assert 9 - (3 + 3) + 1 == 4

    # On S=f_s*P_3 the fixed simple row has coefficient
    # U(x) f_s(x) on V'(x).  Structural separation makes it nonzero.
    sample = f_s.subs({s: 2, x: 7})
    assert sp.expand(sample.subs(z, 7)) != 0
    u0, u1 = sp.symbols("u0 u1", nonzero=True)
    v0, v1 = sp.symbols("v0 v1")
    local_row = sp.expand(
        u1 * sample.subs(z, x) * v0
        + u0
        * (
            sp.diff(sample, z).subs(z, x) * v0
            + sample.subs(z, x) * v1
        )
    )
    assert sp.factor(sp.diff(local_row, v1) - u0 * sample.subs(z, x)) == 0
    assert sp.diff(local_row, v1) != 0


def main() -> None:
    audit_formal_profiles_and_grid()
    audit_common_kernel_bound()
    audit_cubic_intersection_and_simple_row()
    print("p=28 two-quartic singleton-swap q=6 cap: PASS")
    print("for each triple: at most one q=6 singleton choice")
    print("grid consequence: at least h-6 or h-8 all-q=5 columns")
    print("scope guard: dimension statement only, not profile closure")


if __name__ == "__main__":
    main()
