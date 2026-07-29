#!/usr/bin/env python3
"""Symbolic certificate on the first boundary of the dense diagonal chart.

The y-sector is the matching 01|23|45.  The xx cross-blocks have permanent
zero.  Up to vertex/block swaps and diagonal rescaling, the open support
boundary (one block is a two-edge star and the other two are dense) is

    P=(-2*r/D) [[1,1],[0,0]], Q=[[1,1],[1,-1]],
    R=[[r,s],[t,-s*t/r]], D=r^2-r*s+r*t+s*t.

This script derives the complete local first-jet fibers over the relevant
rational-function fields and checks the pair-sector second-jet identities
used in the accompanying note.  It also checks the two rank-drop divisors
separately, without specializing them to numerical points.
"""

from __future__ import annotations

import itertools

import sympy as sp


X, Y, Z = range(3)
N = 6
BLOCKS = ((0, 1), (2, 3), (4, 5))


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position, second in enumerate(vertices[1:], 1):
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


MATCHINGS = tuple(perfect_matchings(range(N)))


def build_base(r, s, t):
    D = sp.factor(r**2 - r * s + r * t + s * t)
    matrices = (
        sp.Matrix(((sp.factor(-2 * r / D), sp.factor(-2 * r / D)), (0, 0))),
        sp.Matrix(((1, 1), (1, -1))),
        sp.Matrix(((r, s), (t, sp.factor(-s * t / r)))),
    )
    q0 = {}
    for matrix, (left, right) in zip(
        matrices, itertools.combinations(BLOCKS, 2)
    ):
        for i, u in enumerate(left):
            for j, v in enumerate(right):
                q0[(u, v, X, X)] = matrix[i, j]
    for edge in BLOCKS:
        q0[edge + (Y, Y)] = sp.Integer(1)
    return D, q0


def output_coefficient(q0, coloring):
    return sp.factor(
        sum(
            sp.prod(q0.get((u, v, coloring[u], coloring[v]), 0)
                    for u, v in matching)
            for matching in MATCHINGS
        )
    )


def local_first_affine(q0, vertex, stem):
    variables = []
    for other in range(N):
        if other == vertex:
            continue
        edge = (min(vertex, other), max(vertex, other))
        for other_color in (X, Y):
            colors = ((Z, other_color) if vertex < other
                      else (other_color, Z))
            variables.append(edge + colors)
    index = {key: position for position, key in enumerate(variables)}

    rows, target = [], []
    for tail in itertools.product((X, Y), repeat=N - 1):
        coloring = list(tail)
        coloring.insert(vertex, Z)
        row = [sp.Integer(0)] * len(variables)
        for matching in MATCHINGS:
            exceptional = next(
                i for i, edge in enumerate(matching) if vertex in edge
            )
            u, v = matching[exceptional]
            key = (u, v, coloring[u], coloring[v])
            if key not in index:
                continue
            coefficient = sp.Integer(1)
            for position, (a, b) in enumerate(matching):
                if position != exceptional:
                    coefficient *= q0.get(
                        (a, b, coloring[a], coloring[b]), 0
                    )
            row[index[key]] += coefficient
        rows.append(row)
        target.append(int(Y not in coloring))

    matrix = sp.Matrix(rows)
    kernel = matrix.nullspace()
    parameters = sp.symbols(f"{stem}_0:{len(kernel)}")
    particular = sp.Matrix([
        q0.get((u, v, X, X), 0) / 2
        if (a, b) in ((Z, X), (X, Z)) else 0
        for u, v, a, b in variables
    ])
    assert all(
        sp.factor(value) == 0
        for value in matrix * particular - sp.Matrix(target)
    )
    forms = {
        key: sp.factor(
            particular[i]
            + sum(parameters[j] * kernel[j][i] for j in range(len(kernel)))
        )
        for i, key in enumerate(variables)
    }
    return matrix.rank(), parameters, forms


def all_first_forms(q0):
    forms = {}
    parameters = {}
    ranks = []
    for vertex in range(N):
        rank, parameters[vertex], local = local_first_affine(
            q0, vertex, f"a{vertex}"
        )
        ranks.append(rank)
        forms.update(local)
    return tuple(ranks), parameters, forms


def pair_rows(q0, parameters, forms, u, v):
    direct = sp.symbols(f"c{u}{v}")
    local = parameters[u] + parameters[v]
    bilinears = tuple(
        left * right
        for left in parameters[u]
        for right in parameters[v]
    )
    features = (direct,) + local + bilinears + (sp.Integer(1),)
    rows = []
    remaining = [w for w in range(N) if w not in (u, v)]
    for tail in itertools.product((X, Y), repeat=N - 2):
        coloring = [None] * N
        coloring[u] = coloring[v] = Z
        for w, color in zip(remaining, tail):
            coloring[w] = color
        value = sp.Integer(-int(Y not in coloring))
        for matching in MATCHINGS:
            for exceptional, (a, b) in enumerate(matching):
                if (coloring[a], coloring[b]) != (Z, Z):
                    continue
                term = direct
                for position, (r, s) in enumerate(matching):
                    if position != exceptional:
                        term *= q0.get(
                            (r, s, coloring[r], coloring[s]), 0
                        )
                value += term
            for first, second in itertools.combinations(range(3), 2):
                a, b = matching[3 - first - second]
                term = q0.get((a, b, coloring[a], coloring[b]), 0)
                for position in (first, second):
                    r, s = matching[position]
                    term *= forms.get(
                        (r, s, coloring[r], coloring[s]), 0
                    )
                value += term
        polynomial = sp.Poly(sp.cancel(value), direct, *local)
        rows.append([
            polynomial.coeff_monomial(
                sp.Poly(feature, direct, *local).monoms()[0]
            )
            for feature in features
        ])
    return features, sp.Matrix(rows)


def eliminated_pair_equations(q0, parameters, forms, u, v):
    features, matrix = pair_rows(q0, parameters, forms, u, v)
    reduced, _ = matrix.rref()
    equations = []
    for row in range(reduced.rows):
        if any(reduced.row(row)) and reduced[row, 0] == 0:
            equations.append(sp.factor(sum(
                coefficient * feature
                for coefficient, feature in zip(reduced.row(row), features)
            )))
    return equations


def all_x_pair_residual(q0, parameters, forms, u, v):
    features, matrix = pair_rows(q0, parameters, forms, u, v)
    # itertools orders the all-x tail first.
    return sp.factor(sum(
        coefficient * feature
        for coefficient, feature in zip(matrix.row(0), features)
    ))


def verify_support_classification():
    entries = ((0, 0), (0, 1), (1, 0), (1, 1))
    for support_bits in itertools.product((0, 1), repeat=4):
        support = {
            entry for entry, present in zip(entries, support_bits) if present
        }
        # A support can carry nonzero weights with permanent zero iff neither
        # of the two permanent monomials is supported.
        admissible = not (
            {(0, 0), (1, 1)} <= support
            or {(0, 1), (1, 0)} <= support
        )
        if admissible and len(support) >= 2:
            rows = {i for i, _ in support}
            columns = {j for _, j in support}
            assert len(rows) == 1 or len(columns) == 1


def generic_open_boundary():
    r, s, t = sp.symbols("r s t", nonzero=True)
    D, q0 = build_base(r, s, t)
    for coloring in itertools.product((X, Y), repeat=N):
        expected = 2 if coloring == (X,) * N else int(coloring == (Y,) * N)
        assert sp.factor(output_coefficient(q0, coloring) - expected) == 0

    ranks, parameters, forms = all_first_forms(q0)
    assert ranks == (8, 9, 9, 9, 9, 9)
    a00, a01 = parameters[0]
    (a10,) = parameters[1]
    (a40,) = parameters[4]
    (a50,) = parameters[5]

    pair01 = eliminated_pair_equations(q0, parameters, forms, 0, 1)
    expected01 = (a00 * a10, a01 * a10 - sp.Rational(1, 4))
    assert len(pair01) == 2
    assert all(
        sp.factor(actual - expected) == 0
        for actual, expected in zip(pair01, expected01)
    )

    pair04 = eliminated_pair_equations(q0, parameters, forms, 0, 4)
    pair05 = eliminated_pair_equations(q0, parameters, forms, 0, 5)
    expected04 = a00 * a40 + t * (r + s) * (t - r) / (4 * r * D)
    expected05 = a00 * a50 + t * (r + s) * (r + t) / (4 * r * D)
    assert len(pair04) == len(pair05) == 1
    assert sp.factor(pair04[0] - expected04) == 0
    assert sp.factor(pair05[0] - expected05) == 0

    E = sp.factor(r**2 + r * s - r * t + s * t)
    return D, E


def exceptional_r_plus_s():
    r, t = sp.symbols("r t", nonzero=True)
    _, q0 = build_base(r, -r, t)
    ranks, parameters, forms = all_first_forms(q0)
    assert ranks == (7, 9, 8, 9, 9, 9)
    # The required coefficient is one, but every complete first tangent and
    # every direct Q2 correction give one half.
    assert all_x_pair_residual(q0, parameters, forms, 0, 2) == -sp.Rational(1, 2)


def exceptional_E():
    r, s = sp.symbols("r s", nonzero=True)
    t = sp.factor(r * (r + s) / (r - s))
    _, q0 = build_base(r, s, t)
    ranks, parameters, forms = all_first_forms(q0)
    assert ranks == (8, 9, 9, 9, 9, 9)
    assert all_x_pair_residual(q0, parameters, forms, 0, 1) == -sp.Rational(1, 2)


def main():
    verify_support_classification()
    D, E = generic_open_boundary()
    exceptional_r_plus_s()
    exceptional_E()
    print("verified permanent-zero support boundary classification")
    print("verified normal-form binary output H(q0)=2X+Y")
    print("verified generic first ranks 8,9,9,9,9,9 and three pair constraints")
    print(f"generic localization factors: D={D}, E={E}")
    print("verified r+s=0 frozen pair {0,2}: coefficient 1/2, target 1")
    print("verified E=0 frozen pair {0,1}: coefficient 1/2, target 1")


if __name__ == "__main__":
    main()
