#!/usr/bin/env python3
"""Exact audit of the generic endpoint-span certificate for DR4.

All arithmetic is in QQ(a,b,c).  The script constructs the endpoint
polynomials, performs the degree filtration described in the companion note,
and verifies the two factored 10 by 10 minors used there.
"""

from sympy.polys.domains import QQ
from sympy.polys.rings import ring


K = QQ.frac_field("a", "b", "c")
a, b, c = K.gens
R, u0, u1, u2, u3 = ring("u0,u1,u2,u3", K)
u = [u0, u1, u2, u3]
t = [K.one, a, b, c]


def phi(nodes, values):
    """The determinant of three quadratic Robin-evaluation rows."""
    x, y, z = nodes
    A, B, C = values
    return (
        -(x - y) * (x - z) * (y - z) * A * B * C
        + (x - y) * (x + y - 2 * z) * A * B
        - (x - z) * (x - 2 * y + z) * A * C
        - (y - z) * (2 * x - y - z) * B * C
        - 2 * (y - z) * A
        + 2 * (x - z) * B
        - 2 * (x - y) * C
    )


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


# Columns in decreasing degree.  A bit mask records a squarefree monomial.
MASKS = [15, 7, 11, 13, 14, 3, 5, 6, 9, 10, 12, 1, 2, 4, 8]
MONOMIALS = [tuple((mask >> i) & 1 for i in range(4)) for mask in MASKS]


def vector(poly):
    return [poly.get(monomial, K.zero) for monomial in MONOMIALS]


def add(left, right, scalar=K.one):
    return [x + scalar * y for x, y in zip(left, right)]


def scale(row, scalar):
    return [scalar * x for x in row]


def determinant(matrix):
    """Gaussian determinant over the exact fraction field K."""
    matrix = [row[:] for row in matrix]
    size = len(matrix)
    answer = K.one
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


e_plus = [endpoint(i, 1) for i in range(4)]
e_minus = [endpoint(i, -1) for i in range(4)]

# Normalize the unique cubic coefficient of E_i^+ to one.
A = []
D = []
uA = []
uD = []
for i in range(4):
    cubic_column = 4 - i
    gamma = vector(e_plus[i])[cubic_column]
    Ai = e_plus[i] / gamma
    Di = (e_plus[i] - e_minus[i]) / gamma
    A.append(vector(Ai))
    D.append(vector(Di))
    uA.append(vector(u[i] * Ai))
    uD.append(vector(u[i] * Di))


def remove_cubics(row):
    for i in range(4):
        row = add(row, A[i], -row[4 - i])
    return row


# After the four cubic pivots A_i and the quartic pivot u_0 A_0, these
# are the eleven rows supported in degrees at most two.
low_rows = (
    [remove_cubics(add(uA[i], uA[0], -1)) for i in range(1, 4)]
    + D
    + [remove_cubics(row) for row in uD]
)
assert all(all(not entry for entry in row[:5]) for row in low_rows)
L = [row[5:] for row in low_rows]

# Delete low row 8 = overline(u_1 D_1), respectively row 9 =
# overline(u_2 D_2).
M8 = determinant([row for i, row in enumerate(L) if i != 8])
M9 = determinant([row for i, row in enumerate(L) if i != 9])

rho = (a - b * c) * (a * b - c) * (a * c - b)
P2 = (
    3 * a**3 * b * c
    - a**2 * b**2 * c**2
    + 4 * a**2 * b**2 * c
    - a**2 * b**2
    + 4 * a**2 * b * c**2
    + 4 * a**2 * b * c
    - a**2 * c**2
    - a * b**3 * c
    + 4 * a * b**2 * c**2
    + 4 * a * b**2 * c
    - a * b * c**3
    + 4 * a * b * c**2
    - a * b * c
    + 3 * b**2 * c**2
)
P3 = (
    a**3 * b * c
    + a**2 * b**2 * c**2
    - 4 * a**2 * b**2 * c
    + a**2 * b**2
    - 4 * a**2 * b * c**2
    - 4 * a**2 * b * c
    - 3 * a**2 * c**2
    - 3 * a * b**3 * c
    - 4 * a * b**2 * c**2
    - 4 * a * b**2 * c
    + a * b * c**3
    - 4 * a * b * c**2
    + a * b * c
    + b**2 * c**2
)

den8 = (
    (a - 1)
    * (a + 1) ** 5
    * (b - 1) ** 2
    * (b + 1) ** 5
    * (c - 1) ** 2
    * (c + 1) ** 5
    * (a - b)
    * (a + b) ** 5
    * (a - c)
    * (a + c) ** 5
    * (b - c) ** 2
    * (b + c) ** 5
)
den9 = (
    (a - 1) ** 2
    * (a + 1) ** 5
    * (b - 1)
    * (b + 1) ** 5
    * (c - 1) ** 2
    * (c + 1) ** 5
    * (a - b)
    * (a + b) ** 5
    * (a - c) ** 4
    * (a + c) ** 5
    * (b - c)
    * (b + c) ** 5
)
constant = K(2**19 * 3**3)
# These are the factorizations for the row normalization above.  An older
# stored normalization missed a common factor -1/4 and, for M9, the
# structural factor (a-c)^2 introduced by this low-row ordering.
expected_M8 = -constant * a * b**2 * c**2 * rho * P2 / (4 * den8)
expected_M9 = (
    constant * a**2 * b * c**2 * (a - c) ** 2 * rho * P3
    / (4 * den9)
)

assert M8 == expected_M8
assert M9 == expected_M9
assert M8 and M9
assert P2 + P3 == 4 * c * (a - b) * (a + b) * (a * b - c)

print("verified exact endpoint construction and degree filtration")
print("verified normalized M8 and M9 factorizations over QQ(a,b,c)")
print("verified P2 + P3 = 4*c*(a-b)*(a+b)*(a*b-c)")
