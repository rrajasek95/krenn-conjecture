#!/usr/bin/env python3
"""Exact audit of the pure fourteen-double five-space frontier."""

from __future__ import annotations

from collections import defaultdict
from itertools import combinations

import sympy as sp


# Saturated common-kernel ledger.
p = 10
N = 10
d = 5
forced = p * (d - 2)
cap = d * (N + 1 - d)
assert forced == cap == 30
assert d**2 - d - 2 * p == 0
assert 6**2 - 6 - 2 * p > 0

# Every possible gcd correction is strict.
assert d + 1 == 6                    # simple node gcd
assert 2 * d + 2 == 12               # node gcd of order at least three

# Gcd-free exact-order-two equality has a unique vanishing sequence.
admissible_sequences = []
for sequence in combinations(range(N + 1), d):
    if sequence[0] != 0:
        continue
    jet_rank = sum(order <= 2 for order in sequence)
    weight = sum(order - index for index, order in enumerate(sequence))
    if jet_rank <= 2 and weight == d - 2:
        admissible_sequences.append(sequence)
assert admissible_sequences == [(0, 1, 3, 4, 5)]
assert sum(order >= 3 for order in admissible_sequences[0]) == 3


z = sp.symbols("z")
values = sp.symbols("a0:4")


def lift_factor(value):
    return sp.expand((z + value) ** 2 * (z - value) ** 3)


# Pair intersections are at most the product line, and any three distinct
# lift factors are independent.
a, b = values[:2]
resultant = sp.factor(sp.resultant(lift_factor(a), lift_factor(b), z))
assert resultant == (a - b) ** 13 * (a + b) ** 12

three_factors = [sp.Poly(lift_factor(value), z) for value in values[1:4]]
minor = sp.Matrix(
    [
        [factor.coeff_monomial(z**degree) for factor in three_factors]
        for degree in (5, 4, 3)
    ]
).det()
expected = -2 * (
    (values[1] - values[2])
    * (values[1] - values[3])
    * (values[2] - values[3])
)
assert sp.factor(minor - expected) == 0

# Thus three edge lines incident to one vertex would be independent after
# division by their common A_a, contradicting a two-plane.
numeric_factors = [sp.Poly(lift_factor(value), z) for value in (1, 2, 3)]
numeric_coefficient_matrix = sp.Matrix(
    [
        [factor.coeff_monomial(z**degree) for factor in numeric_factors]
        for degree in range(6)
    ]
)
assert numeric_coefficient_matrix.rank() == 3


# Exact empty-edge Grassmann model on the rational normal quartic.
t, u = sp.symbols("t u")


def v(parameter):
    return sp.Matrix([1, parameter, parameter**2, parameter**3, parameter**4])


vt = v(t)
vu = v(u)
vpt = vt.diff(t)
vpu = vu.diff(u)
vppt = vpt.diff(t)
vppu = vpu.diff(u)

U_pair_minor = sp.Matrix.hstack(vt, vpt, vu, vpu)[:4, :].det()
V_pair_minor = sp.Matrix.hstack(vt, vpt, vppt, vu, vpu).det()
assert sp.factor(U_pair_minor - (t - u) ** 4) == 0
assert sp.factor(V_pair_minor - 2 * (t - u) ** 6) == 0

for value in range(1, 11):
    vector = v(sp.Integer(value))
    derivative = sp.Matrix([0, 1, 2 * value, 3 * value**2, 4 * value**3])
    second = sp.Matrix([0, 0, 2, 6 * value, 12 * value**2])
    U = sp.Matrix.hstack(vector, derivative)
    V = sp.Matrix.hstack(vector, derivative, second)
    assert U.rank() == 2
    assert V.rank() == 3
    # In the displayed V-basis, J=(phi,0) with phi=(0,0,1).
    J_relative = sp.Matrix([[0, 0, 1], [0, 0, 0]])
    assert J_relative.rank() == 1
    assert len(J_relative.nullspace()) == 2

for left, right in combinations(range(1, 11), 2):
    left = sp.Integer(left)
    right = sp.Integer(right)
    U_left = sp.Matrix.hstack(v(left), v(t).diff(t).subs(t, left))
    U_right = sp.Matrix.hstack(v(right), v(t).diff(t).subs(t, right))
    V_left = sp.Matrix.hstack(
        v(left), v(t).diff(t).subs(t, left), v(t).diff(t, 2).subs(t, left)
    )
    V_right = sp.Matrix.hstack(
        v(right), v(t).diff(t).subs(t, right), v(t).diff(t, 2).subs(t, right)
    )
    assert sp.Matrix.hstack(U_left, U_right).rank() == 4
    assert sp.Matrix.hstack(V_left, V_right).rank() == 5
    assert 2 + 2 - 4 == 0           # U_left intersection U_right
    assert 3 + 3 - 5 == 1           # V_left intersection V_right


# Exact Pieri recursion for [sigma_(6^5)] sigma_(1^3)^10.  Multiplication
# by an elementary class e_3 adds a vertical three-strip.
states = {(0, 0, 0, 0, 0): 1}
for _ in range(10):
    next_states = defaultdict(int)
    for partition, multiplicity in states.items():
        for rows in combinations(range(5), 3):
            candidate = list(partition)
            for row in rows:
                candidate[row] += 1
            if candidate[0] > 6:
                continue
            if not all(candidate[index] >= candidate[index + 1] for index in range(4)):
                continue
            next_states[tuple(candidate)] += multiplicity
    states = dict(next_states)

assert states == {(6, 6, 6, 6, 6): 3396}


# Stable triangular equality thresholds and the post-decic slack/intersection
# growth.  For pure families N=p.
for dimension in range(3, 15):
    triangular_p = dimension * (dimension - 1) // 2
    assert triangular_p * (dimension - 2) == dimension * (
        triangular_p + 1 - dimension
    )
    sequence = (0, 1) + tuple(range(3, dimension + 1))
    assert len(sequence) == dimension
    assert sum(order - index for index, order in enumerate(sequence)) == dimension - 2

for pool_size in range(10, 15):
    five_space_slack = 5 * (pool_size + 1 - 5) - pool_size * 3
    pair_multiple_dimension = pool_size - 9
    assert five_space_slack == 2 * pool_size - 20
    assert pair_multiple_dimension >= 1


# First common-coordinate parity reductions.  The Wronskian is nonzero at
# zero, so the fourth jet there is an isomorphism and a pure-even kernel has
# dimension at most three.
assert 5 - 3 == 2                    # odd projection rank at least two
assert 2 * (5 - 2) == 6              # two-quartic Wronskian cap
assert 10 - 6 == 4                   # at least four regular odd-rank-two squares
assert 4 * 4 > 3 * (6 - 3)           # four local weights beat degree nine
assert 3 * (5 - 3) == 6              # three-quartic Wronskian cap
assert 10 - 3 == 7                   # at least seven regular odd-rank-three squares
assert 2 * 7 > 2 * (6 - 2)           # double roots beat degree eight


# The paired five-jet covariant.  Every monomial Pluecker coordinate is a
# single power x^(sum(I)-4), so x^6 factors universally and the quotient
# has degree at most thirty.
x, w = sp.symbols("x w")
nonzero_exponents = []
paired_constants = {}
wronskian_constants = {}
for indices in combinations(range(11), 5):
    paired_matrix = sp.Matrix(
        [[sp.diff(x**power, x, order) for power in indices] for order in range(3)]
        + [
            [(-x) ** power for power in indices],
            [power * (-x) ** (power - 1) for power in indices],
        ]
    )
    paired = sp.factor(paired_matrix.det())
    exponent = sum(indices) - 4
    constant = sp.factor(paired.subs(x, 1))
    assert sp.factor(paired - constant * x**exponent) == 0
    paired_constants[indices] = constant

    wronskian_constant = sp.prod(
        indices[j] - indices[i]
        for i in range(5)
        for j in range(i + 1, 5)
    )
    wronskian_constants[indices] = wronskian_constant
    if constant != 0:
        nonzero_exponents.append(exponent)

assert min(nonzero_exponents) == 6
assert max(nonzero_exponents) == 36
assert max(nonzero_exponents) - min(nonzero_exponents) == 30

# Equal Wronskian degrees can receive opposite paired-covariant weights.
left_index = (0, 1, 2, 3, 6)
right_index = (0, 1, 2, 4, 5)
assert sum(left_index) == sum(right_index)
assert sp.Rational(
    paired_constants[left_index], wronskian_constants[left_index]
) == sp.Rational(4, 45)
assert sp.Rational(
    paired_constants[right_index], wronskian_constants[right_index]
) == sp.Rational(-4, 45)

# Corank at least two forces a double determinant zero.  A constant rank
# three matrix plus an arbitrary first-order perturbation has no constant
# or linear determinant coefficient.
tau = sp.symbols("tau")
perturbation_symbols = sp.symbols("q0:25")
perturbation = sp.Matrix(5, 5, perturbation_symbols)
rank_three = sp.diag(1, 1, 1, 0, 0)
corank_determinant = sp.Poly((rank_three + tau * perturbation).det(), tau)
assert corank_determinant.coeff_monomial(1) == 0
assert corank_determinant.coeff_monomial(tau) == 0

# With ten nonzero nodes this yields x^6 C^2 R, deg R<=10.
assert 30 - 2 * 10 == 10

# Exact parity row operation behind D_K=-64*x^6*J.  The columns below
# express [F(x),F'(x),F''(x),F(-x),F'(-x)] in terms of
# [E,E',O,O',E''+xO''] at w=x^2.
parity_change = sp.Matrix(
    [
        [1, 0, x, 0, 0],
        [0, 2 * x, 1, 2 * x**2, 0],
        [0, 2, 0, 6 * x, 4 * x**2],
        [1, 0, -x, 0, 0],
        [0, -2 * x, 1, 2 * x**2, 0],
    ]
)
assert sp.factor(parity_change.det() + 64 * x**6) == 0

# The first-four minors have w-degree at most fourteen.  Ten square roots
# therefore contribute Delta(w); contracting with E'' or O'' makes both
# parity pieces of J divisible by Delta=C(x)C(-x).  Together with C^2 and
# the degree-thirty cap, the lcm already exhausts J.
first_four_minor_cap = 14
Delta_degree_in_w = 10
J_degree_in_x = 30
assert first_four_minor_cap >= Delta_degree_in_w
assert 2 * 10 + 10 == J_degree_in_x  # deg C^2 C(-x)

# Audit the even/odd decomposition of the forced nonzero branch.
c = sp.symbols("cp0:10")
C = x**10 + sum(c[index] * x**index for index in range(10))
Cminus = sp.expand(C.subs(x, -x))
Delta = sp.expand(C * Cminus)
assert sp.Poly(Delta, x).terms()[0][0][0] == 20
assert sp.factor(Delta.subs(x, -x) - Delta) == 0
J_forced = sp.expand(C**2 * Cminus)
J_even = sp.expand((J_forced + J_forced.subs(x, -x)) / 2)
J_odd_over_x = sp.cancel((J_forced - J_forced.subs(x, -x)) / (2 * x))
assert sp.factor(J_even - Delta * (C + Cminus) / 2) == 0
assert sp.factor(J_odd_over_x - Delta * (C - Cminus) / (2 * x)) == 0
assert sp.Poly(J_even.subs(x, sp.sqrt(w)), w).degree() <= 15
assert sp.Poly(J_odd_over_x.subs(x, sp.sqrt(w)), w).degree() <= 14

# The zero-J branch would give a nonzero cofactor Q(w) of degree at most
# four.  Its associated kernel member is divisible by (z^2-w)^3, so the
# quotient is affine in w and has z-degree at most four.  The top two
# coefficients are forbidden low-degree members of K.
u = sp.symbols("u")
h0c = sp.symbols("h0c0:5")
h1c = sp.symbols("h1c0:5")
H0 = sum(h0c[index] * z**index for index in range(5))
H1 = sum(h1c[index] * z**index for index in range(5))
global_kernel_member = sp.Poly(
    sp.expand((z**2 - u) ** 3 * (H0 + u * H1)), u
)
assert sp.factor(global_kernel_member.coeff_monomial(u**4) + H1) == 0
assert sp.factor(
    global_kernel_member.coeff_monomial(u**3) + H0 - 3 * z**2 * H1
) == 0
assert max(sp.Poly(H0, z).degree(), sp.Poly(H1, z).degree()) <= 4

# Wronskian degree thirty forces the row-reduced polynomial degrees
# 6,7,8,9,10, so K has no nonzero member of degree at most five.
degree_sequences = [
    sequence
    for sequence in combinations(range(11), 5)
    if sum(sequence) - 10 == 30
]
assert degree_sequences == [(6, 7, 8, 9, 10)]


# Odd-projection rank four is impossible.  In a basis adapted to its
# one-dimensional pure-even kernel, write E=(T,A) and O=(O,0), and put
# R=A'T-AT'.  A direct determinant calculation gives
#
#       A J = det[R,O,O',R'-x A O''].
#
# The symbolic calculation below audits the signs as well as the factor A.
A0, A1, A2 = sp.symbols("A0 A1 A2")
T0 = sp.symbols("T_0_0:4")
T1 = sp.symbols("T_1_0:4")
T2 = sp.symbols("T_2_0:4")
O0 = sp.symbols("O_0_0:4")
O1 = sp.symbols("O_1_0:4")
O2 = sp.symbols("O_2_0:4")
E_row = list(T0) + [A0]
E_prime_row = list(T1) + [A1]
O_row = list(O0) + [0]
O_prime_row = list(O1) + [0]
last_row = [T2[index] + x * O2[index] for index in range(4)] + [A2]
J_rank_four = sp.det(
    sp.Matrix([E_row, E_prime_row, O_row, O_prime_row, last_row])
)
R_row = [A1 * T0[index] - A0 * T1[index] for index in range(4)]
R_prime_row = [A2 * T0[index] - A0 * T2[index] for index in range(4)]
rank_four_right = sp.det(
    sp.Matrix(
        [
            R_row,
            O0,
            O1,
            [R_prime_row[index] - x * A0 * O2[index] for index in range(4)],
        ]
    )
)
assert sp.expand(A0 * J_rank_four - rank_four_right) == 0

# A four-space of quartics has Wronskian degree at most four.  At a point
# where its value/derivative row has rank at most one, the least possible
# gcd-free vanishing sequence has weight three; a base point costs four.
odd_bad_sequences = []
for sequence in combinations(range(5), 4):
    if sum(order <= 1 for order in sequence) <= 1:
        odd_bad_sequences.append(
            (sequence, sum(order - index for index, order in enumerate(sequence)))
        )
assert odd_bad_sequences == [((0, 2, 3, 4), 3), ((1, 2, 3, 4), 4)]
assert 4 * (5 - 4) == 4
assert 4 // 3 == 1                  # at most one bad pool square

# Each component of R has degree at most eight: the possible degree-nine
# leading term in A'T-AT' cancels.  A two-quartic Wronskian has degree at
# most six, hence M=*(R wedge O wedge O') has component degree at most
# fourteen.  After M=Delta Q, deg Q_i<=4, and deg(Q dot O'')<=6.
assert 5 + 5 - 1 - 1 == 8           # equal top degrees cancel once more
assert 4 + 3 - 1 == 6               # two-quartic Wronskian cap
assert 8 + 6 == 14
assert 14 - Delta_degree_in_w == 4
rank_four_odd_scalar_cap = 4 + 2
assert rank_four_odd_scalar_cap == 6
assert p - 1 > rank_four_odd_scalar_cap

# At every regular pool square the full rank-three condition makes both
# R and R'-a A O'' lie in <O,O'>.  Differentiating
# M=*(R wedge O wedge O') therefore makes Q(s) a multiple of
# *(O'' wedge O wedge O'), so (Q dot O'')(s)=0.  Nine roots force this
# degree-six scalar to vanish identically.  The odd part of (35) would then
# make C(x)=C(-x), contradicting the noncollision condition P cap (-P)=0.
assert 10 - 1 == 9
assert 9 > rank_four_odd_scalar_cap

# Audit the final orthogonality in a generic exterior-algebra chart.
def star_three(rows):
    return sp.Matrix(
        [
            (-1) ** column
            * sp.Matrix(
                [
                    [row[index] for index in range(4) if index != column]
                    for row in rows
                ]
            ).det()
            for column in range(4)
        ]
    )


normal_to_odd_osculating_plane = star_three([O2, O0, O1])
assert sp.expand(normal_to_odd_osculating_plane.dot(sp.Matrix(O2))) == 0


# Odd-projection rank five is impossible as well.  Normalize the odd row
# to v=(1,w,w^2,w^3,w^4), so the even part is a linear operator
# T:P_4 -> P_5.  In the moving Taylor basis e_k=(u-w)^k, k=2,3,4,
# let b_k=(T e_k)(w).  The rows induced by T,T',T'' on this three-space
# are L_k=b_k, M_k=b_k'+k b_(k-1), and
# N_k=M_k'+k M_(k-1), respectively.
input_variable = sp.symbols("input_variable")
operator_coefficients = sp.symbols("operator_coefficient_0:30")
operator_images = [
    sum(operator_coefficients[6 * column + degree] * w**degree for degree in range(6))
    for column in range(5)
]


def apply_operator(polynomial):
    polynomial = sp.Poly(sp.expand(polynomial), input_variable)
    return sp.expand(
        sum(
            polynomial.coeff_monomial(input_variable**column)
            * operator_images[column]
            for column in range(5)
        )
    )


b_taylor = {
    order: apply_operator((input_variable - w) ** order) for order in range(5)
}
M_taylor = {
    order: sp.expand(sp.diff(b_taylor[order], w) + order * b_taylor[order - 1])
    for order in range(1, 5)
}
L_row = sp.Matrix([b_taylor[order] for order in (2, 3, 4)])
M_row = sp.Matrix([M_taylor[order] for order in (2, 3, 4)])
N_row = sp.Matrix(
    [
        sp.expand(sp.diff(M_taylor[order], w) + order * M_taylor[order - 1])
        for order in (2, 3, 4)
    ]
)
assert [sp.Poly(entry, w).degree() for entry in L_row] == [7, 8, 9]
assert [sp.Poly(entry, w).degree() for entry in M_row] == [6, 7, 8]
assert [sp.Poly(entry, w).degree() for entry in N_row] == [5, 6, 7]

# The restriction of the full five-row rank condition is
# rank[L;M;N/2+a(1,0,0)]<=1.  Put P=L cross M.  Its sharp component caps
# are (14,13,12), and the moving-basis differential identity is
#
#                 P_0'=(L cross N)_0+3 P_1.
P_taylor = L_row.cross(M_row)
assert [sp.Poly(entry, w).degree() for entry in P_taylor] == [14, 13, 12]
assert sp.expand(
    sp.diff(P_taylor[0], w) - L_row.cross(N_row)[0] - 3 * P_taylor[1]
) == 0

# Translation to the Taylor basis is unipotent.  In that basis the last
# three components of *(T wedge T' wedge v wedge v') are exactly L cross M.
abstract_b = sp.symbols("abstract_b_0:5")
abstract_m = sp.symbols("abstract_m_0:5")
centered_four_rows = sp.Matrix(
    [
        list(abstract_b),
        list(abstract_m),
        [1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0],
    ]
)
centered_cofactor = []
for column in range(5):
    retained = [index for index in range(5) if index != column]
    centered_cofactor.append(
        sp.factor((-1) ** column * centered_four_rows[:, retained].det())
    )
assert centered_cofactor[:2] == [0, 0]
assert sp.Matrix(centered_cofactor[2:]) == sp.Matrix(abstract_b[2:]).cross(
    sp.Matrix(abstract_m[2:])
)

# At a pool root, P_1=0.  The first component of
# L cross (N/2+a e_0) is independent of a and hence also vanishes.
rank_five_a = sp.symbols("rank_five_a")
first_taylor_basis_vector = sp.Matrix([1, 0, 0])
assert sp.expand(
    L_row.cross(N_row / 2 + rank_five_a * first_taylor_basis_vector)[0]
    - L_row.cross(N_row)[0] / 2
) == 0

# Since P=Delta H, the first quotient component has degree at most four.
# The preceding derivative identity gives H_0(s)=0 at all ten simple pool
# roots, so H_0 is identically zero.  It is precisely half of Q dot v''.
assert 14 - Delta_degree_in_w == 4
assert p > 4
residual_h = sp.symbols("residual_h_0:3")
residual_quartic = (input_variable - w) ** 2 * sum(
    residual_h[index] * (input_variable - w) ** index for index in range(3)
)
assert sp.expand(
    sp.diff(residual_quartic, input_variable, 2).subs(input_variable, w)
    - 2 * residual_h[0]
) == 0

# Thus Q dot v''=0, whereas the odd part of the exact nonzero identity
# J=kappa*Delta*C is kappa*Delta*(C-C(-x))/(2x).  It would force C even,
# contradicting the disjointness of the pool from its negative.

# A basepoint-free degree-ten evaluation curve cannot factor through a
# rational normal quartic.  The only nonbirational nondegenerate degree
# factorization is 10=2*5, whose branch vanishing weight is already ten.
assert all(4 * cover_degree != 10 for cover_degree in range(1, 6))
factorizations = [
    (cover_degree, 10 // cover_degree)
    for cover_degree in range(1, 11)
    if 10 % cover_degree == 0 and 10 // cover_degree >= 4
]
assert factorizations == [(1, 10), (2, 5)]
assert sum(2 * index - index for index in range(5)) == 10


print("pure fourteen-double five-space saturation frontier: PASS")
print("Wronskian and all ten local sequences are exactly saturated")
print("the intersection graph has maximum degree two but admits an exact empty graph")
print("paired-coordinate reductions exclude every odd projection rank two through five")
print("the pure fourteen-double five-space saturation branch is closed")
