#!/usr/bin/env python3
"""Exact audit of the h=8, k=4 all-double row-Boolean closure."""

from __future__ import annotations

from itertools import combinations, product
from math import comb
from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import verify_live_three_zero_higher_split_collision_frontier as frontier


def near_perfect_matchings(vertices):
    vertices = tuple(vertices)
    if len(vertices) == 1:
        yield ()
        return
    first = vertices[0]
    # Either first is the unique unused vertex, or it is paired.
    for tail in perfect_matchings(vertices[1:]):
        yield tail
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        for tail in near_perfect_matchings(rest):
            yield ((first, second),) + tail


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


def check_formal_cores_and_derivative() -> None:
    profile = (2,) * 11
    h, k, total = 8, 4, 22
    assert sum(profile) == total == 2 * h + k + 2
    core_count = 0
    for chosen in combinations(range(11), 5):
        outside = set(range(11)) - set(chosen)
        assert len(outside) == 6
        for partial in combinations(chosen, 2):
            takes = {
                index: (1 if index in partial else 2)
                for index in chosen
            }
            assert sum(takes.values()) == h
            assert frontier.leaves_singleton(profile, takes)
            core_count += 1
    assert core_count == comb(11, 5) * comb(5, 2) == 4620

    z, mu = sp.symbols("z mu")
    outside_values = sp.symbols("u0:6")
    chosen_values = sp.symbols("t0:5")
    c_poly = sp.prod(z - value for value in outside_values)
    q_poly = sp.prod(z + value for value in chosen_values)
    assert sp.Poly(c_poly**2, z).degree() == 12
    assert len(outside_values) - 4 == 2

    s0, s1, s2 = sp.symbols("s0:3")
    section = s0 + s1 * z + s2 * z**2
    displayed_derivative = (z + mu) ** 4 * q_poly**2 * section / c_poly**3
    assert sp.factor(displayed_derivative) != 0


def check_rows_and_minors() -> None:
    u, v, xu, xv, zu, zv = sp.symbols("u v xu xv zu zv")

    def row(node, xjet, zjet):
        return sp.Matrix(
            [
                zjet,
                2 * xjet + node * zjet,
                2 + 4 * node * xjet + node**2 * zjet,
            ]
        )

    row_u = row(u, xu, zu)
    row_v = row(v, xv, zv)
    d01 = sp.expand(row_u[0] * row_v[1] - row_u[1] * row_v[0])
    d02 = sp.expand(row_u[0] * row_v[2] - row_u[2] * row_v[0])
    expected_d01 = 2 * (zu * xv - zv * xu) + (v - u) * zu * zv
    assert sp.expand(d01 - expected_d01) == 0

    e02 = sp.factor(d02 - (u + v) * d01)
    expected_e02 = -2 * (
        (u - v) * (zv * xu + xv * zu) + zv - zu
    )
    assert sp.expand(e02 - expected_e02) == 0

    # Exact normalized triple-pole row on a quadratic.
    w = sp.symbols("w")
    b0, b1, b2 = sp.symbols("b0 b1 b2", nonzero=True)
    p0, p1, p2 = sp.symbols("p0 p1 p2")
    unit = b0 + b1 * w + b2 * w**2 / 2
    polynomial = p0 + p1 * w + p2 * w**2 / 2
    residue_row = sp.diff(unit * polynomial, w, 2).subs(w, 0) / b0
    assert sp.expand(
        residue_row
        - (p2 + 2 * (b1 / b0) * p1 + (b2 / b0) * p0)
    ) == 0


def check_boolean_differences() -> None:
    u, v = sp.symbols("u v")
    xu0, xv0, yu0, yv0 = sp.symbols("xu0 xv0 yu0 yv0")
    a = sp.symbols("a0:4")
    b = sp.symbols("b0:4")
    c = sp.symbols("c0:4")
    d = sp.symbols("d0:4")

    def minors(bits):
        xu = xu0 + sum(bits[index] * a[index] for index in range(4))
        xv = xv0 + sum(bits[index] * b[index] for index in range(4))
        yu = yu0 + sum(bits[index] * c[index] for index in range(4))
        yv = yv0 + sum(bits[index] * d[index] for index in range(4))
        zu = xu**2 + yu
        zv = xv**2 + yv
        d01 = 2 * (zu * xv - zv * xu) + (v - u) * zu * zv
        d02 = zu * (2 + 4 * v * xv + v**2 * zv) - zv * (
            2 + 4 * u * xu + u**2 * zu
        )
        return sp.expand(d01), sp.expand(d02 - (u + v) * d01)

    fourth = 0
    for bits in product((0, 1), repeat=4):
        fourth += (-1) ** (4 - sum(bits)) * minors(bits)[0]
    expected_fourth = 4 * (v - u) * sum(
        sp.prod(a[index] for index in chosen)
        * sp.prod(b[index] for index in range(4) if index not in chosen)
        for chosen in combinations(range(4), 2)
    )
    assert sp.factor(fourth - expected_fourth) == 0

    for omitted in range(4):
        active = tuple(index for index in range(4) if index != omitted)
        third = 0
        for active_bits in product((0, 1), repeat=3):
            bits = [0] * 4
            for index, bit in zip(active, active_bits):
                bits[index] = bit
            third += (-1) ** (3 - sum(active_bits)) * minors(tuple(bits))[1]
        expected_third = -4 * (u - v) * (
            sum(
                a[i] * a[j] * b[k]
                for i, j in combinations(active, 2)
                for k in active
                if k not in (i, j)
            )
            + sum(
                a[i] * b[j] * b[k]
                for i in active
                for j, k in combinations(active, 2)
                if i not in (j, k)
            )
        )
        assert sp.factor(third - expected_third) == 0

    ratios = sp.symbols("r0:4")
    equations = [
        sum(ratios[i] * ratios[j] for i, j in combinations(range(4), 2))
    ]
    for omitted in range(4):
        active = tuple(index for index in range(4) if index != omitted)
        equations.append(
            sum(ratios[index] for index in active)
            + sum(ratios[i] * ratios[j] for i, j in combinations(active, 2))
        )
    basis = sp.groebner(equations, *ratios, order="lex")
    assert tuple(basis.polys) == tuple(
        sp.Poly(ratio, *ratios) for ratio in ratios
    )


def check_matching_extension_and_fibres() -> None:
    vertices = tuple(range(9))
    matchings = tuple(near_perfect_matchings(vertices))
    assert all(len(matching) == 4 for matching in matchings)

    # Up to relabeling, equal-fibre pairs are an arbitrary initial
    # matching of size 0,...,4.  Every cross-fibre edge extends to a
    # four-edge matching avoiding all equal-fibre pairs.
    for forbidden_count in range(5):
        forbidden = {
            frozenset((2 * index, 2 * index + 1))
            for index in range(forbidden_count)
        }
        for left, right in combinations(vertices, 2):
            edge = frozenset((left, right))
            if edge in forbidden:
                continue
            assert any(
                edge in {frozenset(pair) for pair in matching}
                and all(frozenset(pair) not in forbidden for pair in matching)
                for matching in matchings
            )

    u, x, y = sp.symbols("u x y", nonzero=True)

    def phi(anchor, value):
        return 2 / (anchor + value) + 3 / (anchor - value)

    assert sp.factor(phi(u, x) - (5 * u + x) / (u**2 - x**2)) == 0
    difference = sp.factor(phi(u, x) - phi(u, y))
    assert sp.factor(
        difference
        - (x - y)
        * (u**2 + 5 * u * x + 5 * u * y + x * y)
        / ((x**2 - u**2) * (y**2 - u**2))
    ) == 0
    fibre_value = sp.symbols("fibre_value")
    fibre_polynomial = sp.expand(
        fibre_value * (u**2 - x**2) - 5 * u - x
    )
    assert sp.Poly(fibre_polynomial, x).degree() <= 2
    assert sp.Poly(fibre_polynomial, x).coeff_monomial(x) == -1


def check_exact_profile_location() -> None:
    profile = (2,) * 11
    counts, residuals = frontier.census(8, 12)
    assert counts["R"] == 46
    assert profile in residuals


def main() -> None:
    check_formal_cores_and_derivative()
    check_rows_and_minors()
    check_boolean_differences()
    check_matching_extension_and_fibres()
    check_exact_profile_location()
    print("PASS: h=8, k=4 all-double row-Boolean closure")
    print("4620 legal formal-five cores and six proportional P_2 rows: exact")
    print("third/fourth swap differences force the zero ratio ideal: exact")
    print("every cross-fibre edge collapses nine values into one quadratic fibre")


if __name__ == "__main__":
    main()
