#!/usr/bin/env python3
"""Exact certificate for Section 2 of notes/induction-route.md."""

from fractions import Fraction
from itertools import product


Q = (0, 1)
VERTICES = tuple(range(1, 7))


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for pos, second in enumerate(vertices[1:], 1):
        rest = vertices[1:pos] + vertices[pos + 1 :]
        for matching in perfect_matchings(rest):
            yield ((first, second),) + matching


def one_entry(c0, c1, weight=1):
    return {(c0, c1): Fraction(weight)}


# Dictionaries are indexed in increasing endpoint order.
X = {
    (1, 2): {(0, 0): Fraction(1), (1, 0): Fraction(1)},
    (3, 4): one_entry(0, 0),
    (5, 6): one_entry(0, 0),
    (2, 4): one_entry(0, 0),
    (1, 3): one_entry(1, 0, -1),
    (1, 6): one_entry(1, 1),
    (2, 3): one_entry(1, 1),
    (4, 5): one_entry(1, 1, Fraction(3, 4)),
    (1, 5): one_entry(1, 1, Fraction(1, 2)),
    (4, 6): one_entry(1, 1, Fraction(1, 2)),
}


def value(edges, u, v, cu, cv):
    if u < v:
        return edges.get((u, v), {}).get((cu, cv), Fraction(0))
    return edges.get((v, u), {}).get((cv, cu), Fraction(0))


def matching_tensor(vertices, edges):
    vertices = tuple(vertices)
    answer = {}
    for coloring in product(Q, repeat=len(vertices)):
        colors = dict(zip(vertices, coloring))
        total = Fraction(0)
        for matching in perfect_matchings(vertices):
            term = Fraction(1)
            for u, v in matching:
                term *= value(edges, u, v, colors[u], colors[v])
            total += term
        if total:
            answer[coloring] = total
    return answer


delta6 = {(0,) * 6: Fraction(1), (1,) * 6: Fraction(1)}
assert matching_tensor(VERTICES, X) == delta6

# Every edge is tensor-active, not merely contained in the support graph.
for edge in X:
    complement = tuple(v for v in VERTICES if v not in edge)
    assert matching_tensor(complement, X), edge

p, q = 1, 5
U = (2, 3, 4, 6)

# K is the diagonal cap.  Formula (2) is evaluated coefficientwise.
s = sum(value(X, p, q, color, color) for color in Q)
assert s == Fraction(1, 2)

R = {}
for pos, a in enumerate(U):
    for b in U[pos + 1 :]:
        matrix = {}
        for ca, cb in product(Q, repeat=2):
            total = Fraction(0)
            for color in Q:
                total += value(X, p, a, color, ca) * value(
                    X, q, b, color, cb
                )
                total += value(X, p, b, color, cb) * value(
                    X, q, a, color, ca
                )
            if total:
                matrix[(ca, cb)] = total
        if matrix:
            R[(a, b)] = matrix

assert R == {
    (2, 4): one_entry(0, 1, Fraction(3, 4)),
    (2, 6): one_entry(0, 0),
    (3, 4): one_entry(0, 1, Fraction(-3, 4)),
    (4, 6): one_entry(1, 1, Fraction(3, 4)),
}

old = matching_tensor(U, X)
quadratic = matching_tensor(U, R)
assert old == {(1, 1, 1, 1): Fraction(1, 2)}
mixed = (0, 0, 1, 0)  # vertex order (2,3,4,6)
assert quadratic == {mixed: Fraction(-3, 4)}

# Compute the directional derivative by replacing exactly one matching edge.
derivative = {}
for coloring in product(Q, repeat=4):
    colors = dict(zip(U, coloring))
    total = Fraction(0)
    for matching in perfect_matchings(U):
        for marked in range(len(matching)):
            term = Fraction(1)
            for index, (u, v) in enumerate(matching):
                edges = R if index == marked else X
                term *= value(edges, u, v, colors[u], colors[v])
            total += term
    if total:
        derivative[coloring] = total

assert derivative == {
    (0, 0, 0, 0): Fraction(1),
    (1, 1, 1, 1): Fraction(3, 4),
}

capped = dict(derivative)
for coloring, coefficient in old.items():
    capped[coloring] = capped.get(coloring, Fraction(0)) + s * coefficient
assert capped == {
    (0, 0, 0, 0): Fraction(1),
    (1, 1, 1, 1): Fraction(1),
}

# The canonical effective edges Y=X+R/s have an unavoidable mixed term.
Y = {edge: dict(matrix) for edge, matrix in X.items() if set(edge) <= set(U)}
for edge, matrix in R.items():
    target = Y.setdefault(edge, {})
    for colors, coefficient in matrix.items():
        target[colors] = target.get(colors, Fraction(0)) + coefficient / s

assert matching_tensor(U, Y) == {
    (0, 0, 0, 0): Fraction(2),
    (1, 1, 1, 1): Fraction(2),
    mixed: Fraction(-3),
}

print("verified the six-vertex target and activity of all ten support edges")
print("verified the exact pair cap and its nonzero four-site cumulant")
