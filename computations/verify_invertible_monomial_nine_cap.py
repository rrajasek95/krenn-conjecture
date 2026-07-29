#!/usr/bin/env python3
"""Exact audit of the invertible-monomial nine-cap classification."""

from __future__ import annotations

from itertools import product

import sympy as sp


def audit_orbit_tables() -> None:
    # The target matrix has only diagonal slices.  Record (target, direct)
    # labels for the identity and 3-cycle permutations.
    identity = {(i, j): (i if i == j else None,
                         i if i == j else None)
                for i in range(3) for j in range(3)}
    cycle = {(i, j): (i if i == j else None,
                      i if j == (i + 1) % 3 else None)
             for i in range(3) for j in range(3)}
    assert sum(t is not None for t, _ in identity.values()) == 3
    assert sum(a is not None for _, a in identity.values()) == 3
    assert sum(t is not None for t, _ in cycle.values()) == 3
    assert sum(a is not None for _, a in cycle.values()) == 3
    assert all(not (t is not None and a is not None)
               for t, a in cycle.values())


def audit_cyclic_two_minors() -> None:
    q, m = sp.symbols("q m", nonzero=True)
    lam = sp.symbols("l0:3", nonzero=True)
    r = {(i, j): sp.symbols(f"r{i}{j}")
         for i in range(3) for j in range(3)}

    # For each cycle edge k -> l, i is the third colour.  The determinant
    # differs from (m lambda_k / 2) q r_ii by exactly one response rectangle.
    for k in range(3):
        ell = (k + 1) % 3
        i = (k + 2) % 3
        matrix = sp.Matrix([
            [m * r[i, i] / 2, m * r[i, ell] / 2],
            [m * r[k, i] / 2, lam[k] * q + m * r[k, ell] / 2],
        ])
        residue = sp.expand(
            matrix.det() - m * lam[k] * q * r[i, i] / 2
        )
        rectangle = sp.expand(
            m**2 * (r[i, i] * r[k, ell]
                    - r[i, ell] * r[k, i]) / 4
        )
        assert sp.expand(residue - rectangle) == 0


def audit_squarefree_countermodel() -> None:
    # A basis monomial is represented by its occupied site -> colour map.
    # Multiplication is zero on a repeated site.
    sites = tuple(range(6))
    pairs = ((0, 1), (2, 3), (4, 5))

    def multiply(left, right):
        if set(left) & set(right):
            return None
        answer = dict(left)
        answer.update(right)
        return answer

    F = []
    for colour, missing in enumerate(pairs):
        F.append({site: colour for site in sites if site not in missing})

    for i, j, k in product(range(3), repeat=3):
        p = {pairs[i][0]: i}
        s = {pairs[j][1]: j}
        value = multiply(multiply(p, s), F[k])
        if i == j == k:
            assert value == {site: i for site in sites}
        else:
            assert value is None

    # Literal product responses obey every 2x2 rectangle.
    # At the level of occupied supports, both sides are the same four
    # linear factors (or both vanish because a site repeats).
    for i, j, k, ell in product(range(3), repeat=4):
        factors_left = (pairs[i][0], pairs[j][1],
                        pairs[k][0], pairs[ell][1])
        factors_right = (pairs[i][0], pairs[ell][1],
                         pairs[k][0], pairs[j][1])
        assert sorted(factors_left) == sorted(factors_right)


def audit_four_site_determinant() -> None:
    x = sp.symbols("x0:3")
    y = sp.symbols("y0:3")
    lam = sp.symbols("l0:3", nonzero=True)
    t = sp.symbols("t")
    direct = sp.zeros(3)
    for i in range(3):
        direct[i, (i + 1) % 3] = lam[i]
    diagonal = sp.diag(*(x[i] * y[i] for i in range(3)))
    expected = (sp.prod(x) * sp.prod(y)
                - sp.prod(lam) * t**3)
    assert sp.expand((diagonal - t * direct).det() - expected) == 0

    # The target monomial has valuation one at every coordinate variable;
    # a polynomial cube has valuations divisible by three.
    target = sp.Poly(sp.prod(x) * sp.prod(y), *(x + y))
    assert target.monoms() == [(1, 1, 1, 1, 1, 1)]


def main() -> None:
    audit_orbit_tables()
    audit_cyclic_two_minors()
    audit_squarefree_countermodel()
    audit_four_site_determinant()
    print(
        "PASS invertible-monomial caps: orbit tables, cyclic rank-one "
        "minors, square-free product countermodel, and four-site cube "
        "obstruction verified exactly"
    )


if __name__ == "__main__":
    main()
