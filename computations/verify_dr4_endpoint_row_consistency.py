#!/usr/bin/env python3
"""Cross-check the two independent DR4 endpoint-row constructions."""

from itertools import combinations
from math import prod

import sympy as sp


def phi(nodes, values):
    a, b, c = nodes
    A, B, C = values
    return (
        -(a - b) * (a - c) * (b - c) * A * B * C
        + (a - b) * (a + b - 2 * c) * A * B
        - (a - c) * (a - 2 * b + c) * A * C
        - (b - c) * (2 * a - b - c) * B * C
        - 2 * (b - c) * A
        + 2 * (a - c) * B
        - 2 * (a - b) * C
    )


def main() -> None:
    anchors = tuple(map(sp.Integer, (1, 2, 3, 6)))
    translations = sp.symbols("U0:4")
    for omitted, ti in enumerate(anchors):
        complement = tuple(index for index in range(4) if index != omitted)
        nodes = tuple(anchors[index] for index in complement)
        for sign in (1, -1):
            shifted = []
            diagonal = {}
            for index in complement:
                tj = anchors[index]
                shift = (
                    -sp.Rational(2, tj + ti)
                    if sign == 1
                    else -sp.Rational(1, tj + ti) - sp.Rational(1, tj - ti)
                )
                shifted.append(translations[index] + shift)
                derivative = sum(
                    sp.Rational(1, tj - anchors[k])
                    for k in complement
                    if k != index
                )
                diagonal[index] = derivative + shift

            direct = sp.Poly(sp.expand(phi(nodes, shifted)), *translations)
            leading_monomial = prod(
                translations[index] for index in complement
            )
            leading = direct.coeff_monomial(leading_monomial)
            direct = sp.expand(direct.as_expr() / leading)

            barycentric = prod(translations[index] for index in complement)
            for pair in combinations(complement, 2):
                remaining = next(index for index in complement if index not in pair)
                barycentric += diagonal[remaining] * prod(
                    translations[index] for index in pair
                )
            for index in complement:
                k, ell = (other for other in complement if other != index)
                barycentric += translations[index] * (
                    diagonal[k] * diagonal[ell]
                    + sp.Rational(1, (anchors[k] - anchors[ell]) ** 2)
                )
            assert sp.expand(direct - barycentric) == 0
    print("DR4 endpoint-row constructions agree exactly")


if __name__ == "__main__":
    main()
