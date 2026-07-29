#!/usr/bin/env python3
"""Exact all-covector six-boundary obstruction over every odd field.

The rational binary n=8 source from ``verify_n8_pair_cap_obstruction.py``
realizes GHZ exactly.  On capping the tensor-active pair 13 by the general
covector K=(k_ij), put s=<K,X_13>, let X be the old six-site edge family,
and let R_K be the first-jet family.  If the usual pair-cap absorption were
clean, Y=X+R_K/s would realize the capped target.  After clearing the cubic
denominator this is

    H_6(sX+R_K) = s^2 (k00 e0^6 + k11 e1^6).

The script proves that the difference has exactly one nonzero coefficient,

    [101111] difference = -k10^2*k11 = -s^2*kappa_1.

Thus no covector with s*kappa_0*kappa_1 nonzero is clean.  The source is
defined over Z[1/2], and the displayed obstruction has coefficient -1, so
the certificate remains valid after every odd-characteristic base change
and after every field extension.
"""

from __future__ import annotations

import itertools
import sympy as sp

from verify_n8_pair_cap_obstruction import (
    VERTICES,
    edge_entry,
    matching_tensor,
    source,
)


def main() -> None:
    edges = source()
    assert matching_tensor(VERTICES, edges) == {
        (0,) * 8: sp.S.One,
        (1,) * 8: sp.S.One,
    }

    p, q = 1, 3
    remaining = tuple(v for v in VERTICES if v not in (p, q))
    assert remaining == (2, 4, 5, 6, 7, 8)
    k00, k01, k10, k11 = sp.symbols("k00 k01 k10 k11")
    cap = ((k00, k01), (k10, k11))

    s = sp.factor(sum(
        cap[i][j] * edge_entry(edges, p, q, i, j)
        for i, j in itertools.product(range(2), repeat=2)
    ))
    assert s == -k10

    # The edge is tensor-active: deleting its endpoints leaves a nonzero
    # matching tensor (equivalently, its source cofactor is nonzero).
    internal = {
        edge: dict(matrix)
        for edge, matrix in edges.items()
        if edge[0] in remaining and edge[1] in remaining
    }
    assert matching_tensor(remaining, internal)

    first_jet = {}
    for a, b in itertools.combinations(remaining, 2):
        matrix = {}
        for ca, cb in itertools.product(range(2), repeat=2):
            value = sp.factor(sum(
                cap[i][j] * (
                    edge_entry(edges, p, a, i, ca)
                    * edge_entry(edges, q, b, j, cb)
                    + edge_entry(edges, p, b, i, cb)
                    * edge_entry(edges, q, a, j, ca)
                )
                for i, j in itertools.product(range(2), repeat=2)
            ))
            if value != 0:
                matrix[ca, cb] = value
        if matrix:
            first_jet[a, b] = matrix

    assert first_jet == {
        (2, 4): {(0, 0): k00 + k10},
        (2, 5): {(1, 1): k11 / 2},
        (2, 6): {(1, 1): k11},
        (4, 5): {(0, 1): k10 / 2},
        (4, 6): {(0, 1): k10},
    }

    # Clear the denominator in Y=X+R/s by writing Z=sX+R.  Since the
    # six-site hafnian is cubic, cleanliness is H_6(Z)=s^2*cap(target).
    z = {}
    for edge in set(internal) | set(first_jet):
        matrix = {}
        for cell in set(internal.get(edge, {})) | set(first_jet.get(edge, {})):
            value = sp.factor(
                s * internal.get(edge, {}).get(cell, 0)
                + first_jet.get(edge, {}).get(cell, 0)
            )
            if value != 0:
                matrix[cell] = value
        if matrix:
            z[edge] = matrix

    actual = matching_tensor(remaining, z)
    expected = {
        (0,) * 6: sp.factor(s**2 * k00),
        (1,) * 6: sp.factor(s**2 * k11),
    }
    difference = {
        coloring: sp.factor(actual.get(coloring, 0) - expected.get(coloring, 0))
        for coloring in set(actual) | set(expected)
    }
    difference = {coloring: value for coloring, value in difference.items() if value != 0}
    assert difference == {(1, 0, 1, 1, 1, 1): -k10**2 * k11}
    assert difference[(1, 0, 1, 1, 1, 1)] == -s**2 * k11

    print("verified exact binary Delta_(8,2) source over Z[1/2]")
    print("pair 13: s =", s, "; kappa_0 =", k00, "; kappa_1 =", k11)
    print("cleared clean-cap defect [101111] =", -s**2 * k11)
    print("no nondegenerate covector cap over any odd-characteristic extension")


if __name__ == "__main__":
    main()
