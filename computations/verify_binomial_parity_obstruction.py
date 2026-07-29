#!/usr/bin/env python3
"""Find exact odd parity circuits among two-term mixed fibers.

If a mixed coefficient has exactly two supported Laurent monomials with
exponent difference d, cancellation requires x^d=-1.  An integer relation
sum z_i d_i=0 with odd sum z_i is impossible.  MILP is used only to propose
short circuits; every accepted circuit is checked with integer arithmetic.
"""

from __future__ import annotations

import itertools

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp


def find_odd_relation(relations, coefficient_bound=4, time_limit=30.0):
    """Return ((index, coefficient), ...) or None.

    ``relations`` is an iterable of equal-length integer exponent vectors.
    The final integer variable h imposes sum(z_i)-2h=1.
    """
    relations = tuple(relations)
    if not relations:
        return None
    differences = np.asarray(relations, dtype=np.int64).T
    dimension, count = differences.shape
    matrix = np.zeros((dimension + 1, 2 * count + 1), dtype=float)
    matrix[:dimension, :count] = differences
    matrix[:dimension, count : 2 * count] = -differences
    matrix[-1, :count] = 1
    matrix[-1, count : 2 * count] = -1
    matrix[-1, -1] = -2
    rhs = np.zeros(dimension + 1)
    rhs[-1] = 1
    objective = np.asarray((*([1.0] * (2 * count)), 0.0))
    lower = np.asarray((*([0.0] * (2 * count)), -1000.0))
    upper = np.asarray(
        (*([float(coefficient_bound)] * (2 * count)), 1000.0)
    )
    result = milp(
        objective,
        integrality=np.ones(2 * count + 1),
        bounds=Bounds(lower, upper),
        constraints=LinearConstraint(matrix, rhs, rhs),
        options={"time_limit": time_limit},
    )
    if not result.success:
        return None
    rounded = np.rint(result.x).astype(np.int64)
    coefficients = rounded[:count] - rounded[count : 2 * count]
    exact = differences @ coefficients
    assert all(int(value) == 0 for value in exact)
    assert int(coefficients.sum()) % 2 == 1
    return tuple(
        (index, int(coefficient))
        for index, coefficient in enumerate(coefficients)
        if coefficient
    )


def express_target(relations, target, coefficient_bound=4, time_limit=10.0):
    """Express ``target`` in the integer relation lattice, with exact audit."""
    relations = tuple(relations)
    differences = np.asarray(relations, dtype=np.int64).T
    dimension, count = differences.shape
    matrix = np.zeros((dimension, 2 * count), dtype=float)
    matrix[:, :count] = differences
    matrix[:, count:] = -differences
    rhs = np.asarray(target, dtype=float)
    result = milp(
        np.ones(2 * count),
        integrality=np.ones(2 * count),
        bounds=Bounds(0.0, float(coefficient_bound)),
        constraints=LinearConstraint(matrix, rhs, rhs),
        options={"time_limit": time_limit},
    )
    if not result.success:
        return None
    rounded = np.rint(result.x).astype(np.int64)
    coefficients = rounded[:count] - rounded[count:]
    exact = differences @ coefficients
    assert tuple(int(value) for value in exact) == tuple(target)
    return tuple(int(value) for value in coefficients)


def cycle_chart():
    n = 6
    colors = range(3)
    cycle = {(0, 3), (0, 5), (1, 4), (1, 5), (2, 3), (2, 4)}
    labels = {
        (0, 1): (2, 1),
        (0, 2): (0, 0),
        (0, 4): (0, 2),
        (1, 2): (1, 1),
        (1, 3): (1, 0),
        (2, 5): (0, 2),
        (3, 4): (2, 0),
        (3, 5): (2, 2),
        (4, 5): (1, 1),
    }
    edges = tuple(itertools.combinations(range(n), 2))
    supports = {
        edge: (
            (set(colors), set(colors))
            if edge in cycle
            else ({labels[edge][0]}, {labels[edge][1]})
        )
        for edge in edges
    }
    keys = []
    for edge, (left, right) in supports.items():
        keys.extend((edge, 0, color) for color in left)
        keys.extend((edge, 1, color) for color in right)
    key_index = {key: index for index, key in enumerate(keys)}

    def perfect_matchings(vertices):
        if not vertices:
            yield ()
            return
        u = vertices[0]
        for position, v in enumerate(vertices[1:], 1):
            rest = vertices[1:position] + vertices[position + 1 :]
            for tail in perfect_matchings(rest):
                yield ((u, v),) + tail

    matchings = tuple(perfect_matchings(tuple(range(n))))

    def exponent(coloring, matching):
        answer = [0] * len(keys)
        for edge in matching:
            a, b = coloring[edge[0]], coloring[edge[1]]
            left, right = supports[edge]
            if a not in left or b not in right:
                return None
            answer[key_index[edge, 0, a]] += 1
            answer[key_index[edge, 1, b]] += 1
        return tuple(answer)

    relations = []
    metadata = []
    fibers = {}
    for coloring in itertools.product(colors, repeat=n):
        if len(set(coloring)) == 1:
            continue
        fiber = tuple(
            (matching, value)
            for matching in matchings
            if (value := exponent(coloring, matching)) is not None
        )
        fibers[coloring] = fiber
        if len(fiber) != 2:
            continue
        difference = tuple(a - b for a, b in zip(fiber[0][1], fiber[1][1]))
        relations.append(difference)
        metadata.append((coloring, fiber[0][0], fiber[1][0]))
    return tuple(relations), tuple(metadata), fibers


def main():
    relations, metadata, fibers = cycle_chart()
    certificate = find_odd_relation(relations)
    print(f"two-term fibers={len(relations)}, odd circuit={certificate}")
    if certificate is not None:
        for index, coefficient in certificate:
            print(coefficient, metadata[index])
        return
    for coloring, fiber in fibers.items():
        if len(fiber) < 3:
            continue
        base = fiber[0][1]
        signs = [1]
        certificates = []
        for _, exponent in fiber[1:]:
            target = tuple(a - b for a, b in zip(exponent, base))
            expression = express_target(relations, target)
            if expression is None:
                break
            signs.append(-1 if sum(expression) % 2 else 1)
            certificates.append(expression)
        else:
            if sum(signs) != 0:
                print(
                    f"inconsistent fiber {coloring}: size={len(fiber)}, "
                    f"forced signs={signs}"
                )
                print(tuple(matching for matching, _ in fiber))
                return
    print("no short quotient-fiber contradiction found")


if __name__ == "__main__":
    main()
