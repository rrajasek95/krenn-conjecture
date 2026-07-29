#!/usr/bin/env python3
"""Exact rational checks for polarized six-site counterexamples.

We work in the site-square-zero algebra.  If q and z are quadratic, the
coefficient of a coloring in z*q^2/2 is the sum over perfect matchings and
one distinguished z-edge.  All arithmetic below uses Fraction.
"""

from __future__ import annotations

import itertools
from fractions import Fraction as F


N = 6
C = 3
EDGES = tuple(itertools.combinations(range(N), 2))
COLORINGS = tuple(itertools.product(range(C), repeat=N))


def perfect_matchings(vertices=tuple(range(N))):
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for v in vertices[1:]:
        rest = tuple(w for w in vertices if w not in (u, v))
        for tail in perfect_matchings(rest):
            yield ((u, v),) + tail


MATCHINGS = tuple(perfect_matchings())


def polarized_coefficients(q, z):
    """Return all coefficients of z*q^2/2."""
    out = {}
    for coloring in COLORINGS:
        value = F(0)
        for matching in MATCHINGS:
            qvals = [q.get((edge, coloring[edge[0]], coloring[edge[1]]), F(0)) for edge in matching]
            zvals = [z.get((edge, coloring[edge[0]], coloring[edge[1]]), F(0)) for edge in matching]
            for distinguished in range(3):
                other = [k for k in range(3) if k != distinguished]
                value += zvals[distinguished] * qvals[other[0]] * qvals[other[1]]
        out[coloring] = value
    return out


def target():
    return {coloring: F(int(len(set(coloring)) == 1)) for coloring in COLORINGS}


def unrestricted_example():
    # Three two-edge near-perfect matchings, one for each color.
    q = {
        ((2, 3), 0, 0): F(1),
        ((4, 5), 0, 0): F(1),
        ((1, 4), 1, 1): F(1),
        ((3, 5), 1, 1): F(1),
        ((0, 5), 2, 2): F(1),
        ((3, 4), 2, 2): F(1),
    }
    z = {
        ((0, 1), 0, 0): F(1),
        ((0, 2), 1, 1): F(1),
        ((1, 2), 2, 2): F(1),
    }
    return q, z


def paircap_example():
    # The omitted cells are exactly zero.
    q = {
        ((0, 1), 1, 0): F(-1),
        ((0, 3), 0, 0): F(1),
        ((0, 3), 1, 1): F(1),
        ((0, 4), 1, 0): F(-1),
        ((0, 4), 1, 1): F(1),
        ((0, 5), 2, 2): F(1),
        ((1, 2), 0, 1): F(-1),
        ((1, 2), 2, 2): F(1),
        ((1, 3), 0, 1): F(-1),
        ((1, 4), 2, 0): F(-1),
        ((1, 5), 1, 1): F(1, 3),
        ((2, 3), 1, 1): F(1),
        ((2, 4), 1, 0): F(-1),
        ((2, 5), 0, 0): F(1, 6),
        ((3, 4), 1, 0): F(-1),
        ((3, 4), 2, 2): F(1, 3),
    }
    p = {
        (1, 0): F(1),
        (4, 0): F(1),
    }
    s = {
        (0, 1): F(1),
        (1, 0): F(1),
        (1, 2): F(1),
        (2, 1): F(1),
        (3, 1): F(1),
        (4, 0): F(1),
    }

    # a=1 and z=q+3ps, with (ps)_ij=p_i*s_j+s_i*p_j.
    z = {}
    for edge in EDGES:
        i, j = edge
        for a, b in itertools.product(range(C), repeat=2):
            value = q.get((edge, a, b), F(0))
            value += 3 * (p.get((i, a), F(0)) * s.get((j, b), F(0)))
            value += 3 * (s.get((i, a), F(0)) * p.get((j, b), F(0)))
            if value:
                z[edge, a, b] = value
    return q, p, s, z


def main():
    expected = target()

    q0, z0 = unrestricted_example()
    got0 = polarized_coefficients(q0, z0)
    assert got0 == expected

    q, p, s, z = paircap_example()
    got = polarized_coefficients(q, z)
    assert got == expected

    # Check the defining pair-cap identity cell by cell independently of
    # the construction loop above.
    for edge in EDGES:
        i, j = edge
        for a, b in itertools.product(range(C), repeat=2):
            ps = p.get((i, a), F(0)) * s.get((j, b), F(0))
            ps += s.get((i, a), F(0)) * p.get((j, b), F(0))
            assert z.get((edge, a, b), F(0)) == q.get((edge, a, b), F(0)) + 3 * ps

    print("unrestricted polarized example: exact PASS")
    print(f"  q cells={len(q0)}, z cells={len(z0)}")
    print("pair-cap constrained example z=q+3ps: exact PASS")
    print(f"  q cells={len(q)}, p coordinates={len(p)}, s coordinates={len(s)}, z cells={len(z)}")
    print("  nonzero output coefficients:")
    for coloring, value in got.items():
        if value:
            print(f"    {''.join(map(str, coloring))}: {value}")


if __name__ == "__main__":
    main()
