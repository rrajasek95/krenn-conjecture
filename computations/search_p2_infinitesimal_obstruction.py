#!/usr/bin/env python3
"""Search for a second-order infinitesimal obstruction to P^2 membership.

The base source is a q=3 presentation of Delta_(6,2).  It deliberately uses
color-2 entries in two cancelling pairs, so the absent pure color-2
coefficient has a nonzero differential.  We solve

    F_mixed(A0 + t V + t^2 W) = 0 mod t^3,
    F_222222(A0 + t V + t^2 W) = t + O(t^2)

over Q.  A successful solution is a homomorphism from R/I to Q[t]/(t^3)
under which P^2 is nonzero, proving P^2 is not in I.
"""

from __future__ import annotations

import itertools
from fractions import Fraction


N = 6
Q = 3
VERTICES = tuple(range(N))
EDGES = tuple(itertools.combinations(VERTICES, 2))
VARIABLES = tuple((u, v, a, b) for u, v in EDGES for a in range(Q) for b in range(Q))
VAR_INDEX = {x: i for i, x in enumerate(VARIABLES)}


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for k in range(1, len(vertices)):
        v = vertices[k]
        rest = vertices[1:k] + vertices[k + 1 :]
        for tail in perfect_matchings(rest):
            yield ((u, v),) + tail


PM = tuple(perfect_matchings(VERTICES))
COLORINGS = tuple(itertools.product(range(Q), repeat=N))
PURE = {(a,) * N for a in range(Q)}
MIXED = tuple(c for c in COLORINGS if c not in PURE)


def put(source, u, v, entries):
    assert u < v
    source[u, v] = {cell: Fraction(value) for cell, value in entries.items()}


GROUPS = (
    (((0, 1), (2, 3), (4, 5)), ((0, 2), (1, 3), (4, 5))),
    (((0, 5), (1, 2), (3, 4)), ((0, 4), (1, 2), (3, 5))),
)


def add_cancelling_group(source, color, matchings, carrier, modified):
    first, second = matchings
    shared = next(edge for edge in first if edge in second)
    carrier_matching = (first, second)[carrier]
    cancellation_matching = (second, first)[carrier]
    carrier_edges = [edge for edge in carrier_matching if edge != shared]
    modified_edge = carrier_edges[modified]
    other_edge = carrier_edges[1 - modified]

    put(source, *shared, {(color, color): 1})
    put(source, *other_edge, {(color, color): 1})
    put(source, *modified_edge, {(color, color): 1, (2, 2): 1})

    # The other matching contributes minus the rank-one decoration T whose
    # local color is 2 on ``modified_edge`` and ``color`` elsewhere.
    local = {v: (2 if v in modified_edge else color) for v in VERTICES}
    cancellation_edges = [edge for edge in cancellation_matching if edge != shared]
    for k, (u, v) in enumerate(cancellation_edges):
        put(source, u, v, {(local[u], local[v]): -1 if k == 0 else 1})
    return modified_edge


def base_source(choice0=(0, 1), choice1=(0, 0)):
    source = {}
    edge0 = add_cancelling_group(source, 0, GROUPS[0], *choice0)
    edge1 = add_cancelling_group(source, 1, GROUPS[1], *choice1)
    return source, (edge0, edge1)


def entry(vector, u, v, a, b):
    if u > v:
        u, v, a, b = v, u, b, a
    return vector[VAR_INDEX[u, v, a, b]]


def dense_source(source):
    vector = [Fraction(0)] * len(VARIABLES)
    for (u, v), matrix in source.items():
        for (a, b), value in matrix.items():
            vector[VAR_INDEX[u, v, a, b]] = value
    return vector


def coefficient(vector, coloring):
    total = Fraction(0)
    for matching in PM:
        value = Fraction(1)
        for u, v in matching:
            value *= entry(vector, u, v, coloring[u], coloring[v])
        total += value
    return total


def jacobian_row(base, coloring):
    row = {}
    for u, v in EDGES:
        complement = tuple(x for x in VERTICES if x not in (u, v))
        cofactor = Fraction(0)
        for matching in perfect_matchings(complement):
            value = Fraction(1)
            for i, j in matching:
                value *= entry(base, i, j, coloring[i], coloring[j])
            cofactor += value
        if cofactor:
            row[VAR_INDEX[u, v, coloring[u], coloring[v]]] = cofactor
    return row


def sparse_solve(equations, number_variables):
    """Solve sparse rational equations; return one solution or None."""
    pivots = {}
    for coefficients, rhs in equations:
        row = {j: Fraction(z) for j, z in coefficients.items() if z}
        rhs = Fraction(rhs)
        while row:
            pivot = min(row)
            if pivot not in pivots:
                scale = row[pivot]
                row = {j: z / scale for j, z in row.items()}
                rhs /= scale
                pivots[pivot] = (row, rhs)
                break
            prow, prhs = pivots[pivot]
            scale = row[pivot]
            for j, z in prow.items():
                value = row.get(j, 0) - scale * z
                if value:
                    row[j] = value
                else:
                    row.pop(j, None)
            rhs -= scale * prhs
        else:
            if rhs:
                return None, pivots

    solution = [Fraction(0)] * number_variables
    for pivot in sorted(pivots, reverse=True):
        row, rhs = pivots[pivot]
        solution[pivot] = rhs - sum(z * solution[j] for j, z in row.items() if j != pivot)
    return solution, pivots


def quadratic_term(base, tangent, coloring):
    total = Fraction(0)
    for matching in PM:
        factors0 = [entry(base, u, v, coloring[u], coloring[v]) for u, v in matching]
        factors1 = [entry(tangent, u, v, coloring[u], coloring[v]) for u, v in matching]
        total += (
            factors1[0] * factors1[1] * factors0[2]
            + factors1[0] * factors0[1] * factors1[2]
            + factors0[0] * factors1[1] * factors1[2]
        )
    return total


def main():
    pure2 = (2,) * N
    candidates = []
    for choice0 in itertools.product(range(2), repeat=2):
        for choice1 in itertools.product(range(2), repeat=2):
            source, modified_edges = base_source(choice0, choice1)
            if set(modified_edges[0]) & set(modified_edges[1]):
                continue
            base = dense_source(source)
            output = {c: coefficient(base, c) for c in COLORINGS}
            assert {c: z for c, z in output.items() if z} == {
                (0,) * N: Fraction(1),
                (1,) * N: Fraction(1),
            }
            rows = {c: jacobian_row(base, c) for c in COLORINGS}
            tangent_equations = [(rows[c], 0) for c in MIXED] + [(rows[pure2], 1)]
            tangent, tangent_pivots = sparse_solve(tangent_equations, len(VARIABLES))
            print(
                f"choices={choice0, choice1}, modified={modified_edges}, "
                f"first_order={'yes' if tangent is not None else 'no'}"
            )
            if tangent is not None:
                candidates.append((choice0, choice1, base, rows, tangent, tangent_pivots))
    if not candidates:
        print("no first-order mixed-flat tangent in the 16 cancelling-pair charts")
        return
    choice0, choice1, base, rows, tangent, tangent_pivots = candidates[0]
    print(f"using choices={choice0, choice1}")
    tangent_support = sum(bool(z) for z in tangent)
    assert all(sum(z * tangent[j] for j, z in rows[c].items()) == 0 for c in MIXED)
    assert sum(z * tangent[j] for j, z in rows[pure2].items()) == 1
    print(
        f"first order solved: rank={len(tangent_pivots)}, "
        f"tangent_support={tangent_support}"
    )

    quadratic = {c: quadratic_term(base, tangent, c) for c in COLORINGS}
    second_equations = [(rows[c], -quadratic[c]) for c in MIXED]
    second, second_pivots = sparse_solve(second_equations, len(VARIABLES))
    if second is None:
        nonzero = sum(bool(quadratic[c]) for c in MIXED)
        print(
            f"second-order lift obstructed for selected tangent: "
            f"quadratic_support={nonzero}, rank={len(second_pivots)}"
        )
        return
    second_support = sum(bool(z) for z in second)
    print(
        f"second order solved: rank={len(second_pivots)}, "
        f"second_support={second_support}"
    )

    # Independent truncated expansion audit for every coefficient.
    for coloring in COLORINGS:
        constant = coefficient(base, coloring)
        linear = sum(z * tangent[j] for j, z in rows[coloring].items())
        quadratic_coefficient = (
            sum(z * second[j] for j, z in rows[coloring].items())
            + quadratic[coloring]
        )
        if coloring in MIXED:
            assert (constant, linear, quadratic_coefficient) == (0, 0, 0)
    assert coefficient(base, pure2) == 0
    assert sum(z * tangent[j] for j, z in rows[pure2].items()) == 1

    print("SUCCESS: P^2 maps to t^2 + O(t^3), so P^2 is not in the mixed ideal")
    print("tangent=", [(VARIABLES[j], z) for j, z in enumerate(tangent) if z])
    print("second=", [(VARIABLES[j], z) for j, z in enumerate(second) if z])


if __name__ == "__main__":
    main()
