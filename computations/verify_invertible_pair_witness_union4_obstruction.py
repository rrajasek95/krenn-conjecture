#!/usr/bin/env python3
r"""Independent hard-first audit for a four-site witness union.

This checker enumerates the 23 S_4 x S_3 incidence orbits, applies only the
proved hard-capacity rules, verifies that twelve orbits survive, and checks
that nine of those satisfy the two-hole determinant criterion.  It also
checks the local determinant factorization and the two exceptional monomial
comparisons.  The three remaining rows are closed analytically in
``notes/n8-hard-annihilator-union-four.md``.
"""

from itertools import product

import sympy as sp

from classify_invertible_pair_witness_union4 import (
    COLORS,
    EXPECTED_SYSTEMS,
    NONE,
    SITES,
    memberships,
    set_system_orbits,
)


ALL_COLORS = frozenset(COLORS)


def hard_assignments(member):
    """Enumerate hard colors consistent with the exact capacity rule."""

    triple_sites = tuple(u for u in SITES if member[u] == ALL_COLORS)
    fixed = {
        u: (frozenset() if u in triple_sites else member[u]) for u in SITES
    }
    answer = []
    for choices in product((NONE,) + COLORS, repeat=len(triple_sites)):
        hard = {u: set(fixed[u]) for u in SITES}
        for u, color in zip(triple_sites, choices, strict=True):
            if color != NONE:
                hard[u].add(color)
        if all(sum(r in hard[u] for u in SITES) >= 2 for r in COLORS):
            answer.append({u: frozenset(hard[u]) for u in SITES})
    return tuple(answer)


def determinant_certificate(member, hard):
    """Find a target color meeting the proved two-hole criterion."""

    for r in COLORS:
        hard_sites = tuple(u for u in SITES if r in hard[u])
        if len(hard_sites) != 2:
            continue
        if not all(len(member[u]) == 2 for u in hard_sites):
            continue
        outside = set(SITES) - set(hard_sites)
        if all(
            any(s in hard[u] for u in outside)
            for s in COLORS
            if s != r
        ):
            return r, hard_sites
    return None


def audit_local_algebra():
    """Check the determinant factorization and monomial distinctions."""

    xr, xa, yr, ya, XR, Xb, YR, Yb = sp.symbols(
        "xr xa yr ya XR Xb YR Yb"
    )
    correction = sp.Matrix(
        [
            [xr * YR + yr * XR, xr * Yb + yr * Xb],
            [xa * YR + ya * XR, xa * Yb + ya * Xb],
        ]
    )
    expected = (xr * ya - xa * yr) * (YR * Xb - Yb * XR)
    assert sp.expand(correction.det() - expected) == 0

    zu1, zu2, zv1, zv2 = sp.symbols("zu1 zu2 zv1 zv2")
    assert sp.Poly(zu1 * zv1, zu1, zu2, zv1, zv2).monoms() != sp.Poly(
        zu2 * zv2, zu1, zu2, zv1, zv2
    ).monoms()
    assert sp.Poly(zu1, zu1, zu2).monoms() != sp.Poly(
        zu2, zu1, zu2
    ).monoms()


EXPECTED_SURVIVORS = {
    ((0, 1), (0, 1), (2, 3)),
    ((0, 1), (0, 1, 2), (0, 2, 3)),
    ((0, 1), (0, 1, 2, 3), (0, 1, 2, 3)),
    ((0, 1), (0, 2), (1, 2, 3)),
    ((0, 1), (0, 2), (1, 3)),
    ((0, 1), (0, 2, 3), (0, 1, 2, 3)),
    ((0, 1), (0, 2, 3), (0, 2, 3)),
    ((0, 1), (0, 2, 3), (1, 2, 3)),
    ((0, 1), (2, 3), (0, 1, 2)),
    ((0, 1), (2, 3), (0, 1, 2, 3)),
    ((0, 1, 2), (0, 1, 3), (0, 1, 2, 3)),
    ((0, 1, 2), (0, 1, 3), (0, 2, 3)),
}

EXPECTED_EXCEPTIONS = {
    ((0, 1), (0, 1), (2, 3)),
    ((0, 1), (0, 1, 2, 3), (0, 1, 2, 3)),
    ((0, 1), (0, 2, 3), (0, 2, 3)),
}


def main():
    assert set_system_orbits() == EXPECTED_SYSTEMS
    audit_local_algebra()

    survivors = {}
    determinant_rows = set()
    for system_tuple in EXPECTED_SYSTEMS:
        member = memberships(tuple(map(frozenset, system_tuple)))
        choices = hard_assignments(member)
        if not choices:
            continue
        survivors[system_tuple] = choices
        if all(determinant_certificate(member, hard) for hard in choices):
            determinant_rows.add(system_tuple)

    assert set(survivors) == EXPECTED_SURVIVORS
    assert determinant_rows == EXPECTED_SURVIVORS - EXPECTED_EXCEPTIONS
    print("classified witness-union orbits:", len(EXPECTED_SYSTEMS))
    print("retained by hard capacity:", len(survivors))
    print("covered by two-hole determinant:", len(determinant_rows))
    print("analytic exceptional rows:", tuple(sorted(EXPECTED_EXCEPTIONS)))


if __name__ == "__main__":
    main()
