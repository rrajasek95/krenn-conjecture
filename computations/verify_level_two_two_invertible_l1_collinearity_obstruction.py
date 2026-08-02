#!/usr/bin/env python3
"""Exact overlapping-L1 obstruction for the 2I incidence survivor.

One normalized invertible edge leaves an aligned endpoint mode and one
antisymmetric skew mode.  Comparing the two incident equations at a
rank-one site whose selected columns are both nonzero kills the skew.
Two-column rank-one sites then align with the same scalar.  An invertible
core-to-zero spoke kills both zero-site endpoint families.

For the exact rank-55/53 survivor these hypotheses hold, so every endpoint
slice is a generalized cut gauge and both pure L0 targets would be
collinear with one residual matching tensor.  Standard library only.
"""

from fractions import Fraction as Q
from pathlib import Path
from runpy import run_path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


HERE = Path(__file__).resolve().parent
source = run_path(str(
    HERE / "verify_level_two_two_invertible_l0_incidence_survivor.py"
))
aligned = run_path(str(
    HERE
    / "verify_level_two_three_invertible_l1_pure_l0_collinearity_obstruction.py"
))


def rational_rank(matrix):
    rows = [[Q(value) for value in row] for row in matrix]
    rank = 0
    width = len(rows[0]) if rows else 0
    for column in range(width):
        pivot = next(
            (row for row in range(rank, len(rows)) if rows[row][column]),
            None,
        )
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        scale = rows[rank][column]
        rows[rank] = [value / scale for value in rows[rank]]
        for row in range(len(rows)):
            if row == rank or not rows[row][column]:
                continue
            multiple = rows[row][column]
            rows[row] = [
                left - multiple * right
                for left, right in zip(rows[row], rows[rank])
            ]
        rank += 1
    return rank


def matrix_vector_product(matrix, vector):
    return [
        sum(Q(value) * coordinate for value, coordinate in zip(row, vector))
        for row in matrix
    ]


def outer(left, right):
    return tuple(
        tuple(left[row] * right[column] for column in range(2))
        for row in range(2)
    )


def add_matrix(left, right):
    return tuple(
        tuple(left[row][column] + right[row][column] for column in range(2))
        for row in range(2)
    )


def scale_matrix(coefficient, matrix):
    return tuple(
        tuple(coefficient * matrix[row][column] for column in range(2))
        for row in range(2)
    )


def flatten(matrix):
    return tuple(value for row in matrix for value in row)


def coefficient_matrix(residual, width):
    columns = []
    for basis in range(width):
        vector = [Q(0)] * width
        vector[basis] = Q(1)
        columns.append(tuple(residual(vector)))
    return [list(row) for row in zip(*columns)]


def audit_invertible_edge_modes():
    # P/V variables are x0,y0,x1,y1,d.  The edge equation is
    # e0 V1^T+V0 e0^T=dJ.
    pv = [
        [1, 0, 1, 0, 0],
        [0, 0, 0, 1, -1],
        [0, 1, 0, 0, -1],
    ]
    pv_aligned = tuple(map(Q, (0, 1, 0, 1, 1)))
    pv_skew = tuple(map(Q, (1, 0, -1, 0, 0)))
    require(rational_rank(pv) == 3,
            "the P/V invertible-edge system rank changed")
    require(not any(matrix_vector_product(pv, pv_aligned))
            and not any(matrix_vector_product(pv, pv_skew)),
            "the P/V edge generators changed")
    require(rational_rank((pv_aligned, pv_skew)) == 2,
            "the P/V generators became dependent")

    # U/Q variables use e1 U1^T+U0 e1^T=dJ.
    uq = [
        [1, 0, -1, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 1, 0, -1],
    ]
    # Write variables as x0,y0,x1,y1,d.  Alignment is U0=U1=e0;
    # skew is U0=e1,U1=-e1.
    uq_aligned = tuple(map(Q, (1, 0, 1, 0, 1)))
    uq_skew = tuple(map(Q, (0, 1, 0, -1, 0)))
    require(rational_rank(uq) == 3,
            "the U/Q invertible-edge system rank changed")
    require(not any(matrix_vector_product(uq, uq_aligned))
            and not any(matrix_vector_product(uq, uq_skew)),
            "the U/Q edge generators changed")
    require(rational_rank((uq_aligned, uq_skew)) == 2,
            "the U/Q generators became dependent")
    return (3, 2), (3, 2)


def audit_rank_one_propagation():
    e0 = (Q(1), Q(0))
    e1 = (Q(0), Q(1))
    h = (Q(3), Q(4))
    p, q = Q(2), Q(5)
    p_t = tuple(p * value for value in h)
    q_t = tuple(q * value for value in h)

    # Variables are Vt0,Vt1,b,x,d0,d1.  At i=0,1,
    # Vi=b e1+epsilon_i x e0 and
    # e0 Vt^T+Vi Pt^T=d_i(e0 Qt^T+e1 Pt^T).
    def pv_residual(vector):
        v_t = tuple(vector[index] for index in (0, 1))
        b, skew = vector[2], vector[3]
        answer = []
        for i, epsilon in enumerate((1, -1)):
            v_i = (epsilon * skew, b)
            numerator = add_matrix(outer(e0, q_t), outer(e1, p_t))
            left = add_matrix(outer(e0, v_t), outer(v_i, p_t))
            answer.extend(flatten(add_matrix(
                left, scale_matrix(-vector[4 + i], numerator)
            )))
        return answer

    pv = coefficient_matrix(pv_residual, 6)
    pv_generator = tuple(q * value for value in h) + (Q(1), Q(0), Q(1), Q(1))
    require(rational_rank(pv) == 5,
            "the rank-one P/V propagation rank changed")
    require(not any(matrix_vector_product(pv, pv_generator)),
            "V_t=b Q_t did not generate the propagation kernel")

    # Variables are Ut0,Ut1,a,y,d0,d1, with
    # Ui=a e0+epsilon_i y e1 and the transposed L1 equation.
    def uq_residual(vector):
        u_t = tuple(vector[index] for index in (0, 1))
        a, skew = vector[2], vector[3]
        answer = []
        for i, epsilon in enumerate((1, -1)):
            u_i = (a, epsilon * skew)
            numerator = add_matrix(outer(e0, q_t), outer(e1, p_t))
            left = add_matrix(outer(e1, u_t), outer(u_i, q_t))
            answer.extend(flatten(add_matrix(
                left, scale_matrix(-vector[4 + i], numerator)
            )))
        return answer

    uq = coefficient_matrix(uq_residual, 6)
    uq_generator = tuple(p * value for value in h) + (Q(1), Q(0), Q(1), Q(1))
    require(rational_rank(uq) == 5,
            "the rank-one U/Q propagation rank changed")
    require(not any(matrix_vector_product(uq, uq_generator)),
            "U_t=a P_t did not generate the propagation kernel")
    return rational_rank(pv), rational_rank(uq)


def determinant(matrix):
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def audit_exact_survivor():
    source["audit_replacement_scope"]()
    checked, slope = source["guard"]["audit_generic_kernel_and_selected_rows"]()
    ranks = source["guard"]["audit_rank_and_kernel"]()
    r2 = source["guard"]["audit_r2"]()
    source["audit_l0_incidence"]()

    x = source["guard"]["X"]
    for site in (2, 3):
        p_t = tuple(x[site][row][0] for row in range(2))
        q_t = tuple(x[site][row][1] for row in range(2))
        require(any(p_t) and any(q_t),
                ("a rank-one site lost one selected column", site))

    blocks = source["BLOCKS"]
    det34 = determinant(blocks[3, 4])
    det05 = determinant(blocks[0, 5])
    require((det34, det05) == (-87, 2352),
            ("zero-site witness determinants changed", det34, det05))
    return checked, ranks, len(r2), sum(value != 0 for value in slope), (
        det34, det05,
    )


def main():
    edge_modes = audit_invertible_edge_modes()
    propagation = audit_rank_one_propagation()
    exact = audit_exact_survivor()
    edge_checks = aligned["audit_aligned_slice_is_generalized_gauge"]()
    matching_checks = aligned["audit_generalized_gauge_differential"]()
    target_checks = aligned["audit_pure_target_unit_certificate"]()
    print("two-invertible L1 collinearity obstruction: all checks passed")
    print(f"  invertible-edge ranks/modes : {edge_modes}")
    print(f"  rank-one propagation ranks  : {propagation}")
    print(f"  exact survivor audits       : {exact}")
    print(f"  aligned gauge edges         : {edge_checks}/15")
    print(f"  matching derivative terms   : {matching_checks}/15")
    print(f"  pure collinearity equations : {target_checks}, ideal (1)")


if __name__ == "__main__":
    main()
