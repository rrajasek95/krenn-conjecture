#!/usr/bin/env python3
"""Exact audit for ``notes/cross-pair-pencil-cancellation.md``.

The rational binary Delta_(8,2) source is capped by the all-colors product
covector at two genuinely different pairs, 12 and 13.  After the specified
boundary alignment, this script enumerates all 64 coefficient polynomials
of H_6(A+tB), verifies the three-row formula in the note, computes the mixed
gcd, and checks both clean roots and the final diagonal normalization.
"""

from __future__ import annotations

import itertools
import sys
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from verify_n8_pair_cap_obstruction import (  # noqa: E402
    VERTICES,
    edge_entry,
    matching_tensor,
    source,
)


def product_cap_degree_two(edges, p, q):
    boundary = tuple(vertex for vertex in VERTICES if vertex not in (p, q))
    scalar = sp.factor(
        sum(
            edge_entry(edges, p, q, i, j)
            for i, j in itertools.product(range(2), repeat=2)
        )
    )
    degree_two = {}
    for u, v in itertools.combinations(boundary, 2):
        matrix = {}
        for color_u, color_v in itertools.product(range(2), repeat=2):
            value = scalar * edge_entry(edges, u, v, color_u, color_v)
            value += sum(
                edge_entry(edges, p, u, i, color_u)
                * edge_entry(edges, q, v, j, color_v)
                + edge_entry(edges, p, v, i, color_v)
                * edge_entry(edges, q, u, j, color_u)
                for i, j in itertools.product(range(2), repeat=2)
            )
            value = sp.factor(value)
            if value != 0:
                matrix[color_u, color_v] = value
        if matrix:
            degree_two[u, v] = matrix
    return scalar, boundary, degree_two


def canonicalize(boundary, family):
    position = {vertex: index for index, vertex in enumerate(boundary)}
    answer = {}
    for (u, v), matrix in family.items():
        answer[position[u], position[v]] = dict(matrix)
    return answer


def permute_sites(family, permutation):
    """Old abstract site i is sent to permutation[i], retaining endpoint order."""

    answer = {}
    for (u, v), matrix in family.items():
        new_u, new_v = permutation[u], permutation[v]
        if new_u < new_v:
            answer[new_u, new_v] = dict(matrix)
        else:
            answer[new_v, new_u] = {
                (color_v, color_u): value
                for (color_u, color_v), value in matrix.items()
            }
    return answer


def linear_combination(left, right, parameter):
    answer = {}
    for edge in set(left) | set(right):
        matrix = {}
        for cell in set(left.get(edge, {})) | set(right.get(edge, {})):
            value = sp.factor(
                left.get(edge, {}).get(cell, 0)
                + parameter * right.get(edge, {}).get(cell, 0)
            )
            if value != 0:
                matrix[cell] = value
        if matrix:
            answer[edge] = matrix
    return answer


def normalize_at_site_zero(family, scales):
    answer = {}
    for (u, v), matrix in family.items():
        transformed = {}
        for (color_u, color_v), value in matrix.items():
            if u == 0:
                value *= scales[color_u]
            elif v == 0:
                value *= scales[color_v]
            transformed[color_u, color_v] = sp.factor(value)
        answer[u, v] = transformed
    return answer


def main() -> None:
    edges = source()
    assert matching_tensor(VERTICES, edges) == {
        (0,) * 8: sp.S.One,
        (1,) * 8: sp.S.One,
    }

    scalar_a, boundary_a, raw_a = product_cap_degree_two(edges, 1, 2)
    scalar_b, boundary_b, raw_b = product_cap_degree_two(edges, 1, 3)
    assert scalar_a == 2
    assert scalar_b == -1
    assert boundary_a == (3, 4, 5, 6, 7, 8)
    assert boundary_b == (2, 4, 5, 6, 7, 8)

    family_a = canonicalize(boundary_a, raw_a)
    family_b = permute_sites(
        canonicalize(boundary_b, raw_b),
        (0, 1, 3, 2, 4, 5),
    )

    assert matching_tensor(tuple(range(6)), family_a) == {
        (0,) * 6: 4,
        (1, 0, 1, 1, 1, 1): 2,
        (1,) * 6: 4,
    }
    assert matching_tensor(tuple(range(6)), family_b) == {
        (0,) * 6: 1,
        (1, 0, 1, 1, 1, 1): -1,
        (1,) * 6: 1,
    }

    t = sp.symbols("t")
    pencil = linear_combination(family_a, family_b, t)
    tensor = matching_tensor(tuple(range(6)), pencil)
    expected = {
        (0,) * 6: sp.factor((t + 1) * (t**2 + 4)),
        (1,) * 6: sp.factor((t - 2) * (8 * t**2 - 7 * t - 16) / 8),
        (1, 0, 1, 1, 1, 1): sp.factor(
            -(t - 2) * (t + 2) * (2 * t + 1) / 2
        ),
    }
    assert tensor == expected

    mixed_polynomials = [
        sp.Poly(value, t, domain=sp.QQ)
        for coloring, value in tensor.items()
        if coloring not in ((0,) * 6, (1,) * 6)
    ]
    mixed_gcd = mixed_polynomials[0]
    for polynomial in mixed_polynomials[1:]:
        mixed_gcd = sp.gcd(mixed_gcd, polynomial)
    assert sp.monic(mixed_gcd.as_expr(), t) == sp.expand(
        (t - 2) * (t + 2) * (t + sp.Rational(1, 2))
    )

    clean_values = {
        -2: (-8, -15),
        -sp.Rational(1, 2): (sp.Rational(17, 8), sp.Rational(105, 32)),
    }
    for root, pure_values in clean_values.items():
        specialized = {
            coloring: sp.factor(value.subs(t, root))
            for coloring, value in tensor.items()
            if value.subs(t, root) != 0
        }
        assert specialized == {
            (0,) * 6: pure_values[0],
            (1,) * 6: pure_values[1],
        }

    combined = linear_combination(family_a, family_b, -2)
    normalized = normalize_at_site_zero(
        combined,
        (sp.Rational(-1, 8), sp.Rational(-1, 15)),
    )
    assert matching_tensor(tuple(range(6)), normalized) == {
        (0,) * 6: sp.S.One,
        (1,) * 6: sp.S.One,
    }

    print("two dirty cross-pair caps and cubic pencil identity: PASS")
    print("clean roots t=-2 and t=-1/2; normalized t=-2 tensor: Delta_(6,2)")


if __name__ == "__main__":
    main()
