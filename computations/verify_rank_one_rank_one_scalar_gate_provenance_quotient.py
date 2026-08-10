#!/usr/bin/env python3
"""Exact audit of the scalar-shore family provenance quotient.

Let

    Q = {K : lambda^T K = 0, K mu = 0} subset Mat_3

and let delta(K)=(K_00,K_11,K_22).  A coefficient functional on a
physical response family Phi(Q) is represented on Q by an ambient matrix
F.  It is induced by one functional on the three diagonal target anchors
iff

    F in Delta + Q^perp,

where Delta is the diagonal-matrix subspace.  If K0=ker Phi, the quotient
of response functionals by target-induced functionals is

    K0^perp / (Delta + Q^perp),

whose dual is ker(delta)/K0.

The proof is elementary linear algebra.  This checker exhausts all
noncoordinate projective lambda,mu over F_5, verifies the exact subspace
identities, and audits every possible K0 subspace of ker(delta).  It is a
regression check for a field-independent theorem, not a finite-field
substitute for the proof and not a proof of SP-CLEAN-BRIDGE.
"""

from hashlib import sha256
from itertools import product


P = 5


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def inv(value):
    value %= P
    require(value != 0, "division by zero")
    return pow(value, P - 2, P)


def rref(rows, width=None):
    rows = [[value % P for value in row] for row in rows]
    if width is None:
        width = len(rows[0]) if rows else 0
    rank = 0
    pivots = []
    for column in range(width):
        pivot = next((index for index in range(rank, len(rows))
                      if rows[index][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        scale = inv(rows[rank][column])
        rows[rank] = [(scale * value) % P for value in rows[rank]]
        for index in range(len(rows)):
            if index == rank or not rows[index][column]:
                continue
            scale = rows[index][column]
            rows[index] = [(left - scale * right) % P
                           for left, right in zip(rows[index], rows[rank])]
        pivots.append(column)
        rank += 1
    return tuple(tuple(row) for row in rows), tuple(pivots)


def rank(rows, width=None):
    return len(rref(rows, width)[1])


def row_basis(rows, width=None):
    reduced, pivots = rref(rows, width)
    return tuple(reduced[index] for index in range(len(pivots)))


def nullspace(rows, width):
    reduced, pivots = rref(rows, width)
    free = [column for column in range(width) if column not in pivots]
    answer = []
    for free_column in free:
        vector = [0] * width
        vector[free_column] = 1
        for row, pivot in enumerate(pivots):
            vector[pivot] = (-reduced[row][free_column]) % P
        answer.append(tuple(vector))
    require(all(all(sum(a * b for a, b in zip(row, vector)) % P == 0
                    for row in rows)
                for vector in answer), "bad nullspace")
    return tuple(answer)


def flatten(matrix):
    return tuple(matrix[i][j] % P for i in range(3) for j in range(3))


def outer(left, right):
    return tuple(tuple(left[i] * right[j] % P for j in range(3))
                 for i in range(3))


def hyperplane_basis(vector):
    return nullspace((vector,), 3)


def projective_vectors():
    answer = []
    for vector in product(range(P), repeat=3):
        if not any(vector):
            continue
        pivot = next(value for value in vector if value)
        normalized = tuple(value * inv(pivot) % P for value in vector)
        if normalized == vector:
            answer.append(vector)
    require(len(answer) == P * P + P + 1, len(answer))
    return tuple(answer)


def diagonal_vector(matrix_vector):
    return tuple(matrix_vector[3 * i + i] for i in range(3))


def possible_kernel_subspaces(kernel_basis):
    dimension = len(kernel_basis)
    if dimension == 0:
        return (tuple(),)
    if dimension == 1:
        return (tuple(), (kernel_basis[0],))
    require(dimension == 2, dimension)
    lines = []
    for coefficients in projective_vectors_2():
        vector = tuple((coefficients[0] * kernel_basis[0][index]
                        + coefficients[1] * kernel_basis[1][index]) % P
                       for index in range(9))
        lines.append((vector,))
    require(len(lines) == P + 1, len(lines))
    return (tuple(), *lines, kernel_basis)


def projective_vectors_2():
    answer = []
    for vector in product(range(P), repeat=2):
        if not any(vector):
            continue
        pivot = next(value for value in vector if value)
        normalized = tuple(value * inv(pivot) % P for value in vector)
        if normalized == vector:
            answer.append(vector)
    return tuple(answer)


def span_equal(left, right, width):
    left_rank = rank(left, width)
    right_rank = rank(right, width)
    return (left_rank == right_rank
            == rank(tuple(left) + tuple(right), width))


def audit_pair(left, right, ledger):
    left_basis = hyperplane_basis(left)
    right_basis = hyperplane_basis(right)
    q_basis = tuple(flatten(outer(x, y))
                    for x in left_basis for y in right_basis)
    require(rank(q_basis, 9) == 4, (left, right, "Q rank"))

    # Q^perp is the kernel of restriction Mat_3 -> Q^*.
    q_perp = nullspace(q_basis, 9)
    require(len(q_perp) == 5, (left, right, "Q perp"))

    diagonal_basis = tuple(tuple(1 if index == 3 * i + i else 0
                                 for index in range(9))
                           for i in range(3))
    # The diagonal map in the chosen four-element basis of Q.
    delta_matrix = tuple(tuple(q_basis[column][3 * i + i]
                               for column in range(4))
                         for i in range(3))
    delta_rank = rank(delta_matrix, 4)
    common_missing = [i for i in range(3)
                      if left[i] == 0 and right[i] == 0]
    expected_rank = 2 if common_missing else 3
    require(delta_rank == expected_rank,
            (left, right, delta_rank, common_missing))

    provenance_rows = row_basis(q_perp + diagonal_basis, 9)
    require(len(provenance_rows) == 5 + delta_rank,
            (left, right, "provenance rank", len(provenance_rows)))

    # The annihilator of Delta+Q^perp is exactly ker(delta) inside Q.
    kernel_coefficients = nullspace(delta_matrix, 4)
    kernel_caps = tuple(tuple(sum(coefficients[column]
                                  * q_basis[column][index]
                                  for column in range(4)) % P
                               for index in range(9))
                        for coefficients in kernel_coefficients)
    provenance_annihilator = nullspace(provenance_rows, 9)
    require(span_equal(kernel_caps, provenance_annihilator, 9),
            (left, right, "dual identification"))
    require(len(kernel_caps) == 4 - delta_rank,
            (left, right, "kernel dimension"))
    require(all(not any(diagonal_vector(cap)) for cap in kernel_caps),
            (left, right, "kernel target"))

    if common_missing:
        missing = common_missing[0]
        other = [i for i in range(3) if i != missing]
        i, j = other
        x = tuple(1 if index == i else
                  (-left[i] * inv(left[j])) % P if index == j else 0
                  for index in range(3))
        y = tuple(1 if index == i else
                  (-right[i] * inv(right[j])) % P if index == j else 0
                  for index in range(3))
        missing_axis = tuple(1 if index == missing else 0
                             for index in range(3))
        cross_caps = (flatten(outer(missing_axis, y)),
                      flatten(outer(x, missing_axis)))
        require(span_equal(cross_caps, kernel_caps, 9),
                (left, right, "cross kernel"))

    # K0=ker Phi may be any subspace of ker(delta).  Audit the response
    # functional quotient K0^perp/(Delta+Q^perp) and its dual.
    for kernel0 in possible_kernel_subspaces(kernel_caps):
        k0_basis = row_basis(kernel0, 9)
        k0_perp = nullspace(k0_basis, 9)
        require(rank(provenance_rows + k0_perp, 9) == len(k0_perp),
                (left, right, "bad containment"))
        quotient_dimension = len(k0_perp) - len(provenance_rows)
        require(quotient_dimension == 4 - delta_rank - len(k0_basis),
                (left, right, "quotient dimension", quotient_dimension))
        v_annihilator = nullspace(k0_perp, 9)
        require(span_equal(v_annihilator, k0_basis, 9),
                (left, right, "K0 bidual"))

    ledger.append((left, right, delta_rank, len(kernel_caps),
                   len(provenance_rows)))


def main():
    vectors = tuple(vector for vector in projective_vectors()
                    if sum(value != 0 for value in vector) >= 2)
    require(len(vectors) == 28, len(vectors))
    ledger = []
    for left in vectors:
        for right in vectors:
            audit_pair(left, right, ledger)

    rank_histogram = {}
    for _, _, delta_rank, _, _ in ledger:
        rank_histogram[delta_rank] = rank_histogram.get(delta_rank, 0) + 1
    digest = sha256(repr(ledger).encode()).hexdigest()
    print("projective noncoordinate vectors", len(vectors))
    print("ordered pairs", len(ledger))
    print("diagonal-rank histogram", sorted(rank_histogram.items()))
    print("ledger sha256", digest)


if __name__ == "__main__":
    main()
