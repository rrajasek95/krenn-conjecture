#!/usr/bin/env python3
"""Exact audits for the collision cofactor/Bianchi hierarchy."""

from __future__ import annotations

import itertools
from fractions import Fraction

import verify_complete_normal_block_countermodel as normal


X, Y, Z = range(3)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position, partner in enumerate(vertices[1:], 1):
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield ((first, partner),) + tail


def source_polynomial(n, q0, tangent, direct, coloring):
    """Coefficient polynomial in t as a degree->Q dictionary."""
    answer = {}
    for matching in perfect_matchings(range(n)):
        polynomial = {0: Fraction(1)}
        for edge in matching:
            labels = tuple(coloring[vertex] for vertex in edge)
            cell = {}
            base = q0.get(edge + labels, 0)
            first = tangent.get(edge + labels, 0)
            second = direct.get(edge, 0) if labels == (Z, Z) else 0
            if base:
                cell[0] = Fraction(base)
            if first:
                cell[1] = Fraction(first)
            if second:
                cell[2] = Fraction(second)
            product = {}
            for left_degree, left_value in polynomial.items():
                for right_degree, right_value in cell.items():
                    degree = left_degree + right_degree
                    product[degree] = product.get(degree, 0) + left_value * right_value
            polynomial = product
        for degree, value in polynomial.items():
            answer[degree] = answer.get(degree, 0) + value
    return {degree: value for degree, value in answer.items() if value}


def half_shift_target(coloring):
    if all(label == Y for label in coloring):
        return {0: Fraction(1)}
    if any(label == Y for label in coloring):
        return {}
    count = coloring.count(Z)
    if count % 2:
        return {}
    return {count: Fraction(2, 2**count)}


def audit_four_site_normalization():
    n = 4
    minus = ((0, 1), (2, 3))
    plus = ((0, 2), (1, 3))
    y_matching = ((0, 3), (1, 2))
    q0, tangent, direct = {}, {}, {}
    for sign, matching in ((-1, minus), (1, plus)):
        for edge in matching:
            q0[edge + (X, X)] = Fraction(1)
            tangent[edge + (Z, X)] = Fraction(sign, 2)
            tangent[edge + (X, Z)] = Fraction(sign, 2)
            direct[edge] = Fraction(1, 4)
    for edge in y_matching:
        q0[edge + (Y, Y)] = Fraction(1)
    for coloring in itertools.product((X, Y, Z), repeat=n):
        assert source_polynomial(n, q0, tangent, direct, coloring) == half_shift_target(coloring)
    print("verified normalized Bianchi hierarchy on exact n=4 collision")


def audit_dormant_connection():
    n = 6
    q0 = {
        (0, 1, X, X): Fraction(2),
        (2, 3, X, X): Fraction(1),
        (4, 5, X, X): Fraction(1),
        (1, 2, Y, Y): Fraction(1),
        (3, 4, Y, Y): Fraction(1),
        (0, 5, Y, Y): Fraction(1),
    }
    tangent = {(1, 3, Z, X): Fraction(1)}
    zero_direct = {}
    live_direct = {(0, 2): Fraction(1)}

    # The binary base is 2X+Y, and the chosen same-shore tangent vanishes.
    for coloring in itertools.product((X, Y), repeat=n):
        expected = {0: Fraction(2)} if coloring == (X,) * n else (
            {0: Fraction(1)} if coloring == (Y,) * n else {}
        )
        assert source_polynomial(n, q0, tangent, zero_direct, coloring) == expected
    for coloring in itertools.product((X, Y, Z), repeat=n):
        if coloring.count(Z) == 1:
            assert source_polynomial(n, q0, tangent, zero_direct, coloring).get(1, 0) == 0

    # W_02 and K^2 are invisible through order two for every coloring.
    for coloring in itertools.product((X, Y, Z), repeat=n):
        left = source_polynomial(n, q0, tangent, zero_direct, coloring)
        right = source_polynomial(n, q0, tangent, live_direct, coloring)
        assert left.get(0, 0) == right.get(0, 0)
        assert left.get(1, 0) == right.get(1, 0)
        assert left.get(2, 0) == right.get(2, 0)

    marked = (Z, Z, Z, X, X, X)
    assert source_polynomial(n, q0, tangent, zero_direct, marked).get(3, 0) == 0
    assert source_polynomial(n, q0, tangent, live_direct, marked).get(3, 0) == 1
    print("verified second-order-dormant W_02 awakens with coefficient 1 at order 3")


def dense_third_coefficient(coloring, direct):
    return source_polynomial(
        normal.N, normal.Q0, normal.K, direct, coloring
    ).get(3, Fraction(0))


def audit_complete_normal_countermodel_bianchi():
    marked = (X, X, X, Z, Z, Z)
    base = dense_third_coefficient(marked, normal.ETA)
    assert base == Fraction(-255, 64)
    pure_invisible = ((0, 1), (2, 3), (4, 5))
    for edge in pure_invisible:
        changed = dict(normal.ETA)
        changed[edge] = Fraction(1)
        assert dense_third_coefficient(marked, changed) == base

    failures = []
    for coloring in itertools.product((X, Y, Z), repeat=normal.N):
        if coloring.count(Z) == 3:
            value = dense_third_coefficient(coloring, normal.ETA)
            if value:
                failures.append((coloring, value))
    assert len(failures) == 30
    print("verified scalar-normal countermodel has 30 third-order failures")
    print("marked Bianchi residual=-255/64 and is independent of three pure-invisible W cells")


def main():
    audit_four_site_normalization()
    audit_dormant_connection()
    audit_complete_normal_countermodel_bianchi()
    print("verified collision cofactor/Bianchi formulas exactly")


if __name__ == "__main__":
    main()
