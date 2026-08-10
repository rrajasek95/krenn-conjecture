#!/usr/bin/env python3
"""Exact audit of the diagonal map on the rank-(1,1) scalar gate.

Let H_l=ker(l^T), H_m=ker(m^T), and Q=H_l tensor H_m.  If neither
l nor m is a coordinate vector, every restricted diagonal coordinate is
nonzero.  This checker verifies the sharper statement used in the companion
note: the map

    Q -> Q^3,  K |-> (K_00,K_11,K_22)

has rank three unless l and m have the same missing coordinate.  In the
rank-three case its kernel is one-dimensional.  When all coordinates of l
and m are nonzero, the kernel is the explicit alternating directed triangle

    K_ij = eps_ij prod(l)prod(m)/(l_i m_j).

Standard library only, exact Fraction arithmetic.  This is a checker for a
uniform linear-algebra lemma, not a proof of SP-CLEAN-BRIDGE.
"""

from fractions import Fraction as Q
from hashlib import sha256
from itertools import product


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def kernel_basis(vector):
    pivot = next(index for index, value in enumerate(vector) if value)
    answer = []
    for index in range(3):
        if index == pivot:
            continue
        row = [Q(0)] * 3
        row[index] = vector[pivot]
        row[pivot] = -vector[index]
        answer.append(tuple(row))
    require(len(answer) == 2, ("bad hyperplane basis", vector, answer))
    require(all(sum(vector[i] * row[i] for i in range(3)) == 0
                for row in answer), ("basis left the kernel", vector))
    return tuple(answer)


def matrix_rank(rows):
    rows = [list(map(Q, row)) for row in rows]
    if not rows:
        return 0
    width = len(rows[0])
    rank = 0
    for column in range(width):
        pivot = next((row for row in range(rank, len(rows))
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        scale = rows[rank][column]
        rows[rank] = [value / scale for value in rows[rank]]
        for row in range(len(rows)):
            if row == rank or not rows[row][column]:
                continue
            scale = rows[row][column]
            rows[row] = [left - scale * right
                         for left, right in zip(rows[row], rows[rank])]
        rank += 1
        if rank == len(rows):
            break
    return rank


def rref_nullspace(rows):
    rows = [list(map(Q, row)) for row in rows]
    width = len(rows[0])
    pivot_columns = []
    rank = 0
    for column in range(width):
        pivot = next((row for row in range(rank, len(rows))
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        scale = rows[rank][column]
        rows[rank] = [value / scale for value in rows[rank]]
        for row in range(len(rows)):
            if row == rank or not rows[row][column]:
                continue
            scale = rows[row][column]
            rows[row] = [left - scale * right
                         for left, right in zip(rows[row], rows[rank])]
        pivot_columns.append(column)
        rank += 1
    free = [column for column in range(width)
            if column not in pivot_columns]
    basis = []
    for free_column in free:
        vector = [Q(0)] * width
        vector[free_column] = Q(1)
        for row, pivot_column in enumerate(pivot_columns):
            vector[pivot_column] = -rows[row][free_column]
        basis.append(tuple(vector))
    require(all(all(sum(row[column] * vector[column]
                        for column in range(width)) == 0
                    for row in rows)
                for vector in basis), "nullspace reconstruction failed")
    return tuple(basis)


def outer(left, right):
    return tuple(tuple(left[i] * right[j] for j in range(3))
                 for i in range(3))


def add_matrix(left, right):
    return tuple(tuple(left[i][j] + right[i][j] for j in range(3))
                 for i in range(3))


def scale_matrix(scalar, matrix):
    return tuple(tuple(scalar * matrix[i][j] for j in range(3))
                 for i in range(3))


def combine(coefficients, basis):
    answer = tuple(tuple(Q(0) for _ in range(3)) for _ in range(3))
    for coefficient, matrix in zip(coefficients, basis):
        answer = add_matrix(answer, scale_matrix(coefficient, matrix))
    return answer


def left_product(vector, matrix):
    return tuple(sum(vector[i] * matrix[i][j] for i in range(3))
                 for j in range(3))


def right_product(matrix, vector):
    return tuple(sum(matrix[i][j] * vector[j] for j in range(3))
                 for i in range(3))


def proportional(left, right):
    pivot = next((index for index, value in enumerate(right) if value), None)
    if pivot is None:
        return not any(left)
    scalar = left[pivot] / right[pivot]
    return all(left[index] == scalar * right[index]
               for index in range(len(left)))


def flatten(matrix):
    return tuple(matrix[i][j] for i in range(3) for j in range(3))


def cycle_matrix(left, right):
    common = Q(1)
    for value in left + right:
        common *= value
    positive = {(0, 1), (1, 2), (2, 0)}
    negative = {(1, 0), (2, 1), (0, 2)}
    answer = []
    for i in range(3):
        row = []
        for j in range(3):
            if i == j:
                row.append(Q(0))
            elif (i, j) in positive:
                row.append(common / (left[i] * right[j]))
            elif (i, j) in negative:
                row.append(-common / (left[i] * right[j]))
            else:
                raise AssertionError((i, j))
        answer.append(tuple(row))
    return tuple(answer)


def solve(rows, target):
    # Solve the consistent 3 by 4 system by augmenting and reading one RREF
    # solution with every free variable set to zero.
    augmented = [list(map(Q, row)) + [Q(value)]
                 for row, value in zip(rows, target)]
    width = len(rows[0])
    pivot_columns = []
    rank = 0
    for column in range(width):
        pivot = next((row for row in range(rank, len(augmented))
                      if augmented[row][column]), None)
        if pivot is None:
            continue
        augmented[rank], augmented[pivot] = augmented[pivot], augmented[rank]
        scale = augmented[rank][column]
        augmented[rank] = [value / scale for value in augmented[rank]]
        for row in range(len(augmented)):
            if row == rank or not augmented[row][column]:
                continue
            scale = augmented[row][column]
            augmented[row] = [left - scale * right
                               for left, right in zip(
                                   augmented[row], augmented[rank])]
        pivot_columns.append(column)
        rank += 1
    require(all(any(row[:width]) or not row[width] for row in augmented),
            ("inconsistent diagonal lift", rows, target))
    answer = [Q(0)] * width
    for row, column in enumerate(pivot_columns):
        answer[column] = augmented[row][width]
    require(all(sum(rows[i][j] * answer[j] for j in range(width)) == target[i]
                for i in range(3)), ("bad diagonal lift", target, answer))
    return tuple(answer)


def support(vector):
    return tuple(index for index, value in enumerate(vector) if value)


def audit_instance(left, right):
    left_basis = kernel_basis(left)
    right_basis = kernel_basis(right)
    q_basis = tuple(outer(x, y)
                    for x in left_basis for y in right_basis)
    diagonal_rows = tuple(tuple(matrix[i][i] for matrix in q_basis)
                          for i in range(3))
    rank = matrix_rank(diagonal_rows)
    common_missing = tuple(index for index in range(3)
                           if left[index] == right[index] == 0)
    expected_rank = 2 if common_missing else 3
    require(rank == expected_rank,
            ("diagonal rank classification failed", left, right,
             rank, expected_rank))
    kernel = rref_nullspace(diagonal_rows)
    require(len(kernel) == 4 - rank,
            ("bad diagonal kernel dimension", left, right, kernel))
    kernel_matrices = tuple(combine(vector, q_basis) for vector in kernel)
    for matrix in kernel_matrices:
        require(not any(left_product(left, matrix)),
                ("left annihilator failed", left, matrix))
        require(not any(right_product(matrix, right)),
                ("right annihilator failed", right, matrix))
        require(not any(matrix[i][i] for i in range(3)),
                ("diagonal kernel failed", matrix))
    lifts = ()
    if rank == 3:
        lifts = tuple(combine(solve(diagonal_rows,
                                    tuple(Q(i == label) for i in range(3))),
                              q_basis)
                      for label in range(3))
        for label, matrix in enumerate(lifts):
            require(tuple(matrix[i][i] for i in range(3)) ==
                    tuple(Q(i == label) for i in range(3)),
                    ("diagonal basis lift failed", label, matrix))
        if all(left) and all(right):
            explicit = cycle_matrix(left, right)
            require(proportional(flatten(kernel_matrices[0]),
                                 flatten(explicit)),
                    ("explicit alternating cycle changed", left, right,
                     kernel_matrices[0], explicit))
            require(not any(left_product(left, explicit)),
                    ("explicit cycle left kernel failed", left, right))
            require(not any(right_product(explicit, right)),
                    ("explicit cycle right kernel failed", left, right))
    return (
        support(left), support(right), rank,
        tuple(flatten(matrix) for matrix in kernel_matrices),
        tuple(flatten(matrix) for matrix in lifts),
    )


def audit_cycle_factorization():
    alternating = {(0, 1): 1, (1, 2): 1, (2, 0): 1,
                   (1, 0): -1, (2, 1): -1, (0, 2): -1}
    factored = {}
    # (p0-p2)(s1-s2) - (p1-p2)(s0-s2)
    for i, left_coefficient in ((0, 1), (2, -1)):
        for j, right_coefficient in ((1, 1), (2, -1)):
            factored[i, j] = factored.get((i, j), 0) + (
                left_coefficient * right_coefficient)
    for i, left_coefficient in ((1, -1), (2, 1)):
        for j, right_coefficient in ((0, 1), (2, -1)):
            factored[i, j] = factored.get((i, j), 0) + (
                left_coefficient * right_coefficient)
    factored = {key: value for key, value in factored.items() if value}
    require(factored == alternating,
            ("alternating response factorization changed", factored))
    return tuple(sorted(alternating.items()))


EXPECTED_DIGEST = "56b3052fe0fad7787e652688a85fa8786f87613e0a19612d9a9e1a7c2d71e945"


def audit():
    samples = (Q(-3), Q(-1), Q(0), Q(1), Q(2))
    vectors = tuple(vector for vector in product(samples, repeat=3)
                    if sum(bool(value) for value in vector) >= 2)
    ledger = []
    counts = {2: 0, 3: 0}
    for left in vectors:
        for right in vectors:
            record = audit_instance(left, right)
            counts[record[2]] += 1
            ledger.append((left, right, record))
    cycle = audit_cycle_factorization()
    digest = sha256(repr((tuple(ledger), cycle)).encode()).hexdigest()
    if EXPECTED_DIGEST is not None:
        require(digest == EXPECTED_DIGEST,
                ("scalar-gate diagonal-cycle ledger changed", digest))
    return len(vectors), counts, digest


def main():
    vector_count, counts, digest = audit()
    print("rank-(1,1) scalar-gate diagonal cycle: passed")
    print(f"  hyperplane vectors       : {vector_count}")
    print(f"  ordered vector pairs     : {vector_count ** 2}")
    print(f"  diagonal ranks           : {dict(sorted(counts.items()))}")
    print(f"  aggregate ledger digest  : {digest}")
    print("  conclusion               : rank 3 except a common missing coordinate")


if __name__ == "__main__":
    main()
