#!/usr/bin/env python3
"""Symbolically test the exceptional complex dense diagonal collision base.

Run with ``uv run --with sympy python ...``.  This is a discovery script;
once a solution is found, a separate verifier should hard-code it.
"""

from __future__ import annotations

import itertools

import sympy as sp


X, Y, Z = range(3)
N = 6
EDGES = tuple(itertools.combinations(range(N), 2))


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for position, v in enumerate(vertices[1:], 1):
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield ((u, v),) + tail


MATCHINGS = tuple(perfect_matchings(range(N)))


def base():
    I = sp.I
    H = sp.Matrix(((1, 1), (1, -1)))
    scalar = (-1 + I) / 4
    matrices = (
        scalar * H,
        sp.diag(I, 1) * H,
        sp.diag(-I, 1) * H * sp.diag(I, 1),
    )
    blocks = ((0, 1), (2, 3), (4, 5))
    q0 = {}
    for matrix, (left, right) in zip(matrices, itertools.combinations(blocks, 2)):
        for i, u in enumerate(left):
            for j, v in enumerate(right):
                q0[(u, v, X, X)] = sp.expand(matrix[i, j])
    for edge in blocks:
        q0[edge + (Y, Y)] = sp.Integer(1)
    return q0


def coefficient(q0, coloring):
    return sp.expand(
        sum(
            sp.prod(q0.get((u, v, coloring[u], coloring[v]), 0) for u, v in matching)
            for matching in MATCHINGS
        )
    )


def first_variables():
    return tuple(
        (u, v, a, b)
        for u, v in EDGES
        for a, b in ((Z, X), (Z, Y), (X, Z), (Y, Z))
    )


def first_system(q0):
    variables = first_variables()
    index = {key: position for position, key in enumerate(variables)}
    rows, target = [], []
    for coloring in itertools.product(range(3), repeat=N):
        if coloring.count(Z) != 1:
            continue
        row = [sp.Integer(0)] * len(variables)
        for matching in MATCHINGS:
            for exceptional, (u, v) in enumerate(matching):
                key = (u, v, coloring[u], coloring[v])
                if key not in index:
                    continue
                value = sp.Integer(1)
                for position, (a, b) in enumerate(matching):
                    if position != exceptional:
                        value *= q0.get((a, b, coloring[a], coloring[b]), 0)
                row[index[key]] += value
        rows.append(row)
        target.append(int(Y not in coloring))
    return variables, sp.Matrix(rows), sp.Matrix(target)


def z_vertex(vector, variables):
    support = set()
    for coefficient_value, (u, v, a, b) in zip(vector, variables):
        if coefficient_value:
            support.add(u if a == Z else v)
    assert len(support) == 1
    return support.pop()


def main():
    q0 = base()
    for coloring in itertools.product((X, Y), repeat=N):
        target = 2 if coloring == (X,) * N else int(coloring == (Y,) * N)
        assert sp.simplify(coefficient(q0, coloring) - target) == 0
    print("verified base")

    variables, first_matrix, first_target = first_system(q0)
    basis = first_matrix.nullspace()
    basis.sort(key=lambda vector: z_vertex(vector, variables))
    assert first_matrix.rank() == 54 and len(basis) == 6
    particular = sp.Matrix(
        [
            q0.get((u, v, X, X), sp.Integer(0)) / 2
            if (a, b) in ((Z, X), (X, Z))
            else 0
            for u, v, a, b in variables
        ]
    )
    assert all(sp.simplify(value) == 0 for value in first_matrix * particular - first_target)
    print("verified first rank=54 nullity=6")

    theta = sp.symbols("t0:6")
    q2_variables = sp.symbols("c0:15")
    q1 = particular + sp.Matrix.hstack(*basis) * sp.Matrix(theta)
    variable_index = {key: position for position, key in enumerate(variables)}
    equations = []
    for coloring in itertools.product((X, Y, Z), repeat=N):
        if coloring.count(Z) != 2:
            continue
        value = sp.Integer(0)
        for matching in MATCHINGS:
            for exceptional, edge in enumerate(matching):
                u, v = edge
                if (coloring[u], coloring[v]) != (Z, Z):
                    continue
                term = q2_variables[EDGES.index(edge)]
                for position, (a, b) in enumerate(matching):
                    if position != exceptional:
                        term *= q0.get((a, b, coloring[a], coloring[b]), 0)
                value += term
            for first, second in itertools.combinations(range(3), 2):
                remaining = 3 - first - second
                a, b = matching[remaining]
                term = q0.get((a, b, coloring[a], coloring[b]), 0)
                for position in (first, second):
                    u, v = matching[position]
                    index = variable_index.get((u, v, coloring[u], coloring[v]))
                    if index is None:
                        term = 0
                        break
                    term *= q1[index]
                value += term
        equations.append(sp.expand(value - int(Y not in coloring)))

    monomials = list(q2_variables) + list(theta) + [
        theta[i] * theta[j] for i in range(6) for j in range(i, 6)
    ] + [sp.Integer(1)]
    rows = []
    for equation in equations:
        polynomial = sp.Poly(equation, *q2_variables, *theta)
        row = []
        for monomial in monomials:
            powers = sp.Poly(monomial, *q2_variables, *theta).monoms()[0]
            row.append(polynomial.coeff_monomial(powers))
        rows.append(row)
    reduced, pivots = sp.Matrix(rows).rref()
    nonzero_rows = [list(reduced.row(i)) for i in range(reduced.rows) if any(reduced.row(i))]
    eliminated = [row for row in nonzero_rows if not any(row[:15])]
    print("second ranks", len(nonzero_rows), len(eliminated))
    assert len(nonzero_rows) >= 15
    product_equations = []
    for row in eliminated:
        expression = sp.expand(sum(a * b for a, b in zip(row, monomials)))
        product_equations.append(expression)
        print("constraint", sp.factor(expression))

    solutions = sp.solve(product_equations, theta, dict=True)
    print("theta solutions", solutions)
    assert solutions
    chosen_theta = solutions[0]
    specialized = [sp.simplify(equation.subs(chosen_theta)) for equation in equations]
    q2_solution = sp.linsolve(specialized, q2_variables)
    print("q2", q2_solution)
    assert q2_solution is not sp.EmptySet


if __name__ == "__main__":
    main()
