#!/usr/bin/env python3
"""Verify the scoped 3I+1R+2Z L1/L0 cut normal form.

On the rank-55 branch where the five gauges are independent and exhaust the
kernel, assume the selected endpoint matrices have ranks (2,2,2,1,0,0), the
potentials are

    (tau,tau,tau,tau,-tau,-tau),

both selected columns at the rank-one site are nonzero, and each zero site
has an invertible spoke to the invertible triangle.  The overlapping L1
equations align every binary endpoint vector with the selected columns.  The
two mixed L0 slices consequently have the same core-versus-zero cut gauge;
they do not supply a one-star kernel.  The pure-triangle determinant cover
then reduces to a scalar identity and adds no further restriction.

This standard-library checker audits the exact linear and polynomial
identities used in that argument.  All checks remain live under ``-O`` and
``-I -S``.
"""

from fractions import Fraction as Q
from itertools import combinations


INNER = (0, 1, 2)
RANK_ONE = 3
ZEROS = (4, 5)
SITES = INNER + (RANK_ONE,) + ZEROS


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def rational_rank(matrix):
    rows = [[Q(entry) for entry in row] for row in matrix]
    height = len(rows)
    width = len(rows[0]) if rows else 0
    rank = 0
    for column in range(width):
        pivot = next(
            (row for row in range(rank, height) if rows[row][column]), None
        )
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        pivot_value = rows[rank][column]
        rows[rank] = [entry / pivot_value for entry in rows[rank]]
        for row in range(height):
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
        sum(Q(entry) * coordinate for entry, coordinate in zip(row, vector))
        for row in matrix
    ]


def triangle_alignment_system(left_selected):
    """L1 equations on the normalized invertible triangle.

    Variables are x0,y0,x1,y1,x2,y2,c01,c02,c12.  For the P/V equation,
    P_i=e0 and

        e0 v_j^T + v_i e0^T = c_ij J.

    For the U/Q equation, Q_i=e1 and the displayed equation is transposed.
    """

    pairs = tuple(combinations(INNER, 2))
    scalar_column = {pair: 6 + index for index, pair in enumerate(pairs)}
    equations = []

    def equation(entries):
        row = [Q(0)] * 9
        for column, coefficient in entries.items():
            row[column] += Q(coefficient)
        equations.append(row)

    for i, j in pairs:
        c = scalar_column[i, j]
        if left_selected == "P":
            # [[x_i+x_j, y_j], [y_i, 0]] = c_ij J.
            equation({2 * i: 1, 2 * j: 1})
            equation({2 * j + 1: 1, c: -1})
            equation({2 * i + 1: 1, c: -1})
        else:
            # [[0, x_i], [x_j, y_i+y_j]] = c_ij J.
            equation({2 * i: 1, c: -1})
            equation({2 * j: 1, c: -1})
            equation({2 * i + 1: 1, 2 * j + 1: 1})
    return equations


def audit_triangle_alignment():
    pv = triangle_alignment_system("P")
    uq = triangle_alignment_system("Q")
    pv_generator = tuple(map(Q, (0, 1, 0, 1, 0, 1, 1, 1, 1)))
    uq_generator = tuple(map(Q, (1, 0, 1, 0, 1, 0, 1, 1, 1)))
    require(rational_rank(pv) == 8, "P/V triangle system is not rank eight")
    require(rational_rank(uq) == 8, "U/Q triangle system is not rank eight")
    require(not any(matrix_vector_product(pv, pv_generator)),
            "constant Q-column did not solve the P/V system")
    require(not any(matrix_vector_product(uq, uq_generator)),
            "constant P-column did not solve the U/Q system")


def audit_rank_one_site_alignment():
    # Once the I-triangle scalar is b, comparison in the basis (P_i,Q_i)
    # gives V_t=k Q_t and (b-k)P_t=0.  A nonzero P_t forces k=b.
    # The chosen proportional selected columns P_t=(2,3), Q_t=(10,15)
    # make the exact coefficient system concrete without losing rank.
    pv = [
        [1, 0, -10, 0],
        [0, 1, -15, 0],
        [0, 0, -2, 2],
        [0, 0, -3, 3],
    ]
    pv_generator = tuple(map(Q, (10, 15, 1, 1)))
    require(rational_rank(pv) == 3, "rank-one P/V comparison changed")
    require(not any(matrix_vector_product(pv, pv_generator)),
            "V_t=b Q_t did not solve the comparison")

    # The U/Q comparison is U_t=k P_t and (a-k)Q_t=0.
    uq = [
        [1, 0, -2, 0],
        [0, 1, -3, 0],
        [0, 0, -10, 10],
        [0, 0, -15, 15],
    ]
    uq_generator = tuple(map(Q, (2, 3, 1, 1)))
    require(rational_rank(uq) == 3, "rank-one U/Q comparison changed")
    require(not any(matrix_vector_product(uq, uq_generator)),
            "U_t=a P_t did not solve the comparison")


# A tiny sparse polynomial ring for determinant identities.


def constant(value):
    return {(): Q(value)} if value else {}


def variable(name):
    return {(name,): Q(1)}


def add(*polynomials):
    answer = {}
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            answer[monomial] = answer.get(monomial, Q(0)) + coefficient
            if not answer[monomial]:
                del answer[monomial]
    return answer


def scale(coefficient, polynomial):
    return {
        monomial: Q(coefficient) * value
        for monomial, value in polynomial.items()
        if coefficient * value
    }


def multiply(left, right):
    answer = {}
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            monomial = tuple(sorted(left_monomial + right_monomial))
            answer[monomial] = (
                answer.get(monomial, Q(0))
                + left_coefficient * right_coefficient
            )
            if not answer[monomial]:
                del answer[monomial]
    return answer


def determinant(matrix):
    return add(
        multiply(matrix[0][0], matrix[1][1]),
        scale(-1, multiply(matrix[0][1], matrix[1][0])),
    )


def audit_zero_site_rank_argument():
    # On an I-Z edge the L1 equation is P_i V_z^T=rho M_iz.  Its left
    # side has determinant zero, whereas an invertible M gives
    # det(rho M)=rho^2 det(M).  Hence rho=0 and then V_z=0 because P_i!=0.
    p0, p1 = variable("p0"), variable("p1")
    v0, v1 = variable("v0"), variable("v1")
    rho = variable("rho")
    outer = (
        (multiply(p0, v0), multiply(p0, v1)),
        (multiply(p1, v0), multiply(p1, v1)),
    )
    require(determinant(outer) == {}, "rank-one outer product gained rank")

    matrix = tuple(
        tuple(variable(f"m{row}{column}") for column in range(2))
        for row in range(2)
    )
    scaled = tuple(
        tuple(multiply(rho, matrix[row][column]) for column in range(2))
        for row in range(2)
    )
    require(
        determinant(scaled)
        == multiply(multiply(rho, rho), determinant(matrix)),
        "det(rho M)=rho^2 det(M) failed",
    )


def audit_cut_potential():
    # Variables are lambda_0,...,lambda_5,c.  The triangle and I-t edges
    # have numerator 2c M.  One invertible I-Z witness at each zero has
    # numerator zero.  These equations force c(1,1,1,1,-1,-1).
    equations = []

    def potential_equation(u, v, multiple):
        row = [Q(0)] * 7
        row[u] = Q(1)
        row[v] = Q(1)
        row[6] = Q(-multiple)
        equations.append(row)

    for u, v in combinations(INNER, 2):
        potential_equation(u, v, 2)
    for u in INNER:
        potential_equation(u, RANK_ONE, 2)
    potential_equation(0, 4, 0)
    potential_equation(1, 5, 0)

    generator = tuple(map(Q, (1, 1, 1, 1, -1, -1, 1)))
    require(rational_rank(equations) == 6, "cut-potential system rank changed")
    require(not any(matrix_vector_product(equations, generator)),
            "the core-versus-zero cut failed the potential equations")

    c = Q(7, 5)
    lambdas = (c, c, c, c, -c, -c)
    direct = -sum(lambdas)
    require(direct == -2 * c, "mixed direct coefficient is not -2c")
    gauge = tuple(value + direct / 6 for value in lambdas)
    require(sum(gauge) == 0, "adjusted cut weights are not trace zero")

    core_adjusted = 2 * c + direct / 3
    cross_adjusted = direct / 3
    require(core_adjusted == gauge[0] + gauge[1] == 4 * c / 3,
            "core adjusted coefficient is not the cut gauge")
    require(cross_adjusted == gauge[0] + gauge[4] == -2 * c / 3,
            "cross adjusted coefficient is not the cut gauge")
    require(gauge[4] + gauge[5] == -8 * c / 3,
            "zero-zero gauge coefficient changed")
    # M_45=0 in the selected potential normal form, so the last coefficient
    # multiplies the zero block.

    # A live core edge 12 and an invertible cross edge 04 are disjoint.
    # Their nonzero adjusted coefficients exclude support on one star.
    require(core_adjusted and cross_adjusted,
            "the nonzero cut specialization collapsed")
    require(set((1, 2)).isdisjoint((0, 4)),
            "the two live cut witnesses unexpectedly share a centre")


def audit_pure_triangle_cover():
    x = tuple(
        tuple(variable(f"x{row}{column}") for column in range(2))
        for row in range(2)
    )
    a, b = variable("a"), variable("b")
    aligned = (
        (multiply(a, x[0][0]), multiply(b, x[0][1])),
        (multiply(a, x[1][0]), multiply(b, x[1][1])),
    )
    require(
        determinant(aligned) == multiply(multiply(a, b), determinant(x)),
        "aligned pure determinant did not scale by ab",
    )

    a0, a1 = variable("a0"), variable("a1")
    b0, b1 = variable("b0"), variable("b1")
    pure_product = multiply(multiply(a0, b0), multiply(a1, b1))
    mixed_product = multiply(multiply(a0, b1), multiply(a1, b0))
    require(pure_product == mixed_product,
            "pure/mixed scalar product identity failed")


def main():
    audit_triangle_alignment()
    audit_rank_one_site_alignment()
    audit_zero_site_rank_argument()
    audit_cut_potential()
    audit_pure_triangle_cover()
    print("verified L1 scalar alignment on the invertible triangle")
    print("verified alignment at a two-column rank-one site")
    print("verified invertible I-Z spokes kill zero-site L0 vectors")
    print("verified the mixed L0 packet is the core/zero cut gauge")
    print("verified the pure-triangle cover becomes automatic")


if __name__ == "__main__":
    main()
