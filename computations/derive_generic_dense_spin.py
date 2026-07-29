#!/usr/bin/env python3
"""Derive generic spin-product constraints for the dense diagonal n=6 chart.

This symbolic discovery script works over Q(x,y,z).  Run with SymPy via
``uv run --with sympy python computations/derive_generic_dense_spin.py``.
"""

from __future__ import annotations

import argparse
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


def build_base():
    x, y, z = sp.symbols("x y z", nonzero=True)
    H = sp.Matrix(((1, 1), (1, -1)))
    matrices = (
        H,
        sp.diag(x, 1) * H,
        sp.diag(y, 1) * H * sp.diag(z, 1),
    )
    blocks = ((0, 1), (2, 3), (4, 5))
    q0 = {}
    for matrix, (left, right) in zip(matrices, itertools.combinations(blocks, 2)):
        for i, u in enumerate(left):
            for j, v in enumerate(right):
                q0[(u, v, X, X)] = matrix[i, j]
    for edge in blocks:
        q0[edge + (Y, Y)] = sp.Integer(1)

    full = sum(
        sp.prod(q0.get((u, v, X, X), 0) for u, v in matching)
        for matching in MATCHINGS
    )
    scale = sp.factor(2 / full)
    for u in blocks[0]:
        for v in blocks[1]:
            q0[(u, v, X, X)] = sp.factor(scale * q0[(u, v, X, X)])
    assert sp.factor(
        sum(
            sp.prod(q0.get((u, v, X, X), 0) for u, v in matching)
            for matching in MATCHINGS
        ) - 2
    ) == 0
    return (x, y, z), sp.factor(full), q0


def first_affine(q0, vertex):
    variables = []
    for other in range(N):
        if other == vertex:
            continue
        edge = (min(vertex, other), max(vertex, other))
        for other_color in (X, Y):
            colors = (Z, other_color) if vertex < other else (other_color, Z)
            variables.append(edge + colors)
    index = {key: position for position, key in enumerate(variables)}
    rows, target = [], []
    for tail in itertools.product((X, Y), repeat=N - 1):
        coloring = list(tail)
        coloring.insert(vertex, Z)
        row = [sp.Integer(0)] * len(variables)
        for matching in MATCHINGS:
            exceptional = next(
                position for position, edge in enumerate(matching) if vertex in edge
            )
            u, v = matching[exceptional]
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
    matrix = sp.Matrix(rows)
    kernel = matrix.nullspace()
    assert len(kernel) == 1
    particular = sp.Matrix(
        [q0.get((u, v, X, X), sp.Integer(0)) / 2 if Y not in (a, b) else 0
         for u, v, a, b in variables]
    )
    assert all(sp.factor(value) == 0 for value in matrix * particular - sp.Matrix(target))
    return {key: (particular[i], kernel[0][i]) for i, key in enumerate(variables)}


def pair_constraint(q0, forms, u, v, allow_multiple=False):
    tu, tv, c = sp.symbols(f"t{u} t{v} c")
    features = (c, tu, tv, tu * tv, sp.Integer(1))
    rows = []
    remaining = [w for w in range(N) if w not in (u, v)]
    for tail in itertools.product((X, Y), repeat=4):
        coloring = [None] * N
        coloring[u] = coloring[v] = Z
        for w, color in zip(remaining, tail):
            coloring[w] = color
        value = sp.Integer(0)
        for matching in MATCHINGS:
            for exceptional, edge in enumerate(matching):
                a, b = edge
                if (coloring[a], coloring[b]) != (Z, Z):
                    continue
                term = c
                for position, (r, s) in enumerate(matching):
                    if position != exceptional:
                        term *= q0.get((r, s, coloring[r], coloring[s]), 0)
                value += term
            for first, second in itertools.combinations(range(3), 2):
                remaining_position = 3 - first - second
                a, b = matching[remaining_position]
                term = q0.get((a, b, coloring[a], coloring[b]), 0)
                for position in (first, second):
                    r, s = matching[position]
                    form = forms.get((r, s, coloring[r], coloring[s]))
                    if form is None:
                        term = 0
                        break
                    parameter = tu if Z == coloring[u] and u in (r, s) else tv
                    term *= form[0] + parameter * form[1]
                value += term
        value -= int(Y not in coloring)
        polynomial = sp.Poly(sp.cancel(value), c, tu, tv)
        row = []
        for feature in features:
            powers = sp.Poly(feature, c, tu, tv).monoms()[0]
            row.append(polynomial.coeff_monomial(powers))
        rows.append(row)
    reduced, _ = sp.Matrix(rows).rref()
    eliminated = []
    for index in range(reduced.rows):
        row = list(reduced.row(index))
        if any(row) and row[0] == 0:
            eliminated.append(sp.factor(sum(a * b for a, b in zip(row, features))))
    if allow_multiple:
        return eliminated
    assert len(eliminated) == 1, (u, v, eliminated)
    equation = eliminated[0]
    coefficient = sp.factor(sp.Poly(equation, tu, tv).coeff_monomial(tu * tv))
    constant = sp.factor(equation.subs({tu: 0, tv: 0}))
    assert coefficient != 0
    return sp.factor(-constant / coefficient), equation


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--x-i", action="store_true")
    parser.add_argument("--x-minus-i", action="store_true")
    parser.add_argument("--y-minus-i", action="store_true")
    parser.add_argument("--z-i", action="store_true")
    args = parser.parse_args()
    parameters, full, q0 = build_base()
    special_x = sp.I if args.x_i else -sp.I if args.x_minus_i else None
    if special_x is not None:
        substitution = {parameters[0]: special_x}
        if args.y_minus_i:
            substitution[parameters[1]] = -sp.I
        if args.z_i:
            substitution[parameters[2]] = sp.I
        parameters = tuple(parameter for parameter in parameters if parameter not in substitution)
        full = sp.factor(full.subs(substitution))
        q0 = {key: sp.factor(value.subs(substitution)) for key, value in q0.items()}
    print("unnormalized hafnian", full)
    forms = {}
    for vertex in range(N):
        forms.update(first_affine(q0, vertex))
        print("first kernel", vertex, "done")
    constants = {}
    for edge in EDGES:
        if special_x is not None:
            constraints = pair_constraint(q0, forms, *edge, allow_multiple=True)
            print(edge, "constraints=", [sp.factor(value) for value in constraints])
            continue
        constants[edge], equation = pair_constraint(q0, forms, *edge)
        print(edge, "product=", sp.factor(constants[edge]))

    if special_x is not None:
        return

    tetrads = {
        "A": constants[(0, 1)] * constants[(2, 4)]
             - constants[(0, 2)] * constants[(1, 4)],
        "B": constants[(2, 3)] * constants[(0, 4)]
             - constants[(0, 2)] * constants[(3, 4)],
        "C": constants[(4, 5)] * constants[(0, 2)]
             - constants[(0, 4)] * constants[(2, 5)],
    }
    for name, value in tetrads.items():
        print("tetrad", name, sp.factor(value))

    all_tetrads = []
    for a, b, c, d in itertools.combinations(range(N), 4):
        def value(i, j):
            return constants[(min(i, j), max(i, j))]
        all_tetrads.extend((
            sp.factor(value(a, b) * value(c, d) - value(a, c) * value(b, d)),
            sp.factor(value(a, b) * value(c, d) - value(a, d) * value(b, c)),
        ))
    numerators = list({sp.factor(sp.together(value).as_numer_denom()[0])
                       for value in all_tetrads if value != 0})
    nonzero_factors = [full]
    nonzero_factors.extend(
        sp.together(value).as_numer_denom()[0] for value in constants.values()
    )
    nonzero_factors.extend(
        sp.together(value).as_numer_denom()[1] for value in constants.values()
    )
    localization = sp.factor(sp.prod(nonzero_factors))
    inverse = sp.symbols("inverse")
    print("computing saturated tetrad ideal", len(numerators), "generators")
    groebner = sp.groebner(
        numerators + [inverse * localization - 1], inverse, *parameters,
        order="grevlex",
    )
    print("saturated contains one", groebner.reduce(sp.Integer(1))[1] == 0)


if __name__ == "__main__":
    main()
