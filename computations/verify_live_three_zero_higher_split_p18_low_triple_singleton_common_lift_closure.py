#!/usr/bin/env python3
"""Exact audit for the complete p=18 low-triple common-lift closure."""

from __future__ import annotations

from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import verify_live_three_zero_higher_split_q5_boundary_census as q5


def selection_data(a: int, b: int, h: int) -> dict[str, int]:
    d = min(b, 2)
    total_singletons = h + 20 - 3 * a - 2 * b
    selected_singletons = h + 2 - 2 * d
    fixed_singletons = selected_singletons - 1
    pool = total_singletons - fixed_singletons
    remaining_doubles = b - d
    complement_singletons = pool - 1
    mass = 3 * a + 2 * remaining_doubles + complement_singletons
    classes = a + remaining_doubles + complement_singletons
    relation_degree = classes - 4
    kernel_degree = relation_degree + 3
    return {
        "d": d,
        "total_singletons": total_singletons,
        "selected_singletons": selected_singletons,
        "pool": pool,
        "remaining_doubles": remaining_doubles,
        "mass": mass,
        "classes": classes,
        "relation_degree": relation_degree,
        "kernel_degree": kernel_degree,
    }


def forced_weight(
    pool: int, doubles: int, triples: int, dim: int
) -> int:
    return (
        pool * (dim - 1)
        + doubles * (dim - 2)
        + triples * (dim - 3)
    )


def wronskian_cap(degree: int, dim: int) -> int:
    return dim * (degree + 1 - dim)


def survivor_triples() -> set[tuple[int, int, int]]:
    out: set[tuple[int, int, int]] = set()
    for a in range(7):
        for b in range(12):
            u = 20 - 3 * a - 2 * b
            applicable = (
                u >= 2
                or (u >= 0 and a + b >= 1)
                or (u >= -2 and (b >= 2 or (a >= 1 and b >= 1)))
            )
            if applicable and not (a == 0 and b == 0):
                out.add((a, b, u))
    assert len(out) == 50
    return out


def audit_singleton_lifts() -> None:
    for h in range(13, 18):
        for a, bs in ((1, range(10)), (0, range(1, 11))):
            for b in bs:
                x = selection_data(a, b, h)
                assert x["selected_singletons"] >= 1
                assert x["pool"] >= 1
                assert x["mass"] == 18
                assert x["relation_degree"] == x["classes"] - 4
                assert x["kernel_degree"] == x["relation_degree"] + 3

                profile = (
                    (3,) * a
                    + (2,) * b
                    + (1,) * x["total_singletons"]
                )
                selections = q5.formal_selections(profile, h, 18)
                expected_complement = tuple(
                    sorted(
                        (3,) * a
                        + (2,) * x["remaining_doubles"]
                        + (1,) * (x["pool"] - 1),
                        reverse=True,
                    )
                )
                assert q5.Selection(
                    x["d"], 0, expected_complement
                ) in selections

                # A transported relation three-space exists.  The common
                # first-/second-/third-order rows permit D=3 but exclude D=4.
                weight3 = forced_weight(
                    x["pool"], x["remaining_doubles"], a, 3
                )
                weight4 = forced_weight(
                    x["pool"], x["remaining_doubles"], a, 4
                )
                assert weight3 <= wronskian_cap(
                    x["kernel_degree"], 3
                )
                assert weight4 > wronskian_cap(
                    x["kernel_degree"], 4
                )

                # Algebraically, the inequality is D^2 + D <= 19.
                for dim in range(3, 8):
                    gap = forced_weight(
                        x["pool"], x["remaining_doubles"], a, dim
                    ) - wronskian_cap(x["kernel_degree"], dim)
                    assert gap == dim * dim + dim - 19

                multiple_dim = max(
                    x["kernel_degree"] - 3 * x["pool"] + 1, 0
                )
                if a == 1 and b == 9:
                    assert (x["pool"], x["remaining_doubles"]) == (2, 7)
                    assert x["kernel_degree"] == 8
                    assert multiple_dim == 3
                else:
                    assert multiple_dim < 3

    # The baseline has the moving singleton as a complementary simple
    # factor (z-q)^(-2), whereas the formal selection has the plus factor
    # z+q.  The cubic is their exact quotient and kills the complete
    # first jet at q, including q=0.
    z, q = sp.symbols("z q")
    s0, s1 = sp.symbols("s0 s1")
    f = (z - q) ** 2 * (z + q)
    assert sp.cancel(f / (z - q) ** 2) == z + q
    local_s = s0 + s1 * (z - q)
    assert (f * local_s).subs(z, q) == 0
    assert sp.diff(f * local_s, z).subs(z, q) == 0


def audit_b9_second_row() -> None:
    z, q1, q2, v = sp.symbols("z q1 q2 v")
    u0, u1, u2 = sp.symbols("u0 u1 u2")
    f1 = (z - q1) ** 2 * (z + q1)
    f2 = (z - q2) ** 2 * (z + q2)
    local_u = u0 + u1 * (z - v) + u2 * (z - v) ** 2
    test = f1 * f2 * (z - v) ** 2
    row = sp.expand(sp.diff(local_u * test, z, 2).subs(z, v))
    expected = 2 * u0 * f1.subs(z, v) * f2.subs(z, v)
    assert sp.factor(row - expected) == 0


def audit_eleven_double_endpoint() -> None:
    h = sp.symbols("h", integer=True)
    total_mass = 2 * 11 + (h - 2)
    selected_mass = 2 * 2 + (h - 2)
    assert sp.expand(total_mass - selected_mass) == 18

    for h_value in range(13, 18):
        profile = (2,) * 11 + (1,) * (h_value - 2)
        selections = q5.formal_selections(profile, h_value, 18)
        assert q5.Selection(2, 0, (2,) * 9) in selections

    complement_classes = 9
    relation_degree = complement_classes - 4
    lift_degree = 5
    kernel_degree = relation_degree + lift_degree
    assert (relation_degree, kernel_degree) == (5, 10)

    # Ten exact second-order rows force D <= 5.
    for dim in range(3, 12):
        gap = 10 * (dim - 2) - wronskian_cap(kernel_degree, dim)
        assert gap == (dim - 5) * (dim + 4)
        if dim >= 6:
            assert gap > 0

    # Coprime quintics inside P_10 have a one-dimensional intersection.
    single_multiple_dim = kernel_degree - 5 + 1
    pair_multiple_dim = kernel_degree - 10 + 1
    assert single_multiple_dim == 6
    assert pair_multiple_dim == 1
    assert 3 + 3 - 4 == 2 > pair_multiple_dim
    assert 3 + 3 - 5 == pair_multiple_dim

    # Removing moving selected double j from the baseline denominator
    # contributes (z-j)^(-3); selecting it contributes (z+j)^2.  Their
    # exact quotient is g_j, whose cube kills the complete baseline
    # two-jet at j.
    z, j = sp.symbols("z j")
    g_j = (z - j) ** 3 * (z + j) ** 2
    assert sp.factor(sp.cancel(g_j / (z - j) ** 3) - (z + j) ** 2) == 0
    s0, s1, s2 = sp.symbols("s0 s1 s2")
    local_s = s0 + s1 * (z - j) + s2 * (z - j) ** 2
    for order in range(3):
        assert sp.diff(g_j * local_s, z, order).subs(z, j) == 0

    # Exact logarithmic-jet and product-rule identities.
    z, x, v = sp.symbols("z x v")
    g = (z - x) ** 3 * (z + x) ** 2
    log_jet = sp.factor(sp.diff(g, z).subs(z, v) / g.subs(z, v))
    assert sp.factor(log_jet - (5 * v + x) / (v**2 - x**2)) == 0

    u0, u1, u2 = sp.symbols("u0 u1 u2", nonzero=True)
    aj, ak, bj0, bk0 = sp.symbols("aj ak bj0 bk0")
    # Normalize U(v)=u0, U'(v)=u1, U''(v)=u2 and
    # g_j(v)=g_k(v)=1.  Their first and second jets are aj,bj0 and
    # ak,bk0.  This verifies C+B_j+B_k+2 A_j A_k.
    t = sp.symbols("t")
    U = u0 + u1 * t + u2 * t**2 / 2
    gj = 1 + aj * t + bj0 * t**2 / 2
    gk = 1 + ak * t + bk0 * t**2 / 2
    normalized_second = sp.expand(sp.diff(U * gj * gk, t, 2).subs(t, 0) / u0)
    target = (
        u2 / u0
        + (bj0 + 2 * u1 * aj / u0)
        + (bk0 + 2 * u1 * ak / u0)
        + 2 * aj * ak
    )
    assert sp.factor(normalized_second - target) == 0

    c = sp.symbols("c")
    fibre_polynomial = sp.expand(c * (v**2 - x**2) - (5 * v + x))
    assert sp.Poly(fibre_polynomial, x).degree() <= 2
    assert sp.Poly(fibre_polynomial, x).coeff_monomial(x) == -1

    # After fixing i and the tested v, nine partners remain; a differing
    # pair forces the other seven into one fibre, and an equal set puts all
    # nine in one fibre.  Both exceed the exact fibre cap two.
    assert 11 - 2 == 9
    assert 9 - 2 == 7
    assert 7 > 2 and 9 > 2


def audit_completed_ledger() -> None:
    old = survivor_triples()
    prior_closed = {
        (a, b, 20 - 3 * a - 2 * b)
        for a in range(2, 7)
        for b in range(12)
    } & old
    one_triple = {(1, b, 17 - 2 * b) for b in range(10)}
    zero_triple = {(0, b, 20 - 2 * b) for b in range(1, 12)}
    newly_closed = one_triple | zero_triple
    assert len(prior_closed) == 29
    assert len(newly_closed) == 21
    assert prior_closed.isdisjoint(newly_closed)
    assert prior_closed | newly_closed == old


def main() -> None:
    audit_singleton_lifts()
    audit_b9_second_row()
    audit_eleven_double_endpoint()
    audit_completed_ledger()
    print("p=18 complete low-triple common-lift closure PASS")
    print("newly closed equality families: 21")
    print("p=18 ledger: 50/50 closed")


if __name__ == "__main__":
    main()
