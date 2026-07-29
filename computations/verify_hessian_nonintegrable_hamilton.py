#!/usr/bin/env python3
"""Exact audit of the nonintegrable Hamilton Hessian countermodel."""

from __future__ import annotations

from itertools import combinations
from math import factorial


def term(n, i, a, j, b, value=1):
    colors = [-1] * n
    colors[i], colors[j] = a, b
    return {tuple(colors): value}


def add(*polys):
    out = {}
    for poly in polys:
        for key, value in poly.items():
            out[key] = out.get(key, 0) + value
            if not out[key]:
                del out[key]
    return out


def multiply(left, right):
    out = {}
    for x, a in left.items():
        for y, b in right.items():
            if any(xi >= 0 and yi >= 0 for xi, yi in zip(x, y)):
                continue
            key = tuple(xi if xi >= 0 else yi for xi, yi in zip(x, y))
            out[key] = out.get(key, 0) + a * b
    return {key: value for key, value in out.items() if value}


def power(poly, exponent, n):
    out = {(-1,) * n: 1}
    for _ in range(exponent):
        out = multiply(out, poly)
    return out


def hamilton_source(n):
    p0 = tuple((i, i + 1) for i in range(0, n, 2))
    p1 = tuple((i, i + 1) for i in range(1, n - 1, 2)) + ((0, n - 1),)
    source = {}
    for i, j in p0:
        source = add(source, term(n, i, 0, j, 0))
    for i, j in p1:
        source = add(source, term(n, i, 1, j, 1))
    return source


def restrict_edges(poly, removed):
    return {
        key: value
        for key, value in poly.items()
        if all(key[v] < 0 for v in removed)
    }


def cell_supported(poly, i, a, j, b):
    probe = next(iter(term(len(next(iter(poly))), i, a, j, b)))
    return probe in poly


def all_pair_extra_kernel(n, source):
    m = n // 2
    vertices = tuple(range(n))
    for u, v in combinations(vertices, 2):
        remaining = [x for x in vertices if x not in (u, v)]
        if (u - v) % 2:
            parity = 0 if sum(x % 2 == 0 for x in remaining) >= 2 else 1
            i, j = [x for x in remaining if x % 2 == parity][:2]
        else:
            parity = u % 2
            i = next(x for x in remaining if x % 2 == parity)
            j = next(x for x in remaining if x % 2 != parity)

        internal = restrict_edges(source, {u, v})
        choices = [(a, b) for a in range(2) for b in range(2)]
        a, b = next(
            pair
            for pair in choices
            if not cell_supported(internal, i, pair[0], j, pair[1])
        )
        z = term(n, i, a, j, b)
        assert not multiply(z, power(internal, m - 2, n))


def audit(n):
    m = n // 2
    source = hamilton_source(n)
    assert power(source, m, n) == {
        (0,) * n: factorial(m),
        (1,) * n: factorial(m),
    }
    assert len(source) == n
    all_pair_extra_kernel(n, source)

    internal = restrict_edges(source, {4, 5})
    z = add(term(n, 0, 1, 2, 1), term(n, 1, 0, 3, 0))

    alpha = [-1, 0, 1] + [0] * (n - 3)
    gauge_terms = []
    for key, value in source.items():
        occupied = [i for i, color in enumerate(key) if color >= 0]
        scalar = alpha[occupied[0]] + alpha[occupied[1]]
        gauge_terms.append({key: scalar * value} if scalar else {})
    tangent = add(z, add(*gauge_terms))

    assert sum(alpha) == 0
    assert sum(alpha[i] for i in range(n) if i not in (4, 5)) == 0
    assert not multiply(tangent, power(source, m - 1, n))
    internal_tangent = restrict_edges(tangent, {4, 5})
    assert not multiply(internal_tangent, power(internal, m - 2, n))

    key01 = next(iter(term(n, 0, 0, 1, 0)))
    assert source[key01] == 1 and tangent[key01] == -1

    gamma = tuple(1 if i in (0, 2) else 0 for i in range(n))
    obstruction = multiply(
        multiply(tangent, tangent), power(source, m - 2, n)
    )
    assert obstruction[gamma] == 2 * factorial(m - 2)

    derivative_power = power(source, m - 1, n)
    for i, j in combinations(range(n), 2):
        for a in range(2):
            for b in range(2):
                derivative = multiply(term(n, i, a, j, b), derivative_power)
                assert derivative.get(gamma, 0) == 0

    second_order = (m * (m - 1) // 2) * obstruction[gamma]
    assert second_order == factorial(m)
    print(
        f"n={n}: exact Delta_2, {n} cells, all {n*(n-1)//2} pair Hessians "
        f"extra-degenerate, obstruction={second_order}"
    )


def main():
    for n in (6, 8, 10):
        audit(n)
    print("verified full tangent is nonintegrable at second order")


if __name__ == "__main__":
    main()
