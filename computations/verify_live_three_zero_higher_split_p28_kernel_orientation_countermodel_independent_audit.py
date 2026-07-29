#!/usr/bin/env python3
"""Independent exact audit of the p=28 kernel-orientation countermodel.

This script reconstructs the displayed E/O model directly over QQ.  It does
not import the primary verifier or any project computation module.
"""

from itertools import combinations

import sympy as sp


tau, z = sp.symbols("tau z")


def basis_vector(index: int) -> sp.Matrix:
    return sp.eye(6)[:, index]


zero = sp.zeros(6, 1)
e = [basis_vector(j) for j in range(6)]

E_coeff = [e[0], e[2], zero, e[4], e[0]]
O_coeff = [
    e[1],
    zero,
    e[3],
    -e[4] - sp.Rational(1, 2) * e[3] - sp.Rational(1, 16) * e[1],
    -e[0]
    + sp.Rational(9, 128) * e[1]
    + sp.Rational(3, 8) * e[3]
    + sp.Rational(1, 2) * e[4]
    + e[5],
]

E = sum((E_coeff[j] * tau**j for j in range(5)), zero)
O = sum((O_coeff[j] * tau**j for j in range(5)), zero)


def taylor_column(vector: sp.Matrix, order: int) -> sp.Matrix:
    return sp.Matrix(
        [sp.Poly(sp.expand(entry), tau).coeff_monomial(tau**order) for entry in vector]
    )


# Six jets require the square-root series through order six.  Taylor
# coefficients rather than factorial-scaled derivatives have the same ranks.
sqrt_series = sum(
    (sp.binomial(sp.Rational(1, 2), j) * tau**j for j in range(7)),
    sp.Integer(0),
)


def sheet_data(sign: int) -> tuple[list[int], list[int]]:
    G = sp.expand(E + sign * sqrt_series * O)
    jets = [taylor_column(G, j) for j in range(7)]
    ranks = [sp.Matrix.hstack(*jets[: j + 1]).rank() for j in range(7)]
    pivots = [j for j, rank in enumerate(ranks) if rank > (ranks[j - 1] if j else 0)]
    return ranks, pivots


plus_ranks, plus_pivots = sheet_data(+1)
minus_ranks, minus_pivots = sheet_data(-1)

assert plus_ranks == [1, 2, 3, 3, 4, 5, 6]
assert plus_pivots == [0, 1, 2, 4, 5, 6]
assert sum(order - j for j, order in enumerate(plus_pivots)) == 3

assert minus_ranks[:6] == [1, 2, 3, 4, 5, 6]
assert minus_pivots[:6] == [0, 1, 2, 3, 4, 5]
assert sum(order - j for j, order in enumerate(minus_pivots[:6])) == 0


# Reconstruct the kernel of eta_0 without using the displayed answer.  A
# covector basis annihilating L_0 turns E'(0),O'(0) into a quotient matrix.
E0 = E.subs(tau, 0)
O0 = O.subs(tau, 0)
E1 = E.diff(tau).subs(tau, 0)
O1 = O.diff(tau).subs(tau, 0)
L0 = sp.Matrix.hstack(E0, O0)
annihilators = sp.Matrix.hstack(*L0.T.nullspace()).T
eta_matrix = annihilators * sp.Matrix.hstack(E1, O1)
eta_kernel = eta_matrix.nullspace()

assert L0.rank() == 2
assert sp.Matrix.hstack(E0, O0, E1, O1).rank() == 3
assert eta_matrix.rank() == 1
assert len(eta_kernel) == 1
assert eta_kernel[0][0] == 0 and eta_kernel[0][1] != 0


# The scalar gcd of the nonzero Pluecker coordinates is exactly tau.
derivative_wedge_matrix = sp.Matrix.hstack(E, O, E.diff(tau), O.diff(tau))
four_minors = []
for rows in combinations(range(6), 4):
    minor = sp.factor(derivative_wedge_matrix[list(rows), :].det())
    if minor != 0:
        four_minors.append(sp.Poly(minor, tau, domain=sp.QQ))

minor_gcd = four_minors[0]
for minor in four_minors[1:]:
    minor_gcd = sp.gcd(minor_gcd, minor)

assert len(four_minors) == 12
assert sp.expand(minor_gcd.monic().as_expr() - tau) == 0


# The square-cover expression really is a six-dimensional polynomial space
# within the saturated degree-nine cap.
F = sp.Matrix(
    [sp.expand(E[j].subs(tau, z**2 - 1) + z * O[j].subs(tau, z**2 - 1)) for j in range(6)]
)
coefficient_matrix = sp.Matrix(
    [[sp.Poly(F[col], z).coeff_monomial(z**row) for col in range(6)] for row in range(10)]
)

assert max(sp.degree(entry, z) for entry in F) <= 9
assert coefficient_matrix.rank() == 6

print("p=28 kernel-orientation countermodel independent audit: PASS")
print(f"plus ranks={plus_ranks}, pivots={plus_pivots}, weight=3")
print(f"minus ranks={minus_ranks[:6]}, pivots={minus_pivots[:6]}, weight=0")
print("kernel(eta_0)=[0:1], wedge gcd=tau, polynomial rank=6, degree cap=9")
