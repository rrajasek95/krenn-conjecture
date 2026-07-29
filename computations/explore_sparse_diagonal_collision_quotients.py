#!/usr/bin/env python3
"""Exact pair-quotient audit for a sparse six-site collision base.

The base has a single y perfect matching and x cross-block matrices

    2 [[1, 1], [1, -1]],  [[1, 1], [-2, 2]],  [[1, 0], [0, 0]].

It realizes ``2 X + Y``.  This script computes the complete homogeneous
one-z tangent kernels, eliminates every direct zz coefficient from the
full binary-complement pair equations, and optionally computes a Groebner
basis in the remaining tangent coordinates.
"""

from __future__ import annotations

import argparse
import itertools
from fractions import Fraction

import sympy as sp

from verify_color_collision_n_plus_two import (
    X,
    Y,
    nullspace,
    perfect_matchings,
    sector_system,
    weighted_matchings,
)


N = 6
VERTICES = tuple(range(N))
EDGES = tuple(itertools.combinations(VERTICES, 2))
MATCHINGS = tuple(perfect_matchings(VERTICES))
BLOCKS = ((0, 1), (2, 3), (4, 5))
BLOCK_PAIRS = ((0, 1), (0, 2), (1, 2))
X_BLOCKS = (
    ((2, 2), (2, -2)),
    ((1, 1), (-2, 2)),
    ((1, 0), (0, 0)),
)


def binary_base():
    q0 = {}
    for (left_index, right_index), matrix in zip(BLOCK_PAIRS, X_BLOCKS):
        left, right = BLOCKS[left_index], BLOCKS[right_index]
        for row, u in enumerate(left):
            for column, v in enumerate(right):
                value = Fraction(matrix[row][column])
                if value:
                    q0[(u, v, X, X)] = value
    for edge in BLOCKS:
        q0[edge + (Y, Y)] = Fraction(1)
    return q0


def verify_base(q0):
    for coloring in itertools.product((X, Y), repeat=N):
        value = weighted_matchings(q0, VERTICES, coloring)
        target = (
            Fraction(2)
            if coloring == (X,) * N
            else Fraction(1)
            if coloring == (Y,) * N
            else Fraction(0)
        )
        assert value == target, (coloring, value, target)


def tangent_data(q0):
    """Return tangent symbols and their sparse cell coefficient forms."""
    symbols = []
    sectors = {}
    cell_forms = {}
    dimensions = []
    for site in VERTICES:
        columns, matrix, _ = sector_system(N, q0, site)
        kernel = nullspace(matrix)
        dimensions.append(len(kernel))
        site_symbols = tuple(sp.symbols(f"t{site}_0:{len(kernel)}"))
        symbols.extend(site_symbols)
        sectors[site] = (columns, kernel, site_symbols)
        for column_index, (other, color) in enumerate(columns):
            cell_forms[(site, other, color)] = sp.Add(
                *(
                    sp.Rational(vector[column_index].numerator, vector[column_index].denominator)
                    * parameter
                    for vector, parameter in zip(kernel, site_symbols)
                )
            )
    return tuple(symbols), sectors, cell_forms, tuple(dimensions)


def complement_cofactor(q0, first, second, coloring):
    remaining = tuple(v for v in VERTICES if v not in (first, second))
    return weighted_matchings(q0, remaining, coloring)


def hessian_component(q0, cell_forms, first, second, coloring):
    """Return the fixed-pair component of 1/2 d^2 H(K,K)."""
    total = sp.Integer(0)
    for matching in MATCHINGS:
        first_edge = next(edge for edge in matching if first in edge)
        second_edge = next(edge for edge in matching if second in edge)
        if first_edge == second_edge:
            continue
        first_other = first_edge[0] if first_edge[1] == first else first_edge[1]
        second_other = second_edge[0] if second_edge[1] == second else second_edge[1]
        first_form = cell_forms[(first, first_other, coloring[first_other])]
        second_form = cell_forms[(second, second_other, coloring[second_other])]
        if first_form == 0 or second_form == 0:
            continue
        base_edge = next(
            edge for edge in matching if edge not in (first_edge, second_edge)
        )
        base_value = q0.get(
            (base_edge[0], base_edge[1], coloring[base_edge[0]], coloring[base_edge[1]]),
            Fraction(0),
        )
        if base_value:
            total += sp.sympify(base_value) * first_form * second_form
    return sp.expand(total)


def primitive(expression):
    if not sp.sympify(expression).free_symbols:
        value = sp.Rational(expression)
        return sp.Integer(1 if value > 0 else -1)
    polynomial = sp.Poly(sp.expand(expression))
    _, value = polynomial.clear_denoms(convert=True)
    content, value = sp.Poly(value).primitive()
    expression = sp.expand(value.as_expr())
    leading = sp.Poly(expression).LC()
    return -expression if leading < 0 else expression


def quotient_equations(q0, cell_forms):
    """Eliminate the one direct zz scalar separately in every pair sector."""
    equations = []
    reports = []
    for first, second in EDGES:
        rows = []
        for tail in itertools.product((X, Y), repeat=N - 2):
            coloring = {}
            cursor = iter(tail)
            for vertex in VERTICES:
                if vertex not in (first, second):
                    coloring[vertex] = next(cursor)
            cofactor = complement_cofactor(q0, first, second, coloring)
            hessian = hessian_component(q0, cell_forms, first, second, coloring)
            target = Fraction(1, 2) if all(value == X for value in tail) else Fraction(0)
            residual = hessian - sp.Rational(target.numerator, target.denominator)
            rows.append((cofactor, residual, tail))

        pivot = next((row for row in rows if row[0]), None)
        pair_equations = []
        if pivot is None:
            pair_equations = [primitive(residual) for _, residual, _ in rows if residual != 0]
        else:
            pivot_cofactor, pivot_residual, _ = pivot
            for cofactor, residual, _ in rows:
                wedge = pivot_cofactor * residual - cofactor * pivot_residual
                if wedge != 0:
                    pair_equations.append(primitive(wedge))

        unique = []
        for equation in pair_equations:
            if equation not in unique and -equation not in unique:
                unique.append(equation)
        equations.extend(unique)
        reports.append(((first, second), pivot is not None, tuple(unique)))
    return tuple(equations), tuple(reports)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--groebner", action="store_true")
    args = parser.parse_args()

    q0 = binary_base()
    verify_base(q0)
    symbols, sectors, cell_forms, dimensions = tangent_data(q0)
    equations, reports = quotient_equations(q0, cell_forms)
    print(f"verified H(q0)=2X+Y; tangent dimensions={dimensions}")
    print(f"tangent variables={len(symbols)} quotient equations={len(equations)}")
    for pair, active, pair_equations in reports:
        print(
            f"pair={pair} cofactor={'nonzero' if active else 'zero'} "
            f"quotient_equations={len(pair_equations)}"
        )
        for equation in pair_equations:
            print("  ", sp.factor(equation))

    if args.groebner:
        basis = sp.groebner(equations, *symbols, order="grevlex")
        contains_one = basis.reduce(sp.Integer(1))[1] == 0
        print(f"Groebner basis size={len(basis.polys)} contains_one={contains_one}")
        for polynomial in basis.polys:
            print(sp.factor(polynomial.as_expr()))


if __name__ == "__main__":
    main()
