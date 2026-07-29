#!/usr/bin/env python3
"""Exact checks for the five-core Cauchy audit.

The calculations use low-level SymPy polynomial domains, so no floating-point
or random specialization enters the certificate.
"""

from sympy.polys.domains import QQ
from sympy.polys.rings import ring


def determinant(matrix, field):
    """Exact Gaussian determinant over ``field``."""
    matrix = [row[:] for row in matrix]
    size = len(matrix)
    answer = field.one
    for column in range(size):
        pivot = next(
            row for row in range(column, size) if matrix[row][column]
        )
        if pivot != column:
            matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
            answer = -answer
        value = matrix[column][column]
        answer *= value
        for j in range(column, size):
            matrix[column][j] /= value
        for row in range(column + 1, size):
            value = matrix[row][column]
            if value:
                for j in range(column, size):
                    matrix[row][j] -= value * matrix[column][j]
    return answer


# ---------------------------------------------------------------------------
# The seven-term Phi formula and the exact quartet identity.
# ---------------------------------------------------------------------------

KT = QQ.frac_field("t0", "t1", "t2", "t3")
t = list(KT.gens)
RU, u0, u1, u2, u3 = ring("u0,u1,u2,u3", KT)
u = [u0, u1, u2, u3]


def phi(nodes, values):
    a, b, c = nodes
    A, B, C = values
    return (
        -(a - b) * (a - c) * (b - c) * A * B * C
        + (a - b) * (a + b - 2 * c) * A * B
        - (a - c) * (a - 2 * b + c) * A * C
        - (b - c) * (2 * a - b - c) * B * C
        - 2 * (b - c) * A
        + 2 * (a - c) * B
        - 2 * (a - b) * C
    )


# First verify Phi itself against the 3 by 3 determinant.
A0, B0, C0 = RU.gens[:3]
aa, bb, cc = t[:3]
robin_matrix = [
    [A0, 1 + aa * A0, 2 * aa + aa**2 * A0],
    [B0, 1 + bb * B0, 2 * bb + bb**2 * B0],
    [C0, 1 + cc * C0, 2 * cc + cc**2 * C0],
]
robin_det = (
    robin_matrix[0][0]
    * (robin_matrix[1][1] * robin_matrix[2][2]
       - robin_matrix[1][2] * robin_matrix[2][1])
    - robin_matrix[0][1]
    * (robin_matrix[1][0] * robin_matrix[2][2]
       - robin_matrix[1][2] * robin_matrix[2][0])
    + robin_matrix[0][2]
    * (robin_matrix[1][0] * robin_matrix[2][1]
       - robin_matrix[1][1] * robin_matrix[2][0])
)
assert robin_det == phi([aa, bb, cc], [A0, B0, C0])


def check_endpoint_reduction():
    """Check both endpoint shifts directly from the cleared nodal row."""
    field = QQ.frac_field("ti", "tj", "u", "r", "rp")
    ti, tj, value, r, rp = field.gens
    q = (tj - ti) * r
    qp = r + (tj - ti) * rp

    def cleared_row(x_value):
        return (
            (x_value**2 - tj**2) * (qp + value * q)
            - (x_value - 3 * tj) * q
        )

    plus = rp + (value - 2 / (ti + tj)) * r
    minus = rp + (
        value - 1 / (ti + tj) - 1 / (tj - ti)
    ) * r
    common_scale = -(tj - ti) ** 2 * (ti + tj)
    assert cleared_row(ti) == common_scale * plus
    assert cleared_row(-ti) == common_scale * minus

    # Equivalently, these are the finite Robin coefficients after dividing
    # q(z)=(z-ti)r(z).
    psi_plus = 1 / (ti - tj) - 2 / (ti + tj)
    psi_minus = 1 / (-ti - tj) - 2 / (-ti + tj)
    assert psi_plus + 1 / (tj - ti) == -2 / (ti + tj)
    assert psi_minus + 1 / (tj - ti) == (
        -1 / (ti + tj) - 1 / (tj - ti)
    )


check_endpoint_reduction()


def endpoint(i, sign):
    complement = [j for j in range(4) if j != i]
    values = []
    for j in complement:
        if sign == 1:
            value = u[j] - 2 / (t[j] + t[i])
        else:
            value = (
                u[j]
                - 1 / (t[j] + t[i])
                - 1 / (t[j] - t[i])
            )
        values.append(value)
    return phi([t[j] for j in complement], values)


left = RU.zero
for i in range(4):
    complement = [j for j in range(4) if j != i]
    delta = KT.one
    for p in range(3):
        for q in range(p + 1, 3):
            delta *= t[complement[q]] - t[complement[p]]
    left += (endpoint(i, 1) - endpoint(i, -1)) / (t[i] * delta)

sum_of_pair_sums = KT.one
for i in range(4):
    for j in range(i + 1, 4):
        sum_of_pair_sums *= t[i] + t[j]

right = RU.zero
for i in range(4):
    sigma = KT.one
    for j in range(4):
        if j != i:
            sigma *= t[i] + t[j]
    right += sigma * u[i]
right *= KT(-6) / sum_of_pair_sums
assert left == right


# ---------------------------------------------------------------------------
# Five quartet equations are exactly B_C v = 0.
# ---------------------------------------------------------------------------

K5 = QQ.frac_field("z0", "z1", "z2", "z3", "z4")
z = list(K5.gens)
sigma5 = []
for i in range(5):
    value = K5.one
    for j in range(5):
        if j != i:
            value *= z[i] + z[j]
    sigma5.append(value)

for m in range(5):
    for i in range(5):
        if i == m:
            continue
        quartet_coefficient = K5.one
        for j in range(5):
            if j != i and j != m:
                quartet_coefficient *= z[i] + z[j]
        assert quartet_coefficient == sigma5[i] / (z[i] + z[m])


# ---------------------------------------------------------------------------
# The moving fifth-anchor determinant has a nonzero numerator of degree <= 6.
# ---------------------------------------------------------------------------

KQ = QQ.frac_field("q0", "q1", "q2", "q3")
q = list(KQ.gens)
RX, x = ring("x", KQ)
H = [
    [KQ.zero if i == j else 1 / (q[i] + q[j]) for j in range(4)]
    for i in range(4)
]


def matrix_minor(matrix, deleted_row, deleted_column):
    return [
        [entry for j, entry in enumerate(row) if j != deleted_column]
        for i, row in enumerate(matrix)
        if i != deleted_row
    ]


def laplace_determinant(matrix):
    """Division-free determinant, used for the universal block identity."""
    size = len(matrix)
    if size == 1:
        return matrix[0][0]
    answer = matrix[0][0] * 0
    for column, entry in enumerate(matrix[0]):
        minor = [
            row[:column] + row[column + 1:]
            for row in matrix[1:]
        ]
        term = entry * laplace_determinant(minor)
        answer = answer - term if column % 2 else answer + term
    return answer


def check_universal_block_identity():
    """Verify det[[H,w],[w^T,0]]=-w^T adj(H)w polynomially."""
    block_ring, *generators = ring(
        "b01,b02,b03,b12,b13,b23,w0,w1,w2,w3", QQ
    )
    b01, b02, b03, b12, b13, b23, w0, w1, w2, w3 = generators
    base = [
        [block_ring.zero, b01, b02, b03],
        [b01, block_ring.zero, b12, b13],
        [b02, b12, block_ring.zero, b23],
        [b03, b13, b23, block_ring.zero],
    ]
    w = [w0, w1, w2, w3]
    bordered = [base[i] + [w[i]] for i in range(4)]
    bordered.append(w + [block_ring.zero])

    adjugate_base = []
    for i in range(4):
        row = []
        for j in range(4):
            cofactor = laplace_determinant(matrix_minor(base, j, i))
            row.append(-cofactor if (i + j) % 2 else cofactor)
        adjugate_base.append(row)

    quadratic_form = sum(
        w[i] * adjugate_base[i][j] * w[j]
        for i in range(4)
        for j in range(4)
    )
    assert laplace_determinant(bordered) == -quadratic_form


check_universal_block_identity()


adjugate = []
for i in range(4):
    row = []
    for j in range(4):
        # adj(H)_{ij} is the (j,i)-cofactor.
        cofactor = determinant(matrix_minor(H, j, i), KQ)
        if (i + j) % 2:
            cofactor = -cofactor
        row.append(cofactor)
    adjugate.append(row)

common_denominator = RX.one
for qi in q:
    common_denominator *= (x + qi) ** 2

numerator = RX.zero
for i in range(4):
    for j in range(4):
        divisor = (x + q[i]) * (x + q[j])
        numerator -= adjugate[i][j] * common_denominator.exquo(divisor)

assert numerator.degree() <= 6
for i in range(4):
    other = [j for j in range(4) if j != i]
    expected_diagonal = KQ(2)
    for p in range(3):
        for r in range(p + 1, 3):
            expected_diagonal /= q[other[p]] + q[other[r]]
    assert adjugate[i][i] == expected_diagonal

    expected_value = -expected_diagonal
    for j in other:
        expected_value *= (q[j] - q[i]) ** 2
    assert numerator.evaluate(x, -q[i]) == expected_value

assert numerator


# ---------------------------------------------------------------------------
# Sharp cardinality bookkeeping and the final quadratic fibre.
# ---------------------------------------------------------------------------

minimum_p = 7
number_of_exceptional_anchors = minimum_p + 8
number_of_nonzero_anchors = number_of_exceptional_anchors - 1
sixth_anchor_roots = number_of_exceptional_anchors - 5
fifth_anchor_candidates = number_of_exceptional_anchors - 4 - 1
good_fifth_anchors = fifth_anchor_candidates - 6

assert number_of_nonzero_anchors >= 4
assert sixth_anchor_roots == minimum_p + 3
assert sixth_anchor_roots > 8
assert fifth_anchor_candidates == minimum_p + 3
assert good_fifth_anchors == minimum_p - 3
assert good_fifth_anchors >= 4
assert good_fifth_anchors > 2

KF = QQ.frac_field("a", "lambda", "y")
a, lam, y = KF.gens
psi = -(y + 3 * a) / (y**2 - a**2)
fibre_polynomial = lam * (y**2 - a**2) + y + 3 * a
assert psi - lam == -fibre_polynomial / (y**2 - a**2)

KY = QQ.frac_field("a", "lambda")
a0, lam0 = KY.gens
RY, yy = ring("y", KY)
fibre_polynomial_y = lam0 * (yy**2 - a0**2) + yy + 3 * a0
assert fibre_polynomial_y
assert fibre_polynomial_y.degree() <= 2
assert fibre_polynomial_y.coeff(yy) == KY.one

print("verified the seven-term Phi determinant")
print("verified both endpoint reductions and the universal block identity")
print("verified the signed quartet identity over QQ(t0,t1,t2,t3)")
print("verified the five-quartet Cauchy coefficient conversion")
print("verified the nonzero degree-six fifth-anchor numerator")
print("verified the root counts and the quadratic-fibre contradiction")
