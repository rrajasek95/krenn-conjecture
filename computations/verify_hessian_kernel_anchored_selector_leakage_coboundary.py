#!/usr/bin/env python3
"""Exact audit of Hessian-kernel blindness and anchored leakage cycles."""

from fractions import Fraction as F
from itertools import combinations


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def edge(i, j):
    return (i, j) if i < j else (j, i)


EDGES = tuple(combinations(range(6), 2))


def hafnian_on(vertices, weights):
    vertices = tuple(vertices)
    if not vertices:
        return F(1)
    first = vertices[0]
    total = F(0)
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        total += weights.get(edge(first, second), F(0)) * hafnian_on(rest, weights)
    return total


def hessian_times(weights, vector):
    out = {}
    all_vertices = set(range(6))
    for missing in EDGES:
        four_set = tuple(sorted(all_vertices - set(missing)))
        value = F(0)
        for chosen in combinations(four_set, 2):
            complement = tuple(sorted(set(four_set) - set(chosen)))
            value += vector.get(edge(*chosen), F(0)) * weights.get(edge(*complement), F(0))
        out[missing] = value
    return out


def gradient(weights):
    all_vertices = set(range(6))
    return {
        missing: hafnian_on(tuple(sorted(all_vertices - set(missing))), weights)
        for missing in EDGES
    }


def dot(left, right):
    return sum((left.get(key, F(0)) * right.get(key, F(0)) for key in EDGES), F(0))


def exact_rank(rows):
    work = [[F(value) for value in row] for row in rows]
    rank = 0
    width = len(work[0]) if work else 0
    for column in range(width):
        pivot = next(
            (row for row in range(rank, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        pivot_value = work[rank][column]
        work[rank] = [value / pivot_value for value in work[rank]]
        for row in range(len(work)):
            if row == rank or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                value - factor * pivot_entry
                for value, pivot_entry in zip(work[row], work[rank])
            ]
        rank += 1
    return rank


def audit_hessian_kernel():
    support = {edge(*item) for item in (
        (0, 1), (0, 2), (0, 3), (0, 4), (0, 5),
        (1, 2), (1, 3), (1, 4), (2, 3), (4, 5),
    )}
    q = {item: F(item in support) for item in EDGES}
    z = {item: F(0) for item in EDGES}
    z[edge(0, 2)] = F(1)
    z[edge(0, 3)] = F(-1)
    z[edge(2, 4)] = F(-1)
    z[edge(3, 4)] = F(1)

    hz = hessian_times(q, z)
    require(all(value == 0 for value in hz.values()), "claimed vector missed the Hessian kernel")

    columns = []
    for selected in EDGES:
        basis = {item: F(item == selected) for item in EDGES}
        image = hessian_times(q, basis)
        columns.append(tuple(image[item] for item in EDGES))
    hessian_rows = tuple(
        tuple(columns[column][row] for column in range(len(EDGES)))
        for row in range(len(EDGES))
    )
    require(exact_rank(hessian_rows) == 14, "guard Hessian is not corank one")

    grad = gradient(q)
    require(dot(grad, z) == 0, "top hafnian derivative did not vanish")

    # d(q_01 q_23 - q_02 q_13) at q, evaluated on z.
    curvature = (
        z[edge(0, 1)] * q[edge(2, 3)]
        + q[edge(0, 1)] * z[edge(2, 3)]
        - z[edge(0, 2)] * q[edge(1, 3)]
        - q[edge(0, 2)] * z[edge(1, 3)]
    )
    require(curvature == -1, "nonzero four-cycle curvature changed")

    bad = dict(z)
    bad[edge(0, 1)] += 1
    require(any(hessian_times(q, bad).values()), "kernel mutation was not detected")
    return q, z


def matrix(rows):
    return tuple(tuple(F(value) for value in row) for row in rows)


def diagonal(values):
    return tuple(tuple(F(values[i]) if i == j else F(0) for j in range(3)) for i in range(3))


def transpose(item):
    return tuple(tuple(item[j][i] for j in range(3)) for i in range(3))


def multiply(left, right):
    return tuple(
        tuple(sum((left[i][k] * right[k][j] for k in range(3)), F(0)) for j in range(3))
        for i in range(3)
    )


def add(left, right):
    return tuple(tuple(left[i][j] + right[i][j] for j in range(3)) for i in range(3))


def scale(value, item):
    value = F(value)
    return tuple(tuple(value * item[i][j] for j in range(3)) for i in range(3))


def frame_derivative(x_connection, y_connection, label):
    unit = tuple(
        tuple(F(i == label and j == label) for j in range(3))
        for i in range(3)
    )
    return scale(-1, add(multiply(transpose(x_connection), unit), multiply(unit, y_connection)))


def audit_anchored_connection():
    direct = matrix(((2, 1, 3), (5, -1, 4), (7, 6, 8)))
    x_values = (F(2), F(-1), F(4))
    x_connection = diagonal(x_values)
    y_connection = scale(-1, x_connection)
    top = F(7)

    for label in range(3):
        require(frame_derivative(x_connection, y_connection, label) == diagonal((0, 0, 0)),
                f"diagonal frame {label} was not horizontal")

    c_derivative = scale(-1, add(multiply(transpose(x_connection), direct), multiply(direct, y_connection)))
    leakage = scale(-top, c_derivative)
    for i in range(3):
        for j in range(3):
            expected = top * (x_values[i] - x_values[j]) * direct[i][j]
            require(leakage[i][j] == expected, f"coboundary formula failed at {(i, j)}")

    for i, j in ((0, 1), (1, 2), (2, 0)):
        require(
            direct[j][i] * leakage[i][j] + direct[i][j] * leakage[j][i] == 0,
            f"two-cycle holonomy survived on {(i, j)}",
        )

    triangle = (
        direct[1][2] * direct[2][0] * leakage[0][1]
        + direct[2][0] * direct[0][1] * leakage[1][2]
        + direct[0][1] * direct[1][2] * leakage[2][0]
    )
    require(triangle == 0, "three-cycle holonomy survived")

    # Breaking one reciprocal diagonal relation is detected both by its
    # labelled frame and by the triangle holonomy.
    mutated_y = diagonal((-x_values[0] + 1, -x_values[1], -x_values[2]))
    require(frame_derivative(x_connection, mutated_y, 0) != diagonal((0, 0, 0)),
            "frame mutation was not detected")
    mutated_c = scale(-1, add(multiply(transpose(x_connection), direct), multiply(direct, mutated_y)))
    mutated_leakage = scale(-top, mutated_c)
    mutated_triangle = (
        direct[1][2] * direct[2][0] * mutated_leakage[0][1]
        + direct[2][0] * direct[0][1] * mutated_leakage[1][2]
        + direct[0][1] * direct[1][2] * mutated_leakage[2][0]
    )
    require(mutated_triangle != 0, "non-horizontal mutation kept zero holonomy")


def main():
    audit_hessian_kernel()
    audit_anchored_connection()
    print("Hessian-kernel anchored selector leakage coboundary: PASS")
    print("raw blindness, reciprocal connection, and cycle holonomy audited")


if __name__ == "__main__":
    main()
