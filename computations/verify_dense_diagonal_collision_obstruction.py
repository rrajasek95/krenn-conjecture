#!/usr/bin/env python3
"""Exact certificate for the dense diagonal collision obstruction at n=6."""

from __future__ import annotations

import itertools
from fractions import Fraction

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
PAIRS = tuple(itertools.combinations_with_replacement(range(N), 2))


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


def rref(matrix):
    rows = [[Fraction(value) for value in row] for row in matrix]
    rank = 0
    pivots = []
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
        pivots.append(column)
        rank += 1
    return rows[:rank], pivots


def nullspace(matrix):
    reduced, pivots = rref(matrix)
    columns = len(matrix[0])
    free = [column for column in range(columns) if column not in pivots]
    basis = []
    for free_column in free:
        vector = [Fraction(0)] * columns
        vector[free_column] = 1
        for row, pivot_column in enumerate(pivots):
            vector[pivot_column] = -reduced[row][free_column]
        basis.append(vector)
    return basis, pivots


def first_family(q0):
    variables, matrix, target = first_system(N, q0)
    basis, pivots = nullspace(matrix)
    assert len(pivots) == 54 and len(basis) == 6
    assert rank_mod(matrix) == 54

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
    for vector in basis:
        for row in matrix:
            assert sum(a * b for a, b in zip(row, vector)) == 0
    assert rank_mod([[vector[i] for vector in basis] for i in range(len(variables))]) == 6
    return variables, particular, basis


def quadratic_rows(q0, variables, particular, basis):
    variable_index = {key: index for index, key in enumerate(variables)}
    pair_index = {pair: index for index, pair in enumerate(PAIRS)}
    forms = [
        (particular[index], tuple(vector[index] for vector in basis))
        for index in range(len(variables))
    ]
    colorings = tuple(
        coloring
        for coloring in itertools.product((X, Y, Z), repeat=N)
        if coloring.count(Z) == 2
    )
    assert len(colorings) == 240
    rows = []
    for coloring in colorings:
        q2_part = [Fraction(0)] * len(EDGES)
        linear = [Fraction(0)] * N
        quadratic = [Fraction(0)] * len(PAIRS)
        constant = Fraction(-int(Y not in coloring))
        for matching in MATCHINGS:
            for position, edge in enumerate(matching):
                u, v = edge
                if (coloring[u], coloring[v]) != (Z, Z):
                    continue
                coefficient = Fraction(1)
                for other, (a, b) in enumerate(matching):
                    if other != position:
                        coefficient *= q0.get(
                            (a, b, coloring[a], coloring[b]), 0
                        )
                q2_part[EDGES.index(edge)] += coefficient

            for first, second in itertools.combinations(range(3), 2):
                remaining = 3 - first - second
                a, b = matching[remaining]
                coefficient = q0.get((a, b, coloring[a], coloring[b]), 0)
                if not coefficient:
                    continue
                selected = []
                for position in (first, second):
                    u, v = matching[position]
                    index = variable_index.get((u, v, coloring[u], coloring[v]))
                    if index is None:
                        selected = []
                        break
                    selected.append(forms[index])
                if not selected:
                    continue
                (left_constant, left), (right_constant, right) = selected
                constant += coefficient * left_constant * right_constant
                for i in range(N):
                    linear[i] += coefficient * (
                        left_constant * right[i] + right_constant * left[i]
                    )
                    for j in range(i, N):
                        value = left[i] * right[j]
                        if i != j:
                            value += left[j] * right[i]
                        quadratic[pair_index[(i, j)]] += coefficient * value
        rows.append(q2_part + linear + quadratic + [constant])
    return rows


def polynomial_add(*polynomials):
    answer = {}
    for polynomial, scalar in polynomials:
        for monomial, coefficient in polynomial.items():
            answer[monomial] = answer.get(monomial, 0) + scalar * coefficient
            if not answer[monomial]:
                del answer[monomial]
    return answer


def polynomial_multiply(left, right):
    answer = {}
    for a, coefficient_a in left.items():
        for b, coefficient_b in right.items():
            monomial = tuple(x + y for x, y in zip(a, b))
            answer[monomial] = answer.get(monomial, 0) + coefficient_a * coefficient_b
    return {monomial: value for monomial, value in answer.items() if value}


def variable(index):
    exponent = [0] * N
    exponent[index] = 1
    return {tuple(exponent): Fraction(1)}


def product_equation(i, j, sign):
    exponent = [0] * N
    exponent[i] += 1
    exponent[j] += 1
    return {tuple(exponent): Fraction(4), (0,) * N: Fraction(-sign)}


def main():
    q0 = dense_base()
    for coloring in itertools.product((X, Y), repeat=N):
        target = 2 if coloring == (X,) * N else int(coloring == (Y,) * N)
        assert output_coefficient(q0, coloring) == target
    variables, particular, basis = first_family(q0)
    rows = quadratic_rows(q0, variables, particular, basis)
    reduced, pivots = rref(rows)
    assert len(reduced) == 30
    assert pivots[: len(EDGES)] == list(range(len(EDGES)))

    eliminated = [row for row in reduced if not any(row[: len(EDGES)])]
    assert len(eliminated) == 15
    signs = {
        (0, 1): 1, (0, 2): 1, (0, 3): 1, (0, 4): -1, (0, 5): -1,
        (1, 2): 1, (1, 3): 1, (1, 4): -1, (1, 5): -1,
        (2, 3): 1, (2, 4): 1, (2, 5): 1,
        (3, 4): 1, (3, 5): 1, (4, 5): 1,
    }
    expected = []
    feature_count = len(EDGES) + N + len(PAIRS) + 1
    pair_index = {pair: index for index, pair in enumerate(PAIRS)}
    for pair, sign in signs.items():
        row = [Fraction(0)] * feature_count
        row[len(EDGES) + N + pair_index[pair]] = 1
        row[-1] = Fraction(-sign, 4)
        expected.append(row)
    assert eliminated == expected

    f01 = product_equation(0, 1, 1)
    f02 = product_equation(0, 2, 1)
    f14 = product_equation(1, 4, -1)
    f24 = product_equation(2, 4, 1)
    a = polynomial_add((f01, 1), (f02, -1))
    b = polynomial_add((f14, 1), (f24, -1))
    bracket = polynomial_add(
        (polynomial_multiply(variable(0), b), 1),
        (polynomial_multiply(variable(4), a), -1),
    )
    certificate = polynomial_add(
        (polynomial_multiply(variable(1), bracket), 2),
        (f01, -1),
    )
    assert certificate == {(0,) * N: Fraction(1)}

    print("verified dense rational base H=2X+Y on all 64 binary colorings")
    print("verified exhaustive first family: rank=54, nullity=6")
    print("verified 240-equation elimination to 4*t_i*t_j=epsilon_ij")
    print("verified four-equation Nullstellensatz certificate 1")


if __name__ == "__main__":
    main()
