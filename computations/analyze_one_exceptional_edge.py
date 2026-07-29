#!/usr/bin/env python3
"""Exact diagnostics for the two residual one-exceptional-edge charts."""

from __future__ import annotations

import itertools
import math

import sympy as sp


VERTICES = tuple(range(6))
COLORS = tuple(range(3))


def perfect_matchings(vertices):
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for v in vertices[1:]:
        rest = tuple(x for x in vertices if x not in (u, v))
        for matching in perfect_matchings(rest):
            yield ((u, v),) + matching


MATCHINGS = tuple(perfect_matchings(VERTICES))

CHARTS = {
    "same": (
        {"00", "01", "02", "11", "21"},
        {
            (0, 2): ("012", "012"),
            (0, 3): ("0", "1"),
            (0, 4): ("0", "0"),
            (0, 5): ("012", "2"),
            (1, 2): ("012", "012"),
            (1, 3): ("1", "1"),
            (1, 4): ("1", "0"),
            (1, 5): ("012", "2"),
            (2, 3): ("012", "1"),
            (2, 4): ("012", "0"),
            (2, 5): ("2", "2"),
            (3, 4): ("2", "2"),
            (3, 5): ("0", "0"),
            (4, 5): ("1", "1"),
        },
    ),
    "different": (
        {"00", "01", "02", "12", "22"},
        {
            (0, 2): ("0", "2"),
            (0, 3): ("012", "012"),
            (0, 4): ("012", "1"),
            (0, 5): ("0", "0"),
            (1, 2): ("2", "2"),
            (1, 3): ("012", "012"),
            (1, 4): ("012", "1"),
            (1, 5): ("2", "0"),
            (2, 3): ("2", "012"),
            (2, 4): ("0", "0"),
            (2, 5): ("1", "1"),
            (3, 4): ("1", "1"),
            (3, 5): ("012", "0"),
            (4, 5): ("2", "2"),
        },
    ),
    "full-after-odd-cuts": (
        {f"{i}{j}" for i in COLORS for j in COLORS},
        {
            (0, 2): ("012", "2"),
            (0, 3): ("012", "012"),
            (0, 4): ("1", "1"),
            (0, 5): ("012", "0"),
            (1, 2): ("012", "2"),
            (1, 3): ("012", "012"),
            (1, 4): ("012", "1"),
            (1, 5): ("0", "0"),
            (2, 3): ("2", "2"),
            (2, 4): ("0", "0"),
            (2, 5): ("1", "1"),
            (3, 4): ("012", "1"),
            (3, 5): ("012", "0"),
            (4, 5): ("2", "2"),
        },
    ),
}


def chart_data(name):
    exceptional_support, factor_supports = CHARTS[name]
    keys = [("A", int(cell[0]), int(cell[1])) for cell in sorted(exceptional_support)]
    for edge, (at_u, at_v) in factor_supports.items():
        keys.extend(("f", edge, 0, int(color)) for color in at_u)
        keys.extend(("f", edge, 1, int(color)) for color in at_v)
    key_index = {key: index for index, key in enumerate(keys)}

    def exponent(coloring, matching):
        answer = [0] * len(keys)
        for u, v in matching:
            if (u, v) == (0, 1):
                answer[key_index[("A", coloring[0], coloring[1])]] += 1
            else:
                answer[key_index[("f", (u, v), 0, coloring[u])]] += 1
                answer[key_index[("f", (u, v), 1, coloring[v])]] += 1
        return tuple(answer)

    fibers = []
    for coloring in itertools.product(COLORS, repeat=6):
        monomials = []
        for matching in MATCHINGS:
            supported = all(
                (
                    f"{coloring[u]}{coloring[v]}" in exceptional_support
                    if (u, v) == (0, 1)
                    else coloring[u] in map(int, factor_supports[u, v][0])
                    and coloring[v] in map(int, factor_supports[u, v][1])
                )
                for u, v in matching
            )
            if supported:
                monomials.append(exponent(coloring, matching))
        target = int(len(set(coloring)) == 1)
        if monomials:
            fibers.append((coloring, tuple(monomials), target))
    return keys, fibers


def primitive_integer_vector(vector):
    denominator_lcm = sp.ilcm(*(entry.q for entry in vector))
    entries = [int(entry * denominator_lcm) for entry in vector]
    divisor = math.gcd(*entries)
    return tuple(entry // divisor for entry in entries)


def main():
    for name in CHARTS:
        keys, fibers = chart_data(name)
        binomial_fibers = [
            (coloring, monomials)
            for coloring, monomials, target in fibers
            if target == 0 and len(monomials) == 2
        ]
        differences = sp.Matrix(
            [
                [a - b for a, b in zip(monomials[0], monomials[1], strict=True)]
                for _, monomials in binomial_fibers
            ]
        )
        kernel = differences.T.nullspace()
        print(name, "variables", len(keys), "binomials", len(binomial_fibers), "rank", differences.rank())
        for basis_vector in kernel:
            integer_vector = primitive_integer_vector(basis_vector)
            if sum(integer_vector) % 2:
                used = [
                    (binomial_fibers[index][0], coefficient)
                    for index, coefficient in enumerate(integer_vector)
                    if coefficient
                ]
                print("ODD RELATION", used)
                break
        else:
            print("no odd relation in rational-kernel basis")


if __name__ == "__main__":
    main()
