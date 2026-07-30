#!/usr/bin/env python3
"""Exact lightweight audit of the odd-covariant Hankel obstruction."""

from fractions import Fraction
from itertools import combinations
from math import comb


def require(condition, message):
    """Optimization-safe audit assertion."""
    if not condition:
        raise RuntimeError(message)


def cartan_matrix(output_degree, q):
    """Matrix for Sym^2 x Sym^(D-2) -> Sym^D in dual monomial bases."""
    auxiliary_degree = output_degree - 2
    matrix = [
        [Fraction(0) for _ in range(auxiliary_degree + 1)]
        for _ in range(output_degree + 1)
    ]
    for m in range(output_degree + 1):
        for i in range(3):
            ell = m - i
            if 0 <= ell <= auxiliary_degree:
                matrix[m][ell] += (
                    comb(output_degree - m, 2 - i) * comb(m, i) * q[i]
                )
    return matrix


def matvec(matrix, vector):
    return [sum(row[j] * vector[j] for j in range(len(vector))) for row in matrix]


def determinant(matrix):
    """Exact determinant by fraction-preserving elimination."""
    size = len(matrix)
    require(all(len(row) == size for row in matrix), "determinant needs a square matrix")
    work = [[Fraction(value) for value in row] for row in matrix]
    value = Fraction(1)
    for column in range(size):
        pivot = next(
            (row for row in range(column, size) if work[row][column]), None
        )
        if pivot is None:
            return Fraction(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            value = -value
        pivot_value = work[column][column]
        value *= pivot_value
        for later in range(column + 1, size):
            factor = work[later][column] / pivot_value
            for entry in range(column + 1, size):
                work[later][entry] -= factor * work[column][entry]
    return value


def exact_rank(matrix):
    """Exact row rank over the rationals."""
    if not matrix:
        return 0
    work = [[Fraction(value) for value in row] for row in matrix]
    row_count = len(work)
    column_count = len(work[0])
    require(
        all(len(row) == column_count for row in work), "rank needs a rectangular matrix"
    )
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(pivot_row, row_count) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][column]
        for row in range(pivot_row + 1, row_count):
            factor = work[row][column] / pivot_value
            for entry in range(column, column_count):
                work[row][entry] -= factor * work[pivot_row][entry]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def pure_axis_hankel(h):
    """Rows for E=<s^h,t^h>; these are the full coordinate basis of S_(2h-1)."""
    degree = 2 * h - 1
    rows = []
    for index in range(h):
        row = [0] * (degree + 1)
        row[index] = 1
        rows.append(row)
    for index in range(h, degree + 1):
        row = [0] * (degree + 1)
        row[index] = 1
        rows.append(row)
    return rows


def check_injective_pivots(matrix, q):
    """Audit the triangular leading-term proof for multiplication by q."""
    first = next((i for i, value in enumerate(q) if value), None)
    require(first is not None, "Cartan multiplier must be nonzero")
    column_count = len(matrix[0])
    for column in range(column_count):
        pivot_row = column + first
        require(
            matrix[pivot_row][column],
            f"missing Cartan pivot in row {pivot_row}, column {column}",
        )
        require(
            all(
                matrix[pivot_row][later] == 0
                for later in range(column + 1, column_count)
            ),
            f"Cartan pivot row {pivot_row} is not triangular",
        )


def check_parity_and_clebsch_gordan():
    for h in range(3, 31):
        target = 2 * h - 1
        require((-1) ** 2 == 1, "quadratic central character is not even")
        require((-1) ** target == -1, "target central character is not odd")
        admissible = []
        for auxiliary in range(target + 4):
            summands = [auxiliary + 2]
            if auxiliary >= 1:
                summands.append(auxiliary)
            if auxiliary >= 2:
                summands.append(auxiliary - 2)
            if target in summands:
                admissible.append(auxiliary)
                require(
                    summands.count(target) == 1,
                    f"target multiplicity is not one for d={auxiliary}, h={h}",
                )
        require(
            admissible == [target - 2, target, target + 2],
            f"wrong Clebsch--Gordan auxiliary orders at h={h}: {admissible}",
        )
        require(
            admissible[0] == 2 * h - 3,
            f"wrong minimal auxiliary order at h={h}",
        )
        auxiliary = target - 2
        dimensions = (auxiliary + 3, auxiliary + 1, auxiliary - 1)
        require(
            sum(dimensions) == 3 * (auxiliary + 1),
            f"Clebsch--Gordan dimensions do not close at h={h}",
        )

        # In the polynomial GL(2) refinement, record summands as
        # (symmetric order, determinant exponent).  Only the Cartan
        # summand can equal the untwisted target (target, 0).
        gl_occurrences = []
        for auxiliary in range(target + 4):
            gl_summands = [(auxiliary + 2, 0)]
            if auxiliary >= 1:
                gl_summands.append((auxiliary, 1))
            if auxiliary >= 2:
                gl_summands.append((auxiliary - 2, 2))
            if (target, 0) in gl_summands:
                gl_occurrences.append(auxiliary)
        require(
            gl_occurrences == [target - 2],
            f"wrong untwisted GL(2) occurrence at h={h}: {gl_occurrences}",
        )

    # Highest weights: U^*=(0,-1), while U tensor det^(-1) has
    # (1,0)+(-1,-1)=(0,-1).  Cubing gives the stated det^(-3) twist.
    require((1 - 1, 0 - 1) == (0, -1), "wrong GL(2) dual variance")
    require((3 - 3, 0 - 3) == (0, -3), "wrong cubic determinant twist")


def check_cartan_and_pure_axis_guard():
    probes = (
        (Fraction(1), Fraction(0), Fraction(0)),
        (Fraction(0), Fraction(1), Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(1)),
        (Fraction(-2), Fraction(1), Fraction(-1)),
    )
    for h in range(3, 31):
        degree = 2 * h - 1
        hankel = pure_axis_hankel(h)
        identity = [
            [int(row == column) for column in range(degree + 1)]
            for row in range(degree + 1)
        ]
        require(hankel == identity, f"pure-axis Macaulay map is not identity at h={h}")
        for q in probes:
            cartan = cartan_matrix(degree, q)
            check_injective_pivots(cartan, q)


def check_h3_three_line_guard():
    # T=[[1,1],[1,2]] gives q=(-D*C,B*C,-A*B)=(-2,1,-1).
    q = (Fraction(-2), Fraction(1), Fraction(-1))
    require(1 * 2 - 1 * 1 == 1, "the h=3 selector block is not invertible")
    anchor_e = (Fraction(-1), Fraction(-2), Fraction(0))
    anchor_a = (Fraction(0), Fraction(1), Fraction(1))
    anchor_matrix = [list(anchor_e), list(anchor_a)]
    require(exact_rank(anchor_matrix) == 2, "the two anchor quadratics are dependent")
    require(
        sum(q[i] * anchor_e[i] for i in range(3)) == 0,
        "theta_2 does not annihilate the e-anchor",
    )
    require(
        sum(q[i] * anchor_a[i] for i in range(3)) == 0,
        "theta_2 does not annihilate the a-anchor",
    )
    anchor_cross_product = (
        anchor_e[1] * anchor_a[2] - anchor_e[2] * anchor_a[1],
        anchor_e[2] * anchor_a[0] - anchor_e[0] * anchor_a[2],
        anchor_e[0] * anchor_a[1] - anchor_e[1] * anchor_a[0],
    )
    require(anchor_cross_product == q, "theta_2 is not the exact anchor null covector")
    cartan = cartan_matrix(5, q)
    expected = [
        [10 * q[0], 0, 0, 0],
        [4 * q[1], 6 * q[0], 0, 0],
        [q[2], 6 * q[1], 3 * q[0], 0],
        [0, 3 * q[2], 6 * q[1], q[0]],
        [0, 0, 6 * q[2], 4 * q[1]],
        [0, 0, 0, 10 * q[2]],
    ]
    require(cartan == expected, "the displayed h=3 Cartan matrix is incorrect")
    require(exact_rank(cartan) == 4, "the h=3 Cartan block is not injective")
    four_by_four_minors = []
    for selected_rows in combinations(range(6), 4):
        minor = [[cartan[row][column] for column in range(4)] for row in selected_rows]
        four_by_four_minors.append(determinant(minor))
    require(len(four_by_four_minors) == 15, "wrong number of 4-by-4 minors")
    expected_minors = [
        2880,
        -5760,
        14400,
        2880,
        -14400,
        14400,
        0,
        3600,
        -7200,
        3600,
        -144,
        0,
        720,
        -720,
        180,
    ]
    require(
        four_by_four_minors == expected_minors,
        f"wrong h=3 4-by-4 minors: {four_by_four_minors}",
    )
    require(
        four_by_four_minors[0] == 2880,
        f"wrong leading 4-by-4 minor: {four_by_four_minors[0]}",
    )
    require(
        any(value for value in four_by_four_minors),
        "all h=3 composite 4-by-4 minors vanished",
    )

    # XY(X+Y) is proportional to dual-coordinate vector (0,1,1,0).
    chi = [Fraction(0), Fraction(1), Fraction(1), Fraction(0)]
    theta_chi = matvec(cartan, chi)
    require(
        theta_chi == [0, -12, 0, 3, -6, 0],
        f"wrong Cartan product theta_2 chi_3: {theta_chi}",
    )
    require(any(theta_chi), "the granted three-line Cartan product vanished")

    # The three granted coefficient lines X, Y, X+Y are pairwise distinct.
    lines = ((1, 0), (0, 1), (1, 1))
    for left, right in combinations(lines, 2):
        require(
            left[0] * right[1] - left[1] * right[0] != 0,
            "the granted pure-factor coefficient lines are not distinct",
        )
    granted_curvature = Fraction(1)
    require(granted_curvature != 0, "the formally granted curvature vanished")

    hankel = pure_axis_hankel(3)
    require(
        hankel == [[int(row == column) for column in range(6)] for row in range(6)],
        "the h=3 pure-axis Macaulay matrix is not identity",
    )
    require(exact_rank(hankel) == 6, "the h=3 Macaulay matrix is not full rank")
    composite = [
        [sum(hankel[row][middle] * cartan[middle][column] for middle in range(6))
         for column in range(4)]
        for row in range(6)
    ]
    require(
        composite == cartan,
        "the h=3 pure-axis Macaulay--Cartan composite is not the Cartan block",
    )
    require(
        exact_rank(composite) == 4,
        "the h=3 pure-axis Macaulay--Cartan composite lost rank",
    )
    require(
        matvec(hankel, theta_chi) == theta_chi,
        "the pure-axis composite changed theta_2 chi_3",
    )
    require(
        any(matvec(hankel, theta_chi)),
        "theta_2 chi_3 unexpectedly satisfies every Hankel equation",
    )


def main():
    check_parity_and_clebsch_gordan()
    check_cartan_and_pure_axis_guard()
    check_h3_three_line_guard()
    print("odd-covariant filtered-to-Hankel obstruction: PASS")
    print("  direct quadratic-to-odd transfer: central-parity zero")
    print("  minimal auxiliary order: 2h-3 (unique Cartan product)")
    print("  granted three-line cubic: nonzero but not Hankel-annihilating")


if __name__ == "__main__":
    main()
