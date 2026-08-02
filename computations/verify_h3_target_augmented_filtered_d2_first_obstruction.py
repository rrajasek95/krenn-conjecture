#!/usr/bin/env python3
"""Exact bounded audit of the first target-augmented filtered-d2 obstruction.

This is the scalar selected-row packet from
``notes/h3-target-augmented-filtered-d2-first-obstruction.md``.  It is not
the full all-label EqSystem.  The packet retains

* the two columns of the selected direct matrix ``[[A,B],[F,U]]``;
* its two adjugate rows and curvature ``kappa = A*U-B*F``;
* the literal scalar-zero cap target/residue graph ``(lambda, lambda*Y)``;
* the same-power diagonal-anchor common mode; and
* the curvature/direct-double filtration correction.

All calculations use ``Fraction`` and explicit matrices.  The checker is
unchanged under ``python -O`` because it uses optimization-safe guards.
"""

from fractions import Fraction
from hashlib import sha256
import json


Q = Fraction
ZERO = Q(0)
ONE = Q(1)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def zeros(rows, columns):
    return [[ZERO for _ in range(columns)] for _ in range(rows)]


def matmul(left, right):
    require(not left or len(left[0]) == len(right), "matrix dimensions disagree")
    if not left:
        return []
    return [
        [
            sum(
                (left[row][middle] * right[middle][column]
                 for middle in range(len(right))),
                ZERO,
            )
            for column in range(len(right[0]))
        ]
        for row in range(len(left))
    ]


def add(*matrices):
    require(matrices, "no matrices to add")
    rows = len(matrices[0])
    columns = len(matrices[0][0]) if rows else 0
    require(
        all(len(matrix) == rows and (not rows or len(matrix[0]) == columns)
            for matrix in matrices),
        "matrix shapes disagree",
    )
    return [
        [sum((matrix[row][column] for matrix in matrices), ZERO)
         for column in range(columns)]
        for row in range(rows)
    ]


def rank(matrix):
    if not matrix:
        return 0
    work = [list(row) for row in matrix]
    rows = len(work)
    columns = len(work[0])
    result = 0
    for column in range(columns):
        pivot = next(
            (row for row in range(result, rows) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[result], work[pivot] = work[pivot], work[result]
        pivot_value = work[result][column]
        work[result] = [entry / pivot_value for entry in work[result]]
        for row in range(rows):
            if row == result:
                continue
            coefficient = work[row][column]
            if coefficient:
                work[row] = [
                    entry - coefficient * pivot_entry
                    for entry, pivot_entry in zip(work[row], work[result])
                ]
        result += 1
    return result


def column(matrix, index):
    return [row[index] for row in matrix]


def is_zero(matrix):
    return all(entry == ZERO for row in matrix for entry in row)


def vector_add(*vectors):
    require(vectors, "no vectors to add")
    require(all(len(vector) == len(vectors[0]) for vector in vectors),
            "vector sizes disagree")
    return [sum((vector[index] for vector in vectors), ZERO)
            for index in range(len(vectors[0]))]


def scalar_times(scalar, vector):
    return [scalar * entry for entry in vector]


def apply(matrix, vector):
    return [
        sum((entry * coefficient for entry, coefficient in zip(row, vector)), ZERO)
        for row in matrix
    ]


def packet(A, B, F, U, Y):
    """Return filtration components for one exact rational specialization.

    Bases by cochain degree are

      C^0: (x, e, a),
      C^1: (V1_0,V1_1,V0_0,V0_1,T,R),
      C^2: (z,w).

    Here x is the comparison cell, e is the adjugate middle lift, a is the
    common diagonal-anchor mode, z is the radial curvature row, and w is
    the target-augmented same-power cap relation.  The pair (T,R) records
    target and odd response, so d_cap(T,R)=R-Y*T.
    """
    A, B, F, U, Y = map(Q, (A, B, F, U, Y))
    kappa = A * U - B * F
    require(kappa != 0, "the selected direct minor must be nonzero")

    c1 = [A, F]
    c2 = [B, U]
    lam = [-F, A]
    eta = [U, -B]
    graph = [ONE, Y]

    require(sum((lam[i] * c1[i] for i in range(2)), ZERO) == 0,
            "first adjugate orthogonality failed")
    require(sum((eta[i] * c2[i] for i in range(2)), ZERO) == 0,
            "second adjugate orthogonality failed")
    require(sum((lam[i] * c2[i] for i in range(2)), ZERO) == kappa,
            "lambda did not read the curvature determinant")
    require(sum((eta[i] * c1[i] for i in range(2)), ZERO) == kappa,
            "eta did not read the curvature determinant")

    # Component C^0 -> C^1 matrices.  Columns are x,e,a.
    d0_01 = zeros(6, 3)
    d0_01[0][1], d0_01[1][1] = c1

    dm1_01 = zeros(6, 3)
    dm1_01[0][0], dm1_01[1][0] = scalar_times(-ONE, c1)
    dm1_01[2][1], dm1_01[3][1] = c2
    dm1_01[4][1], dm1_01[5][1] = scalar_times(-kappa, graph)
    dm1_01[4][2], dm1_01[5][2] = graph

    dm2_01 = zeros(6, 3)
    dm2_01[2][0], dm2_01[3][0] = scalar_times(-ONE, c2)

    # Component C^1 -> C^2 matrices.  Rows are z,w.
    d0_12 = zeros(2, 6)
    d0_12[0][2], d0_12[0][3] = lam
    d0_12[1][4], d0_12[1][5] = -Y, ONE

    dm1_12 = zeros(2, 6)
    dm1_12[0][0], dm1_12[0][1] = scalar_times(-ONE, eta)

    dm2_12 = zeros(2, 6)

    # Every filtration component of d^2 is checked separately.
    drop0 = matmul(d0_12, d0_01)
    drop1 = add(matmul(d0_12, dm1_01), matmul(dm1_12, d0_01))
    drop2 = add(
        matmul(d0_12, dm2_01),
        matmul(dm1_12, dm1_01),
        matmul(dm2_12, d0_01),
    )
    require(is_zero(drop0), "d0^2 is nonzero")
    require(is_zero(drop1), "d0*d-1+d-1*d0 is nonzero")
    require(is_zero(drop2), "drop-two d^2 component is nonzero")

    total_01 = add(d0_01, dm1_01, dm2_01)
    total_12 = add(d0_12, dm1_12, dm2_12)
    require(is_zero(matmul(total_12, total_01)), "the total differential does not square")

    # Lemma 2.1: d_-1 x=-c1 and d0(e)=c1, hence y=e.  The V0
    # contributions cancel and the target-augmented d2 representative is
    # precisely the curvature-weighted scalar-zero cap graph.
    x = [ONE, ZERO, ZERO]
    y = [ZERO, ONE, ZERO]
    beta = vector_add(apply(dm2_01, x), apply(dm1_01, y))
    expected_beta = [ZERO, ZERO, ZERO, ZERO, -kappa, -kappa * Y]
    require(beta == expected_beta, "wrong filtered d2 representative")
    require(apply(d0_12, beta) == [ZERO, ZERO], "d2 representative is not a d0-cycle")

    # The common diagonal-anchor mode a is a d0-cycle and its first
    # differential is exactly the target/residue graph.  Thus beta is a
    # first-page boundary, not the requested secondary class.
    a = [ZERO, ZERO, ONE]
    common_mode = apply(dm1_01, a)
    expected_common = [ZERO, ZERO, ZERO, ZERO, ONE, Y]
    require(common_mode == expected_common, "wrong common anchor mode")
    require(beta == scalar_times(-kappa, common_mode),
            "d2 did not die by the literal common mode")

    # H^1(G0,d0) has the V0 kernel c1 and the cap graph.  The latter is
    # precisely the d1 indeterminacy; the E2 quotient is one-dimensional,
    # but beta is zero in it.
    g0_d0 = [
        [lam[0], lam[1], ZERO, ZERO],
        [ZERO, ZERO, -Y, ONE],
    ]
    require(rank(g0_d0) == 2, "unexpected low d0 rank")
    g0_kernel_dimension = 4 - rank(g0_d0)
    indeterminacy = [[ZERO, ZERO, ONE, Y]]
    require(rank(indeterminacy) == 1, "common-mode indeterminacy vanished")
    e2_dimension = g0_kernel_dimension - rank(indeterminacy)
    require(e2_dimension == 1, "unexpected bounded E2 dimension")

    # The desired target-zero response is not a cycle in the literal
    # target-augmented same-power complex.  Its d0 image is the exact first
    # missing d^2 row.  Deleting the target coordinate sees the desired
    # number but is therefore not a chain operation.
    desired = [ZERO, ZERO, ZERO, ZERO, ZERO, -kappa * Y]
    desired_defect = apply(d0_12, desired)
    require(desired_defect == [ZERO, -kappa * Y],
            "wrong target-zero cap-relation defect")
    require(desired_defect != [ZERO, ZERO],
            "the requested target-zero response accidentally became a cycle")

    # Omitting the direct curvature correction leaves exactly kappa*z in
    # the drop-two square.  This is the adjugate/Koszul curvature readout.
    omitted_curvature = add(
        matmul(dm1_12, dm1_01),
        matmul(dm2_12, d0_01),
    )
    require(column(omitted_curvature, 0) == [kappa, ZERO],
            "omitted curvature correction did not leave kappa*z")

    # Replacing the literal graph cap in d_-1(e) by the hoped-for
    # target-zero pair breaks the drop-one square by -kappa*Y*w.
    mutated_dm1_01 = [list(row) for row in dm1_01]
    mutated_dm1_01[4][1] = ZERO
    mutated_dm1_01[5][1] = -kappa * Y
    mutated_drop1 = add(
        matmul(d0_12, mutated_dm1_01),
        matmul(dm1_12, d0_01),
    )
    require(column(mutated_drop1, 1) == [ZERO, -kappa * Y],
            "target-zero mutation did not expose the missing d^2 row")

    # The pair-valued target/residue projection cannot descend through d1:
    # it is nonzero on the common mode.  The only scalar graph-annihilator
    # R-Y*T vanishes on beta as well.
    pair_readout_on_indeterminacy = common_mode[4:6]
    graph_annihilator_on_beta = beta[5] - Y * beta[4]
    require(pair_readout_on_indeterminacy == graph,
            "pair readout unexpectedly killed the common mode")
    require(graph_annihilator_on_beta == 0,
            "graph-annihilating scalar readout did not kill d2")

    return {
        "A": str(A),
        "B": str(B),
        "F": str(F),
        "U": str(U),
        "Y": str(Y),
        "kappa": str(kappa),
        "direct_free": B == 0,
        "total_ranks": [rank(total_01), rank(total_12)],
        "g0_kernel_dimension": g0_kernel_dimension,
        "e2_dimension": e2_dimension,
        "d2_pair": [str(beta[4]), str(beta[5])],
        "desired_d2_defect": [str(value) for value in desired_defect],
        "omitted_curvature_defect": [str(value) for value in column(omitted_curvature, 0)],
    }


def main():
    samples = (
        (Q(2), Q(3), Q(5), Q(11), Q(7, 5)),
        (Q(3), Q(0), Q(2), Q(5), Q(-4, 9)),  # direct-free B=0
        (Q(-2), Q(7), Q(3), Q(-5), Q(13, 6)),
        (Q(5, 3), Q(-7, 4), Q(11, 5), Q(2, 9), Q(-8, 7)),
    )
    records = [packet(*sample) for sample in samples]
    payload = json.dumps(records, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode("utf-8")).hexdigest()
    print("h=3 target-augmented filtered-d2 first obstruction: PASS")
    print("exact rational packets:", len(records))
    print("direct-free packets:", sum(record["direct_free"] for record in records))
    print("d2: curvature-weighted cap graph, zero modulo common anchor mode")
    print("forced target-zero replacement: noncycle with defect -kappa*Y")
    print("sha256:", digest)


if __name__ == "__main__":
    main()
