#!/usr/bin/env python3
"""Uniform scalar full-nine counterguard to a formal tangent-or-clean claim.

For every tested h, construct a common-q, rank-one-star nine-row packet with
three nonzero diagonal anchors and nonzero direct curvature.  The q-shift
has a nonzero cokernel class modulo all star tangents, while the reciprocal
endpoint clean tail is also nonzero.  Thus a tangent-or-clean theorem must
use physical multisite/cross-chart provenance before scalar contraction.
"""

from fractions import Fraction
from hashlib import sha256
from math import factorial
import json


Q = Fraction
P = (Q(2), Q(-3), Q(5))
S = (Q(7), Q(11), Q(-13))
ANCHORS = (Q(17), Q(19), Q(23))
SELECTED = (0, 1)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def outer(left, right):
    return [[left[i] * right[j] for j in range(3)] for i in range(3)]


def flatten(matrix):
    return tuple(matrix[i][j] for i in range(3) for j in range(3))


def add(left, right):
    return tuple(a + b for a, b in zip(left, right))


def scale(scalar, vector):
    return tuple(scalar * entry for entry in vector)


def rank(columns):
    if not columns:
        return 0
    rows = len(columns[0])
    matrix = [[Q(columns[column][row]) for column in range(len(columns))]
              for row in range(rows)]
    pivot_row = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(pivot_row, rows)
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        value = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / value for entry in matrix[pivot_row]]
        for row in range(rows):
            if row == pivot_row or not matrix[row][column]:
                continue
            multiple = matrix[row][column]
            matrix[row] = [entry - multiple * pivot_entry
                           for entry, pivot_entry
                           in zip(matrix[row], matrix[pivot_row])]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def star_tangent_columns(p, s):
    columns = []
    # u*s^T
    for row in range(3):
        matrix = [[Q(0)] * 3 for _ in range(3)]
        for column in range(3):
            matrix[row][column] = s[column]
        columns.append(flatten(matrix))
    # p*v^T
    for column in range(3):
        matrix = [[Q(0)] * 3 for _ in range(3)]
        for row in range(3):
            matrix[row][column] = p[row]
        columns.append(flatten(matrix))
    return columns


def direct_matrix(h):
    response = outer(P, S)
    return [[(ANCHORS[i] if i == j else Q(0)) - h * response[i][j]
             for j in range(3)] for i in range(3)]


def divided_grade(response, h, grade):
    # q=1, so Q_grade=r^[grade] q^[h-grade].
    return response ** grade / (factorial(grade) * factorial(h - grade))


def audit_order(h):
    require(h >= 3, "order outside theorem")
    response = outer(P, S)
    direct = direct_matrix(h)

    # All nine common-q equations at q=1:
    # d_ij q^[h] + p_i*s_j q^[h-1] = delta_ij X_i,
    # with X_i=t_i/h!.
    rows = []
    for i in range(3):
        for j in range(3):
            left = direct[i][j] / factorial(h)
            left += response[i][j] / factorial(h - 1)
            right = ANCHORS[i] / factorial(h) if i == j else Q(0)
            require(left == right, f"h={h}: full-nine row {(i, j)}")
            rows.append(str(left))

    a, b = SELECTED
    r = response[a][b]
    alpha = direct[a][b]
    require(r != 0 and alpha == -h * r, f"h={h}: selected row")
    require(alpha * divided_grade(r, h, 0) + divided_grade(r, h, 1) == 0,
            f"h={h}: admitted endpoint relation")

    reciprocal_tail = (
        alpha * divided_grade(r, h, h - 1)
        + divided_grade(r, h, h)
    )
    expected_tail = -(h * h - 1) * r ** h / factorial(h)
    require(reciprocal_tail == expected_tail and reciprocal_tail != 0,
            f"h={h}: reciprocal tail")

    # The complete target-eliminated nonlinear clean error also survives.
    clean_error = sum(
        (alpha ** (h - grade) * divided_grade(r, h, grade)
         for grade in range(2, h + 1)), Q(0))
    expected_error = r ** h * (1 - h) ** h / factorial(h)
    require(clean_error == expected_error and clean_error != 0,
            f"h={h}: full clean error")

    # Linearize the normalized nine equations
    # G=d*q^h+h*p*s^T*q^(h-1)-diag(t) at q=1, holding d,t fixed.
    # Modulo star tangents, the q-direction is represented by
    # diag(t)-p*s^T, and its class equals [diag(t)] because p*s^T itself
    # is a star tangent.
    tangent = star_tangent_columns(P, S)
    require(rank(tangent) == 5, f"h={h}: Segre tangent rank")
    q_obstruction_matrix = [[
        (ANCHORS[i] if i == j else Q(0)) - response[i][j]
        for j in range(3)] for i in range(3)]
    q_obstruction = flatten(q_obstruction_matrix)
    diagonal_anchor = flatten([
        [ANCHORS[i] if i == j else Q(0) for j in range(3)]
        for i in range(3)
    ])
    response_vector = flatten(response)
    require(add(q_obstruction, response_vector) == diagonal_anchor,
            f"h={h}: anchor representative")
    require(rank(tangent + [response_vector]) == 5,
            f"h={h}: response not a star tangent")
    require(rank(tangent + [q_obstruction]) == 6,
            f"h={h}: shifted comparison unexpectedly exists")
    require(rank(tangent + [diagonal_anchor]) == 6,
            f"h={h}: diagonal anchor class vanished")

    # Over Q the nonzero reciprocal scalar cannot annihilate the cokernel
    # class.  This is the exact failure of the proposed product dichotomy.
    require(rank(tangent + [scale(reciprocal_tail, q_obstruction)]) == 6,
            f"h={h}: tail unexpectedly annihilates obstruction")

    # With the anchors removed the same q-direction is just -p*s^T and is
    # absorbed by a star scaling.  The anchors are exactly the residual
    # first-jet class, not a hidden tail-killing relation.
    anchor_free = scale(Q(-1), response_vector)
    require(rank(tangent + [anchor_free]) == 5,
            f"h={h}: anchor-free direction did not lift")

    # A literal nonzero 2x2 direct minor survives uniformly.
    curvature = (direct[0][1] * direct[1][2]
                 - direct[0][2] * direct[1][1])
    require(curvature == -Q(494) * h and curvature != 0,
            f"h={h}: direct curvature")

    return {
        "h": h,
        "alpha": str(alpha),
        "response": str(r),
        "targets": [str(value / factorial(h)) for value in ANCHORS],
        "full_nine_rows": len(rows),
        "star_tangent_rank": rank(tangent),
        "obstruction_augmented_rank": rank(tangent + [q_obstruction]),
        "reciprocal_tail": str(reciprocal_tail),
        "tail_times_obstruction_nonzero": True,
        "clean_error": str(clean_error),
        "curvature": str(curvature),
    }


def main():
    records = [audit_order(h) for h in range(3, 16)]
    ledger = {
        "scope": "scalar common-q full-nine quotient; not a physical site-graded source",
        "endpoint_vectors": {
            "p": [str(value) for value in P],
            "s": [str(value) for value in S],
        },
        "anchor_numerators": [str(value) for value in ANCHORS],
        "selected": list(SELECTED),
        "orders": records,
        "physical_comparison_constructed": False,
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    require(digest == "e3cdcc445d69b6f07ab283cfcbc7489d9973e8da476bdd7a3b20bd62b86ea57d",
            f"uniform counterguard changed: {digest}")

    print("uniform scalar full-nine tangent-or-clean counterguard: PASS")
    print("orders h=3..15: all nine anchors and nonzero direct curvature")
    print("shifted-comparison cokernel and reciprocal clean tail are both nonzero")
    print("therefore anchor/source coupling is required before scalar contraction")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
