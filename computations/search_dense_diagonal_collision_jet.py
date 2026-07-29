#!/usr/bin/env python3
"""Probe a dense diagonal n=6 binary base for a collision two-jet.

This is a numerical falsification search, not a proof.  The displayed base
is exact over Q: its x-sector is supported on K_{2,2,2}, each cross-block
2x2 matrix has permanent zero, and its full hafnian is 2; the y-sector is
the three block edges.  We solve the first equations exactly (nullity six)
and optimize the complete second-jet system in those six kernel parameters
plus all fifteen Q2 entries.
"""

from __future__ import annotations

import argparse
import itertools
from fractions import Fraction

import numpy as np
from scipy.optimize import least_squares

from verify_color_collision_second_jet import (
    X,
    Y,
    Z,
    edges,
    first_system,
    perfect_matchings,
    rank_mod,
)


N = 6
EDGES = edges(N)
MATCHINGS = tuple(perfect_matchings(range(N)))


def dense_base():
    blocks = ((0, 1), (2, 3), (4, 5))
    hadamard = ((1, 1), (1, -1))
    q0 = {}
    for position, (left, right) in enumerate(itertools.combinations(blocks, 2)):
        scalar = Fraction(-1, 2) if position == 0 else Fraction(1)
        for i, u in enumerate(left):
            for j, v in enumerate(right):
                q0[(u, v, X, X)] = scalar * hadamard[i][j]
    for edge in blocks:
        q0[edge + (Y, Y)] = Fraction(1)
    return q0


def output_coefficient(q0, coloring):
    total = Fraction(0)
    for matching in MATCHINGS:
        term = Fraction(1)
        for u, v in matching:
            term *= q0.get((u, v, coloring[u], coloring[v]), 0)
        total += term
    return total


def nullspace(matrix):
    rows = [[Fraction(value) for value in row] for row in matrix]
    row = 0
    pivots = []
    columns = len(rows[0])
    for column in range(columns):
        pivot = next(
            (index for index in range(row, len(rows)) if rows[index][column]),
            None,
        )
        if pivot is None:
            continue
        rows[row], rows[pivot] = rows[pivot], rows[row]
        inverse = 1 / rows[row][column]
        rows[row] = [value * inverse for value in rows[row]]
        for index in range(len(rows)):
            if index == row or not rows[index][column]:
                continue
            multiple = rows[index][column]
            rows[index] = [
                left - multiple * right
                for left, right in zip(rows[index], rows[row])
            ]
        pivots.append(column)
        row += 1
    free = [column for column in range(columns) if column not in pivots]
    basis = []
    for free_column in free:
        vector = [Fraction(0)] * columns
        vector[free_column] = 1
        for pivot_row, pivot_column in enumerate(pivots):
            vector[pivot_column] = -rows[pivot_row][free_column]
        basis.append(vector)
    return basis, pivots


def build_problem():
    q0 = dense_base()
    for coloring in itertools.product((X, Y), repeat=N):
        expected = 2 if coloring == (X,) * N else int(coloring == (Y,) * N)
        assert output_coefficient(q0, coloring) == expected

    variables, matrix, target = first_system(N, q0)
    basis, pivots = nullspace(matrix)
    assert len(pivots) == 54 and len(basis) == 6

    def z_vertex(vector):
        support = set()
        for coefficient, (u, v, a, b) in zip(vector, variables):
            if not coefficient:
                continue
            support.add(u if a == Z else v)
        assert len(support) == 1
        return support.pop()

    basis.sort(key=z_vertex)
    assert [z_vertex(vector) for vector in basis] == list(range(N))

    # Half of the infinitesimal x -> z basis change is a canonical solution.
    particular = []
    for u, v, a, b in variables:
        if (a, b) == (Z, X):
            particular.append(q0.get((u, v, X, X), Fraction(0)) / 2)
        elif (a, b) == (X, Z):
            particular.append(q0.get((u, v, X, X), Fraction(0)) / 2)
        else:
            particular.append(Fraction(0))
    for row, rhs in zip(matrix, target):
        assert sum(a * b for a, b in zip(row, particular)) == rhs

    variable_index = {key: index for index, key in enumerate(variables)}
    colorings = tuple(
        coloring
        for coloring in itertools.product((X, Y, Z), repeat=N)
        if coloring.count(Z) == 2
    )
    return q0, variables, variable_index, particular, basis, colorings


Q0, VARIABLES, VARIABLE_INDEX, PARTICULAR, BASIS, COLORINGS = build_problem()
PARTICULAR_FLOAT = np.array(PARTICULAR, dtype=float)
BASIS_FLOAT = np.array(BASIS, dtype=float).T


def exact_quadratic_matrix():
    """Linearize the second equations in q2 and theta monomials."""
    kernel_count = len(BASIS)
    pairs = tuple(itertools.combinations_with_replacement(range(kernel_count), 2))
    pair_index = {pair: index for index, pair in enumerate(pairs)}
    forms = []
    for variable in range(len(VARIABLES)):
        forms.append(
            (PARTICULAR[variable], tuple(vector[variable] for vector in BASIS))
        )

    rows = []
    for coloring in COLORINGS:
        q2_part = [Fraction(0)] * len(EDGES)
        linear = [Fraction(0)] * kernel_count
        quadratic = [Fraction(0)] * len(pairs)
        constant = Fraction(-int(Y not in coloring))
        for matching in MATCHINGS:
            for position, edge in enumerate(matching):
                u, v = edge
                if (coloring[u], coloring[v]) != (Z, Z):
                    continue
                coefficient = Fraction(1)
                for other, (a, b) in enumerate(matching):
                    if other != position:
                        coefficient *= Q0.get(
                            (a, b, coloring[a], coloring[b]), 0
                        )
                q2_part[EDGES.index(edge)] += coefficient

            for first, second in itertools.combinations(range(3), 2):
                remaining = 3 - first - second
                a, b = matching[remaining]
                coefficient = Q0.get((a, b, coloring[a], coloring[b]), 0)
                if not coefficient:
                    continue
                selected = []
                for position in (first, second):
                    u, v = matching[position]
                    index = VARIABLE_INDEX.get((u, v, coloring[u], coloring[v]))
                    if index is None:
                        selected = []
                        break
                    selected.append(forms[index])
                if not selected:
                    continue
                (left_constant, left), (right_constant, right) = selected
                constant += coefficient * left_constant * right_constant
                for i in range(kernel_count):
                    linear[i] += coefficient * (
                        left_constant * right[i] + right_constant * left[i]
                    )
                    for j in range(i, kernel_count):
                        value = left[i] * right[j]
                        if i != j:
                            value += left[j] * right[i]
                        quadratic[pair_index[(i, j)]] += coefficient * value
        rows.append(q2_part + linear + quadratic + [constant])
    return rows


def row_space_basis(matrix):
    rows = [[Fraction(value) for value in row] for row in matrix]
    rank = 0
    for column in range(len(rows[0])):
        pivot = next(
            (index for index in range(rank, len(rows)) if rows[index][column]),
            None,
        )
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inverse = 1 / rows[rank][column]
        rows[rank] = [value * inverse for value in rows[rank]]
        for index in range(len(rows)):
            if index == rank or not rows[index][column]:
                continue
            multiple = rows[index][column]
            rows[index] = [
                left - multiple * right
                for left, right in zip(rows[index], rows[rank])
            ]
        rank += 1
    return rows[:rank]


def groebner_audit(rows):
    import sympy as sp

    theta = sp.symbols(f"t0:{len(BASIS)}")
    pairs = tuple(itertools.combinations_with_replacement(range(len(BASIS)), 2))
    reduced = row_space_basis(rows)
    equations = []
    for row in reduced:
        if any(row[: len(EDGES)]):
            continue
        offset = len(EDGES)
        expression = sum(
            sp.Rational(value.numerator, value.denominator) * theta[i]
            for i, value in enumerate(row[offset : offset + len(BASIS)])
        )
        offset += len(BASIS)
        expression += sum(
            sp.Rational(value.numerator, value.denominator) * theta[i] * theta[j]
            for (i, j), value in zip(pairs, row[offset : offset + len(pairs)])
        )
        expression += sp.Rational(row[-1].numerator, row[-1].denominator)
        equations.append(sp.factor(expression))
    print(f"eliminated Q2: {len(equations)} independent quadratic equations")
    for index, equation in enumerate(equations):
        print(f"eq{index} = {equation}")
    basis = sp.groebner(equations, *theta, order="grevlex")
    contains_one = basis.reduce(sp.Integer(1))[1] == 0
    print(f"Groebner basis size={len(basis.polys)} contains_one={contains_one}")
    for polynomial in basis.polys:
        print(sp.factor(polynomial.as_expr()))


def residual(parameters):
    theta = parameters[: len(BASIS)]
    q2 = parameters[len(BASIS) :]
    q1 = PARTICULAR_FLOAT + BASIS_FLOAT @ theta
    answer = []
    for coloring in COLORINGS:
        coefficient = 0.0
        for matching in MATCHINGS:
            # One Q2 edge and two Q0 edges.
            for position, (u, v) in enumerate(matching):
                if (coloring[u], coloring[v]) != (Z, Z):
                    continue
                term = q2[EDGES.index((u, v))]
                for other, (a, b) in enumerate(matching):
                    if other != position:
                        term *= float(Q0.get((a, b, coloring[a], coloring[b]), 0))
                coefficient += term

            # Two Q1 edges and one Q0 edge.
            for first, second in itertools.combinations(range(3), 2):
                remaining = 3 - first - second
                a, b = matching[remaining]
                term = float(Q0.get((a, b, coloring[a], coloring[b]), 0))
                if not term:
                    continue
                for position in (first, second):
                    u, v = matching[position]
                    index = VARIABLE_INDEX.get((u, v, coloring[u], coloring[v]))
                    if index is None:
                        term = 0.0
                        break
                    term *= q1[index]
                coefficient += term
        target = float(Y not in coloring)
        answer.append(coefficient - target)
    return np.array(answer)


def run(seed, max_evaluations):
    rng = np.random.default_rng(seed)
    initial = rng.normal(scale=0.25, size=len(BASIS) + len(EDGES))
    fit = least_squares(
        residual,
        initial,
        max_nfev=max_evaluations,
        ftol=1e-14,
        xtol=1e-14,
        gtol=1e-14,
    )
    error = residual(fit.x)
    print(
        f"seed={seed} cost={fit.cost:.12g} max={np.max(np.abs(error)):.6g} "
        f"norm={np.linalg.norm(fit.x):.6g} nfev={fit.nfev}"
    )
    if np.max(np.abs(error)) < 1e-8:
        print("parameters", repr(fit.x.tolist()))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--starts", type=int, default=8)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--max-evaluations", type=int, default=5000)
    parser.add_argument("--groebner", action="store_true")
    args = parser.parse_args()
    print("verified dense rational base; first rank=54, nullity=6")
    exact_rows = exact_quadratic_matrix()
    nonconstant_rank = rank_mod([row[:-1] for row in exact_rows])
    full_rank = rank_mod(exact_rows)
    print(
        f"second linearized polynomial rank={full_rank}; "
        f"without constant={nonconstant_rank}"
    )
    if args.groebner:
        groebner_audit(exact_rows)
    for offset in range(args.starts):
        run(args.seed + offset, args.max_evaluations)


if __name__ == "__main__":
    main()
