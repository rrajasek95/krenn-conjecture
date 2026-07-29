#!/usr/bin/env python3
"""Exact audit for the fixed-rainbow-triangle cofactor obstruction.

The mathematical argument is in
``proofs/rainbow-triangle-cofactor-obstruction.md``.  This script checks the
support chart, its color-sensitive stabilizer, the three complementary
matching expansions, and the hypotheses used by the reusable CEGAR
detector.  It performs no floating-point computation.
"""

from __future__ import annotations

import itertools

import sympy as sp

from verify_color_sensitive_support_obstruction import (
    perfect_matchings,
    rainbow_triangle_cofactor_witness,
)


VERTICES = tuple(range(6))
COLORS = tuple(range(3))
EDGES = tuple(itertools.combinations(VERTICES, 2))


def rectangle(left, right):
    return set(itertools.product(left, right))


SUPPORTS = {
    (0, 1): rectangle((0,), COLORS),
    (0, 2): {(0, 0)},
    (0, 3): {(1, 1)},
    (0, 4): {(2, 2)},
    (0, 5): rectangle((0,), COLORS),
    (1, 2): rectangle(COLORS, COLORS),
    (1, 3): rectangle(COLORS, (2,)),
    (1, 4): {(1, 1)},
    (1, 5): rectangle(COLORS, COLORS),
    (2, 3): rectangle(COLORS, (2,)),
    (2, 4): rectangle(COLORS, (1,)),
    (2, 5): rectangle(COLORS, COLORS),
    (3, 4): {(0, 0)},
    (3, 5): {(2, 2)},
    (4, 5): rectangle((1,), COLORS),
}


def endpoint_support(edge, vertex):
    cells = SUPPORTS[edge]
    if vertex == edge[0]:
        return {row for row, _ in cells}
    assert vertex == edge[1]
    return {column for _, column in cells}


def audit_stabilizer():
    u, v, w = sp.symbols("u v w")
    alpha = (
        (0, 1 - u, 1 - w),
        (0, 0, 0),
        (0, 0, 0),
        (1 - v, u, 0),
        (v, 0, w),
        (0, 0, 0),
    )
    triangle = {(0, 3), (0, 4), (3, 4)}
    assert all(
        sp.simplify(sum(alpha[vertex][color] for vertex in VERTICES)) == 1
        for color in COLORS
    )
    for edge in EDGES:
        left, right = edge
        expected = 1 if edge in triangle else 0
        for row, column in SUPPORTS[edge]:
            assert sp.simplify(alpha[left][row] + alpha[right][column]) == expected
    return triangle


def audit_complementary_cofactors(triangle):
    expected_colors = {(0, 3): 1, (0, 4): 2, (3, 4): 0}
    for edge, target_color in expected_colors.items():
        complement = tuple(sorted(set(VERTICES) - set(edge)))
        matchings = tuple(perfect_matchings(complement))
        assert len(matchings) == 3
        assert all(len(matching) == 2 for matching in matchings)

        # Every complementary matching monomial is nonzero on this support.
        for matching in matchings:
            assert all(SUPPORTS[pair] for pair in matching)

        if edge != (3, 4):
            continue

        # For H_{0125}, all three terms share e_0 at vertex 0.  After that
        # factor is removed, their supports in the order (1,2,5) are
        # (full,full,full), (full,e_0,full), (full,full,full).
        ordered = ((0, 1), (2, 5)), ((0, 2), (1, 5)), ((0, 5), (1, 2))
        local = []
        for matching in ordered:
            local.append(
                tuple(
                    endpoint_support(
                        next(pair for pair in matching if vertex in pair), vertex
                    )
                    for vertex in complement
                )
            )
        full = set(COLORS)
        assert local == [
            ({0}, full, full, full),
            ({0}, full, {0}, full),
            ({0}, full, full, full),
        ]
        # Quotient mode 2 first; the two surviving pure tensors must become
        # proportional in modes 1 and 5.  Their common mode-1 support is not
        # the target axis, and the middle term has non-target support at 5.
        assert local[1][2] == {target_color}
        assert local[0][2] != {target_color}
        assert local[2][2] != {target_color}
        assert local[0][1] == local[2][1] != {target_color}
        assert local[1][3] != {target_color}

    witness = rainbow_triangle_cofactor_witness(SUPPORTS, set())
    assert witness is not None
    detected_triangle, detected_edge, center, singled, reason = witness
    assert set(detected_triangle) == triangle
    assert detected_edge in triangle
    assert reason in {"unequal", "two-quotient"}
    print(
        "reusable detector found rainbow triangle:",
        sorted(detected_triangle),
        "cofactor", detected_edge,
        "center", center,
        "term", singled,
        "reason", reason,
    )


def main():
    assert set(SUPPORTS) == set(EDGES)
    triangle = audit_stabilizer()
    audit_complementary_cofactors(triangle)
    print("exact stabilizer and three complementary matching expansions verified")
    print("H_0125 satisfies the support hypotheses of the two-quotient lemma")


if __name__ == "__main__":
    main()
